# Lighthouse Macro Intelligence Pipeline

Institutional-grade, reproducible macro research infrastructure.

**Built for:** Bob Sheehan, CFA, CMT — Founder & CIO, Lighthouse Macro

## Overview

This system automates 75%+ of data collection, processing, and transformation work — allowing focus on analysis and content creation.

### The Three Pillars

1. **Macro Dynamics** — Real economy forces (growth, inflation, employment, housing, trade)
2. **Monetary Mechanics** — Liquidity plumbing (central banks, repos, reserves, funding)
3. **Market Technicals** — Structure meets behavior (positioning, flows, correlations)

## Quick Start

```bash
# Install dependencies
pip install -e .

# Configure API keys
# Edit configs/secrets.env with your keys

# Collect data
lhm collect --pillar macro_dynamics

# Transform data
lhm transform --series GDP --transforms yoy,zscore_12m,ma_3m

# Generate chart
lhm chart GDP --output beacon_chart.png

# Run research workflow
lhm research beacon
```

## Architecture

```
lighthouse-macro/
├── data/           # Raw → Processed → Cache
├── src/            # Core modules
├── notebooks/      # Analysis & exploration
├── configs/        # Configuration & secrets
├── scripts/        # Automation scripts
└── docs/           # Integration guides
```

## Research Cadence

- **Sunday** → The Beacon (long-form narrative)
- **Tuesday/Thursday** → The Beam (chart + paragraph)
- **Friday** → The Chartbook (50+ charts)
- **First Monday** → The Horizon (forward outlook)

## Data Sources

- FRED (Federal Reserve Economic Data)
- TreasuryDirect
- OFR STFM (Office of Financial Research)
- TIC (Treasury International Capital)
- NY Fed (Repos, SOFR)

## Standards

- Code-first, reproducible research
- Never approximate or fabricate data
- Clarity over complexity
- Empirically valid, interpretable, falsifiable

---

**LIGHTHOUSE MACRO**
MACRO, ILLUMINATED.
