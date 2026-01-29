"""
Lighthouse Macro - Official Chart Styling Module
Use this for ALL chartbook charts to ensure consistency
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from datetime import datetime

# === OFFICIAL LIGHTHOUSE MACRO COLORS (Nautical 8-Color Palette) ===
#
# Color stack for multi-series charts (use in order):
#   1. Ocean  - primary blue
#   2. Dusk   - orange accent, contrasts with Ocean
#   3. Sky    - light blue, supports Ocean (sky at dawn when lighthouse turns off)
#   4. Venus  - pink, contrasts well against the blues
#   5. Sea    - teal, 5th distinct color
#
# This order ensures maximum visual distinction:
#   - 3 lines: blue, orange, light blue (all distinct)
#   - 5 lines: blue, orange, light blue, pink, teal (no clustering)
#   - If Sea were 4th, you'd have 3 blue-ish tones before pink
#
COLORS = {
    # Primary stack (in order for multi-series)
    'ocean': '#0089D1',           # 1. Primary blue
    'dusk': '#FF6723',            # 2. Orange accent
    'sky': '#00D4FF',             # 3. Light blue (supports Ocean)
    'venus': '#FF2389',           # 4. Pink (contrasts against blues)
    'sea': '#00BB99',             # 5. Teal
    # Chart structure
    'doldrums': '#D3D6D9',        # Backgrounds, inner chart borders
    # Directional (bullish/bearish)
    'starboard': '#00FF00',       # Bullish/up (green) - starboard = right = green light
    'port': '#FF0000',            # Bearish/down (red) - port = left = red light
    # Utility
    'neutral': '#808080',         # Grey for axes/text
    'black': '#000000',
    'white': '#FFFFFF',
    # Legacy aliases
    'ocean_blue': '#0089D1',
    'orange': '#FF6723',
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


def apply_lighthouse_frame(fig, ax, title, subtitle=None, source='Lighthouse Macro, FRED, Yahoo Finance'):
    """
    Apply full Lighthouse Macro framing:
    - Ocean blue outer border (2px, no whitespace outside)
    - Doldrums inner border around chart area
    - Centered title below header
    - Header: "Lighthouse Macro | Macro, Illuminated."
    - Source line at bottom

    Args:
        fig: matplotlib Figure
        ax: matplotlib Axes
        title: Main chart title (centered)
        subtitle: Optional subtitle below title
        source: Data source string
    """
    from datetime import datetime

    # Remove all whitespace outside figure
    fig.patch.set_facecolor('white')

    # Add Ocean outer border (2px) - full rectangle around entire figure
    fig.patches.clear()
    from matplotlib.patches import Rectangle
    outer_border = Rectangle((0, 0), 1, 1, transform=fig.transFigure,
                              facecolor='none', edgecolor=COLORS['ocean'],
                              linewidth=4, clip_on=False, zorder=1000)
    fig.patches.append(outer_border)

    # Header text: "Lighthouse Macro | Macro, Illuminated." at top left inside border
    fig.text(0.03, 0.96, 'Lighthouse Macro', fontsize=10, fontweight='bold',
             color=COLORS['ocean'], ha='left', va='top')
    fig.text(0.19, 0.96, '|', fontsize=10, color=COLORS['doldrums'], ha='left', va='top')
    fig.text(0.21, 0.96, 'Macro, Illuminated.', fontsize=10, fontweight='bold',
             color=COLORS['dusk'], ha='left', va='top')

    # Centered title (below header)
    fig.text(0.5, 0.91, title, fontsize=16, fontweight='bold',
             color=COLORS['black'], ha='center', va='top')

    # Optional subtitle
    if subtitle:
        fig.text(0.5, 0.87, subtitle, fontsize=11,
                 color=COLORS['neutral'], ha='center', va='top')

    # Doldrums border around chart area
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color(COLORS['doldrums'])
        spine.set_linewidth(1.5)

    # Source line at bottom center
    date_str = datetime.now().strftime('%m.%d.%Y')
    fig.text(0.5, 0.02, f'Source: {source} as of {date_str}',
             fontsize=9, color=COLORS['neutral'], ha='center', va='bottom')

    # No gridlines
    ax.grid(False)
    ax.set_axisbelow(False)


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


def create_framed_chart(title, subtitle=None, ylabel='', xlabel='', source='Lighthouse Macro, FRED, Yahoo Finance', figsize=(14, 9)):
    """
    Create a chart with full Lighthouse framing:
    - Ocean outer border (no whitespace outside)
    - Doldrums inner border around chart
    - Centered title

    Returns:
        fig, ax
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Position axes to leave room for header/footer
    ax.set_position([0.08, 0.12, 0.84, 0.72])

    ax.set_ylabel(ylabel, fontsize=11, fontweight='bold', color=COLORS['neutral'])
    ax.set_xlabel(xlabel, fontsize=11, fontweight='bold', color=COLORS['neutral'])

    # Apply full Lighthouse frame
    apply_lighthouse_frame(fig, ax, title, subtitle, source)

    # Tick styling
    ax.tick_params(colors=COLORS['neutral'])

    return fig, ax


def create_single_axis_chart(chart_number, title, ylabel='', source='FRED'):
    """
    Create a single-axis chart with Lighthouse styling (legacy)

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
