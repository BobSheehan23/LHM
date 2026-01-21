"""
LIGHTHOUSE MACRO - Chart Generation with REAL DATA ONLY
THE HORIZON | JANUARY 2026

NO SYNTHETIC DATA - All charts use actual API data from:
- NY Fed Markets API
- Treasury Fiscal Data API
- FRED API
- BLS API
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import warnings
import os
import sys

warnings.filterwarnings('ignore')

# Import real data fetcher
from real_data_fetcher import RealDataFetcher

# Import Lighthouse styling
from lighthouse_chart_style import (
    LIGHTHOUSE_COLORS,
    apply_lighthouse_style, apply_lighthouse_style_fig,
    add_threshold_line, add_callout_box, add_zone_shading,
    create_figure, create_dual_panel, create_multi_panel,
    add_last_value_label, add_series_with_label, create_tradingview_dual_axis,
)

# Configuration
OUTPUT_DIR = '/Users/bob/Desktop/HORIZON_FINAL./charts'
TARGET_DATE = '2026-01-14'
DPI = 150

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize data fetcher
data = RealDataFetcher()


def add_source(ax, source_text):
    """Add source attribution outside chart area"""
    ax.text(0.0, -0.12, f'Source: Lighthouse Macro, {source_text}',
            transform=ax.transAxes, fontsize=7, color='gray',
            ha='left', va='top')


def add_source_fig(fig, source_text):
    """Add source attribution to figure"""
    fig.text(0.02, 0.01, f'Source: Lighthouse Macro, {source_text}',
             fontsize=7, color='gray', ha='left', va='bottom')


# =============================================================================
# CHART 1: SOFR-EFFR Spread (NY Fed + FRED)
# =============================================================================

def chart_sofr_effr_spread():
    """SOFR-EFFR Spread - Funding Market Early Warning"""
    print("Generating: SOFR-EFFR Spread...")

    # Get real data
    spread_data = data.get_sofr_effr_spread()

    if len(spread_data) == 0:
        print("    ERROR: No data available")
        return None, None

    fig, ax = create_figure(figsize=(14, 9))

    dates = spread_data.index

    # Calculate MA
    spread_data['ma20'] = spread_data['spread'].rolling(20).mean()

    # Daily spread - using new series function
    add_series_with_label(ax, dates, spread_data['spread'],
                          label='Daily Spread',
                          color=LIGHTHOUSE_COLORS['ocean_blue'],
                          linewidth=0.5, show_last_value=False)

    # 20-day MA with last value on axis
    add_series_with_label(ax, dates, spread_data['ma20'],
                          label='20-Day MA',
                          color=LIGHTHOUSE_COLORS['hot_magenta'],
                          linewidth=2.5, show_last_value=True,
                          value_format='{:.1f}', value_side='right')

    # Thresholds with labels on axis
    ax.axhline(y=10, color=LIGHTHOUSE_COLORS['dusk_orange'], linestyle='--', linewidth=2)
    ax.axhline(y=20, color=LIGHTHOUSE_COLORS['pure_red'], linestyle='--', linewidth=2)
    ax.axhline(y=0, color='black', linewidth=1)

    # Threshold labels on left side (axis style)
    add_last_value_label(ax, 10, LIGHTHOUSE_COLORS['dusk_orange'],
                         label_format='10 bps', side='left', fontsize=8)
    add_last_value_label(ax, 20, LIGHTHOUSE_COLORS['pure_red'],
                         label_format='20 bps', side='left', fontsize=8)

    # Callout - bottom left
    add_callout_box(ax,
                    "INTERPRETATION:\n"
                    "- Negative: Secured cheaper (ample)\n"
                    "- 0-10 bps: Normal corridor\n"
                    "- >10 bps: Warning zone\n"
                    "- >20 bps: Stress",
                    (0.02, 0.35), fontsize=8)

    ax.set_ylabel('Spread (bps)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)
    ax.legend(loc='upper right', framealpha=0.95)
    ax.set_ylim(-15, 35)

    apply_lighthouse_style(ax, 'SOFR-EFFR Spread: Funding Market Early Warning')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator())

    add_source(ax, 'NY Fed, FRED')

    return fig, 'S2_16_SOFR_EFFR_Spread.png'


# =============================================================================
# CHART 2: RRP Usage (NY Fed)
# =============================================================================

def chart_rrp_usage():
    """ON RRP Usage - Liquidity Buffer Depletion"""
    print("Generating: RRP Usage...")

    rrp = data.get_rrp_usage()

    if len(rrp) == 0:
        print("    ERROR: No RRP data")
        return None, None

    fig, ax = create_figure(figsize=(14, 8))

    # Use new series function with last value on axis
    add_series_with_label(ax, rrp.index, rrp['totalAmtAccepted'],
                          label='ON RRP Usage',
                          color=LIGHTHOUSE_COLORS['ocean_blue'],
                          linewidth=2, fill=True, fill_alpha=0.4,
                          show_last_value=True,
                          value_format='${:.1f}B', value_side='right')

    # Callout - left side
    current = rrp['totalAmtAccepted'].iloc[-1]
    add_callout_box(ax,
                    "RRP DEPLETION:\n"
                    f"Peak: ~$2.5T (Dec 2022)\n"
                    f"Current: ${current:.1f}B\n"
                    "Buffer exhausted",
                    (0.02, 0.95), fontsize=8)

    ax.set_ylabel('RRP Usage ($ Billions)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)
    ax.set_ylim(bottom=0)
    ax.legend(loc='upper right', framealpha=0.95)

    apply_lighthouse_style(ax, 'Reverse Repo (RRP): The Liquidity Buffer Is Gone')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'NY Fed')

    return fig, 'S2_10_RRP_Usage.png'


# =============================================================================
# CHART 3: Yield Curve Shape (FRED)
# =============================================================================

def chart_yield_curve_shape():
    """Treasury Yield Curve Shape Analysis"""
    print("Generating: Yield Curve Shape...")

    yields_dict = data.get_yield_curve()

    fig, ax = create_figure(figsize=(12, 7))

    tenors = ['3M', '6M', '1Y', '2Y', '3Y', '5Y', '7Y', '10Y', '20Y', '30Y']
    tenor_positions = [0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30]

    # Get latest values
    current = []
    for t in tenors:
        if t in yields_dict and len(yields_dict[t]) > 0:
            current.append(yields_dict[t].iloc[-1])
        else:
            current.append(np.nan)

    ax.plot(tenor_positions, current, 'o-',
            color=LIGHTHOUSE_COLORS['ocean_blue'],
            linewidth=2.5, markersize=8, label='Current')

    # Data labels
    for i, (x, y) in enumerate(zip(tenor_positions, current)):
        if not np.isnan(y):
            ax.annotate(f'{y:.2f}%', (x, y), textcoords='offset points',
                        xytext=(0, 10), ha='center', fontsize=8,
                        color=LIGHTHOUSE_COLORS['ocean_blue'], fontweight='bold')

    # 10Y-2Y spread
    idx_2y = tenors.index('2Y')
    idx_10y = tenors.index('10Y')
    spread_10y2y = (current[idx_10y] - current[idx_2y]) * 100

    add_callout_box(ax,
                    f"10Y-2Y Spread: {spread_10y2y:.0f}bps\n"
                    f"Curve: {'STEEPENING' if spread_10y2y > 0 else 'INVERTED'}",
                    (0.02, 0.95), fontsize=10)

    ax.set_xlabel('Maturity (Years)', fontsize=10)
    ax.set_ylabel('Yield (%)', fontsize=10)
    ax.set_xscale('log')
    ax.set_xticks(tenor_positions)
    ax.set_xticklabels(tenors)
    ax.legend(loc='lower right')

    apply_lighthouse_style(ax, 'Treasury Yield Curve: Shape Analysis')
    add_source(ax, 'FRED (DGS series)')

    return fig, 'S1_16_Yield_Curve_Shape.png'


# =============================================================================
# CHART 4: Credit Spread Percentiles (FRED)
# =============================================================================

def chart_credit_spread_percentiles():
    """Credit Spread Percentile Gauges"""
    print("Generating: Credit Spread Percentiles...")

    spreads = data.get_credit_spreads()

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.patch.set_facecolor('white')

    spreads_config = [
        ('AAA Spread', 'AAA', 75, (0, 0)),
        ('IG Spread', 'IG', 147, (0, 1)),
        ('BBB Spread', 'BBB', 190, (1, 0)),
        ('HY Spread', 'HY', 522, (1, 1))
    ]

    for name, key, hist_mean, pos in spreads_config:
        ax = axes[pos[0], pos[1]]

        series = spreads.get(key, pd.Series())
        if len(series) == 0:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center', transform=ax.transAxes)
            continue

        current = series.iloc[-1] * 100  # Convert to bps

        # Use full history for percentile calculation
        hist_values = series.values * 100
        percentile = (hist_values < current).sum() / len(hist_values) * 100

        # Histogram of historical data
        n, bins, patches = ax.hist(hist_values, bins=40, alpha=0.7,
                                    edgecolor='white', linewidth=0.5)

        for i, patch in enumerate(patches):
            if bins[i] < current:
                patch.set_facecolor(LIGHTHOUSE_COLORS['teal_green'])
            else:
                patch.set_facecolor(LIGHTHOUSE_COLORS['pure_red'])
                patch.set_alpha(0.5)

        ax.axvline(x=current, color=LIGHTHOUSE_COLORS['hot_magenta'],
                   linewidth=2, label=f'Current: {current:.0f} bps')
        ax.axvline(x=hist_mean, color='black', linewidth=1, linestyle='--',
                   label=f'Mean: {hist_mean} bps')

        ax.set_title(f'{name}\nCurrent: {percentile:.0f}th Percentile',
                     fontsize=11, fontweight='bold')
        ax.set_xlabel('Spread (bps)')
        ax.legend(fontsize=8, loc='upper right')

        # 4 spines visible (institutional standard)
        for spine in ['top', 'right', 'left', 'bottom']:
            ax.spines[spine].set_visible(True)
            ax.spines[spine].set_linewidth(0.5)
            ax.spines[spine].set_color('#666666')

        # Add current value label on right axis
        add_last_value_label(ax, current, LIGHTHOUSE_COLORS['hot_magenta'],
                             label_format='{:.0f}', side='right', fontsize=8)

    fig.suptitle('CREDIT SPREAD PERCENTILE GAUGES\nWhere Are Spreads vs History?',
                 fontsize=14, fontweight='bold', y=0.98)

    add_source_fig(fig, 'FRED (ICE BofA indices)')
    plt.tight_layout(rect=[0, 0.03, 1, 0.94])

    return fig, 'S2_07_Credit_Spread_Percentiles.png'


# =============================================================================
# CHART 5: Repo Rate Dispersion (NY Fed)
# =============================================================================

def chart_repo_rate_dispersion():
    """Repo Rate Dispersion - SOFR Percentiles"""
    print("Generating: Repo Rate Dispersion...")

    dispersion = data.get_repo_dispersion()

    if len(dispersion) == 0:
        print("    ERROR: No dispersion data")
        return None, None

    fig, ax = create_figure(figsize=(14, 7))

    # Plot main rate
    if 'sofr' in dispersion.columns:
        ax.plot(dispersion.index, dispersion['sofr'],
                color=LIGHTHOUSE_COLORS['ocean_blue'],
                linewidth=2, label='SOFR')

    # Plot percentile range if available
    if 'sofr_percentile1' in dispersion.columns and 'sofr_percentile99' in dispersion.columns:
        ax.fill_between(dispersion.index,
                        dispersion['sofr_percentile1'],
                        dispersion['sofr_percentile99'],
                        color=LIGHTHOUSE_COLORS['dusk_orange'], alpha=0.2,
                        label='1st-99th Percentile')

    if 'sofr_percentile25' in dispersion.columns and 'sofr_percentile75' in dispersion.columns:
        ax.fill_between(dispersion.index,
                        dispersion['sofr_percentile25'],
                        dispersion['sofr_percentile75'],
                        color=LIGHTHOUSE_COLORS['ocean_blue'], alpha=0.3,
                        label='25th-75th Percentile')

    # Add TGCR/BGCR if available
    if 'tgcr' in dispersion.columns:
        ax.plot(dispersion.index, dispersion['tgcr'],
                color=LIGHTHOUSE_COLORS['teal_green'],
                linewidth=1.5, linestyle='--', label='TGCR')

    if 'bgcr' in dispersion.columns:
        ax.plot(dispersion.index, dispersion['bgcr'],
                color=LIGHTHOUSE_COLORS['neutral_gray'],
                linewidth=1.5, linestyle=':', label='BGCR')

    ax.set_ylabel('Rate (%)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)
    ax.legend(loc='upper left', fontsize=9)

    apply_lighthouse_style(ax, 'Repo Rate Dispersion: Market Fragmentation Signal')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    add_source(ax, 'NY Fed')

    return fig, 'S2_15_Repo_Dispersion.png'


# =============================================================================
# CHART 6: Bank Reserves vs GDP (FRED)
# =============================================================================

def chart_bank_reserves_gdp():
    """Bank Reserves as % of GDP"""
    print("Generating: Bank Reserves vs GDP...")

    reserves_data = data.get_reserves_and_rrp()
    reserves = reserves_data.get('reserves', pd.Series())

    if len(reserves) == 0:
        print("    ERROR: No reserves data")
        return None, None

    fig, ax = create_figure(figsize=(14, 8))

    # Convert to trillions
    reserves_t = reserves / 1e6

    # Use new series function with last value on axis
    add_series_with_label(ax, reserves_t.index, reserves_t.values,
                          label='Bank Reserves',
                          color=LIGHTHOUSE_COLORS['ocean_blue'],
                          linewidth=2, fill=True, fill_alpha=0.3,
                          show_last_value=True,
                          value_format='${:.2f}T', value_side='right')

    # LCLOR threshold with label on axis
    ax.axhline(y=2.8, color=LIGHTHOUSE_COLORS['pure_red'],
               linestyle='--', linewidth=2, alpha=0.8)
    add_last_value_label(ax, 2.8, LIGHTHOUSE_COLORS['pure_red'],
                         label_format='$2.8T LCLOR', side='left', fontsize=8)

    # Comfortable level
    ax.axhline(y=3.0, color=LIGHTHOUSE_COLORS['teal_green'],
               linestyle='--', linewidth=1.5, alpha=0.7)
    add_last_value_label(ax, 3.0, LIGHTHOUSE_COLORS['teal_green'],
                         label_format='$3.0T Comf.', side='left', fontsize=8)

    ax.set_ylabel('Bank Reserves ($ Trillions)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)
    ax.set_ylim(bottom=0)
    ax.legend(loc='upper right', framealpha=0.95)

    apply_lighthouse_style(ax, 'Bank Reserves at Fed: Distribution Matters More Than Level')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'FRED (WRESBAL)')

    return fig, 'S2_04_Bank_Reserves.png'


# =============================================================================
# CHART 7: Labor Fragility Index (BLS + FRED)
# =============================================================================

def chart_labor_fragility_index():
    """Labor Fragility Index - Quits, Hires, LT Unemployment"""
    print("Generating: Labor Fragility Index...")

    labor = data.get_labor_data()

    quits = labor.get('quits', pd.Series())
    hires = labor.get('hires', pd.Series())
    lt_unemp = labor.get('long_term_unemp', pd.Series())

    if len(quits) == 0:
        print("    ERROR: No labor data")
        return None, None

    fig, ax = create_figure(figsize=(14, 8))

    # Plot quits rate with last value on axis
    add_series_with_label(ax, quits.index, quits.values,
                          label='Quits Rate',
                          color=LIGHTHOUSE_COLORS['ocean_blue'],
                          linewidth=2.5, show_last_value=True,
                          value_format='{:.1f}%', value_side='right')

    # Plot hires rate with last value on axis
    if len(hires) > 0:
        add_series_with_label(ax, hires.index, hires.values,
                              label='Hires Rate',
                              color=LIGHTHOUSE_COLORS['teal_green'],
                              linewidth=2, linestyle='--',
                              show_last_value=True,
                              value_format='{:.1f}%', value_side='right')

    # Pre-recession threshold
    ax.axhline(y=2.0, color=LIGHTHOUSE_COLORS['pure_red'],
               linestyle='--', linewidth=1.5, alpha=0.7)
    add_last_value_label(ax, 2.0, LIGHTHOUSE_COLORS['pure_red'],
                         label_format='2.0% Thresh', side='left', fontsize=8)

    add_callout_box(ax,
                    "LFI COMPONENTS:\n"
                    "- Quits rate (confidence)\n"
                    "- Hires rate (dynamism)\n"
                    "- Long-term unemployment\n\n"
                    "Lower quits = less confidence\n"
                    "in job market",
                    (0.02, 0.35), fontsize=8)

    ax.set_ylabel('Rate (%)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)
    ax.legend(loc='upper right', framealpha=0.95)

    apply_lighthouse_style(ax, 'Labor Market: Quits Rate Shows Waning Confidence')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'BLS JOLTS')

    return fig, 'S2_36_Labor_Fragility_Index.png'


# =============================================================================
# CHART 8: Excess Savings / Savings Rate (FRED)
# =============================================================================

def chart_savings_rate():
    """Personal Savings Rate"""
    print("Generating: Personal Savings Rate...")

    consumer = data.get_consumer_data()
    savings = consumer.get('savings_rate', pd.Series())

    if len(savings) == 0:
        print("    ERROR: No savings data")
        return None, None

    fig, ax = create_figure(figsize=(14, 8))

    ax.fill_between(savings.index, 0, savings.values,
                    color=LIGHTHOUSE_COLORS['ocean_blue'], alpha=0.5)
    ax.plot(savings.index, savings.values,
            color=LIGHTHOUSE_COLORS['ocean_blue'], linewidth=2)

    # Historical average
    avg = savings.mean()
    ax.axhline(y=avg, color=LIGHTHOUSE_COLORS['neutral_gray'],
               linestyle='--', linewidth=1.5)
    ax.text(savings.index[0], avg + 0.5, f'Historical Avg: {avg:.1f}%',
            fontsize=8, color=LIGHTHOUSE_COLORS['neutral_gray'])

    # Current
    current = savings.iloc[-1]
    ax.annotate(f'Current: {current:.1f}%\n(vs {avg:.1f}% avg)',
                (savings.index[-1], current),
                textcoords='offset points', xytext=(-80, 20),
                fontsize=10, fontweight='bold',
                color=LIGHTHOUSE_COLORS['hot_magenta'],
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    ax.set_ylabel('Savings Rate (%)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)
    ax.set_ylim(bottom=0)
    ax.legend(['Personal Savings Rate'], loc='upper right')

    apply_lighthouse_style(ax, 'Personal Savings Rate: Buffer Depleted')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'FRED (PSAVERT)')

    return fig, 'S2_01_Savings_Rate.png'


# =============================================================================
# CHART 9: Credit Impulse / Consumer Credit (FRED)
# =============================================================================

def chart_consumer_credit():
    """Consumer Credit Growth"""
    print("Generating: Consumer Credit...")

    consumer = data.get_consumer_data()
    credit = consumer.get('consumer_credit', pd.Series())

    if len(credit) == 0:
        print("    ERROR: No credit data")
        return None, None

    # Calculate YoY growth
    credit_yoy = credit.pct_change(12) * 100

    fig, ax = create_figure(figsize=(14, 8))

    # Color based on positive/negative
    colors = [LIGHTHOUSE_COLORS['teal_green'] if v >= 0 else LIGHTHOUSE_COLORS['pure_red']
              for v in credit_yoy.values]

    ax.fill_between(credit_yoy.index, 0, credit_yoy.values,
                    where=credit_yoy.values >= 0,
                    color=LIGHTHOUSE_COLORS['teal_green'], alpha=0.5)
    ax.fill_between(credit_yoy.index, 0, credit_yoy.values,
                    where=credit_yoy.values < 0,
                    color=LIGHTHOUSE_COLORS['pure_red'], alpha=0.5)

    ax.axhline(y=0, color='black', linewidth=1)

    # Current
    current = credit_yoy.dropna().iloc[-1]
    ax.annotate(f'Current: {current:.1f}% YoY',
                (credit_yoy.index[-1], current),
                textcoords='offset points', xytext=(-80, 20),
                fontsize=10, fontweight='bold',
                color=LIGHTHOUSE_COLORS['hot_magenta'],
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    ax.set_ylabel('YoY Growth (%)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)

    apply_lighthouse_style(ax, 'Consumer Credit Growth: The Credit Impulse')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'FRED (TOTALSL)')

    return fig, 'S1_08_Credit_Impulse.png'


# =============================================================================
# CHART 10: CRE Delinquencies (FRED)
# =============================================================================

def chart_cre_delinquencies():
    """Commercial Real Estate Delinquencies"""
    print("Generating: CRE Delinquencies...")

    delinq = data.get_delinquency_data()
    cre = delinq.get('cre', pd.Series())

    if len(cre) == 0:
        print("    ERROR: No CRE data")
        return None, None

    fig, ax = create_figure(figsize=(14, 8))

    ax.plot(cre.index, cre.values, '-',
            color=LIGHTHOUSE_COLORS['pure_red'],
            linewidth=2.5, label='CRE Delinquency Rate')

    ax.fill_between(cre.index, 0, cre.values,
                    color=LIGHTHOUSE_COLORS['pure_red'], alpha=0.2)

    # 2008 crisis peak reference
    crisis_peak = cre.max()
    ax.axhline(y=crisis_peak, color='black', linestyle='--', linewidth=1.5)
    ax.text(cre.index[0], crisis_peak + 0.2, f'Historical Peak: {crisis_peak:.1f}%',
            fontsize=8, color='black')

    # Current
    current = cre.iloc[-1]
    ax.annotate(f'Current: {current:.1f}%',
                (cre.index[-1], current),
                textcoords='offset points', xytext=(-80, 10),
                fontsize=10, fontweight='bold',
                color=LIGHTHOUSE_COLORS['hot_magenta'],
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    ax.set_ylabel('Delinquency Rate (%)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)
    ax.set_ylim(bottom=0)
    ax.legend(loc='upper right')

    apply_lighthouse_style(ax, 'Commercial Real Estate Delinquencies')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'FRED (DRCLACBS)')

    return fig, 'S2_33_CRE_Delinquencies.png'


# =============================================================================
# CHART 11: Auto Delinquencies (FRED)
# =============================================================================

def chart_auto_delinquencies():
    """Auto Loan Delinquencies"""
    print("Generating: Auto Delinquencies...")

    delinq = data.get_delinquency_data()
    auto = delinq.get('auto', pd.Series())

    if len(auto) == 0:
        print("    ERROR: No auto data")
        return None, None

    fig, ax = create_figure(figsize=(14, 8))

    ax.plot(auto.index, auto.values, '-',
            color=LIGHTHOUSE_COLORS['ocean_blue'],
            linewidth=2.5, label='Auto Loan Delinquency Rate')

    ax.fill_between(auto.index, 0, auto.values,
                    color=LIGHTHOUSE_COLORS['ocean_blue'], alpha=0.3)

    # Current
    current = auto.iloc[-1]
    ax.annotate(f'Current: {current:.2f}%',
                (auto.index[-1], current),
                textcoords='offset points', xytext=(-80, 10),
                fontsize=10, fontweight='bold',
                color=LIGHTHOUSE_COLORS['hot_magenta'],
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    ax.set_ylabel('Delinquency Rate (%)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)
    ax.set_ylim(bottom=0)
    ax.legend(loc='upper right')

    apply_lighthouse_style(ax, 'Auto Loan Delinquencies: Consumer Stress Indicator')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'FRED (DRALACBS)')

    return fig, 'S2_23_Auto_Delinquencies.png'


# =============================================================================
# CHART 12: VIX (FRED)
# =============================================================================

def chart_vix():
    """VIX Volatility Index"""
    print("Generating: VIX...")

    vix = data.get_vix()

    if len(vix) == 0:
        print("    ERROR: No VIX data")
        return None, None

    # Last 3 years
    vix = vix[vix.index >= '2021-01-01']

    fig, ax = create_figure(figsize=(14, 7))

    # Use new series function
    add_series_with_label(ax, vix.index, vix.values,
                          label='VIX',
                          color=LIGHTHOUSE_COLORS['ocean_blue'],
                          linewidth=1.5, show_last_value=True,
                          value_format='{:.1f}', value_side='right')

    # Shade elevated periods
    ax.fill_between(vix.index, 0, vix.values,
                    where=vix.values > 25,
                    color=LIGHTHOUSE_COLORS['dusk_orange'], alpha=0.3)

    # Threshold lines with axis labels
    ax.axhline(y=20, color=LIGHTHOUSE_COLORS['teal_green'],
               linestyle='--', linewidth=1.5)
    add_last_value_label(ax, 20, LIGHTHOUSE_COLORS['teal_green'],
                         label_format='20 Calm', side='left', fontsize=8)

    ax.axhline(y=30, color=LIGHTHOUSE_COLORS['pure_red'],
               linestyle='--', linewidth=1.5)
    add_last_value_label(ax, 30, LIGHTHOUSE_COLORS['pure_red'],
                         label_format='30 Stress', side='left', fontsize=8)

    ax.set_ylabel('VIX', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)
    ax.set_ylim(bottom=0)
    ax.legend(loc='upper right', framealpha=0.95)

    apply_lighthouse_style(ax, 'VIX: Market Volatility Gauge')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'FRED (VIXCLS)')

    return fig, 'S1_15_VIX.png'


# =============================================================================
# CHART 13: Initial Claims (FRED)
# =============================================================================

def chart_initial_claims():
    """Initial Jobless Claims"""
    print("Generating: Initial Claims...")

    claims = data.get_claims()

    if len(claims) == 0:
        print("    ERROR: No claims data")
        return None, None

    # 4-week moving average
    claims_ma = claims.rolling(4).mean()

    # Last 5 years
    claims_ma = claims_ma[claims_ma.index >= '2019-01-01']

    fig, ax = create_figure(figsize=(14, 8))

    # Use new series function with last value on axis
    add_series_with_label(ax, claims_ma.index, claims_ma.values / 1000,
                          label='Initial Claims (4-Week Avg)',
                          color=LIGHTHOUSE_COLORS['ocean_blue'],
                          linewidth=2.5, show_last_value=True,
                          value_format='{:.0f}K', value_side='right')

    # Pre-COVID reference with axis label
    ax.axhline(y=220, color=LIGHTHOUSE_COLORS['teal_green'],
               linestyle='--', linewidth=1.5)
    add_last_value_label(ax, 220, LIGHTHOUSE_COLORS['teal_green'],
                         label_format='220K Avg', side='left', fontsize=8)

    # Warning threshold
    ax.axhline(y=300, color=LIGHTHOUSE_COLORS['dusk_orange'],
               linestyle='--', linewidth=1.5, alpha=0.7)
    add_last_value_label(ax, 300, LIGHTHOUSE_COLORS['dusk_orange'],
                         label_format='300K Warn', side='left', fontsize=8)

    ax.set_ylabel('Claims (Thousands)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)
    ax.legend(loc='upper right', framealpha=0.95)

    apply_lighthouse_style(ax, 'Initial Jobless Claims: Labor Market Health')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'FRED (ICSA)')

    return fig, 'S2_24_Initial_Claims.png'


# =============================================================================
# CHART 14: Federal Debt (FRED)
# =============================================================================

def chart_federal_debt():
    """Federal Debt Trajectory"""
    print("Generating: Federal Debt...")

    debt_data = data.get_debt_data()
    debt = debt_data.get('total', pd.Series())
    debt_gdp = debt_data.get('debt_gdp', pd.Series())

    if len(debt) == 0:
        print("    ERROR: No debt data")
        return None, None

    fig, ax1 = create_figure(figsize=(14, 8))

    # Debt in trillions
    debt_t = debt / 1e6

    ax1.bar(debt_t.index, debt_t.values,
            color=LIGHTHOUSE_COLORS['ocean_blue'], alpha=0.7, width=100)
    ax1.set_ylabel('Debt Outstanding ($ Trillions)', fontsize=10,
                   color=LIGHTHOUSE_COLORS['ocean_blue'])

    # Debt/GDP on second axis
    if len(debt_gdp) > 0:
        ax2 = ax1.twinx()
        ax2.plot(debt_gdp.index, debt_gdp.values, 'o-',
                 color=LIGHTHOUSE_COLORS['teal_green'],
                 linewidth=2, markersize=3, label='Debt/GDP %')
        ax2.set_ylabel('Debt to GDP (%)', fontsize=10,
                       color=LIGHTHOUSE_COLORS['teal_green'])

        # 100% threshold
        ax2.axhline(y=100, color=LIGHTHOUSE_COLORS['pure_red'],
                    linestyle='--', linewidth=1.5)

    # Current
    current_debt = debt_t.iloc[-1]
    ax1.annotate(f'Current: ${current_debt:.1f}T',
                 (debt_t.index[-1], current_debt),
                 textcoords='offset points', xytext=(-80, 10),
                 fontsize=10, fontweight='bold',
                 color=LIGHTHOUSE_COLORS['hot_magenta'],
                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    ax1.set_xlabel('Date', fontsize=10)

    apply_lighthouse_style(ax1, 'Federal Debt Trajectory')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax1, 'FRED (GFDEBTN, GFDEGDQ188S)')

    return fig, 'S2_20_Federal_Debt.png'


# =============================================================================
# CHART 15: GDP Real vs Nominal (FRED)
# =============================================================================

def chart_gdp():
    """Real vs Nominal GDP"""
    print("Generating: GDP...")

    gdp_data = data.get_gdp_data()
    nominal = gdp_data.get('nominal', pd.Series())
    real = gdp_data.get('real', pd.Series())

    if len(nominal) == 0 or len(real) == 0:
        print("    ERROR: No GDP data")
        return None, None

    # Calculate YoY growth
    nominal_yoy = nominal.pct_change(4) * 100  # Quarterly data
    real_yoy = real.pct_change(4) * 100

    # Last 25 years
    nominal_yoy = nominal_yoy[nominal_yoy.index >= '2000-01-01']
    real_yoy = real_yoy[real_yoy.index >= '2000-01-01']

    fig, ax = create_figure(figsize=(14, 8))

    ax.bar(nominal_yoy.index, nominal_yoy.values,
           color=LIGHTHOUSE_COLORS['dusk_orange'], alpha=0.7, width=60,
           label='Nominal GDP YoY')
    ax.plot(real_yoy.index, real_yoy.values, '-',
            color=LIGHTHOUSE_COLORS['ocean_blue'],
            linewidth=2.5, label='Real GDP YoY')

    ax.axhline(y=0, color='black', linewidth=1)

    ax.set_ylabel('YoY Growth (%)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)
    ax.legend(loc='upper right')

    apply_lighthouse_style(ax, 'Real vs Nominal GDP Growth')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'FRED (GDP, GDPC1)')

    return fig, 'S1_09_GDP.png'


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def generate_all_charts():
    """Generate all charts with REAL DATA ONLY"""

    print("=" * 60)
    print("LIGHTHOUSE MACRO - REAL DATA CHART GENERATION")
    print("NO SYNTHETIC DATA")
    print(f"Target Date: {TARGET_DATE}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60 + "\n")

    chart_functions = [
        chart_sofr_effr_spread,
        chart_rrp_usage,
        chart_yield_curve_shape,
        chart_credit_spread_percentiles,
        chart_repo_rate_dispersion,
        chart_bank_reserves_gdp,
        chart_labor_fragility_index,
        chart_savings_rate,
        chart_consumer_credit,
        chart_cre_delinquencies,
        chart_auto_delinquencies,
        chart_vix,
        chart_initial_claims,
        chart_federal_debt,
        chart_gdp,
    ]

    results = []

    for func in chart_functions:
        try:
            result = func()
            if result[0] is None:
                results.append((func.__name__, 'SKIPPED - No data'))
                continue

            fig, filename = result
            filepath = os.path.join(OUTPUT_DIR, filename)
            fig.savefig(filepath, dpi=DPI, bbox_inches='tight',
                        facecolor='white', edgecolor='none')
            plt.close(fig)
            results.append((filename, 'SUCCESS'))
            print(f"  OK: {filename}")
        except Exception as e:
            results.append((func.__name__, f'FAILED: {str(e)}'))
            print(f"  FAIL: {func.__name__} - {e}")

    # Summary
    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)
    success = sum(1 for _, status in results if status == 'SUCCESS')
    print(f"Generated: {success}/{len(results)} charts")
    print(f"Output: {OUTPUT_DIR}")

    if success < len(results):
        print("\nSkipped/Failed:")
        for name, status in results:
            if status != 'SUCCESS':
                print(f"  - {name}: {status}")

    print("=" * 60)

    return results


# =============================================================================
# CHART 16: Treasury Auction Tails (Treasury API)
# =============================================================================

def chart_treasury_auction_tails():
    """Treasury Auction Tails - Demand Signal"""
    print("Generating: Treasury Auction Tails...")

    auctions = data.get_auction_data()

    if len(auctions) == 0:
        print("    ERROR: No auction data")
        return None, None

    # Filter for relevant auctions and calculate tails
    # Tail = High Rate - When Issued Rate (or similar)
    if 'high_investment_rate' not in auctions.columns:
        print("    ERROR: Missing rate columns")
        return None, None

    auctions = auctions.dropna(subset=['high_investment_rate', 'auction_date'])
    auctions = auctions.sort_values('auction_date')

    fig, ax = create_figure(figsize=(14, 8))

    # Plot by security type if available
    if 'security_type' in auctions.columns:
        for sec_type in auctions['security_type'].unique()[:4]:  # Limit to 4 types
            mask = auctions['security_type'] == sec_type
            subset = auctions[mask]
            ax.scatter(subset['auction_date'], subset['high_investment_rate'],
                      alpha=0.6, s=30, label=sec_type)
    else:
        ax.scatter(auctions['auction_date'], auctions['high_investment_rate'],
                  color=LIGHTHOUSE_COLORS['ocean_blue'], alpha=0.6, s=30)

    ax.set_ylabel('High Investment Rate (%)', fontsize=10)
    ax.set_xlabel('Auction Date', fontsize=10)
    ax.legend(loc='upper left', fontsize=8)

    apply_lighthouse_style(ax, 'Treasury Auctions: Bid Coverage and Pricing')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    add_source(ax, 'Treasury Fiscal Data')

    return fig, 'S2_11_Auction_Tails.png'


# =============================================================================
# CHART 17: SOMA Holdings (NY Fed)
# =============================================================================

def chart_soma_holdings():
    """SOMA Holdings - QT Progress"""
    print("Generating: SOMA Holdings...")

    soma = data.nyfed.get_soma_summary()

    if len(soma) == 0:
        print("    ERROR: No SOMA data")
        return None, None

    fig, ax = create_figure(figsize=(14, 8))

    # Convert to trillions
    if 'total' in soma.columns:
        total_t = soma['total'] / 1e12

        ax.fill_between(soma.index, 0, total_t.values,
                        color=LIGHTHOUSE_COLORS['ocean_blue'], alpha=0.5)
        ax.plot(soma.index, total_t.values,
                color=LIGHTHOUSE_COLORS['ocean_blue'], linewidth=2,
                label='Total SOMA')

    # Add component breakdown if available
    if 'notesbonds' in soma.columns:
        notes_t = soma['notesbonds'] / 1e12
        ax.plot(soma.index, notes_t.values,
                color=LIGHTHOUSE_COLORS['teal_green'], linewidth=1.5,
                linestyle='--', label='Notes/Bonds')

    if 'mbs' in soma.columns:
        mbs_t = soma['mbs'] / 1e12
        ax.plot(soma.index, mbs_t.values,
                color=LIGHTHOUSE_COLORS['dusk_orange'], linewidth=1.5,
                linestyle='--', label='MBS')

    # Current annotation
    if 'total' in soma.columns:
        current = total_t.iloc[-1]
        ax.annotate(f'Current: ${current:.2f}T',
                    (soma.index[-1], current),
                    textcoords='offset points', xytext=(-80, 10),
                    fontsize=10, fontweight='bold',
                    color=LIGHTHOUSE_COLORS['hot_magenta'],
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    ax.set_ylabel('Holdings ($ Trillions)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)
    ax.set_ylim(bottom=0)
    ax.legend(loc='upper left')

    apply_lighthouse_style(ax, 'Fed SOMA Holdings: Quantitative Tightening')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'NY Fed SOMA')

    return fig, 'S2_12_SOMA_Holdings.png'


# =============================================================================
# CHART 18: Foreign Treasury Holdings (TIC/FRED)
# =============================================================================

def chart_foreign_holdings():
    """Foreign Treasury Holdings"""
    print("Generating: Foreign Treasury Holdings...")

    holdings_data = data.get_foreign_holdings()

    if isinstance(holdings_data, dict) and len(holdings_data) == 0:
        print("    ERROR: No foreign holdings data")
        return None, None

    fig, ax = create_figure(figsize=(14, 8))

    # Check if it's DataFrame (TIC) or dict (FRED fallback)
    if isinstance(holdings_data, dict):
        # FRED fallback data
        total = holdings_data.get('total_foreign', pd.Series())
        china = holdings_data.get('china')
        japan = holdings_data.get('japan')

        if len(total) > 0:
            # Convert to trillions
            total_t = total / 1e3

            ax.plot(total_t.index, total_t.values,
                    color=LIGHTHOUSE_COLORS['ocean_blue'],
                    linewidth=2.5, label='Total Foreign')

            if china is not None and len(china) > 0:
                china_t = china / 1e3
                ax.plot(china_t.index, china_t.values,
                        color=LIGHTHOUSE_COLORS['pure_red'],
                        linewidth=1.5, linestyle='--', label='China')

            if japan is not None and len(japan) > 0:
                japan_t = japan / 1e3
                ax.plot(japan_t.index, japan_t.values,
                        color=LIGHTHOUSE_COLORS['teal_green'],
                        linewidth=1.5, linestyle='--', label='Japan')

            current = total_t.iloc[-1]
            ax.annotate(f'Total: ${current:.2f}T',
                        (total_t.index[-1], current),
                        textcoords='offset points', xytext=(-80, 10),
                        fontsize=10, fontweight='bold',
                        color=LIGHTHOUSE_COLORS['hot_magenta'],
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

            ax.set_ylabel('Holdings ($ Trillions)', fontsize=10)
            ax.set_xlabel('Date', fontsize=10)
            ax.legend(loc='upper left')
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        else:
            ax.text(0.5, 0.5, 'No data available',
                    ha='center', va='center', transform=ax.transAxes)

    elif hasattr(holdings_data, 'columns'):
        # DataFrame from Treasury TIC
        if 'country' in holdings_data.columns and 'holdings' in holdings_data.columns:
            latest = holdings_data.sort_values('record_date').groupby('country').last()
            top_holders = latest.nlargest(10, 'holdings')

            ax.barh(range(len(top_holders)), top_holders['holdings'].values / 1e3,
                    color=LIGHTHOUSE_COLORS['ocean_blue'], alpha=0.7)
            ax.set_yticks(range(len(top_holders)))
            ax.set_yticklabels(top_holders.index)
            ax.set_xlabel('Holdings ($ Billions)', fontsize=10)

    apply_lighthouse_style(ax, 'Foreign Holdings of U.S. Treasuries')
    add_source(ax, 'FRED (TIC)')

    return fig, 'S2_13_Foreign_Holdings.png'


# =============================================================================
# CHART 19: SRF Usage (NY Fed)
# =============================================================================

def chart_srf_usage():
    """Standing Repo Facility Usage"""
    print("Generating: SRF Usage...")

    repo = data.get_srf_usage()

    if len(repo) == 0:
        print("    ERROR: No repo data")
        return None, None

    fig, ax = create_figure(figsize=(14, 8))

    if 'totalAmtAccepted' in repo.columns:
        ax.bar(repo.index, repo['totalAmtAccepted'].values,
               color=LIGHTHOUSE_COLORS['ocean_blue'], alpha=0.7, width=1)

        current = repo['totalAmtAccepted'].iloc[-1]
        ax.annotate(f'Latest: ${current:.1f}B',
                    (repo.index[-1], current),
                    textcoords='offset points', xytext=(-60, 10),
                    fontsize=9, fontweight='bold',
                    color=LIGHTHOUSE_COLORS['hot_magenta'],
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    ax.set_ylabel('Amount ($ Billions)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)
    ax.set_ylim(bottom=0)

    apply_lighthouse_style(ax, 'Fed Repo Operations (incl. SRF)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    add_source(ax, 'NY Fed')

    return fig, 'S2_14_SRF_Usage.png'


# =============================================================================
# CHART 20: Primary Dealer Positioning (NY Fed)
# =============================================================================

def chart_primary_dealer_positioning():
    """Primary Dealer Net Positions"""
    print("Generating: Primary Dealer Positioning...")

    # This is a large CSV download
    pd_data = data.nyfed.get_primary_dealer_timeseries()

    if len(pd_data) == 0:
        print("    ERROR: No PD data")
        return None, None

    fig, ax = create_figure(figsize=(14, 8))

    # PD data has many series - identify key ones
    if 'As Of Date' in pd_data.columns:
        pd_data['date'] = pd.to_datetime(pd_data['As Of Date'])
        pd_data = pd_data.set_index('date').sort_index()

        # Look for net positions columns
        pos_cols = [c for c in pd_data.columns if 'Net' in c or 'Position' in c]
        if pos_cols:
            for col in pos_cols[:3]:  # Plot first 3
                ax.plot(pd_data.index, pd_data[col], linewidth=1.5, label=col[:30])
            ax.legend(loc='upper left', fontsize=7)

    ax.set_ylabel('Position ($ Billions)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)

    apply_lighthouse_style(ax, 'Primary Dealer Net Positioning')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'NY Fed Primary Dealer Survey')

    return fig, 'S2_17_Primary_Dealer.png'


# =============================================================================
# CHART 21: 10Y-2Y Spread (FRED)
# =============================================================================

def chart_yield_spread_10y2y():
    """10Y-2Y Treasury Spread"""
    print("Generating: 10Y-2Y Spread...")

    yields = data.get_yield_curve()
    y10 = yields.get('10Y', pd.Series())
    y2 = yields.get('2Y', pd.Series())

    if len(y10) == 0 or len(y2) == 0:
        print("    ERROR: No yield data")
        return None, None

    # Align dates
    common = y10.index.intersection(y2.index)
    spread = (y10.loc[common] - y2.loc[common]) * 100  # bps

    # Last 10 years
    spread = spread[spread.index >= '2015-01-01']

    fig, ax = create_figure(figsize=(14, 7))

    # Color by sign
    ax.fill_between(spread.index, 0, spread.values,
                    where=spread.values >= 0,
                    color=LIGHTHOUSE_COLORS['teal_green'], alpha=0.5)
    ax.fill_between(spread.index, 0, spread.values,
                    where=spread.values < 0,
                    color=LIGHTHOUSE_COLORS['pure_red'], alpha=0.5)

    ax.axhline(y=0, color='black', linewidth=1.5)

    # Current
    current = spread.iloc[-1]
    ax.annotate(f'Current: {current:.0f} bps',
                (spread.index[-1], current),
                textcoords='offset points', xytext=(-80, 20 if current > 0 else -30),
                fontsize=10, fontweight='bold',
                color=LIGHTHOUSE_COLORS['hot_magenta'],
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    add_callout_box(ax,
                    "YIELD CURVE SIGNAL:\n"
                    "- Positive: Normal (expansion)\n"
                    "- Negative: Inverted (recession risk)\n"
                    "- Steepening: Recovery signal",
                    (0.02, 0.25), fontsize=8)

    ax.set_ylabel('Spread (bps)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)

    apply_lighthouse_style(ax, '10Y-2Y Treasury Spread: Curve Inversion Signal')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'FRED (DGS10, DGS2)')

    return fig, 'S1_17_Yield_Spread_10Y2Y.png'


# =============================================================================
# CHART 22: Fed Funds Target vs EFFR (FRED)
# =============================================================================

def chart_fed_funds_vs_effr():
    """Fed Funds Target Range vs EFFR"""
    print("Generating: Fed Funds vs EFFR...")

    effr = data.fred.get_effr()
    ff_upper = data.fred.get_series('DFEDTARU', '2015-01-01')
    ff_lower = data.fred.get_series('DFEDTARL', '2015-01-01')

    if len(effr) == 0:
        print("    ERROR: No EFFR data")
        return None, None

    # Limit to recent years
    effr = effr[effr.index >= '2015-01-01']

    fig, ax = create_figure(figsize=(14, 7))

    # Plot target range
    if len(ff_upper) > 0 and len(ff_lower) > 0:
        ff_upper = ff_upper[ff_upper.index >= '2015-01-01']
        ff_lower = ff_lower[ff_lower.index >= '2015-01-01']
        ax.fill_between(ff_upper.index, ff_lower.values, ff_upper.values,
                        color=LIGHTHOUSE_COLORS['neutral_gray'], alpha=0.3,
                        label='Target Range')
        ax.step(ff_upper.index, ff_upper.values, where='post',
                color=LIGHTHOUSE_COLORS['neutral_gray'], linewidth=1.5)
        ax.step(ff_lower.index, ff_lower.values, where='post',
                color=LIGHTHOUSE_COLORS['neutral_gray'], linewidth=1.5)

    # Plot EFFR
    ax.plot(effr.index, effr.values,
            color=LIGHTHOUSE_COLORS['ocean_blue'], linewidth=1.5, label='EFFR')

    current = effr.iloc[-1]
    ax.annotate(f'EFFR: {current:.2f}%',
                (effr.index[-1], current),
                textcoords='offset points', xytext=(-70, 10),
                fontsize=9, fontweight='bold',
                color=LIGHTHOUSE_COLORS['ocean_blue'])

    ax.set_ylabel('Rate (%)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)
    ax.legend(loc='upper left')

    apply_lighthouse_style(ax, 'Fed Funds Target Range vs EFFR')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'FRED (EFFR, DFEDTARU, DFEDTARL)')

    return fig, 'S1_18_Fed_Funds_EFFR.png'


# =============================================================================
# CHART 23: Mortgage Rates (FRED)
# =============================================================================

def chart_mortgage_rates():
    """30Y Mortgage Rate"""
    print("Generating: Mortgage Rates...")

    mortgage = data.fred.get_series('MORTGAGE30US', '2000-01-01')

    if len(mortgage) == 0:
        print("    ERROR: No mortgage data")
        return None, None

    fig, ax = create_figure(figsize=(14, 7))

    ax.plot(mortgage.index, mortgage.values,
            color=LIGHTHOUSE_COLORS['ocean_blue'], linewidth=2)

    ax.fill_between(mortgage.index, 0, mortgage.values,
                    color=LIGHTHOUSE_COLORS['ocean_blue'], alpha=0.2)

    # Historical average
    avg = mortgage.mean()
    ax.axhline(y=avg, color=LIGHTHOUSE_COLORS['neutral_gray'],
               linestyle='--', linewidth=1.5)
    ax.text(mortgage.index[0], avg + 0.3, f'Avg: {avg:.1f}%',
            fontsize=8, color=LIGHTHOUSE_COLORS['neutral_gray'])

    current = mortgage.iloc[-1]
    ax.annotate(f'Current: {current:.2f}%',
                (mortgage.index[-1], current),
                textcoords='offset points', xytext=(-80, 10),
                fontsize=10, fontweight='bold',
                color=LIGHTHOUSE_COLORS['hot_magenta'],
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    ax.set_ylabel('Rate (%)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)
    ax.set_ylim(bottom=0)

    apply_lighthouse_style(ax, '30-Year Mortgage Rate')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'FRED (MORTGAGE30US)')

    return fig, 'S2_25_Mortgage_Rate.png'


# =============================================================================
# CHART 24: Consumer Sentiment (FRED)
# =============================================================================

def chart_consumer_sentiment():
    """University of Michigan Consumer Sentiment"""
    print("Generating: Consumer Sentiment...")

    sentiment = data.fred.get_series('UMCSENT', '2000-01-01')

    if len(sentiment) == 0:
        print("    ERROR: No sentiment data")
        return None, None

    fig, ax = create_figure(figsize=(14, 7))

    ax.plot(sentiment.index, sentiment.values,
            color=LIGHTHOUSE_COLORS['ocean_blue'], linewidth=2)

    # Recession shading reference
    ax.axhline(y=80, color=LIGHTHOUSE_COLORS['dusk_orange'],
               linestyle='--', linewidth=1.5)
    ax.text(sentiment.index[0], 81, 'Caution Zone (<80)',
            fontsize=8, color=LIGHTHOUSE_COLORS['dusk_orange'])

    avg = sentiment.mean()
    ax.axhline(y=avg, color=LIGHTHOUSE_COLORS['neutral_gray'],
               linestyle=':', linewidth=1.5)

    current = sentiment.iloc[-1]
    ax.annotate(f'Current: {current:.1f}',
                (sentiment.index[-1], current),
                textcoords='offset points', xytext=(-70, 10),
                fontsize=10, fontweight='bold',
                color=LIGHTHOUSE_COLORS['hot_magenta'],
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    ax.set_ylabel('Index', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)

    apply_lighthouse_style(ax, 'U. Michigan Consumer Sentiment')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'FRED (UMCSENT)')

    return fig, 'S2_26_Consumer_Sentiment.png'


# =============================================================================
# CHART 25: PCE Inflation (FRED)
# =============================================================================

def chart_pce_inflation():
    """PCE and Core PCE Inflation"""
    print("Generating: PCE Inflation...")

    pce = data.fred.get_series('PCEPI', '2015-01-01')
    core_pce = data.fred.get_series('PCEPILFE', '2015-01-01')

    if len(pce) == 0:
        print("    ERROR: No PCE data")
        return None, None

    # Calculate YoY
    pce_yoy = pce.pct_change(12) * 100
    core_yoy = core_pce.pct_change(12) * 100 if len(core_pce) > 12 else pd.Series()

    fig, ax = create_figure(figsize=(14, 7))

    ax.plot(pce_yoy.index, pce_yoy.values,
            color=LIGHTHOUSE_COLORS['ocean_blue'], linewidth=2, label='PCE YoY')

    if len(core_yoy) > 0:
        ax.plot(core_yoy.index, core_yoy.values,
                color=LIGHTHOUSE_COLORS['dusk_orange'], linewidth=2,
                linestyle='--', label='Core PCE YoY')

    # 2% target
    ax.axhline(y=2, color=LIGHTHOUSE_COLORS['teal_green'],
               linestyle='--', linewidth=2)
    ax.text(pce_yoy.index[0], 2.2, 'Fed Target: 2%',
            fontsize=8, color=LIGHTHOUSE_COLORS['teal_green'])

    current = core_yoy.iloc[-1] if len(core_yoy) > 0 else pce_yoy.iloc[-1]
    ax.annotate(f'Core PCE: {current:.1f}%',
                (core_yoy.index[-1] if len(core_yoy) > 0 else pce_yoy.index[-1], current),
                textcoords='offset points', xytext=(-80, 10),
                fontsize=10, fontweight='bold',
                color=LIGHTHOUSE_COLORS['hot_magenta'],
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    ax.set_ylabel('YoY Inflation (%)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)
    ax.legend(loc='upper right')

    apply_lighthouse_style(ax, 'PCE Inflation: The Fed\'s Preferred Gauge')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'FRED (PCEPI, PCEPILFE)')

    return fig, 'S1_10_PCE_Inflation.png'


# =============================================================================
# CHART 26: CPI Components (FRED)
# =============================================================================

def chart_cpi_components():
    """CPI Components - Shelter, Services, Goods"""
    print("Generating: CPI Components...")

    cpi_all = data.fred.get_series('CPIAUCSL', '2015-01-01')
    cpi_shelter = data.fred.get_series('CUSR0000SAH1', '2015-01-01')
    cpi_services = data.fred.get_series('CUSR0000SAS', '2015-01-01')

    if len(cpi_all) == 0:
        print("    ERROR: No CPI data")
        return None, None

    # Calculate YoY
    cpi_yoy = cpi_all.pct_change(12) * 100
    shelter_yoy = cpi_shelter.pct_change(12) * 100 if len(cpi_shelter) > 12 else pd.Series()
    services_yoy = cpi_services.pct_change(12) * 100 if len(cpi_services) > 12 else pd.Series()

    fig, ax = create_figure(figsize=(14, 7))

    ax.plot(cpi_yoy.index, cpi_yoy.values,
            color=LIGHTHOUSE_COLORS['ocean_blue'], linewidth=2, label='CPI All Items')

    if len(shelter_yoy) > 0:
        ax.plot(shelter_yoy.index, shelter_yoy.values,
                color=LIGHTHOUSE_COLORS['dusk_orange'], linewidth=1.5,
                linestyle='--', label='Shelter')

    if len(services_yoy) > 0:
        ax.plot(services_yoy.index, services_yoy.values,
                color=LIGHTHOUSE_COLORS['teal_green'], linewidth=1.5,
                linestyle=':', label='Services')

    ax.axhline(y=2, color='black', linestyle='--', linewidth=1.5)

    current = cpi_yoy.iloc[-1]
    ax.annotate(f'CPI: {current:.1f}%',
                (cpi_yoy.index[-1], current),
                textcoords='offset points', xytext=(-70, 10),
                fontsize=9, fontweight='bold',
                color=LIGHTHOUSE_COLORS['ocean_blue'])

    ax.set_ylabel('YoY Inflation (%)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)
    ax.legend(loc='upper right')

    apply_lighthouse_style(ax, 'CPI Components: Where Is Inflation Sticky?')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'FRED (CPIAUCSL, CUSR0000SAH1)')

    return fig, 'S1_11_CPI_Components.png'


# =============================================================================
# CHART 27: Unemployment Rate (FRED)
# =============================================================================

def chart_unemployment_rate():
    """Unemployment Rate"""
    print("Generating: Unemployment Rate...")

    unemp = data.fred.get_series('UNRATE', '2000-01-01')

    if len(unemp) == 0:
        print("    ERROR: No unemployment data")
        return None, None

    fig, ax = create_figure(figsize=(14, 7))

    ax.fill_between(unemp.index, 0, unemp.values,
                    color=LIGHTHOUSE_COLORS['ocean_blue'], alpha=0.4)
    ax.plot(unemp.index, unemp.values,
            color=LIGHTHOUSE_COLORS['ocean_blue'], linewidth=2)

    # Natural rate reference (~4%)
    ax.axhline(y=4.0, color=LIGHTHOUSE_COLORS['teal_green'],
               linestyle='--', linewidth=1.5)
    ax.text(unemp.index[0], 4.2, 'Natural Rate (~4%)',
            fontsize=8, color=LIGHTHOUSE_COLORS['teal_green'])

    current = unemp.iloc[-1]
    ax.annotate(f'Current: {current:.1f}%',
                (unemp.index[-1], current),
                textcoords='offset points', xytext=(-70, 10),
                fontsize=10, fontweight='bold',
                color=LIGHTHOUSE_COLORS['hot_magenta'],
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    ax.set_ylabel('Rate (%)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)
    ax.set_ylim(bottom=0)

    apply_lighthouse_style(ax, 'Unemployment Rate')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'FRED (UNRATE)')

    return fig, 'S2_35_Unemployment_Rate.png'


# =============================================================================
# CHART 28: NFP (FRED)
# =============================================================================

def chart_nfp():
    """Nonfarm Payrolls MoM Change"""
    print("Generating: NFP...")

    nfp = data.fred.get_series('PAYEMS', '2019-01-01')

    if len(nfp) == 0:
        print("    ERROR: No NFP data")
        return None, None

    # Monthly change in thousands
    nfp_change = nfp.diff()

    fig, ax = create_figure(figsize=(14, 7))

    colors = [LIGHTHOUSE_COLORS['teal_green'] if v >= 0 else LIGHTHOUSE_COLORS['pure_red']
              for v in nfp_change.values]

    ax.bar(nfp_change.index, nfp_change.values, color=colors, alpha=0.7, width=20)
    ax.axhline(y=0, color='black', linewidth=1)

    # 200K reference
    ax.axhline(y=200, color=LIGHTHOUSE_COLORS['ocean_blue'],
               linestyle='--', linewidth=1.5)
    ax.text(nfp_change.index[0], 220, 'Trend Pace (~200K)',
            fontsize=8, color=LIGHTHOUSE_COLORS['ocean_blue'])

    current = nfp_change.iloc[-1]
    ax.annotate(f'Latest: {current:.0f}K',
                (nfp_change.index[-1], current),
                textcoords='offset points', xytext=(-60, 10 if current > 0 else -20),
                fontsize=9, fontweight='bold',
                color=LIGHTHOUSE_COLORS['hot_magenta'])

    ax.set_ylabel('MoM Change (Thousands)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)

    apply_lighthouse_style(ax, 'Nonfarm Payrolls: Monthly Job Gains')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'FRED (PAYEMS)')

    return fig, 'S2_37_NFP.png'


# =============================================================================
# CHART 29: Retail Sales (FRED)
# =============================================================================

def chart_retail_sales():
    """Retail Sales YoY"""
    print("Generating: Retail Sales...")

    retail = data.fred.get_series('RSXFS', '2015-01-01')

    if len(retail) == 0:
        print("    ERROR: No retail data")
        return None, None

    retail_yoy = retail.pct_change(12) * 100

    fig, ax = create_figure(figsize=(14, 7))

    ax.fill_between(retail_yoy.index, 0, retail_yoy.values,
                    where=retail_yoy.values >= 0,
                    color=LIGHTHOUSE_COLORS['teal_green'], alpha=0.5)
    ax.fill_between(retail_yoy.index, 0, retail_yoy.values,
                    where=retail_yoy.values < 0,
                    color=LIGHTHOUSE_COLORS['pure_red'], alpha=0.5)

    ax.axhline(y=0, color='black', linewidth=1)

    current = retail_yoy.iloc[-1]
    ax.annotate(f'Current: {current:.1f}% YoY',
                (retail_yoy.index[-1], current),
                textcoords='offset points', xytext=(-80, 10),
                fontsize=9, fontweight='bold',
                color=LIGHTHOUSE_COLORS['hot_magenta'])

    ax.set_ylabel('YoY Change (%)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)

    apply_lighthouse_style(ax, 'Retail Sales (ex Auto): Consumer Spending')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'FRED (RSXFS)')

    return fig, 'S2_27_Retail_Sales.png'


# =============================================================================
# CHART 30: Industrial Production (FRED)
# =============================================================================

def chart_industrial_production():
    """Industrial Production Index"""
    print("Generating: Industrial Production...")

    ip = data.fred.get_series('INDPRO', '2015-01-01')

    if len(ip) == 0:
        print("    ERROR: No IP data")
        return None, None

    ip_yoy = ip.pct_change(12) * 100

    fig, ax = create_figure(figsize=(14, 7))

    ax.plot(ip_yoy.index, ip_yoy.values,
            color=LIGHTHOUSE_COLORS['ocean_blue'], linewidth=2)

    ax.axhline(y=0, color='black', linewidth=1)

    # Shade negative
    ax.fill_between(ip_yoy.index, 0, ip_yoy.values,
                    where=ip_yoy.values < 0,
                    color=LIGHTHOUSE_COLORS['pure_red'], alpha=0.3)

    current = ip_yoy.iloc[-1]
    ax.annotate(f'Current: {current:.1f}% YoY',
                (ip_yoy.index[-1], current),
                textcoords='offset points', xytext=(-80, 10),
                fontsize=9, fontweight='bold',
                color=LIGHTHOUSE_COLORS['hot_magenta'])

    ax.set_ylabel('YoY Change (%)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)

    apply_lighthouse_style(ax, 'Industrial Production')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    add_source(ax, 'FRED (INDPRO)')

    return fig, 'S2_28_Industrial_Production.png'


# =============================================================================
# UPDATED MAIN EXECUTION
# =============================================================================

def generate_all_charts():
    """Generate all charts with REAL DATA ONLY"""

    print("=" * 60)
    print("LIGHTHOUSE MACRO - REAL DATA CHART GENERATION")
    print("NO SYNTHETIC DATA")
    print(f"Target Date: {TARGET_DATE}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60 + "\n")

    chart_functions = [
        # Original 15
        chart_sofr_effr_spread,
        chart_rrp_usage,
        chart_yield_curve_shape,
        chart_credit_spread_percentiles,
        chart_repo_rate_dispersion,
        chart_bank_reserves_gdp,
        chart_labor_fragility_index,
        chart_savings_rate,
        chart_consumer_credit,
        chart_cre_delinquencies,
        chart_auto_delinquencies,
        chart_vix,
        chart_initial_claims,
        chart_federal_debt,
        chart_gdp,
        # New additions
        chart_treasury_auction_tails,
        chart_soma_holdings,
        chart_foreign_holdings,
        chart_srf_usage,
        chart_primary_dealer_positioning,
        chart_yield_spread_10y2y,
        chart_fed_funds_vs_effr,
        chart_mortgage_rates,
        chart_consumer_sentiment,
        chart_pce_inflation,
        chart_cpi_components,
        chart_unemployment_rate,
        chart_nfp,
        chart_retail_sales,
        chart_industrial_production,
    ]

    results = []

    for func in chart_functions:
        try:
            result = func()
            if result[0] is None:
                results.append((func.__name__, 'SKIPPED - No data'))
                continue

            fig, filename = result
            filepath = os.path.join(OUTPUT_DIR, filename)
            fig.savefig(filepath, dpi=DPI, bbox_inches='tight',
                        facecolor='white', edgecolor='none')
            plt.close(fig)
            results.append((filename, 'SUCCESS'))
            print(f"  OK: {filename}")
        except Exception as e:
            results.append((func.__name__, f'FAILED: {str(e)}'))
            print(f"  FAIL: {func.__name__} - {e}")

    # Summary
    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)
    success = sum(1 for _, status in results if status == 'SUCCESS')
    print(f"Generated: {success}/{len(results)} charts")
    print(f"Output: {OUTPUT_DIR}")

    if success < len(results):
        print("\nSkipped/Failed:")
        for name, status in results:
            if status != 'SUCCESS':
                print(f"  - {name}: {status}")

    print("=" * 60)

    return results


if __name__ == '__main__':
    generate_all_charts()
