#!/usr/bin/env python3
"""
Enrich SIF events with detailed structural descriptions.

For each SI event selected by analyze_sif.py, generate a detailed description
of the structural system changes using Claude Haiku. Saves progress incrementally.

Usage:
    python3 scripts/enrich_sif_events.py [--batch-size 20] [--resume]
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

import anthropic

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Output file for enriched events
OUTPUT_FILE = DATA_DIR / "sif_enriched_events.json"
PROGRESS_FILE = DATA_DIR / "sif_enrichment_progress.json"

# Import SI selection logic from analyze_sif
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
from analyze_sif import (
    load_data, merge_events, select_si_events, compute_si_keyword_score,
    classify_civilization, classify_era, classify_si_type
)

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 600

SYSTEM_PROMPT = """あなたは歴史社会学の専門家です。与えられた歴史的事象について、
「ソーシャルイノベーション（社会構造変革）」の観点から構造的分析を日本語で記述してください。

以下の5つの次元で分析してください：
1. **問題構造（P）**: この事象が応答した社会的問題の構造的根深さ
2. **制度的応答（R1）**: 導入された制度・法・規範の新規性
3. **波及範囲（R2）**: 地理的・時間的な影響範囲
4. **関係性再編（R3）**: 社会集団間の関係がどう組み替えられたか
5. **認知変容（C）**: 人々の問題認識・世界観がどう変わったか

300-500字の地の文で記述してください。箇条書きではなく散文で。
事実に基づき、推測は最小限にしてください。"""


def get_api_key():
    """Get Anthropic API key from keychain."""
    try:
        key = subprocess.check_output(
            ["security", "find-generic-password", "-l", "anthropic", "-w"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return key
    except subprocess.CalledProcessError:
        # Try alternate keychain entries
        try:
            key = subprocess.check_output(
                ["security", "find-generic-password", "-a", "anthropic", "-w"],
                stderr=subprocess.DEVNULL
            ).decode().strip()
            return key
        except subprocess.CalledProcessError:
            print("ERROR: Anthropic API key not found in keychain")
            sys.exit(1)


def build_prompt(event):
    """Build a prompt for structural description generation."""
    title_ja = event.get("title_ja", "") or ""
    title_en = event.get("title_en", "") or ""
    desc_ja = event.get("description_ja", "") or ""
    desc_en = event.get("description_en", "") or ""
    outcome_ja = event.get("outcome_ja", "") or ""
    outcome_en = event.get("outcome_en", "") or ""
    year = event.get("event_year", "不明")
    location = event.get("location_en", "") or event.get("location_ja", "") or "不明"
    person = event.get("person_name_en", "") or ""

    prompt = f"""以下の歴史的事象について、社会構造変革（ソーシャルイノベーション）の観点から構造的分析を記述してください。

【事象】{title_ja}（{title_en}）
【年代】{year}年
【場所】{location}
【人物】{person}
【概要】{desc_ja} {desc_en}
【結果】{outcome_ja} {outcome_en}

