#!/usr/bin/env python3
"""
Futures（未来のかたち）連載 全100話 HTMLパブリッシャー

Markdown drafts (ep002-draft.md ... ep007-draft.md + 9 batch files) を
ep001.html フォーマットに準拠した99本のHTML（ep002.html ... ep100.html）に変換する。

実行:
  python3 generate_html.py

出力:
  ./ep002.html ... ./ep100.html
"""

from __future__ import annotations

import html
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

SITE_BASE_URL = "https://journal.emerging-future.org/futures-series-v2"
DEFAULT_OG_IMAGE = "https://journal.emerging-future.org/futures-series-v2/og-default.png"


def make_meta_description(ep_number: int, subtitle: str, title: str, lead: str) -> str:
    base = (lead or "").strip().replace('\n', ' ').replace('"', "'")
    if len(base) > 158:
        cut = base[:158]
        idx = cut.rfind('。')
        base = cut[:idx + 1] if idx > 80 else cut[:155] + '…'
    elif len(base) < 50:
        head = f"連載「Futures（未来のかたち）」第{ep_number}話「{subtitle or title}」。"
        base = (head + base)[:158]
    return base

# ---------------------------------------------------------------------------
# 定数
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
INDIVIDUAL_DRAFTS = [BASE_DIR / f"ep{n:03d}-draft.md" for n in range(2, 8)]
BATCH_FILES = [
    BASE_DIR / "ep008-017-batch.md",
    BASE_DIR / "ep018-027-batch.md",
    BASE_DIR / "ep028-037-batch.md",
    BASE_DIR / "ep038-047-batch.md",
    BASE_DIR / "ep048-057-batch.md",
    BASE_DIR / "ep058-067-batch.md",
    BASE_DIR / "ep068-077-batch.md",
    BASE_DIR / "ep078-087-batch.md",
    BASE_DIR / "ep088-100-batch.md",
]

# v2.0 5部構成（PART, 番号, タイトル, 範囲）
PARTS: List[dict] = [
    {
        "key": "PART_I",
        "number": "PART I",
        "title": "現在地",
        "subtitle": "いま私たちが立っている場所",
        "range": (1, 20),
    },
    {
        "key": "PART_II",
        "number": "PART II",
        "title": "問いを問う",
        "subtitle": "未来をめぐる問いを問い直す",
        "range": (21, 40),
    },
    {
        "key": "PART_III",
        "number": "PART III",
        "title": "系譜を読む",
        "subtitle": "未来を切り拓いてきた人々",
        "range": (41, 60),
    },
    {
        "key": "PART_IV",
        "number": "PART IV",
        "title": "担い手の像",
        "subtitle": "これからの担い手の姿",
        "range": (61, 80),
    },
    {
        "key": "PART_V",
        "number": "PART V",
        "title": "未来のかたち",
        "subtitle": "2070年〜2100年の未来像",
        "range": (81, 100),
    },
]

# 8つの問いと話番号の対応（企画書 v2.0 接続マップに準拠）
EIGHT_QUESTIONS = {
    "Q1": {"label": "未来世代の声", "url": "../eight-questions-q1-detail.html"},
    "Q2": {"label": "先住民の知", "url": "../eight-questions-q2-detail.html"},
    "Q3": {"label": "場所性", "url": "../eight-questions-q3-detail.html"},
    "Q4": {"label": "複数の世界観", "url": "../eight-questions-q4-detail.html"},
    "Q5": {"label": "問いの問い", "url": "../eight-questions-q5-detail.html"},
    "Q6": {"label": "ケア教育", "url": "../eight-questions-q6-detail.html"},
    "Q7": {"label": "西洋以外の知", "url": "../eight-questions-q7-detail.html"},
    "Q8": {"label": "複数の自己", "url": "../eight-questions-q8-detail.html"},
}

# 話番号 → 主たるQ番号（v2.0 接続マップ）
EP_TO_Q = {}
for ep in [8, 9, 10, 11, 12, 13, 14]:
    EP_TO_Q[ep] = "Q3"
for ep in [15, 16, 17, 18, 19, 20]:
    EP_TO_Q[ep] = "Q5"
for ep in range(21, 36):
    EP_TO_Q[ep] = "Q5"
for ep in [36, 37, 38, 39]:
    EP_TO_Q[ep] = "Q4"
for ep in range(41, 51):
    EP_TO_Q[ep] = "Q1"
for ep in range(51, 56):
    EP_TO_Q[ep] = "Q2"
for ep in range(56, 61):
    EP_TO_Q[ep] = "Q7"
for ep in range(61, 68):
    EP_TO_Q[ep] = "Q6"
for ep in range(68, 73):
    EP_TO_Q[ep] = "Q3"
for ep in range(73, 81):
    EP_TO_Q[ep] = "Q8"
EP_TO_Q[87] = "Q8"
for ep in [89]:
    EP_TO_Q[ep] = "Q7"

# 話番号 → 主たる学術領域
def lens_for(ep: int) -> str:
    if ep <= 7:
        return "哲学 / 連載序論"
    if 8 <= ep <= 14:
        return "場所論 / 哲学・民俗学・人類学"
    if 15 <= ep <= 20:
        return "問い論 / 哲学・教育学"
    if 21 <= ep <= 35:
        return "問い論 / 哲学・対話学"
    if 36 <= ep <= 40:
        return "存在論 / 人類学・哲学"
    if 41 <= ep <= 50:
        return "未来世代論 / 政治哲学・倫理学"
    if 51 <= ep <= 60:
        return "先住民研究 / 人類学・倫理学"
    if 61 <= ep <= 67:
        return "ケア論 / 哲学・社会学"
    if 68 <= ep <= 72:
        return "民主主義論 / 政治哲学"
    if 73 <= ep <= 80:
        return "自己論 / 哲学・人類学"
    if 81 <= ep <= 87:
        return "制度論 / 法哲学・政治学"
    if 88 <= ep <= 92:
        return "未来像 / 哲学・社会学"
    return "メタ / 連載総括"


