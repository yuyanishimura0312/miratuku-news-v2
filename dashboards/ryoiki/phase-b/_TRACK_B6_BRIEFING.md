# Track B-6 個別ブリーフィング: Phase B 統合HTML化 + ryoiki-index更新

## ミッション
Track B-1 〜 B-5 の全成果物を「Phase B 統合視点」から再編集し、**Phase A 10 トラックと並ぶ Phase B 統合 HTML** として完成させる。同時に上位 `ryoiki-index.html` の Phase B セクションを「進行中」→「完了」に更新する。

## 入力（必読・全 Wave 1-3 完了後）
1. `_PHASE_B_PLAN.md`
2. `track-b1_handoff.md` — 多層人類史 × 41問
3. `track-b2_handoff.md` — Type-A/B/C 三類型 + 三大クラスター + 4層蓄積期間モデル
4. `track-b3_handoff.md` — 5シナリオ × 8 critical junctures × 30問
5. `track-b4_handoff.md` — 7変化検出装置 × 24問評価 + initiatives.db
6. `track-b5_handoff.md` — Hot/Warm/Cool/Dead zones マップ + 優先 TOP10
7. Phase A `track10-integration-handoff.md` — 4 横断テーマ + 6 Mサイン領域
8. `ryoiki-index.html` — 上位インデックス

## B-6 統合の論理構造

### 第I部: Phase B 全体俯瞰
- Phase A → Phase B の論理連続性
- 5 トラック（B-1 基盤 / B-2 補完 / B-3 規範 / B-4 実装 / B-5 診断）の依存関係図
- 統合視点: 「ミラツクが向き合う問いの全体像」

### 第II部: 5 Wave 統合視点
- Wave 0（計画）: 6 トラック構造の必然性
- Wave 1（基盤）: B-1 41問の階層・ホライズン・CTL-1 三軸構造
- Wave 2（補完・規範）: B-2 既出wisdom × B-3 善い社会経路 の重なり/差異
- Wave 3（実装・診断）: B-4 装置カバレッジ × B-5 Hot/Dead zones の差分構造
- Wave 4（統合）: 全トラックを貫く「ミラツク独自視点」の抽出

### 第III部: 統合視点による発見
1. **問いの全体像**: B-1 41 + B-3 30-40 + B-4 24 = 約 95-105 問の重複・差異を整理
2. **wisdom の構造**: B-2 三大クラスター × B-3 5シナリオ × B-1 4ホライズン
3. **動きと装置**: B-4 装置カバレッジと B-5 zones の連結（hot zones には装置あり / dead zones には装置なし、の構造を確認）
4. **「真M由来」の連鎖**: B-1 真M4 / 準M14 / 概念整合15 / 単独T8 が B-3 シナリオ・B-5 zones にどう接続したか
5. **Phase A 6 Mサイン領域との整合性**: Phase A → B-1 → B-3 critical junctures（5/8 接続）の経路

### 第IV部: ミラツクとして取り組むべき優先課題
- B-5 TOP10 を Phase A Mサイン領域 + B-2 wisdom + B-3 シナリオで再ランキング
- 各優先課題に対する想定アプローチ（B-4 装置 + B-2 wisdom 起点）

### 第V部: 研究全体の限界と今後の研究課題
- 各トラックの限界の集約
- Phase C（次フェーズ）への申し送り
- 数値の三系列開示（briefing値 vs 実装値 の最終整理）

## 出力構造（4ファイル）
1. `track-b6-integration-analysis.html` (15,000-20,000字) — 構造化分析
2. `track-b6-integration-verification.html` (8,000-10,000字) — 検証ログ + 全 Track の qa 統合
3. `track-b6-integration-report.html` (25,000-35,000字) — 「ミラツクが向き合う問いの全体像」最終レポート
4. `track-b6_handoff.md` (3,000-5,000字) — Phase C 申し送り

## ryoiki-index 更新
- Phase B セクションを「Wave 進行中」→「全 Wave 完了」に更新
- B-1 〜 B-6 全トラックへのリンクを追加
- Phase A → Phase B の連続性を明示する図（ASCII または SVG）

## 必須要素

### report.html
1. Phase B 全体俯瞰図（5 Wave × 6 Track）
2. 95-105 問の統合マップ（B-1 41 + B-3 30 + B-4 24）
3. wisdom 構造図（B-2 三大クラスター × B-3 5シナリオ）
4. zones × 装置 接続図（B-4 × B-5）
5. 真M連鎖図（Phase A → B-1 → B-3 → B-5）
6. ミラツク優先 TOP10 統合ランキング
7. Phase C 申し送り

### verification.html
- 全 Track の doc-verify + sentinel 結果サマリ
- 数値整合性最終チェック（B-1〜B-5 全数値の照合）
- ハルシネーション総点検

## protocols 準拠（厳守）
- 共通スパン: near (2026-2035) / mid (2036-2055) / far (2056-2080) / very-far (2081-2100)
- 三系列差: 各数値で briefing値 / public値 / DB実装値 を honest 開示
- 【推定】【解釈】【未検証】タグ
- 研究の限界明示
- Track 10 連結ID 継承

## デザイン規約
- 赤白CI #CC1400
- Noto Serif JP（本文）+ Noto Sans JP（UI）
- textbook.html 構造（top-bar 48px + toc-sidebar 240px + main 760px）
- 絵文字・アイコン禁止
- Phase A track10 + Phase B B-1 を参照モデル

## 自己検証 4 カテゴリ
1. スナップショット不整合 — Wave 1-3 全数値の集計値整合
2. ハルシネーション — 各 Track の handoff 数値の引用正確性
3. カバレッジギャップ — Phase B 全要件への対応確認
4. チーム間不整合 — Phase A 値の継承一貫性

## Wave 4 起動条件
Wave 3（B-5）完了 + B-3/B-4 sentinel APPROVED 必須

## 起動方式
process-orchestrator または refinement-coordinator が直接統合執筆を担当（agent 1人）。または:
- 統合分析エージェント（chapter 1-3）
- 統合レポートエージェント（chapter 4-5）
- ryoiki-index 更新エージェント（並列）

の 3 並列も可。
