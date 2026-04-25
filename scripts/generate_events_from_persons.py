#!/usr/bin/env python3
"""
Generate structured events from person summary data.
Extracts key events from summary_ja/en text and person metadata.
Target: ~10,000 events from 12,585 persons.
"""
import json
import os
import re
import glob
from collections import defaultdict

DATA_DIR = os.path.expanduser("~/projects/research/great-figures-db/data")
OUTPUT = os.path.expanduser("~/projects/research/miratuku-news-v2/data/gf_events_expanded.json")

# Event type mapping from category_primary
CATEGORY_TO_EVENT_TYPES = {
    "monarch": ["succession", "reform", "conquest"],
    "military": ["military", "conquest", "alliance"],
    "politician": ["political", "reform", "diplomatic"],
    "revolutionary": ["revolution", "reform", "conflict"],
    "diplomat": ["diplomatic", "alliance", "negotiation"],
    "entrepreneur": ["founding", "innovation", "growth"],
    "business": ["founding", "economic", "growth"],
    "industrialist": ["founding", "innovation", "economic"],
    "inventor": ["innovation", "founding", "publication"],
    "scientist": ["discovery", "publication", "innovation"],
    "philosopher": ["intellectual", "publication", "theory"],
    "writer": ["publication", "cultural", "intellectual"],
    "artist": ["cultural", "innovation", "legacy"],
    "religious": ["religious", "reform", "founding"],
    "explorer": ["exploration", "discovery", "founding"],
    "reformer": ["reform", "political", "social_reform"],
    "jurist": ["reform", "legal", "publication"],
    "economist": ["theory", "publication", "economic"],
    "educator": ["reform", "founding", "intellectual"],
    "architect": ["construction", "cultural", "innovation"],
    "engineer": ["innovation", "construction", "founding"],
    "physician": ["medical", "discovery", "publication"],
    "commander": ["military", "conquest", "conflict"],
    "admiral": ["military", "conquest", "exploration"],
    "general": ["military", "conquest", "conflict"],
    "activist": ["activism", "social_reform", "protest"],
    "builder": ["construction", "reform", "legacy"],
    "administrator": ["reform", "political", "administrative"],
    "merchant": ["economic", "founding", "growth"],
    "banker": ["economic", "founding", "growth"],
    "financier": ["economic", "founding", "growth"],
}

# Japanese summary keywords that indicate specific event types
EVENT_KEYWORDS_JA = {
    "統一": ("conquest", "統一", 5),
    "征服": ("conquest", "征服", 5),
    "建国": ("founding", "建国", 5),
    "創設": ("founding", "創設", 4),
    "創業": ("founding", "創業", 5),
    "設立": ("founding", "設立", 4),
    "発明": ("innovation", "発明", 5),
    "発見": ("discovery", "発見", 5),
    "改革": ("reform", "改革", 4),
    "革命": ("revolution", "革命", 5),
    "法典": ("reform", "法典制定", 5),
    "条約": ("diplomatic", "条約", 4),
    "戦争": ("military", "戦争", 4),
    "戦い": ("military", "戦い", 4),
    "勝利": ("military", "勝利", 4),
    "敗北": ("defeat", "敗北", 3),
    "即位": ("succession", "即位", 4),
    "継承": ("succession", "継承", 3),
    "統治": ("political", "統治", 4),
    "独立": ("political", "独立運動", 5),
    "貿易": ("economic", "貿易", 4),
    "著書": ("publication", "著作", 4),
    "理論": ("theory", "理論提唱", 4),
    "布教": ("religious", "布教", 4),
    "探検": ("exploration", "探検", 5),
    "航海": ("exploration", "航海", 5),
    "建設": ("construction", "建設", 4),
    "拡大": ("expansion", "領土拡大", 4),
    "同盟": ("alliance", "同盟", 4),
    "交渉": ("negotiation", "交渉", 3),
    "開発": ("innovation", "開発", 4),
    "受賞": ("recognition", "受賞", 3),
    "ノーベル": ("recognition", "ノーベル賞", 5),
}


def load_persons():
    """Load all persons from wave files."""
    all_persons = []
    for f in sorted(glob.glob(f"{DATA_DIR}/wave*.json")):
        data = json.load(open(f))
        for k, v in data.items():
            if isinstance(v, list):
                all_persons.extend(v)
    return all_persons


def load_existing_events():
    """Load existing events to avoid duplicates."""
    existing = set()
    for f in sorted(glob.glob(f"{DATA_DIR}/events*.json")):
        data = json.load(open(f))
        for k, v in data.items():
            if isinstance(v, list):
                for e in v:
                    key = (e.get("person_name_en", ""), e.get("title_en", ""))
                    existing.add(key)
    return existing


