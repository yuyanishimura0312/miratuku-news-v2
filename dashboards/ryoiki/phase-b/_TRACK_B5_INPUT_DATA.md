# Track B-5 入力データ確定版

> Track B-5「動きの状況測定」起動入力データの完全版（pre-build）。
> B-3 30問 × B-4 7装置 = 210セルマトリクスを、initiatives.db `coverage_scores` テーブルから直接抽出して構築。
> B-5 リードは hot/warm/cool/dead zones 弁別と二軸ランキングに集中できる状態にする。
>
> 作成日: 2026-05-09
> 作成: Track B-5 起動準備（B-4 軽微追補と並列、作業領域を侵さない）
> データソース: `~/projects/research/initiatives-db/initiatives.db`（B-4 構築・PASS済 coverage_scores 168行）
> 設計指針: B-4 sentinel 申し送りに従い、5補完類型に依存しない独自設計（`MAX(score) GROUP BY question_id` で hot/dead 弁別）
> 基準時点: B-3 30問は B-1 修正後 Mサインラベル + B-3 handoff §2 シナリオ wisdom 配分から逆引き

---

## 0. 設計思想と方法論

### 0.1 B-3 30問 と B-4 24問 の集合関係

Track B-3 と Track B-4 は別系列の問い体系である:

- **B-3 30問**（G-N01〜G-V03）: **規範層** — 善い社会像 × 主体 × 経路の問い
- **B-4 24問**（Q-N01〜Q-V06）: **実装層** — B-1 41問のうち B-4 sentinel 後 max_score≥3 で評価対象とした問い

B-3 30問は B-1 41問のうち抜粋ではなく、B-3 リードが新規に立てた問い体系。ただし B-3 handoff §2.2 のシナリオ別 wisdom 配分（B-2 wisdom が紐づく B-1 問いID）から、各 B-3 問いが「どの B-1 問いの規範的延伸か」を逆引きできる。

本データセットでは、テンプレート §1 の【推定】マッピングに従い、B-3 G問のスコアを B-1 Q問の coverage_scores 実値から継承する設計を採用。これにより 210セルのうち実DB値継承可能なセルを最大化する。

### 0.2 マッピング表（B-3 G問 → B-1 Q問）

B-3 handoff §2.2 と本テンプレート §1 / §4.1 を統合した連結（テンプレート §1 §4.1 から確定）:

