#!/usr/bin/env python3
"""既存ドラフトを延長するためのCodexバッチを生成する。"""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "_build"
DRAFTS = ROOT / "_drafts"
EPISODES = BUILD / "episodes.json"
BRIEF = BUILD / "expand_brief.md"
SAMPLE = DRAFTS / "ep002.md"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--start", type=int, default=4)
    p.add_argument("--end", type=int, default=100)
    p.add_argument("--per-batch", type=int, default=10)
    p.add_argument("--out-sh", type=Path, default=BUILD / "run_expand_batch.sh")
    args = p.parse_args()

    episodes = json.loads(EPISODES.read_text(encoding="utf-8"))
    brief = BRIEF.read_text(encoding="utf-8")
    sample = SAMPLE.read_text(encoding="utf-8")

    target_eps = [e for e in episodes if args.start <= e["num"] <= args.end]

    batches = []
    for i in range(0, len(target_eps), args.per_batch):
        batches.append(target_eps[i : i + args.per_batch])

    sh_lines = ["#!/bin/bash", "set +e", f"OUT={BUILD}", ""]

    for bi, batch in enumerate(batches, 1):
        first_n = batch[0]["num"]
        last_n = batch[-1]["num"]
        prompt_path = BUILD / f"expand_b{bi:02d}_ep{first_n:03d}-{last_n:03d}.md"

        # Build per-episode existing draft + meta
        ep_lines = []
        for ep in batch:
            existing_draft = DRAFTS / f"ep{ep['num']:03d}.md"
            existing_text = existing_draft.read_text(encoding="utf-8") if existing_draft.exists() else ""

            meta_lines = [f"### 第{ep['num']}話「{ep['title']}」"]
            for k_label in [
                ("subtitle", "サブタイトル"),
                ("en_title", "英訳"),
                ("starting_question", "起点"),
                ("humanities", "人文知"),
                ("academic_field", "学術"),
                ("lead", "リード"),
                ("body_core", "本文の核"),
                ("deeper", "DEEPER素材"),
                ("signal", "SIGNAL素材"),
                ("next_question", "次の問い"),
            ]:
                k, label = k_label
                if ep.get(k):
                    meta_lines.append(f"- {label}: {ep[k]}")

            ep_lines.extend(meta_lines)
            ep_lines.append("")
            ep_lines.append(f"#### 既存ドラフト（短い版・これを下敷きに延長してください）：")
            ep_lines.append("")
            ep_lines.append("```")
            ep_lines.append(existing_text.strip() if existing_text else "（既存なし）")
            ep_lines.append("```")
            ep_lines.append("")
            ep_lines.append("---")
            ep_lines.append("")

        prompt = f"""{brief}

---

## 今回あなたが担当する範囲
**第{first_n}話〜第{last_n}話の合計{len(batch)}話**

各話には、企画書のメタ情報と、既存の短いドラフトが付いている。**既存ドラフトを下敷きに、字数指定（本文1,500-1,800字、DEEPER 400-600字、SIGNAL 500-700字）まで延長してください。**

既存ドラフトは品質的に「骨子のみ」の状態である。これを：
- 冒頭は暮らしの場面から入るように書き直す
- 中盤は研究者名・著作名・年代を厚く
- 後半は読者の言葉への翻訳を加える
- DEEPERは学術系譜と日本語圏の蓄積を加える
- SIGNALは国際 / 国内 / 響きあいの3段落構成にする

---

{chr(10).join(ep_lines)}

---

## サンプル（基準品質・ep002 既執筆済み）
```
{sample}
```

---

## 出力指示
{len(batch)}話すべてを、`=== EPNNN ===` マーカーで区切って出力してください。
途中で省略せず、必ず全話書き切ること。
**Web検索は使わない**。
"""

        prompt_path.write_text(prompt, encoding="utf-8")

        out_log = BUILD / f"expand_b{bi:02d}_log.txt"
        done_marker = BUILD / f"expand_b{bi:02d}_done"
        sh_lines.append(
            f'codex exec --sandbox workspace-write --skip-git-repo-check - < "{prompt_path}" > "{out_log}" 2>&1 && '
            f'touch "{done_marker}" &'
        )
        sh_lines.append(f'echo "[launched] expand_b{bi:02d} ep{first_n:03d}-{last_n:03d}"')

    sh_lines.append("")
    sh_lines.append("wait")
    sh_lines.append('echo "[ALL EXPAND BATCHES DONE]"')

    args.out_sh.write_text("\n".join(sh_lines), encoding="utf-8")
    args.out_sh.chmod(0o755)
    print(f"Generated: {args.out_sh}")
    for bi, batch in enumerate(batches, 1):
        print(f"  expand_b{bi:02d}: ep{batch[0]['num']:03d}-{batch[-1]['num']:03d} ({len(batch)} eps)")


if __name__ == "__main__":
    main()
