#!/usr/bin/env python3
"""
Stage 6: Merge all enrichment data into yokai-data.json.
Merges: behavioral data (Stage 4) + ontological roles (Stage 5).

Usage:
    python3 scripts/yokai_stage6_merge.py
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MAIN_FILE = DATA_DIR / "yokai-data.json"
BEHAVIORAL_FILE = DATA_DIR / "yokai-behavioral-complete.json"
ROLES_FILE = DATA_DIR / "yokai-ontological-roles.json"
BACKUP_FILE = DATA_DIR / "yokai-data-backup-pre-stage6.json"

BEHAVIORAL_FIELDS = [
    "behavioral_patterns", "narrative_episodes", "speech_examples",
    "ritual_behaviors", "interaction_patterns"
]


def main():
    print("=== Stage 6: Data Merge ===")

    # Load main data
    with open(MAIN_FILE) as f:
        main_data = json.load(f)
    print(f"Main data: {len(main_data)} yokai")

    # Backup
    with open(BACKUP_FILE, "w") as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2)
    print(f"Backup saved: {BACKUP_FILE}")

    # Load enrichments
    with open(BEHAVIORAL_FILE) as f:
        behavioral = json.load(f)
    behavioral_map = {r["id"]: r for r in behavioral if "id" in r}
    print(f"Behavioral data: {len(behavioral_map)} entries")

    with open(ROLES_FILE) as f:
        roles = json.load(f)
    roles_map = {r["id"]: r for r in roles if "id" in r}
    print(f"Ontological roles: {len(roles_map)} entries")

    # Merge
    merged_behavioral = 0
    merged_roles = 0

    for yokai in main_data:
        yid = yokai["id"]

        # Merge behavioral data
        if yid in behavioral_map:
            bdata = behavioral_map[yid]
            for field in BEHAVIORAL_FIELDS:
                val = bdata.get(field)
                if val:
                    yokai[field] = val
            merged_behavioral += 1

        # Merge ontological role
        if yid in roles_map:
            rdata = roles_map[yid]
            if "ontological_role" in rdata:
                yokai["ontological_role"] = rdata["ontological_role"]
                merged_roles += 1

    # Save
    with open(MAIN_FILE, "w") as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2)

    # Verify
    print(f"\n=== Merge Complete ===")
    print(f"Behavioral merged: {merged_behavioral}/{len(main_data)}")
    print(f"Ontological roles merged: {merged_roles}/{len(main_data)}")

    # Field coverage report
    all_fields = BEHAVIORAL_FIELDS + ["ontological_role"]
    for field in all_fields:
        count = sum(1 for y in main_data if y.get(field))
        pct = 100 * count / len(main_data)
        print(f"  {field}: {count} ({pct:.1f}%)")

    print(f"\nOutput: {MAIN_FILE}")
    print(f"Total fields per yokai: {len(main_data[0].keys())}")


if __name__ == "__main__":
    main()
