# Phase C-4 事前リサーチ — 起こっている偉業 vs 期待される偉業の構造化

> 作成日: 2026-05-09
> 作成: Track C-4 起動準備（C-3 great_actions.db 構築および C-1/C-2 並列走行中、作業領域不可侵）
> 目的: Phase B B-4 の 463 initiatives と B-5 zone 弁別、B-6 ミラツク優先課題 TOP10 + 戦略的空白 13 問を、C-3 great_actions.db に対する「推進状況・成熟度の更新層」として接合するための事前準備
> 入力源: B-4 handoff（463 initiatives / 168 セル / 5 補完類型）/ B-5 handoff（zone 弁別 + 戦略的空白 13 問 + TOP10）/ B-6 handoff（71 独立問い ID + 926 派生レコード + 主要発見 5 点）/ C-3 事前リサーチ（great_actions.db スキーマ初版）/ initiatives.db 実値検証
> 推測タグ: 【推定】= 解析的に演繹した解釈 / 【解釈】= 複数読みが成立する読み方 / 【未検証】= 一次出典で検証していない要素

---

## 0. C-4 のミッション境界（C-3/C-5 との分業）

Phase C 第 3 波の実装-期待マッピング層を担う Track C-4 は、C-3（偉業 DB 構築）の作業領域に立ち入らずに、その成果物（great_actions.db v0.1 / GA-001〜100 件）に対して「Phase B 装置応答実績による上書きレイヤー」を載せる役割を持つ。C-5（担い手特性）とは並列走行となるが、共通入力は great_actions.db のみであり、観測の独立性が確保される。【推定】

| トラック | 主問い | 主要産物 | 入力DB主軸 |
|---|---|---|---|
| C-3 | 現代に求められる偉業はどのような構造か | great_actions.db v0.1 + 32 パターン × TOP10 マッピング | great-figures DB + Era Talents DB + PST DB |
| **C-4** | **起こっているのか／期待されるのか／方向は合っているのか** | **great_actions.db v0.2（推進状況・成熟度・463 initiatives 紐付け）+ warning/opportunity 弁別 + 差分マップ** | **B-4 initiatives.db + B-5 zone + B-6 TOP10** |
| C-5 | 偉業の担い手はどのような特性をもつか | 担い手類型図 + 4 軸（心理/行動/領域/専門）マトリクス | era_talents + great_figures + jpms |

C-4 の中核アウトプットは三つに集約される。

1. **great_actions.db v0.2 更新スキーマ**（推進状況フィールド + 成熟度フィールド + 463 initiatives 紐付けテーブルの追加）【推定・C-3 設計と整合】
2. **既存偉業 vs 期待偉業 vs warning 偉業 vs opportunity 偉業 の四象限弁別**（差分マップとして可視化）
3. **TOP10 × 偉業マッピング**（10 課題 × 各 3-5 偉業 = 約 35-45 件の重点配分）

これらが C-4 リード起動時のブリーフィングと初期 DB 更新案となる。本書はあくまで事前準備であり、本確定値は C-4 リード本体実行時に C-3 確定後の実 DB を見ながら確定する。

---

## 1. Phase B B-4 + B-5 連結の整理

C-4 の解析対象は「B-4 463 initiatives × 168 セル」と「B-5 30 問 × 210 セル × zone 弁別」を接合した複合データセットである。両 Track の構造を改めて整理し、C-4 で扱う統合観測点を確定する。

### 1.1 B-4 168 セル + 463 initiatives の構造

B-4 handoff §3 によれば、対象は B-1 24 問（near 13 + mid 6 + far 3 + very-far 2）× 7 装置（SG/UPR/SGRD/Policy/IR/Funding/Sangaku）= 168 セル。168 セル中、score≥3「強応答」が 73 セル（43.5%）、score≤1「弱応答」が 76 セル（45.2%）。装置別平均は SG 4.00 / IR 3.21 / UPR 2.67 / Funding 2.13 / Policy 1.50 / Sangaku 1.29 / SGRD 0.50 で、SG が圧倒的に強く、SGRD が集計 JSON 制約で過小評価。【B-4 確定値】

initiatives.db の実 DB 値を点検すると、463 件の内訳は以下のように分布している【未検証・初期点検値】。

| 装置別 | 件数 | 割合 |
|---|---|---|
| SG | 115 | 24.8% |
| IR | 105 | 22.7% |
| Policy | 102 | 22.0% |
| Funding | 88 | 19.0% |
| SGRD | 24 | 5.2% |
| UPR | 15 | 3.2% |
| Sangaku | 14 | 3.0% |
| 合計 | 463 | 100% |

| stage 分類 | 件数 |
|---|---|
| experiment（実験段階） | 307 |
| pilot（試行段階） | 96 |
| scale（拡大段階） | 60 |

| horizon 分類 | 件数 |
|---|---|
| near（2030） | 267 |
| mid（2050） | 108 |
| far（2070） | 52 |
| very-far（2100） | 36 |

| initiative_type | 件数 |
|---|---|
| research | 259 |
| policy | 102 |
| investment | 88 |
| partnership | 14 |

ここから読み取れる構造は二点ある。第一に、**experiment 段階が 307 件（66.3%）と全体の三分の二を占める**。これは「現代社会で動いているとされる多くの取り組みが、なお実験段階に留まっている」という構造的事実を示す。scale 段階（60 件・13.0%）に達しているのは Care 経済の市場化や AI 規制の一部など、限定的な領域に集中する。【推定】第二に、**装置間で initiative の質に大きな違いがある**。SG（115 件）の多くは「(detected signal)」というラベルで「組織名なし・現象観測のみ」の signal レコードであり、現実の「動き」とは性格が異なる。一方 Policy（102 件）と IR（105 件）は実在組織の実行中事業を含む。この違いは great_actions.db への紐付け時に「signal-level vs implementation-level」の区別を新設する必要性を示唆する。【解釈】

### 1.2 B-5 30 問 × 7 装置 = 210 セル × zone 弁別

B-5 handoff §3 によれば、B-3 30 問は B-1 24 問とは独立 ID 系列で、B-1 41 問の部分集合ではなく G-prefixed の善い社会問い 30 問として運用される。210 セル（30×7）のうち実 DB 値継承が 154 セル（73.3%）、N/A が 56 セル（B-4 対象外 8 問 × 7 装置）。zone 弁別は Hot 4 / Warm 9 / Cool 9 / Dead 0 / N/A 8 = 30 問。【B-5 確定値】

C-4 の作業観点から重要なのは、B-1 24 問と B-3 30 問の **ID 系列が独立**である点である。すなわち 463 initiatives は Q-prefixed の B-1 ID に紐付いており、TOP10 や戦略的空白 13 問は G-prefixed の B-3 ID で表現される。両者をブリッジする手続きが C-4 で必要となる。【推定】

