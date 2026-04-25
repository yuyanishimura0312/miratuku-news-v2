#!/usr/bin/env python3
"""
generate_cla_text.py

Fetch CLA historical data (yearly + quarterly + meta report) from the
future-insight-app GitHub Pages data source and emit a single,
human-readable text file bundling all 36 years of analysis.

Output: data/cla_36years_analysis.txt

Run: python3 scripts/generate_cla_text.py
"""
from __future__ import annotations

import json
import sys
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

DATA_BASE = "https://yuyanishimura0312.github.io/future-insight-app/data"
FILES = {
    "yearly": f"{DATA_BASE}/cla_historical_yearly.json",
    "quarterly": f"{DATA_BASE}/cla_historical_quarterly.json",
    "meta": f"{DATA_BASE}/cla_meta_report.json",
}

CATEGORY_LABELS = {
    "Political": "政治",
    "Economic": "経済",
    "Social": "社会",
    "Technological": "技術",
    "Legal": "法律",
    "Environmental": "環境",
}
CATEGORY_ORDER = [
    "Political",
    "Economic",
    "Social",
    "Technological",
    "Legal",
    "Environmental",
]

# 4 layers of CLA + auxiliary synthesis fields
LAYER_LABELS = {
    "litany": "Litany (表層・出来事)",
    "systemic_causes": "Systemic Causes (システム的原因)",
    "worldview": "Worldview (世界観・イデオロギー)",
    "myth_metaphor": "Myth / Metaphor (神話・メタファー)",
    "key_tension": "Key Tension (主要な緊張)",
    "emerging_narrative": "Emerging Narrative (立ち現れる物語)",
}
LAYER_ORDER = [
    "litany",
    "systemic_causes",
    "worldview",
    "myth_metaphor",
    "key_tension",
    "emerging_narrative",
]


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "miratuku-news/cla-export"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def normalize_list(data) -> list:
    """Yearly/quarterly files may be either a list or {entries:[...]}"""
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("entries"), list):
        return data["entries"]
    return []


def wrap_paragraph(text: str, indent: str = "") -> str:
    """Return text as a single block prefixed with indent on each line.
    Does not hard-wrap CJK text; Japanese readers prefer unwrapped lines."""
    if text is None:
        return ""
    text = str(text).strip()
    if not text:
        return ""
    lines = text.splitlines()
    return "\n".join(f"{indent}{ln}" if ln else "" for ln in lines)


def format_category_block(cat_key: str, cat_data: dict) -> str:
    out = []
    label = CATEGORY_LABELS.get(cat_key, cat_key)
    out.append(f"【{label} ({cat_key})】")
    if not isinstance(cat_data, dict):
        out.append("  (データなし)")
        return "\n".join(out)
    for layer_key in LAYER_ORDER:
        layer_label = LAYER_LABELS[layer_key]
        val = cat_data.get(layer_key)
        if not val:
            continue
        out.append(f"  ◆ {layer_label}")
        out.append(wrap_paragraph(val, indent="    "))
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def format_entry(entry: dict) -> str:
    period = entry.get("period", "?")
    etype = entry.get("type", "")
    out = []
    divider = "-" * 60
    out.append(divider)
    if etype == "quarterly":
        out.append(f"■ {period}（四半期）")
    else:
        out.append(f"■ {period}年")
    out.append(divider)
    out.append("")

    categories = entry.get("categories") or {}
    for cat in CATEGORY_ORDER:
        if cat in categories:
            out.append(format_category_block(cat, categories[cat]))

    synthesis = entry.get("cross_category_synthesis")
    if synthesis:
        out.append("【分野横断の統合】")
        if isinstance(synthesis, dict):
            for k, v in synthesis.items():
                out.append(f"  ◆ {k}")
                out.append(wrap_paragraph(v, indent="    "))
                out.append("")
        else:
            out.append(wrap_paragraph(synthesis, indent="  "))
            out.append("")

    return "\n".join(out)


