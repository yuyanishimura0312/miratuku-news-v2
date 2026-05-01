#!/usr/bin/env python3
"""
Build Management Studies Database (MG) from GF concepts + additional data.
Extracts 671 concepts from gf_consolidated.json, merges with additional concepts,
adds relationships, researchers, and clusters.
"""

import json
import os
import sys
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = DATA_DIR

# Category → cluster mapping
CATEGORY_CLUSTER_MAP = {
    "strategy": 1,
    "entrepreneurship": 2,
    "leadership": 3,
    "innovation": 4,
    "marketing": 5,
    "organization": 6,
    "governance": 7,
    "finance": 8,
    "operations": 9,
    "psychology": 10,
}

CLUSTER_COLORS = {
    0: "#888888",
    1: "#CC1400",
    2: "#1A6B3C",
    3: "#8B5CF6",
    4: "#D97706",
    5: "#0369A1",
    6: "#BE185D",
    7: "#525252",
    8: "#2563EB",
    9: "#059669",
    10: "#9333EA",
}


def load_gf_concepts():
    """Load concepts from gf_consolidated.json"""
    gf_path = DATA_DIR / "gf_consolidated.json"
    with open(gf_path, "r") as f:
        data = json.load(f)
    return data["concepts"]


def normalize_concept(concept, idx):
    """Normalize a concept to standard MG schema"""
    return {
        "id": f"m{idx:04d}",
        "name_ja": concept.get("name_ja", ""),
        "name_en": concept.get("name_en", ""),
        "framework_ja": concept.get("framework_ja", ""),
        "framework_en": concept.get("framework_en", ""),
        "category": concept.get("category", "unknown"),
        "cluster": CATEGORY_CLUSTER_MAP.get(concept.get("category", ""), 0),
        "definition_ja": concept.get("definition_ja", ""),
        "definition_en": concept.get("definition_en", ""),
        "origin_year": concept.get("origin_year"),
        "origin_theorist": concept.get("origin_theorist", ""),
    }


def deduplicate_concepts(concepts):
    """Remove duplicate concepts by name_en (case-insensitive)"""
    seen = {}
    unique = []
    for c in concepts:
        key = c.get("name_en", "").strip().lower()
        if key and key not in seen:
            seen[key] = True
            unique.append(c)
        elif not key:
            unique.append(c)
    return unique


def merge_additional_concepts(base_concepts, additional_files):
    """Merge additional concept files, deduplicating"""
    # First, deduplicate the base set itself
    seen_base = {}
    deduped_base = []
    for c in base_concepts:
        key = c.get("name_en", "").strip().lower()
        if key and key not in seen_base:
            seen_base[key] = True
            deduped_base.append(c)
        elif not key:
            deduped_base.append(c)
    if len(deduped_base) < len(base_concepts):
        print(f"  Removed {len(base_concepts) - len(deduped_base)} duplicates within base set")
    all_concepts = deduped_base
    existing_names = {c.get("name_en", "").strip().lower() for c in deduped_base}

    for filepath in additional_files:
        if not os.path.exists(filepath):
            print(f"  Skipping missing file: {filepath}")
            continue
        with open(filepath, "r") as f:
            additional = json.load(f)
        added = 0
        for c in additional:
            key = c.get("name_en", "").strip().lower()
            if key and key not in existing_names:
                existing_names.add(key)
                all_concepts.append(c)
                added += 1
        print(f"  Added {added} concepts from {filepath}")

    return all_concepts


def build_graph_data(concepts):
    """Build D3.js graph nodes from concepts"""
    nodes = []
    for c in concepts:
        nodes.append({
            "id": c["id"],
            "name_ja": c["name_ja"],
            "name_en": c["name_en"],
            "subfield": c.get("framework_ja", c.get("category", "")),
            "era_start": c.get("origin_year"),
        })
    return nodes


def build_cluster_map(concepts):
    """Build cluster map {concept_id: cluster_number}"""
    return {c["id"]: c["cluster"] for c in concepts}


