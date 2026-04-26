#!/usr/bin/env python3
"""
Update dashboard HTML pages with real sample data from each database.
Adds a "サンプルデータ" section showing 1 actual record as key-value pairs.
Also updates statistics (article counts, etc.) to match current DB state.
"""

import sqlite3
import json
import os
import re
from html import escape

DASHBOARDS_DIR = os.path.expanduser("~/projects/apps/miratuku-news-v2/dashboards")

# Database configs: id -> (db_path, main_table, display_fields, stats_updates)
DB_CONFIGS = {
    "pe": {
        "db": "~/projects/research/pestle-signal-db/data/pestle.db",
        "table": "articles",
        "query": "SELECT title, summary, published_date, pestle_category, source_name FROM articles WHERE title IS NOT NULL AND summary IS NOT NULL ORDER BY published_date DESC LIMIT 1",
        "field_labels": {
            "title": "タイトル",
            "summary": "要約",
            "published_date": "公開日",
            "pestle_category": "PESTLEカテゴリ",
            "source_name": "ソース",
        },
    },
    "ci": {
        "db": "~/projects/research/cultural-intelligence-db/data/cultural_intelligence.db",
        "table": "articles",
        "query": """SELECT a.title, a.published_at, a.lang, s.name as source_name,
                    GROUP_CONCAT(c.name, ', ') as categories
                    FROM articles a
                    LEFT JOIN article_categories ac ON a.id = ac.article_id
                    LEFT JOIN categories c ON ac.category_id = c.id
                    LEFT JOIN sources s ON a.source_id = s.id
                    WHERE a.title IS NOT NULL AND length(a.title) > 10
                    GROUP BY a.id
                    ORDER BY a.published_at DESC LIMIT 1""",
        "field_labels": {
            "title": "タイトル",
            "published_at": "公開日",
            "lang": "言語",
            "source_name": "ソース",
            "categories": "文化カテゴリ",
        },
    },
    "gr": {
        "db": "~/projects/research/geopolitical-risk-db/data/geopolitical_risk.db",
        "table": "gpr_monthly",
        "query": "SELECT country, year, month, gpr_index, gpr_threat, gpr_act FROM gpr_monthly WHERE gpr_index > 0 ORDER BY year DESC, month DESC LIMIT 1",
        "field_labels": {
            "country": "国",
            "year": "年",
            "month": "月",
            "gpr_index": "GPR指数",
            "gpr_threat": "GPR脅威",
            "gpr_act": "GPR実行",
        },
    },
    "an": {
        "db": "~/projects/research/anthropology-concepts/anthropology.db",
        "table": "concepts",
        "query": "SELECT name_ja, name_en, definition, field, era FROM concepts WHERE definition IS NOT NULL LIMIT 1",
        "field_labels": {
            "name_ja": "概念名（日）",
            "name_en": "概念名（英）",
            "definition": "定義",
            "field": "分野",
            "era": "時代",
        },
    },
    "my": {
        "db": "~/projects/research/pestle-signal-db/data/pestle.db",
        "table": "cla_analyses",
        "query": "SELECT period_label, pestle_category, worldview, myths_metaphors FROM cla_analyses WHERE myths_metaphors IS NOT NULL ORDER BY RANDOM() LIMIT 1",
        "field_labels": {
            "period_label": "期間",
            "pestle_category": "カテゴリ",
            "worldview": "世界観",
            "myths_metaphors": "神話・メタファー",
        },
    },
    "ir": {
        "db": "~/projects/research/investment-signal-radar/data/funding.db",
        "table": "rounds",
        "query": "SELECT c.name as company, r.round_type, r.amount_usd, r.announced_date, r.sector FROM rounds r JOIN companies c ON r.company_id = c.id WHERE r.amount_usd > 0 ORDER BY r.announced_date DESC LIMIT 1",
        "field_labels": {
            "company": "企業名",
            "round_type": "ラウンドタイプ",
            "amount_usd": "調達額 (USD)",
            "announced_date": "発表日",
            "sector": "セクター",
        },
    },
    "me": {
        "db": "~/projects/research/macro-economy-db/data/macro_economy.db",
        "table": "indicators",
        "query": "SELECT country_name, indicator_name, year, value, source FROM indicators WHERE value IS NOT NULL ORDER BY year DESC LIMIT 1",
        "field_labels": {
            "country_name": "国名",
            "indicator_name": "指標名",
            "year": "年",
            "value": "値",
            "source": "出典",
        },
    },
    "rg": {
        "db": "~/projects/research/regulatory-db-japan/data/regulatory.db",
        "table": "laws",
        "query": "SELECT law_title, law_num, category, promulgation_date FROM laws WHERE law_title IS NOT NULL LIMIT 1",
        "field_labels": {
            "law_title": "法令名",
            "law_num": "法令番号",
            "category": "カテゴリ",
            "promulgation_date": "公布日",
        },
    },
    "pd": {
        "db": "~/projects/research/policy-db/data/policy.db",
        "table": "projects",
        "query": "SELECT project_name, ministry, budget_amount, fiscal_year, description FROM projects WHERE project_name IS NOT NULL ORDER BY fiscal_year DESC LIMIT 1",
        "field_labels": {
            "project_name": "事業名",
            "ministry": "省庁",
            "budget_amount": "予算額",
            "fiscal_year": "年度",
            "description": "説明",
        },
    },
}


