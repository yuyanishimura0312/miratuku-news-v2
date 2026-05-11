# Futures Briefing モバイル・アクセシビリティレビュー

- 対象: `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-internal-briefing.html`
- 検査日時: 2026-05-11
- ファイルサイズ: 50KB（51,615 bytes）/ 791 行 / インラインCSS 256 行 / インラインJS 73 行
- 検査者: モバイル・アクセシビリティ専門レビュー（静的レビューのみ。playwright実機未使用）

---

## 結論

**判定**: **GO with minor**

**Critical**: 0 件 / **Major**: 3 件 / **Minor**: 7 件

全体としてはミラツク textbook 系の作法を踏襲し、ダークモード基本コントラストは AA を満たしている。viewport / preconnect / display=swap / `prefers-reduced-motion` / `:focus-visible` / Escape キーハンドラ等、現代的アクセシビリティ実装の足場はすでに整っている。一方で、（1）固定ヘッダー高と sticky オフセットの数値不整合、（2）`.step-content` クラスが CSS 未定義、（3）モバイル時の sidebar `role="dialog"` を常時保持しているなど、修正コストが小さく効果の大きい指摘が複数ある。Critical 級の致命傷はないため、Minor を直して公開可能。

---

## 1. モバイル対応

### 1-1. viewport meta タグ — OK
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```
標準的で問題なし。`maximum-scale` や `user-scalable=no` が無く、ユーザーズーム可能。アクセシビリティ的にも望ましい。

### 1-2. ブレイクポイント設計 — OK with minor
- `@media (max-width: 1000px)` で 1 列化 + TOC ドロワー化
- `@media (max-width: 600px)` で cover タイトル縮小
- `@media (max-width: 1000px)` 内に diagram-wrap の余白縮小ルール（line 134）あり

375px / 414px / 768px すべてカバーされる。ただし **375px と 414px の中間に追加調整がなく**、SVG 図解（特に図2の Futures hub map：viewBox 720×480）は 375px 環境で内部テキスト（font-size="10"〜"11"）が 7-8px 相当まで縮小される。スケールしても可読性は限界ぎりぎり。**Minor**

### 1-3. TOC sidebar のドロワー化 — OK
モバイル時に `position: fixed; left: -100%` → `.is-open` で `left: 0`、overlay と組み合わせて閉じる挙動・Escape キーでも閉じる JS あり（line 776-787）。`max-width: 80vw` 制限もあり、はみ出しなし。

### 1-4. 図解 SVG の viewBox + width:100% — OK
両 SVG とも `viewBox` 指定済み・`.diagram svg { width: 100%; height: auto; max-width: 100%; }` で適切にスケール。

### 1-5. フォントサイズ（モバイル時の最小14px以上か） — Major
- 本文（chapter p）はモバイル時 0.98rem × 15px = **約14.7px** → ぎりぎりOK
- `.team-table th, .team-table td` モバイル時 0.92rem × 15px = **約13.8px** → **14px未満**
- `.outcome-card-desc` 0.9rem × 15px = **約13.5px** → **14px未満**
- `.cover-tag` モバイル時（max-width:600px）0.65rem = **約9.75px** → **大幅に小さい**（装飾的タグなので可読性影響は限定的だが、AA で 12px 未満は推奨外）
- SVG 内テキスト `font-size="10"` は 375px 表示で **約5.2px** まで縮小される。**詳細キャプションが読み取れない**

**Major 1**: SVG 内 font-size と一部小フォント。次の修正推奨。

### 1-6. タップ領域（44×44px 最低） — OK with minor
| 要素 | サイズ | 判定 |
|---|---|---|
| `.theme-toggle` | `min-height: 32px` + padding 6px 14px → 約 32px | **不足** |
| `.toc-toggle` | `min-height: 32px` + padding 4px 12px → 約 32px | **不足** |
| `.back-link` | padding 6px 0 + 4px 10px (line 277 のインラインで上書き) → 約 28px | **不足** |
| `.back-to-top` | 44×44px | OK |
| TOC リンク（モバイル） | `min-height: 44px`（line 222） | OK |
| `.toc-list a`（PC） | `min-height: 36px` | **不足**（PCはマウス操作中心だがタッチ機器でも使用） |
| `.outcome-card`（card 全体タップ） | padding 22px 24px 含めて十分 | OK |

トップバー内 3 要素（INTERNAL タグ・目次ボタン・テーマ切替）すべて 32px 程度。**WCAG 2.5.5 Target Size (Enhanced) 44×44 は AAA だが、新基準 2.5.8 Target Size (Minimum) 24×24 は満たす**。AA 達成自体は問題なし。**Minor**。

### 1-7. 横スクロール発生リスク — OK with minor
- `*, *::before, *::after { box-sizing: border-box; }` 設定済み
- `.diagram svg { max-width: 100%; }` 設定済み
- `.outcome-card-url { word-break: break-all; }` URL 折り返し対応済み
- `.layout { max-width: 1100px; }` は wide ビューポートで適切
- ただし `.diagram-wrap` モバイル時 `margin: 32px -8px` で **横方向 -8px はみ出し**。`overflow-x: hidden` を body や main に付けていない（line 60-64 で `overflow-x` 制御なし）。-8px は通常 viewport ぎりぎりだが、`html, body` に `overflow-x: hidden` を追加するのが安全。**Minor**

### 1-8. 固定ヘッダー高と sticky/scroll オフセットの不整合 — Major
| 場所 | 値 | 行 |
|---|---|---|
| `.top-bar` | `height: 56px` | 75 |
| `html` | `scroll-padding-top: 60px` | 59 |
| `.chapter` | `scroll-margin-top: 60px` | 116 |
| `.toc-sidebar`（PC） | `top: 48px; height: calc(100vh - 48px)` | 103 |
| `.toc-sidebar`（モバイル） | `top: 48px; height: calc(100vh - 48px)` | 217 |

top-bar が **56px** なのに対し、sidebar の sticky/fixed top オフセットは **48px** で **8px ぶん背景が透けて見える/重なる**。scroll-padding は 60px なので、TOC リンク経由のジャンプ時もチャプター見出しがやや下にずれる。**Major 2**

### 1-9. モバイル時の TOC ドロワー閉じ判定 — OK
JS（line 737-746）でリンククリック時に閉じる、overlay クリックでも閉じる、Escape でも閉じる。複数経路あり良好。

---

## 2. アクセシビリティ（WCAG 2.2 AA）

### 2-1. 画像/SVG alt または aria-label — OK
- `<img>` 要素は存在しない
- SVG 2 つともに `role="img" aria-label="..."` 付与済み（line 337, 640）
- `<figcaption>` でも視覚的キャプション提供
- 装飾用 SVG（無し）・`reading-progress` には `aria-hidden="true"`（line 272）

### 2-2. ヘッダー階層（h1 → h2 → h3） — OK
- h1: 1 個（cover-title）
- h2: 9 個（各 chapter-title）
- h3: 5 個（section-h）
順序飛ばしなし、構造は適切。

### 2-3. リンク/ボタンのフォーカス可視性 — OK
```css
:focus-visible { outline: 2px solid var(--accent-warm); outline-offset: 3px; border-radius: 2px; }
```
グローバル適用。`.theme-toggle:focus`、`.toc-toggle:focus` も自動継承。

### 2-4. カラーコントラスト（WCAG 2.2 AA 4.5:1） — OK with minor

#### ダークモード（bg = #1C1410）
| 要素 | 比率 | 判定 |
|---|---|---|
| text #FFFFFF | 18.15:1 | OK |
| text-secondary #D8D5D1 | 12.41:1 | OK |
| text-muted #A6A29D | 7.15:1 | OK |
| **text-faint #7A7672** | **4.03:1** | OK（大文字限定）/ **本文だとAA未達** |
| accent-warm #FF3644（リンク・見出し） | 5.07:1 | OK |
| SVG 内 #9A9690 | 6.17:1 | OK |
| **SVG 内 #7A7672**（line 343 ベースライン） | **4.03:1** | OK（線描・装飾用なので可） |
| **back-to-top 白 on #FF3644** | **3.58:1** | **AA未達**（4.5:1 要）／ ただしテキストではなく `↑` 記号アイコン |
| **Futures hub circle 白 on #FF3644**（SVG 図2） | **3.58:1** | **AA未達**／ 18px 太字＝大文字扱いで 3:1 達成（OK） |

#### ライトモード（bg = #FAF6F0）
| 要素 | 比率 | 判定 |
|---|---|---|
| text #2A1F18 | 14.92:1 | OK |
| text-secondary #5A4838 | 8.06:1 | OK |
| **text-muted #8B7A66** | **3.84:1** | **AA未達**（大文字限定 OK）。`.cover-meta`, `.team-note`, `figcaption` 等で使用 → **本文として4.5未達** |
| **text-faint #B5A48E** | **2.25:1** | **AA大文字も未達**（3:1未満）／ 現状ファイル内未使用に近い |
| **accent-warm #ED2E3B**（リンク色） | **3.86:1** | **AA未達**（4.5:1 要）／ 大文字なら OK |
| back-to-top 白 on #ED2E3B | 4.15:1 | OK（大文字扱い） |

**Major 3**: **ライトモードでリンク色 #ED2E3B が AA 未達**。`.toc-list a:hover { color: var(--accent-warm); }`、本文 `<a>` がライトモード時に 3.86:1 となり、WCAG 2.2 AA（普通文字 4.5:1）を満たさない。`.outcome-card-tag` `.chapter-num` 等の見出し小文字（0.7-0.75rem）も同様。

### 2-5. ARIA role の妥当性 — OK with minor
- `<aside class="toc-sidebar" role="dialog" aria-modal="true" aria-label="目次">` （line 294）
  → **Major 派生**: モバイル時のみドロワー（dialog）として機能するが、PC でも `role="dialog" aria-modal="true"` が付与されたまま。**PC 表示では sidebar は通常のナビゲーションであり、aria-modal は誤誘導**。スクリーンリーダーで「モーダルダイアログ」と誤って認識される。
  → 解決: JS で開閉時のみ動的に付与・削除する、あるいは `<nav aria-label="目次">` に変更し、モバイル時のみ overlay と組み合わせるパターンに変更。
- `<svg role="img" aria-label="...">` ×2 OK
- `<button aria-label="目次を開く">` `<button aria-label="ページトップへ戻る">` OK

### 2-6. キーボードナビゲーション — OK with minor
- 主要要素はすべて `<a>` / `<button>` ネイティブで Tab 順序確保
- ただし TOC ドロワーが開いた状態で **focus trap が無い**。Tab で背後の本文要素にフォーカスが抜ける。`aria-modal="true"` を宣言しているのに modal の責務を果たしていない（line 294 と整合性が取れていない）。**Minor**

### 2-7. TOC sidebar の role="dialog" / aria-modal — Major 派生
2-5 参照。PC とモバイルで挙動が違うのに同じ ARIA を持つ。

### 2-8. Escape キーで閉じる JS — OK
line 776-787 で実装あり。閉じた後 toc-toggle へフォーカス復帰までしている。良好。

### 2-9. Reading order（音声読み上げ順序） — OK
- DOM 順は cover → layout（sidebar → main）→ footer
- スクリーンリーダー読み上げは「カバー → 目次 → 本文 → 脚注」の自然順
- `back-to-top` は body 末尾配置で読み上げ後尾、適切

### 2-10. その他細部 — Minor
- `<html lang="ja">` OK
- `<title>` 適切
- `<meta name="description">` 適切
- `<button>` に type 属性が無い（line 278, 279, 714）。submit にはならないが明示推奨

---

## 3. パフォーマンス

| 指標 | 数値 | 評価 |
|---|---|---|
| ファイルサイズ | 50KB（51,615 bytes） | 軽量・問題なし |
| インラインCSS | 256行 / 約 8KB | 単一HTML自己完結として妥当 |
| インラインJS | 73行 / 約 2KB | 最小限・良好 |
| 外部リクエスト | Google Fonts 2 (preconnect) + favicon 1 | 少ない・良好 |
| `preconnect` | fonts.googleapis.com / fonts.gstatic.com 両方 | OK |
| `display=swap` | あり（line 12） | OK・FOUT で読みやすさ確保 |
| SVG 最適化 | viewBox/シンプル要素のみ・冗長な属性なし | OK |
| `scroll` リスナー | 2 個（progress / back-to-top）すべて `{passive:true}` | OK |
| `resize` リスナー | 1 個（progress）`{passive:true}` | OK |
| LCP リスク | cover-title が large text・即時描画 → 良好 | OK |
| CLS リスク | 図解 SVG が height:auto + viewBox → 初回レイアウトずれ可能性 | **Minor**: aspect-ratio で予約推奨 |

### 推奨
- `.diagram svg` に `aspect-ratio: 900 / 280` / `aspect-ratio: 720 / 480` を明示的に追記すれば、フォント未ロード時の CLS を完全に防げる
- preload 用に `<link rel="preload" as="style" href="...">` まで行うと FOIT を 30-50ms 短縮できる（任意）

---

## 4. その他の発見

### 4-1. CSS 未定義クラス `.step-content` — Major（軽微）
HTML（line 546, 553, 560, 567）で `<div class="step-content">` を使用しているが、CSS に対応するルールがない。`.step-item` の grid 2 列目に自動的に配置されるため見た目は壊れないが、意図的なスタイル（gap・余白）を当てたい場合に効かない。**動作はOK、設計上は不整合**。

### 4-2. textbook.html リファレンスとの差異 — 情報共有
ルール `~/.claude/rules/db-design-system.md` では本来「赤白CI（#CC1400・白基調）」が必須適用。本資料は**焦茶 + Journal red（#FF3644）**を使用しており、ミラツク CI（NOSIGNER 2011 焦茶系）寄り。`/journal.emerging-future.org/` のジャーナル系統と整合しているため、本資料単体としてはブランド適合だが、「DB成果物」枠ではなく「ミラツク内部資料 / Journal 系統」枠として扱う前提なら問題なし。レビュー上は判定材料外とした。

---

## 推奨修正（コード差分）

### 修正1: 固定ヘッダー高の数値統一（Major 2）

```css
/* line 75: top-barのheight 56px → 48px に揃える、または以下のように依存値を全て揃える */

