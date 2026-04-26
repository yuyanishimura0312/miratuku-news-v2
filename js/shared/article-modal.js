'use strict';

// ==============================================================
// FUTUROLOGY THEMES (18 categories)
// ==============================================================
var FUTUROLOGY_THEMES = [
  { no: 1,  name: 'イノベーションの分散と都市国家の誕生', map: '生態系化する社会',
    keywords: ['イノベーション', '都市国家', 'スタートアップ', 'オープンイノベーション', '分散', '都市化', 'グローバル市民', 'スマートシティ', 'innovation', 'startup', 'decentrali',
      'エコシステム', 'クラスター', 'シリコンバレー', 'テックハブ', 'ベンチャー', '起業', '産業集積', 'DAO', 'Web3', '特区', 'hub', 'ecosystem', 'venture', 'technopol', 'cluster', 'incubat', 'accelerat'] },
  { no: 2,  name: 'テクノロジーを用いた理想的身体機能の拡張', map: '技術と身体',
    keywords: ['身体拡張', '義肢', 'ウェアラブル', 'サイボーグ', '脳機械インターフェース', 'BCI', 'バイオハック', 'exoskeleton', 'prosthetic', 'augment', 'biohack',
      'インプラント', 'パワードスーツ', '人工臓器', '生体工学', 'ニューラリンク', 'haptic', 'implant', 'neuroprosthe', 'wearable', 'bioelectron', 'sensory', 'cochlear', 'retinal',
      'hearing aid', 'assistive', 'orthopedic', 'neuralink', 'human enhancement', 'body hack', 'smart glass', 'smart watch', 'health monitor', 'biosensor', 'brain implant', 'robotic limb', 'bionics', 'human augment'] },
  { no: 3,  name: 'テクノロジーの非人間的活用', map: '技術と倫理',
    keywords: ['監視', 'サイバー攻撃', '自律兵器', 'ドローン兵器', 'ディープフェイク', 'AI倫理', 'サイバーセキュリティ', 'surveillance', 'cyber weapon', 'deepfake', 'autonomous weapon',
      '顔認識', '情報操作', 'プロパガンダ', 'ランサムウェア', '偽情報', 'フェイクニュース', 'キラーロボット', 'スパイウェア', 'facial recognition', 'disinformation', 'misinformation', 'ransomware', 'spyware', 'lethal autonomous', 'weaponiz', 'malware', 'hack'] },
  { no: 4,  name: '資源のスマートコントロール', map: '資源と制御',
    keywords: ['スマートグリッド', '資源管理', 'エネルギー効率', 'IoT', 'スマート農業', '水資源', 'リサイクル', 'smart grid', 'resource', 'precision agriculture', 'circular economy',
      'エネルギー', '再生可能', '新エネルギー', '省エネ', '蓄電', 'バッテリー', '送電', '電力', '太陽光', '風力', '水素', 'レアメタル', '廃棄物', 'サプライチェーン', 'energy', 'renewable', 'solar', 'wind', 'hydrogen', 'battery', 'storage', 'grid', 'waste', 'recycl', 'sustain', 'efficien', 'conserv', 'water management', 'desalinat', 'rare earth', 'lithium', 'supply chain'] },
  { no: 5,  name: 'デジタルワールドと現実世界の融合', map: 'デジタルと現実',
    keywords: ['メタバース', 'VR ', 'XR ', 'デジタルツイン', '仮想現実', '拡張現実', 'NFT', 'metaverse', 'digital twin', 'mixed reality', 'virtual reality', 'virtual world',
      'ホログラム', '没入', 'アバター', 'ブロックチェーン', 'デジタルアート', 'バーチャル空間', 'hologram', 'immersive', 'avatar', 'spatial computing', 'blockchain', 'web3',
      'augmented reality', 'extended reality', '仮想空間', 'デジタル世界', 'crypto', 'decentralized app', 'smart contract', 'DAO '] },
  { no: 6,  name: 'ロボットによる自動化する社会', map: '自動化社会',
    keywords: ['ロボット', '自動化', '自動運転', 'RPA', 'ファクトリーオートメーション', '無人', 'AGV', 'robot', 'automat', 'autonomous', 'driverless', 'unmanned',
      'ドローン', '配送ロボット', '無人店舗', '工場自動化', '物流自動化', 'ロボティクス', 'drone', 'warehouse', 'logistics automat', 'robotic', 'self-driving', 'lidar', 'autopilot'] },
  { no: 7,  name: '宇宙に進出する人類', map: '宇宙開発',
    keywords: ['宇宙', '火星', '月面', '衛星', 'ロケット', 'SpaceX', 'NASA', 'JAXA', '宇宙旅行', 'space', 'mars', 'lunar', 'satellite', 'orbit',
      '宇宙ステーション', '小惑星', '宇宙資源', '軌道', 'スペースデブリ', '深宇宙', 'ISS', 'asteroid', 'space station', 'space debris', 'space mining', 'launch', 'rocket', 'cosmos', 'extraterrestr', 'interplanetary', 'Blue Origin', 'starship'] },
  { no: 8,  name: '気候変動と生存圏の縮小', map: '気候と生存',
    keywords: ['気候変動', '温暖化', '海面上昇', '異常気象', '気候難民', 'カーボン', '脱炭素', 'CO2', 'climate', 'warming', 'emission', 'carbon', 'extreme weather', 'flood', 'drought',
      '気候危機', '環境破壊', '生態系', '生物多様性', '森林破壊', '砂漠化', '熱波', '台風', 'ハリケーン', '山火事', '氷河', 'パリ協定', 'グリーン', 'net zero', 'biodiversity', 'deforestation', 'ecosystem', 'wildfire', 'hurricane', 'heatwave', 'glacier', 'sea level', 'methane', 'greenhouse', 'COP', 'adaptation', 'resilien'] },
  { no: 9,  name: '経済以外の新たな価値', map: '価値の多様化',
    keywords: ['ウェルビーイング', '幸福度', 'GDP以外', '社会関係資本', 'ソーシャルキャピタル', 'コモンズ', '共有経済', 'well-being', 'wellbeing', 'happiness index', 'commons', 'sharing economy', 'degrowth',
      '脱成長', 'QOL', '生活の質', 'マインドフルネス', 'ケア経済', '贈与経済', '互助', '連帯経済', '幸福', 'purpose', 'quality of life', 'social capital', 'care economy', 'gift economy', 'cooperative', 'mutual aid', 'solidarity', 'mindful', 'post-growth', 'doughnut economics'] },
  { no: 10, name: '社会的な活動の当たり前化', map: '市民社会',
    keywords: ['市民活動', 'ソーシャルビジネス', '社会起業', 'NGO', 'NPO', 'ボランティア', 'civic tech', 'social enterprise', 'philanthrop', 'social impact', 'CSR', 'ESG',
      'ソーシャルイノベーション', '社会貢献', 'インパクト投資', 'コミュニティ', '草の根', '市民参加', 'クラウドファンディング', '社会的企業', 'social innovation', 'impact invest', 'community', 'grassroot', 'civil society', 'crowdfund', 'activism', 'participat', 'nonprofit', 'SDGs', 'B Corp'] },
  { no: 11, name: '拡大する格差と新たな紛争', map: '格差と紛争',
    keywords: ['格差', '不平等', '貧困', '紛争', '難民', 'テロ', '分断', '移民', 'inequality', 'poverty', 'conflict', 'refugee', 'polariz', 'migration',
      '所得格差', 'デジタルデバイド', '経済格差', '戦争', '内戦', '制裁', '地政学', 'ジェノサイド', '人権侵害', '強制移住', 'war', 'civil war', 'sanction', 'geopolitic', 'displacement', 'digital divide', 'wealth gap', 'terrorism', 'extremism', 'radicali', 'asylum', 'humanitarian'] },
  { no: 12, name: '進展する身体的健康と長寿社会', map: '健康と長寿',
    keywords: ['長寿', 'アンチエイジング', '再生医療', 'ゲノム', '遺伝子治療', '健康寿命', 'バイオテクノロジー', 'longevity', 'aging', 'genome', 'gene therapy', 'regenerative', 'biotech', 'CRISPR',
      '幹細胞', 'mRNA', 'ワクチン', '免疫療法', '個別化医療', 'プレシジョンメディシン', '遺伝子編集', 'テロメア', '老化', '寿命', 'エピジェネティクス', 'stem cell', 'vaccine', 'immunotherapy', 'precision medicine', 'personalized', 'telomere', 'anti-aging', 'lifespan', 'healthspan', 'epigenetic', 'gene editing', 'biopharm'] },
  { no: 13, name: '人とロボットの接近', map: '人機共生',
    keywords: ['コミュニケーションロボット', '介護ロボット', 'ソーシャルロボット', 'ヒューマノイド', '人機', 'AI アシスタント', 'companion robot', 'humanoid', 'social robot', 'cobot', 'human-robot',
      'チャットボット', '対話AI', '感情認識', 'ペットロボット', '接客ロボット', '協働ロボット', 'ChatGPT', 'LLM', '大規模言語', '生成AI', 'conversational AI', 'chatbot', 'emotional AI', 'affective computing', 'collaborative robot', 'service robot', 'AI assistant', 'generative AI', 'language model'] },
  { no: 14, name: '高度な専門技術の一般化', map: '技術の民主化',
    keywords: ['民主化', 'ノーコード', 'ローコード', '3Dプリンタ', 'オープンソース', 'DIY', 'maker', '市民科学', 'democratiz', 'no-code', 'low-code', '3D print', 'open source', 'citizen science',
      'FabLab', 'ファブラボ', 'メイカー', 'Arduino', 'Raspberry Pi', 'バイオDIY', 'クリエイターエコノミー', 'フリーランス', 'GitHub', 'API', 'SaaS', 'creator economy', 'freelance', 'peer production', 'platform', 'accessible technolog'] },
  { no: 15, name: '多様性と共にある発展の実現', map: '包摂的発展',
    keywords: ['多様性', 'ダイバーシティ', 'インクルージョン', 'ジェンダー', 'LGBTQ', 'アクセシビリティ', '共生', 'diversity', 'inclusion', 'gender', 'equity', 'accessibility', 'multicultural',
      'フェミニズム', '同性婚', '障害者', 'ユニバーサルデザイン', '先住民', '民族', '人種', '差別', 'DEI', '公正', 'feminism', 'marriage equality', 'disability', 'universal design', 'indigenous', 'racial', 'ethnic', 'anti-discrimination', 'representat', 'intersectional'] },
  { no: 16, name: '脳の解明と再現', map: '脳科学',
    keywords: ['脳科学', '神経科学', 'ニューロ', '人工知能', 'AGI ', 'ブレイン', '認知科学', 'neuroscience', 'brain', 'neural network', 'consciousness', 'cognitive science',
      '深層学習', 'ディープラーニング', 'ニューラルネットワーク', '機械学習', 'シナプス', '脳波', '脳イメージング', 'deep learning', 'machine learning', 'artificial intelligence', 'transformer model', 'synapse', 'fMRI', 'brain-computer', 'neuromorphic', 'artificial general intelligence', 'superintelligen', 'large language model', 'GPT', 'neural net', 'generative AI', 'AI model', 'AI system'] },
  { no: 17, name: '閉じる国家と停滞する社会', map: '国家と停滞',
    keywords: ['保護主義', '孤立主義', '少子化', '人口減少', '高齢化', '停滞', 'ポピュリズム', '権威主義', 'protectionism', 'isolationism', 'demographic decline', 'aging society', 'populism', 'authoritarian',
      '出生率', '人口危機', 'ナショナリズム', '排外', '関税', 'デカップリング', '国境', '規制強化', 'birth rate', 'fertility', 'nationalism', 'xenophob', 'tariff', 'decoupling', 'border', 'stagnation', 'recession', 'autocra', 'illiberal', 'sovereignty', 'deglobaliz'] },
  { no: 18, name: '暮らしの基盤自体の多様化', map: '暮らしの変容',
    keywords: ['リモートワーク', '多拠点', 'ノマド', '教育改革', 'ベーシックインカム', 'ライフスタイル', 'ワーケーション', '暮らし方', 'remote work', 'nomad', 'basic income', 'lifestyle', 'co-living', 'edtech',
      'テレワーク', 'フレックス', '副業', 'ギグエコノミー', '地方移住', '関係人口', 'シェアハウス', '食の多様化', '代替肉', 'オンライン教育', 'MOOC', 'gig economy', 'hybrid work', 'coworking', 'digital nomad', 'alternative protein', 'plant-based', 'home school', 'lifelong learning', 'work-life', 'four-day work', 'universal basic',
      'housing', 'rent', 'mortgage', 'urban planning', 'suburba', 'commut', 'freelanc', 'side job', 'food delivery', 'sharing economy', 'subscription', 'work from home', 'flexible work', 'education reform', 'online learning', 'childcare', '保育', '住宅', '通勤', '働き方改革', 'ワークライフバランス', '在宅勤務', '非正規', 'フードデリバリー', 'サブスクリプション'] }
];

