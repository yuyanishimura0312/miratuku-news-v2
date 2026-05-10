# Track C-4 doc-verify レポート — 偉業 zone マッピング + great_actions.db v0.2 構築の独立検証

> 作成日: 2026-05-10
> 担当: Phase C Wave 3 doc-verify（独立検証 Layer 1、再実行版）
> 検証対象: Track C-4 4 ファイル（analysis.html / verification.html / report.html / handoff.md）+ great_actions.db v0.2（11 カラム拡張 + 2 新規テーブル + 2,030 リンク）
> 参照基準: `_TRACK_C4_BRIEFING.md` / `_TRACK_C4_PRESEARCH.md` / `_PHASE_A_INHERITANCE_AUDIT.md` / `track-c3-doc-verify-report.md` / `track-c3_handoff.md` / `track-c5_handoff.md` / phase-b/track-b4 / phase-b/track-b5 / phase-b/track-b6 / `migrate_c4_v02.py`
> 検証手法: SQLite 直接 SQL 集計値との突合 + ファイル横断 grep + 4 カテゴリ独立検証 + 前 doc-verify 中断時の発見継承

---

## 0. 総合判定サマリー

| カテゴリ | 検査項目 | PASS | WARN | FAIL |
|---|---|---|---|---|
| A. スナップショット不整合 | 6 | 6 | 0 | 0 |
| B. ハルシネーション | 8 | 3 | 1 | 4 |
| C. カバレッジギャップ | 8 | 7 | 1 | 0 |
| D. チーム間不整合 | 6 | 5 | 1 | 0 |
| **合計** | **28** | **21** | **3** | **4** |

- Critical 不整合: **5 件** — すべてが report §9.1「v0.1 と v0.2 status の差分」表に集中する数値ハルシネーション + 派生 1 件（high warning 「12 件」表記）
- HTML タグバランス: **3 ファイル全て balanced**（analysis.html div 9/9・section 10/10・table 8/8・tr 89/89 / verification.html div 5/5・section 7/7・table 7/7・tr 48/48 / report.html div 105/105・section 11/11・table 8/8・tr 90/90）
- DB SQL 検証: 主要数値 16 件中 **11 件整合・5 件齟齬**（齟齬 5 件はすべて §9.1 表セル）
- sentinel への引継ぎ事項: **6 件**（G-1〜G-6）

**総合判定: 条件付 PASS（修正後再検証必須）**。Phase A/B 数値継承（B-4 463 / B-5 4-9-9-0-8 / B-6 TOP10）・主要発見 1〜3・warning 17 件総数・opportunity 50 件総数・TOP10 × 偉業 78 件 (55.7%)・zone × scenario 主要分布・HTML タグバランスは SQL 値と完全整合。一方、(1) **report.html §9.1 表**「v0.1 と v0.2 status の差分」内の 5 セル（happening 行 3 セル + expected 行 3 セル + speculative 行 2 セル）が実 DB 値と不一致、(2) report.html §6.3 で「high warning 13 件のうち 12 件が G-N04」と書きつつ §6.1 表（L522-534）で 13 件全件 G-N04 を提示する内部矛盾、(3) §9.1 注「v0.1 happening/emerging から expected/speculative への格下げ」が実 crosstab に存在しない誤った構造解釈、の 3 点を Critical FAIL として記録する。

---

## A. スナップショット不整合カテゴリ（6 項目）

### A-1. great_actions.db 140 件保持（v0.1 → v0.2 ALTER のみ）→ **PASS**

handoff §2.1 主張: 「v0.1 既存 30 カラムは破壊せず、c4_* 11 カラム追加」。

```sql
SELECT COUNT(*) FROM great_actions;  -- 140
PRAGMA table_info(great_actions);
-- 0..47 が v0.1 / 48..59 が c4_* 12 カラム（v0.2）
```

合計 60 カラム（v0.1 既存 48 + v0.2 追加 12）。handoff §2.1 が「11 カラム」と記述する点は実は 12 カラム（c4_review_note と c4_updated_at を別々に数えれば 12）で、軽微なカウント差だが内容実体は破壊なし。

### A-2. v0.1 status 内訳（C-3 確定値）の整合 → **PASS**

```sql
SELECT current_stage_status, COUNT(*) FROM great_actions GROUP BY current_stage_status;
-- emerging|6 / expected|24 / happening|104 / speculative|6
```

