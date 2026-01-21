# LIGHTHOUSE MACRO - DATA COLLECTION GUIDE

## Complete list of manual data needed for full chartbook functionality



## 1. NY FED DATA (All available via https://markets.newyorkfed.org/api)

### SOFR, EFFR, OBFR Rates
**Endpoint:** `https://markets.newyorkfed.org/api/rates/secured/sofr/last/500.json`
**Status:** Cached but API response format changed
**Action Needed:**
- Export JSON response
- Save as: `data/nyfed/sofr_rates.json`
- Alternative: Use CSV download from NY Fed website

**Same for:**
- EFFR: `https://markets.newyorkfed.org/api/rates/unsecured/effr/last/500.json`
- OBFR: `https://markets.newyorkfed.org/api/rates/unsecured/obfr/last/500.json`

### BGCR (Broad General Collateral Rate) - For Repo Dispersion
**Endpoint:** `https://markets.newyorkfed.org/api/rates/secured/bgcr/search.json`
**Data Needed:**
- Daily BGCR rates
- Percentile distribution (1st, 25th, 75th, 99th percentiles)
**Save as:** `data/nyfed/bgcr_distribution.csv`

### Primary Dealer Positions
**Source:** NY Fed FR 2004 Weekly Report
**URL:** https://www.newyorkfed.org/markets/desk-operations/primary-dealer-statistics
**Data Needed:**
- Net Treasury positions (Bills, Notes, Bonds)
- Weekly frequency
**Save as:** `data/nyfed/dealer_positions.csv`

**Format:**
```csv
date,bills_net,notes_net,bonds_net,total_net
2024-01-05,-15.2,23.4,8.1,16.3
```

---

## 2. OFR DATA (Already Downloaded)

### Financial Stress Index (FSI)
**Status:** ✅ Already have `data/ofr_downloads/fsi_data.csv` (6,545 observations)
**No action needed**

### Bank Systemic Risk Monitor (BSRM)
**Status:** ✅ Already have `data/ofr_downloads/bsrm_data.csv` (327 observations)
**No action needed**

---

## 3. CROSS-CURRENCY BASIS SWAPS

**Source:** Bloomberg Terminal or BIS
**Data Needed:**
- EUR/USD 3-month basis swap (daily)
- JPY/USD 3-month basis swap (daily)
- Last 5 years

**Save as:** `data/fx/cross_currency_basis.csv`

**Format:**
```csv
date,eur_usd_3m_basis,jpy_usd_3m_basis
2024-01-01,-8.5,-12.3
```

**Alternative Free Source:** Federal Reserve H.15 report (limited coverage)

---

## 4. SWAP SPREADS

**Source:** Bloomberg or FRED (limited)
**Data Needed:**
- 2Y, 5Y, 10Y, 30Y swap spreads
- Swap Rate - Treasury Yield (same maturity)

**Save as:** `data/rates/swap_spreads.csv`

**Format:**
```csv
date,swap_2y,swap_5y,swap_10y,swap_30y
2024-01-01,25.3,28.1,22.5,18.7
```

---

## 5. TRADINGVIEW CRYPTO DATA

### Bitcoin Price
**Chart:** COINBASE:BTCUSD
**Export:** Daily close prices, last 3 years
**Save as:** `data/tradingview_exports/btc_price.csv`

**How to export from TradingView:**
1. Open chart: https://www.tradingview.com/chart/?symbol=COINBASE:BTCUSD
2. Click clock icon → Set to Daily, 3Y range
3. Right-click chart → Export chart data
4. Save CSV

### Stablecoin Supply Data
**Sources:**
- **CoinGecko API:** https://api.coingecko.com/api/v3/coins/tether/market_chart
- **Glassnode:** https://studio.glassnode.com (requires account)

**Data Needed:**
- USDT market cap (daily)
- USDC market cap (daily)
- DAI market cap (daily)

**Save as:** `data/crypto/stablecoin_supply.csv`

**Format:**
```csv
date,usdt_supply,usdc_supply,dai_supply,total_supply
2024-01-01,95000000000,25000000000,5000000000,125000000000
```

### Nasdaq & Gold (for BTC correlation)
**TradingView exports:**
- NASDAQ:NDX (Nasdaq 100 Index)
- OANDA:XAUUSD (Gold spot)

**Save as:** `data/tradingview_exports/nasdaq_price.csv` and `gold_price.csv`

---

## 6. QUALITY vs RISK ETF DATA

