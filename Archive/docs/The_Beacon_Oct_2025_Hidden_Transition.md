# The Beacon | October 2025  
**The Hidden Transition**  
**Lighthouse Macro Research | October 2025**  
*Empirical narratives for late‑cycle clarity.*

---

## Executive Summary

Resilience has become the market’s most dangerous illusion. Headline strength conceals a slow‑motion erosion in the labor and credit foundations that sustained the cycle. The data points diverge: employment looks solid, but churn, duration, and wage behavior show a system quietly exhausting itself. The same misperception extends to credit spreads and liquidity conditions—surface calm masking structural fragility.

The plateau before the slope has arrived. Markets are mispricing asymmetric risk: the transition—not the collapse—is the story.

---

[[CHART: Headline_vs_Flow_Employment]]

```yaml
chart:
  id: Headline_vs_Flow_Employment
  title: "Headline vs Flow: Payrolls vs Quits"
  subtitle: "Apparent employment strength vs decaying labor churn"
  tags: ["labor", "employment", "flows", "quits", "late-cycle"]
  frequency: "monthly"
  region: "United States"
  units: "YoY %, z-score"
  sources:
    - name: "BLS (CES) via FRED"
      series: ["PAYEMS"]
    - name: "BLS (JOLTS) via FRED"
      series: ["JTSQUR"]  # Quits Rate: Total Nonfarm
  data:
    series:
      - id: "PAYEMS"
        transform:
          - pct_change_yoy: {}
      - id: "JTSQUR"
        transform:
          - zscore:
              lookback_years: 3
  calc:
    description: "Compare YoY change in nonfarm payrolls (PAYEMS) with quits rate deviation from 3-year mean (z-score)."
    steps:
      - align: {method: "inner", how: "end_of_month"}
      - scale:
          PAYEMS_yoy: {zscore: {lookback_years: 10}}
      - rename:
          PAYEMS_yoy_z: "Payrolls YoY (z)"
          JTSQUR_z: "Quits Rate (z)"
  visualization:
    chart_type: "line"
    axes:
      primary_axis: "right"
      y:
        label: "Standard deviations from mean"
      x:
        label: "Date"
    series:
      - key: "Payrolls YoY (z)"
        color: "#0077BE"
        linewidth: 3
      - key: "Quits Rate (z)"
        color: "#FF4500"
        linewidth: 3
    legend:
      position: "top_left"
      show: true
    reference_lines:
      - y: 0
        style: "solid"
        color: "#A9A9A9"
    value_tags:
      enabled: true
      rounded_rect: true
      font_color: "#FFFFFF"
      drop_shadow: true
  style:
    background: "#FFFFFF"
    spines: {top: true, right: true, bottom: true, left: true}
    grid: {show: false}
    font_family: "Inter, Helvetica, Arial, sans-serif"
    text_color: "#5A5A5A"
    palette:
      primary: "#0077BE"
      highlight: "#FF4500"
      overlay: "#00BFFF"
      momentum: "#FF00FF"
      neutral: "#A9A9A9"
  export:
    aspect_ratio: "16:9"
    data_region_ratio: "12:7"
    border:
      size_in: 0.25
      color: "#0077BE"
    watermark:
      header: {text: "LIGHTHOUSE MACRO", color: "#0077BE", position: "top-left", small_caps: true}
      footer: {text: "MACRO, ILLUMINATED.", color: "#0077BE", position: "bottom-right", outside_axes: true}
    footer_note: "Source: BLS (JOLTS, CES) via FRED | Calc: YoY payrolls vs quits z-score (3y mean)."
  refresh:
    schedule: "monthly"
    lag_days: 7
  audit:
    script_path: "charts/labor/headline_vs_flow_employment.py"
    version: "2.2"
  last_updated: "2025-10-28"
```

---

## The Plateau Paradox

Momentum persists long after vitality fades. The labor market’s apparent durability has lulled investors into extrapolating stability from a system running on inertia. Flow data—quits, job openings, and employment duration—signal that adjustment is already underway. The paradox: the more investors believe in “resilience,” the more risk concentrates around the inevitable mean reversion. This is not equilibrium—it’s the plateau before the slope.

Households and firms are acting differently. Workers are sticking rather than switching; firms are hoarding rather than hiring. That cocktail cools wage growth, flattens consumption, and delays the credit reckoning just long enough to convince people it won’t arrive. The transition hides in the averages.

---

## I. The Labor Market: The Silent Deceleration

The slowdown began not in layoffs but in behavior. Workers stopped moving. The quits rate has retraced to lows last seen during the early normalization phase, erasing much of the post‑pandemic churn that fueled wage gains. Meanwhile, hours worked are slipping even as payrolls still expand—classic late‑cycle labor hoarding.

[[CHART: Labor_Hours_vs_Employment]]

