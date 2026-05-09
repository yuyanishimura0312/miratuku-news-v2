# Track C-6 個別ブリーフィング: C-1〜C-5 取りまとめ + 検証

## ミッション
C-1〜C-5 を「**構造的なソーシャルイノベーション + 人物行動 + 人物特性**」の三位一体として精緻に取りまとめ、doc-verify 4 カテゴリ + sentinel 最終ゲートによる検証を経て確定する。Phase D（deep-knowledge 統合）への入力データを品質ゲート通過した形で確定する。Phase A 構造的限界 5 点を継承し、Phase C で同様の限界が生じていないかを点検する。

## 答えるべき問い
1. C-1 サイクル × C-2 問い × C-3 偉業 × C-5 担い手 の四位一体マスター図はどう描けるか
2. Phase A 構造的限界 5 点（9 DB 近代偏重 / 集計濃淡 / 派生間独立性 / GF 共有問題 / FK 84.4% 未指定率）は Phase C でどう継承されたか / 解消されたか
3. doc-verify 4 カテゴリ（スナップショット不整合 / ハルシネーション / カバレッジギャップ / チーム間不整合）× C-1〜C-5 の全数値整合は取れているか
4. sentinel APPROVED を取得するための残課題は何か
5. Phase D 起動入力データ（5-10 問候補プール）は確定したか

## 主軸 DB
- C-1〜C-5 全 handoff.md + analysis/verification/report
- Phase B B-6 主要発見 5 点 + Phase C 申し送り 8 件
- Phase A 構造的限界 5 点
- great_actions.db（C-3 + C-4 更新版）
- 各 Phase の数値 source-of-truth テーブル

## 必読
1. `_PHASE_C_PLAN.md` — Phase C 全体計画
2. `_PROTOCOLS.md` + `_FIGURE_STANDARDS.md` + `_INTEGRATION_FRAMEWORK.md`
3. C-1〜C-5 全 handoff.md + report.html
4. Phase B `track-b6-integration-report.html` — TOP10 + 主要発見 5 点 + 申し送り 8 件
5. Phase A `ryoiki-master-report.html` — 構造的限界 5 点 + メタテーマ M01-M15
6. `_PHASE_A_INHERITANCE_AUDIT.md` — 数値 source-of-truth

## 内部チーム編成
1. Synthesizer Lead（あなた=general-purpose）
2. doc-verify エージェント（独立検証、4 カテゴリ）
3. sentinel エージェント（最終ゲート、VETO 権付き）
4. refinement-coordinator（必要に応じ最大 3 ラウンド）
5. Writer（HTML 執筆）
6. Internal Reviewer

## 出力
出力先: `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-c/`
- `track-c6-synthesis-analysis.html`（18K-22K 字 + 統合検証ログ）
- `track-c6-synthesis-verification.html`（10K-12K 字、4 カテゴリ統合検証）
- `track-c6-synthesis-report.html`（25K-30K 字 + ミラツク羅針盤統合像 + 図表 14-18 点）
- `track-c6_handoff.md`（Phase D への引継ぎ）

## 必須要素（report.html）
1. **四位一体マスター図**: C-1 サイクル × C-2 問い × C-3 偉業 × C-5 担い手 の統合図
2. **Phase B 71 + Phase C 偉業 100-150 + 担い手特性 = 統合ナレッジマップ**
3. **Phase A 構造的限界 5 点の Phase C 継承点検**:
   - 9 DB 近代偏重: Phase C でも継承（過去偉業 50-70 件のうち近代偏重は不可避）→ 注釈開示
   - 集計濃淡: great_actions.db archetype 別件数の濃淡を明示
   - 派生間独立性: C-3/C-4/C-5 派生間の独立性確認
   - GF 共有問題: great-figures 9,178 中の Phase C 利用範囲を明示
   - FK 84.4% 未指定率: C-3 great_actions のソース DB 紐付け率を計測
4. **doc-verify 4 カテゴリ通過レポート**:
   - スナップショット不整合: Phase B 数値継承の正確性チェック
   - ハルシネーション: DB 実値との照合
   - カバレッジギャップ: briefing 必須項目への対応率
   - チーム間不整合: C-1〜C-5 間の数値・概念整合
5. **sentinel APPROVED 取得（または CONDITIONAL APPROVAL → refinement）**
6. **Phase D 入力データ確定**: 5-10 問候補プール（DQ-01〜DQ-08 例示済 + 追加 5-10 候補）
7. **C-1〜C-5 連結 ID マトリクス**（22 トラックの相互接続点）
8. 研究の限界（Phase C 全体の限界、Phase A 限界 5 点を継承した部分含む）

## protocols 準拠（厳守）
- 共通スパン: near (2026-2035) / mid (2036-2055) / far (2056-2080) / very-far (2081-2100)
- 三系列差: briefing 値 / 公開値 / DB 実値 の honest 開示（C-1〜C-5 全数値の最終整合）
- 【推定】【解釈】【未検証】タグの統合適用率を verification.html で集計
- Phase A 数値継承: source-of-truth テーブル準拠の最終確認
- B-3 MJ-02 二系列開示（厳密 / 概念整合）の Phase C 全 Track での継承確認
- B-6 タグバランス検証: analysis/verification/report 全 HTML で `<div>`、`<section>`、`<table>` 完全均衡

## デザイン規約
- 赤白 CI #CC1400 / Noto Serif JP + Noto Sans JP / textbook 構造
- 絵文字・アイコン禁止
- 図表は `_FIGURE_STANDARDS.md` 6 種テンプレ（特に四位一体マスター図・統合ナレッジマップ）
- 参考モデル: phase-b/track-b6-integration-report.html（最重要参考）

## 起動条件
Phase C Wave 4 起動条件: C-1〜C-5 全 5 トラック APPROVED 達成。C-6 は単一トラックでシーケンシャル実行（並列なし）。

## 完了報告フォーマット
```
Track C-6 完了:
- analysis.html: {字数} / {統合検証ログ数} / {主要発見 3 点}
- verification.html: {字数} / {4 カテゴリ通過状況} / {自己発見問題数}
- report.html: {字数} / {四位一体マスター図含む図表数}
- doc-verify 結果: {スナップショット OK 数} / {ハルシネーション OK 数} / {カバレッジギャップ OK 数} / {チーム間不整合 OK 数}
- sentinel 判定: APPROVED / CONDITIONAL APPROVAL / REJECT
- refinement ラウンド数: 0 / 1 / 2 / 3
- Phase D 入力確定: {問い候補プール総数} / {確定 DQ-NN 数}
- Phase A 限界 5 点継承点検: {継承件数} / {解消件数} / {未解消件数}
- 他 Phase 接続点: {Phase D D-0 への引継ぎ事項数}
- 研究の限界（自己認識）: {主要 3 点}
- 引継ぎ書パス: track-c6_handoff.md
```

時間をかけて構いません。**質>速度**です。本トラックは Phase C → Phase D の品質ゲートとして最重要。sentinel APPROVED 取得まで refinement 最大 3 ラウンドを許容。
