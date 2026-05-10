#!/usr/bin/env python3
"""futures-series/index.html を生成する。全100話のリストとPART構成を表示。"""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "_build"
EPISODES = BUILD / "episodes.json"

PARTS = [
    (1, 3, "PROLOGUE — 序 章", "現在地から旅をはじめる"),
    (4, 23, "PART I", "いま動き始めている問い（問03 場所性 ／ 問06 ケア教育）"),
    (24, 43, "PART II", "制度に届く問い（問01 未来世代 ／ 問02 先住民の知恵）"),
    (44, 63, "PART III", "学問が組み替わる問い（問07 西洋以外の知 ／ 問08 複数の自己）"),
    (64, 83, "PART IV", "70年後の到達点（問04 複数の世界の見方）"),
    (84, 95, "PART V", "自己診断の問い（問05 問いの問い）"),
    (96, 100, "FINAL — 終 章", "読者の坂を編む"),
]

INDEX_TPL = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>未来のかたち — 全100話 | NPO法人ミラツク</title>
<meta name="description" content="NPO法人ミラツクが発信する100話連載「未来のかたち」。70年先を考えるための100話。">
<link rel="icon" href="https://esse-sense.com/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700;900&family=Noto+Serif+JP:wght@300;400;500;600;700;900&family=Judson:wght@400;700&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #14110F;
  --bg-soft: #1E1B19;
  --bg-tint: #25221F;
  --ink: #FFFFFF;
  --ink-soft: #D8D5D1;
  --ink-mute: #A6A29D;
  --accent: #FF3644;
  --accent-deep: #FF5560;
  --accent-soft: rgba(255, 54, 68, 0.10);
  --line: #2D2A27;
  --serif: "Noto Serif JP", "Hiragino Mincho ProN", Georgia, serif;
  --sans: "Noto Sans JP", "Hiragino Sans", -apple-system, sans-serif;
  --display: "Judson", "Noto Serif JP", Georgia, serif;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; scroll-behavior: smooth; }
body { font-family: var(--serif); background: var(--bg); color: var(--ink); line-height: 1.95; letter-spacing: 0.02em; font-feature-settings: "palt"; -webkit-font-smoothing: antialiased; }
a { color: var(--accent); text-decoration: none; transition: color .15s; }
a:hover { color: var(--accent-deep); text-decoration: underline; }

.site-header { position: sticky; top: 0; z-index: 100; background: rgba(20, 17, 15, 0.92); backdrop-filter: saturate(160%) blur(10px); border-bottom: 1px solid var(--line); }
.site-header-inner { max-width: 1280px; margin: 0 auto; padding: 0 24px; height: 64px; display: flex; align-items: center; justify-content: space-between; gap: 16px; }
.site-brand { font-family: var(--sans); font-size: 12px; font-weight: 700; letter-spacing: 0.16em; color: var(--ink); }
.site-brand small { display: block; font-size: 9.5px; letter-spacing: 0.14em; color: var(--ink-mute); font-weight: 500; margin-top: 2px; }
.site-nav { display: flex; gap: 28px; font-family: var(--sans); font-size: 12px; letter-spacing: 0.1em; }
.site-nav a { color: var(--ink-soft); font-weight: 500; }

.hero { padding: 110px 24px 80px; max-width: 960px; margin: 0 auto; text-align: center; border-bottom: 1px solid var(--line); }
.hero-eyebrow { font-family: var(--sans); font-size: 11px; font-weight: 700; letter-spacing: 0.32em; color: var(--accent); margin-bottom: 28px; }
.hero-title { font-family: var(--serif); font-size: 56px; font-weight: 900; line-height: 1.2; margin-bottom: 28px; letter-spacing: 0.02em; }
.hero-sub { font-family: var(--display); font-size: 22px; color: var(--ink-mute); margin-bottom: 32px; }
.hero-lead { font-family: var(--serif); font-size: 17px; line-height: 2; color: var(--ink-soft); max-width: 720px; margin: 0 auto; padding-left: 22px; border-left: 3px solid var(--accent); text-align: left; }

.parts { max-width: 1080px; margin: 0 auto; padding: 80px 24px 120px; }
.part-block { margin-bottom: 88px; }
.part-eyebrow { font-family: var(--sans); font-size: 12px; font-weight: 700; letter-spacing: 0.28em; color: var(--accent); margin-bottom: 14px; display: flex; align-items: baseline; gap: 18px; padding-bottom: 14px; border-bottom: 1px solid var(--line); }
.part-eyebrow .range { color: var(--ink-mute); font-weight: 500; letter-spacing: 0.14em; }
.part-title { font-family: var(--serif); font-size: 26px; font-weight: 700; margin-bottom: 24px; letter-spacing: 0.02em; }

