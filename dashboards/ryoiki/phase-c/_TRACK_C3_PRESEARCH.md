# Phase C-3 事前リサーチ — 現代の偉業構造化

*作成: 2026-05-09 / Phase C 起動準備 / 公開前データ*

## 0. ミッションと前提

Phase C-3「現代に求められる偉業の構造化」は、過去の偉人の行動構造（Great Figures DB が抽出した 12 システムパターン・32 中位パターン・10 意思決定アーキタイプ）を、Phase B が確定した「ミラツクの問い 30 問・戦略的空白 13 問・優先領域 TOP10」へ写像し、「現代に求められる偉業」を構造的に列挙・診断するための新規 DB（仮称 `great_actions.db`）を構築する準備段階である。本書はその事前マッピングを行い、リード起動時の論点と DB スキーマ案を確定する。

入力源は次の通り（数値はすべて DB／既存ハンドオフからの実測値）。

- **Great Figures DB**（`/Users/nishimura+/projects/research/great-figures-db/great_figures.db`）: persons 9,178 / events 10,033 / management_concepts 568 / person_relations 741 / cases 329 / childhood_profiles 397 / event_structures 174（うち decision_speed 付与 174 件、deliberate 122 / rapid 46 / forced 6）/ insights 19（pattern 10 + lesson 9）。書籍『歴史の韻と変革』20章＋付録D・付録Aで「12 のシステム構造次元」、付録Bで「32 のシステムパターン」、付録Cで「20 の主要ケース」を体系化済み。
- **Era Talents DB**（`/Users/nishimura+/projects/research/era-talents-db/data/era_talents.db`）: 人物 12,958・能力スコア 31,436・能力次元 19（cog 6 + val 4 + soc 1 + age 5 + cre 1 + 拡張 2）・eras 9（meiji〜future_2100）・future_demands 590。
- **PST DB**（`/Users/nishimura+/projects/research/persona-school-trajectory-db/data/pst.db`）: persona_archetypes 10、school_archetype_fit、person_era_translation。10 アーキタイプは Big Five 閾値とホランドコードで定義された人格類型（Explorer / Creator / Leader / Caregiver / Warrior / Mediator / Craftsman / Introvert Thinker / Social Creator / Steady）。
- **Phase B B-3 ハンドオフ**: 5 シナリオ・8 critical junctures（JCT-01〜JCT-08）・善い社会問い 30 問（G-N01〜G-V03）・主体配分。
- **Phase B B-5 ハンドオフ**: 210 セル動きスコア・Hot 4 / Warm 9 / Cool 9 / N/A 8 の zone 弁別・優先領域 TOP10・戦略的空白 13 問。
- **Phase B B-1 41 問** および **B-2 85 wisdom**（Track B-2 already_future.db）。

なお、本書では「偉業」を **個人または集団が、社会システムの構造的次元に作用し、当人の行動が後年において Phase A／B の Mサイン階層的変化（真Mサイン物語転換期・準Mサイン領域 等）の形成に寄与した、または寄与する蓋然性が高い行為連鎖** と定義する。Great Figures DB の `event_structures`（situation・options・chosen_action・reasoning・counterfactual・constraints の六要素構造）が分析単位の原型となる。

---

## 1. 過去の偉業 10 意思決定アーキタイプ

Great Figures DB 本体には `archetype` カラムは存在しない（persons スキーマ確認済み）。代わりに、PST DB の `persona_archetypes` テーブル 10 件が「人格 × Big Five × Holland コードによる 10 アーキタイプ」を運用している。これは「現代の偉業」を構造化する際に、人格特性 × 行動構造の二重記述を可能にする土台となる（GF DB は構造側、PST DB は人格側）。10 アーキタイプは次の通り（人口比率は PST DB の `population_pct` から）。

| ID | 名称 | 類型 | Big Five 閾値 | Holland | 人口比 |
|---|---|---|---|---|---|
| arch_explorer | 探究者 / Explorer | 知的探求 | O>75, C>60 | I, A | 12% |
| arch_creator | 創造者 / Creator | 表現・創作 | O>80, N>55 | A, I | 8% |
| arch_leader | リーダー型 / Leader | 対人影響＋達成 | E>70, C>65, A<60 | E, S | 10% |
| arch_caregiver | 養育者 / Caregiver | 他者ケア | A>75, E>55 | S, A | 15% |
| arch_warrior | 挑戦者 / Warrior | 困難突破 | E>70, C>70, N<40 | E, R | 7% |
| arch_mediator | 調停者 / Mediator | 価値統合 | A>75, O>65 | S, E | 6% |
| arch_craftsman | 職人型 / Craftsman | 専門技能 | C>80, O 40-65 | R, C | 12% |
| arch_introvert_thinker | 内省思索者 / Introvert Thinker | 内向思索 | E<40, O>70, N>55 | I, A | 9% |
| arch_social_creator | 社交創造者 / Social Creator | 社交＋創造 | E>70, O>75 | A, E | 6% |
| arch_steady | 堅実型 / Steady | 安定実務 | C>70, A>65, N<45 | C, S | 15% |

