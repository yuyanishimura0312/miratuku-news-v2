# Phase A → Phase B 数値継承監査

監査日時: 2026-05-09
監査対象: Phase B Track B-1 / B-2 / B-3 の HTML + handoff（13文書）
監査基準: Phase A 9 Track の handoff / doc-verify-report / sentinel-verdict から抽出した ground truth 数値
方法: grep による機械的引用箇所抽出 → Phase A 値との突合 → 差分の重大度判定

---

## 判定: WARN

- FAIL（重大矛盾）: 0件
- WARN（要修正・要追跡）: 2件
- PASS（完全継承）: 8件（主要数値）

WARN は B-2 analysis.html と report.html での Track 9 系 DB 数値のブリーフィング値継承（B-1 はDB実値を継承しており、Phase B 内 Track 間で不整合）。Wave 4 統合段階で B-2 側の数値置換が必要。B-3 は Phase A 主要数値を直接引用しないため対象外。

---

## 数値別検証表

### 1. Track 1 (FK) 系数値

| Phase A 値（ground truth） | Phase A source | Phase B 引用箇所 | 引用値 | 一致/差分 | 判定 |
|---|---|---|---|---|---|
| values 105件 / vesteg_category | track1-doc-verify L-07 / sentinel | b1-analysis L638, b1-report L601/L789-792, b2-analysis L183 | values 0.45%空白（105件） | 完全一致 | PASS |
| trends 650件 | track1-sentinel | （Phase B 直接引用なし） | — | — | N/A |
| FK 0.45% values 空白 = 105 / 23,274 | track1-doc-verify | b1-analysis L638, b1-report L601/L789-792, b2-analysis L183 | 0.45% / 105件 | 完全一致 | PASS |
| Track 7 CTL-V 7,962概念 | track7-doc-verify L60 / handoff §11 | b1-analysis L638, b1-report L601/L792, b2-analysis L183 | CTL-V 7,962概念 | 完全一致 | PASS |

備考: ミッション仕様の「FK 105レポート」は単位の取り違え。Phase A 実値は「values 105件」（reports 総数は 76,548件）。Phase B 文書では正しく「values 105件」として引用されている。

### 2. Track 2 (CLA) 系数値

| Phase A 値 | Phase A source | Phase B 引用箇所 | 引用値 | 一致/差分 | 判定 |
|---|---|---|---|---|---|
| CLA 91,550行 / 19テーブル / 127年 | track2_handoff §1 / doc-verify L-01 | b1-analysis L549 | 91,550行・Thompson Motif 45,496件 | 完全一致 | PASS |
| Thompson Motif 45,496件 | track2-doc-verify | b1-analysis L549 | 45,496件 | 完全一致 | PASS |
| myth/worldview 2,858 keyword | track2_handoff §9 | b1-analysis L620 | 2,858 keyword | 完全一致 | PASS |
| 5系統失効＋5系統萌芽 | track2_handoff §9 | b1-analysis L543/L620, b1-report L583/L523 | 5系統失効＋5系統萌芽 | 完全一致 | PASS |

備考: Track 2 主軸DBは Phase B 全体で一貫して DB 実値で引用されており、改変なし。

### 3. Track 5 (SG) 系数値

| Phase A 値 | Phase A source | Phase B 引用箇所 | 引用値 | 一致/差分 | 判定 |
|---|---|---|---|---|---|
| disruption 7.49（126年最高） | track5_handoff §9 集計L-09 | b1-analysis L543/L620/L1121, b1-report L583 | 7.49（126年最高） | 完全一致 | PASS |
| paradigm_shift 20.4%（過去比+6.0pt） | track5_handoff §9 集計L-11 | b1-analysis L543/L620/L1123, b1-report L583 | 20.4% / +6.0pt | 完全一致 | PASS |
| myth層 11.1%（U字回復） | track5_handoff §9 集計L-12 | b1-analysis L543/L620/L1125, b1-report L583 | 11.1% / U字回復 | 完全一致 | PASS |
| past 14.4% → recent 17.1% → current 20.4% | track5_handoff L-11 | b1-analysis L1123 | 完全継承 | 完全一致 | PASS |
| past 10.9% → recent 6.9% → current 11.1% | track5_handoff L-12 | b1-analysis L1125 | 完全継承 | 完全一致 | PASS |

