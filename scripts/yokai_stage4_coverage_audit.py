#!/usr/bin/env python3
"""
Stage 4: Audit and fill coverage gaps from Stage 3.
Identifies yokai with missing/empty behavioral data and re-processes them.

Usage:
    python3 scripts/yokai_stage4_coverage_audit.py [--resume]
"""

import argparse
import json
import subprocess
import time
from pathlib import Path

import anthropic

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
INPUT_FILE = DATA_DIR / "yokai-data.json"
ENRICHMENT_FILE = DATA_DIR / "yokai-behavioral-enrichment.json"
OUTPUT_FILE = DATA_DIR / "yokai-behavioral-complete.json"
PROGRESS_FILE = DATA_DIR / "yokai-stage4-progress.json"

MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 8192

REQUIRED_FIELDS = [
    "behavioral_patterns", "narrative_episodes", "speech_examples",
    "ritual_behaviors", "interaction_patterns"
]


def get_api_key():
    result = subprocess.run(
        ["security", "find-generic-password", "-s", "ANTHROPIC_API_KEY", "-w"],
        capture_output=True, text=True
    )
    return result.stdout.strip()


SYSTEM_PROMPT = """あなたは日本民俗学・比較神話学・文化人類学の専門家です。
与えられた妖怪の情報に基づいて、欠損しているフィールドを学術的に正確に補完してください。

各フィールドの仕様：
- behavioral_patterns: 典型的な行動パターン（3-5個の配列）
- narrative_episodes: 伝承における代表的エピソード（2-4個の配列）
- speech_examples: 発話例・口癖・鳴き声（1-3個の配列、発話しない妖怪は空配列）
- ritual_behaviors: 儀礼的行動・パターン化された行為（1-3個の配列）
- interaction_patterns: 人間との相互作用パターン（2-4個の配列、各要素はtype+description）

伝承に基づかない推測は行わず、不明な場合は空配列で。"""


def find_gaps(all_yokai, enrichment_data):
    """Find yokai with missing or empty behavioral fields."""
    enriched_map = {r["id"]: r for r in enrichment_data if "id" in r}
    gaps = []

    for y in all_yokai:
        yid = y["id"]
        enriched = enriched_map.get(yid, {})
        missing_fields = []

        for field in REQUIRED_FIELDS:
            val = enriched.get(field)
            if val is None or val == [] or val == "":
                missing_fields.append(field)

        if missing_fields:
            gaps.append({"yokai": y, "missing": missing_fields, "existing": enriched})

    return gaps