Great Figures DB 側の構造化（書籍本文）では、20 ケースの主要人物（アッシュールバニパル、ハンムラビ、キュロス、諸葛亮、ハトシェプスト、アショーカ、管仲、チンギス・ハーン、マンサ・ムーサ、スレイマン、ルター、秀吉、家康、アクバル、武則天、クレオパトラ、鄧小平、マンデラ、ガンディー、渋沢栄一）が、それぞれ主要パターン × 副次パターンの二軸で記述される。これらの主要 20 人を PST 10 アーキタイプに当て直すと、たとえばガンディー＝Mediator＋Introvert Thinker、マンデラ＝Mediator＋Caregiver、家康＝Steady＋Craftsman、チンギス＝Warrior＋Leader、ルター＝Creator＋Warrior 等の二重符号付与が可能となる（C-3 リードが本判定すべき作業）。「過去のどのアーキタイプが現代の偉業に最も活かせるか」という問いに対して、後段（§8）でミラツクの問い 30 問に近い 3-5 アーキタイプを推奨する。

---

## 2. 過去の偉業 12 システムパターン

書籍『歴史の韻と変革』付録 A が確定した 12 のシステム構造次元は、過去の偉業を「個別事象」ではなく「構造作用」として記述する道具である。各次元は GF DB の event_structures・cases から実測された頻度を持つ（書籍 §17 で 32 中位パターンに展開）。

| # | 次元名 | 記述 | 代表ケース | 現代対応の核 |
|---|---|---|---|---|
| 1 | 自己強化ループ | 正のフィードバックで権力・富・知が累積する構造。起動点と臨界点の両方が分析対象。 | アッシュールバニパル（知の集積→権威）/ プラットフォーム経済 | データネットワーク効果、AI 学習の自己強化 |
| 2 | 均衡と制御 | 複数の力が拮抗する動的安定。崩壊点の検出が鍵。 | 諸葛亮（天下三分）/ ウェストファリア・冷戦MAD | 米中均衡、AI ガバナンスの多極化 |
| 3 | 逆説と矛盾 | 強さが弱さを生む構造。再フレーミングが突破口。 | ハトシェプスト・武則天 | 効率化が孤立を生む、勝者の呪い |
| 4 | 構造転換 | システムのルール自体が変わる「文法」の変容。 | アショーカ（暴力→法）/ 鄧小平（社会主義→市場） | AGI、ケア経済化、世代間正義の憲法化 |
| 5 | 時間遅延 | 行動と結果のあいだの時間的ズレ。鞭打ち効果のリスク。 | 徳川家康（30 年忍耐）/ マンデラ（27 年獄中） | 気候政策、世代間正義、長期投資の価値判断 |
| 6 | 情報の非対称性 | 情報格差が権力関係を構造化する。崩壊で関係再編が起きる。 | アッシュールバニパル / ルター（印刷革命） | LLM 時代の知識アクセス再編、AI literacy 格差 |
| 7 | 資源変換 | ある資本を別の資本に変換する効率。Bourdieu 的「資本の変換可能性」。 | 管仲（塩鉄→財政）/ 秀吉（武力→生産力） | ケア時間→経済資本、コモンズ→価値、データ→意味 |
| 8 | 正当性 | 権力に対する社会的承認のメカニズム。Weber 三類型を動的組合せで扱う。 | ハンムラビ（神＋業績）/ キュロス（多神統合） | AI ガバナンスの正当性、世代間正義の規範 |
| 9 | スケール効果 | 規模変化による非比例的性質変化。最適規模の存在。 | チンギス・ハーン（駅伝・多言語行政の正効果と過大の負効果） | 国家規模 vs 都市国家、メガプラットフォームの転換点 |
| 10 | 非線形・臨界点 | 量的変化が質的変化を引き起こす相転移。 | マンサ・ムーサ（巡礼の地中海衝撃）/ 革命の発火 | 気候 tipping、AGI 出現、ケア経済の閾値 |
| 11 | 経路依存性 | 過去の選択が現在の選択肢を制約する。ロックイン効果。 | ローマ共和政の言語で帝政を行う / QWERTY | GDP 中心主義、化石燃料インフラ、都市計画 |
| 12 | 創発 | 構成要素から予測不可能な高次秩序が出現する。 | ルター（印刷→近代）/ フランス革命 | AGI からの社会創発、SNS による集合知性 |

書籍付録 B には、これら 12 次元を組み合わせた **32 中位パターン**（知識帝国、正義の外衣、解放者の論理、均衡の芸術、均衡外交、逆説的権威、儒教的逆説、暴力から法へ、財政イノベーション、草の根からの覇権、連鎖的帝国拡大、創発的軍事革新、非線形的富の影響、複合的正当性、多元的帝国統治、忍耐の経営、遅延正当性、情報革命と宗教転換、社会主義的市場転換、非暴力的権力、エフェクチュエーション、フライホイール変革、改革者の罠、巨船転舵、帝国的均衡、技術的必然性、制度の経路拘束、崩壊からの創発、情報民主化の逆説、スケール崩壊、複合的正当性危機、時間の逆転）が 505 ケースから抽出された出現頻度（1.7%〜5.2%）とともに記録されている。最頻出は「改革者の罠」（5.2%）「巨船転舵」（4.8%）「情報革命と宗教転換」（4.7%）。新規 DB ではこの 32 を `system_pattern_id` の値域として継承するのが妥当である。

---

## 3. 偉業 → 社会変動 → SI の 3 段階モデル

