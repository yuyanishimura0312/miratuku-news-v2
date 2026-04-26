'use strict';
// Initialize nav and auth
initNav('media');
initAuthGuard(function(user) {
  fetchJSON('media_sources.json').then(renderMediaSources);
});

// ==============================================================
// MEDIA TIER OVERRIDE HELPERS
// ==============================================================
function getMediaTierOverrides() {
  return JSON.parse(localStorage.getItem('media_tier_overrides') || '{}');
}

function setMediaTier(name, tier) {
  var overrides = getMediaTierOverrides();
  overrides[name] = tier;
  localStorage.setItem('media_tier_overrides', JSON.stringify(overrides));
}

function resetMediaTiers() {
  localStorage.removeItem('media_tier_overrides');
  if (window._lastMediaSourcesData) renderMediaSources(window._lastMediaSourcesData);
}

// Cycle tier: 1 -> 2 -> 3 -> 1
window.cycleMediaTier = function(mediaName, originalTier) {
  var overrides = getMediaTierOverrides();
  var currentTier = overrides[mediaName] || originalTier || 1;
  var nextTier = currentTier >= 3 ? 1 : currentTier + 1;
  setMediaTier(mediaName, nextTier);
  if (window._lastMediaSourcesData) renderMediaSources(window._lastMediaSourcesData);
};

window.resetMediaTiers = resetMediaTiers;

// ==============================================================
// RENDER: MEDIA SOURCES
// ==============================================================
function renderMediaSources(data) {
  var container = document.getElementById('mediaSourcesContent');
  if (!data) { container.innerHTML = '<p class="text-muted">メディアソースデータを取得できませんでした。</p>'; return; }

  // Store data for re-rendering after tier changes
  window._lastMediaSourcesData = data;
  var tierOverrides = getMediaTierOverrides();
  var hasOverrides = Object.keys(tierOverrides).length > 0;

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

  var isJapan = currentRegion === 'japan';
  var filtered = sources.filter(function(s) {
    var lang = (s.language || '').toLowerCase();
    return isJapan ? lang === 'ja' : lang === 'en';
  });

  document.getElementById('sourcesCount').textContent = filtered.length + 'メディア (' + (isJapan ? '日本語' : '英語') + ') / 全' + sources.length + 'メディア';

  if (filtered.length === 0) { container.innerHTML = '<p class="text-muted">該当するメディアソースがありません。</p>'; return; }

  var totalArticles = filtered.reduce(function(sum, s) { return sum + (s.articles_count || 0); }, 0);

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

  var resetBtn = hasOverrides ? '<button class="tier-reset-btn" onclick="resetMediaTiers()">Tierリセット</button>' : '';

  container.innerHTML = '<div class="media-meta">' + filtered.length + ' RSSフィードから <strong>' + totalArticles.toLocaleString() + '</strong> 件の記事を収集' + (data.total_articles_all ? '（DB全体: ' + data.total_articles_all.toLocaleString() + ' 件）' : '') + resetBtn + '</div>' +
    '<div class="media-table-wrap"><table class="media-table"><thead><tr>' +
    '<th>メディア名</th><th>分野</th><th>Tier</th><th>記事数</th><th>最終取得</th></tr></thead><tbody>' +
    filtered.sort(function(a, b) {
      var tierA = getEffectiveTier(a);
      var tierB = getEffectiveTier(b);
      var tA = tierA === '-' ? 99 : tierA;
      var tB = tierB === '-' ? 99 : tierB;
      if (tA !== tB) return tA - tB;
      return (b.articles_count || 0) - (a.articles_count || 0);
    }).map(function(s) {
      var name = s.name_ja || s.name || s.title || '';
      var rawCat = s.categories || s.category || s.type || '';
      var cat = catToJa(rawCat);
      var originalTier = s.tier || '-';
      var tier = getEffectiveTier(s);
      var isOverridden = tierOverrides[name] !== undefined;
      var tierClass = tier === 1 ? '' : (tier === 2 ? 'tier-badge-2' : 'tier-badge-3');
      var tierStyle = isOverridden ? ' style="box-shadow:0 0 0 2px var(--accent-warm)"' : '';
      return '<tr><td class="media-name">' + escapeHtml(name) + '</td>' +
        '<td>' + escapeHtml(cat) + '</td>' +
        '<td>' + (tier !== '-' ? '<span class="tier-badge ' + tierClass + '"' + tierStyle + ' onclick="cycleMediaTier(\'' + escapeAttr(name) + '\',' + (originalTier === '-' ? 1 : originalTier) + ')" title="クリックでTier変更">Tier ' + tier + '</span>' : '<span class="tier-badge tier-badge-3" onclick="cycleMediaTier(\'' + escapeAttr(name) + '\',1)" title="クリックでTier設定" style="cursor:pointer;opacity:0.5">設定</span>') + '</td>' +
        '<td class="media-count">' + (s.articles_count || 0) + '</td>' +
        '<td class="media-date">' + escapeHtml(s.last_fetched || '-') + '</td></tr>';
    }).join('') + '</tbody></table></div>';
}

// ==============================================================
// REGION TOGGLE LISTENER
// ==============================================================
document.addEventListener('regionChange', function() {
  if (window._lastMediaSourcesData) renderMediaSources(window._lastMediaSourcesData);
});
