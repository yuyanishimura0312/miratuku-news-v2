# UX総合レビュー報告（公開前ゲート）

対象: 書籍版『未来への問い』(future-questions-book.html, 305KB / 13章 / 約3万字) + LP (eight-questions-lp-miratuku.html, 76KB / 8つの問いカード)
対象URL: https://journal.emerging-future.org/future-questions/ ／ https://journal.emerging-future.org/8-questions/#questions
レビュー日: 2026-05-10
検証手段: ローカルソース静的解析 + Playwright (Chromium) 実機検証 (375 / 768 / 1280 px) ＋ 4専門家並列レビュー
レビュー担当: ux-lead（西村勇也指示）

---

## 結論

**UX判定**: GO with minor (Critical 1件の修正後に GO)
**Critical UX欠陥**: 1 件（LP内のQ番号と詳細リンク不整合）
**Major UX問題**: 5 件
**Minor 改善余地**: 12 件

書籍版とLPはどちらも、長文HTMLとしては高水準の読書体験を実現している。タイポグラフィ・余白・コントラスト比（本文）はWCAG AAA水準で、ダークモード基調の焦茶+赤の配色は読書時間50分でも疲労感が抑えられている。スマートフォンでも横スクロール発生はなく、3ブレークポイントすべてで本文が破綻していない。図解SVG 8点もviewBox駆動でモバイル335pxまで縮約しても可読性が保たれている。Tab一発目に焦点が立ち上がり、focus-visibleもLP側では明示的にカスタムされている。

ただし、**LP内の8カードのうちQ3/Q4/Q6/Q7/Q8の5枚で、表示番号と「もっと詳しく」のリンク先ファイルが入れ替わっている**（例: Q3カード → q8-detail.html）という、公開LPとして許容できない致命的な不整合が残っている。これは公開停止レベルではないがリンクをクリックした読者が必ず戸惑う構造的欠陥なので、最優先で修正する。

加えて書籍とLPは「7+1の問い」と「8つの問い」という別の編成で動いており、章番号・問い番号・タイトルが対応していない。これは「同じ素材の二つの版」と読者が期待する暗黙の約束を裏切るが、文脈で「LPは一般読者向け翻訳・書籍は哲学的深堀り」と書き分けてはいるため、Critical でなくMajor として扱う。

---

## チーム別所見

### Visual Designer（視覚デザイン）

**強み**
- 焦茶ベース（#1C1410 / #261C16）+ Journal red（#FF3644）の組み合わせは、既存系列『kurashi-no-katachi』『jigyo-no-katachi』『henka-no-katachi』との家系的な視覚一貫性が担保されている。
- Noto Serif JP本文 + Noto Sans JP（UI） + Judson（数字）の3フォント体系がCI意図通りに機能。`font-feature-settings: "palt"` + 行間1.95 + letter-spacing 0.025emで、約3万字を読み通すリズムが揃っている。
- 章ごとの構造単位（chapter-lead 引用 / section-h 区切り / anchor-box 人文知4点 / scene-grid 2情景 / col-end 読者へのフック）が、視覚的に明確に区別されている（左罫の太さ・色・double線使い分け）。
- 図解SVG 8点はすべてviewBox `0 0 880 460` で統一され、モバイルでも335pxに縮約して破綻しない。診断結果ではどの図も最小335×175pxで表示できている（高解像度デバイスのRetinaなら可読）。
- LPの8カードは `--mt-1〜12` の12色から各カードに固有色を当て、機械的な8並びを「個別の問いの個性」として視覚化している。ダークモード基調にゴールデンオレンジ〜ディープブラウンの12色が並んでも、赤白CIの主役色から大きく逸脱しない。

