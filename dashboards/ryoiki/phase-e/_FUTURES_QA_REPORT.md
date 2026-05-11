# Futures Briefing 品質レビュー

**対象ファイル**: `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-internal-briefing.html`
**最終確認時刻**: 2026-05-11 11:35（55,826 byte / 818 行）
**確認方法**: 統合チームによる更新を 4 分間ポーリングし、3 回連続で md5 一致 → 「安定」と判定して最終 Read。レビューは安定版に対して実施。

---

## 結論

**判定**: **GO with minor**
**Critical**: 0 件 / **Major**: 2 件 / **Minor**: 5 件

Critical（公開を止める）レベルの欠陥は無し。タグバランス完全一致・全リンク疎通 200・体制/期間/参加者数等の必須事実は本文へ反映済み。ただし「DH 蓄積期間（9 年 / 15 年分）」の数値表現不整合と、「プロジェクトマネジャー / マネージャー」の表記揺れは内部資料といえども職員配布前に揃えたい性質のため Major 扱い。これら 2 点を直せばそのまま会合配布可。

---

## A. 構造・タグバランス

### A-1. タグバランス（grep ベース実機計測）

| タグ | 開 | 閉 | 判定 |
|---|---|---|---|
| div | 110 | 110 | OK |
| section | 10 | 10 | OK |
| p | 29 | 29 | OK |
| svg | 2 | 2 | OK |
| figure | 2 | 2 | OK |
| aside | 1 | 1 | OK |
| main | 1 | 1 | OK |
| header | 1 | 1 | OK |
| footer | 1 | 1 | OK |
| ul | 1 | 1 | OK |
| li | 9 | 9 | OK |
| table / thead / tbody / tr / td / th | 1 / 1 / 1 / 5 / 8 / 2 | 同 | OK |
| h1 / h2 / h3 | 1 / 9 / 5 | 同 | OK |
| a / button | 16 / 3 | 同 | OK |
| g / text | 15 / 35 | 同 | OK |
| script / style | 1 / 1 | 同 | OK |

長大 HTML 検証ルール（feedback_html_validation）の懸念だった「章末余分 `</div>`」は無し。

### A-2. 不正ネスト

- `<p><div>` 等のブロック要素 in p インライン違反: なし
- `<a>` でカード全体を囲む構造 (line 431 等 `outcome-card`): 内部に div しか無く HTML5 OK
- `<button onclick=...>` 内に通常テキストのみ: OK

### A-3. ARIA / role

- `role="dialog" aria-modal="true" aria-label="目次"` (line 294) — モバイルの toc-sidebar に dialog role を当てているが、デスクトップでも常時 dialog 扱いになる点が軽微な気がかり（**Minor-1**）。`aria-modal` は overlay 表示時のみ true が理想。実害は支援技術ユーザーが「常に開いているダイアログ」と認識する程度で、内部資料としては許容範囲。
- 各 SVG: `role="img"` + `aria-label` 両方付与 — OK
- `reading-progress` / `toc-overlay`: `aria-hidden="true"` 付与 — OK
- `back-to-top` / `toc-toggle` / `theme-toggle`: `aria-label` 付与 — OK

### A-4. CSS 未定義クラス（実害ほぼなし）

- `.step-content` (line 548/555/562/569 で使用) は **CSS 定義なし**。grid 配置上は単なる中継ラッパーとして機能し、表示は崩れない。**Minor-2**（無害だが将来のメンテで誤解を招く）。

---

## B. 内容の事実関係

### B-1. 必須事実の反映状況

| 項目 | 期待値 | 反映 | 場所 |
|---|---|---|---|
| メンバーシップ期間 | 2011-2017 | ○ | line 378（SVG）／line 328 で「2011年に始まり 6 年余り」 |
| ROOM 期間 | 2020-2025 | ○ | line 328, 386 |
| Futures 期間 | 2026-2027（1 年） | ○ | line 395, 494, 498, 562 |
| ディレクター 西村 | 西村勇也 | ○ | line 582, 594 |
| PM 浜田 | 浜田 | ○ | line 582, 598 |
| 運営コア 古立・高本 | 古立、高本 | ○ | line 602 |
| 運営補佐 末岡・行徳 | 末岡、行徳 | ○ | line 606 |
| 想定参加者 個人100/法人10 | 個人会員100名・法人会員10社 | ○ | line 500, 582 |
| futures.emerging-future.org | 言及 + リンク | ○ | line 504 |
| 教科書 URL | textbook.html | ○ | line 449/453（旧 reports/futures-textbook.html から修正済み） |

