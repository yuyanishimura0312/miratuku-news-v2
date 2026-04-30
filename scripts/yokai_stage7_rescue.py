#!/usr/bin/env python3
"""Rescue partial Stage 7 data from raw batch files."""
import json
import glob
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

results = []
rescued_count = 0
failed_count = 0

for raw_file in sorted(glob.glob(str(DATA_DIR / "yokai-stage7-raw-batch*.txt"))):
    with open(raw_file) as f:
        text = f.read()

    # Remove markdown fences
    if "```json" in text:
        text = text.split("```json", 1)[1]
    if "```" in text:
        text = text.split("```")[0]

    text = text.strip()

    # Try to fix truncated JSON
    # Find all complete yokai objects by matching balanced braces
    depth = 0
    start = None
    objects = []

    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 1:  # Start of a yokai object (inside the array)
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 1 and start is not None:  # End of a yokai object
                obj_str = text[start:i + 1]
                try:
                    obj = json.loads(obj_str)
                    if "id" in obj and "personality_deep" in obj:
                        objects.append(obj)
                except json.JSONDecodeError:
                    pass
                start = None

    if objects:
        results.extend(objects)
        rescued_count += len(objects)
    else:
        failed_count += 1

print(f"Raw files processed: {len(glob.glob(str(DATA_DIR / 'yokai-stage7-raw-batch*.txt')))}")
print(f"Rescued entries: {rescued_count}")
print(f"Failed files: {failed_count}")

# Check quality
has_big_five = sum(1 for r in results if r.get("personality_deep", {}).get("big_five"))
has_archetype = sum(1 for r in results if r.get("personality_deep", {}).get("archetype"))
has_shadow = sum(1 for r in results if r.get("personality_deep", {}).get("shadow_aspects"))
has_defense = sum(1 for r in results if r.get("personality_deep", {}).get("defense_mechanisms"))
print(f"big_five: {has_big_five}/{len(results)}")
print(f"archetype: {has_archetype}/{len(results)}")
print(f"shadow_aspects: {has_shadow}/{len(results)}")
print(f"defense_mechanisms: {has_defense}/{len(results)}")

# Deduplicate by ID
seen = {}
for r in results:
    yid = r.get("id", "")
    if yid and yid not in seen:
        seen[yid] = r
unique = list(seen.values())
print(f"Unique entries: {len(unique)}")

# Save
output = DATA_DIR / "yokai-personality-rescued.json"
with open(output, "w") as f:
    json.dump(unique, f, ensure_ascii=False, indent=2)
print(f"Output: {output}")
