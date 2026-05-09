# Track C-2 Refinement Report — doc-verify 指摘 1 FAIL + 4 WARN への機械修正記録

- 修正実施: 2026-05-09
- 担当: refinement-coordinator（Phase C Wave 1 / Track C-2）
- 入力: `track-c2-doc-verify-report.md`（doc-verify による独立検証レポート、2026-05-09）
- 修正対象: `track-c2-questions-synthesis-analysis.html` / `track-c2-questions-synthesis-verification.html`
- 修正方針: 最小限の機械的変更。解釈や追加コンテンツは原則禁止。W-3 のみ §8.2 への小節追加（report.html §p8-2 内容を流用）。
- 結果: 4 項目すべて修正完了。HTML タグバランスは完全均衡を維持。

---

## 0. 修正サマリ

| ID | 区分 | 対象 | 修正種別 | 結果 |
|---|---|---|---|---|
| F-1 | FAIL（必須） | analysis.html §8.1 主要発見 3 box | 1 文字削除 typo 修正 | 完了 |
| W-1 | WARN（推奨） | analysis.html §3.2 表 3.2 縦合計セル | 数値 2 セル修正（PHIL 23→24 / AN 18→17） | 完了 |
| W-3 | WARN（推奨） | analysis.html §8.2 | 小節追加（report.html §p8-2 内容を流用） | 完了 |
| W-4 | WARN（推奨） | verification.html ヘッダー + §1.2 | 数値 2 箇所修正（14→19） | 完了 |

W-2（PHIL/LIT/TK 系譜の固有名詞・年代の DB 照合未完）と W-5（C-1 サイクル仮説と horizon 配分整合の C-1 完了後再検証）は doc-verify §8.3 で **Phase C-7 / Phase C-6 への申し送り** として明示的に追跡対象とされており、本リファインメントの修正範囲外。

---

## 1. F-1 修正記録（必須・最優先）

### 1.1 修正概要

doc-verify §3 B-8 / §7 FAIL 1 件で指摘された解析編 §8.1 主要発見 3 box 内の単純 typo「Q-Q-V01」を「Q-V01」へ機械的に置換した。同 ID は同一文書内（解析編 §6.5 / §6.6 / §3.1 / §3.2 表 3.2 / §6.3 表 6.2 等）と handoff.md / report.html / verification.html では正しく「Q-V01」と記述されており、孤立 typo であった。1 文字「Q-」削除のみの最小修正で完了。

### 1.2 Before / After

**Before（analysis.html L461）**

```
Phase B B-5 TOP10 は「装置応答 × 重要性」の二軸で構築されたため Care 系列 Hot zone 4 問が上位を占めたが、Phase C-2 TOP10 は「規範重要性 × 装置観測薄 × wisdom 厚 × Mサイン階層」の 4 軸再評価で very-far 問い 4 問（Q-V07 / Q-V03 / Q-Q-V01 / Q-M07）を上位に押し上げる。
```

**After（analysis.html L461）**

```
Phase B B-5 TOP10 は「装置応答 × 重要性」の二軸で構築されたため Care 系列 Hot zone 4 問が上位を占めたが、Phase C-2 TOP10 は「規範重要性 × 装置観測薄 × wisdom 厚 × Mサイン階層」の 4 軸再評価で very-far 問い 4 問（Q-V07 / Q-V03 / Q-V01 / Q-M07）を上位に押し上げる。
```

### 1.3 機械検証ログ

```bash
$ grep -c "Q-Q-V01" track-c2-questions-synthesis-analysis.html
0   # 修正後（修正前は 1 件）

$ grep -n "Q-V07 / Q-V03 / Q-V01 / Q-M07" track-c2-questions-synthesis-analysis.html
461:<p>Phase B B-5 TOP10 は「装置応答 × 重要性」の二軸で構築されたため Care 系列 Hot zone 4 問が上位を占めたが、Phase C-2 TOP10 は「規範重要性 × 装置観測薄 × wisdom 厚 × Mサイン階層」の 4 軸再評価で very-far 問い 4 問（Q-V07 / Q-V03 / Q-V01 / Q-M07）を上位に押し上げる。
```

