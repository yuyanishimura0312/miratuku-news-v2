'use strict';
// Initialize nav and auth
initNav('home');
initAuthGuard(function(user) {
  loadHomeData();
});

// ==============================================================
// HOME PAGE — Data Loading
// ==============================================================

// Store reports data globally for interactive switching
var _insightReportsData = null;
var _insightHeroIndex = 0;

async function loadHomeData() {
  try {
    document.getElementById('headerDate').textContent = formatDateFull(new Date());
    var results = await Promise.all([
      fetchJSON('daily_report.json'),
      fetchJSON('latest.json'),
      fetchJSON('ai_analysis.json'),
      fetchJSON('daily_papers.json'),
      fetchJSON('alerts.json'),
      fetchJSON('media_sources.json'),
      fetchJSON('insight_reports.json')
    ]);
    var dailyReport = results[0];
    var latest = results[1];
    var aiAnalysis = results[2];
    var papers = results[3];
    var alerts = results[4];
    var mediaSources = results[5];
    var insightReports = results[6];

    try {
      renderAlerts(alerts);
      renderHomeDashboard(dailyReport, latest, aiAnalysis, papers, insightReports);
      updateBookmarkUI();

      // Populate foresight context for AI chat quality
      if (aiAnalysis && aiAnalysis.cla) {
        window.__claContext = Object.entries(aiAnalysis.cla)
          .map(function(entry) { return '[' + entry[0] + '] ' + (entry[1].litany || '') + ' ' + (entry[1].key_tension || ''); })
          .join('\n').slice(0, 3000);
      }
      if (aiAnalysis && aiAnalysis.weak_signals) {
        window.__signalsContext = aiAnalysis.weak_signals.slice(0, 20)
          .map(function(s) { return (s.signal || '') + ': ' + (s.description || ''); })
          .join('\n').slice(0, 2000);
      }
      if (latest && latest.pestle) {
        var topNews = [];
        Object.entries(latest.pestle).forEach(function(entry) {
          (entry[1].articles || []).slice(0, 3).forEach(function(a) { topNews.push('[' + entry[0] + '] ' + (a.title || '')); });
        });
        window.__newsContext = topNews.join('\n').slice(0, 2000);
      }

      // Mobile nav scroll hint (first visit only)
      if (!localStorage.getItem('nav_scroll_seen')) {
        var nav = document.querySelector('.site-nav');
        if (nav && nav.scrollWidth > nav.clientWidth) {
          nav.classList.add('scroll-hint');
          setTimeout(function() { nav.classList.remove('scroll-hint'); localStorage.setItem('nav_scroll_seen', '1'); }, 1500);
        }
      }
    } catch (renderErr) {
      console.error('Render error:', renderErr);
      document.getElementById('homeDashboard').innerHTML = '<div class="error-message">データの表示中にエラーが発生しました。ページを再読み込みしてください。</div>';
    }
  } catch (loadErr) {
    console.error('Data load error:', loadErr);
    document.getElementById('homeDashboard').innerHTML = '<div class="error-message">データの読み込みに失敗しました。ページを再読み込みしてください。</div>';
  }
}

// ==============================================================
// RENDER: ALERTS
// ==============================================================
function renderAlerts(data) {
  if (!data || !data.alerts || !data.alerts.length) return;
  var bar = document.getElementById('alertsBar');
  var ticker = document.getElementById('alertTicker');
  bar.style.display = '';
  var typeMap = { emergence: '新出現', surge: '急増', crossover: '横断', EMERGENCE: '新出現', SURGE: '急増', CROSSOVER: '横断' };
  var items = data.alerts.slice(0, 10);
  var html = items.map(function(a) {
    var typeLabel = typeMap[a.type] || a.type || '';
    var title = a.alert_title || a.alert_title_en || a.description || a.topic || '';
    return '<span class="alert-item"><span class="alert-type-badge">' + escapeHtml(typeLabel) + '</span>' + escapeHtml(title) + '</span>';
  }).join('');
  ticker.innerHTML = html + html;
}

