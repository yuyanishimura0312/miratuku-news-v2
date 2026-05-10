#!/usr/bin/env python3
"""Codex の LAB ログから各話の LAB 本文を抽出し、_drafts/ep0NN.md の `# SIGNAL` 前に挿入する。"""

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "_build"
DRAFTS = ROOT / "_drafts"

EP_MARKER = re.compile(r"^===\s*EP(\d{3})\s*===\s*$", re.MULTILINE)


def extract_codex_response(log_text: str) -> str:
    """Codex log から回答本体を抽出（最初の `codex` マーカー以降〜`tokens used` まで）。"""
    codex_match = re.search(r"^codex\s*$", log_text, re.MULTILINE)
    if not codex_match:
        return log_text
    start = codex_match.end()
    tokens_match = re.search(r"^tokens used\s*$", log_text[start:], re.MULTILINE)
    if tokens_match:
        return log_text[start : start + tokens_match.start()]
    return log_text[start:]


def parse_lab_log(log_path: Path) -> dict[int, str]:
    """ログから {ep_num: lab_text} を抽出。同じ ep_num が2回出る場合は1回目のみ採用。"""
    text = extract_codex_response(log_path.read_text(encoding="utf-8"))
    matches = list(EP_MARKER.finditer(text))
    out = {}
    seen = set()
    for i, m in enumerate(matches):
        ep_num = int(m.group(1))
        if ep_num in seen:
            continue
        seen.add(ep_num)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        # コードブロック ``` を除去
        body = re.sub(r"^```[a-z]*\s*\n", "", body, flags=re.MULTILINE)
        body = re.sub(r"\n```\s*$", "", body, flags=re.MULTILINE)
        body = body.strip()
        out[ep_num] = body
    return out


def insert_lab_into_draft(draft_path: Path, lab_text: str) -> bool:
    """draft の `# SIGNAL` の前に `# LAB\n\n{lab_text}\n\n` を挿入する。既存LABがあれば置換。"""
    text = draft_path.read_text(encoding="utf-8")

    # 既存LABがあれば置換
    if "# LAB" in text:
        text = re.sub(
            r"\n# LAB\n.*?(\n# SIGNAL)",
            f"\n# LAB\n\n{lab_text}\n{'\\1'}",
            text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        # # SIGNAL の前に挿入
        if "\n# SIGNAL" not in text:
            return False
        text = text.replace("\n# SIGNAL", f"\n# LAB\n\n{lab_text}\n\n# SIGNAL", 1)

    draft_path.write_text(text, encoding="utf-8")
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("logs", nargs="+", type=Path)
    args = p.parse_args()

    inserted = 0
    skipped = 0
    for log in args.logs:
        labs = parse_lab_log(log)
        for ep_num, lab_text in labs.items():
            draft = DRAFTS / f"ep{ep_num:03d}.md"
            if not draft.exists():
                print(f"[skip] {draft} not found")
                skipped += 1
                continue
            if insert_lab_into_draft(draft, lab_text):
                print(f"[inserted] ep{ep_num:03d} ({len(lab_text)} chars)")
                inserted += 1
            else:
                print(f"[failed] ep{ep_num:03d}: no SIGNAL anchor")
                skipped += 1
    print(f"Total: inserted={inserted}, skipped={skipped}")


if __name__ == "__main__":
    main()
