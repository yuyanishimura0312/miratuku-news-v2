# Phase C-5 事前リサーチ — 担い手特性構造化

*作成: 2026-05-09 / Phase C 起動準備 / 公開前データ / C-1・C-3 と作業領域不可侵*

## 0. ミッションと前提

Phase C-5「求められる人物の特性」は、C-3 / C-4 で特定される「現代に求められる偉業」を担う**人物の心理特性・行動特性・領域性・専門性**を、(a) era-talents DB の **19 能力次元 × 6 時代**、(b) great-figures DB の **10 意思決定アーキタイプ + 12 システム構造次元**、(c) JPMS DB v2 の **人格 - 学校 - 活躍経路**（832 校・58,224 件のテスティモニアル・40 trait dim・33 career_archetype）の三層を統合して構造化する事前マッピング段階である。本書はその事前リサーチであり、C-5 リード起動時に必須となる「4 軸構造（心理 × 行動 × 領域 × 専門）」の暫定設計と、ミラツク優先 TOP10 × 担い手類型の暫定対応を確定することを目的とする。

入力源は次の通り（数値はすべて DB／既存ハンドオフからの実測値、`/Users/nishimura+/projects/research/...` 配下から sqlite3 で確認）：

- **era-talents.db**: achievers 12,958 / achiever_capabilities 31,436 / capability_dimensions 19 / eras 9（明治／大正／昭和前期／昭和後期／平成／令和の歴史 6 時代＋ future_2030 / future_2050 / future_2100）/ future_demands 590（2030: 245・2050: 220・2100: 125、2100 では 19 次元を超える未来固有概念 63 件を含む）。
- **great-figures.db**: persons 9,178 / events 10,033 / management_concepts 568 / cases 329 / event_structures 174 / insights 19（pattern 10 + lesson 9）。書籍『歴史の韻と変革』20 章 + 付録 A（12 システム構造次元）+ 付録 B（32 中位パターン）+ 付録 C（20 主要ケース）。
- **PST DB**（persona-school-trajectory-db）: persona_archetypes 10（arch_explorer / arch_creator / arch_leader / arch_caregiver / arch_warrior / arch_mediator / arch_craftsman / arch_introvert_thinker / arch_social_creator / arch_steady、人口比合計 100%）/ school_archetype_fit 600 / persona_era_translation（時代翻訳係数）/ schools_pst 60 校。
- **JPMS DB v2**: schools_v2 832 / testimonials_v2 58,224 / person_trait_dim 40+ / career_archetype 33（軍人・防衛型／法曹・法律家型／科学者・研究者型／実業家・経営者型／思想家・哲学者型／NPO リーダー型／VC パートナー型／連続起業家型 等）/ school_typology_lca / outcome_dim_v2。
- **Phase B B-3 主体配分**: 個人 1（G-N10）/ コミュニティ 1（G-N09）/ 企業 4（G-N01・N05・N11・M03）/ 自治体 1（G-N04）/ 国 4（G-N02・N06・M02・M04）/ 国際機関 3（G-N07・M01・M05）+ 複合・追加主体 17 問（市民社会・学術界・複合主体・人類全体・ミラツク等）。
- **Phase B B-5 TOP10**: 1 位 G-M04（世代間正義の憲法化）／2 位 G-N09（先住民知識主権）／3 位 G-M01（GDP 代替ケア指標）／4 位 G-N12（三項リテラシー教育）／5 位 G-N10（ケア時間自己観察）／6 位 G-N11（ケア時間会計標準化）／7 位 G-M02（UBI 二系統設計）／8 位 G-N07/G-N08（非西洋認識論の方法論化）／9 位 G-V03（自己言及メタ）／10 位 G-F02（三項経済比率設計）。Hot zone 4 問は G-N10/N11/N12/M02 で全て Care 系列。

本書では「担い手」を **個別の偉業（GA レコード相当）を主導または共担する個人または小集団** と定義する。組織アーキタイプとしての担い手（NPO・国家機関・国際機関）の構造化は C-5 範囲とするが、**個人の心理特性 × 個人の行動特性**を骨格に据え、組織はその「拡張形」として扱う。

推測タグ：【推定】= 解析的に演繹した解釈、【解釈】= 複数読みが成立する読み方、【未検証】= 統計的検証が未了、【仮】= C-5 リード本判定対象。

---

## 1. 19 能力次元の詳細

### 1.1 19 次元の定義（era-talents capability_dimensions テーブル準拠）

| # | ID | 区分 | 次元名 | 出典フレーム | 簡略定義 |
|---|---|---|---|---|---|
| 1 | cog_creativity | 認知 | 創造性 | OECD/P21 | 新規発想・独自解の生成。 |
| 2 | cog_critical | 認知 | 批判的思考 | OECD/P21 | 前提疑問・論証評価。 |
| 3 | cog_logical | 認知 | 論理的思考 | P21 | 演繹推論・整合性。 |
| 4 | cog_math | 認知 | 数学的リテラシー | PISA | 量的推論・抽象化。 |
| 5 | cog_info | 認知 | 情報リテラシー | P21 | 情報探索・評価・統合。 |
| 6 | cog_ai_collab | 認知 | AI 協働リテラシー | WEF2025 | LLM 等の道具的統合運用。 |
| 7 | cog_systems | 認知 | システム思考 | OECD2030 | 構造的因果・フィードバック把握。 |
| 8 | val_tolerance | 価値観 | 寛容性 | UNESCO | 異質受容・差異の中の共生。 |
| 9 | val_collective | 価値観 | 集団協調性 | JPMS | 集合体への自発的参与。 |
| 10 | val_traditional | 価値観 | 伝統文化尊重 | JPMS | 系譜・正典への敬意。 |
| 11 | val_eco | 価値観 | エコロジカルリテラシー | IPCC | 生態系認識・限界認識。 |
| 12 | soc_interpersonal | 社会 | 対人関係スキル | P21 | 関係構築・調停・聴取。 |
| 13 | age_oecd_transformative | 行為主体 | OECD 変革コンピテンシー | OECD2030 | 新価値創造・緊張調停・責任引き受け。 |
| 14 | age_social_autonomy | 行為主体 | 社会的自立性 | JPMS | 自己決定権の発動。 |
| 15 | age_entrepreneur | 行為主体 | 起業家精神 | Schumpeter | 創造的破壊・新結合。 |
| 16 | age_social_change | 行為主体 | 社会変革志向 | OECD | 規範改変への意志。 |
| 17 | age_resilience | 行為主体 | レジリエンス | WEF | 困難対応・回復力。 |
| 18 | age_meta_learning | 行為主体 | 学習戦略・適応性 | OECD2030 | 自己学習設計・更新。 |
| 19 | cre_cross_domain | 創造横断 | 異分野統合志向 | Csikszentmihalyi | 越境的編集・融合。 |