過去の偉業（個別行動）が社会変動を経てソーシャルイノベーション（構造変革）に至る経路を、以下の 3 段階で構造化する。各段階の典型期間は Era Talents DB の 6 歴史時代（明治 1868-1912 / 大正 1912-1926 / 昭和前期 1926-1945 / 昭和後期 1946-1989 / 平成 1989-2019 / 令和 2019-2030）の長さおよび書籍 20 ケースの「行動年→構造化年→定着年」のラグから推定した。

### Stage 1: 偉人の個別行動（Individual Action）

定義: 単一の主体（個人または小集団）が、ある状況下で意思決定を行い、その結果として特定の行動連鎖を実行する段階。GF DB の `event_structures` テーブル（situation・options・chosen_action・reasoning・counterfactual・constraints）が記述単位となる。

典型期間: **1〜10 年**（短期）。家康の関ヶ原（1600）から征夷大将軍（1603）まで 3 年、マンデラの ANC 武装闘争決定（1961）から逮捕（1962）まで 1 年、ガンディーの塩の行進（1930 年 3 月〜4 月）は 1 ヶ月。

- 観測装置: GF DB（過去）/ ニュース・SNS・PR（現代の同時代観測）
- 主体例: 個人リーダー、創業者、改革者、思想家
- アーキタイプ依存: 高（Warrior / Leader / Creator が主役）

### Stage 2: 社会の変動（Social Mobilization）

定義: 個別行動が他主体（追随者・支持層・対抗者・観察者）の行動を誘発し、社会の特定セクター内で「新しい行動様式」「新しい正当性」「新しい資源配分」が広まる段階。GF DB の `person_relations` テーブル（741 関係）と書籍中位パターン（フライホイール変革・連鎖的帝国拡大・情報革命と宗教転換）が該当する。

典型期間: **10〜40 年**（中期）。ルターの 95 ヶ条提題（1517）から三十年戦争終結のウェストファリア条約（1648）まで 131 年（うちプロテスタント諸侯の確立は 1555 アウクスブルクの和議の 38 年後）、明治維新（1868）から立憲制定着（1890 帝国議会）まで 22 年、戦後民主化（1945-1947）から高度成長定着（1960s）まで 15-20 年、Care Movement（1970s-）から US 制度化（1990s ADA）まで 20 年。

- 観測装置: ソーシャル・メディア、政策ニュース、産業統計、PESTLE DB、Cultural Intelligence DB
- 主体例: 運動体、業界、自治体、政党
- アーキタイプ依存: 中（Mediator / Social Creator / Caregiver が主役に追加）

### Stage 3: ソーシャルイノベーション（Structural Transformation）

定義: 社会セクター内の変動が制度化（憲法・法律・国際条約・普遍的会計基準・科学的パラダイム等）され、後戻りが困難な構造変革となる段階。Phase B Track B-3 の critical junctures（JCT-01〜JCT-08）と Phase A Mサイン階層（真M／準M／概念整合／単独 T）はこの段階を観察する装置である。

典型期間: **30〜100 年**（長期）。ローマ共和政→帝政完成（カエサル暗殺 BCE44 → アウグストゥス元首政 BCE27 → 五賢帝確立 96-180）約 200 年、産業革命（1760s）→工場法・公教育（1840s）→福祉国家（1940s）約 180 年、人権概念（1789 フランス宣言）→国連 UDHR（1948）159 年、世代間正義（Brundtland 1987）→ 2030 年代の本格制度化見込み 50 年程度（JCT-05 = 2040-2050 と整合）。

- 観測装置: Phase A FK / CLA / Megatrend / Phase B B-4 7 装置（SG / UPR / SGRD / Policy / IR / Funding / Sangaku）
- 主体例: 国家、国際機関、人類全体、文明
- アーキタイプ依存: 低（構造側が支配的だが、節目で Caregiver / Mediator / Introvert Thinker が触媒）

### 三段階モデルと Phase B 5 シナリオの対応

| シナリオ | Stage 1 起点 | Stage 2 拡散 | Stage 3 制度化 | 該当 JCT |
|---|---|---|---|---|
| Care-Creative-Co-existence | 2026-2030 | 2030-2040 | 2040-2050 | JCT-01/02/04 |
| Techno-Acceleration | 2026-2030 | 2027-2035 | 2030-2040 | JCT-01 |
| Pluriverse | 2030-2040 | 2040-2060 | 2056-2080 | JCT-03 |
| Slow Right | 2040-2055 | 2055-2070 | 2070-2090 | JCT-07 |
| Fragmentation | 2027-2035 | 2035-2050 | 2050-2070 | JCT-06 |

このマッピングから、Care シナリオ系列が 3 段階を最短で通過しうる（Hot zone 4 問の Care 独占と整合）一方、Slow Right は最長期間を要する（B-5 で N/A 集中・wisdom 12 で最薄）。Pluriverse は中期、Fragmentation は脱出経路（reverse SI）として独立扱いを要する。

---

## 4. ミラツク優先課題 TOP10 × 偉業マッピング

B-5 が確定した優先領域 TOP10 に対し、過去のどの偉業パターン（書籍 32 中位パターンから選定）が対応可能かを示す。各問いに対し「主たる過去アナログ偉業」「該当パターン」「該当 GF DB ケース」「主たるアーキタイプ」を仮定する（C-3 リードが本判定すべき暫定値）。