// ==============================================================
// RENDER: HOME DASHBOARD
// ==============================================================
function renderHomeDashboard(dailyReport, latest, aiData, papers, insightReports) {
  var container = document.getElementById('homeDashboard');
  var dateStr = dailyReport?.generated_at ? dailyReport.generated_at.split('T')[0] : new Date().toISOString().split('T')[0];

  var jpReport = dailyReport?.japan;
  var glReport = dailyReport?.global;
  var signals = (aiData?.weak_signals || []).slice(0, 10);

  // Collect papers
  var allPapers = [];
  var fields = papers?.fields || papers?.by_field || {};
  Object.entries(fields).forEach(function(entry) {
    var field = entry[0];
    var list = entry[1];
    var arr = Array.isArray(list) ? list : (list?.papers || []);
    arr.forEach(function(p) { p._field = field; allPapers.push(p); });
  });
  allPapers.sort(function(a, b) { return new Date(b.published_date || 0) - new Date(a.published_date || 0); });
  var topPapers = allPapers.slice(0, 10);

  // Build the full-page 2-column layout: main (left) + signals sidebar (right)
  var html = '<div class="home-news-layout">';

  // --- Left column: main content ---
  html += '<div class="home-news-main">';

  // 1. Insight Reports Hero (main reports at top)
  if (insightReports?.reports?.length > 0) {
    html += renderInsightReportsHero(insightReports);
  }

  // 2. PESTLE grid (Insight News)
  html += '<div><h2 class="section-title">Insight News</h2>' +
    '<div id="homePestleGrid"></div></div>';

  // 3. Papers
  if (topPapers.length > 0) {
    html += '<div><h2 class="section-title">学術研究 — 最新の研究成果</h2>';
    topPapers.slice(0, 3).forEach(function(p) { html += renderHomePaperCard(p); });
    if (topPapers.length > 3) {
      html += '<details><summary class="fulltext-toggle">残り ' + (topPapers.length - 3) + ' 件を表示</summary><div class="fulltext-body">';
      topPapers.slice(3).forEach(function(p) { html += renderHomePaperCard(p); });
      html += '</div></details>';
    }
    html += '<a class="more-link" href="papers.html">全分野を見る &rarr;</a></div>';
  }

  // 4. Future Insight box
  html += '<div class="insight-box">' +
    '<h2 class="section-title">未来洞察</h2>' +
    '<p class="insight-desc">あなたの問題意識を記述してください。蓄積されたデータから未来洞察の視点で回答します。</p>' +
    '<form onsubmit="submitHomeForesight(event)" class="insight-form">' +
      '<input type="text" id="homeForesightInput" placeholder="例: AI規制と雇用市場の今後3年の見通し..." class="insight-input">' +
      '<button type="submit" class="btn-primary">問いかける</button>' +
    '</form>' +
    '<div id="homeForesightResult" class="insight-result"></div>' +
  '</div>';

  // 5. Monthly Analysis Report (moved to bottom)
  html += '<div><h2 class="section-title">月次分析レポート <span class="section-date">' + dateStr + '</span></h2>';
  if (jpReport) html += renderDailyReportCard('日本メディアの視点', jpReport);
  if (glReport) html += renderDailyReportCard('海外メディアの視点', glReport);
  html += '</div>';

  html += '</div>'; // end home-news-main

  // --- Right column: signals sidebar (sticky, always visible) ---
  html += '<div class="home-news-sidebar">' +
    '<div class="home-sidebar-card">' +
      '<h3 class="home-sidebar-title">新着シグナル</h3>' +
      '<div id="homeSidebarSignals">';
  if (signals.length > 0) {
    // Store signals globally for popup access
    window._sidebarSignals = signals;
    var stMap = { 'weak_signal': { l: 'WS', c: '#C4756A' }, 'emerging_trend': { l: 'ET', c: '#B8605A' }, 'wild_card': { l: 'WC', c: '#A84A48' }, 'counter_trend': { l: 'CT', c: '#8E3A3A' }, 'paradigm_shift': { l: 'PS', c: '#6E2C2C' } };
    signals.forEach(function(ws, idx) {
      var impactClass = (ws.potential_impact || '').toLowerCase() === 'high' ? 'ws-badge-high' :
                        (ws.potential_impact || '').toLowerCase() === 'medium' ? 'ws-badge-medium' : 'ws-badge-low';
      var st = stMap[ws.signal_type] || stMap['weak_signal'];
      html += '<div class="home-signal-item" style="cursor:pointer" onclick="openSidebarSignal(' + idx + ')" role="button" tabindex="0" aria-label="シグナル詳細を表示: ' + escapeAttr(ws.signal || '') + '">' +
        '<div class="home-signal-badges">' +
          '<span class="ws-badge" style="background:' + st.c + '20;color:' + st.c + ';border:1px solid ' + st.c + '40;font-size:10px">' + st.l + '</span>' +
          '<span class="ws-badge ' + impactClass + '">' + escapeHtml(ws.potential_impact || '') + '</span>' +
          (ws.three_horizons ? '<span class="ws-badge" style="background:#C4756A20;color:#C4756A;font-size:10px">' + escapeHtml(ws.three_horizons) + '</span>' : '') +
        '</div>' +
        '<div class="home-signal-title">' + escapeHtml(ws.signal || '') + '</div>' +
        '<div class="home-signal-desc">' + escapeHtml(ws.description || '') + '</div>' +
      '</div>';
    });
  } else {
    html += '<p class="fs-meta" style="color:var(--text-muted);line-height:1.6">現在シグナルはありません</p>';
  }
  html += '</div>' +
          '<a class="more-link fs-meta" href="signals.html" style="margin-top:10px;display:inline-block">全シグナルを見る &rarr;</a>' +
        '</div>' +
      '</div>'; // end home-news-sidebar

  html += '</div>'; // end home-news-layout
  container.innerHTML = html;

  // Render PESTLE grid
  var homeGrid = document.getElementById('homePestleGrid');
  if (homeGrid && latest) renderPESTLEInto(homeGrid, latest, aiData);
}

