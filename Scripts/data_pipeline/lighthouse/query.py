"""
LIGHTHOUSE MACRO - QUERY HELPERS
================================
Clean interfaces for querying the master database.
"""

import sqlite3
import pandas as pd
from pathlib import Path
from typing import Optional, List
from datetime import datetime, timedelta

from .config import DB_PATH, OUTPUT_DIR


# ==========================================
# SERIES QUERIES
# ==========================================

def get_series(
    series_id: str,
    start_date: str = None,
    end_date: str = None,
    db_path: Path = None
) -> pd.DataFrame:
    """
    Query a specific series from the database.

    Args:
        series_id: The series identifier (e.g., 'UNRATE', 'BLS_CES0000000001')
        start_date: Optional start date (YYYY-MM-DD)
        end_date: Optional end date (YYYY-MM-DD)
        db_path: Optional custom database path

    Returns:
        DataFrame with 'date' index and 'value' column
    """
    db_path = db_path or DB_PATH
    conn = sqlite3.connect(db_path)

    query = "SELECT date, value FROM observations WHERE series_id = ?"
    params = [series_id]

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)

    query += " ORDER BY date"

    df = pd.read_sql(query, conn, params=params)
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date")

    conn.close()
    return df


def get_multiple_series(
    series_ids: List[str],
    start_date: str = None,
    end_date: str = None,
    db_path: Path = None
) -> pd.DataFrame:
    """
    Query multiple series and return wide-format DataFrame.

    Args:
        series_ids: List of series identifiers
        start_date: Optional start date
        end_date: Optional end date
        db_path: Optional custom database path

    Returns:
        DataFrame with date index and series as columns
    """
    db_path = db_path or DB_PATH
    conn = sqlite3.connect(db_path)

    placeholders = ",".join(["?" for _ in series_ids])
    query = f"SELECT date, series_id, value FROM observations WHERE series_id IN ({placeholders})"
    params = list(series_ids)

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)

    query += " ORDER BY date"

    df = pd.read_sql(query, conn, params=params)
    df["date"] = pd.to_datetime(df["date"])

    # Pivot to wide format
    df_wide = df.pivot(index="date", columns="series_id", values="value")
    df_wide = df_wide[series_ids]  # Maintain order

    conn.close()
    return df_wide


def search_series(
    keyword: str,
    source: str = None,
    category: str = None,
    db_path: Path = None
) -> pd.DataFrame:
    """
    Search for series by keyword in title or series_id.

    Args:
        keyword: Search term
        source: Optional filter by source (FRED, BLS, BEA, NYFED, OFR)
        category: Optional filter by category
        db_path: Optional custom database path

    Returns:
        DataFrame with matching series metadata
    """
    db_path = db_path or DB_PATH
    conn = sqlite3.connect(db_path)

    query = """
        SELECT series_id, title, source, category, frequency, data_quality, obs_count
        FROM series_meta
        WHERE (title LIKE ? OR series_id LIKE ?)
    """
    params = [f"%{keyword}%", f"%{keyword}%"]

    if source:
        query += " AND source = ?"
        params.append(source)
    if category:
        query += " AND category LIKE ?"
        params.append(f"%{category}%")

    query += " ORDER BY source, category, title"

    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df


def get_category(
    category: str,
    db_path: Path = None
) -> pd.DataFrame:
    """Get all series in a category."""
    db_path = db_path or DB_PATH
    conn = sqlite3.connect(db_path)

    df = pd.read_sql("""
        SELECT series_id, title, source, frequency, data_quality
        FROM series_meta
        WHERE category = ?
        ORDER BY title
    """, conn, params=[category])

    conn.close()
    return df


def get_sources(db_path: Path = None) -> pd.DataFrame:
    """Get summary of all sources."""
    db_path = db_path or DB_PATH
    conn = sqlite3.connect(db_path)

    df = pd.read_sql("""
        SELECT source,
               COUNT(*) as series_count,
               SUM(obs_count) as total_obs
        FROM series_meta
        GROUP BY source
        ORDER BY series_count DESC
    """, conn)

    conn.close()
    return df


def get_categories(source: str = None, db_path: Path = None) -> pd.DataFrame:
    """Get all categories (optionally filtered by source)."""
    db_path = db_path or DB_PATH
    conn = sqlite3.connect(db_path)

    query = """
        SELECT source, category, COUNT(*) as series_count
        FROM series_meta
    """
    params = []

    if source:
        query += " WHERE source = ?"
        params.append(source)

    query += " GROUP BY source, category ORDER BY source, series_count DESC"

    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df


