#!/usr/bin/env python3
"""
Discover NOVEL system patterns from historical data.
Uses multi-dimensional causal tagging instead of keyword clustering.
Focuses on authentic text only (176 structures + 1,053 links).
"""
import json
import os
import re
import html as html_mod
from collections import Counter, defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CONSOLIDATED = PROJECT_ROOT / "data" / "gf_consolidated.json"
OUTPUT_HTML = PROJECT_ROOT / "dashboards" / "gf.html"
OUTPUT_JSON = PROJECT_ROOT / "data" / "gf_novel_patterns.json"

# ============================================================
# Structural dimensions (not archetypes)
# ============================================================
DIMENSIONS = {
    "reinforcing": {
        "name_ja": "自己強化",
        "keywords": ["拡大", "強化", "加速", "促進", "増大", "向上", "成長", "蓄積", "好循環", "正帰還", "相乗"],
    },
    "balancing": {
        "name_ja": "均衡・抑制",
        "keywords": ["抵抗", "制約", "限界", "低下", "弱体化", "衰退", "崩壊", "枯渇", "悪循環", "負帰還"],
    },
    "paradox": {
        "name_ja": "逆説・矛盾",
        "keywords": ["しかし", "一方で", "同時に", "反面", "矛盾", "ジレンマ", "逆に", "裏腹", "皮肉", "逆説", "背反"],
    },
    "transformation": {
        "name_ja": "構造転換",
        "keywords": ["転換", "変革", "変容", "転じ", "再定義", "再構築", "再編", "創造的破壊", "ピボット", "カニバリゼーション"],
    },
    "emergence": {
        "name_ja": "創発・自己組織化",
        "keywords": ["自律", "自己組織", "創発", "進化", "適応", "学習", "模倣", "伝播", "分権", "自治"],
    },
    "path_dependence": {
        "name_ja": "経路依存性",
        "keywords": ["経路依存", "ロックイン", "不可逆", "取り返し", "後戻り", "慣性", "固定化", "先行者", "初期条件"],
    },
    "delay": {
        "name_ja": "時間遅延",
        "keywords": ["遅延", "時間差", "タイムラグ", "数十年", "数世紀", "長期的に", "やがて", "徐々に", "世代を超え"],
    },
    "nonlinear": {
        "name_ja": "非線形・臨界点",
        "keywords": ["臨界", "閾値", "爆発的", "一気に", "突然", "急速", "雪崩", "連鎖", "相転移", "ティッピング"],
    },
    "scale": {
        "name_ja": "スケール効果",
        "keywords": ["帝国", "全体", "規模", "スケール", "巨大", "大規模", "広範", "波及", "システム全体"],
    },
    "info_asymmetry": {
        "name_ja": "情報の非対称性",
        "keywords": ["情報", "不確実", "未知", "予測", "偵察", "諜報", "隠蔽", "秘密", "可視化", "透明性"],
    },
    "legitimacy": {
        "name_ja": "正当性の構築",
        "keywords": ["正当", "権威", "信頼", "信用", "正統", "合法", "道徳", "倫理", "大義", "名分"],
    },
    "resource_conversion": {
        "name_ja": "資源変換",
        "keywords": ["変換", "転用", "再利用", "資源", "資本", "人材", "技術", "知識", "ネットワーク"],
    },
}


def load_authentic_data():
    """Load only authentic (non-template) text data."""
    with open(CONSOLIDATED) as f:
        raw = json.load(f)

    records = []
    # Structures: authentic reasoning/counterfactual text
    for s in raw["structures"]:
        person = s.get("person_name_en") or s.get("figure_name_en", "")
        event = s.get("event_title_en") or s.get("reform_name_en", "")
        texts = []
        for field in ["reasoning_ja", "counterfactual_ja", "constraints_ja", "situation_ja"]:
            t = s.get(field, "")
            if t and len(t) > 20:
                texts.append(t)
        if texts:
            records.append({
                "person": person,
                "event": event,
                "source": "structure",
                "all_text": " ".join(texts),
                "texts": texts,
            })

    # Links: authentic explanation text
    person_link_texts = defaultdict(list)
    for l in raw["links"]:
        expl = l.get("explanation_ja", "")
        if expl and len(expl) > 30:
            person = l.get("person_name_en", "")
            concept = l.get("concept_name_en", "")
            link_type = l.get("link_type", "")
            person_link_texts[person].append({
                "concept": concept,
                "type": link_type,
                "text": expl,
            })

    # Group link texts by person
    for person, link_list in person_link_texts.items():
        combined = " ".join(l["text"] for l in link_list)
        concepts = [l["concept"] for l in link_list]
        records.append({
            "person": person,
            "event": f"Conceptual links ({len(link_list)} concepts)",
            "source": "links",
            "all_text": combined,
            "texts": [l["text"] for l in link_list],
            "concepts": concepts,
        })

    return records, raw["events"], raw["concepts"], raw["links"]


