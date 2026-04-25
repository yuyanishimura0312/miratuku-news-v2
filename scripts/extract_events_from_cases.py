#!/usr/bin/env python3
"""
Extract structured events from great-figures-db case study files.

Case files contain 7,000-10,000 word Japanese narrative analyses.
Each ## section becomes one event record with authentic content from the case.
"""

import json
import os
import re
import sys
from pathlib import Path

# Paths
CASES_DIR = Path("/Users/nishimura+/projects/research/great-figures-db/data")
OUTPUT_FILE = Path("/Users/nishimura+/projects/research/miratuku-news-v2/data/gf_events_cases.json")
CONSOLIDATED_FILE = Path("/Users/nishimura+/projects/research/miratuku-news-v2/data/gf_consolidated.json")

# --- Helpers ---

# Keyword → event_type mapping
EVENT_TYPE_KEYWORDS = {
    "founding": ["建国", "創設", "設立", "創業", "建立", "樹立", "創立"],
    "reform": ["改革", "改正", "制度改革", "税制", "廃止", "変革", "刷新"],
    "military": ["戦争", "戦闘", "征服", "遠征", "侵攻", "軍事", "包囲", "戦略", "戦術", "勝利", "敗北"],
    "law": ["法典", "法律", "条文", "立法", "規則", "条約"],
    "innovation": ["発明", "革新", "技術", "イノベーション", "開発", "発見"],
    "trade": ["貿易", "交易", "商業", "商取引", "経済", "市場"],
    "diplomacy": ["外交", "同盟", "条約", "交渉", "和解", "結婚同盟", "政略"],
    "administration": ["統治", "行政", "官僚", "制度", "組織", "マネジメント", "経営"],
    "religion": ["宗教", "信仰", "神学", "改宗", "礼拝", "寺院", "教会"],
    "education": ["教育", "学問", "知識", "学校", "大学", "研究"],
    "construction": ["建設", "建築", "都市", "宮殿", "要塞", "インフラ"],
    "crisis": ["危機", "崩壊", "失敗", "挫折", "反乱", "失脚", "追放"],
    "leadership": ["リーダーシップ", "意思決定", "判断", "決断", "指導"],
}


def infer_event_type(text: str) -> str:
    """Infer event type from Japanese text by keyword matching."""
    for etype, keywords in EVENT_TYPE_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return etype
    return "leadership"  # default


def extract_year_from_text(text: str, era: str) -> int | None:
    """Extract a year (CE or BCE) from Japanese narrative text."""
    # Match patterns like 1556年, 紀元前18世紀, 1500年代
    # BCE (紀元前)
    m = re.search(r'紀元前(\d+)世紀', text)
    if m:
        century = int(m.group(1))
        return -(century * 100 - 50)  # midpoint of century

    m = re.search(r'紀元前(\d+)年', text)
    if m:
        return -int(m.group(1))

    # CE 4-digit year
    m = re.search(r'(\d{4})年', text)
    if m:
        year = int(m.group(1))
        if 100 <= year <= 2100:
            return year

    # CE century e.g. 16世紀
    m = re.search(r'(\d{1,2})世紀', text)
    if m:
        century = int(m.group(1))
        return century * 100 - 50  # midpoint

    return None


ERA_YEAR_MAP = {
    "ancient": -2000,
    "classical": -300,
    "medieval": 900,
    "early_modern": 1550,
    "modern": 1850,
    "contemporary": 1970,
}


def era_to_year(era: str) -> int:
    """Map era string to a representative year."""
    return ERA_YEAR_MAP.get(era, 1500)


def clean_heading(heading: str) -> str:
    """Clean ## heading text for use as title."""
    # Remove leading #, numbers like "1.", surrounding quotes, etc.
    h = heading.strip()
    h = re.sub(r'^#+\s*', '', h)
    h = re.sub(r'^\d+[\.\s]+', '', h)
    h = h.strip('「」『』【】')
    return h[:100].strip()


def extract_sentences(text: str, max_chars: int = 300) -> str:
    """Extract first 2-3 sentences from text, up to max_chars."""
    # Split on Japanese sentence endings
    sentences = re.split(r'(?<=[。！？])', text)
    result = ""
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        if len(result) + len(s) <= max_chars:
            result += s
        else:
            break
    return result.strip() if result else text[:max_chars].strip()