def extract_events_from_person(person, existing):
    """Extract events from a single person record."""
    name_en = person.get("name_en", "")
    name_ja = person.get("name_ja", "")
    summary_ja = person.get("summary_ja", "")
    summary_en = person.get("summary_en", "")
    birth_year = person.get("birth_year")
    death_year = person.get("death_year")
    era = person.get("era", "unknown")
    region = person.get("region_primary", "")
    country = person.get("country_modern", "")
    cat_primary = person.get("category_primary", "")
    cat_secondary = person.get("category_secondary", "")

    if not summary_ja or len(summary_ja) < 5:
        return []

    events = []

    # 1. Main career event (from category)
    event_types = CATEGORY_TO_EVENT_TYPES.get(cat_primary, ["legacy"])
    main_type = event_types[0]

    # Calculate mid-career year
    if birth_year and death_year:
        mid_year = birth_year + (death_year - birth_year) // 3
    elif birth_year:
        mid_year = birth_year + 30
    else:
        mid_year = None

    main_event = {
        "person_name_en": name_en,
        "person_name_ja": name_ja,
        "title_ja": f"{name_ja}の主要業績",
        "title_en": f"Key Achievement of {name_en}",
        "event_year": mid_year,
        "location_en": f"{country or region}",
        "event_type": main_type,
        "importance": 4,
        "description_ja": summary_ja,
        "description_en": summary_en,
        "outcome_ja": f"{cat_primary}分野における歴史的貢献",
        "outcome_en": f"Historical contribution in {cat_primary}",
    }
    key = (name_en, main_event["title_en"])
    if key not in existing:
        events.append(main_event)
        existing.add(key)

    # 2. Keyword-based specific events
    for keyword, (etype, action_ja, importance) in EVENT_KEYWORDS_JA.items():
        if keyword in summary_ja:
            specific_event = {
                "person_name_en": name_en,
                "person_name_ja": name_ja,
                "title_ja": f"{name_ja}の{action_ja}",
                "title_en": f"{action_ja} by {name_en}",
                "event_year": mid_year,
                "location_en": f"{country or region}",
                "event_type": etype,
                "importance": importance,
                "description_ja": f"{summary_ja}（{action_ja}に関連）",
                "description_en": f"{summary_en} (related to {action_ja})",
                "outcome_ja": f"{action_ja}による社会的影響",
                "outcome_en": f"Social impact through {action_ja}",
            }
            key = (name_en, specific_event["title_en"])
            if key not in existing:
                events.append(specific_event)
                existing.add(key)
                break  # One additional event per person max

    # 3. Birth/death events for important figures (importance >= 4 from category)
    if cat_primary in ["monarch", "revolutionary", "entrepreneur"] and birth_year:
        if cat_secondary in ["military", "reformer", "founder"]:
            rise_event = {
                "person_name_en": name_en,
                "person_name_ja": name_ja,
                "title_ja": f"{name_ja}の台頭",
                "title_en": f"Rise of {name_en}",
                "event_year": birth_year + 25 if birth_year else None,
                "location_en": f"{country or region}",
                "event_type": "succession" if cat_primary == "monarch" else "founding",
                "importance": 3,
                "description_ja": f"{name_ja}が{cat_primary}として台頭した時期",
                "description_en": f"Period when {name_en} rose to prominence as {cat_primary}",
                "outcome_ja": f"{region}における権力構造の変化",
                "outcome_en": f"Shift in power structure in {region}",
            }
            key = (name_en, rise_event["title_en"])
            if key not in existing:
                events.append(rise_event)
                existing.add(key)

    return events


def main():
    print("Loading persons...")
    persons = load_persons()
    print(f"  {len(persons)} persons loaded")

    print("Loading existing events...")
    existing = load_existing_events()
    print(f"  {len(existing)} existing events")

    print("Generating events...")
    new_events = []
    for p in persons:
        evts = extract_events_from_person(p, existing)
        new_events.extend(evts)

    print(f"  {len(new_events)} new events generated")
    total = len(existing) + len(new_events)
    print(f"  Total events: {total}")

    # Save
    with open(OUTPUT, "w") as f:
        json.dump({"events": new_events, "count": len(new_events)}, f, ensure_ascii=False, indent=1)
    print(f"  Saved to {OUTPUT}")

    # Also update consolidated data
    consolidated_path = os.path.expanduser("~/projects/research/miratuku-news-v2/data/gf_consolidated.json")
    consolidated = json.load(open(consolidated_path))
    consolidated["events"].extend(new_events)
    with open(consolidated_path, "w") as f:
        json.dump(consolidated, f, ensure_ascii=False)
    print(f"  Updated consolidated data: {len(consolidated['events'])} total events")


if __name__ == "__main__":
    main()
