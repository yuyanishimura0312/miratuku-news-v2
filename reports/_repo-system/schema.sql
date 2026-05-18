-- =====================================================================
-- /repo design rules DB (SQLite)
--
-- 「デザインルールそのもの」を構造化して保管。テーマ追加・トークン拡張・
-- コンポーネント追加・ルール明文化のすべてをこの DB 一カ所で管理する。
-- =====================================================================

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------
-- 1. テーマ (デザインバリエーション)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS themes (
  theme_id      TEXT PRIMARY KEY,          -- 'miratuku' / 'essesense'
  display_name  TEXT NOT NULL,             -- 表示名
  description   TEXT,                      -- テーマ概要
  base_color    TEXT,                      -- 紙地基調 (#F5EBDC / #FFFFFF 等)
  accent_color  TEXT,                      -- アクセント色 (#5A2620 / #CC1400 等)
  ink_color     TEXT,                      -- インク色
  css_file      TEXT NOT NULL,             -- repo-<theme>.css ファイル名
  status        TEXT NOT NULL DEFAULT 'active',  -- active / draft / deprecated
  created_at    TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TEXT
);

-- ---------------------------------------------------------------------
-- 2. デザイントークン (CSS カスタムプロパティ単位)
--    各テーマがどの token をどの値で持つかを行単位で保持
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS design_tokens (
  token_id      INTEGER PRIMARY KEY AUTOINCREMENT,
  theme_id      TEXT NOT NULL REFERENCES themes(theme_id) ON DELETE CASCADE,
  category      TEXT NOT NULL,             -- 'color' / 'typography' / 'spacing' / 'size'
  token_name    TEXT NOT NULL,             -- '--pr-paper' / '--pr-wine' 等
  token_value   TEXT NOT NULL,             -- '#FFFFFF' / '"Inter", sans-serif' 等
  description   TEXT,                      -- 意味・用途の自然文
  UNIQUE(theme_id, token_name)
);

-- ---------------------------------------------------------------------
-- 3. コンポーネント (再利用可能 UI ブロック)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS components (
  component_id  TEXT PRIMARY KEY,          -- 'cover' / 'qa-block' / 'researcher-card' 等
  display_name  TEXT NOT NULL,
  purpose       TEXT,                      -- 何を表現するためのコンポーネントか
  html_class    TEXT NOT NULL,             -- 主たる class 名 (pr-qa-block 等)
  required_vars TEXT,                      -- 必須変数 JSON ['title', 'body', ...]
  optional_vars TEXT,                      -- 任意変数 JSON
  template_snippet TEXT,                   -- HTML スニペット (Jinja 風 {{ }})
  notes         TEXT
);

-- ---------------------------------------------------------------------
-- 4. テーマ × コンポーネント (テーマ毎のコンポーネント上書き)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS theme_component_overrides (
  override_id   INTEGER PRIMARY KEY AUTOINCREMENT,
  theme_id      TEXT NOT NULL REFERENCES themes(theme_id) ON DELETE CASCADE,
  component_id  TEXT NOT NULL REFERENCES components(component_id) ON DELETE CASCADE,
  css_override  TEXT,                      -- 追加 CSS (テーマ固有の修飾)
  notes         TEXT,
  UNIQUE(theme_id, component_id)
);

-- ---------------------------------------------------------------------
-- 5. デザインルール (自然言語の規範)
--    "黒帯引用は使わない"、"日本人研究者を必ず本文に 1 名以上" 等
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS design_rules (
  rule_id       INTEGER PRIMARY KEY AUTOINCREMENT,
  theme_id      TEXT REFERENCES themes(theme_id) ON DELETE CASCADE,
                                           -- NULL = 全テーマ共通ルール
  category      TEXT NOT NULL,             -- 'color' / 'layout' / 'typography' / 'content' / 'branding'
  rule_text     TEXT NOT NULL,             -- ルール本文 (自然言語)
  rationale     TEXT,                      -- なぜそうするか (理由)
  enforcement   TEXT NOT NULL DEFAULT 'must',  -- 'must' / 'should' / 'may'
  source        TEXT,                      -- 出典ルール (~/.claude/rules/...md)
  created_at    TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- 冪等性確保 (seed.sql 再実行時の重複防止)。式インデックスで NULL theme を空文字扱い
CREATE UNIQUE INDEX IF NOT EXISTS uq_design_rules
  ON design_rules (COALESCE(theme_id, ''), rule_text);

-- ---------------------------------------------------------------------
-- 6. ロゴ・アセット
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS assets (
  asset_id      TEXT PRIMARY KEY,          -- 'esse-sense-wordmark' 等
  theme_id      TEXT REFERENCES themes(theme_id) ON DELETE CASCADE,
  asset_type    TEXT NOT NULL,             -- 'logo' / 'icon' / 'image'
  file_path     TEXT NOT NULL,             -- 相対パス (_repo-system/assets/...)
  description   TEXT,
  recommended_size TEXT                    -- 'cover:200px / header:28px' 等
);

-- ---------------------------------------------------------------------
-- 7. レポートテンプレート
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS report_templates (
  template_id   TEXT PRIMARY KEY,          -- 'advisory-report-default' 等
  display_name  TEXT NOT NULL,
  file_path     TEXT NOT NULL,             -- templates/report.html 等
  purpose       TEXT,                      -- 想定用途
  default_pages INTEGER DEFAULT 11,        -- 既定ページ数
  notes         TEXT
);

-- ---------------------------------------------------------------------
-- 8. 生成履歴 (どの問いで・どのテーマで作ったかのトレース)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS generation_history (
  history_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  generated_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  theme_id      TEXT NOT NULL REFERENCES themes(theme_id),
  template_id   TEXT REFERENCES report_templates(template_id),
  output_path   TEXT NOT NULL,
  title         TEXT,
  source_data   TEXT                       -- 入力 JSON (再現可能性のため)
);

-- ---------------------------------------------------------------------
-- 索引
-- ---------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_tokens_theme    ON design_tokens(theme_id);
CREATE INDEX IF NOT EXISTS idx_tokens_category ON design_tokens(category);
CREATE INDEX IF NOT EXISTS idx_rules_theme     ON design_rules(theme_id);
CREATE INDEX IF NOT EXISTS idx_rules_category  ON design_rules(category);
CREATE INDEX IF NOT EXISTS idx_history_theme   ON generation_history(theme_id);
CREATE INDEX IF NOT EXISTS idx_history_date    ON generation_history(generated_at DESC);
