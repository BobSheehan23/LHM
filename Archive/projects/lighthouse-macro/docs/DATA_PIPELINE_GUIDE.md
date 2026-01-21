# Data Pipeline Guide
## Universal Data Collection → Transform → Chart

This system lets you pull data from **ANY source** and chart it with perfect LHM standards.

---

## Quick Example

```python
from collectors.universal import DataPipeline
from charting import LHMChart, set_lhm_style

# Initialize
pipeline = DataPipeline()

# Add data from FRED
pipeline.add_series("payrolls", source="FRED", series_id="PAYEMS", start_date="2000-01-01")

# Add data from CSV (Bloomberg export, FactSet download, etc.)
pipeline.add_series("defaults", source="CSV", filepath="moody_edf.csv", date_column="date", value_column="edf_12m")

# Transform
pipeline.transform("payrolls", "yoy_pct", periods=12)
pipeline.transform("defaults", "zscore_rolling", window=120)

# Align (inner join = show full overlap)
pipeline.align(method="inner")

# Chart
data = pipeline.get_chart_data()
chart = LHMChart()
chart.plot_line(data["payrolls"], label="Payrolls YoY%", color="ocean_blue")
chart.plot_line(data["defaults"], label="Default Risk (z)", color="dusk_orange")
chart.set_title("Your Chart Title")
chart.add_watermarks(source="BLS, Moody's")
chart.save("output.png")
```

---

## Supported Data Sources

### 1. FRED (Federal Reserve)
```python
pipeline.add_series(
    name="gdp",
    source="FRED",
    series_id="GDP",
    start_date="1990-01-01"
)
```

### 2. CSV Files (Bloomberg, FactSet, Manual)
```python
pipeline.add_series(
    name="bbg_data",
    source="CSV",
    filepath="/Users/bob/data/bloomberg_export.csv",
    date_column="Date",
    value_column="PX_LAST"
)
```

### 3. Excel Files (Manual Data, Reports)
```python
pipeline.add_series(
    name="factset",
    source="Excel",
    filepath="/Users/bob/data/factset_spreads.xlsx",
    sheet_name="HY Spreads",
    date_column="date",
    value_column="spread_bps"
)
```

### 4. JSON (API Responses, Glassnode)
```python
pipeline.add_series(
    name="bitcoin",
    source="JSON",
    filepath="glassnode_btc.json",
    date_field="t",
    value_field="v"
)
```

### 5. DataFrame (Programmatic, Calculated)
```python
import pandas as pd

# Your custom calc
df = pd.DataFrame({
    'date': pd.date_range('2020-01-01', periods=100, freq='D'),
    'custom_indicator': [...]
})

pipeline.add_series(
    name="custom",
    source="DataFrame",
    df=df,
    date_column="date",
    value_column="custom_indicator"
)
```

### 6. Manual Entry
```python
pipeline.add_series(
    name="rare_data",
    source="Manual",
    dates=["2024-01-01", "2024-02-01", "2024-03-01"],
    values=[100.0, 102.5, 101.8]
)
```

---

## Transformations

Available transforms (from `src/transformers/`):

### Temporal
- `yoy_pct` - Year-over-year % change
- `mom` - Month-over-month change
- `qoq` - Quarter-over-quarter change
- `ma_3m` - 3-month moving average
- `ma_12m` - 12-month moving average
- `index_to_base` - Index to base period (e.g., 2019=100)

### Statistical
- `zscore` - Full-history z-score
- `zscore_rolling` - Rolling window z-score
- `percentile_rank` - Percentile rank (0-100)

### Structural
- `ratio` - Compute ratio of two series
- `spread` - Compute spread (difference)
- `real_rate` - Nominal rate - inflation

Example:
```python
# Transform after adding series
pipeline.transform("gdp", "yoy_pct", periods=4)  # Quarterly data
pipeline.transform("gdp", "zscore_rolling", window=40)  # 10-year z-score
```

---

## Alignment Methods

### Inner Join (Default) - **USE THIS**
Shows **full history where ALL series overlap**.

```python
pipeline.align(method="inner")
```

**Example:**
- Series A: 1990-2025
- Series B: 2000-2025
- Chart shows: **2000-2025 for BOTH**

### Outer Join (Use carefully)
Shows **full history of ALL series**, filling gaps.

```python
pipeline.align(method="outer", fill_method="ffill")
```

