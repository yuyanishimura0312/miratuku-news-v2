# Futures II「問いをより深く」 — 運用設計書 v0.3

> **タイトル確定**: 「問いをより深く」— Futures II（未来のかたち 第二弾）
> **状態**: 制作運用設計版 — 100話を丁寧に書き切るための制作チーム・DB連携・codex運用・スケジュール
> **作成日**: 2026-05-11
> **対応する企画書**: `_FUTURES_SERIES_V3_PLAN_v0.2.md`（構造企画）／本書（制作運用）
> **西村氏判断**: タイトル「問いをより深く」、その他は推奨案で進行。100話制作のため各DBエージェントと連携、リサーチチーム立ち上げ、codexチーム運用

---

## 0. 制作運用の基本原則

### 0.1 「100話を丁寧に書き切る」ための4原則

1. **量より質、ただし完走を保証する** — 第一弾の連載品質69/100を超え、kurashi級（A評価）を100話全話で達成
2. **学術アンカーは事前検証** — 第一弾の致命的問題（未確認固有名詞）を Phase 1（企画段階）から doc-verify で防ぐ
3. **読者の問う力育成は機械的でなく丁寧に** — PRACTICE FOR YOU は futures2-cultivation-designer が1話ずつ専任設計
4. **3チーム並列 + Claude統合** — codex並列 / Claude統合パターン（feedback_codex_team_research準拠）

### 0.2 「リサーチチーム × DBエージェント × codexチーム」の三層構造

```
┌─────────────────────────────────────────────────┐
│ 第1層: 構造企画チーム（Claude / 中央統制）            │
│ futures2-planner（EP仕様策定）                      │
└────────────────┬────────────────────────────────┘
                 │ EP仕様（深化軸 + プロセス軸の指定）
                 ↓
┌─────────────────────────────────────────────────┐
│ 第2層: 並列リサーチ層（3チーム同時）                 │
│ ┌──────────────┬──────────────┬──────────────┐ │
│ │ DBチーム      │ Webチーム     │ codexチーム   │ │
│ │ 26+ DBエージェント│ futures2-web- │ codex-team    │ │
│ │ academic-oracle│ researcher    │ research      │ │
│ │ 経由で起動     │ （Web/学術）  │（深層・並列）  │ │
│ └──────────────┴──────────────┴──────────────┘ │
└────────────────┬────────────────────────────────┘
                 │ 統合素材パック
                 ↓
┌─────────────────────────────────────────────────┐
│ 第3層: 執筆・編集・公開（Claude / 順次）             │
│ writer → cultivation-designer → deeper           │
│   → editor（A評価ゲート）→ publisher              │
└─────────────────────────────────────────────────┘
```

---

## 1. 制作チーム編成（14体体制 + 既存活用2体）【2026-05-11 拡大版】

### 1.1 オーケストレーター

| エージェント | 役割 |
|---|---|
| **futures2-team** | kurashi-team / keiei-team / itonami-team 準拠の一気通貫オーケストレーター。テーマ1個入力で14体協働を実行 |

### 1.2 中核2体

| エージェント | 役割 | モデル |
|---|---|---|
| **futures2-planner** | 1話分のEP仕様策定（深化軸+プロセス軸の指定、第一弾呼応、PRACTICEフォーマット選定） | Opus |
| **futures2-cultivation-designer** | **第二弾固有**: PRACTICE FOR YOU 設計（8フォーマット×16中核問い×階梯Lv1-6） | Opus |

### 1.3 リサーチ並列3体

| エージェント | 役割 | モデル |
|---|---|---|
| **futures2-researcher** | DB統合リサーチ。26+ DBから素材収集（academic-oracle 経由でDB自動選択） | Sonnet |
| **futures2-web-researcher** | Web・学術論文の最新事例・直近2-3年の論文追加収集 | Sonnet |
| **futures2-codex-research** | codex-team research パターンで深層・並列調査（source_url必須） | codex CLI連携 |

### 1.4 執筆並列2体

| エージェント | 役割 | モデル |
|---|---|---|
| **futures2-writer** | 本文1,000-1,100字執筆。冒頭7型辞書遵守、ですます調・第二人称呼びかけ密度高め | Sonnet |
| **futures2-deeper** | DEEPER 300-400字執筆（古典+現代の2本立て） | Sonnet |