**Tickers:**
- QUAL (iShares MSCI USA Quality Factor ETF)
- SPY (S&P 500 ETF)

**Source:** Yahoo Finance or TradingView
**Export:** Daily close prices, 5 years
**Save as:** `data/etf/qual_spy_prices.csv`

**Format:**
```csv
date,qual_close,spy_close,qual_spy_ratio
2024-01-01,145.23,475.12,0.3057
```

---

## 7. SECTOR ETF DATA (for Sector Rotation Heatmap)

**11 Sector ETFs:**
- XLK (Technology)
- XLF (Financials)
- XLV (Healthcare)
- XLY (Consumer Discretionary)
- XLI (Industrials)
- XLE (Energy)
- XLB (Materials)
- XLP (Consumer Staples)
- XLU (Utilities)
- XLRE (Real Estate)
- XLC (Communication Services)

**Export:** Daily prices, 3 years
**Save as:** `data/etf/sector_performance.csv`

---

## 8. S&P 500 EARNINGS DATA (for Equity Risk Premium)

**Source:** S&P Dow Jones Indices
**URL:** https://www.spglobal.com/spdji/en/indices/equity/sp-500/
**Download:** "Additional Information" → Earnings & P/E data

**Data Needed:**
- Quarterly operating earnings per share
- Calculate earnings yield (E/P ratio)

**Save as:** `data/equity/sp500_earnings.csv`

**Format:**
```csv
date,earnings_per_share,price,earnings_yield
2024-Q1,55.23,5000,1.1046
```

---

## 9. MACROMICRO CHARTS (AI Infrastructure Section)

**Already specified - need screenshots/exports:**

### Chart 36: Mag 7 CapEx Trends
**URL:** https://www.macromicro.me (search for "Magnificent 7 CapEx")
**Save screenshot as:** `macromicro_charts/mag7_capex.png`

### Chart 37: AI Software RPO Growth
**Search:** "AI software RPO" or "Remaining Performance Obligations"
**Save as:** `macromicro_charts/ai_software_rpo.png`

### Chart 38: Global Semi Equipment vs Taiwan Exports
**Search:** "semiconductor equipment" or "Taiwan exports"
**Save as:** `macromicro_charts/semi_equipment_exports.png`

### Chart 39: US IT Investment Contribution to GDP
**Search:** "IT investment GDP"
**Save as:** `macromicro_charts/it_investment_gdp.png`

---

## 10. TRADINGVIEW 3-PANEL SCREENSHOTS (Single Names)

### NVDA 3-Panel Setup
**Chart URL:** https://www.tradingview.com/chart/?symbol=NASDAQ:NVDA

**Panel Configuration:**
1. **Main Panel:** Price + 50-day SMA + 200-day SMA
2. **Panel 2:** Relative Strength vs SMH (custom indicator)
3. **Panel 3:** Robust Relative Z-Score (custom indicator)

**Export:** Full screenshot (1920x1080 recommended)
**Save as:** `tradingview_screenshots/nvda_3panel.png`

### MSFT 3-Panel
**Symbol:** NASDAQ:MSFT
**Benchmark:** QQQ (instead of SMH)
**Save as:** `tradingview_screenshots/msft_3panel.png`

### TSM 3-Panel
**Symbol:** NYSE:TSM
**Benchmark:** SMH
**Save as:** `tradingview_screenshots/tsm_3panel.png`

---

## 11. TREASURY LIQUIDITY METRICS

**Source:** FINRA TRACE or Bloomberg
**Data Needed:**
- Bid-ask spreads for on-the-run Treasuries (2Y, 10Y, 30Y)
- Market depth (order book data)
- Trading volume

**Save as:** `data/treasuries/liquidity_metrics.csv`

**Format:**
```csv
date,bid_ask_2y,bid_ask_10y,bid_ask_30y,volume_10y
2024-01-01,0.5,0.8,1.2,45000000000
```

**Note:** This data is institutional-grade, may require Bloomberg access

---

## 12. CDX INDICES & MOVE INDEX

### CDX IG/HY Indices
**Source:** Bloomberg or Markit
**Data Needed:**
- CDX.NA.IG (Investment Grade) spread
- CDX.NA.HY (High Yield) spread
- Daily, 5 years

**Save as:** `data/credit/cdx_indices.csv`