// ==============================================================
// THEME MATCHING (shared fuzzy matching)
// ==============================================================
// Short English keywords (<=3 chars) use word-boundary matching to avoid false positives
function _kwMatch(text, kw) {
  if (kw.length <= 3 && /^[a-z]+$/i.test(kw)) {
    return new RegExp('\\b' + kw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b', 'i').test(text);
  }
  return text.includes(kw);
}
function _themeMatchScore(text, titleText, kwLower) {
  var score = 0;
  var hits = [];
  kwLower.forEach(function(kw) {
    var inTitle = _kwMatch(titleText, kw);
    var inBody = !inTitle && _kwMatch(text, kw);
    if (inTitle) { score += 2; hits.push(kw); }
    else if (inBody) { score += 1; hits.push(kw); }
  });
  return { score: score, hits: hits };
}

// ==============================================================
// FUTURE THEME CONNECTOR (contextual connection text for modal)
// ==============================================================
function _futureConnectorText(catKey, theme, article) {
  var catContext = {
    political: '政策・制度面から',
    economic: '経済・市場の動向として',
    social: '社会・文化的な変化として',
    technological: '技術革新の観点から',
    legal: '法規制の変化を通じて',
    environmental: '環境・資源の観点から'
  };
  var catPhrase = catContext[catKey] || '';
  var matchCount = theme.hits.length;
  var strength = matchCount >= 3 ? '強く' : matchCount >= 2 ? '' : 'ゆるやかに';
  var desc = {
    1:  'イノベーションの分散や都市型経済圏の変化に関わる動きとして読むことで、断片的なニュースが未来の文脈の中に位置づけられます。',
    2:  '人間の身体能力をテクノロジーで拡張する流れの中に位置づけることができます。',
    3:  'テクノロジーが倫理的課題を生み出す構造として捉えると、未来社会のリスクが見えてきます。',
    4:  '資源の効率的な管理・制御に向けた変化として、持続可能な未来への道筋と接続します。',
    5:  'デジタル世界と現実の境界が曖昧になる流れの中で、新たな生活様式の萌芽として読めます。',
    6:  'ロボットや自動化による社会構造の変化として、労働と生活の未来像と接続します。',
    7:  '人類の活動領域が宇宙へ拡がる動きとして、文明のフロンティアの変化を示唆しています。',
    8:  '気候変動と人類の生存環境への影響として、適応と変革の未来を考えるきっかけになります。',
    9:  '経済的価値とは異なる新たな価値基準の模索として、ポスト資本主義の萌芽と接続します。',
    10: '社会的活動・市民参加が日常化する流れとして、市民社会の未来像に接続します。',
    11: '格差の拡大や新たな対立構造の出現として、社会の分断と統合の未来を考えるヒントです。',
    12: '健康・長寿に関する科学技術の進展として、人生100年時代の未来像と接続します。',
    13: '人間とロボットの関係が近づく変化として、共生社会の未来を示唆しています。',
    14: '高度な技術が一般の人々にも使えるようになる流れとして、創造の民主化の未来と接続します。',
    15: '多様性を前提とした社会の発展モデルとして、包摂的な未来社会への道筋を示しています。',
    16: '脳科学・人工知能による知性の解明と再現の流れとして、意識と知性の未来と接続します。',
    17: '国家の閉鎖性や社会の停滞に関わる動きとして、制度疲労と変革の未来を考えるきっかけです。',
    18: '住まい方・働き方・暮らしの前提が変わる流れとして、日常生活の未来像と接続します。'
  };
  return 'この記事は、' + catPhrase + '「' + theme.name + '」と' + strength + '接続しています。' + (desc[theme.no] || '');
}

// ==============================================================
// ARTICLE MODAL
// ==============================================================
window.openArticleModal = function(catKey, index) {
  var data = dataCache['latest.json'];
  var aiData = dataCache['ai_analysis.json'];
  if (!data) return;
  var article = data.pestle[catKey]?.articles?.[index];
  if (!article) return;
  var trans = aiData?.translations?.[catKey]?.find(function(t) { return t.index === index; });
  var titleJa = trans?.title_translated || '';
  var summaryJa = trans?.summary_translated || '';
  var articleId = 'pestle-' + catKey + '-' + index;
  var catLabel = PESTLE_CATS[catKey]?.labelJa || catKey;
  var catColor = PESTLE_CATS[catKey]?.color || 'var(--accent)';

  // Bookmark state
  var bmId = 'news-' + catKey + '-' + index;
  var isBm = bookmarks.some(function(b) { return b.id === bmId; });

  // Find related weak signals (matching PESTLE category)
  var weakSignals = aiData?.weak_signals || [];
  var relatedSignals = weakSignals.filter(function(ws) {
    return (ws.pestle_categories || []).some(function(c) { return c.toLowerCase() === catKey.toLowerCase(); });
  }).slice(0, 5);

  // Find other articles in same category for context
  var sameCategory = (data.pestle[catKey]?.articles || [])
    .filter(function(a, i) { return i !== index; })
    .slice(0, 3);
  var sameCatTrans = (aiData?.translations || {})[catKey] || [];

  var content = document.getElementById('articleModalContent');
  var html = '';

  // Category badge
  html += '<div style="margin-bottom:12px"><span style="display:inline-block;padding:3px 10px;border-radius:4px;font-size:0.78rem;font-weight:600;background:' + catColor + ';color:#fff">' + escapeHtml(catLabel) + '</span></div>';

  // Title
  html += '<div class="modal-title">' + escapeHtml(article.title) + '</div>';
  if (titleJa) html += '<div class="modal-trans">' + escapeHtml(titleJa) + '</div>';

  // Metadata
  html += '<div class="modal-meta">' + escapeHtml(article.source || '') + ' | ' + escapeHtml(article.published_date || '') +
    (article.relevance_score ? ' | 関連度: ' + Number(article.relevance_score).toFixed(1) : '') +
    (article.tier ? ' | Tier ' + article.tier : '') + '</div>';

  // Summary section
  html += '<div class="modal-summary" style="margin:20px 0">';
  if (summaryJa) html += '<p class="modal-summary-main" style="font-size:1rem;line-height:2.0;color:var(--text)">' + escapeHtml(summaryJa) + '</p>';
  if (article.summary) html += '<p style="font-size:0.88rem;line-height:1.7;color:var(--text-secondary)">' + escapeHtml(article.summary) + '</p>';
  html += '</div>';

  // Action buttons row
  html += '<div class="modal-actions">';
  if (article.url) {
    html += '<a class="btn-primary modal-action-btn modal-action-btn-primary" href="' + escapeAttr(safeUrl(article.url)) + '" target="_blank" rel="noopener noreferrer">元記事を読む <span aria-hidden="true">&nearr;</span><span class="visually-hidden">（外部サイトへ移動）</span></a>';
  }
  html += '<button class="btn-secondary modal-action-btn ' + (isBm ? 'bookmarked' : '') + '" id="modalBookmarkBtn" onclick="toggleBookmark(\'' + bmId + '\',\'' + escapeAttr(article.title || '') + '\',\'' + escapeAttr(safeUrl(article.url)) + '\',this)">' +
    '<span style="font-size:1.1em">&#9734;</span> ' + (isBm ? 'ブックマーク済み' : 'ブックマークに追加') + '</button>';
  html += '<button class="btn-secondary modal-action-btn" onclick="confirmAndGenerateReport(\'' + escapeAttr(catKey) + '\',' + index + ')"><span style="font-size:1.1em">&#9998;</span> レポートを生成</button>';
  html += '</div>';

  // Related signals section
  if (relatedSignals.length > 0) {
    html += '<div class="modal-section-card">';
    html += '<h4 class="modal-section-heading">関連シグナル</h4>';
    var modalStMap = { 'weak_signal': { l: 'Weak Signal', c: '#C4756A' }, 'emerging_trend': { l: 'Emerging', c: '#B8605A' }, 'wild_card': { l: 'Wild Card', c: '#A84A48' }, 'counter_trend': { l: 'Counter', c: '#8E3A3A' }, 'paradigm_shift': { l: 'Paradigm Shift', c: '#6E2C2C' } };
    relatedSignals.forEach(function(ws) {
      var impactColor = (ws.potential_impact || '').toLowerCase() === 'high' ? '#e74c3c' :
                        (ws.potential_impact || '').toLowerCase() === 'medium' ? '#f39c12' : '#95a5a6';
      var mst = modalStMap[ws.signal_type] || modalStMap['weak_signal'];
      html += '<div class="modal-signal-item">' +
        '<div class="modal-signal-header">' +
          '<span class="modal-signal-dot" style="background:' + impactColor + '"></span>' +
          '<span class="modal-signal-name">' + escapeHtml(ws.signal || '') + '</span>' +
          '<span class="modal-signal-badge" style="background:' + mst.c + '20;color:' + mst.c + '">' + mst.l + '</span>' +
          (ws.potential_impact ? '<span class="modal-signal-badge" style="background:' + impactColor + '20;color:' + impactColor + '">' + escapeHtml(ws.potential_impact) + '</span>' : '') +
          (ws.three_horizons ? '<span class="modal-signal-badge" style="background:#C4756A20;color:#C4756A">' + escapeHtml(ws.three_horizons) + '</span>' : '') +
        '</div>' +
        '<div class="modal-signal-desc">' + escapeHtml(ws.description || '') + '</div>' +
        (ws.composite_score ? '<div style="font-size:11px;color:#8E3A3A;margin-top:2px">Score: ' + ws.composite_score + '/10 | <span style="color:#8E3A3A">CLA: ' + (ws.cla_depth || 'N/A') + '</span> | <span style="color:#B8605A">Ansoff L' + (ws.ansoff_level || '?') + '</span></div>' : '') +
      '</div>';
    });
    html += '</div>';
  }

  // Future themes connection (using shared fuzzy matching)
  var articleTitleText = ((article.title || '') + ' ' + (titleJa || '')).toLowerCase();
  var articleText = (articleTitleText + ' ' + (article.summary || '') + ' ' + (summaryJa || '')).toLowerCase();
  var matchedThemes = FUTUROLOGY_THEMES.map(function(theme) {
    var kwLower = theme.keywords.map(function(k) { return k.toLowerCase(); });
    var result = _themeMatchScore(articleText, articleTitleText, kwLower);
    return result.score > 0 ? Object.assign({}, theme, { hits: result.hits, score: result.score }) : null;
  }).filter(Boolean).sort(function(a, b) { return b.score - a.score; });

  html += '<div class="modal-section-card">';
  html += '<h4 class="modal-section-heading">未来予測テーマとの接続</h4>';

  if (matchedThemes.length > 0) {
    var THEME_FOLD = 3;
    matchedThemes.forEach(function(theme, ti) {
      var connector = _futureConnectorText(catKey, theme, article);
      var hidden = (matchedThemes.length > THEME_FOLD && ti >= THEME_FOLD) ? ' style="display:none" data-theme-extra' : '';
      html += '<div class="modal-theme-item"' + hidden + '>' +
        '<div class="modal-theme-header">' +
          '<span class="modal-theme-no">' + theme.no + '</span>' +
          '<span class="modal-theme-name">' + escapeHtml(theme.name) + '</span>' +
          '<span class="modal-theme-map" title="未来社会マップ上のカテゴリ">' + escapeHtml(theme.map) + '</span>' +
        '</div>' +
        '<div class="modal-theme-desc">' + escapeHtml(connector) + '</div>' +
      '</div>';
    });
    if (matchedThemes.length > THEME_FOLD) {
      html += '<button class="modal-theme-toggle" onclick="this.style.display=\'none\';document.querySelectorAll(\'[data-theme-extra]\').forEach(function(el){el.style.display=\'\'})">他' + (matchedThemes.length - THEME_FOLD) + '件のテーマを表示</button>';
    }
  }

  // No matching theme — show as new theme candidate (blank spot on the future map)
  if (matchedThemes.length === 0) {
    var catContext2 = { political:'政策・制度', economic:'経済・市場', social:'社会・文化', technological:'技術・イノベーション', legal:'法・規制', environmental:'環境・資源' };
    var catLabel2 = catContext2[catKey] || catLabel;
    html += '<div class="modal-theme-blank">' +
      '<div class="modal-theme-header">' +
        '<span class="modal-theme-no" style="background:var(--text-muted)">?</span>' +
        '<span class="modal-theme-name" style="color:var(--accent)">新規テーマ候補（空白地帯）</span>' +
      '</div>' +
      '<div class="modal-theme-desc">' +
        'この記事は、既存の18の未来予測テーマのいずれにも直接的に該当しません。' +
        '「' + escapeHtml(catLabel2) + '」領域における新たな変化の兆しとして、既存のテーマでは捉えきれない未来の動きを示唆している可能性があります。' +
        '18テーマの「空白地帯」に位置するこうした記事は、次の未来予測テーマを生み出す種になり得ます。' +
        'どのような新しいテーマが必要か、この記事をきっかけに考えてみてください。' +
      '</div>' +
    '</div>';
  }

  html += '</div>';

  // Same category articles
  if (sameCategory.length > 0) {
    html += '<div class="modal-section-plain">';
    html += '<h4 class="modal-section-heading">同カテゴリの記事</h4>';
    sameCategory.forEach(function(a) {
      var aIdx = (data.pestle[catKey]?.articles || []).indexOf(a);
      var aTr = sameCatTrans.find(function(t) { return t.index === aIdx; });
      var aJa = aTr?.title_translated || '';
      html += '<div class="modal-related-article" tabindex="0" role="button" onclick="openArticleModal(\'' + escapeAttr(catKey) + '\',' + aIdx + ')" onkeydown="if(event.key===\'Enter\')openArticleModal(\'' + escapeAttr(catKey) + '\',' + aIdx + ')">' +
        '<div class="modal-related-meta">' + escapeHtml(a.source || '') + ' | ' + escapeHtml(a.published_date || '') + '</div>' +
        '<div class="modal-related-title">' + escapeHtml(a.title) + '</div>' +
        (aJa ? '<div class="modal-related-trans">' + escapeHtml(aJa) + '</div>' : '') +
      '</div>';
    });
    html += '</div>';
  }

  // Report result container
  html += '<div id="newsReportResult-' + catKey + '-' + index + '"></div>';

  // Comments
  html += '<div class="comment-section" style="margin-top:24px"><h4 class="comment-heading">コメント</h4>' +
    '<div class="comment-input-row"><label for="modalCommentInput" class="visually-hidden">コメントを入力</label><input type="text" class="comment-input" placeholder="この記事にコメント..." id="modalCommentInput" aria-label="コメントを入力">' +
    '<button class="btn-primary" onclick="submitArticleComment(\'' + escapeAttr(articleId) + '\')">投稿</button></div>' +
    '<div class="comment-list" id="modalCommentList">読み込み中...</div></div>';

  content.innerHTML = html;

  // Scroll to top when navigating between articles in modal
  var modalBoxEl = document.getElementById('modalBox');
  if (modalBoxEl) modalBoxEl.scrollTop = 0;

  // Push history state so browser back closes modal (replace if already in modal to avoid stacking)
  var alreadyInModal = document.getElementById('articleModal').classList.contains('visible');
  window._modalReturnFocus = document.activeElement;
  document.getElementById('articleModal').classList.add('visible');
  document.body.style.overflow = 'hidden';
  // Hide background content from assistive technology
  var mainEl = document.querySelector('main');
  if (mainEl) mainEl.setAttribute('aria-hidden', 'true');
  loadArticleComments(articleId);
  setTimeout(function() { var btn = document.querySelector('.modal-back-btn'); if (btn) btn.focus(); }, 100);
  if (alreadyInModal) {
    history.replaceState({ modal: true }, '', location.href);
  } else {
    history.pushState({ modal: true }, '', location.href);
  }
};

window.closeArticleModal = function(fromPopstate) {
  var modal = document.getElementById('articleModal');
  if (!modal.classList.contains('visible')) return;
  modal.classList.remove('visible');
  document.body.style.overflow = '';
  // Restore background content for assistive technology
  var mainEl = document.querySelector('main');
  if (mainEl) mainEl.removeAttribute('aria-hidden');
  var pf = document.getElementById('modalProgressFill'); if (pf) pf.style.width = '0%';
  var mb = document.getElementById('modalBox'); if (mb) mb.scrollTop = 0;
  if (window._modalReturnFocus) { window._modalReturnFocus.focus(); window._modalReturnFocus = null; }
  // Pop the modal history entry (unless we're already handling popstate)
  if (!fromPopstate) history.back();
};

// --- Sidebar signal popup (delegates to unified modal) ---
window.openSidebarSignal = function(idx) {
  var signals = window._sidebarSignals;
  if (!signals || !signals[idx]) return;
  // Temporarily set as allSignals for the modal function
  var prev = window._allSignals;
  window._allSignals = signals;
  if (typeof openSignalModal === 'function') openSignalModal(idx);
  window._allSignals = prev;
};

// --- Modal click/keyboard handlers ---
// These are set up once when the modal shell is injected
document.addEventListener('DOMContentLoaded', function() {
  var articleModal = document.getElementById('articleModal');
  if (articleModal) {
    articleModal.addEventListener('click', function(e) {
      if (e.target === this || !document.getElementById('modalBox').contains(e.target)) closeArticleModal();
    });
  }
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeArticleModal();
    var modal = document.getElementById('articleModal');
    if (!modal || !modal.classList.contains('visible') || e.key !== 'Tab') return;
    var focusable = modal.querySelectorAll('button, input, textarea, a[href], [tabindex]:not([tabindex="-1"])');
    if (focusable.length === 0) return;
    var first = focusable[0], last = focusable[focusable.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });
});

