# series-pq.html ビルドレポート

**ビルド日時**: 2026-05-16 12:08:04
**入力**: `toi-no-sairai/deeper.db` + `episodes/ep***.md` (100話)
**出力**:
- HTML: `dashboards/series-pq.html` (1,315,604 bytes)
- JSON: `dashboards/data/series-pq.json` (929,981 bytes)

## 10層レコード件数

| 層 | テーブル/データ | 件数 |
|---|---|---|
| 01 | series_meta | 1 (8 PART構成) |
| 02 | reference_dbs | 14 |
| 03 | episodes | 100 |
| 04 | episode_body | 100 |
| 05 | body_citations | 844 |
| 06 | deeper_body | 100 |
| 07 | deeper_citations | 493 |
| 08 | key_references | 442 |
| 09 | episode_relations | 143 |
| 10 | cross_series_relations | 25 |

## 統計

- 本文総字数: 196,814（平均 1968 / 話）
- 本文平均段落数: 13.0
- 本文引用抽出: 844 件
- DEEPER総字数: 103,699
- DEEPER引用: 493 件
- DEEPERユニーク著者: 370
- 非西洋＋比較率: 14.4%
- key_references: 442 件
- episode_relations: total 143 / strong 0 / moderate 11 / shared 132

## 10セクション構成

1. メイントピック (series_meta + 螺旋SVG + PARTS表)
2. 参考DB構成 (14 カード + 中心放射ネットワークSVG)
3. 各回タイトル・コンセプト (8 PART 折りたたみ + 検索 + フィルタ)
4. 各回本文（要約） (100話のサマリー + 全文リンク)
5. 本文の学術知 (誰がいつ何を / ページネーション付き)
6. 各回 DEEPER (3要素別表示 / 検索可能)
7. DEEPER 学術知 (493 件 / 分野×文化圏チャート / フィルタ)
8. 典拠情報 (Top10ランキング + 全442件テーブル)
9. 各回相互関係 (D3 force-directed network + Strong/Moderate表)
10. 連載外全体像 (kurashi/henka/futures/futures2 マトリクス)

## デザイン適合

- 赤白CI: #CC1400 アクセント / 白基調
- textbook.html style: top-bar 48px + サイドバーTOC + 中央コラム
- Noto Sans JP + Noto Serif JP
- ダーク/ライト切替実装 (localStorage 永続)
- レスポンシブ: 1024 / 768 / 480 ブレイクポイント
- 印刷時非表示: top-bar / sidebar / filter / pagination

## 公開URL

https://yuyanishimura0312.github.io/miratuku-news-v2/dashboards/series-pq.html
