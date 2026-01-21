"""
Lighthouse Macro Chartbook - Full Integration
FRED + OFR + NY Fed + MacroMicro Charts
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as mpatches
from matplotlib.patches import Circle
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from datetime import datetime
import os
from data_sources import DataOrchestrator
import warnings
warnings.filterwarnings('ignore')

# Lighthouse Macro Brand Colors
COLORS = {
    'primary': '#003366',
    'secondary': '#0066CC',
    'accent': '#FF9900',
    'positive': '#00A86B',
    'negative': '#CC0000',
    'neutral': '#808080',
}

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 10,
    'axes.titlesize': 14,
    'axes.labelsize': 11,
    'figure.figsize': (11, 8.5),
    'figure.dpi': 150,
})

# Initialize data orchestrator
data_source = DataOrchestrator()


def add_branding(ax, chart_number):
    """Add consistent branding"""
    circle = Circle((0.02, 0.98), 0.015, transform=ax.transAxes,
                   facecolor=COLORS['secondary'], edgecolor='none', zorder=100)
    ax.add_patch(circle)
    ax.text(0.02, 0.98, str(chart_number),
            ha='center', va='center', fontsize=10, fontweight='bold',
            color='white', transform=ax.transAxes, zorder=101)

    ax.text(0.02, 0.02, 'Source: Federal Reserve Economic Data (FRED) | Lighthouse Macro',
            ha='left', va='bottom', fontsize=8, color=COLORS['neutral'],
            transform=ax.transAxes)

    ax.text(0.98, 0.02, f'Generated: {datetime.now().strftime("%Y-%m-%d")}',
            ha='right', va='bottom', fontsize=8, color=COLORS['neutral'],
            transform=ax.transAxes)


def create_image_chart(image_path, chart_num):
    """Create chart from PNG image"""
    fig, ax = plt.subplots(figsize=(11, 8.5))
    ax.axis('off')

    expanded_path = os.path.expanduser(image_path)
    if os.path.exists(expanded_path):
        img = mpimg.imread(expanded_path)
        ax.imshow(img)
        add_branding(ax, chart_num)
    else:
        ax.text(0.5, 0.5, f'Image not found: {os.path.basename(image_path)}',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=14, color=COLORS['negative'])

    plt.tight_layout()
    return fig


def create_placeholder(chart_num, title, subtitle):
    """Create placeholder for future charts"""
    fig, ax = plt.subplots(figsize=(11, 8.5))
    ax.axis('off')

    ax.text(0.5, 0.6, f'CHART {chart_num}', ha='center', va='center',
            fontsize=36, fontweight='bold', color=COLORS['primary'],
            transform=ax.transAxes)
    ax.text(0.5, 0.5, title, ha='center', va='center',
            fontsize=20, fontweight='bold', color=COLORS['secondary'],
            transform=ax.transAxes)
    ax.text(0.5, 0.42, subtitle, ha='center', va='center',
            fontsize=14, style='italic', color=COLORS['neutral'],
            transform=ax.transAxes)
    ax.text(0.5, 0.3, '[Full implementation with live data]',
            ha='center', va='center', fontsize=12, color=COLORS['neutral'],
            transform=ax.transAxes)

    add_branding(ax, chart_num)
    plt.tight_layout()
    return fig


# MacroMicro chart mappings
MACROMICRO_CHARTS = {
    18: '~/mm-chart-960x540.png',  # US Redbook Same-Store Retail Sales
    19: '~/mm-chart-960x540 (1).png',  # AI Infrastructure Inventory
    20: '~/mm-chart-960x540 (2).png',  # Mag 7 CapEx
    21: '~/mm-chart-960x540 (3).png',  # AI Software RPO
    22: '~/mm-chart-2025-11-21_Global Semi Equip Billings vs. Taiwan Exports -960x540.png',
    23: '~/mm-chart-2025-11-21_US - Contribution of IT Investment to Change in Real GDP-960x540.png',
    24: '~/mm-chart-2025-11-21_US - Share of Companies Currently or Planning to Use AI-960x540.png',
    25: '~/mm-chart-2025-11-21_World - Number of AI-Related Patents Granted (% of World Total)-960x540.png',
    26: '~/mm-chart-2025-11-21_Bitcoin - Average Mining Costs-960x540.png',
    27: '~/mm-chart-2025-11-21_World - Net AI Talent Migration per 10,000 LinkedIn Members-975x635.png',
}


def generate_chartbook():
    """Generate complete integrated chartbook"""

    print("="*70)
    print("LIGHTHOUSE MACRO - INTEGRATED CHARTBOOK")
    print("="*70)
    print()

    # Import chart functions from existing generator
    from generate_full_chartbook import (
        create_cover_page,
        chart_01_economic_cycle_scatter,
        chart_02_leading_indicators,
        chart_03_unemployment_inflation,
        chart_04_labor_market_heatmap,
        chart_05_ism_composite,
        chart_06_yield_curve,
        chart_07_yield_curve_spreads,
        chart_08_credit_impulse,
        chart_09_cross_asset_correlation,
        chart_10_inflation_components,
        chart_11_fed_balance_sheet,
        chart_12_rrp_vs_vix,
        chart_13_money_market_rates,
        chart_14_treasury_liquidity,
        chart_15_liquidity_composite,
        chart_16_jolts_indicators,
        chart_17_beveridge_curve,
    )

    # Import money market plumbing charts (OFR + NY Fed integration)
    from money_market_charts import (
        chart_33_money_market_dashboard,
        chart_34_swap_spreads,
        chart_35_bill_ois_spread,
        chart_36_basis_trade_capacity,
        chart_37_cross_currency_basis,
        chart_38_repo_market_depth,
        chart_39_sofr_effr_dynamics,
        chart_40_treasury_fails,
        chart_41_dealer_positioning,
        chart_42_mmf_composition,
    )

    # Import credit & risk charts
    from credit_risk_charts import (
        chart_43_high_yield_oas,
        chart_44_credit_cycle,
        chart_45_excess_bond_premium,
        chart_46_ig_hy_differential,
        chart_47_financial_stress_index,
        chart_48_recession_probability,
        chart_49_corporate_leverage,
        chart_50_earnings_revisions,
    )

    # Import TradingView single name charts
    from tradingview_charts import (
        chart_51_nvda,
        chart_52_asml,
        chart_53_msft,
        chart_54_tsm,
        chart_55_coin,
        chart_56_mstr,
        chart_57_mara,
        chart_58_jpm,
        chart_59_gs,
        chart_60_hyg,
    )

    charts = []

    # LAYER 1: MACRO DYNAMICS (1-17)
    print("Layer 1: Macro Dynamics (Charts 1-17)")
    charts.append(("1", chart_01_economic_cycle_scatter()))
    charts.append(("2", chart_02_leading_indicators()))
    charts.append(("3", chart_03_unemployment_inflation()))
    charts.append(("4", chart_04_labor_market_heatmap()))
    charts.append(("5", chart_05_ism_composite()))
    charts.append(("6", chart_06_yield_curve()))
    charts.append(("7", chart_07_yield_curve_spreads()))
    charts.append(("8", chart_08_credit_impulse()))
    charts.append(("9", chart_09_cross_asset_correlation()))
    charts.append(("10", chart_10_inflation_components()))
    charts.append(("11", chart_11_fed_balance_sheet()))
    charts.append(("12", chart_12_rrp_vs_vix()))
    charts.append(("13", chart_13_money_market_rates()))
    charts.append(("14", chart_14_treasury_liquidity()))
    charts.append(("15", chart_15_liquidity_composite()))
    charts.append(("16", chart_16_jolts_indicators()))
    charts.append(("17", chart_17_beveridge_curve()))

    # LAYER 2: AI & MANUFACTURING (18-27) - MacroMicro Charts
    print("\nLayer 2: AI & Manufacturing Transformation (Charts 18-27)")
    for chart_num in range(18, 28):
        if chart_num in MACROMICRO_CHARTS:
            print(f"  Chart {chart_num}: MacroMicro Chart")
            charts.append((str(chart_num), create_image_chart(MACROMICRO_CHARTS[chart_num], chart_num)))

    # LAYER 3: CRYPTO & DIGITAL ASSETS (28-32)
    print("\nLayer 3: Crypto & Digital Assets (Charts 28-32)")
    placeholders_crypto = [
        (28, "Stablecoin Supply vs Bitcoin", "Liquidity Dynamics"),
        (29, "Stablecoin Flows", "Composition Analysis"),
        (30, "Stablecoin vs MMF", "Cross-Market Dynamics"),
        (31, "Depegging Events", "Stability Metrics"),
        (32, "Crypto-Trad Correlation", "Market Integration"),
    ]
    for num, title, subtitle in placeholders_crypto:
        charts.append((str(num), create_placeholder(num, title, subtitle)))

    # LAYER 4: MONEY MARKET PLUMBING (33-42) - OFR + NY Fed Live Data
    print("\nLayer 4: Money Market Plumbing (Charts 33-42)")
    print("  Chart 33: Money Market Dashboard")
    charts.append(("33", chart_33_money_market_dashboard(data_source)))
    print("  Chart 34: Swap Spreads")
    charts.append(("34", chart_34_swap_spreads(data_source)))
    print("  Chart 35: Bill-OIS Spread")
    charts.append(("35", chart_35_bill_ois_spread(data_source)))
    print("  Chart 36: Basis Trade Capacity")
    charts.append(("36", chart_36_basis_trade_capacity(data_source)))
    print("  Chart 37: Cross-Currency Basis")
    charts.append(("37", chart_37_cross_currency_basis(data_source)))
    print("  Chart 38: Repo Market Depth")
    charts.append(("38", chart_38_repo_market_depth(data_source)))
    print("  Chart 39: SOFR-EFFR Dynamics")
    charts.append(("39", chart_39_sofr_effr_dynamics(data_source)))
    print("  Chart 40: Treasury Fails")
    charts.append(("40", chart_40_treasury_fails(data_source)))
    print("  Chart 41: Dealer Positioning")
    charts.append(("41", chart_41_dealer_positioning(data_source)))
    print("  Chart 42: MMF Composition")
    charts.append(("42", chart_42_mmf_composition(data_source)))

    # LAYER 5: CREDIT & RISK (43-50) - Live FRED Data
    print("\nLayer 5: Credit & Risk Indicators (Charts 43-50)")
    print("  Chart 43: High-Yield OAS")
    charts.append(("43", chart_43_high_yield_oas(data_source)))
    print("  Chart 44: Credit Cycle")
    charts.append(("44", chart_44_credit_cycle(data_source)))
    print("  Chart 45: Excess Bond Premium")
    charts.append(("45", chart_45_excess_bond_premium(data_source)))
    print("  Chart 46: IG-HY Differential")
    charts.append(("46", chart_46_ig_hy_differential(data_source)))
    print("  Chart 47: Financial Stress Index")
    charts.append(("47", chart_47_financial_stress_index(data_source)))
    print("  Chart 48: Recession Probability")
    charts.append(("48", chart_48_recession_probability(data_source)))
    print("  Chart 49: Corporate Leverage")
    charts.append(("49", chart_49_corporate_leverage(data_source)))
    print("  Chart 50: Earnings Revisions")
    charts.append(("50", chart_50_earnings_revisions(data_source)))

    # LAYER 6: TRADINGVIEW SINGLE NAMES (51-60)
    print("\nLayer 6: TradingView Single Name Analysis (Charts 51-60)")
    print("  Chart 51: NVDA - AI Infrastructure")
    charts.append(("51", chart_51_nvda()))
    print("  Chart 52: ASML - Semiconductor Equipment")
    charts.append(("52", chart_52_asml()))
    print("  Chart 53: MSFT - AI Software")
    charts.append(("53", chart_53_msft()))
    print("  Chart 54: TSM - Foundry Capacity")
    charts.append(("54", chart_54_tsm()))
    print("  Chart 55: COIN - Crypto Exchange")
    charts.append(("55", chart_55_coin()))
    print("  Chart 56: MSTR - Bitcoin Treasury")
    charts.append(("56", chart_56_mstr()))
    print("  Chart 57: MARA - Bitcoin Miner")
    charts.append(("57", chart_57_mara()))
    print("  Chart 58: JPM - Primary Dealer")
    charts.append(("58", chart_58_jpm()))
    print("  Chart 59: GS - Market Maker")
    charts.append(("59", chart_59_gs()))
    print("  Chart 60: HYG - Credit ETF")
    charts.append(("60", chart_60_hyg()))

    print(f"\n{'='*70}")
    print(f"Generated {len(charts)} charts total")
    print(f"{'='*70}\n")

    return charts


def main():
    """Main execution"""
    output_file = 'Lighthouse_Macro_Chartbook_Integrated.pdf'

    print(f"\nStarting integrated chartbook generation...")
    print(f"Output: {output_file}\n")

    # Generate cover
    from generate_full_chartbook import create_cover_page
    cover = create_cover_page()

    # Generate all charts
    all_charts = generate_chartbook()

    # Create PDF
    print("\nCompiling PDF...")
    with PdfPages(output_file) as pdf:
        pdf.savefig(cover, bbox_inches='tight')
        plt.close(cover)

        for chart_num, fig in all_charts:
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)

    print(f"\n{'='*70}")
    print(f"✓ SUCCESS! Chartbook generated: {output_file}")
    print(f"Total pages: {len(all_charts) + 1} (1 cover + {len(all_charts)} charts)")
    print(f"  • Layer 1: Macro Dynamics (Charts 1-17)")
    print(f"  • Layer 2: AI & Manufacturing (Charts 18-27)")
    print(f"  • Layer 3: Crypto & Digital Assets (Charts 28-32)")
    print(f"  • Layer 4: Money Market Plumbing (Charts 33-42)")
    print(f"  • Layer 5: Credit & Risk (Charts 43-50)")
    print(f"  • Layer 6: TradingView Single Names (Charts 51-60)")
    print(f"{'='*70}\n")

    return output_file


if __name__ == "__main__":
    main()
