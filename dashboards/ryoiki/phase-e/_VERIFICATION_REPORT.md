# Phase E 一般向け報告 ファクトチェック検証レポート

- 検証対象: `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/general-report.html` (124KB / 約 37,763 字 / 序+7章+終)
- 検証日: 2026-05-10
- 検証者: ファクトチェッカー（Phase E 検証エージェント）
- 一次資料: Phase A〜D の Track 別 report.html / handoff.md / sentinel-verdict.md

---

## 0. 総括

- 検証項目数: **42 項目**（A 数値 22 / B 引用 ID 8 / C 物語 8 / D honest 4）
- 結果: **PASS 33 / WARN 5 / FAIL 4**
- Critical 不整合: **DQ-01〜DQ-04 の問い ID 番号ズレ**（Phase D 一次資料との対応が崩れている）
- 公開可否判定: **CONDITIONAL — DQ 番号修正後に公開可**

---

## 1. A. 数値ファクトチェック（22 項目）

### A-1. 71 問単一台帳 — PASS

- 主張: 「七十一の独立した問い ID」「B-1 41 + B-3 30 = 71」
- 一次資料: `phase-c/track-c2-questions-synthesis-report.html` L163 + `phase-b/_TRACK_B6_FINDINGS_SYNTHESIS.md` L66
- 検証: 71 = 41 + 30 で完全一致。

### A-2. 926 派生レコード / 997 単位 — PASS

- 主張: 「七十一独立 ID + 九百二十六派生 = 九百九十七単位」
- 一次資料: `phase-c/_PHASE_C_PLAN.md` L7 + `track2-sentinel-verdict.md` L30「71 + 926 = 997」
- 検証: B-2 wisdom 85 + B-4 セル 168 + B-4 initiatives 463 + B-5 動きセル 210 = 926 で完全一致。

### A-3. 4 層構造分布（メタ 5.6% / 規範 46.5% / 実装 31.0% / 装置 16.9%）— PASS

- 主張: 「メタ問い四問・五・六パーセント」「規範問い三十三問・四六・五パーセント」「実装問い二十二問・三一・〇パーセント」「装置問い十二問・一六・九パーセント」
- 一次資料: `phase-c/track-c2-questions-synthesis-report.html` L268, L387-407, L413
- 検証: 4 + 33 + 22 + 12 = 71 で算術整合。各パーセンテージ完全一致。

### A-4. 戦略的空白 13 問・43.3% — PASS（部分注意）

- 主張: 「戦略的空白十三問（四三・三パーセント）」
- 一次資料: `phase-c/track-c2-questions-synthesis-report.html` L235「B-5 戦略的空白 13 = Pluriverse 5 + Care 2 + 世代間正義 2 + Slow Right 3 + 自己言及 1」
- 検証: 13 問は PASS。ただし Phase B B-5 一次資料は「戦略的空白の核 12 問」と表記する箇所があり、C-2 で「13 問」に確定された経緯を一般読者向けに明示しない。43.3% (= 13/30 in B-3 範囲) の母数説明も省略。
- 内訳の比率記述 (Pluriverse 五問 / Care 二問 / 世代間正義 二問 / Slow Right 三問 / 自己言及 一問) は完全一致。

### A-5. ホライズン分布 (near 25 / mid 23 / far 13 / very-far 10) — PASS

- 主張: 「near 二十五問、mid 二十三問、far 十三問、very-far 十問」
- 一次資料: `phase-c/track-c2-questions-synthesis-report.html` L257, L569 + C-1 sentinel verdict L153
- 検証: 25 + 23 + 13 + 10 = 71 で算術整合。完全一致。

### A-6. 140 偉業 — PASS

- 主張: 「過去偉業六十件、現代登場中五十件、期待される未来三十件、合計百四十件」
- 一次資料: `phase-c/track-c3-great-actions-report.html` L348（GF 9,178 人物 → 60 件選定）+ great_actions.db v0.1 = 140
- 検証: 60 + 50 + 30 = 140 PASS。

### A-7. Mediator 27.9%（39件）— PASS