### 1.5 編集・公開2体

| エージェント | 役割 | モデル |
|---|---|---|
| **futures2-editor** | A評価ゲート編集（10チェック・第一弾比較で「深化したか」検証） | Opus |
| **futures2-publisher** | HTML生成・FTPデプロイ（journal.emerging-future.org） | Sonnet |

### 1.6 品質保証4体【第二弾固有・拡大時新設】

| エージェント | 役割 | モデル |
|---|---|---|
| **futures2-archivist** | 100話横断整合性管理（冒頭7型・呼びかけ密度・引用著者リスト・第一弾呼応網のマクロ統計） | Sonnet |
| **futures2-fact-checker** | 学術アンカー一次ソース照合専任（致命的問題系列の再発防止） | Sonnet |
| **futures2-reader-tester** | PRACTICE 実装可能性を5ペルソナで検証 | Sonnet |
| **futures2-progress-tracker** | Phase進行管理・週次レポート・マイルストーン報告 | Sonnet |

### 1.7 既存エージェント活用

| エージェント | 用途 |
|---|---|
| **doc-verify** | Phase 1 から介在。文書全体の品質検証（fact-checker と二重チェック） |
| **academic-oracle** | 26+ DB の自動選択ハブ。各話の素材収集時に最適なDBへルーティング |

### 1.8 ワークフロー（14体協働の標準フロー）

```
[企画] futures2-planner ← futures2-archivist（同型3連続警告）
   ↓
[リサーチ並列3] researcher + web-researcher + codex-research
   ↓
[検証] doc-verify + futures2-fact-checker（一次ソース照合）
   ↓
[執筆並列3] writer + deeper + cultivation-designer
   ↓
[読者検証] futures2-reader-tester（5ペルソナ通過判定）
   ↓
[編集ゲート] futures2-editor（A評価10チェック）
   ↓
[公開] futures2-publisher
   ↓
[統計更新] futures2-archivist + futures2-progress-tracker
```

---

## 2. DBエージェント連携マップ（26+ DB の役割分担）

第二弾100話の素材収集で活用するDBエージェントを、深化軸の問い別に整理。

### 2.1 学術系DB（理論アンカー）

| DB | 用途 | 関連する深化軸 |
|---|---|---|
| **/anthropology** | 人類学概念500・研究者252。先住民の知・場所性・複数性 | Q2/Q3/Q4 |
| **/philosophy** | 哲学概念8000-10000。問いの哲学・現象学・東洋 | Q1/Q5/Q8 全般 |
| **/poetics** | 詩学DB。問いの文体・言語表現の系譜 | 全話の文体設計 |
| **/lit** | 文学概念11,115。詩・物語形式の問い | 第5部の文学的装置 |
| **/mg** | 経営学概念3,369。組織・意思決定の問い | Q6/対話の系譜 |
| **/innovation-db** | イノベーション理論9,839。社会変革の問い | Q4/Q7 |
| **/traditional-knowledge** | 伝統知3,002グループ。先住民知・公案・口承 | Q2/Q7/新規軸 |
| **/great-figures** | 偉人9,178人。思想家系譜の追跡 | 全問のアンカー人物 |
| **/myth-narratives** | 神話90文化10,615件。神話を方法論として | 新規軸（神話） |
| **/yokai** | 妖怪DB1,010体。デスコラ存在論との接続 | Q4（複数世界観） |

### 2.2 フォーサイト系DB（現在地・実例）

| DB | 用途 | 関連する深化軸 |
|---|---|---|
| **/futures** | 第一弾100話の参照（呼応リンク作成） | 全話の第一弾呼応 |
| **/foresight-kb** | 309機関・45,323レポート。未来世代の議論・場所性の制度 | Q1/Q3/Q6 |
| **/signal-db** | 7,668シグナル。直近事例の予測力評価 | SIGNAL欄全話 |
| **/cla** | 統合CLA。深層メタファ・神話レベル | 深化軸の最深層 |
| **/megatrend** | 18メガトレンド・Three Horizons | 第1部現在地 |
| **/pestle-news** | 196,714記事。直近の社会変化 | SIGNAL欄実例 |
| **/cultural-intelligence** | 576,434記事・21カテゴリ | 文化的前提の問い直し |