def tag_dimensions(text):
    """Tag a text with structural dimensions."""
    tags = {}
    for dim_id, dim in DIMENSIONS.items():
        score = sum(1 for kw in dim["keywords"] if kw in text)
        if score >= 1:
            tags[dim_id] = score
    return tags


def extract_causal_sentences(text, person=""):
    """Extract sentences with causal structures."""
    sentences = [s.strip() for s in text.split("。") if len(s.strip()) > 20]
    results = []
    for sent in sentences:
        tags = tag_dimensions(sent)
        if len(tags) >= 2:  # Multi-dimensional = structurally interesting
            results.append({
                "text": sent,
                "tags": tags,
                "person": person,
            })
    return results


def discover_patterns(records):
    """Discover novel patterns from multi-dimensional tagging."""
    # Tag all records
    all_tagged = []
    for rec in records:
        tags = tag_dimensions(rec["all_text"])
        if tags:
            rec["tags"] = tags
            rec["tag_set"] = frozenset(tags.keys())
            all_tagged.append(rec)

    # Find structural combinations (2+ dimensions)
    combo_records = defaultdict(list)
    for rec in all_tagged:
        if len(rec["tags"]) >= 2:
            # Use top dimensions (sorted by score)
            top_dims = sorted(rec["tags"].items(), key=lambda x: -x[1])
            # Create combo key from top 2-3 dimensions
            key = tuple(sorted(d[0] for d in top_dims[:3]))
            combo_records[key].append(rec)

    # Filter: need at least 3 examples
    patterns = {}
    for combo, recs in combo_records.items():
        if len(recs) >= 3:
            patterns[combo] = recs

    # Sort by count
    patterns = dict(sorted(patterns.items(), key=lambda x: -len(x[1])))

    return patterns, all_tagged


def is_novel(combo):
    """Check if this combination maps to a known system archetype."""
    known_mappings = {
        ("balancing", "reinforcing"): "成長の限界 (Limits to Growth)",
        ("balancing", "reinforcing", "scale"): "成長の限界 (Limits to Growth)",
        ("delay", "reinforcing"): "目標の低下 (Eroding Goals)",
        ("paradox", "reinforcing"): "うまくいかない修正 (Fixes that Fail)",
        ("nonlinear", "reinforcing"): "エスカレーション (Escalation)",
        ("reinforcing", "scale"): "成功が成功を呼ぶ (Success to the Successful)",
    }
    return known_mappings.get(combo)


def characterize_pattern(combo, records):
    """Describe a discovered pattern."""
    dim_names = [DIMENSIONS[d]["name_ja"] for d in combo]
    name = " × ".join(dim_names)

    # Extract representative causal sentences
    key_sentences = []
    for rec in records[:10]:
        for sent in extract_causal_sentences(rec["all_text"], rec["person"]):
            if len(sent["tags"]) >= 2:
                key_sentences.append(sent)

    # Sort by tag count (most multi-dimensional first)
    key_sentences.sort(key=lambda x: -len(x["tags"]))

    # Unique persons
    persons = list(dict.fromkeys(r["person"] for r in records))

    known = is_novel(combo)

    return {
        "name": name,
        "combo": list(combo),
        "dim_names": dim_names,
        "size": len(records),
        "is_novel": known is None,
        "known_match": known,
        "persons": persons[:8],
        "key_sentences": key_sentences[:5],
        "source_mix": Counter(r["source"] for r in records),
    }


# ============================================================
# HTML generation
# ============================================================
def h(text):
    if text is None:
        return ""
    return html_mod.escape(str(text))


