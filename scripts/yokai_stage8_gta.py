#!/usr/bin/env python3
"""
Stage 8: Grounded Theory Analysis (GTA) of yokai behavioral/personality data.
Three phases: Open coding → Axial coding → Selective coding.

Usage:
    python3 scripts/yokai_stage8_gta.py --phase open [--resume] [--batch-size 15]
    python3 scripts/yokai_stage8_gta.py --phase axial
    python3 scripts/yokai_stage8_gta.py --phase selective
    python3 scripts/yokai_stage8_gta.py --phase all
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
OPEN_OUTPUT = DATA_DIR / "yokai-gta-open-codes.json"
AXIAL_OUTPUT = DATA_DIR / "yokai-gta-axial-codes.json"
SELECTIVE_OUTPUT = DATA_DIR / "yokai-gta-results.json"
PROGRESS_FILE = DATA_DIR / "yokai-stage8-progress.json"

MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 16384


def get_api_key():
    result = subprocess.run(
        ["security", "find-generic-password", "-s", "ANTHROPIC_API_KEY", "-w"],
        capture_output=True, text=True
    )
    return result.stdout.strip()


# ── Phase A: Open Coding ──

OPEN_SYSTEM = """あなたはグラウンデッド・セオリー・アプローチ（GTA）の専門家です。
与えられた妖怪の行動様式・言説・人格特性データから、オープンコーディングを行ってください。

オープンコーディングとは：
- データを1行ずつ読み、概念ラベルを付与する
- 同様の概念をカテゴリにまとめる
- 各コードにはプロパティ（属性）とディメンション（次元）を記述する

コーディングの観点：
1. 行動様式のパターン（何をするか）
2. 言説のパターン（何を言うか・どう語るか）
3. 関係性のパターン（人間や他の存在とどう関わるか）
4. 存在論的パターン（何者であるか・どう存在するか）
5. 変容のパターン（どう変化するか）

各妖怪に3-8個のコードを付与してください。"""


def open_coding_prompt(yokai_batch):
    entries = []
    for y in yokai_batch:
        info = f"""ID: {y['id']}
名前: {y['name_ja']}
行動パターン: {json.dumps(y.get('behavioral_patterns',[]), ensure_ascii=False)}
言説例: {json.dumps(y.get('speech_examples',[]), ensure_ascii=False)}
相互作用: {json.dumps(y.get('interaction_patterns',[]), ensure_ascii=False)}
儀礼的行動: {json.dumps(y.get('ritual_behaviors',[]), ensure_ascii=False)}
人格深層: archetype={y.get('personality_deep',{}).get('archetype',{})}, core_motivation={y.get('personality_deep',{}).get('core_motivation','')}
存在論的役割: {json.dumps(y.get('ontological_role',{}), ensure_ascii=False)[:200]}"""
        entries.append(info)

    batch_text = "\n---\n".join(entries)
    return f"""以下の{len(yokai_batch)}体の妖怪データにオープンコーディングを行ってください。

{batch_text}

JSON配列で返してください：
```json
[
  {{
    "id": "妖怪ID",
    "open_codes": [
      {{
        "code": "コード名（短い概念ラベル）",
        "category": "上位カテゴリ名",
        "property": "このコードの属性",
        "dimension": "この属性の次元（例：強い-弱い）",
        "evidence": "根拠となるデータ（1文）"
      }}
    ]
  }}
]
```
JSONのみを返してください。"""


# ── Phase B: Axial Coding ──

AXIAL_SYSTEM = """あなたはGTA（グラウンデッド・セオリー）の専門家です。
オープンコーディングの結果から軸コーディングを行ってください。

軸コーディングとは：
- オープンコードをカテゴリ間の関係性に基づいて再編成する
- パラダイムモデル（条件→現象→文脈→介在条件→作用/相互作用→帰結）を適用する
- カテゴリの階層構造と関係パターンを明らかにする

目標：10-20個のカテゴリに集約し、各カテゴリのサブカテゴリ、プロパティ、
ディメンション、関係性を明確にする。"""


def axial_coding_prompt(open_codes_summary):
    return f"""以下は1,010体の妖怪のオープンコーディング結果の統計サマリーです：

{open_codes_summary}

