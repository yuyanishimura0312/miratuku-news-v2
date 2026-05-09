# Track B-4 個別ブリーフィング: 変化検出装置の予測的応答評価 + 取り組みDB

## ミッション
Track B-1 4ホライズン問い群（24問）に対し、**7変化検出装置**の予測的応答力を評価し、すでにある取り組みを領域別に新規DB化。

## 7変化検出装置
1. **シグナル**（SG） — Signal DB 7,668 / `/signal-db`
2. **研究者プレスリリース**（UPR） — University PR 42,219 / `/university-pr`
3. **企業プレスリリース**（SGRD） — Sangaku R&D PR 36,734 / `/sangaku-rd`
4. **政策**（Policy） — Policy DB 30,118事業 / `/policy-db`
5. **企業ニーズ**（IR） — IR Collector 1,862,236 / `/ir-collector`
6. **資金調達**（funding） — Investment Signal 1,927ラウンド / `/investment-signal`
7. **産学連携**（sangaku-matcher） — 492,646レコード / `/sangaku-matcher`

## 入力（必読）
1. `_PHASE_B_PLAN.md`
2. `track-b1_handoff.md` § 6.2 B-4対象24問
3. `track-b1-layered-history-report.html` 第6部
4. 各装置DBの schema（`python3 ~/tools/db-agent.py schema {dbid}`）

## B-4 対象 24 問
- near (13問): 全Q-N01〜Q-N13
- mid (6問): Q-M02/M04/M05/M08/M09/M12
- far (3問): Q-F01/F03/F08
- very-far (2問): Q-V02/V06

## 評価マトリクス
24問 × 7装置 = 168セル の予測的応答力スコア（0-5）:
- 0: 装置がカバーしていない
- 1: 言及あるが弱い
- 2: 言及多数だが分析浅い
- 3: 構造化されたデータあり
- 4: 時系列で予測的
- 5: 強力な早期警戒シグナル

## 新規DB設計
`~/projects/research/initiatives-db/initiatives.db`

スキーマ:
- `questions` (id from B-1)
- `detection_systems` (id, name, type, db_source, total_records)
- `coverage_scores` (question_id, system_id, score_0to5, evidence_count, latest_signal_date)
- `initiatives` (id, question_id, organization, initiative_name, initiative_type, stage, horizon, source_db, source_id, summary)

目標レコード数: coverage_scores 168セル / initiatives 各問い10-50件 = 計240-1,200件

## 出力
- `track-b4-detection-systems-analysis.html` (15,000-20,000字)
- `track-b4-detection-systems-verification.html` (5,000-8,000字)
- `track-b4-detection-systems-report.html` (12,000-18,000字 + マトリクス + 装置別レポート)
- `track-b4_handoff.md`
- `~/projects/research/initiatives-db/initiatives.db`

## 必須要素（report.html）
1. 7装置 × 24問 のカバレッジマトリクス
2. 各装置の予測的応答力スコア（平均値）
3. すでにある取り組みのDB（領域別ピックアップ）
4. 装置間の補完関係
5. 連結ID（B-5への引継ぎ）

## protocols準拠
共通スパン / 三系列差 / 【推定】【解釈】【未検証】 / 研究の限界 / Track 10連結ID

## デザイン規約
赤白CI、Noto Serif JP/Sans JP、textbook、絵文字なし、Phase B Track B-1 参照モデル
