# Phase B 統合的解析プロジェクト 計画書

## プロジェクト位置づけ

Phase A（9トラック解析）の上に積み上がる**第二段階**。Phase A が「各DBが何を語るか」を抽出したのに対し、Phase B は「**それらを多層構造化し、問い群として再構築する**」フェーズ。

## 全体構造

```
Phase A（完了）         Phase B（本フェーズ）
─────────────────       ─────────────────────
9Track解析     ───→   Track B-1: 多層構造化
  ↓                      （人類史層×4ホライズン層）
27HTML+検証               ↓
  ↓                    Track B-2: すでにある未来
ryoiki-master-report     （人類学/哲学/文学/神話/伝統知）
                          ↓
                       Track B-3: 善い社会の可能性
                          ↓
                       Track B-4: 変化検出装置の予測力
                          ↓
                       Track B-5: 動きの状況測定
                          ↓
                       Track B-6: 統合HTML化
```

## 6トラック詳細

### Track B-1: 多層人類史×4ホライズン × 問い群構築（基盤層）

**目的**: Phase A 9トラック成果を「人類史の変遷」と「2030/2050/2070/2100予測」に多層構造化し、現在の2026ホライズンと各射程の問い群を策定。

**入力**:
- Phase A の9トラック handoff.md（特に T2 CLA 126年・T4 Historical 4DB近代偏重・T8 700万年技術史）
- ryoiki-master-report.html 第1-4部（メタテーマ M01-M15・連結マトリクス）

**出力**:
1. `track-b1-layered-history-analysis.html` — 人類史多層構造の解析
2. `track-b1-layered-history-verification.html` — 4カテゴリ検証
3. `track-b1-layered-history-report.html` — 問い群レポート
4. `track-b1_handoff.md`

**核心成果**:
- 人類史の多層構造（civilization層 × era層 × paradigm層 × myth層）
- 4ホライズン予測の多層構造化（VeSTEG × CTL-1 × Mサイン階層）
- 2026ホライズンに立ち現れつつあるテーマ
- 各射程（2030/50/70/2100）の問い群とサブカテゴリー
- 背景となる Phase A 解析結果の引用

### Track B-2: すでにある未来DB構築（補完層）

**目的**: Track B-1の問い群に対し、人類学・哲学・文学・神話学・伝統知が**すでに考え、回答してきた知**を抽出し、新規データベースとして構築。

**入力**:
- Track B-1 問い群
- Phase A の Track 9 (Good Society) handoff.md
- 既存DB: PHIL 9,583/LIT 11,115/MY 10,615/TK 3,001/AN 500概念

**出力**:
1. `track-b2-already-future-analysis.html`
2. `track-b2-already-future-verification.html`
3. `track-b2-already-future-report.html`
4. `track-b2_handoff.md`
5. **新規DB**: `~/projects/research/already-future-db/already_future.db`
   - スキーマ: question_id（B-1問い）× source_db（PHIL/LIT/MY/TK/AN）× concept × tradition × era × civilization × wisdom_text × derivation_method

**核心成果**:
- B-1問い群 × 5 traditions のマトリクス
- 各問いに対する歴史的回答パターン
- 「既に問われていた問い」と「新たな問い」の弁別

### Track B-3: 善い社会の可能性の未来 × 経路 × 選択（規範層）

**目的**: 哲学・文学・神話・伝統知の「善い社会」テーマと人類史/将来予測を組み合わせ、**複数あり得る可能性の未来**と各経路、現在の選択点での問い群を策定。

**入力**:
- Track B-2 すでにある未来DB
- Track B-1 4ホライズン問い群

**出力**:
1. `track-b3-good-society-paths-analysis.html`
2. `track-b3-good-society-paths-verification.html`
3. `track-b3-good-society-paths-report.html`
4. `track-b3_handoff.md`

**核心成果**:
- 複数あり得る未来（少なくとも3-5シナリオ）
- 各シナリオへの経路図（branching pathways）
- 現在の選択点（critical junctures）
- 「善い社会」可能性のための問い群