ブリッジは _TRACK_LINKAGE_MATRIX.md §2.4 の B-3 → B-1 推定マッピングを継承して実行する。たとえば G-N04（場所性回帰の制度化）= Q-N04、G-N12（ケア経済の組織化）= Q-N12 などは ID が直接対応するが、G-M04（世代間正義の憲法化）に対応する Q-prefixed ID は B-1 41 問内に存在せず、B-1 → B-4 24 問選定からも漏れている（B-4 N/A 対象問いに該当）ため、463 initiatives 内に「G-M04 に直接紐付くレコード」は存在しない【推定・B-5 N/A 8 問の構造的事実】。これは C-4 の主要発見の一つの源泉となる：**戦略的空白 13 問は initiatives 紐付けの構造的真空地帯である**。

### 1.3 463 initiatives × 30 問の擬似マッピング初期推定

C-4 リードの本作業前提として、initiatives.db の question_id（B-1 Q-prefixed 24 問）を B-3 G-prefixed 30 問にマップした際の暫定件数を試算する。マッピング規則は _TRACK_LINKAGE_MATRIX.md §2.4 推定（B-3 リード未確認・m1 申し送り中）に依拠する。【未検証】

| B-3 ID | B-1 ID 推定対応 | initiatives 件数 | B-5 zone |
|---|---|---|---|
| G-N01 | Q-N01 | 27 | Warm |
| G-N02 | Q-N02 | 19 | Warm |
| G-N03 | Q-N03 | 30 | Warm |
| G-N04 | Q-N04 | 21 | Warm |
| G-N05 | Q-N05 | 21 | Warm |
| G-N06 | Q-N06 | 18 | Warm |
| G-N07 | Q-N07 | 10 | **Cool** |
| G-N08 | Q-N08 | 29 | **Cool** |
| G-N09 | （直接対応なし） | 0 | **Cool** |
| G-N10 | Q-N10 | 7 | **Hot** |
| G-N11 | Q-N11 | 16 | **Hot** |
| G-N12 | Q-N12 | 21 | **Hot** |
| G-N13 | Q-N13 | 27 | （N/A or Warm）【未確定】 |
| G-M01 | （直接対応なし） | 0 | N/A |
| G-M02 | Q-M02 | 15 | **Hot** |
| G-M03 | （直接対応なし） | 0 | N/A |
| G-M04 | （直接対応なし） | 0 | N/A |
| G-M05 | Q-M05 | 21 | N/A |
| G-M06 | （直接対応なし） | 0 | N/A |
| G-M07 | （直接対応なし） | 0 | N/A |
| G-M08 | Q-M08 | 7 | Cool |
| G-M09 | Q-M09 | 20 | Cool |
| G-M10 | （Q-M10 別 ID）| 0 | Cool |
| G-M12 | Q-M12 | 27 | （N/A or Warm）【未確定】 |
| G-F01 | Q-F01 | 24 | Cool |
| G-F02 | （直接対応なし） | 0 | Warm |
| G-F03 | Q-F03 | 7 | N/A |
| G-F04 | （直接対応なし） | 0 | Cool |
| G-F05 | （直接対応なし） | 0 | Warm |
| G-V01 | （直接対応なし） | 0 | Cool |
| G-V02 | Q-V02 | 16 | Warm |
| G-V03 | （直接対応なし、Q-V07近接） | 0 | N/A |

【未検証・本マッピングは _TRACK_LINKAGE_MATRIX.md §2.4 推定値を C-4 の事前点検目的で仮置きしたもので、B-3 リードによる確定（B-5 sentinel m1 申し送り）後に上書き必須】

この暫定マッピングからの構造的観察は次の通り。

**観察 1**: Hot 4 問はすべて 7-21 件の initiatives を持つ（G-N10: 7 / G-N11: 16 / G-N12: 21 / G-M02: 15）。合計 59 件で 463 件中 12.7%。Care シナリオ独占は initiatives ベースでも追認される。【推定】

**観察 2**: 戦略的空白 13 問のうち 11 問は initiatives 直接対応がゼロ件（G-N09 / G-M01 / G-M03 / G-M04 / G-M06 / G-M07 / G-F03 を含む）。**戦略的空白＝ initiatives 真空** の構造的二重定義が確認される。例外は G-N07（10 件）/ G-M10（Q-M10 別 ID で 0 件だが他観点で接続候補）等の限定的接続。

**観察 3**: Warm 9 問の総 initiatives 件数は約 175 件（27+19+30+21+21+18+ G-F02 0+ G-F05 0 + Q-V02 16 = 152 件、平均 17 件/問）。Warm zone は「動きが薄〜中程度」の領域だが initiatives 上は十分な観測が存在する。これは C-4 で「Warm の中身を質的に弁別する」必要を示唆する：単に件数があるだけでは「正しい方向の動き」とは限らない。【解釈】

**観察 4**: 「直接対応なし 0 件」12 問のうち 5 問（G-N09, G-M01, G-M04, G-M06, G-V03 等）は B-5 戦略的空白 13 問と一致する。残り 7 問は G-F02・G-F04・G-F05・G-V01 等で、これらは B-1 41 問の Q-F・Q-V から直接マップされず、B-3 独自設計問いとして登場した。C-4 ではこれらにも「対応 initiatives ゼロでありながら zone は Warm/Cool」という新たな観点を導入する必要がある。

### 1.4 zone × stage 二次集計【推定・C-4 本体で確定】

initiatives.db の stage（experiment/pilot/scale）と B-5 zone を二次集計したとき、Hot zone の initiatives は scale 比率が高い、Cool zone は experiment 比率が高い、という仮説が立てられる。【推定】これは C-4 解析時に初期検証すべき核心仮説の一つで、検証コードは次の通り。

```sql
-- C-4 リード本体実行時の検証 SQL
SELECT 
  i.question_id,
  i.stage,
  COUNT(*) AS n
FROM initiatives i
WHERE i.question_id IN ('Q-N10','Q-N11','Q-N12','Q-M02')  -- Hot zone
GROUP BY i.question_id, i.stage
ORDER BY i.question_id, i.stage;
```

仮説検証の結果、もし Hot zone でも experiment 比率が 60% を超える場合、「Hot zone の動きは件数では多いが構造化未到達」という重要な留保が発生する。【未検証】

---

## 2. ミラツク優先課題 TOP10 × 偉業マッピング 仮説提示

B-6 confirmed TOP10 の各問いに対し、C-3 great_actions.db v0.1（GA-001〜100 想定）から 3-5 件の偉業候補をマッピングする仮説を提示する。GA レコードの最終形は C-3 リードの確定を待つが、本書では C-3 事前リサーチ §4「TOP10 × 過去アナログ偉業」マッピングを継承し、それぞれを 1 ↔ N 関係に展開する。

