-- =====================================================================
-- /repo system — Knowledge Consolidation Extension (2026-05-18)
--
-- 既存 5 正本ルールから抽出した知見を統合：
--   - journal-essay-style.md       (ep007 連載エッセイ正本)
--   - journal-series-template.md   (連載トップ + 各記事ページ規範)
--   - notation-style.md            (表記スタイル: 数字・アルファベット・カタカナ)
--   - db-design-system.md          (赤白CI textbook.html 教科書スタイル)
--   - series-db-operations.md      (連載DB運営: 必須登録項目)
-- =====================================================================

-- ---------------------------------------------------------------------
-- NEW THEMES
-- ---------------------------------------------------------------------
INSERT OR REPLACE INTO themes VALUES
('ep007', 'ep007連載エッセイ版',
 'emerging-future.org 連載 (kurashi/keiei/henka/jigyo/itonami/futures) の正本型。純白紙地 + 赤アクセント (#FF3644) + Judson + Noto Serif JP + drop cap + サイドバーTOC。journal-essay-style.md 準拠。',
 '#FFFFFF', '#FF3644', '#1A1A1A', 'repo-ep007.css', 'active', CURRENT_TIMESTAMP, NULL),
('textbook', '教科書・ダッシュボード版',
 '赤白CI textbook.html スタイル。上部固定 top-bar (3px黒) + 左サイドバーTOC + メインカラム max-width 740-760px。ダーク/ライト切替対応。db-design-system.md 準拠。',
 '#FFFFFF', '#CC1400', '#121212', 'repo-textbook.css', 'active', CURRENT_TIMESTAMP, NULL);

-- ---------------------------------------------------------------------
-- DESIGN TOKENS — ep007
-- ---------------------------------------------------------------------
INSERT OR REPLACE INTO design_tokens (theme_id, category, token_name, token_value, description) VALUES
('ep007', 'color', '--ep-paper',       '#FFFFFF', '純白紙地'),
('ep007', 'color', '--ep-ink',         '#1A1A1A', '本文文字色'),
('ep007', 'color', '--ep-ink-soft',    '#4A4A4A', 'メタ・キャプション'),
('ep007', 'color', '--ep-ink-mute',    '#8A8A8A', 'TOC補助・disclaimer'),
('ep007', 'color', '--ep-accent',      '#FF3644', 'kurashi系アクセント赤'),
('ep007', 'color', '--ep-accent-deep', '#CC1400', '濃赤 (esse-sense CI 互換)'),
('ep007', 'color', '--ep-rule',        'rgba(26,26,26,0.12)', '罫線'),
('ep007', 'typography', '--ep-font-display', '"Judson", "Noto Serif JP", serif', 'hero/num/英文タイトル'),
('ep007', 'typography', '--ep-font-body',    '"Noto Serif JP", serif', '本文散文 (17px / lh 2.1)'),
('ep007', 'typography', '--ep-font-ui',      '"Noto Sans JP", sans-serif', 'meta/nav/footer'),
('ep007', 'spacing', '--ep-paragraph-gap',   '30px', '段落間'),
('ep007', 'spacing', '--ep-text-indent',     '1em',  '段落 indent'),
('ep007', 'spacing', '--ep-line-height',     '2.1',  '本文行間'),
('ep007', 'spacing', '--ep-drop-cap-size',   '4.4em','drop cap サイズ');