**問題**
- **書籍CTAリンクのコントラスト不足（Major）**: `.cta-link` (rgb(255,255,255) on rgb(255,54,68)) のコントラスト比 = 3.58。これは「7+1の問い概要へ」と「MIRATUKU JOURNAL」両ボタンに該当。WCAG AA 通常テキスト 4.5:1 を下回る。フォントサイズが13.6〜12.75pxで太字（700）なので「大型テキスト」3:1基準は満たすが、太字の小型テキストはAA通常テキスト基準が適用されるべき微妙なケース。
- **theme-toggle ボタンのコントラスト境界値（Minor）**: 赤テキスト on 焦茶背景で 5.07。AAは満たすがアイコン的UI要素として小さい（10.5px）。
- **書籍デスクトップでTOCリンクの高さが36px（Major）**: 44pxタッチ基準を下回る。`.toc-list a { min-height: 36px }` 指定。デスクトップ用なので致命ではないが、トラックパッドでもクリック精度が下がる。モバイル/タブレットでは44pxに引き上げ済み。
- **LPカードのアクセント色 → 詳細リンクの色まで連動するため、12色が全部赤系の濃淡に寄せられているのは良いが、Q4の `--mt-12: #7A4033` と Q1の `--mt-1: #F0A671` の差が大きく、Q1だけがオレンジで浮く（Minor）**: 8カード並んだとき統一感がやや弱まる。
- **CTAセクション（LP）の見え方が"ライトモード化"する（Minor）**: ダークモード時、背景 `var(--ink) = #FFFFFF`、本文 `rgba(42,31,24,0.78)` で焦茶。これは意図的にKurashi newsletter inverseを再現したデザインで意図通りだが、ダーク基調の長い読書直後に突然ホワイトカードに切り替わるため、視覚的なホップが大きい。CTAの存在が際立つ意図と読めるが、書籍版のCTAは焦茶のままなので姉妹性がやや崩れる。

**スコア**: 17/20

---

### Interaction Designer（インタラクション）

**強み**
- 書籍版の TOC は デスクトップで sticky sidebar（240px幅）、モバイル/タブレットで側面ドロワー化（width 280px / max-width 80vw）。`toc-toggle` ボタンの `display:none` 切替はメディアクエリで明示。Playwrightでモバイル時に開閉が確実に動作することを確認 (`tocOpened: true`, `firstTocLinkBox` h=44px)。
- TOCの章番号 `+1` を `is-mirror` クラスで赤色強調、`prologue` `epilogue` を `is-prologue/epilogue` でイタリック差別化。読者が13エントリの目次の中で「7つの中核」「+1鏡章」「序終」を視覚で区別できる。
- 書籍版の reading-progress-bar は中央スクロールで10.4%（推定読了時間50分相当の進捗）を返した。実装は `requestAnimationFrame` ではなく scroll passive listener で軽量。
- back-to-top ボタンは scrollY > 600 で表示、44×44px のタッチ基準を満たす。
- 章間ナビゲーション（chapter-nav prev/next）が個別章下部に置かれ、序章・章末・終章で文脈に応じた前後ジャンプが可能（コードに含まれている）。
- `scroll-padding-top: 60px` + `section.chapter { scroll-margin-top: 60px }` で、TOCクリック時に章タイトルがtop-bar下に隠れないよう保護されている。Playwrightの実測でも各章 `top: 120px` の固定オフセットで停止。

**問題**
- **書籍版 → LPへの戻り動線が「7+1の問いのページへ」のみで、ヘッダーやフッターから常時アクセスできない（Major）**: top-barにLPへのリンクが無い。読者が章中盤から「8つの問いの一覧に戻りたい」と思ったとき、TOCを開いて「カバーへ戻る」「フッターまでスクロール」のいずれかしか選べない。LP側はtop-barに「レポート版のページへ」ボタンが常駐しているのに、書籍側は非対称。
- **LP内のFig.01（時間軸スロープ図）はモバイルで `display:none`（`@media max-width: 980px`）（Minor）**: モバイルではテキストカード列に置換されるが、書籍版の図解SVG 8点と異なりフォールバックの存在自体に気づきにくい。
- **theme-toggle のラベルが書籍「DARK / LIGHT」、LP「LIGHT / DARK」で並びが逆（Minor）**: 双方向遷移時に違和感を生む。
- **書籍版の cover-link.outline と cover-link.primary が、モバイルで `font-size: 0.74rem` (約11px) と相当小さい（Minor）**: デスクトップではちゃんと0.92rem (≈14.7px) だが、モバイルだけ縮約しすぎでCTAとしての存在感が削がれる。
- **書籍CTAリンクが2つ並んだとき、`<a class="cta-link" style="margin-left: 8px;">` で第二CTAをインラインで上書きしている（Minor）**: スマホで縦並びにならず、横並びのままはみ出す危険。Playwright では overflow は出ていないが、margin指定はインラインで分離していて保守性が低い。

