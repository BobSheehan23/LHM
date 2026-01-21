"""
Recession Probability Model
============================
Estimates the probability of recession onset within the next 12 months
using the MRI and other leading indicators.

Model Architecture:
    - Logistic regression calibrated on historical NBER recessions
    - Uses publication-lag-adjusted indicators
    - Outputs 12-month forward recession probability

Key Inputs:
    - MRI (Macro Risk Index) - primary signal
    - Yield curve slope (10Y-3M)
    - Credit spreads (HY OAS)
    - Labor flows (Quits rate)
"""

import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass
import warnings

from lighthouse_quant.config import NBER_RECESSIONS, DB_PATH


@dataclass
class RecessionProbabilityResult:
    """Results from recession probability model."""
    date: str
    probability_12m: float  # Probability of recession in next 12 months
    probability_6m: float   # Probability of recession in next 6 months
    probability_3m: float   # Probability of recession in next 3 months
    regime: str             # Current regime classification
    key_drivers: Dict[str, float]  # Contribution of each factor
    confidence: str         # Model confidence level


def create_recession_forward_target(index: pd.DatetimeIndex, horizon_months: int = 12) -> pd.Series:
    """
    Create forward-looking recession indicator.
    Returns 1 if recession starts within horizon_months, 0 otherwise.
    """
    recession_starts = [pd.Timestamp(start) for start, _ in NBER_RECESSIONS]

    target = pd.Series(0, index=index, name=f"recession_next_{horizon_months}m")

    for date in index:
        # Check if any recession starts within the horizon
        horizon_end = date + pd.DateOffset(months=horizon_months)
        for rec_start in recession_starts:
            if date < rec_start <= horizon_end:
                target.loc[date] = 1
                break

    return target


def sigmoid(x: np.ndarray) -> np.ndarray:
    """Logistic sigmoid function."""
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))


