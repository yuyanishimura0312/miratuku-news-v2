'use strict';

// ==============================================================
// AUTH GUARD — disabled (login not required)
// initAuthGuard immediately invokes the callback with a synthetic guest user.
// ==============================================================
function initAuthGuard(onAuthenticated) {
  var guest = { uid: 'guest', email: 'guest@local', displayName: 'Guest' };
  if (typeof onAuthenticated === 'function') {
    setTimeout(function () { onAuthenticated(guest); }, 0);
  }
}
