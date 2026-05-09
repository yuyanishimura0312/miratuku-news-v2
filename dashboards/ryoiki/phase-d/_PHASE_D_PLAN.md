# Phase D 展開 1 計画書 — deep-knowledge 書籍との統合

## プロジェクト位置づけ

Phase A → B → C で確立された「ミラツクが描く未来社会への羅針盤」（71 独立問い + 100-150 偉業 + 担い手特性 + 時間軸サイクル）を、**deep-knowledge 書籍 case 11**（『深い知が拓く 2100 年』20 章 280K 字 26 DBs）の物語構造と統合し、**deep knowledge 読者に提示する「現代問うべき問いと背景資料」**を作成する**第四段階**。

deep-knowledge 書籍を **主**、ryoiki-index（Phase A/B/C 統合インデックス）を **従** とし、配布資料・企画決定用コンセプト資料・関係者向け重要資料として機能させる。

## Phase D 構造（4 段階）

```
Phase C 完了
    ↓
D-0: 結合性分析（deep-knowledge × ryoiki の交差点特定）
    ↓
D-1: 問い候補の選定（5-10 問）
    ↓
D-2: 各問いの 4-5 ページ背景解説 HTML 作成（並列）
    ↓
D-3: 統合レビュー + 配布資料化
```

## 4 段階詳細

### D-0: 結合性分析（基盤層）

**目的**: deep-knowledge-book.html（序+18+終 = 20 章 / 第一部「未来を測る」第二部「三つの風景と知性社会」第三部「人類学・哲学・伝統知」第四部「卓越人材と 2100」）と ryoiki-index（Phase A 9 + Phase B 6 + Phase C 7 = 22 トラック）の論理的結合点を分析。

**入力**:
- `https://yuyanishimura0312.github.io/miratuku-news-v2/reports/deep-knowledge-book.html` 全 20 章
- Phase C `phase-c-master-report.html`（C-1 サイクル + C-2 問い + C-3 偉業 + C-5 担い手）
- Phase B B-6 主要発見 5 点 + ミラツク優先 TOP10 + 戦略的空白 13 問
- Phase A `ryoiki-master-report.html` 横断メタテーマ M01-M15

**出力**:
1. `track-d0-linkage-analysis.html`（10K-12K 字、結合点マップ）
2. `track-d0_handoff.md`（D-1 への引継ぎ）

**核心成果**:
- deep-knowledge 20 章 × Phase C 7 トラック 連結マトリクス
- 「物語との結合性」評価（強連結 / 中連結 / 弱連結）
- D-1 で選定すべき問いの候補プール（30-50 問の中から）

**想定人員**: 1 ペア（Lead + Editorial）／3-5 日

---

### D-1: 問い候補の選定（選定層）

**目的**: deep-knowledge 物語との結合性 × Phase C ミラツク優先課題 × 戦略的空白 の三軸で、**5-10 問の核心的問い**を選定。

**入力**:
- D-0 連結マトリクス
- Phase C ミラツク優先 TOP10
- Phase B 戦略的空白 13 問

**出力**:
1. `track-d1-question-selection-report.html`（8K-10K 字、選定理由 + 問いカード 5-10）
2. `track-d1_handoff.md`

**核心成果**:
- 5-10 問の選定（暫定候補）:
  - **D 問い候補例**:
    - DQ-01: 「2100 年に向けたサイクル A 前期 27% 地点で、私たちは何を選ぶか」（C-1 + 第二部「知性社会」結合）
    - DQ-02: 「世代間正義の憲法化（G-M04）はなぜ装置観測されないのか」（戦略的空白 1 位 + 第四部「2100 人材像」結合）
    - DQ-03: 「先住民知識主権（G-N09）と『翻訳しない参照』の倫理」（第三部「伝統知」直結）
    - DQ-04: 「ケア経済の組織化（G-N12 Hot 最強）と GDP 代替指標」（C-3/C-4 偉業 × 第二部結合）
    - DQ-05: 「非西洋認識論の方法論化（G-N07-N08）と『火のまわりの八割』」（第三部 ch15 直結）
    - DQ-06: 「pluriverse cosmology（G-V07）の very-far 実装と神話社会 2100」（第四部結合）
    - DQ-07: 「『場所性回帰』Q-N04 が全 Track 貫通する非対称構造」（B-6 発見 1 結合）
    - DQ-08: 「『第四変容期』概念整合 15 問の規範軸とミラツク独自視点」（B-6 発見 3 結合）
