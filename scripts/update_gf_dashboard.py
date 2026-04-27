#!/usr/bin/env python3
"""Update GF dashboard HTML with latest system patterns from JSON data."""

import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA_FILE = BASE / "data" / "gf_system_patterns.json"
HTML_FILE = BASE / "dashboards" / "gf.html"


def build_pattern_cards(patterns: list) -> str:
    """Generate HTML for systemic pattern cards."""
    cards = []
    for p in patterns:
        # Build example rows
        examples_html = ""
        for ex in p.get("examples", []):
            examples_html += (
                f'<div class="ev">'
                f'<div class="ev-p">{ex["era"]}</div>'
                f'<div class="ev-t">{ex["case"]}</div>'
                f'</div>\n'
            )

        card = f"""<div class="pcard">
  <div class="pcard-h">
    <div>
      <div class="pcard-name">{p["name_ja"]} ({p["name_en"]})</div>
    </div>
    <div class="pcard-meta">
      <span class="badge b-dim">{p["system_archetype"]}</span>
      <span class="badge b-cnt">{p["event_count"]} events</span>
    </div>
  </div>
  <div class="pcard-b">
    <div style="font-size:.84rem;line-height:1.8;margin-bottom:12px">{p["description_ja"]}</div>
    <h3 style="font-size:.82rem;margin:12px 0 8px">歴史的事例</h3>
{examples_html}  </div>
</div>"""
        cards.append(card)
    return "\n".join(cards)


def build_decision_archetypes(archetypes: list) -> str:
    """Generate HTML for decision archetypes section."""
    rows = []
    for a in archetypes:
        persons = ", ".join(ex["person"] for ex in a.get("examples", []))
        row = f"""<div style="border:1px solid var(--border);padding:14px 18px;margin-bottom:10px">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <div style="font-weight:700;font-size:.88rem">{a["name_ja"]} ({a["name_en"]})</div>
    <span class="badge b-cnt">{a["count"]} instances</span>
  </div>
  <div style="font-size:.78rem;color:var(--text-secondary);margin-top:6px">
    {persons}
  </div>
</div>"""
        rows.append(row)
    return "\n".join(rows)


def build_universal_concepts(concepts: list) -> str:
    """Generate HTML for universal concepts grid."""
    badges = []
    for c in concepts:
        badges.append(
            f'<span style="font-size:.72rem;padding:4px 10px;background:var(--surface);'
            f'border:1px solid var(--border-light)">{c["name_en"]} ({c["frequency"]})</span>'
        )
    return '<div style="display:flex;flex-wrap:wrap;gap:6px">\n' + "\n".join(badges) + "\n</div>"


def main():
    # Load JSON data
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    patterns = data["systemic_patterns"]
    archetypes = data["decision_archetypes"]
    concepts = data["universal_concepts"]

    # Read HTML
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # --- Update overview stats ---
    # Change "20" 発見パターン to "12"
    html = html.replace(
        '<div class="ov-val">20</div><div class="ov-lab">発見パターン</div>',
        '<div class="ov-val">12</div><div class="ov-lab">発見パターン</div>'
    )
    # Change "19" 新規発見 to "12"
    html = html.replace(
        '<div class="ov-val">19</div><div class="ov-lab">新規発見</div>',
        '<div class="ov-val">12</div><div class="ov-lab">新規発見</div>'
    )

    # --- Replace pattern section ---
    # Find the section between the patterns h2 and the next h2
    pattern_h2 = "<h2>発見されたシステムパターンと予測的解釈</h2>"
    # Find start and end positions
    start_idx = html.find(pattern_h2)
    if start_idx == -1:
        raise ValueError("Could not find pattern section h2")

    # Find the next <h2> after the pattern section
    after_pattern = html.find("<h2>", start_idx + len(pattern_h2))
    if after_pattern == -1:
        raise ValueError("Could not find next h2 after pattern section")

    # Build new section content
    new_section = f"""{pattern_h2}
<p class="note">{len(patterns)}のシステムパターン、{len(archetypes)}の決定アーキタイプ、{len(concepts)}の普遍的概念を表示。各パターンに歴史的事例を統合表示。</p>

{build_pattern_cards(patterns)}

<h2>決定アーキタイプ</h2>
<p class="note">歴史的人物の意思決定パターンを{len(archetypes)}類型に分類。各類型の代表的人物を表示。</p>

{build_decision_archetypes(archetypes)}

<h2>普遍的概念 TOP {len(concepts)}</h2>
<p class="note">歴史的事例から抽出された、時代を超えて繰り返し出現する普遍的な経営・戦略概念。</p>

{build_universal_concepts(concepts)}

"""

    # Replace the section
    html = html[:start_idx] + new_section + html[after_pattern:]

    # Write updated HTML
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Updated {HTML_FILE}")
    print(f"  Patterns: {len(patterns)}")
    print(f"  Decision archetypes: {len(archetypes)}")
    print(f"  Universal concepts: {len(concepts)}")


if __name__ == "__main__":
    main()