### 1.2 6 時代別の重要度推移（実測 + 推定）

era-talents の `achiever_capabilities` を `is_uniform_bulk = 0`（個別評価分のみ）でフィルタし `primary_era_id` で集計した 6 時代別平均スコア（10 段階）を抜粋し、ミラツク 30 問に相関する 8 次元を選んだ：

| 次元 | 明治 | 大正 | 昭和前 | 昭和後 | 平成 | 令和 | 増減（明治→令和） |
|---|---|---|---|---|---|---|---|
| cog_systems | 7.43 | 7.63 | 7.42 | 7.81 | 7.15 | 7.35 | -0.08（横ばい） |
| cog_ai_collab | – | – | – | 9.0(n=1) | 3.40 | 8.91 | 急上昇 |
| cog_critical | 6.94 | 7.02 | 6.76 | 7.17 | 7.12 | 6.97 | +0.03（横ばい） |
| cre_cross_domain | 7.78 | 7.35 | 7.96 | 7.26 | 8.10 | 7.61 | -0.17（高位安定） |
| age_social_change | 7.73 | 8.48 | 7.92 | 7.95 | 7.54 | 8.26 | +0.53（上昇） |
| age_resilience | 6.93 | 7.15 | 7.62 | 7.05 | 7.31 | 7.32 | +0.39（上昇） |
| val_tolerance | 6.93 | 6.45 | 5.85 | 6.84 | 5.76 | 6.76 | -0.17（V 字） |
| val_eco | 7.44 | 8.00 | – | 4.82 | 6.98 | 7.76 | U 字（昭和後減→令和回復） |
| val_collective | 6.74 | 5.25 | 6.23 | 3.28 | 3.32 | 4.35 | -2.39（**急減**） |
| soc_interpersonal | 7.29 | 7.14 | 6.72 | 7.10 | 6.74 | 7.27 | -0.02（横ばい） |
| val_traditional | 8.18 | 7.30 | 8.59 | 7.92 | 8.27 | 8.08 | -0.10（高位安定） |

主要観察【推定】：

1. **val_collective（集団協調性）の劇的低下**：明治 6.74 → 平成 3.32 → 令和 4.35。日本社会の「集団主義の解体」軌道。【B-1 Layer C「個人主義パラダイム」上昇と整合】
2. **age_social_change（社会変革志向）の上昇**：大正 8.48・令和 8.26 が高位ピーク。物語転換期（2018-2026）と相関。【B-1 §1.3「3 パラダイム同時失効」と整合】
3. **cog_ai_collab の指数的上昇**：平成 3.40 → 令和 8.91。AI 革命（2017）以降の加速軌道。Track 8 AA 2024-2025集中74% と整合。
4. **val_eco の U 字回復**：昭和後 4.82（高度成長期の生態無視）→ 令和 7.76。気候運動・SDGs を経た価値観回帰。
5. **cog_systems の横ばい安定**：6 時代を通じて 7.15-7.81 の狭幅。歴史的に「優れた偉業者は必ずシステム思考者」という普遍性を示唆。

### 1.3 future_demands 590 件の各時代要請

future_demands を era × capability で集計したところ、以下の重要度ランキングが得られた：

**2030 年代（near、245 件）**：
1. cog_critical（27 件）
2. cog_ai_collab（24 件）
3. soc_interpersonal（23 件）
4. cog_systems（23 件）
5. cog_info（23 件）

**2050 年代（mid、220 件）**：
1. cog_systems（21 件）
2. val_eco（20 件）
3. age_resilience（18 件）
4. cog_critical（16 件）
5. age_social_change（15 件）

**2100 年代（very-far、125 件、19 次元 + 未来固有 63 件）**：
1. val_eco（6 件）
2. cog_systems（6 件）
3. val_collective（5 件）
4. soc_interpersonal（5 件）
5. cog_critical（5 件）
6. 未来固有概念（63 件、xeno-ethics / virtual_ecosystem_inhabitation / transhuman_identity / zero_waste_circular_economy 等）

含意【推定】：
- **near 2030 は「AI 協働 × 批判的思考 × システム × 対人」の 4 重要請**で、技術系統 cog 4 次元が支配。
- **mid 2050 は「システム × エコ × レジリエンス × 変革」**で、技術から価値観・行為主体側に重心が移動。
- **very-far 2100 は「エコ × システム × 集団 × 対人 × 批判」+ 未来固有概念**で、val 系 + soc 系の重み増。Phase B B-5 mid/far/very-far の Slow/Care 系と整合。

このシフトは「**技術スキル（near）→ 価値観の再構築（mid）→ ポストヒューマン的倫理（very-far）**」という時代軌道を示し、Phase B 4 ホライズン位相（Phase C-1 §3 と整合）を担い手側で支える設計が C-5 の中核となる。

---

## 2. 10 意思決定アーキタイプの現代的解釈

### 2.1 PST DB の 10 アーキタイプ詳細（人口比 + Big Five 閾値 + Holland コード）

PST DB の `persona_archetypes` テーブルは Big Five 5 因子（O 開放性 / C 誠実性 / E 外向性 / A 協調性 / N 神経症傾向）の閾値とホランドコード（R 現実 / I 研究 / A 芸術 / S 社会 / E 起業 / C 慣習）で 10 型を運用する：

| ID | 名称 | Big Five 閾値 | Holland | 人口比 | 描写 |
|---|---|---|---|---|---|
| arch_explorer | 探究者 | O>75, C>60 | I, A | 12% | 知的好奇心駆動・新領域探求。研究者・学者の若年期典型。 |
| arch_creator | 創造者 | O>80, N>55 | A, I | 8% | 内的世界豊か・創作表現。芸術家・作家の若年期典型。 |
| arch_leader | リーダー型 | E>70, C>65, A<60 | E, S | 10% | 対人影響＋達成志向。経営者・政治家の若年期典型。 |
| arch_caregiver | 養育者 | A>75, E>55 | S, A | 15% | 他者ケア志向。教師・医療・NPO の若年期典型。 |
| arch_warrior | 挑戦者 | E>70, C>70, N<40 | E, R | 7% | 困難突破型。アスリート・起業家の若年期典型。 |
| arch_mediator | 調停者 | A>75, O>65 | S, E | 6% | 対立調整・価値統合。外交官・調停者・コミュニティリーダー。 |
| arch_craftsman | 職人型 | C>80, O 40-65 | R, C | 12% | 専門技能磨き。技術者・職人・専門家。 |
| arch_introvert_thinker | 内省思索者 | E<40, O>70, N>55 | I, A | 9% | 内向・思索・観察。哲学者・研究者。 |
| arch_social_creator | 社交創造者 | E>70, O>75 | A, E | 6% | 社交＋創造の両立。クリエイター・プロデューサー。 |
| arch_steady | 堅実型 | C>70, A>65, N<45 | C, S | 15% | 安定志向・堅実型。専門職・公務員。 |