### 2.3 実データDB（具体・検証）

| DB | 用途 | 関連する深化軸 |
|---|---|---|
| **/regulatory-japan** | 1,332法令。WFG法・関連制度 | Q1（未来世代制度） |
| **/policy-db** | 23府省30,118事業。ケア教育政策 | Q6 |
| **/macro-economy** | 61カ国42指標。比較認識論 | Q7（西洋以外） |
| **/historical-cases** | 20ケース184K字。BC334-AD2024 | 系譜編む（第3部） |
| **/cti-v2** | 文明転換指数。深化の長期軸 | 第5部の世代継承 |

### 2.4 特殊・教育系DB

| DB | 用途 | 関連する深化軸 |
|---|---|---|
| **/era-talents** | 12,958人物19能力次元。問う力の歴史的人材 | プロセス軸全般 |
| **/jpms** | 私学551校36,943件。問いの教育 | Q6（ケア教育） |
| **/pst** | 10アーキタイプ×60校×9時代×600偉人 | 階梯Lv1-6設計 |
| **/epo** | 176研究者×34 facet。研究者の問いの多様性 | Q8（複数の自己） |
| **/futurology** | 約30冊未来予測書籍カード | 深化軸の参考 |
| **/futurology-2** | CLA実データ・シナリオプランニング | 深化軸の方法論 |
| **/wayfinding** | ポリネシア伝統航法。未来洞察の実践知 | プロセス軸の所作 |

### 2.5 DB起動の優先順位（各話のリサーチ時）

```
1. /futures（第一弾呼応の確認）
2. /academic-oracle（学術アンカーのルーティング）
   → philosophy / anthropology / lit / traditional-knowledge から選択
3. /signal-db + /pestle-news（SIGNAL欄の直近事例）
4. /cla（深層メタファ確認）
5. 必要に応じて他DB
```

---

## 3. codex-team Research 運用設計

### 3.1 feedback_codex_team_research 準拠の運用

> ルール: 「リサーチはcodex-team researchを基本。Codex並列→Claude統合」

| ステップ | 担当 | 内容 |
|---|---|---|
| 1. 課題分解 | futures2-planner（Claude） | 1話のリサーチ課題を3-5項目に分解 |
| 2. 並列リサーチ | codex-team research × 3-5プロセス | 各項目を独立並列で深層調査 |
| 3. 検証 | doc-verify（Claude） | source_url実在確認・ハルシネーション検出 |
| 4. 統合 | futures2-researcher（Claude） | 検証済み結果をDB結果と統合 |
| 5. 確定 | futures2-planner（Claude） | 素材パック確定 |

### 3.2 codex運用の品質ガード（feedback_codex_quality 準拠）

- **source_url必須**: codex出力の全引用に検証可能なURL
- **実在プロジェクト限定**: 架空の事例を作らない
- **検証ステップ必須**: doc-verify を必ず通す
- **大量投入の制限**: 1話あたり最大5プロセス並列

### 3.3 codex起動コマンド設計

```bash
# 各話リサーチ時の標準パターン
cd ~/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series-v3
codex research \
  --topic "Ep{N}: {タイトル}" \
  --questions @questions.md \
  --parallel 3 \
  --source-url-required \
  --output ep{N}-codex-research.md
```

`~/.codex/AGENTS.md` 正本に準拠（feedback_codex_bridge 参照）。

---

## 4. 1話の制作ワークフロー（標準8ステップ）

### Step 1: 企画（futures2-planner）

入力: 話番号・深化軸の問い（C1-a〜C8-d）・階梯Lv・第一弾対応話
出力: EP仕様書（lens、PRACTICEフォーマット、引用候補、SIGNAL方向、第一弾呼応シーン）

### Step 2: リサーチ（3並列）

| 並列ライン | エージェント | 出力 |
|---|---|---|
| DB | futures2-researcher → academic-oracle 経由で各DB起動 | DB素材パック（理論アンカー） |
| Web | futures2-web-researcher | Web素材パック（直近2-3年事例） |
| Codex | futures2-codex-research → codex-team research | Codex素材パック（深層並列） |

### Step 3: 検証（doc-verify）

- 学術アンカーの年・訳者・出版社の照合
- SIGNAL欄の固有名詞の一次ソース確認
- ハルシネーション検出
- 重複検出（第一弾・既書話との）