### B-2. 数値・期間の内的整合性（**Major-1**）

DH 蓄積期間の表現に矛盾あり:

| 行 | 記述 | 含意 |
|---|---|---|
| 318 | DH「**15 年分**の蓄積」 | 2011-2026 ≒ 15 年（場の運営期間） |
| 412 | DH「**この数年**で積み上げてきた」 | 数年 |
| 414 | （無記載） | — |
| 416 | （無記載） | — |
| 498 | DB は「**2017 年以降**構築」 | 9 年（厳密な DB 構築期間） |

「Futures が立つ基盤は DH（人文学のデジタル研究）」を語るとき、本文中で「15 年分」「数年」「2017 年以降（=9 年）」が併走しており、職員から「結局何年の蓄積？」と問われる可能性が高い。

**推奨修正**: 「15 年分」（line 318）→「**9 年分**」、「この数年で積み上げてきた」（line 412）→「**この 9 年で積み上げてきた**」に揃える。すべて 2017 年起点に統一すると、line 498「2017 年以降構築」と一致する。

参考: 旧版 (line 318 旧 / 386 旧) では「過去 9 年」と書かれていたものが、今回の改稿で「15 年分」に置き換わった経緯あり。15 年は「ミラツクの場の運営年数」「3 つのコミュニティ系譜の総スパン」の指標で、DH 構築期間と混在している。

### B-3. 表記揺れ（**Major-2**）

| 行 | 表記 |
|---|---|
| 582 | プロジェクトマネ**ジャ**ー |
| 597 | プロジェクトマネ**ージャ**ー |

同一資料・同一役職で長音の有無が異なる。**推奨修正**: 「プロジェクトマネジャー」（短音）に統一（line 597 を修正）。本日の会合での職員指摘リスクを下げる目的。

### B-4. 漢数字混入

- `[百千万億]` 検索結果: 「**4 万字**」(line 440) と SVG 内 「**13 章 4 万字**」 (1 件) のみ。**慣用数量表現として OK**（数字を漢字で書く慣用が定着している字数表記）。
- 「数十／数百／百／千」の本文での出現: なし（line 414 の「何千何万」のみ修辞表現）。

### B-5. 旧モチーフ残存

- 「机／付箋／中央章／ホワイトボード／椅子」: 全件 **0 件**。クリーンアップ済み。

---

## C. 文体・トーン

### C-1. 敬体（ですます調）統一

- 「だ。／である。／であった。」: **0 件**。完全に「ですます調」統一。

### C-2. 接続詞の沈静化

- 「けれど」: **0 件**。連発の問題なし。「とはいえ」(line 330) が 1 箇所、「だからこそ」(line 316) が 1 箇所と適度。

### C-3. 専門用語の言い換え

| 略語 | 初出時の補足 | 評価 |
|---|---|---|
| DH | line 299 (TOC)「DHによる蓄積」→ line 318 で「デジタルヒューマニティーズ（人文学・社会科学の知見をデジタル技術で構造化・横断可能にする研究領域）」と説明 | TOC が先に DH 単独で出るが、章タイトル line 410 では「デジタルヒューマニティーズによる蓄積」と日本語表記。**OK**（Minor-3: TOC のみ DH 略称、開いた本文では日本語フル表記。一貫性は欠くが許容） |
| CLA | line 412「126年分のCLA（**因果階層分析**）」 | OK |
| GTA | （旧版 line 414 では「GTA 解析の基盤」と無補足だったが）**現版で削除済み**。GTA という語は最終版に存在しない | OK |
| RESONANCE | line 629「未来洞察RESONANCE（**生活者発想の質的手法**）」 | OK |

### C-4. 「読者と並んで」の対等性 / 上から目線の有無