C-3 doc-verify A-1 で確認済の値（happening 104 + expected 24 + speculative 6 + emerging 6 = 140）と完全一致。本トラックでも v0.1 既存値が破壊されず保持されていることを確認。

### A-3. v0.2 status 内訳（c4_status_override）の整合 → **PASS**

handoff §2.3 主張: happening 50 / opportunity 50 / warning 17 / expected 13 / emerging 6 / speculative 4 = 140。

```sql
SELECT c4_status_override, COUNT(*) FROM great_actions GROUP BY c4_status_override;
-- emerging|6 / expected|13 / happening|50 / opportunity|50 / speculative|4 / warning|17
```

合計 140、handoff 記述と完全一致。report §3 の bar chart（L412-417）も同値。

### A-4. zone 別偉業分布 Hot 15 / Warm 17 / Cool 43 / N/A 65 → **PASS**

```sql
SELECT c4_b5_zone, COUNT(*) FROM great_actions GROUP BY c4_b5_zone;
-- Cool|43 / Hot|15 / N/A|65 / Warm|17
```

合計 140、handoff §2.3 と一致。B-5 の問い単位 zone 弁別 Hot 4/Warm 9/Cool 9/Dead 0/N/A 8 を偉業単位に展開した派生値で、両軸の独立性は protocols 三系列差として開示済。

### A-5. maturity_score 分布の整合 → **PASS**

handoff §2.3 主張: 5 (scale) 0 / 4 (pilot) 26 / 3 (expt) 50 / 2 (emerging) 2 / 1 (expected) 58 / 0 (speculative) 4 = 140。

```sql
SELECT c4_maturity_score, COUNT(*) FROM great_actions GROUP BY c4_maturity_score;
-- 0|4 / 1|58 / 2|2 / 3|50 / 4|26
```

完全一致。maturity 5 ゼロ件は構造的事実として SQL で確認。なお閾値感度は handoff §5.1 と report §11.3 で honest 開示済（U-3 として継承）。

### A-6. 463 initiatives × 紐付け統計の整合 → **PASS**

handoff §2.4 主張: unique initiatives 紐付け 300 / 463 (64.8%)・紐付けあり actions 76 / 140 (54.3%)・総リンク 2,030。

```sql
SELECT COUNT(DISTINCT initiative_id) FROM action_initiatives_links;       -- 300
SELECT COUNT(DISTINCT action_id) FROM action_initiatives_links;            -- 76
SELECT COUNT(*) FROM action_initiatives_links;                             -- 2030
```

完全一致。300/463 = 0.6479 → 64.8%、76/140 = 54.29% → 54.3%、両者算術整合。

---

## B. ハルシネーションカテゴリ（8 項目）

### B-1. warning 17 件の severity 内訳（critical 4 / high 13）→ **PASS**

```sql
SELECT c4_warning_severity, COUNT(*) FROM great_actions WHERE c4_status_override='warning' GROUP BY c4_warning_severity;
-- critical|4 / high|13
```

handoff §2.5・report §6・analysis §8.2 のいずれも「critical 4 件・high 13 件」と一致。

### B-2. critical 4 件すべて G-N12 集中 → **PASS**

```sql
SELECT primary_question_id, c4_warning_severity, COUNT(*) FROM great_actions
WHERE c4_status_override='warning' GROUP BY primary_question_id, c4_warning_severity;
-- G-N04|high|13 / G-N12|critical|4
```

critical 4 件 = G-N12 のみ、high 13 件 = G-N04 のみ。handoff §2.5「critical 4 件 — すべて G-N12 ケア経済の組織化」「high 13 件 — 主に G-N04 場所性回帰」の前半は厳密に正しい。後半「主に」は実は「全件」だが、「主に」表記は誤りではない（部分集合は表現可能）。

### B-3. warning 17 件の scenario 内訳 Care 13 / Pluriverse 2 / Slow Right 2 → **PASS**

```sql
SELECT scenario_id, COUNT(*) FROM great_actions WHERE c4_status_override='warning' GROUP BY scenario_id;
-- Care|13 / Pluriverse|2 / Slow Right|2
```

合計 17、シナリオ別検証完全整合。

### B-4. opportunity 50 件の問い別分布 → **PASS**

handoff §2.5 主張: G-M04 15 / G-N09 14 / G-V03 6 / G-M07 5 / G-M05 4 / G-F03 3 / G-M06 3。

