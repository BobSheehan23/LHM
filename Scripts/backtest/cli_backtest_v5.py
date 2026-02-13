"""
CLI Backtest v5: Final optimization and presentation
======================================================
v4 found the winning structure:
  Dollar 6-month change (inverted) + Reserve ratio dynamics

This script:
1. Tests BEST configs with stablecoins forced at 15-30%
2. Tests 3-component "presentation" configs (Dollar + Reserves + Crypto-native)
3. Produces final quintile tables for the article
4. Tercile analysis for cleaner regime signals
5. Rolling performance and drawdown analysis

Author: Lighthouse Macro
Date: 2026-02-12
"""

import sqlite3
import pandas as pd
import numpy as np
from scipy import stats
import yfinance as yf
import requests
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
    btc = yf.download('BTC-USD', start='2014-01-01', end='2026-02-13', progress=False)
    if isinstance(btc.columns, pd.MultiIndex):
        btc = btc.droplevel(1, axis=1)
    btc = btc[['Close']].rename(columns={'Close': 'BTC'})
    btc.index = pd.to_datetime(btc.index).tz_localize(None)
    return btc


def fetch_stablecoins():
    # USDT=1, USDC=2 on DefiLlama
    total = None
    for sid in [1, 2]:
        url = f"https://stablecoins.llama.fi/stablecoin/{sid}"
        resp = requests.get(url)
        data = resp.json()
        rows = []
        for pt in data.get('tokens', []):
            dt = pd.to_datetime(pt['date'], unit='s')
            circ = pt.get('circulating', {})
            mc = circ.get('peggedUSD', 0) if isinstance(circ, dict) else 0
            if mc > 0:
                rows.append({'date': dt, 'mcap': mc})
        if not rows:
            continue
        s = pd.DataFrame(rows).set_index('date').sort_index()
        s = s[~s.index.duplicated(keep='last')]
        if total is None:
            total = s.rename(columns={'mcap': 'stable_mcap'})
        else:
            total['stable_mcap'] = total['stable_mcap'].add(
                s['mcap'].reindex(total.index, method='ffill'), fill_value=0)
    return total


def quintile_test(composite, btc_ret, horizons=[5, 10, 21, 42, 63]):
    """Full quintile sort with monotonicity check."""
    results = []
    for hz in horizons:
        fwd = btc_ret.rolling(hz).sum().shift(-hz)
        df = pd.DataFrame({'sig': composite, 'fwd': fwd}).dropna()
        df['q'] = pd.qcut(df['sig'], 5, labels=False, duplicates='drop') + 1
        means = df.groupby('q')['fwd'].mean() * 100
        q1, q5 = means.get(1, 0), means.get(5, 0)
        spread = q5 - q1

        # t-test
        g1 = df[df['q'] == 1]['fwd']
        g5 = df[df['q'] == 5]['fwd']
        if len(g1) > 5 and len(g5) > 5:
            t, p = stats.ttest_ind(g5, g1)
        else:
            t, p = 0, 1

        # Monotonicity check
        vals = [means.get(i, 0) for i in range(1, 6)]
        mono5 = all(vals[i] <= vals[i+1] for i in range(4))
        mono3 = vals[0] < vals[2] < vals[4]

        # Regime spread
        rgm = means.get(5, 0) - means.get(1, 0)

        # Correlation
        r = df['sig'].corr(df['fwd'])

        results.append({
            'hz': hz, 'spread': spread, 't': t, 'p': p,
            'mono5': mono5, 'mono3': mono3, 'rgm': rgm, 'r': r,
            'q1': q1, 'q2': means.get(2, 0), 'q3': means.get(3, 0),
            'q4': means.get(4, 0), 'q5': q5
        })
    return results


def tercile_test(composite, btc_ret, horizons=[5, 10, 21, 42, 63]):
    """Tercile sort for regime analysis."""
    results = []
    for hz in horizons:
        fwd = btc_ret.rolling(hz).sum().shift(-hz)
        df = pd.DataFrame({'sig': composite, 'fwd': fwd}).dropna()
        df['t'] = pd.qcut(df['sig'], 3, labels=['Bearish', 'Neutral', 'Bullish'], duplicates='drop')
        means = df.groupby('t')['fwd'].mean() * 100
        counts = df.groupby('t')['fwd'].count()
        wins = df.groupby('t').apply(lambda x: (x['fwd'] > 0).mean() * 100)
        results.append({
            'hz': hz,
            'bear_ret': means.get('Bearish', 0), 'bear_n': counts.get('Bearish', 0), 'bear_wr': wins.get('Bearish', 0),
            'neut_ret': means.get('Neutral', 0), 'neut_n': counts.get('Neutral', 0), 'neut_wr': wins.get('Neutral', 0),
            'bull_ret': means.get('Bullish', 0), 'bull_n': counts.get('Bullish', 0), 'bull_wr': wins.get('Bullish', 0),
        })
    return results