CSS = """
:root {
  --bg: #FFFFFF; --card: #FFFFFF; --text: #121212; --text-secondary: #555555;
  --text-muted: #6B6B6B; --border: #D9D9D9; --border-light: #EEEEEE;
  --surface: #F7F7F5; --accent-warm: #CC1400; --accent-muted: rgba(204,20,0,0.06);
  --accent-blue: #1565c0; --accent-blue-muted: rgba(21,101,192,0.08);
  --accent-green: #2e7d32; --accent-green-muted: rgba(46,125,50,0.08);
  --font: "Noto Sans JP", sans-serif; --font-serif: "Noto Serif JP", serif;
}
[data-theme="dark"] {
  --bg: #121212; --card: #1A1A1A; --text: #E0E0E0; --text-secondary: #AAAAAA;
  --text-muted: #8A8A8A; --border: #333333; --border-light: #2A2A2A;
  --surface: #1A1A1A; --accent-warm: #FF4444; --accent-muted: rgba(255,68,68,0.1);
  --accent-blue: #64b5f6; --accent-blue-muted: rgba(100,181,246,0.12);
  --accent-green: #66bb6a; --accent-green-muted: rgba(102,187,106,0.12);
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font); color: var(--text); background: var(--bg); line-height: 1.7; max-width: 1000px; margin: 0 auto; padding: 24px 20px 60px; }
.back { display: inline-block; margin-bottom: 20px; font-size: 0.82rem; color: var(--text-secondary); text-decoration: none; }
.back:hover { color: var(--text); }
h1 { font-family: var(--font-serif); font-size: 1.5rem; font-weight: 700; margin-bottom: 4px; }
.db-id { font-family: monospace; font-size: 0.72rem; font-weight: 700; color: var(--accent-warm); background: var(--accent-muted); padding: 2px 8px; margin-right: 8px; }
.subtitle { font-size: 0.84rem; color: var(--text-secondary); margin-bottom: 12px; line-height: 1.7; }
.desc { font-size: 0.84rem; color: var(--text); margin-bottom: 24px; line-height: 1.8; }
.overview { display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 10px; margin-bottom: 28px; }
.overview-card { background: var(--surface); border: 1px solid var(--border-light); padding: 14px; text-align: center; }
.overview-value { font-family: var(--font-serif); font-size: 1.4rem; font-weight: 700; }
.overview-label { font-size: 0.7rem; color: var(--text-muted); margin-top: 2px; }
h2 { font-family: var(--font-serif); font-size: 1.2rem; font-weight: 700; margin: 36px 0 16px; padding-bottom: 8px; border-bottom: 2px solid var(--border); }
h3 { font-family: var(--font-serif); font-size: 1rem; font-weight: 700; margin: 24px 0 12px; }
.pattern-card { border: 1px solid var(--border); margin-bottom: 20px; }
.pattern-header { padding: 16px 20px; border-bottom: 1px solid var(--border-light); }
.pattern-name { font-family: var(--font-serif); font-size: 1.05rem; font-weight: 700; margin-bottom: 6px; }
.pattern-meta { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
.badge { font-size: 0.68rem; padding: 2px 8px; font-weight: 600; }
.badge-novel { background: var(--accent-warm); color: white; }
.badge-known { background: var(--accent-green-muted); color: var(--accent-green); }
.badge-dim { background: var(--accent-blue-muted); color: var(--accent-blue); }
.badge-count { background: var(--surface); color: var(--text-secondary); border: 1px solid var(--border-light); }
.pattern-body { padding: 16px 20px; }
.pattern-desc { font-size: 0.82rem; color: var(--text-secondary); line-height: 1.7; margin-bottom: 14px; }
.pattern-persons { font-size: 0.78rem; color: var(--text-muted); margin-bottom: 14px; }
.evidence { border-left: 3px solid var(--accent-warm); padding: 10px 14px; margin-bottom: 10px; background: var(--surface); }
.evidence-person { font-size: 0.76rem; font-weight: 600; color: var(--accent-warm); margin-bottom: 4px; }
.evidence-text { font-size: 0.82rem; color: var(--text); line-height: 1.7; }
.evidence-tags { margin-top: 6px; }
.evidence-tags span { font-size: 0.66rem; display: inline-block; padding: 1px 5px; margin: 1px 2px; background: var(--accent-blue-muted); color: var(--accent-blue); }
.dim-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 8px; margin-bottom: 20px; }
.dim-card { padding: 10px 14px; background: var(--surface); border: 1px solid var(--border-light); }
.dim-name { font-weight: 600; font-size: 0.84rem; }
.dim-count { font-size: 0.76rem; color: var(--text-muted); margin-top: 2px; }
.dim-keywords { font-size: 0.7rem; color: var(--text-muted); font-family: monospace; margin-top: 4px; }
.heatmap { width: 100%; border-collapse: collapse; font-size: 0.72rem; }
.heatmap th { padding: 6px 4px; text-align: center; font-weight: 600; background: var(--surface); border: 1px solid var(--border-light); }
.heatmap td { padding: 6px 4px; text-align: center; border: 1px solid var(--border-light); }
.heat-0 { background: transparent; } .heat-1 { background: rgba(204,20,0,0.05); }
.heat-2 { background: rgba(204,20,0,0.12); } .heat-3 { background: rgba(204,20,0,0.2); }
.heat-4 { background: rgba(204,20,0,0.3); font-weight: 700; }
.note { font-size: 0.78rem; color: var(--text-muted); line-height: 1.7; margin: 8px 0; }
.theme-toggle { position: fixed; top: 16px; right: 16px; background: var(--surface); border: 1px solid var(--border); padding: 6px 10px; cursor: pointer; font-size: 1rem; z-index: 10; }
"""


