"""
LIGHTHOUSE MACRO - FRED Mega Database
100+ Series with SQLite Storage and Incremental Updates

This is the "manual list" approach - you define exactly what you want.
For automatic category crawling, see fred_quant_database.py
"""

import requests
import pandas as pd
import sqlite3
import time
from datetime import datetime

# ==========================================
# 1. CONFIGURATION
# ==========================================
FRED_API_KEY = "11893c506c07b3b8647bf16cf60586e8"
DB_NAME = "/Users/bob/Desktop/HorizonJan2026_LiveData/US_Economy_Mega.db"

# ==========================================
# 2. THE 100+ SERIES MASTER LIST
# ==========================================
# Format: "Series_ID": ("Category", "Description")

SERIES_MAP = {
    # --- LABOR MARKET: HEADLINE & UNDERUTILIZATION ---
    "UNRATE": ("Labor", "Unemployment Rate (U-3)"),
    "U6RATE": ("Labor", "Unemployment Rate (U-6 Broad)"),
    "CIVPART": ("Labor", "Labor Force Participation Rate"),
    "CLF16OV": ("Labor", "Civilian Labor Force Level"),
    "CE16OV": ("Labor", "Employment Level"),
    "ICSA": ("Labor", "Initial Jobless Claims"),
    "CCSA": ("Labor", "Continued Jobless Claims"),
    "LNS11300060": ("Labor", "Prime Age (25-54) Participation"),

    # --- LABOR MARKET: JOBS BY SECTOR (CES) ---
    "PAYEMS": ("Labor", "Total Nonfarm Payrolls"),
    "MANEMP": ("Labor", "Jobs: Manufacturing"),
    "SRVPRD": ("Labor", "Jobs: Service-Providing"),
    "USCONS": ("Labor", "Jobs: Construction"),
    "USTPU": ("Labor", "Jobs: Trade, Transport, Utilities"),
    "USINFO": ("Labor", "Jobs: Information"),
    "USFIRE": ("Labor", "Jobs: Financial Activities"),
    "USPBS": ("Labor", "Jobs: Professional & Business"),
    "USEHS": ("Labor", "Jobs: Education & Health"),
    "USLAH": ("Labor", "Jobs: Leisure & Hospitality"),
    "USGOVT": ("Labor", "Jobs: Government"),

    # --- WAGES & PRODUCTIVITY ---
    "AHETPI": ("Wages", "Avg Hourly Earnings: All Employees"),
    "AHEMAN": ("Wages", "Avg Hourly Earnings: Manufacturing"),
    "ECIALLCIV": ("Wages", "Employment Cost Index (Total)"),
    "OPHNFB": ("Productivity", "Nonfarm Business Output Per Hour"),
    "ULCNFB": ("Productivity", "Unit Labor Costs"),

    # --- INFLATION & PRICES ---
    "CPIAUCSL": ("Inflation", "CPI-U Headline"),
    "CPILFESL": ("Inflation", "CPI Core (Less Food/Energy)"),
    "PCEPI": ("Inflation", "PCE Price Index (Fed Target)"),
    "PCEPILFE": ("Inflation", "Core PCE Price Index"),
    "PPIACO": ("Inflation", "PPI All Commodities"),
    "CPIFABSL": ("Inflation", "CPI Food & Beverages"),
    "CPIENGSL": ("Inflation", "CPI Energy"),
    "CPIMEDSL": ("Inflation", "CPI Medical Care"),
    "CUSR0000SEHA": ("Inflation", "CPI Rent of Primary Residence"),
    "MICH": ("Inflation", "UMich Inflation Expectations"),

    # --- GDP & NATIONAL ACCOUNTS ---
    "GDP": ("Growth", "Nominal GDP"),
    "GDPC1": ("Growth", "Real GDP"),
    "GDPDEF": ("Growth", "GDP Deflator"),
    "A191RL1Q225SBEA": ("Growth", "Real GDP % Change"),
    "PCE": ("Growth", "Personal Consumption Expenditures"),
    "GPDI": ("Growth", "Gross Private Domestic Investment"),
    "GCE": ("Growth", "Govt Consumption & Investment"),
    "NETEXP": ("Growth", "Net Exports"),
    "CP": ("Growth", "Corporate Profits (After Tax)"),

    # --- INDUSTRIAL PRODUCTION & CAPACITY ---
    "INDPRO": ("Production", "Industrial Production Index"),
    "TCU": ("Production", "Total Capacity Utilization"),
    "IPMAN": ("Production", "Ind Prod: Manufacturing"),
    "IPMINE": ("Production", "Ind Prod: Mining"),
    "IPUTIL": ("Production", "Ind Prod: Utilities"),
    "HTRUCKSSAAR": ("Production", "Heavy Truck Sales"),
    "ALTSALES": ("Production", "Light Vehicle Sales"),

    # --- HOUSING & REAL ESTATE ---
    "HOUST": ("Housing", "Housing Starts: Total"),
    "HOUST1F": ("Housing", "Housing Starts: 1-Unit"),
    "HOUST5F": ("Housing", "Housing Starts: 5+ Units"),
    "PERMIT": ("Housing", "Building Permits"),
    "CSUSHPINSA": ("Housing", "Case-Shiller Home Price Index"),
    "MSPUS": ("Housing", "Median Sales Price of Houses Sold"),
    "HSN1F": ("Housing", "New One-Family Houses Sold"),
    "ETOTALUSQ176N": ("Housing", "Housing Vacancy Rate"),

    # --- CONSUMER & RETAIL ---
    "RSAFS": ("Consumer", "Advance Retail Sales"),
    "RRSFS": ("Consumer", "Real Retail Sales"),
    "PSAVERT": ("Consumer", "Personal Saving Rate"),
    "UMCSENT": ("Consumer", "UMich Consumer Sentiment"),
    "TOTALSL": ("Consumer", "Total Consumer Credit"),

    # --- INTEREST RATES ---
    "FEDFUNDS": ("Rates", "Effective Fed Funds Rate"),
    "DTB3": ("Rates", "3-Month Treasury Bill"),
    "DGS1": ("Rates", "1-Year Treasury Yield"),
    "DGS2": ("Rates", "2-Year Treasury Yield"),
    "DGS5": ("Rates", "5-Year Treasury Yield"),
    "DGS10": ("Rates", "10-Year Treasury Yield"),
    "DGS30": ("Rates", "30-Year Treasury Yield"),
    "T10Y2Y": ("Rates", "10Y-2Y Yield Spread"),
    "T10Y3M": ("Rates", "10Y-3M Yield Spread"),
    "MORTGAGE30US": ("Rates", "30-Year Fixed Mortgage Rate"),
    "DPRIME": ("Rates", "Bank Prime Loan Rate"),
    "BAA": ("Rates", "Moody's Baa Corporate Bond Yield"),
    "AAA": ("Rates", "Moody's Aaa Corporate Bond Yield"),
    "BAMLC0A0CM": ("Rates", "US Corporate Option-Adjusted Spread"),
    "BAMLH0A0HYM2": ("Rates", "US High Yield OAS"),

    # --- MONEY, BANKING & LIQUIDITY ---
    "M1SL": ("Money", "M1 Money Stock"),
    "M2SL": ("Money", "M2 Money Stock"),
    "M2V": ("Money", "Velocity of M2 Money Stock"),
    "BOGMBASE": ("Money", "Monetary Base"),
    "TOTRESNS": ("Money", "Total Reserves of Depository Inst."),
    "BUSLOANS": ("Money", "Commercial and Industrial Loans"),
    "REALLN": ("Money", "Real Estate Loans"),
    "RRPONTSYD": ("Money", "ON RRP Usage"),
    "WALCL": ("Money", "Fed Balance Sheet"),

    # --- DEBT & WEALTH ---
    "TNWBSHNO": ("Wealth", "Households Net Worth"),
    "GFDEBTN": ("Debt", "Federal Debt: Total Public Debt"),
    "GFDEGDQ188S": ("Debt", "Federal Debt to GDP Ratio"),
    "TDSP": ("Debt", "Household Debt Service Ratio"),

    # --- COMMODITIES & EXCHANGE ---
    "DCOILWTICO": ("Commodities", "Crude Oil Price (WTI)"),
    "GASREGW": ("Commodities", "Regular Gas Price"),
    "DTWEXBGS": ("Exchange", "Trade Weighted US Dollar Index"),
    "DEXUSEU": ("Exchange", "US / Euro Exchange Rate"),
    "DEXJPUS": ("Exchange", "Japan / US Exchange Rate"),
    "DEXCHUS": ("Exchange", "China / US Exchange Rate"),

    # --- MARKET VOLATILITY ---
    "VIXCLS": ("Volatility", "CBOE VIX"),

    # --- DELINQUENCIES ---
    "DRCLACBS": ("Delinquencies", "CRE Delinquency Rate"),
    "DRALACBS": ("Delinquencies", "Auto Loan Delinquency Rate"),
    "DRSFRMACBS": ("Delinquencies", "Mortgage Delinquency Rate"),
}