備考: Track 5「物語転換期の三重定量証拠」は B-1 で 4箇所以上に引用され、すべてDB実値と一致。

### 4. Track 6 (era_talents) 系数値

| Phase A 値 | Phase A source | Phase B 引用箇所 | 引用値 | 一致/差分 | 判定 |
|---|---|---|---|---|---|
| ET 12,958人物 | track6_handoff / sentinel | b1-analysis L521 | 12,958人物 | 完全一致 | PASS |
| GF 9,178人物 | track6_handoff / sentinel | b1-analysis L521 | 9,178人物 | 完全一致 | PASS |
| JPMS v2 832校 | track6-sentinel | b1-analysis L521 | 832校 | 完全一致 | PASS |
| PST 600偉人 | track6_handoff | b1-analysis L521 | 600偉人 | 完全一致 | PASS |

備考: Track 6 主軸DB群は B-1 で正確に継承。B-2/B-3 は Track 6 を直接引用しないため対象外。

### 5. Track 7 (Academic) 系数値

| Phase A 値 | Phase A source | Phase B 引用箇所 | 引用値 | 一致/差分 | 判定 |
|---|---|---|---|---|---|
| 5領域17,547概念（執筆時点） | track7-doc-verify L60 | b1-analysis L521 | 17,547概念・5領域 | 完全一致 | PASS |
| CTL-V 7,962概念（45.4%） | track7_handoff §3, §6 | b1-analysis L638, b1-report L601/L792, b2-analysis L183 | CTL-V 7,962概念 | 完全一致 | PASS |
| 約45,000規範的論述群（4DB合算32K + Track 7 CTL-V 7,962） | track9_handoff §3 / track9-doc-verify §3.3 | b1-report L601/L792, b2-analysis L183 | 約45,000規範的論述群 | 完全一致 | PASS |

備考: 「約45,000」の根拠は Track 9 doc-verify §3.3 で検算成立（38,261 + 7,962 ≈ 46,223）。Phase B での文脈上の用法も正確。なお Track 7 自体には「2000-2025期は学術知の22%」が「実DBでは34.5%」というWARN（doc-verify指摘）が残存するが、Phase B での該当数値引用は無し。

### 6. Track 8 (AA) 系数値

| Phase A 値 | Phase A source | Phase B 引用箇所 | 引用値 | 一致/差分 | 判定 |
|---|---|---|---|---|---|
| AA 2024+2025集中 408件・74% | track8-doc-verify §V-12 / sentinel | b1-analysis L620/L1132, b1-report L583/L625/L627, b1-verification L437-438 | 408件・74% | 完全一致 | PASS |
| AA mentions 551 / sources 464 | track8-doc-verify L-05 | b1-analysis L620/L1134, b1-verification L437-438 | 551件 / 464 | 完全一致 | PASS |
| AA 三系列差（ブリーフィング498 / DB実値551 / 集中408） | track8-doc-verify §V-03 | b1-verification L437-438 | 498 / 551 / 408 適切に併記 | 完全一致（開示済） | PASS |

備考: B-1 verification.html L437-438 で Track 8 が開示した三系列差を適切に追跡記述。Track 5 と Track 8 が同一AAスナップショットを共有する論点も B-1 が整合的に扱う。

### 7. Track 9 (4DB) 系数値 ★WARN 検出

#### 7.1 B-1 側引用 — DB実値で正確に継承

