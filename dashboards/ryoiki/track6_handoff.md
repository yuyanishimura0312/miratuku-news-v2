# Track 6 完了引継ぎ書

## 1. メタ情報
- Track番号: 6
- トラック・タイトル: 卓越人材×偉人×JPMS — 時代が求めた人材 vs. 実際に活躍した人材
- 主軸DB: ET (era_talents.db) + GF (great_figures.db) + JPMS v2 (jpms_v2.db) + PST (pst.db)
- 担当: Track 6 リード
- 完了日: 2026-05-09
- 検証ステータス: 自己検証完了（22項目・問題なし8・要解釈4・要追跡7・要修正0・構造的ギャップ3） / doc-verify 待機 / sentinel 待機

## 2. 主要数値（実DB検証済）
- ET: 12,958人物・31,430能力スコア・19能力次元・6時代・590未来需要・800言説・1,353事後評価・7 gap_insights ※集計L-01〜L-12
- GF: 9,178人物・397幼少期プロファイル・568経営概念・329ケース・19構造的洞察・7時代タグ・17職能カテゴリ ※集計L-13〜L-22
- JPMS v2: 832校・58,224証言・101成果次元・38特性次元・4,408学校×時代整合・25 person_archetype（jpms_v2.db）・7成果クラスタ ※集計L-23〜L-37
- PST: 10アーキタイプ（pst.db persona_archetypes）・600偉人プロファイル・60校・37予測経路・540学校×時代整合・8時代 ※集計L-38〜L-40
- 確認済み三系列差: ETスコア「31,436 vs 31,430」（6件差）、JPMS「551校・36,943件 vs 832校・58,224件」（v2全件 vs 主要モデル）の二件
- 検索済みクエリ数: L-01〜L-51（51件）

## 3. 強みホライズン領域
- 主強み: **mid（2036-2055、人材育成リードタイム25-50年と一致、220未来需要）**
- 副強み: **near（2026-2035、認知5次元並走、245未来需要）**
- 独自スパン: **past（1868-2025、6時代×19能力次元の実績マトリクス独自）**
- 構造的弱点: **far（2056-2080、人材育成射程外で0需要）**
- 補強的弱点: **very-far（2081-2100、19次元外64件拡張カテゴリ、526件 89.2%が19次元マッチ）**
- 根拠: report.html 第3章、analysis.html L-06, L-07, L-41, L-41a

## 4. ホライズン×能力次元MAP（要約）

| 能力次元（抜粋） | near (2030) | mid (2050) | far (2070) | very-far (2100) |
|---|---|---|---|---|
| 批判的思考 | H 27 | M 16 | 空白 | L 5 |
| AI協働リテラシー | H 24 | M 12 | 空白 | L 3 |
| システム思考 | H 23 | H 21 | 空白 | L 6 |
| 対人関係スキル | H 23 | M 14 | 空白 | L 5 |
| エコロジカルリテラシー | L 9 | H 20 | 空白 | M 6 |
| レジリエンス | M 18 | M 18 | 空白 | L 5 |
| 19次元外（拡張カテゴリ） | — | — | 空白 | H 64 |

## 5. 問うべき領域TOP10

| # | 領域タイトル | 戦略 | W | C | M | 計 | 主担当ホライズン |
|---|---|---|---|---|---|---|---|
| 1 | 言説-実績ラグ構造の意識化（126年継続 vs 転換） | 密度 | 5 | 5 | 5 | 15 | past→near→mid |
| 2 | 令和の言説-実績逆転の持続性（AI協働等の実績転化） | 密度 | 5 | 4 | 5 | 14 | near→mid |
| 3 | 能力次元体系の再設計（very-far 19次元外64件） | 空白 | 5 | 3 | 5 | 13 | mid→very-far |
| 4 | 教育の階級的偏在の可視化（GF 4.3%カバーが示唆） | 空白 | 5 | 3 | 5 | 13 | past→near |
| 5 | 家族側「期待」のunder-recorded 構造（JPMS 0.34%） | 接続 | 4 | 4 | 5 | 13 | past→near |
| 6 | 創造性の慢性的盲点の意味（戦前4時代0%言及） | 密度 | 4 | 5 | 4 | 13 | past→near |
| 7 | far（2056-2080）構造的空白への応答 | 空白 | 4 | 3 | 5 | 12 | far |
| 8 | 集団協調性・社会的自立性の永遠ギャップ（126年） | 密度 | 4 | 4 | 4 | 12 | past→near |
| 9 | 非西洋認識論×活躍人材プロファイル | 接続 | 4 | 2 | 5 | 11 | mid→very-far |
| 10 | 世代間の物語と能力の同期問題（×Track 1/2連結） | 空白 | 4 | 2 | 5 | 11 | mid→far→very-far |