def format_meta_region(region_key: str, region_data: dict) -> str:
    out = []
    bar = "=" * 70
    title = region_data.get("title") or region_key
    out.append(bar)
    out.append(f"メタ分析: {region_key.upper()} — {title}")
    out.append(bar)
    out.append("")

    report_text = region_data.get("report_text")
    if report_text:
        out.append(report_text.strip())
        out.append("")

    shifts = region_data.get("key_paradigm_shifts") or []
    if shifts:
        out.append("-" * 60)
        out.append("主要パラダイムシフト")
        out.append("-" * 60)
        for i, shift in enumerate(shifts, start=1):
            period = shift.get("period", "")
            desc = shift.get("description") or shift.get("shift") or ""
            out.append(f"{i}. [{period}] {desc}")
        out.append("")

    myths = region_data.get("dominant_myths_timeline") or []
    if myths:
        out.append("-" * 60)
        out.append("支配的な神話・メタファーの変遷")
        out.append("-" * 60)
        for m in myths:
            period = m.get("period", "")
            myth = m.get("myth") or m.get("metaphor") or ""
            out.append(f"  [{period}] {myth}")
        out.append("")

    return "\n".join(out)


def main() -> int:
    print("Fetching CLA data from future-insight-app...", file=sys.stderr)
    yearly = normalize_list(fetch_json(FILES["yearly"]))
    quarterly = normalize_list(fetch_json(FILES["quarterly"]))
    meta = fetch_json(FILES["meta"])
    print(
        f"  yearly={len(yearly)}, quarterly={len(quarterly)}, "
        f"meta={'yes' if meta else 'no'}",
        file=sys.stderr,
    )

    # Sort chronologically just in case
    def sort_key(e):
        p = str(e.get("period", ""))
        return p

    yearly = sorted(yearly, key=sort_key)
    quarterly = sorted(quarterly, key=sort_key)

    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst).strftime("%Y-%m-%d %H:%M JST")
    coverage = (meta or {}).get("data_coverage", {})

    out_lines = []
    bar = "=" * 70
    out_lines.append(bar)
    out_lines.append("CLA (Causal Layered Analysis) 36年分析")
    out_lines.append("1990 - 2026")
    out_lines.append(bar)
    out_lines.append("")
    out_lines.append(f"生成日時: {now}")
    out_lines.append("データソース: miratuku-news / future-insight-app")
    out_lines.append(
        "カバレッジ: 年次 "
        f"{coverage.get('yearly_periods', len(yearly))}件 + 四半期 "
        f"{coverage.get('quarterly_periods', len(quarterly))}件 = "
        f"合計 {coverage.get('total_periods', len(yearly) + len(quarterly))}期間"
    )
    out_lines.append(f"年範囲: {coverage.get('year_range', '1990-2026')}")
    out_lines.append("")
    out_lines.append("【CLA（因果階層分析）とは】")
    out_lines.append(
        "  Sohail Inayatullah が提唱した未来学の分析手法。社会現象を4層"
    )
    out_lines.append(
        "  （Litany / Systemic Causes / Worldview / Myth & Metaphor）に"
    )
    out_lines.append(
        "  分解し、表層の出来事と深層の神話を対応付けることで、"
    )
    out_lines.append("  代替的未来の可能性を構造的に探索する。")
    out_lines.append("")
    out_lines.append("【読み方の手引き】")
    out_lines.append(
        "  各期間について、政治・経済・社会・技術・法律・環境（PESTLE）の"
    )
    out_lines.append(
        "  6分野ごとに、上記4層 + Key Tension + Emerging Narrative を記述。"
    )
    out_lines.append(
        "  冒頭のメタ分析は日本・グローバルそれぞれの36年総括。"
    )
    out_lines.append("")

    # Meta analysis first
    if isinstance(meta, dict):
        for region_key in ("japan", "global"):
            region = meta.get(region_key)
            if isinstance(region, dict):
                out_lines.append(format_meta_region(region_key, region))
                out_lines.append("")

    # Yearly entries
    out_lines.append("")
    out_lines.append("=" * 70)
    out_lines.append(f"第I部: 年次分析 ({len(yearly)}件)")
    out_lines.append("=" * 70)
    out_lines.append("")
    for e in yearly:
        out_lines.append(format_entry(e))
        out_lines.append("")

    # Quarterly entries
    out_lines.append("")
    out_lines.append("=" * 70)
    out_lines.append(f"第II部: 四半期分析 ({len(quarterly)}件)")
    out_lines.append("=" * 70)
    out_lines.append("")
    for e in quarterly:
        out_lines.append(format_entry(e))
        out_lines.append("")

    out_lines.append("")
    out_lines.append("=" * 70)
    out_lines.append("(終わり)")
    out_lines.append("=" * 70)

    text = "\n".join(out_lines)

    out_path = Path(__file__).resolve().parent.parent / "data" / "cla_36years_analysis.txt"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    size_kb = len(text.encode("utf-8")) / 1024
    print(f"Wrote {out_path} ({size_kb:.1f} KB)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
