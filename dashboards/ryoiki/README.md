# 領域策定プロジェクト（Domain Mapping Project）

ミラツクの31+自社DBを横断的に解析し、2030/2050/2070/2100の射程で「未来に向けて問うべき領域」を体系的に抽出し、ミラツクとしての知見を確立するプロジェクト。

## ファイル構成

### 横断文書（メタファイル）
| ファイル | 役割 |
|---|---|
| `_BRIEFING.md` | 全トラック共通仕様。出力フォーマット・字数・必須要素・厳守事項 |
| `_PROTOCOLS.md` | 方法論プロトコル。ホライズン定義・CTL分類軸・W/C/M評価・三系列差処理 |
| `_INTEGRATION_FRAMEWORK.md` | Track 10統合フレーム。連結マトリクス・メタテーマ抽出・知見5-7件設計 |
| `_FIGURE_STANDARDS.md` | 図版規格。6種SVGテンプレート・赤白CI準拠 |
| `_TEAM.md` | チーム編成。横断3レイヤー・トラック内5役・品質ゲート |
| `_HANDOFF_TEMPLATE.md` | トラック完了時の引継ぎ書フォーマット |
| `_TRACK_BRIEFING_TEMPLATE.md` | Track起動時のパラメタライズ済プロンプト雛形 |

### トラック別個別ブリーフィング
- `_TRACK2_CLA.md` — CLA 126年分析
- `_TRACK3_MT.md` — メガトレンド10年検証
- `_TRACK4_HISTORICAL.md` — 長期変動サイクル
- `_TRACK5_SIGNAL.md` — シグナルメタ解析
- `_TRACK6_TALENT.md` — 卓越人材×偉人×JPMS
- `_TRACK7_ACADEMIC.md` — 学術知の系譜
- `_TRACK8_TECH_AI.md` — 技術史×AI発展×加速度
- `_TRACK9_PHIL.md` — 哲学・文学・神話・伝統知

### トラック成果物（HTML×3 + 引継ぎ書）

各トラックは以下4ファイルを出力:
```
track{N}-{slug}-analysis.html         12,000-18,000字 + DB集計ログ
track{N}-{slug}-verification.html     5,000-8,000字 / 4カテゴリ検証
track{N}-{slug}-report.html           8,000-12,000字 + 図表6-10点
track{N}_handoff.md                   統合リード引継ぎ書
```

### 検証文書
- `track{N}-doc-verify-report.md` — 独立検証レポート
- `track{N}-sentinel-verdict.md` — 最終ゲート判定書

### Track 10統合
- `ryoiki-index.html` — 9トラック統合インデックス
- `ryoiki-master-report.html` — 横断メタ統合レポート

## 進行状況

| Wave | 内容 | 状態 |
|---|---|---|
| Wave 0 | 基盤整備（dir・テンプレ・ブリーフィング） | 完了 |
| Wave 0.5 | 横断3文書（PROTOCOLS／INTEGRATION／FIGURE） | 進行中 |
| Wave 1 | Track 1完了（FK）、検証完了、Sentinel判定中 | 進行中 |
| Wave 1+ | Track 2,3,5,7（Sentinel APPROVE後着手） | 待機 |
| Wave 2 | Track 4,6,8,9（Wave 1完了後着手） | 待機 |
| Wave 3 | Track 10統合＋databases.html更新 | 待機 |

## 9トラック概要

| # | テーマ | 主軸DB | スラグ | Wave |
|---|---|---|---|---|
| 1 | FK世界フォーサイト2030/50/70/2100 | FK | fk-foresight | 1 |
| 2 | CLA 126年分析と新たな物語 | CLA | cla | 1 |
| 3 | メガトレンド10年検証＋現代版18MT | MT | megatrend | 1 |
| 4 | 長期変動サイクル | SIF/HIC/GF/TA | historical | 2 |
| 5 | シグナルメタ解析 | SG | signal | 1 |
| 6 | 卓越人材×偉人×JPMS | ET/GF/JPMS | talent | 2 |
| 7 | 学術知の系譜 | Academic | academic | 1 |
| 8 | 技術史×AI発展×加速度 | TA/AI Dev/AA | tech-ai | 2 |
| 9 | 哲学・文学・神話・伝統知 | PHIL/LIT/MY/TK | good-society | 2 |
| 10 | 統合HTML＋databases.html更新 | (横断) | — | 3 |

## 公開先

完了後、`https://yuyanishimura0312.github.io/miratuku-news-v2/databases.html` の新セクション「領域策定」から各トラックHTMLにアクセス可能。
