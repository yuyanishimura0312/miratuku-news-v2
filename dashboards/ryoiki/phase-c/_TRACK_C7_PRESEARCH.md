# Phase C-7 事前リサーチ — Phase C HTML 成果物公開と ryoiki-index 更新

> 作成日: 2026-05-09
> 作成: Track C-7 起動準備（Phase C 全 Track 事前リサーチ群と整合）
> 目的: C-1〜C-6 までの全成果を 5 公開 HTML（master-{analysis,verification,report}.html + phase-c-index.html + ryoiki-index.html 更新）として公開する設計枠組みを、リード本体実行前に確定する
> 入力: _TRACK_C7_BRIEFING.md / _PHASE_C_PLAN.md（特に「ryoiki-index 更新方針」セクション）/ 既存 ryoiki-index.html 全文 / phase-b/track-b6-integration-report.html（最重要モデル）/ db-design-system.md（赤白 CI 規定）/ phase-b/phase-b-index.html（B-6 完了後の最新インデックス）
> 推測タグ: 【推定】= 設計判断として演繹した解釈、【解釈】= 複数の妥当な選択肢が成立する読み方、【未検証】= リード本体段階で実 DB と照合する必要がある記述

---

## 序: Track C-7 の独自位置

Track C-7 は Phase C 7 トラックの最終トラックであり、C-1〜C-6 までの全成果を「ミラツク外部に公開する顔」として最終整形する役割を担う。前 6 トラックが内部成果物（DB 構築・分析・検証）を主眼とするのに対し、C-7 のみが「公開層」として位置づけられ、URL（https://yuyanishimura0312.github.io/miratuku-news-v2/dashboards/ryoiki/phase-c/phase-c-master-report.html）からのアクセスがあらゆる外部読者の Phase C 接触点となる。それゆえ C-7 の品質は「Phase C 全体の品質に等しい」ものとして取り扱う必要があり、本事前リサーチでは特に以下 3 軸を厳しく規定する。

第一軸は **textbook 構造の精度**である。phase-b/track-b6-integration-report.html（78KB）は db-design-system.md 規定の最高品質モデルであり、本 C-7 では同等以上の構造的精度を達成する必要がある。第二軸は **赤白 CI #CC1400 デザインシステムの完全適用**である。色変数・タイポグラフィ・レイアウト原則・必須要素・NG 事項のチェックリストを公開前に完全クリアする。第三軸は **タグバランス検証の完全均衡**である。B-6 で達成した analysis 17/17 + verification 36/36 + report 35/35 の `<div>`/`<section>`/`<table>` 完全均衡を Phase C 5 公開 HTML で再現する。

C-7 リード本体は本事前リサーチを参照しながら、(1) ryoiki-index.html の Phase C セクション追加（破壊的変更なし、追加 only）、(2) phase-c-index.html の新規作成（7 トラック導線）、(3) master-{analysis,verification,report}.html の新規作成（C-1〜C-6 統合）、の 3 系統 5 ファイルを順次完成させる。

---

## 1. ryoiki-index.html 現状解析（Phase A + Phase B セクションの構造）

### 1.1 既存ファイル全体構造

ryoiki-index.html（663 行 / 約 23 KB）は領域策定プロジェクトの全体顔として機能している。本ファイルの構造を C-7 で破壊しない方針で精査する。

ファイルは大きく 6 つの構造ブロックから構成される。第一ブロックは `<head>`（line 3-376）で、CSS 全体を内包する。`:root`/`[data-theme="dark"]` のカラー変数（赤白 CI 完全準拠）、`.top-bar`/`.container`/`.page-header`/`.section`/`.tracks`/`.track-card`/`.callout`/`.framework-grid`/`footer` の主要スタイルが定義される。第二ブロックは `.top-bar`（line 378-384）で、ブランド（MIRATUKU NEWS / 領域策定プロジェクト）+ Databases リンク + テーマ切替ボタン。第三ブロックは `.page-header`（line 388-399）で、PROJECT 全体の説明と meta（9 トラック・4 ホライズン・6 CTL・赤白 CI）。第四ブロックは「プロジェクト構造」セクション（line 401-437）で、framework-grid（HORIZON 4 / CTL MEGA-DOMAIN 6 / EVALUATION W·C·M / QUALITY GATES 3）+ METHODOLOGY DOCUMENTS callout。第五ブロックは「9 トラック」セクション（line 439-572）で、9 個の `.track-card`（Track 01-09 各完了）が grid 表示される。第六ブロックは「統合成果（Track 10）」セクション（line 574-590）で、ryoiki-master-report.html へのリンク + Track 10 出力一覧。

そして本 C-7 で **特に重要なのが Phase B セクション**（line 592-642）である。これは Track 10 セクションの直後・footer の直前に挿入された構造で、「Phase B 統合的解析（全完了）」のセクションタイトル + section-lead + 3 つの callout（PHASE B 全完了 / PHASE B INDEX / PHASE B 主要発見 5 点 / ミラツク優先課題 TOP10）から構成される。Phase C セクション追加は、この **Phase B セクションの直後に挿入する** という構造判断が _PHASE_C_PLAN.md の「ryoiki-index 更新方針」でも前提とされている。

### 1.2 Phase B セクションの内部構造（C-7 のテンプレートとなる構造）

Phase B セクション（line 592-642）の内部構造を要素レベルで分解する。これは C-7 で追加する Phase C セクションのテンプレートとなる。

- `<section class="section">`: 親セクション
- `<h2 class="section-title">`: 「Phase B 統合的解析」+ `.status-badge[data-status="completed"]`「全完了」
- `<p class="section-lead">`: 約 200 字のリード文（Phase A → Phase B の流れ + 6 トラック構成 + B-1〜B-6 全 APPROVED）
- `<div class="callout">` × 4 連続:
  1. PHASE B 全完了 — 統合レポート（B-6 統合 3 リンク + handoff リンク）
  2. PHASE B INDEX（phase-b-index.html リンク + B-1〜B-6 各完成成果の詳細）
  3. PHASE B 主要発見 5 点（5 項目の番号付き列挙）
  4. ミラツク優先課題 TOP10（左上 4 + 右上 4 + メタ独自 1 + 中央 1）
- `</section>`: セクション閉じ

構造的に観察すべきは、各 callout の冒頭に `<div class="callout-title">` で「PHASE B 全完了 — 統合レポート」等のラベルを付与している点、リンク本体を `<strong>...</strong>` で太字化している点、複数リンクを `／` 区切りで列挙している点である。Phase C セクションでも同じ装飾パターンを踏襲することで、視覚的一貫性が確保される。【推定】

### 1.3 既存 CSS クラスの再利用範囲

C-7 では Phase C セクション追加に新規 CSS クラスを追加しない方針が望ましい【推定】。理由は、(1) ryoiki-index.html の `<style>` ブロックは line 11-375 と既に 365 行に達しており、追加でルール変更すると影響範囲が拡大する、(2) 既存の `.section`/`.section-title`/`.section-lead`/`.callout`/`.callout-title`/`.status-badge` で Phase C セクションは完全に表現可能、(3) 新規クラス追加は Phase D セクション以降との整合を崩すリスクを生む、の 3 点による。

