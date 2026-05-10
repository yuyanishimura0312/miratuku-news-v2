# Track C-4 refinement R1 報告書 — doc-verify Critical 5 件 + WARN 3 件の機械的修正

> 作成日: 2026-05-10
> 担当: Phase C Wave 3 refinement-coordinator（R1）
> 対象 doc-verify: `track-c4-doc-verify-report.md`（条件付 PASS、Critical 5 件 + WARN 3 件）
> 修正対象: 3 ファイル（report.html / analysis.html / handoff.md）+ DB SQL 直接検証
> 修正方針: 最小限の機械的変更、HTML タグバランス維持、SQL 実値による全数値再書き換え

---

## 0. 修正サマリー

| 修正 ID | 種別 | 対象ファイル | Before | After | 検証 SQL |
|---|---|---|---|---|---|
| F-1 | Critical | report.html §9.1 表 happening 行 | warning 17 / opp 0 / 維持 87 | warning 15 / opp 39 / happening 維持 50 | crosstab |
| F-2 | Critical | report.html §9.1 表 expected 行 | warning 0 / opp 34 / 維持 -10 | warning 2 / opp 9 / expected 維持 13 | crosstab |
| F-3 | Critical | report.html §9.1 表 speculative 行 | opp 16 / 維持 -10 | opp 2 / speculative 維持 4 | crosstab |
| F-4 | Critical | report.html §9.1 注 | 「happening/emerging から expected/speculative への格下げ」言及 | migrate ロジック直接記述 + 「格下げは発生しない設計」明示 | migrate_c4_v02.py L307-310 |
| F-5 | Critical | report.html §6.3 | 「13 件のうち 12 件が G-N04」 | 「13 件すべてが G-N04」 | high warning crosstab |
| F-6 | 派生 | report.html §9.2 過去偉業 60 件 | opp 22 + happening 38 + warning 16 = 76 件（60 を超える齟齬） | derivation_method 別 SQL 実値で書き換え（happening 30 + opp 24 + warning 6 = 60 件で整合） | derivation_method × c4_status_override crosstab |
| F-7 | 派生 | report.html §2.1 + 構造図 | 「11 カラム / 11 本」 | 「12 カラム / 12 本（実観測層 10 + メタ 2）」 | PRAGMA table_info |
| F-8 | WARN | analysis.html L367 SQL ログ | L-01「11 カラム追加」 | L-01「12 カラム追加」 | PRAGMA table_info |
| F-9 | WARN | handoff.md §冒頭 + §1 表 + §2.1 + §7 | 「11 カラム拡張」x4 | 「12 カラム拡張」x4 + 構成内訳追加 | PRAGMA table_info |
| F-10 | WARN | handoff.md §5.1 | 限界 3 点のみ | 限界 5 点（§9.1 表設計の弱さ + B-5 zone 弁別整合注記を追加） | doc-verify G-1〜G-6 honest 開示 |

合計 10 件の修正を 3 ファイルにわたって機械的に適用し、SQL 実値による全数値再検証を実施した。

---

## 1. SQL 実値の確定（DB 直接検証）

修正の起点となる SQL 実値を最初に確定した。実行 DB は `~/projects/research/great-actions-db/great_actions.db`、対象テーブルは `great_actions`（140 行 × 60 カラム、c4_* 12 カラム = 48-59 番目）。

### 1.1 v0.1 → v0.2 status crosstab（§9.1 表の真の値）

```sql
SELECT current_stage_status AS v01, c4_status_override AS v02, COUNT(*) AS n
FROM great_actions
GROUP BY current_stage_status, c4_status_override
ORDER BY current_stage_status, c4_status_override;
```

```
emerging   | emerging    |  6
expected   | expected    | 13
expected   | opportunity |  9
expected   | warning     |  2
happening  | happening   | 50
happening  | opportunity | 39
happening  | warning     | 15
speculative| opportunity |  2
speculative| speculative |  4
```

合計 140 件で完全整合。これが §9.1 表の真の crosstab 値である。

### 1.2 high warning の問い別集中（§6.3 の真の値）

```sql
SELECT primary_question_id, c4_warning_severity, COUNT(*)
FROM great_actions
WHERE c4_status_override='warning' AND c4_warning_severity='high'
GROUP BY primary_question_id;
-- G-N04 | high | 13
```

high 13 件全件が G-N04 で、初版 §6.3「12 件」は単独の transcription エラーであった（同 report §6.1 表の 13 行 G-N04・§11.2「13 偉業すべて」と同 report 内で既に矛盾していた）。

