# 経営の知的地図 ── 参考文献・引用戦略・出版計画

**対象**: 経営学教科書「経営の知的地図」（20章+付録3編、目標235,000字）  
**作成日**: 2026-05-02  
**ステータス**: Phase 1 — 章構成確定・制作準備中

---

## 1. 現状データ分析（引用情報の棚卸し）

MG DBに収録された3,458概念における書誌情報の保有状況は以下の通りである。

| フィールド | 保有数 | カバー率 |
|-----------|--------|---------|
| `origin_theorist`（提唱者名） | 2,564件 | 74.2% |
| `origin_year`（発表年） | 2,568件 | 74.3% |
| `framework_en`（出典フレームワーク英語名） | 2,592件 | 75.0% |
| `framework_ja`（出典フレームワーク日本語名） | 2,572件 | 74.4% |
| **全項目欠損**（引用情報ゼロ） | 866件 | 25.0% |

引用情報の質に関しても注意が必要である。`framework_en`フィールドは著者名と発表年の構造的な書誌情報ではなく、「Academy of Management Review 2024」「Systems Thinking + Behavioral Science」のような雑誌名・分野名の記述が混在している。完全な書誌情報（著者・タイトル・雑誌・巻号・ページ）を持つ概念は全体の1割程度にとどまると推定される。この現実を踏まえ、以下の戦略を採用する。

---

## 2. 引用スタイルの方針

### 採用スタイル：APA第7版（日本語教科書向け適用）

日本語の経営学教科書としての位置づけ、および以下の判断基準からAPA第7版を採用する。

- **対象読者との適合性**: MBA・経営大学院生・ビジネスパーソンを読者とするため、社会科学系で標準的なAPAが適切である。Chicago形式は人文学寄りで経営学では少数派。
- **入山「世界標準の経営理論」との整合性**: 同書もAPA的な文中引用（著者年方式）を採用しており、参照しやすい。
- **APA第7版の特徴**: 文中に（著者, 年）を挿入し、章末にReference Listを集約する方式。日本語著作は日本語表記を優先し、英語原著は英語表記を維持する。

### 本文中の引用形式

**文中引用（本文内に埋め込む場合）**

```
例1：Porter（1980）はファイブフォース分析を通じて...
例2：資源ベースの視点（Barney, 1991）によれば...
例3：（Kahneman & Tversky, 1979; Thaler & Sunstein, 2008）
例4：知識創造理論（野中・竹内, 1996）は...
```

**2著者の場合は毎回両名を記載**。3著者以上は初出のみ全員表記し、以降は「第一著者 et al.」を使用する。

**DB由来の定義引用**

MG DBの概念定義はAI生成テキストであり、原著からの直接引用ではない。本文中で定義を解説する際は出典を明記しつつ以下のように表現する。

```
【推奨表現】
「ダイナミック・ケイパビリティとは、急速に変化する環境に対応するため
企業の内部・外部コンピテンスを統合・構築・再配置する能力である
（Teece, Pisano & Shuen, 1997）。」

【非推奨表現】
「本書データベース内のダイナミック・ケイパビリティの定義によれば...」
（DB内部を出典として引用するのは避ける）
```

定義の学術的根拠は`origin_theorist`と`origin_year`フィールドを使って原著に紐づける。

### 脚注・章末注・巻末参考文献の構成

本書は以下の3層構造を採用する。

| 層 | 位置 | 用途 |
|----|------|------|
| **文中引用** | 本文内 | 理論・定義の出典を（著者, 年）形式で即時明示 |
| **脚注** | 各ページ下部 | 補足説明・翻訳上の注記・関連概念への言及 |
| **章末参考文献** | 各章末 | その章で引用した文献のReference List（APA7形式） |

巻末には「総合参考文献一覧（付録D）」を別途設け、全章の文献を統合・アルファベット順に掲載する。ページ数は参考文献特有の数え方で付録に含める。

