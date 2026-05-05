'use strict';
var _dbRegistryLoaded = false;

initNav('databases');
initAuthGuard(function(user) {
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

    var container = document.getElementById('dbLayersContent');
    var html = '';
    data.layers.forEach(function(layer) {
      html += '<div class="db-layer"><div class="db-layer-header">' +
        '<div class="db-layer-title">' + escapeHtml(layer.name) + '</div>' +
        '<div class="db-layer-desc">' + escapeHtml(layer.description) + '</div></div>' +
        '<div class="db-layer-grid">';
      layer.databases.forEach(function(dbItem) { html += renderDbEntry(dbItem); });
      html += '</div></div>';
    });
    // \u88dc\u52a9\u30c7\u30fc\u30bf\u30d9\u30fc\u30b9\uff08\u65e2\u5b58\u306e\u30d5\u30e9\u30c3\u30c8\u30ea\u30b9\u30c8\uff09
    if (data.supplementary && data.supplementary.length > 0) {
      html += '<div class="db-supplementary"><div class="db-supplementary-title">\u88dc\u52a9\u30c7\u30fc\u30bf\u30d9\u30fc\u30b9</div>';
      html += '<div class="db-supplementary-grid">';
      data.supplementary.forEach(function(dbItem) {
        html += '<div class="db-supplementary-item"><strong>' + escapeHtml(dbItem.id) + ': ' + escapeHtml(dbItem.nameJa) + '</strong>' +
          '<div>' + escapeHtml(dbItem.stat) + '</div>' +
          '<div style="color:var(--text-muted);margin-top:2px">' + escapeHtml(dbItem.description) + '</div>' +
          (dbItem.dashboard ? '<div style="margin-top:6px"><a href="' + safeUrl(dbItem.dashboard) + '" class="db-dashboard-link">\u30c0\u30c3\u30b7\u30e5\u30dc\u30fc\u30c9 &rarr;</a></div>' : '') +
          '</div>';
      });
      html += '</div></div>';
    }

    // \u88dc\u52a9DB\u306e\u4e0b\u306b\u4e26\u3076\u72ec\u7acb\u30bb\u30af\u30b7\u30e7\u30f3\uff08\u4e8b\u696d\u5316\u306a\u3069\uff09
    if (data.extraSections && data.extraSections.length > 0) {
      data.extraSections.forEach(function(section) {
        html += '<div class="db-extra-section">' +
          '<div class="db-extra-header">' +
            '<div class="db-extra-title">' + escapeHtml(section.name) + '</div>' +
            (section.description ? '<div class="db-extra-desc">' + escapeHtml(section.description) + '</div>' : '') +
          '</div>' +
          '<div class="db-layer-grid">';
        section.databases.forEach(function(dbItem) {
          html += renderDbEntry(dbItem);
        });
        html += '</div></div>';
      });
    }

    container.innerHTML = html;
  }


  function renderDbEntry(dbItem) {
    var meta = '';
    if (dbItem.storage) meta += '<span>' + escapeHtml(dbItem.storage) + '</span>';
    if (dbItem.update) meta += '<span>' + escapeHtml(dbItem.update) + '</span>';
    if (dbItem.tables) meta += '<span>' + escapeHtml(String(dbItem.tables)) + '\u30c6\u30fc\u30d6\u30eb</span>';
    if (dbItem.rows) meta += '<span>' + escapeHtml(dbItem.rows.toLocaleString()) + '\u884c</span>';
    if (dbItem.sizeMB) meta += '<span>' + escapeHtml(String(dbItem.sizeMB)) + 'MB</span>';

    // Build link list (dashboard / textbook / timeline / report)
    var links = [];
    var dashLabel = dbItem.textbook ? '\u6559\u79d1\u66f8' : '\u30c0\u30c3\u30b7\u30e5\u30dc\u30fc\u30c9';
    if (dbItem.dashboard) links.push('<a href="' + safeUrl(dbItem.dashboard) + '" class="db-dashboard-link">' + dashLabel + ' &rarr;</a>');
    if (dbItem.timeline) links.push('<a href="' + safeUrl(dbItem.timeline) + '" class="db-dashboard-link">\u6642\u4ee3\u5909\u9077DB &rarr;</a>');
    if (dbItem.report) links.push('<a href="' + safeUrl(dbItem.report) + '" class="db-dashboard-link">\u30ec\u30dd\u30fc\u30c8 &rarr;</a>');

    return '<div class="db-entry"><div class="db-entry-header">' +
      '<span class="db-entry-id">' + escapeHtml(dbItem.id) + '</span>' +
      '<span class="db-entry-name">' + escapeHtml(dbItem.nameJa) + '</span></div>' +
      '<div class="db-entry-stat">' + escapeHtml(dbItem.stat) + '</div>' +
      '<div class="db-entry-desc">' + escapeHtml(dbItem.description) + '</div>' +
      (meta ? '<div class="db-entry-meta">' + meta + '</div>' : '') +
      (links.length ? '<div class="db-entry-links">' + links.join('') + '</div>' : '') + '</div>';
  }
});
