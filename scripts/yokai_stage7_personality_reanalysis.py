#!/usr/bin/env python3
"""
Stage 7: Deep personality/character structure re-analysis.
Enhances personality_deep with:
- Big Five 30 subfacets
- Archetype normalization (14 categories + secondary + shadow)
- defense_mechanisms, cognitive_style, relational_dynamics, shadow_aspects

Uses behavioral data from Stage 4 + ontological roles from Stage 5.

Usage:
    python3 scripts/yokai_stage7_personality_reanalysis.py [--resume] [--batch-size 10]
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
OUTPUT_FILE = DATA_DIR / "yokai-personality-enhanced.json"
PROGRESS_FILE = DATA_DIR / "yokai-stage7-progress.json"

MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 16384


def get_api_key():
    result = subprocess.run(
        ["security", "find-generic-password", "-s", "ANTHROPIC_API_KEY", "-w"],
        capture_output=True, text=True
    )
    return result.stdout.strip()


SYSTEM_PROMPT = """あなたは深層心理学・人格心理学・ユング心理学の専門家です。
各妖怪の行動パターン・伝承・文化的役割・存在論的特性に基づいて、多面的な人格・性格構造を分析してください。

分析フレームワーク：

1. Big Five 30サブファセット（各1-100スコア + 根拠1文）:
   - Openness: fantasy, aesthetics, feelings, actions, ideas, values
   - Conscientiousness: competence, order, dutifulness, achievement_striving, self_discipline, deliberation
   - Extraversion: warmth, gregariousness, assertiveness, activity, excitement_seeking, positive_emotions
   - Agreeableness: trust, straightforwardness, altruism, compliance, modesty, tender_mindedness
   - Neuroticism: anxiety, angry_hostility, depression, self_consciousness, impulsiveness, vulnerability

2. アーキタイプ（14分類から primary + secondary + shadow を選択）:
   Innocent, Orphan, Hero, Caregiver, Explorer, Rebel, Lover, Creator,
   Jester, Sage, Magician, Ruler, Destroyer, Trickster

3. 防衛機制（2-4個）: projection, denial, displacement, sublimation, reaction_formation,
   intellectualization, regression, repression, splitting, idealization, undoing

4. 認知スタイル: field_dependent/independent, holistic/analytic, reflective/impulsive,
   visual/verbal/kinesthetic

5. 関係力動: dominant/submissive, approach/avoidance, enmeshment/differentiation,
   attachment style (secure/anxious/avoidant/disorganized)

6. 影の側面: その妖怪が抑圧・否認している側面（1-2文）

全て日本語で、行動データに基づいた具体的根拠を付けてください。"""


def build_batch_prompt(yokai_batch):
    entries = []
    for y in yokai_batch:
        info = f"""ID: {y['id']}
名前: {y['name_ja']} ({y.get('name_en','')})
性格: {y.get('personality','')}
既存personality_deep: {json.dumps(y.get('personality_deep',{}), ensure_ascii=False)[:300]}
行動パターン: {json.dumps(y.get('behavioral_patterns',[]), ensure_ascii=False)}
相互作用: {json.dumps(y.get('interaction_patterns',[]), ensure_ascii=False)}
道徳的配置: {y.get('moral_alignment','')}
存在論的役割: {json.dumps(y.get('ontological_role',{}), ensure_ascii=False)[:200]}
文化的役割: {y.get('cultural_role','')}"""
        entries.append(info)

    batch_text = "\n---\n".join(entries)
    return f"""以下の{len(yokai_batch)}体の妖怪の深層人格構造を分析してください。

{batch_text}

JSON配列で返してください。サブファセットはスコアのみ（basisは不要）：
```json
[
  {{
    "id": "妖怪ID",
    "personality_deep": {{
      "big_five": {{
        "openness": {{"score": 75, "subfacets": {{"fantasy": 85, "aesthetics": 60, "feelings": 70, "actions": 80, "ideas": 65, "values": 75}}}},
        "conscientiousness": {{"score": 50, "subfacets": {{"competence": 60, "order": 40, "dutifulness": 55, "achievement_striving": 45, "self_discipline": 50, "deliberation": 50}}}},
        "extraversion": {{"score": 60, "subfacets": {{"warmth": 65, "gregariousness": 55, "assertiveness": 70, "activity": 60, "excitement_seeking": 50, "positive_emotions": 65}}}},
        "agreeableness": {{"score": 40, "subfacets": {{"trust": 35, "straightforwardness": 45, "altruism": 50, "compliance": 30, "modesty": 40, "tender_mindedness": 45}}}},
        "neuroticism": {{"score": 55, "subfacets": {{"anxiety": 60, "angry_hostility": 50, "depression": 45, "self_consciousness": 55, "impulsiveness": 65, "vulnerability": 50}}}}
      }},
      "archetype": {{"primary": "Trickster", "secondary": "Explorer", "shadow": "Destroyer", "integration_level": "中程度"}},
      "attachment_style": "disorganized",
      "emotional_range": {{"dominant": "好奇心", "secondary": "恐怖", "suppressed": "悲しみ"}},
      "core_motivation": "核心的動機（1文）",
      "greatest_fear": "最大の恐怖（1文）",
      "defense_mechanisms": ["projection", "displacement"],
      "cognitive_style": {{"field_dependence": "independent", "processing": "holistic", "tempo": "impulsive", "modality": "kinesthetic"}},
      "relational_dynamics": {{"power_orientation": "dominant", "approach_avoidance": "ambivalent", "differentiation": "oscillating"}},
      "shadow_aspects": "影の側面（1文）"
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

    print("=== Stage 7: Personality Re-analysis ===")

    with open(INPUT_FILE) as f:
        all_yokai = json.load(f)
    print(f"Total yokai: {len(all_yokai)}")

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

    batch_size = args.batch_size
    total_batches = (len(remaining) + batch_size - 1) // batch_size

    for batch_idx in range(total_batches):
        start = batch_idx * batch_size
        batch = remaining[start:start + batch_size]
        done_total = len(completed_set) + start + len(batch)
        print(f"\n[Batch {batch_idx+1}/{total_batches}] ({done_total}/{len(all_yokai)})")

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
                progress["results"].append(r)
                progress["completed_ids"].append(r.get("id", ""))
                completed_set.add(r.get("id", ""))

            print(f"  OK: {len(results)} personalities analyzed")

        except json.JSONDecodeError as e:
            print(f"  JSON ERROR: {e}")
            raw_path = DATA_DIR / f"yokai-stage7-raw-batch{batch_idx+1}.txt"
            with open(raw_path, "w") as f:
                f.write(response.content[0].text)
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

    print(f"\n=== Stage 7 Complete ===")
    print(f"Personalities analyzed: {len(progress['results'])}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
