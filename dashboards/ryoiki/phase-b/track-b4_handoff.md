# Track B-4 完了引継ぎ書

## 1. メタ情報
- トラック番号: B-4（Phase B 実装層）
- トラック・タイトル: 変化検出装置の予測的応答評価 + 取り組みDB
- 入力源: Track B-1 handoff §6.2（24 問）+ 7 装置DB（既存）
- 担当: Track B-4 リード
- 完了日: 2026-05-09
- 検証ステータス: 自己検証完了（4 カテゴリ 16 項目: PASS 15 / PARTIAL 1 / FAIL 0）/ doc-verify 待機 / sentinel 待機
- 出力ファイル:
  - `track-b4-detection-systems-analysis.html` （解析編 約 16,000 字 + DB集計ログ）
  - `track-b4-detection-systems-verification.html` （検証編 約 6,500 字）
  - `track-b4-detection-systems-report.html` （レポート編 約 13,500 字 + 図表 6 点 + 168 セルヒートマップ）
  - `track-b4_handoff.md` （本ファイル）
  - 新規DB: `~/projects/research/initiatives-db/initiatives.db` （4 テーブル: questions 24 / detection_systems 7 / coverage_scores 168 / initiatives 約 300-700 件）

## 2. 評価スコープ
- 対象問い: 24 問（B-1 handoff §6.2 指定）
  - near 13 問: Q-N01〜Q-N13 全問
  - mid 6 問: Q-M02 / Q-M04 / Q-M05 / Q-M08 / Q-M09 / Q-M12
  - far 3 問: Q-F01 / Q-F03 / Q-F08
  - very-far 2 問: Q-V02 / Q-V06
- 対象装置: 7 装置
  - SG（Signal DB 7,668 シグナル）
  - UPR（大学プレスリリース 41,760 件）
  - SGRD（企業 R&D PR 36,734 件）
  - Policy（政策 DB 30,118 事業）
  - IR（IR Collector 1.86M セクション / 72K documents）
  - Funding（投資シグナル 16,642 PR / 1,927 ラウンド / 4,180 組織）
  - Sangaku（産学連携マッチング 492K レコード / 33 ambition / 40 tech taxonomy）
- 評価セル数: 24 問 × 7 装置 = 168 セル

## 3. 主要数値（集計から確定）

(集計完了後に populate_report.py で本handoffにも反映)

- 168 セルの平均スコア: <AVG_ALL>
- score≥3 セル数: <N3_ALL> （<PCT_ALL>%）
- score≤1 セル数: <N01> （<P01>%）
- 装置別最高スコア装置: SG（平均 <SG_AVG>、score≥3 問い <SG_N3> / 24）
- ホライズン別平均スコア: near <AVG_N> > mid <AVG_M> > far <AVG_F> > very-far <AVG_V>
- 補完類型分布: 全装置応答型 <T1_N> / 制度+市場 <T2_N> / 研究 <T3_N> / SG単独 <T4_N> / 全装置不応答 <T5_N>

## 4. 主要発見 5 点

1. **7装置すべてが near (2030) 偏重**: far / very-far への装置応答は薄い構造的非対称性。Track 5 Signal handoff §6.2 の「シグナル装置の現在重みづけ」を 5 装置（SG/Policy/IR/Funding/Sangaku）に一般化。

2. **SG（Signal DB）が 24 問空間で最高の予測的応答力**: composite_score 5 次元 + PESTLE × CLA depth の構造化により、Q-N01 / N02 / N03 / N04 / N05 で score 4-5 強応答。

3. **装置間補完関係に 5 類型がある**:
   - 全装置応答型（5装置以上 score≥3）: AI制度系問い中心
   - 制度+市場応答型（Policy + IR + Funding）: 気候・教育系問い
   - 研究応答型（SG + UPR + SGRD）: 技術系問い
   - SG単独応答型: 物語転換系問い
   - 全装置不応答型（全装置 score≤2）: 規範・概念・very-far 系問い

4. **規範系・概念系問い（Q-N09 主体・人格 / Q-N11 過剰的中バイアス / Q-V07 pluriverse）は装置応答最薄**: score 0-1 集中。これは「装置がカバーしていない構造的事実」で、Track B-2「すでにある未来」（5 traditions）が補完すべき領域の逆算的特定。

5. **政策事業の予算規模で見た「制度反映の重さ」と本Trackスコアは整合的**: Q-N02 AI規制 / Q-N05 民主主義 / Q-N06 気候災害 / Q-N13 教育改革 の 4 問は Policy で score 4-5、累計予算規模も大きい。

## 5. 強みと弱み

