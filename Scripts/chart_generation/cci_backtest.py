#!/usr/bin/env python3
"""
CCI Backtest & Weight Optimization
====================================
1. Adds RSXFS (Retail Sales Control Group) as card spending proxy (7th component)
2. Backtests CCI regime signals vs forward PCE outcomes (6M, 12M)
3. Tests alternative weight schemes and reports signal quality

Usage:
    python3 cci_backtest.py
"""

import os
import sys
import time
import pandas as pd
import numpy as np
from fredapi import Fred
from itertools import product

# FRED API
fred = Fred(api_key=os.environ.get('FRED_API_KEY', ''))

# Cache to avoid rate limits
_CACHE = {}

def fetch(series_id, start='1998-01-01'):
    if series_id in _CACHE:
        return _CACHE[series_id].copy()
    time.sleep(1.0)
    s = fred.get_series(series_id, observation_start=start)
    _CACHE[series_id] = s
    return s.copy()

def yoy(series):
    return series.pct_change(12, fill_method=None) * 100

def quarterly_to_monthly(series):
    return series.resample('MS').ffill()

def quarterly_yoy(series):
    yy = series.pct_change(4, fill_method=None) * 100
    return yy.resample('MS').ffill()

def target_zscore(series, target, scale):
    return (series - target) / scale


# ============================================
# FETCH ALL COMPONENTS
# ============================================
print("=" * 70)
print("CCI BACKTEST & WEIGHT OPTIMIZATION")
print("=" * 70)

print("\nFetching data from FRED...")

# 1. Real PCE YoY
pce_raw = fetch('PCEC96')
pce = yoy(pce_raw).dropna()
print(f"  Real PCE YoY: {len(pce)} obs, {pce.index[0].strftime('%Y-%m')} to {pce.index[-1].strftime('%Y-%m')}")

# 2. Saving Rate (level)
saving = fetch('PSAVERT').dropna()
print(f"  Saving Rate: {len(saving)} obs, {saving.index[0].strftime('%Y-%m')} to {saving.index[-1].strftime('%Y-%m')}")

# 3. CC Delinquency (quarterly, ffill)
cc_dq_raw = fetch('DRCCLACBS')
cc_dq = quarterly_to_monthly(cc_dq_raw).dropna()
print(f"  CC Delinquency: {len(cc_dq)} obs, {cc_dq.index[0].strftime('%Y-%m')} to {cc_dq.index[-1].strftime('%Y-%m')}")

# 4. UMich Sentiment (level)
umich = fetch('UMCSENT').dropna()
print(f"  UMich Sentiment: {len(umich)} obs, {umich.index[0].strftime('%Y-%m')} to {umich.index[-1].strftime('%Y-%m')}")

# 5. Real DPI YoY
dpi_raw = fetch('DSPIC96')
dpi = yoy(dpi_raw).dropna()
print(f"  Real DPI YoY: {len(dpi)} obs, {dpi.index[0].strftime('%Y-%m')} to {dpi.index[-1].strftime('%Y-%m')}")

# 6. Debt Service Ratio (quarterly, ffill)
dsr_raw = fetch('TDSP')
dsr = quarterly_to_monthly(dsr_raw).dropna()
print(f"  Debt Service Ratio: {len(dsr)} obs, {dsr.index[0].strftime('%Y-%m')} to {dsr.index[-1].strftime('%Y-%m')}")

# 7. NEW: Retail Sales Control Group YoY (proxy for card spending)
rsxfs_raw = fetch('RSXFS')
rsxfs = yoy(rsxfs_raw).dropna()
print(f"  Retail Sales Control YoY: {len(rsxfs)} obs, {rsxfs.index[0].strftime('%Y-%m')} to {rsxfs.index[-1].strftime('%Y-%m')}")


# ============================================
# BUILD ALIGNED DATAFRAME
# ============================================
print("\nBuilding aligned DataFrame...")

df = pd.DataFrame({
    'pce': pce,
    'saving': saving,
    'cc_dq': cc_dq,
    'umich': umich,
    'dpi': dpi,
    'dsr': dsr,
    'rsxfs': rsxfs,
}).loc['2002-01-01':].dropna()

