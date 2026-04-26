'use strict';
// Initialize nav and auth
initNav('signals');
initAuthGuard(function(user) {
  fetchJSON('ai_analysis.json').then(renderSignals);
});

// ==============================================================
// RENDER: SIGNALS
// ==============================================================
function renderSignals(aiData) {
  var container = document.getElementById('signalsContent');
  var weakSignals = aiData?.weak_signals || [];
  if (weakSignals.length === 0) { container.innerHTML = '<p class="text-muted">現在検出されているシグナルはありません。</p>'; return; }

  // Signal type labels and colors
  var signalTypeMap = {
    'weak_signal': { label: 'Weak Signal', color: '#C4756A' },
    'emerging_trend': { label: 'Emerging', color: '#B8605A' },
    'wild_card': { label: 'Wild Card', color: '#A84A48' },
    'counter_trend': { label: 'Counter', color: '#8E3A3A' },
    'paradigm_shift': { label: 'Paradigm Shift', color: '#6E2C2C' },
  };
  var horizonMap = { 'H1': 'H1 Decline', 'H2': 'H2 Transition', 'H3': 'H3 Emerging' };
  var claMap = { 'litany': 'Litany', 'systemic': 'Systemic', 'worldview': 'Worldview', 'myth': 'Myth' };
  var pestleList = ['Political','Economic','Social','Technological','Legal','Environmental'];
  var horizonList = ['H1','H2','H3'];

  window._allSignals = weakSignals;
  window._signalTypeMap = signalTypeMap;

  // ===== Dashboard aggregation =====
  var typeCount = {};
  Object.keys(signalTypeMap).forEach(function(k) { typeCount[k] = 0; });
  var impactCount = { high: 0, medium: 0, low: 0 };
  var matrix = {};
  pestleList.forEach(function(p) { matrix[p] = {}; horizonList.forEach(function(h) { matrix[p][h] = 0; }); });
  var histBuckets = [0,0,0,0,0,0,0,0,0,0];

  weakSignals.forEach(function(ws) {
    if (typeCount[ws.signal_type] !== undefined) typeCount[ws.signal_type]++;
    var imp = (ws.potential_impact || '').toLowerCase();
    if (imp === 'high') impactCount.high++;
    else if (imp === 'medium') impactCount.medium++;
    else impactCount.low++;
    var score = parseFloat(ws.composite_score) || 0;
    var bucket = Math.min(Math.floor(score), 9);
    histBuckets[bucket]++;
    (ws.pestle_categories || []).forEach(function(p) {
      if (matrix[p] && ws.three_horizons && matrix[p][ws.three_horizons] !== undefined) {
        matrix[p][ws.three_horizons]++;
      }
    });
  });

  var maxTypeCount = Math.max.apply(null, Object.values(typeCount).concat([1]));
  var maxHistBucket = Math.max.apply(null, histBuckets.concat([1]));
  var maxCell = 0;
  pestleList.forEach(function(p) { horizonList.forEach(function(h) { if (matrix[p][h] > maxCell) maxCell = matrix[p][h]; }); });

  // Type bars HTML
  var typeBarsHtml = Object.keys(signalTypeMap).map(function(key) {
    var info = signalTypeMap[key];
    var cnt = typeCount[key] || 0;
    var pct = Math.round(cnt / maxTypeCount * 100);
    return '<div class="sig-type-bar-row"><span class="sig-type-bar-label">' + info.label + '</span>' +
      '<div class="sig-type-bar-track"><div class="sig-type-bar-fill" style="width:' + pct + '%;background:' + info.color + '"></div></div>' +
      '<span class="sig-type-bar-count">' + cnt + '</span></div>';
  }).join('');

  // Histogram HTML
  var histHtml = histBuckets.map(function(cnt, i) {
    var h = Math.round(cnt / maxHistBucket * 52);
    var cls = i >= 7 ? 'sig-hist-bar--high' : i >= 5 ? 'sig-hist-bar--mid' : '';
    return '<div class="sig-hist-col"><div class="sig-hist-bar ' + cls + '" style="height:' + h + 'px" title="' + i + '-' + (i+1) + ': ' + cnt + '件"></div>' +
      '<div class="sig-hist-col-label">' + i + '</div></div>';
  }).join('');

  // Impact HTML
  var impactColors = { high: '#6E2C2C', medium: '#A84A48', low: '#C4756A' };
  var impactHtml = ['high','medium','low'].map(function(imp) {
    var cnt = impactCount[imp];
    var pct = Math.round(cnt / weakSignals.length * 100);
    return '<div class="sig-impact-row"><div class="sig-impact-dot" style="background:' + impactColors[imp] + '"></div>' +
      '<span class="sig-impact-label">' + imp.charAt(0).toUpperCase() + imp.slice(1) + '</span>' +
      '<span class="sig-impact-count">' + cnt + '</span>' +
      '<span class="sig-impact-pct">' + pct + '%</span></div>';
  }).join('');

  // Matrix HTML
  var cellClass = function(cnt) {
    if (cnt === 0) return 'sig-matrix-cell--0';
    if (cnt >= maxCell * 0.8) return 'sig-matrix-cell--hi';
    if (cnt >= maxCell * 0.5) return 'sig-matrix-cell--4';
    if (cnt >= maxCell * 0.3) return 'sig-matrix-cell--3';
    if (cnt >= maxCell * 0.1) return 'sig-matrix-cell--2';
    return 'sig-matrix-cell--1';
  };
  var matrixHtml = '<table class="sig-matrix"><thead><tr><th></th>' +
    horizonList.map(function(h) { return '<th>' + h + '</th>'; }).join('') +
    '</tr></thead><tbody>' +
    pestleList.map(function(p) {
      return '<tr><td>' + p.substring(0, 3).toUpperCase() + '</td>' +
        horizonList.map(function(h) {
          var cnt = matrix[p][h];
          return '<td class="' + cellClass(cnt) + '">' + (cnt || '\u2014') + '</td>';
        }).join('') + '</tr>';
    }).join('') + '</tbody></table>';

  // ===== Card renderer =====
  var renderCard = function(ws, i) {
    var impactClass = (ws.potential_impact || '').toLowerCase() === 'high' ? 'ws-badge-high' :
                      (ws.potential_impact || '').toLowerCase() === 'medium' ? 'ws-badge-medium' : 'ws-badge-low';
    var stInfo = signalTypeMap[ws.signal_type] || signalTypeMap['weak_signal'];
    var horizon = ws.three_horizons || '';
    var claDepth = ws.cla_depth || '';
    var ansoff = ws.ansoff_level || 0;
    var composite = ws.composite_score || 0;
    var isNoise = ws.noise_flag === true;
    var wsBookmarkId = 'signal-' + i;
    var wsIsBookmarked = bookmarks.some(function(b) { return b.id === wsBookmarkId; });
    var scoreColor = composite >= 7 ? '#6E2C2C' : composite >= 5 ? stInfo.color : '#999';

    return '<div class="ws-card' + (isNoise ? ' ws-card-noise' : '') + '" id="ws-card-' + i + '"' +
      ' onclick="openSignalModal(' + i + ')" style="border-left-color:' + stInfo.color + '"' +
      ' data-type="' + (ws.signal_type || '') + '"' +
      ' data-impact="' + (ws.potential_impact || '').toLowerCase() + '"' +
      ' data-horizon="' + (ws.three_horizons || '') + '"' +
      ' data-pestle="' + (ws.pestle_categories || []).join(',') + '"' +
      ' data-score="' + composite + '">' +
      '<div class="ws-card-header">' +
        '<div class="ws-card-score-circle" style="border-color:' + scoreColor + ';color:' + scoreColor + '">' + (composite ? Number(composite).toFixed(1) : '\u2014') + '</div>' +
        '<div class="ws-card-header-right">' +
          '<div class="ws-card-badges">' +
            '<span class="ws-badge" style="background:' + stInfo.color + '20;color:' + stInfo.color + ';border:1px solid ' + stInfo.color + '40">' + stInfo.label + '</span>' +
            '<span class="ws-badge ' + impactClass + '">' + escapeHtml(ws.potential_impact || 'N/A') + '</span>' +
            (horizon ? '<span class="ws-badge" style="background:#C4756A20;color:#C4756A;border:1px solid #C4756A40">' + (horizonMap[horizon] || horizon) + '</span>' : '') +
            '<button class="bookmark-btn ' + (wsIsBookmarked ? 'bookmarked' : '') + '" onclick="event.stopPropagation();toggleBookmark(\'' + wsBookmarkId + '\',\'' + escapeAttr(ws.description || '') + '\',\'\',this)" title="ブックマーク">&#9734;</button>' +
          '</div>' +
          '<div class="ws-card-title">' + escapeHtml(ws.signal || (ws.description ? ws.description.substring(0, 120) : '')) + '</div>' +
        '</div>' +
      '</div>' +
      '<div class="ws-card-desc">' + escapeHtml(ws.description || '') + '</div>' +
      (((ws.pestle_categories && ws.pestle_categories.length > 0) || claDepth || ansoff) ?
        '<div class="ws-card-meta">' +
          (ws.pestle_categories || []).map(function(c) { return '<span class="ws-card-meta-tag">' + escapeHtml(c) + '</span>'; }).join('') +
          (claDepth ? '<span class="ws-card-meta-tag" style="background:#8E3A3A14;color:#8E3A3A;border:1px solid #8E3A3A20">CLA: ' + (claMap[claDepth] || claDepth) + '</span>' : '') +
          (ansoff ? '<span class="ws-card-meta-tag" style="background:#B8605A14;color:#B8605A;border:1px solid #B8605A20">Ansoff L' + ansoff + '</span>' : '') +
        '</div>' : '') +
      '<div class="ws-card-footer">' +
        '<div class="ws-card-score-bar-wrap"><span>Score</span>' +
          '<div class="ws-card-score-bar"><div class="ws-card-score-bar-fill" style="width:' + (composite * 10) + '%;background:' + scoreColor + '"></div></div>' +
          '<span style="font-weight:600">' + (composite ? Number(composite).toFixed(1) : '\u2014') + '</span>' +
        '</div>' +
        '<span class="ws-card-detail-hint">詳細を見る &rarr;</span>' +
      '</div>' +
    '</div>';
  };

  var cardsHtml = weakSignals.map(function(ws, i) { return renderCard(ws, i); }).join('');

  // ===== Assemble full HTML =====
  container.innerHTML =
    '<p class="pestle-meta-line">PESTLEニュースと学術論文から、学術的シグナル理論（Ansoff, Hiltunen, Inayatullah, Sharpe）に基づき検出された変化の兆し。<strong>' + weakSignals.length + '件</strong>のシグナルを検出。</p>' +
    // Dashboard
    '<div class="sig-dashboard">' +
      '<div class="sig-dash-row">' +
        '<div class="sig-dash-block sig-dash-block--wide"><div class="sig-dash-label">Signal Type Distribution</div><div class="sig-type-bars">' + typeBarsHtml + '</div></div>' +
        '<div class="sig-dash-block sig-dash-block--medium"><div class="sig-dash-label">Score Distribution</div><div class="sig-histogram">' + histHtml + '</div></div>' +
        '<div class="sig-dash-block sig-dash-block--narrow"><div class="sig-dash-label">Impact Summary</div><div class="sig-impact-summary">' + impactHtml + '</div></div>' +
      '</div>' +
      '<div class="sig-dash-row" style="margin-bottom:0"><div class="sig-dash-block" style="flex:1"><div class="sig-dash-label">PESTLE x Three Horizons Matrix</div><div class="sig-matrix-wrap">' + matrixHtml + '</div></div></div>' +
    '</div>' +
    // Filter bar
    '<div class="sig-filterbar" id="sigFilterBar">' +
      '<div style="display:flex;gap:10px;align-items:center;width:100%;padding-bottom:10px;border-bottom:1px solid var(--border-light);margin-bottom:10px;flex-wrap:wrap">' +
        '<input type="search" id="sigSearchInput" placeholder="シグナルを検索..." style="flex:1;min-width:200px;max-width:360px;height:32px;padding:0 10px 0 30px;border:1px solid var(--border);background:var(--surface);color:var(--text);font-size:0.8rem;font-family:var(--font);background-image:url(\'data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2214%22 height=%2214%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%23999%22 stroke-width=%222%22%3E%3Ccircle cx=%2211%22 cy=%2211%22 r=%228%22/%3E%3Cpath d=%22m21 21-4.35-4.35%22/%3E%3C/svg%3E\');background-repeat:no-repeat;background-position:8px center" />' +
        '<select class="sig-sort-select" id="sigSortSelect"><option value="score_desc">Score (高い順)</option><option value="score_asc">Score (低い順)</option><option value="impact">Impact (High優先)</option><option value="horizon">Horizon (H3優先)</option></select>' +
        '<select class="sig-sort-select" id="sigGroupSelect"><option value="none">グループなし</option><option value="type">タイプ別</option><option value="pestle">PESTLE別</option><option value="horizon">Horizon別</option></select>' +
        '<div class="sig-filter-result" style="border-left:1px solid var(--border-light);padding-left:12px"><span id="sigFilterCount">' + weakSignals.length + '件</span>を表示</div>' +
      '</div>' +
      '<div class="sig-filter-group"><span class="sig-filter-label">Type</span><div class="sig-filter-chips" id="filterType">' +
        '<button class="sig-chip sig-chip--active" data-val="all">All</button>' +
        Object.keys(signalTypeMap).map(function(k) { return '<button class="sig-chip" data-val="' + k + '">' + signalTypeMap[k].label + '</button>'; }).join('') +
      '</div></div>' +
      '<div class="sig-filter-group"><span class="sig-filter-label">Impact</span><div class="sig-filter-chips" id="filterImpact">' +
        '<button class="sig-chip sig-chip--active" data-val="all">All</button>' +
        '<button class="sig-chip" data-val="high">High</button><button class="sig-chip" data-val="medium">Medium</button><button class="sig-chip" data-val="low">Low</button>' +
      '</div></div>' +
      '<div class="sig-filter-group"><span class="sig-filter-label">PESTLE</span><div class="sig-filter-chips" id="filterPestle">' +
        '<button class="sig-chip sig-chip--active" data-val="all">All</button>' +
        pestleList.map(function(p) { return '<button class="sig-chip" data-val="' + p + '">' + p.substring(0, 3) + '</button>'; }).join('') +
      '</div></div>' +
      '<div class="sig-filter-group"><span class="sig-filter-label">Horizon</span><div class="sig-filter-chips" id="filterHorizon">' +
        '<button class="sig-chip sig-chip--active" data-val="all">All</button>' +
        '<button class="sig-chip" data-val="H1">H1</button><button class="sig-chip" data-val="H2">H2</button><button class="sig-chip" data-val="H3">H3</button>' +
      '</div></div>' +
      '<div class="sig-filter-group" style="border-right:none"><span class="sig-filter-label">Score Min</span>' +
        '<input type="range" id="sigScoreRange" min="0" max="10" step="0.5" value="0" style="width:80px;accent-color:var(--accent)">' +
        '<span id="sigScoreVal" style="font-size:0.72rem;font-weight:700;color:var(--accent);min-width:20px">ALL</span>' +
      '</div>' +
    '</div>' +
    // Card grid
    '<div class="ws-grid" id="wsGrid">' + cardsHtml + '</div>';

  // ===== Filter / Sort / Group / Search logic =====
  var filterState = { type: 'all', impact: 'all', pestle: 'all', horizon: 'all', minScore: 0, query: '', group: 'none' };

  function getFilteredSorted() {
    var sortVal = (document.getElementById('sigSortSelect') || {}).value || 'score_desc';
    var q = filterState.query.toLowerCase();
    var impactOrderMap = { high: 0, medium: 1, low: 2 };
    var hOrderMap = { H3: 0, H2: 1, H1: 2 };

    var filtered = weakSignals.filter(function(ws, i) {
      if (filterState.type !== 'all' && ws.signal_type !== filterState.type) return false;
      if (filterState.impact !== 'all' && (ws.potential_impact || '').toLowerCase() !== filterState.impact) return false;
      if (filterState.pestle !== 'all' && (ws.pestle_categories || []).indexOf(filterState.pestle) < 0) return false;
      if (filterState.horizon !== 'all' && ws.three_horizons !== filterState.horizon) return false;
      if (filterState.minScore > 0 && (ws.composite_score || 0) < filterState.minScore) return false;
      if (q && ((ws.signal || '') + ' ' + (ws.description || '')).toLowerCase().indexOf(q) < 0) return false;
      return true;
    });

    filtered.sort(function(a, b) {
      if (sortVal === 'score_desc') return (b.composite_score || 0) - (a.composite_score || 0);
      if (sortVal === 'score_asc') return (a.composite_score || 0) - (b.composite_score || 0);
      if (sortVal === 'impact') return (impactOrderMap[(a.potential_impact||'').toLowerCase()] || 99) - (impactOrderMap[(b.potential_impact||'').toLowerCase()] || 99);
      if (sortVal === 'horizon') return (hOrderMap[a.three_horizons] || 99) - (hOrderMap[b.three_horizons] || 99);
      return 0;
    });

    return filtered;
  }

  function rebuildGrid() {
    var filtered = getFilteredSorted();
    var grid = document.getElementById('wsGrid');
    if (!grid) return;

    var groupVal = (document.getElementById('sigGroupSelect') || {}).value || 'none';

    if (filtered.length === 0) {
      grid.innerHTML = '<div style="text-align:center;padding:60px 20px;color:var(--text-muted);grid-column:1/-1">' +
        '<div style="font-size:0.95rem;font-weight:600;color:var(--text-secondary);margin-bottom:8px">条件に一致するシグナルがありません</div>' +
        '<div style="font-size:0.82rem">フィルタを変更するか、条件を緩めてください。</div></div>';
    } else if (groupVal === 'none') {
      grid.innerHTML = filtered.map(function(ws) { return renderCard(ws, weakSignals.indexOf(ws)); }).join('');
    } else {
      var groups = {};
      var groupLabels = {
        type: function(ws) { return ws.signal_type || 'unknown'; },
        pestle: function(ws) { return (ws.pestle_categories && ws.pestle_categories[0]) || 'Other'; },
        horizon: function(ws) { return ws.three_horizons || 'N/A'; }
      };
      var getKey = groupLabels[groupVal] || groupLabels.type;
      filtered.forEach(function(ws) {
        var k = getKey(ws);
        if (!groups[k]) groups[k] = [];
        groups[k].push(ws);
      });

      var groupOrder;
      if (groupVal === 'horizon') groupOrder = ['H3', 'H2', 'H1', 'N/A'];
      else if (groupVal === 'type') groupOrder = ['paradigm_shift', 'wild_card', 'emerging_trend', 'counter_trend', 'weak_signal'];
      else groupOrder = Object.keys(groups).sort();

      var html = '';
      groupOrder.forEach(function(k) {
        if (!groups[k] || groups[k].length === 0) return;
        var displayLabel = groupVal === 'type' ? (signalTypeMap[k] ? signalTypeMap[k].label : k) :
                          groupVal === 'horizon' ? (horizonMap[k] || k) : k;
        html += '<div style="grid-column:1/-1;display:flex;align-items:center;justify-content:space-between;padding:6px 0 10px;border-bottom:2px solid var(--border);margin-top:24px">' +
          '<span style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:var(--text-secondary)">' + escapeHtml(displayLabel) + '</span>' +
          '<span style="font-size:0.68rem;color:var(--text-muted);background:var(--surface);padding:2px 8px;border:1px solid var(--border-light)">' + groups[k].length + '件</span></div>';
        groups[k].forEach(function(ws) { html += renderCard(ws, weakSignals.indexOf(ws)); });
      });
      grid.innerHTML = html;
    }

    var countEl = document.getElementById('sigFilterCount');
    if (countEl) countEl.textContent = filtered.length + '件';
  }

  // Bind filter chips
  [
    { id: 'filterType', key: 'type' },
    { id: 'filterImpact', key: 'impact' },
    { id: 'filterPestle', key: 'pestle' },
    { id: 'filterHorizon', key: 'horizon' }
  ].forEach(function(cfg) {
    var group = document.getElementById(cfg.id);
    if (!group) return;
    group.querySelectorAll('.sig-chip').forEach(function(btn) {
      btn.addEventListener('click', function() {
        group.querySelectorAll('.sig-chip').forEach(function(b) { b.classList.remove('sig-chip--active'); });
        btn.classList.add('sig-chip--active');
        filterState[cfg.key] = btn.dataset.val;
        rebuildGrid();
      });
    });
  });

  // Sort
  var sortSelect = document.getElementById('sigSortSelect');
  if (sortSelect) sortSelect.addEventListener('change', rebuildGrid);

  // Group
  var groupSelect = document.getElementById('sigGroupSelect');
  if (groupSelect) groupSelect.addEventListener('change', function() { filterState.group = groupSelect.value; rebuildGrid(); });

  // Search (debounced)
  var searchInput = document.getElementById('sigSearchInput');
  var searchTimer;
  if (searchInput) searchInput.addEventListener('input', function() {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(function() { filterState.query = searchInput.value; rebuildGrid(); }, 200);
  });

  // Score range
  var scoreRange = document.getElementById('sigScoreRange');
  var scoreVal = document.getElementById('sigScoreVal');
  if (scoreRange) scoreRange.addEventListener('input', function() {
    filterState.minScore = parseFloat(scoreRange.value);
    if (scoreVal) scoreVal.textContent = filterState.minScore > 0 ? filterState.minScore : 'ALL';
    rebuildGrid();
  });

  rebuildGrid();
}

