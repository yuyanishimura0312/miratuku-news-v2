# Track B-2 個別ブリーフィング: すでにある未来DB構築

## ミッション
Track B-1 が策定した 41 問のうち、**B-2 対象 14 問**に対し、人類学（AN）・哲学（PHIL）・文学（LIT）・神話学（MY）・伝統知（TK）の 5 traditions が**すでに考え、回答してきた知**を抽出し、新規データベースとして構築。

## 入力（必読）
1. `_PHASE_B_PLAN.md` — Phase B計画
2. `track-b1_handoff.md` — B-1 完成引継ぎ書（特に §6.1 B-2対象14問）
3. `track-b1-layered-history-report.html` 第6部 — 連結ID
4. Phase A 9 handoff.md（特に Track 9 Good Society）

## B-2 対象 14 問（B-1 §6.1 から）
- near (3問): Q-N04（場所性回帰）/ Q-N09（多元的人格）/ Q-N12（values空白補完）
- mid (4問): Q-M01（ケア・創造・共生）/ Q-M03（非西洋認識論主流化）/ Q-M07（多元的人格の社会）/ Q-M11（身体性復権）
- far (3問): Q-F02（世代間正義制度化）/ Q-F04（神話的人間-非人間境界）/ Q-F06（伝統知の知識主権）
- very-far (4問): Q-V01（サイクルA前期段階の組織形態）/ Q-V03（神話的予見と長期記憶）/ Q-V05（〈ゆっくりの権利〉の制度化）/ Q-V07（pluriverse的cosmology）

## 5 traditions DB
- AN: anthro 24,874 records / `/anthropology`
- PHIL: 9,583概念 / `/philosophy`
- LIT: 11,115概念 / `/lit`
- MY: 10,615物語 / `/myth-narratives`
- TK: 3,001グループ / `/traditional-knowledge`

## 新規DB設計
`~/projects/research/already-future-db/already_future.db`

スキーマ:
- `questions` (id, question_text, horizon, ctl1, msign_origin, b1_track_ref)
- `traditions` (id, name, description, db_source)
- `wisdom_records` (id, question_id, tradition_id, concept, era, civilization, wisdom_text, derivation_method, confidence)
- `cross_question_links` (id, question_a, question_b, shared_wisdom_count)

各問い × 5 traditions = 70セル中、根拠あるもののみ wisdom_records に格納。目標: 各問い5-15レコード = 計70-210レコード。

## 出力
- `track-b2-already-future-analysis.html` (15,000-20,000字)
- `track-b2-already-future-verification.html` (5,000-8,000字)
- `track-b2-already-future-report.html` (10,000-15,000字 + 図表6-10点)
- `track-b2_handoff.md`
- `~/projects/research/already-future-db/already_future.db`

## 必須要素（report.html）
1. 14問 × 5 traditions マトリクス
2. 「既に問われていた問い」（過去に同種の問いを立てた tradition がある）と「新たな問い」（過去に類例がない）の弁別
3. 各問いに対する歴史的回答パターン
4. 連結ID（B-3/B-4 への引継ぎ）

## protocols準拠
- 共通スパン使用 / CTL-1マッピング / 三系列差処理 / 【推定】【解釈】【未検証】タグ厳格使用 / 「研究の限界」 / Track 10 連結ID

## デザイン規約
赤白CI #CC1400、Noto Serif JP/Sans JP、textbook構造、絵文字なし、ダーク・印刷・モバイル対応、favicon esse-sense。Phase B Track B-1 を参照モデル。

## 完了報告
```
Track B-2 完了:
- 4HTML字数 / DB レコード数
- 14問 × 5 traditions のカバレッジ率
- 主要発見3点
- 研究の限界
```
