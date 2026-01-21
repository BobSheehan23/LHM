"""
Lighthouse Macro — Structural Transformations
Ratios, Relatives, Inversions, Spreads
"""

from typing import Union

import pandas as pd
import numpy as np


def ratio(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """
    Calculate ratio of two series.

    Args:
        numerator: Numerator series
        denominator: Denominator series

    Returns:
        Ratio series
    """
    return numerator / denominator


def relative_strength(series: pd.Series, benchmark: pd.Series) -> pd.Series:
    """
    Relative strength: series / benchmark.

    Args:
        series: Series to compare
        benchmark: Benchmark series

    Returns:
        Relative strength series
    """
    return series / benchmark


def spread(series1: pd.Series, series2: pd.Series) -> pd.Series:
    """
    Spread (difference) between two series.

    Args:
        series1: First series
        series2: Second series

    Returns:
        Spread series (series1 - series2)
    """
    return series1 - series2


def yield_spread(long_rate: pd.Series, short_rate: pd.Series) -> pd.Series:
    """
    Yield spread (typically long - short).

    Args:
        long_rate: Long-term rate
        short_rate: Short-term rate

    Returns:
        Yield spread series
    """
    return long_rate - short_rate


def invert(series: pd.Series) -> pd.Series:
    """
    Invert series (1 / series).

    Useful for inverting ratios or creating reciprocals.
    """
    return 1 / series


def negate(series: pd.Series) -> pd.Series:
    """
    Negate series (-1 * series).

    Useful for flipping signs when plotting.
    """
    return -1 * series


def basis_points_to_percent(series: pd.Series) -> pd.Series:
    """Convert basis points to percentage"""
    return series / 100


def percent_to_basis_points(series: pd.Series) -> pd.Series:
    """Convert percentage to basis points"""
    return series * 100


def log_ratio(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """
    Log ratio: ln(numerator / denominator).

    Useful for symmetric percentage differences.
    """
    return np.log(numerator / denominator)


def real_rate(nominal_rate: pd.Series, inflation: pd.Series) -> pd.Series:
    """
    Real interest rate (Fisher equation approximation).

    Real rate ≈ Nominal rate - Inflation
    """
    return nominal_rate - inflation


def output_gap(actual_gdp: pd.Series, potential_gdp: pd.Series) -> pd.Series:
    """
    Output gap: (Actual - Potential) / Potential * 100.

    Returns percentage gap.
    """
    return ((actual_gdp - potential_gdp) / potential_gdp) * 100


def cyclical_component(series: pd.Series, trend: pd.Series) -> pd.Series:
    """
    Cyclical component: series - trend.

    Args:
        series: Original series
        trend: Trend component (e.g., from HP filter or moving average)

    Returns:
        Cyclical component
    """
    return series - trend


def contribution(part: pd.Series, whole: pd.Series) -> pd.Series:
    """
    Calculate contribution of a part to the whole (as percentage).

    Args:
        part: Component series
        whole: Total series

    Returns:
        Contribution series (percentage)
    """
    return (part / whole) * 100


def index_relative(series: pd.Series, base_series: pd.Series, base_value: float = 100) -> pd.Series:
    """
    Index series relative to another series.

    Args:
        series: Series to index
        base_series: Base series
        base_value: Index base value (default 100)

    Returns:
        Indexed series
    """
    return (series / base_series) * base_value


def pct_of_total(series: pd.Series, total: pd.Series) -> pd.Series:
    """
    Express series as percentage of total.

    Args:
        series: Component series
        total: Total series

    Returns:
        Percentage series
    """
    return (series / total) * 100


def deviation_from_mean(series: pd.Series) -> pd.Series:
    """
    Deviation from historical mean.

    Returns:
        Series - mean(series)
    """
    return series - series.mean()


def deviation_from_trend(series: pd.Series, window: int = 24) -> pd.Series:
    """
    Deviation from moving average trend.

    Args:
        series: Input series
        window: Moving average window

    Returns:
        Deviation from trend
    """
    trend = series.rolling(window=window).mean()
    return series - trend


def yield_curve_slope(long_rate: pd.Series, short_rate: pd.Series) -> pd.Series:
    """
    Yield curve slope (long - short).

    Alias for yield_spread, but more explicit naming.
    """
    return yield_spread(long_rate, short_rate)


def is_inverted(long_rate: pd.Series, short_rate: pd.Series) -> pd.Series:
    """
    Check if yield curve is inverted.

    Returns:
        Boolean series (True when long < short)
    """
    return long_rate < short_rate


def cross_sectional_rank(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cross-sectional rank across columns.

    Args:
        df: DataFrame with multiple series

    Returns:
        DataFrame with ranks (1 = lowest, N = highest)
    """
    return df.rank(axis=1)


def cross_sectional_zscore(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cross-sectional z-score across columns.

    Args:
        df: DataFrame with multiple series

    Returns:
        DataFrame with cross-sectional z-scores
    """
    return df.sub(df.mean(axis=1), axis=0).div(df.std(axis=1), axis=0)


def momentum(series: pd.Series, periods: int = 12) -> pd.Series:
    """
    Price momentum: current value / value N periods ago.

    Args:
        series: Input series
        periods: Lookback periods

    Returns:
        Momentum series
    """
    return series / series.shift(periods)


def momentum_diff(series: pd.Series, periods: int = 12) -> pd.Series:
    """
    Momentum as difference: current - N periods ago.

    Args:
        series: Input series
        periods: Lookback periods

    Returns:
        Momentum difference
    """
    return series - series.shift(periods)
