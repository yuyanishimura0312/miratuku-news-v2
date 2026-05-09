# Track C-7 個別ブリーフィング: HTML 成果物 + 公開

## ミッション
C-6 までの全成果を **3 種公開 HTML（master analysis / verification / report）+ phase-c-index.html + ryoiki-index 更新** として公開する。Phase A + Phase B + Phase C の統合インデックスを完成させ、Phase D（deep-knowledge 統合）起動準備を整える。

## 答えるべき問い
1. `phase-c-master-report.html` の章立て構成はどう設計するか（35K-45K 字）
2. `phase-c-master-analysis.html` の論理連続性はどう保証するか（25K-30K 字）
3. `phase-c-master-verification.html` の 4 カテゴリ統合表現はどう描けるか（12K-15K 字）
4. `phase-c-index.html` の 7 トラック導線はどう設計するか
5. `ryoiki-index.html` の Phase C セクション追加はどう統合するか

## 主軸 DB
- C-6 統合済成果物（four-in-one master figure + 統合ナレッジマップ + 5-10 問候補プール）
- 既存 ryoiki-index.html（Phase B 全完了状態）
- C-1〜C-5 全 report.html（公開 HTML 構築の素材）
- 既存 phase-b/_PHASE_B_PLAN.md + phase-b/track-b6-integration-report.html（参考モデル）

## 必読
1. `_PHASE_C_PLAN.md` — Phase C 全体計画 + ryoiki-index 更新方針 HTML スニペット
2. `_PROTOCOLS.md` + `_FIGURE_STANDARDS.md` + `_INTEGRATION_FRAMEWORK.md`
3. C-6 完了済 `track-c6_handoff.md` + 全 report.html
4. C-1〜C-5 全 report.html
5. 既存 `ryoiki-index.html`（Phase A + Phase B セクション構造）
6. 参考モデル: `phase-b/track-b6-integration-report.html`（最重要）+ `reports/deep-knowledge-book.html`
7. `_PHASE_A_INHERITANCE_AUDIT.md` — 数値 source-of-truth

## 内部チーム編成
1. HTML Builder Lead（あなた=general-purpose）
2. Data Aggregator（C-1〜C-6 全数値・図表の master 統合）
3. Designer（赤白 CI / textbook 構造の最終整形）
4. Reviewer（タグバランス検証 + リンク切れ検証 + アクセシビリティ確認）
5. Publisher（git push + GitHub Pages 反映確認）

## 出力
出力先: `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-c/`
- `phase-c-master-analysis.html`（解析結果まとめ、25K-30K 字）
- `phase-c-master-verification.html`（学術的検証、12K-15K 字、4 カテゴリ統合）
- `phase-c-master-report.html`（検証を踏まえた解析結果まとめレポート + 図表 12-18 点、35K-45K 字）
- `phase-c-index.html`（Phase C 7 トラック統合インデックス）
- `ryoiki-index.html` **更新**（Phase C セクション追加、`/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/ryoiki-index.html`）
- `track-c7_handoff.md`（Phase D D-0 への起動シグナル）

## 必須要素

### phase-c-master-report.html（35K-45K 字）
1. 序章: Phase A → B → C 全体の流れ
2. 章 1: C-1 サイクル/螺旋（時間軸層）抜粋
3. 章 2: C-2 問い統合（問い層）抜粋
4. 章 3: C-3 偉業構造化（行為層）抜粋 + great_actions.db サマリ
5. 章 4: C-4 zone マッピング抜粋 + warning/opportunity 偉業
6. 章 5: C-5 担い手特性抜粋 + ミラツク見出すべき人物像
7. 章 6: C-6 四位一体マスター図 + 統合ナレッジマップ
8. 終章: Phase D 起動への接続 + 5-10 問候補プール
9. 付録: Phase A 構造的限界 5 点の Phase C 継承状況 / Phase A 数値継承 source-of-truth
10. 図表 12-18 点（特に四位一体マスター図・統合ナレッジマップは見開き相当）

