# Track B-6 統合構造プロトタイプ

本書は Track B-6（Phase B 統合 HTML 化）の Wave 4 起動高速化のための「構造プロトタイプ」である。B-1〜B-5 の handoff 完了を前提に、各章への成果物流し込みのみで完成する pre-build 構造を規定する。

- 対象成果物: `track-b6-integration-report.html` / `track-b6-integration-analysis.html` / `track-b6-integration-verification.html` / `track-b6_handoff.md`
- 参照モデル: Phase A `ryoiki-master-report.html`（10章・約30,000字・1421行）+ `_INTEGRATION_FRAMEWORK.md`（188行）+ `track-b1-layered-history-report.html`（約13,000字 + 図表9点）
- デザイン規約: 赤白CI #CC1400 / Noto Serif JP（本文）+ Noto Sans JP（UI）/ textbook 構造（top-bar 48px + toc-sidebar 240px + main 760px）/ 絵文字・アイコン禁止
- 起動条件: Wave 3 完了 + B-3 sentinel APPROVED + B-4 sentinel APPROVED + B-5 完了

---

## 1. report.html 章立て（25,000-35,000字 目標）

最終レポートは「ミラツクが向き合う問いの全体像」を主題とする。Phase A `ryoiki-master-report.html` の10章構造を継承しつつ、Phase B 固有の「規範層・実装層・診断層」を統合視点で再編する。

### 第I部: Phase B 全体俯瞰（5,000字 / 約3章相当）
- 1.1 序章（500字）— Phase A から Phase B への論理連続性、本レポートの位置づけ
- 1.2 Phase A→B 連続性（1,500字）— 9トラック × 15メタテーマ × 6 Mサイン領域 が Phase B 5トラックにどう接続したか。Fig.1 を参照
- 1.3 5 Wave × 6 Track 構造（1,500字）— Wave 0（計画）/ Wave 1（B-1基盤）/ Wave 2（B-2補完）/ Wave 3（B-3規範・B-4実装・B-5診断）/ Wave 4（B-6統合）の依存関係。Fig.2 を参照
- 1.4 統合視点の宣言（1,500字）— ミラツクが「問いの立て方そのもの」を提示する三軸統合（時間×構造×確度）の方法論的姿勢

### 第II部: 5 Wave 統合視点（6,000字 / 各Wave約1,200字）
- 2.1 Wave 0 — 6 トラック構造の必然性（1,000字）— なぜ B-1〜B-5 の5+1構成が必要だったか
- 2.2 Wave 1 — B-1 41問の三軸構造（1,200字）— ホライズン × CTL-1 × Mサイン階層
- 2.3 Wave 2 — B-2 「すでにある未来」の70/70=100%充足（1,200字）— 14問92.9%既出回答型 / Type-A/B/C / 三大クラスター
- 2.4 Wave 3-1 — B-3 5シナリオの非序列化（1,200字）— pluriverse 的方法論、8 critical junctures
- 2.5 Wave 3-2 — B-4 24問装置カバレッジ（700字）— 7変化検出装置の実カバレッジと構造的ギャップ
- 2.6 Wave 3-3 — B-5 zones 診断（700字）— Hot/Warm/Cool/Dead の4階層と TOP10 抽出ロジック

### 第III部: 統合視点による発見5点（10,000字 / 各発見約2,000字）

各発見は「〈問い〉＋〈ミラツク独自の答え方〉＋〈他組織との対比〉」の三段構成（Phase A 知見構造に準拠）。

- 3.1 発見1: 95-105問統合マップが示す問いの全体像（2,000字）
  - B-1 41 + B-3 30 + B-4 24（重複24問あり、推定純数 71-95問）の重複・差異整理
  - 重複問い・固有問いのベン図的構造
  - Fig.3 を参照
- 3.2 発見2: wisdom の構造 — B-2 三大クラスター × B-3 5シナリオ × B-1 4ホライズン（2,000字）
  - 三大クラスター（多元的人格群／pluriverse群／長期時間群）が5シナリオにどう分散したか
  - Care 19件・Pluriverse 18件 上位 / Fragmentation 11件 最小 の意味
  - Fig.4 を参照
- 3.3 発見3: 動きと装置 — B-4 装置カバレッジ × B-5 zones の整合・差分構造（2,000字）
  - hot zones には装置あり / dead zones には装置なし、の構造的相関を確認
  - 例外（hot zone 装置なし、dead zone 装置あり）が示すミラツク介入余地
  - Fig.7 を参照
