-- =============================================================================
-- strategy.db Schema DDL
-- Purpose: strategy.html (2-layer tabs + multi-nested structure) を完全再現
-- Created: 2026-05-16
-- Engine:  SQLite 3.x
-- =============================================================================
--
-- 6 tables / 4 indexes / FK enforcement enabled
--   panels       — トップレベルタブ (miratuku / esse-sense)
--   cpanels      — 第二階層タブ (futures2 / kurashi / henka / other / academic ...)
--   sections     — セクション (banner / parts_jump / hero / body etc.)
--   parts        — PART 区切り (futures2-part-i etc.) — 章立て
--   episodes     — 各話レコード
--   meta_blocks  — panel / cpanel 単位の補助 HTML (intro / footer / related ...)
--
-- 設計判断は strategy_schema_notes.md を参照
-- =============================================================================

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA encoding = 'UTF-8';

-- -----------------------------------------------------------------------------
-- 1. panels — top-level tabs
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS panels (
  panel_id      TEXT    PRIMARY KEY,           -- 'miratuku' / 'esse-sense'
  label         TEXT    NOT NULL,              -- 表示ラベル
  sort_order    INTEGER NOT NULL,              -- タブ表示順
  is_active     INTEGER NOT NULL DEFAULT 0,    -- 初期表示フラグ (0/1)
  metadata_json TEXT,                          -- 任意 JSON (theme color, icon ...)
  created_at    TEXT    DEFAULT (datetime('now')),
  updated_at    TEXT    DEFAULT (datetime('now'))
);

