# 領域策定プロジェクト — チーム編成

## 全体構造

```
                    [メイン会話 = 継続オーケストレーター]
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
   [横断レイヤー]             [トラックレイヤー]        [品質レイヤー]
        │                         │                         │
   ─ 方法論                  ─ Track 1〜9              ─ 検証
   ─ 統合（Track 10）         （各5役の小チーム）       ─ 監査
   ─ 図版設計                                          ─ ゲート
```

## 横断レイヤー（クロスカット支援）

| 役割 | 担当エージェント | アウトプット |
|---|---|---|
| **方法論リード** | architect | `_PROTOCOLS.md`：ホライズン定義・テーマ分類軸・統合スキーマ・図版規格 |
| **統合リード** | knowledge-synthesizer | `_INTEGRATION_FRAMEWORK.md`：Track 10統合テンプレ・連結スキーマ |
| **図版デザインリード** | design | `_FIGURE_STANDARDS.md`：図表種別・配色・SVG規格 |
| **継続オーケストレーター** | メイン会話 | 進捗管理・Wave遷移・品質ゲート発動・差戻し判断 |

## トラックレイヤー（各トラック5役の小チーム）

| 役割 | 担当 | 責務 |
|---|---|---|
| **Lead Researcher** | general-purpose | DB探索・クエリ設計・全体統括 |
| **Data Analyst** | data-analyst | 集計実行・統計検証・カバレッジ評価 |
| **Domain Expert** | 該当DBの`/{slash-command}` | 領域知識・専門用語・解釈支援 |
| **Writer** | general-purpose | HTML執筆（analysis/report） |
| **Internal Reviewer** | reviewer | 提出前の自己検証（4カテゴリ） |

各トラック内の進行は**シーケンシャル**（1→2→3→4→5）。Lead Researcherがハブとして他役と連携。

## 品質レイヤー（独立検証・最終ゲート）

| 役割 | 担当エージェント | タイミング |
|---|---|---|
| **独立検証** | doc-verify | 各Track HTML提出直後 |
| **コードレビュー** | qa-code-reviewer | HTML構文・JS動作確認 |
| **最終ゲート（VETO）** | sentinel | doc-verify+code-review通過後 |
| **差戻し判定** | メイン会話 | 上記いずれかが不合格時、最大3ラウンド修正 |

## Wave別運用

### Wave 0（完了）
- 基盤整備：ディレクトリ・テンプレート・ブリーフィング

### Wave 0.5（並行進行：今）
- 方法論リード（architect）：プロトコル文書化
- 統合リード（knowledge-synthesizer）：Track 10フレーム
- 図版デザインリード（design）：図版規格

### Wave 1（Track 1 検証通過後）
- Tracks 2, 3, 5, 7 を**順次**着手（同時最大2まで）
- 各トラックは5役チームで構成

### Wave 2（Wave 1完了後）
- Tracks 4, 6, 8, 9
- Track 4は1〜3の結果を、Track 8は5の結果を参照可

### Wave 3
- Track 10：統合HTML化＋databases.html更新
- sentinel最終ゲート → デプロイ

## 連携プロトコル

各トラック完了時の引継ぎ書（`track{N}_handoff.md`）:
```
- 主要数値（実DB検証済）
- 強みホライズン領域
- 問うべき領域TOP10
- 他トラックとの接続点
- 既知の限界
```

統合リード（knowledge-synthesizer）はこの引継ぎ書を順次集約し、Track 10で統合レポートを構築する。

## エスカレーションルール

- doc-verifyが**Critical**判定：即時差戻し
- sentinelが**VETO**：差戻し or プロセス再設計
- 同一トラックで3ラウンド差戻し：Stage 0/1/2へ戻る判断（メイン会話が決定）
- 不確実性が高い領域：【推定】【解釈】タグで明示し、検証通過とする
