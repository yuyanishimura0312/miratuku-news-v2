# Track C-5 個別ブリーフィング: 求められる人物の特性（担い手層）

## ミッション
C-3/C-4 で特定された偉業（great_actions 100-150 件）を担う人物の**心理特性・行動特性・領域性・専門性**を、era-talents 19 能力次元 × great-figures 10 意思決定アーキタイプ × jpms 人格-学校-活躍経路で構造化する。「ミラツクが見出すべき/育てるべき人物像」を 4 軸特性として確立する。

## 答えるべき問い
1. 100-150 偉業を担う人物の**心理特性**（19 能力次元の中核 5-7）はどう分布するか
2. **行動特性**（10 意思決定アーキタイプ）はどう分類されるか
3. **領域性**（CTL-1 6 軸: 個・関係・場所・時間・物質・知）の配分はどうなるか
4. **専門性**（学術 5 領域 / 業種 / 地域）の構造はどう描けるか
5. 過去（産業革命期）→ 現代 → 2030/50/70/2100 の担い手特性変化軌道はどう描けるか

## 主軸 DB
- C-3/C-4 great_actions.db
- era-talents.db（19 能力次元 + 6 時代 + 12,958 人物 + 47,284 レコード）
- great-figures.db（10 意思決定アーキタイプ + 9,178 人物 + 100 高解像度 event_structures）
- jpms.db v2（832 校 + 58,224 件関係者の声 + 5 数理モデル: 人格-学校-活躍経路）
- Phase B B-3 主体配分（個人 1 / コミュニティ 1 / 企業 4 / 自治体 1 / 国 4 / 国際機関 3 + 複合 17）
- pst.db（PST: 10 人格アーキタイプ × 60 校 × 9 時代 × 600 偉人、補助 DB）

## 必読
1. `_PHASE_C_PLAN.md` — Phase C 全体計画
2. `_PROTOCOLS.md` + `_FIGURE_STANDARDS.md` + `_INTEGRATION_FRAMEWORK.md`
3. C-3 完了済 `track-c3_handoff.md` + great_actions.db 初版
4. C-4 完了済 `track-c4_handoff.md` + great_actions.db 更新版（並走可）
5. Phase B `track-b3-good-society-report.html` — 主体配分
6. Phase A `track6-talent-report.html` — era-talents 19 能力 / 6 時代
7. era-talents 教科書: `~/projects/research/era-talents-db/textbook.html`
8. jpms-db v2 dashboard
9. `_PHASE_A_INHERITANCE_AUDIT.md` — 数値 source-of-truth

## 内部チーム編成
1. Lead Researcher（あなた=general-purpose）
2. Domain Expert（/era-talents、/great-figures、/jpms、/pst 起動可）
3. Data Analyst（19 次元 × 10 アーキタイプ × CTL-1 6 軸 × 専門性 4 軸マトリクス集計）
4. Writer（HTML 執筆）
5. Internal Reviewer

## 出力
出力先: `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-c/`
- `track-c5-actor-traits-analysis.html`（15K-18K 字 + DB 集計ログ）
- `track-c5-actor-traits-verification.html`（6K-8K 字、4 カテゴリ）
- `track-c5-actor-traits-report.html`（20K-25K 字 + 担い手類型図 8-12 点）
- `track-c5_handoff.md`

## 必須要素（report.html）
1. **100-150 偉業 × 担い手特性マトリクス**（偉業ごとの 4 軸プロファイル）
2. **4 軸構造化**:
   - 心理: 19 次元の中核 5-7 軸（創造性 / 戦略性 / 協働性 / 分析性 / 共感性 / 持続性 / 場所性 等）
   - 行動: 10 意思決定アーキタイプ（革新者 / 橋渡し / 守護者 / 挑戦者 / 組織者 / 物語者 / 翻訳者 / 育成者 / 観察者 / 統合者）
   - 領域: CTL-1 6 軸（個・関係・場所・時間・物質・知）
   - 専門性: 学術 5 領域（人文学 / 社会科学 / 自然科学 / 工学 / 芸術）× 業種 × 地域
3. **ミラツク優先課題 TOP10 × 担い手類型 = 「ミラツクが見出すべき/育てるべき人物像」**
4. **担い手特性の時代変化軌道**（過去・現代・2030/50/70/2100）
5. **B-3 主体配分（17 複合パターン）の担い手特性翻訳**
6. **jpms 人格-学校-活躍経路 5 数理モデルの組み込み**（教育インフラへの含意）
7. 連結 ID（C-1 サイクル / C-3 偉業 / C-4 zone / C-6 統合 への接続）
8. 研究の限界（19 次元評価の主観性・過去人物への現代用語適用問題含む）

## protocols 準拠（厳守）
- 共通スパン: near (2026-2035) / mid (2036-2055) / far (2056-2080) / very-far (2081-2100)
- 三系列差: briefing 値 / 公開値 / DB 実値 の honest 開示
- 【推定】【解釈】【未検証】タグ（19 次元の偉業適用は【解釈】必須）
- Phase A 数値継承: source-of-truth テーブル準拠（ET 12,958 / GF 9,178 等）
- 担い手特性の時代横断比較は CTI v2 6 次元との整合を取る

## デザイン規約
- 赤白 CI #CC1400 / Noto Serif JP + Noto Sans JP / textbook 構造
- 絵文字・アイコン禁止
- 図表は `_FIGURE_STANDARDS.md` 6 種テンプレ（特に担い手類型図・4 軸レーダーチャート）
- 参考モデル: phase-b/track-b3-good-society-report.html、era-talents-db/textbook.html

## 起動条件
Phase C Wave 3 起動条件: C-3 APPROVED 達成（great_actions.db 初版完成）。C-4 と並列起動可（共通入力は great_actions.db、独立観点）。

## 完了報告フォーマット
```
Track C-5 完了:
- analysis.html: {字数} / {DB 集計ログ数} / {主要発見 3 点}
- verification.html: {検証項目数} / {自己発見問題数}
- report.html: {字数} / {担い手類型図数}
- 偉業 × 担い手 4 軸マトリクス: {偉業数} × {軸数} = {総セル数}
- TOP10 × 担い手類型: {確定人物像数}
- 時代変化軌道: {過去/現代/4 ホライズンの軌道線}
- jpms 5 数理モデル組み込み: {モデル名} × {応用箇所}
- 他 Track 接続点: {C-1/C-3/C-4/C-6 への接続}
- 研究の限界（自己認識）: {主要 3 点}
- 引継ぎ書パス: track-c5_handoff.md
```

時間をかけて構いません。**質>速度**です。19 次元の評価は主観性が混入しやすいため、複数 DB（era-talents + great-figures + jpms + pst）の交差検証で堅牢性を担保。
