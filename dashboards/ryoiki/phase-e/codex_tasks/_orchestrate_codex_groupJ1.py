"""Group J1: Eliminate [要確認] tags + ensure top-tier journals in KEY REFERENCE.

Targets: 67 files containing [要確認] (signal-list 数値 / KEY REF DOI).
Actions:
1. For SIGNAL [要確認]: if numerical claim is unverifiable, remove the number or replace with qualitative wording
2. For KEY REF [要確認]: replace with verifiable ISBN / publisher / URL
3. Ensure ≥4 top-tier journal entries in KEY REF (Nature/Science/PNAS/Cell/NEJM/Lancet/AER/QJE/Mind/J Philos/Annual Review of XXX)

Research Precision Protocol enforced.
"""
import argparse
import subprocess
import shutil
import time
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

SRC_DIR = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series-v2")
BACKUP_DIR = SRC_DIR / "_backup_codex_groupJ1"
MARKER = "no-verify-tags-toptier-v1"

PROMPT_TEMPLATE = """You are a precision editor for 連載「Futures（未来のかたち）」 with Research Precision Protocol (~/.codex/AGENTS.md Chapter 1).

TASK: Eliminate `[要確認]` tags and ensure top-tier journal references in {filename}.

STEPS:

1. Read {filename}. Identify the episode's central topic (from `<h1 class="ep-hero-title">` + body).

2. **Fix [要確認] in SIGNAL section** (`<div class="signal-list">`):
   For each `<p class="signal-text">` containing `[要確認]`:
   - If `[要確認]件` or numerical placeholders appear, REMOVE the unverifiable number and rephrase qualitatively (e.g., "拡大した" "増加傾向にある"). Do NOT invent specific numbers.
   - If `[要確認]` appears in citation tail (Author, year, [要確認] journal), keep the verifiable parts (author + year) and remove the [要確認] portion.
   - Keep `<strong>` emphasis on remaining verifiable numbers if any.

3. **Fix [要確認] in KEY REFERENCE** (`<ul class="ref-list">`):
   For each `<li>` containing `DOI: [要確認]` or similar:
   - If the work is identifiable, replace with verified ISBN, DOI, or publisher URL.
   - If completely unverifiable, replace `DOI: [要確認]` with `出典: 出版社確認要` (publisher to be verified) or simply remove the ref-doi span.
   - DO NOT invent DOIs, ISBNs, or publication metadata.

4. **Add top-tier journal references** (CRITICAL):
   Currently the file has 5-8 refs. Check existing list:
   - Count entries that contain a top-tier journal: Nature, Science, PNAS, Cell, NEJM, Lancet, AER, QJE, Mind, J Philos, Phil Review, Annual Review of XXX, JAMA, BMJ, Pol Theory, APSR, J Pol Phil, Ethics
   - If <4 such entries: ADD 1-3 NEW reference items that are top-tier journal articles RELEVANT to the episode topic AND that you can name with verifiable metadata (real DOI format `10.xxxx/xxxxx`).
   - For each new top-tier item, use canonical format:
     <li><strong>Author, F. M. (year). "Title." Journal, Vol(Issue): pages.</strong><span class="ref-doi">DOI: 10.xxxx/yyyyy ／ 日本語解説</span></li>
   - DO NOT FABRICATE. If you cannot verify with confidence, do not add.

5. Final state:
   - 0 instances of `[要確認]` in the file
   - 5-8 total KEY REFERENCE items (no decrease, possible increase to 8 max)
   - ≥4 top-tier journal entries if topic permits

6. Add hidden marker `<!-- {marker} -->` right after `<ul class="ref-list">` opening tag (replace existing keyref-expanded-v1 marker line if present).

7. Apply with your edit tool. Modify only signal-list and KEY REF; preserve body / DEEPER.

8. Output one line: "OK: {basename} -> 要確認:N→0, refs:N, top-tier:M"

CRITICAL CONSTRAINTS:
- NEVER fabricate DOIs, ISBNs, journal volumes, page numbers, author names.
- If unsure, prefer qualitative wording or removal over invented data.
- If {marker} already present, output "SKIP: {basename}" and exit.
- Do not modify body, DEEPER, hero, ep-actions, ep-nav, footer.
"""


def has_verify(text: str) -> bool:
    return "[要確認]" in text


def list_targets() -> list:
    targets = []
    for p in sorted(SRC_DIR.glob("ep*.html")):
        if not re.match(r"ep\d{3}\.html$", p.name):
            continue
        text = p.read_text(encoding="utf-8")
        if MARKER in text:
            continue
        if has_verify(text):
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
        verify_count = new.count("[要確認]")
        ref_count = new.count('<li><strong>')
        return {
            "file": filename,
            "status": "ok" if has_marker and verify_count == 0 else "partial" if has_marker else "failed",
            "verify_remaining": verify_count,
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
    ap.add_argument("--wave-size", type=int, default=30)
    args = ap.parse_args()
    remaining = list_targets()
    print(f"=== Group J1: [要確認] elimination + top-tier journal補充 ===")
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
                print(f"  [{r['file']}] {r['status']}  要確認:{r.get('verify_remaining', '-')} refs:{r.get('refs', '-')}")
        elapsed = time.time() - t0
        ok = sum(1 for r in all_results if r["status"] == "ok")
        print(f"  Wave {wave_idx} {elapsed:.1f}s | OK: {ok}/{len(all_results)}")
    ok = sum(1 for r in all_results if r["status"] == "ok")
    print(f"\n=== Final: {ok}/{len(all_results)} OK (zero [要確認]) ===")


if __name__ == "__main__":
    main()
