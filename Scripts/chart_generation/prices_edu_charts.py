#!/usr/bin/env python3
"""
Generate Charts for Educational Series: Post 2 - Prices
========================================================
Generates BOTH white and dark theme versions.
Matches format from Labor: THE SOURCE CODE charts.

Usage:
    python prices_edu_charts.py --chart 1
    python prices_edu_charts.py --chart 1 --theme dark
    python prices_edu_charts.py --all
"""

import os
import argparse
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.ticker import FuncFormatter
from fredapi import Fred

# ============================================
# PATHS & CONFIG
# ============================================
BASE_PATH = '/Users/bob/LHM'
OUTPUT_BASE = f'{BASE_PATH}/Outputs/Educational_Charts/Prices_Post_2'
DB_PATH = f'{BASE_PATH}/Data/databases/Lighthouse_Master.db'

fred = Fred()

COLORS = {
    'ocean': '#0089D1',
    'dusk': '#FF6723',
    'sky': '#4FC3F7',
    'venus': '#FF2389',
    'sea': '#00BB99',
    'doldrums': '#D3D6D9',
    'starboard': '#00FF00',
    'port': '#FF0000',
}

RECESSIONS = [
    ('2001-03-01', '2001-11-01'),
    ('2007-12-01', '2009-06-01'),
    ('2020-02-01', '2020-04-01'),
]

# ============================================
# THEME CONFIG
# ============================================
THEME = {}
OUTPUT_DIR = ''


def set_theme(mode='dark'):
    global THEME, OUTPUT_DIR
    if mode == 'dark':
        THEME.update({
            'bg': '#0A1628',
            'fg': '#e6edf3',
            'muted': '#8b949e',
            'spine': '#1e3350',
            'zero_line': '#e6edf3',
            'recession': '#ffffff',
            'recession_alpha': 0.06,
            'brand_color': COLORS['sky'],
            'brand2_color': COLORS['dusk'],
            'primary': COLORS['sky'],
            'secondary': COLORS['dusk'],
            'tertiary': COLORS['sea'],
            'accent': COLORS['venus'],
            'fill_alpha': 0.20,
            'box_bg': '#0A1628',
            'box_edge': COLORS['sky'],
            'legend_bg': '#0f1f38',
            'legend_fg': '#e6edf3',
            'mode': 'dark',
        })
    else:
        THEME.update({
            'bg': '#ffffff',
            'fg': '#1a1a1a',
            'muted': '#555555',
            'spine': '#cccccc',
            'zero_line': '#333333',
            'recession': 'gray',
            'recession_alpha': 0.12,
            'brand_color': COLORS['ocean'],
            'brand2_color': COLORS['dusk'],
            'primary': COLORS['ocean'],
            'secondary': COLORS['dusk'],
            'tertiary': COLORS['sea'],
            'accent': COLORS['venus'],
            'fill_alpha': 0.15,
            'box_bg': '#ffffff',
            'box_edge': COLORS['ocean'],
            'legend_bg': '#f8f8f8',
            'legend_fg': '#1a1a1a',
            'mode': 'white',
        })
    OUTPUT_DIR = os.path.join(OUTPUT_BASE, mode)
    os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================
# DATA HELPERS
# ============================================
def fetch_fred(series_id, start='2000-01-01'):
    """Fetch a FRED series and return as DataFrame."""
    s = fred.get_series(series_id, observation_start=start)
    df = s.to_frame(name='value')
    df.index.name = 'date'
    return df


def yoy_pct(df, col='value'):
    """Compute YoY % change from index level."""
    return df[col].pct_change(12, fill_method=None) * 100


# ============================================
# CHART STYLING HELPERS (matching labor format)
# ============================================
def new_fig(figsize=(14, 8)):
    """Create figure with theme background. Reserves space for TT deck branding."""
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(THEME['bg'])
    ax.set_facecolor(THEME['bg'])
    # Reserve margins: top for brand/title/subtitle, bottom for accent bar/source
    # Extra right/left margin so end-of-line pills have room outside spines
    fig.subplots_adjust(top=0.88, bottom=0.08, left=0.06, right=0.94)
    return fig, ax


def style_ax(ax, right_primary=True):
    """Style axes: all 4 spines at 0.5pt, grid off."""
    ax.grid(False)
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(True)
        ax.spines[spine].set_linewidth(0.5)
        ax.spines[spine].set_color(THEME['spine'])
    ax.tick_params(colors=THEME['fg'], labelsize=10)
    ax.xaxis.label.set_color(THEME['fg'])
    ax.yaxis.label.set_color(THEME['fg'])
    ax.title.set_color(THEME['fg'])
    if right_primary:
        ax.yaxis.tick_right()
        ax.yaxis.set_label_position('right')