- line 316「完成した構造をお伝えするためではなく、なぜこの形を選びつつあるのか、その背景にあるものを先にお渡ししておくことが、これから一緒に育てていくための土台になると考えています。」 — 対等性 OK
- line 326「Futuresは、その自然な進化の一段階として捉えています。新しい場を立ち上げるというよりは…別の入口からもう一度開き直す試みに近いと感じています。」 — hedging 効いている
- line 726「会員に向けて完成品を披露する立場ではなく、同じく分岐の前に立つ一人として、職員のみなさんに関わっていただける場をつくりたい」 — 並走姿勢 明確
- line 728「読みながら気になった部分、引っかかった部分があれば、その違和感こそが次の設計のヒントになります。」 — 違和感を歓迎する姿勢、対等性 高

「上から目線」「指示口調」「啓蒙トーン」の残存なし。**全体トーン: 良**。

### C-5. 文体軽微（**Minor-4**）

- line 414 末尾「**横断的に組み合わせることで初めて見えてくる風景を生む**。いわば、〜」 — 文末「生む」だけ「ですます」を外している（地の文の韻律を作るための意図的な選択と思われる）。意図的なら可。気になる読者にはエッジに感じられる可能性あり。

---

## D. デザイン・視認性

### D-1. ミラツク CI（焦茶 + Journal red）

- `:root` (line 14-37): `--bg: #1C1410`（焦茶ダーク）, `--accent-warm: #FF3644`（Journal red）— OK
- `[data-theme="light"]` (line 38-57): `--bg: #FAF6F0`（オフホワイト系焦茶）, `--accent-warm: #ED2E3B` — OK
- 上部 `border-top: 3px solid var(--accent-warm)` — OK
- 段落 `text-indent: 1em` (line 123) — OK
- `font-feature-settings: "palt"` (line 62) — OK

ミラツク CI 準拠（reference_akashiro_ci / ci-check 観点）でとくに気になる逸脱なし。

### D-2. ダーク / ライト両対応

- `localStorage` 永続化キー: `futures-internal-theme` (line 694/698) — 他資料と衝突しない命名 OK
- ライトモード時の SVG テキスト視認性: dark 用の置換ルール (line 205-209) はあるが、light 切り替え時には SVG ハードコード色 `#FFFFFF`（中央 Futures ノードのテキスト, line 615/616/668-671）が `#FF3644` 背景の上で表示されるため OK。グレー系 `#D8D5D1` テキストはライト背景 `#FAF6F0` に対して **コントラスト不足** の懸念あり（**Minor-5**）。たとえば line 644「内部成果物（DH 蓄積）」、各ノードラベル等。WCAG AA 比 4.5:1 は届かない見込み。
  - 実害: ライトモード時に SVG ラベルが薄く見える。内部資料として致命的でないが、ライトモード使用者にはやや読みづらい可能性。

### D-3. 図解 2 点の配置と視認性

- 図 1（コミュニティ系譜タイムライン, line 337-403）: viewBox 900×280、横軸 2011-2027 にバー 3 本配置。**Futures バー** (line 391-392) のみ実線 + 点線延長で表現分けあり。良
- 図 2（Futures ハブマップ, line 642-715）: viewBox 900×480、中央 Futures + 上 4 内部成果物 + 下 3 外部協働。実線（内部）/ 点線（外部）の区別あり。良

### D-4. モバイル 375px レイアウト

CSS 確認:
- `@media (max-width: 1000px)` (line 212): サイドバー → 固定 left:-100% で隠す、`.toc-toggle` 表示、`.outcome-grid` を 1 列に
- `@media (max-width: 600px)` (line 243): cover-title 縮小、back-to-top 位置調整
- SVG `width: 100%; height: auto;` (line 132, 337 inline, 642 inline): 親要素の幅にフィット
- `.diagram-wrap { margin: 32px -8px; padding: 16px 8px; }` (line 134): モバイルで余白圧縮

**375px シミュレーションでの懸念**: 図 1/図 2 とも viewBox 幅 900 を 375-16=359px に圧縮するため、SVG 内テキスト `font-size="9-11"` は実画素換算で約 3.6-4.4px となり **判読困難**。ただし内部資料 + figcaption に同内容の説明あり、補完されるので致命度は中。**Minor-6**（モバイル個別最適化は今回はパス可）。

### D-5. フォントロード

line 12: `Noto+Sans+JP:wght@300..900` + `Noto+Serif+JP:wght@300..900` + `Judson:wght@400;700` — すべて含む。`display=swap` で FOUT 回避。OK

### D-6. 印刷対応

