"""Group I1: Add ep-actions block (3 buttons) to all 100 episodes.

Insertion: just before <nav class="ep-nav"> if not already present.
"""
import re
import sys
from pathlib import Path

SRC_DIR = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series-v2")
BACKUP_DIR = SRC_DIR / "_backup_groupI1"

EP_ACTIONS_HTML = '''
<section class="ep-actions" aria-label="読了後アクション">
  <div class="ep-actions-inner">
    <a class="ep-action-btn primary" href="./#newsletter">メルマガで次話を受け取る</a>
    <a class="ep-action-btn" href="mailto:contact@miratuku.org?subject=Futures%E9%80%A3%E8%BC%89%E3%81%B8%E3%81%AE%E6%84%9F%E6%83%B3">この話に感想を送る</a>
    <a class="ep-action-btn" href="./">全100話の地図へ</a>
  </div>
</section>

'''

EP_ACTIONS_CSS = """
/* Group I1: ep-actions */
.ep-actions { max-width: 760px; margin: 56px auto 28px; padding: 0 24px; }
.ep-actions-inner { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; }
.ep-action-btn {
  display: inline-flex; align-items: center; justify-content: center;
  font-family: var(--ui, "Noto Sans JP", sans-serif);
  font-size: 12.5px; font-weight: 500; letter-spacing: 0.12em;
  padding: 13px 22px; min-width: 200px;
  border: 1px solid var(--rule, #d9d9d9); background: transparent;
  color: var(--ink, #121212); text-decoration: none;
  transition: border-color .15s, color .15s, background .15s;
}
.ep-action-btn:hover { border-color: var(--accent, #FF3644); color: var(--accent, #FF3644); }
.ep-action-btn.primary { background: var(--accent, #FF3644); border-color: var(--accent, #FF3644); color: #fff; }
.ep-action-btn.primary:hover { background: var(--accent-deep, #FF5560); border-color: var(--accent-deep, #FF5560); color: #fff; }
@media (max-width: 680px) {
  .ep-actions { margin: 40px auto 20px; padding: 0 18px; }
  .ep-action-btn { width: 100%; min-width: 0; padding: 12px 16px; }
}
"""

NAV_ANCHOR = '<nav class="ep-nav">'
STYLE_CLOSE = '</style>'
HTML_MARKER = 'class="ep-actions"'
CSS_MARKER = '/* Group I1: ep-actions */'


def process(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if HTML_MARKER in text and CSS_MARKER in text:
        return "already"
    if NAV_ANCHOR not in text:
        return "no-anchor"
    if STYLE_CLOSE not in text:
        return "no-style-anchor"

    BACKUP_DIR.mkdir(exist_ok=True)
    bk = BACKUP_DIR / path.name
    if not bk.exists():
        bk.write_text(text, encoding="utf-8")

    if HTML_MARKER not in text:
        text = text.replace(NAV_ANCHOR, EP_ACTIONS_HTML + NAV_ANCHOR, 1)
    if CSS_MARKER not in text:
        text = text.replace(STYLE_CLOSE, EP_ACTIONS_CSS + STYLE_CLOSE, 1)

    path.write_text(text, encoding="utf-8")
    return "modified"


def main():
    dry = "--apply" not in sys.argv
    targets = sorted(SRC_DIR.glob("ep*.html"))
    targets = [p for p in targets if re.match(r"ep\d{3}\.html$", p.name)]
    print(f"Mode: {'DRY-RUN' if dry else 'APPLY'} / {len(targets)} files")
    summary = {}
    for p in targets:
        if dry:
            text = p.read_text(encoding="utf-8")
            if HTML_MARKER in text and CSS_MARKER in text:
                r = "already"
            elif NAV_ANCHOR not in text:
                r = "no-anchor"
            elif STYLE_CLOSE not in text:
                r = "no-style-anchor"
            else:
                r = "modified"
        else:
            r = process(p)
        summary[r] = summary.get(r, 0) + 1
    for k, v in summary.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