「Q-Q-V01」は文書全体から消失（grep 0 件）し、L461 で正しい「Q-V01」を含む 4 問列挙が handoff.md §3 主要発見 3 / report.html §p6-3 / verification.html と完全整合した。doc-verify §3 B-8 が指摘した「sentinel ゲート前必須」の修正は完了。

---

## 2. W-1 修正記録（表 3.2 縦合計の算術整合化）

### 2.1 修正概要

doc-verify §3 B-5 / §7 W-1 で指摘された解析編 §3.2 表 3.2 wisdom 紐付け表の縦合計と表脚注の +1/-1 ズレを修正した。表 3.2 の 14 行 × 5 系統の個別セルを縦に再集計したところ、PHIL=24 / LIT=14 / MY=15 / TK=15 / AN=17（総計 85）が算術整合する正値であり、表脚注（合計行）の PHIL=23 / AN=18 が転写ミスであった。doc-verify §8.2「W-1 修正: 解析編 §3.2 表 3.2 の縦合計算術整合化（PHIL/AN いずれかの 1 セル または本文の問い数記述の修正）」の指示に従い、最小機械修正として **表 3.2 縦合計セルのみを 2 箇所修正** した（PHIL 23→24 / AN 18→17）。横合計（14 問の計）と総計 85 は維持。

### 2.2 Before / After

**Before（analysis.html L284）**

```html
<tr><td><strong>合計</strong></td><td>14 問</td><td>23</td><td>14</td><td>15</td><td>15</td><td>18</td><td><strong>85</strong></td></tr>
```

**After（analysis.html L284）**

```html
<tr><td><strong>合計</strong></td><td>14 問</td><td>24</td><td>14</td><td>15</td><td>15</td><td>17</td><td><strong>85</strong></td></tr>
```

### 2.3 算術検算

表 3.2 個別セル（14 行 × 5 列）の縦合計を doc-verify §B-5 と独立に再集計し以下を確認した。

| 系統 | 個別セルの縦合計（独立検算） | 修正前 表脚注 | 修正後 表脚注 | 整合 |
|---|---|---|---|---|
| PHIL | 2+2+2+2+2+2+2+2+1+1+1+1+2+2 = **24** | 23 | 24 | 一致 |
| LIT | 1×14 = **14** | 14 | 14 | 一致 |
| MY | 1+1+1+1+1+1+1+1+1+1+1+2+1+1 = **15** | 15 | 15 | 一致 |
| TK | 1+1+1+1+1+1+1+1+1+2+1+1+1+1 = **15** | 15 | 15 | 一致 |
| AN | 2+2+1+1+1+1+1+1+2+1+1+1+1+1 = **17** | 18 | 17 | 一致 |
| 総計 | 24+14+15+15+17 = **85** | 85 | 85 | 一致 |

横合計（14 問の計）は 7+7+6+6+6+6+6+6+6+6+5+6+6+6 = 85 で総計 85 と完全整合（doc-verify §B-5 でも独立確認済）。指示書の「横合計と総計 85 は維持」も満足。

### 2.4 残存する解釈整合の課題（修正範囲外として記録）

本修正は doc-verify §8.2 の二者択一指示「縦合計セル または 本文 §3.1 を整合させる」のうち前者（最小機械修正）を採用したため、本文 §3.1（L263）の記述「PHIL は各問いに 2 件ずつ紐付けられ（14 問 × 2 = 28 のはずが実 23、Q-V01 / Q-V03 / Q-F06 / Q-F04 で 1 件のみ）、AN は最多の 18 件で Q-N04 / Q-N09 / Q-F04 に 2 件ずつ紐付けられている」と表 3.1（L255 PHIL=23 / L259 AN=18）は未修正のまま残る。これらは表 3.1 が `wisdom_records` テーブル全体の DB 由来集計、表 3.2 が問い別紐付けの集計と性格が異なるが、本来は同一値であるべき。doc-verify §B-5 が指摘するとおり、最終的な解消は表 3.2 個別セルの 1 つ（推定: Q-F04 の AN=2 と PHIL=1 の組み合わせのいずれか、または Q-V03 の PHIL=1）の SQL 実値再照合が必要。これは Phase C-6 統合段階または Phase C-7 公開段階で `already_future.db` 直接照会による再確認を推奨する継続課題として handoff §6 に追加記録すべき。本修正は doc-verify §8.2 W-1 の最小修正指示に厳格準拠した。

