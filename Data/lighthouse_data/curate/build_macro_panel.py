import pandas as pd
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
