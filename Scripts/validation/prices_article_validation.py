#!/usr/bin/env python3
"""
Validate all empirical claims in the Prices Pillar article.
Runs regressions, Granger causality tests, cross-correlations,
and fetches current readings.
"""

import pandas as pd
import numpy as np
from fredapi import Fred
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

fred = Fred()

print("=" * 70)
print("PRICES ARTICLE EMPIRICAL VALIDATION")
print("=" * 70)

# ============================================
# HELPER: Fetch and compute YoY
# ============================================
def fetch_yoy(series_id, start='1978-01-01'):
    s = fred.get_series(series_id, observation_start=start)
    df = s.to_frame(name='value')
    df['yoy'] = df['value'].pct_change(12, fill_method=None) * 100
    return df

def fetch_level(series_id, start='1978-01-01'):
    s = fred.get_series(series_id, observation_start=start)
    return s.to_frame(name='value')


# ============================================
# CLAIM 1 & 2: Sticky/Flexible CPI predict Core CPI 6 months forward
# Article says: Sticky R² = 0.76, Flexible R² = 0.31 (1980-2025)
# ============================================
print("\n" + "=" * 70)
print("CLAIM 1 & 2: Sticky/Flexible CPI → Core CPI (6-month forward)")
print("=" * 70)

sticky = fetch_level('CORESTICKM159SFRBATL', start='1978-01-01')
flexible = fetch_level('FLEXCPIM159SFRBATL', start='1978-01-01')  # Try flexible
core_cpi = fetch_yoy('CPILFESL', start='1978-01-01')

# Align
df_sf = pd.DataFrame({
    'sticky': sticky['value'],
    'core_cpi_yoy': core_cpi['yoy'],
}).dropna()

# Also try flexible
try:
    flex = fetch_level('FLEXCPIM159SFRBATL', start='1978-01-01')
    df_sf['flexible'] = flex['value']
except:
    # Try alternative
    flex = fetch_level('COREFLEXM159SFRBATL', start='1978-01-01')
    df_sf['flexible'] = flex['value']

df_sf = df_sf.dropna()

# Core CPI 6 months forward
df_sf['core_fwd_6m'] = df_sf['core_cpi_yoy'].shift(-6)
df_sf_clean = df_sf.dropna()

# Trim to 1980+
df_sf_clean = df_sf_clean.loc['1980-01-01':]

# Regression: Core CPI(t+6) ~ Sticky CPI(t)
X_sticky = df_sf_clean[['sticky']].values
X_flex = df_sf_clean[['flexible']].values
y = df_sf_clean['core_fwd_6m'].values

# Sticky
slope_s, intercept_s, r_s, p_s, se_s = stats.linregress(X_sticky.flatten(), y)
r2_sticky = r_s ** 2

# Flexible
slope_f, intercept_f, r_f, p_f, se_f = stats.linregress(X_flex.flatten(), y)
r2_flex = r_f ** 2

print(f"\nSample: {df_sf_clean.index[0].strftime('%Y-%m')} to {df_sf_clean.index[-1].strftime('%Y-%m')}")
print(f"N = {len(df_sf_clean)}")
print(f"\nSticky CPI → Core CPI (t+6):")
print(f"  R² = {r2_sticky:.3f}  (Article claims 0.76)")
print(f"  Coefficient = {slope_s:.3f}")
print(f"  p-value = {p_s:.2e}")
print(f"\nFlexible CPI → Core CPI (t+6):")
print(f"  R² = {r2_flex:.3f}  (Article claims 0.31)")
print(f"  Coefficient = {slope_f:.3f}")
print(f"  p-value = {p_f:.2e}")
print(f"\nSticky/Flexible predictive power ratio: {r2_sticky/r2_flex:.1f}x  (Article claims 2.5x)")


# ============================================
# CLAIM 3 & 4: PPI Granger-causes CPI, not reverse
# Article says: PPI→CPI significant (p<0.001), optimal lag 4-5 months
# CPI→PPI not significant (p=0.18), cross-corr 0.72 at 4.5 months
# ============================================
print("\n" + "=" * 70)
print("CLAIM 3 & 4: PPI Granger-causes CPI")
print("=" * 70)

