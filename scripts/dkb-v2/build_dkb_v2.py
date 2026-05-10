#!/usr/bin/env python3
"""
Build deep-knowledge-book v2 for journal.emerging-future.org/deep-knowledge/
Transformations:
  1. Replace <head>/<style> with 8-questions-aligned design system (dark default + warm palette)
  2. Replace top-bar with kurashi-style transparent bar
  3. Replace book-cover with kurashi-editorial hero
  4. Add reading progress bar, mobile TOC drawer toggle, scroll-to-top
  5. Add prev/next chapter navigation between chapters
  6. Recolor SVGs: #CC1400 -> #FF3644, rgba(204,20,0,*) -> rgba(255,54,68,*)
  7. Wrap inline SVG figures with figure-card (kept neutral; SVGs stay as editorial inserts)
  8. Replace closing JS with new scroll-spy + drawer + progress
"""
import re
from pathlib import Path

SRC = Path.home() / "projects/apps/miratuku-news-v2/reports/deep-knowledge-book.html"
DST = Path("/tmp/journal-upload/deep-knowledge/index.html")
DST.parent.mkdir(parents=True, exist_ok=True)

content = SRC.read_text(encoding="utf-8")

# Chapter ID order for prev/next navigation
CHAPTERS = [
    ("intro",    "序章 浅い知の海で、深い知を求めて"),
    ("ch01",     "01 浅い知の海と、深い知の渇き"),
    ("ch02",     "02 18メガトレンドの構築と10年後の検証"),
    ("ch03",     "03 CLAの127年解析"),
    ("ch04",     "04 シグナルの長期解析と技術発展史"),
    ("ch05",     "05 ホライズン1,2,3と複数サイクルの合流点"),
    ("ch06",     "06 長期サイクルが示す合流地点"),
    ("ch07",     "07 三つの風景"),
    ("ch08",     "08 知性の地平"),
    ("ch09",     "09 知性社会の到来"),
    ("ch10",     "10 そして「深い知」が問われる理由"),
    ("ch11",     "11 関係の網のなかに立つ"),
    ("ch12",     "12 概念を作るということ"),
    ("ch13",     "13 先住民の伝統知"),
    ("ch14",     "14 伝統知の意味と価値・可能性"),
    ("ch15",     "15 火のまわりの八割"),
    ("ch16",     "16 卓越人材研究"),
    ("ch17",     "17 2100年に求められる人材像"),
    ("ch18",     "18 現代に求められる行動と人の育成"),
    ("ch19",     "19 深い知の作法"),
    ("epilogue", "終章 岸辺に立つ私たちへ"),
]