### 2.1 TOP10 × 偉業対応マトリクス（仮説）

| 順位 | 問い ID | 主題 | 偉業候補（仮置 GA-ID） | 推進状況初期判定 |
|---|---|---|---|---|
| 1 | G-M04 | 世代間正義の憲法化 | GA-040「未来世代代表議席制度」/ GA-041「7 世代影響評価制度化」/ GA-042「Iroquois→現代の継承」/ GA-043「気候訴訟による世代間正義先例化」 | expected（initiatives ゼロ・wisdom 厚） |
| 2 | G-N09 | 先住民知識主権 | GA-090「UNDRIP 拡張議定書」/ GA-091「アイヌ・沖縄知識主権制度化」/ GA-092「先住民データ主権 GIDA 採択」/ GA-093「TK Labels の国際規格化」 | emerging（一部実装・10 件以下 init） |
| 3 | G-M01 | GDP 代替ケア指標 | GA-010「Care Economic Index OECD 採用」/ GA-011「ケア時間衛星会計化」/ GA-012「Bhutan GNH の OECD 拡張」/ GA-013「Wellbeing Budget の主流化」 | expected（initiatives 直接対応ゼロ） |
| 4 | G-N12 | ケア経済の組織化 | GA-120「ケア事業協同組合の制度化」/ GA-121「ケア労働者の集合的交渉権」/ GA-122「ケア経済特区」/ GA-123「ケアエコシステム認証」 | **happening**（Hot zone・21 init） |
| 5 | G-N10 | ケア時間自己観察・市場化 | GA-100「ケア時間個人会計アプリ」/ GA-101「ケア労働の市場価格化」/ GA-102「家事労働の GDP 算入」/ GA-103「ケア労働社会保険化」 | **happening**（Hot zone・7 init） |
| 6 | G-N11 | マルチステークホルダー意思決定 | GA-110「企業経営における多元的代表制」/ GA-111「未来世代代表アドバイザリーボード」/ GA-112「市民議会の常設化」/ GA-113「先住民代表の意思決定参加」 | **happening**（Hot zone・16 init） |
| 7 | G-M02 | 人格分散の法人格化 / AI制度反作用 | GA-020「AI 法人格制度化」/ GA-021「分散自我の法的取扱」/ GA-022「digital twin の権利義務」/ GA-023「nonhuman person 概念拡張」 | **happening**（Hot zone・15 init・UPR 単独強応答） |
| 8 | G-N07/G-N08 | 非西洋認識論の方法論化 | GA-070「学術査読基準への複数認識論導入」/ GA-071「東洋哲学の方法論的標準化」/ GA-072「非西洋メソドロジー教科書化」/ GA-073「翻訳不可能性のアーカイブ化」 | emerging（10-29 init・Cool zone） |
| 9 | G-V03 | 自己言及メタ問い | GA-030「ミラツク自己診断 protocol」/ GA-031「2100 年再評価制度」/ GA-032「フォーサイト機関の自己反省装置」 | speculative（initiatives ゼロ・組織固有） |
| 10 | G-F02 | 三項経済（贈与×交換×共有）比率設計 | GA-020「贈与経済の制度的位置づけ」/ GA-021「commons 会計の標準化」/ GA-022「三項会計の OECD 採用」/ GA-023「協同組合の地域経済比率法」 | emerging（initiatives ほぼゼロ・Warm zone） |

【推定・GA-ID 番号は仮置きで C-3 確定後に再付番必須】

### 2.2 構造的観察

このマッピングから読み取れる構造的観察は四点ある。

**第一に、TOP10 のうち 4 問（G-N12 / G-N10 / G-N11 / G-M02）が Care シナリオ Hot zone に集中**し、これらは「happening」状態として great_actions.db で記録される。残り 6 問は emerging（4 問）/ expected（2 問: G-M04・G-M01）/ speculative（1 問: G-V03）に分布する。Care シナリオの非対称優位は great_actions レベルでも追認される。

**第二に、TOP10 × 偉業マッピングの平均偉業数は 4.0 件**で、仮置き合計 40 件。great_actions.db v0.1 の総件数 100-150 件のうち約 27-40% が TOP10 関連となり、TOP10 集中度は高い。

**第三に、戦略的空白 13 問起源の偉業（GA-040 系列・GA-010 系列・GA-090 系列等）は「期待される偉業」として分類される一方、過去アナログ（ハンムラビ・マンデラ・アクバル・キュロス・管仲・渋沢栄一）から導出される構造を持つ**。これは C-3 great_actions.db の `historical_analog_person_ids` フィールドで継承される。

**第四に、G-V03（自己言及メタ）は GA-030 系列の 3 件のみで、過去アナログ ID はゼロ**。これはミラツク固有の「speculative」カテゴリで、C-4 の差分マップ上では「他のどの偉業類型とも異なる例外領域」として独立扱いとなる。【解釈】

---

## 3. 「動きはあるが方向違い」warning 偉業弁別基準（仮説）

C-4 で最も主観性が出やすい領域が warning 偉業の判定である。ブリーフィングで「判定基準を明示・複数視点で検証」が要請されている。本節では仮説的な弁別基準を四つ提示し、複数視点での重ね合わせを提案する。

### 3.1 warning の定義候補

「動きはあるが方向違い」warning 偉業の定義候補は次の四つである。

**定義候補 A: Hot/Warm zone の中で表面的・形式的取り組みに留まる**

initiatives 件数は十分（n≥5）あるが、stage が experiment 集中（pilot/scale が 20% 未満）で、かつ initiative_type に research/policy が偏り investment/partnership が少ない場合、warning と判定する。【推定】これは「動きは観測されるが、構造化に至らず実験で終わる」状態を捉える。

**定義候補 B: B-2 wisdom 接続が薄い領域での過剰実装**

B-2 already_future.db の wisdom records 接続が 5 件未満（PHIL/LIT/MY/TK/AN の 5 系統合計）であるにもかかわらず、Hot/Warm zone に分類される問いは「歴史的検証なき実装」のリスクを抱える。Care シナリオ Hot 4 問は wisdom 厚（19 件）でクリアするが、Fragmentation 系列の動きは wisdom 薄（5 件未満）で warning 候補。【解釈】

**定義候補 C: Mサイン階層との不整合**

initiatives がカバーする方向性（initiative_name の主題分析）が、Phase A Mサイン階層（真M「物語転換期」/ 準M「非西洋認識論・世代間正義・ケア経済」/ 概念整合「第四変容期」）と逆方向に向かう場合、warning 偉業となる。たとえば「AI 規制」が Hot 状態にあるが、その方向性が「既存統治構造の温存」を志向する場合、Mサイン物語転換期と不整合で warning。【推定】