```yaml
chart:
  id: Labor_Hours_vs_Employment
  title: "Under the Hood: Hours vs Headcount"
  subtitle: "Labor hoarding meets weaker demand"
  tags: ["labor", "hours", "employment", "underutilization"]
  frequency: "monthly"
  region: "United States"
  units: "Index (2019=100)"
  sources:
    - name: "BLS (CES) via FRED"
      series: ["CES0500000008", "PAYEMS"]
  data:
    base_date: "2019-12-01"
    series:
      - id: "CES0500000008"  # Avg weekly hours, production & nonsupervisory
        transform:
          - index_to_base:
              base_date: "2019-12-01"
      - id: "PAYEMS"
        transform:
          - index_to_base:
              base_date: "2019-12-01"
  calc:
    description: "Index average weekly hours and total nonfarm payrolls to a common base to show decoupling."
  visualization:
    chart_type: "line"
    axes:
      primary_axis: "right"
      y:
        label: "Index (2019=100)"
      x:
        label: "Date"
    series:
      - key: "Avg Weekly Hours (2019=100)"
        source: "CES0500000008_index"
        color: "#FF4500"
        linewidth: 3
      - key: "Total Nonfarm Payrolls (2019=100)"
        source: "PAYEMS_index"
        color: "#0077BE"
        linewidth: 3
    legend:
      position: "top_left"
    value_tags:
      enabled: true
      rounded_rect: true
      font_color: "#FFFFFF"
      drop_shadow: true
  style:
    background: "#FFFFFF"
    spines: {top: true, right: true, bottom: true, left: true}
    grid: {show: false}
    font_family: "Inter"
    text_color: "#5A5A5A"
    palette:
      primary: "#0077BE"
      highlight: "#FF4500"
      neutral: "#A9A9A9"
  export:
    aspect_ratio: "16:9"
    data_region_ratio: "12:7"
    border: {size_in: 0.25, color: "#0077BE"}
    watermark:
      header: {text: "LIGHTHOUSE MACRO", color: "#0077BE", position: "top-left", small_caps: true}
      footer: {text: "MACRO, ILLUMINATED.", color: "#0077BE", position: "bottom-right", outside_axes: true}
    footer_note: "Source: BLS CES via FRED | Calc: Index (2019=100)."
  refresh: {schedule: "monthly", lag_days: 7}
  audit: {script_path: "charts/labor/hours_vs_employment.py", version: "2.2"}
  last_updated: "2025-10-28"
```

The brief bounce in quits earlier this year was a false dawn—more normalization in services than fresh dynamism. The distribution of employment tenure continues to skew longer: risk aversion replacing ambition. That tilt drags the wage engine because switching—not staying—delivers the step change in pay.

[[CHART: Employment_Duration_Skew]]

```yaml
chart:
  id: Employment_Duration_Skew
  title: "Tenure Tilt: Long Stayers vs New Hires"
  subtitle: "Behavioral shift toward job stickiness"
  tags: ["labor", "tenure", "behavior", "mobility"]
  frequency: "monthly"
  region: "United States"
  units: "pp (percentage points)"
  sources:
    - name: "BLS CPS Microdata"
      series: ["tenure_gt_5y_share", "tenure_lt_1y_share"]
  data:
    series:
      - id: "tenure_gt_5y_share"
      - id: "tenure_lt_1y_share"
  calc:
    description: "Share(tenure>5y) minus share(tenure<1y) to quantify labor stickiness."
    steps:
      - compute_spread:
          numerator: "tenure_gt_5y_share"
          denominator: "tenure_lt_1y_share"
          op: "minus"
          label: "Tenure Skew (pp)"
      - zscore:
          lookback_years: 10
  visualization:
    chart_type: "line"
    axes:
      primary_axis: "right"
      y: {label: "pp / z-score"}
      x: {label: "Date"}
    series:
      - key: "Tenure Skew (pp, z)"
        color: "#FF00FF"
        linewidth: 3
    legend: {position: "top_left", show: false}
    reference_lines:
      - y: 0
        color: "#A9A9A9"
        style: "dashed"
  style:
    background: "#FFFFFF"
    spines: {top: true, right: true, bottom: true, left: true}
    grid: {show: false}
    font_family: "Inter"
    text_color: "#5A5A5A"
  export:
    aspect_ratio: "16:9"
    data_region_ratio: "12:7"
    border: {size_in: 0.25, color: "#0077BE"}
    watermark:
      header: {text: "LIGHTHOUSE MACRO", color: "#0077BE", position: "top-left", small_caps: true}
      footer: {text: "MACRO, ILLUMINATED.", color: "#0077BE", position: "bottom-right", outside_axes: true}
    footer_note: "Source: BLS CPS microdata | Calc: Tenure>5y minus Tenure<1y (pp), z-scored."
  refresh: {schedule: "monthly", lag_days: 15}
  audit: {script_path: "charts/labor/employment_duration_skew.py", version: "2.2"}
  last_updated: "2025-10-28"
```

### Wage Dynamics and Bargaining Power

Nominal wage growth near the mid‑3s looks benign; real wage momentum has stalled. The Atlanta Fed’s Wage Growth Tracker shows median gains fading for job switchers—the group that leads aggregate acceleration. Bargaining power is eroding, not “soft‑landing” into vigor. When mobility cools, wage dispersion narrows, consumption growth moderates, and volatility migrates into balance sheets.

[[CHART: Wage_Risk_Ratio]]

```yaml
chart:
  id: Wage_Risk_Ratio
  title: "Wage–Mobility Tradeoff"
  subtitle: "Real wage momentum vs quits"
  tags: ["wages", "inflation", "quits", "consumption"]
  frequency: "monthly"
  region: "United States"
  units: "z-score"
  sources:
    - name: "Atlanta Fed Wage Growth Tracker"
      series: ["wgt_median_switchers", "wgt_median_stayers"]
    - name: "BLS (CPI) via FRED"
      series: ["CPIAUCSL"]
    - name: "BLS (JOLTS) via FRED"
      series: ["JTSQUR"]
  data:
    series:
      - id: "wgt_median_switchers"
      - id: "CPIAUCSL"
      - id: "JTSQUR"
  calc:
    description: "Real wage growth (switchers, CPI-adjusted) divided by quits rate; z-scored vs 10y mean."
    steps:
      - compute_real_growth:
          nominal_series: "wgt_median_switchers"
          deflator_series: "CPIAUCSL"
          method: "subtract_cpi_yoy"
          label: "Real WGT Switchers YoY"
      - ratio:
          numerator: "Real WGT Switchers YoY"
          denominator: "JTSQUR"
          label: "Wage Risk Ratio"
      - zscore:
          lookback_years: 10
  visualization:
    chart_type: "line"
    axes:
      primary_axis: "right"
      y: {label: "z-score"}
      x: {label: "Date"}
    series:
      - key: "Wage Risk Ratio (z)"
        color: "#00BFFF"
        linewidth: 3
    legend: {position: "top_left", show: false}
    reference_bands:
      - y_min: -1.0
        y_max: 1.0
        color: "#A9A9A9"
        opacity: 0.15
  style:
    background: "#FFFFFF"
    spines: {top: true, right: true, bottom: true, left: true}
    grid: {show: false}
  export:
    aspect_ratio: "16:9"
    data_region_ratio: "12:7"
    border: {size_in: 0.25, color: "#0077BE"}
    watermark:
      header: {text: "LIGHTHOUSE MACRO", color: "#0077BE", position: "top-left", small_caps: true}
      footer: {text: "MACRO, ILLUMINATED.", color: "#0077BE", position: "bottom-right", outside_axes: true}
    footer_note: "Source: Atlanta Fed, BLS JOLTS & CPI via FRED | Calc: Real WGT Switchers ÷ Quits, z-score."
  refresh: {schedule: "monthly", lag_days: 14}
  audit: {script_path: "charts/labor/wage_risk_ratio.py", version: "2.2"}
  last_updated: "2025-10-28"
```

