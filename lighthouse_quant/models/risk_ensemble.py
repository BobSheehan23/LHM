"""
Lighthouse Macro Risk Ensemble
==============================
Combines probability-based recession model with threshold-based warning system
to produce a unified risk assessment that captures both gradual deterioration
AND discontinuity risk.

Philosophy:
    "The Hollow Rally doesn't end because sentiment turns.
     It ends when the system loses capacity to absorb stress."

    The probability model captures gradual regime shifts.
    The warning system captures buffer exhaustion and discontinuity risk.
    The ensemble synthesizes both into actionable intelligence.

Architecture:
    1. Base Rate (Probability Model): Smooth, calibrated recession probability
    2. Discontinuity Risk (Warning System): Binary flags for buffer exhaustion
    3. Ensemble Output: Adjusted probability + regime classification + confidence

Key Innovation:
    When buffers are intact, use the probability model.
    When buffers are depleted, the probability model undersells risk.
    The ensemble adjusts probabilities upward when warning flags trigger.
"""

import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

import sys
sys.path.insert(0, "/Users/bob/LHM")
from lighthouse_quant.config import DB_PATH
from lighthouse_quant.models.recession_probability import (
    RecessionProbabilityModel,
    RecessionProbabilityResult
)
from lighthouse_quant.models.warning_system import (
    WarningSystem,
    WarningLevel,
    SystemWarning,
    ThresholdFlag
)


class RiskRegime(Enum):
    """Unified risk regime classification."""
    EXPANSION = 1       # Low risk, buffers intact
    LATE_CYCLE = 2      # Elevated monitoring, some stress
    HOLLOW_RALLY = 3    # Prices stable but buffers depleted
    PRE_CRISIS = 4      # Multiple stress signals converging
    CRISIS = 5          # Active discontinuity


@dataclass
class EnsembleResult:
    """Complete ensemble risk assessment."""
    date: str

    # Probability outputs
    base_probability: float         # From probability model
    adjusted_probability: float     # After warning adjustments
    discontinuity_premium: float    # Added risk from buffer depletion

    # Regime classification
    regime: RiskRegime
    regime_description: str

    # Component assessments
    probability_regime: str         # From probability model
    warning_level: WarningLevel     # From warning system

    # Confidence and conviction
    model_agreement: str            # AGREE, DIVERGE, SEVERE_DIVERGE
    confidence: str                 # HIGH, MEDIUM, LOW

    # Key drivers
    probability_drivers: Dict[str, float]
    warning_triggers: List[str]

    # Actionable output
    allocation_multiplier: float    # 0.0 to 1.2x
    recommended_actions: List[str]
    invalidation_conditions: List[str]


# ==========================================
# DISCONTINUITY PREMIUM MATRIX
# ==========================================

# How much to adjust probability based on warning level
# Key insight: when buffers are gone, tail risk is underpriced
DISCONTINUITY_PREMIUM = {
    WarningLevel.GREEN: 0.0,
    WarningLevel.YELLOW: 0.05,   # +5% to base probability
    WarningLevel.AMBER: 0.15,   # +15% to base probability
    WarningLevel.RED: 0.30,     # +30% to base probability
}

# Specific flag overrides (additive)
FLAG_PREMIUMS = {
    "RRP_DEPLETED": 0.15,           # Buffer gone = major risk
    "RESERVES_AT_LCLOR": 0.10,      # Funding stress imminent
    "SOFR_EFFR_CRISIS": 0.15,       # Active funding stress
    "LFI_CRITICAL": 0.10,           # Labor in crisis
    "HY_CRISIS": 0.15,              # Credit market stress
    "QUITS_PRERECESSION": 0.05,     # Pre-recessionary labor
    "CLG_MISPRICED": 0.05,          # Credit ignoring reality
}

# Combination effects (non-linear escalation)
COMBINATION_PREMIUMS = [
    {
        "flags": ["RRP_DEPLETED", "RESERVES_BUFFER_THIN"],
        "premium": 0.10,
        "description": "Dual liquidity depletion"
    },
    {
        "flags": ["RRP_DEPLETED", "LFI_ELEVATED"],
        "premium": 0.10,
        "description": "Liquidity + Labor stress convergence"
    },
    {
        "flags": ["CLG_MISPRICED", "HY_COMPLACENT"],
        "premium": 0.05,
        "description": "Credit complacency across metrics"
    },
]


# ==========================================
# REGIME MAPPING
# ==========================================