-- ---------------------------------------------------------------------
-- DESIGN TOKENS — textbook
-- ---------------------------------------------------------------------
INSERT OR REPLACE INTO design_tokens (theme_id, category, token_name, token_value, description) VALUES
('textbook', 'color', '--tb-paper',         '#FFFFFF', '白基調'),
('textbook', 'color', '--tb-paper-dark',    '#121212', 'ダークモード背景'),
('textbook', 'color', '--tb-surface',       '#F7F7F5', 'カード hover/サイドバー背景'),
('textbook', 'color', '--tb-ink',           '#121212', '主要文字色'),
('textbook', 'color', '--tb-ink-soft',      '#555555', '副次文字色'),
('textbook', 'color', '--tb-accent',        '#CC1400', '赤白CI 主役色'),
('textbook', 'color', '--tb-rule',          '#D9D9D9', '罫線'),
('textbook', 'color', '--tb-rule-light',    '#EEEEEE', '薄い罫線'),
('textbook', 'typography', '--tb-font-body',    '"Noto Serif JP", "Hiragino Mincho ProN", Georgia, serif', '本文 (日本語可読性優先)'),
('textbook', 'typography', '--tb-font-ui',      '"Noto Sans JP", "Hiragino Sans", -apple-system, sans-serif', 'UI / TOC'),
('textbook', 'typography', '--tb-font-mono',    '"SF Mono", "Fira Code", monospace', '章番号'),
('textbook', 'spacing', '--tb-content-max',     '760px', 'メインカラム最大幅'),
('textbook', 'spacing', '--tb-sidebar-width',   '260px', 'サイドバー幅'),
('textbook', 'spacing', '--tb-line-height',     '1.85',  '本文行間'),
('textbook', 'spacing', '--tb-letter-spacing',  '0.025em', '字間');

-- ---------------------------------------------------------------------
-- NEW COMPONENTS
-- ---------------------------------------------------------------------
INSERT OR REPLACE INTO components VALUES
('ep-hero',          'EP Hero', '連載各話の開幕ブロック', 'ep-hero',
 '["eyebrow","ep_num","ep_total","title","subtitle_dash","title_en","lead"]',
 '["meta"]',
 '<section class="ep-hero">...</section>',
 'eyebrow は PART/カテゴリ表示。subtitle は「― ...」始まり必須。lead 200-320字'),

('drop-cap-paragraph','Drop Cap 段落', '本文の最初の段落（drop cap 付き）', 'ep-body__first',
 '["body"]', '[]',
 '<p class="ep-body__first">...</p>',
 'Judson 4.4em のイニシャル文字'),

('signal-list',      'SIGNAL リスト', 'DEEPER 末尾の数値根拠 3-4 項目', 'signal-list',
 '["items"]', '[]',
 '<div class="signal-list">...</div>',
 '各 SIGNAL に <strong> で数値強調を必置。書誌略記を括弧内に'),

('key-reference',    'KEY REFERENCE', '5-8 件の典拠リスト', 'ref-list',
 '["references"]', '[]',
 '<ul class="ref-list">...</ul>',
 'top-tier 論文 ≥4 件、和文一次文献 ≥1 件、DOI/URL 必須'),

('question-for-next','QUESTION FOR NEXT', '次号への問い + NEXT EPISODE', 'ep-question',
 '["question_body","next_num","next_title"]', '["next_href"]',
 '<section class="ep-question">...</section>', NULL),

('ep-nav',           'EP Navigation', 'PREV/NEXT 章ナビ', 'ep-nav',
 '["prev_num","prev_title","next_num","next_title"]', '["prev_disabled","next_disabled"]',
 '<nav class="ep-nav">...</nav>', NULL),

('ep-actions',       'EP Actions', '3 ボタン (メルマガ/感想/地図)', 'ep-actions',
 '["actions"]', '[]',
 '<section class="ep-actions">...</section>', 'actions は [{label, href, primary}, ...]'),

('site-header-jp',   '連載 site-header', 'sticky ヘッダー (brand + nav)', 'site-header',
 '["brand_name","nav_items"]', '[]',
 '<header class="site-header">...</header>', NULL),

('site-footer-jp',   '連載 site-footer', '4列フッター + disclaimer', 'site-footer',
 '["columns","disclaimer","year"]', '[]',
 '<footer class="site-footer">...</footer>', '4 columns: ABOUT/NAVIGATION/MIRA TUKU/SOURCE'),

('toc-sidebar',      'TOC サイドバー', '連載/教科書の章リスト + 現在地ハイライト', 'toc-sidebar',
 '["sections","current_index"]', '[]',
 '<aside class="toc-sidebar">...</aside>', NULL),

('toc-fab',          'モバイル目次ボタン', '小画面向けの開閉トリガ', 'toc-fab',
 '[]', '[]',
 '<button class="toc-fab">目次</button>', NULL),

('top-bar',          '教科書上部バー', '上部固定 48px + 黒3pxボーダー + テーマ切替', 'top-bar',
 '["brand_name"]', '["theme_toggle"]',
 '<div class="top-bar">...</div>', NULL),

