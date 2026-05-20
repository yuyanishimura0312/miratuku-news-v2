"""Group H3 + I3: Expand KEY REFERENCE to 5-8 items, and replace [要確認] DOIs
with verifiable ISBN/URL/DOI where possible. Combined to minimize file rewrites.

This prompts codex to:
1. Read the body+DEEPER to understand the episode's central topic and citations
2. Add 2-5 NEW references that are VERIFIABLE — books with ISBN, papers with DOI
3. Replace existing [要確認] DOIs with ISBN/URL for Japanese books, or remove if unverifiable
4. Honor Research Precision Protocol — no fabrication
"""
import argparse
import subprocess
import shutil
import time
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

SRC_DIR = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series-v2")
BACKUP_DIR = SRC_DIR / "_backup_codex_groupHI"
MARKER = "keyref-expanded-v1"

PROMPT_TEMPLATE = """You are a precision editor for 連載「Futures（未来のかたち）」 following Research Precision Protocol (~/.codex/AGENTS.md Chapter 1).

TASK: Expand KEY REFERENCE in {filename} from current count to 5-8 items + resolve [要確認] markers.

CONTEXT:
Current state: 3 references with [要確認] DOI placeholders
Target state: 5-8 references, every DOI either verified or replaced with ISBN/URL/出版社名

CITATION FORMAT (canonical):
<li><strong>Author, F. M. (year). "Title." Journal, Vol(Issue): pages.</strong><span class="ref-doi">DOI: 10.xxxx ／ 日本語解説</span></li>

For Japanese books, use:
<li><strong>著者 (year)『書名』出版社.</strong><span class="ref-doi">ISBN: 978-X-XXXX-XXXX-X ／ 日本語解説</span></li>

For without-DOI/without-ISBN sources (older works, foreign-language books):
<li><strong>Author (year). Title. Publisher.</strong><span class="ref-doi">出版社URL: https://... ／ 日本語解説</span></li>

STEPS:
1. Read {filename}. Identify the episode's central concept (from `<h1 class="ep-hero-title">` + body + DEEPER).
2. Locate `<ul class="ref-list">...</ul>`. Read existing 3 items.
3. For EACH existing item with `DOI: [要確認]`:
   - If the work is a journal article you can identify with confidence (e.g., a well-known classic), replace `[要確認]` with the real DOI (format `10.xxxx/xxxxx`).
   - If the work is a Japanese book (recognizable from publisher name like 岩波・みすず・東京大学出版会・講談社), replace with `ISBN: 978-X-XXXX-XXXX-X` if you can identify it. If unsure, replace with `出版社: 岩波書店` (just the publisher).
   - If the work is a non-Japanese book without a DOI, replace with `出版社: Routledge` (publisher name) or `URL: https://publisher.com/book` if known.
   - If completely unsure, replace `DOI: [要確認]` with `出典: 出版年・出版社未確認` and KEEP the rest of the citation.
4. ADD 2-5 NEW reference items that:
   - Are directly relevant to the episode's central concept (must be supportable by the body/DEEPER content)
   - Have VERIFIED publication metadata (real DOI / real ISBN / real publisher)
   - Include AT LEAST 1 Japanese researcher's work (e.g., 鶴見和子, 三宅陽一郎, 中沢新一, 大澤真幸, 廣松渉, 木村敏, etc. depending on topic)
   - Include AT LEAST 1 top-tier journal paper if topic permits (Nature, Science, PNAS, AER, QJE, Mind, J Philos, Annual Review of XXX, etc.)
   - DO NOT FABRICATE — only cite works you can name with confidence

5. Total result MUST be 5-8 items.
6. Add hidden marker `<!-- {marker} -->` immediately after `<ul class="ref-list">` opening tag.
7. Apply with your edit tool. Modify NOTHING else.
8. Output: "OK: {basename} -> N refs, M Japanese, K with DOI/ISBN"

CRITICAL CONSTRAINTS:
- NEVER fabricate DOIs, ISBNs, journal volumes, page numbers, or author names.
- If a piece of metadata is uncertain, use the safer fallback form (publisher name only / URL only / 出版年確認 required).
- If you cannot identify 2 new references with verifiable metadata, add only what you can verify — even if total stays at 4 (not 5).
- Preserve existing reference content; only restructure the [要確認] DOI portion and add new items.
- If {marker} already present, output "SKIP: {basename}" and exit.
- Body / DEEPER / SIGNAL must NOT be modified.
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
            capture_output=True, text=True, timeout=900,
        )
        new = target.read_text(encoding="utf-8")
        has_marker = MARKER in new
        ref_count = new.count('<li><strong>')
        to_verify = new.count('[要確認]')
        return {
            "file": filename,
            "status": "ok" if has_marker else "failed",
            "refs": ref_count,
            "to_verify": to_verify,
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
    print(f"=== Group H3+I3: KEY REFERENCE expansion + DOI/ISBN resolution ===")
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
                print(f"  [{r['file']}] {r['status']}  refs={r.get('refs', '-')} to_verify={r.get('to_verify', '-')}")
        elapsed = time.time() - t0
        ok = sum(1 for r in all_results if r["status"] == "ok")
        print(f"  Wave {wave_idx} {elapsed:.1f}s | OK: {ok}/{len(all_results)}")
    ok = sum(1 for r in all_results if r["status"] == "ok")
    in_range = sum(1 for r in all_results if 5 <= r.get("refs", 0) <= 8)
    print(f"\n=== Final: {ok}/{len(all_results)} OK, {in_range} in 5-8 range ===")


if __name__ == "__main__":
    main()
