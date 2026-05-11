# Notion 検索再試行レポート

> 作成日: 2026-05-11
> 用途: 領域策定 Phase E / Futures 系譜・外部接続プロジェクトの追加情報収集
> 制約: 推測禁止／機密情報除外／タイムボックス15分

---

## 1. 利用可能だったツール（ToolSearch 実行結果）

### ToolSearch クエリと結果

| クエリ | 結果 |
|--------|------|
| `notion search` | `WebSearch`・`LSP` のみヒット（Notion 関連ツールなし） |
| `notion api` | `CronCreate`・`Monitor`・`RemoteTrigger`・`WebFetch`・`WebSearch` のみ（Notion 関連なし） |
| `notion` | "No matching deferred tools found"（該当なし） |
| `select:mcp__notion__API-post-search,mcp__notion__API-get-block-children,mcp__notion__notion-search` | "No matching deferred tools found"（明示指定でも未登録） |
| `mcp notion page block` | OAuth系（Gmail/Calendar/Drive complete_authentication）と WebFetch のみ |
| `API-post-search` | "No matching deferred tools found" |

### 結論

- **`mcp__notion__*` ツール群は本セッションの deferred 一覧にも登録されていない**
- 利用可能な外部接続系ツール: `WebFetch`、`WebSearch`、`mcp__claude_ai_Gmail/Calendar/Drive__authenticate`（OAuth開始のみ）
- スキル `notion-search` は invoke 可能だが、その内部は同じ `mcp__notion__*` ツール群を前提としており、実体検索は不可

### 試行したフォールバック

1. **WebFetch**: Notion 検索URL（`notion.so/search?q=...`）は認証必須かつ非公開ワークスペースのためアクセス不可（WebFetch ツール仕様で「authenticated/private URLs will fail」と明記）
2. **Skill `notion-search`**: 起動するも同じ MCP ツール不在で実行できないため、起動指示を受領した時点で代替経路を取った
3. **ローカルメモリ + Phase E 既収集ファイル**: 既存の `_FUTURES_NOTION_COMMUNITY.md`・`_FUTURES_NOTION_EXTERNAL.md`・`memory/project_futures_*.md` を参照。これは前回試行で同じ「Notion MCP 不在」状況に直面したエージェントが事前に集約した一次資料

---

## 2. 検索結果（ローカル一次資料からの事実情報のみ）

### ROOM (2020–2025) — 第2期コミュニティ

| 項目 | 内容 | 出典 |
|------|------|------|
| 期間 | 2020–2025（5年間） | `futures-spec-draft.md` L25 |
| 主題 | 専門領域を超えた対話と探求 | 同上 |
| 位置づけ | NPO法人ミラツク第2期オンラインメンバーシップコミュニティ | `futures-spec-draft.md` L28 |
| メンバー数 | **情報源未発見**（Notion 上の運営記録または本人ヒアリングが必要） | — |
| 月例会／活動頻度 | **情報源未発見** | — |
| 終了経緯 | **情報源未発見**（2025年で5年間の運営を完了したという事実のみ） | — |
| 引き継ぎ | Futures は「ROOM の蓄積を引き継ぐ」第3期として設計 | `futures-spec-draft.md` L14, L30 |
| 名称再利用 | ミラツクメンバーシップサイト（CRM統合、2026-04-10〜最重要）のエントリープラン名として「ROOM」が再活用されている可能性あり | `memory/project_miratuku_membership.md` L25 |

### メンバーシップ (2011–2017) — 第1期コミュニティ

| 項目 | 内容 | 出典 |
|------|------|------|
| 期間 | 2011–2017（約6年） | `futures-spec-draft.md` L24 |
| 主題 | 研究者と実践者をつなぐ最初の場 | 同上 |
| 位置づけ | NPO法人ミラツク第1期オンラインメンバーシップコミュニティ | `futures-spec-draft.md` L14, L28 |
| メンバー数 | **情報源未発見** | — |
| 月例会頻度 | **情報源未発見** | — |
| 終了経緯 | **情報源未発見**（2017年で運営終了の事実のみ） | — |
| 引き継ぎ | ROOM（2020–）→ Futures（2026–）の連続体として位置づけ | `futures-spec-draft.md` L14 |