print(f"  Common dates: {len(df)} obs, {df.index[0].strftime('%Y-%m')} to {df.index[-1].strftime('%Y-%m')}")


# ============================================
# Z-SCORES (same target_zscore approach as chart script)
# ============================================
print("\nComputing z-scores...")

z_pce = target_zscore(df['pce'], target=2.5, scale=2.0)
z_saving = target_zscore(df['saving'], target=7.0, scale=3.0)
z_cc_dq = target_zscore(df['cc_dq'], target=3.0, scale=1.5) * -1
z_umich = target_zscore(df['umich'], target=85.0, scale=15.0)
z_dpi = target_zscore(df['dpi'], target=2.5, scale=2.0)
z_dsr = target_zscore(df['dsr'], target=10.0, scale=2.0) * -1
z_rsxfs = target_zscore(df['rsxfs'], target=3.0, scale=3.0)  # Retail sales: 3% YoY = healthy, 3% scale

z_df = pd.DataFrame({
    'z_pce': z_pce,
    'z_saving': z_saving,
    'z_cc_dq': z_cc_dq,
    'z_umich': z_umich,
    'z_dpi': z_dpi,
    'z_dsr': z_dsr,
    'z_rsxfs': z_rsxfs,
})


# ============================================
# DEFINE WEIGHT SCHEMES
# ============================================

weight_schemes = {
    'current_6comp': {
        'desc': 'Current script (6 components, no card spending)',
        'weights': {'z_pce': 0.25, 'z_saving': 0.20, 'z_cc_dq': 0.15,
                    'z_umich': 0.20, 'z_dpi': 0.10, 'z_dsr': 0.10, 'z_rsxfs': 0.00},
    },
    'pillar_doc_7comp': {
        'desc': 'Pillar doc weights (7 components, UMich proxy for CB Exp)',
        'weights': {'z_pce': 0.25, 'z_saving': 0.20, 'z_cc_dq': 0.15,
                    'z_umich': 0.15, 'z_dpi': 0.10, 'z_dsr': 0.10, 'z_rsxfs': 0.05},
    },
    'stress_heavy': {
        'desc': 'Stress-heavy (more weight on delinquency, DSR, less on spending)',
        'weights': {'z_pce': 0.20, 'z_saving': 0.20, 'z_cc_dq': 0.20,
                    'z_umich': 0.15, 'z_dpi': 0.05, 'z_dsr': 0.15, 'z_rsxfs': 0.05},
    },
    'confidence_heavy': {
        'desc': 'Confidence-heavy (more weight on UMich, less on DSR)',
        'weights': {'z_pce': 0.25, 'z_saving': 0.15, 'z_cc_dq': 0.15,
                    'z_umich': 0.25, 'z_dpi': 0.10, 'z_dsr': 0.05, 'z_rsxfs': 0.05},
    },
    'income_focused': {
        'desc': 'Income-focused (DPI + payroll proxy heavier)',
        'weights': {'z_pce': 0.20, 'z_saving': 0.20, 'z_cc_dq': 0.15,
                    'z_umich': 0.10, 'z_dpi': 0.15, 'z_dsr': 0.10, 'z_rsxfs': 0.10},
    },
    'equal_weight': {
        'desc': 'Equal weight (baseline sanity check)',
        'weights': {'z_pce': 1/7, 'z_saving': 1/7, 'z_cc_dq': 1/7,
                    'z_umich': 1/7, 'z_dpi': 1/7, 'z_dsr': 1/7, 'z_rsxfs': 1/7},
    },
}


# ============================================
# COMPUTE CCI FOR EACH SCHEME
# ============================================
print("\nComputing CCI for each weight scheme...")

cci_all = {}
for name, scheme in weight_schemes.items():
    w = scheme['weights']
    cci = sum(w[col] * z_df[col] for col in z_df.columns)
    cci_all[name] = cci
    print(f"  {name}: latest CCI = {cci.iloc[-1]:.3f}")


# ============================================
# FORWARD PCE OUTCOMES
# ============================================
print("\n" + "=" * 70)
print("BACKTEST: CCI Regime vs Forward PCE Outcomes")
print("=" * 70)