# ---------------------------------------------------------------------------
# データ構造
# ---------------------------------------------------------------------------
@dataclass
class Episode:
    number: int
    title: str
    subtitle: str
    body_paragraphs: List[str] = field(default_factory=list)
    pullquotes: List[str] = field(default_factory=list)
    qref_text: Optional[str] = None  # 「この回は、Q?…」の参照行
    deeper_title: str = "学術視点で、この回の前提を深める"
    deeper_paragraphs: List[str] = field(default_factory=list)
    signal_title: str = "現実の地形に立ち上がっている兆し"
    signal_paragraphs: List[str] = field(default_factory=list)
    key_references: List[str] = field(default_factory=list)
    next_question: str = ""

    @property
    def filename(self) -> str:
        return f"ep{self.number:03d}.html"

    def part(self) -> dict:
        for p in PARTS:
            lo, hi = p["range"]
            if lo <= self.number <= hi:
                return p
        return PARTS[0]


# ---------------------------------------------------------------------------
# Markdownパース
# ---------------------------------------------------------------------------
EP_HEADER_RE = re.compile(r"^# 第(\d+)話[「『](.+?)[」』]\s*$")
SUBTITLE_RE = re.compile(r"^##\s*[―—-]\s*(.+?)\s*$")
SECTION_RE = re.compile(r"^##\s+(DEEPER|SIGNAL|KEY REFERENCE|次の問い)\b\s*[：:]?\s*(.*?)\s*$", re.IGNORECASE)
QREF_RE = re.compile(r"^>\s*(この回は、|>?\s*この回は、).*?$")


def split_into_episodes(text: str) -> List[Tuple[int, str]]:
    """テキストを `# 第N話「タイトル」` で区切り、(番号, 本文) のリストを返す。"""
    lines = text.splitlines()
    eps: List[Tuple[int, List[str]]] = []
    current: Optional[Tuple[int, List[str]]] = None
    for line in lines:
        m = EP_HEADER_RE.match(line.strip())
        if m:
            if current is not None:
                eps.append(current)
            current = (int(m.group(1)), [line])
        elif current is not None:
            current[1].append(line)
    if current is not None:
        eps.append(current)
    return [(num, "\n".join(body)) for num, body in eps]


def parse_episode(num: int, body: str) -> Episode:
    """1話分のMarkdownをパースする。"""
    lines = body.splitlines()

    # 1. タイトル行
    title = ""
    subtitle = ""
    idx = 0
    while idx < len(lines):
        m = EP_HEADER_RE.match(lines[idx].strip())
        if m:
            title = m.group(2).strip()
            idx += 1
            break
        idx += 1

    # 2. サブタイトル行（## ― ...）
    while idx < len(lines):
        line = lines[idx]
        if not line.strip():
            idx += 1
            continue
        m = SUBTITLE_RE.match(line.strip())
        if m:
            subtitle = m.group(1).strip()
            idx += 1
        break

    # 3. 本文〜DEEPER直前まで
    body_lines = []
    while idx < len(lines):
        line = lines[idx]
        m = SECTION_RE.match(line.strip())
        if m and m.group(1).upper() in ("DEEPER", "SIGNAL", "KEY REFERENCE", "次の問い"):
            break
        # `## 次の問い` の正規表現対応（半角空白なし版も）
        if line.strip().startswith("## 次の問い"):
            break
        body_lines.append(line)
        idx += 1

    # 4. DEEPERセクション
    deeper_title = "学術視点で、この回の前提を深める"
    deeper_lines: List[str] = []
    if idx < len(lines):
        line = lines[idx].strip()
        m = SECTION_RE.match(line)
        if m and m.group(1).upper() == "DEEPER":
            if m.group(2):
                deeper_title = m.group(2).strip()
            idx += 1
            while idx < len(lines):
                cur = lines[idx]
                next_m = SECTION_RE.match(cur.strip())
                if next_m and next_m.group(1).upper() in ("SIGNAL", "KEY REFERENCE", "次の問い"):
                    break
                if cur.strip().startswith("## 次の問い"):
                    break
                deeper_lines.append(cur)
                idx += 1

    # 5. SIGNALセクション
    signal_title = "現実の地形に立ち上がっている兆し"
    signal_lines: List[str] = []
    if idx < len(lines):
        line = lines[idx].strip()
        m = SECTION_RE.match(line)
        if m and m.group(1).upper() == "SIGNAL":
            if m.group(2):
                signal_title = m.group(2).strip()
            idx += 1
            while idx < len(lines):
                cur = lines[idx]
                next_m = SECTION_RE.match(cur.strip())
                if next_m and next_m.group(1).upper() in ("KEY REFERENCE", "次の問い"):
                    break
                if cur.strip().startswith("## 次の問い"):
                    break
                signal_lines.append(cur)
                idx += 1

    # 6. KEY REFERENCEセクション
    key_refs: List[str] = []
    if idx < len(lines):
        line = lines[idx].strip()
        m = SECTION_RE.match(line)
        if m and m.group(1).upper() == "KEY REFERENCE":
            idx += 1
            while idx < len(lines):
                cur = lines[idx]
                next_m = SECTION_RE.match(cur.strip())
                if next_m and next_m.group(1).upper() in ("次の問い",):
                    break
                if cur.strip().startswith("## 次の問い"):
                    break
                if cur.strip().startswith("- ") or cur.strip().startswith("* "):
                    key_refs.append(cur.strip()[2:].strip())
                idx += 1

    # 7. 次の問い
    next_q_lines: List[str] = []
    if idx < len(lines):
        line = lines[idx].strip()
        if line.startswith("## 次の問い") or (
            SECTION_RE.match(line) and SECTION_RE.match(line).group(1).upper() in ("次の問い",)
        ):
            idx += 1
            while idx < len(lines):
                cur = lines[idx]
                # 次のエピソード境界
                if cur.strip().startswith("# 第") and EP_HEADER_RE.match(cur.strip()):
                    break
                if cur.strip() == "---":
                    break
                next_q_lines.append(cur)
                idx += 1

    # 本文をパース: 段落・pullquote・qref を分離
    paragraphs, pullquotes, qref = parse_body_text(body_lines)

    deeper_paragraphs = parse_paragraphs("\n".join(deeper_lines))
    signal_paragraphs = parse_paragraphs("\n".join(signal_lines))
    next_question = clean_paragraph(" ".join(l.strip() for l in next_q_lines if l.strip())).strip()
    next_question = re.sub(r"^→.*$", "", next_question, flags=re.MULTILINE).strip()

    return Episode(
        number=num,
        title=title,
        subtitle=subtitle,
        body_paragraphs=paragraphs,
        pullquotes=pullquotes,
        qref_text=qref,
        deeper_title=deeper_title,
        deeper_paragraphs=deeper_paragraphs,
        signal_title=signal_title,
        signal_paragraphs=signal_paragraphs,
        key_references=key_refs,
        next_question=next_question,
    )


