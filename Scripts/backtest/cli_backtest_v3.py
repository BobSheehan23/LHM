"""
CLI Backtest v3: Fix SOFR inversion, test Dollar YoY, iterate to monotonic
============================================================================
Key changes from v2:
  - Drop C4a (SOFR-IORB spread) - working backwards, poisoning composite
  - Test Dollar YoY (C8) vs Dollar 20D (C2) - YoY dramatically stronger
  - Focus on strongest individual components: Dollar YoY, Stablecoin 30D, HY OAS
  - Test SOFR as contrarian (inverted sign) separately
  - Grid search weights for monotonicity

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
from itertools import product
warnings.filterwarnings('ignore')

DB_PATH = '/Users/bob/LHM/Data/databases/Lighthouse_Master.db'


def load_series(conn, series_id):
    df = pd.read_sql(
        "SELECT date, value FROM observations WHERE series_id = ? ORDER BY date",
        conn, params=(series_id,), parse_dates=['date']
    )
    return df.set_index('date').rename(columns={'value': series_id})


def fetch_btc():
    print("Fetching BTC-USD...")
    btc = yf.download('BTC-USD', start='2014-01-01', end='2026-02-13', progress=False)
    if isinstance(btc.columns, pd.MultiIndex):
        btc = btc.droplevel(1, axis=1)
    btc = btc[['Close']].rename(columns={'Close': 'BTC'})
    btc.index = pd.to_datetime(btc.index).tz_localize(None)
    print(f"  {len(btc)} obs, {btc.index.min().date()} to {btc.index.max().date()}")
    return btc


def fetch_stablecoins():
    print("Fetching stablecoins from DefiLlama...")
    stables = {'1': 'USDT', '2': 'USDC'}
    all_dfs = []
    for sid, label in stables.items():
        try:
            resp = requests.get(f'https://stablecoins.llama.fi/stablecoin/{sid}', timeout=30)
            data = resp.json()
            rows = []
            for t in data.get('tokens', []):
                mcap = t.get('circulating', {}).get('peggedUSD', None)
                if mcap and mcap > 0:
                    rows.append({'date': pd.Timestamp(t['date'], unit='s').normalize(), label: mcap})
            df = pd.DataFrame(rows).set_index('date')
            df = df[~df.index.duplicated(keep='last')]
            all_dfs.append(df)
            print(f"  {label}: {len(df)} obs")
            time.sleep(1)
        except Exception as e:
            print(f"  {label} FAILED: {e}")
    combined = pd.concat(all_dfs, axis=1)
    combined['STABLE_TOTAL'] = combined.sum(axis=1)
    return combined


def zscore_rolling(series, window=504, min_periods=126):
    mean = series.rolling(window, min_periods=min_periods).mean()
    std = series.rolling(window, min_periods=min_periods).std()
    return (series - mean) / std.replace(0, np.nan)


def forward_returns(prices, horizons=[5, 10, 21, 42, 63]):
    fwd = pd.DataFrame(index=prices.index)
    for h in horizons:
        fwd[f'fwd_{h}d'] = prices.shift(-h) / prices - 1
    return fwd


def test_composite(composite, fwd, label="", verbose=True):
    results = {}
    for hcol in ['fwd_5d', 'fwd_10d', 'fwd_21d', 'fwd_42d', 'fwd_63d']:
        df = pd.DataFrame({'comp': composite, 'fwd': fwd[hcol]}).dropna()
        if len(df) < 100:
            continue

        df['q'] = pd.qcut(df['comp'], 5, labels=['Q1', 'Q2', 'Q3', 'Q4', 'Q5'])
        q_means = df.groupby('q')['fwd'].mean() * 100

        q5 = df[df['q'] == 'Q5']['fwd']
        q1 = df[df['q'] == 'Q1']['fwd']
        t_stat, p_val = stats.ttest_ind(q5, q1, equal_var=False)
        spread = (q5.mean() - q1.mean()) * 100

        vals = q_means.values
        is_monotonic = all(vals[i] <= vals[i + 1] for i in range(len(vals) - 1))

        # Near-monotonic: allow one violation of <= 1%
        violations = sum(1 for i in range(len(vals) - 1) if vals[i] > vals[i + 1])
        max_violation = max((vals[i] - vals[i + 1] for i in range(len(vals) - 1) if vals[i] > vals[i + 1]), default=0)
        near_monotonic = violations <= 1 and max_violation < 1.5

        # Regime
        contr = df[df['comp'] < -0.5]['fwd']
        expan = df[df['comp'] > 0.5]['fwd']
        if len(contr) > 10 and len(expan) > 10:
            regime_spread = (expan.mean() - contr.mean()) * 100
            r_t, r_p = stats.ttest_ind(expan, contr, equal_var=False)
        else:
            regime_spread, r_t, r_p = np.nan, np.nan, np.nan

        corr = df['comp'].corr(df['fwd'])

        results[hcol] = {
            'n': len(df), 'spread': spread, 't_stat': t_stat, 'p_val': p_val,
            'monotonic': is_monotonic, 'near_monotonic': near_monotonic,
            'q_means': q_means.to_dict(), 'regime_spread': regime_spread,
            'regime_t': r_t, 'regime_p': r_p, 'corr': corr,
            'violations': violations, 'max_violation': max_violation,
        }

    if verbose and results:
        print(f"\n  {label}")
        print(f"  {'─' * 72}")
        print(f"  {'Horizon':<8} {'Q5-Q1':>8} {'t':>7} {'p':>10} {'Mono':>5} {'Near':>5} {'Regime':>8} {'Corr':>6}  Quintiles")
        print(f"  {'─' * 72}")
        for h, r in results.items():
            hl = h.replace('fwd_', '').replace('d', 'D')
            sig = '***' if r['p_val'] < 0.001 else ('**' if r['p_val'] < 0.01 else ('*' if r['p_val'] < 0.05 else ''))
            mono = '✓' if r['monotonic'] else '✗'
            near = '~' if r['near_monotonic'] and not r['monotonic'] else (' ' if not r['near_monotonic'] else '✓')
            regime = f"{r['regime_spread']:+.1f}%" if not np.isnan(r['regime_spread']) else 'N/A'
            qm = r['q_means']
            qs = f"Q1={qm.get('Q1', 0):+.1f} Q2={qm.get('Q2', 0):+.1f} Q3={qm.get('Q3', 0):+.1f} Q4={qm.get('Q4', 0):+.1f} Q5={qm.get('Q5', 0):+.1f}"
            print(f"  {hl:<8} {r['spread']:+7.1f}% {r['t_stat']:>6.1f} {r['p_val']:>9.6f}{sig:<3} {mono:>4} {near:>4} {regime:>8} {r['corr']:+.3f}  {qs}")
        print(f"  {'─' * 72}")

    return results


def main():
    print("=" * 70)
    print("  CLI BACKTEST v3: Fixing SOFR, Optimizing Weights")
    print("  Lighthouse Macro | 2026-02-12")
    print("=" * 70)

    import sys
    sys.path.insert(0, '/Users/bob/LHM/Scripts/data_pipeline/lighthouse')
    from config import API_KEYS
    fred_key = API_KEYS.get('FRED', '')

    conn = sqlite3.connect(DB_PATH)

    btc = fetch_btc()
    stablecoins = fetch_stablecoins()

    # Fetch IORB for SOFR contrarian test
    print("Fetching IORB/IOER...")
    iorb_dfs = []
    for sid in ['IORB', 'IOER']:
        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {'series_id': sid, 'api_key': fred_key, 'file_type': 'json', 'observation_start': '2014-01-01'}
        try:
            resp = requests.get(url, params=params, timeout=30)
            data = resp.json()
            if 'observations' in data:
                df = pd.DataFrame(data['observations'])
                df['date'] = pd.to_datetime(df['date'])
                df['value'] = pd.to_numeric(df['value'], errors='coerce')
                df = df.dropna(subset=['value']).set_index('date')[['value']].rename(columns={'value': sid})
                iorb_dfs.append(df)
                print(f"  {sid}: {len(df)} obs")
            time.sleep(1)
        except:
            pass

    iorb = pd.concat(iorb_dfs, axis=1) if iorb_dfs else None
    if iorb is not None:
        if 'IORB' in iorb.columns and 'IOER' in iorb.columns:
            iorb['IORB_RATE'] = iorb['IORB'].fillna(iorb['IOER'])
        elif 'IORB' in iorb.columns:
            iorb['IORB_RATE'] = iorb['IORB']
        else:
            iorb['IORB_RATE'] = iorb['IOER']

    # Load from DB
    m2 = load_series(conn, 'M2SL').resample('D').ffill()
    walcl = load_series(conn, 'WALCL').resample('D').ffill()
    tga = load_series(conn, 'WTREGEN').resample('D').ffill()
    rrp = load_series(conn, 'RRPONTSYD').resample('D').ffill()
    hy_oas = load_series(conn, 'BAMLH0A0HYM2')
    dollar = load_series(conn, 'DTWEXBGS')
    sofr = load_series(conn, 'NYFED_SOFR')

    print("\nBuilding components...")
    comp = pd.DataFrame(index=btc.index)
    comp['BTC'] = btc['BTC']

    # Core components (based on v2 individual results)
    comp['DollarYoY'] = -dollar['DTWEXBGS'].pct_change(252)  # BEST individual: +7.55% 21D spread
    comp['Dollar20d'] = -dollar['DTWEXBGS'].pct_change(20)
    comp['Dollar63d'] = -dollar['DTWEXBGS'].pct_change(63)

    comp['Stable30d'] = stablecoins['STABLE_TOTAL'].pct_change(30)  # 2nd best: +5.02%
    comp['Stable14d'] = stablecoins['STABLE_TOTAL'].pct_change(14)
    comp['Stable7d'] = stablecoins['STABLE_TOTAL'].pct_change(7)

    comp['HY_OAS_Inv'] = -hy_oas['BAMLH0A0HYM2']  # 3rd best: +3.57%

    comp['M2_3m'] = m2['M2SL'].pct_change(63) * 4
    comp['M2_YoY'] = m2['M2SL'].pct_change(252)

    net_liq = walcl['WALCL'] - tga['WTREGEN'] - rrp['RRPONTSYD']
    comp['NetLiq_4w'] = net_liq.pct_change(20)
    comp['NetLiq_13w'] = net_liq.pct_change(63)

    # SOFR spread - test as CONTRARIAN (stress at bottoms = future rally)
    if iorb is not None:
        merged = pd.merge(sofr, iorb[['IORB_RATE']], left_index=True, right_index=True, how='inner')
        sofr_spread = merged['NYFED_SOFR'] - merged['IORB_RATE']
        # CONTRARIAN: higher spread (more stress) = positive signal (buying at stress)
        comp['SOFR_Contrarian'] = sofr_spread
        print("  SOFR spread: contrarian (stress = buy signal)")

    fwd = forward_returns(comp['BTC'].dropna())

    # ================================================================
    # PHASE 1: Test individual components with different lookbacks
    # ================================================================
    print(f"\n{'#' * 70}")
    print(f"  PHASE 1: COMPONENT VARIANTS")
    print(f"{'#' * 70}")

    test_cols = [
        'DollarYoY', 'Dollar63d', 'Dollar20d',
        'Stable30d', 'Stable14d', 'Stable7d',
        'HY_OAS_Inv', 'M2_3m', 'M2_YoY',
        'NetLiq_4w', 'NetLiq_13w',
    ]
    if 'SOFR_Contrarian' in comp.columns:
        test_cols.append('SOFR_Contrarian')

    for col in test_cols:
        if col in comp.columns and comp[col].dropna().shape[0] > 200:
            z = zscore_rolling(comp[col])
            test_composite(z, fwd, label=col, verbose=True)

    # ================================================================
    # PHASE 2: Focused composite configurations
    # ================================================================
    print(f"\n\n{'#' * 70}")
    print(f"  PHASE 2: FOCUSED COMPOSITES (No SOFR, Fixed Dollar)")
    print(f"{'#' * 70}")

    configs = {
        # Core 3: Dollar YoY + Stable 30d + HY OAS (the 3 strongest)
        'A1_Core3_Equal': {
            'DollarYoY': 0.33, 'Stable30d': 0.34, 'HY_OAS_Inv': 0.33,
        },
        'A2_Core3_Dollar_Heavy': {
            'DollarYoY': 0.50, 'Stable30d': 0.25, 'HY_OAS_Inv': 0.25,
        },
        'A3_Core3_Stable_Heavy': {
            'DollarYoY': 0.25, 'Stable30d': 0.50, 'HY_OAS_Inv': 0.25,
        },
        'A4_Core3_HY_Heavy': {
            'DollarYoY': 0.25, 'Stable30d': 0.25, 'HY_OAS_Inv': 0.50,
        },

        # Core 3 + M2
        'B1_Core3_M2_3m': {
            'DollarYoY': 0.25, 'Stable30d': 0.25, 'HY_OAS_Inv': 0.25, 'M2_3m': 0.25,
        },
        'B2_Core3_M2_YoY': {
            'DollarYoY': 0.25, 'Stable30d': 0.25, 'HY_OAS_Inv': 0.25, 'M2_YoY': 0.25,
        },

        # Core 3 + NetLiq
        'C1_Core3_NetLiq4w': {
            'DollarYoY': 0.25, 'Stable30d': 0.25, 'HY_OAS_Inv': 0.25, 'NetLiq_4w': 0.25,
        },
        'C2_Core3_NetLiq13w': {
            'DollarYoY': 0.25, 'Stable30d': 0.25, 'HY_OAS_Inv': 0.25, 'NetLiq_13w': 0.25,
        },

        # Core 3 + M2 + NetLiq (5-component)
        'D1_Full5_Equal': {
            'DollarYoY': 0.20, 'Stable30d': 0.20, 'HY_OAS_Inv': 0.20,
            'M2_3m': 0.20, 'NetLiq_4w': 0.20,
        },
        'D2_Full5_Weighted': {
            'DollarYoY': 0.30, 'Stable30d': 0.25, 'HY_OAS_Inv': 0.20,
            'M2_3m': 0.10, 'NetLiq_4w': 0.15,
        },
        'D3_Full5_TopHeavy': {
            'DollarYoY': 0.35, 'Stable30d': 0.30, 'HY_OAS_Inv': 0.15,
            'M2_3m': 0.10, 'NetLiq_4w': 0.10,
        },

        # Dollar 63d instead of YoY
        'E1_Dollar63d_Core': {
            'Dollar63d': 0.33, 'Stable30d': 0.34, 'HY_OAS_Inv': 0.33,
        },
        'E2_Dollar63d_Full': {
            'Dollar63d': 0.25, 'Stable30d': 0.25, 'HY_OAS_Inv': 0.25,
            'M2_3m': 0.15, 'NetLiq_4w': 0.10,
        },

        # Stable 14d instead of 30d
        'F1_Stable14d_Core': {
            'DollarYoY': 0.33, 'Stable14d': 0.34, 'HY_OAS_Inv': 0.33,
        },

        # SOFR as contrarian addition
        'G1_Core3_SOFR_Contr': {
            'DollarYoY': 0.25, 'Stable30d': 0.25, 'HY_OAS_Inv': 0.25,
            'SOFR_Contrarian': 0.25,
        },

        # 2-component (just the top 2)
        'H1_Dollar_Stable_Only': {
            'DollarYoY': 0.50, 'Stable30d': 0.50,
        },
        'H2_Dollar_HY_Only': {
            'DollarYoY': 0.50, 'HY_OAS_Inv': 0.50,
        },

        # Net liq 13w heavier (medium-term plumbing)
        'I1_NetLiq13w_Heavy': {
            'DollarYoY': 0.20, 'Stable30d': 0.20, 'HY_OAS_Inv': 0.20,
            'NetLiq_13w': 0.40,
        },
    }

    scores = {}
    all_results = {}

    for name, weights in configs.items():
        available = all(c in comp.columns and comp[c].dropna().shape[0] > 200 for c in weights)
        if not available:
            continue

        z_comps = {c: zscore_rolling(comp[c]) for c in weights}
        composite = sum(w * z_comps[c] for c, w in weights.items())

        res = test_composite(composite, fwd, label=name, verbose=True)
        all_results[name] = res

        # Score: prioritize monotonicity, spread, significance
        score = 0
        for h, r in res.items():
            if r['p_val'] < 0.05:
                score += abs(r['spread'])
            if r['monotonic']:
                score += 50
            elif r['near_monotonic']:
                score += 20
            if not np.isnan(r['regime_spread']):
                score += abs(r['regime_spread']) * 0.3
        scores[name] = score

    # ================================================================
    # PHASE 3: Rankings
    # ================================================================
    print(f"\n\n{'#' * 70}")
    print(f"  PHASE 3: RANKINGS")
    print(f"{'#' * 70}")

    ranked = sorted(scores.items(), key=lambda x: -x[1])

    print(f"\n  {'Rank':<5} {'Config':<25} {'Score':>7}  {'5D':>7} {'10D':>7} {'21D':>7} {'42D':>7} {'63D':>7}  {'MonoCount':>9}")
    print(f"  {'─' * 95}")
    for i, (name, scr) in enumerate(ranked, 1):
        r = all_results[name]
        spreads = []
        mono_count = 0
        for h in ['fwd_5d', 'fwd_10d', 'fwd_21d', 'fwd_42d', 'fwd_63d']:
            if h in r:
                spreads.append(f"{r[h]['spread']:+6.1f}%")
                if r[h]['monotonic']:
                    mono_count += 1
            else:
                spreads.append('  N/A ')
        print(f"  {i:<5} {name:<25} {scr:>7.1f}  {'  '.join(spreads)}  {mono_count}/5")

    # ================================================================
    # PHASE 4: Top 3 Deep Dive
    # ================================================================
    print(f"\n\n{'#' * 70}")
    print(f"  PHASE 4: TOP 3 DEEP DIVE")
    print(f"{'#' * 70}")

    for i, (name, _) in enumerate(ranked[:3], 1):
        weights = configs[name]
        z_comps = {c: zscore_rolling(comp[c]) for c in weights}
        composite = sum(w * z_comps[c] for c, w in weights.items())
        valid = composite.dropna()

        print(f"\n  === #{i}: {name} ===")
        print(f"  Weights: {weights}")
        print(f"  Obs: {len(valid)}, Range: {valid.index.min().date()} to {valid.index.max().date()}")
        print(f"  Current: {valid.iloc[-1]:.3f}")
        print(f"  Mean: {valid.mean():.3f}, Std: {valid.std():.3f}")

        for horizon in ['fwd_21d', 'fwd_63d']:
            df_test = pd.DataFrame({'comp': composite, 'fwd': fwd[horizon]}).dropna()
            if len(df_test) < 100:
                continue

            df_test['q'] = pd.qcut(df_test['comp'], 5, labels=['Q1', 'Q2', 'Q3', 'Q4', 'Q5'])
            hl = horizon.replace('fwd_', '').replace('d', '-day')
            print(f"\n  {hl} Forward Returns:")
            for ql in ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']:
                sub = df_test[df_test['q'] == ql]['fwd']
                print(f"    {ql}: {sub.mean() * 100:+7.2f}%  (std={sub.std() * 100:.1f}%, n={len(sub)}, median={sub.median() * 100:+.1f}%)")

            for lbl, mask in [
                ('Contracting (<-0.5)', df_test['comp'] < -0.5),
                ('Neutral (-0.5 to +0.5)', (df_test['comp'] >= -0.5) & (df_test['comp'] <= 0.5)),
                ('Expanding (>+0.5)', df_test['comp'] > 0.5),
            ]:
                sub = df_test[mask]['fwd']
                if len(sub) > 5:
                    print(f"    {lbl}: {sub.mean() * 100:+7.2f}%  (n={len(sub)})")

            # Tercile analysis (might be cleaner than quintile)
            df_test['tercile'] = pd.qcut(df_test['comp'], 3, labels=['T1_Low', 'T2_Mid', 'T3_High'])
            print(f"\n  {hl} Tercile Analysis:")
            for tl in ['T1_Low', 'T2_Mid', 'T3_High']:
                sub = df_test[df_test['tercile'] == tl]['fwd']
                print(f"    {tl}: {sub.mean() * 100:+7.2f}%  (n={len(sub)})")
            t3 = df_test[df_test['tercile'] == 'T3_High']['fwd']
            t1 = df_test[df_test['tercile'] == 'T1_Low']['fwd']
            t_s, p_v = stats.ttest_ind(t3, t1, equal_var=False)
            print(f"    T3-T1 Spread: {(t3.mean() - t1.mean()) * 100:+.2f}%, t={t_s:.2f}, p={p_v:.6f}")

        # Extreme decile
        df_test = pd.DataFrame({'comp': composite, 'fwd': fwd['fwd_21d']}).dropna()
        if len(df_test) > 100:
            p10 = df_test['comp'].quantile(0.10)
            p90 = df_test['comp'].quantile(0.90)
            bot = df_test[df_test['comp'] <= p10]['fwd']
            top = df_test[df_test['comp'] >= p90]['fwd']
            t_s, p_v = stats.ttest_ind(top, bot, equal_var=False)
            print(f"\n  Extreme Decile (21D): Bot10%={bot.mean() * 100:+.2f}%, Top10%={top.mean() * 100:+.2f}%")
            print(f"    Spread: {(top.mean() - bot.mean()) * 100:+.2f}%, t={t_s:.2f}, p={p_v:.6f}")

        # Win rate by regime
        df_test = pd.DataFrame({'comp': composite, 'fwd': fwd['fwd_21d']}).dropna()
        if len(df_test) > 100:
            print(f"\n  Win Rates (21D positive return):")
            for lbl, mask in [
                ('Contracting (<-0.5)', df_test['comp'] < -0.5),
                ('Neutral', (df_test['comp'] >= -0.5) & (df_test['comp'] <= 0.5)),
                ('Expanding (>+0.5)', df_test['comp'] > 0.5),
            ]:
                sub = df_test[mask]['fwd']
                if len(sub) > 10:
                    wr = (sub > 0).mean() * 100
                    print(f"    {lbl}: {wr:.1f}% win rate (n={len(sub)})")

    # ================================================================
    # PHASE 5: Grid search for optimal weights (top components)
    # ================================================================
    print(f"\n\n{'#' * 70}")
    print(f"  PHASE 5: WEIGHT GRID SEARCH (DollarYoY, Stable30d, HY_OAS_Inv)")
    print(f"{'#' * 70}")

    # Test weight triplets in 5% increments that sum to 1.0
    best_score = -999
    best_weights = None
    best_mono_count = 0
    grid_results = []

    weight_options = [round(x * 0.05, 2) for x in range(1, 19)]  # 0.05 to 0.90

    count = 0
    for w1 in weight_options:
        for w2 in weight_options:
            w3 = round(1.0 - w1 - w2, 2)
            if w3 < 0.05 or w3 > 0.90:
                continue
            count += 1

            weights = {'DollarYoY': w1, 'Stable30d': w2, 'HY_OAS_Inv': w3}
            z_comps = {c: zscore_rolling(comp[c]) for c in weights}
            composite = sum(w * z_comps[c] for c, w in weights.items())

            res = test_composite(composite, fwd, verbose=False)

            mono_count = sum(1 for r in res.values() if r['monotonic'])
            near_mono_count = sum(1 for r in res.values() if r['near_monotonic'])

            score = 0
            for r in res.values():
                if r['p_val'] < 0.05:
                    score += abs(r['spread'])
                if r['monotonic']:
                    score += 50
                elif r['near_monotonic']:
                    score += 20

            grid_results.append({
                'w1': w1, 'w2': w2, 'w3': w3,
                'score': score, 'mono': mono_count, 'near_mono': near_mono_count,
                'spread_21d': res.get('fwd_21d', {}).get('spread', 0),
                'spread_63d': res.get('fwd_63d', {}).get('spread', 0),
                'p_21d': res.get('fwd_21d', {}).get('p_val', 1),
            })

            if mono_count > best_mono_count or (mono_count == best_mono_count and score > best_score):
                best_score = score
                best_weights = weights.copy()
                best_mono_count = mono_count

    print(f"\n  Grid search: {count} weight combinations tested")
    print(f"\n  Best monotonic: {best_weights} (mono={best_mono_count}, score={best_score:.1f})")

    # Show top 10 by score
    grid_df = pd.DataFrame(grid_results).sort_values('score', ascending=False)
    print(f"\n  Top 15 by Score:")
    print(f"  {'Dollar':>8} {'Stable':>8} {'HY':>8} {'Score':>8} {'Mono':>5} {'Near':>5} {'21D Spr':>9} {'63D Spr':>9} {'p(21D)':>10}")
    print(f"  {'─' * 80}")
    for _, row in grid_df.head(15).iterrows():
        print(f"  {row['w1']:>7.0%} {row['w2']:>7.0%} {row['w3']:>7.0%} {row['score']:>8.1f} {int(row['mono']):>5} {int(row['near_mono']):>5} {row['spread_21d']:>+8.1f}% {row['spread_63d']:>+8.1f}% {row['p_21d']:>9.6f}")

    # Show best monotonic results
    mono_df = grid_df[grid_df['mono'] > 0].sort_values('mono', ascending=False).head(10)
    if not mono_df.empty:
        print(f"\n  Configurations with ANY monotonic horizon:")
        print(f"  {'Dollar':>8} {'Stable':>8} {'HY':>8} {'Score':>8} {'Mono':>5} {'Near':>5} {'21D Spr':>9} {'63D Spr':>9}")
        print(f"  {'─' * 75}")
        for _, row in mono_df.iterrows():
            print(f"  {row['w1']:>7.0%} {row['w2']:>7.0%} {row['w3']:>7.0%} {row['score']:>8.1f} {int(row['mono']):>5} {int(row['near_mono']):>5} {row['spread_21d']:>+8.1f}% {row['spread_63d']:>+8.1f}%")
    else:
        print(f"\n  No monotonic configurations found in 3-component grid.")
        print(f"  Near-monotonic (<= 1 violation, < 1.5% magnitude):")
        near_df = grid_df[grid_df['near_mono'] > 2].sort_values('score', ascending=False).head(10)
        if not near_df.empty:
            for _, row in near_df.iterrows():
                print(f"  {row['w1']:>7.0%} {row['w2']:>7.0%} {row['w3']:>7.0%} {row['score']:>8.1f} {int(row['mono']):>5} {int(row['near_mono']):>5} {row['spread_21d']:>+8.1f}% {row['spread_63d']:>+8.1f}%")

    # ================================================================
    # PHASE 6: Run the best grid result
    # ================================================================
    if best_weights:
        print(f"\n\n{'#' * 70}")
        print(f"  PHASE 6: BEST GRID RESULT - FULL ANALYSIS")
        print(f"{'#' * 70}")

        z_comps = {c: zscore_rolling(comp[c]) for c in best_weights}
        composite = sum(w * z_comps[c] for c, w in best_weights.items())
        test_composite(composite, fwd, label=f"BEST: {best_weights}", verbose=True)

    conn.close()

    print(f"\n{'=' * 70}")
    print(f"  BACKTEST v3 COMPLETE")
    print(f"{'=' * 70}")


if __name__ == '__main__':
    main()
