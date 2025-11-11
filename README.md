# LHM - Lighthouse Macro Monorepo

[![GitHub](https://img.shields.io/github/license/BobSheehan23/LHM)](LICENSE)

## Overview
LHM is the internal, single source of truth for Lighthouse Macro. This repository contains code, datasets, notebooks, and reusable modules powering reproducible macro research.

## Project Structure

```
LHM/
├── data/               # Data storage (excluded from git)
│   ├── raw/           # Raw, immutable data from external sources
│   ├── external/      # External datasets (FRED, Treasury, etc.)
│   ├── interim/       # Intermediate data transformations
│   └── processed/     # Final, analysis-ready datasets
├── src/               # Reusable Python modules and utilities
├── notebooks/         # Jupyter notebooks for analysis and research
├── charts/            # Exported figures and visualizations
├── reports/           # Draft outputs and research reports
├── configs/           # Configuration files (YAML/JSON)
├── tests/             # Unit and integration tests
└── .github/           # GitHub-specific configurations
    └── copilot-instructions.md  # AI assistant guidelines
```

## Getting Started

### Prerequisites
- Python 3.8+
- Jupyter Lab/Notebook
- Required packages: pandas, numpy, matplotlib, PyYAML
- Optional for Parquet export: `pyarrow` or `fastparquet`

### Installation
```bash
git clone https://github.com/BobSheehan23/LHM.git
cd LHM
pip install -r requirements.txt  # When available
```

## Data Sources
Common data sources include:
- **FRED**: Federal Reserve Economic Data
- **Treasury Direct**: US Treasury data
- **OFR**: Office of Financial Research
- **TIC**: Treasury International Capital
- **NY Fed**: New York Federal Reserve

## Coding Standards
- Use type hints and docstrings
- Set random seeds for reproducibility
- Store credentials in environment variables
- Keep functions small and pure
- Use relative paths in notebooks

## Charting Guidelines
- No gridlines, all spines visible
- Right axis primary for single series
- Color palette: Ocean Blue, Deep Sunset Orange, Neon Carolina Blue, Neon Magenta, Medium-Light Gray
- Line thickness ~3, watermark "MACRO, ILLUMINATED." bottom-right
- Match axes at zero when appropriate

## Repository Consolidation

**Considering consolidating multiple repositories into LHM?** 

See [`docs/repository-consolidation-analysis.md`](docs/repository-consolidation-analysis.md) for detailed analysis and recommendations on integrating your external repositories into this monorepo structure.

**TL;DR:** Selective consolidation of macro research-specific repositories (FRED MCP, SEC EDGAR MCP, Daily Digest, etc.) is recommended, while keeping generic development tools separate.

## Contributing
This is an internal repository. Follow the established coding standards and ensure all data remains confidential.

## License
Internal use only. All rights reserved.

## FRED Data Platform

The monorepo now ships with an end-to-end ingestion stack capable of
maintaining hundreds of FRED indicators on a rolling basis.

Key entry points:

- `configs/fred_catalog_sources.yaml` – tag-based recipe for generating
  category-specific indicator catalogs directly from FRED.
- `configs/fred_series_catalog.yaml` – materialised catalog consumed by
  the ingestion pipeline. Regenerate with `python -m lhm.catalog.generate`
  after supplying a FRED API key.
- `src/lhm/config/series_catalog.py` – loader utilities for the catalog
  format.
- `src/lhm/clients/fred_client.py` – fully functional HTTP client with
  rate limiting, metadata retrieval, tag search, and observation pulls.
- `src/lhm/pipelines/daily_refresh.py` – orchestrates refresh cycles,
  persists results, and records metadata for each series.
- `src/lhm/storage/filesystem.py` – pluggable storage backend capable of
  writing Parquet, CSV, or JSON datasets to disk.
- `src/lhm/cli.py` – command line interface for triggering the pipeline.
- `src/lhm/catalog/generate.py` – helper CLI for expanding the catalog
  using the tag configuration.

Refer to `docs/fred_data_platform.md` for the detailed architecture and
operational guidance.
