-- =============================================================================
-- strategy.html DB化 / リファレンス スキーマ (Phase 0 設計案)
-- =============================================================================
-- Strategy-B が data/strategy_schema.sql を生成中。本ファイルは並行で参照用に
-- 配置する設計叩き台。実装時は data/strategy_schema.sql が真実とする。
--
-- 設計指針:
--  - 順序(sort_order)を全テーブルで保持し、レンダリング順を再現できるようにする
--  - HTMLの再現に必要な未構造化フラグメントは body_html / banner_html / metadata_json に格納
--  - インラインstyle属性、style="..." の小さな違いも metadata_json で保持
--  - DOM ID(cpanel-academic 等) は panels.dom_id / cpanels.dom_id にそのまま保持
-- =============================================================================

-- 戦略 / コンテンツ / テーマ別 の3トップレベル
CREATE TABLE IF NOT EXISTS panels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,            -- 'strategy' | 'content' | 'themes'
    dom_id TEXT NOT NULL,                -- 'top-strategy' | 'top-content' | 'top-themes'
    label TEXT NOT NULL,                 -- '戦略' | 'コンテンツ' | 'テーマ別'
    is_active INTEGER NOT NULL DEFAULT 0,
    sort_order INTEGER NOT NULL DEFAULT 0,
    intro_html TEXT,                     -- 各パネル上部の theme-intro 等
    metadata_json TEXT                   -- 自由属性(class追加など)
);

-- 各トップレベル内のサブタブ
-- 戦略 → panel-miratuku / panel-esse-sense
-- コンテンツ → cpanel-futures2 / cpanel-kurashi / cpanel-henka / cpanel-other / cpanel-academic
CREATE TABLE IF NOT EXISTS cpanels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    panel_key TEXT NOT NULL REFERENCES panels(key),
    key TEXT NOT NULL,                   -- 'miratuku' | 'esse-sense' | 'futures2' | ...
    dom_id TEXT NOT NULL,                -- 'panel-miratuku' | 'cpanel-academic' ...
    label TEXT NOT NULL,                 -- タブ表記
    data_attr TEXT NOT NULL,             -- 'data-panel' or 'data-cpanel'
    is_active INTEGER NOT NULL DEFAULT 0,
    sort_order INTEGER NOT NULL DEFAULT 0,
    intro_html TEXT,                     -- パネル上部の挨拶(theme-intro 等)
    banner_html TEXT,                    -- kl-banner / series-hero など連載リーディング
    body_html TEXT,                      -- そのまま埋め込む HTML フラグメント (構造化外残渣)
    metadata_json TEXT,                  -- パネル独自属性、追加クラスなど
    UNIQUE(panel_key, key)
);

-- 連載/シリーズの「Part」セクション (PROLOGUE / PART I / PART II / FINAL ...)
CREATE TABLE IF NOT EXISTS parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpanel_key TEXT NOT NULL,            -- 'kurashi' | 'henka' | 'futures2' 等
    key TEXT NOT NULL,                   -- 'kurashi-prologue' | 'futures2-part-i' 等 (DOM ID)
    label TEXT,                          -- 'PROLOGUE — 序 章' / 'PART I' 等
    title TEXT,                          -- '衣食住 ― 身体を包む環境' 等
    stats TEXT,                          -- '18話 ／ 公開済 18話'
    sort_order INTEGER NOT NULL DEFAULT 0,
    body_html TEXT,                      -- 残余HTML
    metadata_json TEXT,                  -- 'series-listing'内位置・class
    UNIQUE(cpanel_key, key)
);

-- 連載エピソード一覧
CREATE TABLE IF NOT EXISTS episodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    part_key TEXT NOT NULL,              -- parts.key
    num TEXT NOT NULL,                   -- '001' / '042' 等
    title TEXT,
    sub TEXT,                            -- リード文
    meta_text TEXT,                      -- '深化軸 C5-a / Lv1 / 引用型' 等
    status TEXT,                         -- 'published' | 'draft' | 'upcoming'
    href TEXT,                           -- 公開記事URL (なければNULL)
    badge_label TEXT,                    -- 'ドラフト' | '公開済' 等
    item_class TEXT,                     -- 'kl-ep-item' | 'content-ep' 等
    sort_order INTEGER NOT NULL DEFAULT 0,
    raw_html TEXT,                       -- 元エピソードHTML(再現用)
    metadata_json TEXT
);

-- レポートカード/シリーズカード/テーマカードなど、可変構造の汎用ブロック
-- cpanel(やpanel)内のリスト要素を順に並べる
CREATE TABLE IF NOT EXISTS sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_kind TEXT NOT NULL,           -- 'panel' | 'cpanel' | 'part'
    parent_key TEXT NOT NULL,            -- 親 dom_id or key
    kind TEXT NOT NULL,                  -- 'report_card' | 'series_card' | 'theme_card' | 'coming_soon' | 'banner' | 'jump_grid' | 'progress' | 'raw_html'
    title TEXT,
    body_html TEXT NOT NULL,             -- そのブロックの完全HTML
    sort_order INTEGER NOT NULL DEFAULT 0,
    metadata_json TEXT
);

-- 注釈ブロック・theme-intro・冒頭リード等、自由配置メタ要素
CREATE TABLE IF NOT EXISTS meta_blocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_kind TEXT NOT NULL,           -- 'panel' | 'cpanel' | 'part' | 'global'
    parent_key TEXT NOT NULL,            -- 'top-themes' | 'cpanel-academic' | ...
    position TEXT NOT NULL DEFAULT 'before', -- 'before' | 'after' | 'inline'
    body_html TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    metadata_json TEXT
);

CREATE INDEX IF NOT EXISTS idx_cpanels_panel_sort ON cpanels(panel_key, sort_order);
CREATE INDEX IF NOT EXISTS idx_parts_cpanel_sort ON parts(cpanel_key, sort_order);
CREATE INDEX IF NOT EXISTS idx_episodes_part_sort ON episodes(part_key, sort_order);
CREATE INDEX IF NOT EXISTS idx_sections_parent ON sections(parent_kind, parent_key, sort_order);
CREATE INDEX IF NOT EXISTS idx_meta_parent ON meta_blocks(parent_kind, parent_key, position, sort_order);
