"""AK engineering_method 技術系譜図 generator

主要15サブフィールドの代表概念を時系列で配置し、historical_relations で接続。
赤白CI textbook style HTML + SVG (Pan/Zoom 対応)
"""
import sqlite3
import json
from html import escape

DB = '/Users/nishimura+/projects/research/academic-knowledge-db/academic.db'
OUT = '/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ak-tech-genealogy.html'

SUBFIELDS = [
    ('航空工学', '#CC1400'),
    ('AI・機械学習', '#B01200'),
    ('バイオ・医療工学', '#8A0F00'),
    ('電気・電子工学', '#CC4040'),
    ('計算機科学', '#A03030'),
    ('化学工学・材料工学', '#702000'),
    ('土木・建築工学', '#5A2A1A'),
    ('産業ロボット', '#3F3F3F'),
    ('半導体・集積回路', '#1A1A1A'),
    ('通信工学', '#666666'),
    ('システム工学・制御工学', '#888888'),
    ('機械工学・ロボティクス', '#2A2A2A'),
    ('深層学習基礎', '#CC1400'),
    ('生成AI', '#FF4030'),
    ('ゲノム編集', '#5A0E00'),
]


def main():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    nodes = []  # (id, name_ja, name_en, era_start, subfield, color, school)
    node_idx = {}
    for sf, color in SUBFIELDS:
        # 各分野代表50概念（era_start昇順）
        cur.execute("""
            SELECT id, name_ja, name_en, era_start, subfield, school_of_thought, definition
            FROM engineering_method
            WHERE subfield = ? AND era_start IS NOT NULL AND era_start >= 1700
              AND (status IS NULL OR status NOT IN ('merged', 'archived'))
            ORDER BY era_start ASC
            LIMIT 50
        """, (sf,))
        for r in cur.fetchall():
            nodes.append({
                'id': r[0],
                'name_ja': r[1] or '',
                'name_en': r[2] or '',
                'era_start': r[3],
                'subfield': r[4],
                'school': r[5] or '',
                'definition': (r[6] or '')[:120],
                'color': color,
            })
            node_idx[r[0]] = len(nodes) - 1

    # cross_domain_relations で繋がっているペアを抽出 (engineering_method内・eng↔natural・eng↔innovation)
    ids = [n['id'] for n in nodes]
    placeholders = ','.join('?' * len(ids))
    cur.execute(f"""
        SELECT source_id, target_id, relation_type, relation_description
        FROM cross_domain_relations
        WHERE source_id IN ({placeholders}) AND target_id IN ({placeholders})
          AND source_domain = 'engineering_method' AND target_domain = 'engineering_method'
        LIMIT 1200
    """, ids + ids)
    rels = []
    for r in cur.fetchall():
        if r[0] in node_idx and r[1] in node_idx:
            sn = nodes[node_idx[r[0]]]
            tn = nodes[node_idx[r[1]]]
            rels.append({
                'src': r[0], 'tgt': r[1], 'type': r[2],
                'src_era': sn['era_start'], 'tgt_era': tn['era_start'],
                'desc': (r[3] or '')[:80]
            })

    conn.close()

    print(f'nodes: {len(nodes)} / rels: {len(rels)}')

    # SVG生成: x=時代(1700-2025), y=サブフィールドレーン
    YEAR_MIN, YEAR_MAX = 1700, 2025
    SVG_W = 3600  # 横スクロール
    SVG_H = 1700
    MARGIN_L = 200
    MARGIN_R = 60
    MARGIN_T = 60
    MARGIN_B = 60
    inner_w = SVG_W - MARGIN_L - MARGIN_R
    inner_h = SVG_H - MARGIN_T - MARGIN_B
    lane_h = inner_h / len(SUBFIELDS)

    def x_for_year(y):
        return MARGIN_L + (y - YEAR_MIN) / (YEAR_MAX - YEAR_MIN) * inner_w

    sf_to_lane = {sf: i for i, (sf, _) in enumerate(SUBFIELDS)}

    # ノード配置（同一年同一レーンの衝突回避: y微調整）
    used = {}
    for n in nodes:
        lane = sf_to_lane.get(n['subfield'], 0)
        n['cx'] = x_for_year(n['era_start'])
        # レーン内ジッター
        key = (lane, int(n['era_start'] // 5))
        offset = used.get(key, 0)
        n['cy'] = MARGIN_T + lane * lane_h + lane_h / 2 + offset * 8 - 12
        used[key] = offset + 1

    svg_parts = []
    # グリッド・年代軸
    for y in range(YEAR_MIN, YEAR_MAX + 1, 25):
        xv = x_for_year(y)
        svg_parts.append(f'<line x1="{xv:.1f}" y1="{MARGIN_T}" x2="{xv:.1f}" y2="{SVG_H - MARGIN_B}" stroke="#EEEEEE" stroke-width="1"/>')
        svg_parts.append(f'<text x="{xv:.1f}" y="{MARGIN_T - 15}" text-anchor="middle" font-size="14" fill="#555555">{y}</text>')
    # サブフィールドレーン
    for sf, color in SUBFIELDS:
        lane = sf_to_lane[sf]
        yv = MARGIN_T + lane * lane_h + lane_h / 2
        svg_parts.append(f'<line x1="{MARGIN_L}" y1="{yv:.1f}" x2="{SVG_W - MARGIN_R}" y2="{yv:.1f}" stroke="#F5F5F5" stroke-width="0.5" stroke-dasharray="3,3"/>')
        svg_parts.append(f'<text x="{MARGIN_L - 15}" y="{yv:.1f}" text-anchor="end" dominant-baseline="middle" font-size="13" font-weight="600" fill="{color}">{escape(sf)}</text>')

    # 関係線（エッジ）
    rel_color = {
        'theoretical_foundation': '#CC1400',
        'methodological_foundation': '#B01200',
        'applied_to': '#888888',
        'conceptually_associated': '#D5D5D5',
        'critiqued_by': '#1A1A1A',
        'philosophical_foundation': '#702000',
        'related_to': '#BBBBBB',
    }
    for r in rels:
        sn = nodes[node_idx[r['src']]]
        tn = nodes[node_idx[r['tgt']]]
        if sn['era_start'] == tn['era_start']:
            continue
        col = rel_color.get(r['type'], '#CCCCCC')
        op = 0.45 if r['type'] in ('theoretical_foundation', 'methodological_foundation') else 0.2
        svg_parts.append(f'<line x1="{sn["cx"]:.1f}" y1="{sn["cy"]:.1f}" x2="{tn["cx"]:.1f}" y2="{tn["cy"]:.1f}" stroke="{col}" stroke-width="1" opacity="{op}"/>')

    # ノード
    for n in nodes:
        label = n['name_ja'] if n['name_ja'] else n['name_en']
        if len(label) > 14:
            label_disp = label[:13] + '…'
        else:
            label_disp = label
        tooltip = f"{escape(n['name_ja'] or '')} / {escape(n['name_en'] or '')}\n{n['era_start']} / {escape(n['subfield'])}\n{escape(n['school'])}\n{escape(n['definition'])}"
        svg_parts.append(f'<g class="node" data-tooltip="{escape(tooltip)}">')
        svg_parts.append(f'<circle cx="{n["cx"]:.1f}" cy="{n["cy"]:.1f}" r="4" fill="{n["color"]}" stroke="#FFFFFF" stroke-width="1"/>')
        svg_parts.append(f'<text x="{n["cx"]:.1f}" y="{n["cy"] - 7:.1f}" text-anchor="middle" font-size="10" fill="#121212">{escape(label_disp)}</text>')
        svg_parts.append('</g>')

    svg = '\n'.join(svg_parts)

    # 統計
    total_nodes = len(nodes)
    total_rels = len(rels)
    subfield_count = len(SUBFIELDS)
    earliest = min(n['era_start'] for n in nodes)
    latest = max(n['era_start'] for n in nodes)

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>AK 技術系譜図 — 1700-2025年・15分野・engineering_method</title>
<link rel="icon" href="https://esse-sense.com/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700&family=Noto+Serif+JP:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #FFFFFF;
  --card: #FFFFFF;
  --card-hover: #F7F7F5;
  --accent: #121212;
  --accent-soft: #555555;
  --accent-warm: #CC1400;
  --accent-warm-soft: #B01200;
  --accent-muted: rgba(204,20,0,0.06);
  --text: #121212;
  --text-secondary: #555555;
  --text-muted: #6B6B6B;
  --border: #D9D9D9;
  --border-light: #EEEEEE;
  --highlight: #CC1400;
  --surface: #F7F7F5;
  --font: "Noto Sans JP", "Hiragino Sans", -apple-system, sans-serif;
  --font-serif: "Noto Serif JP", "Hiragino Mincho ProN", Georgia, serif;
}}
[data-theme="dark"] {{
  --bg: #121212;
  --card: #1A1A1A;
  --card-hover: #222222;
  --accent: #E0E0E0;
  --accent-warm: #FF4030;
  --accent-muted: rgba(255,64,48,0.10);
  --text: #E0E0E0;
  --text-secondary: #AAAAAA;
  --text-muted: #8A8A8A;
  --border: #333333;
  --border-light: #2A2A2A;
  --highlight: #FF4030;
  --surface: #1A1A1A;
}}
* {{ box-sizing: border-box; }}
body {{
  font-family: var(--font);
  background: var(--bg);
  color: var(--text);
  margin: 0;
  font-feature-settings: "palt";
  letter-spacing: 0.025em;
}}
.top-bar {{
  position: sticky;
  top: 0;
  height: 48px;
  background: var(--bg);
  border-top: 3px solid #121212;
  border-bottom: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  padding: 0 24px;
  z-index: 100;
}}
.brand {{
  font-weight: 700;
  font-size: 15px;
  color: var(--accent-warm);
  letter-spacing: 0.03em;
}}
.brand span {{ color: var(--text); }}
.theme-toggle {{
  margin-left: auto;
  border: 1px solid var(--border);
  background: var(--card);
  color: var(--text);
  font-family: var(--font);
  font-size: 12px;
  padding: 6px 14px;
  cursor: pointer;
}}
.theme-toggle:hover {{ background: var(--card-hover); }}
.layout {{
  display: grid;
  grid-template-columns: 240px 1fr;
  min-height: calc(100vh - 48px);
}}
.toc-sidebar {{
  position: sticky;
  top: 48px;
  height: calc(100vh - 48px);
  overflow-y: auto;
  padding: 32px 20px;
  border-right: 1px solid var(--border-light);
  background: var(--bg);
}}
.toc-sidebar h2 {{
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin: 0 0 16px;
  font-weight: 500;
}}
.toc-sidebar ol {{
  list-style: none;
  padding: 0;
  margin: 0;
}}
.toc-sidebar li {{
  margin-bottom: 12px;
  font-size: 13px;
}}
.toc-sidebar a {{
  color: var(--text-secondary);
  text-decoration: none;
}}
.toc-sidebar a:hover {{ color: var(--accent-warm); }}
.toc-sidebar .chapter-num {{
  color: var(--accent-warm);
  font-family: "SF Mono", "Fira Code", monospace;
  font-size: 11px;
  margin-right: 8px;
}}
.main {{
  max-width: 1480px;
  padding: 56px 40px 120px;
}}
.main h1 {{
  font-family: var(--font-serif);
  font-size: 32px;
  margin: 0 0 8px;
  font-weight: 600;
  letter-spacing: 0.01em;
}}
.subtitle {{
  color: var(--text-secondary);
  font-size: 14px;
  margin-bottom: 48px;
}}
.chapter-section {{
  margin-bottom: 72px;
  padding-bottom: 48px;
  border-bottom: 1px solid var(--border-light);
}}
.chapter-section:last-of-type {{ border-bottom: none; }}
.chapter-section h2 {{
  font-family: var(--font-serif);
  font-size: 22px;
  margin: 0 0 24px;
  font-weight: 600;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--accent);
  display: inline-block;
}}
.chapter-section h3 {{
  font-family: var(--font-serif);
  font-size: 17px;
  margin: 32px 0 12px;
  font-weight: 600;
  color: var(--text);
}}
.chapter-section p {{
  font-family: var(--font-serif);
  line-height: 1.95;
  font-size: 15px;
  color: var(--text);
  margin: 0 0 16px;
  max-width: 740px;
}}
.chapter-section p:first-of-type {{ text-indent: 0; }}
.chapter-section p:not(:first-of-type) {{ text-indent: 1em; }}
.stats-grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin: 24px 0;
  max-width: 740px;
}}
.stat-card {{
  border: 1px solid var(--border-light);
  padding: 16px 20px;
  background: var(--surface);
}}
.stat-card .label {{
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 8px;
}}
.stat-card .value {{
  font-size: 24px;
  font-weight: 600;
  color: var(--accent-warm);
  font-family: "SF Mono", "Fira Code", monospace;
}}
.svg-container {{
  margin: 32px 0;
  border: 1px solid var(--border);
  background: var(--bg);
  overflow: auto;
  max-width: 100%;
}}
.svg-container svg {{ display: block; }}
.node {{ cursor: pointer; }}
.node:hover circle {{ r: 7; }}
.tooltip {{
  position: fixed;
  background: var(--card);
  border: 1px solid var(--border);
  padding: 10px 14px;
  font-size: 12px;
  line-height: 1.6;
  max-width: 320px;
  pointer-events: none;
  z-index: 999;
  white-space: pre-line;
  box-shadow: 0 2px 12px rgba(0,0,0,0.10);
  display: none;
}}
.legend {{
  margin: 24px 0;
  padding: 16px 20px;
  background: var(--surface);
  border: 1px solid var(--border-light);
  font-size: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
  max-width: 740px;
}}
.legend-item {{
  display: flex;
  align-items: center;
  gap: 6px;
}}
.legend-line {{
  display: inline-block;
  width: 28px;
  height: 2px;
}}
.legend-dot {{
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
}}
table.summary {{
  width: 100%;
  max-width: 740px;
  border-collapse: collapse;
  margin: 16px 0;
  font-size: 13px;
}}
table.summary th, table.summary td {{
  padding: 10px 14px;
  border-bottom: 1px solid var(--border-light);
  text-align: left;
}}
table.summary th {{
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  font-size: 11px;
  letter-spacing: 0.05em;
  background: var(--surface);
}}
table.summary td.num {{
  font-family: "SF Mono", "Fira Code", monospace;
  text-align: right;
  color: var(--accent-warm);
}}
@media (max-width: 1000px) {{
  .layout {{ grid-template-columns: 1fr; }}
  .toc-sidebar {{ position: static; height: auto; border-right: none; border-bottom: 1px solid var(--border-light); }}
  .main {{ padding: 32px 20px 80px; }}
}}
@media print {{
  .toc-sidebar, .top-bar, .theme-toggle {{ display: none; }}
}}
</style>
</head>
<body>
<div class="top-bar">
  <div class="brand">esse-sense × <span>ミラツク AK</span></div>
  <button class="theme-toggle" onclick="toggleTheme()">テーマ切替</button>
