# Track C-3 個別ブリーフィング: 現代の偉業の構造化 + great_actions.db 構築

## ミッション
各時代は「偉人の行動 → 社会変動 → ソーシャルイノベーション」の流れで形成される。Phase B の戦略的空白 13 問・critical junctures 8 個・Mサイン階層を踏まえ、**現代社会で求められる偉業（great actions）を構造化**し、新規 DB（`great_actions.db`）を構築する。great-figures（過去）と initiatives（推進中）の中間に位置する「行為」レイヤーを Phase C の核として確立する。

## 答えるべき問い
1. 偉人の行動 → 社会変動 → SI の現代版とは何か（過去 → 現代の系譜接続）
2. 戦略的空白 13 問に対応する「期待される偉業」候補は何か
3. great_actions.db のスキーマと最低 100-150 件のデータセットはどう構築するか
4. 過去偉業 → 現代偉業 → 未来偉業 の系譜接続はどう描けるか
5. 偉業の 10 アーキタイプ × 5 シナリオ × 4 ホライズン マッピングはどう成立するか

## 主軸 DB
- great-figures.db（9,178 人物 + 568 経営概念 + 1,050 イベント + 200 ケース + 100 高解像度 event_structures + 10 意思決定アーキタイプ）
- era-talents.db（12,958 人物 + 47,284 レコード + 19 能力次元 + 6 時代 + 590 未来予測）
- Phase B B-3 8 critical junctures（JCT-01〜08、2027-2090）
- Phase B B-5 戦略的空白 13 問（Pluriverse 5 + Care 2 + 世代間正義 2 + Slow Right 3 + 自己言及 1）
- Phase A Track 4 SIF 7,389 事象 + ソトコト SI 5 メタ型 × 15 サブ型
- initiatives.db（B-4 463 件、推進中事例として参照）

## 必読
1. `_PHASE_C_PLAN.md` — Phase C 全体計画
2. `_PROTOCOLS.md` + `_FIGURE_STANDARDS.md` + `_INTEGRATION_FRAMEWORK.md`
3. Phase B `track-b3-good-society-report.html` — 30 問 + 8 critical junctures
4. Phase B `track-b5-movement-measurement-report.html` — 戦略的空白 13 問 + zone 弁別
5. Phase B `track-b6-integration-report.html` — TOP10 + 主要発見 5 点
6. Phase A `track4-historical-report.html` — SIF 7,389 + HIC 20 + ソトコト 5 メタ型
7. C-1 / C-2 完了済 handoff.md
8. `_PHASE_A_INHERITANCE_AUDIT.md` — 数値 source-of-truth

## 内部チーム編成
1. Lead Researcher（あなた=general-purpose）
2. DB Builder（great_actions.db スキーマ設計 + 100-150 件データ収集 + sqlite 構築）
3. Domain Expert（/great-figures、/era-talents、/si-framework、/historical-cases、/innovation-db 起動可）
4. Data Analyst（10 アーキタイプ × 5 シナリオ × 4 ホライズン マトリクス検証）
5. Writer（HTML 執筆）
6. Internal Reviewer

## 出力
出力先: `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-c/`
- `track-c3-great-actions-analysis.html`（18K-22K 字 + DB 集計ログ）
- `track-c3-great-actions-verification.html`（7K-9K 字、4 カテゴリ）
- `track-c3-great-actions-report.html`（22K-28K 字 + 偉業類型図 10-14 点）
- `track-c3_handoff.md`
- **新規 DB**: `~/projects/research/great-actions-db/great_actions.db`
  - スキーマ: `actions(action_id, name, era, civilization, scenario_id, junction_id, mistake_label, archetype, locus_subject, scope_horizon, scope_ctl, predecessor_figures, success_pattern, failure_pattern, miratuku_relevance, source_db_refs, derivation_method)`
  - 最低件数: 100-150 件（過去偉業 50-70 + 現代登場中 30-50 + 期待される未来偉業 30）

## 必須要素（report.html）
1. **偉業 10 アーキタイプ × 5 シナリオ × 4 ホライズン マトリクス**（200 セル分類）
2. **戦略的空白 13 問 → 期待される偉業候補**（各空白 2-3 偉業）
3. **過去 → 現代 → 未来 偉業系譜接続**（great-figures 事例から現代偉業への翻訳）
4. **great_actions.db データセット 100-150 件のサマリ**（archetype 別 + scenario 別件数）
5. **偉業 × Mサイン階層**（真M / 準M / 概念整合）の対応関係
6. **B-4 R3 新類型「装置応答型 vs 期待型」の archetype への組み込み**
7. 連結 ID（C-1 サイクル / C-2 問い / C-4 zone / C-5 担い手 への接続）
8. 研究の限界（DB 構築上の選択基準・偏り含む）

## protocols 準拠（厳守）
- 共通スパン: near (2026-2035) / mid (2036-2055) / far (2056-2080) / very-far (2081-2100)
- 三系列差: briefing 値 / 公開値 / DB 実値 の honest 開示
- 【推定】【解釈】【未検証】タグ（特に「期待される偉業」は【推定】必須）
- Phase A 数値継承: source-of-truth テーブル準拠（GF 9,178 / ET 12,958 等）
- DB 構築の選択基準・除外基準を明示（再現可能性確保）
- great_actions.db スキーマは _INTEGRATION_FRAMEWORK.md と整合

## デザイン規約
- 赤白 CI #CC1400 / Noto Serif JP + Noto Sans JP / textbook 構造
- 絵文字・アイコン禁止
- 図表は `_FIGURE_STANDARDS.md` 6 種テンプレ（特に偉業類型図・系譜接続図）
- 参考モデル: phase-b/track-b3-good-society-report.html、phase-b/track-b5-movement-measurement-report.html

## 起動条件
Phase C Wave 2 起動条件: C-1 + C-2 両方 APPROVED 達成。C-1 のサイクル/4 ホライズン投影 + C-2 の 71 問単一台帳が C-3 偉業構築の前提。

## 完了報告フォーマット
```
Track C-3 完了:
- analysis.html: {字数} / {DB 集計ログ数} / {主要発見 3 点}
- verification.html: {検証項目数} / {自己発見問題数}
- report.html: {字数} / {偉業類型図数}
- great_actions.db 構築: {総件数} / {archetype 別件数} / {scenario 別件数} / {horizon 別件数}
- 戦略的空白 13 問対応: {期待偉業候補数}
- 過去-現代-未来系譜: {接続ペア数}
- 他 Track 接続点: {C-1/C-2/C-4/C-5 への接続}
- 研究の限界（自己認識）: {主要 3 点}
- 引継ぎ書パス: track-c3_handoff.md
```

時間をかけて構いません。**質>速度**です。great_actions.db は Phase C/D の核心 DB のため、スキーマ確定・データ品質に最大の注意を。