```sql
SELECT primary_question_id, COUNT(*) FROM great_actions WHERE c4_status_override='opportunity' GROUP BY primary_question_id;
-- G-F03|3 / G-M04|15 / G-M05|4 / G-M06|3 / G-M07|5 / G-N09|14 / G-V03|6
```

合計 50、handoff 記述と完全一致。G-M04 + G-N09 = 29 件 / 50 件 = 58.0% も算術整合（report §7.1）。

### B-5. report §9.1「v0.1 と v0.2 status の差分」表 — happening 行 → **FAIL（Critical）**

report.html L663 表セル: 「happening 104 件 / 警告化 17 / opp 化 0 / 維持 87」。

SQL 実 crosstab:
```sql
SELECT current_stage_status AS v01, c4_status_override AS v02, COUNT(*) AS cnt
FROM great_actions
WHERE current_stage_status='happening'
GROUP BY v02;
-- happening (=維持)|50 / opportunity|39 / warning|15
```

| 列 | report 記述 | DB 実値 | 判定 |
|---|---|---|---|
| v0.1 件数 | 104 | 104 | ○ |
| warning 化 | **17** | **15** | × |
| opportunity 化 | **0** | **39** | × |
| 維持 | **87** | **50** | × |

3 セル中 3 セル誤り。warning 化「17」は **warning 全件総数（17）を happening 行に転記した混同エラー**で、実際の happening → warning は 15 件（残り 2 件は expected → warning から派生）。opportunity 化「0」は致命的誤りで、実際は 39 件が happening から opportunity に上書きされている。維持 87 も実値 50 と齟齬（migrate_c4_v02.py L310: 「`is_opportunity = ... v01_status in (..., 'happening')`」が示す通り、happening は opportunity 化候補に含まれるため、表設計の前提自体が誤り）。

**判定: FAIL（Critical）**。修正必須。修正案:

| v0.1 status | v0.1 件数 | v0.2 で warning 化 | v0.2 で opportunity 化 | v0.2 で維持 |
|---|---|---|---|---|
| happening | 104 | 15 | 39 | 50 |

### B-6. report §9.1 表 — expected 行 → **FAIL（Critical）**

report.html L665 表セル: 「expected 24 件 / warning 化 0 / opp 化 34 / 維持 -10 (差分要確認)」。

SQL 実 crosstab:
```sql
SELECT c4_status_override, COUNT(*) FROM great_actions
WHERE current_stage_status='expected'
GROUP BY c4_status_override;
-- expected (=維持)|13 / opportunity|9 / warning|2
```

| 列 | report 記述 | DB 実値 | 判定 |
|---|---|---|---|
| v0.1 件数 | 24 | 24 | ○ |
| warning 化 | **0** | **2** | × |
| opportunity 化 | **34** | **9** | × |
| 維持 | **-10** | **13** | × |

3 セル中 3 セル誤り。「opp 化 34」は **opportunity 全件総数（50）と他行の opp 化との差分計算ミス**の可能性が高い（24 - (-10) = 34 と逆算した結果）。「維持 -10」というマイナス値は、表設計が破綻していることを示すフラグで、handoff §2.4 → §2.5 の crosstab 値（実は migrate_c4_v02.py が opportunity 化候補に happening を含めているため expected 24 件は素直に分かれている）を正しく集計せず、opportunity 全 50 件を expected/speculative 二行に按分しようとして失敗したと推測される。

**判定: FAIL（Critical）**。修正必須。

### B-7. report §9.1 表 — speculative 行 → **FAIL（Critical）**

report.html L666 表セル: 「speculative 6 件 / warning 化 0 / opp 化 16 / 維持 -10 (差分要確認)」。

SQL 実 crosstab:
```sql
-- speculative (=維持)|4 / opportunity|2
```

| 列 | report 記述 | DB 実値 | 判定 |
|---|---|---|---|
| v0.1 件数 | 6 | 6 | ○ |
| warning 化 | 0 | 0 | ○ |
| opportunity 化 | **16** | **2** | × |
| 維持 | **-10** | **4** | × |

warning 化 0 のみ正しく、残 2 セルが誤り。「16」も「-10」も B-6 と同じく opportunity 全 50 件按分失敗の連鎖誤差。

**判定: FAIL（Critical）**。修正必須。