ppi = fetch_yoy('PPIFIS', start='1978-01-01')
cpi = fetch_yoy('CPIAUCSL', start='1978-01-01')

df_pp = pd.DataFrame({
    'ppi_yoy': ppi['yoy'],
    'cpi_yoy': cpi['yoy'],
}).dropna()
df_pp = df_pp.loc['1980-01-01':]

# Granger causality using statsmodels
from statsmodels.tsa.stattools import grangercausalitytests

print("\nPPI → CPI (does PPI Granger-cause CPI?):")
print("-" * 40)
gc_ppi_cpi = grangercausalitytests(df_pp[['cpi_yoy', 'ppi_yoy']].values, maxlag=8, verbose=False)
for lag in [3, 4, 5, 6]:
    f_stat = gc_ppi_cpi[lag][0]['ssr_ftest'][0]
    p_val = gc_ppi_cpi[lag][0]['ssr_ftest'][1]
    print(f"  Lag {lag}: F={f_stat:.2f}, p={p_val:.4f}")

print("\nCPI → PPI (does CPI Granger-cause PPI?):")
print("-" * 40)
gc_cpi_ppi = grangercausalitytests(df_pp[['ppi_yoy', 'cpi_yoy']].values, maxlag=8, verbose=False)
for lag in [3, 4, 5, 6]:
    f_stat = gc_cpi_ppi[lag][0]['ssr_ftest'][0]
    p_val = gc_cpi_ppi[lag][0]['ssr_ftest'][1]
    print(f"  Lag {lag}: F={f_stat:.2f}, p={p_val:.4f}")

# Cross-correlation
print("\nCross-Correlation (PPI leading CPI):")
print("-" * 40)
max_corr = 0
max_lag = 0
for lag in range(1, 13):
    corr = df_pp['ppi_yoy'].iloc[:-lag].corr(df_pp['cpi_yoy'].iloc[lag:].reset_index(drop=True))
    # Better approach: shift
    shifted_cpi = df_pp['cpi_yoy'].shift(-lag)
    corr = df_pp['ppi_yoy'].corr(shifted_cpi)
    if lag <= 8:
        print(f"  Lag {lag}m: r = {corr:.3f}")
    if corr > max_corr:
        max_corr = corr
        max_lag = lag

print(f"\n  Peak correlation: r = {max_corr:.3f} at lag {max_lag} months")
print(f"  (Article claims 0.72 at 4.5 months)")


# ============================================
# CLAIM 5: Trimmed mean 35-40% lower forecast error (2021-2023)
# ============================================
print("\n" + "=" * 70)
print("CLAIM 5: Trimmed Mean forecast accuracy vs Headline (2021-2023)")
print("=" * 70)

trimmed_pce = fetch_level('PCETRIM12M159SFRBDAL', start='2019-01-01')
core_pce = fetch_yoy('PCEPILFE', start='2019-01-01')
headline_cpi = fetch_yoy('CPIAUCSL', start='2019-01-01')

df_tm = pd.DataFrame({
    'trimmed_pce': trimmed_pce['value'],
    'core_pce_yoy': core_pce['yoy'],
    'headline_cpi_yoy': headline_cpi['yoy'],
}).dropna()

# Core PCE 6 months forward
df_tm['core_pce_fwd_6m'] = df_tm['core_pce_yoy'].shift(-6)
df_tm_clean = df_tm.dropna()

# Focus on 2021-2023
df_tm_eval = df_tm_clean.loc['2021-01-01':'2023-06-01']