### Composite Labor Fragility

Late‑cycle labor weakness rarely announces itself in a single marquee series. It accumulates in the corners: long‑term unemployment inches higher, hours fade, job‑finding slows, and wage diffusion narrows. We roll these into a composite that leads the final downgrade in risk appetite.

[[CHART: Labor_Fragility_Dashboard]]

```yaml
chart:
  id: Labor_Fragility_Dashboard
  title: "Labor Fragility Dashboard"
  subtitle: "Composite warning signal of late-cycle erosion"
  tags: ["labor", "composite", "fragility", "dashboard"]
  frequency: "monthly"
  region: "United States"
  units: "z-score"
  sources:
    - name: "BLS (JOLTS/CPS/CES) via FRED"
      series: ["JTSQUR", "UEMP27OV", "CIVPART", "LNS14027660", "CES0500000008"]
    - name: "Atlanta Fed WGT"
      series: ["wgt_diffusion"]
    - name: "Others"
      series: ["job_finding_rate_proxy"]
  data:
    series:
      - id: "JTSQUR"        # Quits rate
      - id: "UEMP27OV"      # Unemployed 27+ weeks
      - id: "CES0500000008" # Avg weekly hours
      - id: "job_finding_rate_proxy"
      - id: "wgt_diffusion"
  calc:
    description: "Composite z-score of quits, LT unemployment share, hours, job-finding rate, and wage diffusion."
    steps:
      - standardize:
          fields: ["JTSQUR","UEMP27OV","CES0500000008","job_finding_rate_proxy","wgt_diffusion"]
          invert: ["UEMP27OV"]  # higher is worse
      - weighted_sum:
          weights:
            JTSQUR: 0.25
            UEMP27OV: 0.20
            CES0500000008: 0.20
            job_finding_rate_proxy: 0.20
            wgt_diffusion: 0.15
          label: "Labor Fragility (z)"
  visualization:
    chart_type: "line"
    axes:
      primary_axis: "right"
      y: {label: "Composite z-score"}
      x: {label: "Date"}
    series:
      - key: "Labor Fragility (z)"
        color: "#FF4500"
        linewidth: 3
    thresholds:
      - y: 1.0
        label: "Late-cycle risk"
        color: "#FF4500"
      - y: 0.0
        label: "Neutral"
        color: "#A9A9A9"
  style:
    background: "#FFFFFF"
    spines: {top: true, right: true, bottom: true, left: true}
    grid: {show: false}
  export:
    aspect_ratio: "16:9"
    data_region_ratio: "12:7"
    border: {size_in: 0.25, color: "#0077BE"}
    watermark:
      header: {text: "LIGHTHOUSE MACRO", color: "#0077BE", position: "top-left", small_caps: true}
      footer: {text: "MACRO, ILLUMINATED.", color: "#0077BE", position: "bottom-right", outside_axes: true}
    footer_note: "Source: BLS, Atlanta Fed | Calc: Weighted composite (z-scores)."
  refresh: {schedule: "monthly", lag_days: 15}
  audit: {script_path: "dashboards/labor/labor_fragility_dashboard.py", version: "2.2"}
  last_updated: "2025-10-28"
```

---

## Diagnostics Interlude: Proprietary Dashboards

Data without synthesis is noise. We formalize the transition through diagnostics that connect labor behavior to downstream credit and cross‑asset pricing.

[[CHART: Labor_Dynamism_Index]]

```yaml
chart:
  id: Labor_Dynamism_Index
  title: "Labor Dynamism Index"
  subtitle: "Firm births vs deaths × quits-to-layoffs"
  tags: ["dynamism", "firms", "quits", "layoffs"]
  frequency: "quarterly"
  region: "United States"
  units: "z-score"
  sources:
    - name: "Census Business Dynamics Statistics (BDS)"
      series: ["firm_birth_rate","firm_death_rate"]
    - name: "BLS (JOLTS) via FRED"
      series: ["JTSQUR","JTSLUR"]  # layoffs & discharges rate
  data:
    series:
      - id: "firm_birth_rate"
      - id: "firm_death_rate"
      - id: "JTSQUR"
      - id: "JTSLUR"
  calc:
    description: "Ratio of firm birth/death × quits/layoffs; z-scored."
    steps:
      - ratio:
          numerator: "firm_birth_rate"
          denominator: "firm_death_rate"
          label: "Birth/Death Ratio"
      - ratio:
          numerator: "JTSQUR"
          denominator: "JTSLUR"
          label: "Quits/Layoffs Ratio"
      - multiply:
          left: "Birth/Death Ratio"
          right: "Quits/Layoffs Ratio"
          label: "Labor Dynamism Index"
      - zscore:
          lookback_years: 15
  visualization:
    chart_type: "line"
    axes:
      primary_axis: "right"
      y: {label: "z-score"}
      x: {label: "Date"}
    series:
      - key: "Labor Dynamism Index (z)"
        color: "#0077BE"
        linewidth: 3
    reference_lines:
      - y: 0
        color: "#A9A9A9"
        style: "dashed"
  style:
    background: "#FFFFFF"
    spines: {top: true, right: true, bottom: true, left: true}
    grid: {show: false}
  export:
    aspect_ratio: "16:9"
    data_region_ratio: "12:7"
    border: {size_in: 0.25, color: "#0077BE"}
    watermark:
      header: {text: "LIGHTHOUSE MACRO", color: "#0077BE", position: "top-left", small_caps: true}
      footer: {text: "MACRO, ILLUMINATED.", color: "#0077BE", position: "bottom-right", outside_axes: true}
    footer_note: "Source: Census BDS, BLS JOLTS | Calc: (Birth/Death)×(Quits/Layoffs), z-scored."
  refresh: {schedule: "quarterly", lag_days: 60}
  audit: {script_path: "charts/labor/labor_dynamism_index.py", version: "2.2"}
  last_updated: "2025-10-28"
```