def print_quintile(results, label=""):
    if label:
        print(f"\n  {label}")
    print(f"  {'─'*95}")
    print(f"  {'Hz':>4}   {'Q5-Q1':>8}  {'t':>5}  {'p':>12}  {'M5':>3} {'M3':>3}   {'Rgm':>6}  {'r':>6}  " +
          f"{'Q1':>6}  {'Q2':>6}  {'Q3':>6}  {'Q4':>6}  {'Q5':>6}")
    print(f"  {'─'*95}")
    for r in results:
        sig = '***' if r['p'] < 0.001 else '**' if r['p'] < 0.01 else '*' if r['p'] < 0.05 else ''
        m5 = '✓' if r['mono5'] else '✗'
        m3 = '✓' if r['mono3'] else '✗'
        print(f"  {r['hz']:>3}D   {r['spread']:>+7.1f}%  {r['t']:>5.1f}  {r['p']:>10.5f}{sig:<3}  "
              f" {m5:>2} {m3:>2}  {r['rgm']:>+5.1f}%  {r['r']:>+.3f}  "
              f"{r['q1']:>+5.1f}  {r['q2']:>+5.1f}  {r['q3']:>+5.1f}  {r['q4']:>+5.1f}  {r['q5']:>+5.1f}")


def print_tercile(results, label=""):
    if label:
        print(f"\n  {label}")
    print(f"  {'─'*100}")
    print(f"  {'Hz':>4}   {'Bearish':>8} {'WR':>5} {'n':>5}   {'Neutral':>8} {'WR':>5} {'n':>5}   "
          f"{'Bullish':>8} {'WR':>5} {'n':>5}   {'Bull-Bear':>10}")
    print(f"  {'─'*100}")
    for r in results:
        bb = r['bull_ret'] - r['bear_ret']
        print(f"  {r['hz']:>3}D   {r['bear_ret']:>+7.1f}% {r['bear_wr']:>4.0f}% {r['bear_n']:>5.0f}   "
              f"{r['neut_ret']:>+7.1f}% {r['neut_wr']:>4.0f}% {r['neut_n']:>5.0f}   "
              f"{r['bull_ret']:>+7.1f}% {r['bull_wr']:>4.0f}% {r['bull_n']:>5.0f}   "
              f"{bb:>+9.1f}%")


