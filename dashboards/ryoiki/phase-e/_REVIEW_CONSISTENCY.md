# 整合性レビュー報告

検査対象（2026.05.10 22:50 時点の実ファイル）:

- 書籍 `/dashboards/ryoiki/phase-e/future-questions-book.html` (305 KB / 3,425 行 / 約 38,000 日本語字)
- LP `/dashboards/ryoiki/phase-e/eight-questions-lp-miratuku.html` (76 KB / 1,838 行)
- 詳細 `/dashboards/ryoiki/phase-e/eight-questions-q[1-8]-detail.html` (8 ファイル / 計 4,000 行)

公開先（実測ベースの推定）:
- 書籍 → `https://journal.emerging-future.org/future-questions/`（FTP `STOR` で `index.html` として配信）
- LP → `https://journal.emerging-future.org/8-questions/`（書籍内 cover-link が指すパス）
- q-detail → 書籍と同じディレクトリにそのまま配置される想定（`index.html` 参照あり）

## 結論

**判定**: **NO-GO**

**齟齬**: Critical **6 件** / Major **9 件** / Minor **8 件**

LP のカード番号（01〜08）と、各カードがリンクする `q[N]-detail.html` の番号が一致せず、さらに「書籍の第5〜第8」と「q-detail の第5〜第8」の指示内容が完全に交差している。読者がページを行き来した瞬間に、同じ「第5の問い」が三者三様の意味を持つ状況が出来上がっている。**LP のカード本文と q-detail の中身が、テーマレベルでも一致していない箇所が 4 つある**ため、いまのままだと「もっと詳しく」のリンクが偽装リンクとして機能してしまう。最低でも以下 2 系統の修正なしには公開できない。

1. LP カード ↔ q-detail の中身ズレ（4 箇所）の解消
2. 「第N の問い」表記の統一（書籍 7+1 vs q-detail Q1〜Q8 番外編が衝突）

---

## マッピング表（実測）

| 書籍 ch | 書籍内ラベル | 書籍タイトル（topic） | LP card # | LP card タイトル（topic） | LP card → q-detail リンク先 | q-detail 内タイトル（topic） | 一致／差分 |
|---|---|---|---|---|---|---|---|
| ch3 | CHAPTER 03 — 第1の問い | まだ顔のない人々の席（未来世代） | 01 | 未来の世代の声を、今の我々はどう聞くか | q1-detail.html | 第1の問い・未来世代の声 | **三者一致** |
| ch4 | CHAPTER 04 — 第2の問い | 採取しない、という作法（先住民） | 02 | 先住民の知恵を、自分の物差しで測らずに学べるか | q2-detail.html | 第2の問い・先住民の知に触れる作法 | **三者一致** |
| ch5 | CHAPTER 05 — 第3の問い | 見えない世話のかたち（ケア） | 06 | ケアを学ぶ教育は、どこに向かうべきか | q3-detail.html | 第3の問い・見えない世話を物差しに | LP-card 番号と q-detail 番号がねじれ／LP は「ケア教育」、書籍と q-detail は「ケアを物差しにする」 |
| ch6 | CHAPTER 06 — 第4の問い | 複数の世界が並び立つ（教育） | 07 | 西洋以外の知を、対等な学問として認められるか | q4-detail.html | 第4の問い・複数の世界が並び立つ教育 | LP-card 番号と q-detail 番号がねじれ／LP は「西洋以外の知」、書籍と q-detail は「複数世界の教育」 |
| ch7 | CHAPTER 07 — 第5の問い | 誰の声に、結果を変える力を（決定権） | 04 | 複数の世界の見方が、並び立つ社会は可能か | q6-detail.html | 第6の問い・誰の声に決定権を渡すか | **重大ズレ**: LP card 04 のテーマと q-detail の中身が違う／書籍では「第5＝決定権」、q-detail では「第6＝決定権」 |
| ch8 | CHAPTER 08 — 第6の問い | 道具と人格のあいだ（AI） | 08 | 「ひとつの自分」でなくてもいい時代に向けて | q7-detail.html | 第7の問い・人ではない知性に責任の席を | **重大ズレ**: LP card 08 のテーマ（plural selfhood）と q-detail の中身（AI）が違う／書籍では「第6＝AI」、q-detail では「第7＝AI」 |
| ch9 | CHAPTER 09 — 第7の問い | 約束を支える器（新しい器） | 03 | 「どこにいるか」がもう一度大事になる時代 | q8-detail.html | 第8の問い・新しい器のかたち | **重大ズレ**: LP card 03 のテーマ（場所性／地域）と q-detail の中身（組織形態）が違う／書籍では「第7＝器」、q-detail では「第8＝器」 |
| ch11 | CHAPTER 11 — +1の問い | 問いを、問う | 05 | 我々は、自分自身が問うていることを問えているか | q5-detail.html | 第5の問い・問うわたしたち自身を問えるか | LP のテーマは合致、ただし**書籍では「+1」、q-detail では「第5」**で番号が衝突／書籍 ch10「7つの問いが編む未来」は LP 上に対応カード無し |

