"""
CLTI Backtest v2: Crypto-Liquidity Transmission Index
=====================================================
Iterative build with stablecoins from DefiLlama.
Tests multiple weight configurations, component combinations,
and identifies the optimal composite.

Author: Lighthouse Macro
Date: 2026-02-12
"""

import sqlite3
import pandas as pd
import numpy as np
from scipy import stats
import yfinance as yf
import requests
import time
import warnings
import itertools
warnings.filterwarnings('ignore')

DB_PATH = '/Users/bob/LHM/Data/databases/Lighthouse_Master.db'


# ============================================================
# DATA LOADING
# ============================================================

def load_series(conn, series_id):
    df = pd.read_sql(
        "SELECT date, value FROM observations WHERE series_id = ? ORDER BY date",
        conn, params=(series_id,), parse_dates=['date']
    )
    df = df.set_index('date')
    df.columns = [series_id]
    return df


def fetch_btc():
    print("Fetching BTC-USD from yfinance...")
    btc = yf.download('BTC-USD', start='2014-01-01', end='2026-02-13', progress=False)
    if isinstance(btc.columns, pd.MultiIndex):
        btc = btc.droplevel(1, axis=1)
    btc = btc[['Close']].rename(columns={'Close': 'BTC'})
    btc.index = pd.to_datetime(btc.index).tz_localize(None)
    print(f"  BTC: {len(btc)} obs, {btc.index.min().date()} to {btc.index.max().date()}")
    return btc


def fetch_stablecoins_defillama():
    """Fetch USDT + USDC history from DefiLlama (free, no auth)."""
    print("Fetching stablecoins from DefiLlama...")

    stables = {'1': 'USDT', '2': 'USDC'}
    all_dfs = []

    for sid, label in stables.items():
        try:
            resp = requests.get(f'https://stablecoins.llama.fi/stablecoin/{sid}', timeout=30)
            data = resp.json()
            tokens = data.get('tokens', [])

            rows = []
            for t in tokens:
                date = pd.Timestamp(t['date'], unit='s')
                mcap = t.get('circulating', {}).get('peggedUSD', None)
                if mcap is not None and mcap > 0:
                    rows.append({'date': date, label: mcap})

            df = pd.DataFrame(rows).set_index('date')
            df.index = df.index.normalize()
            # Remove duplicates keeping last
            df = df[~df.index.duplicated(keep='last')]
            all_dfs.append(df)
            print(f"  {label}: {len(df)} obs, {df.index.min().date()} to {df.index.max().date()}")
            time.sleep(1)
        except Exception as e:
            print(f"  {label} FAILED: {e}")

    if not all_dfs:
        return None

    combined = pd.concat(all_dfs, axis=1)
    combined['STABLE_TOTAL'] = combined.sum(axis=1)
    return combined


def fetch_iorb(api_key):
    """Combine IOER (pre-2021) and IORB (post-2021) from FRED."""
    print("Fetching IORB/IOER from FRED...")
    dfs = []
    for series_id in ['IORB', 'IOER']:
        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
            'series_id': series_id, 'api_key': api_key,
            'file_type': 'json', 'observation_start': '2014-01-01',
        }
        try:
            resp = requests.get(url, params=params, timeout=30)
            data = resp.json()
            if 'observations' in data and len(data['observations']) > 0:
                df = pd.DataFrame(data['observations'])
                df['date'] = pd.to_datetime(df['date'])
                df['value'] = pd.to_numeric(df['value'], errors='coerce')
                df = df.dropna(subset=['value']).set_index('date')[['value']]
                df.columns = [series_id]
                dfs.append(df)
                print(f"  {series_id}: {len(df)} obs")
                time.sleep(1)
        except Exception as e:
            print(f"  {series_id} failed: {e}")

    if not dfs:
        return None
    combined = pd.concat(dfs, axis=1)
    if 'IORB' in combined.columns and 'IOER' in combined.columns:
        combined['IORB_RATE'] = combined['IORB'].fillna(combined['IOER'])
    elif 'IORB' in combined.columns:
        combined['IORB_RATE'] = combined['IORB']
    else:
        combined['IORB_RATE'] = combined['IOER']
    return combined[['IORB_RATE']]