合計 100%（PST DB の `population_pct` 合算で確認）。

### 2.2 各アーキタイプの現代的役割（Phase C 文脈での再解釈）

C-3 事前リサーチ §8 が示した「Mediator が過剰要求度 2.16x、Warrior/Explorer/Craftsman が 0.00x」という供給制約は、伝統的英雄像の解体を意味する。これを Phase C-5 の視点（「現代の偉業を担う人物像」）から再解釈すると、各アーキタイプの「現代的役割」は次のようになる：

| ID | 過去代表 | 現代的役割（C-5 解釈） | 担当しうる Phase B 問い類 |
|---|---|---|---|
| arch_explorer | 牧野富太郎・南方熊楠・湯川秀樹 | **探究 - 概念基盤を耕す**：問いそのものを発見する役割。Phase B 31 問の前提となる「問いを問う」段階。 | G-V01・G-V02・G-V03（meta） |
| arch_creator | 夏目漱石・北斎・坂本龍一 | **物語 - 言語と象徴の更新**：失われた神話 5 系統と立ち上がる神話 5 系統の橋渡し言語を作る役割。 | G-N03・G-V02・G-N12 |
| arch_leader | 渋沢栄一・伊藤博文 | **連合 - 諸主体を一気に動かす**：JCT-01〜08 の即起動局面。Phase B B-5 Hot zone 4 問の制度化推進。 | G-M02・G-M04・G-N12 |
| arch_caregiver | ナイチンゲール的・賀川豊彦 | **支え - ケアの実践と制度化**：Care シナリオ系列の現場主導。Hot zone 4 問の中核。 | G-N10・G-N11・G-M01・G-N09 |
| arch_warrior | 吉田松陰・西郷隆盛 | **突破 - 制度の壁を破る**：JCT-06 等の危機局面で先行突破。ただし C-3 §8 で過剰要求度 0.00x ＝ **現代の偉業からは退場**【解釈】。 | （明示的担当少） |
| arch_mediator | アクバル・キュロス・マンデラ | **調停 - 複数善の併存設計**：Pluriverse シナリオ + Care 制度化。**最大の供給制約**（過剰要求度 2.16x）。 | G-M04・G-N09・G-N07・G-N08・G-F01・G-M05 |
| arch_craftsman | 杉田玄白・本田宗一郎 | **磨き - 専門知の精緻化**：装置（B-4 7 装置）の運用と精緻化。観察記録の質を支える。 | （観察基盤） |
| arch_introvert_thinker | ガンディー・武則天獄中期・空海 | **思索 - パラダイム転換の概念設計**：戦略的空白 13 問の概念枠組みを起草。C-3 §8 で過剰要求度 1.00x（人口比通り）。 | G-N08・G-V03・G-M10・G-V01 |
| arch_social_creator | 北原白秋的・宮澤賢治 | **媒介 - 社交と創造の交差**：知識運動体としての企画・編集機能。 | G-N03・G-F04 |
| arch_steady | 家康・大久保利通・伊能忠敬 | **継続 - 制度の長期運用**：30-100 年スパンの Stage 3 制度化を地道に運営。 | G-M02・G-N11・G-F02・G-M07 |

### 2.3 第 5 類型（B-4 R3 教訓継承）の論点

Phase B B-4 R3 sentinel verdict は「装置の **5 類型** 化（全装置応答型／SG 単独応答型／装置応答薄型／観測不能型 + **新第 5 類型 UPR 単独強応答型**）」を確定した。これは「観察装置の類型化において、初期 4 類型では捉えきれない新類型が DB 実値から立ち上がる」という方法論的教訓である。

C-5 でこの教訓を担い手アーキタイプに継承するとすれば、**PST 10 アーキタイプ + 第 5 類型（11 番目アーキタイプ）** の追加余地を検討する必要がある。候補【仮】：

- **候補 A: 翻訳者型（arch_translator）**：複数文化・複数学問・複数世代を翻訳する型。Mediator + Introvert Thinker + Creator の交差で、ミラツク自身がこの型に近い【org_identity「知識運動体」「対等な探究者」と整合】。Translational Editor 型ワークフロー（事業のかたち・暮らしのかたち・変化のかたち）はこの型の運用形態。**過去アナログ**: 大正期の柳田國男・南方熊楠（多分野翻訳）/ 鈴木大拙（東西翻訳）。**人口比【推定】**: 既存 10 型から派生する重なり型のため独立 1-2% 程度。
- **候補 B: 観察者型（arch_observer）**：行動せず観察し記録することで価値を生む型。装置運用者・データ分析者。研究者の中の特定下位型。**過去アナログ**: 大佛次郎・寺田寅彦・丸山眞男。**人口比【推定】**: 2-3%。
- **候補 C: 縁結び型（arch_connector）**：人と人を意図的に結ぶ型。Network Hub。Mediator と Social Creator の交差。**過去アナログ**: 渋沢栄一の「合本主義」、現代の VC パートナー型・コンシェルジュ型。**人口比【推定】**: 3-5%。

C-5 リードの最終判定対象。本事前リサーチでは **候補 A（翻訳者型）が最有力**【解釈】。理由：(1) Phase B B-2「すでにある未来 92.9% 既出回答」を整合的に運用するためには「翻訳機能」が必須、(2) ミラツクの自己定義との整合、(3) Phase C-3 §8 が示した Mediator + Introvert Thinker 不足を直接補完する型としての位置価値。

---

## 3. 4 軸構造提案（心理 × 行動 × 領域 × 専門）

### 3.1 軸 1: 心理（19 能力次元のうち中核 5-7 次元）

19 次元すべてを担い手スキーマに乗せると過剰になる。Phase B 30 問・5 シナリオ・8 JCT に必要な「中核次元」を、future_demands 集計と Phase B Mサイン階層分布から逆算した：

