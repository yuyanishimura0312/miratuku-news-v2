#!/usr/bin/env python3
"""
Validate MG (Management Studies) Database quality and integrity.
Checks: duplicates, field completeness, definition quality, distribution balance,
year/theorist plausibility, and relation graph coherence.
"""

import json
import sys
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


def load_db():
    with open(DATA_DIR / "mg_consolidated.json") as f:
        return json.load(f)


def check_duplicates(concepts):
    """Check for duplicate concepts by name_en"""
    issues = []
    seen = {}
    for c in concepts:
        key = (c.get("name_en") or "").strip().lower()
        if not key:
            issues.append(f"  EMPTY name_en: id={c.get('id')}, name_ja={c.get('name_ja')}")
            continue
        if key in seen:
            issues.append(f"  DUPLICATE: '{c.get('name_en')}' (ids: {seen[key]}, {c.get('id')})")
        else:
            seen[key] = c.get("id")
    return issues


def check_field_completeness(concepts):
    """Check required fields are present and non-empty"""
    required = ["name_ja", "name_en", "category", "definition_ja", "origin_year"]
    desirable = ["definition_en", "origin_theorist", "framework_ja", "subfield_id"]
    issues = []
    missing_counts = Counter()

    for c in concepts:
        for field in required:
            val = c.get(field)
            if val is None or (isinstance(val, str) and not val.strip()):
                missing_counts[field] += 1
                if missing_counts[field] <= 3:  # Only show first 3
                    issues.append(f"  MISSING required '{field}': id={c.get('id')}, name={c.get('name_en','?')}")

    for field in desirable:
        count = sum(1 for c in concepts if not c.get(field))
        if count > 0:
            issues.append(f"  INCOMPLETE '{field}': {count}/{len(concepts)} concepts missing")

    return issues


def check_definition_quality(concepts):
    """Check definition length and quality"""
    issues = []
    short_defs = []
    empty_defs = []

    for c in concepts:
        def_ja = c.get("definition_ja", "")
        if not def_ja:
            empty_defs.append(c.get("name_en", "?"))
        elif len(def_ja) < 30:
            short_defs.append((c.get("name_en", "?"), len(def_ja)))

    if empty_defs:
        issues.append(f"  EMPTY definition_ja: {len(empty_defs)} concepts")
        for name in empty_defs[:5]:
            issues.append(f"    - {name}")

    if short_defs:
        issues.append(f"  SHORT definition_ja (<30 chars): {len(short_defs)} concepts")
        for name, length in short_defs[:5]:
            issues.append(f"    - {name} ({length} chars)")

    # Distribution of definition lengths
    lengths = [len(c.get("definition_ja", "")) for c in concepts]
    if lengths:
        avg = sum(lengths) / len(lengths)
        issues.append(f"  Definition length stats: min={min(lengths)}, avg={avg:.0f}, max={max(lengths)}, median={sorted(lengths)[len(lengths)//2]}")

        # AN quality benchmark: 400-600 chars
        an_quality = sum(1 for l in lengths if l >= 200)
        issues.append(f"  AN-quality (>=200 chars): {an_quality}/{len(concepts)} ({an_quality/len(concepts)*100:.1f}%)")

    return issues


def check_distribution(concepts, taxonomy_path=None):
    """Check category and subfield distribution"""
    issues = []
    cat_counts = Counter(c.get("category", "unknown") for c in concepts)

    targets = {
        "strategy": 340, "entrepreneurship": 275, "leadership": 230,
        "organization": 475, "innovation": 290, "marketing": 280,
        "psychology": 345, "finance": 240, "operations": 265, "governance": 210
    }

    issues.append(f"  Category distribution ({len(concepts)} total):")
    for cat in sorted(targets.keys(), key=lambda x: cat_counts.get(x, 0) / targets[x]):
        actual = cat_counts.get(cat, 0)
        target = targets[cat]
        pct = actual / target * 100
        bar = "#" * int(pct / 5)
        issues.append(f"    {cat:<20} {actual:>4}/{target:<4} ({pct:>5.1f}%) {bar}")

    # Subfield distribution
    sf_counts = Counter(c.get("subfield_id", "") for c in concepts if c.get("subfield_id"))
    empty_sf = sum(1 for c in concepts if not c.get("subfield_id"))
    if empty_sf:
        issues.append(f"  Concepts without subfield_id: {empty_sf}")

    return issues