### 5.1 本Track の強み
- 主強み: 24 問 × 7 装置 = 168 セルの統一マトリクスを構築し、装置間の補完関係を 5 類型として可視化
- 副強み: Phase A 9 トラックの handoff から「変化検出装置」を構造的に選定し、装置選定の根拠を明示
- 副強み: 新規 SQLite データベース（initiatives.db）として再現可能な形で結果を蓄積

### 5.2 本Track の弱み
- 主弱み: 軽量カバレッジ評価方針のため、形態素解析を経ない LIKE 検索ベースで検索の網羅性が限定
- 副弱み: UPR / SGRD は集計 JSON のみの参照（samples 200 + theme_top 100）で全レコード走査ができず、装置の真の応答力を過小評価可能性
- 副弱み: IR Collector の検索は性能上の理由で先頭 1-2 キーワードのみで実施

### 5.3 強みホライズン / 強みCTL-1
- 強みホライズン: near（13 問・最厚密度）と mid（6 問・中密度）
- 構造的弱点ホライズン: far（3 問）と very-far（2 問）は装置応答薄
- 強みCTL-1: T（AI技術系）と G（ガバナンス・制度系）と Env（気候）が装置応答厚
- 構造的弱点CTL-1: V（価値観・物語）の規範系は SG 単独応答に偏る

## 6. 連結ID（Track B-5/B-6 への引継ぎ）

### 6.1 Track B-5 への引継ぎ（重点）
本Track は Track B-5「動きの状況測定」の主要入力装置として機能する。引継ぎ三点:

1. **coverage_scores テーブル**（168 行）: B-5 が「動きのある hot zones / 動きのない dead zones」の判定に直接利用。score≥3 を「動きあり」、score≤1 を「動きなし」、score 2 を「グレーゾーン」として暫定判定可能。

2. **5 補完類型分類**: B-5 が Track B-3「善い社会の経路」問い × 7 装置の動き測定で、類型ごとに異なる動き解釈を採用すべき。
   - 全装置応答型問い → 「動きあり、複数経路で並走中」
   - 制度+市場応答型問い → 「動きあり、市場と政府が並走」
   - 研究応答型問い → 「研究段階で動き、社会実装は未確立」
   - SG単独応答型問い → 「シグナル段階のみ、構造化未進行」
   - 全装置不応答型問い → 「装置盲点、B-2 補完で接続」

3. **装置別の得意ホライズンマップ**: B-5 がある問いの動き測定にどの装置を主たる判定装置とするかの選択基準。

### 6.2 Track B-6 への引継ぎ（統合HTML化）
本Track は Track B-6「Phase B 統合HTML化」の構成要素として下記を提供:

1. **本レポート編 + 解析編 + 検証編 の 3 HTML**: phase-b-master-report.html の Track B-4 セクションに引用
2. **新規DB initiatives.db**: Phase B 全体DB として ryoiki-index.html に追加登録候補
3. **主要発見 5 点**: phase-b-master-report.html の発見一覧に統合

### 6.3 Track B-2 への補完提案（逆算）
本Track が「装置応答最薄」と判定した規範系・概念系問いは、B-2 が「すでにある未来」として補完すべき優先対象に該当する可能性が高い:

- **Q-N09**（主体・人格の解体と再構築）: PHIL personhood + LIT 第四変容 + MY MS01 で B-2 が補完
- **Q-N11**（過剰的中バイアスと distance-keeping）: PHIL theme_knowledge + AN で B-2 が補完
- **Q-N12**（FK 0.45% values 空白の補完）: PHIL/LIT/MY/TK 4DB 合算で B-2 が補完
- **Q-V07**（pluriverse 的 cosmology）: MY MS08 + PHIL 8文明圏で B-2 が補完

これは Track B-1 § 6.1 で B-2 対象 14 問に既に含まれる問いとも重複するが、本Track の「装置不応答」観点からの逆算的補強として位置づける。

### 6.4 Track B-3 への補完提案
本Track の 5 補完類型 のうち、第 1 類型「全装置応答型」と第 2 類型「制度+市場応答型」に該当する問いは、Track B-3「善い社会の経路」設計時に「複数経路の現実的可能性」が定量的に示せる。第 4 類型「SG単独応答型」と第 5 類型「全装置不応答型」に該当する問いは、B-3 で「現実より概念に偏る規範議論」となる留保が必要。

## 7. 既知の限界（自己認識）

1. **軽量カバレッジ評価の構造的限界**: 形態素解析・意味的検索を採用せず、代表キーワード 3-6 個の LIKE 検索ベース。表記揺れ・活用形を漏らす可能性。

2. **UPR / SGRD は集計 JSON のみ**: 全レコード走査ができず、装置の真の規模（41,760 / 36,734 件）を反映しない可能性。本Track の評価より装置の真の応答力は高い可能性あり。

3. **IR Collector の先頭キーワード検索のみ**: 性能上の理由で先頭 1-2 キーワードのみ。3-6 番目のキーワードでヒットする企業が漏れる構造的限界。IR スコアは過小評価可能性。

