'use strict';

// ==============================================================
// CONFIG & STATE
// ==============================================================
var DATA_BASE = 'https://yuyanishimura0312.github.io/future-insight-app/data';
function cacheBust() { return '?v=' + Date.now(); }

var currentRegion = 'japan';
var bookmarks = JSON.parse(localStorage.getItem('fin_bookmarks') || '[]');
var dataCache = {};

var PESTLE_CATS = {
  Political:     { label: 'Political',     labelJa: '政治', color: 'var(--P)' },
  Economic:      { label: 'Economic',      labelJa: '経済', color: 'var(--E)' },
  Social:        { label: 'Social',        labelJa: '社会', color: 'var(--S)' },
  Technological: { label: 'Technological', labelJa: '技術', color: 'var(--T)' },
  Legal:         { label: 'Legal',         labelJa: '法律', color: 'var(--L)' },
  Environmental: { label: 'Environmental', labelJa: '環境', color: 'var(--En)' }
};

var CLA_LAYERS = [
  { key: 'litany',              labelJa: 'リタニー（表層事象）', depth: 1 },
  { key: 'systemic_causes',     labelJa: '社会的原因',           depth: 2 },
  { key: 'worldview',           labelJa: 'ディスコース（世界観）', depth: 3 },
  { key: 'myth_metaphor',       labelJa: '神話・メタファー',      depth: 4 },
  { key: 'key_tension',         labelJa: '核心的緊張',           depth: 5 },
  { key: 'emerging_narrative',  labelJa: '新たな物語',           depth: 6 }
];

var JA_SOURCES = ['nhk', 'yahoo', 'nikkei', '日経', '毎日', '朝日', '読売', 'mainichi', 'asahi', 'yomiuri', 'tokyo', 'sankei', 'kyodo', 'jiji', 'nifty'];

function isJaSource(article) {
  if (article.lang === 'ja') return true;
  if (article.lang === 'en') return false;
  var src = (article.source || '').toLowerCase();
  return JA_SOURCES.some(function(s) { return src.includes(s); });
}

// ==============================================================
// UTILITIES
// ==============================================================
function escapeHtml(str) {
  if (str == null) return '';
  var div = document.createElement('div');
  div.textContent = String(str);
  return div.innerHTML;
}

function escapeAttr(str) {
  if (str == null) return '';
  str = String(str);
  return str.replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/"/g, '&quot;').replace(/\n/g, ' ').replace(/\r/g, '');
}

function safeUrl(url) {
  if (!url) return '#';
  try {
    var u = new URL(url, location.href);
    return (u.protocol === 'http:' || u.protocol === 'https:') ? url : '#';
  } catch(e) { return '#'; }
}

function formatDateFull(date) {
  return date.toLocaleDateString('ja-JP', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' });
}

function showToast(message, type) {
  var container = document.getElementById('toastContainer');
  if (!container) return;
  var toast = document.createElement('div');
  toast.className = 'toast' + (type ? ' toast-' + type : '');
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(function() { toast.classList.add('toast-out'); setTimeout(function() { toast.remove(); }, 300); }, 3500);
}

function renderMarkdown(text) {
  if (!text) return '';
  var html = '';
  var inList = false;
  var lines = text.split('\n');
  for (var i = 0; i < lines.length; i++) {
    var trimmed = lines[i].trim();
    if (!trimmed) { if (inList) { html += '</ul>'; inList = false; } continue; }
    if (trimmed.startsWith('### ')) { if (inList) { html += '</ul>'; inList = false; } html += '<h3>' + inlineMd(escapeHtml(trimmed.slice(4))) + '</h3>'; continue; }
    if (trimmed.startsWith('## '))  { if (inList) { html += '</ul>'; inList = false; } html += '<h2>' + inlineMd(escapeHtml(trimmed.slice(3))) + '</h2>'; continue; }
    if (trimmed.startsWith('# '))   { if (inList) { html += '</ul>'; inList = false; } html += '<h2>' + inlineMd(escapeHtml(trimmed.slice(2))) + '</h2>'; continue; }
    if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) { if (!inList) { html += '<ul>'; inList = true; } html += '<li>' + inlineMd(escapeHtml(trimmed.slice(2))) + '</li>'; continue; }
    if (inList) { html += '</ul>'; inList = false; }
    html += '<p>' + inlineMd(escapeHtml(trimmed)) + '</p>';
  }
  if (inList) html += '</ul>';
  return html;
}

function inlineMd(str) {
  return str.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
}

// Strip markdown syntax for plain-text previews
function stripMarkdown(text) {
  return (text || '')
    .replace(/^#{1,6}\s+/gm, '')       // headings
    .replace(/\*\*([^*]+)\*\*/g, '$1')  // bold
    .replace(/\*([^*]+)\*/g, '$1')      // italic
    .replace(/`([^`]+)`/g, '$1')        // inline code
    .replace(/^\s*[-*]\s+/gm, '')       // list items
    .replace(/\n{2,}/g, '\n')           // excess newlines
    .trim();
}

// Shared helpers for PESTLE category display
function getPestleColor(cat) {
  return PESTLE_CATS[cat]?.color || 'var(--accent)';
}
function getPestleLabel(cat) {
  return PESTLE_CATS[cat]?.labelJa || cat;
}
function mythBadgeHtml(relation, cls) {
  var isChange = relation === 'changes';
  var label = isChange ? '神話を変革' : '神話を強化';
  var badgeCls = isChange ? 'ir-myth-badge-transforms' : 'ir-myth-badge-strengthens';
  return '<span class="' + cls + ' ' + badgeCls + '">' + label + '</span>';
}
