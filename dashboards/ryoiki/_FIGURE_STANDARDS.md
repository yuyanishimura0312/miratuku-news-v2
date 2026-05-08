# 領域策定プロジェクト — 図版規格 (Figure Standards)

作成日: 2026-05-09
担当: 図版デザインリード（design agent）
対象: Track 1〜9 の全 report.html が参照する共通図版仕様

---

## 1. 共通カラーパレット（赤白CI準拠）

### 1.1 主役・基本色

| 用途 | ライトモード | ダークモード | 説明 |
|---|---|---|---|
| 主色（強調・高頻度） | `#CC1400` | `#FF4030` | 赤白CI 主役。バー・ドーナツ・セル最大濃度に使用 |
| 主色ソフト | `#B01200` | `#CC2010` | ホバー・2番目に濃いグラデーション段 |
| 副色（系譜・ライン） | `#6E2C2C` | `#8A3A3A` | 影響系譜図の補助ライン・第二データ系列 |
| テキスト | `#121212` | `#E0E0E0` | 本文・軸ラベル |
| テキスト 弱 | `#555555` | `#AAAAAA` | データラベル補足・凡例説明 |
| テキスト 最弱 | `#6B6B6B` | `#8A8A8A` | キャプション・軸目盛り |
| 背景 | `#FFFFFF` | `#121212` | 図版エリア背景 |
| 面（カード） | `#FFFFFF` | `#1A1A1A` | 図版コンテナ背景 |
| サーフェス | `#F7F7F5` | `#1A1A1A` | 凡例エリア・ヘッダー行 |
| ボーダー | `#D9D9D9` | `#333333` | 外枠・区切り線 |
| ボーダー 弱 | `#EEEEEE` | `#2A2A2A` | セル区切り・グリッド線 |

### 1.2 グレースケール 5段階（印刷・色盲対応）

| 段階 | HEX | 用途 |
|---|---|---|
| G0 | `#FFFFFF` | 最小値・空白セル |
| G1 | `#F0EDED` | 低密度（1〜25%） |
| G2 | `#D6CFCF` | 中低密度（26〜50%） |
| G3 | `#A89B9B` | 中高密度（51〜75%） |
| G4 | `#6B5555` | 高密度（76〜100%） |

印刷時（@media print）は赤を G1〜G4 に自動フォールバックする（Section 5.3 CSS参照）。

### 1.3 データ可視化用カラーマップ（赤単色6段階）

ヒートマップ・強度表現には赤白CI の透明度グラデーションを使用する。
外部カラーライブラリ（D3等）は使用しない。

```css
/* ライトモード */
.h-0 { background: #FFFFFF;                  color: #6B6B6B; }  /* 0件 / 空白 */
.h-1 { background: rgba(204,20,0,0.05);      color: #121212; }  /* 最低密度 */
.h-2 { background: rgba(204,20,0,0.12);      color: #121212; }  /* 低密度    */
.h-3 { background: rgba(204,20,0,0.25);      color: #121212; }  /* 中密度    */
.h-4 { background: rgba(204,20,0,0.45);      color: #FFFFFF; font-weight: 700; }  /* 高密度  */
.h-5 { background: rgba(204,20,0,0.72);      color: #FFFFFF; font-weight: 700; }  /* 最高密度 */

/* ダークモード */
[data-theme="dark"] .h-0 { background: #1A1A1A; color: #8A8A8A; }
[data-theme="dark"] .h-1 { background: rgba(255,64,48,0.10); color: #E0E0E0; }
[data-theme="dark"] .h-2 { background: rgba(255,64,48,0.22); color: #E0E0E0; }
[data-theme="dark"] .h-3 { background: rgba(255,64,48,0.38); color: #E0E0E0; }
[data-theme="dark"] .h-4 { background: rgba(255,64,48,0.58); color: #FFFFFF; font-weight: 700; }
[data-theme="dark"] .h-5 { background: rgba(255,64,48,0.82); color: #FFFFFF; font-weight: 700; }
```

### 1.4 複数系列用（色覚多様性対応補色3色）

多変量比較（系譜図・サイクル図の複数ノード）が必要な場合のみ使用する。
いずれも赤白CIの赤（#CC1400）を主役として添え、以下を副次的に使用する。

| 系列 | ライトモード | ダークモード | 役割 |
|---|---|---|---|
| A（主） | `#CC1400` | `#FF4030` | メインデータ・強調 |
| B（副） | `#6E2C2C` | `#A05050` | 第二カテゴリ・補完 |
| C（補） | `#999999` | `#777777` | 参照・背景系列 |
| D（補2） | `#C8B4A0` | `#5A4A3A` | 4系列必要時のみ |

青・緑・紫は主役色として使用しない（赤白CI規約）。
ただしデータの性質が「対立軸」を持つ場合（肯定/否定、高/低など）に限り、
ニュートラルグレー（`#999999`）と赤（`#CC1400`）の2色対比を認める。

---

## 2. 6種図版テンプレート

### 共通ラッパー HTML（全図版共通）

```html
<div class="figure" id="figN">
  <div class="figure-title">図表N: [タイトル]（[出典ラベル例: 集計L-XX]）</div>
  <!-- 図版本体をここに挿入 -->
  <div class="figure-caption">[説明文。出典: [DB名] / [クエリID]。]</div>
</div>
```

`.figure` クラスは _template-akashiro.html に定義済み。
CSS再掲（未実装の場合のみ追記）:

```css
.figure {
  margin: 40px 0;
  padding: 24px;
  border: 1px solid var(--border-light);
  background: var(--card);
}
.figure-title {
  font-family: var(--font);
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--accent-warm);
  margin-bottom: 14px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
.figure-caption {
  font-family: var(--font);
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-top: 14px;
  line-height: 1.6;
}
```

---

### A. ホライズンマップ（Horizon Map）

**用途**: 2030/2050/2070/2100 x N領域のマトリクス。ホライズン別の強み宣言・テーマ分布に使用。
**推奨幅**: 100%（max-width 760px に収まる形）
**形式**: HTML div グリッド（CSSグリッド）。インラインSVGは不要。
**ファイル依存**: なし（インラインCSS）

