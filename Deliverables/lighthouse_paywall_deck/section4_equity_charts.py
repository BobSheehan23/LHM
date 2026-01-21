"""
Lighthouse Macro - Section 4: Equity Positioning & Momentum (Charts 26-32)
PROPRIETARY INDICATORS: EMD (Equity Momentum Divergence), QUAL/SPY, MRI (Macro Risk Index)
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

# Initialize data
data = DataOrchestrator()


def calculate_z_score(series, window=None):
    """Calculate z-score for a series"""
    if window:
        mean = series.rolling(window).mean()
        std = series.rolling(window).std()
    else:
        mean = series.mean()
        std = series.std()
    return (series - mean) / std


def chart_26_equity_momentum_divergence():
    """
    Chart 26: Equity Momentum Divergence (EMD)
    PROPRIETARY: Distance from 200-day MA / Realized Volatility
    """
    fig, ax = create_single_axis_chart(
        chart_number=26,
        title='Equity Momentum Divergence (EMD): Volatility-Adjusted Overbought',
        ylabel='EMD (Z-Score)',
        source='FRED, Lighthouse Proprietary'
    )

    # Fetch S&P 500
    start_date = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')
    spx = data.safe_fetch_fred('SP500', start_date)

    if spx is not None and len(spx) > 0:
        # Calculate 200-day moving average
        ma_200 = spx.rolling(200).mean()

        # Calculate distance from 200-day MA (%)
        distance = ((spx - ma_200) / ma_200) * 100

        # Calculate realized volatility (30-day)
        returns = spx.pct_change()
        realized_vol = returns.rolling(30).std() * np.sqrt(252) * 100  # Annualized %

        # EMD = Distance / Volatility (volatility-adjusted momentum)
        df = pd.DataFrame({
            'distance': distance,
            'vol': realized_vol
        }).dropna()

        if len(df) > 0:
            df['EMD_raw'] = df['distance'] / df['vol']

            # Z-score the EMD
            df['EMD'] = calculate_z_score(df['EMD_raw'])

            # Plot EMD
            ax.plot(df.index, df['EMD'],
                   color=COLORS['ocean_blue'], linewidth=2.5, label='EMD')

            # Threshold bands
            ax.axhline(y=1, color=COLORS['orange'], linestyle='--',
                      linewidth=1.5, alpha=0.6, label='+1σ (Stretched)')
            ax.axhline(y=0, color=COLORS['neutral'], linestyle='-',
                      linewidth=1.5, alpha=0.6, label='Neutral')
            ax.axhline(y=-1, color=COLORS['ocean_blue'], linestyle='--',
                      linewidth=1.5, alpha=0.6, label='-1σ (Oversold)')

            # Shade stretched zone
            ax.fill_between(df.index, 1, df['EMD'],
                           where=(df['EMD'] > 1),
                           color=COLORS['orange'], alpha=0.2,
                           label='Stretched Momentum')

            add_last_value_label(ax, df['EMD'], COLORS['ocean_blue'],
                               side='right', fmt='{:.2f}σ')

            ax.legend(loc='upper right', fontsize=9, framealpha=0.95)
    else:
        ax.text(0.5, 0.5,
                'Equity Momentum Divergence (EMD)\n\n' +
                'PROPRIETARY INDICATOR\n\n' +
                'Formula: (Price - 200-day MA) / Realized Vol (Z-scored)\n\n' +
                'EMD > +1σ = "Stretched momentum with thin shock-absorption\n' +
                '—prone to air-pockets"',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=10, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_27_quality_vs_risk():
    """
    Chart 27: Quality vs Risk Ratio (QUAL/SPY)
    """
    fig, ax = create_single_axis_chart(
        chart_number=27,
        title='Quality vs Risk (QUAL/SPY): Market Preference Signal',
        ylabel='QUAL/SPY Price Ratio',
        source='TradingView (Manual Data Required)'
    )

    # This requires ETF price data - placeholder
    ax.text(0.5, 0.5,
            'Quality vs Risk Ratio (QUAL/SPY)\n\n' +
            'PROPRIETARY INDICATOR\n\n' +
            'Formula: iShares MSCI USA Quality ETF / S&P 500 ETF\n\n' +
            'Ratio declining = Risk-on, junk rally\n' +
            'Ratio rising = Flight to quality\n\n' +
            'Current Insight: "At cycle lows despite macro deterioration;\n' +
            'signals late-stage bull market behavior"\n\n' +
            'Data Source: TradingView export required',
            ha='center', va='center', transform=ax.transAxes,
            fontsize=10, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_28_macro_risk_index():
    """
    Chart 28: Macro Risk Index (MRI)
    PROPRIETARY COMPOSITE: LFI + (-LDI) + YFS + HY OAS + EMD + (-LCI)
    """
    fig, ax = create_single_axis_chart(
        chart_number=28,
        title='Macro Risk Index (MRI): Aggregate Cross-Asset Risk',
        ylabel='MRI (Z-Score Composite)',
        source='FRED, Lighthouse Proprietary'
    )

    # This requires all the components - simplified version
    start_date = (datetime.now() - timedelta(days=1825)).strftime('%Y-%m-%d')

    # Get key components that are easily available
    hy_oas = data.safe_fetch_fred('BAMLH0A0HYM2', start_date)
    vix = data.safe_fetch_fred('VIXCLS', start_date)
    unemployment = data.safe_fetch_fred('UNRATE', start_date)

    if hy_oas is not None and vix is not None and unemployment is not None:
        # Align data
        df = pd.DataFrame({
            'hy_oas': hy_oas,
            'vix': vix,
            'unemployment': unemployment
        }).dropna()

        if len(df) > 0:
            # Calculate z-scores (simplified MRI without full components)
            df['z_hy'] = calculate_z_score(df['hy_oas'])
            df['z_vix'] = calculate_z_score(df['vix'])
            df['z_unemp'] = calculate_z_score(df['unemployment'])

            # Simplified MRI (would include LFI, LDI, YFS, EMD, LCI in full version)
            df['MRI_simple'] = (df['z_hy'] + df['z_vix'] + df['z_unemp']) / 3

            # Plot MRI
            ax.plot(df.index, df['MRI_simple'],
                   color=COLORS['ocean_blue'], linewidth=2.5, label='MRI (Simplified)')

            # Threshold bands
            ax.axhline(y=2, color=COLORS['orange'], linestyle='-',
                      linewidth=2, alpha=0.8, label='+2σ (Crisis)')
            ax.axhline(y=1, color=COLORS['orange'], linestyle='--',
                      linewidth=1.5, alpha=0.6, label='+1σ (Elevated Risk)')
            ax.axhline(y=0, color=COLORS['neutral'], linestyle='-',
                      linewidth=1.5, alpha=0.6, label='Neutral')

            # Shade risk zones
            ax.fill_between(df.index, 1, df['MRI_simple'],
                           where=(df['MRI_simple'] > 1),
                           color=COLORS['orange'], alpha=0.2,
                           label='Elevated Risk Zone')

            add_last_value_label(ax, df['MRI_simple'], COLORS['ocean_blue'],
                               side='right', fmt='{:.2f}σ')

            ax.legend(loc='upper right', fontsize=9, framealpha=0.95)

            # Note about simplified version
            ax.text(0.02, 0.12,
                   'Note: Simplified MRI shown (HY OAS + VIX + Unemployment)\n' +
                   'Full version includes: LFI + (-LDI) + YFS + CSE + EMD + (-LCI)',
                   transform=ax.transAxes, fontsize=7, style='italic',
                   color=COLORS['neutral'], verticalalignment='top')
    else:
        ax.text(0.5, 0.5,
                'Macro Risk Index (MRI)\n\n' +
                'PROPRIETARY COMPOSITE INDICATOR\n\n' +
                'Formula: LFI + (-LDI) + YFS + Credit Spread + EMD + (-LCI)\n\n' +
                'MRI > +1σ = Elevated macro risk\n' +
                'MRI > +2σ = Crisis configuration\n\n' +
                '"Rising MRI while equities climb indicates\n' +
                'markets are under-pricing macro risk"',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=10, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_29_spx_tlt_correlation():
    """
    Chart 29: SPX vs Bond Correlation (60-Day Rolling)
    """
    # Use existing function from macro_regime_charts.py
    from macro_regime_charts import chart_08_cross_asset_correlation
    return chart_08_cross_asset_correlation()


def chart_30_vix_term_structure():
    """
    Chart 30: VIX (with term structure if available)
    """
    fig, ax = create_single_axis_chart(
        chart_number=30,
        title='VIX: Equity Market Volatility',
        ylabel='VIX Level',
        source='FRED'
    )

    # Fetch VIX (3 years)
    start_date = (datetime.now() - timedelta(days=1095)).strftime('%Y-%m-%d')
    vix = data.safe_fetch_fred('VIXCLS', start_date)

    if vix is not None and len(vix) > 0:
        # Plot VIX
        ax.plot(vix.index, vix.values,
               color=COLORS['ocean_blue'], linewidth=2.5, label='VIX')
        ax.fill_between(vix.index, 0, vix.values,
                       color=COLORS['ocean_blue'], alpha=0.1)

        # Threshold levels
        ax.axhline(y=20, color=COLORS['neutral'], linestyle='--',
                  linewidth=1.5, alpha=0.6, label='Elevated (20)')
        ax.axhline(y=30, color=COLORS['orange'], linestyle='--',
                  linewidth=1.5, alpha=0.6, label='High (30)')

        # Shade high volatility zone
        ax.fill_between(vix.index, 30, 100,
                       color=COLORS['orange'], alpha=0.1)

        add_last_value_label(ax, vix, COLORS['ocean_blue'],
                           side='right', fmt='{:.1f}')

        ax.legend(loc='upper right', fontsize=9, framealpha=0.95)
        ax.set_ylim(bottom=0)
    else:
        ax.text(0.5, 0.5, 'VIX data temporarily unavailable',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=11, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_31_sector_rotation():
    """
    Chart 31: Sector Rotation Heatmap (Placeholder)
    """
    fig, ax = create_single_axis_chart(
        chart_number=31,
        title='Sector Rotation: Cyclicals vs Defensives (Z-Score)',
        ylabel='Relative Performance (Z-Score)',
        source='FRED / Sector ETFs'
    )

    ax.text(0.5, 0.5,
            'Sector Rotation Heatmap\n\n' +
            '11 S&P Sectors:\n' +
            'Technology, Financials, Healthcare, Consumer Discretionary,\n' +
            'Industrials, Energy, Materials, Consumer Staples,\n' +
            'Utilities, Real Estate, Communication Services\n\n' +
            'Methodology: Relative performance z-scores\n' +
            'Cyclicals outperforming = Risk-on\n' +
            'Defensives outperforming = Risk-off\n\n' +
            'Data Source: Sector ETF prices (manual collection required)',
            ha='center', va='center', transform=ax.transAxes,
            fontsize=10, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_32_equity_risk_premium():
    """
    Chart 32: Equity Risk Premium (Earnings Yield - 10Y Treasury)
    """
    fig, ax = create_single_axis_chart(
        chart_number=32,
        title='Equity Risk Premium: S&P 500 Earnings Yield - 10Y Treasury',
        ylabel='Risk Premium (%)',
        source='FRED, S&P'
    )

    # Fetch 10Y Treasury
    start_date = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')
    t10y = data.safe_fetch_fred('DGS10', start_date)

    # S&P 500 earnings yield requires E/P ratio (inverse of P/E)
    # Not directly available in FRED - placeholder

    if t10y is not None:
        ax.text(0.5, 0.5,
                'Equity Risk Premium\n\n' +
                'Formula: S&P 500 Earnings Yield - 10Y Treasury Yield\n\n' +
                'High ERP (>4%) = Stocks cheap relative to bonds\n' +
                'Low ERP (<2%) = Stocks expensive, bond competition\n\n' +
                'Requires: S&P 500 earnings data\n' +
                '(Manual collection from S&P or Bloomberg)',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=10, color=COLORS['neutral'])
    else:
        ax.text(0.5, 0.5, 'Treasury data temporarily unavailable',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=11, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


# Section 4 complete: 7 equity positioning & momentum charts
# Proprietary indicators: EMD (Chart 26), QUAL/SPY (Chart 27), MRI (Chart 28)
# Charts 27, 31, 32 are placeholders requiring manual data
# Charts 26, 28, 29, 30 fully functional with FRED data
