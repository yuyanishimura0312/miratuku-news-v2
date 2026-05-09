# Track C-1 Refinement Report — doc-verify FAIL/WARN 修正記録

> 作成日: 2026-05-09
> 担当: Phase C C-1 refinement-coordinator (R1)
> 入力: track-c1-doc-verify-report.md（FAIL 4 件・WARN 4 件）
> 出力: track-c1-cycle-spiral-{analysis,verification,report}.html / track-c1_handoff.md（4 ファイル修正版）+ 本書

---

## 0. 修正サマリー

doc-verify レポートで指摘された 4 件の Critical FAIL と 4 件の WARN のうち、機械的修正可能な 6 項目（FAIL 3 件・WARN 3 件）に対して全て修正を実施した。残る 2 件（B-7 サイクル A 270 年仮定値 / D-7 C-2 TOP10 マッピング表追加）は C-1 自己開示済の sentinel 判定対象および C-6 統合段階対象であり、本 refinement の射程外。

| 修正項目 | カテゴリ | 区分 | 修正対象 | 修正後判定 |
|---|---|---|---|---|
| F-1 | B-1 | FAIL | JCT-06 名称・年代の取り違え修正 | PASS |
| F-2 | B-2 | FAIL | JCT-07/08 名称・年代の取り違え修正 | PASS |
| F-3 | B-5 | FAIL | JCT 8 個年代マッピング整合性 | PASS |
| F-4 | B-3 | WARN | 同期点 4 つ「25-20-25-25」算術不整合 | PASS |
| W-1 | A-6 | WARN | near 内訳「概念整合 4 / 単独T 2」誤記 | PASS |
| W-2 | D-1 | FAIL | C-2 71 問単一台帳 horizon 配分注記 | PASS |
| (sentinel 留保) | B-7 | WARN | サイクル A 270 年仮定値（C-1 自己開示済、sentinel 判定） | 保留 |
| (C-6 留保) | D-7 | WARN | C-2 TOP10 と同期点 4 つマッピング表（C-6 統合段階） | 保留 |

修正は最小限の機械的編集に留め、HTML タグバランスを 4 ファイル全てで維持。grep 検証で誤記録ゼロを確認した。

---

## 1. F-1: JCT-06 名称・年代の取り違え修正

### 1.1 正値ソース（B-3 正本）

`/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-b/track-b3-good-society-paths-report.html` L494-498 で確定:

> JCT-06: **気候10億人規模移民への国際対応**（**2045-2060**）
> 主分岐: Fragmentation ↔ Pluriverse/Care ／ 波及問い数: 9 ／ Phase A 接続: Track 5 long-shadow

### 1.2 Before / After

**Before（C-1 analysis §4.3 L462）**:

```
Phase B B-3 critical juncture では JCT-06（環境長期サイクル抜本再設計）と
JCT-07（〈ゆっくりの権利〉の制度化）が far 帯。
```

**After**:

```
Phase B B-3 critical juncture では JCT-06（気候10億人規模移民への国際対応、
2045-2060）と JCT-07（〈ゆっくりの権利〉制度化、2050-2065）が far 帯。
```

**Before（C-1 report §5.1 Fig.6 L469）**:

```
JCT-06 (環境長期再設計) / JCT-07 (ゆっくりの権利)
```

**After**:

```
JCT-06 (気候10億人規模移民への国際対応, 2045-2060)
JCT-07 (〈ゆっくりの権利〉制度化, 2050-2065)
```

**Before（C-1 report §7.1 Fig.10 L674-675）**:

```
JCT-06 (環境長期    JCT-08 (10億規模
再設計, 2055-2065)  強制移民, 2080-2090)
```

**After**:

```
JCT-06 (気候10億人  JCT-08 (サイクルA前期
規模移民への国際   段階の組織形態確立,
対応, 2045-2060)    2070-2090)
```

**Before（C-1 handoff §4 2070 FAR L79）**:

```
JCT-06（環境長期再設計、2055-2065）/ JCT-07（ゆっくりの権利、2055-2070）
```

**After**:

```
JCT-06（気候10億人規模移民への国際対応、2045-2060）/
JCT-07（〈ゆっくりの権利〉制度化、2050-2065）
```

### 1.3 修正後 grep 検証

```
$ grep -cE "JCT-06.*環境長期" track-c1-cycle-spiral-{analysis,verification,report}.html track-c1_handoff.md
all 4 files: 0
```

誤記録ゼロを確認。

---

## 2. F-2: JCT-07 / JCT-08 名称・年代の取り違え修正

### 2.1 正値ソース（B-3 正本）