def main():
    print("="*70)
    print("  CLI v5: Final Optimization & Presentation")
    print("="*70)

    btc = fetch_btc()
    btc_ret = np.log(btc['BTC'] / btc['BTC'].shift(1))

    stable = fetch_stablecoins()
    print(f"  Stablecoins: {len(stable)} obs")

    conn = sqlite3.connect(DB_PATH)

    # Load components
    dtwex = load_series(conn, 'DTWEXBGS')
    totres = load_series(conn, 'TOTRESNS')
    walcl = load_series(conn, 'WALCL')
    hy = load_series(conn, 'BAMLH0A0HYM2')

    conn.close()

    # Build components
    comps = {}

    # Dollar 126d change inverted (6-month)
    dtwex_d = dtwex['DTWEXBGS'].reindex(btc.index, method='ffill')
    comps['Dollar126d'] = -(dtwex_d / dtwex_d.shift(126) - 1)

    # Dollar 63d change inverted (3-month)
    comps['Dollar63d'] = -(dtwex_d / dtwex_d.shift(63) - 1)

    # Dollar YoY inverted
    comps['DollarYoY'] = -(dtwex_d / dtwex_d.shift(252) - 1)

    # Reserve ratio (TOTRESNS / WALCL)
    res = totres['TOTRESNS'].reindex(btc.index, method='ffill')
    fed = walcl['WALCL'].reindex(btc.index, method='ffill')
    comps['ResRatio'] = res / fed

    # Reserve ratio 63d rate of change
    rr = comps['ResRatio']
    comps['ResRatio_RoC'] = rr / rr.shift(63) - 1

    # HY OAS inverted
    hy_d = hy['BAMLH0A0HYM2'].reindex(btc.index, method='ffill')
    comps['HY_Inv'] = -hy_d

    # Stablecoin 30d momentum
    stable_d = stable['stable_mcap'].reindex(btc.index, method='ffill')
    comps['Stable30d'] = stable_d / stable_d.shift(30) - 1

    # Stablecoin/BTC ratio momentum (inverted - rising ratio = BTC underperforming)
    btc_mcap_proxy = btc['BTC']  # price as proxy
    ratio = stable_d / btc_mcap_proxy
    comps['StableBTC_RoC'] = -(ratio / ratio.shift(21) - 1)

    # Z-score everything
    z_comps = {}
    for name, s in comps.items():
        expanding_mean = s.expanding(min_periods=63).mean()
        expanding_std = s.expanding(min_periods=63).std()
        z_comps[name] = (s - expanding_mean) / expanding_std

    # ================================================================
    # SECTION 1: THE v4 WINNER (no crypto-native)
    # ================================================================
    print("\n" + "#"*70)
    print("  SECTION 1: v4 WINNER (Dollar + Reserves)")
    print("#"*70)

    winner = (0.20 * z_comps['Dollar126d'] +
              0.40 * z_comps['Dollar63d'] +
              0.15 * z_comps['ResRatio'] +
              0.25 * z_comps['ResRatio_RoC']).dropna()

    q_results = quintile_test(winner, btc_ret)
    print_quintile(q_results, "Dollar126d:20% + Dollar63d:40% + ResRatio:15% + ResRatio_RoC:25%")

    t_results = tercile_test(winner, btc_ret)
    print_tercile(t_results, "TERCILE VIEW")

    current_val = winner.dropna().iloc[-1]
    print(f"\n  Current value: {current_val:.3f}")

    # ================================================================
    # SECTION 2: BEST 3-COMPONENT WITH STABLECOINS (15-35%)
    # ================================================================
    print("\n" + "#"*70)
    print("  SECTION 2: BEST 3-COMP WITH STABLECOINS (forced 15-35%)")
    print("#"*70)

    # Test: Dollar + ResRatio_RoC + Stablecoins at various weights
    best_score = -1
    best_cfg = None
    configs_tested = 0

    dollar_options = ['Dollar126d', 'Dollar63d', 'DollarYoY']
    reserve_options = ['ResRatio', 'ResRatio_RoC']
    stable_options = ['Stable30d', 'StableBTC_RoC']

    for d in dollar_options:
        for r in reserve_options:
            for s in stable_options:
                for sw in [15, 20, 25, 30, 35]:
                    remaining = 100 - sw
                    for dw in range(20, remaining, 5):
                        rw = remaining - dw
                        if rw < 10:
                            continue

                        w_d, w_r, w_s = dw/100, rw/100, sw/100
                        comp = (w_d * z_comps[d] + w_r * z_comps[r] + w_s * z_comps[s]).dropna()
                        if len(comp) < 500:
                            continue

                        configs_tested += 1
                        res = quintile_test(comp, btc_ret, horizons=[21, 42])

                        r21 = res[0]
                        r42 = res[1]

                        score = 0
                        if r21['mono5']:
                            score += 100
                        if r42['mono5']:
                            score += 50
                        if r21['mono3']:
                            score += 30
                        if r42['mono3']:
                            score += 15

                        score += r21['spread'] * 30
                        score += r42['spread'] * 10
                        score += max(0, -np.log10(max(r21['p'], 1e-20))) * 20

                        if score > best_score:
                            best_score = score
                            best_cfg = {
                                'comps': f"{d}:{dw}% | {r}:{rw}% | {s}:{sw}%",
                                'd': d, 'r': r, 's': s,
                                'dw': w_d, 'rw': w_r, 'sw': w_s,
                                'score': score,
                                '21d_spread': r21['spread'],
                                '42d_spread': r42['spread'],
                                '21d_mono': r21['mono5'],
                                '42d_mono': r42['mono5'],
                            }

    print(f"  Tested {configs_tested} configurations")
    print(f"\n  BEST: {best_cfg['comps']}")
    print(f"  Score: {best_cfg['score']:.0f}  |  21D spread: {best_cfg['21d_spread']:+.1f}%  |  "
          f"42D spread: {best_cfg['42d_spread']:+.1f}%")
    print(f"  21D mono: {best_cfg['21d_mono']}  |  42D mono: {best_cfg['42d_mono']}")

    # Show full detail
    comp_best = (best_cfg['dw'] * z_comps[best_cfg['d']] +
                 best_cfg['rw'] * z_comps[best_cfg['r']] +
                 best_cfg['sw'] * z_comps[best_cfg['s']]).dropna()
    q_res = quintile_test(comp_best, btc_ret)
    print_quintile(q_res, f"FULL DETAIL: {best_cfg['comps']}")
    t_res = tercile_test(comp_best, btc_ret)
    print_tercile(t_res, "TERCILE VIEW")
    print(f"  Current value: {comp_best.dropna().iloc[-1]:.3f}")

    # ================================================================
    # SECTION 3: 4-COMPONENT WITH STABLECOINS
    # ================================================================
    print("\n" + "#"*70)
    print("  SECTION 3: BEST 4-COMP WITH STABLECOINS (forced 15-30%)")
    print("#"*70)

    best4_score = -1
    best4_cfg = None
    configs4 = 0

    for d in dollar_options:
        for r in reserve_options:
            for s in stable_options:
                # Add HY or another dollar
                extras = ['HY_Inv']
                extra_dollars = [x for x in dollar_options if x != d]
                extra_reserves = [x for x in reserve_options if x != r]
                all_extras = extras + extra_dollars + extra_reserves

                for e in all_extras:
                    for sw in [15, 20, 25, 30]:
                        for ew in [10, 15, 20, 25]:
                            remaining = 100 - sw - ew
                            if remaining < 30:
                                continue
                            for dw in range(15, remaining, 5):
                                rw = remaining - dw
                                if rw < 10:
                                    continue

                                w_d, w_r, w_s, w_e = dw/100, rw/100, sw/100, ew/100
                                comp = (w_d * z_comps[d] + w_r * z_comps[r] +
                                        w_s * z_comps[s] + w_e * z_comps[e]).dropna()
                                if len(comp) < 500:
                                    continue

                                configs4 += 1
                                res = quintile_test(comp, btc_ret, horizons=[21, 42])
                                r21, r42 = res[0], res[1]

                                score = 0
                                if r21['mono5']:
                                    score += 100
                                if r42['mono5']:
                                    score += 50
                                if r21['mono3']:
                                    score += 30
                                if r42['mono3']:
                                    score += 15
                                score += r21['spread'] * 30
                                score += r42['spread'] * 10
                                score += max(0, -np.log10(max(r21['p'], 1e-20))) * 20

                                if score > best4_score:
                                    best4_score = score
                                    best4_cfg = {
                                        'comps': f"{d}:{dw}% | {r}:{rw}% | {s}:{sw}% | {e}:{ew}%",
                                        'comp': comp,
                                        'score': score,
                                        '21d_spread': r21['spread'],
                                        '42d_spread': r42['spread'],
                                        '21d_mono': r21['mono5'],
                                        '42d_mono': r42['mono5'],
                                    }

    print(f"  Tested {configs4} configurations")
    print(f"\n  BEST: {best4_cfg['comps']}")
    print(f"  Score: {best4_cfg['score']:.0f}  |  21D spread: {best4_cfg['21d_spread']:+.1f}%  |  "
          f"42D spread: {best4_cfg['42d_spread']:+.1f}%")
    print(f"  21D mono: {best4_cfg['21d_mono']}  |  42D mono: {best4_cfg['42d_mono']}")

    q4_res = quintile_test(best4_cfg['comp'], btc_ret)
    print_quintile(q4_res, f"FULL DETAIL: {best4_cfg['comps']}")
    t4_res = tercile_test(best4_cfg['comp'], btc_ret)
    print_tercile(t4_res, "TERCILE VIEW")
    print(f"  Current value: {best4_cfg['comp'].dropna().iloc[-1]:.3f}")

    # ================================================================
    # SECTION 4: CANDIDATE COMPARISON TABLE
    # ================================================================
    print("\n" + "#"*70)
    print("  SECTION 4: CANDIDATE COMPARISON")
    print("#"*70)

    candidates = {
        'A: v4 Winner (no crypto)': winner,
        f'B: Best 3-comp w/ stable': comp_best,
        f'C: Best 4-comp w/ stable': best4_cfg['comp'],
    }

    # Also test the v3 winner for comparison
    v3_winner = (0.55 * z_comps['DollarYoY'] +
                 0.05 * z_comps['Stable30d'] +
                 0.40 * z_comps['HY_Inv']).dropna()
    candidates['D: v3 Winner (DollarYoY+Stable+HY)'] = v3_winner

    # Simple 2-component: Dollar + Reserves
    simple2 = (0.55 * z_comps['Dollar126d'] + 0.45 * z_comps['ResRatio_RoC']).dropna()
    candidates['E: Simple 2-comp (Dollar+ResRoC)'] = simple2

    print(f"\n  {'Candidate':<40} {'21D Spread':>10} {'42D Spread':>10} {'63D Spread':>10} "
          f"{'M5@21':>6} {'M5@42':>6} {'M5@63':>6} {'Obs':>5}")
    print(f"  {'─'*110}")

    for name, comp in candidates.items():
        res = quintile_test(comp, btc_ret)
        r21 = [r for r in res if r['hz'] == 21][0]
        r42 = [r for r in res if r['hz'] == 42][0]
        r63 = [r for r in res if r['hz'] == 63][0]
        m21 = '✓' if r21['mono5'] else '✗'
        m42 = '✓' if r42['mono5'] else '✗'
        m63 = '✓' if r63['mono5'] else '✗'
        print(f"  {name:<40} {r21['spread']:>+9.1f}% {r42['spread']:>+9.1f}% {r63['spread']:>+9.1f}% "
              f"{m21:>6} {m42:>6} {m63:>6} {len(comp):>5}")

    # ================================================================
    # SECTION 5: ROLLING PERFORMANCE (WINNER)
    # ================================================================
    print("\n" + "#"*70)
    print("  SECTION 5: ROLLING YEARLY ANALYSIS (v4 Winner)")
    print("#"*70)

    fwd21 = btc_ret.rolling(21).sum().shift(-21)
    df_roll = pd.DataFrame({'sig': winner, 'fwd': fwd21}).dropna()

    # Year-by-year tercile analysis
    df_roll['year'] = df_roll.index.year
    print(f"\n  {'Year':>6}  {'Bear':>8} {'Neut':>8} {'Bull':>8} {'B-B':>8}  {'n':>5}")
    print(f"  {'─'*55}")
    for yr in sorted(df_roll['year'].unique()):
        chunk = df_roll[df_roll['year'] == yr]
        if len(chunk) < 30:
            continue
        try:
            chunk = chunk.copy()
            chunk['t'] = pd.qcut(chunk['sig'], 3, labels=['Bear', 'Neut', 'Bull'], duplicates='drop')
            means = chunk.groupby('t')['fwd'].mean() * 100
            bb = means.get('Bull', 0) - means.get('Bear', 0)
            print(f"  {yr:>6}  {means.get('Bear', 0):>+7.1f}% {means.get('Neut', 0):>+7.1f}% "
                  f"{means.get('Bull', 0):>+7.1f}% {bb:>+7.1f}%  {len(chunk):>5}")
        except Exception:
            print(f"  {yr:>6}  (insufficient data)")

    # ================================================================
    # SECTION 6: CURRENT REGIME
    # ================================================================
    print("\n" + "#"*70)
    print("  SECTION 6: CURRENT READINGS")
    print("#"*70)

    for name, comp in candidates.items():
        val = comp.dropna().iloc[-1]
        last_date = comp.dropna().index[-1].strftime('%Y-%m-%d')
        regime = "Expanding" if val > 0.5 else "Contracting" if val < -0.5 else "Neutral"
        print(f"  {name:<40}  {val:>+.3f}  [{regime}]  as of {last_date}")

    # Component readings
    print(f"\n  COMPONENT READINGS (latest z-scores):")
    for name in ['Dollar126d', 'Dollar63d', 'DollarYoY', 'ResRatio', 'ResRatio_RoC',
                  'HY_Inv', 'Stable30d', 'StableBTC_RoC']:
        z = z_comps[name].dropna()
        if len(z) > 0:
            val = z.iloc[-1]
            dt = z.index[-1].strftime('%Y-%m-%d')
            print(f"    {name:<20}  {val:>+.3f}  as of {dt}")

    print("\n" + "="*70)
    print("  v5 COMPLETE")
    print("="*70)


if __name__ == '__main__':
    main()
