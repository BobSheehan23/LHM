# Lighthouse Macro — Chart Styling Specification

**Version:** 2.0 (TT Deck Standard)
**Last Updated:** January 31, 2026
**Purpose:** Canonical reference for all Lighthouse Macro chart generation. Update this file when standards change.

---

## TT Deck Format (Primary Standard)

All educational, research, and deck charts follow this format unless explicitly overridden.

### Figure-Level Branding

| Element | Position | Style |
|---|---|---|
| **LIGHTHOUSE MACRO** | Top-left | Ocean `#0089D1`, bold, fontsize 13 |
| **Date** | Top-right | Muted color, fontsize 11, `%B %d, %Y` format |
| **Top accent bar** | Below watermarks | Ocean 2/3, Dusk 1/3, height 0.004 |
| **Bottom accent bar** | Above footer | Mirror of top bar |
| **MACRO, ILLUMINATED.** | Bottom-right | Ocean `#0089D1`, bold italic, fontsize 13 |
| **Source line** | Bottom-left | Muted, italic, fontsize 9, format: `Lighthouse Macro | {Source}; mm.dd.yyyy` |

### Title & Subtitle

| Element | Style |
|---|---|
| **Title** | fontsize 15, bold, centered, `y=0.945` |
| **Subtitle** | fontsize 14, italic, Ocean `#0089D1`, centered, `y=0.895` |

### Subplot Margins (fig.subplots_adjust)

```python
# Symmetric for dual-axis charts:
fig.subplots_adjust(top=0.88, bottom=0.08, left=0.06, right=0.94)
# For single-axis charts, left can be tighter (0.04) if no LHS pill needed
```

### Accent Bar Implementation

```python
# Top accent bar
bar = fig.add_axes([0.03, 0.955, 0.94, 0.004])
bar.axhspan(0, 1, 0, 0.67, color='#0089D1')   # Ocean 2/3
bar.axhspan(0, 1, 0.67, 1.0, color='#FF6723')  # Dusk 1/3
bar.set_xlim(0, 1); bar.set_ylim(0, 1); bar.axis('off')

# Bottom accent bar (mirror)
bbar = fig.add_axes([0.03, 0.035, 0.94, 0.004])
bbar.axhspan(0, 1, 0, 0.67, color='#0089D1')
bbar.axhspan(0, 1, 0.67, 1.0, color='#FF6723')
bbar.set_xlim(0, 1); bbar.set_ylim(0, 1); bbar.axis('off')
```

---

## Axes & Spines

- **All 4 spines visible**, linewidth 0.5, colored to theme spine color
- **No gridlines** (`ax.grid(False)`)
- **No tick marks** on any axis (`length=0` on all `tick_params`)
- Tick labels remain (colored to series on dual-axis charts)
- **No rotated y-axis label text** — the pills and colored tick labels tell the story

### Dark Theme Spine Color
```python
'spine': '#1e3350'
```

### White Theme Spine Color
```python
'spine': '#cccccc'
```

---

## Last-Value Pills

Colored rounded pills with bold white text, positioned on the axis edge.

```python
pill = dict(boxstyle='round,pad=0.3', facecolor=series_color, edgecolor=series_color, alpha=0.95)
ax.annotate(label, xy=(1.0, last_y), xycoords=('axes fraction', 'data'),
            fontsize=9, fontweight='bold', color='white',
            ha='left', va='center',
            xytext=(6, 0), textcoords='offset points',
            bbox=pill)
```

### Dual-Axis Charts
- **RHS pill**: Primary axis series, placed at `x=1.0` (right spine), `ha='left'`
- **LHS pill**: Secondary axis series, placed at `x=0.0` (left spine), `ha='right'`

### Single-Axis Charts
- RHS pill only

---

## X-Axis Padding

```python
padding_left = pd.Timedelta(days=30)
padding_right = pd.Timedelta(days=180)  # ~6 months for yearly charts
```

