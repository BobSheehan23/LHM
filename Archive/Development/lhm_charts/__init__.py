# === LHM one-cell plotting toolkit (golden ratio, 85% plot area, dual-axis support) ===
import os, datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Optional import for pandas_datareader
try:
    from pandas_datareader import data as pdr
    PANDAS_DATAREADER_AVAILABLE = True
except ImportError:
    pdr = None
    PANDAS_DATAREADER_AVAILABLE = False

# ---------- config ----------
PHI = 1.61803398875
FIG_WIDTH = 12.0
FIG_HEIGHT = FIG_WIDTH / PHI          # golden ratio
OUTDIR = "charts"
os.makedirs(OUTDIR, exist_ok=True)

# Axes rectangle (left, bottom, width, height) in figure coords.
# 0.95 * 0.90 ≈ 0.855 → ~85% of total figure area devoted to plotting region.
AX_RECT = (0.025, 0.10, 0.95, 0.90)

# Palette
OCEAN_BLUE    = "#005F9E"   # primary
SUNSET_ORANGE = "#FF6B35"   # secondary (deep neon orange)
CAROLINA_BLUE = "#1DAEFF"   # tertiary (neon carolina blue)
MAGENTA       = "#FF4FB3"   # 4th (neon magenta)
LIGHT_GRAY    = "#B0B0B0"   # 5th
MID_GRAY      = "#7A7A7A"
BLACK         = "#000000"

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": MID_GRAY,
    "axes.labelcolor": BLACK,
    "xtick.color": MID_GRAY,
    "ytick.color": MID_GRAY,
    "axes.grid": False,
    "legend.frameon": True,
    "legend.facecolor": "white",
    "legend.edgecolor": "none",
    "legend.loc": "upper left",
    "savefig.facecolor": "white",
    "savefig.bbox": "tight",
    "figure.dpi": 160,
    "lines.linewidth": 2.0,
})

# ---------- utils ----------
def fred_fetch(codes, start="1995-01-01", end=None):
    """Fetch FRED data. codes can be string or list."""
    if not PANDAS_DATAREADER_AVAILABLE:
        raise ImportError("pandas_datareader is required for fred_fetch. Install with: pip install pandas-datareader")

    if isinstance(codes, str):
        codes = [codes]
    end = end or dt.date.today().isoformat()
    out = pd.DataFrame()
    for c in codes:
        s = pdr.DataReader(c, "fred", start=start, end=end)
        out[c] = s[c]
    out.index = pd.DatetimeIndex(out.index).tz_localize(None)
    return out

def yoy(s, periods=12):
    """Year-over-year % change."""
    return s.pct_change(periods, fill_method=None) * 100.0

def last_valid_value(series):
    """Return last valid value or None."""
    s = pd.Series(series).dropna()
    return None if s.empty else float(s.iloc[-1])

def _luma(hex_color):
    """Calculate relative luminance for text color selection."""
    hc = hex_color.lstrip("#")
    r, g, b = [int(hc[i:i+2], 16)/255 for i in (0, 2, 4)]
    def lin(c): return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
    R, G, B = lin(r), lin(g), lin(b)
    return 0.2126*R + 0.7152*G + 0.0722*B

def lastvalue_label(ax, y, color, mode="fill", fmt="{:,.2f}", side="right"):
    """Add last-value label on right axis."""
    if y is None or (isinstance(y, float) and (np.isnan(y) or np.isinf(y))):
        return
    text_color = "#FFF" if _luma(color) < 0.35 else "#111"
    fc, ec = (color, "none") if mode == "fill" else ("#FFF", color)
    txt = text_color if mode == "fill" else color

    x_pos = 1.0 if side == "right" else 0.0
    ha = "right" if side == "right" else "left"

    ax.annotate(
        fmt.format(float(y)),
        xy=(x_pos, y),
        xycoords=("axes fraction", "data"),
        xytext=(0, 0),
        textcoords="offset points",
        ha=ha,
        va="center",
        bbox=dict(boxstyle="round,pad=0.25", fc=fc, ec=ec, lw=1, alpha=0.98),
        color=txt,
        fontsize=9
    )

def auto_left_xlim(ax):
    """Trim left bound to latest first-valid x among plotted lines."""
    starts = []
    for line in ax.get_lines():
        x = line.get_xdata(orig=False)
        y = line.get_ydata(orig=False)
        if x is None or y is None:
            continue
        y = np.asarray(y, dtype=float)
        m = np.isfinite(y)
        if m.any():
            starts.append(np.asarray(x)[m][0])
    if starts:
        ax.set_xlim(left=max(starts))

# Recessions (tz-naive) + clamped shading
_RECESSIONS = None

