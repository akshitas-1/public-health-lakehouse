"""Fetch one indicator from the World Bank API, following pagination, and save it raw."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

BASE_URL = "https://api.worldbank.org/v2/country/all/indicator"
RAW_DIR = Path("data/raw/worldbank")
PER_PAGE = 1000


def fetch_indicator(code: str) -> list[dict]:
    """Return every row for one indicator, looping over all pages."""
    rows: list[dict] = []
    page = 1
    while True:
        url = f"{BASE_URL}/{code}"
        params = {"format": "json", "per_page": PER_PAGE, "page": page}
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        metadata, page_rows = response.json()
        rows.extend(page_rows)
        print(f"  page {page} of {metadata['pages']}: {len(page_rows)} rows")
        if page >= metadata["pages"]:
            break
        page += 1
    return rows


def save_raw(code: str, rows: list[dict]) -> Path:
    """Write the rows to disk untouched, stamped with the fetch time."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    fetched_at = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = RAW_DIR / f"{code}_{fetched_at}.json"
    path.write_text(json.dumps(rows))
    return path


if __name__ == "__main__":
    code = sys.argv[1] if len(sys.argv) > 1 else "SP.DYN.LE00.IN"
    rows = fetch_indicator(code)
    path = save_raw(code, rows)
    print(f"{code}: {len(rows)} rows saved to {path}")
    print("first row:", json.dumps(rows[0], indent=2))