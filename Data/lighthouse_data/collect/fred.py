import pandas as pd
import requests
import numpy as np
from ..config import CONFIG
from ..utils.logging import get_logger
from ..utils.io import write_parquet

log = get_logger(__name__)

# Map FRED Series IDs to Lighthouse Names
FRED_SERIES_MAP = {
    # --- LIQUIDITY & RATES ---
    "RRPONTSYD": "RRP_Balance",      # Overnight Reverse Repurchase Agreements
    "WRESBAL": "Bank_Reserves",      # Reserve Balances
    "DGS10": "UST10Y",               # 10Y Treasury Yield
    "BAMLH0A0HYM2": "HY_OAS",        # High Yield Spreads
    
    # --- MACRO GROWTH ---
    "GDP": "GDP",                    # Gross Domestic Product
    "UNRATE": "UNRATE",              # Headline Unemployment Rate
    
    # --- DEEP LABOR DYNAMICS (NEW) ---
    "JTSJOL": "Job_Openings",        # JOLTS Openings (Total)
    "JTSQUR": "Quits_Rate",          # JOLTS Quits Rate (Voluntary Separations)
    "JTSHIL": "Hires_Level",         # JOLTS Hires Level
    "JTSQUL": "Quits_Level",         # JOLTS Quits Level (for ratios)
    "JTSLDL": "Layoffs_Level",       # JOLTS Layoffs Level
    "UEMP27OV": "Unemp_27_Weeks",    # Civilians Unemployed 27 Weeks +
    "UNEMPLOY": "Unemp_Total"        # Total Unemployed (Level)
}

def fetch_series(series_id, api_key):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": "2015-01-01" # Need history for Z-scores
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
        df = df.dropna(subset=['value'])
        
        return df.set_index('date')['value']
    except Exception as e:
        log.error(f"Failed to fetch {series_id}: {str(e)}")
        return None

def update_fred_raw():
    api_key = CONFIG.fred_api_key
    if not api_key:
        log.error("FRED_API_KEY is missing!")
        return pd.DataFrame()
    
    log.info("Fetching MACRO & LABOR data from FRED...")
    
    frames = {}
    for fred_id, internal_name in FRED_SERIES_MAP.items():
        log.info(f"Requesting {fred_id} ({internal_name})...")
        series = fetch_series(fred_id, api_key)
        if series is not None:
            frames[internal_name] = series
            
    if not frames:
        log.error("Failed to fetch any series.")
        return pd.DataFrame()

    df = pd.DataFrame(frames)
    
    # Resample to daily to align disparate frequencies (Monthly JOLTS vs Daily Rates)
    df = df.resample('D').ffill()
    
    out_path = CONFIG.raw_dir / "fred" / "fred_raw.parquet"
    write_parquet(df, out_path)
    log.info(f"FRED data updated successfully. Shape: {df.shape}")
    return df