# ---- Step 1: Replace head/style block ----
NEW_HEAD = '''<!DOCTYPE html>
<html lang="ja" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>deep knowledge — 深い知が拓く2100年 | MIRA TUKU</title>
<meta name="description" content="未来学の検証から、人類学・哲学・伝統知を経て卓越人材と2100年に求められる人材像へ。NPO法人ミラツクが26のデータベースを横断して描いた21章の知の地図。">
<meta property="og:title" content="深い知が拓く2100年 | MIRA TUKU">
<meta property="og:description" content="26DBs横断、約280,000字。21章の知の地図。">
<meta property="og:type" content="article">
<link rel="icon" href="https://esse-sense.com/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700;900&family=Noto+Serif+JP:wght@300;400;500;600;700;900&family=Judson:wght@400;700&display=swap" rel="stylesheet">
<style>
:root {
  /* === Miratuku CI Palette (NOSIGNER 2011) — warm 12-tone === */
  --mt-1: #F0A671; --mt-2: #F2C792; --mt-3: #F1C189; --mt-4: #CEA26F;
  --mt-5: #F8CDAC; --mt-6: #F0BE83; --mt-7: #EFC4A4; --mt-8: #F7BEA2;
  --mt-9: #DC8766; --mt-10: #B07256; --mt-11: #966D5E; --mt-12: #7A4033;

  /* === Dark mode (default — matches journal.emerging-future.org/8-questions/) === */
  --bg: #1C1410;
  --bg-soft: #261C16;
  --bg-tint: #30251D;
  --bg-alt: #261C16;
  --card: #1C1410;
  --card-hover: #261C16;
  --ink: #FFFFFF;
  --ink-soft: #D8D5D1;
  --ink-mute: #A6A29D;
  --ink-faint: #7A7672;
  --accent: #FF3644;
  --accent-deep: #FF5560;
  --accent-soft: rgba(255, 54, 68, 0.10);
  --accent-tint: rgba(255, 54, 68, 0.22);
  --line: #3A2E22;
  --line-soft: #2A1F16;

  --serif: "Noto Serif JP", "Hiragino Mincho ProN", "Yu Mincho", Georgia, serif;
  --sans:  "Noto Sans JP", "Hiragino Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --display: "Judson", "Noto Serif JP", Georgia, serif;

  /* Aliases (legacy names used in body content) */
  --accent-warm: var(--accent);
  --accent-warm-soft: var(--accent-deep);
  --accent-muted: var(--accent-soft);
  --accent-muted-strong: var(--accent-tint);
  --text: var(--ink);
  --text-secondary: var(--ink-soft);
  --text-muted: var(--ink-mute);
  --border: var(--line);
  --border-light: var(--line-soft);
  --highlight: var(--accent);
  --surface: var(--bg-tint);
  --font: var(--sans);
  --font-serif: var(--serif);
  --font-display: var(--display);
  --green: var(--mt-10);
  --orange: var(--mt-9);
  --blue: var(--mt-12);
}

[data-theme="light"] {
  --bg: #FAF6F0;
  --bg-soft: #F2EBDD;
  --bg-tint: #E8DECB;
  --bg-alt: #F2EBDD;
  --card: #FFFFFF;
  --card-hover: #FAF6F0;
  --ink: #2A1F18;
  --ink-soft: #5A4838;
  --ink-mute: #8B7A66;
  --ink-faint: #B5A48E;
  --accent: #ED2E3B;
  --accent-deep: #C81E2B;
  --accent-soft: rgba(237,46,59,0.08);
  --accent-tint: rgba(237,46,59,0.16);
  --line: #D9CFBF;
  --line-soft: #E8E0D0;
  --highlight: #ED2E3B;
  --surface: #F2EBDD;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; scroll-behavior: smooth; -webkit-font-smoothing: antialiased; }
body {
  font-family: var(--serif);
  background: var(--bg);
  color: var(--ink);
  line-height: 1.95;
  letter-spacing: 0.025em;
  font-feature-settings: "palt";
  min-height: 100vh;
  transition: background .2s, color .2s;
}
a { color: var(--accent); text-decoration: none; transition: color .15s; }
a:hover { color: var(--accent-deep); text-decoration: none; }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; border-radius: 2px; }
::selection { background: var(--accent-tint); color: var(--ink); }

/* === Reading progress bar === */
.read-progress { position: fixed; top: 0; left: 0; right: 0; height: 3px; background: transparent; z-index: 200; pointer-events: none; }
.read-progress-bar { height: 100%; width: 0%; background: linear-gradient(90deg, var(--accent), var(--accent-deep)); transition: width .12s linear; }

/* === Top bar (kurashi-style transparent) === */
.top-bar {
  background: rgba(28, 20, 16, 0.92);
  backdrop-filter: saturate(160%) blur(10px);
  -webkit-backdrop-filter: saturate(160%) blur(10px);
  border-bottom: 1px solid var(--line);
  position: sticky; top: 0; z-index: 100;
  height: 60px;
}
[data-theme="light"] .top-bar { background: rgba(250, 246, 240, 0.92); }
.top-bar-inner {
  max-width: 1280px; margin: 0 auto; padding: 0 24px;
  height: 100%; display: flex; align-items: center; justify-content: space-between; gap: 16px;
}
.top-bar-brand {
  display: inline-flex; align-items: center; gap: 14px; text-decoration: none;
  font-family: var(--sans); font-size: 12px; font-weight: 700; letter-spacing: 0.18em;
  color: var(--ink);
}
.top-bar-brand:hover { color: var(--accent); }
.top-bar-brand small {
  display: block; font-size: 9.5px; letter-spacing: 0.14em;
  color: var(--ink-mute); font-weight: 500; margin-top: 2px;
}
.top-bar-brand-text { line-height: 1.3; }
.top-bar-actions { display: flex; align-items: center; gap: 14px; font-family: var(--sans); }
.back-link {
  color: var(--ink-soft); font-weight: 500; padding: 6px 0;
  border-bottom: 2px solid transparent; font-size: 12px; letter-spacing: 0.1em;
  transition: color .15s, border-color .15s;
}
.back-link:hover { color: var(--accent); border-bottom-color: var(--accent); }
.theme-toggle, .toc-toggle {
  background: none; border: 1px solid var(--line); color: var(--ink-mute);
  cursor: pointer; padding: 5px 12px; font-size: 10.5px;
  font-family: var(--sans); letter-spacing: 0.12em; font-weight: 700;
  transition: border-color .15s, color .15s;
}
.theme-toggle:hover, .toc-toggle:hover { border-color: var(--accent); color: var(--accent); }
.toc-toggle { display: none; }

/* === V1 link banner === */
.v1-banner {
  background: var(--bg-soft);
  border-bottom: 1px solid var(--line);
  padding: 10px 24px;
  font-family: var(--sans); font-size: 11.5px; letter-spacing: 0.06em;
  color: var(--ink-mute); text-align: center;
}
.v1-banner a {
  color: var(--ink-soft); text-decoration: underline; text-underline-offset: 3px;
  text-decoration-color: var(--line);
}
.v1-banner a:hover { color: var(--accent); text-decoration-color: var(--accent); }

/* === Hero (book cover, kurashi-editorial) === */
.book-cover {
  max-width: 760px; margin: 0 auto;
  padding: 100px 24px 80px;
  border-bottom: 1px solid var(--line);
  position: relative;
}
.book-cover-eyebrow {
  font-family: var(--sans); font-size: 11px; font-weight: 700;
  letter-spacing: 0.32em; color: var(--accent); text-transform: uppercase;
  display: flex; align-items: center; gap: 12px; margin-bottom: 28px;
}
.book-cover-eyebrow::before { content: ""; width: 32px; height: 2px; background: var(--accent); }
.book-cover-num {
  font-family: var(--display); font-size: 80px; line-height: 0.95;
  margin-bottom: 24px; letter-spacing: 0;
  display: flex; align-items: baseline; gap: 14px;
  font-weight: 700; color: var(--ink);
}
.book-cover-num-total {
  font-family: var(--display); font-size: 22px;
  color: var(--ink-mute); font-weight: 400;
}
.book-cover-title {
  font-family: var(--serif); font-weight: 700; font-size: 38px;
  line-height: 1.5; letter-spacing: 0.02em; color: var(--ink);
  margin-bottom: 16px;
}
.book-cover-title em { font-style: normal; color: var(--accent); display: inline; }
.book-cover-subtitle {
  font-family: var(--serif); font-weight: 500; font-size: 18px;
  line-height: 1.85; letter-spacing: 0.04em; color: var(--ink-soft);
  margin-bottom: 24px;
}
.book-cover-en {
  font-family: var(--display); font-size: 18px; color: var(--ink-mute);
  letter-spacing: 0.02em; margin-bottom: 32px; font-weight: 400;
}
.book-cover-lead {
  font-family: var(--serif); font-size: 16px; font-weight: 400;
  line-height: 2; color: var(--ink-soft); letter-spacing: 0.04em;
  max-width: 640px; margin-bottom: 36px;
  padding-left: 18px; border-left: 3px solid var(--accent);
}
.book-cover-meta {
  display: flex; gap: 24px; flex-wrap: wrap; align-items: center;
  font-family: var(--sans); font-size: 11.5px; letter-spacing: 0.1em;
  color: var(--ink-mute); padding-top: 24px; border-top: 1px solid var(--line);
}
.book-cover-meta strong { color: var(--ink); font-weight: 700; }
.book-cover-meta .dot { color: var(--ink-faint); }

/* === Layout === */
.book-layout {
  display: grid; grid-template-columns: 280px 1fr;
  max-width: 1240px; margin: 0 auto; padding: 0 24px; gap: 0;
  position: relative;
}
.toc-sidebar {
  position: sticky; top: 60px; height: calc(100vh - 60px);
  overflow-y: auto; padding: 40px 28px 40px 0;
  border-right: 1px solid var(--line-soft);
  scrollbar-width: thin; scrollbar-color: var(--line) transparent;
}
.toc-sidebar::-webkit-scrollbar { width: 6px; }
.toc-sidebar::-webkit-scrollbar-track { background: transparent; }
.toc-sidebar::-webkit-scrollbar-thumb { background: var(--line); border-radius: 3px; }
.toc-title {
  font-family: var(--sans); font-size: 0.7rem; font-weight: 700;
  letter-spacing: 0.22em; text-transform: uppercase;
  color: var(--accent); margin-bottom: 20px; padding-bottom: 12px;
  border-bottom: 1px solid var(--line);
  display: flex; align-items: center; gap: 12px;
}
.toc-title::before { content: ""; width: 24px; height: 2px; background: var(--accent); }
.toc-part {
  font-family: var(--sans); font-size: 0.62rem; font-weight: 700;
  letter-spacing: 0.22em; text-transform: uppercase; color: var(--ink-mute);
  margin: 24px 0 6px; padding-top: 16px;
  border-top: 1px dashed var(--line-soft);
}
.toc-part:first-of-type { padding-top: 0; border-top: none; }
.toc-part-title {
  font-family: var(--serif); font-size: 0.78rem; font-weight: 500;
  color: var(--ink-soft); margin-bottom: 10px; line-height: 1.5;
}
.toc-list { list-style: none; }
.toc-list li { margin: 4px 0; }
.toc-list a {
  display: flex; align-items: flex-start; gap: 8px;
  color: var(--ink-soft); font-family: var(--serif); font-size: 0.82rem;
  line-height: 1.55; padding: 6px 10px; border-left: 2px solid transparent;
  transition: all 0.15s; min-height: 36px;
}
.toc-list a:hover { color: var(--accent); border-left-color: var(--accent); background: var(--accent-soft); text-decoration: none; }
.toc-list a.active { color: var(--accent); border-left-color: var(--accent); font-weight: 500; background: var(--accent-soft); }
.toc-list .toc-num {
  display: inline-block; min-width: 28px; flex-shrink: 0;
  font-family: var(--display); font-size: 0.85rem; font-weight: 700;
  color: var(--ink-mute); line-height: 1.55;
}
.toc-list a.active .toc-num { color: var(--accent); }

/* === Main === */
.book-main { padding: 56px 0 80px 56px; max-width: 760px; }
.chapter-section {
  margin-bottom: 80px; padding-bottom: 64px;
  border-bottom: 1px solid var(--line-soft);
  scroll-margin-top: 80px;
}
.chapter-section:last-child { border-bottom: none; }
.chapter-meta {
  display: flex; flex-wrap: wrap; gap: 16px;
  font-family: var(--sans); font-size: 0.72rem; letter-spacing: 0.12em;
  color: var(--ink-mute); margin-bottom: 14px; align-items: center;
}
.chapter-meta .read-time {
  display: inline-flex; align-items: center; gap: 6px; color: var(--ink-soft);
}
.chapter-meta .read-time::before {
  content: ""; width: 6px; height: 6px; border-radius: 50%; background: var(--accent);
}
.chapter-number-label {
  font-family: var(--sans); font-size: 0.72rem; font-weight: 700;
  letter-spacing: 0.22em; color: var(--accent); text-transform: uppercase;
  display: inline-flex; align-items: center; gap: 12px;
}
.chapter-number-label::before { content: ""; width: 24px; height: 2px; background: var(--accent); }
.chapter-title {
  font-family: var(--serif); font-size: 2rem; font-weight: 700;
  line-height: 1.5; letter-spacing: 0.015em; color: var(--ink); margin-bottom: 36px;
}

.article-h2 {
  font-family: var(--serif); font-size: 1.35rem; font-weight: 700;
  line-height: 1.55; letter-spacing: 0.01em; color: var(--ink);
  margin: 64px 0 22px; padding-top: 24px;
  border-top: 2px solid var(--accent);
  display: inline-block; min-width: 60%;
}
.article-h3 {
  font-family: var(--serif); font-size: 1.1rem; font-weight: 700;
  line-height: 1.55; color: var(--ink); margin: 40px 0 14px;
  padding-left: 14px; border-left: 3px solid var(--accent);
}
.book-main p {
  font-family: var(--serif); font-size: 1.02rem; line-height: 2;
  letter-spacing: 0.04em; color: var(--ink); margin-bottom: 1.4em;
  text-indent: 1em;
}
.book-main p.no-indent, .book-main p:first-of-type { text-indent: 0; }
.book-main p strong { font-weight: 700; color: var(--accent); }
.book-main blockquote {
  font-family: var(--serif); font-style: italic; color: var(--ink-soft);
  border-left: 3px solid var(--accent); padding: 14px 26px; margin: 28px 0;
  background: var(--accent-soft);
}

.epigraph, .literary-opening {
  font-family: var(--serif); font-style: italic; color: var(--ink-soft);
  border-left: 3px solid var(--accent); padding: 22px 28px;
  margin: 32px 0 36px; background: var(--accent-soft);
  line-height: 1.95; font-size: 0.98rem;
}
.epigraph p, .literary-opening p {
  font-family: var(--serif); margin-bottom: 8px; line-height: 1.85; text-indent: 0;
}
.epigraph .attribution, .literary-opening .attribution {
  font-family: var(--sans); font-size: 0.78rem; font-style: normal;
  color: var(--ink-mute); letter-spacing: 0.06em;
}

.col-end {
  background: var(--bg-soft); border-top: 1px solid var(--accent);
  padding: 28px; margin-top: 48px; font-family: var(--serif);
}
.pullquote {
  font-family: var(--serif); font-size: 1.18rem; font-weight: 600;
  color: var(--accent); border-left: 4px solid var(--accent);
  padding: 18px 26px; margin: 36px 0; background: var(--accent-soft);
  line-height: 1.75; text-indent: 0;
}
.table-clean {
  width: 100%; border-collapse: collapse; margin: 24px 0;
  font-family: var(--sans); font-size: 0.86rem; color: var(--ink);
}
.table-clean th {
  background: var(--bg-soft); padding: 12px;
  text-align: left; border-bottom: 2px solid var(--accent);
  color: var(--ink); font-weight: 700;
}
.table-clean td {
  padding: 10px 12px; border-bottom: 1px solid var(--line-soft);
}
.finding-box {
  background: var(--bg-soft); border-left: 4px solid var(--accent);
  padding: 20px 24px; margin: 28px 0; font-family: var(--serif);
}

/* === Drop cap on intro first paragraph === */
#intro > p:not(.epigraph):not(.literary-opening):not([class*="literary-opening"]):first-of-type::first-letter,
#intro p.drop-cap::first-letter {
  font-family: var(--display); font-weight: 700;
  font-size: 4.4em; float: left; line-height: 0.92;
  margin: 0.06em 0.14em 0 0; color: var(--ink);
}

/* === Figure card (SVG editorial inserts) === */
figure {
  margin: 36px 0;
  background: #FFFFFF;
  border: 1px solid var(--line);
  border-radius: 2px;
  padding: 28px 24px 22px;
  box-shadow: 0 4px 18px rgba(0,0,0,0.18);
}
[data-theme="light"] figure { background: #FFFFFF; box-shadow: 0 2px 10px rgba(122, 64, 51, 0.08); }
figure svg { display: block; margin: 0 auto; }
figure figcaption {
  font-family: var(--sans) !important; font-size: 0.82rem !important;
  color: #555 !important; margin-top: 16px !important;
  letter-spacing: 0.04em !important; text-align: center;
  border-top: 1px dashed #D9D9D9; padding-top: 12px;
}

/* === Chapter prev/next nav === */
.chapter-nav {
  display: grid; grid-template-columns: 1fr 1fr; gap: 12px;
  margin: 64px 0 0; padding-top: 32px; border-top: 1px solid var(--line);
}
.chapter-nav a {
  display: flex; flex-direction: column; gap: 4px;
  padding: 16px 18px; border: 1px solid var(--line);
  background: var(--bg-soft); transition: border-color .15s, background .15s;
  text-decoration: none;
}
.chapter-nav a:hover { border-color: var(--accent); background: var(--accent-soft); text-decoration: none; }
.chapter-nav .nav-label {
  font-family: var(--sans); font-size: 0.7rem; letter-spacing: 0.16em;
  color: var(--ink-mute); text-transform: uppercase;
}
.chapter-nav .nav-title {
  font-family: var(--serif); font-size: 0.92rem; font-weight: 500;
  color: var(--ink-soft); line-height: 1.5;
}
.chapter-nav a:hover .nav-label { color: var(--accent); }
.chapter-nav a:hover .nav-title { color: var(--ink); }
.chapter-nav .nav-prev { text-align: left; }
.chapter-nav .nav-next { text-align: right; align-items: flex-end; }
.chapter-nav .nav-empty { background: transparent; border-color: transparent; pointer-events: none; }

/* === Scroll to top button === */
.scroll-top {
  position: fixed; bottom: 24px; right: 24px;
  width: 44px; height: 44px;
  background: var(--accent); color: var(--bg);
  border: none; border-radius: 50%; cursor: pointer;
  font-family: var(--sans); font-size: 18px; font-weight: 700;
  display: none; align-items: center; justify-content: center;
  box-shadow: 0 4px 14px rgba(0,0,0,0.3); z-index: 90;
  transition: background .15s, transform .15s;
}
.scroll-top:hover { background: var(--accent-deep); transform: translateY(-2px); }
.scroll-top.visible { display: flex; }

/* === Mobile TOC drawer overlay === */
.toc-overlay {
  display: none; position: fixed; inset: 0;
  background: rgba(0,0,0,0.6); z-index: 150;
  opacity: 0; transition: opacity .2s;
}
.toc-overlay.open { display: block; opacity: 1; }

/* === Print === */
@media print {
  .top-bar, .v1-banner, .toc-sidebar, .scroll-top, .chapter-nav, .toc-overlay, .read-progress { display: none; }
  .book-layout { grid-template-columns: 1fr; padding: 0; }
  .book-main { padding: 0; max-width: none; }
  body { background: #fff; color: #000; }
  figure { box-shadow: none; border: 1px solid #ccc; page-break-inside: avoid; }
}

/* === Tablet === */
@media (max-width: 1100px) {
  .book-layout { grid-template-columns: 240px 1fr; }
  .toc-sidebar { padding: 32px 20px 32px 0; }
  .book-main { padding: 48px 0 64px 36px; max-width: none; }
}

/* === Mobile === */
@media (max-width: 760px) {
  html { font-size: 15px; }
  .top-bar { height: 56px; }
  .top-bar-inner { padding: 0 16px; }
  .top-bar-brand { font-size: 11px; gap: 10px; }
  .top-bar-brand small { display: none; }
  .top-bar-actions { gap: 8px; }
  .back-link { font-size: 11px; }
  .theme-toggle { padding: 6px 10px; font-size: 10px; }
  .toc-toggle { display: inline-block; padding: 6px 10px; font-size: 10px; }
  .v1-banner { font-size: 10.5px; padding: 8px 16px; }

  .book-cover { padding: 64px 20px 56px; }
  .book-cover-num { font-size: 56px; }
  .book-cover-title { font-size: 26px; line-height: 1.5; }
  .book-cover-subtitle { font-size: 15.5px; }
  .book-cover-lead { font-size: 14.5px; padding-left: 14px; }
  .book-cover-meta { font-size: 10.5px; gap: 12px; }

  .book-layout { grid-template-columns: 1fr; padding: 0 16px; }
  .toc-sidebar {
    position: fixed; top: 0; left: 0; bottom: 0;
    width: 86%; max-width: 320px; height: 100vh;
    background: var(--bg); border-right: 1px solid var(--line);
    padding: 24px 20px; overflow-y: auto;
    transform: translateX(-100%); transition: transform .25s;
    z-index: 160;
  }
  .toc-sidebar.open { transform: translateX(0); box-shadow: 8px 0 32px rgba(0,0,0,0.4); }
  .book-main { padding: 32px 0 120px 0; }

  .chapter-title { font-size: 1.6rem; line-height: 1.55; }
  .article-h2 { font-size: 1.15rem; min-width: 100%; }
  .article-h3 { font-size: 1rem; }
  .book-main p { font-size: 0.98rem; line-height: 1.95; letter-spacing: 0.03em; }
  .pullquote { font-size: 1.05rem; padding: 16px 18px; }
  .epigraph, .literary-opening { padding: 18px 20px; font-size: 0.94rem; }
  figure { padding: 18px 14px 14px; margin: 28px -8px; }
  .table-clean { font-size: 0.78rem; }
  .table-clean th, .table-clean td { padding: 8px 6px; }

  .chapter-nav { grid-template-columns: 1fr; gap: 8px; padding-top: 24px; }
  .chapter-nav .nav-empty { display: none; }
  .scroll-top { bottom: 76px; right: 16px; width: 40px; height: 40px; }
}

/* Read more affordance for very small screens */
@media (max-width: 380px) {
  .book-cover-title { font-size: 22px; }
  .book-cover-num { font-size: 44px; }
}
</style>
</head>
<body>
<div class="read-progress" aria-hidden="true"><div class="read-progress-bar"></div></div>
<header class="top-bar">
  <div class="top-bar-inner">
    <a href="https://journal.emerging-future.org/" class="top-bar-brand" aria-label="MIRA TUKU journal">
      <span class="top-bar-brand-text">MIRA TUKU<small>journal · deep knowledge</small></span>
    </a>
    <div class="top-bar-actions">
      <button class="toc-toggle" onclick="toggleTOC()" aria-label="目次を開く">目次</button>
      <a href="https://journal.emerging-future.org/" class="back-link">← journal</a>
      <button class="theme-toggle" onclick="toggleTheme()" aria-label="ダーク/ライト切替">DARK / LIGHT</button>
    </div>
  </div>
</header>
<div class="v1-banner">
  これは新版（v2）です。<a href="https://yuyanishimura0312.github.io/miratuku-news-v2/reports/deep-knowledge-book.html">初版（v1）を読む →</a>
</div>
<section class="book-cover">
  <div class="book-cover-eyebrow">DEEP KNOWLEDGE BOOK · 2026.05</div>
  <div class="book-cover-num">11<span class="book-cover-num-total">/ case 11</span></div>
  <h1 class="book-cover-title">deep knowledge<br><em>—</em> 深い知が拓く2100年</h1>
  <div class="book-cover-en">A book of deep knowledge for the year 2100.</div>
  <p class="book-cover-subtitle">未来学の検証から、人類学・哲学・伝統知を経て<br>卓越人材と2100年に求められる人材像へ</p>
  <p class="book-cover-lead">「浅い知の海」のなかで、なお求められる「深い知」の輪郭を描く試み。NPO法人ミラツクが26のデータベースを横断して描いた、21章の知の地図。</p>
  <div class="book-cover-meta">
    <span><strong>21章</strong>（序＋四部19章＋終）</span><span class="dot">·</span>
    <span>約<strong>280,000字</strong></span><span class="dot">·</span>
    <span><strong>26DBs</strong> 横断</span><span class="dot">·</span>
    <span>case 11</span>
  </div>
</section>
<div class="toc-overlay" onclick="closeTOC()"></div>
<div class="book-layout"><aside class="toc-sidebar" id="toc-sidebar">'''

