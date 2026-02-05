"""
LIGHTHOUSE MACRO - MARKET BREADTH FETCHER
==========================================
Computes market breadth indicators from S&P 500 component data.

Metrics computed:
- % of stocks above 50-day MA
- % of stocks above 200-day MA
- Advance-Decline Line
- New Highs - New Lows
- McClellan Oscillator
- McClellan Summation Index

Data source: yfinance (free)
"""

import pandas as pd
import numpy as np
import sqlite3
import time
import logging
from datetime import datetime, timedelta
from typing import Tuple, List, Optional
from io import StringIO

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

import requests

logger = logging.getLogger(__name__)


# ==========================================
# S&P 500 CONSTITUENT FETCHER
# ==========================================

def get_sp500_tickers() -> List[str]:
    """
    Fetch current S&P 500 constituents from Wikipedia.
    Returns list of ticker symbols.
    """
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

        # Use requests with proper headers to avoid 403
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        tables = pd.read_html(StringIO(response.text))
        df = tables[0]

        # Clean ticker symbols (replace . with - for yfinance)
        tickers = df['Symbol'].str.replace('.', '-', regex=False).tolist()

        # Filter out any problematic tickers
        tickers = [t for t in tickers if t and isinstance(t, str) and len(t) <= 6]

        logger.info(f"Found {len(tickers)} S&P 500 constituents")
        return tickers

    except Exception as e:
        logger.error(f"Error fetching S&P 500 constituents: {e}")
        # Fallback to a static list of major components
        return [
            'AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'META', 'BRK-B', 'UNH', 'XOM', 'JPM',
            'JNJ', 'V', 'PG', 'MA', 'HD', 'CVX', 'MRK', 'ABBV', 'LLY', 'PEP',
            'COST', 'KO', 'AVGO', 'WMT', 'MCD', 'CSCO', 'TMO', 'ACN', 'ABT', 'DHR',
        ]


# ==========================================
# BREADTH CALCULATOR
# ==========================================

class BreadthCalculator:
    """Calculate market breadth metrics from component price data."""

    def __init__(self, prices: pd.DataFrame):
        """
        Initialize with price DataFrame.

        Args:
            prices: DataFrame with dates as index, tickers as columns
        """
        self.prices = prices.sort_index()

    def pct_above_ma(self, window: int) -> pd.Series:
        """
        Calculate % of stocks above N-day moving average.

        Args:
            window: MA window (e.g., 50, 200)

        Returns:
            Series with date index and % values (0-100)
        """
        mas = self.prices.rolling(window=window, min_periods=window).mean()
        above = (self.prices > mas).astype(float)
        pct_above = above.mean(axis=1) * 100
        return pct_above.dropna()

    def advance_decline(self) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate advances, declines, and cumulative A/D line.

        Returns:
            Tuple of (advances, declines, ad_line)
        """
        returns = self.prices.pct_change()
        advances = (returns > 0).sum(axis=1)
        declines = (returns < 0).sum(axis=1)
        net_advances = advances - declines
        ad_line = net_advances.cumsum()

        return advances, declines, ad_line

    def new_highs_lows(self, window: int = 252) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate new 52-week (or custom window) highs and lows.

        Args:
            window: Lookback window in days (252 = ~1 year)

        Returns:
            Tuple of (new_highs, new_lows, net_new_highs)
        """
        rolling_max = self.prices.rolling(window=window, min_periods=window).max()
        rolling_min = self.prices.rolling(window=window, min_periods=window).min()

        is_high = (self.prices == rolling_max).astype(float)
        is_low = (self.prices == rolling_min).astype(float)

        new_highs = is_high.sum(axis=1)
        new_lows = is_low.sum(axis=1)
        net_new_highs = new_highs - new_lows

        return new_highs.dropna(), new_lows.dropna(), net_new_highs.dropna()

    def mcclellan_oscillator(self) -> Tuple[pd.Series, pd.Series]:
        """
        Calculate McClellan Oscillator and Summation Index.

        McClellan Oscillator = 19-day EMA of (A-D) - 39-day EMA of (A-D)
        Summation Index = Cumulative sum of Oscillator

        Returns:
            Tuple of (oscillator, summation_index)
        """
        returns = self.prices.pct_change()
        net_advances = (returns > 0).sum(axis=1) - (returns < 0).sum(axis=1)

        ema_19 = net_advances.ewm(span=19, adjust=False).mean()
        ema_39 = net_advances.ewm(span=39, adjust=False).mean()

        oscillator = ema_19 - ema_39
        summation = oscillator.cumsum()

        return oscillator.dropna(), summation.dropna()

    def thrust_indicator(self, threshold: float = 0.4) -> pd.Series:
        """
        Calculate breadth thrust indicator.

        A thrust occurs when % above 50d goes from <25% to >threshold in 10 days.

        Returns:
            Series with 1 for thrust days, 0 otherwise
        """
        pct_50d = self.pct_above_ma(50)

        # Check for thrust conditions
        min_10d = pct_50d.rolling(10).min()
        thrust = ((min_10d < 25) & (pct_50d > threshold * 100)).astype(int)

        return thrust


