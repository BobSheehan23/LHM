"""
LIGHTHOUSE MACRO - FLAGSHIP CHART GENERATOR
Creates institutional-quality Macro Risk Index (MRI) visualization

Author: Bob Sheehan, CFA, CMT
Date: November 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Lighthouse Macro color palette
COLORS = {
    'primary': '#003366',      # Deep blue
    'secondary': '#0066CC',    # Bright blue
    'accent': '#FF9900',       # Orange
    'positive': '#00A86B',     # Green
    'negative': '#CC0000',     # Red
    'neutral': '#808080',      # Gray
    'background': '#FFFFFF',   # White
    # TradingView-style palette
    'ocean': '#0089D1',
    'dusk': '#FF7700',
    'sky': '#02CCFE',
    'candy': '#FF13F0',
    'sea': '#20BAAA',
}

def apply_institutional_styling():
    """Apply Lighthouse Macro institutional styling"""
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'font.size': 11,
        'axes.titlesize': 16,
        'axes.titleweight': 'bold',
        'axes.labelsize': 12,
        'axes.labelweight': 'bold',
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.figsize': (14, 8),
        'figure.dpi': 150,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.facecolor': 'white',
        'axes.grid': True,
        'grid.alpha': 0.3,
        'grid.linestyle': '--',
        'grid.linewidth': 0.5,
        'lines.linewidth': 2.5,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.linewidth': 1.5,
    })

def create_mri_chart(indicators_path='proprietary_indicators.csv',
                     output_path='charts/MRI_Macro_Risk_Index.png'):
    """
    Create Macro Risk Index (MRI) flagship chart
    """
    print("=" * 70)
    print("GENERATING FLAGSHIP CHART: MACRO RISK INDEX (MRI)")
    print("=" * 70)

    # Apply styling
    apply_institutional_styling()

    # Load data
    print(f"\n📊 Loading indicators from: {indicators_path}")
    df = pd.read_csv(indicators_path, index_col=0, parse_dates=True)

    # Filter to data with MRI values
    df = df[df['MRI'].notna()].copy()

    print(f"✓ Loaded {len(df)} observations")
    print(f"  Date range: {df.index.min()} to {df.index.max()}")

    # Get latest value
    latest_mri = df['MRI'].iloc[-1]
    latest_date = df.index[-1]

    print(f"\n📊 Latest MRI: {latest_mri:+.2f}σ as of {latest_date.strftime('%Y-%m-%d')}")

    # Create figure
    fig, ax = plt.subplots(figsize=(16, 10))

    # Plot MRI line
    ax.plot(df.index, df['MRI'],
            color=COLORS['primary'],
            linewidth=3,
            label='Macro Risk Index',
            zorder=5)

    # Fill regions
    ax.fill_between(df.index, 0, df['MRI'],
                    where=(df['MRI'] > 0),
                    alpha=0.15, color=COLORS['negative'],
                    label='Elevated Risk', zorder=2)

    ax.fill_between(df.index, 0, df['MRI'],
                    where=(df['MRI'] < 0),
                    alpha=0.15, color=COLORS['positive'],
                    label='Below-Average Risk', zorder=2)

    # Threshold lines
    ax.axhline(y=0, color=COLORS['neutral'], linestyle='-', linewidth=1.5,
               label='Neutral', zorder=3)
    ax.axhline(y=1, color=COLORS['negative'], linestyle='--', linewidth=1.5,
               alpha=0.7, label='+1σ (Caution)', zorder=3)
    ax.axhline(y=2, color=COLORS['negative'], linestyle='--', linewidth=1.5,
               alpha=0.7, label='+2σ (High Risk)', zorder=3)
    ax.axhline(y=-1, color=COLORS['positive'], linestyle='--', linewidth=1.5,
               alpha=0.7, label='-1σ (Low Risk)', zorder=3)

    # Annotate latest value
    ax.scatter([latest_date], [latest_mri],
              color=COLORS['negative'] if latest_mri > 1 else COLORS['accent'],
              s=200, zorder=10, edgecolors='white', linewidths=2)

    # Add text annotation for latest value
    y_offset = 0.3 if latest_mri > 0 else -0.3
    ax.annotate(f'{latest_mri:+.2f}σ',
               xy=(latest_date, latest_mri),
               xytext=(latest_date, latest_mri + y_offset),
               fontsize=14,
               fontweight='bold',
               color=COLORS['negative'] if latest_mri > 1 else COLORS['primary'],
               ha='right',
               bbox=dict(boxstyle='round,pad=0.5',
                        facecolor='white',
                        edgecolor=COLORS['neutral'],
                        alpha=0.9),
               zorder=11)

    # Add regime labels
    regime_text = ""
    if latest_mri > 2:
        regime_text = "🔴 CRISIS RISK\nMarkets significantly under-pricing macro risk"
        regime_color = COLORS['negative']
    elif latest_mri > 1:
        regime_text = "🔴 HIGH RISK\nMarkets under-pricing macro risk"
        regime_color = COLORS['negative']
    elif latest_mri > 0:
        regime_text = "🟡 ELEVATED\nAbove-average systemic risk"
        regime_color = COLORS['accent']
    elif latest_mri > -1:
        regime_text = "🟢 MODERATE\nBelow-average systemic risk"
        regime_color = COLORS['positive']
    else:
        regime_text = "🟢 LOW RISK\nBenign risk environment"
        regime_color = COLORS['positive']

    # Add regime box
    ax.text(0.02, 0.98, regime_text,
           transform=ax.transAxes,
           fontsize=12,
           fontweight='bold',
           color=regime_color,
           va='top',
           ha='left',
           bbox=dict(boxstyle='round,pad=0.8',
                    facecolor='white',
                    edgecolor=regime_color,
                    linewidth=2,
                    alpha=0.95))

    # Title and labels
    title_text = "Lighthouse Macro: Macro Risk Index (MRI)\nComposite Systemic Risk Indicator"
    ax.set_title(title_text, fontsize=18, fontweight='bold',
                loc='left', pad=20, color=COLORS['primary'])

    ax.set_xlabel('Date', fontsize=13, fontweight='bold')
    ax.set_ylabel('Standard Deviations (σ)', fontsize=13, fontweight='bold')

    # Format x-axis
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_minor_locator(mdates.YearLocator(1))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=0, ha='center')

    # Legend
    ax.legend(loc='upper left', frameon=True, shadow=True,
             fancybox=True, framealpha=0.95)

    # TradingView-style spacing: data to left edge, space on right
    ax.set_xlim(left=df.index[0], right=df.index[-1] + pd.Timedelta(days=len(df)*0.02))

    # Grid
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)

    # Add source and formula
    formula_text = "Formula: MRI = LFI - LDI + YFS + z(HY OAS) + EMD - LCI"
    source_text = f"Source: Lighthouse Macro | Bob Sheehan, CFA, CMT\nUpdated: {datetime.now().strftime('%B %d, %Y')}"

    ax.text(0.02, 0.02, formula_text,
           transform=ax.transAxes,
           fontsize=9,
           style='italic',
           color=COLORS['neutral'],
           va='bottom',
           ha='left')

    ax.text(0.98, 0.02, source_text,
           transform=ax.transAxes,
           fontsize=8,
           color=COLORS['neutral'],
           va='bottom',
           ha='right')

    # Add watermark
    ax.text(0.5, 0.5, 'LIGHTHOUSE MACRO',
           transform=ax.transAxes,
           fontsize=60,
           color=COLORS['neutral'],
           alpha=0.05,
           ha='center',
           va='center',
           rotation=30,
           zorder=1)

    # Save
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\n✓ Chart saved: {output_path}")

    # Also save component breakdown chart
    create_mri_component_breakdown(df, output_path.replace('.png', '_components.png'))

    plt.close()

    return fig

def create_mri_component_breakdown(df, output_path):
    """Create MRI component breakdown stacked chart"""
    print(f"\n📊 Creating MRI component breakdown chart...")

    # Apply styling
    apply_institutional_styling()

    # Get components
    components = {
        'LFI (Labor Fragility)': 'MRI_LFI_Component',
        '-LDI (Labor Dynamism)': 'MRI_LDI_Component',
        'YFS (Funding Stress)': 'MRI_YFS_Component',
        'Credit (HY OAS)': 'MRI_Credit_Component',
        'EMD (Equity Momentum)': 'MRI_EMD_Component',
        '-LCI (Liquidity Cushion)': 'MRI_LCI_Component',
    }

    # Create figure with two panels
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12),
                                    gridspec_kw={'height_ratios': [2, 1]})

    # Top panel: Stacked area of components
    comp_data = pd.DataFrame()
    for label, col in components.items():
        if col in df.columns:
            comp_data[label] = df[col].fillna(0)

    # Plot stacked area
    ax1.stackplot(df.index,
                 *[comp_data[col] for col in comp_data.columns],
                 labels=comp_data.columns,
                 alpha=0.7,
                 colors=['#CC0000', '#FF6666', '#FF9900', '#FFCC00', '#0066CC', '#003366'])

    # Overlay total MRI
    ax1.plot(df.index, df['MRI'],
            color='black', linewidth=3, label='Total MRI', zorder=10)

    ax1.axhline(y=0, color='gray', linestyle='-', linewidth=1)
    ax1.axhline(y=1, color='red', linestyle='--', linewidth=1, alpha=0.5)
    ax1.axhline(y=2, color='red', linestyle='--', linewidth=1, alpha=0.5)

    ax1.set_title('MRI Component Breakdown: Contribution Analysis',
                 fontsize=16, fontweight='bold', loc='left', pad=15)
    ax1.set_ylabel('Contribution (σ)', fontsize=12, fontweight='bold')
    ax1.legend(loc='upper left', ncol=2, frameon=True, shadow=True)
    ax1.grid(True, alpha=0.3)

    # Bottom panel: MRI line chart (simplified)
    ax2.plot(df.index, df['MRI'], color=COLORS['primary'], linewidth=2.5)
    ax2.fill_between(df.index, 0, df['MRI'],
                    where=(df['MRI'] > 0),
                    alpha=0.2, color=COLORS['negative'])
    ax2.fill_between(df.index, 0, df['MRI'],
                    where=(df['MRI'] < 0),
                    alpha=0.2, color=COLORS['positive'])

    ax2.axhline(y=0, color='gray', linestyle='-', linewidth=1)
    ax2.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax2.set_ylabel('MRI (σ)', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    # Format dates
    for ax in [ax1, ax2]:
        ax.xaxis.set_major_locator(mdates.YearLocator(2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Component breakdown saved: {output_path}")

    plt.close()

def main():
    """Generate flagship MRI chart"""
    import os

    # Create charts directory if it doesn't exist
    os.makedirs('/Users/bob/lighthouse_paywall_deck/charts', exist_ok=True)
    os.makedirs('/Users/bob/lighthouse_paywall_deck/charts/proprietary', exist_ok=True)

    # Generate MRI chart
    create_mri_chart(
        indicators_path='/Users/bob/lighthouse_paywall_deck/proprietary_indicators.csv',
        output_path='/Users/bob/lighthouse_paywall_deck/charts/proprietary/MRI_Macro_Risk_Index.png'
    )

    print("\n" + "=" * 70)
    print("✓ FLAGSHIP CHART GENERATION COMPLETE")
    print("=" * 70)
    print("\nFiles created:")
    print("  • MRI_Macro_Risk_Index.png (main chart)")
    print("  • MRI_Macro_Risk_Index_components.png (breakdown)")
    print("\nReady for chartbook! 🎨")

if __name__ == "__main__":
    main()