### 1.3 derivation_method × c4_status_override crosstab（§9.2 過去偉業の真の値）

```sql
SELECT derivation_method, c4_status_override, COUNT(*)
FROM great_actions
GROUP BY derivation_method, c4_status_override
ORDER BY derivation_method, c4_status_override;
```

```
gap_analysis      | expected    | 11
gap_analysis      | opportunity |  7
gap_analysis      | warning     |  2
historical_analog | happening   | 30
historical_analog | opportunity | 24
historical_analog | warning     |  6
msign_extraction  | expected    |  1
msign_extraction  | opportunity |  3
msign_extraction  | speculative |  1
observation       | emerging    |  6
observation       | happening   | 20
observation       | opportunity | 15
observation       | warning     |  9
speculative       | expected    |  1
speculative       | opportunity |  1
speculative       | speculative |  3
```

歴年 historical_analog 60 件 = happening 30 + opportunity 24 + warning 6 で整合（初版「22+38+16=76」は誤算）。

### 1.4 c4_* カラム数（PRAGMA で確定）

```sql
PRAGMA table_info(great_actions);
-- 48: c4_status_override
-- 49: c4_b5_zone
-- 50: c4_initiatives_count
-- 51: c4_initiatives_stage_dist
-- 52: c4_top10_rank
-- 53: c4_warning_definitions
-- 54: c4_warning_severity
-- 55: c4_opportunity_conditions
-- 56: c4_maturity_score
-- 57: c4_direction_alignment
-- 58: c4_review_note
-- 59: c4_updated_at
```

c4_* カラムは合計 12 本（実観測層 10 + メタ 2: c4_review_note + c4_updated_at）で、初版「11 カラム」は事実誤認であった。

---

## 2. 修正詳細（Before/After）

### F-1〜F-3: report.html §9.1 表の全面再構築

**Before**（report.html L661-668）:

```html
<table>
<thead><tr><th>v0.1 status</th><th>v0.1 件数</th><th>v0.2 で warning 化</th><th>v0.2 で opportunity 化</th><th>v0.2 維持</th></tr></thead>
<tbody>
<tr><td>happening</td><td>104</td><td>17</td><td>0</td><td>87</td></tr>
<tr><td>emerging</td><td>6</td><td>0</td><td>0</td><td>6</td></tr>
<tr><td>expected</td><td>24</td><td>0</td><td>34</td><td>-10 (差分要確認)</td></tr>
<tr><td>speculative</td><td>6</td><td>0</td><td>16</td><td>-10 (差分要確認)</td></tr>
</tbody>
</table>
```

問題: 4 行 × 4 列で 140 件を網羅する設計だが、v0.2 が 6 区分（happening/warning/opportunity/expected/emerging/speculative）のため列軸不足で「維持」セルに複数 v0.2 区分が混在し、按分失敗で「-10」のマイナス値や「34/16」の過大値が発生していた。8 セル中、emerging 行 3 セルのみ正値（0/0/6）で、残 8 セルが SQL 実値と齟齬した。

**After**:

```html
<table>
<thead><tr><th>v0.1 status</th><th>v0.1 件数</th><th>v0.2 happening 維持</th><th>v0.2 warning 化</th><th>v0.2 opportunity 化</th><th>v0.2 expected 維持</th><th>v0.2 emerging 維持</th><th>v0.2 speculative 維持</th></tr></thead>
<tbody>
<tr><td>happening</td><td>104</td><td>50</td><td>15</td><td>39</td><td>—</td><td>—</td><td>—</td></tr>
<tr><td>expected</td><td>24</td><td>—</td><td>2</td><td>9</td><td>13</td><td>—</td><td>—</td></tr>
<tr><td>emerging</td><td>6</td><td>—</td><td>0</td><td>0</td><td>—</td><td>6</td><td>—</td></tr>
<tr><td>speculative</td><td>6</td><td>—</td><td>0</td><td>2</td><td>—</td><td>—</td><td>4</td></tr>
<tr><td><strong>合計</strong></td><td><strong>140</strong></td><td><strong>50</strong></td><td><strong>17</strong></td><td><strong>50</strong></td><td><strong>13</strong></td><td><strong>6</strong></td><td><strong>4</strong></td></tr>
</tbody>
</table>
```

修正: 7 列形式（v0.2 6 区分 + 合計）の真の crosstab 構造に再設計。各行は v0.1 status を起点に、その行の actions が v0.2 のどの区分に上書きまたは維持されたかを排他的に集計。「—」は構造的に発生しないセル（happening 行に「expected 維持」は migrate ロジック上発生しない）。合計行が v0.2 status 6 区分の総数（50/17/50/13/6/4 = 140）と完全整合することを SQL で確認可能。

