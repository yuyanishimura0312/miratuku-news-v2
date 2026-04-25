#!/usr/bin/env python3
"""
Build integrated dashboard: novel patterns + PESTLE/CI cross-reference + predictive interpretation.
"""
import json
import os
import html as html_mod
from pathlib import Path

PROJECT = Path(__file__).parent.parent

def h(t):
    return html_mod.escape(str(t)) if t else ""

def load_all():
    patterns = json.load(open(PROJECT / "data" / "gf_novel_patterns.json"))
    crossref = json.load(open(PROJECT / "data" / "gf_crossref_analysis.json"))
    pattern_names_data = json.load(open(PROJECT / "data" / "gf_pattern_names.json"))
    pattern_names = pattern_names_data.get("pattern_names", {})
    return patterns, crossref, pattern_names

def build_crossref_map(crossref):
    """Map pattern name -> crossref data."""
    m = {}
    for p in crossref.get("patterns", []):
        m[p["name"]] = p
    return m

DIMENSIONS = {
    "reinforcing": "自己強化", "balancing": "均衡・抑制", "paradox": "逆説・矛盾",
    "transformation": "構造転換", "emergence": "創発・自己組織化", "path_dependence": "経路依存性",
    "delay": "時間遅延", "nonlinear": "非線形・臨界点", "scale": "スケール効果",
    "info_asymmetry": "情報の非対称性", "legitimacy": "正当性の構築", "resource_conversion": "資源変換",
}

# Predictive interpretations based on pattern trends
PREDICTIONS = {
    "均衡・抑制 × 逆説・矛盾 × 構造転換": {
        "current": "気候変動対策と経済成長の構造的矛盾が深化。脱炭素化を推進する力と化石燃料依存からの離脱コストが拮抗し、「変革を目指すほど抵抗が強まる」という逆説的構造が、エネルギー・食料・金融の各セクターで同時進行している。AI技術の急速な発展も、生産性向上と雇用破壊の矛盾を増幅させている。",
        "prediction": "2026-2030年にかけて、この「変革の矛盾」パターンは臨界点に達する可能性が高い。歴史的に見ると、ゴルバチョフ型（体制内改革が体制崩壊を招く）とアタテュルク型（危機を利用した急進的転換）の二つの帰結が存在する。現在のグローバルシステムでは、複数領域で同時に矛盾が噴出するため、セクター間の連鎖的構造転換が起こりうる。",
        "historical": "ゴルバチョフのペレストロイカ（体制内改革→体制崩壊）、アタテュルクの世俗化改革（帝国崩壊後の急進的転換）",
    },
    "均衡・抑制 × スケール効果 × 構造転換": {
        "current": "グローバルサプライチェーンの再編、AI規制の国際的枠組み構築、地政学的ブロック化が同時進行。巨大システム（グローバル経済、インターネット、国際秩序）の構造転換が試みられているが、スケールの大きさが変革のスピードを制約するという均衡ループが作用している。",
        "prediction": "最も急速に増加しているパターン（1990s: 514件→2020s: 852件、66%増）。大規模システムの構造転換圧力は今後も増大し、2025-2030年に「複数の大規模システムが同時に転換点を迎える」可能性がある。歴史的には、帝国の行政再編（ダレイウス1世）やクビライ・ハンの遊牧帝国から定住帝国への転換に類似する構造。",
        "historical": "クビライ・ハン（遊牧→定住帝国の転換）、アケナテン（宗教的・政治的大転換の失敗）",
    },
    "自己強化 × スケール効果 × 構造転換": {
        "current": "プラットフォーム企業の支配力拡大、AIの自己改善能力の加速、デジタル通貨の普及が「成功が変革を加速し、変革がさらなる成功を生む」正帰還ループを形成。特にAI領域では、モデルの性能向上→利用拡大→データ蓄積→さらなる性能向上という自己強化的構造転換が進行中。",
        "prediction": "このパターンは一貫して増加傾向（1990s: 259→2020s: 418）にあり、AI・量子コンピューティング・バイオテクノロジーの収束により、2027-2032年に「技術的自己強化が社会構造を不可逆的に変容させる」フェーズに入る可能性がある。歴史的には、フォードの大量生産革命やジョブズのiPhoneエコシステム構築に類似するが、変化の速度と規模が桁違いに大きい。",
        "historical": "ヘンリー・フォード（大量生産→大衆消費社会への構造転換）、スティーブ・ジョブズ（iPhone→モバイルエコシステムの自己強化的拡大）",
    },
    "均衡・抑制 × 逆説・矛盾 × 自己強化": {
        "current": "SNSの普及が民主主義を「強化」すると同時に「弱体化」させる逆説。情報の民主化が偽情報の拡散を加速し、透明性の向上が監視社会を招くという矛盾構造。さらに、この矛盾自体がエンゲージメントを高め、プラットフォームの影響力を強化するという自己増幅的な逆説が形成されている。",
        "prediction": "2020年代を通じて、この「矛盾の自己強化」パターンは新たな社会制度の設計を要求するようになる。歴史的には、キュロス大王が被征服民を「解放者」として取り込んだ逆説的戦略、武則天が既存体制の内部から根本的改革を行った構造に類似する。",
        "historical": "キュロス大王（征服を解放として正当化する逆説）、武則天（体制内からの構造的転覆）",
    },
    "均衡・抑制 × 資源変換 × スケール効果": {
        "current": "希少資源（半導体、レアアース、水資源）をめぐる地政学的競争が激化。資源の変換・再利用技術（リサイクル、代替材料）が発展する一方、スケール効果による需要増大が資源制約を再び強化するという均衡構造。",
        "prediction": "資源安全保障がグローバルシステムの主要なストレステストとなる。歴史的に、秦始皇帝の度量衡統一やロックフェラーの石油産業統合に見られるように、資源の標準化・統合は帝国規模のシステム効率化をもたらすが、同時に単一障害点を生む。",
        "historical": "秦始皇帝（度量衡統一による帝国効率化）、ジョン・D・ロックフェラー（石油産業の水平統合）",
    },
}