# ============================================================
# COMPONENT CONSTRUCTION
# ============================================================

def zscore_rolling(series, window=504, min_periods=126):
    mean = series.rolling(window, min_periods=min_periods).mean()
    std = series.rolling(window, min_periods=min_periods).std()
    return (series - mean) / std.replace(0, np.nan)


def build_all_components(conn, btc, stablecoins, iorb):
    """Build all candidate components."""

    m2 = load_series(conn, 'M2SL')
    walcl = load_series(conn, 'WALCL')
    tga = load_series(conn, 'WTREGEN')
    rrp = load_series(conn, 'RRPONTSYD')
    hy_oas = load_series(conn, 'BAMLH0A0HYM2')
    dollar = load_series(conn, 'DTWEXBGS')
    sofr = load_series(conn, 'NYFED_SOFR')

    print("\nBuilding components...")

    components = pd.DataFrame(index=btc.index)
    components['BTC'] = btc['BTC']

    # --- C1: M2 Momentum (3-month annualized RoC) ---
    m2_d = m2.resample('D').ffill()
    components['C1_M2_Mom'] = m2_d['M2SL'].pct_change(63) * 4
    print(f"  C1 M2 Momentum: {components['C1_M2_Mom'].dropna().shape[0]} obs")

    # --- C2: Dollar Inverted (20-day RoC) ---
    components['C2_Dollar_Inv'] = -dollar['DTWEXBGS'].pct_change(20)
    print(f"  C2 Dollar Inv: {components['C2_Dollar_Inv'].dropna().shape[0]} obs")

    # --- C3: Net Liquidity Impulse (4-week RoC) ---
    walcl_d = walcl.resample('D').ffill()
    tga_d = tga.resample('D').ffill()
    rrp_d = rrp.resample('D').ffill()
    net_liq = walcl_d['WALCL'] - tga_d['WTREGEN'] - rrp_d['RRPONTSYD']
    components['C3_NetLiq'] = net_liq.pct_change(20)
    print(f"  C3 Net Liq Impulse: {components['C3_NetLiq'].dropna().shape[0]} obs")

    # --- C4a: SOFR-IORB Spread (inverted, stress = negative) ---
    if iorb is not None:
        merged = pd.merge(sofr, iorb, left_index=True, right_index=True, how='inner')
        sofr_spread = merged['NYFED_SOFR'] - merged['IORB_RATE']
        components['C4a_SOFR_Spread'] = -sofr_spread  # Inverted
        print(f"  C4a SOFR-IORB Spread: {components['C4a_SOFR_Spread'].dropna().shape[0]} obs")

    # --- C4b: HY OAS (inverted, wide spreads = negative) ---
    components['C4b_HY_OAS_Inv'] = -hy_oas['BAMLH0A0HYM2']
    print(f"  C4b HY OAS Inv: {components['C4b_HY_OAS_Inv'].dropna().shape[0]} obs")

    # --- C4: Combined Funding Stress (SOFR spread + HY OAS) ---
    if 'C4a_SOFR_Spread' in components.columns:
        c4a_z = zscore_rolling(components['C4a_SOFR_Spread'])
        c4b_z = zscore_rolling(components['C4b_HY_OAS_Inv'])
        components['C4_Funding'] = 0.5 * c4a_z + 0.5 * c4b_z
    else:
        components['C4_Funding'] = zscore_rolling(components['C4b_HY_OAS_Inv'])
    print(f"  C4 Funding Combined: {components['C4_Funding'].dropna().shape[0]} obs")

    # --- C5: Stablecoin Supply Momentum (30-day RoC) ---
    if stablecoins is not None and 'STABLE_TOTAL' in stablecoins.columns:
        components['C5_Stable_Mom'] = stablecoins['STABLE_TOTAL'].pct_change(30)
        print(f"  C5 Stablecoin Mom: {components['C5_Stable_Mom'].dropna().shape[0]} obs")

    # --- C6: Net Liquidity Level Z-Score (not impulse, but level) ---
    components['C6_NetLiq_Level'] = net_liq
    print(f"  C6 Net Liq Level: {components['C6_NetLiq_Level'].dropna().shape[0]} obs")

    # --- C7: M2 YoY (simpler than 3-month annualized) ---
    components['C7_M2_YoY'] = m2_d['M2SL'].pct_change(252)
    print(f"  C7 M2 YoY: {components['C7_M2_YoY'].dropna().shape[0]} obs")

    # --- C8: Dollar YoY inverted ---
    components['C8_Dollar_YoY_Inv'] = -dollar['DTWEXBGS'].pct_change(252)
    print(f"  C8 Dollar YoY Inv: {components['C8_Dollar_YoY_Inv'].dropna().shape[0]} obs")

    # --- C9: Stablecoin 7-day momentum (faster signal) ---
    if stablecoins is not None and 'STABLE_TOTAL' in stablecoins.columns:
        components['C9_Stable_7d'] = stablecoins['STABLE_TOTAL'].pct_change(7)
        print(f"  C9 Stablecoin 7d: {components['C9_Stable_7d'].dropna().shape[0]} obs")

    # --- C10: RRP level (inverted - lower RRP = less buffer = negative) ---
    components['C10_RRP'] = rrp_d['RRPONTSYD']
    print(f"  C10 RRP Level: {components['C10_RRP'].dropna().shape[0]} obs")

    return components


