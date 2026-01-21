"""
Lighthouse Macro - Section 2: Labor Market Dynamics (Charts 11-17)
PROPRIETARY INDICATORS: LFI, LDI, Hours-Employment Divergence
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


def chart_11_labor_fragility_index():
    """
    Chart 11: Labor Fragility Index (LFI)
    Composite: Long-duration unemployment + (inverted quits) + (inverted hires/quits)
    """
    fig, ax = create_single_axis_chart(
        chart_number=11,
        title='Labor Fragility Index (LFI): Job-Finding Effectiveness',
        ylabel='LFI (Z-Score)',
        source='FRED (JOLTS, CPS)'
    )

    # Fetch data (10 years to show full cycle)
    start_date = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')

    # Long-duration unemployment
    long_unemp = data.safe_fetch_fred('UEMP27OV', start_date)  # Unemployed 27+ weeks
    total_unemp = data.safe_fetch_fred('UNEMPLOY', start_date)  # Total unemployed

    # JOLTS data
    quits = data.safe_fetch_fred('JTSQUR', start_date)  # Quits rate
    hires = data.safe_fetch_fred('JTSHIR', start_date)  # Hires rate

    if long_unemp is not None and total_unemp is not None and quits is not None and hires is not None:
        # Calculate long-duration share
        long_duration_share = (long_unemp / total_unemp) * 100

        # Calculate hires/quits ratio
        hires_quits_ratio = hires / quits

        # Align data (monthly)
        df = pd.DataFrame({
            'long_duration': long_duration_share,
            'quits': quits,
            'hires_quits': hires_quits_ratio
        }).dropna()

        if len(df) > 0:
            # Z-score components
            df['z_long_duration'] = calculate_z_score(df['long_duration'])  # Higher = worse
            df['z_quits'] = -calculate_z_score(df['quits'])  # Inverted: lower quits = worse
            df['z_hires_quits'] = -calculate_z_score(df['hires_quits'])  # Inverted: lower ratio = worse

            # LFI = average of components
            df['LFI'] = (df['z_long_duration'] + df['z_quits'] + df['z_hires_quits']) / 3

            # Plot LFI
            ax.plot(df.index, df['LFI'], color=COLORS['ocean_blue'],
                   linewidth=2.5, label='Labor Fragility Index')

            # Threshold bands
            ax.axhline(y=1, color=COLORS['orange'], linestyle='--',
                      linewidth=1.5, alpha=0.6, label='+1σ (High Fragility)')
            ax.axhline(y=0, color=COLORS['neutral'], linestyle='-',
                      linewidth=1.5, alpha=0.6, label='Neutral')
            ax.axhline(y=-1, color=COLORS['ocean_blue'], linestyle='--',
                      linewidth=1.5, alpha=0.6, label='-1σ (Robust Market)')

            # Shade fragile zone
            ax.fill_between(df.index, 1, df['LFI'],
                           where=(df['LFI'] > 1),
                           color=COLORS['orange'], alpha=0.2, label='Fragile Zone')

            add_last_value_label(ax, df['LFI'], COLORS['ocean_blue'],
                               side='right', fmt='{:.2f}σ')

            ax.legend(loc='upper right', fontsize=9, framealpha=0.95)
    else:
        ax.text(0.5, 0.5, 'LFI data temporarily unavailable\n\nRequires: JOLTS, CPS',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=11, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_12_labor_dynamism_index():
    """
    Chart 12: Labor Dynamism Index (LDI)
    Composite: Quits + Hires/Quits + Quits/Layoffs
    """
    fig, ax = create_single_axis_chart(
        chart_number=12,
        title='Labor Dynamism Index (LDI): Worker Optionality & Confidence',
        ylabel='LDI (Z-Score)',
        source='FRED (JOLTS)'
    )

    # Fetch JOLTS data
    start_date = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')

    quits = data.safe_fetch_fred('JTSQUR', start_date)  # Quits rate
    hires = data.safe_fetch_fred('JTSHIR', start_date)  # Hires rate
    layoffs = data.safe_fetch_fred('JTSLDL', start_date)  # Layoffs and discharges level

    # Get quits level for ratio calculation
    quits_level = data.safe_fetch_fred('JTSQUL', start_date)

    if quits is not None and hires is not None and layoffs is not None and quits_level is not None:
        # Calculate ratios
        hires_quits_ratio = hires / quits
        quits_layoffs_ratio = quits_level / layoffs

        # Align data
        df = pd.DataFrame({
            'quits': quits,
            'hires_quits': hires_quits_ratio,
            'quits_layoffs': quits_layoffs_ratio
        }).dropna()

        if len(df) > 0:
            # Z-score components (all positive direction = more dynamism)
            df['z_quits'] = calculate_z_score(df['quits'])
            df['z_hires_quits'] = calculate_z_score(df['hires_quits'])
            df['z_quits_layoffs'] = calculate_z_score(df['quits_layoffs'])

            # LDI = average of components
            df['LDI'] = (df['z_quits'] + df['z_hires_quits'] + df['z_quits_layoffs']) / 3

            # Plot LDI
            ax.plot(df.index, df['LDI'], color=COLORS['ocean_blue'],
                   linewidth=2.5, label='Labor Dynamism Index')

            # Threshold bands
            ax.axhline(y=1, color=COLORS['ocean_blue'], linestyle='--',
                      linewidth=1.5, alpha=0.6, label='+1σ (High Dynamism)')
            ax.axhline(y=0, color=COLORS['neutral'], linestyle='-',
                      linewidth=1.5, alpha=0.6, label='Neutral')
            ax.axhline(y=-1, color=COLORS['orange'], linestyle='--',
                      linewidth=1.5, alpha=0.6, label='-1σ (Low Dynamism)')

            # Shade low dynamism zone
            ax.fill_between(df.index, -1, df['LDI'],
                           where=(df['LDI'] < -1),
                           color=COLORS['orange'], alpha=0.2, label='Stagnant Zone')

            add_last_value_label(ax, df['LDI'], COLORS['ocean_blue'],
                               side='right', fmt='{:.2f}σ')

            ax.legend(loc='upper right', fontsize=9, framealpha=0.95)
    else:
        ax.text(0.5, 0.5, 'LDI data temporarily unavailable\n\nRequires: JOLTS data',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=11, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_13_payroll_quits_divergence():
    """
    Chart 13: Payroll Growth vs Quits Rate Divergence
    "Payrolls can stay positive while quits slide—that's a late-cycle tell"
    """
    fig, ax_left, ax_right = create_dual_axis_chart(
        chart_number=13,
        title='Payroll-Quits Divergence: Late-Cycle Labor Signal',
        left_label='Quits Rate (%)',
        right_label='Payroll Growth (% YoY)',
        source='FRED'
    )

    # Fetch data
    start_date = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')

    payrolls = data.safe_fetch_fred('PAYEMS', start_date)  # Total nonfarm payrolls
    quits = data.safe_fetch_fred('JTSQUR', start_date)  # Quits rate

    if payrolls is not None and quits is not None:
        # Calculate payroll YoY growth
        payroll_yoy = payrolls.pct_change(12) * 100  # 12 months

        # Align data
        df = pd.DataFrame({
            'payroll_yoy': payroll_yoy,
            'quits': quits
        }).dropna()

        if len(df) > 0:
            # Plot quits (left, secondary)
            ax_left.plot(df.index, df['quits'],
                        color=COLORS['neutral'], linewidth=2, alpha=0.7, label='Quits Rate')
            ax_left.fill_between(df.index, 0, df['quits'],
                                color=COLORS['neutral'], alpha=0.1)

            # Plot payroll growth (right, primary)
            ax_right.plot(df.index, df['payroll_yoy'],
                         color=COLORS['ocean_blue'], linewidth=2.5, label='Payroll Growth')
            ax_right.axhline(y=0, color=COLORS['neutral'], linestyle='--',
                            linewidth=1.5, alpha=0.6)

            # Shade divergence periods (payrolls positive, quits declining)
            # Calculate quits trend (6-month change)
            df['quits_chg'] = df['quits'].diff(6)
            divergence = (df['payroll_yoy'] > 0) & (df['quits_chg'] < 0)

            ax_right.fill_between(df.index, 0, df['payroll_yoy'],
                                 where=divergence,
                                 color=COLORS['orange'], alpha=0.2,
                                 label='Divergence Zone')

            add_last_value_label(ax_left, df['quits'], COLORS['neutral'],
                               side='left', fmt='{:.1f}%')
            add_last_value_label(ax_right, df['payroll_yoy'], COLORS['ocean_blue'],
                               side='right', fmt='{:.1f}%')

            # Combined legend
            lines1, labels1 = ax_left.get_legend_handles_labels()
            lines2, labels2 = ax_right.get_legend_handles_labels()
            ax_left.legend(lines1 + lines2, labels1 + labels2,
                          loc='upper right', fontsize=9, framealpha=0.95)
    else:
        ax_left.text(0.5, 0.5, 'Data temporarily unavailable',
                    ha='center', va='center', transform=ax_left.transAxes,
                    fontsize=11, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_14_hours_employment_divergence():
    """
    Chart 14: Hours Worked vs Employment
    "Hours represent the first lever firms pull"
    """
    fig, ax = create_single_axis_chart(
        chart_number=14,
        title='Hours vs Employment Divergence: Leading Layoff Indicator',
        ylabel='YoY Growth (%)',
        source='FRED'
    )

    # Fetch data
    start_date = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')

    # Total hours worked
    hours = data.safe_fetch_fred('HOABS', start_date)  # Hours of all persons

    # Total employment
    employment = data.safe_fetch_fred('PAYEMS', start_date)  # Nonfarm payrolls

    if hours is not None and employment is not None:
        # Calculate YoY growth
        hours_yoy = hours.pct_change(12) * 100
        employment_yoy = employment.pct_change(12) * 100

        # Align data
        df = pd.DataFrame({
            'hours_yoy': hours_yoy,
            'employment_yoy': employment_yoy
        }).dropna()

        if len(df) > 0:
            # Plot both
            ax.plot(df.index, df['hours_yoy'],
                   color=COLORS['orange'], linewidth=2.5, label='Hours Worked YoY')
            ax.plot(df.index, df['employment_yoy'],
                   color=COLORS['ocean_blue'], linewidth=2.5, label='Employment YoY')

            # Zero line
            ax.axhline(y=0, color=COLORS['neutral'], linestyle='--',
                      linewidth=1.5, alpha=0.6)

            # Shade warning zone (hours < employment)
            ax.fill_between(df.index, df['hours_yoy'], df['employment_yoy'],
                           where=(df['hours_yoy'] < df['employment_yoy']),
                           color=COLORS['orange'], alpha=0.2,
                           label='Hours Lagging (Layoffs Ahead)')

            add_last_value_label(ax, df['hours_yoy'], COLORS['orange'],
                               side='right', fmt='{:.1f}%')

            ax.legend(loc='upper right', fontsize=9, framealpha=0.95)
    else:
        ax.text(0.5, 0.5, 'Hours/Employment data temporarily unavailable',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=11, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_15_labor_market_heatmap():
    """
    Chart 15: Labor Market Heatmap (8 Metrics Z-Scores)
    """
    fig, ax = create_single_axis_chart(
        chart_number=15,
        title='Labor Market Health Heatmap: 8-Metric Z-Score Composite',
        ylabel='',
        source='FRED'
    )

    # Fetch data (5 years)
    start_date = (datetime.now() - timedelta(days=1825)).strftime('%Y-%m-%d')

    # 8 key labor metrics
    metrics = {
        'Unemployment': 'UNRATE',
        'Participation': 'CIVPART',
        'Prime-Age Empl': 'LNS12300060',  # 25-54 employment-pop ratio
        'Quits Rate': 'JTSQUR',
        'Hires Rate': 'JTSHIR',
        'Layoffs': 'JTSLDL',
        'Avg Hours': 'AWHAETP',  # Average weekly hours
        'Wage Growth': 'CES0500000003'  # Average hourly earnings
    }

    data_dict = {}
    for name, series_id in metrics.items():
        series = data.safe_fetch_fred(series_id, start_date)
        if series is not None:
            # Calculate YoY or level depending on metric
            if name == 'Wage Growth':
                data_dict[name] = series.pct_change(12) * 100
            else:
                data_dict[name] = series

    if len(data_dict) > 0:
        # Create DataFrame
        df = pd.DataFrame(data_dict).dropna()

        if len(df) > 0:
            # Calculate z-scores (recent 12 months)
            recent_data = df.tail(12)
            z_scores = {}

            for col in recent_data.columns:
                # Invert unemployment and layoffs (higher = worse)
                if col in ['Unemployment', 'Layoffs']:
                    z_scores[col] = -calculate_z_score(df[col]).iloc[-1]
                else:
                    z_scores[col] = calculate_z_score(df[col]).iloc[-1]

            # Create heatmap data
            metrics_list = list(z_scores.keys())
            values = [z_scores[m] for m in metrics_list]

            # Plot as horizontal bar chart colored by z-score
            colors_map = []
            for val in values:
                if val > 1:
                    colors_map.append(COLORS['ocean_blue'])  # Strong positive
                elif val > 0:
                    colors_map.append(COLORS['carolina_blue'])  # Positive
                elif val > -1:
                    colors_map.append(COLORS['neutral'])  # Neutral/Negative
                else:
                    colors_map.append(COLORS['orange'])  # Weak

            y_pos = np.arange(len(metrics_list))
            ax.barh(y_pos, values, color=colors_map, alpha=0.8, edgecolor='black', linewidth=0.5)

            # Add value labels
            for i, (metric, val) in enumerate(zip(metrics_list, values)):
                ax.text(val + 0.1 if val > 0 else val - 0.1, i, f'{val:.1f}σ',
                       va='center', ha='left' if val > 0 else 'right',
                       fontsize=9, fontweight='bold')

            ax.set_yticks(y_pos)
            ax.set_yticklabels(metrics_list, fontsize=10)
            ax.set_xlabel('Z-Score (σ)', fontsize=11, fontweight='bold')
            ax.axvline(x=0, color='black', linewidth=2)
            ax.axvline(x=1, color=COLORS['neutral'], linestyle='--', alpha=0.5, linewidth=1)
            ax.axvline(x=-1, color=COLORS['neutral'], linestyle='--', alpha=0.5, linewidth=1)

            # Legend
            from matplotlib.patches import Rectangle
            legend_elements = [
                Rectangle((0, 0), 1, 1, fc=COLORS['ocean_blue'], label='>+1σ Strong'),
                Rectangle((0, 0), 1, 1, fc=COLORS['carolina_blue'], label='0 to +1σ Positive'),
                Rectangle((0, 0), 1, 1, fc=COLORS['neutral'], label='-1σ to 0 Neutral'),
                Rectangle((0, 0), 1, 1, fc=COLORS['orange'], label='<-1σ Weak')
            ]
            ax.legend(handles=legend_elements, loc='lower right', fontsize=8, framealpha=0.95)

    else:
        ax.text(0.5, 0.5, 'Labor market heatmap data temporarily unavailable',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=11, color=COLORS['neutral'])

    plt.tight_layout()
    return fig


def chart_16_jolts_indicators():
    """
    Chart 16: JOLTS Indicators (3-Panel)
    Openings, Hires vs Separations, Quits vs Layoffs
    """
    # Using the existing function from labor_market_charts.py
    from labor_market_charts import chart_12_jolts_indicators
    return chart_12_jolts_indicators()


def chart_17_beveridge_curve():
    """
    Chart 17: Beveridge Curve
    Unemployment vs Job Openings
    """
    # Using the existing function from labor_market_charts.py
    from labor_market_charts import chart_13_beveridge_curve
    return chart_13_beveridge_curve()


# Section 2 complete: 7 labor market charts
# Proprietary indicators: LFI, LDI fully implemented
# All charts functional with FRED/JOLTS data