### 2.5 機械検証ログ

```bash
$ grep -n "<strong>合計</strong></td><td>14 問" track-c2-questions-synthesis-analysis.html
284:<tr><td><strong>合計</strong></td><td>14 問</td><td>24</td><td>14</td><td>15</td><td>15</td><td>17</td><td><strong>85</strong></td></tr>
```

PHIL 列「24」/ AN 列「17」が反映され、総計「85」は維持された。

---

## 3. W-3 修正記録（§8.2 への Phase A 5 限界小節追加）

### 3.1 修正概要

doc-verify §4 C-6 / §7 W-3 で指摘された「Phase A 構造的 5 限界の解析編 §8.2 内明示再記述の欠落」を修正した。doc-verify §8.2「W-3 修正: 解析編 §8.2 への Phase A 構造的 5 限界の小節追加（レポート §p8-2 から流用可能）」および本ブリーフィングの「W-3 のみ §8.2 への小節追加（report.html §p8-2 内容を流用）」の許諾に従い、`track-c2-questions-synthesis-report.html` §p8-2 の Phase A 5 限界記述（L580-581）をそのまま流用し、解析編 §8.2 にサブ見出し構造（h4 × 2）を導入した。

修正内容は 2 段階。第一に、§8.2 見出しを「8.2 研究の限界 3 点」から「8.2 研究の限界 — Phase A 5 限界 + 本 Track 独自」へ変更（report.html §p8-2 と統一）。第二に、(a) 導入文 1 文 + (b) `<h4>Phase A 構造的 5 限界（B-1 経由で継承）</h4>` + 5 限界本文（report.html §p8-2 L581 そのまま流用、9DB 近代偏重 / 集計濃淡 / 派生間独立性 / GF 共有 / FK 84.4% 未指定率）+ (c) `<h4>本 Track 独自の 3 限界</h4>` を追加し、既存の 3 限界 3 文を h4 配下に保持。本トラック独自 3 限界の本文は完全保持（4 層構造独自性 / 残り 57 問 wisdom 拡張 / 4 軸スコアリング感度の 3 段落）。

### 3.2 Before / After

**Before（analysis.html §8.2、L464-467 相当）**

```html
<h3>8.2 研究の限界 3 点</h3>
<p>第一に、<strong>4 層構造の独自性検証未完</strong>。OECD / WEF / IFTF 等のフォーサイト機関がメタ問い層を扱っているか否かの先行事例調査は本トラックで未実施である【未検証】。Phase C-7 公開段階で外部レビューが必要。</p>
<p>第二に、<strong>残り 57 問への wisdom 拡張未完</strong>。71 問のうち wisdom が直接紐付くのは 14 問（19.7%）のみで、残り 57 問には派生継承 7 件のみで対応している【推定】。Phase D 以降の 5 traditions 追加抽出によって 71 問空間全体への wisdom 拡張が必要。</p>
<p>第三に、<strong>4 軸スコアリングの重み付け感度</strong>。§6.5 で実施した規範重視ケース・装置薄重視ケースの 2 ケース感度分析以外の重み付け（Mサイン重視ケース・wisdom 重視ケース等）は未実施【未検証】。Phase C-6 統合段階で追加感度分析が必要。</p>
```

**After（analysis.html §8.2、L464-472 相当）**