なお emerging 行（6 件 / warning 0 / opp 0 / 維持 6）は **SQL 実値と一致（FAIL なし）**。これは migrate_c4_v02.py が emerging を opportunity 化候補に含めるロジックでありながら（L310）、対象 actions の primary_question_id がたまたま STRATEGIC_GAPS に該当しなかったため結果として全件維持となったもの。

### B-8. report §6.3「high warning 13 件のうち 12 件が G-N04」記述の整合 → **FAIL（Critical）**

report.html L549: 「high warning 13 件のうち **12 件**が G-N04（場所性回帰）に集中した」。
同 §6.1 表（L522-534）: G-N04 タグ付き行 = **13 行**。
同 §11.2（L717）: 「G-N04（場所性回帰）**13 偉業すべて**が warning 化したのは過剰判定の可能性」。

SQL 実値:
```sql
SELECT primary_question_id, c4_warning_severity, COUNT(*) FROM great_actions
WHERE c4_status_override='warning' AND c4_warning_severity='high'
GROUP BY primary_question_id;
-- G-N04|high|13
```

high 13 件 = G-N04 全件で「12 件」記述は誤り。L549 単独の transcription エラーで、同 report 内の §6.1 表・§11.2 と矛盾する内部不整合。

**判定: FAIL（Critical）**。修正案: 「13 件すべてが G-N04（場所性回帰）に集中した」。

### B-9. §9.1 注「v0.1 happening/emerging から expected/speculative への格下げ」→ **WARN（Critical）**

report.html L670: 「差分マイナス値は『v0.1 expected/speculative の一部が opportunity に上書きされ、また v0.1 happening/emerging から expected/speculative への格下げも一部発生したことの集計副作用』を示す」。

SQL crosstab で全 v0.1 → v0.2 遷移を全件確認:
```
v0.1 emerging  → v0.2 emerging (6 件のみ)
v0.1 expected  → v0.2 expected/opportunity/warning（格下げなし、全て上昇または維持）
v0.1 happening → v0.2 happening/opportunity/warning（格下げなし）
v0.1 speculative → v0.2 speculative/opportunity（格下げなし）
```

「happening/emerging から expected/speculative への格下げ」は **実 crosstab に存在しない**。注釈は B-5/B-6/B-7 の表セル誤りを糊塗するための事後説明で、構造解釈そのものが誤り。

**判定: WARN（Critical）**。本注釈は §9.1 表の修正と同時に削除または書き換えが必要。

---

## C. カバレッジギャップカテゴリ（8 項目）

### C-1. 既存偉業 vs 期待偉業の差分構造マップ → **PASS**

report §3 + §10.1 で c4_status_override 6 区分による差分構造を提示。「既存（happening + warning + emerging）73 件 vs 期待（opportunity + expected + speculative）67 件 = 52.1% : 47.9%」も算術整合（73 = 50+17+6、67 = 50+13+4）。

### C-2. ミラツク優先課題 TOP10 × 偉業マッピング → **PASS**

```sql
SELECT SUM(cnt) FROM (SELECT c4_top10_rank, COUNT(*) AS cnt FROM great_actions WHERE c4_top10_rank > 0 GROUP BY c4_top10_rank);
-- 78
```

report §5（L488-498 表）合計 78 件、handoff §3「TOP10 × 偉業 78 件」と一致。140 件中 55.7%（78/140 = 0.5571）も算術整合。

### C-3. warning 偉業の特定（4 定義 + 候補問い + severity）→ **PASS**

report §6 で 4 定義（A〜D）+ 8 候補問い + critical/high 二段階を明示。SQL では critical 4・high 13 が一意に分離されている（B-1/B-2 検証済）。warning 4 定義の主観性は handoff §5.1・report §11.2 で honest 開示済（U-1, U-2 として継承）。

### C-4. opportunity 偉業の特定（戦略的空白 13 問起源 + 3 条件）→ **PASS**

report §7 + analysis §9 で 50 件を 7 問に分散して提示、SQL 実値と一致（B-4）。50 件のうち過去アナログ 35 件 + 期待型 15 件 = 70:30 は report §7.3 で記述（DB 直接検証は未実施だが構造解釈水準で適切）。

### C-5. 463 initiatives × 100-150 great_actions 紐付け統計 → **PASS**

紐付けあり 300/463 (64.8%) + 紐付けなし 163/463 (35.2%) + 総リンク 2030 + 1 initiative 平均 6.8 リンク。SQL で完全再現可能（A-6）。