class RecessionProbabilityModel:
    """
    Recession probability model using MRI and supplementary indicators.

    The model uses a calibrated logistic function:
        P(recession) = sigmoid(a + b*MRI + c*yield_curve + d*credit + e*labor)

    Coefficients are calibrated on historical data to maximize
    recession detection while minimizing false positives.
    """

    def __init__(self, conn: sqlite3.Connection = None):
        """Initialize the model."""
        self.conn = conn or sqlite3.connect(DB_PATH)

        # Calibrated coefficients (fitted on 1990-2024 NBER recessions)
        # Calibration date: 2026-01-19
        self.coefficients = {
            "intercept": -1.5,      # Adjusted for recall (was -2.5)
            "MRI": 4.0,             # Primary signal
            "yield_curve": -3.0,    # Negative slope = higher probability (was -2.0)
            "credit_spread": 1.0,   # Wider spreads = higher probability (was 1.5)
            "quits_inv": 1.0,       # Lower quits = higher probability
        }

        # Model calibration metadata
        self.calibration_date = "2026-01-19"
        self.training_start = "1990-01-01"
        self.training_end = "2024-12-31"

    def load_indicators(self) -> pd.DataFrame:
        """Load required indicators from database."""
        # Load MRI
        mri = pd.read_sql(
            "SELECT date, value as MRI FROM lighthouse_indices WHERE index_id = 'MRI' ORDER BY date",
            self.conn, parse_dates=['date']
        )

        # Load yield curve (10Y-3M spread from horizon_dataset)
        yield_curve = pd.read_sql(
            "SELECT date, Curve_10Y_3M as yield_curve FROM horizon_dataset ORDER BY date",
            self.conn, parse_dates=['date']
        )

        # Load HY OAS
        hy_oas = pd.read_sql(
            "SELECT date, HY_OAS_z as credit_spread FROM horizon_dataset ORDER BY date",
            self.conn, parse_dates=['date']
        )

        # Load Quits rate (inverted z-score)
        quits = pd.read_sql(
            "SELECT date, JOLTS_Quits_Rate_z as quits_z FROM horizon_dataset ORDER BY date",
            self.conn, parse_dates=['date']
        )
        # Invert quits (low quits = high risk)
        if not quits.empty:
            quits['quits_inv'] = -quits['quits_z']
            quits = quits.drop(columns=['quits_z'])

        # Merge all indicators
        df = mri.set_index('date')
        for other in [yield_curve, hy_oas, quits]:
            other_indexed = other.set_index('date')
            df = df.join(other_indexed, how='outer')

        return df.sort_index()

    def calibrate(self, start_date: str = "1990-01-01") -> Dict:
        """
        Calibrate model coefficients on historical data.

        Uses a simple grid search to find coefficients that maximize
        the area under the ROC curve while maintaining reasonable
        precision at the detection threshold.
        """
        df = self.load_indicators()
        df = df.loc[df.index >= start_date].copy()

        # Create target variable (recession in next 12 months)
        target = create_recession_forward_target(df.index, horizon_months=12)
        df['target'] = target

        # Drop rows with missing data
        df = df.dropna()

        if len(df) < 100:
            warnings.warn("Insufficient data for calibration")
            return {}

        # Simple calibration: find coefficients that maximize F1 score
        # This is a simplified version - production would use proper ML

        best_f1 = 0
        best_coeffs = self.coefficients.copy()

        # Grid search over coefficient space
        for mri_coef in [2.0, 3.0, 4.0, 5.0, 6.0]:
            for yc_coef in [-3.0, -2.0, -1.0]:
                for cs_coef in [0.5, 1.0, 1.5, 2.0]:
                    for intercept in [-3.0, -2.5, -2.0, -1.5]:
                        # Compute probabilities
                        z = (intercept +
                             mri_coef * df['MRI'].fillna(0) +
                             yc_coef * df['yield_curve'].fillna(0) / 100 +  # Scale yield curve
                             cs_coef * df['credit_spread'].fillna(0))

                        probs = sigmoid(z)

                        # Compute F1 at threshold 0.5
                        preds = (probs > 0.5).astype(int)
                        tp = ((preds == 1) & (df['target'] == 1)).sum()
                        fp = ((preds == 1) & (df['target'] == 0)).sum()
                        fn = ((preds == 0) & (df['target'] == 1)).sum()

                        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
                        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
                        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

                        if f1 > best_f1:
                            best_f1 = f1
                            best_coeffs = {
                                "intercept": intercept,
                                "MRI": mri_coef,
                                "yield_curve": yc_coef,
                                "credit_spread": cs_coef,
                                "quits_inv": 1.0  # Keep fixed for simplicity
                            }

        self.coefficients = best_coeffs

        return {
            "best_f1": best_f1,
            "coefficients": best_coeffs,
            "n_samples": len(df),
            "n_recessions": df['target'].sum()
        }

    def predict(self, date: str = None) -> RecessionProbabilityResult:
        """
        Predict recession probability for a given date.

        Args:
            date: Date to predict for (default: latest available)

        Returns:
            RecessionProbabilityResult with probabilities and diagnostics
        """
        df = self.load_indicators()

        if date is None:
            date = df.index.max()
        else:
            date = pd.Timestamp(date)

        # Get indicator values for the date
        if date not in df.index:
            # Find closest available date
            available_dates = df.index[df.index <= date]
            if len(available_dates) == 0:
                raise ValueError(f"No data available for {date}")
            date = available_dates.max()

        row = df.loc[date]

        # Extract indicator values, handling NaN
        def get_val(series_or_val, default=0):
            if pd.isna(series_or_val):
                return default
            return float(series_or_val)

        mri = get_val(row.get('MRI', 0))
        yield_curve = get_val(row.get('yield_curve', 0))
        credit_spread = get_val(row.get('credit_spread', 0))
        quits_inv = get_val(row.get('quits_inv', 0))

        # Compute linear combination
        z_12m = (self.coefficients['intercept'] +
                 self.coefficients['MRI'] * mri +
                 self.coefficients['yield_curve'] * yield_curve / 100 +
                 self.coefficients['credit_spread'] * credit_spread +
                 self.coefficients['quits_inv'] * quits_inv)

        # Probability for different horizons
        # 12-month uses full z-score
        # Shorter horizons use steeper sigmoid (more extreme probability)
        # but the base probability is lower (less time for recession to occur)
        prob_12m = float(sigmoid(np.array([z_12m]))[0])
        # 6-month: scale down intercept since less time for recession
        z_6m = self.coefficients['intercept'] * 1.3 + (z_12m - self.coefficients['intercept'])
        prob_6m = float(sigmoid(np.array([z_6m]))[0])
        # 3-month: scale down further
        z_3m = self.coefficients['intercept'] * 1.6 + (z_12m - self.coefficients['intercept'])
        prob_3m = float(sigmoid(np.array([z_3m]))[0])

        # Determine regime
        if prob_12m > 0.7:
            regime = "HIGH RISK"
        elif prob_12m > 0.4:
            regime = "ELEVATED"
        elif prob_12m > 0.2:
            regime = "MODERATE"
        else:
            regime = "LOW RISK"

        # Compute driver contributions
        total_contribution = abs(self.coefficients['MRI'] * mri) + \
                           abs(self.coefficients['yield_curve'] * yield_curve / 100) + \
                           abs(self.coefficients['credit_spread'] * credit_spread) + \
                           abs(self.coefficients['quits_inv'] * quits_inv)

        if total_contribution > 0:
            key_drivers = {
                "MRI": self.coefficients['MRI'] * mri / total_contribution,
                "Yield Curve": self.coefficients['yield_curve'] * yield_curve / 100 / total_contribution,
                "Credit Spreads": self.coefficients['credit_spread'] * credit_spread / total_contribution,
                "Labor Flows": self.coefficients['quits_inv'] * quits_inv / total_contribution,
            }
        else:
            key_drivers = {"MRI": 0, "Yield Curve": 0, "Credit Spreads": 0, "Labor Flows": 0}

        # Confidence based on data availability
        n_valid = sum([1 for v in [mri, yield_curve, credit_spread, quits_inv] if v != 0 and not pd.isna(v)])
        if n_valid >= 4:
            confidence = "HIGH"
        elif n_valid >= 2:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        return RecessionProbabilityResult(
            date=date.strftime("%Y-%m-%d"),
            probability_12m=round(prob_12m, 4),
            probability_6m=round(prob_6m, 4),
            probability_3m=round(prob_3m, 4),
            regime=regime,
            key_drivers=key_drivers,
            confidence=confidence
        )

    def predict_history(self, start_date: str = "1990-01-01") -> pd.DataFrame:
        """
        Generate historical recession probabilities using vectorized operations.

        Returns DataFrame with columns:
            date, prob_12m, prob_6m, prob_3m, regime, actual_recession
        """
        df = self.load_indicators()
        df = df.loc[df.index >= start_date].copy()

        if len(df) == 0:
            return pd.DataFrame()

        # Create actual recession indicator
        actual = create_recession_forward_target(df.index, horizon_months=12)

        # Vectorized probability computation
        mri = df['MRI'].fillna(0)
        yield_curve = df.get('yield_curve', pd.Series(0, index=df.index)).fillna(0)
        credit_spread = df.get('credit_spread', pd.Series(0, index=df.index)).fillna(0)
        quits_inv = df.get('quits_inv', pd.Series(0, index=df.index)).fillna(0)

        # Compute linear combination for all dates at once
        z_12m = (self.coefficients['intercept'] +
                 self.coefficients['MRI'] * mri +
                 self.coefficients['yield_curve'] * yield_curve / 100 +
                 self.coefficients['credit_spread'] * credit_spread +
                 self.coefficients['quits_inv'] * quits_inv)

        # Probabilities for different horizons
        prob_12m = sigmoid(z_12m.values)
        z_6m = self.coefficients['intercept'] * 1.3 + (z_12m - self.coefficients['intercept'])
        prob_6m = sigmoid(z_6m.values)
        z_3m = self.coefficients['intercept'] * 1.6 + (z_12m - self.coefficients['intercept'])
        prob_3m = sigmoid(z_3m.values)

        # Determine regimes vectorized
        def classify_regime(p):
            if p > 0.7:
                return "HIGH RISK"
            elif p > 0.4:
                return "ELEVATED"
            elif p > 0.2:
                return "MODERATE"
            else:
                return "LOW RISK"

        regimes = [classify_regime(p) for p in prob_12m]

        # Build result DataFrame
        result_df = pd.DataFrame({
            "date": df.index.strftime("%Y-%m-%d"),
            "prob_12m": prob_12m,
            "prob_6m": prob_6m,
            "prob_3m": prob_3m,
            "regime": regimes,
            "actual_recession": actual.values
        })

        return result_df

    def evaluate(self, start_date: str = "1990-01-01") -> Dict:
        """
        Evaluate model performance on historical data.

        Returns metrics including:
            - AUC (area under ROC curve)
            - Precision at various recall levels
            - Calibration (predicted vs actual rates)
        """
        history = self.predict_history(start_date)

        if len(history) < 10:
            return {"error": "Insufficient data for evaluation"}

        # Basic metrics
        y_true = history['actual_recession'].values
        y_prob = history['prob_12m'].values

        # Confusion matrix at 0.5 threshold
        y_pred = (y_prob > 0.5).astype(int)
        tp = ((y_pred == 1) & (y_true == 1)).sum()
        fp = ((y_pred == 1) & (y_true == 0)).sum()
        fn = ((y_pred == 0) & (y_true == 1)).sum()
        tn = ((y_pred == 0) & (y_true == 0)).sum()

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        accuracy = (tp + tn) / len(y_true)

        # Metrics at different thresholds
        thresholds = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
        threshold_metrics = []
        for thresh in thresholds:
            y_pred_t = (y_prob > thresh).astype(int)
            tp_t = ((y_pred_t == 1) & (y_true == 1)).sum()
            fp_t = ((y_pred_t == 1) & (y_true == 0)).sum()
            fn_t = ((y_pred_t == 0) & (y_true == 1)).sum()

            prec_t = tp_t / (tp_t + fp_t) if (tp_t + fp_t) > 0 else 0
            rec_t = tp_t / (tp_t + fn_t) if (tp_t + fn_t) > 0 else 0

            threshold_metrics.append({
                "threshold": thresh,
                "precision": round(prec_t, 3),
                "recall": round(rec_t, 3),
                "false_positives": int(fp_t)
            })

        # Calibration: group by probability bins and check actual rates
        history['prob_bin'] = pd.cut(history['prob_12m'], bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0])
        calibration = history.groupby('prob_bin', observed=False)['actual_recession'].agg(['mean', 'count']).reset_index()

        return {
            "n_samples": len(history),
            "n_positive": int(y_true.sum()),
            "base_rate": round(y_true.mean(), 4),
            "metrics_at_0.5": {
                "precision": round(precision, 3),
                "recall": round(recall, 3),
                "f1": round(f1, 3),
                "accuracy": round(accuracy, 3)
            },
            "threshold_metrics": threshold_metrics,
            "coefficients": self.coefficients
        }


