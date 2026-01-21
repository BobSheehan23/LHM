"""
LIGHTHOUSE MACRO - CRYPTO DATA FETCHERS
=======================================
Unified crypto data fetching using Token Terminal API.
Follows the same patterns as other LHM fetchers.

Integrates with the on-chain framework from:
    /Users/bob/LHM/Strategy/ONCHAIN_ANALYTICS_FRAMEWORK.md
"""

import sqlite3
import time
import logging
from datetime import datetime
from typing import Tuple, List, Dict, Optional
import sys
import os

# Add the lighthouse_quant package to path
sys.path.insert(0, '/Users/bob/LHM')

from lighthouse_quant.crypto.token_terminal import TokenTerminalClient
from lighthouse_quant.crypto.fundamentals import CryptoFundamentalsEngine, ProtocolAnalysis

from .config import FETCH_CONFIG

logger = logging.getLogger(__name__)


# ==========================================
# CRYPTO WATCHLIST CONFIGURATION
# ==========================================

# LHM Crypto Watchlist - organized by sector per the On-Chain Framework
# Note: Project IDs must match Token Terminal's project_id field exactly
CRYPTO_WATCHLIST = {
    # Layer 1 (Settlement)
    'layer1': [
        'ethereum', 'solana', 'avalanche', 'near-protocol', 'sui', 'aptos',
    ],
    # Layer 2 (Scaling)
    'layer2': [
        'arbitrum', 'optimism', 'base', 'polygon', 'starknet', 'zksync-era',
    ],
    # DeFi - DEX
    'defi_dex': [
        'uniswap', 'curve', 'pancakeswap', 'raydium', 'aerodrome',
    ],
    # DeFi - Lending
    'defi_lending': [
        'aave', 'compound', 'morpho', 'spark',
    ],
    # DeFi - Derivatives
    'defi_derivatives': [
        'gmx', 'dydx', 'hyperliquid', 'vertex-protocol', 'synthetix',
    ],
    # Liquid Staking
    'liquid_staking': [
        'lido-finance', 'rocket-pool', 'jito', 'marinade',
    ],
    # Infrastructure
    'infrastructure': [
        'chainlink', 'the-graph', 'pyth',
    ],
    # Stablecoins
    'stablecoins': [
        'makerdao',  # Sky (formerly MakerDAO)
    ],
}

# Flatten watchlist for easy iteration
def get_all_watchlist_projects() -> List[str]:
    """Get all projects from the watchlist."""
    projects = []
    for sector_projects in CRYPTO_WATCHLIST.values():
        projects.extend(sector_projects)
    return projects


# Token Terminal metrics to fetch for time series
CRYPTO_METRICS = [
    # Market
    'market_cap_fully_diluted', 'market_cap_circulating', 'price',
    'token_trading_volume', 'tokenholders',
    # Financial
    'fees', 'revenue', 'token_incentives', 'earnings', 'tvl',
    'treasury', 'treasury_net', 'active_loans', 'trading_volume',
    # Usage
    'user_dau', 'user_wau', 'user_mau',
    'transaction_count', 'active_addresses_daily',
    # Development
    'active_developers', 'code_commits',
    # Valuation
    'pf_fully_diluted', 'ps_fully_diluted',
]


# ==========================================
# CRYPTO DATABASE SCHEMA
# ==========================================

def init_crypto_tables(conn: sqlite3.Connection):
    """Initialize crypto-specific tables in the database."""
    c = conn.cursor()

    # Crypto time series metrics (daily snapshots)
    c.execute('''CREATE TABLE IF NOT EXISTS crypto_metrics (
        project_id TEXT,
        date TEXT,
        metric_id TEXT,
        value REAL,
        PRIMARY KEY (project_id, date, metric_id)
    )''')

    # Crypto fundamental scores (daily analysis)
    c.execute('''CREATE TABLE IF NOT EXISTS crypto_scores (
        project_id TEXT,
        date TEXT,
        name TEXT,
        sector TEXT,
        verdict TEXT,
        overall_score INTEGER,
        financial_score INTEGER,
        usage_score INTEGER,
        valuation_score INTEGER,
        fdv REAL,
        market_cap REAL,
        ann_revenue REAL,
        ann_fees REAL,
        pe_ratio REAL,
        pf_ratio REAL,
        subsidy_score REAL,
        float_ratio REAL,
        dau INTEGER,
        mau INTEGER,
        active_developers INTEGER,
        tvl REAL,
        red_flags TEXT,
        PRIMARY KEY (project_id, date)
    )''')

    # Crypto metadata
    c.execute('''CREATE TABLE IF NOT EXISTS crypto_meta (
        project_id TEXT PRIMARY KEY,
        name TEXT,
        symbol TEXT,
        sector TEXT,
        last_updated TEXT,
        last_fetched TEXT,
        data_quality TEXT
    )''')

    # Indexes for efficient queries
    c.execute('CREATE INDEX IF NOT EXISTS idx_crypto_metrics_project ON crypto_metrics(project_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_crypto_metrics_date ON crypto_metrics(date)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_crypto_scores_date ON crypto_scores(date)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_crypto_scores_verdict ON crypto_scores(verdict)')

    conn.commit()
    logger.info("Crypto tables initialized")


