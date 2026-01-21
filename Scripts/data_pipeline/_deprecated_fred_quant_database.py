"""
LIGHTHOUSE MACRO - Quantitative Macro Database
Category Crawling + Smart Updates (Release Calendar Logic)

This is the "automated discovery" approach - finds hundreds of series automatically.
Only downloads what's new based on FRED's last_updated timestamp.
"""

import requests
import pandas as pd
import sqlite3
import time
from datetime import datetime, timedelta

# ==========================================
# 1. CONFIGURATION
# ==========================================
FRED_API_KEY = "11893c506c07b3b8647bf16cf60586e8"
DB_NAME = "/Users/bob/Desktop/HorizonJan2026_LiveData/Macro_Quant_Database.db"

# Category IDs from: https://fred.stlouisfed.org/categories
# Change limit in discover_series_in_category() to control depth
CATEGORY_MAP = {
    "Employment_Situation": 32440,      # ~400+ series (Unemployment, Participation by age/race)
    "CPI_Urban_Consumers": 9,           # ~100+ series (CPI sub-components)
    "Industrial_Production": 32262,     # ~100+ series (Output by sector)
    "Treasury_Rates": 115,              # Yield curve data
    "Money_Banking": 24,                # M1, M2, Reserves
    "Producer_Price_Index": 32263,      # Input costs
    "Employment_Cost_Index": 3,         # Wages & Benefits
    "Exchange_Rates": 94,               # Forex
    "Regional_Fed_Surveys": 32266,      # Empire State, Philly Fed, etc.
    "Housing": 97,                      # Housing starts, permits, sales
    "GDP_National_Accounts": 106,       # GDP components
    "Personal_Income": 110,             # Income & spending
    "Consumer_Credit": 22,              # Consumer debt
    "Interest_Rates": 22,               # Various rates
}


# ==========================================
# 2. DATABASE MANAGEMENT
# ==========================================

def get_db_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    """Initialize database with metadata and observations tables."""
    conn = get_db_connection()
    c = conn.cursor()

    # Metadata Table: Info about each series
    c.execute('''CREATE TABLE IF NOT EXISTS series_meta (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    frequency TEXT,
                    units TEXT,
                    seasonal_adjustment TEXT,
                    category TEXT,
                    last_updated_api TEXT,
                    last_checked_local TEXT
                )''')

    # Data Table: The actual observations
    c.execute('''CREATE TABLE IF NOT EXISTS observations (
                    series_id TEXT,
                    date TEXT,
                    value REAL,
                    PRIMARY KEY (series_id, date),
                    FOREIGN KEY(series_id) REFERENCES series_meta(id)
                )''')

    # Indexes for fast queries
    c.execute('''CREATE INDEX IF NOT EXISTS idx_obs_series ON observations(series_id)''')
    c.execute('''CREATE INDEX IF NOT EXISTS idx_obs_date ON observations(date)''')

    conn.commit()
    conn.close()


# ==========================================
# 3. DISCOVERY ENGINE (Category Crawling)
# ==========================================

def discover_series_in_category(category_id, limit=100):
    """
    Crawl a FRED category to find top series by popularity.
    Increase limit to get more series (e.g., 200, 500).
    """
    url = "https://api.stlouisfed.org/fred/category/series"
    params = {
        "category_id": category_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "limit": limit,
        "order_by": "popularity",
        "sort_order": "desc"
    }

    try:
        r = requests.get(url, params=params, timeout=30)
        data = r.json()
        if "seriess" in data:
            return data["seriess"]
    except Exception as e:
        print(f"   Error crawling category {category_id}: {e}")
    return []


# ==========================================
# 4. SMART UPDATE ENGINE (Release Calendar Logic)
# ==========================================

def update_series_data(series_id, last_api_update, category_name, conn):
    """
    Fetch data ONLY if the API has newer data than our local copy.
    This is the "Release Calendar" logic - skip what hasn't changed.
    """
    c = conn.cursor()

    # Check our local last_updated timestamp
    c.execute("SELECT last_updated_api FROM series_meta WHERE id = ?", (series_id,))
    row = c.fetchone()

    local_last_update = row[0] if row else "1900-01-01"

    # If we already have the latest, skip
    if row and local_last_update >= last_api_update:
        return False, 0

    # Data is new - fetch it
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json"
    }

    try:
        r = requests.get(url, params=params, timeout=30)
        data = r.json()

        if "observations" in data:
            obs_list = []
            for o in data["observations"]:
                if o['value'] != ".":
                    obs_list.append((series_id, o['date'], float(o['value'])))

            if obs_list:
                # Upsert observations (handles revisions)
                c.executemany("INSERT OR REPLACE INTO observations VALUES (?,?,?)", obs_list)

                # Update metadata timestamp
                c.execute("""UPDATE series_meta
                            SET last_updated_api = ?, last_checked_local = ?
                            WHERE id = ?""",
                         (last_api_update, datetime.now().isoformat(), series_id))

                conn.commit()
                return True, len(obs_list)

    except Exception as e:
        print(f"   Failed to update {series_id}: {e}")

    return False, 0