# ==========================================
# EXPORT FUNCTIONS
# ==========================================

def export_wide(
    output_path: Path = None,
    start_date: str = "2000-01-01",
    series_ids: List[str] = None,
    db_path: Path = None
) -> Path:
    """
    Export data to wide-format CSV.

    Args:
        output_path: Output file path (default: Lighthouse_Master_Wide.csv)
        start_date: Start date for export
        series_ids: Optional list of specific series to export
        db_path: Optional custom database path

    Returns:
        Path to exported file
    """
    db_path = db_path or DB_PATH
    output_path = output_path or OUTPUT_DIR / "Lighthouse_Master_Wide.csv"

    conn = sqlite3.connect(db_path)

    if series_ids:
        placeholders = ",".join(["?" for _ in series_ids])
        query = f"""
            SELECT o.date, m.title, o.value
            FROM observations o
            JOIN series_meta m ON o.series_id = m.series_id
            WHERE o.date >= ? AND o.series_id IN ({placeholders})
            ORDER BY o.date
        """
        params = [start_date] + list(series_ids)
    else:
        query = """
            SELECT o.date, m.title, o.value
            FROM observations o
            JOIN series_meta m ON o.series_id = m.series_id
            WHERE o.date >= ?
            ORDER BY o.date
        """
        params = [start_date]

    df = pd.read_sql(query, conn, params=params)
    df_wide = df.pivot_table(index="date", columns="title", values="value")
    df_wide.to_csv(output_path)

    print(f"Exported to: {output_path}")
    print(f"Shape: {df_wide.shape[0]} rows x {df_wide.shape[1]} columns")

    conn.close()
    return output_path


def export_long(
    output_path: Path = None,
    start_date: str = "2000-01-01",
    db_path: Path = None
) -> Path:
    """
    Export data to long-format CSV (better for some models).

    Args:
        output_path: Output file path
        start_date: Start date for export
        db_path: Optional custom database path

    Returns:
        Path to exported file
    """
    db_path = db_path or DB_PATH
    output_path = output_path or OUTPUT_DIR / "Lighthouse_Master_Long.csv"

    conn = sqlite3.connect(db_path)

    query = """
        SELECT o.date, o.series_id, m.title, m.source, m.category, o.value
        FROM observations o
        JOIN series_meta m ON o.series_id = m.series_id
        WHERE o.date >= ?
        ORDER BY o.date, o.series_id
    """

    df = pd.read_sql(query, conn, params=[start_date])
    df.to_csv(output_path, index=False)

    print(f"Exported to: {output_path}")
    print(f"Rows: {len(df):,}")

    conn.close()
    return output_path


# ==========================================
# METADATA QUERIES
# ==========================================

def get_series_info(series_id: str, db_path: Path = None) -> dict:
    """Get metadata for a specific series."""
    db_path = db_path or DB_PATH
    conn = sqlite3.connect(db_path)

    row = conn.execute("""
        SELECT series_id, title, source, category, frequency, units,
               last_updated, data_quality, obs_count, last_value_date
        FROM series_meta
        WHERE series_id = ?
    """, [series_id]).fetchone()

    conn.close()

    if row:
        columns = ["series_id", "title", "source", "category", "frequency", "units",
                   "last_updated", "data_quality", "obs_count", "last_value_date"]
        return dict(zip(columns, row))
    return None


def get_latest_values(
    series_ids: List[str] = None,
    db_path: Path = None
) -> pd.DataFrame:
    """
    Get the most recent value for specified series (or all if none specified).

    Useful for dashboards and quick checks.
    """
    db_path = db_path or DB_PATH
    conn = sqlite3.connect(db_path)

    if series_ids:
        placeholders = ",".join(["?" for _ in series_ids])
        query = f"""
            SELECT m.series_id, m.title, m.last_value_date as date,
                   (SELECT value FROM observations o
                    WHERE o.series_id = m.series_id
                    ORDER BY o.date DESC LIMIT 1) as value
            FROM series_meta m
            WHERE m.series_id IN ({placeholders})
        """
        df = pd.read_sql(query, conn, params=series_ids)
    else:
        query = """
            SELECT m.series_id, m.title, m.last_value_date as date,
                   (SELECT value FROM observations o
                    WHERE o.series_id = m.series_id
                    ORDER BY o.date DESC LIMIT 1) as value
            FROM series_meta m
            ORDER BY m.source, m.title
        """
        df = pd.read_sql(query, conn)

    conn.close()
    return df
