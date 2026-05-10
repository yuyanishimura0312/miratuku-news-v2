#!/usr/bin/env python3
"""100-episodes-plan.md をパースして JSON に変換する。"""

import json
import re
import sys
from pathlib import Path

PLAN = Path(__file__).resolve().parent.parent / "100-episodes-plan.md"
OUT = Path(__file__).resolve().parent / "episodes.json"

# 各話のフィールド（順序固定）
FIELDS = ["サブタイトル", "英訳", "起点", "人文知", "学術", "リード", "本文の核", "DEEPER", "SIGNAL", "次の問い"]


def parse(md_text: str) -> list[dict]:
    """Markdown からエピソードを抽出する。

    エピソードは `## 第N話「...」` または `### 第N話「...」` の見出しで始まる。
    続く行は `- フィールド名: 内容` のリスト。
    """
    episodes = []
    # 見出しパターン
    head_re = re.compile(r"^(#{2,3})\s*第(\d+)話「(.+?)」")
    field_re = re.compile(r"^-\s*([^:：]+)[:：]\s*(.+)$")

    lines = md_text.split("\n")
    i = 0
    while i < len(lines):
        m = head_re.match(lines[i])
        if not m:
            i += 1
            continue
        ep_num = int(m.group(2))
        title = m.group(3).strip()
        ep = {"num": ep_num, "title": title}
        i += 1
        # フィールドを集める（次の見出しに当たるまで）
        while i < len(lines) and not head_re.match(lines[i]):
            fm = field_re.match(lines[i])
            if fm:
                key = fm.group(1).strip()
                val = fm.group(2).strip()
                # キー名を統一
                key_map = {
                    "サブタイトル": "subtitle",
                    "英訳": "en_title",
                    "英訳タイトル": "en_title",
                    "起点": "starting_question",
                    "起点の問い": "starting_question",
                    "人文知": "humanities",
                    "人文知領域": "humanities",
                    "学術": "academic_field",
                    "学術領域": "academic_field",
                    "リード": "lead",
                    "本文の核": "body_core",
                    "DEEPER": "deeper",
                    "SIGNAL": "signal",
                    "次の問い": "next_question",
                    "次回への問い": "next_question",
                }
                ep_key = key_map.get(key)
                if ep_key:
                    ep[ep_key] = val
            i += 1
        episodes.append(ep)
    return episodes


def main():
    md = PLAN.read_text(encoding="utf-8")
    eps = parse(md)
    OUT.write_text(json.dumps(eps, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Parsed {len(eps)} episodes -> {OUT}")
    # 簡易検証
    nums = [ep["num"] for ep in eps]
    missing = [n for n in range(1, 101) if n not in nums]
    if missing:
        print(f"WARN missing episodes: {missing}")
    dups = [n for n in nums if nums.count(n) > 1]
    if dups:
        print(f"WARN duplicate episodes: {set(dups)}")


if __name__ == "__main__":
    main()
