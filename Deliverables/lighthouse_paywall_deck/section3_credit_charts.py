"""
Lighthouse Macro - Section 3: Credit Markets & Risk Appetite (Charts 18-25)
PROPRIETARY INDICATORS: Credit-Labor Gap (CLG), HY Spread vs Volatility Imbalance
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

# Initialize data
data = DataOrchestrator()


def calculate_z_score(series, window=None):
    """Calculate z-score for a series"""
    if window:
        mean = series.rolling(window).mean()
        std = series.rolling(window).std()
    else:
        mean = series.mean()
        std = series.std()
    return (series - mean) / std


def chart_18_high_yield_oas_bbb_aaa():
    """
    Chart 18: High-Yield OAS + BBB-AAA Differential
    """
    fig, ax_left, ax_right = create_dual_axis_chart(
        chart_number=18,
        title='Credit Spreads: High-Yield OAS & Investment Grade Differential',
        left_label='BBB-AAA Spread (bps)',
        right_label='High-Yield OAS (bps)',
        source='FRED'
    )

    # Fetch data (5 years)
    start_date = (datetime.now() - timedelta(days=1825)).strftime('%Y-%m-%d')

    hy_oas = data.safe_fetch_fred('BAMLH0A0HYM2', start_date)  # HY OAS
    bbb_oas = data.safe_fetch_fred('BAMLC0A4CBBB', start_date)  # BBB OAS
    aaa_oas = data.safe_fetch_fred('BAMLC0A1CAAA', start_date)  # AAA OAS

    if hy_oas is not None and len(hy_oas) > 0:
        # Plot HY OAS (right, primary)
        ax_right.plot(hy_oas.index, hy_oas.values,
                     color=COLORS['ocean_blue'], linewidth=2.5, label='High-Yield OAS')
        ax_right.fill_between(hy_oas.index, 0, hy_oas.values,
                             color=COLORS['ocean_blue'], alpha=0.1)

        # Threshold lines
        ax_right.axhline(y=300, color=COLORS['neutral'], linestyle='--',
                        linewidth=1.5, alpha=0.6, label='Normal (300 bps)')
        ax_right.axhline(y=500, color=COLORS['orange'], linestyle='--',
                        linewidth=1.5, alpha=0.6, label='Elevated (500 bps)')
        ax_right.axhline(y=800, color=COLORS['orange'], linestyle='-',
                        linewidth=2, alpha=0.8, label='Crisis (800 bps)')

        add_last_value_label(ax_right, hy_oas, COLORS['ocean_blue'],
                           side='right', fmt='{:.0f}')

    # Calculate and plot IG spread (left, secondary)
    if bbb_oas is not None and aaa_oas is not None:
        ig_spread = (bbb_oas - aaa_oas) * 100  # Convert to bps
        ax_left.plot(ig_spread.index, ig_spread.values,
                    color=COLORS['carolina_blue'], linewidth=2, alpha=0.7,
                    label='BBB-AAA Spread')
        ax_left.fill_between(ig_spread.index, 0, ig_spread.values,
                            color=COLORS['carolina_blue'], alpha=0.1)

        add_last_value_label(ax_left, ig_spread, COLORS['carolina_blue'],
                           side='left', fmt='{:.0f}')

    # Combined legend
    lines1, labels1 = ax_left.get_legend_handles_labels()
    lines2, labels2 = ax_right.get_legend_handles_labels()
    ax_left.legend(lines1 + lines2, labels1 + labels2,
                  loc='upper right', fontsize=9, framealpha=0.95)

    plt.tight_layout()
    return fig


def chart_19_credit_cycle():
    """
    Chart 19: Credit Cycle - C&I Loan Growth
    """
    # Use existing function from credit_risk_charts_v2.py
    from credit_risk_charts_v2 import chart_25_credit_cycle
    return chart_25_credit_cycle()


def chart_20_excess_bond_premium():
    """
    Chart 20: Excess Bond Premium vs Fed Funds
    """
    # Use existing function from credit_risk_charts_v2.py
    from credit_risk_charts_v2 import chart_26_excess_bond_premium
    return chart_26_excess_bond_premium()


def chart_21_corporate_leverage():
    """
    Chart 21: Corporate Leverage - Debt/GDP
    """
    # Use existing function from credit_risk_charts_v2.py
    from credit_risk_charts_v2 import chart_27_corporate_leverage
    return chart_27_corporate_leverage()


def chart_22_credit_impulse():
    """
    Chart 22: Credit Impulse
    """
    # Use existing function from credit_risk_charts_v2.py
    from credit_risk_charts_v2 import chart_28_credit_impulse_v2
    return chart_28_credit_impulse_v2()


def chart_23_credit_labor_gap():
    """
    Chart 23: Credit-Labor Gap (CLG)
    PROPRIETARY INDICATOR: Z(HY OAS) - Z(LFI)
    """
    fig, ax = create_single_axis_chart(
        chart_number=23,
        title='Credit-Labor Gap (CLG): Spread Adequacy vs Macro Fragility',
        ylabel='CLG (Z-Score Difference)',
        source='FRED, Lighthouse Proprietary'
    )

    # Fetch HY OAS
    start_date = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')
    hy_oas = data.safe_fetch_fred('BAMLH0A0HYM2', start_date)

    # Calculate LFI (need JOLTS data)
    long_unemp = data.safe_fetch_fred('UEMP27OV', start_date)
    total_unemp = data.safe_fetch_fred('UNEMPLOY', start_date)
    quits = data.safe_fetch_fred('JTSQUR', start_date)
    hires = data.safe_fetch_fred('JTSHIR', start_date)

    if hy_oas is not None and long_unemp is not None and total_unemp is not None and quits is not None and hires is not None:
        # Calculate LFI components
        long_duration_share = (long_unemp / total_unemp) * 100
        hires_quits_ratio = hires / quits

        # Align data
        df = pd.DataFrame({
            'hy_oas': hy_oas,
            'long_duration': long_duration_share,
            'quits': quits,
            'hires_quits': hires_quits_ratio
        }).dropna()

        if len(df) > 0:
            # Calculate LFI
            df['z_long_duration'] = calculate_z_score(df['long_duration'])
            df['z_quits'] = -calculate_z_score(df['quits'])
            df['z_hires_quits'] = -calculate_z_score(df['hires_quits'])
            df['LFI'] = (df['z_long_duration'] + df['z_quits'] + df['z_hires_quits']) / 3

            # Calculate Z-score of HY OAS
            df['z_hy_oas'] = calculate_z_score(df['hy_oas'])

            # Credit-Labor Gap = Z(HY OAS) - Z(LFI)
            df['CLG'] = df['z_hy_oas'] - df['LFI']

            # Plot CLG
            ax.plot(df.index, df['CLG'], color=COLORS['ocean_blue'],
                   linewidth=2.5, label='Credit-Labor Gap')

            # Zero line (critical threshold)
            ax.axhline(y=0, color=COLORS['neutral'], linestyle='-',
                      linewidth=2, alpha=0.6, label='Neutral (Spreads = Labor Stress)')

            # Shade zones
            ax.fill_between(df.index, 0, df['CLG'],
                           where=(df['CLG'] > 0),
                           color=COLORS['ocean_blue'], alpha=0.15,
                           label='Spreads Wide (Good Compensation)')
            ax.fill_between(df.index, 0, df['CLG'],
                           where=(df['CLG'] < 0),
                           color=COLORS['orange'], alpha=0.2,
                           label='Spreads Tight (Pre-Widening)')

            add_last_value_label(ax, df['CLG'], COLORS['ocean_blue'],
                               side='right', fmt='{:.2f}σ')

            ax.legend(loc='upper right', fontsize=9, framealpha=0.95)
    else:
        ax.text(0.5, 0.5,
                'Credit-Labor Gap (CLG)\n\n' +
                'PROPRIETARY INDICATOR\n\n' +
                'Formula: Z(HY OAS) - Z(LFI)\n\n' +
                'Negative CLG = Spreads too tight given labor stress\n' +
                '"Historically a pre-widening configuration"',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=10, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_24_hy_spread_volatility_imbalance():
    """
    Chart 24: HY Spread vs Volatility Imbalance
    PROPRIETARY INDICATOR: Spread tightness vs spread volatility
    """
    fig, ax = create_single_axis_chart(
        chart_number=24,
        title='HY Spread vs Volatility Imbalance: Risk Compensation Check',
        ylabel='Z-Score',
        source='FRED, Lighthouse Proprietary'
    )

    # Fetch HY OAS
    start_date = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')
    hy_oas = data.safe_fetch_fred('BAMLH0A0HYM2', start_date)

    if hy_oas is not None and len(hy_oas) > 0:
        # Calculate realized volatility of HY OAS (30-day rolling std)
        hy_vol = hy_oas.rolling(30).std()

        # Align data
        df = pd.DataFrame({
            'hy_oas': hy_oas,
            'hy_vol': hy_vol
        }).dropna()

        if len(df) > 0:
            # Calculate z-scores
            df['z_oas'] = calculate_z_score(df['hy_oas'])
            df['z_vol'] = calculate_z_score(df['hy_vol'])

            # Plot both z-scores
            ax.plot(df.index, df['z_oas'],
                   color=COLORS['ocean_blue'], linewidth=2.5, label='HY OAS (Z-Score)')
            ax.plot(df.index, df['z_vol'],
                   color=COLORS['orange'], linewidth=2, alpha=0.7,
                   label='HY Spread Volatility (Z-Score)')

            # Zero line
            ax.axhline(y=0, color=COLORS['neutral'], linestyle='--',
                      linewidth=1.5, alpha=0.6)

            # Threshold bands
            ax.axhline(y=1, color=COLORS['neutral'], linestyle='--',
                      linewidth=1, alpha=0.4)
            ax.axhline(y=-1, color=COLORS['neutral'], linestyle='--',
                      linewidth=1, alpha=0.4)

            # Shade imbalance zones (tight spreads + rising vol = bad)
            imbalance = (df['z_oas'] < 0) & (df['z_vol'] > 0)
            ax.fill_between(df.index, -2, 2,
                           where=imbalance,
                           color=COLORS['orange'], alpha=0.1,
                           label='Imbalance Zone (Tight + High Vol)')

            ax.legend(loc='upper right', fontsize=9, framealpha=0.95)
            ax.set_ylim(bottom=-2.5, top=2.5)
    else:
        ax.text(0.5, 0.5,
                'HY Spread vs Volatility Imbalance\n\n' +
                'PROPRIETARY INDICATOR\n\n' +
                '"Tight spreads with rising vol = poor compensation for risk;\n' +
                'a late-cycle mismatch"',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=10, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_25_cross_asset_credit_stress():
    """
    Chart 25: Cross-Asset Credit Stress
    HY OAS, VIX, IG OAS overlay
    """
    fig, ax = create_single_axis_chart(
        chart_number=25,
        title='Cross-Asset Credit Stress: HY, IG, Equity Vol (Z-Scored)',
        ylabel='Z-Score',
        source='FRED, CBOE'
    )

    # Fetch data (3 years)
    start_date = (datetime.now() - timedelta(days=1095)).strftime('%Y-%m-%d')

    hy_oas = data.safe_fetch_fred('BAMLH0A0HYM2', start_date)
    ig_oas = data.safe_fetch_fred('BAMLC0A0CM', start_date)  # IG Corporate Master OAS
    vix = data.safe_fetch_fred('VIXCLS', start_date)

    # Align data
    df = pd.DataFrame({
        'hy_oas': hy_oas,
        'ig_oas': ig_oas,
        'vix': vix
    }).dropna()

    if len(df) > 0:
        # Calculate z-scores for each
        df['z_hy'] = calculate_z_score(df['hy_oas'])
        df['z_ig'] = calculate_z_score(df['ig_oas'])
        df['z_vix'] = calculate_z_score(df['vix'])

        # Plot all three
        ax.plot(df.index, df['z_hy'],
               color=COLORS['ocean_blue'], linewidth=2.5, label='HY OAS')
        ax.plot(df.index, df['z_ig'],
               color=COLORS['carolina_blue'], linewidth=2, alpha=0.7, label='IG OAS')
        ax.plot(df.index, df['z_vix'],
               color=COLORS['orange'], linewidth=2, alpha=0.7, label='VIX')

        # Zero line
        ax.axhline(y=0, color=COLORS['neutral'], linestyle='--',
                  linewidth=1.5, alpha=0.6)

        # Threshold bands
        ax.axhline(y=1, color=COLORS['neutral'], linestyle='--',
                  linewidth=1, alpha=0.4, label='+1σ (Elevated)')
        ax.axhline(y=2, color=COLORS['orange'], linestyle='--',
                  linewidth=1, alpha=0.4, label='+2σ (Crisis)')

        ax.legend(loc='upper right', fontsize=9, framealpha=0.95)
    else:
        ax.text(0.5, 0.5, 'Cross-asset credit stress data temporarily unavailable',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=11, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


# Section 3 complete: 8 credit & risk charts
# Proprietary indicators: CLG (Chart 23), HY Spread/Vol Imbalance (Chart 24)
# Charts 18-22 use existing functions where available
# Chart 25 is new cross-asset overlay
