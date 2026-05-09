# Track B-5 完了引継ぎ書

## 1. メタ情報
- トラック番号: B-5（Phase B 規範層 × 実装層 接合）
- トラック・タイトル: 動きの状況測定 — B-3 30問 × B-4 7装置 = 210セル
- 入力源: Track B-3 30 問 + Track B-4 168 セル + Track B-2 85 wisdom + Phase A Track 9 善い社会論述 + _TRACK_LINKAGE_MATRIX.md
- 担当: Track B-5 リード
- 完了日: 2026-05-09
- 検証ステータス: 自己検証完了（17 項目 / PASS 17 / WARN 0 / FAIL 0） / doc-verify 待機 / sentinel 待機
- 出力ファイル:
  - `track-b5-current-momentum-analysis.html`（解析編・約 16,000 字）
  - `track-b5-current-momentum-verification.html`（検証編・4 カテゴリ 17 項目）
  - `track-b5-current-momentum-report.html`（レポート編・約 17,000 字 + 210 セルマトリクス + zone マップ + TOP10 + 三軸表）
  - `track-b5_handoff.md`（本ファイル）

## 2. 評価スコープ
- 対象: B-3 30 問 × B-4 7 装置 = 210 セル
- B-3 30 問の内訳: 群I (near 12 問) + 群II (mid 10 問) + 群III (far 5 問) + 群IV (very-far 3 問)
- B-4 7 装置: SG (Signal 7,668) / UPR (大学PR 41,760) / SGRD (企業R&D PR 36,734) / Policy (政策 30,118) / IR (有報セクション 1,769,821) / Funding (16,642 PR + 2,001 ラウンド + 4,264 組織) / Sangaku (492,646 レコード)
- 実 DB 値継承セル: 154 (22 問 × 7 装置)
- N/A セル: 56 (8 問 × 7 装置 = B-4 24 問評価対象外)

## 3. 主要数値（確定値）

### 3.1 zone 弁別最終確定
- **Hot zone** (n≥3≥5): **4 問** (G-N10 / G-N11 / G-N12 / G-M02)
- **Warm zone** (n≥3=3-4): **9 問** (G-N01 / G-N02 / G-N03 / G-N04 / G-N05 / G-N06 / G-F02 / G-F05 / G-V02)
- **Cool zone** (n≥3=1-2): **9 問** (G-N07 / G-N08 / G-N09 / G-M08 / G-M09 / G-M10 / G-F01 / G-F04 / G-V01)
- **Dead zone** (n≥3=0): **0 問** (実 DB 値継承組では該当なし)
- **N/A** (B-4 対象外): **8 問** (G-M01 / G-M03 / G-M04 / G-M05 / G-M06 / G-M07 / G-F03 / G-V03)
- 合計: 4 + 9 + 9 + 0 + 8 = **30 問** ✓

### 3.2 戦略的空白 13 問（43.3%）
| カテゴリ | 件数 | 該当問いID |
|---|---|---|
| Pluriverse 装置応答最薄組 | 5 | G-N07 / G-N08 / G-N09 / G-M10 / G-F01 |
| Care 装置観測不能組（高重要） | 2 | G-M01 / G-M03 |
| 世代間正義 装置観測不能組（最高重要） | 2 | G-M04 / G-M05 |
| Slow Right 装置観測不能組 | 3 | G-M06 / G-M07 / G-F03 |
| 自己言及（最高重要） | 1 | G-V03 |
| **合計** | **13** | — |

### 3.3 critical juncture × Phase A Mサイン接続率（B-3 sentinel verdict MJ-02 統一基準）
- **厳密接続（真M+準M限定）**: **4/8 = 50%**（JCT-01/02 = 真Mサイン物語転換期、JCT-03 = 準Mサイン非西洋認識論、JCT-05 = 準Mサイン世代間正義）
- **概念整合含む（+ 概念整合第四変容期）**: **6/8 = 75%**（+ JCT-04/07 = 概念整合第四変容期）

