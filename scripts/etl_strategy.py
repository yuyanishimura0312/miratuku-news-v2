#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
etl_strategy.py — strategy.html DB化 ETL

入力:
  data/strategy_content.json  (Strategy-A 抽出済み JSON)
  data/strategy_schema.sql    (Strategy-B 設計済み DDL)

処理:
  1. SQLite DB を作成 (data/strategy.db) — 既存なら drop して再構築
  2. スキーマを apply
  3. JSON → 6テーブルへ INSERT
     - panels        : 3 panels (strategy / content / themes)
     - cpanels       : 7 subpanels
     - sections      : すべての非 part_section セクションを構造化保存
     - parts         : part_section を分離
     - episodes      : part_section.episodes を分離
     - meta_blocks   : 各 panel / cpanel の html_inner を保存 (renderer 用)
  4. トランザクション中で全 INSERT。エラー時はロールバック。

CLI:
  python3 scripts/etl_strategy.py
  python3 scripts/etl_strategy.py --json data/strategy_content.json --schema data/strategy_schema.sql --db data/strategy.db
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JSON = ROOT / "data" / "strategy_content.json"
DEFAULT_SCHEMA = ROOT / "data" / "strategy_schema.sql"
FALLBACK_SCHEMA = ROOT / "templates" / "strategy_schema_reference.sql"
DEFAULT_DB = ROOT / "data" / "strategy.db"


def _load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"strategy_content.json not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _load_schema(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    if FALLBACK_SCHEMA.exists():
        sys.stderr.write(
            f"[etl] WARN: {path} missing, using fallback {FALLBACK_SCHEMA}\n"
        )
        return FALLBACK_SCHEMA.read_text(encoding="utf-8")
    raise FileNotFoundError(
        f"Schema not found: {path} (no fallback at {FALLBACK_SCHEMA})"
    )


def _j(v) -> Optional[str]:
    if v is None:
        return None
    if isinstance(v, str):
        return v
    return json.dumps(v, ensure_ascii=False, separators=(",", ":"))


def _drop_tables(conn: sqlite3.Connection) -> None:
    """Drop in dependency-safe order (FK + triggers + views)."""
    # Drop views first
    for v in ("v_strategy_tree", "v_episodes_status_summary"):
        conn.execute(f"DROP VIEW IF EXISTS {v}")
    # Drop triggers (will be re-created by schema)
    for t in (
        "trg_panels_updated_at",
        "trg_cpanels_updated_at",
        "trg_sections_updated_at",
        "trg_parts_updated_at",
        "trg_episodes_updated_at",
        "trg_metablocks_updated_at",
    ):
        conn.execute(f"DROP TRIGGER IF EXISTS {t}")
    # Drop tables in dependency order
    for t in (
        "meta_blocks",
        "episodes",
        "parts",
        "sections",
        "cpanels",
        "panels",
    ):
        conn.execute(f"DROP TABLE IF EXISTS {t}")


def insert_panels(conn: sqlite3.Connection, panels: List[Dict[str, Any]]) -> int:
    count = 0
    for p in panels:
        conn.execute(
            "INSERT INTO panels (panel_id, label, sort_order, is_active, metadata_json) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                p["panel_id"],
                p["label"],
                int(p.get("sort_order", 0)),
                int(bool(p.get("active", False))),
                _j(
                    {
                        "panel_type": p.get("panel_type"),
                        "extracted_html_inner_len": len(p.get("html_inner", "")),
                    }
                ),
            ),
        )
        count += 1
    return count


def insert_cpanels(conn: sqlite3.Connection, panels: List[Dict[str, Any]]) -> int:
    count = 0
    for p in panels:
        for sp in p.get("subpanels", []):
            conn.execute(
                "INSERT INTO cpanels (cpanel_id, parent_panel_id, label, series_name, "
                "total_episodes, status_summary, sort_order, is_active, metadata_json) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    sp["cpanel_id"],
                    p["panel_id"],
                    sp["label"],
                    sp.get("series_name"),
                    sp.get("total_episodes"),
                    sp.get("status_summary"),
                    int(sp.get("sort_order", 0)),
                    int(bool(sp.get("tab_active") or sp.get("active") or False)),
                    _j(
                        {
                            "panel_kind": sp.get("panel_kind"),
                            "html_inner_len": len(sp.get("html_inner", "")),
                        }
                    ),
                ),
            )
            count += 1
    return count


