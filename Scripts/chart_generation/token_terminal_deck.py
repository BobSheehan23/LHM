#!/usr/bin/env python3
"""
TOKEN TERMINAL x LIGHTHOUSE MACRO - Meeting Deck Charts
========================================================
Generates institutional-quality charts combining Token Terminal
fundamental data with Lighthouse Macro indicators.

Output: /Users/bob/LHM/Outputs/token_terminal_deck/
"""

import sys
sys.path.insert(0, '/Users/bob/LHM/Scripts/utilities')

import sqlite3
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch
from pathlib import Path
from datetime import datetime, timedelta

# LHM Style
from lighthouse_chart_style import (
    LIGHTHOUSE_COLORS as C,
    apply_lighthouse_style,
    hex_to_rgba
)

DB = Path('/Users/bob/LHM/Data/databases/Lighthouse_Master.db')
OUT = Path('/Users/bob/LHM/Outputs/token_terminal_deck')
OUT.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB)


def get_scores():
    """Get latest protocol scores."""
    df = pd.read_sql("""
        SELECT * FROM crypto_scores
        WHERE date = (SELECT MAX(date) FROM crypto_scores)
        ORDER BY overall_score DESC
    """, conn)
    return df


def get_metric_ts(metric_id, project_ids=None, days=180):
    """Get time series for a metric."""
    cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    q = f"SELECT project_id, date, value FROM crypto_metrics WHERE metric_id=? AND date>=?"
    params = [metric_id, cutoff]
    if project_ids:
        placeholders = ','.join(['?'] * len(project_ids))
        q += f" AND project_id IN ({placeholders})"
        params.extend(project_ids)
    q += " ORDER BY date"
    return pd.read_sql(q, conn, params=params)


def get_macro_ts(series_id, days=365):
    """Get macro time series."""
    cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    df = pd.read_sql(
        "SELECT date, value FROM observations WHERE series_id=? AND date>=? ORDER BY date",
        conn, params=[series_id, cutoff]
    )
    df['date'] = pd.to_datetime(df['date'])
    return df


