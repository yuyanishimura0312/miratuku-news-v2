// Cloudflare Worker routes for Miratuku News foresight features
// These handlers should be integrated into the main worker/index.js
//
// Required secrets (already configured in existing worker):
//   ANTHROPIC_API_KEY - Anthropic API key
//
// New routes:
//   POST /api/foresight         - Ask a foresight question with context
//   POST /api/foresight-builder - Build insight from bookmarked articles

// Allowed origins for CORS — restrict to known deploy URLs only
const ALLOWED_ORIGINS = [
  'https://yuyanishimura0312.github.io',
  'https://future-insight-proxy.nishimura-69a.workers.dev',
  'https://future-insight-proxy.yuyanishimura0312.workers.dev',
];

// Validate the request Origin header and return restricted CORS headers.
// Returns null if the origin is not allowed (caller should return 403).
function getCorsHeaders(request) {
  const origin = request.headers.get('Origin') || '';
  if (!ALLOWED_ORIGINS.includes(origin)) {
    return null;
  }
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-User-Id',
    'Access-Control-Max-Age': '86400',
  };
}

// Stricter rate limit for foresight: 5 requests/min/user
const foresightRateLimits = new Map();
const FORESIGHT_RATE_WINDOW = 60 * 1000;
const FORESIGHT_RATE_MAX = 5;

function checkForesightRateLimit(userId) {
  const now = Date.now();
  const key = `foresight_${userId || 'anonymous'}`;
  const entry = foresightRateLimits.get(key);

  if (!entry || now - entry.windowStart > FORESIGHT_RATE_WINDOW) {
    foresightRateLimits.set(key, { windowStart: now, count: 1 });
    return true;
  }
  if (entry.count >= FORESIGHT_RATE_MAX) return false;
  entry.count++;
  return true;
}

// Periodically clean up stale entries
function cleanupForesightRateLimits() {
  const now = Date.now();
  for (const [key, entry] of foresightRateLimits) {
    if (now - entry.windowStart > FORESIGHT_RATE_WINDOW * 2) {
      foresightRateLimits.delete(key);
    }
  }
}

// Build the system prompt for foresight questions
function buildForesightPrompt(claContext, signalsContext, newsContext, userQuestion) {
  return `あなたは未来洞察の専門家です。以下のデータを基に、ユーザーの問いかけに対して深い洞察を提供してください。

## 基盤データ
${claContext || '（CLA分析データなし）'} - CLA分析の要約
${signalsContext || '（シグナルデータなし）'} - 弱いシグナルの要約
${newsContext || '（ニュースデータなし）'} - 最新のPESTLEニュースの要約

## ユーザーの問いかけ
${userQuestion}

## 回答指針
- 因果階層分析の4層（リタニー、社会的原因、ディスコース、神話/メタファー）の観点から回答
- 注目すべきシグナルとの関連を示す
- 未来の可能性について複数のシナリオを提示
- 日本語で5,000字程度で回答`;
}

// Build the system prompt for bookmark-based insight
function buildInsightPrompt(bookmarks) {
  const articleList = bookmarks
    .map((b, i) => `${i + 1}. [${b.category || 'N/A'}] ${b.title}`)
    .join('\n');

  return `あなたは未来洞察の専門家であり、因果階層分析（CLA）のスペシャリストです。
以下のブックマークされた記事・シグナル群を基に、横断的な未来洞察を生成してください。

## ブックマークされた資料
${articleList}

## タスク
1. **CLA対比分析**: ブックマークされた資料を因果階層分析の4層（リタニー、社会的原因、ディスコース/世界観、神話/メタファー）で整理し、層間の関係性を分析してください。
2. **横断テーマ**: 複数の資料に共通する深層テーマやパターンを抽出してください。
3. **注目シグナル**: これらの資料の組み合わせから見えてくる弱いシグナルや新興トレンドを提案してください。
4. **シナリオ提示**: これらの情報が示唆する2-3の未来シナリオを描写してください。

日本語で回答してください。`;
}

