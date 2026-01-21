import yfinance as yf
import pandas as pd
from ..config import CONFIG
from ..utils.logging import get_logger
from ..utils.io import write_parquet

log = get_logger(__name__)

# Tickers to Fetch
MARKET_TICKERS = {
    "^GSPC": "SPX",          # S&P 500
    "GC=F": "Gold",          # Gold Futures
    "DX-Y.NYB": "DXY",       # US Dollar Index
    "^IXIC": "Nasdaq",       # Nasdaq Composite
    "^RUT": "Russell2000"    # Small Caps
}

def update_market_raw():
    log.info("Fetching MARKET data (SPX, Gold, DXY)...")
    
    frames = {}
    for ticker, name in MARKET_TICKERS.items():
        try:
            # Fetch full history
            data = yf.download(ticker, start="2000-01-01", progress=False, auto_adjust=True)
            
            if data.empty:
                log.warning(f"No data for {ticker}")
                continue
                
            # Fix for MultiIndex columns in recent yfinance versions
            if isinstance(data.columns, pd.MultiIndex):
                # If columns look like ('Close', '^GSPC'), drop the ticker level
                data.columns = data.columns.get_level_values(0)

            # Select just the Close price
            if 'Close' in data.columns:
                series = data['Close']
            elif 'Adj Close' in data.columns:
                series = data['Adj Close']
            else:
                # Fallback: grab first column
                series = data.iloc[:, 0]

            # Clean up
            series.name = name
            series.index = pd.to_datetime(series.index).normalize()
            
            # Remove timezone if present (to match FRED data)
            if series.index.tz is not None:
                series.index = series.index.tz_localize(None)
                
            frames[name] = series
            
        except Exception as e:
            log.error(f"Failed to fetch {ticker}: {e}")

    if not frames:
        return pd.DataFrame()

    # Combine all series into a single flat DataFrame
    df = pd.concat(frames, axis=1)
    
    # Forward fill weekends/holidays for macro alignment
    df = df.asfreq('D').ffill()

    out_path = CONFIG.raw_dir / "market" / "market_raw.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    write_parquet(df, out_path)
    
    log.info(f"Market data updated successfully. Shape: {df.shape}")
    return df
