# Phase B 用語集・略号定義

監査日: 2026-05-09
監査対象: track-b1〜b4 の handoff.md + analysis/verification/report.html（13文書）+ _PHASE_A_INHERITANCE_AUDIT.md
目的: Phase B-6 統合HTML化の用語統一参照
方法: grep ベースで出現頻度集計 → 多数派採用 + 文書間整合性 + 公式定義チェック

---

## 1. 公式用語（B-6 統合HTML化で採用）

### 1.1 Mサイン階層（Mサイン由来分類）

| 公式用語 | 略号 | 定義 | 採用理由 |
|---------|------|------|---------|
| **真Mサイン由来** | 真M由来 | Phase A で「真Mサイン」認定された領域から派生した問い。物語転換期（2018-2026）が唯一の真M認定領域 | B-1 ground truth、B-1 §5 表で「真M由来」を採用、出現頻度 29 vs 「真Mサイン由来」2 で多数派 |
| **準Mサイン由来** | 準M由来 | Phase A で「準Mサイン」認定された3領域（世代間正義／非西洋認識論／AI革命の制度反作用）から派生 | B-1/B-2/B-3/B-4 すべて「準M由来」表記、出現頻度 38 |
| **概念整合由来** | 概念整合 | Phase A 「概念整合」認定領域（第四変容期）から派生した問い。定量根拠は概念的合意に留まる | B-1/B-3 で「概念整合由来」（43）「概念整合」（47）併用 |
| **単独T由来** | 単独T | 単独 Track 派生で Mサイン認定領域には属さない問い（例: Q-N12 は Phase A Track 1 の独自知見由来） | B-1/B-2/B-3 で統一、出現頻度 35 |

注: 「真Mサイン」自体は装置（Phase A の認定種別）を指す。「真M由来」「準M由来」は問いの派生分類。文脈で使い分け。

### 1.2 装置（変化検出装置 / DB）

| 公式用語 | 略号 | 定義 | 採用理由 |
|---------|------|------|---------|
| **Signal DB** | SG | pestle-signal-db。7,668 signals + 5次元評価 + PESTLE × CLA depth | B-4 §2 装置定義。略号 SG が最多（75）、フル名 Signal DB（18） |
| **University Press Releases** | UPR | 大学プレスリリース。41,760件 | B-4 で UPR 表記が圧倒的（102）。日本語「大学PR」5回・「大学プレス」7回は補助 |
| **Sangaku R&D Press Releases** | SGRD | 企業 R&D PR。36,734件 | B-4 §2 装置定義。SGRD（58）が標準、「企業R&D」3 |
| **Policy DB** | Policy | 政策事業 DB。30,118事業（FY2021-2025） | B-4 で Policy（55）が標準 |
| **IR Collector** | IR | 上場企業有価証券報告書。1,769,821 セクション / 72,502 documents | フル名「IR Collector」（11）、略号 IR が最多（42+）、まれに「IR DB」（2） |
| **Investment Funding** | Funding | 投資シグナル。16,642 PR / 2,001 ラウンド / 4,264 組織 | B-4 で Funding（39）が標準。日本語「投資シグナル」9・「資金調達」9 は補助 |
| **Sangaku Matcher** | Sangaku | 産学連携マッチング。492K レコード / 33 ambition / 40 tech taxonomy | B-4 で Sangaku（41）が標準。「sangaku-matcher」（6）は内部識別子 |

### 1.3 Track識別

| 公式用語 | 略号 | 定義 | 採用理由 |
|---------|------|------|---------|
| **Track B-1** | B-1 | 多層人類史×4ホライズン予測 × 問い群構築（基盤層） | フル名「Track B-1」（107）と略号「B-1」（103）併用、文脈で使い分け |
| **Track B-2** | B-2 | すでにある未来 — 14問×5traditionsの歴史的回答パターン抽出 | 同上 |
| **Track B-3** | B-3 | 善い社会の可能性 × 経路 × 問い（規範層） | 同上 |
| **Track B-4** | B-4 | 変化検出装置の予測的応答評価 + 取り組みDB（実装層） | 同上 |
| **Track B-5** | B-5 | 動きの状況測定（hot/dead zones 弁別） | 後続 Wave |
| **Track B-6** | B-6 | Phase B 統合 HTML 化 | 後続 Wave |

