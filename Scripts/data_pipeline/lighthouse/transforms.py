"""
LIGHTHOUSE MACRO - TRANSFORMS
=============================
Centralized transform functions. Single source of truth.
Both full_transform_export and horizon_dataset_builder use this.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Callable

# ==========================================
# CORE TRANSFORM FUNCTIONS
# ==========================================

def yoy_pct(s: pd.Series, periods: int = 12) -> pd.Series:
    """Year-over-year percent change."""
    return s.pct_change(periods) * 100


def yoy_diff(s: pd.Series, periods: int = 12) -> pd.Series:
    """Year-over-year difference (for rates/spreads)."""
    return s.diff(periods)


def mom_pct(s: pd.Series) -> pd.Series:
    """Month-over-month percent change."""
    return s.pct_change(1) * 100


def mom_diff(s: pd.Series) -> pd.Series:
    """Month-over-month difference."""
    return s.diff(1)


def mom_diff_3ma(s: pd.Series) -> pd.Series:
    """3-month moving average of MoM difference."""
    return s.diff(1).rolling(3).mean()


def qoq_pct(s: pd.Series) -> pd.Series:
    """Quarter-over-quarter percent change."""
    return s.pct_change(1) * 100


def wow_pct(s: pd.Series) -> pd.Series:
    """Week-over-week percent change."""
    return s.pct_change(1) * 100


def wow_diff(s: pd.Series) -> pd.Series:
    """Week-over-week difference."""
    return s.diff(1)


def diff(s: pd.Series) -> pd.Series:
    """Simple first difference."""
    return s.diff(1)


def ann_3m(s: pd.Series) -> pd.Series:
    """3-month annualized rate (for inflation)."""
    return (((s / s.shift(3)) ** 4) - 1) * 100


def ann_6m(s: pd.Series) -> pd.Series:
    """6-month annualized rate (for inflation)."""
    return (((s / s.shift(6)) ** 2) - 1) * 100


def z_score(s: pd.Series, window: int = 24) -> pd.Series:
    """Rolling z-score."""
    rolling_mean = s.rolling(window, min_periods=window // 2).mean()
    rolling_std = s.rolling(window, min_periods=window // 2).std()
    return (s - rolling_mean) / rolling_std


def ma_4wk(s: pd.Series) -> pd.Series:
    """4-week moving average."""
    return s.rolling(4).mean()


def ma_20d(s: pd.Series) -> pd.Series:
    """20-day moving average."""
    return s.rolling(20).mean()


def ma_50d(s: pd.Series) -> pd.Series:
    """50-day moving average."""
    return s.rolling(50).mean()


def ma_200d(s: pd.Series) -> pd.Series:
    """200-day moving average."""
    return s.rolling(200).mean()


# ==========================================
# TRANSFORM REGISTRY
# ==========================================

TRANSFORM_REGISTRY: Dict[str, Callable] = {
    "yoy_pct": yoy_pct,
    "yoy_diff": yoy_diff,
    "mom_pct": mom_pct,
    "mom_diff": mom_diff,
    "mom_diff_3ma": mom_diff_3ma,
    "qoq_pct": qoq_pct,
    "wow_pct": wow_pct,
    "wow_diff": wow_diff,
    "diff": diff,
    "3m_ann": ann_3m,
    "6m_ann": ann_6m,
    "z": z_score,
    "4wk_ma": ma_4wk,
    "20d_ma": ma_20d,
    "50d_ma": ma_50d,
    "200d_ma": ma_200d,
}


# ==========================================
# FREQUENCY-AWARE PERIOD MAPPING
# ==========================================

FREQ_PERIODS = {
    "D": {"yoy": 252, "mom": 21, "z_window": 504},
    "W": {"yoy": 52, "mom": 4, "z_window": 104},
    "M": {"yoy": 12, "mom": 1, "z_window": 24},
    "Q": {"yoy": 4, "mom": 1, "z_window": 8},
    "A": {"yoy": 1, "mom": 1, "z_window": 5},
}


def get_periods_for_freq(freq: str) -> Dict[str, int]:
    """Get appropriate periods for a frequency."""
    return FREQ_PERIODS.get(freq, FREQ_PERIODS["M"])


# ==========================================
# SERIES TYPE INFERENCE
# ==========================================

def infer_series_type(series_id: str, title: str) -> str:
    """
    Infer what type of series this is to determine appropriate transforms.

    Returns: 'rate', 'index', 'ratio', 'price', or 'level'
    """
    title_lower = (title or "").lower()
    sid_lower = series_id.lower()

    # Rates/Yields/Spreads - use diff not pct
    rate_keywords = [
        "rate", "yield", "spread", "oas", "premium", "curve", "dgs", "treasury",
        "mortgage", "fedfund", "sofr", "effr", "obfr", "tips", "breakeven", "libor",
        "prime", "discount", "t10y", "t5y", "dfii", "ff", "baa", "aaa"
    ]
    if any(k in title_lower or k in sid_lower for k in rate_keywords):
        return "rate"

    # Index/Sentiment/Survey - use diff and z-score
    index_keywords = [
        "index", "sentiment", "confidence", "pmi", "ism", "survey", "indicator",
        "optimism", "expectations", "nfci", "fsi", "vix", "stress"
    ]
    if any(k in title_lower or k in sid_lower for k in index_keywords):
        return "index"

    # Ratios/Percentages - use diff
    ratio_keywords = [
        "ratio", "percent", "participation", "utilization", "capacity",
        "saving rate", "delinquency", "unemployment"
    ]
    if any(k in title_lower or k in sid_lower for k in ratio_keywords):
        return "ratio"

    # Price levels - use pct change (inflation calcs)
    price_keywords = ["cpi", "pce", "price", "deflator", "ppi"]
    if any(k in title_lower or k in sid_lower for k in price_keywords):
        return "price"

    # Default to level (counts, stocks, etc.)
    return "level"


def infer_frequency(df: pd.DataFrame) -> str:
    """Infer frequency from date gaps."""
    if len(df) < 3:
        return "U"  # Unknown

    gaps = df.index.to_series().diff().dropna()
    median_gap = gaps.median().days

    if median_gap <= 2:
        return "D"
    elif median_gap <= 10:
        return "W"
    elif median_gap <= 45:
        return "M"
    elif median_gap <= 100:
        return "Q"
    else:
        return "A"


def get_default_transforms(series_type: str, freq: str) -> List[str]:
    """Get default transforms based on series type and frequency."""

    if series_type == "rate":
        return ["diff", "yoy_diff", "z"]

    elif series_type == "index":
        return ["diff", "z", "yoy_diff"]

    elif series_type == "ratio":
        return ["diff", "yoy_diff", "z"]

    elif series_type == "price":
        return ["yoy_pct", "mom_pct", "3m_ann", "6m_ann"]

    elif series_type == "level":
        if freq in ["D", "W"]:
            return ["yoy_pct", "wow_pct", "z"]
        elif freq == "M":
            return ["yoy_pct", "mom_pct", "z"]
        elif freq == "Q":
            return ["yoy_pct", "qoq_pct", "z"]
        else:
            return ["yoy_pct", "z"]

    return ["yoy_pct"]


# ==========================================
# APPLY TRANSFORMS
# ==========================================

def apply_transforms(
    s: pd.Series,
    transforms: List[str],
    freq: str = "M"
) -> pd.DataFrame:
    """
    Apply a list of transforms to a series.

    Args:
        s: Input series (values)
        transforms: List of transform names from TRANSFORM_REGISTRY
        freq: Frequency code (D, W, M, Q, A)

    Returns:
        DataFrame with raw + transformed columns
    """
    result = pd.DataFrame(index=s.index)
    result["raw"] = s

    periods = get_periods_for_freq(freq)

    for t in transforms:
        try:
            if t == "yoy_pct":
                result["yoy_pct"] = yoy_pct(s, periods["yoy"])
            elif t == "yoy_diff":
                result["yoy_diff"] = yoy_diff(s, periods["yoy"])
            elif t == "z":
                result["z"] = z_score(s, periods["z_window"])
            elif t in TRANSFORM_REGISTRY:
                result[t] = TRANSFORM_REGISTRY[t](s)
        except Exception:
            pass  # Skip failed transforms silently

    return result


def apply_transforms_df(
    df: pd.DataFrame,
    transforms: List[str],
    freq: str = "M"
) -> pd.DataFrame:
    """
    Apply transforms to a DataFrame with 'value' column.

    Args:
        df: DataFrame with 'value' column
        transforms: List of transform names
        freq: Frequency code

    Returns:
        DataFrame with raw + transformed columns
    """
    if "value" not in df.columns:
        raise ValueError("DataFrame must have 'value' column")

    return apply_transforms(df["value"], transforms, freq)