---

## 3. 参考文献の自動生成戦略

### DBフィールドからの書誌情報構築ルール

MG DBには著者名と年のみが記録されており、タイトルや雑誌名は別途補完が必要である。以下の優先順位で書誌情報を構築する。

#### ルール1：完全書誌情報への変換（優先）

`origin_theorist`と`origin_year`が存在し、著者が主要研究者232名のいずれかである場合、その代表的著作から書誌情報を補完する。

```python
# 書誌情報構築ロジック（擬似コード）
def build_citation(concept):
    theorist = concept['origin_theorist']
    year = concept['origin_year']
    
    # 主要著作マッピング（手動管理テーブル）
    KNOWN_WORKS = {
        ('Michael Porter', '1980'): {
            'authors': 'Porter, M. E.',
            'title': 'Competitive Strategy: Techniques for Analyzing Industries and Competitors',
            'publisher': 'Free Press',
        },
        # ... 232研究者×主要著作
    }
    
    key = (theorist, year)
    if key in KNOWN_WORKS:
        return KNOWN_WORKS[key]  # 確定書誌
    elif theorist and year:
        return build_partial(theorist, year)  # 部分書誌
    else:
        return None  # 要手動対応
```

#### ルール2：部分書誌（著者+年のみ）

著者名と年は特定できるが原著タイトルが未確定の場合、以下の形式でプレースホルダーを使う。

```
Porter, M. E. (1985). [要確認: Competitive Advantage]. Free Press.
```

角括弧内は推定値であることを示す。出版前に全角括弧箇所をゼロにすることを品質ゲートの条件とする。

#### ルール3：論文（雑誌論文形式）

`framework_en`フィールドが「Academy of Management Review」「Journal of Finance」などの雑誌名を含む場合、論文形式で補完する。

```
Barney, J. (1991). Firm resources and sustained competitive advantage. 
  Journal of Management, 17(1), 99–120.
```

#### ルール4：全項目欠損（866件）への対処

引用情報がゼロの866概念については以下の優先対処を行う。

1. **教科書本文で中核的に扱う概念**（各章の主要30-50概念に含まれる場合）→ 手動でSemantic Scholar・Google Scholar検索し書誌情報を確定する（後述の検証プロセスを参照）
2. **補足的言及にとどまる概念**（教科書本文での登場が軽微な場合）→ 「提唱者不詳」として本文中に（提唱者不詳）と記載し、参考文献には掲載しない
3. **クラスター内で広く共有される概念**（例: クローズド・イノベーション、ハッカソン）→ 概念説明のみ行い、特定の原著への帰属を主張しない

#### 主要著作マッピングテーブル（初期版）

本書で重点扱いとなる研究者の代表著作を以下に示す。各章執筆前にこのテーブルを完成させることを前提とする。

