"""
CLI Out-of-Sample: 90/10 Split
================================
Train: first 90% of observations
Test:  last 10% of observations
Also: walk-forward (expanding window, always test on next quarter)

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

FINAL_WEIGHTS = {
    'DollarYoY': 0.20,
    'ResRatio_RoC': 0.50,
    'StableBTC_RoC': 0.15,
    'ResRatio': 0.15,
}


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
        if len(df) < 50:
            results.append({'hz': hz, 'spread': 0, 't': 0, 'p': 1,
                           'mono5': False, 'mono3': False, 'n': len(df),
                           'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0, 'q5': 0})
            continue
        df['q'] = pd.qcut(df['sig'], 5, labels=False, duplicates='drop') + 1
        means = df.groupby('q')['fwd'].mean() * 100
        q1, q5 = means.get(1, 0), means.get(5, 0)
        spread = q5 - q1

        g1, g5 = df[df['q'] == 1]['fwd'], df[df['q'] == 5]['fwd']
        t, p = stats.ttest_ind(g5, g1) if len(g1) > 5 and len(g5) > 5 else (0, 1)

        vals = [means.get(i, 0) for i in range(1, 6)]
        mono5 = all(vals[i] <= vals[i+1] for i in range(4))
        mono3 = vals[0] < vals[2] < vals[4]

        results.append({
            'hz': hz, 'spread': spread, 't': t, 'p': p,
            'mono5': mono5, 'mono3': mono3, 'n': len(df),
            'q1': q1, 'q2': means.get(2, 0), 'q3': means.get(3, 0),
            'q4': means.get(4, 0), 'q5': q5,
        })
    return results


def tercile_test(composite, btc_ret, horizons=[21, 42, 63]):
    """Tercile instead of quintile - more robust with smaller samples."""
    results = []
    for hz in horizons:
        fwd = btc_ret.rolling(hz).sum().shift(-hz)
        df = pd.DataFrame({'sig': composite, 'fwd': fwd}).dropna()
        if len(df) < 30:
            results.append({'hz': hz, 'spread': 0, 't': 0, 'p': 1, 'n': len(df),
                           'q1': 0, 'q2': 0, 'q3': 0, 'mono': False})
            continue
        df['q'] = pd.qcut(df['sig'], 3, labels=False, duplicates='drop') + 1
        means = df.groupby('q')['fwd'].mean() * 100
        q1, q3 = means.get(1, 0), means.get(3, 0)
        spread = q3 - q1

        g1, g3 = df[df['q'] == 1]['fwd'], df[df['q'] == 3]['fwd']
        t, p = stats.ttest_ind(g3, g1) if len(g1) > 5 and len(g3) > 5 else (0, 1)
        mono = means.get(1, 0) < means.get(2, 0) < means.get(3, 0)

        results.append({
            'hz': hz, 'spread': spread, 't': t, 'p': p, 'n': len(df),
            'q1': q1, 'q2': means.get(2, 0), 'q3': q3, 'mono': mono,
        })
    return results


def print_quintile(results, label):
    print(f"\n  {label}")
    print(f"  {'='*90}")
    print(f"  {'Hz':>4}  {'Q1':>8} {'Q2':>8} {'Q3':>8} {'Q4':>8} {'Q5':>8}  "
          f"{'Spread':>8} {'t':>6} {'p':>10}  {'M5':>3}  {'n':>5}")
    print(f"  {'-'*90}")
    for r in results:
        m5 = 'Y' if r['mono5'] else 'N'
        sig = '***' if r['p'] < 0.001 else '**' if r['p'] < 0.01 else '*' if r['p'] < 0.05 else 'ns'
        print(f"  {r['hz']:>3}D  {r['q1']:>+7.1f}% {r['q2']:>+7.1f}% {r['q3']:>+7.1f}% "
              f"{r['q4']:>+7.1f}% {r['q5']:>+7.1f}%  {r['spread']:>+7.1f}% {r['t']:>5.1f} "
              f"{r['p']:>9.5f}{sig:>3}   {m5:>2}  {r['n']:>5}")


def print_tercile(results, label):
    print(f"\n  {label}")
    print(f"  {'='*75}")
    print(f"  {'Hz':>4}  {'T1(Low)':>10} {'T2(Mid)':>10} {'T3(High)':>10}  "
          f"{'Spread':>8} {'t':>6} {'p':>10}  {'Mono':>4}  {'n':>5}")
    print(f"  {'-'*75}")
    for r in results:
        m = 'Y' if r['mono'] else 'N'
        sig = '***' if r['p'] < 0.001 else '**' if r['p'] < 0.01 else '*' if r['p'] < 0.05 else 'ns'
        print(f"  {r['hz']:>3}D  {r['q1']:>+9.1f}% {r['q2']:>+9.1f}% {r['q3']:>+9.1f}%  "
              f"{r['spread']:>+7.1f}% {r['t']:>5.1f} {r['p']:>9.5f}{sig:>3}   {m:>3}  {r['n']:>5}")


def main():
    print("=" * 70)
    print("  CLI OUT-OF-SAMPLE: 90/10 SPLIT + WALK-FORWARD")
    print("=" * 70)

    btc = fetch_btc()
    btc_ret = np.log(btc['BTC'] / btc['BTC'].shift(1))
    stable = fetch_stablecoins()

    conn = sqlite3.connect(DB_PATH)
    raw = build_raw_components(btc, conn, stable)
    conn.close()

    z_exp = {k: z_expanding(v) for k, v in raw.items()}
    composite = build_composite(z_exp)

    n = len(composite)
    split_idx = int(n * 0.9)
    split_date = composite.index[split_idx]

    print(f"\n  Total observations: {n}")
    print(f"  90/10 split date: {split_date.strftime('%Y-%m-%d')}")
    print(f"  Train: {composite.index[0].strftime('%Y-%m-%d')} to {split_date.strftime('%Y-%m-%d')} ({split_idx} obs)")
    print(f"  Test:  {split_date.strftime('%Y-%m-%d')} to {composite.index[-1].strftime('%Y-%m-%d')} ({n - split_idx} obs)")

    comp_train = composite.iloc[:split_idx]
    comp_test = composite.iloc[split_idx:]
    btc_ret_train = btc_ret.loc[comp_train.index[0]:comp_train.index[-1]]
    btc_ret_test = btc_ret.loc[comp_test.index[0]:]

    # ================================================================
    # 90/10 QUINTILE
    # ================================================================
    res_train = quintile_test(comp_train, btc_ret_train)
    res_test = quintile_test(comp_test, btc_ret_test)
    print_quintile(res_train, "TRAIN (90%) — Quintiles")
    print_quintile(res_test, "TEST (10%) — Quintiles")

    # ================================================================
    # 90/10 TERCILE (more robust for small OOS)
    # ================================================================
    res_train_t = tercile_test(comp_train, btc_ret_train)
    res_test_t = tercile_test(comp_test, btc_ret_test)
    print_tercile(res_train_t, "TRAIN (90%) — Terciles")
    print_tercile(res_test_t, "TEST (10%) — Terciles")

    # ================================================================
    # WALK-FORWARD: Train on expanding window, test on next 63 days
    # ================================================================
    print("\n" + "=" * 70)
    print("  WALK-FORWARD VALIDATION (Expanding Train, 63D Test Windows)")
    print("=" * 70)

    min_train = 504  # 2 years minimum
    step = 63  # quarterly steps
    wf_results = []

    for start in range(min_train, n - 63, step):
        train_comp = composite.iloc[:start]
        test_comp = composite.iloc[start:start + 63]
        test_ret = btc_ret.loc[test_comp.index[0]:]

        fwd = btc_ret.rolling(63).sum().shift(-63)
        df_test = pd.DataFrame({'sig': test_comp, 'fwd': fwd}).dropna()
        if len(df_test) < 10:
            continue

        # Use train quantile boundaries on test data
        boundaries = train_comp.quantile([0.2, 0.4, 0.6, 0.8]).values
        bins = [-np.inf] + list(boundaries) + [np.inf]
        try:
            df_test['q'] = pd.cut(df_test['sig'], bins=bins, labels=[1, 2, 3, 4, 5])
            means = df_test.groupby('q')['fwd'].mean() * 100
            q1 = means.get(1, np.nan)
            q5 = means.get(5, np.nan)
            if pd.notna(q1) and pd.notna(q5):
                wf_results.append({
                    'start': test_comp.index[0],
                    'q1': q1, 'q5': q5, 'spread': q5 - q1,
                    'n': len(df_test)
                })
        except Exception:
            pass

    if wf_results:
        wf_df = pd.DataFrame(wf_results)
        avg_spread = wf_df['spread'].mean()
        pct_positive = (wf_df['spread'] > 0).mean() * 100
        avg_q1 = wf_df['q1'].mean()
        avg_q5 = wf_df['q5'].mean()

        print(f"\n  Walk-forward windows: {len(wf_results)}")
        print(f"  Average Q5-Q1 spread: {avg_spread:+.1f}%")
        print(f"  % of windows with positive spread: {pct_positive:.0f}%")
        print(f"  Average Q1 return: {avg_q1:+.1f}%")
        print(f"  Average Q5 return: {avg_q5:+.1f}%")

    # ================================================================
    # SUMMARY
    # ================================================================
    print("\n" + "=" * 70)
    print("  SUMMARY")
    print("=" * 70)

    for hz in [21, 42, 63]:
        train = [r for r in res_test if r['hz'] == hz][0]
        print(f"\n  {hz}D OOS (10%): Spread = {train['spread']:>+7.1f}%  t = {train['t']:>5.1f}  "
              f"p = {train['p']:.5f}  Mono5 = {train['mono5']}")

    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