// ==============================================================
// FIRESTORE COMMENTS
// ==============================================================
window.submitArticleComment = async function(articleId) {
  var input = document.getElementById('modalCommentInput');
  var text = input.value.trim();
  if (!text) return;
  if (text.length > 1000) { alert('コメントは1000文字以内で入力してください。'); return; }
  var user = auth.currentUser;
  if (!user) { showToast('コメントするにはログインが必要です。', 'error'); return; }
  try {
    await db.collection('news_comments').add({ articleId: articleId, text: text, userId: user.uid, userName: user.displayName || user.email, createdAt: firebase.firestore.FieldValue.serverTimestamp() });
    input.value = '';
    loadArticleComments(articleId);
  } catch (err) { console.error('Comment failed:', err); showToast('コメントの投稿に失敗しました。', 'error'); }
};

async function loadArticleComments(articleId) {
  var container = document.getElementById('modalCommentList');
  if (!container) return;
  try {
    var snap = await db.collection('news_comments').where('articleId', '==', articleId).orderBy('createdAt', 'desc').limit(20).get();
    if (snap.empty) { container.innerHTML = '<div class="text-muted">まだコメントはありません。</div>'; return; }
    container.innerHTML = snap.docs.map(function(doc) {
      var d = doc.data();
      var time = d.createdAt ? new Date(d.createdAt.seconds * 1000).toLocaleString('ja-JP') : '';
      return '<div class="comment-item"><div class="comment-item-meta">' + escapeHtml(d.userName || '匿名') + ' &middot; ' + time + '</div>' +
        '<div class="comment-item-text">' + escapeHtml(d.text) + '</div></div>';
    }).join('');
  } catch (e) { container.innerHTML = '<div class="text-muted">コメントの読み込みに失敗しました。</div>'; }
}