ねじれの構造を要約すると:

- **書籍の番号体系**は **第1〜第7 + +1** (= 7+1)。決定権が**第5**。AI が**第6**。器が**第7**。問いを問う = **+1**。
- **LP カードの番号体系**は **01〜08**。配置順は (1)未来世代→(2)先住民→(3)場所性→(4)複数世界→(5)問いを問う→(6)ケア教育→(7)西洋以外の知→(8)複数自己。
- **q-detail の番号体系**は **第1〜第8（第5は番外編）**。決定権が**第6**。AI が**第7**。器が**第8**。問いを問う = **第5（番外編）**。

3 者で「第5」がそれぞれ「決定権 / 問いを問う / 問いを問う（番外編）」を指す。

---

## Critical 齟齬（公開ブロッカー）

### C-1. LP カード 03（「どこにいるか」が大事な時代）→ q8-detail（新しい器のかたち）リンクが**テーマ違い**
- 場所: `eight-questions-lp-miratuku.html:1496-1507` のカード本文（地域・場所性・トランジション・タウン）と、リンク先 `eight-questions-q8-detail.html`（DAO・B Corp・新しい組織形態）の主題が一致しない。
- 影響: 読者が「もっと詳しく」を押すと、別テーマの記事に飛ばされる。LP の説得力を一瞬で失う。

### C-2. LP カード 04（複数の世界の見方）→ q6-detail（誰の声に決定権を渡すか）リンクが**テーマ違い**
- 場所: `eight-questions-lp-miratuku.html:1510-1521` のカード本文（worldview pluralism）と、リンク先 `eight-questions-q6-detail.html`（市民議会・気候市民会議・決定権）の主題が一致しない。

### C-3. LP カード 07（西洋以外の知）→ q4-detail（複数の世界が並び立つ教育）リンクが**部分テーマ違い**
- 場所: `eight-questions-lp-miratuku.html:1552-1563`。q4-detail はサスカチュワン大学・UNESCO Open Science など「複数知の教育」が主題で、LP 07 の「西洋以外を学問として認める」とは重なるが、LP 07 のメッセージである「日本・東アジア・アンデス・アフリカの方法論承認」は q4-detail にはほぼ無い。

### C-4. LP カード 08（「ひとつの自分」でなくてもいい）→ q7-detail（AI 電子人格）リンクが**主題違い**
- 場所: `eight-questions-lp-miratuku.html:1566-1577`。LP は「複数自己／脳神経多様性／AI と対話する自分」を語り、q7-detail は EU AI Act・電子人格議論。**LP card 08 と書籍に対応する章は存在しない**。
- 補足: 書籍にも「複数自己」を独立した問いとして立てた章は無い。LP 08 はそもそも 7+1 体系から落ちたコンセプトの可能性が高い。

