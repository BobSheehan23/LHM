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
- Required packages: pandas, numpy, matplotlib

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
- Line thickness ~3, watermark "LHM" bottom-right
- Match axes at zero when appropriate

## Contributing
This is an internal repository. Follow the established coding standards and ensure all data remains confidential.

## License
Internal use only. All rights reserved.