('chapter-section',  '教科書 章ブロック', '章本体 (border-bottom 区切り)', 'chapter-section',
 '["chapter_num","title","body_html"]', '["chapter_en"]',
 '<section class="chapter-section">...</section>', 'margin-bottom 64-80px'),

('newsletter-form',  'メルマガ登録フォーム', '2 ステップフォーム', 'newsletter',
 '["title","desc"]', '["consent_text"]',
 '<section class="newsletter">...</section>', NULL),

('skip-link',        'Skip Link', 'アクセシビリティ: 本文へスキップ', 'skip-link',
 '[]', '["target"]',
 '<a class="skip-link" href="#articleBody">本文へスキップ</a>', NULL),

('read-progress',    '読書プログレスバー', '上部固定の読み進み可視化', 'read-progress',
 '[]', '[]',
 '<div class="read-progress"><div class="read-progress-bar"></div></div>', NULL);

-- ---------------------------------------------------------------------
-- NEW REPORT TEMPLATES
-- ---------------------------------------------------------------------
INSERT OR REPLACE INTO report_templates VALUES
('journal-essay-ep007',
 '連載エッセイ (ep007型)',
 'templates/journal-essay-ep007.html',
 'emerging-future.org 連載の各話。hero + 6段落散文 + DEEPER + signal-list + KEY REFERENCE + QUESTION + ep-nav。2,500-3,500字。',
 1,
 'kurashi/keiei/henka/jigyo/itonami/futures で共通。/essay コマンドからも呼ばれる'),
('series-top',
 '連載トップページ',
 'templates/series-top.html',
 '連載シリーズの入口 (hero + intro + featured + parts-overview + newsletter + footer)。journal-series-template.md 準拠。',
 1,
 NULL),
('textbook',
 '教科書・大規模解説 HTML',
 'templates/textbook.html',
 'top-bar + サイドバーTOC + メインカラム (max-width 760px)。章構造・ダークモード対応。db-design-system.md 準拠。',
 1,
 '2万字以上の解説に推奨'),
('dashboard',
 'ダッシュボード HTML',
 'templates/dashboard.html',
 '集計クエリ + SVG 図解 + サイドバー目次。赤白CI 準拠。',
 1,
 'DBプロジェクトの可視化に推奨');

-- ---------------------------------------------------------------------
-- NEW DESIGN RULES — 共通 (notation-style.md, journal-essay-style.md 抜粋)
-- ---------------------------------------------------------------------
INSERT OR IGNORE INTO design_rules (theme_id, category, rule_text, rationale, enforcement, source) VALUES
-- 表記スタイル
(NULL, 'content', '数字はアラビア数字 (1, 2, 3) を使う。漢数字 (一、二、三) は禁止。慣用 (一方/第一に/三幕構成 等) のみ例外。', '読みづらさと誤読を防ぐ。', 'must', 'notation-style.md'),
(NULL, 'content', 'アルファベットは固有名・標準語彙 (ORCID/DOI/SQL 等) のみに限定し、記述レベルの英語 (API/ETL/SaaS 等) は日本語に翻訳する。', '日本語文章としての完成度。「業界既出語」を避ける。', 'must', 'notation-style.md'),
(NULL, 'content', 'カタカナ専門用語 3 連続以上は日本語化を検討する。', '読み手の認知負荷を下げる。', 'should', 'notation-style.md'),
-- 文体規範
(NULL, 'content', '「考えられる／示唆される／観測される」は同一段落内で合計 1 回まで。観測事実 + 年代 + 主体で断定する。', '断定回避が形骸化すると説得力が落ちる。', 'should', 'journal-essay-style.md'),
(NULL, 'content', '横文字専門用語の初出時は日本語の説明を添える (例: 近接学/身体化認知)。', '読者用語ポリシー。', 'must', 'journal-essay-style.md'),
(NULL, 'content', '数値は媒体まで遡る。「ある研究によれば 30%」ではなく「2007年の J Consumer Research 誌の実験で 30% (Meyers-Levy & Zhu, 2007, 34(2): 174-186)」。', '一次資料を遡れる記述に統一。', 'must', 'journal-essay-style.md'),
(NULL, 'content', '著者所属は初出で記載 (米ミネソタ大学のジョーン・マイヤーズ＝レヴィは…)。', '権威性と再現性。', 'should', 'journal-essay-style.md'),
(NULL, 'branding', '本文中に日本人研究者 ≥1名 + DEEPER に ≥1名 = 計 ≥2名を必置。', '文化バランス三原則。', 'must', 'journal-essay-style.md'),
(NULL, 'branding', '少なくとも 1 名の日本人研究者は議論の核を担う (脚注的引用ではない)。', '西洋偏重是正。', 'must', 'journal-essay-style.md'),
(NULL, 'content', '日本独自概念 (「間」「いき」「もったいない」「気」「みち」「侘び・寂び」「縁」「場」等) を論理展開の駆動軸に組み込む。', '日本発の理論・知見の提示。', 'should', 'journal-essay-style.md');

