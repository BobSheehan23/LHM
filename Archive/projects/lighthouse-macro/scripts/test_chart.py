#!/usr/bin/env python3
"""
Test script to verify LHM chart standards are correct.
Generates a sample chart and prints what should be visible.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from charting import LHMChart, set_lhm_style, COLORS

print("="*60)
print("LIGHTHOUSE MACRO — Chart Standards Test")
print("="*60)

# Create sample data
dates = pd.date_range('2020-01-01', periods=100, freq='M')
values = 100 + np.cumsum(np.random.randn(100) * 2)
data = pd.Series(values, index=dates, name="Test Series")

print("\n1. Creating chart with LHM standards...")
print(f"   - Size: 12x7 inches")
print(f"   - DPI: 300")
print(f"   - Outer frame: {COLORS['ocean_blue']} (Ocean Blue), 8px thick")
print(f"   - Data spines: #666666 (Dark Gray), 1px")
print(f"   - Data area: ~85% of canvas (left=8%, right=92%, top=92%, bottom=8%)")

# Create chart
set_lhm_style()
chart = LHMChart()

print("\n2. Plotting data...")
chart.plot_line(data, label="Sample Data", color="ocean_blue")

print("\n3. Adding elements...")
chart.set_title("Test Chart - LHM Standards")
chart.set_labels(ylabel="Value")
chart.add_legend()

print("\n4. Adding watermarks...")
print(f"   - Top-left: 'LIGHTHOUSE MACRO' ({COLORS['ocean_blue']}, 60% opacity)")
print(f"   - Bottom-right: 'MACRO, ILLUMINATED.' ({COLORS['ocean_blue']}, 60% opacity)")
chart.add_watermarks()

print("\n5. Saving chart...")
output_path = Path(__file__).parent.parent / "test_chart.png"
chart.save(str(output_path))

print(f"\n✓ Chart saved to: {output_path}")
print("\n" + "="*60)
print("WHAT YOU SHOULD SEE:")
print("="*60)
print("1. 🔵 THICK OCEAN BLUE FRAME around the entire chart edge")
print("2. ⬛ Thin gray lines (spines) around the data area")
print("3. 🟦 Ocean blue 'LIGHTHOUSE MACRO' text (top-left)")
print("4. 🟦 Ocean blue 'MACRO, ILLUMINATED.' text (bottom-right)")
print("5. 📊 Data area centered with ~15% margins on all sides")
print("6. ➡️  Y-axis labels on the RIGHT side")
print("7. ⬜ No gridlines visible")
print("="*60)

print(f"\nOpen the file to verify:")
print(f"open {output_path}")
print()
