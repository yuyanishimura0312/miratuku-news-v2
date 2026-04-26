'use strict';
initNav('user-reports');
initAuthGuard(function(user) {
  loadUserReports();

  async function loadUserReports() {
    var container = document.getElementById('userReportsContent');
    if (!container) return;

    if (!user) {
      container.innerHTML = '<div style="text-align:center;padding:40px 20px;color:var(--text-secondary)">' +
        '<p class="fs-h3" style="margin-bottom:12px">\u8aad\u8005\u30ec\u30dd\u30fc\u30c8\u3092\u8868\u793a\u3059\u308b\u306b\u306f\u30ed\u30b0\u30a4\u30f3\u304c\u5fc5\u8981\u3067\u3059\u3002</p>' +
        '<p class="fs-body" style="color:var(--text-muted)">\u53f3\u4e0a\u306e\u30ed\u30b0\u30a4\u30f3\u30dc\u30bf\u30f3\u304b\u3089Google\u30a2\u30ab\u30a6\u30f3\u30c8\u3067\u30ed\u30b0\u30a4\u30f3\u3057\u3066\u304f\u3060\u3055\u3044\u3002</p></div>';
      return;
    }

    container.innerHTML = '<div class="loading-indicator"><div class="loading-spinner"></div><div>\u8aad\u307f\u8fbc\u307f\u4e2d...</div></div>';

    try {
      var snap = await db.collection('user_reports')
        .where('userId', '==', user.uid)
        .get();
      var docs = [];
      snap.forEach(function(doc) { docs.push(doc); });
      docs.sort(function(a, b) {
        var aTs = (a.data().createdAt && a.data().createdAt.seconds) || 0;
        var bTs = (b.data().createdAt && b.data().createdAt.seconds) || 0;
        return bTs - aTs;
      });

      if (docs.length === 0) {
        container.innerHTML = '<div style="text-align:center;padding:40px 20px;color:var(--text-secondary)">' +
          '<p class="fs-h3" style="margin-bottom:8px">\u307e\u3060\u30ec\u30dd\u30fc\u30c8\u304c\u3042\u308a\u307e\u305b\u3093</p>' +
          '<p class="fs-body" style="color:var(--text-muted)">\u30ec\u30dd\u30fc\u30c8\u4e00\u89a7\u304b\u3089\u30a4\u30f3\u30b5\u30a4\u30c8\u30ec\u30dd\u30fc\u30c8\u3092\u958b\u304d\u3001\u300c\u3053\u306e\u8a18\u4e8b\u304b\u3089\u30ec\u30dd\u30fc\u30c8\u3092\u751f\u6210\u300d\u30dc\u30bf\u30f3\u3092\u4f7f\u3063\u3066\u30ec\u30dd\u30fc\u30c8\u3092\u4f5c\u6210\u3067\u304d\u307e\u3059\u3002</p></div>';
        return;
      }

      var html = '<div style="display:grid;gap:16px">';
      docs.forEach(function(doc) {
        var d = doc.data();
        var docId = doc.id;
        var preview = (d.generatedText || '').substring(0, 200).replace(/\n/g, ' ');
        if ((d.generatedText || '').length > 200) preview += '...';
        var dateStr = d.createdAt ? new Date(d.createdAt.seconds * 1000).toLocaleDateString('ja-JP', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' }) : '';

        html += '<div class="card" style="padding:20px;cursor:default" id="ur-card-' + docId + '">' +
          '<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px">' +
            '<div>' +
              '<div class="fs-meta" style="color:var(--text-muted);margin-bottom:4px">' + escapeHtml(dateStr) + '</div>' +
              '<div class="fs-body-lg" style="font-weight:600;color:var(--text)">' + escapeHtml(d.sourceReportTitle || '(\u7121\u984c)') + '</div>' +
            '</div>' +
            '<button class="btn-secondary fs-meta" style="padding:4px 10px;flex-shrink:0;margin-left:12px" onclick="deleteUserReport(\'' + docId + '\')">\u524a\u9664</button>' +
          '</div>' +
          '<div class="ur-preview fs-body" id="ur-preview-' + docId + '" style="color:var(--text-secondary);line-height:1.7;cursor:pointer" onclick="toggleUserReportExpand(\'' + docId + '\')">' +
            escapeHtml(preview) +
          '</div>' +
          '<div class="ur-full md-body" id="ur-full-' + docId + '" style="display:none;margin-top:12px;padding-top:12px;border-top:1px solid var(--border-light)" data-text="' + escapeAttr(d.generatedText || '') + '"></div>' +
          '<div style="margin-top:8px"><button class="btn-secondary fs-meta" style="padding:4px 12px" onclick="toggleUserReportExpand(\'' + docId + '\')" id="ur-toggle-' + docId + '">\u5168\u6587\u3092\u8868\u793a</button></div>' +
        '</div>';
      });
      html += '</div>';
      container.innerHTML = html;
    } catch (err) {
      console.error('Load user reports error:', err);
      container.innerHTML = '<div style="text-align:center;padding:40px 20px;color:var(--highlight)">\u8aad\u8005\u30ec\u30dd\u30fc\u30c8\u306e\u8aad\u307f\u8fbc\u307f\u306b\u5931\u6557\u3057\u307e\u3057\u305f: ' + escapeHtml(err.message) + '</div>';
    }
  }

  window.toggleUserReportExpand = function(docId) {
    var previewEl = document.getElementById('ur-preview-' + docId);
    var fullEl = document.getElementById('ur-full-' + docId);
    var toggleBtn = document.getElementById('ur-toggle-' + docId);
    if (!previewEl || !fullEl) return;

    if (fullEl.style.display === 'none') {
      if (!fullEl.innerHTML.trim()) {
        fullEl.innerHTML = renderMarkdown(fullEl.getAttribute('data-text') || '');
      }
      fullEl.style.display = 'block';
      previewEl.style.display = 'none';
      if (toggleBtn) toggleBtn.textContent = '\u6298\u308a\u305f\u305f\u3080';
    } else {
      fullEl.style.display = 'none';
      previewEl.style.display = 'block';
      if (toggleBtn) toggleBtn.textContent = '\u5168\u6587\u3092\u8868\u793a';
    }
  };

  window.deleteUserReport = async function(docId) {
    if (!confirm('\u3053\u306e\u30ec\u30dd\u30fc\u30c8\u3092\u524a\u9664\u3057\u307e\u3059\u304b\uff1f')) return;
    try {
      await db.collection('user_reports').doc(docId).delete();
      var card = document.getElementById('ur-card-' + docId);
      if (card) card.remove();
      showToast('\u30ec\u30dd\u30fc\u30c8\u3092\u524a\u9664\u3057\u307e\u3057\u305f\u3002', 'success');
      var container = document.getElementById('userReportsContent');
      if (container && !container.querySelector('.card')) {
        container.innerHTML = '<div style="text-align:center;padding:40px 20px;color:var(--text-secondary)">' +
          '<p class="fs-h3" style="margin-bottom:8px">\u307e\u3060\u30ec\u30dd\u30fc\u30c8\u304c\u3042\u308a\u307e\u305b\u3093</p>' +
          '<p class="fs-body" style="color:var(--text-muted)">\u30ec\u30dd\u30fc\u30c8\u4e00\u89a7\u304b\u3089\u30a4\u30f3\u30b5\u30a4\u30c8\u30ec\u30dd\u30fc\u30c8\u3092\u958b\u304d\u3001\u300c\u3053\u306e\u8a18\u4e8b\u304b\u3089\u30ec\u30dd\u30fc\u30c8\u3092\u751f\u6210\u300d\u30dc\u30bf\u30f3\u3092\u4f7f\u3063\u3066\u30ec\u30dd\u30fc\u30c8\u3092\u4f5c\u6210\u3067\u304d\u307e\u3059\u3002</p></div>';
      }
    } catch (err) {
      console.error('Delete user report error:', err);
      showToast('\u524a\u9664\u306b\u5931\u6557\u3057\u307e\u3057\u305f\u3002', 'error');
    }
  };
});
