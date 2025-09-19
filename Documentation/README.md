# LHM (Lighthouse Macro) - Complete Repository

## Overview
This repository consolidates all macroeconomic analysis, financial modeling, and data science work into a single, organized source of truth. It includes tools for market analysis, economic indicators tracking, daily digest generation, and more.

## Repository Structure

### 📁 EquiLend/
Contains models and analysis tools adapted from EquiLend work, scrubbed for public use with LHM branding:
- **notebooks/**: Daily digest generators and data processing notebooks
- **charts/**: Visualization and charting tools
- **data_analysis/**: Core analysis notebooks for macro and market analysis
- **utils/**: Utility notebooks for data processing (FRED, labor market charts)

### 📁 MacroAnalysis/
Comprehensive macroeconomic analysis notebooks organized by category:
- **us_economy/**: US-focused economic indicators (CPI, GDP, money supply, employment, etc.)
- **eurozone_economy/**: European economic analysis
- **market_analysis/**: Financial market analysis and indicators
- **investment_tools/**: Portfolio management and investment analysis tools

### 📁 DailyDigest/
Automated daily digest generation tools:
- Daily market digest generators
- Data processing scripts
- Templates and reference files

### 📁 Capstone/
BrainStation Data Science Capstone project materials:
- Complete capstone notebooks
- Presentation materials
- Project documentation

### 📁 Utils/
Shared utilities and configuration files:
- Common requirements and setup files
- Shared configuration templates
- Cross-project utilities

## Getting Started

### Prerequisites
- Python 3.8+
- Jupyter Notebook/Lab
- Required packages (see requirements.txt in each folder)

### Installation
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables using `.env.example` as template
4. Open Jupyter and explore the notebooks

## Key Features

### Economic Analysis
- **Federal Reserve Data Integration**: Automated pulling of FRED economic data
- **Real-time Market Analysis**: Live market data processing and visualization
- **Macro Indicator Tracking**: Comprehensive tracking of key economic indicators
- **Cross-market Analysis**: US and European market comparisons

### Financial Modeling
- **Securities Lending Analysis**: Market microstructure and lending rate analysis
- **Portfolio Optimization**: Asset allocation and portfolio management tools
- **Risk Assessment**: Market risk and volatility analysis
- **Quantitative Research**: Statistical analysis and modeling tools

### Automation Tools
- **Daily Digest Generation**: Automated market summary and analysis reports
- **Data Pipeline**: Streamlined data collection and processing
- **Visualization Suite**: Comprehensive charting and visualization tools
- **Reporting Framework**: Automated report generation and distribution

## Data Sources
- Federal Reserve Economic Data (FRED)
- Public financial market data
- Economic indicators from public APIs
- Statistical data from government sources

*Note: All proprietary data has been removed and replaced with public domain equivalents*

## Usage Examples

### Running Daily Analysis
```python
# Example: Generate daily market digest
from DailyDigest.daily_digest_generator import generate_digest
digest = generate_digest(date='2024-01-01')
```

### Macro Analysis
```python
# Example: Analyze CPI trends
from MacroAnalysis.us_economy.CPI_Indicators import analyze_cpi
cpi_analysis = analyze_cpi()
```

## Contributing
This is a personal research repository. For collaboration opportunities, please reach out directly.

## License
This work is for educational and research purposes. Please respect data source terms of use.

## Contact
For questions about this work or collaboration opportunities, please reach out through GitHub.