| B-3 問いID | 主シナリオ | 紐づく B-1 Q問 | B-4 24問評価対象か |
|---|---|---|---|
| G-N01 | Techno | Q-N09 主体・人格 | YES |
| G-N02 | Techno | Q-N09 主体・人格 | YES |
| G-N03 | Techno | Q-N09 主体・人格 | YES |
| G-N04 | Care/場所性 | （B-1 Q-M07 場所性回帰）→ Q-M05 場所性経済化（B-4対象に含まれる近接問い） | YES（代替Q-M05） |
| G-N05 | Care/場所性 | （Q-M07）→ Q-M05 | YES（代替Q-M05） |
| G-N06 | Care/場所性 | （Q-M07）→ Q-M05 | YES（代替Q-M05） |
| G-N07 | Pluriverse | （Q-V07 pluriverse）→ B-4対象外、近接 Q-N10 非西洋認識論 | YES（代替Q-N10） |
| G-N08 | Pluriverse | （Q-M03）→ B-4対象外、近接 Q-N10 | YES（代替Q-N10） |
| G-N09 | Pluriverse | （Q-F04 先住民知識主権）→ B-4対象外、近接 Q-N10 | YES（代替Q-N10） |
| G-N10 | Care | Q-N04 場所根ざし相互依存 | YES |
| G-N11 | Care | （Q-M01 ケア経済）→ B-4対象外、近接 Q-N04 | YES（代替Q-N04） |
| G-N12 | Care/Edu | Q-N12 / Q-N13 / Q-M12（教育群） | YES（複数継承） |
| G-M01 | Care | （Q-M01 GDP代替）→ B-4対象外、代替なし | NO |
| G-M02 | Care | Q-N04 系 UBI | YES（近接継承） |
| G-M03 | Care | （Q-M01 マルチステークホルダー）→ B-4対象外 | NO |
| G-M04 | cross | （Q-F02 世代間正義）→ B-4対象外 | NO |
| G-M05 | cross | （Q-F02 未来世代代表）→ B-4対象外 | NO |
| G-M06 | Slow | （Q-V05 ゆっくりの権利）→ B-4対象外 | NO |
| G-M07 | Slow | （Q-M11 多元時間）→ B-4対象外 | NO |
| G-M08 | Fragmentation | （Q-F06 気候移民）→ 近接 Q-N06 | YES（代替Q-N06） |
| G-M09 | Fragmentation | （Q-F06）→ 近接 Q-N06 / Q-V06（10億規模強制移民） | YES（複数継承） |
| G-M10 | Pluriverse | （Q-M03 TK共同知）→ B-4対象外、近接 Q-N10 | YES（代替Q-N10） |
| G-F01 | Pluriverse | （Q-V07 cosmology併存）→ 近接 Q-F03 非西洋主流化 | YES（代替Q-F03） |
| G-F02 | Care | （Q-N12 三項並存経済）→ Q-N12 | YES |
| G-F03 | Slow | （Q-M11 多元時間浸透）→ B-4対象外 | NO |
| G-F04 | Fragmentation | cross-scenario → Q-V06 / Q-N06 | YES（複数継承） |
| G-F05 | Techno | （Q-N09 AI共進化）→ Q-N09 / Q-F08 AI×倫理 | YES（複数継承） |
| G-V01 | cross | cross-scenario → 評価困難、最近接 Q-V02 双子峰 / Q-V06 | YES（複数継承） |
| G-V02 | cross | （Q-V03 人間中心↔multispecies）→ B-4対象外、近接 Q-F08 | YES（代替Q-F08） |
| G-V03 | self-reflexive | self-reflexive → B-4対象外 | NO |

**集計**: 評価対象内 22問 / 対象外 8問

### 0.3 スコア継承の表記原則

- **継承**: B-3 問いのスコアは紐づく B-1 Q問の coverage_scores 実DB値から転記
- **複数継承**: 複数 Q問にマップされる場合は MAX を採用（最も強い装置応答を継承）
- **対象外**: B-4 24問にマップできない B-3 問いは「データなし(N/A)」として明示
- **方向性・主体**: B-4 では未付与のため、B-5 リードが追加判定（本データセットでは空欄）

---

## 1. B-3 30問 × B-4 7装置 動きスコアマトリクス（210セル）

### 凡例

- 数値: B-1 Q問の `MAX(score)` を継承（0-5、5装置で最強応答）
- N/A: B-4 24問評価対象外で実装値なし
- (Q-XXX) 注記: 継承元 Q問
- max列: 当問いの7装置中の最大スコア
- n≥3 列: score≥3 の装置数

### 群I (near 2026-2035) ─ 12問