戦略構成: 密度4・空白4・接続2

## 6. 他トラックとの接続点

| 接続先 | 連結強度 | 共通テーマ | 連結提案内容 |
|---|---|---|---|
| Track 1 (FK) | **強** | 未来需要 / 世代間正義 | FK 23,274予測×ET 590需要のテーマ正規化、FK TOP10 #4 と本Track TOP10 #10 接続 |
| Track 2 (CLA) | **強** | 物語の交代期×言説-実績逆転 | CLA worldview/myth層 vs 本Track discourse/achiever層の補完統合。CLA 物語の交代期と本Track 令和逆転は層が異なるが整合 |
| Track 3 (megatrend) | **強** | R1生成AI / R17世代間正義 / R18非西洋 | 修正版18MT 5項目と本Track 19能力次元の細粒度マッピング |
| Track 9 (哲学) | **強** | very-far の19次元外拡張カテゴリ | xeno-ethics・posthuman_ethics・pluriverse 等の哲学概念精緻化 |
| Track 4 (Anthropology) | 中 | OCM × 非西洋型活躍人材像 | 本Track TOP10 #9 を Track 4 OCM分類で具体化 |
| Track 7 (学術知) | 中 | 能力次元体系の学術基盤 | 本Track 19次元のOECD/P21/UNESCO源泉と Track 7 学術DB系譜接続 |
| Track 8 (PESTLE) | 中 | 文化シグナルの活躍人材投影 | PESTLE 196,714ニュース→活躍人材像の文化的受容 |
| Track 5 (投資シグナル) | 弱-中 | start-up人材像 | 本Track 起業家精神スコア × Track 5 投資データ照合 |

## 7. 既知の限界（自己認識）

1. **far（2056-2080）構造的空白**：future_demand 0件。人材育成リードタイム25-50年制約。本Track単独では解消不能（V-10／構造的ギャップ）
2. **GF幼少期プロファイル4.3%カバー**：9,178偉人中397名のみ。「教育→活躍人物」を辿る本Track中核問いに致命的限界（V-11／構造的ギャップ）
3. **JPMS data_completeness 偏在**：832校中501校（60.2%）が30%未満。58,224証言は5%の高完成度学校に偏在の可能性（V-12／構造的ギャップ）
4. **era_school_alignment 36.5%未実装**：832校×8時代のうち実質的判定完了は528校×8時代のみ（V-13／要追跡）
5. **PST 3アーキタイプ未稼働**：pst.db persona_archetypes 全10件のうち arch_warrior/craftsman/introvert_thinker が0件、7アーキタイプに600偉人の93.8%（563件）が集中（V-14／要追跡）
6. **未来需要 Western中心バイアス**：OECD・WEF・McKinsey等のWestern機関中心、グローバルサウス薄い（V-15／要追跡）
7. **ET言説800件の出所偏在**：時代の進行とともに textbook → curriculum → business_proposal/white_paper へカテゴリシフト（V-16／問題なし開示済）

## 8. 後続トラックへの推奨

- **Track 1（FK）連携**：FK 23,274予測の細粒度カテゴリと本Track 19能力次元のマッピング。FK TOP10 #4「世代間正義と長期設計」と本Track TOP10 #10「世代間の物語と能力の同期問題」の Mサイン化。
- **Track 2（CLA）連携**：CLA「物語の交代期」と本Track「令和の言説-実績逆転」を、認識論層（CLA myth/worldview）と実証層（本Track discourse/achiever）の二層補完として Track 10 で統合。
- **Track 3（megatrend）連携**：修正版18MT R1（生成AI過剰的中）と本Track「reiwa cog_ai_collab 8.79＋AI協働言説-実績ギャップ -9.8」を Mサイン化。R18「非西洋認識論」と本Track TOP10 #9 接続。
- **Track 9（哲学）連携**：本Track「very-far 19次元外64件拡張カテゴリ（xeno-ethics 等）」を Track 9 哲学概念体系で精緻化。能力次元体系の再設計の理論基盤を提供。
- **GF 後続Wave**：幼少期プロファイルを 4.3%→30%以上に拡張すると、本Track「教育の階級的偏在」の定量精度が大幅向上。
- **JPMS 後続Wave**：data_completeness 30%未満の501校の補完で、家族側証言の under-recorded 問題に部分的解消。

