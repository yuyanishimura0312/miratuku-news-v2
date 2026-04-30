#!/usr/bin/env python3
"""
Stage 3: Enrich yokai behavioral/narrative data.
Adds: behavioral_patterns, narrative_episodes, speech_examples,
      ritual_behaviors, interaction_patterns

Processes 10 yokai per API call. Resume-safe with progress file.

Usage:
    python3 scripts/yokai_stage3_behavioral_enrichment.py [--resume] [--batch-size 10]
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
INPUT_FILE = DATA_DIR / "yokai-data.json"
OUTPUT_FILE = DATA_DIR / "yokai-behavioral-enrichment.json"
PROGRESS_FILE = DATA_DIR / "yokai-stage3-progress.json"

MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 8192


def get_api_key():
    result = subprocess.run(
        ["security", "find-generic-password", "-s", "ANTHROPIC_API_KEY", "-w"],
        capture_output=True, text=True
    )
    return result.stdout.strip()


SYSTEM_PROMPT = """あなたは日本民俗学・比較神話学・文化人類学の専門家です。
与えられた妖怪の情報に基づいて、以下の5つのフィールドを学術的に正確に生成してください。

1. behavioral_patterns: その妖怪の典型的な行動パターン（3-5個）。観察可能な行動を具体的に記述。
2. narrative_episodes: 伝承・説話における代表的なエピソード（2-4個）。出典がわかれば明記。
3. speech_examples: その妖怪の発話例・口癖・鳴き声（1-3個）。伝承に基づくもの。発話しない妖怪は空配列。
4. ritual_behaviors: 儀礼的行動・パターン化された行為（1-3個）。出現条件、繰り返す行為など。
5. interaction_patterns: 人間や他の存在との相互作用パターン（2-4個）。被害/恩恵/無関心などの分類付き。

各フィールドは配列で、各要素は短い日本語テキスト（1-2文）です。
伝承に基づかない推測は行わず、「不明」や空配列で正直に返してください。
よく知られた妖怪は詳細に、マイナーな妖怪は簡潔にしてください。"""


def build_batch_prompt(yokai_batch):
    """Build prompt for a batch of yokai."""
    entries = []
    for y in yokai_batch:
        info = f"""ID: {y['id']}
名前: {y['name_ja']} ({y.get('name_en','')})
起源: {y.get('origin_culture','')} / {y.get('origin_region','')}
生息地: {y.get('habitat_type','')}
文化的役割: {y.get('cultural_role','')}
性格: {y.get('personality','')}
超自然能力: {json.dumps(y.get('supernatural_abilities',[]), ensure_ascii=False)}
学術的概要: {y.get('scholarly_summary','')}
話し方: {y.get('speech_style','')}
文化的注記: {y.get('cultural_notes','')}"""
        entries.append(info)

    batch_text = "\n---\n".join(entries)
    return f"""以下の{len(yokai_batch)}体の妖怪について、行動・物語データを生成してください。

{batch_text}

以下のJSON配列で返してください。各要素はIDと5つのフィールドを含みます：
```json
[
  {{
    "id": "妖怪ID",
    "behavioral_patterns": ["行動1", "行動2", ...],
    "narrative_episodes": ["エピソード1", ...],
    "speech_examples": ["発話例1", ...],
    "ritual_behaviors": ["儀礼的行動1", ...],
    "interaction_patterns": [
      {{"type": "被害|恩恵|中立|警告|試練", "description": "説明"}}
    ]
  }}
]
```
JSONのみを返してください。"""


def load_progress():
    """Load progress state."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"completed_ids": [], "results": []}


def save_progress(progress):
    """Save progress state."""
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--batch-size", type=int, default=10)
    args = parser.parse_args()

    print("=== Stage 3: Behavioral Enrichment ===")

    with open(INPUT_FILE) as f:
        all_yokai = json.load(f)
    print(f"Total yokai: {len(all_yokai)}")

    # Load or reset progress
    if args.resume:
        progress = load_progress()
        print(f"Resuming: {len(progress['completed_ids'])} already done")
    else:
        progress = {"completed_ids": [], "results": []}

    completed_set = set(progress["completed_ids"])
    remaining = [y for y in all_yokai if y["id"] not in completed_set]
    print(f"Remaining: {len(remaining)}")

    if not remaining:
        print("All done!")
        # Write final output
        with open(OUTPUT_FILE, "w") as f:
            json.dump(progress["results"], f, ensure_ascii=False, indent=2)
        print(f"Output: {OUTPUT_FILE}")
        return

    api_key = get_api_key()
    client = anthropic.Anthropic(api_key=api_key)

    batch_size = args.batch_size
    total_batches = (len(remaining) + batch_size - 1) // batch_size
    errors = 0

    for batch_idx in range(total_batches):
        start = batch_idx * batch_size
        batch = remaining[start:start + batch_size]
        batch_num = batch_idx + 1
        done_total = len(completed_set) + start

        print(f"\n[Batch {batch_num}/{total_batches}] "
              f"({done_total + len(batch)}/{len(all_yokai)}) "
              f"{batch[0]['name_ja']}〜{batch[-1]['name_ja']}")

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

            # Validate and store
            for r in results:
                yid = r.get("id", "")
                progress["results"].append(r)
                progress["completed_ids"].append(yid)
                completed_set.add(yid)

            print(f"  OK: {len(results)} yokai enriched")

        except json.JSONDecodeError as e:
            print(f"  JSON ERROR: {e}")
            errors += 1
            # Save raw for debugging
            raw_path = DATA_DIR / f"yokai-stage3-raw-batch{batch_num}.txt"
            with open(raw_path, "w") as f:
                f.write(response.content[0].text)
            # Mark batch IDs as done to skip on retry
            for y in batch:
                progress["completed_ids"].append(y["id"])
                completed_set.add(y["id"])

        except anthropic.RateLimitError:
            print("  Rate limited. Waiting 60s...")
            time.sleep(60)
            # Don't mark as done — will retry
            continue

        except anthropic.APIError as e:
            print(f"  API ERROR: {e}")
            errors += 1
            if "credit" in str(e).lower():
                print("  Credit exhausted. Stopping.")
                break

        # Save progress after each batch
        save_progress(progress)

        # Delay between batches
        time.sleep(1.0)

    # Write final output
    with open(OUTPUT_FILE, "w") as f:
        json.dump(progress["results"], f, ensure_ascii=False, indent=2)

    print(f"\n=== Stage 3 Complete ===")
    print(f"Enriched: {len(progress['results'])}")
    print(f"Errors: {errors}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