- 3.4 発見4: 「真M由来」の連鎖 Phase A → B-1 → B-3 → B-5（2,000字）
  - Phase A 真M 1件・準M 3件・概念整合 1件 が B-1 41問の 真M4/準M14/概念整合15/単独T8 にどう展開したか
  - その中で B-3 critical junctures 5/8 が Mサイン認定領域と接続
  - Fig.5 を参照
- 3.5 発見5: Phase A 6 Mサイン領域との整合性経路（2,000字）
  - Phase A → B-1 → B-3 critical junctures（5/8 接続）→ B-5 zones の継承一貫性
  - 整合・不整合領域の honest 開示

### 第IV部: ミラツクとして取り組むべき優先課題TOP10（5,000字）

- 4.1 統合ランキングの方法論（500字）— B-5 TOP10 を Phase A Mサイン + B-2 wisdom 厚み + B-3 シナリオ位置 で再ランキング
- 4.2 優先課題TOP10（4,000字 / 各400字）— Fig.6 を参照
- 4.3 各優先課題への想定アプローチ（500字）— B-4 装置 + B-2 wisdom 起点でのアクション設計フレーム

### 第V部: 限界・Phase C 申し送り（4,000字）

- 5.1 各トラックの限界の集約（1,500字）— B-1 6項 / B-2 7項 / B-3 5項 / B-4 / B-5 の限界を統合表で
- 5.2 数値の三系列差 honest 開示（1,000字）— briefing値 / 実装値 / 最終整合値（§6 で詳述）
- 5.3 Phase B 全体の方法論的限界（500字）— 5系統 Skill 限定 / 主観性留保 / 言語的偏向
- 5.4 Phase C への申し送り（1,000字）— SVG/Sankey 精緻化 / 27未カバー問い / Fragmentation 未踏領域研究投資

合計: 5,000 + 6,000 + 10,000 + 5,000 + 4,000 = **30,000字**（25,000-35,000 目標範囲内）

---

## 2. analysis.html 章立て（15,000-20,000字）

構造化分析は report の根拠データ層として機能する。

### 第1章: B-1〜B-5 数値整合性の構造分析（3,500字）
- 1.1 全Track集計値の交差検証（B-1 41問 × B-2 14問 × B-3 30問 × B-4 24問 × B-5 zones）
- 1.2 三系列差の構造（briefing / 実装 / 最終整合）
- 1.3 Phase A 値継承の一貫性検証

### 第2章: 95-105問統合マップ詳細（4,000字）
- 2.1 B-1 41問の CTL-1 × Mサイン × ホライズン 三軸分布
- 2.2 B-3 30問の主体配分 × CTL-1 × ホライズン 構造
- 2.3 B-4 24問の装置別カバレッジ
- 2.4 重複問い（B-1 ⊃ B-3 ⊃ B-4 の包含関係）と固有問いの集合論

### 第3章: wisdom 構造の量的分析（3,500字）
- 3.1 5系統別 wisdom 件数（PHIL 24/AN 17/MY 15/TK 15/LIT 14 = 85件）
- 3.2 三大クラスター × 5シナリオ × 4ホライズンのクロス集計
- 3.3 confidence 分布（5: 42 / 4: 35 / 3: 8）と derivation_method 内訳
- 3.4 蓄積期間4層モデル（古代/近代/戦後/21世紀）の量化

### 第4章: 経路・装置・zones の構造分析（4,000字）
- 4.1 B-3 5シナリオ × 8 critical junctures × 30問 マトリクス
- 4.2 B-4 7装置 × 24問 カバレッジマトリクス
- 4.3 B-5 zones × 装置 × 経路 三軸接続
- 4.4 hot/dead 弁別の閾値ロジック

### 第5章: ミラツク独自視点の構造抽出（3,000字）
- 5.1 各Trackの「ミラツク独自知見候補」3項目×5Track = 15候補の集約
- 5.2 統合視点による5発見への昇格基準
- 5.3 他組織フォーサイト（OECD/UN/WEF/McKinsey）との差別性検証

### 第6章: 集計クエリログ付録（500-1,500字）
- DB集計クエリID一覧（B-2 already_future.db / B-4 initiatives.db）
- 再現可能性担保