def determine_regime(
    base_prob: float,
    adjusted_prob: float,
    warning_level: WarningLevel,
    triggered_flags: List[ThresholdFlag]
) -> Tuple[RiskRegime, str]:
    """
    Determine unified risk regime from ensemble inputs.

    Returns:
        Tuple of (RiskRegime, description string)
    """
    # Count override-level flags
    override_count = sum(1 for f in triggered_flags if f.severity == "override" and f.triggered)
    critical_count = sum(1 for f in triggered_flags if f.severity == "critical" and f.triggered)

    # Check for specific conditions
    rrp_depleted = any(f.name == "RRP_DEPLETED" and f.triggered for f in triggered_flags)
    liquidity_stress = any(
        f.category == "liquidity" and f.severity in ("critical", "override") and f.triggered
        for f in triggered_flags
    )

    # CRISIS: Multiple overrides or very high adjusted probability
    if adjusted_prob > 0.70 or override_count >= 2:
        return RiskRegime.CRISIS, "Active crisis conditions. Multiple critical thresholds breached."

    # PRE-CRISIS: High probability or multiple critical flags
    if adjusted_prob > 0.50 or (override_count >= 1 and critical_count >= 2):
        return RiskRegime.PRE_CRISIS, "Pre-crisis regime. Stress signals converging. Defensive positioning required."

    # HOLLOW RALLY: Low base probability but buffers depleted
    # This is the key insight from Horizon
    if base_prob < 0.30 and (rrp_depleted or liquidity_stress):
        return RiskRegime.HOLLOW_RALLY, "Hollow Rally. Prices stable but shock absorbers exhausted. System fragile to stress."

    # LATE_CYCLE: Elevated but not crisis
    if adjusted_prob > 0.25 or warning_level.value >= WarningLevel.YELLOW.value:
        return RiskRegime.LATE_CYCLE, "Late cycle. Buffers depleted. Elevated monitoring required."

    # EXPANSION: All clear
    return RiskRegime.EXPANSION, "Expansion regime. Buffers intact. Normal operations."


def determine_model_agreement(
    base_prob: float,
    warning_level: WarningLevel
) -> str:
    """Determine how much the models agree."""
    # Map warning level to implied probability range
    warning_to_prob = {
        WarningLevel.GREEN: (0.0, 0.15),
        WarningLevel.YELLOW: (0.15, 0.30),
        WarningLevel.AMBER: (0.30, 0.50),
        WarningLevel.RED: (0.50, 1.0),
    }

    low, high = warning_to_prob[warning_level]

    if low <= base_prob <= high:
        return "AGREE"
    elif abs(base_prob - (low + high) / 2) > 0.25:
        return "SEVERE_DIVERGE"
    else:
        return "DIVERGE"


def calculate_allocation_multiplier(regime: RiskRegime, adjusted_prob: float) -> float:
    """
    Calculate regime-based allocation multiplier.

    Returns value between 0.0 (max defensive) and 1.2 (max aggressive).
    """
    regime_base = {
        RiskRegime.EXPANSION: 1.2,
        RiskRegime.LATE_CYCLE: 0.8,
        RiskRegime.HOLLOW_RALLY: 0.5,
        RiskRegime.PRE_CRISIS: 0.3,
        RiskRegime.CRISIS: 0.0,
    }

    base = regime_base[regime]

    # Further adjust based on probability
    if adjusted_prob > 0.50:
        base *= 0.5
    elif adjusted_prob > 0.30:
        base *= 0.8

    return round(max(0.0, min(1.2, base)), 2)


# ==========================================
# ENSEMBLE CLASS
# ==========================================