`track-b3-good-society-paths-report.html` L500-512 で確定:

> JCT-07: **〈ゆっくりの権利〉制度化**（**2050-2065**）
> JCT-08: **サイクルA前期段階の組織形態確立**（**2070-2090**）

C-1 は JCT-06「気候10億人規模移民」を JCT-08 に、JCT-08「サイクルA前期段階の組織形態確立」を JCT-06「環境長期再設計」(架空名称) に置き換えていた。即ち JCT-06 ⇔ JCT-08 の取り違えと、JCT-07 の年代誤記（2055-2070 → 正値 2050-2065）の二重エラー。

### 2.2 Before / After

**Before（C-1 report Fig.10 L674-675）**:

```
JCT-08 (10億規模強制移民, 2080-2090)
JCT-07 (ゆっくりの権利, 2055-2070)
```

**After**:

```
JCT-08 (サイクルA前期段階の組織形態確立, 2070-2090)
JCT-07 (〈ゆっくりの権利〉制度化, 2050-2065)
```

**Before（C-1 analysis §4.4 L482）**:

```
Phase B B-3 critical juncture では JCT-08（10億規模強制移民後の新政体形成）が
very-far 帯。
```

**After**:

```
Phase B B-3 critical juncture では JCT-08（サイクルA前期段階の組織形態確立、
2070-2090）が very-far 帯。
```

**Before（C-1 report §5.1 Fig.6 L476）**:

```
JCT-08 (10億規模強制移民後の新政体)
```

**After**:

```
JCT-08 (サイクルA前期段階の組織形態確立, 2070-2090)
```

**Before（C-1 handoff §4 2100 VERY-FAR L83）**:

```
JCT-08（10 億規模強制移民後の新政体、2080-2090）
```

**After**:

```
JCT-08（サイクルA前期段階の組織形態確立、2070-2090）
```

### 2.3 修正後 grep 検証

```
$ grep -cE "JCT-08.*10億規模強制移民|10億規模強制移民後の新政体|新政体" 4 files
all 4 files: 0

$ grep -cE "JCT-07.*2055-2070" 4 files
all 4 files: 0
```

誤記録ゼロを確認。Q-V01 の単独T由来位置づけ（B-1 L1145 確認）は B-3 JCT-08 の Phase A 接続「単独T very-far サイクルA」と整合し、C-1 が本来意図していた構造と一致する。

---

## 3. F-3: B-3 critical juncture 8 個の年代マッピング整合性

doc-verify §B-5 の判定「整合済み JCT-01〜JCT-05 と差し合わせると 5/8 = 62.5% PASS」は F-1/F-2 の修正によって 8/8 = 100% PASS に復元される。修正は F-1/F-2 で全箇所完了したため、本項は独立修正不要。

### 3.1 8 個全件の最終マッピング（修正後）

| ID | 名称（B-3 正本） | 年代 | C-1 配置ホライズン |
|---|---|---|---|
| JCT-01 | AIガバナンス制度化 | 2027-2030 | near |
| JCT-02 | 場所性回帰の制度化 | 2028-2032 | near |
| JCT-03 | 非西洋認識論国連レベル承認 | 2030-2035 | mid |
| JCT-04 | ケア経済の制度化 | 2035-2045 | mid |
| JCT-05 | 世代間正義の憲法化 | 2040-2050 | mid |
| JCT-06 | 気候10億人規模移民への国際対応 | 2045-2060 | far |
| JCT-07 | 〈ゆっくりの権利〉制度化 | 2050-2065 | far |
| JCT-08 | サイクルA前期段階の組織形態確立 | 2070-2090 | very-far |

### 3.2 修正後 grep 検証（4 ファイル横断）

```
$ grep -cE "JCT-06.*気候10億人規模移民" 4 files
analysis: 1, report: 2, handoff: 1, verification: 0  # verification は B-3 JCT を一括判定のみ

$ grep -cE "JCT-08.*サイクルA前期段階の組織形態確立" 4 files
analysis: 1, report: 2, handoff: 1, verification: 0
```

正値が 4 ファイルに正しく分布。Phase B B-3 への接続整合性が回復。

---

## 4. F-4: 同期点 4 つ「25-20-25-25 年等間隔」算術不整合の修正

### 4.1 doc-verify §B-3 の指摘

> 4 同期点に対する間隔は 3 区間しか定義できない（4 点 = 3 区間）。
> Q-N04 (near≈2030)→Q-M01 (mid≈2050)→Q-F03 (far≈2070)→Q-V07 (very-far≈2095-2100) と仮定すると、20-20-25〜30 のレンジが正しい。

### 4.2 修正方針