.ep-list { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px 28px; }
.ep-item { padding: 16px 20px; border: 1px solid var(--line); background: var(--bg-soft); transition: border-color .15s, background .15s; display: flex; align-items: baseline; gap: 16px; text-decoration: none; }
.ep-item:hover { border-color: var(--accent); background: var(--bg-tint); text-decoration: none; }
.ep-item.upcoming { opacity: 0.55; }
.ep-num { font-family: var(--display); font-size: 22px; color: var(--accent); font-weight: 700; flex-shrink: 0; min-width: 48px; }
.ep-title { font-family: var(--serif); font-size: 14.5px; color: var(--ink); line-height: 1.55; letter-spacing: 0.04em; }
.ep-status { font-family: var(--sans); font-size: 9.5px; letter-spacing: 0.16em; color: var(--ink-mute); margin-left: auto; flex-shrink: 0; padding-left: 14px; }
.ep-status.published { color: var(--accent); }

footer { background: var(--bg-soft); padding: 48px 24px 32px; border-top: 1px solid var(--line); text-align: center; font-family: var(--sans); font-size: 11px; color: var(--ink-mute); letter-spacing: 0.06em; }

@media (max-width: 720px) {
  .hero-title { font-size: 36px; }
  .hero-sub { font-size: 18px; }
  .ep-list { grid-template-columns: 1fr; }
}
</style>
</head>
<body>

<header class="site-header">
  <div class="site-header-inner">
    <a href="../../ryoiki-index.html" class="site-brand">未来のかたち<small>FUTURES NO KATACHI / 70年先を考えるための100話</small></a>
    <nav class="site-nav">
      <a href="../../ryoiki-index.html">ホーム</a>
      <a href="../eight-questions-lp.html">8つの問い</a>
    </nav>
  </div>
</header>

<section class="hero">
  <div class="hero-eyebrow">A SERIES OF 100 — 70 YEARS AHEAD</div>
  <h1 class="hero-title">未来のかたち</h1>
  <p class="hero-sub">FUTURES NO KATACHI</p>
  <p class="hero-lead">NPO法人ミラツクが、70年先を考えるための100話を編んでいる。「8つの問い」を起点に、哲学・人類学・文学・神話・伝統知の系譜と、いま現実の地形に立ち上がっている兆しの両方を、平らな日本語で翻訳する。連載は7つのPARTで構成され、全100話を読み終えるころ、自分の坂が少しだけ見えてくるよう設計されている。</p>
</section>

<section class="parts">
{{PART_BLOCKS}}
</section>

<footer>
  <p>&copy; NPO法人ミラツク / 未来のかたち</p>
  <p style="margin-top: 8px;">FUTURES NO KATACHI ・ Total 100 episodes</p>
</footer>

</body>
</html>
"""


def main():
    episodes = json.loads(EPISODES.read_text(encoding="utf-8"))
    ep_by_num = {e["num"]: e for e in episodes}

    blocks = []
    for s, e, label, title in PARTS:
        items = []
        for n in range(s, e + 1):
            ep = ep_by_num.get(n)
            if not ep:
                continue
            ep_path = ROOT / f"ep{n:03d}.html"
            published = ep_path.exists()
            cls = "ep-item" if published else "ep-item upcoming"
            href = f"./ep{n:03d}.html" if published else "#"
            status_cls = "ep-status published" if published else "ep-status"
            status_text = "PUBLISHED" if published else "COMING"
            items.append(
                f'      <a class="{cls}" href="{href}">'
                f'<span class="ep-num">{n:02d}</span>'
                f'<span class="ep-title">{html.escape(ep["title"])}</span>'
                f'<span class="{status_cls}">{status_text}</span>'
                f'</a>'
            )
        block = (
            f'  <section class="part-block">\n'
            f'    <div class="part-eyebrow">{html.escape(label)} <span class="range">第{s}話 — 第{e}話</span></div>\n'
            f'    <h2 class="part-title">{html.escape(title)}</h2>\n'
            f'    <div class="ep-list">\n' + "\n".join(items) + "\n    </div>\n"
            f'  </section>'
        )
        blocks.append(block)

    output = INDEX_TPL.replace("{{PART_BLOCKS}}", "\n".join(blocks))
    out_path = ROOT / "index.html"
    out_path.write_text(output, encoding="utf-8")
    print(f"Generated: {out_path}")
    pub_count = sum(1 for n in range(1, 101) if (ROOT / f"ep{n:03d}.html").exists())
    print(f"Published: {pub_count}/100")


if __name__ == "__main__":
    main()