# Compute forward PCE change (6M and 12M ahead)
pce_fwd_6m = pce.shift(-6)   # PCE YoY 6 months from now
pce_fwd_12m = pce.shift(-12)  # PCE YoY 12 months from now
pce_chg_6m = pce_fwd_6m - pce  # Change in PCE YoY over next 6M
pce_chg_12m = pce_fwd_12m - pce  # Change in PCE YoY over next 12M

# Also: did PCE go negative within 12M?
pce_min_12m = pce.rolling(12).min().shift(-12)  # Min PCE YoY in next 12M

# NBER recession dates (manual)
recessions = [
    ('2001-03-01', '2001-11-01'),
    ('2007-12-01', '2009-06-01'),
    ('2020-02-01', '2020-04-01'),
]

# Create recession indicator
recession_flag = pd.Series(0, index=df.index)
for start, end in recessions:
    recession_flag.loc[start:end] = 1

# Also: recession within 12M
recession_12m = recession_flag.rolling(12).max().shift(-12)
recession_12m = recession_12m.reindex(df.index)


def regime_label(val):
    if val > 1.0: return 'Boom'
    elif val > 0.5: return 'Healthy'
    elif val > -0.5: return 'Neutral'
    elif val > -1.0: return 'Stressed'
    else: return 'Crisis'


# ============================================
# ANALYSIS FOR EACH WEIGHT SCHEME
# ============================================
results_summary = []