### C-5. q-detail back-link が「`eight-questions-report.html`」を指している（**新しい書籍を指していない**）
- 場所: 全 8 ファイルの top-bar back-link と bottom-back-link。例: `eight-questions-q1-detail.html:148` `<a href="eight-questions-report.html#ch3">本編・第1の問いに戻る</a>`。
- 問題: `eight-questions-report.html` は旧版（タイトル「2100年に何を残したいか — 8つの問いの物語」、PROLOGUE = 「机のうえの8枚の付箋」）。新書籍 `future-questions-book.html`（『未来への問い — 2100年に向けた分岐と対話』）には繋がっていない。
- 影響: 「本編に戻る」を押しても、読者は新書籍ではなく旧レポートに到達する。

### C-6. LP の「もっと詳しく」と q-detail の表紙コピーが**指示する番号同士で食い違っている**
- 例: LP card 04 の見出しは「複数の世界の見方が、並び立つ社会は可能か」。リンク先 `q6-detail.html` の表紙には「QUESTION 6 OF 8 · 第6の問い・誰の声に決定権を渡すか」と表記。読者は遷移直後に「あれ、別の問いに飛ばされた」と気づき混乱する。

---

## Major 齟齬

### M-1. 書籍の文字数表記が約 30% 過小
- 場所: `future-questions-book.html:7`（meta description）「約3万字」、`:304`（cover-meta）「約3万字 · 7+1の問い · 推定 readingtime 50分」。
- 実測: HTML タグ・CSS・JS・SVG を除いた本文で 38,229 日本語字 / 全非空白 43,271 字。
- 推奨: 「約 4 万字」もしくは「約 38,000 字」。読了時間は 600 字／分換算で 65 分前後（50 分は短すぎ）。

### M-2. LP の「8 段の段差」 vs 書籍の「7 段＋鏡」がぶつかる
- LP 1588:「これらは別々の問いではなく、同じ坂の **8 段の段差**です」 / 1590: 「**8 段の段差**として設計」。
- 書籍 362:「中核となる7つは…**7段の見取り図**」/ 562:「**7段の問いかけと**、その背面に立つもう1つの問いかけ」/ 2986:「**4つの段差**が浮かび上がってくる」。
- 同じ「段差」モチーフで枚数が違う。LP の 8 段が誤りで、書籍が正（7 段＋鏡）。

### M-3. LP に「7+1」の表記がほぼ消えている
- LP 全文中「7+1」は**1 箇所のみ**（`:1338` hero-cta「7+1の問いを見る →」）。それ以外は全て「8 つの問い」。
- 書籍内「7+1」は 34 箇所、「8 つ」も 38 箇所（多くは「7+1 ＝ 合計 8」の説明文脈）。
- 読者が LP → 書籍と進むと「あれ？ 7+1 ってどういう意味？」になる。LP に「7+1 とは何か」の短い説明がほしい。

### M-4. q-detail のタイトル系列が依然「8つの問い」シリーズ
- 例: `eight-questions-q1-detail.html:6` `<title>第1の問い・未来世代の声 — 未来の分岐点 | 8つの問い</title>`。footer も全 8 ファイル「8つの問いの未来分岐点シリーズ · 2026.05」。
- 書籍のタグライン「7+1 の問い／分岐と対話」と整合しない。

### M-5. 「付箋」モチーフが q-detail に全面残存
- 全 8 q-detail の cover-subtitle が「第N の付箋」と書く（`q1-detail.html:157` ほか）。q5-detail:131「8つの星座の中央に据えられた鏡。残り7つの問いの精度を、根の場所で決める **第5の付箋** は、ほかの全ての問いの背面に立つ。」
- 書籍では「付箋」「机」「8 枚」のモチーフを全廃して「分岐と対話／坂／編む」に置き換え済み（旧 `eight-questions-report.html` の PROLOGUE「机のうえの8枚の付箋」が古さの根拠）。
- LP には「付箋／机」は無い（除去済み）。