# Replace from <!DOCTYPE to <aside class="toc-sidebar">
content = re.sub(
    r'^<!DOCTYPE.*?<aside class="toc-sidebar">',
    NEW_HEAD,
    content,
    count=1,
    flags=re.DOTALL,
)

# ---- Step 2: Replace closing script ----
NEW_SCRIPT = '''  <script>
    // === Theme toggle ===
    function toggleTheme() {
      const html = document.documentElement;
      const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('dkb-v2-theme', next);
    }

    // === Mobile TOC drawer ===
    function toggleTOC() {
      const toc = document.getElementById('toc-sidebar');
      const ovl = document.querySelector('.toc-overlay');
      const open = toc.classList.toggle('open');
      ovl.classList.toggle('open', open);
      document.body.style.overflow = open ? 'hidden' : '';
    }
    function closeTOC() {
      document.getElementById('toc-sidebar').classList.remove('open');
      document.querySelector('.toc-overlay').classList.remove('open');
      document.body.style.overflow = '';
    }

    document.addEventListener('DOMContentLoaded', () => {
      // Restore theme
      const saved = localStorage.getItem('dkb-v2-theme');
      if (saved) document.documentElement.setAttribute('data-theme', saved);

      // Reading progress bar
      const progressBar = document.querySelector('.read-progress-bar');
      const updateProgress = () => {
        const h = document.documentElement;
        const total = h.scrollHeight - h.clientHeight;
        const pct = total > 0 ? (h.scrollTop / total) * 100 : 0;
        progressBar.style.width = pct + '%';
      };
      window.addEventListener('scroll', updateProgress, { passive: true });
      updateProgress();

      // Scroll to top button
      const scrollBtn = document.createElement('button');
      scrollBtn.className = 'scroll-top';
      scrollBtn.setAttribute('aria-label', 'ページ上部へ');
      scrollBtn.innerHTML = '↑';
      scrollBtn.onclick = () => window.scrollTo({ top: 0, behavior: 'smooth' });
      document.body.appendChild(scrollBtn);
      window.addEventListener('scroll', () => {
        scrollBtn.classList.toggle('visible', window.scrollY > 600);
      }, { passive: true });

      // TOC scroll-spy
      const links = document.querySelectorAll('.toc-list a');
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const id = entry.target.id;
            links.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + id));
          }
        });
      }, { rootMargin: '-15% 0px -75% 0px' });
      document.querySelectorAll('.chapter-section').forEach(s => observer.observe(s));

      // Close TOC on link click (mobile)
      links.forEach(a => a.addEventListener('click', () => {
        if (window.innerWidth <= 760) closeTOC();
      }));

      // Close TOC with Esc
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeTOC();
      });
    });
  </script>
</body>
</html>'''