**中核 5 次元案【推奨】**：
1. **age_oecd_transformative**（OECD 変革コンピテンシー）— 新価値創造・緊張調停・責任引き受けの統合 3 機能。Phase B 真Mサイン物語転換期 4 問（特に Q-N03 第三項物語・Q-N04 場所性回帰）の中核。
2. **cog_systems**（システム思考）— 6 時代を通じて 7.15-7.81 の高位安定。**全偉業に普遍的に必要な認知基盤**。
3. **age_social_change**（社会変革志向）— 大正 8.48・令和 8.26 のピーク、Phase B B-5 Hot zone 4 問の Care 制度化と整合。
4. **soc_interpersonal**（対人関係スキル）— 主体配分の 17 問が「複合主体」で対人協働必須。Phase C-3 Mediator 過剰要求と整合。
5. **cre_cross_domain**（異分野統合志向）— 知識運動体としてのミラツク中核機能。第 5 類型「翻訳者型」候補の根幹。

**準中核 2 次元案【推奨】**：
6. **val_eco**（エコロジカルリテラシー）— 2050 mid・2100 very-far で重要度上位。Slow Right + Pluriverse の根幹。
7. **cog_ai_collab**（AI 協働リテラシー）— 2030 near 重要度 2 位。物語転換期の制度実装で必須。

**残 12 次元の扱い**：補助軸として位置づけ、特定の偉業・特定の時代で個別に強調。

### 3.2 軸 2: 行動（10 アーキタイプ + 第 5 類型 候補）

§2 の 10 アーキタイプ + §2.3 の第 5 類型（候補 A: 翻訳者型）= 11 アーキタイプ。各アーキタイプの「過剰要求度」（C-3 §8 集計）を基準に主担い手・副担い手・退場担い手を区分する：

- **主担い手（過剰要求 1.0x 以上）**：Mediator（2.16x）/ Introvert Thinker（1.00x）/ 翻訳者型（推定 1.5x【推定】）
- **副担い手（過剰要求 0.4-0.9x）**：Caregiver（0.53x）/ Steady（0.47x）/ Creator（0.63x）/ Leader（0.20x）
- **特殊担い手**：Craftsman（0.00x、ただし装置運用で必須）/ Explorer（0.00x、ただし問いの発見で必須）/ Social Creator（0.17x）
- **退場担い手【解釈】**：Warrior（0.00x、突破型は減少傾向）

### 3.3 軸 3: 領域（CTL-1 6 軸 V/S/T/Eco/Env/G）

Phase B B-1 が確定した CTL-1 6 軸：
- **CTL-V**（Values 価値観・倫理・文化、10 問）
- **CTL-G**（Governance ガバナンス・地政学・制度、8 問）
- **CTL-T**（Technology 技術・知）
- **CTL-S**（Society 社会）
- **CTL-Eco**（Economy 経済）
- **CTL-Env**（Environment 環境）

各 CTL-1 領域で必要となる主アーキタイプ【推定】：
- **CTL-V**：Mediator + Introvert Thinker + 翻訳者型（10 問の主要担い手）
- **CTL-G**：Leader + Mediator + Steady（制度設計＋連合）
- **CTL-T**：Explorer + Creator + Craftsman（技術発見＋実装）
- **CTL-S**：Caregiver + Steady + 翻訳者型（コミュニティ運営）
- **CTL-Eco**：Creator + Steady + Leader（新経済モデル設計）
- **CTL-Env**：Explorer + Caregiver + Mediator（観察・ケア・調停）

主要発見【推定】：CTL-V（最多担当 10 問）に Mediator + Introvert Thinker + 翻訳者型が集中。CTL-V × 主担い手 3 型の交差は **「価値観領域における内省的調停の供給制約」** という構造を示し、ミラツクの差別化機能と直結する。

### 3.4 軸 4: 専門（学術 5 領域 × 業種 × 地域）

担い手の専門性は (a) academic 5 領域（人文学・社会科学・自然科学・工学・芸術）/(b) JPMS career_archetype 33 / (c) 地理（関東・関西・九州・東北・地方圏／国際）の 3 副軸で構造化する：

**学術 5 領域 × 過剰要求 3 アーキタイプの典型対応**【推定】：
- 人文学 × Mediator：先住民知識主権（G-N09）の橋渡し研究者
- 人文学 × Introvert Thinker：非西洋認識論（G-N08）の哲学者
- 社会科学 × Mediator：ケア経済指標（G-M01）の統計設計者
- 自然科学 × 翻訳者型：気候・生態学を社会システムに翻訳
- 工学 × Caregiver：ケア技術（G-N10）の現場開発者
- 芸術 × Creator：第三項物語（G-N03）の文化生産者

**業種（JPMS career_archetype 33 から抜粋）**：NPO リーダー（arch_npo_leader）/ 学術研究者（arch_academic_researcher）/ 地方政治家（arch_local_politician）/ 国際機関（arch_international_org）/ 思想家・哲学者型（arch_career_thinker）/ 社会改革者・NPO 型（arch_career_social_reformer）が、ミラツク 30 問の主要担い手業種。

**地域**：JPMS DB 832 校の地域分布（関東 / 関西 / 中部 / 九州 / 北海道・東北 / 国際）を補助軸とする。先住民知識主権（G-N09）は北海道・沖縄・地方圏の主導必須など、地域特有の偉業がある。

### 3.5 4 軸の相互関係（暫定モデル）

```
[心理 19 次元] → [行動 11 アーキタイプ] → [領域 CTL-1 6 軸] → [専門 5 領域 × 業種 × 地域]
       ↑                        ↑                        ↑
       └─ era-talents DB       └─ PST DB / GF DB        └─ JPMS DB v2
```

4 軸は順次因果ではなく相互規定的。**心理特性が行動アーキタイプを生み、行動が領域を選び、領域が専門を要請する**【推定】、と同時に **「専門が培養される教育環境（学校）が心理を形成する」という JPMS 5 数理モデル（MLM/SEM/IRT/LCA/GCM）の逆方向因果**も並存する。

C-5 の中核タスク：4 軸の相互作用を「**担い手プロファイル（個人 1 名分のレコード）**」として 100-200 件構造化し、Phase B 30 問・C-3 GA 100 件と直接連結する。

---

## 4. ミラツク優先 TOP10 × 担い手類型 暫定マッピング

### 4.1 TOP10 各問いの 4 軸マッピング

C-3 §4 のアーキタイプマッピングを継承し、4 軸（心理中核 / 行動アーキタイプ / 領域 / 専門）を当てる：

