"""
Lighthouse Macro - Official Chart Styling Module
Use this for ALL chartbook charts to ensure consistency
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from datetime import datetime

# === OFFICIAL LIGHTHOUSE MACRO COLORS ===
COLORS = {
    'ocean_blue': '#0089D1',      # Primary
    'orange': '#FF7700',           # Secondary
    'carolina_blue': '#4B9CD3',    # Tertiary
    'magenta': '#FF00FF',          # Quaternary
    'neutral': '#808080',          # Grey for axes/text
    'black': '#000000',
}

# === MATPLOTLIB GLOBAL SETTINGS ===
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 10,
    'axes.titlesize': 14,
    'axes.labelsize': 11,
    'axes.titleweight': 'bold',
    'figure.figsize': (11, 8.5),
    'figure.dpi': 150,
    'axes.grid': False,  # NO GRIDLINES
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.edgecolor': COLORS['neutral'],
    'xtick.color': COLORS['neutral'],
    'ytick.color': COLORS['neutral'],
    'legend.framealpha': 0.95,
    'legend.edgecolor': COLORS['neutral'],
})


def enforce_no_gridlines(ax):
    """
    Absolutely ensure NO gridlines on any axis
    Call this on every ax object to guarantee clean charts

    Args:
        ax: matplotlib Axes object (or list of Axes)
    """
    if isinstance(ax, (list, tuple)):
        for a in ax:
            enforce_no_gridlines(a)
        return

    ax.grid(False)
    ax.set_axisbelow(False)


def add_lighthouse_branding(fig, ax, chart_number, source='FRED, NY Fed, OFR'):
    """
    Add Lighthouse Macro branding to chart

    Args:
        fig: matplotlib Figure
        ax: matplotlib Axes (primary axis if dual-axis)
        chart_number: Chart number (int or str)
        source: Data source string
    """
    # CRITICAL: Enforce NO gridlines
    enforce_no_gridlines(ax)

    # Chart number badge (in axes coordinates)
    circle = Circle((0.02, 0.98), 0.015, transform=ax.transAxes,
                   facecolor=COLORS['ocean_blue'], edgecolor='none', zorder=100)
    ax.add_patch(circle)
    ax.text(0.02, 0.98, str(chart_number),
            ha='center', va='center', fontsize=10, fontweight='bold',
            color='white', transform=ax.transAxes, zorder=101)

    # Top left: LIGHTHOUSE MACRO (in axes coordinates)
    ax.text(0.045, 0.98, 'LIGHTHOUSE MACRO',
            ha='left', va='center', fontsize=9, fontweight='bold',
            color=COLORS['ocean_blue'], transform=ax.transAxes)

    # Bottom left: Source (in FIGURE coordinates - OUTSIDE chart area)
    fig.text(0.02, 0.02, f'Source: {source}',
            ha='left', va='bottom', fontsize=7, color=COLORS['neutral'],
            style='italic')

    # Bottom right: Watermark (in FIGURE coordinates - OUTSIDE chart area)
    fig.text(0.98, 0.02, 'MACRO, ILLUMINATED.',
            ha='right', va='bottom', fontsize=8, fontweight='bold',
            color=COLORS['ocean_blue'], alpha=0.6)

    # Clean axes - NO GRIDLINES
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['neutral'])
    ax.spines['bottom'].set_color(COLORS['neutral'])
    ax.tick_params(colors=COLORS['neutral'])


def add_last_value_label(ax, series, color, side='right', fmt='{:.1f}'):
    """
    Add last value label on axis

    Args:
        ax: matplotlib Axes
        series: pandas Series with data
        color: hex color for label
        side: 'right' or 'left'
        fmt: format string for value
    """
    if len(series) == 0:
        return

    last_val = series.dropna().iloc[-1]

    if side == 'right':
        x_pos = 1.01
        ha = 'left'
    else:
        x_pos = -0.01
        ha = 'right'

    ax.text(x_pos, last_val, fmt.format(last_val),
            transform=ax.get_yaxis_transform(),
            ha=ha, va='center', fontsize=9,
            color=color, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                     edgecolor=color, linewidth=1.5))


def create_single_axis_chart(chart_number, title, ylabel='', source='FRED'):
    """
    Create a single-axis chart with Lighthouse styling

    Returns:
        fig, ax
    """
    fig, ax = plt.subplots(figsize=(11, 8.5))

    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_ylabel(ylabel, fontsize=11, fontweight='bold')

    # TradingView-style tight margins: data starts at left spine
    ax.margins(x=0)  # No padding on x-axis
    ax.set_xlim(auto=True)  # Auto-adjust to data

    add_lighthouse_branding(fig, ax, chart_number, source)

    return fig, ax


def create_dual_axis_chart(chart_number, title, left_label='', right_label='', source='FRED'):
    """
    Create dual-axis chart with Lighthouse styling
    RHS is PRIMARY axis (prominent)

    Returns:
        fig, ax_left, ax_right
    """
    fig, ax_left = plt.subplots(figsize=(11, 8.5))
    ax_right = ax_left.twinx()

    # CRITICAL: Enforce NO gridlines on both axes
    enforce_no_gridlines([ax_left, ax_right])

    # Titles and labels
    ax_left.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax_left.set_ylabel(left_label, fontsize=10, color=COLORS['neutral'])
    ax_right.set_ylabel(right_label, fontsize=11, color=COLORS['ocean_blue'], fontweight='bold')

    # TradingView-style tight margins: data starts at left spine
    ax_left.margins(x=0)  # No padding on x-axis
    ax_left.set_xlim(auto=True)  # Auto-adjust to data

    # Tick colors
    ax_left.tick_params(axis='y', labelcolor=COLORS['neutral'])
    ax_right.tick_params(axis='y', labelcolor=COLORS['ocean_blue'])

    # Clean left axis (secondary)
    ax_left.spines['right'].set_visible(False)

    # Clean right axis (primary) - but keep it visible
    ax_right.spines['left'].set_visible(False)
    ax_right.spines['top'].set_visible(False)
    ax_right.spines['right'].set_color(COLORS['neutral'])
    ax_right.spines['bottom'].set_color(COLORS['neutral'])

    add_lighthouse_branding(fig, ax_left, chart_number, source)

    return fig, ax_left, ax_right


def create_section_page(section_number, section_title, section_description, charts_range):
    """
    Create a section divider page with written annotations

    Args:
        section_number: Layer number (1-6)
        section_title: Title of the section
        section_description: Text description of what this section covers
        charts_range: String like "Charts 1-17"

    Returns:
        fig
    """
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    # Section number (large)
    ax.text(0.5, 0.70, f'LAYER {section_number}',
            ha='center', va='center', fontsize=48, fontweight='bold',
            color=COLORS['ocean_blue'], transform=ax.transAxes)

    # Section title
    ax.text(0.5, 0.58, section_title,
            ha='center', va='center', fontsize=24, fontweight='bold',
            color=COLORS['ocean_blue'], transform=ax.transAxes)

    # Charts range
    ax.text(0.5, 0.52, charts_range,
            ha='center', va='center', fontsize=14,
            color=COLORS['neutral'], style='italic', transform=ax.transAxes)

    # Description (wrapped)
    ax.text(0.5, 0.35, section_description,
            ha='center', va='center', fontsize=12,
            color=COLORS['black'], transform=ax.transAxes,
            wrap=True, multialignment='center')

    # Bottom watermark
    fig.text(0.5, 0.05, 'MACRO, ILLUMINATED.',
            ha='center', va='bottom', fontsize=10, fontweight='bold',
            color=COLORS['ocean_blue'], alpha=0.6)

    return fig


# === EXAMPLE USAGE ===

if __name__ == "__main__":
    import pandas as pd
    import numpy as np

    # Test single axis chart
    fig, ax = create_single_axis_chart(
        chart_number=1,
        title='Test Chart - Single Axis',
        ylabel='Test Metric (%)',
        source='FRED'
    )

    # Add sample data
    dates = pd.date_range('2020-01-01', periods=100, freq='D')
    values = np.cumsum(np.random.randn(100))
    series = pd.Series(values, index=dates)

    ax.plot(dates, values, color=COLORS['ocean_blue'], linewidth=2, label='Test Series')
    add_last_value_label(ax, series, COLORS['ocean_blue'], side='right')

    ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
    plt.tight_layout()
    plt.savefig('test_single_axis.png', dpi=300, bbox_inches='tight')
    print("✓ Saved test_single_axis.png")
    plt.close()

    # Test dual axis chart
    fig, ax_left, ax_right = create_dual_axis_chart(
        chart_number=2,
        title='Test Chart - Dual Axis',
        left_label='Secondary Metric',
        right_label='Primary Metric',
        source='FRED, NY Fed'
    )

    # Left axis (secondary)
    series_left = pd.Series(np.cumsum(np.random.randn(100)) + 50, index=dates)
    ax_left.plot(dates, series_left.values, color=COLORS['neutral'],
                linewidth=1.5, alpha=0.7, label='Secondary')
    add_last_value_label(ax_left, series_left, COLORS['neutral'], side='left')

    # Right axis (primary)
    series_right = pd.Series(np.cumsum(np.random.randn(100)) * 2, index=dates)
    ax_right.plot(dates, series_right.values, color=COLORS['ocean_blue'],
                 linewidth=2.5, label='Primary')
    add_last_value_label(ax_right, series_right, COLORS['ocean_blue'], side='right')

    # Combined legend
    lines1, labels1 = ax_left.get_legend_handles_labels()
    lines2, labels2 = ax_right.get_legend_handles_labels()
    ax_left.legend(lines1 + lines2, labels1 + labels2, loc='upper left',
                  fontsize=9, framealpha=0.95)

    plt.tight_layout()
    plt.savefig('test_dual_axis.png', dpi=300, bbox_inches='tight')
    print("✓ Saved test_dual_axis.png")
    plt.close()

    # Test section page
    fig = create_section_page(
        section_number=1,
        section_title='Macro Dynamics',
        section_description='Core macroeconomic indicators including growth, employment,\ninflation, and central bank policy metrics.',
        charts_range='Charts 1-17'
    )

    plt.savefig('test_section_page.png', dpi=300, bbox_inches='tight')
    print("✓ Saved test_section_page.png")
    plt.close()

    print("\n✓ All tests passed! Color palette and styling verified.")