// ==============================================================
// BOOKMARKS
// ==============================================================
window.toggleBookmark = function(id, title, url, btn) {
  var idx = bookmarks.findIndex(function(b) { return b.id === id; });
  if (idx >= 0) { bookmarks.splice(idx, 1); if (btn) btn.classList.remove('bookmarked'); }
  else { bookmarks.push({ id: id, title: title, url: url, addedAt: new Date().toISOString() }); if (btn) btn.classList.add('bookmarked'); }
  var added = idx < 0;
  if (btn && btn.id === 'modalBookmarkBtn') {
    btn.innerHTML = '<span style="font-size:1.1em">&#9734;</span> ' + (added ? 'ブックマーク済み' : 'ブックマークに追加');
  }
  showToast(added ? 'ブックマークに追加しました' : 'ブックマークを解除しました', 'info');
  localStorage.setItem('fin_bookmarks', JSON.stringify(bookmarks));
  updateBookmarkUI();
};

var bookmarkFilter = 'active';

function updateBookmarkUI() {
  var activeCount = bookmarks.filter(function(b) { return !b.archived; }).length;
  var countEl = document.getElementById('bookmarkCount');
  if (countEl) countEl.textContent = activeCount;
  var list = document.getElementById('bookmarksContent');
  if (!list) return;
  var filtered = bookmarkFilter === 'active' ? bookmarks.filter(function(b) { return !b.archived; }) : bookmarks.filter(function(b) { return b.archived; });

  var html = '<div class="bookmark-filters">' +
    '<button class="btn-' + (bookmarkFilter === 'active' ? 'primary' : 'secondary') + '" onclick="setBookmarkFilter(\'active\')">アクティブ (' + bookmarks.filter(function(b) { return !b.archived; }).length + ')</button>' +
    '<button class="btn-' + (bookmarkFilter === 'archived' ? 'primary' : 'secondary') + '" onclick="setBookmarkFilter(\'archived\')">アーカイブ (' + bookmarks.filter(function(b) { return b.archived; }).length + ')</button>' +
  '</div>';

  if (filtered.length === 0) {
    html += '<p class="text-muted">' + (bookmarkFilter === 'active' ? 'ブックマークはまだありません。記事のブックマークアイコンをクリックして保存できます。' : 'アーカイブされたブックマークはありません。') + '</p>';
  } else {
    filtered.forEach(function(b) {
      html += '<div class="bookmark-list-item"><div class="bookmark-info">' +
        (b.url ? '<a href="' + escapeHtml(safeUrl(b.url)) + '" target="_blank" class="bookmark-title">' + escapeHtml(b.title) + '</a>' : '<span class="bookmark-title">' + escapeHtml(b.title) + '</span>') +
        '<div class="bookmark-date">' + (b.addedAt ? new Date(b.addedAt).toLocaleDateString('ja-JP') : '') + '</div>' +
        '</div><div class="bookmark-actions">' +
        '<button class="bookmark-action-btn" onclick="toggleArchiveBookmark(\'' + escapeAttr(b.id) + '\')" title="' + (b.archived ? '復元' : 'アーカイブ') + '">' + (b.archived ? '&#8634;' : '&#9744;') + '</button>' +
        '<button class="bookmark-action-btn bookmark-action-btn-delete" onclick="deleteBookmark(\'' + escapeAttr(b.id) + '\')" title="削除">&times;</button>' +
        '</div></div>';
    });
  }
  list.innerHTML = html;
}