[[CHART: Credit_Labor_Lag_Spread]]

```yaml
chart:
  id: Credit_Labor_Lag_Spread
  title: "When Credit Notices Labor"
  subtitle: "HY OAS vs lagged Labor Fragility"
  tags: ["credit", "labor", "lead-lag", "spreads"]
  frequency: "monthly"
  region: "United States"
  units: "z-score"
  sources:
    - name: "ICE BofA US High Yield OAS via FRED"
      series: ["BAMLH0A0HYM2"]
    - name: "Lighthouse Macro"
      series: ["Labor_Fragility_z"]
  data:
    series:
      - id: "BAMLH0A0HYM2"
      - id: "Labor_Fragility_z"
        transform:
          - lag:
              periods: 6  # months
  calc:
    description: "HY OAS minus 6m-lagged Labor Fragility (both z-scored) to capture recognition delay."
    steps:
      - zscore: {fields: ["BAMLH0A0HYM2","Labor_Fragility_z_lag6"], lookback_years: 10}
      - spread:
          left: "BAMLH0A0HYM2_z"
          right: "Labor_Fragility_z_lag6_z"
          label: "Credit–Labor Lag Spread (z)"
  visualization:
    chart_type: "line"
    axes:
      primary_axis: "right"
      y: {label: "z-score"}
      x: {label: "Date"}
    series:
      - key: "Credit–Labor Lag Spread (z)"
        color: "#FF4500"
        linewidth: 3
    thresholds:
      - y: 1.0
        label: "Credit rich vs labor weak"
        color: "#FF4500"
  style:
    background: "#FFFFFF"
    spines: {top: true, right: true, bottom: true, left: true}
    grid: {show: false}
  export:
    aspect_ratio: "16:9"
    data_region_ratio: "12:7"
    border: {size_in: 0.25, color: "#0077BE"}
    watermark:
      header: {text: "LIGHTHOUSE MACRO", color: "#0077BE", position: "top-left", small_caps: true}
      footer: {text: "MACRO, ILLUMINATED.", color: "#0077BE", position: "bottom-right", outside_axes: true}
    footer_note: "Source: ICE/BofA via FRED, Lighthouse Macro | Calc: z-score spread, labor lagged 6m."
  refresh: {schedule: "monthly", lag_days: 5}
  audit: {script_path: "charts/credit/credit_labor_lag_spread.py", version: "2.2"}
  last_updated: "2025-10-28"
```

[[CHART: Transition_Heatmap]]

```yaml
chart:
  id: Transition_Heatmap
  title: "The Transition Heatmap"
  subtitle: "Cross-sectional fragility across labor, credit, liquidity"
  tags: ["heatmap", "composite", "state-of-cycle"]
  frequency: "monthly"
  region: "United States"
  units: "percentile"
  sources:
    - name: "Lighthouse Macro Composite"
      series:
        - "Labor_Fragility_z"
        - "HY_OAS_z"
        - "Funding_Stress_z"
        - "Yield_Curve_Inversion_z"
        - "Earnings_Diffusion_z"
        - "Quits_Rate_z"
        - "Reserves_to_GDP_z"
  data:
    series:
      - id: "Labor_Fragility_z"
      - id: "HY_OAS_z"
      - id: "Funding_Stress_z"
      - id: "Yield_Curve_Inversion_z"
      - id: "Earnings_Diffusion_z"
      - id: "Quits_Rate_z"
      - id: "Reserves_to_GDP_z"
  calc:
    description: "Percentile map of standardized indicators; red = deterioration."
    steps:
      - percentile_rank:
          fields: ["Labor_Fragility_z","HY_OAS_z","Funding_Stress_z","Yield_Curve_Inversion_z","Earnings_Diffusion_z","Quits_Rate_z","Reserves_to_GDP_z"]
          horizon_years: 20
  visualization:
    chart_type: "heatmap"
    palette: ["#0077BE","#00BFFF","#A9A9A9","#FF4500","#FF0000"]
    axes:
      primary_axis: "right"
    legend:
      show: true
      position: "bottom"
    annotations:
      - text: "Historically turns red 6–9 months before recessions in backtests"
        anchor: "top_right"
        color: "#5A5A5A"
  style:
    background: "#FFFFFF"
    spines: {top: true, right: true, bottom: true, left: true}
  export:
    aspect_ratio: "16:9"
    data_region_ratio: "12:7"
    border: {size_in: 0.25, color: "#0077BE"}
    watermark:
      header: {text: "LIGHTHOUSE MACRO", color: "#0077BE", position: "top-left", small_caps: true}
      footer: {text: "MACRO, ILLUMINATED.", color: "#0077BE", position: "bottom-right", outside_axes: true}
    footer_note: "Source: Lighthouse Macro composite from public series | Calc: percentile heatmap."
  refresh: {schedule: "monthly", lag_days: 7}
  audit: {script_path: "dashboards/composite/transition_heatmap.py", version: "2.2"}
  last_updated: "2025-10-28"
```

---