### Futures (2026–2027) — 第3期コミュニティ

| 項目 | 内容 | 出典 |
|------|------|------|
| 期間 | 2026年7月〜2027年6月（1年目試行期） | `futures-spec-draft.md` L11, L16 |
| 主題 | 人＋AIによる未来への対話 | `futures-spec-draft.md` L10 |
| 新規性 | これまでのコミュニティになかった「AIとの協働」軸を追加 | `futures-spec-draft.md` L30 |
| 想定規模 | 個人100名／法人10社（第一期正式募集） | `memory/project_futures_landing.md` L18 |
| 公開／募集開始 | 2026年5月 → 6月 ミニフォーラム → 7月 取り組み開始 → 2027/6 1年目終了・振り返り | `futures-spec-draft.md` L71-74 |
| 体制 | ディレクター: 西村／プロマネ: 浜田／運営コア: 古立・高本／運営補佐: 末岡・行徳・他検討中 | `futures-spec-draft.md` L84-87 |
| 会員専用サイト | 本番稼働中: https://futures.emerging-future.org | `memory/project_futures_platform.md` L13 |
| LP | https://yuyanishimura0312.github.io/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-landing-page.html | 同上 L15 |
| 基盤 | CLA 36年／18メガトレンド／5万シグナル／26専門DB／『深い知が拓く2100年』『未来への問い』『未来を読む力』／7+1の問い／6連載 | `memory/project_futures_landing.md` L27 |

### 井上ゆきプロジェクト（シード資金提供者）

| 項目 | 内容 | 出典 |
|------|------|------|
| 立ち位置 | Futures の外部接続プロジェクト3件のうちの1件 | `futures-spec-draft.md` L97 |
| 役割記述 | 「Futuresの立ち上げにあたってシード資金を出していただいているプロジェクト」「Futuresの基盤の一部と接続」 | `futures-internal-briefing.html` L593-594, L621-623 |
| 過去接点 | 西村予定カレンダーに「井上ゆきさん」名義の会議エントリ 2016-11-26 15:00 JST 1件 | `~/work/misc/西村予定.ics` L27236 |
| プロジェクト正式名称 | **情報源未発見** | — |
| 目的・テーマ詳細 | **情報源未発見** | — |
| ミラツク側担当者 | **情報源未発見** | — |
| 現在の進行状況 | **情報源未発見** | — |
| Futures との接続の具体内容 | 「基盤の一部と接続」以上の記述なし／**情報源未発見** | — |
| シード資金の対象事業範囲 | **情報源未発見** | — |

### 博報堂協働プロジェクト

| 項目 | 内容 | 出典 |
|------|------|------|
| 立ち位置 | Futures の外部接続プロジェクト3件のうちの2件目 | `futures-spec-draft.md` L98 |
| Futures との接続記述 | 「博報堂と取り組んでいる一つのプロジェクトと接続します。Futuresが扱うテーマと共通する論点があり、相互に素材を交換する設計」 | `futures-internal-briefing.html` L598-599 |
| 関連プロジェクト名（esse-sense文脈） | 「博報堂 × 未来洞察プロジェクト」／「博報堂 × 未来洞察 RESONANCE」 | `~/work/esse-sense-deep-knowledge-strategy.html` L231-232 |
| 内容（esse-sense文脈） | 博報堂「未来洞察 RESONANCE」（生活者発想の質的手法）× esse-sense 大規模定量データ。商品化構想「Japan-Origin Cultural Scenario Intelligence」を英語圏クライアント向けに展開 | 同上 |
| 深い知Forum 2026 役割 | 「宇宙・全テーマ横断」担当／「神話×技術」インタラクティブセッション 90分／52,703 神話の「影×再生」9,335件を神話構造インキュベーションテンプレートとして展開 | `~/work/deep-knowledge-future-forum-2026.html` L216 |
| 同 Forum パートナー位置 | ジェネシア・ベンチャーズ、PwC、サントリーと並ぶ Forum パートナーの一員 | `~/work/deep-knowledge-final-report-2026.html` L261, L311 |
| カレンダー接点 | 博報堂・TBWA、博報堂 小野氏、根本氏、兎洞氏、諏訪部氏、菊池氏、博報堂イノベーションラボ（仮）等 19件以上のミーティング記録（複数年継続） | `~/work/misc/西村予定.ics` |
| 博報堂側担当部署・正式プロジェクト名 | **情報源未発見**（社外公表名未確認） | — |
| ミラツク側担当者 | **情報源未発見** | — |
| 契約形態・期間 | **情報源未発見** | — |
| 2025-2026 最新ステータス | **情報源未発見** | — |