### 3.4 ホライズン別 zone 分布
| ホライズン | Hot | Warm | Cool | N/A | 合計 |
|---|---|---|---|---|---|
| near (12問) | 3 | 6 | 3 | 0 | 12 |
| mid (10問) | 1 | 0 | 3 | 6 | 10 |
| far (5問) | 0 | 2 | 2 | 1 | 5 |
| very-far (3問) | 0 | 1 | 1 | 1 | 3 |
| **合計** | **4** | **9** | **9** | **8** | **30** |

### 3.5 マトリクス基本数値
- 210 セル中、実 DB 値継承: 154 セル (73.3%)
- N/A セル: 56 セル (26.7%)
- 実 DB 値セル中の score≥3: 74 セル (48.1%)
- 実 DB 値セルの平均スコア: 2.40

## 4. 主要発見 3 点

### 主要発見 1: Hot/Warm/Cool/Dead zones 弁別の最終確定値とシナリオ非対称性
30 問は Hot 4 / Warm 9 / Cool 9 / Dead 0 / N/A 8 に分布。**Hot 4 問すべてが Care シナリオ系列（G-N10/N11/N12/M02）に集中**し、5 シナリオ間で「動きあり×wisdom 厚（Care）/ 動き薄×wisdom 厚（Pluriverse・Slow Right）/ 動きあり×wisdom 薄（Fragmentation・Techno）」の三類型構造が浮かび上がった。「動きと wisdom の両方が厚い領域」「両方薄い領域」が存在しないことは、B-3 5 シナリオ設計が構造的に偏った経路集合であることの定量的確認となる（B-3 設計の精度を逆に裏付ける）。

### 主要発見 2: ミラツク優先領域 TOP10 の二軸構造
TOP10 構成は**左上象限（戦略的空白×高重要）4 問 + 右上象限（即実装×高重要）4 問 + メタ独自 1 問 + 中央 1 問**で、戦略的空白への投資と既存軌道の強化を 4:4 で均衡させる設計となった。1 位 G-M04（世代間正義の憲法化）・2 位 G-N09（先住民知識主権）・3 位 G-M01（GDP 代替ケア指標）・8 位 G-N07/G-N08（非西洋認識論の方法論化）・9 位 G-V03（自己言及メタ）が左上+メタの 5 問でミラツクの中長期戦略の核を構成する。右上 4 位 G-N12 / 5 位 G-N10 / 6 位 G-N11 / 7 位 G-M02 はすべて Care 系列で即実装可能領域となる。

### 主要発見 3: 戦略的空白 13 問（43.3%）の戦略的含意 — 「Mサイン強接続 ⇔ 装置応答薄」の構造的非対称性
戦略的空白 13 問（30 問の 43.3%）は「規範的に重要であるにもかかわらず現代社会の装置で観測不能な問いが半数近く存在する」構造的事実を示す。critical juncture × Mサイン階層接続強度を分析すると、**Mサイン強接続（真M+準M）ほど装置応答薄、Mサイン弱接続ほど装置応答強**という構造的非対称性が確認された。具体的には JCT-03（準Mサイン非西洋認識論）と JCT-05（準Mサイン世代間正義）が「準Mサイン × 装置観測薄」の二重条件で介入余地最大となる。これはミラツクが「動きを生む側」として参画する余地が、装置応答薄かつ Mサイン接続強の領域に最大に開かれることを示す。

## 5. 強みと弱み

### 5.1 本Track の強み
- 主強み: B-3 30 問 × B-4 7 装置 = 210 セルの統一マトリクスを構築し、zone 弁別と二軸ランキングで「ミラツク介入余地最大領域」を定量的に特定
- 副強み: B-3 sentinel verdict C-05「連結IDマトリクス不在」を _TRACK_LINKAGE_MATRIX.md 継承で解消、B-1 41 ↔ B-2 14 ↔ B-3 30 ↔ B-4 24 の連結整合を確認
- 副強み: B-4 sentinel verdict R3 で確定した正値（IR sections 1,769,821 / Funding rounds 2,001 等）を honest 継承し、ハルシネーション残存ゼロ