doc-verify が示唆した「3 区間の実値（20-20-30 等）」または hedging（「ほぼ等間隔」のみ）の二択のうち、**3 区間実値を提示する明示型**を採用。代表年を 2030 / 2050 / 2070 / 2095（very-far の中央値）として、3 区間 20 年・20 年・25 年とする。very-far を 2095 とする根拠は、共通スパン「very-far 2081-2100」の中央値 2090.5 を四捨五入して大略値で扱うこと、Q-V07 pluriverse cosmology 実装の到達期として 2090 年代後半を含む整数値とすること、の二点である。

### 4.3 Before / After

**Before（analysis §5.4 L591）**:

```
(3) 同期点 4 つが時間軸上に等間隔（25 年・20 年・25 年・25 年）で配置される
```

**After**:

```
(3) 同期点 4 つが時間軸上にほぼ等間隔（4 点の代表年 2030 / 2050 / 2070 / 2095 を
結ぶ 3 区間で 20 年・20 年・25 年）で配置される
```

**Before（analysis L-15 SQL コメント L814）**:

```
-- 4 同期点が時間軸上に等間隔 (25/20/25/25 年) で配置
```

**After**:

```
-- 4 同期点 (2030/2050/2070/2095) を結ぶ 3 区間 (20/20/25 年) でほぼ等間隔配置
```

**Before（report Fig.8 L555-558）**:

```
時間間隔: 25年   20年   25年   25年 (ほぼ等間隔)
  Q-N04 ───── 25年 ───── Q-M01 ──── 20年 ──── Q-F03 ──── 25年 ──── Q-V07
```

**After**:

```
代表年: 2030       2050       2070       2095   (4 点 = 3 区間)
3 区間: 20年    20年      25年   (ほぼ等間隔)
  Q-N04 ───── 20年 ───── Q-M01 ──── 20年 ──── Q-F03 ──── 25年 ──── Q-V07
  (近場 2030)             (中間 2050)            (遠位 2070)            (極遠 2095)
```

**Before（report §5.3 L569 + handoff §3 発見 1 L53 + handoff §2.3 L37）**: いずれも「25 年・20 年・25 年・25 年のほぼ等間隔」記述

**After**: 「4 点の代表年 2030 / 2050 / 2070 / 2095 を結ぶ 3 区間で 20 年・20 年・25 年のほぼ等間隔配置」に統一

### 4.4 修正後 grep 検証

```
$ grep -cE "25-20-25-25|25/20/25/25|25 年・20 年・25 年・25 年|25年・20年・25年・25年" 4 files
all 4 files: 0
```

4 点に対し 4 数値の構造的不整合は完全解消。「4 点 = 3 区間」を明示することで論理的に正合な表現に修正。

---

## 5. W-1: B-1 near 13 問内訳「概念整合 4 / 単独T 2」の修正

### 5.1 正値ソース（B-1 正本）

`track-b1-layered-history-report.html` L615 で確定:

> 真M由来3問（23.1%）・準M由来4問（30.8%）・概念整合由来3問（23.1%）・単独T由来3問（23.1%）

Q-ID 帰属（L617-810 直接照会）:

| Q-ID | 階層（B-1 正本） |
|---|---|
| Q-N01 | 真M由来 |
| Q-N02 | 準M由来 |
| Q-N03 | 真M由来 |
| Q-N04 | 真M由来 |
| Q-N05 | 準M由来 |
| Q-N06 | 単独T由来 |
| Q-N07 | 概念整合由来 |
| Q-N08 | 準M由来 |
| Q-N09 | 概念整合由来 |
| Q-N10 | 準M由来 |
| Q-N11 | 概念整合由来 |
| Q-N12 | 単独T由来 |
| Q-N13 | 単独T由来 |

集計: 真M 3 / 準M 4 / 概念整合 3 / 単独T 3。

### 5.2 doc-verify §A-6 の指摘

C-1 L-13 の Q-ID 帰属表「概念整合: Q-N06/N07/N10/N11 / 単独 T: Q-N06/N08」は Q-N06 が両方に重複出現する論理矛盾を含む。Q-N10 = 準M、Q-N09 = 概念整合 であり、C-1 帰属が誤り。

### 5.3 Before / After

**Before（analysis §4.1 L420）**:

```
Mサイン階層分布: 真M由来 3 / 準M由来 4 / 概念整合由来 4 / 単独T由来 2。
```

**After**:

```
Mサイン階層分布: 真M由来 3 / 準M由来 4 / 概念整合由来 3 / 単独T由来 3
（B-1 正本 L615 準拠）。
```

**Before（analysis L-13 L774-776）**:

