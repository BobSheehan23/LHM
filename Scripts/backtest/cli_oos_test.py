"""
CLI Out-of-Sample Test
=======================
Train: 2018-2022 (weight selection period)
Test:  2023-2025 (out-of-sample validation)

Uses SAME weights from cli_final.py (FINAL_WEIGHTS).
Tests whether quintile monotonicity and spreads hold OOS.

Author: Lighthouse Macro
Date: 2026-02-13
"""

import sqlite3
import pandas as pd
import numpy as np
from scipy import stats
import yfinance as yf
import requests
import warnings
warnings.filterwarnings('ignore')

DB_PATH = '/Users/bob/LHM/Data/databases/Lighthouse_Master.db'

# These weights were determined on 2018-2025 full sample
FINAL_WEIGHTS = {
    'DollarYoY': 0.20,
    'ResRatio_RoC': 0.50,
    'StableBTC_RoC': 0.15,
    'ResRatio': 0.15,
}

TRAIN_END = '2022-12-31'
TEST_START = '2023-01-01'


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


def build_raw_components(btc, conn, stable):
    dtwex = load_series(conn, 'DTWEXBGS')
    totres = load_series(conn, 'TOTRESNS')
    walcl = load_series(conn, 'WALCL')

    dtwex_d = dtwex['DTWEXBGS'].reindex(btc.index, method='ffill')
    res = totres['TOTRESNS'].reindex(btc.index, method='ffill')
    fed = walcl['WALCL'].reindex(btc.index, method='ffill')
    stable_d = stable['stable_mcap'].reindex(btc.index, method='ffill')

    comps = {}
    comps['DollarYoY'] = -(dtwex_d / dtwex_d.shift(252) - 1)
    comps['ResRatio'] = res / fed
    rr = comps['ResRatio']
    comps['ResRatio_RoC'] = rr / rr.shift(63) - 1
    ratio = stable_d / btc['BTC']
    comps['StableBTC_RoC'] = -(ratio / ratio.shift(21) - 1)

    return comps


def z_expanding(s, min_periods=63):
    m = s.expanding(min_periods=min_periods).mean()
    sd = s.expanding(min_periods=min_periods).std()
    return (s - m) / sd


def build_composite(z_comps, weights=FINAL_WEIGHTS):
    parts = [weights[k] * z_comps[k] for k in weights]
    return sum(parts).dropna()


def quintile_test(composite, btc_ret, horizons=[21, 42, 63]):
    results = []
    for hz in horizons:
        fwd = btc_ret.rolling(hz).sum().shift(-hz)
        df = pd.DataFrame({'sig': composite, 'fwd': fwd}).dropna()
        df['q'] = pd.qcut(df['sig'], 5, labels=False, duplicates='drop') + 1
        means = df.groupby('q')['fwd'].mean() * 100
        q1, q5 = means.get(1, 0), means.get(5, 0)
        spread = q5 - q1

        g1, g5 = df[df['q'] == 1]['fwd'], df[df['q'] == 5]['fwd']
        t, p = stats.ttest_ind(g5, g1) if len(g1) > 5 and len(g5) > 5 else (0, 1)

        vals = [means.get(i, 0) for i in range(1, 6)]
        mono5 = all(vals[i] <= vals[i+1] for i in range(4))
        mono3 = vals[0] < vals[2] < vals[4]

        # Slugging ratio
        wins_q5 = g5[g5 > 0]
        losses_q5 = g5[g5 <= 0]
        wins_q1 = g1[g1 > 0]
        losses_q1 = g1[g1 <= 0]

        slug_q5 = (wins_q5.mean() / abs(losses_q5.mean())) if len(losses_q5) > 0 and losses_q5.mean() != 0 else float('inf')
        slug_q1 = (wins_q1.mean() / abs(losses_q1.mean())) if len(losses_q1) > 0 and losses_q1.mean() != 0 else 0
        wr_q5 = (g5 > 0).mean() * 100
        wr_q1 = (g1 > 0).mean() * 100

        results.append({
            'hz': hz, 'spread': spread, 't': t, 'p': p,
            'mono5': mono5, 'mono3': mono3, 'n': len(df),
            'q1': q1, 'q2': means.get(2, 0), 'q3': means.get(3, 0),
            'q4': means.get(4, 0), 'q5': q5,
            'wr_q1': wr_q1, 'wr_q5': wr_q5,
            'slug_q1': slug_q1, 'slug_q5': slug_q5,
        })
    return results