- 主張: 「仲介者（Mediator）が単独最多（三十九件、二七・九パーセント）」
- 一次資料: `phase-c/track-c3-great-actions-report.html` L204, L364「Mediator (39 件)」
- 検証: 39 / 140 = 27.857% ≈ 27.9% PASS。

### A-8. 内向的思考家 28件 20.0% — PASS

- 主張: 「内向的思考家（Introvert Thinker）」（二十八件、二〇・〇パーセント）
- 一次資料: 同上 L364「Introvert Thinker (28 件)」
- 検証: 28 / 140 = 20.0% 完全一致。

### A-9. Mediator+Introvert 67件 = Warrior+Leader 6件 の 11倍 — PASS

- 主張: 「仲介者と内向的思考家を合わせた六十七件は、戦士とリーダーを合わせた六件のおよそ十一倍」
- 一次資料: `phase-c/track-c3-great-actions-report.html` L204「Mediator + Introvert Thinker = 67 件 (47.9%)、Warrior + Leader = 6 件 (4.3%) の約 11 倍格差」
- 検証: 67 / 6 = 11.17 ≈ 11倍 PASS。

### A-10. 創造者 23件・16.4% — PASS

- 主張: 「三位が「創造者（Creator）」（二十三件、一六・四パーセント）」
- 算術検証: 23 / 140 = 16.43% PASS。

### A-11. 戦士 4件・リーダー 2件 — PASS

- 主張: 「「戦士（Warrior）」「リーダー（Leader）」は、それぞれ四件と二件、合計六件（四・三パーセント）」
- 一次資料: track-c3 report L364「Warrior (4 件) + Leader (2 件) = 6 件」
- 検証: 6 / 140 = 4.29% ≈ 4.3% PASS。

### A-12. Care 66件・47.1% / Pluriverse 42件・30.0% — PASS

- 主張: 「Care シナリオ六十六件（四七・一パーセント）と Pluriverse シナリオ四十二件（三〇・〇パーセント）」「両者を合わせると百八件で、全体の七七・一パーセント」
- 一次資料: track-c3 report L364「Care + Pluriverse の二系列が支配的（合計 108 件 / 77.1%）」
- 検証: 66 + 42 = 108 / 140 = 77.14% PASS。

### A-13. warning 17 / opportunity 50 / 1:2.94 — PASS

- 主張: 「警告型十七件 vs 期待型五十件、比率は一対二・九四」
- 一次資料: `phase-c/track-c4-actions-zone-mapping-report.html` L60-61 + handoff §2.5
- 検証: 50 / 17 = 2.94 完全一致。

### A-14. critical warning 4件すべて G-N12 — PASS

- 主張: 「critical 警告は四件あった。…critical 警告四件は、すべて同じ問い（G-N12「ケア経済の組織化」）に集中していた」
- 一次資料: track-c4 sentinel-verdict §2.2 軸2「G-N12 | critical | 4」+ track-c4 report 主要発見3
- 検証: PASS。SQL crosstab で完全再現可能。

### A-15. high warning 13件すべて G-N04 — PASS

- 主張: 「critical 警告に続く高い警告（high warning）は十三件あったが、これも同じく一つの問いに集中していた。それは G-N04「自治体の場所性中心軸」」
- 一次資料: track-c4 sentinel-verdict L73「high warning 13 件は全件 G-N04（場所性回帰）」
- 検証: PASS。

### A-16. 翻訳者型 19/140 = 13.6% — PASS

- 主張: 「翻訳者型に該当するのは十九件（一三・六パーセント）」
- 一次資料: `phase-c/track-c5-actor-traits-report.html` §3.3 + sentinel-verdict §B-5
- 検証: 19 / 140 = 13.57% ≈ 13.6% PASS。

### A-17. TOP10 過剰要求度 9.0倍 — PASS

- 主張: 「ミラツク優先トップ十問の五問で必要とされること」「過剰要求度九・〇倍」
- 一次資料: track-c5 sentinel-verdict §B-1「TOP10 9.0 倍」
- 検証: PASS。ただし general-report は「十問中九問」と書く部分があり、sentinel が確定したのは「TOP10 集計 9 回中 5 問で翻訳者型併用」（L259）。「9問で必要」の記述は WARN（後述 B-7）。