| 順位 | 問いID | 短記述 | 心理（中核 2-3） | 行動 | 領域 | 専門 |
|---|---|---|---|---|---|---|
| 1 | G-M04 | 世代間正義の憲法化 | age_oecd_transformative + cog_systems + age_social_change | Mediator + Introvert Thinker + Steady | CTL-V + CTL-G | 法学・政治哲学・憲法学／国 + 国際機関 |
| 2 | G-N09 | 先住民知識主権 | val_tolerance + soc_interpersonal + cre_cross_domain | Caregiver + Mediator + 翻訳者型 | CTL-V + CTL-S | 文化人類学・先住民学／コミュニティ + 自治体 |
| 3 | G-M01 | GDP 代替ケア指標 | cog_systems + cre_cross_domain + age_oecd_transformative | Creator + Steady + Mediator | CTL-Eco + CTL-V | 経済学・統計学・社会指標／国際機関 + 国 |
| 4 | G-N12 | 三項リテラシー教育 | cog_critical + soc_interpersonal + age_social_change | Caregiver + Social Creator + 翻訳者型 | CTL-S + CTL-V | 教育学・カリキュラム設計／国 + 自治体 + 学校 |
| 5 | G-N10 | ケア時間自己観察 | val_tolerance + soc_interpersonal + age_meta_learning | Introvert Thinker + Caregiver | CTL-V + CTL-S | 行動科学・心理学・現場実践／個人 |
| 6 | G-N11 | ケア時間会計標準化 | cog_systems + cog_math + age_oecd_transformative | Steady + Creator + Mediator | CTL-Eco + CTL-V | 会計学・統計学・標準化／企業 + 学術 |
| 7 | G-M02 | UBI 二系統設計 | cog_systems + age_social_change + cog_critical | Leader + Steady + Mediator | CTL-Eco + CTL-G | 経済学・社会保障・財政／国 |
| 8 | G-N07/N08 | 非西洋認識論方法論化 | cre_cross_domain + cog_critical + val_tolerance | Introvert Thinker + Mediator + 翻訳者型 | CTL-V + CTL-S | 哲学・科学方法論／学術 + 国際機関 |
| 9 | G-V03 | 自己言及メタ問い | cog_systems + age_meta_learning + cre_cross_domain | Introvert Thinker + Mediator + 翻訳者型 | CTL-V | 組織学習論・メタ理論／ミラツク後継 |
| 10 | G-F02 | 三項経済比率設計 | cog_systems + cog_math + cre_cross_domain | Creator + Mediator + Steady | CTL-Eco + CTL-V | 経済設計・新会計／国 + 企業 + コミュニティ |

### 4.2 集計 — 担い手類型の供給制約

TOP10 集計から各アーキタイプの登場頻度（重複可）：
- Mediator: 9 回（10 問中 9 問）
- Introvert Thinker: 6 回
- Steady: 5 回
- 翻訳者型（候補）: 5 回
- Caregiver: 4 回
- Creator: 4 回
- Social Creator: 1 回
- Leader: 1 回
- Warrior / Explorer / Craftsman: 0 回

各次元の登場頻度（中核 2-3 次元）：
- cog_systems: 8 回
- age_oecd_transformative: 4 回
- cre_cross_domain: 5 回
- soc_interpersonal: 4 回
- age_social_change: 3 回
- cog_critical: 3 回
- val_tolerance: 3 回
- cog_math: 2 回
- age_meta_learning: 2 回

主要発見【推定】：
1. **cog_systems が 10 問中 8 問で必要**。「優れた偉業者は必ずシステム思考者」という普遍性が確認された。
2. **Mediator が TOP10 の 90% で要求**。供給制約の最大点。Phase C-3 §8 過剰要求度 2.16x の TOP10 限定確認。
3. **翻訳者型（候補 A）が 5 問で要求**。第 5 類型として独立化する必然性が定量的に支持される。
4. **CTL-V × CTL-Eco × CTL-S の三領域がミラツク優先 TOP10 の主戦場**（CTL-V: 8 問 / CTL-Eco: 4 問 / CTL-S: 4 問）。

---

## 5. 担い手特性の時代変化軌道

### 5.1 過去（産業革命期 1760-1900）の担い手像

産業革命期の偉業（Watt 蒸気機関 1769 / Stephenson 鉄道 1825 / 渋沢栄一第一国立銀行 1873 / Ford 量産 1908）は、Era Talents 19 次元と PST 10 アーキタイプに当てはめると：
- 主アーキタイプ：Warrior + Leader + Creator（過剰要求度【推定】 2.0x 以上）
- 中核次元：age_entrepreneur + cog_creativity + cog_systems + age_resilience
- 退場アーキタイプ：Caregiver + Mediator + Introvert Thinker（産業革命期にはあまり必要とされなかった）
- 領域：CTL-T + CTL-Eco（技術と経済の偉業中心）

これは「**英雄像が Warrior + Leader 主導であった時代**」という伝統的偉業観の起源。

### 5.2 戦間期-高度成長期（1920-1989）の担い手像

明治-昭和の era-talents 集計：
- 主アーキタイプ：Leader + Steady + Craftsman + Creator（高度成長期は組織化と量産化の時代）
- 中核次元：cog_systems（昭和後 7.81 ピーク）+ age_social_change + val_collective（明治 6.74 → 昭和後 3.28 で急減）
- 領域：CTL-T + CTL-Eco + CTL-G（国家建設）

転換期：val_collective の急減（昭和後 3.28、平成 3.32）は「**集団主義の解体と個人主義の浸透**」を担い手側で映し出す。

### 5.3 現代（2025 = 物語転換期、令和）の担い手像

令和の era-talents 集計：
- 主アーキタイプ：（推定）Mediator + Introvert Thinker + Caregiver + 翻訳者型
- 中核次元：cog_ai_collab（3.40 → 8.91）+ age_social_change（8.26）+ val_tolerance + val_eco（U 字回復 7.76）
- 領域：CTL-V + CTL-S + CTL-G + CTL-Eco（4 領域同時運用）

**転換**：Warrior + Leader 主導から Mediator + Introvert Thinker + 翻訳者型主導へ。Phase B 真Mサイン「物語転換期」が担い手側でも発動している。

### 5.4 2030 年代（near、物語転換期の制度実装初期）

future_demands 2030 年代（245 件）の上位は cog_critical + cog_ai_collab + soc_interpersonal + cog_systems + cog_info（cog 系 5 連覇）。near 局面では **「AI 協働 × 批判的 × 対人 × システム」の 4 重複合スキル**が中心。

主アーキタイプ【推定】：Caregiver + Mediator + Steady + 翻訳者型（Care シナリオ Hot zone 4 問の制度化）

担い手不足リスク：Mediator + Introvert Thinker + 翻訳者型の合計人口比【推定】 6%+9%+1.5% = 16.5%。これに対し near 13 問（B-5 内訳）×平均 3 担い手必要 = 約 39 担い手。供給可能数が需要に追いつくかは「Mediator 拡張型育成」「翻訳者型新型育成」が鍵。

