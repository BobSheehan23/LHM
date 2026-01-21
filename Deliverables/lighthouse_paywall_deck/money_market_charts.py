"""
Money Market Plumbing Charts - Live Data Implementation
Charts 33-42: OFR + NY Fed + FRED Integration
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data_sources import DataOrchestrator

# Lighthouse Macro Brand Colors
COLORS = {
    'primary': '#003366',
    'secondary': '#0066CC',
    'accent': '#FF9900',
    'positive': '#00A86B',
    'negative': '#CC0000',
    'neutral': '#808080',
}


def add_branding(ax, chart_number):
    """Lighthouse Macro standard branding - NO GRIDLINES"""
    from matplotlib.patches import Circle

    # Chart number badge
    circle = Circle((0.02, 0.98), 0.015, transform=ax.transAxes,
                   facecolor=COLORS['primary'], edgecolor='none', zorder=100)
    ax.add_patch(circle)
    ax.text(0.02, 0.98, str(chart_number),
            ha='center', va='center', fontsize=10, fontweight='bold',
            color='white', transform=ax.transAxes, zorder=101)

    # Top left: LIGHTHOUSE MACRO
    ax.text(0.045, 0.98, 'LIGHTHOUSE MACRO',
            ha='left', va='center', fontsize=9, fontweight='bold',
            color=COLORS['primary'], transform=ax.transAxes)

    # Bottom left: Source credit (small grey)
    ax.text(0.02, 0.02, 'Source: NY Fed, OFR, FRED',
            ha='left', va='bottom', fontsize=7, color=COLORS['neutral'],
            transform=ax.transAxes, style='italic')

    # Bottom right: Watermark (ocean blue)
    ax.text(0.98, 0.02, 'MACRO, ILLUMINATED.',
            ha='right', va='bottom', fontsize=8, fontweight='bold',
            color=COLORS['primary'], alpha=0.6, transform=ax.transAxes)

    # Clean axes - NO GRIDLINES
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['neutral'])
    ax.spines['bottom'].set_color(COLORS['neutral'])
    ax.tick_params(colors=COLORS['neutral'])


def chart_33_money_market_dashboard(data_source):
    """
    Chart 33: Money Market Dashboard (4-Panel Plumbing Health)
    SOFR, EFFR, RRP, and Spread Analysis
    """
    fig = plt.figure(figsize=(11, 8.5))
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

    # Get data
    mm_data = data_source.get_money_market_rates()
    liq_data = data_source.get_liquidity_metrics()

    # Panel 1: SOFR vs EFFR
    ax1 = fig.add_subplot(gs[0, 0])
    if 'SOFR' in mm_data and len(mm_data['SOFR']) > 0:
        mm_data['SOFR'].plot(ax=ax1, label='SOFR', color=COLORS['primary'], linewidth=2)
    if 'EFFR' in mm_data and len(mm_data['EFFR']) > 0:
        mm_data['EFFR'].plot(ax=ax1, label='EFFR', color=COLORS['secondary'], linewidth=2)
    if 'IORB' in mm_data and len(mm_data['IORB']) > 0:
        mm_data['IORB'].plot(ax=ax1, label='IORB', color=COLORS['neutral'],
                           linewidth=1.5, linestyle='--')
    ax1.set_title('Money Market Rates', fontweight='bold', fontsize=12)
    ax1.set_ylabel('Rate (%)', fontsize=10)
    ax1.legend(loc='best', fontsize=9)
    # Grid removed - clean chart style

    # Panel 2: RRP Facility
    ax2 = fig.add_subplot(gs[0, 1])
    if 'RRP' in liq_data and len(liq_data['RRP']) > 0:
        (liq_data['RRP'] / 1000).plot(ax=ax2, color=COLORS['accent'], linewidth=2)
    elif 'RRP_FRED' in liq_data and len(liq_data['RRP_FRED']) > 0:
        (liq_data['RRP_FRED'] / 1000).plot(ax=ax2, color=COLORS['accent'], linewidth=2)
    ax2.set_title('Overnight Reverse Repo Facility', fontweight='bold', fontsize=12)
    ax2.set_ylabel('Billions USD', fontsize=10)
    # Grid removed - clean chart style

    # Panel 3: SOFR-EFFR Spread
    ax3 = fig.add_subplot(gs[1, 0])
    if 'SOFR' in mm_data and 'EFFR' in mm_data:
        if len(mm_data['SOFR']) > 0 and len(mm_data['EFFR']) > 0:
            spread = (mm_data['SOFR'] - mm_data['EFFR']).dropna()
            if len(spread) > 0:
                spread.plot(ax=ax3, color=COLORS['secondary'], linewidth=2)
                ax3.axhline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.5)
                ax3.fill_between(spread.index, 0, spread.values,
                               where=(spread.values > 0), alpha=0.3,
                               color=COLORS['positive'], label='SOFR > EFFR')
                ax3.fill_between(spread.index, 0, spread.values,
                               where=(spread.values < 0), alpha=0.3,
                               color=COLORS['negative'], label='SOFR < EFFR')
    ax3.set_title('SOFR-EFFR Spread', fontweight='bold', fontsize=12)
    ax3.set_ylabel('Basis Points', fontsize=10)
    ax3.legend(loc='best', fontsize=8)
    # Grid removed - clean chart style

    # Panel 4: Bank Reserves
    ax4 = fig.add_subplot(gs[1, 1])
    if 'Reserves' in liq_data and len(liq_data['Reserves']) > 0:
        (liq_data['Reserves'] / 1000).plot(ax=ax4, color=COLORS['primary'], linewidth=2)
    ax4.set_title('Bank Reserves at Fed', fontweight='bold', fontsize=12)
    ax4.set_ylabel('Billions USD', fontsize=10)
    # Grid removed - clean chart style

    fig.suptitle('Money Market Plumbing Dashboard', fontsize=16, fontweight='bold', y=0.98)
    add_branding(ax1, 33)
    plt.tight_layout()

    return fig


def chart_34_swap_spreads(data_source):
    """
    Chart 34: Swap Spreads Across Yield Curve
    2Y, 5Y, 10Y, 30Y swap spreads
    """
    fig, ax = plt.subplots(figsize=(11, 8.5))

    # Fetch swap spread data from FRED
    swap_2y = data_source.safe_fetch_fred('DISCONTINUED_MSWP2', name='2Y Swap Spread')
    swap_5y = data_source.safe_fetch_fred('DISCONTINUED_MSWP5', name='5Y Swap Spread')
    swap_10y = data_source.safe_fetch_fred('DISCONTINUED_MSWP10', name='10Y Swap Spread')
    swap_30y = data_source.safe_fetch_fred('DISCONTINUED_MSWP30', name='30Y Swap Spread')

    # Try alternative tickers
    if len(swap_2y) == 0:
        swap_2y = data_source.safe_fetch_fred('DSWP2', name='2Y Swap Spread')
    if len(swap_5y) == 0:
        swap_5y = data_source.safe_fetch_fred('DSWP5', name='5Y Swap Spread')
    if len(swap_10y) == 0:
        swap_10y = data_source.safe_fetch_fred('DSWP10', name='10Y Swap Spread')
    if len(swap_30y) == 0:
        swap_30y = data_source.safe_fetch_fred('DSWP30', name='30Y Swap Spread')

    colors = [COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['positive']]

    for i, (spread, label) in enumerate([(swap_2y, '2Y'), (swap_5y, '5Y'),
                                          (swap_10y, '10Y'), (swap_30y, '30Y')]):
        if len(spread) > 0:
            spread.plot(ax=ax, label=label, color=colors[i % len(colors)], linewidth=2)

    ax.axhline(0, color='black', linewidth=1, linestyle='--', alpha=0.5)
    ax.set_title('Swap Spreads Across the Curve', fontsize=14, fontweight='bold')
    ax.set_ylabel('Basis Points', fontsize=11)
    ax.set_xlabel('Date', fontsize=11)
    ax.legend(loc='best', fontsize=10)
    # Grid removed - clean chart style

    add_branding(ax, 34)
    plt.tight_layout()

    return fig


def chart_35_bill_ois_spread(data_source):
    """
    Chart 35: Bill-OIS Spread vs MMF Flows
    Credit risk indicator in short-term funding markets
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8.5), height_ratios=[2, 1])

    # T-Bill rates
    tbill_3m = data_source.safe_fetch_fred('DTB3', name='3M T-Bill')
    tbill_6m = data_source.safe_fetch_fred('DTB6', name='6M T-Bill')

    # OIS equivalent (use SOFR or EFFR as proxy)
    mm_data = data_source.get_money_market_rates()
    ois_proxy = mm_data.get('SOFR', mm_data.get('EFFR', pd.Series(dtype=float)))

    # Calculate spread
    if len(tbill_3m) > 0 and len(ois_proxy) > 0:
        # Align dates
        combined = pd.DataFrame({'TBill': tbill_3m, 'OIS': ois_proxy}).dropna()
        if len(combined) > 0:
            spread = combined['TBill'] - combined['OIS']
            spread.plot(ax=ax1, color=COLORS['negative'], linewidth=2.5, label='3M T-Bill - OIS')
            ax1.axhline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.5)
            ax1.fill_between(spread.index, 0, spread.values,
                           where=(spread.values > 0), alpha=0.3, color=COLORS['negative'])

    ax1.set_title('T-Bill - OIS Spread (Credit Risk Indicator)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Basis Points', fontsize=11)
    ax1.legend(loc='best', fontsize=10)
    # Grid removed - clean chart style

    # MMF Assets
    mmf_total = data_source.safe_fetch_fred('MMMFFAQ027S', name='MMF Total Assets')
    if len(mmf_total) > 0:
        (mmf_total / 1000).plot(ax=ax2, color=COLORS['secondary'], linewidth=2)

    ax2.set_title('Money Market Fund Assets', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Billions USD', fontsize=10)
    ax2.set_xlabel('Date', fontsize=11)
    # Grid removed - clean chart style

    add_branding(ax1, 35)
    plt.tight_layout()

    return fig


def chart_36_basis_trade_capacity(data_source):
    """
    Chart 36: Basis Trade Capacity - Hedge Fund Leverage
    Treasury cash-futures basis and dealer leverage
    """
    fig, ax = plt.subplots(figsize=(11, 8.5))

    # Proxy metrics for basis trade capacity
    # 1. Treasury-Eurodollar (TED) spread
    ted_spread = data_source.safe_fetch_fred('TEDRATE', name='TED Spread')

    # 2. Primary dealer financing
    dealer_positions = data_source.safe_fetch_fred('H41RESPPSDBWAQ', name='Dealer Financing')

    if len(ted_spread) > 0:
        ted_spread.plot(ax=ax, color=COLORS['primary'], linewidth=2.5, label='TED Spread (3M)')

    ax.set_title('Basis Trade Capacity Indicator', fontsize=14, fontweight='bold')
    ax.set_ylabel('Basis Points', fontsize=11)
    ax.set_xlabel('Date', fontsize=11)
    ax.legend(loc='best', fontsize=10)
    # Grid removed - clean chart style

    # Highlight stress periods
    ax.axhline(50, color=COLORS['accent'], linewidth=1, linestyle='--',
              alpha=0.7, label='Stress Threshold')

    add_branding(ax, 36)
    plt.tight_layout()

    return fig


def chart_37_cross_currency_basis(data_source):
    """
    Chart 37: Cross-Currency Basis - Dollar Funding Stress
    EUR/USD and JPY/USD basis swaps
    """
    fig, ax = plt.subplots(figsize=(11, 8.5))

    # Cross-currency basis indicators (if available from FRED)
    # These may not be available - using FX volatility as proxy
    eurusd = data_source.safe_fetch_fred('DEXUSEU', name='EUR/USD')
    jpyusd = data_source.safe_fetch_fred('DEXJPUS', name='JPY/USD')

    # Calculate rolling volatility as stress indicator
    if len(eurusd) > 0:
        eur_vol = eurusd.pct_change().rolling(30).std() * 100 * np.sqrt(252)
        eur_vol.plot(ax=ax, label='EUR/USD Volatility', color=COLORS['secondary'], linewidth=2)

    if len(jpyusd) > 0:
        jpy_vol = jpyusd.pct_change().rolling(30).std() * 100 * np.sqrt(252)
        jpy_vol.plot(ax=ax, label='JPY/USD Volatility', color=COLORS['accent'], linewidth=2)

    ax.set_title('Cross-Currency Funding Stress Indicators', fontsize=14, fontweight='bold')
    ax.set_ylabel('Annualized Volatility (%)', fontsize=11)
    ax.set_xlabel('Date', fontsize=11)
    ax.legend(loc='best', fontsize=10)
    # Grid removed - clean chart style

    add_branding(ax, 37)
    plt.tight_layout()

    return fig


def chart_38_repo_market_depth(data_source):
    """
    Chart 38: Repo Market Depth - Collateral Availability
    RRP, Repo volumes, and collateral scarcity
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8.5))

    liq_data = data_source.get_liquidity_metrics()

    # RRP (reverse repo)
    if 'RRP' in liq_data and len(liq_data['RRP']) > 0:
        (liq_data['RRP'] / 1000).plot(ax=ax1, color=COLORS['primary'], linewidth=2.5, label='RRP')
    elif 'RRP_FRED' in liq_data and len(liq_data['RRP_FRED']) > 0:
        (liq_data['RRP_FRED'] / 1000).plot(ax=ax1, color=COLORS['primary'], linewidth=2.5, label='RRP')

    ax1.set_title('Overnight Reverse Repo Operations', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Billions USD', fontsize=11)
    ax1.legend(loc='best', fontsize=10)
    # Grid removed - clean chart style

    # Treasury General Account (TGA) - collateral supply indicator
    if 'TGA' in liq_data and len(liq_data['TGA']) > 0:
        (liq_data['TGA'] / 1000).plot(ax=ax2, color=COLORS['secondary'], linewidth=2.5)

    ax2.set_title('Treasury General Account Balance', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Billions USD', fontsize=10)
    ax2.set_xlabel('Date', fontsize=11)
    # Grid removed - clean chart style

    add_branding(ax1, 38)
    plt.tight_layout()

    return fig


def chart_39_sofr_effr_dynamics(data_source):
    """
    Chart 39: SOFR-EFFR Dynamics - Rate Differentials
    Detailed analysis of secured vs unsecured overnight rates
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8.5), height_ratios=[2, 1])

    mm_data = data_source.get_money_market_rates()

    # Rates overlay
    if 'SOFR' in mm_data and len(mm_data['SOFR']) > 0:
        mm_data['SOFR'].plot(ax=ax1, label='SOFR (Secured)',
                           color=COLORS['primary'], linewidth=2)
    if 'EFFR' in mm_data and len(mm_data['EFFR']) > 0:
        mm_data['EFFR'].plot(ax=ax1, label='EFFR (Unsecured)',
                           color=COLORS['secondary'], linewidth=2)
    if 'IORB' in mm_data and len(mm_data['IORB']) > 0:
        mm_data['IORB'].plot(ax=ax1, label='IORB (Floor)',
                           color=COLORS['neutral'], linewidth=1.5, linestyle='--')

    ax1.set_title('Overnight Rate Dynamics', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Rate (%)', fontsize=11)
    ax1.legend(loc='best', fontsize=10)
    # Grid removed - clean chart style

    # Spread analysis
    if 'SOFR' in mm_data and 'EFFR' in mm_data:
        if len(mm_data['SOFR']) > 0 and len(mm_data['EFFR']) > 0:
            combined = pd.DataFrame({
                'SOFR': mm_data['SOFR'],
                'EFFR': mm_data['EFFR']
            }).dropna()

            if len(combined) > 0:
                spread = combined['SOFR'] - combined['EFFR']
                spread.plot(ax=ax2, color=COLORS['accent'], linewidth=2.5)
                ax2.axhline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.5)

                # Color zones
                ax2.fill_between(spread.index, 0, spread.values,
                               where=(spread.values > 0), alpha=0.3,
                               color=COLORS['positive'])
                ax2.fill_between(spread.index, 0, spread.values,
                               where=(spread.values < 0), alpha=0.3,
                               color=COLORS['negative'])

    ax2.set_title('SOFR-EFFR Spread (Secured vs Unsecured Premium)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Basis Points', fontsize=10)
    ax2.set_xlabel('Date', fontsize=11)
    # Grid removed - clean chart style

    add_branding(ax1, 39)
    plt.tight_layout()

    return fig


