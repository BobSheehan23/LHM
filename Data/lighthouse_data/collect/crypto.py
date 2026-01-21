import pandas as pd
import numpy as np
import san
import ccxt
from dune_client.client import DuneClient
from ..config import CONFIG
from ..utils.logging import get_logger
from ..utils.io import write_parquet

log = get_logger(__name__)

def fetch_santiment_data():
    api_key = CONFIG.santiment_api_key
    if not api_key:
        log.warning("No Santiment API key found.")
        return pd.DataFrame()

    log.info("Fetching MVRV Ratio from Santiment...")
    try:
        san.ApiConfig.api_key = api_key
        # Fetch Bitcoin MVRV Ratio (365d is standard for macro)
        df = san.get(
            "mvrv_usd_365d",
            slug="bitcoin",
            from_date="2018-01-01",
            to_date="utc_now",
            interval="1d"
        )
        if df is None or df.empty:
            return pd.DataFrame()
            
        df.index = pd.to_datetime(df.index).tz_localize(None)
        return df.rename(columns={'value': 'BTC_MVRV_RATIO'})
    except Exception as e:
        log.error(f"Santiment fetch failed: {e}")
        return pd.DataFrame()

def fetch_ccxt_price():
    log.info("Fetching BTC Price from Coinbase via CCXT...")
    try:
        exchange = ccxt.coinbase()
        ohlcv = exchange.fetch_ohlcv('BTC/USD', timeframe='1d', limit=2000)
        
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df.set_index('date')[['close']].rename(columns={'close': 'BTC_CLOSE'})
    except Exception as e:
        log.error(f"CCXT Price fetch failed: {e}")
        return pd.DataFrame()

def update_crypto_raw():
    log.info("Starting REAL Crypto Data Update...")
    
    san_df = fetch_santiment_data()
    price_df = fetch_ccxt_price()
    
    stable_df = pd.DataFrame()
    if CONFIG.santiment_api_key:
        try:
            log.info("Fetching USDT Supply from Santiment...")
            usdt = san.get("total_supply", slug="tether", from_date="2018-01-01", to_date="utc_now", interval="1d")
            if usdt is not None and not usdt.empty:
                usdt.index = pd.to_datetime(usdt.index).tz_localize(None)
                stable_df = usdt.rename(columns={'value': 'TOTAL_STABLECOIN_SUPPLY'})
        except Exception as e:
            log.warning(f"Stablecoin fetch warning: {e}")

    # Merge all sources
    dfs = [d for d in [san_df, price_df, stable_df] if not d.empty]
    if not dfs:
        log.error("No crypto data fetched!")
        return pd.DataFrame()
        
    df = pd.concat(dfs, axis=1).sort_index()
    
    # AGGRESSIVE FILLING: 
    # 1. Forward fill (propagate last valid value forward)
    # 2. Backward fill (handle missing start data if needed)
    df = df.ffill().bfill()
    
    # Normalize to midnight
    df.index = df.index.normalize()
    
    # Remove duplicates
    df = df[~df.index.duplicated(keep='last')]

    out_path = CONFIG.raw_dir / "crypto" / "crypto_raw.parquet"
    write_parquet(df, out_path)
    log.info(f"Crypto raw data updated successfully. Shape: {df.shape}")
    return df
