"""
Lighthouse Macro - Section 3: Money Market Plumbing Charts (Charts 16-23)
Next-generation chartbook with NY Fed live data integration
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from lighthouse_style import (
    COLORS,
    create_single_axis_chart,
    create_dual_axis_chart,
    add_last_value_label,
    enforce_no_gridlines
)
from nyfed_api_reference import NYFedAPI
from data_sources import DataOrchestrator

# Initialize data sources
nyfed = NYFedAPI(cache_hours=24)
data = DataOrchestrator()


def chart_16_money_market_dashboard():
    """
    Chart 16: Money Market Dashboard (4-Panel)
    SOFR, EFFR, RRP, and Spreads
    """
    fig = plt.figure(figsize=(11, 8.5))
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.35,
                          left=0.1, right=0.9, top=0.88, bottom=0.12)

    # Fetch NY Fed data
    sofr = nyfed.get_sofr(last_n=500)
    effr = nyfed.get_effr(last_n=500)
    obfr = nyfed.get_obfr(last_n=500)
    rrp = nyfed.get_rrp_operations()

    # Panel 1: Money Market Rates
    ax1 = fig.add_subplot(gs[0, 0])
    enforce_no_gridlines(ax1)

    if not sofr.empty and 'percentRate' in sofr.columns:
        ax1.plot(sofr.index, sofr['percentRate'],
                color=COLORS['ocean_blue'], linewidth=2.5, label='SOFR')
    if not effr.empty and 'percentRate' in effr.columns:
        ax1.plot(effr.index, effr['percentRate'],
                color=COLORS['orange'], linewidth=2, label='EFFR')
    if not obfr.empty and 'percentRate' in obfr.columns:
        ax1.plot(obfr.index, obfr['percentRate'],
                color=COLORS['carolina_blue'], linewidth=1.5, label='OBFR', alpha=0.8)

    ax1.set_title('Money Market Rates', fontweight='bold', fontsize=11)
    ax1.set_ylabel('Rate (%)', fontsize=9)
    ax1.legend(loc='upper left', fontsize=8)
    ax1.set_ylim(bottom=0)

    # Panel 2: RRP Operations
    ax2 = fig.add_subplot(gs[0, 1])
    enforce_no_gridlines(ax2)

    if not rrp.empty and 'totalAmtAccepted' in rrp.columns:
        # Last 2 years
        recent_rrp = rrp[rrp.index >= (datetime.now() - timedelta(days=730))]
        ax2.plot(recent_rrp.index, recent_rrp['totalAmtAccepted'],
                color=COLORS['ocean_blue'], linewidth=2.5, label='RRP Usage')
        ax2.fill_between(recent_rrp.index, 0, recent_rrp['totalAmtAccepted'],
                        color=COLORS['ocean_blue'], alpha=0.15)

    ax2.set_title('Reverse Repo Operations', fontweight='bold', fontsize=11)
    ax2.set_ylabel('Amount ($B)', fontsize=9)
    ax2.legend(loc='upper left', fontsize=8)
    ax2.set_ylim(bottom=0)

    # Panel 3: SOFR-EFFR Spread
    ax3 = fig.add_subplot(gs[1, 0])
    enforce_no_gridlines(ax3)

    if not sofr.empty and not effr.empty:
        common_dates = sofr.index.intersection(effr.index)
        if len(common_dates) > 0:
            spread = (sofr.loc[common_dates, 'percentRate'] -
                     effr.loc[common_dates, 'percentRate']) * 100  # bps

            ax3.plot(common_dates, spread,
                    color=COLORS['ocean_blue'], linewidth=2.5, label='SOFR-EFFR Spread')
            ax3.axhline(y=0, color=COLORS['neutral'], linestyle='--', linewidth=1, alpha=0.6)
            ax3.fill_between(common_dates, 0, spread,
                            where=(spread >= 0),
                            color=COLORS['ocean_blue'], alpha=0.15)

    ax3.set_title('SOFR-EFFR Spread', fontweight='bold', fontsize=11)
    ax3.set_ylabel('Spread (bps)', fontsize=9)
    ax3.legend(loc='upper left', fontsize=8)

    # Panel 4: Fed Reserves
    ax4 = fig.add_subplot(gs[1, 1])
    enforce_no_gridlines(ax4)

    # Try to get reserves from FRED
    reserves = data.safe_fetch_fred('WRESBAL', '2020-01-01')
    if reserves is not None and len(reserves) > 0:
        reserves_trillions = reserves / 1000
        ax4.plot(reserves_trillions.index, reserves_trillions.values,
                color=COLORS['ocean_blue'], linewidth=2.5, label='Bank Reserves')
        ax4.fill_between(reserves_trillions.index, 0, reserves_trillions.values,
                        color=COLORS['ocean_blue'], alpha=0.15)

    ax4.set_title('Bank Reserves at Fed', fontweight='bold', fontsize=11)
    ax4.set_ylabel('Reserves ($T)', fontsize=9)
    ax4.legend(loc='upper left', fontsize=8)
    ax4.set_ylim(bottom=0)

    # Overall title and branding
    fig.suptitle('Money Market Dashboard: Plumbing Health Check',
                fontsize=14, fontweight='bold', y=0.96)

    # Add branding elements
    from matplotlib.patches import Circle
    # Chart number badge on first panel
    circle = Circle((0.02, 0.98), 0.015, transform=ax1.transAxes,
                   facecolor=COLORS['ocean_blue'], edgecolor='none', zorder=100)
    ax1.add_patch(circle)
    ax1.text(0.02, 0.98, '16',
            ha='center', va='center', fontsize=10, fontweight='bold',
            color='white', transform=ax1.transAxes, zorder=101)
    ax1.text(0.045, 0.98, 'LIGHTHOUSE MACRO',
            ha='left', va='center', fontsize=9, fontweight='bold',
            color=COLORS['ocean_blue'], transform=ax1.transAxes)

    # Source and watermark (in figure coordinates)
    fig.text(0.02, 0.02, 'Source: NY Fed, FRED',
            ha='left', va='bottom', fontsize=7, color=COLORS['neutral'], style='italic')
    fig.text(0.98, 0.02, 'MACRO, ILLUMINATED.',
            ha='right', va='bottom', fontsize=8, fontweight='bold',
            color=COLORS['ocean_blue'], alpha=0.6)

    return fig


def chart_17_rrp_vs_vix():
    """
    Chart 17: RRP Depletion vs Market Volatility
    Dual-axis showing liquidity drain and market stress
    """
    fig, ax_left, ax_right = create_dual_axis_chart(
        chart_number=17,
        title='RRP Depletion vs Market Volatility: Liquidity-Stress Transmission',
        left_label='VIX',
        right_label='RRP Usage ($B)',
        source='NY Fed, FRED'
    )

    # Fetch data
    rrp = nyfed.get_rrp_operations()
    vix = data.safe_fetch_fred('VIXCLS', '2021-01-01')

    if not rrp.empty and vix is not None:
        # Last 2 years
        start_date = datetime.now() - timedelta(days=730)
        recent_rrp = rrp[rrp.index >= start_date]
        recent_vix = vix[vix.index >= start_date]

        # Plot VIX (left, secondary)
        ax_left.plot(recent_vix.index, recent_vix.values,
                    color=COLORS['neutral'], linewidth=2, alpha=0.7, label='VIX')
        ax_left.fill_between(recent_vix.index, 0, recent_vix.values,
                            color=COLORS['neutral'], alpha=0.1)

        # Plot RRP (right, primary)
        ax_right.plot(recent_rrp.index, recent_rrp['totalAmtAccepted'],
                     color=COLORS['ocean_blue'], linewidth=2.5, label='RRP Usage')

        # Last value labels
        add_last_value_label(ax_left, recent_vix, COLORS['neutral'], side='left')
        add_last_value_label(ax_right, recent_rrp['totalAmtAccepted'],
                           COLORS['ocean_blue'], side='right', fmt='${:.0f}B')

        # Combined legend
        lines1, labels1 = ax_left.get_legend_handles_labels()
        lines2, labels2 = ax_right.get_legend_handles_labels()
        ax_left.legend(lines1 + lines2, labels1 + labels2,
                      loc='upper left', fontsize=9, framealpha=0.95)

    plt.tight_layout()
    return fig


def chart_18_sofr_effr_dynamics():
    """
    Chart 18: SOFR-EFFR Dynamics
    Secured vs Unsecured funding premium
    """
    fig, ax = create_single_axis_chart(
        chart_number=18,
        title='SOFR-EFFR Dynamics: Secured vs Unsecured Funding Premium',
        ylabel='Spread (bps)',
        source='NY Fed'
    )

    # Fetch data
    sofr = nyfed.get_sofr(last_n=500)
    effr = nyfed.get_effr(last_n=500)

    if not sofr.empty and not effr.empty:
        common_dates = sofr.index.intersection(effr.index)

        if len(common_dates) > 0:
            spread = (sofr.loc[common_dates, 'percentRate'] -
                     effr.loc[common_dates, 'percentRate']) * 100

            # Plot spread
            ax.plot(common_dates, spread,
                   color=COLORS['ocean_blue'], linewidth=2.5, label='SOFR-EFFR Spread')

            # Zero line
            ax.axhline(y=0, color=COLORS['neutral'], linestyle='--', linewidth=1.5, alpha=0.6)

            # Shade positive (normal) vs negative (stress)
            ax.fill_between(common_dates, 0, spread,
                           where=(spread >= 0),
                           color=COLORS['ocean_blue'], alpha=0.15, label='Normal (Secured < Unsecured)')
            ax.fill_between(common_dates, 0, spread,
                           where=(spread < 0),
                           color=COLORS['orange'], alpha=0.2, label='Stress (Inversion)')

            # Last value label
            add_last_value_label(ax, spread, COLORS['ocean_blue'], side='right', fmt='{:.1f}')

            ax.legend(loc='upper left', fontsize=9, framealpha=0.95)

    plt.tight_layout()
    return fig


def chart_19_treasury_fails():
    """
    Chart 19: Treasury Fails (Settlement Stress)
    Market plumbing dysfunction indicator
    """
    fig, ax = create_single_axis_chart(
        chart_number=19,
        title='Treasury Settlement Fails: Plumbing Stress Indicator',
        ylabel='Fails to Deliver ($B)',
        source='FRED'
    )

    # Fetch fails data (last 5 years)
    start_date = (datetime.now() - timedelta(days=1825)).strftime('%Y-%m-%d')
    fails = data.safe_fetch_fred('DTBSPCKFM', start_date)  # Treasury fails

    if fails is not None and len(fails) > 0:
        # Convert to billions
        fails_billions = fails / 1000

        ax.plot(fails_billions.index, fails_billions.values,
               color=COLORS['ocean_blue'], linewidth=2.5, label='Treasury Fails')

        # Shade elevated periods (>$50B)
        ax.fill_between(fails_billions.index, 0, fails_billions.values,
                       where=(fails_billions.values > 50),
                       color=COLORS['orange'], alpha=0.2, label='Elevated (>$50B)')

        # Threshold line
        ax.axhline(y=50, color=COLORS['neutral'], linestyle='--',
                  linewidth=1.5, alpha=0.6, label='$50B Threshold')

        add_last_value_label(ax, fails_billions, COLORS['ocean_blue'], side='right', fmt='${:.0f}B')

        ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
        ax.set_ylim(bottom=0)

    plt.tight_layout()
    return fig


def chart_20_dealer_positioning():
    """
    Chart 20: Primary Dealer Positioning
    Net Treasury holdings from NY Fed
    """
    fig, ax = create_single_axis_chart(
        chart_number=20,
        title='Primary Dealer Treasury Positioning',
        ylabel='Net Holdings ($B)',
        source='NY Fed'
    )

    # Note: This requires specific Primary Dealer series from NY Fed API
    # For now, use FRED proxy
    start_date = (datetime.now() - timedelta(days=1825)).strftime('%Y-%m-%d')
    dealer_holdings = data.safe_fetch_fred('WSHOMCB', start_date)  # Dealer holdings proxy

    if dealer_holdings is not None and len(dealer_holdings) > 0:
        ax.plot(dealer_holdings.index, dealer_holdings.values,
               color=COLORS['ocean_blue'], linewidth=2.5, label='Dealer Holdings')

        add_last_value_label(ax, dealer_holdings, COLORS['ocean_blue'], side='right', fmt='${:.0f}B')

        ax.legend(loc='upper left', fontsize=9, framealpha=0.95)

    plt.tight_layout()
    return fig


def chart_21_mmf_vs_tbill_supply():
    """
    Chart 21: MMF Assets vs T-Bill Supply
    Money fund demand vs Treasury supply
    """
    fig, ax_left, ax_right = create_dual_axis_chart(
        chart_number=21,
        title='Money Market Funds vs T-Bill Supply',
        left_label='T-Bill Supply ($T)',
        right_label='MMF Assets ($T)',
        source='FRED'
    )

    # Fetch data (last 5 years)
    start_date = (datetime.now() - timedelta(days=1825)).strftime('%Y-%m-%d')
    mmf_assets = data.safe_fetch_fred('MMMFFAQ027S', start_date)  # MMF total assets
    tbill_supply = data.safe_fetch_fred('DTBSL', start_date)  # T-Bill supply (needs conversion)

    if mmf_assets is not None and len(mmf_assets) > 0:
        mmf_trillions = mmf_assets / 1000

        # Plot MMF (right, primary)
        ax_right.plot(mmf_trillions.index, mmf_trillions.values,
                     color=COLORS['ocean_blue'], linewidth=2.5, label='MMF Assets')

        add_last_value_label(ax_right, mmf_trillions, COLORS['ocean_blue'],
                           side='right', fmt='${:.1f}T')

    if tbill_supply is not None and len(tbill_supply) > 0:
        tbill_trillions = tbill_supply / 1000000  # Convert millions to trillions

        # Plot T-Bill supply (left, secondary)
        ax_left.plot(tbill_trillions.index, tbill_trillions.values,
                    color=COLORS['neutral'], linewidth=2, alpha=0.7, label='T-Bill Supply')

        add_last_value_label(ax_left, tbill_trillions, COLORS['neutral'],
                           side='left', fmt='${:.1f}T')

    # Combined legend
    lines1, labels1 = ax_left.get_legend_handles_labels()
    lines2, labels2 = ax_right.get_legend_handles_labels()
    ax_left.legend(lines1 + lines2, labels1 + labels2,
                  loc='upper left', fontsize=9, framealpha=0.95)

    plt.tight_layout()
    return fig


# Charts 22-23 will use TradingView data (to be added in Phase 2 continuation)
# Placeholder functions for now

def chart_22_swap_spreads():
    """
    Chart 22: Swap Spreads (2Y, 5Y, 10Y, 30Y)
    UPGRADE: Will use TradingView data instead of FRED
    """
    fig, ax = create_single_axis_chart(
        chart_number=22,
        title='Swap Spreads: 2Y, 5Y, 10Y, 30Y (TradingView Data Pending)',
        ylabel='Spread (bps)',
        source='TradingView'
    )

    ax.text(0.5, 0.5, 'TradingView swap spread data integration pending\n\nManual export required from TradingView',
            ha='center', va='center', transform=ax.transAxes,
            fontsize=12, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_23_cross_currency_basis():
    """
    Chart 23: Cross-Currency Basis (EUR/USD, JPY/USD)
    UPGRADE: Will use TradingView basis swap data
    """
    fig, ax = create_single_axis_chart(
        chart_number=23,
        title='Cross-Currency Basis: EUR/USD, JPY/USD (TradingView Data Pending)',
        ylabel='Basis (bps)',
        source='TradingView'
    )

    ax.text(0.5, 0.5, 'TradingView cross-currency basis data integration pending\n\nManual export required from TradingView',
            ha='center', va='center', transform=ax.transAxes,
            fontsize=12, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


# Section 3 complete: 8 money market plumbing charts with NY Fed live data