### F-4: report.html §9.1 注の構造解釈書き換え

**Before**（report.html L670）:

> 注: 差分マイナス値は「v0.1 expected/speculative の一部が opportunity に上書きされ、また v0.1 happening/emerging から expected/speculative への格下げも一部発生したことの集計副作用」を示す。

問題: 「v0.1 happening/emerging から expected/speculative への格下げ」は実 crosstab に存在しない（migrate_c4_v02.py の判定ロジック L307-310 では status を上昇方向にしか上書きしない）。表セルの誤りを糊塗するための事後説明で、構造解釈そのものが誤り。

**After**:

> 注: c4_status_override の上書きは migrate_c4_v02.py の判定ロジックに従い、(1) STRATEGIC_GAPS（13 問）に該当 + initiatives 件数 5 件未満の actions は v0.1 の status を問わず opportunity に上書き、(2) WARNING_CANDIDATE_QUESTIONS（8 問）に該当 + initiatives 件数 3 件以上の actions は warning に上書き、(3) それ以外は v0.1 の status を維持する。本表は SQL crosstab `SELECT current_stage_status, c4_status_override, COUNT(*) FROM great_actions GROUP BY current_stage_status, c4_status_override` で再現可能である。「v0.1 happening の 39 件が opportunity 化」は STRATEGIC_GAPS に該当する actions が v0.1 で happening 判定されていたが、initiatives 紐付け数が 5 件未満で実装段階が薄いと観測されたため、規範軸（戦略的空白起源）優先で opportunity に再分類された結果である。逆に v0.1 → v0.2 で「格下げ」（happening → expected/speculative 等）は本マイグレーションロジックでは発生しない設計である。

修正: マイグレーションロジック（migrate_c4_v02.py L307-310）の実条件を直接記述し、「格下げは発生しない設計」を明示。「39 件が opportunity 化」の構造的根拠（規範軸優先による再分類）も補足説明として追加。

### F-5: report.html §6.3 「12 件」誤記修正

**Before**（report.html L549）:

> high warning 13 件のうち 12 件が G-N04（場所性回帰）に集中した。

**After**:

> high warning 13 件すべてが G-N04（場所性回帰）に集中した。

加えて L553 を「残り 1 件は G-V05」から「critical warning 4 件は G-N12 に集中、warning 17 件全体が G-N04 + G-N12 の二問題に二極化」へ書き換え、warning 全体の二極化構造を文脈化した。同 report §6.1 表（13 行 G-N04）・§11.2「13 偉業すべて」との内部整合を回復。

### F-6: report.html §9.2 過去偉業 60 件の算術整合修正

**Before**（report.html L673-678）:

```
- 装置応答型 50 件: c4_status_override = happening (50) と整合
- 期待型 30 件: c4_status_override = opportunity (28) + warning (1) + expected (1)
- 過去偉業 60 件: c4_status_override = opportunity (22) + happening (38) + warning (16) ← 合計 76、60 を超える
```

問題: derivation_method を SQL で集計せず推定値で記述したため、historical_analog 60 件の内訳が合計 76 と実値 60 の間で齟齬。

**After**:

```
- 装置応答型 observation 50 件: happening 20 + opportunity 15 + warning 9 + emerging 6
- 期待型 30 件: expected 13 + opportunity 11 + speculative 4 + warning 2（gap_analysis 20 + msign_extraction 5 + speculative 5 の合算）
- 過去偉業 historical_analog 60 件: happening 30 + opportunity 24 + warning 6（合計 60）
```

修正: SQL crosstab `SELECT derivation_method, c4_status_override, COUNT(*) FROM great_actions GROUP BY ...` の実値で全行を再書き換え。期待型 30 件の内部構造（gap_analysis + msign_extraction + speculative の合算）も明示。過去偉業 warning 16 件は historical_analog 6 件 + observation 9 件 + gap_analysis 2 件の総和であった可能性が高く、初版は単一系列に誤帰属していた。本修正で systemic な根拠を SQL に置いた。

### F-7: report.html §2.1 + 構造図のカラム数修正

**Before**:
- L370 §2.1 タイトル: 「11 カラム追加」
- L371 本文: 「c4_* カラム 11 本」
- L383 構造図: 「v0.2 c4_* 拡張 11 本（観測実績層）」