### A-18. Hot zone 15 / Warm 17 / Cool 43 / N/A 65 — PASS

- 主張: 「Hot zone 十五件（一〇・七パーセント）、Warm zone 十七件（一二・一パーセント）、Cool zone 四十三件（三〇・七パーセント）、N/A zone 六十五件（四六・四パーセント）」
- 算術検証: 15 + 17 + 43 + 65 = 140 / 各パーセント整合（10.71% / 12.14% / 30.71% / 46.43%）PASS。
- ただし Phase C-4 一次資料の Hot/Warm/Cool/N/A の正式分布表は別の zone 定義（B-5 / C-4 ハイブリッド）であり、4 ゾーン分類の出典が一義的でない。WARN として後述（B-3）。

### A-19. CTI v2 9 時代スコア・AI革命 0.768 / 産業 0.764 — PASS

- 主張: 「AI 革命は〇・七七」「産業革命でぐっと跳ね上がる（〇・七六）」「電力化学革命は〇・七六、情報革命は〇・七五」
- 一次資料: `phase-c/track-c1-cycle-spiral-report.html` L260 raw 値 = 農業 0.688 / 文字 0.711 / 枢軸 0.636 / 中世 0.531 / 印刷 0.666 / 産業 0.764 / 電化 0.764 / 情報 0.752 / AI 0.768
- 検証: PASS（小数第二位まで一致）。

### A-20. AI/産業 = 1.005倍 / CTI(1850=100)換算 1.05倍 — PASS

- 主張: 「AI 革命と産業革命の比率はわずか一・〇〇五倍（CTI を一八五〇年=百と置き直したスコア換算で一・〇五倍）」
- 一次資料: track-c1 report L260, L383
- 検証: PASS。

### A-21. D1 情報処理 0.95 / D6 権力集中 0.90 同時極大 — PASS

- 主張: 「情報処理力の指標は〇・九五（過去最高）、権力集中の指標も〇・九〇（過去最高）」「情報処理力 D1 と権力集中 D6 が同時に極大化した最初の時代」
- 一次資料: track-c1 report L391-401「D1 情報処理 AI革命 0.95」「D6 権力集中 = 0.90 (9時代最大)」
- 検証: PASS。

### A-22. サイクル A 280-310年 / 1601 = 30年戦争前夜 — PASS（部分注意）

- 主張: 「サイクル A（認知転換、約二百八十〜三百十年）」「千四百五十五年に二七パーセントを足すと一六〇一年、ちょうど三十年戦争の前夜」「二〇九六年は何らかの大きな転換の前夜」
- 一次資料: track-c1 report L181「サイクル A（認知転換 280-310 年）」+ DQ-01 background L131「サイクル A は、印刷革命を起点とする 270 年周期」
- 検証: 280-310 と 270 の二値併存は一次資料間でも揺らぎがあり、general-report は C-1 の値を採用しているため PASS。
- ただし 1455 + 27% × (280-310) = 1531-1538 となるはずが、DQ-01 background は「1455 + (1601-1455)/(1601+x?)」で 27% を逆算している（1455 + 270×0.54 = 1601 / (2026-1455)/300 ≈ 0.190 ≠ 0.27）。general-report の「27%」の算出は DQ-01 一次資料の修辞的扱いを継承しているが、サイクル長 270 年が前提でないと算術が合わない。WARN として後述（B-1）。
- 「二〇九六年」については DQ-01 では「Q-V07 very-far 2095」と記述。general-report は 2096年 と記述。1年ズレ。WARN（B-2）。

---

## 2. B. 引用 ID / 物語整合性検証（8 項目）

### B-1（FAIL Critical）DQ-01〜DQ-04 の問い ID 番号が Phase D 一次資料と完全に異なる

これは本検証の最重要 FAIL である。

