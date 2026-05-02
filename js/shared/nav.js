'use strict';

// ==============================================================
// NAV — dynamically injects header, nav, alerts, footer, region
// toggle, and toast container into multi-page layout.
// ==============================================================

var NAV_LINKS = [
  { id: 'home',         href: 'home.html',         label: 'ホーム' },
  { id: 'signals',      href: 'signals.html',      label: 'シグナル' },
  { id: 'reports',      href: 'reports.html',       label: 'レポート' },
  { id: 'user-reports', href: 'user-reports.html',  label: '読者レポート' },
  { id: 'papers',       href: 'papers.html',        label: '学術研究' },
  { id: 'cla',          href: 'cla.html',           label: '因果階層分析' },
  { id: 'themes',       href: 'themes.html',        label: 'メガトレンド' },
  { id: 'foresight',    href: 'foresight.html',     label: '未来洞察' },
  { id: 'bookmarks',    href: 'bookmarks.html',     label: 'ブックマーク', badge: true, badgeId: 'bookmarkCount' },
  { id: 'databases',    href: 'databases.html',     label: 'データベース' },
  { id: 'strategy',     href: 'strategy.html',      label: '戦略' },
  { id: 'guide',        href: 'guide.html',         label: '使い方' }
];

var NAV_EXTERNAL_LINKS = [
  { href: 'dashboards/sg.html', label: 'Signal Dashboard' },
  { href: 'dashboard.html',     label: 'Collection' }
];

function initNav(activePageId) {
  _insertHeader(activePageId);
  _insertAlertsBar();
  _insertFooter();
  _insertRegionFloating();
  _insertToastContainer();
  _insertArticleModalShell();
  _setupThemeToggle();
  _setupRegionToggle();
}

// --- Header + Nav ---
function _insertHeader(activePageId) {
  var navEl = document.getElementById('app-nav');
  if (!navEl) return;

  var navItems = '';
  NAV_LINKS.forEach(function(link) {
    var cls = 'nav-link' + (link.id === activePageId ? ' active' : '');
    var badgeHtml = link.badge ? ' <span class="nav-badge" id="' + link.badgeId + '">0</span>' : '';
    var idAttr = link.id === 'bookmarks' ? ' id="navBookmarks"' : '';
    navItems += '<li><a href="' + link.href + '" class="' + cls + '"' + idAttr + '>' + link.label + badgeHtml + '</a></li>';
  });
  NAV_EXTERNAL_LINKS.forEach(function(link) {
    navItems += '<li><a href="' + link.href + '" class="nav-link" style="opacity:0.7">' + link.label + '</a></li>';
  });

  navEl.innerHTML =
    '<header class="site-header">' +
      '<div class="container">' +
        '<div class="header-main">' +
          '<div class="header-left">' +
            '<a href="home.html" class="site-title">Insight News</a>' +
            '<span class="header-date" id="headerDate"></span>' +
          '</div>' +
          '<div class="header-right">' +
            '<button class="theme-toggle" id="themeToggle" title="ダークモード切替" aria-label="ダークモード切替">&#9789;</button>' +
            '<div class="auth-area" id="authArea">' +
              '<span>読み込み中...</span>' +
            '</div>' +
          '</div>' +
        '</div>' +
      '</div>' +
      '<nav class="site-nav" aria-label="メインナビゲーション">' +
        '<div class="container">' +
          '<ul class="nav-list">' + navItems + '</ul>' +
        '</div>' +
      '</nav>' +
    '</header>';

  // Set header date
  var dateEl = document.getElementById('headerDate');
  if (dateEl) dateEl.textContent = formatDateFull(new Date());
}

// --- Alerts Bar ---
function _insertAlertsBar() {
  // Only insert if not already present
  if (document.getElementById('alertsBar')) return;
  var header = document.querySelector('.site-header');
  if (!header) return;
  var bar = document.createElement('div');
  bar.className = 'alerts-bar';
  bar.id = 'alertsBar';
  bar.innerHTML =
    '<div class="container">' +
      '<div class="alerts-inner">' +
        '<span class="alert-badge-label">速報</span>' +
        '<div class="alert-ticker">' +
          '<div class="alert-ticker-track" id="alertTicker"></div>' +
        '</div>' +
      '</div>' +
    '</div>';
  header.parentNode.insertBefore(bar, header.nextSibling);
}