window.setBookmarkFilter = function(f) { bookmarkFilter = f; updateBookmarkUI(); };
window.toggleArchiveBookmark = function(id) { var bm = bookmarks.find(function(b) { return b.id === id; }); if (bm) bm.archived = !bm.archived; localStorage.setItem('fin_bookmarks', JSON.stringify(bookmarks)); updateBookmarkUI(); };
window.deleteBookmark = function(id) { bookmarks = bookmarks.filter(function(b) { return b.id !== id; }); localStorage.setItem('fin_bookmarks', JSON.stringify(bookmarks)); updateBookmarkUI(); };

// ==============================================================
// USER REPORT GENERATION
// ==============================================================
window.confirmAndGenerateReport = function(catKey, index) {
  var data = dataCache['latest.json'];
  var aiData = dataCache['ai_analysis.json'];
  if (!data?.pestle?.[catKey]?.articles?.[index]) { showToast('記事が見つかりません。', 'error'); return; }
  if (!auth.currentUser) { showToast('レポートを生成するにはログインが必要です。', 'error'); return; }
  var article = data.pestle[catKey].articles[index];
  var trans = aiData?.translations?.[catKey]?.find(function(t) { return t.index === index; });
  var titleJa = trans?.title_translated || '';
  var displayTitle = titleJa || article.title || '';
  var catLabel = PESTLE_CATS[catKey]?.labelJa || catKey;

  var modal = document.getElementById('articleModal');
  var content = document.getElementById('articleModalContent');
  content.innerHTML = '<div style="padding:20px 0">' +
    '<h3 class="fs-h2" style="font-weight:700;margin-bottom:16px">この記事のレポートを生成しますか？</h3>' +
    '<div class="card" style="margin-bottom:16px">' +
      '<div class="fs-caption" style="color:var(--text-muted);margin-bottom:4px">' + escapeHtml(catLabel) + ' / ' + escapeHtml(article.source || '') + ' / ' + escapeHtml(article.published_date || '') + '</div>' +
      '<div class="fs-body-lg" style="font-weight:600;line-height:1.5">' + escapeHtml(displayTitle) + '</div>' +
      (article.summary ? '<div class="fs-body-sm" style="color:var(--text-secondary);margin-top:8px;line-height:1.6">' + escapeHtml(article.summary.substring(0, 200)) + '...</div>' : '') +
    '</div>' +
    '<p class="fs-body-sm" style="color:var(--text-secondary);margin-bottom:20px;line-height:1.6">この記事をもとにCLA（因果階層分析）の視点から深層分析レポートを生成します。生成には30秒〜1分程度かかります。</p>' +
    '<div style="display:flex;gap:10px;justify-content:flex-end">' +
      '<button class="btn-secondary" onclick="openArticleModal(\'' + escapeAttr(catKey) + '\',' + index + ')">戻る</button>' +
      '<button class="btn-primary" onclick="closeArticleModal();generateNewsReport(\'' + escapeAttr(catKey) + '\',' + index + ')">レポートを生成する</button>' +
    '</div></div>';
  modal.classList.add('visible');
  document.body.style.overflow = 'hidden';
};