### M-6. q5-detail が「8つの星座の中央」と書く一方、書籍の +1 は「結びの位置」「背後の鏡」
- 場所: `eight-questions-q5-detail.html:7`（meta）「8つの星座の中央に据えられた、問いを問う問い」/ `:131` cover-subtitle「8つの星座の中央に据えられた鏡」。
- 書籍 `:362` 「最後に置かれた+1の問いは、その7つを背後から映す鏡として、本書の結びの位置に据えられます」。
- 「中央」と「最後／結び」で位置が逆。

### M-7. 書籍 cover の本書ナビ → LP（`/8-questions/#questions`）／LP の hero-cta → 書籍（`/future-questions/`）。三者を結ぶ q-detail が**書籍に直接戻れない**
- q-detail から見て:
  - top-bar brand → `https://journal.emerging-future.org/deep-knowledge/`（書籍でも LP でもない、別作品）
  - back-link「8つの問い LP」 → `index.html`（**ローカル `phase-e/` 配下に存在しない**ファイル名）
  - bottom-back / top-bar の「本編に戻る」 → `eight-questions-report.html`（旧版）
- 公開後の URL 上で LP は `/8-questions/index.html` として配信され、`q-detail` も同ディレクトリに配置される設計と推察できるが、**書籍 `future-questions-book.html` への直リンクが q-detail に1本も存在しない**。

### M-8. 「数十／数百／数千」がアラビア数字ルールに反して漢数字で残存
- 書籍 `:475` 「世紀単位の時間軸」、`:2886` 「何百キロ」。q-detail も「数十年」「七世代」「数百年」など複数。LP には「100」「数100万人」と漢数字混在（LP `:1700` 「数100万人の小さな選択」）。
- ルール（書籍冒頭の `_convert_numerals.py` 由来）はアラビア数字統一のはずだが、3 ファイル群で適用度が違う。

### M-9. LP の「書籍を読む」リンク先が**存在しない**ファイル
- LP `:1740` `<a class="action-link" href="../../reports/deep-knowledge-book.html">書籍を読む →</a>`。
- 実測: `dashboards/reports/` ディレクトリ自体が無い（`/dashboards/` 直下に reports は存在しない）。404 確定。
- もっとも、ここで参照されるべきは「『深い知が拓く 2100 年』書籍」と「『未来への問い』書籍」の 2 種類だが、LP 上では『深い知が拓く 2100 年』への参照になっている（本書の方ではない）。本書（future-questions-book.html）への入り口が LP に**1 つも無い**のは設計ミスの可能性が高い。

---

## Minor 齟齬

### m-1. 公開日の表記が三者三様
- 書籍 `:301` 「2026.05.10」、`:3355` footer 「2026.05.10」
- LP `:1334` 「2026年5月」
- q-detail footer 「2026.05」
- どれかに統一推奨（赤白 CI ルール上は `YYYY.MM.DD` が原則）。

### m-2. 書籍 top-bar brand と q-detail top-bar brand のリンク先が違う
- 書籍: `https://journal.emerging-future.org/`（journal トップ）
- q-detail: `https://journal.emerging-future.org/deep-knowledge/`（deep-knowledge 内）
- LP: `https://journal.emerging-future.org/deep-knowledge/`
- q-detail と LP は揃っているが、書籍だけ別。書籍は本記事として journal トップに帰すのが妥当か再検討。

### m-3. 「我々」と「わたしたち」が混在
- 書籍は「わたしたち」基調（例 `:368`「いま手にした技術の射程が…」）。LP は「我々」基調（例 `:1329`「我々が…」）。q-detail は混在。
- レポート版と新書籍で人称基調を切り替えたなら問題ないが、判断点として残す。

### m-4. 「途中」漢字 vs 「とちゅう」ひらがな
- ほぼ「途中」漢字で統一されている（書籍 13 件、LP 1 件）。OK。

