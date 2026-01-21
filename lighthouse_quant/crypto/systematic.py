"""
LIGHTHOUSE MACRO - CRYPTO SYSTEMATIC FRAMEWORK
===============================================
80% Systematic / 20% Discretionary

Philosophy:
    "Flows > Stocks applies to crypto. The systematic engine handles
    regime detection, threshold monitoring, and signal generation.
    Discretion reserved for narrative interpretation and edge cases."

Architecture:
    1. Crypto Health Index (CHI) - Master composite (analogous to MRI)
    2. Warning System - 25+ threshold flags with override logic
    3. Time Series Models - AR/momentum models for trend detection
    4. ML Ensemble - Protocol health probability estimation
    5. Macro Overlay - Regime adjustment from MRI/LCI

The 80/20 split matches the brain's systematic vs intuitive processing:
    - 80% systematic: Pattern recognition, threshold monitoring, regime detection
    - 20% discretionary: Narrative analysis, edge cases, conviction weighting

Usage:
    from lighthouse_quant.crypto.systematic import CryptoSystematicEngine

    engine = CryptoSystematicEngine(conn)
    result = engine.evaluate()

    # Result contains:
    # - chi: Crypto Health Index (-2 to +2 scale)
    # - regime: EXPANSION / LATE_CYCLE / HOLLOW_RALLY / PRE_CRISIS / CRISIS
    # - warning_level: GREEN / YELLOW / AMBER / RED
    # - protocol_signals: Dict of protocol-level systematic scores
    # - sector_rotation: Recommended sector positioning
    # - macro_overlay: MRI/LCI impact on crypto allocation
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import warnings
warnings.filterwarnings('ignore')


# ==========================================
# ENUMS & CONFIGURATION
# ==========================================

class CryptoRegime(Enum):
    """Crypto market regime classification"""
    EXPANSION = "EXPANSION"           # Bull market, fundamentals improving
    LATE_CYCLE = "LATE_CYCLE"         # Bull exhaustion, subsidies rising
    HOLLOW_RALLY = "HOLLOW_RALLY"     # Prices stable, fundamentals eroding
    PRE_CRISIS = "PRE_CRISIS"         # Multiple warnings, exit signals
    CRISIS = "CRISIS"                 # Bear market, capitulation


class WarningLevel(Enum):
    """Warning system levels"""
    GREEN = 1    # Normal, bullish
    YELLOW = 2   # Elevated monitoring
    AMBER = 3    # High alert
    RED = 4      # Crisis conditions


class FlagSeverity(Enum):
    """Threshold flag severity"""
    MONITOR = 1
    WARNING = 2
    CRITICAL = 3
    OVERRIDE = 4  # Forces minimum AMBER


# Threshold definitions for crypto warning flags
CRYPTO_THRESHOLDS = {
    # === FINANCIAL HEALTH ===
    'SUBSIDY_UNSUSTAINABLE': {
        'metric': 'subsidy_score',
        'condition': 'gt',
        'threshold': 2.0,
        'severity': FlagSeverity.CRITICAL,
        'category': 'financial',
        'description': 'Token incentives > 2x revenue (ponzi economics)'
    },
    'SUBSIDY_ELEVATED': {
        'metric': 'subsidy_score',
        'condition': 'gt',
        'threshold': 1.0,
        'severity': FlagSeverity.WARNING,
        'category': 'financial',
        'description': 'Token incentives exceeding revenue'
    },
    'REVENUE_COLLAPSE': {
        'metric': 'revenue_mom',
        'condition': 'lt',
        'threshold': -0.30,
        'severity': FlagSeverity.CRITICAL,
        'category': 'financial',
        'description': 'Revenue down >30% month-over-month'
    },
    'FEE_COLLAPSE': {
        'metric': 'fees_mom',
        'condition': 'lt',
        'threshold': -0.30,
        'severity': FlagSeverity.CRITICAL,
        'category': 'financial',
        'description': 'Fees down >30% month-over-month'
    },
    'TVL_HEMORRHAGE': {
        'metric': 'tvl_mom',
        'condition': 'lt',
        'threshold': -0.25,
        'severity': FlagSeverity.OVERRIDE,
        'category': 'financial',
        'description': 'TVL down >25% month-over-month (bank run)'
    },
    'NEGATIVE_EARNINGS': {
        'metric': 'earnings_negative_streak',
        'condition': 'gt',
        'threshold': 3,
        'severity': FlagSeverity.WARNING,
        'category': 'financial',
        'description': '3+ consecutive months of negative earnings'
    },

    # === USER ADOPTION ===
    'DAU_COLLAPSE': {
        'metric': 'dau_mom',
        'condition': 'lt',
        'threshold': -0.40,
        'severity': FlagSeverity.CRITICAL,
        'category': 'usage',
        'description': 'Daily active users down >40% MoM'
    },
    'STICKINESS_WARNING': {
        'metric': 'dau_mau_ratio',
        'condition': 'lt',
        'threshold': 0.10,
        'severity': FlagSeverity.WARNING,
        'category': 'usage',
        'description': 'DAU/MAU ratio below 10% (poor retention)'
    },
    'DEVELOPER_EXODUS': {
        'metric': 'developer_mom',
        'condition': 'lt',
        'threshold': -0.30,
        'severity': FlagSeverity.CRITICAL,
        'category': 'usage',
        'description': 'Active developers down >30% MoM'
    },
    'GHOST_CHAIN': {
        'metric': 'dau',
        'condition': 'lt',
        'threshold': 500,
        'severity': FlagSeverity.OVERRIDE,
        'category': 'usage',
        'description': 'Fewer than 500 daily active users'
    },

    # === TOKENOMICS / DILUTION ===
    'PREDATORY_FLOAT': {
        'metric': 'float_ratio',
        'condition': 'lt',
        'threshold': 0.20,
        'severity': FlagSeverity.CRITICAL,
        'category': 'tokenomics',
        'description': 'Float ratio <20% (massive unlock overhang)'
    },
    'LOW_FLOAT': {
        'metric': 'float_ratio',
        'condition': 'lt',
        'threshold': 0.35,
        'severity': FlagSeverity.WARNING,
        'category': 'tokenomics',
        'description': 'Float ratio <35% (significant unlock risk)'
    },
    'DILUTION_ACCELERATION': {
        'metric': 'dilution_rate_change',
        'condition': 'gt',
        'threshold': 0.10,
        'severity': FlagSeverity.WARNING,
        'category': 'tokenomics',
        'description': 'Token emission rate accelerating >10%'
    },

    # === VALUATION ===
    'EXTREME_OVERVALUATION': {
        'metric': 'pe_ratio',
        'condition': 'gt',
        'threshold': 200,
        'severity': FlagSeverity.WARNING,
        'category': 'valuation',
        'description': 'P/E ratio >200x'
    },
    'VAPORWARE': {
        'metric': 'revenue_per_billion_fdv',
        'condition': 'lt',
        'threshold': 1_000_000,
        'severity': FlagSeverity.CRITICAL,
        'category': 'valuation',
        'description': 'FDV >$1B with <$1M annual revenue'
    },

    # === SECTOR HEALTH ===
    'SECTOR_CONTAGION': {
        'metric': 'sector_health_score',
        'condition': 'lt',
        'threshold': 40,
        'severity': FlagSeverity.WARNING,
        'category': 'sector',
        'description': 'Sector average health score <40'
    },
    'TIER1_DROUGHT': {
        'metric': 'tier1_count',
        'condition': 'lt',
        'threshold': 3,
        'severity': FlagSeverity.WARNING,
        'category': 'sector',
        'description': 'Fewer than 3 Tier 1 protocols across universe'
    },

    # === MACRO OVERLAY ===
    'MACRO_HOSTILE': {
        'metric': 'mri',
        'condition': 'gt',
        'threshold': 0.25,
        'severity': FlagSeverity.WARNING,
        'category': 'macro',
        'description': 'MRI >0.25 (pre-recession macro environment)'
    },
    'LIQUIDITY_STRESS': {
        'metric': 'lci',
        'condition': 'lt',
        'threshold': -0.5,
        'severity': FlagSeverity.CRITICAL,
        'category': 'macro',
        'description': 'LCI <-0.5 (liquidity scarce, risk-off)'
    },
    'MACRO_CRISIS': {
        'metric': 'mri',
        'condition': 'gt',
        'threshold': 0.50,
        'severity': FlagSeverity.OVERRIDE,
        'category': 'macro',
        'description': 'MRI >0.50 (recession conditions)'
    },
}


# CHI (Crypto Health Index) component weights
CHI_WEIGHTS = {
    'financial_health': 0.30,    # Revenue quality, subsidy sustainability
    'user_adoption': 0.25,       # DAU growth, stickiness, developer activity
    'valuation': 0.20,           # P/E, P/F, earnings yield
    'tokenomics': 0.15,          # Float ratio, dilution rate
    'macro_overlay': 0.10,       # MRI/LCI adjustment
}


# ==========================================
# DATA STRUCTURES
# ==========================================

@dataclass
class WarningFlag:
    """Individual warning flag result"""
    name: str
    triggered: bool
    severity: FlagSeverity
    category: str
    description: str
    current_value: Optional[float] = None
    threshold: Optional[float] = None


@dataclass
class CryptoWarningResult:
    """Complete warning system evaluation"""
    flags: List[WarningFlag]
    overall_level: WarningLevel
    category_scores: Dict[str, int]  # Category -> triggered count
    override_flags: List[str]
    critical_flags: List[str]
    summary: str


@dataclass
class ProtocolSystematicScore:
    """Systematic score for individual protocol"""
    project_id: str
    name: str

    # Component scores (0-100)
    fundamental_score: int      # From fundamentals engine
    momentum_score: int         # Price/usage trend
    warning_score: int          # Inverted from warnings (100 = no warnings)
    macro_adjusted_score: int   # After macro overlay

    # Final systematic output
    systematic_score: int       # 0-100 overall
    systematic_signal: str      # BUY / HOLD / REDUCE / AVOID
    confidence: str             # HIGH / MEDIUM / LOW


@dataclass
class CryptoSystematicResult:
    """Complete systematic evaluation output"""
    date: str

    # Master composite
    chi: float                  # Crypto Health Index (-2 to +2)
    chi_status: str

    # Regime
    regime: CryptoRegime
    regime_description: str

    # Warning system
    warning_level: WarningLevel
    warning_summary: str
    active_flags: List[str]

    # Protocol signals
    protocol_signals: Dict[str, ProtocolSystematicScore]

    # Sector rotation
    sector_rankings: Dict[str, float]  # Sector -> score
    recommended_sectors: List[str]
    avoid_sectors: List[str]

    # Macro overlay
    mri: Optional[float]
    lci: Optional[float]
    macro_allocation_multiplier: float

    # Tier summary
    tier1_protocols: List[str]
    tier2_protocols: List[str]
    avoid_protocols: List[str]

    # Actionable output
    systematic_allocation: float    # 0-100% recommended crypto exposure
    discretionary_notes: List[str]  # Things requiring human judgment


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def compute_zscore(series: pd.Series, window: int = 30, min_periods: int = 10) -> pd.Series:
    """Rolling z-score computation"""
    rolling_mean = series.rolling(window, min_periods=min_periods).mean()
    rolling_std = series.rolling(window, min_periods=min_periods).std()
    rolling_std = rolling_std.replace(0, np.nan)
    return (series - rolling_mean) / rolling_std


def compute_momentum(series: pd.Series, periods: int = 30) -> float:
    """Compute momentum as rate of change"""
    if len(series) < periods + 1:
        return 0.0
    current = series.iloc[-1]
    past = series.iloc[-periods-1]
    if past == 0 or pd.isna(past):
        return 0.0
    return (current - past) / abs(past)


def get_chi_status(chi: float) -> str:
    """Get status label for CHI value"""
    if chi >= 1.0:
        return "STRONG EXPANSION"
    elif chi >= 0.5:
        return "EXPANSION"
    elif chi >= 0.0:
        return "NEUTRAL"
    elif chi >= -0.5:
        return "WEAKENING"
    elif chi >= -1.0:
        return "CONTRACTION"
    else:
        return "CRISIS"


# ==========================================
# MAIN ENGINE
# ==========================================

class CryptoSystematicEngine:
    """
    80% Systematic / 20% Discretionary Crypto Analysis Engine

    Provides systematic signals for:
    - Overall crypto health (CHI)
    - Regime classification
    - Protocol-level scoring
    - Sector rotation
    - Macro overlay adjustments

    Leaves 20% discretionary for:
    - Narrative interpretation
    - Edge case handling
    - Conviction weighting
    - Timing refinement
    """

    def __init__(self, conn: sqlite3.Connection):
        """
        Initialize the systematic engine.

        Args:
            conn: Database connection with crypto_metrics, crypto_scores,
                  lighthouse_indices tables
        """
        self.conn = conn
        self.thresholds = CRYPTO_THRESHOLDS
        self.chi_weights = CHI_WEIGHTS

    # ==========================================
    # WARNING SYSTEM
    # ==========================================

    def evaluate_warnings(self, metrics: Dict[str, float]) -> CryptoWarningResult:
        """
        Evaluate all warning flags against current metrics.

        Args:
            metrics: Dictionary of metric_name -> current_value

        Returns:
            CryptoWarningResult with all flag evaluations
        """
        flags = []
        override_flags = []
        critical_flags = []
        category_counts = {}

        for flag_name, flag_def in self.thresholds.items():
            metric_value = metrics.get(flag_def['metric'])

            # Check if flag is triggered
            triggered = False
            if metric_value is not None:
                if flag_def['condition'] == 'gt':
                    triggered = metric_value > flag_def['threshold']
                elif flag_def['condition'] == 'lt':
                    triggered = metric_value < flag_def['threshold']
                elif flag_def['condition'] == 'eq':
                    triggered = metric_value == flag_def['threshold']

            flag = WarningFlag(
                name=flag_name,
                triggered=triggered,
                severity=flag_def['severity'],
                category=flag_def['category'],
                description=flag_def['description'],
                current_value=metric_value,
                threshold=flag_def['threshold']
            )
            flags.append(flag)

            if triggered:
                category = flag_def['category']
                category_counts[category] = category_counts.get(category, 0) + 1

                if flag_def['severity'] == FlagSeverity.OVERRIDE:
                    override_flags.append(flag_name)
                elif flag_def['severity'] == FlagSeverity.CRITICAL:
                    critical_flags.append(flag_name)

        # Determine overall warning level
        overall_level = self._determine_warning_level(
            override_flags, critical_flags, category_counts
        )

        # Generate summary
        summary = self._generate_warning_summary(
            overall_level, override_flags, critical_flags, category_counts
        )

        return CryptoWarningResult(
            flags=flags,
            overall_level=overall_level,
            category_scores=category_counts,
            override_flags=override_flags,
            critical_flags=critical_flags,
            summary=summary
        )

    def _determine_warning_level(
        self,
        override_flags: List[str],
        critical_flags: List[str],
        category_counts: Dict[str, int]
    ) -> WarningLevel:
        """Determine overall warning level from flags"""

        # Override flags force minimum AMBER
        if len(override_flags) >= 2:
            return WarningLevel.RED
        if override_flags:
            return WarningLevel.AMBER

        # Multiple critical flags across categories -> AMBER
        critical_categories = sum(1 for c in category_counts.values() if c >= 2)
        if critical_categories >= 2:
            return WarningLevel.AMBER

        # Critical flags present -> YELLOW
        if critical_flags:
            return WarningLevel.YELLOW

        # Any warnings -> still GREEN but monitoring
        if category_counts:
            return WarningLevel.GREEN

        return WarningLevel.GREEN

    def _generate_warning_summary(
        self,
        level: WarningLevel,
        override_flags: List[str],
        critical_flags: List[str],
        category_counts: Dict[str, int]
    ) -> str:
        """Generate human-readable warning summary"""
        parts = []

        if level == WarningLevel.RED:
            parts.append("CRISIS CONDITIONS: Multiple override flags triggered.")
        elif level == WarningLevel.AMBER:
            parts.append("HIGH ALERT: Override or multiple critical flags.")
        elif level == WarningLevel.YELLOW:
            parts.append("ELEVATED: Critical flags require monitoring.")
        else:
            parts.append("NORMAL: No critical warnings.")

        if override_flags:
            parts.append(f"Overrides: {', '.join(override_flags)}")
        if critical_flags:
            parts.append(f"Critical: {', '.join(critical_flags[:5])}")

        return " | ".join(parts)

    # ==========================================
    # CRYPTO HEALTH INDEX (CHI)
    # ==========================================

    def compute_chi(self) -> Tuple[float, Dict[str, float]]:
        """
        Compute Crypto Health Index (CHI) - master composite.

        CHI = weighted average of:
        - Financial Health (subsidy sustainability, revenue quality)
        - User Adoption (DAU trends, stickiness, developers)
        - Valuation (P/E distribution, earnings yield)
        - Tokenomics (float ratio distribution, dilution)
        - Macro Overlay (MRI/LCI adjustment)

        Returns:
            Tuple of (chi_value, component_scores)
        """
        components = {}

        # 1. Financial Health Component
        components['financial_health'] = self._compute_financial_health_score()

        # 2. User Adoption Component
        components['user_adoption'] = self._compute_user_adoption_score()

        # 3. Valuation Component
        components['valuation'] = self._compute_valuation_score()

        # 4. Tokenomics Component
        components['tokenomics'] = self._compute_tokenomics_score()

        # 5. Macro Overlay Component
        components['macro_overlay'] = self._compute_macro_overlay_score()

        # Compute weighted CHI
        chi = 0.0
        for component, weight in self.chi_weights.items():
            score = components.get(component, 0.0)
            chi += score * weight

        return chi, components

    def _compute_financial_health_score(self) -> float:
        """
        Financial health: subsidy sustainability, revenue trends.
        Score: -2 to +2
        """
        query = """
            SELECT
                AVG(CASE WHEN subsidy_score < 0.5 THEN 1
                         WHEN subsidy_score < 1.0 THEN 0.5
                         WHEN subsidy_score < 2.0 THEN 0
                         ELSE -1 END) as subsidy_health,
                AVG(CASE WHEN overall_score >= 70 THEN 1
                         WHEN overall_score >= 50 THEN 0.5
                         WHEN overall_score >= 30 THEN 0
                         ELSE -0.5 END) as score_health
            FROM crypto_scores
            WHERE date = (SELECT MAX(date) FROM crypto_scores)
        """
        try:
            result = pd.read_sql(query, self.conn)
            if result.empty:
                return 0.0
            subsidy = result['subsidy_health'].iloc[0] or 0
            score = result['score_health'].iloc[0] or 0
            return (subsidy + score)  # -2 to +2 range
        except Exception:
            return 0.0

    def _compute_user_adoption_score(self) -> float:
        """
        User adoption: DAU trends, developer activity.
        Score: -2 to +2
        """
        query = """
            SELECT
                AVG(CASE WHEN dau > 10000 THEN 1
                         WHEN dau > 1000 THEN 0.5
                         WHEN dau > 100 THEN 0
                         ELSE -1 END) as dau_health,
                AVG(CASE WHEN active_developers > 20 THEN 1
                         WHEN active_developers > 10 THEN 0.5
                         WHEN active_developers > 3 THEN 0
                         ELSE -1 END) as dev_health
            FROM crypto_scores
            WHERE date = (SELECT MAX(date) FROM crypto_scores)
        """
        try:
            result = pd.read_sql(query, self.conn)
            if result.empty:
                return 0.0
            dau = result['dau_health'].iloc[0] or 0
            dev = result['dev_health'].iloc[0] or 0
            return (dau + dev)  # -2 to +2 range
        except Exception:
            return 0.0

    def _compute_valuation_score(self) -> float:
        """
        Valuation attractiveness across universe.
        Score: -2 to +2
        """
        query = """
            SELECT
                AVG(CASE WHEN pe_ratio < 40 AND pe_ratio > 0 THEN 1
                         WHEN pe_ratio < 100 AND pe_ratio > 0 THEN 0.5
                         WHEN pe_ratio < 200 AND pe_ratio > 0 THEN 0
                         ELSE -0.5 END) as pe_health,
                AVG(CASE WHEN pf_ratio < 100 AND pf_ratio > 0 THEN 1
                         WHEN pf_ratio < 500 AND pf_ratio > 0 THEN 0.5
                         WHEN pf_ratio < 1000 AND pf_ratio > 0 THEN 0
                         ELSE -0.5 END) as pf_health
            FROM crypto_scores
            WHERE date = (SELECT MAX(date) FROM crypto_scores)
        """
        try:
            result = pd.read_sql(query, self.conn)
            if result.empty:
                return 0.0
            pe = result['pe_health'].iloc[0] or 0
            pf = result['pf_health'].iloc[0] or 0
            return (pe + pf)  # -2 to +2 range
        except Exception:
            return 0.0

    def _compute_tokenomics_score(self) -> float:
        """
        Tokenomics health: float ratios, dilution.
        Score: -2 to +2
        """
        query = """
            SELECT
                AVG(CASE WHEN float_ratio > 0.7 THEN 1
                         WHEN float_ratio > 0.5 THEN 0.5
                         WHEN float_ratio > 0.3 THEN 0
                         WHEN float_ratio > 0.2 THEN -0.5
                         ELSE -1 END) as float_health
            FROM crypto_scores
            WHERE date = (SELECT MAX(date) FROM crypto_scores)
        """
        try:
            result = pd.read_sql(query, self.conn)
            if result.empty:
                return 0.0
            float_h = result['float_health'].iloc[0] or 0
            return float_h * 2  # Scale to -2 to +2
        except Exception:
            return 0.0

    def _compute_macro_overlay_score(self) -> float:
        """
        Macro overlay from MRI/LCI.
        Score: -2 to +2
        """
        query = """
            SELECT value, index_id
            FROM lighthouse_indices
            WHERE index_id IN ('MRI', 'LCI')
            AND date = (SELECT MAX(date) FROM lighthouse_indices WHERE index_id = 'MRI')
        """
        try:
            result = pd.read_sql(query, self.conn)
            if result.empty:
                return 0.0

            mri = result[result['index_id'] == 'MRI']['value'].iloc[0] if 'MRI' in result['index_id'].values else 0
            lci = result[result['index_id'] == 'LCI']['value'].iloc[0] if 'LCI' in result['index_id'].values else 0

            # MRI: <0 bullish, >0.5 bearish for crypto
            mri_score = 1 - (mri * 2)  # Inverted: low MRI = high score
            mri_score = max(-1, min(1, mri_score))

            # LCI: >0 supportive, <-0.5 restrictive
            lci_score = lci  # Direct: high LCI = high score
            lci_score = max(-1, min(1, lci_score))

            return mri_score + lci_score  # -2 to +2 range
        except Exception:
            return 0.0

    # ==========================================
    # REGIME CLASSIFICATION
    # ==========================================

    def classify_regime(
        self,
        chi: float,
        warning_level: WarningLevel
    ) -> Tuple[CryptoRegime, str]:
        """
        Classify current crypto regime based on CHI and warnings.

        Returns:
            Tuple of (regime, description)
        """
        if warning_level == WarningLevel.RED:
            return CryptoRegime.CRISIS, "Crisis conditions. Multiple override flags. Maximum defense."

        if warning_level == WarningLevel.AMBER:
            if chi < 0:
                return CryptoRegime.PRE_CRISIS, "Multiple warnings with deteriorating fundamentals. Exit signals."
            else:
                return CryptoRegime.HOLLOW_RALLY, "Prices stable but structural risks elevated. Reduce exposure."

        if chi >= 0.5:
            return CryptoRegime.EXPANSION, "Strong fundamentals, favorable macro. Full allocation."

        if chi >= 0:
            if warning_level == WarningLevel.YELLOW:
                return CryptoRegime.LATE_CYCLE, "Fundamentals peaking, early warnings. Defensive positioning."
            return CryptoRegime.EXPANSION, "Positive fundamentals, normal conditions."

        if chi >= -0.5:
            return CryptoRegime.LATE_CYCLE, "Fundamentals weakening. Reduce new positions."

        return CryptoRegime.PRE_CRISIS, "Poor fundamentals, elevated risk. Exit mode."

    # ==========================================
    # PROTOCOL-LEVEL SCORING
    # ==========================================

    def score_protocols(self) -> Dict[str, ProtocolSystematicScore]:
        """
        Generate systematic scores for each protocol.

        Returns:
            Dictionary of project_id -> ProtocolSystematicScore
        """
        query = """
            SELECT project_id, name, overall_score, financial_score,
                   usage_score, valuation_score, verdict,
                   subsidy_score, float_ratio, dau
            FROM crypto_scores
            WHERE date = (SELECT MAX(date) FROM crypto_scores)
        """

        try:
            df = pd.read_sql(query, self.conn)
        except Exception:
            return {}

        # Get macro overlay
        macro_mult = self._get_macro_multiplier()

        scores = {}
        for _, row in df.iterrows():
            # Fundamental score (from engine)
            fundamental = row['overall_score'] or 50

            # Warning score (inverted: high = fewer warnings)
            warning_score = 100
            if row['subsidy_score'] and row['subsidy_score'] > 2.0:
                warning_score -= 30
            if row['subsidy_score'] and row['subsidy_score'] > 1.0:
                warning_score -= 15
            if row['float_ratio'] and row['float_ratio'] < 0.2:
                warning_score -= 30
            if row['float_ratio'] and row['float_ratio'] < 0.35:
                warning_score -= 15
            if row['dau'] and row['dau'] < 100:
                warning_score -= 20
            warning_score = max(0, warning_score)

            # Momentum score (placeholder - needs time series)
            momentum_score = 50  # Neutral default

            # Macro-adjusted score
            raw_score = (fundamental * 0.50 + warning_score * 0.30 + momentum_score * 0.20)
            macro_adjusted = raw_score * macro_mult

            # Final systematic score
            systematic_score = int(min(100, max(0, macro_adjusted)))

            # Signal determination
            if systematic_score >= 75:
                signal = "BUY"
            elif systematic_score >= 55:
                signal = "HOLD"
            elif systematic_score >= 35:
                signal = "REDUCE"
            else:
                signal = "AVOID"

            # Confidence
            if 'TIER 1' in str(row['verdict']) or 'TIER 2' in str(row['verdict']):
                confidence = "HIGH"
            elif 'AVOID' in str(row['verdict']):
                confidence = "HIGH"  # Confident in avoidance too
            else:
                confidence = "MEDIUM"

            scores[row['project_id']] = ProtocolSystematicScore(
                project_id=row['project_id'],
                name=row['name'],
                fundamental_score=int(fundamental),
                momentum_score=momentum_score,
                warning_score=warning_score,
                macro_adjusted_score=int(macro_adjusted),
                systematic_score=systematic_score,
                systematic_signal=signal,
                confidence=confidence
            )

        return scores

    def _get_macro_multiplier(self) -> float:
        """Get allocation multiplier from macro regime"""
        query = """
            SELECT value FROM lighthouse_indices
            WHERE index_id = 'MRI'
            AND date = (SELECT MAX(date) FROM lighthouse_indices WHERE index_id = 'MRI')
        """
        try:
            result = pd.read_sql(query, self.conn)
            if result.empty:
                return 1.0
            mri = result['value'].iloc[0]

            # MRI-based multiplier for crypto
            if mri < -0.2:
                return 1.2  # Expansion - aggressive
            elif mri < 0.1:
                return 1.0  # Mid-cycle - normal
            elif mri < 0.25:
                return 0.8  # Late cycle - defensive
            elif mri < 0.5:
                return 0.6  # Pre-recession - very defensive
            else:
                return 0.3  # Crisis - minimal
        except Exception:
            return 1.0

    # ==========================================
    # SECTOR ROTATION
    # ==========================================

    def compute_sector_rankings(self) -> Tuple[Dict[str, float], List[str], List[str]]:
        """
        Rank sectors by health and identify rotation signals.

        Returns:
            Tuple of (sector_scores, recommended_sectors, avoid_sectors)
        """
        query = """
            SELECT sector, AVG(overall_score) as avg_score,
                   COUNT(*) as protocol_count,
                   SUM(CASE WHEN verdict LIKE '%TIER 1%' THEN 1 ELSE 0 END) as tier1_count,
                   SUM(CASE WHEN verdict LIKE '%AVOID%' THEN 1 ELSE 0 END) as avoid_count
            FROM crypto_scores
            WHERE date = (SELECT MAX(date) FROM crypto_scores)
            GROUP BY sector
        """

        try:
            df = pd.read_sql(query, self.conn)
        except Exception:
            return {}, [], []

        sector_scores = {}
        for _, row in df.iterrows():
            sector = row['sector']

            # Composite sector score
            base_score = row['avg_score'] or 50

            # Bonus for Tier 1 concentration
            tier1_ratio = (row['tier1_count'] or 0) / max(1, row['protocol_count'])
            tier1_bonus = tier1_ratio * 20

            # Penalty for Avoid concentration
            avoid_ratio = (row['avoid_count'] or 0) / max(1, row['protocol_count'])
            avoid_penalty = avoid_ratio * 30

            sector_scores[sector] = base_score + tier1_bonus - avoid_penalty

        # Sort and identify recommendations
        sorted_sectors = sorted(sector_scores.items(), key=lambda x: x[1], reverse=True)

        recommended = [s for s, score in sorted_sectors if score >= 60][:3]
        avoid = [s for s, score in sorted_sectors if score < 45]

        return sector_scores, recommended, avoid

    # ==========================================
    # MAIN EVALUATION
    # ==========================================

    def evaluate(self) -> CryptoSystematicResult:
        """
        Run complete systematic evaluation.

        Returns:
            CryptoSystematicResult with all systematic signals
        """
        today = datetime.now().strftime('%Y-%m-%d')

        # 1. Compute CHI
        chi, chi_components = self.compute_chi()
        chi_status = get_chi_status(chi)

        # 2. Build metrics for warning system
        metrics = self._gather_warning_metrics()

        # 3. Evaluate warnings
        warning_result = self.evaluate_warnings(metrics)

        # 4. Classify regime
        regime, regime_desc = self.classify_regime(chi, warning_result.overall_level)

        # 5. Score protocols
        protocol_signals = self.score_protocols()

        # 6. Sector rotation
        sector_scores, recommended_sectors, avoid_sectors = self.compute_sector_rankings()

        # 7. Get macro indicators
        mri, lci = self._get_macro_indicators()
        macro_mult = self._get_macro_multiplier()

        # 8. Tier summaries
        tier1 = [p for p, s in protocol_signals.items() if s.systematic_signal == "BUY"]
        tier2 = [p for p, s in protocol_signals.items() if s.systematic_signal == "HOLD"]
        avoid = [p for p, s in protocol_signals.items() if s.systematic_signal == "AVOID"]

        # 9. Systematic allocation recommendation
        base_allocation = 60  # Base crypto allocation %

        # Adjust by regime
        regime_adjustments = {
            CryptoRegime.EXPANSION: 1.2,
            CryptoRegime.LATE_CYCLE: 0.8,
            CryptoRegime.HOLLOW_RALLY: 0.6,
            CryptoRegime.PRE_CRISIS: 0.4,
            CryptoRegime.CRISIS: 0.2,
        }

        systematic_allocation = base_allocation * regime_adjustments.get(regime, 1.0) * macro_mult
        systematic_allocation = min(100, max(0, systematic_allocation))

        # 10. Discretionary notes (the 20%)
        discretionary_notes = self._generate_discretionary_notes(
            regime, warning_result, chi, tier1, avoid
        )

        active_flags = warning_result.override_flags + warning_result.critical_flags

        return CryptoSystematicResult(
            date=today,
            chi=round(chi, 3),
            chi_status=chi_status,
            regime=regime,
            regime_description=regime_desc,
            warning_level=warning_result.overall_level,
            warning_summary=warning_result.summary,
            active_flags=active_flags,
            protocol_signals=protocol_signals,
            sector_rankings=sector_scores,
            recommended_sectors=recommended_sectors,
            avoid_sectors=avoid_sectors,
            mri=mri,
            lci=lci,
            macro_allocation_multiplier=round(macro_mult, 2),
            tier1_protocols=tier1,
            tier2_protocols=tier2,
            avoid_protocols=avoid,
            systematic_allocation=round(systematic_allocation, 1),
            discretionary_notes=discretionary_notes
        )

    def _gather_warning_metrics(self) -> Dict[str, float]:
        """Gather all metrics needed for warning evaluation"""
        metrics = {}

        # From crypto_scores
        query = """
            SELECT
                AVG(subsidy_score) as avg_subsidy,
                AVG(float_ratio) as avg_float,
                AVG(dau) as avg_dau,
                AVG(overall_score) as avg_score,
                SUM(CASE WHEN verdict LIKE '%TIER 1%' THEN 1 ELSE 0 END) as tier1_count
            FROM crypto_scores
            WHERE date = (SELECT MAX(date) FROM crypto_scores)
        """
        try:
            result = pd.read_sql(query, self.conn)
            if not result.empty:
                metrics['subsidy_score'] = result['avg_subsidy'].iloc[0]
                metrics['float_ratio'] = result['avg_float'].iloc[0]
                metrics['dau'] = result['avg_dau'].iloc[0]
                metrics['sector_health_score'] = result['avg_score'].iloc[0]
                metrics['tier1_count'] = result['tier1_count'].iloc[0]
        except Exception:
            pass

        # From lighthouse_indices (macro)
        query = """
            SELECT index_id, value
            FROM lighthouse_indices
            WHERE index_id IN ('MRI', 'LCI')
            AND date = (SELECT MAX(date) FROM lighthouse_indices WHERE index_id = 'MRI')
        """
        try:
            result = pd.read_sql(query, self.conn)
            for _, row in result.iterrows():
                if row['index_id'] == 'MRI':
                    metrics['mri'] = row['value']
                elif row['index_id'] == 'LCI':
                    metrics['lci'] = row['value']
        except Exception:
            pass

        return metrics

    def _get_macro_indicators(self) -> Tuple[Optional[float], Optional[float]]:
        """Get latest MRI and LCI values"""
        query = """
            SELECT index_id, value
            FROM lighthouse_indices
            WHERE index_id IN ('MRI', 'LCI')
            AND date = (SELECT MAX(date) FROM lighthouse_indices WHERE index_id = 'MRI')
        """
        try:
            result = pd.read_sql(query, self.conn)
            mri = result[result['index_id'] == 'MRI']['value'].iloc[0] if 'MRI' in result['index_id'].values else None
            lci = result[result['index_id'] == 'LCI']['value'].iloc[0] if 'LCI' in result['index_id'].values else None
            return mri, lci
        except Exception:
            return None, None

    def _generate_discretionary_notes(
        self,
        regime: CryptoRegime,
        warnings: CryptoWarningResult,
        chi: float,
        tier1: List[str],
        avoid: List[str]
    ) -> List[str]:
        """
        Generate notes for the 20% discretionary component.
        These are things the systematic engine flags for human review.
        """
        notes = []

        # Regime-specific notes
        if regime == CryptoRegime.HOLLOW_RALLY:
            notes.append("HOLLOW RALLY: Systematic says reduce. Discretionary call on timing.")

        if regime == CryptoRegime.LATE_CYCLE:
            notes.append("LATE CYCLE: Watch for narrative exhaustion. Quality > quantity.")

        # Warning-based notes
        if 'MACRO_HOSTILE' in [f.name for f in warnings.flags if f.triggered]:
            notes.append("MACRO: Traditional markets stressed. Crypto correlation elevated.")

        # Tier composition notes
        if len(tier1) < 3:
            notes.append(f"THIN BENCH: Only {len(tier1)} Tier 1 protocols. Be selective.")

        if len(avoid) > len(tier1) * 2:
            notes.append("QUALITY DETERIORATION: More Avoid than Tier 1 signals.")

        # CHI divergence notes
        if chi > 0.5 and warnings.overall_level.value >= WarningLevel.YELLOW.value:
            notes.append("DIVERGENCE: CHI positive but warnings elevated. Investigate.")

        if chi < -0.5 and warnings.overall_level == WarningLevel.GREEN:
            notes.append("DIVERGENCE: CHI negative but no warnings. May be lagging.")

        if not notes:
            notes.append("No significant discretionary flags. Systematic signals clean.")

        return notes

    # ==========================================
    # REPORTING
    # ==========================================

    def print_report(self, result: CryptoSystematicResult):
        """Print formatted systematic report"""
        width = 70

        print()
        print("=" * width)
        print("LIGHTHOUSE MACRO - CRYPTO SYSTEMATIC REPORT")
        print(f"Date: {result.date}")
        print("80% Systematic / 20% Discretionary")
        print("=" * width)

        print("\n--- MASTER COMPOSITE ---")
        print(f"CHI (Crypto Health Index):  {result.chi:>8.3f}  [{result.chi_status}]")
        print(f"Regime:                     {result.regime.value}")
        print(f"                            {result.regime_description}")

        print("\n--- WARNING SYSTEM ---")
        print(f"Level: {result.warning_level.name}")
        print(f"Summary: {result.warning_summary}")
        if result.active_flags:
            print(f"Active Flags: {', '.join(result.active_flags[:5])}")

        print("\n--- MACRO OVERLAY ---")
        print(f"MRI:                        {result.mri or 'N/A':>8}")
        print(f"LCI:                        {result.lci or 'N/A':>8}")
        print(f"Allocation Multiplier:      {result.macro_allocation_multiplier:>8.2f}x")

        print("\n--- SYSTEMATIC ALLOCATION ---")
        print(f"Recommended Crypto %:       {result.systematic_allocation:>8.1f}%")

        print("\n--- TIER SUMMARY ---")
        print(f"Tier 1 (BUY):  {len(result.tier1_protocols):>3} protocols")
        if result.tier1_protocols:
            print(f"               {', '.join(result.tier1_protocols[:5])}")
        print(f"Tier 2 (HOLD): {len(result.tier2_protocols):>3} protocols")
        print(f"Avoid:         {len(result.avoid_protocols):>3} protocols")

        print("\n--- SECTOR ROTATION ---")
        print(f"Recommended: {', '.join(result.recommended_sectors) or 'None'}")
        print(f"Avoid:       {', '.join(result.avoid_sectors) or 'None'}")

        print("\n--- DISCRETIONARY NOTES (20%) ---")
        for note in result.discretionary_notes:
            print(f"  • {note}")

        print()
        print("=" * width)
        print("MACRO, ILLUMINATED.")
        print("=" * width)


# ==========================================
# CLI
# ==========================================

if __name__ == "__main__":
    import sys

    DB_PATH = "/Users/bob/LHM/Data/databases/Lighthouse_Master.db"

    print("Lighthouse Macro Crypto Systematic Engine")
    print("=" * 50)

    conn = sqlite3.connect(DB_PATH)
    engine = CryptoSystematicEngine(conn)

    result = engine.evaluate()
    engine.print_report(result)

    conn.close()