### 5.2 本Track の弱み
- 主弱み: B-3 → B-1 マッピングは推定であり、B-3 リードの最終確認が未完了
- 副弱み: 方向性 P/R/B はセルレベルでなく問いレベルで付与（B-6 統合で精緻化推奨）
- 副弱み: N/A 8 問の補完判定（B-2 wisdom + Phase A Mサイン接続）は本Track 独自設計で、別の方法論を採用した場合は別の結果となり得る

### 5.3 強みホライズン / 強みCTL-1
- 強みホライズン: near（12 問・100% カバー、Hot 3 + Warm 6 + Cool 3）
- 構造的弱点ホライズン: mid（10 問・60% N/A、装置盲点集中）
- 強みCTL-1: V (価値観・倫理・文化) — 30 問中の主要分類で wisdom 接続強
- 構造的弱点CTL-1: T (技術・知) — Techno 系列が Warm 偏重で Hot ゼロ

## 6. 連結ID（Track B-6 への引継ぎ）

### 6.1 Track B-6 への引継ぎ（重点）
本Track は Track B-6「Phase B 統合HTML化」の主要構成要素として機能する。引継ぎ六点:

1. **210 セル動きスコアマトリクス**: B-6 master-report.html の主要中核図として引用。本Track レポート編 §2 のヒートマップを SVG 化推奨
2. **Hot/Warm/Cool/Dead zones マップ**: B-6 で四象限図を立体化（実装可能性 × 重要性 × ホライズン）
3. **戦略的空白 13 問のリスト**: B-6 master-report.html の主要発見セクションに引用、特に critical 5 問（G-M04/G-N09/G-M01/G-N07-08/G-V03）を強調表示
4. **ミラツク優先領域 TOP10**: B-6 master-report.html の意思決定支援セクションに引用、各問いのミラツクアクション仮説を別建てで詳細化
5. **critical juncture × シナリオ × 装置応答 三軸表**: B-6 で立体図化（時期軸 × Mサイン階層軸 × 装置観測可能性軸）
6. **連結ID マトリクスの統合継承**: _TRACK_LINKAGE_MATRIX.md を B-6 master-report.html の B-1 41 + B-3 30 = 71 問統合インデックスとして継承

### 6.2 Track B-6 master-report.html での提示推奨

1. **マスター三角形**: B-1 41 問 ↔ B-2 14 wisdom ↔ B-3 30 規範 ↔ B-4 168 装置応答 の Phase B 全体構造を可視化
2. **動きの zone マップ**: 本Track の四象限図（Hot/Warm/Cool/N/A）を時間軸（near/mid/far/very-far）で展開
3. **TOP10 タイル**: 各問いのカード（zone・JCT・wisdom 接続・推奨アクション）
4. **戦略的空白 13 問の特集セクション**: critical 5 問は別建てで詳細化
5. **シナリオ × 装置応答ヒートマップ**: 5 シナリオ × 7 装置 の集計（本Track のレポート編 §3.3 を別図化）
6. **三類型構造図**: 動きあり×wisdom 厚 / 動き薄×wisdom 厚 / 動きあり×wisdom 薄 の三類型を概念図化

### 6.3 Track B-6 への留意事項
- B-3 sentinel verdict「pluriverse 序列化禁止原則」を厳守: 5 シナリオを規範的に序列化せず構造的非対称性として記述
- B-4 sentinel verdict R3 の「5 類型（新定義: UPR 単独強応答型を含む）」を採用、旧第 5 類型「全装置不応答型」は廃止された事実を引き継ぐ
- critical juncture × Mサイン接続率は「厳密 4/8 = 50% / 概念整合含む 6/8 = 75%」の二系列で開示

## 7. 既知の限界（自己認識）

