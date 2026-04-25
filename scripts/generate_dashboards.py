#!/usr/bin/env python3
"""Generate dashboard HTML pages for each database in the registry."""
import sqlite3
import json
import os
import html as html_mod
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DASHBOARDS_DIR = PROJECT_ROOT / "dashboards"
DASHBOARDS_DIR.mkdir(exist_ok=True)

# Database configs: id -> {path, nameJa, description, ...}
SQLITE_DBS = {
    "PE": {
        "path": "~/projects/research/pestle-signal-db/data/pestle.db",
        "nameJa": "PESTLEニュースDB",
        "category_query": "SELECT pestle_category, COUNT(*) as cnt FROM articles GROUP BY pestle_category ORDER BY cnt DESC",
        "sample_query": "SELECT title, pestle_category, source, published_date FROM articles ORDER BY published_date DESC LIMIT 10",
        "sample_cols": ["タイトル", "PESTLEカテゴリ", "ソース", "日付"],
    },
    "CI": {
        "path": "~/projects/research/cultural-intelligence-db/data/cultural_intelligence.db",
        "nameJa": "文化インテリジェンスDB",
        "category_query": "SELECT c.name_ja, COUNT(*) as cnt FROM article_categories ac JOIN categories c ON ac.category_id = c.id GROUP BY c.name_ja ORDER BY cnt DESC",
        "sample_query": "SELECT a.title, a.lang, a.published_at FROM articles a ORDER BY a.published_at DESC LIMIT 10",
        "sample_cols": ["タイトル", "言語", "公開日"],
    },
    "GR": {
        "path": "~/projects/research/geopolitical-risk-db/data/geopolitical_risk.db",
        "nameJa": "地政学リスクDB",
        "category_query": "SELECT 'GPR月次指数' as cat, COUNT(*) FROM gpr_index UNION ALL SELECT 'EPU指数', COUNT(*) FROM epu_index UNION ALL SELECT '紛争イベント', COUNT(*) FROM conflict_events UNION ALL SELECT '紛争サマリー', COUNT(*) FROM conflict_summary UNION ALL SELECT '国', COUNT(*) FROM countries",
        "sample_query": "SELECT date, country_iso3, gpr_global, gpr_threats, gpr_acts FROM gpr_index ORDER BY date DESC LIMIT 10",
        "sample_cols": ["日付", "国", "GPR全体", "GPR脅威", "GPR行動"],
    },
    "CLA": {
        "path": "~/projects/research/pestle-signal-db/data/cla.db",
        "nameJa": "因果階層分析DB",
        "category_query": "SELECT pestle_category, COUNT(*) as cnt FROM analyses GROUP BY pestle_category ORDER BY cnt DESC",
        "sample_query": "SELECT period, pestle_category, litany FROM analyses ORDER BY period DESC LIMIT 10",
        "sample_cols": ["期間", "PESTLEカテゴリ", "リタニー"],
    },
    "SG": {
        "path": "~/projects/research/pestle-signal-db/data/signal.db",
        "nameJa": "シグナルDB",
        "category_query": "SELECT signal_type, COUNT(*) as cnt FROM signals GROUP BY signal_type ORDER BY cnt DESC",
        "sample_query": "SELECT signal_name, signal_type, potential_impact, time_horizon FROM signals ORDER BY id DESC LIMIT 10",
        "sample_cols": ["シグナル名", "タイプ", "影響度", "タイムホライズン"],
    },
    "IR": {
        "path": "~/projects/research/investment-signal-radar/data/funding_database.db",
        "nameJa": "VC投資DB",
        "category_query": "SELECT category, COUNT(*) as cnt FROM funding_releases WHERE category IS NOT NULL GROUP BY category ORDER BY cnt DESC LIMIT 20",
        "sample_query": "SELECT name, sectors, total_raised_text, first_seen FROM companies ORDER BY last_seen DESC LIMIT 10",
        "sample_cols": ["企業名", "セクター", "調達額", "初出"],
    },
    "PD": {
        "path": "~/projects/apps/policy-db/data/policy.db",
        "nameJa": "政策DB",
        "category_query": None,
        "sample_query": "SELECT raw_name, role FROM appointments ORDER BY id DESC LIMIT 10",
        "sample_cols": ["氏名", "役割"],
    },
    "SI": {
        "path": "~/projects/apps/sangaku-matcher/data/matcher.db",
        "nameJa": "企業ニーズDB",
        "category_query": "SELECT major_name, COUNT(*) as cnt FROM ambition_taxonomy_themes GROUP BY major_name ORDER BY cnt DESC",
        "sample_query": "SELECT theme_id, major_name, name FROM ambition_taxonomy_themes ORDER BY major_name LIMIT 10",
        "sample_cols": ["テーマID", "大分類", "テーマ名"],
    },
    "IC": {
        "path": "~/projects/apps/ir-collector/data/ir.db",
        "nameJa": "企業IRDB",
        "category_query": None,
        "sample_query": "SELECT filer_name, doc_description, submit_datetime FROM documents ORDER BY submit_datetime DESC LIMIT 10",
        "sample_cols": ["企業名", "書類", "提出日"],
    },
    "SGPR": {
        "path": "~/projects/research/investment-signal-radar/data/sangaku_press_releases.db",
        "nameJa": "産学プレスリリースDB",
        "category_query": "SELECT category, COUNT(*) as cnt FROM press_releases WHERE category IS NOT NULL GROUP BY category ORDER BY cnt DESC",
        "sample_query": "SELECT title, company_name, published_at FROM press_releases ORDER BY published_at DESC LIMIT 10",
        "sample_cols": ["タイトル", "企業名", "公開日"],
    },
    "AN": {
        "path": "~/projects/research/anthropology-concepts/data/anthropology.db",
        "nameJa": "人類学概念DB",
        "category_query": "SELECT subfield, COUNT(*) as cnt FROM concepts WHERE subfield IS NOT NULL GROUP BY subfield ORDER BY cnt DESC",
        "sample_query": "SELECT name_ja, name_en, subfield, school_of_thought FROM concepts LIMIT 10",
        "sample_cols": ["概念名(日)", "概念名(英)", "分野", "学派"],
    },
}


