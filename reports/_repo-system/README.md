# /repo system

esse-sense / NPO法人ミラツクの公式レポート (A4 印刷可能 HTML) を 1 コマンドで生成する仕組み。デザインルールは SQLite (`design_rules.db`) に格納し、テーマ・トークン・コンポーネント・自然言語ルールを追加することで拡張できる。

## クイックスタート

```bash
cd ~/projects/apps/miratuku-news-v2/reports/_repo-system

# 1. 利用可能なテーマ
python3 build_report.py --list-themes

# 2. 設計ルール (must/should/may + 出典つき)
python3 build_report.py --list-rules essesense

# 3. レポート生成 (esse-sense 版)
python3 build_report.py --input examples/sample.json --theme essesense --open

# 4. ミラツク版
python3 build_report.py --input examples/sample.json --theme miratuku --open
```

出力先: `~/projects/apps/miratuku-news-v2/reports/<slug>-<theme>.html`

## 構造

```
_repo-system/
├── README.md                    ← このファイル
├── design_rules.db              ← SQLite (8 テーブル)
├── schema.sql                   ← スキーマ定義
├── seed.sql                     ← 初期データ
├── css/
│   ├── repo-base.css            ← 構造・コンポーネント (共通)
│   ├── repo-miratuku.css        ← warm cream + wine theme
│   └── repo-essesense.css       ← 純白 + 赤白CI theme
├── templates/
│   └── report.html              ← {{ var }} / {% if %} / {% for %}
├── assets/
│   └── esse-sense-wordmark.png  ← 公式エッセンスワードマーク
├── examples/
│   └── sample.json              ← 入力 JSON サンプル
└── build_report.py              ← CLI (Python3 標準ライブラリのみ)
```

## DB スキーマ

| テーブル | 役割 |
|---|---|
| `themes` | デザインバリエーション登録簿 |
| `design_tokens` | CSS カスタムプロパティ (色・タイポ・スペース) のテーマ別値 |
| `components` | 再利用可能 UI ブロック (cover/page/q-box/researcher-card 等 15 種) |
| `theme_component_overrides` | テーマ × コンポーネント単位の追加 CSS |
| `design_rules` | 自然言語ルール (must/should/may + 出典) |
| `assets` | ロゴ・画像のパスと推奨サイズ |
| `report_templates` | HTML 雛形の登録簿 |
| `generation_history` | 生成履歴 (再現性確保のため source_data JSON を保持) |

## 入力 JSON 仕様

`templates/report.html` の `{{ }}` プレースホルダに対応する key を入れる。最小構成:

```json
{
  "slug": "my-report",
  "theme": "essesense",
  "doc_title": "...",
  "cover_title_html": "和文タイトル\n／第二行",
  "cover_en": "English subtitle.",
  "pages": [
    { "num": 2, "body_html": "<article class='pr-chapter'>...</article>..." }
  ]
}
```

`body_html` には `_repo-system/css/repo-base.css` で定義済みのコンポーネント class (`pr-chapter` / `pr-lead` / `pr-q-box` / `pr-info-grid` / `pr-stat-strip` / `pr-qa-block` / `pr-score-table` / `pr-researcher-card` / `pr-quote-light` / `pr-disclaimer-block` / `pr-sign`) を組み合わせて記述する。

## 拡張方法

### 新テーマ追加

1. CSS: `css/repo-<theme>.css` を作成し、`:root { --pr-paper: ...; --pr-wine: ...; ... }` で token を上書き
2. DB:
   ```sql
   INSERT INTO themes VALUES ('newtheme', '新テーマ', '...', '#XXX', '#YYY', '#ZZZ',
                              'repo-newtheme.css', 'active', CURRENT_TIMESTAMP, NULL);
   INSERT INTO design_tokens (theme_id, category, token_name, token_value) VALUES ...;
   INSERT INTO design_rules (theme_id, category, rule_text, enforcement) VALUES ...;
   ```
3. ロゴが新規ならば `assets/` に置き `assets` テーブルへ登録

### コンポーネント追加

1. `css/repo-base.css` に新 class `.pr-newcomp { ... }` を追加
2. DB:
   ```sql
   INSERT INTO components VALUES
     ('newcomp', '新コンポーネント', '用途', 'pr-newcomp',
      '["required_var"]', '[]', '<div class="pr-newcomp">...</div>', NULL);
   ```

### デザインルール追加

```sql
INSERT INTO design_rules (theme_id, category, rule_text, rationale, enforcement, source)
VALUES (NULL, 'layout', '新しいルール本文', 'なぜそうするか', 'must', 'rules/xxx.md');
```

`theme_id = NULL` で全テーマ共通、特定テーマ id を入れればそのテーマ限定。

## 既存正本ルールとの関係

| ルール文書 (~/.claude/rules/) | 取り込み状況 |
|---|---|
| `progress-report-style.md` | warm cream + wine トークン・章構造ルールを miratuku テーマで継承 |
| `db-design-system.md` | 赤白CI #CC1400 / 純白基調を essesense テーマで継承 |
| `journal-essay-style.md` | 「らしい」「近年」「ある研究によれば」禁止等を共通ルールに登録 |

## 履歴

- 2026-05-18 初版策定。実証 1 号は `answer-day1v3-bio-manufacturing-print*.html`。
