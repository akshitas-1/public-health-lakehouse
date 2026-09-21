"""Download one Our World in Data chart as CSV and save it raw."""

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

BASE_URL = "https://ourworldindata.org/grapher"
RAW_DIR = Path("data/raw/owid")


def fetch_chart(slug: str) -> bytes:
    """Return the full CSV for one chart, as bytes, exactly as served."""
    url = f"{BASE_URL}/{slug}.csv"
    params = {"v": 1, "csvType": "full", "useColumnShortNames": "true"}
    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()
    return response.content


def save_raw(slug: str, content: bytes) -> Path:
    """Write the CSV to disk untouched, stamped with the fetch time."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    fetched_at = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = RAW_DIR / f"{slug}_{fetched_at}.csv"
    path.write_bytes(content)
    return path


if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else "life-expectancy"
    content = fetch_chart(slug)
    path = save_raw(slug, content)
    df = pd.read_csv(path)
    print(f"{slug}: {len(df)} rows, {len(df.columns)} columns saved to {path}")
    print("columns:", list(df.columns))
    print(df.head())