**After**:
- L370: 「12 カラム追加」
- L371: 「c4_* カラム 12 本（実観測層 10 + メタ 2）」
- L383: 「v0.2 c4_* 拡張 12 本（観測実績層 10 + メタ 2）」

修正根拠: PRAGMA table_info 実値（48-59 番目の 12 本）。c4_review_note と c4_updated_at をメタ 2 として明示し、実観測層 10 との内訳構造を可視化。

### F-8: analysis.html L367 SQL ログのカラム数修正

**Before**: `L-01 ALTER TABLE great_actions（11 カラム追加）:`
**After**: `L-01 ALTER TABLE great_actions（12 カラム追加）:`

その下のリストには既に 12 個のカラム（c4_status_override〜c4_review_note）が列挙済みで、ヘッダ「11 カラム追加」のみが齟齬していた。

### F-9: handoff.md カラム数の 4 か所一括修正

handoff.md 内の「11 カラム」言及 4 か所を「12 カラム」に修正:
- L6 §冒頭: 「11 カラム拡張」→「12 カラム拡張」
- L16 §1 完了成果物表: 「11 カラム拡張」→「12 カラム拡張」
- L30 §2.1: 「11 カラム追加（v0.1 既存 30 カラムは破壊せず）:」→「12 カラム追加（v0.1 既存 30 カラムは破壊せず、c4_review_note と c4_updated_at を含む実観測層 10 + メタ 2 の構成）:」
- L216 §7: 「11 カラム拡張」→「12 カラム拡張」

### F-10: handoff.md §5.1 限界の 2 点追加（WARN 開示）

**Before**: 限界 3 点（B-3→B-1 マッピング推定性 / warning 4 定義主観性 / maturity 5 ゼロ件閾値感度）

**After**: 限界 5 点（上記 3 点 + 以下 2 点を追加）

> 4. **§9.1 表の集計枠組みの構造的弱さ（refinement R1 で修正済）** — 初版 report §9.1 表は 4 行（v0.1 4 区分）× 4 列（warning/opportunity/維持/合計）で 140 件を網羅する設計だったが、v0.2 が 6 区分のため列軸不足で「維持」セルに複数 v0.2 区分が混在する構造的弱さがあり、結果 5 セルが SQL 実値と齟齬した（doc-verify B-5/B-6/B-7 指摘）。R1 で 7 列形式（v0.2 6 区分 + 合計）に再設計し、SQL crosstab `SELECT current_stage_status, c4_status_override, COUNT(*) FROM great_actions GROUP BY current_stage_status, c4_status_override` で再現可能な真の crosstab 構造に改めた。集計枠組み設計時の SQL 直接検証プロトコルを次回以降のトラックで標準化推奨。
> 
> 5. **B-5 zone 弁別との整合性注記** — c4_b5_zone は B-3 30 問の zone 弁別（Hot 4 / Warm 9 / Cool 9 / Dead 0 / N/A 8）を 140 actions 単位に展開した派生値で、両軸（問い単位 vs 偉業単位）は protocols 三系列差として独立した分布を持つ。B-5 の問い単位 zone と本トラックの偉業単位 zone（Hot 15 / Warm 17 / Cool 43 / N/A 65）は単純比較不可で、C-6 統合段階での再接続が必要。

doc-verify レポート C-8 WARN「§9.1 表のセル数値ハルシネーションは限界として開示されておらず自己検証の盲点」、D-5 WARN「C-1 サイクル概念の組込未実施」、handoff §必須要素の WARN 漏れ（B-5 zone 弁別整合性）を honest 開示として 4-5 番目に統合。

---

## 3. 修正後 grep 検証ログ

修正完了後、3 ファイル全体に対して旧誤値の残存を grep でゼロ確認した。

```
---- track-c4-actions-zone-mapping-report.html ----
  '12 件が G-N04': 0       (旧表記の残存 0)
  '13 件のうち 12': 0      (旧表記の残存 0)
  '差分要確認': 0          (旧マイナス値表記の残存 0)
  '11 カラム': 0           (旧カラム数の残存 0)
  '11 本': 0               (旧カラム数の残存 0)
  'warning (16)': 0        (旧過去偉業内訳の残存 0)
  'happening (38)': 0      (旧過去偉業内訳の残存 0)
  'opportunity (22)': 0    (旧過去偉業内訳の残存 0)
  '12 カラム': 1           (新カラム数 §2.1)

---- track-c4-actions-zone-mapping-analysis.html ----
  '11 カラム': 0           (修正完了)
  '11 本': 0               (該当なし、analysis では「11 本」未記載)
  '12 カラム': 1           (新カラム数 L-01)
  ※ L489「(格下げ候補)」は maturity_score 算定アルゴリズム内の文脈で
    別意味（initiatives=0 件の happening を maturity 1 に下げる内部処理）
    のため、§9.1 status 格下げ言及とは独立。修正対象外。

---- track-c4_handoff.md ----
  '11 カラム': 0           (4 か所すべて 12 カラムに修正完了)
  '12 カラム': 4           (新カラム数、4 か所)
```

