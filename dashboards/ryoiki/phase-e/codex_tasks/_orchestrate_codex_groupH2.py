"""Group H2: Compress DEEPER box to 200-300 Japanese chars per spec §6.

Current DEEPER is 500-550 chars (~2x oversize). Compress to 200-300 keeping the
'decisive moment' (year + person) opening style.
"""
import argparse
import subprocess
import shutil
import time
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

SRC_DIR = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series-v2")
BACKUP_DIR = SRC_DIR / "_backup_codex_groupH2"
MARKER = "deeper-compressed-v1"

PROMPT_TEMPLATE = """You are a precision editor for 連載「Futures（未来のかたち）」.

TASK: Compress the DEEPER box in {filename} to 200-300 Japanese characters.

CONTEXT:
- DEEPER currently is 500-550 chars (~2x spec range)
- Spec §6.2: DEEPER must be 200-300 chars, single paragraph prose
- Open with a 'decisive moment': year + person + venue (e.g., "1984年にウルリックがScienceに発表した実験で、...")
- Then 1-2 lines of follow-up research / 2010s state
- Preserve at least one Japanese researcher reference if originally present

STEPS:
1. Read {filename}. Locate `<details class="reading-lens" id="lens-academic-deep">` or similar DEEPER block.
2. Find the main `<p>` inside reading-lens-body that contains the prose (NOT the signal-list).
3. Rewrite to 200-300 Japanese chars (count visible chars, exclude HTML tags).
   - Keep the decisive moment opening (year + person + source)
   - Preserve any Japanese researcher mention
   - Compress secondary references to 1-2 lines
4. Add hidden marker `<!-- {marker} -->` right after the `<details class="reading-lens" id="lens-academic-deep">` opening tag.
5. Apply with your edit tool. Do not modify signal-list or KEY REFERENCE.
6. Output: "OK: {basename} -> N chars"

CONSTRAINTS:
- Modify ONLY the main DEEPER `<p>` text — preserve signal-list/signal-item completely
- Do not invent facts. Use existing claims only.
- If {marker} already present, output "SKIP: {basename}"
- Final length MUST be 200-300 chars; verify before submitting
"""


def list_targets() -> list:
    targets = []
    for p in sorted(SRC_DIR.glob("ep*.html")):
        if not re.match(r"ep\d{3}\.html$", p.name):
            continue
        text = p.read_text(encoding="utf-8")
        if MARKER in text:
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
        return {
            "file": filename,
            "status": "ok" if has_marker else "failed",
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
    args = ap.parse_args()
    remaining = list_targets()
    print(f"=== Group H2: DEEPER compression to 200-300 chars ===")
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
        print(f"\n=== Wave {wave_idx}: {len(batch)} codex ===")
        with ThreadPoolExecutor(max_workers=args.wave_size) as pool:
            futs = {pool.submit(run_codex, f): f for f in batch}
            for fut in as_completed(futs):
                r = fut.result()
                all_results.append(r)
                print(f"  [{r['file']}] {r['status']}")
        elapsed = time.time() - t0
        ok = sum(1 for r in all_results if r["status"] == "ok")
        print(f"  Wave {wave_idx} {elapsed:.1f}s | OK: {ok}/{len(all_results)}")
    ok = sum(1 for r in all_results if r["status"] == "ok")
    print(f"\n=== Final: {ok}/{len(all_results)} ===")


if __name__ == "__main__":
    main()
