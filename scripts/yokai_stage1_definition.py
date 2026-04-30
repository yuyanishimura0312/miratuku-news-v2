#!/usr/bin/env python3
"""
Stage 1: Research yokai definition framework.
Core: Philippe Descola's ontological classification.
Integrates Japanese folkloristics, multispecies ethnography, and comparative ontology.

Usage:
    python3 scripts/yokai_stage1_definition.py
"""

import json
import subprocess
from pathlib import Path

import anthropic

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_FILE = DATA_DIR / "yokai-definition-framework.json"

MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 8192


def get_api_key():
    result = subprocess.run(
        ["security", "find-generic-password", "-s", "ANTHROPIC_API_KEY", "-w"],
        capture_output=True, text=True
    )
    return result.stdout.strip()


SYSTEM_PROMPT = """あなたは比較存在論・文化人類学・民俗学の専門家です。
以下の学術的知識を統合して、「妖怪」の定義フレームワークを構築してください。

核となる理論的基盤:
1. フィリップ・デスコラ (Philippe Descola) — 『自然と文化を超えて』(Beyond Nature and Culture, 2013)
   - 4つの存在論的モード: アニミズム、トーテミズム、アナロジズム、ナチュラリズム
   - interiority（内面性）とphysicality（身体性）の2軸による分類
   - 妖怪はこの4分類のどこに位置づけられるか

2. エドゥアルド・ヴィヴェイロス・デ・カストロ (Eduardo Viveiros de Castro) — 多自然主義とパースペクティヴィズム
   - 同一の精神、異なる身体という存在論
   - 妖怪の「見え方の多層性」への接続

3. ティム・インゴルド (Tim Ingold) — メッシュワーク理論
   - 生物と環境の不可分性
   - 妖怪は「生命の線の結び目」として理解できるか

4. エドゥアルド・コーン (Eduardo Kohn) — 記号過程と「森は考える」
   - 人間を超えた存在論的主体性
   - 妖怪は非人間的記号過程の担い手か

5. 日本の民俗学的伝統
   - 柳田国男: 妖怪の分類体系、一つ目小僧考、妖怪名彙
   - 小松和彦: 妖怪学の体系化、異人論
   - 折口信夫: マレビト論（来訪神としての妖怪）
   - 水木しげる: 妖怪の図像学的整理
   - 現代の妖怪研究（多種民族誌的アプローチ）

6. ヤーコプ・フォン・ユクスキュル (Jakob von Uexküll) — 環世界 (Umwelt) 理論
   - 各存在は独自の知覚世界を持つ
   - 妖怪の環世界は何を知覚しているか

回答は必ず以下のJSON構造に従ってください。全て日本語で記述してください。"""

USER_PROMPT = """妖怪の定義フレームワークを以下のJSON構造で生成してください。
学術的に正確かつ、実際のデータベース（1,010体の妖怪）に適用可能な実用的フレームワークにしてください。

```json
{
  "framework_version": "1.0",
  "core_ontology": {
    "descola_four_modes": {
      "animism": {
        "definition_ja": "内面性は共有するが身体性は異なる。精霊・動物・植物が人間と同じ魂を持つとみなす。",
        "yokai_relevance": "アニミズム的妖怪がどのように位置づけられるか",
        "diagnostic_criteria": ["この分類に該当する妖怪の特徴リスト"],
        "exemplary_yokai": ["代表的な妖怪のID"]
      },
      "totemism": { "同上の構造" },
      "analogism": { "同上の構造" },
      "naturalism": { "同上の構造" }
    },
    "interiority_physicality_axes": {
      "description_ja": "デスコラの2軸による詳細な説明",
      "yokai_application": "妖怪データベースでの interiority_similarity / physicality_similarity スコアの解釈指針"
    },
    "hybrid_ontology": {
      "description_ja": "単一分類に収まらない妖怪の存在論的位置づけ",
      "criteria": "ハイブリッド分類の判定基準"
    }
  },
  "japanese_folkloristics": {
    "yanagita_kunio": {
      "yokai_definition": "柳田国男による妖怪の定義と分類体系",
      "key_concepts": ["重要概念のリスト"],
      "classification_system": "柳田の分類体系の説明"
    },
    "komatsu_kazuhiko": {
      "yokai_definition": "小松和彦による妖怪学の定義",
      "key_concepts": [],
      "ijin_theory": "異人論と妖怪の関係"
    },
    "orikuchi_shinobu": {
      "marebito_theory": "折口信夫のマレビト論",
      "yokai_as_visitor": "来訪神としての妖怪の位置づけ"
    },
    "contemporary_scholars": [
      {"name": "研究者名", "contribution": "貢献内容"}
    ]
  },
  "comparative_frameworks": {
    "viveiros_de_castro_perspectivism": {
      "theory_ja": "パースペクティヴィズムの説明",
      "yokai_application": "妖怪への適用"
    },
    "ingold_meshwork": {
      "theory_ja": "メッシュワーク理論の説明",
      "yokai_application": "妖怪への適用"
    },
    "kohn_semiosis": {
      "theory_ja": "森の思考の説明",
      "yokai_application": "妖怪への適用"
    },
    "uexkull_umwelt": {
      "theory_ja": "環世界理論の説明",
      "yokai_application": "妖怪の環世界への適用"
    }
  },
  "multispecies_ethnography": {
    "definition_ja": "多種民族誌の説明",
    "yokai_as_multispecies_agents": "妖怪を多種民族誌的に捉える視点",
    "key_scholars": []
  },
  "synthesis": {
    "working_definition_ja": "上記全てを統合した妖怪の作業的定義（200-300字の散文）",
    "ontological_dimensions": [
      {
        "dimension": "次元名",
        "description_ja": "説明",
        "measurement": "データベースでの測定方法"
      }
    ],
    "classification_axes": [
      {
        "axis": "分類軸名",
        "poles": ["極1", "極2"],
        "description_ja": "説明"
      }
    ],
    "yokai_unique_characteristics": [
      "妖怪が他の超自然的存在と異なる固有の特徴"
    ]
  }
}
```

全フィールドを学術的に充実させてください。各フィールドは1-3文の散文で記述してください。"""


def main():
    print("=== Stage 1: Yokai Definition Framework ===")

    api_key = get_api_key()
    if not api_key:
        print("ERROR: Could not retrieve API key")
        return

    client = anthropic.Anthropic(api_key=api_key)

    print("Generating definition framework...")
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": USER_PROMPT}]
    )

    text = response.content[0].text.strip()

    # Extract JSON from response
    if "```json" in text:
        text = text.split("```json", 1)[1]
        text = text.split("```", 1)[0]
    elif "```" in text:
        text = text.split("```", 1)[1]
        text = text.split("```", 1)[0]

    try:
        framework = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        print(f"Raw response saved to {DATA_DIR / 'yokai-stage1-raw.txt'}")
        with open(DATA_DIR / "yokai-stage1-raw.txt", "w") as f:
            f.write(response.content[0].text)
        return

    # Save framework
    with open(OUTPUT_FILE, "w") as f:
        json.dump(framework, f, ensure_ascii=False, indent=2)

    print(f"Framework saved to {OUTPUT_FILE}")
    print(f"Top-level keys: {list(framework.keys())}")

    # Validate structure
    required_keys = ["core_ontology", "japanese_folkloristics", "comparative_frameworks", "synthesis"]
    missing = [k for k in required_keys if k not in framework]
    if missing:
        print(f"WARNING: Missing keys: {missing}")
    else:
        print("All required sections present.")


if __name__ == "__main__":
    main()
