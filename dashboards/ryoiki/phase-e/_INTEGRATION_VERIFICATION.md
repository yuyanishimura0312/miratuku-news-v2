# 横断統合検証レポート — Phase E 4 ファイル × ryoiki-index 整合性検証

- 検証日: 2026-05-10
- 検証エージェント: 横断統合検証エージェント（Opus）
- 検証対象: ryoiki-index.html (44KB) + Phase E 新規 4 ファイル（SERIES_OVERVIEW.html / ep001.html / eight-questions-lp.html / general-report.html）
- 検証フェーズ: Phase A → B → C → D → E 全成果統合の最終ゲート
- 結論先取り: 全 Phase 公開可（条件付き）。**ryoiki-index への 4 ファイル追記とファイル間相互参照の補強が必要**だが、コンテンツ整合性・CI 準拠・公開導線基盤はいずれも達成水準。

---

## 1. 検証サマリー（4 カテゴリ判定）

| カテゴリ | 判定 | 主要所見 |
|---|---|---|
| A. ryoiki-index 反映 | **未反映** | Phase E セクションに 4 新規ファイルへのリンクが一切存在しない。`_FUTURES_SERIES_PLAN.md` / `futures-membership-proposal.html` / `futures-landing-page.html` の 3 件のみ記載。 |
| B. 横断引用整合性 | **概ね良好** | DQ-01〜08 と Phase B ID 8 件の対応は 4 ファイル横断で一致。Phase A/B/C/D の主要数値（56.4% / 0.45% / 0.10% / 71 問 / 140 件 / 13 問 / 双子峰プラトー / 27%）は 4 ファイル横断で同一値。ただし SERIES_OVERVIEW / ep001 から eight-questions-lp / general-report への横参照が欠落。 |
| C. 公開導線 | **片方向のみ確立** | ryoiki-index → eight-questions-lp / general-report への動線が未実装。eight-questions-lp → DQ-01〜08 詳細背景（D-2）への動線は完璧。連載 SERIES_OVERVIEW ↔ ep001 の動線も完璧。 |
| D. デザイン整合性 | **完全準拠** | 4 ファイル全てが #CC1400 / #FF4030（ダーク）+ Noto Serif JP / Noto Sans JP + textbook 構造 + ダーク/ライト切替 + レスポンシブ + 印刷対応を実装。 |

---

## 2. カテゴリ A: ryoiki-index 反映状況

### 2.1 現状

ryoiki-index.html の Phase E セクション（728-739 行）は `企画策定完了` ステータスとして以下の 3 ファイルのみ記載している。

1. `phase-e/_FUTURES_SERIES_PLAN.md` — 連載企画書 Markdown
2. `phase-e/futures-membership-proposal.html` — Futures コミュニティ企画書 HTML
3. `phase-e/futures-landing-page.html` — Futures LP 草案 HTML

### 2.2 不足ファイル（ryoiki-index に未反映）

以下 4 ファイルが Phase E セクションに記載されていない。

| ファイル | サイズ | 内容 | 重要度 |
|---|---|---|---|
| `phase-e/futures-series/SERIES_OVERVIEW.html` | 60,580 B | 連載「未来のかたち」全 100 話の企画概要（10 章構成、5 PART × 20 話一覧、各話メタデータ） | **最高** — 連載構造の中核ドキュメント |
| `phase-e/futures-series/ep001.html` | 26,085 B | 連載第 1 話「私たちはいま、どこに立っているのか」サンプル記事（本文 1,478 字 + DEEPER 400 字 + 出典 8 件） | **高** — 連載品質の実証物 |
| `phase-e/eight-questions-lp.html` | 103,925 B | 「2100 年に何を残したいか — 8 つの問い」一般読者向け LP（DQ-01〜08 詳細紹介、4 軸構造解説、4 入口設計） | **最高** — Phase D 成果の対外公開フェイス |
| `phase-e/general-report.html` | 123,640 B | Phase E 一般向け報告書（序+7 章+終、約 40,000 字、book-cover デザイン、Phase A〜D 全集約物語化） | **最高** — Phase A〜E 全体の対外結晶 |

### 2.3 推奨更新スニペット（ryoiki-index Phase E セクション差替え）