**スコア**: 17/20

---

### Accessibility Expert（WCAG 2.2 AA）

**強み**
- `<html lang="ja">` 明示。両ページとも。
- 書籍 h1 = 1, h2 = 14（cover + 13章）、h3 は不使用で `section-h` クラスを使う（h3が無いのは惜しいが、見出しの階層は破綻していない）。LP は h1 = 1, h2 = 6 (5セクション + CTA), h3 = 10 (intro 2 + 8 dq-card)。
- 画像なし(書籍) または1枚（LP top-bar logo, alt="MIRA TUKU symbol"）。alt漏れゼロ。
- ボタン3つ全てに `aria-label` または text あり（buttonsNoLabel = 0）、リンク全てにテキストあり（linksNoText = 0）。
- LPは `:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px }` でフォーカス輪郭を独自設計（赤2px solid）。Tab一発目で `7+1の問いを見る →` がフォーカスし、輪郭が確認できた。
- コントラスト比は本文要素のほぼすべてが7.0以上を確保（最低 5.07 = `--accent-warm` テキスト on bg、AA達成、AAA未達）。本文 18.15、anchor-box 10.2、scene-card 12.41、toc-list 7.15。

**問題**
- **書籍版にカスタムフォーカス輪郭が無い（Major）**: ブラウザデフォルト `outline: rgb(0, 95, 204) auto 1px` が適用される。背景焦茶（#1C1410）に対する `#005FCC` のコントラスト比は 4.7:1 で AA は満たすが、書籍CIの赤白文脈と齟齬する青の輪郭が出る。LP は `:focus-visible { outline: 2px solid var(--accent) }` を設定済みなので、書籍にも同等の指定を追加すべき。
- **TOCドロワー（モバイル）に role/aria-modal/keyboard trap が無い（Major）**: `.toc-overlay` は `aria-hidden="true"` 付与済みだが、ドロワー自体に `aria-modal` `role="dialog"` が無く、開いたままTabするとフォーカスが背後の本文に飛ぶ。Escapeキーでも閉じない。
- **書籍版 .cta-link のコントラスト 3.58 (Major)**: WCAG AA 通常テキストの 4.5:1 を下回る。ボタンは13.6pxの太字なので大型テキスト基準（3:1）は満たすが、UIボタンとしては読み手によっては読みづらい。
- **LP top-bar の back-link (4本) のタッチ高さがモバイルで 19px（Major）**: Playwrightで `「8つの問い」 (w=13, h=131)` `「レポート版のページへ →」(w=13, h=271)` といった極端に縦長のbox計測値が出た。これは flex-wrap で改行して縦積みになった結果（モバイルで back-link がインラインのまま縦に折り返されている）。実質的なクリック領域は 13×19px 程度になり、44px × 44px 基準を満たさない。
- **scroll-behavior: smooth のreduced-motion 対応が無い（Minor）**: `prefers-reduced-motion: reduce` の指定無し。前庭機能症の読者には負担。
- **書籍 `[aria-hidden="true"]` がreading-progressとtoc-overlayにあるのは正しいが、`.diagram svg` に `aria-hidden` または `<title>` が無い（Minor）**: 8枚の図解はアニメーションなしの静的SVGで、すべて `<figcaption>` に説明テキストが置かれているため意図は伝わるが、SVGノードに `role="img"` + `<title>` を追加すれば screen reader で図を見つけやすくなる。

**スコア**: 14/20

---

### Content Reviewer（マイクロコピー・概念伝達）

**強み**
- 書籍カバー文「いま、地球は長い坂のひとつの分岐点に差しかかっています」は、3万字の本書全体を貫く比喩を一文で立ち上げる。LPの「70 年以上先の社会から振り返ったとき、『もっと早く考えておけばよかった』と後悔しないために、いま立てておくべき問いを選び抜きました」も同等の重み。両者とも哲学色を保ちつつ一般読者に届く距離感。
- 書籍各章の `chapter-lead`（赤罫付きイタリック引用）が章の主題を1段落で立ち上げる構造になっており、流し読みでも章の論点が掴める。
- LP `dq-example`（身近な例）→ `dq-section-label "なぜ大切か"` → `dq-why`（理論的背景）の3段構造が、各カードで一貫して機能。一般読者向けの「なぜ大切か」前置きは秀逸。
- 「7+1の問い」というラベリングは、書籍コンテキストでは「7つの分岐+1つの背面の鏡」というメタファーで論理的に一貫。終章で「ペンは静かに、共有された道具として、読者の側にも置かれています」というラインが読者を共著者の位置に置く編集設計。

