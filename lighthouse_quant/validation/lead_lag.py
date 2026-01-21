"""
Lead-Lag Analysis and Granger Causality Testing
================================================
Validates whether leading indicators actually lead their target variables.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from scipy import stats
import warnings


@dataclass
class LeadLagResult:
    """Results from lead-lag analysis."""
    leading_indicator: str
    lagging_indicator: str
    optimal_lag: int  # Positive = leading actually leads
    correlation_at_optimal_lag: float
    correlation_at_zero_lag: float
    granger_pvalue: float  # At optimal lag
    granger_pvalues_by_lag: Dict[int, float]
    expected_lag: int
    expected_relationship: str  # "positive" or "negative"
    relationship_confirmed: bool
    lead_confirmed: bool
    n_observations: int


def compute_cross_correlation(
    leading: pd.Series,
    lagging: pd.Series,
    max_lag: int = 24,
    normalize: bool = True
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute cross-correlation between two series at various lags.

    Args:
        leading: Series hypothesized to lead
        lagging: Series hypothesized to lag
        max_lag: Maximum lag to test (in both directions)
        normalize: Whether to normalize to [-1, 1]

    Returns:
        Tuple of (lags, correlations)
        Positive lag means leading is shifted forward (leads lagging)
    """
    # Align series
    df = pd.concat([leading.rename("lead"), lagging.rename("lag")], axis=1).dropna()

    if len(df) < max_lag + 10:
        raise ValueError(f"Insufficient data: {len(df)} observations for {max_lag} lags")

    lead = df["lead"].values
    lag = df["lag"].values

    correlations = []
    lags = list(range(-max_lag, max_lag + 1))

    for l in lags:
        if l < 0:
            # Negative lag: leading is shifted backward (lagging leads)
            corr = np.corrcoef(lead[-l:], lag[:l])[0, 1]
        elif l > 0:
            # Positive lag: leading is shifted forward (leading leads)
            corr = np.corrcoef(lead[:-l], lag[l:])[0, 1]
        else:
            corr = np.corrcoef(lead, lag)[0, 1]
        correlations.append(corr)

    return np.array(lags), np.array(correlations)


def granger_causality_test(
    leading: pd.Series,
    lagging: pd.Series,
    max_lag: int = 12,
    significance_level: float = 0.05
) -> Dict[int, float]:
    """
    Perform Granger causality test at multiple lags.

    Tests whether past values of 'leading' help predict 'lagging'
    beyond what past values of 'lagging' alone would predict.

    Args:
        leading: Series hypothesized to Granger-cause
        lagging: Series hypothesized to be Granger-caused
        max_lag: Maximum lag to test
        significance_level: Threshold for significance

    Returns:
        Dictionary mapping lag -> p-value
    """
    try:
        from statsmodels.tsa.stattools import grangercausalitytests
    except ImportError:
        warnings.warn("statsmodels not installed, returning empty results")
        return {}

    # Align and prepare data
    df = pd.concat([lagging.rename("y"), leading.rename("x")], axis=1).dropna()

    if len(df) < max_lag * 3:
        warnings.warn(f"Insufficient data for Granger test: {len(df)} rows")
        return {}

    # Granger test expects [y, x] format where we test if x Granger-causes y
    data = df[["y", "x"]].values

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            results = grangercausalitytests(data, maxlag=max_lag, verbose=False)
        except Exception as e:
            warnings.warn(f"Granger test failed: {e}")
            return {}

    # Extract F-test p-values
    pvalues = {}
    for lag in range(1, max_lag + 1):
        if lag in results:
            # Use ssr_ftest (sum of squared residuals F-test)
            pvalues[lag] = results[lag][0]["ssr_ftest"][1]

    return pvalues


