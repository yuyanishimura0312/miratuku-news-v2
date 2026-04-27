#!/usr/bin/env python3
"""
Build SI event relationships using multiple strategies.

Strategies:
1. Person-based: same person → direct causal chain
2. Thematic: same SI type + same civilization + temporal proximity
3. Structural: LLM-based analysis of structural_analysis text similarity
4. Geographic-temporal: same location + temporal proximity
5. Concept-mediated: original link-based approach (retained)

Usage:
    python3 scripts/build_sif_relationships.py [--llm] [--resume]
"""

import json
import os
import subprocess
import sys
import time
import argparse
from pathlib import Path
from collections import defaultdict, Counter
from itertools import combinations

DATA_DIR = Path(__file__).parent.parent / "data"


def load_si_events():
    """Load enriched SI events."""
    path = DATA_DIR / "sif_enriched_events.json"
    with open(path) as f:
        data = json.load(f)
    return data["events"]


def load_links():
    """Load concept links from consolidated data."""
    path = DATA_DIR / "gf_consolidated.json"
    with open(path) as f:
        data = json.load(f)
    return data.get("links", [])


# =============================================================================
# Strategy 1: Person-based relationships
# =============================================================================

def build_person_relationships(events):
    """Events by the same person are directly related."""
    person_events = defaultdict(list)
    for e in events:
        person = e.get("person_name_en", "")
        if person:
            # Normalize: handle Atatürk/Ataturk variants
            norm = person.strip()
            person_events[norm].append(e)

    # Merge obvious duplicates (Atatürk variants etc.)
    merged = defaultdict(list)
    seen = {}
    for person, evs in person_events.items():
        key = person.lower().replace("ü", "u").replace("é", "e").replace("ā", "a")
        if key in seen:
            merged[seen[key]].extend(evs)
        else:
            seen[key] = person
            merged[person] = evs

    relationships = []
    for person, evs in merged.items():
        if len(evs) < 2:
            continue
        # Sort by year
        evs_sorted = sorted(evs, key=lambda e: e.get("event_year") or 0)
        # Chain: each event influences the next (temporal order)
        for i in range(len(evs_sorted) - 1):
            for j in range(i + 1, min(i + 4, len(evs_sorted))):  # Connect up to 3 ahead
                e1, e2 = evs_sorted[i], evs_sorted[j]
                y1 = e1.get("event_year") or 0
                y2 = e2.get("event_year") or 0
                gap = abs(y2 - y1)

                if gap == 0:
                    rel_type = "parallel"
                    strength = "strong"
                elif gap <= 10:
                    rel_type = "directly_led_to"
                    strength = "strong"
                elif gap <= 30:
                    rel_type = "evolved_into"
                    strength = "moderate"
                else:
                    rel_type = "legacy_influence"
                    strength = "weak"

                relationships.append({
                    "source": e1.get("title_en", ""),
                    "target": e2.get("title_en", ""),
                    "type": rel_type,
                    "strength": strength,
                    "mechanism": "same_person",
                    "person": person,
                    "year_gap": gap,
                })

    return relationships


# =============================================================================
# Strategy 2: Thematic clustering
# =============================================================================

def build_thematic_relationships(events):
    """Events in same SI type + civilization + era are thematically related."""
    clusters = defaultdict(list)
    for e in events:
        si_type = e.get("si_type", "complex")
        civ = e.get("civilization", "unclassified")
        era = e.get("era", "")
        key = (si_type, civ, era)
        clusters[key].append(e)

    relationships = []
    for key, evs in clusters.items():
        if len(evs) < 2 or len(evs) > 50:  # Skip very large clusters
            continue
        evs_sorted = sorted(evs, key=lambda e: e.get("event_year") or 0)

        # Connect temporally adjacent events within cluster
        for i in range(len(evs_sorted) - 1):
            e1, e2 = evs_sorted[i], evs_sorted[i + 1]
            y1 = e1.get("event_year") or 0
            y2 = e2.get("event_year") or 0
            gap = abs(y2 - y1)

            if gap > 100:  # Too far apart
                continue

            if gap <= 10:
                rel_type = "co-occurrence"
                strength = "strong"
            elif gap <= 30:
                rel_type = "thematic_succession"
                strength = "moderate"
            else:
                rel_type = "thematic_echo"
                strength = "weak"

            relationships.append({
                "source": e1.get("title_en", ""),
                "target": e2.get("title_en", ""),
                "type": rel_type,
                "strength": strength,
                "mechanism": "thematic_cluster",
                "cluster": f"{key[0]}_{key[1]}_{key[2]}",
                "year_gap": gap,
            })

    return relationships


