#!/usr/bin/env python3
"""
Segment-based collector for 2020-2023 period.
Usage: python3 collect_2020_segment.py <segment_id> <total_segments>
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
OUTPUT_DIR = '/Users/nishimura+/projects/apps/miratuku-news-v2/data/segments_2020'
CUTOFF_START = '2020-01-01'
CUTOFF_END = '2023-05-01'

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

def fetch(url, retries=3):
    hdrs = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
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
    return None

def main():
    seg_id = int(sys.argv[1])
    total_segs = int(sys.argv[2])

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, f'segment_{seg_id:03d}.json')

    conn = sqlite3.connect(DB_PATH, timeout=30)
    c = conn.cursor()

    companies = c.execute("SELECT edinet_code, name FROM companies ORDER BY edinet_code").fetchall()
    # Get existing URLs to avoid duplicates
    existing_urls = set(row[0] for row in c.execute("SELECT url FROM press_releases WHERE url IS NOT NULL"))
    conn.close()

    # Split into segments
    seg_size = len(companies) // total_segs
    start = seg_id * seg_size
    end = start + seg_size if seg_id < total_segs - 1 else len(companies)
    my_companies = companies[start:end]

    print(f"Segment {seg_id}: companies {start}-{end} ({len(my_companies)} companies)")

    results = []
    processed = 0

    for edinet_code, name in my_companies:
        clean = name.replace('株式会社','').replace('有限会社','').replace('合同会社','')
        clean = clean.replace('　',' ').replace('（','').replace('）','').strip()
        if not clean or len(clean) < 2:
            continue

        seen_urls = set()

        for search_term in [f'{clean} 研究開発 2020', f'{clean} 研究開発 2021', f'{clean} 研究開発 2022', f'{clean} 共同研究 2021']:
            prs, total = search_prtimes(search_term, 1)
            if not prs:
                continue

            all_prs = list(prs)
            if total > 40:
                for page in range(2, min(4, (total//40)+2)):
                    more, _ = search_prtimes(search_term, page)
                    if more:
                        all_prs.extend(more)
                    time.sleep(0.7)

            for r in all_prs:
                title = r['title']
                url = r['url']
                date = r['date']

                if not url or url in seen_urls or not title:
                    continue
                seen_urls.add(url)

                if not date or date < CUTOFF_START or date >= CUTOFF_END:
                    continue
                if not is_rd(title):
                    continue
                if url in existing_urls:
                    continue

                full_text = fetch_article_text(url)
                time.sleep(0.4)

                if not full_text:
                    full_text = title

                combined = title + ' ' + (full_text or '')
                univs = list(set(UNIV_RE.findall(combined)))

                results.append({
                    'edinet_code': edinet_code,
                    'company_name': name,
                    'title': title,
                    'url': url,
                    'published_at': date,
                    'full_text': full_text,
                    'universities_mentioned': ', '.join(univs) if univs else None,
                })
                existing_urls.add(url)

            time.sleep(0.5)

        processed += 1
        if processed % 50 == 0:
            # Save intermediate
            with open(output_file, 'w') as f:
                json.dump(results, f, ensure_ascii=False)
            print(f"  Segment {seg_id}: [{processed}/{len(my_companies)}] {len(results)} articles")

    with open(output_file, 'w') as f:
        json.dump(results, f, ensure_ascii=False)
    print(f"Segment {seg_id} done: {processed} companies, {len(results)} articles")

if __name__ == '__main__':
    main()