1. **B-3 → B-1 マッピングの推定性**: B-3 handoff には明示マッピング表が存在せず、本Track は _TRACK_LINKAGE_MATRIX.md §2.4 の推定マッピングを使用。B-3 リードの最終確認が未完了。
2. **複数 Q 問への継承の MAX 採用**: G-N12 / G-F04 / G-F05 / G-V01 で MAX(score) を採用。AVG/SUM/MIN を採用した場合は別の結果となる。
3. **N/A 8 問の補完判定の独自設計**: 本Track は「B-2 wisdom + Phase A Mサイン階層 + JCT 接続強度」で代替評価する設計を採用した解釈であり、別の方法論を採用した場合は別の結果となる。
4. **方向性 P/R/B の問いレベル付与**: セルレベル付与は実施せず、問い単位で「主に P か R か B か」を judg した暫定値。B-6 統合段階で精緻化推奨。
5. **二軸ランキングの主観性**: Y 軸の重み付け（真Mサイン+3 / 準Mサイン+3 / 概念整合+2 / cross +2 / wisdom 厚+2 等）は解釈であり、別の重み付けで TOP10 順位は入れ替わり得る。
6. **critical 5 問の選定**: 戦略的空白 13 問のうち critical 5 問の選定は解釈であり、別の選定基準で順位は入れ替わり得る。
7. **pluriverse 序列化禁止原則の遵守**: 「Pluriverse 系列がミラツクの介入余地最大」という構造記述は「介入余地」の構造記述であり、「Pluriverse シナリオが望ましい」という規範的序列化ではない。
8. **5 補完類型に依存しない設計**: 本Track は B-4 sentinel verdict §9 が指示する「5 補完類型に依存しない独自設計」を採用。zone 弁別は MAX(score) GROUP BY question_id で独自に実施。

## 8. ミラツク独自知見の候補

1. **「規範層 × 装置観測の交差で動きの状況を測定する」方法論**: ミラツク以外で「規範問い 30 × 変化検出装置 7 = 210 セル」のマトリクスを構築する組織は希少。本Track の方法論はミラツク固有の領域診断ツールとして機能。

2. **「Mサイン強接続 ⇔ 装置応答薄」の構造的非対称性の発見**: critical juncture × Phase A Mサイン階層接続強度と装置応答強度が逆比例することは、B-3 と B-4 の独立 Track 結果の交差で初めて検出される構造的事実。

3. **「動きあり×wisdom 厚 / 動き薄×wisdom 厚 / 動きあり×wisdom 薄」の三類型構造**: 5 シナリオを規範的序列化せず、構造的非対称性として三類型分類する分析手法は、政府機関・大手シンクタンクのフォーサイトでは見られないミラツク独自の整理。

4. **「自己言及メタ問い G-V03 を TOP10 に含める」設計**: 「2100 時点で振り返って Phase B が立てた 30 問は妥当だったか」という自己言及メタ問いを優先領域 TOP10 に含めるのは、ミラツクの自己診断 protocol を 5 年ごとに再評価する装置設計を意識した独自判断。

## 9. 統合用連結ID（_PROTOCOLS.md 6.2 標準フォーマット）

- **基盤Track**: B-3（30 問規範層）+ B-4（168 セル装置応答）+ B-2（85 wisdom）+ Phase A Track 9（善い社会論述）
- **強みホライズン**: near 12 問 + mid 4 問 + far 4 問 + very-far 2 問 = 22 問（実 DB 値継承）
- **強みCTL-1**: V（価値観）30 問中の主要分類
- **問い群総数**: 30 問（B-3 から継承）
- **多層化マトリクス**: 210 セル（30 問 × 7 装置）+ zone 弁別 (Hot 4 / Warm 9 / Cool 9 / Dead 0 / N/A 8) + TOP10 + 戦略的空白 13 問
- **連結IDマトリクス**: _TRACK_LINKAGE_MATRIX.md 継承（B-1 41 ↔ B-2 14 ↔ B-3 30 ↔ B-4 24）

