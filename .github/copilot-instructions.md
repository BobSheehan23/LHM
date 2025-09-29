# Copilot Instructions — LHM (Source of Truth Monorepo)

## Purpose
LHM is the internal, single source of truth for Lighthouse Macro. It contains code, datasets, notebooks, and reusable modules powering reproducible macro research.

## Operating Mode
- Task-first, agent-style. Concise and technical.
- Never fabricate or approximate data. If inputs are missing, stop and request the exact source (FRED, TreasuryDirect, OFR, TIC, NY Fed, etc.).
- Python by default (pandas, numpy, matplotlib; statsmodels/pyarrow optional).
- Deliver runnable code first; add minimal context after.



## Charting Standards
- No gridlines. All four spines visible. Right axis is primary.
- Color palette: Ocean Blue, Deep Sunset Orange, Neon Carolina Blue, Neon Magenta, Medium-Light Gray.
- Line thickness ~3; longest history available.
- Axes matched at zero; independently scaled (linear/log/stdev ranges) for clarity.
- Labels clear, no overlaps. Watermark "MACRO, ILLUMINATED." bottom-right (never overlap data).

## Project Structure (recommended)
- `/data/` (raw, external, interim, processed) — never commit proprietary client data.
- `/src/` (reusable modules)
- `/notebooks/` (analysis notebooks; keep I/O paths relative)
- `/charts/` (exported figures, auto-watermarked)
- `/reports/` (draft outputs for Lighthouse Macro repo)
- `/configs/` (YAML/JSON configs, credentials via env vars only)
- `/tests/`

##
