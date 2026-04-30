#!/usr/bin/env python3
"""
Stage 7 parallel worker: processes a slice of yokai.
Each worker handles a range [start_idx, end_idx) and saves to its own output file.

Usage:
    python3 scripts/yokai_stage7_parallel.py --worker-id 0 --start 0 --end 200 --batch-size 10
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
MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 16384

SYSTEM_PROMPT = """あなたは深層心理学・人格心理学・ユング心理学の専門家です。
各妖怪の行動パターン・伝承・文化的役割・存在論的特性に基づいて、多面的な人格・性格構造を分析してください。

分析フレームワーク：

1. Big Five 30サブファセット（各1-100スコア）:
   - Openness: fantasy, aesthetics, feelings, actions, ideas, values
   - Conscientiousness: competence, order, dutifulness, achievement_striving, self_discipline, deliberation
   - Extraversion: warmth, gregariousness, assertiveness, activity, excitement_seeking, positive_emotions
   - Agreeableness: trust, straightforwardness, altruism, compliance, modesty, tender_mindedness
   - Neuroticism: anxiety, angry_hostility, depression, self_consciousness, impulsiveness, vulnerability

2. アーキタイプ（14分類から primary + secondary + shadow を選択）:
   Innocent, Orphan, Hero, Caregiver, Explorer, Rebel, Lover, Creator,
   Jester, Sage, Magician, Ruler, Destroyer, Trickster

3. 防衛機制（2-4個）

4. 認知スタイル: field_dependence, processing, tempo, modality

5. 関係力動: power_orientation, approach_avoidance, differentiation

6. 影の側面: 1文

全て日本語で記述。"""


def get_api_key():
    result = subprocess.run(
        ["security", "find-generic-password", "-s", "ANTHROPIC_API_KEY", "-w"],
        capture_output=True, text=True
    )
    return result.stdout.strip()


def build_batch_prompt(yokai_batch):
    entries = []
    for y in yokai_batch:
        info = f"""ID: {y['id']}
名前: {y['name_ja']} ({y.get('name_en','')})
性格: {y.get('personality','')}
行動パターン: {json.dumps(y.get('behavioral_patterns',[]), ensure_ascii=False)}
相互作用: {json.dumps(y.get('interaction_patterns',[]), ensure_ascii=False)}
道徳的配置: {y.get('moral_alignment','')}
存在論的役割: {json.dumps(y.get('ontological_role',{}), ensure_ascii=False)[:200]}
文化的役割: {y.get('cultural_role','')}"""
        entries.append(info)

    batch_text = "\n---\n".join(entries)
    return f"""以下の{len(yokai_batch)}体の妖怪の深層人格構造を分析してください。

{batch_text}

JSON配列で返してください。サブファセットはスコアのみ：
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
      "core_motivation": "核心的動機",
      "greatest_fear": "最大の恐怖",
      "defense_mechanisms": ["projection", "displacement"],
      "cognitive_style": {{"field_dependence": "independent", "processing": "holistic", "tempo": "impulsive", "modality": "kinesthetic"}},
      "relational_dynamics": {{"power_orientation": "dominant", "approach_avoidance": "ambivalent", "differentiation": "oscillating"}},
      "shadow_aspects": "影の側面"
    }}
  }}
]
```
JSONのみを返してください。"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-id", type=int, required=True)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--batch-size", type=int, default=10)
    args = parser.parse_args()

    output_file = DATA_DIR / f"yokai-stage7-worker{args.worker_id}.json"
    print(f"Worker {args.worker_id}: range [{args.start}, {args.end}), output: {output_file}")

    with open(INPUT_FILE) as f:
        all_yokai = json.load(f)

    worker_yokai = all_yokai[args.start:args.end]
    print(f"Processing {len(worker_yokai)} yokai")

    api_key = get_api_key()
    client = anthropic.Anthropic(api_key=api_key)

    results = []
    batch_size = args.batch_size
    total_batches = (len(worker_yokai) + batch_size - 1) // batch_size

    for batch_idx in range(total_batches):
        start = batch_idx * batch_size
        batch = worker_yokai[start:start + batch_size]
        print(f"  [{batch_idx+1}/{total_batches}] {batch[0]['name_ja']}〜{batch[-1]['name_ja']}")

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

            batch_results = json.loads(text)
            if not isinstance(batch_results, list):
                batch_results = [batch_results]
            results.extend(batch_results)
            print(f"    OK: {len(batch_results)}")

        except json.JSONDecodeError as e:
            print(f"    JSON ERROR: {e}")
            # Mark as empty
            for y in batch:
                results.append({"id": y["id"], "personality_deep": {}})

        except anthropic.RateLimitError:
            print("    Rate limited. Waiting 60s...")
            time.sleep(60)
            # Retry this batch
            try:
                response = client.messages.create(
                    model=MODEL, max_tokens=MAX_TOKENS,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": prompt}],
                )
                text = response.content[0].text.strip()
                if "```json" in text:
                    text = text.split("```json", 1)[1].split("```", 1)[0]
                batch_results = json.loads(text)
                if not isinstance(batch_results, list):
                    batch_results = [batch_results]
                results.extend(batch_results)
            except Exception:
                for y in batch:
                    results.append({"id": y["id"], "personality_deep": {}})

        except anthropic.APIError as e:
            print(f"    API ERROR: {e}")
            for y in batch:
                results.append({"id": y["id"], "personality_deep": {}})

        # Save incrementally
        with open(output_file, "w") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        time.sleep(1.0)

    print(f"Worker {args.worker_id} complete: {len(results)} results")


if __name__ == "__main__":
    main()