### 9.1 補完が必要な領域
- B-6: Phase B 全体統合HTML化（本Track が一構成要素）
- B-3 リード: B-3 → B-1 マッピングの最終確認
- B-6: セル別方向性 P/R/B の精緻化（本Track は問いレベルのみ付与）

### 9.2 提供できる補完
- B-6 への 210 セルマトリクス + zone マップ + TOP10 + 戦略的空白 13 問 + 三軸表
- B-6 への連結ID マトリクス整合確認結果
- B-6 への「Mサイン強接続 ⇔ 装置応答薄」の構造的非対称性発見

## 10. 統合リードへの申し送り

### 特に強調してほしい発見
1. **Hot 4 問すべてが Care シナリオ独占**: G-N10/G-N11/G-N12/G-M02 が現代社会の装置で観測される即実装可能領域を独占し、Care シナリオが「既存軌道強化型」として位置づけられる。
2. **戦略的空白 13 問（43.3%）の存在**: B-3 30 問の半数近くが「規範的に重要であるにもかかわらず装置で観測不能」な構造的事実。critical 5 問（G-M04 世代間正義 / G-N09 先住民知識主権 / G-M01 GDP 代替ケア指標 / G-N07-08 非西洋認識論 / G-V03 自己言及メタ）がミラツクの中長期戦略の核。
3. **「Mサイン強接続 ⇔ 装置応答薄」構造的非対称性**: 真Mサイン JCT-01/02 は装置応答強（既存軌道）、準Mサイン JCT-03/05 は装置応答薄（介入余地最大）。ミラツクが「動きを生む側」として参画する余地は装置応答薄×Mサイン強接続の領域に最大に開かれる。

### 他 Phase B Track との矛盾候補
- **B-3「8 critical juncture が観測可能と仮定」 vs B-4「変化検出装置の現実的カバレッジ」**: B-4 確定後の本Track 解析で、JCT-04（ケア経済）は near 強応答だが mid 装置盲点（G-M01/G-M03）の二極化、JCT-05（世代間正義）は装置観測完全不能、JCT-07（ゆっくりの権利）は B-4 対象外であることを確認。B-3 verification.html §4.3 WARN は本Track の解析で部分解消（厳密 50% / 概念整合 75% の二系列開示）。

### Phase B Wave 4（B-6）への送り事項
- B-6 着手時: 本Track の 210 セルマトリクス + zone マップ + TOP10 + 戦略的空白 13 問 + 三軸表を master-report.html の主要構成要素として統合
- B-6 master-report.html では「規範層（B-3 30 問）+ 歴史的回答（B-2 85 wisdom）+ 装置観測（B-4 168 セル）+ 動き測定（B-5 210 セル）」の四層構造を立体化
- B-6 では SVG/Sankey 化を実施: ヒートマップ・四象限図・三軸表
- B-6 では 71 問統合インデックス（B-1 41 + B-3 30）を提示
- B-6 では「Mサイン強接続 ⇔ 装置応答薄」の構造的非対称性を Phase B 主要発見として強調

## 11. 自己検証サマリー

- カテゴリA（スナップショット不整合）: 5/5 PASS
- カテゴリB（ハルシネーション）: 4/4 PASS
- カテゴリC（カバレッジギャップ）: 4/4 PASS
- カテゴリD（チーム間不整合）: 4/4 PASS
- 合計: 17 項目 / **PASS 17 / WARN 0 / FAIL 0**
- 詳細: `track-b5-current-momentum-verification.html`
- HTMLタグバランス: analysis.html 40/40 div + 9/9 section + 8/8 table + 1/1 main + 1/1 nav / verification.html 16/16 div + 6/6 section + 1/1 table / report.html 377/377 div + 10/10 section + 8/8 table + 1/1 main + 1/1 nav

## 12. 用語統一（B-5 briefing 申し送り遵守）

本Track 内で以下の用語を統一して使用:

