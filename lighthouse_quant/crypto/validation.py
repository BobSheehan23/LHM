"""
LIGHTHOUSE MACRO - CRYPTO SYSTEMATIC VALIDATION FRAMEWORK
=========================================================
Backtest and validate systematic crypto signals against historical regimes.

The 80/20 Rule: 80% systematic (this framework) + 20% discretionary overlay.

Key Validation Targets:
    1. Bear Market Detection: Did CHI/warnings flag before major drawdowns?
    2. Recovery Identification: Did momentum models catch bottoms?
    3. Protocol Health: Did health classifier avoid blowups?
    4. Regime Accuracy: Did regime classification match actual market conditions?

Historical Crypto Bear Markets for Validation:
    - 2018 Crypto Winter (Jan 2018 - Dec 2018): -85% BTC drawdown
    - March 2020 COVID Crash: -50% in days
    - May 2021 China Ban: -50% drawdown
    - 2022 Bear (Luna/FTX): -75% drawdown, multiple protocol failures
    - 2024 Corrections: Various 20-30% drawdowns
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import sqlite3
import logging

logger = logging.getLogger(__name__)


# ==========================================
# HISTORICAL EVENT DEFINITIONS
# ==========================================

@dataclass
class CryptoEvent:
    """Historical crypto event for validation."""
    name: str
    start_date: str
    end_date: str
    event_type: str  # 'bear_market', 'crash', 'protocol_failure', 'recovery'
    peak_drawdown: float  # As decimal (0.85 = 85% drawdown)
    affected_protocols: List[str] = field(default_factory=list)
    description: str = ""


# Major historical events for validation
VALIDATION_EVENTS = [
    CryptoEvent(
        name="2018 Crypto Winter",
        start_date="2018-01-08",
        end_date="2018-12-15",
        event_type="bear_market",
        peak_drawdown=0.85,
        affected_protocols=["ethereum", "all"],
        description="Post-ICO bubble burst, 85% drawdown"
    ),
    CryptoEvent(
        name="March 2020 COVID Crash",
        start_date="2020-03-08",
        end_date="2020-03-23",
        event_type="crash",
        peak_drawdown=0.50,
        affected_protocols=["all"],
        description="Global COVID panic, 50% crash in days"
    ),
    CryptoEvent(
        name="May 2021 China Ban",
        start_date="2021-05-12",
        end_date="2021-07-20",
        event_type="crash",
        peak_drawdown=0.50,
        affected_protocols=["all"],
        description="China mining ban, 50% correction"
    ),
    CryptoEvent(
        name="Luna Collapse",
        start_date="2022-05-07",
        end_date="2022-05-13",
        event_type="protocol_failure",
        peak_drawdown=0.99,
        affected_protocols=["terra-luna"],
        description="UST depeg, algorithmic stablecoin failure"
    ),
    CryptoEvent(
        name="3AC/Celsius Contagion",
        start_date="2022-06-12",
        end_date="2022-06-18",
        event_type="crash",
        peak_drawdown=0.35,
        affected_protocols=["aave", "compound", "all"],
        description="CeFi contagion from 3AC collapse"
    ),
    CryptoEvent(
        name="FTX Collapse",
        start_date="2022-11-06",
        end_date="2022-11-14",
        event_type="protocol_failure",
        peak_drawdown=0.25,
        affected_protocols=["solana", "all"],
        description="FTX fraud revealed, SOL ecosystem hit hardest"
    ),
    CryptoEvent(
        name="2023 Recovery",
        start_date="2023-01-01",
        end_date="2023-12-31",
        event_type="recovery",
        peak_drawdown=-0.50,  # Negative = gain
        affected_protocols=["all"],
        description="Post-FTX recovery, selective strength"
    ),
]


# ==========================================
# VALIDATION METRICS
# ==========================================

@dataclass
class ValidationResult:
    """Results from validating signals against an event."""
    event: CryptoEvent

    # Timing metrics
    warning_lead_days: Optional[int] = None  # Days warning preceded event
    signal_at_bottom: bool = False  # Did we signal buy at/near bottom?

    # Accuracy metrics
    regime_correct: bool = False  # Did regime match event type?
    health_flagged: List[str] = field(default_factory=list)  # Protocols flagged before failure

    # Performance metrics
    hypothetical_drawdown_avoided: float = 0.0  # How much DD avoided vs buy-hold
    recovery_capture: float = 0.0  # % of recovery captured

    # Signal quality
    false_positives: int = 0  # Warnings that didn't precede events
    false_negatives: int = 0  # Events not flagged by warnings

    def score(self) -> float:
        """Composite validation score (0-100)."""
        score = 0.0

        # Warning timing (0-30 points)
        if self.warning_lead_days is not None:
            if self.warning_lead_days >= 7:
                score += 30
            elif self.warning_lead_days >= 3:
                score += 20
            elif self.warning_lead_days >= 1:
                score += 10

        # Regime accuracy (0-20 points)
        if self.regime_correct:
            score += 20

        # Drawdown avoidance (0-30 points)
        score += min(30, self.hypothetical_drawdown_avoided * 60)

        # Recovery capture (0-20 points)
        score += self.recovery_capture * 20

        return score


@dataclass
class BacktestResults:
    """Full backtest results across all events."""
    event_results: List[ValidationResult]

    # Aggregate metrics
    total_events: int = 0
    events_flagged: int = 0
    avg_warning_lead_days: float = 0.0
    total_dd_avoided: float = 0.0
    total_recovery_captured: float = 0.0

    # Model-specific metrics
    chi_accuracy: float = 0.0  # CHI regime accuracy
    momentum_accuracy: float = 0.0  # Momentum model accuracy
    health_accuracy: float = 0.0  # Health classifier accuracy

    def overall_score(self) -> float:
        """Overall validation score (0-100)."""
        if not self.event_results:
            return 0.0
        return np.mean([r.score() for r in self.event_results])

    def summary(self) -> Dict:
        """Summary statistics."""
        return {
            'overall_score': self.overall_score(),
            'events_tested': self.total_events,
            'detection_rate': self.events_flagged / max(1, self.total_events),
            'avg_lead_days': self.avg_warning_lead_days,
            'dd_avoided': self.total_dd_avoided,
            'recovery_captured': self.total_recovery_captured,
            'chi_accuracy': self.chi_accuracy,
            'momentum_accuracy': self.momentum_accuracy,
            'health_accuracy': self.health_accuracy,
        }


# ==========================================
# VALIDATION ENGINE
# ==========================================

class CryptoValidationEngine:
    """
    Validate systematic crypto signals against historical events.

    This is the "prove it works" layer for the 80% systematic framework.
    """

    def __init__(self, conn: sqlite3.Connection):
        """
        Initialize validation engine.

        Args:
            conn: SQLite connection to database with crypto data
        """
        self.conn = conn

    def validate_event(
        self,
        event: CryptoEvent,
        chi_series: pd.Series,
        warnings_df: pd.DataFrame,
        regime_series: pd.Series,
        momentum_signals: pd.DataFrame,
        health_scores: pd.DataFrame
    ) -> ValidationResult:
        """
        Validate signals against a single historical event.

        Args:
            event: Historical event to validate against
            chi_series: CHI values indexed by date
            warnings_df: Warning flags with dates
            regime_series: Regime classifications by date
            momentum_signals: Momentum model signals
            health_scores: Protocol health scores

        Returns:
            ValidationResult with all metrics
        """
        result = ValidationResult(event=event)

        event_start = pd.to_datetime(event.start_date)
        event_end = pd.to_datetime(event.end_date)

        # 1. Check warning lead time
        pre_event_window = chi_series.loc[:event_start].tail(30)
        if not pre_event_window.empty:
            # Look for CHI dropping below warning threshold
            warning_dates = pre_event_window[pre_event_window < 40].index
            if len(warning_dates) > 0:
                first_warning = warning_dates[0]
                result.warning_lead_days = (event_start - first_warning).days

        # 2. Check regime accuracy
        if not regime_series.empty:
            event_regime = regime_series.loc[event_start:event_end]
            if not event_regime.empty:
                if event.event_type in ['bear_market', 'crash', 'protocol_failure']:
                    # Should be PRE_CRISIS or CRISIS
                    crisis_regimes = ['PRE_CRISIS', 'CRISIS', 'HOLLOW_RALLY']
                    result.regime_correct = any(r in crisis_regimes for r in event_regime.values)
                elif event.event_type == 'recovery':
                    # Should be EXPANSION or LATE_CYCLE
                    bull_regimes = ['EXPANSION', 'LATE_CYCLE']
                    result.regime_correct = any(r in bull_regimes for r in event_regime.values)

        # 3. Check health scores for affected protocols
        if not health_scores.empty and event.affected_protocols:
            pre_event_health = health_scores.loc[:event_start].tail(7)
            for protocol in event.affected_protocols:
                if protocol == 'all':
                    continue
                if protocol in pre_event_health.columns:
                    protocol_health = pre_event_health[protocol]
                    if (protocol_health < 40).any():
                        result.health_flagged.append(protocol)

        # 4. Estimate drawdown avoided (simplified)
        if event.event_type in ['bear_market', 'crash', 'protocol_failure']:
            # If we had a warning, assume we reduced exposure
            if result.warning_lead_days and result.warning_lead_days >= 3:
                # Assume 50% exposure reduction on warning
                result.hypothetical_drawdown_avoided = event.peak_drawdown * 0.5
            elif result.warning_lead_days and result.warning_lead_days >= 1:
                # Partial reduction
                result.hypothetical_drawdown_avoided = event.peak_drawdown * 0.25

        # 5. Check momentum for recovery capture
        if event.event_type == 'recovery' and not momentum_signals.empty:
            recovery_signals = momentum_signals.loc[event_start:event_end]
            if not recovery_signals.empty:
                # Check if we had bullish signals during recovery
                if 'signal' in recovery_signals.columns:
                    bullish_days = (recovery_signals['signal'] > 0).sum()
                    total_days = len(recovery_signals)
                    result.recovery_capture = bullish_days / max(1, total_days)

        # 6. Check for bottom signal
        if event.event_type in ['crash', 'protocol_failure']:
            # Look for momentum reversal near event end
            post_bottom = momentum_signals.loc[event_end:event_end + timedelta(days=14)]
            if not post_bottom.empty and 'signal' in post_bottom.columns:
                result.signal_at_bottom = (post_bottom['signal'] > 0).any()

        return result

    def run_full_backtest(
        self,
        events: List[CryptoEvent] = None
    ) -> BacktestResults:
        """
        Run full validation across all historical events.

        Args:
            events: List of events to validate (default: VALIDATION_EVENTS)

        Returns:
            BacktestResults with aggregate metrics
        """
        if events is None:
            events = VALIDATION_EVENTS

        # Load historical data from database
        chi_series = self._load_chi_history()
        warnings_df = self._load_warnings_history()
        regime_series = self._load_regime_history()
        momentum_signals = self._load_momentum_history()
        health_scores = self._load_health_history()

        results = []
        for event in events:
            try:
                result = self.validate_event(
                    event=event,
                    chi_series=chi_series,
                    warnings_df=warnings_df,
                    regime_series=regime_series,
                    momentum_signals=momentum_signals,
                    health_scores=health_scores
                )
                results.append(result)
            except Exception as e:
                logger.warning(f"Could not validate event {event.name}: {e}")

        # Aggregate results
        backtest = BacktestResults(event_results=results)
        backtest.total_events = len(results)
        backtest.events_flagged = sum(1 for r in results if r.warning_lead_days is not None)

        lead_days = [r.warning_lead_days for r in results if r.warning_lead_days is not None]
        backtest.avg_warning_lead_days = np.mean(lead_days) if lead_days else 0.0

        backtest.total_dd_avoided = sum(r.hypothetical_drawdown_avoided for r in results)
        backtest.total_recovery_captured = np.mean([r.recovery_capture for r in results])

        # Model accuracies
        backtest.chi_accuracy = sum(1 for r in results if r.regime_correct) / max(1, len(results))

        return backtest

    def _load_chi_history(self) -> pd.Series:
        """Load CHI history from database."""
        try:
            query = """
                SELECT date, value FROM lighthouse_indices
                WHERE series_id = 'CHI'
                ORDER BY date
            """
            df = pd.read_sql(query, self.conn)
            if not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                return df.set_index('date')['value']
        except Exception as e:
            logger.debug(f"No CHI history: {e}")
        return pd.Series(dtype=float)

    def _load_warnings_history(self) -> pd.DataFrame:
        """Load warning flag history."""
        # Would need a warnings log table - return empty for now
        return pd.DataFrame()

    def _load_regime_history(self) -> pd.Series:
        """Load regime classification history."""
        try:
            query = """
                SELECT date, value FROM lighthouse_indices
                WHERE series_id = 'CRYPTO_REGIME'
                ORDER BY date
            """
            df = pd.read_sql(query, self.conn)
            if not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                return df.set_index('date')['value']
        except Exception as e:
            logger.debug(f"No regime history: {e}")
        return pd.Series(dtype=str)

    def _load_momentum_history(self) -> pd.DataFrame:
        """Load momentum signal history."""
        try:
            query = """
                SELECT date, value as signal FROM lighthouse_indices
                WHERE series_id = 'CRYPTO_MOMENTUM'
                ORDER BY date
            """
            df = pd.read_sql(query, self.conn)
            if not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                return df.set_index('date')
        except Exception as e:
            logger.debug(f"No momentum history: {e}")
        return pd.DataFrame()

    def _load_health_history(self) -> pd.DataFrame:
        """Load protocol health score history."""
        try:
            query = """
                SELECT project_id, date, overall_score as health
                FROM crypto_scores
                ORDER BY date
            """
            df = pd.read_sql(query, self.conn)
            if not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                # Pivot to get protocols as columns
                pivot = df.pivot(index='date', columns='project_id', values='health')
                return pivot
        except Exception as e:
            logger.debug(f"No health history: {e}")
        return pd.DataFrame()

    def generate_validation_report(self) -> str:
        """Generate a text report of validation results."""
        results = self.run_full_backtest()
        summary = results.summary()

        report = []
        report.append("=" * 70)
        report.append("CRYPTO SYSTEMATIC VALIDATION REPORT")
        report.append("80/20 Framework - Historical Backtest Results")
        report.append("=" * 70)
        report.append("")
        report.append(f"Overall Score: {summary['overall_score']:.1f}/100")
        report.append(f"Events Tested: {summary['events_tested']}")
        report.append(f"Detection Rate: {summary['detection_rate']:.1%}")
        report.append(f"Avg Warning Lead: {summary['avg_lead_days']:.1f} days")
        report.append(f"Total DD Avoided: {summary['dd_avoided']:.1%}")
        report.append(f"Recovery Captured: {summary['recovery_captured']:.1%}")
        report.append("")
        report.append("Model Accuracies:")
        report.append(f"  CHI/Regime: {summary['chi_accuracy']:.1%}")
        report.append(f"  Momentum: {summary['momentum_accuracy']:.1%}")
        report.append(f"  Health: {summary['health_accuracy']:.1%}")
        report.append("")
        report.append("-" * 70)
        report.append("Event-by-Event Results:")
        report.append("-" * 70)

        for result in results.event_results:
            report.append(f"\n{result.event.name} ({result.event.start_date})")
            report.append(f"  Type: {result.event.event_type}")
            report.append(f"  Peak DD: {result.event.peak_drawdown:.0%}")
            report.append(f"  Warning Lead: {result.warning_lead_days or 'None'} days")
            report.append(f"  Regime Correct: {result.regime_correct}")
            report.append(f"  DD Avoided: {result.hypothetical_drawdown_avoided:.1%}")
            report.append(f"  Score: {result.score():.1f}/100")
            if result.health_flagged:
                report.append(f"  Protocols Flagged: {', '.join(result.health_flagged)}")

        report.append("")
        report.append("=" * 70)
        report.append("Note: Validation requires historical data in database.")
        report.append("Run daily pipeline to accumulate validation dataset.")
        report.append("=" * 70)

        return "\n".join(report)


# ==========================================
# WALK-FORWARD VALIDATION
# ==========================================

class WalkForwardValidator:
    """
    Walk-forward validation for ML models.

    Tests model performance using expanding or rolling windows,
    ensuring no look-ahead bias in parameter estimation.
    """

    def __init__(
        self,
        train_window_days: int = 365,
        test_window_days: int = 30,
        step_days: int = 30,
        expanding: bool = True
    ):
        """
        Initialize walk-forward validator.

        Args:
            train_window_days: Training window size
            test_window_days: Test window size
            step_days: Days to step forward each iteration
            expanding: Use expanding (vs rolling) window
        """
        self.train_window = train_window_days
        self.test_window = test_window_days
        self.step_days = step_days
        self.expanding = expanding

    def validate_model(
        self,
        model,
        features_df: pd.DataFrame,
        target_series: pd.Series
    ) -> Dict:
        """
        Run walk-forward validation on a model.

        Args:
            model: Model with fit/predict methods
            features_df: Feature DataFrame indexed by date
            target_series: Target series indexed by date

        Returns:
            Dict with validation metrics
        """
        # Align features and target
        common_dates = features_df.index.intersection(target_series.index)
        if len(common_dates) < self.train_window + self.test_window:
            return {'error': 'Insufficient data for walk-forward validation'}

        features = features_df.loc[common_dates]
        target = target_series.loc[common_dates]

        results = []
        start_idx = self.train_window

        while start_idx + self.test_window <= len(common_dates):
            # Define train/test splits
            if self.expanding:
                train_start = 0
            else:
                train_start = start_idx - self.train_window

            train_end = start_idx
            test_end = start_idx + self.test_window

            X_train = features.iloc[train_start:train_end]
            y_train = target.iloc[train_start:train_end]
            X_test = features.iloc[train_end:test_end]
            y_test = target.iloc[train_end:test_end]

            try:
                # Fit model on training data
                if hasattr(model, 'fit'):
                    model.fit(X_train, y_train)

                # Predict on test data
                if hasattr(model, 'predict'):
                    y_pred = model.predict(X_test)
                elif hasattr(model, 'generate_signal'):
                    y_pred = model.generate_signal(X_test)
                else:
                    continue

                # Calculate metrics
                if len(y_pred) == len(y_test):
                    # Direction accuracy
                    direction_acc = np.mean(np.sign(y_pred) == np.sign(y_test))
                    # Correlation
                    corr = np.corrcoef(y_pred.flatten(), y_test.values.flatten())[0, 1]

                    results.append({
                        'test_start': common_dates[train_end],
                        'test_end': common_dates[test_end - 1],
                        'direction_accuracy': direction_acc,
                        'correlation': corr if not np.isnan(corr) else 0.0
                    })
            except Exception as e:
                logger.debug(f"Walk-forward step failed: {e}")

            start_idx += self.step_days

        if not results:
            return {'error': 'No valid walk-forward results'}

        results_df = pd.DataFrame(results)

        return {
            'n_windows': len(results),
            'avg_direction_accuracy': results_df['direction_accuracy'].mean(),
            'std_direction_accuracy': results_df['direction_accuracy'].std(),
            'avg_correlation': results_df['correlation'].mean(),
            'std_correlation': results_df['correlation'].std(),
            'min_direction_accuracy': results_df['direction_accuracy'].min(),
            'max_direction_accuracy': results_df['direction_accuracy'].max(),
            'results_df': results_df
        }


# ==========================================
# CLI
# ==========================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Crypto Systematic Validation")
    parser.add_argument("--db", type=str,
                       default="/Users/bob/LHM/Data/databases/Lighthouse_Master.db",
                       help="Database path")
    parser.add_argument("--report", action="store_true", help="Generate validation report")

    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    engine = CryptoValidationEngine(conn)

    if args.report:
        print(engine.generate_validation_report())
    else:
        results = engine.run_full_backtest()
        print(f"Validation Score: {results.overall_score():.1f}/100")
        print(f"Events Flagged: {results.events_flagged}/{results.total_events}")

    conn.close()