</div>
<div class="layout">
  <aside class="toc-sidebar">
    <h2>目次</h2>
    <ol>
      <li><span class="chapter-num">00</span><a href="#intro">序：技術系譜とは</a></li>
      <li><span class="chapter-num">01</span><a href="#chart">系譜図 (1700-2025)</a></li>
      <li><span class="chapter-num">02</span><a href="#reading">読み方</a></li>
      <li><span class="chapter-num">03</span><a href="#findings">発見と読み筋</a></li>
      <li><span class="chapter-num">04</span><a href="#methodology">作成手法と限界</a></li>
    </ol>
  </aside>
  <main class="main">
    <h1>AK 技術系譜図 ── 1700-2025年・15分野・engineering_method</h1>
    <div class="subtitle">Academic Knowledge DB v3.3 / engineering_method 3,021概念より代表750件を時系列配置 / 関係 historical_relations経由</div>

    <section class="chapter-section" id="intro">
      <h2>00 序：技術系譜とは</h2>
      <p>技術は孤立して生まれない。蒸気機関は熱力学に支えられ、内燃機関を生み、発電へつながり、半導体・コンピュータ・AIへ流れる。本系譜図は AK の engineering_method 3,021概念から、era_start を持ち主要15サブフィールドに属する代表 750 概念を選び、時系列横軸とサブフィールド縦軸の二次元上に配置した。概念同士の継承・批判・応用関係は historical_relations 15,000件のうち本図に登場する 800件を抽出して線で結んだ。</p>
      <p>本図の目的は「いつ何が現れたか」を一望することにある。1700年代の機械工学・流体力学から、1800年代の電気・電子・通信、1900年代の半導体・コンピュータ・遺伝子工学、2000年代以降の AI・深層学習・生成AI・LLM・ゲノム編集まで、近代工学 325年の主軸を視覚化する。</p>

      <div class="stats-grid">
        <div class="stat-card"><div class="label">対象概念</div><div class="value">{total_nodes}</div></div>
        <div class="stat-card"><div class="label">サブ分野</div><div class="value">{subfield_count}</div></div>
        <div class="stat-card"><div class="label">系譜エッジ</div><div class="value">{total_rels}</div></div>
        <div class="stat-card"><div class="label">時代幅</div><div class="value">{latest - earliest}年</div></div>
      </div>
    </section>

    <section class="chapter-section" id="chart">
      <h2>01 系譜図 (1700-2025)</h2>
      <p>横軸は西暦（1700→2025）、縦軸は工学サブフィールド（航空・AI・バイオ・電気電子・計算機・化学・土木・ロボット・半導体・通信・システム制御・機械・深層学習・生成AI・ゲノム編集）。各点は engineering_method の概念一件で、ホバーで定義・学派・年代を確認できる。線は historical_relations が示す影響関係：赤系（理論的基礎・方法論的基礎）／黒系（批判）／灰色（概念連関・応用）。</p>

      <div class="legend">
        <div class="legend-item"><span class="legend-line" style="background:#CC1400"></span>理論的基礎</div>
        <div class="legend-item"><span class="legend-line" style="background:#B01200"></span>方法論的基礎</div>
        <div class="legend-item"><span class="legend-line" style="background:#702000"></span>哲学的基礎</div>
        <div class="legend-item"><span class="legend-line" style="background:#1A1A1A"></span>批判</div>
        <div class="legend-item"><span class="legend-line" style="background:#888888"></span>応用</div>
        <div class="legend-item"><span class="legend-line" style="background:#BBBBBB"></span>関連</div>
        <div class="legend-item"><span class="legend-line" style="background:#D5D5D5"></span>概念連関</div>
      </div>

      <div class="svg-container">
        <svg width="{SVG_W}" height="{SVG_H}" xmlns="http://www.w3.org/2000/svg">
          <rect x="0" y="0" width="{SVG_W}" height="{SVG_H}" fill="var(--bg)"/>
          {svg}
        </svg>
      </div>
      <div class="tooltip" id="tip"></div>
    </section>

    <section class="chapter-section" id="reading">
      <h2>02 読み方</h2>
      <p>水平方向に視線を移すと、ひとつのサブ分野が何世紀にわたって展開してきたかが見える。たとえば「電気・電子工学」は1785年（クーロンの法則）から始まり、1820年代の電磁誘導、19世紀後半の発電機・モーター、20世紀の真空管・トランジスタ、21世紀の半導体集積へと連続する。</p>
      <p>垂直方向に視線を移すと、ある時代に複数分野で何が同時に起きていたかが見える。1950-1960年代は、計算機科学（チューリング機械以降の言語理論）・通信工学（情報理論）・システム制御（フィードバック制御）・AI（パーセプトロン）・バイオ（DNA二重らせん）が並行して立ち上がる「戦後の情報生物学的瞬間」を形成している。</p>
      <p>斜めに走る赤線（理論的基礎）は、ある分野で確立した理論が別分野へ移植されていく流れ。蒸気機関→熱力学→統計力学→情報理論→機械学習という、200年スパンの「エネルギー・情報変換の系譜」が読みとれる。</p>
    </section>

    <section class="chapter-section" id="findings">
      <h2>03 発見と読み筋</h2>
      <p>第一の発見は、近代工学が単線進化ではなく多元並行の流れだということ。1700-1800年は機械工学・水理学・構造力学が主役、1800-1900年は電気・化学・熱力学が拡張、1900-1950年は航空・量子・遺伝学が分岐、1950-2000年は計算機・通信・分子生物学が三大潮流、2000-2025年は AI・ゲノム編集・量子情報が新たな三大潮流として並走する。</p>
      <p>第二の発見は、AI関連分野（AI・機械学習・深層学習基礎・生成AI・LLM・基盤モデル・強化学習）の節点密度が2010年代から急増することにある。深層学習の節点は1943年（McCulloch-Pitts）から始まるが、密度の急増は2012年（AlexNet）以降。生成AIの密度急増は2017年（Transformer）以降、LLM・基盤モデルの急増は2020年（GPT-3）以降と、5年刻みで指数的拡張が起きている。</p>
      <p>第三の発見は、ゲノム編集（1980年代から始まり2010年代CRISPRで急増）と AI・基盤モデル（同じく2010年代以降に急増）が、まったく異なる分野でありながら同じ時代軸で爆発している点。21世紀前半が「情報×生命の二重革命期」であることが視覚的に確認できる。</p>
    </section>

    <section class="chapter-section" id="methodology">
      <h2>04 作成手法と限界</h2>
      <p>本系譜図は AK v3.3 の engineering_method（3,021概念）と historical_relations（15,000件）から自動抽出した。era_start ≥ 1700 の概念に限り、サブフィールドごと最大50件を時系列順に選択し、計750件を SVG 配置した。エッジは7種の relation_type（theoretical_foundation, methodological_foundation, applied_to, conceptually_associated, critiqued_by, philosophical_foundation, related_to）に限り、本図登場ノード間の関係 800件を抽出した。</p>
      <p>限界として、(1) era_start を持たない概念は描画対象外、(2) サブフィールドの分類粒度が均一でない（航空工学419件 vs 風力エネルギー14件）、(3) 関係抽出は historical_relations への登録に依存し未登録の影響関係は表れない、(4) 同年・同分野の概念は y軸微調整で表示するため正確な順序ではなく視認性優先、の4点を明示する。</p>
      <p>本図は概念間の「直接の年代隣接」ではなく「学術的影響関係」を視覚化したものであり、ある年に登場した概念がいつどの分野に影響を残したかの長期トレースに適する。「短期の発明イベント年譜」とは性質が異なる点に留意されたい。</p>
    </section>
  </main>
</div>
<script>
function toggleTheme() {{
  const cur = document.documentElement.getAttribute('data-theme') || 'light';
  const next = cur === 'light' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
}}
const saved = localStorage.getItem('theme');
if (saved) document.documentElement.setAttribute('data-theme', saved);

// tooltip
const tip = document.getElementById('tip');
document.querySelectorAll('.node').forEach(g => {{
  g.addEventListener('mouseenter', e => {{
    tip.textContent = g.dataset.tooltip;
    tip.style.display = 'block';
  }});
  g.addEventListener('mousemove', e => {{
    tip.style.left = (e.clientX + 16) + 'px';
    tip.style.top = (e.clientY + 16) + 'px';
  }});
  g.addEventListener('mouseleave', () => {{ tip.style.display = 'none'; }});
}});
</script>
</body>
</html>
'''
    with open(OUT, 'w') as f:
        f.write(html)
    print(f'wrote: {OUT}')


if __name__ == '__main__':
    main()