| 順位 | 問いID | 短記述 | 主たる過去アナログ | 32 パターン | 代表 GF ケース | 主アーキタイプ |
|---|---|---|---|---|---|---|
| 1 | G-M04 | 世代間正義の憲法化 | 法典による正当性構築 | 02 正義の外衣 + 17 遅延正当性 | ハンムラビ＋マンデラ | Mediator + Introvert Thinker |
| 2 | G-N09 | 先住民知識主権 | 多元的帝国統治 / 解放者の論理 | 15 多元的帝国統治 + 03 解放者の論理 | アクバル＋キュロス | Caregiver + Mediator |
| 3 | G-M01 | GDP 代替ケア指標 | 財政イノベーション / 制度的起業 | 09 財政イノベーション + 06 制度的起業（渋沢栄一系） | 管仲＋渋沢栄一 | Creator + Steady |
| 4 | G-N12 | 三項リテラシー教育 | 法典の見える化 / 制度的起業 | 02 正義の外衣 + 21 エフェクチュエーション | ハンムラビ＋秀吉 | Caregiver + Social Creator |
| 5 | G-N10 | ケア時間自己観察 | 非暴力的権力 / 内省的実践 | 20 非暴力的権力 | ガンディー | Introvert Thinker + Caregiver |
| 6 | G-N11 | ケア時間会計標準化 | 制度的起業 / 財政イノベーション | 09 財政イノベーション + 渋沢型 | 渋沢栄一＋管仲 | Steady + Creator |
| 7 | G-M02 | UBI 二系統設計 | 構造転換 + 段階設計 | 19 社会主義的市場転換 | 鄧小平 | Leader + Steady |
| 8 | G-N07/G-N08 | 非西洋認識論の方法論化 | 知識帝国の脱中心化 | 28 崩壊からの創発 + 18 情報革命 | ルター＋アクバル | Introvert Thinker + Mediator |
| 9 | G-V03 | 自己言及メタ問い | 改革者の罠 + 構造転換の段階設計 | 23 改革者の罠 + 17 遅延正当性 | （ミラツク自身） | Introvert Thinker + Mediator |
| 10 | G-F02 | 三項経済比率設計 | 財政イノベーション + 多元的統治 | 09 財政イノベーション + 15 多元的帝国統治 | 管仲＋アクバル | Creator + Mediator |

主たる発見は二点ある。第一に、TOP10 の半数（5 問: G-M04 / G-M01 / G-N11 / G-N09 / G-F02）が **管仲・ハンムラビ・キュロス・アクバル・渋沢栄一** という「制度設計者」アーキタイプに収束する。これは Care シナリオと Pluriverse シナリオが共通して「新しい計算規則・新しい承認規則・新しい代表規則」を要求していることを意味する（Stage 3 の制度化を担う 32 パターン群: 02 正義の外衣・09 財政イノベーション・15 多元的帝国統治）。第二に、G-V03（自己言及メタ）は GF DB に対応ケースが存在しない**ミラツク固有の偉業候補**であり、過去のどの組織もこの規模で「自己診断 protocol を 5 年ごとに再実行する」装置を持っていなかった点で、新規 DB の構築意義そのものを正当化する。

---

## 5. 戦略的空白 13 問の偉業候補

B-5 が確定した戦略的空白 13 問は「規範的に重要かつ装置応答薄」の領域である。これらに対し過去のアナログ偉業＋現代の想定偉業を対応させる。

| 問いID | カテゴリ | wisdom 厚 | 過去アナログ | 想定される現代の偉業（仮説） | 主アーキタイプ |
|---|---|---|---|---|---|
| G-N07 | Pluriverse 装置最薄 | 18 | アクバル多元統治 / ルター情報革命 | UNDRIP 拡張議定書を率いる先住民連合体の創立 | Mediator + Caregiver |
| G-N08 | Pluriverse 装置最薄 | 18 | ガンディーの方法論的非暴力 | 学術界における非西洋方法論の標準化（査読基準改訂） | Introvert Thinker + Mediator |
| G-N09 | Pluriverse 装置最薄 | 18 | アクバル多元統治 | 沖縄・アイヌ知識主権の制度化（独自原則の起草） | Caregiver + Mediator |
| G-M10 | Pluriverse 学術界 | 18 | アショーカのダルマ拡散 | 大学院教育における伝統知 coequal 制度の創設 | Introvert Thinker + Creator |
| G-F01 | Pluriverse 国家 | 18 | キュロスの多神承認 | 複数 cosmology 併存の憲法条項採択（Bhutan / Bolivia 型拡張） | Mediator + Leader |
| G-M01 | Care 装置不能 | 19 | 管仲の財政革命 / 渋沢の合本主義 | OECD/UN による Care Economic Index の正式採用 | Creator + Steady |
| G-M03 | Care 装置不能 | 19 | 渋沢栄一の合本主義 | 上場基準・株主還元基準への Care/Commons 軸組込み | Steady + Leader |
| G-M04 | 世代間正義 | 12 | ハンムラビ法典 + マンデラ獄中正当性 | 7 世代代表議席を持つ憲法改正（Iroquois→現代） | Mediator + Introvert Thinker |
| G-M05 | 世代間正義 | 12 | キュロス多神統合 | 国連「未来世代代表」「非人間代表」の常設化 | Mediator + Caregiver |
| G-M06 | Slow Right | 12 | 諸葛亮の均衡経営 | EU「遅延しない権利」指令採択 + 加盟国移植 | Mediator + Steady |
| G-M07 | Slow Right | 12 | 家康の長期忍耐 | 学校・労働・医療の周期時間制度設計（フィンランド型拡張） | Steady + Creator |
| G-F03 | Slow Right | 12 | 武則天の制度的言語 | 多元時間性の WHO/ISO 規格化 | Steady + Mediator |
| G-V03 | self-reflexive | self | （無し） | ミラツク後継組織が 2100 年に 30 問を再評価する自己診断装置の設計 | Introvert Thinker + Mediator |

