"""
CLI: Win/loss asymmetry and risk-adjusted metrics by quintile
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

def z_expanding(s, min_periods=63):
    m = s.expanding(min_periods=min_periods).mean()
    sd = s.expanding(min_periods=min_periods).std()
    return (s - m) / sd

def main():
    btc = fetch_btc()
    btc_ret = np.log(btc['BTC'] / btc['BTC'].shift(1))
    stable = fetch_stablecoins()

    conn = sqlite3.connect(DB_PATH)
    dtwex = load_series(conn, 'DTWEXBGS')
    totres = load_series(conn, 'TOTRESNS')
    walcl = load_series(conn, 'WALCL')
    conn.close()

    # Build components
    dtwex_d = dtwex['DTWEXBGS'].reindex(btc.index, method='ffill')
    stable_d = stable['stable_mcap'].reindex(btc.index, method='ffill')
    res = totres['TOTRESNS'].reindex(btc.index, method='ffill')
    fed = walcl['WALCL'].reindex(btc.index, method='ffill')

    raw = {
        'DollarYoY': -(dtwex_d / dtwex_d.shift(252) - 1),
        'ResRatio': res / fed,
        'StableBTC_RoC': -(stable_d / btc['BTC'] / (stable_d.shift(21) / btc['BTC'].shift(21)) - 1),
    }
    rr = raw['ResRatio']
    raw['ResRatio_RoC'] = rr / rr.shift(63) - 1

    z = {k: z_expanding(v) for k, v in raw.items()}
    cli =(0.20 * z['DollarYoY'] + 0.50 * z['ResRatio_RoC'] +
            0.15 * z['StableBTC_RoC'] + 0.15 * z['ResRatio']).dropna()

    print("="*80)
    print("  CLI: WIN/LOSS ASYMMETRY & RISK-ADJUSTED METRICS")
    print("="*80)

    for hz in [21, 42, 63]:
        fwd = btc_ret.rolling(hz).sum().shift(-hz) * 100
        df = pd.DataFrame({'sig': cli, 'fwd': fwd}).dropna()
        df['q'] = pd.qcut(df['sig'], 5, labels=False, duplicates='drop') + 1

        print(f"\n  {hz}D FORWARD RETURNS:")
        print(f"  {'Q':>4} {'Avg':>8} {'Med':>8} {'WR':>6} {'Avg Win':>9} {'Avg Loss':>9} "
              f"{'Win/Loss':>9} {'Sharpe':>7} {'Slugging':>9} {'Sortino':>8}")
        print(f"  {'─'*90}")

        for q in range(1, 6):
            g = df[df['q'] == q]['fwd']
            avg = g.mean()
            med = g.median()
            wr = (g > 0).mean() * 100
            wins = g[g > 0]
            losses = g[g <= 0]
            avg_win = wins.mean() if len(wins) > 0 else 0
            avg_loss = losses.mean() if len(losses) > 0 else 0
            win_loss = abs(avg_win / avg_loss) if avg_loss != 0 else float('inf')
            sharpe = g.mean() / g.std() if g.std() > 0 else 0
            # Slugging: (win rate * avg win) / (loss rate * avg loss)
            loss_rate = 1 - wr/100
            slug_num = (wr/100) * avg_win
            slug_den = loss_rate * abs(avg_loss) if loss_rate > 0 and avg_loss != 0 else 1
            slugging = slug_num / slug_den
            # Sortino: mean / downside deviation
            downside = g[g < 0]
            down_std = np.sqrt((downside**2).mean()) if len(downside) > 0 else 1
            sortino = avg / down_std

            print(f"  Q{q:>2} {avg:>+7.1f}% {med:>+7.1f}% {wr:>5.0f}% {avg_win:>+8.1f}% {avg_loss:>+8.1f}% "
                  f"{win_loss:>8.2f}x {sharpe:>+6.2f} {slugging:>8.2f}x {sortino:>+7.2f}")

        # Tercile regime version
        print(f"\n  {hz}D TERCILE REGIMES:")
        cuts = df['sig'].quantile([1/3, 2/3])
        df['regime'] = pd.cut(df['sig'],
                              bins=[-np.inf, cuts.iloc[0], cuts.iloc[1], np.inf],
                              labels=['Contracting', 'Neutral', 'Expanding'])

        print(f"  {'Regime':<14} {'Avg':>8} {'Med':>8} {'WR':>6} {'Avg Win':>9} {'Avg Loss':>9} "
              f"{'Win/Loss':>9} {'Sharpe':>7} {'Slugging':>9} {'Sortino':>8}")
        print(f"  {'─'*90}")

        for regime in ['Contracting', 'Neutral', 'Expanding']:
            g = df[df['regime'] == regime]['fwd']
            avg = g.mean()
            med = g.median()
            wr = (g > 0).mean() * 100
            wins = g[g > 0]
            losses = g[g <= 0]
            avg_win = wins.mean() if len(wins) > 0 else 0
            avg_loss = losses.mean() if len(losses) > 0 else 0
            win_loss = abs(avg_win / avg_loss) if avg_loss != 0 else float('inf')
            sharpe = g.mean() / g.std() if g.std() > 0 else 0
            loss_rate = 1 - wr/100
            slug_num = (wr/100) * avg_win
            slug_den = loss_rate * abs(avg_loss) if loss_rate > 0 and avg_loss != 0 else 1
            slugging = slug_num / slug_den
            downside = g[g < 0]
            down_std = np.sqrt((downside**2).mean()) if len(downside) > 0 else 1
            sortino = avg / down_std

            print(f"  {regime:<14} {avg:>+7.1f}% {med:>+7.1f}% {wr:>5.0f}% {avg_win:>+8.1f}% {avg_loss:>+8.1f}% "
                  f"{win_loss:>8.2f}x {sharpe:>+6.2f} {slugging:>8.2f}x {sortino:>+7.2f}")

    print("\n" + "="*80)

if __name__ == '__main__':
    main()
