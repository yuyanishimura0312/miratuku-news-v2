# q-detail 8ファイル整合修正 完了レポート

実施日: 2026-05-10
対象: `eight-questions-q[1-8]-detail.html` 全8ファイル
修正方針出典: `_REVIEW_CONSISTENCY.md` / `_REVIEW_DESIGN_HARMONY.md`

---

## 結論

判定: **完了 (GO)**

旧書籍体系（8つの問い）から新書籍体系（7+1）への内部表記整合、SVG白背景ハレーション解消、back-link張り替え、cover-tag のLPカード番号併記まで、Critical 4項目とMajor 3項目を一括修正済み。

タグバランス検査: 8ファイルとも `<div>` 27/27, `<section>` 3/3 で完全に揃っている。

---

## 修正サマリ

### Critical-1: back-link 張り替え（C-1 / M-7）

全8ファイルの top-bar back-link、bottom-back の bb-link、bb-link.is-secondary の3箇所を、旧 `eight-questions-report.html` から新書籍 `https://journal.emerging-future.org/future-questions/` へ張り替え。リンク文言も「← レポート版『未来への問い』へ」「レポート版『未来への問い』へ」「本編トップへ」に統一。

合計置換数: 24箇所（8ファイル × 3本）。grep 検証で `eight-questions-report.html` の参照は0件。

### Critical-2: SVG白背景ハレーション（C-2）

q1-detail と q6-detail の SVG 内 `<rect width="880" height="460" fill="#FFFFFF"/>` を削除。q2/q3/q4/q5/q7/q8 は当該rect不在を確認済み（SVG内に別の背景パターンが入っていたため）。

加えて全8ファイルの `<style>` 末尾に以下の CSS を追加：

```css
[data-theme="dark"] .diagram svg text[fill="#121212"],
[data-theme="dark"] .diagram svg text[fill="#555555"],
[data-theme="dark"] .diagram svg text[fill="#6B6B6B"] { fill: #E0E0E0 !important; }
```

ダークモード時に SVG 内の暗色テキストが暗色背景に埋もれる二次問題を解消。

### Critical-3: 旧モチーフ「付箋」全廃（M-5）

全8ファイルの cover-subtitle にあった「第N の付箋」を「第N の問い」「+1 の問い」へ置換。grep 検証で「の付箋」の残存は0件。

q5-detail の subtitle 「8つの星座の中央に据えられた鏡」は、書籍と整合する「7つの問いの結びの位置に据えられた鏡」へ書き換え。M-6 にも応答。

### Critical-4: 問い番号のシフト整合（C-4 / C-6）

新7+1 体系へ番号系を統一：

| ファイル | 旧表記 (タイトル) | 新表記 (タイトル) | 旧 cover-tag | 新 cover-tag |
|---|---|---|---|---|
| q1-detail | 第1の問い | 第1の問い | QUESTION 1 OF 8 | QUESTION 1 of 7+1（LPカード 01番） |
| q2-detail | 第2の問い | 第2の問い | QUESTION 2 OF 8 | QUESTION 2 of 7+1（LPカード 02番） |
| q3-detail | 第3の問い | 第3の問い | QUESTION 3 OF 8 | QUESTION 3 of 7+1（LPカード 06番） |
| q4-detail | 第4の問い | 第4の問い | QUESTION 4 OF 8 | QUESTION 4 of 7+1（LPカード 07番） |
| q5-detail | 第5の問い (番外編) | +1の問い (番外編) | 番外編 · 第5の問い · 7+1の鏡 | 番外編 · +1 の問い · 7+1 の鏡（LPカード 05番） |
| q6-detail | 第6の問い | 第5の問い | QUESTION 6 OF 8 | QUESTION 5 of 7+1（LPカード 04番） |
| q7-detail | 第7の問い | 第6の問い | QUESTION 7 OF 8 | QUESTION 6 of 7+1（LPカード 08番）· 道具と人格のあいだ |
| q8-detail | 第8の問い | 第7の問い | QUESTION 8 OF 8 | QUESTION 7 of 7+1（LPカード 03番）· 約束を支える器 |

### Major-3: LPカード番号の併記（M-3）

cover-tag 内に LPカード番号を併記し、読者が LP カードから到着した際の現在地把握を容易化。特に q6/q7/q8 はファイル名と新Q番号がねじれているため、この併記が読者の混乱防止に直結する。

### 付帯修正

- `<title>` の「| 8つの問い」→「| 7+1の問い」（全8）
- `meta description` 内「第N の付箋」→「第N の問い」（全8）
- top-bar brand small 「2100年に向けた8つの問い」→「2100年に向けた7+1の問い」（全8）
- qn-section の見出し「8つの問いを巡る」→「7+1の問いを巡る」（全8）
- qn-grid の card 番号: Q6→Q5、Q7→Q6、Q8→Q7、番外編→+1（タイトルも 「誰が決めるか」「道具と人格」「約束を支える器」「問いを問う問い」へ統一、全8）
- bottom-back-text 「他の7つの問いとの絡まり方は、本編で読めます」→「他の7つの問い+1との絡まり方は、書籍版『未来への問い』で読めます」（全8）
- footer 「8つの問いの未来分岐点シリーズ」→「7+1の問いの未来分岐点シリーズ」（全8）

---

## 検証結果

### grep 残存ゼロ確認

```
[refs eight-questions-report.html:] 全8ファイルとも 0
[refs 付箋:] 全8ファイルとも 0
[refs 8つの問い:] 全8ファイルとも 0
[refs QUESTION N OF 8:] 全8ファイルとも 0
[refs SVG 880x460 white rect:] 全8ファイルとも 0
```

### HTMLタグバランス確認

```
q1-q8 detail: <div>=27 </div>=27, <section>=3 </section>=3
```

全ファイルで完全一致。閉じタグ過剰・不足なし。

### 新表記の出現確認

全8ファイルで以下を実装：
- `https://journal.emerging-future.org/future-questions/` のリンク × 3本
- 「QUESTION N of 7+1」または「番外編 · +1 の問い」の cover-tag × 1本
- LPカード番号の併記（全8）

---

## 未対応・次版へ持ち越し項目

以下は今回の修正範囲外（指示にない、もしくは別ファイルの責務）：

- M-1 （書籍 cover-meta 文字数表記の修正）
- M-3 / 推奨修正 3 （LP の「8つ」「8段の段差」表現整合）
- M-9 （LP の `dashboards/reports/deep-knowledge-book.html` リンク切れ）
- 推奨修正 8 （書籍 → q-detail への入口設置）
- 推奨修正 11 （top-bar brand 遷移先の三者統一）

これらは LP / 書籍側の修正で対応する別タスク。

---

検査担当: Claude Opus 4.7 (1M context)