def generate_html(patterns_list, dim_stats, combo_matrix, all_tagged, records):
    n_novel = sum(1 for p in patterns_list if p["is_novel"])
    n_known = sum(1 for p in patterns_list if not p["is_novel"])
    total_classified = sum(p["size"] for p in patterns_list)

    overview = "".join([
        f'<div class="overview-card"><div class="overview-value">{len(records)}</div><div class="overview-label">分析対象レコード</div></div>',
        f'<div class="overview-card"><div class="overview-value">{len(patterns_list)}</div><div class="overview-label">発見パターン</div></div>',
        f'<div class="overview-card"><div class="overview-value">{n_novel}</div><div class="overview-label">新規パターン</div></div>',
        f'<div class="overview-card"><div class="overview-value">{len(DIMENSIONS)}</div><div class="overview-label">構造次元</div></div>',
        f'<div class="overview-card"><div class="overview-value">{total_classified}</div><div class="overview-label">分類済み</div></div>',
    ])

    # Dimension overview
    dim_html = '<div class="dim-grid">'
    for dim_id, count in dim_stats.most_common():
        dim = DIMENSIONS[dim_id]
        kw_str = "、".join(dim["keywords"][:5])
        dim_html += f'<div class="dim-card"><div class="dim-name">{h(dim["name_ja"])}</div><div class="dim-count">{count}件のレコードで検出</div><div class="dim-keywords">{h(kw_str)}</div></div>'
    dim_html += '</div>'

    # Patterns (novel first)
    sorted_patterns = sorted(patterns_list, key=lambda p: (0 if p["is_novel"] else 1, -p["size"]))
    patterns_html = ""
    for i, p in enumerate(sorted_patterns):
        # Badge
        if p["is_novel"]:
            badge = '<span class="badge badge-novel">新規発見</span>'
        else:
            badge = f'<span class="badge badge-known">既知: {h(p["known_match"])}</span>'

        dim_badges = " ".join(f'<span class="badge badge-dim">{h(d)}</span>' for d in p["dim_names"])
        count_badge = f'<span class="badge badge-count">{p["size"]}件</span>'

        persons = ", ".join(p["persons"][:6])
        if len(p["persons"]) > 6:
            persons += f" 他{len(p['persons'])-6}名"

        # Evidence sentences
        evidence_html = ""
        for sent in p["key_sentences"][:4]:
            tag_spans = " ".join(f'<span>{h(DIMENSIONS[t]["name_ja"])}</span>' for t in sent["tags"] if t in DIMENSIONS)
            evidence_html += f'''<div class="evidence">
<div class="evidence-person">{h(sent["person"])}</div>
<div class="evidence-text">{h(sent["text"][:300])}</div>
<div class="evidence-tags">{tag_spans}</div>
</div>'''

        patterns_html += f'''<div class="pattern-card">
<div class="pattern-header">
<div class="pattern-name">{h(p["name"])}</div>
<div class="pattern-meta">{badge} {dim_badges} {count_badge}</div>
</div>
<div class="pattern-body">
<div class="pattern-persons">関連人物: {h(persons)}</div>
{evidence_html}
</div>
</div>'''

    # Heatmap: dimension co-occurrence
    dim_ids = list(DIMENSIONS.keys())
    dim_names = [DIMENSIONS[d]["name_ja"] for d in dim_ids]
    heatmap = '<table class="heatmap"><thead><tr><th></th>'
    for name in dim_names:
        heatmap += f'<th>{h(name[:4])}</th>'
    heatmap += '</tr></thead><tbody>'
    for i, d1 in enumerate(dim_ids):
        heatmap += f'<tr><th style="text-align:right">{h(dim_names[i])}</th>'
        for j, d2 in enumerate(dim_ids):
            key = tuple(sorted([d1, d2]))
            val = combo_matrix.get(key, 0)
            heat_class = f"heat-{min(4, val // 3)}" if val > 0 else "heat-0"
            heatmap += f'<td class="{heat_class}">{val if val > 0 else ""}</td>'
        heatmap += '</tr>'
    heatmap += '</tbody></table>'

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>歴史構造DB ― 新規システムパターンの発見 | Insight News</title>
<link rel="icon" href="https://esse-sense.com/favicon.ico">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Noto+Serif+JP:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<button class="theme-toggle" onclick="document.documentElement.setAttribute('data-theme',document.documentElement.getAttribute('data-theme')==='dark'?'':'dark')">&#9789;</button>
<a class="back" href="app.html#section-databases">&larr; データベース一覧に戻る</a>
<h1><span class="db-id">GF</span>歴史構造DB ― 新規システムパターンの発見</h1>
<p class="subtitle">176の構造分析と1,053のリンク説明文から、12の構造次元の組合せとしてシステムパターンをボトムアップに発見する</p>
<p class="desc">既知のシステムアーキタイプ（成長の限界、エスカレーション等）に当てはめるのではなく、歴史的テキストに含まれる12の構造次元（自己強化、均衡、逆説、構造転換、創発、経路依存性、時間遅延、非線形性、スケール効果、情報非対称性、正当性、資源変換）の組合せパターンを発見します。2つ以上の次元が同時に出現する文は、単一次元のパターンより構造的に豊かな知見を含みます。</p>
<div class="overview">{overview}</div>