### m-5. LP の「Foresight 2026」「BONUS · 番外編」など英語混在表記
- LP `:1326` 「MIRA TUKU ／ FORESIGHT 2026」、q5-detail `:190` 「FIGURE · BONUS · 番外編 · SELF-REFERENTIAL QUESTION」。
- 書籍にはほぼ英字 caption が無い。トーン差は意図的なら良いが、書籍と q-detail の温度差として認識しておく。

### m-6. LP 内の「8 つ」の半角数字＋スペースが多い
- LP は「8 つの問い」（半角数字＋半角スペース）で統一されているが、書籍 `:303` は「7+1の問い」（全半角スペース無し）、q-detail は「8つの問い」（スペース無し）。
- LP のスタイルだけ違う。

### m-7. LP 「7 つが」の用法
- LP `:1533` 「ほかの 7 つが「未来の社会」を問う…」 — 7+1 体系を意識した記述で書籍と整合。OK。

### m-8. q-detail bottom-back のテキストが書籍の構造を反映していない
- q1-detail `:447` 「この問いの全体像と、他の **7 つの問い** との絡まり方は、本編で読めます」 — q-detail は計 8 ファイルあるが、書籍は 7+1 で「他は 7 つ」表現は新書籍と整合。番号体系を統一すれば自動的に合う。

---

## リンク確認結果（実測）

### 書籍（future-questions-book.html）
- top-bar brand → `https://journal.emerging-future.org/` ✓ ジャーナルトップへ
- cover-link primary → `#prologue` ✓
- cover-link outline → `https://journal.emerging-future.org/8-questions/#questions` ✓ LP 宛
- footer cta-link → `https://journal.emerging-future.org/8-questions/#questions` ✓
- footer cta-link 2 → `https://journal.emerging-future.org/` ✓
- 結論: **書籍から q-detail への直リンクは 1 本も無い**（主要章の最後から「q-detail で深掘り」のフックが無い）

### LP（eight-questions-lp-miratuku.html）
- top-bar brand → `deep-knowledge/` （書籍でも LP の所属でもない）
- back-link 1 → `deep-knowledge/`
- back-link 2 → `#questions`
- back-link 3 → `https://journal.emerging-future.org/future-questions/` ✓ 書籍の公開先
- hero-cta primary → `#questions`
- hero-cta secondary → `https://journal.emerging-future.org/future-questions/` ✓ 書籍
- dq-link 01〜08 → q1〜q8 detail（**ただしテーマ整合は前述の通り破綻**）
- action-link 03（書籍を読む）→ `../../reports/deep-knowledge-book.html` ✗ **404**
- action-link 04 → `./futures-membership-proposal.html` ✓ 同階層に実在

### q-detail 共通
- top-bar brand → `deep-knowledge/`
- back-link 1 → `eight-questions-report.html#ch{N}` ✗ **旧レポート版**
- back-link 2 → `index.html` ✗ **ローカル不在**（公開後 LP が `index.html` で配信されれば動く）
- bottom-back 1 → `eight-questions-report.html#ch{N}` ✗ 同上
- bottom-back 2 → `eight-questions-report.html` ✗ 同上
- qn-grid 内のサイドリンク → 同ディレクトリの `eight-questions-q[1-8]-detail.html` ✓

---

## 推奨修正（優先度順）

### P0（公開ブロッカー、必修）

1. **LP カードと q-detail のテーマ／番号を一致させる**
   - 案 A: LP のカード並びを「書籍の 7+1 体系」に揃え、card 01〜07 = 第1〜第7、card 08 = +1（問いを問う）。同時に各カード本文を「書籍の章サマリ」に書き換える。q-detail 側は番号を 1→1, 2→2, 3→3, 4→4, 5→決定権, 6→AI, 7→器, +1（番外編）→問いを問う、として再番号付与する。
   - 案 B: q-detail の番号を新体系に合わせ、ファイル名も `q1=未来世代/q2=先住民/q3=ケア/q4=教育/q5=決定権/q6=AI/q7=器/q-plus-1=問いを問う` に変更し、LP の dq-link を再配線。
   - どちらにせよ「第N の問い・タイトル」の意味が三者で一致する状態を必ず作る。