# =============================================================================
# Strategy 3: Geographic-temporal proximity
# =============================================================================

def build_geographic_relationships(events):
    """Events in same location within temporal proximity."""
    loc_events = defaultdict(list)
    for e in events:
        loc = (e.get("location_en") or "").strip()
        if loc and len(loc) > 2:  # Skip empty/short
            loc_events[loc].append(e)

    relationships = []
    for loc, evs in loc_events.items():
        if len(evs) < 2:
            continue
        evs_sorted = sorted(evs, key=lambda e: e.get("event_year") or 0)

        for i in range(len(evs_sorted)):
            for j in range(i + 1, min(i + 5, len(evs_sorted))):
                e1, e2 = evs_sorted[i], evs_sorted[j]
                # Skip if same person (already covered)
                if (e1.get("person_name_en") and
                    e1.get("person_name_en") == e2.get("person_name_en")):
                    continue

                y1 = e1.get("event_year") or 0
                y2 = e2.get("event_year") or 0
                gap = abs(y2 - y1)

                if gap > 50:
                    continue

                if gap <= 5:
                    rel_type = "co-located_contemporary"
                    strength = "strong"
                elif gap <= 20:
                    rel_type = "local_succession"
                    strength = "moderate"
                else:
                    rel_type = "local_tradition"
                    strength = "weak"

                relationships.append({
                    "source": e1.get("title_en", ""),
                    "target": e2.get("title_en", ""),
                    "type": rel_type,
                    "strength": strength,
                    "mechanism": "geographic_temporal",
                    "location": loc,
                    "year_gap": gap,
                })

    return relationships


# =============================================================================
# Strategy 4: Concept-mediated (improved from original)
# =============================================================================

def build_concept_relationships(events, links):
    """Original concept-mediated approach with better matching."""
    si_titles = {e.get("title_en", ""): e for e in events}
    si_by_norm = {}
    for e in events:
        norm = e.get("title_en", "").lower().strip()
        si_by_norm[norm] = e

    def find_si_event(title):
        if title in si_titles:
            return si_titles[title]
        norm = title.lower().strip()
        if norm in si_by_norm:
            return si_by_norm[norm]
        for si_title in si_titles:
            if len(norm) > 10 and (norm in si_title.lower() or si_title.lower() in norm):
                return si_titles[si_title]
        return None

    concept_events = defaultdict(list)
    for link in links:
        event_title = link.get("event_title_en", "")
        si_ev = find_si_event(event_title)
        if si_ev is not None:
            concept_events[link.get("concept_name_en", "")].append({
                "event": si_ev.get("title_en", ""),
                "type": link.get("link_type"),
            })

    relationships = []
    for concept, event_list in concept_events.items():
        unique = {el["event"]: el for el in event_list}
        unique_list = list(unique.values())
        if len(unique_list) < 2:
            continue
        for i in range(len(unique_list)):
            for j in range(i + 1, len(unique_list)):
                e1_title = unique_list[i]["event"]
                e2_title = unique_list[j]["event"]
                if e1_title == e2_title:
                    continue
                ev1 = si_titles.get(e1_title, {})
                ev2 = si_titles.get(e2_title, {})
                y1 = ev1.get("event_year") or 0
                y2 = ev2.get("event_year") or 0

                relationships.append({
                    "source": e1_title if y1 <= y2 else e2_title,
                    "target": e2_title if y1 <= y2 else e1_title,
                    "type": "concept_linked",
                    "strength": "moderate",
                    "mechanism": "shared_concept",
                    "concept": concept,
                    "year_gap": abs(y2 - y1),
                })

    return relationships


# =============================================================================
# Strategy 5: LLM-based structural similarity (batch processing)
# =============================================================================

