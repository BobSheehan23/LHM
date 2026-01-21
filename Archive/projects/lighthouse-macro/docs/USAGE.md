# Lighthouse Macro — Usage Guide

Comprehensive guide to using the Lighthouse Macro Intelligence Pipeline.

---

## Core Workflows

### Data Collection

**Collect by Pillar**
```bash
# Macro Dynamics (GDP, inflation, employment, etc.)
python cli.py collect fred --pillar macro_dynamics

# Monetary Mechanics (Fed balance sheet, rates, credit)
python cli.py collect fred --pillar monetary_mechanics

# Market Technicals (indices, spreads, flows)
python cli.py collect fred --pillar market_technicals
```

**Collect Specific Series**
```bash
python cli.py collect fred --series GDP
python cli.py collect fred --series CPIAUCSL
python cli.py collect fred --series WALCL
```

**Collect with Date Range**
```bash
# Last 5 years
python cli.py collect fred --pillar macro_dynamics --start-date 2020-01-01

# Specific series since 2015
python cli.py collect fred --series GDP --start-date 2015-01-01
```

**Automated Collection (All Data)**
```bash
cd scripts
python collect.py
```

---

## Data Transformations

Use Python to transform data programmatically:

```python
from src.collectors import FREDCollector
from src.transformers import yoy, zscore_12m, ma_3m

# Load data
collector = FREDCollector()
gdp = collector.load_latest("GDP")["GDP"]

# Apply transformations
gdp_yoy = yoy(gdp)
gdp_zscore = zscore_12m(gdp)
gdp_smooth = ma_3m(gdp)
```

**Available Transformations**

*Temporal:*
- `yoy()`, `yoy_pct()` - Year-over-year
- `mom()`, `mom_pct()` - Month-over-month
- `qoq()`, `qoq_pct()` - Quarter-over-quarter
- `ma_3m()`, `ma_6m()`, `ma_12m()`, `ma_24m()` - Moving averages
- `growth_rate()`, `log_difference()`, `cumulative_sum()`

*Statistical:*
- `zscore()`, `zscore_12m()`, `zscore_24m()` - Z-scores
- `percentile_rank()`, `percentile_rank_rolling()` - Percentiles
- `bollinger_bands()`, `percentile_bands()` - Bands
- `rolling_correlation()`, `rolling_std()`, `rolling_var()`

*Structural:*
- `spread()`, `yield_spread()` - Differences
- `ratio()`, `relative_strength()` - Ratios
- `output_gap()`, `real_rate()` - Economic concepts
- `momentum()`, `deviation_from_mean()` - Momentum indicators

---

## Charting

### Create Standard Charts

**Basic Chart**
```bash
python cli.py chart create GDP --output charts/gdp.png
```

**With Custom Title**
```bash
python cli.py chart create UNRATE --title "US Unemployment Rate" --output unemployment.png
```

### Python Charting

```python
from src.charting import LHMChart, set_lhm_style, COLORS
from src.collectors import FREDCollector

# Set global style
set_lhm_style()

# Load data
collector = FREDCollector()
gdp = collector.load_latest("GDP")

# Create chart
chart = LHMChart(figsize=(12, 7), dpi=300)
chart.plot_line(gdp, label="Real GDP", color="ocean_blue")
chart.set_title("US Real Gross Domestic Product")
chart.set_labels(ylabel="Billions of Dollars")
chart.add_watermarks()
chart.add_hline(y=gdp.mean(), color="dusk_orange", linestyle="--", label="Mean")
chart.add_legend()
chart.tight_layout()
chart.save("gdp_chart.png")
```

**Multiple Series**
```python
chart = LHMChart()
chart.plot_line(dgs10, label="10Y Treasury", color="ocean_blue")
chart.plot_line(dgs2, label="2Y Treasury", color="carolina_blue")
chart.plot_line(spread, label="10Y-2Y Spread", color="dusk_orange")
chart.add_hline(y=0, color="black", linestyle="-", linewidth=1)
chart.set_title("Treasury Yield Curve")
chart.add_watermarks()
chart.add_legend()
chart.save("yield_curve.png")
```

**Color Palette**
```python
COLORS = {
    "ocean_blue": "#0077FF",      # Primary
    "dusk_orange": "#FF4500",     # Contrast
    "carolina_blue": "#00BFFF",   # Highlight
    "neon_magenta": "#FF00FF",    # Structural
    "light_gray": "#D3D3D3",      # Neutral
    "signal_green": "#00FF7F",    # Positive
    "signal_red": "#FF3333",      # Negative
}
```

---

## AI Workflows

### Research Cadence

**The Beacon (Sunday — Long-form)**
```bash
python cli.py research beacon
```

**The Beam (Tuesday/Thursday — Chart + Paragraph)**
```bash
python cli.py research beam GDP
python cli.py research beam UNRATE
```

**The Chartbook (Friday — 50+ Charts)**
```bash
python cli.py research chartbook
```

**The Horizon (First Monday — Forward Outlook)**
```bash
python cli.py research horizon
```

### Python AI Integration

```python
from src.ai import BeaconWorkflow, BeamWorkflow, AIRouter, TaskType

# Generate Beam content
beam = BeamWorkflow()
content = beam.generate(
    series_id="GDP",
    chart_description="Real GDP growth accelerating above trend"
)
print(content)

# Use AI router
router = AIRouter()
config = router.get_model_for_task(TaskType.NARRATIVE_SYNTHESIS)
print(f"Using {config['model']} because: {config['reason']}")
```

