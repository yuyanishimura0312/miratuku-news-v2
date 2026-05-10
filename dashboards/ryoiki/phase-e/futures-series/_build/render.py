#!/usr/bin/env python3
"""Futures NO KATACHI — 各話HTMLレンダラー

Inputs:
  - _build/template.html       (HTMLテンプレ)
  - _build/episodes.json       (企画書パース結果)
  - _drafts/ep0NN.md           (Codex生成の本文ドラフト)

Output:
  - ep0NN.html                 (公開用HTML)
"""

import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # futures-series/
BUILD = ROOT / "_build"
DRAFTS = ROOT / "_drafts"
TEMPLATE = BUILD / "template.html"
EPISODES = BUILD / "episodes.json"

# PART定義
PARTS = [
    # (start, end, eyebrow_label, toc_part_label, toc_title)
    (1, 3, "PROLOGUE — 序 章", "PROLOGUE — 序 章", "現在地から旅をはじめる"),
    (4, 23, "PART I", "PART I", "いま動き始めている問い（問03 + 問06）"),
    (24, 43, "PART II", "PART II", "制度に届く問い（問01 + 問02）"),
    (44, 63, "PART III", "PART III", "学問が組み替わる問い（問07 + 問08）"),
    (64, 83, "PART IV", "PART IV", "70年後の到達点（問04）"),
    (84, 95, "PART V", "PART V", "自己診断の問い（問05）"),
    (96, 100, "FINAL — 終 章", "FINAL — 終 章", "読者の坂を編む"),
]


def part_for(num: int):
    for s, e, eyeb, p_lbl, p_title in PARTS:
        if s <= num <= e:
            return (s, e, eyeb, p_lbl, p_title)
    raise ValueError(num)


def build_toc(current_ep_num: int, current_title: str) -> str:
    """サイドバーTOCを生成。現在のPARTには現在話を強調表示。"""
    blocks = []
    cur_part_idx = next(i for i, (s, e, *_) in enumerate(PARTS) if s <= current_ep_num <= e)
    for idx, (s, e, eyeb, p_lbl, p_title) in enumerate(PARTS):
        if idx == cur_part_idx:
            esc_title = html.escape(current_title)
            blocks.append(
                f'    <div class="toc-section">\n'
                f'      <a class="toc-part" href="../../ryoiki-index.html#phase-e">{html.escape(p_lbl)}</a>\n'
                f'      <a class="toc-part-title" href="../../ryoiki-index.html#phase-e">{html.escape(p_title)}</a>\n'
                f'      <span class="toc-current">第{current_ep_num}話 ― {esc_title}</span>\n'
                f'    </div>'
            )
        else:
            blocks.append(
                f'    <div class="toc-section">\n'
                f'      <a class="toc-part" href="../../ryoiki-index.html#phase-e">{html.escape(p_lbl)}</a>\n'
                f'      <a class="toc-part-title" href="../../ryoiki-index.html#phase-e">{html.escape(p_title)}</a>\n'
                f'    </div>'
            )
    return "\n".join(blocks)


def parse_draft(text: str) -> dict:
    """ドラフトmdをパース。

    形式:
        ---
        read_time: 7
        date: 2026-05-17
        deeper_title: 学術視点で、この回の前提を深める
        next_episode_num: 3
        next_episode_title: 第3話「...」
        next_question_paragraph: ...
        ---

        # BODY

        段落1

        段落2

        > プルクオート

        段落3
        ...

        # DEEPER

        段落1

        段落2

        # SIGNAL

        段落1
        段落2
        段落3
    """
    out = {"meta": {}, "body": [], "deeper": [], "lab": [], "signal": []}

    # frontmatter
    fm_match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if fm_match:
        fm_text, rest = fm_match.group(1), fm_match.group(2)
        for line in fm_text.split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                out["meta"][k.strip()] = v.strip()
    else:
        rest = text

    # セクション分割
    sections = re.split(r"\n#\s+(BODY|DEEPER|LAB|SIGNAL)\s*\n", rest)
    # sections = [pre, key1, body1, key2, body2, ...]
    cur = None
    for i, chunk in enumerate(sections):
        if i == 0:
            continue
        if i % 2 == 1:
            cur = chunk.strip().lower()  # body/deeper/signal
        else:
            paragraphs = []
            buf = []
            for ln in chunk.split("\n"):
                if ln.strip() == "":
                    if buf:
                        paragraphs.append("\n".join(buf).strip())
                        buf = []
                else:
                    buf.append(ln)
            if buf:
                paragraphs.append("\n".join(buf).strip())
            out[cur] = [p for p in paragraphs if p]
    return out


