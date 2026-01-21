#!/usr/bin/env python3
"""
Generate key charts for The Beacon | October 2025: The Hidden Transition
Using available FRED data
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from charting import LHMChart, set_lhm_style, COLORS
from collectors import FREDCollector
from transformers import yoy_pct, zscore, zscore_rolling, index_to_base

print("="*80)
print("THE BEACON | October 2025")
print("The Hidden Transition — Chart Generation")
print("="*80)

# Initialize
set_lhm_style()
collector = FREDCollector()
output_dir = Path("/Users/bob/Desktop/beacon_charts")
output_dir.mkdir(exist_ok=True)

print(f"\nOutput directory: {output_dir}")
print(f"Generating charts with available FRED data...\n")

# ==============================================================================
# CHART 1: Headline vs Flow Employment - Payrolls vs Quits
# ==============================================================================
print("1. Headline vs Flow: Payrolls vs Quits...")
try:
    # Fetch/load data
    payrolls_df = collector.load_latest("PAYEMS")
    quits_df = collector.load_latest("JTSQUR")

    if payrolls_df is None:
        print("   Collecting PAYEMS...")
        payrolls_df = collector.fetch("PAYEMS", start_date="2010-01-01")
    if quits_df is None:
        print("   Collecting JTSQUR...")
        quits_df = collector.fetch("JTSQUR", start_date="2010-01-01")

    # Transform
    payrolls_yoy = yoy_pct(payrolls_df["PAYEMS"], periods=12)
    payrolls_z = zscore_rolling(payrolls_yoy, window=120)  # 10 years
    quits_z = zscore_rolling(quits_df["JTSQUR"], window=36)  # 3 years

    # Chart
    chart = LHMChart()
    chart.plot_line(payrolls_z, label="Payrolls YoY (z)", color="ocean_blue")
    chart.plot_line(quits_z, label="Quits Rate (z)", color="dusk_orange")
    chart.add_hline(0, color="#666666", linestyle="--", linewidth=1)
    chart.set_title("Headline vs Flow: Payrolls vs Quits")
    chart.set_labels(ylabel="Standard deviations from mean")
    chart.add_legend()
    chart.add_watermarks(source="BLS (JOLTS, CES) via FRED")
    chart.save(str(output_dir / "01_headline_vs_flow_employment.png"))
    print("   ✓ Saved")
except Exception as e:
    print(f"   ✗ Error: {e}")

# ==============================================================================
# CHART 2: Labor Hours vs Employment
# ==============================================================================
print("2. Under the Hood: Hours vs Headcount...")
try:
    hours_df = collector.load_latest("AWHAETP")  # All employees, total private
    payrolls_df = collector.load_latest("PAYEMS")

    if hours_df is None:
        print("   Collecting AWHAETP...")
        hours_df = collector.fetch("AWHAETP", start_date="2019-01-01")
    if payrolls_df is None:
        print("   Collecting PAYEMS...")
        payrolls_df = collector.fetch("PAYEMS", start_date="2019-01-01")

    # Index to 2019-12
    base_date = "2019-12-01"
    hours_idx = index_to_base(hours_df["AWHAETP"], base_date)
    payrolls_idx = index_to_base(payrolls_df["PAYEMS"], base_date)

    chart = LHMChart()
    chart.plot_line(hours_idx, label="Avg Weekly Hours (2019=100)", color="dusk_orange")
    chart.plot_line(payrolls_idx, label="Total Nonfarm Payrolls (2019=100)", color="ocean_blue")
    chart.set_title("Under the Hood: Hours vs Headcount")
    chart.set_labels(ylabel="Index (2019=100)")
    chart.add_legend()
    chart.add_watermarks(source="BLS CES via FRED")
    chart.save(str(output_dir / "02_labor_hours_vs_employment.png"))
    print("   ✓ Saved")
except Exception as e:
    print(f"   ✗ Error: {e}")

# ==============================================================================
# CHART 3: Labor Fragility Composite
# ==============================================================================
print("3. Labor Fragility Dashboard...")
try:
    quits_df = collector.load_latest("JTSQUR")
    lt_unemp_df = collector.load_latest("UEMP27OV")
    hours_df = collector.load_latest("AWHAETP")

    if quits_df is None:
        quits_df = collector.fetch("JTSQUR", start_date="2010-01-01")
    if lt_unemp_df is None:
        lt_unemp_df = collector.fetch("UEMP27OV", start_date="2010-01-01")
    if hours_df is None:
        hours_df = collector.fetch("AWHAETP", start_date="2010-01-01")

    # Create composite with z-scores
    quits_z = zscore(quits_df["JTSQUR"])
    lt_unemp_z = -zscore(lt_unemp_df["UEMP27OV"])  # Invert (higher is worse)
    hours_z = zscore(hours_df["AWHAETP"])

    # Align and weight
    composite = pd.DataFrame({
        'quits': quits_z,
        'lt_unemp': lt_unemp_z,
        'hours': hours_z
    }).dropna()

    composite_series = 0.4 * composite['quits'] + 0.3 * composite['lt_unemp'] + 0.3 * composite['hours']

    chart = LHMChart()
    chart.plot_line(composite_series, label="Labor Fragility (z)", color="dusk_orange")
    chart.add_hline(0, color="#666666", linestyle="--", linewidth=1)
    chart.add_hline(1, color="#FF4500", linestyle=":", linewidth=1, alpha=0.5)
    chart.set_title("Labor Fragility Dashboard")
    chart.set_labels(ylabel="Composite z-score")
    chart.add_legend()
    chart.add_watermarks(source="BLS via FRED")
    chart.save(str(output_dir / "03_labor_fragility_dashboard.png"))
    print("   ✓ Saved")
except Exception as e:
    print(f"   ✗ Error: {e}")

# ==============================================================================
# CHART 4: Labor Dynamism - Quits/Layoffs Ratio
# ==============================================================================
print("4. Labor Dynamism Index...")
try:
    quits_df = collector.load_latest("JTSQUR")
    layoffs_df = collector.load_latest("JTSLDR")

    if quits_df is None:
        quits_df = collector.fetch("JTSQUR", start_date="2010-01-01")
    if layoffs_df is None:
        layoffs_df = collector.fetch("JTSLDR", start_date="2010-01-01")

    # Ratio and z-score
    dynamism = quits_df["JTSQUR"] / layoffs_df["JTSLDR"]
    dynamism_z = zscore_rolling(dynamism, window=180)  # 15 years

    chart = LHMChart()
    chart.plot_line(dynamism_z, label="Labor Dynamism Index (z)", color="ocean_blue")
    chart.add_hline(0, color="#666666", linestyle="--", linewidth=1)
    chart.set_title("Labor Dynamism Index")
    chart.set_labels(ylabel="z-score")
    chart.add_legend()
    chart.add_watermarks(source="BLS JOLTS via FRED")
    chart.save(str(output_dir / "04_labor_dynamism_index.png"))
    print("   ✓ Saved")
except Exception as e:
    print(f"   ✗ Error: {e}")

# ==============================================================================
# CHART 5: HY Spread vs Default Risk (using unemployment as proxy)
# ==============================================================================
print("5. HY Spread vs Default Probability...")
try:
    hy_oas_df = collector.load_latest("BAMLH0A0HYM2")
    unemp_df = collector.load_latest("UNRATE")

    if hy_oas_df is None:
        hy_oas_df = collector.fetch("BAMLH0A0HYM2", start_date="2010-01-01")
    if unemp_df is None:
        unemp_df = collector.fetch("UNRATE", start_date="2010-01-01")

    chart = LHMChart()
    chart.plot_line(hy_oas_df["BAMLH0A0HYM2"], label="HY OAS", color="ocean_blue", axis="primary")
    chart.plot_line(unemp_df["UNRATE"], label="Unemployment Rate", color="dusk_orange", axis="secondary")
    chart.align_axes_at_zero()
    chart.set_title("HY Spread vs Default Probability")
    chart.set_labels(ylabel="HY OAS (bps)")
    if chart.ax2:
        chart.ax2.set_ylabel("Unemployment Rate (%)")
    chart.add_legend()
    chart.add_watermarks(source="ICE/BofA, BLS via FRED")
    chart.save(str(output_dir / "05_hy_spread_vs_default_prob.png"))
    print("   ✓ Saved")
except Exception as e:
    print(f"   ✗ Error: {e}")

# ==============================================================================
# CHART 6: Credit Spread Volatility
# ==============================================================================
print("6. Credit Spread Convexity...")
try:
    hy_oas_df = collector.load_latest("BAMLH0A0HYM2")

    if hy_oas_df is None:
        hy_oas_df = collector.fetch("BAMLH0A0HYM2", start_date="2010-01-01")

    # 20-day rolling volatility
    hy_vol = hy_oas_df["BAMLH0A0HYM2"].rolling(20).std()
    hy_vol_z = zscore(hy_vol)

    chart = LHMChart()
    chart.plot_line(hy_vol_z, label="Spread Convexity (z)", color="neon_magenta")
    chart.add_hline(0, color="#666666", linestyle="--", linewidth=1)
    chart.add_hline(1, color="#FF4500", linestyle=":", linewidth=1, alpha=0.5)
    chart.set_title("When Passive Flows Bite")
    chart.set_labels(ylabel="z-score")
    chart.add_legend()
    chart.add_watermarks(source="ICE/BofA via FRED")
    chart.save(str(output_dir / "06_credit_spread_convexity_index.png"))
    print("   ✓ Saved")
except Exception as e:
    print(f"   ✗ Error: {e}")

# ==============================================================================
# CHART 7: RRP and Reserves Trend
# ==============================================================================
print("7. The Fading Cushion: RRP & Reserves...")
try:
    rrp_df = collector.load_latest("RRPONTSYD")
    reserves_df = collector.load_latest("RESBALNS")
    gdp_df = collector.load_latest("GDP")

    if rrp_df is None:
        rrp_df = collector.fetch("RRPONTSYD", start_date="2020-01-01")
    if reserves_df is None:
        reserves_df = collector.fetch("RESBALNS", start_date="2020-01-01")
    if gdp_df is None:
        gdp_df = collector.fetch("GDP", start_date="2020-01-01")

    # Resample to monthly and calculate % of GDP
    gdp_monthly = gdp_df["GDP"].resample('ME').ffill()
    rrp_pct = (rrp_df["RRPONTSYD"] / gdp_monthly) * 100
    reserves_pct = (reserves_df["RESBALNS"] / gdp_monthly) * 100

    chart = LHMChart()
    chart.plot_line(reserves_pct, label="Reserves to GDP", color="ocean_blue", axis="primary")
    chart.plot_line(rrp_pct, label="ON RRP to GDP", color="dusk_orange", axis="secondary")
    chart.align_axes_at_zero()
    chart.set_title("The Fading Cushion")
    chart.set_labels(ylabel="Reserves, % of GDP")
    if chart.ax2:
        chart.ax2.set_ylabel("ON RRP, % of GDP")
    chart.add_legend()
    chart.add_watermarks(source="Federal Reserve H.4.1, BEA")
    chart.save(str(output_dir / "07_rrp_and_reserves_trend.png"))
    print("   ✓ Saved")
except Exception as e:
    print(f"   ✗ Error: {e}")

# ==============================================================================
# CHART 8: Funding Stress (TED Spread)
# ==============================================================================
print("8. Funding Stress Thermometer...")
try:
    ted_df = collector.load_latest("TEDRATE")

    if ted_df is None:
        ted_df = collector.fetch("TEDRATE", start_date="2010-01-01")

    # Convert to percentile
    ted_percentile = ted_df["TEDRATE"].rank(pct=True) * 100

    chart = LHMChart()
    chart.plot_line(ted_percentile, label="Funding Stress Thermometer", color="dusk_orange")
    chart.add_hline(50, color="#666666", linestyle="--", linewidth=1)
    chart.add_hline(80, color="#FF4500", linestyle=":", linewidth=1, alpha=0.5)
    chart.set_title("Funding Stress Thermometer")
    chart.set_labels(ylabel="Percentile (0–100)")
    chart.add_legend()
    chart.add_watermarks(source="Fed via FRED")
    chart.save(str(output_dir / "08_funding_stress_thermometer.png"))
    print("   ✓ Saved")
except Exception as e:
    print(f"   ✗ Error: {e}")

# ==============================================================================
# CHART 9: Transition Tracker Composite
# ==============================================================================
print("9. Transition Tracker Composite...")
try:
    quits_df = collector.load_latest("JTSQUR")
    hy_oas_df = collector.load_latest("BAMLH0A0HYM2")
    ted_df = collector.load_latest("TEDRATE")

    if quits_df is None:
        quits_df = collector.fetch("JTSQUR", start_date="2010-01-01")
    if hy_oas_df is None:
        hy_oas_df = collector.fetch("BAMLH0A0HYM2", start_date="2010-01-01")
    if ted_df is None:
        ted_df = collector.fetch("TEDRATE", start_date="2010-01-01")

    # Z-scores
    quits_z = zscore(quits_df["JTSQUR"])
    hy_z = zscore(hy_oas_df["BAMLH0A0HYM2"])
    ted_z = zscore(ted_df["TEDRATE"])

    # Composite
    composite_df = pd.DataFrame({
        'quits': quits_z,
        'hy': hy_z,
        'ted': ted_z
    }).dropna()

    composite_series = 0.4 * composite_df['quits'] + 0.35 * composite_df['hy'] + 0.25 * composite_df['ted']

    chart = LHMChart()
    chart.plot_line(composite_series, label="Transition Tracker (z)", color="ocean_blue")
    chart.add_hline(0, color="#666666", linestyle="--", linewidth=1)
    chart.add_hline(1, color="#FF4500", linestyle=":", linewidth=1, alpha=0.5)
    chart.set_title("Transition Tracker")
    chart.set_labels(ylabel="Composite z-score")
    chart.add_legend()
    chart.add_watermarks(source="Lighthouse Macro")
    chart.save(str(output_dir / "09_transition_tracker_composite.png"))
    print("   ✓ Saved")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "="*80)
print("✓ Chart generation complete!")
print(f"All charts saved to: {output_dir}")
print("="*80)
print("\nTo view charts:")
print(f"open {output_dir}")
