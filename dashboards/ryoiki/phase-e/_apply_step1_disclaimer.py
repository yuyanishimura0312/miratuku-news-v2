"""Step 1: Add disclaimer block to all 100 episodes of futures-series-v2.

Insertion point: just before `<footer class="site-footer">` line.
Safe additive change. Adapted from journal-essay-style.md §12.
"""
import re
import sys
from pathlib import Path

SRC_DIR = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series-v2")
BACKUP_DIR = SRC_DIR / "_backup_step1"

DISCLAIMER_HTML = """
<section class="ep-disclaimer" aria-label="本連載の利用について">
  <div class="ep-disclaimer-inner">
    <p class="ep-disclaimer-title"><strong>本連載の利用について</strong></p>
    <p class="ep-disclaimer-text">本連載で紹介する研究内容や事例は、公表された時点までの知見に基づくもので、その後の研究や実践で更新される可能性があります。引用した数値・効果は集団の傾向であり、個人差や文脈差が大きいことが前提です。政策・事業・個人の判断に活用される場合は、必ず一次資料や専門家への確認をあわせて行ってください。研究の存在・年代・著者は実在検証を行っていますが、解釈や要約に誤りを発見された場合は <a href="mailto:contact@miratuku.org">contact@miratuku.org</a> までお知らせください。</p>
  </div>
</section>
"""

DISCLAIMER_CSS = """
/* Step 1: Disclaimer block */
.ep-disclaimer { max-width: 760px; margin: 64px auto 32px; padding: 0 24px; }
.ep-disclaimer-inner { padding: 24px 28px; border-top: 1px solid var(--rule, #d9d9d9); border-bottom: 1px solid var(--rule, #d9d9d9); }
.ep-disclaimer-title { margin: 0 0 10px; font-size: 12px; letter-spacing: 0.14em; color: var(--ink-mute, #6b6b6b); font-family: var(--ui, "Noto Sans JP", sans-serif); }
.ep-disclaimer-text { margin: 0; font-size: 13px; line-height: 1.85; color: var(--ink-mute, #6b6b6b); font-family: var(--ui, "Noto Sans JP", sans-serif); letter-spacing: 0.02em; }
.ep-disclaimer-text a { color: var(--accent, #FF3644); text-decoration: none; border-bottom: 1px dotted currentColor; }
.ep-disclaimer-text a:hover { color: var(--accent, #FF3644); border-bottom-style: solid; }
@media (max-width: 680px) {
  .ep-disclaimer { margin: 48px auto 24px; padding: 0 18px; }
  .ep-disclaimer-inner { padding: 20px 18px; }
}
"""

FOOTER_TAG = '<footer class="site-footer">'
STYLE_CLOSE_TAG = '</style>'
DISCLAIMER_MARKER = 'class="ep-disclaimer"'
DISCLAIMER_CSS_MARKER = '/* Step 1: Disclaimer block */'


def process_file(path: Path) -> str:
    """Return one of: 'modified', 'already', 'no-anchor', 'no-style-anchor'."""
    text = path.read_text(encoding="utf-8")

    if DISCLAIMER_MARKER in text:
        return "already"

    if FOOTER_TAG not in text:
        return "no-anchor"

    # Insert CSS into first <style> block (before its </style>)
    if DISCLAIMER_CSS_MARKER not in text:
        # Use a regex anchored to first </style>
        if STYLE_CLOSE_TAG not in text:
            return "no-style-anchor"
        text = text.replace(STYLE_CLOSE_TAG, DISCLAIMER_CSS + STYLE_CLOSE_TAG, 1)

    # Insert HTML before <footer class="site-footer">
    text = text.replace(FOOTER_TAG, DISCLAIMER_HTML + "\n" + FOOTER_TAG, 1)

    path.write_text(text, encoding="utf-8")
    return "modified"


def main():
    dry_run = "--apply" not in sys.argv
    targets = sorted(SRC_DIR.glob("ep*.html"))
    targets = [p for p in targets if re.match(r"ep\d{3}\.html$", p.name)]

    if not targets:
        print("No ep###.html files found.")
        sys.exit(1)

    print(f"Mode: {'DRY-RUN (no writes)' if dry_run else 'APPLY (will modify files)'}")
    print(f"Target: {len(targets)} files")

    if not dry_run:
        BACKUP_DIR.mkdir(exist_ok=True)
        # Backup originals (only if no backup yet)
        for p in targets:
            bk = BACKUP_DIR / p.name
            if not bk.exists():
                bk.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Backups: {BACKUP_DIR} ({len(targets)} files)")

    summary = {"modified": 0, "already": 0, "no-anchor": 0, "no-style-anchor": 0}
    for p in targets:
        if dry_run:
            # Just check
            text = p.read_text(encoding="utf-8")
            if DISCLAIMER_MARKER in text:
                summary["already"] += 1
            elif FOOTER_TAG not in text:
                summary["no-anchor"] += 1
            elif STYLE_CLOSE_TAG not in text:
                summary["no-style-anchor"] += 1
            else:
                summary["modified"] += 1
        else:
            r = process_file(p)
            summary[r] = summary.get(r, 0) + 1

    print("\nSummary:")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    if dry_run:
        print("\nRun with --apply to perform writes.")


if __name__ == "__main__":
    main()
