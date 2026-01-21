"""
Lighthouse Macro - Section 4: Credit & Risk Charts (Charts 24-30)
Next-generation chartbook with corrected styling
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

# Initialize data orchestrator
data = DataOrchestrator()


def chart_24_high_yield_oas():
    """
    Chart 24: High-Yield OAS + BBB-AAA Differential
    Credit risk pricing across quality spectrum
    """
    fig, ax_left, ax_right = create_dual_axis_chart(
        chart_number=24,
        title='Credit Spreads: High-Yield OAS & Investment Grade Differential',
        left_label='BBB-AAA Spread (bps)',
        right_label='High-Yield OAS (bps)',
        source='FRED'
    )

    # Fetch data (last 5 years)
    start_date = (datetime.now() - timedelta(days=1825)).strftime('%Y-%m-%d')

    hy_oas = data.safe_fetch_fred('BAMLH0A0HYM2', start_date)  # HY OAS
    bbb_yield = data.safe_fetch_fred('BAMLC0A4CBBB', start_date)  # BBB OAS
    aaa_yield = data.safe_fetch_fred('BAMLC0A1CAAA', start_date)  # AAA OAS

    # Calculate BBB-AAA spread
    if bbb_yield is not None and aaa_yield is not None:
        ig_spread = (bbb_yield - aaa_yield) * 100  # Convert to bps

        # Plot IG spread (left, secondary)
        ax_left.plot(ig_spread.index, ig_spread.values,
                    color=COLORS['neutral'], linewidth=2, alpha=0.7, label='BBB-AAA Spread')
        ax_left.fill_between(ig_spread.index, 0, ig_spread.values,
                            color=COLORS['neutral'], alpha=0.1)

        add_last_value_label(ax_left, ig_spread, COLORS['neutral'], side='left', fmt='{:.0f}')

    # Plot HY OAS (right, primary)
    if hy_oas is not None and len(hy_oas) > 0:
        ax_right.plot(hy_oas.index, hy_oas.values,
                     color=COLORS['ocean_blue'], linewidth=2.5, label='High-Yield OAS')
        ax_right.fill_between(hy_oas.index, 0, hy_oas.values,
                             color=COLORS['ocean_blue'], alpha=0.1)

        # Stress threshold (>500 bps = elevated stress)
        ax_right.axhline(y=500, color=COLORS['orange'], linestyle='--',
                        linewidth=1.5, alpha=0.6, label='Stress Threshold')

        add_last_value_label(ax_right, hy_oas, COLORS['ocean_blue'], side='right', fmt='{:.0f}')

    # Combined legend
    lines1, labels1 = ax_left.get_legend_handles_labels()
    lines2, labels2 = ax_right.get_legend_handles_labels()
    ax_left.legend(lines1 + lines2, labels1 + labels2,
                  loc='upper left', fontsize=9, framealpha=0.95)

    plt.tight_layout()
    return fig


def chart_25_credit_cycle():
    """
    Chart 25: Credit Cycle - C&I Loan Growth
    Commercial & Industrial lending as leading indicator
    """
    fig, ax = create_single_axis_chart(
        chart_number=25,
        title='Credit Cycle: C&I Loan Growth (YoY)',
        ylabel='Growth Rate (% YoY)',
        source='FRED'
    )

    # Fetch data (last 10 years to show full cycle)
    start_date = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')
    ci_loans = data.safe_fetch_fred('BUSLOANS', start_date)  # C&I loans outstanding

    if ci_loans is not None and len(ci_loans) > 0:
        # Calculate YoY growth
        loan_growth = ci_loans.pct_change(52) * 100  # 52 weeks = 1 year

        # Plot growth rate
        ax.plot(loan_growth.index, loan_growth.values,
               color=COLORS['ocean_blue'], linewidth=2.5, label='C&I Loan Growth')

        # Zero line
        ax.axhline(y=0, color=COLORS['neutral'], linestyle='--', linewidth=1.5, alpha=0.6)

        # Shade expansion (positive) vs contraction (negative)
        ax.fill_between(loan_growth.index, 0, loan_growth.values,
                       where=(loan_growth.values > 0),
                       color=COLORS['ocean_blue'], alpha=0.15, label='Credit Expansion')
        ax.fill_between(loan_growth.index, 0, loan_growth.values,
                       where=(loan_growth.values < 0),
                       color=COLORS['orange'], alpha=0.2, label='Credit Contraction')

        add_last_value_label(ax, loan_growth, COLORS['ocean_blue'], side='right', fmt='{:.1f}%')

        ax.legend(loc='upper left', fontsize=9, framealpha=0.95)

    else:
        ax.text(0.5, 0.5, 'C&I loan data temporarily unavailable',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=14, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_26_excess_bond_premium():
    """
    Chart 26: Excess Bond Premium vs Fed Funds
    Policy transmission to credit markets
    """
    fig, ax_left, ax_right = create_dual_axis_chart(
        chart_number=26,
        title='Excess Bond Premium vs Fed Funds: Policy Transmission',
        left_label='Fed Funds Rate (%)',
        right_label='Excess Bond Premium (bps)',
        source='FRED'
    )

    # Fetch data (last 5 years)
    start_date = (datetime.now() - timedelta(days=1825)).strftime('%Y-%m-%d')

    ebp = data.safe_fetch_fred('BAMLH0A0HYM2EY', start_date)  # Excess bond premium
    fed_funds = data.safe_fetch_fred('FEDFUNDS', start_date)  # Fed funds rate

    # Plot Fed Funds (left, secondary)
    if fed_funds is not None and len(fed_funds) > 0:
        ax_left.plot(fed_funds.index, fed_funds.values,
                    color=COLORS['neutral'], linewidth=2, alpha=0.7, label='Fed Funds Rate')

        add_last_value_label(ax_left, fed_funds, COLORS['neutral'], side='left', fmt='{:.2f}%')

    # Plot EBP (right, primary)
    if ebp is not None and len(ebp) > 0:
        ax_right.plot(ebp.index, ebp.values,
                     color=COLORS['ocean_blue'], linewidth=2.5, label='Excess Bond Premium')

        # Threshold for elevated risk premium
        ax_right.axhline(y=100, color=COLORS['orange'], linestyle='--',
                        linewidth=1.5, alpha=0.6, label='Elevated Premium')

        add_last_value_label(ax_right, ebp, COLORS['ocean_blue'], side='right', fmt='{:.0f}')

    # Combined legend
    lines1, labels1 = ax_left.get_legend_handles_labels()
    lines2, labels2 = ax_right.get_legend_handles_labels()
    ax_left.legend(lines1 + lines2, labels1 + labels2,
                  loc='upper left', fontsize=9, framealpha=0.95)

    plt.tight_layout()
    return fig


def chart_27_corporate_leverage():
    """
    Chart 27: Corporate Leverage + Debt Service Coverage
    Corporate debt sustainability
    """
    fig, ax = create_single_axis_chart(
        chart_number=27,
        title='Corporate Leverage: Nonfinancial Debt to GDP',
        ylabel='Debt/GDP Ratio (%)',
        source='FRED'
    )

    # Fetch data (last 10 years)
    start_date = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')

    corp_debt = data.safe_fetch_fred('BCNSDODNS', start_date)  # Nonfinancial corporate debt
    gdp = data.safe_fetch_fred('GDP', start_date)  # GDP

    if corp_debt is not None and gdp is not None:
        # Align quarterly data
        df = pd.DataFrame({'debt': corp_debt, 'gdp': gdp}).dropna()

        if len(df) > 0:
            # Calculate debt-to-GDP ratio
            leverage_ratio = (df['debt'] / df['gdp']) * 100

            # Plot
            ax.plot(leverage_ratio.index, leverage_ratio.values,
                   color=COLORS['ocean_blue'], linewidth=2.5, label='Corp Debt/GDP')
            ax.fill_between(leverage_ratio.index, 0, leverage_ratio.values,
                           color=COLORS['ocean_blue'], alpha=0.1)

            # Historical average
            avg_leverage = leverage_ratio.mean()
            ax.axhline(y=avg_leverage, color=COLORS['neutral'], linestyle='--',
                      linewidth=1.5, alpha=0.6, label=f'Avg: {avg_leverage:.1f}%')

            add_last_value_label(ax, leverage_ratio, COLORS['ocean_blue'], side='right', fmt='{:.1f}%')

            ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
            ax.set_ylim(bottom=0)

    else:
        ax.text(0.5, 0.5, 'Corporate leverage data temporarily unavailable',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=14, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_28_credit_impulse():
    """
    Chart 28: Credit Impulse
    Change in credit growth (leading indicator)
    """
    fig, ax = create_single_axis_chart(
        chart_number=28,
        title='Credit Impulse: Bank Lending Acceleration/Deceleration',
        ylabel='Credit Impulse (% of GDP)',
        source='FRED'
    )

    # Fetch data
    start_date = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')

    total_credit = data.safe_fetch_fred('TOTBKCR', start_date)  # Total bank credit
    gdp = data.safe_fetch_fred('GDP', start_date)

    if total_credit is not None and gdp is not None:
        # Resample credit to quarterly (same as GDP)
        credit_quarterly = total_credit.resample('Q').last()

        # Align data
        df = pd.DataFrame({'credit': credit_quarterly, 'gdp': gdp}).dropna()

        if len(df) > 4:
            # Calculate credit growth (YoY change)
            credit_growth = df['credit'].pct_change(4)  # 4 quarters

            # Credit impulse = change in credit growth
            # As % of GDP: d(credit growth)/GDP
            credit_impulse = credit_growth.diff() * 100

            # Plot
            ax.plot(credit_impulse.index, credit_impulse.values,
                   color=COLORS['ocean_blue'], linewidth=2.5, label='Credit Impulse')

            # Zero line
            ax.axhline(y=0, color=COLORS['neutral'], linestyle='--', linewidth=1.5, alpha=0.6)

            # Shade positive (accelerating) vs negative (decelerating)
            ax.fill_between(credit_impulse.index, 0, credit_impulse.values,
                           where=(credit_impulse.values > 0),
                           color=COLORS['ocean_blue'], alpha=0.15, label='Accelerating')
            ax.fill_between(credit_impulse.index, 0, credit_impulse.values,
                           where=(credit_impulse.values < 0),
                           color=COLORS['orange'], alpha=0.2, label='Decelerating')

            add_last_value_label(ax, credit_impulse, COLORS['ocean_blue'], side='right', fmt='{:.2f}')

            ax.legend(loc='upper left', fontsize=9, framealpha=0.95)

    else:
        ax.text(0.5, 0.5, 'Credit impulse data temporarily unavailable',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=14, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_29_move_index():
    """
    Chart 29: MOVE Index (Bond Market Volatility)
    UPGRADE: Will use TradingView CBOE:MOVE data
    """
    fig, ax = create_single_axis_chart(
        chart_number=29,
        title='MOVE Index: Bond Market Volatility (TradingView Data Pending)',
        ylabel='MOVE Index',
        source='TradingView - CBOE:MOVE'
    )

    ax.text(0.5, 0.5, 'TradingView MOVE Index data integration pending\n\n' +
            'CBOE:MOVE - Bond market volatility indicator\n' +
            'Manual export required from TradingView\n\n' +
            'This data is NOT available in FRED',
            ha='center', va='center', transform=ax.transAxes,
            fontsize=11, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_30_cdx_indices():
    """
    Chart 30: CDX IG/HY Indices
    UPGRADE: Will use TradingView CDX data for real-time credit
    """
    fig, ax = create_single_axis_chart(
        chart_number=30,
        title='CDX IG/HY Indices: Real-Time Credit (TradingView Data Pending)',
        ylabel='Spread (bps)',
        source='TradingView'
    )

    ax.text(0.5, 0.5, 'TradingView CDX Indices data integration pending\n\n' +
            'CDX Investment Grade (IG) and High-Yield (HY) indices\n' +
            'Manual export required from TradingView\n\n' +
            'Provides better real-time credit data than FRED',
            ha='center', va='center', transform=ax.transAxes,
            fontsize=11, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


# Section 4 complete: 7 credit & risk charts with corrected Lighthouse styling
# Charts 29-30 are placeholders for TradingView data integration