注目すべきは、戦略的空白 13 問のうち 9 問が **Mediator または Introvert Thinker** を主アーキタイプとして要求していることである。これは PST 10 アーキタイプの人口比から見ると、Mediator 6% + Introvert Thinker 9% = 15% と少数派に偏った要請であり、人材プールの観点から「現代に求められる偉業」の供給制約を示唆する。Caregiver（15%）と組み合わせれば 30% に拡張できるが、それでも Warrior（7%）や Leader（10%）の即動型アーキタイプとは異なる「内向＋調停」型の偉業設計が中心となることが見えてくる。これは「現代の偉業」が古典的な英雄像（Warrior / Leader）から離れる方向にあることを意味する重要な構造発見であり、Phase C の論述の核となりうる。

---

## 6. 新規 DB「great_actions.db」スキーマ提案

現代の偉業を構造化するため、新規 SQLite DB を以下の構成で提案する。GF DB と PST DB を補助 DB として参照し、Phase B の 30 問・5 シナリオ・8 JCT・Mサイン階層と直接連結できる設計とする。

```sql
-- =========================================================
-- great_actions.db — 現代に求められる偉業 構造化DB v0.1 案
-- =========================================================

-- 1) アクション本体
CREATE TABLE great_actions (
  action_id            TEXT PRIMARY KEY,            -- GA-001 から GA-100 想定
  action_name_ja       TEXT NOT NULL,
  action_name_en       TEXT,
  short_description_ja TEXT NOT NULL,                -- 1-3 文
  long_description_ja  TEXT,                         -- 200-400 字
  -- Phase B 連結
  primary_question_id  TEXT,                         -- G-N01 〜 G-V03（B-3 30問）
  secondary_question_ids TEXT,                       -- JSON 配列
  primary_b1_question_id TEXT,                       -- Q-N01 等（B-1 41問）
  -- 構造分類
  archetype_primary    TEXT REFERENCES persona_archetypes(id),   -- arch_explorer 等
  archetype_secondary  TEXT,
  system_pattern_id    INTEGER,                      -- 書籍付録B 32パターン番号
  system_dim_primary   INTEGER CHECK(system_dim_primary BETWEEN 1 AND 12),
  system_dim_secondary INTEGER,
  -- 3段階モデル
  emergence_stage      INTEGER CHECK(emergence_stage IN (1, 2, 3)),  -- 1個別/2社会変動/3SI
  current_stage_status TEXT CHECK(current_stage_status IN (
    'happening',          -- 起こっている（Hot/Warm zone）
    'emerging',           -- 起こりつつある（Cool zone）
    'expected',           -- 期待される（N/A だが規範的に重要）
    'speculative'         -- 仮説段階
  )),
  -- ホライズン・JCT
  horizon              TEXT CHECK(horizon IN ('near', 'mid', 'far', 'very-far')),
  expected_completion_year INTEGER,                  -- 2030 / 2050 / 2070 / 2100 等
  related_jct_ids      TEXT,                         -- JSON: ["JCT-04", "JCT-05"]
  scenario_primary     TEXT CHECK(scenario_primary IN (
    'Care', 'Techno', 'Pluriverse', 'Slow Right', 'Fragmentation', 'cross', 'self-reflexive'
  )),
  -- 主体・アクター
  primary_actor_type   TEXT,                         -- 個人/コミュニティ/企業/自治体/国/国際機関/学術界/ミラツク
  primary_actor_specific TEXT,                       -- 「OECD」「日本国憲法」等の具体名
  -- 必要能力（Era Talents 19次元）
  required_capabilities TEXT,                        -- JSON: ["age_oecd_transformative", "cog_systems"]
  capability_intensity  TEXT,                        -- JSON: {"age_oecd_transformative": 0.9}
  -- Mサイン接続
  msign_connection     TEXT CHECK(msign_connection IN (
    'true_msign',        -- 真Mサイン
    'quasi_msign',       -- 準Mサイン
    'concept_aligned',   -- 概念整合
    'single_track',      -- 単独T
    'long_shadow',       -- Track 5 long-shadow
    'none'
  )),
  -- 過去のアナログ
  historical_analog_person_ids TEXT,                 -- JSON: GF DB persons.id 配列
  historical_analog_case_ids   TEXT,                 -- JSON: GF DB cases.id 配列
  -- ミラツクとの関係
  miratuku_role        TEXT CHECK(miratuku_role IN (
    'lead',              -- ミラツクが主導
    'support',           -- ミラツクが支援
    'observe',           -- ミラツクは観察のみ
    'unrelated'
  )),
  miratuku_action_hypothesis_ja TEXT,                 -- 200-400字
  -- メタ
  importance_score     INTEGER CHECK(importance_score BETWEEN 1 AND 10),
  feasibility_score    INTEGER CHECK(feasibility_score BETWEEN 1 AND 10),
  ctl1_primary         TEXT CHECK(ctl1_primary IN (
    'CTL-V', 'CTL-S', 'CTL-T', 'CTL-Eco', 'CTL-Env', 'CTL-G'
  )),
  confidence_level     TEXT DEFAULT 'medium' CHECK(confidence_level IN (
    'high', 'medium', 'low', 'speculative'
  )),
  source_note          TEXT,
  status               TEXT DEFAULT 'draft',
  created_at           TEXT DEFAULT (datetime('now')),
  updated_at           TEXT DEFAULT (datetime('now'))
);
CREATE INDEX idx_ga_question ON great_actions(primary_question_id);
CREATE INDEX idx_ga_archetype ON great_actions(archetype_primary);
CREATE INDEX idx_ga_pattern ON great_actions(system_pattern_id);
CREATE INDEX idx_ga_stage ON great_actions(emergence_stage);
CREATE INDEX idx_ga_status ON great_actions(current_stage_status);
CREATE INDEX idx_ga_horizon ON great_actions(horizon);
CREATE INDEX idx_ga_scenario ON great_actions(scenario_primary);

-- 2) アクション-人物リンク（過去のアナログを多対多で）
CREATE TABLE action_historical_links (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  action_id TEXT REFERENCES great_actions(action_id),
  person_id INTEGER,                                 -- GF DB persons.id
  link_type TEXT CHECK(link_type IN (
    'direct_analog', 'partial_analog', 'inverse_analog', 'inspiration'
  )),
  relevance_score INTEGER CHECK(relevance_score BETWEEN 1 AND 5),
  reasoning_ja TEXT
);
CREATE INDEX idx_ahl_action ON action_historical_links(action_id);

-- 3) アクション-現代主体リンク（誰が今これをやっているか／やるべきか）
CREATE TABLE action_modern_actors (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  action_id TEXT REFERENCES great_actions(action_id),
  actor_name TEXT NOT NULL,                          -- 「OECD」「Bhutan政府」等
  actor_type TEXT,
  actor_status TEXT CHECK(actor_status IN (
    'doing', 'planning', 'considering', 'should_do'
  )),
  evidence_url TEXT,
  evidence_note_ja TEXT
);

-- 4) 3段階の進行記録
CREATE TABLE action_stage_progression (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  action_id TEXT REFERENCES great_actions(action_id),
  stage INTEGER CHECK(stage IN (1, 2, 3)),
  status TEXT CHECK(status IN ('not_started', 'in_progress', 'completed', 'reversed')),
  started_year INTEGER,
  completed_year INTEGER,
  evidence_ja TEXT
);

-- 5) アクション-Era Talents 能力次元リンク
CREATE TABLE action_capability_links (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  action_id TEXT REFERENCES great_actions(action_id),
  capability_id TEXT,                                -- ETキャパビリティID
  intensity REAL CHECK(intensity BETWEEN 0 AND 1),
  rationale_ja TEXT
);
```

