#!/usr/bin/env python3
"""
LIGHTHOUSE MACRO - CRYPTO INDEX COMPUTATION
============================================
Computes crypto-specific indices from crypto_metrics and crypto_scores tables.

Indices computed:
    - SLI (Stablecoin Liquidity Impulse) - rate of change in stablecoin market cap
    - CFI (Crypto Fundamentals Index) - aggregate health of DeFi protocols
    - CDI (Crypto Developer Index) - development activity across protocols
    - CVI (Crypto Valuation Index) - aggregate valuation metrics (P/F, P/S)
    - CTI (Crypto Tier Index) - count/ratio of Tier 1 vs Avoid protocols

These indices integrate into Pillar 10 (Plumbing) and provide crypto-specific
signals for the broader macro framework.

Usage:
    python compute_crypto_indices.py              # Compute all crypto indices
    python compute_crypto_indices.py --latest     # Only compute latest date
    python compute_crypto_indices.py --verify     # Verify against thresholds
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os

# Add paths
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/Users/bob/LHM")

from lighthouse.config import DB_PATH as CONFIG_DB_PATH

# Database path
DB_PATH = Path("/Users/bob/LHM/Data/databases/Lighthouse_Master.db")


# ==========================================
# STATUS THRESHOLDS (Crypto-Specific)
# ==========================================

CRYPTO_STATUS_THRESHOLDS = {
    "SLI": [
        (1.5, "RAPID EXPANSION"),
        (0.5, "EXPANSION"),
        (-0.5, "STABLE"),
        (-1.0, "CONTRACTION"),
        (-999, "SEVERE CONTRACTION")
    ],
    "CFI": [
        (70, "STRONG FUNDAMENTALS"),
        (55, "HEALTHY"),
        (45, "NEUTRAL"),
        (35, "WEAK"),
        (-999, "POOR FUNDAMENTALS")
    ],
    "CDI": [
        (1.0, "HIGH ACTIVITY"),
        (0.5, "ACTIVE"),
        (-0.5, "MODERATE"),
        (-1.0, "LOW ACTIVITY"),
        (-999, "DORMANT")
    ],
    "CVI": [
        (1.5, "OVERVALUED"),
        (0.5, "RICH"),
        (-0.5, "FAIR VALUE"),
        (-1.0, "CHEAP"),
        (-999, "VERY CHEAP")
    ],
    "CTI": [
        (0.6, "BULLISH SETUP"),
        (0.4, "NEUTRAL"),
        (0.2, "CAUTIOUS"),
        (-999, "BEARISH SETUP")
    ],
    # Sector-specific
    "DEFI_HEALTH": [
        (70, "HEALTHY"),
        (50, "NEUTRAL"),
        (30, "WEAK"),
        (-999, "STRESSED")
    ],
    "L1_HEALTH": [
        (70, "STRONG"),
        (50, "NEUTRAL"),
        (30, "WEAK"),
        (-999, "STRESSED")
    ],
}


def get_crypto_status(index_name: str, value: float) -> str:
    """Get status label for a crypto index value."""
    if pd.isna(value):
        return "NO DATA"
    thresholds = CRYPTO_STATUS_THRESHOLDS.get(index_name, [])
    for threshold, status in thresholds:
        if value >= threshold:
            return status
    return "UNKNOWN"


# ==========================================
# Z-SCORE HELPER
# ==========================================

def compute_zscore(series: pd.Series, window: int = 30, min_periods: int = 10) -> pd.Series:
    """Compute rolling z-score."""
    rolling_mean = series.rolling(window, min_periods=min_periods).mean()
    rolling_std = series.rolling(window, min_periods=min_periods).std()
    rolling_std = rolling_std.replace(0, np.nan)
    return (series - rolling_mean) / rolling_std


# ==========================================
# CRYPTO INDEX COMPUTATIONS
# ==========================================

def compute_sli(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Stablecoin Liquidity Impulse (SLI)

    Measures rate of change in stablecoin/crypto market cap.
    Uses aggregate TVL from DeFi protocols as proxy for stablecoin liquidity.

    Formula:
        SLI = z(TVL_30d_RoC) where TVL_30d_RoC = (TVL_today - TVL_30d_ago) / TVL_30d_ago

    High SLI = Expanding liquidity = Bullish for risk assets
    Low SLI = Contracting liquidity = Bearish / Risk-off

    Returns:
        DataFrame with columns: date, SLI, TVL_Total, TVL_RoC_30d
    """
    # Query TVL data from crypto_metrics
    query = """
        SELECT date, SUM(value) as tvl_total
        FROM crypto_metrics
        WHERE metric_id = 'tvl'
        GROUP BY date
        ORDER BY date
    """

    try:
        df = pd.read_sql(query, conn, parse_dates=['date'])
        if df.empty:
            print("      Warning: No TVL data found for SLI computation")
            return pd.DataFrame(columns=["date", "SLI", "TVL_Total", "TVL_RoC_30d"])

        df = df.set_index('date').sort_index()

        # Compute 30-day rate of change
        df['tvl_30d_ago'] = df['tvl_total'].shift(30)
        df['tvl_roc_30d'] = (df['tvl_total'] - df['tvl_30d_ago']) / df['tvl_30d_ago']

        # Z-score the rate of change
        df['SLI'] = compute_zscore(df['tvl_roc_30d'], window=90, min_periods=30)

        # Prepare output
        result = df.reset_index()[['date', 'SLI', 'tvl_total', 'tvl_roc_30d']]
        result.columns = ['date', 'SLI', 'TVL_Total', 'TVL_RoC_30d']

        return result.dropna(subset=['SLI'])

    except Exception as e:
        print(f"      Error computing SLI: {e}")
        return pd.DataFrame(columns=["date", "SLI", "TVL_Total", "TVL_RoC_30d"])