### Step 4: 統合素材パック作成（futures2-planner）

3並列の出力を統合し、執筆チームへの素材パックを確定

### Step 5: 執筆（並列2体）

| エージェント | 出力 |
|---|---|
| futures2-writer | 本文1,000-1,100字（6段落、深化動作1つ・前提暴き1つ） |
| futures2-deeper | DEEPER 300-400字（古典+現代の2本立て） |

### Step 6: PRACTICE設計（futures2-cultivation-designer）

階梯Lv・8フォーマットから選定し、200-300字の稽古プロンプトを設計

### Step 7: 編集A評価ゲート（futures2-editor）

| チェック項目 |
|---|
| 深化したか（第一弾の問いを超えているか） |
| 冒頭パターン（前2話と同型でないか） |
| PRACTICEの実装可能性（読者が実際に試せるか） |
| 学術アンカーの正確性（doc-verifyとのダブル） |
| ですます調・第二人称呼びかけ密度 |
| 1,500-1,800字（PRACTICEを除く本文部分） |

A評価未達は writer/cultivation/deeper へ差し戻し（最大3ラウンド）

### Step 8: 公開（futures2-publisher）

- HTML生成（kurashi-no-katachi形式準拠）
- ローカル検証（タグバランス・モバイル表示）
- FTP デプロイ（reference_journal_emerging_future_ftp 参照）
- index.html 更新
- git commit + push

---

## 5. 100話制作スケジュール（1年計画）

### 5.1 全体タイムライン

| 期間 | フェーズ | 目標話数 |
|---|---|---|
| 2026-05〜06 | **Phase 0** 準備 | 0 |
| 2026-06〜07 | **Phase 1** 第1部試作 | 1-5話 |
| 2026-07〜09 | **Phase 2** 第1-2部 | 6-40話 |
| 2026-09〜11 | **Phase 3** 第3-4部 | 41-80話 |
| 2026-11〜2027-01 | **Phase 4** 第5部 | 81-100話 |
| 2027-01〜02 | **Phase 5** 校正・統合 | 100 |
| 2027-03 | **Phase 6** 公開開始 | 公開 |

### 5.2 Phase 0 準備（2026-05〜06）

| タスク | 担当 | 期限 |
|---|---|---|
| v0.3 運用設計（**本書**） | Claude | 2026-05-11 |
| 制作チーム8エージェント定義作成 | Claude | 2026-05-15 |
| /futures2-team オーケストレータ起動 | Claude | 2026-05-15 |
| 100話別タイトル骨子化（v0.4） | futures2-planner | 2026-05-20 |
| 第1話試作（Pilot Episode） | チーム全体 | 2026-05-25 |
| 試作レビュー・チーム調整 | 西村氏 | 2026-05-30 |
| Phase 1 始動準備 | Claude | 2026-06-01 |

### 5.3 各Phase の制作ペース

- Phase 1（試作期）: 5話 / 1ヶ月（じっくり）
- Phase 2-4（量産期）: 20話 / 2ヶ月 = 10話 / 月（週2-3話）
- Phase 5（校正期）: 全話のクロスチェック

### 5.4 週次ペース（Phase 2-4）

- 月: 2話分の planning + research 並列起動
- 火-水: 執筆（writer + cultivation + deeper）
- 木: editor 編集A評価
- 金: A評価通過分の publisher 公開、未達は差し戻し
- 土日: バッファ・休息

---

## 6. 品質保証設計（第一弾の課題を排除）

### 6.1 冒頭7型辞書（事前配分）

100話の冒頭タイプを企画段階で配分し、同型3連続を禁止:

| 型 | 上限 | 例 |
|---|---|---|
| institutional space型 | 10話 | 「ある会議室で〜」 |
| 自然描写型 | 15話 | 「秋の風が〜」 |
| 数字・固有名詞型 | 15話 | 「2024年〜」 |
| 引用型 | 10話 | 「『〜』と書いた人がいます」 |
| 質問型 | 15話 | 「あなたは〜」 |
| 比喩型 | 15話 | 「机の隅に〜」 |
| シーン描写型（具体個別） | 20話 | 「祖母の手が〜」 |

### 6.2 話法多様性（事前計画）

