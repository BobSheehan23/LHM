from pathlib import Path

# ---------------------------------------------------------
# 1. UPGRADE FRED COLLECTOR (Add Labor Series)
# ---------------------------------------------------------
new_fred_code = """import pandas as pd
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
"""

# ---------------------------------------------------------
# 2. UPGRADE INDICATORS (Add LFI & LDI Logic)
# ---------------------------------------------------------
new_indicator_code = """import pandas as pd
import numpy as np
from ..features.transforms_core import zscore
from ..config import CONFIG
from ..utils.io import write_parquet
from ..utils.logging import get_logger

log = get_logger(__name__)

def compute_lci(df: pd.DataFrame) -> pd.Series:
    if not {"RRP_Balance", "Bank_Reserves", "GDP"}.issubset(df.columns): return None
    rrp_gdp = df["RRP_Balance"] / df["GDP"]
    res_gdp = df["Bank_Reserves"] / df["GDP"]
    return (zscore(rrp_gdp) + zscore(res_gdp)) / 2

def compute_lfi(df: pd.DataFrame) -> pd.Series:
    # Labor Fragility Index (LFI)
    # High LFI = Structural Weakness (Bad)
    # Components: Long-Term Unemp Share (+), Quits (-), Hires/Quits (-)
    
    required = {"Unemp_27_Weeks", "Unemp_Total", "Quits_Rate", "Hires_Level", "Quits_Level"}
    if not required.issubset(df.columns): return None
    
    # 1. Long Duration Share (Rising = Bad)
    long_share = df["Unemp_27_Weeks"] / df["Unemp_Total"]
    
    # 2. Quits Rate (Falling = Bad, so we invert sign for Fragility)
    quits = -df["Quits_Rate"]
    
    # 3. Hires to Quits Ratio (Falling = Bad, invert sign)
    hires_quits = -(df["Hires_Level"] / df["Quits_Level"])
    
    return (zscore(long_share) + zscore(quits) + zscore(hires_quits)) / 3

def compute_ldi(df: pd.DataFrame) -> pd.Series:
    # Labor Dynamism Index (LDI)
    # High LDI = Confidence/Churn (Good)
    
    required = {"Quits_Rate", "Hires_Level", "Quits_Level", "Layoffs_Level"}
    if not required.issubset(df.columns): return None
    
    quits_rate = df["Quits_Rate"]
    hires_quits = df["Hires_Level"] / df["Quits_Level"]
    
    # Avoid div by zero on layoffs
    layoffs = df["Layoffs_Level"].replace(0, np.nan) 
    quits_layoffs = df["Quits_Level"] / layoffs
    
    return (zscore(quits_rate) + zscore(hires_quits) + zscore(quits_layoffs)) / 3

def compute_stablecoin_momentum(df: pd.DataFrame) -> pd.Series:
    if "TOTAL_STABLECOIN_SUPPLY" not in df.columns: return None
    growth = df["TOTAL_STABLECOIN_SUPPLY"].pct_change(periods=90)
    return zscore(growth)

def compute_btc_risk_premium(df: pd.DataFrame) -> pd.Series:
    if "BTC_MVRV_RATIO" not in df.columns: return None
    return zscore(df["BTC_MVRV_RATIO"], window=504)

def compute_mri(df: pd.DataFrame, lci: pd.Series, lfi: pd.Series, ldi: pd.Series) -> pd.Series:
    # Macro Risk Index (Master Composite)
    # MRI = LFI - LDI - LCI + Credit Stress
    
    hy_z = zscore(df["HY_OAS"]) if "HY_OAS" in df.columns else 0
    
    # Handle missing series gracefully
    lfi_val = lfi if lfi is not None else 0
    ldi_val = ldi if ldi is not None else 0
    lci_val = lci if lci is not None else 0
    
    # Formula: Fragility + Credit Stress - Dynamism - Liquidity
    return lfi_val - ldi_val + hy_z - lci_val

def compute_all_indicators(panel: pd.DataFrame):
    log.info("Computing proprietary indicators...")
    ind = pd.DataFrame(index=panel.index)
    
    # Base Indicators
    ind["LCI"] = compute_lci(panel)
    ind["LFI"] = compute_lfi(panel) # NEW
    ind["LDI"] = compute_ldi(panel) # NEW
    
    # Crypto
    ind["Stablecoin_Momentum"] = compute_stablecoin_momentum(panel)
    ind["BTC_Risk_Premium"] = compute_btc_risk_premium(panel)
    
    # Master Composite
    ind["MRI"] = compute_mri(panel, ind["LCI"], ind["LFI"], ind["LDI"])
    
    write_parquet(ind, CONFIG.indicators_dir / "indicators_daily.parquet")
    return ind
"""

# Overwrite files
base_path_collect = Path("lighthouse_data/collect")
base_path_indicators = Path("lighthouse_data/indicators")

with open(base_path_collect / "fred.py", "w") as f:
    f.write(new_fred_code)
print("Upgraded: fred.py (Added JOLTS/Labor series)")

with open(base_path_indicators / "core.py", "w") as f:
    f.write(new_indicator_code)
print("Upgraded: indicators/core.py (Added LFI/LDI Logic)")