-- ---------------------------------------------------------------------
-- NEW DESIGN RULES — ep007 固有 (連載エッセイ)
-- ---------------------------------------------------------------------
INSERT OR IGNORE INTO design_rules (theme_id, category, rule_text, rationale, enforcement, source) VALUES
('ep007', 'layout',     'hero lead は 200-320字／本文散文は 1,100-1,300字／6段落／DEEPER 200-300字／signal-list 3-4項目／KEY REFERENCE 5-8件。', '記事規模の標準化。', 'must', 'journal-essay-style.md'),
('ep007', 'layout',     '本文は必ず 6 段落構成 (経験→文化→身体→提案→哲学→結語)。', '読者の流れを設計する。', 'must', 'journal-essay-style.md'),
('ep007', 'layout',     '最初の段落のみ drop cap (Judson 4.4em) を付与。他段落は text-indent 1em。', '紙物の格を出す。', 'must', 'journal-essay-style.md'),
('ep007', 'content',    'タイトルは命題的・動詞を含む宣言形。「〜について／〜とは／〜を考える」等の説明的タイトル禁止。', '読者の前提を反転させる切れ味。', 'must', 'journal-essay-style.md'),
('ep007', 'content',    '結論段落 (6段落目) は「問いを開く」OR「既存常識を反転させる」で終える。「バランス／再考／重要／これからが大事」等の凡庸結語禁止。両論併記禁止。', 'コミットメントある結末。', 'must', 'journal-essay-style.md'),
('ep007', 'content',    'KEY REFERENCE 5-8件のうち最低 4 件は top-tier journal の原著論文。レビュー論文・一般向け著作は最大 2 件まで。日本語一次文献 (岩波/東大出版会/講談社学術文庫/みすず書房 等) ≥1件。', '典拠の権威性確保。', 'must', 'journal-essay-style.md'),
('ep007', 'content',    'SIGNAL 各項に <strong> で数値強調を必置。書誌略記 (著者, 年, 誌名 巻号: ページ) を括弧内に。', '数値根拠の明示。', 'must', 'journal-essay-style.md'),
('ep007', 'content',    'DEEPER は時代・人で「決定的瞬間」を冒頭に固定 (例: 1984年にロジャー・S・ウルリックが…)。', '学術的厚みを最初に置く。', 'should', 'journal-essay-style.md'),
('ep007', 'content',    '段落内強調は <strong> のみ。<em> は使わない。', 'タイポ統制。', 'must', 'journal-essay-style.md'),
('ep007', 'content',    'QUESTION FOR NEXT は今回の終点 → 次号入口の橋渡し 1 段落で書く。', '次号への接続。', 'must', 'journal-essay-style.md'),
('ep007', 'typography', '本文は font-size 17px / line-height 2.1 / text-indent 1em / margin-bottom 30px。', '読みやすさ最優先。', 'must', 'journal-essay-style.md'),
('ep007', 'typography', '英文一文は Judson 18px italic。直訳でなく英語として独立で読める形に。', 'グローバル可読性。', 'should', 'journal-essay-style.md'),
('ep007', 'layout',     '推定読了時間を 5-6 分 (字数 / 250-300) で実計算して表示する。', '読者の意思決定を助ける。', 'must', 'journal-essay-style.md'),
('ep007', 'content',    '「らしい／のようだ／だろう」は禁止用語。', '一次資料に基づく断定。', 'must', 'journal-essay-style.md'),
('ep007', 'content',    '年代は西暦4桁。元号・「最近／近年」禁止。', '将来読み返したときも年代が確定する。', 'must', 'journal-essay-style.md');