def parse_body_text(lines: List[str]) -> Tuple[List[str], List[str], Optional[str]]:
    """本文ラインから 段落配列・pullquote配列・Q参照テキスト を抽出する。"""
    text = "\n".join(lines).strip()
    blocks = re.split(r"\n\s*\n", text)
    paragraphs: List[str] = []
    pullquotes: List[str] = []
    qref: Optional[str] = None
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        # `>` から始まる引用ブロック
        if block.startswith(">"):
            quote_text = "\n".join(re.sub(r"^>\s?", "", l) for l in block.splitlines()).strip()
            if quote_text.startswith("この回は、") or "8つの問い" in quote_text and len(quote_text) < 200:
                # Q対応の参照行
                qref = quote_text
            else:
                pullquotes.append(quote_text)
            continue
        paragraphs.append(clean_paragraph(block))
    return paragraphs, pullquotes, qref


def parse_paragraphs(text: str) -> List[str]:
    text = text.strip()
    if not text:
        return []
    blocks = re.split(r"\n\s*\n", text)
    return [clean_paragraph(b) for b in blocks if b.strip()]


def clean_paragraph(text: str) -> str:
    """段落テキストの改行・余白を整理する。"""
    # 改行は半角スペースに（日本語なので除去でも良いが、念のためスペース）
    one_line = re.sub(r"\s*\n\s*", "", text.strip())
    return one_line


# ---------------------------------------------------------------------------
# HTML生成
# ---------------------------------------------------------------------------
def render_inline(text: str) -> str:
    """段落内の **強調** を <strong> に、それ以外は HTMLエスケープ。"""
    # まず全体をエスケープ
    escaped = html.escape(text, quote=False)
    # **bold** → <strong>
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    # *italic* は使われていないので無視
    return escaped


def build_toc_sidebar(ep: Episode) -> str:
    """5部構成のTOCサイドバーを生成。現在話のPARTにcurrentマーカーを置く。"""
    cur_part = ep.part()
    sections: List[str] = []
    sections.append('<div class="toc-label">FULL SERIES — 全100話</div>')

    for p in PARTS:
        is_current = p["key"] == cur_part["key"]
        lo, hi = p["range"]
        section_lines = ['<div class="toc-section">']
        section_lines.append(
            f'<a class="toc-part" href="../../ryoiki-index.html#phase-e">{html.escape(p["number"])} ― {html.escape(p["title"])}（{lo}-{hi}）</a>'
        )
        section_lines.append(
            f'<a class="toc-part-title" href="../../ryoiki-index.html#phase-e">{html.escape(p["subtitle"])}</a>'
        )
        if is_current:
            label_text = f"第{ep.number}話 ― {ep.title}"
            section_lines.append(
                f'<span class="toc-current">{html.escape(label_text)}</span>'
            )
        section_lines.append("</div>")
        sections.append("\n      ".join(section_lines))

    return "\n    ".join(sections)