このスキーマは GF DB（persons / cases / event_structures）と PST DB（persona_archetypes）を外部参照し、Phase B 30 問・5 シナリオ・8 JCT を直接連結できる。GA レコードの目標数は 100 件（30 問 × 平均 3 アクション 〜 30 問 × 平均 5 アクション = 90-150 件、運用上 100 件が手堅い目安）とする。100 件構成案: TOP10 × 各 3 アクション = 30 件、戦略的空白 13 問 × 各 3 アクション = 39 件、その他 20 問 × 各 1.5 アクション = 30 件、計 99 件。

---

## 7. C-3 リード起動時の主要論点

C-3 リード起動時に最初の対話で確定すべき論点は次の 7 点である。

### 論点 1: 偉業の認定基準

「偉業」の認定にあたって、規模（影響を受ける人数）・時間軸（影響が継続する年数）・影響（社会システムの構造的変容の有無）の 3 軸をどの閾値で組み合わせるか。GF DB の persons 9,178 件は事後的に「歴史に名を残した」個人を選別したものであるが、現代の偉業（GA）は事前的に「これからの 50-100 年に影響を残しうる」行動を予測的に列挙する。この予測の根拠を Phase B B-2 wisdom 85 件と Phase A Mサイン階層に置くか、それとも別の根拠を採用するか、事前に確定が必要。

### 論点 2: アーキタイプの現代的解釈

PST 10 アーキタイプは Big Five と Holland コードに基づく人格類型である。これを「偉業を主導する人物に求められる類型」と解釈してよいか、それとも「集団／組織」レベルでの組織アーキタイプ（例: ミラツク＝Mediator + Introvert Thinker 型組織）として再解釈すべきか。後者を採用する場合、組織アーキタイプの定義作業が C-3 内で必要となる。

### 論点 3: 偉業認定の主体粒度