### phase-c-master-analysis.html（25K-30K 字）
- C-1〜C-6 各トラックの解析結果を論理連続的に統合
- DB 集計ログを統合（C-3 great_actions.db 件数 / C-4 紐付け統計 等）

### phase-c-master-verification.html（12K-15K 字）
- doc-verify 4 カテゴリの統合検証結果
- C-1〜C-5 各 verification.html の主要検証項目を統合
- Phase A 構造的限界 5 点の Phase C 継承点検結果
- sentinel APPROVED 判定の根拠開示

### phase-c-index.html
- 7 トラック（C-1〜C-7）への導線
- 各トラックの一行サマリ + analysis/verification/report 3 リンク
- great_actions.db ダウンロード導線
- Phase A + Phase B index への戻り導線

### ryoiki-index.html 更新
- `_PHASE_C_PLAN.md` の「ryoiki-index 更新方針」セクション HTML スニペットを正確に組み込み
- Phase A セクション + Phase B セクション + Phase C セクション の三段構成
- Phase D セクション placeholder（「展開 1: deep-knowledge 統合（着手予定）」）

## protocols 準拠（厳守）
- 共通スパン: near (2026-2035) / mid (2036-2055) / far (2056-2080) / very-far (2081-2100) の表記統一
- 三系列差: 公開 HTML でも DB 実値を一次値、briefing 値・公開値との差は注釈開示
- 【推定】【解釈】【未検証】タグの公開 HTML 適用率を verification.html で集計
- Phase A 数値継承: source-of-truth テーブル準拠の最終公開値確認
- B-6 タグバランス検証: 全 HTML で `<div>`、`<section>`、`<table>` 完全均衡（公開前必須チェック）
- リンク切れ検証: 内部リンク全件・外部リンク主要件をチェック
- favicon: https://esse-sense.com/favicon.ico

## デザイン規約
- 赤白 CI #CC1400（main） / #FF4030（dark mode）
- Noto Serif JP（本文）+ Noto Sans JP（UI）+ SF Mono（章番号）
- textbook.html 構造（top-bar 48px + toc-sidebar 240-260px + main 740-760px）
- 段落 text-indent 1em、行間 1.85-1.95、letter-spacing 0.025em、font-feature-settings "palt"
- top-bar に border-top 3px solid #121212、サイドバー TOC 章番号付き、ダークモード切替 JS、印刷時サイドバー非表示、モバイル<1000px 上部展開
- 絵文字・アイコンフォント禁止、派手色（青/緑/紫）非主役、文字飾り（影/輪郭）禁止、card 内背景多用禁止
- 参考モデル: phase-b/track-b6-integration-report.html（最重要）+ reports/deep-knowledge-book.html

## 起動条件
Phase C Wave 5 起動条件: C-6 sentinel APPROVED 取得済。C-7 は単一トラックでシーケンシャル実行（並列なし）。

## 完了報告フォーマット
```
Track C-7 完了:
- phase-c-master-analysis.html: {字数} / {図表数}
- phase-c-master-verification.html: {字数} / {検証項目数}
- phase-c-master-report.html: {字数} / {図表数}
- phase-c-index.html: 7 トラック導線確認 OK
- ryoiki-index.html 更新: Phase C セクション追加 OK / Phase D placeholder 配置 OK
- タグバランス検証: 全 HTML 完全均衡（div/section/table 各々）
- リンク切れ検証: 内部 N 件 / 外部 N 件 全件 OK
- 公開 URL: https://yuyanishimura0312.github.io/miratuku-news-v2/dashboards/ryoiki/phase-c/phase-c-master-report.html
- git push 完了 / GitHub Pages 反映確認 OK
- 他 Phase 接続点: Phase D D-0 起動準備完了
- 研究の限界（自己認識）: {主要 3 点}
- 引継ぎ書パス: track-c7_handoff.md
```

時間をかけて構いません。**質>速度**です。本トラックは Phase C 全体の公開顔として最終整形の精度が問われます。タグバランス検証・リンク切れ検証・アクセシビリティ確認を厳格に。