for name, cci in cci_all.items():
    scheme = weight_schemes[name]

    # Align with forward outcomes
    analysis = pd.DataFrame({
        'cci': cci,
        'pce_now': pce.reindex(cci.index),
        'pce_fwd_6m': pce_fwd_6m.reindex(cci.index),
        'pce_fwd_12m': pce_fwd_12m.reindex(cci.index),
        'pce_chg_6m': pce_chg_6m.reindex(cci.index),
        'pce_chg_12m': pce_chg_12m.reindex(cci.index),
        'recession_12m': recession_12m.reindex(cci.index),
    }).dropna()

    analysis['regime'] = analysis['cci'].apply(regime_label)

    print(f"\n{'─' * 60}")
    print(f"SCHEME: {name}")
    print(f"  {scheme['desc']}")
    print(f"  Weights: {scheme['weights']}")
    print(f"  Obs: {len(analysis)}")
    print(f"  Latest CCI: {cci.iloc[-1]:.3f}")
    print(f"  Latest Regime: {regime_label(cci.iloc[-1])}")

    # Regime distribution
    print(f"\n  Regime Distribution:")
    regime_counts = analysis['regime'].value_counts()
    for r in ['Boom', 'Healthy', 'Neutral', 'Stressed', 'Crisis']:
        if r in regime_counts:
            pct = regime_counts[r] / len(analysis) * 100
            print(f"    {r:12s}: {regime_counts[r]:4d} months ({pct:5.1f}%)")

    # Forward PCE by regime
    print(f"\n  Forward PCE Change by Regime:")
    print(f"  {'Regime':12s} | {'N':>4s} | {'6M Fwd PCE Chg':>15s} | {'12M Fwd PCE Chg':>15s} | {'Recession 12M':>14s}")
    print(f"  {'-'*12}-+-{'-'*4}-+-{'-'*15}-+-{'-'*15}-+-{'-'*14}")

    for r in ['Boom', 'Healthy', 'Neutral', 'Stressed', 'Crisis']:
        mask = analysis['regime'] == r
        if mask.sum() == 0:
            continue
        n = mask.sum()
        chg6 = analysis.loc[mask, 'pce_chg_6m'].mean()
        chg12 = analysis.loc[mask, 'pce_chg_12m'].mean()
        rec_pct = analysis.loc[mask, 'recession_12m'].mean() * 100
        print(f"  {r:12s} | {n:4d} | {chg6:+14.2f}pp | {chg12:+14.2f}pp | {rec_pct:13.1f}%")

    # Signal quality metrics
    # 1. Correlation: CCI vs forward PCE change
    corr_6m = analysis['cci'].corr(analysis['pce_chg_6m'])
    corr_12m = analysis['cci'].corr(analysis['pce_chg_12m'])

    # 2. Recession detection: When CCI < -0.5, what % of time is recession within 12M?
    stressed_mask = analysis['cci'] < -0.5
    if stressed_mask.sum() > 0:
        recession_precision = analysis.loc[stressed_mask, 'recession_12m'].mean() * 100
        stressed_count = stressed_mask.sum()
    else:
        recession_precision = 0
        stressed_count = 0

    # 3. Recession recall: When recession within 12M, what % of time is CCI < -0.5?
    recession_mask = analysis['recession_12m'] == 1
    if recession_mask.sum() > 0:
        recession_recall = (analysis.loc[recession_mask, 'cci'] < -0.5).mean() * 100
    else:
        recession_recall = 0

    # 4. Lead time: How many months before recession does CCI first drop below -0.5?
    lead_times = []
    for rec_start, rec_end in recessions:
        rec_start_ts = pd.Timestamp(rec_start)
        if rec_start_ts < analysis.index[0]:
            continue
        # Look back 24 months before recession start
        lookback_start = rec_start_ts - pd.DateOffset(months=24)
        pre_rec = analysis.loc[lookback_start:rec_start_ts, 'cci']
        stressed_dates = pre_rec[pre_rec < -0.5]
        if len(stressed_dates) > 0:
            first_stress = stressed_dates.index[0]
            lead_months = (rec_start_ts - first_stress).days / 30.44
            lead_times.append((rec_start, lead_months))

    print(f"\n  Signal Quality:")
    print(f"    Corr(CCI, 6M fwd PCE chg):  {corr_6m:+.3f}")
    print(f"    Corr(CCI, 12M fwd PCE chg): {corr_12m:+.3f}")
    print(f"    Recession Precision (CCI<-0.5 → recession 12M): {recession_precision:.1f}% (n={stressed_count})")
    print(f"    Recession Recall (recession 12M → CCI<-0.5):    {recession_recall:.1f}%")

    if lead_times:
        print(f"    Lead Times (months before recession CCI first < -0.5):")
        for rec_start, lead in lead_times:
            print(f"      {rec_start}: {lead:.0f} months ahead")

    results_summary.append({
        'name': name,
        'desc': scheme['desc'],
        'latest_cci': cci.iloc[-1],
        'latest_regime': regime_label(cci.iloc[-1]),
        'corr_6m': corr_6m,
        'corr_12m': corr_12m,
        'recession_precision': recession_precision,
        'recession_recall': recession_recall,
        'lead_times': lead_times,
    })


# ============================================
# COMPARISON TABLE
# ============================================
print("\n" + "=" * 70)
print("COMPARISON SUMMARY")
print("=" * 70)

print(f"\n{'Scheme':22s} | {'Latest':>7s} | {'Regime':10s} | {'Corr 6M':>8s} | {'Corr 12M':>9s} | {'Prec':>6s} | {'Recall':>6s}")
print(f"{'-'*22}-+-{'-'*7}-+-{'-'*10}-+-{'-'*8}-+-{'-'*9}-+-{'-'*6}-+-{'-'*6}")

for r in results_summary:
    print(f"{r['name']:22s} | {r['latest_cci']:+7.3f} | {r['latest_regime']:10s} | {r['corr_6m']:+8.3f} | {r['corr_12m']:+9.3f} | {r['recession_precision']:5.1f}% | {r['recession_recall']:5.1f}%")


# ============================================
# COMPONENT CORRELATIONS (which components best predict forward PCE?)
# ============================================
print("\n" + "=" * 70)
print("COMPONENT-LEVEL ANALYSIS: Which z-scores best predict forward PCE?")
print("=" * 70)

fwd = pd.DataFrame({
    'pce_chg_6m': pce_chg_6m.reindex(z_df.index),
    'pce_chg_12m': pce_chg_12m.reindex(z_df.index),
    'recession_12m': recession_12m.reindex(z_df.index),
}).dropna()

common_idx = z_df.index.intersection(fwd.index)