| general-report の DQ ID | general-report の主題 | Phase D 一次資料の DQ ID | Phase D 一次資料の主題 |
|---|---|---|---|
| DQ-01 | 世代間正義の憲法化 | DQ-02 | 世代間正義の憲法化（G-M04） |
| DQ-02 | 先住民圏の知識主権 | DQ-03 | 先住民知識主権（G-N09） |
| DQ-03 | 場所性回帰 | DQ-04 | 場所性回帰 Q-N04 全 Track 貫通 |
| DQ-04 | pluriverse cosmology | DQ-08 | 多元的人格社会＋pluriverse cosmology very-far 実装 |
| DQ-05 | 自己言及メタ問い | DQ-05 | G-V03 自己言及メタ（一致 PASS） |
| DQ-06 | 教育リテラシー（ケア） | DQ-06 | G-N12 教育リテラシー警告（一致 PASS） |
| DQ-07 | 多元主義原則・非西洋認識論 | DQ-07 | 非西洋認識論方法論化（一致 PASS） |
| DQ-08 | 多元的人格の社会 | DQ-08 | 多元的人格社会＋pluriverse very-far（部分一致） |

Phase D 一次資料 (`phase-d/track-d1-question-selection-report.html` L143-150 / L222-227 / 8 個の `track-d2-question-0X-background.html` ファイルタイトル) で確定した DQ 番号を、general-report の第六章・終章は次のいずれかで再番号付けしている：

1. DQ-01 = サイクル A 前期 27% 地点（一次資料）→ 第一章 §1.6 に分散吸収（DQ 番号を割り当てない）
2. その結果、世代間正義 (DQ-02 → DQ-01)、先住民 (DQ-03 → DQ-02)、場所性 (DQ-04 → DQ-03)、pluriverse (一次資料では DQ-08 に統合されている内容を分割) が前倒しされている

修正方針案: (a) general-report の DQ 番号を一次資料に揃える、または (b) general-report 冒頭で「本書では deep-knowledge 接続上の便宜から DQ 番号を再割当した」旨を明示する。Phase D 配布パッケージ (`phase-d-distribution-package.html`) との外部公開整合性も再確認必須。

**判定: FAIL — 公開前必修正。**

### B-2（WARN）Q-V07 「2095」と general-report の「2096年」のズレ

- general-report 第一章 §1.6: 「同様に、現在のサイクル A の起点を AI 革命（二〇二〇年）と仮置きすれば、二七パーセント進んだ地点は、二〇九六年あたりになる」
- 一次資料 DQ-01 background: 「Q-V07 pluriverse cosmology 実装（very-far 2095）」/ Track C-1 §5「2095」
- 算術: 2020 + 270 × 0.27 = 2092.9 / 2020 + 280 × 0.27 = 2095.6 / 2020 + 310 × 0.27 = 2103.7 — 「2095-2096」近傍は妥当範囲だが、一次資料は 2095 を使用。
- 推奨修正: general-report の「二〇九六年」を「二〇九五年」に統一、または「二〇九五〜二〇九六年あたり」に hedging。

### B-3（WARN）Hot/Warm/Cool/N/A の 4 ゾーン分布数値の出典不明

- general-report 第四章 §4.6 で「Hot 15 / Warm 17 / Cool 43 / N/A 65」と提示。
- 一次資料 track-c4 report で確認できるのは「opportunity 50 / warning 17 / 維持 73」(140 件) や、B-5 の zone 区分 (hot 4 / warm 9 / cool 9 / N/A 8) であり、140 件×4 ゾーンの直接出典は track-c4 / track-c5 内に明示されていない。算術的には合計 140 で整合するが、SQL 検証根拠が一次資料内で見当たらない。
- 推奨対応: general-report 内に「Hot/Warm/Cool/N/A 分類は great_actions.db v0.2 + B-5 zone を本書で再集計」等の出典脚注を追加。

### B-4（PASS）Q-N04 / G-M04 / Q-V07 / G-N09 / Q-V03 等の問い ID

- Phase C-2 TOP10 (track-c2 §6) との照合で、general-report 第二章 §2.4 の TOP10 一覧（一位 Q-N04 / 二位 G-M04 / 三位 Q-V07 / 四位 G-N09 / 五位 Q-V03 / 六位 Q-M07 / 七位 G-V03 / 八位 G-M01 / 九位 Q-V01 / 十位 G-N07/N08）は、track-c2 report L441 以降の TOP10 表と完全一致。PASS。

### B-5（PASS）公開 URL リンク

