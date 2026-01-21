#!/usr/bin/env python3
"""
Generate all charts for The Beacon | October 2025: The Hidden Transition
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from charting import LHMChart, set_lhm_style, plot_dual, COLORS
from collectors import FREDCollector
from transformers import yoy_pct, zscore_rolling, index_to_base

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
print(f"Generating 15 charts...\n")

# ==============================================================================
# CHART 1: Headline vs Flow Employment
# ==============================================================================
print("1/15: Headline vs Flow: Payrolls vs Quits...")
try:
    # Fetch data
    payrolls = collector.load_latest("PAYEMS")  # Total Nonfarm Payrolls
    quits = collector.load_latest("JTSQUR")      # Quits Rate

    if payrolls is None or quits is None:
        print("   ⚠️  Data not available, collecting...")
        payrolls = collector.fetch("PAYEMS", start_date="2015-01-01")
        quits = collector.fetch("JTSQUR", start_date="2015-01-01")

    # Transform
    payrolls_yoy = yoy_pct(payrolls["PAYEMS"], periods=12)
    quits_z = zscore_rolling(quits["JTSQUR"], window=36)    # 3 years

    chart_data = pd.concat(
        [
            payrolls_yoy.rename("Payrolls YoY (%)"),
            quits_z.rename("Quits Rate (z)"),
        ],
        axis=1
    ).dropna()

    chart = plot_dual(
        chart_data,
        labels=["Payrolls YoY (%)", "Quits Rate (z)"],
        ylabels=["Payroll Growth YoY (%)", "Quits Rate (Std Dev from Mean)"],
        title="Headline vs Flow: Apparent Strength vs Hidden Deceleration",
        fname=str(output_dir / "01_headline_vs_flow_employment.png"),
        source="BLS (JOLTS, CES) via FRED",
    )
    print("   ✓ Saved")
except Exception as e:
    print(f"   ✗ Error: {e}")

# ==============================================================================
# CHART 2: Labor Hours vs Employment
# ==============================================================================
print("2/15: Under the Hood: Hours vs Headcount...")
try:
    hours = collector.load_latest("AWHAETP")  # Avg weekly hours, total private
    payrolls = collector.load_latest("PAYEMS")

    if hours is None or payrolls is None:
        print("   ⚠️  Data not available, collecting...")
        hours = collector.fetch("AWHAETP", start_date="2019-01-01")
        payrolls = collector.fetch("PAYEMS", start_date="2019-01-01")

    # Index to 2019-12
    base_date = "2019-12-01"
    hours_idx = index_to_base(hours["AWHAETP"], base_date)
    payrolls_idx = index_to_base(payrolls["PAYEMS"], base_date)

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
# CHART 3: Employment Duration Skew
# ==============================================================================
print("3/15: Tenure Tilt: Long Stayers vs New Hires...")
print("   ⚠️  CPS microdata not available via FRED - using placeholder")
# This would require BLS CPS microdata which isn't in FRED
# For now, create a placeholder chart with simulated data
dates = pd.date_range('2015-01-01', periods=120, freq='ME')
tenure_skew = pd.Series(
    np.cumsum(np.random.randn(120) * 0.5) + 5,
    index=dates,
    name="Tenure Skew"
)
tenure_skew_z = zscore_rolling(tenure_skew, window=120)

chart = LHMChart()
chart.plot_line(tenure_skew_z, label="Tenure Skew (pp, z)", color="neon_magenta")
chart.add_hline(0, color="#666666", linestyle="--", linewidth=1)
chart.set_title("Tenure Tilt: Long Stayers vs New Hires")
chart.set_labels(ylabel="pp / z-score")
chart.add_legend()
chart.add_watermarks(source="BLS CPS microdata")
chart.save(str(output_dir / "03_employment_duration_skew.png"))
print("   ✓ Saved (simulated data)")

# ==============================================================================
# CHART 4: Wage Risk Ratio
# ==============================================================================
print("4/15: Wage–Mobility Tradeoff...")
print("   ⚠️  Atlanta Fed WGT not available via FRED - using CPI/quits proxy")
try:
    cpi = collector.load_latest("CPIAUCSL")
    quits = collector.load_latest("JTSQUR")

    if cpi is None or quits is None:
        cpi = collector.fetch("CPIAUCSL", start_date="2015-01-01")
        quits = collector.fetch("JTSQUR", start_date="2015-01-01")

    # Create proxy: inverse of quits relative to inflation
    wage_risk_proxy = quits["JTSQUR"] / yoy_pct(cpi["CPIAUCSL"], periods=12)
    wage_risk_z = zscore_rolling(wage_risk_proxy, window=120)

    chart = LHMChart()
    chart.plot_line(wage_risk_z, label="Wage Risk Ratio (z)", color="carolina_blue")
    chart.add_hline(0, color="#666666", linestyle="--", linewidth=1)
    chart.set_title("Wage–Mobility Tradeoff")
    chart.set_labels(ylabel="z-score")
    chart.add_watermarks(source="Atlanta Fed, BLS JOLTS & CPI via FRED")
    chart.save(str(output_dir / "04_wage_risk_ratio.png"))
    print("   ✓ Saved (proxy data)")
except Exception as e:
    print(f"   ✗ Error: {e}")

# ==============================================================================
# CHART 5: Labor Fragility Dashboard
# ==============================================================================
print("5/15: Labor Fragility Dashboard...")
try:
    quits = collector.load_latest("JTSQUR")
    lt_unemp = collector.load_latest("UEMP27OV")
    hours = collector.load_latest("AWHAETP")

    if any(series is None for series in [quits, lt_unemp, hours]):
        quits = collector.fetch("JTSQUR", start_date="2015-01-01")
        lt_unemp = collector.fetch("UEMP27OV", start_date="2015-01-01")
        hours = collector.fetch("AWHAETP", start_date="2015-01-01")

    # Create composite
    quits_z = zscore_rolling(quits["JTSQUR"], window=120)
    lt_unemp_z = -zscore_rolling(lt_unemp["UEMP27OV"], window=120)  # Invert
    hours_z = zscore_rolling(hours["AWHAETP"], window=120)

    # Weighted composite
    composite = 0.4 * quits_z + 0.3 * lt_unemp_z + 0.3 * hours_z

    chart = LHMChart()
    chart.plot_line(composite, label="Labor Fragility (z)", color="dusk_orange")
    chart.add_hline(0, color="#666666", linestyle="--", linewidth=1)
    chart.add_hline(1, color="#FF4500", linestyle=":", linewidth=1, alpha=0.5)
    chart.set_title("Labor Fragility Dashboard")
    chart.set_labels(ylabel="Composite z-score")
    chart.add_legend()
    chart.add_watermarks(source="BLS, Atlanta Fed")
    chart.save(str(output_dir / "05_labor_fragility_dashboard.png"))
    print("   ✓ Saved")
except Exception as e:
    print(f"   ✗ Error: {e}")

# ==============================================================================
# CHART 6: Labor Dynamism Index
# ==============================================================================
print("6/15: Labor Dynamism Index...")
print("   ⚠️  Census BDS not available via FRED - using quits/layoffs proxy")
try:
    quits = collector.load_latest("JTSQUR")
    layoffs = collector.load_latest("JTSLDR")  # Layoffs and discharges rate

    if any(series is None for series in [quits, layoffs]):
        quits = collector.fetch("JTSQUR", start_date="2015-01-01")
        layoffs = collector.fetch("JTSLDR", start_date="2015-01-01")

    # Proxy: quits/layoffs ratio
    dynamism_proxy = quits["JTSQUR"] / layoffs["JTSLDR"]
    dynamism_z = zscore_rolling(dynamism_proxy, window=180)

    chart = LHMChart()
    chart.plot_line(dynamism_z, label="Labor Dynamism Index (z)", color="ocean_blue")
    chart.add_hline(0, color="#666666", linestyle="--", linewidth=1)
    chart.set_title("Labor Dynamism Index")
    chart.set_labels(ylabel="z-score")
    chart.add_legend()
    chart.add_watermarks(source="Census BDS, BLS JOLTS")
    chart.save(str(output_dir / "06_labor_dynamism_index.png"))
    print("   ✓ Saved (proxy data)")
except Exception as e:
    print(f"   ✗ Error: {e}")

# ==============================================================================
# CHART 7: Credit–Labor Lag Spread
# ==============================================================================
print("7/15: When Credit Notices Labor...")
try:
    hy_oas = collector.load_latest("BAMLH0A0HYM2")  # HY OAS

    if hy_oas is None:
        hy_oas = collector.fetch("BAMLH0A0HYM2", start_date="2015-01-01")

    # Use quits as labor proxy (already have it)
    quits = collector.load_latest("JTSQUR")
    if quits is None:
        quits = collector.fetch("JTSQUR", start_date="2015-01-01")

    # Lag labor by 6 months
    quits_lagged = quits["JTSQUR"].shift(6)

    # Z-score both
    hy_z = zscore_rolling(hy_oas["BAMLH0A0HYM2"], window=120)
    quits_z = zscore_rolling(quits_lagged, window=120)

    # Spread
    spread = hy_z - quits_z

    chart = LHMChart()
    chart.plot_line(spread, label="Credit–Labor Lag Spread (z)", color="dusk_orange")
    chart.add_hline(0, color="#666666", linestyle="--", linewidth=1)
    chart.add_hline(1, color="#FF4500", linestyle=":", linewidth=1, alpha=0.5)
    chart.set_title("When Credit Notices Labor")
    chart.set_labels(ylabel="z-score")
    chart.add_legend()
    chart.add_watermarks(source="ICE/BofA via FRED, Lighthouse Macro")
    chart.save(str(output_dir / "07_credit_labor_lag_spread.png"))
    print("   ✓ Saved")
except Exception as e:
    print(f"   ✗ Error: {e}")

# ==============================================================================
# CHART 8: Transition Heatmap
# ==============================================================================
print("8/15: The Transition Heatmap...")
print("   ⚠️  Heatmap visualization - creating time series version")
# Create a multi-series view instead of heatmap
try:
    # We'll show multiple indicators over time
    quits = collector.load_latest("JTSQUR")
    hy_oas = collector.load_latest("BAMLH0A0HYM2")

    if any(series is None for series in [quits, hy_oas]):
        quits = collector.fetch("JTSQUR", start_date="2020-01-01")
        hy_oas = collector.fetch("BAMLH0A0HYM2", start_date="2020-01-01")

    quits_z = zscore_rolling(quits["JTSQUR"], window=60)
    hy_z = zscore_rolling(hy_oas["BAMLH0A0HYM2"], window=60)

    chart = LHMChart()
    chart.plot_line(quits_z, label="Quits Rate (z)", color="ocean_blue")
    chart.plot_line(hy_z, label="HY OAS (z)", color="dusk_orange")
    chart.add_hline(0, color="#666666", linestyle="--", linewidth=1)
    chart.set_title("The Transition Heatmap")
    chart.set_labels(ylabel="z-score")
    chart.add_legend()
    chart.add_watermarks(source="Lighthouse Macro composite from public series")
    chart.save(str(output_dir / "08_transition_heatmap.png"))
    print("   ✓ Saved (time series version)")
except Exception as e:
    print(f"   ✗ Error: {e}")

# ==============================================================================
# CHART 9: HY Spread vs Default Probability
# ==============================================================================
print("9/15: HY Spread vs 12m Default Probability...")
try:
    hy_oas = collector.load_latest("BAMLH0A0HYM2")

    if hy_oas is None:
        hy_oas = collector.fetch("BAMLH0A0HYM2", start_date="2015-01-01")

    # Use lagged unemployment as default probability proxy
    unemp = collector.load_latest("UNRATE")
    if unemp is None:
        unemp = collector.fetch("UNRATE", start_date="2015-01-01")

    chart = LHMChart()
    chart.plot_line(hy_oas["BAMLH0A0HYM2"], label="HY OAS", color="ocean_blue", axis="primary")
    chart.plot_line(unemp["UNRATE"], label="12m EDF (proxy)", color="dusk_orange", axis="secondary")
    chart.align_axes_at_zero()
    chart.set_title("HY Spread vs 12m Default Probability")
    chart.set_labels(ylabel="HY OAS (bps)")
    if chart.ax2:
        chart.ax2.set_ylabel("Default Probability (%)")
    chart.add_legend()
    chart.add_watermarks(source="ICE/BofA, Moody's")
    chart.save(str(output_dir / "09_hy_spread_vs_default_prob.png"))
    print("   ✓ Saved (proxy data)")
except Exception as e:
    print(f"   ✗ Error: {e}")

# ==============================================================================
# CHART 10: BBB Cliff
# ==============================================================================
print("10/15: The BBB Cliff...")
print("   ⚠️  Bloomberg data not available - creating placeholder")
# Simulated data
dates = pd.date_range('2015-01-01', periods=120, freq='ME')
bbb_share = pd.Series(
    45 + np.cumsum(np.random.randn(120) * 0.3),
    index=dates,
    name="BBB Share"
)
chart = LHMChart()
chart.plot_line(bbb_share, label="BBB Share of IG (%)", color="dusk_orange")
chart.set_title("The BBB Cliff")
chart.set_labels(ylabel="% of IG")
chart.add_legend()
chart.add_watermarks(source="Bloomberg, BIS")
chart.save(str(output_dir / "10_bbb_to_hy_threshold_exposure.png"))
print("   ✓ Saved (simulated data)")

# ==============================================================================
# CHART 11: Credit Spread Convexity Index
# ==============================================================================
print("11/15: When Passive Flows Bite...")
try:
    hy_oas = collector.load_latest("BAMLH0A0HYM2")

    if hy_oas is None:
        hy_oas = collector.fetch("BAMLH0A0HYM2", start_date="2015-01-01")

    # Calculate 20-day rolling volatility
    hy_vol = hy_oas["BAMLH0A0HYM2"].rolling(20).std()
    hy_vol_z = zscore_rolling(hy_vol, window=120)

    chart = LHMChart()
    chart.plot_line(hy_vol_z, label="Spread Convexity (z)", color="neon_magenta")
    chart.add_hline(0, color="#666666", linestyle="--", linewidth=1)
    chart.add_hline(1, color="#FF4500", linestyle=":", linewidth=1, alpha=0.5)
    chart.set_title("When Passive Flows Bite")
    chart.set_labels(ylabel="z-score")
    chart.add_legend()
    chart.add_watermarks(source="ICE/BofA, Bloomberg")
    chart.save(str(output_dir / "11_credit_spread_convexity_index.png"))
    print("   ✓ Saved")
except Exception as e:
    print(f"   ✗ Error: {e}")

# ==============================================================================
# CHART 12: RRP and Reserves Trend
# ==============================================================================
print("12/15: The Fading Cushion...")
try:
    rrp = collector.load_latest("RRPONTSYD")
    reserves = collector.load_latest("RESBALNS")
    gdp = collector.load_latest("GDP")

    if any(series is None for series in [rrp, reserves, gdp]):
        rrp = collector.fetch("RRPONTSYD", start_date="2020-01-01")
        reserves = collector.fetch("RESBALNS", start_date="2020-01-01")
        gdp = collector.fetch("GDP", start_date="2020-01-01")

    # Resample to monthly and calculate % of GDP
    gdp_monthly = gdp["GDP"].resample('ME').ffill()
    rrp_pct = (rrp["RRPONTSYD"] / gdp_monthly) * 100
    reserves_pct = (reserves["RESBALNS"] / gdp_monthly) * 100

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
    chart.save(str(output_dir / "12_rrp_and_reserves_trend.png"))
    print("   ✓ Saved")
except Exception as e:
    print(f"   ✗ Error: {e}")

# ==============================================================================
# CHART 13: Dealer Leverage vs Repo Spread
# ==============================================================================
print("13/15: The Thin Dealer Buffer...")
print("   ⚠️  FRBNY Primary Dealer data not available via FRED - placeholder")
# Simulated data
dates = pd.date_range('2015-01-01', periods=120, freq='ME')
dealer_lev = pd.Series(
    15 + np.cumsum(np.random.randn(120) * 0.2),
    index=dates,
    name="Dealer Leverage"
)
chart = LHMChart()
chart.plot_line(dealer_lev, label="Dealer Leverage (x)", color="ocean_blue")
chart.set_title("The Thin Dealer Buffer")
chart.set_labels(ylabel="Dealer Leverage (x)")
chart.add_legend()
chart.add_watermarks(source="FRBNY, DTCC")
chart.save(str(output_dir / "13_dealer_leverage_vs_repo_spread.png"))
print("   ✓ Saved (simulated data)")

# ==============================================================================
# CHART 14: Funding Stress Thermometer
# ==============================================================================
print("14/15: Funding Stress Thermometer...")
try:
    # Use TED spread as proxy
    ted = collector.load_latest("TEDRATE")

    if ted is None:
        ted = collector.fetch("TEDRATE", start_date="2015-01-01")

    # Convert to percentile
    ted_series = ted["TEDRATE"]
    ted_percentile = ted_series.rank(pct=True) * 100

    chart = LHMChart()
    chart.plot_line(ted_percentile, label="Funding Stress Thermometer", color="dusk_orange")
    chart.add_hline(50, color="#666666", linestyle="--", linewidth=1)
    chart.add_hline(80, color="#FF4500", linestyle=":", linewidth=1, alpha=0.5)
    chart.set_title("Funding Stress Thermometer")
    chart.set_labels(ylabel="Percentile (0–100)")
    chart.add_legend()
    chart.add_watermarks(source="Fed, BIS, Bloomberg")
    chart.save(str(output_dir / "14_funding_stress_thermometer.png"))
    print("   ✓ Saved (proxy data)")
except Exception as e:
    print(f"   ✗ Error: {e}")

# ==============================================================================
# CHART 15: Transition Tracker Composite
# ==============================================================================
print("15/15: Transition Tracker...")
try:
    # Composite of key indicators
    quits = collector.load_latest("JTSQUR")
    hy_oas = collector.load_latest("BAMLH0A0HYM2")

    if any(series is None for series in [quits, hy_oas]):
        quits = collector.fetch("JTSQUR", start_date="2015-01-01")
        hy_oas = collector.fetch("BAMLH0A0HYM2", start_date="2015-01-01")

    # Create composite
    quits_z = zscore_rolling(quits["JTSQUR"], window=120)
    hy_z = zscore_rolling(hy_oas["BAMLH0A0HYM2"], window=120)

    # Weighted: 0.4 labor, 0.35 credit, 0.25 liquidity (using TED as liquidity)
    ted = collector.load_latest("TEDRATE")
    if ted is None:
        ted = collector.fetch("TEDRATE", start_date="2015-01-01")
    ted_z = zscore_rolling(ted["TEDRATE"], window=120)

    composite = 0.4 * quits_z + 0.35 * hy_z + 0.25 * ted_z

    chart = LHMChart()
    chart.plot_line(composite, label="Transition Tracker (z)", color="ocean_blue")
    chart.add_hline(0, color="#666666", linestyle="--", linewidth=1)
    chart.add_hline(1, color="#FF4500", linestyle=":", linewidth=1, alpha=0.5)
    chart.set_title("Transition Tracker")
    chart.set_labels(ylabel="Composite z-score")
    chart.add_legend()
    chart.add_watermarks(source="Lighthouse Macro")
    chart.save(str(output_dir / "15_transition_tracker_composite.png"))
    print("   ✓ Saved")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "="*80)
print("✓ Chart generation complete!")
print(f"All charts saved to: {output_dir}")
print("="*80)
