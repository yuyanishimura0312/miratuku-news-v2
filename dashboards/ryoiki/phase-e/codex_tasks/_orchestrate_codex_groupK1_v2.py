"""Group K1: Ensure ≥4 top-tier journal references in KEY REFERENCE for episodes
that currently have <4.

Targets only episodes failing the threshold.
"""
import argparse
import subprocess
import shutil
import time
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

SRC_DIR = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series-v2")
BACKUP_DIR = SRC_DIR / "_backup_codex_groupK1"
MARKER = "top-tier-4plus-v2"

TOP_TIER = [
    "Nature", "Science", "PNAS", "Cell", "NEJM", "New England Journal",
    "Lancet", "JAMA", "BMJ",
    "American Economic Review", "Quarterly Journal of Economics", "QJE",
    "Econometrica", "Journal of Political Economy", "JPE",
    "American Political Science Review", "APSR", "Journal of Politics",
    "Mind", "Journal of Philosophy", "J Philos", "Philosophical Review", "Ethics",
    "Annual Review of",
    "PLOS One", "PLOS ONE", "PLoS",
    "Psychological Review", "American Psychologist", "American Sociological Review",
    "American Journal of Sociology", "Sociological Theory",
    "Pol Theory", "Political Theory",
    "Journal of Consumer Research",
    "Critical Inquiry",
    "Past & Present",
    "Futures", "Technological Forecasting", "Foresight"
]


def count_top_tier(text: str) -> int:
    m = re.search(r'<ul class="ref-list"[^>]*>(.*?)</ul>', text, re.DOTALL)
    if not m: return 0
    refs = m.group(1)
    items = re.findall(r'<li>.*?</li>', refs, re.DOTALL)
    count = 0
    for item in items:
        if any(tt in item for tt in TOP_TIER):
            count += 1
    return count


PROMPT_TEMPLATE = """You are a precision editor for 連載「Futures（未来のかたち）」 with Research Precision Protocol.

TASK: Add top-tier journal references to {filename} so that the KEY REFERENCE list contains AT LEAST 4 top-tier journal entries.

CURRENT STATE: {current_count} top-tier journal entries in KEY REF.
TARGET: 4 or more top-tier entries.
ADD: {needed} more verifiable top-tier journal references.

TOP-TIER JOURNALS (any of these counts):
- General science: Nature, Science, PNAS, Cell, NEJM, Lancet, JAMA, BMJ
- Economics: American Economic Review (AER), Quarterly Journal of Economics (QJE), Econometrica, Journal of Political Economy (JPE)
- Political science: American Political Science Review (APSR), Journal of Politics, Political Theory
- Philosophy: Mind, Journal of Philosophy, Philosophical Review, Ethics
- Reviews: Annual Review of XXX (any field), PLOS ONE
- Psychology: Psychological Review, American Psychologist
- Sociology: American Sociological Review, American Journal of Sociology, Sociological Theory
- Marketing/Consumer: Journal of Consumer Research
- Futures/Foresight: Futures (Elsevier), Technological Forecasting & Social Change, Foresight
- History/Theory: Critical Inquiry, Past & Present

STEPS:
1. Read {filename}. Identify the episode's central topic (from `<h1 class="ep-hero-title">` + body + DEEPER).
2. Identify currently existing top-tier entries in `<ul class="ref-list">`.
3. Generate {needed} NEW top-tier reference items that:
   - Match a top-tier journal from the list above
   - Are topically relevant to the episode
   - Have VERIFIABLE DOI in format `10.xxxx/xxxxx` (use only DOIs you can name with high confidence)
   - Format: <li><strong>Author, F. M. (year). "Title." Journal, Vol(Issue): pages.</strong><span class="ref-doi">DOI: 10.xxxx/yyyy ／ 日本語解説</span></li>
4. INSERT the new items inside `<ul class="ref-list">` at appropriate position (end of list).
5. Total ref count should not exceed 8.
6. Add hidden marker `<!-- {marker} -->` right after `<ul class="ref-list">` opening tag.
7. Apply with your edit tool.
8. Output: "OK: {basename} -> added N top-tier refs, total {needed}+ now"

CRITICAL CONSTRAINTS:
- NEVER fabricate DOIs, journal volumes, page numbers, or author names.
- If you cannot identify {needed} verifiable top-tier articles, try harder — use 'Futures' (Elsevier), 'Technological Forecasting & Social Change', 'PLOS ONE', or 'Annual Review of XXX' which are broad enough to fit most topics.
- Use exact top-tier journal name in the citation (case-sensitive).
- Preserve existing references.
- If {marker} already present, output "SKIP: {basename}".
- Do not modify body / DEEPER / SIGNAL / hero / footer.
"""


def list_targets() -> list:
    targets = []
    for p in sorted(SRC_DIR.glob("ep*.html")):
        if not re.match(r"ep\d{3}\.html$", p.name): continue
        text = p.read_text(encoding="utf-8")
        if MARKER in text: continue
        cnt = count_top_tier(text)
        if cnt < 4:
            ref_count = text.count('<li><strong>')
            # Need 4 - cnt new ones, but cap at 8 total
            need = min(4 - cnt, 8 - ref_count)
            if need > 0:
                targets.append((p.name, cnt, need))
    return targets


def run_codex(filename: str, current: int, need: int) -> dict:
    target = SRC_DIR / filename
    BACKUP_DIR.mkdir(exist_ok=True)
    backup = BACKUP_DIR / filename
    if not backup.exists():
        shutil.copy(target, backup)

    prompt = PROMPT_TEMPLATE.format(
        filename=filename,
        basename=filename.replace(".html", ""),
        marker=MARKER,
        current_count=current,
        needed=need,
    )
    try:
        result = subprocess.run(
            ["codex", "exec", "--cd", str(SRC_DIR), "--skip-git-repo-check", prompt],
            capture_output=True, text=True, timeout=900,
        )
        new = target.read_text(encoding="utf-8")
        has_marker = MARKER in new
        new_top = count_top_tier(new)
        return {
            "file": filename,
            "status": "ok" if has_marker and new_top >= 4 else "partial" if has_marker else "failed",
            "top_tier_before": current,
            "top_tier_after": new_top,
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
    print(f"=== Group K1: top-tier journal ≥4件達成 ===")
    print(f"Targets: {len(remaining)}")
    if not args.apply:
        print("DRY-RUN")
        for f, c, n in remaining[:20]:
            print(f"  {f}: current={c}, need={n}")
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
            futs = {pool.submit(run_codex, f, c, n): f for f, c, n in batch}
            for fut in as_completed(futs):
                r = fut.result()
                all_results.append(r)
                print(f"  [{r['file']}] {r['status']}  top-tier: {r.get('top_tier_before', '-')}→{r.get('top_tier_after', '-')}")
        elapsed = time.time() - t0
        ok = sum(1 for r in all_results if r["status"] == "ok")
        print(f"  Wave {wave_idx} {elapsed:.1f}s | OK: {ok}/{len(all_results)}")
    ok = sum(1 for r in all_results if r["status"] == "ok")
    print(f"\n=== Final: {ok}/{len(all_results)} OK ===")


if __name__ == "__main__":
    main()