**問題**
- **【CRITICAL】LPの問い番号と詳細リンクファイル名が大幅に錯綜している（Critical）**:
  - Q3「どこにいるか」 → eight-questions-q8-detail.html
  - Q4「複数の世界の見方」 → eight-questions-q6-detail.html
  - Q6「ケアを学ぶ教育」 → eight-questions-q3-detail.html
  - Q7「西洋以外の知」 → eight-questions-q4-detail.html
  - Q8「ひとつの自分」 → eight-questions-q7-detail.html
  
  Q1, Q2, Q5 のみリンクファイル名と一致。これは公開LPの読者が「もっと詳しく」をクリックした瞬間に必ず混乱する。recently再ナンバリングしたが detail ファイル名を更新し忘れた事故と推測。
- **書籍とLPの「7+1の問い」内容が対応していない（Major）**:
  - 書籍の問い構造（序章末で列挙）: 第1=未来世代の声 / 第2=先住民の知 / 第3=見えない世話 / 第4=複数の世界が並び立つ教育 / 第5=結果を変える力 / 第6=人ではない知性 / 第7=世代をまたぐ約束の器 / +1=問いを問う
  - 一方、LPの問い構造: Q1=未来世代 / Q2=先住民 / Q3=どこにいるか / Q4=複数の世界 / Q5=自分の問いを問う / Q6=ケアを学ぶ教育 / Q7=西洋以外の知 / Q8=ひとつの自分
  - **対応するのはQ1（未来世代）とQ2（先住民）のみ**。Q3-Q8は完全に別主題。書籍は「7+1=7つの問い+1つの鏡章」を「同じ坂の8段の足場」と説明しているが、LPは「8つの問い」と並列扱いで、5番目に自己反射の問いを置く構造。
  - 書籍カバーから「7+1の問いのページへ」というアウトリンクで LP に飛んだ読者は、「あれ、書籍と違う問いが並んでいる」と感じる。LP top-barの「レポート版のページへ」で書籍に来た読者も同様。
  - これは公開停止レベルではないが、両者の関係を **読者が不安にならない形で明示する一文** が必須。LPの hero-lead か intro 末尾、書籍のカバー副題か序章末に「LPと書籍では同じ7+1の問いを、それぞれ別の言葉で展開しています。詳細な対応関係は注釈をご覧ください」のような一文が要る。または、両ページの問いラインナップを統一する。
- **LPの hero-eyebrow「8.／Questions for 2100」 と hero-CTA「7+1の問いを見る」 で 8 と 7+1 が混在（Major）**: 同一画面の上部で「8」「7+1」「8つの問い」（subtitle小）が共存。読者にとっては書籍の「7+1」とLPの「8」を統一する手がかりが混乱する。
- **書籍 Q5/+1の問いに対応するLPカードのリンクラベルが「もっと詳しく（番外編）」（Minor）**: 「番外編」という言葉は、本書で +1 を「7つを背後から映す鏡」「最後に置かれた本書の結びの問い」と位置付けた重要性と齟齬する。「番外編」だと付け足しの軽い扱いに読める。書籍では「ほかの7章すべての背後に、静かに立ち続けています」と最重要級の扱い。
- **LP intro の「予測 vs 選択」フレーミングが秀逸だが、書籍序章は「分岐」「対話」「桟橋」のメタファー（Minor）**: 同じ思想を別語彙で説明しているのは健全な姉妹性だが、最初の入り口で読者が「予測ではなく選択」（LP）と理解した後、書籍では「論証ではなく対話」と微妙に違う対立軸を提示される。両者とも正しいが、橋渡しの一文が欲しい。
- **書籍カバー副題の `推定 readingtime 50分` の英単語混在（Minor）**: 一文だけ "readingtime" の英表記。日本語表記「読了 約50分」に統一するほうが書籍トーンに合う。
- **書籍 cover-link.outline ボタンラベル「7+1の問いのページへ」 vs LP top-barリンク「レポート版のページへ」（Minor）**: 「レポート版」という言葉が書籍版を指す呼称として LP 側だけで使われ、書籍側にはこの呼称が出てこない。「レポート版」は書籍内ではどこにも出てこないので、LPに来た読者が初めて遭遇する語彙。「書籍版」「本書」「レポート版」が混在している。

