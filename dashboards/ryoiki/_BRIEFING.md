# 領域策定プロジェクト — トラック共通ブリーフィング

## プロジェクト目的
ミラツクの31+自社DBを横断的に解析し、**2030/2050/2070/2100の射程**で「未来に向けて問うべき領域」を体系的に抽出する。各DBが強みとするホライズン領域からの問いを構造化し、ミラツクとしての知見（独自知見）を確立する。

## あなた（トラック担当）のミッション
1. 担当トラックの主軸DBを集計・解析
2. 3種類のHTMLを `~/projects/apps/miratuku-news-v2/dashboards/ryoiki/` に出力
3. 完了時に総括レポート（短文）を返す

## 必須出力（3HTML/トラック）

ファイル名: `track{N}-{slug}-{kind}.html`
- `{N}`: 1-9
- `{slug}`: 短い英字スラッグ（fk-foresight, cla, megatrend, ... 各担当トラック仕様に明記）
- `{kind}`: `analysis` / `verification` / `report`

| Kind | 字数目安 | 内容 |
|---|---|---|
| analysis | 12,000-18,000字 | DB集計・主要発見の記述。クエリ結果と数値を地の文で展開 |
| verification | 5,000-8,000字 | 4カテゴリ検証: ①スナップショット不整合 ②ハルシネーション ③カバレッジギャップ ④チーム間不整合 |
| report | 8,000-12,000字 + 図表6-10点 | 最終レポート。検証結果反映済。テーマMAP・ホライズン別問い・問うべき領域TOP10必須 |

## デザイン規約（厳守）
- テンプレート: `~/projects/apps/miratuku-news-v2/dashboards/_template-akashiro.html`
- ルール: `~/.claude/rules/db-design-system.md`
- 色: 赤白CI（#CC1400メイン、#FFFFFF背景）
- フォント: Noto Serif JP本文 + Noto Sans JP UI
- 構造: top-bar + toc-sidebar + main(max-width 760px)
- ダークモード対応・印刷対応・モバイル対応
- **絵文字・アイコン未使用（厳守）**
- favicon: `https://esse-sense.com/favicon.ico`
- Back link: `← Databases` → `../databases.html`

## 共通枠組み（report.htmlに必須4要素）
1. **ホライズン×テーマMAP**: 2030/2050/2070/2100 × 各DB強みドメインのマトリクス
2. **DBが強みとするホライズン領域の宣言**: 「このDBは何年スパンの問いに最も答えられるか」+ 根拠
3. **問うべき領域TOP10**: 重要度・確からしさ・ミラツクとの親和性で評価（テーブル形式）
4. **他トラックとの接続点**: Track 10統合用フック（このトラックは他のどのトラックと連結するか）

## DB アクセス方法
- SQLite DB: `python3 ~/tools/db-agent.py query "SQL文" --db {dbid}`
- DB一覧: `python3 ~/tools/db-agent.py list`
- スキーマ: `python3 ~/tools/db-agent.py schema {dbid}`
- 専門エージェント呼出: 必要に応じてSkill経由で `/foresight-kb` `/cla` `/megatrend` 等を活用

## 引用・出典（厳格化）
- **すべての数値・固有名詞・年代は実DB検索結果に基づく。ハルシネーション厳禁**
- analysis.htmlの末尾に「DB集計ログ（付録）」セクション必須。実行したSQLクエリ・件数・抽出条件を記載
- 各章の主要主張には根拠ID（クエリ番号 or 表番号 or 出典）を本文中に明示（例: 「※集計L-3」「（表2参照）」）
- 推定・補完・解釈である箇所は **【推定】【解釈】【未検証】** タグで明示
- 限界・バイアス・カバレッジ未達領域を「研究の限界」セクションで必ず開示
- 「らしい」「と思われる」など曖昧な伝聞調を避け、根拠の有無で書き分ける

## 品質チェックリスト（提出前にあなた自身で確認）
- [ ] 全数値が DB検索結果またはソース明示済み
- [ ] DB集計ログ（クエリ・件数）を analysis.html 末尾に記載
- [ ] 推定/解釈は明示タグ付与
- [ ] 限界セクション記載
- [ ] HTML構文（タグバランス）OK
- [ ] 絵文字・アイコン未使用
- [ ] テーマ切替JS動作
- [ ] 必須4要素（report.html）含む
- [ ] verification.html で4カテゴリ検証完了

## 後工程の品質ゲート（あなたの提出後にオーケストレーターが実施）
1. `/doc-verify` による独立検証（4カテゴリ: スナップショット不整合・ハルシネーション・カバレッジギャップ・チーム間不整合）
2. `sentinel` エージェントによる Devil's Advocate 視点での最終ゲート（VETO権あり）
3. 不合格の場合、最大3ラウンドの修正サイクル

このため、提出時には「**DBに直接照会できる粒度の根拠**」が含まれていることが必須条件です。根拠不足の主張は容赦なく差戻されます。

## 完了の定義
- [ ] 3HTMLファイル出力済み
- [ ] HTML構文（タグバランス）OK
- [ ] 必須4要素を report.html に含む
- [ ] verification.html で4カテゴリ検証完了
- [ ] 絵文字・アイコン未使用
- [ ] テーマ切替JS動作

## 進捗報告
完了時、以下フォーマットで返答:
```
Track {N} 完了:
- analysis.html: {字数} / {主要発見}
- verification.html: {検証項目数} / {ハルシネーション件数}
- report.html: {字数} / {問うべき領域TOP10タイトル}
- 他トラック接続点: {Track X, Y との連結提案}
```

## 出力先
`~/projects/apps/miratuku-news-v2/dashboards/ryoiki/track{N}-{slug}-{kind}.html`
