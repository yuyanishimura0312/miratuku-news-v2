'use strict';
var _dbRegistryLoaded = false;

initNav('databases');
(function() {
  loadDatabaseRegistry();

  function loadDatabaseRegistry() {
    if (_dbRegistryLoaded) return;
    fetch('data/db-registry.json')
      .then(function(res) { return res.json(); })
      .then(function(data) {
        renderDatabaseRegistry(data);
        _dbRegistryLoaded = true;
      })
      .catch(function(err) {
        console.error('DB registry load error:', err);
        document.getElementById('dbLayersContent').innerHTML =
          '<p style="color:var(--text-muted)">\u30c7\u30fc\u30bf\u30d9\u30fc\u30b9\u60c5\u5831\u306e\u8aad\u307f\u8fbc\u307f\u306b\u5931\u6557\u3057\u307e\u3057\u305f\u3002</p>';
      });
  }

  function renderDatabaseRegistry(data) {
    var overview = document.getElementById('dbOverview');
    var stats = data.totalStats;
    overview.innerHTML =
      '<div class="db-overview-card"><div class="db-overview-value">' + escapeHtml(String(stats.totalDatabases)) + '</div><div class="db-overview-label">\u30c7\u30fc\u30bf\u30d9\u30fc\u30b9</div></div>' +
      '<div class="db-overview-card"><div class="db-overview-value">' + escapeHtml(String(stats.totalRecords)) + '</div><div class="db-overview-label">\u7dcf\u30ec\u30b3\u30fc\u30c9\u6570</div></div>' +
      '<div class="db-overview-card"><div class="db-overview-value">' + escapeHtml(String(stats.layers)) + '</div><div class="db-overview-label">\u30a2\u30fc\u30ad\u30c6\u30af\u30c1\u30e3\u5c64</div></div>' +
      '<div class="db-overview-card"><div class="db-overview-value">' + escapeHtml(String(stats.updateFrequency)) + '</div><div class="db-overview-label">\u66f4\u65b0\u983b\u5ea6</div></div>';

    // Architecture diagram + number-bearing subtitles
    renderArchitecture(data);

    // \u81ea\u52d5\u66f4\u65b0\u30d1\u30a4\u30d7\u30e9\u30a4\u30f3\u72b6\u614b\u30c0\u30c3\u30b7\u30e5\u30dc\u30fc\u30c9
    renderPipelineStatus(data);

    var container = document.getElementById('dbLayersContent');
    var html = '';
    var layerEyebrows = { core: 'CORE', structural: 'STRUCTURAL', detection: 'DETECTION', conceptual: 'CONCEPTUAL' };
    data.layers.forEach(function(layer) {
      var eyebrow = layerEyebrows[layer.id] || layer.id.toUpperCase();
      var count = layer.databases.length;
      html += '<div class="db-layer" data-layer-id="' + escapeHtml(layer.id) + '">' +
        '<div class="db-layer-header">' +
          '<div class="db-layer-header-main">' +
            '<div class="db-layer-eyebrow">' + escapeHtml(eyebrow) + '</div>' +
            '<div class="db-layer-title">' + escapeHtml(layer.name) + '</div>' +
            '<div class="db-layer-desc">' + escapeHtml(layer.description) + '</div>' +
          '</div>' +
          '<div>' +
            '<div class="db-layer-count">' + count + '</div>' +
            '<div class="db-layer-count-label">DATABASES</div>' +
          '</div>' +
        '</div>' +
        '<div class="db-layer-grid">';
      layer.databases.forEach(function(dbItem) { html += renderDbEntry(dbItem); });
      html += '</div></div>';
    });

    // \u4e8b\u696d\u5316\u30bb\u30af\u30b7\u30e7\u30f3
    if (data.extraSections && data.extraSections.length > 0) {
      data.extraSections.forEach(function(section) {
        var secCount = section.databases.length;
        html += '<div class="db-extra-section">' +
          '<div class="db-extra-header">' +
            '<div class="db-layer-header" style="background:transparent;border:none;padding:0;margin:0">' +
              '<div class="db-layer-header-main">' +
                '<div class="db-extra-eyebrow">' + escapeHtml(section.id.toUpperCase()) + '</div>' +
                '<div class="db-extra-title">' + escapeHtml(section.name) + '</div>' +
                (section.description ? '<div class="db-extra-desc">' + escapeHtml(section.description) + '</div>' : '') +
              '</div>' +
              '<div>' +
                '<div class="db-layer-count">' + secCount + '</div>' +
                '<div class="db-layer-count-label">DATABASES</div>' +
              '</div>' +
            '</div>' +
          '</div>' +
          '<div class="db-layer-grid">';
        section.databases.forEach(function(dbItem) {
          html += renderDbEntry(dbItem);
        });
        html += '</div></div>';
      });
    }

    // \u88dc\u52a9\u30c7\u30fc\u30bf\u30d9\u30fc\u30b9
    if (data.supplementary && data.supplementary.length > 0) {
      html += '<div class="db-supplementary">' +
        '<div class="db-supplementary-eyebrow">SUPPLEMENTARY</div>' +
        '<div class="db-supplementary-title">\u88dc\u52a9\u30c7\u30fc\u30bf\u30d9\u30fc\u30b9 (' + data.supplementary.length + ')</div>' +
        '<div class="db-supplementary-desc">4\u5c64\u30a2\u30fc\u30ad\u30c6\u30af\u30c1\u30e3\u3068\u4e8b\u696d\u5316\u30bb\u30af\u30b7\u30e7\u30f3\u3092\u88dc\u8db3\u3059\u308b\u9818\u57df\u7279\u5316\u30c7\u30fc\u30bf\u30d9\u30fc\u30b9\u7fa4\u3002</div>';
      html += '<div class="db-supplementary-grid">';
      data.supplementary.forEach(function(dbItem) {
        var supLinks = [];
        if (dbItem.dashboard) supLinks.push('<a href="' + safeUrl(dbItem.dashboard) + '" class="db-dashboard-link">\u30c0\u30c3\u30b7\u30e5\u30dc\u30fc\u30c9 &rarr;</a>');
        if (dbItem.report) supLinks.push('<a href="' + safeUrl(dbItem.report) + '" class="db-dashboard-link">\u30ec\u30dd\u30fc\u30c8 &rarr;</a>');
        if (dbItem.textbook) supLinks.push('<a href="' + safeUrl(dbItem.textbook) + '" class="db-dashboard-link">\u6559\u79d1\u66f8 &rarr;</a>');
        if (dbItem.network) supLinks.push('<a href="' + safeUrl(dbItem.network) + '" class="db-dashboard-link">\u30cd\u30c3\u30c8\u30ef\u30fc\u30af &rarr;</a>');
        if (dbItem.essay) supLinks.push('<a href="' + safeUrl(dbItem.essay) + '" class="db-dashboard-link">\u8ad6\u8003 &rarr;</a>');
        if (dbItem.essay2) supLinks.push('<a href="' + safeUrl(dbItem.essay2) + '" class="db-dashboard-link">\u7d9a\u8ad6 &rarr;</a>');
        if (dbItem.gta) supLinks.push('<a href="' + safeUrl(dbItem.gta) + '" class="db-dashboard-link">GTA\u5206\u6790 &rarr;</a>');
        if (dbItem.paper) supLinks.push('<a href="' + safeUrl(dbItem.paper) + '" class="db-dashboard-link">\u8ad6\u6587 &rarr;</a>');
        var supAgentBadge = dbItem.agent ? ' <span class="db-entry-agent" title="Claude Code\u3067' + escapeHtml(dbItem.agent) + '\u3067\u8d77\u52d5">' + escapeHtml(dbItem.agent) + '</span>' : '';
        html += '<div class="db-supplementary-item"><strong>' + escapeHtml(dbItem.id) + ': ' + escapeHtml(dbItem.nameJa || dbItem.name_ja || dbItem.name) + '</strong>' + supAgentBadge +
          '<div style="color:var(--text);font-weight:600">' + escapeHtml(dbItem.stat || '') + '</div>' +
          '<div style="color:var(--text-muted);margin-top:4px">' + escapeHtml(dbItem.description || '') + '</div>' +
          (supLinks.length ? '<div style="margin-top:8px">' + supLinks.join(' ') + '</div>' : '') +
          '</div>';
      });
      html += '</div></div>';
    }

    container.innerHTML = html;
  }


  // Render 4-layer architecture from registry (replaces hardcoded HTML)
  function renderArchitecture(data) {
    var archFlow = document.getElementById('archFlow');
    if (!archFlow) return;

    var layersById = {};
    (data.layers || []).forEach(function(l) { layersById[l.id] = l; });

    // Preserve original visual order: Conceptual → Core → Structural → Detection → Output
    var order = [
      { id: 'conceptual', label: 'Conceptual', name: '概念基盤' },
      { id: 'core',       label: 'Core',       name: '基軸DB' },
      { id: 'structural', label: 'Structural', name: '構造理解' },
      { id: 'detection',  label: 'Detection',  name: '変化検出' }
    ];

    var cellsHtml = order.map(function(spec) {
      var layer = layersById[spec.id];
      if (!layer) return '';
      var dbs = layer.databases || [];
      var codes = dbs.map(function(x) { return x.id; }).join('・');
      return '<div class="arch-cell" data-layer="' + escapeHtml(spec.id) + '">' +
        '<div class="arch-layer-label">' + escapeHtml(spec.label) + '</div>' +
        '<div class="arch-layer-name">' + escapeHtml(spec.name) + '</div>' +
        '<div class="arch-layer-count">' + dbs.length + '<span class="arch-layer-count-unit">DB</span></div>' +
        '<div class="arch-layer-codes">' + escapeHtml(codes) + '</div>' +
        '</div>';
    }).join('');

    var totalAgents = (data.totalStats && data.totalStats.totalAgents) || 0;
    cellsHtml += '<div class="arch-cell" data-layer="output">' +
      '<div class="arch-layer-label">Output</div>' +
      '<div class="arch-layer-name">有望領域の特定</div>' +
      '<div class="arch-layer-count">' + escapeHtml(String(totalAgents)) + '<span class="arch-layer-count-unit">AGENTS</span></div>' +
      '<div class="arch-layer-codes">統合分析・予測較正・全エージェント連携</div>' +
      '</div>';

    archFlow.innerHTML = cellsHtml;

    // Update number-bearing subtitles / lead text from registry
    var commerc = (data.extraSections || []).find(function(s) { return s.id === 'commercialization'; });
    var commercCount = commerc ? commerc.databases.length : 0;
    var supCount = (data.supplementary || []).length;
    // Compute totalDBs from actual structure (avoids stale totalStats.totalDatabases drift)
    var layerSum = (data.layers || []).reduce(function(acc, l) { return acc + (l.databases || []).length; }, 0);
    var extraSum = (data.extraSections || []).reduce(function(acc, s) { return acc + (s.databases || []).length; }, 0);
    var totalDBs = layerSum + extraSum + supCount;

    var topSubtitle = document.getElementById('topSubtitle');
    if (topSubtitle && totalDBs) {
      topSubtitle.textContent = 'ミラツク・インテリジェンス・パイプラインを支える' + totalDBs + 'データソース＋専門エージェント';
    }

    var archLead = document.getElementById('archLead');
    if (archLead && commercCount && supCount) {
      archLead.textContent = '概念基盤・基軸DB・構造理解・変化検出という4層のデータベース群が、有望領域の特定という最終出力に向かって流れる。各層は独立した役割を持ちつつ、互いに参照し合うことで、単独では捉えられない構造的変化を可視化する。事業化（' + commercCount + 'DB）と補助DB（' + supCount + '件）が応用層を成す。';
    }

    var dashSubtitle = document.getElementById('dashSubtitle');
    if (dashSubtitle && totalDBs) {
      dashSubtitle.textContent = totalDBs + 'DB横断・ライブKPI・全文検索・エージェント呼び出し';
    }

    var dashCtaTitle = document.getElementById('dashCtaTitle');
    if (dashCtaTitle && totalDBs) {
      dashCtaTitle.textContent = totalDBs + 'DB横断ライブKPI・レイヤー分析・全文検索・専門エージェント連携';
    }
  }

  function formatTs(ts) {
    if (!ts) return '';
    // ISO 8601 -> YYYY-MM-DD HH:MM (no seconds)
    var s = String(ts).replace('T', ' ').replace(/:\d{2}(\.\d+)?([+\-Z].*)?$/, '');
    return s;
  }

  function freshnessClass(ts) {
    if (!ts) return 'stale';
    var t = new Date(String(ts).replace(' ', 'T'));
    if (isNaN(t.getTime())) return '';
    var hoursAgo = (Date.now() - t.getTime()) / 36e5;
    if (hoursAgo <= 36) return 'fresh';
    if (hoursAgo <= 72) return 'warm';
    return 'stale';
  }

  function renderPipelineStatus(data) {
    var pipeline = data.autoUpdatePipeline;
    var container = document.getElementById('pipelineStatus');
    if (!container) return;
    if (!pipeline || !pipeline.databases) {
      container.innerHTML = '';
      return;
    }
    var dbs = pipeline.databases;
    var order = ['PE', 'CI', 'UPR', 'SGPR', 'SG'];
    var rows = order.filter(function(k) { return dbs[k]; }).map(function(k) {
      var d = dbs[k];
      var ts = d.lastUpdated || d.lastChecked;
      var cls = freshnessClass(ts);
      var deltaTxt = '';
      if (typeof d.lastUpdatedDelta === 'number') {
        var sign = d.lastUpdatedDelta >= 0 ? '+' : '';
        deltaTxt = '<span class="pipeline-delta">' + sign + d.lastUpdatedDelta.toLocaleString() + '</span>';
      }
      var rowsTxt = (typeof d.rows === 'number') ? d.rows.toLocaleString() : '-';
      var verb = d.lastUpdated ? '\u66f4\u65b0' : '\u78ba\u8a8d';
      return '<a href="#" data-db="' + escapeHtml(k) + '" class="pipeline-card pipeline-' + cls + '">' +
        '<div class="pipeline-card-head"><span class="pipeline-id">' + escapeHtml(k) + '</span><span class="pipeline-name">' + escapeHtml(d.nameJa || '') + '</span></div>' +
        '<div class="pipeline-card-rows">' + rowsTxt + '<span class="pipeline-card-unit">\u4ef6</span>' + deltaTxt + '</div>' +
        '<div class="pipeline-card-ts">\u6700\u7d42' + verb + ': ' + escapeHtml(formatTs(ts) || '\u672a\u53d6\u5f97') + '</div>' +
        '</a>';
    }).join('');
    var lastRunTxt = formatTs(pipeline.lastRun) || '\u672a\u5b9f\u884c';
    container.innerHTML =
      '<div class="pipeline-status-header">' +
        '<div>' +
          '<div class="pipeline-status-eyebrow">AUTO-UPDATE PIPELINE</div>' +
          '<div class="pipeline-status-title">\u81ea\u52d5\u66f4\u65b0\u30d1\u30a4\u30d7\u30e9\u30a4\u30f3\u72b6\u614b</div>' +
          '<div class="pipeline-status-desc">' + escapeHtml(pipeline.schedule || '') + ' / \u6700\u7d42\u5b9f\u884c: <strong>' + escapeHtml(lastRunTxt) + '</strong></div>' +
        '</div>' +
        (pipeline.repository ? '<a href="' + safeUrl(pipeline.repository) + '" target="_blank" class="pipeline-status-link">Pipeline repo \u2192</a>' : '') +
      '</div>' +
      '<div class="pipeline-status-grid">' + rows + '</div>';
  }

  function renderDbEntry(dbItem) {
    var meta = '';
    if (dbItem.storage) meta += '<span>' + escapeHtml(dbItem.storage) + '</span>';
    if (dbItem.update) meta += '<span>' + escapeHtml(dbItem.update) + '</span>';
    if (dbItem.tables) meta += '<span>' + escapeHtml(String(dbItem.tables)) + '\u30c6\u30fc\u30d6\u30eb</span>';
    if (dbItem.rows) meta += '<span>' + escapeHtml(dbItem.rows.toLocaleString()) + '\u884c</span>';
    if (dbItem.sizeMB) meta += '<span>' + escapeHtml(String(dbItem.sizeMB)) + 'MB</span>';
    // \u6700\u7d42\u66f4\u65b0\u30bf\u30a4\u30e0\u30b9\u30bf\u30f3\u30d7\uff08\u81ea\u52d5\u66f4\u65b0\u30d1\u30a4\u30d7\u30e9\u30a4\u30f3\u5bfe\u8c61DB\uff09
    if (dbItem.isPipelineWatched) {
      var pts = dbItem.lastUpdated || dbItem.lastChecked;
      if (pts) {
        var cls = freshnessClass(pts);
        var verb = dbItem.lastUpdated ? '\u66f4\u65b0' : '\u78ba\u8a8d';
        var deltaTxt = (typeof dbItem.lastUpdatedDelta === 'number')
          ? ' <span class="pipeline-delta-inline">' + (dbItem.lastUpdatedDelta >= 0 ? '+' : '') + dbItem.lastUpdatedDelta.toLocaleString() + '</span>'
          : '';
        meta += '<span class="pipeline-badge pipeline-' + cls + '" title="\u81ea\u52d5\u66f4\u65b0\u30d1\u30a4\u30d7\u30e9\u30a4\u30f3\u7ba1\u8f44">\u2605 \u6700\u7d42' + verb + ' ' + escapeHtml(formatTs(pts)) + deltaTxt + '</span>';
      }
    }

    // Build link list (dashboard / textbook / summary / timeline / report)
    var links = [];
    if (dbItem.dashboard) links.push('<a href="' + safeUrl(dbItem.dashboard) + '" class="db-dashboard-link">\u30c0\u30c3\u30b7\u30e5\u30dc\u30fc\u30c9 &rarr;</a>');
    if (dbItem.textbook) links.push('<a href="' + safeUrl(dbItem.textbook) + '" class="db-dashboard-link">\u6559\u79d1\u66f8 &rarr;</a>');
    if (dbItem.summary) links.push('<a href="' + safeUrl(dbItem.summary) + '" class="db-dashboard-link">\u30b5\u30de\u30ea\u30fc &rarr;</a>');
    if (dbItem.timeline) links.push('<a href="' + safeUrl(dbItem.timeline) + '" class="db-dashboard-link">\u6642\u4ee3\u5909\u9077DB &rarr;</a>');
    if (dbItem.report) links.push('<a href="' + safeUrl(dbItem.report) + '" class="db-dashboard-link">\u30ec\u30dd\u30fc\u30c8 &rarr;</a>');

    // Agent badge (Claude Code slash command)
    var agentBadge = '';
    if (dbItem.agent) {
      agentBadge = '<span class="db-entry-agent" title="Claude Code\u3067' + escapeHtml(dbItem.agent) + '\u3067\u8d77\u52d5">' + escapeHtml(dbItem.agent) + '</span>';
    }

    var statText = String(dbItem.stat || '');
    var descText = String(dbItem.description || '');
    // Heuristic: stat > 80 chars or desc > 180 chars indicates clamp will trigger.
    var needsToggle = statText.length > 80 || descText.length > 180;
    var toggleBtn = needsToggle
      ? '<button type="button" class="db-entry-toggle" data-action="toggle-entry">+ 全文を読む</button>'
      : '';
    return '<div class="db-entry"><div class="db-entry-header">' +
      '<span class="db-entry-id">' + escapeHtml(dbItem.id) + '</span>' +
      '<span class="db-entry-name">' + escapeHtml(dbItem.nameJa) + '</span>' +
      agentBadge + '</div>' +
      '<div class="db-entry-stat">' + escapeHtml(statText) + '</div>' +
      '<div class="db-entry-desc">' + escapeHtml(descText) + '</div>' +
      toggleBtn +
      (meta ? '<div class="db-entry-meta">' + meta + '</div>' : '') +
      (links.length ? '<div class="db-entry-links">' + links.join('') + '</div>' : '') + '</div>';
  }

  // Wire up click-to-expand on db-entry cards (event delegation).
  document.addEventListener('click', function(e) {
    var toggle = e.target.closest('[data-action="toggle-entry"]');
    if (toggle) {
      e.stopPropagation();
      e.preventDefault();
      var entry = toggle.closest('.db-entry');
      if (entry) {
        var expanded = entry.classList.toggle('is-expanded');
        toggle.textContent = expanded ? '− 折りたたむ' : '+ 全文を読む';
      }
      return;
    }
    // Clicking on the card area (but not inside a link or button) toggles too.
    var entry = e.target.closest('.db-entry');
    if (!entry) return;
    if (e.target.closest('a, button')) return;
    var expanded = entry.classList.toggle('is-expanded');
    var btn = entry.querySelector('[data-action="toggle-entry"]');
    if (btn) btn.textContent = expanded ? '− 折りたたむ' : '+ 全文を読む';
  });
})();
