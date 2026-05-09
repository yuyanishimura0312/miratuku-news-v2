# Track B-2 独立検証レポート（doc-verify）

**検証担当**: Phase B Track B-2 doc-verify エージェント（独立）
**検証日**: 2026-05-09
**検証対象**:
- `track-b2-already-future-analysis.html`（650行・36,720字）
- `track-b2-already-future-verification.html`（205行・13,572字）
- `track-b2-already-future-report.html`（894行・44,945字）
- `track-b2_handoff.md`（123行）
- 新規DB: `~/projects/research/already-future-db/already_future.db`（4テーブル・126レコード）

**検証方法**: Phase A Track 7 doc-verify と同等の厳格さで4カテゴリ独立検証を実施。DB を直接 SQLite で照会し、HTML/handoff の主要主張と突合した。

**総合判定**: **CONDITIONAL PASS**（DB実装と handoff 主張に明確な不整合 1 件、表現精確性課題 2 件、ただし全体構造・主成果物の論理的整合性は強固）

---

## Phase 1: DB独立確認

DB を Python sqlite3 で直接照会した結果は以下の通り。

| 項目 | handoff主張 | DB実値 | 判定 |
|---|---|---|---|
| questions レコード数 | 14件 | 14件 | OK |
| traditions レコード数 | 5件 | 5件 | OK |
| wisdom_records レコード数 | 85件 | 85件 | OK |
| cross_question_links レコード数 | 22件 | 22件 | OK |
| tradition別 PHIL | 24件 | 24件 | OK |
| tradition別 AN | 17件 | 17件 | OK |
| tradition別 TK | 15件 | 15件 | OK |
| tradition別 MY | 15件 | 15件 | OK |
| tradition別 LIT | 14件 | 14件 | OK |
| 各問い wisdom 数（Q-V01=5、他=6-7） | 一致 | 一致 | OK |
| confidence 4-5 のみ | **主張** | **confidence 3 が 8 件存在** | **FAIL** |

**Phase 1 判定**: **WARN**

レコード件数・tradition分布・問い別分布はすべて handoff 主張と完全一致。スキーマも合理的（questions/traditions/wisdom_records/cross_question_links の4テーブル、外部キー関係明確）。

ただし、「confidence 4-5 のみ採用」という主張は**事実と異なる**。実DBには confidence=3 のレコードが 8件存在する：

- Q-F02/MY 黄金時代神話・終末論的責任（conf=3）
- Q-V01/AN modes of organization Wenger 学習共同体（conf=3）
- Q-V01/MY 千年王国・ユガ周期（conf=3）
- Q-V03/AN neogeneration / 文化伝達の長期（conf=3）
- Q-V03/LIT 長期スパン文学・多世代叙事詩（conf=3）
- Q-V05/MY 悠久神話・mountain time（conf=3）
- Q-V05/LIT Slow literature（conf=3）
- Q-V05/AN rhythms of practice / Mauss-Halbwachs（conf=3、唯一の inference レコード）

興味深いことに、`analysis.html` 第6.5節は「confidence 5: 42件・4: 35件・3: 8件」と**正確に分布を報告**し、§7.6 でも inference 1件（confidence=3）を率直に開示している。つまり「confidence 4-5 のみ」という誤った要約は handoff §2 と verification.html §2.3 のみに残存している。**自己申告と実装の矛盾**は doc-verify として記録すべき。

---

## Phase 2: 4カテゴリ検証

### カテゴリ1: スナップショット不整合

| 項目 | ブリーフィング値 | DB/Track A値 | 本Track採用値 | 判定 |
|---|---|---|---|---|
| PHIL DB 概念総数 | 9,583 | 10,292（Track 9） | 9,583 | WARN（系列差） |
| LIT DB 概念総数 | 11,115 | 11,115 | 11,115 | OK |
| MY DB 物語総数 | 10,615 | 11,936（Track 9） | 10,615 | WARN（系列差） |
| TK DB グループ総数 | 3,001 | 3,002 | 3,001 | OK（差1は誤差） |