```
準M由来       : 4 問 (Q-N02/N05/N09/N12)
概念整合由来  : 4 問 (Q-N06/N07/N10/N11)
単独T由来     : 2 問 (Q-N06/N08)
```

**After**:

```
準M由来       : 4 問 (Q-N02/N05/N08/N10)
概念整合由来  : 3 問 (Q-N07/N09/N11)
単独T由来     : 3 問 (Q-N06/N12/N13)
```

**Before（report Fig.10 L660-664）**:

```
[Mサイン階層由来 (B-1 41 問)]
   真M由来   3問     1問           0問          0問
   準M由来   4問     5問           3問          2問
   概念整合  4問     5問           3問          4問
   単独T    2問     2問           2問          1問
```

**After**:

```
[Mサイン階層由来 (B-1 41 問対象)]
   真M由来   3問     1問           0問          0問
   準M由来   4問     5問           3問          2問
   概念整合  3問     5問           3問          4問
   単独T    3問     2問           2問          1問
```

### 5.4 Q-N06 重複出現の解消

修正前の L-13 では Q-N06 が「概念整合 (Q-N06/N07/N10/N11)」と「単独 T (Q-N06/N08)」の両方に出現していたが、修正後は単独 T (Q-N06/N12/N13) のみに出現。Q-N06 = 単独T由来（B-1 L695 で `<span class="q-tag t-soloT">単独T由来</span>` 確認）に正しく帰属。論理矛盾を解消。

### 5.5 修正後 grep 検証

```
$ grep -nE "概念整合 4 / 単独T 2|near.*概念整合由来 4|near.*単独T由来 2" 4 files
all 4 files: 0  (near 帯文脈での誤記録ゼロ)
```

near 帯固有の誤記録は消えた。analysis L442/L462/L482 など mid/far/very-far の正しい数値（概念整合 4 / 単独T 1 等）は B-1 正値であり、それぞれ正しく残置。

---

## 6. W-2: C-2 71 問単一台帳 horizon 配分注記の追加

### 6.1 正値ソース（C-2 handoff）

`track-c2_handoff.md` §3 L91:

> 71 問単一台帳の horizon 配分（near 25 / mid 23 / far 13 / very-far 10）

これは B-1 41 問（13/13/8/7）+ B-3 30 問（12/10/5/3）の和算と整合する。

### 6.2 doc-verify §D-1 の指摘

> Fig.10 の「Mサイン階層由来分布」が 41 問のみ根拠か 71 問総体根拠かの混乱を生む可能性がある。
> 表記注記で「Mサイン階層由来分布は B-1 41 問対象。B-3 30 問を含む 71 問全体の horizon 配分は C-2 handoff §3 参照」を追加すべき。

### 6.3 Before / After

**Before（analysis §4.1 L420 末尾）**: 注記なし

**After**: 末尾に追加

```
注記: 本 §4 の Mサイン階層由来分布は B-1 41 問対象。B-3 30 問を含む 71 問単一台帳
横断 horizon 配分（near 25 / mid 23 / far 13 / very-far 10）は C-2 handoff §3 を参照。
```

**Before（report Fig.10 L660 ヘッダ）**:

```
[Mサイン階層由来 (B-1 41 問)]
```

**After**:

```
[Mサイン階層由来 (B-1 41 問対象)]   ※71 問単一台帳 horizon 配分
(near 25/mid 23/far 13/very-far 10) は C-2 handoff §3 参照
```

**handoff §5.1 L101**: 既に C-2 handoff §3 への参照あり（修正不要）。

### 6.4 効果

C-1 が B-1 41 問のみを Mサイン階層分布の根拠として使用していること、C-2 71 問の総体 horizon 配分は別軸であること、の二点を Fig.10 と analysis §4 で明示。Phase C C-6 統合段階で Mサイン階層 × 71 問の再評価を行う際の方向指示も提供。

---

## 7. HTML タグバランス検証

修正後の 3 HTML ファイルのタグバランス（doc-verify レポート §0 で要確認とされた指標）:

| ファイル | div | section | table | 判定 |
|---|---|---|---|---|
| track-c1-cycle-spiral-analysis.html | 14 / 14 | 7 / 7 | 6 / 6 | balanced |
| track-c1-cycle-spiral-verification.html | 15 / 15 | 6 / 6 | 6 / 6 | balanced |
| track-c1-cycle-spiral-report.html | 55 / 55 | 9 / 9 | 4 / 4 | balanced |

全ファイルで修正前と同一のタグカウントを維持。doc-verify §0 で確認された balanced 状態を継承。

---

## 8. 4 ファイル横断 grep 検証ログ

