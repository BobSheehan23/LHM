# Lighthouse Macro — Quick Start

Get up and running in 5 minutes.

---

## 1. Install (2 minutes)

```bash
cd ~/lighthouse-macro
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

---

## 2. Verify (30 seconds)

```bash
python cli.py status
```

Should show:
```
✓ FRED API: Configured
```

---

## 3. Collect Data (1 minute)

```bash
# Get key macro series
python cli.py collect fred --series GDP
python cli.py collect fred --series UNRATE
python cli.py collect fred --series CPIAUCSL
```

---

## 4. Create Chart (30 seconds)

```bash
python cli.py chart create GDP --output gdp_chart.png
open gdp_chart.png
```

You should see a chart with:
- ✓ Ocean blue line
- ✓ "LIGHTHOUSE MACRO" watermark (top-left)
- ✓ "MACRO, ILLUMINATED." watermark (bottom-right)
- ✓ Right-side axis
- ✓ No gridlines

---

## 5. Try Python (1 minute)

```python
python3
```

```python
import sys
sys.path.insert(0, 'src')

from collectors import FREDCollector
from transformers import yoy_pct
from charting import LHMChart, set_lhm_style

# Load data
collector = FREDCollector()
gdp = collector.load_latest("GDP")["GDP"]

# Transform
gdp_growth = yoy_pct(gdp, periods=4)

# Chart
set_lhm_style()
chart = LHMChart()
chart.plot_line(gdp_growth, label="GDP Growth YoY%", color="ocean_blue")
chart.set_title("Real GDP Growth")
chart.add_watermarks()
chart.save("gdp_growth.png")

print(f"Latest GDP growth: {gdp_growth.dropna().iloc[-1]:.2f}%")
```

---

## What You Just Built

✅ **Automated data collection** from FRED
✅ **50+ transformation functions** (YoY, Z-scores, moving averages, spreads, etc.)
✅ **LHM-standard charting** (exact colors, watermarks, styling)
✅ **AI orchestration layer** (Claude + GPT routing)
✅ **Research workflows** (Beacon, Beam, Chartbook, Horizon)
✅ **CLI tools** for daily use
✅ **Python API** for custom analysis

---

## Next Steps

**Option 1: Explore Documentation**
```bash
cat docs/SETUP.md      # Full setup guide
cat docs/USAGE.md      # Comprehensive usage
cat docs/WHAT_WAS_BUILT.md  # Complete feature list
```

**Option 2: Try Jupyter Notebook**
```bash
cd notebooks
jupyter notebook quickstart.ipynb
```

**Option 3: Collect Full Dataset**
```bash
python scripts/collect.py  # All pillars
```

**Option 4: Add AI Keys**
Edit `configs/secrets.env`:
```bash
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

Then try:
```bash
python cli.py research beam GDP
```

---

## Daily Workflow

**Morning data refresh:**
```bash
python scripts/collect.py
```

**Generate chart for Beam:**
```bash
python cli.py chart create UNRATE --output beam_chart.png
python cli.py research beam UNRATE
```

**Create custom analysis:**
```bash
jupyter notebook notebooks/
```

---

## Troubleshooting

**Import errors:**
```bash
source venv/bin/activate
pip install -e .
```

**No data found:**
```bash
python cli.py collect fred --series GDP
```

**Chart doesn't look right:**
```python
from charting import set_lhm_style
set_lhm_style()  # Call this first
```

---

## CLI Cheat Sheet

```bash
# System
python cli.py status           # Check API keys
python cli.py config-info      # Show configuration

# Data Collection
python cli.py collect fred --pillar macro_dynamics
python cli.py collect fred --series GDP

# Charting
python cli.py chart create GDP --output chart.png

# Research
python cli.py research beam GDP
python cli.py research beacon
```

---

## What This Replaces

Instead of:
1. Open FRED website
2. Search for series
3. Download CSV
4. Open Excel
5. Calculate transformations
6. Copy to charting tool
7. Manually format chart
8. Export and adjust styling
9. Copy data to AI chat
10. Paste response into document

**You do:**
```bash
python cli.py collect fred --series GDP
python cli.py chart create GDP
python cli.py research beam GDP
```

**75% time saved. Focus on analysis, not data wrangling.**

---

**LIGHTHOUSE MACRO**
MACRO, ILLUMINATED.