def get_sample(config):
    """Get one sample record from database."""
    db_path = os.path.expanduser(config["db"])
    if not os.path.exists(db_path):
        return None, f"DB not found: {db_path}"

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(config["query"])
        row = c.fetchone()
        conn.close()

        if not row:
            return None, "No data found"

        result = {}
        for key in row.keys():
            val = row[key]
            if val is not None:
                label = config["field_labels"].get(key, key)
                # Truncate long values
                val_str = str(val)
                if len(val_str) > 300:
                    val_str = val_str[:300] + "..."
                result[label] = val_str
        return result, None
    except Exception as e:
        return None, str(e)


def build_sample_html(sample, db_id):
    """Build HTML for a sample data card."""
    if not sample:
        return ""

    rows = ""
    for label, value in sample.items():
        rows += f'<tr><td style="font-weight:600;color:var(--accent-warm);white-space:nowrap;vertical-align:top;padding-right:12px;width:120px">{escape(label)}</td><td style="word-break:break-all">{escape(value)}</td></tr>'

    return f'''<h3>サンプルデータ（1件）</h3>
<div class="detail-card">
<table style="width:100%;border-collapse:collapse;font-size:0.82rem;line-height:1.7">
{rows}
</table>
</div>'''


def inject_sample_into_html(html_path, sample_html):
    """Inject sample HTML before the closing </body> tag or before テーブル構成."""
    with open(html_path, "r") as f:
        html = f.read()

    # Remove existing sample section if present
    html = re.sub(
        r'<h3>サンプルデータ（1件）</h3>\s*<div class="detail-card">.*?</div>\s*',
        "",
        html,
        flags=re.DOTALL,
    )

    # Insert before テーブル構成 section, or before </body>
    if '<h3>テーブル構成</h3>' in html:
        html = html.replace('<h3>テーブル構成</h3>', sample_html + '\n<h3>テーブル構成</h3>')
    elif '</body>' in html:
        html = html.replace('</body>', sample_html + '\n</body>')

    with open(html_path, "w") as f:
        f.write(html)

    return True


