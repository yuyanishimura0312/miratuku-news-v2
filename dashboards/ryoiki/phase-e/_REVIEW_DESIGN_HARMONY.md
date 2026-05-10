# デザインハレーション検査報告

検査日: 2026-05-10
対象: 書籍 / LP / q-detail 8点（journal.emerging-future.org）
検査環境: Playwright Chromium, 1280px / 768px / 375px, Light/Dark 両モード

---

## 結論

**判定: GO with minor（軽微な修正を経て公開可）**
**ハレーション: Critical 1件 / Major 4件 / Minor 5件**

3ファミリー間の基本的な設計方針（焦茶基調・Noto Serif JP・赤いアクセント・余白リズム）は統一されており、全体的な品質水準は高い。ただし「SVG白背景がダークモードで島のように浮く問題（Critical）」と「3ファミリー間のカラートークンの不一致（Major）」が公開前に必ず解消すべき課題として存在する。

---

## カラーハレーション

### Critical-1: SVGの全面白背景がダークモードで白い島として浮き上がる

書籍（future-questions-book.html）および q-detail 全8ファイルの SVG 図解は、最初の矩形として `<rect width="880" height="460" fill="#FFFFFF"/>` を持つ。この白矩形は CSS の var() に接続されておらず、ダークモード（書籍 --bg: #1C1410、q-detail --bg: #1A140E）に切り替えると暗い背景の上に白い板が島状に浮き上がる。

実機確認済み：書籍ダークモード時の q1-diagram は白矩形の全面が浮き上がり、焦茶紙面との間に 100% の明度差が発生する。これはページ全体の没入感を破壊する最大のビジュアルノイズである。

影響ファイル: future-questions-book.html（8図解すべて）、eight-questions-q1,2,5,6,7,8-detail.html（各 SVG 内）

修正コード（SVG 側）:

変更前: `<rect width="880" height="460" fill="#FFFFFF"/>`
変更後: `<rect width="880" height="460" fill="transparent"/>`

CSS 側（figure.diagram の背景で制御）:

```css
/* 書籍 */
.diagram-wrap {
  background: var(--bg-alt);   /* ダーク: #261C16 / ライト: #F2EBDD */
}

/* q-detail */
figure.diagram {
  background: var(--bg-alt);   /* ダーク: #211915 / ライト: #F2EBDD */
}
```

ただし SVG 内のテキストや罫線の一部（stroke: #121212、fill: #1A1A1A 等）はライトモード用の暗色のままであり、背景透明化によってダークモードでは暗色テキストが暗色背景に埋もれる二次問題が発生する。根本的な解決には SVG 内のクラスにテーマ対応の CSS 変数を適用する必要がある（後述 推奨修正参照）。

---

### Major-1: accent-warm（アクセント赤）が3ファミリー間で3値に分裂している

| ファミリー | ライトモード accent-warm | ダークモード accent-warm |
|------------|------------------------|------------------------|
| 書籍       | #ED2E3B (hsl 356°, 84%, 53%) | #FF3644 |
| LP         | #CC1400 (hsl 6°, 100%, 40%) | #FF4030 |
| q-detail   | #D5202C (hsl 355°, 74%, 48%) | #F5505C |

書籍とq-detailは色相355–356°で近い。しかしLPは6°（赤いオレンジ寄り）かつ明度・彩度が大きく異なり、#CC1400 は旧 DB デザインシステムのCI色（db-design-system.md 定義）であって、書籍ファミリーのJournal redパレットとは別系統となっている。

書籍→LP へ遷移した読者は、ボタンやリンクの赤の質感が変わることで潜在的な違和感を受ける。

修正（LP を書籍・q-detail に合わせて更新）:

```css
/* eight-questions-lp.html の :root を変更 */
:root {
  --accent-warm: #D5202C;       /* 旧: #CC1400 */
  --accent-warm-soft: #ED2E3B;  /* 旧: #B01200 */
  --accent-muted: rgba(213,32,44,0.08);
}
[data-theme="dark"] {
  --accent-warm: #F5505C;       /* 旧: #FF4030 */
  --accent-warm-soft: #FF6B75;  /* 旧: #FF6050 */
}
```

---

### Major-2: 書籍の .col-end に旧CI色 rgba(204,20,0,0.04) がハードコードされている

future-questions-book.html 158行目:

```css
.col-end {
  background: rgba(204,20,0,0.04);   /* 旧 #CC1400 直打ち */
  border-top: 1px solid var(--accent-warm);  /* こちらは変数使用 */
}
```

修正:

```css
.col-end {
  background: var(--accent-muted);
  border-top: 1px solid var(--accent-warm);
}
```

---

### Major-3: SVG 内の #CC1400 が書籍の現行アクセント (#ED2E3B/#FF3644) と並置されている

future-questions-book.html の SVG 内に #CC1400 が 80 箇所、#FF3644 が 3 箇所 使用されており、同一 SVG 内で 2 種類の赤が混在している。

修正方針: SVG 内の SVG の <style> ブロックにテーマ対応クラスを追記。

```svg
<style>
  [data-theme="dark"] .q1-bad-arrow { stroke: #F5505C; }
  [data-theme="light"] .q1-bad-arrow { stroke: #D5202C; }
</style>
```

---

### Major-4: top-bar の border-top が3ファミリーで不統一

| ファミリー | top-bar border-top |
|------------|-------------------|
| 書籍       | なし（border-bottom のみ） |
| LP         | 3px solid var(--accent) = #121212 黒 |
| q-detail   | 3px solid var(--accent-warm) = 赤 |

修正（q-detail 基準に統一）:

