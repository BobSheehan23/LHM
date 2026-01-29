#!/usr/bin/env python3
"""
LCI Forward-Looking Analysis
============================
Tests whether LCI *predicts* future returns, not just correlates concurrently.

This script produces:
1. Lead-lag analysis (cross-correlation at various lags)
2. Granger causality tests
3. Information Coefficient (IC) at multiple forward horizons
4. Regime-conditioned forward returns
5. Out-of-sample predictive tests

Output: Tables and stats for the LIQUIDITY_ANALYSIS_COMBINED.md writeup
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

import sys
sys.path.insert(0, '/Users/bob/LHM/Charts/ConksRebuttal')
sys.path.insert(0, '/Users/bob/LHM/lighthouse_quant/validation')

from lci_calculator import calculate_lci
from lead_lag import (
    compute_cross_correlation,
    granger_causality_test,
    compute_information_coefficient
)

import yfinance as yf
from scipy import stats


def fetch_asset_prices():
    """Fetch SPX and BTC price data"""
    print("Fetching asset prices...")

    # SPX
    spx_df = yf.download('^GSPC', start='2003-01-01', progress=False)
    spx = spx_df['Close'].squeeze()
    spx.name = 'SPX'
    # Remove duplicate indices
    spx = spx[~spx.index.duplicated(keep='first')]
    # Remove timezone info if present
    if spx.index.tz is not None:
        spx.index = spx.index.tz_localize(None)

    # BTC
    btc_df = yf.download('BTC-USD', start='2014-01-01', progress=False)
    btc = btc_df['Close'].squeeze()
    btc.name = 'BTC'
    # Remove duplicate indices
    btc = btc[~btc.index.duplicated(keep='first')]
    # Remove timezone info if present
    if btc.index.tz is not None:
        btc.index = btc.index.tz_localize(None)

    return spx, btc


def calculate_forward_returns(prices, periods=[5, 10, 21, 63]):
    """Calculate forward returns at multiple horizons"""
    returns = pd.DataFrame(index=prices.index)
    for p in periods:
        returns[f'fwd_{p}d'] = prices.pct_change(p).shift(-p) * 100
    return returns


def run_lead_lag_analysis(lci, returns, asset_name, max_lag=30):
    """Run cross-correlation analysis"""
    print(f"\n{'='*60}")
    print(f"LEAD-LAG ANALYSIS: LCI vs {asset_name}")
    print('='*60)

    # Clean up indices - remove duplicates
    lci_clean = lci[~lci.index.duplicated(keep='first')].rename('LCI')
    returns_clean = returns[~returns.index.duplicated(keep='first')]

    # Align data
    df = pd.concat([lci_clean, returns_clean], axis=1).dropna()

    results = []
    for col in returns.columns:
        if col not in df.columns:
            continue

        try:
            lags, corrs = compute_cross_correlation(
                df['LCI'],
                df[col],
                max_lag=max_lag
            )

            # Find optimal lag
            opt_idx = np.nanargmax(corrs)
            opt_lag = lags[opt_idx]
            opt_corr = corrs[opt_idx]

            # Zero-lag correlation
            zero_idx = np.where(lags == 0)[0][0]
            zero_corr = corrs[zero_idx]

            results.append({
                'horizon': col,
                'optimal_lag': opt_lag,
                'corr_at_optimal': opt_corr,
                'corr_at_zero': zero_corr,
                'improvement': opt_corr - zero_corr
            })

            print(f"\n{col}:")
            print(f"  Optimal lag: {opt_lag} days (LCI leads by {opt_lag} days)")
            print(f"  Correlation at optimal: {opt_corr:.4f}")
            print(f"  Correlation at zero: {zero_corr:.4f}")
            print(f"  Improvement from lead: {opt_corr - zero_corr:.4f}")

        except Exception as e:
            print(f"  Error with {col}: {e}")

    return pd.DataFrame(results)


def run_granger_tests(lci, returns, asset_name, max_lag=12):
    """Run Granger causality tests"""
    print(f"\n{'='*60}")
    print(f"GRANGER CAUSALITY: LCI -> {asset_name} Returns")
    print('='*60)

    lci_clean = lci[~lci.index.duplicated(keep='first')].rename('LCI')
    returns_clean = returns[~returns.index.duplicated(keep='first')]
    df = pd.concat([lci_clean, returns_clean], axis=1).dropna()

    results = []
    for col in returns.columns:
        if col not in df.columns:
            continue

        pvals = granger_causality_test(df['LCI'], df[col], max_lag=max_lag)

        if pvals:
            min_pval = min(pvals.values())
            best_lag = min(pvals, key=pvals.get)
            significant = min_pval < 0.05

            results.append({
                'horizon': col,
                'best_lag': best_lag,
                'min_pvalue': min_pval,
                'significant': significant
            })

            print(f"\n{col}:")
            print(f"  Best lag: {best_lag}")
            print(f"  Min p-value: {min_pval:.6f}")
            print(f"  Significant (p<0.05): {'YES ***' if significant else 'No'}")

    return pd.DataFrame(results)


def run_information_coefficient(lci, returns, asset_name):
    """Calculate IC at various forward periods"""
    print(f"\n{'='*60}")
    print(f"INFORMATION COEFFICIENT: LCI -> {asset_name}")
    print('='*60)

    lci_clean = lci[~lci.index.duplicated(keep='first')].rename('LCI')
    returns_clean = returns[~returns.index.duplicated(keep='first')]
    df = pd.concat([lci_clean, returns_clean], axis=1).dropna()

    # Map return columns to periods
    period_map = {
        'fwd_5d': 5,
        'fwd_10d': 10,
        'fwd_21d': 21,
        'fwd_63d': 63
    }

    results = []
    for col, period in period_map.items():
        if col not in df.columns:
            continue

        # IC is correlation of signal with forward returns
        ic = df['LCI'].corr(df[col])

        # Test significance
        n = len(df.dropna(subset=['LCI', col]))
        t_stat = ic * np.sqrt(n - 2) / np.sqrt(1 - ic**2)
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n - 2))

        results.append({
            'horizon': col,
            'period_days': period,
            'IC': ic,
            't_stat': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        })

        sig_marker = '***' if p_value < 0.01 else ('**' if p_value < 0.05 else '')
        print(f"{col} ({period}d): IC = {ic:.4f}, t = {t_stat:.2f}, p = {p_value:.4f} {sig_marker}")

    return pd.DataFrame(results)


def run_regime_forward_returns(lci, returns, asset_name):
    """Analyze forward returns by LCI regime"""
    print(f"\n{'='*60}")
    print(f"REGIME-CONDITIONED FORWARD RETURNS: {asset_name}")
    print('='*60)

    lci_clean = lci[~lci.index.duplicated(keep='first')].rename('LCI')
    returns_clean = returns[~returns.index.duplicated(keep='first')]
    df = pd.concat([lci_clean, returns_clean], axis=1).dropna()

    # Define regimes
    df['regime'] = pd.cut(
        df['LCI'],
        bins=[-np.inf, -0.5, 0.5, np.inf],
        labels=['Scarce', 'Neutral', 'Ample']
    )

    results = []
    for col in returns.columns:
        if col not in df.columns:
            continue

        print(f"\n{col}:")
        regime_stats = df.groupby('regime')[col].agg(['mean', 'std', 'count'])

        for regime in ['Scarce', 'Neutral', 'Ample']:
            if regime in regime_stats.index:
                mean = regime_stats.loc[regime, 'mean']
                std = regime_stats.loc[regime, 'std']
                n = regime_stats.loc[regime, 'count']
                print(f"  {regime}: {mean:.2f}% (std={std:.2f}%, n={n:.0f})")

                results.append({
                    'horizon': col,
                    'regime': regime,
                    'mean_return': mean,
                    'std': std,
                    'n': n
                })

        # T-test: Ample vs Scarce
        if 'Ample' in df['regime'].values and 'Scarce' in df['regime'].values:
            ample = df[df['regime'] == 'Ample'][col].dropna()
            scarce = df[df['regime'] == 'Scarce'][col].dropna()

            if len(ample) > 10 and len(scarce) > 10:
                t_stat, p_val = stats.ttest_ind(ample, scarce, equal_var=False)
                spread = ample.mean() - scarce.mean()
                print(f"  Ample-Scarce spread: {spread:.2f}% (t={t_stat:.2f}, p={p_val:.4f})")

    return pd.DataFrame(results)


def run_out_of_sample_test(lci, returns, asset_name, train_pct=0.7):
    """Out-of-sample predictive test"""
    print(f"\n{'='*60}")
    print(f"OUT-OF-SAMPLE TEST: {asset_name}")
    print('='*60)

    lci_clean = lci[~lci.index.duplicated(keep='first')].rename('LCI')
    returns_clean = returns[~returns.index.duplicated(keep='first')]
    df = pd.concat([lci_clean, returns_clean], axis=1).dropna()

    # Split
    n = len(df)
    train_end = int(n * train_pct)
    train = df.iloc[:train_end]
    test = df.iloc[train_end:]

    print(f"Train period: {train.index.min().date()} to {train.index.max().date()} ({len(train)} obs)")
    print(f"Test period: {test.index.min().date()} to {test.index.max().date()} ({len(test)} obs)")

    results = []
    for col in returns.columns:
        if col not in df.columns:
            continue

        # In-sample correlation
        is_corr = train['LCI'].corr(train[col])

        # Out-of-sample correlation
        oos_corr = test['LCI'].corr(test[col])

        # Regime performance OOS
        test_with_regime = test.copy()
        test_with_regime['regime'] = pd.cut(
            test_with_regime['LCI'],
            bins=[-np.inf, -0.5, 0.5, np.inf],
            labels=['Scarce', 'Neutral', 'Ample']
        )

        regime_means = test_with_regime.groupby('regime')[col].mean()

        ample_oos = regime_means.get('Ample', np.nan)
        scarce_oos = regime_means.get('Scarce', np.nan)
        spread_oos = ample_oos - scarce_oos if pd.notna(ample_oos) and pd.notna(scarce_oos) else np.nan

        results.append({
            'horizon': col,
            'is_corr': is_corr,
            'oos_corr': oos_corr,
            'oos_ample': ample_oos,
            'oos_scarce': scarce_oos,
            'oos_spread': spread_oos
        })

        print(f"\n{col}:")
        print(f"  In-sample IC: {is_corr:.4f}")
        print(f"  Out-of-sample IC: {oos_corr:.4f}")
        print(f"  OOS Ample-Scarce spread: {spread_oos:.2f}%" if pd.notna(spread_oos) else "  OOS spread: N/A")

    return pd.DataFrame(results)


def run_rolling_predictive_power(lci, returns, asset_name, window=252):
    """Rolling window IC to test stability"""
    print(f"\n{'='*60}")
    print(f"ROLLING IC STABILITY: {asset_name}")
    print('='*60)

    lci_clean = lci[~lci.index.duplicated(keep='first')].rename('LCI')
    returns_clean = returns[~returns.index.duplicated(keep='first')]
    df = pd.concat([lci_clean, returns_clean], axis=1).dropna()

    results = {}
    for col in returns.columns:
        if col not in df.columns:
            continue

        # Rolling correlation
        rolling_ic = df['LCI'].rolling(window).corr(df[col])

        results[col] = {
            'mean_ic': rolling_ic.mean(),
            'std_ic': rolling_ic.std(),
            'pct_positive': (rolling_ic > 0).mean() * 100,
            'min_ic': rolling_ic.min(),
            'max_ic': rolling_ic.max()
        }

        print(f"\n{col} (rolling {window}d):")
        print(f"  Mean IC: {results[col]['mean_ic']:.4f}")
        print(f"  Std IC: {results[col]['std_ic']:.4f}")
        print(f"  % Positive: {results[col]['pct_positive']:.1f}%")
        print(f"  Range: [{results[col]['min_ic']:.4f}, {results[col]['max_ic']:.4f}]")

    return results


def main():
    """Run full forward-looking analysis"""
    print("="*60)
    print("LCI FORWARD-LOOKING ANALYSIS")
    print("Testing: Does LCI *predict* future returns?")
    print("="*60)

    # Calculate LCI (using original formula that showed strong results)
    print("\n[1/7] Calculating LCI...")
    lci_df = calculate_lci(version='original')
    lci = lci_df['LCI']

    # Fetch prices
    print("\n[2/7] Fetching asset prices...")
    spx, btc = fetch_asset_prices()

    # Calculate forward returns
    print("\n[3/7] Calculating forward returns...")
    spx_fwd = calculate_forward_returns(spx)
    btc_fwd = calculate_forward_returns(btc)

    # Align LCI with each asset
    lci_for_spx = lci.copy()
    lci_for_btc = lci.copy()

    # === RUN ALL ANALYSES ===

    all_results = {}

    # SPX Analysis
    print("\n" + "="*60)
    print("ANALYZING: S&P 500")
    print("="*60)

    all_results['spx_lead_lag'] = run_lead_lag_analysis(lci_for_spx, spx_fwd, 'SPX')
    all_results['spx_granger'] = run_granger_tests(lci_for_spx, spx_fwd, 'SPX')
    all_results['spx_ic'] = run_information_coefficient(lci_for_spx, spx_fwd, 'SPX')
    all_results['spx_regime'] = run_regime_forward_returns(lci_for_spx, spx_fwd, 'SPX')
    all_results['spx_oos'] = run_out_of_sample_test(lci_for_spx, spx_fwd, 'SPX')
    all_results['spx_rolling'] = run_rolling_predictive_power(lci_for_spx, spx_fwd, 'SPX')

    # BTC Analysis
    print("\n" + "="*60)
    print("ANALYZING: Bitcoin")
    print("="*60)

    all_results['btc_lead_lag'] = run_lead_lag_analysis(lci_for_btc, btc_fwd, 'BTC')
    all_results['btc_granger'] = run_granger_tests(lci_for_btc, btc_fwd, 'BTC')
    all_results['btc_ic'] = run_information_coefficient(lci_for_btc, btc_fwd, 'BTC')
    all_results['btc_regime'] = run_regime_forward_returns(lci_for_btc, btc_fwd, 'BTC')
    all_results['btc_oos'] = run_out_of_sample_test(lci_for_btc, btc_fwd, 'BTC')
    all_results['btc_rolling'] = run_rolling_predictive_power(lci_for_btc, btc_fwd, 'BTC')

    # === SUMMARY ===
    print("\n" + "="*60)
    print("SUMMARY: KEY FINDINGS")
    print("="*60)

    print("\n### PREDICTIVE POWER (Information Coefficient)")
    print("\nSPX:")
    if 'spx_ic' in all_results and len(all_results['spx_ic']) > 0:
        for _, row in all_results['spx_ic'].iterrows():
            sig = '***' if row['p_value'] < 0.01 else ('**' if row['p_value'] < 0.05 else '')
            print(f"  {row['horizon']}: IC = {row['IC']:.4f} {sig}")

    print("\nBTC:")
    if 'btc_ic' in all_results and len(all_results['btc_ic']) > 0:
        for _, row in all_results['btc_ic'].iterrows():
            sig = '***' if row['p_value'] < 0.01 else ('**' if row['p_value'] < 0.05 else '')
            print(f"  {row['horizon']}: IC = {row['IC']:.4f} {sig}")

    print("\n### GRANGER CAUSALITY")
    print("\nSPX:")
    if 'spx_granger' in all_results and len(all_results['spx_granger']) > 0:
        for _, row in all_results['spx_granger'].iterrows():
            sig = 'YES ***' if row['significant'] else 'No'
            print(f"  {row['horizon']}: p = {row['min_pvalue']:.4f} ({sig})")

    print("\nBTC:")
    if 'btc_granger' in all_results and len(all_results['btc_granger']) > 0:
        for _, row in all_results['btc_granger'].iterrows():
            sig = 'YES ***' if row['significant'] else 'No'
            print(f"  {row['horizon']}: p = {row['min_pvalue']:.4f} ({sig})")

    print("\n### OUT-OF-SAMPLE PERFORMANCE")
    print("\nSPX:")
    if 'spx_oos' in all_results and len(all_results['spx_oos']) > 0:
        for _, row in all_results['spx_oos'].iterrows():
            print(f"  {row['horizon']}: IS IC = {row['is_corr']:.4f}, OOS IC = {row['oos_corr']:.4f}, OOS Spread = {row['oos_spread']:.2f}%")

    print("\nBTC:")
    if 'btc_oos' in all_results and len(all_results['btc_oos']) > 0:
        for _, row in all_results['btc_oos'].iterrows():
            spread_str = f"{row['oos_spread']:.2f}%" if pd.notna(row['oos_spread']) else "N/A"
            print(f"  {row['horizon']}: IS IC = {row['is_corr']:.4f}, OOS IC = {row['oos_corr']:.4f}, OOS Spread = {spread_str}")

    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)

    return all_results


if __name__ == '__main__':
    results = main()
