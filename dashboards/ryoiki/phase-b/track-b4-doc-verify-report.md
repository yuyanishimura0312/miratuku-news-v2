# Track B-4 文書品質検証レポート (doc-verify)

判定日: 2026-05-09
判定者: doc-verify エージェント（Track B-4 実装者とは別人格）
最終判定: **CONDITIONAL PASS（重大ハルシネーション 1件・スナップショット不整合 2件・チーム間不整合 1件あり、要修正）**

検証対象:
- track-b4-detection-systems-analysis.html (約 25KB)
- track-b4-detection-systems-verification.html (約 17KB)
- track-b4-detection-systems-report.html (約 28KB)
- track-b4_handoff.md (約 14KB)
- ~/projects/research/initiatives-db/initiatives.db (180KB / questions 24・detection_systems 7・coverage_scores 168・initiatives 463)

---

## 0. 概観: 集計の核心は健全、ただし派生記述に検証可能な誤りあり

DB の実集計値（168 セル充足率・装置別平均スコア・初期化件数）は、handoff/report/verification の主要数値と完全一致する。一方で、以下の検証で詳述するとおり、報告本文中に「DB と矛盾する分類」「実 DB レコード数より多めの装置メタ情報」「B-1 系列ドキュメント間のラベル取り違え」が混在する。集計プロセスは健全だが、集計結果の言語化（解釈段）に複数の誤りが残っている。

---

## A. スナップショット不整合 (検出: 4 件 / うち WARN 2・要修正 2)

### A-01: 168 セル充足率の算術整合 — **PASS**

要求検証: score≥3 = 73/168 (43.5%)、score≤1 = 76/168 (45.2%)、score 2 = 19/168 (11.3%)、合計 168。

実DB集計（`SELECT score, count(*) FROM coverage_scores GROUP BY score`）:
- score 0 = 48, score 1 = 28, score 2 = 19, score 3 = 21, score 4 = 22, score 5 = 30
- score≥3 = 21+22+30 = **73** ✓ (43.5% ✓)
- score≤1 = 48+28 = **76** ✓ (45.2% ✓)
- score 2 = **19** ✓ (11.3% ✓)
- 合計 = 73+76+19 = **168** ✓

report 第1部 §1.1（line 185-187）の数値は完全整合。

### A-02: 装置別平均スコアの算術整合 — **PASS（Funding に 0.01 の丸め差）**

要求検証: SG 4.00 / IR 3.21 / UPR 2.67 / Funding 2.12 / Policy 1.50 / Sangaku 1.29 / SGRD 0.50。

実DB集計:
- SG 4.00 ✓ / IR 3.21 ✓ / UPR 2.67 ✓ / Policy 1.50 ✓ / Sangaku 1.29 ✓ / SGRD 0.50 ✓
- **Funding 2.13**（DB 値）vs **2.12**（handoff/report 値） — 差 0.01

差は丸め由来（51/24 = 2.125、四捨五入で 2.13、切り捨てで 2.12）であり、構造的問題ではないが、handoff §3 と report 図2（line 221）は 2.12 で記載、内部一貫性は確保されている。これ自体は WARN 以下。

### A-03: 装置別レコード規模主張と実 DB 値の乖離 — **要修正（重大）**

handoff §2 と report で装置レコード規模を以下のように記載:

| 装置 | 記述値 | 実 DB 値 | 差 |
|---|---|---|---|
| SG signals | 7,668 | 7,668 ✓ | 0 |
| UPR PR | 41,760 | 41,760 ✓ (consolidated.json) | 0（ただしブリーフィング 42,219 と差） |
| SGRD PR | 36,734 | 36,734 ✓ (stats.json) | 0 |
| Policy 事業 | 30,118 | 30,118 ✓ | 0 |
| **IR sections** | **1,862,236**（report 図2 line 217 行内、handoff §2 で 1.86M） | **1,769,821** | **▲92,415** |
| Funding press_releases | 16,642 | 16,642 ✓ | 0 |
| **Funding rounds** | **1,927** | **2,001** | +74 |
| **Funding organizations** | **4,180** | **4,264** | +84 |
| Sangaku records | 492,646 | n/a（matcher.db companies 3,872 のみ確認） | — |

