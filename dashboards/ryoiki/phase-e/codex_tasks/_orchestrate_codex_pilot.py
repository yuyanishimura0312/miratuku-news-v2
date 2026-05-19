"""Pilot: launch 3 codex agents in parallel for Group A (ep-hero-en English title generation).

Tests:
- codex exec invocation pattern
- file modification correctness
- parallel coordination
- backup safety

Run: python3 _orchestrate_codex_pilot.py
"""
import subprocess
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

SRC_DIR = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series-v2")
BACKUP_DIR = SRC_DIR / "_backup_codex_pilot"
PILOT_TARGETS = ["ep002.html", "ep003.html", "ep004.html"]

PROMPT_TEMPLATE = """You are a precision editor for the 連載「Futures」 series at journal.emerging-future.org.

TASK: Add a single English title line to {filename}.

STEPS:
1. Read {filename} in this working directory.
2. Find the `<h1 class="ep-hero-title">` (Japanese title) and `<h2 class="ep-hero-subtitle">` (subtitle).
3. Generate ONE English title sentence that captures the essence of the episode:
   - Title Case
   - No trailing punctuation
   - 8-15 words
   - Reflects the Japanese title's core insight, not literal translation
4. Insert exactly this line right after the existing `<h2 class="ep-hero-subtitle">...</h2>` line:
   <p class="ep-hero-en">{{english_title}}</p>
5. Apply the edit using your file-editing tool. Do not modify anything else.
6. Output a single line summary: "OK: ep### → <english title>"

CONSTRAINTS:
- Do not modify any other content
- Do not change indentation of existing lines
- Use double quotes for the class attribute
- The English title must be unique across the series (don't reuse generic phrases)
"""


def run_codex(filename: str) -> dict:
    """Run codex exec for one file."""
    target = SRC_DIR / filename
    if not target.exists():
        return {"file": filename, "status": "missing"}

    # Backup
    BACKUP_DIR.mkdir(exist_ok=True)
    backup = BACKUP_DIR / filename
    if not backup.exists():
        shutil.copy(target, backup)

    prompt = PROMPT_TEMPLATE.format(filename=filename)

    try:
        result = subprocess.run(
            ["codex", "exec", "--cd", str(SRC_DIR), "--skip-git-repo-check", prompt],
            capture_output=True, text=True, timeout=600,
        )
        success = result.returncode == 0
        # Verify the edit happened
        new_content = target.read_text(encoding="utf-8")
        has_en = '<p class="ep-hero-en">' in new_content
        return {
            "file": filename,
            "status": "ok" if success and has_en else "failed",
            "returncode": result.returncode,
            "stdout_tail": result.stdout[-500:] if result.stdout else "",
            "stderr_tail": result.stderr[-300:] if result.stderr else "",
            "has_en_p_tag": has_en,
        }
    except subprocess.TimeoutExpired:
        return {"file": filename, "status": "timeout"}
    except Exception as e:
        return {"file": filename, "status": "error", "exception": str(e)}


def main():
    print(f"=== Codex Pilot: {len(PILOT_TARGETS)} parallel codex agents ===")
    print(f"Targets: {PILOT_TARGETS}")
    print(f"Backup dir: {BACKUP_DIR}")
    print()

    results = []
    with ThreadPoolExecutor(max_workers=len(PILOT_TARGETS)) as pool:
        futures = {pool.submit(run_codex, f): f for f in PILOT_TARGETS}
        for fut in as_completed(futures):
            r = fut.result()
            results.append(r)
            print(f"[{r['file']}] status={r['status']}", end="")
            if r.get('stdout_tail'):
                last_line = r['stdout_tail'].strip().split('\n')[-1][:100]
                print(f"  | {last_line}")
            else:
                print()

    print("\n=== Summary ===")
    ok = sum(1 for r in results if r["status"] == "ok")
    print(f"  Success: {ok}/{len(results)}")
    for r in results:
        if r["status"] != "ok":
            print(f"  {r['file']}: {r['status']}")
            if "stderr_tail" in r and r["stderr_tail"]:
                print(f"    stderr: {r['stderr_tail'][:200]}")

    # Show the actual new lines
    print("\n=== Inserted English titles ===")
    for r in results:
        if r["status"] == "ok":
            target = SRC_DIR / r["file"]
            text = target.read_text(encoding="utf-8")
            import re
            m = re.search(r'<p class="ep-hero-en">([^<]+)</p>', text)
            if m:
                print(f"  {r['file']}: {m.group(1)}")


if __name__ == "__main__":
    main()