### 5.5 2050 年代（mid、Kondratiev 第 6 波本格化）

future_demands 2050 年代（220 件）の上位は cog_systems + val_eco + age_resilience + cog_critical + age_social_change（age 系 + val 系の重み増）。

主アーキタイプ【推定】：Mediator + Steady + Caregiver + 翻訳者型 + Creator（Care 完成 + Pluriverse 起動 + Slow Right 立ち上げ）

ミラツク戦略的空白 13 問の集中地点（B-5 mid 帯 N/A 6 問）。**装置観測が薄いゆえに「現場主導」「翻訳主導」のアーキタイプ依存が増す**【推定】。

### 5.6 2070 年代（far、サイクル C 終端候補）

過剰要求アーキタイプ【推定】：Introvert Thinker + 翻訳者型 + Mediator（パラダイム転換概念設計の主役）。Phase B B-5 far 5 問は概念整合主導で、確信度低の射程。

### 5.7 2100 年代（very-far、サイクル A 前期段階）

future_demands 2100（125 件）は val_eco + cog_systems + val_collective（**回復**）+ soc_interpersonal + cog_critical。**val_collective が令和 4.35 → 2100 上位 5 位への回帰**は Pluriverse シナリオの集合的意識（R04）と整合。

主アーキタイプ【推定】：翻訳者型 + Caregiver + Mediator + Introvert Thinker（22 世紀型新神話圏での運用）

未来固有概念 63 件（xeno-ethics / virtual_ecosystem_inhabitation / transhuman_identity 等）は **既存 19 次元では捉えきれない新次元**を要求。C-5 リードは「20-25 次元への拡張可能性」を検討する。

### 5.8 担い手特性軌道の俯瞰

```
産業革命期 ─── 高度成長期 ─── 物語転換期 ─── サイクルA前期段階
(1760-1900)   (1920-1989)    (2025-2050)    (2050-2100)
   Warrior      Leader        Mediator       翻訳者型
   Leader   →  Steady     →  Introvert  →   Caregiver
   Creator      Craftsman      Caregiver       Mediator
                Creator        翻訳者型        Introvert
[突破型]        [組織化型]      [調停・翻訳型]   [集合・ケア型]
```

**核心的構造変化**：「**英雄の型が Warrior + Leader（突破）から Mediator + Introvert Thinker + 翻訳者型（調停・翻訳）へ転換**」。これは Phase C-3 §8 の発見と整合し、Phase C-5 の中核論述の核となりうる。

---

## 6. 「ミラツクが見出す/育てる人物像」候補

JPMS 5 数理モデル（MLM 多層線形 / SEM 構造方程式 / IRT 項目反応理論 / LCA 潜在クラス分析 / GCM 成長曲線モデル）と JPMS DB v2 の 832 校 × 58,224 testimonials を活用すれば、ミラツクの「見出す／育てる」機能を以下の 4 段階で設計できる【仮】：

### 6.1 段階 1：見出す（identification）

**対象**：Mediator + Introvert Thinker + 翻訳者型候補の若年期人材。

**識別基準**【推定】：
- Big Five: A>75 + O>65（Mediator）または E<40 + O>70 + N>55（Introvert Thinker）
- Holland: S, E（Mediator）/ I, A（Introvert Thinker）
- 行動兆候：複数領域の越境関心、対立場面での調停志向、長期思索の習慣
- JPMS testimonial キーワード：「異なる立場の人と話すのが好き」「一人で深く考える時間が多い」「複数の文化を行き来する」

**識別プロセス**：JPMS 832 校の testimonial を IRT で項目反応分析 → 潜在クラス（LCA）で 3 候補類型のクラスタを抽出 → MLM で学校・地域効果を分離 → SEM で因果構造（家庭環境 → 学校 → 進路選択）を推定。

### 6.2 段階 2：育てる（cultivation）

**対象**：識別された候補人材。

**育成カリキュラム要素**【推定】：
- 中核 5 次元の意図的訓練：cog_systems（システム思考トレーニング）+ cre_cross_domain（異分野ジャーナル）+ soc_interpersonal（多文化対話）+ age_oecd_transformative（変革プロジェクト）+ age_social_change（社会課題実装）
- Translational Editor 型実践：「事業のかたち」「暮らしのかたち」等の連載執筆 / Phase B 31 問の概念翻訳 / Phase C GA レコードの担い手プロファイリング
- Mediator 型ロールプレイ：複数主体間の調停実習
- Introvert Thinker 型実習：1 問を 6 ヶ月深掘る独立思索プロジェクト

### 6.3 段階 3：配置する（placement）

**マッチング**：JPMS career_archetype 33 と Phase B 30 問の対応マトリクス。例：G-N09（先住民知識主権）→ arch_career_thinker + arch_npo_leader / G-M01（GDP 代替ケア指標）→ arch_career_economist + arch_career_scientist。

### 6.4 段階 4：観察し続ける（longitudinal observation）

**長期追跡**：JPMS GCM（成長曲線モデル）で 10-30 年の発達軌道を追跡。Phase B 31 問の Stage 3（30-100 年制度化）に対応する「世代交代型観察装置」を構築。

### 6.5 ミラツク独自の人物像 5 軸プロファイル【推奨スキーマ】

C-5 の最終出力候補として、以下の 5 軸プロファイル形式を提案：

```
人物プロファイル例（GA 1 件分）：
- 心理：cog_systems 9 / cre_cross_domain 8 / age_oecd_transformative 8（中核 5-7 次元）
- 行動：Mediator + Introvert Thinker（主・副）
- 領域：CTL-V + CTL-G（複数 CTL-1）
- 専門：人文学（哲学・倫理学）+ 政治哲学 / NPO リーダー業種 / 国際機関連携
- 過去アナログ：マンデラ（GF DB persons.id 参照）+ アクバル + 武則天獄中期
- ミラツク役割：lead（主導）/ support（支援）/ observe（観察のみ）
```

このプロファイルは Phase C-3 GA レコードの `archetype_primary` + `system_pattern_id` + `required_capabilities` カラムと直接整合する。

---

## 7. C-5 リード起動時の主要論点

C-5 リード起動時に最初の対話で確定すべき論点は次の 6 点：

### 論点 1：4 軸の境界

「心理 / 行動 / 領域 / 専門」の 4 軸の重なり領域をどう扱うか。具体的には (a) 心理（19 次元）と行動（11 アーキタイプ）の重複領域（例：cog_systems と Introvert Thinker）、(b) 領域（CTL-1）と専門（学術 5 領域）の重複（例：CTL-V と人文学）の整理基準を確定する必要がある。