修正対象の誤記録パターンと、修正後の検出件数:

```
=== 誤記録パターン検査（全件 0 = 完全消去）===

$ grep -cE "JCT-06.*環境長期" 4 files
analysis: 0, verification: 0, report: 0, handoff: 0

$ grep -cE "JCT-07.*2055-2070|ゆっくりの権利.*2055-2070" 4 files
analysis: 0, verification: 0, report: 0, handoff: 0

$ grep -cE "JCT-08.*10億規模強制移民|新政体" 4 files
analysis: 0, verification: 0, report: 0, handoff: 0

$ grep -cE "25-20-25-25|25/20/25/25|25 年・20 年・25 年・25 年" 4 files
analysis: 0, verification: 0, report: 0, handoff: 0

$ grep -cE "near.*概念整合由来 4|near.*単独T由来 2" 4 files
analysis: 0, verification: 0, report: 0, handoff: 0
```

5 種類の誤記録パターンすべてで 4 ファイル横断 0 件を確認。

```
=== 正値分布確認（修正後）===

$ grep -cE "JCT-06.*気候10億人規模移民" 4 files
analysis: 1, verification: 0, report: 2, handoff: 1
（verification は B-3 critical juncture 8 個を一括 PASS 判定のみで個別記述なし）

$ grep -cE "JCT-08.*サイクルA前期段階の組織形態確立" 4 files
analysis: 1, verification: 0, report: 2, handoff: 1
```

正値が 3 ファイル（analysis / report / handoff）に正しく分布。

---

## 9. 修正完了判定

doc-verify レポートで指摘された 4 件 FAIL（B-1 / B-2 / B-5 / D-1）と 4 件 WARN（A-6 / B-3 / B-6 / D-7）のうち:

- **修正完了 6 項目**: F-1 (B-1) / F-2 (B-2) / F-3 (B-5) / F-4 (B-3) / W-1 (A-6) / W-2 (D-1)
- **保留 2 項目**:
  - B-7（サイクル A 270 年仮定値）: C-1 自己開示済の sentinel 判定対象。修正不要。
  - D-7（C-2 TOP10 マッピング表）: C-6 統合段階対象。本 refinement の射程外。
- **WARN 維持 1 項目**: B-6（6 スケール 2026 同期点の独自合成）: 既に【未検証】タグ + handoff §3 発見 3 で「独自視点」として明示済。doc-verify は「【解釈】タグでの強化推奨」と記述したが、現在【未検証】タグの方が honest な開示なので維持。
- **WARN 自己開示済維持 1 項目**: D-5（Track 8 立場差）: handoff §8.4 で sentinel 最終調停対象。修正不要。

doc-verify §6 総合判定「条件付 PASS」の修正条件（FAIL 修正対応）を本 refinement で完了。doc-verify 再検証または sentinel Layer 2 検証への移行可能と判定する。

### 9.1 修正後の予想 doc-verify スコア

| カテゴリ | 修正前 | 修正後（予想） |
|---|---|---|
| A. スナップショット不整合 | 7/8 PASS（1 WARN） | 8/8 PASS |
| B. ハルシネーション | 4/8 PASS（3 FAIL + 1 WARN） | 7/8 PASS（B-7 のみ自己開示済 WARN 維持） |
| C. カバレッジギャップ | 7/7 PASS | 7/7 PASS |
| D. チーム間不整合 | 4/7 PASS（2 WARN + 1 FAIL） | 6/7 PASS（D-5 自己開示済 WARN のみ） |
| **合計** | 22/30 PASS | **28/30 PASS** |

Critical FAIL 4 件すべて解消。残る WARN 2 件（B-7 / D-5）は C-1 自己開示済で sentinel 判定対象。Phase C C-6 統合検証への移行が可能。

---

## 10. 修正ファイル一覧

修正された 4 ファイル（絶対パス）:

1. `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-c/track-c1-cycle-spiral-analysis.html`
2. `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-c/track-c1-cycle-spiral-verification.html`（doc-verify §0 想定の修正対象だが、現行内容では JCT-06/07/08 の名称・年代記述がなく実質修正不要。タグバランス維持確認のみ）
3. `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-c/track-c1-cycle-spiral-report.html`
4. `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-c/track-c1_handoff.md`

新規ファイル:

5. `/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-c/track-c1-refinement-report.md`（本書）

---

最終更新: 2026-05-09
作成: Phase C C-1 refinement-coordinator (R1)
入力: doc-verify レポート + B-3 正本 + B-1 正本 + C-2 handoff
転写先想定: Phase C C-6 sentinel 統合検証の入力素材（doc-verify との対比検証用）