**スコア**: 16/20

---

### Responsive Design（参考点）

3ブレークポイント（375 / 768 / 1280px）すべてで `horizontalOverflow: false` を確認。

| 項目 | 375px | 768px | 1280px |
|------|-------|-------|--------|
| 書籍 SVG width | 335px | 720px | 664px (sidebar込み) |
| 書籍 chapter font-size | 14.7px | 14.7px | 16px |
| LP dq-title | 18.88px | 21.76px | 21.76px |
| 書籍 TOC | drawer | drawer | sticky sidebar |
| LP CTA-btn | フル幅 | 横並び | 横並び |

問題は「書籍デスクトップTOCの36pxタップ高さ」「LPの back-link がモバイルで縦折り返してタップ19px化」の2点のみ。

**スコア**: 17/20

---

## UX総合スコア: 81/100

| カテゴリ | スコア | キーポイント |
|----------|--------|--------------|
| Visual Design | 17/20 | 焦茶+赤の落ち着き / CTA色コントラスト3.58が惜しい |
| Interaction Design | 17/20 | TOCドロワー・進捗バー・章間ナビ完備 / 書籍→LP戻り動線非対称 |
| Accessibility | 14/20 | コントラスト本文は十分 / 書籍focus-visible未設定・モバイルback-linkタップ領域不足 |
| Content Quality | 16/20 | 編集水準高い / **LP内Q番号とリンク先の致命的錯綜** |
| Responsive Design | 17/20 | 3ブレークポイント全て破綻なし / SVG縮約成功 |

---

## クリティカルパス（修正必須・公開前）

### CRITICAL-1: LP内のQ番号と詳細リンクファイル名の不整合（最優先）

**何が問題か**
LPの8カードのうち、Q3〜Q8の5枚で、表示番号と「もっと詳しく」リンク先ファイルがずれている。

**修正コード**

ファイル: `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/eight-questions-lp-miratuku.html`

```diff
  <!-- Q3 -->
  <article class="dq-card" id="q-03">
    ... タイトル「どこにいるか」 ...
-    <a class="dq-link" href="eight-questions-q8-detail.html">もっと詳しく <span class="dq-link-arrow">→</span></a>
+    <a class="dq-link" href="eight-questions-q3-detail.html">もっと詳しく <span class="dq-link-arrow">→</span></a>
  </article>

  <!-- Q4 -->
  <article class="dq-card" id="q-04">
    ... タイトル「複数の世界の見方が並び立つ社会は可能か」 ...
-    <a class="dq-link" href="eight-questions-q6-detail.html">もっと詳しく <span class="dq-link-arrow">→</span></a>
+    <a class="dq-link" href="eight-questions-q4-detail.html">もっと詳しく <span class="dq-link-arrow">→</span></a>
  </article>

  <!-- Q6 -->
  <article class="dq-card" id="q-06">
    ... タイトル「ケアを学ぶ教育は、どこに向かうべきか」 ...
-    <a class="dq-link" href="eight-questions-q3-detail.html">もっと詳しく <span class="dq-link-arrow">→</span></a>
+    <a class="dq-link" href="eight-questions-q6-detail.html">もっと詳しく <span class="dq-link-arrow">→</span></a>
  </article>

  <!-- Q7 -->
  <article class="dq-card" id="q-07">
    ... タイトル「西洋以外の知を、対等な学問として認められるか」 ...
-    <a class="dq-link" href="eight-questions-q4-detail.html">もっと詳しく <span class="dq-link-arrow">→</span></a>
+    <a class="dq-link" href="eight-questions-q7-detail.html">もっと詳しく <span class="dq-link-arrow">→</span></a>
  </article>

  <!-- Q8 -->
  <article class="dq-card" id="q-08">
    ... タイトル「ひとつの自分でなくてもいい時代に向けて」 ...
-    <a class="dq-link" href="eight-questions-q7-detail.html">もっと詳しく <span class="dq-link-arrow">→</span></a>
+    <a class="dq-link" href="eight-questions-q8-detail.html">もっと詳しく <span class="dq-link-arrow">→</span></a>
  </article>
```