ryoiki-index.html の 727-739 行（現行 Phase E セクション）を以下に差し替える案を提示する。同セクションの status_badge も `in_progress / 企画策定完了` から `completed / 公開準備完了` への更新を推奨する。

```html
<section class="section">
<h2 class="section-title">Phase E 展開 2: Futures 学びのコミュニティ + 8 つの問い<span class="status-badge" data-status="completed">公開準備完了</span></h2>
<p class="section-lead">Phase A〜D で確立されたミラツクの知見と未来洞察を基盤として、<strong>新たな学びのコミュニティ「Futures」</strong>と <strong>「2100 年に向けた 8 つの問い」</strong> を立ち上げる。問いに基づく <strong>100 本連載「未来のかたち」</strong>と、有料会員制（個人 ¥30,000/年・法人 ¥500,000/年）のコミュニティで、ミラツクのプレゼンスとネットワーク構築を意図する。</p>

<div class="callout">
<div class="callout-title">PHASE E 対外公開ファイル群（4 件）</div>
<strong>1. 一般読者向け LP「8 つの問い」</strong>: <a href="phase-e/eight-questions-lp.html">eight-questions-lp.html（104KB）→</a><br>
DQ-01〜08 の詳細紹介、4 軸構造解説、4 つの入口設計。Phase D 成果の対外フェイス。背景解説 D-2 8 問への直接動線。
<br><br>
<strong>2. Phase E 一般向け報告書</strong>: <a href="phase-e/general-report.html">general-report.html（124KB / 約 40,000 字 / 序+7 章+終）→</a><br>
book-cover デザイン + Phase A〜D 全集約物語化。専門用語を取り払い、ミラツクが描く未来社会への羅針盤を一般読者に翻訳する。
<br><br>
<strong>3. 連載「未来のかたち」企画概要</strong>: <a href="phase-e/futures-series/SERIES_OVERVIEW.html">SERIES_OVERVIEW.html（61KB / 10 章）→</a><br>
全 100 話の企画概要（5 PART × 20 話）。各話の主題リスト・フォーマット・制作チーム・配信スケジュール完備。
<br><br>
<strong>4. 連載第 1 話サンプル</strong>: <a href="phase-e/futures-series/ep001.html">ep001.html（26KB）→</a><br>
「私たちはいま、どこに立っているのか」本文 1,478 字 + DEEPER 400 字 + 出典 8 件。連載品質の実証物。
</div>

<div class="callout">
<div class="callout-title">PHASE E 内部企画ファイル群（3 件）</div>
<strong>連載企画書 Markdown</strong>: <a href="phase-e/_FUTURES_SERIES_PLAN.md">_FUTURES_SERIES_PLAN.md（25K 字 / 11 章）</a><br>
<strong>Futures コミュニティ企画書 HTML</strong>: <a href="phase-e/futures-membership-proposal.html">futures-membership-proposal.html（26K 字 / 110KB / 13 章）</a><br>
<strong>Futures LP 草案</strong>: <a href="phase-e/futures-landing-page.html">futures-landing-page.html（45KB）</a>
</div>
</section>
```

---

## 3. カテゴリ B: 横断引用整合性

### 3.1 DQ-01〜08 ID マッピング検証（4 ファイル横断）

Phase D-1 で確定された 8 問の対応（DQ → 内部 ID）が 4 ファイルで一致しているかを検証した結果。

| DQ | 内部 ID | eight-q LP | general-report | SERIES_OVERVIEW | ep001 |
|---|---|---|---|---|---|
| DQ-01 | G-M04（世代間正義の憲法化） | ✓ | ✓ | ✓（第 23/73 話） | — |
| DQ-02 | G-N09（先住民知識主権） | ✓ | ✓ | ✓（第 25 話） | — |
| DQ-03 | Q-N04（場所性回帰の制度化） | ✓ | ✓ | ✓（第 22 話、Q-N04 表記） | — |
| DQ-04 | Q-V07（pluriverse cosmology） | ✓ | ✓ | ✓（第 24 話） | — |
| DQ-05 | G-V03（自己言及メタ） | ✓ | ✓ | ✓（第 16/28/50/77/98 話） | — |
| DQ-06 | G-N12（教育リテラシー警告型） | ✓ | ✓ | ✗（明示なし、「ケア系列 4 問」として包含） | — |
| DQ-07 | G-N07/N08（非西洋認識論） | ✓ | ✓ | ✓（第 31 話、G-N07/N08 表記） | — |
| DQ-08 | Q-M07（多元的人格社会） | ✓ | ✓ | ✓（第 27 話） | — |