P（問題構造）・R1（制度的応答）・R2（波及範囲）・R3（関係性再編）・C（認知変容）の5次元で、300-500字の散文で分析してください。"""

    return prompt


def enrich_batch(client, events, start_idx, batch_size):
    """Enrich a batch of events. Returns list of enriched events."""
    enriched = []
    end_idx = min(start_idx + batch_size, len(events))

    for i in range(start_idx, end_idx):
        event = events[i]
        title = event.get("title_ja", event.get("title_en", "?"))

        try:
            prompt = build_prompt(event)
            response = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
                timeout=60.0,
            )
            description = response.content[0].text

            enriched_event = {
                "title_ja": event.get("title_ja", ""),
                "title_en": event.get("title_en", ""),
                "event_year": event.get("event_year"),
                "location_en": event.get("location_en", ""),
                "location_ja": event.get("location_ja", ""),
                "person_name_en": event.get("person_name_en", ""),
                "event_type": event.get("event_type", ""),
                "importance": event.get("importance"),
                "description_ja": event.get("description_ja", ""),
                "description_en": event.get("description_en", ""),
                "outcome_ja": event.get("outcome_ja", ""),
                "outcome_en": event.get("outcome_en", ""),
                "structural_analysis": description,
                "civilization": classify_civilization(event),
                "era": classify_era(event),
                "si_type": classify_si_type(event),
            }
            enriched.append(enriched_event)

            # Progress indicator
            progress = i + 1
            print(f"  [{progress}/{len(events)}] {title[:40]}... ({len(description)}字)")

        except anthropic.APIError as e:
            print(f"  [{i+1}/{len(events)}] ERROR: {title[:40]}: {e}")
            # Save what we have and continue
            enriched_event = {
                "title_ja": event.get("title_ja", ""),
                "title_en": event.get("title_en", ""),
                "event_year": event.get("event_year"),
                "location_en": event.get("location_en", ""),
                "person_name_en": event.get("person_name_en", ""),
                "event_type": event.get("event_type", ""),
                "importance": event.get("importance"),
                "description_ja": event.get("description_ja", ""),
                "description_en": event.get("description_en", ""),
                "outcome_ja": event.get("outcome_ja", ""),
                "outcome_en": event.get("outcome_en", ""),
                "structural_analysis": None,
                "civilization": classify_civilization(event),
                "era": classify_era(event),
                "si_type": classify_si_type(event),
                "_error": str(e),
            }
            enriched.append(enriched_event)

            # If rate limited, wait
            if "rate" in str(e).lower():
                print("  Rate limited. Waiting 60s...")
                time.sleep(60)
            elif "credit" in str(e).lower() or "balance" in str(e).lower():
                print("  Credit balance too low. Stopping.")
                return enriched, True  # Signal to stop

        # Delay to avoid rate limits (Haiku has generous limits)
        time.sleep(0.5)

    return enriched, False


def save_progress(enriched_events, total, processed):
    """Save enriched events and progress."""
    # Save enriched events
    with open(OUTPUT_FILE, "w") as f:
        json.dump({
            "metadata": {
                "total_events": total,
                "enriched_count": len(enriched_events),
                "enriched_with_analysis": sum(1 for e in enriched_events if e.get("structural_analysis")),
                "model": MODEL,
            },
            "events": enriched_events,
        }, f, ensure_ascii=False, indent=2)

    # Save progress
    with open(PROGRESS_FILE, "w") as f:
        json.dump({"processed": processed, "total": total}, f)

    print(f"  Saved: {len(enriched_events)} events to {OUTPUT_FILE}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=50,
                        help="Number of events per batch")
    parser.add_argument("--resume", action="store_true",
                        help="Resume from last progress")
    args = parser.parse_args()

    print("=" * 60)
    print("SIF Event Enrichment Pipeline")
    print("=" * 60)

    # Load and select SI events
    print("\n[1/3] Loading and selecting SI events...")
    consolidated, cases = load_data()
    all_events = merge_events(consolidated, cases)
    si_events = select_si_events(all_events)
    print(f"  SI events to enrich: {len(si_events)}")

    # Sort by importance (highest first) for best ROI
    si_events.sort(key=lambda e: (e.get("importance", 0) or 0, e.get("_si_keyword_score", 0)), reverse=True)

    # Resume logic
    start_idx = 0
    existing_enriched = []
    if args.resume and OUTPUT_FILE.exists():
        with open(OUTPUT_FILE) as f:
            existing_data = json.load(f)
            existing_enriched = existing_data.get("events", [])
        if PROGRESS_FILE.exists():
            with open(PROGRESS_FILE) as f:
                progress = json.load(f)
                start_idx = progress.get("processed", 0)
        print(f"  Resuming from event {start_idx} ({len(existing_enriched)} already enriched)")

    # Initialize API client
    print("\n[2/3] Connecting to Anthropic API...")
    api_key = get_api_key()
    client = anthropic.Anthropic(api_key=api_key)
    print(f"  Model: {MODEL}")
    print(f"  Batch size: {args.batch_size}")

    # Process in batches
    print(f"\n[3/3] Enriching events (starting from {start_idx})...")
    all_enriched = list(existing_enriched)
    total = len(si_events)

    for batch_start in range(start_idx, total, args.batch_size):
        batch_end = min(batch_start + args.batch_size, total)
        print(f"\n--- Batch {batch_start}-{batch_end} of {total} ---")

        batch_enriched, should_stop = enrich_batch(
            client, si_events, batch_start, args.batch_size
        )
        all_enriched.extend(batch_enriched)

        # Save after each batch
        save_progress(all_enriched, total, batch_end)

        if should_stop:
            print("\nStopping due to API error. Use --resume to continue later.")
            break

    # Final summary
    with_analysis = sum(1 for e in all_enriched if e.get("structural_analysis"))
    without = sum(1 for e in all_enriched if not e.get("structural_analysis"))
    print(f"\n{'=' * 60}")
    print(f"COMPLETE: {with_analysis} enriched, {without} failed, {total} total")
    print(f"Output: {OUTPUT_FILE}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
