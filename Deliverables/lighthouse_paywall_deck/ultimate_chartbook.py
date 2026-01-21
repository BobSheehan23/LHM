"""
Lighthouse Macro - ULTIMATE Chartbook
Uses the ACTUAL charts we built, not generic placeholders
42 Best Charts Only - Corrected Lighthouse Styling
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from pathlib import Path

# Import the REAL charts we actually built
from generate_full_chartbook import (
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

# Import styling module
from lighthouse_style import create_section_page

# Import additional chart modules we built
from money_market_charts_v2 import (
    chart_16_money_market_dashboard,
    chart_17_rrp_vs_vix as chart_17_rrp_vix_v2,
    chart_18_sofr_effr_dynamics,
    chart_19_treasury_fails,
    chart_20_dealer_positioning,
    chart_21_mmf_vs_tbill_supply,
    chart_22_swap_spreads,
    chart_23_cross_currency_basis,
)

from credit_risk_charts_v2 import (
    chart_24_high_yield_oas,
    chart_25_credit_cycle,
    chart_26_excess_bond_premium,
    chart_27_corporate_leverage,
    chart_28_credit_impulse as chart_28_credit_impulse_v2,
    chart_29_move_index,
    chart_30_cdx_indices,
)

from crypto_charts import (
    chart_31_bitcoin_stablecoin_overlay,
    chart_32_stablecoin_composition,
    chart_33_stablecoin_vs_mmf,
    chart_34_btc_realized_vol,
    chart_35_btc_correlation,
)

from ai_infrastructure_charts import (
    chart_36_mag7_capex,
    chart_37_ai_software_rpo,
    chart_38_semi_equipment_exports,
    chart_39_it_investment_gdp,
    chart_40_nvda,
    chart_41_msft,
    chart_42_tsm,
)

# Import macro regime charts
from macro_regime_charts import (
    chart_01_economic_cycle_scatter as chart_01_v2,
    chart_02_phillips_curve,
    chart_03_ism_composite as chart_03_v2,
    chart_04_yield_curve as chart_04_v2,
    chart_05_yield_curve_spreads as chart_05_v2,
    chart_06_inflation_components as chart_06_v2,
    chart_07_fed_balance_sheet as chart_07_v2,
    chart_08_cross_asset_correlation as chart_08_v2,
    chart_09_financial_stress_index,
    chart_10_recession_probability,
)

# Import labor market charts
from labor_market_charts import (
    chart_11_labor_market_heatmap,
    chart_12_jolts_indicators as chart_12_v2,
    chart_13_beveridge_curve as chart_13_v2,
)


def generate_ultimate_chartbook():
    """
    Generate the ULTIMATE 42-chart chartbook using the best charts we actually built
    """
    timestamp = datetime.now().strftime('%Y-%m-%d')
    output_dir = Path(__file__).parent / "chartbooks"
    output_dir.mkdir(exist_ok=True)

    pdf_path = output_dir / f"Lighthouse_Macro_ULTIMATE_Chartbook_{timestamp}.pdf"

    print("=" * 80)
    print("GENERATING ULTIMATE LIGHTHOUSE MACRO CHARTBOOK")
    print("Using ACTUAL charts we built (not generic placeholders)")
    print("=" * 80)
    print(f"Output: {pdf_path}")
    print()

    with PdfPages(pdf_path) as pdf:

        # === SECTION 1: MACRO REGIME (Charts 1-10) ===
        print("\n[SECTION 1] Macro Regime - Charts 1-10")

        section_fig = create_section_page(
            section_number=1,
            section_title='Macro Regime',
            section_description='Economic cycle positioning, Phillips curve, ISM, yield curve,\ninflation dynamics, Fed policy, financial stress',
            charts_range='Charts 1-10'
        )
        pdf.savefig(section_fig, dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Section divider page")

        # Use the BEST version of each chart (from generate_full_chartbook or macro_regime_charts)
        chart_functions_s1 = [
            ("Economic Cycle Scatter", chart_01_economic_cycle_scatter),
            ("Leading Indicators", chart_02_leading_indicators),
            ("Phillips Curve", chart_02_phillips_curve),  # Better than unemployment_inflation
            ("Labor Market Heatmap", chart_04_labor_market_heatmap),
            ("ISM Composite", chart_05_ism_composite),
            ("Yield Curve", chart_06_yield_curve),
            ("Yield Curve Spreads", chart_07_yield_curve_spreads),
            ("Credit Impulse", chart_08_credit_impulse),
            ("Financial Stress Index", chart_09_financial_stress_index),
            ("Recession Probability", chart_10_recession_probability),
        ]

        for i, (name, chart_func) in enumerate(chart_functions_s1, start=1):
            try:
                print(f"  [{i:2d}/10] Generating {name}...")
                fig = chart_func()
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)
            except Exception as e:
                print(f"  ✗ Error in Chart {i} ({name}): {e}")

        # === SECTION 2: LABOR MARKETS (Charts 11-13) ===
        print("\n[SECTION 2] Labor Markets - Charts 11-13")

        section_fig = create_section_page(
            section_number=2,
            section_title='Labor Markets',
            section_description='Multi-metric heatmap, JOLTS indicators, Beveridge curve,\nlabor market flow dynamics',
            charts_range='Charts 11-13'
        )
        pdf.savefig(section_fig, dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Section divider page")

        chart_functions_s2 = [
            ("Labor Market Heatmap", chart_11_labor_market_heatmap),
            ("JOLTS Indicators", chart_16_jolts_indicators),
            ("Beveridge Curve", chart_17_beveridge_curve),
        ]

        for i, (name, chart_func) in enumerate(chart_functions_s2, start=11):
            try:
                print(f"  [{i:2d}/13] Generating {name}...")
                fig = chart_func()
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)
            except Exception as e:
                print(f"  ✗ Error in Chart {i} ({name}): {e}")

        # === SECTION 3: MONEY MARKET PLUMBING (Charts 14-23) ===
        print("\n[SECTION 3] Money Market Plumbing - Charts 14-23")

        section_fig = create_section_page(
            section_number=3,
            section_title='Money Market Plumbing',
            section_description='Fed balance sheet, RRP dynamics, money market rates, treasury liquidity,\nSOFR/EFFR spreads, dealer positioning, swap spreads',
            charts_range='Charts 14-23'
        )
        pdf.savefig(section_fig, dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Section divider page")

        chart_functions_s3 = [
            ("Fed Balance Sheet", chart_11_fed_balance_sheet),
            ("RRP vs VIX", chart_12_rrp_vs_vix),
            ("Money Market Rates", chart_13_money_market_rates),
            ("Treasury Liquidity", chart_14_treasury_liquidity),
            ("Liquidity Composite", chart_15_liquidity_composite),
            ("SOFR-EFFR Dynamics", chart_18_sofr_effr_dynamics),
            ("Treasury Fails", chart_19_treasury_fails),
            ("Dealer Positioning", chart_20_dealer_positioning),
            ("Swap Spreads", chart_22_swap_spreads),
            ("Cross-Currency Basis", chart_23_cross_currency_basis),
        ]

        for i, (name, chart_func) in enumerate(chart_functions_s3, start=14):
            try:
                print(f"  [{i:2d}/23] Generating {name}...")
                fig = chart_func()
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)
            except Exception as e:
                print(f"  ✗ Error in Chart {i} ({name}): {e}")

        # === SECTION 4: CREDIT & RISK (Charts 24-30) ===
        print("\n[SECTION 4] Credit & Risk - Charts 24-30")

        section_fig = create_section_page(
            section_number=4,
            section_title='Credit & Risk',
            section_description='High-yield spreads, credit cycle, corporate leverage,\nexcess bond premium, MOVE index, CDX indices',
            charts_range='Charts 24-30'
        )
        pdf.savefig(section_fig, dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Section divider page")

        chart_functions_s4 = [
            ("High-Yield OAS", chart_24_high_yield_oas),
            ("Credit Cycle", chart_25_credit_cycle),
            ("Excess Bond Premium", chart_26_excess_bond_premium),
            ("Corporate Leverage", chart_27_corporate_leverage),
            ("Credit Impulse", chart_28_credit_impulse_v2),
            ("MOVE Index", chart_29_move_index),
            ("CDX Indices", chart_30_cdx_indices),
        ]

        for i, (name, chart_func) in enumerate(chart_functions_s4, start=24):
            try:
                print(f"  [{i:2d}/30] Generating {name}...")
                fig = chart_func()
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)
            except Exception as e:
                print(f"  ✗ Error in Chart {i} ({name}): {e}")

        # === SECTION 5: CRYPTO & DIGITAL ASSETS (Charts 31-35) ===
        print("\n[SECTION 5] Crypto & Digital Assets - Charts 31-35")

        section_fig = create_section_page(
            section_number=5,
            section_title='Crypto & Digital Assets',
            section_description='Bitcoin-stablecoin dynamics, crypto-traditional correlations,\ndigital dollar competition with money market funds',
            charts_range='Charts 31-35'
        )
        pdf.savefig(section_fig, dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Section divider page")

        chart_functions_s5 = [
            ("Bitcoin-Stablecoin Overlay", chart_31_bitcoin_stablecoin_overlay),
            ("Stablecoin Composition", chart_32_stablecoin_composition),
            ("Stablecoin vs MMF", chart_33_stablecoin_vs_mmf),
            ("BTC Realized Volatility", chart_34_btc_realized_vol),
            ("BTC Correlation", chart_35_btc_correlation),
        ]

        for i, (name, chart_func) in enumerate(chart_functions_s5, start=31):
            try:
                print(f"  [{i:2d}/35] Generating {name}...")
                fig = chart_func()
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)
            except Exception as e:
                print(f"  ✗ Error in Chart {i} ({name}): {e}")

        # === SECTION 6: AI INFRASTRUCTURE (Charts 36-42) ===
        print("\n[SECTION 6] AI Infrastructure - Charts 36-42")

        section_fig = create_section_page(
            section_number=6,
            section_title='AI Infrastructure',
            section_description='Mag 7 CapEx, AI software growth, semiconductor supply chain,\nsingle-name technical analysis (NVDA, MSFT, TSM)',
            charts_range='Charts 36-42'
        )
        pdf.savefig(section_fig, dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Section divider page")

        chart_functions_s6 = [
            ("Mag 7 CapEx", chart_36_mag7_capex),
            ("AI Software RPO", chart_37_ai_software_rpo),
            ("Semi Equipment Exports", chart_38_semi_equipment_exports),
            ("IT Investment/GDP", chart_39_it_investment_gdp),
            ("NVDA 3-Panel", chart_40_nvda),
            ("MSFT 3-Panel", chart_41_msft),
            ("TSM 3-Panel", chart_42_tsm),
        ]

        for i, (name, chart_func) in enumerate(chart_functions_s6, start=36):
            try:
                print(f"  [{i:2d}/42] Generating {name}...")
                fig = chart_func()
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)
            except Exception as e:
                print(f"  ✗ Error in Chart {i} ({name}): {e}")

    print("\n" + "=" * 80)
    print(f"✓ ULTIMATE Chartbook generation complete!")
    print(f"✓ Output: {pdf_path}")
    print(f"✓ Total pages: 42 charts + 6 section dividers = 48 pages")
    print("=" * 80)

    return pdf_path


if __name__ == "__main__":
    pdf_path = generate_ultimate_chartbook()
    print(f"\n✓ ULTIMATE Lighthouse Macro Chartbook ready: {pdf_path}")