```css
/* 書籍 .top-bar に追加 */
.top-bar {
  border-top: 3px solid var(--accent-warm);
}

/* LP .top-bar を変更 */
.top-bar {
  border-top: 3px solid var(--accent-warm);  /* 旧: 3px solid var(--accent) */
}
```

---

## タイポグラフィハレーション

### Minor-1: line-height が書籍/q-detail=1.95、LP=1.90 でわずかに異なる

統一値 1.95 への揃えを推奨する。

### Minor-2: cover-title の font-size が3者で異なる

| ファミリー | desktop | 375px |
|------------|---------|-------|
| 書籍       | 2.6rem  | 1.5rem |
| LP         | 3.2rem（hero-title） | 1.9rem |
| q-detail   | 2.2rem  | 1.7rem |

q-detail の cover-title を 2.2rem → 2.4rem に引き上げることで書籍との連続感が出る。

### Minor-3: Judson フォントが書籍のみに定義されているが使用箇所が存在しない

--font-display: "Judson" が定義されているが var(--font-display) の参照が CSS 内に見当たらない。不使用のフォントロードを削除することで Google Fonts への余分なリクエストを削減できる。

---

## SVG統合性

1. 白背景問題（Critical-1 再掲）: q1 の SVG は `<rect fill="#FFFFFF"/>` が全面に敷かれており、ダークモードで白板が浮き上がる。

2. テキストカラーのハードコード: SVG 内タイトルテキストが fill="#1B5E20"（暗緑）等で直打ちされており、ダークモードで暗色背景に沈む。

3. 緑（#2E7D32）×赤（#CC1400）の共存: RESPOND/AVOID の2分岐を示す設計意図は明確で許容できる。ただし #2E7D32 はダークモードの #261C16 背景に対してコントラスト比 2.9:1 程度（WCAG AA 未達）。ダークモード用に #66BB6A への切り替えを SVG 内スタイルで対応する必要がある。

4. figcaption の margin-top: q-detail=18px、書籍=14px で差異あり。統一値 16px を推奨。

---

## モバイルでの視覚崩れ

### 375px の確認結果

書籍（375px）: 問題なし。TOC トグルが表示され、ボタンの min-height: 48px が確保されている。

LP（375px）: top-bar のナビゲーションリンクが縦積みになり、文字が折り返される。

```css
/* LP のモバイルtop-bar修正 */
@media (max-width: 600px) {
  .top-bar { height: auto; padding: 8px 16px; flex-wrap: wrap; gap: 6px; }
  .back-link { font-size: 0.65rem; }
  .theme-toggle { padding: 3px 8px; font-size: 0.65rem; }
}
```

q-detail（375px）: top-bar が折り返しを起こし「本編・第1の問いに戻る」テキストが縦折れしている。

```css
/* q-detail のモバイルtop-bar修正 */
@media (max-width: 640px) {
  .back-link { display: none; }
  .top-bar-actions { gap: 10px; }
}
```

SVG のモバイル対応: viewBox と preserveAspectRatio="xMidYMid meet" が設定されており 375px でも縮小表示される。ただしテキストが 0.6–0.7rem 相当まで縮小するため図解内の日本語テキストが読めない水準になる。意図的なビジュアルとして許容するかどうかの判断が必要。

---

## ダーク／ライトモードの対称性

書籍はデフォルト data-theme="dark"、LP・q-detail はデフォルト data-theme="light"。書籍から「7+1の問いのページへ」リンクで LP に遷移すると、読者は焦茶暗背景から白背景へ突然切り替わる。

加えて localStorage のキーが3者で分断されている：

| ファミリー | localStorage key |
|------------|-----------------|
| 書籍       | future-q-book-theme |
| LP         | miratuku-theme |
| q-detail   | eight-q-theme |

修正: 3ファミリーで共通キーを使用する。

```javascript
const THEME_KEY = 'miratuku-journal-theme';
// 全ファイルで統一して使用
localStorage.setItem('miratuku-journal-theme', next);
const saved = localStorage.getItem('miratuku-journal-theme');
```

書籍のデフォルト data-theme="dark" を data-theme="light" に変更して3者を統一することを推奨する。

---

## デザイントークン統一案

```css
/* Miratuku Journal Shared Tokens (推奨) */
:root {
  --mj-bg:           #FAF6F0;
  --mj-bg-alt:       #F2EBDD;
  --mj-text:         #2A1F18;
  --mj-text-sec:     #5A4838;
  --mj-text-muted:   #8B7A66;
  --mj-accent-warm:  #D5202C;
  --mj-accent-warm-soft: #ED2E3B;
  --mj-accent-muted: rgba(213,32,44,0.08);
  --mj-border:       #D9CFBF;
  --mj-good:         #2E7D32;
  --mj-good-dark:    #66BB6A;
}
[data-theme="dark"] {
  --mj-bg:           #1A140E;
  --mj-bg-alt:       #211915;
  --mj-text:         #EFE6D7;
  --mj-text-sec:     #C7B9A5;
  --mj-text-muted:   #998A77;
  --mj-accent-warm:  #F5505C;
  --mj-accent-warm-soft: #FF6B75;
  --mj-accent-muted: rgba(245,80,92,0.12);
  --mj-border:       #3D2F26;
}
```

---

## スクリーンショット参照先

格納先: /tmp/design_review_screenshots/

主要確認ファイル:
- book_dark_first_diagram.png: 書籍ダークモードでのSVG白島問題を確認
- q1_dark_svg_visible.png: q1-detailダークモードでのSVG白島問題を確認
- lp_375_light.png: LPモバイルtop-bar折り返し問題を確認
- q1_375_light.png: q1-detailモバイルtop-bar折り返し問題を確認