| 研究者 | 代表著作 | 出版年 | APA書誌 |
|-------|---------|-------|---------|
| Michael Porter | Competitive Strategy | 1980 | Porter, M. E. (1980). *Competitive Strategy*. Free Press. |
| Michael Porter | Competitive Advantage | 1985 | Porter, M. E. (1985). *Competitive Advantage*. Free Press. |
| Clayton Christensen | The Innovator's Dilemma | 1997 | Christensen, C. M. (1997). *The Innovator's Dilemma*. Harvard Business School Press. |
| Daniel Kahneman | Thinking, Fast and Slow | 2011 | Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux. |
| David Teece | Dynamic Capabilities and Strategic Management | 1997 | Teece, D. J., Pisano, G., & Shuen, A. (1997). Dynamic capabilities and strategic management. *Strategic Management Journal, 18*(7), 509–533. |
| Jay Barney | Firm Resources and Sustained Competitive Advantage | 1991 | Barney, J. (1991). Firm resources and sustained competitive advantage. *Journal of Management, 17*(1), 99–120. |
| Richard Thaler & Cass Sunstein | Nudge | 2008 | Thaler, R. H., & Sunstein, C. R. (2008). *Nudge*. Yale University Press. |
| 野中郁次郎・竹内弘高 | 知識創造企業 | 1996 | 野中郁次郎・竹内弘高（1996）『知識創造企業』東洋経済新報社。 |
| Henry Mintzberg | The Nature of Managerial Work | 1973 | Mintzberg, H. (1973). *The Nature of Managerial Work*. Harper & Row. |
| Karl Weick | Sensemaking in Organizations | 1995 | Weick, K. E. (1995). *Sensemaking in Organizations*. Sage. |
| Amy Edmondson | Psychological Safety | 1999 | Edmondson, A. (1999). Psychological safety and learning behavior in work teams. *Administrative Science Quarterly, 44*(2), 350–383. |
| Saras Sarasvathy | Effectuation | 2001 | Sarasvathy, S. D. (2001). Causation and effectuation. *Academy of Management Review, 26*(2), 243–263. |
| Jensen & Meckling | Agency Theory | 1976 | Jensen, M. C., & Meckling, W. H. (1976). Theory of the firm. *Journal of Financial Economics, 3*(4), 305–360. |
| W. Chan Kim & Renée Mauborgne | Blue Ocean Strategy | 2005 | Kim, W. C., & Mauborgne, R. (2005). *Blue Ocean Strategy*. Harvard Business School Press. |

---

## 4. 学術的検証プロセス

### 検証の目的と原則

本書のMG DBはAIが生成した定義・書誌情報をベースとしている。出版前の学術的信頼性を確保するため、以下の3段階検証を実施する。**検証は執筆エージェントとは独立した別エージェント（または手動）が行い、構造的バイアスを排除する**。

### ステップ1：概念50件ランダムサンプルによる`origin_theorist`・`origin_year`検証

対象の抽出方法と手順を以下に示す。

```python
# 検証サンプル抽出スクリプト
import json, random

d = json.load(open('data/mg_consolidated.json'))
concepts = [c for c in d['concepts'] if c.get('origin_theorist') and c.get('origin_year')]
sample = random.sample(concepts, 50)

for c in sample:
    print(f"概念: {c['name_ja']}")
    print(f"  提唱者: {c['origin_theorist']}")
    print(f"  発表年: {c['origin_year']}")
    print(f"  検証URL: https://api.semanticscholar.org/graph/v1/paper/search?query={c['name_en']}")
    print()
```

各サンプルについて、Semantic Scholar APIまたはGoogle Scholarで以下を確認する。

| 確認項目 | 合格基準 |
|---------|---------|
| 提唱者名の正確性 | 苗字のスペルが一致 |
| 発表年の正確性 | ±2年以内 |
| 概念の基本的意味 | 重大な乖離がない |

**合格基準**: 50件中45件（90%）以上が合格した場合、DBの学術的信頼性を「良好」と評価し執筆を続行する。90%未満の場合はDB全体の品質見直しを検討する。

### ステップ2：重要概念20件の定義精度監査

各章の中核概念（各章の導入部・系譜図で最初に扱う概念）から20件を選定し、定義文が原著の主旨と整合するかを確認する。