2. **q-detail の back-link 系を新書籍 `future-questions-book.html` に張り替える**
   - 上 top-bar の `← 本編・第N の問いに戻る` と bottom-back-link の 2 か所、計 8 ファイル × 2 箇所 = 16 リンクを `future-questions-book.html#ch{該当章}` に置換。
   - 公開後の URL に合わせるなら `https://journal.emerging-future.org/future-questions/#ch{該当章}` のフルURL も検討。
   - 加えて「本編トップへ」も `future-questions-book.html` を指すように差し替え。

3. **LP 内「8 つ」「8 段の段差」を書籍と整合する表現に整える**
   - hero `:1327` 「8.／ Questions for 2100」、`:1348` 「なぜ今、この **8** つの問いなのか」、`:1379` 「我々が選んだ **8** つの問い」、`:1588` 「**8 段の段差**」、`:1763` 「8 つの問いを見る →」を、最低限「**7+1 の問い／7 段の段差＋鏡**」へ書き換える。
   - hero メイン見出しのトーンを保つために、見出しレベルでは「**7+1 の問い**」にして、本文中で「合わせて 8 つの足場として」と書き分ける案が書籍と最も整合する。

4. **書籍 cover-meta の文字数・読了時間を実測値に合わせる**
   - `:7` meta description と `:304` cover-meta の「約3万字」を「約 4 万字（約 38,000 字）」に。読了時間 50 分を「**60〜70 分**」に修正。

5. **LP `action-link` 03（書籍を読む）リンク切れの修正**
   - `dashboards/reports/deep-knowledge-book.html` は存在しない。仮に「『深い知が拓く 2100 年』」を指したいのであれば、現在公開されているパスを確認して付け直す。
   - 加えて、本書（『未来への問い』 = `future-questions-book.html`）への入り口を LP の Action リストに 1 行加えると、ユーザー導線が完結する。

### P1（強く推奨）

6. **「付箋／机」モチーフを q-detail から全廃**（`第N の付箋` → `第N の問い` に置換）。q5-detail の「8 つの星座の中央」は「+1 の鏡として最後に置く」へ書き換え。

7. **q-detail の `<title>` と footer のシリーズ名を「7+1 の問い／未来の分岐点」に揃える**
   - 例: `第1の問い・未来世代の声 — 未来の分岐点 | 7+1 の問い`。
   - footer も「8つの問いの未来分岐点シリーズ」を「7+1 の問いの未来分岐点シリーズ」へ。

8. **書籍にも q-detail への入口を 1 本ずつ用意する**
   - 各章末（書籍 `ch3〜ch9, ch11`）に「この問いの分岐点をさらに深掘り → q-detail」の小さなリンクボックスを置けば、書籍 → 詳細 → 書籍 の往復が成立する。

### P2（次版で対応可）

9. 公開日表記を `2026.05.10` に三者統一。
10. 漢数字／アラビア数字を `_convert_numerals.py` で再変換し直す（特に「数十」「数百」「数千」「7 世代」「100 万人」）。
11. top-bar brand の遷移先を「書籍 = journal トップ／LP = deep-knowledge／q-detail = deep-knowledge」と設計上意図的なら保持、そうでなければ統一。
12. 「我々／わたしたち」基調の使い分け方針をどこかに明記。

---

## 公開判定の付帯条件

- P0 の 1〜5 をすべて修正できれば **GO with minor**。
- P0 の 1（テーマ整合）と 2（back-link 修正）が未対応なら **NO-GO**。LP からの「もっと詳しく」を踏んだ瞬間に読者が混乱する致命傷だから。
- 修正後はもう一度この `_REVIEW_CONSISTENCY.md` を回して、マッピング表が「**三者一致**」のみで埋まることを確認すること。

---

検査日時: 2026.05.10
検査担当: 整合性検査エンジニア（Claude Opus 4.7 1M context）