注: ファイル名に使うときは小文字 `track-b1` を採用（19件、内部識別子）。文中表記は「Track B-1」または「B-1」。

### 1.4 シナリオ名（B-3）

| 公式用語 | 略号/別名 | 定義 | 採用理由 |
|---------|---------|------|---------|
| **Pluriverse シナリオ** | Pluriverse | 多元的世界の制度化（中核 wisdom 18件） | B-3 §2.1 公式名。出現頻度 Pluriverse 71 / pluriverse 81（小文字は概念用語、大文字はシナリオ名） |
| **Techno-Acceleration シナリオ** | Techno-Acceleration | テクノ加速の極（中核 wisdom 13件） | B-3 §2.1 公式名（32）。日本語「テクノ加速」（22）は説明補助 |
| **Care-Creative-Co-existence シナリオ** | Care-Creative-Co-existence | ケア・創造・共生の経済原理化（中核 wisdom 19件） | B-3 §2.1 公式名（24）。短縮形「Care-Co-existence」（5）は揺れ |
| **Slow Right シナリオ** | Slow Right | 〈ゆっくりの権利〉の制度化（中核 wisdom 12件） | B-3 §2.1 公式名（42）。日本語「ゆっくりの権利」（31）は概念説明 |
| **Fragmentation シナリオ** | Fragmentation | 地政学的・認識論的分断（中核 wisdom 11件） | B-3 §2.1 公式名（59）。日本語訳は使用なし |

### 1.5 共通スパン（4ホライズン）

| 公式用語 | 略号 | 期間定義 | 採用理由 |
|---------|------|---------|---------|
| **near** | N | 2026-2035 | B-1 §2.2 確定（188回出現）、全Track で同一定義 |
| **mid** | M | 2036-2055 | 同上（172回） |
| **far** | F | 2056-2080 | 同上（144回） |
| **very-far** | V | 2081-2100 | 同上（176回）。表記は「very-far」（ハイフン付き）固定 |

注: 全文書で同一定義であることを確認済（_PHASE_B_PLAN.md / B-1 §2.2 / B-3 §4.1 / B-4 §2 すべて一致）。問いID 接頭辞 N/M/F/V もこの 4 区分と対応。

### 1.6 5 traditions（B-2 補完装置）

| 公式用語 | 略号 | 定義 | 採用理由 |
|---------|------|------|---------|
| **5 traditions** または **5系統** | — | PHIL / LIT / MY / TK / AN の5系統学術DB | 出現頻度: 5系統 128 / 5 traditions 27 / 5traditions 9。日本語文脈は「5系統」、英語的文脈は「5 traditions」を推奨。意味は同一 |
| PHIL | PHIL | 哲学概念DB（10,292概念）★DB実値 | B-1/B-2 統一 |
| LIT | LIT | 文学概念DB（11,115概念） | B-1/B-2 統一 |
| MY | MY | 神話ナラティブDB（11,936物語）★DB実値 | B-1/B-2 統一（B-2 文書内の 10,615 は旧ブリーフィング値、置換要） |
| TK | TK | 伝統知DB（3,002グループ / 36,360項目）★DB実値 | B-1/B-2 統一（B-2 文書内の 3,001 は旧値、置換要） |
| AN | AN | 人類学概念DB（500概念） | B-1/B-2 統一 |

---

## 2. 表記揺れ検出表

