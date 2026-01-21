"""
Lighthouse Macro - Comprehensive Financial Dashboard
Daily dashboard combining NY Fed + OFR data

Includes:
- Money Market Rates (SOFR, EFFR, OBFR)
- RRP Operations
- OFR Financial Stress Index
- OFR Bank Systemic Risk Monitor
- Primary Dealer Stats
- SOMA Holdings

Usage:
    python3 comprehensive_financial_dashboard.py
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

from nyfed_api_reference import NYFedAPI
from ofr_data_readers import OFRDataReader
from lighthouse_style import (
    COLORS,
    create_single_axis_chart,
    create_dual_axis_chart,
    add_last_value_label,
    create_section_page
)

# Output directory
OUTPUT_DIR = Path(__file__).parent / "dashboards"
OUTPUT_DIR.mkdir(exist_ok=True)


def create_comprehensive_dashboard():
    """Generate comprehensive financial markets dashboard"""
    timestamp = datetime.now().strftime('%Y-%m-%d')
    pdf_path = OUTPUT_DIR / f"Comprehensive_Financial_Dashboard_{timestamp}.pdf"

    with PdfPages(pdf_path) as pdf:
        print("=" * 70)
        print("GENERATING COMPREHENSIVE FINANCIAL DASHBOARD")
        print("=" * 70)

        # Initialize APIs
        nyfed = NYFedAPI(cache_hours=24)
        ofr = OFRDataReader()

        # === SECTION 1: MONEY MARKETS ===
        section_fig = create_section_page(
            section_number=1,
            section_title='Money Market Dynamics',
            section_description='Reference rates, funding markets, and Federal Reserve operations',
            charts_range='Charts 1-5'
        )
        pdf.savefig(section_fig, dpi=300, bbox_inches='tight')
        plt.close()

        # Chart 1: Reference Rates
        print("\n[Chart 1] Fetching reference rates...")
        sofr = nyfed.get_sofr(last_n=500)
        effr = nyfed.get_effr(last_n=500)
        obfr = nyfed.get_obfr(last_n=500)

        if not sofr.empty and not effr.empty and not obfr.empty:
            fig, ax = create_single_axis_chart(
                chart_number=1,
                title='Money Market Reference Rates',
                ylabel='Rate (%)',
                source='NY Fed'
            )

            ax.plot(sofr.index, sofr['percentRate'],
                   color=COLORS['ocean_blue'], linewidth=2.5, label='SOFR')
            ax.plot(effr.index, effr['percentRate'],
                   color=COLORS['orange'], linewidth=2, label='EFFR')
            ax.plot(obfr.index, obfr['percentRate'],
                   color=COLORS['carolina_blue'], linewidth=2, label='OBFR')

            add_last_value_label(ax, sofr['percentRate'], COLORS['ocean_blue'])
            add_last_value_label(ax, effr['percentRate'], COLORS['orange'])
            add_last_value_label(ax, obfr['percentRate'], COLORS['carolina_blue'])

            ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
            ax.set_ylim(bottom=0)
            plt.tight_layout()
            pdf.savefig(fig, dpi=300, bbox_inches='tight')
            plt.close()
            print("   ✓ Chart 1 saved")

        # Chart 2: RRP Operations
        print("\n[Chart 2] Fetching RRP operations...")
        rrp = nyfed.get_rrp_operations()

        if not rrp.empty:
            fig, ax = create_single_axis_chart(
                chart_number=2,
                title='Reverse Repo (RRP) Operations - Fed Liquidity Drain',
                ylabel='Amount Accepted ($B)',
                source='NY Fed'
            )

            # Last 2 years for better visibility
            recent_rrp = rrp[rrp.index >= (datetime.now() - timedelta(days=730))]

            ax.plot(recent_rrp.index, recent_rrp['totalAmtAccepted'],
                   color=COLORS['ocean_blue'], linewidth=2.5, label='RRP Usage')
            ax.fill_between(recent_rrp.index, 0, recent_rrp['totalAmtAccepted'],
                           color=COLORS['ocean_blue'], alpha=0.1)

            add_last_value_label(ax, recent_rrp['totalAmtAccepted'], COLORS['ocean_blue'], fmt='{:.0f}B')

            ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
            ax.set_ylim(bottom=0)
            plt.tight_layout()
            pdf.savefig(fig, dpi=300, bbox_inches='tight')
            plt.close()
            print("   ✓ Chart 2 saved")

        # Chart 3: SOFR vs EFFR Volumes
        print("\n[Chart 3] Creating volume comparison...")
        if not sofr.empty and not effr.empty:
            fig, ax_left, ax_right = create_dual_axis_chart(
                chart_number=3,
                title='Money Market Volumes: SOFR vs EFFR',
                left_label='EFFR Volume ($B)',
                right_label='SOFR Volume ($B)',
                source='NY Fed'
            )

            # Last year for visibility
            recent_dates = sofr.index >= (datetime.now() - timedelta(days=365))

            ax_left.plot(sofr.index[recent_dates], effr.loc[sofr.index[recent_dates], 'volumeInBillions'],
                        color=COLORS['orange'], linewidth=2, alpha=0.7, label='EFFR Volume')

            ax_right.plot(sofr.index[recent_dates], sofr.loc[recent_dates, 'volumeInBillions'],
                         color=COLORS['ocean_blue'], linewidth=2.5, label='SOFR Volume')

            lines1, labels1 = ax_left.get_legend_handles_labels()
            lines2, labels2 = ax_right.get_legend_handles_labels()
            ax_left.legend(lines1 + lines2, labels1 + labels2, loc='upper left',
                          fontsize=9, framealpha=0.95)

            plt.tight_layout()
            pdf.savefig(fig, dpi=300, bbox_inches='tight')
            plt.close()
            print("   ✓ Chart 3 saved")

        # Chart 4: SOFR-EFFR Spread
        print("\n[Chart 4] Creating rate spread...")
        if not sofr.empty and not effr.empty:
            common_dates = sofr.index.intersection(effr.index)

            fig, ax = create_single_axis_chart(
                chart_number=4,
                title='SOFR-EFFR Spread (Secured vs Unsecured Funding)',
                ylabel='Spread (bps)',
                source='NY Fed'
            )

            spread = (sofr.loc[common_dates, 'percentRate'] -
                     effr.loc[common_dates, 'percentRate']) * 100

            ax.plot(common_dates, spread,
                   color=COLORS['ocean_blue'], linewidth=2.5, label='SOFR-EFFR Spread')
            ax.axhline(0, color=COLORS['neutral'], linestyle='--', linewidth=1, alpha=0.5)
            ax.fill_between(common_dates, 0, spread,
                           where=(spread >= 0),
                           color=COLORS['ocean_blue'], alpha=0.1)
            ax.fill_between(common_dates, 0, spread,
                           where=(spread < 0),
                           color=COLORS['orange'], alpha=0.1)

            add_last_value_label(ax, spread, COLORS['ocean_blue'], fmt='{:.1f}')

            ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
            plt.tight_layout()
            pdf.savefig(fig, dpi=300, bbox_inches='tight')
            plt.close()
            print("   ✓ Chart 4 saved")

        # === SECTION 2: FINANCIAL STRESS ===
        section_fig = create_section_page(
            section_number=2,
            section_title='Financial Stress Indicators',
            section_description='OFR Financial Stress Index and component breakdown showing\nsystem-wide stress across credit, funding, and volatility metrics',
            charts_range='Charts 5-7'
        )
        pdf.savefig(section_fig, dpi=300, bbox_inches='tight')
        plt.close()

        # Chart 5: OFR Financial Stress Index
        print("\n[Chart 5] Loading OFR FSI...")
        fsi = ofr.read_fsi()

        if not fsi.empty and 'OFR FSI' in fsi.columns:
            fig, ax = create_single_axis_chart(
                chart_number=5,
                title='OFR Financial Stress Index',
                ylabel='FSI (Std. Deviations)',
                source='OFR'
            )

            # Last 5 years for visibility
            recent_fsi = fsi[fsi.index >= (datetime.now() - timedelta(days=1825))]

            ax.plot(recent_fsi.index, recent_fsi['OFR FSI'],
                   color=COLORS['ocean_blue'], linewidth=2.5, label='OFR FSI')
            ax.axhline(0, color=COLORS['neutral'], linestyle='--', linewidth=1, alpha=0.5)

            # Highlight stress periods
            ax.fill_between(recent_fsi.index, 0, recent_fsi['OFR FSI'],
                           where=(recent_fsi['OFR FSI'] > 0),
                           color=COLORS['orange'], alpha=0.2, label='Elevated Stress')

            add_last_value_label(ax, recent_fsi['OFR FSI'], COLORS['ocean_blue'], fmt='{:.2f}')

            ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
            plt.tight_layout()
            pdf.savefig(fig, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"   ✓ Chart 5 saved | Latest FSI: {fsi['OFR FSI'].iloc[-1]:.2f}")

        # Chart 6: FSI Components
        print("\n[Chart 6] Creating FSI components chart...")
        if not fsi.empty:
            fig, ax = create_single_axis_chart(
                chart_number=6,
                title='OFR FSI Components Breakdown',
                ylabel='Component Value (Std. Dev)',
                source='OFR'
            )

            # Last 5 years
            recent_fsi = fsi[fsi.index >= (datetime.now() - timedelta(days=1825))]

            # Plot key components
            if 'Credit' in fsi.columns:
                ax.plot(recent_fsi.index, recent_fsi['Credit'],
                       color=COLORS['ocean_blue'], linewidth=2, label='Credit', alpha=0.8)
            if 'Funding' in fsi.columns:
                ax.plot(recent_fsi.index, recent_fsi['Funding'],
                       color=COLORS['orange'], linewidth=2, label='Funding', alpha=0.8)
            if 'Volatility' in fsi.columns:
                ax.plot(recent_fsi.index, recent_fsi['Volatility'],
                       color=COLORS['carolina_blue'], linewidth=2, label='Volatility', alpha=0.8)
            if 'Safe assets' in fsi.columns:
                ax.plot(recent_fsi.index, recent_fsi['Safe assets'],
                       color=COLORS['magenta'], linewidth=1.5, label='Safe Assets', alpha=0.7)

            ax.axhline(0, color=COLORS['neutral'], linestyle='--', linewidth=1, alpha=0.5)
            ax.legend(loc='upper left', fontsize=9, framealpha=0.95, ncol=2)
            plt.tight_layout()
            pdf.savefig(fig, dpi=300, bbox_inches='tight')
            plt.close()
            print("   ✓ Chart 6 saved")

        # Chart 7: FSI Regional Breakdown
        print("\n[Chart 7] Creating FSI regional breakdown...")
        if not fsi.empty:
            fig, ax = create_single_axis_chart(
                chart_number=7,
                title='OFR FSI Regional Contributions',
                ylabel='Regional Component (Std. Dev)',
                source='OFR'
            )

            # Last 5 years
            recent_fsi = fsi[fsi.index >= (datetime.now() - timedelta(days=1825))]

            if 'United States' in fsi.columns:
                ax.plot(recent_fsi.index, recent_fsi['United States'],
                       color=COLORS['ocean_blue'], linewidth=2.5, label='United States', alpha=0.9)
            if 'Other advanced economies' in fsi.columns:
                ax.plot(recent_fsi.index, recent_fsi['Other advanced economies'],
                       color=COLORS['orange'], linewidth=2, label='Other Advanced Economies', alpha=0.8)
            if 'Emerging markets' in fsi.columns:
                ax.plot(recent_fsi.index, recent_fsi['Emerging markets'],
                       color=COLORS['carolina_blue'], linewidth=2, label='Emerging Markets', alpha=0.8)

            ax.axhline(0, color=COLORS['neutral'], linestyle='--', linewidth=1, alpha=0.5)
            ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
            plt.tight_layout()
            pdf.savefig(fig, dpi=300, bbox_inches='tight')
            plt.close()
            print("   ✓ Chart 7 saved")

        # === SECTION 3: BANKING SECTOR RISK ===
        section_fig = create_section_page(
            section_number=3,
            section_title='Bank Systemic Risk Monitor',
            section_description='OFR measures of systemic importance and interconnectedness\nacross global systemically important banks (G-SIBs)',
            charts_range='Chart 8'
        )
        pdf.savefig(section_fig, dpi=300, bbox_inches='tight')
        plt.close()

        # Chart 8: BSRM - Top Systemically Important Banks
        print("\n[Chart 8] Loading OFR BSRM...")
        bsrm = ofr.read_bsrm()

        if not bsrm.empty and 'Systemic Importance Score' in bsrm.columns:
            # Get latest year data and top 15 banks
            latest_year = bsrm['Year'].max()
            latest_data = bsrm[bsrm['Year'] == latest_year].copy()
            top_banks = latest_data.nlargest(15, 'Systemic Importance Score')

            fig, ax = plt.subplots(figsize=(11, 8.5))
            ax.set_title(f'Top 15 Systemically Important Banks ({int(latest_year)})',
                        fontsize=14, fontweight='bold', pad=15)

            # Horizontal bar chart
            y_pos = np.arange(len(top_banks))
            bars = ax.barh(y_pos, top_banks['Systemic Importance Score'],
                          color=COLORS['ocean_blue'], alpha=0.8)

            # Color bars by score magnitude
            for i, (idx, row) in enumerate(top_banks.iterrows()):
                score = row['Systemic Importance Score']
                if score > 400:
                    bars[i].set_color(COLORS['orange'])
                elif score > 300:
                    bars[i].set_color(COLORS['ocean_blue'])
                else:
                    bars[i].set_color(COLORS['carolina_blue'])

            ax.set_yticks(y_pos)
            ax.set_yticklabels([f"{row['Institution Name']} ({row['Parent Country']})"
                               for idx, row in top_banks.iterrows()],
                              fontsize=9)
            ax.set_xlabel('Systemic Importance Score', fontsize=11, fontweight='bold')
            ax.invert_yaxis()

            # Add branding
            from lighthouse_style import add_lighthouse_branding
            add_lighthouse_branding(fig, ax, 8, 'OFR BSRM')

            plt.tight_layout()
            pdf.savefig(fig, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"   ✓ Chart 8 saved | {len(top_banks)} banks, latest year: {int(latest_year)}")

        print("\n" + "=" * 70)
        print(f"✓ Dashboard saved: {pdf_path}")
        print("=" * 70)

        return pdf_path


if __name__ == "__main__":
    pdf_path = create_comprehensive_dashboard()
    print(f"\n✓ Comprehensive Financial Dashboard complete: {pdf_path}")