// ==============================================================
// RENDER: DAILY REPORT CARD
// ==============================================================
function renderDailyReportCard(label, report) {
  var preview = (report.report_text || '').substring(0, 300);
  var obs = report.key_observations || report.observations || [];
  var declining = report.myth_in_transition?.declining || report.declining_myths || [];
  var emerging = report.myth_in_transition?.emerging || report.emerging_myths || [];

  var html = '<details open class="report-card">' +
    '<summary class="report-summary">' +
      '<span class="report-chevron">&#9654;</span>' +
      '<span class="report-label">' + escapeHtml(label) + '</span>' +
      '<span class="report-count">' + (obs.length || 0) + '件の観測</span>' +
    '</summary><div class="report-body">' +
    '<div class="report-preview">' + escapeHtml(preview) + '...</div>';

  if ((Array.isArray(declining) && declining.length) || (Array.isArray(emerging) && emerging.length)) {
    html += '<div class="myth-grid">';
    if (Array.isArray(declining) && declining.length) {
      html += '<div class="myth-box"><div class="myth-label myth-label-decline">衰退する神話</div>';
      declining.slice(0, 3).forEach(function(m) { html += '<div class="myth-item">- ' + escapeHtml(String(m)) + '</div>'; });
      html += '</div>';
    }
    if (Array.isArray(emerging) && emerging.length) {
      html += '<div class="myth-box"><div class="myth-label myth-label-emerge">浮上する神話</div>';
      emerging.slice(0, 3).forEach(function(m) { html += '<div class="myth-item">- ' + escapeHtml(String(m)) + '</div>'; });
      html += '</div>';
    }
    html += '</div>';
  }

  html += '<details><summary class="fulltext-toggle">全文を読む</summary>' +
    '<div class="fulltext-body md-body">' + renderMarkdown(report.report_text || '') + '</div></details>';
  html += '</div></details>';
  return html;
}