// ==============================================================
// SIGNAL DETAIL MODAL
// ==============================================================
window.toggleWSCard = function(index) {
  var card = document.getElementById('ws-card-' + index);
  if (card) card.classList.toggle('open');
};

window.openSignalModal = function(idx) {
  var signals = window._allSignals || window._sidebarSignals;
  if (!signals || !signals[idx]) return;
  var ws = signals[idx];

  var stMap = window._signalTypeMap || {
    'weak_signal': { label: 'Weak Signal', color: '#C4756A' },
    'emerging_trend': { label: 'Emerging Trend', color: '#B8605A' },
    'wild_card': { label: 'Wild Card', color: '#A84A48' },
    'counter_trend': { label: 'Counter Trend', color: '#8E3A3A' },
    'paradigm_shift': { label: 'Paradigm Shift', color: '#6E2C2C' }
  };
  var stInfo = stMap[ws.signal_type] || stMap['weak_signal'];
  var impactColors = { 'high': '#6E2C2C', 'medium': '#A84A48', 'low': '#C4756A' };
  var impactColor = impactColors[(ws.potential_impact || '').toLowerCase()] || '#6b7280';
  var composite = ws.composite_score || 0;
  var scoreColor = composite >= 7 ? '#6E2C2C' : composite >= 5 ? stInfo.color : '#999';
  var claMap2 = { 'litany': 'Litany (表層)', 'systemic': 'Systemic (構造)', 'worldview': 'Worldview (世界観)', 'myth': 'Myth/Metaphor (神話)' };
  var horizonMap2 = { 'H1': 'Horizon 1 \u2014 衰退する現体制', 'H2': 'Horizon 2 \u2014 移行期の革新', 'H3': 'Horizon 3 \u2014 新興の未来' };
  var pestleColors = { 'Political': '#8E3A3A', 'Economic': '#A84A48', 'Social': '#B8605A', 'Technological': '#9E5050', 'Legal': '#7A3535', 'Environmental': '#C4756A' };

  var content = document.getElementById('articleModalContent');
  var html = '<div class="modal-reader-col">';

  // Back bar
  html += '<div class="modal-back-bar">' +
    '<button class="modal-back-btn" onclick="closeArticleModal()">&larr; 戻る</button>' +
    '<button class="modal-close" onclick="closeArticleModal()" aria-label="閉じる">&times;</button>' +
  '</div>';

  // Header with score circle and badges
  html += '<div style="display:flex;gap:20px;align-items:flex-start;margin-bottom:20px">';
  html += '<div style="width:72px;height:72px;border-radius:50%;border:3px solid ' + scoreColor + ';display:flex;flex-direction:column;align-items:center;justify-content:center;flex-shrink:0">' +
    '<div style="font-size:1.3rem;font-weight:700;color:' + scoreColor + ';line-height:1">' + (composite ? Number(composite).toFixed(1) : '-') + '</div>' +
    '<div style="font-size:0.55rem;color:var(--text-muted);margin-top:1px">/10</div>' +
  '</div>';
  html += '<div style="flex:1;min-width:0">';
  html += '<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px">' +
    '<span style="display:inline-block;padding:4px 14px;border-radius:4px;font-size:0.78rem;font-weight:600;background:' + stInfo.color + ';color:#fff">' + escapeHtml(stInfo.label || '') + '</span>' +
    '<span style="display:inline-block;padding:4px 14px;border-radius:4px;font-size:0.78rem;font-weight:600;background:' + impactColor + '18;color:' + impactColor + ';border:1px solid ' + impactColor + '35">Impact: ' + escapeHtml(ws.potential_impact || 'N/A') + '</span>' +
    (ws.three_horizons ? '<span style="display:inline-block;padding:4px 14px;border-radius:4px;font-size:0.78rem;font-weight:600;background:#C4756A18;color:#C4756A;border:1px solid #C4756A35">' + escapeHtml(ws.three_horizons) + '</span>' : '') +
  '</div>';
  html += '<h2 style="font-family:var(--font-serif);font-size:1.25rem;font-weight:700;line-height:1.5;color:var(--text);margin:0">' + escapeHtml(ws.signal || '') + '</h2>';
  html += '</div></div>';

  // Meta grid
  var metaItems = [
    { label: 'Three Horizons', value: ws.three_horizons ? (horizonMap2[ws.three_horizons] || ws.three_horizons) : 'N/A', color: '#C4756A' },
    { label: 'CLA Depth', value: ws.cla_depth ? (claMap2[ws.cla_depth] || ws.cla_depth) : 'N/A', color: '#8E3A3A' },
    { label: 'Ansoff Level', value: ws.ansoff_level != null ? 'Level ' + ws.ansoff_level : 'N/A', color: '#B8605A' },
    { label: 'Time Horizon', value: ws.time_horizon || 'N/A', color: '#A84A48' }
  ];
  html += '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin-bottom:24px">';
  metaItems.forEach(function(m) {
    html += '<div style="background:var(--card);padding:14px 16px;border-top:2px solid ' + m.color + ';border-right:1px solid var(--border-light)">' +
      '<div style="font-size:0.62rem;text-transform:uppercase;letter-spacing:0.06em;color:' + m.color + ';margin-bottom:4px;font-weight:600">' + m.label + '</div>' +
      '<div style="font-size:0.85rem;font-weight:600;color:var(--text);line-height:1.4">' + escapeHtml(m.value) + '</div>' +
    '</div>';
  });
  html += '</div>';

  // Description
  html += '<div style="font-size:0.95rem;line-height:2.0;color:var(--text);margin-bottom:24px;padding:0 2px">' + escapeHtml(ws.description || '') + '</div>';

  // PESTLE categories
  if (ws.pestle_categories && ws.pestle_categories.length > 0) {
    html += '<div style="margin-bottom:24px">' +
      '<div class="ws-label" style="margin-bottom:8px">PESTLE Categories</div>' +
      '<div style="display:flex;gap:8px;flex-wrap:wrap">';
    ws.pestle_categories.forEach(function(cat) {
      var pc = pestleColors[cat] || '#6b7280';
      html += '<span style="display:inline-flex;align-items:center;gap:5px;padding:6px 14px;border-radius:4px;font-size:0.78rem;font-weight:500;background:' + pc + '12;color:' + pc + ';border:1px solid ' + pc + '25">' +
        '<span style="width:8px;height:8px;border-radius:50%;background:' + pc + '"></span>' + escapeHtml(cat) + '</span>';
    });
    html += '</div></div>';
  }

  // Scores visualization
  if (ws.scores) {
    var scoreLabels = {
      novelty: { ja: '新規性', en: 'Novelty' },
      disruption: { ja: '破壊性', en: 'Disruption' },
      cross_domain: { ja: '分野横断性', en: 'Cross-domain' },
      evidence_diversity: { ja: 'エビデンスの多様性', en: 'Evidence Diversity' },
      acceleration: { ja: '加速度', en: 'Acceleration' },
      counter_narrative: { ja: '対抗的ナラティブ', en: 'Counter Narrative' },
      global_local: { ja: 'グローバル/ローカル', en: 'Global-Local' },
      connectivity: { ja: '接続性', en: 'Connectivity' },
      credibility: { ja: '信頼性', en: 'Credibility' },
      early_stage: { ja: '初期段階性', en: 'Early Stage' }
    };
    html += '<div style="margin-bottom:24px">' +
      '<div class="ws-label" style="margin-bottom:10px">Signal Quality Scores</div>' +
      '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px 24px">';
    Object.keys(ws.scores).forEach(function(key) {
      var val = ws.scores[key];
      var info = scoreLabels[key] || { ja: key, en: key };
      var barColor = val >= 7 ? '#6E2C2C' : val >= 5 ? stInfo.color : '#bbb';
      html += '<div>' +
        '<div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:4px">' +
          '<span style="font-size:0.78rem;color:var(--text-secondary)">' + escapeHtml(info.ja) + '</span>' +
          '<span style="font-size:0.78rem;font-weight:700;color:' + barColor + '">' + Number(val).toFixed(1) + '</span>' +
        '</div>' +
        '<div style="height:6px;background:var(--border-light);border-radius:3px;overflow:hidden">' +
          '<div style="height:100%;width:' + (val * 10) + '%;background:' + barColor + ';border-radius:3px;transition:width 0.3s"></div>' +
        '</div>' +
      '</div>';
    });
    html += '</div></div>';
  }

  // Counter trend
  if (ws.counter_trend) {
    html += '<div style="margin-bottom:24px;padding:16px 20px;background:var(--surface);border-left:3px solid #8E3A3A;border-radius:0 4px 4px 0">' +
      '<div class="ws-label" style="margin-top:0;margin-bottom:8px">Counter Trend</div>' +
      '<p style="font-size:0.9rem;line-height:1.8;color:var(--text-secondary);margin:0">' + escapeHtml(ws.counter_trend) + '</p>' +
    '</div>';
  }

  // Related headlines
  if (ws.related_headlines && ws.related_headlines.length > 0) {
    html += '<div style="margin-bottom:24px">' +
      '<div class="ws-label" style="margin-bottom:8px">Related Headlines (' + ws.related_headlines.length + ')</div>';
    ws.related_headlines.forEach(function(h) {
      var headline = typeof h === 'string' ? h : (h.title || h.headline || JSON.stringify(h));
      html += '<div style="padding:10px 14px;border-bottom:1px solid var(--border-light);font-size:0.84rem;line-height:1.6;color:var(--text-secondary)">' + escapeHtml(headline) + '</div>';
    });
    html += '</div>';
  }

  // Evidence type
  if (ws.evidence_type) {
    html += '<div style="font-size:0.75rem;color:var(--text-muted);padding-top:8px;border-top:1px solid var(--border-light)">Evidence Type: ' + escapeHtml(ws.evidence_type) + '</div>';
  }

  html += '</div>'; // end modal-reader-col
  content.innerHTML = html;

  // Open modal
  var modalBoxEl = document.getElementById('modalBox');
  if (modalBoxEl) modalBoxEl.scrollTop = 0;
  var alreadyInModal = document.getElementById('articleModal').classList.contains('visible');
  window._modalReturnFocus = document.activeElement;
  document.getElementById('articleModal').classList.add('visible');
  document.body.style.overflow = 'hidden';
  var mainEl = document.querySelector('main');
  if (mainEl) mainEl.setAttribute('aria-hidden', 'true');
  setTimeout(function() { var btn = document.querySelector('.modal-back-btn'); if (btn) btn.focus(); }, 100);
  if (alreadyInModal) {
    history.replaceState({ modal: true }, '', location.href);
  } else {
    history.pushState({ modal: true }, '', location.href);
  }
};