ただし、もし Phase C 独自の視覚的識別要素を導入する必要が生じた場合は、`.callout--phase-c` のような BEM 修飾子記法で既存 `.callout` を派生させる設計が望ましい。【解釈】 リード本体実行時に「Phase C セクションも視覚的に Phase B と区別したい」という要求が出た場合のみ採用する。

### 1.4 既存ファイルの品質チェック観点

破壊的変更を避けるため、C-7 リード本体実行時には以下を前提として作業する必要がある。

- ryoiki-index.html は既に Phase B 全完了状態の最終整合版として動作中であり、本ファイルへの編集は **Phase C セクションの新規挿入のみ**に限定する。
- 既存 line 1-642 の編集は禁止（line 642 の `</section>` 閉じタグ直後に Phase C セクションを挿入し、line 644-647 の footer はそのまま継承）。
- 編集後の検証は (1) HTML タグバランス（特に Phase C セクションが完全に閉じているか）、(2) 既存 Phase B セクションのリンクが全て生きているか、(3) Track 1-9 カードの表示が崩れていないか、の 3 系統で行う。

---

## 2. Phase C セクション追加の HTML テンプレート設計

### 2.1 _PHASE_C_PLAN.md の HTML スニペットの精査

_PHASE_C_PLAN.md（line 303-330）に「ryoiki-index 更新方針」として既に HTML スニペットが提供されている。本スニペットを起点として、リード本体実行時の追加要素を予め設計する。

提供スニペットは Phase B セクションと同じ構造（`<section class="section">` + `<h2 class="section-title">` + `<p class="section-lead">` + `<div class="callout">` × 2）で構成される。callout 1 は「PHASE C 全完了 — 統合レポート」、callout 2 は「PHASE C INDEX」となっている。

ただし、Phase B セクションは callout を 4 つ用意している（統合レポート / INDEX / 主要発見 5 点 / 優先課題 TOP10）のに対し、提供スニペットは 2 つに留まる。C-7 リード本体では、Phase B 同様に **Phase C 主要発見 + Phase C 優先 5-10 問候補プールも追加 callout として組み込む**設計が望ましい。【推定】 これは Phase B の「主要発見 5 点」「優先課題 TOP10」と並ぶ Phase C 独自の知的成果（C-3 great_actions.db 100-150 件 / C-4 zone マッピング / C-5 担い手特性類型 / C-6 四位一体マスター図）を読者にも提示するためである。

### 2.2 Phase C セクション完成形の構造案

C-7 リード本体で組み込む Phase C セクション完成形の構造案を以下に示す。これは _PHASE_C_PLAN.md の提供スニペットを「Phase B との視覚的均衡」を保つ方向で発展させた案である。

```
<section class="section">
  <h2 class="section-title">Phase C 収束<span class="status-badge" data-status="completed">全完了</span></h2>
  <p class="section-lead">[Phase A → B → C の流れ + 7 トラック構成 + 4 軸統合（時間軸 × 問い × 偉業 × 担い手）]</p>

  <div class="callout">  <!-- callout 1: 統合レポート -->
    <div class="callout-title">PHASE C 全完了 — 統合レポート</div>
    [phase-c-master-report.html リンク + analysis/verification リンク]
  </div>

  <div class="callout">  <!-- callout 2: INDEX -->
    <div class="callout-title">PHASE C INDEX</div>
    [phase-c-index.html リンク + C-1〜C-7 各完成成果リンク列挙]
  </div>

  <div class="callout">  <!-- callout 3: 主要発見 -->
    <div class="callout-title">PHASE C 主要発見</div>
    [C-1 サイクル / C-2 問い統合 / C-3 偉業構造化 / C-4 zone マッピング / C-5 担い手特性 / C-6 四位一体]
  </div>

  <div class="callout">  <!-- callout 4: Phase D 起動準備 -->
    <div class="callout-title">PHASE D 起動準備（展開 1: deep-knowledge 統合）</div>
    [Phase D placeholder + great_actions.db ダウンロード導線]
  </div>
</section>
```

callout 4 を「Phase D 起動準備」とすることで、Phase B セクションが「TOP10 優先課題」で終わったのに対し、Phase C セクションは「次フェーズへの接続」で締めるという構造的差別化が生まれる。これは Phase C が Phase D（deep-knowledge 統合）への入力データを確定する役割を担うことの視覚的表現である。【推定】

### 2.3 各 callout の詳細記述案

**callout 1（統合レポート）の記述案**:
リンク本体は `phase-c/phase-c-master-report.html`（35K-45K 字）。Phase B との対称性を保ち、analysis（25K-30K 字）と verification（12K-15K 字）も並列リンクで提示する。Phase B の callout 1 と同じく「サブタイトル → 主リンク（太字）→ 説明文 → 補助リンク」の 4 要素構造とする。

**callout 2（INDEX）の記述案**:
リンク本体は `phase-c/phase-c-index.html`。Phase B INDEX callout は B-1〜B-6 各 3 リンク（report/analysis/verification）をすべて列挙して 5 段落構造をとっているが、Phase C は 7 トラックで段落数が増える。簡潔化のため「7 トラック構成: C-1（時間軸）/ C-2（問い）/ C-3（偉業 DB）/ C-4（zone マッピング）/ C-5（担い手）/ C-6（統合）/ C-7（公開）」の一行サマリと、phase-c-index.html への詳細誘導の 2 段構成にする。【推定】

**callout 3（主要発見）の記述案**:
Phase C 全体の「主要発見」を 5 点程度にまとめる。Phase B の主要発見 5 点（真M由来の非対称構造 / 戦略的空白 13 問 / 第四変容期貫通 / 三類型構造 / Mサイン強接続⇔装置応答薄）は B-6 統合段階で確定された結論であった。Phase C の主要発見はリード本体実行時に C-1〜C-6 の成果から抽出するが、現時点で予想される候補は以下である【推定】:
1. サイクル A 前期 27% 地点としての 2100 年位置づけ（C-1）
2. 71 問統合インデックスと「今問うべき問い」の Phase C 観点再ランキング（C-2）
3. great_actions.db 100-150 件で構造化された 10 アーキタイプ × 5 シナリオ × 4 ホライズンマッピング（C-3/C-4）
4. 戦略的空白 13 問それぞれに対応する「期待される偉業」候補（C-4）
5. 担い手の 4 軸特性（心理 19 次元 × 行動 10 アーキタイプ × 領域 CTL-1 × 専門性）（C-5）

**callout 4（Phase D 起動準備）の記述案**:
Phase D（deep-knowledge 統合）への接続ポイントを示す。great_actions.db のダウンロード導線、Phase D D-0 起動条件達成の宣言、5-10 問候補プール（Phase C で確定）への誘導を含める。

---

## 3. 5 公開 HTML ファイル設計

### 3.1 phase-c-master-report.html（35K-45K 字）— 主役 HTML

本ファイルは Phase C 全体の「公開顔」であり、外部読者が最初にアクセスする HTML である。phase-b/track-b6-integration-report.html（B-6 統合レポート、78KB）が直接の参考モデルとなる。【BRIEFING 必読 #4】

#### 3.1.1 章立て構成（_TRACK_C7_BRIEFING.md §必須要素準拠）

BRIEFING の必須要素 1-10 を踏まえた章立て構成案。

