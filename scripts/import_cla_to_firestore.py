#!/usr/bin/env python3
"""
Import CLA historical data into Firestore.

Reads cla_historical_yearly.json and cla_historical_quarterly.json
from the future-insight-app data directory and stores each period
as a document in the 'cla_historical' Firestore collection.

Collection structure:
  cla_historical/{period}
    - period: "1990" or "2025-Q1"
    - type: "yearly" or "quarterly"
    - categories: { Political: { litany, systemic_causes, worldview, myth_metaphor }, ... }
    - cross_category_synthesis: "..."
    - imported_at: timestamp

Also stores meta report in:
  cla_meta/{region}  (japan, global)

Usage:
  GOOGLE_APPLICATION_CREDENTIALS=path/to/serviceAccount.json python3 scripts/import_cla_to_firestore.py
  # Or using the admin page import feature in the browser
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    print("[ERROR] firebase-admin package not installed. Install with:")
    print("  pip install firebase-admin")
    sys.exit(1)


DATA_DIR = Path(__file__).parent.parent.parent / "future-insight-app" / "data"
COLLECTION = "cla_historical"
META_COLLECTION = "cla_meta"


def init_firestore():
    """Initialize Firestore client."""
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {"projectId": "miratuku-afa2c"})
    return firestore.client()


def load_json(filename):
    """Load JSON file from data directory."""
    path = DATA_DIR / filename
    if not path.exists():
        print(f"[WARN] {path} not found")
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else data.get("entries", [])


def import_historical(db_client):
    """Import yearly and quarterly CLA data into Firestore."""
    yearly = load_json("cla_historical_yearly.json")
    quarterly = load_json("cla_historical_quarterly.json")

    print(f"  Yearly entries: {len(yearly)}")
    print(f"  Quarterly entries: {len(quarterly)}")

    batch = db_client.batch()
    count = 0

    for entry in yearly + quarterly:
        period = entry.get("period", "")
        if not period:
            continue

        doc_ref = db_client.collection(COLLECTION).document(period)
        doc_data = {
            "period": period,
            "type": entry.get("type", "yearly" if not any(c in period for c in ["-", "Q"]) else "quarterly"),
            "categories": entry.get("categories", {}),
            "cross_category_synthesis": entry.get("cross_category_synthesis", ""),
            "imported_at": firestore.SERVER_TIMESTAMP,
        }
        batch.set(doc_ref, doc_data)
        count += 1

        # Firestore batch limit is 500
        if count % 400 == 0:
            batch.commit()
            batch = db_client.batch()
            print(f"  Committed {count} documents...")

    if count % 400 != 0:
        batch.commit()

    print(f"  Total: {count} CLA entries imported to '{COLLECTION}' collection")
    return count


def import_meta(db_client):
    """Import meta analysis reports into Firestore."""
    path = DATA_DIR / "cla_meta_report.json"
    if not path.exists():
        print("[WARN] cla_meta_report.json not found, skipping meta import")
        return 0

    with open(path, encoding="utf-8") as f:
        meta = json.load(f)

    count = 0
    for region in ["japan", "global"]:
        if region in meta:
            doc_ref = db_client.collection(META_COLLECTION).document(region)
            doc_data = {
                **meta[region],
                "data_coverage": meta.get("data_coverage", {}),
                "generated_at": meta.get("generated_at", ""),
                "imported_at": firestore.SERVER_TIMESTAMP,
            }
            doc_ref.set(doc_data)
            count += 1
            chars = len(meta[region].get("report_text", ""))
            print(f"  {region}: {chars} chars imported to '{META_COLLECTION}'")

    return count


def main():
    print(f"{'=' * 60}")
    print(f"  CLA Firestore Import")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'=' * 60}")

    db_client = init_firestore()

    print("\n[1/2] Importing historical CLA data...")
    hist_count = import_historical(db_client)

    print("\n[2/2] Importing meta analysis reports...")
    meta_count = import_meta(db_client)

    print(f"\n{'=' * 60}")
    print(f"  Complete: {hist_count} historical + {meta_count} meta documents")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
