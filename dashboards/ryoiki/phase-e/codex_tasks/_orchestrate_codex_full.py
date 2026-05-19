"""Full Codex orchestration for Group A: ep-hero-en for remaining 96 episodes.

Pilot already covered ep002/003/004. This runs the remaining 96 in waves of N parallel.

Usage:
  python3 _orchestrate_codex_full.py            # dry-run
  python3 _orchestrate_codex_full.py --apply    # launch
  python3 _orchestrate_codex_full.py --apply --wave-size 10 --wave-count 10  # 10x10
"""
import argparse
import subprocess
import shutil
import time
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

SRC_DIR = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series-v2")
BACKUP_DIR = SRC_DIR / "_backup_codex_groupA"

PROMPT_TEMPLATE = """You are a precision editor for the 連載「Futures」 series.

TASK: Add a single English title line to {filename}.

STEPS:
1. Read {filename} in this working directory.
2. Find the `<h1 class="ep-hero-title">` (Japanese title) and `<p class="ep-hero-subtitle">` or `<h2 class="ep-hero-subtitle">`.
3. Generate ONE English title sentence:
   - Title Case
   - No trailing punctuation
   - 8-15 words
   - Captures the episode's core insight (not literal translation)
4. Insert exactly this line right after the subtitle line:
   <p class="ep-hero-en">{{english_title}}</p>
5. Apply with your file-edit tool. Modify nothing else.
6. Output one line: "OK: {basename} -> <english title>"

CONSTRAINTS:
- Do not modify any other content
- Use double quotes for class
- Title must be unique (avoid generic phrases)
- If ep-hero-en already exists, output "SKIP: {basename}" and do nothing
"""


def list_remaining_episodes() -> list:
    """Return ep files that DON'T yet have <p class="ep-hero-en">."""
    targets = []
    for p in sorted(SRC_DIR.glob("ep*.html")):
        if not re.match(r"ep\d{3}\.html$", p.name):
            continue
        text = p.read_text(encoding="utf-8")
        if '<p class="ep-hero-en">' not in text:
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
    )
    try:
        result = subprocess.run(
            ["codex", "exec", "--cd", str(SRC_DIR), "--skip-git-repo-check", prompt],
            capture_output=True, text=True, timeout=600,
        )
        new = target.read_text(encoding="utf-8")
        has_en = '<p class="ep-hero-en">' in new
        eng = ""
        m = re.search(r'<p class="ep-hero-en">([^<]+)</p>', new)
        if m:
            eng = m.group(1).strip()
        return {
            "file": filename,
            "status": "ok" if has_en else "failed",
            "english": eng,
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
    ap.add_argument("--wave-size", type=int, default=10, help="parallel codex per wave")
    ap.add_argument("--wave-count", type=int, default=None, help="max waves (None = until done)")
    ap.add_argument("--limit", type=int, default=None, help="cap total episodes processed")
    args = ap.parse_args()

    remaining = list_remaining_episodes()
    if args.limit:
        remaining = remaining[: args.limit]
    print(f"=== Codex Full Run: Group A (ep-hero-en) ===")
    print(f"Remaining episodes: {len(remaining)}")
    print(f"Wave size: {args.wave_size} parallel codex")
    print(f"Estimated waves: {(len(remaining) + args.wave_size - 1) // args.wave_size}")
    if not args.apply:
        print("\nDRY-RUN (use --apply to launch)")
        for i, f in enumerate(remaining[:10]):
            print(f"  {i+1}. {f}")
        if len(remaining) > 10:
            print(f"  ... and {len(remaining) - 10} more")
        return

    all_results = []
    wave_idx = 0
    while remaining:
        if args.wave_count is not None and wave_idx >= args.wave_count:
            break
        batch = remaining[: args.wave_size]
        remaining = remaining[args.wave_size :]
        wave_idx += 1
        t0 = time.time()
        print(f"\n=== Wave {wave_idx}: {len(batch)} codex agents ({batch[0]}...{batch[-1]}) ===")
        with ThreadPoolExecutor(max_workers=args.wave_size) as pool:
            futs = {pool.submit(run_codex, f): f for f in batch}
            for fut in as_completed(futs):
                r = fut.result()
                all_results.append(r)
                if r["status"] == "ok":
                    print(f"  [{r['file']}] OK: {r['english']}")
                else:
                    print(f"  [{r['file']}] {r['status']} (rc={r.get('returncode', '?')})")
                    if r.get("stderr_tail"):
                        print(f"    {r['stderr_tail'][:150]}")
        elapsed = time.time() - t0
        ok = sum(1 for r in all_results if r["status"] == "ok")
        print(f"  Wave {wave_idx} done in {elapsed:.1f}s | cumulative OK: {ok}/{len(all_results)}")

    print(f"\n=== Final ===")
    ok = sum(1 for r in all_results if r["status"] == "ok")
    print(f"Total processed: {len(all_results)}")
    print(f"Success: {ok}")
    print(f"Backup: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
