from pathlib import Path

# ---------------------------------------------------------
# UPDATE FRED COLLECTOR (2000 Days)
# ---------------------------------------------------------
fred_code = """import pandas as pd
import requests
import numpy as np
from ..config import CONFIG
from ..utils.logging import get_logger
from ..utils.io import write_parquet

log = get_logger(__name__)

FRED_SERIES_MAP = {
    "RRPONTSYD": "RRP_Balance",
    "WRESBAL": "Bank_Reserves",
    "GDP": "GDP",
    "UNRATE": "UNRATE",
    "DGS10": "UST10Y",
    "BAMLH0A0HYM2": "HY_OAS"
}

def update_fred_raw():
    log.info("Updating FRED data...")
    
    # CHANGED: Increased from 500 to 2000 days to support long-window indicators
    dates = pd.date_range(end=pd.Timestamp.today(), periods=2000, freq='D')
    data = {}
    
    # Synthetic Data Generation
    data["RRP_Balance"] = np.random.normal(2000, 100, 2000)  # Billions
    data["Bank_Reserves"] = np.random.normal(3000, 150, 2000)
    data["GDP"] = np.linspace(20000, 25000, 2000)
    data["UNRATE"] = np.random.normal(4.0, 0.2, 2000)
    data["UST10Y"] = np.random.normal(4.0, 0.5, 2000)
    data["HY_OAS"] = np.random.normal(3.5, 0.8, 2000)

    df = pd.DataFrame(data, index=dates)
    
    out_path = CONFIG.raw_dir / "fred" / "fred_raw.parquet"
    write_parquet(df, out_path)
    log.info("FRED data updated (Synthetic - 2000 Days).")
    return df
"""

# ---------------------------------------------------------
# UPDATE CRYPTO COLLECTOR (2000 Days)
# ---------------------------------------------------------
crypto_code = """import pandas as pd
import numpy as np
from ..config import CONFIG
from ..utils.logging import get_logger
from ..utils.io import write_parquet

log = get_logger(__name__)

def update_crypto_raw():
    log.info("Updating Crypto data...")
    
    # CHANGED: Increased from 500 to 2000 days
    dates = pd.date_range(end=pd.Timestamp.today(), periods=2000, freq='D')
    data = {}
    
    # Synthetic Crypto Data
    data["BTC_CLOSE"] = np.linspace(30000, 65000, 2000) + np.random.normal(0, 1000, 2000)
    data["BTC_MVRV_RATIO"] = np.random.normal(1.8, 0.4, 2000)
    data["TOTAL_STABLECOIN_SUPPLY"] = np.linspace(120e9, 140e9, 2000)
    
    df = pd.DataFrame(data, index=dates)
    
    out_path = CONFIG.raw_dir / "crypto" / "crypto_raw.parquet"
    write_parquet(df, out_path)
    log.info("Crypto data updated (Synthetic - 2000 Days).")
    return df
"""

# Write the updates
base_path = Path("lighthouse_data/collect")
with open(base_path / "fred.py", "w") as f:
    f.write(fred_code)
print("Patched fred.py")

with open(base_path / "crypto.py", "w") as f:
    f.write(crypto_code)
print("Patched crypto.py")
