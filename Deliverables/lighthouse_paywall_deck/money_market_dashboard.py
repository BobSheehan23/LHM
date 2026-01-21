"""
Lighthouse Macro - Comprehensive Money Market Dashboard
Daily dashboard combining NY Fed + OFR data sources

Usage:
    python3 money_market_dashboard.py

Generates multi-page PDF with:
- SOFR, EFFR, OBFR rates and trends
- RRP operations and usage
- Primary Dealer positioning
- SOMA holdings
- OFR repo rates (when available)
- OFR commercial paper rates (when available)
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

from nyfed_api_reference import NYFedAPI
from ofr_api_reference import OFRAPI
from lighthouse_style import (
    COLORS,
    create_single_axis_chart,
    create_dual_axis_chart,
    add_last_value_label
)

# Output directory
OUTPUT_DIR = Path(__file__).parent / "dashboards"
OUTPUT_DIR.mkdir(exist_ok=True)


def create_dashboard():
    """Generate comprehensive money market dashboard"""
    timestamp = datetime.now().strftime('%Y-%m-%d')
    pdf_path = OUTPUT_DIR / f"Money_Market_Dashboard_{timestamp}.pdf"

    with PdfPages(pdf_path) as pdf:
        print("=" * 70)
        print("GENERATING MONEY MARKET DASHBOARD")
        print("=" * 70)

        # Initialize APIs
        nyfed = NYFedAPI(cache_hours=24)
        ofr_stfm = OFRAPI(cache_hours=24, api_type='stfm')

        # === PAGE 1: REFERENCE RATES ===
        print("\n1. Fetching reference rates (SOFR, EFFR, OBFR)...")

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
            print("   ✓ Reference Rates chart saved")
        else:
            print("   ✗ Failed to fetch reference rates")

        # === PAGE 2: RRP OPERATIONS ===
        print("\n2. Fetching RRP operations...")

        rrp = nyfed.get_rrp_operations()

        if not rrp.empty:
            fig, ax = create_single_axis_chart(
                chart_number=2,
                title='Reverse Repo (RRP) Operations',
                ylabel='Amount Accepted ($B)',
                source='NY Fed'
            )

            ax.plot(rrp.index, rrp['totalAmtAccepted'],
                   color=COLORS['ocean_blue'], linewidth=2.5, label='RRP Usage')

            add_last_value_label(ax, rrp['totalAmtAccepted'], COLORS['ocean_blue'], fmt='{:.0f}B')

            ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
            ax.set_ylim(bottom=0)
            plt.tight_layout()
            pdf.savefig(fig, dpi=300, bbox_inches='tight')
            plt.close()
            print("   ✓ RRP Operations chart saved")
        else:
            print("   ✗ Failed to fetch RRP data")

        # === PAGE 3: SOFR VOLUME ===
        print("\n3. Creating SOFR volume chart...")

        if not sofr.empty and 'volumeInBillions' in sofr.columns:
            fig, ax = create_single_axis_chart(
                chart_number=3,
                title='SOFR Daily Volume',
                ylabel='Volume ($B)',
                source='NY Fed'
            )

            ax.plot(sofr.index, sofr['volumeInBillions'],
                   color=COLORS['ocean_blue'], linewidth=2.5, label='SOFR Volume')

            add_last_value_label(ax, sofr['volumeInBillions'], COLORS['ocean_blue'], fmt='{:.0f}B')

            ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
            ax.set_ylim(bottom=0)
            plt.tight_layout()
            pdf.savefig(fig, dpi=300, bbox_inches='tight')
            plt.close()
            print("   ✓ SOFR Volume chart saved")

        # === PAGE 4: EFFR VOLUME ===
        print("\n4. Creating EFFR volume chart...")

        if not effr.empty and 'volumeInBillions' in effr.columns:
            fig, ax = create_single_axis_chart(
                chart_number=4,
                title='EFFR Daily Volume',
                ylabel='Volume ($B)',
                source='NY Fed'
            )

            ax.plot(effr.index, effr['volumeInBillions'],
                   color=COLORS['orange'], linewidth=2.5, label='EFFR Volume')

            add_last_value_label(ax, effr['volumeInBillions'], COLORS['orange'], fmt='{:.0f}B')

            ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
            ax.set_ylim(bottom=0)
            plt.tight_layout()
            pdf.savefig(fig, dpi=300, bbox_inches='tight')
            plt.close()
            print("   ✓ EFFR Volume chart saved")

        # === PAGE 5: RATE SPREADS ===
        print("\n5. Creating rate spread chart...")

        if not sofr.empty and not effr.empty:
            # Align dates
            common_dates = sofr.index.intersection(effr.index)

            fig, ax = create_single_axis_chart(
                chart_number=5,
                title='SOFR-EFFR Spread',
                ylabel='Spread (bps)',
                source='NY Fed'
            )

            spread = (sofr.loc[common_dates, 'percentRate'] -
                     effr.loc[common_dates, 'percentRate']) * 100  # Convert to bps

            ax.plot(common_dates, spread,
                   color=COLORS['ocean_blue'], linewidth=2.5, label='SOFR-EFFR Spread')
            ax.axhline(0, color=COLORS['neutral'], linestyle='--', linewidth=1, alpha=0.5)

            add_last_value_label(ax, spread, COLORS['ocean_blue'], fmt='{:.1f}')

            ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
            plt.tight_layout()
            pdf.savefig(fig, dpi=300, bbox_inches='tight')
            plt.close()
            print("   ✓ Rate Spread chart saved")

        # === PAGE 6: PRIMARY DEALER SERIES LIST ===
        print("\n6. Fetching Primary Dealer series...")

        pd_series = nyfed.list_primary_dealer_series()

        if not pd_series.empty:
            print(f"   ✓ Found {len(pd_series)} Primary Dealer series")
            print("   Top 10 series:")
            if 'label' in pd_series.columns:
                for idx, row in pd_series.head(10).iterrows():
                    print(f"     - {row.get('keyid', 'N/A')}: {row.get('label', 'N/A')}")

        # === PAGE 7: SOMA SUMMARY ===
        print("\n7. Fetching SOMA holdings summary...")

        soma_summary = nyfed.get_soma_summary()

        if not soma_summary.empty:
            print(f"   ✓ SOMA summary: {len(soma_summary)} rows")

        # === OFR DATA (if accessible) ===
        print("\n8. Attempting to fetch OFR data...")
        print("   Note: OFR API endpoints may require authentication")

        # Try to get mnemonics list (this worked)
        try:
            mnemonics = ofr_stfm.list_all_mnemonics()
            if isinstance(mnemonics, list):
                print(f"   ✓ Found {len(mnemonics)} OFR series available")
                print("   Sample mnemonics:")
                for m in mnemonics[:10]:
                    print(f"     - {m}")
        except Exception as e:
            print(f"   ✗ Failed to fetch OFR data: {e}")

        print("\n" + "=" * 70)
        print(f"✓ Dashboard saved: {pdf_path}")
        print("=" * 70)

        return pdf_path


def create_summary_table():
    """Generate summary statistics table"""
    print("\n" + "=" * 70)
    print("MONEY MARKET SUMMARY STATISTICS")
    print("=" * 70)

    nyfed = NYFedAPI(cache_hours=24)

    # Fetch latest data
    sofr = nyfed.get_sofr(last_n=10)
    effr = nyfed.get_effr(last_n=10)
    obfr = nyfed.get_obfr(last_n=10)
    rrp = nyfed.get_rrp_operations()

    if not sofr.empty:
        latest_sofr = sofr['percentRate'].iloc[-1]
        print(f"\nSOFR: {latest_sofr:.2f}%")
        print(f"  Volume: ${sofr['volumeInBillions'].iloc[-1]:.1f}B")

    if not effr.empty:
        latest_effr = effr['percentRate'].iloc[-1]
        print(f"\nEFFR: {latest_effr:.2f}%")
        print(f"  Volume: ${effr['volumeInBillions'].iloc[-1]:.1f}B")

    if not obfr.empty:
        latest_obfr = obfr['percentRate'].iloc[-1]
        print(f"\nOBFR: {latest_obfr:.2f}%")
        if 'volumeInBillions' in obfr.columns:
            print(f"  Volume: ${obfr['volumeInBillions'].iloc[-1]:.1f}B")

    if not rrp.empty:
        latest_rrp = rrp['totalAmtAccepted'].iloc[-1]
        print(f"\nRRP Usage: ${latest_rrp:.1f}B")

    if not sofr.empty and not effr.empty:
        spread = (latest_sofr - latest_effr) * 100
        print(f"\nSOFR-EFFR Spread: {spread:.1f} bps")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    # Generate dashboard
    pdf_path = create_dashboard()

    # Print summary table
    create_summary_table()

    print(f"\n✓ Money Market Dashboard complete: {pdf_path}")