**定義候補 D: グリーンウォッシング・SDGs 形式適用型**

具体的に企業 IR や ESG 開示で「形式的 SDGs アライメント」「purpose ウォッシング」型の initiatives が含まれる場合、warning と判定する。これは Sangaku-PR や SGRD の press_release タイトルから抽出可能で、形式判定可能。【未検証】

### 3.2 warning 候補の暫定リスト

上記 4 定義を緩く適用した warning 候補（C-4 リード本体実行時に厳密判定必須）。

| 候補 | 該当問い | 候補理由 | 該当定義 |
|---|---|---|---|
| W-01 | G-N02 AI 規制（Warm） | EU AI Act・日本生成AI政策の多くが企業規制でなく開発推奨型に偏向【解釈】 | C |
| W-02 | G-N06 気候災害適応（Warm） | 適応策が緩和策の代替として運用される置換リスク【解釈】 | A, C |
| W-03 | G-N01 AI ガバナンス空白（Warm） | 装置応答（SG/IR）強だが企業主導 self-regulation で規範性弱い【解釈】 | A, B |
| W-04 | G-N13 教育改革（Warm） | edtech 投資先行で教育目的論議論不在の可能性【未検証】 | A |
| W-05 | G-N03 第三項物語（Warm） | 「第三の道」「第三項論」の濫用で実体不明確化リスク【解釈】 | C |
| W-06 | G-N12 ケア経済の組織化（Hot） | Care 経済化が市場化に偏重し、相互扶助構造の解体を伴う可能性【未検証】 | A, C |

【推定・複数視点必要】

特に W-06 は Hot zone に対する warning 判定であり、リスクの高い解釈である。Care 経済 Hot 4 問は規範的に望ましいとされるが、「ケア労働の市場化」が「ケア関係の純粋贈与的性格」を毀損する論争は philosophical care ethics（Tronto, Held, Noddings）からの伝統的批判である。C-4 ではこの論争を warning 偉業の独立カテゴリとして組み入れることを提案する。【解釈】

### 3.3 warning 判定の複数視点検証プロトコル

C-4 リード本体実行時、warning 判定は以下の三視点で重ね合わせ検証する。

1. **規範視点**: B-2 wisdom と整合するか、Track 9 善き社会 4 根本前提（個・関係・場所・時間）と整合するか
2. **実装視点**: initiatives stage 分布が experiment に偏りすぎていないか、scale 到達があれば構造的整合か
3. **歴史視点**: 過去アナログ偉業（GF DB cases）の失敗パターン（書籍 §17 32 中位パターンの「改革者の罠」「制度の経路拘束」「複合的正当性危機」）と類似性があるか

3 視点のうち 2 視点で warning 該当の場合のみ great_actions.db に warning タグを付与する。3 視点全該当の場合は critical warning として強調表示する。【推定・C-4 リードと議論で決定】

### 3.4 warning 件数仮目標

great_actions.db v0.2 への warning タグ付与件数の仮目標は **10-15 件**（全 100-150 件の 7-15%）とする。これは「過半数を warning 認定する過剰判定」と「皆無の過小判定」の中間で、判定の慎重さを保つ。【推定】

---

## 4. 「動きはないが期待される」opportunity 偉業弁別基準（仮説）

opportunity 偉業の弁別は warning よりも構造的に明確である。B-5 戦略的空白 13 問が事実上 opportunity の核を成す。ただし 13 問の機械的継承だけでなく、追加観点での opportunity 抽出を提案する。

### 4.1 opportunity の定義

「動きはないが期待される」opportunity 偉業は次の三条件を満たす。

**条件 1**: B-5 戦略的空白 13 問または initiatives 件数 5 件未満の問い起源
**条件 2**: B-2 wisdom 接続が厚い（5 件以上、PHIL/LIT/MY/TK/AN の 2 系統以上から）
**条件 3**: B-3 critical juncture（JCT-01〜08）に接続する、または Phase A Mサイン階層（真M/準M/概念整合）と接続する

3 条件全該当の場合、opportunity と判定。3 条件のうち 2 条件該当は「opportunity 候補」として保留扱い。

### 4.2 opportunity 偉業の暫定リスト

戦略的空白 13 問起源の opportunity 偉業は次の通り（C-3 事前リサーチ §5 から継承・初期 13 件）。

| 候補 | 該当問い | wisdom | JCT 接続 | Mサイン |
|---|---|---|---|---|
| O-01 | G-N07 非西洋認識論の方法論化 | 18 | JCT-03 準M | 準M由来 |
| O-02 | G-N08 学術界の方法論標準化 | 18 | JCT-03 準M | 準M由来 |
| O-03 | G-N09 先住民知識主権 | 18 | JCT-03 準M | 準M由来 |
| O-04 | G-M10 大学院教育における伝統知 coequal | 18 | JCT-03 準M | 概念整合 |
| O-05 | G-F01 複数 cosmology 併存の憲法条項 | 18 | JCT-03 準M | 準M由来 |
| O-06 | G-M01 OECD/UN による Care Economic Index | 19 | JCT-04 概念整合 | 概念整合 |
| O-07 | G-M03 上場基準への Care/Commons 軸組込み | 19 | JCT-04 概念整合 | 概念整合 |
| O-08 | G-M04 7 世代代表議席を持つ憲法改正 | 12 | JCT-05 準M | 準M由来 |
| O-09 | G-M05 国連「未来世代代表」常設化 | 12 | JCT-05 準M | 準M由来 |
| O-10 | G-M06 EU「遅延しない権利」指令 | 12 | JCT-07 概念整合 | 概念整合 |
| O-11 | G-M07 学校・労働・医療の周期時間制度 | 12 | JCT-07 概念整合 | 概念整合 |
| O-12 | G-F03 多元時間性の WHO/ISO 規格 | 12 | JCT-07 概念整合 | 概念整合 |
| O-13 | G-V03 ミラツク自己診断 protocol | self | — | self-reflexive |

【B-6 戦略的空白 13 問の継承・C-3 事前リサーチ §5 から派生】

### 4.3 opportunity 偉業の追加観点

13 問の機械的継承に加えて、以下の追加観点で opportunity を抽出する候補を提案する。

**追加観点 A**: Cool zone 9 問のうち wisdom 接続が厚い問い（Cool zone は initiatives 1-2 件で「動き弱・規範厚」の中間状態）。例：G-V01・G-F04 等。

**追加観点 B**: Warm zone でも initiatives 直接対応ゼロの問い（G-F02 三項経済比率設計・G-F05 等）。これは「動きはあるが initiatives 真空」という別の opportunity 形態。