- **序章: Phase A → B → C 全体の流れ**（2K-3K 字）
  - Phase A の 9 トラック構造的成果（15 メタテーマ・Mサイン階層・9×9 連結マトリクス・独自知見 7 件）の継承
  - Phase B の 71 問 + 926 派生 = 997 単位の継承
  - Phase C の独自貢献（時間軸 × 問い × 偉業 × 担い手の 4 軸統合）の宣言

- **章 1: C-1 サイクル/螺旋（時間軸層）抜粋**（4K-5K 字、図表 1-2 点）
  - サイクル A（認知転換 280-310 年）/ B（制度興亡 150-300 年）/ C（プラトー 250 年）の入れ子構造
  - CTI v2「双子峰プラトー」発見の含意（産業革命以降 250 年高位プラトー、AI 革命/産業革命 = 1.05 倍）
  - 2030/2050/2070/2100 への投影（near 真M由来 23.1% 等の B-1 数値継承）
  - 螺旋構造仮説（物語転換期 + 第四変容期の 4 ホライズン再投影）

- **章 2: C-2 問い統合（問い層）抜粋**（4K-5K 字、図表 1-2 点）
  - 71 問統合インデックス（B-1 41 + B-3 30）の単一台帳化
  - 「善い社会」歴史的捉え方系譜（5 系統 traditions × 古代-現代）
  - 「今問うべき問い」核心リスト（Phase C 観点の再ランキング）
  - メタ問い × 規範問い × 実装問い × 装置問いの 4 層統合構造図

- **章 3: C-3 偉業構造化（行為層）抜粋 + great_actions.db サマリ**（5K-6K 字、図表 2-3 点）
  - 偉業の 10 アーキタイプ（GF 由来）× 5 シナリオ × 4 ホライズンマッピング
  - 戦略的空白 13 問それぞれに対応する「期待される偉業」候補
  - great_actions.db スキーマ（actions テーブル + 関連テーブル）+ 件数（過去偉業 50-70 + 現代登場中 30-50 + 期待 30 = 100-150 件）
  - great-figures 過去事例 → 現代偉業 → 未来偉業の系譜接続図

- **章 4: C-4 zone マッピング抜粋 + warning/opportunity 偉業**（4K-5K 字、図表 2-3 点）
  - 既存偉業（463 initiatives 起源 = 推進中）vs 期待偉業（戦略的空白 13 問起源）の差分構造
  - ミラツク優先課題 TOP10 × 偉業マッピング
  - warning 偉業（動きはあるが方向違い）/ opportunity 偉業（動きはないが期待される）の弁別
  - great_actions.db 推進状況・成熟度フィールド付与版

- **章 5: C-5 担い手特性抜粋 + ミラツク見出すべき人物像**（4K-5K 字、図表 1-2 点）
  - 100-150 偉業 × 担い手特性マトリクス
  - 4 軸構造化（心理 19 次元 × 行動 10 アーキタイプ × 領域 CTL-1 6 軸 × 専門性）
  - ミラツク優先課題 TOP10 × 担い手類型 = ミラツク見出すべき/育てるべき人物像
  - 担い手特性の時代変化（産業革命期 → 現代 → 2030/50/70/2100）

- **章 6: C-6 四位一体マスター図 + 統合ナレッジマップ**（6K-8K 字、図表 2-3 点、見開き相当の図表 1 点）
  - C-1 サイクル × C-2 問い × C-3 偉業 × C-5 担い手の四位一体マスター図【見開き相当】
  - Phase B 71 + Phase C 偉業 100-150 + 担い手特性 = 統合ナレッジマップ【見開き相当】
  - doc-verify 4 カテゴリ通過 + sentinel APPROVED の根拠開示
  - Phase D（deep-knowledge 統合）への入力データ確定

- **終章: Phase D 起動への接続 + 5-10 問候補プール**（3K-4K 字）
  - Phase D D-0 起動条件達成の宣言
  - deep-knowledge 20 章 × Phase C 7 トラックの連結マトリクス候補
  - 5-10 問候補プールの提示

- **付録**（2K-3K 字、表 1-2 点）
  - Phase A 構造的限界 5 点の Phase C 継承状況（9 DB 近代偏重 / 集計濃淡 / 派生間独立性 / GF 共有 / FK 84.4% 未指定率）
  - Phase A 数値継承 source-of-truth テーブル（_PHASE_A_INHERITANCE_AUDIT.md 準拠）

字数合計: 約 34K-44K 字（BRIEFING 指定 35K-45K 字に整合）。

#### 3.1.2 図表 12-18 点の構造分布

各章への図表配分案:
- 序章: 0 点
- 章 1: 1-2 点（サイクル入れ子図 / 双子峰プラトー図）
- 章 2: 1-2 点（71 問統合インデックス / 4 層問い構造図）
- 章 3: 2-3 点（偉業 10 アーキタイプ / 5 シナリオ × 4 ホライズン / great_actions.db スキーマ図）
- 章 4: 2-3 点（zone マッピング / warning vs opportunity 弁別 / 優先課題 TOP10 × 偉業マッピング）
- 章 5: 1-2 点（4 軸担い手特性図 / 時代変化図）
- 章 6: 2-3 点（**四位一体マスター図【見開き相当】** / **統合ナレッジマップ【見開き相当】** / 検証構造図）
- 終章: 0-1 点（Phase D 連結マトリクス）
- 付録: 1-2 点（Phase A 限界継承表 / source-of-truth テーブル）

合計 12-18 点（中央値 14-15 点）で BRIEFING 指定値に整合。

### 3.2 phase-c-master-analysis.html（25K-30K 字）— 解析結果まとめ

本ファイルは「論理連続性」を最重要視点とする解析統合 HTML。C-1〜C-6 各トラックの解析結果（track-c{1-6}-{...}-analysis.html）を統合し、トラック横断の論理連続性を保証する。

#### 3.2.1 章立て構成

- **第 I 部: Phase C 解析の全体俯瞰**（4K 字）
  - C-1〜C-6 の解析方法論の連続性
  - 各トラックの主要分析手法と入力 DB
  - DB 集計ログ統合（C-3 great_actions.db 件数 / C-4 紐付け統計 等）

- **第 II 部: 6 トラック解析の連続性**（15K-18K 字）
  - C-1 解析: サイクル A/B/C の入れ子構造分析手法
  - C-2 解析: 71 問統合インデックス策定手法
  - C-3 解析: great_actions.db スキーマ設計と 100-150 件の構造化手法
  - C-4 解析: zone マッピング（既存 vs 期待）の差分構造分析手法
  - C-5 解析: 4 軸担い手特性マトリクス構築手法
  - C-6 解析: 四位一体マスター図と統合ナレッジマップの統合手法

- **第 III 部: 解析統合の方法論**（4K-5K 字）
  - Phase B からの方法論継承（Mサイン階層 / 三系列差 honest 開示 / 集計→言語化照合）
  - Phase C 独自の方法論進化（4 軸統合 / great_actions.db 構築）
  - Phase D（deep-knowledge 統合）への方法論的接続

- **第 IV 部: 解析の限界（自己認識）**（2K-3K 字）
  - C-3 great_actions.db 100-150 件の網羅性限界
  - C-5 担い手特性の心理 19 次元限界（era-talents.db 由来）
  - 主観的選定の構造的留保（Phase B からの継承）