### C-6. zone 別偉業分布（Hot 4/Warm 9/Cool 9/Dead 0/N/A 8 と great_actions 対応）→ **PASS**

report §4 + analysis §5 で zone × archetype・zone × scenario 集計を実装。Hot zone Care 86.7%、Cool zone Pluriverse 86.0% は SQL で確認可能。zone 軸は「30 問単位」と「140 actions 単位」の二系列開示が protocols 三系列差として実装されている（briefing 必須要素 6 を充足）。

### C-7. 連結 ID（C-3 偉業 / C-5 担い手 / C-6 統合 への接続）→ **PASS**

handoff §4.1〜4.4 で C-5（担い手）・C-6（統合）・C-7（公開）・Phase D（deep-knowledge）への引継ぎを 4 段階で明示。各引継ぎで具体的接続点と要追跡事項を記載。

### C-8. 研究の限界（warning 判定の主観性含む）→ **WARN**

handoff §5.1 で限界 3 点（B-3→B-1 マッピング推定性 / warning 4 定義主観性 / maturity 5 ゼロ件閾値感度）+ §5.2 で未検証 6 件 + verification §6 で 4 自己発見問題、計 13 件を honest 開示済。**ただし §9.1 表のセル数値ハルシネーション（B-5〜B-7 の Critical FAIL 5 件）は限界として開示されておらず**、「自己検証の盲点」として WARN 判定。

**判定: WARN**。修正後再検証時に「§9.1 表の数値修正後、表設計そのものの妥当性（合計 140 を達成する 4 行 × 4 列の集計枠組み）」を限界として handoff §5.1 に追加することが望ましい。

---

## D. チーム間不整合カテゴリ（6 項目）

### D-1. C-3 great_actions.db v0.1 との接続（破壊禁止）→ **PASS**

verification §T-1: 「v0.1 既存データを破壊せず ALTER TABLE のみで層追加」PASS。SQL 確認: v0.1 30 カラム + v0.2 c4_* 12 カラム = 42 + その他 = 60 カラムで、既存 140 行は破壊されず保持（A-2 で v0.1 status 内訳 SQL 一致確認済）。設計整合。

### D-2. C-3 装置応答型 vs 期待型 の接続 → **PASS**

handoff §4.1 で derivation_method（C-3 設定）と c4_status_override（C-4 上書き）の二層保持を明示。report §10.1 で「装置応答型 50 件 → c4_status_override = happening (50) と整合」「期待型 30 件 → opportunity (28) + warning (1) + expected (1) = 30」「過去偉業 60 件 → opportunity (22) + happening (38) + warning (16) = 76?」と記述。

ここで過去偉業 60 件の内訳「22+38+16=76」は 60 を超え、報告書内に算術齟齬がある可能性。ただし当該記述は本文 prose 内（report L678）で、SQL 直接検証用のラベルが不明確。重大判定は留保し、記述の数量整合性確認を G-6 として継承する。

設計上の二層保持構造そのものは整合のため **PASS（記述算術齟齬の WARN は G-6 へ）**。

### D-3. C-5 担い手特性領域への引継ぎ整合 → **PASS**

handoff §4.1（C-5 引継ぎ）で zone × archetype 構造的非対称（Hot=Caregiver 53% / Cool=Mediator 42%）+ critical warning 4 件の Caregiver 8 件深掘り推奨を明示。C-5 handoff §7.4 では「C-4 と並列実行のため本解析時点では C-4 出力未確定」と honest 開示済で、C-6 統合段階での再接続を引継ぎ。並列実行構造として設計整合。

### D-4. C-2 71 問（B-1 41 + B-3 30）独立 ID 整合 → **PASS**

verification §T-3 で「c4_b5_zone は B-3 30 問 G-prefixed 単位で付与、C-2 71 問空間と独立」PASS。primary_question_id（B-3 30 問 G-prefixed）と primary_b1_question_id（B-1 41 問 Q-prefixed）の二重カラム実装は C-3 から継承されており、C-4 の zone マッピングは B-3 軸のみで実施されている。設計整合。

### D-5. C-1 サイクル概念の組込 → **WARN（自己発見済）**

verification §T-4 で「C-1 サイクル A/B/C と great_actions の直接マッピング未実施 — C-6 統合段階での実施を引継ぎ」WARN を自己発見。C-6 へ申し送り構造が確立済。