```html
<!-- ======================================================
     図版 A: ホライズンマップ
     使用法: figure-title と figure-caption を実データに書き換える
     grid-template-columns は列数に応じて調整
     ====================================================== -->
<style>
.horizon-map {
  display: grid;
  gap: 1px;
  background: var(--border-light);
  border: 1px solid var(--border);
  font-family: var(--font);
  font-size: 0.80rem;
  overflow-x: auto;
}
.horizon-map > div {
  background: var(--card);
  padding: 9px 11px;
  line-height: 1.5;
}
.horizon-map .hm-head {
  background: var(--surface);
  font-weight: 700;
  font-size: 0.75rem;
  letter-spacing: 0.04em;
  text-align: center;
  color: var(--text-secondary);
}
.horizon-map .hm-row-label {
  background: var(--surface);
  font-weight: 700;
  font-size: 0.80rem;
  color: var(--text);
}
.horizon-map .hm-cell {
  text-align: center;
  font-size: 0.75rem;
  color: var(--text-secondary);
}
/* 強み度（str-0〜3） */
.horizon-map .str-0  { color: var(--text-muted); }
.horizon-map .str-1  { color: var(--text-secondary); }
.horizon-map .str-2  { color: var(--accent-warm); font-weight: 700; }
.horizon-map .str-3  { color: var(--accent-warm); font-weight: 700;
                        background: rgba(204,20,0,0.06); }
[data-theme="dark"] .horizon-map .str-3 {
  background: rgba(255,64,48,0.12);
}
</style>

<div class="figure" id="figA-sample">
  <div class="figure-title">図表A: ホライズン x 領域 強みマップ（ダミーデータ）</div>
  <!-- 列数: 1(ラベル) + 4(ホライズン) = 5列 -->
  <div class="horizon-map" style="grid-template-columns: 200px repeat(4, 1fr);">
    <!-- ヘッダー行 -->
    <div class="hm-head">領域</div>
    <div class="hm-head">2030</div>
    <div class="hm-head">2050</div>
    <div class="hm-head">2070</div>
    <div class="hm-head">2100</div>

    <!-- データ行（str-0〜3 で強度表現） -->
    <div class="hm-row-label">テクノロジー・AI</div>
    <div class="hm-cell str-3">強</div>
    <div class="hm-cell str-2">中</div>
    <div class="hm-cell str-1">弱</div>
    <div class="hm-cell str-0">—</div>

    <div class="hm-row-label">環境・気候</div>
    <div class="hm-cell str-2">中</div>
    <div class="hm-cell str-3">強</div>
    <div class="hm-cell str-2">中</div>
    <div class="hm-cell str-1">弱</div>

    <div class="hm-row-label">地政学・安全保障</div>
    <div class="hm-cell str-2">中</div>
    <div class="hm-cell str-1">弱</div>
    <div class="hm-cell str-0">—</div>
    <div class="hm-cell str-0">—</div>

    <div class="hm-row-label">社会・人口動態</div>
    <div class="hm-cell str-1">弱</div>
    <div class="hm-cell str-2">中</div>
    <div class="hm-cell str-1">弱</div>
    <div class="hm-cell str-0">—</div>

    <div class="hm-row-label">ガバナンス・制度</div>
    <div class="hm-cell str-1">弱</div>
    <div class="hm-cell str-1">弱</div>
    <div class="hm-cell str-0">—</div>
    <div class="hm-cell str-0">—</div>
  </div>
  <div class="figure-caption">
    強み評価: 強=密度・多様性ともに高い中核領域、中=一定の蓄積あり、弱=部分的、—=記録がほぼない。
    出典: [DB名] / 集計[L-XX]。
  </div>
</div>
```

---

### B. テーマ分布図（Theme Distribution）

**用途**: テーマ別の件数比較。バーチャートまたはドーナツチャートで頻度を示す。
**推奨幅**: 100%（バー）/ 200px SVG部分（ドーナツ）
**形式**: バーチャートは HTML div + CSS。ドーナツはインライン SVG。
**ファイル依存**: なし

#### B-1. 横バーチャート（最もシンプル。大量カテゴリに対応）

```html
<style>
.bar-chart { width: 100%; }
.bar-chart .row {
  display: flex;
  align-items: center;
  margin-bottom: 7px;
  gap: 12px;
  font-family: var(--font);
  font-size: 0.82rem;
}
.bar-chart .row .label {
  width: 180px;
  flex-shrink: 0;
  color: var(--text);
  text-align: right;
  line-height: 1.4;
}
.bar-chart .row .bar-wrap {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
}
.bar-chart .row .bar-bar {
  height: 14px;
  background: var(--accent-warm);
  min-width: 2px;
}
.bar-chart .row .bar-val {
  color: var(--text-muted);
  font-weight: 700;
  min-width: 56px;
  font-size: 0.80rem;
}
@media (max-width: 600px) {
  .bar-chart .row .label { width: 120px; font-size: 0.75rem; }
  .bar-chart .row .bar-val { min-width: 44px; font-size: 0.75rem; }
}
</style>

<div class="figure" id="figB1-sample">
  <div class="figure-title">図表B: テーマ別予測件数 上位8（ダミーデータ）</div>
  <div class="bar-chart">
    <!--
      width は最大値に対する割合(%)を手計算して設定。
      例: 最大値 707 を 100% とすると、409 は 409/707*100 = 57.8%
    -->
    <div class="row">
      <div class="label">テクノロジー・AI</div>
      <div class="bar-wrap">
        <div class="bar-bar" style="width: 100%;"></div>
        <div class="bar-val">707件</div>
      </div>
    </div>
    <div class="row">
      <div class="label">経済・金融</div>
      <div class="bar-wrap">
        <div class="bar-bar" style="width: 57.8%;"></div>
        <div class="bar-val">409件</div>
      </div>
    </div>
    <div class="row">
      <div class="label">環境・気候</div>
      <div class="bar-wrap">
        <div class="bar-bar" style="width: 39.6%;"></div>
        <div class="bar-val">280件</div>
      </div>
    </div>
    <div class="row">
      <div class="label">地政学・安全保障</div>
      <div class="bar-wrap">
        <div class="bar-bar" style="width: 26.7%;"></div>
        <div class="bar-val">189件</div>
      </div>
    </div>
    <div class="row">
      <div class="label">社会・人口動態</div>
      <div class="bar-wrap">
        <div class="bar-bar" style="width: 20.9%;"></div>
        <div class="bar-val">148件</div>
      </div>
    </div>
    <div class="row">
      <div class="label">健康・医療</div>
      <div class="bar-wrap">
        <div class="bar-bar" style="width: 15.7%;"></div>
        <div class="bar-val">111件</div>
      </div>
    </div>
    <div class="row">
      <div class="label">エネルギー・資源</div>
      <div class="bar-wrap">
        <div class="bar-bar" style="width: 14.4%;"></div>
        <div class="bar-val">102件</div>
      </div>
    </div>
    <div class="row">
      <div class="label">ガバナンス・制度</div>
      <div class="bar-wrap">
        <div class="bar-bar" style="width: 10.6%;"></div>
        <div class="bar-val">75件</div>
      </div>
    </div>
  </div>
  <div class="figure-caption">
    N=1,021件（年明示予測より抽出）。バー幅は最大件数（707件）を100%とした相対表示。
    出典: [DB名] / 集計[L-XX]。
  </div>
</div>
```

