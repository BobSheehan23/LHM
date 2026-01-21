"""
Lighthouse Macro — Charting Standards
Enforce LHM visual identity across all charts
"""

from typing import Any, Dict, Optional, Sequence, Tuple, Union

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from core import get_config


# LHM Color Palette - Cotton candy sky, dusk, ocean cloudless day, sea green
COLORS = {
    "ocean_blue": "#0089d1",        # Ocean on cloudless day
    "dusk_orange": "#E8530E",       # Dusk orange
    "carolina_blue": "#00D4FF",     # Cotton candy sky (vibrant cyan)
    "neon_magenta": "#FF0090",      # Cotton candy sky (hot magenta)
    "sea_green": "#00CBA9",         # Sea green / turquoise
    "light_gray": "#D3D3D3",
    "signal_green": "#00FF7F",
    "signal_red": "#FF3333",
}


class LHMChart:
    """
    Lighthouse Macro chart builder with enforced standards.
    """

    def __init__(
        self,
        figsize: Tuple[float, float] = (12, 7),
        dpi: int = 300,
    ):
        """
        Initialize LHM chart with ocean blue outer frame.

        Args:
            figsize: Figure size (width, height) in inches (default 12x7)
            dpi: Resolution for export (default 300)
        """
        self.config = get_config()
        self.charting_config = self.config.charting_config

        # Create figure and axis with tight data area (~85% of canvas)
        self.fig, self.ax = plt.subplots(
            figsize=figsize,
            dpi=dpi,
            facecolor='white',
            edgecolor=COLORS["ocean_blue"],
            linewidth=8
        )

        # Position data area to be ~85% of canvas (leaves room for frame + watermarks)
        self.fig.subplots_adjust(
            left=0.08,
            right=0.92,
            top=0.92,
            bottom=0.08
        )

        # Apply LHM standards
        self._apply_standards()

    def _apply_standards(self) -> None:
        """Apply Lighthouse Macro charting standards"""

        # Remove grid
        self.ax.grid(False)

        # All four spines visible (black/gray for data area)
        for spine in self.ax.spines.values():
            spine.set_visible(True)
            spine.set_color("#666666")  # Dark gray
            spine.set_linewidth(1.0)

        # Primary axis on right
        self.ax.yaxis.tick_right()
        self.ax.yaxis.set_label_position("right")

        # Set background colors
        self.fig.patch.set_facecolor("white")
        self.ax.set_facecolor("white")

        # Add margins to prevent data clipping
        self.ax.margins(y=0.1)  # 10% buffer above/below data

        # OUTER blue frame is set in __init__ via fig.patch.set_edgecolor
        # Data spines (already set above) are gray for the data area

        # Track secondary axis
        self.ax2 = None

    def _get_or_create_secondary_axis(self):
        """Get or create secondary (left) y-axis"""
        if self.ax2 is None:
            # Create twin axis
            self.ax2 = self.ax.twinx()

            # Configure secondary axis on LEFT
            self.ax2.yaxis.set_ticks_position('left')
            self.ax2.yaxis.set_label_position('left')

            # Move the spine to the left
            self.ax2.spines['right'].set_visible(False)
            self.ax2.spines['left'].set_position(('outward', 0))
            self.ax2.spines['left'].set_visible(True)
            self.ax2.spines['left'].set_color("#666666")
            self.ax2.spines['left'].set_linewidth(1.0)
            self.ax2.spines['top'].set_visible(False)
            self.ax2.spines['bottom'].set_visible(False)

            # Add margins to prevent data clipping
            self.ax2.margins(y=0.1)  # 10% buffer above/below data

            self.ax2.grid(False)

            # Keep primary axis on right
            self.ax.yaxis.set_ticks_position('right')
            self.ax.yaxis.set_label_position('right')

        return self.ax2

    def _add_last_value_label(self, data, color, ax):
        """Add last value label on the axis with opaque background"""
        import pandas as pd

        # Get last valid value
        if isinstance(data, pd.Series):
            clean = data.dropna()
            if clean.empty:
                return
            last_value = clean.iloc[-1]
        else:
            try:
                # best effort for array-like data
                clean = [value for value in data if value is not None]
            except TypeError:
                clean = []
            if not clean:
                return
            last_value = clean[-1]

        # Format the value
        if abs(last_value) >= 1000:
            label_text = f"{last_value:,.0f}"
        elif abs(last_value) >= 10:
            label_text = f"{last_value:.1f}"
        else:
            label_text = f"{last_value:.2f}"

        # Add text on the axis with opaque background matching line color
        ax.text(
            1.01 if ax == self.ax else -0.01,  # Position outside axis
            last_value,
            f" {label_text} ",
            transform=ax.get_yaxis_transform(),
            fontsize=9,
            fontweight='bold',
            color='white',
            bbox=dict(
                boxstyle='round,pad=0.3',
                facecolor=color,
                edgecolor='none',
                alpha=1.0
            ),
            ha='left' if ax == self.ax else 'right',
            va='center',
            zorder=100
        )

    def align_axes_at_zero(self):
        """Align primary and secondary axes at zero while allowing independent scaling"""
        if self.ax2 is None:
            return

        # Get current limits
        y1_min, y1_max = self.ax.get_ylim()
        y2_min, y2_max = self.ax2.get_ylim()

        # Only align if both axes cross zero
        if not ((y1_min < 0 < y1_max) and (y2_min < 0 < y2_max)):
            return

        # Calculate where zero should be as a fraction of the axis (0 = bottom, 1 = top)
        # We want zero at the same vertical position on both axes
        zero_position1 = abs(y1_min) / (y1_max - y1_min)

        # Apply same zero position to secondary axis
        range2 = y2_max - y2_min
        new_y2_min = -zero_position1 * range2
        new_y2_max = (1 - zero_position1) * range2

        self.ax2.set_ylim(new_y2_min, new_y2_max)

    def plot_line(
        self,
        data,
        label: Optional[str] = None,
        color: Optional[str] = None,
        linewidth: float = 2.5,
        add_last_value_label: bool = True,
        axis: str = "primary",
        **kwargs,
    ):
        """
        Plot line with LHM standards.

        Args:
            data: Series or DataFrame to plot
            label: Legend label
            color: Color (hex or LHM color name)
            linewidth: Line width
            add_last_value_label: Add last value label on axis (default True)
            axis: Which axis to use - "primary" or "secondary"
            **kwargs: Additional matplotlib arguments
        """
        # Resolve color
        if color is None:
            color = COLORS["ocean_blue"]
        elif color in COLORS:
            color = COLORS[color]

        # Select axis
        ax = self.ax if axis == "primary" else self._get_or_create_secondary_axis()

        # Plot the line
        line = ax.plot(data, label=label, color=color, linewidth=linewidth, **kwargs)[0]

        # Add last value label if requested
        if add_last_value_label:
            self._add_last_value_label(data, color, ax)

        return line

    def plot_area(
        self,
        data,
        label: Optional[str] = None,
        color: Optional[str] = None,
        alpha: float = 0.3,
        **kwargs,
    ):
        """Plot filled area"""
        if color is None:
            color = COLORS["ocean_blue"]
        elif color in COLORS:
            color = COLORS[color]

        self.ax.fill_between(
            data.index, data.values, label=label, color=color, alpha=alpha, **kwargs
        )

    def add_hline(
        self, y: float, color: str = "black", linestyle: str = "--", linewidth: float = 1.0, **kwargs
    ):
        """Add horizontal reference line"""
        self.ax.axhline(y=y, color=color, linestyle=linestyle, linewidth=linewidth, **kwargs)

    def add_vline(
        self, x, color: str = "black", linestyle: str = "--", linewidth: float = 1.0, **kwargs
    ):
        """Add vertical reference line"""
        self.ax.axvline(x=x, color=color, linestyle=linestyle, linewidth=linewidth, **kwargs)

    def add_recession_bars(self, recession_dates: list):
        """
        Add NBER recession shading.

        Args:
            recession_dates: List of (start, end) date tuples
        """
        for start, end in recession_dates:
            self.ax.axvspan(start, end, color=COLORS["light_gray"], alpha=0.3, zorder=0)

    def set_title(self, title: str, fontsize: int = 16, **kwargs):
        """Set chart title (centered)"""
        self.ax.set_title(title, fontsize=fontsize, fontweight="bold", loc="center", **kwargs)

    def set_labels(
        self, xlabel: Optional[str] = None, ylabel: Optional[str] = None, fontsize: int = 12
    ):
        """Set axis labels"""
        if xlabel:
            self.ax.set_xlabel(xlabel, fontsize=fontsize)
        if ylabel:
            self.ax.set_ylabel(ylabel, fontsize=fontsize)

    def add_legend(self, loc: str = "upper left", fontsize: int = 10, **kwargs):
        """Add legend combining both axes if dual axis is used, with white opaque background"""
        if self.ax2 is not None:
            # Get handles and labels from both axes
            handles1, labels1 = self.ax.get_legend_handles_labels()
            handles2, labels2 = self.ax2.get_legend_handles_labels()
            # Combine them
            legend = self.ax.legend(
                handles1 + handles2, labels1 + labels2,
                loc=loc, fontsize=fontsize, frameon=True,
                facecolor='white', edgecolor='#666666',
                framealpha=1.0, **kwargs
            )
        else:
            # Single axis - normal legend
            legend = self.ax.legend(
                loc=loc, fontsize=fontsize, frameon=True,
                facecolor='white', edgecolor='#666666',
                framealpha=1.0, **kwargs
            )

    def add_watermarks(self, source: Optional[str] = None):
        """
        Add LHM watermarks and optional source citation.

        Args:
            source: Data source name (e.g., "FRED", "Bloomberg", "FactSet")
        """
        # Top-left: LIGHTHOUSE MACRO (Ocean Blue)
        self.fig.text(
            0.02,
            0.98,
            "LIGHTHOUSE MACRO",
            ha="left",
            va="top",
            fontsize=14,
            alpha=0.6,
            fontweight="bold",
            color=COLORS["ocean_blue"],
        )

        # Bottom-right: MACRO, ILLUMINATED. (Ocean Blue)
        self.fig.text(
            0.98,
            0.02,
            "MACRO, ILLUMINATED.",
            ha="right",
            va="bottom",
            fontsize=14,
            alpha=0.6,
            fontweight="bold",
            color=COLORS["ocean_blue"],
        )

        # Bottom-left: Source citation (if provided)
        if source:
            self.fig.text(
                0.02,
                0.02,
                f"Source: {source}  |  Analysis: Lighthouse Macro",
                ha="left",
                va="bottom",
                fontsize=8,
                color="#666666",
                style="italic",
            )

    def tight_layout(self):
        """
        Adjust layout (already optimized in __init__ with subplots_adjust).
        This is a no-op since we manually control positioning for the blue frame.
        """
        # Layout already set in __init__ to accommodate blue frame + watermarks
        pass

    def save(self, filepath: str, dpi: Optional[int] = None, **kwargs):
        """
        Save chart to file.

        Args:
            filepath: Output file path
            dpi: Resolution (uses chart dpi if not specified)
            **kwargs: Additional savefig arguments
        """
        if dpi is None:
            dpi = self.fig.dpi

        self.fig.savefig(filepath, dpi=dpi, bbox_inches="tight", **kwargs)

    def show(self):
        """Display chart"""
        plt.show()

    def close(self):
        """Close figure"""
        plt.close(self.fig)


