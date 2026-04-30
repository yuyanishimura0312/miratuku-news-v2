'use strict';
var WORKER_BASE = 'https://future-insight-proxy.nishimura-69a.workers.dev';

initNav('analysis-reports');
initAuthGuard(function(user) {
  var currentUser = user;
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
  function getList(key) {
    try { return JSON.parse(localStorage.getItem(key) || '[]'); } catch(e) { return []; }
  }
  function setList(key, ids) { localStorage.setItem(key, JSON.stringify(ids)); }
  function toggleList(key, id) {
    var list = getList(key);
    var idx = list.indexOf(id);
    if (idx === -1) list.push(id); else list.splice(idx, 1);
    setList(key, list);
    return idx === -1;
  }

  var currentData = null;
  var currentQuery = '';
  var currentSort = 'date-desc';
  var activeDbFilter = '';
  var showBookmarksOnly = false;
  var aiSearchIds = null;       // null = not in AI mode, [] = AI returned no results
  var aiSearchReason = '';
  var aiSearchLoading = false;

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

    html += '<div style="margin-bottom:16px"><a href="databases.html" style="font-size:0.78rem;color:var(--text-secondary);text-decoration:none">&larr; \u30c7\u30fc\u30bf\u30d9\u30fc\u30b9\u306b\u623b\u308b</a></div>';
    html += '<p style="font-size:0.84rem;color:var(--text-secondary);line-height:1.7;max-width:720px;margin-bottom:24px">' + escapeHtml(data.description) + '</p>';

    // Overview stats
    html += '<div class="db-overview" id="ar-stats"></div>';

    // Toolbar: search + AI button + bookmark toggle + sort
    html += '<div class="ar-toolbar">';
    html += '<div class="ar-search-wrap">';
    html += '<input type="text" class="ar-search" id="ar-search" placeholder="AI\u691c\u7d22: \u81ea\u7136\u8a00\u8a9e\u3067\u691c\u7d22\u3067\u304d\u307e\u3059\u3002Enter\u3067AI\u691c\u7d22\u3001\u5165\u529b\u4e2d\u306f\u30ad\u30fc\u30ef\u30fc\u30c9\u7d5e\u308a\u8fbc\u307f">';
    html += '<button class="ar-ai-search-btn" id="ar-ai-search-btn" title="AI\u691c\u7d22\u3092\u5b9f\u884c">AI</button>';
    html += '</div>';
    html += '<button class="ar-bookmark-toggle" id="ar-bookmark-toggle" title="\u30d6\u30c3\u30af\u30de\u30fc\u30af\u306e\u307f\u8868\u793a">\u2606 <span id="ar-bookmark-count">0</span></button>';
    html += '<select class="ar-sort" id="ar-sort">';
    html += '<option value="date-desc">\u65b0\u3057\u3044\u9806</option>';
    html += '<option value="date-asc">\u53e4\u3044\u9806</option>';
    html += '<option value="words-desc">\u6587\u5b57\u6570\u304c\u591a\u3044\u9806</option>';
    html += '<option value="title-asc">\u30bf\u30a4\u30c8\u30eb\u9806</option>';
    html += '</select>';
    html += '</div>';

    // AI search status
    html += '<div id="ar-ai-status" class="ar-ai-status"></div>';

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

  // --- AI Search ---
  function runAiSearch(query) {
    if (aiSearchLoading) return;
    if (!query || query.trim().length === 0) {
      clearAiSearch();
      return;
    }

    aiSearchLoading = true;
    var statusEl = document.getElementById('ar-ai-status');
    var btnEl = document.getElementById('ar-ai-search-btn');
    statusEl.innerHTML = '<div class="ar-ai-loading"><div class="loading-spinner loading-spinner-sm"></div> AI\u304c\u691c\u7d22\u4e2d...</div>';
    btnEl.classList.add('loading');

    // Build compact report catalog for the prompt
    var catalog = currentData.reports.map(function(r, i) {
      return '[' + i + '] id=' + r.id + ' | ' + r.title + ' | DB: ' + (r.databases || []).join(',') + ' | ' + (r.summary || '').substring(0, 200);
    }).join('\n');

    var prompt = '\u3042\u306a\u305f\u306f\u89e3\u6790\u30ec\u30dd\u30fc\u30c8\u306e\u691c\u7d22\u30a2\u30b7\u30b9\u30bf\u30f3\u30c8\u3067\u3059\u3002\u30e6\u30fc\u30b6\u30fc\u306e\u81ea\u7136\u8a00\u8a9e\u30af\u30a8\u30ea\u306b\u57fa\u3065\u3044\u3066\u3001\u95a2\u9023\u3059\u308b\u30ec\u30dd\u30fc\u30c8\u3092\u9078\u3093\u3067\u304f\u3060\u3055\u3044\u3002\n\n## \u30ec\u30dd\u30fc\u30c8\u4e00\u89a7\n' + catalog + '\n\n## \u30e6\u30fc\u30b6\u30fc\u306e\u691c\u7d22\u30af\u30a8\u30ea\n' + query.trim().slice(0, 500) + '\n\n## \u30bf\u30b9\u30af\n\u30af\u30a8\u30ea\u306b\u95a2\u9023\u3059\u308b\u30ec\u30dd\u30fc\u30c8\u306e\u30a4\u30f3\u30c7\u30c3\u30af\u30b9\u756a\u53f7\u3092\u3001\u95a2\u9023\u5ea6\u306e\u9ad8\u3044\u9806\u306bJSON\u914d\u5217\u3067\u8fd4\u3057\u3066\u304f\u3060\u3055\u3044\u3002\n\u95a2\u9023\u5ea6\u304c\u4f4e\u3044\u30ec\u30dd\u30fc\u30c8\u306f\u542b\u3081\u306a\u3044\u3067\u304f\u3060\u3055\u3044\u3002\n\u8a72\u5f53\u306a\u3057\u306e\u5834\u5408\u306f\u7a7a\u914d\u5217\u3092\u8fd4\u3057\u3066\u304f\u3060\u3055\u3044\u3002\n\n\u51fa\u529b\u5f62\u5f0f\uff08JSON\u306e\u307f\u3001\u4ed6\u306e\u30c6\u30ad\u30b9\u30c8\u4e0d\u8981\uff09:\n{"matches": [0, 3, 7], "reason": "\u691c\u7d22\u7d50\u679c\u306e\u7c21\u6f54\u306a\u8aac\u660e\uff08\u65e5\u672c\u8a9e\u30011-2\u6587\uff09"}';

    fetch(WORKER_BASE + '/api/anthropic', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-User-Id': currentUser.uid || 'anonymous'
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5-20251001',
        max_tokens: 1000,
        messages: [{ role: 'user', content: prompt }]
      })
    })
    .then(function(res) { return res.json(); })
    .then(function(data) {
      aiSearchLoading = false;
      btnEl.classList.remove('loading');
      if (data.error) {
        statusEl.innerHTML = '<div class="ar-ai-error">' + escapeHtml(data.error.message || data.error) + '</div>';
        return;
      }

      // Extract text from Anthropic response
      var answerText = '';
      if (data.content && data.content.length > 0) {
        answerText = data.content.map(function(b) { return b.text || ''; }).join('');
      }

      // Parse JSON response
      var parsed;
      try {
        var cleaned = answerText.replace(/^```(?:json)?\s*/, '').replace(/\s*```$/, '').trim();
        parsed = JSON.parse(cleaned);
      } catch(e) {
        parsed = { matches: [], reason: '\u89e3\u6790\u30a8\u30e9\u30fc' };
      }

      // Convert indices to report IDs
      aiSearchIds = (parsed.matches || [])
        .filter(function(idx) { return idx >= 0 && idx < currentData.reports.length; })
        .map(function(idx) { return currentData.reports[idx].id; });
      aiSearchReason = parsed.reason || '';

      var html = '<div class="ar-ai-result">';
      html += '<span class="ar-ai-result-label">AI\u691c\u7d22\u7d50\u679c: </span>';
      html += '<span class="ar-ai-result-text">' + escapeHtml(aiSearchReason) + ' (' + aiSearchIds.length + '\u4ef6)</span>';
      html += '<button class="ar-ai-clear" id="ar-ai-clear">\u00d7 \u30af\u30ea\u30a2</button>';
      html += '</div>';
      statusEl.innerHTML = html;
      document.getElementById('ar-ai-clear').addEventListener('click', function() {
        clearAiSearch();
        document.getElementById('ar-search').value = '';
        currentQuery = '';
      });
      applyFilters();
    })
    .catch(function(err) {
      aiSearchLoading = false;
      btnEl.classList.remove('loading');
      statusEl.innerHTML = '<div class="ar-ai-error">AI\u691c\u7d22\u306b\u5931\u6557\u3057\u307e\u3057\u305f: ' + escapeHtml(err.message) + '</div>';
    });
  }

  function clearAiSearch() {
    aiSearchIds = null;
    aiSearchReason = '';
    var statusEl = document.getElementById('ar-ai-status');
    if (statusEl) statusEl.innerHTML = '';
    applyFilters();
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

  function renderDbFilters(reports) {
    var dbMap = collectDatabases(reports);
    var entries = Object.keys(dbMap).sort(function(a, b) { return dbMap[b] - dbMap[a]; });
    var html = '<button class="ar-tag-btn' + (activeDbFilter === '' ? ' active' : '') + '" data-db="">\u3059\u3079\u3066</button>';
    entries.forEach(function(db) {
      html += '<button class="ar-tag-btn' + (activeDbFilter === db ? ' active' : '') + '" data-db="' + escapeHtml(db) + '">' + escapeHtml(db) + ' <span style="opacity:0.6">(' + dbMap[db] + ')</span></button>';
    });
    document.getElementById('ar-db-filters').innerHTML = html;
  }

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

  function updateBookmarkToggle() {
    var bookmarks = getList('ar_bookmarked');
    var toggleEl = document.getElementById('ar-bookmark-toggle');
    if (toggleEl) {
      toggleEl.classList.toggle('active', showBookmarksOnly);
      toggleEl.innerHTML = (showBookmarksOnly ? '\u2605' : '\u2606') + ' <span id="ar-bookmark-count">' + bookmarks.length + '</span>';
    }
  }

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
    var archived = getList('ar_archived');
    var deleted = getList('ar_deleted');
    var bookmarks = getList('ar_bookmarked');

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

    var visibleAll = activeReports.concat(archivedReports);
    renderStats(visibleAll);
    renderDbFilters(visibleAll);
    updateBookmarkToggle();

    // Filter active reports
    var q = aiSearchIds !== null ? '' : currentQuery.toLowerCase(); // skip keyword filter when AI search is active
    var filtered = activeReports.filter(function(r) {
      if (aiSearchIds !== null && aiSearchIds.indexOf(r.id) === -1) return false;
      if (aiSearchIds === null && !matchesQuery(r, q)) return false;
      if (!matchesDbFilter(r)) return false;
      if (showBookmarksOnly && bookmarks.indexOf(r.id) === -1) return false;
      return true;
    });

    // When AI search is active, preserve AI ranking order
    if (aiSearchIds !== null && aiSearchIds.length > 0) {
      var idOrder = {};
      aiSearchIds.forEach(function(id, i) { idOrder[id] = i; });
      filtered.sort(function(a, b) {
        var oa = idOrder[a.id] !== undefined ? idOrder[a.id] : 9999;
        var ob = idOrder[b.id] !== undefined ? idOrder[b.id] : 9999;
        return oa - ob;
      });
    } else if (aiSearchIds === null) {
      filtered = sortReports(filtered);
    }

    var cardsEl = document.getElementById('ar-cards');
    if (filtered.length === 0 && (activeReports.length > 0 || aiSearchIds !== null)) {
      cardsEl.innerHTML = '<div class="ar-no-results">' +
        (aiSearchIds !== null ? 'AI\u691c\u7d22\u306b\u8a72\u5f53\u3059\u308b\u30ec\u30dd\u30fc\u30c8\u304c\u3042\u308a\u307e\u305b\u3093' : '\u8a72\u5f53\u3059\u308b\u30ec\u30dd\u30fc\u30c8\u304c\u3042\u308a\u307e\u305b\u3093') +
        '</div>';
    } else {
      cardsEl.innerHTML = renderCards(filtered, 'active', bookmarks);
    }

    // Archived section (hide during AI search)
    var archivedEl = document.getElementById('ar-archived-section');
    if (archivedReports.length > 0 && aiSearchIds === null) {
      var filteredArchived = archivedReports.filter(function(r) {
        if (!matchesQuery(r, q)) return false;
        if (!matchesDbFilter(r)) return false;
        if (showBookmarksOnly && bookmarks.indexOf(r.id) === -1) return false;
        return true;
      });
      filteredArchived = sortReports(filteredArchived);
      archivedEl.innerHTML =
        '<div class="ar-section-header"><h3 class="ar-section-title">\u30a2\u30fc\u30ab\u30a4\u30d6 <span class="ar-section-count">(' + archivedReports.length + '\u4ef6)</span></h3></div>' +
        renderCards(filteredArchived, 'archived', bookmarks);
    } else {
      archivedEl.innerHTML = '';
    }

    // Deleted section
    var deletedEl = document.getElementById('ar-deleted-section');
    if (deletedReports.length > 0 && aiSearchIds === null) {
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

    bindFulltextToggles();
  }

  // --- Render cards ---
  function renderCards(reports, mode, bookmarks) {
    var html = '';
    reports.forEach(function(r) {
      var isBookmarked = bookmarks.indexOf(r.id) !== -1;
      var dbBadges = (r.databases || []).map(function(d) {
        return '<span class="report-archive-badge-db">' + escapeHtml(d) + '</span>';
      }).join('');
      var tagBadges = (r.tags || []).map(function(t) {
        return '<span class="report-archive-badge-tag">' + escapeHtml(t) + '</span>';
      }).join('');

      var archivedClass = mode === 'archived' ? ' is-archived' : '';
      html += '<div class="report-archive-card' + archivedClass + '">';

      html += '<div class="report-archive-header">';
      html += '<div class="report-archive-title">' + escapeHtml(r.title) + '</div>';
      html += '<div style="display:flex;align-items:center;gap:8px;flex-shrink:0">';
      html += '<button class="ar-btn-bookmark' + (isBookmarked ? ' active' : '') + '" data-id="' + escapeHtml(r.id) + '" title="' + (isBookmarked ? '\u30d6\u30c3\u30af\u30de\u30fc\u30af\u89e3\u9664' : '\u30d6\u30c3\u30af\u30de\u30fc\u30af') + '">' + (isBookmarked ? '\u2605' : '\u2606') + '</button>';
      html += '<span class="report-archive-date">' + escapeHtml(r.date) + '</span>';
      html += '</div>';
      html += '</div>';

      if (r.subtitle) {
        html += '<div class="report-archive-subtitle">' + escapeHtml(r.subtitle) + '</div>';
      }
      if (dbBadges || tagBadges) {
        html += '<div class="report-archive-badges">' + dbBadges + tagBadges + '</div>';
      }
      if (r.summary) {
        html += '<div class="report-archive-preview">' + escapeHtml(r.summary) + '</div>';
      }
      if (r.key_findings && r.key_findings.length > 0) {
        html += '<div class="report-archive-findings"><div class="report-obs-label">\u4e3b\u8981\u306a\u767a\u898b</div>';
        r.key_findings.forEach(function(f) {
          html += '<div class="report-archive-finding">- ' + escapeHtml(f) + '</div>';
        });
        html += '</div>';
      }
      html += '<div class="report-archive-meta">';
      if (r.word_count) html += '<span>' + r.word_count.toLocaleString() + '\u6587\u5b57</span>';
      if (r.sections) html += '<span>' + r.sections + '\u7ae0</span>';
      html += '</div>';

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
    var searchEl = document.getElementById('ar-search');
    var debounceTimer;

    // Typing = keyword filter (instant)
    searchEl.addEventListener('input', function() {
      clearTimeout(debounceTimer);
      var val = this.value;
      // Clear AI results when user edits the query
      if (aiSearchIds !== null) {
        clearAiSearch();
      }
      debounceTimer = setTimeout(function() {
        currentQuery = val;
        applyFilters();
      }, 200);
    });

    // Enter = AI search
    searchEl.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        runAiSearch(this.value);
      }
    });

    // AI search button
    document.getElementById('ar-ai-search-btn').addEventListener('click', function() {
      runAiSearch(searchEl.value);
    });

    // Sort
    document.getElementById('ar-sort').addEventListener('change', function() {
      currentSort = this.value;
      applyFilters();
    });

    // Bookmark toggle
    document.getElementById('ar-bookmark-toggle').addEventListener('click', function() {
      showBookmarksOnly = !showBookmarksOnly;
      applyFilters();
    });

    // DB filter buttons
    document.getElementById('ar-db-filters').addEventListener('click', function(e) {
      var btn = e.target.closest('.ar-tag-btn');
      if (!btn) return;
      activeDbFilter = btn.dataset.db || '';
      applyFilters();
    });

    // Action buttons
    container.addEventListener('click', function(e) {
      var btn = e.target.closest('[data-id]');
      if (!btn) return;
      if (btn.tagName === 'A') return;
      var id = btn.dataset.id;

      if (btn.classList.contains('ar-btn-bookmark')) {
        toggleList('ar_bookmarked', id);
        applyFilters();
      } else if (btn.classList.contains('ar-btn-archive')) {
        var list = getList('ar_archived');
        if (list.indexOf(id) === -1) list.push(id);
        setList('ar_archived', list);
        applyFilters();
      } else if (btn.classList.contains('ar-btn-unarchive')) {
        setList('ar_archived', getList('ar_archived').filter(function(x) { return x !== id; }));
        applyFilters();
      } else if (btn.classList.contains('ar-btn-delete')) {
        if (confirm('\u300c' + id + '\u300d\u3092\u524a\u9664\u3057\u307e\u3059\u304b\uff1f')) {
          var dl = getList('ar_deleted');
          if (dl.indexOf(id) === -1) dl.push(id);
          setList('ar_deleted', dl);
          applyFilters();
        }
      } else if (btn.classList.contains('ar-btn-restore')) {
        setList('ar_deleted', getList('ar_deleted').filter(function(x) { return x !== id; }));
        applyFilters();
      }
    });
  }
});