content = re.sub(
    r'<script>.*?</script>\s*</body>\s*</html>\s*$',
    NEW_SCRIPT,
    content,
    count=1,
    flags=re.DOTALL,
)

# ---- Step 3: Recolor SVGs (#CC1400 -> #FF3644 + rgba) ----
content = re.sub(r'#CC1400\b', '#FF3644', content)
content = re.sub(r'#cc1400\b', '#ff3644', content)
content = re.sub(r'rgba\(204,\s*20,\s*0,\s*([0-9.]+)\)', r'rgba(255,54,68,\1)', content)
# Light-mode accent variant in inline styles
content = re.sub(r'#B01200\b', '#C81E2B', content)

# Recolor green/orange/blue in case some chapters use them
content = re.sub(r'fill="#2[eE]7[dD]32"', 'fill="#B07256"', content)
content = re.sub(r'stroke="#2[eE]7[dD]32"', 'stroke="#B07256"', content)
content = re.sub(r'fill="#[eE]65100"', 'fill="#DC8766"', content)
content = re.sub(r'stroke="#[eE]65100"', 'stroke="#DC8766"', content)
content = re.sub(r'fill="#1565[cC]0"', 'fill="#7A4033"', content)
content = re.sub(r'stroke="#1565[cC]0"', 'stroke="#7A4033"', content)

