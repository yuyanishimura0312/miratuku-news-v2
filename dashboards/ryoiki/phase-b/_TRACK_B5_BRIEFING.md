# Track B-5 個別ブリーフィング: B-3問い群 × 現代社会の動き状況測定

## ミッション
Track B-3「善い社会」問い群（30-40問）に対し、現代社会の実態にどの程度動きがあるかを Track B-4 の7変化検出装置で測定。**hot zones / dead zones の弁別**を実施。

## 入力（必読・依存）
1. `_PHASE_B_PLAN.md`
2. `track-b3_handoff.md` — 善い社会問い群（30-40問）
3. `track-b4_handoff.md` — 7装置カバレッジマトリクス + initiatives.db
4. Phase A 9 handoff

## B-5 出力構造

### 状況測定マトリクス
B-3 善い社会問い群（30-40問） × 7装置 = 210-280セル
- 各セルの「動きスコア」（0-5）
- 動きの方向性（推進・抵抗・両論）
- 動きの主体（政府・企業・市民・学術）

### Hot zones / Dead zones の弁別
- **Hot zones**: 7装置のうち5以上で動きあり、複数主体が参画
- **Warm zones**: 3-4装置で動きあり、特定主体に偏る
- **Cool zones**: 1-2装置で動きあり、限定的
- **Dead zones**: 動きほぼなし、構造的空白

### 善い社会問い群の優先順位
- 実装可能性（Hot zones）×重要性（B-3シナリオ評価）の二軸で再ランキング
- 「動きはあるが方向違い」の問いを特定
- 「動きはないが重要」の問い（戦略的空白）を特定

## 出力
- `track-b5-current-momentum-analysis.html` (15,000-20,000字)
- `track-b5-current-momentum-verification.html` (5,000-8,000字)
- `track-b5-current-momentum-report.html` (12,000-18,000字 + マトリクス + zoneマップ)
- `track-b5_handoff.md`

## 必須要素（report.html）
1. B-3問い × 7装置 状況測定マトリクス
2. Hot/Warm/Cool/Dead zones マップ
3. 「動きの方向違い」問いの特定（warning）
4. 「戦略的空白」問いの特定（opportunity）
5. ミラツクが取り組むべき優先領域TOP10
6. 連結ID（B-6 統合への引継ぎ）

## protocols準拠
共通スパン / 三系列差 / 【推定】【解釈】【未検証】 / 研究の限界 / Track 10連結ID

## デザイン規約
赤白CI、Noto Serif JP/Sans JP、textbook、絵文字なし、Phase B Track B-1 参照モデル

## B-3 sentinel verdict 申し送り（必読）
- **MJ-02 解消済**: critical juncture × Phase A Mサイン領域接続は「厳密接続 4/8 = 50% (真M+準M)」+「概念整合含む 6/8 = 75%」で honest 開示済
- **C-05 残課題**: B-3 30問 ↔ B-1 41問 ↔ B-2 14問 の連結IDマトリクスは B-5 で構築する責任あり
- **MJ-01/m1 解消済**: 主体配分は実体集計値で確定（個人1/コミュニティ1/企業4/自治体1/国4/国際機関3 + 複合17）

## B-4 doc-verify 申し送り（B-4 sentinel 後に最終確定）
- **B-4 重大ハルシネーション B-02**: 全装置不応答型 Q-N07/Q-M02 は実際 UPR で score 5 獲得。max_score≤2 問いは 24問中 0問
- **B-4 IR sections**: 1,769,821 が正、1,862,236 は誤
- **B-4 24問評価対象**: B-1 41問のうち near 13全 + mid M02/M04/M05/M08/M09/M12 + far F01/F03/F08 + very-far V02/V06。Q-V07 は対象外

## 入力データ pre-build（Wave 3 起動高速化用）

- `_TRACK_B5_INPUT_TEMPLATE.md` — 雛形構造
- `_TRACK_B5_INPUT_DATA.md` — **210セル動きスコア確定版** (coverage_scores DB直接参照)
  - Hot zones 4問 (G-N10/N11/N12/M02 全Care系列)
  - Warm 9 / Cool 9 / Dead 0 / N/A 8 (B-4 24問対象外)
  - 戦略的空白13問 (43.3%)
  - 最重要構造的非対称性: mid 10問のうち6問が装置観測不能 (Care核心 G-M01・世代間正義 G-M04/M05 含む)
  - ミラツク優先領域TOP10 暫定ランキング
- `_TRACK_LINKAGE_MATRIX.md` — **B-1 41 × B-2 14 × B-3 30 × B-4 24 連結IDマトリクス** (C-05 解消)
  - B-2×B-4交差わずか3問 (Q-N04/N09/N12 全near帯) = Phase B最重点
  - B-3 30問のうち6問はB-1/B-2/B-4対象外の独立 (mid/far/very-far集中)
  - B-1 §6.1×§6.2 補完設計の構造的観察

## B-5 リードへの実装指針（pre-build 成果統合後）

1. `_TRACK_B5_INPUT_DATA.md` の暫定弁別を起点とし、5シナリオ評価 (B-3) と組み合わせて優先順位を再構築
2. `_TRACK_LINKAGE_MATRIX.md` を活用して連結IDを確定 (C-05 解消の基盤)
3. B-3 sentinel verdict MJ-02 解消値「critical juncture × Phase A Mサイン領域接続 = 4/8 = 50% (厳密) / 6/8 = 75% (概念整合含む)」を継承