**重大な内的不整合**: report 自身の中に IR sections の数値が「1,862,236」（line 217）と「1,769,821」（line 714）の二系列存在し、しかも片方（1,862,236）は実DBと不整合。verification HTML §2.1（line 186）はこの差を「documents 72,502 + sections 1,769,821 の合算的記述」と説明しようとしているが、72,502 + 1,769,821 = 1,842,323 で 1,862,236 にも届かない。検証編の説明そのものがハルシネーションを正当化する形になっている。**判定: 要修正**。

Funding の rounds 1,927 と organizations 4,180 も実 DB と差異がある。装置メタ情報の数値根拠を再点検すべき。

### A-04: 4 ホライズン分類の整合 — **PASS**

near 13 / mid 6 / far 3 / very-far 2 = 24 問の配分は B-1 handoff §6.2 と DB の questions テーブルで完全一致。ホライズン別平均（near 2.45 > far 2.05 > mid 1.98 > very-far 1.29）も実 DB と完全一致。

**A 総合**: 4 項目中 PASS 3 / 要修正 1（A-03 IR sections の二重記載 + 数値乖離）。

---

## B. ハルシネーション (検出: 4 件 / うち重大 1・要修正 2・WARN 1)

### B-01: 7 装置の実在性 — **PASS**

7 装置すべてが実在 DB / JSON を持つことを確認:

- SG: `~/projects/research/pestle-signal-db/data/signal.db`（signals 7,668 ✓）
- UPR: `~/projects/apps/miratuku-news-v2/data/upr_consolidated.json`（41,760 ✓）
- SGRD: `~/projects/apps/miratuku-news-v2/dashboards/sgrd-stats.json`（36,734 ✓）
- Policy: `~/projects/apps/policy-db/data/policy.db`（projects 30,118 ✓）
- IR: `~/projects/apps/ir-collector/data/ir.db`（sections 1,769,821 / documents 72,502 ✓）
- Funding: `~/projects/research/investment-signal-radar/data/investment_signal_v2.db`（press_releases 16,642 / funding_rounds 2,001 / organizations 4,264）
- Sangaku: `~/projects/apps/sangaku-matcher/data/matcher.db`（companies 3,872 ✓）

7 装置すべて実在し、ハルシネーションなし。

### B-02: 「全装置不応答型」分類 Q-N07 / Q-M02 の DB 値との矛盾 — **重大ハルシネーション・要修正**

report § 5（line 565-566）の図 5「補完類型別の問い分布」は次のとおり:

> **5. 全装置不応答型（すべて score≤2）**: 2 問: **Q-N07, Q-M02**

handoff §3（line 44）も同主張:

> 全装置不応答型 2 問: **Q-N07（科学AI）・Q-M02（AI制度反作用 mid）**

**DB の実値（`SELECT system_name, score, evidence_count FROM coverage_scores WHERE question_id IN ('Q-N07','Q-M02')`）**:

| Q-ID | SG | UPR | SGRD | Policy | IR | Funding | Sangaku | MAX |
|---|---|---|---|---|---|---|---|---|
| Q-N07 | 0 (0) | **5 (82)** | 0 (0) | 0 (0) | 1 (8) | 1 (4) | 0 (0) | **5** |
| Q-M02 | 2 (6) | **5 (34)** | 0 (0) | 0 (0) | 1 (1) | 1 (3) | 0 (0) | **5** |

**両問いとも UPR で score 5（最高位の「強力な早期警戒シグナル」）を獲得しており、「すべて score≤2」の定義を満たさない**。検証編 §2.4（line 203）は「Q-N10 と Q-F03 は SG のみ score 5/4 で他装置 score 0-1 の構造を確認」と記述しているが、この記述は「Q-N07 / Q-M02 が全装置不応答」とする report § 5 の主張と論理的に独立しており、Q-N07 / Q-M02 については検証されていない。