| 問いID | 継承元 | SG | UPR | SGRD | Policy | IR | Funding | Sangaku | max | n≥3 |
|--------|--------|----|----|------|--------|----|----|---------|-----|-----|
| G-N01 | Q-N09 | 5 | 4 | 1 | 2 | 5 | 3 | 0 | 5 | 4 |
| G-N02 | Q-N09 | 5 | 4 | 1 | 2 | 5 | 3 | 0 | 5 | 4 |
| G-N03 | Q-N09 | 5 | 4 | 1 | 2 | 5 | 3 | 0 | 5 | 4 |
| G-N04 | Q-M05 | 3 | 1 | 1 | 2 | 3 | 3 | 0 | 3 | 3 |
| G-N05 | Q-M05 | 3 | 1 | 1 | 2 | 3 | 3 | 0 | 3 | 3 |
| G-N06 | Q-M05 | 3 | 1 | 1 | 2 | 3 | 3 | 0 | 3 | 3 |
| G-N07 | Q-N10 | 5 | 0 | 0 | 0 | 1 | 0 | 0 | 5 | 1 |
| G-N08 | Q-N10 | 5 | 0 | 0 | 0 | 1 | 0 | 0 | 5 | 1 |
| G-N09 | Q-N10 | 5 | 0 | 0 | 0 | 1 | 0 | 0 | 5 | 1 |
| G-N10 | Q-N04 | 5 | 5 | 1 | 3 | 4 | 4 | 1 | 5 | 5 |
| G-N11 | Q-N04 | 5 | 5 | 1 | 3 | 4 | 4 | 1 | 5 | 5 |
| G-N12 | MAX(Q-N12,Q-N13,Q-M12) | 5 | 5 | 1 | 3 | 5 | 4 | 4 | 5 | 6 |

### 群II (mid 2036-2055) ─ 10問

| 問いID | 継承元 | SG | UPR | SGRD | Policy | IR | Funding | Sangaku | max | n≥3 |
|--------|--------|----|----|------|--------|----|----|---------|-----|-----|
| G-M01 | (Q-M01) 対象外 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| G-M02 | Q-N04 | 5 | 5 | 1 | 3 | 4 | 4 | 1 | 5 | 5 |
| G-M03 | (Q-M01) 対象外 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| G-M04 | (Q-F02) 対象外 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| G-M05 | (Q-F02) 対象外 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| G-M06 | (Q-V05) 対象外 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| G-M07 | (Q-M11) 対象外 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| G-M08 | Q-N06 | 5 | 0 | 0 | 2 | 4 | 1 | 0 | 5 | 2 |
| G-M09 | MAX(Q-N06,Q-V06) | 5 | 0 | 0 | 2 | 4 | 2 | 0 | 5 | 2 |
| G-M10 | Q-N10 | 5 | 0 | 0 | 0 | 1 | 0 | 0 | 5 | 1 |

### 群III (far 2056-2080) ─ 5問

| 問いID | 継承元 | SG | UPR | SGRD | Policy | IR | Funding | Sangaku | max | n≥3 |
|--------|--------|----|----|------|--------|----|----|---------|-----|-----|
| G-F01 | Q-F03 | 4 | 0 | 0 | 0 | 1 | 0 | 0 | 4 | 1 |
| G-F02 | Q-N12 | 5 | 5 | 0 | 1 | 5 | 2 | 1 | 5 | 3 |
| G-F03 | (Q-M11) 対象外 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| G-F04 | MAX(Q-V06,Q-N06) | 5 | 0 | 0 | 2 | 4 | 2 | 0 | 5 | 2 |
| G-F05 | MAX(Q-N09,Q-F08) | 5 | 5 | 1 | 2 | 5 | 3 | 1 | 5 | 4 |

### 群IV (very-far 2081-2100) ─ 3問

| 問いID | 継承元 | SG | UPR | SGRD | Policy | IR | Funding | Sangaku | max | n≥3 |
|--------|--------|----|----|------|--------|----|----|---------|-----|-----|
| G-V01 | MAX(Q-V02,Q-V06) | 5 | 0 | 0 | 2 | 3 | 2 | 0 | 5 | 2 |
| G-V02 | Q-F08 | 5 | 5 | 0 | 2 | 3 | 1 | 1 | 5 | 3 |
| G-V03 | self-reflexive 対象外 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

### マトリクス全体集計

- 全210セル中、実DB値が入ったセル: **154セル**（22問×7装置）
- N/A セル: **56セル**（8問×7装置 = B-4 24問対象外）
- 実DB値セルの平均スコア: **2.40**（全210セル基準では 1.76）
- 実DB値セルのうち score≥3 セル: **74セル**（48.1%）

---

## 2. Hot/Warm/Cool/Dead zones 暫定弁別