def extract_last_sentence(text: str) -> str:
    """Extract last meaningful sentence from text."""
    sentences = re.split(r'(?<=[。！？])', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    if sentences:
        return sentences[-1][:200]
    return text[-150:].strip()


def infer_importance(section_text: str, heading: str) -> int:
    """Score importance 3-5 based on content signals."""
    high_signals = ["革命的", "歴史的", "転換点", "最初", "最大", "最重要", "画期的", "根本", "抜本"]
    low_signals = ["補足", "参考", "付録", "まとめ", "教訓", "現代の"]
    combined = heading + section_text[:200]
    if any(s in combined for s in high_signals):
        return 5
    if any(s in combined for s in low_signals):
        return 3
    return 4


# --- Core extraction ---

def extract_events_from_case(case: dict, existing_titles: set) -> list:
    """Extract event records from a single case dict."""
    content = case.get("content_ja", "")
    person = case.get("person_name_en", "Unknown")
    title_en = case.get("title_en", "")
    era = case.get("era", "")
    era_year = era_to_year(era)

    if not content or len(content) < 500:
        return []

    # Split on ## headings (keep heading with section body)
    # content format: # Title\n## Section1\n...\n## Section2\n...
    raw_sections = re.split(r'\n## ', content)

    events = []
    # Skip section 0 (top-level # title) and section 1 (usually intro/subtitle)
    for raw in raw_sections[2:]:
        lines = raw.split('\n')
        heading_line = lines[0].strip()
        body = '\n'.join(lines[1:]).strip()

        # Skip very short sections (less than 150 chars body)
        if len(body) < 150:
            continue

        # Skip "lessons" / meta sections at the end
        skip_headings = ["まとめ", "おわり", "参考文献", "注釈", "現代の経営者へ", "現代へ", "教訓"]
        if any(sh in heading_line for sh in skip_headings):
            continue

        title_ja = clean_heading(heading_line)
        if not title_ja:
            continue

        # Deduplicate: skip if same person+title already seen
        dedup_key = f"{person}|{title_ja}"
        if dedup_key in existing_titles:
            continue
        existing_titles.add(dedup_key)

        # Extract year from heading + first 500 chars of body
        search_text = heading_line + " " + body[:500]
        event_year = extract_year_from_text(search_text, era) or era_year

        # Paragraphs (non-empty lines)
        paragraphs = [p.strip() for p in body.split('\n') if p.strip() and not p.startswith('#')]

        # Build description from first meaningful paragraphs
        desc_text = ""
        for p in paragraphs:
            if len(p) > 30:  # skip very short lines / headers
                desc_text = p
                break
        description_ja = extract_sentences(desc_text, 300) if desc_text else body[:300]

        # Outcome from last paragraph
        outcome_text = ""
        for p in reversed(paragraphs):
            if len(p) > 30:
                outcome_text = p
                break
        outcome_ja = extract_last_sentence(outcome_text) if outcome_text else ""

        event_type = infer_event_type(heading_line + " " + description_ja)
        importance = infer_importance(body, heading_line)

        event = {
            "person_name_en": person,
            "title_ja": title_ja,
            "title_en": title_en,
            "event_year": event_year,
            "event_year_end": None,
            "location_ja": "",
            "location_en": "",
            "event_type": event_type,
            "importance": importance,
            "description_ja": description_ja,
            "description_en": "",
            "outcome_ja": outcome_ja,
            "outcome_en": "",
            "source": "case_study",
        }
        events.append(event)

    return events


def load_all_cases() -> list:
    """Load all case dicts from case_*.json and cases_*.json files."""
    all_cases = []
    case_files = sorted([
        f for f in CASES_DIR.iterdir()
        if f.name.startswith("case") and f.suffix == ".json"
    ])

    for fpath in case_files:
        try:
            with open(fpath, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"  [WARN] Could not read {fpath.name}: {e}", file=sys.stderr)
            continue

        if isinstance(data, dict) and "cases" in data:
            # Batch file: {"cases": [...]}
            cases = data["cases"]
            all_cases.extend(cases)
            print(f"  {fpath.name}: {len(cases)} cases")
        elif isinstance(data, dict) and "content_ja" in data:
            # Single case file
            all_cases.append(data)
            print(f"  {fpath.name}: 1 case")
        else:
            print(f"  [SKIP] {fpath.name}: unrecognized structure", file=sys.stderr)

    return all_cases


def build_existing_key_set(existing_events: list) -> set:
    """Build dedup keys from events already in consolidated file."""
    keys = set()
    for e in existing_events:
        person = e.get("person_name_en", "")
        title = e.get("title_ja", "")
        keys.add(f"{person}|{title}")
    return keys


def main():
    print("=== extract_events_from_cases.py ===")
    print(f"Cases dir: {CASES_DIR}")
    print(f"Output: {OUTPUT_FILE}")
    print(f"Consolidated: {CONSOLIDATED_FILE}")
    print()

    # Load existing consolidated events for dedup
    print("Loading existing consolidated data...")
    with open(CONSOLIDATED_FILE, encoding="utf-8") as f:
        consolidated = json.load(f)
    existing_events = consolidated.get("events", [])
    print(f"  Existing events: {len(existing_events)}")
    existing_keys = build_existing_key_set(existing_events)

    # Load all cases
    print("\nLoading case files...")
    all_cases = load_all_cases()
    print(f"\nTotal cases loaded: {len(all_cases)}")

    # Extract events
    print("\nExtracting events from case narratives...")
    new_events = []
    seen_keys = set(existing_keys)  # start from existing to avoid cross-case dups too

    per_person_counts: dict[str, int] = {}
    for case in all_cases:
        person = case.get("person_name_en", "Unknown")
        events = extract_events_from_case(case, seen_keys)
        new_events.extend(events)
        if events:
            per_person_counts[person] = per_person_counts.get(person, 0) + len(events)

    print(f"\nExtracted {len(new_events)} new events from {len(per_person_counts)} persons")

    # Show top persons by event count
    top = sorted(per_person_counts.items(), key=lambda x: -x[1])[:20]
    print("\nTop persons by extracted events:")
    for p, n in top:
        print(f"  {p}: {n}")

    # Save new events to output file
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(new_events, f, ensure_ascii=False, indent=2)
    print(f"\nSaved {len(new_events)} events to {OUTPUT_FILE}")

    # Update consolidated file
    print("\nUpdating consolidated file...")
    updated_events = existing_events + new_events
    consolidated["events"] = updated_events

    with open(CONSOLIDATED_FILE, "w", encoding="utf-8") as f:
        json.dump(consolidated, f, ensure_ascii=False, indent=2)
    print(f"Consolidated events: {len(existing_events)} → {len(updated_events)} (+{len(new_events)})")

    # Show sample extracted event
    if new_events:
        print("\nSample extracted event:")
        print(json.dumps(new_events[0], ensure_ascii=False, indent=2))

    print("\nDone.")


if __name__ == "__main__":
    main()