handoff §4「主要発見」§3 の「全装置不応答型 2 問」も DB の実値と矛盾。

**正しい分類**:
- 真に「全装置 score≤2」のセル群を抽出すると、24 問中 max_score≤2 となる問いは **0 問**（全問いに少なくとも 1 装置の score 3+ あり）。
- 「全装置不応答型」類型は実体として存在しない、もしくは分類定義を変更（例: SG を除いた 6 装置で score≤2）する必要がある。

これは Phase A Track 4 r2 教訓（キーワードgrepチェックリスト）における「集計値と分類言語化の照合不足」の典型例。**判定: 重大ハルシネーション・要修正**。

### B-03: B-4 の自己検証編 §2.4「PASS」判定の偽陽性 — **要修正**

verification.html §2.4（line 203）は次のとおり判定:

> Q-N10 と Q-F03 は SG のみ score 5 / 4 で他装置 score 0-1 の構造を確認。

DB 実値:
- Q-N10: SG=5(89), UPR=0, SGRD=0, Policy=0, IR=1(2), Funding=0, Sangaku=0 — ✓ 確認可能
- Q-F03: SG=4(57), UPR=0, SGRD=0, Policy=0, IR=1(2), Funding=0, Sangaku=0 — ✓ 確認可能

この 2 問の検証は正しい。だが、検証編は「Q-N07 / Q-M02 全装置不応答型」を独立検証していない。検証編 §2 ハルシネーションカテゴリ全体が「4/4 PASS」と判定（line 207）しているが、上記 B-02 の重大不整合を見逃しており、自己検証の十分性に欠ける。**判定: 自己検証の補強を要修正**。

### B-04: 463 件 initiatives の実在性 — **PASS**

実 DB から `SELECT count(*) FROM initiatives` = **463** ✓。source_db 別内訳: SG 115 / IR 105 / Policy 102 / Funding 88 / SGRD 24 / UPR 15 / Sangaku 14 = 463 ✓。各 initiative は organization / initiative_name / source_db / source_id 等を保持し、ハルシネーションなく実在 DB ソースから取得されたものと判断。代表サンプル確認: Q-N01 SG 由来「Tech giants capturing AI monopoly outside regulatory frameworks」「AI capability-governance gap widening into security vacuum」等は signal.db の signal_name と整合する形式。

**B 総合**: 4 項目中 PASS 2 / 重大要修正 1（B-02）/ 要修正 1（B-03 自己検証の補強）。

---

## C. カバレッジギャップ (検出: 4 件 / うち WARN 1)

### C-01: B-1 41 問のうち 24 問の選定根拠 — **PASS**

handoff §2 で対象 24 問を明示（near 13 全 / mid: M02 M04 M05 M08 M09 M12 / far: F01 F03 F08 / very-far: V02 V06）。B-1 handoff §6.2 の指定リストを継承する形で正しく開示されている。

### C-02: 装置不応答（dead zones）問いの honest 開示 — **WARN**

要求検証: 「Q-N07 / Q-M02 score 0 の honest 開示」「Q-N10 / Q-F03 / Q-V07 score 0-1 集中の honest 開示」。

開示状況:
- **Q-N07 / Q-M02**: 上記 B-02 のとおり「全装置不応答」と分類されているが、DB 実値ではいずれも UPR で score 5 を獲得しており、honest 開示になっていない。誤った honest（実は強応答装置あり）。
- **Q-N10**: report § 5（line 565）で「SG 単独応答型」（SG のみ score≥3）に分類。DB 実値（SG=5, 他=0-1）と整合。**正しく honest 開示**。
- **Q-F03**: 同じく「SG 単独応答型」に分類。DB 実値と整合。**正しく honest 開示**。
- **Q-V07 pluriverse**: handoff §4 主要発見 §4（line 60）と §6.3（line 111）と §10（line 161）で「装置不応答 = B-2 補完候補」として言及されているが、**Q-V07 は B-4 の評価対象 24 問に含まれていない**（24 問は Q-V02 と Q-V06 のみ）。Q-V07 の score 値は B-4 では一切評価されておらず、「score 0-1 集中」と主張する根拠が B-4 内にない。これは B-1 の 41 問空間で評価されるべき内容を、B-4 の評価結果として誤って継承している。

