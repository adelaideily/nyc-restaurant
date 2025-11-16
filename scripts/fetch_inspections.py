"""
fetch_inspections.py

This script downloads NYC DOHMH Restaurant Inspection Results
from the NYC Open Data API and saves them as a CSV file in the data/ folder.

Dataset:
DOHMH New York City Restaurant Inspection Results (ID: 43nn-pn8j)
"""

import requests
import pandas as pd
from pathlib import Path

BASE_URL = "https://data.cityofnewyork.us/resource/43nn-pn8j.json"

PARAMS = {
    "$limit": 50000,
    "$order": "inspection_date DESC"
}

def main():
    print("Requesting data from NYC Open Data API...")
    response = requests.get(BASE_URL, params=PARAMS)
    response.raise_for_status()

    data = response.json()
    print(f"Downloaded {len(data)} rows.")

    df = pd.DataFrame(data)

    for col in ["inspection_date", "grade_date", "record_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    Path("data").mkdir(exist_ok=True)
    output_path = Path("data/nyc_restaurant_inspections_raw.csv")
    df.to_csv(output_path, index=False)
    print(f"Saved data to {output_path}")

if __name__ == "__main__":
    main()