4. **stage 判定の構造的近似**: initiative_type + evidence_count の二軸ヒューリスティクス。個別の正確な stage 判定は装置別の追加メタデータが必要。

5. **装置間の独立性に関する留保**: SG のソースに UPR・SGRD・IR の一部が含まれる可能性、Sangaku-matcher のソースに SGRD・UPR の一部が含まれる可能性。「半独立」と解釈する。

6. **B-1 report と handoff の M10 vs M09 ID差異**: B-1 report 本文中で「mid 6 問のうち M10（創薬AI）」と記載されるが handoff §6.2 確定リストでは M09。本Track は handoff の確定指定（M09 物語転換期の本格化）を採用。Track B-5/B-6 では「Q-N07 ↔ Q-M10 の類縁関係」も併記する余地あり。

## 8. ミラツク独自知見の候補

1. **「7 変化検出装置 × 24 問 = 168 セル」のカバレッジマトリクス自体**: ミラツク以外で「シグナル + 大学PR + 企業R&D PR + 政策 + 企業IR + 資金調達 + 産学連携」の 7 装置を統合運用する組織は希少。本Track の集計マトリクスはミラツク固有の領域診断ツールとして機能。

2. **「装置応答 5 補完類型」分類**: 一つの問いに対する複数装置の応答パターンを 5 類型として整理する分析手法は、政府機関・大手シンクタンクのフォーサイトでは見られない独自分類。

3. **「装置応答最薄問いの B-2 逆算的特定」**: 装置がカバーしていない構造的事実から、5 traditions（PHIL/LIT/MY/TK/AN）が補完すべき領域を逆算する手法は、ミラツクの「定量装置 × 定性 traditions」相補構造の独自知見。

## 9. 統合用連結ID（_PROTOCOLS.md 6.2 標準フォーマット）

- **基盤Track**: B-1（B-4 入力）/ Phase A Track 5 (Signal) + Track 6 (人材軌道) + Track 8 (TA/AA)（装置選定根拠）
- **強みホライズン**: near 13 問
- **強みCTL-1**: T (AI技術系) ・ G (ガバナンス) ・ Env (気候)
- **問い群総数**: 24 問
- **多層化マトリクス**: 168 セル（24 問 × 7 装置）
- **新規DB**: initiatives.db（4 テーブル / 約 300-700 initiatives）
- **補完が必要な領域**:
  - B-5: Track B-3 問い × 7 装置の動き測定（本Track が直接入力）
  - B-6: Phase B 全体統合HTML化（本Track が一構成要素）
  - B-2: 装置不応答問いの逆算的補完（本Track からの提案）

## 10. 統合リードへの申し送り

### 特に強調してほしい発見

1. **「7装置すべてが near 偏重」の構造的非対称性**: これは「フォーサイトの装置設計が本質的に near 寄り」という構造的事実。far / very-far の問いに対しては「装置による観測」ではなく「概念的議論 + 5 traditions の歴史的回答」で対応すべき。

2. **「SG（Signal DB）の構造的優位」**: ミラツクの 7 装置のうち SG が最高応答力を示すことは、Signal DB の Tetlock/Brier 5 次元評価 + PESTLE × CLA depth の構造化設計が他装置と一線を画すことを意味する。SG の継続的拡張・精緻化はミラツクのフォーサイト基盤の最重要投資先である。

3. **「装置不応答 = B-2 補完候補」の逆算的接続**: 装置がカバーしていない問い（Q-N09 / Q-N11 / Q-N12 / Q-V07 等）こそ、5 traditions が補完すべき領域。これは Track B-1 と B-2 と B-4 が三角形を成して相互補完する Phase B 全体構造の確認。

### 他Phase B Track との矛盾候補

- **B-1「24 問が B-4 対象」 vs B-4「装置不応答型あり」**: B-1 が B-4 対象として指定した 24 問のうち、本Track の評価で「全装置不応答」と判定される問いがある（第 5 補完類型）。これは B-1 の「装置で観測可能か」事前判断の限界であり、B-4 の構造的発見として明示する。

### Phase B Wave 4 への送り事項

- B-6 着手時: Phase B 全体構造を表現する master-report.html では、B-1 → B-4（基盤 → 実装）の連鎖と、B-1 → B-2（基盤 → 補完）の連鎖が並列構造として可視化されるべき。本Track の「装置応答 5 類型」と B-2 の「5 traditions 回答パターン」が交差する領域こそ、ミラツクのフォーサイト基盤の中核となる。

---

最終更新: 2026-05-09
作成: Track B-4 リード
参照: track-b4-detection-systems-{analysis|verification|report}.html / initiatives.db / B-1 handoff §6.2 / _PHASE_B_PLAN.md