-- -----------------------------------------------------------------------------
-- 2. cpanels — child panels (2nd layer tabs)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cpanels (
  cpanel_id        TEXT    PRIMARY KEY,        -- 'futures2' / 'kurashi' / 'henka' / 'other' / 'academic'
  parent_panel_id  TEXT    NOT NULL,           -- panels.panel_id への FK
  label            TEXT    NOT NULL,           -- 表示ラベル
  series_name      TEXT,                       -- 連載名 (例: '未来のかたち II')
  total_episodes   INTEGER,                    -- 想定話数 (例: 100)
  status_summary   TEXT,                       -- '0/100公開' 等
  sort_order       INTEGER NOT NULL,
  is_active        INTEGER NOT NULL DEFAULT 0,
  metadata_json    TEXT,                       -- カラーテーマ・アイコン URL 等
  created_at       TEXT    DEFAULT (datetime('now')),
  updated_at       TEXT    DEFAULT (datetime('now')),
  FOREIGN KEY (parent_panel_id) REFERENCES panels(panel_id) ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- 3. sections — generic content sections
--    panel 直下 / cpanel 配下のどちらにも置ける (どちらか一方を必ず指定)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sections (
  section_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  cpanel_id      TEXT,                         -- cpanel 配下のときセット
  panel_id       TEXT,                         -- panel 直下のときセット
  section_type   TEXT    NOT NULL,             -- 'banner' / 'parts_jump' / 'part_section' /
                                               -- 'hero' / 'intro' / 'cta' / 'list' / 'note' ...
  dom_id         TEXT,                         -- HTML id 属性
  title          TEXT,
  subtitle       TEXT,
  body_html      TEXT,                         -- セクション本体 HTML (ul/li/p などを含む raw)
  sort_order     INTEGER NOT NULL,
  metadata_json  TEXT,                         -- 任意 (CSS class / icon / link 等)
  created_at     TEXT    DEFAULT (datetime('now')),
  updated_at     TEXT    DEFAULT (datetime('now')),
  FOREIGN KEY (cpanel_id) REFERENCES cpanels(cpanel_id) ON DELETE CASCADE,
  FOREIGN KEY (panel_id)  REFERENCES panels(panel_id)  ON DELETE CASCADE,
  CHECK (
    (cpanel_id IS NOT NULL AND panel_id IS NULL)
    OR (cpanel_id IS NULL AND panel_id IS NOT NULL)
  )
);

-- -----------------------------------------------------------------------------
-- 4. parts — PART 区切り (e.g. futures2-part-i, futures2-part-ii ...)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS parts (
  part_id         TEXT    PRIMARY KEY,         -- 'futures2-part-i' 等
  cpanel_id       TEXT    NOT NULL,
  part_label      TEXT    NOT NULL,            -- 'PART I' 等
  part_title      TEXT    NOT NULL,            -- 章タイトル
  era             TEXT,                        -- '2026-2040' 等 (任意)
  ep_range_start  INTEGER,                     -- 話数レンジ開始 (任意)
  ep_range_end    INTEGER,                     -- 話数レンジ終了 (任意)
  sort_order      INTEGER NOT NULL,
  banner_html     TEXT,                        -- 章扉バナー HTML (任意)
  metadata_json   TEXT,
  created_at      TEXT    DEFAULT (datetime('now')),
  updated_at      TEXT    DEFAULT (datetime('now')),
  FOREIGN KEY (cpanel_id) REFERENCES cpanels(cpanel_id) ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- 5. episodes — 各話レコード
--    part_id は nullable (PART構成を取らない連載でも使えるよう)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS episodes (
  ep_id          INTEGER PRIMARY KEY AUTOINCREMENT,
  part_id        TEXT,                         -- nullable: PART構成のない連載対応
  cpanel_id      TEXT    NOT NULL,
  ep_num         INTEGER,                      -- 話数 (1-100)
  title          TEXT    NOT NULL,
  url            TEXT,                         -- 公開 URL
  status         TEXT,                         -- '公開済' / '予定' / '草稿' / '非公開'
  summary        TEXT,                         -- 1-2 行要約
  sort_order     INTEGER NOT NULL,
  published_at   TEXT,                         -- ISO 8601 (任意)
  metadata_json  TEXT,                         -- タグ・サムネ URL・著者 等
  created_at     TEXT    DEFAULT (datetime('now')),
  updated_at     TEXT    DEFAULT (datetime('now')),
  FOREIGN KEY (part_id)   REFERENCES parts(part_id)     ON DELETE SET NULL,
  FOREIGN KEY (cpanel_id) REFERENCES cpanels(cpanel_id) ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- 6. meta_blocks — panel / cpanel スコープの補助 HTML
--    intro / footer / related links など、繰り返し挿入するブロック
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS meta_blocks (
  block_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  scope_type   TEXT    NOT NULL,               -- 'panel' / 'cpanel'
  scope_id     TEXT    NOT NULL,               -- panels.panel_id または cpanels.cpanel_id
  block_type   TEXT    NOT NULL,               -- 'intro' / 'footer' / 'related' / 'note'
  content_html TEXT    NOT NULL,
  sort_order   INTEGER NOT NULL,
  metadata_json TEXT,
  created_at   TEXT    DEFAULT (datetime('now')),
  updated_at   TEXT    DEFAULT (datetime('now')),
  CHECK (scope_type IN ('panel', 'cpanel'))
);

-- =============================================================================
-- Indexes
-- =============================================================================
CREATE INDEX IF NOT EXISTS idx_episodes_cpanel  ON episodes(cpanel_id);
CREATE INDEX IF NOT EXISTS idx_episodes_part    ON episodes(part_id);
CREATE INDEX IF NOT EXISTS idx_episodes_status  ON episodes(status);
CREATE INDEX IF NOT EXISTS idx_episodes_title   ON episodes(title);
CREATE INDEX IF NOT EXISTS idx_sections_cpanel  ON sections(cpanel_id);
CREATE INDEX IF NOT EXISTS idx_sections_panel   ON sections(panel_id);
CREATE INDEX IF NOT EXISTS idx_sections_type    ON sections(section_type);
CREATE INDEX IF NOT EXISTS idx_parts_cpanel     ON parts(cpanel_id);
CREATE INDEX IF NOT EXISTS idx_cpanels_parent   ON cpanels(parent_panel_id);
CREATE INDEX IF NOT EXISTS idx_metablocks_scope ON meta_blocks(scope_type, scope_id);

-- =============================================================================
-- Triggers — updated_at 自動更新
-- =============================================================================
CREATE TRIGGER IF NOT EXISTS trg_panels_updated_at
AFTER UPDATE ON panels FOR EACH ROW BEGIN
  UPDATE panels SET updated_at = datetime('now') WHERE panel_id = OLD.panel_id;
END;

CREATE TRIGGER IF NOT EXISTS trg_cpanels_updated_at
AFTER UPDATE ON cpanels FOR EACH ROW BEGIN
  UPDATE cpanels SET updated_at = datetime('now') WHERE cpanel_id = OLD.cpanel_id;
END;

CREATE TRIGGER IF NOT EXISTS trg_sections_updated_at
AFTER UPDATE ON sections FOR EACH ROW BEGIN
  UPDATE sections SET updated_at = datetime('now') WHERE section_id = OLD.section_id;
END;

CREATE TRIGGER IF NOT EXISTS trg_parts_updated_at
AFTER UPDATE ON parts FOR EACH ROW BEGIN
  UPDATE parts SET updated_at = datetime('now') WHERE part_id = OLD.part_id;
END;

CREATE TRIGGER IF NOT EXISTS trg_episodes_updated_at
AFTER UPDATE ON episodes FOR EACH ROW BEGIN
  UPDATE episodes SET updated_at = datetime('now') WHERE ep_id = OLD.ep_id;
END;

CREATE TRIGGER IF NOT EXISTS trg_metablocks_updated_at
AFTER UPDATE ON meta_blocks FOR EACH ROW BEGIN
  UPDATE meta_blocks SET updated_at = datetime('now') WHERE block_id = OLD.block_id;
END;

-- =============================================================================
-- Reference views — レンダリング時の補助
-- =============================================================================

-- panel → cpanel → part → episode の階層を一覧化
CREATE VIEW IF NOT EXISTS v_strategy_tree AS
SELECT
  p.panel_id,
  p.label              AS panel_label,
  p.sort_order         AS panel_order,
  cp.cpanel_id,
  cp.label             AS cpanel_label,
  cp.sort_order        AS cpanel_order,
  pt.part_id,
  pt.part_label,
  pt.part_title,
  pt.sort_order        AS part_order,
  ep.ep_id,
  ep.ep_num,
  ep.title             AS episode_title,
  ep.status            AS episode_status,
  ep.url               AS episode_url,
  ep.sort_order        AS episode_order
FROM panels p
LEFT JOIN cpanels  cp ON cp.parent_panel_id = p.panel_id
LEFT JOIN parts    pt ON pt.cpanel_id = cp.cpanel_id
LEFT JOIN episodes ep ON ep.cpanel_id = cp.cpanel_id
                      AND (ep.part_id = pt.part_id OR (ep.part_id IS NULL AND pt.part_id IS NULL))
ORDER BY p.sort_order, cp.sort_order, pt.sort_order, ep.sort_order;

-- 公開済み話数の集計
CREATE VIEW IF NOT EXISTS v_episodes_status_summary AS
SELECT
  cp.cpanel_id,
  cp.label             AS cpanel_label,
  cp.total_episodes,
  COUNT(ep.ep_id)                                      AS total_registered,
  SUM(CASE WHEN ep.status = '公開済' THEN 1 ELSE 0 END) AS published_count,
  SUM(CASE WHEN ep.status = '予定'   THEN 1 ELSE 0 END) AS scheduled_count,
  SUM(CASE WHEN ep.status = '草稿'   THEN 1 ELSE 0 END) AS draft_count
FROM cpanels cp
LEFT JOIN episodes ep ON ep.cpanel_id = cp.cpanel_id
GROUP BY cp.cpanel_id, cp.label, cp.total_episodes;

-- =============================================================================
-- End of schema
-- =============================================================================