def render_paragraphs_html(paragraphs: List[str], pullquotes: Optional[List[str]] = None) -> str:
    """本文段落を <p>...</p> に。pullquoteがあれば適切な位置（中盤）に挿入。"""
    pullquotes = pullquotes or []
    n = len(paragraphs)
    if n == 0:
        return ""

    # pullquote挿入位置: 段落数の半分の直後
    insert_positions: List[int] = []
    if pullquotes:
        if n >= 4:
            # 中盤に1個目、後半に2個目
            insert_positions.append(n // 2)
            if len(pullquotes) >= 2:
                insert_positions.append(min(n - 1, n // 2 + 2))
        else:
            insert_positions.append(max(1, n // 2))

    parts: List[str] = []
    pq_idx = 0
    for i, para in enumerate(paragraphs):
        parts.append(f"    <p>{render_inline(para)}</p>")
        if pq_idx < len(pullquotes) and pq_idx < len(insert_positions) and i + 1 == insert_positions[pq_idx]:
            pq_text = pullquotes[pq_idx]
            parts.append(f'    <p class="ep-pullquote">{render_inline(pq_text)}</p>')
            pq_idx += 1
    # 残りpullquoteは末尾に
    while pq_idx < len(pullquotes):
        parts.append(f'    <p class="ep-pullquote">{render_inline(pullquotes[pq_idx])}</p>')
        pq_idx += 1
    return "\n".join(parts)


def render_lens(label: str, title: str, paragraphs: List[str], lens_id: str) -> str:
    if not paragraphs:
        return ""
    body_html = "\n        ".join(f"<p>{render_inline(p)}</p>" for p in paragraphs)
    return f'''    <details class="reading-lens" id="{lens_id}">
      <summary class="reading-lens-trigger">
        <span class="reading-lens-label">{html.escape(label)}</span>
        <span class="reading-lens-title">{html.escape(title)}</span>
        <span class="reading-lens-arrow">▾</span>
      </summary>
      <div class="reading-lens-body">
        {body_html}
      </div>
    </details>'''


def render_key_reference(refs: List[str], lens_id: str) -> str:
    if not refs:
        return ""
    items = "\n          ".join(f"<li>{render_inline(r)}</li>" for r in refs)
    return f'''    <details class="reading-lens" id="{lens_id}">
      <summary class="reading-lens-trigger">
        <span class="reading-lens-label">KEY REF</span>
        <span class="reading-lens-title">この回の主要参照文献</span>
        <span class="reading-lens-arrow">▾</span>
      </summary>
      <div class="reading-lens-body">
        <ul style="font-family: var(--serif); font-size: 15.5px; line-height: 2.1; color: var(--ink-soft); list-style: none; padding-left: 0; margin: 0;">
          {items}
        </ul>
      </div>
    </details>'''


def render_qref(ep: Episode) -> str:
    """Q参照リード（hero下またはbody先頭）を生成。"""
    q = EP_TO_Q.get(ep.number)
    if not q and not ep.qref_text:
        return ""

    if ep.qref_text:
        text = ep.qref_text
    else:
        qinfo = EIGHT_QUESTIONS[q]
        text = f"この回は、8つの問いの「{q} {qinfo['label']}」と関わります。"

    if q:
        url = EIGHT_QUESTIONS[q]["url"]
        link = f'　<a href="{url}" style="color: var(--accent); font-family: var(--sans); font-size: 12.5px; letter-spacing: 0.06em;">詳細記事を読む →</a>'
    else:
        link = ""

    return f'''    <p style="font-family: var(--sans); font-size: 12.5px; color: var(--ink-mute); letter-spacing: 0.06em; padding: 12px 16px; background: var(--bg-soft); border-left: 2px solid var(--accent); margin-bottom: 36px; line-height: 1.85; text-indent: 0;">{render_inline(text)}{link}</p>'''


def build_episode_html(ep: Episode, prev_ep: Optional[Episode], next_ep: Optional[Episode]) -> str:
    cur_part = ep.part()
    eyebrow = f"{cur_part['number']} ― {cur_part['title']}　第{ep.number}話"
    page_title = f"第{ep.number}話 ― {ep.title} | 未来のかたち"
    en_subtitle = ""  # English subtitleは原稿に明示なし

    # リード文（hero-lead）: 本文1段落目を要約として使う or 副題
    lead = ""
    if ep.body_paragraphs:
        first = ep.body_paragraphs[0]
        # 1段落目を110字程度で切ってリードに（句点で）
        sentences = re.split(r"(?<=。)", first)
        lead_buf = ""
        for s in sentences:
            if len(lead_buf) + len(s) > 180:
                break
            lead_buf += s
        lead = lead_buf if lead_buf else first[:160]

    page_desc = make_meta_description(ep.number, ep.subtitle, ep.title, lead)

    # 番号表示
    num_display = f"{ep.number:02d}"

    # TOC
    toc_html = build_toc_sidebar(ep)

    # 本文
    body_html = render_paragraphs_html(ep.body_paragraphs, ep.pullquotes)

    # Lens (DEEPER, SIGNAL, KEY REF)
    qref_html = render_qref(ep)
    deeper_html = render_lens(
        "DEEPER",
        ep.deeper_title,
        ep.deeper_paragraphs,
        f"lens-deeper-ep{ep.number:03d}",
    )
    signal_html = render_lens(
        "SIGNAL",
        ep.signal_title,
        ep.signal_paragraphs,
        f"lens-signal-ep{ep.number:03d}",
    )
    keyref_html = render_key_reference(ep.key_references, f"lens-keyref-ep{ep.number:03d}")

    # 次の問い
    next_question_text = ep.next_question or "次回へ続きます。"

    # 次話・前話のリンク
    if prev_ep is not None:
        prev_title = f"第{prev_ep.number}話「{prev_ep.title}」"
        prev_link = f'<a class="ep-nav-link" href="./{prev_ep.filename}"><span class="ep-nav-label">← PREV</span><span class="ep-nav-title">{html.escape(prev_title)}</span></a>'
    elif ep.number == 2:
        prev_link = '<a class="ep-nav-link" href="../futures-series/ep001.html"><span class="ep-nav-label">← PREV</span><span class="ep-nav-title">第1話「未来は『当てる』ものではなく『描く』もの」</span></a>'
    else:
        prev_link = '<a class="ep-nav-link disabled" href="#" aria-disabled="true"><span class="ep-nav-label">← PREV</span><span class="ep-nav-title">― 連載のはじまり ―</span></a>'

    if next_ep is not None:
        next_title = f"第{next_ep.number}話「{next_ep.title}」"
        next_link = f'<a class="ep-nav-link next" href="./{next_ep.filename}"><span class="ep-nav-label">NEXT →</span><span class="ep-nav-title">{html.escape(next_title)}</span></a>'
        question_next_meta = "NEXT EPISODE"
        question_next_title = next_title
        question_next_link = (
            f'<a class="ep-question-next-link" href="./{next_ep.filename}">次の話を読む →</a>'
        )
    else:
        next_link = '<a class="ep-nav-link next disabled" href="#" aria-disabled="true"><span class="ep-nav-label">NEXT →</span><span class="ep-nav-title">― 連載完結 ―</span></a>'
        question_next_meta = "FINAL"
        question_next_title = "連載完結。坂はあなたの足元に。"
        question_next_link = (
            '<a class="ep-question-next-link" href="../../ryoiki-index.html#phase-e">索引へ戻る →</a>'
        )

    # 学術領域
    lens_label = lens_for(ep.number)

    # OG description（meta descriptionと統一）
    og_desc = page_desc

    canonical_url = f"{SITE_BASE_URL}/{ep.filename}"
    prev_link_rel = f'<link rel="prev" href="./{prev_ep.filename}">' if prev_ep else ''
    next_link_rel = f'<link rel="next" href="./{next_ep.filename}">' if next_ep else ''

    jsonld_payload = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"第{ep.number}話 ― {ep.title}",
        "description": page_desc,
        "inLanguage": "ja",
        "url": canonical_url,
        "isPartOf": {
            "@type": "CreativeWorkSeries",
            "name": "Futures（未来のかたち）",
            "position": ep.number,
        },
        "publisher": {"@type": "NGO", "name": "NPO法人ミラツク"},
    }
    jsonld_block = json.dumps(jsonld_payload, ensure_ascii=False)

    html_doc = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(page_title)}</title>
<meta name="description" content="{html.escape(page_desc)}">
<meta name="theme-color" content="#14110F">
<meta property="og:title" content="第{ep.number}話 ― {html.escape(ep.title)}">
<meta property="og:description" content="{html.escape(og_desc)}">
<meta property="og:type" content="article">
<meta property="og:url" content="{canonical_url}">
<meta property="og:image" content="{DEFAULT_OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{canonical_url}">
{prev_link_rel}
{next_link_rel}
<script type="application/ld+json">{jsonld_block}</script>
<link rel="icon" href="https://esse-sense.com/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700;900&family=Noto+Serif+JP:wght@300;400;500;600;700;900&family=Judson:wght@400;700&display=swap" rel="stylesheet">
<style>
:root {{
  --bg:           #14110F;
  --bg-soft:      #1E1B19;
  --bg-tint:      #25221F;
  --ink:          #FFFFFF;
  --ink-soft:     #D8D5D1;
  --ink-mute:     #A6A29D;
  --ink-faint:    #7A7672;
  --accent:       #FF3644;
  --accent-deep:  #FF5560;
  --accent-soft:  rgba(255, 54, 68, 0.10);
  --accent-tint:  rgba(255, 54, 68, 0.22);
  --line:         #2D2A27;
  --line-soft:    #1F1D1B;
  --serif:   "Noto Serif JP", "Hiragino Mincho ProN", "Yu Mincho", "Plantin MT Pro", Georgia, serif;
  --sans:    "Noto Sans JP", "Hiragino Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --display: "Judson", "Noto Serif JP", Georgia, serif;
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ font-size: 16px; scroll-behavior: smooth; }}
body {{
  font-family: var(--serif);
  background: var(--bg);
  color: var(--ink);
  line-height: 1.95;
  letter-spacing: 0.02em;
  font-feature-settings: "palt";
  -webkit-font-smoothing: antialiased;
}}
a {{ color: var(--accent); text-decoration: none; transition: color .15s; }}
a:hover {{ color: var(--accent-deep); }}

:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 3px; border-radius: 2px; }}
.skip-link {{ position: absolute; left: -9999px; top: 0; }}
.skip-link:focus {{ left: 8px; top: 8px; z-index: 9999; background: var(--accent); color: #fff; padding: 8px 14px; border-radius: 4px; font-family: var(--sans); font-size: 13px; }}
@media (prefers-reduced-motion: reduce) {{
  html {{ scroll-behavior: auto; }}
  * {{ transition-duration: .01ms !important; animation-duration: .01ms !important; }}
}}

.read-progress {{ position: fixed; top: 0; left: 0; right: 0; height: 2px; background: transparent; z-index: 200; pointer-events: none; }}
.read-progress-bar {{ height: 100%; width: 0%; background: var(--accent); transition: width .1s linear; }}

.site-header {{ position: sticky; top: 0; z-index: 100; background: rgba(20, 17, 15, 0.92); backdrop-filter: saturate(160%) blur(10px); -webkit-backdrop-filter: saturate(160%) blur(10px); border-bottom: 1px solid var(--line); }}
.site-header-inner {{ max-width: 1280px; margin: 0 auto; padding: 0 24px; height: 64px; display: flex; align-items: center; justify-content: space-between; gap: 16px; }}
.site-brand {{ display: flex; align-items: center; gap: 12px; text-decoration: none; }}
.site-brand-text {{ font-family: var(--sans); font-size: 12px; font-weight: 700; letter-spacing: 0.16em; color: var(--ink); line-height: 1.3; }}
.site-brand-text small {{ display: block; font-size: 9.5px; letter-spacing: 0.14em; color: var(--ink-mute); font-weight: 500; margin-top: 2px; }}
.site-nav {{ display: flex; gap: 28px; font-family: var(--sans); font-size: 12px; letter-spacing: 0.1em; }}
.site-nav a {{ color: var(--ink-soft); font-weight: 500; padding: 6px 0; border-bottom: 2px solid transparent; transition: color .15s, border-color .15s; }}
.site-nav a:hover {{ color: var(--accent); border-bottom-color: var(--accent); }}
.site-nav a.active {{ color: var(--ink); border-bottom-color: var(--ink); }}

.ep-hero {{ background: var(--bg); color: var(--ink); padding: 80px 24px 64px; position: relative; border-bottom: 1px solid var(--line); }}
.ep-hero-inner {{ max-width: 760px; margin: 0 auto; position: relative; }}
.ep-hero-eyebrow {{ font-family: var(--sans); font-size: 11px; letter-spacing: 0.32em; color: var(--accent); font-weight: 700; display: flex; align-items: center; gap: 12px; margin-bottom: 28px; flex-wrap: wrap; }}
.ep-hero-eyebrow::before {{ content: ""; width: 32px; height: 2px; background: var(--accent); }}
.ep-hero-num {{ font-family: var(--display); font-size: 80px; color: var(--ink); line-height: 0.95; margin-bottom: 24px; letter-spacing: 0; display: flex; align-items: baseline; gap: 14px; font-weight: 700; }}
.ep-hero-num-total {{ font-family: var(--display); font-size: 22px; color: var(--ink-mute); font-weight: 400; }}
.ep-hero-title {{ font-family: var(--serif); font-weight: 700; font-size: 34px; line-height: 1.55; letter-spacing: 0.02em; color: var(--ink); margin-bottom: 14px; }}
.ep-hero-subtitle {{ font-family: var(--serif); font-weight: 500; font-size: 18px; line-height: 1.7; letter-spacing: 0.04em; color: var(--ink-soft); margin-bottom: 22px; }}
.ep-hero-en {{ font-family: var(--display); font-size: 18px; color: var(--ink-mute); letter-spacing: 0.02em; margin-bottom: 32px; font-weight: 400; }}
.ep-hero-lead {{ font-family: var(--serif); font-size: 16px; font-weight: 400; line-height: 2; color: var(--ink-soft); letter-spacing: 0.04em; max-width: 640px; margin-bottom: 36px; padding-left: 18px; border-left: 3px solid var(--accent); }}
.ep-hero-meta {{ display: flex; gap: 24px; flex-wrap: wrap; align-items: center; font-family: var(--sans); font-size: 11.5px; letter-spacing: 0.1em; color: var(--ink-mute); padding-top: 24px; border-top: 1px solid var(--line); }}
.ep-hero-meta strong {{ color: var(--ink); font-weight: 700; }}
.ep-hero-meta .read-time {{ display: inline-flex; align-items: center; gap: 6px; color: var(--ink-soft); }}
.ep-hero-meta .read-time::before {{ content: ""; width: 6px; height: 6px; border-radius: 50%; background: var(--accent); }}

.ep-layout {{ display: grid; grid-template-columns: 240px minmax(0, 1fr); max-width: 1180px; margin: 0 auto; gap: 48px; padding: 0 24px; align-items: start; }}
.toc-sidebar {{ position: sticky; top: 84px; padding: 56px 0 80px; font-family: var(--sans); font-size: 12px; align-self: start; max-height: calc(100vh - 84px); overflow-y: auto; }}
.toc-label {{ font-size: 10px; letter-spacing: 0.28em; color: var(--accent); font-weight: 700; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 2px solid var(--ink); }}
.toc-section {{ margin-bottom: 18px; }}
.toc-part {{ display: block; font-family: var(--sans); font-size: 10.5px; font-weight: 700; letter-spacing: 0.18em; color: var(--ink); margin-bottom: 6px; text-decoration: none; }}
.toc-part:hover {{ color: var(--accent); }}
.toc-part-title {{ display: block; font-family: var(--serif); font-size: 13px; color: var(--ink-soft); line-height: 1.6; letter-spacing: 0.04em; text-decoration: none; margin-bottom: 4px; font-weight: 500; }}
.toc-part-title:hover {{ color: var(--accent); }}
.toc-current {{ display: block; font-family: var(--sans); font-size: 11.5px; color: var(--ink); font-weight: 700; background: var(--accent-soft); border-left: 3px solid var(--accent); padding: 10px 12px; letter-spacing: 0.04em; line-height: 1.6; margin-top: 8px; }}
.toc-current::before {{ content: "● 現在地"; display: block; font-size: 9px; letter-spacing: 0.2em; color: var(--accent); margin-bottom: 4px; font-weight: 700; }}

.ep-body {{ max-width: 720px; margin: 0 auto; padding: 64px 0 96px; }}
.ep-body p {{ font-family: var(--serif); font-size: 17px; line-height: 2.1; color: var(--ink); margin-bottom: 30px; text-indent: 1em; letter-spacing: 0.04em; }}
.ep-body > p:first-of-type {{ text-indent: 0; }}
.ep-body > p:first-of-type::first-letter {{ font-family: var(--display); font-weight: 700; font-size: 4.4em; float: left; line-height: 0.92; margin: 0.06em 0.14em 0 0; color: var(--ink); }}
.ep-body p strong {{ font-weight: 700; color: var(--ink); }}

.ep-body p .hl, .ep-body p span.hl, .ep-body .hl {{ background-image: linear-gradient(transparent 60%, var(--accent-tint) 60%); padding: 0 1px; }}
::selection {{ background: var(--accent-tint); color: var(--ink); }}

.ep-section-mark {{ display: flex; align-items: center; gap: 16px; margin: 56px 0 36px; font-family: var(--sans); font-size: 10.5px; font-weight: 700; letter-spacing: 0.26em; color: var(--accent); }}
.ep-section-mark::after {{ content: ""; flex: 1; height: 1px; background: var(--line); }}

.ep-pullquote {{ margin: 56px 0; padding: 32px 0 32px 32px; border-left: 4px solid var(--accent); font-family: var(--serif); font-size: 19px; line-height: 2; color: var(--ink); letter-spacing: 0.04em; font-weight: 600; font-feature-settings: "palt"; position: relative; text-indent: 0 !important; }}
.ep-pullquote::before {{ content: "\\201C"; position: absolute; top: -18px; left: 18px; font-family: var(--display); font-size: 64px; color: var(--accent); line-height: 1; font-weight: 700; }}

.reading-lens {{ margin-top: 40px; border: 1px solid var(--line); background: var(--bg); transition: border-color .2s; }}
.reading-lens[open] {{ border-color: var(--ink); }}
.reading-lens + .reading-lens {{ margin-top: 16px; }}
.reading-lens-trigger {{ list-style: none; cursor: pointer; padding: 22px 26px; display: flex; align-items: center; gap: 16px; user-select: none; transition: background .15s; }}
.reading-lens-trigger::-webkit-details-marker {{ display: none; }}
.reading-lens-trigger:hover {{ background: var(--bg-soft); }}
.reading-lens[open] .reading-lens-trigger {{ border-bottom: 1px solid var(--line); background: var(--bg-tint); }}
.reading-lens-label {{ font-family: var(--sans); font-size: 9.5px; font-weight: 700; letter-spacing: 0.22em; color: var(--accent); flex-shrink: 0; padding: 4px 10px; border: 1px solid var(--accent); }}
.reading-lens-title {{ font-family: var(--serif); font-size: 16px; font-weight: 700; color: var(--ink); letter-spacing: 0.04em; flex: 1; }}
.reading-lens-arrow {{ font-family: var(--sans); font-size: 14px; color: var(--ink-mute); margin-left: auto; transition: transform .25s; flex-shrink: 0; }}
.reading-lens[open] .reading-lens-arrow {{ transform: rotate(180deg); color: var(--accent); }}
.reading-lens-body {{ padding: 28px 26px 32px; }}
.reading-lens-body p {{ font-family: var(--serif); font-size: 15.5px; line-height: 2.1; color: var(--ink-soft); margin-bottom: 18px; text-indent: 1em; letter-spacing: 0.04em; }}
.reading-lens-body p:last-child {{ margin-bottom: 0; }}

.ep-question {{ margin-top: 56px; padding: 32px 30px 30px; background: var(--bg-tint); border-top: 3px solid var(--ink); position: relative; }}
.ep-question-label {{ font-family: var(--sans); font-size: 10.5px; font-weight: 700; letter-spacing: 0.26em; color: var(--accent); margin-bottom: 12px; }}
.ep-question-q {{ font-family: var(--serif); font-size: 17px; font-weight: 600; color: var(--ink); line-height: 1.95; letter-spacing: 0.04em; margin-bottom: 22px; }}
.ep-question-next {{ display: flex; align-items: baseline; justify-content: space-between; gap: 14px; flex-wrap: wrap; padding-top: 18px; border-top: 1px solid var(--line); }}
.ep-question-next-meta {{ font-family: var(--sans); font-size: 10.5px; font-weight: 700; letter-spacing: 0.2em; color: var(--ink-mute); }}
.ep-question-next-title {{ font-family: var(--serif); font-size: 14px; color: var(--ink); letter-spacing: 0.04em; font-weight: 600; }}
.ep-question-next-link {{ font-family: var(--sans); font-size: 11.5px; font-weight: 700; letter-spacing: 0.16em; color: var(--bg); background: var(--ink); padding: 9px 18px; border-radius: 20px; text-decoration: none; transition: background .15s; }}
.ep-question-next-link:hover {{ background: var(--accent); text-decoration: none; }}

.ep-nav {{ background: var(--bg); border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); }}
.ep-nav-inner {{ max-width: 760px; margin: 0 auto; padding: 28px 24px; display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }}
.ep-nav-link {{ display: flex; flex-direction: column; gap: 6px; padding: 18px 20px; background: var(--bg); border: 1px solid var(--line); text-decoration: none; transition: border-color .15s; }}
.ep-nav-link:hover {{ border-color: var(--accent); text-decoration: none; }}
.ep-nav-link.disabled {{ opacity: 0.45; pointer-events: none; background: var(--bg-soft); }}
.ep-nav-label {{ font-family: var(--sans); font-size: 10px; letter-spacing: 0.2em; color: var(--accent); font-weight: 700; }}
.ep-nav-link.next {{ text-align: right; }}
.ep-nav-title {{ font-family: var(--serif); font-size: 13.5px; color: var(--ink); line-height: 1.65; letter-spacing: 0.04em; font-weight: 500; }}

.site-footer {{ background: var(--bg-soft); padding: 56px 24px 32px; border-top: 1px solid var(--line); }}
.site-footer-inner {{ max-width: 1180px; margin: 0 auto; }}
.site-footer-bottom {{ padding-top: 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px; font-family: var(--sans); font-size: 11px; color: var(--ink-mute); letter-spacing: 0.06em; }}

@media (max-width: 1080px) {{
  .ep-layout {{ grid-template-columns: 1fr; gap: 0; padding: 0; }}
  .toc-sidebar {{ display: none; }}
  .ep-body {{ padding: 56px 24px 64px; }}
}}
@media (max-width: 760px) {{
  .site-nav {{ gap: 8px; font-size: 11px; }}
  .site-nav a {{ padding: 12px 8px; min-height: 44px; display: flex; align-items: center; }}
  .site-brand-text small {{ display: none; }}
  .ep-hero {{ padding: 56px 22px 48px; }}
  .ep-hero-num {{ font-size: 60px; }}
  .ep-hero-num-total {{ font-size: 18px; }}
  .ep-hero-title {{ font-size: 24px; }}
  .ep-hero-subtitle {{ font-size: 15.5px; }}
  .ep-hero-en {{ font-size: 15px; }}
  .ep-hero-lead {{ font-size: 14.5px; padding-left: 14px; }}
  .ep-body {{ padding: 44px 22px 60px; }}
  .ep-body p {{ font-size: 15.5px; line-height: 2.05; margin-bottom: 28px; }}
  .ep-body > p:first-of-type::first-letter {{ font-size: 3.8em; }}
  .ep-pullquote {{ font-size: 16px; padding: 24px 0 24px 22px; margin: 40px 0; }}
  .reading-lens-trigger {{ padding: 18px 20px; flex-wrap: wrap; }}
  .reading-lens-title {{ font-size: 15px; flex-basis: 100%; order: 3; }}
  .reading-lens-label {{ font-size: 9px; }}
  .reading-lens-body {{ padding: 22px 20px 26px; }}
  .reading-lens-body p {{ font-size: 14.5px; line-height: 2; }}
  .ep-question {{ padding: 26px 22px; }}
  .ep-question-q {{ font-size: 15.5px; }}
  .ep-question-next {{ flex-direction: column; align-items: flex-start; }}
  .ep-nav-inner {{ grid-template-columns: 1fr; padding: 22px 22px; }}
  .ep-nav-link.next {{ text-align: left; }}
}}

@media print {{
  :root {{
    --bg: #FFFFFF; --bg-soft: #FAFAFA; --bg-tint: #F5F5F4;
    --ink: #14110F; --ink-soft: #3A3633; --ink-mute: #6B6661; --ink-faint: #9C9692;
    --line: #E8E5E1; --line-soft: #F0EDE9;
  }}
  .read-progress, .site-header, .toc-sidebar, .ep-nav, .site-footer {{ display: none !important; }}
  body {{ background: #FFFFFF; color: #14110F; }}
  .ep-hero {{ background: #FFFFFF; padding: 24px 0; page-break-after: avoid; border-bottom: none; }}
  .ep-layout {{ grid-template-columns: 1fr; padding: 0; }}
  .ep-body {{ padding: 0 24px; }}
  .reading-lens {{ border: 1px solid #14110F; page-break-inside: avoid; }}
  .reading-lens[open] .reading-lens-body {{ display: block !important; }}
  .reading-lens-arrow {{ display: none; }}
  .ep-pullquote, .ep-question {{ page-break-inside: avoid; }}
}}
</style>
</head>
<body>

<a class="skip-link" href="#content">本文へジャンプ</a>
<div class="read-progress" aria-hidden="true"><div class="read-progress-bar" id="readProgressBar"></div></div>

<header class="site-header">
  <div class="site-header-inner">
    <a href="../" class="site-brand">
      <div class="site-brand-text">未来のかたち<small>FUTURES NO KATACHI / 70年先を考えるための100話</small></div>
    </a>
    <nav class="site-nav" aria-label="サイト内ナビゲーション">
      <a href="../">ホーム</a>
      <a href="./index.html">全100話</a>
      <a href="../8-questions/">8つの問い</a>
    </nav>
  </div>
</header>

<main id="content" role="main">

<section class="ep-hero">
  <div class="ep-hero-inner">
    <div class="ep-hero-eyebrow">{html.escape(eyebrow)}</div>
    <div class="ep-hero-num">{num_display}.<span class="ep-hero-num-total">/ 100</span></div>
    <h1 class="ep-hero-title">{html.escape(ep.title)}</h1>
    <p class="ep-hero-subtitle">― {html.escape(ep.subtitle)}</p>
    <p class="ep-hero-lead">{html.escape(lead)}</p>
    <div class="ep-hero-meta">
      <span class="ep-hero-author"><strong>西村 勇也</strong>（NPO法人ミラツク 代表理事）</span>
      <span class="ep-hero-date">2026年5月10日</span>
      <span class="read-time">推定読了 約7分</span>
      <span style="color: var(--ink-mute);">学術領域: {html.escape(lens_label)}</span>
    </div>
  </div>
</section>

<div class="ep-layout">

  <aside class="toc-sidebar" aria-label="連載目次">
    {toc_html}
  </aside>

  <article class="ep-body" id="articleBody">

{qref_html}
{body_html}

{deeper_html}

{signal_html}

{keyref_html}

    <section class="ep-question">
      <div class="ep-question-label">QUESTION FOR NEXT — 次回への問い</div>
      <p class="ep-question-q">{render_inline(next_question_text)}</p>
      <div class="ep-question-next">
        <span class="ep-question-next-meta">{question_next_meta}</span>
        <span class="ep-question-next-title">{html.escape(question_next_title)}</span>
        {question_next_link}
      </div>
    </section>

  </article>
</div>

<nav class="ep-nav">
  <div class="ep-nav-inner">
    {prev_link}
    {next_link}
  </div>
</nav>

</main>

<footer class="site-footer">
  <div class="site-footer-inner">
    <div class="site-footer-bottom">
      <span>&copy; NPO法人ミラツク / 未来のかたち</span>
      <span>FUTURES NO KATACHI ・ Episode {ep.number:02d} / 100</span>
    </div>
  </div>
</footer>

<script>
(function(){{
  var bar = document.getElementById('readProgressBar');
  var body = document.getElementById('articleBody');
  if(!bar || !body) return;
  function update(){{
    var rect = body.getBoundingClientRect();
    var total = rect.height - window.innerHeight;
    var scrolled = -rect.top;
    var pct = total > 0 ? Math.max(0, Math.min(100, (scrolled / total) * 100)) : 0;
    bar.style.width = pct + '%';
  }}
  window.addEventListener('scroll', update, {{ passive: true }});
  window.addEventListener('resize', update);
  update();
}})();
</script>

</body>
</html>
"""
    return html_doc


# ---------------------------------------------------------------------------
# HTMLバランス検証
# ---------------------------------------------------------------------------
TAG_RE = re.compile(r"<\s*(/?)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*?(/?)\s*>")
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

def validate_tag_balance(text: str) -> List[str]:
    """簡易タグバランス検証。エラー一覧を返す。"""
    errors: List[str] = []
    stack: List[Tuple[str, int]] = []
    for m in TAG_RE.finditer(text):
        closing = bool(m.group(1))
        name = m.group(2).lower()
        self_closing = bool(m.group(3))
        if name in VOID_TAGS or self_closing:
            continue
        if not closing:
            stack.append((name, m.start()))
        else:
            if not stack:
                errors.append(f"余分な閉じタグ </{name}> at offset {m.start()}")
                continue
            top_name, top_pos = stack[-1]
            if top_name == name:
                stack.pop()
            else:
                # 不一致があってもポップして次へ（HTML5の寛容さに合わせる）
                # ただしエラー登録
                errors.append(
                    f"閉じタグ不一致: </{name}> at offset {m.start()} (expected </{top_name}>)"
                )
                stack.pop()
    if stack:
        for name, pos in stack:
            errors.append(f"開きタグ未閉鎖: <{name}> at offset {pos}")
    return errors


# ---------------------------------------------------------------------------
# メイン
# ---------------------------------------------------------------------------
def collect_episodes() -> List[Episode]:
    eps: List[Episode] = []

    # 1. 個別ドラフト ep002-007
    for fp in INDIVIDUAL_DRAFTS:
        if not fp.exists():
            print(f"[WARN] missing: {fp}")
            continue
        text = fp.read_text(encoding="utf-8")
        for num, body in split_into_episodes(text):
            eps.append(parse_episode(num, body))

    # 2. バッチ
    for fp in BATCH_FILES:
        if not fp.exists():
            print(f"[WARN] missing: {fp}")
            continue
        text = fp.read_text(encoding="utf-8")
        for num, body in split_into_episodes(text):
            eps.append(parse_episode(num, body))

    eps.sort(key=lambda e: e.number)
    return eps


def main() -> None:
    eps = collect_episodes()
    print(f"検出話数: {len(eps)}")
    nums = [e.number for e in eps]
    expected = list(range(2, 101))
    missing = sorted(set(expected) - set(nums))
    extra = sorted(set(nums) - set(expected))
    if missing:
        print(f"[WARN] 不足話番号: {missing}")
    if extra:
        print(f"[WARN] 想定外話番号: {extra}")

    # 重複排除（最初の出現を優先）
    seen = set()
    unique: List[Episode] = []
    for e in eps:
        if e.number in seen:
            continue
        seen.add(e.number)
        unique.append(e)
    eps = unique

    by_num = {e.number: e for e in eps}
    total_errors = 0
    written = 0
    for e in eps:
        prev_ep = by_num.get(e.number - 1) if e.number - 1 >= 2 else None
        next_ep = by_num.get(e.number + 1)
        html_doc = build_episode_html(e, prev_ep, next_ep)
        out_path = BASE_DIR / e.filename
        out_path.write_text(html_doc, encoding="utf-8")
        errs = validate_tag_balance(html_doc)
        if errs:
            total_errors += len(errs)
            print(f"[TAG ERR] ep{e.number:03d}.html — {len(errs)} 件")
            for err in errs[:3]:
                print(f"  - {err}")
        written += 1

    print(f"書き出し完了: {written} ファイル / タグエラー総数: {total_errors}")
    print("EP-Q マッピング適用率:")
    matched = sum(1 for e in eps if e.number in EP_TO_Q)
    print(f"  {matched} / {len(eps)} = {matched/len(eps)*100:.1f}%")


if __name__ == "__main__":
    main()