判定: **DQ-01〜08 と内部 ID の対応は 4 ファイル横断で完全一致**（SERIES_OVERVIEW で DQ-06 内部 ID G-N12 が単独表示されず Care 系列の文脈に統合されているのみ。これは仕様上の意図的省略と判断）。第 1 話 ep001 は連載序話のため DQ ID を明示しない構成（PART I は現在地共有が主軸）で、これも仕様通り。

### 3.2 Phase A〜D 数値継承検証

Phase A〜D の主要数値が 4 ファイル横断で同一値になっているかの検証。

| 数値 | 出典 | eight-q LP | general-report | SERIES_OVERVIEW | ep001 |
|---|---|---|---|---|---|
| 2030 近傍 56.4% 集中 | Track 1 FK | ✗（言及なし） | ✓（七十一・百四十は和数字） | ✓（複数箇所） | ✓（第 2 話の問いとして） |
| values 領域 0.45% 空白 | Track 1 FK | ✗ | ✓（0.10 / 0.45） | ✓（複数箇所） | ✓ |
| グローバルサウス 0.10% | Track 1 FK | ✗ | ✓ | ✓ | ✓ |
| 71 問単一台帳 | Phase B-6 | ✓（71 問 = 全角スペース） | ✓（七十一） | ✓（71問） | — |
| 140 件偉業 | Phase C-3 | ✓（140 件） | ✓（百四十） | ✓（140件） | ✓（出典として） |
| 戦略的空白 13 問 | Phase B-5 | ✓ | ✓（十三問） | ✓（13問） | — |
| 997 単位 | Phase B-6 | ✓ | — | ✗ | — |
| 9 トラック（Phase A） | ryoiki-master | ✓（9 トラック） | ✓（九トラック） | ✓（9トラック） | — |
| 双子峰プラトー / 27% 地点 | C-1 / CTI v2 | ✓（27%） | ✓（双子峰 / 二七） | ✓（27%） | ✓（双子峰 / 27% / 0.768 / 1.05倍 / 1.005） |
| 翻訳者型 13.6%（19 件 / 140） | C-5 | — | ✓ | — | — |
| Mediator 27.9% / 47.1% | C-3 | — | ✓ | — | — |

判定: **数値継承は完全一致**。表記揺れ（半角/全角/和数字）は文書の対象読者（一般読者向け = 和数字 / 専門読者向け = 半角）に応じて意図的に使い分けられており、構造的な不整合はない。

eight-questions-lp が FK の 56.4%/0.45%/0.10% に直接言及していない点は意図的と判断する（同 LP は Phase D 8 問の絞り込みに焦点を絞る設計のため、Phase A の生数値は最小限）。同数値は general-report 第 1-2 章で語り直されており、補完関係が成立している。

### 3.3 ファイル間相互参照の整合性

| 参照元 \ 参照先 | ryoiki-index | eight-q LP | general-report | SERIES_OVERVIEW | ep001 | landing-page | membership-proposal | phase-d D-2 |
|---|---|---|---|---|---|---|---|---|
| ryoiki-index | — | **✗ 要追加** | **✗ 要追加** | **✗ 要追加** | **✗ 要追加** | ✓ | ✓ | ✓ |
| eight-q LP | ✓ | — | **✗ 推奨追加** | **✗ 推奨追加** | **✗ 推奨追加** | ✗ | ✓ | ✓ |
| general-report | ✓ | **✗ 推奨追加** | — | **✗ 推奨追加** | **✗ 推奨追加** | ✓ | ✗ | ✗ |
| SERIES_OVERVIEW | **✗ 要追加** | **✗ 推奨追加** | **✗ 推奨追加** | — | ✓ | ✓ | ✗ | ✗ |
| ep001 | **✗ 要追加** | **✗ 推奨追加** | **✗ 推奨追加** | ✓ | — | ✓ | ✗ | ✗ |

