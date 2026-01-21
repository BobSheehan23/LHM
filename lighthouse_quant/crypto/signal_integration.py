"""
LIGHTHOUSE MACRO - CRYPTO SIGNAL INTEGRATION
=============================================
Integrate systematic signals into the unified crypto scoring system.

The 80/20 Split:
    - 80% Systematic: CHI, ML signals, momentum, regime, warnings
    - 20% Discretionary: Fundamental verdicts, red flags, sector tilts

This module combines all systematic components into actionable signals
that augment (not replace) the existing fundamental analysis.

Output: 24-Point Protocol Score
    - Technical (0-8): Momentum, mean reversion, trend
    - Fundamental (0-8): Health classifier, CHI contribution
    - Microstructure (0-8): Tokenomics, liquidity, regime fit
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum
import sqlite3
import logging

from .systematic import CryptoSystematicEngine, CryptoRegime, WarningFlag, WarningLevel
from .ml_models import CryptoMLEngine

logger = logging.getLogger(__name__)


# ==========================================
# SCORE COMPONENTS
# ==========================================

class SignalStrength(Enum):
    """Signal strength levels."""
    STRONG_SELL = -2
    SELL = -1
    NEUTRAL = 0
    BUY = 1
    STRONG_BUY = 2


@dataclass
class TechnicalScore:
    """Technical component of 24-point score (0-8)."""
    momentum_score: float = 0.0  # 0-3
    mean_reversion_score: float = 0.0  # 0-2
    trend_score: float = 0.0  # 0-3

    @property
    def total(self) -> float:
        return min(8, self.momentum_score + self.mean_reversion_score + self.trend_score)

    def breakdown(self) -> Dict:
        return {
            'momentum': self.momentum_score,
            'mean_reversion': self.mean_reversion_score,
            'trend': self.trend_score,
            'total': self.total
        }


@dataclass
class FundamentalScore:
    """Fundamental component of 24-point score (0-8)."""
    health_score: float = 0.0  # 0-4 (from ML classifier)
    chi_contribution: float = 0.0  # 0-2 (from CHI)
    verdict_score: float = 0.0  # 0-2 (from existing verdicts)

    @property
    def total(self) -> float:
        return min(8, self.health_score + self.chi_contribution + self.verdict_score)

    def breakdown(self) -> Dict:
        return {
            'health': self.health_score,
            'chi': self.chi_contribution,
            'verdict': self.verdict_score,
            'total': self.total
        }


@dataclass
class MicrostructureScore:
    """Microstructure component of 24-point score (0-8)."""
    tokenomics_score: float = 0.0  # 0-3 (float ratio, emissions)
    liquidity_score: float = 0.0  # 0-3 (volume, depth)
    regime_fit_score: float = 0.0  # 0-2 (alignment with crypto regime)

    @property
    def total(self) -> float:
        return min(8, self.tokenomics_score + self.liquidity_score + self.regime_fit_score)

    def breakdown(self) -> Dict:
        return {
            'tokenomics': self.tokenomics_score,
            'liquidity': self.liquidity_score,
            'regime_fit': self.regime_fit_score,
            'total': self.total
        }


@dataclass
class IntegratedProtocolScore:
    """Complete 24-point integrated score for a protocol."""
    project_id: str
    date: str

    # Component scores
    technical: TechnicalScore = field(default_factory=TechnicalScore)
    fundamental: FundamentalScore = field(default_factory=FundamentalScore)
    microstructure: MicrostructureScore = field(default_factory=MicrostructureScore)

    # Composite
    @property
    def total_score(self) -> float:
        """Total 24-point score."""
        return self.technical.total + self.fundamental.total + self.microstructure.total

    # Signal derivation
    @property
    def signal(self) -> SignalStrength:
        """Derive signal from total score."""
        score = self.total_score
        if score >= 18:
            return SignalStrength.STRONG_BUY
        elif score >= 14:
            return SignalStrength.BUY
        elif score >= 10:
            return SignalStrength.NEUTRAL
        elif score >= 6:
            return SignalStrength.SELL
        else:
            return SignalStrength.STRONG_SELL

    # Tier classification (matches existing TIER 1/2/etc)
    @property
    def tier(self) -> str:
        """Map score to tier classification."""
        score = self.total_score
        if score >= 16:
            return "TIER 1 (Accumulate)"
        elif score >= 12:
            return "TIER 2 (Hold)"
        elif score >= 8:
            return "NEUTRAL (Watch)"
        elif score >= 5:
            return "CAUTION"
        else:
            return "AVOID"

    # Warnings
    active_warnings: List[WarningFlag] = field(default_factory=list)

    @property
    def has_override_warning(self) -> bool:
        """Check if any override-level warnings are active."""
        return any(w.severity == 'OVERRIDE' for w in self.active_warnings)

    def to_dict(self) -> Dict:
        """Convert to dictionary for storage/display."""
        return {
            'project_id': self.project_id,
            'date': self.date,
            'total_score': self.total_score,
            'technical_score': self.technical.total,
            'fundamental_score': self.fundamental.total,
            'microstructure_score': self.microstructure.total,
            'signal': self.signal.name,
            'tier': self.tier,
            'has_override': self.has_override_warning,
            'warning_count': len(self.active_warnings),
            'technical_breakdown': self.technical.breakdown(),
            'fundamental_breakdown': self.fundamental.breakdown(),
            'microstructure_breakdown': self.microstructure.breakdown(),
        }


# ==========================================
# INTEGRATION ENGINE
# ==========================================

class CryptoSignalIntegration:
    """
    Master integration class for crypto systematic signals.

    Combines:
        - CryptoSystematicEngine (CHI, warnings, regime)
        - CryptoMLEngine (momentum, reversion, health, rotation)
        - Existing fundamental verdicts

    Into a unified 24-point scoring system.
    """

    def __init__(self, conn: sqlite3.Connection):
        """
        Initialize signal integration.

        Args:
            conn: SQLite connection to database
        """
        self.conn = conn
        self.systematic = CryptoSystematicEngine(conn)
        self.ml_engine = CryptoMLEngine(conn)
        self._ml_signals_cache = None  # Cache ML signals for batch processing

    def compute_protocol_score(
        self,
        project_id: str,
        date: str = None
    ) -> IntegratedProtocolScore:
        """
        Compute full 24-point integrated score for a protocol.

        Args:
            project_id: Protocol to score
            date: Date for scoring (default: today)

        Returns:
            IntegratedProtocolScore with all components
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        score = IntegratedProtocolScore(project_id=project_id, date=date)

        # Load protocol data
        protocol_data = self._load_protocol_data(project_id)
        if protocol_data is None:
            return score

        # 1. TECHNICAL SCORE (0-8)
        score.technical = self._compute_technical_score(project_id, protocol_data)

        # 2. FUNDAMENTAL SCORE (0-8)
        score.fundamental = self._compute_fundamental_score(project_id, protocol_data)

        # 3. MICROSTRUCTURE SCORE (0-8)
        score.microstructure = self._compute_microstructure_score(project_id, protocol_data)

        # 4. WARNINGS
        score.active_warnings = self._get_protocol_warnings(project_id, protocol_data)

        return score

    def _get_ml_signals(self):
        """Get or compute ML signals (cached)."""
        if self._ml_signals_cache is None:
            try:
                self._ml_signals_cache = self.ml_engine.generate_signals()
            except Exception as e:
                logger.warning(f"Could not generate ML signals: {e}")
                self._ml_signals_cache = None
        return self._ml_signals_cache

    def _compute_technical_score(
        self,
        project_id: str,
        data: Dict
    ) -> TechnicalScore:
        """Compute technical component (momentum, reversion, trend)."""
        tech = TechnicalScore()

        try:
            # Get ML signals (cached)
            ml_signals = self._get_ml_signals()

            # Get protocol-specific time series signals
            if ml_signals and project_id in ml_signals.protocol_timeseries:
                ts = ml_signals.protocol_timeseries[project_id]

                # Momentum (0-3) from momentum score
                mom_score = ts.momentum_score / 100  # Normalize 0-100 to 0-1
                if mom_score > 0.7:
                    tech.momentum_score = 3.0
                elif mom_score > 0.5:
                    tech.momentum_score = 2.0
                elif mom_score > 0.3:
                    tech.momentum_score = 1.0
                else:
                    tech.momentum_score = 0.0

                # Mean Reversion (0-2) from reversion score
                rev_score = ts.reversion_score / 100  # Normalize 0-100 to 0-1
                if rev_score > 0.6:
                    tech.mean_reversion_score = 2.0
                elif rev_score > 0.4:
                    tech.mean_reversion_score = 1.0
                else:
                    tech.mean_reversion_score = 0.5

                # Trend (0-3) from trend info
                if ts.revenue_trend == 'ACCELERATING':
                    tech.trend_score = 3.0
                elif ts.revenue_trend == 'STABLE':
                    tech.trend_score = 2.0
                else:
                    tech.trend_score = 0.5
            else:
                # Fallback: use price history if ML signals unavailable
                price_data = data.get('price_history', pd.Series())
                if len(price_data) >= 50:
                    current = price_data.iloc[-1] if len(price_data) > 0 else 0
                    ma20 = price_data.tail(20).mean()
                    ma50 = price_data.tail(50).mean()

                    if current > ma20 > ma50:
                        tech.trend_score = 3.0
                    elif current > ma50:
                        tech.trend_score = 2.0
                    elif current > ma20:
                        tech.trend_score = 1.0
                    else:
                        tech.trend_score = 0.0

        except Exception as e:
            logger.debug(f"Technical score error for {project_id}: {e}")

        return tech

    def _compute_fundamental_score(
        self,
        project_id: str,
        data: Dict
    ) -> FundamentalScore:
        """Compute fundamental component (health, CHI, verdict)."""
        fund = FundamentalScore()

        try:
            # Health from ML classifier (0-4)
            ml_signals = self._get_ml_signals()
            if ml_signals and project_id in ml_signals.protocol_predictions:
                pred = ml_signals.protocol_predictions[project_id]
                health_prob = pred.health_probability
                fund.health_score = health_prob * 4.0

            # CHI contribution (0-2)
            chi_result = self.systematic.compute_chi()
            if chi_result is not None:
                chi_value = chi_result[0] if isinstance(chi_result, tuple) else chi_result
                # Scale CHI (-2 to +2) to (0-2)
                fund.chi_contribution = max(0, min(2, (chi_value + 2) / 2))

            # Existing verdict (0-2)
            verdict = data.get('verdict', '')
            verdict_map = {
                'TIER 1': 2.0,
                'TIER 2': 1.5,
                'NEUTRAL': 1.0,
                'CAUTION': 0.5,
                'AVOID': 0.0
            }
            for v_key, v_score in verdict_map.items():
                if v_key in verdict:
                    fund.verdict_score = v_score
                    break

        except Exception as e:
            logger.debug(f"Fundamental score error for {project_id}: {e}")

        return fund

    def _compute_microstructure_score(
        self,
        project_id: str,
        data: Dict
    ) -> MicrostructureScore:
        """Compute microstructure component (tokenomics, liquidity, regime)."""
        micro = MicrostructureScore()

        try:
            # Tokenomics (0-3)
            float_ratio = data.get('float_ratio', 0)
            subsidy_score = data.get('subsidy_score', float('inf'))

            # Good float = high circulating vs FDV
            if float_ratio > 0.7:
                micro.tokenomics_score += 1.5
            elif float_ratio > 0.5:
                micro.tokenomics_score += 1.0
            elif float_ratio > 0.3:
                micro.tokenomics_score += 0.5

            # Low subsidy = sustainable
            if subsidy_score < 1.0:
                micro.tokenomics_score += 1.5
            elif subsidy_score < 3.0:
                micro.tokenomics_score += 1.0
            elif subsidy_score < 5.0:
                micro.tokenomics_score += 0.5

            # Liquidity (0-3)
            volume = data.get('trading_volume', 0)
            mcap = data.get('market_cap', 1)
            volume_ratio = volume / mcap if mcap > 0 else 0

            if volume_ratio > 0.10:
                micro.liquidity_score = 3.0
            elif volume_ratio > 0.05:
                micro.liquidity_score = 2.0
            elif volume_ratio > 0.02:
                micro.liquidity_score = 1.0
            else:
                micro.liquidity_score = 0.5

            # Regime fit (0-2)
            chi_result = self.systematic.compute_chi()
            chi_value = chi_result[0] if isinstance(chi_result, tuple) else (chi_result or 0)
            regime, _ = self.systematic.classify_regime(chi_value, WarningLevel.GREEN)
            sector = data.get('sector', '')

            # Sector-regime alignment
            regime_sector_fit = {
                CryptoRegime.EXPANSION: ['defi_dex', 'layer1', 'defi_derivatives'],
                CryptoRegime.LATE_CYCLE: ['stablecoins', 'liquid_staking', 'defi_lending'],
                CryptoRegime.HOLLOW_RALLY: [],  # Nothing fits well
                CryptoRegime.PRE_CRISIS: ['stablecoins'],
                CryptoRegime.CRISIS: [],
            }

            favorable_sectors = regime_sector_fit.get(regime, [])
            if sector in favorable_sectors:
                micro.regime_fit_score = 2.0
            elif regime in [CryptoRegime.EXPANSION, CryptoRegime.LATE_CYCLE]:
                micro.regime_fit_score = 1.0
            else:
                micro.regime_fit_score = 0.0

        except Exception as e:
            logger.debug(f"Microstructure score error for {project_id}: {e}")

        return micro

    def _get_protocol_warnings(
        self,
        project_id: str,
        data: Dict
    ) -> List[WarningFlag]:
        """Get active warnings for a protocol based on its data."""
        warnings = []

        try:
            # Build protocol-specific metrics
            metrics = {
                'subsidy_score': data.get('subsidy_score'),
                'float_ratio': data.get('float_ratio'),
                'dau': data.get('dau'),
                'pe_ratio': data.get('pe_ratio'),
                'pf_ratio': data.get('pf_ratio'),
            }

            # Evaluate warnings using the systematic engine
            warning_result = self.systematic.evaluate_warnings(metrics)

            # Return triggered warnings
            for flag in warning_result.flags:
                if flag.triggered:
                    warnings.append(flag)

        except Exception as e:
            logger.debug(f"Warning check error for {project_id}: {e}")

        return warnings

    def _load_protocol_data(self, project_id: str) -> Optional[Dict]:
        """Load all relevant data for a protocol."""
        try:
            c = self.conn.cursor()

            # Get latest score
            c.execute("""
                SELECT * FROM crypto_scores
                WHERE project_id = ?
                ORDER BY date DESC LIMIT 1
            """, (project_id,))
            row = c.fetchone()

            if not row:
                return None

            # Map to dict
            columns = [d[0] for d in c.description]
            data = dict(zip(columns, row))

            # Get price history
            c.execute("""
                SELECT date, value FROM crypto_metrics
                WHERE project_id = ? AND metric_id = 'price'
                ORDER BY date
            """, (project_id,))
            price_rows = c.fetchall()
            if price_rows:
                data['price_history'] = pd.Series(
                    [r[1] for r in price_rows],
                    index=pd.to_datetime([r[0] for r in price_rows])
                )
            else:
                data['price_history'] = pd.Series()

            return data

        except Exception as e:
            logger.error(f"Error loading data for {project_id}: {e}")
            return None

    def score_all_protocols(self) -> pd.DataFrame:
        """
        Compute integrated scores for all protocols.

        Returns:
            DataFrame with scores for all protocols
        """
        c = self.conn.cursor()
        c.execute("SELECT DISTINCT project_id FROM crypto_scores")
        protocols = [row[0] for row in c.fetchall()]

        results = []
        for pid in protocols:
            score = self.compute_protocol_score(pid)
            results.append(score.to_dict())

        return pd.DataFrame(results)

    def get_tier1_systematic(self) -> List[str]:
        """Get protocols that qualify as Tier 1 by systematic scoring."""
        scores_df = self.score_all_protocols()
        tier1 = scores_df[
            (scores_df['total_score'] >= 16) &
            (~scores_df['has_override'])
        ]
        return tier1['project_id'].tolist()

    def generate_daily_signals(self) -> Dict:
        """
        Generate daily signal summary.

        Returns:
            Dict with regime, CHI, top picks, warnings
        """
        # CHI
        chi_result = self.systematic.compute_chi()
        chi_value = chi_result[0] if isinstance(chi_result, tuple) else (chi_result or 0)

        # Gather metrics for warnings
        metrics = self.systematic._gather_warning_metrics()
        warning_result = self.systematic.evaluate_warnings(metrics)

        # Regime
        regime, _ = self.systematic.classify_regime(chi_value, warning_result.overall_level)

        # All scores
        scores_df = self.score_all_protocols()

        # Top picks (Tier 1, no overrides)
        top_picks = scores_df[
            (scores_df['total_score'] >= 16) &
            (~scores_df['has_override'])
        ].sort_values('total_score', ascending=False)

        # Critical warnings
        critical_warnings = warning_result.critical_flags + warning_result.override_flags

        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'regime': regime.value if regime else 'UNKNOWN',
            'chi': chi_value,
            'chi_status': 'HEALTHY' if chi_value > 0.5 else 'STRESSED' if chi_value < 0 else 'NEUTRAL',
            'top_picks': top_picks['project_id'].tolist()[:5] if not top_picks.empty else [],
            'tier1_count': len(top_picks),
            'avoid_count': len(scores_df[scores_df['total_score'] < 6]),
            'warning_count': len([f for f in warning_result.flags if f.triggered]),
            'critical_warnings': critical_warnings,
            'scores': scores_df.to_dict('records')
        }

    def write_scores_to_db(self):
        """Write integrated scores to database for historical tracking."""
        scores_df = self.score_all_protocols()
        date = datetime.now().strftime('%Y-%m-%d')

        c = self.conn.cursor()

        # Create table if not exists
        c.execute("""CREATE TABLE IF NOT EXISTS crypto_integrated_scores (
            project_id TEXT,
            date TEXT,
            total_score REAL,
            technical_score REAL,
            fundamental_score REAL,
            microstructure_score REAL,
            signal TEXT,
            tier TEXT,
            has_override INTEGER,
            warning_count INTEGER,
            PRIMARY KEY (project_id, date)
        )""")

        # Insert scores
        for _, row in scores_df.iterrows():
            c.execute("""INSERT OR REPLACE INTO crypto_integrated_scores
                        VALUES (?,?,?,?,?,?,?,?,?,?)""",
                     (row['project_id'], date, row['total_score'],
                      row['technical_score'], row['fundamental_score'],
                      row['microstructure_score'], row['signal'],
                      row['tier'], int(row['has_override']), row['warning_count']))

        self.conn.commit()
        logger.info(f"Wrote {len(scores_df)} integrated scores to database")