def render_body(paragraphs: list[str]) -> str:
    """本文段落のHTMLを生成。`> ...` で始まる段落はpullquoteとして処理。"""
    out = []
    for p in paragraphs:
        if p.startswith(">"):
            text = p.lstrip("> ").strip()
            out.append(f'    <p class="ep-pullquote">{html.escape(text)}</p>')
        else:
            out.append(f'    <p>{html.escape(p)}</p>')
    return "\n\n".join(out)


def render_lens_body(paragraphs: list[str]) -> str:
    """DEEPER/SIGNALの本文HTMLを生成。"""
    return "\n".join(f'        <p>{html.escape(p)}</p>' for p in paragraphs)


def render_lab_block(paragraphs: list[str]) -> str:
    """LAB（自然科学・工学）reading-lensのHTMLを生成。LAB が空なら空文字列を返す。"""
    if not paragraphs:
        return ""
    body = "\n".join(f'        <p>{html.escape(p)}</p>' for p in paragraphs)
    return (
        '    <details class="reading-lens" id="lens-lab">\n'
        '      <summary class="reading-lens-trigger">\n'
        '        <span class="reading-lens-label">LAB</span>\n'
        '        <span class="reading-lens-title">科学の知から</span>\n'
        '        <span class="reading-lens-arrow">▾</span>\n'
        '      </summary>\n'
        '      <div class="reading-lens-body">\n'
        f'{body}\n'
        '      </div>\n'
        '    </details>\n'
    )


