"""Group D: KEY REFERENCE upgrade for all 100 episodes.

Spec: journal-essay-style.md §7
- 5-8 references per episode (currently 3 most)
- DOI required for each ref where applicable
- Each in <li> with ref-list class
- Format: <strong>Author (year). "Title." Journal Vol(Issue): pages.</strong>
         <span class="ref-doi">DOI: 10.xxxx ／ Japanese annotation</span>
- Preserve existing refs; only ADD verified new ones (no hallucinated DOIs)
"""
import argparse
import subprocess
import shutil
import time
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

SRC_DIR = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series-v2")
BACKUP_DIR = SRC_DIR / "_backup_codex_groupD"
MARKER = "key-reference-v2"

PROMPT_TEMPLATE = """You are a precision editor for 連載「Futures（未来のかたち）」 with Research Precision Protocol (~/.codex/AGENTS.md Chapter 1).

TASK: Restructure KEY REFERENCE in {filename} to canonical format.

CONTEXT:
Canonical structure (from kurashi/ep007.html):
<ul class="ref-list">
  <li><strong>Ulrich, R. S. (1984). "View through a window may influence recovery from surgery." Science, 224(4647): 420-421.</strong><span class="ref-doi">DOI: 10.1126/science.6143402 ／ 病室の窓と回復速度の古典的論文。</span></li>
  ... 5-8 items ...
</ul>

STEPS:
1. Read {filename}. Find the KEY REFERENCE / 参考文献 section.
2. Reformat each EXISTING reference into:
   <li><strong>{{書誌完全形}}</strong><span class="ref-doi">DOI: {{doi}} ／ {{日本語の一文説明}}</span></li>
   - If DOI is mentioned in the text, use it verbatim
   - If DOI is NOT in the text, output `DOI: [要確認]` — DO NOT INVENT
   - 書誌完全形 for journal: `Author, F. M. (year). "Title." Journal, Vol(Issue): pages.`
   - 書誌完全形 for book: `著者 (year)『書名』出版社.`
3. Wrap the whole list in `<ul class="ref-list">...</ul>` and ensure parent `<details class="reading-lens" id="lens-key-reference">` exists.
4. Do NOT add new references that weren't already cited in the body/DEEPER. Quality over quantity.
5. Preserve the current count (3-4 items is OK if that's what exists). The goal is FORMAT, not invention.
6. Add hidden marker `<!-- {marker} -->` immediately before the <ul>.
7. Output: "OK: {basename} -> <ref count> refs"

CONSTRAINTS:
- NEVER fabricate DOIs, journal volumes, page numbers, or author names
- If unsure about a field, leave it as `[要確認]`
- Preserve all existing reference content; just restructure
- Do not modify the body, DEEPER, or SIGNAL sections
- If {marker} already present, output "SKIP: {basename}" and exit
- Use double quotes for class attributes
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
            capture_output=True, text=True, timeout=900,
        )
        new = target.read_text(encoding="utf-8")
        has_marker = MARKER in new
        ref_count = new.count('<li><strong>')
        has_ref_list = 'class="ref-list"' in new
        return {
            "file": filename,
            "status": "ok" if has_marker and has_ref_list else "failed",
            "refs": ref_count,
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
    print(f"=== Group D: KEY REFERENCE upgrade ===")
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
                print(f"  [{r['file']}] {r['status']}  refs={r.get('refs', '-')}")
        elapsed = time.time() - t0
        ok = sum(1 for r in all_results if r["status"] == "ok")
        print(f"  Wave {wave_idx} {elapsed:.1f}s | OK: {ok}/{len(all_results)}")

    ok = sum(1 for r in all_results if r["status"] == "ok")
    print(f"\n=== Final: {ok}/{len(all_results)} OK ===")


if __name__ == "__main__":
    main()