class RiskEnsemble:
    """
    Lighthouse Macro Risk Ensemble.

    Synthesizes probability model and warning system into unified risk assessment.
    """

    def __init__(self, conn: sqlite3.Connection = None):
        self.conn = conn or sqlite3.connect(DB_PATH)
        self.prob_model = RecessionProbabilityModel(self.conn)
        self.warning_system = WarningSystem(self.conn)

    def evaluate(self, date: str = None) -> EnsembleResult:
        """
        Run full ensemble evaluation.

        Args:
            date: Date to evaluate (default: latest available)

        Returns:
            EnsembleResult with complete assessment
        """
        # Get component outputs
        prob_result = self.prob_model.predict(date)
        warning_result = self.warning_system.evaluate(date)

        # Calculate discontinuity premium
        base_premium = DISCONTINUITY_PREMIUM[warning_result.overall_level]

        # Add flag-specific premiums
        flag_premium = 0.0
        triggered_names = [f.name for f in warning_result.triggered_flags]

        for flag_name, premium in FLAG_PREMIUMS.items():
            if flag_name in triggered_names:
                flag_premium += premium

        # Add combination premiums
        combo_premium = 0.0
        for combo in COMBINATION_PREMIUMS:
            if all(f in triggered_names for f in combo["flags"]):
                combo_premium += combo["premium"]

        # Apply RMP risk modifier (Fed intervention can reduce or increase risk)
        rmp_modifier = 0.0
        if warning_result.rmp_assessment:
            rmp_modifier = warning_result.rmp_assessment.risk_modifier

        # Total discontinuity premium (capped at 0.50, floored at 0.0)
        total_premium = max(0.0, min(0.50, base_premium + flag_premium + combo_premium + rmp_modifier))

        # Adjusted probability (capped at 0.95)
        base_prob = prob_result.probability_12m
        adjusted_prob = min(0.95, base_prob + total_premium)

        # Determine regime
        regime, regime_desc = determine_regime(
            base_prob,
            adjusted_prob,
            warning_result.overall_level,
            warning_result.triggered_flags
        )

        # Model agreement
        agreement = determine_model_agreement(base_prob, warning_result.overall_level)

        # Confidence based on model agreement and data availability
        if agreement == "AGREE" and prob_result.confidence == "HIGH":
            confidence = "HIGH"
        elif agreement == "SEVERE_DIVERGE":
            confidence = "LOW"
        else:
            confidence = "MEDIUM"

        # Allocation multiplier
        alloc_mult = calculate_allocation_multiplier(regime, adjusted_prob)

        # Generate actions
        actions = self._generate_actions(regime, warning_result, adjusted_prob)
        invalidations = self._generate_invalidations(regime, warning_result)

        # Warning trigger descriptions
        warning_triggers = [
            f"{f.name}: {f.description}"
            for f in warning_result.triggered_flags
            if f.severity in ("critical", "override")
        ]

        return EnsembleResult(
            date=prob_result.date,
            base_probability=base_prob,
            adjusted_probability=adjusted_prob,
            discontinuity_premium=total_premium,
            regime=regime,
            regime_description=regime_desc,
            probability_regime=prob_result.regime,
            warning_level=warning_result.overall_level,
            model_agreement=agreement,
            confidence=confidence,
            probability_drivers=prob_result.key_drivers,
            warning_triggers=warning_triggers,
            allocation_multiplier=alloc_mult,
            recommended_actions=actions,
            invalidation_conditions=invalidations,
        )

    def _generate_actions(
        self,
        regime: RiskRegime,
        warning: SystemWarning,
        adjusted_prob: float
    ) -> List[str]:
        """Generate recommended actions based on regime."""
        actions = []

        if regime == RiskRegime.EXPANSION:
            actions.append("Maintain strategic equity allocation")
            actions.append("Continue normal monitoring cadence")
            actions.append("Review positions quarterly")

        elif regime == RiskRegime.LATE_CYCLE:
            actions.append("Reduce beta exposure moderately")
            actions.append("Increase quality tilt in equity holdings")
            actions.append("Review tail hedges monthly")
            actions.append("Monitor weekly jobless claims")

        elif regime == RiskRegime.HOLLOW_RALLY:
            actions.append("Position defensively despite calm surface")
            actions.append("Maintain elevated cash/liquidity (20-30%)")
            actions.append("Implement volatility hedges while cheap")
            actions.append("Accept near-term underperformance vs momentum")
            actions.append("Monitor funding markets daily")
            actions.append("Prepare rebalancing shopping list for stress")

        elif regime == RiskRegime.PRE_CRISIS:
            actions.append("Maximum defensive positioning")
            actions.append("Reduce gross exposure significantly")
            actions.append("Ensure portfolio liquidity for redemptions")
            actions.append("Implement explicit tail hedges")
            actions.append("Daily monitoring of all stress indicators")

        elif regime == RiskRegime.CRISIS:
            actions.append("Capital preservation mode")
            actions.append("Minimize risk exposure")
            actions.append("Maintain liquidity for opportunities")
            actions.append("Watch for capitulation signals")
            actions.append("Prepare for tactical re-entry on exhaustion")

        return actions

    def _generate_invalidations(
        self,
        regime: RiskRegime,
        warning: SystemWarning
    ) -> List[str]:
        """Generate conditions that would invalidate the regime call."""
        invalidations = []

        if regime in (RiskRegime.HOLLOW_RALLY, RiskRegime.PRE_CRISIS, RiskRegime.CRISIS):
            invalidations.append("Quits rate rebounds above 2.3%")
            invalidations.append("RRP rebuilds above $250B")
            invalidations.append("Initial claims sustained below 225K")
            invalidations.append("HY spreads widen to >400bps (risk priced)")

        if regime == RiskRegime.LATE_CYCLE:
            invalidations.append("MRI falls below -0.10 (expansion)")
            invalidations.append("Employment diffusion rebounds above 55%")
            invalidations.append("Credit-Labor Gap normalizes above -0.5")

        if regime == RiskRegime.EXPANSION:
            invalidations.append("Quits rate falls below 2.3%")
            invalidations.append("RRP depleted below $250B")
            invalidations.append("Initial claims rise above 250K")

        return invalidations

    def print_report(self, result: EnsembleResult = None):
        """Print formatted ensemble report."""
        if result is None:
            result = self.evaluate()

        regime_icons = {
            RiskRegime.EXPANSION: "🟢",
            RiskRegime.LATE_CYCLE: "🟡",
            RiskRegime.HOLLOW_RALLY: "🟠",
            RiskRegime.PRE_CRISIS: "🔴",
            RiskRegime.CRISIS: "⛔",
        }

        print("\n" + "=" * 70)
        print("LIGHTHOUSE MACRO RISK ENSEMBLE")
        print(f"Date: {result.date}")
        print("=" * 70)

        print(f"\n{regime_icons[result.regime]} REGIME: {result.regime.name}")
        print(f"   {result.regime_description}")

        print("\n" + "-" * 70)
        print("PROBABILITY ASSESSMENT")
        print("-" * 70)
        print(f"   Base Recession Probability:     {result.base_probability:.1%}")
        print(f"   Discontinuity Premium:          +{result.discontinuity_premium:.1%}")
        print(f"   Adjusted Probability:           {result.adjusted_probability:.1%}")

        print("\n" + "-" * 70)
        print("MODEL SYNTHESIS")
        print("-" * 70)
        print(f"   Probability Model Says:   {result.probability_regime}")
        print(f"   Warning System Says:      {result.warning_level.name}")
        print(f"   Model Agreement:          {result.model_agreement}")
        print(f"   Ensemble Confidence:      {result.confidence}")

        if result.model_agreement == "SEVERE_DIVERGE":
            print(f"\n   ⚠️  SEVERE DIVERGENCE: Probability model missing discontinuity risk!")

        if result.warning_triggers:
            print("\n" + "-" * 70)
            print("CRITICAL WARNING TRIGGERS")
            print("-" * 70)
            for trigger in result.warning_triggers:
                print(f"   🔴 {trigger}")

        print("\n" + "-" * 70)
        print("POSITIONING GUIDANCE")
        print("-" * 70)
        print(f"   Allocation Multiplier: {result.allocation_multiplier}x")
        print(f"\n   Recommended Actions:")
        for i, action in enumerate(result.recommended_actions, 1):
            print(f"   {i}. {action}")

        print(f"\n   Invalidation Conditions:")
        for cond in result.invalidation_conditions:
            print(f"   • {cond}")

        print("\n" + "=" * 70)

        return result


def compute_ensemble_risk(conn: sqlite3.Connection = None) -> pd.DataFrame:
    """
    Compute ensemble risk for output to database.

    Returns DataFrame with columns suitable for lighthouse_indices.
    """
    ensemble = RiskEnsemble(conn)
    result = ensemble.evaluate()

    return pd.DataFrame([{
        "date": result.date,
        "index_id": "ENSEMBLE_RISK",
        "value": result.adjusted_probability,
        "status": result.regime.name,
    }, {
        "date": result.date,
        "index_id": "DISCONTINUITY_PREMIUM",
        "value": result.discontinuity_premium,
        "status": f"+{result.discontinuity_premium:.1%}",
    }, {
        "date": result.date,
        "index_id": "ALLOC_MULTIPLIER",
        "value": result.allocation_multiplier,
        "status": f"{result.allocation_multiplier}x",
    }])


# CLI interface
if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    ensemble = RiskEnsemble(conn)
    ensemble.print_report()
    conn.close()