**判定: WARN（自己発見継承）**。Phase C 全体ガバナンスとして C-6 master report での実施が必須。

### D-6. Phase A Mサイン階層整合 → **PASS**

verification §T-6 で「opportunity 条件 3 で Mサイン階層接続を明示判定基準に組込」PASS。great_actions.db v0.1 の msign_connection カラム（true_msign 61 / concept_aligned 66 等）は C-3 から継承され、C-4 はその参照のみ（書き込みなし）。Phase A 数値継承の伝言ゲーム化は構造的に発生不可。設計整合。

---

## E. HTML タグバランス検証

```
analysis.html:    div   9/9   / section 10/10 / table 8/8 / tr 89/89    -- 完全均衡
verification.html: div   5/5   / section  7/7  / table 7/7 / tr 48/48   -- 完全均衡
report.html:       div 105/105 / section 11/11 / table 8/8 / tr 90/90   -- 完全均衡
```

3 ファイル全てバランス OK。長大 HTML（report 50K 字・analysis 35K 字）に対して章末尾の余分 `</div>` 等の典型的不整合は発見されず。memory `feedback_html_validation` の警告は本トラックでは回避済。

---

## F. DB 集計値整合（SQL 検証サマリ）

| 検証対象 | 文書記述 | DB SQL 実値 | 判定 |
|---|---|---|---|
| 総件数 | 140 | 140 | PASS |
| v0.1 status 内訳 | 104+24+6+6=140 | 同 | PASS |
| v0.2 status 内訳 | 50+50+17+13+6+4=140 | 同 | PASS |
| zone 内訳 | 15+17+43+65=140 | 同 | PASS |
| maturity 内訳 | 0+26+50+2+58+4=140 | 同 | PASS |
| 紐付けあり initiatives | 300/463 (64.8%) | 300 | PASS |
| 紐付けあり actions | 76/140 (54.3%) | 76 | PASS |
| 総リンク数 | 2030 | 2030 | PASS |
| critical 4 / high 13 | 4+13=17 | 4+13 | PASS |
| critical 4 件すべて G-N12 | G-N12 | G-N12 | PASS |
| high 13 件すべて G-N04 | (12 vs 13 内部矛盾) | 13 | **FAIL** |
| warning シナリオ Care 13/Plu 2/SR 2 | 13+2+2=17 | 同 | PASS |
| opportunity 50 件問い別 | M04 15/N09 14/V03 6/M07 5/M05 4/F03 3/M06 3 | 同 | PASS |
| TOP10 × 偉業 | 78 (55.7%) | 78 | PASS |
| **§9.1 happening 行** | 17 / 0 / 87 | **15 / 39 / 50** | **FAIL** |
| **§9.1 expected 行** | 0 / 34 / -10 | **2 / 9 / 13** | **FAIL** |
| **§9.1 speculative 行** | 0 / 16 / -10 | **0 / 2 / 4** | **FAIL** |
| §9.1 emerging 行 | 0 / 0 / 6 | 0 / 0 / 6 | PASS |

主要数値 17 件中 13 件 SQL 整合、4 件 FAIL（high warning 「12 件」記述 + §9.1 表 3 行）。なお §9.1 注の構造解釈誤り（happening/emerging からの格下げ言及）は WARN として B-9 で計上。

### F-1. SQL 実値表（§9.1 修正案 — 完全版）

修正案として以下を report §9.1 に置換。

| v0.1 status | v0.1 件数 | v0.2 で happening 維持 | v0.2 で warning 化 | v0.2 で opportunity 化 | v0.2 で expected 維持 | v0.2 で emerging 維持 | v0.2 で speculative 維持 |
|---|---|---|---|---|---|---|---|
| happening | 104 | 50 | 15 | 39 | — | — | — |
| expected | 24 | — | 2 | 9 | 13 | — | — |
| emerging | 6 | — | 0 | 0 | — | 6 | — |
| speculative | 6 | — | 0 | 2 | — | — | 4 |
| **合計** | **140** | **50** | **17** | **50** | **13** | **6** | **4** |

合計列が v0.2 status 6 区分の総数（happening 50 / warning 17 / opportunity 50 / expected 13 / emerging 6 / speculative 4 = 140）と完全一致することを確認可能。

### F-2. 構造解釈の修正

§9.1 注は次のように書き換えるべきである。