**判定**: WARN（Q-N07/Q-M02 の誤分類は B-02 と重複、Q-V07 の評価範囲外言及は要修正）。

### C-03: 装置間補完関係の論理整合 — **WARN**

report § 5.2（line 555-569）の補完類型 5 分類は、定義と実値の整合性に部分的問題あり:

- 類型 1「全装置応答型」（5 装置以上 score≥3）6 問（Q-N01, Q-N03, Q-N04, Q-N13, Q-M12, Q-F01）は、実 DB で確認可能（例: Q-N01 は SG=5 / UPR=2 / SGRD=3 / Policy=2 / IR=4 / Funding=4 / Sangaku=4 で 5 装置 score≥3 達成）。
- 類型 2「制度+市場応答型」(Policy + IR + Funding 主体) 4 問のうち Q-N09 は Policy=2 / IR=5 / Funding=3 で Policy が条件を満たさず、定義との整合性に疑義。
- 類型 5「全装置不応答型」は B-02 のとおり実体がない。

合計 6+4+4+8+2 = 24 問（24 問空間と整合）。分類間の MECE 性は保たれているが、定義と実値の整合性に不備あり。

### C-04: 168 セル全公開 — **PASS**

DB の coverage_scores テーブルは 168 行すべてに score / evidence_count / latest_signal_date / notes が収載され、後続Track が SQL で直接参照可能。report § 2 でヒートマップ（CSS Grid h-0〜h-5）として全 168 セルが可視化されている（タグバランスは別途確認していないが、report § 1 の図表記述と整合）。

**C 総合**: 4 項目中 PASS 2 / WARN 2（C-02 と C-03、いずれも B-02 起因）。

---

## D. チーム間不整合 (検出: 4 件 / うち重大 1・WARN 1)

### D-01: B-1 § 6.2 の 24 問 ID リストの継承精度 — **要修正**

要求検証: B-1 修正後 Mサインラベルの正確継承、B-1 report と handoff §6.2 の M10 vs M09 ID 差異についての処理。

実態:

- **B-1 handoff §6.2（line 63）の確定リスト**: 「2050の問い: Q-M02／Q-M04／Q-M05／Q-M08／**Q-M10（創薬AI）**／Q-M12」 → **M10**
- **B-1 report § 6.2**: M10（B-1 doc-verify report の line 136 で確認済み「report §6.2 では正しく Q-M02・M04・M05・M08・M10・M12」）
- **_TRACK_B4_BRIEFING.md（line 23）**: 「mid (6問): Q-M02/M04/M05/M08/**M09**/M12」 → **M09**
- **B-4 採用**: M09（物語転換期の本格化）

B-4 自身の handoff §6.2 と verification §4.1 では:

> B-1 report 本文中で「mid 6 問のうち **M10（創薬AI）**」と記載されるが **B-1 handoff §6.2 確定リストでは M09**。本Track は handoff の確定指定（M09 物語転換期の本格化）を採用。

これは事実と逆。実際は B-1 report も B-1 handoff §6.2 も両方が **M10** と書いており、**B-4 ブリーフィング** が M09 に変更している。B-4 は「ブリーフィング指定（M09）」に従ったのが事実だが、根拠を「B-1 handoff §6.2」と誤帰属している。

なお、B-1 doc-verify report（既存）の line 230 でも「実装の Q-M04（少子化）／Q-M05（場所性経済化）／Q-M10（創薬AI）」が正解と認定されている。

**判定: 要修正**。B-4 handoff §7.6 と verification §4.1 の文言を「ブリーフィング指定が M09、B-1 handoff/report は M10」に訂正すべき。なお、B-4 が M09 を採用したこと自体は、ブリーフィング命令系統の優先で許容範囲。

