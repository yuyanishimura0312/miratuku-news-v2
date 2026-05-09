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