def brand_fig(fig, title, subtitle=None, source=None):
    """Apply TT deck branding at figure level."""
    fig.patch.set_facecolor(THEME['bg'])

    OCEAN = '#0089D1'
    DUSK = '#FF6723'

    # Top-left watermark
    fig.text(0.03, 0.98, 'LIGHTHOUSE MACRO', fontsize=13,
             color=OCEAN, fontweight='bold', va='top')

    # Date top-right
    fig.text(0.97, 0.98, datetime.now().strftime('%B %d, %Y'),
             fontsize=11, color=THEME['muted'], ha='right', va='top')

    # Top accent bar: ocean 2/3, dusk 1/3
    bar = fig.add_axes([0.03, 0.955, 0.94, 0.004])
    bar.axhspan(0, 1, 0, 0.67, color=OCEAN)
    bar.axhspan(0, 1, 0.67, 1.0, color=DUSK)
    bar.set_xlim(0, 1); bar.set_ylim(0, 1); bar.axis('off')

    # Bottom accent bar: mirror of top
    bbar = fig.add_axes([0.03, 0.035, 0.94, 0.004])
    bbar.axhspan(0, 1, 0, 0.67, color=OCEAN)
    bbar.axhspan(0, 1, 0.67, 1.0, color=DUSK)
    bbar.set_xlim(0, 1); bbar.set_ylim(0, 1); bbar.axis('off')

    # Bottom-right watermark
    fig.text(0.97, 0.015, 'MACRO, ILLUMINATED.', fontsize=13,
             color=OCEAN, ha='right', va='top', style='italic', fontweight='bold')

    # Source line bottom-left
    if source:
        date_str = datetime.now().strftime('%m.%d.%Y')
        fig.text(0.03, 0.015, f'Lighthouse Macro | {source}; {date_str}',
                 fontsize=9, color=THEME['muted'], ha='left', va='top', style='italic')

    # Title and subtitle
    fig.suptitle(title, fontsize=15, fontweight='bold', y=0.945,
                 color=THEME['fg'])
    if subtitle:
        fig.text(0.5, 0.895, subtitle, fontsize=14, ha='center',
                 color=OCEAN, style='italic')


def add_last_value_label(ax, y_data, color, fmt='{:.1f}%', side='right'):
    """Add colored pill with bold white text on the axis edge.
    side='right' places on RHS spine, side='left' places on LHS spine.
    """
    if len(y_data) == 0:
        return
    last_y = float(y_data.iloc[-1]) if hasattr(y_data, 'iloc') else float(y_data[-1])
    label = fmt.format(last_y)
    pill = dict(boxstyle='round,pad=0.3', facecolor=color, edgecolor=color, alpha=0.95)
    if side == 'right':
        ax.annotate(label, xy=(1.0, last_y), xycoords=('axes fraction', 'data'),
                    fontsize=9, fontweight='bold', color='white',
                    ha='left', va='center',
                    xytext=(6, 0), textcoords='offset points',
                    bbox=pill)
    else:
        ax.annotate(label, xy=(0.0, last_y), xycoords=('axes fraction', 'data'),
                    fontsize=9, fontweight='bold', color='white',
                    ha='right', va='center',
                    xytext=(-6, 0), textcoords='offset points',
                    bbox=pill)


def add_recessions(ax, start_date=None):
    """Add recession shading."""
    for s, e in RECESSIONS:
        ts, te = pd.Timestamp(s), pd.Timestamp(e)
        if start_date and te < pd.Timestamp(start_date):
            continue
        ax.axvspan(ts, te, color=THEME['recession'],
                   alpha=THEME['recession_alpha'], zorder=0)


def set_xlim_to_data(ax, idx):
    """Set x limits. Extra right padding so lines end well before the right spine."""
    padding_left = pd.Timedelta(days=30)
    padding_right = pd.Timedelta(days=180)
    ax.set_xlim(idx.min() - padding_left, idx.max() + padding_right)


def legend_style():
    """Legend styling dict."""
    return dict(
        framealpha=0.95,
        facecolor=THEME['legend_bg'],
        edgecolor=THEME['spine'],
        labelcolor=THEME['legend_fg'],
    )