## II. Credit Markets: Pricing Perfection

High‑yield spreads hover near cycle tights even as default risk fattens in the background. Market logic equates steady payroll prints with stable cash flows. That skips the lag structure. Credit typically reprices one to two quarters after labor turnover peaks. We are sitting in that window.

Spreads also ignore quality migration. BBB now dominates IG market value; every downgrade concentrates duration and convexity in HY ETFs. That structure can trade like a gentle stream until it doesn’t—passive flows add mechanical convexity on the way up and down. The tail wags the dog.

[[CHART: HY_Spread_vs_Default_Prob]]

```yaml
chart:
  id: HY_Spread_vs_Default_Prob
  title: "HY Spread vs 12m Default Probability"
  subtitle: "Valuation implies too-sanguine default risk"
  tags: ["credit", "high-yield", "defaults", "valuation"]
  frequency: "monthly"
  region: "United States"
  units: "bps, %"
  sources:
    - name: "ICE BofA US HY OAS via FRED"
      series: ["BAMLH0A0HYM2"]
    - name: "Moody's EDF (12m-ahead)"
      series: ["moodys_edf_12m"]
  data:
    series:
      - id: "BAMLH0A0HYM2"
      - id: "moodys_edf_12m"
  calc:
    description: "Compare HY OAS (bps) vs 12m expected default probability."
    steps:
      - align: {method: "end_of_month"}
      - normalize:
          fields: ["BAMLH0A0HYM2","moodys_edf_12m"]
          method: "minmax"
  visualization:
    chart_type: "line_dual_axis"
    axes:
      primary_axis: "right"   # right = HY OAS
      y_right: {label: "HY OAS (bps)"}
      y_left: {label: "Default Probability (%)"}
    series:
      - key: "HY OAS"
        source: "BAMLH0A0HYM2"
        axis: "right"
        color: "#0077BE"
        linewidth: 3
      - key: "12m EDF"
        source: "moodys_edf_12m"
        axis: "left"
        color: "#FF4500"
        linewidth: 3
    legend: {position: "top_left", show: true}
    notes:
      - "Independent scaling; zero lines matched as per dual-axis standard."
  style:
    background: "#FFFFFF"
    spines: {top: true, right: true, bottom: true, left: true}
    grid: {show: false}
  export:
    aspect_ratio: "16:9"
    data_region_ratio: "12:7"
    border: {size_in: 0.25, color: "#0077BE"}
    watermark:
      header: {text: "LIGHTHOUSE MACRO", color: "#0077BE", position: "top-left", small_caps: true}
      footer: {text: "MACRO, ILLUMINATED.", color: "#0077BE", position: "bottom-right", outside_axes: true}
    footer_note: "Source: ICE/BofA, Moody’s | Calc: Level comparison, normalized for visualization."
  refresh: {schedule: "monthly", lag_days: 10}
  audit: {script_path: "charts/credit/hy_spread_vs_default_prob.py", version: "2.2"}
  last_updated: "2025-10-28"
```

[[CHART: BBB_to_HY_Threshold_Exposure]]

```yaml
chart:
  id: BBB_to_HY_Threshold_Exposure
  title: "The BBB Cliff"
  subtitle: "Market value exposed to HY via one-notch migration"
  tags: ["credit", "fallen-angels", "BBB", "HY"]
  frequency: "monthly"
  region: "United States"
  units: "USD trillions, % of IG"
  sources:
    - name: "Bloomberg Indexes"
      series: ["IG_BBB_market_value","IG_total_market_value","BBB_leverage_gt_4x_share"]
    - name: "BIS Credit Stats"
      series: ["bbb_eligibles"]
  data:
    series:
      - id: "IG_BBB_market_value"
      - id: "IG_total_market_value"
      - id: "BBB_leverage_gt_4x_share"
  calc:
    description: "Exposure of BBB notional to potential HY migration."
    steps:
      - compute_share:
          numerator: "IG_BBB_market_value"
          denominator: "IG_total_market_value"
          label: "BBB Share of IG (%)"
      - adjust_by_quality:
          base: "IG_BBB_market_value"
          factor: "BBB_leverage_gt_4x_share"
          label: "BBB at Risk (USD)"
  visualization:
    chart_type: "bars_dual_axis"
    axes:
      primary_axis: "right"
      y_right: {label: "USD (trillions)"}
      y_left: {label: "% of IG"}
    series:
      - key: "BBB at Risk (USD)"
        axis: "right"
        color: "#FF4500"
      - key: "BBB Share of IG (%)"
        axis: "left"
        color: "#0077BE"
    legend: {position: "top_left"}
    value_tags:
      enabled: true
      rounded_rect: true
      font_color: "#FFFFFF"
      drop_shadow: true
  style:
    background: "#FFFFFF"
    spines: {top: true, right: true, bottom: true, left: true}
  export:
    aspect_ratio: "16:9"
    data_region_ratio: "12:7"
    border: {size_in: 0.25, color: "#0077BE"}
    watermark:
      header: {text: "LIGHTHOUSE MACRO", color: "#0077BE", position: "top-left", small_caps: true}
      footer: {text: "MACRO, ILLUMINATED.", color: "#0077BE", position: "bottom-right", outside_axes: true}
    footer_note: "Source: Bloomberg, BIS | Calc: Market value × leverage share."
  refresh: {schedule: "monthly", lag_days: 5}
  audit: {script_path: "charts/credit/bbb_to_hy_threshold_exposure.py", version: "2.2"}
  last_updated: "2025-10-28"
```

[[CHART: Credit_Spread_Convexity_Index]]