これを軸コーディングで分析し、以下のJSON構造で返してください：

```json
{{
  "axial_categories": [
    {{
      "category": "カテゴリ名",
      "description": "カテゴリの説明（2-3文）",
      "subcategories": ["サブカテゴリ1", "サブカテゴリ2"],
      "properties": [
        {{"name": "属性名", "dimension": "次元（例：高い-低い）"}}
      ],
      "paradigm": {{
        "conditions": "このカテゴリが生じる条件",
        "phenomenon": "中心現象",
        "context": "文脈",
        "intervening_conditions": "介在条件",
        "strategies": "作用/相互作用戦略",
        "consequences": "帰結"
      }},
      "yokai_count": 0,
      "representative_yokai": ["代表的な妖怪名"]
    }}
  ],
  "category_relationships": [
    {{
      "from": "カテゴリ名",
      "to": "カテゴリ名",
      "relationship_type": "因果|条件|相関|矛盾|包含",
      "description": "関係の説明"
    }}
  ]
}}
```
JSONのみを返してください。"""


# ── Phase C: Selective Coding ──

SELECTIVE_SYSTEM = """あなたはGTA（グラウンデッド・セオリー）の専門家です。
軸コーディングの結果から選択コーディングを行い、コアカテゴリを発見してください。

選択コーディングとは：
- 全てのカテゴリを統合するコアカテゴリを特定する
- コアカテゴリと他カテゴリの体系的関係を記述する
- ストーリーライン（理論的物語）を構築する
- 理論的飽和を評価する

目標：妖怪の行動様式と人格構造から浮かび上がる「理論」を生成する。"""


def selective_coding_prompt(axial_result):
    return f"""以下は妖怪データの軸コーディング結果です：

{json.dumps(axial_result, ensure_ascii=False, indent=2)}

選択コーディングを行い、以下のJSON構造で返してください：

