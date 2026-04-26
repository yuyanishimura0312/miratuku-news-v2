'use strict';
initNav('foresight');
initAuthGuard(function(user) {
  var WORKER_BASE = 'https://future-insight-proxy.nishimura-69a.workers.dev';

  // Load AI analysis and latest data to populate context for foresight queries
  Promise.all([
    fetchJSON('ai_analysis.json'),
    fetchJSON('latest.json')
  ]).then(function(results) {
    var aiAnalysis = results[0];
    var latest = results[1];
    dataCache['ai_analysis.json'] = aiAnalysis;
    dataCache['latest.json'] = latest;

    // Populate foresight context for AI chat quality
    if (aiAnalysis && aiAnalysis.cla) {
      window.__claContext = Object.entries(aiAnalysis.cla)
        .map(function(kv) { return '[' + kv[0] + '] ' + (kv[1].litany || '') + ' ' + (kv[1].key_tension || ''); })
        .join('\n').slice(0, 3000);
    }
    if (aiAnalysis && aiAnalysis.weak_signals) {
      window.__signalsContext = aiAnalysis.weak_signals.slice(0, 20)
        .map(function(s) { return (s.signal || '') + ': ' + (s.description || ''); })
        .join('\n').slice(0, 2000);
    }
    if (latest && latest.pestle) {
      var topNews = [];
      Object.entries(latest.pestle).forEach(function(kv) {
        (kv[1].articles || []).slice(0, 3).forEach(function(a) { topNews.push('[' + kv[0] + '] ' + (a.title || '')); });
      });
      window.__newsContext = topNews.join('\n').slice(0, 2000);
    }
  });

  // Load foresight history
  loadForesightHistory();

  async function loadForesightHistory() {
    var container = document.getElementById('foresightHistoryContent');
    if (!container) return;
    if (!user) {
      container.innerHTML = '<p class="text-muted">\u6d1e\u5bdf\u5c65\u6b74\u3092\u898b\u308b\u306b\u306f\u30ed\u30b0\u30a4\u30f3\u304c\u5fc5\u8981\u3067\u3059\u3002</p>';
      return;
    }
    container.innerHTML = '<div class="loading-indicator"><div class="loading-spinner"></div><div>\u8aad\u307f\u8fbc\u307f\u4e2d...</div></div>';
    try {
      var snap = await db.collection('foresight_queries')
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
        container.innerHTML = '<p class="text-muted">\u307e\u3060\u6d1e\u5bdf\u306e\u5c65\u6b74\u304c\u3042\u308a\u307e\u305b\u3093\u3002\u300c\u672a\u6765\u6d1e\u5bdf\u300d\u304b\u3089\u554f\u3044\u304b\u3051\u3066\u304f\u3060\u3055\u3044\u3002</p>';
        return;
      }
      var html = '';
      docs.forEach(function(doc) {
        var d = doc.data();
        var ts = d.createdAt ? d.createdAt.toDate() : null;
        var dateStr = ts ? ts.toLocaleDateString('ja-JP', { year: 'numeric', month: 'long', day: 'numeric' }) + ' ' + ts.toLocaleTimeString('ja-JP', { hour: '2-digit', minute: '2-digit' }) : '';
        html += '<div class="card" id="fh-' + doc.id + '">' +
          '<div class="card-title">' + escapeHtml(d.question || '') + '</div>' +
          '<div class="card-sub">' + escapeHtml(dateStr) + '</div>' +
          '<div class="md-body">' + renderMarkdown(d.answer || '') + '</div>' +
          '<div style="margin-top:0.75rem;text-align:right;">' +
          '<button class="btn-secondary fs-body-sm" style="padding:0.3rem 0.8rem;" onclick="deleteForesightEntry(\'' + doc.id + '\')">\u524a\u9664</button>' +
          '</div></div>';
      });
      container.innerHTML = html;
    } catch (err) {
      console.error('Foresight history error:', err);
      container.innerHTML = '<p class="text-muted">\u5c65\u6b74\u306e\u8aad\u307f\u8fbc\u307f\u306b\u5931\u6557\u3057\u307e\u3057\u305f: ' + escapeHtml(err.message) + '</p>';
    }
  }

  window.deleteForesightEntry = async function(docId) {
    if (!confirm('\u3053\u306e\u6d1e\u5bdf\u5c65\u6b74\u3092\u524a\u9664\u3057\u307e\u3059\u304b\uff1f')) return;
    try {
      await db.collection('foresight_queries').doc(docId).delete();
      var el = document.getElementById('fh-' + docId);
      if (el) el.remove();
      showToast('\u524a\u9664\u3057\u307e\u3057\u305f\u3002', 'success');
      var container = document.getElementById('foresightHistoryContent');
      if (container && !container.querySelector('.card')) {
        container.innerHTML = '<p class="text-muted">\u307e\u3060\u6d1e\u5bdf\u306e\u5c65\u6b74\u304c\u3042\u308a\u307e\u305b\u3093\u3002\u300c\u672a\u6765\u6d1e\u5bdf\u300d\u304b\u3089\u554f\u3044\u304b\u3051\u3066\u304f\u3060\u3055\u3044\u3002</p>';
      }
    } catch (err) {
      console.error('Delete error:', err);
      showToast('\u524a\u9664\u306b\u5931\u6557\u3057\u307e\u3057\u305f\u3002', 'error');
    }
  };

  // Insight form submit handler
  var insightForm = document.getElementById('insightForm');
  if (insightForm) {
    insightForm.addEventListener('submit', async function(e) {
      e.preventDefault();
      var text = document.getElementById('insightText').value.trim();
      if (!text) return;
      if (!user) { showToast('\u6295\u7a3f\u3059\u308b\u306b\u306f\u30ed\u30b0\u30a4\u30f3\u304c\u5fc5\u8981\u3067\u3059\u3002', 'error'); return; }
      var submitBtn = this.querySelector('button[type="submit"]');
      var origText = submitBtn.textContent;
      submitBtn.disabled = true;
      submitBtn.textContent = '\u5206\u6790\u4e2d...';

      try {
        var resp = await fetch(WORKER_BASE + '/api/foresight', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-User-Id': user.uid },
          body: JSON.stringify({ question: text, claContext: window.__claContext || '', signalsContext: window.__signalsContext || '', newsContext: window.__newsContext || '' })
        });
        if (!resp.ok) { var err = await resp.json().catch(function() { return {}; }); throw new Error(err.error || 'HTTP ' + resp.status); }
        var data = await resp.json();
        var answerEl = document.getElementById('foresightAnswer');
        answerEl.className = 'insight-answer md-body';
        answerEl.innerHTML = '<h4 class="cla-extra-label">\u56de\u7b54</h4>' + renderMarkdown(data.answer || '');
        try { await db.collection('foresight_queries').add({ question: text, answer: data.answer || '', userId: user.uid, createdAt: firebase.firestore.FieldValue.serverTimestamp() }); } catch (se) { console.warn('Save failed:', se); }
        showToast('\u56de\u7b54\u3092\u751f\u6210\u3057\u307e\u3057\u305f\u3002', 'success');
      } catch (err) {
        console.error('Foresight error:', err);
        showToast('\u56de\u7b54\u306e\u53d6\u5f97\u306b\u5931\u6557\u3057\u307e\u3057\u305f: ' + err.message, 'error');
      } finally { submitBtn.disabled = false; submitBtn.textContent = origText; }
    });
  }
});
