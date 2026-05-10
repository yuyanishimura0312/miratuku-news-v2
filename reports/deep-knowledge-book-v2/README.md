# deep knowledge book — v2 (journal edition)

新版（v2）。journal.emerging-future.org に公開しているデザイン刷新版。

## 公開URL
- 新版: https://journal.emerging-future.org/deep-knowledge/
- 初版（v1）: https://yuyanishimura0312.github.io/miratuku-news-v2/reports/deep-knowledge-book.html

## v2 で変わった点
- カラー: 8-questions 準拠（ミラツクCI 焦茶+暖色12色 + 赤アクセント `#FF3644`）、dark default
- フォント: Noto Serif JP + Noto Sans JP + Judson
- 図解35個: SVG内の固定色を CSS 変数化、テーマ対応（dark/light で文字色が反転）
- UI/UX: reading progress bar、IntersectionObserver による TOC scroll-spy、章末 prev/next ナビ、推定読了時間、scroll-to-top、序章 drop cap
- スマホ: ハンバーガー → TOC ドロワー、44px タップターゲット、本文 padding 調整、prev/next 縦並び
- バージョン管理: v1 残置、相互リンク、ダッシュボード4ファイルから両方アクセス可

## ビルドフロー
```
v1 (reports/deep-knowledge-book.html)
   ↓ scripts/dkb-v2/build_dkb_v2.py
   ↓ scripts/dkb-v2/recolor_svgs.py
v2 (reports/deep-knowledge-book-v2/index.html)
   ↓ lftp -> ftp2.gmoserver.jp
journal.emerging-future.org/deep-knowledge/
```

## 再ビルド手順
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
put reports/deep-knowledge-book-v2/index.html -o /journal.emerging-future.org/deep-knowledge/index.html
bye
EOF
```