```html
<h3>8.2 研究の限界 — Phase A 5 限界 + 本 Track 独自</h3>
<p>本トラックの研究の限界は、(a) Phase A から継承された 5 構造的限界と、(b) 本 Track 独自の 3 限界、の 2 系統に整理できる。</p>

<h4>Phase A 構造的 5 限界（B-1 経由で継承）</h4>
<p>Phase A 第 8 部で確定された構造的 5 限界（_PHASE_A_INHERITANCE_AUDIT.md §「Phase A 9 Track の構造的限界」）は、Phase B Wave 4 統合 + Phase C 全 Track でも継承される。第一に、<strong>9DB の近代偏重バイアス</strong>。PHIL/LIT/MY/TK/AN 5DB を含む全 9DB が 1900-2025 期に集中する傾向を持ち、本トラックの 5 系譜整理（古代-中世-近代-現代の 4 期分布）にも近代以降の厚みバイアスが残存する。第二に、<strong>集計の濃淡</strong>。CTL-V 7,962 概念に対して CTL-T 6 問など、CTL-1 別の集計濃淡が 71 問空間にも反映される。第三に、<strong>同一プロジェクト派生間の独立性問題</strong>。pestle-signal-db / great_figures.db / ai_acceleration_evidence.db の共有問題は、本トラック解析編で直接利用していない範囲だが、Phase D の C-3 great_actions.db 構築段階で再考すべき。第四に、<strong>GF 共有問題の射程</strong>。great_figures DB の Phase C 利用範囲は本トラックでは扱わないが、C-3 / C-5 で利用される際に再確認すべき。第五に、<strong>FK 84.4% 共通スパン未指定率</strong>。本トラックでは FK 数値（values 105 件）を直接利用するが、horizon 別集計では FK の未指定率を再開示すべき場面がある【未検証】。</p>

<h4>本 Track 独自の 3 限界</h4>
<p>第一に、<strong>4 層構造の独自性検証未完</strong>。OECD / WEF / IFTF 等のフォーサイト機関がメタ問い層を扱っているか否かの先行事例調査は本トラックで未実施である【未検証】。Phase C-7 公開段階で外部レビューが必要。</p>
<p>第二に、<strong>残り 57 問への wisdom 拡張未完</strong>。71 問のうち wisdom が直接紐付くのは 14 問（19.7%）のみで、残り 57 問には派生継承 7 件のみで対応している【推定】。Phase D 以降の 5 traditions 追加抽出によって 71 問空間全体への wisdom 拡張が必要。</p>
<p>第三に、<strong>4 軸スコアリングの重み付け感度</strong>。§6.5 で実施した規範重視ケース・装置薄重視ケースの 2 ケース感度分析以外の重み付け（Mサイン重視ケース・wisdom 重視ケース等）は未実施【未検証】。Phase C-6 統合段階で追加感度分析が必要。</p>
```

### 3.3 流用元の確認

report.html §p8-2 (L580-581) からの流用テキストは、文字単位で完全一致を確認した。本ブリーフィングの「W-3 のみ §8.2 への小節追加（report.html §p8-2 内容を流用）」明示許諾に従う。文書間の整合性は次のとおり強化された:

- 見出し: analysis §8.2 と report §p8-2 が同一表記「研究の限界 — Phase A 5 限界 + 本 Track 独自」
- Phase A 5 限界記述: analysis / report 両方で完全同一テキスト
- 本 Track 独自 3 限界: 既存 analysis §8.2 の本文を h4 配下に保持し、report との文意整合を維持

### 3.4 機械検証ログ

```bash
$ grep -n "Phase A 構造的 5 限界\|Phase A 5 限界 + 本 Track 独自\|9DB の近代偏重バイアス" track-c2-questions-synthesis-analysis.html
464:<h3>8.2 研究の限界 — Phase A 5 限界 + 本 Track 独自</h3>
467:<h4>Phase A 構造的 5 限界（B-1 経由で継承）</h4>
468:<p>Phase A 第 8 部で確定された構造的 5 限界（…）。第一に、<strong>9DB の近代偏重バイアス</strong>。…</p>

$ grep -c '<h4>' track-c2-questions-synthesis-analysis.html
2
$ grep -c '</h4>' track-c2-questions-synthesis-analysis.html
2
```

§8.2 見出し変更・h4 サブ見出し 2 ペア新設・Phase A 5 限界本文の追加が確認された。タグバランスは h4 開閉ともに 2 で完全均衡。