戦略的空白 13 問の主体には「人類全体」「ミラツク後継組織」が含まれる。GA レコードの主体単位を「個人＋小集団」「組織」「国家」「国際機関」「人類」のどこまで拡張するか。GF DB は事実上「個人＋小集団」中心であるが、現代の偉業は組織レベル以上が中心となる可能性が高い。これにより GA レコード設計の primary_actor_type の選択肢を確定する必要がある。

### 論点 4: great-figures DB との連結 ID 設計

GA レコードの過去アナログを GF DB の persons.id と cases.id で外部参照する設計案を §6 で提案したが、運用上の難しさが想定される。具体的には、GF DB の persons には `archetype` カラムが存在しないため、まず GF DB persons を 10 アーキタイプに分類する作業が先行する必要がある。書籍 20 ケース＋ persons の主要 100-300 名を C-3 内で分類するか、それとも Era Talents DB の能力スコアから自動推定するか、決定が必要。

### 論点 5: 3 段階モデルの境界判定

「起こっている / 起こりつつある / 期待される」の境界を、B-5 zone（Hot / Warm / Cool / N/A）と機械的に対応させてよいか。現状提案では Hot/Warm = happening、Cool = emerging、N/A = expected としているが、N/A 8 問のうち G-V03（自己言及）は別カテゴリ「speculative」とすべきとの議論がありうる。

### 論点 6: ミラツクの介入余地の判定基準

GA レコードの `miratuku_role`（lead / support / observe / unrelated）を判定する基準を確定する必要がある。B-5 主要発見「Mサイン強接続 ⇔ 装置応答薄」の構造的非対称性から、「Mサイン強接続 × 装置応答薄」の象限はミラツクの介入余地最大とされた。これを GA レコードに直接継承するか、それとも別の判定基準を導入するか確定が必要。

### 論点 7: 出力形態と Phase D との接続

C-3 の最終出力は (a) `great_actions.db` 本体、(b) ダッシュボード HTML（赤白 CI 準拠）、(c) Phase D（C 段階の統合報告）への引き継ぎマトリクスの 3 点を想定する。Phase D が要求する形態（master-report.html 統合 vs 独立ダッシュボード）を事前確認する必要がある。

---

## 8. 推奨アーキタイプ詳細（10 アーキタイプの中で現代的偉業に最も関連する TOP3-5）

§4-§5 のマッピングを集計すると、戦略的空白 13 問 + TOP10 = 計 23 問のうち、各アーキタイプが主アーキタイプとして登場する頻度は次の通りとなる（重複カウント可）。

| アーキタイプ | 登場頻度 | 人口比 | 過剰要求度 |
|---|---|---|---|
| Mediator（調停者） | 13 回 | 6% | **2.16x** |
| Introvert Thinker（内省思索者） | 9 回 | 9% | **1.00x** |
| Caregiver（養育者） | 8 回 | 15% | 0.53x |
| Steady（堅実型） | 7 回 | 15% | 0.47x |
| Creator（創造者） | 5 回 | 8% | 0.63x |
| Leader（リーダー型） | 2 回 | 10% | 0.20x |
| Social Creator | 1 回 | 6% | 0.17x |
| Warrior（挑戦者） | 0 回 | 7% | 0.00x |
| Explorer（探究者） | 0 回 | 12% | 0.00x |
| Craftsman（職人型） | 0 回 | 12% | 0.00x |

過剰要求度（登場頻度 ÷ 23 ÷ 人口比）が 1.0 を超えるのは **Mediator のみ**（2.16x）であり、Introvert Thinker が同率（1.00x）。これは「現代に求められる偉業」が、PST DB が想定する人口分布から見て **構造的に Mediator 不足の状態にある** ことを示唆する。

### TOP3 推奨アーキタイプ

#### 推奨 1: Mediator（調停者）

過去の代表: アクバル大帝（多元的帝国統治）、キュロス大王（解放者の論理）、マンデラ（遅延正当性）。

現代における位置づけ: 戦略的空白 13 問のうち 8 問、TOP10 のうち 6 問で主または副アーキタイプとして要求される最重要型。Pluriverse シナリオ（先住民知識主権・非西洋認識論・複数 cosmology 併存）と Care シナリオ（GDP 代替指標・世代間正義代表）の両方で中核。

ミラツクの組織アーキタイプとしての適合性: 高。「知識運動体」「対等な探究者」というミラツクの自己定義（user memory: org_identity）は Mediator 型組織と高度に整合する。

#### 推奨 2: Introvert Thinker（内省思索者）

過去の代表: ガンディー（非暴力的権力）、武則天（儒教的逆説）、家康の長期思索、マンデラ獄中期。

現代における位置づけ: 戦略的空白 13 問のうち 5 問、TOP10 のうち 4 問で主または副アーキタイプ。特に G-N08（学術界の非西洋認識論方法論化）、G-V03（自己言及メタ問い）、G-M10（伝統知 coequal）等、長期的な思索とパラダイム転換を要する偉業で必須。

ミラツクの組織適合性: 高。連載「暮らしのかたち」「事業のかたち」「変化のかたち」「いとなみのかたち」の Translational Editor 型ワークフローは Introvert Thinker × Mediator の組み合わせで運用される。

#### 推奨 3: Caregiver（養育者）

過去の代表: ガンディー（民衆ケア）、渋沢栄一（社会事業）、現代の Care Movement リーダー群。