#### B-2. ドーナツチャート（SVG版。上位5〜7カテゴリまで）

```html
<!--
  stroke-dasharray の計算方法:
  半径 r=70 → 円周 = 2×π×70 ≒ 439.82
  各セグメントの dash = 割合 × 439.82
  stroke-dashoffset = -(それまでの累積 dash 合計)
-->
<style>
.donut-wrap {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 24px;
  align-items: center;
}
@media (max-width: 600px) {
  .donut-wrap { grid-template-columns: 1fr; }
}
.legend {
  font-family: var(--font);
  font-size: 0.78rem;
  color: var(--text-secondary);
}
.legend .item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 5px;
  line-height: 1.4;
}
.legend .swatch {
  width: 12px;
  height: 12px;
  flex-shrink: 0;
  border-radius: 1px;
}
</style>

<div class="figure" id="figB2-sample">
  <div class="figure-title">図表B-2: 主体タイプ別レポート構成比（ダミーデータ）</div>
  <div class="donut-wrap">
    <svg viewBox="0 0 160 160" width="200" height="200"
         role="img" aria-label="主体タイプ別構成比 ドーナツチャート">
      <!--
        サンプルデータ（合計 100% = 439.82px）:
        academic: 68.8% → dash=302.6  offset=0
        int_org:  23.3% → dash=102.5  offset=-302.6
        government: 6.8% → dash=29.9  offset=-405.1
        others:   1.1%  → dash=4.8   offset=-435.0
      -->
      <circle cx="80" cy="80" r="70"
              fill="none" stroke="#EEEEEE" stroke-width="20"/>
      <circle cx="80" cy="80" r="70"
              fill="none" stroke="#CC1400" stroke-width="20"
              stroke-dasharray="302.6 439.82"
              stroke-dashoffset="0"
              transform="rotate(-90 80 80)"/>
      <circle cx="80" cy="80" r="70"
              fill="none" stroke="#6E2C2C" stroke-width="20"
              stroke-dasharray="102.5 439.82"
              stroke-dashoffset="-302.6"
              transform="rotate(-90 80 80)"/>
      <circle cx="80" cy="80" r="70"
              fill="none" stroke="#999999" stroke-width="20"
              stroke-dasharray="29.9 439.82"
              stroke-dashoffset="-405.1"
              transform="rotate(-90 80 80)"/>
      <circle cx="80" cy="80" r="70"
              fill="none" stroke="#C8B4A0" stroke-width="20"
              stroke-dasharray="4.8 439.82"
              stroke-dashoffset="-435.0"
              transform="rotate(-90 80 80)"/>
      <text x="80" y="74" text-anchor="middle"
            font-family="'Noto Sans JP', sans-serif"
            font-size="11" fill="currentColor" font-weight="700">N=</text>
      <text x="80" y="90" text-anchor="middle"
            font-family="'Noto Sans JP', sans-serif"
            font-size="13" fill="#CC1400" font-weight="700">76,548</text>
    </svg>
    <div class="legend">
      <div class="item">
        <div class="swatch" style="background:#CC1400;"></div>
        academic（学術）— 68.8%
      </div>
      <div class="item">
        <div class="swatch" style="background:#6E2C2C;"></div>
        international_org — 23.3%
      </div>
      <div class="item">
        <div class="swatch" style="background:#999999;"></div>
        government — 6.8%
      </div>
      <div class="item">
        <div class="swatch" style="background:#C8B4A0;"></div>
        others — 1.1%
      </div>
    </div>
  </div>
  <div class="figure-caption">
    ドーナツの各弧は割合比。中央数値は総レポート件数。
    出典: [DB名] / 集計[L-XX]。
  </div>
</div>
```

---

### C. TOP10ランキング（Ranking Table）

**用途**: 「問うべき領域TOP10」など順位付きリスト。テーブル形式が基本。
**推奨幅**: 100%
**形式**: HTMLテーブル。インラインSVGは不要。
**ファイル依存**: なし