def get_api_key():
    try:
        return subprocess.check_output(
            ["security", "find-generic-password", "-a", "anthropic", "-w"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return os.environ.get("ANTHROPIC_API_KEY", "")


def build_llm_relationships(events, existing_rels, progress_path):
    """Use LLM to identify structural influence relationships.
    Groups events by era+civilization and asks LLM to identify
    cross-event influences within each group."""
    import anthropic

    api_key = get_api_key()
    if not api_key:
        print("  No API key found, skipping LLM relationships")
        return []

    client = anthropic.Anthropic(api_key=api_key)

    # Load progress
    progress = {}
    if progress_path.exists():
        with open(progress_path) as f:
            progress = json.load(f)

    # Build groups: era + civilization (manageable size)
    groups = defaultdict(list)
    for e in events:
        era = e.get("era", "unknown")
        civ = e.get("civilization", "unclassified")
        groups[(era, civ)].append(e)

    # Filter to groups with 3-80 events
    valid_groups = {k: v for k, v in groups.items() if 3 <= len(v) <= 80}
    print(f"  LLM groups to process: {len(valid_groups)}")

    all_relationships = []
    processed = 0

    for (era, civ), grp_events in sorted(valid_groups.items()):
        group_key = f"{era}_{civ}"
        if group_key in progress:
            all_relationships.extend(progress[group_key])
            processed += 1
            continue

        # Build compact event list for prompt
        event_summaries = []
        for i, e in enumerate(sorted(grp_events, key=lambda x: x.get("event_year") or 0)):
            analysis = e.get("structural_analysis", "")[:200]
            event_summaries.append(
                f"[{i}] {e.get('title_en', '')} ({e.get('event_year', '?')}) — {analysis}"
            )

        prompt = f"""以下は{era}時代・{civ}文明圏のソーシャルイノベーション事象リストです。
これらの事象間で、構造的な影響関係（あるイベントが別のイベントの制度的前提・思想的基盤・直接的契機となった関係）を特定してください。

事象リスト:
{chr(10).join(event_summaries)}

以下のJSON形式で、影響関係を出力してください。明確な根拠がある関係のみ含めてください（推測は不要）。
各関係の"evidence"には、なぜこの影響関係が成立するかを1文で説明してください。

```json
[
  {{"source_idx": 0, "target_idx": 1, "type": "caused|enabled|inspired|opposed", "evidence": "..."}}
]
```

関係がない場合は空配列[]を返してください。"""

        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=2000,
                temperature=0,
                messages=[{"role": "user", "content": prompt}],
                timeout=90.0,
            )
            text = response.content[0].text

            # Extract JSON
            import re
            json_match = re.search(r'\[[\s\S]*?\]', text)
            if json_match:
                rels_raw = json.loads(json_match.group())
            else:
                rels_raw = []

            group_rels = []
            sorted_events = sorted(grp_events, key=lambda x: x.get("event_year") or 0)
            for r in rels_raw:
                si = r.get("source_idx", -1)
                ti = r.get("target_idx", -1)
                if 0 <= si < len(sorted_events) and 0 <= ti < len(sorted_events) and si != ti:
                    src = sorted_events[si]
                    tgt = sorted_events[ti]
                    group_rels.append({
                        "source": src.get("title_en", ""),
                        "target": tgt.get("title_en", ""),
                        "type": r.get("type", "influenced"),
                        "strength": "strong",
                        "mechanism": "llm_structural",
                        "evidence": r.get("evidence", ""),
                        "year_gap": abs((tgt.get("event_year") or 0) - (src.get("event_year") or 0)),
                    })

            all_relationships.extend(group_rels)
            progress[group_key] = group_rels
            processed += 1

            # Save progress
            with open(progress_path, "w") as f:
                json.dump(progress, f, ensure_ascii=False)

            print(f"  [{processed}/{len(valid_groups)}] {group_key}: {len(group_rels)} relationships found")
            time.sleep(0.5)

        except Exception as ex:
            print(f"  Error on {group_key}: {ex}")
            time.sleep(2)

    return all_relationships


# =============================================================================
# Deduplication and merging
# =============================================================================

def deduplicate_relationships(all_rels):
    """Merge duplicate pairs, keeping the strongest mechanism."""
    strength_order = {"strong": 3, "moderate": 2, "weak": 1}
    pair_best = {}

    for r in all_rels:
        pair = tuple(sorted([r["source"], r["target"]]))
        existing = pair_best.get(pair)
        if existing is None:
            pair_best[pair] = r
        else:
            # Keep stronger or add mechanism
            curr_s = strength_order.get(r.get("strength", "weak"), 1)
            exist_s = strength_order.get(existing.get("strength", "weak"), 1)
            if curr_s > exist_s:
                # Keep new but note multiple mechanisms
                r["mechanisms"] = list(set([
                    existing.get("mechanism", ""),
                    r.get("mechanism", "")
                ]))
                pair_best[pair] = r
            elif curr_s == exist_s and r.get("mechanism") != existing.get("mechanism"):
                existing["mechanisms"] = list(set(
                    existing.get("mechanisms", [existing.get("mechanism", "")]) +
                    [r.get("mechanism", "")]
                ))
                existing["strength"] = "strong"  # Multiple confirming mechanisms

    return list(pair_best.values())


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--llm", action="store_true", help="Enable LLM-based relationship detection")
    parser.add_argument("--resume", action="store_true", help="Resume LLM processing from progress file")
    args = parser.parse_args()

    print("=" * 60)
    print("SIF Relationship Builder — Multi-Strategy Analysis")
    print("=" * 60)

    events = load_si_events()
    links = load_links()
    print(f"Loaded {len(events)} SI events, {len(links)} concept links")

    all_relationships = []

    # Strategy 1: Person-based
    print("\n[1/5] Person-based relationships...")
    person_rels = build_person_relationships(events)
    print(f"  Found: {len(person_rels)}")
    all_relationships.extend(person_rels)

    # Strategy 2: Thematic clustering
    print("\n[2/5] Thematic cluster relationships...")
    thematic_rels = build_thematic_relationships(events)
    print(f"  Found: {len(thematic_rels)}")
    all_relationships.extend(thematic_rels)

    # Strategy 3: Geographic-temporal
    print("\n[3/5] Geographic-temporal relationships...")
    geo_rels = build_geographic_relationships(events)
    print(f"  Found: {len(geo_rels)}")
    all_relationships.extend(geo_rels)

    # Strategy 4: Concept-mediated
    print("\n[4/5] Concept-mediated relationships...")
    concept_rels = build_concept_relationships(events, links)
    print(f"  Found: {len(concept_rels)}")
    all_relationships.extend(concept_rels)

    # Strategy 5: LLM-based (optional)
    if args.llm:
        print("\n[5/5] LLM-based structural relationships...")
        progress_path = DATA_DIR / "sif_relationship_llm_progress.json"
        llm_rels = build_llm_relationships(events, all_relationships, progress_path)
        print(f"  Found: {len(llm_rels)}")
        all_relationships.extend(llm_rels)
    else:
        print("\n[5/5] LLM-based relationships: SKIPPED (use --llm to enable)")

    # Filter out empty source/target
    all_relationships = [r for r in all_relationships if r.get("source") and r.get("target")]

    # Deduplicate
    print(f"\nTotal raw relationships: {len(all_relationships)}")
    deduped = deduplicate_relationships(all_relationships)
    print(f"After deduplication: {len(deduped)}")

    # Statistics
    by_mechanism = Counter(r.get("mechanism", "unknown") for r in deduped)
    by_strength = Counter(r.get("strength", "unknown") for r in deduped)
    by_type = Counter(r.get("type", "unknown") for r in deduped)
    print(f"\nBy mechanism: {dict(by_mechanism)}")
    print(f"By strength: {dict(by_strength)}")
    print(f"By type: {dict(by_type)}")

    # Network metrics
    node_degree = Counter()
    for r in deduped:
        node_degree[r["source"]] += 1
        node_degree[r["target"]] += 1
    connected = len(node_degree)
    print(f"\nConnected events: {connected}/{len(events)} ({100*connected/len(events):.1f}%)")
    if node_degree:
        top_hubs = node_degree.most_common(10)
        print("Top hubs:")
        for title, degree in top_hubs:
            print(f"  [{degree}] {title}")

    # Save
    output = {
        "metadata": {
            "total_events": len(events),
            "total_relationships": len(deduped),
            "connected_events": connected,
            "strategies": ["person", "thematic", "geographic", "concept"] + (["llm"] if args.llm else []),
            "by_mechanism": dict(by_mechanism),
            "by_strength": dict(by_strength),
        },
        "relationships": deduped,
    }
    out_path = DATA_DIR / "sif_relationships.json"
    with open(out_path, "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