### 2.1 判定基準（B-5 briefing 準拠）

| 区分 | 装置数（score≥3） | 解釈 |
|---|---|---|
| Hot | 5装置以上 | 実装可能性が現時点で高い |
| Warm | 3-4装置 | 一部主体のみが推進 |
| Cool | 1-2装置 | 動きはあるが薄い、萌芽 |
| Dead | 0装置 | 構造的空白、戦略的空白候補 |
| N/A | 評価対象外 | B-4 24問にマップなし、別系列で判定要 |

### 2.2 30問の zone 分布

| 区分 | 件数 | 該当問いID |
|---|---|---|
| **Hot** (n≥3 = 5以上) | **4問** | G-N10 / G-N11 / G-N12 / G-M02 |
| **Warm** (n≥3 = 3-4) | **9問** | G-N01 / G-N02 / G-N03 / G-N04 / G-N05 / G-N06 / G-F02 / G-F05 / G-V02 |
| **Cool** (n≥3 = 1-2) | **9問** | G-N07 / G-N08 / G-N09 / G-M08 / G-M09 / G-M10 / G-F01 / G-F04 / G-V01 |
| **Dead** (n≥3 = 0) | **0問** | （実DB値が入った22問では該当なし） |
| **N/A** (B-4 対象外) | **8問** | G-M01 / G-M03 / G-M04 / G-M05 / G-M06 / G-M07 / G-F03 / G-V03 |

集計: Hot 4 + Warm 9 + Cool 9 + Dead 0 + N/A 8 = **30問** ✓

### 2.3 ホライズン別 zone 分布（実DB値継承分のみ）

| ホライズン | Hot | Warm | Cool | N/A | 合計 |
|---|---|---|---|---|---|
| 群I (near) | 3 (G-N10,N11,N12) | 6 (G-N01〜N06) | 3 (G-N07,N08,N09) | 0 | 12 |
| 群II (mid) | 1 (G-M02) | 0 | 3 (G-M08,M09,M10) | 6 | 10 |
| 群III (far) | 0 | 2 (G-F02,F05) | 2 (G-F01,F04) | 1 | 5 |
| 群IV (very-far) | 0 | 1 (G-V02) | 1 (G-V01) | 1 | 3 |
| **合計** | **4** | **9** | **9** | **8** | **30** |

---

## 3. B-3 30問のうち B-4 24問評価対象 vs 対象外

### 3.1 対象内（実装値あり）: 22問

| ホライズン | 件数 | 問いID |
|---|---|---|
| near | 12 | G-N01 / G-N02 / G-N03 / G-N04 / G-N05 / G-N06 / G-N07 / G-N08 / G-N09 / G-N10 / G-N11 / G-N12 |
| mid | 4 | G-M02 / G-M08 / G-M09 / G-M10 |
| far | 4 | G-F01 / G-F02 / G-F04 / G-F05 |
| very-far | 2 | G-V01 / G-V02 |

### 3.2 対象外（推測のみ／B-2 補完待ち）: 8問

| ホライズン | 件数 | 問いID | 紐づく B-1 Q問 | 補完戦略 |
|---|---|---|---|---|
| mid | 6 | G-M01 / G-M03 | Q-M01 ケア経済 | B-2 Care wisdom 19件で補完 |
| mid |  | G-M04 / G-M05 | Q-F02 世代間正義 | B-2 cross-scenario wisdom 12件で補完 |
| mid |  | G-M06 | Q-V05 ゆっくりの権利 | B-2 Slow wisdom 12件で補完 |
| mid |  | G-M07 | Q-M11 多元的時間 | B-2 Slow wisdom 12件で補完 |
| far | 1 | G-F03 | Q-M11 多元的時間 | B-2 Slow wisdom 12件で補完 |
| very-far | 1 | G-V03 | self-reflexive | ミラツク後継組織問い、B-5/B-6 で別途処理 |

### 3.3 評価対象/対象外の構造的偏り