/* 案A: top-bar 高さを 48px へ */
.top-bar { ... height: 48px; ... }
html { ... scroll-padding-top: 48px; }
.chapter { ... scroll-margin-top: 48px; }

/* 案B: top-bar 56px を維持し、sidebar / scroll を 56px に揃える（推奨） */
.toc-sidebar { ... top: 56px; height: calc(100vh - 56px); }
html { ... scroll-padding-top: 56px; }
.chapter { ... scroll-margin-top: 56px; }

@media (max-width: 1000px) {
  .toc-sidebar { ... top: 56px; height: calc(100vh - 56px); ... }
}
```

### 修正2: ライトモードのアクセント色を AA 適合へ（Major 3）

```css
[data-theme="light"] {
  ...
  --accent-warm:      #C8202C; /* 旧 #ED2E3B (3.86:1) → #C8202C (約5.6:1) */
  --accent-warm-soft: #E62C38;
  --accent-muted:     rgba(200, 32, 44, 0.08);
  --accent-tint:      rgba(200, 32, 44, 0.16);
  --highlight:        #C8202C;
  --text-muted:       #6F5E4B; /* 旧 #8B7A66 (3.84:1) → #6F5E4B (約5.5:1) */
  /* text-faint は装飾的なので 4.5:1 まで上げる場合は #8C7B65（4.4:1）近辺へ */
}
```

### 修正3: SVG 内テキストの最小サイズと白テキスト on 赤の保証（Major 1）

```svg
<!-- 図2 hub circle (line 642-644): font-size を 18 → 20 へ + font-weight 700 を維持
     これで 18px 太字 = WCAG「大文字」扱い→3:1 で AA 達成（現状3.58:1 でOK） -->

