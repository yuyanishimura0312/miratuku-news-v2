// Foresight query UI logic — connects to Worker API and Firestore
// Depends on: firebase-config.js, reactions.js

const Foresight = {
  // Worker endpoint for AI-powered foresight
  workerBase: 'https://future-insight-proxy.yuyanishimura0312.workers.dev',

  /**
   * Send a foresight question to the Worker API with context data
   * Automatically gathers CLA/signal/news context if available on the page
   * @param {string} question - User's question text
   * @returns {Promise<Object>} { answer, model, usage }
   */
  async askQuestion(question) {
    if (!question || question.trim().length === 0) {
      throw new Error('Question is required');
    }

    const user = auth.currentUser;
    if (!user) throw new Error('Authentication required');

    // Gather context from the page if available (global variables set by data-loader)
    const claContext = window.__claContext || '';
    const signalsContext = window.__signalsContext || '';
    const newsContext = window.__newsContext || '';

    const resp = await fetch(`${this.workerBase}/api/foresight`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-User-Id': user.uid,
      },
      body: JSON.stringify({
        question: question.trim(),
        claContext,
        signalsContext,
        newsContext,
      }),
    });

    if (!resp.ok) {
      const err = await resp.json().catch(() => ({ error: `HTTP ${resp.status}` }));
      throw new Error(err.error || `Request failed (${resp.status})`);
    }

    const data = await resp.json();

    // Persist to Firestore so the user can review later
    try {
      await NewsReactions.saveForesightQuery(question.trim(), data.answer);
    } catch (e) {
      console.warn('Failed to save foresight query to Firestore:', e);
    }

    return data;
  },

  /**
   * Build a cross-cutting insight from bookmarked articles
   * @param {Array<string>} bookmarkIds - Array of bookmark document IDs
   * @returns {Promise<Object>} { insight, model, usage, bookmarkCount }
   */
  async buildInsight(bookmarkIds) {
    if (!Array.isArray(bookmarkIds) || bookmarkIds.length === 0) {
      throw new Error('At least one bookmark is required');
    }

    const user = auth.currentUser;
    if (!user) throw new Error('Authentication required');

    // Fetch bookmark details from Firestore to send titles/categories to the API
    const bookmarks = [];
    for (const id of bookmarkIds) {
      try {
        const doc = await db.collection('news_bookmarks').doc(id).get();
        if (doc.exists) {
          bookmarks.push({ id: doc.id, ...doc.data() });
        }
      } catch (e) {
        console.warn(`Failed to fetch bookmark ${id}:`, e);
      }
    }

    if (bookmarks.length === 0) {
      throw new Error('No valid bookmarks found');
    }

    const resp = await fetch(`${this.workerBase}/api/foresight-builder`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-User-Id': user.uid,
      },
      body: JSON.stringify({ bookmarks }),
    });

    if (!resp.ok) {
      const err = await resp.json().catch(() => ({ error: `HTTP ${resp.status}` }));
      throw new Error(err.error || `Request failed (${resp.status})`);
    }

    return await resp.json();
  },

  /**
   * Render an AI answer into a container element with Markdown-like formatting
   * @param {string} answer - The answer text
   * @param {HTMLElement} container - DOM element to render into
   */
  renderAnswer(answer, container) {
    if (!container) return;

    // Clear previous content
    container.innerHTML = '';

    if (!answer) {
      container.innerHTML = '<p class="text-muted">No answer available.</p>';
      return;
    }

    // Split into paragraphs and apply basic formatting
    const paragraphs = answer.split('\n\n');
    paragraphs.forEach((para) => {
      const trimmed = para.trim();
      if (!trimmed) return;

      // Heading detection (## style)
      if (trimmed.startsWith('## ')) {
        const h = document.createElement('h4');
        h.className = 'foresight-heading mt-3 mb-2';
        h.textContent = trimmed.replace(/^##\s+/, '');
        container.appendChild(h);
        return;
      }

      // Bullet list detection
      if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
        const ul = document.createElement('ul');
        ul.className = 'foresight-list';
        const items = trimmed.split('\n').filter((line) => line.trim().startsWith('- ') || line.trim().startsWith('* '));
        items.forEach((item) => {
          const li = document.createElement('li');
          li.textContent = item.replace(/^[-*]\s+/, '');
          ul.appendChild(li);
        });
        container.appendChild(ul);
        return;
      }

      // Regular paragraph
      const p = document.createElement('p');
      p.className = 'foresight-paragraph';
      // Escape HTML first, then apply Markdown-like formatting
      const escaped = trimmed.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      p.innerHTML = escaped
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');
      container.appendChild(p);
    });
  },

  /**
   * Render a list of past foresight queries into a container
   * @param {Array} queries - Array from getForesightHistory()
   * @param {HTMLElement} container - DOM element to render into
   */
  renderHistory(queries, container) {
    if (!container) return;
    container.innerHTML = '';

    if (!queries || queries.length === 0) {
      container.innerHTML = '<p class="text-muted">No past queries.</p>';
      return;
    }

    queries.forEach((query) => {
      const card = document.createElement('div');
      card.className = 'foresight-history-card card mb-3';

      const header = document.createElement('div');
      header.className = 'card-header d-flex justify-content-between';

      const questionEl = document.createElement('strong');
      questionEl.textContent = query.question;
      header.appendChild(questionEl);

      if (query.createdAt) {
        const dateEl = document.createElement('small');
        dateEl.className = 'text-muted';
        dateEl.textContent = query.createdAt.toLocaleDateString('ja-JP');
        header.appendChild(dateEl);
      }

      const body = document.createElement('div');
      body.className = 'card-body';

      // Render the answer inside the card body
      this.renderAnswer(query.answer, body);

      card.appendChild(header);
      card.appendChild(body);
      container.appendChild(card);
    });
  },
};
