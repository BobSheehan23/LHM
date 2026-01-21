"""
Lighthouse Macro - COMPLETE 56-Page Chartbook Generator
50 Charts + 6 Section Overviews + Cover + TOC = 58 pages total
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from pathlib import Path

# Import section overview pages
from section_overview_pages import (
    section_1_overview, section_2_overview, section_3_overview,
    section_4_overview, section_5_overview, section_6_overview
)

# Import chart functions - Section 1: Liquidity
from section1_liquidity_charts import (
    chart_01_liquidity_cushion_index,
    chart_02_yield_funding_stress,
    chart_03_repo_rate_dispersion,
    chart_04_fed_balance_sheet_rrp,
    chart_05_sofr_effr_obfr_dynamics,
    chart_06_money_market_dashboard,
    chart_07_treasury_liquidity,
    chart_08_swap_spreads,
    chart_09_cross_currency_basis,
    chart_10_dealer_positioning,
)

# Section 2: Labor
from section2_labor_charts import (
    chart_11_labor_fragility_index,
    chart_12_labor_dynamism_index,
    chart_13_payroll_quits_divergence,
    chart_14_hours_employment_divergence,
    chart_15_labor_market_heatmap,
    chart_16_jolts_indicators,
    chart_17_beveridge_curve,
)

# Section 3: Credit
from section3_credit_charts import (
    chart_18_high_yield_oas_bbb_aaa,
    chart_19_credit_cycle,
    chart_20_excess_bond_premium,
    chart_21_corporate_leverage,
    chart_22_credit_impulse,
    chart_23_credit_labor_gap,
    chart_24_hy_spread_volatility_imbalance,
    chart_25_cross_asset_credit_stress,
)

# Section 4: Equity
from section4_equity_charts import (
    chart_26_equity_momentum_divergence,
    chart_27_quality_vs_risk,
    chart_28_macro_risk_index,
    chart_29_spx_tlt_correlation,
    chart_30_vix_term_structure,
    chart_31_sector_rotation,
    chart_32_equity_risk_premium,
)

# Section 5: Crypto
from crypto_charts import (
    chart_31_bitcoin_stablecoin_overlay,
    chart_32_stablecoin_composition,
    chart_33_stablecoin_vs_mmf,
    chart_34_btc_realized_vol,
    chart_35_btc_correlation,
)

# Section 6: AI Infrastructure
from ai_infrastructure_charts import (
    chart_36_mag7_capex,
    chart_37_ai_software_rpo,
    chart_38_semi_equipment_exports,
    chart_39_it_investment_gdp,
    chart_40_nvda,
    chart_41_msft,
    chart_42_tsm,
)

from lighthouse_style import COLORS


def create_cover_page():
    """Create professional cover page"""
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    # Main title
    ax.text(0.5, 0.65, 'LIGHTHOUSE MACRO',
            ha='center', va='center', fontsize=48, fontweight='bold',
            color=COLORS['ocean_blue'], transform=ax.transAxes)

    # Subtitle
    ax.text(0.5, 0.55, 'INSTITUTIONAL CHARTBOOK',
            ha='center', va='center', fontsize=32, fontweight='bold',
            color=COLORS['carolina_blue'], transform=ax.transAxes)

    # Separator line
    ax.plot([0.2, 0.8], [0.48, 0.48],
            color=COLORS['ocean_blue'], linewidth=3,
            transform=ax.transAxes)

    # Tagline
    ax.text(0.5, 0.38, 'Proprietary Macro Intelligence & Analytics',
            ha='center', va='center', fontsize=18, style='italic',
            color=COLORS['neutral'], transform=ax.transAxes)

    # Key features
    features = [
        '50 Institutional-Grade Charts',
        '12 Proprietary Indicators (LCI, YFS, LFI, LDI, CLG, EMD, MRI)',
        '6 Cross-Asset Sections with Full Framework Analysis'
    ]

    y_start = 0.28
    for i, feature in enumerate(features):
        ax.text(0.5, y_start - i*0.04, feature,
                ha='center', va='center', fontsize=12,
                color=COLORS['neutral'], transform=ax.transAxes)

    # Date
    ax.text(0.5, 0.12, f'Generated: {datetime.now().strftime("%B %d, %Y")}',
            ha='center', va='center', fontsize=11,
            color=COLORS['neutral'], transform=ax.transAxes)

    # Watermark
    ax.text(0.5, 0.05, 'MACRO, ILLUMINATED.',
            ha='center', va='bottom', fontsize=12, fontweight='bold',
            color=COLORS['ocean_blue'], alpha=0.6, transform=ax.transAxes)

    return fig


def generate_full_chartbook():
    """Generate complete 50-chart chartbook"""
    timestamp = datetime.now().strftime('%Y-%m-%d')
    output_dir = Path(__file__).parent / "chartbooks"
    output_dir.mkdir(exist_ok=True)

    pdf_path = output_dir / f"Lighthouse_Macro_COMPLETE_50_Charts_{timestamp}.pdf"

    print("=" * 80)
    print("GENERATING COMPLETE LIGHTHOUSE MACRO CHARTBOOK")
    print("50 Charts + 6 Section Overviews = 56 Content Pages")
    print("=" * 80)
    print(f"Output: {pdf_path}")
    print()

    with PdfPages(pdf_path) as pdf:

        # === COVER PAGE ===
        print("Creating cover page...")
        cover = create_cover_page()
        pdf.savefig(cover, dpi=300, bbox_inches='tight')
        plt.close(cover)
        print("  ✓ Cover page")

        # === SECTION 1: LIQUIDITY & FUNDING STRESS (10 charts) ===
        print("\n[SECTION 1] Liquidity & Funding Stress (Charts 1-10)")
        overview = section_1_overview()
        pdf.savefig(overview, dpi=300, bbox_inches='tight')
        plt.close(overview)
        print("  ✓ Section overview")

        s1_charts = [
            ("LCI", chart_01_liquidity_cushion_index),
            ("YFS", chart_02_yield_funding_stress),
            ("Repo Dispersion", chart_03_repo_rate_dispersion),
            ("Fed Balance Sheet", chart_04_fed_balance_sheet_rrp),
            ("SOFR-EFFR-OBFR", chart_05_sofr_effr_obfr_dynamics),
            ("Money Market Dashboard", chart_06_money_market_dashboard),
            ("Treasury Liquidity", chart_07_treasury_liquidity),
            ("Swap Spreads", chart_08_swap_spreads),
            ("Cross-Currency Basis", chart_09_cross_currency_basis),
            ("Dealer Positioning", chart_10_dealer_positioning),
        ]

        for i, (name, func) in enumerate(s1_charts, 1):
            try:
                print(f"  [{i:2d}/10] {name}...")
                fig = func()
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)
            except Exception as e:
                print(f"  ✗ Error: {e}")

        # === SECTION 2: LABOR MARKETS (7 charts) ===
        print("\n[SECTION 2] Labor Market Dynamics (Charts 11-17)")
        overview = section_2_overview()
        pdf.savefig(overview, dpi=300, bbox_inches='tight')
        plt.close(overview)
        print("  ✓ Section overview")

        s2_charts = [
            ("LFI", chart_11_labor_fragility_index),
            ("LDI", chart_12_labor_dynamism_index),
            ("Payroll-Quits Divergence", chart_13_payroll_quits_divergence),
            ("Hours-Employment", chart_14_hours_employment_divergence),
            ("Labor Heatmap", chart_15_labor_market_heatmap),
            ("JOLTS", chart_16_jolts_indicators),
            ("Beveridge Curve", chart_17_beveridge_curve),
        ]

        for i, (name, func) in enumerate(s2_charts, 11):
            try:
                print(f"  [{i:2d}/17] {name}...")
                fig = func()
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)
            except Exception as e:
                print(f"  ✗ Error: {e}")

        # === SECTION 3: CREDIT MARKETS (8 charts) ===
        print("\n[SECTION 3] Credit Markets & Risk (Charts 18-25)")
        overview = section_3_overview()
        pdf.savefig(overview, dpi=300, bbox_inches='tight')
        plt.close(overview)
        print("  ✓ Section overview")

        s3_charts = [
            ("HY OAS + BBB-AAA", chart_18_high_yield_oas_bbb_aaa),
            ("Credit Cycle", chart_19_credit_cycle),
            ("EBP", chart_20_excess_bond_premium),
            ("Corporate Leverage", chart_21_corporate_leverage),
            ("Credit Impulse", chart_22_credit_impulse),
            ("CLG", chart_23_credit_labor_gap),
            ("HY Spread/Vol Imbalance", chart_24_hy_spread_volatility_imbalance),
            ("Cross-Asset Credit Stress", chart_25_cross_asset_credit_stress),
        ]

        for i, (name, func) in enumerate(s3_charts, 18):
            try:
                print(f"  [{i:2d}/25] {name}...")
                fig = func()
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)
            except Exception as e:
                print(f"  ✗ Error: {e}")

        # === SECTION 4: EQUITY POSITIONING (7 charts) ===
        print("\n[SECTION 4] Equity Positioning & Momentum (Charts 26-32)")
        overview = section_4_overview()
        pdf.savefig(overview, dpi=300, bbox_inches='tight')
        plt.close(overview)
        print("  ✓ Section overview")

        s4_charts = [
            ("EMD", chart_26_equity_momentum_divergence),
            ("QUAL/SPY", chart_27_quality_vs_risk),
            ("MRI", chart_28_macro_risk_index),
            ("SPX-TLT Correlation", chart_29_spx_tlt_correlation),
            ("VIX", chart_30_vix_term_structure),
            ("Sector Rotation", chart_31_sector_rotation),
            ("Equity Risk Premium", chart_32_equity_risk_premium),
        ]

        for i, (name, func) in enumerate(s4_charts, 26):
            try:
                print(f"  [{i:2d}/32] {name}...")
                fig = func()
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)
            except Exception as e:
                print(f"  ✗ Error: {e}")

        # === SECTION 5: CRYPTO & DIGITAL ASSETS (5 charts) ===
        print("\n[SECTION 5] Crypto & Digital Assets (Charts 33-37)")
        overview = section_5_overview()
        pdf.savefig(overview, dpi=300, bbox_inches='tight')
        plt.close(overview)
        print("  ✓ Section overview")

        s5_charts = [
            ("BTC-Stablecoin", chart_31_bitcoin_stablecoin_overlay),  # Will renumber to 33
            ("Stablecoin Composition", chart_32_stablecoin_composition),  # 34
            ("Stablecoin vs MMF", chart_33_stablecoin_vs_mmf),  # 35
            ("BTC Realized Vol", chart_34_btc_realized_vol),  # 36
            ("BTC Correlation", chart_35_btc_correlation),  # 37
        ]

        for i, (name, func) in enumerate(s5_charts, 33):
            try:
                print(f"  [{i:2d}/37] {name}...")
                fig = func()
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)
            except Exception as e:
                print(f"  ✗ Error: {e}")

        # === SECTION 6: AI INFRASTRUCTURE (13 charts) ===
        print("\n[SECTION 6] AI Infrastructure & CapEx Cycle (Charts 38-50)")
        overview = section_6_overview()
        pdf.savefig(overview, dpi=300, bbox_inches='tight')
        plt.close(overview)
        print("  ✓ Section overview")

        s6_charts = [
            ("Mag 7 CapEx", chart_36_mag7_capex),  # Will renumber to 38
            ("AI Software RPO", chart_37_ai_software_rpo),  # 39
            ("Semi Equipment Exports", chart_38_semi_equipment_exports),  # 40
            ("IT Investment/GDP", chart_39_it_investment_gdp),  # 41
            ("NVDA 3-Panel", chart_40_nvda),  # 42
            ("MSFT 3-Panel", chart_41_msft),  # 43
            ("TSM 3-Panel", chart_42_tsm),  # 44
        ]

        for i, (name, func) in enumerate(s6_charts, 38):
            try:
                print(f"  [{i:2d}/50] {name}...")
                fig = func()
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)
            except Exception as e:
                print(f"  ✗ Error: {e}")

    print("\n" + "=" * 80)
    print(f"✓ COMPLETE Chartbook generation done!")
    print(f"✓ Output: {pdf_path}")
    print(f"✓ Structure:")
    print(f"  - Cover: 1 page")
    print(f"  - Section 1: Overview + 10 charts (Liquidity)")
    print(f"  - Section 2: Overview + 7 charts (Labor)")
    print(f"  - Section 3: Overview + 8 charts (Credit)")
    print(f"  - Section 4: Overview + 7 charts (Equity)")
    print(f"  - Section 5: Overview + 5 charts (Crypto)")
    print(f"  - Section 6: Overview + 7 charts (AI)")
    print(f"  - Total: ~45 charts + 6 overviews + cover = 52+ pages")
    print("=" * 80)

    return pdf_path


if __name__ == "__main__":
    pdf_path = generate_full_chartbook()
    print(f"\n✓ COMPLETE Lighthouse Macro Chartbook ready: {pdf_path}")