def check_year_plausibility(concepts):
    """Check origin_year values are plausible"""
    issues = []
    suspicious = []

    for c in concepts:
        year = c.get("origin_year")
        if year is None:
            continue
        if not isinstance(year, (int, float)):
            suspicious.append(f"  NON-NUMERIC year: {c.get('name_en')} = {year}")
        elif year < 1800 or year > 2026:
            suspicious.append(f"  SUSPICIOUS year: {c.get('name_en')} = {year}")

    no_year = sum(1 for c in concepts if c.get("origin_year") is None)
    if no_year:
        issues.append(f"  Missing origin_year: {no_year} concepts")
    if suspicious:
        issues.append(f"  Suspicious years: {len(suspicious)}")
        issues.extend(suspicious[:5])

    return issues


def check_relations(db):
    """Check relation graph quality"""
    issues = []
    edges = db.get("graph_edges", [])
    concepts = db.get("concepts", [])
    concept_ids = {c["id"] for c in concepts}

    # Check for dangling references
    dangling = 0
    for e in edges:
        src = e.get("source") if isinstance(e.get("source"), str) else e.get("source", {}).get("id")
        tgt = e.get("target") if isinstance(e.get("target"), str) else e.get("target", {}).get("id")
        if src not in concept_ids or tgt not in concept_ids:
            dangling += 1

    if dangling:
        issues.append(f"  Dangling references: {dangling}/{len(edges)} edges")

    # Relation type distribution
    rel_types = Counter(e.get("type", "unknown") for e in edges)
    issues.append(f"  Relation types: {dict(rel_types)}")

    # Connectivity
    connected = set()
    for e in edges:
        src = e.get("source") if isinstance(e.get("source"), str) else e.get("source", {}).get("id")
        tgt = e.get("target") if isinstance(e.get("target"), str) else e.get("target", {}).get("id")
        if src:
            connected.add(src)
        if tgt:
            connected.add(tgt)

    isolated = len(concept_ids) - len(connected)
    issues.append(f"  Connected concepts: {len(connected)}/{len(concepts)} ({len(connected)/len(concepts)*100:.1f}%)")
    issues.append(f"  Isolated concepts (no relations): {isolated}")

    # Avg degree
    degree = Counter()
    for e in edges:
        src = e.get("source") if isinstance(e.get("source"), str) else e.get("source", {}).get("id")
        tgt = e.get("target") if isinstance(e.get("target"), str) else e.get("target", {}).get("id")
        if src:
            degree[src] += 1
        if tgt:
            degree[tgt] += 1

    if degree:
        avg_deg = sum(degree.values()) / len(degree)
        max_concept = max(degree, key=degree.get)
        max_name = next((c.get("name_en") for c in concepts if c.get("id") == max_concept), "?")
        issues.append(f"  Avg degree: {avg_deg:.1f}, max: {max_name} ({degree[max_concept]})")

    return issues


def check_researchers(db):
    """Check researcher data quality"""
    issues = []
    researchers = db.get("researchers", [])

    # Duplicate check
    names = Counter(r.get("name_en", "").lower() for r in researchers)
    dups = {name: count for name, count in names.items() if count > 1 and name}
    if dups:
        issues.append(f"  Duplicate researchers: {dups}")

    # Field completeness
    missing_bio = sum(1 for r in researchers if not r.get("bio_ja"))
    missing_year = sum(1 for r in researchers if not r.get("birth_year"))
    issues.append(f"  Total: {len(researchers)}")
    issues.append(f"  Missing bio_ja: {missing_bio}")
    issues.append(f"  Missing birth_year: {missing_year}")

    return issues


def main():
    print("=" * 70)
    print("MG Database Validation Report")
    print("=" * 70)

    db = load_db()
    concepts = db["concepts"]

    print(f"\n## Overview")
    print(f"  Concepts: {len(concepts)}")
    print(f"  Researchers: {len(db.get('researchers', []))}")
    print(f"  Relations: {len(db.get('graph_edges', []))}")
    print(f"  Clusters: {len(db.get('clusters', []))}")

    sections = [
        ("Duplicate Check", check_duplicates(concepts)),
        ("Field Completeness", check_field_completeness(concepts)),
        ("Definition Quality", check_definition_quality(concepts)),
        ("Distribution Balance", check_distribution(concepts)),
        ("Year Plausibility", check_year_plausibility(concepts)),
        ("Relation Graph", check_relations(db)),
        ("Researchers", check_researchers(db)),
    ]

    total_issues = 0
    for title, issues in sections:
        print(f"\n## {title}")
        for issue in issues:
            print(issue)
            if issue.strip().startswith("DUPLICATE") or issue.strip().startswith("MISSING") or issue.strip().startswith("EMPTY"):
                total_issues += 1

    print(f"\n{'=' * 70}")
    print(f"Total issues requiring attention: {total_issues}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
