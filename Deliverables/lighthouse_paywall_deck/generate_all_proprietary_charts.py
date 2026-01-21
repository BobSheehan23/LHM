"""
LIGHTHOUSE MACRO - ALL PROPRIETARY CHARTS GENERATOR
Batch-generates all 25+ proprietary indicator charts with institutional styling

Author: Bob Sheehan, CFA, CMT
Date: November 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

# Lighthouse Macro color palette
COLORS = {
    'primary': '#003366',
    'secondary': '#0066CC',
    'accent': '#FF9900',
    'positive': '#00A86B',
    'negative': '#CC0000',
    'neutral': '#808080',
    'background': '#FFFFFF',
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

class ChartGenerator:
    """Generate all proprietary indicator charts"""

    def __init__(self, indicators_path, master_data_path, output_dir):
        self.indicators = pd.read_csv(indicators_path, index_col=0, parse_dates=True)
        self.master = pd.read_csv(master_data_path, index_col=0, parse_dates=True)
        self.output_dir = output_dir

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        apply_institutional_styling()

    def add_watermark(self, ax):
        """Add Lighthouse Macro watermark"""
        ax.text(0.5, 0.5, 'LIGHTHOUSE MACRO',
               transform=ax.transAxes,
               fontsize=60, color=COLORS['neutral'],
               alpha=0.05, ha='center', va='center',
               rotation=30, zorder=1)

    def add_source_footer(self, ax, formula=None):
        """Add source and formula footer"""
        source_text = f"Source: Lighthouse Macro | Bob Sheehan, CFA, CMT\nUpdated: {datetime.now().strftime('%B %d, %Y')}"

        ax.text(0.98, 0.02, source_text,
               transform=ax.transAxes, fontsize=8,
               color=COLORS['neutral'], va='bottom', ha='right')

        if formula:
            ax.text(0.02, 0.02, f"Formula: {formula}",
                   transform=ax.transAxes, fontsize=9,
                   style='italic', color=COLORS['neutral'],
                   va='bottom', ha='left')

    def create_single_indicator_chart(self, indicator_col, title, ylabel,
                                      thresholds=None, interpretation=None,
                                      formula=None, output_name=None, inverted=False):
        """Generic single-indicator chart with threshold bands

        inverted: If True, flip colors (red for low, green for high) - use for LDI, LCI
        """

        if indicator_col not in self.indicators.columns:
            print(f"  ⚠ Skipping {indicator_col} - not found in indicators")
            return None

        df = self.indicators[self.indicators[indicator_col].notna()].copy()

        if len(df) == 0:
            print(f"  ⚠ Skipping {indicator_col} - no data")
            return None

        fig, ax = plt.subplots(figsize=(16, 9))

        # Determine colors based on inverted flag
        positive_color = COLORS['negative'] if inverted else COLORS['positive']
        negative_color = COLORS['positive'] if inverted else COLORS['negative']

        # Main line (smooth with interpolation='monotonic' if supported)
        ax.plot(df.index, df[indicator_col],
               color=COLORS['primary'], linewidth=2.5,
               label=title, zorder=5, antialiased=True)

        # Fill regions
        ax.fill_between(df.index, 0, df[indicator_col],
                       where=(df[indicator_col] > 0),
                       alpha=0.15, color=negative_color,
                       label='Elevated/Stress' if not inverted else 'Strong/Healthy', zorder=2)

        ax.fill_between(df.index, 0, df[indicator_col],
                       where=(df[indicator_col] < 0),
                       alpha=0.15, color=positive_color,
                       label='Below Average/Benign' if not inverted else 'Weak/Fragile', zorder=2)

        # Zero line
        ax.axhline(y=0, color=COLORS['neutral'], linestyle='-',
                  linewidth=1.5, label='Neutral', zorder=3)

        # Threshold bands (respect inverted coloring)
        if thresholds:
            for level, label in thresholds.items():
                band_color = negative_color if level > 0 else positive_color
                ax.axhline(y=level, color=band_color,
                          linestyle='--', linewidth=1.5, alpha=0.7,
                          label=label, zorder=3)
        else:
            # Default ±1σ, ±2σ
            ax.axhline(y=1, color=negative_color, linestyle='--',
                      linewidth=1.5, alpha=0.7, label='+1σ', zorder=3)
            ax.axhline(y=2, color=negative_color, linestyle='--',
                      linewidth=1.5, alpha=0.7, label='+2σ', zorder=3)
            ax.axhline(y=-1, color=positive_color, linestyle='--',
                      linewidth=1.5, alpha=0.7, label='-1σ', zorder=3)

        # Latest value on right y-axis (TradingView style)
        latest_val = df[indicator_col].iloc[-1]

        # Horizontal line at latest value
        ax.axhline(latest_val, color=COLORS['primary'], linewidth=1,
                  linestyle='--', alpha=0.3, xmax=0.99)

        # Latest value label on right axis
        ax.text(1.01, latest_val, f'{latest_val:+.2f}σ',
               transform=ax.get_yaxis_transform(),
               fontsize=11, fontweight='bold',
               color='white',
               va='center', ha='left',
               bbox=dict(boxstyle='round,pad=0.4',
                        facecolor=COLORS['negative'] if latest_val > 1 else COLORS['primary'],
                        edgecolor='none', alpha=0.95))

        # Interpretation box
        if interpretation:
            ax.text(0.02, 0.98, interpretation,
                   transform=ax.transAxes, fontsize=11,
                   va='top', ha='left',
                   bbox=dict(boxstyle='round,pad=0.8', facecolor='white',
                            edgecolor=COLORS['primary'], linewidth=2, alpha=0.95))

        # Title and labels
        ax.set_title(f"Lighthouse Macro: {title}",
                    fontsize=18, fontweight='bold',
                    loc='left', pad=20, color=COLORS['primary'])

        ax.set_xlabel('Date', fontsize=13, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=13, fontweight='bold')

        # Format x-axis
        ax.xaxis.set_major_locator(mdates.YearLocator(2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax.xaxis.set_minor_locator(mdates.YearLocator(1))

        # Legend - top right to avoid covering indicator name
        ax.legend(loc='upper right', frameon=True, shadow=True,
                 fancybox=True, framealpha=0.95)

        # No gridlines (TradingView style)
        ax.grid(False)

        # All 4 spines visible (box around chart)
        for spine in ['top', 'right', 'bottom', 'left']:
            ax.spines[spine].set_visible(True)
            ax.spines[spine].set_color('#333333')
            ax.spines[spine].set_linewidth(1)

        # TradingView-style spacing: data to left edge, space on right
        ax.set_xlim(left=df.index[0], right=df.index[-1] + pd.Timedelta(days=len(df)*0.02))
        ax.margins(y=0.05)

        # Add watermark and footer
        self.add_watermark(ax)
        self.add_source_footer(ax, formula=formula)

        # Save
        output_path = f"{self.output_dir}/{output_name or indicator_col}.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        return output_path

    def create_dual_axis_chart(self, series1_col, series2_col, title,
                               ylabel1, ylabel2, output_name,
                               series1_label=None, series2_label=None,
                               formula=None):
        """Dual-axis chart for divergence analysis"""

        # Get data from master (for raw series)
        if series1_col in self.master.columns and series2_col in self.master.columns:
            df = self.master[[series1_col, series2_col]].dropna()
        else:
            print(f"  ⚠ Skipping {output_name} - series not found")
            return None

        if len(df) == 0:
            return None

        fig, ax2 = plt.subplots(figsize=(16, 9))

        # Right axis is PRIMARY (TradingView style)
        color2 = COLORS['accent']
        ax2.plot(df.index, df[series2_col],
                color=color2, linewidth=2.5,
                label=series2_label or series2_col)

        ax2.set_xlabel('Date', fontsize=13, fontweight='bold')
        ax2.set_ylabel(ylabel2, fontsize=13, fontweight='bold', color=color2)
        ax2.tick_params(axis='y', labelcolor=color2)
        ax2.yaxis.set_label_position("right")
        ax2.yaxis.tick_right()

        # Left axis is SECONDARY
        ax1 = ax2.twinx()
        color1 = COLORS['primary']
        ax1.plot(df.index, df[series1_col],
                color=color1, linewidth=2.5, linestyle='--',
                label=series1_label or series1_col)

        ax1.set_ylabel(ylabel1, fontsize=13, fontweight='bold', color=color1)
        ax1.tick_params(axis='y', labelcolor=color1)
        ax1.yaxis.set_label_position("left")
        ax1.yaxis.tick_left()

        # Combined legend
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2,
                  loc='upper right', frameon=True, shadow=True)

        # Title
        ax2.set_title(f"Lighthouse Macro: {title}",
                     fontsize=18, fontweight='bold',
                     loc='left', pad=20, color=COLORS['primary'])

        # No gridlines (TradingView style)
        ax1.grid(False)
        ax2.grid(False)

        # All 4 spines visible
        for spine in ['top', 'right', 'bottom', 'left']:
            ax2.spines[spine].set_visible(True)
            ax2.spines[spine].set_color('#333333')
            ax2.spines[spine].set_linewidth(1)

        # TradingView-style spacing: data to left edge, space on right
        ax2.set_xlim(left=df.index[0], right=df.index[-1] + pd.Timedelta(days=len(df)*0.02))
        ax2.margins(y=0.05)

        # Watermark and footer
        self.add_watermark(ax2)
        self.add_source_footer(ax2, formula=formula)

        # Save
        output_path = f"{self.output_dir}/{output_name}.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        return output_path

    def generate_all_charts(self):
        """Generate all 25 proprietary charts"""

        print("=" * 70)
        print("GENERATING ALL PROPRIETARY INDICATOR CHARTS")
        print("=" * 70)

        charts_generated = []

        # 1. Liquidity Cushion Index (LCI) - INVERTED COLORING
        print("\n[1/25] Liquidity Cushion Index (LCI)...")
        path = self.create_single_indicator_chart(
            'LCI',
            'Liquidity Cushion Index (LCI)',
            'Standard Deviations (σ)',
            interpretation='High LCI = Ample liquidity\nLow LCI = Constrained liquidity\nCurrent <-1σ = Critical constraint',
            formula='LCI = z(RRP/GDP) + z(Reserves/GDP) / 2',
            output_name='01_LCI_Liquidity_Cushion_Index',
            inverted=True  # Red for low (bad), green for high (good)
        )
        if path: charts_generated.append(path)

        # 2. Labor Fragility Index (LFI)
        print("[2/25] Labor Fragility Index (LFI)...")
        path = self.create_single_indicator_chart(
            'LFI',
            'Labor Fragility Index (LFI)',
            'Standard Deviations (σ)',
            interpretation='High LFI = Labor market stress\nLow LFI = Healthy labor market\nLeads payroll weakness by 2-3 quarters',
            formula='LFI = z(LongUnemployment) + z(-Quits) + z(-Hires/Quits) / 3',
            output_name='02_LFI_Labor_Fragility_Index'
        )
        if path: charts_generated.append(path)

        # 3. Labor Dynamism Index (LDI) - INVERTED COLORING
        print("[3/25] Labor Dynamism Index (LDI)...")
        path = self.create_single_indicator_chart(
            'LDI',
            'Labor Dynamism Index (LDI)',
            'Standard Deviations (σ)',
            interpretation='High LDI = Worker confidence\nLow LDI = Reduced optionality\nLeads payrolls by 2-3 quarters',
            formula='LDI = z(Quits) + z(Hires/Quits) + z(Quits/Layoffs) / 3',
            output_name='03_LDI_Labor_Dynamism_Index',
            inverted=True  # Red for low (bad), green for high (good)
        )
        if path: charts_generated.append(path)

        # 4. Credit-Labor Gap (CLG)
        print("[4/25] Credit-Labor Gap (CLG)...")
        path = self.create_single_indicator_chart(
            'CLG',
            'Credit-Labor Gap (CLG)',
            'Standard Deviations (σ)',
            thresholds={0: 'Fair Pricing'},
            interpretation='CLG < 0 = Spreads too tight given labor stress\nCLG > 0 = Fair credit pricing\nNegative gap = Pre-widening setup',
            formula='CLG = z(HY OAS) - z(LFI)',
            output_name='04_CLG_Credit_Labor_Gap'
        )
        if path: charts_generated.append(path)

        # 5. Yield-Funding Stress (YFS)
        print("[5/25] Yield-Funding Stress (YFS)...")
        path = self.create_single_indicator_chart(
            'YFS',
            'Yield-Funding Stress (YFS)',
            'Standard Deviations (σ)',
            interpretation='High YFS = Curve inversion + stress\nLow YFS = Steep curve, smooth plumbing\nSensitive in low-cushion world',
            formula='YFS = z(10Y-2Y) + z(10Y-3M) + z(BGCR-EFFR) / 3',
            output_name='05_YFS_Yield_Funding_Stress'
        )
        if path: charts_generated.append(path)

        # 6. Spread-Volatility Imbalance (SVI)
        print("[6/25] Spread-Volatility Imbalance (SVI)...")
        path = self.create_single_indicator_chart(
            'SVI',
            'Spread-Volatility Imbalance (SVI)',
            'Ratio',
            interpretation='Low SVI = Tight spreads + rising vol\n= Poor risk compensation\nLate-cycle mismatch rarely persists',
            formula='SVI = z(HY OAS Level) / z(HY OAS Volatility)',
            output_name='06_SVI_Spread_Volatility_Imbalance'
        )
        if path: charts_generated.append(path)

        # 7. Equity Momentum Divergence (EMD)
        print("[7/25] Equity Momentum Divergence (EMD)...")
        path = self.create_single_indicator_chart(
            'EMD',
            'Equity Momentum Divergence (EMD)',
            'Standard Deviations (σ)',
            interpretation='EMD >+1σ = Stretched momentum\nThin shock absorption\nProne to air pockets',
            formula='EMD = z((SP500 - MA200) / Realized Vol)',
            output_name='07_EMD_Equity_Momentum_Divergence'
        )
        if path: charts_generated.append(path)

        # 8. Bill-SOFR Spread
        print("[8/25] 3M Bill-SOFR Spread...")
        path = self.create_single_indicator_chart(
            'Bill_SOFR_Spread',
            '3-Month Bill-SOFR Spread',
            'Basis Points',
            interpretation='Positive spread = Bills trading rich\nDriven by stablecoin demand\nVolatility = collateral stress',
            formula='Spread = 3M T-Bill Rate - SOFR',
            output_name='08_Bill_SOFR_Spread'
        )
        if path: charts_generated.append(path)

        # 9-10. Payrolls vs Quits Divergence (dual-axis)
        print("[9/25] Payrolls vs Quits Rate Divergence...")
        path = self.create_dual_axis_chart(
            'Total_Nonfarm_Payrolls', 'Quits',
            'Payroll Growth vs Quits Rate Divergence',
            'Nonfarm Payrolls (000s)', 'Quits (000s)',
            '09_Payrolls_vs_Quits_Divergence',
            series1_label='Nonfarm Payrolls',
            series2_label='Quits Rate',
            formula='Divergence shows when workers stop quitting despite job growth'
        )
        if path: charts_generated.append(path)

        # 10. Hours vs Employment (dual-axis)
        print("[10/25] Hours Worked vs Employment Divergence...")
        path = self.create_dual_axis_chart(
            'Total_Hours_Worked', 'Total_Nonfarm_Payrolls',
            'Hours Worked vs Employment Divergence',
            'Aggregate Hours Index', 'Payrolls (000s)',
            '10_Hours_vs_Employment_Divergence',
            series1_label='Total Hours',
            series2_label='Employment',
            formula='Hours YoY < Employment YoY = Layoffs coming'
        )
        if path: charts_generated.append(path)

        # 11-15. Component charts for MRI
        print("[11/25] LCI Components...")
        self._create_component_chart('LCI',
            ['LCI_RRP_Component', 'LCI_Reserves_Component'],
            'Liquidity Cushion Index - Components',
            '11_LCI_Components')

        print("[12/25] LFI Components...")
        self._create_component_chart('LFI',
            ['LFI_LongUnemployment', 'LFI_Quits', 'LFI_HiresQuits'],
            'Labor Fragility Index - Components',
            '12_LFI_Components')

        print("[13/25] LDI Components...")
        self._create_component_chart('LDI',
            ['LDI_Quits', 'LDI_HiresQuits', 'LDI_QuitsLayoffs'],
            'Labor Dynamism Index - Components',
            '13_LDI_Components')

        print("[14/25] YFS Components...")
        self._create_component_chart('YFS',
            ['YFS_10Y2Y_Component', 'YFS_10Y3M_Component'],
            'Yield-Funding Stress - Components',
            '14_YFS_Components')

        print("[15/25] CLG Components...")
        self._create_component_chart('CLG',
            ['CLG_HY_Component', 'CLG_LFI_Component'],
            'Credit-Labor Gap - Components',
            '15_CLG_Components')

        # 16-20. Additional raw data visualizations
        print("[16/25] HY OAS Timeline...")
        path = self._create_raw_data_chart('HY_OAS',
            'High-Yield OAS Timeline',
            'Basis Points',
            '16_HY_OAS_Timeline',
            thresholds={300: 'Tight', 500: 'Normal', 800: 'Wide'})
        if path: charts_generated.append(path)

        print("[17/25] VIX Timeline...")
        path = self._create_raw_data_chart('VIX',
            'VIX - Market Volatility Index',
            'VIX Level',
            '17_VIX_Timeline',
            thresholds={15: 'Low Vol', 20: 'Elevated', 30: 'High Stress'})
        if path: charts_generated.append(path)

        print("[18/25] Unemployment Rate...")
        path = self._create_raw_data_chart('Unemployment_Rate',
            'Unemployment Rate',
            'Percent',
            '18_Unemployment_Rate',
            thresholds={4: 'Low', 5: 'Moderate', 6: 'Elevated'})
        if path: charts_generated.append(path)

        print("[19/25] Job Openings...")
        path = self._create_raw_data_chart('Job_Openings',
            'Job Openings (JOLTS)',
            'Thousands',
            '19_Job_Openings')
        if path: charts_generated.append(path)

        print("[20/25] Fed Funds Rate...")
        path = self._create_raw_data_chart('Fed_Funds_Rate',
            'Federal Funds Effective Rate',
            'Percent',
            '20_Fed_Funds_Rate')
        if path: charts_generated.append(path)

        # 21-25. Supporting calculations
        print("[21/25] Credit Growth YoY...")
        path = self._create_supporting_chart('Credit_Growth_YoY',
            'Bank Credit Growth (YoY %)',
            '21_Credit_Growth_YoY')
        if path: charts_generated.append(path)

        print("[22/25] Payrolls YoY...")
        path = self._create_supporting_chart('Payrolls_YoY',
            'Nonfarm Payrolls Growth (YoY %)',
            '22_Payrolls_YoY')
        if path: charts_generated.append(path)

        print("[23/25] Hours YoY...")
        path = self._create_supporting_chart('Hours_YoY',
            'Aggregate Hours Growth (YoY %)',
            '23_Hours_YoY')
        if path: charts_generated.append(path)

        print("[24/25] Hours-Employment Divergence...")
        path = self._create_supporting_chart('Hours_Employment_Divergence',
            'Hours vs Employment Divergence (pp)',
            '24_Hours_Employment_Divergence')
        if path: charts_generated.append(path)

        print("[25/25] Yield Curve 10Y-2Y...")
        path = self._create_raw_data_chart('Yield_Curve_10Y2Y',
            'Treasury Yield Curve: 10Y-2Y Spread',
            'Basis Points',
            '25_Yield_Curve_10Y2Y',
            thresholds={0: 'Inversion Threshold'})
        if path: charts_generated.append(path)

        print("\n" + "=" * 70)
        print("✓ CHART GENERATION COMPLETE")
        print("=" * 70)
        print(f"\nTotal charts generated: {len(charts_generated)}")

        return charts_generated

    def _create_component_chart(self, main_indicator, components, title, output_name):
        """Create component breakdown chart"""
        available_components = [c for c in components if c in self.indicators.columns]

        if not available_components:
            return None

        fig, ax = plt.subplots(figsize=(16, 9))

        for comp in available_components:
            df = self.indicators[self.indicators[comp].notna()]
            ax.plot(df.index, df[comp], linewidth=2, label=comp.split('_')[-1])

        # Plot main indicator
        if main_indicator in self.indicators.columns:
            df = self.indicators[self.indicators[main_indicator].notna()]
            ax.plot(df.index, df[main_indicator],
                   linewidth=3, color='black', label=f'Total {main_indicator}', zorder=10)

        ax.axhline(y=0, color='gray', linestyle='-', linewidth=1)
        ax.set_title(f"Lighthouse Macro: {title}", fontsize=18, fontweight='bold',
                    loc='left', pad=20, color=COLORS['primary'])
        ax.set_xlabel('Date', fontsize=13, fontweight='bold')
        ax.set_ylabel('Standard Deviations (σ)', fontsize=13, fontweight='bold')
        ax.legend(loc='best', frameon=True, shadow=True)
        ax.grid(True, alpha=0.3)

        self.add_watermark(ax)
        self.add_source_footer(ax)

        output_path = f"{self.output_dir}/{output_name}.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        return output_path

    def _create_raw_data_chart(self, series_col, title, ylabel, output_name, thresholds=None):
        """Create chart for raw data series"""
        if series_col not in self.master.columns:
            return None

        df = self.master[self.master[series_col].notna()]

        if len(df) == 0:
            return None

        fig, ax = plt.subplots(figsize=(16, 9))

        ax.plot(df.index, df[series_col],
               color=COLORS['primary'], linewidth=2.5)

        if thresholds:
            for level, label in thresholds.items():
                ax.axhline(y=level, linestyle='--', linewidth=1.5,
                          alpha=0.7, label=label)

        ax.set_title(f"Lighthouse Macro: {title}",
                    fontsize=18, fontweight='bold',
                    loc='left', pad=20, color=COLORS['primary'])
        ax.set_xlabel('Date', fontsize=13, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=13, fontweight='bold')
        ax.legend(loc='best', frameon=True, shadow=True)
        ax.grid(True, alpha=0.3)

        self.add_watermark(ax)
        self.add_source_footer(ax)

        output_path = f"{self.output_dir}/{output_name}.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        return output_path

    def _create_supporting_chart(self, indicator_col, title, output_name):
        """Create chart for supporting calculation"""
        if indicator_col not in self.indicators.columns:
            return None

        df = self.indicators[self.indicators[indicator_col].notna()]

        if len(df) == 0:
            return None

        fig, ax = plt.subplots(figsize=(16, 9))

        ax.plot(df.index, df[indicator_col],
               color=COLORS['primary'], linewidth=2.5)
        ax.axhline(y=0, color='gray', linestyle='-', linewidth=1)

        ax.set_title(f"Lighthouse Macro: {title}",
                    fontsize=18, fontweight='bold',
                    loc='left', pad=20, color=COLORS['primary'])
        ax.set_xlabel('Date', fontsize=13, fontweight='bold')
        ax.set_ylabel(title, fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)

        self.add_watermark(ax)
        self.add_source_footer(ax)

        output_path = f"{self.output_dir}/{output_name}.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        return output_path


def main():
    """Generate all proprietary charts"""

    base_path = '/Users/bob/lighthouse_paywall_deck'

    generator = ChartGenerator(
        indicators_path=f'{base_path}/proprietary_indicators.csv',
        master_data_path=f'{base_path}/chartbook_master_data.csv',
        output_dir=f'{base_path}/charts/proprietary'
    )

    charts = generator.generate_all_charts()

    print(f"\n✓ All charts saved to: {base_path}/charts/proprietary/")
    print(f"✓ Total files created: {len(charts)}")
    print("\nReady for chartbook assembly! 📊")


if __name__ == "__main__":
    main()