| # | 揺れた表現 | 出現Track/箇所 | 推奨統一形 | 重大度 |
|---|-----------|---------------|-----------|--------|
| 1 | 「真M由来」(29) / 「真Mサイン由来」(2) | B-1/B-2/B-3/B-4 横断 | **真M由来**（多数派、handoff §5 表で採用） | 軽 |
| 2 | 「概念整合」(47) / 「概念整合由来」(43) | B-1 §5 / B-3 §3 | **概念整合由来**（明示的、§5 表記基準）。概念的議論を指す場合のみ「概念整合」 | 中 |
| 3 | 「単独T」(12) / 「単独T由来」(35) | B-1 §5 横断 | **単独T由来**（明示形、多数派） | 軽 |
| 4 | 「Care-Creative-Co-existence」(24) / 「Care-Co-existence」(5) | B-3 内部 | **Care-Creative-Co-existence**（フル名固定、シナリオ名識別性のため） | 中 |
| 5 | 「Pluriverse」(71・シナリオ名) / 「pluriverse」(81・概念) | B-1〜B-4 | **シナリオ名は Pluriverse、概念は pluriverse**（大小文字で意味分離） | 軽 |
| 6 | 「IR」(42) / 「IR Collector」(11) / 「IR DB」(2) | B-4 横断 | **本文初出は IR Collector、以降 IR**（B-4 §2 の装置定義に倣う） | 軽 |
| 7 | 「Sangaku」(41) / 「sangaku-matcher」(6) / 「産学」(14) | B-4 内部 | **本文は Sangaku、識別子のみ sangaku-matcher** | 軽 |
| 8 | 「Funding」(39) / 「投資シグナル」(9) / 「資金調達」(9) | B-4 内部 | **本文は Funding、説明文で「投資シグナル」併記可** | 軽 |
| 9 | 「Policy」(55) / 「policy」(4) / 「政策DB」 | B-4 横断 | **Policy**（B-4 §2 標準、固有名詞として大文字始め） | 軽 |
| 10 | 「85 wisdom records」(9) / 「85件」(28) / 「85件 wisdom」(4) | B-2/B-3 | **85件 wisdom records**（明示形、英日併記） | 軽 |
| 11 | 「Track B-1」(107) / 「B-1」(103) / 「track-b1」(19) | 全文書 | **本文初出は Track B-1、以降 B-1。ファイル名は track-b1** | 軽 |
| 12 | 「多層人類史」(12) / 「多層構造化」(6) | B-1 内部 | **多層人類史×4ホライズン予測**（B-1 タイトル準拠）。手法を指すときは「多層構造化」 | 軽 |
| 13 | 「critical juncture」(60) / 「分岐点」(36) | B-3 横断 | **本文初出は critical juncture（分岐点）、以降 critical juncture** | 軽 |
| 14 | 「168 セル」(27) / 「168セル」(2) | B-4 / B-3 | **168 セル**（半角数字＋全角空白＋セル） | 軽 |
| 15 | 「coverage_score」(20) / 「coverage score」/ 「カバレッジスコア」(2) | B-4 横断 | **coverage_score**（DB列名・技術用語）／**カバレッジスコア**（説明文） | 軽 |
| 16 | 「wisdom records」(27) / 「wisdom_records」(21) | B-2/B-3 | **wisdom_records**（DB列名）／**wisdom records**（本文） | 軽 |
| 17 | 「initiatives.db」(17) / 「initiatives-db」(8) / 「initiatives_db」(5) | B-4 横断 | **initiatives.db**（ファイル名）／**initiatives-db**（ディレクトリ名）。混同しないこと | 中 |
| 18 | 「already_future.db」(24) / 「already-future-db」(4) | B-2 横断 | **already_future.db**（ファイル名）／**already-future-db**（ディレクトリ名） | 軽 |
| 19 | 「5系統」(128) / 「5 traditions」(27) / 「5traditions」(9) | B-1/B-2/B-3 | **日本語文脈は5系統、英文脈は 5 traditions**（5traditions のスペース無し形は非推奨） | 軽 |
| 20 | Q-V05 の Mサイン階層: B-1 ground truth=「概念整合由来」、B-2 analysis 旧表記=「単独T由来」 | B-1 vs B-2 | **B-1 ground truth = 概念整合由来**（B-2 sentinel verdict M1 で修正済） | **重要**（B-6 引用時は B-1 を最終 source-of-truth とする） |
| 21 | Q-N12 の Mサイン階層: B-1 ground truth=「単独T由来」、B-2 analysis 旧表記=「概念整合由来」 | B-1 vs B-2 | **B-1 ground truth = 単独T由来**（B-2 sentinel verdict M1 で修正済） | **重要** |

---

## 3. 数値定義（最終 source-of-truth）

### 3.1 問い群総数