// Store for completed background reports
window._pendingReports = [];

window.generateNewsReport = function(catKey, index) {
  var data = dataCache['latest.json'];
  var aiData = dataCache['ai_analysis.json'];
  if (!data) { showToast('ニュースデータがありません。', 'error'); return; }
  var article = data.pestle?.[catKey]?.articles?.[index];
  if (!article) { showToast('記事が見つかりません。', 'error'); return; }
  var user = auth.currentUser;
  if (!user) { showToast('レポートを生成するにはログインが必要です。', 'error'); return; }

  showToast('レポートをバックグラウンドで生成中...', 'info');

  var trans = aiData?.translations?.[catKey]?.find(function(t) { return t.index === index; });
  var titleJa = trans?.title_translated || '';
  var summaryJa = trans?.summary_translated || '';
  var catCla = aiData?.cla?.[catKey] || {};
  var reportTitle = titleJa || article.title || '';

  // Collect related weak signals for prompt context
  var rptWeakSignals = aiData?.weak_signals || [];
  var rptRelatedSigs = rptWeakSignals.filter(function(ws) {
    return (ws.pestle_categories || []).some(function(c) { return c.toLowerCase() === catKey.toLowerCase(); });
  }).slice(0, 5);
  var rptSigCtx = '';
  if (rptRelatedSigs.length > 0) {
    rptSigCtx = '\n\n## 関連する弱いシグナル';
    rptRelatedSigs.forEach(function(ws, i) {
      rptSigCtx += '\n' + (i + 1) + '. ' + (ws.signal || '') + '（影響度: ' + (ws.potential_impact || 'N/A') + '）';
      if (ws.description) rptSigCtx += '\n   ' + ws.description;
      if (ws.time_horizon) rptSigCtx += '\n   時間軸: ' + ws.time_horizon;
    });
  }

  // Match against 18 futurology themes for prompt context (using shared fuzzy matching)
  var rptTitleText = ((article.title || '') + ' ' + (titleJa || '')).toLowerCase();
  var rptArtText = (rptTitleText + ' ' + (article.summary || '') + ' ' + (summaryJa || '')).toLowerCase();
  var rptThemeMatches = FUTUROLOGY_THEMES.map(function(theme) {
    var kwLower = theme.keywords.map(function(k) { return k.toLowerCase(); });
    var result = _themeMatchScore(rptArtText, rptTitleText, kwLower);
    return result.score > 0 ? { no: theme.no, name: theme.name, map: theme.map, score: result.score } : null;
  }).filter(Boolean).sort(function(a, b) { return b.score - a.score; });

  var rptThemeCtx = '\n\n## メガトレンド（未来予測18テーマ）との関連';
  if (rptThemeMatches.length > 0) {
    rptThemeMatches.forEach(function(t) {
      rptThemeCtx += '\n- テーマ' + t.no + '「' + t.name + '」（マップ: ' + t.map + '、マッチ度: ' + t.score + '）';
    });
  } else {
    rptThemeCtx += '\n- 既存18テーマに直接該当なし（空白地帯の可能性）。この記事がどのような新テーマを示唆するか分析してください。';
  }

  var question = '以下のニュース記事について、CLA（因果階層分析）・弱いシグナル・メガトレンド（未来予測18テーマ）の3つの視点から統合的な深層分析レポートを日本語で生成してください。\n\n' +
    '## 記事情報\nタイトル: ' + (article.title || '') +
    (titleJa ? '\n日本語タイトル: ' + titleJa : '') +
    '\n出典: ' + (article.source || '') + ' (' + (article.published_date || '') + ')' +
    '\n要約: ' + (article.summary || '') +
    (summaryJa ? '\n日本語要約: ' + summaryJa : '') +
    '\nPESTLEカテゴリ: ' + catKey +
    '\n\n## CLA分析コンテキスト（' + catKey + '分野）' +
    (catCla.myth_metaphor ? '\n神話・メタファー: ' + catCla.myth_metaphor : '') +
    (catCla.emerging_narrative ? '\n浮上するナラティブ: ' + catCla.emerging_narrative : '') +
    rptSigCtx +
    rptThemeCtx +
    '\n\n## レポート構成（3本柱で均等に扱うこと）\n' +
    '以下の構成で、各セクションを散文形式（地の文）で記述してください。箇条書きのみは不可。\n\n' +
    '### 1. エグゼクティブサマリー（500字程度）\n' +
    '記事の要点と、3つの分析視点（CLA・シグナル・メガトレンド）から見た意義を統合的に述べる。\n\n' +
    '### 2. メガトレンドとの接続\n' +
    '上記の未来予測18テーマとの関連を具体的に論じる。この記事がどのメガトレンドの文脈に位置づけられるか、なぜそのテーマと接続するのかを説明。18テーマに該当しない場合は「空白地帯」としてどのような新テーマの萌芽を示唆するか考察。複数テーマにまたがる場合はテーマ間の相互作用にも言及。\n\n' +
    '### 3. シグナル分析\n' +
    '関連する弱いシグナルとの関係を分析。この記事が示す変化の兆しは何か、シグナルの強度（強い/弱い）と時間軸（短期・中期・長期）を評価。複数のシグナルが収束している場合はその意味を解釈。\n\n' +
    '### 4. CLA深層分析\n' +
    '因果階層分析（リタニー→システム→世界観→神話）の4層で記事を読み解く。特に世界観と神話層の変化に注目。\n\n' +
    '### 5. 歴史的経緯と構造変化\n' +
    'この動きの歴史的背景を簡潔に整理し、現在の構造的転換点を論じる。\n\n' +
    '### 6. 今後のウォッチポイント（3つ）\n' +
    '経営者・コンサルタントが注視すべきポイント。具体的なアクション示唆を含む。\n\n' +
    '### 7. 関連する学術的知見（2つ）\n' +
    '読者は経営者・コンサルタント。知的かつ実用的な洞察を提供してください。';

  var WORKER_BASE = 'https://future-insight-proxy.nishimura-69a.workers.dev';

  // Run in background - doesn't block page navigation
  (async function() {
    try {
      var resp = await fetch(WORKER_BASE + '/api/foresight', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-User-Id': user.uid },
        body: JSON.stringify({
          question: question,
          claContext: window.__claContext || '',
          signalsContext: window.__signalsContext || '',
          newsContext: window.__newsContext || ''
        })
      });
      if (!resp.ok) { var err = await resp.json().catch(function() { return {}; }); throw new Error(err.error || 'HTTP ' + resp.status); }
      var respData = await resp.json();
      var generatedText = respData.answer || '';

      // Save to Firestore
      try {
        await db.collection('user_reports').add({
          userId: user.uid,
          userName: user.displayName || user.email || '',
          sourceReportTitle: reportTitle,
          sourceCategory: catKey,
          sourceUrl: article.url || '',
          generatedText: generatedText,
          createdAt: firebase.firestore.FieldValue.serverTimestamp()
        });
        if (typeof loadUserReportsSidebar === 'function') loadUserReportsSidebar();
      } catch (saveErr) {
        console.warn('User report save failed:', saveErr);
      }

      // Store completed report for viewing
      var catInfo = PESTLE_CATS[catKey] || { labelJa: catKey, color: 'var(--accent)' };
      window._pendingReports.push({
        title: reportTitle,
        catKey: catKey,
        catInfo: catInfo,
        article: article,
        generatedText: generatedText
      });

      // Show notification toast with "view" action
      showReportCompleteToast(reportTitle);
    } catch (err) {
      console.error('News report generation error:', err);
      showToast('レポートの生成に失敗しました: ' + (err.message || err), 'error');
    }
  })();
};

