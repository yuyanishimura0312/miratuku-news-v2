#!/usr/bin/env python3
"""Codex並列バッチスクリプトを生成する。

100-episodes-plan.md の各話メタを読み込み、Codex 1並列につき N 話の本文ドラフト生成
プロンプトを作成する。バッチを並列起動するシェルスクリプトを出力。

Usage:
  python3 build_codex_batch.py --start 3 --end 100 --per-batch 10
"""

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # futures-series/
BUILD = ROOT / "_build"
DRAFTS = ROOT / "_drafts"
EPISODES = BUILD / "episodes.json"
BRIEF = BUILD / "codex_brief.md"
SAMPLE = DRAFTS / "ep002.md"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--start", type=int, default=3)
    p.add_argument("--end", type=int, default=100)
    p.add_argument("--per-batch", type=int, default=10, help="Codex 1並列が担当する話数")
    p.add_argument("--out-sh", type=Path, default=BUILD / "run_codex_batch.sh")
    args = p.parse_args()

    episodes = json.loads(EPISODES.read_text(encoding="utf-8"))
    brief = BRIEF.read_text(encoding="utf-8")
    sample = SAMPLE.read_text(encoding="utf-8")

    # 担当範囲のエピソードを抽出
    target_eps = [e for e in episodes if args.start <= e["num"] <= args.end]

    # 既存ドラフトを除外
    target_eps = [e for e in target_eps if not (DRAFTS / f"ep{e['num']:03d}.md").exists()]

    # batch分割
    batches = []
    for i in range(0, len(target_eps), args.per_batch):
        batches.append(target_eps[i : i + args.per_batch])

    BUILD.mkdir(parents=True, exist_ok=True)

    sh_lines = ["#!/bin/bash", "set +e", f"OUT={BUILD}", "DRAFTS={}".format(DRAFTS), ""]

    for bi, batch in enumerate(batches, 1):
        first_n = batch[0]["num"]
        last_n = batch[-1]["num"]
        prompt_path = BUILD / f"prompt_b{bi:02d}_ep{first_n:03d}-{last_n:03d}.md"
        out_dir_marker = BUILD / f"batch_b{bi:02d}_done"

        # episodes セクションを構築
        ep_lines = []
        for ep in batch:
            ep_lines.append(f"### 第{ep['num']}話「{ep['title']}」")
            for k in [
                "subtitle", "en_title", "starting_question",
                "humanities", "academic_field", "lead", "body_core",
                "deeper", "signal", "next_question",
            ]:
                if ep.get(k):
                    label = {
                        "subtitle": "サブタイトル",
                        "en_title": "英訳",
                        "starting_question": "起点",
                        "humanities": "人文知",
                        "academic_field": "学術",
                        "lead": "リード",
                        "body_core": "本文の核",
                        "deeper": "DEEPER素材",
                        "signal": "SIGNAL素材",
                        "next_question": "次の問い",
                    }[k]
                    ep_lines.append(f"- {label}: {ep[k]}")
            ep_lines.append("")

        prompt = f"""{brief}

---

## 今回あなたが担当する範囲
**第{first_n}話〜第{last_n}話の合計{len(batch)}話**

各話のメタ情報（企画書から）：

{chr(10).join(ep_lines)}

---

## サンプル（既執筆済み・第2話）
このフォーマットを忠実に守ること。本文の質感・段落構成・プルクオート位置を参考に。

```
{sample}
```

---

## 出力指示
{len(batch)}話すべての本文ドラフトを、以下のように区切って出力してください：

```
=== EP{first_n:03d} ===
（第{first_n}話の frontmatter+BODY+DEEPER+SIGNAL ※サンプル形式に従う）

=== EP{first_n+1:03d} ===
（第{first_n+1}話）

...
```

各 `=== EPNNN ===` の見出しで区切ること。途中で省略せず、{len(batch)}話すべて書き切ること。
"""

        prompt_path.write_text(prompt, encoding="utf-8")

        out_log = BUILD / f"batch_b{bi:02d}_log.txt"
        sh_lines.append(
            f'codex exec --sandbox workspace-write --skip-git-repo-check - < "{prompt_path}" > "{out_log}" 2>&1 && '
            f'touch "{out_dir_marker}" &'
        )
        sh_lines.append(f'echo "[launched] batch_b{bi:02d} ep{first_n:03d}-{last_n:03d}"')

    sh_lines.append("")
    sh_lines.append("wait")
    sh_lines.append('echo "[ALL BATCHES DONE]"')
    sh_lines.append('ls -la $OUT/batch_b*_log.txt')

    args.out_sh.write_text("\n".join(sh_lines), encoding="utf-8")
    args.out_sh.chmod(0o755)
    print(f"Generated batch script: {args.out_sh}")
    print(f"Total batches: {len(batches)} ({len(target_eps)} episodes)")
    for bi, batch in enumerate(batches, 1):
        print(f"  b{bi:02d}: ep{batch[0]['num']:03d}-{batch[-1]['num']:03d} ({len(batch)} eps)")


if __name__ == "__main__":
    main()
