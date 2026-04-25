// Shared data loader — fetches from Future Insight App data pipeline
const DataLoader = {
  base: SHARED_DATA_BASE,
  cache: {},

  // Fetch with cache busting
  async fetch(filename) {
    const v = Date.now();
    const url = `${this.base}/${filename}?v=${v}`;
    const resp = await fetch(url);
    if (!resp.ok) throw new Error(`Failed to load ${filename}: ${resp.status}`);
    return resp.json();
  },

  // Cached fetch — only re-fetches if older than maxAge (ms)
  async fetchCached(filename, maxAge = 300000) {
    const cached = this.cache[filename];
    if (cached && Date.now() - cached.time < maxAge) return cached.data;
    const data = await this.fetch(filename);
    this.cache[filename] = { data, time: Date.now() };
    return data;
  },

  // Core data loaders
  async loadNews() {
    return this.fetchCached('latest.json');
  },

  async loadAIAnalysis() {
    return this.fetchCached('ai_analysis.json');
  },

  async loadPapersLight() {
    return this.fetchCached('papers_light.json', 600000);
  },

  async loadDailyPapers() {
    return this.fetchCached('daily_papers.json');
  },

  async loadPaperAlerts() {
    return this.fetchCached('paper_alerts.json');
  },

  async loadAlerts() {
    return this.fetchCached('alerts.json');
  },

  async loadScenarios() {
    return this.fetchCached('scenarios.json');
  },

  async loadPestleHistory() {
    return this.fetchCached('pestle_history.json', 600000);
  },

  async loadPestleIndex() {
    return this.fetchCached('pestle_index.json');
  },

  async loadPapersStats() {
    return this.fetchCached('papers_stats.json');
  },

  // Load all core data in parallel
  async loadAll() {
    const [news, ai, dailyPapers, alerts, paperAlerts] = await Promise.all([
      this.loadNews(),
      this.loadAIAnalysis(),
      this.loadDailyPapers(),
      this.loadAlerts(),
      this.loadPaperAlerts(),
    ]);
    return { news, ai, dailyPapers, alerts, paperAlerts };
  },

  // Load news-app specific data (from miratuku-news repo)
  async loadNewsAppData(filename) {
    const newsBase = location.origin + location.pathname.replace(/[^/]*$/, '') + 'data';
    const v = Date.now();
    const resp = await fetch(`${newsBase}/${filename}?v=${v}`);
    if (!resp.ok) throw new Error(`Failed to load ${filename}: ${resp.status}`);
    return resp.json();
  },
};