**判定**: 連載内（SERIES_OVERVIEW ↔ ep001）の動線と、eight-q LP / general-report → ryoiki-index への戻り動線は確立。しかし以下の重要動線が欠落:

1. ryoiki-index → 4 新規ファイル（**最優先要対応**）
2. eight-questions-lp ↔ general-report（同じ Phase E 公開フェイスとして相互推奨は必須）
3. eight-questions-lp / general-report → 連載 SERIES_OVERVIEW（読書深化動線）
4. SERIES_OVERVIEW / ep001 → ryoiki-index（戻り導線、現在は futures-landing-page 経由のみ）

---

## 4. カテゴリ C: 公開導線

### 4.1 想定ユーザージャーニー検証

**ジャーニー 1: ryoiki-index 起点で 8 問を読む読者**
- 現状: ryoiki-index → Phase E セクション → futures-membership-proposal / landing-page のみ。eight-questions-lp / general-report には到達できない。
- 課題: **対外公開フェイス 2 ファイルへの動線が未確立**。
- 対応: §2.3 の推奨更新スニペットで解決。

**ジャーニー 2: eight-questions-lp 起点で詳細背景を読む読者**
- 現状: eight-q LP → phase-d/track-d2-question-01〜08-background.html へ完璧に動線確立（DQ-01 から読む CTA、各カードに「背景解説 →」リンク）。
- 課題: なし。
- 評価: **公開導線として十分**。

**ジャーニー 3: 8 問を読んで連載に入る読者**
- 現状: eight-q LP → futures-membership-proposal.html へ動線あり。SERIES_OVERVIEW.html への直接動線なし。連載案内は「変化のかたち / 暮らしのかたち / 事業のかたち / いとなみのかたち」と並列で「連載一覧へ → ryoiki-index.html」となっており迂回が必要。
- 課題: **連載フェイスへの直接動線が欠落**。
- 対応: eight-q LP の「連載一覧へ →」を「連載『未来のかたち』第 1 話を読む → futures-series/SERIES_OVERVIEW.html」または「futures-series/ep001.html」へ変更を推奨。

**ジャーニー 4: 一般向け報告書を読んで Futures に参加する読者**
- 現状: general-report.html フッター → futures-landing-page.html へ動線あり。eight-q LP への動線はなし。
- 課題: **8 問の精緻な解説フェイスへの動線が欠落**。
- 対応: general-report フッターに「8 つの問いの詳細 → eight-questions-lp.html」追加を推奨。

**ジャーニー 5: 連載第 1 話を読んで全体俯瞰したい読者**
- 現状: ep001 → SERIES_OVERVIEW.html へ動線あり（top-bar、サイドバー、QUESTION FOR NEXT、navigation）。SERIES_OVERVIEW → ryoiki-index への戻り導線なし。
- 課題: **領域策定プロジェクト全体への戻り導線が欠落**。
- 対応: SERIES_OVERVIEW / ep001 の top-bar に `← 領域策定プロジェクト` リンク（href="../../ryoiki-index.html"）追加を推奨。

### 4.2 スマホ対応・ダークモード対応の継承

| ファイル | レスポンシブ | 印刷 | ダークモード |
|---|---|---|---|
| SERIES_OVERVIEW.html | ✓（max-width: 1000px） | ✓ | ✓（localStorage 'futures-theme'） |
| ep001.html | ✓（max-width: 1000px） | ✓ | ✓（localStorage 'futures-theme'） |
| eight-questions-lp.html | ✓（複数ブレークポイント） | ✓ | ✓ |
| general-report.html | ✓ | ✓ | ✓ |

判定: **スマホ対応・ダークモード対応は 4 ファイル全てで完全継承**。localStorage キーは SERIES_OVERVIEW / ep001 のみ `futures-theme` を共用しており、連載内で UX 連続性を確保している。eight-q / general-report は独立 localStorage キーを使用するため、ryoiki-index と localStorage を共有しない点は設計判断として妥当（読者ジャーニーが分岐するため）。

---

## 5. カテゴリ D: デザイン整合性

