#!/usr/bin/env python3
"""
Build mg-textbook.html from 20 Markdown chapter files.
"""

import re
import os
import html

CHAPTERS_DIR = "/Users/nishimura+/projects/research/miratuku-news-v2/mg-textbook/chapters"
OUTPUT_FILE = "/Users/nishimura+/projects/research/miratuku-news-v2/book/mg-textbook.html"


def md_to_html(text):
    """Convert markdown text to HTML (basic conversion)."""
    lines = text.split('\n')
    output = []
    in_table = False
    table_lines = []
    in_list = False
    list_items = []
    list_type = None
    paragraph_lines = []
    in_code = False

    def flush_paragraph():
        if paragraph_lines:
            content = ' '.join(paragraph_lines).strip()
            if content:
                output.append(f'<p>{process_inline(content)}</p>')
            paragraph_lines.clear()

    def flush_list():
        nonlocal in_list, list_type
        if list_items:
            tag = list_type or 'ul'
            output.append(f'<{tag}>')
            for item in list_items:
                output.append(f'  <li>{process_inline(item)}</li>')
            output.append(f'</{tag}>')
            list_items.clear()
        in_list = False
        list_type = None

    def flush_table():
        nonlocal in_table
        if table_lines:
            output.append('<table>')
            is_header = True
            for tl in table_lines:
                # Skip separator rows (e.g., |---|---|)
                if re.match(r'^\s*\|[\s\-:|]+\|\s*$', tl):
                    is_header = False
                    continue
                cells = [c.strip() for c in tl.strip().strip('|').split('|')]
                if is_header:
                    output.append('<thead><tr>')
                    for c in cells:
                        output.append(f'  <th>{process_inline(c)}</th>')
                    output.append('</tr></thead><tbody>')
                    is_header = False
                else:
                    output.append('<tr>')
                    for c in cells:
                        output.append(f'  <td>{process_inline(c)}</td>')
                    output.append('</tr>')
            output.append('</tbody></table>')
            table_lines.clear()
        in_table = False

    i = 0
    while i < len(lines):
        line = lines[i]

        # Code block
        if line.strip().startswith('```'):
            flush_paragraph()
            flush_list()
            if not in_code:
                in_code = True
                output.append('<pre><code>')
            else:
                in_code = False
                output.append('</code></pre>')
            i += 1
            continue

        if in_code:
            output.append(html.escape(line))
            i += 1
            continue

        # Table detection
        if line.strip().startswith('|'):
            flush_paragraph()
            flush_list()
            in_table = True
            table_lines.append(line)
            i += 1
            continue
        elif in_table:
            flush_table()

        # Horizontal rule
        if re.match(r'^\s*---+\s*$', line):
            flush_paragraph()
            flush_list()
            output.append('<hr class="chapter-divider">')
            i += 1
            continue

        # Headings (skip h1 — handled separately as chapter title)
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            flush_paragraph()
            flush_list()
            level = len(m.group(1))
            heading_text = m.group(2).strip()
            if level == 1:
                # Chapter title — already handled in outer loop
                output.append(f'<h2 class="chapter-title">{process_inline(heading_text)}</h2>')
            elif level == 2:
                output.append(f'<h3 class="section-heading">{process_inline(heading_text)}</h3>')
            elif level == 3:
                output.append(f'<h4 class="subsection-heading">{process_inline(heading_text)}</h4>')
            else:
                output.append(f'<h5>{process_inline(heading_text)}</h5>')
            i += 1
            continue

        # Ordered list
        m = re.match(r'^\d+\.\s+(.*)', line)
        if m:
            flush_paragraph()
            if not in_list or list_type != 'ol':
                flush_list()
                in_list = True
                list_type = 'ol'
            list_items.append(m.group(1))
            i += 1
            continue

        # Unordered list
        m = re.match(r'^[-*+]\s+(.*)', line)
        if m:
            flush_paragraph()
            if not in_list or list_type != 'ul':
                flush_list()
                in_list = True
                list_type = 'ul'
            list_items.append(m.group(1))
            i += 1
            continue

        # Blockquote
        if line.strip().startswith('>'):
            flush_paragraph()
            flush_list()
            content = re.sub(r'^>\s?', '', line.strip())
            output.append(f'<blockquote><p>{process_inline(content)}</p></blockquote>')
            i += 1
            continue

        # Empty line
        if line.strip() == '':
            flush_paragraph()
            flush_list()
            i += 1
            continue

        # Regular paragraph line
        flush_list()
        paragraph_lines.append(line.strip())
        i += 1

    flush_paragraph()
    flush_list()
    if in_table:
        flush_table()

    return '\n'.join(output)


