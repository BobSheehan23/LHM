"""
Data loading functions for Lighthouse Quant.
"""

import sqlite3
import pandas as pd
import numpy as np
from typing import Optional, List, Union
from pathlib import Path

from lighthouse_quant.config import DB_PATH, NBER_RECESSIONS, PUBLICATION_LAGS


def load_horizon_dataset(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    columns: Optional[List[str]] = None,
    db_path: Path = DB_PATH
) -> pd.DataFrame:
    """
    Load horizon_dataset from SQLite database.

    Args:
        start_date: Filter data from this date (YYYY-MM-DD)
        end_date: Filter data to this date (YYYY-MM-DD)
        columns: List of columns to load (None = all)
        db_path: Path to database

    Returns:
        DataFrame with date index
    """
    conn = sqlite3.connect(db_path)

    # Build query
    if columns:
        cols = ", ".join(["date"] + [c for c in columns if c != "date"])
        query = f"SELECT {cols} FROM horizon_dataset"
    else:
        query = "SELECT * FROM horizon_dataset"

    # Add date filters
    conditions = []
    if start_date:
        conditions.append(f"date >= '{start_date}'")
    if end_date:
        conditions.append(f"date <= '{end_date}'")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY date"

    df = pd.read_sql(query, conn, parse_dates=["date"])
    df = df.set_index("date").sort_index()

    conn.close()
    return df


def load_lighthouse_indices(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    indices: Optional[List[str]] = None,
    db_path: Path = DB_PATH
) -> pd.DataFrame:
    """
    Load lighthouse_indices from SQLite database.

    Returns wide-format DataFrame with index values as columns.
    """
    conn = sqlite3.connect(db_path)

    query = "SELECT date, index_id, value FROM lighthouse_indices"
    conditions = []

    if start_date:
        conditions.append(f"date >= '{start_date}'")
    if end_date:
        conditions.append(f"date <= '{end_date}'")
    if indices:
        idx_list = ", ".join([f"'{i}'" for i in indices])
        conditions.append(f"index_id IN ({idx_list})")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    df = pd.read_sql(query, conn, parse_dates=["date"])
    conn.close()

    # Pivot to wide format
    df_wide = df.pivot(index="date", columns="index_id", values="value")
    df_wide = df_wide.sort_index()

    return df_wide


def create_nber_recession_series(index: pd.DatetimeIndex) -> pd.Series:
    """
    Create NBER recession indicator series.

    Args:
        index: DatetimeIndex to use

    Returns:
        Series with 1 during recessions, 0 otherwise
    """
    recession = pd.Series(0, index=index, name="NBER_Recession")

    for start, end in NBER_RECESSIONS:
        start_dt = pd.Timestamp(start)
        end_dt = pd.Timestamp(end)
        mask = (index >= start_dt) & (index <= end_dt)
        recession.loc[mask] = 1

    return recession


def apply_publication_lags(
    df: pd.DataFrame,
    as_of_date: pd.Timestamp
) -> pd.DataFrame:
    """
    Apply publication lags to simulate real-time data availability.

    Returns DataFrame with future data (relative to as_of_date) set to NaN.
    """
    result = df.copy()

    for col in result.columns:
        lag_days = PUBLICATION_LAGS.get(col, 0)
        if lag_days > 0:
            cutoff = as_of_date - pd.Timedelta(days=lag_days)
            mask = result.index > cutoff
            result.loc[mask, col] = np.nan

    return result


def resample_to_monthly(df: pd.DataFrame, method: str = "last") -> pd.DataFrame:
    """
    Resample daily data to monthly frequency.

    Args:
        df: DataFrame with daily DatetimeIndex
        method: 'last' (end of month), 'mean', or 'first'

    Returns:
        Monthly DataFrame
    """
    if method == "last":
        return df.resample("ME").last()
    elif method == "mean":
        return df.resample("ME").mean()
    elif method == "first":
        return df.resample("ME").first()
    else:
        raise ValueError(f"Unknown method: {method}")


def get_available_columns(db_path: Path = DB_PATH) -> List[str]:
    """Return list of all columns in horizon_dataset."""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM horizon_dataset LIMIT 1", conn)
    conn.close()
    return [c for c in df.columns if c != "date"]