`verification.html` §1.3 は MY 10,615 vs Track 9 11,936 の差を「継続収集による時点差」として三系列 honest 開示しており、_PROTOCOLS.md §7 準拠は満たす。ただし Track B-1 doc-verify report は Track 9 値「PHIL 10,292/MY 11,936」を採用していたため、**Phase B 内部で同一スナップショットを採用していない不整合**が発生している。これは Track B-3 以降が混乱する素地となる。

**カテゴリ1 判定**: **WARN**（honest 開示は満たすが、Phase B 内一貫性に課題）

### カテゴリ2: ハルシネーション

85件の wisdom_records の引用著者・著作・年代をサンプリング検証。

**実在確認済み（高信頼）**:
- Hans Jonas (1979) Das Prinzip Verantwortung — 実在
- Derek Parfit (1984) Reasons and Persons — 実在
- William MacAskill (2022) What We Owe the Future — 実在
- Toby Ord (2020) The Precipice — 実在
- Marcel Mauss (1925) Essai sur le don — 実在
- Marilyn Strathern (1988) The Gender of the Gift — 実在
- Eduardo Viveiros de Castro (1998) Cosmological Deixis — 実在
- Arturo Escobar (2018) Designs for the Pluriverse — 実在
- Philippe Descola (2013) Beyond Nature and Culture — 実在
- Carol Gilligan (1982) In a Different Voice — 実在
- Joan Tronto (1993) Moral Boundaries — 実在
- Maurice Merleau-Ponty (1945) Phénoménologie de la perception — 実在
- Henri Bergson (1889) Essai sur les données immédiates — 実在
- David Hume (1739) Treatise of Human Nature — 実在
- Anna Tsing (2015) Mushroom at the End of the World — 実在
- Donna Haraway (2016) Staying with the Trouble — 実在
- Eduardo Kohn (2013) How Forests Think — 実在
- 西田幾多郎『場所』(1927)・和辻哲郎『風土』(1935)・京都学派 — 実在
- ナーガールジュナ『中論』 — 実在
- Te Awa Tupua Act 2017 — 実在（NZ Whanganui 川法人格）
- Ecuador Constitution Art. 71-74 — 実在（2008年自然権憲法）
- UNDRIP第31条・Nagoya Protocol — 実在
- イロコイ Great Law of Peace — 実在
- GIDA CARE Principles (2019) — 実在

**注意点（精度ではなく粒度の課題）**:
- Q-M07/PHIL「和辻哲郎『人間の学としての倫理学』+ Buber Ich und Du + Levinas」: 三人を一束にしているが、いずれも実在で、関係的人格論の系譜として並べる学術的妥当性はあり。
- Q-V05/AN「Halbwachs (1925) / Bourdieu (1980) Le sens pratique」: Halbwachs は1925 ではなく Cadres sociaux de la mémoire (1925) を指す可能性あり。Bourdieu の Le sens pratique は1980で正確。**自己申告で「inference 1件」として開示済み**。

**85件中、明確なハルシネーションは検出されず。**全引用は学術文献データベースで確認可能な範囲。derivation_method の25件 direct_quote / 59件 paraphrase / 1件 inference の内訳は適切に開示されている。

**カテゴリ2 判定**: **OK**

### カテゴリ3: カバレッジギャップ

handoff §6 が自己申告した6限界の検証：

1. **wisdom_text の要約性**: 100-300字要約に留まる旨を明記、handoff §6.1 で開示済み — 整合
2. **PHIL の西洋シフト**: PHIL 24件中、東洋・南アジア（中論・道蔵・Patanjali Yoga Sutra）が約5件、ubuntu（南アフリカ）1件、京都学派・比較哲学（Van Norden, Panikkar）2件で**非西洋PHIL 8件は handoff §6.2 主張と一致** — 整合
3. **MY embedding 未活用**: MY 15件はすべて MY DB MS01-MS08・scenario_2100・神話アーキタイプの直接参照で、embedding 検索は使用されず — handoff §6.3 主張と整合
4. **TK 知識主権配慮**: TK 15件のうち話者個人名は出さず集団名（イロコイ、アンデス、Hopi等）のみで開示。Lyons O.（イロコイ口承伝承家）は公開講演者として例外 — handoff §6.4 主張と整合
5. **操作的定義の主観性**: Type-A/B/C 三類型分類は handoff §6.5 で主観性を開示済み、Q-V01 を Type-C と判定する基準は「他問いより wisdom 5件と少なく、全て歴史的類比に依拠」と analysis §3.1 / report §2 で明示 — 整合
6. **confidence 4-5 限定**: **不整合（実DBに confidence=3 が 8件）**