- 各問いの選定根拠（物語結合性 + Phase C 優先度 + ミラツク独自視点の三段論）

**想定人員**: 1 トリオ（Lead + Editorial + Domain Expert）／4-6 日

---

### D-2: 各問いの 4-5 ページ背景解説 HTML 作成（並列展開層）

**目的**: D-1 で選定された 5-10 問それぞれに対し、**4-5 ページ（2,500-4,000 字）の背景解説 HTML** を**並列**で作成。各問いの「**なぜこの問いが重要か / なぜ問うべきか**」が見える資料。

**入力**:
- D-1 選定済 5-10 問
- 各問いの Phase A/B/C 紐付けデータ（B-2 wisdom / B-4 initiatives / C-3 偉業 / C-5 担い手）

**出力（5-10 問×各 4 ファイル）**:
- 各問いごと:
  - `track-d2-question-{NN}-background.html`（4-5 ページ、2.5K-4K 字）
  - 構造: 序文 / 問いの背景 / 既出回答（B-2 wisdom 起点）/ 現在の動き（B-4/B-5 起点）/ 期待される偉業（C-3/C-4 起点）/ 担い手の特性（C-5 起点）/ 参照
- 全問い統合カバー:
  - `track-d2-question-cards-index.html`

**核心成果**:
- 5-10 問それぞれの自立した背景解説 HTML（独立配布可能）
- deep-knowledge 該当章への内部リンク + ryoiki-index への深いリンク
- 各問い末尾に「ミラツクの羅針盤上の位置」を記す位置決め図

**想定人員**: 5-10 並列（1 問 1 Writer）+ 1 Editorial Reviewer ／7-10 日

**並列度**: 各問いは独立して書ける構造のため、最大 5-10 並列実行可。

---

### D-3: 統合レビュー + 配布資料化（統合層）

**目的**: D-2 個別問い解説を**配布資料・企画決定用コンセプト資料・関係者向け重要資料**として統合。

**入力**:
- D-2 全 5-10 問背景解説 HTML
- D-1 選定理由レポート

**出力**:
1. `phase-d-master-report.html`（35K-50K 字、5-10 問統合 + 序文 + 終章 + 付録）
2. `phase-d-distribution-package.html`（配布資料一覧 + ダウンロード導線）
3. `phase-d-index.html`（Phase D 4 段階 + 5-10 問統合インデックス）
4. `ryoiki-index.html` **更新**（Phase D セクション追加）

**核心成果**:
- 配布資料パッケージ（PDF 化可能 HTML / 印刷対応）
- 企画決定用コンセプト資料（経営層・関係者向け）
- deep-knowledge 読者ガイド（書籍を読む人が次に手に取るべき資料）

**想定人員**: 1 ペア（Editorial Lead + HTML Builder）／4-6 日

---

## 依存関係グラフ（Wave 構成）

```
Wave 0: D-0 結合性分析（3-5 日）
  ↓
Wave 1: D-1 問い選定（4-6 日）
  ↓
Wave 2: D-2 各問い背景解説 5-10 並列（7-10 日）
  ↓ 全問い完了後
Wave 3: D-3 統合レビュー + 配布資料化（4-6 日）
  ↓
Phase D 完了 → 次フェーズ（展開 2: 別ターゲット）検討
```

