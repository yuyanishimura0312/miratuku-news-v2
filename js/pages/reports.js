'use strict';
// Initialize nav and auth
initNav('reports');
initAuthGuard(function(user) {
  loadReportsData();
});

// Store reports data globally for insight report modal
var _insightReportsData = null;

async function loadReportsData() {
  var results = await Promise.all([
    fetchJSON('daily_report.json'),
    fetchJSON('insight_reports.json')
  ]);
  var dailyReport = results[0];
  var insightReports = results[1];

  // Store insight reports for modal access
  if (insightReports) {
    _insightReportsData = insightReports;
  }

  renderReportsArchive(dailyReport);
  updateBookmarkUI();
}

// ==============================================================
// RENDER: REPORTS ARCHIVE
// ==============================================================
function renderReportsArchive(dailyReport) {
  var container = document.getElementById('reportsArchiveContent');
  if (!dailyReport) { container.innerHTML = '<p class="text-muted">レポートデータがありません。</p>'; return; }
  var dateStr = dailyReport.generated_at ? dailyReport.generated_at.split('T')[0] : '';

  var html = '';

  // Insight Reports section
  var irData = dataCache['insight_reports.json'];
  if (irData?.reports?.length > 0) {
    html += '<h3 class="section-title" style="margin-bottom:12px">インサイトレポート <span class="section-date">' + escapeHtml(irData.date || '') + '</span></h3>';
    html += '<div class="ir-report-grid">';
    irData.reports.forEach(function(r, i) {
      var color = getPestleColor(r.article?.pestle_category);
      html += '<div class="ir-carousel-card" onclick="openInsightReport(' + i + ')" style="flex:none;width:auto">' +
        '<div class="ir-carousel-accent" style="background:' + color + '"></div>' +
        '<div class="ir-carousel-body">' +
          '<div class="ir-carousel-header"><div class="ir-carousel-dot" style="background:' + color + '" title="' + escapeHtml(getPestleLabel(r.article?.pestle_category)) + '"></div>' +
          '<span class="ir-carousel-cat">' + escapeHtml(getPestleLabel(r.article?.pestle_category)) + '</span></div>' +
          '<div class="ir-carousel-title" style="-webkit-line-clamp:3">' + escapeHtml(r.report_title || '') + '</div>' +
          mythBadgeHtml(r.myth_relation, 'ir-carousel-myth') +
          '<div class="ir-carousel-preview">' + escapeHtml(r.summary ? r.summary.substring(0, 150) : stripMarkdown(r.report_text || '').substring(0, 150)) + '...</div>' +
        '</div></div>';
    });
    html += '</div>';

    // Load and render index for past dates
    if (!dataCache['insight_reports_index.json']) {
      fetchJSON('insight_reports_index.json').then(function(idx) {
        if (idx) renderInsightReportIndex(idx, irData.date);
      });
    } else {
      setTimeout(function() { renderInsightReportIndex(dataCache['insight_reports_index.json'], irData.date); }, 0);
    }
    html += '<div id="irArchiveIndex"></div>';
  }

  // Separator
  html += '<h3 class="section-title" style="margin-bottom:12px">月次分析レポート</h3>';

  ['japan', 'global'].forEach(function(regionKey) {
    var region = dailyReport[regionKey];
    if (!region) return;
    var regionLabel = regionKey === 'japan' ? '日本版' : 'グローバル版';
    var preview = (region.report_text || '').substring(0, 200) + '...';
    var obs = region.key_observations || region.observations || [];
    var declining = region.myth_in_transition?.declining || region.declining_myths || [];
    var emerging = region.myth_in_transition?.emerging || region.emerging_myths || [];

    html += '<div class="report-archive-card">' +
      '<div class="report-archive-header"><div class="report-archive-title">' + dateStr + ' レポート</div>' +
      '<span class="report-archive-region">' + regionLabel + '</span></div>' +
      '<div class="report-archive-preview">' + escapeHtml(preview) + '</div>';

    if (obs.length > 0) {
      html += '<div class="report-obs-label">観測</div>';
      obs.forEach(function(o) { html += '<div class="report-obs-item">[' + escapeHtml(o.category || '') + '] ' + escapeHtml(o.observation || '') + '</div>'; });
    }

    var decArr = Array.isArray(declining) ? declining : [];
    var emArr = Array.isArray(emerging) ? emerging : [];
    if (decArr.length > 0 || emArr.length > 0) {
      html += '<div class="report-myth-section">';
      if (decArr.length > 0) {
        html += '<div><div class="report-myth-label myth-label-decline">衰退する神話</div>';
        decArr.forEach(function(m) { html += '<div class="report-myth-item">- ' + escapeHtml(m) + '</div>'; });
        html += '</div>';
      }
      if (emArr.length > 0) {
        html += '<div><div class="report-myth-label myth-label-emerge">浮上する神話</div>';
        emArr.forEach(function(m) { html += '<div class="report-myth-item">- ' + escapeHtml(m) + '</div>'; });
        html += '</div>';
      }
      html += '</div>';
    }

    html += '<details><summary class="fulltext-toggle">全文を読む</summary>' +
      '<div class="fulltext-body md-body">' + renderMarkdown(region.report_text || '') + '</div></details>';
    html += '</div>';
  });

  container.innerHTML = html || '<p class="text-muted">レポートデータがありません。</p>';
}