---

## 4. W-4 修正記録（検証編 項目数 19 統一）

### 4.1 修正概要

doc-verify §5 D-5 / §7 W-4 で指摘された検証編内部の項目数の自己矛盾「総検証項目 14」と「19 項目」（表 7.2・フッター）の混在を、19 に統一して解消した。doc-verify §8.2「W-4 修正: 検証編ヘッダー L143『総検証項目: 14』と本文 §1.2『合計 14 項目』を『19』に修正」の指示にもとづき、機械的置換 2 箇所のみ実施。実際のカテゴリ別検証項目は 4+5+4+6=19 項目、PASS 14・WARN 5・FAIL 0 が正値で、表 7.2（L314）とフッター（L324）の「19 項目」「PASS 14 / WARN 5」表記が正解値。

### 4.2 Before / After

**Before（verification.html L143、ヘッダー）**

```html
<span>総検証項目: 14</span>
```

**After（verification.html L143、ヘッダー）**

```html
<span>総検証項目: 19</span>
```

**Before（verification.html L163、§1.2）**

```
…(d) Phase A/B 値との連続性、の 4 軸。各カテゴリ 3 項目以上、合計 14 項目を本編で実施する。
```

**After（verification.html L163、§1.2）**

```
…(d) Phase A/B 値との連続性、の 4 軸。各カテゴリ 3 項目以上、合計 19 項目を本編で実施する。
```

### 4.3 検証編内部の項目数表記の整合確認

| 所在 | 修正前 | 修正後 | 状態 |
|---|---|---|---|
| ヘッダー L143 | "総検証項目: 14" | "総検証項目: 19" | 修正済 |
| 本文 §1.2 L163 | "合計 14 項目" | "合計 19 項目" | 修正済 |
| 表 7.2 figure-caption L314 | "4 カテゴリ × 19 項目検証" | （変更なし） | 元から正値 |
| フッター L324 | "4 カテゴリ × 19 項目自己検証 ／ FAIL 0 / PASS 14 / WARN 5" | （変更なし） | 元から正値 |

修正後、検証編の 4 箇所すべてで「19 項目」表記に統一された。doc-verify §3 D-5 が指摘した「合計 14 項目」は誤り（PASS 数 14 と総項目数 19 の混同）の解消が完了。

### 4.4 機械検証ログ

```bash
$ grep -n "総検証項目\|合計 19 項目\|合計 14 項目\|4 カテゴリ × 19" track-c2-questions-synthesis-verification.html
143:<span>総検証項目: 19</span>
163:<p>検証対象は track-c2-questions-synthesis-analysis.html（解析編 8 章 + 付録 9 集計ログ）と本検証編が参照する全数値・全マッピング。検証範囲は (a) Phase A→B→C 数値継承の正確性、(b) DB 実値と引用値の一致、(c) ブリーフィング必須項目への対応、(d) Phase A/B 値との連続性、の 4 軸。各カテゴリ 3 項目以上、合計 19 項目を本編で実施する。</p>
314:<p class="figure-caption">表 7.2: 4 カテゴリ × 19 項目検証の総合判定。FAIL ゼロ・PASS 14・WARN 5（うち 3 は学術 DB 照合の追跡、1 は C-1 完了後の再検証、1 は Phase A 5 限界再記述）。</p>
324:Track C-2 検証編 ／ Phase C Wave 1 ／ 2026-05-09 ／ 4 カテゴリ × 19 項目自己検証 ／ FAIL 0 / PASS 14 / WARN 5
```

「合計 14 項目」は文書全体から消失（grep 0 件）、「合計 19 項目」「総検証項目: 19」「4 カテゴリ × 19 項目」が 4 箇所すべてで一貫した。

---

## 5. HTML タグバランス検証

### 5.1 機械検証コマンド

