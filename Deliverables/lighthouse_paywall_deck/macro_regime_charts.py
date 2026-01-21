"""
Lighthouse Macro - Section 1: Macro Regime Charts (Charts 1-10)
Next-generation chartbook with corrected styling
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from lighthouse_style import (
    COLORS,
    create_single_axis_chart,
    create_dual_axis_chart,
    add_last_value_label,
    enforce_no_gridlines
)
from data_sources import DataOrchestrator

# Initialize data orchestrator
data = DataOrchestrator()


def chart_01_economic_cycle_scatter():
    """
    Chart 1: Economic Cycle Positioning
    Growth vs Inflation quadrant analysis
    """
    fig, ax = create_single_axis_chart(
        chart_number=1,
        title='Economic Cycle Positioning: Growth vs Inflation',
        ylabel='PCE Inflation (% YoY)',
        source='FRED'
    )
    ax.set_xlabel('Real GDP Growth (%)', fontsize=11, fontweight='bold')

    # Fetch data
    gdp_growth = data.safe_fetch_fred('A191RL1Q225SBEA', '2015-01-01')  # Real GDP Growth (Quarterly)
    pce_inflation = data.safe_fetch_fred('PCEPI', '2015-01-01')  # PCE Price Index

    if gdp_growth is None or pce_inflation is None or len(gdp_growth) == 0 or len(pce_inflation) == 0:
        ax.text(0.5, 0.5, 'Data temporarily unavailable',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=14, color=COLORS['neutral'])
        plt.tight_layout()
        return fig

    # Calculate YoY inflation
    inflation = pce_inflation.pct_change(12) * 100

    # Align quarterly GDP with monthly inflation (take quarterly endpoints)
    df = pd.DataFrame({'growth': gdp_growth, 'inflation': inflation}).dropna()

    if len(df) > 10:
        # Scatter with time gradient
        dates_numeric = np.arange(len(df))
        scatter = ax.scatter(df['growth'], df['inflation'],
                           c=dates_numeric, cmap='coolwarm',
                           s=80, alpha=0.6, edgecolors=COLORS['neutral'], linewidths=0.5)

        # Quadrant lines (2% thresholds)
        ax.axhline(y=2.0, color=COLORS['neutral'], linestyle='--', linewidth=1, alpha=0.4, zorder=1)
        ax.axvline(x=2.0, color=COLORS['neutral'], linestyle='--', linewidth=1, alpha=0.4, zorder=1)

        # Latest point (prominent)
        ax.scatter(df['growth'].iloc[-1], df['inflation'].iloc[-1],
                  s=250, color=COLORS['orange'], edgecolors=COLORS['ocean_blue'],
                  linewidths=2.5, zorder=10, marker='*', label='Current')

        # Quadrant labels (subtle)
        ax.text(0.05, 0.95, 'High Inflation\nLow Growth',
                transform=ax.transAxes, ha='left', va='top',
                fontsize=8, color=COLORS['neutral'], style='italic', alpha=0.7)
        ax.text(0.95, 0.95, 'High Inflation\nHigh Growth',
                transform=ax.transAxes, ha='right', va='top',
                fontsize=8, color=COLORS['neutral'], style='italic', alpha=0.7)
        ax.text(0.05, 0.05, 'Low Inflation\nLow Growth',
                transform=ax.transAxes, ha='left', va='bottom',
                fontsize=8, color=COLORS['neutral'], style='italic', alpha=0.7)
        ax.text(0.95, 0.05, 'Goldilocks\n(Low Infl, High Growth)',
                transform=ax.transAxes, ha='right', va='bottom',
                fontsize=8, color=COLORS['ocean_blue'], style='italic', alpha=0.7)

        ax.legend(loc='upper left', fontsize=9, framealpha=0.95)

    plt.tight_layout()
    return fig


def chart_02_phillips_curve():
    """
    Chart 2: Phillips Curve
    Unemployment vs Core Inflation relationship
    """
    fig, ax = create_single_axis_chart(
        chart_number=2,
        title='Phillips Curve: Unemployment vs Core Inflation',
        ylabel='Core PCE Inflation (% YoY)',
        source='FRED'
    )
    ax.set_xlabel('Unemployment Rate (%)', fontsize=11, fontweight='bold')

    # Fetch data
    unemployment = data.safe_fetch_fred('UNRATE', '2015-01-01')
    core_pce = data.safe_fetch_fred('PCEPILFE', '2015-01-01')  # Core PCE

    if unemployment is None or core_pce is None:
        ax.text(0.5, 0.5, 'Data temporarily unavailable',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=14, color=COLORS['neutral'])
        plt.tight_layout()
        return fig

    # Calculate YoY inflation
    inflation = core_pce.pct_change(12) * 100

    # Align data
    df = pd.DataFrame({'unemployment': unemployment, 'inflation': inflation}).dropna()

    if len(df) > 10:
        # Scatter with time gradient
        dates_numeric = np.arange(len(df))
        scatter = ax.scatter(df['unemployment'], df['inflation'],
                           c=dates_numeric, cmap='viridis',
                           s=60, alpha=0.6, edgecolors=COLORS['neutral'], linewidths=0.5)

        # Latest point
        ax.scatter(df['unemployment'].iloc[-1], df['inflation'].iloc[-1],
                  s=250, color=COLORS['orange'], edgecolors=COLORS['ocean_blue'],
                  linewidths=2.5, zorder=10, marker='*', label='Current')

        # Fed targets (dashed lines)
        ax.axhline(y=2.0, color=COLORS['ocean_blue'], linestyle='--',
                  linewidth=1.5, alpha=0.5, label='Fed 2% Target')

        ax.legend(loc='upper left', fontsize=9, framealpha=0.95)

    plt.tight_layout()
    return fig


def chart_03_ism_composite():
    """
    Chart 3: ISM Manufacturing & Services
    Business cycle real-time indicators
    """
    fig, ax = create_single_axis_chart(
        chart_number=3,
        title='ISM Manufacturing & Services Composite',
        ylabel='ISM Index',
        source='FRED'
    )

    # Fetch data (last 5 years)
    start_date = (datetime.now() - timedelta(days=1825)).strftime('%Y-%m-%d')
    ism_mfg = data.safe_fetch_fred('NAPM', start_date)  # ISM Manufacturing PMI
    ism_svc = data.safe_fetch_fred('NMFCI', start_date)  # ISM Services (Non-Manufacturing)

    if ism_mfg is None or ism_svc is None:
        ax.text(0.5, 0.5, 'Data temporarily unavailable',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=14, color=COLORS['neutral'])
        plt.tight_layout()
        return fig

    # Plot both series
    ax.plot(ism_mfg.index, ism_mfg.values,
           color=COLORS['ocean_blue'], linewidth=2.5, label='ISM Manufacturing', zorder=3)
    ax.plot(ism_svc.index, ism_svc.values,
           color=COLORS['orange'], linewidth=2, label='ISM Services', zorder=2)

    # 50 expansion/contraction line
    ax.axhline(y=50, color=COLORS['neutral'], linestyle='--',
              linewidth=1.5, alpha=0.6, label='Expansion/Contraction (50)')

    # Shading for contraction
    ax.fill_between(ism_mfg.index, 50, ism_mfg.values,
                    where=(ism_mfg.values < 50),
                    color=COLORS['orange'], alpha=0.15, zorder=1)

    # Last value labels
    add_last_value_label(ax, ism_mfg, COLORS['ocean_blue'], side='right', fmt='{:.1f}')
    add_last_value_label(ax, ism_svc, COLORS['orange'], side='right', fmt='{:.1f}')

    ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
    ax.set_ylim(bottom=30, top=70)

    plt.tight_layout()
    return fig


def chart_04_yield_curve():
    """
    Chart 4: Yield Curve
    2Y, 5Y, 10Y, 30Y Treasury yields
    """
    fig, ax = create_single_axis_chart(
        chart_number=4,
        title='Treasury Yield Curve: 2Y, 5Y, 10Y, 30Y',
        ylabel='Yield (%)',
        source='FRED'
    )

    # Fetch data (last 5 years)
    start_date = (datetime.now() - timedelta(days=1825)).strftime('%Y-%m-%d')
    y2 = data.safe_fetch_fred('DGS2', start_date)
    y5 = data.safe_fetch_fred('DGS5', start_date)
    y10 = data.safe_fetch_fred('DGS10', start_date)
    y30 = data.safe_fetch_fred('DGS30', start_date)

    if y2 is None or y10 is None:
        ax.text(0.5, 0.5, 'Data temporarily unavailable',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=14, color=COLORS['neutral'])
        plt.tight_layout()
        return fig

    # Plot all yields
    ax.plot(y2.index, y2.values,
           color=COLORS['carolina_blue'], linewidth=1.5, label='2Y', alpha=0.8)
    if y5 is not None:
        ax.plot(y5.index, y5.values,
               color=COLORS['neutral'], linewidth=1.5, label='5Y', alpha=0.7)
    ax.plot(y10.index, y10.values,
           color=COLORS['ocean_blue'], linewidth=2.5, label='10Y')
    if y30 is not None:
        ax.plot(y30.index, y30.values,
               color=COLORS['orange'], linewidth=2, label='30Y')

    # Last value labels
    add_last_value_label(ax, y2, COLORS['carolina_blue'], side='right')
    add_last_value_label(ax, y10, COLORS['ocean_blue'], side='right')

    ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    return fig


def chart_05_yield_curve_spreads():
    """
    Chart 5: Yield Curve Spreads
    10Y-2Y and 10Y-3M with recession shading
    """
    fig, ax = create_single_axis_chart(
        chart_number=5,
        title='Yield Curve Spreads: Inversion as Recession Predictor',
        ylabel='Spread (bps)',
        source='FRED'
    )

    # Fetch data (last 10 years for recession history)
    start_date = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')
    y10 = data.safe_fetch_fred('DGS10', start_date)
    y2 = data.safe_fetch_fred('DGS2', start_date)
    y3m = data.safe_fetch_fred('DGS3MO', start_date)

    if y10 is None or y2 is None:
        ax.text(0.5, 0.5, 'Data temporarily unavailable',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=14, color=COLORS['neutral'])
        plt.tight_layout()
        return fig

    # Calculate spreads in basis points
    df = pd.DataFrame({
        '10Y-2Y': (y10 - y2) * 100,
        '10Y-3M': (y10 - y3m) * 100 if y3m is not None else None
    }).dropna()

    # Plot spreads
    ax.plot(df.index, df['10Y-2Y'],
           color=COLORS['ocean_blue'], linewidth=2.5, label='10Y-2Y Spread')
    if '10Y-3M' in df.columns:
        ax.plot(df.index, df['10Y-3M'],
               color=COLORS['orange'], linewidth=2, label='10Y-3M Spread', alpha=0.8)

    # Zero line
    ax.axhline(y=0, color=COLORS['neutral'], linestyle='--', linewidth=1.5, alpha=0.6)

    # Shade inversion periods
    ax.fill_between(df.index, 0, df['10Y-2Y'],
                    where=(df['10Y-2Y'] < 0),
                    color=COLORS['orange'], alpha=0.2, label='Inversion Zone')

    # Last value labels
    add_last_value_label(ax, df['10Y-2Y'], COLORS['ocean_blue'], side='right', fmt='{:.0f}')

    ax.legend(loc='upper left', fontsize=9, framealpha=0.95)

    plt.tight_layout()
    return fig


def chart_06_inflation_components():
    """
    Chart 6: Inflation Components
    Headline CPI, Core CPI, and PCE
    """
    fig, ax = create_single_axis_chart(
        chart_number=6,
        title='Inflation Components: Headline vs Core',
        ylabel='Inflation (% YoY)',
        source='FRED'
    )

    # Fetch data (last 5 years)
    start_date = (datetime.now() - timedelta(days=1825)).strftime('%Y-%m-%d')
    cpi = data.safe_fetch_fred('CPIAUCSL', start_date)  # Headline CPI
    core_cpi = data.safe_fetch_fred('CPILFESL', start_date)  # Core CPI
    pce = data.safe_fetch_fred('PCEPI', start_date)  # PCE

    if cpi is None:
        ax.text(0.5, 0.5, 'Data temporarily unavailable',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=14, color=COLORS['neutral'])
        plt.tight_layout()
        return fig

    # Calculate YoY inflation
    headline_inflation = cpi.pct_change(12) * 100
    core_inflation = core_cpi.pct_change(12) * 100 if core_cpi is not None else None
    pce_inflation = pce.pct_change(12) * 100 if pce is not None else None

    # Plot
    ax.plot(headline_inflation.index, headline_inflation.values,
           color=COLORS['orange'], linewidth=2.5, label='Headline CPI')
    if core_inflation is not None:
        ax.plot(core_inflation.index, core_inflation.values,
               color=COLORS['ocean_blue'], linewidth=2.5, label='Core CPI')
    if pce_inflation is not None:
        ax.plot(pce_inflation.index, pce_inflation.values,
               color=COLORS['carolina_blue'], linewidth=2, label='PCE', alpha=0.8)

    # Fed 2% target
    ax.axhline(y=2.0, color=COLORS['neutral'], linestyle='--',
              linewidth=1.5, alpha=0.6, label='Fed 2% Target')

    # Last value labels
    add_last_value_label(ax, headline_inflation, COLORS['orange'], side='right')
    if core_inflation is not None:
        add_last_value_label(ax, core_inflation, COLORS['ocean_blue'], side='right')

    ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
    ax.set_ylim(bottom=-2)

    plt.tight_layout()
    return fig


def chart_07_fed_balance_sheet():
    """
    Chart 7: Fed Balance Sheet
    Total assets with QT tracking
    """
    fig, ax = create_single_axis_chart(
        chart_number=7,
        title='Federal Reserve Balance Sheet: QT in Progress',
        ylabel='Total Assets ($T)',
        source='FRED'
    )

    # Fetch data (last 10 years to show QE cycles)
    start_date = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')
    total_assets = data.safe_fetch_fred('WALCL', start_date)  # Fed total assets

    if total_assets is None:
        ax.text(0.5, 0.5, 'Data temporarily unavailable',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=14, color=COLORS['neutral'])
        plt.tight_layout()
        return fig

    # Convert to trillions
    assets_trillions = total_assets / 1000

    # Plot
    ax.plot(assets_trillions.index, assets_trillions.values,
           color=COLORS['ocean_blue'], linewidth=2.5, label='Fed Total Assets')
    ax.fill_between(assets_trillions.index, 0, assets_trillions.values,
                    color=COLORS['ocean_blue'], alpha=0.1)

    # Last value label
    add_last_value_label(ax, assets_trillions, COLORS['ocean_blue'], side='right', fmt='${:.1f}T')

    ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    return fig


def chart_08_cross_asset_correlation():
    """
    Chart 8: Cross-Asset Correlation Matrix
    SPY, TLT, GLD, DXY rolling correlations
    """
    fig, ax = create_single_axis_chart(
        chart_number=8,
        title='Cross-Asset Correlations: SPY-TLT 60-Day Rolling',
        ylabel='Correlation',
        source='FRED'
    )

    # Fetch data (last 2 years for correlation analysis)
    start_date = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
    spy = data.safe_fetch_fred('SP500', start_date)  # S&P 500
    # For bonds, use 10Y yield as proxy (inverse correlation to TLT)
    bond_yield = data.safe_fetch_fred('DGS10', start_date)

    if spy is None or bond_yield is None:
        ax.text(0.5, 0.5, 'Data temporarily unavailable',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=14, color=COLORS['neutral'])
        plt.tight_layout()
        return fig

    # Calculate returns
    spy_returns = spy.pct_change()
    bond_returns = bond_yield.diff()  # Yield changes (inverse to bond prices)

    # Rolling 60-day correlation
    df = pd.DataFrame({'spy': spy_returns, 'bonds': bond_returns}).dropna()
    rolling_corr = df['spy'].rolling(60).corr(df['bonds'])

    # Plot
    ax.plot(rolling_corr.index, rolling_corr.values,
           color=COLORS['ocean_blue'], linewidth=2.5, label='SPY-Bond Yield Correlation (60d)')

    # Zero line
    ax.axhline(y=0, color=COLORS['neutral'], linestyle='--', linewidth=1.5, alpha=0.6)

    # Shade positive/negative correlation
    ax.fill_between(rolling_corr.index, 0, rolling_corr.values,
                    where=(rolling_corr.values > 0),
                    color=COLORS['ocean_blue'], alpha=0.15, label='Risk-On (Positive Corr)')
    ax.fill_between(rolling_corr.index, 0, rolling_corr.values,
                    where=(rolling_corr.values < 0),
                    color=COLORS['orange'], alpha=0.15, label='Diversification (Negative Corr)')

    # Last value label
    add_last_value_label(ax, rolling_corr, COLORS['ocean_blue'], side='right', fmt='{:.2f}')

    ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
    ax.set_ylim(bottom=-1, top=1)

    plt.tight_layout()
    return fig


def chart_09_financial_stress_index():
    """
    Chart 9: OFR Financial Stress Index
    System-wide stress indicator
    """
    from ofr_data_readers import OFRDataReader

    fig, ax = create_single_axis_chart(
        chart_number=9,
        title='OFR Financial Stress Index: System-Wide Stress',
        ylabel='FSI (Std. Deviations)',
        source='OFR'
    )

    # Load OFR FSI data
    ofr = OFRDataReader()
    fsi = ofr.read_fsi()

    if fsi.empty or 'OFR FSI' not in fsi.columns:
        ax.text(0.5, 0.5, 'OFR FSI data not available',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=14, color=COLORS['neutral'])
        plt.tight_layout()
        return fig

    # Last 5 years
    recent_fsi = fsi[fsi.index >= (datetime.now() - timedelta(days=1825))]

    # Plot
    ax.plot(recent_fsi.index, recent_fsi['OFR FSI'],
           color=COLORS['ocean_blue'], linewidth=2.5, label='OFR FSI')

    # Zero line (normal conditions)
    ax.axhline(y=0, color=COLORS['neutral'], linestyle='--', linewidth=1.5, alpha=0.6)

    # Shade elevated stress periods
    ax.fill_between(recent_fsi.index, 0, recent_fsi['OFR FSI'],
                    where=(recent_fsi['OFR FSI'] > 0),
                    color=COLORS['orange'], alpha=0.2, label='Elevated Stress')

    # Last value label
    add_last_value_label(ax, recent_fsi['OFR FSI'], COLORS['ocean_blue'], side='right', fmt='{:.2f}')

    ax.legend(loc='upper left', fontsize=9, framealpha=0.95)

    plt.tight_layout()
    return fig


def chart_10_recession_probability():
    """
    Chart 10: Recession Probability Model
    Smoothed recession probabilities from yield curve
    """
    fig, ax = create_single_axis_chart(
        chart_number=10,
        title='Recession Probability: Yield Curve Model',
        ylabel='Probability (%)',
        source='FRED'
    )

    # Fetch recession probability series
    start_date = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')
    rec_prob = data.safe_fetch_fred('RECPROUSM156N', start_date)  # Smoothed recession probabilities

    if rec_prob is None:
        ax.text(0.5, 0.5, 'Data temporarily unavailable',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=14, color=COLORS['neutral'])
        plt.tight_layout()
        return fig

    # Plot
    ax.plot(rec_prob.index, rec_prob.values,
           color=COLORS['ocean_blue'], linewidth=2.5, label='Recession Probability')

    # Shade high-probability periods (>50%)
    ax.fill_between(rec_prob.index, 0, rec_prob.values,
                    where=(rec_prob.values > 50),
                    color=COLORS['orange'], alpha=0.3, label='High Probability (>50%)')

    # 50% threshold line
    ax.axhline(y=50, color=COLORS['neutral'], linestyle='--', linewidth=1.5, alpha=0.6)

    # Last value label
    add_last_value_label(ax, rec_prob, COLORS['ocean_blue'], side='right', fmt='{:.0f}%')

    ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
    ax.set_ylim(bottom=0, top=100)

    plt.tight_layout()
    return fig


# Section 1 complete: 10 macro regime charts with corrected Lighthouse styling