def recessions():
    """Load NBER recession dates (tz-naive)."""
    if not PANDAS_DATAREADER_AVAILABLE:
        raise ImportError("pandas_datareader is required for recession data. Install with: pip install pandas-datareader")

    global _RECESSIONS
    if _RECESSIONS is not None:
        return _RECESSIONS
    rec = pdr.DataReader("USREC", "fred", "1950-01-01").astype(int)
    rec.index = pd.DatetimeIndex(rec.index).tz_localize(None)
    sw = rec["USREC"].shift(1, fill_value=0)
    starts = rec.index[(rec["USREC"] == 1) & (sw == 0)]
    ends = rec.index[(rec["USREC"] == 0) & (sw == 1)]
    if len(ends) < len(starts):
        ends = ends.append(pd.DatetimeIndex([rec.index[-1]]))
    _RECESSIONS = list(zip(starts, ends))
    return _RECESSIONS

def shade_recessions(ax, alpha=0.15, color=LIGHT_GRAY, zorder=1):
    """Shade recession periods, clamped to current axis xlim."""
    xl, xr = ax.get_xlim()
    xl_dt = mdates.num2date(xl).replace(tzinfo=None)
    xr_dt = mdates.num2date(xr).replace(tzinfo=None)
    for s, e in recessions():
        s_clamp = max(s, xl_dt)
        e_clamp = min(e, xr_dt)
        if s_clamp < e_clamp:
            ax.axvspan(s_clamp, e_clamp, color=color, alpha=alpha, zorder=zorder, lw=0)

def watermark(ax):
    """Add 'MACRO, ILLUMINATED.' watermark in bottom right."""
    ax.text(
        0.99, 0.01, "MACRO, ILLUMINATED.",
        transform=ax.transAxes,
        fontsize=10,
        color=OCEAN_BLUE,
        alpha=0.6,
        ha="right",
        va="bottom",
        style="italic",
        weight="bold"
    )

# ---------- Dual-axis chart builder ----------
def chart_dual(
    df,
    left_cols,
    right_cols,
    left_label="",
    right_label="",
    title="",
    left_color=OCEAN_BLUE,
    right_color=SUNSET_ORANGE,
    left_fmt="{:,.1f}",
    right_fmt="{:,.1f}",
    match_zero=True,
    left_log=False,
    right_log=False,
    filename=None,
    show_recessions=True,
    legend_loc="upper left"
):
    """
    Create dual-axis chart matching LHM standards.

    Parameters:
    -----------
    df : DataFrame with DatetimeIndex
    left_cols : list of column names for left axis
    right_cols : list of column names for right axis
    left_label : str, left y-axis label
    right_label : str, right y-axis label
    title : str, chart title
    left_color : hex color for left axis series
    right_color : hex color for right axis series
    left_fmt : format string for left axis labels
    right_fmt : format string for right axis labels
    match_zero : bool, if True align axes at zero
    left_log : bool, use log scale for left axis
    right_log : bool, use log scale for right axis
    filename : str, output filename (saves to OUTDIR)
    show_recessions : bool, shade recessions
    legend_loc : str, legend location
    """
    fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
    ax1 = fig.add_axes(AX_RECT)
    ax2 = ax1.twinx()

    # Ensure all spines visible
    for spine in ['top', 'bottom', 'left', 'right']:
        ax1.spines[spine].set_visible(True)
        ax1.spines[spine].set_color(MID_GRAY)
        ax1.spines[spine].set_linewidth(0.8)

    # Plot left axis series
    left_lines = []
    left_labels = []
    colors_left = [left_color, CAROLINA_BLUE, MAGENTA, LIGHT_GRAY]
    for i, col in enumerate(left_cols):
        if col not in df.columns:
            continue
        c = colors_left[i % len(colors_left)]
        line = ax1.plot(df.index, df[col], color=c, linewidth=2.0, label=col, zorder=5)[0]
        left_lines.append(line)
        left_labels.append(col)
        # Add last value label
        last_val = last_valid_value(df[col])
        if last_val is not None:
            lastvalue_label(ax1, last_val, c, fmt=left_fmt, side="left")

    # Plot right axis series
    right_lines = []
    right_labels = []
    colors_right = [right_color, MAGENTA, CAROLINA_BLUE, LIGHT_GRAY]
    for i, col in enumerate(right_cols):
        if col not in df.columns:
            continue
        c = colors_right[i % len(colors_right)]
        line = ax2.plot(df.index, df[col], color=c, linewidth=2.0, linestyle='--', label=col, zorder=5)[0]
        right_lines.append(line)
        right_labels.append(col)
        # Add last value label
        last_val = last_valid_value(df[col])
        if last_val is not None:
            lastvalue_label(ax2, last_val, c, fmt=right_fmt, side="right")

    # Set labels
    ax1.set_ylabel(left_label, color=BLACK, fontsize=11, weight='bold')
    ax2.set_ylabel(right_label, color=BLACK, fontsize=11, weight='bold')
    ax1.set_title(title, fontsize=13, weight='bold', pad=15, color=BLACK)

    # Color axis ticks
    ax1.tick_params(axis='y', colors=left_color, labelsize=9)
    ax2.tick_params(axis='y', colors=right_color, labelsize=9)
    ax1.tick_params(axis='x', labelsize=9)

    # Set log scales if requested
    if left_log:
        ax1.set_yscale('log')
    if right_log:
        ax2.set_yscale('log')

    # Match axes at zero if requested and not using log scale
    if match_zero and not left_log and not right_log:
        yl1 = ax1.get_ylim()
        yl2 = ax2.get_ylim()

        # Find the ratio needed to align zeros
        if yl1[0] <= 0 <= yl1[1] and yl2[0] <= 0 <= yl2[1]:
            # Both axes span zero
            ratio_left_neg = abs(yl1[0]) / (yl1[1] - yl1[0])
            ratio_left_pos = abs(yl1[1]) / (yl1[1] - yl1[0])
            ratio_right_neg = abs(yl2[0]) / (yl2[1] - yl2[0])
            ratio_right_pos = abs(yl2[1]) / (yl2[1] - yl2[0])

            # Use the larger range to set both
            if (yl1[1] - yl1[0]) > (yl2[1] - yl2[0]):
                # Scale right axis to match left
                new_yl2_min = -ratio_left_neg * (yl2[1] - yl2[0]) / ratio_left_pos
                new_yl2_max = ratio_left_pos * (yl2[1] - yl2[0]) / ratio_left_pos
                ax2.set_ylim(new_yl2_min, new_yl2_max)
            else:
                # Scale left axis to match right
                new_yl1_min = -ratio_right_neg * (yl1[1] - yl1[0]) / ratio_right_pos
                new_yl1_max = ratio_right_pos * (yl1[1] - yl1[0]) / ratio_right_pos
                ax1.set_ylim(new_yl1_min, new_yl1_max)

    # Recession shading (behind data)
    if show_recessions:
        shade_recessions(ax1, alpha=0.12, zorder=1)

    # Auto-adjust x-axis
    auto_left_xlim(ax1)

    # Combined legend
    all_lines = left_lines + right_lines
    all_labels = left_labels + right_labels
    if all_lines:
        ax1.legend(all_lines, all_labels, loc=legend_loc, frameon=True,
                  facecolor='white', edgecolor='none', fontsize=9)

    # Watermark
    watermark(ax1)

    # Date formatting
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax1.xaxis.set_major_locator(mdates.YearLocator(5))

    # Save
    if filename:
        path = os.path.join(OUTDIR, filename)
        plt.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"💾 Saved: {path}")

    plt.tight_layout()
    return fig, ax1, ax2

