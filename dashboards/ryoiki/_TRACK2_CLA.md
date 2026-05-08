# Track 2: CLA 126年分析と新たな物語の状況

## ミッション
1900-2026年の127年間にわたる因果階層分析（CLA）から、現代社会の立ち位置と問われている新たな物語の状況を抽出し、CLAが強みとするホライズン領域から将来に向けての問いとなるテーマ群を導出する。

## 答えるべき問い
1. CLA 91,550レコード（神話46,345・社会指標34,212・パラダイムシフト・キーワード索引）から、127年間の四層（litany→system→worldview→myth）の変遷はどう描けるか
2. 現代（2020-2026）の zeitgeist は何か。litany層・system層・worldview層・myth層のそれぞれで何が支配的か
3. 「新たな物語」が立ち上がりつつある兆候はどこにあるか（myth層の崩壊と再生）
4. CLAが強みとするホライズン領域は何年スパンか（過去パターンから未来推定への射程）
5. CLA分析を通じて見えてくる「未来に向けて問うべき領域」TOP10は何か

## 主軸DB
- リポジトリ: `~/projects/research/pestle-signal-db/`（dbId: cla, 19テーブル, 91,550行）
- DB CLI: `python3 ~/tools/db-agent.py query "SQL文" --db cla`
- 専門エージェント: `/cla` を活用
- 補完エージェント: `/futurology-2`（CLA+シナリオプランニング統合）、`/cti-v2`（文明転換指数との対比）

## 重要メモリ
- Memory: [Integrated CLA as primary] 統合版CLA（integrated_cla）が今後のCLA基礎データ。カテゴリ別ではなく統合版を使用
- Memory: [CLA Rebuild CI] CLA 36年分再構築（CI統合版）。2020年まで完了

## スラグ
`cla`（出力ファイル名: `track2-cla-{analysis|verification|report}.html`）

## 慎重な解析の重点
- 神話46,345件をデコードして「失われつつある神話」「立ち上がる神話」を特定
- 社会指標34,212件で litany 層の変遷を実証
- パラダイムシフト記録から worldview層の転換点を特定
- 過去126年で発生した「物語の交代パターン」を抽出し、現代がどの局面か診断

## 必須4要素（report.htmlに）
1. ホライズン×四層MAP（2030/2050/2070/2100 × litany/system/worldview/myth）
2. CLAが強みとするホライズン領域宣言（過去126年の知見から導く）
3. 問うべき領域TOP10（特に myth層・worldview層の問い重視）
4. 他トラック接続点（Track 1=FKと現在物語、Track 9=哲学/神話と worldview/myth）

## 留意点
- Track 1（FK）が「values領域0.45%空白・2070-2100構造的弱点」を発見済み。CLAは過去126年データで「values=worldview/myth層」を補える可能性
- ホライズン定義は `_PROTOCOLS.md` 完成後に従う
- 図版は `_FIGURE_STANDARDS.md` の6種テンプレを使用
