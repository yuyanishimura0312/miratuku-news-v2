#!/usr/bin/env python3
"""Generate stats JSON for the SGRD dashboard from sangaku_rd.db."""
import sqlite3
import json

DB_PATH = '/Users/nishimura+/projects/apps/miratuku-news-v2/data/sangaku-rd/sangaku_rd.db'
OUTPUT_PATH = '/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/sgrd-stats.json'

def main():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    c = conn.cursor()

    total_pr = c.execute("SELECT count(*) FROM press_releases").fetchone()[0]
    total_companies = c.execute("SELECT count(DISTINCT edinet_code) FROM press_releases WHERE edinet_code IS NOT NULL").fetchone()[0]
    total_analyzed = c.execute("SELECT count(*) FROM analysis WHERE research_theme_20 IS NOT NULL").fetchone()[0]
    total_gta = c.execute("SELECT count(*) FROM gta_codebook").fetchone()[0]
    total_themes = c.execute("SELECT count(DISTINCT research_theme_20) FROM analysis WHERE research_theme_20 IS NOT NULL").fetchone()[0]
    full_text_count = c.execute("SELECT count(*) FROM press_releases WHERE length(full_text) > 100").fetchone()[0]

    # Universities from mentions
    all_univs = set()
    for row in c.execute("SELECT universities_mentioned FROM press_releases WHERE universities_mentioned IS NOT NULL AND universities_mentioned != ''"):
        for u in row[0].split(','):
            u = u.strip()
            if u and len(u) > 1:
                all_univs.add(u)
    total_universities = len(all_univs)

    # By industry
    by_industry = []
    for row in c.execute("""
        SELECT c.industry, count(pr.id) as cnt
        FROM press_releases pr
        JOIN companies c ON pr.edinet_code = c.edinet_code
        WHERE c.industry IS NOT NULL
        GROUP BY c.industry
        ORDER BY cnt DESC LIMIT 25
    """):
        by_industry.append({'label': row[0], 'count': row[1]})

    # Top themes
    top_themes = []
    for row in c.execute("""
        SELECT research_theme_20, count(*) as cnt
        FROM analysis WHERE research_theme_20 IS NOT NULL AND research_theme_20 != ''
        GROUP BY research_theme_20
        ORDER BY cnt DESC LIMIT 30
    """):
        top_themes.append({'label': row[0], 'count': row[1]})

    # GTA distribution
    gta_dist = []
    for row in c.execute("SELECT code, example_count FROM gta_codebook ORDER BY example_count DESC LIMIT 30"):
        gta_dist.append({'label': row[0], 'count': row[1] or 0})

    # Top universities
    univ_counts = {}
    for row in c.execute("SELECT universities_mentioned FROM press_releases WHERE universities_mentioned IS NOT NULL AND universities_mentioned != ''"):
        for u in row[0].split(','):
            u = u.strip()
            if u and len(u) > 2:
                univ_counts[u] = univ_counts.get(u, 0) + 1
    top_univs = sorted(univ_counts.items(), key=lambda x: -x[1])[:20]
    top_universities = [{'label': u, 'count': c} for u, c in top_univs]

    # Recent press releases
    recent = []
    for row in c.execute("""
        SELECT pr.published_at, pr.company_name, pr.title, pr.url,
               a.research_theme_20, pr.universities_mentioned
        FROM press_releases pr
        LEFT JOIN analysis a ON pr.id = a.press_release_id
        WHERE pr.published_at IS NOT NULL
        ORDER BY pr.published_at DESC
        LIMIT 100
    """):
        company = (row[1] or '').replace('株式会社', '').replace('　', ' ').strip()
        recent.append({
            'date': row[0] or '',
            'company': company[:20],
            'title': (row[2] or '')[:80],
            'url': row[3] or '',
            'theme': row[4] or '',
            'university': (row[5] or '')[:40],
        })

    # Year distribution
    year_dist = []
    for row in c.execute("""
        SELECT substr(published_at, 1, 4) as year, count(*) as cnt
        FROM press_releases WHERE published_at IS NOT NULL
        GROUP BY year ORDER BY year
    """):
        if row[0] and int(row[0]) >= 2020:
            year_dist.append({'label': row[0], 'count': row[1]})

    stats = {
        'total_pr': total_pr,
        'total_companies': total_companies,
        'total_universities': total_universities,
        'total_themes': total_themes,
        'total_gta': total_gta,
        'total_analyzed': total_analyzed,
        'full_text_count': full_text_count,
        'full_text_rate': round(100.0 * full_text_count / total_pr, 1) if total_pr > 0 else 0,
        'year_distribution': year_dist,
        'by_industry': by_industry,
        'top_themes': top_themes,
        'gta_distribution': gta_dist,
        'top_universities': top_universities,
        'recent': recent,
    }

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(f"Stats generated: {OUTPUT_PATH}")
    print(f"  PRs: {total_pr}, Companies: {total_companies}, Analyzed: {total_analyzed}")
    print(f"  Universities: {total_universities}, Themes: {total_themes}, Full text: {stats['full_text_rate']}%")

    conn.close()

if __name__ == '__main__':
    main()
