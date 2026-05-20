"""Group G: Verify [要確認] DOIs using Crossref API and patch HTML.

Strategy:
1. For each episode, extract all <li><strong>citation</strong>... entries with [要確認] DOI
2. Parse author / year / title from each citation
3. Query Crossref REST API (https://api.crossref.org/works?query=...)
4. If found with high confidence (title fuzzy match), replace [要確認] with real DOI
5. If not found, keep [要確認] but log

This runs PURELY in Python — no codex per episode (since the task is API-driven, not generative).
Parallelized via ThreadPoolExecutor.
"""
import json
import re
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from difflib import SequenceMatcher

SRC_DIR = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series-v2")
BACKUP_DIR = SRC_DIR / "_backup_groupG"
USER_AGENT = "MiratukuFuturesSeriesV2/1.0 (mailto:contact@miratuku.org)"


def crossref_query(query: str, timeout: int = 15) -> list:
    """Query Crossref Works API and return top results."""
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode({
        "query": query,
        "rows": 3,
        "select": "DOI,title,author,issued,container-title",
    })
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read())
            return data.get("message", {}).get("items", [])
    except Exception:
        return []


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_doi(citation_text: str) -> tuple:
    """Return (doi, confidence) or (None, 0) if not found."""
    # Clean for query
    clean = re.sub(r'[<>"]', ' ', citation_text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    # Limit to ~150 chars for query
    query = clean[:200]
    items = crossref_query(query)
    if not items:
        return None, 0.0
    # Pick the best match by title similarity
    # Try to extract a quoted title from the citation
    title_match = re.search(r'["「\']([^"」\']+)["」\']', citation_text)
    target_title = title_match.group(1) if title_match else citation_text[:80]
    best = None
    best_score = 0.0
    for item in items:
        titles = item.get("title", [])
        if not titles:
            continue
        for t in titles:
            s = similarity(target_title, t)
            if s > best_score:
                best_score = s
                best = item
    if best and best_score > 0.55:
        return best.get("DOI"), best_score
    return None, best_score


def process_one_citation(citation_html: str) -> tuple:
    """citation_html is the inner text/HTML of <li>...</li>.
    Returns (new_html, found_doi) or (citation_html, None)."""
    if "[要確認]" not in citation_html:
        return citation_html, None
    # Extract <strong>...</strong> portion
    m = re.search(r'<strong>(.*?)</strong>', citation_html, re.DOTALL)
    if not m:
        return citation_html, None
    citation_text = re.sub(r'<[^>]+>', '', m.group(1))
    doi, conf = find_doi(citation_text)
    if doi:
        new = citation_html.replace("DOI: [要確認]", f"DOI: {doi}", 1)
        return new, doi
    return citation_html, None


def process_file(path: Path) -> dict:
    backup = BACKUP_DIR / path.name
    if not backup.exists():
        backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    text = path.read_text(encoding="utf-8")
    if "[要確認]" not in text:
        return {"file": path.name, "status": "skip", "found": 0, "total": 0}
    # Find all <li>...</li> within ref-list
    ref_list_match = re.search(r'<ul class="ref-list"[^>]*>(.*?)</ul>', text, re.DOTALL)
    if not ref_list_match:
        return {"file": path.name, "status": "no-ref-list", "found": 0, "total": 0}
    ref_html = ref_list_match.group(1)
    items = re.findall(r'<li>(.*?)</li>', ref_html, re.DOTALL)
    found = 0
    total_to_verify = sum(1 for it in items if "[要確認]" in it)
    new_ref_html = ref_html
    for item_html in items:
        if "[要確認]" not in item_html:
            continue
        new_item, doi = process_one_citation(item_html)
        if doi:
            new_ref_html = new_ref_html.replace(item_html, new_item, 1)
            found += 1
    if new_ref_html != ref_html:
        text = text.replace(ref_html, new_ref_html, 1)
        path.write_text(text, encoding="utf-8")
    return {"file": path.name, "status": "ok", "found": found, "total": total_to_verify}


def main():
    BACKUP_DIR.mkdir(exist_ok=True)
    files = sorted([p for p in SRC_DIR.glob("ep*.html") if re.match(r"ep\d{3}\.html$", p.name)])
    print(f"=== Group G: Crossref DOI verification ===")
    print(f"Files: {len(files)}")

    results = []
    # Throttle to ~20 parallel (Crossref recommends modest rate)
    with ThreadPoolExecutor(max_workers=20) as pool:
        futs = {pool.submit(process_file, p): p for p in files}
        for fut in as_completed(futs):
            r = fut.result()
            results.append(r)
            if r["status"] == "ok":
                print(f"  [{r['file']}] found {r['found']}/{r['total']} DOIs")
            else:
                print(f"  [{r['file']}] {r['status']}")

    total_found = sum(r.get("found", 0) for r in results)
    total_attempted = sum(r.get("total", 0) for r in results)
    print(f"\n=== Final: {total_found}/{total_attempted} DOIs resolved ===")


if __name__ == "__main__":
    main()
