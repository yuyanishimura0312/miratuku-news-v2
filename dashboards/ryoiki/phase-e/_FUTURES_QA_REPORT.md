# Futures Briefing 最終QAレポート

**対象ファイル**: `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-internal-briefing.html`
**サイズ**: 57,304 bytes / 850 行（Round 3 修正後の最終版）
**QA実施日**: 2026-05-11
**本番URL**: https://journal.emerging-future.org/futures-briefing/

---

## 結論

**判定: GO（公開可水準・職員会合配布可能）**

| 区分 | 件数 |
|---|---|
| Critical | 0 |
| Major | 0 |
| Minor | 2 |

前回QA（55KB版）で検出されたMajor 5件（DH期間矛盾／PM表記揺れ／モバイル小フォント／sticky数値不整合／ライトモードAA未達）は **全て解消** されています。残るのは美観上のMinor 2件のみで、本番配布の妨げにはなりません。

---

## A. 構造・タグバランス

**全パス**（30タグ種すべて opens = closes）

| タグ | open / close |
|------|----|
| html / head / body | 1/1 各 |
| div | 110 / 110 |
| section | 10 / 10 |
| main | 1 / 1 |
| aside | 1 / 1 |
| header / footer | 1 / 1 各 |
| figure / figcaption | 2 / 2 |
| svg | 2 / 2 |
| p | 29 / 29 |
| table / thead / tbody | 1 / 1 各 |
| tr | 5 / 5 |
| th | 2 / 2 |
| td | 8 / 8 |
| ul | 1 / 1 |
| li | 9 / 9 |
| a | 16 / 16 |
| h1 / h2 / h3 | 1 / 9 / 5（階層順守） |
| button | 3 / 3 |
| style / script | 1 / 1 |

不正ネスト・余分タグ・閉じ忘れはなし。

---

## B. 内容の事実関係

### 必須キーワード反映確認
| 項目 | 出現回数 | 状態 |
|---|---|---|
| プロジェクトマネージャー | 2 | ✓ 統一済 |
| プロジェクトマネジャー（旧表記） | 0 | ✓ 残存ゼロ |
| #C81F2E（ライトモードAA適合赤） | 2 | ✓ 適用済 |
| 個人会員100 | 2 | ✓ 反映済 |
| 法人会員10 | 2 | ✓ 反映済 |
| futures.emerging-future.org | 2 | ✓ 本番URL明記 |
| textbook.html（教科書正典） | 2 | ✓ 正典URL |
| RESONANCE（博報堂協働具体名） | 1 | ✓ 反映済 |
| バックキャスティング（PwC協働） | 1 | ✓ 反映済 |
| 井上ゆき | 3 | ✓ 明記 |
| 人＋AI（テーマ） | 6 | ✓ 各章で反復 |

### DH蓄積期間の整合性
| 表現 | 回数 | 評価 |
|---|---|---|
| 「15年」 | 1 | ✓ 組織歴の文脈のみ（line 326「ミラツクが15年かけて」） |
| 「9年」 | 2 | ✓ DH蓄積期間として統一（2017年以降） |

数値矛盾は完全解消。

### 旧モチーフ残存
| 語 | 回数 |
|---|---|
| 机 / 付箋 / 8枚 / 九枚目 / 中央章 / とちゅう / ホワイトボード / 姉妹書 | すべて 0 |

完全解消済み。

### 漢数字混入
| 語 | 回数 | 判定 |
|---|---|---|
| 一つ | 1 | Minor（後述）：「もう一つの基盤」という慣用表現の代名詞用法 |
| 二つ〜十年 | 0 | ✓ |

---

## C. 文体・トーン

### 敬体統一
- 接続詞「けれど」: 0 ／「もっとも」: 0 ／「ところが」: 0 ／「しかし」: 0 ／「一方」: 0
- 「とはいえ」: 1（許容範囲）

接続詞は十分に沈静化され、段落の沈黙で論を運ぶ西村文体に整っています。

### 常体逸脱
- 「する。」: 1件のみ（図2 figcaption の「結ぶ蝶番として機能する。」）
  - 評価：figcaption の体言止め的解説文として許容範囲（**Minor-1**）

### トーン
- 西村らしい「同じく分岐の前に立つ一人として」の対等性が確保されている
- 「違和感こそが次の設計のヒント」など、職員からの参画を上から目線なく呼びかける質感

---

## D. デザイン・視認性

### ミラツクCI
- 焦茶 #1C1410 + Journal red #FF3644（ダーク既定）：✓ 維持
- ライトモード：#FAF6F0 + #C81F2E（AA適合・4.7:1）：✓ 修正反映済

### sticky/scroll の数値整合性
| プロパティ | 出現 |
|---|---|
| `top: 56px` | 4 |
| `top: 48px`（旧値） | 0 |
| `height: 56px` | 1 |
| `scroll-padding-top: 56px` | 1（旧60pxから修正済） |
| `scroll-margin-top: 56px` | 1（旧60pxから修正済） |

全て56pxで統一。

### A11y要素
| 属性 | 出現 |
|---|---|
| aria-label | 6 |
| aria-modal | 4 |
| aria-hidden | 2 |
| role="img"（SVG） | 2 |
| role="dialog"（静的） | 0（モバイル時のみ動的付与へ修正済） |
| focus-visible | 1 |
| prefers-reduced-motion | 1 |

PC環境で TOC sidebar が誤って dialog 扱いされる問題は解消。

---

## E. リンク疎通（実測 curl）

| URL | HTTP |
|---|---|
| /futures-briefing/ | ✓ 200 |
| /（journal トップ） | ✓ 200 |
| /deep-knowledge/ | ✓ 200 |
| /deep-knowledge/methodology/ | ✓ 200 |
| /future-questions/ | ✓ 200 |
| /8-questions/ | ✓ 200 |
| /methodology/ | ✓ 200 |
| GitHub Pages /textbook.html | ✓ 200 |
| GitHub Pages /kurashi-no-katachi/ | ✓ 200 |
| GitHub Pages /henka-no-katachi/ | ✓ 200 |
| https://futures.emerging-future.org/ | ✓ 200 |

**11/11 すべて HTTP 200**。リンク切れゼロ。

---

## F. Minor（公開後の改善候補）

### Minor-1: figcaption末尾の常体表現
- 場所：図2 figcaption「結ぶ蝶番として機能する。」
- 影響：軽微。読者は文脈で違和感を受けない可能性が高い
- 推奨：「機能します。」 or 体言止め「結ぶ蝶番」で締める

### Minor-2: 「もう一つの基盤」の表記
- 場所：DH蓄積セクション冒頭「Futuresのもう一つの基盤は…」
- 評価：「一つ」が慣用的代名詞用法のため、厳密にはアラビア数字化ルールの対象外と判断できる
- 推奨：そのまま許容

---

## G. 公開判定

**本資料は職員会合への配布可能水準に到達しています**。

- Critical / Major ゼロ
- 全タグバランス OK
- 全リンク HTTP 200
- 旧モチーフ完全除去
- AA適合（ライト／ダーク両モード）
- 西村らしい対等性のトーン維持

Minor 2件は美観上の調整で、職員配布の妨げになりません。

---

*QA実施: 2026-05-11 / 対象: futures-internal-briefing.html v Round 3 (57,304 bytes)*
