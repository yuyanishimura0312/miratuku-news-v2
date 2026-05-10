# deep knowledge book — v2.0.0（完成版 / Final）

NPO 法人ミラツクが 26 のデータベースを横断して描いた 21 章の知の地図。
journal.emerging-future.org に公開している正式版。

## 公開URL

- **新版（v2 / 正式公開）**: https://journal.emerging-future.org/deep-knowledge/
- 初版（v1 / 参照用に残置）: https://yuyanishimura0312.github.io/miratuku-news-v2/reports/deep-knowledge-book.html

## バージョン管理

| Version | Status | Date | Note |
|---------|--------|------|------|
| v1.0    | 参照用に残置 | 2026-05 | GitHub Pages 上の初版。URL は維持 |
| **v2.0.0** | **完成版（正式公開）** | **2026-05-10** | **journal.emerging-future.org/deep-knowledge/** |

完成版マーカー: commit `77d0c9d` を v2.0.0 として記録。以降の修正は v2.0.x として追記する。

## v2 で確定した仕様

### デザイン
- **デフォルトテーマ**: light（journal-shared.css と整合 / 暖色クリーム背景）
- **オプションテーマ**: dark（焦茶背景）— 右上のテーマ切替ボタンで切替、`localStorage` 永続化
- **公式ロゴ**: NOSIGNER 2011/2014 の miratuku CI を PDF から抽出して使用
  - `miratuku-mark-real.png`: 種クラスタ・暖色（light モード）
  - `miratuku-mark-white.png`: 種クラスタ・白（dark モード）
  - `miratuku-logo-light.png` / `miratuku-logo-dark.png` / `miratuku-logo-white.png`: 横並び全体
  - グレー背景は距離ベースのアルファ抽出で完全透過化
- **タイポグラフィ**: Noto Serif JP（本文）+ Noto Sans JP（UI）+ Judson（display 数字のみ）
- **アクセント色**: light `#D5202C` / dark `#FF3644`
- **イタリック使用は最小限**（accent 番号、タグライン、ウォーターマークすべて normal に）

### トップカバー
- メインタイトル: 「深い知が拓く2100年」 1 行（`white-space: nowrap`、clamp 26-52px）
- 「2100」のみ赤アクセント
- 92px 赤罫
- サブタイトル: 「未来学の検証から、人類学・哲学・伝統知を経て、2100年への道筋と選択」
- 背景ウォーターマーク: "deep" / "knowledge" の 2 段（5% 透明度）
- A BOOK / MAY 2026 / case 11 / メタグリッド / lead 段落 / v1 リンク / 連載リンク はすべて削除

### ヘッダー
- 左: 公式ロゴ + "MIRA TUKU" + small "deep knowledge"
- 左ロゴクリック → 当ページ最上部にスムーズスクロール
- 右: 月／太陽アイコン付きテーマ切替ボタン（pill 型、スマホはアイコンのみ）
- 背景は `var(--bg)` で本文と完全統一

### 図解 35 個
- すべて SVG 内の固定色を CSS 変数化（`--svg-text` / `--svg-card` / `--svg-line`）
- dark / light モードで文字色が自動切替
- 寒色（緑・橙・青）はミラツク CI 暖色（テラコッタ・アンバーブラウン・ディープブラウン）に置換
- 赤アクセント `#CC1400` → `#FF3644`（dark）、`#ED2E3B`（light）

### 本文 UI/UX
- 上部固定の reading progress bar（赤グラデ）
- 左サイドバー TOC（IntersectionObserver で active 章ハイライト）
- 各章末に prev/next ナビ（21 章すべて自動生成）
- 各章先頭に推定読了時間
- scroll-to-top フローティングボタン
- 序章 first paragraph に drop cap

### スマホ（≤760px）
- 左下に浮かぶ TOC FAB（タップでドロワー展開、86% 幅、左から）
- jh-bar 縮小（mark 32px、brand-name 12.5px）
- 本文 1rem / 1.92 line-height、TOC リンク 44px 最小高
- 図解は左右 -10px はみ出しでフル幅表示
- ≤380px: brand-text-sub 非表示、章タイトル 1.4rem、メタなし
- `prefers-reduced-motion` 対応

## ビルドフロー

```
v1 (reports/deep-knowledge-book.html)
   ↓ scripts/dkb-v2/build_dkb_v2.py    (CSS + nav + meta inject)
   ↓ scripts/dkb-v2/recolor_svgs.py    (SVG token swap)
v2 (reports/deep-knowledge-book-v2/index.html)
   ↓ lftp -> ftp2.gmoserver.jp
journal.emerging-future.org/deep-knowledge/
```

## 再ビルド・デプロイ手順

```bash
# 1. v1 を編集（必要なら）
vim reports/deep-knowledge-book.html

# 2. v2 を生成
python3 scripts/dkb-v2/build_dkb_v2.py
python3 scripts/dkb-v2/recolor_svgs.py

# 3. ローカルファイルを repo にコピー
cp /tmp/journal-upload/deep-knowledge/index.html reports/deep-knowledge-book-v2/index.html

# 4. FTP デプロイ
PW=$(security find-generic-password -l "onamae-ftp" -w)
lftp -u "sd0177751@gmoserver.jp,$PW" ftp://ftp2.gmoserver.jp <<EOF
cd /journal.emerging-future.org/deep-knowledge
put reports/deep-knowledge-book-v2/index.html -o index.html
put reports/deep-knowledge-book-v2/miratuku-mark-real.png
put reports/deep-knowledge-book-v2/miratuku-mark-white.png
put reports/deep-knowledge-book-v2/miratuku-logo-light.png
put reports/deep-knowledge-book-v2/miratuku-logo-dark.png
put reports/deep-knowledge-book-v2/miratuku-logo-white.png
bye
EOF
```

## アセット一覧

```
reports/deep-knowledge-book-v2/
├── README.md                       (本ファイル)
├── index.html                      (本体 1.15MB / 21 章 280K 字)
├── miratuku-mark-real.png          (公式 mark / 暖色)
├── miratuku-mark-white.png         (公式 mark / 白)
├── miratuku-logo-light.png         (公式 horizontal / brown text)
├── miratuku-logo-dark.png          (公式 horizontal / cream text)
└── miratuku-logo-white.png         (公式 horizontal / white text)

scripts/dkb-v2/
├── build_dkb_v2.py                 (CSS 全置換 + nav 注入 + 章 meta)
└── recolor_svgs.py                 (SVG トークン化)
```

## 制作履歴

- 2026-05-10 v2.0.0 完成版確定 (commit `77d0c9d`)
- 2026-05-10 タイトル階層・UI 簡素化（meta グリッド／lead 段落／eyebrow / 連載 nav / v1 banner 削除、テーマ切替追加）
- 2026-05-10 公式 PDF (`miratuku_logos_f.pdf`) から白ロゴ抽出、light default 切替
- 2026-05-10 ブックカバー再設計（背景 watermark / 4 セルメタ）
- 2026-05-10 SVG 図解 35 個のテーマトークン化、figure を編集インサート化
- 2026-05-10 8-questions 準拠デザイン、journal-shared.css 統合、FTP 初回デプロイ
