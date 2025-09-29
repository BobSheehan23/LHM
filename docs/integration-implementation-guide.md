# Repository Integration Implementation Guide

This document provides step-by-step instructions for consolidating selected repositories into the LHM monorepo.

## Phase 1: High-Priority Integrations

### Prerequisites
1. Backup current LHM repository
2. Verify git remotes and branch structure
3. Ensure clean working directory

### 1. Integrate Daily_Digest (72 KB)

```bash
# Add as git subtree
cd /path/to/LHM
git subtree add --prefix=notebooks/daily_digest https://github.com/BobSheehan23/Daily_Digest.git main --squash

# Alternative: Manual integration
git clone https://github.com/BobSheehan23/Daily_Digest.git /tmp/daily_digest
cp -r /tmp/daily_digest/* notebooks/daily_digest/
rm -rf /tmp/daily_digest
```

### 2. Integrate fred-mcp-server (1.03 MB)

```bash
# Create structure
mkdir -p src/data_clients/fred_mcp

# Add as subtree
git subtree add --prefix=src/data_clients/fred_mcp https://github.com/BobSheehan23/fred-mcp-server.git main --squash

# Update imports and paths as needed
find src/data_clients/fred_mcp -name "*.ts" -o -name "*.js" | xargs sed -i 's/import from "\.\//import from "src\/data_clients\/fred_mcp\//g'
```

### 3. Integrate sec-edgar-mcp (277 KB)

```bash
mkdir -p src/data_clients/sec_edgar_mcp
git subtree add --prefix=src/data_clients/sec_edgar_mcp https://github.com/BobSheehan23/sec-edgar-mcp.git main --squash
```

### 4. Integrate mcp_polygon (135 KB)

```bash
mkdir -p src/data_clients/polygon_mcp  
git subtree add --prefix=src/data_clients/polygon_mcp https://github.com/BobSheehan23/mcp_polygon.git main --squash
```

## Phase 2: Dependency Management

### Create Unified Requirements

Create `requirements.txt`:
```txt
# Data processing
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0

# API clients
requests>=2.31.0
python-dotenv>=1.0.0

# FRED data
fredapi>=0.5.0

# SEC data  
sec-api>=1.0.0

# Polygon data
polygon-api-client>=1.0.0

# Jupyter
jupyter>=1.0.0
ipykernel>=6.0.0
```

Create `package.json` for Node.js dependencies:
```json
{
  "name": "lhm-monorepo",
  "version": "1.0.0",
  "description": "Lighthouse Macro monorepo",
  "scripts": {
    "build": "tsc",
    "test": "jest",
    "start": "node dist/index.js"
  },
  "dependencies": {
    "@anthropic-ai/claude": "^1.0.0",
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0"
  }
}
```

### Update .gitignore

```gitignore
# Existing entries
__pycache__/
*.py[cod]
.Python
build/
dist/

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Data clients
src/data_clients/*/node_modules/
src/data_clients/*/.env
src/data_clients/*/dist/

# API Keys
.env
*.key
secrets/
```

## Phase 3: Configuration Consolidation

### Create Data Source Configurations

Create `configs/data_sources/fred.yaml`:
```yaml
fred:
  base_url: "https://api.stlouisfed.org/fred"
  api_key_env: "FRED_API_KEY"
  default_params:
    file_type: "json"
    realtime_start: "1776-07-04"
    realtime_end: "9999-12-31"
  
series_groups:
  inflation:
    - "CPIAUCSL"  # CPI All Urban
    - "CPILFESL"  # Core CPI
    - "PCETRIM12M159SFRBDAL"  # Trimmed Mean PCE
  employment:
    - "UNRATE"    # Unemployment Rate  
    - "PAYEMS"    # Nonfarm Payrolls
    - "CIVPART"   # Participation Rate
```

Create `configs/data_sources/sec_edgar.yaml`:
```yaml
sec_edgar:
  base_url: "https://www.sec.gov/Archives/edgar/data"
  user_agent: "LighthouseMacro research@lighthousemacro.com"
  rate_limit: 
    requests_per_second: 10
    max_retries: 3
  
forms:
  "13F":
    endpoints:
      search: "/cgi-bin/browse-edgar"
      filing: "/Archives/edgar/data"
    required_fields:
      - "cik"
      - "form_type"  
      - "date_filed"
```

### Create Analysis Configurations  

Create `configs/analysis/charting.yaml`:
```yaml
charting:
  style:
    figure_size: [12, 8]
    line_width: 3
    colors:
      primary: "#1f77b4"    # Ocean Blue
      secondary: "#ff7f0e"  # Deep Sunset Orange  
      tertiary: "#17becf"   # Neon Carolina Blue
      quaternary: "#e377c2" # Neon Magenta
      neutral: "#7f7f7f"    # Medium-Light Gray
  
  layout:
    spines: 
      top: true
      bottom: true
      left: true  
      right: true
    grid: false
    watermark:
      text: "LHM"
      position: "bottom-right"
      alpha: 0.3
  
  axes:
    primary: "right"
    zero_aligned: true
    independent_scaling: true
```

## Phase 4: Testing Integration

### Create Test Structure

```bash
mkdir -p tests/unit/data_clients
mkdir -p tests/integration
mkdir -p tests/notebooks
```

Create `tests/unit/data_clients/test_fred_mcp.py`:
```python
import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../src'))

from data_clients.fred_mcp import FredMCPClient

class TestFredMCPClient:
    def test_client_initialization(self):
        """Test FRED MCP client can be initialized."""
        client = FredMCPClient()
        assert client is not None
    
    def test_series_request(self):
        """Test basic series data request."""
        # Mock API response for testing
        pass
```

### Create Integration Tests

Create `tests/integration/test_data_pipeline.py`:
```python
import pytest
from src.data_clients.fred_mcp import FredMCPClient
from src.analysis.sec_13f import SEC13FAnalyzer

class TestDataPipeline:
    def test_fred_to_analysis_pipeline(self):
        """Test data flows from FRED client to analysis."""
        # Integration test with mocked data
        pass
```

## Phase 5: Documentation Updates

### Update Main README

Add sections for:
- Data client usage
- Configuration management  
- Development setup
- API documentation

### Create Module Documentation

```bash
mkdir -p docs/api
mkdir -p docs/tutorials
mkdir -p docs/examples
```

## Phase 6: CI/CD Updates

### Update GitHub Actions

Create `.github/workflows/test.yml`:
```yaml
name: Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
        node-version: [18, 20]

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Set up Node.js  
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
    
    - name: Install Python dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Install Node.js dependencies
      run: |
        npm install
    
    - name: Run Python tests
      run: |
        pytest tests/ -v
    
    - name: Run Node.js tests
      run: |
        npm test
    
    - name: Run integration tests
      run: |
        pytest tests/integration/ -v
```

## Maintenance and Updates

### Keeping Integrated Repos Updated

```bash
# Update subtree from upstream
git subtree pull --prefix=src/data_clients/fred_mcp https://github.com/BobSheehan23/fred-mcp-server.git main --squash

# Or use git submodules for easier updates
git submodule add https://github.com/BobSheehan23/fred-mcp-server.git src/data_clients/fred_mcp
git submodule update --remote
```

### Regular Maintenance Tasks

1. **Weekly:** Update dependencies
2. **Monthly:** Sync with upstream repositories  
3. **Quarterly:** Review and optimize structure
4. **Annually:** Evaluate consolidation success