def build_batch_prompt(gap_batch):
    entries = []
    for gap in gap_batch:
        y = gap["yokai"]
        missing = gap["missing"]
        info = f"""ID: {y['id']}
名前: {y['name_ja']} ({y.get('name_en','')})
起源: {y.get('origin_culture','')} / {y.get('origin_region','')}
文化的役割: {y.get('cultural_role','')}
超自然能力: {json.dumps(y.get('supernatural_abilities',[]), ensure_ascii=False)}
学術的概要: {y.get('scholarly_summary','')}
補完が必要なフィールド: {', '.join(missing)}"""
        entries.append(info)

    batch_text = "\n---\n".join(entries)
    return f"""以下の{len(gap_batch)}体の妖怪について、欠損フィールドを補完してください。

{batch_text}

JSON配列で返してください：
```json
[
  {{
    "id": "妖怪ID",
    "behavioral_patterns": [...],
    "narrative_episodes": [...],
    "speech_examples": [...],
    "ritual_behaviors": [...],
    "interaction_patterns": [{{"type": "...", "description": "..."}}]
  }}
]
```
JSONのみを返してください。"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    print("=== Stage 4: Coverage Audit & Fill ===")

    with open(INPUT_FILE) as f:
        all_yokai = json.load(f)

    with open(ENRICHMENT_FILE) as f:
        enrichment = json.load(f)

    print(f"Total yokai: {len(all_yokai)}")
    print(f"Stage 3 results: {len(enrichment)}")

    # Find gaps
    gaps = find_gaps(all_yokai, enrichment)
    print(f"Yokai with gaps: {len(gaps)}")

    if not gaps:
        print("No gaps found! Copying enrichment as-is.")
        with open(OUTPUT_FILE, "w") as f:
            json.dump(enrichment, f, ensure_ascii=False, indent=2)
        return

    # Show gap summary
    from collections import Counter
    field_counts = Counter()
    for g in gaps:
        for m in g["missing"]:
            field_counts[m] += 1
    print("Gap summary:")
    for field, count in field_counts.most_common():
        print(f"  {field}: {count} missing")

    # Load progress
    if args.resume and PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            progress = json.load(f)
    else:
        progress = {"completed_ids": [], "fill_results": []}

    completed_set = set(progress["completed_ids"])
    remaining_gaps = [g for g in gaps if g["yokai"]["id"] not in completed_set]
    print(f"Remaining gaps to fill: {len(remaining_gaps)}")

    if not remaining_gaps:
        print("All gaps filled!")
    else:
        api_key = get_api_key()
        client = anthropic.Anthropic(api_key=api_key)

        batch_size = 10
        total_batches = (len(remaining_gaps) + batch_size - 1) // batch_size

        for batch_idx in range(total_batches):
            start = batch_idx * batch_size
            batch = remaining_gaps[start:start + batch_size]
            print(f"\n[Fill batch {batch_idx+1}/{total_batches}] {len(batch)} yokai")

            try:
                prompt = build_batch_prompt(batch)
                response = client.messages.create(
                    model=MODEL,
                    max_tokens=MAX_TOKENS,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": prompt}],
                )

                text = response.content[0].text.strip()
                if "```json" in text:
                    text = text.split("```json", 1)[1].split("```", 1)[0]
                elif "```" in text:
                    text = text.split("```", 1)[1].split("```", 1)[0]

                results = json.loads(text)
                if not isinstance(results, list):
                    results = [results]

                for r in results:
                    progress["fill_results"].append(r)
                    progress["completed_ids"].append(r.get("id", ""))
                    completed_set.add(r.get("id", ""))

                print(f"  OK: {len(results)} gaps filled")

            except (json.JSONDecodeError, anthropic.APIError) as e:
                print(f"  ERROR: {e}")
                for g in batch:
                    progress["completed_ids"].append(g["yokai"]["id"])
                    completed_set.add(g["yokai"]["id"])

            with open(PROGRESS_FILE, "w") as f:
                json.dump(progress, f, ensure_ascii=False)
            time.sleep(1.0)

    # Merge: enrichment + fill results
    enriched_map = {r["id"]: r for r in enrichment if "id" in r}
    for fill in progress.get("fill_results", []):
        fid = fill.get("id", "")
        if fid in enriched_map:
            # Only fill missing fields
            for field in REQUIRED_FIELDS:
                if not enriched_map[fid].get(field):
                    enriched_map[fid][field] = fill.get(field, [])
        else:
            enriched_map[fid] = fill

    # Ensure all yokai are present
    for y in all_yokai:
        if y["id"] not in enriched_map:
            enriched_map[y["id"]] = {
                "id": y["id"],
                "behavioral_patterns": [],
                "narrative_episodes": [],
                "speech_examples": [],
                "ritual_behaviors": [],
                "interaction_patterns": []
            }

    final = list(enriched_map.values())
    with open(OUTPUT_FILE, "w") as f:
        json.dump(final, f, ensure_ascii=False, indent=2)

    # Coverage report
    covered = 0
    for r in final:
        has_data = any(r.get(f) for f in REQUIRED_FIELDS)
        if has_data:
            covered += 1

    print(f"\n=== Stage 4 Complete ===")
    print(f"Total entries: {len(final)}")
    print(f"With behavioral data: {covered} ({100*covered/len(final):.1f}%)")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
