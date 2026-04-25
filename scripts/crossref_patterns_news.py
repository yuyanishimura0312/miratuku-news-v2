#!/usr/bin/env python3
"""
Cross-reference 19 novel system patterns with modern news (1990-2026).
Queries PESTLE DB, Cultural Intelligence DB, and Signal DB.
"""
import json
import sqlite3
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent
PESTLE_DB = Path.home() / "projects/research/pestle-signal-db/data/pestle.db"
SIGNAL_DB = Path.home() / "projects/research/pestle-signal-db/data/signal.db"
CI_DB = Path.home() / "projects/research/cultural-intelligence-db/data/cultural_intelligence.db"
OUTPUT_JSON = PROJECT_ROOT / "data" / "gf_crossref_analysis.json"
PATTERNS_JSON = PROJECT_ROOT / "data" / "gf_novel_patterns.json"

# ============================================================
# Structural dimension keywords (from discover_novel_patterns.py)
# Using 2-3 most distinctive keywords per dimension for SQL efficiency
# ============================================================
DIMENSIONS = {
    "reinforcing": {
        "name_ja": "自己強化",
        "keywords": ["reinforcing", "feedback loop", "self-reinforcing", "flywheel", "compounding",
                     "virtuous cycle", "exponential growth", "network effect", "positive feedback"],
        "keywords_en": ["reinforcing loop", "feedback", "compounding", "network effect", "flywheel",
                        "exponential", "self-reinforcing", "virtuous cycle", "amplification"],
    },
    "balancing": {
        "name_ja": "均衡・抑制",
        "keywords": ["resistance", "constraint", "limit", "decline", "collapse", "balancing",
                     "countervailing", "diminishing returns", "saturation", "ceiling"],
        "keywords_en": ["resistance", "constraint", "limit", "decline", "collapse", "balancing",
                        "countervailing", "diminishing returns", "saturation", "pushback"],
    },
    "paradox": {
        "name_ja": "逆説・矛盾",
        "keywords": ["paradox", "contradiction", "dilemma", "irony", "counterintuitive",
                     "unintended consequence", "double-edged", "trade-off", "tension"],
        "keywords_en": ["paradox", "contradiction", "dilemma", "irony", "counterintuitive",
                        "unintended consequence", "backfire", "perverse effect", "trade-off"],
    },
    "transformation": {
        "name_ja": "構造転換",
        "keywords": ["transformation", "disruption", "restructuring", "pivot", "transition",
                     "paradigm shift", "revolution", "creative destruction", "reinvention"],
        "keywords_en": ["transformation", "disruption", "restructuring", "pivot", "transition",
                        "paradigm shift", "revolution", "reinvention", "overhaul"],
    },
    "emergence": {
        "name_ja": "創発・自己組織化",
        "keywords": ["emergence", "self-organization", "decentralization", "autonomous", "adaptation",
                     "evolution", "bottom-up", "spontaneous order", "complexity"],
        "keywords_en": ["emergence", "self-organizing", "decentralized", "autonomous", "adaptive",
                        "evolutionary", "bottom-up", "spontaneous", "complex system"],
    },
    "path_dependence": {
        "name_ja": "経路依存性",
        "keywords": ["path dependence", "lock-in", "irreversible", "inertia", "legacy",
                     "first-mover", "sunk cost", "historical", "inherited"],
        "keywords_en": ["path dependence", "lock-in", "irreversible", "inertia", "legacy system",
                        "sunk cost", "incumbent advantage", "historical constraint"],
    },
    "delay": {
        "name_ja": "時間遅延",
        "keywords": ["delay", "lag", "slow", "long-term", "decade", "gradual", "latent",
                     "deferred", "time lag", "latency"],
        "keywords_en": ["time lag", "delayed effect", "slow-moving", "long-term consequence",
                        "gradual", "latent", "deferred", "lagging indicator"],
    },
    "nonlinear": {
        "name_ja": "非線形・臨界点",
        "keywords": ["tipping point", "threshold", "exponential", "sudden", "cascade",
                     "nonlinear", "phase transition", "critical mass", "inflection point"],
        "keywords_en": ["tipping point", "threshold", "cascade", "nonlinear", "phase transition",
                        "critical mass", "inflection point", "sudden shift", "explosive growth"],
    },
    "scale": {
        "name_ja": "スケール効果",
        "keywords": ["scale", "massive", "global", "systemic", "widespread", "large-scale",
                     "ecosystem", "platform", "economies of scale", "network scale"],
        "keywords_en": ["scale", "massive", "global", "systemic", "widespread", "large-scale",
                        "platform", "economies of scale", "network scale"],
    },
    "info_asymmetry": {
        "name_ja": "情報の非対称性",
        "keywords": ["information asymmetry", "uncertainty", "opacity", "surveillance",
                     "intelligence", "disinformation", "hidden", "transparency", "data control"],
        "keywords_en": ["information asymmetry", "opacity", "surveillance", "disinformation",
                        "hidden information", "data monopoly", "transparency", "intelligence gap"],
    },
    "legitimacy": {
        "name_ja": "正当性の構築",
        "keywords": ["legitimacy", "authority", "trust", "credibility", "mandate", "consensus",
                     "sovereignty", "moral authority", "public trust", "institutional trust"],
        "keywords_en": ["legitimacy", "authority", "credibility", "mandate", "public trust",
                        "institutional trust", "democratic", "consent", "moral authority"],
    },
    "resource_conversion": {
        "name_ja": "資源変換",
        "keywords": ["resource conversion", "repurpose", "reallocation", "capital conversion",
                     "human capital", "knowledge transfer", "technology transfer", "asset reuse"],
        "keywords_en": ["repurpose", "reallocation", "capital conversion", "human capital",
                        "knowledge transfer", "technology transfer", "pivot resources", "asset conversion"],
    },
}