| 段階 | Track | 並列度 | 想定期間 |
|------|-------|--------|----------|
| Wave 0 | D-0 結合性分析 | 1 ペア | 3-5 日 |
| Wave 1 | D-1 問い選定（5-10 問） | 1 トリオ | 4-6 日 |
| Wave 2 | D-2 各問い背景解説（並列） | 5-10 並列 | 7-10 日 |
| Wave 3 | D-3 統合レビュー + 配布資料化 | 1 ペア | 4-6 日 |

**想定総期間**: 約 4-5 週間（最短 18 日、最長 27 日）。Wave 2 の並列度がボトルネック。

---

## 品質ゲート方針

Phase A/B/C と同様の三層:
1. doc-verify（4 カテゴリ独立検証）
2. sentinel（最終ゲート、VETO 権）
3. refinement-coordinator（最大 3 ラウンド）

ただし Phase D は配布資料の性格上、**Editorial Review（読者目線レビュー）** を doc-verify と並走させる。

---

## デザイン規約

deep-knowledge-book.html の体裁を主モデルとする:
- book-cover デザイン（CASE 11 メタタグ + serif title + divider）
- 2 カラム（toc-sidebar 260px + book-main 760px）
- 序文 epigraph + literary-opening + 章番号 label
- 赤白 CI #CC1400 / Noto Serif JP（本文）+ Noto Sans JP（UI）
- 各問い HTML は deep-knowledge と同じ「book」スタイルで統一感を担保

---

## 出力先

すべて: `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-d/`

公開 URL（想定）:
- Phase D master: https://yuyanishimura0312.github.io/miratuku-news-v2/dashboards/ryoiki/phase-d/phase-d-master-report.html
- Phase D index: https://yuyanishimura0312.github.io/miratuku-news-v2/dashboards/ryoiki/phase-d/phase-d-index.html
- 各問い: https://yuyanishimura0312.github.io/miratuku-news-v2/dashboards/ryoiki/phase-d/track-d2-question-NN-background.html

---

## ryoiki-index 更新方針（D-3 担当）

```html
<section class="section">
<h2 class="section-title">Phase D 展開 1: deep-knowledge 統合<span class="status-badge" data-status="completed">完了</span></h2>
<p class="section-lead">deep-knowledge 書籍 case 11『深い知が拓く 2100 年』を主、ryoiki-index を従として、
deep knowledge 読者に提示する「現代問うべき問いと背景資料」を作成。
5-10 問の核心問いそれぞれに 4-5 ページの背景解説。
配布資料・企画決定用コンセプト資料・関係者向け重要資料として機能。</p>

<div class="callout">
<div class="callout-title">PHASE D MASTER</div>
<a href="phase-d/phase-d-master-report.html"><strong>Phase D マスターレポート →</strong></a><br>
5-10 問統合背景解説 + 配布資料パッケージ。
</div>
</section>
```

---

## Phase B/C 教訓継承

- **問いごとの 4-5 ページ単位**: B-2 14 問 × 5 系統 = 70 セルの設計と整合。各問いを独立配布可能な単位として扱う。
- **数値の三系列開示**: Phase A→B WARN-1/2 教訓を継承し、各問いの背景解説でも DB 実値を一次値として採用、ブリーフィング値・公開値との差は注釈開示。
- **honest 開示**: B-3 MJ-02 二系列形式（厳密 4/8 / 概念整合 6/8）を Phase D でも踏襲。
- **deep-knowledge 体裁の踏襲**: book-cover、章番号 label、literary-opening、epigraph 等を Phase D HTML でも継承し、書籍と資料の連続性を担保。

---

## 確認事項（着手前）

1. **本計画で実行可か** / 修正点があるか
2. **D-1 選定問い数**: 5/7/10 問のいずれを目安とするか（暫定候補 8 問例示済）
3. **D-2 並列度**: 5-10 並列の最大数許容範囲
4. **配布形式**: HTML のみ / PDF 化 / Notion 配信 のいずれか優先

ご承認いただけ次第、Wave 0（D-0 結合性分析）から起動します。

---

## 改訂履歴

- 2026-05-09 v1.0: spec-writer 初版作成。Phase C 完了を前提とした 4 段階構造。