### D-02: B-1 strong findings との整合 — **PASS**

B-1 が認定した真M（物語転換期 → Q-M09 / Q-N03 系）・準M（世代間正義・非西洋認識論・AI制度反作用 → Q-N02 / Q-N05 / Q-N10 / Q-M02 / Q-N12 系）に対して、B-4 装置応答評価は概ね Mサイン認定領域に応答スコア（SG 中心に score 4-5）を返している。整合性確認できる。

### D-03: B-2 14 問との重複・差異の明示 — **WARN**

handoff §6.3（line 113）は次のとおり:

> これは Track B-1 § 6.1 で B-2 対象 **14 問**に既に含まれる問いとも重複するが、本Track の「装置不応答」観点からの逆算的補強として位置づける。

B-1 handoff §6.1 の B-2 対象 14 問リストと B-4 24 問の重複問いが具体的に明示されていない（個別 Q-ID 突合なし）。「Q-V07 等」と言及されるが、Q-V07 は B-4 24 問に含まれず（C-02 参照）、重複論議として成立しない。

**判定: WARN**。重複問いの具体的 Q-ID リスト（B-2 14 問 ∩ B-4 24 問）を明示すべき。

### D-04: B-3 30 問との独立性の明示 — **WARN**

B-3 は G-prefixed 30 問（G-N01〜N12, G-M01〜M10, G-F01〜F05, G-V01〜V03、合計 30）の独立系列。B-4 は Q-prefixed 24 問（B-1 直接継承）。両者は別系列（G ID と Q ID）であり構造的に独立だが、B-4 出力（handoff / report / verification）は B-3 30 問との独立性を**明示していない**。handoff §6.3 と §6.4 で B-3 への補完提案は記述されるが、「B-4 24 問は B-1 直接継承で B-3 と独立」「B-3 G ID は別系列」の注記なし。

**判定: WARN**。B-3 独立性の注記を追加すべき。

**D 総合**: 4 項目中 PASS 1 / 要修正 1（D-01）/ WARN 2（D-03 / D-04）。

---

## 5. 三系列開示原則のチェック（briefing値 vs 実装値）

| 項目 | briefing 値 | 実装値 | 差 | 開示状況 |
|---|---|---|---|---|
| UPR 件数 | 42,219（_TRACK_B4_BRIEFING.md line 8） | 41,760（実 JSON） | ▲459 | verification.html callout（line 188-191）で開示 ✓ |
| 投資シグナル ラウンド | 1,927（briefing line 12） | 2,001（実DB） | +74 | **未開示** |
| 投資シグナル 組織 | （briefing記載なし） | 4,264（実DB） | — | （比較対象なし） |
| IR レコード | 1,862,236（briefing line 11） | 1,769,821（sections）+ 72,502（documents） | — | verification.html §2.1 で「合算的記述として整合」と説明、ただし合算してもギャップあり |
| mid 6 問の M09/M10 | M09（briefing line 23） | M09（実装） | 0 | 一致するが、起源を B-1 handoff §6.2 と誤帰属 |

briefing 値と実装値の乖離があれば WARN 以上というルールに照らすと、**投資シグナル ラウンド（1,927 vs 2,001）が未開示** で WARN 該当。**IR レコード**（1.86M vs 1.77M）は開示努力はあるが、説明自体が誤算（72,502 + 1,769,821 = 1,842,323 ≠ 1,862,236）でハルシネーションの自己強化。

---

## 6. 最終判定と修正要請

### 最終判定: **CONDITIONAL PASS**

**判定根拠**:
- 集計プロセス・168 セルマトリクス・装置別平均スコア・Initiatives DB 実体は健全で、Phase B Wave 2 の中核成果として有効。
- ただし、重大なハルシネーション 1 件（B-02「全装置不応答型」分類が DB と矛盾）と装置レコード規模の数値乖離（A-03）、B-1 系列ID差異の起源誤帰属（D-01）が混在しており、PASS は条件付き。

