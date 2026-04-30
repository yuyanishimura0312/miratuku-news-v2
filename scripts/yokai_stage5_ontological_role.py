#!/usr/bin/env python3
"""
Stage 5: Analyze ontological role for each yokai.
Uses Stage 2 framework + Stage 4 behavioral data.
Adds: ontological_role field with role_type, cosmological_function,
      boundary_mediations, human_yokai_interface, ecological_function.

Usage:
    python3 scripts/yokai_stage5_ontological_role.py [--resume] [--batch-size 10]
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
BEHAVIORAL_FILE = DATA_DIR / "yokai-behavioral-complete.json"
FRAMEWORK_FILE = DATA_DIR / "yokai-ontological-framework.json"
OUTPUT_FILE = DATA_DIR / "yokai-ontological-roles.json"
PROGRESS_FILE = DATA_DIR / "yokai-stage5-progress.json"

MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 8192


def get_api_key():
    result = subprocess.run(
        ["security", "find-generic-password", "-s", "ANTHROPIC_API_KEY", "-w"],
        capture_output=True, text=True
    )
    return result.stdout.strip()


def build_system_prompt(framework):
    roles = framework.get("integrated_thesis", {}).get("ontological_roles", [])
    roles_text = "\n".join(f"- {r['role']}: {r['description_ja']}" for r in roles)

    return f"""あなたは比較存在論・文化人類学の専門家です。
各妖怪の行動パターン・伝承・文化的役割に基づいて、存在論的役割を分析してください。

以下はStage 2で定義された存在論的役割カテゴリです：
{roles_text}

各妖怪について以下を分析してください：
1. role_type: 上記6カテゴリから最も適合するもの（複数可）
2. cosmological_function: 宇宙論的機能（秩序維持、境界監視、豊穣保証など）
3. boundary_mediations: 媒介する境界の種類（生/死、人間/自然、聖/俗など）
4. human_yokai_interface: 人間との接点の様態（遭遇条件、交流パターン）
5. ecological_function: 生態的機能（環境保全、資源管理、生態系の象徴的代表など）

全て日本語で、学術的に正確に記述してください。"""


def build_batch_prompt(yokai_batch, behavioral_map):
    entries = []
    for y in yokai_batch:
        yid = y["id"]
        bdata = behavioral_map.get(yid, {})
        info = f"""ID: {yid}
名前: {y['name_ja']} ({y.get('name_en','')})
デスコラ分類: {json.dumps(y.get('descola_classification',{}), ensure_ascii=False)}
文化的役割: {y.get('cultural_role','')}
環世界: {y.get('umwelt_primary','')}
道徳的配置: {y.get('moral_alignment','')}
行動パターン: {json.dumps(bdata.get('behavioral_patterns',[]), ensure_ascii=False)}
相互作用: {json.dumps(bdata.get('interaction_patterns',[]), ensure_ascii=False)}
儀礼的行動: {json.dumps(bdata.get('ritual_behaviors',[]), ensure_ascii=False)}
学術的概要: {y.get('scholarly_summary','')}"""
        entries.append(info)

    batch_text = "\n---\n".join(entries)
    return f"""以下の{len(yokai_batch)}体の妖怪の存在論的役割を分析してください。

{batch_text}

JSON配列で返してください：
```json
[
  {{
    "id": "妖怪ID",
    "ontological_role": {{
      "role_type": ["境界媒介者", ...],
      "cosmological_function": "宇宙論的機能の説明（1-2文）",
      "boundary_mediations": ["生/死", "人間/自然", ...],
      "human_yokai_interface": "人間との接点の説明（1-2文）",
      "ecological_function": "生態的機能の説明（1-2文）"
    }}
  }}
]
```
JSONのみを返してください。"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--batch-size", type=int, default=10)
    args = parser.parse_args()

    print("=== Stage 5: Ontological Role Analysis ===")

    with open(INPUT_FILE) as f:
        all_yokai = json.load(f)
    with open(BEHAVIORAL_FILE) as f:
        behavioral = json.load(f)
    with open(FRAMEWORK_FILE) as f:
        framework = json.load(f)

    behavioral_map = {r["id"]: r for r in behavioral if "id" in r}
    print(f"Total yokai: {len(all_yokai)}")
    print(f"Behavioral data: {len(behavioral_map)}")

    # Progress
    if args.resume and PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            progress = json.load(f)
    else:
        progress = {"completed_ids": [], "results": []}

    completed_set = set(progress["completed_ids"])
    remaining = [y for y in all_yokai if y["id"] not in completed_set]
    print(f"Remaining: {len(remaining)}")

    if not remaining:
        print("All done!")
        with open(OUTPUT_FILE, "w") as f:
            json.dump(progress["results"], f, ensure_ascii=False, indent=2)
        return

    api_key = get_api_key()
    client = anthropic.Anthropic(api_key=api_key)
    system = build_system_prompt(framework)

    batch_size = args.batch_size
    total_batches = (len(remaining) + batch_size - 1) // batch_size

    for batch_idx in range(total_batches):
        start = batch_idx * batch_size
        batch = remaining[start:start + batch_size]
        done_total = len(completed_set) + start + len(batch)
        print(f"\n[Batch {batch_idx+1}/{total_batches}] ({done_total}/{len(all_yokai)})")

        try:
            prompt = build_batch_prompt(batch, behavioral_map)
            response = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=system,
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
                progress["results"].append(r)
                progress["completed_ids"].append(r.get("id", ""))
                completed_set.add(r.get("id", ""))

            print(f"  OK: {len(results)} roles analyzed")

        except json.JSONDecodeError as e:
            print(f"  JSON ERROR: {e}")
            for y in batch:
                progress["completed_ids"].append(y["id"])
                completed_set.add(y["id"])

        except anthropic.RateLimitError:
            print("  Rate limited. Waiting 60s...")
            time.sleep(60)
            continue

        except anthropic.APIError as e:
            print(f"  API ERROR: {e}")
            if "credit" in str(e).lower():
                break
            for y in batch:
                progress["completed_ids"].append(y["id"])
                completed_set.add(y["id"])

        with open(PROGRESS_FILE, "w") as f:
            json.dump(progress, f, ensure_ascii=False)
        time.sleep(1.0)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(progress["results"], f, ensure_ascii=False, indent=2)

    print(f"\n=== Stage 5 Complete ===")
    print(f"Roles analyzed: {len(progress['results'])}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
