"""
Extended FRED Data Collection for Priority 1 Charts
Lighthouse Macro - January 2026

New Series:
- TGA Balance (Treasury General Account)
- Fed Balance Sheet (WALCL)
- Real Rates & Breakevens
- Bank Lending Standards (SLOOS)
- Money Market Fund Assets
- Dollar Index proxy data
"""

import pandas as pd
import requests
from ..config import CONFIG
from ..utils.logging import get_logger
from ..utils.io import write_parquet

log = get_logger(__name__)

# Extended FRED Series Map for Priority 1 Charts
FRED_EXTENDED_MAP = {
    # === TGA & FED BALANCE SHEET ===
    "WTREGEN": "TGA_Balance",           # Treasury General Account (Weekly)
    "WALCL": "Fed_Total_Assets",        # Fed Total Assets (Balance Sheet)
    "WRESBAL": "Bank_Reserves",         # Reserve Balances (already in core, duplicate for completeness)
    "RRPONTSYD": "RRP_Balance",         # Reverse Repo (already in core)

    # === REAL RATES & INFLATION EXPECTATIONS ===
    "DFII10": "TIPS_10Y",               # 10-Year TIPS Real Yield
    "DFII5": "TIPS_5Y",                 # 5-Year TIPS Real Yield
    "T10YIE": "Breakeven_10Y",          # 10-Year Breakeven Inflation
    "T5YIE": "Breakeven_5Y",            # 5-Year Breakeven Inflation
    "T5YIFR": "Forward_5Y5Y",           # 5-Year, 5-Year Forward Inflation Expectation

    # === BANK LENDING STANDARDS (SLOOS) ===
    "DRTSCILM": "SLOOS_CandI_Large",    # Net % Tightening: C&I Loans to Large Firms
    "DRTSCLCC": "SLOOS_Consumer_Credit", # Net % Tightening: Consumer Credit Cards
    "SUBLPDRCSC": "SLOOS_Subprime_Auto", # Subprime Auto Loan Delinquency (related)

    # === MONEY MARKET FUNDS ===
    "MMMFFAQ027S": "MMF_Total_Assets",  # Money Market Funds Total Financial Assets
    "WRMFSL": "Retail_MMF",             # Retail Money Market Funds
    "WIMFSL": "Inst_MMF",               # Institutional Money Market Funds

    # === DOLLAR & TRADE ===
    "DTWEXBGS": "Trade_Weighted_USD",   # Trade Weighted U.S. Dollar Index: Broad
    "DTWEXAFEGS": "USD_vs_AFE",         # USD vs Advanced Foreign Economies
    "DTWEXEMEGS": "USD_vs_EME",         # USD vs Emerging Market Economies

    # === TREASURY YIELDS (Full Curve) ===
    "DGS1MO": "UST_1M",
    "DGS3MO": "UST_3M",
    "DGS6MO": "UST_6M",
    "DGS1": "UST_1Y",
    "DGS2": "UST_2Y",
    "DGS5": "UST_5Y",
    "DGS10": "UST_10Y",
    "DGS20": "UST_20Y",
    "DGS30": "UST_30Y",

    # === TERM PREMIUM (ACM Model) ===
    "THREEFYTP10": "Term_Premium_10Y",  # 10-Year Term Premium (ACM)

    # === FUNDING RATES ===
    "SOFR": "SOFR",                     # Secured Overnight Financing Rate
    "EFFR": "EFFR",                     # Effective Federal Funds Rate
    "OBFR": "OBFR",                     # Overnight Bank Funding Rate

    # === CREDIT SPREADS (Additional) ===
    "BAMLC0A1CAAAEY": "AAA_OAS",        # AAA Corporate OAS
    "BAMLC0A2CAAEY": "AA_OAS",          # AA Corporate OAS
    "BAMLC0A3CAEY": "A_OAS",            # A Corporate OAS
    "BAMLC0A4CBBBEY": "BBB_OAS",        # BBB Corporate OAS
    "BAMLH0A0HYM2EY": "HY_OAS",         # High Yield OAS

    # === CONSUMER METRICS ===
    "PSAVERT": "Savings_Rate",          # Personal Savings Rate
    "TOTALSL": "Consumer_Credit_Total", # Total Consumer Credit
    "DRCCLACBS": "CC_Delinquency_Rate", # Credit Card Delinquency Rate
    "DRSFRMACBS": "Mortgage_Delinq",    # Mortgage Delinquency Rate
}


def fetch_fred_series(series_id: str, api_key: str, start_date: str = "2010-01-01") -> pd.Series | None:
    """Fetch a single FRED series with error handling."""
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": start_date
    }

    try:
        response = requests.get(url, params=params, timeout=15)
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