| 数値 | 定義 | 最終 source-of-truth | Track別引用箇所 |
|------|------|---------------------|----------------|
| **41問** | B-1 全問い数（near 13 / mid 13 / far 8 / very-far 7） | B-1 §3 / handoff §5 集計表 | b1-handoff §3 / b1-report 第4部 / b2-handoff §10 / b3-handoff §5 / b4-handoff §6 |
| **14問** | B-2 対象（B-1 §6.1 指定14問の完全継承） | B-1 §6.1 + B-2 §3.2 | b1-handoff §6.1 / b2-handoff §3.2 / b3-handoff §5.2 |
| **30問** | B-3 善い社会問い群（near 12 + mid 10 + far 5 + very-far 3） | B-3 §4.1 | b3-handoff §4 / b3-report 第6部 |
| **24問** | B-4 装置評価対象（B-1 §6.2 指定） | B-1 §6.2 + B-4 §2 | b1-handoff §6.2 / b4-handoff §2 |
| **71問** | Phase B 全問い総数（B-1 41 + B-3 30） | B-3 handoff §10 | b3-handoff §10 |

### 3.2 Mサイン階層数値（B-1 全41問の分布）★最終確定値

| 階層 | 件数 | 割合 | 最終 source-of-truth |
|------|------|------|---------------------|
| 真M由来 | 4 | 9.8% | b1-handoff §5 集計表 + b1-report 第5部 |
| 準M由来 | 14 | 34.1% | 同上 |
| 概念整合由来 | 15 | 36.6% | 同上 |
| 単独T由来 | 8 | 19.5% | 同上 |
| **合計** | **41** | **100%** | — |

注: B-1 当初版で「真M3 / 準M4」等の不整合（修正前）があったが、修正後は上記が最終確定値。B-6 引用時は **必ず** 上記を採用すること。

### 3.3 B-2 対象14問の Mサイン階層分布（B-1 から再集計）

| 階層 | 件数 | 該当問い |
|------|------|---------|
| 真M由来 | 1 | Q-N04 |
| 準M由来 | 2 | Q-F02 / Q-M03 |
| 概念整合由来 | 8 | Q-V05 / Q-N09 / Q-M01 / Q-M07 / Q-M11 / Q-V03 / Q-V07 / Q-F04 |
| 単独T由来 | 3 | Q-N12 / Q-F06 / Q-V01 |
| **合計** | **14** | — |

source: b2-handoff §5.1 マッピング表（B-1 ground truth と完全同期）

### 3.4 B-3 critical juncture × Phase A Mサイン領域接続

| 接続基準 | 件数/合計 | 割合 | 該当 JCT |
|---------|----------|------|---------|
| 厳密接続（真M+準M） | **4/8** | **50%** | JCT-01・JCT-02（真M）／JCT-03・JCT-05（準M） |
| 概念整合含む | **6/8** | **75%** | 上記 4 + JCT-04・JCT-07（概念整合） |

注: B-3 sentinel verdict MJ-02 統一基準により、**主表記は 4/8 = 50%（厳密）**、**補完表記は 6/8 = 75%（概念整合含む）** とする。当初一部文書に「5/8」表記があったが、最終的に上記2基準に集約された。

### 3.5 B-2 wisdom_records 統計

| 項目 | 値 | 最終 source-of-truth |
|------|------|---------------------|
| wisdom_records 総数 | **85件** | b2-handoff §3.2 / already_future.db |
| カバレッジ | 70/70 セル（100%） | b2-handoff §2.2 |
| 系統別: PHIL | 24件（28.2%） | b2-handoff §3.2 |
| 系統別: AN | 17件（20.0%） | 同上 |
| 系統別: MY | 15件（17.6%） | 同上 |
| 系統別: TK | 15件（17.6%） | 同上 |
| 系統別: LIT | 14件（16.5%） | 同上 |

### 3.6 B-4 coverage_scores 統計

| 項目 | 値 | 最終 source-of-truth |
|------|------|---------------------|
| coverage_scores 総数 | **168 セル**（24問 × 7装置） | b4-handoff §2 / initiatives.db |
| 平均スコア | 2.18 | b4-handoff §3 |
| score≥3 | 73/168（43.5%） | 同上 |
| score≤1 | 76/168（45.2%） | 同上 |
| Initiatives レコード総数 | **463件** | b4-handoff §3 |
| 装置別最高: SG | 平均 4.00 / score≥3 が 22/24 | 同上 |
| 装置別最低: SGRD | 平均 0.50 | 同上（集計 JSON 制約による過小評価） |

### 3.7 B-3 5シナリオ wisdom 配分