Fill methods:
- `"ffill"` - Forward fill
- `"bfill"` - Backward fill
- `"interpolate"` - Linear interpolation
- `None` - Leave NaN (will have gaps)

---

## Chart Explanations

**Always include:**

1. **Thesis**: What are you trying to show?
2. **Data Sources**: Where does each series come from?
3. **Transformations**: What did you do to the data?
4. **Interpretation**: What does the current pattern mean?
5. **Trading Implication**: So what?

See `examples/beacon_chart_example.py` for full template.

---

## Common Patterns

### Pattern 1: Headline vs Flow
```python
pipeline.add_series("headline", source="FRED", series_id="PAYEMS")
pipeline.add_series("flow", source="FRED", series_id="JTSQUR")
pipeline.transform("headline", "yoy_pct", periods=12)
pipeline.transform("headline", "zscore_rolling", window=120)
pipeline.transform("flow", "zscore_rolling", window=36)
pipeline.align(method="inner")
```

### Pattern 2: Dual Axis (Different Units)
```python
data = pipeline.get_chart_data()
chart = LHMChart()
chart.plot_line(data["series1"], label="Series 1", color="ocean_blue", axis="primary")
chart.plot_line(data["series2"], label="Series 2", color="dusk_orange", axis="secondary")
chart.align_axes_at_zero()  # Important for dual axis
```

### Pattern 3: Composite Index
```python
# Add multiple series
pipeline.add_series("indicator1", ...)
pipeline.add_series("indicator2", ...)
pipeline.add_series("indicator3", ...)

# Transform to z-scores
for name in ["indicator1", "indicator2", "indicator3"]:
    pipeline.transform(name, "zscore")

# Align
pipeline.align(method="inner")

# Get data and create composite
data = pipeline.get_chart_data()
composite = 0.4 * data["indicator1"] + 0.35 * data["indicator2"] + 0.25 * data["indicator3"]

# Chart
chart = LHMChart()
chart.plot_line(composite, label="Composite Index", color="ocean_blue")
```

---

## Workflow Checklist

1. ✅ **Add all series** with appropriate start dates
2. ✅ **Transform** each series as needed
3. ✅ **Align** with `method="inner"` (default)
4. ✅ **Verify alignment** with `pipeline.describe()`
5. ✅ **Create chart** with proper labels
6. ✅ **Add source attribution**
7. ✅ **Write explanation** of what it shows

---

## Troubleshooting

### "No data after alignment"
- Check series date ranges: `pipeline.describe()`
- One series might not overlap with others
- Use broader start dates when adding series

### "Wrong series length"
- Did you align? Call `pipeline.align()` before `get_chart_data()`
- Check alignment method (`inner` vs `outer`)

### "Transform fails"
- Some transforms need minimum data (e.g., z-score needs > 2 observations)
- Check input data with `print(pipeline.series[name].head())`

---

## Real-World Example: Moody's EDF Data

You download Moody's 12-month EDF (Expected Default Frequency) as CSV from Bloomberg terminal:

```python
pipeline = DataPipeline()

# FRED data
pipeline.add_series("hy_oas", source="FRED", series_id="BAMLH0A0HYM2", start_date="2000-01-01")

# Bloomberg/Moody's CSV export
pipeline.add_series(
    name="edf_12m",
    source="CSV",
    filepath="/Users/bob/Downloads/moodys_edf_20251028.csv",
    date_column="Date",
    value_column="EDF_12M_Median"
)

# Don't transform EDF (already in %, meaningful levels)
# Align - will show full period where BOTH exist
pipeline.align(method="inner")

# Chart
data = pipeline.get_chart_data()
chart = LHMChart()
chart.plot_line(data["hy_oas"], label="HY OAS (bps)", color="ocean_blue", axis="primary")
chart.plot_line(data["edf_12m"], label="12m Default Probability (%)", color="dusk_orange", axis="secondary")
chart.align_axes_at_zero()
chart.set_title("HY Spread vs Default Probability")
chart.add_watermarks(source="ICE/BofA, Moody's")
chart.save("hy_vs_defaults.png")
```

**Result**: Chart shows relationship between market-implied risk (spreads) and model-implied risk (EDF), using ACTUAL default probability data, not unemployment proxy.

---

**LIGHTHOUSE MACRO**
MACRO, ILLUMINATED.