// POST /api/foresight — Foresight question handler
async function handleForesight(request, env, _corsHeaders) {
  // Use origin-restricted CORS headers instead of the permissive ones from caller
  const corsHeaders = getCorsHeaders(request);
  if (!corsHeaders) {
    return new Response(JSON.stringify({ error: 'Origin not allowed' }), {
      status: 403,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST required' }), {
      status: 405,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }

  if (!env.ANTHROPIC_API_KEY) {
    return new Response(JSON.stringify({ error: 'ANTHROPIC_API_KEY not configured' }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }

  // Rate limit: 5 requests/min/user
  const userId = request.headers.get('X-User-Id') || 'unknown';
  if (!checkForesightRateLimit(userId)) {
    return new Response(
      JSON.stringify({ error: 'Rate limit exceeded (max 5 requests/min). Please wait.' }),
      { status: 429, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON body' }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }

  const { question, claContext, signalsContext, newsContext } = body;

  if (!question || typeof question !== 'string' || question.trim().length === 0) {
    return new Response(JSON.stringify({ error: 'question is required' }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }

  // Cap question length to prevent prompt injection via very long inputs
  const trimmedQuestion = question.trim().slice(0, 2000);

  const prompt = buildForesightPrompt(claContext, signalsContext, newsContext, trimmedQuestion);

  try {
    const anthropicResp = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 8000,
        messages: [{ role: 'user', content: prompt }],
      }),
    });

    const data = await anthropicResp.json();

    if (!anthropicResp.ok) {
      return new Response(JSON.stringify({ error: 'Anthropic API error', detail: data }), {
        status: anthropicResp.status,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // Extract text from response
    const answerText =
      data.content && data.content.length > 0
        ? data.content.map((block) => block.text || '').join('')
        : '';

    return new Response(
      JSON.stringify({
        answer: answerText,
        model: data.model,
        usage: data.usage,
      }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  } catch (e) {
    return new Response(JSON.stringify({ error: 'Failed to call Anthropic API', detail: e.message }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }
}

// POST /api/foresight-builder — Build insight from bookmarks
async function handleForesightBuilder(request, env, _corsHeaders) {
  const corsHeaders = getCorsHeaders(request);
  if (!corsHeaders) {
    return new Response(JSON.stringify({ error: 'Origin not allowed' }), {
      status: 403,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST required' }), {
      status: 405,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }

  if (!env.ANTHROPIC_API_KEY) {
    return new Response(JSON.stringify({ error: 'ANTHROPIC_API_KEY not configured' }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }

  const userId = request.headers.get('X-User-Id') || 'unknown';
  if (!checkForesightRateLimit(userId)) {
    return new Response(
      JSON.stringify({ error: 'Rate limit exceeded (max 5 requests/min). Please wait.' }),
      { status: 429, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON body' }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }

  const { bookmarks } = body;

  if (!Array.isArray(bookmarks) || bookmarks.length === 0) {
    return new Response(JSON.stringify({ error: 'bookmarks array is required and must not be empty' }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }

  // Limit to 50 bookmarks to keep prompt size reasonable
  const limitedBookmarks = bookmarks.slice(0, 50);
  const prompt = buildInsightPrompt(limitedBookmarks);

  try {
    const anthropicResp = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 8000,
        messages: [{ role: 'user', content: prompt }],
      }),
    });

    const data = await anthropicResp.json();

    if (!anthropicResp.ok) {
      return new Response(JSON.stringify({ error: 'Anthropic API error', detail: data }), {
        status: anthropicResp.status,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    const answerText =
      data.content && data.content.length > 0
        ? data.content.map((block) => block.text || '').join('')
        : '';

    return new Response(
      JSON.stringify({
        insight: answerText,
        model: data.model,
        usage: data.usage,
        bookmarkCount: limitedBookmarks.length,
      }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  } catch (e) {
    return new Response(JSON.stringify({ error: 'Failed to call Anthropic API', detail: e.message }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }
}

// POST /api/regenerate-report — Regenerate an insight report with structured JSON output
async function handleRegenerateReport(request, env, _corsHeaders) {
  const corsHeaders = getCorsHeaders(request);
  if (!corsHeaders) {
    return new Response(JSON.stringify({ error: 'Origin not allowed' }), {
      status: 403,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST required' }), {
      status: 405,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }

  if (!env.ANTHROPIC_API_KEY) {
    return new Response(JSON.stringify({ error: 'ANTHROPIC_API_KEY not configured' }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }

  const userId = request.headers.get('X-User-Id') || 'unknown';
  if (!checkForesightRateLimit(userId)) {
    return new Response(
      JSON.stringify({ error: 'Rate limit exceeded (max 5 requests/min). Please wait.' }),
      { status: 429, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON body' }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }

  const { article, existingReport, category } = body;

  if (!article && !existingReport) {
    return new Response(JSON.stringify({ error: 'article or existingReport is required' }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }

  // Build structured regeneration prompt
  const prompt = `あなたは因果階層分析（CLA）を専門とする未来洞察の専門家です。以下のニュース記事について、インサイトレポートを生成してください。

## 記事情報
タイトル: ${article?.title || ''}
${article?.title_ja ? '日本語タイトル: ' + article.title_ja : ''}
出典: ${article?.source || ''} (${article?.published_date || ''})
要約: ${article?.summary || ''}
PESTLEカテゴリ: ${category || article?.pestle_category || ''}

${existingReport ? '## 既存レポート（改善・刷新の対象）\n' + existingReport.substring(0, 3000) + '\n' : ''}

## 出力要件
必ず以下のJSON形式のみを出力してください（他のテキストは不要です）：

{
  "title": "レポートタイトル（日本語、40字以内）",
  "summary": "要約（日本語、150字以内、読者の関心を引くリード文）",
  "full_report": "本文（日本語、2000〜4000字、散文形式、マークダウン可。CLA4層の視点から深層分析）",
  "historical_context": "歴史的経緯（マークダウン可、500〜1000字）",
  "future_signals": "未来へのシグナル分析（マークダウン可、500〜1000字）",
  "watch_points": "今後ウォッチすべきポイント（マークダウン可、300〜500字）",
  "related_myth": "関連する神話・メタファー（1文）",
  "myth_relation": "strengthens または changes",
  "timeline": [{"year": "年", "event": "出来事", "significance": "意義"}],
  "related_research": [{"title": "論文/書籍名", "author": "著者", "comment": "この記事との関連を説明するコメント"}]
}

## 注意事項
- 読者は経営者・コンサルタント。知的かつ実用的な洞察を提供
- full_reportは散文形式（箇条書きのみは不可）
- timelineは3〜6件、related_researchは2〜3件
- JSONのみを出力。マークダウンのコードブロックで囲まないこと`;

  try {
    const anthropicResp = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 8000,
        messages: [{ role: 'user', content: prompt }],
      }),
    });

    const data = await anthropicResp.json();

    if (!anthropicResp.ok) {
      return new Response(JSON.stringify({ error: 'Anthropic API error', detail: data }), {
        status: anthropicResp.status,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    const answerText =
      data.content && data.content.length > 0
        ? data.content.map((block) => block.text || '').join('')
        : '';

    // Try to parse as JSON for validation
    let parsed = null;
    try {
      // Strip markdown code blocks if present
      const cleaned = answerText.replace(/^```(?:json)?\s*/, '').replace(/\s*```$/, '').trim();
      parsed = JSON.parse(cleaned);
    } catch {
      // Return raw text if JSON parsing fails
      parsed = null;
    }

    return new Response(
      JSON.stringify({
        report: parsed,
        rawText: answerText,
        model: data.model,
        usage: data.usage,
      }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  } catch (e) {
    return new Response(JSON.stringify({ error: 'Failed to call Anthropic API', detail: e.message }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }
}

// Export handlers and cleanup for integration into main worker
export {
  handleForesight,
  handleForesightBuilder,
  handleRegenerateReport,
  cleanupForesightRateLimits,
  getCorsHeaders,
  ALLOWED_ORIGINS,
};

// Integration example for main worker/index.js:
// -------------------------------------------------
// import { handleForesight, handleForesightBuilder, handleRegenerateReport, cleanupForesightRateLimits } from './news-routes.js';
//
// In the fetch handler, add before the 404 fallback:
//
//   cleanupForesightRateLimits();
//
//   if (path === '/api/foresight') {
//     return handleForesight(request, env, corsHeaders);
//   }
//   if (path === '/api/foresight-builder') {
//     return handleForesightBuilder(request, env, corsHeaders);
//   }
//   if (path === '/api/regenerate-report') {
//     return handleRegenerateReport(request, env, corsHeaders);
//   }