// ==============================================================
// RENDER: INSIGHT REPORTS HERO + CAROUSEL
// ==============================================================
function renderInsightReportsHero(data) {
  if (!data?.reports?.length) return '';
  _insightReportsData = data;
  _insightHeroIndex = 0;
  var reports = data.reports;
  var hero = reports[0];
  var dateStr = data.date || '';

  var html = '<div class="ir-section">';
  html += '<h2 class="section-title">Insight Reports <span class="section-date">' + escapeHtml(dateStr) + '</span></h2>';

  // Hero layout: hero card + side panel
  html += '<div class="ir-hero-layout">';
  html += '<div id="irHeroCard">' + renderIRHeroCard(hero, 0) + '</div>';

  // Side panel with all report titles
  html += '<div class="ir-side-panel" id="irSidePanel">';
  html += '<div class="ir-side-panel-title">全レポート</div>';
  reports.forEach(function(r, i) {
    var catInfo = PESTLE_CATS[r.article?.pestle_category] || { labelJa: '', color: 'var(--accent)' };
    var mythLabel = r.myth_relation === 'strengthens' ? '強化' : '変革';
    var mythClass = r.myth_relation === 'strengthens' ? 'ir-myth-badge-strengthens' : 'ir-myth-badge-transforms';
    html += '<div class="ir-side-item' + (i === 0 ? ' active' : '') + '" onclick="switchHeroReport(' + i + ')" data-ir-index="' + i + '">' +
      '<div class="ir-side-dot" style="background:' + catInfo.color + '" title="' + escapeHtml(catInfo.labelJa || '') + '" aria-label="' + escapeHtml(catInfo.labelJa || '') + '"></div>' +
      '<div class="ir-side-text">' +
        '<div class="ir-side-title">' + escapeHtml(r.report_title || '') + '</div>' +
        '<span class="ir-side-myth ' + mythClass + '">' + mythLabel + '</span>' +
      '</div></div>';
  });
  html += '</div>'; // side panel
  html += '</div>'; // hero layout

  // Carousel with remaining reports
  if (reports.length > 1) {
    html += '<div class="ir-carousel-wrap">';
    html += '<button class="ir-carousel-btn ir-carousel-btn-left" onclick="scrollInsightCarousel(-1)" aria-label="前へ">&#9664;</button>';
    html += '<div class="ir-carousel" id="irCarousel">';
    reports.slice(1).forEach(function(r, idx) {
      var realIdx = idx + 1;
      var catInfo = PESTLE_CATS[r.article?.pestle_category] || { labelJa: '', color: 'var(--accent)' };
      var mythLabel = r.myth_relation === 'strengthens' ? '強化' : '変革';
      var mythClass = r.myth_relation === 'strengthens' ? 'ir-myth-badge-strengthens' : 'ir-myth-badge-transforms';
      var preview = r.summary ? r.summary.substring(0, 120) : stripMarkdown(r.report_text || '').substring(0, 120);
      html += '<div class="ir-carousel-card" onclick="openInsightReport(' + realIdx + ')">' +
        '<div class="ir-carousel-accent" style="background:' + catInfo.color + '"></div>' +
        '<div class="ir-carousel-body">' +
          '<div class="ir-carousel-header">' +
            '<div class="ir-carousel-dot" style="background:' + catInfo.color + '" title="' + escapeHtml(catInfo.labelJa || '') + '"></div>' +
            '<span class="ir-carousel-cat">' + escapeHtml(catInfo.labelJa || r.article?.pestle_category || '') + '</span>' +
          '</div>' +
          '<div class="ir-carousel-title">' + escapeHtml(r.report_title || '') + '</div>' +
          '<span class="ir-carousel-myth ' + mythClass + '">' + mythLabel + '</span>' +
          '<div class="ir-carousel-preview">' + escapeHtml(preview) + '</div>' +
        '</div></div>';
    });
    html += '</div>'; // carousel
    html += '<button class="ir-carousel-btn ir-carousel-btn-right" onclick="scrollInsightCarousel(1)" aria-label="次へ">&#9654;</button>';
    html += '</div>'; // carousel wrap
  }

  html += '</div>'; // ir-section
  return html;
}

function renderIRHeroCard(report, index) {
  var catInfo = PESTLE_CATS[report.article?.pestle_category] || { labelJa: '', color: 'var(--accent)' };
  var mythLabel = report.myth_relation === 'strengthens' ? '神話を強化' : '神話を変革';
  var mythClass = report.myth_relation === 'strengthens' ? 'ir-myth-badge-strengthens' : 'ir-myth-badge-transforms';
  var preview = stripMarkdown(report.report_text || '').substring(0, 300);

  var summaryHtml = report.summary
    ? '<div class="ir-summary">' + escapeHtml(report.summary) + '</div>'
    : '<div class="ir-hero-preview">' + escapeHtml(preview) + '</div>';

  return '<div class="ir-hero-card" onclick="openInsightReport(' + index + ')">' +
    '<div class="ir-hero-accent" style="background:' + catInfo.color + '"></div>' +
    '<div class="ir-hero-body">' +
      '<span class="ir-hero-cat-badge" style="background:' + catInfo.color + '">' + escapeHtml(catInfo.labelJa || report.article?.pestle_category || '') + '</span>' +
      '<div class="ir-hero-title">' + escapeHtml(report.report_title || '') + '</div>' +
      '<span class="ir-myth-badge ' + mythClass + '">' + mythLabel + '</span>' +
      (report.related_myth ? '<div class="ir-myth-text">' + escapeHtml(report.related_myth) + '</div>' : '') +
      summaryHtml +
      '<span class="ir-hero-read-more" onclick="event.stopPropagation();openInsightReport(' + index + ')">続きを読む &rarr;</span>' +
      '<div class="ir-hero-source">' +
        escapeHtml(report.article?.source || '') + ' | ' + escapeHtml(report.article?.published_date || '') +
        (report.article?.url ? ' | <a href="' + escapeAttr(safeUrl(report.article.url)) + '" target="_blank" onclick="event.stopPropagation()">元記事</a>' : '') +
      '</div>' +
    '</div></div>';
}

