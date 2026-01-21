# Lighthouse Macro - Data Infrastructure Summary

## What's Working Now ✅

### NY Fed Markets API (Fully Operational)
**File**: `nyfed_api_reference.py`
**Status**: ✅ Working with 24-hour local caching

**Available Data**:
- **SOFR** (Secured Overnight Financing Rate)
  - Daily rates and volumes
  - Percentile distributions
  - 500+ days of history cached
  - Latest: 3.91% ($3,170B volume)

- **EFFR** (Effective Federal Funds Rate)
  - Daily rates and volumes
  - Percentile distributions
  - Latest: 3.88% ($75B volume)

- **OBFR** (Overnight Bank Funding Rate)
  - Daily rates and volumes
  - Latest: 3.88% ($179B volume)

- **RRP Operations** (Reverse Repo)
  - Daily operations data
  - Submitted and accepted amounts
  - Latest: $2,503B usage
  - 3,194 observations cached

- **Primary Dealer Statistics**
  - 1,539 available timeseries
  - Positioning data
  - Treasury holdings

- **SOMA Holdings**
  - System Open Market Account summary
  - Treasury holdings breakdown
  - 1,168 rows of holdings data

**Cache Location**: `data/nyfed_cache/`
**Update**: Automatic via API calls (24hr cache expiry)

---

### OFR API - Partial Access ⚠️

**File**: `ofr_api_reference.py`
**Status**: ⚠️ Limited - Most endpoints return 403 Forbidden

**What Works**:
- ✅ Metadata endpoint: List of 442 available series mnemonics
- ✅ Supports both STFM and HFM API types
- ✅ Local caching infrastructure ready

**What Doesn't Work** (403 Forbidden):
- ❌ Series data endpoints
- ❌ Search functionality
- ❌ Time series downloads
- ❌ HFM category CSVs

**Workaround**: Manual downloads (see `ofr_data_readers.py`)

**Known Series**:
```
FNYR-BGCR-A          - Broad General Collateral Rate
FNYR-EFFR-A          - Effective Federal Funds Rate (OFR version)
REPO-TRI_AR_OO-P     - Tri-party repo overnight
REPO-DVP_AR_OO-P     - DVP repo overnight
CP-AA_AR_OO-P        - AA commercial paper overnight
```

---

### OFR Manual Download System 📥

**File**: `ofr_data_readers.py`
**Status**: ✅ Ready to use (waiting for downloaded files)

**Supported Datasets**:

1. **Financial Stress Index (FSI)**
   - URL: https://www.financialresearch.gov/financial-stress-index/
   - File: `data/ofr_downloads/fsi_data.csv`
   - Use: Chart 40 (Financial Stress Monitor)

2. **Bank Systemic Risk Monitor (BSRM)**
   - URL: https://www.financialresearch.gov/bank-systemic-risk-monitor/
   - File: `data/ofr_downloads/bsrm_data.csv`
   - Use: Banking sector stress analysis

3. **STFM Repo Rates**
   - URL: https://www.financialresearch.gov/short-term-funding-monitor/
   - File: `data/ofr_downloads/stfm_repo_rates.csv`
   - Use: Chart 22 (Repo Market Dynamics)

4. **STFM Commercial Paper**
   - URL: https://www.financialresearch.gov/short-term-funding-monitor/
   - File: `data/ofr_downloads/stfm_commercial_paper.csv`
   - Use: Chart 23 (Commercial Paper Market)

5. **Hedge Fund Monitor (HFM)**
   - URL: https://www.financialresearch.gov/hedge-fund-monitor/
   - File: `data/ofr_downloads/hfm_data.csv`
   - Use: Chart 42 (Hedge Fund Positioning)

**Usage**:
```python
from ofr_data_readers import OFRDataReader

reader = OFRDataReader()
reader.print_status()  # Check what's available

fsi = reader.read_fsi()
bsrm = reader.read_bsrm()
repo = reader.read_stfm_repo()
```

---

## Daily Dashboard ✅

**File**: `money_market_dashboard.py`
**Output**: `dashboards/Money_Market_Dashboard_YYYY-MM-DD.pdf`

**Current Charts**:
1. Money Market Reference Rates (SOFR, EFFR, OBFR)
2. RRP Operations ($2,503B usage)
3. SOFR Daily Volume ($3,170B)
4. EFFR Daily Volume ($75B)
5. SOFR-EFFR Spread (3.0 bps)

**Summary Statistics**:
```
SOFR: 3.91%  |  Volume: $3,170B
EFFR: 3.88%  |  Volume: $75B
OBFR: 3.88%  |  Volume: $179B
RRP Usage: $2,503B
SOFR-EFFR Spread: 3.0 bps
```

**Run**: `python3 money_market_dashboard.py`

---

## Chart Styling ✅

**File**: `lighthouse_style.py`
**Status**: ✅ Complete with corrected colors

**Official Colors**:
```python
COLORS = {
    'ocean_blue': '#0089D1',      # Primary
    'orange': '#FF7700',           # Secondary
    'carolina_blue': '#4B9CD3',    # Tertiary
    'magenta': '#FF00FF',          # Quaternary
    'neutral': '#808080',          # Grey for axes/text
}
```

