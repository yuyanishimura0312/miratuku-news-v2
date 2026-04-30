#!/usr/bin/env python3
"""
Stage 8 Phase A parallel worker: Open coding for a slice of yokai.

Usage:
    python3 scripts/yokai_stage8_parallel_open.py --worker-id 0 --start 0 --end 100 --batch-size 15
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

SYSTEM = """あなたはグラウンデッド・セオリー・アプローチ（GTA）の専門家です。
与えられた妖怪の行動様式・言説・人格特性データから、オープンコーディングを行ってください。

コーディングの観点：
1. 行動様式のパターン（何をするか）
2. 言説のパターン（何を言うか・どう語るか）
3. 関係性のパターン（人間や他の存在とどう関わるか）
4. 存在論的パターン（何者であるか・どう存在するか）
5. 変容のパターン（どう変化するか）

各妖怪に3-8個のコードを付与してください。"""


def get_api_key():
    result = subprocess.run(
        ["security", "find-generic-password", "-s", "ANTHROPIC_API_KEY", "-w"],
        capture_output=True, text=True
    )
    return result.stdout.strip()


def build_prompt(yokai_batch):
    entries = []
    for y in yokai_batch:
        info = f"""ID: {y['id']}
名前: {y['name_ja']}
行動: {json.dumps(y.get('behavioral_patterns',[]), ensure_ascii=False)[:200]}
言説: {json.dumps(y.get('speech_examples',[]), ensure_ascii=False)[:100]}
相互作用: {json.dumps(y.get('interaction_patterns',[]), ensure_ascii=False)[:200]}
アーキタイプ: {y.get('personality_deep',{}).get('archetype',{})}
動機: {y.get('personality_deep',{}).get('core_motivation','')}
存在論的役割: {json.dumps(y.get('ontological_role',{}), ensure_ascii=False)[:150]}"""
        entries.append(info)

    return f"""以下の{len(yokai_batch)}体にオープンコーディングを行ってください。

{"---".join(entries)}

JSON配列で返してください：
```json
[{{"id":"ID","open_codes":[{{"code":"コード名","category":"カテゴリ","property":"属性","dimension":"次元"}}]}}]
```
JSONのみ。"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-id", type=int, required=True)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--batch-size", type=int, default=15)
    args = parser.parse_args()

    output = DATA_DIR / f"yokai-gta-open-worker{args.worker_id}.json"
    print(f"GTA Open Worker {args.worker_id}: [{args.start},{args.end})")

    with open(INPUT_FILE) as f:
        all_yokai = json.load(f)
    worker_yokai = all_yokai[args.start:args.end]

    api_key = get_api_key()
    client = anthropic.Anthropic(api_key=api_key)

    results = []
    bs = args.batch_size
    total = (len(worker_yokai) + bs - 1) // bs

    for bi in range(total):
        batch = worker_yokai[bi*bs:(bi+1)*bs]
        print(f"  [{bi+1}/{total}]")
        try:
            resp = client.messages.create(
                model=MODEL, max_tokens=MAX_TOKENS, system=SYSTEM,
                messages=[{"role": "user", "content": build_prompt(batch)}]
            )
            text = resp.content[0].text.strip()
            if "```json" in text:
                text = text.split("```json",1)[1].split("```",1)[0]
            elif "```" in text:
                text = text.split("```",1)[1].split("```",1)[0]
            batch_r = json.loads(text)
            if not isinstance(batch_r, list): batch_r = [batch_r]
            results.extend(batch_r)
        except (json.JSONDecodeError, anthropic.APIError) as e:
            print(f"    ERROR: {e}")
            for y in batch:
                results.append({"id": y["id"], "open_codes": []})
        except anthropic.RateLimitError:
            print("    Rate limit, waiting 60s...")
            time.sleep(60)
            continue

        with open(output, "w") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        time.sleep(1.0)

    print(f"Worker {args.worker_id}: {len(results)} coded")

if __name__ == "__main__":
    main()
