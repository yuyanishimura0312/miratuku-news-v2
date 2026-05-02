'use strict';

// ==============================================================
// AUTH GUARD — reusable across all authenticated pages
// ==============================================================
function initAuthGuard(onAuthenticated) {
  auth.onAuthStateChanged(async function(user) {
    var area = document.getElementById('authArea');
    if (!user) { window.location.href = 'index.html'; return; }

    // Re-validate user status and trial expiry on every auth state change
    try {
      var userDoc = await db.collection('users').doc(user.uid).get();
      if (userDoc.exists) {
        var data = userDoc.data();
        if (data.status === 'disabled') {
          await auth.signOut();
          window.location.href = 'index.html';
          return;
        }
        if (data.trialExpiresAt && data.trialExpiresAt.toDate() < new Date() && data.role !== 'admin') {
          await auth.signOut();
          window.location.href = 'index.html';
          return;
        }
      }
    } catch (e) {
      console.error('User validation failed:', e);
    }

    var name = user.displayName || user.email || 'User';
    if (area) {
      area.innerHTML = '<span class="user-name">' + escapeHtml(name) + '</span>' +
        '<button class="auth-btn" onclick="auth.signOut()">ログアウト</button>';
    }
    if (onAuthenticated) onAuthenticated(user);
  });
}