function showReportCompleteToast(title) {
  var container = document.getElementById('toastContainer');
  if (!container) return;
  var toast = document.createElement('div');
  toast.className = 'toast toast-success toast-report-complete';
  toast.innerHTML = '<div style="margin-bottom:6px"><strong>レポート生成完了</strong></div>' +
    '<div style="font-size:0.78rem;margin-bottom:8px">' + escapeHtml(title.substring(0, 60)) + '</div>' +
    '<button class="btn-primary" style="font-size:0.72rem;padding:6px 14px" onclick="viewLatestReport();this.parentElement.remove()">レポートを見る</button>';
  container.appendChild(toast);
  setTimeout(function() { if (toast.parentElement) { toast.classList.add('toast-out'); setTimeout(function() { toast.remove(); }, 300); } }, 10000);
}

window.viewLatestReport = function() {
  var report = window._pendingReports.pop();
  if (!report) { showToast('表示するレポートがありません。', 'info'); return; }
  var content = document.getElementById('articleModalContent');
  content.innerHTML = '<div style="border-top:4px solid ' + report.catInfo.color + ';padding-top:16px">' +
    '<span class="ir-hero-cat-badge" style="background:' + report.catInfo.color + '">' + escapeHtml(report.catInfo.labelJa) + '</span> ' +
    '<span class="fs-label" style="font-weight:600;padding:2px 10px;border-radius:12px;background:var(--accent-light);color:var(--accent)">読者レポート</span>' +
    '<h2 class="fs-h1" style="margin:12px 0 8px;line-height:1.4">' + escapeHtml(report.title) + '</h2>' +
    '<div class="fs-meta" style="color:var(--text-muted);margin-bottom:16px">' +
      escapeHtml(report.article.source || '') + ' / ' + escapeHtml(report.article.published_date || '') +
      (report.article.url ? ' &mdash; <a href="' + escapeAttr(safeUrl(report.article.url)) + '" target="_blank" style="color:var(--accent)">元記事</a>' : '') +
    '</div>' +
    '<div class="md-body">' + renderMarkdown(report.generatedText) + '</div></div>';
  document.getElementById('articleModal').classList.add('visible');
  document.body.style.overflow = 'hidden';
};

