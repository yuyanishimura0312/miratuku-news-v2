"""Step 1b: Add miratuku-series.css <link> to all futures-series-v2 episodes + index.

Pure additive: inserts <link> right before <style>. Existing inline styles override
ms.css where conflicts exist, so this is non-disruptive.

Brand layer (variables, fonts, site-header/footer) inherits from ms.css when not
overridden inline. Once verified, follow-up step can prune redundant inline rules.
"""
import re
import sys
from pathlib import Path

SRC_DIR = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series-v2")
BACKUP_DIR = SRC_DIR / "_backup_step1b"

MS_LINK = '<link rel="stylesheet" href="https://journal.emerging-future.org/shared/miratuku-series.css">'

STYLE_ANCHOR = re.compile(r"(\n[ \t]*)<style", re.M)
ALREADY_MARKER = "miratuku-series.css"


def process_file(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if ALREADY_MARKER in text:
        return "already"
    # Insert MS_LINK before the first <style>
    new_text, n = STYLE_ANCHOR.subn(rf"\1{MS_LINK}\1<style", text, count=1)
    if n == 0:
        return "no-style-anchor"
    path.write_text(new_text, encoding="utf-8")
    return "modified"


def main():
    dry_run = "--apply" not in sys.argv
    targets = sorted(SRC_DIR.glob("ep*.html"))
    targets = [p for p in targets if re.match(r"ep\d{3}\.html$", p.name)]
    index_p = SRC_DIR / "index.html"
    if index_p.exists():
        targets.append(index_p)

    print(f"Mode: {'DRY-RUN' if dry_run else 'APPLY'}")
    print(f"Target: {len(targets)} files")

    if not dry_run:
        BACKUP_DIR.mkdir(exist_ok=True)
        for p in targets:
            bk = BACKUP_DIR / p.name
            if not bk.exists():
                bk.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Backups: {BACKUP_DIR}")

    summary = {"modified": 0, "already": 0, "no-style-anchor": 0}
    for p in targets:
        if dry_run:
            text = p.read_text(encoding="utf-8")
            if ALREADY_MARKER in text:
                summary["already"] += 1
            elif not STYLE_ANCHOR.search(text):
                summary["no-style-anchor"] += 1
            else:
                summary["modified"] += 1
        else:
            r = process_file(p)
            summary[r] = summary.get(r, 0) + 1

    print("\nSummary:")
    for k, v in summary.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