- 「真M由来」「準M由来」「概念整合由来」「単独T由来」「Track 5 long-shadow」（Phase A Mサイン階層）
- 「Pluriverse」（シナリオ名・大文字）/ 「pluriverse」（概念・小文字）
- 「critical juncture」「JCT-01〜JCT-08」（B-3 8 分岐点）
- 「wisdom」（B-2 5 traditions 抽出）
- 「coverage_scores」（B-4 装置応答スコアテーブル）
- 「zone（Hot/Warm/Cool/Dead/N/A）」（本Track の弁別 5 階層）
- 「戦略的空白」（左上象限・低実装×高重要）
- 「動きの方向違い」「warning」（右下象限候補）
- 「動きはないが重要」「opportunity」（左上象限候補）

## 13. データソース・再現性

### 13.1 SQL 再現コマンド

```sql
-- 24問×7装置スコアマトリクス（B-4 24問の MAX score）
SELECT question_id,
  MAX(CASE WHEN system_name='SG' THEN score END) AS SG,
  MAX(CASE WHEN system_name='UPR' THEN score END) AS UPR,
  MAX(CASE WHEN system_name='SGRD' THEN score END) AS SGRD,
  MAX(CASE WHEN system_name='Policy' THEN score END) AS Policy,
  MAX(CASE WHEN system_name='IR' THEN score END) AS IR,
  MAX(CASE WHEN system_name='Funding' THEN score END) AS Funding,
  MAX(CASE WHEN system_name='Sangaku' THEN score END) AS Sangaku
FROM coverage_scores
GROUP BY question_id
ORDER BY question_id;

-- zone 弁別（独自設計、5類型非依存）
SELECT 
  CASE 
    WHEN n_strong >= 5 THEN 'Hot'
    WHEN n_strong BETWEEN 3 AND 4 THEN 'Warm'
    WHEN n_strong BETWEEN 1 AND 2 THEN 'Cool'
    ELSE 'Dead'
  END AS zone,
  COUNT(*) AS n_questions
FROM (
  SELECT question_id, COUNT(CASE WHEN score>=3 THEN 1 END) AS n_strong
  FROM coverage_scores
  GROUP BY question_id
)
GROUP BY zone;
```

### 13.2 マッピング根拠ファイル
- B-3 30 問体系: `track-b3_handoff.md` §4
- B-3 → B-1 推定マッピング: `_TRACK_LINKAGE_MATRIX.md` §2.4 + `_TRACK_B5_INPUT_DATA.md` §0.2
- B-1 → B-4 24 問選定: `track-b4_handoff.md` §2
- B-4 sentinel 設計指示: `track-b4-sentinel-verdict-r3.md` §9
- B-3 sentinel 申し送り: `track-b3-sentinel-verdict.md` (MJ-02 統一基準)
- B-2 wisdom 配分: `track-b2_handoff.md` + `track-b3_handoff.md` §2.2

### 13.3 入力データ pre-build 継承
本Track は Wave 3 起動高速化のため pre-build された以下の補助文書を継承:
- `_TRACK_B5_INPUT_TEMPLATE.md` — 雛形構造
- `_TRACK_B5_INPUT_DATA.md` — 210 セル動きスコア確定版（coverage_scores 直接参照）
- `_TRACK_B5_SCENARIO_PATH_ANALYSIS.md` — シナリオ別経路解析（18K字、6章）
- `_TRACK_LINKAGE_MATRIX.md` — 連結IDマトリクス
- `_TERMINOLOGY_GLOSSARY.md` — 用語集

これら pre-build 成果は本Track の解析編・レポート編・検証編に統合され、Wave 3 の時間管理を効率化した。

---

最終更新: 2026-05-09
作成: Track B-5 リード
参照: track-b5-current-momentum-{analysis|verification|report}.html / initiatives.db / B-3 handoff §4 / B-4 sentinel verdict R3 / _TRACK_LINKAGE_MATRIX.md / _TRACK_B5_INPUT_DATA.md / _TRACK_B5_SCENARIO_PATH_ANALYSIS.md