# Concise English search keywords for SQL LIKE queries (2-3 per dimension)
DIM_SQL_KEYWORDS = {
    "reinforcing":        ["feedback loop", "network effect", "compounding"],
    "balancing":          ["resistance", "constraint", "diminishing returns"],
    "paradox":            ["paradox", "unintended consequence", "counterintuitive"],
    "transformation":     ["disruption", "paradigm shift", "transformation"],
    "emergence":          ["emergence", "self-organiz", "decentraliz"],
    "path_dependence":    ["lock-in", "path dependence", "inertia"],
    "delay":              ["time lag", "delayed effect", "slow-moving"],
    "nonlinear":          ["tipping point", "cascade", "critical mass"],
    "scale":              ["large-scale", "systemic", "economies of scale"],
    "info_asymmetry":     ["information asymmetry", "disinformation", "opacity"],
    "legitimacy":         ["legitimacy", "public trust", "institutional trust"],
    "resource_conversion":["repurpose", "knowledge transfer", "reallocation"],
}


def build_like_clauses(dims: list[str], fields: list[str]) -> tuple[str, list]:
    """Build WHERE clause for LIKE matching across dimensions and fields."""
    clauses = []
    params = []
    for dim in dims:
        keywords = DIM_SQL_KEYWORDS.get(dim, [])
        for kw in keywords:
            field_clauses = []
            for field in fields:
                field_clauses.append(f"LOWER({field}) LIKE ?")
                params.append(f"%{kw.lower()}%")
            clauses.append(f"({' OR '.join(field_clauses)})")
    if not clauses:
        return "1=0", []
    return f"({' OR '.join(clauses)})", params


def decade_from_date(date_str: str) -> str | None:
    """Extract decade from date string."""
    if not date_str:
        return None
    try:
        year = int(str(date_str)[:4])
        if year < 1990 or year > 2026:
            return None
        if year < 2000:
            return "1990s"
        elif year < 2010:
            return "2000s"
        elif year < 2020:
            return "2010s"
        else:
            return "2020s"
    except (ValueError, TypeError):
        return None


def determine_trend(decade_counts: dict) -> str:
    """Determine trend from decade counts."""
    decades = ["1990s", "2000s", "2010s", "2020s"]
    counts = [decade_counts.get(d, 0) for d in decades]
    non_zero = [(d, c) for d, c in zip(decades, counts) if c > 0]

    if not non_zero:
        return "absent"
    if len(non_zero) == 1:
        decade, _ = non_zero[0]
        return "emerging" if decade in ("2010s", "2020s") else "historical"

    # Check if last two decades have highest counts
    recent_total = sum(decade_counts.get(d, 0) for d in ["2010s", "2020s"])
    early_total = sum(decade_counts.get(d, 0) for d in ["1990s", "2000s"])

    if counts[-1] > counts[-2] > 0:
        return "increasing"
    elif counts[-1] < counts[-2] and early_total > recent_total:
        return "decreasing"
    elif recent_total > early_total * 2:
        return "emerging"
    elif abs(recent_total - early_total) < max(recent_total, early_total) * 0.3:
        return "stable"
    else:
        return "fluctuating"