```yaml
chart:
  id: Credit_Spread_Convexity_Index
  title: "When Passive Flows Bite"
  subtitle: "HY OAS volatility ÷ ETF volume beta"
  tags: ["credit", "etf", "convexity", "volatility"]
  frequency: "weekly"
  region: "United States"
  units: "z-score"
  sources:
    - name: "ICE/BofA via FRED"
      series: ["BAMLH0A0HYM2"]
    - name: "Bloomberg"
      series: ["HYG_volume","JNK_volume","HY_OAS_vol_20d","ETF_volume_beta"]
  data:
    series:
      - id: "HY_OAS_vol_20d"
      - id: "ETF_volume_beta"
  calc:
    description: "Convexity Index = HY OAS vol / ETF volume beta; z-scored."
    steps:
      - ratio:
          numerator: "HY_OAS_vol_20d"
          denominator: "ETF_volume_beta"
          label: "Spread Convexity"
      - zscore:
          lookback_years: 10
  visualization:
    chart_type: "line"
    axes:
      primary_axis: "right"
      y: {label: "z-score"}
      x: {label: "Date"}
    series:
      - key: "Spread Convexity (z)"
        color: "#FF00FF"
        linewidth: 3
    thresholds:
      - y: 1.0
        label: "Amplification risk"
        color: "#FF4500"
  style:
    background: "#FFFFFF"
    spines: {top: true, right: true, bottom: true, left: true}
  export:
    aspect_ratio: "16:9"
    data_region_ratio: "12:7"
    border: {size_in: 0.25, color: "#0077BE"}
    watermark:
      header: {text: "LIGHTHOUSE MACRO", color: "#0077BE", position: "top-left", small_caps: true}
      footer: {text: "MACRO, ILLUMINATED.", color: "#0077BE", position: "bottom-right", outside_axes: true}
    footer_note: "Source: ICE/BofA, Bloomberg | Calc: OAS vol ÷ ETF beta, z-scored."
  refresh: {schedule: "weekly", lag_days: 2}
  audit: {script_path: "charts/credit/credit_spread_convexity_index.py", version: "2.2"}
  last_updated: "2025-10-28"
```

---

## III. Fiscal–Liquidity Backdrop: The Vanishing Buffer

The liquidity buffer that once insulated risk is depleted. The ON RRP facility has been drawn down while net Treasury issuance expands. Dealers intermediate, but balance sheet capacity is finite. When supply meets constraints, stress does not require a crisis trigger—duration and collateral mismatches suffice.

Funding dynamics now act as a transmission accelerant. Cross‑currency basis, repo dispersion, and policy‑rate spread behavior register the system’s tension long before a headline.

[[CHART: RRP_and_Reserves_Trend]]

```yaml
chart:
  id: RRP_and_Reserves_Trend
  title: "The Fading Cushion"
  subtitle: "ON RRP and reserve balances as % of GDP"
  tags: ["liquidity", "RRP", "reserves", "GDP"]
  frequency: "weekly"
  region: "United States"
  units: "% of GDP"
  sources:
    - name: "Federal Reserve H.4.1 / SOMA"
      series: ["RRPONTSYD","RESBALNS"]
    - name: "BEA"
      series: ["GDP"]
  data:
    series:
      - id: "RRPONTSYD"
        transform:
          - weekly_to_monthly: {method: "avg"}
      - id: "RESBALNS"
        transform:
          - weekly_to_monthly: {method: "avg"}
      - id: "GDP"
        transform:
          - interpolate_monthly: {}
  calc:
    description: "Scale ON RRP and reserve balances by nominal GDP."
    steps:
      - ratio_to_gdp:
          fields: ["RRPONTSYD","RESBALNS"]
          gdp: "GDP"
          scale: 100
  visualization:
    chart_type: "line_dual_axis"
    axes:
      primary_axis: "right"
      y_right: {label: "Reserves, % of GDP"}
      y_left: {label: "ON RRP, % of GDP"}
    series:
      - key: "Reserves to GDP"
        axis: "right"
        color: "#0077BE"
        linewidth: 3
      - key: "ON RRP to GDP"
        axis: "left"
        color: "#FF4500"
        linewidth: 3
    legend: {position: "top_left"}
  style:
    background: "#FFFFFF"
    spines: {top: true, right: true, bottom: true, left: true}
  export:
    aspect_ratio: "16:9"
    data_region_ratio: "12:7"
    border: {size_in: 0.25, color: "#0077BE"}
    watermark:
      header: {text: "LIGHTHOUSE MACRO", color: "#0077BE", position: "top-left", small_caps: true}
      footer: {text: "MACRO, ILLUMINATED.", color: "#0077BE", position: "bottom-right", outside_axes: true}
    footer_note: "Source: Federal Reserve H.4.1, BEA | Calc: Weekly to monthly, % of GDP."
  refresh: {schedule: "weekly", lag_days: 5}
  audit: {script_path: "charts/liquidity/rrp_and_reserves_trend.py", version: "2.2"}
  last_updated: "2025-10-28"
```

[[CHART: Dealer_Leverage_vs_Repo_Spread]]

```yaml
chart:
  id: Dealer_Leverage_vs_Repo_Spread
  title: "The Thin Dealer Buffer"
  subtitle: "Dealer net repo exposure vs GCF repo spread"
  tags: ["funding", "dealers", "repo", "leverage"]
  frequency: "weekly"
  region: "United States"
  units: "ratio, bps"
  sources:
    - name: "FRBNY Primary Dealer Statistics"
      series: ["dealer_net_repo","dealer_capital"]
    - name: "DTCC GCF Repo Index"
      series: ["GCF_repo_spread"]
  data:
    series:
      - id: "dealer_net_repo"
      - id: "dealer_capital"
      - id: "GCF_repo_spread"
  calc:
    description: "Dealer net repo exposure to capital ratio vs GCF repo spread."
    steps:
      - ratio:
          numerator: "dealer_net_repo"
          denominator: "dealer_capital"
          label: "Dealer Leverage (repo/capital)"
  visualization:
    chart_type: "line_dual_axis"
    axes:
      primary_axis: "right"
      y_right: {label: "Dealer Leverage (x)"}
      y_left: {label: "GCF Repo Spread (bps)"}
    series:
      - key: "Dealer Leverage (x)"
        axis: "right"
        color: "#0077BE"
        linewidth: 3
      - key: "GCF Repo Spread (bps)"
        axis: "left"
        color: "#FF4500"
        linewidth: 3
    legend: {position: "top_left", show: true}
  style:
    background: "#FFFFFF"
    spines: {top: true, right: true, bottom: true, left: true}
  export:
    aspect_ratio: "16:9"
    data_region_ratio: "12:7"
    border: {size_in: 0.25, color: "#0077BE"}
    watermark:
      header: {text: "LIGHTHOUSE MACRO", color: "#0077BE", position: "top-left", small_caps: true}
      footer: {text: "MACRO, ILLUMINATED.", color: "#0077BE", position: "bottom-right", outside_axes: true}
    footer_note: "Source: FRBNY, DTCC | Calc: Repo exposure/capital vs GCF spread."
  refresh: {schedule: "weekly", lag_days: 7}
  audit: {script_path: "charts/liquidity/dealer_leverage_vs_repo_spread.py", version: "2.2"}
  last_updated: "2025-10-28"
```