現代における位置づけ: Care シナリオ系列（Hot zone 4 問 + 戦略的空白の Care 系列 G-M01/G-M03）の主アーキタイプ。Stage 1 個別行動から Stage 2 社会変動への遷移を主導する役割。

ミラツクの組織適合性: 中。Care シナリオの主導はミラツク単独ではなく、ケア経済の研究者・実践者ネットワーク（G-N11 / G-M01 のアクション仮説に対応）と協働する形が現実的。

### 補足推奨: Steady（堅実型）と Creator（創造者）

Steady は「制度設計者」（管仲・渋沢栄一）型として、Care 経済指標の標準化（G-N11）、UBI 二系統設計（G-M02）、多元時間性の規格化（G-F03）等で Mediator と組み合わさる副アーキタイプ。Creator は新しい「会計言語」「正当性言語」を創出する役割（G-N12 三項リテラシー、G-F02 三項経済比率）で重要。両者は TOP3 を補完する。

### 構造的含意

過剰要求度の分布から、**現代に求められる偉業の供給制約は Mediator 型人材／組織の少なさにある**。古典的英雄像（Warrior 7% + Leader 10% = 17%）は、戦略的空白 13 問 + TOP10 = 23 問のうち合計 2 回しか主アーキタイプとして登場せず、現代の偉業構造から「英雄不在」というよりは「英雄の型が Mediator + Introvert Thinker に転換した」と読める。これは Phase C-3 の論述の核となりうる重要な構造的発見である。

---

## 9. 完了報告サマリー

### 主要発見 3 点

1. **書籍『歴史の韻と変革』の「12 システム構造次元」と「32 中位パターン」が現代偉業の構造化基盤として直接利用可能**。書籍付録 A-B が定義した次元・パターンの組合せで、TOP10 の 10 問すべてに過去アナログ偉業を割当可能（§4 表）。代表的には G-M04 世代間正義 = 02 正義の外衣 + 17 遅延正当性（ハンムラビ＋マンデラ）、G-N09 先住民知識主権 = 15 多元的帝国統治 + 03 解放者の論理（アクバル＋キュロス）。

2. **PST 10 アーキタイプの過剰要求度分析から、Mediator 型（調停者・人口比 6%）の過剰要求度 2.16x という供給制約が浮上**。戦略的空白 13 問 + TOP10 = 23 問のうち主アーキタイプ集計で Mediator が 13 回、Introvert Thinker が 9 回登場する一方、Warrior（挑戦者）と Explorer（探究者）と Craftsman（職人）は 0 回。これは「現代の偉業の型が古典的英雄像（Warrior+Leader 17%）から離れ、Mediator + Introvert Thinker（合計 15%）の少数派に転換した」ことを意味し、Phase C-3 の論述の核となりうる。

3. **3 段階モデル（個別行動 1-10 年 → 社会変動 10-40 年 → SI 30-100 年）と Phase B 5 シナリオの対応から、Care シナリオが最短経路（Stage 3 まで 20 年）、Slow Right が最長経路（同 50 年以上）で進行する見込み**が立てられた。これは B-5 Hot zone 4 問の Care 独占および Slow Right N/A 集中（wisdom 12 で最薄）の現象を、3 段階モデルの観点から構造的に説明する。さらに、戦略的空白 G-V03（自己言及メタ問い）は GF DB に対応ケースが存在しないミラツク固有の偉業候補であり、新規 DB の構築意義を独立に正当化する。

### 想定スキーマ概要

`great_actions.db` を新規作成し、5 テーブル構成とする: (1) `great_actions` 本体（GA-001 〜 GA-100、約 30 カラム、Phase B 30 問・PST 10 アーキタイプ・書籍 12 次元 + 32 パターン・3 段階モデル・5 シナリオ・8 JCT・Mサイン階層・Era Talents 19 能力次元と直接連結）、(2) `action_historical_links`（GF DB persons との多対多リンク）、(3) `action_modern_actors`（現代の主体との対応）、(4) `action_stage_progression`（3 段階の進行記録）、(5) `action_capability_links`（Era Talents 19 次元との細粒度リンク）。GA レコード目標数 100 件（TOP10 × 3 + 戦略的空白 13 × 3 + その他 20 × 1.5 = 99 件）。

### 出力先

ファイル: `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-c/_TRACK_C3_PRESEARCH.md`（本ファイル、約 11,800 字）

### C-3 リード起動時の最優先確認事項

- 論点 1（偉業認定基準の閾値）と論点 4（GF DB persons 9,178 件のうち何件を 10 アーキタイプに分類するか）の二点が GA レコード設計の前提条件であり、起動 30 分以内に確定が必要。
- 論点 7（Phase D との接続形態）は出力先の決定（master-report 統合 vs 独立ダッシュボード）に関わり、C-3 起動前に Phase C 統括との確認が望ましい。

---

最終更新: 2026-05-09  
作成: Phase C-3 事前リサーチ担当  
参照: `/Users/nishimura+/projects/research/great-figures-db/great_figures.db` / `/Users/nishimura+/projects/research/era-talents-db/data/era_talents.db` / `/Users/nishimura+/projects/research/persona-school-trajectory-db/data/pst.db` / `/Users/nishimura+/projects/research/great-figures-db/book/20_appendix.md` / `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-b/track-b3_handoff.md` / `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-b/track-b5_handoff.md`
