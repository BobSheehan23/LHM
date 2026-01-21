"""
THE HORIZON - CHART LIBRARY
Lighthouse Macro | December 2025

Production-ready charts using REAL DATA from FRED and Yahoo Finance.
Charts tell the story OF the data - no synthetic placeholders.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# DATA FETCHING INFRASTRUCTURE
# ============================================================================

try:
    import yfinance as yf
except ImportError:
    yf = None
    print("Warning: yfinance not installed. Run: pip install yfinance")

try:
    from fredapi import Fred
except ImportError:
    Fred = None
    print("Warning: fredapi not installed. Run: pip install fredapi")

import os

FRED_API_KEY = os.environ.get('FRED_API_KEY', '')


class DataFetcher:
    """Centralized data fetcher - REAL DATA ONLY."""

    def __init__(self, fred_api_key: Optional[str] = None):
        self.fred_api_key = fred_api_key or FRED_API_KEY
        self._fred = None
        self._cache = {}

    @property
    def fred(self):
        if self._fred is None and Fred and self.fred_api_key:
            self._fred = Fred(api_key=self.fred_api_key)
        return self._fred

    def get_fred_series(self, series_id: str, start_date: str = '2000-01-01') -> pd.Series:
        cache_key = f"fred_{series_id}_{start_date}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        if self.fred is None:
            raise ValueError("FRED API not available. Set FRED_API_KEY.")
        data = self.fred.get_series(series_id, observation_start=start_date)
        self._cache[cache_key] = data
        return data

    def get_yahoo_data(self, ticker: str, start: str = '2000-01-01') -> pd.DataFrame:
        if yf is None:
            raise ImportError("yfinance not installed")
        end = datetime.now().strftime('%Y-%m-%d')
        cache_key = f"yf_{ticker}_{start}_{end}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        data = yf.download(ticker, start=start, end=end, progress=False)
        self._cache[cache_key] = data
        return data


_fetcher = None

def get_fetcher() -> DataFetcher:
    global _fetcher
    if _fetcher is None:
        _fetcher = DataFetcher()
    return _fetcher


# ============================================================================
# LHM COLOR PALETTE & STYLING
# ============================================================================

# LHM 8-COLOR PALETTE (from CLAUDE.md visual standards)
LHM_COLORS = {
    'ocean': '#0089D1',      # Ocean Blue - Primary data series
    'dusk': '#FF6723',       # Dusk Orange - Secondary / Warning thresholds
    'electric': '#03DDFF',   # Electric Cyan - Volatility / Highlights
    'hot': '#FF00F0',        # Hot Magenta - Extreme stress / Attention
    'sea': '#289389',        # Sea Teal - Neutral / Balanced
    'silvs': '#D1D1D1',      # Silvs Gray - Reference lines / Background
    'down_red': '#FF3333',   # Down Red - Bearish / Danger
    'up_green': '#008000'    # Up Green - Bullish (corrected from #00CC66)
}

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 10


def apply_lhm_style(ax):
    """Apply LHM visual standards: no gridlines, clean spines"""
    # Remove gridlines (LHM standard)
    ax.grid(False)
    # Clean spines - keep only left and bottom
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(LHM_COLORS['silvs'])
    ax.spines['bottom'].set_color(LHM_COLORS['silvs'])
    ax.tick_params(colors=LHM_COLORS['silvs'])


def smart_annotate(ax, text, xy, data_series=None, prefer_side='right'):
    """
    Smart annotation that avoids overlapping with data.
    prefer_side: 'left', 'right', 'above', 'below'
    """
    x, y = xy

    # Base offsets depending on preferred side
    offsets = {
        'right': (60, 0),
        'left': (-120, 0),
        'above': (0, 40),
        'below': (0, -50)
    }

    offset = offsets.get(prefer_side, (60, 0))

    # Check if we need to flip (if annotation would go off chart)
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # For time series, check if we're near right edge
    if hasattr(x, 'timestamp'):
        x_num = x.timestamp()
        xlim_right = xlim[1]
        if isinstance(xlim_right, (int, float)):
            # Already numeric
            pass
        else:
            xlim_right = xlim_right.timestamp() if hasattr(xlim_right, 'timestamp') else xlim[1]

    ax.annotate(text, xy=xy, xytext=offset, textcoords='offset points',
                fontsize=10, fontweight='bold', color=LHM_COLORS['hot'],
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                         edgecolor=LHM_COLORS['hot'], linewidth=1.5, alpha=0.95),
                arrowprops=dict(arrowstyle='->', color=LHM_COLORS['hot'], lw=1.5))


def add_lighthouse_branding(fig, position='both'):
    if position in ['both', 'top-left']:
        fig.text(0.01, 0.995, 'LIGHTHOUSE MACRO',
                fontsize=9, fontweight='bold',
                color=LHM_COLORS['ocean'], alpha=0.8,
                verticalalignment='top', horizontalalignment='left')
    if position in ['both', 'bottom-right']:
        fig.text(0.99, 0.005, 'MACRO, ILLUMINATED.',
                fontsize=8, style='italic',
                color=LHM_COLORS['silvs'], alpha=0.7,
                verticalalignment='bottom', horizontalalignment='right')


def add_recession_shading(ax, start_date='2000-01-01'):
    recessions = [
        ('2001-03-01', '2001-11-01'),
        ('2007-12-01', '2009-06-01'),
        ('2020-02-01', '2020-04-01')
    ]
    for start, end in recessions:
        if pd.to_datetime(start) >= pd.to_datetime(start_date):
            ax.axvspan(pd.to_datetime(start), pd.to_datetime(end),
                      alpha=0.15, color=LHM_COLORS['silvs'])


# ============================================================================
# CHART 1: ON RRP DRAWDOWN - REAL FRED DATA
# ============================================================================

def chart_01_rrp_drawdown():
    """ON RRP Drawdown using REAL FRED data (RRPONTSYD)"""
    fetcher = get_fetcher()

    # REAL DATA
    rrp = fetcher.get_fred_series('RRPONTSYD', '2021-01-01')
    rrp_billions = rrp / 1000  # Convert millions to billions

    fig, ax = plt.subplots(figsize=(14, 8))

    # Plot actual data
    ax.fill_between(rrp_billions.index, 0, rrp_billions.values, alpha=0.3, color=LHM_COLORS['ocean'])
    ax.plot(rrp_billions.index, rrp_billions.values, linewidth=2.5, color=LHM_COLORS['ocean'], label='ON RRP Balance')

    # Calculate REAL statistics from data
    peak_val = rrp_billions.max()
    peak_date = rrp_billions.idxmax()
    current_val = rrp_billions.iloc[-1]
    current_date = rrp_billions.index[-1]
    pct_decline = ((peak_val - current_val) / peak_val) * 100
    months_since_peak = (current_date - peak_date).days / 30

    # Annotate Peak - position to the right of peak
    ax.annotate(f'Peak: ${peak_val:,.0f}B\n{peak_date.strftime("%b %Y")}',
                xy=(peak_date, peak_val), xytext=(80, -30),
                textcoords='offset points',
                arrowprops=dict(arrowstyle='->', color=LHM_COLORS['dusk'], lw=1.5),
                fontsize=10, fontweight='bold', color=LHM_COLORS['dusk'],
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=LHM_COLORS['dusk'], alpha=0.95))

    # Annotate Current - position to the LEFT since it's at right edge
    ax.annotate(f'Current: ${current_val:,.1f}B\n({pct_decline:.1f}% decline)',
                xy=(current_date, current_val), xytext=(-160, 60),
                textcoords='offset points',
                arrowprops=dict(arrowstyle='->', color=LHM_COLORS['down_red'], lw=1.5),
                fontsize=10, fontweight='bold', color=LHM_COLORS['down_red'],
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=LHM_COLORS['down_red'], alpha=0.95))

    ax.set_xlabel('', fontweight='bold')  # Remove redundant x-label
    ax.set_ylabel('ON RRP Balance ($ Billions)', fontweight='bold')
    ax.set_title('ON RRP Drawdown: The Buffer is Gone',
                 fontsize=14, fontweight='bold', pad=20)

    # Apply LHM styling (no gridlines, clean spines)
    apply_lhm_style(ax)
    ax.legend(loc='upper right', framealpha=0.95, frameon=False)

    # Stats box - positioned in upper left where there's space
    if months_since_peak > 0:
        avg_drain = (peak_val - current_val) / months_since_peak
    else:
        avg_drain = 0
    textstr = f'Peak: ${peak_val:,.0f}B ({peak_date.strftime("%b %Y")})\nCurrent: ${current_val:,.1f}B\nDecline: {pct_decline:.1f}%\nMonths: {months_since_peak:.0f}\nAvg drain: ${avg_drain:,.0f}B/mo'
    props = dict(boxstyle='round', facecolor='white', edgecolor=LHM_COLORS['ocean'], linewidth=2, alpha=0.95)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=props, family='monospace')

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


# ============================================================================
# CHART 2: RESERVES - REAL FRED DATA
# ============================================================================

def chart_02_liquidity_cushion_index():
    """Bank Reserves vs GDP - REAL FRED data"""
    fetcher = get_fetcher()

    # REAL DATA
    reserves = fetcher.get_fred_series('TOTRESNS', '2008-01-01')  # Total reserves
    gdp = fetcher.get_fred_series('GDP', '2008-01-01')  # Nominal GDP (quarterly)

    # Align to quarterly
    reserves_q = reserves.resample('Q').mean()
    gdp_aligned = gdp.reindex(reserves_q.index, method='ffill')

    # Calculate ratio (reserves in billions, GDP in billions)
    ratio = (reserves_q / gdp_aligned) * 100  # as percentage
    ratio = ratio.dropna()

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.fill_between(ratio.index, 0, ratio.values, alpha=0.3, color=LHM_COLORS['ocean'])
    ax.plot(ratio.index, ratio.values, linewidth=2.5, color=LHM_COLORS['ocean'], label='Reserves / GDP (%)')

    # REAL statistics
    current_val = ratio.iloc[-1]
    peak_val = ratio.max()
    peak_date = ratio.idxmax()

    # Sept 2019 value (if available)
    sept_2019 = ratio.loc['2019-09-01':'2019-12-31']
    if len(sept_2019) > 0:
        sept_2019_val = sept_2019.iloc[0]
        ax.axhline(sept_2019_val, color=LHM_COLORS['down_red'], linestyle='--',
                  linewidth=2, alpha=0.7, label=f'Sept 2019 level: {sept_2019_val:.1f}%')

    ax.scatter(ratio.index[-1], current_val, s=200, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=2.5, zorder=5)
    ax.annotate(f'Current: {current_val:.1f}%',
               xy=(ratio.index[-1], current_val), xytext=(-100, 30),
               textcoords='offset points', fontsize=10, fontweight='bold',
               color=LHM_COLORS['hot'],
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=LHM_COLORS['hot'], alpha=0.95))

    add_recession_shading(ax, '2008-01-01')

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('Bank Reserves as % of GDP', fontweight='bold')
    ax.set_title('Bank Reserves / GDP: Real FRED Data (TOTRESNS, GDP)',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards
    ax.legend(loc='upper left', framealpha=0.95)

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


# ============================================================================
# CHART 3: SOFR-EFFR SPREAD - REAL FRED DATA
# ============================================================================

def chart_03_sofr_effr_spread():
    """SOFR - EFFR Spread using REAL FRED data"""
    fetcher = get_fetcher()

    # REAL DATA
    sofr = fetcher.get_fred_series('SOFR', '2018-04-01')
    effr = fetcher.get_fred_series('EFFR', '2018-04-01')

    # Align and calculate spread
    combined = pd.DataFrame({'SOFR': sofr, 'EFFR': effr}).dropna()
    spread = (combined['SOFR'] - combined['EFFR']) * 100  # Convert to bps

    fig, ax = plt.subplots(figsize=(14, 8))

    # Color code by level
    for i in range(len(spread)-1):
        val = spread.iloc[i]
        color = (LHM_COLORS['ocean'] if val < 5
                else LHM_COLORS['dusk'] if val < 10
                else LHM_COLORS['down_red'])
        ax.plot(spread.index[i:i+2], spread.iloc[i:i+2], color=color, linewidth=1.5)

    # REAL statistics
    current = spread.iloc[-1]
    mean_spread = spread.mean()
    std_spread = spread.std()
    max_spread = spread.max()
    max_date = spread.idxmax()

    ax.axhline(mean_spread, color=LHM_COLORS['silvs'], linestyle='--',
              linewidth=1.5, alpha=0.7, label=f'Mean: {mean_spread:.1f} bps')

    ax.scatter(spread.index[-1], current, s=200, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=2.5, zorder=5)
    ax.annotate(f'Current: {current:.1f} bps',
               xy=(spread.index[-1], current), xytext=(-60, 30),
               textcoords='offset points', fontsize=10, fontweight='bold',
               color=LHM_COLORS['hot'],
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=LHM_COLORS['hot'], linewidth=1.5, alpha=0.95))

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('SOFR - EFFR Spread (basis points)', fontweight='bold')
    ax.set_title('SOFR-EFFR Spread: Real FRED Data',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards
    ax.legend(loc='upper left', framealpha=0.95)

    textstr = f'Mean: {mean_spread:.1f} bps\nStd: {std_spread:.1f} bps\nMax: {max_spread:.1f} bps ({max_date.strftime("%b %Y")})\nCurrent: {current:.1f} bps'
    props = dict(boxstyle='round', facecolor='white', edgecolor=LHM_COLORS['ocean'], linewidth=2, alpha=0.95)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=props, family='monospace')

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


# ============================================================================
# CHART 4: FEDERAL DEBT - REAL FRED DATA
# ============================================================================

def chart_04_reserves_vs_gdp():
    """Federal Debt using REAL FRED data"""
    fetcher = get_fetcher()

    # REAL DATA
    debt = fetcher.get_fred_series('GFDEBTN', '2000-01-01')  # Federal Debt Total
    gdp = fetcher.get_fred_series('GDP', '2000-01-01')

    # Align quarterly
    debt_q = debt.resample('Q').last()
    gdp_aligned = gdp.reindex(debt_q.index, method='ffill')

    # Debt to GDP ratio
    debt_gdp = (debt_q / gdp_aligned) * 100
    debt_gdp = debt_gdp.dropna()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Left: Debt levels (in trillions)
    debt_t = debt_q / 1000  # Convert to trillions
    ax1.fill_between(debt_t.index, 0, debt_t.values, alpha=0.3, color=LHM_COLORS['ocean'])
    ax1.plot(debt_t.index, debt_t.values, linewidth=2.5, color=LHM_COLORS['ocean'], label='Federal Debt')

    current_debt = debt_t.iloc[-1]
    ax1.scatter(debt_t.index[-1], current_debt, s=200, color=LHM_COLORS['hot'],
               edgecolors='white', linewidth=2.5, zorder=5)
    ax1.annotate(f'${current_debt:,.1f}T',
                xy=(debt_t.index[-1], current_debt), xytext=(-80, 30),
                textcoords='offset points', fontsize=11, fontweight='bold', color=LHM_COLORS['hot'],
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=LHM_COLORS['hot'], alpha=0.95))

    add_recession_shading(ax1, '2000-01-01')
    ax1.set_xlabel('Date', fontweight='bold')
    ax1.set_ylabel('Total Federal Debt ($ Trillions)', fontweight='bold')
    ax1.set_title('Federal Debt: Real FRED Data (GFDEBTN)', fontsize=13, fontweight='bold')
    apply_lhm_style(ax1)
    ax1.legend(loc='upper left', framealpha=0.95)

    # Right: Debt/GDP
    ax2.fill_between(debt_gdp.index, 0, debt_gdp.values, alpha=0.3, color=LHM_COLORS['dusk'])
    ax2.plot(debt_gdp.index, debt_gdp.values, linewidth=2.5, color=LHM_COLORS['dusk'])

    current_ratio = debt_gdp.iloc[-1]
    ax2.scatter(debt_gdp.index[-1], current_ratio, s=200, color=LHM_COLORS['hot'],
               edgecolors='white', linewidth=2.5, zorder=5)
    ax2.annotate(f'{current_ratio:.1f}%',
                xy=(debt_gdp.index[-1], current_ratio), xytext=(-80, 30),
                textcoords='offset points', fontsize=11, fontweight='bold', color=LHM_COLORS['hot'],
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=LHM_COLORS['hot'], alpha=0.95))

    ax2.axhline(100, color=LHM_COLORS['down_red'], linestyle='--', linewidth=2, alpha=0.7, label='100% threshold')

    add_recession_shading(ax2, '2000-01-01')
    ax2.set_xlabel('Date', fontweight='bold')
    ax2.set_ylabel('Debt-to-GDP Ratio (%)', fontweight='bold')
    ax2.set_title('Debt-to-GDP: Real FRED Data', fontsize=13, fontweight='bold')
    apply_lhm_style(ax2)
    ax2.legend(loc='upper left', framealpha=0.95)

    fig.suptitle('Federal Debt Analysis: Real Data', fontsize=16, fontweight='bold', y=0.98)
    add_lighthouse_branding(fig, position='bottom-right')
    plt.tight_layout()
    return fig


# ============================================================================
# CHART 5: INTEREST EXPENSE - REAL FRED DATA
# ============================================================================

def chart_05_srf_usage():
    """Interest Expense as % of Revenue - REAL FRED data"""
    fetcher = get_fetcher()

    # REAL DATA
    interest = fetcher.get_fred_series('A091RC1Q027SBEA', '1970-01-01')  # Interest payments
    revenue = fetcher.get_fred_series('FGRECPT', '1970-01-01')  # Federal receipts

    # Align quarterly
    interest_q = interest.resample('Q').last()
    revenue_q = revenue.resample('Q').last()

    combined = pd.DataFrame({'interest': interest_q, 'revenue': revenue_q}).dropna()
    ratio = (combined['interest'] / combined['revenue']) * 100

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.fill_between(ratio.index, 0, ratio.values, alpha=0.3, color=LHM_COLORS['dusk'])
    ax.plot(ratio.index, ratio.values, linewidth=2.5, color=LHM_COLORS['dusk'], label='Interest / Revenue')

    current = ratio.iloc[-1]
    peak = ratio.max()
    peak_date = ratio.idxmax()

    ax.scatter(ratio.index[-1], current, s=200, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=2.5, zorder=5)
    ax.annotate(f'Current: {current:.1f}%',
               xy=(ratio.index[-1], current), xytext=(30, 30),
               textcoords='offset points', fontsize=10, fontweight='bold',
               color=LHM_COLORS['hot'],
               arrowprops=dict(arrowstyle='->', color=LHM_COLORS['hot'], lw=2))

    ax.axhline(10, color=LHM_COLORS['down_red'], linestyle='--', linewidth=2, alpha=0.7, label='10% threshold')

    add_recession_shading(ax, '1970-01-01')

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('Net Interest as % of Federal Revenue', fontweight='bold')
    ax.set_title('Interest Expense: Real FRED Data (A091RC1Q027SBEA, FGRECPT)',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards
    ax.legend(loc='upper left', framealpha=0.95)

    textstr = f'Current: {current:.1f}%\nPeak: {peak:.1f}% ({peak_date.strftime("%b %Y")})\nMean: {ratio.mean():.1f}%'
    props = dict(boxstyle='round', facecolor='white', edgecolor=LHM_COLORS['ocean'], linewidth=2, alpha=0.95)
    ax.text(0.65, 0.35, textstr, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=props, family='monospace')

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


# ============================================================================
# CHART 6: TREASURY YIELDS - REAL FRED DATA
# ============================================================================

def chart_06_debt_trajectory():
    """Treasury Yield Curve - REAL FRED data"""
    fetcher = get_fetcher()

    # REAL DATA - multiple maturities
    yields = {}
    series = {'3M': 'DGS3MO', '2Y': 'DGS2', '5Y': 'DGS5', '10Y': 'DGS10', '30Y': 'DGS30'}
    for name, sid in series.items():
        yields[name] = fetcher.get_fred_series(sid, '2000-01-01')

    # 2s10s spread
    spread_2s10s = fetcher.get_fred_series('T10Y2Y', '2000-01-01')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Left: 2s10s spread
    ax1.fill_between(spread_2s10s.index, 0, spread_2s10s.values,
                    where=spread_2s10s.values >= 0, alpha=0.3, color=LHM_COLORS['ocean'])
    ax1.fill_between(spread_2s10s.index, 0, spread_2s10s.values,
                    where=spread_2s10s.values < 0, alpha=0.3, color=LHM_COLORS['down_red'])
    ax1.plot(spread_2s10s.index, spread_2s10s.values, linewidth=1.5, color=LHM_COLORS['ocean'])
    ax1.axhline(0, color='black', linewidth=1.5)

    current_spread = spread_2s10s.iloc[-1]
    ax1.scatter(spread_2s10s.index[-1], current_spread, s=200, color=LHM_COLORS['hot'],
               edgecolors='white', linewidth=2.5, zorder=5)
    ax1.annotate(f'{current_spread:.0f} bps',
                xy=(spread_2s10s.index[-1], current_spread), xytext=(10, 20),
                textcoords='offset points', fontsize=10, fontweight='bold', color=LHM_COLORS['hot'])

    add_recession_shading(ax1, '2000-01-01')
    ax1.set_xlabel('Date', fontweight='bold')
    ax1.set_ylabel('2s10s Spread (basis points)', fontweight='bold')
    ax1.set_title('2s10s Treasury Spread: Real FRED Data (T10Y2Y)', fontsize=13, fontweight='bold')
    apply_lhm_style(ax1)

    # Right: Current curve shape
    maturities = [0.25, 2, 5, 10, 30]
    mat_labels = ['3M', '2Y', '5Y', '10Y', '30Y']
    current_yields = [yields[m].iloc[-1] for m in mat_labels]

    ax2.plot(maturities, current_yields, linewidth=3, color=LHM_COLORS['ocean'],
            marker='o', markersize=10, label='Current Curve')

    for x, y, label in zip(maturities, current_yields, mat_labels):
        ax2.annotate(f'{y:.2f}%', xy=(x, y), xytext=(0, 10),
                    textcoords='offset points', fontsize=9, ha='center', fontweight='bold')

    ax2.set_xlabel('Maturity (Years)', fontweight='bold')
    ax2.set_ylabel('Yield (%)', fontweight='bold')
    ax2.set_title('Current Yield Curve Shape', fontsize=13, fontweight='bold')
    apply_lhm_style(ax2)
    ax2.legend(loc='lower right', framealpha=0.95)
    ax2.set_xlim(-1, 32)

    fig.suptitle('Treasury Yield Curve: Real FRED Data', fontsize=16, fontweight='bold', y=0.98)
    add_lighthouse_branding(fig, position='bottom-right')
    plt.tight_layout()
    return fig


# ============================================================================
# CHART 7: HY SPREADS - REAL FRED DATA
# ============================================================================

def chart_07_interest_expense():
    """High Yield Spreads - REAL FRED data"""
    fetcher = get_fetcher()

    # REAL DATA
    hy_oas = fetcher.get_fred_series('BAMLH0A0HYM2', '2000-01-01')

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.fill_between(hy_oas.index, 0, hy_oas.values, alpha=0.3, color=LHM_COLORS['dusk'])
    ax.plot(hy_oas.index, hy_oas.values, linewidth=2, color=LHM_COLORS['dusk'], label='HY OAS')

    # REAL statistics
    current = hy_oas.iloc[-1]
    mean_oas = hy_oas.mean()
    median_oas = hy_oas.median()
    percentile = (hy_oas < current).mean() * 100
    peak = hy_oas.max()
    peak_date = hy_oas.idxmax()

    ax.axhline(mean_oas, color=LHM_COLORS['silvs'], linestyle='--',
              linewidth=2, alpha=0.7, label=f'Mean: {mean_oas:.0f} bps')

    ax.scatter(hy_oas.index[-1], current, s=300, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=3, zorder=5)
    ax.annotate(f'Current: {current:.0f} bps\n{percentile:.0f}th percentile',
               xy=(hy_oas.index[-1], current), xytext=(-120, 80),
               textcoords='offset points', fontsize=11, fontweight='bold',
               color=LHM_COLORS['hot'],
               arrowprops=dict(arrowstyle='->', color=LHM_COLORS['hot'], lw=2),
               bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                        edgecolor=LHM_COLORS['hot'], linewidth=2, alpha=0.95))

    add_recession_shading(ax, '2000-01-01')

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('High Yield OAS (basis points)', fontweight='bold')
    ax.set_title('High Yield Spreads: Real FRED Data (BAMLH0A0HYM2)',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards
    ax.legend(loc='upper right', framealpha=0.95)

    textstr = f'Current: {current:.0f} bps\nMean: {mean_oas:.0f} bps\nMedian: {median_oas:.0f} bps\nPercentile: {percentile:.0f}th\nPeak: {peak:.0f} bps ({peak_date.strftime("%b %Y")})'
    props = dict(boxstyle='round', facecolor='white', edgecolor=LHM_COLORS['ocean'], linewidth=2, alpha=0.95)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=props, family='monospace')

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


# ============================================================================
# CHART 8: QUITS RATE - REAL FRED DATA
# ============================================================================

def chart_08_term_premium():
    """Quits Rate - REAL FRED data"""
    fetcher = get_fetcher()

    # REAL DATA
    quits = fetcher.get_fred_series('JTSQUR', '2001-01-01')

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.fill_between(quits.index, 0, quits.values, alpha=0.3, color=LHM_COLORS['ocean'])
    ax.plot(quits.index, quits.values, linewidth=2.5, color=LHM_COLORS['ocean'], label='Quits Rate')

    # REAL statistics
    current = quits.iloc[-1]
    mean_quits = quits.mean()
    peak = quits.max()
    peak_date = quits.idxmax()
    trough = quits.min()
    trough_date = quits.idxmin()

    # Pre-COVID average (2015-2019)
    pre_covid = quits.loc['2015-01-01':'2019-12-31'].mean()
    ax.axhline(pre_covid, color=LHM_COLORS['silvs'], linestyle='--',
              linewidth=2, alpha=0.7, label=f'Pre-COVID avg: {pre_covid:.1f}%')

    ax.scatter(quits.index[-1], current, s=250, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=2.5, zorder=5)
    ax.annotate(f'Current: {current:.1f}%',
               xy=(quits.index[-1], current), xytext=(-80, -40),
               textcoords='offset points', fontsize=10, fontweight='bold',
               color=LHM_COLORS['hot'],
               arrowprops=dict(arrowstyle='->', color=LHM_COLORS['hot'], lw=2))

    # Peak annotation
    ax.annotate(f'Peak: {peak:.1f}%\n{peak_date.strftime("%b %Y")}',
               xy=(peak_date, peak), xytext=(20, 10),
               textcoords='offset points', fontsize=9, fontweight='bold',
               color=LHM_COLORS['up_green'])

    add_recession_shading(ax, '2001-01-01')

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('Quits Rate (% of Employment)', fontweight='bold')
    ax.set_title('JOLTS Quits Rate: Real FRED Data (JTSQUR)',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards
    ax.legend(loc='upper right', framealpha=0.95)

    textstr = f'Current: {current:.1f}%\nPre-COVID avg: {pre_covid:.1f}%\nPeak: {peak:.1f}% ({peak_date.strftime("%b %Y")})\nTrough: {trough:.1f}% ({trough_date.strftime("%b %Y")})'
    props = dict(boxstyle='round', facecolor='white', edgecolor=LHM_COLORS['ocean'], linewidth=2, alpha=0.95)
    ax.text(0.02, 0.35, textstr, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=props, family='monospace')

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


# ============================================================================
# CHART 9: UNEMPLOYMENT - REAL FRED DATA
# ============================================================================

def chart_09_foreign_holdings():
    """Unemployment Rate - REAL FRED data"""
    fetcher = get_fetcher()

    # REAL DATA
    unrate = fetcher.get_fred_series('UNRATE', '2000-01-01')

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.fill_between(unrate.index, 0, unrate.values, alpha=0.3, color=LHM_COLORS['ocean'])
    ax.plot(unrate.index, unrate.values, linewidth=2.5, color=LHM_COLORS['ocean'], label='Unemployment Rate')

    current = unrate.iloc[-1]
    mean_rate = unrate.mean()
    peak = unrate.max()
    peak_date = unrate.idxmax()
    trough = unrate.min()
    trough_date = unrate.idxmin()

    ax.axhline(mean_rate, color=LHM_COLORS['silvs'], linestyle='--',
              linewidth=2, alpha=0.7, label=f'Mean: {mean_rate:.1f}%')

    ax.scatter(unrate.index[-1], current, s=250, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=2.5, zorder=5)
    ax.annotate(f'Current: {current:.1f}%',
               xy=(unrate.index[-1], current), xytext=(-100, 30),
               textcoords='offset points', fontsize=10, fontweight='bold',
               color=LHM_COLORS['hot'],
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=LHM_COLORS['hot'], alpha=0.95))

    add_recession_shading(ax, '2000-01-01')

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('Unemployment Rate (%)', fontweight='bold')
    ax.set_title('Unemployment Rate: Real FRED Data (UNRATE)',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards
    ax.legend(loc='upper right', framealpha=0.95)

    textstr = f'Current: {current:.1f}%\nMean: {mean_rate:.1f}%\nPeak: {peak:.1f}% ({peak_date.strftime("%b %Y")})\nTrough: {trough:.1f}% ({trough_date.strftime("%b %Y")})'
    props = dict(boxstyle='round', facecolor='white', edgecolor=LHM_COLORS['ocean'], linewidth=2, alpha=0.95)
    ax.text(0.65, 0.95, textstr, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=props, family='monospace')

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


# ============================================================================
# CHART 10: S&P 500 - REAL YAHOO DATA
# ============================================================================

def chart_10_maturity_wall():
    """S&P 500 Performance - REAL Yahoo data"""
    fetcher = get_fetcher()

    # REAL DATA
    spx = fetcher.get_yahoo_data('^GSPC', '2000-01-01')

    # Handle multi-index columns
    if isinstance(spx.columns, pd.MultiIndex):
        close = spx['Close']['^GSPC'] if '^GSPC' in spx['Close'].columns else spx['Close'].iloc[:, 0]
    else:
        close = spx['Close']
    close = close.dropna()

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.fill_between(close.index, 0, close.values, alpha=0.3, color=LHM_COLORS['ocean'])
    ax.plot(close.index, close.values, linewidth=2, color=LHM_COLORS['ocean'], label='S&P 500')

    current = close.iloc[-1]
    peak = close.max()
    peak_date = close.idxmax()

    # Calculate returns
    ytd_return = ((current / close.loc[f'{datetime.now().year}-01-01':].iloc[0]) - 1) * 100 if len(close.loc[f'{datetime.now().year}-01-01':]) > 0 else 0

    ax.scatter(close.index[-1], current, s=250, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=2.5, zorder=5)
    ax.annotate(f'{current:,.0f}\nYTD: {ytd_return:+.1f}%',
               xy=(close.index[-1], current), xytext=(-80, -40),
               textcoords='offset points', fontsize=10, fontweight='bold',
               color=LHM_COLORS['hot'])

    add_recession_shading(ax, '2000-01-01')

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('S&P 500 Index', fontweight='bold')
    ax.set_title('S&P 500: Real Yahoo Finance Data',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards
    ax.legend(loc='upper left', framealpha=0.95)

    textstr = f'Current: {current:,.0f}\nATH: {peak:,.0f} ({peak_date.strftime("%b %Y")})\nYTD Return: {ytd_return:+.1f}%'
    props = dict(boxstyle='round', facecolor='white', edgecolor=LHM_COLORS['ocean'], linewidth=2, alpha=0.95)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=props, family='monospace')

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


# ============================================================================
# CHART 11: VIX - REAL YAHOO DATA
# ============================================================================

def chart_11_labor_fragility_index():
    """VIX Index - REAL Yahoo data"""
    fetcher = get_fetcher()

    vix = fetcher.get_yahoo_data('^VIX', '2000-01-01')

    if isinstance(vix.columns, pd.MultiIndex):
        close = vix['Close']['^VIX'] if '^VIX' in vix['Close'].columns else vix['Close'].iloc[:, 0]
    else:
        close = vix['Close']
    close = close.dropna()

    fig, ax = plt.subplots(figsize=(14, 8))

    # Color code by level
    ax.fill_between(close.index, 0, close.values, alpha=0.3, color=LHM_COLORS['ocean'])
    ax.plot(close.index, close.values, linewidth=1.5, color=LHM_COLORS['ocean'], label='VIX')

    # Threshold lines
    ax.axhline(20, color=LHM_COLORS['dusk'], linestyle='--', linewidth=1.5, alpha=0.7, label='Elevated (20)')
    ax.axhline(30, color=LHM_COLORS['down_red'], linestyle='--', linewidth=1.5, alpha=0.7, label='Fear (30)')

    current = close.iloc[-1]
    mean_vix = close.mean()
    peak = close.max()
    peak_date = close.idxmax()

    ax.scatter(close.index[-1], current, s=250, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=2.5, zorder=5)
    ax.annotate(f'Current: {current:.1f}',
               xy=(close.index[-1], current), xytext=(-100, 30),
               textcoords='offset points', fontsize=10, fontweight='bold',
               color=LHM_COLORS['hot'],
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=LHM_COLORS['hot'], alpha=0.95))

    add_recession_shading(ax, '2000-01-01')

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('VIX Index', fontweight='bold')
    ax.set_title('VIX (Volatility Index): Real Yahoo Finance Data',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards
    ax.legend(loc='upper right', framealpha=0.95)

    textstr = f'Current: {current:.1f}\nMean: {mean_vix:.1f}\nPeak: {peak:.1f} ({peak_date.strftime("%b %Y")})'
    props = dict(boxstyle='round', facecolor='white', edgecolor=LHM_COLORS['ocean'], linewidth=2, alpha=0.95)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=props, family='monospace')

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


# ============================================================================
# CHART 12: CRE DELINQUENCIES - REAL FRED DATA
# ============================================================================

def chart_12_quits_rate():
    """CRE Delinquency Rate - REAL FRED data"""
    fetcher = get_fetcher()

    # REAL DATA
    cre_delinq = fetcher.get_fred_series('DRCRELEXFACBS', '2000-01-01')

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.fill_between(cre_delinq.index, 0, cre_delinq.values, alpha=0.3, color=LHM_COLORS['down_red'])
    ax.plot(cre_delinq.index, cre_delinq.values, linewidth=2.5, color=LHM_COLORS['down_red'], label='CRE Delinquency Rate')

    current = cre_delinq.iloc[-1]
    mean_rate = cre_delinq.mean()
    peak = cre_delinq.max()
    peak_date = cre_delinq.idxmax()

    ax.axhline(mean_rate, color=LHM_COLORS['silvs'], linestyle='--',
              linewidth=2, alpha=0.7, label=f'Mean: {mean_rate:.1f}%')

    ax.scatter(cre_delinq.index[-1], current, s=250, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=2.5, zorder=5)
    ax.annotate(f'Current: {current:.2f}%',
               xy=(cre_delinq.index[-1], current), xytext=(-100, 30),
               textcoords='offset points', fontsize=10, fontweight='bold',
               color=LHM_COLORS['hot'],
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=LHM_COLORS['hot'], alpha=0.95))

    add_recession_shading(ax, '2000-01-01')

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('Delinquency Rate (%)', fontweight='bold')
    ax.set_title('CRE Delinquency Rate: Real FRED Data (DRCRELEXFACBS)',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards
    ax.legend(loc='upper right', framealpha=0.95)

    textstr = f'Current: {current:.2f}%\nMean: {mean_rate:.1f}%\nPeak: {peak:.1f}% ({peak_date.strftime("%b %Y")})'
    props = dict(boxstyle='round', facecolor='white', edgecolor=LHM_COLORS['ocean'], linewidth=2, alpha=0.95)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=props, family='monospace')

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


# ============================================================================
# REMAINING CHARTS (13-24) - WILL USE REAL DATA WHERE AVAILABLE
# ============================================================================

def chart_13_consumer_bifurcation():
    """Consumer Credit Delinquencies - REAL FRED data"""
    fetcher = get_fetcher()

    # Consumer credit delinquency rate
    cc_delinq = fetcher.get_fred_series('DRCCLACBS', '2000-01-01')  # Credit card delinquency

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.fill_between(cc_delinq.index, 0, cc_delinq.values, alpha=0.3, color=LHM_COLORS['dusk'])
    ax.plot(cc_delinq.index, cc_delinq.values, linewidth=2.5, color=LHM_COLORS['dusk'], label='Credit Card Delinquency')

    current = cc_delinq.iloc[-1]
    mean_rate = cc_delinq.mean()
    peak = cc_delinq.max()
    peak_date = cc_delinq.idxmax()

    ax.axhline(mean_rate, color=LHM_COLORS['silvs'], linestyle='--', linewidth=2, alpha=0.7, label=f'Mean: {mean_rate:.1f}%')

    ax.scatter(cc_delinq.index[-1], current, s=250, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=2.5, zorder=5)
    ax.annotate(f'Current: {current:.2f}%',
               xy=(cc_delinq.index[-1], current), xytext=(20, 20),
               textcoords='offset points', fontsize=10, fontweight='bold', color=LHM_COLORS['hot'])

    add_recession_shading(ax, '2000-01-01')

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('Delinquency Rate (%)', fontweight='bold')
    ax.set_title('Credit Card Delinquency: Real FRED Data (DRCCLACBS)',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards
    ax.legend(loc='upper right', framealpha=0.95)

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


def chart_14_hy_spread_history():
    """IG Spreads - REAL FRED data"""
    fetcher = get_fetcher()

    ig_oas = fetcher.get_fred_series('BAMLC0A0CM', '2000-01-01')

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.fill_between(ig_oas.index, 0, ig_oas.values, alpha=0.3, color=LHM_COLORS['ocean'])
    ax.plot(ig_oas.index, ig_oas.values, linewidth=2, color=LHM_COLORS['ocean'], label='IG OAS')

    current = ig_oas.iloc[-1]
    mean_oas = ig_oas.mean()
    percentile = (ig_oas < current).mean() * 100

    ax.axhline(mean_oas, color=LHM_COLORS['silvs'], linestyle='--', linewidth=2, alpha=0.7, label=f'Mean: {mean_oas:.0f} bps')

    ax.scatter(ig_oas.index[-1], current, s=300, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=3, zorder=5)
    ax.annotate(f'Current: {current:.0f} bps\n{percentile:.0f}th percentile',
               xy=(ig_oas.index[-1], current), xytext=(-100, 50),
               textcoords='offset points', fontsize=10, fontweight='bold', color=LHM_COLORS['hot'],
               arrowprops=dict(arrowstyle='->', color=LHM_COLORS['hot'], lw=2))

    add_recession_shading(ax, '2000-01-01')

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('Investment Grade OAS (basis points)', fontweight='bold')
    ax.set_title('Investment Grade Spreads: Real FRED Data (BAMLC0A0CM)',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards
    ax.legend(loc='upper right', framealpha=0.95)

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


def chart_15_credit_labor_gap():
    """HY vs IG Spread Differential - REAL FRED data"""
    fetcher = get_fetcher()

    hy = fetcher.get_fred_series('BAMLH0A0HYM2', '2000-01-01')
    ig = fetcher.get_fred_series('BAMLC0A0CM', '2000-01-01')

    combined = pd.DataFrame({'HY': hy, 'IG': ig}).dropna()
    diff = combined['HY'] - combined['IG']

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.fill_between(diff.index, 0, diff.values, alpha=0.3, color=LHM_COLORS['dusk'])
    ax.plot(diff.index, diff.values, linewidth=2, color=LHM_COLORS['dusk'], label='HY - IG Spread')

    current = diff.iloc[-1]
    mean_diff = diff.mean()

    ax.axhline(mean_diff, color=LHM_COLORS['silvs'], linestyle='--', linewidth=2, alpha=0.7, label=f'Mean: {mean_diff:.0f} bps')

    ax.scatter(diff.index[-1], current, s=250, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=2.5, zorder=5)
    ax.annotate(f'Current: {current:.0f} bps',
               xy=(diff.index[-1], current), xytext=(20, 20),
               textcoords='offset points', fontsize=10, fontweight='bold', color=LHM_COLORS['hot'])

    add_recession_shading(ax, '2000-01-01')

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('HY - IG Spread (basis points)', fontweight='bold')
    ax.set_title('Credit Quality Differential: Real FRED Data',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards
    ax.legend(loc='upper right', framealpha=0.95)

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


def chart_16_dealer_balance_sheet():
    """Hires Rate - REAL FRED data"""
    fetcher = get_fetcher()

    hires = fetcher.get_fred_series('JTSHIR', '2001-01-01')

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.fill_between(hires.index, 0, hires.values, alpha=0.3, color=LHM_COLORS['ocean'])
    ax.plot(hires.index, hires.values, linewidth=2.5, color=LHM_COLORS['ocean'], label='Hires Rate')

    current = hires.iloc[-1]
    mean_rate = hires.mean()
    pre_covid = hires.loc['2015-01-01':'2019-12-31'].mean()

    ax.axhline(pre_covid, color=LHM_COLORS['silvs'], linestyle='--', linewidth=2, alpha=0.7, label=f'Pre-COVID avg: {pre_covid:.1f}%')

    ax.scatter(hires.index[-1], current, s=250, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=2.5, zorder=5)
    ax.annotate(f'Current: {current:.1f}%',
               xy=(hires.index[-1], current), xytext=(20, 20),
               textcoords='offset points', fontsize=10, fontweight='bold', color=LHM_COLORS['hot'])

    add_recession_shading(ax, '2001-01-01')

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('Hires Rate (% of Employment)', fontweight='bold')
    ax.set_title('JOLTS Hires Rate: Real FRED Data (JTSHIR)',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards
    ax.legend(loc='upper right', framealpha=0.95)

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


def chart_17_auction_tails():
    """Job Openings - REAL FRED data"""
    fetcher = get_fetcher()

    openings = fetcher.get_fred_series('JTSJOL', '2001-01-01')
    openings_millions = openings / 1000

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.fill_between(openings_millions.index, 0, openings_millions.values, alpha=0.3, color=LHM_COLORS['ocean'])
    ax.plot(openings_millions.index, openings_millions.values, linewidth=2.5, color=LHM_COLORS['ocean'], label='Job Openings')

    current = openings_millions.iloc[-1]
    peak = openings_millions.max()
    peak_date = openings_millions.idxmax()

    ax.scatter(openings_millions.index[-1], current, s=250, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=2.5, zorder=5)
    ax.annotate(f'Current: {current:.1f}M',
               xy=(openings_millions.index[-1], current), xytext=(20, 20),
               textcoords='offset points', fontsize=10, fontweight='bold', color=LHM_COLORS['hot'])

    add_recession_shading(ax, '2001-01-01')

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('Job Openings (Millions)', fontweight='bold')
    ax.set_title('JOLTS Job Openings: Real FRED Data (JTSJOL)',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards
    ax.legend(loc='upper left', framealpha=0.95)

    textstr = f'Current: {current:.1f}M\nPeak: {peak:.1f}M ({peak_date.strftime("%b %Y")})'
    props = dict(boxstyle='round', facecolor='white', edgecolor=LHM_COLORS['ocean'], linewidth=2, alpha=0.95)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=props, family='monospace')

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


def chart_18_cre_delinquencies():
    """PCE Inflation - REAL FRED data"""
    fetcher = get_fetcher()

    pce = fetcher.get_fred_series('PCEPI', '2000-01-01')
    pce_yoy = pce.pct_change(12) * 100
    pce_yoy = pce_yoy.dropna()

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.fill_between(pce_yoy.index, 0, pce_yoy.values, alpha=0.3, color=LHM_COLORS['dusk'])
    ax.plot(pce_yoy.index, pce_yoy.values, linewidth=2, color=LHM_COLORS['dusk'], label='PCE YoY')

    ax.axhline(2, color=LHM_COLORS['up_green'], linestyle='--', linewidth=2, alpha=0.7, label='2% Target')

    current = pce_yoy.iloc[-1]
    ax.scatter(pce_yoy.index[-1], current, s=250, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=2.5, zorder=5)
    ax.annotate(f'Current: {current:.1f}%',
               xy=(pce_yoy.index[-1], current), xytext=(20, 20),
               textcoords='offset points', fontsize=10, fontweight='bold', color=LHM_COLORS['hot'])

    add_recession_shading(ax, '2000-01-01')

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('PCE Inflation YoY (%)', fontweight='bold')
    ax.set_title('PCE Inflation: Real FRED Data (PCEPI)',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards
    ax.legend(loc='upper right', framealpha=0.95)

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


def chart_19_mag7_concentration():
    """Core PCE Inflation - REAL FRED data"""
    fetcher = get_fetcher()

    core_pce = fetcher.get_fred_series('PCEPILFE', '2000-01-01')
    core_yoy = core_pce.pct_change(12) * 100
    core_yoy = core_yoy.dropna()

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.fill_between(core_yoy.index, 0, core_yoy.values, alpha=0.3, color=LHM_COLORS['ocean'])
    ax.plot(core_yoy.index, core_yoy.values, linewidth=2, color=LHM_COLORS['ocean'], label='Core PCE YoY')

    ax.axhline(2, color=LHM_COLORS['up_green'], linestyle='--', linewidth=2, alpha=0.7, label='2% Target')

    current = core_yoy.iloc[-1]
    ax.scatter(core_yoy.index[-1], current, s=250, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=2.5, zorder=5)
    ax.annotate(f'Current: {current:.1f}%',
               xy=(core_yoy.index[-1], current), xytext=(20, 20),
               textcoords='offset points', fontsize=10, fontweight='bold', color=LHM_COLORS['hot'])

    add_recession_shading(ax, '2000-01-01')

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('Core PCE Inflation YoY (%)', fontweight='bold')
    ax.set_title('Core PCE Inflation: Real FRED Data (PCEPILFE)',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards
    ax.legend(loc='upper right', framealpha=0.95)

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


def chart_20_equity_momentum_divergence():
    """Fed Funds Rate - REAL FRED data"""
    fetcher = get_fetcher()

    ffr = fetcher.get_fred_series('FEDFUNDS', '2000-01-01')

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.fill_between(ffr.index, 0, ffr.values, alpha=0.3, color=LHM_COLORS['ocean'])
    ax.plot(ffr.index, ffr.values, linewidth=2.5, color=LHM_COLORS['ocean'], label='Fed Funds Rate')

    current = ffr.iloc[-1]
    ax.scatter(ffr.index[-1], current, s=250, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=2.5, zorder=5)
    ax.annotate(f'Current: {current:.2f}%',
               xy=(ffr.index[-1], current), xytext=(20, 20),
               textcoords='offset points', fontsize=10, fontweight='bold', color=LHM_COLORS['hot'])

    add_recession_shading(ax, '2000-01-01')

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('Fed Funds Rate (%)', fontweight='bold')
    ax.set_title('Federal Funds Rate: Real FRED Data (FEDFUNDS)',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards
    ax.legend(loc='upper right', framealpha=0.95)

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


def chart_21_yield_curve():
    """Real GDP Growth - REAL FRED data"""
    fetcher = get_fetcher()

    gdp = fetcher.get_fred_series('A191RL1Q225SBEA', '2000-01-01')  # Real GDP growth

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.bar(gdp.index, gdp.values, width=60, color=[LHM_COLORS['up_green'] if v >= 0 else LHM_COLORS['down_red'] for v in gdp.values], alpha=0.7)
    ax.axhline(0, color='black', linewidth=1.5)

    current = gdp.iloc[-1]
    mean_growth = gdp.mean()

    ax.axhline(mean_growth, color=LHM_COLORS['silvs'], linestyle='--', linewidth=2, alpha=0.7, label=f'Mean: {mean_growth:.1f}%')

    ax.scatter(gdp.index[-1], current, s=250, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=2.5, zorder=5)

    add_recession_shading(ax, '2000-01-01')

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('Real GDP Growth (%)', fontweight='bold')
    ax.set_title('Real GDP Growth (QoQ Annualized): Real FRED Data',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards
    ax.legend(loc='lower right', framealpha=0.95)

    textstr = f'Latest: {current:.1f}%\nMean: {mean_growth:.1f}%'
    props = dict(boxstyle='round', facecolor='white', edgecolor=LHM_COLORS['ocean'], linewidth=2, alpha=0.95)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=props, family='monospace')

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


def chart_22_cross_asset_correlation():
    """Industrial Production - REAL FRED data"""
    fetcher = get_fetcher()

    indpro = fetcher.get_fred_series('INDPRO', '2000-01-01')
    indpro_yoy = indpro.pct_change(12) * 100
    indpro_yoy = indpro_yoy.dropna()

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.fill_between(indpro_yoy.index, 0, indpro_yoy.values,
                   where=indpro_yoy.values >= 0, alpha=0.3, color=LHM_COLORS['up_green'])
    ax.fill_between(indpro_yoy.index, 0, indpro_yoy.values,
                   where=indpro_yoy.values < 0, alpha=0.3, color=LHM_COLORS['down_red'])
    ax.plot(indpro_yoy.index, indpro_yoy.values, linewidth=2, color=LHM_COLORS['ocean'])
    ax.axhline(0, color='black', linewidth=1.5)

    current = indpro_yoy.iloc[-1]
    ax.scatter(indpro_yoy.index[-1], current, s=250, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=2.5, zorder=5)
    ax.annotate(f'Current: {current:.1f}%',
               xy=(indpro_yoy.index[-1], current), xytext=(20, 20),
               textcoords='offset points', fontsize=10, fontweight='bold', color=LHM_COLORS['hot'])

    add_recession_shading(ax, '2000-01-01')

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('Industrial Production YoY (%)', fontweight='bold')
    ax.set_title('Industrial Production: Real FRED Data (INDPRO)',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


def chart_23_positioning_matrix():
    """Retail Sales - REAL FRED data"""
    fetcher = get_fetcher()

    retail = fetcher.get_fred_series('RSXFS', '2000-01-01')  # Retail sales ex food services
    retail_yoy = retail.pct_change(12) * 100
    retail_yoy = retail_yoy.dropna()

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.fill_between(retail_yoy.index, 0, retail_yoy.values, alpha=0.3, color=LHM_COLORS['ocean'])
    ax.plot(retail_yoy.index, retail_yoy.values, linewidth=2, color=LHM_COLORS['ocean'], label='Retail Sales YoY')
    ax.axhline(0, color='black', linewidth=1.5)

    current = retail_yoy.iloc[-1]
    mean_growth = retail_yoy.mean()

    ax.axhline(mean_growth, color=LHM_COLORS['silvs'], linestyle='--', linewidth=2, alpha=0.7, label=f'Mean: {mean_growth:.1f}%')

    ax.scatter(retail_yoy.index[-1], current, s=250, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=2.5, zorder=5)
    ax.annotate(f'Current: {current:.1f}%',
               xy=(retail_yoy.index[-1], current), xytext=(20, 20),
               textcoords='offset points', fontsize=10, fontweight='bold', color=LHM_COLORS['hot'])

    add_recession_shading(ax, '2000-01-01')

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('Retail Sales YoY (%)', fontweight='bold')
    ax.set_title('Retail Sales ex Food Services: Real FRED Data (RSXFS)',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards
    ax.legend(loc='upper right', framealpha=0.95)

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


def chart_24_risk_calendar():
    """Housing Starts - REAL FRED data"""
    fetcher = get_fetcher()

    starts = fetcher.get_fred_series('HOUST', '2000-01-01')

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.fill_between(starts.index, 0, starts.values, alpha=0.3, color=LHM_COLORS['ocean'])
    ax.plot(starts.index, starts.values, linewidth=2.5, color=LHM_COLORS['ocean'], label='Housing Starts')

    current = starts.iloc[-1]
    mean_starts = starts.mean()
    peak = starts.max()
    peak_date = starts.idxmax()

    ax.axhline(mean_starts, color=LHM_COLORS['silvs'], linestyle='--', linewidth=2, alpha=0.7, label=f'Mean: {mean_starts:.0f}K')

    ax.scatter(starts.index[-1], current, s=250, color=LHM_COLORS['hot'],
              edgecolors='white', linewidth=2.5, zorder=5)
    ax.annotate(f'Current: {current:.0f}K',
               xy=(starts.index[-1], current), xytext=(20, 20),
               textcoords='offset points', fontsize=10, fontweight='bold', color=LHM_COLORS['hot'])

    add_recession_shading(ax, '2000-01-01')

    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('Housing Starts (Thousands, SAAR)', fontweight='bold')
    ax.set_title('Housing Starts: Real FRED Data (HOUST)',
                 fontsize=14, fontweight='bold', pad=20)
    apply_lhm_style(ax)  # No gridlines, clean spines per LHM standards
    ax.legend(loc='upper right', framealpha=0.95)

    textstr = f'Current: {current:.0f}K\nMean: {mean_starts:.0f}K\nPeak: {peak:.0f}K ({peak_date.strftime("%b %Y")})'
    props = dict(boxstyle='round', facecolor='white', edgecolor=LHM_COLORS['ocean'], linewidth=2, alpha=0.95)
    ax.text(0.65, 0.95, textstr, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=props, family='monospace')

    add_lighthouse_branding(fig)
    plt.tight_layout()
    return fig


# ============================================================================
# GENERATION
# ============================================================================

def generate_all_charts(output_dir: str = 'output'):
    """Generate all 24 charts using REAL DATA"""
    import os
    os.makedirs(output_dir, exist_ok=True)

    charts = [
        ('chart_01_rrp_drawdown', chart_01_rrp_drawdown),
        ('chart_02_reserves_gdp', chart_02_liquidity_cushion_index),
        ('chart_03_sofr_effr', chart_03_sofr_effr_spread),
        ('chart_04_federal_debt', chart_04_reserves_vs_gdp),
        ('chart_05_interest_expense', chart_05_srf_usage),
        ('chart_06_yield_curve', chart_06_debt_trajectory),
        ('chart_07_hy_spreads', chart_07_interest_expense),
        ('chart_08_quits_rate', chart_08_term_premium),
        ('chart_09_unemployment', chart_09_foreign_holdings),
        ('chart_10_spx', chart_10_maturity_wall),
        ('chart_11_vix', chart_11_labor_fragility_index),
        ('chart_12_cre_delinquency', chart_12_quits_rate),
        ('chart_13_cc_delinquency', chart_13_consumer_bifurcation),
        ('chart_14_ig_spreads', chart_14_hy_spread_history),
        ('chart_15_hy_ig_diff', chart_15_credit_labor_gap),
        ('chart_16_hires_rate', chart_16_dealer_balance_sheet),
        ('chart_17_job_openings', chart_17_auction_tails),
        ('chart_18_pce_inflation', chart_18_cre_delinquencies),
        ('chart_19_core_pce', chart_19_mag7_concentration),
        ('chart_20_fed_funds', chart_20_equity_momentum_divergence),
        ('chart_21_gdp_growth', chart_21_yield_curve),
        ('chart_22_industrial_prod', chart_22_cross_asset_correlation),
        ('chart_23_retail_sales', chart_23_positioning_matrix),
        ('chart_24_housing_starts', chart_24_risk_calendar),
    ]

    print("Generating Horizon charts with REAL DATA...")
    print("=" * 60)

    success = 0
    for name, func in charts:
        try:
            print(f"Generating {name}...")
            fig = func()
            filepath = f"{output_dir}/{name}.png"
            fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
            plt.close(fig)
            print(f"  ✓ Saved to {filepath}")
            success += 1
        except Exception as e:
            print(f"  ✗ Error: {e}")

    print("=" * 60)
    print(f"Complete! {success}/{len(charts)} charts generated.")
    print(f"Charts saved to: {output_dir}")


if __name__ == "__main__":
    generate_all_charts()
