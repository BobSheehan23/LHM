"""
LIGHTHOUSE MACRO - Comprehensive Economic Deep Dive
Multi-source extraction: BLS + BEA + FRED

Data Range: 1919-present
Total Series: 100+
Sources: BLS (Labor/Prices), BEA (GDP/Income), FRED (Financial/Historical)
"""

import requests
import pandas as pd
import time
from datetime import datetime

# ==========================================
# API KEYS
# ==========================================
KEYS = {
    "BLS": "2e66aeb26c664d4fbc862de06d1f8899",
    "BEA": "4401D40D-4047-414F-B4FE-D441E96F8DE8",
    "FRED": "11893c506c07b3b8647bf16cf60586e8"
}

# ==========================================
# SERIES DEFINITIONS
# ==========================================

# A. BLS: Labor & Prices (Granular by Supersector)
BLS_SERIES = {
    # Employment by Sector
    "CES0000000001": "Jobs_Total_Nonfarm",
    "CES1000000001": "Jobs_Mining_Logging",
    "CES2000000001": "Jobs_Construction",
    "CES3000000001": "Jobs_Manufacturing",
    "CES4000000001": "Jobs_Trade_Transport_Utilities",
    "CES5000000001": "Jobs_Information",
    "CES5500000001": "Jobs_Financial_Activities",
    "CES6000000001": "Jobs_Professional_Business",
    "CES6500000001": "Jobs_Education_Health",
    "CES7000000001": "Jobs_Leisure_Hospitality",
    "CES8000000001": "Jobs_Other_Services",
    "CES9000000001": "Jobs_Government",

    # Unemployment
    "LNS14000000": "Unemployment_Rate_U3",
    "LNS13327709": "Unemployment_Rate_U6_Broad",
    "LNS11300000": "Labor_Force_Participation",
    "LNS12300000": "Employment_Population_Ratio",

    # JOLTS
    "JTS000000000000000QUR": "JOLTS_Quits_Rate",
    "JTS000000000000000HIR": "JOLTS_Hires_Rate",
    "JTS000000000000000JOR": "JOLTS_Openings_Rate",

    # Prices
    "CUUR0000SA0": "CPI_Headline",
    "CUUR0000SA0L1E": "CPI_Core_Less_Food_Energy",
    "CUUR0000SA0E": "CPI_Energy",
    "CUUR0000SAH1": "CPI_Shelter",
    "CUUR0000SAS": "CPI_Services",
    "WPSFD4": "PPI_Final_Demand",

    # Wages
    "CES0500000003": "Avg_Hourly_Earnings_Private",
}

# B. BEA: GDP & Income (Full Granular Tables)
BEA_TABLES = [
    {"table": "T10105", "desc": "GDP_Components"},      # GDP breakdown
    {"table": "T10101", "desc": "GDP_Growth"},          # Real GDP % change
    {"table": "T20305", "desc": "PCE_Components"},      # Consumer spending
    {"table": "T20100", "desc": "Personal_Income"},     # Income, DPI, Savings
    {"table": "T11200", "desc": "Corporate_Profits"},   # Profits before/after tax
    {"table": "T11000", "desc": "GDI"},                 # Gross Domestic Income
    {"table": "T30100", "desc": "Govt_Receipts_Exp"},   # Government
    {"table": "T20304", "desc": "PCE_Prices"},          # PCE Price Index
    {"table": "T10104", "desc": "GDP_Prices"},          # GDP Price Index
]