if len(df_tm_eval) > 0:
    # MAE: using current reading as "forecast" of 6-month forward core PCE
    mae_headline = np.abs(df_tm_eval['headline_cpi_yoy'] - df_tm_eval['core_pce_fwd_6m']).mean()
    mae_trimmed = np.abs(df_tm_eval['trimmed_pce'] - df_tm_eval['core_pce_fwd_6m']).mean()

    improvement = (mae_headline - mae_trimmed) / mae_headline * 100

    print(f"\nSample: 2021-01 to 2023-06 (N={len(df_tm_eval)})")
    print(f"\nMAE (Headline CPI → Core PCE 6m fwd): {mae_headline:.2f} ppts")
    print(f"MAE (Trimmed Mean → Core PCE 6m fwd):  {mae_trimmed:.2f} ppts")
    print(f"Improvement: {improvement:.1f}%  (Article claims 35-40%)")
else:
    print("  Insufficient data for 2021-2023 evaluation window")


# ============================================
# CURRENT READINGS: Validate all numbers cited in article
# ============================================
print("\n" + "=" * 70)
print("CURRENT READINGS VALIDATION")
print("=" * 70)

# Fetch latest readings
indicators = {
    'Headline CPI YoY': ('CPIAUCSL', 'yoy'),
    'Core CPI YoY': ('CPILFESL', 'yoy'),
    'Core PCE YoY': ('PCEPILFE', 'yoy'),
    'Core Goods CPI YoY': ('CUSR0000SACL1E', 'yoy'),
    'Core Services CPI YoY': ('CUSR0000SASLE', 'yoy'),
    'Shelter CPI YoY': ('CUSR0000SAH1', 'yoy'),
    'Sticky CPI': ('CORESTICKM159SFRBATL', 'level'),
    'PPI Final Demand YoY': ('PPIFIS', 'yoy'),
    'Trimmed Mean PCE 12M': ('PCETRIM12M159SFRBDAL', 'level'),
    '5Y5Y Forward': ('T5YIFR', 'level'),
    'ECI Total Comp YoY': ('ECIALLCIV', 'yoy_quarterly'),
}

for name, (series_id, method) in indicators.items():
    try:
        if method == 'yoy':
            df = fetch_yoy(series_id)
            val = df['yoy'].dropna().iloc[-1]
            date = df['yoy'].dropna().index[-1]
            print(f"  {name}: {val:.1f}%  ({date.strftime('%Y-%m')})")
        elif method == 'level':
            df = fetch_level(series_id)
            val = df['value'].dropna().iloc[-1]
            date = df['value'].dropna().index[-1]
            if '5Y5Y' in name:
                print(f"  {name}: {val:.2f}%  ({date.strftime('%Y-%m-%d')})")
            else:
                print(f"  {name}: {val:.1f}%  ({date.strftime('%Y-%m')})")
        elif method == 'yoy_quarterly':
            df = fetch_level(series_id, start='2020-01-01')
            # ECI is an index, compute YoY from 4 quarters ago
            df['yoy'] = df['value'].pct_change(4, fill_method=None) * 100
            val = df['yoy'].dropna().iloc[-1]
            date = df['yoy'].dropna().index[-1]
            print(f"  {name}: {val:.1f}%  ({date.strftime('%Y-%m')})")
    except Exception as e:
        print(f"  {name}: ERROR - {e}")

# Core PCE 3M annualized
print("\nDerived Metrics:")
core_pce_idx = fred.get_series('PCEPILFE', observation_start='2024-01-01')
mom = core_pce_idx.pct_change(1)
ann3m = ((1 + mom).rolling(3).apply(lambda x: x.prod(), raw=True) ** 4 - 1) * 100
last_3m = ann3m.dropna().iloc[-1]
print(f"  Core PCE 3M Annualized: {last_3m:.1f}%  ({ann3m.dropna().index[-1].strftime('%Y-%m')})")

# Goods-Services spread
goods = fetch_yoy('CUSR0000SACL1E')
services = fetch_yoy('CUSR0000SASLE')
g_last = goods['yoy'].dropna().iloc[-1]
s_last = services['yoy'].dropna().iloc[-1]
print(f"  Goods-Services Spread: {g_last - s_last:.1f} ppts ({g_last:.1f}% - {s_last:.1f}%)")

print("\n" + "=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)