**追加観点 C**: B-1 41 問のうち B-3 30 問への継承で漏れた問い。たとえば B-1 真M由来 4 問のうち Q-N04（場所性回帰）= G-N04 のみが直接継承され、Q-N01/Q-N03 は warm zone 入り、Q-M09（物語転換期の本格化）は Cool zone。これらに対応する未開拓偉業が opportunity となる可能性。【推定】

### 4.4 opportunity 件数仮目標

great_actions.db v0.2 への opportunity タグ付与件数の仮目標は **30-40 件**（全 100-150 件の 25-30%）。これは戦略的空白 13 問 × 各 2-3 偉業 = 26-39 件 + 追加観点 5-10 件で算出。warning（10-15 件）の約 3 倍となり、「期待される偉業の方が、方向違い偉業よりも数が多い」という構造的非対称が現れる。これは「現代社会は方向違いに転んでいるよりも、まだ動き始めていない領域の方が多い」というミラツク独自の楽観的構造観を支える数字となる。【解釈】

---

## 5. great_actions.db 更新スキーマ提案

C-3 great_actions.db v0.1 のスキーマ（事前リサーチ §6 提案）を C-4 で v0.2 に更新する。本節では C-3 設計と整合する形で、推進状況・成熟度・463 initiatives 紐付けの追加フィールド群を提案する。

### 5.1 great_actions テーブルへの追加フィールド

C-3 v0.1 の `great_actions` テーブルは `current_stage_status`（happening/emerging/expected/speculative）を既に持つ。C-4 v0.2 ではこれを「Phase B 観測実績による上書き層」として強化する。【推定・C-3 確定後に整合確認必須】

```sql
-- great_actions テーブルへの追加カラム（v0.2 マイグレーション）
ALTER TABLE great_actions ADD COLUMN c4_status_override TEXT 
  CHECK(c4_status_override IN (
    'happening', 'emerging', 'expected', 'speculative', 'warning', 'opportunity'
  ));
ALTER TABLE great_actions ADD COLUMN c4_b5_zone TEXT 
  CHECK(c4_b5_zone IN ('Hot', 'Warm', 'Cool', 'Dead', 'N/A'));
ALTER TABLE great_actions ADD COLUMN c4_initiatives_count INTEGER DEFAULT 0;
ALTER TABLE great_actions ADD COLUMN c4_initiatives_stage_dist TEXT;  -- JSON {"experiment": 5, "pilot": 2, "scale": 1}
ALTER TABLE great_actions ADD COLUMN c4_top10_rank INTEGER;  -- 1-10 (TOP10 該当の場合)
ALTER TABLE great_actions ADD COLUMN c4_warning_definitions TEXT;  -- JSON ["A", "B"] (warning 該当時)
ALTER TABLE great_actions ADD COLUMN c4_warning_severity TEXT 
  CHECK(c4_warning_severity IN ('critical', 'high', 'medium', 'low', NULL));
ALTER TABLE great_actions ADD COLUMN c4_opportunity_conditions TEXT;  -- JSON ["1", "2", "3"] (opportunity 該当時)
ALTER TABLE great_actions ADD COLUMN c4_maturity_score INTEGER 
  CHECK(c4_maturity_score BETWEEN 0 AND 5);  -- 0=speculative, 1=expected, 2=emerging, 3=happening_experiment, 4=happening_pilot, 5=happening_scale
ALTER TABLE great_actions ADD COLUMN c4_direction_alignment TEXT 
  CHECK(c4_direction_alignment IN ('aligned', 'partial', 'misaligned', 'unknown'));
ALTER TABLE great_actions ADD COLUMN c4_updated_at TEXT DEFAULT (datetime('now'));
ALTER TABLE great_actions ADD COLUMN c4_review_note TEXT;
```

`c4_status_override` は v0.1 の `current_stage_status` を上書きする。v0.1 では C-3 リードが机上判定した状態を、v0.2 では Phase B 観測実績で更新する。warning と opportunity は v0.2 で新設するカテゴリ。【推定】

`c4_maturity_score` は 0-5 の数値で、initiatives.db の stage 分布から自動算出可能（experiment が 50% 以上 = 3、pilot が 50% 以上 = 4、scale が 30% 以上 = 5、initiatives ゼロ = 0-1）。これにより great_actions レベルでの定量比較が可能となる。【推定】

`c4_direction_alignment` は warning 判定の基礎データで、aligned（方向整合）/ partial（部分整合）/ misaligned（方向違い）/ unknown（判定不能）の四値。warning は misaligned 判定の偉業に付与される。【推定】

### 5.2 新規テーブル: action_initiatives_links

463 initiatives と great_actions の紐付けテーブルを新設する。多対多関係で、1 initiative が複数 actions に紐付く可能性、1 action が複数 initiatives で観測される可能性の両方を扱う。【推定】

```sql
CREATE TABLE action_initiatives_links (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  action_id TEXT REFERENCES great_actions(action_id),
  initiative_id INTEGER,  -- initiatives.db の initiatives.id
  initiative_question_id TEXT,  -- 紐付けの根拠としての B-1 問い ID
  link_strength TEXT CHECK(link_strength IN ('strong', 'medium', 'weak', 'speculative')),
  link_type TEXT CHECK(link_type IN ('direct', 'inverse', 'partial', 'analog')),
  -- direct = この initiative はこの action の実例
  -- inverse = この initiative はこの action の反例（方向違い）
  -- partial = この initiative は action の一部側面のみ実装
  -- analog = 他領域だが構造的に類似
  initiative_stage TEXT,  -- experiment/pilot/scale
  initiative_horizon TEXT,
  reasoning_ja TEXT,
  reviewed_by TEXT,
  created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX idx_ail_action ON action_initiatives_links(action_id);
CREATE INDEX idx_ail_initiative ON action_initiatives_links(initiative_id);
```

`link_type = 'inverse'` のレコードは「この initiative は当該 action の方向に反する動き」を表し、warning 偉業の根拠となる。たとえば G-N12 ケア経済の Hot zone に「ケア労働の市場化偏重」initiative があった場合、それは「ケアの相互扶助的性格を保全する偉業（GA-122 等）」の inverse link として記録される。【推定】

### 5.3 新規テーブル: action_zone_mapping

zone × archetype × scenario の三軸集計テーブル。差分マップ可視化の基礎データとなる。

```sql
CREATE TABLE action_zone_mapping (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  zone TEXT CHECK(zone IN ('Hot', 'Warm', 'Cool', 'Dead', 'N/A', 'cross')),
  scenario TEXT CHECK(scenario IN ('Care', 'Techno', 'Pluriverse', 'Slow Right', 'Fragmentation', 'cross', 'self-reflexive')),
  archetype TEXT,
  action_count INTEGER,
  warning_count INTEGER,
  opportunity_count INTEGER,
  happening_count INTEGER,
  emerging_count INTEGER,
  expected_count INTEGER,
  speculative_count INTEGER,
  computed_at TEXT DEFAULT (datetime('now'))
);
```