```html
<style>
.ranking-table {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--font);
  font-size: 0.84rem;
  line-height: 1.55;
  margin: 0;
}
.ranking-table th, .ranking-table td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid var(--border-light);
  vertical-align: top;
}
.ranking-table thead th {
  background: var(--surface);
  font-weight: 700;
  font-size: 0.78rem;
  letter-spacing: 0.04em;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border);
}
.ranking-table tbody tr:hover td {
  background: var(--card-hover);
}
.rank-num {
  font-family: "SF Mono", "Fira Code", monospace;
  font-weight: 700;
  color: var(--accent-warm);
  font-size: 0.92rem;
  white-space: nowrap;
}
.rank-badge {
  display: inline-block;
  font-family: var(--font);
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  padding: 2px 6px;
  border: 1px solid var(--border);
  color: var(--text-muted);
}
.rank-badge.density  { border-color: var(--accent-warm); color: var(--accent-warm); }
.rank-badge.blank    { border-color: var(--text-muted);  color: var(--text-muted); }
.score-bar-wrap {
  display: flex;
  align-items: center;
  gap: 6px;
}
.score-bar {
  height: 6px;
  background: var(--accent-warm);
  border-radius: 2px;
  min-width: 2px;
}
.score-val {
  font-size: 0.78rem;
  color: var(--text-muted);
  font-weight: 700;
  min-width: 36px;
  text-align: right;
}
@media (max-width: 600px) {
  .ranking-table th, .ranking-table td { padding: 8px 8px; font-size: 0.78rem; }
  .score-bar-wrap { display: none; }
}
</style>

<div class="figure" id="figC-sample">
  <div class="figure-title">図表C: 問うべき領域TOP10（ダミーデータ）</div>
  <table class="ranking-table">
    <thead>
      <tr>
        <th style="width:44px;">順位</th>
        <th>領域</th>
        <th style="width:72px;">戦略</th>
        <th style="width:100px;">重要度スコア</th>
        <th>根拠</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><span class="rank-num">01</span></td>
        <td><strong>AI・自動化と労働変容</strong><br>
            <span style="font-size:0.75rem;color:var(--text-muted);">
              技術加速と社会構造の非同期に関する問い
            </span>
        </td>
        <td><span class="rank-badge density">密度戦略</span></td>
        <td>
          <div class="score-bar-wrap">
            <div class="score-bar" style="width:96px;"></div>
            <div class="score-val">9.6</div>
          </div>
        </td>
        <td style="font-size:0.75rem;color:var(--text-muted);">集計L-05</td>
      </tr>
      <tr>
        <td><span class="rank-num">02</span></td>
        <td><strong>気候転換と生態系閾値</strong><br>
            <span style="font-size:0.75rem;color:var(--text-muted);">
              2050-2100の長期軌道分析
            </span>
        </td>
        <td><span class="rank-badge density">密度戦略</span></td>
        <td>
          <div class="score-bar-wrap">
            <div class="score-bar" style="width:88px;"></div>
            <div class="score-val">8.8</div>
          </div>
        </td>
        <td style="font-size:0.75rem;color:var(--text-muted);">集計L-08</td>
      </tr>
      <tr>
        <td><span class="rank-num">03</span></td>
        <td><strong>地政学的多極化と制度設計</strong><br>
            <span style="font-size:0.75rem;color:var(--text-muted);">
              グローバルガバナンスの空白
            </span>
        </td>
        <td><span class="rank-badge density">密度戦略</span></td>
        <td>
          <div class="score-bar-wrap">
            <div class="score-bar" style="width:80px;"></div>
            <div class="score-val">8.0</div>
          </div>
        </td>
        <td style="font-size:0.75rem;color:var(--text-muted);">集計L-12</td>
      </tr>
      <tr>
        <td><span class="rank-num">04</span></td>
        <td><strong>グローバルサウスの認識論的転換</strong><br>
            <span style="font-size:0.75rem;color:var(--text-muted);">
              既存フォーサイトの地理的偏りへの対抗
            </span>
        </td>
        <td><span class="rank-badge blank">空白戦略</span></td>
        <td>
          <div class="score-bar-wrap">
            <div class="score-bar" style="width:76px;"></div>
            <div class="score-val">7.6</div>
          </div>
        </td>
        <td style="font-size:0.75rem;color:var(--text-muted);">集計L-36</td>
      </tr>
      <tr>
        <td><span class="rank-num">05</span></td>
        <td><strong>世代間正義と長期設計</strong><br>
            <span style="font-size:0.75rem;color:var(--text-muted);">
              2070-2100の未開拓フロンティア
            </span>
        </td>
        <td><span class="rank-badge blank">空白戦略</span></td>
        <td>
          <div class="score-bar-wrap">
            <div class="score-bar" style="width:72px;"></div>
            <div class="score-val">7.2</div>
          </div>
        </td>
        <td style="font-size:0.75rem;color:var(--text-muted);">集計L-19</td>
      </tr>
      <!-- 残り（06〜10）は同じ構造で追加 -->
    </tbody>
  </table>
  <div class="figure-caption">
    重要度スコア = (予測密度 x 0.4) + (ミラツク親和性 x 0.35) + (確からしさ x 0.25)。
    密度戦略: 既存フォーサイトが集中する領域でミラツク独自視点を確立。
    空白戦略: フォーサイトの構造的空白に先行参入。
    出典: 集計[L-XX]、評価ルーブリックは verification.html 参照。
  </div>
</div>
```

---

### D. 系譜図（Genealogy / Timeline）

**用途**: 概念・トレンドの影響関係をタイムライン上に示す。
**推奨幅**: 100%（SVG viewBox で伸縮）
**形式**: インライン SVG。`currentColor` + CSS変数連携でダークモード対応。
**ファイル依存**: なし