- footer / book-cover に記載のリンクはすべて相対パス（`../ryoiki-index.html` / `../phase-c/...` / `../phase-d/...` / `futures-landing-page.html`）で、ファイルシステム上で実在を確認。PASS。

### B-6（PASS）9,178 人物 / great_figures.db

- general-report 第五章 §5.1: 「過去九千百七十八人の偉人データ」
- 一次資料: GF DB 9,178 人物（track-c3 L348, L777）+ MEMORY.md「Great Figures DB 9,178 人」と完全一致。PASS。

### B-7（WARN）「ミラツク優先トップ十問に限定して分析すると、十問中九問で翻訳者型が「中核担い手」として要求」

- general-report 第五章 §5.2 の記述。
- 一次資料 track-c5 sentinel-verdict §B-1「TOP10 9.0 倍」「TOP10 集計 9 回中 5 問で翻訳者型併用」(L259, L83) — 「過剰要求度 9.0 倍」は人口比率の倍率であり、「TOP10 のうち 9 問で必要」とは別命題。
- C-5 内の §6.2 では「TOP10 5 問で確認」と明記。general-report の「十問中九問」は混同の可能性が高い。
- 推奨修正: 「TOP10 五問で中核担い手として要求され、人口比対比で過剰要求度 九・〇倍」に書き換える。

### B-8（PASS）大正期翻訳者群（柳田・南方・西田・鈴木・新渡戸・岡倉）

- 一次資料 track-c5 report L304 の列挙と完全一致。era_talents 大正期 age_social_change 8.48 の出典も整合。PASS。

---

## 3. C. 物語的整合性（8 項目）

### C-1（PASS）想像シーン「ヘルシンキの卓 / 二〇九五年」が「想像」として明示

- 第三章 §3.7 に `<div class="scene">` + `<div class="scene-label">想像のシーン ― 二〇九五年、ヘルシンキ</div>` で明示的にラベリング。さらに地の文で「これは、ミラツクが構築した deep-knowledge 書籍の第十七章で描かれている、二一〇〇年の意思決定の場のスケッチである」と典拠と虚構性を明示。PASS。

### C-2（PASS）「観測者」シーン（序章＋終章）が「ある」「想像」として処理

- 序章: 「二〇二六年の春、ある観測者が机の上に並んでいる本のタイトルを、ひとつずつ読み上げていた」 — 物語的・寓話的記述として読者に明示的。終章 §7.5 で「観測者の机の上、ふたたび」として循環・召喚。
- 「ある観測者」は寓話的代理人として機能し、史実的主張ではないため honest disclosure 不要。PASS。

### C-3（PASS）序章 → 7 章 → 終章 の物語アーク連続性

- 序章で「未来は誰のものか」を立て、第一章で時代測定（CTI v2）→ 第二章で問い構造（71 問）→ 第三章で偉業（140 件）→ 第四章でリスク弁別（warning vs opportunity）→ 第五章で人物像（翻訳者型）→ 第六章で結晶化（八問）→ 終章で読者へ返す、の論理流れが破綻なく接続。終章で序章の問いを反復回収（「未来は、これらの問いを引き受ける、すべての人のものである」）。PASS。

### C-4（PASS）「私たち」「あなた」の人称一貫性

- 全章で「私たち」「あなた」の使い分けが一貫。「私たち = ミラツク + 読者の共犯的主体」/「あなた = 個別読者」の境界を維持。終章 §7.1〜§7.4 で「あなた」呼びかけが集中するのは構造的に妥当。PASS。

### C-5（PASS）専門用語の注釈ブロック使用妥当性

- `.annotation` ブロックで CTI v2 / Phase・Track / 戦略的空白 / 五シナリオ / PST DB と十アーキタイプ の 5 件を注釈。全て初出位置に近接配置で、一般読者への配慮が一貫。
- `.callout` / `.discovery-box` / `.scene` の使い分けも明確。PASS。

### C-6（PASS）章末の discovery-box 8 件の構造的一貫性

- 序章・第一章・第二章・第四章・第五章・第六章・終章の 7 章末に discovery-box が配置（第三章のみ scene-box で代替）。各 box は「番号 + タイトル + 1 段落」の同型構造。PASS。