def print_results(results, label):
    print(f"\n  {label}")
    print(f"  {'='*100}")
    print(f"  {'Hz':>4}  {'Q1':>8} {'Q2':>8} {'Q3':>8} {'Q4':>8} {'Q5':>8}  "
          f"{'Spread':>8} {'t':>6} {'p':>10}  {'M5':>3} {'WR_Q1':>6} {'WR_Q5':>6}  {'n':>5}")
    print(f"  {'-'*100}")
    for r in results:
        m5 = 'Y' if r['mono5'] else 'N'
        sig = '***' if r['p'] < 0.001 else '**' if r['p'] < 0.01 else '*' if r['p'] < 0.05 else 'ns'
        print(f"  {r['hz']:>3}D  {r['q1']:>+7.1f}% {r['q2']:>+7.1f}% {r['q3']:>+7.1f}% "
              f"{r['q4']:>+7.1f}% {r['q5']:>+7.1f}%  {r['spread']:>+7.1f}% {r['t']:>5.1f} "
              f"{r['p']:>9.5f}{sig:>3}   {m5:>2} {r['wr_q1']:>5.0f}% {r['wr_q5']:>5.0f}%  {r['n']:>5}")


def main():
    print("=" * 70)
    print("  CLI OUT-OF-SAMPLE VALIDATION")
    print("  Train: 2018 - 2022 | Test: 2023 - 2025")
    print("  Weights: FIXED from full-sample optimization")
    print("=" * 70)

    btc = fetch_btc()
    btc_ret = np.log(btc['BTC'] / btc['BTC'].shift(1))
    stable = fetch_stablecoins()

    conn = sqlite3.connect(DB_PATH)
    raw = build_raw_components(btc, conn, stable)
    conn.close()

    # Build composite using expanding z-scores (same as final)
    z_exp = {k: z_expanding(v) for k, v in raw.items()}
    composite = build_composite(z_exp)

    # ================================================================
    # FULL SAMPLE (reference)
    # ================================================================
    res_full = quintile_test(composite, btc_ret)
    print_results(res_full, "FULL SAMPLE (2018-2025) — Reference")

    # ================================================================
    # IN-SAMPLE (train period)
    # ================================================================
    comp_train = composite.loc[:TRAIN_END]
    btc_ret_train = btc_ret.loc[:TRAIN_END]
    res_train = quintile_test(comp_train, btc_ret_train)
    print_results(res_train, "IN-SAMPLE (2018-2022) — Training Period")

    # ================================================================
    # OUT-OF-SAMPLE (test period)
    # ================================================================
    comp_test = composite.loc[TEST_START:]
    btc_ret_test = btc_ret.loc[TEST_START:]
    res_test = quintile_test(comp_test, btc_ret_test)
    print_results(res_test, "OUT-OF-SAMPLE (2023-2025) — Validation Period")

    # ================================================================
    # SUMMARY
    # ================================================================
    print("\n" + "=" * 70)
    print("  SUMMARY: Does the signal survive out-of-sample?")
    print("=" * 70)

    for hz in [21, 42, 63]:
        full = [r for r in res_full if r['hz'] == hz][0]
        train = [r for r in res_train if r['hz'] == hz][0]
        test = [r for r in res_test if r['hz'] == hz][0]

        print(f"\n  {hz}D Forward:")
        print(f"    Full:   Q5-Q1 = {full['spread']:>+7.1f}%  t = {full['t']:>5.1f}  Mono5 = {full['mono5']}  n = {full['n']}")
        print(f"    Train:  Q5-Q1 = {train['spread']:>+7.1f}%  t = {train['t']:>5.1f}  Mono5 = {train['mono5']}  n = {train['n']}")
        print(f"    OOS:    Q5-Q1 = {test['spread']:>+7.1f}%  t = {test['t']:>5.1f}  Mono5 = {test['mono5']}  n = {test['n']}")

        if test['mono5'] and test['p'] < 0.05:
            print(f"    VERDICT: PASSES OOS ✓")
        elif test['mono3'] and test['spread'] > 0:
            print(f"    VERDICT: PARTIALLY PASSES (mono3, positive spread)")
        else:
            print(f"    VERDICT: DOES NOT PASS OOS ✗")

    print("\n" + "=" * 70)
    print("  TEST COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    main()
