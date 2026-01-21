"""
Regime Validation
=================
Validates regime indicators against historical events (NBER recessions, drawdowns).
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

from lighthouse_quant.config import NBER_RECESSIONS


@dataclass
class RegimeValidationResult:
    """Results from regime validation."""
    indicator_name: str
    threshold: float
    threshold_direction: str  # "above" or "below"

    # Detection metrics
    true_positive_rate: float   # % of recessions detected
    false_positive_rate: float  # % of time signaling outside recession
    average_lead_time: float    # Months before recession start
    median_lead_time: float

    # Per-recession details
    recession_details: List[Dict]

    # Overall stats
    n_recessions_tested: int
    n_recessions_detected: int
    n_false_alarms: int
    precision: float  # TP / (TP + FP)
    recall: float     # TP / (TP + FN)
    f1_score: float


def create_nber_series(index: pd.DatetimeIndex) -> pd.Series:
    """Create binary recession indicator."""
    recession = pd.Series(0, index=index, name="recession")
    for start, end in NBER_RECESSIONS:
        start_dt = pd.Timestamp(start)
        end_dt = pd.Timestamp(end)
        mask = (index >= start_dt) & (index <= end_dt)
        recession.loc[mask] = 1
    return recession


def validate_against_nber(
    indicator: pd.Series,
    threshold: float,
    threshold_direction: str = "above",
    min_signal_months: int = 2,
    max_lead_months: int = 18,
    start_date: str = "1970-01-01"
) -> RegimeValidationResult:
    """
    Validate an indicator's ability to predict NBER recessions.

    Args:
        indicator: Time series of indicator values (monthly recommended)
        threshold: Threshold for signal (e.g., MRI > 1.0)
        threshold_direction: "above" if signal when > threshold, "below" otherwise
        min_signal_months: Minimum months signal must persist to count
        max_lead_months: Maximum lead time to consider valid
        start_date: Start date for analysis

    Returns:
        RegimeValidationResult with detailed metrics
    """
    # Filter to analysis period
    indicator = indicator.loc[indicator.index >= start_date].copy()

    # Resample to monthly if needed
    if indicator.index.freq is None or indicator.index.freq.name != "M":
        indicator = indicator.resample("ME").last()

    # Create recession series
    recession = create_nber_series(indicator.index)

    # Create signal series
    if threshold_direction == "above":
        signal = (indicator > threshold).astype(int)
    else:
        signal = (indicator < threshold).astype(int)

    # Identify signal episodes (consecutive months of signal)
    signal_diff = signal.diff().fillna(0)
    signal_starts = signal_diff[signal_diff == 1].index
    signal_ends = signal_diff[signal_diff == -1].index

    # Get recession periods in our sample
    recession_periods = []
    for start, end in NBER_RECESSIONS:
        start_dt = pd.Timestamp(start)
        end_dt = pd.Timestamp(end)
        if start_dt >= indicator.index.min() and start_dt <= indicator.index.max():
            recession_periods.append((start_dt, end_dt))

    # Analyze each recession
    recession_details = []
    n_detected = 0

    for rec_start, rec_end in recession_periods:
        # Look for signal in the max_lead_months before recession
        lookback_start = rec_start - pd.DateOffset(months=max_lead_months)
        lookback_end = rec_start

        signal_window = signal.loc[lookback_start:lookback_end]

        # Find first signal occurrence
        signal_dates = signal_window[signal_window == 1].index

        if len(signal_dates) > 0:
            first_signal = signal_dates[0]
            lead_months = (rec_start - first_signal).days / 30.44

            # Check if signal persisted
            signal_duration = signal_window.sum()

            if signal_duration >= min_signal_months:
                detected = True
                n_detected += 1
            else:
                detected = False
                lead_months = np.nan
        else:
            detected = False
            first_signal = None
            lead_months = np.nan
            signal_duration = 0

        recession_details.append({
            "recession_start": rec_start,
            "recession_end": rec_end,
            "detected": detected,
            "first_signal_date": first_signal,
            "lead_months": lead_months,
            "signal_duration_months": signal_duration
        })

    # Calculate false alarms (signal episodes not within max_lead of recession)
    false_alarms = 0
    for start in signal_starts:
        is_valid_signal = False
        for rec_start, _ in recession_periods:
            if start <= rec_start and (rec_start - start).days / 30.44 <= max_lead_months:
                is_valid_signal = True
                break
            # Also count signals during recession as valid
            for rec_start, rec_end in recession_periods:
                if start >= rec_start and start <= rec_end:
                    is_valid_signal = True
                    break
        if not is_valid_signal:
            false_alarms += 1

    # Calculate metrics
    n_recessions = len(recession_periods)
    tpr = n_detected / n_recessions if n_recessions > 0 else 0

    # False positive rate: % of non-recession months with signal
    non_recession_signal = signal[recession == 0]
    fpr = non_recession_signal.mean() if len(non_recession_signal) > 0 else 0

    # Lead times for detected recessions
    lead_times = [d["lead_months"] for d in recession_details if d["detected"]]
    avg_lead = np.mean(lead_times) if lead_times else np.nan
    med_lead = np.median(lead_times) if lead_times else np.nan

    # Precision and recall
    # TP = n_detected, FP = false_alarms, FN = n_recessions - n_detected
    tp = n_detected
    fp = false_alarms
    fn = n_recessions - n_detected

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return RegimeValidationResult(
        indicator_name=indicator.name if indicator.name else "indicator",
        threshold=threshold,
        threshold_direction=threshold_direction,
        true_positive_rate=tpr,
        false_positive_rate=fpr,
        average_lead_time=avg_lead,
        median_lead_time=med_lead,
        recession_details=recession_details,
        n_recessions_tested=n_recessions,
        n_recessions_detected=n_detected,
        n_false_alarms=false_alarms,
        precision=precision,
        recall=recall,
        f1_score=f1
    )


def compute_regime_statistics(
    indicator: pd.Series,
    regimes: Dict[str, Tuple[float, float]],
    returns: Optional[pd.Series] = None,
    start_date: str = "1970-01-01"
) -> pd.DataFrame:
    """
    Compute statistics for each regime defined by indicator thresholds.

    Args:
        indicator: Regime indicator series
        regimes: Dict mapping regime name to (lower, upper) thresholds
        returns: Optional returns series to compute regime-specific returns
        start_date: Analysis start date

    Returns:
        DataFrame with statistics per regime
    """
    indicator = indicator.loc[indicator.index >= start_date].copy()

    results = []

    for regime_name, (lower, upper) in regimes.items():
        # Identify regime periods
        if lower == -np.inf:
            mask = indicator <= upper
        elif upper == np.inf:
            mask = indicator > lower
        else:
            mask = (indicator > lower) & (indicator <= upper)

        regime_data = indicator[mask]

        stats = {
            "regime": regime_name,
            "lower_threshold": lower,
            "upper_threshold": upper,
            "n_periods": len(regime_data),
            "pct_of_time": len(regime_data) / len(indicator) * 100 if len(indicator) > 0 else 0,
            "avg_value": regime_data.mean(),
            "std_value": regime_data.std(),
        }

        # Add return statistics if provided
        if returns is not None:
            aligned = pd.concat([indicator, returns], axis=1).dropna()
            aligned.columns = ["indicator", "returns"]
            regime_returns = aligned.loc[mask, "returns"]

            if len(regime_returns) > 0:
                stats["avg_return"] = regime_returns.mean()
                stats["std_return"] = regime_returns.std()
                stats["sharpe"] = (regime_returns.mean() / regime_returns.std() *
                                   np.sqrt(12)) if regime_returns.std() > 0 else np.nan
                stats["min_return"] = regime_returns.min()
                stats["max_return"] = regime_returns.max()

        results.append(stats)

    return pd.DataFrame(results)


def find_optimal_threshold(
    indicator: pd.Series,
    target_event: pd.Series,
    threshold_range: Tuple[float, float],
    n_thresholds: int = 20,
    direction: str = "above",
    optimize_for: str = "f1"
) -> Tuple[float, Dict]:
    """
    Find optimal threshold for predicting target events.

    Args:
        indicator: Indicator series
        target_event: Binary event series (1 = event)
        threshold_range: (min, max) threshold to search
        n_thresholds: Number of thresholds to test
        direction: "above" or "below"
        optimize_for: "f1", "precision", "recall", or "lead_time"

    Returns:
        Tuple of (optimal threshold, results dict)
    """
    thresholds = np.linspace(threshold_range[0], threshold_range[1], n_thresholds)

    best_threshold = None
    best_score = -np.inf if optimize_for != "lead_time" else np.inf
    all_results = []

    for threshold in thresholds:
        # Create signal
        if direction == "above":
            signal = (indicator > threshold).astype(int)
        else:
            signal = (indicator < threshold).astype(int)

        # Align with target
        df = pd.concat([signal.rename("signal"), target_event.rename("target")], axis=1).dropna()

        if len(df) < 20:
            continue

        # Compute metrics
        tp = ((df["signal"] == 1) & (df["target"] == 1)).sum()
        fp = ((df["signal"] == 1) & (df["target"] == 0)).sum()
        fn = ((df["signal"] == 0) & (df["target"] == 1)).sum()
        tn = ((df["signal"] == 0) & (df["target"] == 0)).sum()

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        result = {
            "threshold": threshold,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "tn": tn
        }
        all_results.append(result)

        # Check if this is the best
        if optimize_for == "f1":
            score = f1
        elif optimize_for == "precision":
            score = precision
        elif optimize_for == "recall":
            score = recall
        else:
            score = f1  # Default to F1

        if score > best_score:
            best_score = score
            best_threshold = threshold

    return best_threshold, {"best_score": best_score, "all_results": all_results}


# Standard regime definitions
# MRI thresholds recalibrated 2026-01-19 based on actual distribution
# Cycle-based naming convention
MRI_REGIMES = {
    "early_expansion": (-np.inf, -0.20),
    "mid_cycle": (-0.20, 0.10),
    "late_cycle": (0.10, 0.25),
    "pre_recession": (0.25, 0.50),
    "recession": (0.50, np.inf)
}

LCI_REGIMES = {
    "abundant": (1.0, np.inf),
    "ample": (0.5, 1.0),
    "tight": (-0.5, 0.5),
    "scarce": (-1.0, -0.5),
    "stress": (-np.inf, -1.0)
}

LFI_REGIMES = {
    "healthy": (-np.inf, 0.0),
    "neutral": (0.0, 0.5),
    "elevated": (0.5, 1.0),
    "high": (1.0, 1.5),
    "critical": (1.5, np.inf)
}