- **near 100% カバー**: 全12問が実装値あり
- **mid 40% カバー**: 4/10問のみ。**mid 60% (6問) が B-4 装置で観測不能**
- **far 80% カバー**: 4/5問
- **very-far 67% カバー**: 2/3問

**示唆**: 「mid 領域における規範問いの装置盲点」が構造的に存在。この6問（Q-M01/Q-F02/Q-V05/Q-M11 系列）はミラツクの「規範系・概念系」装置盲点と整合する（B-4 主要発見4 と一貫）。

---

## 4. 戦略的空白候補（dead zones / quasi-dead）

実DB値継承22問では厳密 Dead（n≥3=0）はゼロ。ただし以下を「準 Dead / 戦略的空白候補」として B-5 リード本判定に渡す:

### 4.1 装置応答最薄問い（n≥3=1問い）

実装値継承組のうち、装置応答が最も薄い問い:

| 問いID | 継承元 | n≥3 | max | シナリオ | critical juncture | B-3 重要度 |
|---|---|---|---|---|---|---|
| G-N07 | Q-N10 | 1 | 5 | Pluriverse | JCT-03 | 高（準Mサイン非西洋認識論接続） |
| G-N08 | Q-N10 | 1 | 5 | Pluriverse | JCT-03 | 高（準Mサイン非西洋認識論接続） |
| G-N09 | Q-N10 | 1 | 5 | Pluriverse | JCT-03 | 高（準Mサイン非西洋認識論接続） |
| G-M10 | Q-N10 | 1 | 5 | Pluriverse | JCT-06 | 中（学術界主体・TK共同知） |
| G-F01 | Q-F03 | 1 | 4 | Pluriverse | JCT-08前段 | 高（cosmology併存・全シナリオ完成形） |

→ **Pluriverse シナリオ系列の 5問が「装置応答最薄かつ critical juncture 接続厚」** の構造。これは B-4 主要発見4「規範系・概念系問いは装置応答最薄」と完全整合。**Pluriverse 系列はミラツクの戦略的空白の最有力候補**。

### 4.2 B-4 24問対象外で最重要な問い（潜在的 Dead）

8問の対象外問いのうち、critical juncture 接続性が高く B-3 シナリオ評価で wisdom 厚い問い:

| 問いID | シナリオ | wisdom件数 | critical juncture | B-3 重要度 |
|---|---|---|---|---|
| G-M01 | Care | 19件 | JCT-04 ケア経済制度化 | 最高 |
| G-M03 | Care | 19件 | JCT-04 | 高 |
| G-M04 | cross | 12件 | JCT-05 世代間正義憲法化 | 最高（Phase A 準Mサイン） |
| G-M05 | cross | 12件 | JCT-05 | 最高 |
| G-M06 | Slow | 12件 | JCT-07前段 | 中 |
| G-M07 | Slow | 12件 | JCT-07前段 | 中 |
| G-F03 | Slow | 12件 | JCT-07 | 中 |
| G-V03 | self-reflexive | - | 全JCT | 最高（自己言及） |

→ **G-M01/G-M03/G-M04/G-M05 の 4問が「critical juncture 接続最強かつ装置観測不能」の構造的空白の核**。これらは「動きはないが重要」の最有力候補。

### 4.3 戦略的空白の暫定数

| カテゴリ | 件数 | 問い |
|---|---|---|
| Pluriverse 装置応答最薄組 | 5 | G-N07 / G-N08 / G-N09 / G-M10 / G-F01 |
| Care 装置観測不能組（高重要） | 2 | G-M01 / G-M03 |
| 世代間正義 装置観測不能組（最高重要） | 2 | G-M04 / G-M05 |
| Slow Right 装置観測不能組 | 3 | G-M06 / G-M07 / G-F03 |
| 自己言及（最高重要） | 1 | G-V03 |
| **戦略的空白候補 合計** | **13問** | （30問の 43.3%） |

---