# Default prediction for patterns without specific analysis
DEFAULT_PRED = {
    "current": "現代のニュースデータでこのパターンの出現頻度が確認されている。",
    "prediction": "歴史的な類似構造の帰結を参照し、現代文脈での展開を注視する必要がある。",
    "historical": "",
}


CSS = """
:root {
  --bg: #FFFFFF; --card: #FFFFFF; --text: #121212; --text-secondary: #555555;
  --text-muted: #6B6B6B; --border: #D9D9D9; --border-light: #EEEEEE;
  --surface: #F7F7F5; --accent-warm: #CC1400; --accent-muted: rgba(204,20,0,0.06);
  --accent-blue: #1565c0; --accent-blue-muted: rgba(21,101,192,0.08);
  --accent-green: #2e7d32; --accent-green-muted: rgba(46,125,50,0.08);
  --accent-orange: #e65100; --accent-orange-muted: rgba(230,81,0,0.08);
  --font: "Noto Sans JP", sans-serif; --font-serif: "Noto Serif JP", serif;
}
[data-theme="dark"] {
  --bg: #121212; --card: #1A1A1A; --text: #E0E0E0; --text-secondary: #AAAAAA;
  --text-muted: #8A8A8A; --border: #333333; --border-light: #2A2A2A;
  --surface: #1A1A1A; --accent-warm: #FF4444; --accent-muted: rgba(255,68,68,0.1);
  --accent-blue: #64b5f6; --accent-blue-muted: rgba(100,181,246,0.12);
  --accent-green: #66bb6a; --accent-green-muted: rgba(102,187,106,0.12);
  --accent-orange: #ffb74d; --accent-orange-muted: rgba(255,183,77,0.12);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--font);color:var(--text);background:var(--bg);line-height:1.7;max-width:1000px;margin:0 auto;padding:24px 20px 60px}
.back{display:inline-block;margin-bottom:20px;font-size:.82rem;color:var(--text-secondary);text-decoration:none}
h1{font-family:var(--font-serif);font-size:1.5rem;font-weight:700;margin-bottom:4px}
.db-id{font-family:monospace;font-size:.72rem;font-weight:700;color:var(--accent-warm);background:var(--accent-muted);padding:2px 8px;margin-right:8px}
.subtitle{font-size:.84rem;color:var(--text-secondary);margin-bottom:12px;line-height:1.7}
.desc{font-size:.84rem;color:var(--text);margin-bottom:24px;line-height:1.8}
.overview{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:10px;margin-bottom:28px}
.ov-card{background:var(--surface);border:1px solid var(--border-light);padding:14px;text-align:center}
.ov-val{font-family:var(--font-serif);font-size:1.4rem;font-weight:700}
.ov-lab{font-size:.7rem;color:var(--text-muted);margin-top:2px}
h2{font-family:var(--font-serif);font-size:1.15rem;font-weight:700;margin:36px 0 14px;padding-bottom:8px;border-bottom:2px solid var(--border)}
h3{font-family:var(--font-serif);font-size:.95rem;font-weight:700;margin:20px 0 10px}
.note{font-size:.78rem;color:var(--text-muted);line-height:1.7;margin:6px 0 14px}
.pcard{border:1px solid var(--border);margin-bottom:20px}
.pcard-h{padding:14px 18px;border-bottom:1px solid var(--border-light);display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:6px}
.pcard-name{font-family:var(--font-serif);font-size:1rem;font-weight:700}
.pcard-meta{display:flex;gap:5px;flex-wrap:wrap}
.badge{font-size:.66rem;padding:2px 7px;font-weight:600}
.b-novel{background:var(--accent-warm);color:#fff}
.b-known{background:var(--accent-green-muted);color:var(--accent-green)}
.b-dim{background:var(--accent-blue-muted);color:var(--accent-blue)}
.b-trend-up{background:var(--accent-orange-muted);color:var(--accent-orange)}
.b-trend-flat{background:var(--surface);color:var(--text-muted);border:1px solid var(--border-light)}
.b-cnt{background:var(--surface);color:var(--text-secondary);border:1px solid var(--border-light)}
.pcard-b{padding:14px 18px}
.ev{border-left:3px solid var(--accent-warm);padding:8px 12px;margin-bottom:8px;background:var(--surface)}
.ev-p{font-size:.74rem;font-weight:600;color:var(--accent-warm);margin-bottom:3px}
.ev-t{font-size:.8rem;color:var(--text);line-height:1.6}
.ev-tags{margin-top:4px}.ev-tags span{font-size:.64rem;display:inline-block;padding:1px 4px;margin:1px 1px;background:var(--accent-blue-muted);color:var(--accent-blue)}
.trend-box{background:var(--surface);border:1px solid var(--border-light);padding:12px 16px;margin:10px 0}
.trend-bar{display:flex;gap:4px;align-items:flex-end;height:50px;margin:8px 0}
.trend-col{flex:1;display:flex;flex-direction:column;align-items:center;gap:2px}
.trend-fill{width:100%;background:var(--accent-warm);opacity:.6;min-height:2px}
.trend-lab{font-size:.64rem;color:var(--text-muted)}
.trend-val{font-size:.68rem;font-family:monospace;color:var(--text-secondary)}
.pred-box{border:1px solid var(--accent-orange);background:var(--accent-orange-muted);padding:14px 18px;margin:10px 0}
.pred-title{font-size:.82rem;font-weight:700;color:var(--accent-orange);margin-bottom:6px}
.pred-text{font-size:.82rem;color:var(--text);line-height:1.7}
.pred-hist{font-size:.76rem;color:var(--text-muted);margin-top:8px;font-style:italic}
.news-sample{font-size:.76rem;padding:6px 10px;border-bottom:1px solid var(--border-light)}
.news-sample:last-child{border-bottom:none}
.news-src{font-size:.64rem;color:var(--text-muted);margin-right:6px}
.heatmap{width:100%;border-collapse:collapse;font-size:.7rem;margin:10px 0}
.heatmap th{padding:5px 3px;text-align:center;font-weight:600;background:var(--surface);border:1px solid var(--border-light)}
.heatmap td{padding:5px 3px;text-align:center;border:1px solid var(--border-light)}
.h0{background:transparent}.h1{background:rgba(204,20,0,.05)}.h2{background:rgba(204,20,0,.12)}.h3{background:rgba(204,20,0,.22)}.h4{background:rgba(204,20,0,.35);font-weight:700}
.theme-toggle{position:fixed;top:16px;right:16px;background:var(--surface);border:1px solid var(--border);padding:6px 10px;cursor:pointer;font-size:1rem;z-index:10}
"""