window.switchHeroReport = function(index) {
  if (!_insightReportsData?.reports?.[index]) return;
  _insightHeroIndex = index;
  var heroContainer = document.getElementById('irHeroCard');
  if (heroContainer) {
    heroContainer.innerHTML = renderIRHeroCard(_insightReportsData.reports[index], index);
  }
  // Update active state in side panel
  var items = document.querySelectorAll('#irSidePanel .ir-side-item');
  items.forEach(function(item) {
    var itemIdx = parseInt(item.getAttribute('data-ir-index'), 10);
    if (itemIdx === index) {
      item.classList.add('active');
    } else {
      item.classList.remove('active');
    }
  });
};

window.openInsightReport = function(reportIndex) {
  if (!_insightReportsData?.reports?.[reportIndex]) return;
  var r = _insightReportsData.reports[reportIndex];
  var catInfo = PESTLE_CATS[r.article?.pestle_category] || { labelJa: '', color: 'var(--accent)' };
  var mythLabel = r.myth_relation === 'strengthens' ? '神話を強化' : '神話を変革';
  var mythClass = r.myth_relation === 'strengthens' ? 'ir-myth-badge-strengthens' : 'ir-myth-badge-transforms';

  // Estimate reading time (Japanese: ~500 chars/min)
  var totalChars = (r.report_text || '').length + (r.summary || '').length + (r.historical_context || '').length + (r.future_signals || '').length + (r.watch_points || '').length;
  var readingMin = Math.max(1, Math.round(totalChars / 500));

  var content = document.getElementById('articleModalContent');
  var modalHtml = '<div class="modal-title">' + escapeHtml(r.report_title || '') + '</div>' +
    '<div class="modal-meta" style="margin-bottom:12px;display:flex;align-items:center;gap:8px;flex-wrap:wrap">' +
      '<span class="ir-hero-cat-badge fs-tiny" style="background:' + catInfo.color + ';">' + escapeHtml(catInfo.labelJa || '') + '</span> ' +
      '<span class="ir-myth-badge ' + mythClass + '">' + mythLabel + '</span>' +
      '<span class="fs-caption" style="color:var(--text-muted);margin-left:auto">' + readingMin + '分で読了</span>' +
    '</div>';

  if (r.related_myth) {
    modalHtml += '<div class="fs-body-lg" style="font-style:italic;color:var(--text-secondary);margin-bottom:14px;">' + escapeHtml(r.related_myth) + '</div>';
  }

  // Summary lead text
  if (r.summary) {
    modalHtml += '<div class="ir-summary">' + escapeHtml(r.summary) + '</div>';
  }

  // Source article link
  if (r.article) {
    modalHtml += '<div class="fs-meta" style="color:var(--text-muted);margin-bottom:16px;padding:10px 14px;background:var(--surface);border-radius:var(--radius-xs)">' +
      '元記事: ' + escapeHtml(r.article.title_ja || r.article.title || '') +
      ' (' + escapeHtml(r.article.source || '') + ', ' + escapeHtml(r.article.published_date || '') + ')' +
      (r.article.url ? ' <a href="' + escapeAttr(safeUrl(r.article.url)) + '" target="_blank">記事を読む &rarr;</a>' : '') +
    '</div>';
  }

  // Historical context (timeline visualization, falls back to markdown)
  if (r.timeline && r.timeline.length > 0) {
    modalHtml += '<div class="ir-modal-section open">' +
      '<div class="ir-modal-section-header" onclick="this.parentElement.classList.toggle(\'open\')">歴史的経緯<span class="ir-modal-section-chevron">&#9654;</span></div>' +
      '<div class="ir-modal-section-body">';
    modalHtml += '<div class="ir-timeline">';
    r.timeline.forEach(function(t) {
      modalHtml += '<div class="ir-timeline-entry">' +
        '<div class="ir-timeline-year">' + escapeHtml(t.year || '') + '</div>' +
        '<div class="ir-timeline-event">' + escapeHtml(t.event || '') + '</div>' +
        (t.significance ? '<div class="ir-timeline-sig">' + escapeHtml(t.significance) + '</div>' : '') +
      '</div>';
    });
    modalHtml += '</div></div></div>';
  } else if (r.historical_context) {
    modalHtml += '<div class="ir-modal-section open">' +
      '<div class="ir-modal-section-header" onclick="this.parentElement.classList.toggle(\'open\')">歴史的経緯<span class="ir-modal-section-chevron">&#9654;</span></div>' +
      '<div class="ir-modal-section-body md-body">' + renderMarkdown(r.historical_context) + '</div>' +
    '</div>';
  }

  // Future signals
  if (r.future_signals) {
    var fsLabel = r.future_signals_title ? escapeHtml(r.future_signals_title) : '未来へのシグナル';
    modalHtml += '<div class="ir-modal-section open">' +
      '<div class="ir-modal-section-header" onclick="this.parentElement.classList.toggle(\'open\')">' + fsLabel + '<span class="ir-modal-section-chevron">&#9654;</span></div>' +
      '<div class="ir-modal-section-body md-body">' + renderMarkdown(r.future_signals) + '</div>' +
    '</div>';
  }

  // Watch points
  if (r.watch_points) {
    var wpLabel = r.watch_points_title ? escapeHtml(r.watch_points_title) : 'ウォッチポイント';
    modalHtml += '<div class="ir-modal-section open">' +
      '<div class="ir-modal-section-header" onclick="this.parentElement.classList.toggle(\'open\')">' + wpLabel + '<span class="ir-modal-section-chevron">&#9654;</span></div>' +
      '<div class="ir-modal-section-body md-body">' + renderMarkdown(r.watch_points) + '</div>' +
    '</div>';
  }

  // Related research
  if (r.related_research) {
    if (Array.isArray(r.related_research)) {
      modalHtml += '<div class="ir-modal-section open">' +
        '<div class="ir-modal-section-header" onclick="this.parentElement.classList.toggle(\'open\')">関連学術成果<span class="ir-modal-section-chevron">&#9654;</span></div>' +
        '<div class="ir-modal-section-body">' +
        '<div class="ir-related-grid">';
      r.related_research.forEach(function(item) {
        modalHtml += '<div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-xs);padding:14px">' +
          '<div class="fs-body" style="line-height:1.7;color:var(--text);margin-bottom:10px">' + escapeHtml(item.comment || item.summary || '') + '</div>' +
          '<div class="fs-meta" style="color:var(--text-muted);border-top:1px solid var(--border-light);padding-top:8px">' +
            '<span style="font-weight:600">' + escapeHtml(item.title || '') + '</span>' +
            (item.author ? ' — ' + escapeHtml(item.author) : '') +
          '</div>' +
        '</div>';
      });
      modalHtml += '</div></div></div>';
    } else {
      modalHtml += '<div class="ir-modal-section open">' +
        '<div class="ir-modal-section-header" onclick="this.parentElement.classList.toggle(\'open\')">関連学術成果<span class="ir-modal-section-chevron">&#9654;</span></div>' +
        '<div class="ir-modal-section-body md-body">' + renderMarkdown(r.related_research) + '</div>' +
      '</div>';
    }
  }

  // Full report text
  modalHtml += '<div class="ir-modal-section open">' +
    '<div class="ir-modal-section-header" onclick="this.parentElement.classList.toggle(\'open\')">全文レポート<span class="ir-modal-section-chevron">&#9654;</span></div>' +
    '<div class="ir-modal-section-body md-body">' + renderMarkdown(r.report_text || '') + '</div>' +
  '</div>';

  content.innerHTML = modalHtml;
  var wasVisible = document.getElementById('articleModal').classList.contains('visible');
  window._modalReturnFocus = document.activeElement;
  document.getElementById('articleModal').classList.add('visible');
  document.body.style.overflow = 'hidden';
  if (!wasVisible) history.pushState({ modal: true }, '', location.href);

  // Reading progress bar
  var modalBox = document.getElementById('modalBox');
  var progressFill = document.getElementById('modalProgressFill');
  if (modalBox && progressFill) {
    if (window._modalScrollHandler) modalBox.removeEventListener('scroll', window._modalScrollHandler);
    window._modalScrollHandler = function() {
      var scrollTop = modalBox.scrollTop;
      var scrollHeight = modalBox.scrollHeight - modalBox.clientHeight;
      var pct = scrollHeight > 0 ? Math.min(100, (scrollTop / scrollHeight) * 100) : 0;
      progressFill.style.width = pct + '%';
    };
    modalBox.addEventListener('scroll', window._modalScrollHandler);
    progressFill.style.width = '0%';
  }

  setTimeout(function() { var btn = document.querySelector('#articleModal .modal-close'); if (btn) btn.focus(); }, 100);
};