# ---- Step 4: Insert prev/next chapter navigation ----
def make_nav(prev_id, prev_title, next_id, next_title):
    parts = ['<nav class="chapter-nav" aria-label="章ナビゲーション">']
    if prev_id:
        parts.append(
            f'<a class="nav-prev" href="#{prev_id}">'
            f'<span class="nav-label">← 前の章</span>'
            f'<span class="nav-title">{prev_title}</span></a>'
        )
    else:
        parts.append('<span class="nav-empty"></span>')
    if next_id:
        parts.append(
            f'<a class="nav-next" href="#{next_id}">'
            f'<span class="nav-label">次の章 →</span>'
            f'<span class="nav-title">{next_title}</span></a>'
        )
    else:
        parts.append('<span class="nav-empty"></span>')
    parts.append('</nav>')
    return '\n'.join(parts)

# For each chapter, find its closing and inject nav before next chapter starts.
# Strategy: split on `<section class="chapter-section" id="...">` and inject nav at end of each.
ch_ids = [c[0] for c in CHAPTERS]
ch_titles = dict(CHAPTERS)

# Find each chapter section and the next one's start, then inject nav before </section>
# We'll iterate from the last chapter backwards to keep offsets stable.
for i in range(len(CHAPTERS) - 1, -1, -1):
    cid, title = CHAPTERS[i]
    prev_cid = CHAPTERS[i-1][0] if i > 0 else None
    prev_title = CHAPTERS[i-1][1] if i > 0 else None
    next_cid = CHAPTERS[i+1][0] if i < len(CHAPTERS) - 1 else None
    next_title = CHAPTERS[i+1][1] if i < len(CHAPTERS) - 1 else None

    nav_html = make_nav(prev_cid, prev_title, next_cid, next_title)

    # Find the end of this chapter: it's the last </section> before the next chapter,
    # or the final </section> in document if it's the last chapter.
    open_pat = re.compile(rf'<section class="chapter-section" id="{cid}">')
    open_match = open_pat.search(content)
    if not open_match:
        print(f"[WARN] Could not find chapter id={cid}")
        continue
    open_pos = open_match.start()

    # Find the start of next chapter or end of last </section> for the final chapter
    if next_cid:
        next_open = re.search(rf'<section class="chapter-section" id="{next_cid}">', content)
        if not next_open:
            print(f"[WARN] Could not find next chapter id={next_cid}")
            continue
        # Find last </section> before next_open
        section_end_pat = re.compile(r'</section>')
        last_end = None
        for m in section_end_pat.finditer(content, open_pos, next_open.start()):
            last_end = m
        if not last_end:
            print(f"[WARN] No </section> found in chapter {cid}")
            continue
        # Insert nav before this </section>
        insert_pos = last_end.start()
        content = content[:insert_pos] + nav_html + '\n' + content[insert_pos:]
    else:
        # Final chapter: nav before final </section> before </main>
        main_close = re.search(r'</main>', content)
        if not main_close:
            print(f"[WARN] No </main> found")
            continue
        # Find last </section> before </main>
        last_end = None
        for m in re.finditer(r'</section>', content, flags=0):
            if m.start() < main_close.start():
                last_end = m
        if not last_end:
            continue
        insert_pos = last_end.start()
        content = content[:insert_pos] + nav_html + '\n' + content[insert_pos:]

