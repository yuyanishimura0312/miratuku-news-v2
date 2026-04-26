'use strict';
initNav('themes');
initAuthGuard(function(user) {
  // Load latest.json and ai_analysis.json, then render themes
  Promise.all([
    fetchJSON('latest.json'),
    fetchJSON('ai_analysis.json')
  ]).then(function(results) {
    dataCache['latest.json'] = results[0];
    dataCache['ai_analysis.json'] = results[1];
    renderThemes();
  });

  // FUTUROLOGY_THEMES is defined in js/shared/article-modal.js as a global var
  var _themesRendered = false;

  // Shared fuzzy matching: checks title (weight 2) and summary (weight 1)
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

  function matchNewsToThemes(articles) {
    var results = FUTUROLOGY_THEMES.map(function(theme) {
      var matched = [];
      var kwLower = theme.keywords.map(function(k) { return k.toLowerCase(); });
      (articles || []).forEach(function(art) {
        var titleText = ((art.title || '') + ' ' + (art._titleJa || '')).toLowerCase();
        var text = (titleText + ' ' + (art.summary || '') + ' ' + (art._summaryJa || '')).toLowerCase();
        var result = _themeMatchScore(text, titleText, kwLower);
        if (result.score > 0) {
          matched.push(Object.assign({}, art, { _matchScore: result.score, _matchedKeywords: result.hits }));
        }
      });
      matched.sort(function(a, b) { return b._matchScore - a._matchScore; });
      return Object.assign({}, theme, { matched: matched });
    });
    return results;
  }

  function renderThemes() {
    if (_themesRendered) return;
    var container = document.getElementById('themesContent');
    if (!container) return;

    // Collect all articles across PESTLE categories, with translations
    var allArticles = [];
    var latestRaw = dataCache['latest.json'];
    var aiTranslations = (dataCache['ai_analysis.json'] && dataCache['ai_analysis.json'].translations) || {};
    if (!latestRaw) return;

    var pestle = latestRaw.pestle || latestRaw;
    if (pestle && typeof pestle === 'object') {
      Object.keys(pestle).forEach(function(catKey) {
        var cat = pestle[catKey];
        var catTrans = aiTranslations[catKey] || [];
        var rawArticles = cat.articles || [];
        rawArticles.forEach(function(art, idx) {
          if (art && art.title) {
            if (!art.pestle_category && !art.category) art.pestle_category = catKey;
            var tr = catTrans.find(function(t) { return t.index === idx; });
            if (tr) {
              art._titleJa = tr.title_translated || '';
              art._summaryJa = tr.summary_translated || '';
            }
            allArticles.push(art);
          }
        });
      });
    }

    var themed = matchNewsToThemes(allArticles);

    var html = '<div class="theme-grid" id="themeGrid">';
    themed.forEach(function(t, idx) {
      var count = t.matched.length;
      html += '<div class="theme-card" onclick="showThemeDetail(' + idx + ')">' +
        '<div class="theme-card-title">' + t.no + '. ' + escapeHtml(t.name) + '</div>' +
        '<div class="theme-card-meta">' + escapeHtml(t.map) + (count > 0 ? ' <span class="theme-match-count">' + count + '\u4ef6\u306e\u95a2\u9023\u30cb\u30e5\u30fc\u30b9</span>' : '') + '</div>' +
        '<div class="theme-card-keywords">' + t.keywords.slice(0, 6).map(function(k) { return '<span class="theme-keyword">' + escapeHtml(k) + '</span>'; }).join('') + '</div>' +
      '</div>';
    });
    html += '</div>';
    html += '<div id="themeDetail" style="display:none"></div>';
    container.innerHTML = html;
    _themesRendered = true;
    window._themedData = themed;
  }

  window.showThemeDetail = function(idx) {
    var themed = window._themedData;
    if (!themed || !themed[idx]) return;
    var t = themed[idx];
    var grid = document.getElementById('themeGrid');
    var detail = document.getElementById('themeDetail');
    if (grid) grid.style.display = 'none';
    if (!detail) return;

    var html = '<button class="theme-back-btn" onclick="hideThemeDetail()">&larr; \u30e1\u30ac\u30c8\u30ec\u30f3\u30c9\u4e00\u89a7\u306b\u623b\u308b</button>';
    html += '<div class="theme-detail-header">' +
      '<div class="theme-detail-title">' + t.no + '. ' + escapeHtml(t.name) + '</div>' +
      '<div class="theme-detail-desc">\u30de\u30c3\u30d7\u30c6\u30fc\u30de: ' + escapeHtml(t.map) + '</div>' +
    '</div>';

    if (t.matched.length > 0) {
      html += '<h3 class="guide-heading" style="margin-top:16px">\u95a2\u9023\u30cb\u30e5\u30fc\u30b9\uff08' + t.matched.length + '\u4ef6\uff09</h3>';
      html += '<div class="theme-matched-news">';
      t.matched.slice(0, 30).forEach(function(art) {
        var catKey = art.pestle_category || art.category || '';
        var catInfo = PESTLE_CATS[catKey] || {};
        var displayTitle = art._titleJa || art.title || '';
        var displaySummary = art._summaryJa || art.summary || '';
        var hasOriginal = art._titleJa && art.title && art._titleJa !== art.title;
        html += '<div class="news-item" style="padding:10px 0;border-bottom:1px solid var(--border-light)">' +
          '<div style="display:flex;gap:8px;align-items:center;margin-bottom:4px">' +
            (catInfo.labelJa ? '<span class="pestle-badge" style="background:' + catInfo.color + ';color:#fff;padding:1px 6px;font-size:0.7rem">' + catInfo.labelJa + '</span>' : '') +
            '<span style="font-size:0.76rem;color:var(--text-muted)">' + escapeHtml(art.source || '') + '</span>' +
            '<span class="theme-match-count">' + art._matchScore + '\u30ad\u30fc\u30ef\u30fc\u30c9\u4e00\u81f4</span>' +
          '</div>' +
          '<div style="font-size:0.88rem;font-weight:600;color:var(--text);margin-bottom:2px;cursor:pointer" onclick="openArticleInModal(this)" data-url="' + escapeHtml(art.url || '') + '" data-title="' + escapeHtml(art.title || '') + '">' + escapeHtml(displayTitle) + '</div>' +
          (hasOriginal ? '<div style="font-size:0.76rem;color:var(--text-muted);margin-bottom:4px">' + escapeHtml(art.title) + '</div>' : '') +
          '<div style="font-size:0.82rem;color:var(--text-secondary);line-height:1.6">' + escapeHtml(displaySummary.slice(0, 200)) + (displaySummary.length > 200 ? '...' : '') + '</div>' +
          '<div style="margin-top:4px;display:flex;flex-wrap:wrap;gap:3px">' + (art._matchedKeywords || []).map(function(k) { return '<span class="theme-keyword" style="background:color-mix(in srgb, var(--accent) 10%, transparent);border-color:var(--accent)">' + escapeHtml(k) + '</span>'; }).join('') + '</div>' +
        '</div>';
      });
      html += '</div>';
    } else {
      html += '<p style="color:var(--text-muted);font-size:0.84rem;margin-top:16px">\u4eca\u65e5\u306e\u30cb\u30e5\u30fc\u30b9\u306b\u3053\u306e\u30e1\u30ac\u30c8\u30ec\u30f3\u30c9\u306b\u95a2\u9023\u3059\u308b\u8a18\u4e8b\u306f\u898b\u3064\u304b\u308a\u307e\u305b\u3093\u3067\u3057\u305f\u3002</p>';
    }

    detail.innerHTML = html;
    detail.style.display = 'block';
    window.scrollTo(0, 0);
    history.pushState({ themeDetail: idx }, '', location.href);
  };

  window.hideThemeDetail = function(fromPopstate) {
    var grid = document.getElementById('themeGrid');
    var detail = document.getElementById('themeDetail');
    if (grid) grid.style.display = '';
    if (detail) detail.style.display = 'none';
    if (!fromPopstate) history.back();
  };

  // Handle browser back button for theme detail
  window.addEventListener('popstate', function(e) {
    if (e.state && e.state.themeDetail !== undefined) return;
    var themeDetail = document.getElementById('themeDetail');
    if (themeDetail && themeDetail.style.display !== 'none' && themeDetail.innerHTML) {
      hideThemeDetail(true);
    }
  });

  // openArticleInModal for theme detail — uses shared article modal
  window.openArticleInModal = function(el) {
    var url = el.getAttribute('data-url');
    var title = el.getAttribute('data-title');
    if (!url) return;
    // Use the shared article modal infrastructure
    var content = document.getElementById('articleModalContent');
    if (!content) return;
    content.innerHTML = '<div class="modal-reader-col">' +
      '<div class="modal-back-bar">' +
        '<button class="modal-back-btn" onclick="closeArticleModal()">&larr; \u623b\u308b</button>' +
        '<button class="modal-close" onclick="closeArticleModal()" aria-label="\u9589\u3058\u308b">&times;</button>' +
      '</div>' +
      '<h2 style="font-family:var(--font-serif);font-size:1.15rem;font-weight:700;line-height:1.5;margin-bottom:12px">' + escapeHtml(title || '') + '</h2>' +
      '<div style="margin-bottom:16px"><a href="' + escapeHtml(url) + '" target="_blank" style="color:var(--accent);font-size:0.84rem">\u5143\u8a18\u4e8b\u3092\u8aad\u3080 &rarr;</a></div>' +
      '<div class="loading-indicator"><div class="loading-spinner loading-spinner-sm"></div><span>\u8a18\u4e8b\u3092\u8aad\u307f\u8fbc\u307f\u4e2d...</span></div>' +
    '</div>';
    document.getElementById('articleModal').classList.add('visible');
    document.body.style.overflow = 'hidden';
    history.pushState({ modal: true }, '', location.href);
  };
});