window.scrollInsightCarousel = function(direction) {
  var carousel = document.getElementById('irCarousel');
  if (carousel) {
    carousel.scrollBy({ left: direction * 320, behavior: 'smooth' });
  }
};

// ==============================================================
// RENDER: HOME PAPER CARD
// ==============================================================
function renderHomePaperCard(p) {
  var fieldColors = { '自然科学': 'var(--T)', '工学': 'var(--L)', '社会科学': 'var(--S)', '人文学': 'var(--E)', '芸術': 'var(--P)' };
  var color = fieldColors[p._field] || 'var(--accent)';
  return '<div class="home-paper-card">' +
    '<div class="home-paper-meta">' +
      '<span class="home-paper-field-badge" style="color:' + color + ';background:' + color + '15">' + escapeHtml(p._field || '') + '</span>' +
      '<span class="home-paper-source">' + escapeHtml(p.source_name || '') + '</span>' +
      (p.novelty_score ? '<span class="home-paper-novelty">新規性: ' + p.novelty_score + '</span>' : '') +
    '</div>' +
    '<div class="home-paper-title">' + escapeHtml(p.title_ja || p.title || '') + '</div>' +
    (p.title_ja && p.title ? '<div class="home-paper-sub">' + escapeHtml(p.title) + '</div>' : '') +
    (p.authors ? '<div class="home-paper-sub">' + escapeHtml(p.authors) + '</div>' : '') +
  '</div>';
}

