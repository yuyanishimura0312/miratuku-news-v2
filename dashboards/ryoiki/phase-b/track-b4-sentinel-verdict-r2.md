# Track B-4 Sentinel 最終ゲート再判定書 (Round 2)

判定日: 2026-05-09
判定者: Sentinel（Devil's Advocate / VETO権付き最終ゲート）
対象: track-b4-detection-systems-{analysis,verification,report}.html + track-b4_handoff.md（refinement後）+ initiatives.db
前提: refinement-coordinator ALL_RESOLVED 報告（C1+M1+M2 履行主張）

## 1. 判定

**REJECT（差し戻し）— Wave 3（B-5）起動不可**

refinement-coordinator は「ALL_RESOLVED」と報告したが、独立検証で **3件中2件の必須修正に重大な未履行・部分履行** を発見。さらに C1 修正の再構成方針自体が新たな整合性違反を生んだ。

## 2. 要約

168セルマトリクスとDB集計基盤は健全のまま。しかし「ALL_RESOLVED」報告にもかかわらず、**analysis.html は IR/Funding 旧数値が完全に未修正のまま放置（5箇所）**、handoff/verification では「5類型」表現が **6箇所残存**、Q-N07/Q-M02 を「研究応答型」に統合した結果 **第3類型の元定義違反 2問混入**、自己検証ステータスに **FAIL 1 vs FAIL 0 の混在** が発生。

## 3. 検証した前提

- 前回 verdict: 必須修正3件（Critical C1 + Major M1+M2）+ 推奨修正4件
- refinement完了報告: ALL_RESOLVED（C1=4類型再構成 / M1=実DB値統一 / M2=起源訂正）
- 検証手段: 独立 SQL再集計、grep全件残存チェック、HTMLタグバランス

## 4. 実施した検証

1. **C1 残存チェック**: 「5類型」「全装置不応答」「Q-N07.*M02」grep
   → handoff L66/L88/L114/L134/L167 + verification L231/L264 + report L677/L681/L701 に **5類型表現が9箇所残存**

2. **M1 残存チェック**: 旧値 grep
   → analysis.html **L193/L194/L207/L276/L329 に5箇所未修正**（report.html / handoff.md は修正完了）

3. **M2 残存チェック**: 「handoff §6.2 = M09」逆帰属
   → handoff §7.6 (L128) と verification callout L251 は訂正完了
   → ただし verification **L268, L307 に逆帰属表現2箇所残存**

4. **新たな論理整合性違反**: 第3類型「研究応答型」の元定義 = 「SG+UPR+SGRD の 3装置のうち 2装置以上 score≥3」
   - Q-N07: SG=0, UPR=5, SGRD=0 → 1装置のみ ≥3 **（定義違反）**
   - Q-M02: SG=2, UPR=5, SGRD=0 → 1装置のみ ≥3 **（定義違反）**
   - report L551 の例外条項では救済不能、MECE性毀損

5. **DB 装置別平均スコア再集計**: 6装置完全一致、Funding のみ 0.01 差（DB 2.13 vs 記載 2.12）

6. **MAX(score) GROUP BY question_id**: max≤2 = 0問 ✓

7. **Initiatives DB 463件**: source_db別 SG 115/IR 105/Policy 102/Funding 88/SGRD 24/UPR 15/Sangaku 14=463 完全一致

8. **HTMLタグバランス**: analysis 28/28, verification 18/18, report 247/247 ✓

9. **自己検証ステータス内的不整合**:
   - handoff L9 「PASS 15 / PARTIAL 1 / FAIL 0」
   - verification L295 「PASS 15・FAIL 1」
   - verification L317 「PASS 15・PARTIAL 1・FAIL 0」
   → **FAIL 1 と FAIL 0 が混在**

10. **第4類型「SG単独応答型」MECE再検証**: 8問のうち Q-N02/Q-N06/Q-V02 の **3問が「SG のみ score≥3」定義違反**（IR でも score≥3）。前回見落としの構造的瑕疵。

## 5. 所見

### Critical（リリースブロッカー）

- **C1-r2: 第3類型「研究応答型」の定義違反 2問混入（新規）** — 報告書 §4.4 参照
- **M1-r2: analysis.html の IR/Funding 数値が完全未修正（refinement漏れ）** — L193/L194/L207/L276/L329 の5箇所

### Major

- **C1-r2-b: 「5類型」表現の残存 6箇所** — handoff/verification/report
- **M2-r2: M09/M10 起源訂正の部分残存 2箇所** — verification L268, L307
- **新規: 自己検証ステータス数値不整合** — FAIL 1 vs FAIL 0 混在

### Minor