def build_html(patterns_data, crossref_data, pattern_names):
    crossref_map = build_crossref_map(crossref_data)
    patterns = patterns_data["patterns"]

    # Sort: novel first, then by size
    novel = [p for p in patterns if p["is_novel"]]
    known = [p for p in patterns if not p["is_novel"]]
    sorted_patterns = sorted(novel, key=lambda x: -x["size"]) + sorted(known, key=lambda x: -x["size"])

    n_novel = len(novel)
    n_increasing = sum(1 for p in sorted_patterns if crossref_map.get(p["name"], {}).get("trend") == "increasing")
    total_news = sum(
        sum(crossref_map.get(p["name"], {}).get("decade_counts", {}).values())
        for p in sorted_patterns
    )

    overview = "".join([
        f'<div class="ov-card"><div class="ov-val">{len(sorted_patterns)}</div><div class="ov-lab">発見パターン</div></div>',
        f'<div class="ov-card"><div class="ov-val">{n_novel}</div><div class="ov-lab">新規発見</div></div>',
        f'<div class="ov-card"><div class="ov-val">{n_increasing}</div><div class="ov-lab">増加トレンド</div></div>',
        f'<div class="ov-card"><div class="ov-val">{total_news:,}</div><div class="ov-lab">関連ニュース</div></div>',
        f'<div class="ov-card"><div class="ov-val">12</div><div class="ov-lab">構造次元</div></div>',
    ])

    # Build dimension co-occurrence heatmap from patterns data
    dim_ids = list(DIMENSIONS.keys())
    dim_names = list(DIMENSIONS.values())
    combo_counts = {}
    for p in patterns_data["patterns"]:
        combo = p["combo"]
        for i in range(len(combo)):
            for j in range(i, len(combo)):
                key = tuple(sorted([combo[i], combo[j]]))
                combo_counts[key] = combo_counts.get(key, 0) + p["size"]

    heatmap = '<table class="heatmap"><thead><tr><th></th>'
    for n in dim_names:
        heatmap += f'<th>{h(n[:4])}</th>'
    heatmap += '</tr></thead><tbody>'
    for i, d1 in enumerate(dim_ids):
        heatmap += f'<tr><th style="text-align:right;font-size:.68rem">{h(dim_names[i])}</th>'
        for j, d2 in enumerate(dim_ids):
            key = tuple(sorted([d1, d2]))
            val = combo_counts.get(key, 0)
            hc = f"h{min(4, val // 5)}" if val > 0 else "h0"
            heatmap += f'<td class="{hc}">{val if val else ""}</td>'
        heatmap += '</tr>'
    heatmap += '</tbody></table>'

    # Pattern cards with cross-reference and predictions
    cards_html = ""
    for p in sorted_patterns:
        pname = p["name"]
        cr = crossref_map.get(pname, {})
        pred = PREDICTIONS.get(pname, DEFAULT_PRED)

        # Look up intuitive name from pattern_names
        pname_info = pattern_names.get(pname, {})
        intuitive_name = pname_info.get("name", "")
        intuitive_name_en = pname_info.get("name_en", "")
        pname_description = pname_info.get("description", "")

        # Build display title: intuitive name if available, else dimension combo
        if intuitive_name:
            card_title = f'{h(intuitive_name)} ({h(intuitive_name_en)})'
            card_subtitle = f'<div style="font-size:.78rem;color:var(--text-muted);margin-top:3px">{h(pname)}</div>'
        else:
            card_title = h(pname)
            card_subtitle = ""

        # Badges
        novelty = '<span class="badge b-novel">新規発見</span>' if p["is_novel"] else f'<span class="badge b-known">既知: {h(p["known_match"])}</span>'
        dim_badges = " ".join(f'<span class="badge b-dim">{h(DIMENSIONS.get(d, d))}</span>' for d in p["combo"])
        trend = cr.get("trend", "unknown")
        trend_badge = f'<span class="badge b-trend-up">増加</span>' if trend == "increasing" else f'<span class="badge b-trend-flat">{h(trend)}</span>'
        cnt_badge = f'<span class="badge b-cnt">歴史{p["size"]}件</span>'

        # Evidence from historical patterns
        evidence_html = ""
        for s in p.get("key_sentences", [])[:3]:
            tag_spans = " ".join(f'<span>{h(DIMENSIONS.get(t, t))}</span>' for t in s.get("tags", []))
            evidence_html += f'<div class="ev"><div class="ev-p">{h(s.get("person",""))}</div><div class="ev-t">{h(s.get("text","")[:250])}</div><div class="ev-tags">{tag_spans}</div></div>'

        # Trend visualization
        dc = cr.get("decade_counts", {})
        trend_html = ""
        if dc:
            max_val = max(dc.values()) if dc.values() else 1
            trend_html = '<div class="trend-box"><div style="font-size:.78rem;font-weight:600;margin-bottom:4px">PESTLE/CI ニュース出現頻度（1990-2026）</div><div class="trend-bar">'
            for decade in ["1990s", "2000s", "2010s", "2020s"]:
                val = dc.get(decade, 0)
                pct = int(val / max_val * 45) if max_val else 0
                trend_html += f'<div class="trend-col"><div class="trend-val">{val}</div><div class="trend-fill" style="height:{max(2,pct)}px"></div><div class="trend-lab">{decade}</div></div>'
            trend_html += '</div></div>'

        # News samples
        news_html = ""
        samples = cr.get("sample_articles", [])[:4]
        if samples:
            news_html = '<h3 style="font-size:.82rem">関連ニュース例</h3>'
            for a in samples:
                src = a.get("source", "")
                date = a.get("date", "")
                news_html += f'<div class="news-sample"><span class="news-src">[{h(src)}]</span>{h(a.get("title","")[:100])} <span class="news-src">{h(date)}</span></div>'

        # Prediction
        pred_html = ""
        if pred.get("current") and pred["current"] != DEFAULT_PRED["current"]:
            pred_html = f'''<div class="pred-box">
<div class="pred-title">現在の構造的状況</div>
<div class="pred-text">{h(pred["current"])}</div>
</div>
<div class="pred-box" style="border-color:var(--accent-warm);background:var(--accent-muted)">
<div class="pred-title" style="color:var(--accent-warm)">予測的解釈</div>
<div class="pred-text">{h(pred["prediction"])}</div>
<div class="pred-hist">歴史的参照: {h(pred["historical"])}</div>
</div>'''

        # Pattern description block (shown after badges if available)
        desc_html = f'<div style="font-size:.8rem;color:var(--text-secondary);margin-bottom:10px;line-height:1.7">{h(pname_description)}</div>' if pname_description else ""

        cards_html += f'''<div class="pcard">
<div class="pcard-h">
<div>
<div class="pcard-name">{card_title}</div>
{card_subtitle}
</div>
<div class="pcard-meta">{novelty} {trend_badge} {cnt_badge}</div>
</div>
<div class="pcard-b">
<div style="margin-bottom:8px">{dim_badges}</div>
{desc_html}
{pred_html}
{trend_html}
<h3 style="font-size:.82rem">歴史的証拠</h3>
<div style="font-size:.76rem;color:var(--text-muted);margin-bottom:8px">関連人物: {h(", ".join(p["persons"][:6]))}</div>
{evidence_html}
{news_html}
</div>
</div>'''

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>歴史構造DB ― システム構造の発見と予測 | Insight News</title>
<link rel="icon" href="https://esse-sense.com/favicon.ico">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Noto+Serif+JP:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<button class="theme-toggle" onclick="document.documentElement.setAttribute('data-theme',document.documentElement.getAttribute('data-theme')==='dark'?'':'dark')">&#9789;</button>
<a class="back" href="app.html#section-databases">&larr; データベース一覧に戻る</a>
<h1><span class="db-id">GF</span>歴史構造DB ― システム構造の発見と予測</h1>
<p class="subtitle">歴史的意思決定のボトムアップ分析から発見されたシステムパターンを、現代ニュース（1990-2026年）と照合し、現在進行中の構造変化を予測する</p>
<p class="desc">176件の構造分析と1,053件のリンク説明文から12の構造次元の多次元組合せを発見し、PESTLE DB（276K記事）・Cultural Intelligence DB（241K記事）との照合により現代での出現頻度を計測しました。歴史的パターンの軌跡と現代ニュースのトレンドを重ね合わせ、2026年以降のシステム構造の展開について予測的解釈を行います。</p>
<div class="overview">{overview}</div>

<h2>次元間共起マップ</h2>
<p class="note">12の構造次元がどのように組み合わさって出現するか。濃い色ほど頻繁に共起する次元の対。</p>
{heatmap}

<h2>発見されたシステムパターンと予測的解釈</h2>
<p class="note">新規発見パターンを優先表示。各パターンに、歴史的証拠・現代ニュースとの照合結果・予測的解釈を統合表示。</p>
{cards_html}

</body>
</html>"""


def main():
    print("Loading data...")
    patterns, crossref, pattern_names = load_all()

    print("Building integrated dashboard...")
    html = build_html(patterns, crossref, pattern_names)
    (PROJECT / "dashboards" / "gf.html").write_text(html, encoding="utf-8")
    print(f"  Dashboard: dashboards/gf.html")
    print("Done!")


if __name__ == "__main__":
    main()