字数合計: 約 25K-30K 字（BRIEFING 指定値整合）。

### 3.3 phase-c-master-verification.html（12K-15K 字）— 学術的検証

本ファイルは doc-verify 4 カテゴリの統合検証結果を提示する HTML。phase-b/track-b6-integration-verification.html（60KB / 約 25K 字）の構造を縮約版として参照する。

#### 3.3.1 章立て構成

- **第 1 章: 検証の全体俯瞰**（1K 字）
  - doc-verify 4 カテゴリの構造（スナップショット不整合 / ハルシネーション / カバレッジギャップ / チーム間不整合）
  - C-1〜C-5 各 verification.html の主要検証項目統合方針

- **第 2 章: スナップショット不整合検証**（2K-3K 字）
  - Phase B 数値継承の正確性（71 問 + 926 派生 = 997 単位）
  - Phase A 数値継承 source-of-truth 準拠（_PHASE_A_INHERITANCE_AUDIT.md）
  - 装置レコード規模（IR 1,769,821 / Funding 2,001 / UPR 41,760 等）の継承確認

- **第 3 章: ハルシネーション検証**（3K-4K 字）
  - C-3 great_actions.db 100-150 件の DB 実値照合
  - GF 由来 10 アーキタイプの実 DB 確認
  - era-talents 19 能力次元の実 DB 確認
  - 各章引用文献の実在確認

- **第 4 章: カバレッジギャップ検証**（2K-3K 字）
  - BRIEFING 必須項目の対応確認（10 必須要素）
  - 三系列差 honest 開示（briefing 値 / 実装値 / 公開値）
  - 27 未カバー問い（B-1 41 - B-2/B-3 14）の Phase C 装置評価追加状況

- **第 5 章: チーム間不整合検証**（2K-3K 字）
  - Phase A/B 値との連続性
  - C-1〜C-6 トラック間の数値整合
  - sentinel APPROVED 判定の根拠開示

- **第 6 章: Phase A 構造的限界 5 点の Phase C 継承点検**（2K 字）
  - 9 DB 近代偏重バイアス
  - 集計濃淡（FK 84.4% 未指定率等）
  - 派生間独立性
  - GF 共有問題
  - 前 4 点の Phase C での再発有無

- **第 7 章: 【推定】【解釈】【未検証】タグの公開 HTML 適用率集計**（1K-2K 字）
  - C-1〜C-6 各 report の各タグ適用率
  - 公開 HTML の各タグ密度
  - 過剰断定の検出有無

字数合計: 約 13K-16K 字（BRIEFING 指定 12K-15K 字に整合）。

### 3.4 phase-c-index.html（7 トラック導線）

本ファイルは Phase C 7 トラックへの導線として機能する。phase-b/phase-b-index.html（B-6 完了後の最新版、20KB）が直接の参考モデルとなる。

#### 3.4.1 構造案

- **page-header**: PROJECT 説明 + meta（7 トラック / 4 軸統合 / 4 ホライズン継承 / 赤白 CI）
- **「Phase C プロジェクト構造」セクション**: framework-grid（C-1 時間軸層 / C-2 問い層 / C-3 行為層 / C-4 実装-期待層 / C-5 担い手層 / C-6 統合層 / C-7 公開層）+ METHODOLOGY DOCUMENTS callout
- **「7 トラック」セクション**: 7 個の `.track-card`（C-1〜C-7、各完了状態）
  - 各カード: track-num + track-title + track-db + track-desc + track-stat + track-links（report/analysis/verification の 3 リンク）
- **「統合成果（Track C-7）」セクション**: phase-c-master-report.html へのリンク + Track C-7 出力一覧
- **「great_actions.db ダウンロード」callout**: C-3 で構築された新規 DB へのアクセス導線
- **「Phase A + Phase B Index」戻り導線**: 過去フェーズへの参照
- **footer**: 標準的な Phase C 全完了の宣言

#### 3.4.2 7 トラックカードの記述案

各カードは Phase B の B-1〜B-6 カードと同じ装飾（track-num / status-badge / track-title / track-db / track-desc / track-stat / track-links）を踏襲する。track-stat 行には各 HTML のサイズ（XX KB / 字数）+ 主要発見を記載する。

### 3.5 ryoiki-index.html 更新（追加 only）

本ファイルは既存 Phase B 全完了状態を破壊せず、Phase C セクションの追加のみで更新する。挿入位置は line 642 の `</section>`（Phase B セクション閉じ）直後、line 644 の `<footer>` の直前である。

#### 3.5.1 挿入する HTML スニペット

§2.2 で設計した 4 callout 構造（統合レポート / INDEX / 主要発見 / Phase D 起動準備）を持つ Phase C セクションを line 642 直後に挿入する。

**重要な検証観点**:
- 既存 line 1-642 は一切編集禁止
- 既存 line 644-647 footer も継承
- 挿入後の line 数は約 730-740 行（70-80 行増加）に【推定】
- 既存の `<style>` ブロック（line 11-375）は新規 CSS を追加しない（§1.3 方針）

---

## 4. textbook 構造の Phase C 適用案

### 4.1 phase-b/track-b6-integration-report.html の構造抽出

phase-b/track-b6-integration-report.html（592 行 / 78 KB）の構造を要素レベルで抽出する。これが Phase C master-report.html の直接の参考モデルとなる。

**top-bar（line 126-133）**:
- 高さ 48px、border-top 3px solid #121212、sticky 配置
- ブランド: `MIRATUKU NEWS / <span>Phase B 統合レポート</span>`
- アクション: 戻りリンク 2 種（`← Phase B Index` / `領域策定`）+ テーマ切替

**book-layout（line 135-)**:
- `display: grid; grid-template-columns: 240px 1fr;`（PC）
- `max-width: 1200px;`
- モバイル時（@media max-width: 1000px）は 1 カラム

**toc-sidebar（line 136-167）**:
- position: sticky; top: 48px; height: calc(100vh - 48px); overflow-y: auto;
- padding: 40px 24px 40px 0; border-right: 1px solid var(--border-light);
- toc-label「CONTENTS」+ ol.toc-list（章番号 + リンク）
- 章番号スタイル: `font-family: "SF Mono","Fira Code",monospace; color: var(--accent-warm)`

**book-main（line 169-571）**:
- padding: 60px 0 100px 48px; max-width: 760px;
- book-header（line 170-185）: db-tags + book-title + book-subtitle + book-meta
- chapter-section × 5（PART I〜V）: 各 margin-bottom: 80px; padding-bottom: 60px; border-bottom: 1px solid var(--border-light);

**chapter-section 内部要素**:
- chapter-number-label「PART I」（accent-warm 色 / uppercase）
- chapter-title（serif font / 1.7rem）
- p.lead（1.08rem / 太字寄り / 序文）
- h3（1.2rem / 通常見出し）
- h4（accent-warm 色 / 強調見出し）
- p（text-indent: 1em; first-of-type は 0）
- figure（border + padding 24px / figure-title + 内容 + figure-caption）
- callout（surface 背景 + accent-warm 左 border 3px）
- discovery-box（accent-warm border + accent-muted 背景）
- table（簡素な border-bottom のみ）
- tag-est / tag-int / tag-unv（推定/解釈/未検証タグ）