| シナリオ | wisdom件数 | 該当問い |
|---------|-----------|---------|
| Care-Creative-Co-existence | 19 | Q-M01 + Q-N12 + Q-N04 |
| Pluriverse | 18 | Q-M03 + Q-V07 + Q-F04 |
| Techno-Acceleration | 13 | Q-N09 + Q-M07 |
| Slow Right | 12 | Q-V05 + Q-M11 |
| Fragmentation | 11 | Q-F06 + Q-V01 |
| cross-scenario共通基層 | 12 | Q-F02 + Q-V03 |
| **合計** | **85** | — |

source: b3-handoff §2.2

### 3.8 装置DB 規模（B-4 装置定義）

| 装置 | 規模 |
|------|------|
| SG | 7,668 signals |
| UPR | 41,760 件 |
| SGRD | 36,734 件 |
| Policy | 30,118 事業 |
| IR | 1,769,821 セクション / 72,502 documents |
| Funding | 16,642 PR / 2,001 ラウンド / 4,264 組織 |
| Sangaku | 492K レコード / 33 ambition / 40 tech taxonomy |

source: b4-handoff §2

### 3.9 Phase A 継承数値（_PHASE_A_INHERITANCE_AUDIT.md 確定 source-of-truth）

WARN-1（B-2 文書での旧ブリーフィング値残存）の影響を受ける数値は **B-1 採用の DB 実値** を最終値とする：

| 項目 | DB実値 | B-2 内残存値（採用しない） |
|------|--------|--------------------------|
| PHIL 概念総数 | **10,292** | 9,583（旧） |
| MY 物語総数 | **11,936** | 10,615（旧） |
| TK グループ | **3,002** | 3,001（旧） |

その他主要数値（FK 105件 / CLA 91,550 / SG disruption 7.49 / ET 12,958 等）は B-1 で正確継承され、PASS 判定済。詳細は _PHASE_A_INHERITANCE_AUDIT.md §「最終 source-of-truth テーブル」参照。

---

## 4. 用語使用時の注意

### 4.1 大小文字の使い分け（pluriverse / Pluriverse）

- **シナリオ名（B-3 5シナリオの1つ）として参照する場合 → `Pluriverse シナリオ`**（大文字始め）
- **概念（多元的世界、pluriverse cosmology 等）として参照する場合 → `pluriverse`**（小文字、固有概念用語）
- 例: 「Pluriverse シナリオは pluriverse 的 cosmology を制度化する経路を描く」

### 4.2 Track名の文中表記（B-1 vs Track B-1）

- **本文初出**: 「Track B-1（多層人類史×4ホライズン予測 × 問い群構築）」とフル名 + サブタイトルで導入
- **以降**: 「B-1」と短縮可
- **ファイル名・URL**: 小文字 `track-b1` / `track-b2` 等
- **連結ID**: 「Track B-1 → Track B-2」のようにフル名推奨（マトリクス・図表）

### 4.3 「問い」の使い分け

| 表記 | 用途 |
|------|------|
| 問い | 日本語本文での標準表記（B-1〜B-4 すべて「問い」を採用、出現多数） |
| Question | 英語翻訳が必要な場合のみ（Phase B 内部では原則使わない） |
| Q-N04 / Q-M01 / Q-F02 / Q-V01 等 | 問いID。N=near / M=mid / F=far / V=very-far + 連番 |
| G-N01 / G-M01 / G-F01 / G-V01 等 | B-3 善い社会問い ID（接頭辞 G=Good Society） |

### 4.4 Mサイン階層 ground truth の遵守

- **最終 source-of-truth は `track-b1-layered-history-report.html` 第5部**
- B-2 DB 内の `msign_origin` 列も B-1 と同期済（B-2 sentinel verdict M1 で修正完了）
- 個別問い（特に Q-V05 / Q-N12）の Mサイン階層を引用する場合、必ず B-1 ground truth を最終確認すること
- 集計値（真M4 / 準M14 / 概念整合15 / 単独T8 = 41）の引用は影響なし

### 4.5 critical juncture の接続率表記

- **主表記**: 「4/8 = 50%（厳密 真M+準M）」
- **補完表記**: 「6/8 = 75%（概念整合含む）」
- 単独表記の場合は **必ず両基準を併記** すること（B-3 sentinel verdict MJ-02 統一基準）

### 4.6 装置略号の優先順位

