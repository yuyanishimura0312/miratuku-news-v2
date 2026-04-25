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

PESTLE_JA = {"Political": "政治", "Economic": "経済", "Social": "社会", "Technological": "技術", "Legal": "法律", "Environmental": "環境"}
TABLE_JA = {
    # PE
    "articles": "ニュース記事", "cla_analyses": "CLA分析", "cla_meta_reports": "CLAメタレポート",
    "cla_syntheses": "CLA統合分析", "collections": "収集ログ", "daily_reports": "日次レポート",
    "db_meta": "メタデータ", "media_sources": "メディアソース", "quarterly_stats": "四半期統計",
    # CI
    "sources": "情報ソース", "article_categories": "記事カテゴリ紐付け", "categories": "カテゴリマスタ",
    "collection_stats": "収集統計",
    # GR
    "gpr_index": "GPR地政学リスク指数", "epu_index": "EPU経済政策不確実性指数",
    "conflict_events": "紛争イベント", "conflict_summary": "紛争サマリー", "countries": "国マスタ",
    # CLA
    "analyses": "CLA分析（v1）", "analyses_v2": "CLA分析（v2・CI統合版）",
    "annual_36yr": "36年分年次CLA", "keyword_index": "キーワード索引",
    "myths_timeline": "神話タイムライン", "paradigm_shifts": "パラダイムシフト",
    "cross_category_syntheses": "カテゴリ横断統合", "meta_reports": "メタレポート",
    # SG
    "signals": "シグナル", "alerts": "アラート", "scenarios": "シナリオ",
    "scenario_variants": "シナリオバリアント", "signal_article_links": "シグナル-記事リンク",
    "signal_cla_links": "シグナル-CLA連結", "signal_cross_impact": "シグナル相互影響",
    "signal_network_metrics": "ネットワーク指標",
    # IR
    "companies": "企業", "funding_releases": "資金調達リリース", "monthly_stats": "月次統計",
    # PD
    "ministries": "省庁", "councils": "審議会・委員会", "council_members": "委員",
    "persons": "有識者", "organizations": "組織", "appointments": "委員任命",
    "projects": "予算事業",
    # SI
    "ambition_taxonomy_themes": "企業志向テーマ", "ambition_taxonomy_proximity": "企業-テーマ近接度",
    "companies_master": "企業マスタ", "edinet_companies": "EDINET企業",
    # IC
    "documents": "IR書類", "collection_log": "収集ログ", "edinet_companies": "EDINET企業",
    # SGPR
    "press_releases": "プレスリリース", "metadata": "メタデータ",
    # AN
    "concepts": "人類学概念", "researchers": "研究者", "publications": "文献",
    "publication_authors": "著者", "ocm_categories": "OCM分類",
    "concept_ocm": "概念-OCMマッピング", "concept_researchers": "概念-研究者リンク",
    "concept_publications": "概念-文献リンク", "concept_relations": "概念間関係",
}


def h(text):
    if text is None:
        return ""
    return html_mod.escape(str(text)[:300])


def get_table_stats(conn):
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
            stats.append({"name": tname, "name_ja": TABLE_JA.get(tname, tname), "rows": cnt, "columns": col_names})
        except:
            pass
    return stats


def safe_query(conn, sql):
    try:
        return conn.execute(sql).fetchall()
    except:
        return []


CSS = """
:root {
  --bg: #FFFFFF; --card: #FFFFFF; --text: #121212; --text-secondary: #555555;
  --text-muted: #6B6B6B; --border: #D9D9D9; --border-light: #EEEEEE;
  --surface: #F7F7F5; --accent-warm: #CC1400; --accent-muted: rgba(204,20,0,0.06);
  --font: "Noto Sans JP", sans-serif; --font-serif: "Noto Serif JP", serif;
}
[data-theme="dark"] {
  --bg: #121212; --card: #1A1A1A; --text: #E0E0E0; --text-secondary: #AAAAAA;
  --text-muted: #8A8A8A; --border: #333333; --border-light: #2A2A2A;
  --surface: #1A1A1A; --accent-warm: #FF4444; --accent-muted: rgba(255,68,68,0.1);
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font); color: var(--text); background: var(--bg); line-height: 1.7; max-width: 960px; margin: 0 auto; padding: 24px 20px; }
.back { display: inline-block; margin-bottom: 20px; font-size: 0.82rem; color: var(--text-secondary); text-decoration: none; }
.back:hover { color: var(--text); }
h1 { font-family: var(--font-serif); font-size: 1.5rem; font-weight: 700; margin-bottom: 4px; }
.db-id { font-family: monospace; font-size: 0.72rem; font-weight: 700; color: var(--accent-warm); background: var(--accent-muted); padding: 2px 8px; margin-right: 8px; }
.subtitle { font-size: 0.84rem; color: var(--text-secondary); margin-bottom: 12px; line-height: 1.7; }
.desc { font-size: 0.84rem; color: var(--text); margin-bottom: 24px; line-height: 1.8; }
.overview { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 10px; margin-bottom: 28px; }
.overview-card { background: var(--surface); border: 1px solid var(--border-light); padding: 14px; text-align: center; }
.overview-value { font-family: var(--font-serif); font-size: 1.4rem; font-weight: 700; }
.overview-label { font-size: 0.7rem; color: var(--text-muted); margin-top: 2px; }
h3 { font-family: var(--font-serif); font-size: 1rem; font-weight: 700; margin: 28px 0 12px; padding-bottom: 6px; border-bottom: 1px solid var(--border); }
.cat-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 6px; }
.cat-item { display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; background: var(--surface); border: 1px solid var(--border-light); font-size: 0.82rem; }
.cat-name { color: var(--text); } .cat-count { font-weight: 700; color: var(--text-secondary); font-family: monospace; }
.table-list { display: grid; gap: 6px; }
.table-item { padding: 10px 14px; border: 1px solid var(--border-light); background: var(--surface); display: grid; grid-template-columns: 1fr auto; gap: 4px; }
.table-name { font-weight: 600; font-size: 0.84rem; } .table-name-en { font-size: 0.72rem; color: var(--text-muted); font-family: monospace; }
.table-rows { font-size: 0.78rem; color: var(--text-secondary); text-align: right; font-family: monospace; }
.sample-table-wrap { overflow-x: auto; border: 1px solid var(--border); margin-top: 4px; }
.sample-table { width: 100%; border-collapse: collapse; font-size: 0.78rem; }
.sample-table th { background: var(--surface); padding: 8px 10px; text-align: left; font-weight: 600; border-bottom: 1px solid var(--border); white-space: nowrap; }
.sample-table td { padding: 8px 10px; border-bottom: 1px solid var(--border-light); max-width: 400px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.sample-table tr:hover td { background: var(--surface); }
.theme-toggle { position: fixed; top: 16px; right: 16px; background: var(--surface); border: 1px solid var(--border); padding: 6px 10px; cursor: pointer; font-size: 1rem; }
.note { font-size: 0.78rem; color: var(--text-muted); margin-top: 6px; line-height: 1.6; }
.detail-card { border: 1px solid var(--border); margin-bottom: 12px; padding: 16px 20px; background: var(--card); }
.detail-card-label { font-size: 0.7rem; font-weight: 600; color: var(--accent-warm); letter-spacing: 0.05em; margin-bottom: 6px; }
.detail-card-title { font-size: 0.92rem; font-weight: 700; margin-bottom: 6px; line-height: 1.4; }
.detail-card-body { font-size: 0.82rem; color: var(--text-secondary); line-height: 1.7; }
.detail-card-meta { font-size: 0.72rem; color: var(--text-muted); margin-top: 8px; }
.detail-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 10px; }
"""