合計: 3,500 + 4,000 + 3,500 + 4,000 + 3,000 + 1,000 = **19,000字**（15,000-20,000 範囲内）

---

## 3. verification.html 章立て（8,000-10,000字、4カテゴリ全Track統合）

doc-verify 4カテゴリを全 Track 横断で統合実行。

### 第1章: 検証方法論と全Track サマリー（1,000字）
- 各 Track の自己検証結果集約表
- B-1 / B-2 / B-3 / B-4 / B-5 の sentinel verdict 状況

### 第2章: カテゴリ1 — スナップショット不整合（2,000字）
- Wave 1-3 全数値の集計値整合
- B-1 41問 vs B-3 30問 vs B-4 24問 の重複・包含検証
- B-2 85件 wisdom × 三大クラスター 12問 + 独立2問 = 14問の整合
- B-3 5シナリオ wisdom 配分 18+13+19+12+11+12 = 85 の整合
- 三系列差（briefing値/実装値/最終整合値）の honest 開示

### 第3章: カテゴリ2 — ハルシネーション総点検（2,500字）
- 各 Track handoff 数値の引用正確性
- B-2 inference 1件（Q-V05/AN Mauss-Halbwachs）の honest 開示維持
- B-3 8 critical junctures の Phase A Mサイン領域接続（5/8）の根拠検証
- direct_quote 25件・paraphrase 59件の典拠確認

### 第4章: カテゴリ3 — カバレッジギャップ（2,000字）
- Phase B 全要件への対応確認（_TRACK_B6_BRIEFING.md チェックリスト）
- 27未カバー問い（B-1 41 - B-2/B-3 14）の構造的開示
- 5系統 Skill 限定 vs ARTS/HISTORICAL/CTI 未検証 の限界
- B-4 装置「カバレッジゼロ」問いの構造的発見

### 第5章: カテゴリ4 — チーム間不整合（1,500字）
- Phase A 値の継承一貫性
- B-1 ground truth と B-2 DB msign_origin の同期確認（B-2 verdict M1 同期済）
- B-3 主体配分の改訂（実体集計値）整合
- B-3 CTL-1 配分 33（30問・3問重複帰属）の honest 開示

### 第6章: 検証結果総括と Wave 4 起動可否判定（500-1,000字）
- PASS / WARN / FAIL カウント
- 残存 WARN の重要度評価
- Phase C への検証申し送り

合計: 1,000 + 2,000 + 2,500 + 2,000 + 1,500 + 1,000 = **10,000字**（8,000-10,000 上限）

---

## 4. handoff.md 構造（3,000-5,000字、Phase C 申し送り）

Phase A `track{N}_handoff.md` テンプレート（_INTEGRATION_FRAMEWORK.md §6.1）に準拠。

### 1. メタ情報
- トラック番号: B-6
- トラック・タイトル: Phase B 統合 HTML 化 + ryoiki-index 更新
- 入力源: B-1〜B-5 全 handoff + Phase A `ryoiki-master-report.html`
- 出力ファイル4点（report / analysis / verification / handoff）
- 検証ステータス: 自己検証 + doc-verify + sentinel

### 2. ミッション達成状況
- 必須項目達成表（4HTML + ryoiki-index 更新 + Phase A→B 連続性図 + 図表7点）
- 字数達成（report 30K / analysis 19K / verification 10K / handoff 4K）

### 3. Phase B 統合の主要発見（経営層向け3点）
- 発見1: 95-105問統合マップによる「ミラツクが向き合う問いの全体像」確定
- 発見2: wisdom × シナリオ × ホライズン三軸統合の方法論的姿勢
- 発見3: 真M連鎖（Phase A → B-1 → B-3 → B-5）の継承一貫性

### 4. ryoiki-index.html 更新内容
- Phase B セクション「Wave 進行中」→「全 Wave 完了」
- B-1〜B-6 リンク追加
- Phase A → Phase B 連続性図（ASCII または SVG）

### 5. 既知の限界
- 統合の方法論的主観性
- 5系統 Skill 限定継承
- SVG/Sankey 未実装（Phase C 課題）
- Fragmentation 未踏領域

### 6. Phase C への申し送り事項
- SVG/Sankey 精緻化（B-3 経路図、B-4 装置マトリクス）
- 27未カバー問いの装置評価追加
- ARTS/HISTORICAL/CTI 系統追加検討
- 三系列差の最終整合プロトコル定式化
- Fragmentation 未踏領域への研究投資判断

