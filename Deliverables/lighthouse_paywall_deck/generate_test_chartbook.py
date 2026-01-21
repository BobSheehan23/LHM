"""
Lighthouse Macro - Test Chartbook Generator
Sections 1-2 only (Liquidity + Labor) with full-page section overviews
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from pathlib import Path

# Import section overview pages
from section_overview_pages import section_1_overview, section_2_overview

# Import chart functions
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

from section2_labor_charts import (
    chart_11_labor_fragility_index,
    chart_12_labor_dynamism_index,
    chart_13_payroll_quits_divergence,
    chart_14_hours_employment_divergence,
    chart_15_labor_market_heatmap,
    chart_16_jolts_indicators,
    chart_17_beveridge_curve,
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
    ax.text(0.5, 0.38, 'Proprietary Macro Intelligence',
            ha='center', va='center', fontsize=18, style='italic',
            color=COLORS['neutral'], transform=ax.transAxes)

    # Version info
    ax.text(0.5, 0.28, 'TEST EDITION - Sections 1-2',
            ha='center', va='center', fontsize=14,
            color=COLORS['neutral'], transform=ax.transAxes)

    ax.text(0.5, 0.24, 'Liquidity & Funding Stress • Labor Market Dynamics',
            ha='center', va='center', fontsize=12,
            color=COLORS['neutral'], transform=ax.transAxes)

    # Date
    ax.text(0.5, 0.15, f'Generated: {datetime.now().strftime("%B %d, %Y")}',
            ha='center', va='center', fontsize=11,
            color=COLORS['neutral'], transform=ax.transAxes)

    # Watermark
    ax.text(0.5, 0.05, 'MACRO, ILLUMINATED.',
            ha='center', va='bottom', fontsize=12, fontweight='bold',
            color=COLORS['ocean_blue'], alpha=0.6, transform=ax.transAxes)

    return fig


def create_toc_page():
    """Create table of contents"""
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    # Title
    ax.text(0.5, 0.90, 'TABLE OF CONTENTS',
            ha='center', va='center', fontsize=24, fontweight='bold',
            color=COLORS['ocean_blue'], transform=ax.transAxes)

    # Separator
    ax.plot([0.15, 0.85], [0.87, 0.87],
            color=COLORS['ocean_blue'], linewidth=2,
            transform=ax.transAxes)

    # TOC entries
    toc_entries = [
        ("SECTION 1: LIQUIDITY & FUNDING STRESS", "Charts 1-10"),
        ("  • Liquidity Cushion Index (LCI)", "Chart 1"),
        ("  • Yield-Funding Stress (YFS)", "Chart 2"),
        ("  • Repo Rate Dispersion", "Chart 3"),
        ("  • Fed Balance Sheet + RRP", "Chart 4"),
        ("  • SOFR-EFFR-OBFR Dynamics", "Chart 5"),
        ("  • Money Market Dashboard", "Chart 6"),
        ("  • Treasury Liquidity", "Chart 7"),
        ("  • Swap Spreads", "Chart 8"),
        ("  • Cross-Currency Basis", "Chart 9"),
        ("  • Dealer Positioning", "Chart 10"),
        ("", ""),
        ("SECTION 2: LABOR MARKET DYNAMICS", "Charts 11-17"),
        ("  • Labor Fragility Index (LFI)", "Chart 11"),
        ("  • Labor Dynamism Index (LDI)", "Chart 12"),
        ("  • Payroll-Quits Divergence", "Chart 13"),
        ("  • Hours-Employment Divergence", "Chart 14"),
        ("  • Labor Market Heatmap", "Chart 15"),
        ("  • JOLTS Indicators", "Chart 16"),
        ("  • Beveridge Curve", "Chart 17"),
    ]

    y_position = 0.82
    for entry, page in toc_entries:
        if entry == "":
            y_position -= 0.02
            continue

        # Entry
        ax.text(0.15, y_position, entry,
                ha='left', va='top',
                fontsize=11 if entry.startswith("SECTION") else 10,
                fontweight='bold' if entry.startswith("SECTION") else 'normal',
                color=COLORS['ocean_blue'] if entry.startswith("SECTION") else COLORS['black'],
                transform=ax.transAxes)

        # Page number
        ax.text(0.85, y_position, page,
                ha='right', va='top',
                fontsize=11 if entry.startswith("SECTION") else 10,
                color=COLORS['neutral'],
                transform=ax.transAxes)

        y_position -= 0.035 if entry.startswith("SECTION") else 0.028

    # Watermark
    ax.text(0.5, 0.05, 'MACRO, ILLUMINATED.',
            ha='center', va='bottom', fontsize=10, fontweight='bold',
            color=COLORS['ocean_blue'], alpha=0.6, transform=ax.transAxes)

    return fig


def generate_test_chartbook():
    """Generate test chartbook with Sections 1-2"""
    timestamp = datetime.now().strftime('%Y-%m-%d')
    output_dir = Path(__file__).parent / "chartbooks"
    output_dir.mkdir(exist_ok=True)

    pdf_path = output_dir / f"Lighthouse_TEST_Chartbook_Sections_1-2_{timestamp}.pdf"

    print("=" * 80)
    print("GENERATING LIGHTHOUSE MACRO TEST CHARTBOOK")
    print("Sections 1-2: Liquidity & Labor Market")
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

        # === TABLE OF CONTENTS ===
        print("Creating table of contents...")
        toc = create_toc_page()
        pdf.savefig(toc, dpi=300, bbox_inches='tight')
        plt.close(toc)
        print("  ✓ Table of contents")

        # === SECTION 1: LIQUIDITY & FUNDING STRESS ===
        print("\n[SECTION 1] Liquidity & Funding Stress")

        # Section overview page (full-page text)
        print("  Creating section overview page...")
        overview = section_1_overview()
        pdf.savefig(overview, dpi=300, bbox_inches='tight')
        plt.close(overview)
        print("  ✓ Section 1 overview page")

        # Charts 1-10
        section1_charts = [
            ("Liquidity Cushion Index (LCI)", chart_01_liquidity_cushion_index),
            ("Yield-Funding Stress (YFS)", chart_02_yield_funding_stress),
            ("Repo Rate Dispersion", chart_03_repo_rate_dispersion),
            ("Fed Balance Sheet + RRP", chart_04_fed_balance_sheet_rrp),
            ("SOFR-EFFR-OBFR Dynamics", chart_05_sofr_effr_obfr_dynamics),
            ("Money Market Dashboard", chart_06_money_market_dashboard),
            ("Treasury Liquidity", chart_07_treasury_liquidity),
            ("Swap Spreads", chart_08_swap_spreads),
            ("Cross-Currency Basis", chart_09_cross_currency_basis),
            ("Dealer Positioning", chart_10_dealer_positioning),
        ]

        for i, (name, chart_func) in enumerate(section1_charts, start=1):
            try:
                print(f"  [{i:2d}/10] Generating {name}...")
                fig = chart_func()
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)
            except Exception as e:
                print(f"  ✗ Error in Chart {i} ({name}): {e}")
                import traceback
                traceback.print_exc()

        # === SECTION 2: LABOR MARKET DYNAMICS ===
        print("\n[SECTION 2] Labor Market Dynamics")

        # Section overview page
        print("  Creating section overview page...")
        overview = section_2_overview()
        pdf.savefig(overview, dpi=300, bbox_inches='tight')
        plt.close(overview)
        print("  ✓ Section 2 overview page")

        # Charts 11-17
        section2_charts = [
            ("Labor Fragility Index (LFI)", chart_11_labor_fragility_index),
            ("Labor Dynamism Index (LDI)", chart_12_labor_dynamism_index),
            ("Payroll-Quits Divergence", chart_13_payroll_quits_divergence),
            ("Hours-Employment Divergence", chart_14_hours_employment_divergence),
            ("Labor Market Heatmap", chart_15_labor_market_heatmap),
            ("JOLTS Indicators", chart_16_jolts_indicators),
            ("Beveridge Curve", chart_17_beveridge_curve),
        ]

        for i, (name, chart_func) in enumerate(section2_charts, start=11):
            try:
                print(f"  [{i:2d}/17] Generating {name}...")
                fig = chart_func()
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)
            except Exception as e:
                print(f"  ✗ Error in Chart {i} ({name}): {e}")
                import traceback
                traceback.print_exc()

    print("\n" + "=" * 80)
    print(f"✓ TEST Chartbook generation complete!")
    print(f"✓ Output: {pdf_path}")
    print(f"✓ Total pages: Cover + TOC + 2 Section Overviews + 17 Charts = ~21 pages")
    print("=" * 80)

    return pdf_path


if __name__ == "__main__":
    pdf_path = generate_test_chartbook()
    print(f"\n✓ Test Chartbook ready: {pdf_path}")