# ==========================================
# BREADTH DATA FETCHER
# ==========================================

class BreadthDataFetcher:
    """
    Fetch S&P 500 component prices and compute breadth metrics.
    Stores results in the Lighthouse database.
    """

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def _fetch_prices_batch(self, tickers: List[str], start_date: str,
                            batch_size: int = 50) -> pd.DataFrame:
        """
        Fetch historical prices for tickers in batches.

        Args:
            tickers: List of ticker symbols
            start_date: Start date (YYYY-MM-DD)
            batch_size: Tickers per batch (to avoid rate limits)

        Returns:
            DataFrame with dates as index, tickers as columns
        """
        if not YFINANCE_AVAILABLE:
            logger.error("yfinance not installed. Run: pip install yfinance")
            return pd.DataFrame()

        all_prices = {}
        failed_tickers = []

        logger.info(f"Fetching prices for {len(tickers)} tickers...")

        for i in range(0, len(tickers), batch_size):
            batch = tickers[i:i + batch_size]
            batch_str = ' '.join(batch)

            try:
                logger.info(f"   Batch {i//batch_size + 1}/{(len(tickers)-1)//batch_size + 1}: {len(batch)} tickers")

                data = yf.download(
                    batch_str,
                    start=start_date,
                    progress=False,
                    threads=True
                )

                if isinstance(data.columns, pd.MultiIndex):
                    # Multiple tickers: extract Close prices
                    closes = data['Close']
                else:
                    # Single ticker
                    closes = pd.DataFrame({batch[0]: data['Close']})

                for col in closes.columns:
                    if not closes[col].isna().all():
                        all_prices[col] = closes[col]

                time.sleep(1)  # Rate limiting

            except Exception as e:
                logger.warning(f"   Batch error: {e}")
                failed_tickers.extend(batch)

        if failed_tickers:
            logger.warning(f"Failed to fetch: {len(failed_tickers)} tickers")

        df = pd.DataFrame(all_prices)
        df.index = pd.to_datetime(df.index)

        logger.info(f"   Got prices for {len(df.columns)} stocks, {len(df)} days")

        return df

    def fetch_and_compute(self, lookback_years: int = 3) -> Tuple[int, int]:
        """
        Fetch S&P 500 prices and compute all breadth metrics.

        Args:
            lookback_years: Years of history to fetch

        Returns:
            Tuple of (series_count, observations_count)
        """
        c = self.conn.cursor()
        total_obs = 0

        # Get S&P 500 constituents
        tickers = get_sp500_tickers()

        # Calculate start date
        start_date = (datetime.now() - timedelta(days=lookback_years * 365)).strftime('%Y-%m-%d')

        # Fetch prices
        prices = self._fetch_prices_batch(tickers, start_date)

        if prices.empty:
            logger.error("No price data fetched")
            return 0, 0

        # Initialize calculator
        calc = BreadthCalculator(prices)

        # Compute and store metrics
        metrics_to_store = {}

        # % Above MAs
        logger.info("Computing % above MAs...")
        metrics_to_store['SPX_PCT_ABOVE_20D'] = calc.pct_above_ma(20)
        metrics_to_store['SPX_PCT_ABOVE_50D'] = calc.pct_above_ma(50)
        metrics_to_store['SPX_PCT_ABOVE_200D'] = calc.pct_above_ma(200)

        # Advance-Decline
        logger.info("Computing A/D line...")
        advances, declines, ad_line = calc.advance_decline()
        metrics_to_store['SPX_ADVANCES'] = advances
        metrics_to_store['SPX_DECLINES'] = declines
        metrics_to_store['SPX_AD_LINE'] = ad_line
        metrics_to_store['SPX_AD_RATIO'] = advances / (declines + 1)  # Avoid div by zero

        # New Highs - New Lows
        logger.info("Computing NH-NL...")
        new_highs, new_lows, net_nh_nl = calc.new_highs_lows()
        metrics_to_store['SPX_NEW_HIGHS'] = new_highs
        metrics_to_store['SPX_NEW_LOWS'] = new_lows
        metrics_to_store['SPX_NET_NEW_HIGHS'] = net_nh_nl

        # McClellan
        logger.info("Computing McClellan...")
        mcclellan_osc, mcclellan_sum = calc.mcclellan_oscillator()
        metrics_to_store['SPX_MCCLELLAN_OSC'] = mcclellan_osc
        metrics_to_store['SPX_MCCLELLAN_SUM'] = mcclellan_sum

        # Breadth Thrust
        logger.info("Computing breadth thrust...")
        thrust = calc.thrust_indicator()
        metrics_to_store['SPX_BREADTH_THRUST'] = thrust

        # Store all metrics
        logger.info("Storing metrics in database...")

        series_metadata = {
            'SPX_PCT_ABOVE_20D': ('S&P 500 % Above 20-Day MA', 'Percent'),
            'SPX_PCT_ABOVE_50D': ('S&P 500 % Above 50-Day MA', 'Percent'),
            'SPX_PCT_ABOVE_200D': ('S&P 500 % Above 200-Day MA', 'Percent'),
            'SPX_ADVANCES': ('S&P 500 Daily Advances', 'Count'),
            'SPX_DECLINES': ('S&P 500 Daily Declines', 'Count'),
            'SPX_AD_LINE': ('S&P 500 Advance-Decline Line', 'Cumulative'),
            'SPX_AD_RATIO': ('S&P 500 Advance-Decline Ratio', 'Ratio'),
            'SPX_NEW_HIGHS': ('S&P 500 New 52-Week Highs', 'Count'),
            'SPX_NEW_LOWS': ('S&P 500 New 52-Week Lows', 'Count'),
            'SPX_NET_NEW_HIGHS': ('S&P 500 Net New Highs', 'Count'),
            'SPX_MCCLELLAN_OSC': ('S&P 500 McClellan Oscillator', 'Index'),
            'SPX_MCCLELLAN_SUM': ('S&P 500 McClellan Summation Index', 'Index'),
            'SPX_BREADTH_THRUST': ('S&P 500 Breadth Thrust Signal', 'Binary'),
        }

        for series_id, series_data in metrics_to_store.items():
            obs_count = 0

            for date, value in series_data.items():
                if pd.notna(value) and np.isfinite(value):
                    date_str = date.strftime('%Y-%m-%d')
                    c.execute(
                        "INSERT OR REPLACE INTO observations VALUES (?,?,?)",
                        (series_id, date_str, float(value))
                    )
                    obs_count += 1

            total_obs += obs_count

            # Update metadata
            title, units = series_metadata.get(series_id, (series_id, 'Value'))
            c.execute("""INSERT OR REPLACE INTO series_meta
                        (series_id, title, source, category, frequency, units, last_updated, last_fetched)
                        VALUES (?,?,?,?,?,?,?,?)""",
                     (series_id, title, "Computed", "Market_Breadth", "Daily", units,
                      datetime.now().isoformat(), datetime.now().isoformat()))

            logger.info(f"   {series_id}: {obs_count:,} observations")

        self.conn.commit()

        series_count = len(metrics_to_store)
        logger.info(f"\nBreadth total: {series_count} series, {total_obs:,} observations")

        return series_count, total_obs


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    db_path = "/Users/bob/LHM/Data/databases/Lighthouse_Master.db"
    conn = sqlite3.connect(db_path)

    fetcher = BreadthDataFetcher(conn)
    series, obs = fetcher.fetch_and_compute(lookback_years=3)

    print(f"\nComplete: {series} series, {obs:,} observations")
    conn.close()