## 9. ミラツク独自知見の候補

本Trackから他組織と差別化される独自知見の候補：

1. **「言説-実績ラグ構造」の発見**：126年×19能力次元のセル単位の差分計測は、政府機関・大手シンクタンクのフォーサイトには見られない独自視点。「教育の意図と結果のずれ」を時代横断で定量化することで、〈教育設計の盲点〉を構造的に可視化できる。これはミラツクの「対等な探究者」「暗黙知の形式知化」という三本柱と直接接続する。

2. **「令和の言説-実績逆転」の同定**：過去5時代の主流（言説が実績を後追い）から、令和（2019-2030）で初めて言説が実績を先取りする逆転構造を観察。これは時代の構造転換点の指標となりうる。Track 2 CLA「物語の交代期」、Track 3「過剰的中（生成AI）」と並ぶ「現在は方向転換期」の独立指標で、Mサイン候補。

3. **「人材育成リードタイム25-50年」をホライズン感度として導入**：4ホライズンに対して「direct feedback」「one-generation feedback」「beyond-feedback」「paradigm-redesign」のゾーン分けを提案。far が単なる予測の不確実性ではなく、生物学的・制度的に「直接フィードバック不能」のゾーンであることを明確化。

4. **「教育の階級的偏在」の構造提示**：GF 397幼少期のうちelite/royalty/nobility が63%以上を占める事実から、「偉人」概念そのものが階級バイアスを持つカテゴリである可能性を提示。ミラツクET「local_excellent_business 572／local_excellent_craft 69／local_excellent_culture 51／local_excellent_social 9＋agriculture_local 336」（合計1,037名・8%）は、〈無名の卓越者〉を含めた活躍人材像をミラツク独自視点として打ち出せる土台。

5. **「能力次元体系の枠不足」の発見**：very-far で future_demand が19能力次元の枠を超えた64件拡張カテゴリ（xeno-ethics・posthuman_ethics・pluriverse_cosmology・planetary_scale_systems_thinking等、全590件の10.8%）に流れる事実は、現行能力次元体系の「再設計需要」を定量的に示唆する（19次元マッチ526件 89.2%、拡張64件 10.8%）。64件は19次元中15次元集計値（35件）を上回り、「枠不足」という論旨は維持される。これは Track 9（哲学）連携で深化可能。

## 10. 出力ファイルパス

- analysis: `track6-talent-analysis.html`（約20,000字 / 図表6点 / L-01〜L-51）
- verification: `track6-talent-verification.html`（約11,500字 / 4カテゴリ × 22項目）
- report: `track6-talent-report.html`（約13,500字 / 図表6点 / 必須4要素含む）
- 引継ぎ書（このファイル）: `track6_handoff.md`

## 11. 統合リードへの申し送り

### 特に強調してほしい発見

- **「言説-実績ラグ」の126年継続構造**：6時代×19能力次元のセル単位差分計測は、領域策定プロジェクト全体の方法論的洞察として強調されるべき。Track 10 メタ統合レポートの「ミラツク独自知見」5-7件の有力候補。
- **「令和の言説-実績逆転」**：Track 2 CLA「物語の交代期」、Track 3「過剰的中」と並ぶ「現在は方向転換期」の独立指標。3 Tracks の独立合意は Mサイン候補。
- **「人材育成リードタイム」のホライズン感度**：4ホライズンの「直接フィードバック可能性」を一段深く読み解く視点。Track 10 で各Trackがどのホライズンに対して direct/one-generation/beyond/redesign のどれを担えるかを明示する設計。

### 他トラックとの矛盾候補

