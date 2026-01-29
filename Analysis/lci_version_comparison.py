#!/usr/bin/env python3
"""
LCI Version Comparison Analysis
===============================
Tests whether different LCI versions work better for different asset classes.

Hypothesis:
- SPX: V2 (NFCI-heavy) may outperform
- BTC: Original (pure plumbing) may outperform

Versions tested:
- Original: (RRP + Reserves) / 2
- V1: Full formula with all components
- V2: NFCI-heavy (50% NFCI)
- V3: Pure Fed plumbing (no NFCI)
- Production: Current balanced formula
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3
import warnings
warnings.filterwarnings('ignore')

import sys
sys.path.insert(0, '/Users/bob/LHM/Charts/ConksRebuttal')

from lci_calculator import calculate_lci
import yfinance as yf
from scipy import stats


DB_PATH = '/Users/bob/LHM/Data/databases/Lighthouse_Master.db'


def load_production_lci():
    """Load production LCI from database"""
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT date, value as LCI
    FROM lighthouse_indices
    WHERE index_id = 'LCI'
    ORDER BY date
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    df = df[~df.index.duplicated(keep='first')]
    return df['LCI'].rename('Production')


def fetch_asset_prices():
    """Fetch SPX and BTC price data"""
    print("Fetching asset prices...")

    spx_df = yf.download('^GSPC', start='2003-01-01', progress=False)
    spx = spx_df['Close'].squeeze()
    spx.name = 'SPX'
    spx = spx[~spx.index.duplicated(keep='first')]
    if spx.index.tz is not None:
        spx.index = spx.index.tz_localize(None)

    btc_df = yf.download('BTC-USD', start='2014-01-01', progress=False)
    btc = btc_df['Close'].squeeze()
    btc.name = 'BTC'
    btc = btc[~btc.index.duplicated(keep='first')]
    if btc.index.tz is not None:
        btc.index = btc.index.tz_localize(None)

    return spx, btc


def calculate_forward_returns(prices, periods=[5, 10, 21, 63]):
    """Calculate forward returns at multiple horizons"""
    returns = pd.DataFrame(index=prices.index)
    for p in periods:
        returns[f'fwd_{p}d'] = prices.pct_change(p).shift(-p) * 100
    return returns


def compute_metrics(lci, returns, asset_name):
    """Compute IC and regime spread for a given LCI version"""
    lci_clean = lci[~lci.index.duplicated(keep='first')]
    returns_clean = returns[~returns.index.duplicated(keep='first')]

    df = pd.concat([lci_clean.rename('LCI'), returns_clean], axis=1).dropna()

    results = {}

    for col in returns.columns:
        if col not in df.columns:
            continue

        # IC
        ic = df['LCI'].corr(df[col])
        n = len(df.dropna(subset=['LCI', col]))
        if n > 20 and abs(ic) < 1:
            t_stat = ic * np.sqrt(n - 2) / np.sqrt(1 - ic**2)
            p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n - 2))
        else:
            t_stat = np.nan
            p_value = np.nan

        # Regime spread
        df_temp = df.copy()
        df_temp['regime'] = pd.cut(
            df_temp['LCI'],
            bins=[-np.inf, -0.5, 0.5, np.inf],
            labels=['Scarce', 'Neutral', 'Ample']
        )

        ample = df_temp[df_temp['regime'] == 'Ample'][col].dropna()
        scarce = df_temp[df_temp['regime'] == 'Scarce'][col].dropna()

        if len(ample) > 10 and len(scarce) > 10:
            spread = ample.mean() - scarce.mean()
            t_spread, p_spread = stats.ttest_ind(ample, scarce, equal_var=False)
        else:
            spread = np.nan
            t_spread = np.nan
            p_spread = np.nan

        results[col] = {
            'IC': ic,
            't_stat': t_stat,
            'p_value': p_value,
            'spread': spread,
            't_spread': t_spread,
            'p_spread': p_spread,
            'n': n
        }

    return results


def main():
    print("="*70)
    print("LCI VERSION COMPARISON ANALYSIS")
    print("Testing: Which LCI version works best for each asset class?")
    print("="*70)

    # === CALCULATE ALL LCI VERSIONS ===
    print("\n[1/5] Calculating LCI versions from source data...")

    versions = {}

    print("  Calculating Original (RRP + Reserves)...")
    df_original = calculate_lci(version='original')
    versions['Original'] = df_original['LCI']

    print("\n  Calculating V1 (Full formula)...")
    df_v1 = calculate_lci(version='v1')
    versions['V1'] = df_v1['LCI']

    print("\n  Calculating V2 (NFCI-heavy)...")
    df_v2 = calculate_lci(version='v2')
    versions['V2'] = df_v2['LCI']

    print("\n  Calculating V3 (Pure plumbing)...")
    df_v3 = calculate_lci(version='v3')
    versions['V3'] = df_v3['LCI']

    print("\n  Loading Production from database...")
    versions['Production'] = load_production_lci()

    # === FETCH ASSET PRICES ===
    print("\n[2/5] Fetching asset prices...")
    spx, btc = fetch_asset_prices()

    # === CALCULATE FORWARD RETURNS ===
    print("\n[3/5] Calculating forward returns...")
    spx_fwd = calculate_forward_returns(spx)
    btc_fwd = calculate_forward_returns(btc)

    # === RUN COMPARISON ===
    print("\n[4/5] Running comparison analysis...")

    all_results = {'SPX': {}, 'BTC': {}}

    for version_name, lci in versions.items():
        print(f"\n  Testing {version_name}...")
        all_results['SPX'][version_name] = compute_metrics(lci, spx_fwd, 'SPX')
        all_results['BTC'][version_name] = compute_metrics(lci, btc_fwd, 'BTC')

    # === OUTPUT RESULTS ===
    print("\n" + "="*70)
    print("[5/5] RESULTS")
    print("="*70)

    horizons = ['fwd_5d', 'fwd_10d', 'fwd_21d', 'fwd_63d']

    for asset in ['SPX', 'BTC']:
        print(f"\n{'='*70}")
        print(f"{asset} - INFORMATION COEFFICIENT BY LCI VERSION")
        print("="*70)

        # Header
        print(f"\n{'Version':<12} | {'5d IC':>8} | {'10d IC':>8} | {'21d IC':>8} | {'63d IC':>8}")
        print("-"*60)

        for version_name in ['Original', 'V1', 'V2', 'V3', 'Production']:
            row = f"{version_name:<12} |"
            for h in horizons:
                if h in all_results[asset][version_name]:
                    ic = all_results[asset][version_name][h]['IC']
                    p = all_results[asset][version_name][h]['p_value']
                    sig = '***' if p < 0.01 else ('**' if p < 0.05 else ('*' if p < 0.1 else ''))
                    row += f" {ic:>6.3f}{sig:<2} |"
                else:
                    row += f" {'N/A':>8} |"
            print(row)

        print(f"\n{'='*70}")
        print(f"{asset} - REGIME SPREAD (Ample - Scarce) BY LCI VERSION")
        print("="*70)

        print(f"\n{'Version':<12} | {'5d Sprd':>8} | {'10d Sprd':>8} | {'21d Sprd':>8} | {'63d Sprd':>8}")
        print("-"*60)

        for version_name in ['Original', 'V1', 'V2', 'V3', 'Production']:
            row = f"{version_name:<12} |"
            for h in horizons:
                if h in all_results[asset][version_name]:
                    spread = all_results[asset][version_name][h]['spread']
                    p = all_results[asset][version_name][h]['p_spread']
                    if pd.notna(spread):
                        sig = '***' if p < 0.01 else ('**' if p < 0.05 else ('*' if p < 0.1 else ''))
                        row += f" {spread:>5.2f}%{sig:<2}|"
                    else:
                        row += f" {'N/A':>8} |"
                else:
                    row += f" {'N/A':>8} |"
            print(row)

    # === WINNER SUMMARY ===
    print("\n" + "="*70)
    print("WINNER SUMMARY")
    print("="*70)

    for asset in ['SPX', 'BTC']:
        print(f"\n{asset}:")
        for h in horizons:
            best_ic = -999
            best_version = None
            for version_name in versions.keys():
                if h in all_results[asset][version_name]:
                    ic = all_results[asset][version_name][h]['IC']
                    if pd.notna(ic) and ic > best_ic:
                        best_ic = ic
                        best_version = version_name

            if best_version:
                print(f"  {h}: {best_version} (IC = {best_ic:.4f})")

    # === HYPOTHESIS TEST ===
    print("\n" + "="*70)
    print("HYPOTHESIS TEST")
    print("="*70)

    print("\nHypothesis 1: V2 (NFCI-heavy) outperforms for SPX")
    v2_wins_spx = 0
    prod_wins_spx = 0
    for h in horizons:
        v2_ic = all_results['SPX']['V2'][h]['IC'] if h in all_results['SPX']['V2'] else np.nan
        prod_ic = all_results['SPX']['Production'][h]['IC'] if h in all_results['SPX']['Production'] else np.nan
        if pd.notna(v2_ic) and pd.notna(prod_ic):
            if v2_ic > prod_ic:
                v2_wins_spx += 1
            else:
                prod_wins_spx += 1
    print(f"  V2 wins {v2_wins_spx}/4 horizons vs Production")
    print(f"  Result: {'CONFIRMED' if v2_wins_spx >= 3 else 'NOT CONFIRMED'}")

    print("\nHypothesis 2: Original (pure plumbing) outperforms for BTC")
    orig_wins_btc = 0
    prod_wins_btc = 0
    for h in horizons:
        orig_ic = all_results['BTC']['Original'][h]['IC'] if h in all_results['BTC']['Original'] else np.nan
        prod_ic = all_results['BTC']['Production'][h]['IC'] if h in all_results['BTC']['Production'] else np.nan
        if pd.notna(orig_ic) and pd.notna(prod_ic):
            if orig_ic > prod_ic:
                orig_wins_btc += 1
            else:
                prod_wins_btc += 1
    print(f"  Original wins {orig_wins_btc}/4 horizons vs Production")
    print(f"  Result: {'CONFIRMED' if orig_wins_btc >= 3 else 'NOT CONFIRMED'}")

    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)

    return all_results


if __name__ == '__main__':
    results = main()