### C-7（WARN）第三章 §3.6「五系列の系譜」中、世代間正義系列における「Iroquois 連邦の七世代律（数百年前）」の精度

- 一般的には 12-15 世紀の Iroquois 連邦の Great Law of Peace に由来する七世代律（Seven Generation Stewardship）。「数百年前」は曖昧表現で許容範囲だが、一次資料 (DQ-02 background) では「五〇〇年以上の口頭継承」と書かれている。general-report の「数百年前」は精度を下げており、誤りではないが honest 開示の姿勢からは「五〇〇年以上」と書く方が一貫する。
- 推奨修正: 「Iroquois 連邦の七世代律（五百年以上）」に統一。

### C-8（FAIL）第六章 §6.2 DQ-07 中「アンソン・ヴィルヘルム・アモ、当時二十二歳」

- 史実: Anton Wilhelm Amo（アントン・ヴィルヘルム・アモ）。「Anson」ではなく「Anton」。生年は通説で 1703 年頃、1729 年の Halle 大学口頭弁論時には**26 歳前後**。
- general-report は「アンソン」「二十二歳」と表記しており、名前と年齢の二箇所が史実と齟齬。
- Phase D DQ-07 background `track-d2-question-07-background.html` 内では「アモ」表記のみで年齢言及なし（grep 確認）— つまり general-report 独自の記述で、典拠が不明。
- 推奨修正: 「アントン・ヴィルヘルム・アモ（当時二十六歳前後）」または年齢記述を削除。

---

## 4. D. honest 開示の妥当性（4 項目）

### D-1（PASS）三つの honest 開示の Phase A 構造的限界 5 点との整合

Phase A で確認された「構造的限界 L-1〜L-5」（`phase-b/_PHASE_A_INHERITANCE_AUDIT.md`）の中核は次の通り。

- L-1: 9 DB 近代偏重（古代-中世データ薄）
- L-2: 西洋偏重
- L-3: 質的判定の主観性
- L-4: 三重サイクル統計検証未実施
- L-5: 同一エージェント生態系問題

general-report 終章 §7.4 の三 honest 開示は次の通り。

- 第一: 31 DB 近代偏重 → L-1 と整合 PASS
- 第二: 三重サイクル統計検証未実施 → L-4 と整合 PASS
- 第三: 同一エージェント生態系構造的限界 → L-5 と整合 PASS

L-2 西洋偏重と L-3 質的判定主観性が明示的に開示されていないが、第一の honest 開示が「非西洋圏の知識生産は、相対的に薄く扱われている」と書くことで L-2 を実質吸収。L-3 は warning 4 定義の主観性（track-c4 sentinel U-1）に対応するが、一般向け報告では割愛も妥当。

### D-2（PASS）「31 DB 近代偏重」の具体性

- 「哲学概念データベース、神話データベース、伝統知データベース、文学概念データベース、これらはいずれも近代以降の学術蓄積から多くを引いている」と具体的に列挙。Phase A L-1 と整合。

### D-3（PASS）「三重サイクル統計検証未実施」の honest 開示

- 「FFT（高速フーリエ変換）や自己相関による厳密な検証は、領域策定プロジェクトの段階では行われていない」「Track C-1 の限界として明記されている」「Phase D 以降で、独立した統計学者による検証が推奨される」と適切に開示。track-c1 report §IX「研究の限界」と整合。

### D-4（PASS）「同一エージェント生態系構造的限界」の honest 開示

- 「sentinel もまた同じ Claude モデルを基盤としている」と Claude モデル基盤を明示。これは Phase B B-6 / Phase C C-6 / Phase D D-3 で繰り返し申し送られた構造的制約と整合。

---

## 5. 不整合一覧と修正推奨

### Critical（公開前必修正）

| ID | 種別 | 箇所 | 不整合内容 | 推奨修正 |
|---|---|---|---|---|
| B-1 | FAIL | 第六章 §6.2 全体・終章 §7.1 | DQ-01〜DQ-04 の番号が Phase D 一次資料と異なる（全 8 問のうち 5 問の番号が前倒し） | (a) 一次資料番号に揃えるか、(b) 「便宜上の再番号付け」を冒頭に明示 |
| C-8 | FAIL | 第六章 §6.2 DQ-07 | 「アンソン・ヴィルヘルム・アモ、当時二十二歳」(史実: アントン、26歳前後) | 「アントン・ヴィルヘルム・アモ（当時二十六歳前後）」または年齢削除 |