```json
{{
  "core_category": {{
    "name": "コアカテゴリ名",
    "definition": "定義（2-3文）",
    "theoretical_narrative": "理論的物語（ストーリーライン）（400-600字の散文）"
  }},
  "theoretical_framework": {{
    "propositions": [
      {{
        "proposition": "理論的命題",
        "supporting_categories": ["支持するカテゴリ名"],
        "evidence_strength": "強い|中程度|弱い"
      }}
    ],
    "boundary_conditions": "理論の適用範囲と限界",
    "theoretical_saturation": "理論的飽和度の評価（1-2文）"
  }},
  "yokai_typology": [
    {{
      "type_name": "妖怪類型名",
      "description": "説明（2-3文）",
      "core_category_relation": "コアカテゴリとの関係",
      "representative_yokai": ["代表的な妖怪名"],
      "estimated_count": 0
    }}
  ],
  "implications": {{
    "for_anthropology": "文化人類学への示唆",
    "for_psychology": "心理学への示唆",
    "for_ecology": "生態学への示唆"
  }}
}}
```
JSONのみを返してください。"""


def run_open_coding(client, all_yokai, args):
    """Phase A: Open coding."""
    print("\n=== Phase A: Open Coding ===")

    if args.resume and PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            progress = json.load(f)
    else:
        progress = {"completed_ids": [], "results": []}

    completed_set = set(progress["completed_ids"])
    remaining = [y for y in all_yokai if y["id"] not in completed_set]
    print(f"Remaining: {len(remaining)}")

    if not remaining:
        with open(OPEN_OUTPUT, "w") as f:
            json.dump(progress["results"], f, ensure_ascii=False, indent=2)
        return progress["results"]

    batch_size = args.batch_size
    total_batches = (len(remaining) + batch_size - 1) // batch_size

    for batch_idx in range(total_batches):
        start = batch_idx * batch_size
        batch = remaining[start:start + batch_size]
        done = len(completed_set) + start + len(batch)
        print(f"[Open {batch_idx+1}/{total_batches}] ({done}/{len(all_yokai)})")

        try:
            prompt = open_coding_prompt(batch)
            response = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=OPEN_SYSTEM,
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

            print(f"  OK: {len(results)} coded")

        except json.JSONDecodeError:
            print(f"  JSON ERROR")
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

    with open(OPEN_OUTPUT, "w") as f:
        json.dump(progress["results"], f, ensure_ascii=False, indent=2)

    print(f"Open codes: {len(progress['results'])} yokai coded")
    return progress["results"]


def summarize_open_codes(open_codes):
    """Summarize open codes for axial coding input."""
    from collections import Counter
    category_counts = Counter()
    code_counts = Counter()
    all_codes = []

    for entry in open_codes:
        for code in entry.get("open_codes", []):
            cat = code.get("category", "unknown")
            cn = code.get("code", "unknown")
            category_counts[cat] += 1
            code_counts[cn] += 1
            all_codes.append(code)

    summary_parts = [
        f"総妖怪数: {len(open_codes)}",
        f"総コード数: {len(all_codes)}",
        f"\nカテゴリ別頻度 (上位30):"
    ]
    for cat, cnt in category_counts.most_common(30):
        summary_parts.append(f"  {cat}: {cnt}")

    summary_parts.append(f"\nコード別頻度 (上位50):")
    for code, cnt in code_counts.most_common(50):
        summary_parts.append(f"  {code}: {cnt}")

    # Sample codes per category
    summary_parts.append(f"\n各カテゴリのコード例:")
    cat_examples = {}
    for code in all_codes:
        cat = code.get("category", "unknown")
        if cat not in cat_examples:
            cat_examples[cat] = []
        if len(cat_examples[cat]) < 3:
            cat_examples[cat].append(code)
    for cat, examples in list(cat_examples.items())[:20]:
        summary_parts.append(f"\n  [{cat}]")
        for ex in examples:
            summary_parts.append(f"    - {ex.get('code','')}: {ex.get('property','')} ({ex.get('dimension','')})")

    return "\n".join(summary_parts)


def run_axial_coding(client, open_codes):
    """Phase B: Axial coding."""
    print("\n=== Phase B: Axial Coding ===")

    summary = summarize_open_codes(open_codes)
    print(f"Summary length: {len(summary)} chars")

    # May need multiple calls for large summaries
    # Truncate if too long
    if len(summary) > 12000:
        summary = summary[:12000] + "\n...(truncated)"

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=AXIAL_SYSTEM,
        messages=[{"role": "user", "content": axial_coding_prompt(summary)}],
    )

    text = response.content[0].text.strip()
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0]
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0]

    axial = json.loads(text)
    with open(AXIAL_OUTPUT, "w") as f:
        json.dump(axial, f, ensure_ascii=False, indent=2)

    cats = axial.get("axial_categories", [])
    print(f"Axial categories: {len(cats)}")
    for c in cats:
        print(f"  - {c['category']}")

    return axial


def run_selective_coding(client, axial_result):
    """Phase C: Selective coding."""
    print("\n=== Phase C: Selective Coding ===")

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SELECTIVE_SYSTEM,
        messages=[{"role": "user", "content": selective_coding_prompt(axial_result)}],
    )

    text = response.content[0].text.strip()
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0]
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0]

    selective = json.loads(text)
    with open(SELECTIVE_OUTPUT, "w") as f:
        json.dump(selective, f, ensure_ascii=False, indent=2)

    core = selective.get("core_category", {})
    print(f"Core category: {core.get('name', '?')}")
    types = selective.get("yokai_typology", [])
    print(f"Typology: {len(types)} types")
    for t in types:
        print(f"  - {t.get('type_name', '?')}")

    return selective


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["open", "axial", "selective", "all"], required=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--batch-size", type=int, default=15)
    args = parser.parse_args()

    with open(INPUT_FILE) as f:
        all_yokai = json.load(f)
    print(f"Total yokai: {len(all_yokai)}")

    api_key = get_api_key()
    client = anthropic.Anthropic(api_key=api_key)

    if args.phase in ("open", "all"):
        open_codes = run_open_coding(client, all_yokai, args)
    else:
        with open(OPEN_OUTPUT) as f:
            open_codes = json.load(f)

    if args.phase in ("axial", "all"):
        axial = run_axial_coding(client, open_codes)
    elif args.phase == "selective":
        with open(AXIAL_OUTPUT) as f:
            axial = json.load(f)

    if args.phase in ("selective", "all"):
        selective = run_selective_coding(client, axial)

    print("\n=== Stage 8 Complete ===")


if __name__ == "__main__":
    main()