[[CHART: Funding_Stress_Thermometer]]

```yaml
chart:
  id: Funding_Stress_Thermometer
  title: "Funding Stress Thermometer"
  subtitle: "SOFR–FF, xccy basis, repo dispersion (PCA)"
  tags: ["funding", "xccy", "repo", "stress"]
  frequency: "daily"
  region: "United States"
  units: "percentile"
  sources:
    - name: "Federal Reserve / Bloomberg / BIS"
      series: ["SOFR","EFFR","XCCY_basis_3m","repo_rate_dispersion"]
  data:
    series:
      - id: "SOFR"
      - id: "EFFR"
      - id: "XCCY_basis_3m"
      - id: "repo_rate_dispersion"
  calc:
    description: "PCA-weighted index of short-term funding stresses, scaled to percentiles."
    steps:
      - compute_spread:
          numerator: "SOFR"
          denominator: "EFFR"
          op: "minus"
          label: "SOFR–FF Spread"
      - pca:
          fields: ["SOFR–FF Spread","XCCY_basis_3m","repo_rate_dispersion"]
          components: 1
          label: "Funding Stress PCA"
      - to_percentile:
          field: "Funding Stress PCA"
          horizon_years: 15
  visualization:
    chart_type: "line"
    axes:
      primary_axis: "right"
      y: {label: "Percentile (0–100)"}
      x: {label: "Date"}
    series:
      - key: "Funding Stress Thermometer"
        color: "#FF4500"
        linewidth: 3
    thresholds:
      - y: 80
        label: "Alert"
        color: "#FF4500"
      - y: 50
        label: "Watch"
        color: "#A9A9A9"
  style:
    background: "#FFFFFF"
    spines: {top: true, right: true, bottom: true, left: true}
  export:
    aspect_ratio: "16:9"
    data_region_ratio: "12:7"
    border: {size_in: 0.25, color: "#0077BE"}
    watermark:
      header: {text: "LIGHTHOUSE MACRO", color: "#0077BE", position: "top-left", small_caps: true}
      footer: {text: "MACRO, ILLUMINATED.", color: "#0077BE", position: "bottom-right", outside_axes: true}
    footer_note: "Source: Fed, BIS, Bloomberg | Calc: PCA of funding indicators mapped to percentiles."
  refresh: {schedule: "daily", lag_days: 1}
  audit: {script_path: "dashboards/liquidity/funding_stress_thermometer.py", version: "2.2"}
  last_updated: "2025-10-28"
```

---

## IV. Cross‑Asset Implications: The Mirage of Stability

Valuations rest on a generous assumption: earnings and spreads will glide, not gap. History rarely offers that courtesy. With real rates sticky and risk premia compressed, any credit repricing transmits quickly to duration‑sensitive assets. Equities don’t need a collapse in earnings to de‑rate; they just need the discount rate to stop playing nice while the margin of safety thins. Commodities remain tethered to fiscal pulse and supply constraints but show weaker follow‑through when liquidity cushions shrink.

The narrative risk is semantic. The market will call it “sudden.” The data calls it inevitable. Transition shocks masquerade as events; they’re actually the bill for prior stability.

**Tactical read‑through:**

- **Equities:** Favor high‑quality balance sheets with cash conversion discipline; fade multiple expansion where credit beta is embedded in narratives.  
- **Credit:** Reduce exposure to lower‑quality HY; upgrade within IG and trim BBBs near leverage cliffs. Maintain dry powder for spread convexity spikes.  
- **Rates:** Duration is the hedge of last resort, not the hero. Use convexity via intermediate tenors and roll‑down where curve normalization begins but is incomplete.  
- **FX & Basis:** Watch x‑ccy basis widening as an early funding‑pressure tell. Dollar strength can coexist with slower growth when global liquidity tightens.  
- **Gold & Defensives:** Maintain a core allocation as a funding‑stress hedge and policy‑response option value, not as a pure inflation bet.

---

## V. Base Case, Shock Case, Invalidation

**Base Case (60%)**  
A drawn‑out transition: slow labor decay, gradual credit widening, modest equity de‑rating. Real yields remain sticky; policy eases only after slack becomes visible in flow data. Growth flirts with contraction without falling into it. The system “rots in place.”

**Shock Case (40%)**  
Liquidity fracture intersects with labor retrenchment. Funding stress spikes; downgrades cascade; equities overshoot. Duration and gold outperform as cross‑asset volatility surges; HY ETFs gap wider than index due to flow convexity.

[[CHART: Transition_Tracker_Composite]]