# ---------- Single-axis chart builder (enhanced) ----------
def chart(
    df,
    cols,
    ylabel="",
    title="",
    colors=None,
    fmt="{:,.1f}",
    log_scale=False,
    filename=None,
    show_recessions=True,
    legend_loc="upper left"
):
    """
    Create single-axis chart matching LHM standards.
    """
    if colors is None:
        colors = [OCEAN_BLUE, SUNSET_ORANGE, CAROLINA_BLUE, MAGENTA, LIGHT_GRAY]

    fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
    ax = fig.add_axes(AX_RECT)

    # Ensure all spines visible
    for spine in ['top', 'bottom', 'left', 'right']:
        ax.spines[spine].set_visible(True)
        ax.spines[spine].set_color(MID_GRAY)
        ax.spines[spine].set_linewidth(0.8)

    # Plot series
    lines = []
    labels = []
    for i, col in enumerate(cols):
        if col not in df.columns:
            continue
        c = colors[i % len(colors)]
        line = ax.plot(df.index, df[col], color=c, linewidth=2.0, label=col, zorder=5)[0]
        lines.append(line)
        labels.append(col)
        # Add last value label
        last_val = last_valid_value(df[col])
        if last_val is not None:
            lastvalue_label(ax, last_val, c, fmt=fmt)

    # Labels and title
    ax.set_ylabel(ylabel, fontsize=11, weight='bold', color=BLACK)
    ax.set_title(title, fontsize=13, weight='bold', pad=15, color=BLACK)
    ax.tick_params(labelsize=9)

    # Log scale
    if log_scale:
        ax.set_yscale('log')

    # Recession shading
    if show_recessions:
        shade_recessions(ax, alpha=0.12, zorder=1)

    # Auto-adjust x-axis
    auto_left_xlim(ax)

    # Legend
    if lines:
        ax.legend(lines, labels, loc=legend_loc, frameon=True,
                 facecolor='white', edgecolor='none', fontsize=9)

    # Watermark
    watermark(ax)

    # Date formatting
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator(5))

    # Save
    if filename:
        path = os.path.join(OUTDIR, filename)
        plt.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"💾 Saved: {path}")

    plt.tight_layout()
    return fig, ax

__all__ = [
    'chart', 'chart_dual', 'fred_fetch', 'yoy', 'last_valid_value',
    'shade_recessions', 'watermark', 'OCEAN_BLUE', 'SUNSET_ORANGE',
    'CAROLINA_BLUE', 'MAGENTA', 'LIGHT_GRAY', 'MID_GRAY', 'BLACK'
]