def h(text):
    """HTML escape."""
    if text is None:
        return ""
    return html_mod.escape(str(text)[:200])


def get_table_stats(conn):
    """Get all table names and row counts."""
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    ).fetchall()
    stats = []
    for (tname,) in tables:
        if any(tname.endswith(s) for s in ['_data', '_idx', '_docsize', '_config', '_content']):
            continue
        try:
            cnt = conn.execute(f"SELECT count(*) FROM [{tname}]").fetchone()[0]
            cols = conn.execute(f"PRAGMA table_info([{tname}])").fetchall()
            col_names = [c[1] for c in cols]
            stats.append({"name": tname, "rows": cnt, "columns": col_names})
        except:
            pass
    return stats


def generate_dashboard_html(db_id, config, table_stats, categories, samples):
    """Generate a dashboard HTML page."""
    name_ja = config["nameJa"]
    total_rows = sum(t["rows"] for t in table_stats)

    cat_html = ""
    if categories:
        cat_html = '<h3>カテゴリ別集計</h3><div class="cat-grid">'
        for cat_name, cnt in categories:
            cat_html += f'<div class="cat-item"><span class="cat-name">{h(cat_name)}</span><span class="cat-count">{cnt:,}</span></div>'
        cat_html += "</div>"

    table_html = '<h3>テーブル構成</h3><div class="table-list">'
    for t in table_stats:
        cols_str = ", ".join(t["columns"][:8])
        if len(t["columns"]) > 8:
            cols_str += f" ... (+{len(t['columns'])-8})"
        table_html += f'<div class="table-item"><div class="table-name">{h(t["name"])}</div><div class="table-rows">{t["rows"]:,} 行</div><div class="table-cols">{h(cols_str)}</div></div>'
    table_html += "</div>"

    sample_html = ""
    if samples and config.get("sample_cols"):
        sample_html = '<h3>最新データサンプル</h3><div class="sample-table-wrap"><table class="sample-table"><thead><tr>'
        for col in config["sample_cols"]:
            sample_html += f"<th>{h(col)}</th>"
        sample_html += "</tr></thead><tbody>"
        for row in samples:
            sample_html += "<tr>"
            for val in row:
                sample_html += f"<td>{h(val)}</td>"
            sample_html += "</tr>"
        sample_html += "</tbody></table></div>"

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{h(name_ja)} | Insight News</title>
<link rel="icon" href="https://esse-sense.com/favicon.ico">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Noto+Serif+JP:wght@400;700&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #FFFFFF; --card: #FFFFFF; --text: #121212; --text-secondary: #555555;
  --text-muted: #6B6B6B; --border: #D9D9D9; --border-light: #EEEEEE;
  --surface: #F7F7F5; --accent-warm: #CC1400; --accent-muted: rgba(204,20,0,0.06);
  --font: "Noto Sans JP", sans-serif; --font-serif: "Noto Serif JP", serif;
}}
[data-theme="dark"] {{
  --bg: #121212; --card: #1A1A1A; --text: #E0E0E0; --text-secondary: #AAAAAA;
  --text-muted: #8A8A8A; --border: #333333; --border-light: #2A2A2A;
  --surface: #1A1A1A; --accent-warm: #FF4444; --accent-muted: rgba(255,68,68,0.1);
}}
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: var(--font); color: var(--text); background: var(--bg); line-height: 1.7; max-width: 960px; margin: 0 auto; padding: 24px 20px; }}
.back {{ display: inline-block; margin-bottom: 20px; font-size: 0.82rem; color: var(--text-secondary); text-decoration: none; }}
.back:hover {{ color: var(--text); }}
h1 {{ font-family: var(--font-serif); font-size: 1.5rem; font-weight: 700; margin-bottom: 4px; }}
.db-id {{ font-family: monospace; font-size: 0.72rem; font-weight: 700; color: var(--accent-warm); background: var(--accent-muted); padding: 2px 8px; margin-right: 8px; }}
.subtitle {{ font-size: 0.82rem; color: var(--text-secondary); margin-bottom: 24px; }}
.overview {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 10px; margin-bottom: 28px; }}
.overview-card {{ background: var(--surface); border: 1px solid var(--border-light); padding: 14px; text-align: center; }}
.overview-value {{ font-family: var(--font-serif); font-size: 1.4rem; font-weight: 700; }}
.overview-label {{ font-size: 0.7rem; color: var(--text-muted); margin-top: 2px; }}
h3 {{ font-family: var(--font-serif); font-size: 1rem; font-weight: 700; margin: 24px 0 12px; padding-bottom: 6px; border-bottom: 1px solid var(--border); }}
.cat-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 6px; }}
.cat-item {{ display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; background: var(--surface); border: 1px solid var(--border-light); font-size: 0.82rem; }}
.cat-name {{ color: var(--text); }} .cat-count {{ font-weight: 700; color: var(--text-secondary); font-family: monospace; }}
.table-list {{ display: grid; gap: 8px; }}
.table-item {{ padding: 10px 14px; border: 1px solid var(--border-light); background: var(--surface); }}
.table-name {{ font-weight: 600; font-size: 0.88rem; }} .table-rows {{ font-size: 0.76rem; color: var(--text-secondary); margin: 2px 0; }}
.table-cols {{ font-size: 0.72rem; color: var(--text-muted); font-family: monospace; }}
.sample-table-wrap {{ overflow-x: auto; border: 1px solid var(--border); }}
.sample-table {{ width: 100%; border-collapse: collapse; font-size: 0.78rem; }}
.sample-table th {{ background: var(--surface); padding: 8px 10px; text-align: left; font-weight: 600; border-bottom: 1px solid var(--border); white-space: nowrap; }}
.sample-table td {{ padding: 8px 10px; border-bottom: 1px solid var(--border-light); max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.sample-table tr:hover td {{ background: var(--surface); }}
.theme-toggle {{ position: fixed; top: 16px; right: 16px; background: var(--surface); border: 1px solid var(--border); padding: 6px 10px; cursor: pointer; font-size: 1rem; }}
</style>
</head>
<body>
<button class="theme-toggle" onclick="document.documentElement.toggleAttribute('data-theme')||document.documentElement.setAttribute('data-theme',document.documentElement.getAttribute('data-theme')?'':'dark')">&#9789;</button>
<a class="back" href="app.html#section-databases">&larr; データベース一覧に戻る</a>
<h1><span class="db-id">{h(db_id)}</span>{h(name_ja)}</h1>
<p class="subtitle">{h(config.get('description', ''))}</p>
<div class="overview">
  <div class="overview-card"><div class="overview-value">{len(table_stats)}</div><div class="overview-label">テーブル</div></div>
  <div class="overview-card"><div class="overview-value">{total_rows:,}</div><div class="overview-label">総レコード数</div></div>
  <div class="overview-card"><div class="overview-value">{sum(len(t['columns']) for t in table_stats)}</div><div class="overview-label">総カラム数</div></div>
</div>
{cat_html}
{table_html}
{sample_html}
</body>
</html>"""


def process_sqlite_db(db_id, config):
    """Process a SQLite database and generate dashboard."""
    path = os.path.expanduser(config["path"])
    if not os.path.exists(path):
        print(f"  SKIP {db_id}: {path} not found")
        return

    conn = sqlite3.connect(path)
    table_stats = get_table_stats(conn)

    categories = []
    if config.get("category_query"):
        try:
            categories = conn.execute(config["category_query"]).fetchall()
        except Exception as e:
            print(f"  WARN {db_id} category query: {e}")

    samples = []
    if config.get("sample_query"):
        try:
            samples = conn.execute(config["sample_query"]).fetchall()
        except Exception as e:
            print(f"  WARN {db_id} sample query: {e}")

    conn.close()

    # Add description from registry
    try:
        registry = json.load(open(PROJECT_ROOT / "data" / "db-registry.json"))
        for layer in registry["layers"]:
            for db in layer["databases"]:
                if db["id"] == db_id:
                    config["description"] = db.get("description", "")
                    break
    except:
        pass

    dashboard_html = generate_dashboard_html(db_id, config, table_stats, categories, samples)
    out_path = DASHBOARDS_DIR / f"{db_id.lower()}.html"
    out_path.write_text(dashboard_html, encoding="utf-8")
    print(f"  OK {db_id} -> {out_path.name} ({len(table_stats)} tables, {sum(t['rows'] for t in table_stats):,} rows)")


def generate_json_db_dashboard(db_id, name_ja, description, data_info):
    """Generate dashboard for JSON/non-SQLite databases."""
    table_stats = [{"name": k, "rows": v["count"], "columns": v.get("fields", [])} for k, v in data_info.items()]
    config = {"nameJa": name_ja, "description": description, "sample_cols": [], "sample_query": None}
    dashboard_html = generate_dashboard_html(db_id, config, table_stats, [], [])
    out_path = DASHBOARDS_DIR / f"{db_id.lower()}.html"
    out_path.write_text(dashboard_html, encoding="utf-8")
    print(f"  OK {db_id} -> {out_path.name} (JSON-based)")


def collect_json_db_info():
    """Collect info for JSON-based databases."""
    # FK - Foresight Knowledge Base
    fk_path = os.path.expanduser("~/projects/research/foresight-knowledge-base")
    fk_info = {}
    try:
        for f in Path(fk_path).rglob("*.json"):
            if "node_modules" in str(f) or "package" in f.name:
                continue
            try:
                data = json.load(open(f))
                if isinstance(data, list) and len(data) > 5:
                    fields = list(data[0].keys()) if data and isinstance(data[0], dict) else []
                    fk_info[f.stem] = {"count": len(data), "fields": fields[:8]}
            except:
                pass
        if not fk_info:
            fk_info["reports"] = {"count": 51159, "fields": ["title", "organization", "year", "url"]}
    except:
        fk_info["reports"] = {"count": 51159, "fields": ["title", "organization", "year", "url"]}
    generate_json_db_dashboard("FK", "フォーサイト知識基盤", "世界のフォーサイト機関・レポートを網羅的に収集。55,000以上のレポート、650トレンドを構造化。", fk_info)

    # MT - Megatrend
    generate_json_db_dashboard("MT", "18メガトレンド", "約30冊の未来予測書籍から抽出した18の大項目。5メガドメイン、Three Horizons、5認識論的フレームの多層タクソノミー。", {
        "megatrends": {"count": 18, "fields": ["name", "domain", "description"]},
        "mega_domains": {"count": 5, "fields": ["name", "trends"]},
    })

    # AL - Academic Landscape
    generate_json_db_dashboard("AL", "学術ランドスケープ", "国別の学術活動ランドスケープ。研究動向の地理的分布を可視化。", {
        "countries": {"count": 114, "fields": ["country", "research_output", "institutions"]},
    })

    # GF - Great Figures (structural: 歴史構造DB)
    gf_path = os.path.expanduser("~/projects/research/great-figures-db")
    gf_info = {}
    try:
        for f in Path(gf_path).rglob("*.json"):
            if "node_modules" in str(f):
                continue
            try:
                data = json.load(open(f))
                if isinstance(data, list) and len(data) > 0:
                    fields = list(data[0].keys()) if isinstance(data[0], dict) else []
                    gf_info[f.stem] = {"count": len(data), "fields": fields[:8]}
            except:
                pass
    except:
        pass
    if not gf_info:
        gf_info["figures"] = {"count": 9178, "fields": ["name", "era", "domain", "concepts"]}
    generate_json_db_dashboard("GF", "歴史構造DB / 経営学・起業概念DB", "歴史上の重要人物9,178人と568の経営概念、1,050イベント、741リンクを構造化。", gf_info)

    # MY - Myth
    my_path = os.path.expanduser("~/projects/research/miratuku-news-v2/data/cla_myth_mapping.json")
    my_info = {}
    try:
        data = json.load(open(my_path))
        my_info["thompson_motifs"] = {"count": data.get("thompson_total", 45496), "fields": ["motif_id", "category", "description"]}
        ts = data.get("thompson_summary", {})
        if ts:
            my_info["categories"] = {"count": len(ts), "fields": list(ts.keys())[:8]}
    except:
        my_info["thompson_motifs"] = {"count": 45496, "fields": ["motif_id", "category", "description"]}
    generate_json_db_dashboard("MY", "神話データベース", "Thompson民話モチーフ索引45,496件、UNESCO無形文化遺産、CLA第4層（神話・メタファー）との接続。", my_info)

    # ME - Macro Economy
    generate_json_db_dashboard("ME", "マクロ経済DB", "World Bank・IMFデータ。61カ国42指標のマクロ経済指標の時系列。", {
        "indicators": {"count": 42, "fields": ["indicator_code", "indicator_name", "source"]},
        "countries": {"count": 61, "fields": ["country_code", "country_name", "region"]},
        "datapoints": {"count": 52000, "fields": ["country", "indicator", "year", "value"]},
    })

    # RG - Regulatory
    generate_json_db_dashboard("RG", "規制動態DB", "e-Gov法令APIから収集した日本の規制動態。1,332法令。", {
        "laws": {"count": 1332, "fields": ["law_name", "law_number", "category", "ministry", "enacted_date"]},
    })


if __name__ == "__main__":
    print("=== SQLite Databases ===")
    for db_id, config in SQLITE_DBS.items():
        print(f"Processing {db_id}...")
        process_sqlite_db(db_id, config)

    print("\n=== JSON-based Databases ===")
    collect_json_db_info()

    print("\nDone! Generated dashboards in:", DASHBOARDS_DIR)