// --- Footer ---
function _insertFooter() {
  var footerEl = document.getElementById('app-footer');
  if (!footerEl) return;

  footerEl.innerHTML =
    '<footer class="site-footer">' +
      '<div class="container">' +
        '<div class="footer-grid">' +
          '<div>' +
            '<div class="footer-brand">Insight News</div>' +
            '<p class="footer-desc">ミラツク・インテリジェンス・パイプラインによる自動ニュース収集、因果階層分析、学術論文追跡。未来思考のためのシグナルを毎日配信しています。</p>' +
          '</div>' +
          '<div>' +
            '<div class="footer-heading">セクション</div>' +
            '<ul class="footer-links">' +
              '<li><a href="home.html">ホーム</a></li>' +
              '<li><a href="signals.html">シグナル</a></li>' +
              '<li><a href="reports.html">レポート</a></li>' +
              '<li><a href="papers.html">学術研究</a></li>' +
              '<li><a href="foresight.html">未来洞察</a></li>' +
            '</ul>' +
          '</div>' +
          '<div>' +
            '<div class="footer-heading">その他</div>' +
            '<ul class="footer-links">' +
              '<li><a href="cla.html">因果階層分析</a></li>' +
              '<li><a href="guide.html">使い方ガイド</a></li>' +
              '<li><a href="#" onclick="auth.signOut();return false;">ログアウト</a></li>' +
            '</ul>' +
          '</div>' +
        '</div>' +
        '<div class="footer-bottom">&copy; 2026 Miratuku / esse-sense. All rights reserved. データは毎日午前4時に自動更新されます。</div>' +
      '</div>' +
    '</footer>';
}

// --- Region Floating Button ---
function _insertRegionFloating() {
  if (document.getElementById('regionFloating')) return;
  var div = document.createElement('div');
  div.className = 'region-floating';
  div.id = 'regionFloating';
  div.innerHTML =
    '<button class="region-btn active" data-region="japan">日本</button>' +
    '<button class="region-btn" data-region="global">グローバル</button>';
  document.body.appendChild(div);
}

// --- Toast Container ---
function _insertToastContainer() {
  if (document.getElementById('toastContainer')) return;
  var div = document.createElement('div');
  div.className = 'toast-container';
  div.id = 'toastContainer';
  document.body.appendChild(div);
}

// --- Article Modal Shell ---
function _insertArticleModalShell() {
  if (document.getElementById('articleModal')) return;
  var div = document.createElement('div');
  div.className = 'modal-overlay';
  div.id = 'articleModal';
  div.setAttribute('role', 'dialog');
  div.setAttribute('aria-modal', 'true');
  div.innerHTML =
    '<div class="modal-progress-bar"><div class="modal-progress-fill" id="modalProgressFill"></div></div>' +
    '<div class="modal-box" id="modalBox">' +
      '<div class="modal-reader-col">' +
        '<div class="modal-back-bar">' +
          '<button class="modal-back-btn" onclick="closeArticleModal()" aria-label="記事を閉じて戻る">&larr; 戻る</button>' +
          '<button class="modal-close" onclick="closeArticleModal()" aria-label="閉じる">&times;</button>' +
        '</div>' +
        '<div id="articleModalContent"></div>' +
      '</div>' +
    '</div>';
  document.body.appendChild(div);
}

// --- Theme Toggle ---
function _setupThemeToggle() {
  if (localStorage.getItem('fin_theme') === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
  var btn = document.getElementById('themeToggle');
  if (!btn) return;
  btn.addEventListener('click', function() {
    var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    if (isDark) { document.documentElement.removeAttribute('data-theme'); localStorage.setItem('fin_theme', 'light'); }
    else { document.documentElement.setAttribute('data-theme', 'dark'); localStorage.setItem('fin_theme', 'dark'); }
  });
}

// --- Region Toggle ---
function _setupRegionToggle() {
  document.querySelectorAll('.region-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      document.querySelectorAll('.region-btn').forEach(function(b) { b.classList.remove('active'); });
      this.classList.add('active');
      currentRegion = this.dataset.region;
      // Fire a custom event so page-specific JS can react
      document.dispatchEvent(new CustomEvent('regionChange', { detail: { region: currentRegion } }));
    });
  });
}