### 4.2 Phase C master-report.html への適用判断

B-6 構造を Phase C master-report.html にどう適用するかの判断を以下に示す。

**完全踏襲する要素**:
- top-bar 構造（高さ 48px / border-top 3px / sticky）
- book-layout grid（240px + 1fr）
- toc-sidebar の sticky 配置
- book-main の max-width: 760px
- chapter-section の構造
- discovery-box / callout / figure / tag-est-int-unv のスタイル

**Phase C 独自に拡張する要素**:
- toc-list の章番号: 「序章 / 第 1 章 / 第 2 章 / ... / 第 6 章 / 終章 / 付録」の 9 セクション体系（B-6 は「第 I 部〜第 V 部」の 5 セクション）
- 章数増加に伴い toc-list の行数も増加（B-6: 25 行 → C-7: 35-40 行【推定】）
- figure の見開き相当表現: 章 6 の「四位一体マスター図」「統合ナレッジマップ」は通常 figure より広い領域が必要
  - 案 A: max-width: 760px のまま、SVG 内部で詳細表現
  - 案 B: 該当 figure のみ max-width: 1100px に拡張（book-main の枠を超える）
  - 推奨: 案 A（既存構造を破壊しない）【推定】

**top-bar の戻りリンク**:
- `← Phase C Index`（phase-c-index.html へ）
- `領域策定`（ryoiki-index.html へ）
- 必要なら `Phase B Index` も併記

### 4.3 phase-c-master-analysis.html / phase-c-master-verification.html / phase-c-index.html の textbook 構造適用

**analysis.html / verification.html**:
master-report.html と同じ book-layout を採用する。toc-sidebar の章番号は各ファイルの章立て構造に合わせて変更する（analysis: 第 I-IV 部の 4 部構成 / verification: 第 1-7 章の 7 章構成）。装飾・色彩・フォントは完全に共通化する。

**phase-c-index.html**:
ryoiki-index.html / phase-b-index.html と同じ「container 中央配置」構造を採用する（book-layout ではない）。tracks grid + framework-grid を含むダッシュボード型レイアウト。max-width: 1100px。

---

## 5. 赤白 CI #CC1400 デザインシステム適用チェックリスト

### 5.1 db-design-system.md の必須要件

db-design-system.md（125 行）の規定を Phase C 5 公開 HTML に適用するチェックリストを作成する。

**:root カラー変数の完全コピー**:
- `--bg: #FFFFFF` / `--card: #FFFFFF` / `--card-hover: #F7F7F5`
- `--accent: #121212` / `--accent-soft: #555555`
- `--accent-warm: #CC1400` / `--accent-warm-soft: #B01200` / `--accent-muted: rgba(204,20,0,0.06)`
- `--text: #121212` / `--text-secondary: #555555` / `--text-muted: #6B6B6B`
- `--border: #D9D9D9` / `--border-light: #EEEEEE`
- `--highlight: #CC1400` / `--surface: #F7F7F5`
- `--font: "Noto Sans JP", ...` / `--font-serif: "Noto Serif JP", ...`

**[data-theme="dark"] カラー変数の完全コピー**:
- `--bg: #121212` / `--card: #1A1A1A` / `--card-hover: #222222`
- `--accent: #E0E0E0` / `--accent-warm: #FF4030` / `--accent-warm-soft: #FF6050`
- 残りの変数も db-design-system.md 規定通り

**フォント・タイポグラフィ**:
- Google Fonts: `Noto Sans JP` (300, 400, 500, 700) + `Noto Serif JP` (400, 600, 700)
- 章番号: `"SF Mono", "Fira Code", monospace`
- 行間: `line-height: 1.85-1.95`（master-report 系は 1.95、index 系は 1.85）
- 字間: `letter-spacing: 0.025em`
- 機能: `font-feature-settings: "palt"`
- 段落: `text-indent: 1em`、first-of-type は 0

**必須要素**:
- top-bar: `border-top: 3px solid #121212`（var(--accent)）/ ブランド / テーマ切替ボタン
- サイドバー TOC: 位置固定（sticky）/ 章番号付き / ホバーで accent-warm
- メインカラム: max-width 740-760px
- テーマ切替 JS: data-theme 属性切替 / localStorage 保存
- 印刷時: top-bar / sidebar 非表示（@media print）
- モバイル（<1000px）: サイドバー上部展開

**favicon**:
- `<link rel="icon" href="https://esse-sense.com/favicon.ico">`

### 5.2 NG 事項チェック

db-design-system.md の NG 事項を Phase C 5 公開 HTML で完全排除する。

- 絵文字使用ゼロ（本文・UI・コメント・ファイル名すべて）
- 派手色（青/緑/紫等）を主役色にしない（赤白 CI #CC1400 のみが主役、他色は subtle な装飾のみ）
- card 内背景色の多用禁止（白基調維持）
- 文字飾り（影・輪郭）禁止
- アイコンフォント（Font Awesome 等）使用禁止

### 5.3 公開前チェックリスト（Phase C 5 公開 HTML 各々）

各 HTML（master-report.html / master-analysis.html / master-verification.html / phase-c-index.html / ryoiki-index.html 更新）で以下を確認する。

- [ ] `:root` に上記カラー変数を完全コピー
- [ ] `[data-theme="dark"]` のダークモード対応
- [ ] Google Fonts ロード（Noto Sans JP + Noto Serif JP）
- [ ] top-bar に `border-top: 3px solid #121212` 適用
- [ ] サイドバー TOC（master-report/analysis/verification のみ、位置固定、章番号付き）
- [ ] メインカラム max-width 760px（master-report/analysis/verification）または 1100px（index 系）
- [ ] 段落の text-indent 1em（first-of-type は 0）
- [ ] 絵文字・アイコン未使用（gsearch で `[\u{1F300}-\u{1F9FF}]` 確認）
- [ ] モバイル対応（@media max-width: 1000px / 720px）
- [ ] 印刷対応（@media print で top-bar / sidebar 非表示）
- [ ] テーマ切替 JS 実装（toggleTheme 関数 + localStorage）
- [ ] favicon: `https://esse-sense.com/favicon.ico`
- [ ] 言語属性: `<html lang="ja" data-theme="light">`
- [ ] meta charset: UTF-8、meta viewport: 適切な値

---

## 6. 図表 12-18 点の優先度ランキング案

### 6.1 master-report.html 図表候補と優先度

phase-c-master-report.html に組み込む図表 12-18 点の優先度ランキングを提示する。優先度は (1) Phase C 全体の核心成果との直接性、(2) 視覚的説明力、(3) 既存図表（B-6 等）との差別化、の 3 軸で判定する。

**【最優先 Tier 1: 必須 8 点】**

