// Firestore operations for comments, bookmarks, and foresight queries
// Depends on firebase-config.js being loaded first (provides `db` and `auth`)

const NewsReactions = {
  // ============================================================
  // Comments
  // ============================================================

  /**
   * Post a comment on a news article or signal
   * @param {string} articleId - Unique article identifier
   * @param {string} articleType - 'pestle' | 'signal' | 'cla'
   * @param {string} content - Comment text
   * @param {string} [region] - Region tag if applicable
   * @returns {Promise<string>} Created comment document ID
   */
  async postComment(articleId, articleType, content, region) {
    const user = auth.currentUser;
    if (!user) throw new Error('Authentication required');
    if (!content || content.trim().length === 0) throw new Error('Comment content is required');

    const docRef = await db.collection('news_comments').add({
      articleId,
      articleType,
      content: content.trim(),
      region: region || null,
      userId: user.uid,
      userName: user.displayName || user.email || 'Anonymous',
      createdAt: firebase.firestore.FieldValue.serverTimestamp(),
    });
    return docRef.id;
  },

  /**
   * Get all comments for a specific article, ordered by creation time
   * @param {string} articleId - Article identifier
   * @returns {Promise<Array>} Array of comment objects
   */
  async getComments(articleId) {
    const snapshot = await db
      .collection('news_comments')
      .where('articleId', '==', articleId)
      .orderBy('createdAt', 'asc')
      .get();

    return snapshot.docs.map((doc) => ({
      id: doc.id,
      ...doc.data(),
      // Convert Firestore Timestamp to JS Date for display
      createdAt: doc.data().createdAt ? doc.data().createdAt.toDate() : null,
    }));
  },

  /**
   * Delete a comment (only the owner can delete)
   * @param {string} commentId - Comment document ID
   */
  async deleteComment(commentId) {
    const user = auth.currentUser;
    if (!user) throw new Error('Authentication required');

    // Verify ownership before attempting delete (Firestore rules also enforce this)
    const doc = await db.collection('news_comments').doc(commentId).get();
    if (!doc.exists) throw new Error('Comment not found');
    if (doc.data().userId !== user.uid) throw new Error('Permission denied');

    await db.collection('news_comments').doc(commentId).delete();
  },

  // ============================================================
  // Bookmarks
  // ============================================================

  /**
   * Add a bookmark for an article
   * @param {string} articleId - Article identifier
   * @param {string} articleType - 'pestle' | 'signal' | 'cla'
   * @param {string} title - Article title for display in bookmark list
   * @param {string} [category] - PESTLE category or signal theme
   * @param {string} [region] - Region tag
   * @returns {Promise<string>} Created bookmark document ID
   */
  async addBookmark(articleId, articleType, title, category, region) {
    const user = auth.currentUser;
    if (!user) throw new Error('Authentication required');

    // Use a deterministic ID to prevent duplicate bookmarks
    const bookmarkId = `${user.uid}_${articleId}`;

    await db.collection('news_bookmarks').doc(bookmarkId).set({
      articleId,
      articleType,
      title: title || '',
      category: category || null,
      region: region || null,
      userId: user.uid,
      createdAt: firebase.firestore.FieldValue.serverTimestamp(),
    });

    return bookmarkId;
  },

  /**
   * Remove a bookmark
   * @param {string} bookmarkId - Bookmark document ID
   */
  async removeBookmark(bookmarkId) {
    const user = auth.currentUser;
    if (!user) throw new Error('Authentication required');

    await db.collection('news_bookmarks').doc(bookmarkId).delete();
  },

  /**
   * Get bookmarks for the current user with optional filters
   * @param {string} userId - User ID (must match current user due to security rules)
   * @param {Object} [filters] - Optional filters
   * @param {string} [filters.articleType] - Filter by article type
   * @param {string} [filters.category] - Filter by category
   * @returns {Promise<Array>} Array of bookmark objects
   */
  async getBookmarks(userId, filters = {}) {
    const user = auth.currentUser;
    if (!user) throw new Error('Authentication required');
    // Security rules only allow reading own bookmarks
    if (userId !== user.uid) throw new Error('Can only read own bookmarks');

    let query = db.collection('news_bookmarks').where('userId', '==', userId);

    if (filters.articleType) {
      query = query.where('articleType', '==', filters.articleType);
    }
    if (filters.category) {
      query = query.where('category', '==', filters.category);
    }

    // Order by creation time (newest first)
    query = query.orderBy('createdAt', 'desc');

    const snapshot = await query.get();
    return snapshot.docs.map((doc) => ({
      id: doc.id,
      ...doc.data(),
      createdAt: doc.data().createdAt ? doc.data().createdAt.toDate() : null,
    }));
  },

  /**
   * Check if an article is bookmarked by the current user
   * @param {string} articleId - Article identifier
   * @returns {Promise<boolean>} True if bookmarked
   */
  async isBookmarked(articleId) {
    const user = auth.currentUser;
    if (!user) return false;

    const bookmarkId = `${user.uid}_${articleId}`;
    const doc = await db.collection('news_bookmarks').doc(bookmarkId).get();
    return doc.exists;
  },

  // ============================================================
  // Foresight Queries
  // ============================================================

  /**
   * Save a foresight question and its AI-generated answer
   * @param {string} question - User's question text
   * @param {string} answer - AI-generated answer text
   * @returns {Promise<string>} Created query document ID
   */
  async saveForesightQuery(question, answer) {
    const user = auth.currentUser;
    if (!user) throw new Error('Authentication required');

    const docRef = await db.collection('foresight_queries').add({
      question,
      answer,
      userId: user.uid,
      createdAt: firebase.firestore.FieldValue.serverTimestamp(),
    });
    return docRef.id;
  },

  /**
   * Get the current user's foresight query history (newest first)
   * @param {number} [limit=20] - Max number of queries to return
   * @returns {Promise<Array>} Array of query objects
   */
  async getForesightHistory(limit = 20) {
    const user = auth.currentUser;
    if (!user) throw new Error('Authentication required');

    const snapshot = await db
      .collection('foresight_queries')
      .where('userId', '==', user.uid)
      .orderBy('createdAt', 'desc')
      .limit(limit)
      .get();

    return snapshot.docs.map((doc) => ({
      id: doc.id,
      ...doc.data(),
      createdAt: doc.data().createdAt ? doc.data().createdAt.toDate() : null,
    }));
  },
};