```html
<style>
.genealogy-svg { width: 100%; height: auto; overflow: visible; }
.genealogy-axis     { stroke: var(--border);      stroke-width: 1; }
.genealogy-line     { stroke: var(--accent-warm); stroke-width: 1.5; fill: none; }
.genealogy-line-sub { stroke: var(--text-muted);  stroke-width: 1;   fill: none;
                      stroke-dasharray: 4 3; }
.genealogy-node     { fill: var(--card);   stroke: var(--accent-warm); stroke-width: 1.5; }
.genealogy-node-sub { fill: var(--card);   stroke: var(--border);      stroke-width: 1; }
.genealogy-text     { font-family: "Noto Sans JP", sans-serif; font-size: 11px;
                      fill: var(--text); text-anchor: middle; }
.genealogy-text-sub { fill: var(--text-secondary); }
.genealogy-year     { font-family: "SF Mono","Fira Code",monospace; font-size: 10px;
                      fill: var(--text-muted); text-anchor: middle; }
.genealogy-arrow     { fill: var(--accent-warm); }
.genealogy-arrow-sub { fill: var(--text-muted); }
</style>

<div class="figure" id="figD-sample">
  <div class="figure-title">図表D: 概念系譜図（ダミーデータ — 3系統の影響関係）</div>
  <svg class="genealogy-svg" viewBox="0 0 720 260"
       role="img" aria-label="概念系譜図（3系統）">
    <defs>
      <marker id="arrow-red" markerWidth="8" markerHeight="8"
              refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" class="genealogy-arrow"/>
      </marker>
      <marker id="arrow-gray" markerWidth="8" markerHeight="8"
              refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" class="genealogy-arrow-sub"/>
      </marker>
    </defs>

    <!-- タイムライン軸 -->
    <line x1="40" y1="230" x2="700" y2="230" class="genealogy-axis"/>

    <!-- 年代ラベル -->
    <text x="80"  y="248" class="genealogy-year">1990</text>
    <text x="200" y="248" class="genealogy-year">2000</text>
    <text x="320" y="248" class="genealogy-year">2010</text>
    <text x="440" y="248" class="genealogy-year">2020</text>
    <text x="560" y="248" class="genealogy-year">2030</text>
    <text x="660" y="248" class="genealogy-year">2050</text>

    <!-- グリッド線 -->
    <line x1="80"  y1="20" x2="80"  y2="230" class="genealogy-axis" stroke-dasharray="2 4"/>
    <line x1="200" y1="20" x2="200" y2="230" class="genealogy-axis" stroke-dasharray="2 4"/>
    <line x1="320" y1="20" x2="320" y2="230" class="genealogy-axis" stroke-dasharray="2 4"/>
    <line x1="440" y1="20" x2="440" y2="230" class="genealogy-axis" stroke-dasharray="2 4"/>
    <line x1="560" y1="20" x2="560" y2="230" class="genealogy-axis" stroke-dasharray="2 4"/>
    <line x1="660" y1="20" x2="660" y2="230" class="genealogy-axis" stroke-dasharray="2 4"/>

    <!-- 系統A（主系列: 赤ライン） -->
    <rect x="40" y="42" width="80" height="28" rx="2" class="genealogy-node"/>
    <text x="80" y="60" class="genealogy-text">概念A1</text>
    <line x1="122" y1="56" x2="190" y2="56"
          class="genealogy-line" marker-end="url(#arrow-red)"/>
    <rect x="192" y="42" width="80" height="28" rx="2" class="genealogy-node"/>
    <text x="232" y="60" class="genealogy-text">概念A2</text>
    <line x1="274" y1="56" x2="310" y2="56"
          class="genealogy-line" marker-end="url(#arrow-red)"/>
    <rect x="312" y="42" width="80" height="28" rx="2" class="genealogy-node"/>
    <text x="352" y="60" class="genealogy-text">概念A3</text>
    <line x1="394" y1="56" x2="550" y2="56"
          class="genealogy-line" marker-end="url(#arrow-red)"/>
    <!-- 将来ノード（破線枠） -->
    <rect x="552" y="42" width="80" height="28" rx="2"
          fill="rgba(204,20,0,0.06)" stroke="#CC1400" stroke-width="1.5"
          stroke-dasharray="4 2"/>
    <text x="592" y="60" class="genealogy-text" font-weight="700">A4（推定）</text>

    <!-- 系統B（補助系列: グレーライン） -->
    <rect x="160" y="112" width="80" height="28" rx="2" class="genealogy-node-sub"/>
    <text x="200" y="130" class="genealogy-text genealogy-text-sub">概念B1</text>
    <rect x="310" y="112" width="80" height="28" rx="2" class="genealogy-node-sub"/>
    <text x="350" y="130" class="genealogy-text genealogy-text-sub">概念B2</text>
    <line x1="242" y1="126" x2="308" y2="126"
          class="genealogy-line-sub" marker-end="url(#arrow-gray)"/>
    <!-- B2 → A3 クロス影響 -->
    <line x1="350" y1="112" x2="352" y2="72"
          class="genealogy-line-sub" marker-end="url(#arrow-gray)"/>

    <!-- 系統C（第三系列） -->
    <rect x="390" y="170" width="90" height="28" rx="2" class="genealogy-node-sub"/>
    <text x="435" y="188" class="genealogy-text genealogy-text-sub">概念C1</text>
    <rect x="530" y="170" width="90" height="28" rx="2" class="genealogy-node-sub"/>
    <text x="575" y="188" class="genealogy-text genealogy-text-sub">概念C2</text>
    <line x1="482" y1="184" x2="528" y2="184"
          class="genealogy-line-sub" marker-end="url(#arrow-gray)"/>
    <!-- C2 → A4 クロス影響 -->
    <line x1="575" y1="170" x2="592" y2="72"
          class="genealogy-line-sub" marker-end="url(#arrow-gray)"/>
  </svg>
  <div class="figure-caption">
    実線赤矢印=主要影響関係、破線灰矢印=補助影響関係。
    破線枠ノードは【推定】（実DB未確認）。
    出典: [DB名] / 集計[L-XX]。
  </div>
</div>
```

---

### E. ヒートマップ（Heat Map）

**用途**: ホライズン x テーマの2次元密度マトリクス。Track 1 の実装を標準とする。
**推奨幅**: 100%（グリッド列数に応じて grid-template-columns を調整）
**形式**: HTML CSSグリッド（`.heatmap`クラス）。セル数が多い場合は `overflow-x: auto`。
**ファイル依存**: なし

強度クラス（`.h-0`〜`.h-5`）は Section 1.3 の CSS を使用する。

```html
<style>
.heatmap {
  display: grid;
  gap: 1px;
  background: var(--border-light);
  border: 1px solid var(--border);
  font-family: var(--font);
  font-size: 0.78rem;
  overflow-x: auto;
}
.heatmap > div {
  background: var(--card);
  padding: 8px 10px;
  line-height: 1.5;
}
.heatmap > div.head {
  background: var(--surface);
  font-weight: 700;
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-align: center;
  letter-spacing: 0.03em;
}
.heatmap > div.row-label {
  background: var(--surface);
  font-weight: 700;
  font-size: 0.80rem;
}
.heatmap > div:not(.head):not(.row-label) { text-align: center; }
@media (max-width: 700px) {
  .heatmap { font-size: 0.70rem; }
  .heatmap > div { padding: 6px 6px; }
}
</style>

<div class="figure" id="figE-sample">
  <div class="figure-title">図表E: ホライズン x L1テーマ ヒートマップ（ダミーデータ）</div>
  <!-- 列数: 1(ラベル) + 4(ホライズン) + 1(合計) = 6列 -->
  <div class="heatmap" style="grid-template-columns: 200px repeat(4, 1fr) 80px;">
    <!-- ヘッダー -->
    <div class="head">L1領域</div>
    <div class="head">2030</div>
    <div class="head">2050</div>
    <div class="head">2070</div>
    <div class="head">2100</div>
    <div class="head">計</div>

    <!-- データ行 -->
    <div class="row-label">テクノロジー・AI</div>
    <div class="h-5">707</div><div class="h-3">103</div>
    <div class="h-1">5</div><div class="h-1">2</div><div class="h-5">817</div>

    <div class="row-label">経済・金融</div>
    <div class="h-4">409</div><div class="h-2">43</div>
    <div class="h-0">0</div><div class="h-1">1</div><div class="h-4">453</div>

    <div class="row-label">環境・気候</div>
    <div class="h-3">155</div><div class="h-3">79</div>
    <div class="h-1">1</div><div class="h-2">9</div><div class="h-3">244</div>

    <div class="row-label">地政学・安全保障</div>
    <div class="h-3">139</div><div class="h-1">21</div>
    <div class="h-1">1</div><div class="h-1">6</div><div class="h-3">167</div>

    <div class="row-label">社会・人口動態</div>
    <div class="h-2">88</div><div class="h-2">33</div>
    <div class="h-1">2</div><div class="h-1">1</div><div class="h-2">124</div>

    <div class="row-label">ガバナンス・制度</div>
    <div class="h-2">64</div><div class="h-1">4</div>
    <div class="h-0">0</div><div class="h-0">0</div><div class="h-1">68</div>
  </div>
  <div class="figure-caption">
    セルの色濃度は予測件数に対応（白=0件→濃赤=最大）。
    h-0〜h-5 のしきい値は各トラックの最大値に合わせて相対設定する（付録参照）。
    出典: [DB名] / 集計[L-XX]。
  </div>
</div>
```

