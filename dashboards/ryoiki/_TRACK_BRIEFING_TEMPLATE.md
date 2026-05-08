# Track {N}: {タイトル} — 担当者向けブリーフィング

各トラック起動時に、本テンプレを当該トラックのスコープで埋めて、Lead Researcher（general-purpose）への指示プロンプトに同梱する。

---

## ミッション
{1〜2文の核心目的}

## 答えるべき問い
1. {問1}
2. {問2}
3. {問3}
4. {問4：強みホライズン特定}
5. {問5：問うべき領域TOP10}

## 主軸DB
- リポジトリ: `{path}`
- DB CLI: `python3 ~/tools/db-agent.py {list|schema|query|search|cross}`
- 専門エージェント: `/{slash-command}`
- 補完エージェント: `/{slash-command-2}`

## 必読
1. `_BRIEFING.md` — 共通仕様
2. `_PROTOCOLS.md` — 方法論プロトコル（ホライズン定義・分類軸・評価指標）
3. `_FIGURE_STANDARDS.md` — 図版規格・SVGテンプレ
4. `_INTEGRATION_FRAMEWORK.md` — Track 10との連結スキーマ
5. `_TEAM.md` — チーム編成
6. `_HANDOFF_TEMPLATE.md` — 完了時の引継ぎ書フォーマット
7. テンプレート: `_template-akashiro.html`
8. デザインルール: `~/.claude/rules/db-design-system.md`
9. Track 1完成版（参考）: `track1-fk-foresight-*.html`
10. Track 1検証レポート（学習用）: `track1-doc-verify-report.md`

## 内部チーム編成（5役シーケンシャル）
1. Lead Researcher（あなた=general-purpose）: DB探索・全体統括
2. Data Analyst: 集計実行・統計検証（必要に応じてSkill `/data-analyst` 起動）
3. Domain Expert: `/{slash-command}` で領域知識照会
4. Writer: HTML執筆（あなた自身が担当）
5. Internal Reviewer: 提出前自己検証

## 慎重な実行手順
1. **Phase A: 探索**（DB全体構造・schema・カバレッジ把握、実数値控え）
2. **Phase B: 集計**（ホライズン別・テーマ別SQLクエリ実行、全クエリと件数を記録）
3. **Phase C: 検証**（異なる切り口で再確認、バイアス特定）
4. **Phase D: 執筆**（analysis.html、地の文中心、根拠ID付与）
5. **Phase E: 自己検証**（verification.html、4カテゴリ）
6. **Phase F: 統合レポート**（report.html、必須4要素含む）
7. **Phase G: 引継ぎ書**（`track{N}_handoff.md`、`_HANDOFF_TEMPLATE.md`に従う）

## 出力（4ファイル）
出力先: `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/`

- `track{N}-{slug}-analysis.html` (12,000-18,000字 + DB集計ログ付録)
- `track{N}-{slug}-verification.html` (5,000-8,000字)
- `track{N}-{slug}-report.html` (8,000-12,000字 + 図表6-10点)
- `track{N}_handoff.md`（引継ぎ書）

## 厳守事項
- 全数値・固有名詞・年代は実DB検索結果に基づく（ハルシネーション厳禁）
- DB集計ログを analysis.html 末尾に記載
- 主張ごとに根拠ID（集計番号・表番号）を本文中に明示
- 【推定】【解釈】【未検証】タグ厳格使用
- 「研究の限界」セクション必須
- 曖昧な伝聞調禁止
- 絵文字・アイコン未使用
- 赤白CI（#CC1400）+ textbook.html構造厳守
- 文章は地の文中心、箇条書きだけにしない
- 図版は `_FIGURE_STANDARDS.md` の6種テンプレを使用
- ホライズン定義は `_PROTOCOLS.md` に従う

## 後工程（あなたの提出後にオーケストレーターが実施）
1. doc-verify独立検証（4カテゴリ）
2. sentinel最終ゲート（VETO権あり）
3. 不合格時は最大3ラウンド修正サイクル

## 完了報告フォーマット
```
Track {N} 完了:
- analysis.html: {字数} / {DB集計ログ数} / {主要発見3点}
- verification.html: {検証項目数} / {自己発見した問題数}
- report.html: {字数} / {問うべき領域TOP10タイトル}
- 強みホライズン領域: {年数とその根拠}
- 他トラック接続点: {Track X, Y との連結提案}
- 研究の限界（自己認識）: {主要な3点}
- 引継ぎ書パス: track{N}_handoff.md
```

時間をかけて構いません。**質>速度**です。
