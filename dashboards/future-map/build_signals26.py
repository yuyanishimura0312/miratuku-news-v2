#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""シグナル一覧（26領域版）を組む。index.html（18テーマ版）の 26領域版。

★データは既存資産だけを使う。新しい割当を発明しない。
  - 26領域・8メタ領域 : gta-2026/gta_map2_full.json（GTA の結果。★これが唯一の実体）
  - 領域別シグナル      : gta-2026/enrichment.json（埋め込み類似度で機械的に紐付けたもの）
  - 出典・型・PESTLE   : signal.db → pestle.db の記事へ join して**実URL**まで解決する
    ★18テーマ版は出典を持っていない。ここが 26領域版で足す唯一の新しい情報。

★enrichment.json は上書きしない（domain-map / dashboard も参照しているため）。
★数値は焼き込まず、すべてここで数え直して埋める。
"""
import json
import os
import re
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime
from html import escape as esc

HERE = os.path.dirname(os.path.abspath(__file__))
GTA = os.path.expanduser(
    "~/Documents/miratuku-materials/04_レポート分析/miratuku-18themes-signals/gta-2026")
MAP_JSON = os.path.join(GTA, "gta_map2_full.json")
ENR_JSON = os.path.join(GTA, "enrichment.json")
SIGDB = os.path.expanduser("~/projects/research/pestle-signal-db/data/signal.db")
PESDB = os.path.expanduser("~/projects/research/pestle-signal-db/data/pestle.db")
OUT = os.path.join(HERE, "signals-26.html")

TYPE_JA = {
    "weak_signal": "弱いシグナル", "emerging_trend": "萌芽トレンド",
    "paradigm_shift": "パラダイム転換", "wild_card": "ワイルドカード",
    "counter_trend": "対抗トレンド", "CROSSOVER_CI": "文化との交差",
    "SANGAKU_LINK": "産学の接続", "EMERGENCE": "語彙の出現",
    "SURGE_PESTLE": "報道の急増", "systemic": "系の変化",
}
IMP_JA = {"critical": "重大", "high": "大", "medium": "中", "low": "小"}
CLA_JA = {"litany": "現象", "systemic": "体系的原因", "worldview": "世界観", "myth": "神話"}
TH_JA = {"H1": "H1 近未来", "H2": "H2 中期", "H3": "H3 長期"}


def norm_cla(v):
    v = (v or "").strip()
    for k in CLA_JA:
        if v.startswith(k):
            return k
    return ""


def main():
    M = json.load(open(MAP_JSON, encoding="utf-8"))
    DOMS = M["domains"]
    METAS = M["meta_categories"]
    ENR = json.load(open(ENR_JSON, encoding="utf-8"))

    sg = sqlite3.connect("file:%s?mode=ro" % SIGDB, uri=True)
    sg.row_factory = sqlite3.Row
    sg.execute("attach database ? as pe", ("file:%s?mode=ro" % PESDB,))

    # ── enrichment のシグナル名 → signal.db の行（型・PESTLE・対抗）を引く ──
    slots = [(int(k), s) for k, v in ENR.items() for s in v["signals"]]
    names = sorted({s["name"] for _, s in slots})
    ph = ",".join("?" * len(names))
    meta_by_name = {}
    for r in sg.execute(
            "SELECT signal_name,id,signal_type,pestle_categories,counter_trend,"
            "detected_date,signal_period FROM signals WHERE signal_name IN (%s)" % ph, names):
        # 同名が複数ある場合は最初の1件（6件のみ。IDの小さい方を採る）
        meta_by_name.setdefault(r["signal_name"], dict(r))

    # ── 出典（記事URL）。★隔離された記事は除く ──
    ids = [m["id"] for m in meta_by_name.values()]
    qi = ",".join("?" * len(ids))
    src = defaultdict(list)
    for r in sg.execute("""
        SELECT l.signal_id, a.title, a.title_ja, a.source, a.url, a.published_date
        FROM signal_article_links l
        JOIN pe.articles a ON a.url_hash = l.article_url_hash
        LEFT JOIN pe.synthetic_provenance q ON q.url_hash = l.article_url_hash
        WHERE l.signal_id IN (%s) AND q.url_hash IS NULL
          AND a.url IS NOT NULL AND a.url <> ''
        ORDER BY a.published_date DESC""" % qi, ids):
        src[r["signal_id"]].append(
            {"t": (r["title_ja"] or r["title"] or "")[:110], "s": r["source"] or "",
             "u": r["url"], "d": (r["published_date"] or "")[:10]})

    # ── 横断シグナル（複数領域に現れるもの）を数える ──
    dom_of = defaultdict(set)
    for did, s in slots:
        dom_of[s["name"]].add(did)

    # ── 出力データを組む ──
    meta_order = [m["name_ja"] for m in METAS]
    by_id = {d["id"]: d for d in DOMS}
    out = []
    for m in METAS:
        for did in m["domain_ids"]:
            d = by_id[did]
            e = ENR.get(str(did), {})
            sigs = []
            for s in e.get("signals", []):
                mm = meta_by_name.get(s["name"], {})
                sid = mm.get("id")
                try:
                    pes = json.loads(mm.get("pestle_categories") or "[]")
                except Exception:
                    pes = []
                sigs.append({
                    "name": s["name"], "desc": s["desc"], "period": s.get("period", ""),
                    "impact": s.get("impact", ""), "h": s.get("h", ""),
                    "cla": norm_cla(s.get("cla")), "score": s.get("score"),
                    "headline": s.get("headline", ""),
                    "type": mm.get("signal_type", ""),
                    "counter": (mm.get("counter_trend") or "")[:160],
                    "pestle": pes[:4],
                    "cross": sorted(dom_of[s["name"]]) if len(dom_of[s["name"]]) > 1 else [],
                    "src": src.get(sid, [])[:3],
                })
            out.append({
                "id": did, "title": d["name_ja"], "en": d.get("name_en", ""),
                "meta": d["meta"], "ov": d.get("overview", ""),
                "labels": d.get("member_labels", []), "weight": d.get("weight_full", d.get("weight", 0)),
                "accel": e.get("accel", {}), "signals": sigs,
            })

    # ── 実測（★焼き込まない） ──
    n_slot = sum(len(x["signals"]) for x in out)
    n_uniq = len({s["name"] for x in out for s in x["signals"]})
    n_cross = sum(1 for n, ds in dom_of.items() if len(ds) > 1)
    n_with_src = len({s["name"] for x in out for s in x["signals"] if s["src"]})
    periods = [s["period"] for x in out for s in x["signals"] if re.match(r"^\d{4}-\d{2}-\d{2}$", s["period"] or "")]
    win = (min(periods), max(periods)) if periods else ("", "")
    dd = [meta_by_name[n]["detected_date"] for n in meta_by_name if meta_by_name[n]["detected_date"]]
    dwin = (min(dd)[:10], max(dd)[:10]) if dd else ("", "")
    enr_stamp = datetime.fromtimestamp(os.path.getmtime(ENR_JSON)).strftime("%Y-%m-%d")
    stats = {
        "domains": len(out), "metas": len(METAS), "slots": n_slot, "uniq": n_uniq,
        "cross": n_cross, "with_src": n_with_src, "win": win, "dwin": dwin,
        "enr_stamp": enr_stamp, "corpus": M.get("corpus_full"),
        "method": M.get("method_full", ""),
    }
    return out, METAS, stats


if __name__ == "__main__":
    data, metas, st = main()
    print(json.dumps(st, ensure_ascii=False, indent=2))
    json.dump({"data": data, "metas": metas, "stats": st},
              open(os.path.join(HERE, "_signals26.json"), "w", encoding="utf-8"),
              ensure_ascii=False)
    print("wrote _signals26.json")