# ============================================================
# COMPOSITE CONSTRUCTION & TESTING
# ============================================================

def compute_composite(df, component_weights):
    """Compute a weighted composite from z-scored components."""
    z_scores = {}
    for col in component_weights:
        if col in df.columns:
            z_scores[col] = zscore_rolling(df[col])

    composite = pd.Series(0.0, index=df.index)
    total_weight = 0
    for col, w in component_weights.items():
        if col in z_scores:
            composite += w * z_scores[col]
            total_weight += w

    # Normalize if weights don't sum to 1
    if total_weight > 0 and abs(total_weight - 1.0) > 0.01:
        composite /= total_weight

    return composite


def forward_returns(prices, horizons=[5, 10, 21, 42, 63]):
    fwd = pd.DataFrame(index=prices.index)
    for h in horizons:
        fwd[f'fwd_{h}d'] = prices.shift(-h) / prices - 1
    return fwd


def test_composite(composite, fwd, label="", verbose=True):
    """Run full test suite on a composite. Returns summary dict."""
    results = {}

    for horizon_col in ['fwd_5d', 'fwd_10d', 'fwd_21d', 'fwd_42d', 'fwd_63d']:
        df = pd.DataFrame({'comp': composite, 'fwd': fwd[horizon_col]}).dropna()
        if len(df) < 100:
            continue

        # Quintile analysis
        df['q'] = pd.qcut(df['comp'], 5, labels=['Q1', 'Q2', 'Q3', 'Q4', 'Q5'])
        q_means = df.groupby('q')['fwd'].mean() * 100

        q5 = df[df['q'] == 'Q5']['fwd']
        q1 = df[df['q'] == 'Q1']['fwd']
        t_stat, p_val = stats.ttest_ind(q5, q1, equal_var=False)
        spread = (q5.mean() - q1.mean()) * 100

        # Monotonicity check
        vals = q_means.values
        is_monotonic = all(vals[i] <= vals[i+1] for i in range(len(vals)-1))

        # Regime analysis
        contracting = df[df['comp'] < -0.5]['fwd']
        expanding = df[df['comp'] > 0.5]['fwd']
        if len(contracting) > 10 and len(expanding) > 10:
            regime_spread = (expanding.mean() - contracting.mean()) * 100
            r_t, r_p = stats.ttest_ind(expanding, contracting, equal_var=False)
        else:
            regime_spread, r_t, r_p = np.nan, np.nan, np.nan

        # Correlation
        corr = df['comp'].corr(df['fwd'])

        results[horizon_col] = {
            'n': len(df),
            'spread': spread,
            't_stat': t_stat,
            'p_val': p_val,
            'monotonic': is_monotonic,
            'q_means': q_means.to_dict(),
            'regime_spread': regime_spread,
            'regime_t': r_t,
            'regime_p': r_p,
            'corr': corr,
        }

    if verbose and results:
        print(f"\n  {label}")
        print(f"  {'─'*65}")
        print(f"  {'Horizon':<12} {'Q5-Q1':>8} {'t-stat':>8} {'p-val':>10} {'Mono':>6} {'Regime':>8} {'Corr':>6}")
        print(f"  {'─'*65}")
        for h, r in results.items():
            h_label = h.replace('fwd_', '').replace('d', 'D')
            mono = '✓' if r['monotonic'] else '✗'
            sig = '***' if r['p_val'] < 0.001 else ('**' if r['p_val'] < 0.01 else ('*' if r['p_val'] < 0.05 else ''))
            regime = f"{r['regime_spread']:+.1f}%" if not np.isnan(r['regime_spread']) else 'N/A'
            print(f"  {h_label:<12} {r['spread']:+7.2f}% {r['t_stat']:>7.2f}  {r['p_val']:>9.6f}{sig:<3} {mono:>5} {regime:>8} {r['corr']:+.3f}")
        print(f"  {'─'*65}")
        # Print quintile detail for 21d
        if 'fwd_21d' in results:
            qm = results['fwd_21d']['q_means']
            print(f"  21D quintiles: Q1={qm.get('Q1',0):+.1f}%  Q2={qm.get('Q2',0):+.1f}%  Q3={qm.get('Q3',0):+.1f}%  Q4={qm.get('Q4',0):+.1f}%  Q5={qm.get('Q5',0):+.1f}%")

    return results