<h2>1. 構造次元の検出状況</h2>
<p class="note">12の構造次元がオリジナルテキスト中にどの程度検出されたか。各次元のキーワード群は事前定義だが、次元の「組合せ」はデータから発見される。</p>
{dim_html}

<h2>2. 次元間共起ヒートマップ</h2>
<p class="note">どの次元の組合せが頻出するかを示す。濃い色ほど共起頻度が高い。対角線上は単独出現数。既知アーキタイプに対応しない高頻度の組合せが、新規パターンの候補である。</p>
{heatmap}

<h2>3. 発見されたパターン（新規発見を優先表示）</h2>
<p class="note">2次元以上の組合せで3件以上のレコードが該当するパターン。各パターンに「新規発見」または「既知アーキタイプとの対応」を付与。証拠テキストは176の構造分析と1,053のリンク説明文から抽出したオリジナル文。</p>
{patterns_html}

</body>
</html>"""


# ============================================================
# Main
# ============================================================
def main():
    print("Loading authentic data...")
    records, events, concepts, links = load_authentic_data()
    print(f"  {len(records)} records (structures + link groups)")

    print("Tagging dimensions...")
    dim_stats = Counter()
    for rec in records:
        tags = tag_dimensions(rec["all_text"])
        rec["tags"] = tags
        for dim in tags:
            dim_stats[dim] += 1
    print(f"  Dimensions detected: {dict(dim_stats.most_common())}")

    print("Discovering patterns...")
    patterns, all_tagged = discover_patterns(records)
    print(f"  {len(patterns)} combination patterns found")

    # Build combo matrix for heatmap
    combo_matrix = Counter()
    for rec in records:
        dims = list(rec.get("tags", {}).keys())
        for i in range(len(dims)):
            combo_matrix[tuple(sorted([dims[i], dims[i]]))] += 1  # diagonal
            for j in range(i + 1, len(dims)):
                combo_matrix[tuple(sorted([dims[i], dims[j]]))] += 1

    # Characterize patterns
    patterns_list = []
    for combo, recs in list(patterns.items())[:20]:
        char = characterize_pattern(combo, recs)
        patterns_list.append(char)

    n_novel = sum(1 for p in patterns_list if p["is_novel"])
    print(f"  Novel: {n_novel}, Known: {len(patterns_list) - n_novel}")

    print("Generating HTML...")
    html = generate_html(patterns_list, dim_stats, combo_matrix, all_tagged, records)
    OUTPUT_HTML.write_text(html, encoding="utf-8")
    print(f"  Dashboard: {OUTPUT_HTML}")

    # Save JSON
    json_data = {
        "patterns": [
            {
                "name": p["name"],
                "combo": p["combo"],
                "size": p["size"],
                "is_novel": p["is_novel"],
                "known_match": p["known_match"],
                "persons": p["persons"],
                "key_sentences": [{"person": s["person"], "text": s["text"][:200], "tags": list(s["tags"].keys())} for s in p["key_sentences"]],
            }
            for p in patterns_list
        ],
        "dimensions": {k: {"name": v["name_ja"], "count": dim_stats[k]} for k, v in DIMENSIONS.items()},
        "total_records": len(records),
    }
    with open(OUTPUT_JSON, "w") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"  JSON: {OUTPUT_JSON}")

    print("\nDone!")


if __name__ == "__main__":
    main()