def compute_cfi(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Crypto Fundamentals Index (CFI)

    Aggregate fundamental health score across tracked protocols.
    Uses the overall_score from crypto_scores table.

    Formula:
        CFI = mean(overall_score) across all protocols

    Returns:
        DataFrame with columns: date, CFI, protocols_count
    """
    query = """
        SELECT date, AVG(overall_score) as cfi, COUNT(*) as protocols_count
        FROM crypto_scores
        GROUP BY date
        ORDER BY date
    """

    try:
        df = pd.read_sql(query, conn, parse_dates=['date'])
        if df.empty:
            return pd.DataFrame(columns=["date", "CFI", "protocols_count"])

        df.columns = ['date', 'CFI', 'protocols_count']
        return df

    except Exception as e:
        print(f"      Error computing CFI: {e}")
        return pd.DataFrame(columns=["date", "CFI", "protocols_count"])


def compute_cdi(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Crypto Developer Index (CDI)

    Aggregate developer activity across protocols.
    Uses active_developers from crypto_scores.

    Formula:
        CDI = z(mean(active_developers))

    High CDI = Strong development activity across ecosystem
    Low CDI = Declining development activity

    Returns:
        DataFrame with columns: date, CDI, avg_developers, total_developers
    """
    query = """
        SELECT date,
               AVG(active_developers) as avg_devs,
               SUM(active_developers) as total_devs
        FROM crypto_scores
        GROUP BY date
        ORDER BY date
    """

    try:
        df = pd.read_sql(query, conn, parse_dates=['date'])
        if df.empty:
            return pd.DataFrame(columns=["date", "CDI", "avg_developers", "total_developers"])

        df = df.set_index('date')
        df['CDI'] = compute_zscore(df['avg_devs'], window=30, min_periods=10)

        result = df.reset_index()[['date', 'CDI', 'avg_devs', 'total_devs']]
        result.columns = ['date', 'CDI', 'avg_developers', 'total_developers']

        return result.dropna(subset=['CDI'])

    except Exception as e:
        print(f"      Error computing CDI: {e}")
        return pd.DataFrame(columns=["date", "CDI", "avg_developers", "total_developers"])


def compute_cvi(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Crypto Valuation Index (CVI)

    Aggregate valuation metrics across protocols.
    Uses P/E and P/F ratios from crypto_scores.

    Formula:
        CVI = z(mean(pe_ratio)) where pe_ratio is capped at 500

    High CVI = Expensive valuations (overvalued)
    Low CVI = Cheap valuations (potentially undervalued)

    Returns:
        DataFrame with columns: date, CVI, avg_pe, avg_pf
    """
    query = """
        SELECT date,
               AVG(CASE WHEN pe_ratio < 500 THEN pe_ratio ELSE NULL END) as avg_pe,
               AVG(CASE WHEN pf_ratio < 1000 THEN pf_ratio ELSE NULL END) as avg_pf
        FROM crypto_scores
        GROUP BY date
        ORDER BY date
    """

    try:
        df = pd.read_sql(query, conn, parse_dates=['date'])
        if df.empty:
            return pd.DataFrame(columns=["date", "CVI", "avg_pe", "avg_pf"])

        df = df.set_index('date')
        df['CVI'] = compute_zscore(df['avg_pe'], window=30, min_periods=10)

        result = df.reset_index()[['date', 'CVI', 'avg_pe', 'avg_pf']]
        result.columns = ['date', 'CVI', 'avg_pe', 'avg_pf']

        return result.dropna(subset=['CVI'])

    except Exception as e:
        print(f"      Error computing CVI: {e}")
        return pd.DataFrame(columns=["date", "CVI", "avg_pe", "avg_pf"])


def compute_cti(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Crypto Tier Index (CTI)

    Ratio of Tier 1/Tier 2 protocols vs Avoid/Caution.
    Indicates overall health of the crypto ecosystem from fundamental perspective.

    Formula:
        CTI = (Tier1_count + Tier2_count) / total_count

    High CTI (>0.6) = Most protocols are fundamentally sound = Bullish
    Low CTI (<0.3) = Most protocols are problematic = Bearish

    Returns:
        DataFrame with columns: date, CTI, tier1_count, tier2_count, avoid_count
    """
    query = """
        SELECT date,
               SUM(CASE WHEN verdict LIKE '%TIER 1%' THEN 1 ELSE 0 END) as tier1_count,
               SUM(CASE WHEN verdict LIKE '%TIER 2%' THEN 1 ELSE 0 END) as tier2_count,
               SUM(CASE WHEN verdict LIKE '%AVOID%' THEN 1 ELSE 0 END) as avoid_count,
               COUNT(*) as total_count
        FROM crypto_scores
        GROUP BY date
        ORDER BY date
    """

    try:
        df = pd.read_sql(query, conn, parse_dates=['date'])
        if df.empty:
            return pd.DataFrame(columns=["date", "CTI", "tier1_count", "tier2_count", "avoid_count"])

        df['CTI'] = (df['tier1_count'] + df['tier2_count']) / df['total_count']

        return df[['date', 'CTI', 'tier1_count', 'tier2_count', 'avoid_count']]

    except Exception as e:
        print(f"      Error computing CTI: {e}")
        return pd.DataFrame(columns=["date", "CTI", "tier1_count", "tier2_count", "avoid_count"])


def compute_sector_health(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Sector-specific health indices.

    Computes average overall_score for each sector.

    Returns:
        DataFrame with columns: date, sector, health_score, protocol_count
    """
    query = """
        SELECT date, sector, AVG(overall_score) as health_score, COUNT(*) as protocol_count
        FROM crypto_scores
        GROUP BY date, sector
        ORDER BY date, sector
    """

    try:
        df = pd.read_sql(query, conn, parse_dates=['date'])
        return df

    except Exception as e:
        print(f"      Error computing sector health: {e}")
        return pd.DataFrame(columns=["date", "sector", "health_score", "protocol_count"])


# ==========================================
# MAIN COMPUTATION ENGINE
# ==========================================

def compute_all_crypto_indices(conn: sqlite3.Connection, latest_only: bool = False) -> pd.DataFrame:
    """
    Compute all crypto indices.

    Args:
        conn: Database connection
        latest_only: If True, filter to latest date only

    Returns:
        DataFrame with columns: date, index_id, value, status
    """
    print("\n--- Computing Crypto Indices ---")

    # Compute each index
    print("   Computing SLI (Stablecoin Liquidity Impulse)...")
    sli_df = compute_sli(conn)

    print("   Computing CFI (Crypto Fundamentals Index)...")
    cfi_df = compute_cfi(conn)

    print("   Computing CDI (Crypto Developer Index)...")
    cdi_df = compute_cdi(conn)

    print("   Computing CVI (Crypto Valuation Index)...")
    cvi_df = compute_cvi(conn)

    print("   Computing CTI (Crypto Tier Index)...")
    cti_df = compute_cti(conn)

    print("   Computing Sector Health Indices...")
    sector_df = compute_sector_health(conn)

    # Build output rows
    rows = []

    # Add SLI
    for _, row in sli_df.iterrows():
        rows.append({
            "date": row['date'].strftime("%Y-%m-%d") if hasattr(row['date'], 'strftime') else str(row['date']),
            "index_id": "SLI",
            "value": round(row['SLI'], 4),
            "status": get_crypto_status("SLI", row['SLI'])
        })

    # Add CFI
    for _, row in cfi_df.iterrows():
        rows.append({
            "date": row['date'].strftime("%Y-%m-%d") if hasattr(row['date'], 'strftime') else str(row['date']),
            "index_id": "CFI",
            "value": round(row['CFI'], 2),
            "status": get_crypto_status("CFI", row['CFI'])
        })

    # Add CDI
    for _, row in cdi_df.iterrows():
        rows.append({
            "date": row['date'].strftime("%Y-%m-%d") if hasattr(row['date'], 'strftime') else str(row['date']),
            "index_id": "CDI",
            "value": round(row['CDI'], 4),
            "status": get_crypto_status("CDI", row['CDI'])
        })

    # Add CVI
    for _, row in cvi_df.iterrows():
        rows.append({
            "date": row['date'].strftime("%Y-%m-%d") if hasattr(row['date'], 'strftime') else str(row['date']),
            "index_id": "CVI",
            "value": round(row['CVI'], 4),
            "status": get_crypto_status("CVI", row['CVI'])
        })

    # Add CTI
    for _, row in cti_df.iterrows():
        rows.append({
            "date": row['date'].strftime("%Y-%m-%d") if hasattr(row['date'], 'strftime') else str(row['date']),
            "index_id": "CTI",
            "value": round(row['CTI'], 4),
            "status": get_crypto_status("CTI", row['CTI'])
        })

    # Add Sector Health
    for _, row in sector_df.iterrows():
        sector_name = row['sector'].upper().replace(' ', '_').replace('-', '_')[:20]
        index_id = f"CRYPTO_{sector_name}_HEALTH"
        rows.append({
            "date": row['date'].strftime("%Y-%m-%d") if hasattr(row['date'], 'strftime') else str(row['date']),
            "index_id": index_id,
            "value": round(row['health_score'], 2),
            "status": get_crypto_status("DEFI_HEALTH", row['health_score'])
        })

    result_df = pd.DataFrame(rows)

    if latest_only and not result_df.empty:
        latest_date = result_df['date'].max()
        result_df = result_df[result_df['date'] == latest_date]

    print(f"   Generated {len(result_df)} crypto index observations")

    return result_df


def write_crypto_indices_to_db(conn: sqlite3.Connection, indices_df: pd.DataFrame):
    """Write computed crypto indices to lighthouse_indices table."""
    c = conn.cursor()

    # Create table if not exists (same schema as macro indices)
    c.execute('''CREATE TABLE IF NOT EXISTS lighthouse_indices (
        date TEXT,
        index_id TEXT,
        value REAL,
        status TEXT,
        PRIMARY KEY (date, index_id)
    )''')

    # Insert/replace data
    for _, row in indices_df.iterrows():
        c.execute("""
            INSERT OR REPLACE INTO lighthouse_indices (date, index_id, value, status)
            VALUES (?, ?, ?, ?)
        """, (row["date"], row["index_id"], row["value"], row["status"]))

    conn.commit()
    print(f"   Wrote {len(indices_df)} crypto index rows to lighthouse_indices")


def verify_crypto_indices(conn: sqlite3.Connection):
    """Verify latest crypto index values."""
    print("\n--- Verification: Latest Crypto Index Values ---")

    query = """
        SELECT index_id, value, status, date
        FROM lighthouse_indices
        WHERE index_id IN ('SLI', 'CFI', 'CDI', 'CVI', 'CTI')
           OR index_id LIKE 'CRYPTO_%_HEALTH'
        AND date = (SELECT MAX(date) FROM lighthouse_indices WHERE index_id = 'SLI')
        ORDER BY index_id
    """

    try:
        latest = pd.read_sql(query, conn)

        if latest.empty:
            print("   No crypto indices found in database")
            return

        print(f"\nLatest crypto values ({latest['date'].iloc[0] if len(latest) > 0 else 'N/A'}):")
        print("-" * 60)

        for _, row in latest.iterrows():
            status_str = row['status'] if row['status'] else "N/A"
            print(f"   {row['index_id']:25} {row['value']:>10.3f}  [{status_str}]")

        print("-" * 60)

    except Exception as e:
        print(f"   Error verifying indices: {e}")


# ==========================================
# CLI
# ==========================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Compute Lighthouse Macro Crypto Indices")
    parser.add_argument("--latest", action="store_true", help="Only compute latest date")
    parser.add_argument("--verify", action="store_true", help="Verify against expected values")
    parser.add_argument("--dry-run", action="store_true", help="Compute but don't write to database")

    args = parser.parse_args()

    print("=" * 70)
    print("LIGHTHOUSE MACRO - CRYPTO INDEX COMPUTATION")
    print(f"Database: {DB_PATH}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    conn = sqlite3.connect(DB_PATH)

    # Check if crypto tables exist
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='crypto_scores'")
    if not c.fetchone():
        print("\nWARNING: crypto_scores table does not exist.")
        print("Run the pipeline with --sources CRYPTO first to populate crypto data.")
        conn.close()
        return

    # Compute indices
    indices_df = compute_all_crypto_indices(conn, latest_only=args.latest)

    if indices_df.empty:
        print("\nNo crypto indices computed - ensure crypto data is populated first.")
        conn.close()
        return

    # Write to database
    if not args.dry_run:
        print("\n--- Writing to Database ---")
        write_crypto_indices_to_db(conn, indices_df)
    else:
        print("\n--- Dry Run: Skipping database write ---")

    # Verify
    if args.verify or not args.dry_run:
        verify_crypto_indices(conn)

    conn.close()

    print("\n" + "=" * 70)
    print("CRYPTO INDEX COMPUTATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
