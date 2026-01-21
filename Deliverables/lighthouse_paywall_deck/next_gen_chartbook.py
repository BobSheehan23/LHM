"""
Lighthouse Macro - Next Generation Chartbook
42 Charts - Best Quality Only - Corrected Styling

SECTIONS:
1. Macro Regime (Charts 1-10)
2. Labor Markets (Charts 11-13) [14-15 reserved for Phase 4 extension]
3. Money Market Plumbing (Charts 16-23)
4. Credit & Risk (Charts 24-30)
5. Crypto & Digital Assets (Charts 31-35)
6. AI Infrastructure (Charts 36-42)

Total: 42 charts + 6 section dividers = 48-page PDF
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from pathlib import Path

# Import chart modules
from macro_regime_charts import (
    chart_01_economic_cycle_scatter,
    chart_02_phillips_curve,
    chart_03_ism_composite,
    chart_04_yield_curve,
    chart_05_yield_curve_spreads,
    chart_06_inflation_components,
    chart_07_fed_balance_sheet,
    chart_08_cross_asset_correlation,
    chart_09_financial_stress_index,
    chart_10_recession_probability
)

from labor_market_charts import (
    chart_11_labor_market_heatmap,
    chart_12_jolts_indicators,
    chart_13_beveridge_curve
)

from money_market_charts_v2 import (
    chart_16_money_market_dashboard,
    chart_17_rrp_vs_vix,
    chart_18_sofr_effr_dynamics,
    chart_19_treasury_fails,
    chart_20_dealer_positioning,
    chart_21_mmf_vs_tbill_supply,
    chart_22_swap_spreads,
    chart_23_cross_currency_basis
)

from credit_risk_charts_v2 import (
    chart_24_high_yield_oas,
    chart_25_credit_cycle,
    chart_26_excess_bond_premium,
    chart_27_corporate_leverage,
    chart_28_credit_impulse,
    chart_29_move_index,
    chart_30_cdx_indices
)

from crypto_charts import (
    chart_31_bitcoin_stablecoin_overlay,
    chart_32_stablecoin_composition,
    chart_33_stablecoin_vs_mmf,
    chart_34_btc_realized_vol,
    chart_35_btc_correlation
)

from ai_infrastructure_charts import (
    chart_36_mag7_capex,
    chart_37_ai_software_rpo,
    chart_38_semi_equipment_exports,
    chart_39_it_investment_gdp,
    chart_40_nvda,
    chart_41_msft,
    chart_42_tsm
)

from lighthouse_style import create_section_page


def generate_next_gen_chartbook():
    """
    Generate complete 42-chart next-generation chartbook
    """
    timestamp = datetime.now().strftime('%Y-%m-%d')
    output_dir = Path(__file__).parent / "chartbooks"
    output_dir.mkdir(exist_ok=True)

    pdf_path = output_dir / f"Lighthouse_Macro_NextGen_Chartbook_42_Charts_{timestamp}.pdf"

    print("=" * 80)
    print("GENERATING NEXT-GENERATION LIGHTHOUSE MACRO CHARTBOOK")
    print("=" * 80)
    print(f"Output: {pdf_path}")
    print()

    with PdfPages(pdf_path) as pdf:

        # === SECTION 1: MACRO REGIME (Charts 1-10) ===
        print("\n[SECTION 1] Macro Regime - Charts 1-10")

        section_fig = create_section_page(
            section_number=1,
            section_title='Macro Regime',
            section_description='Core macroeconomic indicators: growth, inflation, yields, Fed policy,\nfinancial stress, and recession probability',
            charts_range='Charts 1-10'
        )
        pdf.savefig(section_fig, dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Section divider page")

        chart_functions_s1 = [
            chart_01_economic_cycle_scatter,
            chart_02_phillips_curve,
            chart_03_ism_composite,
            chart_04_yield_curve,
            chart_05_yield_curve_spreads,
            chart_06_inflation_components,
            chart_07_fed_balance_sheet,
            chart_08_cross_asset_correlation,
            chart_09_financial_stress_index,
            chart_10_recession_probability
        ]

        for i, chart_func in enumerate(chart_functions_s1, start=1):
            try:
                print(f"  [{i:2d}/10] Generating {chart_func.__name__}...")
                fig = chart_func()
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)
            except Exception as e:
                print(f"  ✗ Error in Chart {i}: {e}")

        # === SECTION 2: LABOR MARKETS (Charts 11-13) ===
        print("\n[SECTION 2] Labor Markets - Charts 11-13")

        section_fig = create_section_page(
            section_number=2,
            section_title='Labor Markets',
            section_description='Labor market health: multi-metric heatmap, JOLTS indicators,\nand Beveridge curve efficiency analysis',
            charts_range='Charts 11-13'
        )
        pdf.savefig(section_fig, dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Section divider page")

        chart_functions_s2 = [
            chart_11_labor_market_heatmap,
            chart_12_jolts_indicators,
            chart_13_beveridge_curve
        ]

        for i, chart_func in enumerate(chart_functions_s2, start=11):
            try:
                print(f"  [{i:2d}/13] Generating {chart_func.__name__}...")
                fig = chart_func()
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)
            except Exception as e:
                print(f"  ✗ Error in Chart {i}: {e}")

        # === SECTION 3: MONEY MARKET PLUMBING (Charts 16-23) ===
        print("\n[SECTION 3] Money Market Plumbing - Charts 16-23")

        section_fig = create_section_page(
            section_number=3,
            section_title='Money Market Plumbing',
            section_description='Fed operations, funding markets, RRP dynamics, dealer positioning,\nand cross-market stress transmission',
            charts_range='Charts 16-23'
        )
        pdf.savefig(section_fig, dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Section divider page")

        chart_functions_s3 = [
            chart_16_money_market_dashboard,
            chart_17_rrp_vs_vix,
            chart_18_sofr_effr_dynamics,
            chart_19_treasury_fails,
            chart_20_dealer_positioning,
            chart_21_mmf_vs_tbill_supply,
            chart_22_swap_spreads,
            chart_23_cross_currency_basis
        ]

        for i, chart_func in enumerate(chart_functions_s3, start=16):
            try:
                print(f"  [{i:2d}/23] Generating {chart_func.__name__}...")
                fig = chart_func()
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)
            except Exception as e:
                print(f"  ✗ Error in Chart {i}: {e}")

        # === SECTION 4: CREDIT & RISK (Charts 24-30) ===
        print("\n[SECTION 4] Credit & Risk - Charts 24-30")

        section_fig = create_section_page(
            section_number=4,
            section_title='Credit & Risk',
            section_description='High-yield spreads, credit cycle, corporate leverage, bond volatility,\nand real-time credit derivatives',
            charts_range='Charts 24-30'
        )
        pdf.savefig(section_fig, dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Section divider page")

        chart_functions_s4 = [
            chart_24_high_yield_oas,
            chart_25_credit_cycle,
            chart_26_excess_bond_premium,
            chart_27_corporate_leverage,
            chart_28_credit_impulse,
            chart_29_move_index,
            chart_30_cdx_indices
        ]

        for i, chart_func in enumerate(chart_functions_s4, start=24):
            try:
                print(f"  [{i:2d}/30] Generating {chart_func.__name__}...")
                fig = chart_func()
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)
            except Exception as e:
                print(f"  ✗ Error in Chart {i}: {e}")

        # === SECTION 5: CRYPTO & DIGITAL ASSETS (Charts 31-35) ===
        print("\n[SECTION 5] Crypto & Digital Assets - Charts 31-35")

        section_fig = create_section_page(
            section_number=5,
            section_title='Crypto & Digital Assets',
            section_description='Bitcoin dynamics, stablecoin supply, crypto-traditional correlations,\nand digital dollar competition with money market funds',
            charts_range='Charts 31-35'
        )
        pdf.savefig(section_fig, dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Section divider page")

        chart_functions_s5 = [
            chart_31_bitcoin_stablecoin_overlay,
            chart_32_stablecoin_composition,
            chart_33_stablecoin_vs_mmf,
            chart_34_btc_realized_vol,
            chart_35_btc_correlation
        ]

        for i, chart_func in enumerate(chart_functions_s5, start=31):
            try:
                print(f"  [{i:2d}/35] Generating {chart_func.__name__}...")
                fig = chart_func()
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)
            except Exception as e:
                print(f"  ✗ Error in Chart {i}: {e}")

        # === SECTION 6: AI INFRASTRUCTURE (Charts 36-42) ===
        print("\n[SECTION 6] AI Infrastructure - Charts 36-42")

        section_fig = create_section_page(
            section_number=6,
            section_title='AI Infrastructure',
            section_description='Mag 7 CapEx, AI software growth, semiconductor supply chain,\nand single-name technical analysis (NVDA, MSFT, TSM)',
            charts_range='Charts 36-42'
        )
        pdf.savefig(section_fig, dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Section divider page")

        chart_functions_s6 = [
            chart_36_mag7_capex,
            chart_37_ai_software_rpo,
            chart_38_semi_equipment_exports,
            chart_39_it_investment_gdp,
            chart_40_nvda,
            chart_41_msft,
            chart_42_tsm
        ]

        for i, chart_func in enumerate(chart_functions_s6, start=36):
            try:
                print(f"  [{i:2d}/42] Generating {chart_func.__name__}...")
                fig = chart_func()
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)
            except Exception as e:
                print(f"  ✗ Error in Chart {i}: {e}")

    print("\n" + "=" * 80)
    print(f"✓ Chartbook generation complete!")
    print(f"✓ Output: {pdf_path}")
    print(f"✓ Total pages: 42 charts + 6 section dividers = 48 pages")
    print("=" * 80)

    return pdf_path


if __name__ == "__main__":
    pdf_path = generate_next_gen_chartbook()
    print(f"\n✓ Next-Generation Lighthouse Macro Chartbook ready: {pdf_path}")