def main():
    print("=== Building Management Studies Database (MG) ===\n")

    # Step 1: Load GF concepts
    print("Step 1: Loading GF concepts...")
    gf_concepts = load_gf_concepts()
    print(f"  Loaded {len(gf_concepts)} concepts from GF")

    # Step 2: Normalize
    print("\nStep 2: Normalizing concepts...")
    normalized = [normalize_concept(c, i + 1) for i, c in enumerate(gf_concepts)]

    # Step 3: Merge additional concepts
    print("\nStep 3: Merging additional concepts...")
    additional_files = [
        DATA_DIR / "mg_additional_strategy.json",
        DATA_DIR / "mg_additional_org.json",
        DATA_DIR / "mg_additional_misc.json",
        DATA_DIR / "mg_additional_innov_ops.json",
        DATA_DIR / "mg_batch2_marketing.json",
        DATA_DIR / "mg_batch2_finance.json",
        DATA_DIR / "mg_batch2_governance.json",
        DATA_DIR / "mg_batch2_org.json",
        DATA_DIR / "mg_batch2_leadership.json",
        DATA_DIR / "mg_batch2_entrepreneurship.json",
        DATA_DIR / "mg_batch3_expansion1.json",
        DATA_DIR / "mg_batch3_expansion2.json",
    ]
    all_concepts = merge_additional_concepts(normalized, additional_files)

    # Step 3.5: Apply enriched definitions (update only if new is longer)
    enriched_defs_path = DATA_DIR / "mg_enriched_defs_batch1.json"
    if enriched_defs_path.exists():
        with open(enriched_defs_path, "r") as f:
            enriched_defs = json.load(f)
        name_to_def = {d["name_en"].strip().lower(): d["definition_ja"] for d in enriched_defs if d.get("name_en") and d.get("definition_ja")}
        def_updated = 0
        for c in all_concepts:
            key = c.get("name_en", "").strip().lower()
            if key in name_to_def:
                new_def = name_to_def[key]
                if len(new_def) > len(c.get("definition_ja", "")):
                    c["definition_ja"] = new_def
                    def_updated += 1
        print(f"\nStep 3.5: Applied {def_updated} enriched definitions from {enriched_defs_path.name}")
    else:
        print(f"\nStep 3.5: Skipped (enriched defs file not found)")

    # Step 4: Re-index after merge
    print(f"\nStep 4: Re-indexing {len(all_concepts)} concepts...")
    for i, c in enumerate(all_concepts):
        c["id"] = f"m{i + 1:04d}"
        if "cluster" not in c:
            c["cluster"] = CATEGORY_CLUSTER_MAP.get(c.get("category", ""), 0)

    # Step 5: Load enrichment data (clusters, researchers, relations)
    print("\nStep 5: Loading enrichment data...")
    enrichment_path = DATA_DIR / "mg_enrichment.json"
    clusters = []
    researchers = []
    relations = []
    if enrichment_path.exists():
        with open(enrichment_path, "r") as f:
            enrichment = json.load(f)
        clusters = enrichment.get("clusters", [])
        researchers = enrichment.get("researchers", [])
        relations = enrichment.get("key_relations", [])
        print(f"  Clusters: {len(clusters)}, Researchers: {len(researchers)}, Relations: {len(relations)}")
    else:
        print("  WARNING: mg_enrichment.json not found, using defaults")

    # Step 6: Match relations to concept IDs (with fuzzy matching)
    print("\nStep 6: Matching relations to concept IDs...")
    name_to_id = {}
    for c in all_concepts:
        key = c["name_en"].strip().lower()
        name_to_id[key] = c["id"]
        # Also index without common suffixes/prefixes for fuzzy matching
        for suffix in [" analysis", " framework", " theory", " model", " strategy"]:
            if key.endswith(suffix):
                name_to_id[key[: -len(suffix)]] = c["id"]
        # Index parenthetical variants
        if "(" in key:
            name_to_id[key.split("(")[0].strip()] = c["id"]
        # Index with common variant mappings
        name_to_id[key.replace("-", " ")] = c["id"]

    # Add manual aliases for common naming mismatches
    aliases = {
        "five forces": "five forces analysis",
        "bcg matrix": "bcg growth-share matrix",
        "scientific management": "scientific management",
        "resource-based view": "resource-based view",
        "bounded rationality": "bounded rationality",
        "4p (marketing mix)": "4p（マーケティングミックス）",
        "csr": "corporate social responsibility",
        "capm": "capital asset pricing model",
        "dcf (discounted cash flow)": "dcf法",
        "seci model": "seci model",
        "roi (return on investment)": "roi（投資利益率）",
        "balanced scorecard": "balanced scorecard",
        "emotional intelligence": "emotional intelligence",
        "innovation diffusion": "innovation diffusion theory",
        "marketing myopia": "marketing myopia",
        "maslow's hierarchy of needs": "maslow's hierarchy of needs",
        "sensemaking": "sensemaking",
        "shared value": "shared value",
        "theory x / theory y": "theory x and theory y",
        "creative destruction": "creative destruction",
        "agile / scrum": "agile / scrum",
    }
    # Try to find aliases in existing names
    for alias_key, alias_target in aliases.items():
        if alias_key not in name_to_id:
            # Try partial matching
            for existing_key, existing_id in list(name_to_id.items()):
                if alias_key in existing_key or existing_key in alias_key:
                    name_to_id[alias_key] = existing_id
                    break

    def fuzzy_find(name):
        key = name.strip().lower()
        if key in name_to_id:
            return name_to_id[key]
        # Try substring match
        for existing_key, existing_id in name_to_id.items():
            if key in existing_key or existing_key in key:
                return existing_id
        return None

    graph_edges = []
    matched = 0
    for rel in relations:
        from_id = fuzzy_find(rel.get("from_name_en", ""))
        to_id = fuzzy_find(rel.get("to_name_en", ""))
        if from_id and to_id and from_id != to_id:
            graph_edges.append({
                "source": from_id,
                "target": to_id,
                "type": rel.get("relation", "related"),
            })
            matched += 1
    print(f"  Matched {matched}/{len(relations)} relations")

    # Step 7: Build output
    print("\nStep 7: Building output...")
    graph_nodes = build_graph_data(all_concepts)
    cluster_map = build_cluster_map(all_concepts)

    output = {
        "concepts": all_concepts,
        "clusters": clusters,
        "researchers": researchers,
        "graph_nodes": graph_nodes,
        "graph_edges": graph_edges,
        "cluster_map": cluster_map,
        "cluster_colors": CLUSTER_COLORS,
        "stats": {
            "total_concepts": len(all_concepts),
            "total_researchers": len(researchers),
            "total_relations": len(graph_edges),
            "total_clusters": len(clusters),
            "by_category": dict(Counter(c.get("category", "unknown") for c in all_concepts)),
        },
    }

    output_path = OUTPUT_DIR / "mg_consolidated.json"
    with open(output_path, "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n  Output: {output_path}")
    print(f"  Size: {output_path.stat().st_size / 1024:.1f} KB")

    # Summary
    print(f"\n=== Summary ===")
    print(f"  Total concepts: {output['stats']['total_concepts']}")
    print(f"  Total researchers: {output['stats']['total_researchers']}")
    print(f"  Total relations: {output['stats']['total_relations']}")
    print(f"  Categories:")
    for cat, count in sorted(output["stats"]["by_category"].items(), key=lambda x: -x[1]):
        print(f"    {cat}: {count}")


if __name__ == "__main__":
    main()