def save_fig(fig, filename):
    """Save figure to output directory."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(filepath, dpi=200, bbox_inches='tight', pad_inches=0.15,
                facecolor=THEME['bg'], edgecolor='none')
    plt.close(fig)
    print(f'  Saved: {filepath}')
    return filepath


# ============================================
# CHART 1: Goods vs Services CPI YoY
# ============================================
def chart_01():
    """The Great Divergence: Core Goods vs Core Services CPI YoY (dual axis, same scale)."""
    print('\nChart 1: Goods vs Services CPI YoY...')

    # Fetch SA index levels from FRED
    goods = fetch_fred('CUSR0000SACL1E', start='1999-01-01')
    services = fetch_fred('CUSR0000SASLE', start='1999-01-01')

    goods['yoy'] = yoy_pct(goods)
    services['yoy'] = yoy_pct(services)

    # Trim to 2000+
    goods = goods.loc['2000-01-01':]
    services = services.loc['2000-01-01':]

    fig, ax1 = new_fig()
    ax2 = ax1.twinx()

    c1 = THEME['primary']    # goods = sky/ocean
    c2 = THEME['secondary']  # services = dusk

    # Drop NaN before plotting so line doesn't break at gaps
    g_plot = goods['yoy'].dropna()
    s_plot = services['yoy'].dropna()

    # Plot goods on LHS
    ax1.plot(g_plot.index, g_plot, color=c1, linewidth=2.5,
             label='Core Goods CPI (LHS)')
    # Plot services on RHS
    ax2.plot(s_plot.index, s_plot, color=c2, linewidth=2.5,
             label='Core Services CPI (RHS)')

    # Zero line
    ax1.axhline(0, color=THEME['muted'], linewidth=0.8, alpha=0.5, linestyle='--')

    # Same scale, aligned at zero
    g_data = goods['yoy'].dropna()
    s_data = services['yoy'].dropna()
    all_min = min(g_data.min(), s_data.min())
    all_max = max(g_data.max(), s_data.max())
    pad = (all_max - all_min) * 0.08
    y_lo, y_hi = all_min - pad, all_max + pad

    ax1.set_ylim(y_lo, y_hi)
    ax2.set_ylim(y_lo, y_hi)

    # Style axes
    style_ax(ax1, right_primary=False)
    ax1.grid(False)
    ax2.grid(False)
    for spine in ax2.spines.values():
        spine.set_color(THEME['spine'])
        spine.set_linewidth(0.5)

    # Kill ALL tick marks on both axes (major + minor, both sides)
    ax1.tick_params(axis='both', which='both', length=0)
    ax1.tick_params(axis='y', labelcolor=c1, labelsize=10)
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'{x:.0f}%'))

    ax2.tick_params(axis='both', which='both', length=0)
    ax2.tick_params(axis='y', labelcolor=c2, labelsize=10)
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'{x:.0f}%'))

    # Also kill any secondary tick marks ax1 might draw on right via twinx
    ax1.yaxis.set_tick_params(which='both', right=False)
    ax2.yaxis.set_tick_params(which='both', left=False)

    set_xlim_to_data(ax1, goods.index)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    # Last value labels: goods on LHS, services on RHS
    add_last_value_label(ax1, g_data, color=c1, side='left')
    add_last_value_label(ax2, s_data, color=c2, side='right')

    # Recession shading
    add_recessions(ax1)

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', **legend_style())

    # Annotation box — takeaway in the dead space, right of recession bars
    takeaway = "Services inflation running 2x goods.\nThe last mile problem is a services problem."
    ax1.text(0.52, 0.92, takeaway, transform=ax1.transAxes,
             fontsize=10, color=THEME['fg'], ha='center', va='top',
             style='italic',
             bbox=dict(boxstyle='round,pad=0.5',
                       facecolor=THEME['bg'], edgecolor='#0089D1',
                       alpha=0.9))

    # TT deck branding at figure level
    brand_fig(fig, 'The Great Divergence: Core Goods vs Core Services',
              subtitle='Goods deflating while services remain sticky',
              source='BLS CPI')

    return save_fig(fig, 'chart_01_goods_vs_services.png')


# ============================================
# MAIN
# ============================================
CHART_MAP = {
    1: chart_01,
}


def main():
    parser = argparse.ArgumentParser(description='Generate Prices educational charts')
    parser.add_argument('--chart', type=int, help='Chart number to generate (1-18)')
    parser.add_argument('--theme', default='both', choices=['dark', 'white', 'both'],
                        help='Theme to generate')
    parser.add_argument('--all', action='store_true', help='Generate all charts')
    args = parser.parse_args()

    if args.all:
        charts_to_gen = sorted(CHART_MAP.keys())
    elif args.chart:
        charts_to_gen = [args.chart]
    else:
        charts_to_gen = [1]

    themes_to_gen = ['dark', 'white'] if args.theme == 'both' else [args.theme]

    for mode in themes_to_gen:
        set_theme(mode)
        for chart_num in charts_to_gen:
            if chart_num not in CHART_MAP:
                print(f'Chart {chart_num} not implemented yet.')
                continue
            CHART_MAP[chart_num]()

    print('\nDone.')


if __name__ == '__main__':
    main()