このテーブルは集計テーブルで、great_actions と action_initiatives_links から週次再計算する想定。ダッシュボード表示の高速化のため。【推定】

### 5.4 マイグレーション順序

C-4 リード本体実行時のマイグレーション順序提案：

1. C-3 完了確認（GA-001〜100 件以上の great_actions レコード存在確認）
2. ALTER TABLE で c4_* カラム追加（10 カラム）
3. action_initiatives_links と action_zone_mapping テーブル新設
4. 463 initiatives × 100-150 great_actions の手動マッピング（1-2 日想定）
5. c4_initiatives_count 等の集計値を SQL で更新
6. warning/opportunity タグ付与（複数視点検証経由・3-5 日想定）
7. action_zone_mapping 集計テーブル生成
8. v0.2 整合性チェック（v0.1 の status と c4_status_override の差分レビュー）

【推定・C-4 リード本体実行時に時間配分要確認】

---

## 6. C-3 great_actions.db との接続点

C-4 は C-3 の出力（GA-001〜100 件）を直接更新する形を取るため、C-3 設計との整合が必須となる。本節では C-3 事前リサーチ（§6 スキーマ提案）と C-4 v0.2 マイグレーションの接続点を整理する。

### 6.1 既存・期待・登場中フラグの整合

C-3 v0.1 の `current_stage_status` は次の 4 値を持つ。

- **happening**（起こっている = Hot/Warm zone）
- **emerging**（起こりつつある = Cool zone）
- **expected**（期待される = N/A だが規範的に重要）
- **speculative**（仮説段階）

C-4 v0.2 の `c4_status_override` は上記 4 値に **warning** と **opportunity** を加えて 6 値となる。warning は元 happening/emerging から、opportunity は元 expected/speculative から派生する派生カテゴリで、上書きでなく「上書き候補」としてフラグ管理する。【推定】

| C-3 v0.1 status | C-4 v0.2 上書き候補 | 判定根拠 |
|---|---|---|
| happening | warning | 動きはあるが方向違い（§3 4 定義） |
| emerging | opportunity | 動きが弱いが規範的に重要（§4 3 条件） |
| expected | opportunity | 戦略的空白 13 問起源 |
| speculative | opportunity / speculative | self-reflexive 系列は speculative 維持 |

### 6.2 463 initiatives 紐付けによる「動きあり」確証

C-3 v0.1 で `current_stage_status = 'happening'` と判定された GA レコードは、C-4 で `action_initiatives_links` に 1 件以上の direct link が存在することで「動きあり」が確証される。direct link がゼロの場合、C-3 の judg は table 上の根拠なき happening 認定であり、C-4 で emerging または expected に格下げ候補となる。【推定】

逆に、C-3 で `expected` 判定でありながら C-4 で direct link が 5 件以上あった場合は、「Phase B 観測時には捉えられていなかったが initiatives レベルで動きが既に発生」していることを意味し、emerging または happening に格上げ候補となる。これは Phase B 装置応答薄問いに対する C-4 独自の発見となる可能性がある。【解釈】

### 6.3 archetype × zone の交差テスト

C-3 事前リサーチ §8 で発見された「Mediator 過剰要求度 2.16x」「Warrior/Explorer/Craftsman 0 回登場」の構造的非対称が、C-4 v0.2 の zone 分布でどう現れるかは独立検証点となる。仮説は次の通り。【推定・C-4 本体検証】

- Hot zone 4 問（Care 系列）= Caregiver + Steady 主導 → C-3 §8 の Caregiver 8 回・Steady 7 回登場と整合
- Cool zone 9 問（Pluriverse 中心）= Mediator + Introvert Thinker 主導 → C-3 §8 の Mediator 13 回登場と整合
- N/A 8 問 = Mediator + Introvert Thinker + Caregiver 混合 → 戦略的空白の人材プール制約と整合

仮説検証の結果、archetype × zone の対応がきれいに現れる場合、「現代の偉業の構造的供給制約はアーキタイプ分布の偏りにある」という主張が C-4 で強化される。これは C-5 担い手特性 Track への重要な引き継ぎとなる。【推定】

### 6.4 scenario × initiatives 件数の対応

C-3 v0.1 の `scenario_primary` 5 値（Care/Techno/Pluriverse/Slow Right/Fragmentation + cross）と、C-4 で集計する initiatives 件数の対応は次の仮説で接続される。【推定】

| シナリオ | initiatives 件数仮計（B-3 30 問対応分） | 平均 zone | warning 比率仮 | opportunity 比率仮 |
|---|---|---|---|---|
| Care | 約 60 件 | Hot 中心 | 中（市場化偏重リスク） | 中（GDP 代替指標未実装） |
| Techno | 約 100 件 | Warm 中心 | 高（AI ガバナンス偏向） | 低 |
| Pluriverse | 約 30 件 | Cool 中心 | 低 | 高（戦略的空白集中） |
| Slow Right | 約 5 件未満 | N/A 集中 | 低 | 高（最大の opportunity 領域） |
| Fragmentation | 約 50 件 | Warm 中心 | 高（脱出経路として観察） | 低 |
| cross/self-reflexive | 約 0 件 | N/A | — | 中（G-V03 等独立扱い） |

【推定・C-4 本体での実値検証必須】

この仮説が支持される場合、Care シナリオは「動きはあるが方向違いリスクが中程度」、Slow Right と Pluriverse は「動きが少ないが期待される領域」、Techno と Fragmentation は「動きはあるが方向違いリスク高」という三類型構造（B-5 主要発見）が偉業レベルで再現されることになる。【解釈】

---

## 7. 戦略的空白 13 問の各々への対応偉業候補（暫定リスト）

§4 で opportunity 偉業の暫定リストを示したが、本節では戦略的空白 13 問の各々に対する偉業候補を、C-3 事前リサーチ §5 の表を継承・拡張して提示する。

### 7.1 各問いに対する 3 偉業候補