**ただし要確認**: 各 detail ファイルの中身が「LPの新Qx」と整合しているか。もし detail-q3-detail.html の中身が古い順序の Q3 (= LP新Q3とは別主題) のままなら、リンク修正後も内容が合わない。**検出後、両者の対応関係を西村と確認してから修正する**。

---

## Major（公開前に対応推奨）

### MAJOR-1: 書籍版にも `:focus-visible` を設定

ファイル: `future-questions-book.html` の `<style>` 内
```css
:focus-visible {
  outline: 2px solid var(--accent-warm);
  outline-offset: 3px;
  border-radius: 2px;
}
```
LP と統一する。

### MAJOR-2: 書籍 TOC ドロワーにモーダル属性 + Escape ハンドラ

`<aside class="toc-sidebar">` を `<aside class="toc-sidebar" role="dialog" aria-modal="true" aria-label="目次">` に変更。
JS末尾に：
```js
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const sidebar = document.querySelector('.toc-sidebar');
    if (sidebar && sidebar.classList.contains('is-open')) {
      sidebar.classList.remove('is-open');
      document.querySelector('.toc-overlay')?.classList.remove('is-open');
      document.querySelector('.toc-toggle')?.focus();
    }
  }
});
```

### MAJOR-3: LP top-bar の back-link を flex-wrap 対策

LP の `.top-bar-actions` がモバイルで縦折り返した結果、Playwrightで back-link タップ高さ19pxの計測。修正方向：
- モバイル(<720px)では back-link を非表示にし、ハンバーガーメニュー化
- もしくは `min-height: 44px` + `padding-top/bottom: 12px`を強制

```css
@media (max-width: 760px) {
  .top-bar-actions { gap: 8px; flex-wrap: wrap; }
  .top-bar-actions .back-link { 
    min-height: 44px; 
    display: inline-flex; 
    align-items: center; 
    padding: 10px 6px;
  }
}
```

### MAJOR-4: 書籍 .cta-link のコントラスト改善

