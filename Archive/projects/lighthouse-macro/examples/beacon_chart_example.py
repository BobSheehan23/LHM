#!/usr/bin/env python3
"""
Example: Creating The Beacon Chart 1 — Headline vs Flow Employment

THESIS: Employment headline strength masks underlying labor market fragility.

CHART EXPLANATION:
- Payrolls (headline) show continued growth (YoY %, z-scored)
- Quits rate (flow) shows workers are risk-averse, not switching jobs (z-scored)
- Divergence = apparent strength concealing behavioral weakness
- Late-cycle signal: workers stick to jobs out of fear, not confidence

DATA REQUIREMENTS:
1. PAYEMS (Total Nonfarm Payrolls) - monthly, BLS via FRED
2. JTSQUR (Quits Rate) - monthly, BLS JOLTS via FRED

TRANSFORMATION LOGIC:
1. Payrolls: YoY% change → z-score (10-year rolling window)
2. Quits: Raw rate → z-score (3-year rolling window, captures post-pandemic normalization)
3. Align: Inner join (show full overlap period where BOTH series exist)

INTERPRETATION:
- When lines move together: labor market is coherent
- When payrolls high but quits low: "resilience illusion" - workers trapped, not thriving
- Current state: Payrolls elevated, quits declining = hidden transition underway
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from collectors.universal import DataPipeline
from charting import LHMChart, set_lhm_style

# Initialize
set_lhm_style()
pipeline = DataPipeline()

print("="*80)
print("BEACON CHART EXAMPLE: Headline vs Flow Employment")
print("="*80)

# Add series
print("\n1. Adding data series...")
print("   - PAYEMS (Total Nonfarm Payrolls) from FRED")
print("   - JTSQUR (Quits Rate) from FRED")

pipeline.add_series(
    name="payrolls",
    source="FRED",
    series_id="PAYEMS",
    start_date="2000-01-01"  # Get maximum history
)

pipeline.add_series(
    name="quits",
    source="FRED",
    series_id="JTSQUR",
    start_date="2000-01-01"  # JOLTS starts Dec 2000
)

# Transform
print("\n2. Applying transformations...")
print("   - Payrolls: YoY% → z-score (10y rolling)")
print("   - Quits: z-score (3y rolling)")

pipeline.transform("payrolls", "yoy_pct", periods=12)
pipeline.transform("payrolls", "zscore_rolling", window=120)  # 10 years
pipeline.transform("quits", "zscore_rolling", window=36)  # 3 years

# Align
print("\n3. Aligning series (inner join)...")
pipeline.align(method="inner")  # Only show where BOTH exist

# Get data
data = pipeline.get_chart_data()
print(f"\n4. Aligned data:")
print(f"   Start: {data.index.min().strftime('%Y-%m')}")
print(f"   End: {data.index.max().strftime('%Y-%m')}")
print(f"   Observations: {len(data)}")
print(f"   Coverage: {((data.index.max() - data.index.min()).days / 365.25):.1f} years")

# Create chart
print("\n5. Creating chart...")
chart = LHMChart()
chart.plot_line(data["payrolls"], label="Payrolls YoY (z)", color="ocean_blue")
chart.plot_line(data["quits"], label="Quits Rate (z)", color="dusk_orange")
chart.add_hline(0, color="#666666", linestyle="--", linewidth=1)
chart.set_title("Headline vs Flow: Payrolls vs Quits")
chart.set_labels(ylabel="Standard deviations from mean")
chart.add_legend()
chart.add_watermarks(source="BLS (JOLTS, CES) via FRED")

output_path = Path(__file__).parent.parent / "example_headline_vs_flow.png"
chart.save(str(output_path))

print(f"\n✓ Chart saved: {output_path}")
print("\n" + "="*80)
print("INTERPRETATION:")
print("="*80)
print("""
When you open this chart, you should see:

1. TIME PERIOD: Dec 2000 - Present (when JOLTS data begins)
   - Both series show FULL history where they overlap
   - NOT truncated to shorter series

2. CURRENT PATTERN (2023-2025):
   - Payrolls YoY (blue): Still elevated, showing job growth
   - Quits Rate (orange): Declining toward/below zero
   - DIVERGENCE = The Hidden Transition

3. WHAT THIS MEANS:
   - Strong payrolls = headline looks good
   - Weak quits = workers are scared, not confident
   - Historical pattern: This divergence precedes slowdowns
   - Late-cycle signature: People cling to jobs they have

4. TRADING IMPLICATION:
   - Market prices in payroll strength (good!)
   - Market ignores quit weakness (fragility!)
   - Asymmetric risk: transition already underway, not priced
""")
print("="*80)