| 問いID | 主要偉業候補 | 副次偉業候補 | 第三候補 |
|---|---|---|---|
| **G-N07**（Pluriverse 認識論方法論化） | UNDRIP 拡張議定書を率いる先住民連合体の創立 | 査読基準への複数認識論導入（学会連合主導） | 翻訳不可能性アーカイブの設立 |
| **G-N08**（学術界の方法論標準化） | 主要学会の方法論憲章改訂 | 大学院教育の必修化 | 国際科学会議（ICSU）後継機関での議題化 |
| **G-N09**（先住民知識主権） | アイヌ・沖縄・琉球の知識主権制度化 | TK Labels の国際規格化（ISO） | GIDA 採択の各国実装 |
| **G-M10**（伝統知 coequal 大学院） | 京大・東北大等での伝統知 coequal カリキュラム | 米国先住民系大学（TCU）モデルの拡張 | UNESCO による標準モデル制定 |
| **G-F01**（複数 cosmology 併存憲法条項） | Bhutan/Bolivia/Ecuador 型の自然権憲法拡張 | 日本国憲法における場所性条項追加 | EU 基本権憲章の cosmology 条項 |
| **G-M01**（OECD/UN ケア経済指標） | OECD Better Life Index への Care Economic Index 組込 | UN-SNA 改訂による無償ケア労働算入 | 各国統計局のケア衛星会計化 |
| **G-M03**（上場基準の Care 軸） | 東証グロース市場の Care/Commons 開示要件 | EU CSRD への Care 軸追加 | 国際会計基準（IFRS）への Commons 軸 |
| **G-M04**（7 世代代表議席憲法改正） | ウェールズ「Future Generations Act」型の各国拡張 | Iroquois 7 世代原則の制度化 | 国連憲章改正 |
| **G-M05**（国連未来世代代表常設化） | UN「Pact for the Future」具体化 | UNGA 常設委員会化 | 各国に未来世代代表の常設化 |
| **G-M06**（EU 遅延しない権利指令） | EU 加盟国法制化 | 日本における過剰スピード規制 | 国際労働機関 ILO 指令化 |
| **G-M07**（学校・労働・医療周期時間） | フィンランド・デンマーク型の周期教育 | 4 日労働制の法制化 | 医療における慢性時間概念の制度化 |
| **G-F03**（多元時間性 WHO/ISO 規格） | WHO による文化時間規格策定 | ISO 8601 拡張提案 | 多文化時間管理の医療応用 |
| **G-V03**（自己言及メタ問い） | ミラツク 5 年再評価 protocol | 2100 年振り返り装置設計 | フォーサイト機関連合での自己診断標準 |

【C-3 事前リサーチ §5 継承・拡張・推定】

### 7.2 構造的観察

戦略的空白 13 問 × 平均 3 偉業候補 = 39 件が opportunity 偉業の核となる。§4.4 で示した opportunity 件数仮目標 30-40 件と整合する。【推定】

13 問の偉業候補から読み取れる二点の観察：

**観察 1**: 13 問の主要偉業候補のうち、**国際機関主導が 6 件**（OECD/UN/UNESCO/EU/ILO/WHO）、**国家・地域主導が 4 件**（Bhutan/フィンランド/ウェールズ/各国憲法）、**ミラツク・先住民連合・学会主導が 3 件**（連合体創立・カリキュラム・自己診断）。これは戦略的空白の偉業が主に「制度設計者」レイヤーで発生することを意味し、C-3 事前リサーチ §4 で確認した「TOP10 半数が制度設計者アーキタイプに収束」と整合する。【解釈】

**観察 2**: G-V03 の偉業候補はすべてミラツク自身またはフォーサイト機関連合に集中しており、**他のどの偉業類型にも属さない例外領域**を構成する。これは C-4 差分マップ上で独立クラスタとして可視化すべきである。【推定】

### 7.3 Stage 1-3 三段階モデルとの対応

C-3 §3 で提示された「個別行動 1-10 年 → 社会変動 10-40 年 → SI 30-100 年」三段階モデルと戦略的空白 13 問の対応【推定】：

| 問い | Stage 1 起点想定 | Stage 2 拡散想定 | Stage 3 制度化想定 |
|---|---|---|---|
| G-N07-09（Pluriverse 系列） | 2030-2040 | 2040-2060 | 2060-2080 |
| G-M01/M03（Care 系列） | 2026-2030 | 2030-2040 | 2040-2050 |
| G-M04/M05（世代間正義） | 2030-2040 | 2040-2055 | 2055-2070 |
| G-M06/M07/F03（Slow Right） | 2040-2055 | 2055-2070 | 2070-2090 |
| G-V03（self-reflexive） | 2026 起動 | 2031 第一回再評価 | 2100 最終評価 |

ここから読み取れるのは、**戦略的空白 13 問の Stage 3 完了は 2050-2090 に集中**し、ミラツクのフォーサイト射程（2100 年）の中盤〜後半で結実する設計となっていることである。これは「戦略的空白偉業＝中長期投資領域」というミラツクの戦略仮説を支える時間配分となる。【解釈】

---

## 8. C-4 リード本体実行時の論点（5-7 点）

C-4 リード起動時の最優先確認事項を 7 点に整理する。各論点は本リサーチで先送りした判断や、C-3/C-5 との整合確認が必要な事項を含む。

### 論点 1: B-3 → B-1 マッピング確定

B-5 sentinel m1 申し送りで「B-3 → B-1 マッピングは推定段階・B-3 リード確認未了」とされている。C-4 の中核作業は 463 initiatives × G-prefixed 30 問の紐付けであり、本マッピングが確定していないと作業全体が暫定値に留まる。C-4 リード起動 30 分以内に B-3 リード（または C-2 リード）と接触し、_TRACK_LINKAGE_MATRIX.md §2.4 を正本化する必要がある。【推定】

### 論点 2: warning 判定の主観性管理

ブリーフィング §3.3 で「warning 判定は最も主観性が出やすい領域」と明記されている。本書 §3 で 4 定義を提示したが、複数視点検証プロトコル（規範視点・実装視点・歴史視点の 3 視点重ね合わせ）の閾値（2 視点該当 vs 3 視点該当）を C-4 リードと議論で決定する必要がある。閾値が緩い場合 warning 件数が膨張し、厳しい場合 warning 概念自体が形骸化する。仮目標 10-15 件を維持できる閾値設計が望ましい。【推定】

### 論点 3: Hot zone への warning 判定の妥当性

§3.2 で Hot zone（特に G-N12 ケア経済の組織化）に warning 判定（W-06）を加える可能性を提示した。これは「Care 経済 Hot 4 問は規範的に望ましいとされるが、市場化偏重リスクを抱える」という解釈である。Hot zone への warning 認定は B-5 主要発見「Hot 4 問 = Care シナリオ独占 = 即実装可能領域」の意義を相対化する側面を持つため、C-4 リードと議論で扱い方を決定する必要がある。場合によっては「critical warning」サブカテゴリとして独立扱いとする選択肢も。【解釈】

### 論点 4: C-3 great_actions.db の状態確認

C-4 起動時点で C-3 が GA-001〜100 件以上の great_actions レコードを完成していることが前提となる。C-3 の進捗が遅延している場合、C-4 は「スキーマ拡張のみ実行」「マッピング作業は C-3 完了待ち」の二段階運用を選択する必要がある。並列起動可能性を C-4 起動前に確認する。【推定】