1. **Fig.0: Phase A → B → C 全体の流れ図**（序章）— Phase A 9 トラック → Phase B 6 トラック → Phase C 7 トラックの全体俯瞰図。B-6 Fig.1 を発展させる。
2. **Fig.1: サイクル A/B/C 入れ子構造図**（章 1）— 認知転換 280-310 年 / 制度興亡 150-300 年 / プラトー 250 年の 3 サイクル時間軸並置図。
3. **Fig.2: 71 問統合インデックス**（章 2）— B-1 41 問 + B-3 30 問の単一台帳化図。問い ID × ホライズン × Mサイン階層の三軸表。
4. **Fig.3: 偉業 10 アーキタイプ × 5 シナリオ × 4 ホライズンマッピング**（章 3）— C-3 great_actions.db の核心構造図。
5. **Fig.4: zone マッピング（既存 vs 期待偉業の差分構造）**（章 4）— Hot/Warm/Cool/Dead/N/A zone × 偉業推進状況。
6. **Fig.5: 4 軸担い手特性マトリクス**（章 5）— 心理 × 行動 × 領域 × 専門性の 4 軸統合図。
7. **Fig.6: 四位一体マスター図【見開き相当】**（章 6）— C-1 サイクル × C-2 問い × C-3 偉業 × C-5 担い手の四位一体。Phase C 最重要図。
8. **Fig.7: 統合ナレッジマップ【見開き相当】**（章 6）— Phase B 71 + Phase C 偉業 100-150 + 担い手特性 = 全 1,100-1,200 単位の統合可視化。

**【高優先 Tier 2: 推奨 4-6 点】**

9. **Fig.8: CTI v2 双子峰プラトー図**（章 1）— 9 時代 CTI スコア棒グラフ。AI 革命 104.7 / 産業革命 100.0 の 1.05 倍関係を可視化。
10. **Fig.9: 4 層問い構造図（メタ × 規範 × 実装 × 装置）**（章 2）— 71 問の 4 層分類図。
11. **Fig.10: great_actions.db スキーマ図**（章 3）— actions テーブル + 関連テーブルの ER 図。
12. **Fig.11: 優先課題 TOP10 × 偉業マッピング**（章 4）— Phase B B-5 確定 TOP10 × Phase C 偉業候補の交差表。
13. **Fig.12: 担い手特性の時代変化図**（章 5）— 産業革命期 → 現代 → 2030/50/70/2100 の 4 時点比較。
14. **Fig.13: Phase D 連結マトリクス候補**（終章）— deep-knowledge 20 章 × Phase C 7 トラックの 140 セル候補図。

**【補助 Tier 3: 余裕があれば 2-4 点】**

15. **Fig.14: 5 シナリオ × 偉業類型対応表**（章 4）— Pluriverse 18 / Techno 13 / Care 19 / Slow 12 / Frag 11 の偉業候補配分。
16. **Fig.15: great-figures 過去事例 → 現代偉業 → 未来偉業の系譜接続図**（章 3）— 9,178 GF 由来の系譜継承。
17. **Fig.16: warning vs opportunity 偉業弁別図**（章 4）— 「動きはあるが方向違い」と「動きはないが期待される」の対比。
18. **Fig.17: Phase A 構造的限界 5 点の Phase C 継承状況**（付録）— 限界 × 継承可否のマトリクス表。

### 6.2 図表表現方法の判断

各図表を SVG / Canvas / `<pre>` ASCII art / `<table>` のいずれで表現するかの判断基準を整理する。

- **SVG**: Fig.6（四位一体マスター図）/ Fig.7（統合ナレッジマップ）/ Fig.10（ER 図）/ Fig.13（Phase D 連結マトリクス）等、視覚的複雑度が高い図表
- **`<pre>` ASCII art**: Fig.0（全体の流れ図）/ Fig.1（サイクル入れ子構造図）等、単純な階層・流れ図（B-6 Fig.1/Fig.2 のスタイルを踏襲）
- **`<table>`**: Fig.2（71 問統合インデックス）/ Fig.3（偉業マッピング）/ Fig.4（zone マッピング）/ Fig.11（優先課題 TOP10）/ Fig.17（限界継承表）等、構造化データ
- **棒グラフ・散布図**: Fig.8（CTI v2 双子峰プラトー）/ Fig.12（担い手特性時代変化）等、定量比較

【推定】 Phase C リード本体実行時には、SVG 図表を新規作成する工数が大きいため、Tier 1 の Fig.6/Fig.7（見開き相当）に SVG 工数を集中させ、Tier 2/3 の図表は `<pre>` / `<table>` で簡素化する戦略が望ましい。これは B-6 Fig.1-Fig.6 の 6 図表のうち SVG 図表が 0 個・`<pre>` ASCII art と `<table>` が中心であった戦略と整合する。

---

## 7. HTML タグバランス検証手法（B-6 完全均衡の手法）

### 7.1 B-6 達成値の確認

phase-b/track-b6-integration-report.html では analysis 17/17 + verification 36/36 + report 35/35 の `<div>` 完全均衡を達成した。【BRIEFING より、未検証なので C-7 リード本体で実 grep 数値確認が必要】

具体的には、track-b6-integration-report.html を grep で確認すると以下のタグ構造が確認された:
- `<section class="chapter-section">` × 5（PART I〜V）+ それぞれ `</section>` 対応
- `<div class="figure">` 7-8 件 + それぞれ `</div>` 対応
- `<div class="callout">` 2-3 件 + それぞれ `</div>` 対応
- `<div class="discovery-box">` 5 件 + それぞれ `</div>` 対応
- `<table>` 3 件 + それぞれ `</table>` 対応

### 7.2 検証手法の標準化

C-7 リード本体実行時のタグバランス検証手法を以下に標準化する。

**手順 1: grep カウント**

```bash
# 各 HTML ファイルに対して実行
file=phase-c-master-report.html

echo "=== <div> bal ==="
echo "open: $(grep -c '<div' $file)"
echo "close: $(grep -c '</div>' $file)"

echo "=== <section> bal ==="
echo "open: $(grep -c '<section' $file)"
echo "close: $(grep -c '</section>' $file)"

echo "=== <table> bal ==="
echo "open: $(grep -c '<table' $file)"
echo "close: $(grep -c '</table>' $file)"
```

**手順 2: 階層整合性検証**

grep カウントが均衡していても、ネスト構造が崩れている場合がある。Python の `html.parser` または BeautifulSoup で構文解析し、構造的整合性を確認する。

```python
from bs4 import BeautifulSoup
with open('phase-c-master-report.html') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')
# soup が完全パースされれば構文整合
```

**手順 3: 各章の独立検証**

chapter-section 単位で開始タグから閉じタグまでの内部 div / section / table の均衡を確認する。これは特に章 6（四位一体マスター図 + 統合ナレッジマップ + 検証構造図の 3 figure を含む長い章）で崩れやすい。

**手順 4: 公開 HTML 5 ファイル全件の最終チェック**

5 ファイル（master-report / master-analysis / master-verification / phase-c-index / ryoiki-index 更新版）の全件で手順 1-3 を実行し、完全均衡を確認する。完了報告フォーマットに「タグバランス検証: 全 HTML 完全均衡」を記載する。

### 7.3 再発防止のための事前注意

Phase B で「各章末尾の余分 `</div>`」が再発する問題があった（feedback_html_validation.md より）。Phase C ではこの問題を以下の方法で防止する。

- chapter-section の閉じタグは必ず前後 1 行空行で区切る（visual な確認容易性）
- 図表 figure の閉じタグも前後 1 行空行
- discovery-box / callout も同様
- ファイル末尾の `</main>` `</div>` `</body>` `</html>` を 4 行で明示

---