```yaml
chart:
  id: Transition_Tracker_Composite
  title: "Transition Tracker"
  subtitle: "Labor fragility + credit lag + liquidity stress"
  tags: ["composite", "late-cycle", "risk"]
  frequency: "monthly"
  region: "United States"
  units: "z-score"
  sources:
    - name: "Lighthouse Macro"
      series: ["Labor_Fragility_z","Credit_Labor_Lag_Spread_z","Funding_Stress_percentile"]
  data:
    series:
      - id: "Labor_Fragility_z"
      - id: "Credit_Labor_Lag_Spread_z"
      - id: "Funding_Stress_percentile"
        transform:
          - map_percentile_to_z: {}
  calc:
    description: "Weighted composite: 0.4 labor, 0.35 credit, 0.25 liquidity."
    steps:
      - weighted_sum:
          weights:
            Labor_Fragility_z: 0.40
            Credit_Labor_Lag_Spread_z: 0.35
            Funding_Stress_percentile_z: 0.25
          label: "Transition Tracker (z)"
  visualization:
    chart_type: "line"
    axes:
      primary_axis: "right"
      y: {label: "Composite z-score"}
      x: {label: "Date"}
    series:
      - key: "Transition Tracker (z)"
        color: "#0077BE"
        linewidth: 3
    thresholds:
      - y: 1.0
        label: "Turning point"
        color: "#FF4500"
      - y: 0.0
        label: "Neutral"
        color: "#A9A9A9"
    value_tags:
      enabled: true
      rounded_rect: true
      font_color: "#FFFFFF"
      drop_shadow: true
  style:
    background: "#FFFFFF"
    spines: {top: true, right: true, bottom: true, left: true}
  export:
    aspect_ratio: "16:9"
    data_region_ratio: "12:7"
    border: {size_in: 0.25, color: "#0077BE"}
    watermark:
      header: {text: "LIGHTHOUSE MACRO", color: "#0077BE", position: "top-left", small_caps: true}
      footer: {text: "MACRO, ILLUMINATED.", color: "#0077BE", position: "bottom-right", outside_axes: true}
    footer_note: "Source: Lighthouse Macro | Calc: Weighted composite (labor, credit, liquidity)."
  refresh: {schedule: "monthly", lag_days: 7}
  audit: {script_path: "dashboards/composite/transition_tracker_composite.py", version: "2.2"}
  last_updated: "2025-10-28"
```

**Invalidation Threshold**  
A convincing upturn in labor dynamism (quits plus job‑finding) with real wage growth above **1.5% YoY** would undercut the transition thesis. Pair that with a fall in the Funding Stress Thermometer below the median and a narrowing of the Credit–Labor Lag Spread into negative territory, and the regime would shift back toward benign carry.

---

## VI. Positioning Playbook

This is the “how” behind the narrative—tactical, risk‑aware, and flexible.

1. **Credit:**  
   - **Reduce HY beta**, especially names with refinancing needs within 12–18 months.  
   - **Overweight upper‑IG** and stressed rising stars with clear catalysts; avoid BBBs sitting near leverage thresholds.  
   - **Optionality:** Keep capital for convex widening—spreads don’t need to blow out for the math to work if recovery assumptions compress.

2. **Equities:**  
   - **Quality and cash conversion** over sales‑beta. Favor firms that compound free cash flow and can self‑fund.  
   - **Avoid narrative carry:** Valuations embedding credit beta (subscription models with thin margins, capex narratives with bond‑like funding needs).  
   - **Factor tilt:** Defensives with pricing power, low earnings variability, and modest supply‑chain intensity.

3. **Rates:**  
   - **Intermediate duration** for convexity without full long‑end volatility.  
   - **Roll‑down capture** where curve begins to re‑normalize; add payers against front‑end cuts priced too early if labor continues to erode slowly.  

4. **Macro Hedges:**  
   - **Gold and quality duration** as stress hedges; **long USD** vs cyclicals where x‑ccy basis widens.  
   - **Vol overlays** targeted at credit ETFs for event‑convexity without running outright short risk.

5. **Risk Management:**  
   - **Trigger discipline:** Elevations above 80th percentile on the Funding Stress Thermometer or a +1σ break in the Transition Tracker flips the book more defensive.  
   - **Stop‑in logic:** If Labor Dynamism Index breaks back above zero with quits outpacing layoffs and real wages >1.5% YoY, progressively remove hedges.

---

## VII. Appendix Charts (Foundations)

To complete the 15‑chart set, we include the headline/flow labor diagnostics, composites, and funding structure charts that anchor the transition thesis.

1. (Already listed) **Headline vs Flow: Payrolls vs Quits**  
2. (Already listed) **Hours vs Employment**  
3. (Already listed) **Employment Duration Skew**  
4. (Already listed) **Wage Risk Ratio**  
5. (Already listed) **Labor Fragility Dashboard**  
6. (Already listed) **Labor Dynamism Index**  
7. (Already listed) **Credit–Labor Lag Spread**  
8. (Already listed) **Transition Heatmap**  
9. (Already listed) **HY Spread vs Default Probability**  
10. (Already listed) **BBB to HY Threshold Exposure**  
11. (Already listed) **Credit Spread Convexity Index**  
12. (Already listed) **RRP & Reserves Trend**  
13. (Already listed) **Dealer Leverage vs Repo Spread**  
14. (Already listed) **Funding Stress Thermometer**  
15. (Already listed) **Transition Tracker Composite**  

Each chart adheres to Lighthouse standards: no gridlines, all spines visible, white background; Ocean Blue header watermark and border, Slate text; right axis is primary; 16:9 display with a 12:7 data region; value tags are color‑matched rounded rectangles with white text and subtle shadow; and every export includes a source‑calc footer note for reproducibility.

---

## VIII. Conclusion: Seeing Through the Plateau

Our job is to recognize when stillness is not balance but latency. The labor market’s behavior tells you the story: mobility is fading, wages are losing impulse, and fragility is rising in the corners. Credit has not fully priced that reality. Liquidity no longer cushions the miss.

The market calls it resilience.  
The data calls it fatigue.  

The transition—not the collapse—is the story. Navigate the plateau before the slope.

---

*That’s our view from the Watch. We’ll keep the light on.*
