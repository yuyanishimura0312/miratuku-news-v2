// Shared UI components — used by both FIW and Miratuku News

// HTML escape utility
function esc(str) {
  if (!str) return '';
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// Format date in Japanese style
function formatDate(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  if (isNaN(d)) return dateStr;
  if (LANG === 'ja') {
    return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`;
  }
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

// Format relative time
function timeAgo(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  const now = new Date();
  const diff = now - d;
  const mins = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);
  if (LANG === 'ja') {
    if (mins < 60) return `${mins}分前`;
    if (hours < 24) return `${hours}時間前`;
    if (days < 7) return `${days}日前`;
    return formatDate(dateStr);
  }
  if (mins < 60) return `${mins}m ago`;
  if (hours < 24) return `${hours}h ago`;
  if (days < 7) return `${days}d ago`;
  return formatDate(dateStr);
}

// Truncate text with ellipsis
function truncate(text, maxLen = 150) {
  if (!text || text.length <= maxLen) return text || '';
  return text.substring(0, maxLen) + '...';
}

// Show toast notification
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  document.body.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add('show'));
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 2500);
}

// Modal dialog
function showModal(title, contentHTML, options = {}) {
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.innerHTML = `
    <div class="modal-content ${options.wide ? 'modal-wide' : ''}">
      <div class="modal-header">
        <h3>${esc(title)}</h3>
        <button class="modal-close" aria-label="Close">&times;</button>
      </div>
      <div class="modal-body">${contentHTML}</div>
    </div>
  `;
  overlay.querySelector('.modal-close').addEventListener('click', () => overlay.remove());
  overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });
  document.body.appendChild(overlay);
  return overlay;
}

// Loading overlay
function showLoading(container) {
  const el = document.createElement('div');
  el.className = 'loading-overlay';
  el.innerHTML = '<div class="loading-spinner"></div>';
  container.style.position = 'relative';
  container.appendChild(el);
  return () => el.remove();
}

// Debounce utility
function debounce(fn, delay = 300) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

// PESTLE category metadata
const PESTLE_META = {
  'P': { key: 'Political', name_ja: '政治', name_en: 'Political', color: '#8B3D2F' },
  'E': { key: 'Economic', name_ja: '経済', name_en: 'Economic', color: '#B87A4A' },
  'S': { key: 'Social', name_ja: '社会', name_en: 'Social', color: '#4F7A47' },
  'T': { key: 'Technological', name_ja: '技術', name_en: 'Technological', color: '#3A7A96' },
  'L': { key: 'Legal', name_ja: '法律', name_en: 'Legal', color: '#6B4F82' },
  'En': { key: 'Environmental', name_ja: '環境', name_en: 'Environmental', color: '#2D7A6B' },
};

// Academic field metadata
const FIELD_META = {
  '自然科学': { name_en: 'Natural Sciences', color: '#3A7A96' },
  '工学': { name_en: 'Engineering', color: '#6B4F82' },
  '社会科学': { name_en: 'Social Sciences', color: '#4F7A47' },
  '人文学': { name_en: 'Humanities', color: '#B87A4A' },
  '芸術': { name_en: 'Arts', color: '#8B3D2F' },
};