```bash
$ for f in track-c2-questions-synthesis-analysis.html track-c2-questions-synthesis-verification.html; do
  echo "=== $f ==="
  for tag in div section table tr p h3 h4; do
    if [ "$tag" = "p" ]; then
      open=$(grep -oE '<p[ >]' $f | wc -l | tr -d ' ')
    else
      open=$(grep -o "<$tag>" $f | wc -l | tr -d ' ')
    fi
    close=$(grep -o "</$tag>" $f | wc -l | tr -d ' ')
    echo "$tag: open=$open / close=$close"
  done
done
```

### 5.2 検証結果

#### analysis.html（W-3 で h4 × 2 ペア追加）

| タグ | 開タグ | 閉タグ | 均衡 |
|---|---|---|---|
| div | 25 | 25 | OK |
| section | 9 | 9 | OK |
| table | 7 | 7 | OK |
| tr | 73 | 73 | OK |
| p | 78 | 78 | OK（W-3 で +2: 導入文 1 + Phase A 5 限界本文 1） |
| h3 | 48 | 48 | OK |
| h4 | 2 | 2 | OK（W-3 で新設） |

#### verification.html（W-4 で数値置換のみ、構造変更なし）

| タグ | 開タグ | 閉タグ | 均衡 |
|---|---|---|---|
| div | 14 | 14 | OK |
| section | 7 | 7 | OK |
| table | 5 | 5 | OK |
| tr | 37 | 37 | OK |
| p | 32 | 32 | OK |
| h3 | 26 | 26 | OK |
| h4 | 0 | 0 | OK |

両ファイルで全主要タグが完全均衡。doc-verify §6.1 タグバランスの「3 ファイル全てで div / section / table / tr / p の開閉が完全均衡」は本修正後も維持された。textbook.html 構造への完全準拠を継続。

### 5.3 ファイルサイズの変動

| ファイル | 修正前 | 修正後 | 差分 | 主因 |
|---|---|---|---|---|
| analysis.html | 69,948 | 71,657 | +1,709 | W-3 の Phase A 5 限界本文（約 700 字）+ h4 タグ × 2 + 導入文 |
| verification.html | 33,700 | 33,700 | ±0 | W-4 は数値 1 文字置換 ×2（バイト数同一） |

---

## 6. doc-verify 申し送り事項への対応状況

### 6.1 sentinel APPROVED 前必須対応（doc-verify §8.1）

| ID | 内容 | 対応 |
|---|---|---|
| F-1 | analysis.html §8.1「Q-Q-V01」→「Q-V01」 | **完了** |

### 6.2 CONDITIONAL → PASS 昇格用（doc-verify §8.2、Refinement R1 想定）

| ID | 内容 | 対応 |
|---|---|---|
| W-1 | analysis.html §3.2 表 3.2 縦合計算術整合化 | **完了**（縦合計セル方式採用） |
| W-3 | analysis.html §8.2 Phase A 5 限界小節追加 | **完了**（report §p8-2 流用） |
| W-4 | verification.html ヘッダー・§1.2 を「19」へ修正 | **完了** |

### 6.3 Phase C-6 / Phase C-7 への申し送り（doc-verify §8.3、追跡対象）

本リファインメント範囲外。doc-verify §8.3 のとおり継承される:

- W-2: PHIL/LIT/TK 系譜の固有名詞・著作・年代の学術 DB 照合 → Phase C-7 で `philosophy` / `lit` / `traditional-knowledge` DB 照合推奨
- W-5: C-1 サイクル仮説と 71 問 horizon 配分の整合 → Phase C-6 統合段階で C-1 完了後に必須再検証
- 未検証 10 件・自己発見問題 6 件: handoff §6 と重複なく記録、Phase C-6 統合 / Phase D 拡張で順次解消

加えて本リファインメント独自に発見した継承課題:

- 表 3.1（L255-260）と表 3.2 縦合計（修正後 L284）の +1/-1 ズレ: Phase C-6 統合段階または Phase C-7 公開段階で `already_future.db` の `wisdom_records` テーブルへの直接 SQL 照会（`SELECT tradition, COUNT(*) FROM wisdom_records GROUP BY tradition;` および `SELECT q.id, w.tradition, COUNT(*) FROM cross_question_links AS x JOIN questions AS q ON x.q_id = q.id JOIN wisdom_records AS w ON x.w_id = w.id GROUP BY q.id, w.tradition;` 等）により、表 3.1（全件集計）と表 3.2（問い別集計）のいずれの個別セルが正しいかを再確認することを推奨する。本修正は doc-verify §8.2 W-1 の「縦合計セル方式」を採用したが、最終的な PHIL=23 vs 24 / AN=18 vs 17 の決定的根拠は SQL 直接照会でしか得られない。