### 必須修正項目（sentinel ゲート前に対応）

1. **【最重要】B-02 全装置不応答型分類の修正**:
   - report § 5 図 5（line 565-566）の「Q-N07, Q-M02 = 全装置不応答型」を、DB 実値（両問いとも UPR score 5）と整合する形で修正。
   - 補完類型 5 分類の定義そのものを見直す（例: 「SG・UPR 以外の 5 装置で全 score≤2」と再定義）か、類型 5 を削除し 4 類型に再構成する。
   - handoff §3（line 44）「全装置不応答型 2 問: Q-N07・Q-M02」と handoff §4 主要発見 §3 を同様に修正。

2. **A-03 装置レコード規模の修正**:
   - report 図 2（line 217）の IR sections 1,862,236 を実 DB 値 1,769,821 に修正。
   - handoff §2「IR 1.86M セクション / 72K documents」を「sections 1,769,821 / documents 72,502」に修正。
   - Funding rounds を 1,927 → 2,001、organizations を 4,180 → 4,264 に修正（または再集計時の差異として開示）。
   - verification §2.1（line 186）の「合算的記述として整合」説明を撤回。

3. **D-01 M09/M10 起源の修正**:
   - handoff §7.6 と verification §4.1 callout（line 250-252）を「B-1 handoff §6.2 と B-1 report は両方 M10。B-4 ブリーフィング指定で M09 に変更されたため B-4 は M09 を採用」と訂正。

### 推奨修正項目（次回 Wave サイクルで対応）

4. **C-02 Q-V07 言及の修正**: handoff §4 主要発見 §4 と §6.3 と §10 の「Q-V07」言及は B-4 評価対象外であることを明示し、B-1 41 問空間からの推測として位置づける。

5. **D-03 B-2 14 問との重複明示**: handoff §6.3 で B-2 対象 14 問と B-4 24 問の交差 Q-ID リストを具体的に列挙。

6. **D-04 B-3 30 問独立性の注記**: handoff §6 で「B-3 は G-prefixed 30 問の独立系列、B-4 は B-1 直接継承の Q-prefixed 24 問」を注記。

7. **A-02 Funding 平均スコア 0.01 差**: 2.12 か 2.13 のいずれかに統一（実 DB 値は 2.13）。

---

## 7. 集計（カテゴリ別）

| カテゴリ | 検出件数 | 内訳 | 総合 |
|---|---|---|---|
| A. スナップショット不整合 | 4 件 | PASS 3 / 要修正 1（A-03） | 要修正あり |
| B. ハルシネーション | 4 件 | PASS 2 / 重大要修正 1（B-02）/ 要修正 1（B-03） | **重大あり** |
| C. カバレッジギャップ | 4 件 | PASS 2 / WARN 2（C-02・C-03） | WARN |
| D. チーム間不整合 | 4 件 | PASS 1 / 要修正 1（D-01）/ WARN 2（D-03・D-04） | 要修正あり |
| **合計** | **16 件** | **PASS 8 / 要修正 3 / WARN 4 / 重大 1** | **CONDITIONAL PASS** |

---

## 8. 後続 Track への引継ぎ（sentinel/B-5/B-6 向け）

- sentinel: 上記必須修正 1-3 の対応完了確認をゲートに含めるべき。特に B-02（全装置不応答型分類）は 5 補完類型分類全体の妥当性に波及するため、B-5「動きの状況測定」での hot/dead zones 判定に直接影響する。
- B-5 リード: B-4 の coverage_scores テーブル 168 行は健全に利用可能だが、「全装置不応答型」分類はそのまま継承せず、独自に max_score≤2 のセル抽出を行うことを推奨。
- B-6 リード: phase-b-master-report.html での B-4 セクション統合時、IR sections 数値・Funding rounds 数値を実 DB 値で再記述すべき。

---

検証担当: doc-verify エージェント
方法論: 4 カテゴリ独立検証 + 実 DB 集計再現 + B-1/B-3/briefing 系列横断クロスチェック
所要時間: 約 30 分
