"""Group B: Hero lead expansion (50-80 chars added) for all 100 episodes.

Spec: journal-essay-style.md §3.4
- Current lead: 145-172 chars
- Target: 200-320 chars
- Preserve existing body, structure
- Strengthen "body experience → why this becomes scholarly object" arc
"""
import argparse
import subprocess
import shutil
import time
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

SRC_DIR = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series-v2")
BACKUP_DIR = SRC_DIR / "_backup_codex_groupB"
MARKER = "ep-hero-lead-extended-v1"

PROMPT_TEMPLATE = """You are a precision editor for 連載「Futures（未来のかたち）」 at journal.emerging-future.org.

TASK: Expand the hero lead in {filename} to 200-320 characters (Japanese).

CONTEXT:
- The series follows ep007 canonical style (kurashi/ep007.html)
- Hero lead must enter from a bodily/concrete experience, then bridge to why this becomes a scholarly object
- Current leads are 145-172 chars (too short)
- Target: 200-320 chars (counting Japanese characters)

STEPS:
1. Read {filename} in the working directory.
2. Locate `<p class="ep-hero-lead">...</p>` (single paragraph).
3. Rewrite the lead in Japanese, satisfying ALL:
   - 200-320 Japanese characters (count visible chars, excluding HTML)
   - Open with a concrete/bodily scene (not abstract definition)
   - Bridge to the episode's central question
   - End with a thread that pulls the reader into the body
   - Keep the SAME core message as the existing lead
   - Use only `<strong>` for any emphasis (no `<em>`)
   - Do not introduce new claims unsupported by the body
4. Add a hidden marker comment immediately before the lead: `<!-- {marker} -->`
   (this lets us detect already-processed files)
5. Apply via your edit tool. Modify nothing else.
6. Output one line: "OK: {basename} -> <character count>"

CONSTRAINTS:
- Modify only the contents of <p class="ep-hero-lead">
- Add ONLY the hidden marker; do not modify other tags
- If {marker} already present in file, output "SKIP: {basename}" and exit
- Preserve indentation
- Stay within 200-320 chars; verify by counting before submitting
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
        # Extract lead length
        m = re.search(r'<p class="ep-hero-lead">([^<]+(?:<[^/][^>]*>[^<]*</[^>]+>[^<]*)*)</p>', new)
        lead_text = ""
        if m:
            lead_text = re.sub(r"<[^>]+>", "", m.group(1))
        return {
            "file": filename,
            "status": "ok" if has_marker else "failed",
            "lead_chars": len(lead_text),
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
    print(f"=== Group B: Hero lead expansion ===")
    print(f"Remaining: {len(remaining)}")
    if not args.apply:
        print("DRY-RUN (use --apply)")
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
                marker = "OK" if r["status"] == "ok" else r["status"].upper()
                print(f"  [{r['file']}] {marker}  lead={r.get('lead_chars', '-')} chars")
        elapsed = time.time() - t0
        ok = sum(1 for r in all_results if r["status"] == "ok")
        print(f"  Wave {wave_idx} {elapsed:.1f}s | cumulative OK: {ok}/{len(all_results)}")

    print(f"\n=== Final ===")
    ok = sum(1 for r in all_results if r["status"] == "ok")
    print(f"Success: {ok}/{len(all_results)}")
    # Distribution
    in_range = sum(1 for r in all_results if r["status"] == "ok" and 200 <= r.get("lead_chars", 0) <= 320)
    print(f"In target range (200-320 chars): {in_range}")


if __name__ == "__main__":
    main()
