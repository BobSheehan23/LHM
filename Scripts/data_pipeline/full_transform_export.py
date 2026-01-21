"""
LIGHTHOUSE MACRO - FULL DATABASE TRANSFORM & EXPORT
====================================================
Takes ALL series from master database.
Applies smart transformations based on series characteristics.
Exports full CSV for model ingestion.

Now uses centralized transforms from lighthouse package.
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import re
import sys
import os

# Add lighthouse package to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lighthouse.config import DB_PATH, OUTPUT_DIR
from lighthouse.transforms import (
    infer_frequency,
    infer_series_type,
    get_default_transforms,
    apply_transforms
)

# ==========================================
# CONFIGURATION
# ==========================================

OUTPUT_CSV = OUTPUT_DIR / "Lighthouse_Full_Transformed.csv"
OUTPUT_LONG_CSV = OUTPUT_DIR / "Lighthouse_Full_Long.csv"
YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def clean_column_name(name: str) -> str:
    """Clean column name for CSV compatibility."""
    name = re.sub(r'[^\w\s\-]', '', name)
    name = re.sub(r'\s+', '_', name)
    return name[:80]


def build_full_export():
    """Build the full transformed dataset from all series."""
    print("=" * 70)
    print("LIGHTHOUSE MACRO - FULL DATABASE TRANSFORM")
    print(f"Source: {DB_PATH}")
    print(f"Cutoff: {YESTERDAY}")
    print("=" * 70)

    conn = sqlite3.connect(DB_PATH)

    # Get all series
    series_meta = pd.read_sql("SELECT series_id, title, source, category FROM series_meta", conn)
    print(f"\nTotal series in database: {len(series_meta)}")

    all_data = {}
    processed = 0
    skipped = 0
    total_transforms = 0

    print("\n--- Processing All Series ---")

    for idx, row in series_meta.iterrows():
        series_id = row["series_id"]
        title = row["title"] or series_id
        source = row["source"]

        # Fetch data
        query = "SELECT date, value FROM observations WHERE series_id = ? ORDER BY date"
        df = pd.read_sql(query, conn, params=[series_id])

        if df.empty or len(df) < 5:
            skipped += 1
            continue

        # Convert and dedupe
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date", "value"])
        df = df.set_index("date")
        df = df[~df.index.duplicated(keep='first')]
        df = df.sort_index()

        # Trim to yesterday max
        df = df[df.index <= YESTERDAY]

        if len(df) < 5:
            skipped += 1
            continue

        # Use centralized transform logic
        freq = infer_frequency(df)
        series_type = infer_series_type(series_id, title)
        transforms = get_default_transforms(series_type, freq)

        # Apply transforms
        df_transformed = apply_transforms(df["value"], transforms, freq)

        # Create clean base name
        base_name = clean_column_name(f"{source}_{series_id}")

        # Add to output
        for col in df_transformed.columns:
            if col == "raw":
                col_name = base_name
            else:
                col_name = f"{base_name}_{col}"

            all_data[col_name] = df_transformed[col]
            total_transforms += 1

        processed += 1

        if processed % 100 == 0:
            print(f"   Processed {processed} series...")

    conn.close()

    print(f"\n   Processed: {processed} series")
    print(f"   Skipped: {skipped} series (insufficient data)")
    print(f"   Total columns: {total_transforms}")

    # Combine into DataFrame
    print("\n--- Building Combined Dataset ---")
    full_df = pd.DataFrame(all_data)
    full_df.index.name = "date"
    full_df = full_df.sort_index()

    # Remove completely empty rows
    full_df = full_df.dropna(how='all')

    print(f"\nDataset Shape: {full_df.shape[0]:,} rows x {full_df.shape[1]:,} columns")
    print(f"Date Range: {full_df.index.min().date()} to {full_df.index.max().date()}")

    # Memory estimate
    mem_mb = full_df.memory_usage(deep=True).sum() / 1024 / 1024
    print(f"Memory: {mem_mb:.1f} MB")

    # Export wide format
    print(f"\n--- Exporting Wide CSV ---")
    full_df.to_csv(OUTPUT_CSV)
    csv_size = OUTPUT_CSV.stat().st_size / 1024 / 1024
    print(f"   Saved: {OUTPUT_CSV}")
    print(f"   Size: {csv_size:.1f} MB")

    # Also export long format
    print(f"\n--- Exporting Long CSV ---")
    long_df = full_df.reset_index().melt(id_vars=["date"], var_name="series", value_name="value")
    long_df = long_df.dropna(subset=["value"])
    long_df.to_csv(OUTPUT_LONG_CSV, index=False)
    long_size = OUTPUT_LONG_CSV.stat().st_size / 1024 / 1024
    print(f"   Saved: {OUTPUT_LONG_CSV}")
    print(f"   Size: {long_size:.1f} MB")
    print(f"   Rows: {len(long_df):,}")

    # Summary by source
    print("\n--- Column Summary by Source ---")
    source_counts = {}
    for col in full_df.columns:
        source = col.split("_")[0]
        source_counts[source] = source_counts.get(source, 0) + 1
    for source, count in sorted(source_counts.items(), key=lambda x: -x[1]):
        print(f"   {source}: {count} columns")

    print("\n" + "=" * 70)
    print("EXPORT COMPLETE")
    print("=" * 70)

    return full_df


if __name__ == "__main__":
    df = build_full_export()
    print("\nSample columns:")
    print(list(df.columns[:20]))
