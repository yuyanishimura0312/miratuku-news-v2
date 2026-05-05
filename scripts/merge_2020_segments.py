#!/usr/bin/env python3
"""Merge 2020-2023 segment JSONs into sangaku_rd.db."""
import sqlite3
import json
import os
import glob

DB_PATH = '/Users/nishimura+/projects/apps/miratuku-news-v2/data/sangaku-rd/sangaku_rd.db'
SEGMENTS_DIR = '/Users/nishimura+/projects/apps/miratuku-news-v2/data/segments_2020'

def main():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=10000")
    c = conn.cursor()

    existing_urls = set(row[0] for row in c.execute("SELECT url FROM press_releases WHERE url IS NOT NULL"))

    total_new = 0
    total_dup = 0

    for seg_file in sorted(glob.glob(os.path.join(SEGMENTS_DIR, 'segment_*.json'))):
        with open(seg_file) as f:
            articles = json.load(f)

        seg_new = 0
        for a in articles:
            url = a.get('url')
            if not url or url in existing_urls:
                total_dup += 1
                continue

            try:
                c.execute("""INSERT INTO press_releases
                    (edinet_code, company_name, title, url, published_at, source, full_text, universities_mentioned, researchers_mentioned, industry)
                    VALUES (?, ?, ?, ?, ?, 'prtimes', ?, ?, ?, ?)""",
                    (a.get('edinet_code'), a.get('company_name'), a.get('title'),
                     url, a.get('published_at'), a.get('full_text'),
                     a.get('universities_mentioned'), None, None))
                existing_urls.add(url)
                seg_new += 1
            except sqlite3.IntegrityError:
                total_dup += 1

        conn.commit()
        total_new += seg_new
        print(f"  {os.path.basename(seg_file)}: +{seg_new} new, {len(articles)} total")

    conn.close()
    print(f"\nMerge complete: +{total_new} new, {total_dup} duplicates skipped")
    print(f"Run 'python3 scripts/generate_sgrd_stats.py' to update dashboard stats")

if __name__ == '__main__':
    main()
