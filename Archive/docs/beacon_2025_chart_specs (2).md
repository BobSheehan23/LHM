# The Beacon: Chart Data Specifications (October 2025)

Author: Bob Sheehan, CFA, CMT | Lighthouse Macro | October 2025

---

This document details data collection, sources, and transformation instructions for all 15 charts in "The Beacon: The Hidden Transition". Each chart section lists the source, precise fields/range, and transformation or calculation needed to match the reporting and visual standards used by Lighthouse Macro. Data must be sourced exactly as described—never fabricated. Readers should find this a fully reproducible research record for Lighthouse Macro’s 2025 cycle inflection report.

## Chart 1: Unemployment Rate vs. Quits Rate (Dual Axis)
- **Data Location:**
  - Unemployment Rate: BLS Employment Situation, Series LNS14000000, monthly Jan 2019–Oct 2025
  - Quits Rate: BLS JOLTS database, Series JTSQUR (Total Nonfarm), monthly Jan 2019–Oct 2025
- **Transformation:**
  - Plot unemployment on left axis, quits rate on right; highlight divergence from 2022–2025
- **Processing:**
  - Monthly average, no smoothing; annotate COVID and post-COVID inflection points

## Chart 2: Credit Spreads – BBB & HY OAS vs. Historical Percentiles
- **Data Location:**
  - BBB OAS: ICE BofA BBB US Corporate Index Option-Adjusted Spread (BAMLC0A4CBBB, FRED), Jan 2000–Oct 2025
  - HY OAS: ICE BofA US High Yield Index Option-Adjusted Spread (BAMLH0A0HYM2, FRED)
- **Transformation:**
  - Percentile shading calculated across Jan 2000–Oct 2025; plot current spread as line with percentiles as background bands

## Chart 3: Quits Rate 2019–Present
- **Data Location:**
  - BLS JOLTS, JTSQUR, Total Nonfarm, monthly Jan 2019–Oct 2025
- **Transformation:**
  - Direct line plot, annotate peak (Great Resignation) and low (current 2025 value)
  - No smoothing

## Chart 4: Long-Duration Unemployment (27+ Weeks)
- **Data Location:**
  - BLS CPS Table A-12, Persons Unemployed 27 Weeks and Over (UEMP27OV), monthly Jan 2019–Oct 2025
- **Transformation:**
  - Plot as both count (Millions) and share of total unemployed; shaded area for percent of total

## Chart 5: Job Openings vs. Hires Rate (Dual Axis)
- **Data Location:**
  - Job Openings: BLS JOLTS, JTSJOL (Total Nonfarm), monthly Jan 2019–Oct 2025
  - Hires Rate: BLS JOLTS, JTSHIR (Total Nonfarm), monthly
- **Transformation:**
  - Plot both series, dual Y-axis; annotate periods of delta = 0 (plateau)

## Chart 6: Avg Weekly Hours Worked (Manufacturing & Services)
- **Data Location:**
  - Manufacturing: BLS CES, Series AWHAEMAN, monthly
  - Services: BLS CES, Series AWHAESER, monthly (if needed, use subcomponent)
- **Transformation:**
  - Simple line plot for each; highlight pre-recession, COVID-era, and current levels

## Chart 7: BBB Credit Spreads – Historical Percentiles
- **Data Location:**
  - BAMLC0A4CBBB (ICE BofA BBB OAS, FRED), Jan 2000–Oct 2025
- **Transformation:**
  - Calculate rolling percentile (window/all-time) for the time series and shade accordingly

## Chart 8: HY Spread vs. Default Rate
- **Data Location:**
  - BAMLH0A0HYM2 (ICE BofA US HY OAS, FRED)
  - Default Rate: Moody’s US HY Default Rate, monthly/quarterly
- **Transformation:**
  - Dual-axis, line both series; highlight disconnect post-pandemic and in 2025
- **Processing:**
  - Use 12m trailing default rate for comparison

## Chart 9: Credit Spreads vs. Labor Leading Indicators (Lag Analysis)
- **Data Location:**
  - BBB OAS: BAMLC0A4CBBB (FRED)
  - Labor Composite: Custom, see Chart 15 below
- **Transformation:**
  - Plot labor composite (Chart 15), overlay with inverted BBB OAS (inverted due to lag)
  - Quantify 3-6m lag visually and in footnote

## Chart 10: Fed ON RRP Facility Balance
- **Data Location:**
  - Federal Reserve H.4.1 Release / FRED (RRPONTSYD), daily or monthly totals, Jan 2022–Oct 2025
- **Transformation:**
  - Area chart, mark Dec 2022 peak, Oct 2025 value
- **Processing:**
  - Monthly/month end, with annotation of inflection points

## Chart 11: Bank Reserves + RRP Combined System Liquidity
- **Data Location:**
  - Bank reserves: FRED TOTRESNS, monthly
  - RRP: FRED RRPONTSYD, monthly
- **Transformation:**
  - Stacked area chart, sum both to show total system liquidity evolution
  - Annotate depletion of RRP and stable reserves period

## Chart 12: Primary Dealer Net Treasury Positions
- **Data Location:**
  - NY Fed Primary Dealer Statistics, "Net Positions in U.S. Treasury Securities" (total and by maturity), quarterly/monthly
- **Transformation:**
  - Line chart showing net position vs. regulatory capital headroom
  - Add SLR (Supplementary Leverage Ratio) constraint as reference

## Chart 13: Credit Spread Widening vs. SP500 Forward PE (Lead-Lag)
- **Data Location:**
  - BBB OAS: FRED BAMLC0A4CBBB, Jan 2019–Oct 2025
  - SP500 Forward PE: MacroMicro, YCharts, or FactSet, Jan 2019–Oct 2025
- **Transformation:**
  - Scatter or dual-axis line showing that BBB OAS leads changes in SP500 forward PE by 3-6 months
  - Annotate lead-lag
  
## Chart 14: 2s10s Yield Curve vs. Credit Spreads
- **Data Location:**
  - 2s10s curve: FRED, T10Y2Y, daily/monthly
  - BBB OAS: FRED BAMLC0A4CBBB
- **Transformation:**
  - Plot both series; highlight yield curve inversion and steepening alongside credit spread expansion

## Chart 15: Composite Leading Labor Indicator (Lighthouse Macro Proprietary)
- **Data Location:**
  - Inputs: Quits Rate (JTSQUR), Long-Duration UE (UEMP27OV share), Job Openings/Hires Ratio (JTSJOL/JTSHIR), Avg Weekly Hours (AWHAEMAN)
- **Transformation:**
  - Z-score each input, scale as follows: Quits Rate (weight 40%, inverted), Long-duration UE (30%, inverted), Openings/Hires Ratio (20%), Avg Hours (10%); composite = weighted sum
  - Smooth using 3m moving average; chart final index value

---

# Notes/Standards
- **Sources:** All chart data must use the precise FRED/BLS series and field codes given, or Moody’s/NY Fed when noted. All transformations (percentile, z-score, lead/lag) must be code-reproducible.
- **Chart Style:**
  - No gridlines, four spines visible
  - Color palette: Ocean Blue, Deep Sunset Orange, Neon Carolina Blue, Neon Magenta, Light Gray (see lighthousemacro.com/brand-standards)
  - Line width 2.5–3
  - Y-axes start at zero unless log/stdev indicated, annotate critical values/inflections
  - Watermark "Lighthouse Macro" top-left, "MACRO, ILLUMINATED." lower-right, always out of data region
---

