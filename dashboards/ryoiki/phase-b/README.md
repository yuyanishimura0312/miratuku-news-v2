# Phase B 統合的解析プロジェクト

ミラツク領域策定プロジェクトの第二段階。Phase A（9トラック解析）の上に積み上がる「多層構造化と問い群再構築」フェーズ。

## 構成（6トラック）

| Track | 内容 | 主要成果 |
|-------|------|---------|
| B-1 | 多層人類史 × 4 ホライズン × 41 問構築 | 真M4 / 準M14 / 概念整合15 / 単独T8、CTL-V 17 / T 6 / G 6 |
| B-2 | 哲学/文学/神話/伝統知「すでにある未来」抽出 | 14 問 × 5 系統 × 85 wisdom records、Type-A/B/C 三類型 + 三大クラスター |
| B-3 | 善い社会 5 シナリオ × 30 問 × 経路設計 | Pluriverse 18 / Care 19 / Techno 13 / Slow 12 / Frag 11、8 critical junctures |
| B-4 | 7 変化検出装置 × 24 問 × 168 セル評価 | initiatives 463 件、装置別平均 SG 4.00 / IR 3.21 / UPR 2.67 |
| B-5 | hot/dead zones 弁別 + 優先領域 TOP10 | 待機中 |
| B-6 | 統合 HTML 化 + ryoiki-index 更新 | 待機中 |

## 構築 DB

- `~/projects/research/already-future-db/already_future.db`（B-2: 14 問 / 5 系統 / 85 wisdom / 22 cross-question links）
- `~/projects/research/initiatives-db/initiatives.db`（B-4: 24 問 / 7 装置 / 168 coverage_scores / 463 initiatives）

## 主要発見（2026-05-09 時点）

1. **B-1**: 「2030 near 真M由来 23.1% (3/13)」「Mサイン階層由来 53.8%」「3 パラダイム同時失効」（進歩・科学中立性・西洋普遍主義）
2. **B-2**: 「14 問の 92.9% が既出回答型」「三大クラスター（多元的人格群／pluriverse 群／長期時間群）」
3. **B-3**: 「pluriverse 的前提を方法論レベルで実装する規範層」「critical juncture 8点のうち 4/8 = 50%（厳密: 真M+準M）/ 6/8 = 75%（概念整合含む）が Phase A Mサイン領域接続」「Fragmentation シナリオ wisdom 蓄積の薄さ（未踏領域）」
4. **B-4**: 「SG 除く 6装置が near 偏重」「規範系・概念系問い（Q-N10/Q-F03/Q-V07）が装置応答最薄」「全装置不応答型は実体ゼロ → 4類型に再構成」

## 品質ゲート方針（3層）

```
リード → doc-verify → refinement-coordinator → sentinel
```

各 Track で：
1. **リード**: 実装エージェントが analysis/verification/report/handoff を生成
2. **doc-verify**: 別エージェントが 4カテゴリ（スナップショット不整合/ハルシネーション/カバレッジギャップ/チーム間不整合）を検証
3. **refinement-coordinator**: doc-verify 指摘を修正（最大3ラウンド）
4. **sentinel**: Devil's Advocate 視点で VETO 権付き最終ゲート

## ファイル構成

```
phase-b/
├── _PHASE_B_PLAN.md              # 計画書
├── _PHASE_B_STATUS.md            # リアルタイム進捗
├── _TRACK_B{2-6}_BRIEFING.md     # 各トラックbriefing
├── _TRACK_B5_INPUT_TEMPLATE.md   # B-5 入力雛形
├── _TRACK_B5_INPUT_DATA.md       # B-5 入力確定版
├── _TRACK_B6_STRUCTURE.md        # B-6 構造設計
├── _TRACK_B6_VERIFICATION_TEMPLATE.html  # B-6 verification 雛形
├── _TRACK_B4_REFINEMENT_BRIEFING.md      # B-4 軽微追補ガイド
├── _TRACK_LINKAGE_MATRIX.md      # B-1×B-2×B-3×B-4 連結マトリクス
├── _PHASE_A_INHERITANCE_AUDIT.md # Phase A → B 数値継承監査
├── phase-b-index.html            # Phase B インデックス
├── track-b{1,2,3,4}-{analysis,verification,report}.html  # 各トラック成果物
├── track-b{1,2,3,4}_handoff.md   # 各トラック引継ぎ書
├── track-b{1,2,3,4}-doc-verify-report.md  # doc-verify 結果
└── track-b{1,2,3,4}-sentinel-verdict.md   # sentinel verdict
```

## デザイン規約

- 赤白CI（#CC1400）
- Noto Serif JP（本文）+ Noto Sans JP（UI）
- textbook.html 構造（top-bar 48px + toc-sidebar 240px + main 760px）
- 絵文字・アイコンフォント禁止
- HTMLタグバランス完全（差分0）

## 関連リンク

- **Phase A 9 トラック**: `../track{1-9}-*-{analysis,verification,report}.html`
- **Phase A 統合**: `../ryoiki-master-report.html`
- **Phase B Index**: `phase-b-index.html`
- **領域策定全体 Index**: `../ryoiki-index.html`
- **公開URL**: https://yuyanishimura0312.github.io/miratuku-news-v2/dashboards/ryoiki/phase-b/

## ライセンス・著者

- **NPO法人ミラツク** 領域策定プロジェクト
- 主任研究: 西村勇也
- 公開: 2026-05-09 〜
