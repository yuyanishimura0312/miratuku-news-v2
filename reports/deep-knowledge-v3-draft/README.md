# deep knowledge — 新版 基礎論考（v3 draft 0.1）

「知性社会への途上で — 私たちが立ち直す場所」
deep knowledge の新版を構築するための、約1万字の基礎論考と背景情報レポートの素案。

## 位置づけ

| Version | Status | Date | URL / Location |
|---------|--------|------|----------------|
| v1.0 | 参照用残置 | 2026-05 | yuyanishimura0312.github.io/miratuku-news-v2/reports/deep-knowledge-book.html |
| **v2.0.0** | **完成版（正式公開）** | 2026-05-10 | journal.emerging-future.org/deep-knowledge/ |
| **v3 draft 0.1** | **新版素案（本ディレクトリ）** | 2026-05-15 | reports/deep-knowledge-v3-draft/ |

v3 は v2（21章本論）を継承しつつ、2026年4月-5月に立ち上がった新しい知見の地層（4補論／GC-DB／FVCP／DB Coverage Diagnostic／Tier -1 Meta Agent／katachi-100 等）を編集し、本論の最終句「知の獲得に翻弄される時代が終わり、知性とともに時代を横断しながら歩む時代が始まる」を発展的に書き継ぐ「橋渡しの素案」。

## アセット一覧

```
reports/deep-knowledge-v3-draft/
├── README.md           (本ファイル)
├── index.html          (基礎論考 / 序＋6章＋終 / 約10K字 + SVG4図 + pull quote)
├── background.html     (背景情報レポート / 11セクション / 約14K字 + 11表+問い箱)
├── miratuku-logo-light.png   (v2より複製)
├── miratuku-logo-dark.png    (v2より複製)
├── miratuku-mark-real.png    (v2より複製)
└── miratuku-mark-white.png   (v2より複製)
```

## 構成

### index.html — 基礎論考
- 序章「後ろ側に立つということ」（アイマラ語＋本論最終句から起点）
- 第1章「知性社会という未来像」
- 第2章「非主体的コミュニケーションの登場」
- 第3章「AGI の先で人類が立つ問い」（5局面）
- 第4章「歴史変動の精緻な読解」
- 第5章「神話・伝統知と『未来は後ろ側にある』」
- 第6章「現在の特殊性と普遍性の両立」
- 終章「深い知の作法」（読者へ手渡す5つの問い）

### background.html — 背景情報レポート（執筆台本）
1. なぜ新版が必要か（本論到達点と新版差分）
2. 6本柱の論拠系譜
3. 動員すべき DB 基盤（12 DB 一覧表）
4. 動員すべき方法論（FVCP / Meta Agent / 源泉サイクル / DB Coverage Diagnostic）
5. 2026年 4-5 月の取り組みからの洞察（指標表付き）
6. 反証耐性のための批判視点（Sentinel 指摘脆弱点3点）
7. 反証可能性条件5本（Popper 基準）
8. 章立て構成案 A／B／C 案
9. 読者旅程3アーキタイプ（研究者／経営者／実践者）
10. 未解明問い10件（次の full book に向けて）
11. 基礎論考の到達点と次のステップ

## 仕様

### デザイン（v2 と統合整合）
- デフォルトテーマ light（暖色クリーム #FAF6F0）／オプション dark（焦茶 #1C1410）
- アクセント色 light #D5202C / dark #FF3644
- タイポグラフィ Noto Serif JP（本文）+ Noto Sans JP（UI）+ Judson（数字 display）
- 上部固定 top-bar + reading progress bar
- 左サイドバー TOC（IntersectionObserver で active 章自動ハイライト）
- 章ごとに drop cap、推定字数、text-indent 1em
- 図解はテーマトークン化 SVG（インライン、currentColor + var(--accent)）
- pull quote callout（赤左ボーダー + クォート記号）
- @media print 対応（サイドバー非表示、ページブレイク制御）
- @media prefers-reduced-motion 対応

### コンテンツソース
- 基礎論考素材：12並列チーム（5本柱研究＋背景情報棚卸＋序章/結論/特殊性章/本論接続/章立て構成案/Sentinel批判検証）
- HTML 強化素材：第2波8チーム（pull quotes / SVG / 表題案 / 留保節 / 読者旅程 / 未解明問い / 背景HTML設計 / 反証可能性条件）
- 元 markdown：~/writings/deep-knowledge-v2-draft/

## 制作履歴

- 2026-05-15 12並列チーム編成で基礎論考1万字を構築
- 2026-05-15 ~/writings/deep-knowledge-v2-draft/ に markdown 版 2 本保存
- 2026-05-15 v3 draft HTML 化（基礎論考 index.html + 背景情報 background.html）
- 2026-05-15 第2波8チームで SVG 4図 + pull quote + 反証可能性 + 未解明問い等を追加生成
- 2026-05-15 v3-draft directory 完成（reports/deep-knowledge-v3-draft/）

## 次のステップ

1. 各章を独立した補論的ボリューム（1万-3万字）へ拡張
2. 4補論（製造／移動／HRORG／FOODAG）を新版の構造のなかに正式に位置づけ
3. 批判耐性の追加強化（Sentinel 指摘3脆弱点への明示応答節を本論版で500-800字規模で展開）
4. 読者の問いを受け取る構造（journal.emerging-future.org 上の問いの場）を準備
5. FTP デプロイ判断（v2 と並列に v3-draft/ として公開するか、別 URL で素案公開するか）

## ローカル確認

```bash
open ~/projects/apps/miratuku-news-v2/reports/deep-knowledge-v3-draft/index.html
open ~/projects/apps/miratuku-news-v2/reports/deep-knowledge-v3-draft/background.html
```

## 関連

- 元 markdown 草稿: `~/writings/deep-knowledge-v2-draft/`
- v2 正式版: `~/projects/apps/miratuku-news-v2/reports/deep-knowledge-book-v2/`
- v1 残置: `~/projects/apps/miratuku-news-v2/reports/deep-knowledge-book.html`
- 連載統合エージェント: `/katachi`（未来系軸）