### 7. 統合用連結ID（_PROTOCOLS.md §6.2 標準フォーマット）
- 主軸DB / 強みホライズン / 強み CTL-1 / 全成果物リスト

合計: **約4,000字**（3,000-5,000 範囲内）

---

## 5. 想定する図表リスト

| ID | タイトル | 形式 | 出力先 | データ源 |
|---|---|---|---|---|
| Fig.1 | Phase A→B 連続性図 | フロー図（ASCII or SVG） | report 1.2 / handoff §1 | Phase A 9 Track + 15メタテーマ + 6 Mサイン → B-1〜B-5 |
| Fig.2 | 5 Wave × 6 Track 依存関係図 | DAG（有向非巡回グラフ） | report 1.3 | _PHASE_B_PLAN.md + 各 Track 依存関係 |
| Fig.3 | 95-105問統合マップ | ベン図 + 数値表 | report 3.1 / analysis 2.4 | B-1 41 + B-3 30 + B-4 24 |
| Fig.4 | B-2 三大クラスター × B-3 5シナリオ 接続表 | クロスマトリクス | report 3.2 / analysis 3.2 | B-2 §6 + B-3 §2.2 |
| Fig.5 | 真M連鎖図（Phase A → B-1 → B-3 → B-5） | サンキー風フロー（ASCII） | report 3.4 | Phase A Mサイン + B-1 §5 + B-3 §3 (5/8 接続) |
| Fig.6 | ミラツク優先 TOP10 統合ランキング表 | 順位表（10行 × 7列） | report 4.2 | B-5 TOP10 + Mサイン + wisdom厚 + シナリオ位置 |
| Fig.7 | zones × 装置 接続図 | バブルチャート風配置 | report 3.3 | B-4 7装置 + B-5 zones |
| Fig.A1 | B-1 41問 三軸分布ヒートマップ | 3D表現を2Dで | analysis 2.1 | B-1 §5 集計 |
| Fig.A2 | wisdom 蓄積期間4層モデル | 横棒グラフ風 | analysis 3.4 | B-2 §10 |

注: SVG 化は Phase C 課題。Phase B B-6 では ASCII 風構造図 + HTML table を採用（B-3 §10 経路図と同方針）。

---

## 6. 数値継承の honest 開示テンプレート

### 6.1 三系列差テンプレート

各主要数値について、3列開示を必須とする：

```
| 指標 | briefing値 | 実装値 | 最終整合値 | 差分理由 |
|---|---|---|---|---|
| B-1 問い数 | 40-50問想定 | 41問 | 41問 | 想定範囲内 |
| B-2 wisdom | 70-210件 | 85件 | 85件 | 範囲下限近傍 |
| B-2 系統カバレッジ | 70セル想定 | 70/70 = 100% | 70/70 | 完全達成 |
| B-3 シナリオ | 5-7想定 | 5シナリオ | 5シナリオ | 設計確定 |
| B-3 critical junctures | 6-10想定 | 8 | 8 | 想定範囲内 |
| B-3 善い社会問い | 30-40想定 | 30問 | 30問 | 範囲下限 |
| B-3 CTL-1配分合計 | 30 | 33 | 33 | 重複帰属3問のため |
| B-3 主体配分 | 旧6カテゴリ | 単独14 + 複合17 | 単独+複合 | 改訂（doc-verify A-10対応） |
| B-4 装置カバレッジ問い | 24想定 | （実装値） | （実装値） | B-4 完了待ち |
| B-5 TOP10 | 10件想定 | （実装値） | （実装値） | B-5 完了待ち |
```

### 6.2 confidence 分布の継承

B-2 wisdom_records 85件の confidence 内訳:
- confidence 5: 42件（49.4%）
- confidence 4: 35件（41.2%）
- confidence 3: 8件（9.4%）
- confidence 1-2: 0件

B-3 5シナリオ wisdom 配分（合計 85件 = B-2 全件）:
- Pluriverse: 18件 / Techno-Acceleration: 13件 / Care-Co-existence: 19件 / Slow Right: 12件 / Fragmentation: 11件 / cross-scenario: 12件

### 6.3 ground truth 同期