### Track B-4: 変化検出装置の予測的応答評価 + 取り組みDB（実装層）

**目的**: シグナル/研究者PR/企業PR/政策/企業ニーズ/資金調達/産学連携などの**変化検出装置**が、Track B-1問い群にどの程度予測的に応答できているかを評価。すでにある取り組みを領域別にDB化。

**入力**:
- Track B-1 4ホライズン問い群
- 既存DB: SG 7,668シグナル/UPR 大学PR/SGRD 企業RDPR/Policy/IR/funding/sangaku-matcher等

**出力**:
1. `track-b4-detection-systems-analysis.html`
2. `track-b4-detection-systems-verification.html`
3. `track-b4-detection-systems-report.html`
4. `track-b4_handoff.md`
5. **新規DB**: `~/projects/research/initiatives-db/initiatives.db`
   - スキーマ: question_id × initiative_type × source_db × organization × initiative × stage × horizon × detection_lag

**核心成果**:
- 7変化検出装置 × B-1問い群のカバレッジマトリクス
- 各装置の予測的応答力スコア
- すでにある取り組みのDB（領域別）

### Track B-5: B-3問い群 × 現代社会の動きの状況測定（診断層）

**目的**: Track B-3「善い社会」問い群に対し、現代社会の実態にどの程度動きがあるかを Track B-4 の変化検出装置と紐付けて測定。

**入力**:
- Track B-3 善い社会問い群
- Track B-4 取り組みDB
- 7変化検出装置すべて

**出力**:
1. `track-b5-current-momentum-analysis.html`
2. `track-b5-current-momentum-verification.html`
3. `track-b5-current-momentum-report.html`
4. `track-b5_handoff.md`

**核心成果**:
- B-3問い群 × 7装置の動き測定マトリクス
- 動きのある群（hot zones）/ 動きのない群（dead zones）の弁別
- 構造的空白領域の特定

### Track B-6: Phase B 統合HTML化 + ryoiki-index.html更新

**目的**: Track B-1〜B-5 の解析結果を統合HTML化し、ryoiki-index.html に Phase B セクションを追加。

**出力**:
1. `phase-b-master-report.html` — Phase B統合メタレポート
2. `phase-b-index.html` — Phase B 5トラック統合インデックス
3. `ryoiki-index.html` 更新 — Phase A + Phase B 統合インデックス

## 実行体制（Phase A 教訓継承）

### 三層品質ゲート
- **doc-verify**: 各Track完了後、独立検証（4カテゴリ）
- **sentinel**: doc-verify通過後、最終ゲート（VETO権付き）
- **refinement-coordinator**: 修正サイクル（最大3ラウンド）

### Phase A 教訓の継承
1. **キーワードgrepチェックリスト化**（Track 4 r2 教訓）
2. **doc-verify §4-§6 sentinel引継ぎ事項の必須精査**（Track 5 r2 教訓）
3. **末尾構造への波及確認**（Track 6 教訓）
4. **三系列 honest 開示**（Track 7 教訓）
5. **文脈別の独立性表現処理**（Track 8 教訓）
6. **取り違え防止の構造的予防注記**（Track 6 教訓）

### Track 投入順序（依存関係）

```
Wave 0: 基盤整備（本ドキュメント）
  ↓
Wave 1: Track B-1（基盤層、最初に実行）
  ↓ 検証通過後
Wave 2: Track B-2 + Track B-4 並列（B-1依存）
  ↓ 検証通過後
Wave 3: Track B-3（B-2依存） + Track B-5（B-3とB-4両方依存→B-3完了待ち）
  ↓ 検証通過後
Wave 4: Track B-6 統合
```

## デザイン規約（Phase A継承）

- 赤白CI #CC1400
- Noto Serif JP本文 + Noto Sans JP UI
- textbook.html構造（top-bar + toc-sidebar + main 760px）
- 絵文字未使用、★マーカーは _INTEGRATION_FRAMEWORK §3.2 規定通り
- ダークモード・印刷・モバイル対応
- favicon: esse-sense.com