# ==========================================
# CLI
# ==========================================

if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Crypto Signal Integration")
    parser.add_argument("--db", type=str,
                       default="/Users/bob/LHM/Data/databases/Lighthouse_Master.db",
                       help="Database path")
    parser.add_argument("--protocol", type=str, help="Score specific protocol")
    parser.add_argument("--all", action="store_true", help="Score all protocols")
    parser.add_argument("--signals", action="store_true", help="Generate daily signals")
    parser.add_argument("--write", action="store_true", help="Write scores to database")

    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    integration = CryptoSignalIntegration(conn)

    if args.protocol:
        score = integration.compute_protocol_score(args.protocol)
        print(f"\n{args.protocol} - Integrated Score: {score.total_score:.1f}/24")
        print(f"  Technical: {score.technical.total:.1f}/8")
        print(f"  Fundamental: {score.fundamental.total:.1f}/8")
        print(f"  Microstructure: {score.microstructure.total:.1f}/8")
        print(f"  Signal: {score.signal.name}")
        print(f"  Tier: {score.tier}")
        if score.active_warnings:
            print(f"  Warnings: {len(score.active_warnings)}")

    elif args.all:
        scores = integration.score_all_protocols()
        print(scores[['project_id', 'total_score', 'signal', 'tier']].to_string())

    elif args.signals:
        signals = integration.generate_daily_signals()
        print(json.dumps(signals, indent=2, default=str))

    if args.write:
        integration.write_scores_to_db()
        print("Scores written to database.")

    conn.close()