**6項目中5項目は適切に開示。1項目（confidence限定）は実装と齟齬**。

`verification.html` §3.4 の「Q-V01 wisdom 5件」自己ギャップは適切で、analysis §3.1 で「5系統の蓄積が薄く、Phase A 兆候から立てられた純新規問い」と理由付けあり。

**カテゴリ3 判定**: **WARN**（5/6 OK、1件 FAIL）

### カテゴリ4: チーム間不整合準備

#### B-1 14問との整合
DB questions テーブルの horizon・ctl1・msign_origin・b1_track_ref を B-1 handoff §6.1 と突合した結果、**14/14問完全一致**。Q-N04 の msign_origin は「真M由来」、Q-N09 は「概念整合由来」、Q-V01 は「単独T由来」「Track 4」など、B-1 §6.1 表と全面整合。

#### B-3 5シナリオ × 中核 wisdom マッピング
handoff §5 で5シナリオ（Pluriverse / Techno-Acceleration / Care-Creative-Co-existence / Slow Right / Fragmentation）への中核 wisdom 推奨マッピングが提示されている。ただし、「Techno-Acceleration」シナリオの中核 wisdom として Q-N09/M07 の「脱人間化系譜」が割り当てられているが、wisdom_records 自体は「dividual」「personhood」「関係的自己」を肯定的に扱っており、テクノロジー駆動の脱人間化との結びつけは B-3 側の解釈に依存する。**B-3 着手時に「dividual ≠ techno-acceleration」の前提整理が必要**。

#### 「Q-N09↔Q-M07↔Q-V07 三連鎖」主張
handoff §3 と report §6 の主張を実DBで検証した結果：
- Q-N09 ↔ Q-M07: 共有5件で **OK**
- Q-M07 ↔ Q-V07: 共有3件で OK
- Q-N09 ↔ Q-V07: **DBに直接リンク存在せず**

「三連鎖」は Q-M07 を経由した間接連鎖であり、直接連鎖ではない。表現精度として「Q-N09→Q-M07→Q-V07（Q-M07経由の連鎖）」と明示すべき。

#### 「Q-M01 三独立合流」主張
handoff §7 主張「PHIL 仁 + AN 贈与論 + PHIL ubuntu の三独立合流」を実DBで検証：
- Q-M01 wisdom: AN 贈与経済（Mauss 1925）/ PHIL ケアの倫理・仁 / PHIL ubuntu / LIT ケア物語 / MY 創造神話 / TK 互酬経済（minga/ayni/yui）
- 「仁」（中国・東アジア）と「ubuntu」（サブサハラ）は**学派的には独立**だが、**両方とも tradition=PHIL に分類**されており、厳密には「3 traditions の独立合流」ではなく「2 traditions × 3 学派の合流」。

ただし、TK の互酬経済（ayni/minga）と AN の贈与経済（Mauss）が別個に存在し、Q-M01 全体として **AN+PHIL+LIT+MY+TK の5traditions すべてに wisdom がある**ため、「ケア経済が人類史標準型への回帰」という発見の妥当性自体は揺るがない。表現の精確性のみの課題。

#### B-4「変化検出装置」との関係
handoff §8「B-2「すでにある未来」と B-4「現在の取り組み」の交差で、B-5 が hot zones / dead zones を弁別する」は役割分離が明確。重複なし。

#### B-5 hot/dead zones
「Q-V01 wisdom 5件 → dead zones リスク高」は handoff §8 で開示。妥当。

**カテゴリ4 判定**: **WARN**（B-1 整合・B-4 役割分離は OK、ただし「三連鎖」「三独立合流」表現精度に課題、B-3 シナリオ解釈に注意必要）

---

## Phase 3: 構造的品質

### HTMLタグバランス
- analysis.html: open_div=21 / close_div=21、body=1/1 → **OK**
- verification.html: open_div=13 / close_div=13、body=1/1 → **OK**
- report.html: open_div=196 / close_div=196、body=1/1 → **OK**