**Key Features**:
- NO gridlines (per requirements)
- Watermarks OUTSIDE chart area using `fig.text()`
- Last value labels on axes
- Chart number badge (ocean blue circle)
- "LIGHTHOUSE MACRO" top-left branding
- "MACRO, ILLUMINATED." bottom-right watermark
- Source attribution bottom-left

**Functions**:
- `create_single_axis_chart()`
- `create_dual_axis_chart()`
- `create_section_page()`
- `add_lighthouse_branding()`
- `add_last_value_label()`

---

## Data Architecture

```
lighthouse_paywall_deck/
├── data/
│   ├── nyfed_cache/           # ✅ Auto-cached (8 files, working)
│   ├── ofr_cache/             # ⚠️ Partial (1 file, limited API access)
│   └── ofr_downloads/         # 📥 Manual downloads (0 files, ready)
│
├── dashboards/
│   └── Money_Market_Dashboard_2025-11-22.pdf  # ✅ Generated daily
│
├── nyfed_api_reference.py     # ✅ Working with retry logic
├── ofr_api_reference.py       # ⚠️ Limited API access
├── ofr_data_readers.py        # 📥 Manual download support
├── money_market_dashboard.py  # ✅ Daily dashboard generator
├── lighthouse_style.py        # ✅ Corrected branding
│
├── OFR_DATA_SOURCES.md        # 📖 OFR data guide
├── CORRECTED_COLORS.md        # 📖 Color palette
└── TRADINGVIEW_DATA_REFERENCE.md  # 📖 TradingView integration
```

---

## Next Steps

### Immediate (User Action Required)
1. **Download OFR datasets**:
   - FSI: https://www.financialresearch.gov/financial-stress-index/
   - BSRM: https://www.financialresearch.gov/bank-systemic-risk-monitor/
   - STFM: https://www.financialresearch.gov/short-term-funding-monitor/
   - HFM: https://www.financialresearch.gov/hedge-fund-monitor/

2. **Save files to**: `data/ofr_downloads/`
   - `fsi_data.csv`
   - `bsrm_data.csv`
   - `stfm_repo_rates.csv`
   - `stfm_commercial_paper.csv`
   - `hfm_data.csv`

3. **Test readers**:
   ```bash
   python3 ofr_data_readers.py
   ```

### Code Updates Needed
1. ✅ ~~Complete OFR API HFM support~~ (Done, but API blocked)
2. ❌ Integrate existing `lhm_charts` toolkit into chartbook
3. ❌ Remove gridlines from charts 1-17
4. ❌ Add section divider pages with explanatory text
5. ❌ Update all charts to use #0089D1 ocean blue
6. ❌ Fix legend positioning (upper left)

### Future Enhancements
1. **Automated OFR Downloads**:
   - Shell scripts to fetch weekly
   - Cron job for daily FSI updates

2. **Expanded Dashboards**:
   - Banking stress dashboard (using BSRM)
   - Hedge fund monitor dashboard (using HFM)
   - Comprehensive stress dashboard (using FSI)

3. **TradingView Integration**:
   - API setup for automated pulls
   - MOVE index for bond volatility
   - Crypto data (Charts 28-32)

---

## Performance

**NY Fed API**:
- Initial fetch: ~5-10 seconds per endpoint
- Cached fetch: <0.1 seconds
- Cache expiry: 24 hours
- Retry logic: 3 attempts with exponential backoff

**OFR API**:
- Limited by 403 authentication errors
- Mnemonics list works (442 series)
- Series data blocked
- Manual download workflow ready

**Dashboard Generation**:
- 5-7 charts generated in ~3 seconds
- Using cached data for speed
- PDF output: ~1.5MB per dashboard

---

## Usage Examples

### Generate Daily Dashboard
```bash
python3 money_market_dashboard.py
```

### Check Data Availability
```python
from nyfed_api_reference import NYFedAPI
from ofr_data_readers import OFRDataReader

# Check NY Fed cache
nyfed = NYFedAPI()
stats = nyfed.get_cache_stats()
print(f"NY Fed cache: {stats['total_files']} files, {stats['total_size_mb']:.2f} MB")

# Check OFR downloads
ofr = OFRDataReader()
ofr.print_status()
```

### Fetch Latest Data
```python
from nyfed_api_reference import NYFedAPI

api = NYFedAPI(cache_hours=24)

# Get latest rates
sofr = api.get_sofr(last_n=10)
effr = api.get_effr(last_n=10)
rrp = api.get_rrp_operations()

print(f"Latest SOFR: {sofr['percentRate'].iloc[-1]:.2f}%")
print(f"Latest RRP: ${rrp['totalAmtAccepted'].iloc[-1]:.1f}B")
```

---

## Summary

✅ **Working**: NY Fed API, caching, dashboard generation, chart styling
⚠️ **Partial**: OFR API (metadata only)
📥 **Ready**: Manual OFR download system
❌ **TODO**: Download OFR files, integrate existing charts, remove gridlines

**Key Achievement**: Robust data infrastructure with local caching prevents repeated API failures. User now has full-blown dashboards at fingertips for NY Fed data. OFR data ready to integrate once files are downloaded.
