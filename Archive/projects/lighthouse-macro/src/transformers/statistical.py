"""
Lighthouse Macro — Statistical Transformations
Z-scores, Percentiles, Standard Deviation Bands, Normalization
"""

from typing import Optional

import pandas as pd
import numpy as np


def zscore(series: pd.Series) -> pd.Series:
    """
    Standard z-score (full history).

    Z = (X - μ) / σ
    """
    return (series - series.mean()) / series.std()


def zscore_rolling(series: pd.Series, window: int) -> pd.Series:
    """
    Rolling z-score.

    Args:
        series: Input time series
        window: Rolling window size

    Returns:
        Rolling z-score series
    """
    rolling_mean = series.rolling(window=window).mean()
    rolling_std = series.rolling(window=window).std()
    return (series - rolling_mean) / rolling_std


def zscore_12m(series: pd.Series) -> pd.Series:
    """12-month rolling z-score"""
    return zscore_rolling(series, 12)


def zscore_24m(series: pd.Series) -> pd.Series:
    """24-month rolling z-score"""
    return zscore_rolling(series, 24)


def percentile_rank(series: pd.Series) -> pd.Series:
    """
    Percentile rank (0-100) over full history.

    Returns:
        Percentile rank series
    """
    return series.rank(pct=True) * 100


def percentile_rank_rolling(series: pd.Series, window: int) -> pd.Series:
    """
    Rolling percentile rank.

    Args:
        series: Input time series
        window: Rolling window size

    Returns:
        Rolling percentile rank series
    """
    return series.rolling(window=window).apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1] * 100)


def normalize_minmax(series: pd.Series, min_val: float = 0, max_val: float = 1) -> pd.Series:
    """
    Min-max normalization.

    Scales series to range [min_val, max_val]
    """
    series_min = series.min()
    series_max = series.max()
    return (series - series_min) / (series_max - series_min) * (max_val - min_val) + min_val


def normalize_standard(series: pd.Series) -> pd.Series:
    """
    Standard normalization (z-score).

    Transforms to mean=0, std=1
    """
    return zscore(series)


def rolling_std(series: pd.Series, window: int) -> pd.Series:
    """Rolling standard deviation"""
    return series.rolling(window=window).std()


def rolling_var(series: pd.Series, window: int) -> pd.Series:
    """Rolling variance"""
    return series.rolling(window=window).var()


def bollinger_bands(
    series: pd.Series, window: int = 20, num_std: float = 2.0
) -> pd.DataFrame:
    """
    Bollinger Bands.

    Args:
        series: Input time series
        window: Moving average window
        num_std: Number of standard deviations for bands

    Returns:
        DataFrame with columns: middle, upper, lower
    """
    middle = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()

    upper = middle + (std * num_std)
    lower = middle - (std * num_std)

    return pd.DataFrame(
        {"middle": middle, "upper": upper, "lower": lower}, index=series.index
    )


def percentile_bands(
    series: pd.Series, window: int, lower_pct: float = 25, upper_pct: float = 75
) -> pd.DataFrame:
    """
    Percentile bands.

    Args:
        series: Input time series
        window: Rolling window size
        lower_pct: Lower percentile (e.g., 25)
        upper_pct: Upper percentile (e.g., 75)

    Returns:
        DataFrame with columns: median, upper, lower
    """
    median = series.rolling(window=window).median()
    lower = series.rolling(window=window).quantile(lower_pct / 100)
    upper = series.rolling(window=window).quantile(upper_pct / 100)

    return pd.DataFrame(
        {"median": median, "upper": upper, "lower": lower}, index=series.index
    )


def expanding_mean(series: pd.Series, min_periods: int = 1) -> pd.Series:
    """Expanding mean (cumulative average)"""
    return series.expanding(min_periods=min_periods).mean()


def expanding_std(series: pd.Series, min_periods: int = 1) -> pd.Series:
    """Expanding standard deviation"""
    return series.expanding(min_periods=min_periods).std()


def outlier_filter(
    series: pd.Series, method: str = "zscore", threshold: float = 3.0
) -> pd.Series:
    """
    Filter outliers from series.

    Args:
        series: Input time series
        method: 'zscore' or 'iqr'
        threshold: Z-score threshold or IQR multiplier

    Returns:
        Series with outliers replaced by NaN
    """
    if method == "zscore":
        z = zscore(series)
        return series.where(np.abs(z) < threshold)
    elif method == "iqr":
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - threshold * iqr
        upper = q3 + threshold * iqr
        return series.where((series >= lower) & (series <= upper))
    else:
        raise ValueError(f"Unknown outlier filter method: {method}")


def winsorize(series: pd.Series, lower: float = 0.05, upper: float = 0.95) -> pd.Series:
    """
    Winsorize series (cap extreme values at percentiles).

    Args:
        series: Input time series
        lower: Lower percentile (e.g., 0.05 for 5th percentile)
        upper: Upper percentile (e.g., 0.95 for 95th percentile)

    Returns:
        Winsorized series
    """
    lower_bound = series.quantile(lower)
    upper_bound = series.quantile(upper)
    return series.clip(lower=lower_bound, upper=upper_bound)


def exponential_smoothing(series: pd.Series, alpha: float = 0.3) -> pd.Series:
    """
    Exponential smoothing.

    Args:
        series: Input time series
        alpha: Smoothing parameter (0 < alpha < 1)

    Returns:
        Smoothed series
    """
    return series.ewm(alpha=alpha, adjust=False).mean()


def rolling_correlation(
    series1: pd.Series, series2: pd.Series, window: int
) -> pd.Series:
    """
    Rolling correlation between two series.

    Args:
        series1: First time series
        series2: Second time series
        window: Rolling window size

    Returns:
        Rolling correlation series
    """
    return series1.rolling(window=window).corr(series2)


def rolling_covariance(
    series1: pd.Series, series2: pd.Series, window: int
) -> pd.Series:
    """
    Rolling covariance between two series.

    Args:
        series1: First time series
        series2: Second time series
        window: Rolling window size

    Returns:
        Rolling covariance series
    """
    return series1.rolling(window=window).cov(series2)
