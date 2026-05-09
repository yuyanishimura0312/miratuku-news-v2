# Track B-4 軽微追補 Briefing（pre-build）

doc-verify 指摘 計16項目（PASS 8 / 要修正 3 / WARN 4 / 重大 1）に対する修正タスク

## 必須修正（重大 1 + 要修正 3）

### B-02【重大ハルシネーション】「全装置不応答型 Q-N07/Q-M02」分類の誤り
**事実**: DB実値で Q-N07 = UPR score 5 (count 82)、Q-M02 = UPR score 5 (count 34)。両問いとも UPR で最高位スコア達成。max_score≤2 の問いは 24 問中 **0 問**。

**修正対象**:
- report § 5（line 565-566）「全装置不応答型」分類削除 or 定義変更
- handoff §3 line 44 全装置不応答型記述削除
- handoff §4 主要発見 §3「全装置不応答型 2 問」削除
- 5補完類型 → 4補完類型に再構築（類型5を削除）
  - 全装置応答型 6 / 制度+市場 4 / 研究 4 / SG単独 8 / 不応答 0 → 単独UPR応答型 2 (Q-N07/Q-M02) で別カテゴリ化 or 既存分類への統合

**修正方法案**:
- A案: 「全装置不応答型 0問」に修正し、honest 開示で「想定していた装置不応答型は実体がなかった。Q-N07/Q-M02 は UPR 単独応答型として再分類」と注記
- B案: 5補完類型を 4補完類型に再編し、Q-N07/Q-M02 を「UPR 単独応答型」or「SG-UPR 補完型」に再配置

### A-03【要修正】IR sections の二重記載 + 数値乖離
**事実**:
- IR sections: report 内で「1,862,236」(line 217) と「1,769,821」(line 714) が両方存在
- 実DB: sections 1,769,821 / documents 72,502
- Funding rounds: 1,927 vs 実DB 2,001 (差 +74)
- Funding organizations: 4,180 vs 実DB 4,264 (差 +84)

**修正対象**:
- report line 217: 「1,862,236」→ 「1,769,821（sections のみ。documents 72,502 を加えると 1,842,323）」
- handoff §2 IR記述を実DB値に同期
- Funding 数値も実DB値に統一

### B-03【要修正】verification §2.4 自己検証の偽陽性
**事実**: verification §2 ハルシネーションカテゴリ全体で「4/4 PASS」と判定したが、B-02 の重大不整合を独立検証していない。

**修正対象**:
- verification §2 を 4/4 PASS → 3/4 PASS + 1/4 FAIL（B-02 検出）に修正
- 自己検証の十分性に欠けた点を honest 開示

### C-02【要修正】Q-V07 評価範囲外言及
**事実**: handoff §4 主要発見 §4 / §6.3 / §10 で Q-V07 を「装置不応答 = B-2 補完候補」として言及するが、Q-V07 は B-4 24問評価対象に含まれていない（24問は Q-V02/Q-V06 のみ）。

**修正対象**:
- handoff §4/§6.3/§10 で Q-V07 を「B-4 評価対象外」と明示し、score 0-1 集中の主張を撤回
- もしくは、B-1 全 41 問空間での主張として再分類

### D-01【要修正】M09/M10 起源の誤帰属
**事実**:
- handoff §7.6 と verification §4.1 主張: 「B-1 handoff §6.2 が M09、B-1 report が M10」
- 実態: B-1 handoff §6.2 と B-1 report の両方が M10
- M09 を指定したのは _TRACK_B4_BRIEFING.md (line 23)

**修正対象**:
- handoff §7.6 と verification §4.1 を事実に修正
- 起源帰属を「_TRACK_B4_BRIEFING.md が M09 を指定。本Track はそれに従う」に修正

## WARN対応（推奨修正 4件）

- A-02 Funding 平均スコア 2.12 vs 2.13 丸め差: 注記推奨
- C-03 類型2「制度+市場」の Q-N09 が定義不適合: 再分類 or 注記
- D-02/D-03/D-04: チーム間整合性の細部記述追加

## 制約
- DB（initiatives.db）の集計値・168セル・463 initiatives は変更しない（doc-verify で完全 PASS）
- 7装置実在性は変更しない（B-01 PASS）
- 集計プロセスの核心は健全（line 18）

## 完了基準
- B-02/B-03/A-03/C-02/D-01 の必須5件を解消
- HTMLタグバランス維持（analysis 28/28、verification 18/18、report 247/247）
- 5補完類型 → 4補完類型の構造的再編 or 「全装置不応答型 0問」への素直な honest 修正
- 完了報告: ALL_RESOLVED または PARTIALLY_RESOLVED + 残課題

iteration: 1/3