def process_inline(text):
    """Process inline markdown: bold, italic, code, concept IDs."""
    # Escape HTML first — but we want to preserve any existing entities
    # Don't double-escape; process raw text
    # Bold + italic
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    # Bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Links [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Concept IDs [mXXXX] — styled in red monospace
    text = re.sub(r'\[m(\d+)\]', r'<span class="concept-id">[m\1]</span>', text)
    return text


def extract_chapter_title(md_text):
    """Extract the first H1 heading as chapter title."""
    m = re.match(r'^#\s+(.+)', md_text.strip(), re.MULTILINE)
    if m:
        return m.group(1).strip()
    return "章"


def read_chapter(filepath):
    """Read a chapter file and return (title, html_body)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    title = extract_chapter_title(content)
    # Remove the H1 title line so it's not duplicated
    content_without_h1 = re.sub(r'^#\s+.+\n', '', content.strip(), count=1)
    body_html = md_to_html(content_without_h1)
    return title, body_html


# Chapter titles for TOC (extracted from files)
def build_html():
    chapters = []
    for n in range(1, 21):
        filename = f"ch{n:02d}.md"
        filepath = os.path.join(CHAPTERS_DIR, filename)
        title, body = read_chapter(filepath)
        chapters.append({
            'num': n,
            'id': f'chapter-{n:02d}',
            'title': title,
            'body': body,
        })

    # Build TOC
    toc_items = []
    for ch in chapters:
        toc_items.append(
            f'<li><a href="#{ch["id"]}">'
            f'<span class="toc-num">{ch["num"]:02d}</span> {ch["title"]}'
            f'</a></li>'
        )
    toc_html = '\n        '.join(toc_items)

    # Build chapter sections
    sections = []
    for ch in chapters:
        sections.append(f'''
  <section id="{ch["id"]}" class="chapter-section">
    <div class="chapter-number-label">Chapter {ch["num"]:02d}</div>
    <h2 class="chapter-title">{ch["title"]}</h2>
    {ch["body"]}
  </section>''')
    sections_html = '\n'.join(sections)

    html_content = f'''<!DOCTYPE html>
<html lang="ja" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>経営の知的地図 | Insight News</title>
  <link rel="icon" href="https://esse-sense.com/favicon.ico">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Noto+Serif+JP:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #FFFFFF;
      --card: #FFFFFF;
      --card-hover: #F7F7F5;
      --accent: #121212;
      --accent-soft: #555555;
      --accent-light: #F7F7F5;
      --accent-warm: #CC1400;
      --accent-muted: rgba(204,20,0,0.06);
      --text: #121212;
      --text-secondary: #555555;
      --text-muted: #6B6B6B;
      --border: #D9D9D9;
      --border-light: #EEEEEE;
      --highlight: #CC1400;
      --surface: #F7F7F5;
      --font: "Noto Sans JP", "Hiragino Sans", -apple-system, sans-serif;
      --font-serif: "Noto Serif JP", "Hiragino Mincho ProN", Georgia, serif;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.05);
      --shadow-md: 0 2px 8px rgba(0,0,0,0.08);
    }}

    [data-theme="dark"] {{
      --bg: #121212;
      --card: #1A1A1A;
      --card-hover: #222222;
      --accent: #E0E0E0;
      --accent-soft: #999999;
      --accent-warm: #FF4444;
      --accent-light: #1A1A1A;
      --text: #E0E0E0;
      --text-secondary: #AAAAAA;
      --text-muted: #8A8A8A;
      --border: #333333;
      --border-light: #2A2A2A;
      --highlight: #FF4444;
      --surface: #1A1A1A;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
      --shadow-md: 0 2px 8px rgba(0,0,0,0.4);
    }}

    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ font-size: 16px; scroll-behavior: smooth; -webkit-font-smoothing: antialiased; }}

    body {{
      font-family: var(--font-serif);
      color: var(--text);
      background: var(--bg);
      line-height: 1.9;
      letter-spacing: 0.02em;
      font-feature-settings: "palt";
      min-height: 100vh;
      transition: background 0.2s, color 0.2s;
    }}

    a {{ color: var(--accent-warm); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}

    .top-bar {{
      background: var(--bg);
      border-top: 3px solid var(--accent);
      border-bottom: 1px solid var(--border);
      padding: 0 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 48px;
      position: sticky;
      top: 0;
      z-index: 100;
    }}
    .top-bar-brand {{
      font-family: var(--font);
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--text-muted);
    }}
    .top-bar-brand span {{ color: var(--accent-warm); }}
    .top-bar-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .back-link {{
      font-family: var(--font);
      font-size: 0.75rem;
      color: var(--text-muted);
      text-decoration: none;
    }}
    .back-link:hover {{ color: var(--accent-warm); text-decoration: none; }}
    .theme-toggle {{
      background: none;
      border: 1px solid var(--border);
      color: var(--text-muted);
      cursor: pointer;
      padding: 4px 10px;
      font-size: 0.72rem;
      font-family: var(--font);
      letter-spacing: 0.05em;
      transition: all 0.2s;
    }}
    .theme-toggle:hover {{ border-color: var(--accent-warm); color: var(--accent-warm); }}

    .book-layout {{
      display: grid;
      grid-template-columns: 220px 1fr;
      max-width: 1100px;
      margin: 0 auto;
      padding: 0 24px;
      gap: 0;
    }}

    .toc-sidebar {{
      position: sticky;
      top: 48px;
      height: calc(100vh - 48px);
      overflow-y: auto;
      padding: 40px 24px 40px 0;
      border-right: 1px solid var(--border-light);
    }}
    .toc-sidebar::-webkit-scrollbar {{ width: 4px; }}
    .toc-sidebar::-webkit-scrollbar-thumb {{ background: var(--border); }}
    .toc-label {{
      font-family: var(--font);
      font-size: 0.65rem;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--text-muted);
      margin-bottom: 16px;
    }}
    .toc-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}
    .toc-list li a {{
      display: flex;
      align-items: baseline;
      gap: 8px;
      font-family: var(--font);
      font-size: 0.72rem;
      color: var(--text-secondary);
      padding: 5px 8px 5px 0;
      transition: color 0.15s;
      line-height: 1.4;
    }}
    .toc-list li a:hover {{ color: var(--accent-warm); text-decoration: none; }}
    .toc-num {{
      font-family: "SF Mono", "Fira Code", monospace;
      font-size: 0.65rem;
      color: var(--accent-warm);
      min-width: 20px;
      flex-shrink: 0;
    }}

    .book-main {{
      padding: 60px 0 100px 48px;
      max-width: 740px;
    }}

    .book-header {{
      margin-bottom: 64px;
      padding-bottom: 48px;
      border-bottom: 1px solid var(--border);
    }}
    .book-db-tags {{
      display: flex;
      gap: 8px;
      margin-bottom: 24px;
      flex-wrap: wrap;
    }}
    .db-tag {{
      font-family: var(--font);
      font-size: 0.65rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      padding: 3px 8px;
      border: 1px solid var(--border);
      color: var(--text-muted);
    }}
    .db-tag.primary {{ border-color: var(--accent-warm); color: var(--accent-warm); }}
    .book-title {{
      font-family: var(--font-serif);
      font-size: 2rem;
      font-weight: 700;
      line-height: 1.4;
      letter-spacing: 0.03em;
      color: var(--text);
      margin-bottom: 16px;
    }}
    .book-subtitle {{
      font-family: var(--font);
      font-size: 0.88rem;
      color: var(--text-secondary);
      line-height: 1.7;
      margin-bottom: 28px;
      font-weight: 400;
    }}
    .book-meta {{
      display: flex;
      gap: 24px;
      align-items: center;
      flex-wrap: wrap;
    }}
    .book-author {{
      font-family: var(--font);
      font-size: 0.82rem;
      color: var(--text);
      font-weight: 500;
    }}
    .book-date {{
      font-family: var(--font);
      font-size: 0.78rem;
      color: var(--text-muted);
    }}
    .book-metrics {{
      display: flex;
      gap: 20px;
      margin-top: 24px;
      flex-wrap: wrap;
    }}
    .metric-item {{
      font-family: var(--font);
      font-size: 0.75rem;
      color: var(--text-muted);
    }}
    .metric-item strong {{ color: var(--text); font-weight: 600; }}

    .chapter-section {{
      margin-bottom: 80px;
      padding-bottom: 60px;
      border-bottom: 1px solid var(--border-light);
    }}
    .chapter-section:last-child {{ border-bottom: none; }}
    .chapter-number-label {{
      font-family: var(--font);
      font-size: 0.65rem;
      font-weight: 700;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--accent-warm);
      margin-bottom: 12px;
    }}
    .chapter-title {{
      font-family: var(--font-serif);
      font-size: 1.5rem;
      font-weight: 700;
      line-height: 1.5;
      letter-spacing: 0.02em;
      color: var(--text);
      margin-bottom: 36px;
      padding-bottom: 16px;
      border-bottom: 2px solid var(--accent-warm);
    }}
    .section-heading {{
      font-family: var(--font-serif);
      font-size: 1.08rem;
      font-weight: 600;
      color: var(--text);
      margin: 40px 0 16px;
      line-height: 1.6;
      letter-spacing: 0.02em;
    }}
    .subsection-heading {{
      font-family: var(--font);
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--text-secondary);
      margin: 28px 0 12px;
      letter-spacing: 0.03em;
    }}

    p {{
      font-size: 0.92rem;
      line-height: 1.9;
      text-align: justify;
      margin-bottom: 1.2em;
      color: var(--text);
    }}
    strong {{ font-weight: 700; }}
    em {{ font-style: italic; }}

    ul, ol {{
      font-size: 0.92rem;
      padding-left: 1.8em;
      margin-bottom: 1.2em;
      line-height: 1.9;
    }}
    li {{ margin-bottom: 4px; }}

    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 24px 0;
      font-size: 0.85rem;
    }}
    th {{
      background: var(--surface);
      font-family: var(--font);
      font-weight: 600;
      font-size: 0.78rem;
      padding: 10px 14px;
      border: 1px solid var(--border);
      text-align: left;
      letter-spacing: 0.03em;
    }}
    td {{
      padding: 10px 14px;
      border: 1px solid var(--border-light);
      vertical-align: top;
    }}
    tr:nth-child(even) td {{ background: var(--surface); }}

    blockquote {{
      border-left: 3px solid var(--border);
      padding: 12px 20px;
      margin: 20px 0;
      color: var(--text-secondary);
      font-style: italic;
      font-size: 0.9rem;
    }}

    .epigraph {{
      font-style: italic;
      font-size: 0.9rem;
      color: var(--text-muted);
      border-left: 3px solid var(--accent-warm);
      padding: 12px 20px;
      margin: 24px 0 32px;
      line-height: 1.7;
    }}
    .epigraph .attribution {{
      display: block;
      margin-top: 8px;
      font-style: normal;
      font-size: 0.78rem;
      color: var(--text-muted);
    }}

    .callout, .callout-person, .callout-concept, .callout-case, .callout-data {{
      background: var(--surface);
      border-left: 3px solid var(--accent-warm);
      padding: 16px 20px;
      margin: 24px 0;
    }}
    .callout-label {{
      font-family: var(--font);
      font-size: 0.65rem;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--accent-warm);
      margin-bottom: 8px;
    }}
    .callout p, .callout-person p, .callout-concept p, .callout-case p, .callout-data p {{
      font-size: 0.88rem;
      margin-bottom: 0.6em;
    }}
    .callout p:last-child, .callout-person p:last-child, .callout-concept p:last-child,
    .callout-case p:last-child, .callout-data p:last-child {{ margin-bottom: 0; }}

    .pullquote {{
      font-family: var(--font-serif);
      font-size: 1.1rem;
      font-weight: 600;
      line-height: 1.6;
      color: var(--accent-warm);
      text-align: center;
      padding: 24px 32px;
      margin: 32px 0;
      border-top: 1px solid var(--border);
      border-bottom: 1px solid var(--border);
    }}

    .insight-box {{
      background: var(--accent-muted);
      border: 1px solid var(--accent-warm);
      padding: 20px 24px;
      margin: 24px 0;
    }}
    .insight-box-label {{
      font-family: var(--font);
      font-size: 0.65rem;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--accent-warm);
      margin-bottom: 10px;
    }}
    .insight-box p {{
      font-size: 0.88rem;
      margin-bottom: 0.6em;
    }}
    .insight-box p:last-child {{ margin-bottom: 0; }}

    .case-study {{
      border: 1px solid var(--border);
      padding: 20px 24px;
      margin: 24px 0;
      background: var(--card);
    }}
    .case-study-label {{
      font-family: var(--font);
      font-size: 0.65rem;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--text-muted);
      margin-bottom: 8px;
    }}
    .case-study p {{ font-size: 0.88rem; }}

    .summary-box {{
      background: var(--surface);
      border: 1px solid var(--border);
      padding: 20px 24px;
      margin: 32px 0;
    }}
    .summary-box h4 {{
      font-family: var(--font);
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--text-secondary);
      letter-spacing: 0.06em;
      text-transform: uppercase;
      margin-bottom: 12px;
    }}
    .summary-box ul, .summary-box ol {{
      font-size: 0.88rem;
      padding-left: 1.4em;
    }}
    .summary-box li {{ margin-bottom: 6px; }}

    .chapter-divider {{
      border: none;
      border-top: 1px solid var(--border-light);
      margin: 40px 0;
    }}

    .concept-id {{
      font-family: monospace;
      font-size: 0.75em;
      color: var(--accent-warm);
      background: var(--accent-muted);
      padding: 1px 4px;
      border-radius: 2px;
    }}

    pre {{
      background: var(--surface);
      border: 1px solid var(--border-light);
      padding: 16px 20px;
      margin: 20px 0;
      overflow-x: auto;
      font-size: 0.85rem;
    }}
    code {{
      font-family: "SF Mono", "Fira Code", monospace;
      font-size: 0.85em;
      background: var(--surface);
      padding: 1px 4px;
      border-radius: 2px;
    }}
    pre code {{
      background: none;
      padding: 0;
    }}

    .reading-progress {{
      position: fixed;
      top: 51px;
      left: 0;
      height: 2px;
      background: var(--accent-warm);
      width: 0%;
      z-index: 99;
      transition: width 0.1s;
    }}

    @media (max-width: 768px) {{
      .book-layout {{ grid-template-columns: 1fr; }}
      .toc-sidebar {{ display: none; }}
      .book-main {{ padding: 40px 0 80px 0; }}
      .book-title {{ font-size: 1.5rem; }}
    }}
    @media print {{
      .top-bar, .toc-sidebar, .reading-progress {{ display: none; }}
      .book-main {{ padding: 0; max-width: 100%; }}
    }}
  </style>
</head>
<body>
  <div class="reading-progress" id="readingProgress"></div>

  <header class="top-bar">
    <div class="top-bar-brand">
      <span>MG Knowledge DB</span> — Textbook
    </div>
    <div class="top-bar-actions">
      <a href="../databases.html" class="back-link">&larr; データベース一覧に戻る</a>
      <button class="theme-toggle" id="themeToggle" onclick="toggleTheme()">DARK</button>
    </div>
  </header>

  <div class="book-layout">

    <nav class="toc-sidebar" aria-label="目次">
      <div class="toc-label">目次</div>
      <ol class="toc-list">
        {toc_html}
      </ol>
    </nav>

    <main class="book-main">

      <header class="book-header">
        <div class="book-db-tags">
          <span class="db-tag primary">MG: Management Studies DB</span>
          <span class="db-tag">3,458概念</span>
          <span class="db-tag">5,267関係</span>
        </div>
        <h1 class="book-title">経営の知的地図</h1>
        <p class="book-subtitle">3,458概念で読み解く経営学の全体像 ── データ駆動型・概念系譜アプローチによる統合的経営学教科書</p>
        <div class="book-meta">
          <span class="book-author">西村勇也</span>
          <span class="book-date">2026年5月</span>
        </div>
        <div class="book-metrics">
          <span class="metric-item"><strong>20</strong> 章</span>
          <span class="metric-item"><strong>3,458</strong> 概念</span>
          <span class="metric-item"><strong>232</strong> 研究者</span>
          <span class="metric-item"><strong>5,267</strong> 関係</span>
        </div>
      </header>

{sections_html}

    </main>
  </div>

  <script>
    function toggleTheme() {{
      const html = document.documentElement;
      const btn = document.getElementById('themeToggle');
      if (html.getAttribute('data-theme') === 'dark') {{
        html.setAttribute('data-theme', 'light');
        btn.textContent = 'DARK';
        localStorage.setItem('theme', 'light');
      }} else {{
        html.setAttribute('data-theme', 'dark');
        btn.textContent = 'LIGHT';
        localStorage.setItem('theme', 'dark');
      }}
    }}

    // Restore theme
    (function() {{
      const saved = localStorage.getItem('theme');
      if (saved === 'dark') {{
        document.documentElement.setAttribute('data-theme', 'dark');
        const btn = document.getElementById('themeToggle');
        if (btn) btn.textContent = 'LIGHT';
      }}
    }})();

    // Reading progress bar
    window.addEventListener('scroll', function() {{
      const scrollTop = window.scrollY || document.documentElement.scrollTop;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      document.getElementById('readingProgress').style.width = progress + '%';
    }});

    // Highlight active TOC item
    const sections = document.querySelectorAll('.chapter-section');
    const tocLinks = document.querySelectorAll('.toc-list a');

    const observer = new IntersectionObserver((entries) => {{
      entries.forEach(entry => {{
        if (entry.isIntersecting) {{
          tocLinks.forEach(link => {{
            link.style.color = '';
            link.style.fontWeight = '';
          }});
          const id = entry.target.getAttribute('id');
          const activeLink = document.querySelector(`.toc-list a[href="#${{id}}"]`);
          if (activeLink) {{
            activeLink.style.color = 'var(--accent-warm)';
            activeLink.style.fontWeight = '600';
          }}
        }}
      }});
    }}, {{ rootMargin: '-20% 0px -70% 0px' }});

    sections.forEach(s => observer.observe(s));
  </script>
</body>
</html>'''

    return html_content


if __name__ == '__main__':
    print("Building mg-textbook.html...")
    html_content = build_html()

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)

    size_bytes = os.path.getsize(OUTPUT_FILE)
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024
    print(f"Done! Output: {OUTPUT_FILE}")
    print(f"File size: {size_bytes:,} bytes ({size_kb:.1f} KB / {size_mb:.2f} MB)")
    print(f"Lines: {html_content.count(chr(10)):,}")