| # | 概念（例） | 検証先 | 担当章 |
|---|-----------|-------|-------|
| 1 | ファイブフォース分析 | Porter (1980) | 第8章 |
| 2 | ダイナミック・ケイパビリティ | Teece et al. (1997) | 第9章 |
| 3 | 破壊的イノベーション | Christensen (1997) | 第10章 |
| 4 | プロスペクト理論 | Kahneman & Tversky (1979) | 第6章 |
| 5 | 組織文化の3層モデル | Schein (1985) | 第4章 |
| 6 | センスメイキング | Weick (1995) | 第4章 |
| 7 | 心理的安全性 | Edmondson (1999) | 第7章 |
| 8 | エフェクチュエーション | Sarasvathy (2001) | 第12章 |
| 9 | エージェンシー理論 | Jensen & Meckling (1976) | 第13章 |
| 10 | 組織的両利き経営 | O'Reilly & Tushman (2004) | 第10章 |
| 11 | コア・コンピタンス | Prahalad & Hamel (1990) | 第9章 |
| 12 | 制度的同型化 | DiMaggio & Powell (1983) | 第4章 |
| 13 | 限定合理性 | Simon (1947) | 第6章 |
| 14 | 知識創造（SECIモデル） | 野中・竹内 (1996) | 第9章 |
| 15 | ブルーオーシャン戦略 | Kim & Mauborgne (2005) | 第8章 |
| 16 | 資源ベースの視点 | Barney (1991) | 第9章 |
| 17 | 変革型リーダーシップ | Burns (1978); Bass (1985) | 第5章 |
| 18 | ナッジ理論 | Thaler & Sunstein (2008) | 第6章 |
| 19 | トヨタ生産方式 | 大野耐一 (1978) | 第15章 |
| 20 | オープンイノベーション | Chesbrough (2003) | 第10章 |

検証方法は以下の通りとする。

1. Semantic Scholar MCP（`mcp__semantic-scholar__search_papers`）で原著論文を検索する
2. 原著の要旨（Abstract）と本書の定義文を比較する
3. 重大な乖離（意味の逆転・重要な要素の欠落）がある場合はフラグを立て、定義文を修正する

### ステップ3：既存教科書との照合

以下の主要参照文献と照合し、本書の解説内容が乖離していないかを確認する。

| 文献 | 照合対象 |
|------|---------|
| 入山章栄『世界標準の経営理論』（ダイヤモンド社, 2019） | 全31理論の定義・背景 |
| 沼上幹『組織デザイン』（日経文庫, 2004） | 組織論の用語定義 |
| Porter, M. E.『競争の戦略』（ダイヤモンド社, 1982） | 競争戦略関連概念 |
| Christensen, C. M.『イノベーションのジレンマ』（翔泳社, 2001） | イノベーション関連概念 |

照合の重点は「重大な誤謬の排除」であり、解説の切り口や強調点の違いは問題としない。

---

## 5. 著作権・ライセンス方針

### 概念定義の著作権的位置づけ

本書に収録される概念定義はすべてAIが生成したオリジナルテキストであり、原著からの直接引用・複製は行っていない。したがって、定義文自体について原著者への著作権侵害は発生しない。

ただし以下の点に注意が必要である。

- **引用の必要性と誠実性**: 概念の発見・提唱は特定の研究者の知的貢献であり、出典の明記は法的義務というよりも学術的誠実性（academic integrity）の問題である。引用を省くことは著作権侵害ではないが、研究倫理として不適切である。
- **図表の利用**: 原著の図表（例: Porterのバリューチェーン図、ScheinのER図）を転載する場合は著作権者の許諾が必要である。本書では原図の「再現」ではなく、独自のD3.js可視化（概念ネットワーク図・系譜図）を使用することで転載問題を回避する。
- **引用文の扱い**: 原著からの直接引用（括弧付き引用）は、研究・教育目的の「引用の要件」（著作権法第32条）を満たす範囲内（必要最小限、出典明記、引用の従属性）で使用できる。1段落を超える長文引用は避ける。

### 知識グラフの原著性

3,458概念・5,267関係のネットワーク構造と、クラスター間分析に基づく章構成設計は本プロジェクトのオリジナルな知的産物である。

### 推奨ライセンス：CC BY-NC-SA 4.0

**Creative Commons 表示—非営利—継承 4.0 国際**を採用する。

- **BY（表示）**: 引用・転載時には著者（西村勇也 / NPO法人ミラツク）と出典URLを明記すること
- **NC（非営利）**: 商業的利用不可（教育目的・研究目的・個人利用は可）
- **SA（継承）**: 改変・再頒布する場合は同一ライセンスを適用すること

