"""
Lighthouse Macro - Section 2: Labor Markets (Charts 11-15)
Next-generation chartbook with corrected styling

Charts 11-13: Core labor market indicators
Charts 14-15: Extended analysis (to be added in Phase 4)
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


def chart_11_labor_market_heatmap():
    """
    Chart 11: Labor Market Heatmap
    Multi-dimensional z-score view of labor market health
    """
    fig, ax = create_single_axis_chart(
        chart_number=11,
        title='Labor Market Heatmap: Multi-Metric Z-Scores',
        ylabel='Z-Score (Std. Deviations)',
        source='FRED'
    )

    # Fetch labor market data (last 5 years for z-score calculation)
    start_date = (datetime.now() - timedelta(days=1825)).strftime('%Y-%m-%d')

    # Get key labor metrics
    unemployment = data.safe_fetch_fred('UNRATE', start_date)
    lfpr = data.safe_fetch_fred('CIVPART', start_date)  # Labor force participation
    emp_pop = data.safe_fetch_fred('EMRATIO', start_date)  # Employment-population ratio
    avg_hours = data.safe_fetch_fred('AWHAETP', start_date)  # Average weekly hours
    hourly_earnings = data.safe_fetch_fred('CES0500000003', start_date)  # Average hourly earnings

    # Calculate z-scores (standardized values)
    def calc_zscore(series):
        if series is None or len(series) == 0:
            return None
        return (series - series.mean()) / series.std()

    metrics = {}
    if unemployment is not None:
        metrics['Unemployment'] = calc_zscore(unemployment) * -1  # Invert (lower is better)
    if lfpr is not None:
        metrics['Labor Force Part.'] = calc_zscore(lfpr)
    if emp_pop is not None:
        metrics['Emp-Pop Ratio'] = calc_zscore(emp_pop)
    if avg_hours is not None:
        metrics['Avg Hours'] = calc_zscore(avg_hours)
    if hourly_earnings is not None:
        wage_growth = hourly_earnings.pct_change(12) * 100  # YoY growth
        metrics['Wage Growth'] = calc_zscore(wage_growth)

    if len(metrics) > 0:
        # Plot each metric
        colors_list = [COLORS['ocean_blue'], COLORS['orange'], COLORS['carolina_blue'],
                      COLORS['magenta'], COLORS['neutral']]

        for i, (name, series) in enumerate(metrics.items()):
            if series is not None:
                color = colors_list[i % len(colors_list)]
                ax.plot(series.index, series.values,
                       color=color, linewidth=2, label=name, alpha=0.8)

        # Zero line (average conditions)
        ax.axhline(y=0, color=COLORS['neutral'], linestyle='--', linewidth=1.5, alpha=0.6)

        # Shade strong/weak periods
        composite = pd.DataFrame(metrics).mean(axis=1)
        ax.fill_between(composite.index, 0, composite.values,
                       where=(composite.values > 0),
                       color=COLORS['ocean_blue'], alpha=0.1, label='Above Average')
        ax.fill_between(composite.index, 0, composite.values,
                       where=(composite.values < 0),
                       color=COLORS['orange'], alpha=0.1, label='Below Average')

        ax.legend(loc='upper left', fontsize=8, framealpha=0.95, ncol=2)
        ax.set_ylim(bottom=-3, top=3)

    else:
        ax.text(0.5, 0.5, 'Labor market data temporarily unavailable',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=14, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_12_jolts_indicators():
    """
    Chart 12: JOLTS Indicators
    Job openings, hires, and quits
    """
    fig, ax = create_single_axis_chart(
        chart_number=12,
        title='JOLTS Indicators: Openings, Hires, Quits',
        ylabel='Millions',
        source='FRED'
    )

    # Fetch JOLTS data (last 5 years)
    start_date = (datetime.now() - timedelta(days=1825)).strftime('%Y-%m-%d')

    openings = data.safe_fetch_fred('JTSJOL', start_date)  # Job openings
    hires = data.safe_fetch_fred('JTSHIL', start_date)  # Hires
    quits = data.safe_fetch_fred('JTSQUL', start_date)  # Quits

    if openings is not None and len(openings) > 0:
        # Convert to millions
        openings_millions = openings / 1000

        ax.plot(openings_millions.index, openings_millions.values,
               color=COLORS['ocean_blue'], linewidth=2.5, label='Job Openings')

    if hires is not None and len(hires) > 0:
        hires_millions = hires / 1000
        ax.plot(hires_millions.index, hires_millions.values,
               color=COLORS['orange'], linewidth=2, label='Hires')

    if quits is not None and len(quits) > 0:
        quits_millions = quits / 1000
        ax.plot(quits_millions.index, quits_millions.values,
               color=COLORS['carolina_blue'], linewidth=2, label='Quits', alpha=0.8)

    # Last value labels
    if openings is not None and len(openings) > 0:
        add_last_value_label(ax, openings_millions, COLORS['ocean_blue'], side='right', fmt='{:.1f}M')
    if hires is not None and len(hires) > 0:
        add_last_value_label(ax, hires_millions, COLORS['orange'], side='right', fmt='{:.1f}M')

    ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    return fig


def chart_13_beveridge_curve():
    """
    Chart 13: Beveridge Curve
    Unemployment vs job openings rate (labor market efficiency)
    """
    fig, ax = create_single_axis_chart(
        chart_number=13,
        title='Beveridge Curve: Labor Market Efficiency',
        ylabel='Job Openings Rate (%)',
        source='FRED'
    )
    ax.set_xlabel('Unemployment Rate (%)', fontsize=11, fontweight='bold')

    # Fetch data (last 10 years to show full cycle)
    start_date = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')

    unemployment = data.safe_fetch_fred('UNRATE', start_date)
    openings_rate = data.safe_fetch_fred('JTSJOR', start_date)  # Job openings rate

    if unemployment is not None and openings_rate is not None:
        # Align data
        df = pd.DataFrame({
            'unemployment': unemployment,
            'openings_rate': openings_rate
        }).dropna()

        if len(df) > 10:
            # Scatter with time gradient
            dates_numeric = np.arange(len(df))
            scatter = ax.scatter(df['unemployment'], df['openings_rate'],
                               c=dates_numeric, cmap='viridis',
                               s=60, alpha=0.6, edgecolors=COLORS['neutral'], linewidths=0.5)

            # Latest point (prominent)
            ax.scatter(df['unemployment'].iloc[-1], df['openings_rate'].iloc[-1],
                      s=250, color=COLORS['orange'], edgecolors=COLORS['ocean_blue'],
                      linewidths=2.5, zorder=10, marker='*', label='Current')

            # Add trend line (simple moving average path)
            window = 12  # 12-month window
            if len(df) > window:
                df_smooth = df.rolling(window=window, center=True).mean().dropna()
                ax.plot(df_smooth['unemployment'], df_smooth['openings_rate'],
                       color=COLORS['ocean_blue'], linewidth=1.5, alpha=0.4,
                       linestyle='--', label='12-Month Trend')

            ax.legend(loc='upper left', fontsize=9, framealpha=0.95)

    else:
        ax.text(0.5, 0.5, 'Beveridge curve data temporarily unavailable',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=14, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


# Charts 14-15: Extended labor market analysis
# To be added in Phase 4 (wage decomposition, unemployment duration)


# Section 2 complete: 3 core labor market charts with corrected Lighthouse styling