# C. FRED: Financials & Long History
FRED_SERIES = {
    # Rates
    "GS10": "Rate_10Y_Treasury",
    "GS2": "Rate_2Y_Treasury",
    "GS1": "Rate_1Y_Treasury",
    "T10Y2Y": "Yield_Curve_10Y_2Y",
    "T10Y3M": "Yield_Curve_10Y_3M",
    "FEDFUNDS": "Fed_Funds_Rate",
    "DFEDTARU": "Fed_Funds_Upper",
    "DFEDTARL": "Fed_Funds_Lower",

    # Money & Credit
    "M2SL": "Money_Supply_M2",
    "TOTRESNS": "Bank_Reserves",
    "RRPONTSYD": "RRP_Usage",
    "WALCL": "Fed_Balance_Sheet",

    # Economic Activity
    "INDPRO": "Industrial_Production",
    "UNRATE": "Unemployment_Rate",
    "PAYEMS": "Nonfarm_Payrolls",
    "ICSA": "Initial_Claims",

    # Prices
    "PCEPI": "PCE_Price_Index",
    "PCEPILFE": "Core_PCE",
    "CPIAUCSL": "CPI_Index",

    # Credit Spreads
    "BAMLH0A0HYM2": "HY_OAS_Spread",
    "BAMLC0A0CM": "IG_OAS_Spread",

    # Consumer
    "PSAVERT": "Personal_Saving_Rate",
    "TOTALSL": "Consumer_Credit",
    "UMCSENT": "Consumer_Sentiment",

    # Housing
    "MORTGAGE30US": "Mortgage_30Y",
    "HOUST": "Housing_Starts",

    # Fiscal
    "GFDEBTN": "Federal_Debt",
    "GFDEGDQ188S": "Debt_to_GDP",

    # Volatility
    "VIXCLS": "VIX",
}


# ==========================================
# EXTRACTION FUNCTIONS
# ==========================================

def get_bls_data(series_map=None, start_year=1945):
    """
    Fetch BLS data with 20-year chunking.
    Returns long DataFrame with Date, Series, Value, Source columns.
    """
    if series_map is None:
        series_map = BLS_SERIES

    print(f"--- Fetching BLS Data ({len(series_map)} series) ---")

    intervals = [(start, min(start + 19, 2026)) for start in range(start_year, 2027, 20)]
    all_records = []
    series_ids = list(series_map.keys())

    for start_yr, end_yr in intervals:
        print(f"   {start_yr}-{end_yr}...")
        payload = {
            "seriesid": series_ids,
            "startyear": str(start_yr),
            "endyear": str(end_yr),
            "registrationkey": KEYS["BLS"]
        }
        try:
            r = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/',
                            json=payload, timeout=60)
            if r.status_code == 200:
                data = r.json()
                if data.get('status') == 'REQUEST_SUCCEEDED':
                    for s in data['Results']['series']:
                        col_name = series_map.get(s['seriesID'], s['seriesID'])
                        for item in s['data']:
                            all_records.append({
                                'Date': f"{item['year']}-{item['period'][1:]}-01",
                                'Series': col_name,
                                'Value': item['value'],
                                'Source': 'BLS'
                            })
            time.sleep(0.3)
        except Exception as e:
            print(f"   Error: {e}")

    df = pd.DataFrame(all_records)
    print(f"   -> {len(df):,} records")
    return df


def get_bea_data(table_list=None):
    """
    Fetch BEA NIPA tables with full granularity.
    Returns long DataFrame with Date, Series, Value, Source columns.
    """
    if table_list is None:
        table_list = BEA_TABLES

    print(f"\n--- Fetching BEA Data ({len(table_list)} tables) ---")
    all_records = []

    for item in table_list:
        print(f"   {item['desc']} ({item['table']})...")
        params = {
            "UserID": KEYS["BEA"],
            "Method": "GetData",
            "DatasetName": "NIPA",
            "TableName": item['table'],
            "Frequency": "Q",
            "Year": "ALL",
            "ResultFormat": "JSON"
        }
        try:
            r = requests.get("https://apps.bea.gov/api/data/", params=params, timeout=60)
            if r.status_code == 200:
                data = r.json()
                if "BEAAPI" in data and "Results" in data["BEAAPI"]:
                    rows = data["BEAAPI"]["Results"]["Data"]
                    for row in rows:
                        q_map = {'Q1': '01', 'Q2': '04', 'Q3': '07', 'Q4': '10'}
                        tp = row['TimePeriod']
                        if 'Q' in tp:
                            month = q_map.get(tp[-2:], '01')
                            date_str = f"{tp[:4]}-{month}-01"
                        else:
                            date_str = f"{tp}-01-01"

                        all_records.append({
                            'Date': date_str,
                            'Series': f"BEA_{item['desc']}_{row['LineDescription']}",
                            'Value': row['DataValue'],
                            'Source': 'BEA'
                        })
                    print(f"      -> {len(rows):,} rows")
            time.sleep(0.5)
        except Exception as e:
            print(f"   Error: {e}")

    return pd.DataFrame(all_records)


