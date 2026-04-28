'use strict';
initNav('analysis-reports');
initAuthGuard(function(user) {
  loadAnalysisReports();

  function loadAnalysisReports() {
    fetch('data/analysis-reports.json')
      .then(function(res) { return res.json(); })
      .then(function(data) {
        renderAnalysisReports(data);
      })
      .catch(function(err) {
        console.error('Analysis reports load error:', err);
        document.getElementById('analysisReportsContent').innerHTML =
          '<p style="color:var(--text-muted)">\u30ec\u30dd\u30fc\u30c8\u306e\u8aad\u307f\u8fbc\u307f\u306b\u5931\u6557\u3057\u307e\u3057\u305f\u3002</p>';
      });
  }

  // State management via localStorage
  function getArchived() {
    try { return JSON.parse(localStorage.getItem('ar_archived') || '[]'); } catch(e) { return []; }
  }
  function setArchived(ids) {
    localStorage.setItem('ar_archived', JSON.stringify(ids));
  }
  function getDeleted() {
    try { return JSON.parse(localStorage.getItem('ar_deleted') || '[]'); } catch(e) { return []; }
  }
  function setDeleted(ids) {
    localStorage.setItem('ar_deleted', JSON.stringify(ids));
  }

  function archiveReport(id) {
    var list = getArchived();
    if (list.indexOf(id) === -1) list.push(id);
    setArchived(list);
  }
  function unarchiveReport(id) {
    var list = getArchived().filter(function(x) { return x !== id; });
    setArchived(list);
  }
  function deleteReport(id) {
    var list = getDeleted();
    if (list.indexOf(id) === -1) list.push(id);
    setDeleted(list);
  }
  function restoreReport(id) {
    var list = getDeleted().filter(function(x) { return x !== id; });
    setDeleted(list);
  }

  var currentData = null;

  function renderAnalysisReports(data) {
    currentData = data;
    var container = document.getElementById('analysisReportsContent');
    var archived = getArchived();
    var deleted = getDeleted();

    var activeReports = [];
    var archivedReports = [];
    var deletedReports = [];

    data.reports.forEach(function(r) {
      if (deleted.indexOf(r.id) !== -1) {
        deletedReports.push(r);
      } else if (archived.indexOf(r.id) !== -1) {
        archivedReports.push(r);
      } else {
        activeReports.push(r);
      }
    });

    var html = '';

    // Back button
    html += '<div style="margin-bottom:16px"><a href="databases.html" style="font-size:0.78rem;color:var(--text-secondary);text-decoration:none">&larr; \u30c7\u30fc\u30bf\u30d9\u30fc\u30b9\u306b\u623b\u308b</a></div>';

    // Description
    html += '<p style="font-size:0.84rem;color:var(--text-secondary);line-height:1.7;max-width:720px;margin-bottom:24px">' + escapeHtml(data.description) + '</p>';

    // Overview
    var visibleReports = activeReports.concat(archivedReports);
    var uniqueDbs = {};
    var uniqueTags = {};
    visibleReports.forEach(function(r) {
      (r.databases || []).forEach(function(d) { uniqueDbs[d] = true; });
      (r.tags || []).forEach(function(t) { uniqueTags[t] = true; });
    });
    var totalWords = visibleReports.reduce(function(s, r) { return s + (r.word_count || 0); }, 0);

    html += '<div class="db-overview" style="margin-bottom:24px">' +
      '<div class="db-overview-card"><div class="db-overview-value">' + activeReports.length + '</div><div class="db-overview-label">\u30ec\u30dd\u30fc\u30c8\u6570</div></div>' +
      '<div class="db-overview-card"><div class="db-overview-value">' + Object.keys(uniqueDbs).length + '</div><div class="db-overview-label">\u53c2\u7167DB\u6570</div></div>' +
      '<div class="db-overview-card"><div class="db-overview-value">' + Object.keys(uniqueTags).length + '</div><div class="db-overview-label">\u30c8\u30d4\u30c3\u30af</div></div>' +
      '<div class="db-overview-card"><div class="db-overview-value">' + Math.round(totalWords / 1000) + 'K</div><div class="db-overview-label">\u7dcf\u6587\u5b57\u6570</div></div>' +
    '</div>';

    // Active reports
    html += renderReportCards(activeReports, 'active');

    // Archived section
    if (archivedReports.length > 0) {
      html += '<div style="margin-top:40px;border-top:2px solid var(--border);padding-top:20px">';
      html += '<h3 style="font-family:var(--font-serif);font-size:1rem;font-weight:700;color:var(--text-muted);margin-bottom:16px">';
      html += '\u30a2\u30fc\u30ab\u30a4\u30d6 <span style="font-size:0.78rem;font-weight:400">(' + archivedReports.length + '\u4ef6)</span></h3>';
      html += renderReportCards(archivedReports, 'archived');
      html += '</div>';
    }

    // Deleted section
    if (deletedReports.length > 0) {
      html += '<div style="margin-top:40px;border-top:1px dashed var(--border);padding-top:20px">';
      html += '<h3 style="font-family:var(--font-serif);font-size:0.88rem;font-weight:700;color:var(--text-muted);margin-bottom:12px">';
      html += '\u524a\u9664\u6e08\u307f <span style="font-size:0.72rem;font-weight:400">(' + deletedReports.length + '\u4ef6)</span></h3>';
      deletedReports.forEach(function(r) {
        html += '<div style="display:flex;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid var(--border-light);opacity:0.5">';
        html += '<span style="font-size:0.82rem;flex:1">' + escapeHtml(r.title) + '</span>';
        html += '<button class="ar-btn ar-btn-restore" data-id="' + escapeHtml(r.id) + '" style="font-size:0.68rem;padding:2px 8px;border:1px solid var(--border);background:none;color:var(--text-muted);cursor:pointer">\u5fa9\u5143</button>';
        html += '</div>';
      });
      html += '</div>';
    }

    container.innerHTML = html;

    // Event delegation for buttons
    container.addEventListener('click', function(e) {
      var btn = e.target.closest('[data-id]');
      if (!btn) return;
      var id = btn.dataset.id;

      if (btn.classList.contains('ar-btn-archive')) {
        archiveReport(id);
        renderAnalysisReports(currentData);
      } else if (btn.classList.contains('ar-btn-unarchive')) {
        unarchiveReport(id);
        renderAnalysisReports(currentData);
      } else if (btn.classList.contains('ar-btn-delete')) {
        if (confirm('\u300c' + id + '\u300d\u3092\u524a\u9664\u3057\u307e\u3059\u304b\uff1f')) {
          deleteReport(id);
          renderAnalysisReports(currentData);
        }
      } else if (btn.classList.contains('ar-btn-restore')) {
        restoreReport(id);
        renderAnalysisReports(currentData);
      }
    });

    // Lazy-load full text on expand
    container.querySelectorAll('details').forEach(function(det) {
      det.addEventListener('toggle', function() {
        if (!this.open) return;
        var body = this.querySelector('.fulltext-body');
        if (!body || body.dataset.loaded) return;
        body.dataset.loaded = 'true';
        var file = body.dataset.file;
        fetch(file).then(function(res) { return res.text(); }).then(function(text) {
          body.innerHTML = renderMarkdown(text);
        }).catch(function() {
          body.innerHTML = '<p class="text-muted">\u8aad\u307f\u8fbc\u307f\u306b\u5931\u6557\u3057\u307e\u3057\u305f\u3002</p>';
        });
      });
    });
  }

  function renderReportCards(reports, mode) {
    var html = '';
    reports.forEach(function(r) {
      var dbBadges = (r.databases || []).map(function(d) {
        return '<span style="display:inline-block;padding:1px 6px;background:var(--accent-warm);color:#fff;border-radius:3px;font-size:0.65rem;font-weight:600">' + escapeHtml(d) + '</span>';
      }).join(' ');
      var tagBadges = (r.tags || []).map(function(t) {
        return '<span style="display:inline-block;padding:1px 6px;background:var(--surface-alt, #f0f0f0);color:var(--text-secondary);border-radius:3px;font-size:0.65rem">' + escapeHtml(t) + '</span>';
      }).join(' ');
      var findings = (r.key_findings || []).map(function(f) {
        return '<div style="font-size:0.78rem;color:var(--text-secondary);padding:3px 0;border-bottom:1px solid var(--border-light, #eee)">- ' + escapeHtml(f) + '</div>';
      }).join('');

      var opacity = mode === 'archived' ? 'opacity:0.7;' : '';
      html += '<div class="report-archive-card" style="margin-bottom:16px;' + opacity + '">' +
        '<div class="report-archive-header">' +
          '<div class="report-archive-title" style="font-size:1.05rem">' + escapeHtml(r.title) + '</div>' +
          '<span class="report-archive-region">' + escapeHtml(r.date) + '</span>' +
        '</div>' +
        '<div style="font-size:0.8rem;color:var(--text-secondary);margin-bottom:8px">' + escapeHtml(r.subtitle || '') + '</div>' +
        '<div style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:8px">' + dbBadges + ' ' + tagBadges + '</div>' +
        '<div class="report-archive-preview" style="margin-bottom:8px">' + escapeHtml(r.summary || '') + '</div>';

      if (findings) {
        html += '<div class="report-obs-label">\u4e3b\u8981\u306a\u767a\u898b</div>' + findings;
      }

      html += '<div style="display:flex;gap:12px;margin-top:10px;font-size:0.72rem;color:var(--text-muted)">';
      if (r.word_count) html += '<span>' + r.word_count.toLocaleString() + '\u6587\u5b57</span>';
      if (r.sections) html += '<span>' + r.sections + '\u7ae0</span>';
      html += '</div>';

      // Action buttons row
      html += '<div style="display:flex;gap:8px;margin-top:12px;align-items:center">';
      if (r.report_file) {
        html += '<a href="' + escapeHtml(r.report_file) + '" target="_blank" style="display:inline-flex;align-items:center;gap:4px;padding:6px 12px;background:var(--accent-warm);color:#fff;border-radius:4px;font-size:0.75rem;font-weight:500;text-decoration:none">\u30ec\u30dd\u30fc\u30c8\u3092\u8aad\u3080 &rarr;</a>';
      }
      if (r.dashboard) {
        html += '<a href="' + escapeHtml(r.dashboard) + '" target="_blank" style="display:inline-flex;align-items:center;gap:4px;padding:6px 12px;border:1px solid var(--border);color:var(--text-secondary);border-radius:4px;font-size:0.75rem;text-decoration:none">\u30c0\u30c3\u30b7\u30e5\u30dc\u30fc\u30c9 &rarr;</a>';
      }

      // Archive / Unarchive button
      html += '<span style="flex:1"></span>';
      if (mode === 'active') {
        html += '<button class="ar-btn ar-btn-archive" data-id="' + escapeHtml(r.id) + '" style="padding:5px 10px;border:1px solid var(--border);background:none;color:var(--text-muted);border-radius:4px;font-size:0.72rem;cursor:pointer">\u30a2\u30fc\u30ab\u30a4\u30d6</button>';
      } else if (mode === 'archived') {
        html += '<button class="ar-btn ar-btn-unarchive" data-id="' + escapeHtml(r.id) + '" style="padding:5px 10px;border:1px solid var(--border);background:none;color:var(--text-muted);border-radius:4px;font-size:0.72rem;cursor:pointer">\u623b\u3059</button>';
      }
      // Delete button
      html += '<button class="ar-btn ar-btn-delete" data-id="' + escapeHtml(r.id) + '" style="padding:5px 10px;border:1px solid var(--border);background:none;color:var(--text-muted);border-radius:4px;font-size:0.72rem;cursor:pointer">\u524a\u9664</button>';
      html += '</div>';

      if (r.report_file) {
        html += '<details style="margin-top:12px"><summary class="fulltext-toggle">\u5168\u6587\u3092\u8868\u793a</summary>' +
          '<div class="fulltext-body md-body" id="ar-fulltext-' + escapeHtml(r.id) + '" data-file="' + escapeHtml(r.report_file) + '">' +
          '<div class="loading-indicator" style="padding:12px"><div class="loading-spinner loading-spinner-sm"></div><span>\u8aad\u307f\u8fbc\u307f\u4e2d...</span></div>' +
          '</div></details>';
      }

      html += '</div>';
    });
    return html;
  }
});