def query_pestle(combo: list[str], conn: sqlite3.Connection) -> tuple[dict, list]:
    """Query PESTLE DB for a pattern combo. Returns decade_counts and samples."""
    where_clause, params = build_like_clauses(combo, ["title", "summary"])
    date_filter = "AND published_date >= '1990-01-01' AND published_date <= '2026-12-31'"

    # Count per decade
    decade_counts = defaultdict(int)
    samples = []

    for decade, start, end in [
        ("1990s", "1990-01-01", "1999-12-31"),
        ("2000s", "2000-01-01", "2009-12-31"),
        ("2010s", "2010-01-01", "2019-12-31"),
        ("2020s", "2020-01-01", "2026-12-31"),
    ]:
        sql = f"""
            SELECT COUNT(*) FROM articles
            WHERE {where_clause}
            AND published_date >= ? AND published_date <= ?
            AND published_date >= '1990-01-01'
        """
        cur = conn.execute(sql, params + [start, end])
        count = cur.fetchone()[0]
        decade_counts[decade] = count

        # Get samples (up to 2 per decade)
        if count > 0:
            sample_sql = f"""
                SELECT title, published_date, source, pestle_category FROM articles
                WHERE {where_clause}
                AND published_date >= ? AND published_date <= ?
                AND published_date >= '1990-01-01'
                AND title IS NOT NULL AND title != ''
                ORDER BY relevance_score DESC
                LIMIT 2
            """
            cur2 = conn.execute(sample_sql, params + [start, end])
            for row in cur2.fetchall():
                samples.append({
                    "title": row[0],
                    "date": row[1],
                    "category": row[3],
                    "source": "pestle",
                })

    return dict(decade_counts), samples[:5]


def query_ci(combo: list[str], conn: sqlite3.Connection) -> tuple[dict, list]:
    """Query Cultural Intelligence DB for a pattern combo."""
    where_clause, params = build_like_clauses(combo, ["title"])
    decade_counts = defaultdict(int)
    samples = []

    for decade, start, end in [
        ("1990s", "1990-01-01", "1999-12-31"),
        ("2000s", "2000-01-01", "2009-12-31"),
        ("2010s", "2010-01-01", "2019-12-31"),
        ("2020s", "2020-01-01", "2026-12-31"),
    ]:
        sql = f"""
            SELECT COUNT(*) FROM articles
            WHERE {where_clause}
            AND published_at >= ? AND published_at <= ?
            AND published_at >= '1990-01-01'
        """
        cur = conn.execute(sql, params + [start, end])
        count = cur.fetchone()[0]
        decade_counts[decade] = count

        if count > 0:
            sample_sql = f"""
                SELECT title, published_at FROM articles
                WHERE {where_clause}
                AND published_at >= ? AND published_at <= ?
                AND published_at >= '1990-01-01'
                AND title IS NOT NULL AND title != ''
                LIMIT 2
            """
            cur2 = conn.execute(sample_sql, params + [start, end])
            for row in cur2.fetchall():
                samples.append({
                    "title": row[0],
                    "date": row[1][:10] if row[1] else "",
                    "source": "cultural_intelligence",
                })

    return dict(decade_counts), samples[:3]


def query_signals(combo: list[str], conn: sqlite3.Connection) -> list:
    """Query Signal DB for signals matching pattern dimensions."""
    where_clause, params = build_like_clauses(combo, ["signal_name", "description", "potential_impact"])

    sql = f"""
        SELECT signal_name, signal_type, potential_impact, time_horizon, composite_score
        FROM signals
        WHERE {where_clause}
        ORDER BY composite_score DESC
        LIMIT 5
    """
    cur = conn.execute(sql, params)
    results = []
    for row in cur.fetchall():
        results.append({
            "name": row[0],
            "type": row[1],
            "impact": row[2][:150] if row[2] else "",
            "time_horizon": row[3],
            "score": round(row[4], 3) if row[4] else None,
        })
    return results