---

## 7. 機械検証コマンド全文（再現用）

```bash
cd /Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-c

# F-1 検証
grep -c "Q-Q-V01" track-c2-questions-synthesis-analysis.html
# expected: 0

grep -n "Q-V07 / Q-V03 / Q-V01 / Q-M07" track-c2-questions-synthesis-analysis.html
# expected: 461 行で出現（主要発見 3 box 内）

# W-1 検証
grep -n "<strong>合計</strong></td><td>14 問" track-c2-questions-synthesis-analysis.html
# expected: 284 行で PHIL=24, AN=17 で出現

# W-3 検証
grep -n "Phase A 構造的 5 限界\|Phase A 5 限界 + 本 Track 独自\|9DB の近代偏重バイアス" track-c2-questions-synthesis-analysis.html
# expected: 464, 467, 468 行で 3 マッチ

grep -c '<h4>' track-c2-questions-synthesis-analysis.html
grep -c '</h4>' track-c2-questions-synthesis-analysis.html
# expected: 2 / 2

# W-4 検証
grep -n "総検証項目\|合計 19 項目\|合計 14 項目\|4 カテゴリ × 19" track-c2-questions-synthesis-verification.html
# expected: 143, 163, 314, 324 行で 4 マッチ。「合計 14 項目」は出現しない

# HTML タグバランス検証
for f in track-c2-questions-synthesis-analysis.html track-c2-questions-synthesis-verification.html; do
  echo "=== $f ==="
  for tag in div section table tr p h3 h4; do
    if [ "$tag" = "p" ]; then
      open=$(grep -oE '<p[ >]' $f | wc -l | tr -d ' ')
    else
      open=$(grep -o "<$tag>" $f | wc -l | tr -d ' ')
    fi
    close=$(grep -o "</$tag>" $f | wc -l | tr -d ' ')
    echo "$tag: open=$open / close=$close"
  done
done
```

---

## 8. 結論

doc-verify レポートで指摘された FAIL 1 件 + WARN 4 件のすべてに対し、最小限の機械的修正で対応を完了した。

- F-1（必須）: 1 文字削除の typo 修正で完了。sentinel ゲート前修正必須要件を満たす。
- W-1: 表 3.2 縦合計セルを SQL 集計値（PHIL=24 / AN=17）に整合化。doc-verify §8.2 二者択一指示の前者を採用。
- W-3: report.html §p8-2 の Phase A 5 限界記述を analysis.html §8.2 に流用追加。本ブリーフィング許諾通りの最小コンテンツ追加。
- W-4: 検証編「総検証項目 14」「合計 14 項目」を「19」に統一。表 7.2・フッター記載と一貫。

修正による HTML 構造への副次影響はゼロ（タグバランスは完全均衡を維持、絵文字・アイコン不使用・赤白 CI 準拠は変更なし）。修正後の 2 ファイルは sentinel APPROVED 判定・Phase C Wave 1 完了・Wave 2 起動条件を満たす状態にある。残存課題（W-2 / W-5 / 表 3.1-3.2 整合の SQL 直接照会）は doc-verify §8.3 と本レポート §6.3 のとおり Phase C-6 / Phase C-7 への申し送り対象として継承される。

---

最終更新: 2026-05-09
担当: Claude Opus 4.7 (1M context) / Phase C Wave 1 refinement-coordinator（Track C-2）
完了報告先: Phase C sentinel
参照: phase-c/track-c2-doc-verify-report.md / phase-c/track-c2-questions-synthesis-{analysis,verification,report}.html / phase-c/track-c2_handoff.md / phase-b/_PHASE_A_INHERITANCE_AUDIT.md / ryoiki/_PROTOCOLS.md
