from ..config import CONFIG
from ..collect.fred import update_fred_raw
from ..collect.fred_extended import update_fred_extended
from ..collect.crypto import update_crypto_raw
from ..collect.market import update_market_raw
from ..collect.volatility import update_volatility_raw
from ..curate.build_macro_panel import build_macro_panel
from ..curate.build_crypto_panel import build_crypto_panel
from ..curate.build_chartbook_panel import build_chartbook_panel
from ..indicators.core import compute_all_indicators
from ..utils.logging import get_logger

log = get_logger(__name__)


class DailyFlow:
    def run_all(self, include_extended=True, include_dashboards=False):
        """
        Run the full daily data pipeline.

        Args:
            include_extended: If True, fetch extended FRED series (TGA, Fed BS, etc.)
            include_dashboards: If True, generate dashboards after data collection
        """
        CONFIG.ensure_dirs()
        log.info("=== STARTING LIGHTHOUSE MACRO DAILY FLOW ===")

        # 1. Collect (Raw Layer) - Core
        log.info("\n--- STAGE 1: DATA COLLECTION ---")
        update_fred_raw()
        update_crypto_raw()
        update_market_raw()

        # 1b. Collect Extended Data (Priority 1 Charts)
        if include_extended:
            log.info("\n--- STAGE 1b: EXTENDED DATA COLLECTION ---")
            update_fred_extended()
            update_volatility_raw()

        # 2. Curate (Clean Layer)
        log.info("\n--- STAGE 2: DATA CURATION ---")
        build_macro_panel()
        build_crypto_panel()

        # 3. Assemble Master Panel
        log.info("\n--- STAGE 3: PANEL ASSEMBLY ---")
        chartbook = build_chartbook_panel()

        # 4. Compute Intelligence
        log.info("\n--- STAGE 4: INDICATOR COMPUTATION ---")
        indicators = compute_all_indicators(chartbook)

        log.info("\n=== FLOW COMPLETE ===")

        # Print summary
        print("\nLatest Market Prices:")
        market_cols = ['SPX', 'Gold', 'DXY', 'BTC_CLOSE']
        available_cols = [c for c in market_cols if c in chartbook.columns]
        if available_cols:
            print(chartbook[available_cols].tail(3))

        print("\nLatest Proprietary Indicators:")
        print(indicators.tail(3))

        # 5. Generate Dashboards (Optional)
        if include_dashboards:
            log.info("\n--- STAGE 5: DASHBOARD GENERATION ---")
            self._generate_dashboards()

        return chartbook, indicators

    def run_core_only(self):
        """Run only the core data pipeline (no extended data)."""
        return self.run_all(include_extended=False, include_dashboards=False)

    def run_with_dashboards(self):
        """Run full pipeline including dashboard generation."""
        return self.run_all(include_extended=True, include_dashboards=True)

    def _generate_dashboards(self):
        """Generate all dashboards."""
        try:
            from ..dashboards.run_all_dashboards import smart_run
            smart_run()
        except Exception as e:
            log.error(f"Dashboard generation failed: {e}")


# Convenience function for backward compatibility
def run_daily_flow():
    """Run the daily flow pipeline."""
    flow = DailyFlow()
    return flow.run_all()
