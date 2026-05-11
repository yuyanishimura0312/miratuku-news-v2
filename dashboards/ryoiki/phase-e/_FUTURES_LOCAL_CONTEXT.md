# Futures ローカル文脈収集レポート

> 収集日: 2026-05-11 / 担当: knowledge agent / タイムボックス: 15分以内
> 範囲: `~/work/`, `~/writings/`, `~/projects/apps/miratuku-news-v2/`（特に `dashboards/ryoiki/phase-e/`）, `~/.claude/projects/-Users-nishimura-/memory/`
> Slack: 本セッションで MCP slack ツールが利用不可だったためスキップ（指示通り）

---

## 0. 既存の同名/類似ブリーフィング

本タスクと重複する既存資料が phase-e/ に存在する。今回の調査結果は本ファイルに残しつつ、内容の重なる範囲では既存資料を一次出典として参照する。

- `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/_FUTURES_BRIEFING_CONTEXT.md`（2026-05-11、同一タスク先行版）
- `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-spec-draft.md`（2026-05-11、Futures仕様素案147行）

---

## 1. メンバーシップコミュニティ（2011-2017）の活動記録

| 項目 | 内容 | 出典 |
|---|---|---|
| 設立年 | 2011年 | `futures-spec-draft.md` L24 |
| 終了年 | 2017年 | `futures-spec-draft.md` L24, L28 |
| 主題 | 研究者と実践者をつなぐ最初の場 | 同 L24, L28 |
| 位置づけ | NPO法人ミラツク 第1期オンラインメンバーシップコミュニティ | 同 L14, L28 |

- 勉強会・フォーラム・成果物の個別記録、終了経緯、引き継ぎ事項の詳細は、`~/work/`・`~/writings/`・`~/.claude/projects/.../memory/` を横断検索した範囲では**情報源未発見**（grep `2011` `メンバーシップ` `ROOM` の組合せで該当文書なし）。
- 参照可能なのは Futures 仕様書の系譜表のみで、活動詳細はヒアリングまたは Notion 補完が必要。

---

## 2. ROOM（2020-2025）の活動記録

| 項目 | 内容 | 出典 |
|---|---|---|
| 設立年 | 2020年 | `futures-spec-draft.md` L25 |
| 終了年 | 2025年（5年間運営） | 同 L25, L28-30 |
| 主題 | 専門領域を超えた対話と探求 | 同 L25 |
| 位置づけ | ミラツク 第2期オンラインメンバーシップコミュニティ | 同 L14, L28 |

- 月例会のテーマ、参加者数、印象的なエピソード等の個別記録は、横断検索の範囲では**情報源未発見**。
- 補足: 同名「ROOM」が `miratuku-membership`（最重要プロジェクト、2026-04-10〜）のプラン名（¥1,500/月、Professional ¥5,000/月・法人パートナー ¥30,000/月と並列）として再利用されている可能性あり。
  - 出典: `~/.claude/projects/-Users-nishimura-/memory/project_miratuku_membership.md` L25

---

## 3. Futures 準備の経緯

### 3.1 検討開始の最古の痕跡（確認できた範囲）

- 系譜上は ROOM 終了（2025年）からの連続性が前提。仕様素案の作成は **2026-05-11**（`futures-spec-draft.md` L1）。
- LP 初回 FTP 配置: **2026-05-10**（`~/.claude/projects/.../memory/project_futures_landing.md` L74）。
- LP デザインチーム再演出版（最新）commit `b00615e`: **2026-05-11**（同上 L52, L82）。
- Futures Platform（会員専用サイト）本番リリース: **2026-05-10〜11**（`project_futures_platform.md` 全文）。
- ローカル検索の範囲では、これより前の「対話の議事録」「準備メモ」は発見できず。具体的な検討対話の経緯は Notion または slack に存在する可能性が高い。

### 3.2 スケジュール（spec L67-76）

| 時期 | 内容 |
|---|---|
| 2026年5月 | 公開・募集開始 |
| 2026年6月 | ミニフォーラム |
| 2026年7月 | 取り組み開始（1年目） |
| 2027年6月 | 1年目終了・振り返り |

### 3.3 体制（spec L82-89）

- ディレクター: 西村 / プロマネ: 浜田 / 運営コア: 古立、高本 / 運営補佐: 末岡、行徳ほか検討中

### 3.4 第一期募集仕様（LP/会員サイト確定値）

- 個人 100名 / 法人 10社 / 2026年（プレ募集ではなく正式）
- 個人 ¥30,000/年、法人 ¥500,000/年（5名まで登録可）
- 出典: `~/.claude/projects/-Users-nishimura-/memory/project_futures_landing.md` L17-20
- Stripe TEST mode 価格: `price_1TVY3HDp58OiTzeSMEvjFzMM` (個人¥3K/月)、`price_1TVY3HDp58OiTzeSqST0T27F` (法人¥30K/月)
  - 出典: `project_futures_platform.md` L39（テスト額と LP表記額の整合性確認は別途必要）

