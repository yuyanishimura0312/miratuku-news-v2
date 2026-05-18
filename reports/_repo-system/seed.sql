-- =====================================================================
-- /repo design rules DB — 初期データ
--   themes: miratuku / esse-sense
--   tokens, rules, components, assets, templates
-- =====================================================================

-- ---------------------------------------------------------------------
-- THEMES
-- ---------------------------------------------------------------------
INSERT OR REPLACE INTO themes VALUES
('miratuku',  'ミラツク版',
 'NPO法人ミラツク標準。warm cream 紙地に wine 系アクセント。NOSIGNER 2011 公式マークを採用。',
 '#F5EBDC', '#5A2620', '#2A1F18', 'repo-miratuku.css', 'active', CURRENT_TIMESTAMP, NULL),
('essesense', 'esse-sense版',
 '株式会社 esse-sense 標準。赤白 CI を基軸とした純白紙地＋赤 (#CC1400) アクセント。公式ワードマークを採用。',
 '#FFFFFF', '#CC1400', '#121212', 'repo-essesense.css', 'active', CURRENT_TIMESTAMP, NULL);

-- ---------------------------------------------------------------------
-- DESIGN TOKENS — miratuku
-- ---------------------------------------------------------------------
INSERT OR REPLACE INTO design_tokens (theme_id, category, token_name, token_value, description) VALUES
('miratuku', 'color', '--pr-paper',          '#F5EBDC', 'warm cream 紙地'),
('miratuku', 'color', '--pr-paper-deep',     '#EFE3D0', 'リード/箱の基調 (やや深いクリーム)'),
('miratuku', 'color', '--pr-ink',            '#2A1F18', '主要文字色 (純黒禁止)'),
('miratuku', 'color', '--pr-ink-soft',       '#5B4A3F', 'メタ・ラベル'),
('miratuku', 'color', '--pr-ink-mute',       '#8A7868', 'フッター・ノート'),
('miratuku', 'color', '--pr-wine',           '#5A2620', '表紙ベース wine'),
('miratuku', 'color', '--pr-wine-deep',      '#3F1814', '表紙陰影'),
('miratuku', 'color', '--pr-wine-bright',    '#8B3A2E', 'アクセント'),
('miratuku', 'color', '--pr-wine-soft',      '#A04030', '文中強調'),
('miratuku', 'color', '--pr-terracotta',     '#F0DBC4', 'リード/引用箱'),
('miratuku', 'color', '--pr-terracotta-rim', '#C89478', '箱の左縦線'),
('miratuku', 'color', '--pr-gold',           '#C89478', '表紙バッジ/装飾'),
('miratuku', 'color', '--pr-cream',          '#E8D9C8', 'ダーク背景上の本文'),
('miratuku', 'typography', '--pr-font-jp-serif', '"Noto Serif JP", serif', '和文 (本文・タイトル・章タイトル)'),
('miratuku', 'typography', '--pr-font-lt-serif', '"Cormorant Garamond", serif', 'ラテン斜体 (章番号・英文副題)'),
('miratuku', 'typography', '--pr-font-lt-sans',  '"Inter", sans-serif', 'ラテン正体 (ラベル・小キャップ)'),
('miratuku', 'typography', '--pr-font-jp-sans',  '"Noto Sans JP", sans-serif', '和文 sans (メタ・フッター)');

-- ---------------------------------------------------------------------
-- DESIGN TOKENS — esse-sense
-- ---------------------------------------------------------------------
INSERT OR REPLACE INTO design_tokens (theme_id, category, token_name, token_value, description) VALUES
('essesense', 'color', '--pr-paper',          '#FFFFFF', '純白紙地'),
('essesense', 'color', '--pr-paper-deep',     '#FFFFFF', '純白固定 (off-white 不使用)'),
('essesense', 'color', '--pr-ink',            '#121212', 'メイン文字色 (黒)'),
('essesense', 'color', '--pr-ink-soft',       '#444444', '副次文字色'),
('essesense', 'color', '--pr-ink-mute',       '#6B6B6B', 'メタ・補助文字'),
('essesense', 'color', '--pr-wine',           '#CC1400', '赤白CI 主役色'),
('essesense', 'color', '--pr-wine-deep',      '#A01000', 'hover/濃赤'),
('essesense', 'color', '--pr-wine-bright',    '#CC1400', 'アクセント (同 #CC1400)'),
('essesense', 'color', '--pr-wine-soft',      '#B01200', '文中強調'),
('essesense', 'color', '--pr-terracotta',     '#FFFFFF', 'リード/引用箱 = 純白'),
('essesense', 'color', '--pr-terracotta-rim', 'rgba(18,18,18,0.18)', '枠線 (rgba 黒)'),
('essesense', 'color', '--pr-gold',           '#CC1400', 'バッジ等 = 赤'),
('essesense', 'color', '--pr-cream',          '#FFFFFF', 'ダーク背景代替 = 白'),
('essesense', 'typography', '--pr-font-jp-serif', '"Noto Serif JP", serif', '和文 (本文・タイトル)'),
('essesense', 'typography', '--pr-font-lt-serif', '"Inter", serif', 'ラテン italic は Inter で代替 (Cormorant 不使用)'),
('essesense', 'typography', '--pr-font-lt-sans',  '"Inter", sans-serif', 'ラテン正体'),
('essesense', 'typography', '--pr-font-jp-sans',  '"Noto Sans JP", sans-serif', '和文 sans');