def chart_40_treasury_fails(data_source):
    """
    Chart 40: Treasury Fails - Settlement Stress
    Failed treasury settlements as market stress indicator
    """
    fig, ax = plt.subplots(figsize=(11, 8.5))

    # Treasury fails data from FRED
    fails = data_source.safe_fetch_fred('FDHBFRBN', name='Treasury Fails')

    if len(fails) > 0:
        (fails / 1000).plot(ax=ax, color=COLORS['negative'], linewidth=2.5)

        # Highlight stress periods
        ax.axhline(50, color=COLORS['accent'], linewidth=1, linestyle='--',
                  alpha=0.7, label='Elevated Stress (>$50B)')

        # Shade high stress regions
        ax.fill_between(fails.index, 0, fails.values / 1000,
                       where=(fails.values / 1000 > 50), alpha=0.3,
                       color=COLORS['negative'], label='High Stress')

    ax.set_title('Treasury Settlement Fails (Market Stress Indicator)',
                fontsize=14, fontweight='bold')
    ax.set_ylabel('Billions USD', fontsize=11)
    ax.set_xlabel('Date', fontsize=11)
    ax.legend(loc='best', fontsize=10)
    # Grid removed - clean chart style

    add_branding(ax, 40)
    plt.tight_layout()

    return fig


