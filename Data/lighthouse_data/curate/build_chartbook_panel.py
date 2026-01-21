import pandas as pd
from ..config import CONFIG
from ..utils.io import read_parquet, write_parquet
from ..utils.dates import to_daily_index

def build_chartbook_panel():
    # Load Panels
    macro = read_parquet(CONFIG.curated_dir / "macro_master_panel.parquet")
    crypto = read_parquet(CONFIG.curated_dir / "crypto_master_panel.parquet")
    
    # Load & Curate Market Data (New)
    market_path = CONFIG.raw_dir / "market" / "market_raw.parquet"
    if market_path.exists():
        market = read_parquet(market_path)
    else:
        market = pd.DataFrame()

    # Merge All (Macro + Crypto + Market)
    # We use 'outer' join to keep all history
    df = macro.join(crypto, how='outer').join(market, how='outer')
    
    # Final Clean
    df = to_daily_index(df)
    
    write_parquet(df, CONFIG.curated_dir / "chartbook_master_data.parquet")
    return df
