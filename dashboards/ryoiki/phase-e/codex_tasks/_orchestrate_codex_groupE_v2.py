"""Group E: Consolidate 7-paragraph body to 6 paragraphs.

Spec: journal-essay-style.md §5.1 - body must be EXACTLY 6 paragraphs.
74 episodes currently have 7 body <p> elements.

Strategy: merge the two most semantically adjacent paragraphs.
"""
import argparse
import subprocess
import shutil
import time
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

SRC_DIR = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series-v2")
BACKUP_DIR = SRC_DIR / "_backup_codex_groupE"
MARKER = "body-6paragraph-v2"

PROMPT_TEMPLATE = """You are a precision editor for 連載「Futures（未来のかたち）」.

TASK: Consolidate the body of {filename} to EXACTLY 6 paragraphs.

CONTEXT:
- The canonical ep007 style requires the body to be exactly 6 paragraphs
- Current body has 7 paragraphs (one too many)
- The body is within `<article class="ep-body">` or `<div class="ep-body">`
- Body paragraphs are the `<p>` tags BEFORE any `<details>` or `<section class="ep-question">`
- DO NOT touch DEEPER, KEY REFERENCE, SIGNAL, QUESTION FOR NEXT — those are outside the body

STEPS:
1. Read {filename}.
2. Locate the body paragraphs (direct `<p>` children of `<article class="ep-body">` or `<div class="ep-body">`, BEFORE any `<details>` tag).
3. Identify which two consecutive paragraphs share the closest semantic theme (often paragraphs 3+4, or 5+6).
4. Merge them into ONE paragraph by:
   - Concatenating the text with a connector sentence (e.g. "そして、" "つまり、" or natural prose flow)
   - The merged paragraph length should be 250-440 chars (i.e. about the sum of both)
   - Preserve all `<strong>` emphases and factual claims
5. The result MUST be EXACTLY 6 `<p>` tags in the body section.
   - BEFORE submitting, COUNT the body paragraphs in your output.
   - If count != 6 (e.g. 5 or 7), redo the merge until count == 6.
   - It is CRITICAL that the body has exactly 6 paragraphs, not 5, not 7.
6. Add hidden marker `<!-- {marker} -->` immediately after `<article class="ep-body">` or `<div class="ep-body">` opening tag.
7. Apply with your edit tool. Modify NOTHING else.
8. Output one line: "OK: {basename} -> N paragraphs"

CONSTRAINTS:
- The DEEPER details block, signal-list, KEY REFERENCE, QUESTION FOR NEXT, ep-actions, ep-nav, footer must NOT be modified
- The opening drop-cap paragraph (first `<p>`) should be preserved with its structure
- If {marker} already present, output "SKIP: {basename}" and exit
- Use double quotes for class attributes
- Do not invent new content; only merge existing
"""


def count_body_paragraphs(text: str) -> int:
    m = re.search(r'class="ep-body"[^>]*>(.*?)</article>', text, re.DOTALL)
    if not m:
        return 0
    body = m.group(1)
    body = re.sub(r'<details[^>]*>.*?</details>', '', body, flags=re.DOTALL)
    body = re.sub(r'<section[^>]*class="ep-question[^"]*"[^>]*>.*?</section>', '', body, flags=re.DOTALL)
    body = re.sub(r'<p class="ep-pullquote"[^>]*>.*?</p>', '', body, flags=re.DOTALL)
    return len(re.findall(r'<p(?:\s[^>]*)?>', body))


def list_targets() -> list:
    targets = []
    for p in sorted(SRC_DIR.glob("ep*.html")):
        if not re.match(r"ep\d{3}\.html$", p.name):
            continue
        text = p.read_text(encoding="utf-8")
        if MARKER in text:
            continue
        if count_body_paragraphs(text) != 7:
            continue
        targets.append(p.name)
    return targets


def run_codex(filename: str) -> dict:
    target = SRC_DIR / filename
    BACKUP_DIR.mkdir(exist_ok=True)
    backup = BACKUP_DIR / filename
    if not backup.exists():
        shutil.copy(target, backup)

    prompt = PROMPT_TEMPLATE.format(
        filename=filename,
        basename=filename.replace(".html", ""),
        marker=MARKER,
    )
    try:
        result = subprocess.run(
            ["codex", "exec", "--cd", str(SRC_DIR), "--skip-git-repo-check", prompt],
            capture_output=True, text=True, timeout=600,
        )
        new = target.read_text(encoding="utf-8")
        p_count = count_body_paragraphs(new)
        has_marker = MARKER in new
        return {
            "file": filename,
            "status": "ok" if has_marker and p_count == 6 else "failed",
            "paragraphs": p_count,
            "returncode": result.returncode,
            "stderr_tail": (result.stderr or "")[-200:],
        }
    except subprocess.TimeoutExpired:
        return {"file": filename, "status": "timeout"}
    except Exception as e:
        return {"file": filename, "status": "error", "exception": str(e)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--wave-size", type=int, default=50)
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    remaining = list_targets()
    if args.limit:
        remaining = remaining[: args.limit]
    print(f"=== Group E: 7→6 paragraph consolidation ===")
    print(f"Targets: {len(remaining)}")
    if not args.apply:
        print("DRY-RUN")
        return

    all_results = []
    wave_idx = 0
    while remaining:
        batch = remaining[: args.wave_size]
        remaining = remaining[args.wave_size :]
        wave_idx += 1
        t0 = time.time()
        print(f"\n=== Wave {wave_idx}: {len(batch)} codex ({batch[0]}...{batch[-1]}) ===")
        with ThreadPoolExecutor(max_workers=args.wave_size) as pool:
            futs = {pool.submit(run_codex, f): f for f in batch}
            for fut in as_completed(futs):
                r = fut.result()
                all_results.append(r)
                print(f"  [{r['file']}] {r['status']}  paragraphs={r.get('paragraphs', '-')}")
        elapsed = time.time() - t0
        ok = sum(1 for r in all_results if r["status"] == "ok")
        print(f"  Wave {wave_idx} {elapsed:.1f}s | OK: {ok}/{len(all_results)}")

    ok = sum(1 for r in all_results if r["status"] == "ok")
    print(f"\n=== Final: {ok}/{len(all_results)} OK ===")


if __name__ == "__main__":
    main()