def validate_indicator_relationship(
    df: pd.DataFrame,
    leading_col: str,
    lagging_col: str,
    expected_lag: int = 6,
    expected_relationship: str = "positive",
    max_lag: int = 24
) -> LeadLagResult:
    """
    Validate a hypothesized lead-lag relationship between two indicators.

    Args:
        df: DataFrame containing both series
        leading_col: Column name of leading indicator
        lagging_col: Column name of lagging indicator
        expected_lag: Expected lead time in periods
        expected_relationship: "positive" or "negative"
        max_lag: Maximum lag to search

    Returns:
        LeadLagResult with validation metrics
    """
    # Check columns exist
    if leading_col not in df.columns:
        raise ValueError(f"Column not found: {leading_col}")
    if lagging_col not in df.columns:
        raise ValueError(f"Column not found: {lagging_col}")

    leading = df[leading_col].dropna()
    lagging = df[lagging_col].dropna()

    # Compute cross-correlation
    try:
        lags, correlations = compute_cross_correlation(leading, lagging, max_lag=max_lag)
    except ValueError as e:
        # Return empty result if insufficient data
        return LeadLagResult(
            leading_indicator=leading_col,
            lagging_indicator=lagging_col,
            optimal_lag=0,
            correlation_at_optimal_lag=np.nan,
            correlation_at_zero_lag=np.nan,
            granger_pvalue=np.nan,
            granger_pvalues_by_lag={},
            expected_lag=expected_lag,
            expected_relationship=expected_relationship,
            relationship_confirmed=False,
            lead_confirmed=False,
            n_observations=0
        )

    # Find optimal lag based on expected relationship
    if expected_relationship == "negative":
        # For negative relationship, find minimum (most negative) correlation
        optimal_idx = np.nanargmin(correlations)
    else:
        # For positive relationship, find maximum correlation
        optimal_idx = np.nanargmax(correlations)

    optimal_lag = lags[optimal_idx]
    correlation_at_optimal = correlations[optimal_idx]

    # Zero-lag correlation
    zero_idx = np.where(lags == 0)[0][0]
    correlation_at_zero = correlations[zero_idx]

    # Granger causality
    granger_pvalues = granger_causality_test(leading, lagging, max_lag=min(12, max_lag))

    # Get p-value at optimal lag (or nearest available)
    if abs(optimal_lag) in granger_pvalues:
        granger_pvalue = granger_pvalues[abs(optimal_lag)]
    elif granger_pvalues:
        granger_pvalue = min(granger_pvalues.values())
    else:
        granger_pvalue = np.nan

    # Validate relationship direction
    if expected_relationship == "negative":
        relationship_confirmed = correlation_at_optimal < -0.1
    else:
        relationship_confirmed = correlation_at_optimal > 0.1

    # Validate lead (optimal lag should be in the direction of expected lag)
    # Positive expected_lag means leading should lead lagging
    if expected_lag > 0:
        lead_confirmed = optimal_lag > 0 and abs(optimal_lag - expected_lag) <= expected_lag
    elif expected_lag < 0:
        lead_confirmed = optimal_lag < 0 and abs(optimal_lag - expected_lag) <= abs(expected_lag)
    else:
        lead_confirmed = abs(optimal_lag) <= 2

    # Count valid observations
    combined = pd.concat([leading, lagging], axis=1).dropna()
    n_obs = len(combined)

    return LeadLagResult(
        leading_indicator=leading_col,
        lagging_indicator=lagging_col,
        optimal_lag=int(optimal_lag),
        correlation_at_optimal_lag=float(correlation_at_optimal),
        correlation_at_zero_lag=float(correlation_at_zero),
        granger_pvalue=float(granger_pvalue) if not np.isnan(granger_pvalue) else np.nan,
        granger_pvalues_by_lag=granger_pvalues,
        expected_lag=expected_lag,
        expected_relationship=expected_relationship,
        relationship_confirmed=relationship_confirmed,
        lead_confirmed=lead_confirmed,
        n_observations=n_obs
    )


def validate_all_relationships(
    df: pd.DataFrame,
    relationships: List[Tuple[str, str, int, str]],
    max_lag: int = 24
) -> pd.DataFrame:
    """
    Validate multiple indicator relationships.

    Args:
        df: DataFrame containing all series
        relationships: List of (leading, lagging, expected_lag, relationship) tuples
        max_lag: Maximum lag to search

    Returns:
        DataFrame with validation results for each relationship
    """
    results = []

    for leading, lagging, exp_lag, exp_rel in relationships:
        try:
            result = validate_indicator_relationship(
                df, leading, lagging,
                expected_lag=exp_lag,
                expected_relationship=exp_rel,
                max_lag=max_lag
            )
            results.append({
                "leading": result.leading_indicator,
                "lagging": result.lagging_indicator,
                "expected_lag": result.expected_lag,
                "optimal_lag": result.optimal_lag,
                "lag_diff": abs(result.optimal_lag - result.expected_lag),
                "expected_relationship": result.expected_relationship,
                "correlation": result.correlation_at_optimal_lag,
                "corr_at_zero": result.correlation_at_zero_lag,
                "granger_pvalue": result.granger_pvalue,
                "relationship_ok": result.relationship_confirmed,
                "lead_ok": result.lead_confirmed,
                "n_obs": result.n_observations,
                "valid": result.relationship_confirmed and result.lead_confirmed
            })
        except Exception as e:
            results.append({
                "leading": leading,
                "lagging": lagging,
                "expected_lag": exp_lag,
                "optimal_lag": np.nan,
                "lag_diff": np.nan,
                "expected_relationship": exp_rel,
                "correlation": np.nan,
                "corr_at_zero": np.nan,
                "granger_pvalue": np.nan,
                "relationship_ok": False,
                "lead_ok": False,
                "n_obs": 0,
                "valid": False,
                "error": str(e)
            })

    return pd.DataFrame(results)


def compute_information_coefficient(
    signal: pd.Series,
    forward_returns: pd.Series,
    periods: List[int] = [1, 3, 6, 12]
) -> Dict[int, float]:
    """
    Compute Information Coefficient (IC) of signal vs forward returns.

    IC is the correlation between signal value and subsequent returns.

    Args:
        signal: Signal/indicator series
        forward_returns: Returns series (same frequency as signal)
        periods: Forward periods to compute IC for

    Returns:
        Dictionary mapping period -> IC
    """
    results = {}

    for period in periods:
        # Shift returns back to align with signal
        fwd = forward_returns.shift(-period)
        combined = pd.concat([signal, fwd], axis=1).dropna()

        if len(combined) > 20:
            ic = combined.iloc[:, 0].corr(combined.iloc[:, 1])
            results[period] = ic
        else:
            results[period] = np.nan

    return results