def plot_dual(
    data,
    labels: Optional[Sequence[str]] = None,
    ylabels: Optional[Sequence[str]] = None,
    title: Optional[str] = None,
    fname: Optional[Union[str, Path]] = None,
    colors: Optional[Sequence[str]] = None,
    source: Optional[str] = None,
    align_zero: bool = True,
    zero_line: bool = True,
    legend_loc: str = "upper left",
    figsize: Tuple[float, float] = (12, 7),
    dpi: int = 300,
) -> LHMChart:
    """
    Convenience wrapper for producing a dual-axis Lighthouse Macro chart.

    Args:
        data: DataFrame or 2-column structure containing the series to plot.
        labels: Legend labels for the primary and secondary series.
        ylabels: Axis labels for the primary (right) and secondary (left) axes.
        title: Chart title.
        fname: Optional output path to save the figure.
        colors: Optional iterable of two color names/hex values.
        source: Optional source string for watermarking.
        align_zero: Align zero across axes when both cross zero (default True).
        zero_line: Draw dashed zero reference line on the primary axis.
        legend_loc: Location for the combined legend.
        figsize: Figure size passed to `LHMChart`.
        dpi: Resolution passed to `LHMChart`.
    """
    if data is None:
        raise ValueError("plot_dual requires data to plot")
    if not hasattr(data, "iloc"):
        raise TypeError("plot_dual expects a pandas DataFrame or similar structure with .iloc")
    if not hasattr(data, "shape") or data.shape[1] < 2:
        raise ValueError("plot_dual requires at least two columns")

    # Ensure index-aligned series
    primary = data.iloc[:, 0]
    secondary = data.iloc[:, 1]

    # Default labels
    resolved_labels = list(labels) if labels else [str(primary.name or "Series 1"), str(secondary.name or "Series 2")]
    if len(resolved_labels) < 2:
        resolved_labels = (resolved_labels + ["Series 2"])[:2]

    resolved_colors = list(colors) if colors else ["ocean_blue", "dusk_orange"]
    if len(resolved_colors) < 2:
        resolved_colors = (resolved_colors + ["dusk_orange"])[:2]

    chart = LHMChart(figsize=figsize, dpi=dpi)
    chart.plot_line(primary, label=resolved_labels[0], color=resolved_colors[0], axis="primary")
    chart.plot_line(secondary, label=resolved_labels[1], color=resolved_colors[1], axis="secondary")

    if align_zero:
        chart.align_axes_at_zero()

    if zero_line:
        chart.add_hline(0, color="#666666", linestyle="--", linewidth=1)

    if title:
        chart.set_title(title)

    if ylabels:
        if ylabels and len(ylabels) > 0:
            chart.set_labels(ylabel=ylabels[0])
        if len(ylabels) > 1 and chart.ax2 is not None:
            chart.ax2.set_ylabel(ylabels[1], fontsize=12)

    chart.add_legend(loc=legend_loc)
    chart.add_watermarks(source=source)

    if fname:
        output_path = Path(fname)
        chart.save(str(output_path))

    return chart


def set_lhm_style():
    """
    Set global matplotlib style for LHM charts.
    Call once at the beginning of a session.
    """
    mpl.rcParams.update(
        {
            # Figure
            "figure.facecolor": "white",
            "figure.dpi": 100,
            # Axes
            "axes.facecolor": "white",
            "axes.edgecolor": "black",
            "axes.linewidth": 0.8,
            "axes.grid": False,
            "axes.labelsize": 12,
            "axes.titlesize": 16,
            "axes.titleweight": "bold",
            # Lines
            "lines.linewidth": 2.5,
            "lines.antialiased": True,
            # Ticks
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "xtick.direction": "out",
            "ytick.direction": "out",
            # Legend
            "legend.frameon": False,
            "legend.fontsize": 10,
            # Font
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            # Grid (disabled by default)
            "grid.alpha": 0,
        }
    )