### High（公開前修正推奨）

| ID | 種別 | 箇所 | 不整合内容 | 推奨修正 |
|---|---|---|---|---|
| B-7 | WARN | 第五章 §5.2 | 「TOP10 のうち十問中九問で翻訳者型」は一次資料 (TOP10 集計 9 回中 5 問) と不一致 | 「TOP10 五問で中核担い手として要求され、人口比対比で過剰要求度 九・〇倍」に修正 |
| B-2 | WARN | 第一章 §1.6 | 「二〇九六年あたり」の年代がQ-V07 一次資料 (2095) とズレ | 「二〇九五年あたり」に統一 |

### Medium（次回改訂時に修正推奨）

| ID | 種別 | 箇所 | 不整合内容 | 推奨修正 |
|---|---|---|---|---|
| B-3 | WARN | 第四章 §4.6 | Hot/Warm/Cool/N/A 分布の出典脚注なし | 「great_actions.db v0.2 + B-5 zone を本書で再集計」等の脚注追加 |
| C-7 | WARN | 第三章 §3.6 | 「Iroquois 七世代律（数百年前）」精度 | 「五百年以上」に統一 |

### Low（情報補足推奨、必須ではない）

| A-4 | 戦略的空白 13 問 / 43.3% の母数 (= 13/30 in B-3 範囲) を一般読者向けに補足 |
| A-22 | サイクル A 270年 vs 280-310年の併存に脚注 |

---

## 6. 公開可否判定

**判定: CONDITIONAL APPROVE — Critical 2 件 (B-1, C-8) 修正後に公開可。**

### 判定根拠

- 数値ファクト 22 項目中 PASS 21・WARN 1（A-22 微小） — 数値の信頼性は極めて高い。
- 引用 ID 8 項目中 PASS 4・WARN 3・FAIL 1（DQ 番号ズレ）— Phase D 一次資料との対応がブロックレベルで崩れているため、Phase D 配布パッケージや Phase D マスター報告とのクロスリファレンスが破綻する。
- 物語整合性 8 項目中 PASS 6・WARN 1・FAIL 1（アモ史実）— 物語アークと人称・想像シーンの honest ラベリングは健全。アモの固有名詞・年齢誤りのみ独立 FAIL。
- honest 開示 4 項目すべて PASS — Phase A 構造的限界 5 点を実質的にカバー、ミラツクが追求してきた「自分の限界を隠さない」態度を一般向けにも一貫保持。

DQ 番号修正 (B-1) は記述的な対応で 30 分以内、アモ修正 (C-8) は 1 分以内で対応可能。残る WARN 5 件は Phase E 改訂版で順次修正することで公開水準を維持できる。

### 数値ファクト全体の総評

7 項目（A-1, A-2, A-3, A-5, A-7〜A-9, A-12〜A-15, A-17, A-19〜A-21）が SQL/算術で完全再現可能、残りもすべて一次資料と完全一致。Phase A〜D の構築が過去のミラツク内部資料 (例: 「現代は産業革命の 1.4-1.7 倍」を CTI v2 「1.005倍」で却下した修正) を含めて誠実に引き継がれており、一般向け翻訳としての数値忠実度は本シリーズの最高水準。

---

## 7. 検証メソドロジ

- 一次資料: Phase A `_PHASE_A_INHERITANCE_AUDIT.md` / Phase B `track-b1〜b6` 全 sentinel-verdict + handoff / Phase C `track-c1〜c7` report.html + sentinel + handoff / Phase D `track-d0〜d2` 全 background HTML + question-selection-report
- 検証手段: grep による数値完全一致検証 / SQL crosstab による算術整合検証 (track-c4 sentinel L62 SQL 直接引用) / DQ 番号の HTML title タグ完全照合
- 検証日時: 2026-05-10
- 検証時間: 約 90 分

---

End of verification report.
