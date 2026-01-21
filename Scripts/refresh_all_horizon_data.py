"""
HORIZON 2026 - FULL DATA REFRESH
Lighthouse Macro | January 2026

Updates the SQLite database with fresh FRED data through January 7, 2026
and regenerates all charts.

Usage:
    python refresh_all_horizon_data.py
"""

import os
import sqlite3
import pandas as pd
import requests
from datetime import datetime
from pathlib import Path

# Database path
DB_PATH = Path('/Users/bob/LHM/projects/lighthouse-macro/charts/output/horizon_data.db')

# FRED API key
FRED_API_KEY = os.environ.get('FRED_API_KEY')
if not FRED_API_KEY:
    raise ValueError("FRED_API_KEY environment variable required")


# All series to update (from the database tables)
FRED_SERIES = {
    # Fed Balance Sheet
    'fed_balance_sheet': 'WALCL',
    'treasury_holdings': 'TREAST',
    'mbs_holdings': 'WSHOMCB',
    'tga_balance': 'WTREGEN',
    'reserves': 'WRESBAL',
    'rrp_balance': 'RRPONTSYD',

    # Rates
    'fed_funds': 'FEDFUNDS',
    'prime_rate': 'DPRIME',
    'sofr': 'SOFR',
    'effr': 'EFFR',

    # Treasuries
    'treasury_1m': 'DGS1MO',
    'treasury_3m': 'DGS3MO',
    'treasury_6m': 'DGS6MO',
    'treasury_1y': 'DGS1',
    'treasury_2y': 'DGS2',
    'treasury_3y': 'DGS3',
    'treasury_5y': 'DGS5',
    'treasury_7y': 'DGS7',
    'treasury_10y': 'DGS10',
    'treasury_20y': 'DGS20',
    'treasury_30y': 'DGS30',

    # Spreads
    'spread_10y2y': 'T10Y2Y',
    'spread_10y3m': 'T10Y3M',
    'hy_spread': 'BAMLH0A0HYM2',
    'ig_spread': 'BAMLC0A0CM',
    'bbb_spread': 'BAMLC0A4CBBB',
    'aaa_spread': 'BAMLC0A1CAAA',

    # Inflation
    'cpi_all': 'CPIAUCSL',
    'cpi_core': 'CPILFESL',
    'pce': 'PCEPI',
    'pce_core': 'PCEPILFE',
    'breakeven_5y': 'T5YIE',
    'breakeven_10y': 'T10YIE',

    # Labor
    'unemployment_rate': 'UNRATE',
    'unemployment_u6': 'U6RATE',
    'participation_rate': 'CIVPART',
    'employment_pop_ratio': 'EMRATIO',
    'nonfarm_payrolls': 'PAYEMS',
    'private_payrolls': 'USPRIV',
    'initial_claims': 'ICSA',
    'continued_claims': 'CCSA',
    'job_openings': 'JTSJOL',
    'quits_rate': 'JTSQUR',
    'hires_rate': 'JTSHIR',
    'layoffs_rate': 'JTSLDL',
    'avg_hourly_earnings': 'CES0500000003',
    'avg_weekly_hours': 'AWHAETP',

    # GDP/Growth
    'gdp': 'GDP',
    'gdp_real': 'GDPC1',
    'gdp_growth': 'A191RL1Q225SBEA',
    'gdi': 'GDI',
    'personal_income': 'PI',
    'personal_spending': 'PCE',
    'savings_rate': 'PSAVERT',

    # Industry
    'industrial_production': 'INDPRO',
    'capacity_utilization': 'TCU',
    'durable_goods': 'DGORDER',
    'business_inventories': 'BUSINV',
    'new_orders': 'NEWORDER',

    # Consumer
    'retail_sales': 'RSXFS',
    'retail_sales_total': 'MRTSSM44X72USS',
    'consumer_sentiment': 'UMCSENT',
    'vehicle_sales': 'TOTALSA',

    # Housing
    'housing_starts': 'HOUST',
    'building_permits': 'PERMIT',
    'new_home_sales': 'HSN1F',
    'existing_home_sales': 'EXHOSLUSM495S',
    'case_shiller_national': 'CSUSHPINSA',
    'median_home_price': 'MSPUS',
    'mortgage_rate_30y': 'MORTGAGE30US',
    'mortgage_rate_15y': 'MORTGAGE15US',

    # Fiscal
    'debt_to_gdp': 'GFDEGDQ188S',
    'federal_debt': 'GFDEBTN',
    'federal_surplus': 'MTSDS133FMS',
    'federal_receipts': 'FGRECPT',
    'interest_payments': 'A091RC1Q027SBEA',

    # Credit/Delinquency
    'cc_delinquency': 'DRCCLACBS',
    'cre_delinquency': 'DRSFRMACBS',
    'mortgage_delinquency': 'DRSFRMACBS',
    'business_loans_delinq': 'DRBLACBS',
    'consumer_credit': 'TOTALSL',

    # Money Supply
    'm1': 'M1SL',
    'm2': 'M2SL',
    'velocity_m2': 'M2V',

    # Commodities
    'oil_wti': 'DCOILWTICO',
    'gas_price': 'GASREGW',

    # Financial Conditions
    'chicago_fed_nfci': 'NFCI',
    'chicago_fed_anfci': 'ANFCI',
    'st_louis_fsi': 'STLFSI4',

    # Trade
    'trade_balance': 'BOPGSTB',
    'dollar_index': 'DTWEXBGS',
    'euro_usd': 'DEXUSEU',
    'yen_usd': 'DEXJPUS',

    # Bank Credit
    'bank_credit': 'TOTBKCR',
    'commercial_loans': 'BUSLOANS',
    'real_estate_loans': 'RELACBW027SBOG',
    'consumer_loans': 'CONSUMER',
}


