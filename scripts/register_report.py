#!/usr/bin/env python3
"""Register a new analysis report in analysis-reports.json.

Usage:
  python3 scripts/register_report.py \\
    --id "my-report-2026" \\
    --title "Report Title" \\
    --subtitle "Optional subtitle" \\
    --date "2026-05-01" \\
    --databases "DB1,DB2" \\
    --tags "tag1,tag2" \\
    --summary "Brief summary text" \\
    --findings "Finding 1||Finding 2||Finding 3" \\
    --report-file "reports/my-report.html" \\
    --dashboard "dashboards/my-dashboard.html" \\
    --word-count 15000 \\
    --sections 8

If --id already exists, the entry is updated (upsert).
If --date is omitted, today's date is used.
If --id is omitted, it is derived from the report filename.
"""

import argparse
import json
import os
import re
import sys
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
JSON_PATH = os.path.join(PROJECT_DIR, 'data', 'analysis-reports.json')


def estimate_word_count(report_file):
    """Estimate word count from HTML report file."""
    fpath = os.path.join(PROJECT_DIR, report_file)
    if not os.path.exists(fpath):
        return 0
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    # Strip HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', '', text)  # CJK: count characters
    return len(text)


def count_sections(report_file):
    """Count h2/h3 sections in HTML report."""
    fpath = os.path.join(PROJECT_DIR, report_file)
    if not os.path.exists(fpath):
        return 0
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    return len(re.findall(r'<h[23][^>]*>', text))


def derive_id(report_file):
    """Derive report ID from filename."""
    basename = os.path.basename(report_file)
    name = os.path.splitext(basename)[0]
    return name


def main():
    parser = argparse.ArgumentParser(description='Register analysis report')
    parser.add_argument('--id', help='Report ID (derived from filename if omitted)')
    parser.add_argument('--title', required=True, help='Report title')
    parser.add_argument('--subtitle', default='', help='Report subtitle')
    parser.add_argument('--date', default=date.today().isoformat(), help='Publication date (YYYY-MM-DD)')
    parser.add_argument('--databases', default='', help='Comma-separated database names')
    parser.add_argument('--tags', default='', help='Comma-separated tags')
    parser.add_argument('--summary', default='', help='Summary text')
    parser.add_argument('--findings', default='', help='Key findings separated by ||')
    parser.add_argument('--report-file', required=True, help='Path to report HTML (relative to project root)')
    parser.add_argument('--dashboard', default='', help='Path to dashboard HTML')
    parser.add_argument('--word-count', type=int, default=0, help='Word count (auto-estimated if 0)')
    parser.add_argument('--sections', type=int, default=0, help='Section count (auto-counted if 0)')
    args = parser.parse_args()

    # Load existing data
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    report_id = args.id or derive_id(args.report_file)

    # Auto-estimate if not provided
    word_count = args.word_count or estimate_word_count(args.report_file)
    sections = args.sections or count_sections(args.report_file)

    databases = [d.strip() for d in args.databases.split(',') if d.strip()]
    tags = [t.strip() for t in args.tags.split(',') if t.strip()]
    findings = [f.strip() for f in args.findings.split('||') if f.strip()]

    entry = {
        'id': report_id,
        'title': args.title,
        'subtitle': args.subtitle,
        'date': args.date,
        'databases': databases,
        'tags': tags,
        'summary': args.summary,
        'key_findings': findings,
        'word_count': word_count,
        'sections': sections,
        'report_file': args.report_file,
    }
    if args.dashboard:
        entry['dashboard'] = args.dashboard

    # Upsert: replace if ID exists, otherwise prepend (newest first)
    existing_idx = None
    for i, r in enumerate(data['reports']):
        if r['id'] == report_id:
            existing_idx = i
            break

    if existing_idx is not None:
        data['reports'][existing_idx] = entry
        action = 'Updated'
    else:
        data['reports'].insert(0, entry)
        action = 'Added'

    # Write back
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'{action} report: {report_id}')
    print(f'  Title: {args.title}')
    print(f'  Date: {args.date}')
    print(f'  Databases: {databases}')
    print(f'  Word count: {word_count}')
    print(f'  Sections: {sections}')
    print(f'  File: {args.report_file}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