### 3.5 外部接続プロジェクト（spec L93-101 + 関連資料）

- 井上ゆきさんシード資金プロジェクト — 詳細記述は**情報源未発見**
- 博報堂協働プロジェクト — esse-sense 文脈で「博報堂 × 未来洞察RESONANCE × Japan-Origin Cultural Scenario Intelligence」構想あり
  - 出典: `~/work/esse-sense-deep-knowledge-strategy.html`, `~/work/deep-knowledge-future-forum-2026.html`
- PwC協働プロジェクト — esse-sense 文脈で「PwC × 未来駆動型経営 / バックキャスティング型R&D戦略」構想あり
  - 出典: 同上 + `~/work/deep-knowledge-final-report-2026.html`
- 注意: 博報堂・PwC の活動内容として記載がある資料はいずれも esse-sense / 深い知Forum文脈であり、Futures 本体での具体的共同活動は仕様書上「今後検討」段階。

---

## 4. 連載5本（暮らし・変化・事業・いとなみ・経営）と Futures の接続

### 4.1 仕様素案上の位置づけ（spec L40-45）

> 「5つの連載（暮らし・変化・事業・いとなみ・経営）+ Futures連載」
> 「5つの連載（暮らし・変化・事業・いとなみ・経営）に加えて、Futures連載が新たに加わる」

- すなわち Futures 連載は既存 5 連載と並列の「6本目」として企画されている（仕様書ベース）。

### 4.2 LP上の表現との不整合（要確認）

- `futures-landing-page.html` L823 では Futures 連載を「『暮らしのかたち』『変化のかたち』『事業のかたち』に続く5番目のシリーズ」と記載。
- 仕様素案では 5 既存連載 + Futures = 6本目、LP では 4 既存連載（暮・変・事 → 4番目相当）+ Futures = 5番目、と数え方が一致していない。
- 解釈余地:
  - LP 時点ではまだ「いとなみ」「経営」が連載として揃っておらず、3 連載 + Futures（4本目）→ さらに後発の「いとなみ」「経営」企画が立ち上がり仕様素案が更新された可能性。
  - 実際 `~/.claude/projects/.../memory/MEMORY.md` インデックスでも `henka-no-katachi`（完結）/`kurashi-no-katachi`（完結）/`jigyo`（運用中）の3本は公開済確定、`itonami_no_katachi`（2026-05-09企画立案）・`keiei_no_katachi`（EP006試作完了、Stage 0 仕様策定中）はごく最近の立ち上げと記録されている。
- LP 公開後に仕様素案が「5既存連載+Futures」へ更新された経緯と推定される。LP本文の修正可否は判断保留。

### 4.3 接続の機能的説明（spec L43, L113-115 + Series Plan v2）

- 7+1の問い、26以上のDB、主要書籍3点（『深い知が拓く2100年』『未来への問い』『未来を読む力』）と並ぶ「共通参照点」として、5連載+Futures連載が位置づけられる（spec L40-45）。
- Futures Series Plan v2 (320行) の中で、連載第88話「2070年の暮らし — 場所と複数性」など、既存連載テーマ（暮らし等）と接続するエピソードが個別に設計されている。
- 出典: `_FUTURES_SERIES_PLAN_v2.md`

### 4.4 5連載それぞれの現状（MEMORY.md より）

| 連載 | エージェント | 現状 |
|---|---|---|
| 暮らしのかたち | `/kurashi` | 全100話完結（2026-05-09 GitHub Pages） |
| 変化のかたち | `/henka` | 全100話完結（2026-05-09）、87/100点・編集主幹検証済 |
| 事業のかたち | `/jigyo` | 連載100話・5 PART × 18領域 公開済（stg.miratuku-journal.org） |
| いとなみのかたち | `/itonami` | 新シリーズ（2026-05-09企画立案）、5領域×20話=100話計画 |
| 経営のかたち | `/keiei-team` ほか | EP006試作完了、Stage 0 仕様策定中 |

---

## 5. 未来学教科書『未来を読む力』の公開URL

### 5.1 確認できた実体（2系統）

| 場所 | パス | GitHub Remote | 状態 |
|---|---|---|---|
| (A) miratuku-news-v2 配下 | `/Users/nishimura+/projects/apps/miratuku-news-v2/textbook.html` | `github.com/yuyanishimura0312/miratuku-news-v2.git` | 単一HTML、`<title>未来を読む力 — 現代未来学の理論と実践 \| FS Knowledge DB</title>`、本文最終段落あり |
| (B) futures-textbook 専用リポ | `/Users/nishimura+/projects/apps/futures-textbook/` | `github.com/yuyanishimura0312/futures-textbook.git` | `index.html` + `chapters/ch01.html〜ch20.html` の章別構成 |

### 5.2 公開URL（メモリ記録）

- **公開URL（メモリ上の正典）**: `https://yuyanishimura0312.github.io/miratuku-news-v2/textbook.html`
  - 出典: `~/.claude/projects/-Users-nishimura-/memory/project_futures_textbook.md` L12
