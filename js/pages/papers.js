'use strict';
// Initialize nav and auth
initNav('papers');
initAuthGuard(function(user) {
  fetchJSON('daily_papers.json').then(renderPapers);
});

// ==============================================================
// RENDER: PAPERS
// ==============================================================
function renderPapers(data) {
  var container = document.getElementById('papersContent');
  if (!data) { container.innerHTML = '<p class="text-muted">学術論文データを取得できませんでした。</p>'; return; }
  var fields = data.fields || data.by_field || {};
  var fieldNames = Object.keys(fields);
  if (fieldNames.length === 0) { container.innerHTML = '<p class="text-muted">論文データがありません。</p>'; return; }

  document.getElementById('papersDateSub').textContent = data.generated_at ? data.generated_at.split('T')[0] : (data.date || '');

  var INITIAL_SHOW = 3;
  var html = '<div class="papers-accordion">';
  fieldNames.forEach(function(name, i) {
    var fieldData = fields[name];
    var papers = Array.isArray(fieldData) ? fieldData : (fieldData?.papers || []);
    papers = papers.slice().sort(function(a, b) { return new Date(b.published_date || 0) - new Date(a.published_date || 0); });
    var count = papers.length;

    html += '<div class="papers-field-group open" id="papers-group-' + i + '">' +
      '<div class="papers-field-header" onclick="togglePapersGroup(' + i + ')">' +
        '<div class="papers-field-info"><span class="papers-field-name">' + escapeHtml(name) + '</span><span class="papers-field-count">' + count + '</span></div>' +
        '<span class="papers-field-chevron">&#9654;</span>' +
      '</div>' +
      '<div class="papers-field-body"><div class="paper-list" id="papers-list-' + i + '">';
    papers.slice(0, INITIAL_SHOW).forEach(function(p, idx) { html += renderPaperItem(p, idx, name); });
    html += '</div>';
    if (count > INITIAL_SHOW) {
      html += '<div id="papers-more-' + i + '" class="paper-list" style="display:none">';
      papers.slice(INITIAL_SHOW).forEach(function(p, idx) { html += renderPaperItem(p, INITIAL_SHOW + idx, name); });
      html += '</div><div class="papers-more-wrap"><button class="btn-secondary" id="papers-toggle-' + i + '" onclick="togglePapersMore(' + i + ',' + count + ')">残り' + (count - INITIAL_SHOW) + '件を表示</button></div>';
    }
    html += '</div></div>';
  });
  html += '</div>';
  container.innerHTML = html;
}

function renderPaperItem(paper, idx, fieldName) {
  var sourceName = paper.source_name || '';
  var title = paper.title || '';
  var isJournalOnly = title && sourceName && title.trim() === sourceName.trim();
  var displayTitle = isJournalOnly ? (paper.title_ja || sourceName) : title;
  var bookmarkId = 'paper-' + fieldName + '-' + idx;
  var isBookmarked = bookmarks.some(function(b) { return b.id === bookmarkId; });

  return '<div class="paper-item">' +
    (sourceName ? '<div class="paper-journal">' + escapeHtml(sourceName) + '</div>' : '') +
    '<div class="paper-title-row"><div class="paper-title"><a href="' + escapeAttr(safeUrl(paper.source_url || paper.doi || '#')) + '" target="_blank">' + escapeHtml(displayTitle) + '</a></div>' +
    '<button class="bookmark-btn ' + (isBookmarked ? 'bookmarked' : '') + '" onclick="event.stopPropagation();toggleBookmark(\'' + bookmarkId + '\',\'' + escapeAttr(displayTitle) + '\',\'' + escapeAttr(safeUrl(paper.source_url || paper.doi || '')) + '\',this)" title="ブックマーク">&#9734;</button></div>' +
    (!isJournalOnly && paper.title_ja ? '<div class="paper-title-ja">' + escapeHtml(paper.title_ja) + '</div>' : '') +
    (paper.authors ? '<div class="paper-authors">' + escapeHtml(paper.authors) + '</div>' : '') +
    '<div class="paper-meta-row">' +
      (paper.field ? '<span class="paper-field-badge">' + escapeHtml(paper.field) + '</span>' : '') +
      (paper.subfield ? '<span class="paper-field-badge">' + escapeHtml(paper.subfield) + '</span>' : '') +
      (paper.published_date ? '<span class="paper-date">' + escapeHtml(paper.published_date) + '</span>' : '') +
    '</div>' +
    (paper.summary_ja || paper.summary ? '<div class="paper-summary">' + escapeHtml(paper.summary_ja || paper.summary) + '</div>' : '') +
    (paper.novelty_score ? '<div class="paper-novelty">新規性: ' + Math.round(Number(paper.novelty_score)) + '/10 <span class="paper-novelty-bar"><span class="paper-novelty-fill" style="width:' + (Number(paper.novelty_score) * 10) + '%"></span></span></div>' : '') +
  '</div>';
}

window.togglePapersGroup = function(index) {
  var group = document.getElementById('papers-group-' + index);
  if (group) group.classList.toggle('open');
};

window.togglePapersMore = function(index, total) {
  var more = document.getElementById('papers-more-' + index);
  var btn = document.getElementById('papers-toggle-' + index);
  if (!more) return;
  var isHidden = more.style.display === 'none';
  more.style.display = isHidden ? 'block' : 'none';
  btn.textContent = isHidden ? '折りたたむ' : '残り' + (total - 3) + '件を表示';
};
