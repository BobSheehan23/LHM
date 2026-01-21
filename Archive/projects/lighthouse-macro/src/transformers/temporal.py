"""
Lighthouse Macro — Temporal Transformations
YoY, MoM, QoQ, Moving Averages, Rolling Windows
"""

from typing import Optional

import pandas as pd


def yoy(series: pd.Series, periods: int = 12) -> pd.Series:
    """
    Year-over-year change.

    Args:
        series: Input time series
        periods: Number of periods in a year (12 for monthly, 4 for quarterly)

    Returns:
        YoY change series
    """
    return series.diff(periods)


def yoy_pct(series: pd.Series, periods: int = 12) -> pd.Series:
    """
    Year-over-year percentage change.

    Args:
        series: Input time series
        periods: Number of periods in a year

    Returns:
        YoY % change series
    """
    return series.pct_change(periods) * 100


def mom(series: pd.Series) -> pd.Series:
    """Month-over-month change"""
    return series.diff(1)


def mom_pct(series: pd.Series) -> pd.Series:
    """Month-over-month percentage change"""
    return series.pct_change(1) * 100


def qoq(series: pd.Series) -> pd.Series:
    """Quarter-over-quarter change"""
    return series.diff(3)


def qoq_pct(series: pd.Series) -> pd.Series:
    """Quarter-over-quarter percentage change"""
    return series.pct_change(3) * 100


def qoq_annualized(series: pd.Series) -> pd.Series:
    """Quarter-over-quarter annualized percentage change"""
    return ((1 + series.pct_change(3)) ** 4 - 1) * 100


def moving_average(series: pd.Series, window: int) -> pd.Series:
    """
    Simple moving average.

    Args:
        series: Input time series
        window: Window size (e.g., 3, 6, 12, 24 months)

    Returns:
        Moving average series
    """
    return series.rolling(window=window).mean()


def ma_3m(series: pd.Series) -> pd.Series:
    """3-month moving average"""
    return moving_average(series, 3)


def ma_6m(series: pd.Series) -> pd.Series:
    """6-month moving average"""
    return moving_average(series, 6)


def ma_12m(series: pd.Series) -> pd.Series:
    """12-month moving average"""
    return moving_average(series, 12)


def ma_24m(series: pd.Series) -> pd.Series:
    """24-month moving average"""
    return moving_average(series, 24)


def rolling_mean(series: pd.Series, window: int) -> pd.Series:
    """Rolling mean (alias for moving_average)"""
    return moving_average(series, window)


def rolling_sum(series: pd.Series, window: int) -> pd.Series:
    """Rolling sum"""
    return series.rolling(window=window).sum()


def cumulative_sum(series: pd.Series) -> pd.Series:
    """Cumulative sum"""
    return series.cumsum()


def first_difference(series: pd.Series) -> pd.Series:
    """First difference"""
    return series.diff(1)


def log_difference(series: pd.Series) -> pd.Series:
    """Log difference (approximately equal to % change for small changes)"""
    import numpy as np

    return np.log(series).diff(1)


def growth_rate(series: pd.Series, periods: int = 1) -> pd.Series:
    """
    Growth rate over specified periods.

    Args:
        series: Input time series
        periods: Number of periods

    Returns:
        Growth rate series
    """
    return (series / series.shift(periods) - 1) * 100


def index_to_base(series: pd.Series, base_date: Optional[str] = None, base_value: float = 100) -> pd.Series:
    """
    Index series to a base value at a specific date.

    Args:
        series: Input time series
        base_date: Date to use as base (if None, uses first date)
        base_value: Value at base date (default 100)

    Returns:
        Indexed series
    """
    if base_date is None:
        base = series.iloc[0]
    else:
        base = series.loc[base_date]

    return (series / base) * base_value


def detrend(series: pd.Series, method: str = "linear") -> pd.Series:
    """
    Remove trend from series.

    Args:
        series: Input time series
        method: 'linear' or 'hp' (Hodrick-Prescott filter)

    Returns:
        Detrended series
    """
    if method == "linear":
        from scipy import signal

        return pd.Series(signal.detrend(series.values), index=series.index, name=series.name)
    elif method == "hp":
        # HP filter implementation would go here
        # For now, return series minus its moving average
        return series - series.rolling(window=24, center=True).mean()
    else:
        raise ValueError(f"Unknown detrend method: {method}")


def seasonal_difference(series: pd.Series, periods: int = 12) -> pd.Series:
    """
    Seasonal differencing (subtract value from same period last year).

    Args:
        series: Input time series
        periods: Seasonal period (12 for monthly, 4 for quarterly)

    Returns:
        Seasonally differenced series
    """
    return series.diff(periods)
