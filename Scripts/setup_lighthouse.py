import os
from pathlib import Path

# Base directory for the project
BASE_DIR = Path("lighthouse_mega")

# File contents defined as a dictionary
files = {
    # ---------------------------------------------------------
    # ROOT FILES
    # ---------------------------------------------------------
    "requirements.txt": """pandas>=2.0.0
numpy>=1.26.0
pyyaml>=6.0
requests>=2.31.0
python-dateutil>=2.8.2
matplotlib>=3.8.0
seaborn>=0.13.0
scikit-learn>=1.4.0
xgboost>=2.0.0
sanpy>=0.8.0
dune-client>=1.10.0
ccxt>=4.1.66
""",
    
    "pyproject.toml": """[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "lighthouse-data"
version = "0.1.0"
description = "Lighthouse Macro Mega Data Warehouse"
authors = [
  { name="Bob Sheehan", email="bob@lighthousemacro.com" }
]
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
  "pandas", "numpy", "pyyaml", "requests", "sanpy", "dune-client", "ccxt"
]

[tool.setuptools.packages.find]
where = ["."]
include = ["lighthouse_data*"]
""",

    "README.md": """# Lighthouse Mega Data Warehouse
Institutional-grade macro data pipeline.
Run `pip install -r requirements.txt` then `python scripts/daily_update.py`.
""",

    # ---------------------------------------------------------
    # CORE PACKAGE: CONFIG & UTILS
    # ---------------------------------------------------------
    "lighthouse_data/__init__.py": "",
    
    "lighthouse_data/config.py": """from pathlib import Path
from dataclasses import dataclass
import os

@dataclass
class DataConfig:
    base_dir: Path = Path(__file__).resolve().parents[1]
    data_dir: Path = base_dir / "data"
    raw_dir: Path = data_dir / "raw"
    curated_dir: Path = data_dir / "curated"
    indicators_dir: Path = data_dir / "indicators"
    logs_dir: Path = base_dir / "logs"
    
    # API Keys (set these in your environment variables for security)
    fred_api_key: str | None = os.environ.get('FRED_API_KEY')
    santiment_api_key: str | None = os.environ.get('SANTIMENT_API_KEY')
    dune_api_key: str | None = os.environ.get('DUNE_API_KEY')
    coinglass_api_key: str | None = os.environ.get('COINGLASS_API_KEY')

    def ensure_dirs(self) -> None:
        for p in [self.data_dir, self.raw_dir, self.curated_dir, self.indicators_dir, self.logs_dir]:
            p.mkdir(parents=True, exist_ok=True)

CONFIG = DataConfig()
CONFIG.ensure_dirs()
""",

    "lighthouse_data/utils/__init__.py": "",
    
    "lighthouse_data/utils/logging.py": """import logging
from ..config import CONFIG

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Console Handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # File Handler
        fh = logging.FileHandler(CONFIG.logs_dir / "lighthouse.log")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger
""",

    "lighthouse_data/utils/io.py": """import pandas as pd
from pathlib import Path

def read_parquet(path: Path) -> pd.DataFrame:
    return pd.read_parquet(path)

def write_parquet(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path)
""",

    "lighthouse_data/utils/dates.py": """import pandas as pd

def to_daily_index(df: pd.DataFrame) -> pd.DataFrame:
    # Resample to daily frequency and forward fill
    if not isinstance(df.index, pd.DatetimeIndex):
        try:
            df.index = pd.to_datetime(df.index)
        except:
            return df
    
    df = df.sort_index()
    # Handle duplicates by taking the last value
    df = df[~df.index.duplicated(keep='last')]
    
    # Resample to Daily 'D' and forward fill
    return df.asfreq('D').ffill()
""",

    # ---------------------------------------------------------
    # CATALOGS
    # ---------------------------------------------------------
    "lighthouse_data/catalog/__init__.py": "",
    
    "lighthouse_data/catalog/datasets.yaml": """datasets:
  fred_us_macro:
    source: "FRED"
    loader: "lighthouse_data.collect.fred.update_fred_raw"
    storage: "data/raw/fred/fred_raw.parquet"
  crypto_raw:
    source: "Multi-API"
    loader: "lighthouse_data.collect.crypto.update_crypto_raw"
    storage: "data/raw/crypto/crypto_raw.parquet"
""",

    "lighthouse_data/catalog/indicators.yaml": """indicators:
  LCI:
    description: "Liquidity Cushion Index"
    function: "lighthouse_data.indicators.core.compute_lci"
  MRI:
    description: "Macro Risk Index"
    function: "lighthouse_data.indicators.core.compute_mri"
  Stablecoin_Momentum:
    description: "Crypto M2 Proxy"
    function: "lighthouse_data.indicators.core.compute_stablecoin_momentum"
""",

    # ---------------------------------------------------------
    # FEATURES & TRANSFORMS
    # ---------------------------------------------------------
    "lighthouse_data/features/__init__.py": "",
    
    "lighthouse_data/features/transforms_core.py": """import pandas as pd
import numpy as np

def zscore(s: pd.Series, window: int = 252) -> pd.Series:
    r = s.rolling(window)
    return (s - r.mean()) / r.std()

def rolling_vol(s: pd.Series, window: int = 21) -> pd.Series:
    return s.pct_change().rolling(window).std() * np.sqrt(252)

def rolling_mean(s: pd.Series, window: int = 200) -> pd.Series:
    return s.rolling(window).mean()
""",

    # ---------------------------------------------------------
    # COLLECTORS
    # ---------------------------------------------------------
    "lighthouse_data/collect/__init__.py": "",

    "lighthouse_data/collect/fred.py": """import pandas as pd
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
    # NOTE: In a real run, you would use requests.get() with CONFIG.fred_api_key
    # For this setup to be runnable immediately, we generate synthetic data
    
    dates = pd.date_range(end=pd.Timestamp.today(), periods=500, freq='D')
    data = {}
    
    # Synthetic Data Generation
    data["RRP_Balance"] = np.random.normal(2000, 100, 500)  # Billions
    data["Bank_Reserves"] = np.random.normal(3000, 150, 500)
    data["GDP"] = np.linspace(20000, 25000, 500)
    data["UNRATE"] = np.random.normal(4.0, 0.2, 500)
    data["UST10Y"] = np.random.normal(4.0, 0.5, 500)
    data["HY_OAS"] = np.random.normal(3.5, 0.8, 500)

    df = pd.DataFrame(data, index=dates)
    
    out_path = CONFIG.raw_dir / "fred" / "fred_raw.parquet"
    write_parquet(df, out_path)
    log.info("FRED data updated (Synthetic).")
    return df
""",

    "lighthouse_data/collect/crypto.py": """import pandas as pd
import numpy as np
from ..config import CONFIG
from ..utils.logging import get_logger
from ..utils.io import write_parquet

log = get_logger(__name__)

def update_crypto_raw():
    log.info("Updating Crypto data...")
    # NOTE: Real implementation uses sanpy/dune-client/ccxt
    # Simulating for immediate functionality
    
    dates = pd.date_range(end=pd.Timestamp.today(), periods=500, freq='D')
    data = {}
    
    # Synthetic Crypto Data
    data["BTC_CLOSE"] = np.linspace(30000, 65000, 500) + np.random.normal(0, 1000, 500)
    data["BTC_MVRV_RATIO"] = np.random.normal(1.8, 0.4, 500)
    data["TOTAL_STABLECOIN_SUPPLY"] = np.linspace(120e9, 140e9, 500)
    
    df = pd.DataFrame(data, index=dates)
    
    out_path = CONFIG.raw_dir / "crypto" / "crypto_raw.parquet"
    write_parquet(df, out_path)
    log.info("Crypto data updated (Synthetic).")
    return df
""",

    # ---------------------------------------------------------
    # CURATION & PANELS
    # ---------------------------------------------------------
    "lighthouse_data/curate/__init__.py": "",

    "lighthouse_data/curate/build_macro_panel.py": """import pandas as pd
from ..config import CONFIG
from ..utils.io import read_parquet, write_parquet
from ..utils.dates import to_daily_index
from ..collect.fred import update_fred_raw

def build_macro_panel():
    path = CONFIG.raw_dir / "fred" / "fred_raw.parquet"
    if not path.exists():
        update_fred_raw()
    
    df = read_parquet(path)
    df_daily = to_daily_index(df)
    write_parquet(df_daily, CONFIG.curated_dir / "macro_master_panel.parquet")
    return df_daily
""",

    "lighthouse_data/curate/build_crypto_panel.py": """import pandas as pd
from ..config import CONFIG
from ..utils.io import read_parquet, write_parquet
from ..utils.dates import to_daily_index
from ..collect.crypto import update_crypto_raw

def build_crypto_panel():
    path = CONFIG.raw_dir / "crypto" / "crypto_raw.parquet"
    if not path.exists():
        update_crypto_raw()
    
    df = read_parquet(path)
    df_daily = to_daily_index(df)
    write_parquet(df_daily, CONFIG.curated_dir / "crypto_master_panel.parquet")
    return df_daily
""",

    "lighthouse_data/curate/build_chartbook_panel.py": """import pandas as pd
from ..config import CONFIG
from ..utils.io import read_parquet, write_parquet
from ..utils.dates import to_daily_index

def build_chartbook_panel():
    macro = read_parquet(CONFIG.curated_dir / "macro_master_panel.parquet")
    crypto = read_parquet(CONFIG.curated_dir / "crypto_master_panel.parquet")
    
    # Outer join to align timestamps
    df = macro.join(crypto, how='outer')
    df = to_daily_index(df)
    
    write_parquet(df, CONFIG.curated_dir / "chartbook_master_data.parquet")
    return df
""",

    # ---------------------------------------------------------
    # INDICATORS
    # ---------------------------------------------------------
    "lighthouse_data/indicators/__init__.py": "",

    "lighthouse_data/indicators/core.py": """import pandas as pd
from ..features.transforms_core import zscore
from ..config import CONFIG
from ..utils.io import write_parquet
from ..utils.logging import get_logger

log = get_logger(__name__)

def compute_lci(df):
    if not {"RRP_Balance", "Bank_Reserves", "GDP"}.issubset(df.columns): return None
    rrp_gdp = df["RRP_Balance"] / df["GDP"]
    res_gdp = df["Bank_Reserves"] / df["GDP"]
    return (zscore(rrp_gdp) + zscore(res_gdp)) / 2

def compute_stablecoin_momentum(df):
    if "TOTAL_STABLECOIN_SUPPLY" not in df.columns: return None
    growth = df["TOTAL_STABLECOIN_SUPPLY"].pct_change(periods=90)
    return zscore(growth)

def compute_btc_risk_premium(df):
    if "BTC_MVRV_RATIO" not in df.columns: return None
    return zscore(df["BTC_MVRV_RATIO"], window=504)

def compute_all_indicators(panel: pd.DataFrame):
    log.info("Computing proprietary indicators...")
    ind = pd.DataFrame(index=panel.index)
    
    # 1. Liquidity Indicators
    ind["LCI"] = compute_lci(panel)
    
    # 2. Crypto Indicators
    ind["Stablecoin_Momentum"] = compute_stablecoin_momentum(panel)
    ind["BTC_Risk_Premium"] = compute_btc_risk_premium(panel)
    
    # 3. Macro Risk Index (Simplified for now)
    # MRI requires LFI/LDI which we'll add next, using LCI and Credit for now
    if "HY_OAS" in panel.columns and "LCI" in ind.columns:
        hy_z = zscore(panel["HY_OAS"])
        ind["MRI"] = hy_z - ind["LCI"]
    
    write_parquet(ind, CONFIG.indicators_dir / "indicators_daily.parquet")
    return ind
""",

    # ---------------------------------------------------------
    # ORCHESTRATION & SCRIPTS
    # ---------------------------------------------------------
    "lighthouse_data/orchestration/__init__.py": "",

    "lighthouse_data/orchestration/daily_flows.py": """from ..config import CONFIG
from ..collect.fred import update_fred_raw
from ..collect.crypto import update_crypto_raw
from ..curate.build_macro_panel import build_macro_panel
from ..curate.build_crypto_panel import build_crypto_panel
from ..curate.build_chartbook_panel import build_chartbook_panel
from ..indicators.core import compute_all_indicators
from ..utils.logging import get_logger

log = get_logger(__name__)

class DailyFlow:
    def run_all(self):
        CONFIG.ensure_dirs()
        log.info("=== STARTING LIGHTHOUSE MACRO DAILY FLOW ===")
        
        # 1. Collect
        update_fred_raw()
        update_crypto_raw()
        
        # 2. Curate
        build_macro_panel()
        build_crypto_panel()
        chartbook = build_chartbook_panel()
        
        # 3. Compute
        indicators = compute_all_indicators(chartbook)
        
        log.info("=== FLOW COMPLETE ===")
        print(f"Latest Indicators:\\n{indicators.tail(3)}")
""",

    "scripts/daily_update.py": """import sys
import os

# Add project root to python path so we can import lighthouse_data
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lighthouse_data.orchestration.daily_flows import DailyFlow

if __name__ == "__main__":
    DailyFlow().run_all()
"""
}

def create_structure():
    # Create the base project directory
    if not BASE_DIR.exists():
        BASE_DIR.mkdir()
        print(f"Created project directory: {BASE_DIR}")

    # Create directories and write files
    for file_path_str, content in files.items():
        full_path = BASE_DIR / file_path_str
        
        # Ensure parent directory exists
        if not full_path.parent.exists():
            full_path.parent.mkdir(parents=True)
            print(f"Created directory: {full_path.parent}")
            
        # Write file content
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Wrote file: {full_path}")

    print("\n" + "="*50)
    print("LIGHTHOUSE MACRO DATA STACK GENERATED SUCCESSFULLY")
    print("="*50)
    print("Next steps:")
    print(f"1. cd {BASE_DIR}")
    print("2. pip install -r requirements.txt")
    print("3. python scripts/daily_update.py")

if __name__ == "__main__":
    create_structure()