-- ---------------------------------------------------------------------
-- NEW DESIGN RULES — textbook 固有 (教科書・ダッシュボード)
-- ---------------------------------------------------------------------
INSERT OR IGNORE INTO design_rules (theme_id, category, rule_text, rationale, enforcement, source) VALUES
('textbook', 'layout',     '上部固定 top-bar (高さ 48px) + 上端 3px 黒ボーダー + ブランド左 + ダーク/ライト切替右。', '赤白CI 体裁の固定。', 'must', 'db-design-system.md'),
('textbook', 'layout',     '2 カラム構成: 左 toc-sidebar (220-280px) + 右 main (max-width 740-760px)。', '本文中心の読みやすさ。', 'must', 'db-design-system.md'),
('textbook', 'layout',     '章単位は chapter-section (margin-bottom 64-80px / border-bottom 区切り)。', '視認的な章区切り。', 'must', 'db-design-system.md'),
('textbook', 'typography', '本文は Noto Serif JP / line-height 1.85-1.95 / letter-spacing 0.025em / font-feature-settings "palt"。段落は text-indent 1em (first-of-type のみ 0)。', '日本語明朝の組版精度。', 'must', 'db-design-system.md'),
('textbook', 'color',      '紙地 #FFFFFF / インク #121212 / accent-warm #CC1400 を主軸。派手色 (青/緑/紫) を主役にしない。', '赤白CI 統一。', 'must', 'db-design-system.md'),
('textbook', 'layout',     'data-theme 属性によるダーク/ライト切替 + localStorage 永続化を実装する。', '長時間読書への配慮。', 'should', 'db-design-system.md'),
('textbook', 'layout',     '@media print でサイドバーを非表示にする。', '印刷時の本文集中。', 'must', 'db-design-system.md'),
('textbook', 'layout',     'モバイル (<1000px) はサイドバーを上部展開へ切り替える。', 'レスポンシブ。', 'should', 'db-design-system.md'),
('textbook', 'branding',   'favicon は https://esse-sense.com/favicon.ico を必置。', 'ブランド統一。', 'must', 'db-design-system.md'),
('textbook', 'typography', '章番号は SF Mono / Fira Code 等のモノスペース。', '番号視認性。', 'should', 'db-design-system.md');

-- ---------------------------------------------------------------------
-- DESIGN RULES — 連載DB運営 (series-db-operations.md 抜粋)
-- ---------------------------------------------------------------------
INSERT OR IGNORE INTO design_rules (theme_id, category, rule_text, rationale, enforcement, source) VALUES
(NULL, 'content', '連載エッセイを公開する際は series.db に episodes/episode_body/body_citations/deeper_body/deeper_citations/key_references を同一トランザクションで記録する。', '連載運営の必須登録。', 'must', 'series-db-operations.md'),
(NULL, 'content', '修正時は edit_history に before/after_text + edit_reason、新 episode_versions に snapshot を残す。', '編集履歴の追跡可能性。', 'must', 'series-db-operations.md'),
(NULL, 'content', '修正の理由・パターンを edit_principles として学習・蓄積する (applied_count ≥10 ∧ success_rate ≥0.8 で established 昇格)。', '編集方針の継続改善。', 'should', 'series-db-operations.md');

-- ---------------------------------------------------------------------
-- ASSETS — 連載共通 (series-style.css 等)
-- ---------------------------------------------------------------------
INSERT OR REPLACE INTO assets VALUES
('series-style-css', 'ep007', 'image',
 'https://journal.emerging-future.org/shared/series-style.css',
 '連載共通 CSS (journal.emerging-future.org)',
 'link'),
('favicon-essesense', NULL, 'icon',
 'https://esse-sense.com/favicon.ico',
 'esse-sense favicon (全ページ共通)',
 '16x16');
