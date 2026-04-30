'use strict';
initNav('analysis-reports');
initAuthGuard(function(user) {
  loadAnalysisReports();

  function loadAnalysisReports() {
    fetch('data/analysis-reports.json')
      .then(function(res) { return res.json(); })
      .then(function(data) { initPage(data); })
      .catch(function(err) {
        console.error('Analysis reports load error:', err);
        document.getElementById('analysisReportsContent').innerHTML =
          '<p class="text-muted">\u30ec\u30dd\u30fc\u30c8\u306e\u8aad\u307f\u8fbc\u307f\u306b\u5931\u6557\u3057\u307e\u3057\u305f\u3002</p>';
      });
  }

  // --- State ---
  function getArchived() {
    try { return JSON.parse(localStorage.getItem('ar_archived') || '[]'); } catch(e) { return []; }
  }
  function setArchived(ids) { localStorage.setItem('ar_archived', JSON.stringify(ids)); }
  function getDeleted() {
    try { return JSON.parse(localStorage.getItem('ar_deleted') || '[]'); } catch(e) { return []; }
  }
  function setDeleted(ids) { localStorage.setItem('ar_deleted', JSON.stringify(ids)); }

  var currentData = null;
  var currentQuery = '';
  var currentSort = 'date-desc';
  var activeDbFilter = '';

  // --- Init ---
  function initPage(data) {
    currentData = data;
    var container = document.getElementById('analysisReportsContent');
    container.innerHTML = buildPageHTML(data);
    bindEvents(container);
    applyFilters();
  }

  // --- Build static page structure ---
  function buildPageHTML(data) {
    var html = '';

    // Back link
    html += '<div style="margin-bottom:16px"><a href="databases.html" style="font-size:0.78rem;color:var(--text-secondary);text-decoration:none">&larr; \u30c7\u30fc\u30bf\u30d9\u30fc\u30b9\u306b\u623b\u308b</a></div>';

    // Description
    html += '<p style="font-size:0.84rem;color:var(--text-secondary);line-height:1.7;max-width:720px;margin-bottom:24px">' + escapeHtml(data.description) + '</p>';

    // Overview stats
    html += '<div class="db-overview" id="ar-stats"></div>';

    // Toolbar: search + sort
    html += '<div class="ar-toolbar">';
    html += '<input type="text" class="ar-search" id="ar-search" placeholder="\u30ec\u30dd\u30fc\u30c8\u3092\u691c\u7d22...">';
    html += '<select class="ar-sort" id="ar-sort">';
    html += '<option value="date-desc">\u65b0\u3057\u3044\u9806</option>';
    html += '<option value="date-asc">\u53e4\u3044\u9806</option>';
    html += '<option value="words-desc">\u6587\u5b57\u6570\u304c\u591a\u3044\u9806</option>';
    html += '<option value="title-asc">\u30bf\u30a4\u30c8\u30eb\u9806</option>';
    html += '</select>';
    html += '</div>';

    // DB filter tags
    html += '<div class="ar-tag-filters" id="ar-db-filters"></div>';

    // Report cards container
    html += '<div id="ar-cards"></div>';

    // Archived section
    html += '<div id="ar-archived-section"></div>';

    // Deleted section
    html += '<div id="ar-deleted-section"></div>';

    return html;
  }

  // --- Collect unique DBs ---
  function collectDatabases(reports) {
    var dbMap = {};
    reports.forEach(function(r) {
      (r.databases || []).forEach(function(d) {
        dbMap[d] = (dbMap[d] || 0) + 1;
      });
    });
    return dbMap;
  }

  // --- Render DB filter buttons ---
  function renderDbFilters(reports) {
    var dbMap = collectDatabases(reports);
    var entries = Object.keys(dbMap).sort(function(a, b) { return dbMap[b] - dbMap[a]; });
    var html = '<button class="ar-tag-btn' + (activeDbFilter === '' ? ' active' : '') + '" data-db="">\u3059\u3079\u3066</button>';
    entries.forEach(function(db) {
      html += '<button class="ar-tag-btn' + (activeDbFilter === db ? ' active' : '') + '" data-db="' + escapeHtml(db) + '">' + escapeHtml(db) + ' <span style="opacity:0.6">(' + dbMap[db] + ')</span></button>';
    });
    document.getElementById('ar-db-filters').innerHTML = html;
  }

  // --- Render stats ---
  function renderStats(reports) {
    var uniqueDbs = {};
    var uniqueTags = {};
    reports.forEach(function(r) {
      (r.databases || []).forEach(function(d) { uniqueDbs[d] = true; });
      (r.tags || []).forEach(function(t) { uniqueTags[t] = true; });
    });
    var totalWords = reports.reduce(function(s, r) { return s + (r.word_count || 0); }, 0);

    document.getElementById('ar-stats').innerHTML =
      '<div class="db-overview-card"><div class="db-overview-value">' + reports.length + '</div><div class="db-overview-label">\u30ec\u30dd\u30fc\u30c8\u6570</div></div>' +
      '<div class="db-overview-card"><div class="db-overview-value">' + Object.keys(uniqueDbs).length + '</div><div class="db-overview-label">\u53c2\u7167DB\u6570</div></div>' +
      '<div class="db-overview-card"><div class="db-overview-value">' + Object.keys(uniqueTags).length + '</div><div class="db-overview-label">\u30c8\u30d4\u30c3\u30af</div></div>' +
      '<div class="db-overview-card"><div class="db-overview-value">' + Math.round(totalWords / 1000) + 'K</div><div class="db-overview-label">\u7dcf\u6587\u5b57\u6570</div></div>';
  }

  // --- Sort ---
  function sortReports(reports) {
    var sorted = reports.slice();
    switch (currentSort) {
      case 'date-desc':
        sorted.sort(function(a, b) { return (b.date || '').localeCompare(a.date || ''); });
        break;
      case 'date-asc':
        sorted.sort(function(a, b) { return (a.date || '').localeCompare(b.date || ''); });
        break;
      case 'words-desc':
        sorted.sort(function(a, b) { return (b.word_count || 0) - (a.word_count || 0); });
        break;
      case 'title-asc':
        sorted.sort(function(a, b) { return (a.title || '').localeCompare(b.title || ''); });
        break;
    }
    return sorted;
  }

  // --- Filter ---
  function matchesQuery(r, q) {
    if (!q) return true;
    var text = (r.title + ' ' + (r.subtitle || '') + ' ' + (r.summary || '') + ' ' +
      (r.databases || []).join(' ') + ' ' + (r.tags || []).join(' ')).toLowerCase();
    return q.split(/\s+/).every(function(w) { return text.indexOf(w) !== -1; });
  }

  function matchesDbFilter(r) {
    if (!activeDbFilter) return true;
    return (r.databases || []).indexOf(activeDbFilter) !== -1;
  }

  // --- Apply all filters and render ---
  function applyFilters() {
    var archived = getArchived();
    var deleted = getDeleted();

    var activeReports = [];
    var archivedReports = [];
    var deletedReports = [];

    currentData.reports.forEach(function(r) {
      if (deleted.indexOf(r.id) !== -1) {
        deletedReports.push(r);
      } else if (archived.indexOf(r.id) !== -1) {
        archivedReports.push(r);
      } else {
        activeReports.push(r);
      }
    });

    // Stats use all visible (active + archived)
    var visibleAll = activeReports.concat(archivedReports);
    renderStats(visibleAll);
    renderDbFilters(visibleAll);

    // Filter active reports
    var q = currentQuery.toLowerCase();
    var filtered = activeReports.filter(function(r) {
      return matchesQuery(r, q) && matchesDbFilter(r);
    });
    filtered = sortReports(filtered);

    // Render active cards
    var cardsEl = document.getElementById('ar-cards');
    if (filtered.length === 0 && activeReports.length > 0) {
      cardsEl.innerHTML = '<div class="ar-no-results">\u8a72\u5f53\u3059\u308b\u30ec\u30dd\u30fc\u30c8\u304c\u3042\u308a\u307e\u305b\u3093</div>';
    } else {
      cardsEl.innerHTML = renderCards(filtered, 'active');
    }

    // Archived section
    var archivedEl = document.getElementById('ar-archived-section');
    if (archivedReports.length > 0) {
      var filteredArchived = archivedReports.filter(function(r) {
        return matchesQuery(r, q) && matchesDbFilter(r);
      });
      filteredArchived = sortReports(filteredArchived);
      archivedEl.innerHTML =
        '<div class="ar-section-header"><h3 class="ar-section-title">\u30a2\u30fc\u30ab\u30a4\u30d6 <span class="ar-section-count">(' + archivedReports.length + '\u4ef6)</span></h3></div>' +
        renderCards(filteredArchived, 'archived');
    } else {
      archivedEl.innerHTML = '';
    }

    // Deleted section
    var deletedEl = document.getElementById('ar-deleted-section');
    if (deletedReports.length > 0) {
      var dhtml = '<div class="ar-deleted-section"><h3 class="ar-section-title" style="font-size:0.88rem;margin-bottom:12px">\u524a\u9664\u6e08\u307f <span class="ar-section-count">(' + deletedReports.length + '\u4ef6)</span></h3>';
      deletedReports.forEach(function(r) {
        dhtml += '<div class="ar-deleted-row"><span class="ar-deleted-title">' + escapeHtml(r.title) + '</span>' +
          '<button class="ar-btn-ghost ar-btn-restore" data-id="' + escapeHtml(r.id) + '">\u5fa9\u5143</button></div>';
      });
      dhtml += '</div>';
      deletedEl.innerHTML = dhtml;
    } else {
      deletedEl.innerHTML = '';
    }

    // Lazy-load full text
    bindFulltextToggles();
  }

  // --- Render cards ---
  function renderCards(reports, mode) {
    var html = '';
    reports.forEach(function(r) {
      var dbBadges = (r.databases || []).map(function(d) {
        return '<span class="report-archive-badge-db">' + escapeHtml(d) + '</span>';
      }).join('');
      var tagBadges = (r.tags || []).map(function(t) {
        return '<span class="report-archive-badge-tag">' + escapeHtml(t) + '</span>';
      }).join('');

      var archivedClass = mode === 'archived' ? ' is-archived' : '';
      html += '<div class="report-archive-card' + archivedClass + '">';

      // Header
      html += '<div class="report-archive-header">';
      html += '<div class="report-archive-title">' + escapeHtml(r.title) + '</div>';
      html += '<span class="report-archive-date">' + escapeHtml(r.date) + '</span>';
      html += '</div>';

      // Subtitle
      if (r.subtitle) {
        html += '<div class="report-archive-subtitle">' + escapeHtml(r.subtitle) + '</div>';
      }

      // Badges
      if (dbBadges || tagBadges) {
        html += '<div class="report-archive-badges">' + dbBadges + tagBadges + '</div>';
      }

      // Summary
      if (r.summary) {
        html += '<div class="report-archive-preview">' + escapeHtml(r.summary) + '</div>';
      }

      // Key findings
      if (r.key_findings && r.key_findings.length > 0) {
        html += '<div class="report-archive-findings"><div class="report-obs-label">\u4e3b\u8981\u306a\u767a\u898b</div>';
        r.key_findings.forEach(function(f) {
          html += '<div class="report-archive-finding">- ' + escapeHtml(f) + '</div>';
        });
        html += '</div>';
      }

      // Meta
      html += '<div class="report-archive-meta">';
      if (r.word_count) html += '<span>' + r.word_count.toLocaleString() + '\u6587\u5b57</span>';
      if (r.sections) html += '<span>' + r.sections + '\u7ae0</span>';
      html += '</div>';

      // Actions
      html += '<div class="report-archive-actions">';
      if (r.report_file) {
        html += '<a href="' + escapeHtml(r.report_file) + '" target="_blank" class="ar-btn-primary">\u30ec\u30dd\u30fc\u30c8\u3092\u8aad\u3080 &rarr;</a>';
      }
      if (r.dashboard) {
        html += '<a href="' + escapeHtml(r.dashboard) + '" target="_blank" class="ar-btn-secondary">\u30c0\u30c3\u30b7\u30e5\u30dc\u30fc\u30c9 &rarr;</a>';
      }
      html += '<span class="ar-spacer"></span>';
      if (mode === 'active') {
        html += '<button class="ar-btn-ghost ar-btn-archive" data-id="' + escapeHtml(r.id) + '">\u30a2\u30fc\u30ab\u30a4\u30d6</button>';
      } else if (mode === 'archived') {
        html += '<button class="ar-btn-ghost ar-btn-unarchive" data-id="' + escapeHtml(r.id) + '">\u623b\u3059</button>';
      }
      html += '<button class="ar-btn-ghost ar-btn-delete" data-id="' + escapeHtml(r.id) + '">\u524a\u9664</button>';
      html += '</div>';

      // Fulltext toggle
      if (r.report_file) {
        html += '<details style="margin-top:12px"><summary class="fulltext-toggle">\u5168\u6587\u3092\u8868\u793a</summary>' +
          '<div class="fulltext-body md-body" data-file="' + escapeHtml(r.report_file) + '">' +
          '<div class="loading-indicator" style="padding:12px"><div class="loading-spinner loading-spinner-sm"></div><span>\u8aad\u307f\u8fbc\u307f\u4e2d...</span></div>' +
          '</div></details>';
      }

      html += '</div>';
    });
    return html;
  }

  // --- Fulltext lazy load ---
  function bindFulltextToggles() {
    document.querySelectorAll('#analysisReportsContent details').forEach(function(det) {
      if (det.dataset.bound) return;
      det.dataset.bound = 'true';
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

  // --- Event binding ---
  function bindEvents(container) {
    // Search
    var searchEl = document.getElementById('ar-search');
    var debounceTimer;
    searchEl.addEventListener('input', function() {
      clearTimeout(debounceTimer);
      var val = this.value;
      debounceTimer = setTimeout(function() {
        currentQuery = val;
        applyFilters();
      }, 200);
    });

    // Sort
    document.getElementById('ar-sort').addEventListener('change', function() {
      currentSort = this.value;
      applyFilters();
    });

    // DB filter buttons (delegated)
    document.getElementById('ar-db-filters').addEventListener('click', function(e) {
      var btn = e.target.closest('.ar-tag-btn');
      if (!btn) return;
      activeDbFilter = btn.dataset.db || '';
      applyFilters();
    });

    // Action buttons (delegated on container)
    container.addEventListener('click', function(e) {
      var btn = e.target.closest('[data-id]');
      if (!btn) return;
      if (btn.tagName === 'A') return; // don't intercept links
      var id = btn.dataset.id;

      if (btn.classList.contains('ar-btn-archive')) {
        var list = getArchived();
        if (list.indexOf(id) === -1) list.push(id);
        setArchived(list);
        applyFilters();
      } else if (btn.classList.contains('ar-btn-unarchive')) {
        setArchived(getArchived().filter(function(x) { return x !== id; }));
        applyFilters();
      } else if (btn.classList.contains('ar-btn-delete')) {
        if (confirm('\u300c' + id + '\u300d\u3092\u524a\u9664\u3057\u307e\u3059\u304b\uff1f')) {
          var dl = getDeleted();
          if (dl.indexOf(id) === -1) dl.push(id);
          setDeleted(dl);
          applyFilters();
        }
      } else if (btn.classList.contains('ar-btn-restore')) {
        setDeleted(getDeleted().filter(function(x) { return x !== id; }));
        applyFilters();
      }
    });
  }
});
