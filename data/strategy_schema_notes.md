# strategy.db スキーマ設計ノート

`strategy.html` (2層タブ + 多段ネスト構造) を完全に再現可能な SQLite データベースの設計判断と運用方針をまとめる。

- 作成日: 2026-05-16
- 対象ファイル: `data/strategy.db`
- DDL: `data/strategy_schema.sql`
- エンジン: SQLite 3.x (WAL モード / FK 強制)

---

## 1. 全体構造

### 1.1 階層モデル

```
panels (top tabs: miratuku / esse-sense)
  └── cpanels (2nd tabs: futures2 / kurashi / henka / other / academic ...)
        ├── sections (banner / parts_jump / hero / intro / cta ...)
        ├── parts (PART I / PART II ...)
        │     └── episodes (各話)
        └── episodes (PART 非所属の単発話)
sections (panel 直下)
meta_blocks (panel または cpanel スコープの intro / footer / related 等)
```

### 1.2 6 テーブル構成

| # | テーブル | 役割 | PK | 想定レコード数 |
|---|---|---|---|---|
| 1 | `panels` | 最上位タブ | `panel_id` TEXT | 2-5 |
| 2 | `cpanels` | 第二階層タブ | `cpanel_id` TEXT | 5-15 |
| 3 | `sections` | 汎用セクション | `section_id` INTEGER | 30-80 |
| 4 | `parts` | PART 区切り (章) | `part_id` TEXT | 10-30 |
| 5 | `episodes` | 各話 | `ep_id` INTEGER | 200-700 |
| 6 | `meta_blocks` | 補助 HTML | `block_id` INTEGER | 10-40 |

総レコード数 (フル投入時想定): **約 270 - 870 行**。

---

## 2. 設計判断の根拠

### 2.1 HTML 完全再現可能性

- **`body_html` / `banner_html` / `content_html` を raw HTML として保持**
  - 構造化しにくい多段 `<ul>` / `<li>` / 強調マーキングなどをそのまま保存
  - レンダラ側は「テンプレ + raw HTML 挿入」だけで済むため、ジェネレータが単純化される
- **`metadata_json` をすべての主要テーブルに用意**
  - CSS クラス・テーマカラー・アイコン URL・タグなど、列追加せずに拡張可能
  - 将来のレイアウト変更や A/B テスト時にスキーマ変更なしで対応

### 2.2 検索容易性

- `episodes.title` / `episodes.cpanel_id` / `episodes.status` を主要検索軸として個別 INDEX 化
- `episodes` は `cpanel_id` 必須 (NOT NULL) にし、必ず「どの連載に属する話か」が一意に決まる
- `sections.section_type` を INDEX 化し「banner だけ取り出す」「parts_jump だけ取り出す」等のフィルタを高速化

### 2.3 拡張性 — 新 cpanel 追加が容易

- `cpanels` テーブルに 1 行 INSERT + `sections` / `parts` / `episodes` を順次 INSERT するだけ
- `parent_panel_id` FK で `panels` (miratuku / esse-sense) に紐づける
- 既存データ・ジェネレータコードを変更せずに新連載を追加可能 (path-1 ベース)
- `cpanel_id` は意味のある TEXT (`futures2` / `kurashi` ...) にし、URL や DOM id とも一致させやすい

### 2.4 panel 直下セクションの扱い

- `sections.cpanel_id` / `sections.panel_id` のどちらか一方が必ず NOT NULL になる CHECK 制約
- これにより「esse-sense panel 直下の hero」「miratuku panel 直下のお知らせ」のような cpanel に属さないセクションも表現できる
- 同様に `meta_blocks.scope_type` で `'panel'` / `'cpanel'` を切り替え

### 2.5 PART を取らない連載への対応

- `episodes.part_id` を nullable にし、PART 構成を取らない連載 (other / 単発記事) でも `episodes` テーブルを共用
- FK は `ON DELETE SET NULL` で part を削除しても episode は残る (履歴保全)

### 2.6 ソート順管理

- 全テーブルに `sort_order INTEGER NOT NULL` を持たせ、表示順を明示制御
- ID (連番) や作成日時に依存しない → 並び替えが容易

### 2.7 更新時刻の自動管理

- 全主要テーブルに `created_at` / `updated_at` を持ち、UPDATE 時は AFTER UPDATE TRIGGER で `updated_at` を自動更新
- 監査ログやキャッシュ無効化判定に利用可能

---

## 3. 主要リレーション

```
panels (1) ──< (N) cpanels
panels (1) ──< (N) sections        [cpanel_id IS NULL]
panels (1) ──< (N) meta_blocks     [scope_type='panel']

cpanels (1) ──< (N) sections       [panel_id IS NULL]
cpanels (1) ──< (N) parts
cpanels (1) ──< (N) episodes
cpanels (1) ──< (N) meta_blocks    [scope_type='cpanel']

parts (1) ──< (N) episodes
```

- すべての FK は `ON DELETE CASCADE` (`episodes.part_id` のみ `SET NULL`)
- 親 panel / cpanel が消えると配下も一括削除される

---

## 4. ビュー (View)

### 4.1 `v_strategy_tree`

panel → cpanel → part → episode の階層フラット展開ビュー。
レンダリング時の「全タブ一括取得」「サイドバー目次生成」に利用。

### 4.2 `v_episodes_status_summary`

cpanel ごとの登録話数・公開済・予定・草稿のカウント。
タブ上の `0/100 公開` 等のステータス表示用。

---

## 5. ETL / 運用ルール

### 5.1 投入順序