## 5. ミラツク優先領域 TOP10 暫定ランキング

二軸: **実装可能性** (n≥3 装置数) × **重要性** (B-3 シナリオ wisdom厚×JCT接続)

### 5.1 重要性スコアの暫定算出

- wisdom 厚: B-3 §2.2 シナリオ別件数（Pluriverse 18 / Techno 13 / Care 19 / Slow 12 / Frag 11 / cross 12）
- JCT 接続: 各 critical juncture との接続強度
- B-3 sentinel verdict MJ-02 の Mサイン領域接続厚みを加味

### 5.2 TOP10 暫定ランキング

| 順位 | 問いID | n≥3 | wisdom厚 | JCT | シナリオ | 二軸位置 |
|---|---|---|---|---|---|---|
| 1 | G-N12 | 6 | 19 (Care) | JCT-01/02/04 | Care | **右上**（即実装×最高重要） |
| 2 | G-N10 | 5 | 19 (Care) | JCT-04前段 | Care | **右上**（即実装×最高重要） |
| 3 | G-N11 | 5 | 19 (Care) | JCT-04前段 | Care | **右上**（即実装×最高重要） |
| 4 | G-M02 | 5 | 19 (Care) | JCT-04 | Care | **右上**（即実装×最高重要） |
| 5 | G-N01 | 4 | 13 (Techno) | JCT-01 | Techno | **右上**（即実装×中重要） |
| 6 | G-N02 | 4 | 13 (Techno) | JCT-01 | Techno | **右上**（即実装×中重要） |
| 7 | G-N03 | 4 | 13 (Techno) | JCT-01 | Techno | **右上**（即実装×中重要） |
| 8 | G-F05 | 4 | 13 (Techno延長) | JCT-01延長 | Techno | **中央**（中実装×far領域） |
| 9 | G-F02 | 3 | 19 (Care) | JCT-04後段 | Care | **中央**（中実装×Care厚） |
| 10 | G-V02 | 3 | 12 (cross) | JCT-08 | cross | **中央**（very-far 重要） |

注: 戦略的空白として **G-M01 / G-M04 / G-N07-09** は別建てで「左上（低実装性×高重要性）」象限に配置（次セクション参照）。

### 5.3 戦略的空白 TOP5（左上象限・中長期投資先）

| 順位 | 問いID | wisdom厚 | JCT | シナリオ | 投資理由 |
|---|---|---|---|---|---|
| 1 | G-M04 | 12 (cross) | JCT-05 | 世代間正義 | 準Mサイン直接接続、装置観測不能 |
| 2 | G-M01 | 19 (Care最厚) | JCT-04 | Care GDP代替 | Care wisdom最厚にもかかわらず装置観測不能 |
| 3 | G-N09 | 18 (Pluriverse) | JCT-03 | 先住民知識主権 | 準Mサイン接続、装置応答最薄 |
| 4 | G-V03 | self | 全JCT | ミラツク後継組織 | 自己言及・最高重要 |
| 5 | G-M07 | 12 (Slow) | JCT-07前段 | 多元時間 | 概念整合第四変容期接続、装置観測不能 |

### 5.4 二軸ランキング全体構造

| 象限 | 件数 | 主問い |
|---|---|---|
| **右上**（即実装×高重要） | 7 | G-N10/N11/N12/M02/N01/N02/N03 |
| **中央**（中実装×中重要） | 6 | G-N04/N05/N06/F05/F02/V02 |
| **左上**（低実装×高重要、戦略的空白） | 5 | G-M04/M01/N09/V03/M07 |
| **右下**（高実装×低重要、warning候補） | 0 | （該当なし、装置応答強の問いはすべて重要） |
| **左下**（低実装×低重要） | 4 | G-N07/N08/M10/F01 |
| **N/A 別建て要検討** | 8 | mid 6 + far 1 + very-far 1 |

---

## 6. B-5 リードへの引継ぎサマリー

### 6.1 即時利用可能な確定値