# ==========================================
# 3. DATABASE SETUP
# ==========================================

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS econ_history
                 (date TEXT, category TEXT, series_id TEXT,
                  description TEXT, value REAL,
                  UNIQUE(date, series_id) ON CONFLICT REPLACE)''')
    c.execute('''CREATE INDEX IF NOT EXISTS idx_series ON econ_history(series_id)''')
    c.execute('''CREATE INDEX IF NOT EXISTS idx_date ON econ_history(date)''')
    conn.commit()
    return conn


def get_last_date(conn, series_id):
    c = conn.cursor()
    c.execute("SELECT MAX(date) FROM econ_history WHERE series_id = ?", (series_id,))
    res = c.fetchone()[0]
    return res if res else "1900-01-01"


# ==========================================
# 4. DATA FETCHING LOGIC
# ==========================================

def fetch_and_store(conn, full_refresh=False):
    """
    Fetch all series and store in database.
    full_refresh=True forces re-download of all history.
    """
    print(f"--- Starting Mega-Monitor Update ({len(SERIES_MAP)} series) ---")
    print(f"Database: {DB_NAME}")
    print()

    total_added = 0

    for sid, (category, desc) in SERIES_MAP.items():
        if full_refresh:
            start_date = "1900-01-01"
        else:
            last_date = get_last_date(conn, sid)
            start_date = last_date

        print(f"   {desc} ({sid})...", end=" ")

        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
            "series_id": sid,
            "api_key": FRED_API_KEY,
            "file_type": "json",
            "observation_start": start_date
        }

        try:
            r = requests.get(url, params=params, timeout=30)
            data = r.json()

            if "observations" in data:
                rows = []
                for obs in data["observations"]:
                    val = obs['value']
                    if val != ".":
                        rows.append((obs['date'], category, sid, desc, float(val)))

                if rows:
                    conn.executemany("INSERT INTO econ_history VALUES (?,?,?,?,?)", rows)
                    conn.commit()
                    print(f"{len(rows)} records")
                    total_added += len(rows)
                else:
                    print("up to date")
            else:
                print(f"API Error: {data.get('error_message', 'Unknown')}")

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(0.2)

    print(f"\n--- Update Complete: {total_added:,} records added ---")
    return total_added


# ==========================================
# 5. EXPORT & REPORTING
# ==========================================

def generate_report(conn):
    """Generate summary statistics and export to CSV."""
    print("\n--- Database Summary ---")

    # Stats by category
    df_stats = pd.read_sql("""
        SELECT category,
               COUNT(DISTINCT series_id) as series_count,
               COUNT(*) as data_points,
               MIN(date) as earliest,
               MAX(date) as latest
        FROM econ_history
        GROUP BY category
        ORDER BY category
    """, conn)
    print(df_stats.to_string(index=False))

    # Total
    total = pd.read_sql("SELECT COUNT(*) as total FROM econ_history", conn)
    print(f"\nTotal Data Points: {total['total'].iloc[0]:,}")

    return df_stats


def export_wide_csv(conn, output_path=None):
    """Export to wide format CSV (Date x Series)."""
    if output_path is None:
        output_path = DB_NAME.replace('.db', '_Wide.csv')

    print(f"\nExporting to: {output_path}")

    df_all = pd.read_sql("""
        SELECT date, description, value
        FROM econ_history
        ORDER BY date
    """, conn)

    df_wide = df_all.pivot_table(index='date', columns='description', values='value')
    df_wide = df_wide.reindex(sorted(df_wide.columns), axis=1)
    df_wide.to_csv(output_path)

    print(f"Exported {len(df_wide)} rows x {len(df_wide.columns)} columns")
    return output_path


def query_series(conn, series_id, start_date=None, end_date=None):
    """Query a specific series from the database."""
    query = "SELECT date, value FROM econ_history WHERE series_id = ?"
    params = [series_id]

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)

    query += " ORDER BY date"
    return pd.read_sql(query, conn, params=params)


# ==========================================
# 6. MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    db_conn = init_db()

    # Run update
    fetch_and_store(db_conn, full_refresh=False)

    # Generate report
    generate_report(db_conn)

    # Export to CSV
    export_wide_csv(db_conn)

    db_conn.close()