1. `panels` (miratuku / esse-sense)
2. `cpanels` (各連載)
3. `parts` (PART 構成がある連載)
4. `episodes` (PART 非所属の単発話は `part_id = NULL`)
5. `sections` (banner / parts_jump / hero ...)
6. `meta_blocks` (intro / footer ...)

### 5.2 一意性ルール

- `panel_id` / `cpanel_id` / `part_id` は意味のある TEXT (URL safe slug 推奨)
- `episodes.ep_num` は `cpanel_id` 内で一意になるように運用 (DB 制約は付けず、UNIQUE 部分インデックスで補強可能)
- `sections` / `episodes` の `sort_order` は `cpanel_id` 内で一意になるように運用

### 5.3 HTML 保存ルール

- `body_html` / `banner_html` / `content_html` は **最小限の DOM 単位** で保存 (例: `<ul>...</ul>` 単位)
- 外側のラッパー (`<section class="...">` 等) はジェネレータ側で生成し、DB には body 部分だけ持つ
- 改行・インデントは保存時に保持し、再現性を優先

### 5.4 検索クエリ例

```sql
-- 公開済みの全話一覧
SELECT cpanel_id, ep_num, title, url
FROM episodes
WHERE status = '公開済'
ORDER BY cpanel_id, sort_order;

-- 特定 cpanel の PART 構成ツリー
SELECT pt.part_label, pt.part_title, ep.ep_num, ep.title, ep.status
FROM parts pt
LEFT JOIN episodes ep ON ep.part_id = pt.part_id
WHERE pt.cpanel_id = 'futures2'
ORDER BY pt.sort_order, ep.sort_order;

-- esse-sense panel 配下のすべての section
SELECT s.section_type, s.title, s.body_html
FROM sections s
LEFT JOIN cpanels cp ON cp.cpanel_id = s.cpanel_id
WHERE s.panel_id = 'esse-sense' OR cp.parent_panel_id = 'esse-sense'
ORDER BY s.sort_order;
```

---

## 6. 拡張ポイント (将来対応)

### 6.1 多言語化

- `episodes`・`sections`・`meta_blocks` に `lang` 列を追加し、`(scope_id, lang)` でユニーク
- または別テーブル `episodes_i18n (ep_id, lang, title, summary)` を追加して翻訳を分離

### 6.2 タグ / カテゴリ

- 中間テーブル `episode_tags (ep_id, tag)` を追加 (現状は `metadata_json` で代用可能)
- タグ検索を高速化したい場合のみ正規化

### 6.3 著者・担当

- `authors (author_id, name, ...)` テーブルを追加し、`episode_authors (ep_id, author_id, role)` で多対多リンク
- 現状は `metadata_json` の `author` キーで代用

### 6.4 公開履歴 / バージョニング

- `episode_revisions (revision_id, ep_id, snapshot_json, created_at)` を追加し変更履歴を保持
- 大規模更新時の差分追跡用

### 6.5 cross-DB 参照 (db-registry 連携)

- 各 cpanel が依存する DB / 連載エージェントを表す `cpanel_db_refs (cpanel_id, db_id, ref_type)` を追加
- 既存 67 DB エコシステム (db-registry.json) との接続点を可視化

### 6.6 レンダリングテンプレ管理

- `templates (template_id, name, html, css)` テーブルを追加し、`sections.metadata_json` から `template_id` を参照
- 同じ section_type でも複数のレイアウトバリエーションを管理可能

---

## 7. 既知の制約・注意点

- **`body_html` 直書き** は XSS リスクがあるため、編集者の入力ルール (許可タグリスト) と CI のサニタイズ検証が必要
- **`metadata_json` の自由度** が高いため、キー命名規約をプロジェクト内で文書化 (例: `metadata_json.theme_color`, `metadata_json.icon_url`)
- **`sections` の CHECK 制約** により `panel_id` と `cpanel_id` の同時 NOT NULL は不可。両方に紐づくセクションは別レコードとして扱う
- **`episodes.ep_num`** の重複は DB 制約では防がない。投入スクリプト側でバリデーション必須
- **`status` 値** ('公開済' / '予定' / '草稿' / '非公開') は ENUM 化していないため、定数表をアプリ側で持つ運用

---

## 8. ファイル一覧

| ファイル | 役割 |
|---|---|
| `data/strategy_schema.sql` | DDL 完全版 (本ノートの実装) |
| `data/strategy_schema_notes.md` | 本ファイル (設計判断・拡張ポイント) |
| `data/strategy.db` | SQLite DB 実体 (DDL 適用後に生成) |

---

## 9. 想定スケール (フル投入時)

| テーブル | 想定レコード数 | 主な根拠 |
|---|---|---|
| `panels` | 2-5 | miratuku / esse-sense + 将来拡張 |
| `cpanels` | 5-15 | futures2 / kurashi / henka / jigyo / keiei / itonami / other / academic ... |
| `parts` | 10-30 | 各連載 3-5 PART × 5-10 連載 |
| `episodes` | **200-700** | 連載あたり最大 100 話 × 5-7 連載 |
| `sections` | 30-80 | banner / parts_jump / hero / intro / cta × cpanel 数 |
| `meta_blocks` | 10-40 | intro / footer / related × cpanel + panel |
| **合計** | **約 270 - 870 行** | |

軽量サイズ (DB ファイルは数 MB 程度) で全文検索なしでも十分高速。

---

## 10. 履歴

- 2026-05-16 初版策定。strategy.html (2層タブ + 多段ネスト) の完全再現スキーマを 6 テーブル構成で設計。