def chart_41_dealer_positioning(data_source):
    """
    Chart 41: Dealer Positioning - Primary Dealer Survey
    Net treasury positions of primary dealers
    """
    fig, ax = plt.subplots(figsize=(11, 8.5))

    # Primary dealer treasury positions
    dealer_positions = data_source.safe_fetch_fred('H41RESPPSDBWAQ',
                                                   name='Dealer Treasury Positions')

    if len(dealer_positions) > 0:
        (dealer_positions / 1000).plot(ax=ax, color=COLORS['primary'], linewidth=2.5)
        ax.axhline(0, color='black', linewidth=1, linestyle='--', alpha=0.5)

        # Shade positive/negative positioning
        ax.fill_between(dealer_positions.index, 0, dealer_positions.values / 1000,
                       where=(dealer_positions.values > 0), alpha=0.3,
                       color=COLORS['positive'], label='Long Positioning')
        ax.fill_between(dealer_positions.index, 0, dealer_positions.values / 1000,
                       where=(dealer_positions.values < 0), alpha=0.3,
                       color=COLORS['negative'], label='Short Positioning')

    ax.set_title('Primary Dealer Treasury Positioning', fontsize=14, fontweight='bold')
    ax.set_ylabel('Billions USD', fontsize=11)
    ax.set_xlabel('Date', fontsize=11)
    ax.legend(loc='best', fontsize=10)
    # Grid removed - clean chart style

    add_branding(ax, 41)
    plt.tight_layout()

    return fig