**Direct AI Client Usage**
```python
from src.ai import ClaudeClient, OpenAIClient

# Claude for deep analysis
claude = ClaudeClient()
analysis = claude.complete(
    prompt="Analyze the recent shift in Fed policy stance...",
    temperature=0.7
)

# GPT for quick extraction
gpt = OpenAIClient()
summary = gpt.extract_structured(
    prompt="Extract key data points from this FOMC statement: ..."
)
```

---

## Jupyter Notebooks

Start Jupyter:
```bash
cd notebooks
jupyter notebook
```

**Typical Analysis Notebook**
```python
import sys
sys.path.insert(0, '../src')

from collectors import FREDCollector
from transformers import yoy, zscore_12m, ma_12m
from charting import LHMChart, set_lhm_style
import pandas as pd

# Set style
set_lhm_style()

# Collect data
collector = FREDCollector()
gdp = collector.load_latest("GDP")["GDP"]
cpi = collector.load_latest("CPIAUCSL")["CPIAUCSL"]

# Transform
gdp_yoy = yoy(gdp, periods=4)  # Quarterly data
cpi_yoy = yoy(cpi)

# Chart
chart = LHMChart()
chart.plot_line(gdp_yoy, label="GDP YoY", color="ocean_blue")
chart.set_title("Real GDP Growth YoY")
chart.add_watermarks()
chart.tight_layout()
```

---

## Advanced Usage

### Combining Multiple Transformations

```python
from src.transformers import *

# Load series
collector = FREDCollector()
unrate = collector.load_latest("UNRATE")["UNRATE"]

# Chain transformations
unrate_smooth = ma_3m(unrate)
unrate_zscore = zscore_rolling(unrate_smooth, 12)
unrate_deviation = deviation_from_mean(unrate)

# Create composite view
chart = LHMChart(figsize=(14, 8))
ax1 = chart.ax
ax2 = ax1.twinx()

ax1.plot(unrate, label="Unemployment Rate", color=COLORS["ocean_blue"], linewidth=2.5)
ax2.plot(unrate_zscore, label="12m Z-Score", color=COLORS["dusk_orange"], linewidth=2.5)

chart.add_watermarks()
chart.save("unemployment_composite.png")
```

### Custom Workflow

```python
from src.ai.workflows import ResearchWorkflow
from src.ai.router import TaskType

class CustomWorkflow(ResearchWorkflow):
    def generate_insight(self, data_summary: str) -> str:
        prompt = f"""
        Analyze this data for key insights:
        {data_summary}

        Focus on:
        1. Divergences from historical patterns
        2. Cross-asset implications
        3. Forward-looking signals
        """

        return self._execute_stage(TaskType.CHART_ANALYSIS, prompt)

# Use it
workflow = CustomWorkflow()
result = workflow.generate_insight("GDP +3.2%, CPI +3.1%, UNRATE 3.7%")
```

---

## Automation

### Cron Job (macOS/Linux)

Edit crontab:
```bash
crontab -e
```

Add scheduled jobs:
```cron
# Collect data daily at 9 AM
0 9 * * * cd ~/lighthouse-macro && ./venv/bin/python scripts/collect.py

# Generate Beam on Tuesday/Thursday at 10 AM
0 10 * * 2,4 cd ~/lighthouse-macro && ./venv/bin/python cli.py research beam GDP
```

### Python Scheduler

```python
import schedule
import time
from scripts.collect import collect_all_fred

def job():
    print("Running daily data collection...")
    collect_all_fred()

schedule.every().day.at("09:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## Configuration

### Add Custom Series

Edit `configs/series.yaml`:

```yaml
macro_dynamics:
  custom_category:
    - SERIES_ID_1
    - SERIES_ID_2
    - SERIES_ID_3
```

### Customize AI Routing

Edit `configs/ai_routing.yaml`:

```yaml
routing:
  custom_task:
    model: claude-sonnet-4
    provider: anthropic
    reason: "Your reasoning here"
    temperature: 0.5
```

### Modify Chart Styling

Edit `configs/charting.yaml`:

```yaml
colors:
  custom_color: "#HEXCODE"

style:
  line_width: 3.0
  figure_width: 14
```

---

## Tips & Best Practices

1. **Always collect data first** before charting or analysis
2. **Use virtual environment** to avoid dependency conflicts
3. **Check data freshness** with `collector.get_metadata(series_id)`
4. **Cache AI responses** to avoid re-processing (automatic)
5. **Version control configs** to track changes over time
6. **Test transformations** on small date ranges first
7. **Use descriptive filenames** for charts: `{series}_{transformation}_{date}.png`

---

## CLI Reference

```bash
# System
python cli.py status              # Check configuration
python cli.py config-info         # Show detailed config

# Collection
python cli.py collect fred --pillar <pillar>
python cli.py collect fred --series <series_id>

# Charting
python cli.py chart create <series_id> --output <file>

# Research
python cli.py research beacon
python cli.py research beam <series_id>
python cli.py research chartbook
python cli.py research horizon
```

---

**LIGHTHOUSE MACRO**
MACRO, ILLUMINATED.