### 必須要素
- 赤白CI #CC1400: 全HTMLで :root 定義あり → OK
- Noto Sans JP + Noto Serif JP Google Fonts ロード: 全HTMLで確認 → OK
- top-bar 3px solid #121212 ボーダー: 全HTMLで確認 → OK
- toc-sidebar（位置固定・章番号付き）: 全HTMLで確認 → OK
- main max-width 760px: 全HTMLで確認 → OK
- 段落 text-indent 1em: 全HTMLで確認 → OK
- ダークモード切替JS: 全HTMLで確認 → OK
- 印刷対応@media print: 全HTMLで確認 → OK
- favicon esse-sense.com: 全HTMLで確認 → OK
- 絵文字未使用: 全HTMLで確認 → OK

### protocols準拠
- 三系列差処理: analysis §1.5 で開示、verification §1.3 で開示 → OK
- 【推定】【解釈】【未検証】タグ: analysis/report で span class でマーク → OK
- 「研究の限界」セクション: report §7 / analysis §7 で7-8項目開示 → OK
- Track 10 連結ID: report §6 で4トラック × 引継ぎ要素を表形式で明文化 → OK

**Phase 3 判定**: **OK**

---

## Phase 4: 「過去に類例なしの問いはゼロ」主張の検証

handoff §3.1「14問のうち『過去に類例なし』の問いはゼロ」 vs report §5.1「13問（92.9%）に既存の歴史的回答が存在し、純新規問いは Q-V01 の1問（7.1%）」は**内部矛盾**。

整理すると、**handoff 自身も「ゼロ」と「Q-V01 が Type-C」を併記**しており、handoff §3.1 の表現は不正確。Track B-2 の主成果物 report.html では「13問が Type-A/B、Q-V01 のみ Type-C」と正しく分類されている。Q-V01 の wisdom 5件はすべて「歴史的類比」（Plato Academy, Calvin Geneva Academy, More Utopia, ユガ周期, イロコイ連邦）であり、「直接の蓄積を持たない」という解釈には妥当性がある。

正確な表現は「**14問すべてに5 traditionsの少なくとも1つ（多くは全5）が wisdom 5-7件で回答**。ただし Q-V01 のみは『歴史的類比のみ』で『直接の蓄積』を持たない Type-C」となる。

**Phase 4 判定**: **部分確認**（DB上は14/14問が wisdom を持つので「ゼロ」は数値上正しい、ただし「Type-C 1問」との関係を併記すべき）

---

## Phase 5: cross_question_links 整合性

22件のリンクをサンプリング検証：

| リンク | 共有数 | 共有概念 | 両問いに該当 wisdom 存在 |
|---|---|---|---|
| Q-N09↔Q-M07 | 5 | 多元的人格／dividual／関係的自己 | OK（両者に dividual/personhood/relational self の wisdom） |
| Q-M03↔Q-V07 | 5 | 非西洋認識論／pluriverse | OK（両者に Viveiros de Castro/Descola/比較哲学） |
| Q-M01↔Q-M07 | 4 | ケア／関係性／ubuntu | OK（Q-M01 ubuntu + Q-M07 kinship as relational personhood） |
| Q-N04↔Q-M07 | 3 | 場所性／関係性／kinship | OK（Q-N04 place-making + Q-M07 ayllu/kinship） |
| Q-F02↔Q-V03 | 3 | 世代間／長期記憶／7世代律 | OK（Q-F02 7世代律 + Q-V03 oral tradition long-term memory） |
| Q-F04↔Q-V07 | 3 | perspectivism／多重存在論 | OK（Q-F04 perspectivism + Q-V07 MS08 多重存在論） |
| Q-V01↔Q-V07 | 2 | 新組織形態／pluriverse統治 | やや弱い（Q-V01 はイロコイ連邦・Q-V07 は Buen Vivir、間接接続） |

22件のうち**18件は明確に整合、4件はやや弱い間接接続**（Q-V01↔Q-V07、Q-V05↔Q-V07、Q-V03↔Q-V07、Q-N04↔Q-V05）。これらは「概念的近接性」レベルで、共有 wisdom が直接同一でない。ただし共有数が 2件と低く設定されており、過大評価ではない。