def chart_42_mmf_composition(data_source):
    """
    Chart 42: MMF Composition - Government vs Prime
    Breakdown of money market fund types
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8.5))

    # Government MMF
    gov_mmf = data_source.safe_fetch_fred('MMMFFAQ027S', name='Total MMF')

    # Institutional vs Retail
    inst_mmf = data_source.safe_fetch_fred('WRMFNS', name='Institutional MMF')
    retail_mmf = data_source.safe_fetch_fred('RMMMFAQ027S', name='Retail MMF')

    # Plot total
    if len(gov_mmf) > 0:
        (gov_mmf / 1000).plot(ax=ax1, color=COLORS['primary'], linewidth=2.5, label='Total MMF')

    ax1.set_title('Total Money Market Fund Assets', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Billions USD', fontsize=11)
    ax1.legend(loc='best', fontsize=10)
    # Grid removed - clean chart style

    # Plot institutional vs retail
    if len(inst_mmf) > 0:
        (inst_mmf / 1000).plot(ax=ax2, label='Institutional',
                             color=COLORS['secondary'], linewidth=2)
    if len(retail_mmf) > 0:
        (retail_mmf / 1000).plot(ax=ax2, label='Retail',
                               color=COLORS['accent'], linewidth=2)

    ax2.set_title('MMF Breakdown: Institutional vs Retail', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Billions USD', fontsize=10)
    ax2.set_xlabel('Date', fontsize=11)
    ax2.legend(loc='best', fontsize=10)
    # Grid removed - clean chart style

    add_branding(ax1, 42)
    plt.tight_layout()

    return fig