- **Track 1 FK が「2030近傍と2050+の二焦点」と診断、本Track が「mid主軸＋near副軸」**：両者は near と mid で並行整合だが、Track 1 は「2050+」（つまりmid+far+very-far の合算）として広めに、本Track は「far」を構造的弱点として狭めに切り出す違いがある。粒度差（FK レポート単位 vs 本Track 個人能力スコア単位）に由来する微差。Track 10 で粒度差を明示すれば解消（V-17）。
- **Track 2 CLA「強みCTL-1：V/G/S」と本Track「強みCTL-1：V/T/S」**：CTL-V と CTL-S が重複する。両Track は補完関係にあり、CLA は worldview/myth の認識論層、本Track は能力次元層と層が異なる。Track 10 で重複の意味解釈を明示要追跡（V-21）。
- **Track 3 R1「生成AI過剰的中」と本Track「AI協働ギャップ -9.8（言説過剰）」**：両者は内容的に整合的だが、本Track は「実績側でまだ薄い」という独自診断を加える。Track 10 で粒度差明示要追跡（V-19）。

### Track 10 中核問い

**「教育の意図と結果の126年ラグは、現在初めて逆転しつつあるのか、それとも空文化に向かうのか」**

これを領域策定プロジェクトの教育・人材設計の中核的問いとして提案する。Track 1（世代間正義）×Track 2（物語の交代期）×Track 3（過剰的中）と直結する。

### Track 11以降への送り事項

- 「言説-実績ラグ構造」を領域策定プロジェクトの標準枠組みとして採用するか、Track 11 で再評価。
- 「人材育成リードタイム」をホライズン感度の標準次元として採用するか、Track 11 で再評価。
- GF 後続Wave で幼少期プロファイル拡張が完了したら、本Track の「教育の階級的偏在」を再分析する仕組み。

## 12. 統合用連結ID（_PROTOCOLS.md 6.2 標準フォーマット）

- 主軸DB: era_talents.db + great_figures.db + jpms_v2.db + pst.db
- 強みホライズン: past 1868-2025（独自）＋ mid 2036-2055（主強み・220需要）＋ near 2026-2035（副強み・245需要）
- 弱みホライズン: far 2056-2080（人材育成射程外で0需要）＋ very-far 2081-2100（19次元外64件拡張カテゴリ、526件 89.2%が19次元マッチ）
- 強みCTL-1: V（価値観・倫理・文化）／T（技術・知）／S（社会・人口・コミュニティ）
- 弱みCTL-1: Eco（経済・産業・労働）／Env（環境・気候）／G（ガバナンス・制度）
- 補完が必要な領域: Track 1（細粒度予測テーマ展開）／Track 4（非西洋型活躍人材像）／Track 9（19次元外哲学概念精緻化）／GF後続Wave（幼少期4.3%→30%+）／JPMS後続Wave（30%未満校の補完）
- 提供できる補完: Track 1（言説-実績ラグ構造）／Track 2（worldview vs 能力次元の対応）／Track 3（18MT 5項目の能力次元対応）／Track 4（教育階級偏在の定量基盤）／Track 9（言説-実績ラグの構造的意識化）／Track 10（人材育成リードタイム・3系列ラグ・教育階級偏在の3独自視点）

## 13. 添付：主要集計クエリ一覧

### L-01: ET achievers by primary_era
```sql
SELECT primary_era_id, COUNT(*) FROM achievers GROUP BY primary_era_id;
-- meiji 1412 / taisho 1196 / showa_pre 1105 / showa_post 1911 / heisei 2952 / reiwa 4382
```

### L-04: ET achiever_capabilities by capability
```sql
SELECT capability_id, COUNT(*), AVG(score) FROM achiever_capabilities GROUP BY capability_id;
-- 19能力次元別の集計。soc_interpersonal 3450(7.20), cog_creativity 3419(8.25),
-- cog_systems 3261(7.48), age_resilience 2896(7.51) 他
```

### L-05: ET era × capability avg_score（実績マトリクス）
```sql
SELECT a.primary_era_id, ac.capability_id, COUNT(*), AVG(ac.score)
FROM achiever_capabilities ac JOIN achievers a ON a.id=ac.achiever_id
GROUP BY a.primary_era_id, ac.capability_id;
-- 6時代 × 19能力次元 = 114セル。詳細はanalysis図表4。
```

