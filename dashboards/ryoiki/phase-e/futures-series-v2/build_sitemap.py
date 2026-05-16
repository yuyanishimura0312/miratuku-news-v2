#!/usr/bin/env python3
"""Generate sitemap.xml for futures-series-v2 (index + ep001-ep100)."""
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET

BASE = "https://journal.emerging-future.org/futures-series-v2"
SRC_DIR = Path(__file__).resolve().parent
OUTPUT = SRC_DIR / "sitemap.xml"
TODAY = datetime.now().strftime("%Y-%m-%d")

urls = [{
    "loc": f"{BASE}/index.html",
    "changefreq": "weekly",
    "priority": "1.0",
    "lastmod": TODAY,
}]
for n in range(1, 101):
    urls.append({
        "loc": f"{BASE}/ep{n:03d}.html",
        "changefreq": "monthly",
        "priority": "0.8",
        "lastmod": TODAY,
    })

urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
for u in urls:
    el = ET.SubElement(urlset, "url")
    ET.SubElement(el, "loc").text = u["loc"]
    ET.SubElement(el, "lastmod").text = u["lastmod"]
    ET.SubElement(el, "changefreq").text = u["changefreq"]
    ET.SubElement(el, "priority").text = u["priority"]

ET.indent(ET.ElementTree(urlset), space="  ")
tree = ET.ElementTree(urlset)
tree.write(OUTPUT, xml_declaration=True, encoding="utf-8")
print(f"Wrote {OUTPUT} ({len(urls)} URLs)")