def render_episode(ep_num: int, episodes: list[dict], drafts_dir: Path, template: str) -> str:
    ep = next((e for e in episodes if e["num"] == ep_num), None)
    if not ep:
        raise ValueError(f"Episode {ep_num} not found in episodes.json")

    # ドラフトを読む
    draft_path = drafts_dir / f"ep{ep_num:03d}.md"
    if not draft_path.exists():
        raise FileNotFoundError(f"Draft not found: {draft_path}")
    draft = parse_draft(draft_path.read_text(encoding="utf-8"))

    # PART情報
    s, e, eyebrow, p_lbl, p_title = part_for(ep_num)

    # 次のエピソードのメタ情報を episodes.json から拾う（ドラフト指定があればそちら優先）
    next_meta = ep.get("num", ep_num) + 1 if ep_num < 100 else None
    next_ep_data = next((x for x in episodes if x["num"] == ep_num + 1), None) if next_meta else None

    next_episode_title = draft["meta"].get("next_episode_title")
    if not next_episode_title and next_ep_data:
        next_episode_title = f'第{ep_num+1}話「{next_ep_data["title"]}」'

    # next_question 本文段落（draftが指定 or 企画書から）
    next_question_paragraph = draft["meta"].get("next_question_paragraph", "")
    if not next_question_paragraph:
        nq = ep.get("next_question", "")
        if nq:
            next_question_paragraph = nq

    # PREV/NEXT NAV
    if ep_num == 1:
        prev_disabled = "disabled"
        prev_href = "#"
        prev_aria = ' aria-disabled="true"'
        prev_title = "― 連載のはじまり ―"
    else:
        prev_disabled = ""
        prev_href = f"./ep{ep_num-1:03d}.html"
        prev_aria = ""
        prev_ep_data = next((x for x in episodes if x["num"] == ep_num - 1), None)
        prev_title = f'第{ep_num-1}話「{prev_ep_data["title"]}」' if prev_ep_data else f"第{ep_num-1}話"

    if ep_num == 100:
        next_disabled = "disabled"
        next_href = "#"
        next_nav_title = "― 連載のおわり ―"
        next_episode_href = "../../ryoiki-index.html#phase-e"
        next_cta = "完結"
    elif next_ep_data:
        # 次話のドラフトが存在するなら直リンク、なければインデックスへ
        next_draft_exists = (drafts_dir / f"ep{ep_num+1:03d}.md").exists()
        if next_draft_exists:
            next_disabled = ""
            next_href = f"./ep{ep_num+1:03d}.html"
            next_episode_href = next_href
            next_cta = "次の話を読む →"
            next_nav_title = next_episode_title
        else:
            next_disabled = ""
            next_href = "../../ryoiki-index.html#phase-e"
            next_episode_href = next_href
            next_cta = "公開を待つ →"
            next_nav_title = f"{next_episode_title}（公開予定）"
    else:
        next_disabled = "disabled"
        next_href = "#"
        next_nav_title = "―"
        next_episode_href = "#"
        next_cta = "―"

    # メタ情報
    date = draft["meta"].get("date", "2026年5月")
    read_time = draft["meta"].get("read_time", "7")
    deeper_title = draft["meta"].get("deeper_title", "学術視点で、この回の前提を深める")

    # description（メタタグ用）
    meta_desc = draft["meta"].get("description", "")
    if not meta_desc:
        meta_desc = f"未来のかたち第{ep_num}話。{ep.get('lead', '')[:80]}"

    # サブタイトル
    subtitle = ep.get("subtitle", "").strip()
    if subtitle and not subtitle.startswith("―"):
        subtitle = "― " + subtitle

    # English タイトル（ない場合は連番）
    en_title = ep.get("en_title", "").strip() or f"Episode {ep_num} of 100"

    replacements = {
        "{{EP_NUM}}": str(ep_num),
        "{{EP_NUM_PADDED}}": f"{ep_num:02d}",
        "{{TITLE}}": html.escape(ep["title"]),
        "{{SUBTITLE}}": html.escape(subtitle),
        "{{EN_TITLE}}": html.escape(en_title),
        "{{LEAD}}": html.escape(ep.get("lead", "")),
        "{{DATE}}": html.escape(date),
        "{{READ_TIME}}": html.escape(read_time),
        "{{ACADEMIC_FIELD}}": html.escape(ep.get("academic_field", "")),
        "{{PART_EYEBROW}}": html.escape(eyebrow),
        "{{META_DESC}}": html.escape(meta_desc[:140]),
        "{{TOC_BLOCKS}}": build_toc(ep_num, ep["title"]),
        "{{BODY_PARAGRAPHS}}": render_body(draft["body"]),
        "{{DEEPER_TITLE}}": html.escape(deeper_title),
        "{{DEEPER_BODY}}": render_lens_body(draft["deeper"]),
        "{{LAB_BLOCK}}": render_lab_block(draft.get("lab", [])),
        "{{SIGNAL_BODY}}": render_lens_body(draft["signal"]),
        "{{NEXT_QUESTION_PARAGRAPH}}": html.escape(next_question_paragraph),
        "{{NEXT_EPISODE_TITLE}}": html.escape(next_episode_title or "―"),
        "{{NEXT_EPISODE_HREF}}": next_episode_href,
        "{{NEXT_EPISODE_CTA}}": html.escape(next_cta),
        "{{PREV_DISABLED_CLASS}}": prev_disabled,
        "{{PREV_HREF}}": prev_href,
        "{{PREV_ARIA}}": prev_aria,
        "{{PREV_TITLE}}": html.escape(prev_title),
        "{{NEXT_DISABLED_CLASS}}": next_disabled,
        "{{NEXT_HREF}}": next_href,
        "{{NEXT_NAV_TITLE}}": html.escape(next_nav_title),
    }

    out = template
    for k, v in replacements.items():
        out = out.replace(k, v)
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("episodes", nargs="*", type=int, help="話数（省略時は_drafts/にあるものすべて）")
    p.add_argument("--out-dir", type=Path, default=ROOT)
    args = p.parse_args()

    template = TEMPLATE.read_text(encoding="utf-8")
    episodes = json.loads(EPISODES.read_text(encoding="utf-8"))

    if args.episodes:
        targets = args.episodes
    else:
        targets = sorted(int(re.search(r"ep(\d+)", f.name).group(1)) for f in DRAFTS.glob("ep*.md"))

    rendered = 0
    for n in targets:
        try:
            html_text = render_episode(n, episodes, DRAFTS, template)
        except FileNotFoundError as e:
            print(f"[SKIP] ep{n:03d}: {e}")
            continue
        out_path = args.out_dir / f"ep{n:03d}.html"
        out_path.write_text(html_text, encoding="utf-8")
        print(f"[render] ep{n:03d} -> {out_path}")
        rendered += 1
    print(f"Total rendered: {rendered}")


if __name__ == "__main__":
    main()
