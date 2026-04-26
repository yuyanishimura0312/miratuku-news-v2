'use strict';
// Initialize nav and auth
initNav('bookmarks');
initAuthGuard(function(user) {
  updateBookmarkUI();
});