def analyze_temporal_summary(patterns_results: list) -> str:
    """Generate a temporal summary narrative across all patterns."""
    decade_totals = defaultdict(int)
    trend_counts = defaultdict(int)

    for p in patterns_results:
        for decade, count in p["decade_counts"].items():
            decade_totals[decade] += count
        trend_counts[p["trend"]] += 1

    summary_parts = []
    summary_parts.append(
        f"Analysis of {len(patterns_results)} novel system patterns across 1990-2026 reveals the following temporal distribution: "
        f"1990s ({decade_totals['1990s']:,} article matches), "
        f"2000s ({decade_totals['2000s']:,}), "
        f"2010s ({decade_totals['2010s']:,}), "
        f"2020s ({decade_totals['2020s']:,})."
    )

    dominant_trend = max(trend_counts, key=trend_counts.get)
    summary_parts.append(
        f"The dominant temporal trend across patterns is '{dominant_trend}' "
        f"(seen in {trend_counts[dominant_trend]} of {len(patterns_results)} patterns). "
        f"Trend distribution: {dict(trend_counts)}."
    )

    # Identify fastest-growing pattern
    max_ratio = 0
    max_pattern = None
    for p in patterns_results:
        early = (p["decade_counts"].get("1990s", 0) + p["decade_counts"].get("2000s", 0)) or 1
        recent = p["decade_counts"].get("2010s", 0) + p["decade_counts"].get("2020s", 0)
        ratio = recent / early
        if ratio > max_ratio:
            max_ratio = ratio
            max_pattern = p["name"]

    if max_pattern:
        summary_parts.append(
            f"The fastest-growing pattern (2010s+2020s vs 1990s+2000s ratio: {max_ratio:.1f}x) is: '{max_pattern}'."
        )

    return " ".join(summary_parts)


def main():
    print("Loading novel patterns...")
    with open(PATTERNS_JSON) as f:
        patterns_data = json.load(f)

    # Filter to novel patterns only, take top 10 by size
    novel_patterns = [p for p in patterns_data["patterns"] if p.get("is_novel", False)]
    top10 = sorted(novel_patterns, key=lambda x: x["size"], reverse=True)[:10]
    print(f"Found {len(novel_patterns)} novel patterns, analyzing top {len(top10)}.")

    print("Connecting to databases...")
    pestle_conn = sqlite3.connect(str(PESTLE_DB))
    ci_conn = sqlite3.connect(str(CI_DB))
    signal_conn = sqlite3.connect(str(SIGNAL_DB))

    # Enable faster reads
    for conn in [pestle_conn, ci_conn, signal_conn]:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA cache_size=10000")

    results = []

    for i, pattern in enumerate(top10):
        name = pattern["name"]
        combo = pattern["combo"]
        print(f"\n[{i+1}/{len(top10)}] Analyzing: {name} ({combo})")

        # Query PESTLE
        print(f"  PESTLE query...")
        p_decades, p_samples = query_pestle(combo, pestle_conn)
        print(f"  PESTLE counts: {p_decades}")

        # Query CI
        print(f"  Cultural Intelligence query...")
        c_decades, c_samples = query_ci(combo, ci_conn)
        print(f"  CI counts: {c_decades}")

        # Combine decade counts
        all_decades = {}
        for decade in ["1990s", "2000s", "2010s", "2020s"]:
            all_decades[decade] = p_decades.get(decade, 0) + c_decades.get(decade, 0)

        # Determine trend
        trend = determine_trend(all_decades)

        # Query signals
        print(f"  Signal query...")
        signals = query_signals(combo, signal_conn)
        print(f"  Found {len(signals)} signals")

        # Combine samples (PESTLE + CI, max 5 total)
        all_samples = (p_samples + c_samples)[:5]

        results.append({
            "name": name,
            "combo": combo,
            "size": pattern["size"],
            "pestle_decade_counts": p_decades,
            "ci_decade_counts": c_decades,
            "decade_counts": all_decades,
            "trend": trend,
            "sample_articles": all_samples,
            "signals": signals,
        })

    # Generate temporal summary
    temporal_summary = analyze_temporal_summary(results)

    output = {
        "patterns": results,
        "temporal_summary": temporal_summary,
        "metadata": {
            "total_patterns_analyzed": len(results),
            "databases": ["pestle", "cultural_intelligence", "signal"],
            "date_range": "1990-2026",
            "generated_at": __import__("datetime").datetime.now().isoformat(),
        },
    }

    pestle_conn.close()
    ci_conn.close()
    signal_conn.close()

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSaved results to {OUTPUT_JSON}")
    print("\n=== SUMMARY ===")
    print(temporal_summary)
    print("\nPattern results:")
    for r in results:
        print(f"  {r['name']}")
        print(f"    Trend: {r['trend']} | Decades: {r['decade_counts']}")
        print(f"    Signals: {len(r['signals'])}")


if __name__ == "__main__":
    main()