- m1: Funding 平均 2.12 vs 2.13 丸め由来 0.01 差
- m2: 第4類型 MECE違反 3問（Q-N02/Q-N06/Q-V02）
- m3: Q-V07 言及 5箇所が B-4 評価範囲外
- m4: B-2 14問 ∩ B-4 24問 交差Q-IDリスト未明示
- m5: B-3 30問独立性注記なし

## 6. リスク評価

- **技術的リスク: 高**（前回より悪化）— ALL_RESOLVED 報告の信頼性崩壊
- **運用リスク: 高** — 「4類型」「5類型」混在 + 第3類型定義違反が B-5 に連鎖
- **ユーザー影響: 中** — 数理基盤は信頼可能だが解釈レイヤー悪化

## 7. 採用判定

| 領域 | 判定 |
|---|---|
| 168セル集計基盤 | 採用 |
| 装置別平均スコア（Funding除く） | 採用 |
| Initiatives DB 463件 | 採用 |
| 補完類型1（全装置応答型） | 採用 |
| 補完類型2（制度+市場応答型） | 条件付き採用 |
| **補完類型3（研究応答型）** | **採用拒否（定義違反）** |
| 補完類型4（SG単独応答型） | 条件付き採用 |
| **装置レコード規模（analysis.html）** | **採用拒否（5箇所未修正）** |
| 装置レコード規模（report/handoff） | 採用 |
| **M09/M10起源（verification L268, L307）** | **採用拒否（部分残存）** |
| ホライズン別平均 | 採用 |
| **自己検証ステータス整合性** | **採用拒否（FAIL混在）** |

## 8. Sentinel 最終コメント

refinement-coordinator が「ALL_RESOLVED」と報告したにもかかわらず、独立検証で重大な未履行が発見された。これは前回 sentinel verdict の信頼性ではなく、**refinement プロセスの完了判定精度に関わる構造的問題**。

特に深刻なのが、**C1 修正の再構成方針そのものが新たな整合性違反を生んだ点**。Q-N07/Q-M02 を「研究応答型」に統合する判断は UPR=5 のみを根拠にし、第3類型の元定義「SG+UPR+SGRD のうち 2装置以上 score≥3」と整合しない。前回 verdict §9 の「新類型『研究系・UPR強応答型』または既存類型2/3に再分類」助言を refinement は表層的に「第3類型に統合」と読み替えただけで、定義側の整合まで詰めていない。

**より根本的な解決策**:
- 案A': 第3類型を「**SG/UPR/SGRD のいずれか1装置以上で score≥3 かつ Policy/IR/Funding/Sangaku すべてで score≤2**」と再定義
- 案B': Q-N07/Q-M02 を「**UPR 単独強応答型**」として **第5類型として独立**（旧「全装置不応答型」とは異なる定義）

完了判定時に「修正必要箇所 N → 修正済み箇所 N」の同等性チェックスクリプトを必須化すべき。

## 9. 次アクション（Wave 3 起動可否）

### Wave 3（B-5）起動可否: **REJECT / 起動不可**

差し戻し先: **Stage 4 Refinement（再 Round 2）**

### 必須再修正項目

1. **【Critical】analysis.html の IR/Funding 数値完全修正**
   - L193「1,862,236 セクション」→ 1,769,821 セクション
   - L194「1,927 ラウンド」→ 2,001 ラウンド + 「4,180 組織」→ 4,264 組織
   - L207/L276/L329「1.86M セクション」→ 1.77M セクション

2. **【Critical】第3類型の定義整合性確保**
   - **案B' 推奨**: Q-N07/Q-M02 を「UPR 単独強応答型」として第5類型（旧と異なる定義）に独立。4類型→5類型に再構成
   - もしくは案A': 第3類型定義変更
   - report L551, L564, L568 / handoff L44, L91, L114 を整合的に修正

3. **【Major】「5類型」残存表現の全件修正**
   - handoff L66, L167 / verification L231, L264 / report L677, L681, L701（または「5類型」を採用するなら整合化）

4. **【Major】M09/M10 起源訂正の残存修正**
   - verification L268, L307 を「ブリーフィングの確定指定を採用」に書き換え

5. **【Major】自己検証ステータス整合化**
   - handoff L9 / verification L295/L317 で「FAIL 1」または「FAIL 0」のいずれかに統一

### refinement-coordinator への申し送り（Round 2 必須）

- 次回 ALL_RESOLVED 報告前に必須実行: `grep -n "1.86M\|1,862,236\|1,927\|4,180\|5 類型\|5類型\|5 補完類型\|5補完類型" *.html *.md`
- 修正範囲を「report.html + handoff.md」に限定せず、**全 4 ファイル統一修正**を必須化
- 修正方針が新たな整合性違反を生んでいないか SQL検証 1コマンドで判定可能（`SUM(CASE WHEN score>=3 THEN 1 ELSE 0 END) GROUP BY question_id`）