# ==========================================
# 5. MAIN UPDATE ROUTINE
# ==========================================

def run_daily_update(series_per_category=100):
    """
    Main update routine:
    1. Discover series in each category
    2. Check which have been updated on FRED
    3. Download only new/revised data
    """
    init_db()
    conn = get_db_connection()
    c = conn.cursor()

    total_series = 0
    updated_count = 0
    total_obs = 0

    print("=" * 60)
    print("LIGHTHOUSE MACRO - QUANT DATABASE UPDATE")
    print(f"Database: {DB_NAME}")
    print(f"Categories: {len(CATEGORY_MAP)}")
    print(f"Series per category: {series_per_category}")
    print("=" * 60)

    print("\n--- Phase 1: Discovery ---")
    for cat_name, cat_id in CATEGORY_MAP.items():
        print(f"\n{cat_name} (ID: {cat_id})...")

        found_series = discover_series_in_category(cat_id, limit=series_per_category)
        print(f"   Found {len(found_series)} series")

        for s in found_series:
            # Insert/update metadata
            c.execute("""INSERT OR REPLACE INTO series_meta
                        (id, title, frequency, units, seasonal_adjustment, category, last_updated_api)
                        VALUES (?, ?, ?, ?, ?, ?, COALESCE(
                            (SELECT last_updated_api FROM series_meta WHERE id = ?), '1900-01-01'))""",
                     (s['id'], s['title'], s.get('frequency', ''),
                      s.get('units', ''), s.get('seasonal_adjustment', ''),
                      cat_name, s['id']))

            # Check if update needed
            did_update, obs_count = update_series_data(
                s['id'], s['last_updated'], cat_name, conn
            )

            if did_update:
                updated_count += 1
                total_obs += obs_count
                print(f"   [UPDATED] {s['id']}: {s['title'][:50]}... ({obs_count} obs)")

            total_series += 1

        conn.commit()
        time.sleep(0.5)

    print("\n" + "=" * 60)
    print("UPDATE COMPLETE")
    print("=" * 60)
    print(f"Total Series Tracked: {total_series}")
    print(f"Series Updated: {updated_count}")
    print(f"Observations Added: {total_obs:,}")

    conn.close()
    return total_series, updated_count, total_obs


# ==========================================
# 6. QUERY & ANALYTICS
# ==========================================

def get_database_stats():
    """Show database health and coverage."""
    conn = get_db_connection()

    print("\n--- Database Statistics ---")

    # Total observations
    total = conn.execute("SELECT COUNT(*) FROM observations").fetchone()[0]
    print(f"Total Observations: {total:,}")

    # Series count
    series_count = conn.execute("SELECT COUNT(*) FROM series_meta").fetchone()[0]
    print(f"Total Series: {series_count}")

    # By category
    print("\nBy Category:")
    df = pd.read_sql("""
        SELECT category,
               COUNT(DISTINCT id) as series,
               (SELECT COUNT(*) FROM observations o WHERE o.series_id IN
                (SELECT id FROM series_meta sm WHERE sm.category = series_meta.category)) as obs
        FROM series_meta
        GROUP BY category
        ORDER BY series DESC
    """, conn)
    print(df.to_string(index=False))

    # Date range
    dates = conn.execute("""
        SELECT MIN(date) as earliest, MAX(date) as latest
        FROM observations
    """).fetchone()
    print(f"\nDate Range: {dates[0]} to {dates[1]}")

    conn.close()


def query_series(series_id):
    """Retrieve a specific series."""
    conn = get_db_connection()
    df = pd.read_sql("""
        SELECT o.date, o.value, m.title
        FROM observations o
        JOIN series_meta m ON o.series_id = m.id
        WHERE o.series_id = ?
        ORDER BY o.date
    """, conn, params=[series_id])
    conn.close()
    return df


def export_to_csv(output_path=None):
    """Export all data to wide-format CSV."""
    if output_path is None:
        output_path = DB_NAME.replace('.db', '_Wide.csv')

    conn = get_db_connection()

    print(f"\nExporting to: {output_path}")

    df = pd.read_sql("""
        SELECT o.date, m.title, o.value
        FROM observations o
        JOIN series_meta m ON o.series_id = m.id
        ORDER BY o.date
    """, conn)

    df_wide = df.pivot_table(index='date', columns='title', values='value')
    df_wide.to_csv(output_path)

    print(f"Exported {len(df_wide)} rows x {len(df_wide.columns)} columns")

    conn.close()
    return output_path


# ==========================================
# 7. MAIN
# ==========================================

if __name__ == "__main__":
    # Run update (change series_per_category for more depth)
    # 50 = ~700 series, 100 = ~1400 series, 200 = ~2800 series
    run_daily_update(series_per_category=50)

    # Show stats
    get_database_stats()
