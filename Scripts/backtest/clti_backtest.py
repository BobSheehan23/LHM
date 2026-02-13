"""
CLTI Backtest: Crypto-Liquidity Transmission Index
===================================================
Tests whether a composite of macro liquidity, US plumbing, and crypto-native
signals has predictive power for BTC forward returns.

Components (what we can build from available data):
  Tier 1 - Macro Tide:
    C1: US M2 momentum (3-month annualized RoC) [FRED: M2SL]
    C2: Dollar momentum, inverted (20-day RoC) [FRED: DTWEXBGS]
  Tier 2 - US Plumbing:
    C3: Net liquidity impulse (4-week RoC of WALCL-TGA-RRP) [FRED]
    C4: Funding stress, inverted (SOFR spread + HY OAS z-score) [NYFED + FRED]
  Tier 3 - Crypto Channels:
    C5: Stablecoin supply momentum (30-day RoC) [DefiLlama API]

  Regime Filter:
    Perp funding rates [NOT AVAILABLE - skip for now]

Missing (noted but excluded):
  - ETF flows (no historical data in DB)
  - Exchange stablecoin reserves (no CryptoQuant API)
  - Foreign M2 (China, EU, Japan, UK - not in DB)
  - Perp funding rates (not in DB)

Methodology: Same as Conks rebuttal (quintile sorts, regime analysis, t-tests)

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
warnings.filterwarnings('ignore')

DB_PATH = '/Users/bob/LHM/Data/databases/Lighthouse_Master.db'


def load_series(conn, series_id):
    """Load a time series from the master DB."""
    df = pd.read_sql(
        "SELECT date, value FROM observations WHERE series_id = ? ORDER BY date",
        conn, params=(series_id,), parse_dates=['date']
    )
    df = df.set_index('date')
    df.columns = [series_id]
    return df


def fetch_btc_history():
    """Fetch BTC-USD daily history from yfinance."""
    print("Fetching BTC-USD history from yfinance...")
    btc = yf.download('BTC-USD', start='2014-01-01', end='2026-02-13', progress=False)
    if isinstance(btc.columns, pd.MultiIndex):
        btc = btc.droplevel(1, axis=1)
    btc = btc[['Close']].rename(columns={'Close': 'BTC'})
    btc.index = pd.to_datetime(btc.index).tz_localize(None)
    print(f"  BTC: {len(btc)} obs, {btc.index.min().date()} to {btc.index.max().date()}")
    return btc


def fetch_stablecoin_history():
    """Fetch stablecoin market cap history from CoinGecko."""
    print("Fetching stablecoin history from CoinGecko...")

    stablecoin_ids = {
        'tether': 'USDT',
        'usd-coin': 'USDC',
    }

    all_data = []

    for coin_id, label in stablecoin_ids.items():
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {'vs_currency': 'usd', 'days': 'max', 'interval': 'daily'}

        try:
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            mc = data.get('market_caps', [])
            df = pd.DataFrame(mc, columns=['timestamp', label])
            df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.normalize()
            df = df.set_index('date')[[label]]
            all_data.append(df)
            print(f"  {label}: {len(df)} obs, {df.index.min().date()} to {df.index.max().date()}")

            time.sleep(2)  # Rate limit
        except Exception as e:
            print(f"  {label} FAILED: {e}")

    if not all_data:
        return None

    combined = pd.concat(all_data, axis=1)
    combined['STABLE_TOTAL'] = combined.sum(axis=1)
    return combined


def fetch_iorb_from_fred(api_key):
    """Fetch IORB (Interest on Reserve Balances) from FRED."""
    print("Fetching IORB from FRED...")

    # Try IORB first (post-July 2021), then IOER (pre-July 2021)
    for series_id in ['IORB', 'IOER']:
        url = f"https://api.stlouisfed.org/fred/series/observations"
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '2014-01-01',
        }
        try:
            resp = requests.get(url, params=params, timeout=30)
            data = resp.json()
            if 'observations' in data and len(data['observations']) > 0:
                df = pd.DataFrame(data['observations'])
                df['date'] = pd.to_datetime(df['date'])
                df['value'] = pd.to_numeric(df['value'], errors='coerce')
                df = df.dropna(subset=['value'])
                df = df.set_index('date')[['value']].rename(columns={'value': series_id})
                print(f"  {series_id}: {len(df)} obs, {df.index.min().date()} to {df.index.max().date()}")
                time.sleep(1)
                yield df
        except Exception as e:
            print(f"  {series_id} failed: {e}")
            time.sleep(1)


def build_iorb_series(api_key):
    """Combine IOER (pre-2021) and IORB (post-2021) into one series."""
    dfs = list(fetch_iorb_from_fred(api_key))
    if not dfs:
        return None
    combined = pd.concat(dfs, axis=1)
    # IORB takes precedence where both exist
    if 'IORB' in combined.columns and 'IOER' in combined.columns:
        combined['IORB_RATE'] = combined['IORB'].fillna(combined['IOER'])
    elif 'IORB' in combined.columns:
        combined['IORB_RATE'] = combined['IORB']
    elif 'IOER' in combined.columns:
        combined['IORB_RATE'] = combined['IOER']
    return combined[['IORB_RATE']]


def zscore_rolling(series, window=504):
    """Rolling z-score with 2-year (504 trading day) window."""
    mean = series.rolling(window, min_periods=126).mean()
    std = series.rolling(window, min_periods=126).std()
    return (series - mean) / std.replace(0, np.nan)


def build_components(conn, btc, stablecoins, iorb, api_key):
    """Build all CLTI components and merge into a single DataFrame."""

    # Load from DB
    m2 = load_series(conn, 'M2SL')
    walcl = load_series(conn, 'WALCL')
    tga = load_series(conn, 'WTREGEN')
    rrp = load_series(conn, 'RRPONTSYD')
    hy_oas = load_series(conn, 'BAMLH0A0HYM2')
    dollar = load_series(conn, 'DTWEXBGS')
    sofr = load_series(conn, 'NYFED_SOFR')

    print("\nBuilding components...")

    # === C1: M2 Momentum (3-month annualized RoC) ===
    # M2 is monthly, need to forward-fill to daily
    m2_daily = m2.resample('D').ffill()
    c1 = (m2_daily['M2SL'].pct_change(63) * 4)  # ~3 months, annualized
    c1.name = 'C1_M2_Momentum'
    print(f"  C1 (M2 Momentum): {c1.dropna().index.min().date()} to {c1.dropna().index.max().date()}")

    # === C2: Dollar Momentum, Inverted (20-day RoC) ===
    c2 = -dollar['DTWEXBGS'].pct_change(20)
    c2.name = 'C2_Dollar_Inv'
    print(f"  C2 (Dollar Inv): {c2.dropna().index.min().date()} to {c2.dropna().index.max().date()}")

    # === C3: Net Liquidity Impulse (4-week RoC) ===
    # Forward-fill weekly series to daily
    walcl_d = walcl.resample('D').ffill()
    tga_d = tga.resample('D').ffill()
    rrp_d = rrp.resample('D').ffill()

    net_liq = walcl_d['WALCL'] - tga_d['WTREGEN'] - rrp_d['RRPONTSYD']
    # WALCL and TGA are in millions, RRP in billions - normalize
    # Actually let's check units
    print(f"    WALCL latest: {walcl_d['WALCL'].dropna().iloc[-1]:,.0f}")
    print(f"    TGA latest: {tga_d['WTREGEN'].dropna().iloc[-1]:,.0f}")
    print(f"    RRP latest: {rrp_d['RRPONTSYD'].dropna().iloc[-1]:,.0f}")

    c3 = net_liq.pct_change(20)  # 4 weeks ≈ 20 trading days
    c3.name = 'C3_NetLiq_Impulse'
    print(f"  C3 (Net Liq Impulse): {c3.dropna().index.min().date()} to {c3.dropna().index.max().date()}")

    # === C4: Funding Stress, Inverted ===
    # SOFR - IORB spread (inverted: positive = stress = bad)
    # Plus HY OAS z-score (inverted: high spreads = bad)

    if iorb is not None and not iorb.empty:
        sofr_iorb = pd.merge(sofr, iorb, left_index=True, right_index=True, how='inner')
        sofr_spread = sofr_iorb['NYFED_SOFR'] - sofr_iorb['IORB_RATE']
        sofr_spread_z = zscore_rolling(sofr_spread)
    else:
        print("  WARNING: No IORB data, using SOFR level z-score as proxy")
        sofr_spread_z = zscore_rolling(sofr['NYFED_SOFR'])

    hy_z = zscore_rolling(hy_oas['BAMLH0A0HYM2'])

    # Combine: both inverted (high stress = negative signal)
    # Align on common dates
    c4_df = pd.DataFrame({
        'sofr_z': -sofr_spread_z,  # Inverted: less stress = positive
        'hy_z': -hy_z,              # Inverted: tighter spreads = positive
    })
    c4 = 0.5 * c4_df['sofr_z'] + 0.5 * c4_df['hy_z']
    c4.name = 'C4_Funding_Stress_Inv'
    print(f"  C4 (Funding Stress Inv): {c4.dropna().index.min().date()} to {c4.dropna().index.max().date()}")

    # === C5: Stablecoin Supply Momentum (30-day RoC) ===
    if stablecoins is not None and 'STABLE_TOTAL' in stablecoins.columns:
        c5 = stablecoins['STABLE_TOTAL'].pct_change(30)
        c5.name = 'C5_Stablecoin_Momentum'
        print(f"  C5 (Stablecoin Mom): {c5.dropna().index.min().date()} to {c5.dropna().index.max().date()}")
    else:
        c5 = pd.Series(dtype=float, name='C5_Stablecoin_Momentum')
        print("  C5 (Stablecoin Mom): NOT AVAILABLE")

    # === Merge everything ===
    components = pd.DataFrame({
        'BTC': btc['BTC'],
        'C1_M2_Momentum': c1,
        'C2_Dollar_Inv': c2,
        'C3_NetLiq_Impulse': c3,
        'C4_Funding_Stress_Inv': c4,
    })

    if not c5.empty:
        components['C5_Stablecoin_Momentum'] = c5

    return components


def compute_clti(df, has_c5=True):
    """Compute the CLTI composite from z-scored components."""

    # Z-score each component
    comp_cols = ['C1_M2_Momentum', 'C2_Dollar_Inv', 'C3_NetLiq_Impulse', 'C4_Funding_Stress_Inv']
    if has_c5 and 'C5_Stablecoin_Momentum' in df.columns:
        comp_cols.append('C5_Stablecoin_Momentum')

    z_df = pd.DataFrame(index=df.index)
    for col in comp_cols:
        z_df[f'z_{col}'] = zscore_rolling(df[col])

    # Weights
    if has_c5 and 'C5_Stablecoin_Momentum' in df.columns:
        # 5-component version
        weights = {
            'z_C1_M2_Momentum': 0.25,        # Tier 1: Macro
            'z_C2_Dollar_Inv': 0.20,          # Tier 1: Macro
            'z_C3_NetLiq_Impulse': 0.20,      # Tier 2: Plumbing
            'z_C4_Funding_Stress_Inv': 0.15,  # Tier 2: Plumbing
            'z_C5_Stablecoin_Momentum': 0.20, # Tier 3: Crypto
        }
    else:
        # 4-component version (no stablecoins)
        weights = {
            'z_C1_M2_Momentum': 0.30,
            'z_C2_Dollar_Inv': 0.25,
            'z_C3_NetLiq_Impulse': 0.25,
            'z_C4_Funding_Stress_Inv': 0.20,
        }

    clti = pd.Series(0.0, index=df.index)
    for col, w in weights.items():
        if col in z_df.columns:
            clti += w * z_df[col]

    return clti, z_df


def forward_returns(prices, horizons=[5, 10, 21, 63]):
    """Compute forward returns at various horizons."""
    fwd = pd.DataFrame(index=prices.index)
    for h in horizons:
        fwd[f'fwd_{h}d'] = prices.shift(-h) / prices - 1
    return fwd


def quintile_analysis(clti, fwd_returns, horizon_col, label="CLTI"):
    """Quintile sort analysis."""
    df = pd.DataFrame({
        'clti': clti,
        'fwd': fwd_returns[horizon_col]
    }).dropna()

    if len(df) < 50:
        print(f"  Insufficient data for quintile analysis ({len(df)} obs)")
        return None

    df['quintile'] = pd.qcut(df['clti'], 5, labels=['Q1(Low)', 'Q2', 'Q3', 'Q4', 'Q5(High)'])

    results = df.groupby('quintile')['fwd'].agg(['mean', 'std', 'count'])
    results['mean_pct'] = results['mean'] * 100
    results['se'] = results['std'] / np.sqrt(results['count'])

    # Q5-Q1 spread test
    q5 = df[df['quintile'] == 'Q5(High)']['fwd']
    q1 = df[df['quintile'] == 'Q1(Low)']['fwd']
    t_stat, p_val = stats.ttest_ind(q5, q1, equal_var=False)
    spread = (q5.mean() - q1.mean()) * 100

    return {
        'table': results,
        'spread': spread,
        't_stat': t_stat,
        'p_val': p_val,
        'n_total': len(df),
    }


def regime_analysis(clti, fwd_returns, horizon_col, thresholds=(-0.5, 0.5)):
    """Regime analysis (Scarce / Neutral / Ample)."""
    df = pd.DataFrame({
        'clti': clti,
        'fwd': fwd_returns[horizon_col]
    }).dropna()

    if len(df) < 50:
        print(f"  Insufficient data for regime analysis ({len(df)} obs)")
        return None

    conditions = [
        df['clti'] < thresholds[0],
        (df['clti'] >= thresholds[0]) & (df['clti'] <= thresholds[1]),
        df['clti'] > thresholds[1],
    ]
    labels = ['Contracting', 'Neutral', 'Expanding']
    df['regime'] = np.select(conditions, labels, default='Neutral')

    results = df.groupby('regime')['fwd'].agg(['mean', 'std', 'count'])
    results['mean_pct'] = results['mean'] * 100

    # Expanding vs Contracting spread
    expanding = df[df['regime'] == 'Expanding']['fwd']
    contracting = df[df['regime'] == 'Contracting']['fwd']

    if len(expanding) > 5 and len(contracting) > 5:
        t_stat, p_val = stats.ttest_ind(expanding, contracting, equal_var=False)
        spread = (expanding.mean() - contracting.mean()) * 100
    else:
        t_stat, p_val, spread = np.nan, np.nan, np.nan

    return {
        'table': results,
        'spread': spread,
        't_stat': t_stat,
        'p_val': p_val,
        'n_total': len(df),
    }


def extreme_decile_analysis(clti, fwd_returns, horizon_col):
    """Top/Bottom 10% extreme analysis."""
    df = pd.DataFrame({
        'clti': clti,
        'fwd': fwd_returns[horizon_col]
    }).dropna()

    if len(df) < 50:
        return None

    bottom_10 = df['clti'].quantile(0.10)
    top_10 = df['clti'].quantile(0.90)

    bottom = df[df['clti'] <= bottom_10]['fwd']
    middle = df[(df['clti'] > bottom_10) & (df['clti'] < top_10)]['fwd']
    top = df[df['clti'] >= top_10]['fwd']

    if len(top) > 5 and len(bottom) > 5:
        t_stat, p_val = stats.ttest_ind(top, bottom, equal_var=False)
        spread = (top.mean() - bottom.mean()) * 100
    else:
        t_stat, p_val, spread = np.nan, np.nan, np.nan

    return {
        'bottom_10': {'mean': bottom.mean() * 100, 'n': len(bottom)},
        'middle_80': {'mean': middle.mean() * 100, 'n': len(middle)},
        'top_10': {'mean': top.mean() * 100, 'n': len(top)},
        'spread': spread,
        't_stat': t_stat,
        'p_val': p_val,
    }


def rolling_correlation(clti, btc_returns, window=252):
    """Rolling correlation stability check."""
    df = pd.DataFrame({
        'clti': clti,
        'btc_ret': btc_returns
    }).dropna()

    rolling_corr = df['clti'].rolling(window, min_periods=63).corr(df['btc_ret'])

    return {
        'mean': rolling_corr.mean(),
        'pct_positive': (rolling_corr > 0).mean() * 100,
        'min': rolling_corr.min(),
        'max': rolling_corr.max(),
    }


def print_results(label, quintile_res, regime_res, extreme_res, corr_res):
    """Pretty-print all results."""
    print(f"\n{'='*70}")
    print(f"  {label}")
    print(f"{'='*70}")

    if quintile_res:
        print(f"\n  QUINTILE ANALYSIS (n={quintile_res['n_total']})")
        print(f"  {'─'*50}")
        for idx, row in quintile_res['table'].iterrows():
            print(f"    {idx:10s}  {row['mean_pct']:+7.2f}%   (n={int(row['count'])})")
        print(f"  {'─'*50}")
        print(f"    Q5-Q1 Spread: {quintile_res['spread']:+.2f}%")
        print(f"    t-stat: {quintile_res['t_stat']:.2f}, p-value: {quintile_res['p_val']:.6f}")
        sig = "***" if quintile_res['p_val'] < 0.001 else ("**" if quintile_res['p_val'] < 0.01 else ("*" if quintile_res['p_val'] < 0.05 else "n.s."))
        print(f"    Significance: {sig}")

    if regime_res:
        print(f"\n  REGIME ANALYSIS (n={regime_res['n_total']})")
        print(f"  {'─'*50}")
        for idx, row in regime_res['table'].iterrows():
            print(f"    {idx:12s}  {row['mean_pct']:+7.2f}%   (n={int(row['count'])})")
        print(f"  {'─'*50}")
        print(f"    Expanding-Contracting Spread: {regime_res['spread']:+.2f}%")
        if not np.isnan(regime_res['t_stat']):
            print(f"    t-stat: {regime_res['t_stat']:.2f}, p-value: {regime_res['p_val']:.6f}")

    if extreme_res:
        print(f"\n  EXTREME DECILE ANALYSIS")
        print(f"  {'─'*50}")
        print(f"    Bottom 10%:  {extreme_res['bottom_10']['mean']:+7.2f}%  (n={extreme_res['bottom_10']['n']})")
        print(f"    Middle 80%:  {extreme_res['middle_80']['mean']:+7.2f}%  (n={extreme_res['middle_80']['n']})")
        print(f"    Top 10%:     {extreme_res['top_10']['mean']:+7.2f}%  (n={extreme_res['top_10']['n']})")
        print(f"  {'─'*50}")
        print(f"    Top-Bottom Spread: {extreme_res['spread']:+.2f}%")
        if not np.isnan(extreme_res['t_stat']):
            print(f"    t-stat: {extreme_res['t_stat']:.2f}, p-value: {extreme_res['p_val']:.6f}")

    if corr_res:
        print(f"\n  ROLLING CORRELATION (1-year window)")
        print(f"  {'─'*50}")
        print(f"    Mean:          {corr_res['mean']:+.3f}")
        print(f"    % Positive:    {corr_res['pct_positive']:.1f}%")
        print(f"    Range:         [{corr_res['min']:+.3f}, {corr_res['max']:+.3f}]")


def main():
    print("=" * 70)
    print("  CLTI BACKTEST: Crypto-Liquidity Transmission Index")
    print("  Lighthouse Macro | 2026-02-12")
    print("=" * 70)

    # Load API key
    import sys
    sys.path.insert(0, '/Users/bob/LHM/Scripts/data_pipeline/lighthouse')
    from config import API_KEYS
    fred_key = API_KEYS.get('FRED', '')

    # Connect to DB
    conn = sqlite3.connect(DB_PATH)

    # Fetch external data
    btc = fetch_btc_history()
    stablecoins = fetch_stablecoin_history()
    iorb = build_iorb_series(fred_key) if fred_key else None

    # Build components
    components = build_components(conn, btc, stablecoins, iorb, fred_key)

    # Check what we have
    print(f"\nMerged dataset: {len(components)} rows")
    print(f"Date range: {components.index.min().date()} to {components.index.max().date()}")
    print(f"\nData availability:")
    for col in components.columns:
        valid = components[col].dropna()
        if len(valid) > 0:
            print(f"  {col}: {len(valid)} obs ({valid.index.min().date()} to {valid.index.max().date()})")
        else:
            print(f"  {col}: NO DATA")

    has_c5 = 'C5_Stablecoin_Momentum' in components.columns and components['C5_Stablecoin_Momentum'].dropna().shape[0] > 100

    # Compute CLTI
    clti, z_components = compute_clti(components, has_c5=has_c5)
    clti.name = 'CLTI'

    valid_clti = clti.dropna()
    print(f"\nCLTI computed: {len(valid_clti)} valid observations")
    print(f"  Range: {valid_clti.index.min().date()} to {valid_clti.index.max().date()}")
    print(f"  Mean: {valid_clti.mean():.3f}, Std: {valid_clti.std():.3f}")
    print(f"  Current value: {valid_clti.iloc[-1]:.3f}")

    # Forward returns
    btc_prices = components['BTC'].dropna()
    fwd = forward_returns(btc_prices)
    btc_21d_ret = btc_prices.pct_change(21)

    # ===== RUN ALL TESTS =====

    horizons = {
        'fwd_5d': '1-Week Forward',
        'fwd_10d': '2-Week Forward',
        'fwd_21d': '1-Month Forward',
        'fwd_63d': '3-Month Forward',
    }

    print("\n")
    print("#" * 70)
    print("  RESULTS: FULL CLTI COMPOSITE")
    print("#" * 70)

    for horizon_col, horizon_label in horizons.items():
        label = f"CLTI → BTC {horizon_label} Returns"

        q_res = quintile_analysis(clti, fwd, horizon_col, "CLTI")
        r_res = regime_analysis(clti, fwd, horizon_col)
        e_res = extreme_decile_analysis(clti, fwd, horizon_col)
        c_res = rolling_correlation(clti, btc_21d_ret) if horizon_col == 'fwd_21d' else None

        print_results(label, q_res, r_res, e_res, c_res)

    # ===== TEST INDIVIDUAL COMPONENTS =====

    print("\n\n")
    print("#" * 70)
    print("  RESULTS: INDIVIDUAL COMPONENT TESTS (1-Month Forward)")
    print("#" * 70)

    comp_names = {
        'C1_M2_Momentum': 'C1: M2 Momentum',
        'C2_Dollar_Inv': 'C2: Dollar (Inverted)',
        'C3_NetLiq_Impulse': 'C3: Net Liquidity Impulse',
        'C4_Funding_Stress_Inv': 'C4: Funding Stress (Inverted)',
    }
    if has_c5:
        comp_names['C5_Stablecoin_Momentum'] = 'C5: Stablecoin Momentum'

    for col, name in comp_names.items():
        if col in components.columns:
            comp_z = zscore_rolling(components[col])
            q_res = quintile_analysis(comp_z, fwd, 'fwd_21d', name)
            r_res = regime_analysis(comp_z, fwd, 'fwd_21d')
            e_res = extreme_decile_analysis(comp_z, fwd, 'fwd_21d')
            print_results(name, q_res, r_res, e_res, None)

    # ===== 4-COMPONENT VERSION (without stablecoins, longer history) =====

    print("\n\n")
    print("#" * 70)
    print("  RESULTS: 4-COMPONENT CLTI (No Stablecoins, Longer History)")
    print("#" * 70)

    clti_4, _ = compute_clti(components, has_c5=False)
    clti_4.name = 'CLTI_4comp'

    valid_4 = clti_4.dropna()
    print(f"\n  4-Component CLTI: {len(valid_4)} valid obs")
    print(f"  Range: {valid_4.index.min().date()} to {valid_4.index.max().date()}")

    for horizon_col, horizon_label in horizons.items():
        label = f"CLTI (4-comp) → BTC {horizon_label} Returns"
        q_res = quintile_analysis(clti_4, fwd, horizon_col)
        r_res = regime_analysis(clti_4, fwd, horizon_col)
        e_res = extreme_decile_analysis(clti_4, fwd, horizon_col)
        print_results(label, q_res, r_res, e_res, None)

    # ===== MONOTONICITY CHECK =====

    print("\n\n")
    print("#" * 70)
    print("  MONOTONICITY CHECK")
    print("#" * 70)

    for horizon_col, horizon_label in horizons.items():
        df_check = pd.DataFrame({'clti': clti, 'fwd': fwd[horizon_col]}).dropna()
        if len(df_check) < 50:
            continue
        df_check['quintile'] = pd.qcut(df_check['clti'], 5, labels=[1, 2, 3, 4, 5])
        means = df_check.groupby('quintile')['fwd'].mean()
        is_monotonic = all(means.iloc[i] <= means.iloc[i+1] for i in range(len(means)-1))
        print(f"  {horizon_label}: {'MONOTONIC ✓' if is_monotonic else 'NOT MONOTONIC ✗'}")
        print(f"    Q1={means.iloc[0]*100:+.2f}%  Q2={means.iloc[1]*100:+.2f}%  Q3={means.iloc[2]*100:+.2f}%  Q4={means.iloc[3]*100:+.2f}%  Q5={means.iloc[4]*100:+.2f}%")

    conn.close()

    print("\n\n" + "=" * 70)
    print("  BACKTEST COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    main()
