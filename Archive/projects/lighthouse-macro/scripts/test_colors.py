#!/usr/bin/env python3
"""
Test script for LHM color palette and last value labels.
Demonstrates all 4 primary colors with dual axis alignment.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from charting import LHMChart, set_lhm_style, COLORS

print("="*60)
print("LIGHTHOUSE MACRO — Color Palette & Label Test")
print("="*60)

# Create sample data
dates = pd.date_range('2020-01-01', periods=100, freq='ME')

# Create 5 series with different ranges
series1 = pd.Series(100 + np.cumsum(np.random.randn(100) * 2), index=dates, name="Ocean Blue Series")
series2 = pd.Series(50 + np.cumsum(np.random.randn(100) * 1.5), index=dates, name="Dusk Orange Series")
series3 = pd.Series(-10 + np.cumsum(np.random.randn(100) * 1), index=dates, name="Carolina Blue Series")
series4 = pd.Series(5 + np.cumsum(np.random.randn(100) * 0.5), index=dates, name="Neon Magenta Series")
series5 = pd.Series(75 + np.cumsum(np.random.randn(100) * 1.2), index=dates, name="Sea Green Series")

print("\n1. Creating chart with all 5 LHM colors...")
print(f"   - Ocean Blue: {COLORS['ocean_blue']} (Ocean cloudless day)")
print(f"   - Dusk Orange: {COLORS['dusk_orange']} (Dusk)")
print(f"   - Carolina Blue: {COLORS['carolina_blue']} (Cotton candy sky)")
print(f"   - Neon Magenta: {COLORS['neon_magenta']} (Cotton candy sky)")
print(f"   - Sea Green: {COLORS['sea_green']} (Sea green / turquoise)")

# Create chart
set_lhm_style()
chart = LHMChart()

print("\n2. Plotting 5 series with last value labels...")
chart.plot_line(series1, label="Ocean Blue", color="ocean_blue", axis="primary")
chart.plot_line(series2, label="Dusk Orange", color="dusk_orange", axis="primary")
chart.plot_line(series5, label="Sea Green", color="sea_green", axis="primary")
chart.plot_line(series3, label="Carolina Blue", color="carolina_blue", axis="secondary")
chart.plot_line(series4, label="Neon Magenta", color="neon_magenta", axis="secondary")

print("\n3. Aligning axes at zero...")
chart.align_axes_at_zero()

print("\n4. Adding chart elements...")
chart.set_title("LHM Color Palette Test — All 5 Primary Colors")
chart.set_labels(ylabel="Primary Axis (Right)")
if chart.ax2:
    chart.ax2.set_ylabel("Secondary Axis (Left)")
chart.add_legend()

print("\n5. Adding watermarks and source citation...")
chart.add_watermarks(source="Test Data")

print("\n6. Saving chart...")
output_path = Path(__file__).parent.parent / "test_colors.png"
chart.save(str(output_path))

print(f"\n✓ Chart saved to: {output_path}")
print("\n" + "="*60)
print("WHAT YOU SHOULD SEE:")
print("="*60)
print("1. 🔵 OCEAN BLUE frame around entire chart (thick border)")
print("2. ⬛ Gray spines around data area")
print("3. 🟦 Ocean blue watermarks (top-left, bottom-right)")
print("4. 📊 Five vibrant colored lines:")
print(f"   - Ocean Blue: {COLORS['ocean_blue']} (ocean cloudless day)")
print(f"   - Dusk Orange: {COLORS['dusk_orange']} (dusk)")
print(f"   - Sea Green: {COLORS['sea_green']} (sea green/turquoise)")
print(f"   - Carolina Blue: {COLORS['carolina_blue']} (cotton candy sky)")
print(f"   - Neon Magenta: {COLORS['neon_magenta']} (cotton candy sky)")
print("5. 🏷️  LAST VALUE LABELS on both axes:")
print("   - Ocean Blue, Dusk Orange & Sea Green labels on RIGHT axis")
print("   - Carolina Blue & Neon Magenta labels on LEFT axis")
print("   - Each label has OPAQUE background matching line color")
print("   - Each label has WHITE text")
print("6. 📏 BOTH AXES have visible ticks and scale")
print("7. 📖 LEGEND shows ALL 5 lines")
print("8. ⚖️  Axes aligned at zero (can scale independently)")
print("="*60)

print(f"\nOpen the file to verify:")
print(f"open {output_path}")
print()