この選択の理由は以下の通りである。教育・研究コミュニティへの最大限の開放性を確保しつつ（BY+SA）、無断商用利用から組織の知的資産を保護する（NC）。なお、ミラツクが商業的パートナーシップのもとで本書コンテンツを活用する場合には、CC BYライセンスへの切り替えを協議することができる。

ライセンス表記は以下の形式でHTMLの末尾およびPDFの奥付に記載する。

```
© 2026 西村勇也 / NPO法人ミラツク
本書は CC BY-NC-SA 4.0 ライセンスのもとで公開されています。
https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ja
```

---

## 6. 出版・配布戦略

### 一次配布：GitHub Pages HTML（textbook.htmlスタイル）

**位置づけ**: 本書の主要な公開形態。オープンアクセスで誰でも無料アクセス可能。

実装仕様は以下の通りとする。

- スタイル: `textbook.html`スタイル（サイドバー目次・ダークモード・書籍レイアウト）
- CI準拠: ミラツクCI（赤 #CC1400 + 白背景、Noto Sans JP）
- 章ヘッダー: 各クラスターカラーのアクセント
- 可視化: D3.jsインタラクティブ系譜図（章ごとに埋め込み）
- ナビゲーション: 目次サイドバー（固定）、前章・次章リンク、概念索引へのジャンプ
- MG Dashboardへのリンク: 各章末に「この章の概念をデータベースで探索する →」のCTA

**ファイル構成**

```
mg-textbook/
├── index.html          # 表紙・章一覧
├── chapter-01.html     # 第1章
├── chapter-02.html     # 第2章
│   ...
├── chapter-20.html     # 第20章
├── appendix-a.html     # 付録A: 概念索引
├── appendix-b.html     # 付録B: 研究者人名録
├── appendix-c.html     # 付録C: 系譜図ガイド
├── appendix-d.html     # 付録D: 総合参考文献一覧
└── assets/
    ├── textbook.css
    └── genealogy.js    # D3.js系譜図共通ロジック
```

**デプロイ先**: `yuyanishimura0312.github.io/research-dashboard/mg-textbook/index.html`（既存Research Dashboard配下にサブディレクトリで統合）

### 二次配布：PDF（オフライン閲覧用）

Puppeteer（またはheadless Chrome）でHTMLからPDFを自動生成する。印刷適合の設定（A4縦、フォント埋め込み、ページ番号付き）を適用する。配布はGitHub ReleasesにPDFファイルをアップロードする形式とし、ダウンロードリンクをindex.htmlに設置する。

生成コマンド例:

```bash
# 全章を1つのPDFに統合（将来実装）
node scripts/generate-pdf.js --chapters all --output mg-textbook.pdf
```

### 三次配布：Notionページ（組織内共有）

ミラツク内部のNotionワークスペースに章単位でページを作成し、メンバーが検索・参照できる形で保管する。NotionページはHTMLと同期するものではなく、各章の「エグゼクティブサマリー版」（2,000〜3,000字）を別途作成する。

格納先: 「Claude code」ページ配下 → 「経営の知的地図（MG教科書）」サブページ

### ターゲット読者と配布チャネル

| 読者層 | 規模（推定） | 配布チャネル |
|-------|------------|------------|
| MBA・経営大学院生 | 数百〜数千人 | GitHub Pages URL共有、Twitterポスト |
| 経営コンサルタント・事業企画担当者 | 数千〜数万人 | SlackコミュニティへのURL共有 |
| ミラツク会員・関係者 | 200〜300人 | Notionページ、ニュースレター |
| 社会科学系研究者 | 数百人 | ResearchGate・academia.edu登録（将来検討） |
| 経営学を独学するビジネスパーソン | 不特定多数 | SEO（GitHub Pages＋README） |

### 出版形態の明確化