## 出力先

すべて: `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-b/`

## 完成時の公開URL

- Phase B index: https://yuyanishimura0312.github.io/miratuku-news-v2/dashboards/ryoiki/phase-b/phase-b-index.html
- Phase B master-report: https://yuyanishimura0312.github.io/miratuku-news-v2/dashboards/ryoiki/phase-b/phase-b-master-report.html
- 統合インデックス（更新後）: https://yuyanishimura0312.github.io/miratuku-news-v2/dashboards/ryoiki/ryoiki-index.html

## 確認事項（着手前）

1. **本計画で実行可か** / 修正点があるか
2. **Track 投入順序**: 上記Wave 1-4の段階方式でよいか、並列度を上げるか
3. **新規DB構築**: SQLite として作成し、ryoiki配下に置くか別ディレクトリか
4. **承認後の進行**: Wave 1（Track B-1）から起動

ご承認いただけ次第、Wave 1 から順次起動します。

---

## 進捗追記（2026-05-09 14:50 JST 時点）

詳細は `_PHASE_B_STATUS.md` 参照。

| Wave | Track | 状態 |
|------|-------|------|
| 1 | B-1 多層人類史×41問 | ✅ APPROVED |
| 2 | B-2 すでにある未来 + already_future.db | ✅ APPROVED（Q-N12/Q-V05 ラベル同期済 + Phase A WARN追補済） |
| 2 | B-4 7変化検出装置×24問×168セル + initiatives.db | sentinel CONDITIONAL APPROVAL → 軽微追補中（C1+M1+M2 修正） |
| 3 | B-3 5シナリオ×30問×8 critical junctures | ✅ APPROVED（MJ-01/m1/MJ-02 ホットフィックス済） |
| 3 | B-5 hot/dead zones 弁別 | 待機（B-4 軽微追補完了後起動） |
| 4 | B-6 統合 HTML 化 + ryoiki-index 更新 | 待機（B-5 完了後起動） |

### Phase B で構築済み補助 DB

- `~/projects/research/already-future-db/already_future.db`（B-2）
- `~/projects/research/initiatives-db/initiatives.db`（B-4、463 件 initiatives）

### Wave 4 起動準備済成果物（pre-build）

- `_TRACK_B5_INPUT_TEMPLATE.md` — B-3 30問 × B-4 7装置 = 210セルマトリクス雛形
- `_TRACK_B6_STRUCTURE.md` — Phase B 統合 HTML 章立て（report 30K字 + analysis 19K字 + verification 10K字 + handoff 4K字）
- `_TRACK_B6_BRIEFING.md` — B-6 統合 HTML 化 briefing
- `_PHASE_A_INHERITANCE_AUDIT.md` — Phase A → B 数値継承監査（WARN 2件は B-2 で修正済）
- `_TRACK_B4_REFINEMENT_BRIEFING.md` — B-4 軽微追補 briefing（C1/M1/M2 対応ガイド）

### Phase B で得られた主要発見（2026-05-09 時点）

1. **B-1**: 「2030 near 真M由来 23.1% (3/13)」「Mサイン階層由来 53.8%」「3 パラダイム同時失効」（進歩・科学中立性・西洋普遍主義）
2. **B-2**: 「14 問の 92.9% が既出回答型」「Type-A/B/C 三類型 + 三大クラスター（多元的人格群／pluriverse 群／長期時間群）」
3. **B-3**: 「pluriverse 的前提を方法論レベルで実装する規範層」「critical juncture 8点のうち 4/8（厳密）/ 6/8（概念整合含む）が Phase A Mサイン領域接続」「Fragmentation シナリオ wisdom 蓄積の薄さ」
4. **B-4**: 「SG 除く 6装置が near 偏重」「規範系・概念系問いが装置応答最薄」「5補完類型のうち全装置不応答型は実体ゼロ→4類型に再構成中」