| Phase A DB実値 | Phase A source | B-1 引用箇所 | 引用値 | 判定 |
|---|---|---|---|---|
| PHIL 10,292概念 | track9-doc-verify L-01 / sentinel | b1-analysis L521/L527/L638/L998 | 10,292概念 | PASS |
| LIT 11,115概念 | track9-doc-verify L-01 | b1-analysis L521/L638 | 11,115概念 | PASS |
| MY 11,936物語 | track9-doc-verify L-01 | b1-analysis L521/L549/L638, b1-report L1184/L1318 | 11,936物語 | PASS |
| TK 3,002グループ / 36,360項目 / 16,260関係 | track9-doc-verify L-01 | b1-analysis L521/L537/L638, b1-report L1103 | 3,002グループ・36,360項目 | PASS |
| PHIL 西洋5,008・東アジア1,938・横断750 等 | track9-sentinel / doc-verify L-08 | b1-analysis L527 | 完全継承 | PASS |
| PHIL 古代2,107・中世1,380 | track9-doc-verify L-13 | b1-analysis L537 | 完全継承 | PASS |

#### 7.2 B-2 側引用 — ★ブリーフィング値（旧値）を残存使用

| Phase A DB実値 | B-2 引用箇所 | B-2 引用値 | 差分 | 判定 |
|---|---|---|---|---|
| PHIL 10,292概念 | b2-analysis L176, b2-report L764 | **9,583概念** | -709（旧ブリーフィング値） | **WARN** |
| MY 11,936物語 | b2-analysis L178, b2-report L764 | **10,615物語** | -1,321（旧ブリーフィング値） | **WARN** |
| TK 3,002グループ | b2-analysis L179 | **3,001グループ** | -1（許容差±1、ただしB-1は3,002） | WARN（軽微） |
| LIT 11,115概念 | b2-analysis L177, b2-report L764 | 11,115概念 | 完全一致 | PASS |
| TK 36,360項目 | b2-analysis L179, b2-report L764 | 36,360項目 | 完全一致 | PASS |

備考: Track 9 doc-verify §1.1 の三系列差表で示された通り、9,583/10,615/3,001 は Phase A の「ブリーフィング値」であり、DB実値（10,292/11,936/3,002）との差分が当該文書で明示開示・採用宣言されている。にもかかわらず B-2 はブリーフィング値を残存使用。これは Phase B 内 Track 間（B-1 vs B-2）で同一DBに対する数値が不整合の状態。

### 8. Track 4 (歴史素材) 系数値

| Phase A 値 | Phase A source | Phase B 引用箇所 | 引用値 | 判定 |
|---|---|---|---|---|
| SIF 7,389事象 | track4_handoff（推測） | b1-analysis L521 | 7,389事象 | PASS（要追跡）|
| TA 226,996レコード | track8-doc-verify §1.2 | b1-analysis L521 | 226,996レコード | PASS |
| HIC 20ケース | track4_handoff（推測） | b1-analysis L521 | 20ケース | PASS（要追跡）|

備考: Track 4 handoff の本確認は本監査で省略（タスク必須対象外）。値自体は MEMORY.md・既存DBレジストリと整合。

---

## WARN 一覧

### WARN-1: B-2 文書での Track 9 PHIL/MY 旧ブリーフィング値残存

**重大度**: 中（事実不整合だが Phase A 自体が両系列を開示済のため悪意の改変ではない）

**所在**:
- `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-b/track-b2-already-future-analysis.html` L176（PHIL 9,583概念）
- 同 L178（MY 10,615物語）
- `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-b/track-b2-already-future-report.html` L764（PHIL 9,583概念 / MY 10,615物語）

**Phase A ground truth**: PHIL 10,292概念 / MY 11,936物語（track9-doc-verify L-01、track9-sentinel）

**改変理由の探索**: track-b2_handoff.md には数値選択の理由記述なし。Phase B Track B-2 が Phase A Track 9 のブリーフィング値（古いスナップショット）を参照したまま DB 実値への置換を失念したと推測。同一文書内の LIT 11,115（実値）/ TK 36,360項目（実値）は正確のため、PHIL と MY のみ部分的に旧値が残存している。

