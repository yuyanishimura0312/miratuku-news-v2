# Track B-4 Sentinel 最終ゲート判定書

判定日: 2026-05-09
判定者: Sentinel（Devil's Advocate / VETO権付き最終ゲート）
対象: track-b4-detection-systems-{analysis,verification,report}.html + track-b4_handoff.md + initiatives.db
入力検証根拠: track-b4-doc-verify-report.md（CONDITIONAL PASS、重大1+要修正3+WARN4）

## 1. 判定

**CONDITIONAL APPROVAL（条件付承認）— Wave 3 起動は必須修正完了後**

doc-verify の CONDITIONAL PASS を独立支持。Sentinel独自評価で、**B-02 ハルシネーション（第5補完類型）は Wave 3 への波及リスクが定量的に大きい**ため、Wave 3 起動前の必須修正に格上げ。

## 2. 要約

168セルマトリクスの集計プロセス・装置別平均スコア・Initiatives DB（463件）・7装置の実在性・168セル全公開といった**数理基盤は完全に健全**。一方、解釈段で **(a) 「全装置不応答型」の重大ハルシネーション、(b) IR/Funding 装置メタ情報乖離、(c) M09/M10 起源の逆帰属** が確認された。修正範囲は限定的だが、誤ったまま B-5 が継承すると 5補完類型分類全体が破綻。

## 3. 検証した前提

- B-1 handoff §6.2 指定の Q-prefixed 24問（near 13 / mid 6 / far 3 / very-far 2）
- 7装置: SG/UPR/SGRD/Policy/IR/Funding/Sangaku
- 168 cells (24×7), 装置別スコア 0-5
- B-1 修正後ラベル + B-2 sentinel verdict 継承
- doc-verify 16項目（PASS 8 / 要修正 3 / WARN 4 / 重大 1）

## 4. 実施した検証

1. **B-02 ハルシネーション独立再現** — coverage_scores SQL 直接実行: Q-N07 UPR=5(82) / Q-M02 UPR=5(34)。「すべて score≤2」の定義違反。
2. **「全装置不応答型」存在検証** — `MAX(score) GROUP BY question_id` で全24問。max≤2 = **0問**。第5補完類型は実体ゼロ。
3. **装置別平均スコア再算** — Funding=2.13（DB） vs 2.12（記載）丸め差0.01、他完全一致。
4. **装置レコード規模実体照合** — IR sections **1,769,821**（記載「1.86M / 1,862,236」▲92,415乖離）、Funding rounds **2,001**（記載 1,927）、organizations **4,264**（記載 4,180）。verification §2.1 「合算」説明は算術不成立。
5. **5補完類型 MECE 検証** — 6+4+4+8+2=24 総数OK。Q-N09 類型2 包含は IR=5/Funding=3 で実装適合。
6. **M09/M10 起源逆帰属確認** — B-1 handoff §6.2 line 63 = M10 / B-1 report = M10 / briefing line 23 = M09 変更。B-4 verification §4.1 と handoff §7.6 の「B-1 handoff §6.2 が M09」記述は事実逆。
7. **Initiatives 463件実在性** — count(*)=463、source_db別 SG 115/IR 105/Policy 102/Funding 88/SGRD 24/UPR 15/Sangaku 14=463 完全一致。
8. **7装置 DB 実在性** — IR Collector ir.db (33GB)・Policy DB・Signal DB・Investment Signal v2 DB 4本実在確認。

## 5. 所見

### Critical（リリースブロッカー / Wave 3 起動阻害）

- **C1: 第5補完類型「全装置不応答型」が DBと矛盾するハルシネーション**
  根拠: Q-N07 / Q-M02 ともに UPR で score=5 獲得。max≤2 問い 0問。
  影響: B-5 dead zones判定が連鎖破綻、B-6 に永続化。
  該当箇所: report.html L565-566（図5）、handoff.md L42-44, L58, L165

### Major（早急対応 / Wave 3 起動はブロックしない）

- **M1: 装置レコード規模乖離**
  IR sections 1,862,236 vs 実値 1,769,821（▲92,415、4.97%差）、Funding rounds 1,927→2,001、organizations 4,180→4,264。
  該当箇所: report.html L221, L523, L533、verification.html L186、handoff.md L28-29

- **M2: M09/M10 起源誤帰属（チーム間不整合）**
  B-1 handoff §6.2 line 63 = M10、briefing line 23 = M09 変更。verification §4.1 / handoff §7.6 の「handoff §6.2 が M09」は事実逆。
  該当箇所: verification.html L251-252、handoff.md L130

### Minor

