#!/usr/bin/env python3
"""Codex出力ログを `=== EPNNN ===` マーカーで分割し、_drafts/ep0NN.md に保存する。"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "_build"
DRAFTS = ROOT / "_drafts"

EP_MARKER = re.compile(r"^===\s*EP(\d{3})\s*===\s*$", re.MULTILINE)


def extract_codex_response(log_text: str) -> str:
    """Codex log から実際の回答本体を抽出する。`codex` 行の後 〜 `tokens used` 行の前。"""
    # codex 行を探す
    codex_match = re.search(r"^codex\s*$", log_text, re.MULTILINE)
    if not codex_match:
        # マーカーがない場合、ログ全体を返す（フォールバック）
        return log_text
    start = codex_match.end()
    tokens_match = re.search(r"^tokens used\s*$", log_text[start:], re.MULTILINE)
    if tokens_match:
        return log_text[start : start + tokens_match.start()]
    return log_text[start:]


def split_log(log_path: Path, drafts_dir: Path, force: bool = False) -> int:
    log_text = log_path.read_text(encoding="utf-8")
    response = extract_codex_response(log_text)

    # マーカーで分割
    matches = list(EP_MARKER.finditer(response))
    if not matches:
        print(f"[WARN] no EP markers in {log_path}")
        return 0

    drafts_dir.mkdir(parents=True, exist_ok=True)
    saved = 0
    for i, m in enumerate(matches):
        ep_num = int(m.group(1))
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(response)
        body = response[start:end].strip()

        # コードブロック ``` を取り除く
        body = re.sub(r"^```[a-z]*\s*\n", "", body, flags=re.MULTILINE)
        body = re.sub(r"\n```\s*$", "", body, flags=re.MULTILINE)
        body = body.strip()

        out_path = drafts_dir / f"ep{ep_num:03d}.md"
        if out_path.exists() and not force:
            print(f"[SKIP exists] {out_path}")
            continue
        out_path.write_text(body + "\n", encoding="utf-8")
        print(f"[saved] {out_path} ({len(body)} chars)")
        saved += 1
    return saved


def main():
    p = argparse.ArgumentParser()
    p.add_argument("logs", nargs="+", type=Path)
    p.add_argument("--drafts-dir", type=Path, default=DRAFTS)
    p.add_argument("--force", action="store_true", help="既存ドラフトを上書き")
    args = p.parse_args()

    total = 0
    for log in args.logs:
        total += split_log(log, args.drafts_dir, args.force)
    print(f"Total saved: {total}")


if __name__ == "__main__":
    main()