## 8. リンク切れ検証手法

### 8.1 内部リンク検証

Phase C 5 公開 HTML 内のすべての `href` を検証する。

**内部リンク種別**:
- 同一フェーズ内: `phase-c-master-{analysis,verification,report}.html` / `phase-c-index.html` / `track-c{1-7}-{...}-{report,analysis,verification}.html` / `track-c{1-7}_handoff.md`
- 上位フェーズ: `../ryoiki-index.html` / `../databases.html`
- 過去フェーズ: `../phase-b/phase-b-index.html` / `../phase-b/track-b6-integration-report.html`

**検証方法**:

```bash
# Phase C ディレクトリ内の全 href 抽出
cd /Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-c
grep -roh 'href="[^"]*"' *.html | sort -u > /tmp/phase-c-hrefs.txt

# 内部リンクのファイル存在確認
while IFS= read -r line; do
    href=$(echo "$line" | sed 's/href="\(.*\)"/\1/')
    # # アンカーは無視、http は外部リンクは別途検証
    if [[ "$href" == http* || "$href" == \#* ]]; then continue; fi
    # 相対パス解決
    if [[ -e "$href" ]]; then
        echo "OK: $href"
    else
        echo "BROKEN: $href"
    fi
done < /tmp/phase-c-hrefs.txt
```

### 8.2 外部リンク検証

主要な外部リンクは限定的（favicon / Google Fonts / GitHub Pages の自己参照）であり、curl で HTTP 200 確認する。

```bash
curl -sSf -o /dev/null https://esse-sense.com/favicon.ico
curl -sSf -o /dev/null https://fonts.googleapis.com/css2
```

### 8.3 アンカーリンク検証

`<a href="#section-id">` のアンカーリンクは、対応する `id="section-id"` 属性が同一ファイル内に存在することを確認する。

```bash
# アンカー抽出
grep -oh 'href="#[^"]*"' phase-c-master-report.html | sed 's/href="#\(.*\)"/\1/' | sort -u > /tmp/anchors.txt
# id 属性抽出
grep -oh 'id="[^"]*"' phase-c-master-report.html | sed 's/id="\(.*\)"/\1/' | sort -u > /tmp/ids.txt
# 差分（アンカーに対応する id がない場合は欠損）
comm -23 /tmp/anchors.txt /tmp/ids.txt
```

---

## 9. C-7 リード本体実行時の論点（4-6 点）

### 9.1 論点 1: 図表 12-18 点中の SVG 化判断

§6.2 で示したように、Tier 1 の Fig.6（四位一体マスター図）と Fig.7（統合ナレッジマップ）は「見開き相当」の表現が必要であり、SVG での新規作成が望ましい。しかし、これらは **C-7 単独で工数 2-3 日**を要する大型作業となる可能性が高い【推定】。

**判断選択肢**:
- 案 A: Fig.6/Fig.7 のみ SVG 化、他は `<pre>` / `<table>` で簡素化（推奨）
- 案 B: 全 18 図表を SVG 化（高品質だが工数 5-7 日増）
- 案 C: SVG 化はゼロ、すべて `<pre>` / `<table>` で表現（B-6 同様の戦略、低工数）

リード本体実行時の判断軸: (1) BRIEFING 「質>速度」原則 / (2) 公開 URL の外部受信者像 / (3) Phase D 起動への時間制約。

### 9.2 論点 2: phase-c-master-report.html 字数 35K-45K 字の達成方法

BRIEFING 指定 35K-45K 字（B-6 報告書 78KB ≒ 28-35K 字相当）を超える字数で、内容の希薄化を避ける必要がある。

**判断選択肢**:
- 案 A: 各章を均等配分（章 1-6 各 4-7K 字 + 序章/終章/付録 8-12K 字 = 約 36-42K 字）
- 案 B: 章 6（四位一体 + ナレッジマップ）に最大配分（10-12K 字、他章 3-4K 字）
- 案 C: 各章を C-1〜C-6 report.html から「抜粋」として直接転載（重複リスクあり）

推奨: 案 A（均等配分、章 6 のみ 6-8K 字 + 図表 2-3 点で実質的な厚みを確保）【推定】。BRIEFING で「C-1〜C-5 各 report.html の主要検証項目を統合」とあるため、verification.html 側で重複統合を担い、report.html では各 Track の核心成果を独自言語化する戦略が望ましい。

### 9.3 論点 3: master-verification.html 4 カテゴリの統合方法

doc-verify 4 カテゴリ（スナップショット不整合 / ハルシネーション / カバレッジギャップ / チーム間不整合）を 12K-15K 字で統合する際、C-1〜C-5 各 verification.html の重複を避ける必要がある。

**判断選択肢**:
- 案 A: 4 カテゴリ × C-1〜C-5（5 トラック）= 20 セルで埋める（統合後の最小単位）
- 案 B: 4 カテゴリ × Phase C 全体（独立記述）= 4 章で埋める（重複を完全排除）
- 案 C: 主要検証項目のみ 12-15 件抽出して統合（中間案）

推奨: 案 C（主要検証項目 12-15 件の統合）【推定】。これは Phase B B-6 verification.html（60KB / 約 25K 字）の構造と整合する。

### 9.4 論点 4: ryoiki-index.html Phase C セクションの callout 数

§2.2 で 4 callout 構造を提案したが、_PHASE_C_PLAN.md 提供スニペットは 2 callout 構造である。

**判断選択肢**:
- 案 A: 提供スニペット通り 2 callout（最小）
- 案 B: Phase B との対称性で 4 callout（推奨、§2.2 案）
- 案 C: 5 callout 以上（過剰）

推奨: 案 B（Phase B との視覚的均衡）【推定】。ただし、リード本体実行時に Phase C 全体の主要発見数が 5 点に満たない場合（4 点以下）は callout 3「主要発見」を統合レポート callout 内に吸収する設計に切り替える。

### 9.5 論点 5: phase-c-index.html の 7 トラック表示順

7 トラックは依存順（C-1 → C-2 → C-3 → C-4 → C-5 → C-6 → C-7）で表示するのが標準だが、優先度順（重要度高い順）にする選択肢もある。

**判断選択肢**:
- 案 A: 依存順（C-1 → C-7、Phase B Index と整合）
- 案 B: 優先度順（C-6 統合 / C-3 great_actions.db を上位、補助トラックを下位）
- 案 C: ハイブリッド（最初に C-6 をハイライト → C-1〜C-5 が依存順 → C-7 公開）

推奨: 案 A（依存順、Phase B Index と整合）【推定】。これは Phase B Index が B-1 → B-6 の依存順を採用した設計と一貫する。

### 9.6 論点 6: 公開後の保守責任とアーカイブ範囲

Phase C 5 公開 HTML は GitHub Pages 公開後、Phase D 進行中も外部読者に常時アクセスされる。Phase D で Phase C の数値・成果が更新される場合、ryoiki-index.html / phase-c-master-report.html の整合をどう保つか。

**判断選択肢**:
- 案 A: Phase C は完了スナップショットとして固定、Phase D は別ディレクトリ（phase-d/）で展開
- 案 B: Phase C ファイルも Phase D で適宜更新（差分追記）
- 案 C: Phase C / Phase D を統合した unified-index.html を新規作成