### MOVE Index (Bond Volatility)
**Source:** CBOE (via Bloomberg) or Ice Data Services
**Alternative:** TradingView chart export
**Symbol:** CBOE:MOVE or $MOVE

**Save as:** `data/volatility/move_index.csv`

---

## DATA DIRECTORY STRUCTURE

```
/Users/bob/lighthouse_paywall_deck/data/
├── nyfed/
│   ├── sofr_rates.json
│   ├── effr_rates.json
│   ├── obfr_rates.json
│   ├── bgcr_distribution.csv
│   └── dealer_positions.csv
├── ofr_downloads/
│   ├── fsi_data.csv ✅
│   └── bsrm_data.csv ✅
├── fx/
│   └── cross_currency_basis.csv
├── rates/
│   └── swap_spreads.csv
├── tradingview_exports/
│   ├── btc_price.csv
│   ├── nasdaq_price.csv
│   └── gold_price.csv
├── crypto/
│   └── stablecoin_supply.csv
├── etf/
│   ├── qual_spy_prices.csv
│   └── sector_performance.csv
├── equity/
│   └── sp500_earnings.csv
├── treasuries/
│   └── liquidity_metrics.csv
├── credit/
│   └── cdx_indices.csv
└── volatility/
    └── move_index.csv

/Users/bob/lighthouse_paywall_deck/macromicro_charts/
├── mag7_capex.png
├── ai_software_rpo.png
├── semi_equipment_exports.png
└── it_investment_gdp.png

/Users/bob/lighthouse_paywall_deck/tradingview_screenshots/
├── nvda_3panel.png
├── msft_3panel.png
└── tsm_3panel.png
```

---

## PRIORITY DATA COLLECTION ORDER

### Tier 1: Critical (Fixes Current Errors)
1. ✅ NY Fed SOFR/EFFR/OBFR - Fix API response parsing
2. BGCR distribution - Repo Dispersion chart
3. MacroMicro screenshots (4 charts)
4. TradingView 3-panel screenshots (3 charts)

### Tier 2: High Priority (Proprietary Indicators)
5. Stablecoin supply data - Crypto section
6. QUAL/SPY prices - Quality vs Risk indicator
7. Bitcoin/Nasdaq/Gold prices - Correlation analysis

### Tier 3: Nice to Have (Institutional Data)
8. Cross-currency basis swaps
9. Swap spreads
10. CDX indices & MOVE index
11. Treasury liquidity metrics
12. S&P 500 earnings
13. Sector ETF data

---

## EXPORT TEMPLATES

### TradingView CSV Export Template
```csv
time,open,high,low,close,Volume
2024-01-01,100.00,102.50,99.50,101.25,1000000
```

### NY Fed API JSON Response Template
```json
{
  "refRates": [
    {
      "effectiveDate": "2024-01-01",
      "percentRate": 5.33,
      "percentPercentile1": 5.25,
      "percentPercentile25": 5.30,
      "percentPercentile75": 5.35,
      "percentPercentile99": 5.40
    }
  ]
}
```

### MacroMicro Screenshot Settings
- Resolution: 1920x1080 minimum
- Format: PNG
- Capture: Full chart including title, legend, source
- Background: White (for clean Lighthouse branding overlay)

---

## AUTOMATION SCRIPTS (Optional)

I can create Python scripts to:
1. ✅ Fetch FRED data (already working)
2. ✅ Cache NY Fed API responses (already implemented)
3. Parse CoinGecko API for stablecoin data
4. Calculate z-scores and composite indicators
5. Auto-update charts when new data arrives

Let me know which automation you want prioritized.

---

## CURRENT STATUS

**Working Data Sources:**
- ✅ FRED (800k+ series, working perfectly)
- ✅ OFR FSI & BSRM (downloaded, integrated)
- ✅ NY Fed RRP (cached, working)
- ✅ Basic labor/credit/equity charts (FRED-based)

**Need Manual Collection:**
- ⚠️ NY Fed SOFR/EFFR/OBFR (API format issue, need CSV export)
- ⚠️ BGCR distribution (manual download)
- ⚠️ MacroMicro charts (4 screenshots)
- ⚠️ TradingView screenshots (3 single-name charts)
- ⚠️ Stablecoin data (CoinGecko or manual)
- ⚠️ Cross-currency basis (Bloomberg or manual)
- ⚠️ Institutional data (swap spreads, CDX, MOVE, Treasury liquidity)

**Total Manual Items:** ~15-20 data files/screenshots needed for 100% complete chartbook
