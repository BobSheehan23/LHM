from pathlib import Path

real_fred_code = """import pandas as pd
import requests
import numpy as np
from ..config import CONFIG
from ..utils.logging import get_logger
from ..utils.io import write_parquet

log = get_logger(__name__)

# Map FRED Series IDs to Lighthouse Names
FRED_SERIES_MAP = {
    "RRPONTSYD": "RRP_Balance",      # Overnight Reverse Repurchase Agreements
    "WRESBAL": "Bank_Reserves",      # Reserve Balances with Federal Reserve Banks
    "GDP": "GDP",                    # Gross Domestic Product
    "UNRATE": "UNRATE",              # Unemployment Rate
    "DGS10": "UST10Y",               # Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity
    "BAMLH0A0HYM2": "HY_OAS"         # ICE BofA US High Yield Index Option-Adjusted Spread
}

def fetch_series(series_id, api_key):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": "2018-01-01"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json().get('observations', [])
        
        if not data:
            log.warning(f"No data returned for {series_id}")
            return None
            
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        
        # Handle "." strings which FRED uses for missing data
        df = df.dropna(subset=['value'])
        
        return df.set_index('date')['value']
    except Exception as e:
        log.error(f"Failed to fetch {series_id}: {str(e)}")
        return None

def update_fred_raw():
    api_key = CONFIG.fred_api_key
    if not api_key:
        log.error("FRED_API_KEY is missing! Cannot fetch real data.")
        return pd.DataFrame()
    
    log.info("Fetching REAL data from FRED API...")
    
    frames = {}
    for fred_id, internal_name in FRED_SERIES_MAP.items():
        log.info(f"Requesting {fred_id}...")
        series = fetch_series(fred_id, api_key)
        if series is not None:
            frames[internal_name] = series
            
    if not frames:
        log.error("Failed to fetch any series.")
        return pd.DataFrame()

    df = pd.DataFrame(frames)
    
    # Resample to daily to align disparate frequencies (Monthly GDP vs Daily Rates)
    # ffill() propagates the last known value forward (standard macro practice)
    df = df.resample('D').ffill()
    
    out_path = CONFIG.raw_dir / "fred" / "fred_raw.parquet"
    write_parquet(df, out_path)
    log.info(f"FRED data updated successfully. Shape: {df.shape}")
    return df
"""

# Overwrite the file
base_path = Path("lighthouse_data/collect")
with open(base_path / "fred.py", "w") as f:
    f.write(real_fred_code)
print("Successfully upgraded fred.py to use real API data.")
