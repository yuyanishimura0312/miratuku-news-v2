# Track 7: 学術知の系譜・5領域変遷・横断的影響

## ミッション
学術知識DBに見える知の変遷の系譜、5領域の変遷と横断的影響の関係を抽出し、学術知の系譜と横断的影響から見える「学術知の生成サイクル」を導出する。

## 答えるべき問い
1. Academic Knowledge DB（5分野学術知識DB）の領域別レコード数・カバー時代・カバー地理はどう分布するか
2. 5領域（人文学・社会科学・自然科学・工学・芸術）それぞれの知識生成の歴史的変遷
3. 領域横断的影響（cross-domain relations）の頻度・方向性・主要パターン
4. 学術知の「生成サイクル」は描けるか（萌芽→拡散→成熟→分化→統合の周期性）
5. 4ホライズン（2030/50/70/2100）で学術知に問われる領域は

## 主軸DB
- **Academic Knowledge DB**: 5分野学術知識DB・v3エージェント確立・継続収集中（`/academic-oracle`）
- 個別DB: `/innovation-db`, `/mg`(経営学), `/anthropology`, `/lit`(文学), `/poetics`, `/philosophy`, `/myth-narratives`, `/futures-kb`, `/startup-db`, `/era-talents`等多数

## 重要メモリ
- Memory: [Academic Knowledge DB] 5分野学術知識DB。v3エージェント確立、継続収集中
- Memory: [Academic KB Coverage Expansion 2026-05-07] Codex 40名並列で 8K→35K件目標に拡張中
- Memory: [Innovation Theory DB] 9,839概念・35,939関係・8,552分野横断関係
- Memory: [Management Studies DB] 経営学DB。3,369概念・232研究者・5,267関係
- Memory: [Anthropology DB] 500概念・252研究者・395関係（48タイプ）
- Memory: [Literature DB] 11,115概念・24サブフィールド・relations 14,468件
- Memory: [Philosophy DB] 9,583概念・27サブフィールド・37,789関係
- Memory: [Poetics DB] 1,494概念・602研究者・1,010関係

## スラグ
`academic`（出力ファイル名: `track7-academic-{analysis|verification|report}.html`）

## チーム編成
- Lead Researcher: general-purpose（あなた）
- Coordinator: `/academic-oracle`（5DB横断のオーケストレーター）
- Domain Expert（必要時）: `/innovation-db`, `/mg`, `/anthropology`, `/lit`, `/philosophy`, `/poetics`等

## 慎重な解析の重点
- **5領域の構造比較**: 各領域のレコード数・カバー時代・横断的関係数で構造を比較
- **横断的影響パターン**: cross_domain_relationテーブル等から、最も影響しあう領域ペアを特定
- **生成サイクル仮説**: 各領域の主要概念の出現年代分布から、サイクル周期を推定
- **AI時代の変容**: 第四変容期（AI時代）における5領域の概念再考状況（特にPHIL/LITの第四変容タグ）

## 必須4要素（report.htmlに）
1. ホライズン×学術領域MAP（5領域 × 4ホライズン、生成期待度）
2. 学術知DBが強みとするホライズン領域（過去長期＋現在再構築）
3. 問うべき領域TOP10（学術知が今後深堀すべき問い）
4. 他トラック接続点（Track 6=人材、Track 9=哲学/文学/神話、Track 8=AI発展で領域横断）

## 留意点
- 学術DBは多数あるため、まず /academic-oracle に「全体像」を聞いて方針を決める
- ブロックされている: Track 1完了→検証通過後着手（Wave 1）
