"""Group C: SIGNAL list format conversion for all 100 episodes.

Spec: journal-essay-style.md §6.3
- Convert existing SIGNAL prose to signal-list > signal-item > signal-num + signal-text
- 3-4 items
- Each item: <strong> for numerical emphasis
- Citation tail: (Author, year, Journal Vol(Issue): pages)
"""
import argparse
import subprocess
import shutil
import time
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

SRC_DIR = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series-v2")
BACKUP_DIR = SRC_DIR / "_backup_codex_groupC"
MARKER = "signal-list-v1"

PROMPT_TEMPLATE = """You are a precision editor for 連載「Futures（未来のかたち）」.

TASK: Convert the SIGNAL section in {filename} into the canonical signal-list structure.

CONTEXT:
Canonical structure (from kurashi/ep007.html):
<div class="signal-list">
  <div class="signal-item">
    <div class="signal-num">SIGNAL 01</div>
    <p class="signal-text">{{命題文}}、<strong>{{数値}}</strong>{{追記}}（{{著者}}, {{年}}, {{誌名}}, {{巻号}}: {{ページ}}）。</p>
  </div>
  ... 3-4 items total ...
</div>

STEPS:
1. Read {filename} in the working directory.
2. Locate the SIGNAL section. The current format is free-form (paragraphs or a list).
   - Look for the heading "SIGNAL", "シグナル", or contextually relevant section
   - It often appears in a `<div class="reading-lens-body">` or similar after DEEPER
3. Convert into 3-4 signal-items following the canonical structure above.
   - Each item: 80-140 Japanese characters
   - Each item MUST have at least one <strong> wrapping a number/effect size
   - Citation tail in parentheses (existing citations preserved; do not invent new ones)
   - Numbering: SIGNAL 01, SIGNAL 02, SIGNAL 03, SIGNAL 04
4. Preserve the surrounding section structure (e.g., the `<details class="reading-lens">` wrapper).
5. Add hidden marker `<!-- {marker} -->` immediately before the signal-list div.
6. Apply via your edit tool. Do not invent citations or numbers not in the source.
7. Output: "OK: {basename} -> <item count> items"

CONSTRAINTS:
- Use ONLY citations already present in the file; if a number is missing, mark with [要確認]
- Do not modify the body paragraphs (`<p>`) or other sections
- If {marker} already present, output "SKIP: {basename}" and exit
- Class names exactly: signal-list, signal-item, signal-num, signal-text
"""


def list_targets() -> list:
    targets = []
    for p in sorted(SRC_DIR.glob("ep*.html")):
        if not re.match(r"ep\d{3}\.html$", p.name):
            continue
        if MARKER in p.read_text(encoding="utf-8"):
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
        has_marker = MARKER in new
        signal_items = new.count('class="signal-item"')
        return {
            "file": filename,
            "status": "ok" if has_marker else "failed",
            "signal_items": signal_items,
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
    print(f"=== Group C: SIGNAL list conversion ===")
    print(f"Remaining: {len(remaining)}")
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
                print(f"  [{r['file']}] {r['status']}  items={r.get('signal_items', '-')}")
        elapsed = time.time() - t0
        ok = sum(1 for r in all_results if r["status"] == "ok")
        print(f"  Wave {wave_idx} {elapsed:.1f}s | OK: {ok}/{len(all_results)}")

    ok = sum(1 for r in all_results if r["status"] == "ok")
    in_range = sum(1 for r in all_results if 3 <= r.get("signal_items", 0) <= 4)
    print(f"\n=== Final: {ok}/{len(all_results)} OK, {in_range} with 3-4 items ===")


if __name__ == "__main__":
    main()
