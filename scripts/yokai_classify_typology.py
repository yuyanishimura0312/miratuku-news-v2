#!/usr/bin/env python3
"""Classify each yokai into GTA typology using Haiku."""
import json
import subprocess
import time
from pathlib import Path

import anthropic

DATA_DIR = Path(__file__).parent.parent / "data"


def get_api_key():
    result = subprocess.run(
        ["security", "find-generic-password", "-s", "ANTHROPIC_API_KEY", "-w"],
        capture_output=True, text=True
    )
    return result.stdout.strip()


def main():
    with open(DATA_DIR / "yokai-data.json") as f:
        main_data = json.load(f)

    client = anthropic.Anthropic(api_key=get_api_key())
    results = {}
    batch_size = 50

    for bi in range(0, len(main_data), batch_size):
        batch = main_data[bi:bi + batch_size]
        items = []
        for y in batch:
            role = y.get("ontological_role", {})
            arch = y.get("personality_deep", {}).get("archetype", {})
            items.append(
                f'{y["id"]}: role_type={role.get("role_type","")}, '
                f'arch={arch.get("primary","")}/{arch.get("secondary","")}, '
                f'moral={y.get("moral_alignment","")}'
            )

        prompt = (
            f"以下の{len(items)}体の妖怪を3類型に分類してください。\n\n"
            "類型の定義：\n"
            "- 秩序維持型: 社会秩序・道徳・自然法則を守る機能が主\n"
            "- 変容促進型: 変化・混乱・創造・反秩序を促す機能が主\n"
            "- 媒介統合型: 異なる世界・存在・領域を繋ぐ媒介機能が主\n\n"
            + "\n".join(items)
            + '\n\nJSON辞書で返してください：{"id": "類型名", ...}\nJSONのみ。'
        )

        try:
            resp = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
            )
            text = resp.content[0].text.strip()
            if "```json" in text:
                text = text.split("```json", 1)[1].split("```", 1)[0]
            elif "```" in text:
                text = text.split("```", 1)[1].split("```", 1)[0]
            batch_results = json.loads(text)
            results.update(batch_results)
            print(f"Batch {bi // batch_size + 1}: {len(batch_results)} classified")
        except Exception as e:
            print(f"Batch {bi // batch_size + 1}: ERROR {e}")
        time.sleep(0.5)

    # Apply
    from collections import Counter
    for y in main_data:
        y["gta_core_category"] = results.get(y["id"], "媒介統合型")

    with open(DATA_DIR / "yokai-data.json", "w") as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2)

    dist = Counter(y["gta_core_category"] for y in main_data)
    for t, c in dist.most_common():
        print(f"  {t}: {c} ({100 * c / len(main_data):.1f}%)")


if __name__ == "__main__":
    main()