推奨: 案 A（Phase C 固定、Phase D は別ディレクトリ）【推定】。これは Phase A → B 移行時に track1-9 の HTML を変更せず Phase B セクションのみ追加した方針と一貫する。

---

## 10. 完了基準と引継ぎ書テンプレート

### 10.1 C-7 完了基準（BRIEFING §完了報告フォーマットより）

C-7 リード本体実行時の完了基準を以下に整理する。

- phase-c-master-analysis.html: 25K-30K 字 / 図表数 確認
- phase-c-master-verification.html: 12K-15K 字 / 検証項目数 確認
- phase-c-master-report.html: 35K-45K 字 / 図表 12-18 点 確認
- phase-c-index.html: 7 トラック導線完備
- ryoiki-index.html 更新: Phase C セクション追加 + Phase D placeholder 配置
- タグバランス検証: 全 HTML で `<div>` / `<section>` / `<table>` 完全均衡
- リンク切れ検証: 内部リンク全件 OK / 外部リンク主要件 OK
- 公開 URL 反映確認: GitHub Pages で URL がアクセス可能
- git push 完了
- track-c7_handoff.md 作成（Phase D D-0 への起動シグナル）

### 10.2 track-c7_handoff.md の構造案

Phase B の track-b6_handoff.md（17,777 字）を参考に、Phase C C-7 引継ぎ書の構造案を以下に示す。

- §1: Track C-7 の最終整合値（5 公開 HTML サイズ・字数・図表数・検証結果）
- §2: Phase C 全体の核心成果（4 軸統合 / great_actions.db / 四位一体マスター図 / 統合ナレッジマップ）
- §3: Phase D D-0 起動条件達成の宣言
- §4: Phase D 連結マトリクス候補（deep-knowledge 20 章 × Phase C 7 トラック = 140 セル）
- §5: 5-10 問候補プール（Phase C で確定）
- §6: Phase C から Phase D への申し送り（Phase A 構造的限界 5 点の継承状況、新規限界の honest 開示）
- §7: 公開 URL 一覧 + GitHub Pages 反映確認結果
- §8: 研究の限界（自己認識 3 点）

---

## 11. リード本体実行時の優先順位ガイド

C-7 リード本体実行時の優先順位を以下に示す。質>速度の原則のもと、最も重要な作業から順に着手する。

**Phase 1: 基盤整備（着手時、半日）**
1. ryoiki-index.html 現状再確認（編集禁止範囲の確認）
2. phase-c-index.html の新規作成（既存 phase-b-index.html を参考に簡易版を先行作成）
3. db-design-system.md チェックリストを 5 公開 HTML 用テンプレートとして抽出

**Phase 2: 主役 HTML の構築（中盤、2-3 日）**
4. phase-c-master-report.html の章立て確定（§3.1.1）+ 序章 + 章 1 + 章 2 から執筆開始
5. phase-c-master-analysis.html の章立て確定（§3.2.1）+ 第 I 部 + 第 II 部 から執筆開始
6. 図表 Tier 1（Fig.0-Fig.7）の SVG/`<pre>`/`<table>` 表現を順次構築

**Phase 3: 検証 HTML と総合 HTML（後半、1-2 日）**
7. phase-c-master-verification.html の 7 章構造（§3.3.1）を執筆
8. phase-c-master-report.html の章 3-6 + 終章 + 付録を執筆完了
9. 図表 Tier 2（Fig.8-Fig.13）を追加

**Phase 4: 統合・公開（最終日、半日-1 日）**
10. ryoiki-index.html の Phase C セクション追加（§2.2 案 B 採用、4 callout 構造）
11. タグバランス検証（§7）+ リンク切れ検証（§8）の全件実行
12. git commit + push + GitHub Pages 反映確認
13. track-c7_handoff.md 作成（§10.2 構造）

合計工数想定: 4-6 日（BRIEFING 想定値と整合）。

---

## 12. 残された不確定事項と Phase C 全体への波及

### 12.1 C-1〜C-6 完了後にしか確定できない項目

本事前リサーチは Phase C 計画書策定段階（Wave 0）で作成されているため、以下の項目は C-7 リード本体実行時（Wave 5、C-6 完了後）に最終確定する。

- C-1 サイクル A/B/C の最終投影値（2030/50/70/2100）
- C-2 71 問統合インデックスの最終単一台帳
- C-3 great_actions.db の最終件数（100-150 件のどこか）+ スキーマ最終形
- C-4 zone マッピングの最終マッピング数値
- C-5 担い手特性類型の最終件数
- C-6 四位一体マスター図 + 統合ナレッジマップの最終構造
- Phase C 全体の主要発見数（4-6 点予想）+ 5-10 問候補プールの最終リスト

### 12.2 Phase C 全体への波及

C-7 で最終整形された Phase C 5 公開 HTML は、以下の波及効果を持つ。

- **Phase D（deep-knowledge 統合）への入力データ確定**: phase-c-master-report.html / phase-c-master-analysis.html / great_actions.db が Phase D D-0 の主入力となる
- **ミラツク外部公開資産の質的変化**: Phase A の ryoiki-master-report.html → Phase B の B-6 統合レポート → Phase C の四位一体マスター図 = 3 段階で「ミラツクが描く未来社会への羅針盤」が完成
- **Phase A 構造的限界 5 点の継承記録**: Phase D 着手時にも引き継がれる構造的限界の honest 開示が、Phase C 5 公開 HTML で確定する

---

## 結語

本事前リサーチは Track C-7 リード本体が「Phase C HTML 成果物公開と ryoiki-index 更新」を実行する際の設計枠組みを以下の 9 軸で確定した。

1. ryoiki-index.html 現状解析（Phase A 9 トラック + Track 10 + Phase B 6 トラック構造を破壊しない方針確認）
2. Phase C セクション追加の HTML テンプレート設計（4 callout 構造案）
3. 5 公開 HTML ファイル設計（master-{analysis,verification,report} + phase-c-index + ryoiki-index 更新）
4. textbook 構造の Phase C 適用案（B-6 完全踏襲 + 7-9 章への章数拡張）
5. 赤白 CI #CC1400 デザインシステム適用チェックリスト（公開前必須クリア）
6. 図表 12-18 点の優先度ランキング（Tier 1: 8 点必須、Tier 2: 4-6 点推奨、Tier 3: 2-4 点補助）
7. HTML タグバランス検証手法（B-6 完全均衡の手法を grep + Python パーサで標準化）
8. リンク切れ検証手法（内部リンク全件・外部リンク主要件・アンカーリンク）
9. C-7 リード本体実行時の論点 6 点（SVG 化判断 / 字数達成 / 検証統合方法 / callout 数 / 表示順 / 公開後保守）

C-7 リード本体実行時には本事前リサーチを参照しながら、§11 の優先順位ガイドに従って Phase 1-4 を段階的に実行する。完了基準は §10.1 の通り、5 公開 HTML 全件の字数・図表数・タグバランス・リンク切れ検証・GitHub Pages 反映確認の 5 系統で判定する。

質>速度の原則のもと、本トラックは Phase C 全体の公開顔として最終整形の精度が問われる。タグバランス検証・リンク切れ検証・アクセシビリティ確認を厳格に行い、Phase D 起動準備を整える。
