# Track C-4 個別ブリーフィング: 起こっている偉業 vs 期待される偉業の構造化

## ミッション
「**既に起こっているもの・起こりつつあるもの**」（B-5 zone 弁別の Hot/Warm zones）と「**今後登場が期待されるもの**」（Cool/Dead zones、戦略的空白 13 問）を構造化し、C-3 で構築された great_actions.db を更新する。「動きはあるが方向違い」warning と「動きはないが期待される」opportunity を弁別し、ミラツクの優先課題 TOP10 と偉業群の対応関係を確立する。

## 答えるべき問い
1. Hot/Warm zones（既存）と Cool/Dead/N/A zones（期待）の偉業差分はどう構造化されるか
2. B-4 463 initiatives は great_actions.db のどの archetype/scenario に紐付くか
3. ミラツク優先課題 TOP10 × 偉業マッピングはどう描けるか
4. 「動きはあるが方向違い」warning 偉業はどう特定されるか
5. 「動きはないが期待される」opportunity 偉業（戦略的空白起源）はどう特定されるか

## 主軸 DB
- C-3 great_actions.db（初版、100-150 件）
- Phase B B-4 463 initiatives + 168 セル
- Phase B B-5 zone 弁別（Hot 4 / Warm 9 / Cool 9 / Dead 0 / N/A 8）+ 戦略的空白 13 問
- Phase B B-6 ミラツク優先課題 TOP10（左上 4 + 右上 4 + メタ 1 + 中央 1）
- initiatives.db（推進中の動き）

## 必読
1. `_PHASE_C_PLAN.md` — Phase C 全体計画
2. `_PROTOCOLS.md` + `_FIGURE_STANDARDS.md` + `_INTEGRATION_FRAMEWORK.md`
3. C-3 完了済 `track-c3_handoff.md` + great_actions.db 初版
4. Phase B `track-b4-detection-devices-report.html` — 7 装置 × 24 行 = 168 セル + 463 initiatives
5. Phase B `track-b5-movement-measurement-report.html` — zone 弁別 + 戦略的空白 13 問
6. Phase B `track-b6-integration-report.html` — TOP10 + ミラツク優先課題
7. C-1 / C-2 完了済 handoff.md
8. `_PHASE_A_INHERITANCE_AUDIT.md` — 数値 source-of-truth

## 内部チーム編成
1. Lead Researcher（あなた=general-purpose）
2. Data Analyst（463 initiatives × great_actions マッピング + zone 差分集計）
3. Domain Expert（/signal-db、/sangaku-pr、/sangaku-rd、/innovation-db 起動可）
4. DB Updater（great_actions.db に推進状況・成熟度フィールド追加）
5. Writer（HTML 執筆）
6. Internal Reviewer

## 出力
出力先: `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-c/`
- `track-c4-actions-zone-mapping-analysis.html`（15K-18K 字 + 紐付けログ）
- `track-c4-actions-zone-mapping-verification.html`（6K-8K 字、4 カテゴリ）
- `track-c4-actions-zone-mapping-report.html`（20K-25K 字 + 差分マップ 8-12 点）
- `track-c4_handoff.md`
- great_actions.db **更新**（既存・期待・登場中フラグ + 463 initiatives 紐付け + maturity フィールド）

## 必須要素（report.html）
1. **既存偉業（463 initiatives 起源 = 推進中）vs 期待偉業（戦略的空白 13 問起源）の差分構造マップ**
2. **ミラツク優先課題 TOP10 × 偉業マッピング**（10 課題 × 各 3-5 偉業）
3. **warning 偉業の特定**（動きはあるが方向違い: 例 — 表面的 SDGs 対応・グリーンウォッシング型）
4. **opportunity 偉業の特定**（動きはないが期待される: 戦略的空白 13 問起源）
5. **463 initiatives × 100-150 great_actions の紐付け統計**（紐付けあり / 紐付けなし / 部分紐付け）
6. **zone 別偉業分布**（Hot 4 / Warm 9 / Cool 9 / Dead 0 / N/A 8 と great_actions の対応）
7. 連結 ID（C-3 偉業 / C-5 担い手 / C-6 統合 への接続）
8. 研究の限界（warning 判定の主観性含む）

## protocols 準拠（厳守）
- 共通スパン: near (2026-2035) / mid (2036-2055) / far (2056-2080) / very-far (2081-2100)
- 三系列差: briefing 値 / 公開値 / DB 実値 の honest 開示
- 【推定】【解釈】【未検証】タグ（warning 判定は【解釈】必須）
- Phase A 数値継承: source-of-truth テーブル準拠
- B-5 zone 弁別の二系列開示（Hot 4 厳密 / Warm 9 拡張）継承
- great_actions.db 更新時のスキーマ変更ログを残す（migration 記録）

## デザイン規約
- 赤白 CI #CC1400 / Noto Serif JP + Noto Sans JP / textbook 構造
- 絵文字・アイコン禁止
- 図表は `_FIGURE_STANDARDS.md` 6 種テンプレ（特に差分マップ・zone 分布図）
- 参考モデル: phase-b/track-b5-movement-measurement-report.html、phase-b/track-b4-detection-devices-report.html

## 起動条件
Phase C Wave 3 起動条件: C-3 APPROVED 達成（great_actions.db 初版完成）。C-5 と並列起動可（共通入力は great_actions.db、独立観点）。

## 完了報告フォーマット
```
Track C-4 完了:
- analysis.html: {字数} / {紐付けログ数} / {主要発見 3 点}
- verification.html: {検証項目数} / {自己発見問題数}
- report.html: {字数} / {差分マップ数}
- great_actions.db 更新: {追加フィールド数} / {463 紐付け済件数} / {warning 件数} / {opportunity 件数}
- TOP10 × 偉業マッピング: {対応偉業総数}
- zone × 偉業分布: {Hot/Warm/Cool/Dead/N/A 別件数}
- 他 Track 接続点: {C-3/C-5/C-6 への接続}
- 研究の限界（自己認識）: {主要 3 点}
- 引継ぎ書パス: track-c4_handoff.md
```

時間をかけて構いません。**質>速度**です。warning 判定は最も主観性が出やすい領域のため、判定基準を明示・複数視点で検証を。