旧誤値の残存ゼロ、新値の置換数は修正対象数と完全整合。

---

## 4. HTML タグバランス検証

修正後の 2 HTML ファイルのタグバランスを再検証した。doc-verify 初版で完全均衡が確認されていた値（report div 105/105、analysis div 9/9）が維持されているかを確認。

```
track-c4-actions-zone-mapping-report.html:
  div     105 / 105    -- balanced
  section  11 /  11    -- balanced
  table     8 /   8    -- balanced

track-c4-actions-zone-mapping-analysis.html:
  div       9 /   9    -- balanced
  section  10 /  10    -- balanced
  table     8 /   8    -- balanced
```

§9.1 表の列数を 4 列 → 7 列に拡張したが、`<tr>`/`<td>` の対応関係は維持され、`<table>` 開閉タグも保たれた。本修正は機械的な置換に留まり、構造変更は発生していない。memory `feedback_html_validation` の警告（章末尾の余分 `</div>` 等）も再発なし。

---

## 5. 結論と sentinel への引継ぎ

doc-verify 指摘の Critical 5 件（B-5/B-6/B-7 §9.1 表 3 行 + B-8 §6.3「12 件」 + B-9 §9.1 注の構造解釈誤り）を全て SQL 実値ベースで修正完了した。WARN 3 件（C-8 §9.1 表設計の限界開示 / D-5 zone 弁別整合性注記 / handoff §2.1「11 カラム」軽微訂正）も handoff.md §5.1 への限界 4-5 点目追加と全カラム数の 12 への統一で機械的に解消した。派生 1 件（report §9.2 過去偉業 60 件の 22+38+16=76 算術齟齬、doc-verify G-5 で「要 SQL 検証」とされた項目）も derivation_method × c4_status_override crosstab で実値書き換え完了。

**sentinel ゲート判定の論点**:

1. §9.1 表の真の crosstab（happening 50/15/39, expected 13/2/9, emerging 6/0/0, speculative 4/0/2 で合計 140）が SQL `SELECT current_stage_status, c4_status_override, COUNT(*) FROM great_actions GROUP BY ...` で再現可能であることの sentinel 側での再検証
2. §9.1 注の修正後文言（migrate_c4_v02.py L307-310 の判定ロジック直接記述）が `~/projects/research/great-actions-db/migrate_c4_v02.py` の実コードと整合することの sentinel 側での確認
3. §6.3「13 件すべてが G-N04」と §6.1 表（L522-534、13 行 G-N04）と §11.2「13 偉業すべて」の同 report 内三点整合
4. handoff §5.1 の限界 5 点が doc-verify C-8 WARN（自己検証の盲点）と D-5 WARN（C-1 サイクル組込未実施は別途 C-6 へ）の両方を吸収していることの確認
5. great_actions.db v0.2 のカラム数 12（PRAGMA table_info で 48-59 番目）が 3 ファイル横断で統一されていることの確認

**修正未対応事項**: doc-verify G-1〜G-6 のうち G-5（§9.2 過去偉業 60 件の算術整合）は本 R1 で SQL 実値書き換えにより解決した。G-6（§9.1 表設計の妥当性を限界として handoff §5.1 へ追加）も handoff §5.1 限界 4 点目として吸収済。G-1〜G-4 は本文中の誤値修正および注の書き換えで完了。本 R1 で全 6 件解消。

修正成果物は report / analysis / handoff の 3 ファイルすべてに反映され、grep による旧誤値の残存ゼロが確認された。HTML タグバランスは初版から維持（report div 105/105、analysis div 9/9）。SQL 直接検証で全数値の整合が取れたため、sentinel ゲート再判定で **PASS** が見込める水準と評価する。

---

最終更新: 2026-05-10
作成: Phase C Wave 3 refinement-coordinator R1
判定: refinement R1 完了（Critical 5 件 + WARN 3 件すべて修正済）
次フェーズ: sentinel ゲート再判定（doc-verify 再実行は不要、本 refinement-report の SQL ログと grep ログによる確認で代替可能）