現在 white on `--accent-warm` (#FF3644) で 3.58:1。修正案：背景を少し暗めの `--accent-warm-soft`（dark mode は #FF5560 でなく、AA達成のため新トークン #E51E2C を導入）。または `font-size: 16px` 以上 + 太字なら大型テキスト基準で許容、明示する。

簡易案:
```css
.cta-link { background: #D52030; }  /* dark固定で 4.6:1 */
.cta-link:hover { background: #FF3644; }
```

### MAJOR-5: 書籍版 → LP の戻り動線をtop-bar に追加

書籍 `<header class="top-bar">` に LP リンクを常設。
```diff
  <div class="top-bar-actions">
    <button class="toc-toggle" onclick="toggleToc()" aria-label="目次を開く">目次</button>
+   <a href="https://journal.emerging-future.org/8-questions/#questions" class="back-link">8つの問いへ →</a>
    <button class="theme-toggle" onclick="toggleTheme()">DARK / LIGHT</button>
  </div>
```
LPのtop-barと対称になる。

---

## Minor（公開後の改善）

1. **LP hero-eyebrow と hero-CTA の語彙統一**: 「8.／ Questions for 2100」 と 「7+1の問いを見る」 のどちらかに統一。書籍が「7+1」を採用しているので、LP側も「7+1の問い」「うち5番目は鏡となる自己診断」と説明する一文追加。
2. **書籍とLPの問い対応表を両ページに掲載**: フッター直前または序章末に「LP の Q1〜Q8 と本書の第1章〜+1章は、必ずしも一対一には対応しません。LPは一般読者向け、本書は哲学的展開として、別の言葉で再編成しています」の注釈。
3. **書籍カバーの「推定 readingtime 50分」を「推定読了 約50分」**へ
4. **theme-toggle の表記統一**: 書籍/LPで「DARK / LIGHT」または「LIGHT / DARK」のどちらかに揃える。
5. **`prefers-reduced-motion` 対応**: 両ページの `<style>` 末尾に
```css
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
```
6. **書籍 SVG 図解 8点に `role="img"` と `<title>`**: スクリーンリーダーが図の存在に気づくため。
7. **書籍デスクトップ TOC リンクのタップ高さを44pxへ**: `.toc-list a { min-height: 44px }`（現状36px）。
8. **「番外編」 → 「鏡章」「+1の問い」へ**: LP Q5 の `もっと詳しく（番外編）` を `もっと詳しく（+1の鏡章）` などに。書籍の語彙と統一。
9. **書籍 cover-link がモバイルで小さすぎる**: `font-size: 0.74rem` を `0.85rem` 以上へ。
10. **書籍 `<a class="cta-link" style="margin-left: 8px;">` のインライン style 撤去**: CSSクラスへ。
11. **LP の Fig.01 モバイル fallback の発見性を上げる**: モバイル列の上に「下に4つの時間軸の問い分布があります」と一言入れる。
12. **書籍版・LP共通で `<noscript>` フォールバック**: 進捗バー・theme-toggle・TOCドロワーは JS依存なので、JS無効環境のための代替メッセージかCSS-onlyフォールバック。

---

## 推奨改修順序（優先度順）

### Phase 1（公開前ゲート、即時）
1. **CRITICAL-1**: LP の Q3/Q4/Q6/Q7/Q8 詳細リンクファイル名修正（5箇所）
   - 修正後、各 detail ファイルを実際に開いて中身が正しい問いか目視確認

### Phase 2（公開前推奨、当日中）
2. MAJOR-1: 書籍 :focus-visible 設定
3. MAJOR-3: LP モバイルtop-bar タップ領域確保
4. MAJOR-5: 書籍 top-bar に LP戻りリンク追加
5. MAJOR-4: 書籍 .cta-link コントラスト改善

### Phase 3（公開後72時間以内）
6. MAJOR-2: 書籍 TOC モーダルa11y属性
7. Minor 1, 2: 8 vs 7+1 の語彙統一 + 対応表
8. Minor 5, 6: prefers-reduced-motion + SVG title
9. Minor 7, 8, 9, 10: 細部のタイポ・ボタン精度

### Phase 4（次期改修・後追い）
10. Minor 3, 4, 11, 12: 表記揺れ統一・fallback整備

---

## 公開可否の総合判定

**判定**: GO with one critical fix

公開前に **CRITICAL-1（LP詳細リンク5箇所修正）** のみ必ず実施。これは数分で対応可能で、対応しないと公開LPの致命的な誤動作になる。

その他の Major / Minor は公開後の数日以内のローリング更新でも構わないが、Phase 2 の4項目は同日中の対応を強く推奨する（書籍 focus-visible・LPモバイルタップ領域・書籍top-barのLP戻り・CTAコントラスト）。

書籍版とLPの問い構造の不一致（Q番号・章番号がほぼ別主題）は、すぐに修正するなら大きな再編集を要するため、**最低限「両者は別の編成です」と読者に伝える注釈を入れる**ことで Phase 3 で吸収する案が現実的。完璧に揃えるには書籍の章構造を「LPと同じ8問」に再編する大改訂が必要となり、これは公開後の検討事項として区切る。

---

## チームからの一言

書籍版の編集水準（とくに3万字を50分で読み切る読書設計、TOC・進捗バー・章間ナビ・人文知4アンカー・2情景の章構造の一貫性）は、ミラツク連載シリーズの中でも特に高いレベル。LPの「8カード × 12色のカードアクセント × 時間軸スロープ図」もKurashi系列の系譜を引き継ぎつつ、ナラティブの一般読者向け翻訳として独立したクオリティに到達している。

公開前ゲートで止まる致命傷は、LP内のリンクファイル名のずれという「公開直前の最後の編集事故」のみ。ここを通過すれば、公開しても恥ずかしくない水準にあると判定する。

7+1という編成と8問という編成の差は、本来であれば公開前に揃えるか、揃えないなら明示的にアナウンスする項目だが、両ページとも個別に完成度が高いため、注釈一文の追加で読者の混乱は十分緩和できる。

— UX Lead / 4 specialists