- 210セルマトリクス（実DB値継承 154セル + N/A 56セル）
- zone 暫定弁別: Hot 4 / Warm 9 / Cool 9 / Dead 0 / N/A 8
- 戦略的空白候補: 13問（うち critical 5問）
- ミラツク優先領域 TOP10 暫定（右上7 + 中央3）

### 6.2 B-5 リードが本判定すべき項目

1. **方向性付与** (P/R/B): 本データセットでは未付与。装置別に B-3 シナリオの善い社会像と比較して P/R/B 判定
2. **主体付与** (G/C/Civ/A): B-3 §4.2 主体配分から各セルに主体記号付与
3. **N/A 8問の補完判定**: B-2 wisdom 件数を装置スコア相当値に変換するか別軸で扱うかを決定
4. **ミラツク優先領域 TOP10 確定**: 右上7問 + 戦略的空白5問 + その他から選定
5. **動きの方向違い (warning) 検出**: 本データセットでは方向性未付与のため未検出
6. **複合主体問い 16問の按分判定**: テンプレート §7-5 留意事項参照

### 6.3 主要発見の暫定 (B-5 lead が確定)

1. **Care シナリオが「即実装最強」**: 上位 4位までが Care 系列（G-N10/N11/N12/M02）で n≥3=5-6
2. **Pluriverse シナリオが「装置応答最薄」**: 5問（G-N07-09/M10/F01）が n≥3=1 集中。準Mサイン非西洋認識論との接続厚いにもかかわらず観測装置で薄い構造
3. **mid 領域に装置盲点 60%**: 10問中 6問が B-4 装置で評価不能。Care/世代間正義/Slow Right の規範問いが該当
4. **near 12問は全カバー**: B-4 装置の near 偏重設計と一貫し、near 規範問いはすべて装置観測可能
5. **very-far 2/3 問が観測可能**: 群IV は規模小さいが G-V01/G-V02 は観測値継承可

### 6.4 Sentinel 申し送り遵守事項

- 5補完類型に依存しない設計を採用済み（独自に MAX(score) GROUP BY question_id で弁別）
- B-4 軽微追補 agent (a8a27149da6396690) の作業領域 (analysis/report/verification/handoff) は不可侵
- coverage_scores テーブル直接参照のみ実施、装置メタ情報・5類型分類は未利用

---

## 7. データソース・再現性

### 7.1 SQL 再現コマンド

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

### 7.2 マッピング根拠ファイル

- B-3 30問体系: `track-b3_handoff.md` §4.1
- B-3 → B-1 推定マッピング: `_TRACK_B5_INPUT_TEMPLATE.md` §1 + §4.1
- B-1 → B-4 24問選定: `track-b4_handoff.md` §2
- B-4 sentinel 設計指示: `track-b4-sentinel-verdict.md` §9

### 7.3 既知の限界

1. **B-3 → B-1 マッピングは【推定】** — テンプレート §1 由来。B-4 軽微追補完了後の正式 connection_id で再確認要
2. **複数 Q問への継承は MAX 採用** — 平均/合算/最弱など別集計も可能。B-5 リードの方法論判断に従う
3. **N/A 8問の扱いは未確定** — B-2 wisdom 件数を「補完装置スコア」に変換する方法は B-5 が独自設計
4. **方向性 P/R/B は未付与** — 本データセットは「動きの強さ」のみ。「動きの向き」は B-5 が個別判定

---

最終更新: 2026-05-09
作成: Track B-5 起動準備（B-4 軽微追補と並列作業、作業領域不可侵）
データ根拠: `~/projects/research/initiatives-db/initiatives.db` coverage_scores テーブル直接抽出（24問×7装置 = 168セル実値）
継承根拠: `_TRACK_B5_INPUT_TEMPLATE.md` §1 + §4.1 推定マッピング
設計指針: B-4 sentinel verdict §9 — 5補完類型非依存、MAX(score) GROUP BY question_id 独自弁別