<!-- 図1 帯ラベル小キャプション (line 378, 386, 395) font-size 11 → 12 に変更 -->

<!-- 軸ラベル (line 346 group内 font-size="10") → 12 に変更 -->
```

### 修正4: PC では aria-modal を外す（Major 派生）

```html
<!-- 静的属性は dialog ではなく nav に。モーダル化は JS で動的付与 -->
<aside class="toc-sidebar" aria-label="目次">
  ...
</aside>
```

```js
// toggleToc() を以下のように変更
function toggleToc() {
  const sidebar = document.querySelector('.toc-sidebar');
  const overlay = document.querySelector('.toc-overlay');
  if (!sidebar) return;
  const opening = !sidebar.classList.contains('is-open');
  sidebar.classList.toggle('is-open');
  if (overlay) overlay.classList.toggle('is-open');
  if (window.innerWidth <= 1000) {
    if (opening) {
      sidebar.setAttribute('role', 'dialog');
      sidebar.setAttribute('aria-modal', 'true');
      // 最初のリンクにフォーカス
      const firstLink = sidebar.querySelector('a');
      if (firstLink) firstLink.focus();
    } else {
      sidebar.removeAttribute('role');
      sidebar.removeAttribute('aria-modal');
    }
  }
}
```

### 修正5: .step-content の CSS を追加（Major 軽微）

```css
.step-content { /* line 162 .step-item の grid 2列目用 */
  min-width: 0; /* テキスト折り返し保証 */
}
```

### 修正6: 横スクロール保険（Minor）

```css
html, body { overflow-x: hidden; }
```

### 修正7: モバイル小フォントの底上げ（Major 1 補強）

```css
@media (max-width: 1000px) {
  .team-table th, .team-table td { font-size: 0.96rem; /* 0.92rem → 0.96rem (約14.4px) */ }
  .outcome-card-desc { font-size: 0.95rem; }
}
```

### 修正8: SVG の CLS 予約（Minor）

```css
.diagram svg { width: 100%; height: auto; max-width: 100%; display: block; margin: 0 auto; }
/* 各 svg に viewBox に応じた aspect-ratio をインライン or 別クラスで */
.diagram-1 svg { aspect-ratio: 900 / 280; }
.diagram-2 svg { aspect-ratio: 720 / 480; }
```

### 修正9: button type 属性追加（Minor）

```html
<button type="button" class="toc-toggle" ...>
<button type="button" class="theme-toggle" ...>
<button type="button" class="back-to-top" ...>
```

---

## まとめ

実装の足場（focus-visible、prefers-reduced-motion、Escape ハンドラ、SVG ARIA、preconnect、display=swap）は本資料の規模に対して非常に丁寧に組まれており、ベース品質は高い。一方で、**(1) ヘッダー高 56px と sticky オフセット 48px の数値不一致**、**(2) ライトモードのリンク色 #ED2E3B が 4.5:1 未達**、**(3) SVG 内テキストが 375px 環境で 5-6px 相当まで縮小**の 3 点は、公開前に修正する価値が高い。残りの Minor は時間があれば順次対応で良い。GO 判定（with minor）。