def fetch_fred_series(series_id: str, start_date: str = '2000-01-01') -> pd.DataFrame:
    """Fetch a single FRED series."""
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': series_id,
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'observation_start': start_date,
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    if 'observations' not in data:
        return pd.DataFrame()

    df = pd.DataFrame(data['observations'])
    df = df[df['value'] != '.']
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = pd.to_numeric(df['value'])

    return df[['date', 'value']]


def update_table(conn: sqlite3.Connection, table_name: str, df: pd.DataFrame):
    """Update a database table with new data."""
    if df.empty:
        return

    # Get existing max date
    try:
        existing = pd.read_sql_query(f"SELECT MAX(date) as max_date FROM {table_name}", conn)
        max_date = existing['max_date'].iloc[0]
        if max_date:
            max_date = pd.to_datetime(max_date)
            # Only insert new data
            df = df[df['date'] > max_date]
    except:
        pass

    if df.empty:
        return

    # Insert new rows
    df.to_sql(table_name, conn, if_exists='append', index=False)


def refresh_all_data():
    """Refresh all FRED data in the database."""
    print("=" * 60)
    print("LIGHTHOUSE MACRO - DATA REFRESH")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Database: {DB_PATH}")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)

    success_count = 0
    error_count = 0

    for table_name, series_id in FRED_SERIES.items():
        try:
            print(f"  Fetching {series_id:20} -> {table_name}...", end=' ')
            df = fetch_fred_series(series_id)

            if df.empty:
                print("NO DATA")
                continue

            # Update the table
            update_table(conn, table_name, df)

            last_date = df['date'].max().strftime('%Y-%m-%d')
            print(f"OK (through {last_date})")
            success_count += 1

        except Exception as e:
            print(f"ERROR: {e}")
            error_count += 1

    conn.commit()
    conn.close()

    print("\n" + "=" * 60)
    print(f"REFRESH COMPLETE: {success_count} success, {error_count} errors")
    print("=" * 60)


def verify_data_freshness():
    """Check data freshness after refresh."""
    print("\n" + "=" * 60)
    print("DATA FRESHNESS CHECK")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)

    key_tables = [
        'rrp_balance', 'reserves', 'tga_balance', 'fed_balance_sheet',
        'sofr', 'effr', 'treasury_10y', 'treasury_2y',
        'hy_spread', 'quits_rate', 'unemployment_rate', 'initial_claims',
        'cc_delinquency', 'savings_rate'
    ]

    for table in key_tables:
        try:
            df = pd.read_sql_query(
                f"SELECT date, value FROM {table} ORDER BY date DESC LIMIT 1",
                conn
            )
            if not df.empty:
                date = df['date'].iloc[0]
                value = df['value'].iloc[0]
                print(f"  {table:25} Last: {date[:10]}  Value: {value:.2f}")
        except Exception as e:
            print(f"  {table:25} ERROR: {e}")

    conn.close()


if __name__ == "__main__":
    refresh_all_data()
    verify_data_freshness()