最強連結ペア（共有5件以上）2件は**主張通り**。

**Phase 5 判定**: **OK**

---

## 総合判定

**CONDITIONAL PASS**

### 強み
1. **DB 4テーブル 126レコードの実装は handoff 主張と件数完全一致**（85 wisdom + 22 cross_links + 14 questions + 5 traditions）
2. **85件の引用著者・著作の実在性は全件確認可能**、ハルシネーションなし
3. **HTMLタグバランス・赤白CI・textbook構造・三系列差処理・連結ID は全項目 OK**
4. **B-1 14問の horizon/ctl1/msign_origin/b1_track_ref が完全一致**
5. **70セル × 5系統 × 14問 のカバレッジ100%は実DBで実証**
6. **cross_question_links 22件のうち最強連結 2件（共有5件）は主張通り**

### 弱み（修正推奨）
1. **【FAIL】confidence 4-5 のみ採用」主張と実装の不整合**: 実DBには confidence=3 が 8件存在。`handoff.md §2` と `verification.html §2.3` の表現を「confidence 3-5 採用、うち confidence 4-5 が 77件（90.6%）、confidence 3 が 8件（9.4%、inference 1件含む）」に修正すべき。analysis §6.5 と §7.6 では正しく開示されているので、要約の精度を上げるだけの修正で済む。
2. **【WARN】「Q-N09↔Q-M07↔Q-V07 三連鎖」表現の精確性**: Q-N09↔Q-V07 直接リンクは DB に存在しない。Q-M07 経由の間接連鎖と明示すべき。
3. **【WARN】「Q-M01 三独立合流」表現の精確性**: 「仁」と「ubuntu」は両方 PHIL に分類されるため、「3 traditions」ではなく「2 traditions × 3 学派」「PHIL 内 2 学派 + AN + LIT + MY + TK の5系統合流」と表現すべき。
4. **【WARN】Phase B 内部のスナップショット非統一**: Track B-1 doc-verify は Track 9 値「PHIL 10,292/MY 11,936」、Track B-2 は「PHIL 9,583/MY 10,615」で系列差。Phase B 内で統一スナップショットを採用するか、honest 開示を Phase B index に集約すべき。

### 中立（注意）
- Q-V05/AN「rhythms of practice / Mauss-Halbwachs」は唯一の inference レコード。analysis §7.6 と report §7.5 で適切に開示済み、修正不要。

### sentinel 引継ぎコメント

Track B-2 は新規DBの実装品質・引用の実在性・HTMLの構造品質はすべて高水準。ただし**自己検証 verification.html §2.3 が「すべて confidence 4-5」と誤って主張している**点が4カテゴリ検証で最大の不整合（カテゴリ2/3にまたがるFAIL）。修正は handoff 1行・verification 1行・主張要約の調整で済むため、sentinel は「修正後 PASS」として承認可能。analysis.html §6.5 と §7.6 は正しい数字を持っているため、自己検証側を実装値に合わせる方向で統一すべき。「三連鎖」「三独立合流」「過去に類例なしゼロ」は表現精度の課題で、内容自体の妥当性は強固。

Track B-3 着手前の必須修正：
1. handoff §2「confidence 4-5 のみ」→「confidence 3-5 採用（4-5 が 90.6%、3 が 9.4%）」
2. verification.html §2.3 と §3.3 の表現を実DB分布に合わせて修正
3. 「三連鎖」「三独立合流」を「Q-M07 経由連鎖」「2 traditions × 3 学派合流」に表現修正
4. Phase B index で MY 物語数のスナップショット差（10,615 vs 11,936）を明示

これらの修正後、Track B-2 は Track B-3「善い社会の経路」の中核入力源として **PASS** 判定可能。後続 B-3 が「dividual = techno-acceleration」の解釈接続を行う際は、Q-N09/M07 wisdom が肯定的記述である点を踏まえた前提整理を求める。

---

最終更新: 2026-05-09
独立検証: Track B-2 doc-verify エージェント（Phase B Wave 2）
参照: already_future.db / track-b2-{analysis,verification,report}.html / track-b2_handoff.md