// ==============================================================
// RENDER: INSIGHT REPORT INDEX (past dates)
// ==============================================================
function renderInsightReportIndex(indexData, currentDate) {
  var el = document.getElementById('irArchiveIndex');
  if (!el || !indexData?.dates) return;
  var pastDates = indexData.dates.filter(function(d) { return d.date !== currentDate; });
  if (pastDates.length === 0) return;

  var html = '<h4 class="fs-body" style="color:var(--text-secondary);margin:16px 0 8px">過去のインサイトレポート</h4>';
  pastDates.forEach(function(d) {
    html += '<details class="report-card" style="margin-bottom:8px">' +
      '<summary class="report-summary fs-body" style="cursor:pointer;padding:10px 14px;">' +
        '<span class="report-chevron">&#9654;</span>' +
        '<span style="font-weight:600">' + escapeHtml(d.date) + '</span>' +
        '<span class="report-count">' + d.count + '件</span>' +
      '</summary>' +
      '<div class="report-body" id="irArchive-' + d.date + '">' +
        '<div class="loading-indicator" style="padding:12px"><div class="loading-spinner loading-spinner-sm"></div><span>読み込み中...</span></div>' +
      '</div></details>';
  });
  el.innerHTML = html;

  // Load past reports on expand
  el.querySelectorAll('details').forEach(function(det) {
    det.addEventListener('toggle', function() {
      if (!this.open) return;
      var dateKey = this.querySelector('[id^="irArchive-"]')?.id?.replace('irArchive-', '');
      if (!dateKey) return;
      var target = document.getElementById('irArchive-' + dateKey);
      if (target.dataset.loaded) return;
      target.dataset.loaded = 'true';
      fetchJSON('insight_reports_' + dateKey + '.json').then(function(data) {
        if (!data?.reports) { target.innerHTML = '<p class="text-muted">データがありません。</p>'; return; }
        // Cache for modal use
        dataCache['insight_reports_' + dateKey + '.json'] = data;
        var inner = '<div class="ir-archive-grid">';
        data.reports.forEach(function(r, i) {
          var color = getPestleColor(r.article?.pestle_category);
          inner += '<div class="ir-carousel-card" style="flex:none;width:auto;cursor:pointer" onclick="openArchivedInsightReport(\'' + dateKey + '\',' + i + ')">' +
            '<div class="ir-carousel-accent" style="background:' + color + '"></div>' +
            '<div class="ir-carousel-body">' +
              '<div class="ir-carousel-header"><div class="ir-carousel-dot" style="background:' + color + '" title="' + escapeHtml(getPestleLabel(r.article?.pestle_category)) + '"></div>' +
              '<span class="ir-carousel-cat">' + escapeHtml(getPestleLabel(r.article?.pestle_category)) + '</span></div>' +
              '<div class="ir-carousel-title">' + escapeHtml(r.report_title || '') + '</div>' +
              mythBadgeHtml(r.myth_relation, 'ir-carousel-myth') +
            '</div></div>';
        });
        inner += '</div>';
        target.innerHTML = inner;
      });
    });
  });
}

// ==============================================================
// OPEN INSIGHT REPORT (modal)
// ==============================================================
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

  if (r.summary) {
    modalHtml += '<div class="ir-summary">' + escapeHtml(r.summary) + '</div>';
  }

  if (r.article) {
    modalHtml += '<div class="fs-meta" style="color:var(--text-muted);margin-bottom:16px;padding:10px 14px;background:var(--surface);border-radius:var(--radius-xs)">' +
      '元記事: ' + escapeHtml(r.article.title_ja || r.article.title || '') +
      ' (' + escapeHtml(r.article.source || '') + ', ' + escapeHtml(r.article.published_date || '') + ')' +
      (r.article.url ? ' <a href="' + escapeAttr(safeUrl(r.article.url)) + '" target="_blank">記事を読む &rarr;</a>' : '') +
    '</div>';
  }

  // Historical context
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

  if (r.future_signals) {
    var fsLabel = r.future_signals_title ? escapeHtml(r.future_signals_title) : '未来へのシグナル';
    modalHtml += '<div class="ir-modal-section open">' +
      '<div class="ir-modal-section-header" onclick="this.parentElement.classList.toggle(\'open\')">' + fsLabel + '<span class="ir-modal-section-chevron">&#9654;</span></div>' +
      '<div class="ir-modal-section-body md-body">' + renderMarkdown(r.future_signals) + '</div>' +
    '</div>';
  }

  if (r.watch_points) {
    var wpLabel = r.watch_points_title ? escapeHtml(r.watch_points_title) : 'ウォッチポイント';
    modalHtml += '<div class="ir-modal-section open">' +
      '<div class="ir-modal-section-header" onclick="this.parentElement.classList.toggle(\'open\')">' + wpLabel + '<span class="ir-modal-section-chevron">&#9654;</span></div>' +
      '<div class="ir-modal-section-body md-body">' + renderMarkdown(r.watch_points) + '</div>' +
    '</div>';
  }

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
            (item.author ? ' \u2014 ' + escapeHtml(item.author) : '') +
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

window.openArchivedInsightReport = function(dateKey, index) {
  var data = dataCache['insight_reports_' + dateKey + '.json'];
  if (!data?.reports?.[index]) return;
  // Temporarily set data for modal reuse
  var prevData = _insightReportsData;
  _insightReportsData = data;
  openInsightReport(index);
  _insightReportsData = prevData;
};