def update_fred_extended(start_date: str = "2010-01-01") -> pd.DataFrame:
    """
    Fetch all extended FRED series for Priority 1 charts.

    Returns:
        DataFrame with all series, resampled to daily frequency
    """
    api_key = CONFIG.fred_api_key
    if not api_key:
        log.error("FRED_API_KEY is missing!")
        return pd.DataFrame()

    log.info("Fetching EXTENDED FRED data for Priority 1 charts...")

    frames = {}
    total = len(FRED_EXTENDED_MAP)

    for i, (fred_id, internal_name) in enumerate(FRED_EXTENDED_MAP.items(), 1):
        log.info(f"[{i}/{total}] Requesting {fred_id} ({internal_name})...")
        series = fetch_fred_series(fred_id, api_key, start_date)
        if series is not None:
            frames[internal_name] = series

    if not frames:
        log.error("Failed to fetch any series.")
        return pd.DataFrame()

    df = pd.DataFrame(frames)

    # Resample to daily to align disparate frequencies
    df = df.resample('D').ffill()

    # Save to raw directory
    out_path = CONFIG.raw_dir / "fred" / "fred_extended.parquet"
    write_parquet(df, out_path)

    log.info(f"Extended FRED data updated. Shape: {df.shape}")
    log.info(f"Columns: {list(df.columns)}")

    return df


def get_tga_history() -> pd.DataFrame:
    """Convenience function to get TGA balance history."""
    api_key = CONFIG.fred_api_key
    if not api_key:
        return pd.DataFrame()

    series = fetch_fred_series("WTREGEN", api_key, "2015-01-01")
    if series is None:
        return pd.DataFrame()

    df = series.to_frame(name="TGA_Balance")
    df['TGA_Billions'] = df['TGA_Balance'] / 1e6  # Convert millions to billions
    return df


def get_fed_balance_sheet() -> pd.DataFrame:
    """Convenience function to get Fed balance sheet components."""
    api_key = CONFIG.fred_api_key
    if not api_key:
        return pd.DataFrame()

    components = {
        "WALCL": "Total_Assets",
        "WRESBAL": "Reserves",
        "RRPONTSYD": "RRP",
        "WTREGEN": "TGA"
    }

    frames = {}
    for fred_id, name in components.items():
        series = fetch_fred_series(fred_id, api_key, "2008-01-01")
        if series is not None:
            frames[name] = series

    if not frames:
        return pd.DataFrame()

    df = pd.DataFrame(frames)
    df = df.resample('D').ffill()

    # Calculate "Other Liabilities" = Total - Reserves - RRP - TGA
    if all(col in df.columns for col in ['Total_Assets', 'Reserves', 'RRP', 'TGA']):
        df['Other_Liabilities'] = df['Total_Assets'] - df['Reserves'] - df['RRP'] - df['TGA']

    return df


def get_real_rates() -> pd.DataFrame:
    """Convenience function to get real rates and breakevens."""
    api_key = CONFIG.fred_api_key
    if not api_key:
        return pd.DataFrame()

    series_map = {
        "DFII10": "Real_10Y",
        "DFII5": "Real_5Y",
        "T10YIE": "Breakeven_10Y",
        "T5YIE": "Breakeven_5Y",
        "T5YIFR": "Forward_5Y5Y",
        "DGS10": "Nominal_10Y"
    }

    frames = {}
    for fred_id, name in series_map.items():
        series = fetch_fred_series(fred_id, api_key, "2010-01-01")
        if series is not None:
            frames[name] = series

    if not frames:
        return pd.DataFrame()

    return pd.DataFrame(frames).resample('D').ffill()


def get_sloos_data() -> pd.DataFrame:
    """Convenience function to get SLOOS lending standards data."""
    api_key = CONFIG.fred_api_key
    if not api_key:
        return pd.DataFrame()

    series_map = {
        "DRTSCILM": "CandI_Large_Tightening",
        "DRTSCLCC": "Consumer_CC_Tightening",
        "DRTSCIS": "CandI_Small_Tightening",
    }

    frames = {}
    for fred_id, name in series_map.items():
        series = fetch_fred_series(fred_id, api_key, "1990-01-01")
        if series is not None:
            frames[name] = series

    if not frames:
        return pd.DataFrame()

    return pd.DataFrame(frames).resample('D').ffill()


def get_mmf_flows() -> pd.DataFrame:
    """Convenience function to get Money Market Fund data."""
    api_key = CONFIG.fred_api_key
    if not api_key:
        return pd.DataFrame()

    series_map = {
        "WRMFSL": "Retail_MMF",
        "WIMFSL": "Inst_MMF",
    }

    frames = {}
    for fred_id, name in series_map.items():
        series = fetch_fred_series(fred_id, api_key, "2010-01-01")
        if series is not None:
            frames[name] = series

    if not frames:
        return pd.DataFrame()

    df = pd.DataFrame(frames).resample('D').ffill()

    # Calculate total and flows
    if 'Retail_MMF' in df.columns and 'Inst_MMF' in df.columns:
        df['Total_MMF'] = df['Retail_MMF'] + df['Inst_MMF']
        df['MMF_Weekly_Flow'] = df['Total_MMF'].diff(7)
        df['MMF_4W_Flow'] = df['Total_MMF'].diff(28)

    return df


if __name__ == "__main__":
    # Test the extended collector
    df = update_fred_extended()
    print(f"\nFetched {len(df.columns)} series")
    print(df.tail())