| 文体 | 話数 |
|---|---|
| 通常文体 | 70話 |
| 手紙形式 | 10話 |
| 対話形式 | 10話 |
| モノローグ | 5話 |
| シーン描写型 | 5話 |

### 6.3 「あなた」呼びかけ密度

- 各話最低1回の「あなた」呼びかけ
- PRACTICE FOR YOU は全話「あなた」主語
- 第一人称複数「我々／私たち」の集権性を意図的に緩める

### 6.4 学術アンカー事前検証

- Phase 1（企画段階）で doc-verify を必ず通す
- SIGNAL欄の現代固有名詞は一次ソース照合済みのみ採用
- 第一弾の致命的問題（立教大学「問いの図書館」等）の系列を再使用しない

---

## 7. リサーチ・チーム立ち上げ（Phase 0 最初の起動）

### 7.1 即時起動する3並列リサーチ

100話の骨格を確定するために、以下の追加リサーチをPhase 0で並列実行:

| # | テーマ | エージェント | 目的 |
|---|---|---|---|
| 4 | 16中核問いの拡張学術調査 | researcher | 各C-a/b 問いに対する追加学術アンカー収集（v0.4の各話素材） |
| 5 | 第一弾100話の象徴シーン抽出 | codebase-analyst | 第一弾全話から「読者の生活内に置き換え可能なシーン」リスト化 |
| 6 | 100話別タイトル骨子化 | futures2-planner（新設エージェント） | 100話×400字骨子 → v0.4 |

### 7.2 codex-team Research の試運転

最初の試運転として Episode 1 のリサーチを codex-team research で実行:

```bash
codex research \
  --topic "Ep1: 第一弾Ep100からの引き継ぎ ―『あなたが見つけた坂はどんな形をしていますか』" \
  --questions \
    "第一弾Ep100の正確な引用箇所と文脈" \
    "読者を共同編集者へ反転させる装置の前例" \
    "連載冒頭の優れた例（手紙・問いかけ・反転）" \
  --parallel 3 \
  --source-url-required
```

doc-verify で検証後、futures2-writer 起動。

---

## 8. 関連ファイル・URL

### 制作管理

| 種類 | パス／URL |
|---|---|
| 構造企画書 v0.2 | `~/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series-v3/_FUTURES_SERIES_V3_PLAN_v0.2.md` |
| 運用設計書 v0.3（**本書**） | 同ディレクトリ `_FUTURES_SERIES_V3_OPERATIONS_v0.3.md` |
| 100話骨子（予定） | v0.4 で同ディレクトリに作成 |
| Episode別 markdown | `futures-series-v3/ep001.md` 〜 `ep100.md` |
| Episode別 HTML | `futures-series-v3/ep001.html` 〜 `ep100.html` |

### 制作チーム定義

| エージェント | 定義ファイル |
|---|---|
| futures2-* 系統 | `~/.claude/commands/futures2-*.md`（新規作成予定） |
| futures2-team オーケストレータ | `~/.claude/commands/futures2-team.md` |

### 公開先

- 連載目次: https://journal.emerging-future.org/futures-series-v3/index.html（予定）
- 各話: https://journal.emerging-future.org/futures-series-v3/ep001.html〜
- FTP: reference_journal_emerging_future_ftp 参照
- 関連: https://journal.emerging-future.org/futures/ （第一弾）
- 関連: https://journal.emerging-future.org/8-questions/ （7+1の問いLP）

---

## 9. 次のアクション（即時実行）

| # | アクション | 担当 | 期限 |
|---|---|---|---|
| 1 | 制作チーム8エージェント定義作成 | Claude | 2026-05-15 |
| 2 | futures2-team オーケストレータ作成 | Claude | 2026-05-15 |
| 3 | Phase 0 追加リサーチ並列起動（16中核問い拡張・第一弾象徴シーン抽出） | researcher + codebase-analyst | 2026-05-12 |
| 4 | 100話別タイトル骨子化（v0.4） | futures2-planner | 2026-05-20 |
| 5 | Episode 1 試作 | チーム全体 | 2026-05-25 |
| 6 | メモリエントリ登録 | Claude | 2026-05-11（本日） |

---

**Document version**: v0.3（運用設計）
**Status**: 制作チーム編成 → 即時着手
**Next update**: v0.4（100話別タイトル骨子）— Phase 0 完了時