// ==============================================================
// USER REPORTS SIDEBAR (home page)
// ==============================================================
window.loadUserReportsSidebar = async function() {
  var el = document.getElementById('homeUserReports');
  if (!el) return;
  var user = auth.currentUser;
  if (!user) { el.innerHTML = '<p class="text-muted fs-body-sm">ログインするとレポートが表示されます</p>'; return; }
  try {
    var snap = await db.collection('user_reports')
      .where('userId', '==', user.uid)
      .get();
    // Sort client-side to avoid requiring a composite Firestore index
    var docs = [];
    snap.forEach(function(doc) { docs.push(doc); });
    docs.sort(function(a, b) {
      var aTs = (a.data().createdAt && a.data().createdAt.seconds) || 0;
      var bTs = (b.data().createdAt && b.data().createdAt.seconds) || 0;
      return bTs - aTs;
    });
    docs = docs.slice(0, 5);
    if (docs.length === 0) {
      el.innerHTML = '<p class="text-muted fs-body-sm">ニュース記事の &#9998; ボタンからレポートを生成できます</p>';
      return;
    }
    var html = '';
    docs.forEach(function(doc) {
      var d = doc.data();
      var ts = d.createdAt ? d.createdAt.toDate() : null;
      var dateStr = ts ? ts.toLocaleDateString('ja-JP', { month: 'short', day: 'numeric' }) : '';
      var catInfo = PESTLE_CATS[d.sourceCategory] || { labelJa: '', color: 'var(--accent)' };
      var preview = (d.generatedText || '').replace(/[#*`\n]/g, ' ').substring(0, 80);
      html += '<div class="card" style="padding:12px 14px;margin-bottom:8px;cursor:pointer" onclick="openUserReportModal(\'' + doc.id + '\')">' +
        '<div style="display:flex;align-items:center;gap:6px;margin-bottom:4px">' +
          '<span style="width:6px;height:6px;border-radius:50%;background:' + catInfo.color + ';flex-shrink:0"></span>' +
          '<span class="fs-meta" style="font-weight:600;color:var(--text);flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">' + escapeHtml(d.sourceReportTitle || '') + '</span>' +
          '<span class="fs-tiny" style="color:var(--text-muted);flex-shrink:0">' + dateStr + '</span>' +
        '</div>' +
        '<div class="fs-meta" style="color:var(--text-secondary);line-height:1.5">' + escapeHtml(preview) + '...</div>' +
      '</div>';
    });
    el.innerHTML = html;
  } catch (err) {
    console.warn('Sidebar user reports error:', err);
  }
};

window.openUserReportModal = async function(docId) {
  try {
    var doc = await db.collection('user_reports').doc(docId).get();
    if (!doc.exists) { showToast('レポートが見つかりません。', 'error'); return; }
    var d = doc.data();
    var catInfo = PESTLE_CATS[d.sourceCategory] || { labelJa: '', color: 'var(--accent)' };
    var content = document.getElementById('articleModalContent');
    content.innerHTML = '<div style="border-top:4px solid ' + catInfo.color + ';padding-top:16px">' +
      '<span class="ir-hero-cat-badge" style="background:' + catInfo.color + '">' + escapeHtml(catInfo.labelJa || '') + '</span> ' +
      '<span class="fs-label" style="font-weight:600;padding:2px 10px;border-radius:12px;background:var(--accent-light);color:var(--accent)">読者レポート</span>' +
      '<h2 class="fs-h1" style="margin:12px 0 8px;line-height:1.4">' + escapeHtml(d.sourceReportTitle || '') + '</h2>' +
      '<div class="fs-meta" style="color:var(--text-muted);margin-bottom:16px">' +
        escapeHtml(d.userName || '') + ' / ' +
        (d.createdAt ? d.createdAt.toDate().toLocaleDateString('ja-JP') : '') +
        (d.sourceUrl ? ' &mdash; <a href="' + escapeAttr(safeUrl(d.sourceUrl)) + '" target="_blank" style="color:var(--accent)">元記事</a>' : '') +
      '</div>' +
      '<div class="md-body">' + renderMarkdown(d.generatedText || '') + '</div></div>';
    document.getElementById('articleModal').classList.add('visible');
    document.body.style.overflow = 'hidden';
  } catch (err) {
    showToast('レポートの読み込みに失敗しました。', 'error');
  }
};