-- ---------------------------------------------------------------------
-- DESIGN RULES
-- ---------------------------------------------------------------------

-- 共通ルール (theme_id NULL)
INSERT OR IGNORE INTO design_rules (theme_id, category, rule_text, rationale, enforcement, source) VALUES
(NULL, 'layout',     'A4 (210×297mm) を 1 ページ単位とし、表紙 + 内容 11–15 ページ程度に収める。', 'PDF 印刷時の見開き整合性を保つため。', 'must', 'progress-report-style.md'),
(NULL, 'layout',     '各章タイトル直下に pr-lead を必置する。', '導入文で章の主旨を 200-300 字で示すと読者の理解が高速化する。', 'should', 'progress-report-style.md'),
(NULL, 'layout',     '段落は両端揃え + 1em インデントとする。', '伝統的な明朝組版に近づける。', 'must', 'progress-report-style.md'),
(NULL, 'content',    '章番号は 01-99 の 2 桁ゼロ埋め表記とする。', '視覚的に整列し、章順序を即座に把握できる。', 'must', 'progress-report-style.md'),
(NULL, 'content',    '段落内の強調は <strong> ではなく .pr-hl クラスを使用する。', 'インライン強調をカラーで表現するため。', 'should', 'progress-report-style.md'),
(NULL, 'content',    '「らしい」「近年」「ある研究によれば」等の曖昧表現を禁止する。', '一次資料を遡れる記述に統一する。', 'must', 'journal-essay-style.md'),
(NULL, 'content',    '年代は西暦 4 桁で書く。元号・「最近」は使わない。', '将来読み返したときも年代が確定する。', 'must', 'journal-essay-style.md'),
(NULL, 'typography', '絵文字・アイコンフォントを使用しない。', '紙物としての品位を保つ。', 'must', 'db-design-system.md'),
(NULL, 'branding',   'ロゴはテーマで定義された公式アセットのみを使用する。', '非公式ロゴ・代替記号を排除する。', 'must', NULL),
(NULL, 'branding',   '純白 (#FFFFFF) または theme の base_color のみを背景に用いる。', '中間色 (off-white) の散発を防ぐ。', 'must', NULL),
(NULL, 'layout',     'pr-quote-dark (黒帯引用) は使用しない。', '紙面の重さを避け、本文の集中を保つ。', 'must', NULL);

-- miratuku 固有ルール
INSERT OR IGNORE INTO design_rules (theme_id, category, rule_text, rationale, enforcement, source) VALUES
('miratuku', 'color',  '紙地は warm cream (#F5EBDC) で固定。純白は使わない。',                     '紙の温度感を保ち、書籍的な読み心地に近づける。', 'must', 'progress-report-style.md'),
('miratuku', 'color',  'インクは warm dark (#2A1F18) 固定。純黒 (#000000) は使わない。',          '紙地と調和するため。',                         'must', 'progress-report-style.md'),
('miratuku', 'color',  'アクセントは wine 系 (#5A2620 / #8B3A2E)。鮮赤 (#CC1400) を主役にしない。', 'esse-sense との分離のため。',                  'must', 'progress-report-style.md'),
('miratuku', 'branding','フッター組織表記は「NPO法人ミラツク」を用いる。',                          '法人名表記を統一する。',                        'must', NULL);

-- esse-sense 固有ルール
INSERT OR IGNORE INTO design_rules (theme_id, category, rule_text, rationale, enforcement, source) VALUES
('essesense', 'color',  '紙地は純白 (#FFFFFF) 固定。off-white (#F7F7F5 等) を使わない。',         '白か黒の二元構成で清潔感を保つ。',                                      'must', NULL),
('essesense', 'color',  'インクは #121212 系。アクセントは #CC1400 のみ。',                       '赤白 CI 規範。',                                                       'must', 'db-design-system.md'),
('essesense', 'color',  'ページトップに赤 6px (cover) / 黒 3px (内ページ) のボーダーを置く。',     'CI のトップバーを再現する。',                                          'must', NULL),
('essesense', 'branding','ロゴは公式 2 段組ワードマーク (assets/esse-sense-wordmark.png) のみ使用。', 'テキスト wordmark spans は重複排除のため非表示。',                       'must', NULL),
('essesense', 'typography','Cormorant Garamond は使わず Inter italic で代替する。',               'esse-sense のタイポ規範に整合させる。',                                'must', NULL);

-- ---------------------------------------------------------------------
-- COMPONENTS
-- ---------------------------------------------------------------------
INSERT OR REPLACE INTO components VALUES
('cover',           '表紙', '提出先・タイトル・日付を表示する 1 ページ目', 'pr-cover',
 '["badge_tag","badge_date","eyebrow","title","subtitle_en"]',
 '["org_name","contact_email","cover_logo_path"]',
 '<section class="pr-cover">...</section>', NULL),