---

### F. サイクル図（Cycle Diagram）

**用途**: 周期性・循環プロセスの可視化（4〜6ステップ）。
**推奨幅**: 320px（中央配置）またはモバイルで 100%
**形式**: インライン SVG。`currentColor` + CSS変数でダークモード対応。
**ファイル依存**: なし

```html
<!--
  4ステップ版 計算メモ:
  中心 cx=160 cy=160, 弧半径 r=110
  円周: 2 x π x 110 = 691.15
  25% の弧長: 172.8px, gap(矢印スペース): 14px
  stroke-dasharray: "158.8 532.35"
  各ステップの stroke-dashoffset: 0 / -172.8 / -345.6 / -518.4
  ノード位置（弧の中央=45°刻み）:
    STEP01: 45°  → (237.8, 82.2)
    STEP02: 135° → (237.8, 237.8)
    STEP03: 225° → (82.2, 237.8)
    STEP04: 315° → (82.2, 82.2)
-->
<style>
.cycle-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}
.cycle-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 12px 24px;
  font-family: var(--font);
  font-size: 0.78rem;
  color: var(--text-secondary);
  max-width: 480px;
  justify-content: center;
}
.cycle-legend .item { display: flex; align-items: center; gap: 6px; }
.cycle-legend .swatch {
  width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0;
}
</style>

<div class="figure" id="figF-sample">
  <div class="figure-title">図表F: 4段階サイクル図（ダミーデータ）</div>
  <div class="cycle-wrap">
    <svg viewBox="0 0 320 320" width="320" height="320"
         style="max-width:100%;"
         role="img" aria-label="4段階サイクル図">

      <!-- ベース円（背景トラック） -->
      <circle cx="160" cy="160" r="110"
              fill="none" stroke="var(--border-light)" stroke-width="22"/>

      <!-- STEP01（上: 12時〜3時） 赤 -->
      <circle cx="160" cy="160" r="110"
              fill="none" stroke="#CC1400" stroke-width="22"
              stroke-dasharray="158.8 532.35" stroke-dashoffset="0"
              transform="rotate(-90 160 160)"/>
      <!-- STEP02（右: 3時〜6時） 深赤 -->
      <circle cx="160" cy="160" r="110"
              fill="none" stroke="#6E2C2C" stroke-width="22"
              stroke-dasharray="158.8 532.35" stroke-dashoffset="-172.8"
              transform="rotate(-90 160 160)"/>
      <!-- STEP03（下: 6時〜9時） グレー -->
      <circle cx="160" cy="160" r="110"
              fill="none" stroke="#999999" stroke-width="22"
              stroke-dasharray="158.8 532.35" stroke-dashoffset="-345.6"
              transform="rotate(-90 160 160)"/>
      <!-- STEP04（左: 9時〜12時） ベージュ -->
      <circle cx="160" cy="160" r="110"
              fill="none" stroke="#C8B4A0" stroke-width="22"
              stroke-dasharray="158.8 532.35" stroke-dashoffset="-518.4"
              transform="rotate(-90 160 160)"/>

      <!-- ノード（各弧の中央） -->
      <!-- STEP01: 45° = (160+110×cos45°, 160-110×sin45°) = (237.8, 82.2) -->
      <circle cx="237.8" cy="82.2" r="22"
              fill="var(--card)" stroke="#CC1400" stroke-width="2"/>
      <text x="237.8" y="78" text-anchor="middle"
            font-family="'Noto Sans JP',sans-serif" font-size="9"
            fill="var(--text)" font-weight="700">STEP</text>
      <text x="237.8" y="90" text-anchor="middle"
            font-family="'SF Mono','Fira Code',monospace" font-size="12"
            fill="#CC1400" font-weight="700">01</text>

      <!-- STEP02: 135° = (237.8, 237.8) -->
      <circle cx="237.8" cy="237.8" r="22"
              fill="var(--card)" stroke="#6E2C2C" stroke-width="2"/>
      <text x="237.8" y="233" text-anchor="middle"
            font-family="'Noto Sans JP',sans-serif" font-size="9"
            fill="var(--text)" font-weight="700">STEP</text>
      <text x="237.8" y="245" text-anchor="middle"
            font-family="'SF Mono','Fira Code',monospace" font-size="12"
            fill="#6E2C2C" font-weight="700">02</text>

      <!-- STEP03: 225° = (82.2, 237.8) -->
      <circle cx="82.2" cy="237.8" r="22"
              fill="var(--card)" stroke="#999999" stroke-width="2"/>
      <text x="82.2" y="233" text-anchor="middle"
            font-family="'Noto Sans JP',sans-serif" font-size="9"
            fill="var(--text)" font-weight="700">STEP</text>
      <text x="82.2" y="245" text-anchor="middle"
            font-family="'SF Mono','Fira Code',monospace" font-size="12"
            fill="#999999" font-weight="700">03</text>

      <!-- STEP04: 315° = (82.2, 82.2) -->
      <circle cx="82.2" cy="82.2" r="22"
              fill="var(--card)" stroke="#C8B4A0" stroke-width="2"/>
      <text x="82.2" y="78" text-anchor="middle"
            font-family="'Noto Sans JP',sans-serif" font-size="9"
            fill="var(--text)" font-weight="700">STEP</text>
      <text x="82.2" y="90" text-anchor="middle"
            font-family="'SF Mono','Fira Code',monospace" font-size="12"
            fill="#C8B4A0" font-weight="700">04</text>

      <!-- 中央ラベル -->
      <text x="160" y="154" text-anchor="middle"
            font-family="'Noto Sans JP',sans-serif" font-size="10"
            fill="var(--text-muted)">サイクル</text>
      <text x="160" y="170" text-anchor="middle"
            font-family="'Noto Sans JP',sans-serif" font-size="10"
            fill="var(--text-muted)">名称</text>

      <!-- 外部テキストラベル（ノード周辺） -->
      <text x="237.8" y="48" text-anchor="middle"
            font-family="'Noto Sans JP',sans-serif" font-size="10"
            fill="var(--text)" font-weight="700">フェーズ名A</text>
      <text x="283" y="244" text-anchor="start"
            font-family="'Noto Sans JP',sans-serif" font-size="10"
            fill="var(--text)" font-weight="700">フェーズ名B</text>
      <text x="82.2" y="274" text-anchor="middle"
            font-family="'Noto Sans JP',sans-serif" font-size="10"
            fill="var(--text)" font-weight="700">フェーズ名C</text>
      <text x="14" y="80" text-anchor="end"
            font-family="'Noto Sans JP',sans-serif" font-size="10"
            fill="var(--text)" font-weight="700">フェーズ名D</text>
    </svg>

    <div class="cycle-legend">
      <div class="item">
        <div class="swatch" style="background:#CC1400;"></div>フェーズ名A
      </div>
      <div class="item">
        <div class="swatch" style="background:#6E2C2C;"></div>フェーズ名B
      </div>
      <div class="item">
        <div class="swatch" style="background:#999999;"></div>フェーズ名C
      </div>
      <div class="item">
        <div class="swatch" style="background:#C8B4A0;"></div>フェーズ名D
      </div>
    </div>
  </div>
  <div class="figure-caption">
    4段階サイクルの各弧が一ステップを示す。ステップ番号は弧の中央ノードに表示。
    出典: [DB名] / 集計[L-XX]。
  </div>
</div>
```

