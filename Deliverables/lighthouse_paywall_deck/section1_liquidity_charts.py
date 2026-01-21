"""
Lighthouse Macro - Section 1: Liquidity & Funding Stress (Charts 1-10)
PROPRIETARY INDICATORS: LCI, YFS, Repo Dispersion
"""

import matplotlib.pyplot as plt
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
from data_sources import DataOrchestrator
from nyfed_api_reference import NYFedAPI

# Initialize data sources
data = DataOrchestrator()
nyfed = NYFedAPI(cache_hours=24)


def calculate_z_score(series, window=None):
    """Calculate z-score for a series"""
    if window:
        mean = series.rolling(window).mean()
        std = series.rolling(window).std()
    else:
        mean = series.mean()
        std = series.std()
    return (series - mean) / std


def chart_01_liquidity_cushion_index():
    """
    Chart 1: Liquidity Cushion Index (LCI)
    Z-score average of ON RRP/GDP + Bank Reserves/GDP
    """
    fig, ax = create_single_axis_chart(
        chart_number=1,
        title='Liquidity Cushion Index (LCI): System Shock-Absorption Capacity',
        ylabel='LCI (Z-Score)',
        source='NY Fed, FRED'
    )

    # Fetch data (5 years)
    start_date = (datetime.now() - timedelta(days=1825)).strftime('%Y-%m-%d')

    # Get RRP
    rrp = nyfed.get_rrp_operations()

    # Get GDP (quarterly)
    gdp = data.safe_fetch_fred('GDP', start_date)

    # Get bank reserves
    reserves = data.safe_fetch_fred('TOTRESNS', start_date)  # Total reserves

    if rrp is not None and gdp is not None and reserves is not None:
        # Resample RRP and reserves to quarterly (match GDP frequency)
        rrp_quarterly = rrp['totalAmtAccepted'].resample('Q').mean() / 1000  # Convert to billions
        reserves_quarterly = reserves.resample('Q').mean()

        # Align data
        df = pd.DataFrame({
            'rrp': rrp_quarterly,
            'reserves': reserves_quarterly,
            'gdp': gdp
        }).dropna()

        if len(df) > 0:
            # Calculate ratios
            df['rrp_gdp'] = (df['rrp'] / df['gdp']) * 100
            df['reserves_gdp'] = (df['reserves'] / df['gdp']) * 100

            # Z-score each component
            df['rrp_z'] = calculate_z_score(df['rrp_gdp'])
            df['reserves_z'] = calculate_z_score(df['reserves_gdp'])

            # LCI = average of both z-scores
            df['LCI'] = (df['rrp_z'] + df['reserves_z']) / 2

            # Plot LCI
            ax.plot(df.index, df['LCI'], color=COLORS['ocean_blue'],
                   linewidth=2.5, label='Liquidity Cushion Index')

            # Threshold bands
            ax.axhline(y=1, color=COLORS['neutral'], linestyle='--',
                      linewidth=1.5, alpha=0.6, label='+1σ (High Cushion)')
            ax.axhline(y=0, color=COLORS['neutral'], linestyle='-',
                      linewidth=1.5, alpha=0.6, label='Neutral')
            ax.axhline(y=-1, color=COLORS['orange'], linestyle='--',
                      linewidth=1.5, alpha=0.6, label='-1σ (Low Cushion)')

            # Shade vulnerable zone
            ax.fill_between(df.index, -1, df['LCI'],
                           where=(df['LCI'] < -1),
                           color=COLORS['orange'], alpha=0.2, label='Vulnerable Zone')

            # Shade resilient zone
            ax.fill_between(df.index, 1, df['LCI'],
                           where=(df['LCI'] > 1),
                           color=COLORS['ocean_blue'], alpha=0.1, label='Resilient Zone')

            add_last_value_label(ax, df['LCI'], COLORS['ocean_blue'],
                               side='right', fmt='{:.2f}σ')

            ax.legend(loc='upper right', fontsize=9, framealpha=0.95)
    else:
        ax.text(0.5, 0.5, 'LCI data temporarily unavailable\n\nRequires: RRP, Reserves, GDP',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=11, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_02_yield_funding_stress():
    """
    Chart 2: Yield-Funding Stress (YFS) Composite
    Curve inversion + plumbing metrics
    """
    fig, ax = create_single_axis_chart(
        chart_number=2,
        title='Yield-Funding Stress (YFS): Financial Plumbing Health',
        ylabel='YFS Composite (Z-Score)',
        source='NY Fed, FRED'
    )

    # Fetch data (3 years)
    start_date = (datetime.now() - timedelta(days=1095)).strftime('%Y-%m-%d')

    # Get yield curve spreads
    t10y = data.safe_fetch_fred('DGS10', start_date)
    t2y = data.safe_fetch_fred('DGS2', start_date)
    t3m = data.safe_fetch_fred('DGS3MO', start_date)

    # Get money market rates
    sofr = nyfed.get_sofr()
    effr = nyfed.get_effr()

    if t10y is not None and t2y is not None and sofr is not None and effr is not None:
        # Calculate spreads
        spread_10y2y = t10y - t2y
        spread_10y3m = t10y - t3m if t3m is not None else None

        # Resample SOFR/EFFR to daily
        sofr_daily = sofr['percentRate'].resample('D').last()
        effr_daily = effr['percentRate'].resample('D').last()

        # Calculate SOFR-EFFR spread
        sofr_effr = sofr_daily - effr_daily

        # Align all data
        df = pd.DataFrame({
            'spread_10y2y': spread_10y2y,
            'sofr_effr': sofr_effr
        }).dropna()

        if spread_10y3m is not None:
            df['spread_10y3m'] = spread_10y3m

        if len(df) > 0:
            # Z-score each component (invert yield spreads - negative = stress)
            df['z_10y2y'] = -calculate_z_score(df['spread_10y2y'])  # Inverted
            df['z_sofr_effr'] = calculate_z_score(df['sofr_effr'])  # Positive spread = stress

            components = ['z_10y2y', 'z_sofr_effr']
            if 'spread_10y3m' in df.columns:
                df['z_10y3m'] = -calculate_z_score(df['spread_10y3m'])
                components.append('z_10y3m')

            # YFS = average of components
            df['YFS'] = df[components].mean(axis=1)

            # Plot YFS
            ax.plot(df.index, df['YFS'], color=COLORS['ocean_blue'],
                   linewidth=2.5, label='YFS Composite')

            # Threshold bands
            ax.axhline(y=1, color=COLORS['orange'], linestyle='--',
                      linewidth=1.5, alpha=0.6, label='+1σ (Elevated Stress)')
            ax.axhline(y=0, color=COLORS['neutral'], linestyle='-',
                      linewidth=1.5, alpha=0.6, label='Neutral')

            # Shade stress zone
            ax.fill_between(df.index, 1, df['YFS'],
                           where=(df['YFS'] > 1),
                           color=COLORS['orange'], alpha=0.2, label='Stress Zone')

            add_last_value_label(ax, df['YFS'], COLORS['ocean_blue'],
                               side='right', fmt='{:.2f}σ')

            ax.legend(loc='upper right', fontsize=9, framealpha=0.95)
    else:
        ax.text(0.5, 0.5, 'YFS data temporarily unavailable\n\nRequires: Yield curve, SOFR, EFFR',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=11, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_03_repo_rate_dispersion():
    """
    Chart 3: Repo Rate Dispersion Index
    99th - 1st percentile BGCR spread
    NOTE: BGCR percentile data not available via standard APIs
    This is a placeholder showing the methodology
    """
    fig, ax = create_single_axis_chart(
        chart_number=3,
        title='Repo Rate Dispersion Index: Funding Fragmentation',
        ylabel='BGCR Dispersion (bps)',
        source='NY Fed (Requires BGCR Percentile Data)'
    )

    # BGCR percentile data not available via public API
    # Would need to scrape NY Fed BGCR distribution data

    ax.text(0.5, 0.5,
            'Repo Rate Dispersion Index\n\n' +
            'Methodology:\n' +
            '99th percentile BGCR - 1st percentile BGCR\n\n' +
            'Data Source: NY Fed BGCR Distribution\n' +
            '(Requires manual data collection or specialized API)\n\n' +
            'Low Dispersion (<20 bps) = Healthy funding\n' +
            'High Dispersion (>50 bps) = Fragmentation, pre-stress',
            ha='center', va='center', transform=ax.transAxes,
            fontsize=10, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_04_fed_balance_sheet_rrp():
    """
    Chart 4: Fed Balance Sheet + RRP Overlay
    Stacked area showing composition
    """
    fig, ax = create_single_axis_chart(
        chart_number=4,
        title='Fed Balance Sheet Components: Assets, RRP, Reserves',
        ylabel='Trillions ($)',
        source='NY Fed, FRED'
    )

    # Fetch data (10 years to show full QE/QT cycle)
    start_date = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')

    # Fed balance sheet
    fed_assets = data.safe_fetch_fred('WALCL', start_date)  # Fed total assets

    # RRP
    rrp = nyfed.get_rrp_operations()

    # Bank reserves
    reserves = data.safe_fetch_fred('TOTRESNS', start_date)

    if fed_assets is not None:
        # Convert to trillions
        fed_assets_t = fed_assets / 1000

        # Plot Fed assets
        ax.plot(fed_assets_t.index, fed_assets_t.values,
               color=COLORS['ocean_blue'], linewidth=2.5, label='Fed Total Assets')
        ax.fill_between(fed_assets_t.index, 0, fed_assets_t.values,
                       color=COLORS['ocean_blue'], alpha=0.1)

        if rrp is not None and len(rrp) > 0:
            # Resample RRP to weekly (match Fed assets frequency)
            rrp_weekly = rrp['totalAmtAccepted'].resample('W').mean() / 1000000  # To trillions

            # Plot RRP
            ax.plot(rrp_weekly.index, rrp_weekly.values,
                   color=COLORS['orange'], linewidth=2, label='ON RRP Usage')

        if reserves is not None and len(reserves) > 0:
            reserves_t = reserves / 1000

            # Plot reserves
            ax.plot(reserves_t.index, reserves_t.values,
                   color=COLORS['carolina_blue'], linewidth=2,
                   alpha=0.7, label='Bank Reserves')

        # Mark key events
        qe_end = pd.Timestamp('2022-03-01')
        qt_start = pd.Timestamp('2022-06-01')

        ax.axvline(x=qe_end, color=COLORS['neutral'], linestyle='--',
                  linewidth=1, alpha=0.5)
        ax.text(qe_end, ax.get_ylim()[1] * 0.95, 'QE Ends',
               fontsize=8, ha='right', color=COLORS['neutral'])

        add_last_value_label(ax, fed_assets_t, COLORS['ocean_blue'],
                           side='right', fmt='${:.1f}T')

        ax.legend(loc='upper right', fontsize=9, framealpha=0.95)
        ax.set_ylim(bottom=0)
    else:
        ax.text(0.5, 0.5, 'Fed balance sheet data temporarily unavailable',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=11, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_05_sofr_effr_obfr_dynamics():
    """
    Chart 5: SOFR-EFFR-OBFR Dynamics
    Three money market rates with spread overlay
    """
    fig, ax_left, ax_right = create_dual_axis_chart(
        chart_number=5,
        title='Money Market Rates: SOFR, EFFR, OBFR Dynamics',
        left_label='Rate (%)',
        right_label='SOFR-EFFR Spread (bps)',
        source='NY Fed'
    )

    # Get rates from NY Fed
    sofr = nyfed.get_sofr()
    effr = nyfed.get_effr()
    obfr = nyfed.get_obfr()

    if sofr is not None and effr is not None:
        # Plot rates (left axis)
        ax_left.plot(sofr.index, sofr['percentRate'],
                    color=COLORS['ocean_blue'], linewidth=2, label='SOFR', alpha=0.8)
        ax_left.plot(effr.index, effr['percentRate'],
                    color=COLORS['carolina_blue'], linewidth=2, label='EFFR', alpha=0.8)

        if obfr is not None and len(obfr) > 0:
            ax_left.plot(obfr.index, obfr['percentRate'],
                        color=COLORS['neutral'], linewidth=1.5, label='OBFR',
                        alpha=0.6, linestyle='--')

        # Calculate and plot spread (right axis)
        spread = (sofr['percentRate'] - effr['percentRate']) * 100  # Convert to bps
        ax_right.plot(spread.index, spread.values,
                     color=COLORS['orange'], linewidth=2.5, label='SOFR-EFFR Spread')

        # Stress threshold
        ax_right.axhline(y=15, color=COLORS['orange'], linestyle='--',
                        linewidth=1.5, alpha=0.6, label='Stress Threshold (15 bps)')
        ax_right.axhline(y=0, color=COLORS['neutral'], linestyle='-',
                        linewidth=1, alpha=0.4)

        # Combined legend
        lines1, labels1 = ax_left.get_legend_handles_labels()
        lines2, labels2 = ax_right.get_legend_handles_labels()
        ax_left.legend(lines1 + lines2, labels1 + labels2,
                      loc='upper right', fontsize=9, framealpha=0.95)
    else:
        ax_left.text(0.5, 0.5, 'Money market rate data temporarily unavailable',
                    ha='center', va='center', transform=ax_left.transAxes,
                    fontsize=11, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_06_money_market_dashboard():
    """
    Chart 6: Money Market Dashboard (4-Panel)
    SOFR term structure, EFFR vs target, RRP, Reserves
    """
    fig = plt.figure(figsize=(11, 8.5))

    # Create 2x2 grid
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3,
                          left=0.1, right=0.95, top=0.88, bottom=0.15)

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 0])
    ax4 = fig.add_subplot(gs[1, 1])

    # Apply no gridlines to all
    enforce_no_gridlines([ax1, ax2, ax3, ax4])

    # Get data
    sofr = nyfed.get_sofr()
    effr = nyfed.get_effr()
    rrp = nyfed.get_rrp_operations()
    reserves = data.safe_fetch_fred('TOTRESNS', '2020-01-01')

    # Panel A: SOFR (just overnight, term structure data not in standard API)
    if sofr is not None:
        recent_sofr = sofr.tail(250)  # Last year
        ax1.plot(recent_sofr.index, recent_sofr['percentRate'],
                color=COLORS['ocean_blue'], linewidth=2)
        ax1.set_title('SOFR Overnight', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Rate (%)', fontsize=9)

    # Panel B: EFFR vs Fed Target Range
    if effr is not None:
        recent_effr = effr.tail(250)
        ax2.plot(recent_effr.index, recent_effr['percentRate'],
                color=COLORS['carolina_blue'], linewidth=2, label='EFFR')

        # Fed target range (current: 5.25-5.50%)
        current_target_upper = 5.50
        current_target_lower = 5.25
        ax2.axhline(y=current_target_upper, color=COLORS['neutral'],
                   linestyle='--', linewidth=1, alpha=0.5, label='Target Range')
        ax2.axhline(y=current_target_lower, color=COLORS['neutral'],
                   linestyle='--', linewidth=1, alpha=0.5)
        ax2.fill_between(recent_effr.index, current_target_lower, current_target_upper,
                        color=COLORS['neutral'], alpha=0.1)

        ax2.set_title('EFFR vs Fed Target', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Rate (%)', fontsize=9)
        ax2.legend(loc='upper right', fontsize=8)

    # Panel C: RRP Usage
    if rrp is not None:
        recent_rrp = rrp.tail(250)
        ax3.plot(recent_rrp.index, recent_rrp['totalAmtAccepted'] / 1000,
                color=COLORS['orange'], linewidth=2)
        ax3.fill_between(recent_rrp.index, 0, recent_rrp['totalAmtAccepted'] / 1000,
                        color=COLORS['orange'], alpha=0.2)
        ax3.set_title('ON RRP Usage', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Billions ($)', fontsize=9)
        ax3.set_ylim(bottom=0)

    # Panel D: Bank Reserves
    if reserves is not None:
        recent_reserves = reserves.tail(250)
        ax4.plot(recent_reserves.index, recent_reserves.values,
                color=COLORS['carolina_blue'], linewidth=2)
        ax4.fill_between(recent_reserves.index, 0, recent_reserves.values,
                        color=COLORS['carolina_blue'], alpha=0.2)
        ax4.set_title('Bank Reserves', fontsize=11, fontweight='bold')
        ax4.set_ylabel('Billions ($)', fontsize=9)
        ax4.set_ylim(bottom=0)

    # Overall title and branding
    fig.text(0.5, 0.95, 'Money Market Dashboard: Fed Operational Framework',
            ha='center', va='center', fontsize=14, fontweight='bold',
            color=COLORS['ocean_blue'])

    # Chart number badge
    from matplotlib.patches import Circle
    circle = Circle((0.02, 0.98), 0.015, transform=fig.transFigure,
                   facecolor=COLORS['ocean_blue'], edgecolor='none', zorder=100)
    fig.patches.append(circle)
    fig.text(0.02, 0.98, '6',
            ha='center', va='center', fontsize=10, fontweight='bold',
            color='white', transform=fig.transFigure, zorder=101)

    # LIGHTHOUSE MACRO
    fig.text(0.045, 0.98, 'LIGHTHOUSE MACRO',
            ha='left', va='center', fontsize=9, fontweight='bold',
            color=COLORS['ocean_blue'], transform=fig.transFigure)

    # Source
    fig.text(0.02, 0.02, 'Source: NY Fed, FRED',
            ha='left', va='bottom', fontsize=7, color=COLORS['neutral'], style='italic')

    # Watermark
    fig.text(0.98, 0.02, 'MACRO, ILLUMINATED.',
            ha='right', va='bottom', fontsize=8, fontweight='bold',
            color=COLORS['ocean_blue'], alpha=0.6)

    return fig


def chart_07_treasury_liquidity():
    """
    Chart 7: Treasury Liquidity Metrics
    Placeholder - requires specialized data
    """
    fig, ax = create_single_axis_chart(
        chart_number=7,
        title='Treasury Market Liquidity: Bid-Ask Spreads & Market Depth',
        ylabel='Liquidity Score',
        source='FRED, FINRA TRACE'
    )

    ax.text(0.5, 0.5,
            'Treasury Liquidity Metrics\n\n' +
            'Components:\n' +
            '- Bid-ask spreads (tightness)\n' +
            '- Market depth (order book)\n' +
            '- Price impact (resilience)\n\n' +
            'Requires: FINRA TRACE data or Bloomberg access\n\n' +
            'Proxy available: Treasury trading volume from FRED',
            ha='center', va='center', transform=ax.transAxes,
            fontsize=10, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_08_swap_spreads():
    """
    Chart 8: Swap Spreads (2Y, 5Y, 10Y, 30Y)
    """
    fig, ax = create_single_axis_chart(
        chart_number=8,
        title='Swap Spreads: Interbank Credit Health',
        ylabel='Spread (bps)',
        source='FRED'
    )

    # Fetch data
    start_date = (datetime.now() - timedelta(days=1825)).strftime('%Y-%m-%d')

    # Swap spreads (if available in FRED)
    # Note: These series may not exist, using placeholder approach
    swap_2y = data.safe_fetch_fred('DISCONTINUED', start_date)  # Placeholder

    ax.text(0.5, 0.5,
            'Swap Spreads Across Curve\n\n' +
            'Methodology: Swap Rate - Treasury Yield\n\n' +
            'Normal: Positive spread (20-40 bps)\n' +
            'Stress: Widening spreads (>60 bps)\n' +
            'Anomaly: Negative spreads (post-QE distortion)\n\n' +
            'Requires: Bloomberg or swap market data\n' +
            'FRED coverage limited for swap spreads',
            ha='center', va='center', transform=ax.transAxes,
            fontsize=10, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_09_cross_currency_basis():
    """
    Chart 9: Cross-Currency Basis (EUR/USD, JPY/USD)
    """
    fig, ax = create_dual_axis_chart(
        chart_number=9,
        title='Cross-Currency Basis Swaps: Dollar Funding Stress',
        left_label='EUR/USD 3M Basis (bps)',
        right_label='JPY/USD 3M Basis (bps)',
        source='Bloomberg, BIS'
    )

    ax_left.text(0.5, 0.5,
                'Cross-Currency Basis Swaps\n\n' +
                'EUR/USD Basis (primary)\n' +
                'JPY/USD Basis (secondary)\n\n' +
                'Negative basis = Premium to borrow USD\n' +
                'Crisis indicator: < -50 bps\n\n' +
                'Requires: Bloomberg or BIS data\n' +
                'Not available in standard FRED feeds',
                ha='center', va='center', transform=ax_left.transAxes,
                fontsize=10, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_10_dealer_positioning():
    """
    Chart 10: Primary Dealer Treasury Positions
    """
    fig, ax = create_single_axis_chart(
        chart_number=10,
        title='Primary Dealer Net Treasury Positions: Market-Making Capacity',
        ylabel='Net Position ($B)',
        source='NY Fed (FR 2004)'
    )

    # Dealer positioning data from NY Fed FR 2004 survey
    # Not available via standard FRED API

    ax.text(0.5, 0.5,
            'Primary Dealer Positioning\n\n' +
            'Net Long: Dealers warehousing supply (vulnerable to sell-off)\n' +
            'Net Short: Facilitating client demand (potential short squeeze)\n' +
            'Neutral: Efficient market functioning\n\n' +
            'Data Source: NY Fed FR 2004 Survey\n' +
            '(Requires manual collection or specialized scraping)\n\n' +
            'Available breakdowns: Bills, Notes, Bonds',
            ha='center', va='center', transform=ax.transAxes,
            fontsize=10, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


# Section 1 complete: 10 liquidity & funding stress charts
# Charts 1-2 are fully functional (LCI, YFS)
# Charts 3, 7-10 are methodology placeholders (require specialized data sources)
# Charts 4-6 are functional with available data
