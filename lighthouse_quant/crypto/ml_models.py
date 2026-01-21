"""
LIGHTHOUSE MACRO - CRYPTO ML & TIME SERIES MODELS
==================================================
Quantitative models for systematic crypto analysis.

Models Implemented:
    1. Momentum Model - Trend detection using moving averages and rate of change
    2. Mean Reversion Model - Z-score based reversion signals
    3. Protocol Health Classifier - Logistic regression for health prediction
    4. Regime Transition Model - Markov-inspired regime probability
    5. Sector Rotation Model - Cross-sector momentum and correlation

Philosophy:
    - Time series models capture "flows" (rate of change, momentum)
    - ML models capture "patterns" (multivariate relationships)
    - Ensemble approach combines both for robust signals
    - All models designed for interpretability (no black boxes)

Usage:
    from lighthouse_quant.crypto.ml_models import CryptoMLEngine

    engine = CryptoMLEngine(conn)
    signals = engine.generate_signals()
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import warnings
warnings.filterwarnings('ignore')


# ==========================================
# DATA STRUCTURES
# ==========================================

class MomentumSignal(Enum):
    """Momentum classification"""
    STRONG_BULLISH = "STRONG_BULLISH"
    BULLISH = "BULLISH"
    NEUTRAL = "NEUTRAL"
    BEARISH = "BEARISH"
    STRONG_BEARISH = "STRONG_BEARISH"


class ReversionSignal(Enum):
    """Mean reversion classification"""
    OVERSOLD = "OVERSOLD"           # Buy signal
    SLIGHTLY_OVERSOLD = "SLIGHTLY_OVERSOLD"
    FAIR_VALUE = "FAIR_VALUE"
    SLIGHTLY_OVERBOUGHT = "SLIGHTLY_OVERBOUGHT"
    OVERBOUGHT = "OVERBOUGHT"       # Sell signal


@dataclass
class ProtocolTimeSeries:
    """Time series analysis for a protocol"""
    project_id: str

    # Momentum metrics
    revenue_momentum: float         # 30d rate of change
    dau_momentum: float
    tvl_momentum: float
    fee_momentum: float
    momentum_signal: MomentumSignal
    momentum_score: int             # 0-100

    # Reversion metrics
    revenue_zscore: float
    dau_zscore: float
    valuation_zscore: float
    reversion_signal: ReversionSignal
    reversion_score: int            # 0-100

    # Trend metrics
    revenue_trend: str              # ACCELERATING / STABLE / DECELERATING
    dau_trend: str
    overall_trend_score: int        # 0-100


@dataclass
class ProtocolHealthPrediction:
    """ML prediction for protocol health"""
    project_id: str

    # Prediction outputs
    health_probability: float       # P(healthy in 6 months)
    survival_probability: float     # P(still active in 12 months)
    tier_probability: Dict[str, float]  # P(Tier1), P(Tier2), P(Avoid)

    # Feature importance
    key_drivers: List[Tuple[str, float]]  # (feature, contribution)

    # Confidence
    confidence: str                 # HIGH / MEDIUM / LOW
    uncertainty: float              # Model uncertainty estimate


@dataclass
class SectorRotationSignal:
    """Sector rotation recommendation"""
    sector: str
    momentum_score: float           # Relative momentum vs universe
    relative_strength: float        # Vs BTC/ETH benchmark
    quality_score: float            # Fundamental quality
    rotation_signal: str            # OVERWEIGHT / NEUTRAL / UNDERWEIGHT
    recommended_weight: float       # 0-100% of crypto allocation


@dataclass
class CryptoMLSignals:
    """Complete ML signal output"""
    date: str

    # Protocol-level signals
    protocol_timeseries: Dict[str, ProtocolTimeSeries]
    protocol_predictions: Dict[str, ProtocolHealthPrediction]

    # Sector signals
    sector_rotation: Dict[str, SectorRotationSignal]

    # Aggregate signals
    universe_momentum: MomentumSignal
    universe_reversion: ReversionSignal
    regime_transition_prob: Dict[str, float]  # Regime -> probability

    # Ensemble score
    ml_conviction_score: int        # 0-100 overall ML confidence


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def compute_zscore_static(values: np.ndarray) -> float:
    """Compute z-score for latest value in array"""
    if len(values) < 10:
        return 0.0
    mean = np.nanmean(values[:-1])
    std = np.nanstd(values[:-1])
    if std == 0 or np.isnan(std):
        return 0.0
    return (values[-1] - mean) / std


def compute_momentum(values: np.ndarray, periods: int = 30) -> float:
    """Compute rate of change momentum"""
    if len(values) < periods + 1:
        return 0.0
    current = values[-1]
    past = values[-(periods+1)]
    if past == 0 or np.isnan(past) or np.isnan(current):
        return 0.0
    return (current - past) / abs(past)


def compute_trend_acceleration(values: np.ndarray, short: int = 7, long: int = 30) -> str:
    """Detect if trend is accelerating or decelerating"""
    if len(values) < long + 1:
        return "STABLE"

    short_mom = compute_momentum(values, short)
    long_mom = compute_momentum(values, long)

    if short_mom > long_mom + 0.05:
        return "ACCELERATING"
    elif short_mom < long_mom - 0.05:
        return "DECELERATING"
    return "STABLE"


def sigmoid(x: float) -> float:
    """Sigmoid function for probability conversion"""
    return 1 / (1 + np.exp(-x))


# ==========================================
# MOMENTUM MODEL
# ==========================================

class MomentumModel:
    """
    Momentum-based trend detection model.

    Uses multiple timeframe momentum (7d, 30d, 90d) to classify trend strength.
    Momentum = Rate of Change = (Current - Past) / Past
    """

    def __init__(self):
        self.weights = {
            'revenue': 0.35,
            'dau': 0.25,
            'tvl': 0.20,
            'fees': 0.20
        }

    def compute_signal(
        self,
        revenue_series: np.ndarray,
        dau_series: np.ndarray,
        tvl_series: np.ndarray,
        fee_series: np.ndarray
    ) -> Tuple[MomentumSignal, int, Dict[str, float]]:
        """
        Compute momentum signal from time series data.

        Returns:
            Tuple of (signal, score, component_momentums)
        """
        momentums = {}

        # Revenue momentum (30d)
        momentums['revenue'] = compute_momentum(revenue_series, 30)

        # DAU momentum (30d)
        momentums['dau'] = compute_momentum(dau_series, 30)

        # TVL momentum (30d)
        momentums['tvl'] = compute_momentum(tvl_series, 30)

        # Fee momentum (30d)
        momentums['fees'] = compute_momentum(fee_series, 30)

        # Weighted composite momentum
        composite = sum(
            momentums.get(k, 0) * v
            for k, v in self.weights.items()
        )

        # Classify signal
        if composite > 0.20:
            signal = MomentumSignal.STRONG_BULLISH
        elif composite > 0.05:
            signal = MomentumSignal.BULLISH
        elif composite > -0.05:
            signal = MomentumSignal.NEUTRAL
        elif composite > -0.20:
            signal = MomentumSignal.BEARISH
        else:
            signal = MomentumSignal.STRONG_BEARISH

        # Score (0-100)
        # Map composite from [-0.5, 0.5] to [0, 100]
        score = int(min(100, max(0, (composite + 0.5) * 100)))

        return signal, score, momentums


# ==========================================
# MEAN REVERSION MODEL
# ==========================================

class MeanReversionModel:
    """
    Z-score based mean reversion model.

    Identifies when metrics are extended relative to historical norms.
    Useful for timing entries/exits on stretched fundamentals.
    """

    def __init__(self):
        self.thresholds = {
            'oversold': -1.5,
            'slightly_oversold': -0.75,
            'fair_value_low': -0.25,
            'fair_value_high': 0.25,
            'slightly_overbought': 0.75,
            'overbought': 1.5
        }

    def compute_signal(
        self,
        revenue_series: np.ndarray,
        dau_series: np.ndarray,
        valuation_series: np.ndarray  # P/E or P/F ratio
    ) -> Tuple[ReversionSignal, int, Dict[str, float]]:
        """
        Compute mean reversion signal.

        Returns:
            Tuple of (signal, score, component_zscores)
        """
        zscores = {}

        # Revenue z-score (positive = above mean = bullish)
        zscores['revenue'] = compute_zscore_static(revenue_series)

        # DAU z-score (positive = above mean = bullish)
        zscores['dau'] = compute_zscore_static(dau_series)

        # Valuation z-score (INVERTED: high = expensive = bearish)
        zscores['valuation'] = -compute_zscore_static(valuation_series)

        # Composite (equal weight)
        composite = np.nanmean(list(zscores.values()))

        # Classify signal
        if composite <= self.thresholds['oversold']:
            signal = ReversionSignal.OVERSOLD
        elif composite <= self.thresholds['slightly_oversold']:
            signal = ReversionSignal.SLIGHTLY_OVERSOLD
        elif composite <= self.thresholds['fair_value_high']:
            signal = ReversionSignal.FAIR_VALUE
        elif composite <= self.thresholds['slightly_overbought']:
            signal = ReversionSignal.SLIGHTLY_OVERBOUGHT
        else:
            signal = ReversionSignal.OVERBOUGHT

        # Score (0-100, where 100 = most oversold = buy signal)
        # Map composite from [-2, 2] to [100, 0] (inverted for buy signal)
        score = int(min(100, max(0, (-composite + 2) * 25)))

        return signal, score, zscores


# ==========================================
# PROTOCOL HEALTH CLASSIFIER
# ==========================================

class ProtocolHealthClassifier:
    """
    Logistic regression-style classifier for protocol health prediction.

    Predicts probability of:
    - Protocol being "healthy" (positive earnings) in 6 months
    - Protocol surviving (still active) in 12 months
    - Protocol tier classification

    Features:
    - Subsidy score (negative = healthier)
    - Float ratio (higher = healthier)
    - Revenue trend (positive = healthier)
    - Developer count (higher = healthier)
    - DAU/MAU ratio (higher = healthier)
    """

    def __init__(self):
        # Calibrated coefficients (interpretable logistic regression)
        self.health_coefficients = {
            'intercept': 0.0,
            'subsidy_score': -1.5,      # High subsidy = unhealthy
            'float_ratio': 1.0,          # High float = healthy
            'revenue_momentum': 2.0,     # Growing revenue = healthy
            'developer_count': 0.5,      # More devs = healthy
            'dau_mau_ratio': 1.5,        # High stickiness = healthy
        }

        self.survival_coefficients = {
            'intercept': 1.0,            # Base survival is high
            'subsidy_score': -2.0,       # Unsustainable = death
            'developer_count': 1.0,      # Devs keep it alive
            'dau': 0.3,                  # Users = survival
            'float_ratio': 0.5,          # Dilution kills
        }

    def predict(
        self,
        subsidy_score: float,
        float_ratio: float,
        revenue_momentum: float,
        developer_count: int,
        dau_mau_ratio: float,
        dau: int
    ) -> ProtocolHealthPrediction:
        """
        Predict protocol health probabilities.

        Returns:
            ProtocolHealthPrediction with probabilities and drivers
        """
        # Health probability (6 month)
        health_logit = (
            self.health_coefficients['intercept'] +
            self.health_coefficients['subsidy_score'] * min(subsidy_score, 5) +
            self.health_coefficients['float_ratio'] * float_ratio +
            self.health_coefficients['revenue_momentum'] * revenue_momentum +
            self.health_coefficients['developer_count'] * np.log1p(developer_count) / 3 +
            self.health_coefficients['dau_mau_ratio'] * dau_mau_ratio
        )
        health_prob = sigmoid(health_logit)

        # Survival probability (12 month)
        survival_logit = (
            self.survival_coefficients['intercept'] +
            self.survival_coefficients['subsidy_score'] * min(subsidy_score, 5) +
            self.survival_coefficients['developer_count'] * np.log1p(developer_count) / 3 +
            self.survival_coefficients['dau'] * np.log1p(dau) / 10 +
            self.survival_coefficients['float_ratio'] * float_ratio
        )
        survival_prob = sigmoid(survival_logit)

        # Tier probabilities (simplified)
        tier_probs = self._compute_tier_probs(
            subsidy_score, float_ratio, health_prob
        )

        # Key drivers (feature contributions)
        drivers = [
            ('subsidy_score', -subsidy_score * 0.3),
            ('float_ratio', float_ratio * 0.2),
            ('revenue_momentum', revenue_momentum * 0.25),
            ('developer_activity', np.log1p(developer_count) * 0.1),
            ('user_stickiness', dau_mau_ratio * 0.15),
        ]
        drivers.sort(key=lambda x: abs(x[1]), reverse=True)

        # Confidence based on data completeness
        data_quality = sum([
            1 if subsidy_score > 0 else 0,
            1 if float_ratio > 0 else 0,
            1 if developer_count > 0 else 0,
            1 if dau > 0 else 0,
        ]) / 4

        if data_quality > 0.75:
            confidence = "HIGH"
        elif data_quality > 0.5:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        uncertainty = 1 - data_quality

        return ProtocolHealthPrediction(
            project_id="",  # Filled by caller
            health_probability=round(health_prob, 3),
            survival_probability=round(survival_prob, 3),
            tier_probability=tier_probs,
            key_drivers=drivers[:3],
            confidence=confidence,
            uncertainty=round(uncertainty, 2)
        )

    def _compute_tier_probs(
        self,
        subsidy_score: float,
        float_ratio: float,
        health_prob: float
    ) -> Dict[str, float]:
        """Compute tier classification probabilities"""

        # Tier 1: Organic growth, healthy float, high health prob
        tier1_score = (
            (1 if subsidy_score < 0.5 else 0) * 0.4 +
            (1 if float_ratio > 0.5 else 0) * 0.3 +
            health_prob * 0.3
        )

        # Avoid: Unsustainable or predatory
        avoid_score = (
            (1 if subsidy_score > 2.0 else 0) * 0.5 +
            (1 if float_ratio < 0.2 else 0) * 0.3 +
            (1 - health_prob) * 0.2
        )

        # Tier 2: Everything else
        tier2_score = 1 - tier1_score - avoid_score
        tier2_score = max(0, tier2_score)

        # Normalize
        total = tier1_score + tier2_score + avoid_score
        if total > 0:
            return {
                'tier1': round(tier1_score / total, 3),
                'tier2': round(tier2_score / total, 3),
                'avoid': round(avoid_score / total, 3)
            }
        return {'tier1': 0.33, 'tier2': 0.34, 'avoid': 0.33}


# ==========================================
# SECTOR ROTATION MODEL
# ==========================================

class SectorRotationModel:
    """
    Cross-sector momentum and rotation model.

    Identifies which sectors are gaining/losing relative strength.
    Recommends overweight/underweight positions by sector.
    """

    def __init__(self):
        self.momentum_weight = 0.40
        self.quality_weight = 0.35
        self.relative_strength_weight = 0.25

    def compute_rotation(
        self,
        sector_data: Dict[str, Dict]  # sector -> {momentum, quality, rel_strength}
    ) -> Dict[str, SectorRotationSignal]:
        """
        Compute sector rotation signals.

        Args:
            sector_data: Dictionary with sector metrics

        Returns:
            Dictionary of sector -> SectorRotationSignal
        """
        signals = {}

        # Compute composite scores
        scores = {}
        for sector, data in sector_data.items():
            momentum = data.get('momentum', 0)
            quality = data.get('quality', 50)
            rel_strength = data.get('relative_strength', 0)

            # Normalize momentum to 0-100 scale
            momentum_norm = min(100, max(0, (momentum + 0.5) * 100))

            # Composite score
            composite = (
                momentum_norm * self.momentum_weight +
                quality * self.quality_weight +
                (rel_strength + 1) * 50 * self.relative_strength_weight
            )
            scores[sector] = composite

        # Rank sectors
        sorted_sectors = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        total_sectors = len(sorted_sectors)

        for rank, (sector, score) in enumerate(sorted_sectors):
            data = sector_data[sector]

            # Signal based on rank
            if rank < total_sectors * 0.33:
                signal = "OVERWEIGHT"
                weight = 1.5 / total_sectors * 100  # 50% more than neutral
            elif rank < total_sectors * 0.67:
                signal = "NEUTRAL"
                weight = 1.0 / total_sectors * 100
            else:
                signal = "UNDERWEIGHT"
                weight = 0.5 / total_sectors * 100  # 50% less than neutral

            signals[sector] = SectorRotationSignal(
                sector=sector,
                momentum_score=data.get('momentum', 0),
                relative_strength=data.get('relative_strength', 0),
                quality_score=data.get('quality', 50),
                rotation_signal=signal,
                recommended_weight=round(weight, 1)
            )

        return signals


# ==========================================
# MAIN ML ENGINE
# ==========================================

class CryptoMLEngine:
    """
    Complete ML engine for crypto systematic analysis.

    Combines:
    - Momentum model (trend detection)
    - Mean reversion model (value signals)
    - Health classifier (fundamental prediction)
    - Sector rotation (cross-sector positioning)
    """

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.momentum_model = MomentumModel()
        self.reversion_model = MeanReversionModel()
        self.health_classifier = ProtocolHealthClassifier()
        self.sector_model = SectorRotationModel()

    def generate_signals(self) -> CryptoMLSignals:
        """
        Generate all ML signals for current state.

        Returns:
            CryptoMLSignals with complete signal set
        """
        today = datetime.now().strftime('%Y-%m-%d')

        # 1. Load time series data
        timeseries_data = self._load_timeseries_data()

        # 2. Load latest scores
        scores_data = self._load_scores_data()

        # 3. Compute protocol-level time series signals
        protocol_ts = {}
        for project_id, ts_data in timeseries_data.items():
            protocol_ts[project_id] = self._compute_protocol_timeseries(
                project_id, ts_data
            )

        # 4. Compute protocol health predictions
        protocol_pred = {}
        for project_id, score_data in scores_data.items():
            ts = protocol_ts.get(project_id)
            rev_mom = ts.revenue_momentum if ts else 0

            pred = self.health_classifier.predict(
                subsidy_score=score_data.get('subsidy_score', 1.0),
                float_ratio=score_data.get('float_ratio', 0.5),
                revenue_momentum=rev_mom,
                developer_count=score_data.get('active_developers', 0),
                dau_mau_ratio=score_data.get('dau_mau_ratio', 0.15),
                dau=score_data.get('dau', 0)
            )
            pred.project_id = project_id
            protocol_pred[project_id] = pred

        # 5. Compute sector rotation
        sector_data = self._compute_sector_data(scores_data, protocol_ts)
        sector_rotation = self.sector_model.compute_rotation(sector_data)

        # 6. Compute universe-level signals
        universe_mom = self._compute_universe_momentum(protocol_ts)
        universe_rev = self._compute_universe_reversion(protocol_ts)

        # 7. Regime transition probabilities
        regime_probs = self._estimate_regime_transitions(
            universe_mom, universe_rev, scores_data
        )

        # 8. Ensemble conviction score
        conviction = self._compute_ml_conviction(
            universe_mom, universe_rev, protocol_pred
        )

        return CryptoMLSignals(
            date=today,
            protocol_timeseries=protocol_ts,
            protocol_predictions=protocol_pred,
            sector_rotation=sector_rotation,
            universe_momentum=universe_mom,
            universe_reversion=universe_rev,
            regime_transition_prob=regime_probs,
            ml_conviction_score=conviction
        )

    def _load_timeseries_data(self) -> Dict[str, Dict[str, np.ndarray]]:
        """Load time series data for all protocols"""
        query = """
            SELECT project_id, date, metric_id, value
            FROM crypto_metrics
            WHERE metric_id IN ('revenue', 'fees', 'user_dau', 'tvl', 'pf_fully_diluted')
            AND date >= date('now', '-90 days')
            ORDER BY project_id, metric_id, date
        """

        try:
            df = pd.read_sql(query, self.conn)
        except Exception:
            return {}

        result = {}
        for project_id in df['project_id'].unique():
            project_df = df[df['project_id'] == project_id]
            result[project_id] = {}

            for metric in ['revenue', 'fees', 'user_dau', 'tvl', 'pf_fully_diluted']:
                metric_df = project_df[project_df['metric_id'] == metric]
                if not metric_df.empty:
                    result[project_id][metric] = metric_df['value'].values

        return result

    def _load_scores_data(self) -> Dict[str, Dict]:
        """Load latest scores data"""
        query = """
            SELECT project_id, subsidy_score, float_ratio, dau, mau,
                   active_developers, overall_score, sector
            FROM crypto_scores
            WHERE date = (SELECT MAX(date) FROM crypto_scores)
        """

        try:
            df = pd.read_sql(query, self.conn)
        except Exception:
            return {}

        result = {}
        for _, row in df.iterrows():
            dau_mau = row['dau'] / row['mau'] if row['mau'] and row['mau'] > 0 else 0
            result[row['project_id']] = {
                'subsidy_score': row['subsidy_score'] or 1.0,
                'float_ratio': row['float_ratio'] or 0.5,
                'dau': row['dau'] or 0,
                'mau': row['mau'] or 0,
                'dau_mau_ratio': dau_mau,
                'active_developers': row['active_developers'] or 0,
                'overall_score': row['overall_score'] or 50,
                'sector': row['sector'] or 'Unknown'
            }

        return result

    def _compute_protocol_timeseries(
        self,
        project_id: str,
        ts_data: Dict[str, np.ndarray]
    ) -> ProtocolTimeSeries:
        """Compute time series analysis for single protocol"""

        revenue = ts_data.get('revenue', np.array([0]))
        fees = ts_data.get('fees', np.array([0]))
        dau = ts_data.get('user_dau', np.array([0]))
        tvl = ts_data.get('tvl', np.array([0]))
        valuation = ts_data.get('pf_fully_diluted', np.array([0]))

        # Momentum signals
        mom_signal, mom_score, momentums = self.momentum_model.compute_signal(
            revenue, dau, tvl, fees
        )

        # Reversion signals
        rev_signal, rev_score, zscores = self.reversion_model.compute_signal(
            revenue, dau, valuation
        )

        # Trend acceleration
        revenue_trend = compute_trend_acceleration(revenue)
        dau_trend = compute_trend_acceleration(dau)

        # Overall trend score
        trend_scores = {'ACCELERATING': 75, 'STABLE': 50, 'DECELERATING': 25}
        trend_score = (
            trend_scores.get(revenue_trend, 50) * 0.6 +
            trend_scores.get(dau_trend, 50) * 0.4
        )

        return ProtocolTimeSeries(
            project_id=project_id,
            revenue_momentum=momentums.get('revenue', 0),
            dau_momentum=momentums.get('dau', 0),
            tvl_momentum=momentums.get('tvl', 0),
            fee_momentum=momentums.get('fees', 0),
            momentum_signal=mom_signal,
            momentum_score=mom_score,
            revenue_zscore=zscores.get('revenue', 0),
            dau_zscore=zscores.get('dau', 0),
            valuation_zscore=zscores.get('valuation', 0),
            reversion_signal=rev_signal,
            reversion_score=rev_score,
            revenue_trend=revenue_trend,
            dau_trend=dau_trend,
            overall_trend_score=int(trend_score)
        )

    def _compute_sector_data(
        self,
        scores_data: Dict[str, Dict],
        protocol_ts: Dict[str, ProtocolTimeSeries]
    ) -> Dict[str, Dict]:
        """Aggregate protocol data to sector level"""
        sector_metrics = {}

        for project_id, data in scores_data.items():
            sector = data.get('sector', 'Unknown')

            if sector not in sector_metrics:
                sector_metrics[sector] = {
                    'momentums': [],
                    'qualities': [],
                    'count': 0
                }

            # Add momentum from time series
            ts = protocol_ts.get(project_id)
            if ts:
                sector_metrics[sector]['momentums'].append(ts.revenue_momentum)

            # Add quality from scores
            sector_metrics[sector]['qualities'].append(data.get('overall_score', 50))
            sector_metrics[sector]['count'] += 1

        # Compute sector-level metrics
        result = {}
        for sector, metrics in sector_metrics.items():
            result[sector] = {
                'momentum': np.nanmean(metrics['momentums']) if metrics['momentums'] else 0,
                'quality': np.nanmean(metrics['qualities']),
                'relative_strength': 0,  # Would need benchmark data
                'protocol_count': metrics['count']
            }

        return result

    def _compute_universe_momentum(
        self,
        protocol_ts: Dict[str, ProtocolTimeSeries]
    ) -> MomentumSignal:
        """Compute universe-wide momentum signal"""
        if not protocol_ts:
            return MomentumSignal.NEUTRAL

        scores = [ts.momentum_score for ts in protocol_ts.values()]
        avg_score = np.nanmean(scores)

        if avg_score >= 70:
            return MomentumSignal.STRONG_BULLISH
        elif avg_score >= 55:
            return MomentumSignal.BULLISH
        elif avg_score >= 45:
            return MomentumSignal.NEUTRAL
        elif avg_score >= 30:
            return MomentumSignal.BEARISH
        return MomentumSignal.STRONG_BEARISH

    def _compute_universe_reversion(
        self,
        protocol_ts: Dict[str, ProtocolTimeSeries]
    ) -> ReversionSignal:
        """Compute universe-wide reversion signal"""
        if not protocol_ts:
            return ReversionSignal.FAIR_VALUE

        scores = [ts.reversion_score for ts in protocol_ts.values()]
        avg_score = np.nanmean(scores)

        if avg_score >= 75:
            return ReversionSignal.OVERSOLD
        elif avg_score >= 60:
            return ReversionSignal.SLIGHTLY_OVERSOLD
        elif avg_score >= 40:
            return ReversionSignal.FAIR_VALUE
        elif avg_score >= 25:
            return ReversionSignal.SLIGHTLY_OVERBOUGHT
        return ReversionSignal.OVERBOUGHT

    def _estimate_regime_transitions(
        self,
        momentum: MomentumSignal,
        reversion: ReversionSignal,
        scores_data: Dict[str, Dict]
    ) -> Dict[str, float]:
        """Estimate probability of transitioning to each regime"""

        # Base probabilities from momentum
        mom_probs = {
            MomentumSignal.STRONG_BULLISH: {'expansion': 0.6, 'late_cycle': 0.3, 'pre_crisis': 0.08, 'crisis': 0.02},
            MomentumSignal.BULLISH: {'expansion': 0.5, 'late_cycle': 0.35, 'pre_crisis': 0.12, 'crisis': 0.03},
            MomentumSignal.NEUTRAL: {'expansion': 0.25, 'late_cycle': 0.40, 'pre_crisis': 0.25, 'crisis': 0.10},
            MomentumSignal.BEARISH: {'expansion': 0.10, 'late_cycle': 0.30, 'pre_crisis': 0.40, 'crisis': 0.20},
            MomentumSignal.STRONG_BEARISH: {'expansion': 0.05, 'late_cycle': 0.15, 'pre_crisis': 0.35, 'crisis': 0.45},
        }

        probs = mom_probs.get(momentum, mom_probs[MomentumSignal.NEUTRAL]).copy()

        # Adjust by reversion (oversold = more likely to expand)
        if reversion == ReversionSignal.OVERSOLD:
            probs['expansion'] += 0.15
            probs['crisis'] -= 0.10
        elif reversion == ReversionSignal.OVERBOUGHT:
            probs['expansion'] -= 0.15
            probs['pre_crisis'] += 0.10

        # Normalize
        total = sum(probs.values())
        return {k: round(v/total, 3) for k, v in probs.items()}

    def _compute_ml_conviction(
        self,
        momentum: MomentumSignal,
        reversion: ReversionSignal,
        predictions: Dict[str, ProtocolHealthPrediction]
    ) -> int:
        """Compute overall ML conviction score"""

        # Momentum component
        mom_scores = {
            MomentumSignal.STRONG_BULLISH: 90,
            MomentumSignal.BULLISH: 70,
            MomentumSignal.NEUTRAL: 50,
            MomentumSignal.BEARISH: 30,
            MomentumSignal.STRONG_BEARISH: 10,
        }
        mom_score = mom_scores.get(momentum, 50)

        # Reversion component (oversold = bullish)
        rev_scores = {
            ReversionSignal.OVERSOLD: 80,
            ReversionSignal.SLIGHTLY_OVERSOLD: 65,
            ReversionSignal.FAIR_VALUE: 50,
            ReversionSignal.SLIGHTLY_OVERBOUGHT: 35,
            ReversionSignal.OVERBOUGHT: 20,
        }
        rev_score = rev_scores.get(reversion, 50)

        # Health prediction component
        health_scores = [p.health_probability * 100 for p in predictions.values()]
        health_score = np.nanmean(health_scores) if health_scores else 50

        # Weighted ensemble
        conviction = int(
            mom_score * 0.35 +
            rev_score * 0.30 +
            health_score * 0.35
        )

        return min(100, max(0, conviction))

    def print_summary(self, signals: CryptoMLSignals):
        """Print summary of ML signals"""
        print()
        print("=" * 70)
        print("CRYPTO ML SIGNALS SUMMARY")
        print(f"Date: {signals.date}")
        print("=" * 70)

        print("\n--- UNIVERSE SIGNALS ---")
        print(f"Momentum:  {signals.universe_momentum.value}")
        print(f"Reversion: {signals.universe_reversion.value}")
        print(f"ML Conviction Score: {signals.ml_conviction_score}/100")

        print("\n--- REGIME TRANSITION PROBABILITIES ---")
        for regime, prob in signals.regime_transition_prob.items():
            print(f"  {regime:12} {prob:>6.1%}")

        print("\n--- SECTOR ROTATION ---")
        for sector, sig in signals.sector_rotation.items():
            print(f"  {sector[:25]:25} {sig.rotation_signal:12} {sig.recommended_weight:5.1f}%")

        print("\n--- TOP PROTOCOLS (by health probability) ---")
        sorted_pred = sorted(
            signals.protocol_predictions.items(),
            key=lambda x: x[1].health_probability,
            reverse=True
        )[:10]
        for pid, pred in sorted_pred:
            print(f"  {pid[:25]:25} Health: {pred.health_probability:5.1%}  Survival: {pred.survival_probability:5.1%}")

        print()
        print("=" * 70)


# ==========================================
# CLI
# ==========================================

if __name__ == "__main__":
    DB_PATH = "/Users/bob/LHM/Data/databases/Lighthouse_Master.db"

    print("Lighthouse Macro Crypto ML Engine")
    print("=" * 50)

    conn = sqlite3.connect(DB_PATH)
    engine = CryptoMLEngine(conn)

    signals = engine.generate_signals()
    engine.print_summary(signals)

    conn.close()