### L-06: ET future_demands × era × capability
```
future_2030: cog_critical 27, cog_ai_collab 24, soc_interpersonal 23, cog_systems 23, cog_info 23
future_2050: cog_systems 21, val_eco 20, age_resilience 18, cog_critical 16, age_social_change 15
future_2100: val_eco 6, cog_systems 6, val_collective 5, soc_interpersonal 5, cog_critical 5 + 拡張64件
```

### L-09: ET era_discourses × era × capability（言説）
```
meiji: age_social_autonomy 19, val_collective 16, val_traditional 15
taisho: age_social_autonomy 13, soc_interpersonal 12, val_collective 11
showa_pre: val_collective 19, val_traditional 17, age_resilience 17
showa_post: age_social_autonomy 17, val_tolerance 15, age_meta_learning 15
heisei: age_meta_learning 20, cog_info 15, cog_critical 14
reiwa: age_meta_learning 15, cre_cross_domain 11, cog_info 11, cog_ai_collab 10
```

### L-12: ET gap_insights 7件全件
```
1. l1_l2_gap: showa_pre x cog_critical (conf 6)
2-6. cross_era: 起業家精神/批判的思考/システム思考/学習戦略/社会変革志向 普遍能力 (conf 8)
7. era_to_future: 未来固有能力 AI協働リテラシー (conf 7)
```

### L-20-21: GF childhood social_class & formal_education
```
social_class: royalty 108 (27.2%), elite_professional 94 (23.7%), unknown 51, nobility 50 (12.6%),
  skilled_artisan 45, merchant 26, peasant 15, slave 5, clergy 3 = 397
formal_education: elite 164 (41.3%), classical 68, unknown 55, mixed 38, practical 35,
  religious 27, none 7, self_taught 3 = 397
```

### L-23-24a: JPMS schools & testimonials
```
schools_v2 = 832
testimonials_v2 = 58,224 (student_current 21440, principal 14598, student_alumni 10011,
  teacher 9265, parent 2907, chairperson 3)
```

### L-45: JPMS testimonials family-related keywords
```
parent: 家族19/親102/期待10/卒業124/リーダー1/社会58/自立5 (total 2907)
parent「期待」 10/2907 = 0.34% （under-recorded）
principal「期待」 96/14598 = 0.66%
principal「社会」 1049/14598 = 7.18%
```

### L-48: ET era × capability 完全マトリクス
```
6時代 × 19能力次元 = 114セル中、n>=5 のセルは100セル
各時代TOP-5 (avg_sc, n>=30):
- meiji: 創造性 8.27, 起業家精神 8.21, 伝統文化尊重 8.06, 論理的思考 8.00, 異分野統合志向 7.83
- taisho: 起業家精神 8.87, 社会変革志向 8.41, 社会的自立性 8.40, 論理的思考 8.23, エコロジカル 8.00
- showa_pre: 伝統文化尊重 8.58, 起業家精神 8.35, 情報リテラシー 8.33, 論理的思考 8.15, 創造性 8.13
- showa_post: 起業家精神 8.88, 論理的思考 8.82, 情報リテラシー 8.46, 創造性 8.10, 伝統文化尊重 8.08
- heisei: 創造性 8.71, 伝統文化尊重 8.37, 論理的思考 8.36, 起業家精神 8.15, OECD変革 8.00
- reiwa: AI協働 8.79, 情報リテラシー 8.76, 論理的思考 8.71, 数学的リテラシー 8.61, 創造性 8.48
```

### L-49: JPMS era_school_alignment
```
each era: high 528, unknown 23 = 551 (時代×8 = 4408)
unknownは「文化スコア未算出のため中立評価」（36.5% 未実装）
```

### L-51: JPMS outcome_dim_v2 全101件
```
cluster: cognitive 約25 / social_emotional 13-14 / values_morals 13-14 / agency_civic 13 /
  wellbeing 13 / creative_excellence 13 / market_management 14 = 101
framework: OECD/CASEL/PERMA/P21/PISA/JP/Cox/Simonton/Lerner/Collins/Christensen等
```

---

最終更新: 2026-05-09
作成: Track 6 リード
参照: track6-talent-{analysis|verification|report}.html