- m1: Funding平均 2.12 vs 2.13 丸め由来
- m2: Q-V07 言及は B-4 24問 評価範囲外
- m3: B-2 14問 ∩ B-4 24問 交差Q-IDリスト未明示
- m4: B-3 30問独立性注記なし

## 6. リスク評価

- 技術的リスク: **中**（集計基盤は健全、解釈段に局所誤り）
- 運用リスク: **高**（B-5 が誤類型継承で判定破綻のリスク）
- ユーザー影響: **低〜中**（数理基盤は信頼可能、解釈レイヤー誤）

## 7. 採用判定

| 領域 | 判定 |
|---|---|
| 168セル集計基盤 | 採用 |
| 装置別平均スコア（Funding除く） | 採用 |
| Initiatives DB 463件 | 採用 |
| 補完類型1〜4 | 採用 |
| **補完類型5「全装置不応答型」** | **採用拒否（修正後再提出）** |
| 装置レコード規模メタ情報 | **採用拒否（実DB値で再記述後採用）** |
| M09/M10起源帰属 | **採用拒否（事実訂正後採用）** |
| ホライズン別平均 | 採用 |
| B-1 strong findings 整合 | 採用 |

## 8. Sentinel 最終コメント

doc-verify の精度は高く、独立再検証で 16項目すべて再現。「集計プロセスは健全、解釈言語化に局所的誤りが混入」診断は的確。Sentinel は doc-verify よりも 1段階厳しい判断: B-02 ハルシネーションは Wave 3 への波及リスクが定量的に大きいため、必須修正に格上げ。

修正コストは小さい（report L565-566 + handoff L42-44 + L58 + L165 計4箇所）。SQL再集計（max≤2=0、よって類型5を削除し4類型に再構成）で30分以内完了。

実装者・QA担当へのフィードバック:
- **強み**: 168セル統一マトリクス、SQL再現性、Initiatives DB 463件、7装置選定根拠、ホライズン別平均は Phase A〜B 屈指の品質
- **改善点**: 集計値→分類言語化の照合を SQL `MAX(score) GROUP BY question_id` 1コマンドで事前検証すべき。Phase A Track 4 r2 「キーワードgrepチェックリスト」教訓未活用
- **構造的助言**: 装置メタ情報を db_meta.json で自動引用する設計に切り替えれば M1 系乖離は構造的防止可能
- **称賛**: doc-verify 自身が「自己検証 §2.4 が PASS と判定したが B-02 を見逃した」と認めた検証文化は高評価

## 9. 次アクション

### Wave 3（B-5）起動可否: **保留 / 必須修正完了後に起動可**

### 必須修正項目（B-5 起動前）

1. **【Critical】第5補完類型処理**
   - report.html L565-566 図5 から「Q-N07, Q-M02 = 全装置不応答型」削除
   - 案A（推奨）: 類型5削除し 4類型構成に再構成。Q-N07/Q-M02 を新類型「研究系・UPR強応答型」または既存類型2/3に再分類
   - 案B: 定義を「7装置中5装置以上で score≤1」に変更し SQL再集計
   - handoff.md L42-44, L58, L165 同期修正
   - verification.html §2.4 で DB値クロスチェック

2. **【Major】装置レコード規模実DB値整合**
   - report.html L217, L221, L523, L533 IR sections「1,862,236 / 1.86M」→ **1,769,821** 統一
   - Funding rounds **2,001** / organizations **4,264** に修正
   - verification.html L186 「合算的記述」説明撤回
   - handoff.md L28-29 実DB値再記述

3. **【Major】M09/M10 起源誤帰属訂正**
   - verification.html L251-252 を「B-1 handoff §6.2 と B-1 report は両方とも M10。**ブリーフィング (`_TRACK_B4_BRIEFING.md` L23) が M09 に変更**したため、B-4 はブリーフィング指定に従い M09 を採用」に書き換え
   - handoff.md L130 同様訂正

### 推奨修正項目（B-5 起動と並行可、B-6 統合前完了）

4. Funding平均 2.12 → 2.13 統一
5. Q-V07 言及の範囲外明示
6. B-2 14問 ∩ B-4 24問 Q-ID リスト明示
7. B-3 30問独立性注記

### B-5 リードへの引継ぎ事項（修正完了前提）

- coverage_scores テーブル 168行 は SQL直接参照可
- 5類型分類は再分類完了後に継承。それまで独自に `MAX(score) GROUP BY question_id` で hot/dead zones抽出
- 装置レコード規模は修正後実DB値採用
- M09 採用は B-1 ではなく briefing 由来