**B-1 との不整合**: B-1 analysis.html L521/L638 と b1-report L601/L792 では PHIL 10,292・MY 11,936 を正確に引用しており、Phase B 内 Track 間で同一DBに異なる値が並存している状態。

**推奨アクション**: B-5/B-6 統合エージェントが B-2 の該当2箇所＋3箇所（合計5箇所）を DB 実値に置換。Phase A 第7部 §7.1 の方針（DB実値を一次値、ブリーフィング値は時点の異なる有効値として併記）に従い、置換時は注釈で経緯を明示することが望ましい。

### WARN-2: TK グループ数 ±1 差（3,001 vs 3,002）

**重大度**: 軽微（許容差）

**所在**: track-b2-already-future-analysis.html L179（3,001グループ）

**Phase A ground truth**: TK 3,002グループ（track9-doc-verify L-01、track9-sentinel）

**判定根拠**: track9-doc-verify は ±1 を「無視可能」として OK 判定済。ただし B-1 は 3,002 を使用、B-2 のみ 3,001 を残しているため、Wave 4 統合時の文書間の見栄え整合性として置換推奨。

---

## FAIL 一覧

なし。

---

## 補足: B-3 の Phase A 数値継承

B-3（track-b3-good-society-paths-*）は Phase A の主要数値を直接引用していない。代わりに以下のメタ情報を継承する形:
- 「Phase A Mサイン認定領域」「物語転換期」「pluriverse cosmology」「世代間正義」「第四変容期」などの概念ラベル
- 「critical juncture 8点の 5/8 が Phase A Mサイン領域と接続」（62.5% の独自指標）
- B-1 41問 + B-2 85 wisdom + Phase A Track 9 善い社会論述の入力源宣言

数値継承の改変リスクは B-3 では低い。質的継承の整合性は別途 B-3 sentinel/doc-verify の領分。

---

## Phase B Track B-4/B-5/B-6 への申し送り — 最終 source-of-truth

Wave 4 統合段階で B-5/B-6 が継承すべき Phase A 数値の最終 source-of-truth を以下に固定する。WARN-1 の影響を受けた数値は **DB実値（B-1 で採用された値）を採用** し、B-2 側のブリーフィング値は採用しない。

### 確定 source-of-truth テーブル

