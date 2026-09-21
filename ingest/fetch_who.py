"""Fetch one indicator from the WHO Global Health Observatory API and save it raw."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

BASE_URL = "https://ghoapi.azureedge.net/api"
RAW_DIR = Path("data/raw/who")


def fetch_indicator(code: str) -> list[dict]:
    """Return every row the API has for one indicator code."""
    url = f"{BASE_URL}/{code}"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return response.json()["value"]


def save_raw(code: str, rows: list[dict]) -> Path:
    """Write the rows to disk untouched, stamped with the fetch time."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    fetched_at = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = RAW_DIR / f"{code}_{fetched_at}.json"
    path.write_text(json.dumps(rows))
    return path


if __name__ == "__main__":
    code = sys.argv[1] if len(sys.argv) > 1 else "WHOSIS_000001"
    rows = fetch_indicator(code)
    path = save_raw(code, rows)
    print(f"{code}: {len(rows)} rows saved to {path}")
    print("first row:", json.dumps(rows[0], indent=2))