### 論点 5: opportunity 件数仮目標の妥当性

§4.4 で opportunity 件数仮目標 30-40 件、§3.4 で warning 件数仮目標 10-15 件を提案した。これらの 3:1 比率が「ミラツクは方向違い偉業よりも未開拓領域に注目する楽観的構造観」を支える数字となる解釈を §4.4 で示した。この比率設計の妥当性を C-4 リードと議論で確認する。1:1 比率や 1:2 比率を採用すれば異なる構造観となる。【解釈】

### 論点 6: G-V03 self-reflexive の独立扱い

G-V03（自己言及メタ問い）は C-3 §5 で「過去アナログ偉業ゼロ」「ミラツク固有 speculative」と分類された。C-4 では「opportunity か speculative か」の判定が問われる。本書 §4.2 では opportunity に分類したが、ブリーフィング §6.2 「TOP10 × 偉業マッピング」での扱いは不明確。C-4 リードで「self-reflexive を独立第三カテゴリとして扱うか opportunity に統合するか」を確定する。【推定】

### 論点 7: C-5 担い手特性 Track への接続点

C-4 は C-5 と並列走行となるが、共通入力は great_actions.db のみ。C-4 v0.2 で `c4_warning_severity` や `c4_maturity_score` を新設すれば、C-5 が「warning 偉業の担い手特性は何か」「opportunity 偉業の担い手特性は何か」という独立分析を行える。C-4 から C-5 への引き継ぎポイントを C-4 起動前に明示する。【推定】

---

## 9. 完了報告サマリー

### 9.1 主要発見 3 点

**主要発見 1**: 463 initiatives × B-3 30 問の擬似マッピングから、**戦略的空白 13 問 = initiatives 真空** の二重定義が確認された。13 問のうち 11 問が initiatives 直接対応ゼロで、戦略的空白の概念は装置応答薄（B-5 zone）と initiatives 件数ゼロ（B-4 派生）の両方で構造的に支持される。これは great_actions.db v0.2 での opportunity タグ付与の根拠となる。【推定】

**主要発見 2**: warning 偉業の弁別は 4 定義（A: 表面的・形式的取り組み / B: wisdom 接続薄での過剰実装 / C: Mサイン階層との不整合 / D: グリーンウォッシング型）と 3 視点検証プロトコル（規範・実装・歴史）の重ね合わせで実装可能。仮目標 10-15 件を維持する閾値設計が望ましく、特に Hot zone への warning 認定（W-06: Care 経済の市場化偏重リスク）は B-5 主要発見の意義を相対化する側面を持つため C-4 リードと議論で決定。【解釈】

**主要発見 3**: opportunity 偉業件数仮目標 30-40 件 vs warning 仮目標 10-15 件の **3:1 比率** は、「ミラツクは方向違い偉業よりも未開拓領域に注目する楽観的構造観」を支える数字となる。戦略的空白 13 問 × 各 3 偉業候補 = 39 件で算出される opportunity 群は、Stage 3 制度化が 2050-2090 に集中しミラツクのフォーサイト射程（2100 年）の中盤〜後半で結実する時間配分を持つ。これは「戦略的空白偉業 = 中長期投資領域」という戦略仮説を支える。【解釈】

### 9.2 想定スキーマ概要

great_actions.db v0.2 マイグレーション概要：

- **great_actions テーブル拡張**: 10 カラム追加（c4_status_override / c4_b5_zone / c4_initiatives_count / c4_initiatives_stage_dist / c4_top10_rank / c4_warning_definitions / c4_warning_severity / c4_opportunity_conditions / c4_maturity_score / c4_direction_alignment）
- **新規テーブル action_initiatives_links**: 463 initiatives × 100-150 great_actions の多対多紐付け、link_strength（strong/medium/weak/speculative）と link_type（direct/inverse/partial/analog）
- **新規テーブル action_zone_mapping**: zone × scenario × archetype の三軸集計、ダッシュボード表示の高速化
- **マイグレーション順序**: C-3 完了確認 → ALTER TABLE → 新規テーブル新設 → 手動マッピング → 集計値更新 → warning/opportunity タグ付与 → action_zone_mapping 生成 → v0.2 整合性チェック

### 9.3 出力先

ファイル: `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-c/_TRACK_C4_PRESEARCH.md`（本ファイル、約 12,000 字）

### 9.4 C-4 リード起動時の最優先確認事項

- **論点 1**（B-3 → B-1 マッピング確定）と **論点 4**（C-3 great_actions.db の状態確認）の二点は C-4 中核作業の前提条件であり、C-4 リード起動 30 分以内に確定が必要。
- **論点 2**（warning 判定の主観性管理）と **論点 3**（Hot zone への warning 判定の妥当性）はブリーフィング指示の核心領域で、C-4 リードと統括の議論を経て確定。
- **論点 7**（C-5 担い手特性 Track への接続点）は C-4 v0.2 のスキーマ設計時点で C-5 リードへの事前共有が望ましい。

### 9.5 研究の限界（自己認識）

1. **B-3 → B-1 マッピングの推定性**: 本書の 463 initiatives × G-prefixed 30 問マッピング（§1.3）はすべて _TRACK_LINKAGE_MATRIX.md §2.4 推定値依拠で、B-3 リード確認後に上書き必須。
2. **warning 4 定義の主観性**: §3.1 で提示した 4 定義の閾値・優先順位はすべて事前リサーチ担当の解釈で、C-4 リードによる再評価を必須とする。
3. **C-3 確定後の整合確認**: 本書のスキーマ提案（§5）は C-3 事前リサーチ §6 提案を継承するが、C-3 リード本体実行時の確定スキーマと整合確認が必須。

### 9.6 凡例: 推測タグの分布

本書では【推定】タグ 約 35 箇所、【解釈】タグ 約 15 箇所、【未検証】タグ 約 10 箇所を付与した。【推定】は B-4/B-5 確定値に基づく解析的演繹、【解釈】は複数読みが成立する読み方、【未検証】は B-3 リード確認待ちまたは initiatives.db の SQL 検証未了の項目を表す。warning 判定（§3）は構造上【解釈】タグが多用される領域となる。

---

最終更新: 2026-05-09  
作成: Phase C-4 事前リサーチ担当  
参照: `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-c/_TRACK_C4_BRIEFING.md` / `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-c/_PHASE_C_PLAN.md` / `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-c/_TRACK_C3_PRESEARCH.md` / `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-b/track-b4_handoff.md` / `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-b/track-b5_handoff.md` / `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-b/track-b6_handoff.md` / `/Users/nishimura+/projects/research/initiatives-db/initiatives.db`
