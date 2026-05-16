#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_strategy.py — strategy.db -> strategy.html レンダラー

設計:
  - templates/strategy_head.html (head + body + main + section-header + 3トップタブ)
  - DB から panels を sort_order で取得し、各 panel に対し
      <div class="strategy-top-panel{ ' active' if is_active else ''}" id="top-{panel_id}">
        {meta_blocks.content_html (scope_type='panel', scope_id=panel_id, block_type='inner_html')}
      </div>
    を生成
  - templates/strategy_foot.html (</section> </main> + footer + 元の tab JS)

ポイント:
  - 元の html_inner を信用 (Strategy-A が DOM 完全抽出している)
  - インラインstyle / DOM ID / クラスは元 HTML のまま保存
  - タブ切替 JS / Web Fonts / favicon / firebase は templates が保持

CLI:
  python3 scripts/render_strategy.py
  python3 scripts/render_strategy.py --output strategy_generated.html
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = ROOT / "data" / "strategy.db"
DEFAULT_HEAD = ROOT / "templates" / "strategy_head.html"
DEFAULT_FOOT = ROOT / "templates" / "strategy_foot.html"
DEFAULT_OUTPUT = ROOT / "strategy.html"


def _connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def render_body(conn: sqlite3.Connection) -> str:
    panels = list(
        conn.execute(
            "SELECT panel_id, label, is_active FROM panels ORDER BY sort_order, panel_id"
        )
    )
    pieces: List[str] = []
    for p in panels:
        panel_id = p["panel_id"]
        label = p["label"]
        is_active = bool(p["is_active"])
        # Retrieve html_inner from meta_blocks
        row = conn.execute(
            "SELECT content_html FROM meta_blocks "
            "WHERE scope_type='panel' AND scope_id=? AND block_type='inner_html' "
            "ORDER BY sort_order LIMIT 1",
            (panel_id,),
        ).fetchone()
        inner = (row["content_html"] if row else "") or ""
        # Strip leading newline (Strategy-A emits "\n" at start)
        inner_stripped = inner.lstrip("\n")
        # Comment + opening tag (mirror original strategy.html format)
        comment = f"      <!-- =========================== {label} =========================== -->"
        opening = (
            f'      <div class="strategy-top-panel active" id="top-{panel_id}">'
            if is_active
            else f'      <div class="strategy-top-panel" id="top-{panel_id}">'
        )
        closing = "      </div>"
        pieces.append(
            f"{comment}\n{opening}\n{inner_stripped.rstrip()}\n{closing}"
        )
    # Join with blank line between panels
    return "\n\n".join(pieces)


def render(
    db_path: Path = DEFAULT_DB,
    head_path: Path = DEFAULT_HEAD,
    foot_path: Path = DEFAULT_FOOT,
    output_path: Path = DEFAULT_OUTPUT,
) -> int:
    for label, p in (
        ("db", db_path),
        ("head template", head_path),
        ("foot template", foot_path),
    ):
        if not p.exists():
            sys.stderr.write(f"[render] ERROR: {label} not found: {p}\n")
            return 2

    head = head_path.read_text(encoding="utf-8")
    foot = foot_path.read_text(encoding="utf-8")

    conn = _connect(db_path)
    try:
        body = render_body(conn)
    finally:
        conn.close()

    # Concatenate with deterministic separators matching original strategy.html
    parts = []
    parts.append(head.rstrip("\n"))
    parts.append("\n\n")
    parts.append(body.rstrip("\n"))
    parts.append("\n\n")
    parts.append(foot)
    out = "".join(parts)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(out, encoding="utf-8")
    size = output_path.stat().st_size
    print(f"[render] OK wrote: {output_path}  ({size:,} bytes)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Render strategy.db -> strategy.html")
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--head", type=Path, default=DEFAULT_HEAD)
    ap.add_argument("--foot", type=Path, default=DEFAULT_FOOT)
    ap.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="出力 HTML パス (デフォルト: strategy.html を上書き)",
    )
    args = ap.parse_args()
    return render(args.db, args.head, args.foot, args.output)


if __name__ == "__main__":
    sys.exit(main())
