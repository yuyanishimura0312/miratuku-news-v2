'use strict';
// Initialize nav and auth
initNav('guide');
initAuthGuard(function(user) {
  fetchJSON('media_sources.json').then(renderGuideMedia);
});

// ==============================================================
// RENDER: GUIDE MEDIA LIST + STATS
// ==============================================================
function renderGuideMedia(data) {
  var guideContainer = document.getElementById('guideMediaContent');
  if (!data || !guideContainer) return;

  var tierOverrides = JSON.parse(localStorage.getItem('media_tier_overrides') || '{}');

  var sources = Array.isArray(data) ? data : (data.sources || data.feeds || []);
  if (!Array.isArray(sources) && typeof data === 'object') {
    sources = [];
    for (var key in data) {
      if (data.hasOwnProperty(key) && Array.isArray(data[key])) {
        data[key].forEach(function(s) {
          sources.push(typeof s === 'string' ? { name: s, category: key } : Object.assign({}, s, { category: s.categories || s.category || key }));
        });
      }
    }
  }

  function catToJa(rawCat) {
    var cats = Array.isArray(rawCat) ? rawCat : [rawCat];
    return cats.map(function(c) {
      var info = PESTLE_CATS[c];
      return info ? info.labelJa : c;
    }).join(', ');
  }

  function getEffectiveTier(source) {
    var name = source.name_ja || source.name || source.title || '';
    var originalTier = source.tier || '-';
    if (tierOverrides[name] !== undefined) return tierOverrides[name];
    return originalTier;
  }

  var allArticles = sources.reduce(function(sum, s) { return sum + (s.articles_count || 0); }, 0);
  var totalAll = data.total_articles_all || 0;
  var jaCount = sources.filter(function(s) { return (s.language || '').toLowerCase() === 'ja'; }).length;
  var enCount = sources.filter(function(s) { return (s.language || '').toLowerCase() === 'en'; }).length;

  var allSorted = sources.slice().sort(function(a, b) {
    var tA = (getEffectiveTier(a) === '-' ? 99 : getEffectiveTier(a));
    var tB = (getEffectiveTier(b) === '-' ? 99 : getEffectiveTier(b));
    if (tA !== tB) return tA - tB;
    return (b.articles_count || 0) - (a.articles_count || 0);
  });

  var dbNote = totalAll ? '<div class="media-meta" style="margin-top:4px;font-size:0.9em;opacity:0.8">データベース全体: <strong>' + totalAll.toLocaleString() + '</strong> 件（GDELT・歴史データ含む ' + (data.distinct_sources_all || 0).toLocaleString() + ' ソース）</div>' : '';

  guideContainer.innerHTML = '<div class="media-meta">' + sources.length + ' RSSフィードから <strong>' + allArticles.toLocaleString() + '</strong> 件の記事を収集（国内' + jaCount + ' + 海外' + enCount + '）</div>' + dbNote +
    '<div class="media-table-wrap"><table class="media-table"><thead><tr>' +
    '<th>メディア名</th><th>分野</th><th>Tier</th><th>言語</th><th>記事数</th><th>最終取得</th></tr></thead><tbody>' +
    allSorted.map(function(s) {
      var name = s.name_ja || s.name || s.title || '';
      var cat = catToJa(s.categories || s.category || s.type || '');
      var tier = getEffectiveTier(s);
      var tierClass = tier === 1 ? '' : (tier === 2 ? 'tier-badge-2' : 'tier-badge-3');
      var lang = (s.language || '').toLowerCase() === 'ja' ? '日本語' : '英語';
      return '<tr><td class="media-name">' + escapeHtml(name) + '</td>' +
        '<td>' + escapeHtml(cat) + '</td>' +
        '<td>' + (tier !== '-' ? '<span class="tier-badge ' + tierClass + '">Tier ' + tier + '</span>' : '-') + '</td>' +
        '<td>' + lang + '</td>' +
        '<td class="media-count">' + (s.articles_count || 0) + '</td>' +
        '<td class="media-date">' + escapeHtml(s.last_fetched || '-') + '</td></tr>';
    }).join('') + '</tbody></table></div>';

  // Update hardcoded guide stats with live data
  var overviewEl = document.getElementById('guideOverviewStats');
  if (overviewEl && totalAll) {
    overviewEl.textContent = sources.length + 'のRSSフィード（国内' + jaCount + '、海外' + enCount + '）と学術API、さらに1900年から現在まで126年分・' + totalAll.toLocaleString() + '件超の歴史データベース';
  }
  var streamEl = document.getElementById('guideStreamStats');
  if (streamEl) {
    streamEl.textContent = sources.length + 'のRSSフィード（国内' + jaCount + '、海外' + enCount + '）';
  }
  var introEl = document.getElementById('guideMediaIntro');
  if (introEl) {
    introEl.textContent = '以下の' + sources.length + 'メディアからニュースを自動収集しています。各メディアの信頼性に基づきTier分類されています。';
  }
}