---

## 3. 図表サイズ規格

### 3.1 幅・高さの基本ルール

| 図版種別 | デスクトップ幅 | モバイル幅（<600px） | 高さの指定方法 |
|---|---|---|---|
| A. ホライズンマップ | 100%（max 760px） | 100%（overflow-x: auto） | 行数×セル高（自動） |
| B-1. バーチャート | 100% | 100% | 自動（行数に依存） |
| B-2. ドーナツ | 200px SVG + 凡例 | 縦積み（1fr） | viewBox で縦横比維持 |
| C. TOP10テーブル | 100% | 100% | 自動 |
| D. 系譜図 | 100% SVG | 100% | viewBox="0 0 720 260" |
| E. ヒートマップ | 100%（max 760px） | overflow-x: auto | 行数×セル高（自動） |
| F. サイクル図 | 320px（中央） | max-width: 320px; width: 100% | viewBox="0 0 320 320" |

### 3.2 `.figure` コンテナの余白

```css
.figure { margin: 40px 0; padding: 24px; }
```

同一章内に3点以上図版が連続する場合は `margin-bottom: 24px` に縮小可。

### 3.3 キャプション・タイトル配置ルール

- `.figure-title` は図版本体の**上部**（大文字、赤色 `var(--accent-warm)`）
- `.figure-caption` は図版本体の**下部**（出典必須）
- 上部キャプション配置は禁止

### 3.4 凡例配置

| 図版 | 凡例位置 |
|---|---|
| バーチャート | ラベルを棒の左側（`.label` クラス）。凡例不要 |
| ドーナツ | SVGの右側（`.donut-wrap` グリッド + `.legend`） |
| ヒートマップ | `.figure-caption` 内に文言説明 |
| 系譜図 | `.figure-caption` 内に矢印の意味を説明 |
| サイクル図 | SVGの下に `.cycle-legend` |
| ホライズンマップ | `.figure-caption` 内に強み評価の意味を説明 |

### 3.5 モバイル縮小ルール（< 600px）

- バーチャート: ラベル幅 180px → 120px
- ドーナツ: `grid-template-columns: 1fr`（縦積み）
- ヒートマップ: `overflow-x: auto` でスクロール（フォント 0.78rem → 0.70rem）
- 系譜図・サイクル: `width: 100%; height: auto`（SVG の viewBox が縦横比を維持）
- ランキングテーブル: スコアバーを `display: none` で非表示

---

## 4. タイポグラフィ規格（SVG内文字）

### 4.1 フォント指定

SVG内の `font-family` は以下の順で指定する（Google Fontsでロード済みの前提）:

```
"'Noto Sans JP', 'Hiragino Sans', -apple-system, sans-serif"
```

本文（Noto Serif JP）はSVG内では使用しない。UI・データラベルに Noto Sans JP を統一する。
章番号・数値ラベルには等幅フォントを使用する:

```
"'SF Mono', 'Fira Code', monospace"
```

### 4.2 文字サイズ階層

| 用途 | font-size | font-weight | 備考 |
|---|---|---|---|
| 図版タイトル（`.figure-title`） | 0.85rem（CSS外） | 700 | SVG外のCSSで制御 |
| データラベル（数値・%） | 12〜13px | 700 | 等幅フォント推奨 |
| 軸ラベル（テーマ名・年代） | 10〜11px | 400 | 長い場合は略称化（ルール4.3参照） |
| 凡例テキスト | 10px | 400 | - |
| 補助テキスト（補足説明） | 9px | 400 | これ以下は使わない |
| キャプション（`.figure-caption`） | 0.78rem（CSS外） | 400 | SVG外のCSSで制御 |

### 4.3 軸ラベルの省略ルール

SVG内の軸ラベルが長い場合、以下の優先順で短縮する:

