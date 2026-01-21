import pandas as pd
import numpy as np

def zscore(s: pd.Series, window: int = 252) -> pd.Series:
    r = s.rolling(window)
    return (s - r.mean()) / r.std()

def rolling_vol(s: pd.Series, window: int = 21) -> pd.Series:
    return s.pct_change().rolling(window).std() * np.sqrt(252)

def rolling_mean(s: pd.Series, window: int = 200) -> pd.Series:
    return s.rolling(window).mean()