This creates breathing room between the end of the data lines and the right spine where the pills sit.

---

## Data Handling

- **Always `dropna()` before plotting** to prevent line breaks at NaN gaps
- FRED data frequently has sporadic NaN values that create orphaned data points

```python
g_plot = data['yoy'].dropna()
ax.plot(g_plot.index, g_plot, ...)
```

---

## Zero Line

```python
ax.axhline(0, color=THEME['muted'], linewidth=0.8, alpha=0.5, linestyle='--')
```

Full-width dashed line. Extends to spines on both sides.

---

## Annotation Box (Takeaway)

Every chart should have an annotation box with 1-2 line commentary summarizing the takeaway. Positioned in dead space where there is no data.

```python
takeaway = "Your insight here.\nSecond line if needed."
ax.text(x, y, takeaway, transform=ax.transAxes,
        fontsize=10, color=THEME['fg'], ha='center', va='top',
        style='italic',
        bbox=dict(boxstyle='round,pad=0.5',
                  facecolor=THEME['bg'], edgecolor='#0089D1',
                  alpha=0.9))
```

- **Border color**: Always Ocean `#0089D1`
- **Background**: Theme background color (opaque)
- **Text**: Theme foreground, italic, fontsize 10
- **Position**: Find the largest empty area on the chart. Avoid overlapping data, recession shading, or legend.

---

## Recession Shading

```python
RECESSIONS = [
    ('2001-03-01', '2001-11-01'),
    ('2007-12-01', '2009-06-01'),
    ('2020-02-01', '2020-04-01'),
]
# Dark: white, alpha 0.06
# White: gray, alpha 0.12
ax.axvspan(start, end, color=color, alpha=alpha, zorder=0)
```

---

## Legend

```python
legend_style = dict(
    framealpha=0.95,
    facecolor=THEME['legend_bg'],
    edgecolor=THEME['spine'],
    labelcolor=THEME['legend_fg'],
)
ax.legend(loc='upper left', **legend_style)
```

---

## Color Assignments by Theme

### Dark Theme
| Role | Color | Hex |
|---|---|---|
| Primary series | Sky | `#4FC3F7` |
| Secondary series | Dusk | `#FF6723` |
| Tertiary series | Sea | `#00BB99` |
| Accent | Venus | `#FF2389` |
| Background | Dark Navy | `#0A1628` |
| Foreground text | Light | `#e6edf3` |
| Muted text | Gray | `#8b949e` |
| Legend bg | Dark Blue | `#0f1f38` |

### White Theme
| Role | Color | Hex |
|---|---|---|
| Primary series | Ocean | `#0089D1` |
| Secondary series | Dusk | `#FF6723` |
| Tertiary series | Sea | `#00BB99` |
| Accent | Venus | `#FF2389` |
| Background | White | `#ffffff` |
| Foreground text | Dark | `#1a1a1a` |
| Muted text | Gray | `#555555` |
| Legend bg | Light | `#f8f8f8` |

**Rationale**: Sky replaces Ocean on dark theme because Ocean has insufficient contrast against dark navy.

---

## Save Settings

```python
fig.savefig(path, dpi=200, bbox_inches='tight', pad_inches=0.15,
            facecolor=THEME['bg'], edgecolor='none')
```

- **DPI**: 200
- **No `tight_layout()`** — conflicts with accent bar axes
- Use `bbox_inches='tight'` with `pad_inches=0.15`

---

## Dual-Theme Generation

Every chart script must generate **both dark and white** versions. Default behavior is `--theme both`.

```
Output structure:
  /Outputs/.../dark/chart_XX_name.png
  /Outputs/.../white/chart_XX_name.png
```

---

## Reference Implementation

The canonical implementation of this spec lives in:
```
/Users/bob/LHM/Scripts/chart_generation/prices_edu_charts.py
```

For the TT research deck implementation:
```
/Users/bob/LHM/Scripts/chart_generation/tt_research_charts.py
```