line 250-256: `@media print` で top-bar / sidebar / progress / back-to-top / toc-toggle / toc-overlay を非表示、章を page-break-inside: avoid。基本要件満たす。

---

## E. リンク疎通（実測 / 2026-05-11）

| URL | HTTP code |
|---|---|
| https://journal.emerging-future.org/deep-knowledge/ | **200** |
| https://journal.emerging-future.org/future-questions/ | **200** |
| https://journal.emerging-future.org/8-questions/ | **200** |
| https://journal.emerging-future.org/methodology/ | **200** |
| https://journal.emerging-future.org/deep-knowledge/methodology/ | **200** |
| https://yuyanishimura0312.github.io/miratuku-news-v2/textbook.html | **200** |
| https://yuyanishimura0312.github.io/kurashi-no-katachi/ | **200** |
| https://yuyanishimura0312.github.io/henka-no-katachi/ | **200** |
| https://futures.emerging-future.org | **200** |

curl `-sL --max-time 15` でフォロー後のステータス。**全 9 件 200 OK**。リンク疎通の不安は無し。

（補足）本資料内で実際に href として記載されているのは:
- top-bar brand: https://journal.emerging-future.org/ (200)
- outcome card 4 枚: deep-knowledge / future-questions / 8-questions / miratuku-news-v2/textbook.html (全 200)
- series-list 1 件: yuyanishimura0312.github.io/kurashi-no-katachi/ (200)
- futures platform: https://futures.emerging-future.org (200)

`/henka-no-katachi/` `/methodology/` `/deep-knowledge/methodology/` はリクエスト URL リスト上で疎通を要確認とされた URL であり、本資料に直接 href としての記載は無いが、いずれにせよ稼働確認済み。

---

## 推奨修正

### Major（職員配布前に直したい・2 件）

1. **DH 蓄積期間の表現を 9 年に統一**
   - line 318: 「**15 年分**の蓄積」 → 「**9 年分**の蓄積」
   - line 412: 「この**数年で**積み上げてきた」 → 「この**9 年で**積み上げてきた」
   - 理由: line 498 が「2017 年以降構築」と明示しており、9 年が事実値。15 年は「3 コミュニティの系譜（2011-2026）」を意図した記述だが、DH の説明文では誤誘導になる。

2. **「プロジェクトマネジャー / マネージャー」表記統一**
   - line 597: 「プロジェクト**マネージャー**」 → 「プロジェクト**マネジャー**」（line 582 と一致させる、ミラツク社内表記の慣例に沿うなら短音側を推奨）

### Minor（時間があれば直したい・5 件）

3. **TOC の「DH」を「デジタルヒューマニティーズ」に**（line 299）
   - 章タイトル line 410 と一致させる。略称初出のまま TOC に出るのを避ける。

4. **`.step-content` ラッパーに CSS 定義追加 or 削除**
   - 機能はしているが無定義ラッパー。`.step-content { display: contents; }` を追記するか、HTML からラッパーを外す。

5. **line 414 文末「風景を生む。」→「風景を生みます。」**
   - 「ですます」統一の徹底。意図的な韻律操作なら現状維持可。

6. **ライトモード SVG ラベルのコントラスト改善**
   - 図 1/2 の `fill="#D8D5D1"` を data-theme="light" 時に `#5A4838` 等に置換する CSS ルール追加。
   - 例:
     ```css
     [data-theme="light"] .diagram svg text[fill="#D8D5D1"],
     [data-theme="light"] .diagram svg text[fill="#9A9690"] { fill: #5A4838; }
     ```

7. **モバイル 375px での SVG テキスト判読性**
   - 図 1/2 を viewBox スケール最適化または mobile media query で `font-size` 拡大。または figcaption への代替テキスト充実で代替可。

### 修正不要（確認済みクリーン）

- リンク疎通: 全 200
- タグバランス: 完全一致
- 旧モチーフ（机/付箋/中央章）: 完全削除
- 漢数字混入: 慣用「4 万字」のみで問題なし
- 敬体統一: ほぼ完全（Minor-5 の 1 文除く）
- 旧 URL `reports/futures-textbook.html`: `textbook.html` に修正済み
- 体制 4 行: 期待値どおり全件反映
- 参加者数 個人 100 / 法人 10: 反映済み
- futures.emerging-future.org: 言及 + リンク 反映済み
