"""
CLTI Backtest v4: Expanded component set + data-driven weighting
================================================================
New components:
  - Reserves as % of Fed assets (TOTRESNS / WALCL) - buffer adequacy
  - T-bill yield spread (3mo - 1mo) as demand proxy
  - RRP rate of change
  - Net liquidity as % of GDP (scale-adjusted)
  - Stablecoin/BTC mcap ratio momentum

Grid search over 3, 4, and 5 component combos.
Data-driven: let the optimizer find what works.

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
from itertools import combinations
warnings.filterwarnings('ignore')

DB_PATH = '/Users/bob/LHM/Data/databases/Lighthouse_Master.db'


def load_series(conn, sid):
    df = pd.read_sql(
        "SELECT date, value FROM observations WHERE series_id = ? ORDER BY date",
        conn, params=(sid,), parse_dates=['date']
    ).set_index('date').rename(columns={'value': sid})
    return df


def fetch_btc():
    print("Fetching BTC...")
    btc = yf.download('BTC-USD', start='2014-01-01', end='2026-02-13', progress=False)
    if isinstance(btc.columns, pd.MultiIndex):
        btc = btc.droplevel(1, axis=1)
    btc = btc[['Close']].rename(columns={'Close': 'BTC'})
    btc.index = pd.to_datetime(btc.index).tz_localize(None)
    return btc


def fetch_stablecoins():
    print("Fetching stablecoins...")
    all_dfs = []
    for sid, label in [('1', 'USDT'), ('2', 'USDC')]:
        try:
            resp = requests.get(f'https://stablecoins.llama.fi/stablecoin/{sid}', timeout=30)
            rows = [{'date': pd.Timestamp(t['date'], unit='s').normalize(),
                     label: t.get('circulating', {}).get('peggedUSD', None)}
                    for t in resp.json().get('tokens', [])]
            df = pd.DataFrame(rows).dropna().set_index('date')
            df = df[~df.index.duplicated(keep='last')]
            all_dfs.append(df)
            time.sleep(1)
        except Exception as e:
            print(f"  {label}: {e}")
    combined = pd.concat(all_dfs, axis=1)
    combined['STABLE_TOTAL'] = combined.sum(axis=1)
    return combined


def z(series, window=504, min_p=126):
    mean = series.rolling(window, min_periods=min_p).mean()
    std = series.rolling(window, min_periods=min_p).std()
    return (series - mean) / std.replace(0, np.nan)


def fwd_returns(prices):
    fwd = pd.DataFrame(index=prices.index)
    for h in [5, 10, 21, 42, 63]:
        fwd[f'fwd_{h}d'] = prices.shift(-h) / prices - 1
    return fwd


def test(composite, fwd, verbose=False, label=""):
    results = {}
    for hcol in ['fwd_5d', 'fwd_10d', 'fwd_21d', 'fwd_42d', 'fwd_63d']:
        df = pd.DataFrame({'c': composite, 'f': fwd[hcol]}).dropna()
        if len(df) < 150:
            continue

        df['q'] = pd.qcut(df['c'], 5, labels=['Q1', 'Q2', 'Q3', 'Q4', 'Q5'])
        qm = df.groupby('q')['f'].mean() * 100
        vals = qm.values

        q5 = df[df['q'] == 'Q5']['f']
        q1 = df[df['q'] == 'Q1']['f']
        t_s, p_v = stats.ttest_ind(q5, q1, equal_var=False)
        spread = (q5.mean() - q1.mean()) * 100

        mono = all(vals[i] <= vals[i + 1] for i in range(len(vals) - 1))
        violations = sum(1 for i in range(len(vals) - 1) if vals[i] > vals[i + 1])
        max_v = max((vals[i] - vals[i + 1] for i in range(len(vals) - 1) if vals[i] > vals[i + 1]), default=0)
        near = violations <= 1 and max_v < 1.5

        # Regime
        contr = df[df['c'] < -0.5]['f']
        expan = df[df['c'] > 0.5]['f']
        if len(contr) > 10 and len(expan) > 10:
            rs = (expan.mean() - contr.mean()) * 100
        else:
            rs = np.nan

        # Tercile monotonicity
        df['t3'] = pd.qcut(df['c'], 3, labels=['T1', 'T2', 'T3'])
        t3m = df.groupby('t3')['f'].mean() * 100
        t3_mono = t3m.iloc[0] <= t3m.iloc[1] <= t3m.iloc[2]

        results[hcol] = {
            'n': len(df), 'spread': spread, 't': t_s, 'p': p_v,
            'mono': mono, 'near': near, 'qm': qm.to_dict(),
            'regime': rs, 'corr': df['c'].corr(df['f']),
            't3_mono': t3_mono, 'violations': violations,
        }

    if verbose and results:
        print(f"\n  {label}")
        print(f"  {'─' * 85}")
        print(f"  {'Hz':<6} {'Q5-Q1':>7} {'t':>6} {'p':>9} {'M5':>3} {'M3':>3} {'Rgm':>7} {'r':>5}  Q1      Q2      Q3      Q4      Q5")
        print(f"  {'─' * 85}")
        for h, r in results.items():
            hl = h.replace('fwd_', '').replace('d', 'D')
            sig = '***' if r['p'] < 0.001 else ('**' if r['p'] < 0.01 else ('*' if r['p'] < 0.05 else ''))
            m5 = '✓' if r['mono'] else '✗'
            m3 = '✓' if r['t3_mono'] else '✗'
            rgm = f"{r['regime']:+.1f}" if not np.isnan(r['regime']) else 'N/A'
            qm = r['qm']
            print(f"  {hl:<6} {r['spread']:+6.1f}% {r['t']:>5.1f} {r['p']:>8.5f}{sig:<3} {m5:>2} {m3:>2} {rgm:>6}% {r['corr']:+.3f}  {qm['Q1']:+5.1f}   {qm['Q2']:+5.1f}   {qm['Q3']:+5.1f}   {qm['Q4']:+5.1f}   {qm['Q5']:+5.1f}")

    return results


def score(results):
    s = 0
    for r in results.values():
        if r['p'] < 0.05:
            s += abs(r['spread']) * 2
        if r['mono']:
            s += 100
        elif r['near']:
            s += 40
        if r['t3_mono']:
            s += 30
        if not np.isnan(r['regime']):
            s += abs(r['regime'])
    return s


def main():
    print("=" * 70)
    print("  CLTI v4: Data-Driven Component Discovery")
    print("=" * 70)

    import sys
    sys.path.insert(0, '/Users/bob/LHM/Scripts/data_pipeline/lighthouse')
    from config import API_KEYS

    conn = sqlite3.connect(DB_PATH)
    btc = fetch_btc()
    stables = fetch_stablecoins()

    # Load DB series
    m2 = load_series(conn, 'M2SL').resample('D').ffill()
    walcl = load_series(conn, 'WALCL').resample('D').ffill()
    tga = load_series(conn, 'WTREGEN').resample('D').ffill()
    rrp = load_series(conn, 'RRPONTSYD').resample('D').ffill()
    hy = load_series(conn, 'BAMLH0A0HYM2')
    dollar = load_series(conn, 'DTWEXBGS')
    reserves = load_series(conn, 'TOTRESNS').resample('D').ffill()
    dgs1mo = load_series(conn, 'DGS1MO')
    dgs3mo = load_series(conn, 'DGS3MO')

    print("\nBuilding expanded component set...")
    c = pd.DataFrame(index=btc.index)
    c['BTC'] = btc['BTC']

    # --- Proven winners from v3 ---
    c['DollarYoY'] = -dollar['DTWEXBGS'].pct_change(252)
    c['HY_Inv'] = -hy['BAMLH0A0HYM2']
    c['Stable30d'] = stables['STABLE_TOTAL'].pct_change(30)

    # --- Dollar variants ---
    c['Dollar63d'] = -dollar['DTWEXBGS'].pct_change(63)
    c['Dollar126d'] = -dollar['DTWEXBGS'].pct_change(126)

    # --- Net liquidity ---
    net_liq = walcl['WALCL'] - tga['WTREGEN'] - rrp['RRPONTSYD']
    c['NetLiq_4w'] = net_liq.pct_change(20)
    c['NetLiq_13w'] = net_liq.pct_change(63)

    # --- NEW: Reserves as % of Fed assets ---
    # Higher ratio = more buffer = positive
    res_ratio = reserves['TOTRESNS'] / walcl['WALCL']
    c['ResRatio'] = res_ratio
    c['ResRatio_RoC'] = res_ratio.pct_change(63)
    print(f"  ResRatio: {c['ResRatio'].dropna().shape[0]} obs")

    # --- NEW: RRP depletion signal ---
    # RRP level (higher = more buffer = positive)
    c['RRP_Level'] = rrp['RRPONTSYD']
    # RRP as % of Fed assets
    c['RRP_Ratio'] = rrp['RRPONTSYD'] / walcl['WALCL']
    # RRP change (negative = draining = ambiguous)
    c['RRP_RoC_13w'] = rrp['RRPONTSYD'].pct_change(63)
    print(f"  RRP variants: {c['RRP_Level'].dropna().shape[0]} obs")

    # --- NEW: T-bill spread (3mo - 1mo) as demand/stress proxy ---
    # Inverted: when 3mo yields less than 1mo, bills in high demand = positive
    c['TBill_Spread_Inv'] = -(dgs3mo['DGS3MO'] - dgs1mo['DGS1MO'])
    print(f"  TBill Spread: {c['TBill_Spread_Inv'].dropna().shape[0]} obs")

    # --- NEW: Stablecoin / BTC mcap ratio ---
    btc_mcap = btc['BTC'] * 19.8e6  # ~19.8M BTC circulating
    stable_btc = stables['STABLE_TOTAL'] / btc_mcap
    c['StableBTC_RoC'] = stable_btc.pct_change(30)
    print(f"  Stable/BTC ratio: {c['StableBTC_RoC'].dropna().shape[0]} obs")

    # --- M2 ---
    c['M2_3m'] = m2['M2SL'].pct_change(63) * 4
    c['M2_YoY'] = m2['M2SL'].pct_change(252)

    # --- NEW: TGA impulse (TGA drawdown = liquidity release) ---
    c['TGA_Impulse'] = -tga['WTREGEN'].pct_change(20)  # Inverted: drawdown = positive
    c['TGA_Impulse_13w'] = -tga['WTREGEN'].pct_change(63)
    print(f"  TGA Impulse: {c['TGA_Impulse'].dropna().shape[0]} obs")

    # --- NEW: WALCL momentum (Fed balance sheet growth) ---
    c['Fed_BS_13w'] = walcl['WALCL'].pct_change(63)
    print(f"  Fed BS 13w: {c['Fed_BS_13w'].dropna().shape[0]} obs")

    fwd = fwd_returns(c['BTC'].dropna())

    # ================================================================
    # PHASE 1: Test all new components individually
    # ================================================================
    print(f"\n{'#' * 70}")
    print(f"  PHASE 1: ALL COMPONENTS INDIVIDUALLY")
    print(f"{'#' * 70}")

    all_comps = [
        'DollarYoY', 'Dollar63d', 'Dollar126d',
        'HY_Inv', 'Stable30d', 'StableBTC_RoC',
        'NetLiq_4w', 'NetLiq_13w',
        'ResRatio', 'ResRatio_RoC',
        'RRP_Level', 'RRP_Ratio', 'RRP_RoC_13w',
        'TBill_Spread_Inv', 'TGA_Impulse', 'TGA_Impulse_13w',
        'Fed_BS_13w', 'M2_3m', 'M2_YoY',
    ]

    individual = {}
    for col in all_comps:
        if col in c.columns and c[col].dropna().shape[0] > 300:
            zc = z(c[col])
            res = test(zc, fwd, verbose=True, label=col)
            if res:
                # Use 21D spread as primary ranking
                s21 = res.get('fwd_21d', {}).get('spread', 0)
                p21 = res.get('fwd_21d', {}).get('p', 1)
                m21 = res.get('fwd_21d', {}).get('mono', False)
                individual[col] = {'spread': s21, 'p': p21, 'mono': m21, 'res': res}

    # Rank by 21D spread
    ranked_ind = sorted(individual.items(), key=lambda x: -abs(x[1]['spread']))
    print(f"\n  INDIVIDUAL RANKING (21D spread):")
    print(f"  {'Component':<20} {'21D Spread':>10} {'p-val':>10} {'Mono':>5}")
    print(f"  {'─' * 50}")
    for name, info in ranked_ind:
        sig = '***' if info['p'] < 0.001 else ('**' if info['p'] < 0.01 else ('*' if info['p'] < 0.05 else ''))
        m = '✓' if info['mono'] else '✗'
        print(f"  {name:<20} {info['spread']:>+9.2f}% {info['p']:>9.6f}{sig} {m:>4}")

    # ================================================================
    # PHASE 2: All 3-component combos from top 8
    # ================================================================
    print(f"\n\n{'#' * 70}")
    print(f"  PHASE 2: 3-COMPONENT COMBO SEARCH (top 10 components)")
    print(f"{'#' * 70}")

    # Take top 10 by individual performance
    top_comps = [name for name, _ in ranked_ind[:10]]
    print(f"  Using: {top_comps}")

    best_3 = []
    weight_sets = [
        (0.50, 0.30, 0.20),
        (0.40, 0.35, 0.25),
        (0.33, 0.34, 0.33),
        (0.60, 0.25, 0.15),
        (0.45, 0.30, 0.25),
        (0.55, 0.25, 0.20),
        (0.50, 0.35, 0.15),
        (0.40, 0.40, 0.20),
    ]

    for combo in combinations(top_comps, 3):
        # Check all have enough overlapping data
        valid_counts = [c[col].dropna().shape[0] for col in combo if col in c.columns]
        if min(valid_counts) < 300:
            continue

        for w_set in weight_sets:
            for perm in set(__import__('itertools').permutations(w_set)):
                weights = dict(zip(combo, perm))
                z_comps = {col: z(c[col]) for col in combo}
                composite = sum(w * z_comps[col] for col, w in weights.items())

                res = test(composite, fwd, verbose=False)
                if not res:
                    continue

                sc = score(res)
                mono_21 = res.get('fwd_21d', {}).get('mono', False)
                mono_42 = res.get('fwd_42d', {}).get('mono', False)
                t3_21 = res.get('fwd_21d', {}).get('t3_mono', False)

                best_3.append({
                    'combo': combo, 'weights': weights, 'score': sc,
                    'spread_21': res.get('fwd_21d', {}).get('spread', 0),
                    'spread_63': res.get('fwd_63d', {}).get('spread', 0),
                    'mono_21': mono_21, 'mono_42': mono_42, 't3_21': t3_21,
                    'p_21': res.get('fwd_21d', {}).get('p', 1),
                    'res': res,
                })

    # Sort by score
    best_3.sort(key=lambda x: -x['score'])

    print(f"\n  Tested {len(best_3)} 3-component configurations")
    print(f"\n  TOP 20 BY SCORE:")
    print(f"  {'Score':>7} {'M21':>4} {'M42':>4} {'T3':>3} {'21D':>7} {'63D':>7} {'p(21)':>9}  Components + Weights")
    print(f"  {'─' * 90}")
    for entry in best_3[:20]:
        m21 = '✓' if entry['mono_21'] else '✗'
        m42 = '✓' if entry['mono_42'] else '✗'
        t3 = '✓' if entry['t3_21'] else '✗'
        w_str = ' | '.join(f"{k}:{v:.0%}" for k, v in entry['weights'].items())
        print(f"  {entry['score']:>7.0f} {m21:>3} {m42:>3} {t3:>3} {entry['spread_21']:+6.1f}% {entry['spread_63']:+6.1f}% {entry['p_21']:>8.5f}  {w_str}")

    # Show only monotonic at 21D
    mono_configs = [e for e in best_3 if e['mono_21']]
    print(f"\n  MONOTONIC AT 21D: {len(mono_configs)} configs found")
    if mono_configs:
        print(f"  {'Score':>7} {'M42':>4} {'21D':>7} {'63D':>7}  Components + Weights")
        print(f"  {'─' * 80}")
        for entry in mono_configs[:15]:
            m42 = '✓' if entry['mono_42'] else '✗'
            w_str = ' | '.join(f"{k}:{v:.0%}" for k, v in entry['weights'].items())
            print(f"  {entry['score']:>7.0f} {m42:>3} {entry['spread_21']:+6.1f}% {entry['spread_63']:+6.1f}%  {w_str}")

    # ================================================================
    # PHASE 3: 4-component combos from top 6
    # ================================================================
    print(f"\n\n{'#' * 70}")
    print(f"  PHASE 3: 4-COMPONENT COMBOS (top 8 components)")
    print(f"{'#' * 70}")

    top6 = [name for name, _ in ranked_ind[:8]]

    best_4 = []
    w4_sets = [
        (0.35, 0.25, 0.25, 0.15),
        (0.30, 0.30, 0.20, 0.20),
        (0.40, 0.25, 0.20, 0.15),
        (0.25, 0.25, 0.25, 0.25),
        (0.35, 0.30, 0.20, 0.15),
        (0.40, 0.20, 0.20, 0.20),
    ]

    for combo in combinations(top6, 4):
        valid_counts = [c[col].dropna().shape[0] for col in combo if col in c.columns]
        if min(valid_counts) < 300:
            continue

        for w_set in w4_sets:
            for perm in set(__import__('itertools').permutations(w_set)):
                weights = dict(zip(combo, perm))
                z_comps = {col: z(c[col]) for col in combo}
                composite = sum(w * z_comps[col] for col, w in weights.items())

                res = test(composite, fwd, verbose=False)
                if not res:
                    continue

                sc = score(res)
                mono_21 = res.get('fwd_21d', {}).get('mono', False)
                mono_42 = res.get('fwd_42d', {}).get('mono', False)

                best_4.append({
                    'combo': combo, 'weights': weights, 'score': sc,
                    'spread_21': res.get('fwd_21d', {}).get('spread', 0),
                    'spread_63': res.get('fwd_63d', {}).get('spread', 0),
                    'mono_21': mono_21, 'mono_42': mono_42,
                    'p_21': res.get('fwd_21d', {}).get('p', 1),
                    'res': res,
                })

    best_4.sort(key=lambda x: -x['score'])

    print(f"\n  Tested {len(best_4)} 4-component configurations")
    print(f"\n  TOP 20 BY SCORE:")
    print(f"  {'Score':>7} {'M21':>4} {'M42':>4} {'21D':>7} {'63D':>7}  Components + Weights")
    print(f"  {'─' * 90}")
    for entry in best_4[:20]:
        m21 = '✓' if entry['mono_21'] else '✗'
        m42 = '✓' if entry['mono_42'] else '✗'
        w_str = ' | '.join(f"{k}:{v:.0%}" for k, v in entry['weights'].items())
        print(f"  {entry['score']:>7.0f} {m21:>3} {m42:>3} {entry['spread_21']:+6.1f}% {entry['spread_63']:+6.1f}%  {w_str}")

    mono4 = [e for e in best_4 if e['mono_21']]
    print(f"\n  MONOTONIC AT 21D: {len(mono4)} configs")
    if mono4:
        for entry in mono4[:10]:
            m42 = '✓' if entry['mono_42'] else '✗'
            w_str = ' | '.join(f"{k}:{v:.0%}" for k, v in entry['weights'].items())
            print(f"  {entry['score']:>7.0f} {m42:>3} {entry['spread_21']:+6.1f}% {entry['spread_63']:+6.1f}%  {w_str}")

    # ================================================================
    # PHASE 4: Full detail on best overall configs
    # ================================================================
    print(f"\n\n{'#' * 70}")
    print(f"  PHASE 4: TOP 5 CONFIGS - FULL DETAIL")
    print(f"{'#' * 70}")

    # Merge best 3 and 4 component, take top 5
    all_best = best_3 + best_4
    all_best.sort(key=lambda x: -x['score'])

    # Deduplicate by combo+weights
    seen = set()
    unique_best = []
    for entry in all_best:
        key = str(sorted(entry['weights'].items()))
        if key not in seen:
            seen.add(key)
            unique_best.append(entry)

    for i, entry in enumerate(unique_best[:5], 1):
        weights = entry['weights']
        z_comps = {col: z(c[col]) for col in weights}
        composite = sum(w * z_comps[col] for col, w in weights.items())
        valid = composite.dropna()

        w_str = ' + '.join(f"{k}({v:.0%})" for k, v in weights.items())
        print(f"\n  === #{i}: {w_str} ===")
        print(f"  Obs: {len(valid)}, {valid.index.min().date()} to {valid.index.max().date()}")
        print(f"  Current: {valid.iloc[-1]:.3f}")

        test(composite, fwd, verbose=True, label=f"#{i}")

        # Win rates
        df_wr = pd.DataFrame({'comp': composite, 'fwd': fwd['fwd_21d']}).dropna()
        if len(df_wr) > 100:
            print(f"  Win Rates (21D):")
            for lbl, mask in [
                ('Contracting (<-0.5)', df_wr['comp'] < -0.5),
                ('Neutral', (df_wr['comp'] >= -0.5) & (df_wr['comp'] <= 0.5)),
                ('Expanding (>+0.5)', df_wr['comp'] > 0.5),
            ]:
                sub = df_wr[mask]['fwd']
                if len(sub) > 10:
                    print(f"    {lbl}: {(sub > 0).mean() * 100:.1f}% (n={len(sub)}, avg={sub.mean() * 100:+.1f}%)")

    conn.close()
    print(f"\n{'=' * 70}")
    print(f"  v4 COMPLETE")
    print(f"{'=' * 70}")


if __name__ == '__main__':
    main()