# ---- Step 5: Add chapter-meta with read time after each chapter-number-label ----
# Estimate read time per chapter (rough: chars / 600 chars per minute for Japanese)
# We'll calculate per chapter by extracting text between section opens.
def estimate_read_time(text):
    # Rough char count, strip HTML tags
    plain = re.sub(r'<[^>]+>', '', text)
    plain = re.sub(r'\s+', '', plain)
    chars = len(plain)
    minutes = max(2, round(chars / 600))
    return minutes

# Find each chapter and prepend a chapter-meta line containing read time
for cid, _title in CHAPTERS:
    section_re = re.compile(
        rf'(<section class="chapter-section" id="{cid}">)(.*?)(</section>)',
        flags=re.DOTALL,
    )
    m = section_re.search(content)
    if not m:
        continue
    inner = m.group(2)
    minutes = estimate_read_time(inner)
    # Insert chapter-meta right after first <div class="chapter-number-label"...>...</div>
    meta_html = f'<div class="chapter-meta"><span class="read-time">約{minutes}分</span></div>'
    new_inner, n = re.subn(
        r'(<div class="chapter-number-label">[^<]*</div>)',
        rf'\1\n{meta_html}',
        inner,
        count=1,
    )
    if n:
        content = content[:m.start()] + m.group(1) + new_inner + m.group(3) + content[m.end():]

# Write output
DST.write_text(content, encoding="utf-8")
print(f"Written: {DST}")
print(f"Size: {DST.stat().st_size:,} bytes")
print(f"Lines: {len(content.splitlines()):,}")
