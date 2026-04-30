#!/usr/bin/env python3
"""
Stage 2: Synthesize ontological meaning of yokai for humanity.
Integrates boundary theory, marebito theory, ecological ontology.
Uses Stage 1 definition framework as input.

Usage:
    python3 scripts/yokai_stage2_ontological_framework.py
"""

import json
import subprocess
from pathlib import Path

import anthropic

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
INPUT_FILE = DATA_DIR / "yokai-definition-framework.json"
OUTPUT_FILE = DATA_DIR / "yokai-ontological-framework.json"

MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 8192


def get_api_key():
    result = subprocess.run(
        ["security", "find-generic-password", "-s", "ANTHROPIC_API_KEY", "-w"],
        capture_output=True, text=True
    )
    return result.stdout.strip()


def main():
    print("=== Stage 2: Ontological Framework ===")

    with open(INPUT_FILE) as f:
        definition = json.load(f)

    api_key = get_api_key()
    client = anthropic.Anthropic(api_key=api_key)

    system = """あなたは比較存在論・文化人類学・宗教学・生態人類学の専門家です。
Stage 1で構築した妖怪の定義フレームワークを踏まえて、「妖怪とは人類にとってどのような存在か」
という問いに対する存在論的な統合的回答を構築してください。

以下の学術的視点を必ず統合してください：

1. 境界論（Boundary Theory）
   - 妖怪は何と何の境界に存在するか（自然/文化、生/死、人間/非人間、聖/俗）
   - メアリー・ダグラス『汚穢と禁忌』の境界侵犯論との接続
   - ヴィクター・ターナー『儀礼の過程』のリミナリティ理論

2. マレビト論と来訪者としての妖怪
   - 折口信夫のマレビト論の現代的再解釈
   - 妖怪が「外部からの訪問者」である場合と「内部に潜む者」である場合の区別
   - 歓待の論理（デリダのホスピタリティ論）との接続

3. 生態学的存在論
   - 妖怪は生態系のどの位置にいるか
   - アニマ・ムンディ（世界霊魂）の伝統との関係
   - 妖怪が環境倫理に果たす役割

4. 心理的・現象学的次元
   - ユングのアーキタイプ理論（影、アニマ/アニムス、トリックスター）
   - ハイデガーの「不安」概念と妖怪の出現条件
   - 妖怪体験の現象学（知覚・情動・身体感覚）

5. 社会的機能
   - デュルケームの集合的表象としての妖怪
   - 社会統制装置としての妖怪
   - 抵抗と転覆の装置としての妖怪

6. 時間論
   - 妖怪と季節・暦・時刻の関係
   - 「逢魔が時」の時間論的意味
   - 近代化・技術進歩と妖怪の消長

全て日本語で記述し、学術的正確性を保ちつつ実用的な分析フレームワークとしてください。"""

    user_msg = f"""以下はStage 1で構築した定義フレームワークです：

{json.dumps(definition, ensure_ascii=False, indent=2)}

このフレームワークを踏まえて、以下のJSON構造で妖怪の存在論的意味をまとめてください：

```json
{{
  "ontological_meaning": {{
    "boundary_theory": {{
      "yokai_as_boundary_beings": "妖怪が境界存在であることの学術的説明（3-5文）",
      "boundary_types": [
        {{
          "boundary": "境界の名前",
          "description_ja": "この境界での妖怪の役割",
          "exemplary_yokai_types": ["該当する妖怪タイプ"]
        }}
      ],
      "liminality_analysis": "ターナーのリミナリティ理論による分析",
      "douglas_pollution": "ダグラスの汚穢論による分析"
    }},
    "marebito_and_hospitality": {{
      "orikuchi_reinterpretation": "マレビト論の現代的再解釈",
      "visitor_vs_insider": "外来者としての妖怪と内部者としての妖怪の分析",
      "hospitality_logic": "歓待の論理と妖怪の関係"
    }},
    "ecological_ontology": {{
      "ecological_position": "妖怪の生態学的位置づけ",
      "environmental_ethics": "環境倫理における妖怪の役割",
      "anima_mundi": "世界霊魂との関係"
    }},
    "psychological_phenomenology": {{
      "jungian_archetypes": "ユング心理学における妖怪の位置",
      "heideggerian_anxiety": "ハイデガーの不安概念との接続",
      "phenomenology_of_encounter": "妖怪遭遇の現象学的分析"
    }},
    "social_functions": {{
      "collective_representation": "集合的表象としての妖怪",
      "social_control": "社会統制装置としての機能",
      "resistance_subversion": "抵抗・転覆の装置としての機能"
    }},
    "temporality": {{
      "seasonal_temporal": "妖怪と時間・季節の関係",
      "omagatoki": "逢魔が時の時間論",
      "modernity_tension": "近代化と妖怪の消長"
    }}
  }},
  "integrated_thesis": {{
    "thesis_statement_ja": "妖怪が人類にとって何であるかの統合的テーゼ（200-400字の散文）",
    "ontological_roles": [
      {{
        "role": "役割名",
        "description_ja": "説明（2-3文）",
        "database_field_mapping": "データベースのontological_roleフィールドでの対応値"
      }}
    ],
    "universal_vs_particular": "妖怪の普遍性と日本文化の特殊性の分析"
  }}
}}
```

各フィールドを学術的に充実させ、全て日本語で記述してください。"""

    print("Generating ontological framework...")
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": user_msg}]
    )

    text = response.content[0].text.strip()
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0]
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0]

    try:
        framework = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        raw_path = DATA_DIR / "yokai-stage2-raw.txt"
        with open(raw_path, "w") as f:
            f.write(response.content[0].text)
        print(f"Raw response saved to {raw_path}")
        return

    with open(OUTPUT_FILE, "w") as f:
        json.dump(framework, f, ensure_ascii=False, indent=2)

    print(f"Framework saved to {OUTPUT_FILE}")
    print(f"Top-level keys: {list(framework.keys())}")

    # Validate
    required = ["ontological_meaning", "integrated_thesis"]
    missing = [k for k in required if k not in framework]
    if missing:
        print(f"WARNING: Missing keys: {missing}")
    else:
        print("All required sections present.")
        if "ontological_roles" in framework.get("integrated_thesis", {}):
            roles = framework["integrated_thesis"]["ontological_roles"]
            print(f"Ontological roles defined: {len(roles)}")
            for r in roles:
                print(f"  - {r['role']}")


if __name__ == "__main__":
    main()
