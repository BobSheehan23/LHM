# OFR (Office of Financial Research) - Complete Data Sources

## Overview
The OFR provides critical financial market data through multiple platforms:
1. **Short-term Funding Monitor (STFM)** - Money market data
2. **Hedge Fund Monitor (HFM)** - Hedge fund metrics
3. **Financial Stress Index (FSI)** - System-wide stress indicator
4. **Bank Systemic Risk Monitor (BSRM)** - Banking sector risk

## Data Sources & Access

### 1. Short-term Funding Monitor (STFM)
**URL**: https://data.financialresearch.gov/v1
**Status**: API available but many endpoints require authentication (403 errors)

**Available via API**:
- `GET /metadata/mnemonics/` - List all 442 available series ✅ WORKING
- Series include: repo rates, commercial paper, ABCP, etc.

**Manual Download Available**:
- Visit: https://www.financialresearch.gov/short-term-funding-monitor/
- Download CSV exports for:
  - Repo rates (tri-party, DVP, GCF)
  - Commercial paper rates
  - Asset-backed commercial paper
  - Money market fund data

**Key Series Mnemonics** (from API):
```
REPO-TRI_AR_OO-P    - Tri-party repo overnight rate
REPO-DVP_AR_OO-P    - DVP repo overnight rate
REPO-GCF_AR_OO-P    - GCF repo overnight rate
CP-AA_AR_OO-P       - AA commercial paper overnight
CP-A2P2_AR_OO-P     - A2/P2 commercial paper overnight
ABCP-AA_AR_OO-P     - AA asset-backed CP overnight
```

### 2. Hedge Fund Monitor (HFM)
**URL**: https://data.financialresearch.gov/hf/v1
**Status**: API available but requires authentication

**Categories** (CSV format):
- `aum` - Assets Under Management
- `leverage` - Leverage metrics
- `liquidity` - Liquidity metrics
- `performance` - Performance metrics
- `concentration` - Concentration metrics

**Manual Download**:
- Visit: https://www.financialresearch.gov/hedge-fund-monitor/
- Download quarterly reports and data files

### 3. Financial Stress Index (FSI)
**URL**: https://www.financialresearch.gov/financial-stress-index/
**Status**: Manual download only

**What it measures**:
- Credit stress (corporate, sovereign)
- Equity market volatility
- Funding stress
- Safe haven demand
- Real activity stress

**Download**:
- CSV file with daily FSI values
- Components breakdown
- Historical data back to 2000

**Integration**:
- Save to `data/ofr_fsi/fsi_data.csv`
- Use for Chart 40 (Financial Stress Monitor)

### 4. Bank Systemic Risk Monitor (BSRM)
**URL**: https://www.financialresearch.gov/bank-systemic-risk-monitor/
**Status**: Manual download only

**What it measures**:
- Systemic risk contributions by bank
- Network effects
- Contagion risk
- Capital adequacy stress

**Download**:
- Quarterly data releases
- Institution-level risk metrics
- System-wide aggregates

**Integration**:
- Save to `data/ofr_bsrm/`
- Use for banking sector stress analysis

## Local Data Integration Strategy

### Automated (NY Fed API)
✅ Already implemented with local caching:
- SOFR, EFFR, OBFR (daily updates)
- RRP operations (daily)
- SOMA holdings (weekly)
- Primary dealer stats (weekly)

### Manual Downloads (OFR)
📥 Need to set up manual download workflow:

1. **Weekly Downloads**:
   - FSI data (updated daily, download weekly)
   - BSRM data (updated quarterly)

2. **Monthly Downloads**:
   - STFM repo rates (if API fails)
   - HFM hedge fund metrics

3. **Storage Structure**:
```
data/
├── nyfed_cache/          # Auto-cached via API ✅
├── ofr_cache/            # Auto-cached via API (partial) ⚠️
├── ofr_fsi/              # Manual downloads 📥
│   └── fsi_data.csv
├── ofr_bsrm/             # Manual downloads 📥
│   └── bsrm_quarterly.csv
└── ofr_stfm/             # Manual downloads 📥
    ├── repo_rates.csv
    └── commercial_paper.csv
```

## Data Freshness

| Source | Update Frequency | Access Method | Status |
|--------|-----------------|---------------|--------|
| NY Fed SOFR | Daily | API (auto) | ✅ Working |
| NY Fed EFFR | Daily | API (auto) | ✅ Working |
| NY Fed RRP | Daily | API (auto) | ✅ Working |
| OFR STFM Mnemonics | Static | API (auto) | ✅ Working |
| OFR STFM Series Data | Daily | Manual CSV | 📥 Setup needed |
| OFR FSI | Daily | Manual CSV | 📥 Setup needed |
| OFR BSRM | Quarterly | Manual CSV | 📥 Setup needed |
| OFR HFM | Quarterly | Manual CSV | 📥 Setup needed |

## Next Steps

1. **Set up manual download scripts**:
   - `download_ofr_fsi.sh` - Fetch latest FSI data
   - `download_ofr_bsrm.sh` - Fetch latest BSRM data
   - Schedule via cron or manual weekly run

2. **Create OFR data readers**:
   - `ofr_fsi_reader.py` - Parse FSI CSV files
   - `ofr_bsrm_reader.py` - Parse BSRM data
   - `ofr_stfm_reader.py` - Parse STFM manual downloads

3. **Integrate into dashboards**:
   - Add FSI to Money Market Dashboard
   - Create BSRM banking stress dashboard
   - Add STFM repo rates to existing charts

## API Authentication Note

The OFR API appears to require authentication for most endpoints beyond the basic mnemonics list. Options:

1. **Contact OFR** for API key/access
2. **Use manual downloads** from their website (CSV exports)
3. **Web scraping** (last resort, check robots.txt)

**Recommended**: Hybrid approach
- Use API for metadata (works now)
- Download CSV files manually for actual data
- Store locally with timestamped files
- Build readers to parse into DataFrames

## Chart Integration

**Where OFR data will be used**:
- Chart 22: Repo rates (STFM)
- Chart 23: Commercial paper (STFM)
- Chart 40: Financial stress (FSI)
- Chart 41: Banking sector stress (BSRM)
- Chart 42: Hedge fund positioning (HFM)

**Current workarounds**:
- Using FRED repo rates as proxy
- Using credit spreads for stress proxy
- Missing direct hedge fund data

**With OFR data**:
- Direct repo market rates from tri-party dealers
- Comprehensive FSI (superior to custom stress indices)
- Bank systemic risk scores
- Hedge fund leverage and liquidity metrics
