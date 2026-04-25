// Shared i18n module — bilingual support for Miratuku apps
let LANG = localStorage.getItem('miratuku_lang') || 'ja';

const i18n = {
  ja: {
    // Navigation
    nav_home: 'ホーム',
    nav_pestle: 'PESTLEニュース',
    nav_academic: '学術研究',
    nav_cla: '因果階層分析',
    nav_foresight: '未来洞察',
    nav_bookmarks: 'ブックマーク',
    nav_history: '履歴',
    nav_media: 'メディアソース',
    nav_guide: '使い方',

    // Region toggle
    region_japan: '日本版',
    region_global: 'グローバル版',

    // PESTLE categories
    pestle_P: '政治',
    pestle_E: '経済',
    pestle_S: '社会',
    pestle_T: '技術',
    pestle_L: '法律',
    pestle_En: '環境',

    // Academic fields
    field_natural: '自然科学',
    field_engineering: '工学',
    field_social: '社会科学',
    field_humanities: '人文学',
    field_arts: '芸術',

    // CLA layers
    cla_litany: 'リタニー（表層事象）',
    cla_systemic: '社会的原因（構造）',
    cla_worldview: 'ディスコース（世界観）',
    cla_myth: '神話・メタファー（深層）',

    // Actions
    action_bookmark: 'ブックマーク',
    action_comment: 'コメントする',
    action_ask: '問いかける',
    action_search: '検索',
    action_filter: 'フィルタ',
    action_load_more: 'もっと読む',

    // Reports
    report_daily: '本日の分析レポート',
    report_meta: 'メタ分析レポート',
    report_myth: '神話の変遷と現在の状況',

    // Time
    today: '今日',
    this_week: '今週',
    this_month: '今月',
    all_time: '全期間',

    // Auth
    login: 'ログイン',
    signup: '新規登録',
    logout: 'ログアウト',
    email: 'メールアドレス',
    password: 'パスワード',

    // Status
    loading: '読み込み中...',
    no_data: 'データがありません',
    error: 'エラーが発生しました',
    saved: '保存しました',

    // Media sources
    media_list: 'メディアソース一覧',
    media_name: 'メディア名',
    media_field: '分野',
    media_count: '収集件数',
    media_last: '最終取得',
    media_add: 'メディアを追加',
  },
  en: {
    nav_home: 'Home',
    nav_pestle: 'PESTLE News',
    nav_academic: 'Academic Research',
    nav_cla: 'Causal Layered Analysis',
    nav_foresight: 'Foresight',
    nav_bookmarks: 'Bookmarks',
    nav_history: 'History',
    nav_media: 'Media Sources',
    nav_guide: 'Guide',

    region_japan: 'Japan',
    region_global: 'Global',

    pestle_P: 'Political',
    pestle_E: 'Economic',
    pestle_S: 'Social',
    pestle_T: 'Technological',
    pestle_L: 'Legal',
    pestle_En: 'Environmental',

    field_natural: 'Natural Sciences',
    field_engineering: 'Engineering',
    field_social: 'Social Sciences',
    field_humanities: 'Humanities',
    field_arts: 'Arts',

    cla_litany: 'Litany (Surface Events)',
    cla_systemic: 'Systemic Causes (Structure)',
    cla_worldview: 'Discourse (Worldview)',
    cla_myth: 'Myth / Metaphor (Deep Layer)',

    action_bookmark: 'Bookmark',
    action_comment: 'Comment',
    action_ask: 'Ask',
    action_search: 'Search',
    action_filter: 'Filter',
    action_load_more: 'Load More',

    report_daily: "Today's Analysis Report",
    report_meta: 'Meta-Analysis Report',
    report_myth: 'Myth Transition & Current Situation',

    today: 'Today',
    this_week: 'This Week',
    this_month: 'This Month',
    all_time: 'All Time',

    login: 'Login',
    signup: 'Sign Up',
    logout: 'Logout',
    email: 'Email',
    password: 'Password',

    loading: 'Loading...',
    no_data: 'No data available',
    error: 'An error occurred',
    saved: 'Saved',

    media_list: 'Media Sources',
    media_name: 'Name',
    media_field: 'Field',
    media_count: 'Articles',
    media_last: 'Last Fetched',
    media_add: 'Add Media',
  }
};

function t(key) {
  return (i18n[LANG] || i18n['ja'])[key] || (i18n['ja'])[key] || key;
}

function setLang(lang) {
  LANG = lang;
  localStorage.setItem('miratuku_lang', lang);
}