// ==============================================================
// PESTLE GRID RENDERER
// ==============================================================
function renderPESTLEInto(targetEl, data, aiData) {
  if (!data?.pestle) { targetEl.innerHTML = '<p class="text-muted">ニュースデータを取得できませんでした。</p>'; return; }
  var pestle = data.pestle;
  var translations = aiData?.translations || {};
  var catKeys = Object.keys(PESTLE_CATS);
  var gridHtml = '<div class="pestle-grid">';

  catKeys.forEach(function(catKey) {
    var catData = pestle[catKey];
    if (!catData) return;
    var catInfo = PESTLE_CATS[catKey];
    var articles = (catData.articles || []).slice();
    articles.sort(function(a, b) { return new Date(b.published_date || 0) - new Date(a.published_date || 0); });
    var allArticles = articles.slice();
    articles = currentRegion === 'japan' ? articles.filter(function(a) { return isJaSource(a); }) : articles.filter(function(a) { return !isJaSource(a); });
    var display = articles.slice(0, 5);
    var catTrans = translations[catKey] || [];

    gridHtml += '<div class="pestle-card"><div class="pestle-card-top" style="background:' + catInfo.color + '"></div>' +
      '<div class="pestle-card-header"><span class="pestle-cat-name" style="color:' + catInfo.color + '">' + catInfo.labelJa + '</span>' +
      '<span class="pestle-cat-count">' + articles.length + '件</span></div><div class="pestle-articles">';

    var rawArticles = catData.articles || [];
    if (display.length === 0) {
      gridHtml += '<div class="pestle-no-articles">記事がありません</div>';
    } else {
      display.forEach(function(a, displayIdx) {
        var origIdx = rawArticles.indexOf(a);
        var tr = catTrans.find(function(t) { return t.index === origIdx; });
        var ja = tr?.title_translated || '';
        var bmId = 'news-' + catKey + '-' + origIdx;
        var isBm = bookmarks.some(function(b) { return b.id === bmId; });
        gridHtml += '<div class="pestle-article"><div class="pestle-article-row">' +
          '<div class="pestle-article-content" onclick="openArticleModal(\'' + escapeAttr(catKey) + '\',' + origIdx + ')">' +
          '<div class="pestle-article-meta"><span class="pestle-article-source">' + escapeHtml(a.source || '') + '</span>' +
          '<span class="pestle-article-time">' + escapeHtml(a.published_date || '') + '</span></div>' +
          '<div class="pestle-article-title">' + escapeHtml(a.title) + '</div>' +
          (ja ? '<div class="pestle-article-trans">' + escapeHtml(ja) + '</div>' : '') +
          '</div>' +
        '</div></div>';
      });
    }
    if (articles.length > 5) {
      gridHtml += '<a class="pestle-show-more" onclick="event.stopPropagation();expandHomePESTLE(\'' + catKey + '\')">全' + articles.length + '件を表示</a>';
    }
    gridHtml += '</div></div>';
  });
  gridHtml += '</div>';

  var total = catKeys.reduce(function(s, k) {
    var a = pestle[k]?.articles || [];
    return s + (currentRegion === 'japan' ? a.filter(function(x) { return isJaSource(x); }).length : a.filter(function(x) { return !isJaSource(x); }).length);
  }, 0);
  var rl = currentRegion === 'japan' ? '日本メディア' : '海外メディア';
  targetEl.innerHTML = '<div class="pestle-meta-line">' + (data.date || '') + ' / ' + total + '件 (' + rl + ')</div>' + gridHtml;
}

