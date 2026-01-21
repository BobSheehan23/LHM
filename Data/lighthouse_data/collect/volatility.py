"""
Volatility Data Collection for Priority 1 Charts
Lighthouse Macro - January 2026

Fetches:
- VIX (CBOE Volatility Index)
- MOVE Index (ICE BofA MOVE - Treasury Volatility)
- Other volatility metrics
"""

import pandas as pd
import yfinance as yf
from ..config import CONFIG
from ..utils.logging import get_logger
from ..utils.io import write_parquet

log = get_logger(__name__)

# Volatility Tickers
VOLATILITY_TICKERS = {
    "^VIX": "VIX",              # CBOE Volatility Index
    "^VVIX": "VVIX",            # VIX of VIX (volatility of volatility)
    "^VXN": "VXN",              # Nasdaq 100 Volatility
    "^RVX": "RVX",              # Russell 2000 Volatility
    "^OVX": "OVX",              # Oil Volatility
    "^GVZ": "GVZ",              # Gold Volatility
}


def fetch_move_index() -> pd.Series | None:
    """
    Fetch MOVE Index (ICE BofA MOVE).

    The MOVE index measures Treasury volatility and is a key indicator
    for rates volatility leading equity volatility.

    Note: MOVE is not directly available on Yahoo Finance.
    We use a proxy or FRED alternative.
    """
    log.info("Fetching MOVE Index proxy...")

    # Try FRED first (MOVE is sometimes available as BAMLMOVE)
    # If not available, calculate proxy from Treasury yield volatility
    try:
        # Attempt yfinance for MOVE ETN (VXTLT as proxy for Treasury vol)
        # Note: There's no direct MOVE ticker, so we use Treasury ETF volatility
        tlt = yf.download("TLT", start="2010-01-01", progress=False, auto_adjust=True)

        if tlt.empty:
            log.warning("Could not fetch TLT for MOVE proxy")
            return None

        # Handle MultiIndex columns
        if isinstance(tlt.columns, pd.MultiIndex):
            tlt.columns = tlt.columns.get_level_values(0)

        close = tlt['Close'] if 'Close' in tlt.columns else tlt.iloc[:, 0]

        # Calculate realized volatility as MOVE proxy
        # MOVE is roughly 10x the annualized daily vol of long-term Treasuries
        returns = close.pct_change()
        realized_vol = returns.rolling(21).std() * (252 ** 0.5) * 100  # Annualized, in %
        move_proxy = realized_vol * 10  # Scale to approximate MOVE levels

        move_proxy.name = "MOVE_Proxy"
        move_proxy.index = pd.to_datetime(move_proxy.index).normalize()

        if move_proxy.index.tz is not None:
            move_proxy.index = move_proxy.index.tz_localize(None)

        return move_proxy.dropna()

    except Exception as e:
        log.error(f"Failed to calculate MOVE proxy: {e}")
        return None


def update_volatility_raw() -> pd.DataFrame:
    """
    Fetch all volatility indices.

    Returns:
        DataFrame with volatility metrics, daily frequency
    """
    log.info("Fetching VOLATILITY data (VIX, MOVE proxy)...")

    frames = {}

    # Fetch standard volatility tickers
    for ticker, name in VOLATILITY_TICKERS.items():
        try:
            data = yf.download(ticker, start="2010-01-01", progress=False, auto_adjust=True)

            if data.empty:
                log.warning(f"No data for {ticker}")
                continue

            # Handle MultiIndex columns
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)

            if 'Close' in data.columns:
                series = data['Close']
            else:
                series = data.iloc[:, 0]

            series.name = name
            series.index = pd.to_datetime(series.index).normalize()

            if series.index.tz is not None:
                series.index = series.index.tz_localize(None)

            frames[name] = series
            log.info(f"Fetched {name}: {len(series)} observations")

        except Exception as e:
            log.error(f"Failed to fetch {ticker}: {e}")

    # Add MOVE proxy
    move = fetch_move_index()
    if move is not None:
        frames['MOVE_Proxy'] = move
        log.info(f"Calculated MOVE proxy: {len(move)} observations")

    if not frames:
        log.error("No volatility data fetched!")
        return pd.DataFrame()

    # Combine all series
    df = pd.concat(frames, axis=1)

    # Forward fill weekends/holidays
    df = df.asfreq('D').ffill()

    # Calculate derived metrics
    if 'VIX' in df.columns and 'MOVE_Proxy' in df.columns:
        # VIX/MOVE ratio - when MOVE leads VIX higher, rates vol is driving
        df['VIX_MOVE_Ratio'] = df['VIX'] / df['MOVE_Proxy']

        # Rolling correlation
        df['VIX_MOVE_Corr_60D'] = df['VIX'].rolling(60).corr(df['MOVE_Proxy'])

    if 'VIX' in df.columns:
        # VIX term structure proxy (VIX vs realized vol)
        spx = yf.download("^GSPC", start="2010-01-01", progress=False, auto_adjust=True)
        if not spx.empty:
            if isinstance(spx.columns, pd.MultiIndex):
                spx.columns = spx.columns.get_level_values(0)
            spx_close = spx['Close'] if 'Close' in spx.columns else spx.iloc[:, 0]
            spx_close.index = pd.to_datetime(spx_close.index).normalize()
            if spx_close.index.tz is not None:
                spx_close.index = spx_close.index.tz_localize(None)

            # Realized vol (21-day)
            realized = spx_close.pct_change().rolling(21).std() * (252 ** 0.5) * 100
            realized = realized.reindex(df.index).ffill()

            df['SPX_Realized_Vol'] = realized
            df['VIX_Premium'] = df['VIX'] - df['SPX_Realized_Vol']  # Implied - Realized

    # Save
    out_path = CONFIG.raw_dir / "volatility" / "volatility_raw.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    write_parquet(df, out_path)

    log.info(f"Volatility data updated. Shape: {df.shape}")
    return df


def get_vix_move_analysis() -> pd.DataFrame:
    """
    Convenience function for VIX vs MOVE analysis.
    Returns DataFrame ready for charting.
    """
    vol_path = CONFIG.raw_dir / "volatility" / "volatility_raw.parquet"

    if vol_path.exists():
        df = pd.read_parquet(vol_path)
    else:
        df = update_volatility_raw()

    if df.empty:
        return pd.DataFrame()

    # Select relevant columns for MOVE vs VIX chart
    cols = ['VIX', 'MOVE_Proxy', 'VIX_MOVE_Ratio', 'VIX_MOVE_Corr_60D', 'VIX_Premium']
    available = [c for c in cols if c in df.columns]

    return df[available].dropna(how='all')


if __name__ == "__main__":
    df = update_volatility_raw()
    print(f"\nFetched columns: {list(df.columns)}")
    print(df.tail(10))