本書は以下の意味で「オープンアクセス・セルフパブリッシング」を採用する。

- 商業出版社との契約は行わない
- ISBN取得は行わない（デジタルファーストの方針）
- ミラツクの活動紹介・知識普及の一環として位置づける
- 将来的に紙書籍化の打診があれば、その時点でライセンス条件を再交渉する

---

## 7. 章別公開前品質保証チェックリスト

以下のチェックリストは各章の原稿が完成した後、HTMLとして公開する前に実施する。執筆エージェントとは別のエージェントまたはユーザー自身が確認することが原則である。

### A. 引用・書誌情報チェック

- [ ] 本文中に登場するすべての研究者名のスペルを確認した
- [ ] 文中引用（著者, 年）が本文中に正確に挿入されている
- [ ] 章末Reference Listに本文引用のすべての文献が掲載されている
- [ ] APA第7版の書誌フォーマットに準拠している（著者名のイニシャル、斜体のタイトル、DOI等）
- [ ] `origin_year`の値が原著発表年と一致する（±2年以内）
- [ ] 角括弧付きの推定書誌情報（`[要確認]`タグ）がゼロになっている

### B. 定義精度チェック（1章あたり5概念を抽出して実施）

- [ ] 抽出した5概念について、原著または入山（2019）との比較を実施した
- [ ] 定義文に重大な誤謬・意味の逆転がない
- [ ] AI生成定義であることが読者に誤解を招く形で隠されていない

### C. 概念カバレッジチェック

- [ ] 各章の担当概念リスト（PLAN.mdの各章仕様）と照合し、抜け落ちている主要概念がない
- [ ] 章内の概念数（30〜50概念）が目標範囲内に収まっている
- [ ] ハブ概念（組織文化、ダイナミック・ケイパビリティ等）は太字または系譜図で強調されている

### D. クロスリファレンスチェック

- [ ] 他の章への参照（「第9章参照」等）が正しい章番号を指している
- [ ] 「ブリッジ概念」の説明が、接続先の章の解説と矛盾していない
- [ ] 付録Aの概念索引にこの章で扱う主要概念が収録されている

### E. ケーススタディの事実確認

- [ ] 登場する企業・人物・数値は公知の情報に基づいている
- [ ] 特定の企業に対して根拠なく肯定的または否定的な断定をしていない
- [ ] 事例の時制（「現在〜している」vs「〜した」）が事実に整合している

### F. デザイン・技術チェック

- [ ] 系譜図（D3.js）がブラウザ上で正常に表示・動作する
- [ ] ダークモードで文字・図の視認性に問題がない
- [ ] サイドバー目次のリンクが正しいセクションに飛ぶ
- [ ] 前章・次章のナビゲーションリンクが正しい
- [ ] 画像・図のalt属性が設定されている（アクセシビリティ）

---

## 8. 書誌情報補完スクリプト（実装ガイド）

章執筆の前段階として、各章で使用する概念の書誌情報を一括補完するスクリプトを実装する。以下に設計仕様を示す。

```python
# scripts/enrich_citations.py
"""
章で使用する概念リストに対して、Semantic Scholar APIで書誌情報を補完する。
実行: python3 scripts/enrich_citations.py --chapter 8
"""

import json
import time
import requests

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"

def search_paper(author: str, year: str, concept_name: str) -> dict | None:
    """Semantic Scholarで論文を検索し、書誌情報を返す。"""
    query = f"{author} {concept_name} {year}"
    params = {
        "query": query,
        "fields": "title,authors,year,venue,externalIds",
        "limit": 3,
    }
    try:
        resp = requests.get(SEMANTIC_SCHOLAR_API, params=params, timeout=10)
        data = resp.json()
        papers = data.get("data", [])
        # 発表年が一致する最初の結果を返す
        for paper in papers:
            if paper.get("year") and abs(int(paper["year"]) - int(year)) <= 2:
                return paper
    except Exception as e:
        print(f"  Error: {e}")
    return None

def enrich_chapter_citations(chapter_concepts: list[dict]) -> list[dict]:
    """概念リストに書誌情報を付加して返す。"""
    enriched = []
    for concept in chapter_concepts:
        theorist = concept.get("origin_theorist", "")
        year = concept.get("origin_year", "")
        name_en = concept.get("name_en", "")
        
        if theorist and year and name_en:
            paper = search_paper(theorist, year, name_en)
            if paper:
                concept["verified_citation"] = {
                    "title": paper.get("title"),
                    "year": paper.get("year"),
                    "venue": paper.get("venue"),
                    "doi": paper.get("externalIds", {}).get("DOI"),
                }
            time.sleep(1)  # API rate limit
        
        enriched.append(concept)
    
    return enriched
```