def score_composite(results):
    """Score a composite for optimization. Higher = better."""
    if not results:
        return -999

    score = 0
    for h, r in results.items():
        # Reward: spread magnitude * significance
        if r['p_val'] < 0.05:
            score += abs(r['spread']) * (1 / max(r['p_val'], 1e-10)) * 0.0001
        # Reward monotonicity
        if r['monotonic']:
            score += 10
        # Reward regime spread
        if not np.isnan(r['regime_spread']):
            score += abs(r['regime_spread']) * 0.5
        # Reward correlation
        score += abs(r['corr']) * 5

    return score


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 70)
    print("  CLTI BACKTEST v2: Iterative Optimization")
    print("  Lighthouse Macro | 2026-02-12")
    print("=" * 70)

    import sys
    sys.path.insert(0, '/Users/bob/LHM/Scripts/data_pipeline/lighthouse')
    from config import API_KEYS
    fred_key = API_KEYS.get('FRED', '')

    conn = sqlite3.connect(DB_PATH)

    # Fetch data
    btc = fetch_btc()
    stablecoins = fetch_stablecoins_defillama()
    iorb = fetch_iorb(fred_key) if fred_key else None

    # Build all candidate components
    components = build_all_components(conn, btc, stablecoins, iorb)

    # Forward returns
    fwd = forward_returns(components['BTC'].dropna())

    print(f"\n{'='*70}")
    print(f"  DATA SUMMARY")
    print(f"{'='*70}")
    for col in components.columns:
        if col == 'BTC':
            continue
        valid = components[col].dropna()
        if len(valid) > 0:
            print(f"  {col:25s}: {len(valid):5d} obs  ({valid.index.min().date()} to {valid.index.max().date()})")

    # ========================================================
    # TEST 1: Individual Components
    # ========================================================
    print(f"\n\n{'#'*70}")
    print(f"  PHASE 1: INDIVIDUAL COMPONENT TESTS (z-scored)")
    print(f"{'#'*70}")

    individual_cols = [
        'C1_M2_Mom', 'C2_Dollar_Inv', 'C3_NetLiq', 'C4_Funding',
        'C5_Stable_Mom', 'C4a_SOFR_Spread', 'C4b_HY_OAS_Inv',
        'C7_M2_YoY', 'C8_Dollar_YoY_Inv', 'C9_Stable_7d',
    ]

    individual_results = {}
    for col in individual_cols:
        if col in components.columns and components[col].dropna().shape[0] > 200:
            z = zscore_rolling(components[col])
            res = test_composite(z, fwd, label=col, verbose=True)
            individual_results[col] = res

    # ========================================================
    # TEST 2: Weight Configurations
    # ========================================================
    print(f"\n\n{'#'*70}")
    print(f"  PHASE 2: COMPOSITE WEIGHT CONFIGURATIONS")
    print(f"{'#'*70}")

    configs = {
        'V1_Equal': {
            'C1_M2_Mom': 0.20, 'C2_Dollar_Inv': 0.20,
            'C3_NetLiq': 0.20, 'C4_Funding': 0.20,
            'C5_Stable_Mom': 0.20,
        },
        'V2_Macro_Heavy': {
            'C1_M2_Mom': 0.30, 'C2_Dollar_Inv': 0.25,
            'C3_NetLiq': 0.15, 'C4_Funding': 0.10,
            'C5_Stable_Mom': 0.20,
        },
        'V3_Plumbing_Heavy': {
            'C1_M2_Mom': 0.15, 'C2_Dollar_Inv': 0.15,
            'C3_NetLiq': 0.25, 'C4_Funding': 0.25,
            'C5_Stable_Mom': 0.20,
        },
        'V4_Crypto_Heavy': {
            'C1_M2_Mom': 0.15, 'C2_Dollar_Inv': 0.15,
            'C3_NetLiq': 0.15, 'C4_Funding': 0.15,
            'C5_Stable_Mom': 0.40,
        },
        'V5_Research_Spec': {
            'C1_M2_Mom': 0.20, 'C2_Dollar_Inv': 0.20,
            'C3_NetLiq': 0.15, 'C4_Funding': 0.15,
            'C5_Stable_Mom': 0.30,
        },
        'V6_Dollar_Stable': {
            'C2_Dollar_Inv': 0.30, 'C4_Funding': 0.30,
            'C5_Stable_Mom': 0.40,
        },
        'V7_No_M2': {
            'C2_Dollar_Inv': 0.25, 'C3_NetLiq': 0.20,
            'C4_Funding': 0.25, 'C5_Stable_Mom': 0.30,
        },
        'V8_YoY_Macro': {
            'C7_M2_YoY': 0.25, 'C8_Dollar_YoY_Inv': 0.25,
            'C3_NetLiq': 0.15, 'C4_Funding': 0.15,
            'C5_Stable_Mom': 0.20,
        },
        'V9_Fast_Stable': {
            'C2_Dollar_Inv': 0.20, 'C4_Funding': 0.30,
            'C9_Stable_7d': 0.50,
        },
        'V10_Funding_Only': {
            'C4a_SOFR_Spread': 0.50, 'C4b_HY_OAS_Inv': 0.50,
        },
        'V11_HY_Stable': {
            'C4b_HY_OAS_Inv': 0.40, 'C5_Stable_Mom': 0.60,
        },
        'V12_Kitchen_Sink': {
            'C1_M2_Mom': 0.10, 'C2_Dollar_Inv': 0.15,
            'C3_NetLiq': 0.10, 'C4a_SOFR_Spread': 0.10,
            'C4b_HY_OAS_Inv': 0.15, 'C5_Stable_Mom': 0.25,
            'C9_Stable_7d': 0.15,
        },
        'V13_Macro_Funding': {
            'C1_M2_Mom': 0.25, 'C2_Dollar_Inv': 0.25,
            'C4_Funding': 0.50,
        },
        'V14_Three_Pillars': {
            'C2_Dollar_Inv': 0.33, 'C4_Funding': 0.34,
            'C5_Stable_Mom': 0.33,
        },
        'V15_Stable_Dominant': {
            'C4_Funding': 0.20, 'C5_Stable_Mom': 0.50,
            'C2_Dollar_Inv': 0.30,
        },
    }

    config_scores = {}
    config_results = {}

    for name, weights in configs.items():
        # Check all components exist
        available = all(
            c in components.columns and components[c].dropna().shape[0] > 200
            for c in weights
        )
        if not available:
            print(f"\n  {name}: SKIPPED (missing components)")
            continue

        comp = compute_composite(components, weights)
        res = test_composite(comp, fwd, label=name, verbose=True)
        scr = score_composite(res)
        config_scores[name] = scr
        config_results[name] = res

    # ========================================================
    # RANK CONFIGURATIONS
    # ========================================================
    print(f"\n\n{'#'*70}")
    print(f"  PHASE 3: CONFIGURATION RANKINGS")
    print(f"{'#'*70}")

    ranked = sorted(config_scores.items(), key=lambda x: -x[1])
    print(f"\n  {'Rank':<6} {'Config':<25} {'Score':>8} {'21D Spread':>12} {'21D Mono':>10} {'63D Spread':>12}")
    print(f"  {'─'*75}")
    for i, (name, scr) in enumerate(ranked, 1):
        r = config_results[name]
        s21 = r.get('fwd_21d', {}).get('spread', 0)
        m21 = '✓' if r.get('fwd_21d', {}).get('monotonic', False) else '✗'
        s63 = r.get('fwd_63d', {}).get('spread', 0)
        print(f"  {i:<6} {name:<25} {scr:>8.1f} {s21:>+11.2f}% {m21:>9} {s63:>+11.2f}%")

    # ========================================================
    # DETAILED RESULTS: TOP 3
    # ========================================================
    print(f"\n\n{'#'*70}")
    print(f"  PHASE 4: TOP 3 DETAILED ANALYSIS")
    print(f"{'#'*70}")

    for i, (name, _) in enumerate(ranked[:3], 1):
        print(f"\n  === #{i}: {name} ===")
        weights = configs[name]
        print(f"  Weights: {weights}")

        comp = compute_composite(components, weights)
        valid = comp.dropna()
        print(f"  Obs: {len(valid)}, Range: {valid.index.min().date()} to {valid.index.max().date()}")
        print(f"  Current: {valid.iloc[-1]:.3f}")

        # Full quintile detail
        for horizon in ['fwd_21d', 'fwd_63d']:
            df_test = pd.DataFrame({'comp': comp, 'fwd': fwd[horizon]}).dropna()
            if len(df_test) < 100:
                continue

            df_test['q'] = pd.qcut(df_test['comp'], 5, labels=['Q1', 'Q2', 'Q3', 'Q4', 'Q5'])

            h_label = horizon.replace('fwd_', '').replace('d', '-day')
            print(f"\n  {h_label} Forward Returns by Quintile:")
            for q_label in ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']:
                subset = df_test[df_test['q'] == q_label]['fwd']
                print(f"    {q_label}: {subset.mean()*100:+7.2f}%  (std={subset.std()*100:.1f}%, n={len(subset)})")

            # Regime
            for regime_label, mask in [
                ('Contracting (<-0.5)', df_test['comp'] < -0.5),
                ('Neutral', (df_test['comp'] >= -0.5) & (df_test['comp'] <= 0.5)),
                ('Expanding (>+0.5)', df_test['comp'] > 0.5),
            ]:
                subset = df_test[mask]['fwd']
                if len(subset) > 5:
                    print(f"    {regime_label}: {subset.mean()*100:+7.2f}%  (n={len(subset)})")

        # Extreme deciles
        df_test = pd.DataFrame({'comp': comp, 'fwd': fwd['fwd_21d']}).dropna()
        if len(df_test) > 100:
            p10 = df_test['comp'].quantile(0.10)
            p90 = df_test['comp'].quantile(0.90)
            bottom = df_test[df_test['comp'] <= p10]['fwd']
            top = df_test[df_test['comp'] >= p90]['fwd']
            t_s, p_v = stats.ttest_ind(top, bottom, equal_var=False)
            print(f"\n  Extreme Decile (21D): Bottom 10% = {bottom.mean()*100:+.2f}%, Top 10% = {top.mean()*100:+.2f}%")
            print(f"    Spread: {(top.mean()-bottom.mean())*100:+.2f}%, t={t_s:.2f}, p={p_v:.6f}")

    conn.close()

    print(f"\n\n{'='*70}")
    print(f"  BACKTEST v2 COMPLETE")
    print(f"{'='*70}")


if __name__ == '__main__':
    main()
