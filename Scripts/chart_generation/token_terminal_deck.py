#!/usr/bin/env python3
"""
TOKEN TERMINAL x LIGHTHOUSE MACRO - Dashboard
==============================================
Single-page institutional dashboard combining Token Terminal
protocol fundamentals with Lighthouse Macro liquidity overlay.

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
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.lines import Line2D
from pathlib import Path
from datetime import datetime, timedelta

from lighthouse_chart_style import (
    LIGHTHOUSE_COLORS as C,
    apply_lighthouse_style,
    apply_lighthouse_style_fig,
    hex_to_rgba
)

DB = Path('/Users/bob/LHM/Data/databases/Lighthouse_Master.db')
OUT = Path('/Users/bob/LHM/Outputs/token_terminal_deck')
OUT.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB)

# =========================================================================
# DATA HELPERS
# =========================================================================

def get_scores():
    """Get latest protocol scores with proper names."""
    df = pd.read_sql("""
        SELECT cs.*, cm.name as meta_name
        FROM crypto_scores cs
        LEFT JOIN crypto_meta cm ON cs.project_id = cm.project_id
        WHERE cs.date = (SELECT MAX(date) FROM crypto_scores)
        ORDER BY cs.overall_score DESC
    """, conn)
    # Use scores name if available, else meta name, else project_id
    df['display_name'] = df['name'].fillna(df['meta_name']).fillna(df['project_id'])
    return df


def get_metric_ts(metric_id, project_ids=None, days=180):
    """Get time series for a metric."""
    cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    q = "SELECT cm.project_id, cm.date, cm.value FROM crypto_metrics cm WHERE cm.metric_id=? AND cm.date>=?"
    params = [metric_id, cutoff]
    if project_ids:
        placeholders = ','.join(['?'] * len(project_ids))
        q += f" AND cm.project_id IN ({placeholders})"
        params.extend(project_ids)
    q += " ORDER BY cm.date"
    return pd.read_sql(q, conn, params=params)


def get_macro_ts(series_id, days=730):
    """Get macro time series from observations."""
    cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    df = pd.read_sql(
        "SELECT date, value FROM observations WHERE series_id=? AND date>=? ORDER BY date",
        conn, params=[series_id, cutoff]
    )
    df['date'] = pd.to_datetime(df['date'])
    return df


def get_names():
    """Get display names for all protocols."""
    scores = get_scores()
    return dict(zip(scores['project_id'], scores['display_name']))


# =========================================================================
# DASHBOARD 1: Protocol Fundamentals (single page, 6 panels)
# =========================================================================

def dashboard_protocol_fundamentals():
    """
    6-panel dashboard:
      Top-left:     Scoring matrix (top 15)
      Top-right:    Valuation map (scatter)
      Mid-left:     Revenue trends (top 6)
      Mid-right:    DAU trends (top 6)
      Bottom-left:  Sector health
      Bottom-right: Key stats table
    """
    scores = get_scores()
    names = get_names()

    fig = plt.figure(figsize=(22, 28), facecolor='white')

    # Custom grid: 3 rows x 2 cols
    gs = gridspec.GridSpec(3, 2, hspace=0.35, wspace=0.25,
                           left=0.06, right=0.96, top=0.92, bottom=0.03)

    palette = [C['ocean_blue'], C['dusk_orange'], C['teal_green'],
               C['hot_magenta'], C['electric_cyan'], '#8B5CF6']

    # ------------------------------------------------------------------
    # PANEL 1: Scoring Matrix (top-left)
    # ------------------------------------------------------------------
    ax1 = fig.add_subplot(gs[0, 0])
    df = scores[scores['overall_score'] > 0].head(15)

    protocols = df['display_name'].tolist()
    fin = df['financial_score'].fillna(0).tolist()
    use = df['usage_score'].fillna(0).tolist()
    val = df['valuation_score'].fillna(0).tolist()
    total = df['overall_score'].fillna(0).tolist()

    y = np.arange(len(protocols))
    bh = 0.25

    ax1.barh(y + bh, fin, bh, label='Financial', color=C['ocean_blue'], alpha=0.9)
    ax1.barh(y, use, bh, label='Usage', color=C['teal_green'], alpha=0.9)
    ax1.barh(y - bh, val, bh, label='Valuation', color=C['dusk_orange'], alpha=0.9)

    for i, t in enumerate(total):
        ax1.text(max(fin[i], use[i], val[i]) + 1.5, y[i], f'{t:.0f}',
                 va='center', fontsize=8, fontweight='bold', color='#333')

    # Tier color dots
    for i, row in enumerate(df.itertuples()):
        v = str(row.verdict) if row.verdict else ''
        if 'TIER 1' in v:
            c = C['teal_green']
        elif 'TIER 2' in v:
            c = C['ocean_blue']
        elif 'NEUTRAL' in v:
            c = C['neutral_gray']
        else:
            c = C['pure_red']
        ax1.plot(-2, y[i], 'o', color=c, markersize=6, clip_on=False)

    ax1.set_yticks(y)
    ax1.set_yticklabels(protocols, fontsize=8)
    ax1.invert_yaxis()
    ax1.set_xlim(-4, 105)
    ax1.legend(loc='lower right', fontsize=7, framealpha=0.9)
    ax1.set_title('LHM Protocol Scoring Matrix', fontsize=12, fontweight='bold', pad=10)
    ax1.text(0.5, 1.01, '24-Point System | Financial + Usage + Valuation',
             transform=ax1.transAxes, fontsize=8, ha='center', color='#666', style='italic')
    for spine in ax1.spines.values():
        spine.set_linewidth(0.5)
        spine.set_color('#999')

    # ------------------------------------------------------------------
    # PANEL 2: Valuation Map (top-right)
    # ------------------------------------------------------------------
    ax2 = fig.add_subplot(gs[0, 1])
    vdf = scores[(scores['ann_revenue'] > 0) & (scores['pf_ratio'] > 0) & (scores['pf_ratio'] < 10000)].copy()

    colors = []
    for v in vdf['verdict']:
        v = str(v)
        if 'TIER 1' in v:
            colors.append(C['teal_green'])
        elif 'TIER 2' in v:
            colors.append(C['ocean_blue'])
        elif 'NEUTRAL' in v:
            colors.append(C['neutral_gray'])
        else:
            colors.append(C['pure_red'])

    sizes = np.clip(vdf['fdv'].fillna(1e8) / 1e8, 30, 400)

    ax2.scatter(vdf['ann_revenue'] / 1e6, vdf['pf_ratio'],
                c=colors, s=sizes, alpha=0.7, edgecolors='#333', linewidth=0.5)

    for _, row in vdf.iterrows():
        if row['ann_revenue'] > 3e6 or row['pf_ratio'] < 5 or row['overall_score'] >= 75:
            ax2.annotate(row['display_name'], (row['ann_revenue'] / 1e6, row['pf_ratio']),
                         fontsize=7, ha='left', va='bottom',
                         xytext=(4, 4), textcoords='offset points')

    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('Annualized Revenue ($M)', fontsize=9)
    ax2.set_ylabel('P/F Ratio (FDV / Fees)', fontsize=9)
    ax2.axhline(y=10, color=C['dusk_orange'], linestyle='--', alpha=0.4, linewidth=1)
    ax2.axvline(x=10, color=C['dusk_orange'], linestyle='--', alpha=0.4, linewidth=1)

    # Value zone label
    ax2.text(0.95, 0.05, 'VALUE ZONE\nHigh Rev + Low P/F', fontsize=8,
             color=C['teal_green'], alpha=0.5, fontweight='bold',
             ha='right', va='bottom', transform=ax2.transAxes)

    legend_els = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor=C['teal_green'], markersize=8, label='Tier 1'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=C['ocean_blue'], markersize=8, label='Tier 2'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=C['neutral_gray'], markersize=8, label='Neutral'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=C['pure_red'], markersize=8, label='Avoid'),
    ]
    ax2.legend(handles=legend_els, loc='upper left', fontsize=7, framealpha=0.9)

    ax2.set_title('Protocol Valuation Map', fontsize=12, fontweight='bold', pad=10)
    ax2.text(0.5, 1.01, 'Revenue vs P/F | Bubble Size = FDV | Color = LHM Verdict',
             transform=ax2.transAxes, fontsize=8, ha='center', color='#666', style='italic')
    for spine in ax2.spines.values():
        spine.set_linewidth(0.5)
        spine.set_color('#999')

    # ------------------------------------------------------------------
    # PANEL 3: Revenue Trends (mid-left)
    # ------------------------------------------------------------------
    ax3 = fig.add_subplot(gs[1, 0])
    top6 = scores.head(6)['project_id'].tolist()
    rev_df = get_metric_ts('revenue', top6, days=180)
    rev_df['date'] = pd.to_datetime(rev_df['date'])

    for i, pid in enumerate(top6):
        sub = rev_df[rev_df['project_id'] == pid].copy()
        if sub.empty:
            continue
        sub = sub[['date', 'value']].set_index('date').resample('W').mean().reset_index()
        label = names.get(pid, pid)
        ax3.plot(sub['date'], sub['value'] / 1e6, color=palette[i % len(palette)],
                 linewidth=1.8, label=label, alpha=0.85)

    ax3.set_ylabel('Weekly Revenue ($M)', fontsize=9)
    ax3.legend(loc='upper left', fontsize=7, ncol=2, framealpha=0.9)
    ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:.1f}M'))
    ax3.set_title('Revenue Trends (6M)', fontsize=12, fontweight='bold', pad=10)
    ax3.text(0.5, 1.01, 'Token Terminal | Weekly Avg | Top 6 by LHM Score',
             transform=ax3.transAxes, fontsize=8, ha='center', color='#666', style='italic')
    for spine in ax3.spines.values():
        spine.set_linewidth(0.5)
        spine.set_color('#999')

    # ------------------------------------------------------------------
    # PANEL 4: DAU Trends (mid-right)
    # ------------------------------------------------------------------
    ax4 = fig.add_subplot(gs[1, 1])
    dau_df = get_metric_ts('user_dau', top6, days=180)
    dau_df['date'] = pd.to_datetime(dau_df['date'])

    for i, pid in enumerate(top6):
        sub = dau_df[dau_df['project_id'] == pid].copy()
        if sub.empty:
            continue
        sub = sub[['date', 'value']].set_index('date').resample('W').mean().reset_index()
        label = names.get(pid, pid)
        ax4.plot(sub['date'], sub['value'] / 1e3, color=palette[i % len(palette)],
                 linewidth=1.8, label=label, alpha=0.85)

    ax4.set_ylabel('Daily Active Users (K)', fontsize=9)
    ax4.legend(loc='upper left', fontsize=7, ncol=2, framealpha=0.9)
    ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0f}K'))
    ax4.set_title('DAU Trends (6M)', fontsize=12, fontweight='bold', pad=10)
    ax4.text(0.5, 1.01, 'Token Terminal | Weekly Avg | Top 6 by LHM Score',
             transform=ax4.transAxes, fontsize=8, ha='center', color='#666', style='italic')
    for spine in ax4.spines.values():
        spine.set_linewidth(0.5)
        spine.set_color('#999')

    # ------------------------------------------------------------------
    # PANEL 5: Sector Health (bottom-left)
    # ------------------------------------------------------------------
    ax5 = fig.add_subplot(gs[2, 0])
    sectors = scores.groupby('sector').agg({
        'overall_score': 'mean',
        'financial_score': 'mean',
        'usage_score': 'mean',
        'valuation_score': 'mean',
        'ann_revenue': 'sum',
        'project_id': 'count'
    }).rename(columns={'project_id': 'count'}).sort_values('overall_score', ascending=True)

    sy = np.arange(len(sectors))
    scolors = [C['teal_green'] if s >= 70 else C['ocean_blue'] if s >= 55
               else C['dusk_orange'] if s >= 40 else C['pure_red']
               for s in sectors['overall_score']]

    ax5.barh(sy, sectors['overall_score'], color=scolors, alpha=0.85,
             edgecolor='#333', linewidth=0.5)

    for i, (score, count, rev) in enumerate(zip(
            sectors['overall_score'], sectors['count'], sectors['ann_revenue'])):
        ax5.text(score + 1, sy[i], f'{score:.0f}  ({count}p, ${rev/1e6:.0f}M rev)',
                 va='center', fontsize=7.5, color='#333')

    ax5.set_yticks(sy)
    ax5.set_yticklabels([s.replace('_', ' ').title() if s else 'Other'
                         for s in sectors.index], fontsize=8)
    ax5.set_xlim(0, 100)
    ax5.axvline(55, color=C['dusk_orange'], linestyle='--', alpha=0.3, linewidth=1)
    ax5.axvline(70, color=C['teal_green'], linestyle='--', alpha=0.3, linewidth=1)
    ax5.set_title('Sector Health', fontsize=12, fontweight='bold', pad=10)
    ax5.text(0.5, 1.01, 'Avg LHM Score | (protocols, total annualized revenue)',
             transform=ax5.transAxes, fontsize=8, ha='center', color='#666', style='italic')
    for spine in ax5.spines.values():
        spine.set_linewidth(0.5)
        spine.set_color('#999')

    # ------------------------------------------------------------------
    # PANEL 6: Key Stats Table (bottom-right)
    # ------------------------------------------------------------------
    ax6 = fig.add_subplot(gs[2, 1])
    ax6.axis('off')

    # Build stats
    tier1 = scores[scores['verdict'].str.contains('TIER 1', na=False)]
    tier2 = scores[scores['verdict'].str.contains('TIER 2', na=False)]
    avoid = scores[scores['verdict'].str.contains('AVOID', na=False)]

    total_rev = scores['ann_revenue'].sum()
    total_fees = scores['ann_fees'].sum()
    avg_pf = scores.loc[scores['pf_ratio'] > 0, 'pf_ratio'].median()
    total_dau = scores['dau'].sum()
    total_tvl = scores['tvl'].sum()

    # Latest macro
    rrp_val = get_macro_ts('RRPONTSYD', 7)
    rrp_latest = f"${rrp_val['value'].iloc[-1]:.1f}B" if not rrp_val.empty else "N/A"
    nfci_val = get_macro_ts('NFCI', 7)
    nfci_latest = f"{nfci_val['value'].iloc[-1]:.2f}" if not nfci_val.empty else "N/A"
    hy_val = get_macro_ts('BAMLH0A0HYM2', 7)
    hy_latest = f"{hy_val['value'].iloc[-1]:.0f}bps" if not hy_val.empty else "N/A"
    vix_val = get_macro_ts('VIXCLS', 7)
    vix_latest = f"{vix_val['value'].iloc[-1]:.1f}" if not vix_val.empty else "N/A"

    stats_data = [
        ['PROTOCOL UNIVERSE', ''],
        ['Protocols Covered', f'{len(scores)}'],
        ['Tier 1 (Accumulate)', f'{len(tier1)} protocols'],
        ['Tier 2 (Hold)', f'{len(tier2)} protocols'],
        ['Avoid / Caution', f'{len(avoid)} protocols'],
        ['', ''],
        ['AGGREGATE FUNDAMENTALS', ''],
        ['Total Ann. Revenue', f'${total_rev/1e6:.0f}M'],
        ['Total Ann. Fees', f'${total_fees/1e6:.0f}M'],
        ['Median P/F Ratio', f'{avg_pf:.1f}x'],
        ['Total DAU', f'{total_dau/1e3:.0f}K'],
        ['Total TVL', f'${total_tvl/1e9:.1f}B'],
        ['', ''],
        ['MACRO CONTEXT', ''],
        ['Reverse Repo (RRP)', rrp_latest],
        ['NFCI (Fin Conditions)', nfci_latest],
        ['HY OAS (Credit)', hy_latest],
        ['VIX', vix_latest],
    ]

    # Draw table manually for better control
    y_pos = 0.95
    for label, value in stats_data:
        if value == '' and label != '':
            # Section header
            ax6.text(0.05, y_pos, label, transform=ax6.transAxes,
                     fontsize=10, fontweight='bold', color=C['ocean_blue'],
                     family='monospace')
            y_pos -= 0.005
            ax6.plot([0.03, 0.97], [y_pos, y_pos], color=C['ocean_blue'],
                     linewidth=0.8, alpha=0.5, transform=ax6.transAxes, clip_on=False)
        elif label == '' and value == '':
            pass  # spacer
        else:
            ax6.text(0.08, y_pos, label, transform=ax6.transAxes,
                     fontsize=9, color='#333', family='monospace')
            ax6.text(0.92, y_pos, value, transform=ax6.transAxes,
                     fontsize=9, fontweight='bold', color='#111',
                     ha='right', family='monospace')
        y_pos -= 0.05

    ax6.set_title('Dashboard Summary', fontsize=12, fontweight='bold', pad=10)

    # ------------------------------------------------------------------
    # FIGURE-LEVEL BRANDING
    # ------------------------------------------------------------------
    fig.text(0.03, 0.97, 'LIGHTHOUSE MACRO', fontsize=14,
             color=C['ocean_blue'], fontweight='bold')
    fig.text(0.03, 0.955, f'Token Terminal Integration | {datetime.now().strftime("%B %d, %Y")}',
             fontsize=10, color='#666', style='italic')
    fig.text(0.97, 0.01, 'MACRO, ILLUMINATED.', fontsize=8,
             color=C['hot_magenta'], ha='right', style='italic')

    # Accent bar at top
    bar = fig.add_axes([0.03, 0.935, 0.94, 0.005])
    bar.axhspan(0, 1, 0, 0.67, color=C['ocean_blue'])
    bar.axhspan(0, 1, 0.67, 1.0, color=C['dusk_orange'])
    bar.set_xlim(0, 1)
    bar.set_ylim(0, 1)
    bar.axis('off')

    fig.savefig(OUT / 'dashboard_protocol_fundamentals.png', dpi=150,
                bbox_inches='tight', facecolor='white', edgecolor=C['ocean_blue'])
    plt.close()
    print('  [1] Protocol fundamentals dashboard')


# =========================================================================
# DASHBOARD 2: Macro Liquidity + Crypto Overlay
# =========================================================================

def dashboard_macro_overlay():
    """
    6-panel dashboard:
      Top-left:     RRP (2Y)
      Top-right:    NFCI (2Y)
      Mid-left:     HY OAS (2Y)
      Mid-right:    VIX (2Y)
      Bottom-left:  Yield curve (10Y-2Y, 10Y-3M)
      Bottom-right: Crypto revenue vs RRP overlay
    """
    fig = plt.figure(figsize=(22, 28), facecolor='white')
    gs = gridspec.GridSpec(3, 2, hspace=0.35, wspace=0.25,
                           left=0.06, right=0.96, top=0.92, bottom=0.03)

    names = get_names()

    # ------------------------------------------------------------------
    # PANEL 1: RRP
    # ------------------------------------------------------------------
    ax1 = fig.add_subplot(gs[0, 0])
    rrp = get_macro_ts('RRPONTSYD', 730)
    if not rrp.empty:
        ax1.fill_between(rrp['date'], rrp['value'], alpha=0.3, color=C['ocean_blue'])
        ax1.plot(rrp['date'], rrp['value'], color=C['ocean_blue'], linewidth=1.5)
        ax1.axhline(200, color=C['pure_red'], linestyle='--', alpha=0.5, linewidth=1)
        ax1.text(0.97, 0.15, 'Buffer Exhausted (<$200B)', fontsize=8,
                 color=C['pure_red'], ha='right', transform=ax1.transAxes, alpha=0.7)
        # Latest value callout
        latest = rrp.iloc[-1]
        ax1.annotate(f'${latest["value"]:.1f}B', xy=(latest['date'], latest['value']),
                     fontsize=10, fontweight='bold', color=C['ocean_blue'],
                     xytext=(10, 15), textcoords='offset points',
                     arrowprops=dict(arrowstyle='->', color=C['ocean_blue'], lw=1.2))
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:.0f}B'))
    ax1.set_title('Reverse Repo Facility ($B)', fontsize=12, fontweight='bold', pad=10)
    ax1.text(0.5, 1.01, 'Fed Liquidity Buffer | Effectively Zero',
             transform=ax1.transAxes, fontsize=8, ha='center', color='#666', style='italic')
    for spine in ax1.spines.values():
        spine.set_linewidth(0.5)
        spine.set_color('#999')

    # ------------------------------------------------------------------
    # PANEL 2: NFCI
    # ------------------------------------------------------------------
    ax2 = fig.add_subplot(gs[0, 1])
    nfci = get_macro_ts('NFCI', 730)
    if not nfci.empty:
        pos_mask = nfci['value'] >= 0
        neg_mask = nfci['value'] < 0
        ax2.fill_between(nfci['date'], nfci['value'], where=pos_mask,
                         alpha=0.3, color=C['pure_red'])
        ax2.fill_between(nfci['date'], nfci['value'], where=neg_mask,
                         alpha=0.3, color=C['teal_green'])
        ax2.plot(nfci['date'], nfci['value'], color=C['ocean_blue'], linewidth=1.5)
        ax2.axhline(0, color='#333', linewidth=0.8)
        latest = nfci.iloc[-1]
        ax2.annotate(f'{latest["value"]:.2f}', xy=(latest['date'], latest['value']),
                     fontsize=10, fontweight='bold', color=C['ocean_blue'],
                     xytext=(10, -20), textcoords='offset points',
                     arrowprops=dict(arrowstyle='->', color=C['ocean_blue'], lw=1.2))
    ax2.set_title('Financial Conditions (NFCI)', fontsize=12, fontweight='bold', pad=10)
    ax2.text(0.5, 1.01, 'Negative = Loose | Positive = Tight',
             transform=ax2.transAxes, fontsize=8, ha='center', color='#666', style='italic')
    for spine in ax2.spines.values():
        spine.set_linewidth(0.5)
        spine.set_color('#999')

    # ------------------------------------------------------------------
    # PANEL 3: HY OAS
    # ------------------------------------------------------------------
    ax3 = fig.add_subplot(gs[1, 0])
    hy = get_macro_ts('BAMLH0A0HYM2', 730)
    if not hy.empty:
        ax3.fill_between(hy['date'], hy['value'] * 100, alpha=0.25, color=C['dusk_orange'])
        ax3.plot(hy['date'], hy['value'] * 100, color=C['dusk_orange'], linewidth=1.5)
        ax3.axhline(300, color=C['pure_red'], linestyle='--', alpha=0.5, linewidth=1)
        ax3.text(0.97, 0.85, 'Complacency (<300bps)', fontsize=8,
                 color=C['pure_red'], ha='right', transform=ax3.transAxes, alpha=0.7)
        latest = hy.iloc[-1]
        ax3.annotate(f'{latest["value"]*100:.0f}bps', xy=(latest['date'], latest['value']*100),
                     fontsize=10, fontweight='bold', color=C['dusk_orange'],
                     xytext=(10, 15), textcoords='offset points',
                     arrowprops=dict(arrowstyle='->', color=C['dusk_orange'], lw=1.2))
    ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0f}'))
    ax3.set_ylabel('Spread (bps)', fontsize=9)
    ax3.set_title('HY Credit Spreads (OAS)', fontsize=12, fontweight='bold', pad=10)
    ax3.text(0.5, 1.01, 'Risk Appetite Proxy | Tight = Complacent',
             transform=ax3.transAxes, fontsize=8, ha='center', color='#666', style='italic')
    for spine in ax3.spines.values():
        spine.set_linewidth(0.5)
        spine.set_color('#999')

    # ------------------------------------------------------------------
    # PANEL 4: VIX
    # ------------------------------------------------------------------
    ax4 = fig.add_subplot(gs[1, 1])
    vix = get_macro_ts('VIXCLS', 730)
    if not vix.empty:
        ax4.fill_between(vix['date'], vix['value'], alpha=0.25, color=C['hot_magenta'])
        ax4.plot(vix['date'], vix['value'], color=C['hot_magenta'], linewidth=1.5)
        ax4.axhline(20, color=C['dusk_orange'], linestyle='--', alpha=0.5, linewidth=1)
        ax4.axhline(30, color=C['pure_red'], linestyle='--', alpha=0.5, linewidth=1)
        latest = vix.iloc[-1]
        ax4.annotate(f'{latest["value"]:.1f}', xy=(latest['date'], latest['value']),
                     fontsize=10, fontweight='bold', color=C['hot_magenta'],
                     xytext=(10, 15), textcoords='offset points',
                     arrowprops=dict(arrowstyle='->', color=C['hot_magenta'], lw=1.2))
    ax4.set_title('VIX (Implied Volatility)', fontsize=12, fontweight='bold', pad=10)
    ax4.text(0.5, 1.01, 'Fear Gauge | >20 Caution | >30 Stress',
             transform=ax4.transAxes, fontsize=8, ha='center', color='#666', style='italic')
    for spine in ax4.spines.values():
        spine.set_linewidth(0.5)
        spine.set_color('#999')

    # ------------------------------------------------------------------
    # PANEL 5: Yield Curve
    # ------------------------------------------------------------------
    ax5 = fig.add_subplot(gs[2, 0])
    t10y2y = get_macro_ts('T10Y2Y', 730)
    t10y3m = get_macro_ts('T10Y3M', 730)

    if not t10y2y.empty:
        ax5.fill_between(t10y2y['date'], t10y2y['value'],
                         where=t10y2y['value'] < 0, alpha=0.25, color=C['pure_red'])
        ax5.fill_between(t10y2y['date'], t10y2y['value'],
                         where=t10y2y['value'] >= 0, alpha=0.15, color=C['teal_green'])
        ax5.plot(t10y2y['date'], t10y2y['value'], color=C['ocean_blue'],
                 linewidth=1.5, label='10Y-2Y')
    if not t10y3m.empty:
        ax5.plot(t10y3m['date'], t10y3m['value'], color=C['dusk_orange'],
                 linewidth=1.5, label='10Y-3M', alpha=0.8)
    ax5.axhline(0, color='#333', linewidth=0.8)
    ax5.legend(loc='upper left', fontsize=8, framealpha=0.9)
    ax5.set_ylabel('Spread (%)', fontsize=9)
    ax5.set_title('Yield Curve', fontsize=12, fontweight='bold', pad=10)
    ax5.text(0.5, 1.01, 'Inversion = Recession Signal | Steepening = Normalization',
             transform=ax5.transAxes, fontsize=8, ha='center', color='#666', style='italic')
    for spine in ax5.spines.values():
        spine.set_linewidth(0.5)
        spine.set_color('#999')

    # ------------------------------------------------------------------
    # PANEL 6: Crypto Revenue vs RRP Overlay
    # ------------------------------------------------------------------
    ax6 = fig.add_subplot(gs[2, 1])

    # Total crypto revenue (aggregate across all protocols)
    all_rev = get_metric_ts('revenue', days=365)
    if not all_rev.empty:
        all_rev['date'] = pd.to_datetime(all_rev['date'])
        agg_rev = all_rev.groupby('date')['value'].sum().reset_index()
        agg_rev = agg_rev.set_index('date').resample('W').mean().reset_index()

        ax6.bar(agg_rev['date'], agg_rev['value'] / 1e6, width=5,
                color=C['teal_green'], alpha=0.6, label='Total Protocol Revenue ($M/wk)')
        ax6.set_ylabel('Weekly Revenue ($M)', fontsize=9, color=C['teal_green'])
        ax6.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:.0f}M'))

        # RRP overlay on right axis
        ax6r = ax6.twinx()
        rrp_1y = get_macro_ts('RRPONTSYD', 365)
        if not rrp_1y.empty:
            ax6r.plot(rrp_1y['date'], rrp_1y['value'], color=C['ocean_blue'],
                      linewidth=2, label='RRP ($B)', alpha=0.8)
            ax6r.set_ylabel('RRP ($B)', fontsize=9, color=C['ocean_blue'])
            ax6r.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:.0f}B'))
            ax6r.spines['right'].set_color(C['ocean_blue'])

        ax6.legend(loc='upper left', fontsize=7, framealpha=0.9)
        if not rrp_1y.empty:
            ax6r.legend(loc='upper right', fontsize=7, framealpha=0.9)

    ax6.set_title('Crypto Revenue vs Liquidity', fontsize=12, fontweight='bold', pad=10)
    ax6.text(0.5, 1.01, 'Total Protocol Rev (bars) vs Fed RRP (line) | 1Y',
             transform=ax6.transAxes, fontsize=8, ha='center', color='#666', style='italic')
    for spine in ax6.spines.values():
        spine.set_linewidth(0.5)
        spine.set_color('#999')

    # ------------------------------------------------------------------
    # FIGURE-LEVEL BRANDING
    # ------------------------------------------------------------------
    fig.text(0.03, 0.97, 'LIGHTHOUSE MACRO', fontsize=14,
             color=C['ocean_blue'], fontweight='bold')
    fig.text(0.03, 0.955, f'Macro Liquidity Context | {datetime.now().strftime("%B %d, %Y")}',
             fontsize=10, color='#666', style='italic')
    fig.text(0.97, 0.01, 'MACRO, ILLUMINATED.', fontsize=8,
             color=C['hot_magenta'], ha='right', style='italic')

    bar = fig.add_axes([0.03, 0.935, 0.94, 0.005])
    bar.axhspan(0, 1, 0, 0.67, color=C['ocean_blue'])
    bar.axhspan(0, 1, 0.67, 1.0, color=C['dusk_orange'])
    bar.set_xlim(0, 1)
    bar.set_ylim(0, 1)
    bar.axis('off')

    fig.savefig(OUT / 'dashboard_macro_liquidity.png', dpi=150,
                bbox_inches='tight', facecolor='white', edgecolor=C['ocean_blue'])
    plt.close()
    print('  [2] Macro liquidity dashboard')


# =========================================================================
# RUN ALL
# =========================================================================
if __name__ == '__main__':
    print('LIGHTHOUSE MACRO x TOKEN TERMINAL - Dashboards')
    print('=' * 50)
    print(f'Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    print(f'Output: {OUT}')
    print()

    dashboard_protocol_fundamentals()
    dashboard_macro_overlay()

    conn.close()

    print()
    print(f'Done. 2 dashboards saved to {OUT}/')
    print(f'Open: open {OUT}')