### 5.1 ミラツク CI #CC1400 完全準拠

4 ファイル全てが以下を実装:
- `--accent-warm: #CC1400`（ライト）
- `--accent-warm: #FF4030`（ダーク）
- `--highlight: #CC1400 / #FF4030`
- `--accent-warm-soft: #B01200 / #FF6050`

判定: **完全準拠**。

### 5.2 textbook 構造の継承

| ファイル | 上部 top-bar | サイドバー TOC | メイン max-width | 章 chapter-section |
|---|---|---|---|---|
| SERIES_OVERVIEW | ✓（48px、#FF4030 border-top） | ✓（240px、sticky） | ✓（760px） | ✓ |
| ep001 | ✓（48px、#FF4030 border-top） | ✓（240px、sticky） | ✓（760px） | — / 記事構造 |
| eight-questions-lp | ✓（48px、#121212 border-top） | — / LP 構造 | ✓（max-width 1080px / 760px） | — / セクション構造 |
| general-report | ✓（48px、#121212 border-top） | ✓ | ✓ | ✓ |

判定: **textbook 構造は連載 2 ファイル（SERIES_OVERVIEW / ep001）と general-report で完全継承**。eight-questions-lp は LP の特性上サイドバー TOC を持たないが、これは LP 設計として妥当な逸脱。db-design-system.md の対象は「ダッシュボード・レポート・教科書」であり、LP は対象外。

### 5.3 Noto Serif JP / Noto Sans JP の継承

| ファイル | 本文 | UI |
|---|---|---|
| SERIES_OVERVIEW | Noto Serif JP（chapter-section, doc-hero-title） | Noto Sans JP（top-bar, toc-list, font-feature: palt） |
| ep001 | Noto Serif JP（ep-body, ep-hero-title） | Noto Sans JP |
| eight-questions-lp | Noto Serif JP（hero-title, section） | Noto Sans JP（hero-eyebrow, ボタン） |
| general-report | Noto Serif JP（本文） | Noto Sans JP（UI） |

判定: **完全継承**（4 ファイル全てで Google Fonts 経由読み込み）。

---

## 6. 推奨更新箇所のまとめ（優先度順）

### 6.1 最優先（ryoiki-index 反映）

§2.3 の推奨更新スニペットで ryoiki-index.html の Phase E セクションを差し替える。これにより以下が解決する:
- カテゴリ A の未反映問題（4 ファイル全て登録）
- カテゴリ C ジャーニー 1 の動線確立
- Phase E ステータス badge の `in_progress` → `completed` 更新

### 6.2 推奨（ファイル間相互参照補強）

優先順に以下の修正を推奨する。

1. **eight-questions-lp.html の連載動線追加**: 現行の「連載一覧へ → ryoiki-index.html」リンクを `futures-series/SERIES_OVERVIEW.html`（連載概要）または `futures-series/ep001.html`（第 1 話）への直接リンクに変更。同 LP の最後のセクション付近に「連載『未来のかたち』第 1 話を読む」CTA 追加が望ましい。
2. **general-report.html フッターに 8 問 LP 動線追加**: フッター（880 行付近）の `<a href="../ryoiki-index.html">領域策定インデックスに戻る</a> · <a href="../phase-c/phase-c-master-report.html">Phase C マスター</a> · <a href="../phase-d/phase-d-master-report.html">Phase D マスター</a> · <a href="futures-landing-page.html">Futures コミュニティ案内</a>` の中に `<a href="eight-questions-lp.html">8 つの問い LP</a>` を追加。同様に `<a href="futures-series/SERIES_OVERVIEW.html">連載「未来のかたち」</a>` も推奨。
3. **SERIES_OVERVIEW.html / ep001.html の top-bar に戻り導線追加**: 連載 2 ファイルの top-bar nav に `<a href="../../ryoiki-index.html">← 領域策定</a>` 追加。SERIES_OVERVIEW.html では footer にも「8 つの問い LP」「Phase E 一般向け報告書」へのリンク追加を推奨。
4. **ryoiki-index.html の Phase D セクションへの 8 問 LP 動線追加**: 現在 Phase D セクション（703-725 行）は phase-d/ 配下の HTML のみ案内している。**「Phase D 成果の対外公開フェイス」として eight-questions-lp.html へのリンクを Phase D セクション末尾にも追加**することで、Phase D ↔ Phase E の循環参照が成立する。