# ==========================================
# CRYPTO FETCHER CLASS
# ==========================================

class CryptoFetcher:
    """
    Fetch crypto data from Token Terminal and compute LHM fundamentals.

    Follows the same patterns as FREDFetcher, BLSFetcher, etc.
    """

    def __init__(self, conn: sqlite3.Connection, api_key: str = None):
        """
        Initialize the crypto fetcher.

        Args:
            conn: SQLite database connection
            api_key: Token Terminal API key (optional, uses env/default)
        """
        self.conn = conn
        self.client = TokenTerminalClient(api_key=api_key)
        self.engine = CryptoFundamentalsEngine(client=self.client)

        # Initialize crypto tables
        init_crypto_tables(conn)

    def fetch_metrics(
        self,
        project_ids: List[str] = None,
        days: int = 30
    ) -> Tuple[int, int]:
        """
        Fetch time series metrics for protocols.

        Args:
            project_ids: List of project IDs (default: watchlist)
            days: Days of history to fetch

        Returns:
            Tuple of (projects_updated, observations_added)
        """
        if project_ids is None:
            project_ids = get_all_watchlist_projects()

        c = self.conn.cursor()
        total_projects = 0
        total_obs = 0

        logger.info(f"Fetching metrics for {len(project_ids)} protocols...")

        for pid in project_ids:
            try:
                logger.info(f"   {pid}...")

                # Fetch metrics from Token Terminal
                df = self.client.get_metrics(pid, days=days, metric_ids=CRYPTO_METRICS)

                if df.empty:
                    logger.warning(f"   {pid}: No data")
                    continue

                obs_count = 0
                for date_idx in df.index:
                    date_str = str(date_idx)
                    for metric_id in df.columns:
                        if metric_id == 'timestamp':
                            continue
                        value = df.loc[date_idx, metric_id]
                        if value is not None and str(value) not in ['', 'nan', 'None']:
                            try:
                                c.execute(
                                    "INSERT OR REPLACE INTO crypto_metrics VALUES (?,?,?,?)",
                                    (pid, date_str, metric_id, float(value))
                                )
                                obs_count += 1
                            except (ValueError, TypeError):
                                pass

                # Update metadata
                c.execute("""INSERT OR REPLACE INTO crypto_meta
                            (project_id, name, sector, last_updated, last_fetched)
                            VALUES (?,?,?,?,?)""",
                         (pid, pid, self._get_sector(pid),
                          datetime.now().isoformat(), datetime.now().isoformat()))

                total_projects += 1
                total_obs += obs_count
                logger.info(f"   {pid}: {obs_count:,} observations")

                # Rate limiting
                time.sleep(FETCH_CONFIG.get("rate_limit_delay", 0.25))

            except Exception as e:
                logger.error(f"   {pid}: Error - {e}")
                continue

        self.conn.commit()
        return total_projects, total_obs

    def fetch_fundamentals(
        self,
        project_ids: List[str] = None
    ) -> Tuple[int, int]:
        """
        Compute and store LHM fundamental scores for protocols.

        Args:
            project_ids: List of project IDs (default: watchlist)

        Returns:
            Tuple of (projects_analyzed, scores_stored)
        """
        if project_ids is None:
            project_ids = get_all_watchlist_projects()

        c = self.conn.cursor()
        total_analyzed = 0
        today = datetime.now().strftime('%Y-%m-%d')

        logger.info(f"Computing fundamentals for {len(project_ids)} protocols...")

        for pid in project_ids:
            try:
                logger.info(f"   {pid}...")

                # Run LHM fundamental analysis
                analysis = self.engine.analyze_protocol(pid)

                if analysis is None:
                    logger.warning(f"   {pid}: Insufficient data")
                    continue

                # Store the analysis
                c.execute("""INSERT OR REPLACE INTO crypto_scores
                            (project_id, date, name, sector, verdict, overall_score,
                             financial_score, usage_score, valuation_score,
                             fdv, market_cap, ann_revenue, ann_fees,
                             pe_ratio, pf_ratio, subsidy_score, float_ratio,
                             dau, mau, active_developers, tvl, red_flags)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                         (pid, today, analysis.name, analysis.sector,
                          analysis.verdict.value, analysis.overall_score,
                          analysis.financial_score, analysis.usage_score,
                          analysis.valuation_score, analysis.fdv, analysis.market_cap,
                          analysis.annualized_revenue, analysis.annualized_fees,
                          analysis.pe_ratio if analysis.pe_ratio != float('inf') else None,
                          analysis.pf_ratio if analysis.pf_ratio != float('inf') else None,
                          analysis.subsidy_score if analysis.subsidy_score != float('inf') else None,
                          analysis.float_ratio, analysis.dau, analysis.mau,
                          analysis.active_developers, analysis.tvl,
                          '; '.join(analysis.red_flags) if analysis.red_flags else None))

                total_analyzed += 1
                logger.info(f"   {pid}: {analysis.verdict.value} (Score: {analysis.overall_score})")

                # Rate limiting (analysis already made API calls)
                time.sleep(FETCH_CONFIG.get("rate_limit_delay", 0.1))

            except Exception as e:
                logger.error(f"   {pid}: Error - {e}")
                continue

        self.conn.commit()
        return total_analyzed, total_analyzed

    def fetch_all(self, days: int = 30) -> Tuple[int, int]:
        """
        Full crypto data update: metrics + fundamentals.

        Args:
            days: Days of metric history to fetch

        Returns:
            Tuple of (series_updated, observations_added)
        """
        total_series = 0
        total_obs = 0

        # 1. Fetch time series metrics
        logger.info("--- CRYPTO: Time Series Metrics ---")
        series, obs = self.fetch_metrics(days=days)
        total_series += series
        total_obs += obs

        # 2. Compute fundamental scores
        logger.info("--- CRYPTO: Fundamental Analysis ---")
        analyzed, scores = self.fetch_fundamentals()
        total_series += analyzed
        total_obs += scores

        return total_series, total_obs

    def _get_sector(self, project_id: str) -> str:
        """Get sector for a project from the watchlist."""
        for sector, projects in CRYPTO_WATCHLIST.items():
            if project_id in projects:
                return sector
        return 'uncategorized'

    def get_latest_scores(self) -> 'pd.DataFrame':
        """Get the most recent fundamental scores for all protocols."""
        import pandas as pd

        query = """
        SELECT * FROM crypto_scores
        WHERE date = (SELECT MAX(date) FROM crypto_scores)
        ORDER BY overall_score DESC
        """
        return pd.read_sql(query, self.conn)

    def get_tier1_protocols(self) -> List[str]:
        """Get list of Tier 1 (Accumulate) protocols."""
        c = self.conn.cursor()
        c.execute("""
            SELECT project_id FROM crypto_scores
            WHERE date = (SELECT MAX(date) FROM crypto_scores)
            AND verdict LIKE '%TIER 1%'
        """)
        return [row[0] for row in c.fetchall()]

    def get_protocol_history(
        self,
        project_id: str,
        metric_id: str,
        days: int = 365
    ) -> 'pd.DataFrame':
        """Get historical time series for a protocol metric."""
        import pandas as pd

        query = """
        SELECT date, value FROM crypto_metrics
        WHERE project_id = ? AND metric_id = ?
        ORDER BY date DESC
        LIMIT ?
        """
        df = pd.read_sql(query, self.conn, params=(project_id, metric_id, days))
        df['date'] = pd.to_datetime(df['date'])
        return df.set_index('date').sort_index()


# ==========================================
# CLI INTERFACE
# ==========================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Lighthouse Macro Crypto Fetcher")
    parser.add_argument("--metrics-only", action="store_true", help="Only fetch metrics")
    parser.add_argument("--fundamentals-only", action="store_true", help="Only compute fundamentals")
    parser.add_argument("--days", type=int, default=30, help="Days of history to fetch")
    parser.add_argument("--projects", nargs="+", help="Specific projects to fetch")

    args = parser.parse_args()

    # Use the main database
    from .config import DB_PATH
    conn = sqlite3.connect(DB_PATH)

    fetcher = CryptoFetcher(conn)

    if args.metrics_only:
        series, obs = fetcher.fetch_metrics(project_ids=args.projects, days=args.days)
        print(f"Fetched {series} protocols, {obs:,} observations")
    elif args.fundamentals_only:
        analyzed, scores = fetcher.fetch_fundamentals(project_ids=args.projects)
        print(f"Analyzed {analyzed} protocols")
    else:
        series, obs = fetcher.fetch_all(days=args.days)
        print(f"Total: {series} series, {obs:,} observations")

    conn.close()
