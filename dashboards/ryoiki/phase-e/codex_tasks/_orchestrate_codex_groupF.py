"""Group F: Replace prohibited expressions (近年/らしい/ある研究によれば/のようだ)
with specific year references or concrete sources.

Spec: journal-essay-style.md §8.4, §8.5
"""
import argparse
import subprocess
import shutil
import time
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

SRC_DIR = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series-v2")
BACKUP_DIR = SRC_DIR / "_backup_codex_groupF"
MARKER = "no-vague-expressions-v1"
PROHIBITED = ['近年', 'らしい', 'ある研究によれば', 'のようだ']

PROMPT_TEMPLATE = """You are a precision editor for 連載「Futures（未来のかたち）」.

TASK: Eliminate prohibited vague expressions from {filename}.

PROHIBITED:
- 「近年」 → use specific year (e.g. 「2020年代以降」「2024年に」)
- 「らしい」 → use definitive form or remove
- 「ある研究によれば」 → name the specific study/author/year
- 「のようだ」 → use definitive form

STEPS:
1. Read {filename}.
2. Find each occurrence of the prohibited expressions in the body, DEEPER, or signal-list (NOT in the disclaimer, KEY REFERENCE list, or CSS).
3. For each occurrence:
   - If a specific year/study is implied by context, replace with that concrete reference
   - If unclear, use the safest concrete replacement (e.g., 「近年」 → 「2020年代に入り」)
   - For 「らしい」「のようだ」: convert to definitive statement if the body supports it; otherwise remove the hedge
4. Do NOT invent facts. Only restate what the existing text supports.
5. Add hidden marker `<!-- {marker} -->` after `<article class="ep-body">` opening tag (or right after `<div class="ep-body">`).
6. Apply with your edit tool.
7. Output: "OK: {basename} -> N replacements"

CONSTRAINTS:
- Only modify the prose; preserve all HTML structure
- Do not modify the disclaimer section (`class="ep-disclaimer"`) or KEY REFERENCE (`class="ref-list"`)
- If {marker} already present, output "SKIP: {basename}" and exit
- If you find no prohibited expressions (perhaps already cleaned), output "CLEAN: {basename}"
"""


def has_prohibited(text: str) -> bool:
    body = text
    body = re.sub(r'<section[^>]*class="ep-disclaimer"[^>]*>.*?</section>', '', body, flags=re.DOTALL)
    body = re.sub(r'class="ref-list"[^>]*>.*?</ul>', '', body, flags=re.DOTALL)
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL)
    return any(p in body for p in PROHIBITED)


def list_targets() -> list:
    targets = []
    for p in sorted(SRC_DIR.glob("ep*.html")):
        if not re.match(r"ep\d{3}\.html$", p.name):
            continue
        text = p.read_text(encoding="utf-8")
        if MARKER in text:
            continue
        if has_prohibited(text):
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
        still_has = has_prohibited(new)
        has_marker = MARKER in new
        return {
            "file": filename,
            "status": "ok" if has_marker and not still_has else "partial" if has_marker else "failed",
            "still_has": still_has,
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
    ap.add_argument("--wave-size", type=int, default=30)
    args = ap.parse_args()

    remaining = list_targets()
    print(f"=== Group F: prohibited expression cleanup ===")
    print(f"Targets: {len(remaining)}")
    if not args.apply:
        print("DRY-RUN")
        for f in remaining[:20]:
            print(f"  {f}")
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
                still = "still" if r.get("still_has") else "clean"
                print(f"  [{r['file']}] {r['status']} ({still})")
        elapsed = time.time() - t0
        ok = sum(1 for r in all_results if r["status"] == "ok")
        print(f"  Wave {wave_idx} {elapsed:.1f}s | OK: {ok}/{len(all_results)}")

    ok = sum(1 for r in all_results if r["status"] == "ok")
    print(f"\n=== Final: {ok}/{len(all_results)} OK ===")


if __name__ == "__main__":
    main()