def get_fred_data(series_map=None, start_date="1900-01-01"):
    """
    Fetch FRED series with full history.
    Returns long DataFrame with Date, Series, Value, Source columns.
    """
    if series_map is None:
        series_map = FRED_SERIES

    print(f"\n--- Fetching FRED Data ({len(series_map)} series) ---")
    all_records = []

    for sid, name in series_map.items():
        print(f"   {name} ({sid})...")
        params = {
            "series_id": sid,
            "api_key": KEYS["FRED"],
            "file_type": "json",
            "observation_start": start_date
        }
        try:
            r = requests.get("https://api.stlouisfed.org/fred/series/observations",
                           params=params, timeout=30)
            if r.status_code == 200:
                data = r.json()
                obs_count = 0
                for obs in data['observations']:
                    if obs['value'] != '.':
                        all_records.append({
                            'Date': obs['date'],
                            'Series': name,
                            'Value': obs['value'],
                            'Source': 'FRED'
                        })
                        obs_count += 1
                print(f"      -> {obs_count:,} obs")
        except Exception as e:
            print(f"   Error: {e}")

    return pd.DataFrame(all_records)


def get_full_deep_dive():
    """
    Fetch ALL data from BLS + BEA + FRED.
    Returns cleaned, merged DataFrame.
    """
    print("=" * 60)
    print("LIGHTHOUSE MACRO - FULL ECONOMIC DEEP DIVE")
    print("=" * 60)

    # Fetch all sources
    df_bls = get_bls_data()
    df_bea = get_bea_data()
    df_fred = get_fred_data()

    # Combine
    print("\n--- Processing & Merging ---")
    master_df = pd.concat([df_bls, df_bea, df_fred], ignore_index=True)

    # Clean
    master_df['Date'] = pd.to_datetime(master_df['Date'], errors='coerce')
    master_df['Value'] = pd.to_numeric(
        master_df['Value'].astype(str).str.replace(',', ''),
        errors='coerce'
    )
    master_df = master_df.dropna(subset=['Value', 'Date'])
    master_df = master_df.sort_values('Date')

    # Summary
    print(f"\n{'=' * 60}")
    print("EXTRACTION COMPLETE")
    print(f"{'=' * 60}")
    print(f"Total Data Points: {len(master_df):,}")
    print(f"Date Range: {master_df['Date'].min().date()} to {master_df['Date'].max().date()}")
    print(f"Unique Series: {master_df['Series'].nunique()}")
    print(f"\nBy Source:")
    print(master_df.groupby('Source').size().to_string())
    print(f"{'=' * 60}")

    return master_df


def pivot_wide(df):
    """Convert long format to wide format (Dates x Series)."""
    return df.pivot_table(index='Date', columns='Series', values='Value')


# ==========================================
# MAIN
# ==========================================

if __name__ == '__main__':
    # Run full extraction
    master_df = get_full_deep_dive()

    # Show sample
    print("\nSample (recent data):")
    sample_series = ['CPI_Headline', 'Rate_10Y_Treasury', 'Jobs_Total_Nonfarm', 'Unemployment_Rate_U3']
    sample = master_df[master_df['Series'].isin(sample_series)]
    print(sample.sort_values('Date').tail(20).to_string())

    # Optional: Save
    # master_df.to_csv("US_Economic_Deep_Dive.csv", index=False)
    # pivot_wide(master_df).to_csv("US_Economic_Deep_Dive_Wide.csv")
