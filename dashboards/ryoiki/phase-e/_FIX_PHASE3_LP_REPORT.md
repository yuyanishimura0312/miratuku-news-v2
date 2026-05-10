# Phase 3 LP 最終校正レポート

対象: `eight-questions-lp-miratuku.html`
作業日: 2026-05-10
担当: 公開直前 LP 最終校正エンジニア

---

## 結論

レビュー3点（整合性 / デザインハレーション / UX）から指示された Critical 1 件 + Major 6 件の修正を完了。
LP の語彙体系は「8つの問い」から「7+1 の問い（7つの中核 + 1つの番外編）」へ移行。番外編バッジ付与・モバイルタップ領域確保・FOOTER/META書き換えまで反映済み。

---

## 修正項目と対応

### Critical-1: 「8.」「8つの問い」と新「7+1の問い」の語彙混在の解消 ✓

| 場所 | Before | After |
|---|---|---|
| `<title>` | 8 つの問い | 7+1 の問い |
| `<meta description>` | 8 つの問い | 7+1 の問い（7 つの中核 + 1 つの番外編） |
| top-bar brand small | 2100年に向けた8つの問い | 2100年に向けた7+1の問い |
| top-bar nav 中央リンク | 8つの問い | 7+1の問いを見る |
| hero-num-total | ／ Questions for 2100 | ／ 7+1 Questions for 2100 |
| hero-subtitle | 8 つの問い | 7+1 の問い（7 つの中核 + 1 つの番外編） |
| hero-en | Eight Questions | Seven plus One Questions |
| Section 1 タイトル | なぜ今、この 8 つの問いなのか | なぜ今、この 7+1 の問いなのか |
| Section 1 本文 (4箇所) | 8 つの問い／8 つ／8 問 | 7+1 の問い／7+1 |
| Section 2 ヘッダ | 8 つの問い／我々が選んだ 8 つの問い | 7+1 の問い／我々が選んだ 7+1 の問い |
| Section 2 nav aria-label / eyebrow | 8つの問い 一覧 | 7+1 の問い 一覧 |
| Q5 カード構造 | 通常 dq-card | dq-card-plus-one + dq-badge-plus-one バッジ |
| Q5 リード文 | いま立てた 8 つの問いは | いま立てた 7 つの中核の問いは |
| Q5 dq-link テキスト | もっと詳しく（番外編） | もっと詳しく（+1 の鏡章） |
| Q5 dq-why 末尾 | (none) | "ほかの 7 問と並列に並ぶのではなく、それらを背後から静かに映す「+1 の鏡」として置かれています" を追加 |
| Q6 dq-why | 8 つの問い | 7+1 の問い |
| Section 3 ヘッダ | 8 段の段差 | 7 段の段差と、それを背後から映す 1 枚の鏡 |
| Section 3 lead | 8 つ／8 段の段差 | 7+1 の問い／7 段の段差 + +1 の鏡 |
| Fig.01 タイトル | 8つの問いと時間軸 | 7+1 の問いと時間軸 |
| Section 4 本文 (5箇所) | 8 つの問い／8 問 | 7+1 の問い／7+1 |
| Section 5 タイトル | この 8 問の先にあるもの | この 7+1 問の先にあるもの |
| Section 5 action 01,02,03,04 desc | 8 つの問い／8つの問い（7+1） | 7+1 の問い |
| CTA section text | 8 つの問い | 7+1 の問い |
| CTA primary button | 8 つの問いを見る → | 7+1 の問いを見る → |
| Footer ABOUT | 2100年に向けた8つの問い | 2100年に向けた7+1の問い + 7つの中核と+1の番外編説明追加 |
| Footer NAVIGATION | 8つの問い | 7+1 の問いを見る |
| Footer disclaimer | 8つの問い | 7+1 の問い |
| Footer bottom | 2100年に向けた8つの問い | 2100年に向けた7+1の問い |

**+1 バッジの実装**: Q5 カードの先頭に `<div class="dq-badge-plus-one">+1 of 7+1 ／ 番外編・背後から映す鏡</div>` を追加。CSS で:
- `.dq-card-plus-one` 専用色（mt-4 Camel）と上部の accent-tint グラデーション背景
- `.dq-badge-plus-one` は Journal red の outlined badge（accent-warm border + accent-soft 背景）
- ライトモード対応も別途指定

### Major M-1: accent-warm 色の統一 ✓

LP の `[data-theme="light"]` の `--accent-warm: #ED2E3B` は既に書籍と同値で統一済み。LP 内に hardcoded `#CC1400` は grep の結果存在せず（全て `var(--accent-warm)` 経由）。SVG 内も同様に存在せず。**追加対応不要**と判定。

### Major M-2: モバイル top-bar nav タップ領域不足 ✓

`@media (max-width: 720px)` ブロックを拡張:
```css
.top-bar { height: auto; min-height: 64px; }
.top-bar-inner { flex-wrap: wrap; padding: 8px 16px; gap: 8px; }
.top-bar-actions { gap: 14px; flex-wrap: wrap; padding: 4px 0; row-gap: 4px; }
.top-bar-actions .back-link {
  min-height: 44px; display: inline-flex; align-items: center; padding: 10px 0;
}
.theme-toggle { min-height: 36px; padding: 8px 12px; display: inline-flex; align-items: center; }
```
これで 375px 表示時もタップ領域 44px を確保。

### Major M-3: meta description / footer ABOUT の「8つ」表記 ✓
（C-1 表に含む）

### Major M-4: CTA section 「8 つの問いを見る」リンク ✓
（C-1 表に含む）。CTA primary を「7+1 の問いを見る →」に更新。

### Major M-5: q-detail との整合 ✓
LP card の textはユーザー指示通り変更不要。Q5 を「+1 の鏡章」「+1 of 7+1」と明示することで、q-detail 側で「LPカード番号も併記」する形で吸収する設計と整合。

### Major M-6: top-bar の「8つの問い」リンク ✓
top-bar nav の `<a href="#questions">` テキストを「8つの問い」→「7+1の問いを見る」へ更新。

---

## ローカル検証

- grep `8段の段差` → **0 件** ✓
- grep `8つの問い` / `8 つの問い` → **0 件** ✓
- HTML タグバランス（python re）:
  - `<div>`: open 80 / close 80 / balance 0 ✓
  - `<article>`: open 8 / close 8 / balance 0 ✓
  - `<section>`: open 7 / close 7 / balance 0 ✓
- 行数: 1891 行（修正前 1847 行から +44 行）

---

## 残件 / 制約遵守確認

- ミラツクCI（焦茶 + Journal red）保持 ✓
- light mode header / Card 03 / Card 04 など修正済箇所には触れていない ✓
- card 内「もっと詳しく」リンク href は維持 ✓（Q3→q3, Q4→q4, ... の整合は Agent 2 が q-detail 側で番号体系の付け直し対応）
- footer Social・コピーライト等維持 ✓
- 文中「独立した 8 つの点ではなく」は「8 個の点」を否定して 7+1 を提示する文脈の意図的な数値で残置（コピー本来の意味として必要）

---

## 出力ファイル

- LP HTML: `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/eight-questions-lp-miratuku.html`
- 完了レポート: `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/_FIX_PHASE3_LP_REPORT.md`
