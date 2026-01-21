# Lighthouse Macro — Setup Guide

Complete setup instructions for the Lighthouse Macro Intelligence Pipeline.

---

## Prerequisites

- **Python 3.11+** (Check: `python3 --version`)
- **pip** package manager
- **Git** (for version control)

---

## Installation

### 1. Navigate to Project Directory

```bash
cd ~/lighthouse-macro
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -e .
```

For development tools (Jupyter, testing, linting):

```bash
pip install -e ".[dev]"
```

### 4. Install Playwright (for web scraping)

```bash
playwright install
```

---

## Configuration

### API Keys

Edit `configs/secrets.env` with your API keys:

```bash
# Already configured
FRED_API_KEY=7f8e44038ee69c4f78cf71873e85db16

# Add these
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Optional (for publishing)
SUBSTACK_API_KEY=your_key_here
TWITTER_API_KEY=your_key_here
TWITTER_API_SECRET=your_secret_here
TWITTER_ACCESS_TOKEN=your_token_here
TWITTER_ACCESS_SECRET=your_secret_here
```

### Get API Keys

**FRED (Federal Reserve Economic Data)**
- Already configured: `7f8e44038ee69c4f78cf71873e85db16`
- Or get your own at: https://fred.stlouisfed.org/docs/api/api_key.html

**Anthropic (Claude)**
- Sign up at: https://console.anthropic.com/
- Get API key from: Settings → API Keys

**OpenAI (GPT)**
- Sign up at: https://platform.openai.com/
- Get API key from: API Keys section

---

## Verify Installation

Check system status:

```bash
python cli.py status
```

You should see:
```
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Component          ┃ Status       ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ FRED API           │ ✓ Configured │
│ Anthropic (Claude) │ ✓ Configured │
│ OpenAI (GPT)       │ ✓ Configured │
│ Substack           │ ✗ Missing    │
│ Twitter            │ ✗ Missing    │
└────────────────────┴──────────────┘
```

---

## Quick Start

### 1. Collect Data

Collect all Macro Dynamics data:

```bash
python cli.py collect fred --pillar macro_dynamics
```

Collect specific series:

```bash
python cli.py collect fred --series GDP
python cli.py collect fred --series UNRATE
```

Collect with date range:

```bash
python cli.py collect fred --pillar monetary_mechanics --start-date 2020-01-01
```

### 2. Create Charts

Generate LHM-standard chart:

```bash
python cli.py chart create GDP --output gdp_chart.png
```

With custom title:

```bash
python cli.py chart create UNRATE --title "US Unemployment Rate" --output unemployment.png
```

### 3. Run Research Workflows

Generate Beam content:

```bash
python cli.py research beam GDP
```

Generate Beacon article (interactive):

```bash
python cli.py research beacon
```

---

## Directory Structure

```
lighthouse-macro/
├── data/
│   ├── raw/           # Original collected data (timestamped)
│   ├── processed/     # Transformed data (by pillar)
│   └── cache/         # AI response cache
├── src/
│   ├── collectors/    # Data collection modules
│   ├── transformers/  # Data transformation engine
│   ├── ai/           # AI orchestration
│   ├── charting/     # Chart generation
│   └── core/         # Configuration & utilities
├── notebooks/        # Jupyter notebooks for analysis
├── configs/          # Configuration files
├── scripts/          # Automation scripts
├── docs/            # Documentation
└── cli.py           # Main CLI interface
```

---

## Data Flow

1. **Collection** → Raw data saved to `data/raw/{source}/`
2. **Transformation** → Processed data saved to `data/processed/{pillar}/`
3. **Analysis** → Charts, insights, content generation
4. **Publishing** → Substack, Twitter, etc.

---

## Configuration Files

### `configs/series.yaml`
- Defines data series organized by Three Pillars
- Add custom series here

### `configs/charting.yaml`
- LHM visual standards (colors, fonts, watermarks)
- Modify for custom styling

### `configs/ai_routing.yaml`
- AI model routing logic (Claude vs GPT)
- Task-specific settings
- Workflow definitions

---

## Troubleshooting

**Import Errors**
```bash
# Ensure you're in virtual environment
source venv/bin/activate

# Reinstall
pip install -e .
```

**FRED API Errors**
```bash
# Test API key
python -c "from src.collectors import FREDCollector; c = FREDCollector(); print('✓ FRED working')"
```

**Missing Data**
```bash
# Check if data exists
ls data/raw/fred/

# Re-collect if needed
python cli.py collect fred --series GDP
```

---

## Next Steps

1. **Configure AI Keys** → Add Anthropic/OpenAI keys to `configs/secrets.env`
2. **Collect Data** → Run `python scripts/collect.py` for full data pull
3. **Explore Notebooks** → Open Jupyter in `notebooks/` directory
4. **Customize Series** → Edit `configs/series.yaml` for your needs
5. **Automate** → Set up cron jobs or schedulers (see `docs/AUTOMATION.md`)

---

## Support

**Documentation**: `docs/` directory
**Issues**: File issues with specific error messages
**Configuration**: Check `configs/` files for settings

---

**LIGHTHOUSE MACRO**
MACRO, ILLUMINATED.