1. 括弧内を除去（「テクノロジー・デジタル（ICT含む）」→「テクノロジー・デジタル」）
2. 後半を除去（「環境・気候変動」→「環境・気候」）
3. 英字略称は最終手段（「テクノロジー・AI」→「Tech/AI"）

---

## 5. アクセシビリティ

### 5.1 色覚多様性対応（ColorBlind-safe 設計）

赤白CI の赤（#CC1400）と白・グレーの組み合わせは、
第1色盲（赤色弱）では赤がほぼグレーに見えるため、色のみでデータを区別しない。

必須対応一覧:

| 図版 | 対応 |
|---|---|
| ヒートマップ | セルに数値テキストを必ず表示 |
| バーチャート | バーの右に数値ラベル（`.bar-val`）を必ず表示 |
| ドーナツ | 凡例（`.legend`）に文字と割合を併記 |
| 系譜図 | 実線/破線で関係の種類を区別（色のみに依存しない） |
| サイクル図 | ステップ番号（01/02/03/04）をノード内に表示 |
| ランキング | 戦略区分を文字バッジ（`.rank-badge`）で表現 |

### 5.2 ARIA 属性

SVG要素には以下を必ず付与する:

```html
<svg role="img" aria-label="[図版の内容を一文で説明]">
```

複雑な図版には `<title>` 要素を SVG 内に追加する:

```html
<svg role="img" aria-labelledby="fig-title-N">
  <title id="fig-title-N">ホライズン x L1テーマ ヒートマップ（2030〜2100年の予測件数分布）</title>
```

### 5.3 印刷時のグレースケール対応 CSS

report.html の `<style>` 内に以下を追加する（_template-akashiro.html の @media print を拡張）:

```css
@media print {
  /* バーチャート: 枠線で識別を補完 */
  .bar-chart .row .bar-bar { border: 1px solid #000000; }

  /* ヒートマップ: セル枠線を追加 + グレースケールフォールバック */
  .heatmap > div { border: 0.5px solid #999999; }
  .h-4, .h-5    { font-weight: 700; }
  .h-0 { background: #FFFFFF !important; }
  .h-1 { background: #F0EDED !important; color: #121212 !important; }
  .h-2 { background: #D6CFCF !important; color: #121212 !important; }
  .h-3 { background: #A89B9B !important; color: #121212 !important; }
  .h-4 { background: #6B5555 !important; color: #FFFFFF !important; }
  .h-5 { background: #3D2B2B !important; color: #FFFFFF !important; }

  /* 図版は改ページ禁止 */
  .figure { break-inside: avoid; }

  /* サイドバー・top-bar は印刷非表示（_BRIEFING.md 準拠） */
  .top-bar, .toc-sidebar { display: none; }
  .book-layout { grid-template-columns: 1fr; }
  .book-main { padding: 0; }
}
```

---

## 6. ダークモード対応

### 6.1 `currentColor` の活用

SVGのテキスト（`fill`）と線（`stroke`）には可能な限り `currentColor` を使用する。
これにより、`body { color: var(--text); }` の変化がSVGに自動伝播する。

```html
<!-- 推奨 -->
<text fill="currentColor" ...>ラベル</text>
<line stroke="currentColor" .../>

<!-- 非推奨（ダークモードで暗背景に埋もれる） -->
<text fill="#121212" ...>ラベル</text>
```

### 6.2 CSS変数との連携手順

1. SVG を `<div class="figure">` でラップする（インラインSVG）
2. SVG の `fill` / `stroke` に CSS変数を参照する
3. `:root` と `[data-theme="dark"]` で変数値を切り替える

```css
.genealogy-node { fill: var(--card); stroke: var(--accent-warm); }
.genealogy-text { fill: var(--text); }
.genealogy-axis { stroke: var(--border); }
```

外部SVGファイル（`<img src="*.svg">`）では CSS変数が効かない。
**必ずインラインSVGとして埋め込む**こと。

### 6.3 ヒートマップのダークモード対応

Section 1.3 の `[data-theme="dark"] .h-N` ルールをそのまま使用する。
ライトモードは `rgba(204,20,0, ...)` ベース、ダークモードは `rgba(255,64,48, ...)` ベース。
`h-4`/`h-5` では `color: #FFFFFF` を明示して視認性を確保する。

### 6.4 ドーナツ・サイクル図のダークモード

弧の `stroke` に直接 HEX 値（`#CC1400` 等）を指定しているため、
ダークモードでも弧の色は変わらない（これは意図した挙動）。
中央テキストには `fill="currentColor"` を使用して背景色と対比させる。

---

## 7. 使用チェックリスト（図版単位）

report.html に図版を追加するたびに以下を確認する:

- [ ] `.figure` ラッパーを使用し `id="figN"` を付与
- [ ] `.figure-title` に「図表N:」番号と出典ラベルを記載
- [ ] `.figure-caption` に出典（DB名 / 集計L-XX）を記載
- [ ] 色のみでデータを区別していない（数値/テキスト/形状を併用）
- [ ] SVG に `role="img"` と `aria-label` を付与
- [ ] ダークモードで色が正常（CSS変数 or currentColor を使用）
- [ ] `@media print` でグレースケール対応済み
- [ ] モバイル（<600px）でレイアウト調整済み
- [ ] 推定値には本文中に【推定】タグ付き説明を追記
- [ ] 絵文字・アイコンフォント未使用

---

## 付録: ヒートマップしきい値の決め方

`h-0`〜`h-5` のクラスをどの件数に割り当てるかは、
各トラックの最大値に対する相対比率で設定する。

| クラス | 条件 | 件数例（最大値 707 の場合） |
|---|---|---|
| h-0 | 0件 | 0件 |
| h-1 | 最大値の 0〜5% | 1〜35件 |
| h-2 | 最大値の 5〜20% | 36〜141件 |
| h-3 | 最大値の 20〜40% | 142〜282件 |
| h-4 | 最大値の 40〜70% | 283〜494件 |
| h-5 | 最大値の 70〜100% | 495〜707件 |

各トラックで最大値が異なるため、クラス割り当てはトラックごとに再計算すること。

---

_以上。本文書は領域策定プロジェクト全トラック（Track 1〜9）共通の図版規格として適用する。_
_更新が必要な場合は図版デザインリード（design agent）を通じてオーケストレーターへ連絡。_