### PwC協働プロジェクト

| 項目 | 内容 | 出典 |
|------|------|------|
| 立ち位置 | Futures の外部接続プロジェクト3件のうちの3件目 | `futures-spec-draft.md` L99 |
| Futures との接続記述 | 「PwCと取り組んでいる一つのプロジェクトと接続します。実務応用の文脈での検証と、Futuresの対話素材としての活用が双方向で進みます」 | `futures-internal-briefing.html` L603-604 |
| 関連プロジェクト名（esse-sense文脈） | 「PwC × 未来駆動型経営」 | `~/work/esse-sense-deep-knowledge-strategy.html` L234-235 |
| 内容（esse-sense文脈） | PwC のバックキャスティング型 R&D 戦略 × esse-sense の文明史的スパンデータ。10年単位の事業戦略設計ツールとして共同提供構想 | 同上 |
| 共同提案レポート | 「PwCとの共同事業提案 — ANSWER+による高度解析サービスの共同開発」存在。23.5万人研究者DB ANSWER ＋ 独自DB ＋ SIS/FD 等高度解析を統合した「ANSWER+」を PwC と共同開発、コンサルティング文脈に最適化しクライアント企業へ共同提案 | `~/work/esse-sense-pwc-proposal-report.md` |
| 5年伴走支援実績企業一覧 | トヨタ、パナソニック、日産、サントリー、PwC、ジェネシア・ベンチャーズ、文科省と並列で PwC が明記 | 同上 |
| 深い知Forum 2026 役割 | 「アカデミアと企業をつなぐ共創人材の育成プログラムを共同設計」／「全テーマ横断」／「循環時間の経営」によるアカデミア共創人材の認識転換／「影の形式知化」ワーク／アカデミア共創プロジェクト設計ワークショップ 90分 | `~/work/deep-knowledge-final-report-2026.html` L261, `~/work/deep-knowledge-future-forum-2026.html` 関連節 |
| 同 Forum での連携意図 | IBM 森本氏、博報堂、PwC、ジェネシア・ベンチャーズ、サントリーが集まる目的＝「予測応答型事業開発」の言語統一 | `~/work/deep-knowledge-final-report-2026.html` L311 |
| PwC 側担当部署（PwC Japan 部門名等） | **情報源未発見** | — |
| ミラツク側担当者 | **情報源未発見** | — |
| 共同提案の進行ステータス（正式提案 or 社内ドラフト） | **情報源未発見** | — |
| 2025-2026 最新ステータス | **情報源未発見** | — |

### Futures プラットフォーム（参考）