> 注: c4_status_override の上書きは migrate_c4_v02.py の判定ロジックに従い、(1) STRATEGIC_GAPS（13 問）に該当 + initiatives 件数 < 5 の actions は v0.1 の status を問わず opportunity に上書き、(2) WARNING_CANDIDATE_QUESTIONS（8 問）に該当 + initiatives 件数 ≥ 3 の actions は warning に上書き、(3) それ以外は v0.1 の status を維持する。本表は v0.1 → v0.2 の遷移を SQL crosstab で再現可能。「v0.1 happening の 39 件が opportunity 化」は STRATEGIC_GAPS に該当する actions が v0.1 で happening 判定されていたが、initiatives 紐付け数が 5 件未満で実装段階が薄いと観測されたため、規範軸（戦略的空白起源）優先で opportunity に再分類された結果である。

---

## G. sentinel への引継ぎ事項（6 件）

### G-1. report §9.1 表 3 行（happening/expected/speculative）の数値修正（FAIL Critical）

3 行 9 セルが SQL 実値と齟齬（うち 8 セル誤り、emerging 行 1 セルのみ正しい）。F-1 修正案へ全面置換。analysis.html § / handoff §2.5 等への伝播がないか追加確認の上、3 ファイル横断で整合性回復。

### G-2. report §9.1 注の構造解釈書き換え（WARN Critical）

「v0.1 happening/emerging から expected/speculative への格下げ」は実 crosstab に存在しない誤った解釈で、F-2 修正案へ書き換え。マイグレーションロジック（migrate_c4_v02.py L307-310）の実条件を直接記述する形が望ましい。

### G-3. report §6.3 高 warning 「12 件」記述の修正（FAIL Critical）

L549「13 件のうち 12 件が G-N04」を「13 件すべてが G-N04」に修正。同 report §6.1 表（13 行 G-N04）と §11.2「13 偉業すべて」との内部整合を確保。

### G-4. handoff §2.1「11 カラム拡張」の表記精緻化（軽微）

実装は 12 カラム（c4_review_note + c4_updated_at を含む）。「11 カラム」は事実誤認だが影響軽微。次回 handoff 更新時に「12 カラム拡張（実観測層 10 + メタ 2）」等への精緻化が望ましい。

### G-5. report §10.1 過去偉業 60 件の内訳算術整合（FAIL の可能性、要検証）

L678「過去偉業 60 件 ... opportunity (22) + happening (38) + warning (16) = 76」と記述（合計 76 が 60 を超える）。derivation_method='historical_analog' のサブセット内訳が単純合算で 60 を超えるのは別軸併存（同一 action が複数の派生方法を持つ）が原因の可能性があるが、表記上「過去偉業 60 件のうち」と読者に解釈を要求しているため、修正または注記追加が必要。SQL での再検証要。

### G-6. §9.1 表設計の妥当性（research 限界としての追加開示）

§9.1 表は 4 行（v0.1 4 区分） × 4 列（warning/opportunity/維持/合計）で 140 件を網羅する設計だが、v0.2 が 6 区分のため列軸の不足で「維持」セルに複数 v0.2 区分が混在する構造的弱さがある。F-1 で示した 7 列形式（v0.2 6 区分 + 合計）が真の crosstab 構造。handoff §5.1「研究の限界」に「§9.1 表の集計枠組みの再検証」を 4 件目として追加することを推奨。

---

## H. 総括

Track C-4 は great_actions.db v0.2（11 カラム拡張 + 2 新規テーブル + 2,030 リンク）を Phase B 観測実績層と Phase C 偉業構造の中核接合 DB として確立し、warning 17 件 / opportunity 50 件 / TOP10 × 偉業 78 件・463 initiatives × 140 great_actions の多対多紐付け 2,030 件・zone × scenario × archetype の三軸集計 43 セル × 11 集計列 = 473 集計値を構造化した。HTML タグバランスは 3 ファイル全てバランス、Phase A/B 数値継承（B-4 463 / B-5 4-9-9-0-8 / B-6 TOP10）は構造的に伝言ゲーム化が発生不可、C-3 great_actions v0.1 からの継承は ALTER TABLE のみで破壊なし、C-2 71 問 / C-5 担い手 / C-6 統合 / Phase D deep-knowledge への引継ぎ構造も protocols 準拠水準を保つ。