def build_html(db_id, title, subtitle, desc, overview_cards, sections):
    overview_html = ""
    for val, label in overview_cards:
        overview_html += f'<div class="overview-card"><div class="overview-value">{h(str(val))}</div><div class="overview-label">{h(label)}</div></div>'

    sections_html = ""
    for sec in sections:
        sections_html += sec

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{h(title)} | Insight News</title>
<link rel="icon" href="https://esse-sense.com/favicon.ico">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Noto+Serif+JP:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<button class="theme-toggle" onclick="document.documentElement.setAttribute('data-theme',document.documentElement.getAttribute('data-theme')==='dark'?'':'dark')">&#9789;</button>
<a class="back" href="app.html#section-databases">&larr; データベース一覧に戻る</a>
<h1><span class="db-id">{h(db_id)}</span>{h(title)}</h1>
<p class="subtitle">{subtitle}</p>
<p class="desc">{desc}</p>
<div class="overview">{overview_html}</div>
{sections_html}
</body>
</html>"""


def make_detail_cards(title, cards):
    """cards: list of {label, title, body, meta}"""
    if not cards:
        return ""
    html = f'<h3>{h(title)}</h3><div class="detail-grid">'
    for c in cards:
        html += '<div class="detail-card">'
        if c.get("label"):
            html += f'<div class="detail-card-label">{h(c["label"])}</div>'
        if c.get("title"):
            html += f'<div class="detail-card-title">{h(c["title"])}</div>'
        if c.get("body"):
            html += f'<div class="detail-card-body">{h(c["body"])}</div>'
        if c.get("meta"):
            html += f'<div class="detail-card-meta">{h(c["meta"])}</div>'
        html += '</div>'
    html += '</div>'
    return html


def make_cat_section(title, cats, translate=None):
    html = f'<h3>{h(title)}</h3><div class="cat-grid">'
    for name, cnt in cats:
        display = translate.get(name, name) if translate else name
        html += f'<div class="cat-item"><span class="cat-name">{h(display)}</span><span class="cat-count">{cnt:,}</span></div>'
    html += '</div>'
    return html


def make_table_section(table_stats):
    html = '<h3>テーブル構成</h3><div class="table-list">'
    for t in sorted(table_stats, key=lambda x: -x["rows"]):
        if t["rows"] == 0:
            continue
        html += f'<div class="table-item"><div><div class="table-name">{h(t["name_ja"])}</div><div class="table-name-en">{h(t["name"])}</div></div><div class="table-rows">{t["rows"]:,} 行</div></div>'
    html += '</div>'
    return html


def make_sample_section(title, cols, rows):
    if not rows:
        return ""
    html = f'<h3>{h(title)}</h3><div class="sample-table-wrap"><table class="sample-table"><thead><tr>'
    for c in cols:
        html += f'<th>{h(c)}</th>'
    html += '</tr></thead><tbody>'
    for row in rows:
        html += '<tr>'
        for val in row:
            html += f'<td>{h(val)}</td>'
        html += '</tr>'
    html += '</tbody></table></div>'
    return html


def gen_pe():
    path = os.path.expanduser("~/projects/research/pestle-signal-db/data/pestle.db")
    conn = sqlite3.connect(path)
    ts = get_table_stats(conn)
    cats = safe_query(conn, "SELECT pestle_category, COUNT(*) FROM articles GROUP BY pestle_category ORDER BY COUNT(*) DESC")
    sources = safe_query(conn, "SELECT source, COUNT(*) FROM articles GROUP BY source ORDER BY COUNT(*) DESC LIMIT 10")
    date_range = safe_query(conn, "SELECT MIN(published_date), MAX(published_date) FROM articles WHERE published_date > '1900'")
    media = safe_query(conn, "SELECT name_ja, region, categories, language FROM media_sources WHERE name_ja IS NOT NULL LIMIT 15")
    # Get detailed samples with summary
    detail_rows = safe_query(conn, "SELECT title, summary, pestle_category, source, published_date FROM articles WHERE summary IS NOT NULL AND length(summary)>80 ORDER BY published_date DESC LIMIT 6")
    conn.close()
    art_count = next((t["rows"] for t in ts if t["name"] == "articles"), 0)
    src_count = next((t["rows"] for t in ts if t["name"] == "media_sources"), 0)
    dr = date_range[0] if date_range else ("?", "?")

    detail_cards = []
    for r in detail_rows:
        detail_cards.append({
            "label": f"{PESTLE_JA.get(r[2], r[2])} | {r[3]} | {r[4]}",
            "title": r[0],
            "body": r[1][:250] + ("..." if len(r[1] or "") > 250 else ""),
        })

    media_cards = []
    for m in media[:8]:
        region = "日本" if m[1] == "japan" else ("グローバル" if m[1] == "global" else m[1])
        media_cards.append({
            "label": f"{region} / {m[3]}",
            "title": m[0],
            "body": f"カテゴリ: {PESTLE_JA.get(m[2], m[2])}",
        })

    html = build_html("PE", "PESTLEニュースDB",
        "政治・経済・社会・技術・法律・環境の6分野に自動分類されたニュース記事データベース",
        f"124のRSSフィード（国内57、海外67）から毎日自動収集し、PESTLE分類を行うニュースデータベースです。{art_count:,}件のニュース記事を蓄積しており、{dr[0]}から{dr[1]}までをカバーしています。各記事には以下のデータが付与されます: タイトル（日英）、要約、PESTLEカテゴリ、関連度スコア（0-1）、ソース名、言語、地域タグ、収集日。",
        [(f"{art_count:,}", "ニュース記事"), (f"{src_count}", "メディアソース"), ("6", "PESTLEカテゴリ"), (f"{dr[0]}〜", "データ期間")],
        [
            make_cat_section("PESTLEカテゴリ別記事数", cats, PESTLE_JA),
            make_detail_cards("格納データの具体例（最新記事）", detail_cards),
            make_detail_cards("登録メディアソースの例", media_cards),
            make_cat_section("主要メディアソース別記事数（上位10件）", sources),
            make_table_section(ts),
        ])
    (DASHBOARDS_DIR / "pe.html").write_text(html, encoding="utf-8")
    print("  OK PE")


def gen_ci():
    path = os.path.expanduser("~/projects/research/cultural-intelligence-db/data/cultural_intelligence.db")
    conn = sqlite3.connect(path)
    ts = get_table_stats(conn)
    cats = safe_query(conn, "SELECT c.name_ja, COUNT(*) FROM article_categories ac JOIN categories c ON ac.category_id=c.id GROUP BY c.name_ja ORDER BY COUNT(*) DESC")
    langs = safe_query(conn, "SELECT CASE lang WHEN 'ja' THEN '日本語' WHEN 'en' THEN '英語' ELSE lang END, COUNT(*) FROM articles GROUP BY lang ORDER BY COUNT(*) DESC")
    samples = safe_query(conn, "SELECT a.title, c.name_ja FROM articles a JOIN article_categories ac ON a.id=ac.article_id JOIN categories c ON ac.category_id=c.id WHERE a.lang='ja' ORDER BY a.published_at DESC LIMIT 12")
    conn.close()
    art_count = next((t["rows"] for t in ts if t["name"] == "articles"), 0)

    detail_cards = []
    for title, cat in samples[:8]:
        detail_cards.append({"label": cat, "title": title})

    html = build_html("CI", "文化インテリジェンスDB",
        "ミラツク独自の21カテゴリ体系で分類された文化ニュースデータベース",
        f"「国家・民主主義」「人権」「衣食住」「感情」「人知を超えたもの」など、ミラツクの文化構造フレームワークに基づく21のカテゴリで文化関連ニュースを日次収集しています。{art_count:,}件の記事を蓄積。各記事にはタイトル・言語・公開日・複数カテゴリが付与され、1記事が複数カテゴリに分類されます。PESTLE DBでは捉えきれない「衣食住」「感情」「人知を超えたもの」等の文化的変化を検出します。",
        [(f"{art_count:,}", "記事数"), ("21", "文化カテゴリ"), (f"{len(langs)}", "言語")],
        [
            make_cat_section("文化カテゴリ別記事数（21カテゴリ）", cats),
            make_detail_cards("格納データの具体例（日本語記事）", detail_cards),
            make_cat_section("言語別記事数", langs),
            make_table_section(ts),
        ])
    (DASHBOARDS_DIR / "ci.html").write_text(html, encoding="utf-8")
    print("  OK CI")


def gen_gr():
    path = os.path.expanduser("~/projects/research/geopolitical-risk-db/data/geopolitical_risk.db")
    conn = sqlite3.connect(path)
    ts = get_table_stats(conn)
    data_types = safe_query(conn, "SELECT 'GPR地政学リスク指数', COUNT(*) FROM gpr_index UNION ALL SELECT 'EPU経済政策不確実性指数', COUNT(*) FROM epu_index UNION ALL SELECT '紛争イベント', COUNT(*) FROM conflict_events UNION ALL SELECT '紛争サマリー', COUNT(*) FROM conflict_summary UNION ALL SELECT '対象国', COUNT(*) FROM countries")
    gpr_sample = safe_query(conn, "SELECT date, gpr_global, gpr_threats, gpr_acts FROM gpr_index WHERE gpr_global IS NOT NULL ORDER BY date DESC LIMIT 6")
    conflicts = safe_query(conn, "SELECT conflict_name, year, country_iso3, intensity_level, region FROM conflict_summary ORDER BY year DESC LIMIT 6")
    conn.close()
    total = sum(t["rows"] for t in ts)
    countries = next((t["rows"] for t in ts if t["name"] == "countries"), 0)

    gpr_cards = []
    for r in gpr_sample:
        gpr_cards.append({
            "label": r[0],
            "title": f"GPR全体: {r[1]:.1f}",
            "body": f"脅威指数: {r[2]:.1f} / 行動指数: {r[3]:.1f}",
        })
    conflict_cards = [{"label": f"{c[4]} / {c[2]} / {c[1]}年", "title": c[0], "body": f"紛争強度レベル: {c[3]}"} for c in conflicts]

    html = build_html("GR", "地政学リスクDB",
        "GPR指数・EPU指数・紛争データを統合した地政学リスク分析データベース",
        f"Matteo Iacovielloの地政学リスク指数（GPR）、Baker-Bloom-Davisの経済政策不確実性指数（EPU）、UCDPの紛争データを統合しています。{countries}カ国をカバーし、1900年から現在までの月次GPR指数を収録。各GPRレコードにはGPR全体指数・脅威指数・行動指数の3指標が、紛争データには日付・位置座標・暴力種別・死傷者数が含まれます。",
        [(f"{total:,}", "総レコード"), (f"{countries}", "対象国"), ("1900年〜", "GPRデータ期間"), ("3", "統合データソース")],
        [
            make_cat_section("データ種別", data_types),
            make_detail_cards("格納データの具体例（GPR指数）", gpr_cards),
            make_detail_cards("格納データの具体例（紛争サマリー）", conflict_cards),
            make_table_section(ts),
        ])
    (DASHBOARDS_DIR / "gr.html").write_text(html, encoding="utf-8")
    print("  OK GR")


def gen_cla():
    path = os.path.expanduser("~/projects/research/pestle-signal-db/data/cla.db")
    conn = sqlite3.connect(path)
    ts = get_table_stats(conn)
    period_types = safe_query(conn, "SELECT CASE period_type WHEN 'daily' THEN '日次' WHEN 'quarterly' THEN '四半期' WHEN 'yearly' THEN '年次' ELSE period_type END, COUNT(*) FROM analyses GROUP BY period_type")
    # Get full 4-layer CLA examples
    full_cla = safe_query(conn, "SELECT period, pestle_category, litany, systemic_causes, worldview, myth_metaphor FROM analyses WHERE length(litany)>50 AND myth_metaphor IS NOT NULL ORDER BY period DESC LIMIT 4")
    conn.close()
    total = sum(t["rows"] for t in ts)

    detail_cards = []
    for r in full_cla:
        body = f"【リタニー（表層事象）】{(r[2] or '')[:200]}\n\n【社会的原因】{(r[3] or '')[:200]}\n\n【世界観】{(r[4] or '')[:200]}\n\n【神話・メタファー】{(r[5] or '')[:200]}"
        detail_cards.append({
            "label": f"{r[0]} / {PESTLE_JA.get(r[1], r[1])}",
            "title": f"CLA分析: {r[0]} ({PESTLE_JA.get(r[1], r[1])})",
            "body": body,
        })

    html = build_html("CLA", "因果階層分析DB",
        "リタニー・社会的原因・世界観・神話の4層でニュースを深層分析するCLAデータベース",
        "因果階層分析（Causal Layered Analysis）は未来学者ソハイル・イナヤトゥラが開発した手法です。各分析レコードには以下の4層が含まれます: (1) リタニー: メディアで報じられる表層事象、(2) 社会的原因: 事象を生む制度・構造、(3) 世界観: 社会が「当たり前」と見なす前提、(4) 神話・メタファー: 深層にある物語パターン。36年分の年次・22四半期・日次のCLA分析をPESTLE6カテゴリごとに蓄積しています。",
        [(f"{total:,}", "総レコード"), ("36年分", "年次CLA"), ("22", "四半期CLA"), ("4層", "分析深度")],
        [
            make_cat_section("分析期間タイプ", period_types),
            make_detail_cards("格納データの具体例（4層CLA分析）", detail_cards),
            make_table_section(ts),
        ])
    (DASHBOARDS_DIR / "cla.html").write_text(html, encoding="utf-8")
    print("  OK CLA")


def gen_sg():
    path = os.path.expanduser("~/projects/research/pestle-signal-db/data/signal.db")
    conn = sqlite3.connect(path)
    ts = get_table_stats(conn)
    type_ja = {"emerging_trend": "新興トレンド", "weak_signal": "ウィークシグナル", "paradigm_shift": "パラダイムシフト", "counter_trend": "カウンタートレンド", "wild_card": "ワイルドカード", "systemic": "システミック", "paradox": "パラドックス"}
    types = safe_query(conn, "SELECT signal_type, COUNT(*) FROM signals GROUP BY signal_type ORDER BY COUNT(*) DESC")
    # Detailed signal samples
    sig_details = safe_query(conn, "SELECT signal_name, description, signal_type, potential_impact, time_horizon, counter_trend FROM signals ORDER BY id DESC LIMIT 6")
    # Alert samples
    alert_details = safe_query(conn, "SELECT alert_title, level, description, detected_date FROM alerts ORDER BY detected_date DESC LIMIT 3")
    alert_count = safe_query(conn, "SELECT COUNT(*) FROM alerts")[0][0]
    scenario_count = safe_query(conn, "SELECT COUNT(*) FROM scenarios")[0][0]
    conn.close()
    sig_count = next((t["rows"] for t in ts if t["name"] == "signals"), 0)

    sig_cards = []
    for r in sig_details:
        body = (r[1] or "")[:250]
        meta_parts = []
        if r[3]:
            meta_parts.append(f"影響: {r[3][:80]}")
        if r[5]:
            meta_parts.append(f"カウンタートレンド: {r[5][:80]}")
        sig_cards.append({
            "label": f"{type_ja.get(r[2], r[2])} | {r[4] or ''}",
            "title": r[0],
            "body": body,
            "meta": " / ".join(meta_parts) if meta_parts else None,
        })

    alert_cards = []
    for r in alert_details:
        alert_cards.append({
            "label": f"レベル: {r[1]} | {r[3]}",
            "title": r[0],
            "body": (r[2] or "")[:200],
        })

    html = build_html("SG", "シグナルDB",
        "パイプラインの中核出力 ― PESTLEニュースから自動検出された変化の兆し",
        f"PESTLEニュースと学術論文から、AIが自動的に「変化の兆し」を検出・分類するデータベースです。{sig_count:,}件のシグナルを蓄積。各シグナルには以下のデータが含まれます: シグナル名、説明文、タイプ（5種）、影響度評価、タイムホライズン（1-3年/3-5年/5-10年）、カウンタートレンド。さらにシグナル間の相互影響スコア（1,806件）とネットワーク構造も分析済みです。",
        [(f"{sig_count:,}", "シグナル"), (f"{alert_count}", "アラート"), (f"{scenario_count}", "シナリオ"), ("5種", "シグナルタイプ")],
        [
            make_cat_section("シグナルタイプ別件数", [(type_ja.get(t, t), c) for t, c in types]),
            make_detail_cards("格納データの具体例（シグナル）", sig_cards),
            make_detail_cards("最新アラート", alert_cards),
            make_table_section(ts),
        ])
    (DASHBOARDS_DIR / "sg.html").write_text(html, encoding="utf-8")
    print("  OK SG")


def gen_ir():
    path = os.path.expanduser("~/projects/research/investment-signal-radar/data/funding_database.db")
    conn = sqlite3.connect(path)
    ts = get_table_stats(conn)
    cat_ja = {"funding": "資金調達", "other": "その他", "event": "イベント", "accelerator": "アクセラレータ", "exit": "EXIT", "partnership": "提携", "product_launch": "製品発表", "hiring": "採用", "award": "受賞", "expansion": "事業拡大"}
    cats = safe_query(conn, "SELECT category, COUNT(*) FROM funding_releases WHERE category IS NOT NULL GROUP BY category ORDER BY COUNT(*) DESC LIMIT 10")
    # Detailed funding releases
    releases = safe_query(conn, "SELECT title, company_name, category, amount_raw, round_type, published_at FROM funding_releases WHERE amount_raw IS NOT NULL ORDER BY published_at DESC LIMIT 6")
    conn.close()
    comp_count = next((t["rows"] for t in ts if t["name"] == "companies"), 0)
    rel_count = next((t["rows"] for t in ts if t["name"] == "funding_releases"), 0)

    round_ja = {"seed": "シード", "series_a": "シリーズA", "series_b": "シリーズB", "series_c": "シリーズC", "pre_series_b": "PreシリーズB", "debt": "デット"}
    detail_cards = []
    for r in releases:
        rt = round_ja.get(r[4], r[4] or "")
        detail_cards.append({
            "label": f"{cat_ja.get(r[2], r[2])} | {rt} | {r[5]}",
            "title": r[0],
            "body": f"企業: {r[1] or '不明'} / 調達額: {r[3]}",
        })

    html = build_html("IR", "VC投資DB",
        "スタートアップの資金調達動向を追跡するVC投資データベース",
        f"スタートアップの資金調達プレスリリースを自動収集・分類するデータベースです。{comp_count:,}社の企業プロファイルと{rel_count:,}件の資金調達リリースを蓄積。各リリースにはタイトル・企業名・カテゴリ・調達額（原文）・調達額（円換算）・ラウンド種別・公開日が構造化されています。",
        [(f"{comp_count:,}", "企業"), (f"{rel_count:,}", "リリース"), ("月次", "更新頻度")],
        [
            make_cat_section("リリースカテゴリ別件数", [(cat_ja.get(c, c), n) for c, n in cats]),
            make_detail_cards("格納データの具体例（資金調達リリース）", detail_cards),
            make_table_section(ts),
        ])
    (DASHBOARDS_DIR / "ir.html").write_text(html, encoding="utf-8")
    print("  OK IR")


def gen_pd():
    path = os.path.expanduser("~/projects/apps/policy-db/data/policy.db")
    conn = sqlite3.connect(path)
    ts = get_table_stats(conn)
    council_count = safe_query(conn, "SELECT COUNT(*) FROM councils")[0][0]
    person_count = safe_query(conn, "SELECT COUNT(*) FROM persons")[0][0]
    org_count = safe_query(conn, "SELECT COUNT(*) FROM organizations")[0][0]
    appt_count = safe_query(conn, "SELECT COUNT(*) FROM appointments")[0][0]
    # Top councils
    top_councils = safe_query(conn, "SELECT c.name, COUNT(cm.id) as cnt FROM councils c LEFT JOIN council_members cm ON c.id=cm.council_id GROUP BY c.id ORDER BY cnt DESC LIMIT 8")
    # Persons
    persons = safe_query(conn, "SELECT canonical_name, org_name FROM persons WHERE org_name IS NOT NULL ORDER BY id DESC LIMIT 6")
    # Projects
    projects = safe_query(conn, "SELECT name, ministry_name, finalized_amount FROM projects WHERE finalized_amount IS NOT NULL ORDER BY CAST(finalized_amount AS REAL) DESC LIMIT 5")
    conn.close()

    council_cards = [{"label": f"委員数: {c[1]}", "title": c[0]} for c in top_councils]
    person_cards = [{"label": p[1], "title": p[0]} for p in persons]
    project_cards = []
    for p in projects:
        amt = p[2]
        if amt and amt > 1e12:
            amt_str = f"{amt/1e12:.1f}兆円"
        elif amt and amt > 1e8:
            amt_str = f"{amt/1e8:.0f}億円"
        else:
            amt_str = str(amt)
        project_cards.append({"label": p[1], "title": p[0], "body": f"予算額: {amt_str}"})

    html = build_html("PD", "政策DB",
        "23省庁の審議会・委員会・有識者・予算事業を網羅した政策データベース",
        f"日本政府23省庁の政策決定プロセスを構造化したデータベースです。{council_count:,}の審議会・委員会、{person_count:,}名の有識者、{org_count:,}の関連組織、{appt_count:,}件の委員任命データを収録。各審議会には委員構成・所管省庁・開催回次が、各有識者には所属組織・肩書・参加審議会が紐付けられています。予算事業データには事業名・省庁・要求額・確定額・執行率が含まれます。",
        [(f"{council_count:,}", "審議会・委員会"), (f"{person_count:,}", "有識者"), (f"{org_count:,}", "組織"), (f"{appt_count:,}", "任命")],
        [
            make_detail_cards("格納データの具体例（主要審議会）", council_cards),
            make_detail_cards("格納データの具体例（有識者）", person_cards),
            make_detail_cards("格納データの具体例（大型予算事業）", project_cards),
            make_table_section(ts),
        ])
    (DASHBOARDS_DIR / "pd.html").write_text(html, encoding="utf-8")
    print("  OK PD")


def gen_si():
    path = os.path.expanduser("~/projects/apps/sangaku-matcher/data/matcher.db")
    conn = sqlite3.connect(path)
    ts = get_table_stats(conn)
    themes = safe_query(conn, "SELECT major_name, COUNT(*) FROM ambition_taxonomy_themes GROUP BY major_name ORDER BY COUNT(*) DESC")
    theme_samples = safe_query(conn, "SELECT major_name, name FROM ambition_taxonomy_themes ORDER BY major_name LIMIT 10")
    conn.close()
    total = sum(t["rows"] for t in ts)
    prox_count = next((t["rows"] for t in ts if t["name"] == "ambition_taxonomy_proximity"), 0)

    theme_cards = [{"label": t[0], "title": t[1]} for t in theme_samples]
    comp_count = next((t["rows"] for t in ts if t["name"] == "companies"), 0)

    html = build_html("SI", "企業ニーズDB",
        "上場企業のIR文書から抽出した事業志向・技術ニーズのデータベース",
        f"EDINET有価証券報告書から企業の事業志向を自動抽出し、40のテーマに分類。{comp_count:,}社の企業データと{prox_count:,}件の企業-テーマ近接度データを保持。各企業がどのテーマにどの程度関心を持っているかを0-1の近接度スコアで定量化し、産学連携マッチングの基盤として活用します。",
        [(f"{comp_count:,}", "企業"), ("40", "志向テーマ"), (f"{prox_count:,}", "企業-テーマ近接度")],
        [
            make_cat_section("大分類別テーマ数", themes),
            make_detail_cards("格納データの具体例（志向テーマ）", theme_cards),
            make_table_section(ts),
        ])
    (DASHBOARDS_DIR / "si.html").write_text(html, encoding="utf-8")
    print("  OK SI")


def gen_ic():
    path = os.path.expanduser("~/projects/apps/ir-collector/data/ir.db")
    conn = sqlite3.connect(path)
    ts = get_table_stats(conn)
    samples = safe_query(conn, "SELECT filer_name, doc_description, submit_datetime FROM documents ORDER BY submit_datetime DESC LIMIT 10")
    edinet_count = safe_query(conn, "SELECT COUNT(*) FROM edinet_companies")
    conn.close()
    doc_count = next((t["rows"] for t in ts if t["name"] == "documents"), 0)
    ec = edinet_count[0][0] if edinet_count else 0

    html = build_html("IC", "企業IRDB",
        "EDINET有価証券報告書を自動収集する上場企業IRデータベース",
        f"金融庁EDINETから有価証券報告書等のIR文書を自動収集するデータベースです。{ec:,}社の上場企業を対象に、提出書類のメタデータ（企業名・書類種別・提出日時・XBRL有無）を管理します。企業の経営動向変化を検出するセンサーとして機能します。",
        [(f"{ec:,}", "対象企業"), (f"{doc_count:,}", "IR書類"), ("四半期", "更新頻度")],
        [
            make_table_section(ts),
            make_sample_section("最新IR書類サンプル", ["企業名", "書類種別", "提出日時"], samples),
        ])
    (DASHBOARDS_DIR / "ic.html").write_text(html, encoding="utf-8")
    print("  OK IC")


def gen_sgpr():
    path = os.path.expanduser("~/projects/research/investment-signal-radar/data/sangaku_press_releases.db")
    conn = sqlite3.connect(path)
    ts = get_table_stats(conn)
    cat_ja = {"funding": "資金調達", "other": "その他", "partnership": "提携", "hiring": "採用", "product_launch": "製品発表"}
    cats = safe_query(conn, "SELECT category, COUNT(*) FROM press_releases WHERE category IS NOT NULL GROUP BY category ORDER BY COUNT(*) DESC")
    samples = safe_query(conn, "SELECT title, company_name, category, published_at FROM press_releases ORDER BY published_at DESC LIMIT 10")
    conn.close()
    pr_count = next((t["rows"] for t in ts if t["name"] == "press_releases"), 0)

    detail_cards = [{"label": f"{cat_ja.get(r[2], r[2] or '')} | {r[3]}", "title": r[0], "body": f"企業: {r[1]}" if r[1] else None} for r in samples[:6]]

    html = build_html("SGPR", "産学プレスリリースDB",
        "産学連携に関するプレスリリースを自動分類・蓄積するデータベース",
        f"産学連携関連のプレスリリース{pr_count:,}件を収集・分類しています。各レコードにはタイトル・企業名・カテゴリ・資金調達関連フラグ・公開日が含まれます。",
        [(f"{pr_count:,}", "プレスリリース"), (f"{len(cats)}", "カテゴリ")],
        [
            make_cat_section("カテゴリ別件数", [(cat_ja.get(c, c), n) for c, n in cats]),
            make_detail_cards("格納データの具体例", detail_cards),
            make_table_section(ts),
        ])
    (DASHBOARDS_DIR / "sgpr.html").write_text(html, encoding="utf-8")
    print("  OK SGPR")


def gen_an():
    path = os.path.expanduser("~/projects/research/anthropology-concepts/data/anthropology.db")
    conn = sqlite3.connect(path)
    ts = get_table_stats(conn)
    subfields = safe_query(conn, "SELECT subfield, COUNT(*) FROM concepts WHERE subfield IS NOT NULL GROUP BY subfield ORDER BY COUNT(*) DESC LIMIT 15")
    concepts = safe_query(conn, "SELECT name_ja, name_en, definition, subfield, school_of_thought FROM concepts WHERE definition IS NOT NULL AND name_ja IS NOT NULL LIMIT 6")
    researchers = safe_query(conn, "SELECT name_ja, name_full, nationality, primary_institution, research_themes FROM researchers WHERE name_ja IS NOT NULL LIMIT 6")
    researcher_count = safe_query(conn, "SELECT COUNT(*) FROM researchers")[0][0]
    pub_count = safe_query(conn, "SELECT COUNT(*) FROM publications")[0][0]
    concept_count = safe_query(conn, "SELECT COUNT(*) FROM concepts")[0][0]
    conn.close()

    concept_cards = [{"label": f"{c[3] or ''} / {c[4] or ''}", "title": f"{c[0]}（{c[1]}）", "body": (c[2] or "")[:300]} for c in concepts]
    researcher_cards = [{"label": f"{r[2] or ''} / {r[3] or ''}", "title": f"{r[0]}（{r[1]}）", "body": f"研究テーマ: {r[4] or ''}"} for r in researchers]

    html = build_html("AN", "人類学概念DB",
        "人類学の主要概念・研究者・文献を系譜的に構造化したデータベース",
        f"文化人類学・医療人類学・経済人類学など多領域にわたる{concept_count}の概念を収録。各概念には日本語名・英語名・定義・分野・学派が、{researcher_count}名の研究者には氏名・国籍・所属・研究テーマが、{pub_count}件の文献にはタイトル・出版年・DOIが含まれます。概念間の影響関係285件とOCM分類との対応44件も構造化済みです。",
        [(f"{concept_count}", "概念"), (f"{researcher_count}", "研究者"), (f"{pub_count}", "文献"), ("285", "概念間関係")],
        [
            make_cat_section("分野別概念数", subfields),
            make_detail_cards("格納データの具体例（概念）", concept_cards),
            make_detail_cards("格納データの具体例（研究者）", researcher_cards),
            make_table_section(ts),
        ])
    (DASHBOARDS_DIR / "an.html").write_text(html, encoding="utf-8")
    print("  OK AN")


def gen_json_dbs():
    # FK
    html = build_html("FK", "フォーサイト知識基盤",
        "世界363機関のフォーサイトレポートを網羅的に収集した知識基盤",
        "OECD、世界経済フォーラム、各国政府のフォーサイト機関など、世界363の組織が発行するフォーサイトレポート51,159件を収集・構造化しています。650以上のトレンドを抽出し、地域・テーマ・時間軸で横断検索が可能です。パイプライン全体の「未来の視点」を提供する基軸データベースです。",
        [("363", "フォーサイト機関"), ("51,159", "レポート"), ("650+", "トレンド"), ("週次", "更新")],
        ['<h3>収録データの概要</h3><div class="note">各フォーサイト機関のレポートに対して、発行機関・発行年・テーマ・地域・要約・トレンドキーワードが構造化されています。Three Horizons（短期・中期・長期）の時間軸分類も付与されています。</div>'])
    (DASHBOARDS_DIR / "fk.html").write_text(html, encoding="utf-8")
    print("  OK FK")

    # MT
    html = build_html("MT", "18メガトレンド",
        "未来予測書籍から抽出した18の大テーマによる多層タクソノミー",
        "ミラツクが約30冊の未来予測関連書籍を読書会形式で読み解き、抽出した18の大テーマです。5つのメガドメイン（地球環境・技術革新・社会構造・経済システム・ガバナンス）に分類され、Three Horizons（短期・中期・長期）と5つの認識論的フレームによる多層構造を持ちます。ニュースを「未来の文脈」に位置づけるためのフレームワークです。",
        [("18", "メガトレンド"), ("5", "メガドメイン"), ("3", "時間軸（Horizons）"), ("5", "認識論的フレーム")],
        ['<h3>構造</h3><div class="note">各メガトレンドには、トレンドの定義・関連する書籍引用・具体的な変化の指標が紐付けられています。ニュース記事のカテゴリ分類に使用され、日々のニュースを長期的な未来予測の文脈に接続します。</div>'])
    (DASHBOARDS_DIR / "mt.html").write_text(html, encoding="utf-8")
    print("  OK MT")

    # AL
    html = build_html("AL", "学術ランドスケープ",
        "114カ国の学術活動を俯瞰する研究動向マップ",
        "国別の研究活動量・重点分野・国際共著率などを構造化した学術ランドスケープデータベースです。114カ国をカバーし、各国の学術的強みと研究動向の地理的分布を可視化します。シグナル検出の「学術的文脈」を提供するデータソースです。",
        [("114", "対象国")],
        [])
    (DASHBOARDS_DIR / "al.html").write_text(html, encoding="utf-8")
    print("  OK AL")

    # GF
    html = build_html("GF", "歴史構造DB / 経営学・起業概念DB",
        "歴史上の経営者・起業家と経営概念を構造化した歴史パターン分析基盤",
        "9,178人の歴史上の重要人物（経営者・起業家・政治指導者・思想家）と568の経営概念を構造化しています。1,050の歴史的イベント、741の人物間リンク、100の高解像度構造分析、6件の詳細ケースレポートを含みます。「過去のパターンから未来を読む」ための構造理解ツールとして機能します。",
        [("9,178", "人物"), ("568", "概念"), ("1,050", "イベント"), ("6", "ケースレポート")],
        ['<h3>収録データの概要</h3><div class="note">各人物には、活動時期・地域・主要業績・関連概念・影響関係が構造化されています。渋沢栄一、孫正義、ジェフ・ベゾスなどの詳細ケーススタディも含まれ、経営判断のパターン分析が可能です。</div>'])
    (DASHBOARDS_DIR / "gf.html").write_text(html, encoding="utf-8")
    print("  OK GF")

    # MY
    my_path = os.path.expanduser("~/projects/research/miratuku-news-v2/data/cla_myth_mapping.json")
    try:
        data = json.load(open(my_path))
        thompson_total = data.get("thompson_total", 45496)
        ts = data.get("thompson_summary", {})
        cats = [(k, v.get("count", 0) if isinstance(v, dict) else v) for k, v in list(ts.items())[:15]]
    except:
        thompson_total = 45496
        cats = []

    html = build_html("MY", "神話データベース",
        "世界の神話・民話モチーフとCLA第4層（神話・メタファー）を接続するデータベース",
        f"Stith Thompsonの民話モチーフ索引（Motif-Index of Folk-Literature）から{thompson_total:,}件のモチーフを23カテゴリに構造化。さらにUNESCO無形文化遺産データとCLA分析の第4層（神話・メタファー）を接続し、現代社会の深層にある「物語の力」を可視化します。ニュースの表層の奥にある文化的無意識を読み解くための基盤です。",
        [(f"{thompson_total:,}", "Thompsonモチーフ"), ("23", "カテゴリ"), ("CLA第4層", "接続先")],
        [
            make_cat_section("モチーフカテゴリ", cats) if cats else "",
            '<h3>活用方法</h3><div class="note">CLA分析の「神話・メタファー」層において、現代のニュースやトレンドがどのような古代の物語パターンと共鳴しているかを分析します。例えば、AI技術の台頭は「プロメテウスの火」のモチーフと、環境運動は「楽園喪失」のモチーフと結びつきます。</div>',
        ])
    (DASHBOARDS_DIR / "my.html").write_text(html, encoding="utf-8")
    print("  OK MY")

    # ME
    html = build_html("ME", "マクロ経済DB",
        "World Bank・IMFの主要経済指標を統合した国際マクロ経済データベース",
        "World BankとIMFのオープンデータから61カ国の42種類のマクロ経済指標（GDP、インフレ率、失業率、貿易収支など）の時系列データ52,000件以上を収録しています。経済的な変化検出の定量的基盤として、PESTLEのEconomicカテゴリを補完します。",
        [("61", "対象国"), ("42", "経済指標"), ("52K+", "データポイント"), ("2", "データソース")],
        [])
    (DASHBOARDS_DIR / "me.html").write_text(html, encoding="utf-8")
    print("  OK ME")

    # RG
    html = build_html("RG", "規制動態DB",
        "e-Gov法令APIから収集した日本の法規制変化を追跡するデータベース",
        "e-Gov法令APIを通じて日本の法令1,332件の構造化データを収録しています。法令名・法令番号・所管省庁・制定日・改正履歴を管理し、PESTLEのLegalカテゴリにおける規制変化の検出に活用します。「どの分野の規制が、いつ、どのように変わったか」を追跡可能にします。",
        [("1,332", "法令"), ("e-Gov", "データソース")],
        [])
    (DASHBOARDS_DIR / "rg.html").write_text(html, encoding="utf-8")
    print("  OK RG")


if __name__ == "__main__":
    print("Generating dashboards...")
    gen_pe()
    gen_ci()
    gen_gr()
    gen_cla()
    gen_sg()
    gen_ir()
    gen_pd()
    gen_si()
    gen_ic()
    gen_sgpr()
    gen_an()
    gen_json_dbs()
    print("\nDone!")
