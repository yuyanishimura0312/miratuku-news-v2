#!/usr/bin/env python3
"""1500字未満の短い話だけを 3話単位のCodexバッチに分けて、xargs並列実行用スクリプトを生成する。"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "_build"
DRAFTS = ROOT / "_drafts"
EPISODES = BUILD / "episodes.json"
BRIEF = BUILD / "expand_brief_v2.md"
SAMPLE = DRAFTS / "ep002.md"

PER_BATCH = 3
THRESHOLD = 1500


def get_body_chars(draft_path: Path) -> int:
    text = draft_path.read_text(encoding="utf-8")
    m = re.match(r"^---\n.*?\n---\n", text, re.DOTALL)
    body = text[m.end():] if m else text
    body_m = re.search(r"# BODY\n(.*?)\n# DEEPER", body, re.DOTALL)
    return len(body_m.group(1).strip()) if body_m else 0


def main():
    episodes = json.loads(EPISODES.read_text(encoding="utf-8"))
    brief = BRIEF.read_text(encoding="utf-8")
    sample = SAMPLE.read_text(encoding="utf-8")

    # 1500字未満の話を抽出
    short = []
    for ep in episodes:
        n = ep["num"]
        if n < 4:
            continue
        draft = DRAFTS / f"ep{n:03d}.md"
        if not draft.exists():
            continue
        chars = get_body_chars(draft)
        if chars < THRESHOLD:
            short.append((n, chars))

    short.sort()
    print(f"Short episodes (BODY < {THRESHOLD}): {len(short)}")

    # 連続する番号でグループ化（PART境界とスタイル一貫性のため）
    groups = []
    current = []
    for n, c in short:
        if current and n - current[-1][0] != 1:
            groups.append(current)
            current = []
        current.append((n, c))
        if len(current) >= PER_BATCH:
            groups.append(current)
            current = []
    if current:
        groups.append(current)

    print(f"Total batches: {len(groups)}")

    ep_by_num = {e["num"]: e for e in episodes}

    sh_lines = ["#!/bin/bash", "set +e", f"OUT={BUILD}", ""]

    for bi, batch in enumerate(groups, 1):
        first_n = batch[0][0]
        last_n = batch[-1][0]
        prompt_path = BUILD / f"short_b{bi:03d}_ep{first_n:03d}-{last_n:03d}.md"

        ep_lines = []
        for n, _ in batch:
            ep = ep_by_num[n]
            existing_text = (DRAFTS / f"ep{n:03d}.md").read_text(encoding="utf-8")
            meta_lines = [f"### 第{n}話「{ep['title']}」"]
            for k, label in [
                ("subtitle", "サブタイトル"), ("en_title", "英訳"),
                ("starting_question", "起点"), ("humanities", "人文知"),
                ("academic_field", "学術"), ("lead", "リード"),
                ("body_core", "本文の核"), ("deeper", "DEEPER素材"),
                ("signal", "SIGNAL素材"), ("next_question", "次の問い"),
            ]:
                if ep.get(k):
                    meta_lines.append(f"- {label}: {ep[k]}")
            ep_lines.extend(meta_lines)
            ep_lines.append("")
            ep_lines.append("#### 既存ドラフト（短い版・これを下敷きに延長）：")
            ep_lines.append("```")
            ep_lines.append(existing_text.strip())
            ep_lines.append("```")
            ep_lines.append("")
            ep_lines.append("---")
            ep_lines.append("")

        prompt = f"""{brief}

---

## 今回あなたが担当する範囲
**第{first_n}話〜第{last_n}話の合計{len(batch)}話**

各話は1,600字未満で短い状態。**1,600-1,800字に必ず延長してください。** 1,500字を下回らないこと。

{chr(10).join(ep_lines)}

---

## サンプル（参考品質、ep002）
```
{sample}
```

---

## 出力指示
{len(batch)}話すべてを `=== EPNNN ===` マーカーで区切って出力してください。
**Web検索を絶対に使わない**。**字数を必ず守る**（BODY 1,600-1,800字、DEEPER 500-700字、SIGNAL 600-800字）。
"""
        prompt_path.write_text(prompt, encoding="utf-8")

        out_log = BUILD / f"short_b{bi:03d}_log.txt"
        done_marker = BUILD / f"short_b{bi:03d}_done"
        sh_lines.append(
            f'codex exec --sandbox workspace-write --skip-git-repo-check - < "{prompt_path}" > "{out_log}" 2>&1 && '
            f'touch "{done_marker}"'
        )

    # xargs -P 10 で並列実行
    runner = ["#!/bin/bash"]
    runner.append("set +e")
    runner.append(f"cd {BUILD}")
    runner.append("# 各バッチを10並列で実行")
    runner.append("ls short_b*_ep*.md | sed 's/_ep.*//' | sort -u > /tmp/short_batch_ids.txt")
    runner.append("while read bid; do")
    runner.append('  prompt=$(ls "${bid}_ep"*.md | head -1)')
    runner.append('  echo "[launch] $bid -> $prompt"')
    runner.append('  codex exec --sandbox workspace-write --skip-git-repo-check - < "$prompt" > "${bid}_log.txt" 2>&1 && touch "${bid}_done" &')
    runner.append('  # 並列度制御: アクティブジョブ10未満まで')
    runner.append('  while [ $(jobs -r | wc -l) -ge 10 ]; do sleep 2; done')
    runner.append("done < /tmp/short_batch_ids.txt")
    runner.append("wait")
    runner.append('echo "[ALL_SHORT_DONE]"')

    runner_sh = BUILD / "run_short_batches.sh"
    runner_sh.write_text("\n".join(runner), encoding="utf-8")
    runner_sh.chmod(0o755)
    print(f"Generated runner: {runner_sh}")
    print(f"Batches: {len(groups)}")
    for bi, batch in enumerate(groups, 1):
        print(f"  short_b{bi:03d}: ep{batch[0][0]:03d}-{batch[-1][0]:03d} ({len(batch)} eps)")


if __name__ == "__main__":
    main()