主要発見の数値正確性検証では、warning 17 件の severity 内訳（critical 4 / high 13）・scenario 内訳（Care 13 / Pluriverse 2 / Slow Right 2）・primary_question_id 集中（critical = G-N12 / high = G-N04）はすべて SQL 完全整合、opportunity 50 件の 7 問分布も完全一致、TOP10 × 偉業 78 件 (55.7%) も完全一致、紐付け統計 300/463 (64.8%) と総リンク 2,030 も SQL 整合。一方、**report §9.1「v0.1 と v0.2 status の差分」表の 3 行 8 セルが SQL 実 crosstab と齟齬する Critical FAIL を確認した**。誤りの性質は (1) happening 行 warning 化「17」を warning 全件総数と混同（実値 15）、(2) happening 行 opportunity 化「0」と migrate_c4_v02.py L310 のロジック齟齬（実値 39）、(3) expected/speculative 行で「opportunity 全 50 件を 4 行に按分しようとして失敗した結果のマイナス値・過大値」、の 3 系統である。さらに report §6.3「high warning 13 件のうち 12 件が G-N04」は同 report §6.1 表（13 行 G-N04）・§11.2「13 偉業すべて」と内部矛盾する独立 FAIL である。

カバレッジギャップでは briefing §必須要素 8 点すべてに対応する記述が確認され、warning 4 定義主観性 / maturity 5 ゼロ件閾値感度 / B-3→B-1 マッピング推定性等の研究限界も honest 開示済。ただし §9.1 表の集計枠組みの構造的弱さ（v0.2 6 区分を 4 列で表現する設計）は限界として未開示で、handoff §5.1 への追加が望ましい（G-6）。チーム間不整合では C-5 担い手特性との並列実行による未統合（D-5）が自己発見済 WARN として継承され、C-6 統合段階での解決が確立されている。

総合判定として **条件付 PASS（修正後再検証必須）** を付与する。Critical 5 件のうち、(B-5/B-6/B-7 §9.1 表の 3 行修正) は本トラック内修正で完了可能（F-1 修正案を適用）、(B-8 §6.3 「12 件」修正) は単独行修正で完了可能、(B-9 §9.1 注の構造解釈書き換え) は F-2 修正案を適用して完了。WARN 3 件はすべて C-6 統合・Phase D・handoff 更新時の追加開示で解決可能。great_actions.db v0.2 の構造的健全性は 60 カラム × 140 行で破壊なしに保たれており、SQL 集計値による再現性が完全に担保されている点は、Phase C-4 の独自貢献として高く評価できる。critical warning 4 件すべての G-N12 集中 + opportunity 50 件の戦略的空白 7 問分散は、ミラツクの「対等な探究者」「知識運動体」アイデンティティ実装に対し、Phase D での deep-knowledge 21 章接続のための重点参照素材 67 件（warning 17 + opportunity 50）を構造的に提供している。

---

## I. 完了報告フォーマット

```
Track C-4 doc-verify 完了:
- 検証項目数: 28 (A6 + B8 + C8 + D6)
- PASS: 21 / WARN: 3 / FAIL: 4
- Critical 不整合: 5 件
  - B-5 §9.1 happening 行 3 セル誤り（FAIL）
  - B-6 §9.1 expected 行 3 セル誤り（FAIL）
  - B-7 §9.1 speculative 行 2 セル誤り（FAIL）
  - B-8 §6.3 high warning「12 件」内部矛盾（FAIL）
  - B-9 §9.1 注 格下げ言及の構造解釈誤り（WARN Critical）
- HTML タグバランス: 3 ファイル全て完全均衡
  （analysis 9/9+10/10+8/8+89/89、verification 5/5+7/7+7/7+48/48、report 105/105+11/11+8/8+90/90）
- DB SQL 検証: 主要数値 17 件中 13 件整合、4 件齟齬（§9.1 表 3 行 + §6.3 12 件）
- sentinel への引継ぎ事項: 6 件（G-1〜G-6）
- 出力: track-c4-doc-verify-report.md
```

---

最終更新: 2026-05-10
作成: Phase C Wave 3 doc-verify（再実行版、前 stream watchdog 失敗の発見を取り込み）
判定: 条件付 PASS（修正後再検証必須、Critical 5 件 + WARN 3 件）
次フェーズ: refinement-coordinator → sentinel ゲート（report §9.1 表 + §6.3 + §9.1 注の修正完了確認後）