- futures-textbook 専用リポの GitHub Pages 公開可否、(A) と (B) の関係（単一HTML版が公開用ビルド成果物か、別系統か）は本調査範囲では確認できず（実URL の HTTP 確認も未実施）。
- Futures LP（`futures-landing-page.html`）内には textbook へのリンク埋め込みは **未検出**（`grep textbook` でヒット0）。仕様書 L40-43 の言及にとどまる。

---

## 6. その他、Futures 関連で見つかった重要ファイル一覧（出典マップ）

### 6.1 phase-e/ 配下の Futures 関連資料群

```
_FUTURES_BRIEFING_CONTEXT.md           （本タスクと重複する先行ブリーフィング）
_FUTURES_EDITORIAL_GUIDELINE_v2.md     （連載編集ガイドライン v2）
_FUTURES_FACTCHECK_v2.md               （連載 v2 ファクトチェック）
_FUTURES_NARRATIVE_QUALITY_v2.md       （連載 v2 ナラティブ品質）
_FUTURES_PUBLICATION_REVIEW_v2.md      （連載 v2 公開レビュー）
_FUTURES_QA_FULL_v2.md                 （連載 v2 QA フル）
_FUTURES_QA_REPORT_v2_ep02-03.md       （連載 v2 ep02-03 QA）
_FUTURES_QA_REPORT_v2_revised.md       （連載 v2 QA 改訂版）
_FUTURES_SERIES_PLAN.md                （初版シリーズ計画）
_FUTURES_SERIES_PLAN_v2.md             （v2 シリーズ計画、320行）
_FUTURES_SERIES_PLAN_v2_skeleton.md    （v2 骨格）
_FUTURES_SERIES_PLAN_v2_prologue.md    （プロローグ）
_FUTURES_SERIES_PLAN_v2_part1.md       〜 part5.md   （5部構成詳細）
_FUTURES_SERIES_PLAN_v2_full.md        （v2 全文）
_FUTURES_SERIES_PLAN_v3_200ep.md       （v3 200エピソード案）
_FUTURES_SIGNAL_RESEARCH_v2.md         （シグナル研究）
futures-spec-draft.md                  （仕様素案 147行、2026-05-11）
futures-landing-page.html              （LP 元ドラフト、GitHub Pages 残置）
futures-membership-proposal.html       （会員企画書）
futures-internal-briefing.html         （内部ブリーフィング）
futures-deploy/                        （FTP配信成果物）
futures-series/                        （連載素材 v1）
futures-series-v2/                     （連載素材 v2）
book-chapters/                         （書籍章資料）
```

### 6.2 関連メモリ（`~/.claude/projects/-Users-nishimura-/memory/`）

- `project_futures_platform.md` — Futures 会員サイト本番稼働情報、AWS構成、Stripe・SendGrid・Supabase 統合
- `project_futures_landing.md` — LP @ journal.emerging-future.org/futures/、第一期100/10/2026、ブランド
- `project_futures_textbook.md` — 教科書「未来を読む力」公開URL、全20章219,653字、futures-textbook リポ
- `project_futures_studies_db.md` — 基盤DB（448研究者・99手法・507概念）
- `project_miratuku_membership.md` — ROOM 名称の現行プラン体系での利用
- `reference_miratuku_future_materials.md` — ミラツク未来予測資料一式（1,141予測→18領域MAP等）iCloud Documents

### 6.3 関連プロジェクト（spec L97-99 文脈の補強資料）

- `~/work/esse-sense-deep-knowledge-strategy.html`
- `~/work/deep-knowledge-future-forum-2026.html`
- `~/work/deep-knowledge-final-report-2026.html`
- `~/work/esse-sense-miratuku-strategy-2026.html`

---

## 7. 制約と未確認事項（追加調査が必要な項目）

- 第1期メンバーシップコミュニティ（2011-2017）の活動詳細・成果物・終了経緯 — **横断検索で未発見**、ヒアリングまたは Notion 補完が必要
- ROOM（2020-2025）の月例会テーマ・参加者数・エピソード — **同上、未発見**
- Futures 検討開始の最古の対話/議事録 — ローカルでは 2026-05-10〜11 の最終アーティファクトしか確認できず、それ以前の準備対話は Slack/Notion に存在する可能性
- 井上ゆきさんプロジェクトの具体内容・規模・スキーム — **未発見**
- LP（5番目のシリーズ）と仕様素案（5+Futures=6本目）の表記不整合 — 編集対応の要否は判断保留
- 教科書公開URL `https://yuyanishimura0312.github.io/miratuku-news-v2/textbook.html` の実 HTTP 到達性は本調査では未確認（メモリ記録ベース）
- Slack 履歴（mcp__slack 系ツール）は本セッションで未提供のためスキップ
- 機密性の高い金額・契約条件・認証情報は本資料に記載していない（指示遵守）

---

*記録: 2026-05-11 / knowledge agent / 推測排除・出典明記原則で記録*