このスクリプトは各章の執筆着手前に実行し、書誌情報の確認済みフラグ（`verified_citation`）を持つ概念リストを生成する。生成したリストは各章の仕様書（`chapter-XX-spec.json`）として`mg-textbook/specs/`に保存する。

---

## 9. 参考文献例（APA第7版フォーマット）

本書全体で参照される代表的な文献を、正式なAPA第7版形式で以下に例示する。執筆エージェントはこのリストを参照しながら章末Reference Listを作成する。

### 日本語文献

入山章栄（2019）．『世界標準の経営理論』ダイヤモンド社.

大野耐一（1978）．『トヨタ生産方式』ダイヤモンド社.

沼上幹（2004）．『組織デザイン』日本経済新聞社.

野中郁次郎・竹内弘高（1996）．『知識創造企業』東洋経済新報社.

### 英語文献（書籍）

Barney, J. B., & Hesterly, W. S. (2022). *Strategic management and competitive advantage: Concepts and cases* (6th ed.). Pearson.

Burns, J. M. (1978). *Leadership*. Harper & Row.

Chesbrough, H. W. (2003). *Open innovation: The new imperative for creating and profiting from technology*. Harvard Business School Press.

Christensen, C. M. (1997). *The innovator's dilemma: When new technologies cause great firms to fail*. Harvard Business School Press.

Drucker, P. F. (1954). *The practice of management*. Harper & Row.

Jensen, M. C., & Meckling, W. H. (1976). Theory of the firm: Managerial behavior, agency costs and ownership structure. *Journal of Financial Economics, 3*(4), 305–360. https://doi.org/10.1016/0304-405X(76)90026-X

Kahneman, D. (2011). *Thinking, fast and slow*. Farrar, Straus and Giroux.

Kim, W. C., & Mauborgne, R. (2005). *Blue ocean strategy: How to create uncontested market space and make the competition irrelevant*. Harvard Business School Press.

Mintzberg, H. (1979). *The structuring of organizations*. Prentice-Hall.

Porter, M. E. (1980). *Competitive strategy: Techniques for analyzing industries and competitors*. Free Press.

Porter, M. E. (1985). *Competitive advantage: Creating and sustaining superior performance*. Free Press.

Schein, E. H. (1985). *Organizational culture and leadership*. Jossey-Bass.

Simon, H. A. (1947). *Administrative behavior*. Macmillan.

Teece, D. J., Pisano, G., & Shuen, A. (1997). Dynamic capabilities and strategic management. *Strategic Management Journal, 18*(7), 509–533. https://doi.org/10.1002/(SICI)1097-0266(199708)18:7<509::AID-SMJ882>3.0.CO;2-Z

Thaler, R. H., & Sunstein, C. R. (2008). *Nudge: Improving decisions about health, wealth, and happiness*. Yale University Press.

Weick, K. E. (1995). *Sensemaking in organizations*. Sage.

---

## 改訂履歴

| 日付 | 改訂内容 |
|------|---------|
| 2026-05-02 | 初版作成（データ分析完了、全6セクション策定） |