- **本文初出**: フル名（例: 「Signal DB（SG）」「IR Collector（IR）」）
- **以降**: 略号のみ（例: 「SG」「IR」）
- **マトリクス・表**: 略号のみ統一（SG / UPR / SGRD / Policy / IR / Funding / Sangaku）
- **DB識別子**: 内部参照のみ（pestle-signal-db / sangaku-matcher 等）

### 4.7 5類型（B-4 補完関係分類）の正式名

B-4 sentinel verdict Round 2 案B' で確定した最新の5類型名（旧第5類型「人感応型」等は廃止）:

1. **全装置応答型**（5装置以上 score≥3）— 6問
2. **制度+市場応答型**（Policy + IR + Funding 2装置以上 score≥3）— 4問
3. **研究応答型**（SG + UPR + SGRD のうち 2装置以上 score≥3）— 4問
4. **SG単独応答型** — 8問
5. **UPR単独強応答型**（UPR 単独 score≥3、他装置 score≤2 を許容）— 2問

注: B-4 旧版・旧文書では別の第5類型が記載されている可能性あり。**必ず B-4 sentinel verdict Round 2 採用版を最終とする**。

### 4.8 already_future.db / initiatives.db の混同回避

- **already_future.db**（B-2 構築）: questions / traditions / wisdom_records / cross_question_links の 4テーブル / 126レコード
- **initiatives.db**（B-4 構築）: questions / detection_systems / coverage_scores / initiatives の 4テーブル / 約 462+ レコード
- 両DBは **全く別のスキーマ・別の用途**。B-6 統合HTML化では両方を Phase B 全体DBとして登録する

### 4.9 Type-A/B/C 三類型（B-2）の遵守

B-2 で確定した三類型分類は B-3/B-4/B-5 が継承する：

- **Type-A 既出回答型**（9問）— 「再発見・再活性化」経路
- **Type-B 並走認識型**（4問）— 「実装ギャップ分析」経路
- **Type-C 新規問い型**（1問）— 「歴史的類比による外挿」経路

### 4.10 三大クラスター（B-2）の遵守

B-2 で確定した三大クラスター（B-3 経路設計の縦糸）：

- **多元的人格群**（4問）: Q-N09 / Q-M07 / Q-M11 / Q-M01
- **pluriverse群**（4問）: Q-M03 / Q-V07 / Q-F04 / Q-F06
- **長期時間群**（4問）: Q-F02 / Q-V03 / Q-V05 / Q-N04
- 独立2問: Q-N12（補完装置問い）/ Q-V01（新規問い）

---

## 5. B-6 統合HTML化での運用ガイドライン

1. **本文初出の用語は必ずフル名 + 略号** で導入する（例: 「Signal DB（SG、7,668 signals）」）
2. **数値引用は §3 の最終 source-of-truth を必ず参照**。Phase A 旧ブリーフィング値（PHIL 9,583 / MY 10,615 / TK 3,001）は **採用しない**
3. **Mサイン階層を引用するときは B-1 §5 集計表を最終 source-of-truth** とする
4. **critical juncture 接続率は両基準併記**（4/8 = 50% 厳密 / 6/8 = 75% 概念整合含む）
5. **シナリオ名は §1.4 のフル名表記**を採用（Care-Creative-Co-existence / Pluriverse / Techno-Acceleration / Slow Right / Fragmentation）
6. **問いID** は接頭辞統一（B-1 系: Q-N/M/F/V、B-3 系: G-N/M/F/V）
7. **DB識別子・ファイル名は §4.8 を遵守** — initiatives.db / already_future.db の混同を避ける

---

## 6. 監査の制約

- 本監査は grep ベースの機械検証で、文脈的妥当性は完全にはカバーしていない
- B-5 / B-6 はまだ未着手のため対象外
- _PHASE_A_INHERITANCE_AUDIT.md WARN-1（B-2 旧ブリーフィング値残存）は本監査でも継承
- B-4 sentinel verdict Round 2 採用後の最新表記が一部文書（旧版）と齟齬する可能性あり。**最新版を優先**

---

監査者: Phase B 用語統一エージェント
作成日: 2026-05-09
完了報告先: B-6 統合HTML化リード
参照: track-b{1,2,3,4}_handoff.md / track-b{1,2,3,4}-{analysis,verification,report}.html / _PHASE_A_INHERITANCE_AUDIT.md