component_names = {
    'z_pce': 'Real PCE YoY',
    'z_saving': 'Saving Rate',
    'z_cc_dq': 'CC Delinquency (inv)',
    'z_umich': 'UMich Sentiment',
    'z_dpi': 'Real DPI YoY',
    'z_dsr': 'Debt Service Ratio (inv)',
    'z_rsxfs': 'Retail Sales Control YoY',
}

print(f"\n{'Component':28s} | {'Corr 6M':>8s} | {'Corr 12M':>9s} | {'Current z':>10s}")
print(f"{'-'*28}-+-{'-'*8}-+-{'-'*9}-+-{'-'*10}")

for col in z_df.columns:
    c6 = z_df.loc[common_idx, col].corr(fwd.loc[common_idx, 'pce_chg_6m'])
    c12 = z_df.loc[common_idx, col].corr(fwd.loc[common_idx, 'pce_chg_12m'])
    curr = z_df[col].iloc[-1]
    label = component_names.get(col, col)
    print(f"{label:28s} | {c6:+8.3f} | {c12:+9.3f} | {curr:+10.3f}")


# ============================================
# SUGGESTED OPTIMAL WEIGHTS (economic logic + empirical)
# ============================================
print("\n" + "=" * 70)
print("SUGGESTED WEIGHTS BASED ON ANALYSIS")
print("=" * 70)

# Compute absolute correlations to inform weighting
abs_corrs = {}
for col in z_df.columns:
    c6 = abs(z_df.loc[common_idx, col].corr(fwd.loc[common_idx, 'pce_chg_6m']))
    c12 = abs(z_df.loc[common_idx, col].corr(fwd.loc[common_idx, 'pce_chg_12m']))
    abs_corrs[col] = (c6 + c12) / 2

total_corr = sum(abs_corrs.values())
empirical_weights = {k: v / total_corr for k, v in abs_corrs.items()}

print("\nPure empirical weights (correlation-driven):")
for col in z_df.columns:
    label = component_names.get(col, col)
    print(f"  {label:28s}: {empirical_weights[col]:.3f}")

# Blended: 60% economic logic (pillar doc) + 40% empirical
pillar_weights = {'z_pce': 0.25, 'z_saving': 0.20, 'z_cc_dq': 0.15,
                  'z_umich': 0.15, 'z_dpi': 0.10, 'z_dsr': 0.10, 'z_rsxfs': 0.05}

blended = {}
for col in z_df.columns:
    blended[col] = round(0.60 * pillar_weights[col] + 0.40 * empirical_weights[col], 3)

# Normalize to sum to 1.0
total_blended = sum(blended.values())
blended = {k: round(v / total_blended, 3) for k, v in blended.items()}

# Adjust to nice round numbers (sum to 1.00)
print("\nBlended weights (60% economic logic + 40% empirical):")
for col in z_df.columns:
    label = component_names.get(col, col)
    doc_w = pillar_weights[col]
    emp_w = empirical_weights[col]
    bl_w = blended[col]
    print(f"  {label:28s}: {bl_w:.3f}  (doc: {doc_w:.2f}, empirical: {emp_w:.3f})")

# Compute CCI with blended weights and show result
cci_blended = sum(blended[col] * z_df[col] for col in z_df.columns)
analysis_bl = pd.DataFrame({
    'cci': cci_blended,
    'pce_chg_6m': pce_chg_6m.reindex(cci_blended.index),
    'pce_chg_12m': pce_chg_12m.reindex(cci_blended.index),
}).dropna()

corr_6m_bl = analysis_bl['cci'].corr(analysis_bl['pce_chg_6m'])
corr_12m_bl = analysis_bl['cci'].corr(analysis_bl['pce_chg_12m'])

print(f"\nBlended weights performance:")
print(f"  Latest CCI: {cci_blended.iloc[-1]:.3f} ({regime_label(cci_blended.iloc[-1])})")
print(f"  Corr(CCI, 6M fwd PCE chg):  {corr_6m_bl:+.3f}")
print(f"  Corr(CCI, 12M fwd PCE chg): {corr_12m_bl:+.3f}")

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