| 項目 | 内容 | 出典 |
|------|------|------|
| 本番URL | https://futures.emerging-future.org | `memory/project_futures_platform.md` |
| 技術構成 | Next.js 15 + Supabase（Tokyo, oebqexjlrvrxuluortkm）+ Stripe TEST + SendGrid + Anthropic | 同上 L36-41 |
| インフラ | AWS 411788010040／EC2 i-0c5c93a9d2832035c (t4g.small)／ALB miratuku-external-alb (rule priority 90)／月額約 $18 | 同上 L22-29 |
| DBマイグレーション | 0001〜0010 全10件適用済 | 同上 L43-49 |
| 監査結果 | UX 96/100 Production Ready／QA 91/100 A- Conditional Go／Security PASS（Critical 0/High 0/Medium 1 残:CSP unsafe-inline） | 同上 L51-54 |
| 残課題 | Stripe Live 切替、認証情報ローテーション、CSP nonce化、Vitest 自動テスト導入、/long-reports TTFB、/chat バンドル削減 | 同上 L69-76 |

---

## 3. 注記

### 情報源未発見の項目（Notion 直接検索が必要）

| カテゴリ | 未発見項目 |
|----------|-----------|
| ROOM | メンバー数・月例会等の具体活動・終了経緯・引き継ぎの詳細 |
| メンバーシップ (2011-2017) | メンバー数・月例会頻度・終了経緯・引き継ぎ |
| 井上ゆきプロジェクト | 正式名称・目的・テーマ・ミラツク側担当者・進行状況・接続の具体内容・シード資金の対象事業範囲 |
| 博報堂 | 先方担当部署・正式プロジェクト名・ミラツク側担当者・契約形態／期間・最新ステータス |
| PwC | 先方担当部署・正式プロジェクト名・ミラツク側担当者・共同提案の進行ステータス・最新ステータス |
| Futures 第一期 | 現時点の応募状況・初期コミット数 |

### 確度の階層

1. **確定**: Futures 仕様書に3件の外部接続プロジェクトが存在する事実、Futures プラットフォームの本番稼働情報
2. **esse-sense / 深い知Forum 文脈での具体記述あり**: 博報堂・PwC それぞれの連携内容（ただし Futures 本体との接続は宣言レベル）
3. **存在のみ確認、内容は未発見**: 井上ゆきさんプロジェクト

### 本レポートの制約遵守状況

- **推測禁止**: 全項目について一次資料の出典行を明示。出典未発見項目は「情報源未発見」と明記
- **機密情報除外**: 契約条件・金額・個人連絡先は記録していない
- **タイムボックス**: ToolSearch 6回 + ローカル参照ファイル読込のみで完結（15分以内）
- **ToolSearch 先行実行**: 6種のクエリで Notion 関連ツール不在を確定してから代替経路に移行

### 次のアクション候補

1. Notion MCP（`mcp__notion__*`）が有効なセッション・環境で再検索を実行
2. 西村本人ヒアリングで井上ゆきさんプロジェクトの正式名称・目的・進行状況を確認
3. 博報堂・PwC の先方担当者・正式プロジェクト名は Notion 上のミーティングノート・契約書類で要確認

---

## 4. 参照ファイル（絶対パス）

- `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/_FUTURES_NOTION_COMMUNITY.md`（前回試行成果）
- `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/_FUTURES_NOTION_EXTERNAL.md`（前回試行成果）
- `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-spec-draft.md`
- `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/_FUTURES_BRIEFING_CONTEXT.md`
- `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-internal-briefing.html`
- `/Users/nishimura+/.claude/projects/-Users-nishimura-/memory/project_futures_platform.md`
- `/Users/nishimura+/.claude/projects/-Users-nishimura-/memory/project_futures_landing.md`
- `/Users/nishimura+/.claude/projects/-Users-nishimura-/memory/project_miratuku_membership.md`
- `/Users/nishimura+/work/esse-sense-deep-knowledge-strategy.html`
- `/Users/nishimura+/work/esse-sense-pwc-proposal-report.md`
- `/Users/nishimura+/work/deep-knowledge-future-forum-2026.html`
- `/Users/nishimura+/work/deep-knowledge-final-report-2026.html`
- `/Users/nishimura+/work/misc/西村予定.ics`
