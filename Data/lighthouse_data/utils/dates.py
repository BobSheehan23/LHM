import pandas as pd

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