('page',            '内ページ', '章の本文を載せる A4 1 枚', 'pr-page',
 '["page_num","page_total","header_meta","body_html"]',
 '["footer_brand","footer_jp"]',
 '<section class="pr-page">...</section>', NULL),

('chapter',         '章ヘッダー', '章番号 + タイトル + 英文サブ + 区切り線', 'pr-chapter',
 '["chapter_num","title_jp","title_en"]', '[]',
 '<article class="pr-chapter">...</article>', NULL),

('lead',            'リード文', '章導入の散文ブロック', 'pr-lead',
 '["body"]', '["title"]',
 '<div class="pr-lead"><p>...</p></div>', NULL),

('lead-titled',     '見出し付きリード', '見出し + dt/dd の要旨表', 'pr-lead-titled',
 '["head","items"]', '[]',
 '<div class="pr-lead-titled">...</div>', 'items は [{dt, dd}, ...]'),

('toc',             '目次', '章リスト + 該当ページ番号', 'pr-toc-list',
 '["items"]', '[]',
 '<ul class="pr-toc-list">...</ul>', 'items は [{num, title, page}, ...]'),

('q-box',           '問いボックス', '読者の問い・前提条件を強調', 'pr-q-box',
 '["label","body"]', '[]',
 '<div class="pr-q-box">...</div>', NULL),

('info-card-grid',  '情報カード 2 カラム', '対比的な 2 つの情報を並列表示', 'pr-info-grid',
 '["left","right"]', '[]',
 '<div class="pr-info-grid">...</div>', 'left/right は {label, value, meta}'),

('stat-strip',      '統計ストリップ', '数値指標を横一列で並べる', 'pr-stat-strip',
 '["items"]', '[]',
 '<div class="pr-stat-strip">...</div>', 'items は [{num, label}, ...]'),

('qa-block',        'Q&A 風ブロック', 'タイトル + 目的 + 本文', 'pr-qa-block',
 '["title","body"]', '["aim","chars"]',
 '<div class="pr-qa-block">...</div>', NULL),

('score-table',     'スコア表', '評価軸 × スコア × バー', 'pr-score-table',
 '["rows"]', '[]',
 '<table class="pr-score-table">...</table>', 'rows は [{axis, weight, score, pct}, ...]'),

('researcher-card', '研究者カード', '番号 + 氏名 + 所属 + テーマ + コメント', 'pr-researcher-card',
 '["rank","name","affil","theme","note"]', '["sim"]',
 '<div class="pr-researcher-card">...</div>', NULL),

('quote-light',     '引用 (light)', '本文中の補助引用', 'pr-quote-light',
 '["body"]', '["attr"]',
 '<blockquote class="pr-quote-light">...</blockquote>', NULL),

('disclaimer',      '免責ブロック', '末尾の利用条件・免責文', 'pr-disclaimer-block',
 '["body"]', '["title"]',
 '<div class="pr-disclaimer-block">...</div>', NULL),

('sign',            '署名', '末尾の発行体名・連絡先', 'pr-sign',
 '["org_name"]', '["date","name","role","contact"]',
 '<div class="pr-sign">...</div>', NULL);

-- ---------------------------------------------------------------------
-- ASSETS
-- ---------------------------------------------------------------------
INSERT OR REPLACE INTO assets VALUES
('miratuku-mark',          'miratuku',  'logo',
 'https://journal.emerging-future.org/shared/progress-report/assets/miratuku-mark.png',
 'NOSIGNER 2011 ミラツク CI 正規マーク (カラー、内ページヘッダー用)',
 'cover-top:32px / header:28px / cover-art:200px'),
('miratuku-mark-white',    'miratuku',  'logo',
 'https://journal.emerging-future.org/shared/progress-report/assets/miratuku-mark-white.png',
 'NOSIGNER 白マーク (ダーク背景上の表示用)',
 'cover-top:32px'),
('miratuku-logo',          'miratuku',  'logo',
 'https://journal.emerging-future.org/shared/progress-report/assets/miratuku-logo.png',
 'NOSIGNER フルロゴ (マーク + ワードマーク縦組)',
 'cover-art:200px'),
('esse-sense-wordmark',    'essesense', 'logo',
 'assets/esse-sense-wordmark.png',
 '株式会社 esse-sense 公式 2 段組ワードマーク',
 'cover-top:32px / header:28px / cover-art:200px');

-- ---------------------------------------------------------------------
-- REPORT TEMPLATES
-- ---------------------------------------------------------------------
INSERT OR REPLACE INTO report_templates VALUES
('advisory-report-default',
 'アドバイザリーレポート (既定 11 ページ)',
 'templates/report.html',
 '事業・研究領域への助言を表紙 + 5 章 (要旨 / 問いの理解 / 学術理解 / 事業検討 / 共同研究) + 利用について の構成で出す。',
 11,
 'バイオものづくり進出戦略レポートで初出。/repo の既定テンプレート。');