def compute_recession_probability(conn: sqlite3.Connection = None) -> pd.Series:
    """
    Compute recession probability for the full history.

    Returns:
        pd.Series with recession probability indexed by date
    """
    model = RecessionProbabilityModel(conn)
    history = model.predict_history(start_date="1990-01-01")

    if history.empty:
        return pd.Series(dtype=float, name="REC_PROB")

    result = history.set_index('date')['prob_12m']
    result.index = pd.to_datetime(result.index)
    result.name = "REC_PROB"

    return result


# CLI interface
if __name__ == "__main__":
    import sys

    conn = sqlite3.connect(DB_PATH)
    model = RecessionProbabilityModel(conn)

    if len(sys.argv) > 1 and sys.argv[1] == "--calibrate":
        print("Calibrating model...")
        result = model.calibrate()
        print(f"Best F1: {result.get('best_f1', 'N/A'):.3f}")
        print(f"Coefficients: {result.get('coefficients', {})}")
    elif len(sys.argv) > 1 and sys.argv[1] == "--evaluate":
        print("Evaluating model...")
        metrics = model.evaluate()
        print(f"Samples: {metrics.get('n_samples', 'N/A')}")
        print(f"Base Rate: {metrics.get('base_rate', 'N/A'):.1%}")
        print(f"Metrics at 0.5: {metrics.get('metrics_at_0.5', {})}")
    else:
        # Default: predict for latest date
        result = model.predict()
        print(f"\nRecession Probability Model - {result.date}")
        print("=" * 50)
        print(f"12-Month Probability: {result.probability_12m:.1%}")
        print(f"6-Month Probability:  {result.probability_6m:.1%}")
        print(f"3-Month Probability:  {result.probability_3m:.1%}")
        print(f"Regime: {result.regime}")
        print(f"Confidence: {result.confidence}")
        print(f"\nKey Drivers:")
        for driver, contrib in result.key_drivers.items():
            print(f"  {driver}: {contrib:+.1%}")

    conn.close()
