"""
labor_market_charts_updated.py
--------------------------------

This script produces a suite of labour market charts using data
downloaded from FRED/BLS. The aim is to adhere to Lighthouse Macro's
house style as described by the user:

* Evenly spaced chart area with minimal wasted whitespace.
* Legends positioned in the upper‐left corner, outside the data area
  if possible, with a semi‐opaque white background so that lines
  remain unobscured.
* Source attribution placed just below the x‐axis on the right,
  outside the plot area.
* A watermark in the bottom‐right corner (or top‐right on crowded
  plots) comprising stylised text rather than the lighthouse logo.
* Axis spines coloured a medium light grey for a subtle frame.
* The primary y‐axis is on the right for single‐axis charts. For
  dual‐axis charts, the left axis corresponds to the second series
  (e.g. U‑6 or inflation) and the right axis holds the primary
  (headline) series.
* A consistent colour palette matching the Lighthouse Macro brand.

The script generates more than a dozen charts covering ratios of job
openings to unemployed persons, churn dynamics, labour supply, wage
growth, unemployment gaps, long‐term unemployment shares, and several
derived indicators. It also includes a few dashboards (multiple
panels) which the user counts as two charts.

To run the script:
    python labor_market_charts_updated.py
It will load the required CSVs from the current directory (by
default `/home/oai/share`) and emit PNG files into the same folder.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from PIL import Image, ImageDraw, ImageFont

# Base directory where CSVs are stored (env override to aid testing)
BASE_PATH = os.environ.get('DATA_DIR', '/home/oai/share')

# Colour palette drawn from Lighthouse Macro guidelines
PALETTE = {
    'ocean_blue': '#003f5c',         # deep ocean blue
    'sunset_orange': '#fc6736',      # deep sunset orange
    'carolina_blue': '#00a8e8',      # neon Carolina blue
    'magenta': '#d45087',           # neon magenta
    'gray': '#a3a3a3',              # medium‑light grey
}


def load_series(name: str) -> pd.DataFrame:
    """Load a FRED CSV into a DataFrame with datetime index.

    Parameters
    ----------
    name : str
        Name of the CSV without extension.

    Returns
    -------
    DataFrame
        DataFrame indexed by 'date' with a value column.
    """
    path = os.path.join(BASE_PATH, f"{name}.csv")
    df = pd.read_csv(path)
    # normalise column names: first column is date, second is value
    df.columns = ['date', name]
    df['date'] = pd.to_datetime(df['date'])
    return df


def prepare_data():
    """Load and merge all data series and compute derived measures.

    Returns
    -------
    dict
        Dictionary containing DataFrames keyed by descriptive names.
    """
    series = {}
    # primary series
    series['u3'] = load_series('UNRATE')
    series['u6'] = load_series('U6RATE')
    series['lfpr'] = load_series('CIVPART')
    series['epop'] = load_series('LNS12300060')
    series['unemploy'] = load_series('UNEMPLOY')
    series['jol'] = load_series('JTSJOL')
    series['quits'] = load_series('JTSQUR')
    series['hires'] = load_series('JTSHIR')
    series['cpi'] = load_series('CPIAUCSL')
    series['wages'] = load_series('CES0500000003')

    # Merge unemployment rates
    un = series['u3'].merge(series['u6'], on='date', how='inner')
    un.columns = ['date', 'u3', 'u6']

    # Ratio of job openings to unemployed
    job_ratio = series['jol'].merge(series['unemploy'], on='date', how='inner')
    job_ratio['ratio'] = job_ratio['JTSJOL'] / job_ratio['UNEMPLOY']

    # Quits vs hires
    churn = series['quits'].merge(series['hires'], on='date', how='inner')
    churn.columns = ['date', 'quits', 'hires']
    churn['hire_to_quit'] = churn['hires'] / churn['quits']

    # Labour force participation vs prime‑age employment population ratio
    supply = series['lfpr'].merge(series['epop'], on='date', how='inner')
    supply.columns = ['date', 'lfpr', 'epop']
    supply['epop_minus_lfpr'] = supply['epop'] - supply['lfpr']

    # Wage and inflation series
    wages = series['wages'].copy()
    cpi = series['cpi'].copy()
    wages['wage_growth'] = wages['CES0500000003'].pct_change(12) * 100
    cpi['cpi_inflation'] = cpi['CPIAUCSL'].pct_change(12) * 100
    w_cpi = wages[['date', 'wage_growth']].merge(
        cpi[['date', 'cpi_inflation']], on='date', how='inner')
    w_cpi['real_wage'] = w_cpi['wage_growth'] - w_cpi['cpi_inflation']

    # U6 minus U3 gap
    un['u_gap'] = un['u6'] - un['u3']

    # Real wage index: cumulative from 100 at first valid observation
    real_wage_index = w_cpi[['date', 'real_wage']].copy()
    real_wage_index = real_wage_index.dropna()
    # create an index by accumulating real wage growth
    real_wage_index['real_wage_index'] = (1 + real_wage_index['real_wage']/100).cumprod() * 100

    data = {
        'un': un,
        'job_ratio': job_ratio,
        'churn': churn,
        'supply': supply,
        'w_cpi': w_cpi,
        'real_wage_index': real_wage_index,
    }
    return data


def create_watermark_image(text: str = 'LIGHTHOUSE MACRO', tagline: str = 'MACRO, ILLUMINATED.',
                            font_size: int = 14, tagline_size: int = 10,
                            colour: str = '#b5b5b5') -> Image.Image:
    """Generate a simple text watermark image using PIL.

    This avoids dependency on external logo files. The watermark
    contains a main title and a tagline stacked vertically. The
    generated image uses a transparent background.

    Parameters
    ----------
    text : str
        Main text for the watermark.
    tagline : str
        Secondary tagline.
    font_size : int
        Font size for the main text.
    tagline_size : int
        Font size for the tagline.
    colour : str
        Hex colour for the text.

    Returns
    -------
    PIL.Image
        Watermark image with transparent background.
    """
    # Create a blank canvas large enough for the text
    width, height = 300, 60
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    # Attempt to use a sans-serif font; fallback to default if unavailable
    try:
        font_main = ImageFont.truetype('DejaVuSans-Bold.ttf', font_size)
        font_tag = ImageFont.truetype('DejaVuSans.ttf', tagline_size)
    except IOError:
        font_main = ImageFont.load_default()
        font_tag = ImageFont.load_default()
    # Determine text widths/heights
    w_text, h_text = draw.textsize(text, font=font_main)
    w_tag, h_tag = draw.textsize(tagline, font=font_tag)
    # Compute positions to centre texts within the canvas
    x_text = (width - w_text) / 2
    y_text = 0
    x_tag = (width - w_tag) / 2
    y_tag = h_text + 2
    # Draw the text
    draw.text((x_text, y_text), text, font=font_main, fill=colour)
    draw.text((x_tag, y_tag), tagline, font=font_tag, fill=colour)
    return img


def add_watermark(ax, wm: Image.Image, scale: float = 0.25, xoff: float = 0.85, yoff: float = 0.10):
    """Overlay a watermark onto the given axes.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes on which to overlay the watermark.
    wm : PIL.Image
        Watermark image to use.
    scale : float
        Scaling factor relative to axes; adjust for different figure sizes.
    xoff : float
        Horizontal position in axes fraction coordinates (0 = left, 1 = right).
    yoff : float
        Vertical position in axes fraction coordinates (0 = bottom, 1 = top).
    """
    from matplotlib.offsetbox import OffsetImage, AnnotationBbox
    im = OffsetImage(wm, zoom=scale)
    ab = AnnotationBbox(im, (xoff, yoff), frameon=False, xycoords='axes fraction')
    ax.add_artist(ab)


def style_axes(ax):
    """Apply standard styling to an Axes object.

    The primary y‐axis is moved to the right and the spines are
    coloured a light grey. Tick labels and axis labels are also
    configured.
    """
    # Move primary y-axis to the right
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position('right')
    # Colour spines
    for spine in ax.spines.values():
        spine.set_color(PALETTE['gray'])
    # Adjust gridlines for y-axis only
    ax.grid(axis='y', linestyle='--', linewidth=0.6, color='#e0e0e0', zorder=0)


def add_source(ax, text: str, pad: float = -0.12):
    """Add a source note below the x-axis.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes to annotate.
    text : str
        Source string to display.
    pad : float
        Vertical offset in axes fraction (negative values place
        below the axis). Defaults to -0.12, which positions the
        source neatly below the x-axis labels without overlap.
    """
    ax.text(1.0, pad, text, ha='right', va='top', fontsize=8, color=PALETTE['gray'], transform=ax.transAxes)


def save_fig(fig, filename: str):
    """Save a figure to the BASE_PATH with high resolution and tight layout."""
    fig.savefig(os.path.join(BASE_PATH, filename), dpi=300, bbox_inches='tight')
    plt.close(fig)


def plot_all():
    """Create all charts and dashboards as specified by the user."""
    data = prepare_data()
    wm = create_watermark_image()

    ###############################################
    # Chart 1: Job openings to unemployed ratio
    ###############################################
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ax.plot(data['job_ratio']['date'], data['job_ratio']['ratio'], color=PALETTE['ocean_blue'], linewidth=2,
            label='Job Openings / Unemployed')
    # Horizontal line at 1
    ax.axhline(1, color=PALETTE['sunset_orange'], linestyle='--', linewidth=1.5, label='Ratio = 1')
    # Format axes
    ax.set_title('Labor Market Balance: Job Openings vs Unemployment', fontsize=13, weight='bold', pad=10)
    ax.set_xlabel('Year', fontsize=10)
    ax.set_ylabel('Ratio', fontsize=10)
    style_axes(ax)
    # Date formatting
    ax.xaxis.set_major_locator(mdates.YearLocator(base=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    # Legend at upper left with white background
    legend = ax.legend(loc='upper left', bbox_to_anchor=(0.0, 1.0), framealpha=0.9, facecolor='white', edgecolor='none', fontsize=9)
    # Add watermark and source
    add_watermark(ax, wm, scale=0.20, xoff=0.88, yoff=0.15)
    add_source(ax, 'Source: Lighthouse Macro, FRED (JTSJOL, UNEMPLOY)')
    save_fig(fig, 'chart01_job_openings_ratio.png')

    ###############################################
    # Chart 2: Quits vs hires rate and hire-to-quit ratio
    ###############################################
    fig, ax1 = plt.subplots(figsize=(8.5, 4.5))
    # left axis for hires to quits ratio; right axis for rates
    ax1.plot(data['churn']['date'], data['churn']['hire_to_quit'], color=PALETTE['carolina_blue'], linewidth=2,
             label='Hires/Quits Ratio')
    ax1.set_ylabel('Hires/Quits Ratio', color=PALETTE['carolina_blue'], fontsize=10)
    ax1.tick_params(axis='y', labelcolor=PALETTE['carolina_blue'])
    # style only spines; we keep axis on right for left axis? We'll treat this as secondary axis to left.
    ax1.yaxis.tick_left()
    ax1.yaxis.set_label_position('left')
    for spine in ['top', 'bottom', 'left', 'right']:
        ax1.spines[spine].set_color(PALETTE['gray'])
    # Create a secondary axis on the right for quits and hires rate
    ax2 = ax1.twinx()
    ax2.plot(data['churn']['date'], data['churn']['quits'], color=PALETTE['ocean_blue'], linewidth=2, label='Quits Rate')
    ax2.plot(data['churn']['date'], data['churn']['hires'], color=PALETTE['sunset_orange'], linewidth=2, label='Hires Rate')
    ax2.set_ylabel('Rate (%)', fontsize=10)
    # Format axes and ticks
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position('right')
    # Title and x-axis
    ax1.set_title('Labor Market Churn: Quits vs Hires and Hiring Intensity', fontsize=13, weight='bold', pad=10)
    ax1.set_xlabel('Year', fontsize=10)
    # Date formatting
    ax1.xaxis.set_major_locator(mdates.YearLocator(base=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    # Combine legends
    lines = ax1.get_lines() + ax2.get_lines()
    labels = [l.get_label() for l in lines]
    ax2.legend(lines, labels, loc='upper left', bbox_to_anchor=(0.0, 1.0), framealpha=0.9, facecolor='white', edgecolor='none', fontsize=9)
    # Grid and spines on both axes
    for ax_tmp in [ax1, ax2]:
        ax_tmp.grid(axis='y', linestyle='--', linewidth=0.6, color='#e0e0e0', zorder=0)
        for spine in ax_tmp.spines.values():
            spine.set_color(PALETTE['gray'])
    # Watermark and source
    add_watermark(ax2, wm, scale=0.18, xoff=0.88, yoff=0.15)
    add_source(ax2, 'Source: Lighthouse Macro, FRED (JTSQUR, JTSHIR)')
    save_fig(fig, 'chart02_quits_hires.png')

    ###############################################
    # Chart 3: Labour supply – LFPR vs prime‑age EPOP and their spread
    ###############################################
    fig, ax1 = plt.subplots(figsize=(8.5, 4.5))
    # Spread as area on left axis (left). Ensure numeric type to avoid masked_invalid errors.
    # Convert series to numeric array and coerce non-finite to NaN
    spread_vals = pd.to_numeric(data['supply']['epop_minus_lfpr'], errors='coerce').astype(float).values
    # Replace NaN with zero for the area fill to avoid type issues
    spread_vals_fill = pd.Series(spread_vals).fillna(0).values
    # Convert date to matplotlib numeric format to work with fill_between (avoids numpy isfinite on datetime64)
    x_dates = mdates.date2num(data['supply']['date'].to_numpy())
    zeros = [0.0] * len(spread_vals_fill)
    ax1.fill_between(x_dates, zeros, spread_vals_fill, color=PALETTE['magenta'], alpha=0.2,
                     label='EPOP minus LFPR')
    ax1.set_ylabel('Difference (pp)', color=PALETTE['magenta'], fontsize=10)
    ax1.yaxis.tick_left()
    ax1.yaxis.set_label_position('left')
    ax1.tick_params(axis='y', labelcolor=PALETTE['magenta'])
    # Secondary axis for LFPR and EPOP on right
    ax2 = ax1.twinx()
    ax2.plot(data['supply']['date'], data['supply']['lfpr'], color=PALETTE['ocean_blue'], linewidth=2, label='LFPR')
    ax2.plot(data['supply']['date'], data['supply']['epop'], color=PALETTE['sunset_orange'], linewidth=2, label='Prime‑age EPOP')
    ax2.set_ylabel('Rate (%)', fontsize=10)
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position('right')
    # Title and x-axis
    ax1.set_title('Labour Supply: Participation vs Employment and Spread', fontsize=13, weight='bold', pad=10)
    ax1.set_xlabel('Year', fontsize=10)
    ax1.xaxis.set_major_locator(mdates.YearLocator(base=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    # Legends
    # Compose legend entries from both axes
    lines = [ax1.collections[0]] + ax2.get_lines()
    labels = ['EPOP – LFPR'] + [l.get_label() for l in ax2.get_lines()]
    ax2.legend(lines, labels, loc='upper left', bbox_to_anchor=(0.0, 1.0), framealpha=0.9,
               facecolor='white', edgecolor='none', fontsize=9)
    # Style spines
    for ax_tmp in [ax1, ax2]:
        for spine in ax_tmp.spines.values():
            spine.set_color(PALETTE['gray'])
        ax_tmp.grid(axis='y', linestyle='--', linewidth=0.6, color='#e0e0e0', zorder=0)
    # Watermark and source
    add_watermark(ax2, wm, scale=0.18, xoff=0.88, yoff=0.15)
    add_source(ax2, 'Source: Lighthouse Macro, FRED (CIVPART, LNS12300060)')
    save_fig(fig, 'chart03_lfpr_epop.png')

    ###############################################
    # Chart 4: Unemployment vs underemployment and their gap
    ###############################################
    fig, ax1 = plt.subplots(figsize=(8.5, 4.5))
    # Gap on left axis
    ax1.plot(data['un']['date'], data['un']['u_gap'], color=PALETTE['magenta'], linewidth=2, label='U6 – U3 Gap')
    ax1.set_ylabel('Gap (pp)', color=PALETTE['magenta'], fontsize=10)
    ax1.yaxis.tick_left()
    ax1.yaxis.set_label_position('left')
    ax1.tick_params(axis='y', labelcolor=PALETTE['magenta'])
    # Secondary axis for U3 and U6 on right
    ax2 = ax1.twinx()
    ax2.plot(data['un']['date'], data['un']['u3'], color=PALETTE['ocean_blue'], linewidth=2, label='U‑3 Unemployment')
    ax2.plot(data['un']['date'], data['un']['u6'], color=PALETTE['sunset_orange'], linewidth=2, label='U‑6 Underemployment')
    ax2.set_ylabel('Rate (%)', fontsize=10)
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position('right')
    # Title and x-axis
    ax1.set_title('Unemployment vs Underemployment and Slack Gap', fontsize=13, weight='bold', pad=10)
    ax1.set_xlabel('Year', fontsize=10)
    ax1.xaxis.set_major_locator(mdates.YearLocator(base=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    # Legend
    lines = [ax1.get_lines()[0]] + ax2.get_lines()
    labels = ['U6 – U3 Gap'] + [l.get_label() for l in ax2.get_lines()]
    ax2.legend(lines, labels, loc='upper left', bbox_to_anchor=(0.0, 1.0), framealpha=0.9,
               facecolor='white', edgecolor='none', fontsize=9)
    # Style and grid
    for ax_tmp in [ax1, ax2]:
        for spine in ax_tmp.spines.values():
            spine.set_color(PALETTE['gray'])
        ax_tmp.grid(axis='y', linestyle='--', linewidth=0.6, color='#e0e0e0', zorder=0)
    # Watermark and source
    add_watermark(ax2, wm, scale=0.18, xoff=0.88, yoff=0.15)
    add_source(ax2, 'Source: Lighthouse Macro, FRED (UNRATE, U6RATE)')
    save_fig(fig, 'chart04_un_u6_gap.png')

    ###############################################
    # Chart 5: Wage dynamics – nominal, CPI inflation, real, and real wage index
    ###############################################
    fig, ax1 = plt.subplots(figsize=(8.5, 4.5))
    # Real wage index as left axis
    ax1.plot(data['real_wage_index']['date'], data['real_wage_index']['real_wage_index'],
             color=PALETTE['carolina_blue'], linewidth=2, label='Real Wage Index (base=100)')
    ax1.set_ylabel('Real Wage Index', color=PALETTE['carolina_blue'], fontsize=10)
    ax1.yaxis.tick_left()
    ax1.yaxis.set_label_position('left')
    ax1.tick_params(axis='y', labelcolor=PALETTE['carolina_blue'])
    # Secondary axis for nominal, inflation and real wage growth
    ax2 = ax1.twinx()
    ax2.plot(data['w_cpi']['date'], data['w_cpi']['wage_growth'], color=PALETTE['ocean_blue'], linewidth=2, label='Nominal Wage Growth')
    ax2.plot(data['w_cpi']['date'], data['w_cpi']['cpi_inflation'], color=PALETTE['sunset_orange'], linewidth=2, label='CPI Inflation')
    ax2.plot(data['w_cpi']['date'], data['w_cpi']['real_wage'], color=PALETTE['magenta'], linewidth=2, label='Real Wage Growth')
    ax2.set_ylabel('YoY Growth (%)', fontsize=10)
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position('right')
    # Titles and axis
    ax1.set_title('Wage Dynamics: Nominal vs Inflation and Real Wage Index', fontsize=13, weight='bold', pad=10)
    ax1.set_xlabel('Year', fontsize=10)
    ax1.xaxis.set_major_locator(mdates.YearLocator(base=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    # Legend
    lines = [ax1.get_lines()[0]] + ax2.get_lines()
    labels = ['Real Wage Index'] + [l.get_label() for l in ax2.get_lines()]
    ax2.legend(lines, labels, loc='upper left', bbox_to_anchor=(0.0, 1.0), framealpha=0.9,
               facecolor='white', edgecolor='none', fontsize=9)
    # Style
    for ax_tmp in [ax1, ax2]:
        for spine in ax_tmp.spines.values():
            spine.set_color(PALETTE['gray'])
        ax_tmp.grid(axis='y', linestyle='--', linewidth=0.6, color='#e0e0e0', zorder=0)
    # Watermark and source
    add_watermark(ax2, wm, scale=0.18, xoff=0.88, yoff=0.15)
    add_source(ax2, 'Source: Lighthouse Macro, FRED (CES05…, CPIAUCSL)')
    save_fig(fig, 'chart05_wage_dynamics.png')

    ###############################################
    # Chart 6: Long-term unemployment share comparison (bar chart)
    ###############################################
    # Hard-coded long-term unemployment shares; update as new data becomes available
    lt_df = pd.DataFrame({
        'Period': ['Pre‑Pandemic (2019)', 'Post‑Recession (2014)', 'Aug 2025'],
        'Share': [21.1, 19.5, 25.7],
        'Colour': [PALETTE['ocean_blue'], PALETTE['carolina_blue'], PALETTE['sunset_orange']]
    })
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    bars = ax.bar(lt_df['Period'], lt_df['Share'], color=lt_df['Colour'], width=0.6)
    for idx, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, f"{height:.1f}%", ha='center', va='bottom', fontsize=9, weight='bold')
    ax.set_title('Long‑term Unemployment Share Comparison', fontsize=13, weight='bold', pad=10)
    ax.set_ylabel('Share of Unemployed (%)', fontsize=10)
    ax.set_ylim(0, 30)
    # Style spines and ticks
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position('right')
    for spine in ax.spines.values():
        spine.set_color(PALETTE['gray'])
    ax.grid(axis='y', linestyle='--', linewidth=0.6, color='#e0e0e0', zorder=0)
    # Legend substitute: none; colours implicitly encoded
    # Watermark and source
    add_watermark(ax, wm, scale=0.22, xoff=0.88, yoff=0.15)
    add_source(ax, 'Source: BLS – Current Population Survey (Calculation by LHM)')
    save_fig(fig, 'chart06_longterm_unemploy_share.png')

    ###############################################
    # Chart 7: Labour market slack – difference between job openings and unemployed
    ###############################################
    slack = data['job_ratio'].copy()
    # Compute slack and ensure numeric
    slack['slack'] = pd.to_numeric(slack['JTSJOL'], errors='coerce') - pd.to_numeric(slack['UNEMPLOY'], errors='coerce')
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    # Convert dates to numeric for fill_between
    x_slack = mdates.date2num(slack['date'].to_numpy())
    slack_vals = pd.to_numeric(slack['slack'], errors='coerce').astype(float) / 1000.0  # thousands
    import numpy as _np
    zeros_slack = _np.zeros_like(slack_vals, dtype=float)
    # Ensure arrays for where mask
    slack_vals_arr = _np.asarray(slack_vals, dtype=float)
    ax.fill_between(x_slack, zeros_slack, slack_vals_arr, where=slack_vals_arr>=0,
                    color=PALETTE['carolina_blue'], alpha=0.4, label='Excess Job Openings')
    ax.fill_between(x_slack, zeros_slack, slack_vals_arr, where=slack_vals_arr<0,
                    color=PALETTE['sunset_orange'], alpha=0.4, label='Excess Unemployed')
    ax.set_title('Labour Market Slack: Job Openings – Unemployed', fontsize=13, weight='bold', pad=10)
    ax.set_xlabel('Year', fontsize=10)
    ax.set_ylabel('Difference (k)', fontsize=10)
    # Primary axis right
    style_axes(ax)
    # Date formatting
    ax.xaxis.set_major_locator(mdates.YearLocator(base=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    # Legend
    ax.legend(loc='upper left', bbox_to_anchor=(0.0, 1.0), framealpha=0.9, facecolor='white', edgecolor='none', fontsize=9)
    # Watermark and source
    add_watermark(ax, wm, scale=0.20, xoff=0.88, yoff=0.15)
    add_source(ax, 'Source: Lighthouse Macro, FRED (JTSJOL, UNEMPLOY)')
    save_fig(fig, 'chart07_labor_slack.png')

    ###############################################
    # Chart 8: Spread between prime-age EPOP and LFPR vs unemployment gap
    ###############################################
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ax.plot(data['supply']['date'], data['supply']['epop_minus_lfpr'], color=PALETTE['carolina_blue'], linewidth=2,
            label='EPOP – LFPR')
    # Second series: U6 – U3 gap, same axis to simplify view
    ax.plot(data['un']['date'], data['un']['u_gap'], color=PALETTE['sunset_orange'], linewidth=2, label='U6 – U3 Gap')
    ax.set_title('Labour Supply Spread vs Underemployment Gap', fontsize=13, weight='bold', pad=10)
    ax.set_xlabel('Year', fontsize=10)
    ax.set_ylabel('Difference (pp)', fontsize=10)
    style_axes(ax)
    ax.xaxis.set_major_locator(mdates.YearLocator(base=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.legend(loc='upper left', bbox_to_anchor=(0.0, 1.0), framealpha=0.9, facecolor='white', edgecolor='none', fontsize=9)
    add_watermark(ax, wm, scale=0.20, xoff=0.88, yoff=0.15)
    add_source(ax, 'Source: Lighthouse Macro, FRED')
    save_fig(fig, 'chart08_spread_gap.png')

    ###############################################
    # Chart 9: Hires vs Quits ratio correlation with real wage growth
    ###############################################
    # Align series by date intersection
    hires_quits = data['churn'][['date', 'hire_to_quit']]
    real_wage = data['w_cpi'][['date', 'real_wage']]
    corr_df = hires_quits.merge(real_wage, on='date', how='inner').dropna()
    fig, ax = plt.subplots(figsize=(6.5, 5.0))
    ax.scatter(corr_df['hire_to_quit'], corr_df['real_wage'], color=PALETTE['ocean_blue'], alpha=0.5)
    # Fit a simple trend line
    if len(corr_df) > 2:
        m, b = np.polyfit(corr_df['hire_to_quit'], corr_df['real_wage'], 1)
        x_vals = np.linspace(corr_df['hire_to_quit'].min(), corr_df['hire_to_quit'].max(), 100)
        ax.plot(x_vals, m * x_vals + b, color=PALETTE['sunset_orange'], linewidth=2,
                label=f'Trend: slope={m:.2f}')
    ax.set_title('Hires/Quits Ratio vs Real Wage Growth', fontsize=13, weight='bold', pad=10)
    ax.set_xlabel('Hires/Quits Ratio', fontsize=10)
    ax.set_ylabel('Real Wage Growth (%)', fontsize=10)
    # Spines style
    for spine in ax.spines.values():
        spine.set_color(PALETTE['gray'])
    # Legend
    ax.legend(loc='upper left', bbox_to_anchor=(0.0, 1.0), framealpha=0.9, facecolor='white', edgecolor='none', fontsize=9)
    # Add grid
    ax.grid(True, linestyle='--', linewidth=0.6, color='#e0e0e0', zorder=0)
    # Watermark and source
    add_watermark(ax, wm, scale=0.25, xoff=0.80, yoff=0.15)
    add_source(ax, 'Source: Lighthouse Macro, FRED (JTSQUR, JTSHIR, CES05…, CPIAUCSL)')
    save_fig(fig, 'chart09_hire_quit_vs_real_wage.png')

    ###############################################
    # Chart 10: Real wage growth vs unemployment gap over time
    ###############################################
    # Align series
    gap = data['un'][['date', 'u_gap']]
    real = data['w_cpi'][['date', 'real_wage']]
    merge_df = gap.merge(real, on='date', how='inner').dropna()
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    # dual axis: left for real wage, right for gap
    ax_left = ax
    ax_left.plot(merge_df['date'], merge_df['real_wage'], color=PALETTE['ocean_blue'], linewidth=2, label='Real Wage Growth')
    ax_left.set_ylabel('Real Wage Growth (%)', color=PALETTE['ocean_blue'], fontsize=10)
    ax_left.yaxis.tick_left()
    ax_left.yaxis.set_label_position('left')
    ax_left.tick_params(axis='y', labelcolor=PALETTE['ocean_blue'])
    ax_right = ax.twinx()
    ax_right.plot(merge_df['date'], merge_df['u_gap'], color=PALETTE['sunset_orange'], linewidth=2, label='U6 – U3 Gap')
    ax_right.set_ylabel('Gap (pp)', color=PALETTE['sunset_orange'], fontsize=10)
    ax_right.yaxis.tick_right()
    ax_right.yaxis.set_label_position('right')
    ax_right.tick_params(axis='y', labelcolor=PALETTE['sunset_orange'])
    # Title and x-axis
    ax_left.set_title('Real Wage Growth vs Underemployment Gap', fontsize=13, weight='bold', pad=10)
    ax_left.set_xlabel('Year', fontsize=10)
    ax_left.xaxis.set_major_locator(mdates.YearLocator(base=5))
    ax_left.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    # Legend
    lines = ax_left.get_lines() + ax_right.get_lines()
    labels = [l.get_label() for l in lines]
    ax_right.legend(lines, labels, loc='upper left', bbox_to_anchor=(0.0, 1.0), framealpha=0.9,
                    facecolor='white', edgecolor='none', fontsize=9)
    # Style spines
    for ax_tmp in [ax_left, ax_right]:
        for spine in ax_tmp.spines.values():
            spine.set_color(PALETTE['gray'])
        ax_tmp.grid(axis='y', linestyle='--', linewidth=0.6, color='#e0e0e0', zorder=0)
    # Watermark and source
    add_watermark(ax_right, wm, scale=0.18, xoff=0.88, yoff=0.15)
    add_source(ax_right, 'Source: Lighthouse Macro, FRED')
    save_fig(fig, 'chart10_real_wage_vs_gap.png')

    ###############################################
    # Chart 11: Dashboard – Macro Labour Overview (4 panels)
    ###############################################
    fig, axs = plt.subplots(2, 2, figsize=(10, 7))
    # Panel A: Job ratio
    ax = axs[0, 0]
    ax.plot(data['job_ratio']['date'], data['job_ratio']['ratio'], color=PALETTE['ocean_blue'], linewidth=1.5, label='Job Openings/Unemployed')
    ax.axhline(1, color=PALETTE['sunset_orange'], linestyle='--', linewidth=1, label='Ratio = 1')
    ax.set_title('Job Openings Ratio', fontsize=11, weight='bold')
    ax.xaxis.set_major_locator(mdates.YearLocator(base=10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    style_axes(ax)
    ax.legend(loc='upper left', fontsize=7, framealpha=0.9, facecolor='white', edgecolor='none')
    add_source(ax, '')  # leave blank to avoid duplication

    # Panel B: Churn (Quits vs Hires)
    ax = axs[0, 1]
    ax.plot(data['churn']['date'], data['churn']['quits'], color=PALETTE['ocean_blue'], linewidth=1.5, label='Quits Rate')
    ax.plot(data['churn']['date'], data['churn']['hires'], color=PALETTE['sunset_orange'], linewidth=1.5, label='Hires Rate')
    ax.set_title('Quits vs Hires', fontsize=11, weight='bold')
    ax.xaxis.set_major_locator(mdates.YearLocator(base=10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    style_axes(ax)
    ax.legend(loc='upper left', fontsize=7, framealpha=0.9, facecolor='white', edgecolor='none')
    add_source(ax, '')

    # Panel C: U Gap vs Real Wage (simplified)
    ax = axs[1, 0]
    ax.plot(merge_df['date'], merge_df['u_gap'], color=PALETTE['sunset_orange'], linewidth=1.5, label='U6 – U3 Gap')
    ax.plot(merge_df['date'], merge_df['real_wage'], color=PALETTE['carolina_blue'], linewidth=1.5, label='Real Wage Growth')
    ax.set_title('Gap vs Real Wage Growth', fontsize=11, weight='bold')
    ax.xaxis.set_major_locator(mdates.YearLocator(base=10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    style_axes(ax)
    ax.legend(loc='upper left', fontsize=7, framealpha=0.9, facecolor='white', edgecolor='none')
    add_source(ax, '')

    # Panel D: Labour Supply Spread
    ax = axs[1, 1]
    ax.plot(data['supply']['date'], data['supply']['epop_minus_lfpr'], color=PALETTE['magenta'], linewidth=1.5, label='EPOP – LFPR')
    ax.set_title('EPOP – LFPR Spread', fontsize=11, weight='bold')
    ax.xaxis.set_major_locator(mdates.YearLocator(base=10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    style_axes(ax)
    ax.legend(loc='upper left', fontsize=7, framealpha=0.9, facecolor='white', edgecolor='none')
    add_source(ax, '')

    # Global adjustments for the dashboard
    fig.suptitle('Macro Labour Overview', fontsize=14, weight='bold', y=0.98)
    # Add watermark to the last axis only to avoid clutter
    add_watermark(axs[1, 1], wm, scale=0.15, xoff=0.88, yoff=0.25)
    # Global source note below entire figure
    fig.text(1.0, -0.02, 'Source: Lighthouse Macro, FRED/BLS', ha='right', va='top', fontsize=8, color=PALETTE['gray'])
    save_fig(fig, 'chart11_dashboard_overview.png')

    ###############################################
    # Chart 12: Dashboard – Wage, Inflation & Labour Slack (4 panels)
    ###############################################
    fig, axs = plt.subplots(2, 2, figsize=(10, 7))
    # Panel A: Nominal vs CPI inflation
    ax = axs[0, 0]
    ax.plot(data['w_cpi']['date'], data['w_cpi']['wage_growth'], color=PALETTE['ocean_blue'], linewidth=1.5, label='Nominal Wage Growth')
    ax.plot(data['w_cpi']['date'], data['w_cpi']['cpi_inflation'], color=PALETTE['sunset_orange'], linewidth=1.5, label='CPI Inflation')
    ax.set_title('Nominal Wages vs CPI', fontsize=11, weight='bold')
    ax.xaxis.set_major_locator(mdates.YearLocator(base=10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    style_axes(ax)
    ax.legend(loc='upper left', fontsize=7, framealpha=0.9, facecolor='white', edgecolor='none')
    add_source(ax, '')

    # Panel B: Real wage index
    ax = axs[0, 1]
    ax.plot(data['real_wage_index']['date'], data['real_wage_index']['real_wage_index'], color=PALETTE['carolina_blue'], linewidth=1.5, label='Real Wage Index')
    ax.set_title('Real Wage Index', fontsize=11, weight='bold')
    ax.xaxis.set_major_locator(mdates.YearLocator(base=10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    style_axes(ax)
    ax.legend(loc='upper left', fontsize=7, framealpha=0.9, facecolor='white', edgecolor='none')
    add_source(ax, '')

    # Panel C: Labour slack difference
    ax = axs[1, 0]
    # Convert dates to numeric for fill_between in panel C
    x_slack_panel = mdates.date2num(slack['date'].to_numpy())
    slack_vals_panel = pd.to_numeric(slack['slack'], errors='coerce').astype(float) / 1000.0
    import numpy as _np
    zeros_panel = _np.zeros_like(slack_vals_panel, dtype=float)
    slack_vals_panel_arr = _np.asarray(slack_vals_panel, dtype=float)
    ax.fill_between(x_slack_panel, zeros_panel, slack_vals_panel_arr, where=slack_vals_panel_arr>=0,
                    color=PALETTE['carolina_blue'], alpha=0.4)
    ax.fill_between(x_slack_panel, zeros_panel, slack_vals_panel_arr, where=slack_vals_panel_arr<0,
                    color=PALETTE['sunset_orange'], alpha=0.4)
    ax.set_title('Labour Slack (k)', fontsize=11, weight='bold')
    ax.xaxis.set_major_locator(mdates.YearLocator(base=10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    style_axes(ax)
    ax.legend(['Excess Job Openings','Excess Unemployed'], loc='upper left', fontsize=7, framealpha=0.9, facecolor='white', edgecolor='none')
    add_source(ax, '')

    # Panel D: Hires to Quits ratio
    ax = axs[1, 1]
    ax.plot(data['churn']['date'], data['churn']['hire_to_quit'], color=PALETTE['magenta'], linewidth=1.5, label='Hires/Quits Ratio')
    ax.set_title('Hires/Quits Ratio', fontsize=11, weight='bold')
    ax.xaxis.set_major_locator(mdates.YearLocator(base=10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    style_axes(ax)
    ax.legend(loc='upper left', fontsize=7, framealpha=0.9, facecolor='white', edgecolor='none')
    add_source(ax, '')

    fig.suptitle('Wages, Inflation & Labour Slack', fontsize=14, weight='bold', y=0.98)
    add_watermark(axs[1, 1], wm, scale=0.15, xoff=0.88, yoff=0.25)
    fig.text(1.0, -0.02, 'Source: Lighthouse Macro, FRED/BLS', ha='right', va='top', fontsize=8, color=PALETTE['gray'])
    save_fig(fig, 'chart12_dashboard_wage_slack.png')

    ###############################################
    # Chart 13: Custom LHM indicator – "Recalibration Index"
    ###############################################
    # A simple indicator combining job ratio, real wage growth and unemployment gap.
    # We normalise each component to mean 0 and std 1, then average.
    df_tmp = data['job_ratio'][['date', 'ratio']].merge(data['w_cpi'][['date', 'real_wage']], on='date', how='inner')
    df_tmp = df_tmp.merge(data['un'][['date', 'u_gap']], on='date', how='inner').dropna()
    from scipy.stats import zscore
    df_tmp['ratio_z'] = zscore(df_tmp['ratio'])
    df_tmp['real_wage_z'] = zscore(df_tmp['real_wage'])
    df_tmp['u_gap_z'] = zscore(df_tmp['u_gap'])
    # Recalibration index: positive when job ratio high and wage growth high but unemployment gap low (tight labour)
    df_tmp['recalibration_index'] = (df_tmp['ratio_z'] + df_tmp['real_wage_z'] - df_tmp['u_gap_z']) / 3
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ax.plot(df_tmp['date'], df_tmp['recalibration_index'], color=PALETTE['ocean_blue'], linewidth=2)
    ax.axhline(0, color=PALETTE['gray'], linewidth=1, linestyle='--')
    ax.set_title('LHM Recalibration Index (z‑score composite)', fontsize=13, weight='bold', pad=10)
    ax.set_xlabel('Year', fontsize=10)
    ax.set_ylabel('Standardised Index', fontsize=10)
    style_axes(ax)
    ax.xaxis.set_major_locator(mdates.YearLocator(base=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.legend(['Recalibration Index'], loc='upper left', bbox_to_anchor=(0.0, 1.0), framealpha=0.9,
              facecolor='white', edgecolor='none', fontsize=9)
    add_watermark(ax, wm, scale=0.20, xoff=0.88, yoff=0.15)
    add_source(ax, 'Source: Lighthouse Macro, FRED – Composite Calculation')
    save_fig(fig, 'chart13_recalibration_index.png')

    ###############################################
    # Chart 14: Real wage index and job openings ratio overlay
    ###############################################
    # Align series and normalise both to 100 at a common start date
    base_date = max(data['real_wage_index']['date'].min(), data['job_ratio']['date'].min())
    idx_df = data['real_wage_index'][['date', 'real_wage_index']].merge(
        data['job_ratio'][['date', 'ratio']], on='date', how='inner').dropna()
    idx_df['rw_norm'] = (idx_df['real_wage_index'] / idx_df['real_wage_index'].iloc[0]) * 100
    idx_df['ratio_norm'] = (idx_df['ratio'] / idx_df['ratio'].iloc[0]) * 100
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ax.plot(idx_df['date'], idx_df['rw_norm'], color=PALETTE['ocean_blue'], linewidth=2, label='Real Wage Index (norm)')
    ax.plot(idx_df['date'], idx_df['ratio_norm'], color=PALETTE['sunset_orange'], linewidth=2, label='Job Ratio (norm)')
    ax.set_title('Indexed Real Wages vs Job Openings Ratio', fontsize=13, weight='bold', pad=10)
    ax.set_xlabel('Year', fontsize=10)
    ax.set_ylabel('Index (100 = start)', fontsize=10)
    style_axes(ax)
    ax.xaxis.set_major_locator(mdates.YearLocator(base=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.legend(loc='upper left', bbox_to_anchor=(0.0, 1.0), framealpha=0.9,
              facecolor='white', edgecolor='none', fontsize=9)
    add_watermark(ax, wm, scale=0.20, xoff=0.88, yoff=0.15)
    add_source(ax, 'Source: Lighthouse Macro, FRED')
    save_fig(fig, 'chart14_indexed_rw_vs_ratio.png')

    ###############################################
    # Chart 15: Underemployment share vs hires/quit ratio scatter with density hue
    ###############################################
    # Create scatter of U6 share vs hires/quits; compute hires/quits ratio again
    hires_quits_df = data['churn'][['date', 'hire_to_quit']]
    u6_share = data['un'][['date', 'u6']]
    scatter_df = hires_quits_df.merge(u6_share, on='date', how='inner').dropna()
    # Ensure numeric types for plotting
    scatter_df['hire_to_quit'] = pd.to_numeric(scatter_df['hire_to_quit'], errors='coerce').astype(float)
    scatter_df['u6'] = pd.to_numeric(scatter_df['u6'], errors='coerce').astype(float)
    fig, ax = plt.subplots(figsize=(6.5, 5.0))
    # Use point size to encode time order (recent points larger)
    sizes = np.linspace(20, 100, len(scatter_df))
    sc = ax.scatter(scatter_df['hire_to_quit'], scatter_df['u6'], c=scatter_df['u6'], cmap='coolwarm', s=sizes, alpha=0.7)
    ax.set_title('Underemployment Rate vs Hires/Quits Ratio', fontsize=13, weight='bold', pad=10)
    ax.set_xlabel('Hires/Quits Ratio', fontsize=10)
    ax.set_ylabel('U6 Rate (%)', fontsize=10)
    for spine in ax.spines.values():
        spine.set_color(PALETTE['gray'])
    ax.grid(True, linestyle='--', linewidth=0.6, color='#e0e0e0', zorder=0)
    # Colourbar
    cbar = plt.colorbar(sc, ax=ax, orientation='vertical', pad=0.02)
    cbar.set_label('U6 Rate (%)', fontsize=9)
    # Watermark and source
    add_watermark(ax, wm, scale=0.25, xoff=0.80, yoff=0.15)
    add_source(ax, 'Source: Lighthouse Macro, FRED (JTSHIR, JTSQUR, U6RATE)')
    save_fig(fig, 'chart15_u6_vs_hire_quit.png')


if __name__ == '__main__':
    import numpy as np  # local import for scatter/regressions
    plot_all()