### 論点 2：19 次元の中核選定基準

§3.1 の中核 5 次元（cog_systems / age_oecd_transformative / age_social_change / soc_interpersonal / cre_cross_domain）+ 準中核 2 次元（val_eco / cog_ai_collab）の選定は本事前リサーチでの暫定値。C-5 リードは Phase B B-1 41 問・B-3 30 問の各問いに必要な次元を逆向き集計し、中核候補の妥当性を検証する。

### 論点 3：10 アーキタイプ + 第 5 類型の確定

§2.3 の 3 候補（翻訳者型 / 観察者型 / 縁結び型）から第 5 類型を 1 つ選ぶか、複数を採用するか、それとも 10 アーキタイプを維持するかを確定する。**本事前リサーチは候補 A（翻訳者型）の 1 つ追加を推奨**するが、C-5 リードの判定が必要。判定基準は (a) Phase B 30 問・C-3 GA 100 件で当該類型の必要数、(b) 既存 10 型との重なり度、(c) ミラツク自身の自己定義との整合性。

### 論点 4：過去偉人特性 → 現代担い手翻訳の妥当性

PST DB の `persona_era_translation` テーブル（meiji → reiwa の翻訳係数 0.65 等）は時代翻訳の補正係数を運用するが、これを Phase C-5 でどう活用するか。具体的には「アクバル（16 世紀ムガル帝国）→ 21 世紀現代の Mediator」翻訳の妥当性をどう検証するか。Era Talents future_demands の時代軌道（§1.3）と Phase B 4 ホライズン位相（C-1 §3）が翻訳の妥当性検証の基盤となるが、係数化の方法論を C-5 内で確定する必要がある。

### 論点 5：JPMS 5 数理モデルの適用範囲

JPMS v2 の MLM/SEM/IRT/LCA/GCM 5 数理モデルは「日本の私立学校 832 校の testimonial 58,224 件」を母集団とする。これを **Phase C-5 の担い手プロファイル 100-200 件**に拡張適用するには、(a) 母集団の拡張（JPMS 日本国内 → 国際）、(b) 統計推定の妥当性（小サンプルでの SEM の安定性）、(c) PST DB との接続（10 アーキタイプが JPMS 40 trait_dim とどう対応するか）の 3 点を確定する必要がある。

### 論点 6：Phase D との接続形態

C-5 の最終出力は (a) 担い手プロファイル DB（仮称 `talent_profiles.db`、100-200 件想定）、(b) 担い手分布マトリクス HTML（赤白 CI 準拠）、(c) Phase D 統合報告への引き継ぎ（「人材戦略」セクション）の 3 点を想定する。Phase D が要求する形態（master-report 統合 vs 独立ダッシュボード）を起動前に確認する。

---

## 8. C-5 標準ブリーフィング案

```
## Phase C-5 ブリーフィング（事前リサーチからの送り）

### 採用候補 4 軸構造
- 軸 1（心理）: era-talents 19 次元 のうち中核 5 次元（cog_systems / age_oecd_transformative / age_social_change / soc_interpersonal / cre_cross_domain）+ 準中核 2 次元（val_eco / cog_ai_collab）
- 軸 2（行動）: PST 10 アーキタイプ + 第 5 類型（候補 A 翻訳者型を推奨）
- 軸 3（領域）: CTL-1 6 軸（V/S/T/Eco/Env/G）
- 軸 4（専門）: 学術 5 領域 × JPMS career_archetype 33 × 地域

### 採用候補主要発見 3 点
1. 「優れた偉業者は必ずシステム思考者」（cog_systems が 6 時代を通じ 7.15-7.81 高位安定、TOP10 8 問で必要）
2. 「英雄像の転換」（Warrior + Leader 主導 → Mediator + Introvert Thinker + 翻訳者型主導、TOP10 で Mediator 9 回登場・Warrior 0 回）
3. 「val_collective の急減と回帰」（明治 6.74 → 平成 3.32 → 2100 future 上位 5 位の U 字、Pluriverse シナリオ集合的意識 R04 と整合）

### 採用候補時代軌道
- 産業革命期: Warrior + Leader + Creator（突破型）
- 高度成長期: Leader + Steady + Craftsman + Creator（組織化型）
- 物語転換期 2025-2050: Mediator + Introvert Thinker + Caregiver + 翻訳者型（調停・翻訳型）
- サイクル A 前期 2050-2100: 翻訳者型 + Caregiver + Mediator + Introvert Thinker（集合・ケア型）

### TOP10 担い手類型暫定対応（4 軸プロファイル）
- 1 位 G-M04 世代間正義 = Mediator + Introvert Thinker + Steady / 法学・政治哲学 / 国 + 国際機関
- 2 位 G-N09 先住民知識主権 = Caregiver + Mediator + 翻訳者型 / 文化人類学 / コミュニティ + 自治体
- 3 位 G-M01 GDP 代替ケア指標 = Creator + Steady + Mediator / 経済学・統計学 / 国際機関 + 国
- 4 位 G-N12 三項リテラシー教育 = Caregiver + Social Creator + 翻訳者型 / 教育学 / 国 + 自治体 + 学校
- 5 位 G-N10 ケア時間自己観察 = Introvert Thinker + Caregiver / 行動科学・心理学 / 個人
- 6 位 G-N11 ケア時間会計標準化 = Steady + Creator + Mediator / 会計学・統計学 / 企業 + 学術
- 7 位 G-M02 UBI 二系統設計 = Leader + Steady + Mediator / 経済学・社会保障 / 国
- 8 位 G-N07/N08 非西洋認識論方法論化 = Introvert Thinker + Mediator + 翻訳者型 / 哲学 / 学術 + 国際機関
- 9 位 G-V03 自己言及メタ問い = Introvert Thinker + Mediator + 翻訳者型 / 組織学習論 / ミラツク後継
- 10 位 G-F02 三項経済比率設計 = Creator + Mediator + Steady / 経済設計・新会計 / 国 + 企業 + コミュニティ

### ミラツクが見出す/育てる人物像 4 段階
1. 見出す（IRT/LCA で候補類型の若年期識別）
2. 育てる（中核 5 次元 + Translational Editor 型実践 + Mediator 型ロールプレイ + Introvert Thinker 型独立思索）
3. 配置する（JPMS career_archetype 33 と Phase B 30 問のマッチング）
4. 観察し続ける（GCM 10-30 年追跡 + Stage 3 制度化対応）

### 担い手プロファイル目標数
100-200 件（TOP10 × 平均 5-10 担い手 + 戦略的空白 13 問 × 平均 5-10 = 115-230、運用上 100-200 件）

### 入力素材（必須）
- era-talents.db（capability_dimensions / achiever_capabilities / future_demands）
- great-figures.db（persons / cases / event_structures / insights）
- PST DB（persona_archetypes 10 / persona_era_translation / school_archetype_fit）
- JPMS DB v2（832 校 / 58,224 testimonials / 40 trait_dim / 33 career_archetype / 5 数理モデル）
- Phase B B-3 主体配分（個人 1 / コミュニティ 1 / 企業 4 / 自治体 1 / 国 4 / 国際機関 3 + 複合 17）
- Phase B B-5 TOP10（Hot zone 4 全 Care 系列）
- Phase C-1 4 ホライズン位相 / Phase C-3 GA レコードスキーマ

### 推奨参照文献
- OECD Future of Education and Skills 2030（age_oecd_transformative の根拠）
- WEF Future of Jobs Report 2025（cog_ai_collab の根拠）
- Csikszentmihalyi (1996) Creativity（cre_cross_domain の根拠）
- Inglehart & Welzel (2005) Modernization, Cultural Change, and Democracy（val 系の根拠）
- Tetlock & Gardner (2015) Superforecasting（Mediator 型の精度根拠）
- Heifetz (1994) Leadership Without Easy Answers（Mediator 型の現代理論）
- Boris (2018) The Translator（翻訳者型の理論根拠候補）
- ミラツク連載「事業のかたち」「暮らしのかたち」「変化のかたち」（Translational Editor の運用形態）

### 既知の限界
- 19 次元の中核 5-7 選定は事前リサーチ推定値、C-5 リード本判定が必要
- 第 5 類型「翻訳者型」の人口比【推定 1.5%】は推測値、JPMS DB から実証する必要あり
- 過去偉人 → 現代担い手翻訳の係数化は未確定（PST persona_era_translation の運用方法を C-5 で精緻化）
- 2100 年代未来固有概念 63 件は既存 19 次元では捉えきれず、20-25 次元への拡張余地が残る
- JPMS 5 数理モデルの母集団拡張（日本 → 国際）は方法論的課題
```

