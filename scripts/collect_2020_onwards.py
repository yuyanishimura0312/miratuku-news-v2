#!/usr/bin/env python3
"""
Collect R&D press releases from 2020 onwards for all companies.
Targets the gap period: 2020-01-01 to 2023-05-04 (before original collection started).
"""
import sqlite3
import urllib.request
import urllib.parse
import time
import re
import os
import sys
import json
from datetime import datetime

DB_PATH = '/Users/nishimura+/projects/apps/miratuku-news-v2/data/sangaku-rd/sangaku_rd.db'
CUTOFF_START = '2020-01-01'
CUTOFF_END = '2023-05-01'  # Before original collection period

RD_KEYWORDS = [
    '研究開発','共同研究','産学連携','技術開発','新技術','特許','論文',
    '学会','研究成果','実証実験','実用化','AI','人工知能','DX','IoT',
    '量子','バイオ','ゲノム','創薬','再生医療','脱炭素','水素',
    '半導体','ロボット','自動運転','宇宙','大学','研究所','博士','教授',
    '開発成功','世界初','日本初','R&D','新素材','ナノ','センサー',
    '臨床試験','治験','基盤技術','次世代','革新的','研究機関',
    'カーボンニュートラル','燃料電池','光学','デバイス','プラットフォーム',
    '機械学習','ディープラーニング','深層学習','自然言語処理','画像認識',
    'リチウム','電池','蓄電','再生可能エネルギー','太陽光',
    '抗体','ワクチン','診断','医療機器','ヘルスケア',
]

UNIV_RE = re.compile(r'([^\s,、。]{2,10}(?:大学|研究所|研究機構|研究センター))')
RESEARCHER_RE = re.compile(r'([^\s,、。（）]{2,6})\s*(?:教授|准教授|助教|講師|主任研究員|研究員|フェロー)')

def fetch(url, retries=3):
    hdrs = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'ja,en;q=0.5',
    }
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode('utf-8', errors='replace')
        except:
            if i < retries-1:
                time.sleep(2*(i+1))
    return None

def is_rd(title, text=''):
    s = (title+' '+text).lower()
    return sum(1 for k in RD_KEYWORDS if k.lower() in s) >= 1

def parse_date(date_str):
    m = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', date_str)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    return None

def search_prtimes(query, page=1):
    encoded = urllib.parse.quote(query)
    url = f'https://prtimes.jp/main/action.php?run=html&page=searchkey&search_word={encoded}&pagenum={page}'
    html = fetch(url)
    if not html:
        return [], 0
    nd = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
    if not nd:
        return [], 0
    try:
        data = json.loads(nd.group(1))
        pages = data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['pages']
        page_data = pages[0]
        total = int(page_data.get('total', 0))
        releases = page_data.get('releaseList', [])
        results = []
        for r in releases:
            results.append({
                'title': r.get('title', ''),
                'url': f"https://prtimes.jp{r.get('releaseUrl', '')}",
                'date': parse_date(r.get('releasedAt', '')),
                'company_pr': r.get('companyName', ''),
            })
        return results, total
    except:
        return [], 0

def fetch_article_text(url):
    html = fetch(url)
    if not html:
        return None
    nd = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
    if nd:
        try:
            data = json.loads(nd.group(1))
            ds = data.get('props',{}).get('pageProps',{}).get('dehydratedState',{})
            for q in ds.get('queries',[]):
                rd = q.get('state',{}).get('data',{})
                if isinstance(rd, dict):
                    body = rd.get('body','') or rd.get('releaseBody','') or rd.get('content','')
                    if body:
                        body = re.sub(r'<br\s*/?>', '\n', body)
                        body = re.sub(r'</(p|div|h[1-6]|li)>', '\n', body)
                        body = re.sub(r'<[^>]+>', ' ', body)
                        body = re.sub(r'&[a-z]+;', ' ', body)
                        body = re.sub(r'\n\s*\n', '\n', body).strip()
                        return body
        except:
            pass
    for pattern in [r'class="[^"]*article-body[^"]*"[^>]*>(.*?)</div>',
                    r'class="[^"]*rich-text[^"]*"[^>]*>(.*?)</div>',
                    r'class="[^"]*release-body[^"]*"[^>]*>(.*?)</div>']:
        m = re.search(pattern, html, re.DOTALL)
        if m:
            body = m.group(1)
            body = re.sub(r'<br\s*/?>', '\n', body)
            body = re.sub(r'</(p|div|h[1-6]|li)>', '\n', body)
            body = re.sub(r'<[^>]+>', ' ', body)
            body = re.sub(r'&[a-z]+;', ' ', body)
            body = re.sub(r'\n\s*\n', '\n', body).strip()
            if body:
                return body
    return None

def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 500

    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=10000")
    c = conn.cursor()

    # Get companies - prioritize those with higher R&D expense
    companies = c.execute("""
        SELECT edinet_code, name FROM companies
        ORDER BY COALESCE(rd_expense, 0) DESC
    """).fetchall()

    print(f"Collecting 2020-2023 PRs for {len(companies)} companies (limit={limit})")

    total_new = 0
    processed = 0

    for edinet_code, name in companies:
        if processed >= limit:
            break

        clean = name.replace('株式会社','').replace('有限会社','').replace('合同会社','')
        clean = clean.replace('　',' ').replace('（','').replace('）','').strip()
        if not clean or len(clean) < 2:
            continue

        company_new = 0
        seen_urls = set()

        for search_term in [f'{clean} 研究開発 2020', f'{clean} 研究開発 2021', f'{clean} 研究開発 2022', f'{clean} 共同研究']:
            results, total = search_prtimes(search_term, 1)
            if not results:
                continue

            all_results = list(results)
            if total > 40:
                for page in range(2, min(4, (total//40)+2)):
                    more, _ = search_prtimes(search_term, page)
                    if more:
                        all_results.extend(more)
                    time.sleep(0.7)

            for r in all_results:
                title = r['title']
                url = r['url']
                date = r['date']

                if not url or url in seen_urls or not title or len(title) < 5:
                    continue
                seen_urls.add(url)

                # Only collect 2020-2023 period
                if not date:
                    continue
                if date < CUTOFF_START or date >= CUTOFF_END:
                    continue
                if not is_rd(title):
                    continue

                c.execute("SELECT id FROM press_releases WHERE url=?", (url,))
                if c.fetchone():
                    continue

                full_text = fetch_article_text(url)
                time.sleep(0.5)

                if not full_text:
                    full_text = title

                combined = title + ' ' + (full_text or '')
                univs = list(set(UNIV_RE.findall(combined)))
                researchers = list(set(RESEARCHER_RE.findall(combined)))

                try:
                    c.execute("""INSERT INTO press_releases
                        (edinet_code, company_name, title, url, published_at, source, full_text, universities_mentioned, researchers_mentioned, industry)
                        VALUES (?, ?, ?, ?, ?, 'prtimes', ?, ?, ?, ?)""",
                        (edinet_code, name, title, url, date, full_text,
                         ', '.join(univs) if univs else None,
                         ', '.join(researchers) if researchers else None,
                         None))
                    company_new += 1
                    total_new += 1
                except sqlite3.IntegrityError:
                    pass

            time.sleep(0.5)

        if company_new > 0:
            conn.commit()

        processed += 1
        if processed % 50 == 0:
            conn.commit()
            print(f"  [{processed}/{limit}] +{total_new} new PRs (2020-2023)")

    conn.commit()
    conn.close()
    print(f"\nDone: processed {processed} companies, collected {total_new} new PRs (2020-2023)")

if __name__ == '__main__':
    main()