def insert_sections_and_parts(
    conn: sqlite3.Connection,
    panels: List[Dict[str, Any]],
) -> Dict[str, int]:
    """Sections / Parts / Episodes を分離して INSERT。"""
    sec_count = 0
    parts_count = 0
    eps_count = 0

    def emit_section(
        sec: Dict[str, Any],
        *,
        sort_order: int,
        cpanel_id: Optional[str],
        panel_id: Optional[str],
    ) -> None:
        nonlocal sec_count
        # JSON はやや異なるキー使い: type / section_type 双方ありうる
        section_type = sec.get("section_type") or sec.get("type") or "raw"
        conn.execute(
            "INSERT INTO sections (cpanel_id, panel_id, section_type, dom_id, title, "
            "subtitle, body_html, sort_order, metadata_json) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                cpanel_id,
                panel_id,
                section_type,
                sec.get("dom_id"),
                sec.get("title"),
                sec.get("subtitle") or sec.get("title_en"),
                sec.get("html") or sec.get("body_html"),
                sort_order,
                _j(
                    {
                        k: v
                        for k, v in sec.items()
                        if k
                        not in (
                            "section_type",
                            "type",
                            "dom_id",
                            "title",
                            "subtitle",
                            "title_en",
                            "html",
                            "body_html",
                            "parts",
                            "episodes",
                        )
                    }
                ),
            ),
        )
        sec_count += 1

    def emit_part(
        sec: Dict[str, Any],
        *,
        sort_order: int,
        cpanel_id: str,
    ) -> None:
        nonlocal parts_count
        part_id = sec.get("part_id") or f"{cpanel_id}-part-{sort_order}"
        conn.execute(
            "INSERT INTO parts (part_id, cpanel_id, part_label, part_title, era, "
            "ep_range_start, ep_range_end, sort_order, banner_html, metadata_json) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                part_id,
                cpanel_id,
                sec.get("part_label") or "",
                sec.get("part_title") or "",
                sec.get("era"),
                sec.get("ep_range_start"),
                sec.get("ep_range_end"),
                sort_order,
                sec.get("banner_html"),
                _j({"part_stats": sec.get("part_stats")}),
            ),
        )
        parts_count += 1
        # Episodes
        for i, ep in enumerate(sec.get("episodes", [])):
            insert_episode(ep, part_id=part_id, cpanel_id=cpanel_id, sort_order=i)

    def insert_episode(
        ep: Dict[str, Any],
        *,
        part_id: Optional[str],
        cpanel_id: str,
        sort_order: int,
    ) -> None:
        nonlocal eps_count
        meta = {
            k: v
            for k, v in ep.items()
            if k
            not in (
                "ep_num",
                "title",
                "url",
                "status",
                "subtitle",
                "summary",
                "published_at",
            )
        }
        conn.execute(
            "INSERT INTO episodes (part_id, cpanel_id, ep_num, title, url, status, "
            "summary, sort_order, published_at, metadata_json) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                part_id,
                cpanel_id,
                ep.get("ep_num"),
                ep.get("title") or "",
                ep.get("url"),
                ep.get("status"),
                ep.get("subtitle") or ep.get("summary"),
                sort_order,
                ep.get("published_at"),
                _j(meta) if meta else None,
            ),
        )
        eps_count += 1

    for p in panels:
        # Panel-level sections (themes panel has these)
        for i, sec in enumerate(p.get("sections", []) or []):
            stype = sec.get("section_type") or sec.get("type")
            if stype == "part_section":
                # Edge case: panel-level part_section — drop into sections only
                emit_section(sec, sort_order=i, cpanel_id=None, panel_id=p["panel_id"])
            else:
                emit_section(sec, sort_order=i, cpanel_id=None, panel_id=p["panel_id"])

        # Sub-panel sections
        for sp in p.get("subpanels", []):
            cpid = sp["cpanel_id"]
            for i, sec in enumerate(sp.get("sections", []) or []):
                stype = sec.get("section_type") or sec.get("type")
                if stype == "part_section":
                    emit_part(sec, sort_order=i, cpanel_id=cpid)
                else:
                    emit_section(
                        sec, sort_order=i, cpanel_id=cpid, panel_id=None
                    )

    return {"sections": sec_count, "parts": parts_count, "episodes": eps_count}


def insert_meta_blocks(
    conn: sqlite3.Connection, panels: List[Dict[str, Any]]
) -> int:
    """html_inner を meta_blocks に格納 (renderer 用の真実層)。"""
    count = 0
    for p in panels:
        html_inner = p.get("html_inner") or ""
        if html_inner:
            conn.execute(
                "INSERT INTO meta_blocks (scope_type, scope_id, block_type, "
                "content_html, sort_order, metadata_json) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                ("panel", p["panel_id"], "inner_html", html_inner, 0, None),
            )
            count += 1
        for sp in p.get("subpanels", []):
            sp_inner = sp.get("html_inner") or ""
            if sp_inner:
                conn.execute(
                    "INSERT INTO meta_blocks (scope_type, scope_id, block_type, "
                    "content_html, sort_order, metadata_json) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    ("cpanel", sp["cpanel_id"], "inner_html", sp_inner, 0, None),
                )
                count += 1
    return count


def run_etl(
    json_path: Path = DEFAULT_JSON,
    schema_path: Path = DEFAULT_SCHEMA,
    db_path: Path = DEFAULT_DB,
) -> Dict[str, int]:
    data = _load_json(json_path)
    schema_sql = _load_schema(schema_path)
    panels = data.get("panels", [])

    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    try:
        # Clean rebuild
        conn.execute("PRAGMA foreign_keys = OFF")  # disable for drops
        with conn:
            _drop_tables(conn)
            conn.executescript(schema_sql)
        conn.execute("PRAGMA foreign_keys = ON")

        counts: Dict[str, int] = {}
        with conn:
            counts["panels"] = insert_panels(conn, panels)
            counts["cpanels"] = insert_cpanels(conn, panels)
            sub = insert_sections_and_parts(conn, panels)
            counts["sections"] = sub["sections"]
            counts["parts"] = sub["parts"]
            counts["episodes"] = sub["episodes"]
            counts["meta_blocks"] = insert_meta_blocks(conn, panels)
    finally:
        conn.close()
    return counts


def main() -> int:
    ap = argparse.ArgumentParser(description="ETL: strategy_content.json -> strategy.db")
    ap.add_argument("--json", type=Path, default=DEFAULT_JSON)
    ap.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    args = ap.parse_args()
    try:
        counts = run_etl(args.json, args.schema, args.db)
    except FileNotFoundError as e:
        sys.stderr.write(f"[etl] ERROR: {e}\n")
        return 2
    except Exception as e:
        sys.stderr.write(f"[etl] ERROR during ETL: {type(e).__name__}: {e}\n")
        return 1
    print("[etl] OK clean-build complete")
    for t, n in counts.items():
        print(f"  {t:12s} : {n:6d}")
    print(f"[etl] DB written: {args.db}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