# =========================================================================
# CHART 1: Protocol Scoring Matrix (Heatmap-style)
# =========================================================================
def chart_1_scoring_matrix():
    df = get_scores()
    df = df[df['overall_score'] > 0].head(20)

    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor('white')

    protocols = df['name'].fillna(df['project_id']).tolist()
    fin = df['financial_score'].fillna(0).tolist()
    use = df['usage_score'].fillna(0).tolist()
    val = df['valuation_score'].fillna(0).tolist()
    total = df['overall_score'].fillna(0).tolist()

    y = np.arange(len(protocols))
    bar_h = 0.22

    ax.barh(y + bar_h, fin, bar_h, label='Financial', color=C['ocean_blue'], alpha=0.9)
    ax.barh(y, use, bar_h, label='Usage', color=C['teal_green'], alpha=0.9)
    ax.barh(y - bar_h, val, bar_h, label='Valuation', color=C['dusk_orange'], alpha=0.9)

    # Add total score labels
    for i, t in enumerate(total):
        ax.text(max(fin[i], use[i], val[i]) + 2, y[i], f'{t}',
                va='center', fontsize=9, fontweight='bold', color='#333')

    ax.set_yticks(y)
    ax.set_yticklabels(protocols, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel('Score', fontsize=10)
    ax.legend(loc='lower right', fontsize=9, framealpha=0.9)

    apply_lighthouse_style(ax, 'LHM Protocol Scoring Matrix',
                          subtitle='Token Terminal Fundamentals | 24-Point System',
                          primary_side='left')
    ax.set_xlim(0, 110)

    # Add tier color bars on left
    for i, row in df.iterrows():
        idx = list(df.index).index(i)
        verdict = row.get('verdict', '')
        if 'TIER 1' in str(verdict):
            color = C['teal_green']
        elif 'TIER 2' in str(verdict):
            color = C['ocean_blue']
        elif 'NEUTRAL' in str(verdict):
            color = C['neutral_gray']
        else:
            color = C['pure_red']
        ax.barh(y[idx], 1.5, 0.7, left=-3, color=color, alpha=0.8)

    fig.tight_layout()
    fig.savefig(OUT / '01_scoring_matrix.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor=C['ocean_blue'])
    plt.close()
    print('  [1] Scoring matrix')


# =========================================================================
# CHART 2: Revenue vs P/F Scatter (Valuation Map)
# =========================================================================
def chart_2_valuation_map():
    df = get_scores()
    df = df[(df['ann_revenue'] > 0) & (df['pf_ratio'] > 0) & (df['pf_ratio'] < 10000)]
    df['name'] = df['name'].fillna(df['project_id'])

    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('white')

    # Color by verdict
    colors = []
    for v in df['verdict']:
        v = str(v)
        if 'TIER 1' in v:
            colors.append(C['teal_green'])
        elif 'TIER 2' in v:
            colors.append(C['ocean_blue'])
        elif 'NEUTRAL' in v:
            colors.append(C['neutral_gray'])
        else:
            colors.append(C['pure_red'])

    # Size by FDV
    sizes = np.clip(df['fdv'].fillna(1e8) / 1e8, 20, 500)

    scatter = ax.scatter(df['ann_revenue'] / 1e6, df['pf_ratio'],
                        c=colors, s=sizes, alpha=0.7, edgecolors='#333', linewidth=0.5)

    # Label key protocols
    for _, row in df.iterrows():
        if row['ann_revenue'] > 5e6 or row['pf_ratio'] < 5 or row['overall_score'] >= 80:
            ax.annotate(row['name'], (row['ann_revenue'] / 1e6, row['pf_ratio']),
                       fontsize=7, ha='left', va='bottom',
                       xytext=(5, 5), textcoords='offset points')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Annualized Revenue ($M)', fontsize=10)
    ax.set_ylabel('P/F Ratio (FDV / Fees)', fontsize=10)

    # Add "cheap + high rev" quadrant shading
    ax.axhline(y=10, color=C['dusk_orange'], linestyle='--', alpha=0.5, linewidth=1)
    ax.axvline(x=10, color=C['dusk_orange'], linestyle='--', alpha=0.5, linewidth=1)
    ax.text(100, 3, 'VALUE ZONE\nHigh Rev + Low P/F', fontsize=8,
            color=C['teal_green'], alpha=0.6, fontweight='bold', ha='center')

    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor=C['teal_green'], markersize=10, label='Tier 1 (Accumulate)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=C['ocean_blue'], markersize=10, label='Tier 2 (Hold)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=C['neutral_gray'], markersize=10, label='Neutral'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=C['pure_red'], markersize=10, label='Avoid'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=8, framealpha=0.9)

    apply_lighthouse_style(ax, 'Protocol Valuation Map',
                          subtitle='Revenue vs P/F Ratio | Size = FDV | Color = LHM Verdict',
                          primary_side='left')

    fig.tight_layout()
    fig.savefig(OUT / '02_valuation_map.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor=C['ocean_blue'])
    plt.close()
    print('  [2] Valuation map')


# =========================================================================
# CHART 3: Revenue Trends (Top Protocols)
# =========================================================================
def chart_3_revenue_trends():
    top = get_scores().head(8)['project_id'].tolist()
    df = get_metric_ts('revenue', top, days=180)
    df['date'] = pd.to_datetime(df['date'])

    # Get names
    names = dict(conn.execute(
        "SELECT project_id, name FROM crypto_meta").fetchall())

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')

    palette = [C['ocean_blue'], C['dusk_orange'], C['teal_green'],
               C['hot_magenta'], C['electric_cyan'], '#8B5CF6', '#F59E0B', '#EC4899']

    for i, pid in enumerate(top):
        sub = df[df['project_id'] == pid].copy()
        if sub.empty:
            continue
        # 7-day rolling average for smoothing
        sub = sub[['date', 'value']].set_index('date').resample('W').mean().reset_index()
        label = names.get(pid, pid)
        ax.plot(sub['date'], sub['value'] / 1e6, color=palette[i % len(palette)],
                linewidth=1.8, label=label, alpha=0.85)

    ax.set_ylabel('Weekly Revenue ($M)', fontsize=10)
    ax.legend(loc='upper left', fontsize=8, ncol=2, framealpha=0.9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:.1f}M'))

    apply_lighthouse_style(ax, 'Protocol Revenue Trends (6M)',
                          subtitle='Token Terminal | Weekly Avg | Top 8 by LHM Score')

    fig.tight_layout()
    fig.savefig(OUT / '03_revenue_trends.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor=C['ocean_blue'])
    plt.close()
    print('  [3] Revenue trends')


# =========================================================================
# CHART 4: DAU Trends (Top Protocols)
# =========================================================================
def chart_4_dau_trends():
    top = get_scores().head(8)['project_id'].tolist()
    df = get_metric_ts('user_dau', top, days=180)
    df['date'] = pd.to_datetime(df['date'])

    names = dict(conn.execute(
        "SELECT project_id, name FROM crypto_meta").fetchall())

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')

    palette = [C['ocean_blue'], C['dusk_orange'], C['teal_green'],
               C['hot_magenta'], C['electric_cyan'], '#8B5CF6', '#F59E0B', '#EC4899']

    for i, pid in enumerate(top):
        sub = df[df['project_id'] == pid].copy()
        if sub.empty:
            continue
        sub = sub[['date', 'value']].set_index('date').resample('W').mean().reset_index()
        label = names.get(pid, pid)
        ax.plot(sub['date'], sub['value'] / 1e3, color=palette[i % len(palette)],
                linewidth=1.8, label=label, alpha=0.85)

    ax.set_ylabel('Daily Active Users (K)', fontsize=10)
    ax.legend(loc='upper left', fontsize=8, ncol=2, framealpha=0.9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0f}K'))

    apply_lighthouse_style(ax, 'Protocol DAU Trends (6M)',
                          subtitle='Token Terminal | Weekly Avg | Top 8 by LHM Score')

    fig.tight_layout()
    fig.savefig(OUT / '04_dau_trends.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor=C['ocean_blue'])
    plt.close()
    print('  [4] DAU trends')


# =========================================================================
# CHART 5: Macro Overlay - RRP + NFCI + HY OAS (Crypto Context)
# =========================================================================
def chart_5_macro_liquidity():
    rrp = get_macro_ts('RRPONTSYD', 730)
    nfci = get_macro_ts('NFCI', 730)
    hy = get_macro_ts('BAMLH0A0HYM2', 730)
    vix = get_macro_ts('VIXCLS', 730)

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.patch.set_facecolor('white')

    # RRP
    ax = axes[0, 0]
    if not rrp.empty:
        ax.fill_between(rrp['date'], rrp['value'], alpha=0.3, color=C['ocean_blue'])
        ax.plot(rrp['date'], rrp['value'], color=C['ocean_blue'], linewidth=1.5)
        ax.axhline(200, color=C['pure_red'], linestyle='--', alpha=0.5, linewidth=1)
        ax.text(rrp['date'].iloc[-1], 200, 'Buffer Exhausted', fontsize=7,
                color=C['pure_red'], va='bottom', ha='right')
    apply_lighthouse_style(ax, 'Reverse Repo ($B)', subtitle='Fed Liquidity Buffer',
                          primary_side='left')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:.0f}B'))

    # NFCI
    ax = axes[0, 1]
    if not nfci.empty:
        ax.fill_between(nfci['date'], nfci['value'], alpha=0.3,
                        color=np.where(nfci['value'] > 0, C['pure_red'], C['teal_green']))
        ax.plot(nfci['date'], nfci['value'], color=C['ocean_blue'], linewidth=1.5)
        ax.axhline(0, color='#333', linewidth=0.8)
    apply_lighthouse_style(ax, 'Financial Conditions (NFCI)',
                          subtitle='Negative = Loose | Positive = Tight',
                          primary_side='left')

    # HY OAS
    ax = axes[1, 0]
    if not hy.empty:
        ax.fill_between(hy['date'], hy['value'], alpha=0.3, color=C['dusk_orange'])
        ax.plot(hy['date'], hy['value'], color=C['dusk_orange'], linewidth=1.5)
        ax.axhline(3, color=C['pure_red'], linestyle='--', alpha=0.5, linewidth=1)
        ax.text(hy['date'].iloc[-1], 3, 'Complacency', fontsize=7,
                color=C['pure_red'], va='bottom', ha='right')
    apply_lighthouse_style(ax, 'HY Credit Spreads (OAS)', subtitle='Risk Appetite Proxy',
                          primary_side='left')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0f}bps'))

    # VIX
    ax = axes[1, 1]
    if not vix.empty:
        ax.fill_between(vix['date'], vix['value'], alpha=0.3, color=C['hot_magenta'])
        ax.plot(vix['date'], vix['value'], color=C['hot_magenta'], linewidth=1.5)
        ax.axhline(20, color=C['dusk_orange'], linestyle='--', alpha=0.5, linewidth=1)
    apply_lighthouse_style(ax, 'VIX (Implied Volatility)', subtitle='Fear Gauge',
                          primary_side='left')

    fig.suptitle('Macro Liquidity Dashboard', fontsize=16, fontweight='bold',
                color='#333', y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / '05_macro_liquidity.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor=C['ocean_blue'])
    plt.close()
    print('  [5] Macro liquidity dashboard')


# =========================================================================
# CHART 6: Sector Health Summary
# =========================================================================
def chart_6_sector_health():
    df = get_scores()

    # Group by sector
    sectors = df.groupby('sector').agg({
        'overall_score': 'mean',
        'financial_score': 'mean',
        'usage_score': 'mean',
        'valuation_score': 'mean',
        'ann_revenue': 'sum',
        'project_id': 'count'
    }).rename(columns={'project_id': 'count'}).sort_values('overall_score', ascending=True)

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')

    y = np.arange(len(sectors))
    colors = [C['teal_green'] if s >= 70 else C['ocean_blue'] if s >= 55
              else C['dusk_orange'] if s >= 40 else C['pure_red']
              for s in sectors['overall_score']]

    bars = ax.barh(y, sectors['overall_score'], color=colors, alpha=0.85, edgecolor='#333', linewidth=0.5)

    # Add score + count labels
    for i, (score, count) in enumerate(zip(sectors['overall_score'], sectors['count'])):
        ax.text(score + 1, y[i], f'{score:.0f} ({count} protocols)',
                va='center', fontsize=9, color='#333')

    ax.set_yticks(y)
    ax.set_yticklabels([s.replace('_', ' ').title() if s else 'Uncategorized'
                        for s in sectors.index], fontsize=9)
    ax.set_xlim(0, 100)
    ax.axvline(55, color=C['dusk_orange'], linestyle='--', alpha=0.4, linewidth=1)
    ax.axvline(70, color=C['teal_green'], linestyle='--', alpha=0.4, linewidth=1)

    apply_lighthouse_style(ax, 'Sector Health Summary',
                          subtitle='Avg LHM Score by Sector | Token Terminal Fundamentals',
                          primary_side='left')

    fig.tight_layout()
    fig.savefig(OUT / '06_sector_health.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor=C['ocean_blue'])
    plt.close()
    print('  [6] Sector health')


# =========================================================================
# CHART 7: Subsidy Score (Token Incentives / Revenue) - Who's Real
# =========================================================================
def chart_7_subsidy():
    df = get_scores()
    df = df[df['ann_revenue'] > 0].copy()
    df['name'] = df['name'].fillna(df['project_id'])
    df['subsidy'] = df['subsidy_score'].fillna(0)
    df = df.sort_values('subsidy', ascending=True).head(20)

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor('white')

    y = np.arange(len(df))
    colors = [C['teal_green'] if s < 50 else C['dusk_orange'] if s < 100
              else C['pure_red'] for s in df['subsidy']]

    ax.barh(y, df['subsidy'], color=colors, alpha=0.85, edgecolor='#333', linewidth=0.5)

    ax.set_yticks(y)
    ax.set_yticklabels(df['name'].tolist(), fontsize=9)
    ax.axvline(100, color=C['pure_red'], linestyle='--', alpha=0.5, linewidth=1)
    ax.text(100, len(df) - 1, '100% = Paying more in tokens\nthan earning in fees',
            fontsize=7, color=C['pure_red'], va='top', ha='left')

    apply_lighthouse_style(ax, 'Subsidy Score: Token Incentives / Revenue',
                          subtitle='Lower = More Sustainable | >100% = Unsustainable Economics',
                          primary_side='left')

    fig.tight_layout()
    fig.savefig(OUT / '07_subsidy_score.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor=C['ocean_blue'])
    plt.close()
    print('  [7] Subsidy score')


# =========================================================================
# RUN ALL
# =========================================================================
if __name__ == '__main__':
    print('LIGHTHOUSE MACRO x TOKEN TERMINAL - Meeting Deck')
    print('=' * 50)
    print(f'Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    print(f'Output: {OUT}')
    print()

    chart_1_scoring_matrix()
    chart_2_valuation_map()
    chart_3_revenue_trends()
    chart_4_dau_trends()
    chart_5_macro_liquidity()
    chart_6_sector_health()
    chart_7_subsidy()

    conn.close()

    print()
    print(f'Done. {7} charts saved to {OUT}/')
    print(f'Open: open {OUT}')
