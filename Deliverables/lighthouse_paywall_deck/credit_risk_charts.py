"""
Credit & Risk Charts - Live Data Implementation
Charts 43-50: FRED Credit Market Data
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np
from datetime import datetime
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
    ax.text(0.02, 0.02, 'Source: FRED',
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


def add_last_value_label(ax, series, color, y_position=None):
    """Add last value label on right axis"""
    if len(series) > 0:
        last_val = series.iloc[-1]
        if y_position is None:
            y_position = last_val

        ax.text(1.01, y_position, f'{last_val:.1f}',
                transform=ax.get_yaxis_transform(),
                ha='left', va='center', fontsize=9,
                color=color, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                         edgecolor=color, linewidth=1.5))


def chart_43_high_yield_oas(data_source):
    """Chart 43: High-Yield OAS - Credit Spread Decomposition"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8.5), height_ratios=[2, 1])

    credit_data = data_source.get_credit_data()

    # High Yield Spread
    if 'HY_Spread' in credit_data and len(credit_data['HY_Spread']) > 0:
        credit_data['HY_Spread'].plot(ax=ax1, color=COLORS['negative'], linewidth=2.5, label='HY OAS')

        # Shade stress zones
        ax1.axhline(500, color=COLORS['accent'], linestyle='--', linewidth=1, alpha=0.7)
        ax1.axhline(1000, color=COLORS['negative'], linestyle='--', linewidth=1, alpha=0.7)
        ax1.fill_between(credit_data['HY_Spread'].index, 500, credit_data['HY_Spread'].values,
                        where=(credit_data['HY_Spread'].values > 500), alpha=0.2, color=COLORS['accent'])

        add_last_value_label(ax1, credit_data['HY_Spread'], COLORS['negative'])

    ax1.set_title('High-Yield Option-Adjusted Spread', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Basis Points', fontsize=11)
    ax1.legend(['HY OAS', 'Elevated (500bp)', 'Crisis (1000bp)'], loc='upper left', fontsize=9, framealpha=0.95)

    # BBB vs AAA spread differential
    if 'BBB_Spread' in credit_data and 'AAA_Spread' in credit_data:
        if len(credit_data['BBB_Spread']) > 0 and len(credit_data['AAA_Spread']) > 0:
            combined = pd.DataFrame({
                'BBB': credit_data['BBB_Spread'],
                'AAA': credit_data['AAA_Spread']
            }).dropna()

            if len(combined) > 0:
                diff = combined['BBB'] - combined['AAA']
                diff.plot(ax=ax2, color=COLORS['secondary'], linewidth=2, label='BBB-AAA Diff')
                add_last_value_label(ax2, diff, COLORS['secondary'])

    ax2.set_title('BBB-AAA Spread Differential', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Basis Points', fontsize=10)
    ax2.set_xlabel('Date', fontsize=11)
    ax2.legend(loc='upper left', fontsize=9, framealpha=0.95)

    add_branding(ax1, 43)
    plt.tight_layout()
    return fig


def chart_44_credit_cycle(data_source):
    """Chart 44: Credit Cycle - Positioning Analysis"""
    fig, ax = plt.subplots(figsize=(11, 8.5))

    credit_data = data_source.get_credit_data()

    # Commercial & Industrial Loans YoY growth
    if 'Commercial_Loans' in credit_data and len(credit_data['Commercial_Loans']) > 0:
        ci_growth = credit_data['Commercial_Loans'].pct_change(12) * 100
        ci_growth.plot(ax=ax, color=COLORS['primary'], linewidth=2.5, label='C&I Loan Growth (YoY%)')

        ax.axhline(0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
        ax.fill_between(ci_growth.index, 0, ci_growth.values,
                       where=(ci_growth.values > 0), alpha=0.3, color=COLORS['positive'])
        ax.fill_between(ci_growth.index, 0, ci_growth.values,
                       where=(ci_growth.values < 0), alpha=0.3, color=COLORS['negative'])

        add_last_value_label(ax, ci_growth, COLORS['primary'])

    ax.set_title('Credit Cycle: C&I Loan Growth', fontsize=14, fontweight='bold')
    ax.set_ylabel('YoY % Change', fontsize=11)
    ax.set_xlabel('Date', fontsize=11)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.95)

    add_branding(ax, 44)
    plt.tight_layout()
    return fig


def chart_45_excess_bond_premium(data_source):
    """Chart 45: Excess Bond Premium vs Fed Funds"""
    fig, ax1 = plt.subplots(figsize=(11, 8.5))

    # HY Spread as credit risk premium proxy
    hy_spread = data_source.safe_fetch_fred('BAMLH0A0HYM2', name='HY Spread')
    fed_funds = data_source.safe_fetch_fred('DFF', name='Fed Funds')

    # Fed Funds on LEFT (secondary)
    if len(fed_funds) > 0:
        ax1.plot(fed_funds.index, fed_funds.values, color=COLORS['neutral'],
                linewidth=1.5, alpha=0.7, label='Fed Funds (L)')
        add_last_value_label(ax1, fed_funds, COLORS['neutral'])

    ax1.set_ylabel('Fed Funds Rate (%)', fontsize=10, color=COLORS['neutral'])
    ax1.tick_params(axis='y', labelcolor=COLORS['neutral'])

    # HY Spread on RIGHT (primary)
    ax2 = ax1.twinx()
    if len(hy_spread) > 0:
        ax2.plot(hy_spread.index, hy_spread.values, color=COLORS['negative'],
                linewidth=2.5, label='Credit Premium (R)')
        add_last_value_label(ax2, hy_spread, COLORS['negative'])

    ax2.set_ylabel('HY Spread (bp)', fontsize=11, color=COLORS['negative'], fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=COLORS['negative'])

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9, framealpha=0.95)

    ax1.set_title('Credit Risk Premium vs Fed Policy', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Date', fontsize=11)

    add_branding(ax1, 45)
    plt.tight_layout()
    return fig


def chart_46_ig_hy_differential(data_source):
    """Chart 46: IG-HY Differential - Risk Mispricing"""
    fig, ax = plt.subplots(figsize=(11, 8.5))

    credit_data = data_source.get_credit_data()

    # Plot both IG and HY
    if 'BBB_Spread' in credit_data and len(credit_data['BBB_Spread']) > 0:
        credit_data['BBB_Spread'].plot(ax=ax, label='IG (BBB)',
                                      color=COLORS['secondary'], linewidth=2)
        add_last_value_label(ax, credit_data['BBB_Spread'], COLORS['secondary'])

    if 'HY_Spread' in credit_data and len(credit_data['HY_Spread']) > 0:
        credit_data['HY_Spread'].plot(ax=ax, label='High Yield',
                                     color=COLORS['negative'], linewidth=2)
        add_last_value_label(ax, credit_data['HY_Spread'], COLORS['negative'])

    ax.set_title('Investment Grade vs High Yield Spreads', fontsize=14, fontweight='bold')
    ax.set_ylabel('Basis Points', fontsize=11)
    ax.set_xlabel('Date', fontsize=11)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.95)

    add_branding(ax, 46)
    plt.tight_layout()
    return fig


def chart_47_financial_stress_index(data_source):
    """Chart 47: Financial Stress Index - Composite Indicator"""
    fig, ax = plt.subplots(figsize=(11, 8.5))

    # St. Louis Fed Financial Stress Index
    fsi = data_source.safe_fetch_fred('STLFSI2', name='Financial Stress Index')

    if len(fsi) > 0:
        fsi.plot(ax=ax, color=COLORS['primary'], linewidth=2.5, label='Financial Stress Index')

        ax.axhline(0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
        ax.axhline(1, color=COLORS['accent'], linestyle='--', linewidth=1, alpha=0.7)

        # Shade stress periods
        ax.fill_between(fsi.index, 0, fsi.values,
                       where=(fsi.values > 0), alpha=0.3, color=COLORS['negative'])
        ax.fill_between(fsi.index, 0, fsi.values,
                       where=(fsi.values < 0), alpha=0.3, color=COLORS['positive'])

        add_last_value_label(ax, fsi, COLORS['primary'])

    ax.set_title('St. Louis Fed Financial Stress Index', fontsize=14, fontweight='bold')
    ax.set_ylabel('Index Value', fontsize=11)
    ax.set_xlabel('Date', fontsize=11)
    ax.legend(['FSI', 'Zero Line', 'Elevated (>1)'], loc='upper left', fontsize=9, framealpha=0.95)

    add_branding(ax, 47)
    plt.tight_layout()
    return fig


def chart_48_recession_probability(data_source):
    """Chart 48: Recession Probability - Model Estimates"""
    fig, ax = plt.subplots(figsize=(11, 8.5))

    # Smoothed US Recession Probabilities
    recession_prob = data_source.safe_fetch_fred('RECPROUSM156N', name='Recession Probability')

    if len(recession_prob) > 0:
        recession_prob.plot(ax=ax, color=COLORS['negative'], linewidth=2.5, label='Recession Probability')

        ax.axhline(50, color=COLORS['accent'], linestyle='--', linewidth=1, alpha=0.7)
        ax.fill_between(recession_prob.index, 0, recession_prob.values,
                       where=(recession_prob.values > 50), alpha=0.3, color=COLORS['negative'])

        add_last_value_label(ax, recession_prob, COLORS['negative'])

    ax.set_title('Recession Probability Model', fontsize=14, fontweight='bold')
    ax.set_ylabel('Probability (%)', fontsize=11)
    ax.set_xlabel('Date', fontsize=11)
    ax.set_ylim(0, 100)
    ax.legend(['Recession Probability', '50% Threshold'], loc='upper left', fontsize=9, framealpha=0.95)

    add_branding(ax, 48)
    plt.tight_layout()
    return fig


def chart_49_corporate_leverage(data_source):
    """Chart 49: Corporate Leverage - Distribution by Rating"""
    fig, ax = plt.subplots(figsize=(11, 8.5))

    # Nonfinancial Corporate Business Debt
    corp_debt = data_source.safe_fetch_fred('BCNSDODNS', name='Corporate Debt')
    corp_profits = data_source.safe_fetch_fred('CP', name='Corporate Profits')

    if len(corp_debt) > 0 and len(corp_profits) > 0:
        combined = pd.DataFrame({
            'Debt': corp_debt,
            'Profits': corp_profits
        }).dropna()

        if len(combined) > 0:
            leverage = combined['Debt'] / combined['Profits']
            leverage.plot(ax=ax, color=COLORS['primary'], linewidth=2.5, label='Debt/Profits')
            add_last_value_label(ax, leverage, COLORS['primary'])

    ax.set_title('Corporate Leverage (Debt to Profits)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Ratio', fontsize=11)
    ax.set_xlabel('Date', fontsize=11)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.95)

    add_branding(ax, 49)
    plt.tight_layout()
    return fig


def chart_50_earnings_revisions(data_source):
    """Chart 50: Earnings Revisions - Forward Outlook"""
    fig, ax = plt.subplots(figsize=(11, 8.5))

    # Use Industrial Production as earnings proxy
    ind_prod = data_source.safe_fetch_fred('INDPRO', name='Industrial Production')

    if len(ind_prod) > 0:
        ind_growth = ind_prod.pct_change(12) * 100
        ind_growth.plot(ax=ax, color=COLORS['secondary'], linewidth=2.5, label='Industrial Production Growth')

        ax.axhline(0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
        ax.fill_between(ind_growth.index, 0, ind_growth.values,
                       where=(ind_growth.values > 0), alpha=0.3, color=COLORS['positive'])
        ax.fill_between(ind_growth.index, 0, ind_growth.values,
                       where=(ind_growth.values < 0), alpha=0.3, color=COLORS['negative'])

        add_last_value_label(ax, ind_growth, COLORS['secondary'])

    ax.set_title('Industrial Production Growth (Earnings Proxy)', fontsize=14, fontweight='bold')
    ax.set_ylabel('YoY % Change', fontsize=11)
    ax.set_xlabel('Date', fontsize=11)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.95)

    add_branding(ax, 50)
    plt.tight_layout()
    return fig
