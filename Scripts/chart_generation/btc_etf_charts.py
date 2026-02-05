"""
BTC ETF Charts - Spot Capitulation & On-Chain Reality
Lighthouse Macro Chart Styling Spec v3.0
Uses REAL data from Farside Investors + yfinance + DefiLlama
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter
import pandas as pd
import numpy as np
from pathlib import Path
import yfinance as yf
import requests

# ———————— COLORS (FIXED) ————————
COLORS = {
    'ocean': '#0089D1',
    'dusk': '#FF6723',
    'sky': '#4FC3F7',
    'sea': '#00BB99',
    'venus': '#FF2389',
    'doldrums': '#D3D6D9',
}

# ———————— THEME DEFINITION (DARK) ————————
# Updated: Ocean (#0089D1) is PRIMARY for BOTH themes per MEMORY.md
THEME = {
    'bg': '#0A1628',
    'fg': '#e6edf3',
    'muted': '#8b949e',
    'spine': '#1e3350',
    'primary': '#0089D1',        # Ocean (Primary Data - RHS) - ALWAYS
    'secondary': '#FF6723',      # Dusk (Secondary Data - LHS)
    'tertiary': '#4FC3F7',       # Sky (third series)
    'accent': '#FF2389',         # Venus
    'legend_bg': '#0f1f38',
    'legend_fg': '#e6edf3',
}

# ———————— OUTPUT PATH ————————
OUTPUT_DIR = Path('/Users/bob/LHM/Outputs/Educational_Charts/BTC_ETF')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ———————— LOAD REAL DATA ————————
def load_etf_flows():
    """Load Farside ETF flow data and compute cumulative flows."""
    csv_path = '/Users/bob/LHM/Data/raw/btc_etf_flows_farside.csv'
    df = pd.read_csv(csv_path)

    # Parse date (format: "11 Jan 2024")
    df['Date'] = pd.to_datetime(df['Date'], format='%d %b %Y')
    df = df.set_index('Date').sort_index()

    # Calculate cumulative flows from daily totals
    df['Cumulative_Flows'] = df['Total'].cumsum()

    return df


def load_btc_price(start_date, end_date):
    """Load BTC price data from yfinance."""
    btc = yf.download('BTC-USD', start=start_date, end=end_date, progress=False)
    btc = btc[['Close']].rename(columns={'Close': 'BTC_Price'})
    # Flatten MultiIndex columns if present
    if isinstance(btc.columns, pd.MultiIndex):
        btc.columns = btc.columns.get_level_values(0)
    return btc


def load_base_tvl():
    """Load Base chain TVL from DefiLlama."""
    url = "https://api.llama.fi/v2/historicalChainTvl/Base"
    resp = requests.get(url)
    data = resp.json()
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'], unit='s')
    df = df.set_index('date').sort_index()
    df = df.rename(columns={'tvl': 'Base_TVL'})
    df['Base_TVL'] = df['Base_TVL'] / 1e9  # Convert to billions
    return df


def load_cbbtc_supply():
    """Load cbBTC supply from DefiLlama."""
    # cbBTC is Coinbase wrapped BTC on Base
    url = "https://api.llama.fi/protocol/cbbtc"
    resp = requests.get(url)
    data = resp.json()

    # Extract TVL history
    tvl_history = data.get('tvl', [])
    df = pd.DataFrame(tvl_history)
    df['date'] = pd.to_datetime(df['date'], unit='s')
    df = df.set_index('date').sort_index()
    df = df.rename(columns={'totalLiquidityUSD': 'cbBTC_TVL'})
    df['cbBTC_TVL'] = df['cbBTC_TVL'] / 1e9  # Convert to billions
    return df[['cbBTC_TVL']]


def prepare_data():
    """Prepare merged dataset with ETF flows and BTC price."""
    # Load ETF flows
    flows = load_etf_flows()

    # Load BTC price for same date range
    start = flows.index.min()
    end = flows.index.max() + pd.Timedelta(days=1)
    price = load_btc_price(start, end)

    # Merge on date
    df = flows[['Cumulative_Flows', 'Total']].join(price, how='outer')

    # Forward fill price for weekends/holidays, then back fill any remaining
    df['BTC_Price'] = df['BTC_Price'].ffill().bfill()

    # Drop rows where we don't have flow data
    df = df.dropna(subset=['Cumulative_Flows'])

    return df


def prepare_onchain_data():
    """Prepare Base TVL data (cbBTC not separately trackable on DefiLlama)."""
    try:
        base = load_base_tvl()
        return base
    except Exception as e:
        print(f"Warning: Could not load on-chain data: {e}")
        return None


# Load data at module level
print("Loading real data...")
df = prepare_data()
print(f"ETF data loaded: {len(df)} days from {df.index.min().date()} to {df.index.max().date()}")
print(f"Cumulative flows: ${df['Cumulative_Flows'].iloc[-1]:,.0f}M")
print(f"BTC Price: ${df['BTC_Price'].iloc[-1]:,.0f}")

print("Loading on-chain data...")
df_onchain = prepare_onchain_data()
if df_onchain is not None:
    print(f"On-chain data loaded: {len(df_onchain)} days")
    print(f"Base TVL: ${df_onchain['Base_TVL'].iloc[-1]:.1f}B")
    if 'cbBTC_TVL' in df_onchain.columns:
        print(f"cbBTC TVL: ${df_onchain['cbBTC_TVL'].iloc[-1]:.2f}B")


# ———————— HELPER FUNCTIONS ————————

def new_fig(figsize=(14, 8)):
    """Create figure with theme background and standard margins."""
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(THEME['bg'])
    ax.set_facecolor(THEME['bg'])
    return fig, ax


def style_ax(ax):
    """Core spine/grid styling."""
    for spine in ax.spines.values():
        spine.set_color(THEME['spine'])
        spine.set_linewidth(0.5)
    ax.grid(False)
    ax.tick_params(axis='both', which='both', length=0, colors=THEME['muted'])
    ax.tick_params(axis='x', labelsize=10, labelcolor=THEME['muted'])


def style_dual_ax(ax1, ax2, c1, c2):
    """Full dual-axis styling: LHS=c1 (secondary), RHS=c2 (primary)."""
    for ax in [ax1, ax2]:
        ax.set_facecolor(THEME['bg'])
        for spine in ax.spines.values():
            spine.set_color(THEME['spine'])
            spine.set_linewidth(0.5)
        ax.grid(False)

    # Axis 1 (LHS - Secondary)
    ax1.tick_params(axis='both', which='both', length=0, colors=THEME['muted'])
    ax1.tick_params(axis='y', labelcolor=c1, labelsize=10)
    ax1.tick_params(axis='x', labelsize=10, labelcolor=THEME['muted'])

    # Axis 2 (RHS - Primary)
    ax2.tick_params(axis='both', which='both', length=0, colors=THEME['muted'])
    ax2.tick_params(axis='y', labelcolor=c2, labelsize=10)


def set_xlim_to_data(ax, idx, padding_left_days=0):
    """Set x-axis limits with optional left padding and ~2 month right padding."""
    padding_left = pd.Timedelta(days=padding_left_days)
    padding_right = pd.Timedelta(days=54)  # Extends to ~March 31, 2026
    ax.set_xlim(idx.min() - padding_left, idx.max() + padding_right)


def add_last_value_label(ax, y_val, color, fmt='{:.1f}', side='right', fontsize=9, pad=0.3):
    """Add colored pill on axis edge."""
    label = fmt.format(y_val)
    pill = dict(boxstyle=f'round,pad={pad}', facecolor=color, edgecolor=color, alpha=0.95)

    if side == 'right':
        ax.annotate(label, xy=(1.0, y_val), xycoords=('axes fraction', 'data'),
                    fontsize=fontsize, fontweight='bold', color='white',
                    ha='left', va='center', xytext=(6, 0), textcoords='offset points', bbox=pill)
    else:
        ax.annotate(label, xy=(0.0, y_val), xycoords=('axes fraction', 'data'),
                    fontsize=fontsize, fontweight='bold', color='white',
                    ha='right', va='center', xytext=(-6, 0), textcoords='offset points', bbox=pill)


def brand_fig(fig, title, subtitle, source='Lighthouse Macro'):
    """Apply all figure-level branding (watermarks, bars, title)."""
    # Top accent bar (Ocean 2/3, Dusk 1/3) - FIRST so titles go on top
    ax_top = fig.add_axes([0.03, 0.96, 0.94, 0.004])
    ax_top.axhspan(0, 1, 0, 0.67, color=COLORS['ocean'])
    ax_top.axhspan(0, 1, 0.67, 1.0, color=COLORS['dusk'])
    ax_top.set_xlim(0, 1)
    ax_top.set_ylim(0, 1)
    ax_top.axis('off')

    # Bottom accent bar (mirror)
    ax_bot = fig.add_axes([0.03, 0.035, 0.94, 0.004])
    ax_bot.axhspan(0, 1, 0, 0.67, color=COLORS['ocean'])
    ax_bot.axhspan(0, 1, 0.67, 1.0, color=COLORS['dusk'])
    ax_bot.set_xlim(0, 1)
    ax_bot.set_ylim(0, 1)
    ax_bot.axis('off')

    # Top-left: LIGHTHOUSE MACRO
    fig.text(0.06, 0.98, 'LIGHTHOUSE MACRO', fontsize=13, fontweight='bold', color=COLORS['ocean'])

    # Top-right: Date
    fig.text(0.94, 0.98, 'February 05, 2026', fontsize=11, color=THEME['muted'], ha='right')

    # Title and Subtitle - adjusted positions
    fig.text(0.50, 0.93, title, fontsize=16, fontweight='bold', color=THEME['fg'], ha='center')
    fig.text(0.50, 0.895, subtitle, fontsize=12, style='italic', color=COLORS['ocean'], ha='center')

    # Bottom-right: Tagline
    fig.text(0.94, 0.015, 'MACRO, ILLUMINATED.', fontsize=13, fontweight='bold',
             style='italic', color=COLORS['ocean'], ha='right')

    # Bottom-left: Source
    fig.text(0.06, 0.015, f'Lighthouse Macro | {source}; 02.05.2026',
             fontsize=9, style='italic', color=THEME['muted'])


def add_outer_border(fig):
    """Add 1.5pt border at absolute figure edge."""
    fig.patches.append(plt.Rectangle(
        (0, 0), 1, 1, transform=fig.transFigure,
        fill=False, edgecolor=THEME['spine'], linewidth=1.5,
        zorder=100, clip_on=False
    ))


def add_annotation_box(ax, text, x=0.52, y=0.08):
    """Add takeaway box - default to bottom of chart area."""
    ax.text(x, y, text, transform=ax.transAxes,
            fontsize=10, color=THEME['fg'], ha='center', va='bottom', style='italic',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=THEME['bg'],
                      edgecolor=COLORS['ocean'], alpha=0.9))


def legend_style():
    """Return legend kwargs dict."""
    return dict(
        framealpha=0.95,
        facecolor=THEME['legend_bg'],
        edgecolor=THEME['spine'],
        labelcolor=THEME['legend_fg'],
    )


def save_fig(fig, name):
    """Save with standard settings."""
    path = OUTPUT_DIR / f'{name}.png'
    fig.savefig(path, dpi=200, bbox_inches='tight', pad_inches=0.15,
                facecolor=THEME['bg'], edgecolor='none')
    print(f"Saved: {path}")
    plt.close(fig)


# ———————— CHART 1: ETF FLOWS VS PRICE ————————
def chart_01_etf_flows():
    """The Spot Capitulation - ETF Flows vs BTC Price"""
    fig, ax1 = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(THEME['bg'])
    ax2 = ax1.twinx()

    c_secondary = THEME['secondary']  # Dusk - LHS
    c_primary = THEME['primary']      # Sky - RHS

    # LHS: Cumulative Flows (Dusk - Secondary)
    ax1.fill_between(df.index, df['Cumulative_Flows'], 0, color=c_secondary, alpha=0.15)
    l1, = ax1.plot(df.index, df['Cumulative_Flows'], color=c_secondary, linewidth=1.5,
                   label=f'Cum. Net ETF Flows (${df["Cumulative_Flows"].iloc[-1]:,.0f}M)')

    # RHS: Price (Sky - Primary)
    l2, = ax2.plot(df.index, df['BTC_Price'], color=c_primary, linewidth=2,
                   label=f'BTC Price (${df["BTC_Price"].iloc[-1]:,.0f})')

    # Styling
    style_dual_ax(ax1, ax2, c_secondary, c_primary)

    # Y-axis formatters
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x/1000:.0f}B' if abs(x) >= 1000 else f'${x:.0f}M'))
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))

    # Set limits with padding
    flow_min = df['Cumulative_Flows'].min()
    flow_max = df['Cumulative_Flows'].max()
    ax1.set_ylim(min(0, flow_min * 1.1), flow_max * 1.15)
    ax2.set_ylim(df['BTC_Price'].min() * 0.9, df['BTC_Price'].max() * 1.1)
    set_xlim_to_data(ax1, df.index, padding_left_days=0)

    # Pills
    add_last_value_label(ax1, df['Cumulative_Flows'].iloc[-1], c_secondary, fmt='${:,.0f}M', side='left')
    add_last_value_label(ax2, df['BTC_Price'].iloc[-1], c_primary, fmt='${:,.0f}', side='right')

    # Calculate stats for annotation
    peak_idx = df['Cumulative_Flows'].idxmax()
    peak_flows = df['Cumulative_Flows'].max()
    current_flows = df['Cumulative_Flows'].iloc[-1]
    outflows_since_peak = current_flows - peak_flows

    price_at_peak = df.loc[peak_idx, 'BTC_Price']
    current_price = df['BTC_Price'].iloc[-1]
    price_drawdown = (current_price - price_at_peak) / price_at_peak * 100

    # Branding
    brand_fig(fig, 'THE SPOT CAPITULATION', 'Cumulative ETF Flows vs. BTC Price', source='Farside Investors, Yahoo Finance')
    add_annotation_box(ax1, f"Outflows since peak: ${outflows_since_peak:,.0f}M  |  Price vs. peak: {price_drawdown:+.1f}%", x=0.5, y=0.03)

    # Legend
    lines = [l1, l2]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', **legend_style())

    # Margins and border
    fig.subplots_adjust(top=0.86, bottom=0.10, left=0.06, right=0.94)
    add_outer_border(fig)

    save_fig(fig, 'chart_01_etf_flows_vs_price')


# ———————— CHART 2: FLOW MOMENTUM ————————
def chart_02_flow_momentum():
    """Flow Momentum - 20-day rolling sum of daily flows"""
    fig, ax1 = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(THEME['bg'])
    ax2 = ax1.twinx()

    c_secondary = THEME['secondary']  # Dusk - LHS
    c_primary = THEME['primary']      # Sky - RHS

    # Calculate 30-day rolling sum
    df['Flow_30d'] = df['Total'].rolling(30).sum()

    # LHS: 30-day flow momentum (Dusk - Secondary)
    ax1.fill_between(df.index, df['Flow_30d'], 0,
                     where=df['Flow_30d'] >= 0, color=COLORS['sea'], alpha=0.3)
    ax1.fill_between(df.index, df['Flow_30d'], 0,
                     where=df['Flow_30d'] < 0, color=COLORS['venus'], alpha=0.3)
    l1, = ax1.plot(df.index, df['Flow_30d'], color=c_secondary, linewidth=1.5,
                   label=f'30-Day Flow Sum (${df["Flow_30d"].iloc[-1]:,.0f}M)')

    # RHS: Price (Sky - Primary)
    l2, = ax2.plot(df.index, df['BTC_Price'], color=c_primary, linewidth=2,
                   label=f'BTC Price (${df["BTC_Price"].iloc[-1]:,.0f})')

    # Zero line
    ax1.axhline(0, color=COLORS['doldrums'], linewidth=1, linestyle='--', alpha=0.5)

    # Styling
    style_dual_ax(ax1, ax2, c_secondary, c_primary)

    # Y-axis formatters
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x/1000:.1f}B' if abs(x) >= 1000 else f'${x:.0f}M'))
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))

    # Set limits
    flow_min = df['Flow_30d'].min()
    flow_max = df['Flow_30d'].max()
    ax1.set_ylim(flow_min * 1.2, flow_max * 1.2)
    ax2.set_ylim(df['BTC_Price'].min() * 0.9, df['BTC_Price'].max() * 1.1)
    set_xlim_to_data(ax1, df.index, padding_left_days=0)

    # Pills
    add_last_value_label(ax1, df['Flow_30d'].iloc[-1], c_secondary, fmt='${:,.0f}M', side='left')
    add_last_value_label(ax2, df['BTC_Price'].iloc[-1], c_primary, fmt='${:,.0f}', side='right')

    # Branding
    brand_fig(fig, 'FLOW MOMENTUM', '30-Day Rolling Flow Sum vs. BTC Price', source='Farside Investors, Yahoo Finance')

    # Count days of negative momentum
    recent_neg = (df['Flow_30d'].iloc[-30:] < 0).sum()
    add_annotation_box(ax1, f"Negative momentum: {recent_neg}/30 recent days", x=0.5, y=0.03)

    # Legend
    lines = [l1, l2]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', **legend_style())

    # Margins and border
    fig.subplots_adjust(top=0.86, bottom=0.10, left=0.06, right=0.94)
    add_outer_border(fig)

    save_fig(fig, 'chart_02_flow_momentum')


# ———————— CHART 3: ON-CHAIN REALITY ————————
def chart_03_onchain():
    """The On-Chain Reality - Base Chain TVL Growth"""
    if df_onchain is None:
        print("Skipping chart 3 - no on-chain data available")
        return

    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(THEME['bg'])

    # Filter for last 12 months
    cutoff = df_onchain.index.max() - pd.Timedelta(days=365)
    df_recent = df_onchain[df_onchain.index >= cutoff].copy()

    c_primary = THEME['primary']  # Ocean

    # Single axis: Base TVL
    ax.fill_between(df_recent.index, df_recent['Base_TVL'], 0, color=c_primary, alpha=0.15)
    l1, = ax.plot(df_recent.index, df_recent['Base_TVL'], color=c_primary, linewidth=2,
                  label=f'Base Chain TVL (${df_recent["Base_TVL"].iloc[-1]:.1f}B)')

    # Styling
    style_ax(ax)
    ax.set_facecolor(THEME['bg'])

    # Y-axis formatter
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x:.1f}B'))
    ax.tick_params(axis='y', labelcolor=c_primary, labelsize=10)

    # Set limits
    ax.set_ylim(0, df_recent['Base_TVL'].max() * 1.2)
    set_xlim_to_data(ax, df_recent.index, padding_left_days=0)

    # Pill
    add_last_value_label(ax, df_recent['Base_TVL'].iloc[-1], c_primary, fmt='${:.1f}B', side='right')

    # Calculate growth
    start_tvl = df_recent['Base_TVL'].iloc[0]
    end_tvl = df_recent['Base_TVL'].iloc[-1]
    growth_pct = (end_tvl - start_tvl) / start_tvl * 100

    # Branding
    brand_fig(fig, 'THE ON-CHAIN REALITY', 'Base Chain Total Value Locked', source='DefiLlama')
    add_annotation_box(ax, f"12-month TVL growth: +{growth_pct:.0f}%  |  Price falls, infrastructure grows.", x=0.5, y=0.03)

    # Legend
    ax.legend(loc='upper left', **legend_style())

    # Margins and border
    fig.subplots_adjust(top=0.86, bottom=0.10, left=0.06, right=0.94)
    add_outer_border(fig)

    save_fig(fig, 'chart_03_onchain_reality')


# ———————— CHART 4: GBTC VS REST ————————
def chart_04_gbtc_vs_rest():
    """GBTC Exodus - Cumulative GBTC outflows vs rest of field inflows"""
    # Need raw flows data
    flows_raw = load_etf_flows()

    fig, ax1 = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(THEME['bg'])
    ax2 = ax1.twinx()

    c_secondary = THEME['secondary']  # Dusk - LHS (GBTC)
    c_primary = THEME['primary']      # Ocean - RHS (Rest)

    # Calculate cumulative flows
    gbtc_cum = flows_raw['GBTC'].cumsum()
    rest_cols = [c for c in flows_raw.columns if c not in ['GBTC', 'Total', 'BTC', 'Cumulative_Flows']]
    rest_cum = flows_raw[rest_cols].sum(axis=1).cumsum()

    # LHS: GBTC cumulative (Dusk - will be negative)
    ax1.fill_between(gbtc_cum.index, gbtc_cum, 0, color=c_secondary, alpha=0.15)
    l1, = ax1.plot(gbtc_cum.index, gbtc_cum, color=c_secondary, linewidth=2,
                   label=f'GBTC Cum. Flows (${gbtc_cum.iloc[-1]/1000:.1f}B)')

    # RHS: Rest of field cumulative (Ocean - positive)
    ax2.fill_between(rest_cum.index, rest_cum, 0, color=c_primary, alpha=0.15)
    l2, = ax2.plot(rest_cum.index, rest_cum, color=c_primary, linewidth=2,
                   label=f'All Other ETFs (${rest_cum.iloc[-1]/1000:.1f}B)')

    # Zero lines
    ax1.axhline(0, color=COLORS['doldrums'], linewidth=0.8, linestyle='--', alpha=0.5)

    # Styling
    style_dual_ax(ax1, ax2, c_secondary, c_primary)

    # Y-axis formatters
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x/1000:.0f}B'))
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x/1000:.0f}B'))

    # Set limits
    ax1.set_ylim(gbtc_cum.min() * 1.1, gbtc_cum.max() * 0.5 if gbtc_cum.max() > 0 else 1000)
    ax2.set_ylim(0, rest_cum.max() * 1.15)
    set_xlim_to_data(ax1, gbtc_cum.index, padding_left_days=0)

    # Pills
    add_last_value_label(ax1, gbtc_cum.iloc[-1], c_secondary, fmt='${:,.0f}M', side='left')
    add_last_value_label(ax2, rest_cum.iloc[-1], c_primary, fmt='${:,.0f}M', side='right')

    # Branding
    brand_fig(fig, 'THE GBTC EXODUS', 'Grayscale Outflows vs. New ETF Inflows', source='Farside Investors')
    add_annotation_box(ax1, f"GBTC: ${gbtc_cum.iloc[-1]/1000:.1f}B out  |  Others: +${rest_cum.iloc[-1]/1000:.1f}B in", x=0.5, y=0.03)

    # Legend
    lines = [l1, l2]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', **legend_style())

    # Margins and border
    fig.subplots_adjust(top=0.86, bottom=0.10, left=0.06, right=0.94)
    add_outer_border(fig)

    save_fig(fig, 'chart_04_gbtc_vs_rest')


# ———————— CHART 5: LARGEST SINGLE-DAY FLOWS ————————
def chart_05_largest_flows():
    """Top 10 Largest Inflows and Outflows"""
    flows_raw = load_etf_flows()

    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(THEME['bg'])

    # Get top 10 inflows and outflows
    top_inflows = flows_raw['Total'].nlargest(10)
    top_outflows = flows_raw['Total'].nsmallest(10)

    # Combine and sort by absolute value
    combined = pd.concat([top_inflows, top_outflows]).sort_values()

    # Colors based on sign
    colors = [COLORS['venus'] if v < 0 else COLORS['sea'] for v in combined.values]

    # Horizontal bar chart
    y_pos = np.arange(len(combined))
    bars = ax.barh(y_pos, combined.values, color=colors, alpha=0.8, height=0.7)

    # Format y-axis labels as dates
    date_labels = [d.strftime('%b %d, %Y') for d in combined.index]
    ax.set_yticks(y_pos)
    ax.set_yticklabels(date_labels, fontsize=9, color=THEME['fg'])

    # Zero line
    ax.axvline(0, color=COLORS['doldrums'], linewidth=1, linestyle='-', alpha=0.7)

    # Styling
    ax.set_facecolor(THEME['bg'])
    for spine in ax.spines.values():
        spine.set_color(THEME['spine'])
        spine.set_linewidth(0.5)
    ax.tick_params(axis='both', which='both', length=0, colors=THEME['muted'])
    ax.tick_params(axis='x', labelsize=10, labelcolor=THEME['muted'])

    # X-axis formatter
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x/1000:.1f}B' if abs(x) >= 1000 else f'${x:.0f}M'))

    # Add value labels on bars
    for bar, val in zip(bars, combined.values):
        x_pos = val + (50 if val > 0 else -50)
        ha = 'left' if val > 0 else 'right'
        ax.text(x_pos, bar.get_y() + bar.get_height()/2,
                f'${val:,.0f}M', va='center', ha=ha,
                fontsize=8, color=THEME['fg'], fontweight='bold')

    # Branding
    brand_fig(fig, 'EXTREME FLOW DAYS', 'Top 10 Largest Daily Inflows & Outflows', source='Farside Investors')

    # Find the biggest outflow
    worst_day = flows_raw['Total'].idxmin()
    worst_val = flows_raw['Total'].min()
    add_annotation_box(ax, f"Largest outflow: ${worst_val:,.0f}M on {worst_day.strftime('%b %d, %Y')}", x=0.25, y=0.03)

    # Margins and border
    fig.subplots_adjust(top=0.86, bottom=0.10, left=0.15, right=0.94)
    add_outer_border(fig)

    save_fig(fig, 'chart_05_largest_flows')


# ———————— CHART 6: DAILY FLOWS WITH ±2 STDEV BANDS ————————
def chart_06_flow_bands():
    """Daily Flows with Historical ±2 Std Dev Bands"""
    flows_raw = load_etf_flows()

    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(THEME['bg'])

    c_primary = THEME['primary']  # Ocean

    # Calculate rolling mean and std (use 60-day for smoother bands)
    window = 60
    roll_mean = flows_raw['Total'].rolling(window).mean()
    roll_std = flows_raw['Total'].rolling(window).std()

    upper_2 = roll_mean + 2 * roll_std
    lower_2 = roll_mean - 2 * roll_std

    # Plot bands
    ax.fill_between(flows_raw.index, lower_2, upper_2, color=c_primary, alpha=0.15, label='±2σ Band')

    # Plot daily flows as bars (colored by sign)
    pos_mask = flows_raw['Total'] >= 0
    neg_mask = flows_raw['Total'] < 0

    ax.bar(flows_raw.index[pos_mask], flows_raw['Total'][pos_mask],
           color=COLORS['sea'], alpha=0.7, width=1)
    ax.bar(flows_raw.index[neg_mask], flows_raw['Total'][neg_mask],
           color=COLORS['venus'], alpha=0.7, width=1)

    # Plot rolling mean
    l1, = ax.plot(roll_mean.index, roll_mean, color=c_primary, linewidth=1.5,
                  label=f'60-Day Mean (${roll_mean.iloc[-1]:,.0f}M)')

    # Zero line
    ax.axhline(0, color=COLORS['doldrums'], linewidth=1, linestyle='--', alpha=0.5)

    # Styling
    style_ax(ax)
    ax.set_facecolor(THEME['bg'])
    ax.tick_params(axis='y', labelcolor=c_primary, labelsize=10)

    # Y-axis formatter
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x/1000:.1f}B' if abs(x) >= 1000 else f'${x:.0f}M'))

    # Set limits
    y_max = max(upper_2.max(), flows_raw['Total'].max()) * 1.1
    y_min = min(lower_2.min(), flows_raw['Total'].min()) * 1.1
    ax.set_ylim(y_min, y_max)
    set_xlim_to_data(ax, flows_raw.index, padding_left_days=0)

    # Count outliers
    recent_90 = flows_raw['Total'].iloc[-90:]
    recent_upper = upper_2.iloc[-90:]
    recent_lower = lower_2.iloc[-90:]
    outliers_up = (recent_90 > recent_upper).sum()
    outliers_down = (recent_90 < recent_lower).sum()

    # Branding
    brand_fig(fig, 'FLOW VOLATILITY', 'Daily Flows with ±2σ Historical Bands', source='Farside Investors')
    add_annotation_box(ax, f"Last 90 days: {outliers_up} above +2σ, {outliers_down} below -2σ", x=0.5, y=0.03)

    # Legend
    ax.legend(loc='upper left', **legend_style())

    # Margins and border
    fig.subplots_adjust(top=0.86, bottom=0.10, left=0.06, right=0.94)
    add_outer_border(fig)

    save_fig(fig, 'chart_06_flow_bands')


# ———————— MAIN ————————
if __name__ == '__main__':
    print("\nGenerating BTC ETF charts with REAL data...")
    chart_01_etf_flows()
    chart_02_flow_momentum()
    chart_03_onchain()
    chart_04_gbtc_vs_rest()
    chart_05_largest_flows()
    chart_06_flow_bands()
    print("Done.")