最終 source-of-truth は `track-b1-layered-history-report.html`。B-2 DB の msign_origin 同期済（B-2 sentinel verdict M1）。B-3/B-4/B-5 の Mサイン階層参照は、集計値ベースなら影響なし、個別問い参照なら B-1 ground truth を最終確認。

### 6.4 Mサイン階層継承

| 階層 | Phase A | B-1 41問由来 | B-2 14問内訳 |
|---|---|---|---|
| 真M | 1（物語転換期） | 4問 | 1（Q-N04） |
| 準M | 3（世代間正義・非西洋認識論・AI制度反作用） | 14問 | 2（Q-F02・Q-M03） |
| 概念整合 | 1（第四変容期） | 15問 | 8 |
| 単独T | - | 8問 | 3（Q-N12・Q-F06・Q-V01） |

---

## 7. CSS/HTML 規約

### 7.1 必須要素（db-design-system 準拠）

- `:root` カラー変数完全コピー（白基調 #FFFFFF / 赤 #CC1400 / テキスト #121212）
- `[data-theme="dark"]` ダークモード（#121212 bg / #FF4030 赤）
- Google Fonts: `Noto Sans JP` + `Noto Serif JP` ロード
- top-bar: 48px固定 + `border-top: 3px solid #121212` + ブランドロゴ + テーマ切替
- toc-sidebar: 240px 位置固定、章番号付き、ホバー時赤色
- main: max-width 760px、本文中心
- 段落: `text-indent: 1em` (first-of-typeのみ0)
- 行間: 1.85-1.95 / 字間: 0.025em / `font-feature-settings: "palt"`
- 印刷時: サイドバー非表示（`@media print`）
- モバイル（<1000px）: サイドバー上部展開
- favicon: `https://esse-sense.com/favicon.ico`
- テーマ切替JS: `data-theme` 属性切替 + `localStorage` 保存

### 7.2 章番号体系

- `<h1 class="book-title">` Phase B 統合レポート — ミラツクが向き合う問いの全体像
- `<h2 class="chapter-title">` 第I部〜第V部
- `<h3>` 各部の節（1.1, 1.2, ...）
- `<h4>` 必要に応じ小節

### 7.3 figure 埋め込み

```html
<figure class="figure-block">
  <figcaption>Fig.N: タイトル</figcaption>
  <pre class="ascii-figure">...</pre>
  <p class="figure-note">出典: ...</p>
</figure>
```

ASCII図は `<pre>` 内に等幅フォントで配置。SVG化は Phase C 課題として明記。

### 7.4 参照モデル

- 主参照: `track-b1-layered-history-report.html`（Phase B 内一貫性）
- 副参照: `ryoiki-master-report.html`（Phase A 統合）+ `_INTEGRATION_FRAMEWORK.md`（章立て哲学）
- 図版規格: `_FIGURE_STANDARDS.md`

### 7.5 出力ファイル配置

```
~/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-b/
├── track-b6-integration-report.html         (~30,000字, 図表7-9点)
├── track-b6-integration-analysis.html       (~19,000字, DB集計付録)
├── track-b6-integration-verification.html   (~10,000字, 4カテゴリ統合)
└── track-b6_handoff.md                      (~4,000字)

~/projects/apps/miratuku-news-v2/dashboards/ryoiki/
└── ryoiki-index.html                        (Phase B セクション更新)
```

---

## 8. Wave 4 起動チェックリスト

B-6 着手時に以下を確認：

- [ ] B-1 / B-2 / B-3 / B-4 / B-5 全 handoff 到着
- [ ] B-3 sentinel APPROVED
- [ ] B-4 sentinel APPROVED
- [ ] B-5 完了
- [ ] 本書（`_TRACK_B6_STRUCTURE.md`）章立てに沿った流し込み
- [ ] §6 三系列差テンプレートの最終整合値埋め込み
- [ ] Fig.1〜Fig.7 の最終データ確定
- [ ] db-design-system 必須チェック完了
- [ ] doc-verify 4カテゴリ自己検証
- [ ] ryoiki-index.html Phase B セクション更新

---

最終更新: 2026-05-09
作成: Track B-6 構造プロトタイプ設計（Wave 4 起動高速化）
参照: `_TRACK_B6_BRIEFING.md` / `track-b1_handoff.md` / `track-b2_handoff.md` / `track-b3_handoff.md` / `_INTEGRATION_FRAMEWORK.md` / `ryoiki-master-report.html`
