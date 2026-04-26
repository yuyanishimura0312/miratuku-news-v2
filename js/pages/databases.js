'use strict';
initNav('databases');
initAuthGuard(function(user) {
  loadDatabaseRegistry();

  var dbRegistryLoaded = false;

  function loadDatabaseRegistry() {
    if (dbRegistryLoaded) return;
    fetch('data/db-registry.json')
      .then(function(res) { return res.json(); })
      .then(function(data) {
        renderDatabaseRegistry(data);
        dbRegistryLoaded = true;
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
      '<div class="db-overview-card"><div class="db-overview-value">' + stats.totalDatabases + '</div><div class="db-overview-label">\u30c7\u30fc\u30bf\u30d9\u30fc\u30b9</div></div>' +
      '<div class="db-overview-card"><div class="db-overview-value">' + stats.totalRecords + '</div><div class="db-overview-label">\u7dcf\u30ec\u30b3\u30fc\u30c9\u6570</div></div>' +
      '<div class="db-overview-card"><div class="db-overview-value">' + stats.layers + '</div><div class="db-overview-label">\u30a2\u30fc\u30ad\u30c6\u30af\u30c1\u30e3\u5c64</div></div>' +
      '<div class="db-overview-card"><div class="db-overview-value">' + stats.updateFrequency + '</div><div class="db-overview-label">\u66f4\u65b0\u983b\u5ea6</div></div>';

    var container = document.getElementById('dbLayersContent');
    var html = '';
    data.layers.forEach(function(layer) {
      html += '<div class="db-layer"><div class="db-layer-header">' +
        '<div class="db-layer-title">' + layer.name + '</div>' +
        '<div class="db-layer-desc">' + layer.description + '</div></div>' +
        '<div class="db-layer-grid">';
      layer.databases.forEach(function(dbItem) { html += renderDbEntry(dbItem); });
      html += '</div></div>';
    });
    if (data.supplementary && data.supplementary.length > 0) {
      html += '<div class="db-supplementary"><div class="db-supplementary-title">\u88dc\u52a9\u30c7\u30fc\u30bf\u30d9\u30fc\u30b9</div><div class="db-supplementary-grid">';
      data.supplementary.forEach(function(dbItem) {
        html += '<div class="db-supplementary-item"><strong>' + dbItem.id + ': ' + dbItem.nameJa + '</strong>' +
          '<div>' + dbItem.stat + '</div>' +
          '<div style="color:var(--text-muted);margin-top:2px">' + dbItem.description + '</div></div>';
      });
      html += '</div></div>';
    }
    container.innerHTML = html;
  }

  function renderDbEntry(dbItem) {
    var meta = '';
    if (dbItem.storage) meta += '<span>' + dbItem.storage + '</span>';
    if (dbItem.update) meta += '<span>' + dbItem.update + '</span>';
    if (dbItem.tables) meta += '<span>' + dbItem.tables + '\u30c6\u30fc\u30d6\u30eb</span>';
    if (dbItem.rows) meta += '<span>' + dbItem.rows.toLocaleString() + '\u884c</span>';
    if (dbItem.sizeMB) meta += '<span>' + dbItem.sizeMB + 'MB</span>';
    var dashboardLink = dbItem.dashboard ? '<a href="' + dbItem.dashboard + '" style="font-size:0.72rem;color:var(--accent-warm);font-weight:500">\u30c0\u30c3\u30b7\u30e5\u30dc\u30fc\u30c9 &rarr;</a>' : '';
    return '<div class="db-entry"><div class="db-entry-header">' +
      '<span class="db-entry-id">' + dbItem.id + '</span>' +
      '<span class="db-entry-name">' + dbItem.nameJa + '</span></div>' +
      '<div class="db-entry-stat">' + dbItem.stat + '</div>' +
      '<div class="db-entry-desc">' + dbItem.description + '</div>' +
      (meta ? '<div class="db-entry-meta">' + meta + '</div>' : '') +
      (dashboardLink ? '<div style="margin-top:8px">' + dashboardLink + '</div>' : '') + '</div>';
  }
});