def update_ci_stats(html_path):
    """Update CI dashboard with current statistics."""
    db_path = os.path.expanduser("~/projects/research/cultural-intelligence-db/data/cultural_intelligence.db")
    if not os.path.exists(db_path):
        return

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM articles")
    total = c.fetchone()[0]

    # Category counts
    c.execute("""SELECT c.name, COUNT(*) as cnt
                 FROM article_categories ac
                 JOIN categories c ON ac.category_id = c.id
                 GROUP BY c.name ORDER BY cnt DESC""")
    cats = [(r[0], r[1]) for r in c.fetchall()]

    # Language counts
    c.execute("SELECT lang, COUNT(*) FROM articles GROUP BY lang ORDER BY COUNT(*) DESC")
    langs = [(r[0], r[1]) for r in c.fetchall()]
    lang_labels = {"en": "英語", "ja": "日本語"}

    conn.close()

    with open(html_path, "r") as f:
        html = f.read()

    # Update total count in overview
    html = re.sub(
        r'<div class="overview-value">\d[\d,]*</div><div class="overview-label">記事数',
        f'<div class="overview-value">{total:,}</div><div class="overview-label">記事数',
        html,
    )

    # Update category grid
    cat_html = "".join(
        f'<div class="cat-item"><span class="cat-name">{escape(name)}</span><span class="cat-count">{count:,}</span></div>'
        for name, count in cats
    )
    html = re.sub(
        r'<h3>文化カテゴリ別記事数.*?</h3><div class="cat-grid">.*?</div>',
        f'<h3>文化カテゴリ別記事数（21カテゴリ）</h3><div class="cat-grid">{cat_html}</div>',
        html,
        flags=re.DOTALL,
    )

    # Update language grid
    lang_html = "".join(
        f'<div class="cat-item"><span class="cat-name">{escape(lang_labels.get(lang, lang))}</span><span class="cat-count">{count:,}</span></div>'
        for lang, count in langs
    )
    html = re.sub(
        r'<h3>言語別記事数</h3><div class="cat-grid">.*?</div>',
        f'<h3>言語別記事数</h3><div class="cat-grid">{lang_html}</div>',
        html,
        flags=re.DOTALL,
    )

    # Update desc text
    html = re.sub(
        r'\d[\d,]*件の記事を蓄積',
        f'{total:,}件の記事を蓄積',
        html,
    )

    # Update table rows
    c2 = sqlite3.connect(db_path)
    c2r = c2.cursor()
    c2r.execute("SELECT COUNT(*) FROM article_categories")
    ac_count = c2r.fetchone()[0]
    c2.close()

    html = re.sub(
        r'<div class="table-rows">[\d,]+ 行</div></div><div class="table-item"><div><div class="table-name">ニュース記事',
        f'<div class="table-rows">{ac_count:,} 行</div></div><div class="table-item"><div><div class="table-name">ニュース記事',
        html,
    )
    html = re.sub(
        r'ニュース記事</div><div class="table-name-en">articles</div></div><div class="table-rows">[\d,]+ 行',
        f'ニュース記事</div><div class="table-name-en">articles</div></div><div class="table-rows">{total:,} 行',
        html,
    )

    with open(html_path, "w") as f:
        f.write(html)

    print(f"  Updated CI stats: {total:,} articles, {len(cats)} categories")


def update_pe_stats(html_path):
    """Update PE dashboard with current statistics."""
    db_path = os.path.expanduser("~/projects/research/pestle-signal-db/data/pestle.db")
    if not os.path.exists(db_path):
        return

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM articles")
    total = c.fetchone()[0]

    c.execute("SELECT pestle_category, COUNT(*) FROM articles GROUP BY pestle_category ORDER BY COUNT(*) DESC")
    cats = [(r[0], r[1]) for r in c.fetchall() if r[0]]
    conn.close()

    with open(html_path, "r") as f:
        html = f.read()

    # Update overview count
    html = re.sub(
        r'<div class="overview-value">[\d,]+</div><div class="overview-label">記事',
        f'<div class="overview-value">{total:,}</div><div class="overview-label">記事',
        html,
    )

    with open(html_path, "w") as f:
        f.write(html)

    print(f"  Updated PE stats: {total:,} articles")


# Main
if __name__ == "__main__":
    for db_id, config in DB_CONFIGS.items():
        html_path = os.path.join(DASHBOARDS_DIR, f"{db_id}.html")
        if not os.path.exists(html_path):
            print(f"[{db_id}] SKIP - no dashboard HTML")
            continue

        sample, err = get_sample(config)
        if err:
            print(f"[{db_id}] ERROR: {err}")
            continue

        if sample:
            sample_html = build_sample_html(sample, db_id)
            # Remove old "格納データの具体例" section first
            with open(html_path, "r") as f:
                html = f.read()
            html = re.sub(
                r'<h3>格納データの具体例.*?</h3><div class="detail-grid">.*?</div>',
                '',
                html,
                flags=re.DOTALL,
            )
            with open(html_path, "w") as f:
                f.write(html)

            inject_sample_into_html(html_path, sample_html)
            print(f"[{db_id}] OK - sample injected ({len(sample)} fields)")
        else:
            print(f"[{db_id}] SKIP - no sample data")

    # Update specific page stats
    update_ci_stats(os.path.join(DASHBOARDS_DIR, "ci.html"))
    update_pe_stats(os.path.join(DASHBOARDS_DIR, "pe.html"))

    print("\nDone!")