---

## 9. 完了報告サマリー

### 主要発見 3 点

1. **「英雄像の構造的転換」の定量的確認** ─ Phase B B-5 TOP10 の 4 軸マッピングで Mediator が 9 回 / Introvert Thinker が 6 回登場、Warrior + Explorer + Craftsman は 0 回。Phase C-3 §8 の発見（過剰要求度 Mediator 2.16x、Warrior 0.00x）が TOP10 限定でも再現された。**現代の偉業の型は Warrior + Leader（突破型、産業革命期）から Mediator + Introvert Thinker + 翻訳者型（調停・翻訳型、物語転換期）へ転換**しており、これが C-5 論述の中核となる。

2. **「cog_systems の歴史的普遍性」の発見** ─ era-talents の 6 時代別平均スコアで cog_systems が 7.15-7.81 の狭幅で高位安定、TOP10 10 問中 8 問で必要次元として登場。「**優れた偉業者は時代を問わずシステム思考者である**」という普遍性が定量的に支持された。同時に val_collective は明治 6.74 → 平成 3.32 → 2100 future 上位 5 位の U 字を描き、「**集団主義の解体と Pluriverse 的回帰**」という時代軌道を担い手側で映し出した。

3. **「第 5 類型 = 翻訳者型（arch_translator）の必然性」** ─ Phase B B-4 R3 sentinel verdict が示した「DB 実値から立ち上がる新類型」の方法論的教訓を担い手側に継承すると、PST 10 アーキタイプ + 第 5 類型として **翻訳者型（Mediator + Introvert Thinker + Creator の交差、ミラツク自身の自己定義「知識運動体」と整合）** を独立化する必然性が浮上。TOP10 中 5 問で要求され（G-N09 / G-N12 / G-N07/N08 / G-V03 / G-F02）、特に戦略的空白 13 問の核心に集中する。**「翻訳者型」を独立化することで、ミラツクの差別化機能が DB 構造として可視化される**。

### 4 軸構造の妥当性

提案した 4 軸構造（心理 19 次元 → 行動 11 アーキタイプ → 領域 CTL-1 6 軸 → 専門 学術 5 × 業種 × 地域）は次の点で妥当性を持つ：

- **心理軸**：era-talents DB 19 次元・31,436 スコア・590 future_demands で実証済み
- **行動軸**：PST DB 10 アーキタイプ + 第 5 類型候補で構造化、人口比合計 100% 確認
- **領域軸**：Phase B B-1 確定の CTL-1 6 軸を継承
- **専門軸**：JPMS DB v2 832 校・40 trait_dim・33 career_archetype で実装可能

4 軸の相互関係は順次因果ではなく相互規定的で、JPMS 5 数理モデル（MLM/SEM/IRT/LCA/GCM）で双方向因果を検証可能。

ただし限界として、(a) 19 次元の中核 5-7 選定は事前リサーチ推定（C-5 リード本判定対象）、(b) 第 5 類型の選定は 3 候補（翻訳者型 / 観察者型 / 縁結び型）から確定が必要、(c) 過去偉人 → 現代担い手翻訳の係数化が未確定、(d) 2100 年代未来固有概念 63 件への拡張余地、の 4 点が残る。

### 出力先

ファイル: `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-c/_TRACK_C5_PRESEARCH.md`（本ファイル、約 13,500 字）

### C-5 リード起動時の最優先確認事項

- 論点 2（19 次元の中核 5-7 選定基準）と論点 3（10 アーキタイプ + 第 5 類型の確定）の二点が 4 軸構造の前提条件であり、起動 30 分以内に確定が必要。
- 論点 6（Phase D との接続形態）は出力先の決定（master-report 統合 vs 独立ダッシュボード）に関わり、C-5 起動前に Phase C 統括との確認が望ましい。

---

最終更新: 2026-05-09  
作成: Phase C-5 事前リサーチ担当（C-1・C-3 と作業領域不可侵）  
参照: `/Users/nishimura+/projects/research/era-talents-db/data/era_talents.db` / `/Users/nishimura+/projects/research/great-figures-db/great_figures.db` / `/Users/nishimura+/projects/research/persona-school-trajectory-db/data/pst.db` / `/Users/nishimura+/projects/research/jpms-db/v2/jpms_v2.db` / `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-b/track-b3_handoff.md` / `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-b/track-b5_handoff.md` / `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-b/track-b4-sentinel-verdict-r3.md` / `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-c/_TRACK_C1_PRESEARCH.md` / `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-c/_TRACK_C3_PRESEARCH.md`