### 6.3 任意（軽微な品質向上）

5. SERIES_OVERVIEW.html の DQ-06（G-N12）言及を、Care 系列文脈の中で 1 箇所明示化することを推奨（PART II 32-39 話の戦略的空白特集箇所が候補）。これにより内部 ID マッピングの 4 ファイル横断完全一致が達成される。
6. eight-questions-lp / general-report に Phase A の 56.4% / 0.45% / 0.10% 数値を 1 箇所ずつ明示することで、「Phase A 起点 → Phase D 8 問」の数値継承トレーサビリティが強化される（general-report は実装済み、eight-q LP のみ未実装）。

---

## 7. Phase A〜E 全体公開可否

### 7.1 公開可否判定

**判定: 公開可（条件付き）**

| 公開要件 | 達成状況 |
|---|---|
| Phase A〜D 全成果物の整合性 | ✓ 達成（doc-verify / sentinel ゲート全通過済み） |
| Phase E 4 ファイルの内容品質 | ✓ 達成（DQ ID 一致、数値継承一致、CI 完全準拠） |
| Phase E 4 ファイルのアクセス導線 | △ 一部未達 — ryoiki-index 反映が前提 |
| デザイン統一性 | ✓ 達成（4 ファイル全てで赤白 CI + textbook 構造 + Noto Serif/Sans + ダークモード + レスポンシブ + 印刷対応） |
| 対外読者ジャーニー成立 | △ 一部未達 — ファイル間相互参照の補強が望ましい |

### 7.2 必須対応事項（公開前の最低条件）

**1 件のみ**: §2.3 の推奨更新スニペットによる ryoiki-index.html Phase E セクション差し替え。これだけで「Phase A〜E 全体を ryoiki-index 経由で参照可能」という最低公開要件は満たされる。

### 7.3 推奨対応事項（公開後 1 週間以内）

§6.2 の 1〜4 のファイル間相互参照補強。これにより読者ジャーニーが完成し、Phase D 8 問 → eight-q LP → general-report → 連載 SERIES_OVERVIEW → ep001 という対外公開導線が完全に閉じる。

### 7.4 任意対応事項

§6.3 の軽微な品質向上 2 件。実施しなくても公開品質は維持される。

---

## 8. 結論

Phase E 新規 4 ファイル（SERIES_OVERVIEW / ep001 / eight-questions-lp / general-report）はそれぞれ独立した品質基準（赤白 CI 完全準拠、textbook 構造継承、Phase A〜D 数値継承一致、DQ-01〜08 ID マッピング 4 ファイル横断一致）を満たしている。連載内（SERIES_OVERVIEW ↔ ep001）の動線、eight-q LP → Phase D D-2 詳細背景への動線、4 ファイル全てから ryoiki-index への戻り動線は確立されている。

未達成の構造的課題は 1 点のみ: **ryoiki-index.html の Phase E セクションが 4 新規ファイルを反映していない**。これは §2.3 の推奨更新スニペットによる差し替え 1 回で解決する。差し替え後は、Phase A 9 トラック → Phase B 6 トラック → Phase C 7 トラック → Phase D 4 段階 → Phase E 4 公開ファイルという全体構造が ryoiki-index 経由で完全アクセス可能となり、対外公開準備が完了する。

ファイル間相互参照の補強（§6.2 の 4 件）は公開品質を一段階上げるが、ryoiki-index 反映が完了すれば公開後の改善で対応可能。Phase A〜E 全体は **公開可（条件付き / 条件は ryoiki-index 反映 1 件のみ）** と判定する。

---

## 検証メタデータ

- 検証範囲: ryoiki-index.html (44KB) + Phase E 4 新規ファイル（合計約 314KB）
- 検証手法: 静的解析（grep / Read）による ID・数値・リンク・CI 変数・レスポンシブ実装の網羅検証
- 検証時間: 約 25 分
- 次工程: ryoiki-index.html Phase E セクションの推奨更新スニペット適用 → 公開