| 系統 | Phase A ground truth | Phase B 採用値 | 引用元（最優先） |
|---|---|---|---|
| FK values空白 | 105件 / 0.45% | **105件 / 0.45%** | b1-analysis L638, b1-report L601 |
| FK trends | 650件 | **650件**（必要時） | track1-sentinel |
| CLA総レコード | 91,550行 / 19テーブル / 127年 | **91,550 / 19テーブル / 127年** | b1-analysis L549 |
| CLA Thompson Motif | 45,496件 | **45,496件** | b1-analysis L549 |
| CLA myth/worldview keyword | 2,858件 | **2,858件** | b1-analysis L620 |
| SG disruption ピーク | 7.49（2024-2026、126年最高） | **7.49** | b1-analysis L620, b1-report L583 |
| SG paradigm_shift current | 20.4%（past比+6.0pt） | **20.4%** | b1-analysis L620, b1-report L583 |
| SG myth層 current | 11.1%（U字回復） | **11.1%** | b1-analysis L620, b1-report L583 |
| ET 人物 | 12,958人物 / 31,430スコア | **12,958 / 31,430** | b1-analysis L521 |
| GF 人物 | 9,178人物 | **9,178** | b1-analysis L521 |
| JPMS v2 校 | 832校 / 58,224件 | **832 / 58,224** | b1-analysis L521 |
| PST 偉人 | 600偉人 / 10アーキタイプ | **600 / 10** | b1-analysis L521 |
| Academic 5領域概念 | 17,547概念（執筆時）/ 18,090（最新） | **17,547概念**（B-1 表記基準） | b1-analysis L521 |
| Academic CTL-V | 7,962概念（45.4%） | **7,962（45.4%）** | b1-analysis L638 |
| 規範的論述群合算 | 約45,000（4DB 38,261 + Track 7 7,962 = 46,223） | **約45,000規範的論述群** | b1-report L601 |
| AA mentions / sources | 551 / 464（DB実値） | **551 / 464** | b1-analysis L620, b1-verification L437 |
| AA 2024-2025集中 | 408件 / 74%（275+133=408） | **408件 / 74%** | b1-report L583 |
| AA 三系列差（透明性開示） | ブリーフィング498 / DB実値551 / 集中408 | **三系列併記**（Phase A方針継承） | b1-verification L437-438 |
| PHIL 概念総数 | **10,292概念**（DB実値） | **10,292概念** | b1-analysis L521/L638（B-2 の 9,583 は採用しない）|
| PHIL 関係数 | 37,789 | **37,789** | track9-doc-verify L-01 |
| PHIL 27サブフィールド / 8文明圏 | 27 / 8 | **27 / 8** | track9-doc-verify L-01 |
| LIT 概念総数 | 11,115概念 | **11,115概念** | b1-analysis L521 |
| LIT 24サブフィールド | 24 / 第四変容タグ 9,045件 | **24 / 9,045** | b2-analysis L177 |
| MY 物語総数 | **11,936物語**（DB実値） | **11,936物語** | b1-analysis L521/L549/L638（B-2 の 10,615 は採用しない）|
| TK グループ | **3,002グループ**（DB実値） | **3,002グループ** | b1-analysis L521（B-2 の 3,001 は採用しない）|
| TK 項目 | 36,360項目 | **36,360項目** | b1-analysis L521/L537/L638 |
| TK 関係 | 16,260関係 | **16,260関係** | track9-doc-verify L-01 |
| AN 概念 | 500概念 | **500概念** | b2-report L764 |
| 4DB合算規範論述 | 約32,000概念（PHIL 10,292 + LIT 11,115 + MY 11,936 + TK 3,002 を合算根拠とする） | 約32K（Track 9 §3.3 検算成立） | track9-doc-verify §3.3 |
| SIF 事象 | 7,389事象 | **7,389事象** | b1-analysis L521 |
| TA レコード | 226,996レコード（44表） | **226,996レコード** | b1-analysis L521 |
| HIC ケース | 20ケース | **20ケース** | b1-analysis L521 |

### Phase A 9 Track の構造的限界（Phase B 全体で継承）

Phase A 第8部の構造的5限界は Phase B Wave 4 統合まで継承される（b1-report L1361 で明記）:
1. 9DB の近代偏重バイアス
2. 集計の濃淡
3. 同一プロジェクト派生間の独立性問題（pestle-signal-db / great_figures.db / ai_acceleration_evidence.db の共有）
4. GF 共有問題の射程
5. FK 84.4% 共通スパン未指定率

これらは Wave 4 統合段階で「再追跡可能な構造的限界」として開示維持すべき。

---

## 監査の制約と限界

1. **本監査は grep ベースの機械検証**: 数値の文脈的妥当性（例: 「約」「概ね」修飾語の正確性）は完全には判定していない。
2. **Track 1/4 の handoff.md は ryoiki ディレクトリに存在せず**: doc-verify-report と sentinel-verdict から ground truth を抽出。
3. **B-3 の質的内容検証は本監査の射程外**: B-3 sentinel/doc-verify が別途行う領分。
4. **B-4（既出）も B-1〜B-3 並列稼働中の中間状態**として読み取りのみ実施し、本監査では検証対象外。
5. **B-2 verification.html (L437-438類似) の独自開示有無**: 本監査では確認していない。WARN-1 が B-2 verification 側で既に開示されている場合は判定が変わる可能性あり。

---

監査者: Claude Opus 4.7 (1M context) / Phase B 横断検証 sentinel
完了報告先: Wave 4 統合エージェント / B-5/B-6 リードエージェント