window.expandHomePESTLE = function(catKey) {
  var data = dataCache['latest.json'];
  var aiData = dataCache['ai_analysis.json'];
  if (!data?.pestle?.[catKey]) return;
  var articles = (data.pestle[catKey].articles || []).slice();
  articles.sort(function(a, b) { return new Date(b.published_date || 0) - new Date(a.published_date || 0); });
  var filtered = currentRegion === 'japan' ? articles.filter(function(a) { return isJaSource(a); }) : articles.filter(function(a) { return !isJaSource(a); });
  var rawArticles = data.pestle[catKey].articles || [];
  var catTrans = (aiData?.translations || {})[catKey] || [];
  var cards = document.querySelectorAll('#homePestleGrid .pestle-card');
  var idx = Object.keys(PESTLE_CATS).indexOf(catKey);
  if (idx < 0 || !cards[idx]) return;
  var el = cards[idx].querySelector('.pestle-articles');
  if (!el) return;
  el.innerHTML = filtered.map(function(a) {
    var origIdx = rawArticles.indexOf(a);
    var tr = catTrans.find(function(t) { return t.index === origIdx; });
    var ja = tr?.title_translated || '';
    var bmId = 'news-' + catKey + '-' + origIdx;
    var isBm = bookmarks.some(function(b) { return b.id === bmId; });
    return '<div class="pestle-article"><div class="pestle-article-row">' +
      '<div class="pestle-article-content" onclick="openArticleModal(\'' + escapeAttr(catKey) + '\',' + origIdx + ')">' +
      '<div class="pestle-article-meta"><span class="pestle-article-source">' + escapeHtml(a.source || '') + '</span>' +
      '<span class="pestle-article-time">' + escapeHtml(a.published_date || '') + '</span></div>' +
      '<div class="pestle-article-title">' + escapeHtml(a.title) + '</div>' +
      (ja ? '<div class="pestle-article-trans">' + escapeHtml(ja) + '</div>' : '') +
      '</div>' +
    '</div></div>';
  }).join('');
  var more = cards[idx].querySelector('.pestle-show-more');
  if (more) more.remove();
};

// ==============================================================
// HOME FORESIGHT
// ==============================================================
window.submitHomeForesight = async function(e) {
  e.preventDefault();
  var input = document.getElementById('homeForesightInput');
  var question = input.value.trim();
  if (!question) return;
  var user = auth.currentUser;
  if (!user) { showToast('問いかけるにはログインが必要です。', 'error'); return; }

  var result = document.getElementById('homeForesightResult');
  result.classList.add('visible');
  result.innerHTML = '<div class="insight-loading"><div class="loading-spinner loading-spinner-sm"></div><span>分析中です。しばらくお待ちください...</span></div>';
  input.value = '';

  var WORKER_BASE = 'https://future-insight-proxy.nishimura-69a.workers.dev';
  try {
    var resp = await fetch(WORKER_BASE + '/api/foresight', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-User-Id': user.uid },
      body: JSON.stringify({ question: question, claContext: window.__claContext || '', signalsContext: window.__signalsContext || '', newsContext: window.__newsContext || '' })
    });
    if (!resp.ok) { var err = await resp.json().catch(function() { return {}; }); throw new Error(err.error || 'HTTP ' + resp.status); }
    var data = await resp.json();
    result.innerHTML = '<div class="insight-answer md-body">' + renderMarkdown(data.answer || '') + '</div>';
    try { await db.collection('foresight_queries').add({ question: question, answer: data.answer || '', userId: user.uid, createdAt: firebase.firestore.FieldValue.serverTimestamp() }); } catch (se) { console.warn('Save failed:', se); }
  } catch (err) {
    console.error('Foresight error:', err);
    result.innerHTML = '<div class="insight-error">回答の取得に失敗しました: ' + escapeHtml(err.message) + '</div>';
  }
};

// ==============================================================
// REGION TOGGLE LISTENER
// ==============================================================
document.addEventListener('regionChange', function() {
  renderHomeDashboard(dataCache['daily_report.json'], dataCache['latest.json'], dataCache['ai_analysis.json'], dataCache['daily_papers.json'], dataCache['insight_reports.json']);
});
