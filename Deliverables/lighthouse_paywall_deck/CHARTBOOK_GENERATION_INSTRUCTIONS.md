# LIGHTHOUSE MACRO - CHARTBOOK GENERATION INSTRUCTIONS
## Complete Agent Guide for Automated Chartbook Production

**Version:** 1.0
**Last Updated:** November 23, 2025
**Author:** Bob Sheehan, CFA, CMT

---

## OVERVIEW

This document provides complete instructions for generating the Lighthouse Macro Premium Chartbook from start to finish. Follow these steps sequentially to produce a publication-ready PDF.

---

## PREREQUISITES

### Required Software
- Python 3.9+ with virtual environment
- Git (for version control)
- FRED API key (stored in environment or config)

### Required Python Packages
```bash
cd /Users/bob/lighthouse_paywall_deck
source venv/bin/activate
pip install pandas numpy matplotlib requests reportlab pillow fredapi
```

### Directory Structure
```
/Users/bob/lighthouse_paywall_deck/
├── venv/                          # Virtual environment
├── data/                          # Raw data cache
├── charts/
│   └── proprietary/               # Generated proprietary charts (output)
├── gather_all_chartbook_data.py   # Step 1: Data collection
├── calculate_proprietary_indicators.py  # Step 2: Indicator calculation
├── generate_all_proprietary_charts.py   # Step 3: Chart generation
├── generate_premium_chartbook.py  # Step 4: PDF assembly
├── daily_update.sh                # Automation script
├── chartbook_master_data.csv      # Master data file (output)
├── proprietary_indicators.csv     # Calculated indicators (output)
└── PROPRIETARY_INDICATORS_REFERENCE.md  # Indicator documentation

/Users/bob/macromicro_charts/      # Manual MacroMicro screenshots
/Users/bob/tradingview_charts/     # Manual TradingView screenshots
/Users/bob/Lighthouse_Macro_Premium_Chartbook.pdf  # Final output
```

---

## STEP-BY-STEP GENERATION PROCESS

### STEP 1: DATA COLLECTION

**Script:** `gather_all_chartbook_data.py`

**Purpose:** Fetch all raw economic data from FRED, OFR, and NY Fed APIs

**Data Sources:**
1. **FRED API** (Federal Reserve Economic Data)
   - 60+ economic series
   - Categories: Liquidity, Labor, Credit, Equity, Crypto, AI Infrastructure

2. **OFR** (Office of Financial Research)
   - Financial Stress Index (FSI)
   - Bank Systemic Risk Monitor (BSRM)
   - Manual download from: https://www.financialresearch.gov/financial-stress-index/
   - Place files in: `/Users/bob/lighthouse_paywall_deck/data/`

3. **NY Fed API**
   - SOFR, EFFR, OBFR (overnight rates)
   - RRP facility usage
   - Endpoint: https://markets.newyorkfed.org/api/

**Output:** `chartbook_master_data.csv` (1.9 MB, 68 series, 7,413 rows)

**Key Series Required:**
```
LIQUIDITY:
- RRPONTSYD (Reverse Repo)
- WRESBAL (Bank Reserves)
- GDP (Nominal GDP)
- WALCL (Fed Balance Sheet)
- WLRRAL (Fed Loan Programs)

LABOR:
- PAYEMS (Nonfarm Payrolls)
- UNRATE (Unemployment Rate)
- U6RATE (Underemployment)
- LNU03008396 (Long-term Unemployment >27 weeks)
- JTSJOL (Job Openings)
- JTSQUR (Quits Rate)
- JTSHIR (Hires Rate)
- JTSLDL (Layoffs/Discharges)
- AWHAETP (Average Weekly Hours)

CREDIT:
- BAMLH0A0HYM2 (HY OAS - High Yield Spread)
- BAMLC0A4CBBB (BBB Corporate Spread)
- TERMCBCCALLNS (Commercial Paper Spread)
- DRTSCILM (Consumer Credit Growth)
- TOTCI (Commercial & Industrial Loans)

EQUITY:
- SP500 (S&P 500 Index)
- VIX (Volatility Index)
- VIXCLS (VIX Close)

YIELD CURVE:
- DGS10 (10-Year Treasury)
- DGS2 (2-Year Treasury)
- DGS3MO (3-Month Treasury)
- T10Y2Y (10Y-2Y Spread)
```

**Data Transformations:**
- Forward-fill missing values for mixed-frequency data
- Align all series to daily frequency
- Handle weekends/holidays via forward-fill
- Date range: 2000-01-01 to present

**Run Command:**
```bash
cd /Users/bob/lighthouse_paywall_deck
source venv/bin/activate
python gather_all_chartbook_data.py
```

**Expected Output:**
```
✓ Collected 68 data series
✓ Date range: 2000-01-03 to 2025-11-23
✓ Saved to: chartbook_master_data.csv
```

---

### STEP 2: PROPRIETARY INDICATOR CALCULATION

**Script:** `calculate_proprietary_indicators.py`

**Purpose:** Calculate all 38 proprietary indicators with z-score normalization

**Input:** `chartbook_master_data.csv`
**Output:** `proprietary_indicators.csv` (2.2 MB, 38 columns)

#### Z-SCORE METHODOLOGY

**Standard Z-Score Formula:**
```python
z = (x - rolling_mean) / rolling_std

Where:
- rolling_mean = 252-day rolling average
- rolling_std = 252-day rolling standard deviation
- min_periods = 30 days (minimum data required)
```

**Interpretation:**
- `z > +1σ`: Above normal (elevated risk/stress)
- `z between -1σ and +1σ`: Normal range
- `z < -1σ`: Below normal (low risk/abundant conditions)
- `z > +2σ`: Extreme risk/stress
- `z < -2σ`: Extreme abundance/complacency

#### CORE COMPOSITE INDICATORS

**1. Macro Risk Index (MRI)**
```python
Formula:
MRI = LFI - LDI + YFS + z(HY_OAS) + EMD - LCI

Components:
- LFI: Labor Fragility Index
- LDI: Labor Dynamism Index (inverted - lower is worse)
- YFS: Yield-Funding Stress
- z(HY_OAS): Z-scored High Yield Spread
- EMD: Equity Momentum Divergence
- LCI: Liquidity Cushion Index (inverted - lower is worse)

Interpretation:
- MRI > +1σ: Markets under-pricing systemic risk
- MRI > +2σ: Crisis-level risk not priced in
- MRI < -1σ: Risk-on environment, low systemic stress
```

**2. Liquidity Cushion Index (LCI)**
```python
Formula:
LCI = [z(RRP/GDP) + z(Reserves/GDP)] / 2

Components:
- RRP/GDP: Reverse repo facility usage as % of GDP
- Reserves/GDP: Bank reserves as % of GDP

Data Sources:
- RRPONTSYD (RRP daily)
- WRESBAL (Reserves weekly, forward-filled)
- GDP (Quarterly, forward-filled)

Interpretation:
- LCI < -1σ: Critically low liquidity cushion (risk)
- LCI > +1σ: Abundant liquidity (supports risk assets)
```

**3. Labor Fragility Index (LFI)**
```python
Formula:
LFI = [z(LongUnemployment%) + z(-Quits) + z(-Hires/Quits)] / 3

Components:
- LongUnemployment%: % of unemployed >27 weeks
- Quits: Inverted quits rate (lower quits = higher fragility)
- Hires/Quits: Inverted ratio (lower ratio = higher fragility)

Data Sources:
- LNU03008396 (Long-term unemployed, monthly)
- UNEMPLOY (Total unemployed, monthly)
- JTSQUR (Quits rate, monthly)
- JTSHIR (Hires rate, monthly)

Calculation:
LongUnemployment% = (LNU03008396 / UNEMPLOY) * 100

Interpretation:
- LFI > +1σ: Labor market deteriorating (recession signal)
- LFI > +2σ: Severe labor fragility (imminent downturn)
```

**4. Labor Dynamism Index (LDI)**
```python
Formula:
LDI = [z(Quits) + z(Hires/Quits) + z(Quits/Layoffs)] / 3

Components:
- Quits: Job quit rate (higher = healthier labor market)
- Hires/Quits: Hiring efficiency
- Quits/Layoffs: Worker confidence ratio

Data Sources:
- JTSQUR (Quits, monthly)
- JTSHIR (Hires, monthly)
- JTSLDL (Layoffs, monthly)

Interpretation:
- LDI < -1σ: Reduced labor dynamism (structural weakness)
- LDI > +1σ: Strong labor market health
```

**5. Credit-Labor Gap (CLG)**
```python
Formula:
CLG = z(HY_OAS) - LFI

Purpose: Identifies divergence between credit pricing and labor stress

Interpretation:
- CLG > +1σ: Credit markets too complacent vs. labor weakness
- CLG < -1σ: Credit markets pricing more stress than labor shows
- CLG near 0: Credit and labor signals aligned
```

**6. Yield-Funding Stress (YFS)**
```python
Formula:
YFS = [z(10Y-2Y) + z(10Y-3M) + z(Bill-SOFR Spread)] / 3

Components:
- 10Y-2Y: Yield curve slope (inverted = stress)
- 10Y-3M: Term premium stress
- Bill-SOFR Spread: Money market plumbing stress

Data Sources:
- T10Y2Y (10Y-2Y spread, daily)
- DGS10, DGS3MO (for 10Y-3M calculation)
- DTB3 (3-month T-bill, daily)
- SOFR (Secured Overnight Financing Rate from NY Fed)

Bill-SOFR Calculation:
Bill_SOFR_Spread = DTB3 - SOFR

Interpretation:
- YFS > +1σ: Funding market stress
- YFS > +2σ: Severe plumbing issues (repo stress, dealer constraints)
```

**7. Spread-Volatility Imbalance (SVI)**
```python
Formula:
SVI = z(HY_OAS) - z(VIX)

Purpose: Compares credit spread levels to equity volatility pricing

Interpretation:
- SVI < -1σ: Equity vol pricing more risk than credit (divergence)
- SVI > +1σ: Credit pricing more risk than equity vol (rare)
```

**8. Equity Momentum Divergence (EMD)**
```python
Formula:
EMD = z(SP500_20d_momentum) - z(SP500_60d_momentum)

Calculation:
- SP500_20d_momentum = (SP500 / SP500.shift(20) - 1) * 100
- SP500_60d_momentum = (SP500 / SP500.shift(60) - 1) * 100

Interpretation:
- EMD < -1σ: Short-term momentum weakening (deteriorating breadth)
- EMD > +1σ: Strong near-term momentum vs. longer trend
```

#### SUPPORTING INDICATORS (RAW Z-SCORES)

Calculate z-scores for the following:
```python
z(HY_OAS)           # High yield credit spread
z(VIX)              # Equity volatility
z(Unemployment)     # Unemployment rate
z(U6)               # Underemployment rate
z(Job_Openings)     # JOLTS openings
z(Quits)            # Quits rate
z(Payrolls_YoY)     # Payroll growth YoY
z(Hours_YoY)        # Average hours YoY
z(Credit_Growth)    # Credit growth YoY
z(Fed_Funds)        # Federal funds rate
z(10Y2Y)            # Yield curve slope
```

**Run Command:**
```bash
python calculate_proprietary_indicators.py
```

**Expected Output:**
```
✓ Calculated 38 proprietary indicators
✓ MRI: +3.10σ (ELEVATED RISK)
✓ LCI: -1.45σ (Low liquidity)
✓ LFI: +0.57σ (Elevated fragility)
✓ Saved to: proprietary_indicators.csv
```

---

### STEP 3: PROPRIETARY CHART GENERATION

**Script:** `generate_all_proprietary_charts.py`

**Purpose:** Generate 27 institutional-quality PNG charts

**Input:** `proprietary_indicators.csv`
**Output Directory:** `/Users/bob/lighthouse_paywall_deck/charts/proprietary/`

#### CHART STYLING STANDARDS

**Color Palette:**
```python
COLORS = {
    'primary': '#003366',      # Deep blue (main line)
    'secondary': '#0066CC',    # Bright blue (secondary line)
    'accent': '#FF9900',       # Orange (highlights)
    'positive': '#00A86B',     # Green (positive zones)
    'negative': '#CC0000',     # Red (negative zones)
    'neutral': '#808080',      # Gray (neutral zones)
    'background': '#FFFFFF',   # White background
    'grid': '#E0E0E0',         # Light gray grid
}
```

**Matplotlib RC Params:**
```python
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': '#333333',
    'axes.linewidth': 1.5,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
    'lines.linewidth': 2.5,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
})
```

**Standard Chart Layout:**
```python
fig, ax = plt.subplots(figsize=(12, 7))

# Title
ax.set_title(
    'CHART TITLE',
    fontsize=16,
    fontweight='bold',
    color='#003366',
    pad=20
)

# Threshold bands (for z-scored indicators)
ax.axhspan(-2, -1, alpha=0.1, color='green', label='Low Risk')
ax.axhspan(-1, 1, alpha=0.05, color='gray', label='Normal')
ax.axhspan(1, 2, alpha=0.1, color='orange', label='Elevated Risk')
ax.axhspan(2, 10, alpha=0.15, color='red', label='High Risk')

# Zero line
ax.axhline(0, color='black', linewidth=1, linestyle='--', alpha=0.5)

# Latest value annotation
latest_val = series.iloc[-1]
ax.text(
    series.index[-1], latest_val,
    f'{latest_val:.2f}σ',
    fontsize=12, fontweight='bold',
    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8)
)

# Watermark
fig.text(
    0.99, 0.01,
    'Lighthouse Macro | lighthousemacro.com',
    ha='right', va='bottom',
    fontsize=8, color='gray', alpha=0.5
)

# Save
plt.savefig(
    'chart_name.png',
    dpi=300,
    bbox_inches='tight',
    facecolor='white'
)
plt.close()
```

#### CHARTS TO GENERATE

**Priority Charts (19 required for chartbook):**
1. `MRI_Macro_Risk_Index.png` - Flagship composite
2. `MRI_Macro_Risk_Index_components.png` - Component breakdown
3. `01_LCI_Liquidity_Cushion_Index.png`
4. `02_LFI_Labor_Fragility_Index.png`
5. `03_LDI_Labor_Dynamism_Index.png`
6. `04_CLG_Credit_Labor_Gap.png`
7. `05_YFS_Yield_Funding_Stress.png`
8. `06_SVI_Spread_Volatility_Imbalance.png`
9. `07_EMD_Equity_Momentum_Divergence.png`
10. `09_Payrolls_vs_Quits_Divergence.png` (dual-axis)
11. `10_Hours_vs_Employment_Divergence.png` (dual-axis)
12. `11_LCI_Components.png` (RRP vs Reserves breakdown)
13. `12_LFI_Components.png` (LFI component breakdown)
14. `13_LDI_Components.png` (LDI component breakdown)
15. `16_HY_OAS_Timeline.png` (raw data)
16. `17_VIX_Timeline.png` (raw data)
17. `18_Unemployment_Rate.png` (raw data)
18. `19_Job_Openings.png` (raw data)
19. `25_Yield_Curve_10Y2Y.png` (raw data)

**Chart Types:**

**A. Single Indicator Chart:**
- One line plot with z-score threshold bands
- Latest value callout
- Date range: 2010-present (for readability)

**B. Component Breakdown Chart:**
- Multiple lines showing sub-components
- Stacked area chart OR separate lines
- Legend identifying each component

**C. Dual-Axis Divergence Chart:**
- Left axis: First series (e.g., Payrolls YoY%)
- Right axis: Second series (e.g., Quits rate)
- Highlight divergences with shading

**Run Command:**
```bash
python generate_all_proprietary_charts.py
```

**Expected Output:**
```
✓ Generated 27 charts in charts/proprietary/
✓ Total size: ~13 MB
✓ All charts 300 DPI publication quality
```

---

### STEP 4: MANUAL CHART COLLECTION

#### MACROMICRO CHARTS

**Location:** `/Users/bob/macromicro_charts/`

**Source:** https://en.macromicro.me/

**Required Charts (~10-12):**
1. **US LEI vs. S&P 500** - Leading economic indicators vs equity performance
2. **Global Semi Equipment Billings vs. Taiwan Exports** - AI/chip cycle proxy
3. **US IT Investment Contribution to GDP** - Tech capex health
4. **US Companies Using AI (%)** - AI adoption trend
5. **World AI Patents Granted** - Innovation proxy
6. **AI Talent Migration** - Global talent flows
7. **Bitcoin Mining Costs** - Crypto fundamentals
8. **Additional macro data** - As needed for weekly themes

**Collection Process:**
1. Navigate to MacroMicro website
2. Select relevant charts
3. Screenshot at 960x540 or 975x635 resolution
4. Save to `/Users/bob/macromicro_charts/`
5. Use descriptive filenames: `mm-chart-YYYY-MM-DD_Chart Title-WIDTHxHEIGHT.png`

**Naming Convention:**
```
mm-chart-2025-11-21_US LEIs vs. S&P500 YoY%-975x635.png
mm-chart-2025-11-21_Global Semi Equip Billings-960x540.png
```

#### TRADINGVIEW CHARTS

**Location:** `/Users/bob/tradingview_charts/`

**Source:** https://www.tradingview.com/

**Required Charts (10 names):**
1. **NVDA** - Nvidia (AI semiconductor leader)
2. **ASML** - ASML (chip equipment)
3. **TSM** - Taiwan Semi (foundry leader)
4. **MSFT** - Microsoft (mega-cap tech + AI)
5. **JPM** - JPMorgan (bank credit proxy)
6. **GS** - Goldman Sachs (investment banking proxy)
7. **COIN** - Coinbase (crypto exchange)
8. **MSTR** - MicroStrategy (BTC treasury play)
9. **MARA** - Marathon Digital (BTC mining)
10. **HYG** - iShares HY Bond ETF (credit sentiment)

**Chart Setup:**
- Timeframe: Daily, 6-12 months visible
- Indicators: Volume, key moving averages (20/50/200 SMA)
- Trendlines: Support/resistance marked
- Resolution: 1920x1080 minimum

**Collection Process:**
1. Open TradingView
2. Load ticker
3. Add technical indicators
4. Screenshot
5. Save to `/Users/bob/tradingview_charts/`
6. Filename format: `TICKER_YYYY-MM-DD_HH-MM-SS.png`

**Naming Convention:**
```
NVDA_2025-11-22_02-17-21.png
ASML_2025-11-22_02-17-37.png
```

---

### STEP 5: PDF CHARTBOOK ASSEMBLY

**Script:** `generate_premium_chartbook.py`

**Purpose:** Combine all charts into institutional-quality PDF with explanatory text

**Inputs:**
- `proprietary_indicators.csv` (for latest values)
- `charts/proprietary/*.png` (27 charts)
- `/Users/bob/macromicro_charts/*.png` (12 charts)
- `/Users/bob/tradingview_charts/*.png` (10 charts)

**Output:** `/Users/bob/Lighthouse_Macro_Premium_Chartbook.pdf`

#### PDF STRUCTURE

**Cover Page:**
- Lighthouse Macro branding
- "Premium Institutional Chartbook" subtitle
- Current date
- Executive summary with latest MRI reading
- Key indicator values (MRI, LCI, LFI, LDI, CLG, YFS)
- Current market state assessment

**Section I: Proprietary Indicators**
- Section intro (1 page of explanatory text)
- Describes what proprietary indicators are
- Explains z-score methodology
- Defines key composites (MRI, LCI, LFI, LDI, CLG)
- 19 charts with individual annotations
- Each chart preceded by brief interpretation text

**Section II: Global Macro Intelligence**
- Section intro (1 page)
- Explains MacroMicro data sources
- Key focus areas (AI, semis, leading indicators)
- 12 MacroMicro charts (no annotations needed - charts are self-explanatory)

**Section III: Technical Analysis - Key Names**
- Section intro (1 page)
- Describes coverage universe
- Groups by sector (semis, financials, crypto, tech, credit)
- 10 TradingView charts with ticker labels

**Footer (all pages):**
```
Left: "Lighthouse Macro | lighthousemacro.com | © 2025"
Right: "Page X of Y"
```

#### ANNOTATION TEXT EXAMPLES

**For MRI:**
```
Macro Risk Index (MRI): Composite systemic risk gauge. Readings >+1σ
indicate elevated risk not priced into markets. Current elevated reading
driven by low liquidity cushion and rising labor fragility.
```

**For LCI:**
```
Liquidity Cushion Index (LCI): Tracks Fed RRP + bank reserves relative
to GDP. Negative readings indicate banking system liquidity stress.
Currently at critically low levels.
```

**For LFI:**
```
Labor Fragility Index (LFI): Measures labor market deterioration via
long-term unemployment, declining quits, and reduced hiring efficiency.
Elevated readings precede consumer spending weakness.
```

#### REPORTLAB CONFIGURATION

```python
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak

doc = SimpleDocTemplate(
    OUTPUT_PDF,
    pagesize=letter,  # 8.5" x 11"
    topMargin=0.75*inch,
    bottomMargin=0.75*inch,
    leftMargin=0.75*inch,
    rightMargin=0.75*inch
)

# Image sizing
img = Image(chart_path, width=6.5*inch, height=4.5*inch)

# Text styling
title_style: fontSize=24, color=#003366, bold
section_style: fontSize=16, color=#0066CC, bold
body_style: fontSize=10, justified
indicator_style: fontSize=9, gray background box
```

**Run Command:**
```bash
python generate_premium_chartbook.py
```

**Expected Output:**
```
============================================================
LIGHTHOUSE MACRO - PREMIUM CHARTBOOK GENERATOR
============================================================

[1/5] Loading latest indicator values...
   MRI: 3.10σ
   LCI: -1.45σ
   LFI: 0.57σ

[2/5] Initializing PDF document...

[3/5] Building cover page...

[4/5] Adding proprietary indicators section...
   ✓ Added 19 charts

[5/5] Adding MacroMicro section...
   ✓ Added 12 charts

[6/6] Adding TradingView section...
   ✓ Added 10 charts

============================================================
CHARTBOOK COMPLETE!
============================================================

Output: /Users/bob/Lighthouse_Macro_Premium_Chartbook.pdf
Size: 15.8 MB
Date: November 24, 2025
Current MRI: 3.10σ

✓ Ready for distribution!
```

---

## AUTOMATION: ONE-COMMAND UPDATE

**Script:** `daily_update.sh`

**Purpose:** Run all steps sequentially for daily refresh

```bash
#!/bin/bash
cd /Users/bob/lighthouse_paywall_deck
source venv/bin/activate

# Step 1: Update data
python gather_all_chartbook_data.py

# Step 2: Calculate indicators
python calculate_proprietary_indicators.py

# Step 3: Generate charts
python generate_all_proprietary_charts.py

# Step 4: Assemble PDF (requires manual charts added)
python generate_premium_chartbook.py

echo "✓ Chartbook generation complete!"
```

**Run Command:**
```bash
cd /Users/bob/lighthouse_paywall_deck
./daily_update.sh
```

**Cron Schedule (Optional - Weekdays at 6 AM):**
```bash
0 6 * * 1-5 cd /Users/bob/lighthouse_paywall_deck && ./daily_update.sh
```

---

## QUALITY CHECKLIST

Before distributing the chartbook, verify:

### Data Quality
- [ ] `chartbook_master_data.csv` exists and is >1 MB
- [ ] Date range covers 2000-present
- [ ] No excessive missing values (check last 30 days)
- [ ] Forward-fill applied correctly

### Indicator Calculation
- [ ] `proprietary_indicators.csv` has 38 columns
- [ ] MRI value is reasonable (-5σ to +5σ range)
- [ ] No NaN values in last 252 days
- [ ] Z-scores have mean ~0, std ~1 (check distribution)

### Chart Generation
- [ ] 27 charts exist in `charts/proprietary/`
- [ ] All charts are 300 DPI
- [ ] Latest values visible on charts
- [ ] Threshold bands rendered correctly
- [ ] Watermarks present

### Manual Charts
- [ ] 10-12 MacroMicro charts in `/Users/bob/macromicro_charts/`
- [ ] 10 TradingView charts in `/Users/bob/tradingview_charts/`
- [ ] Charts dated within last week
- [ ] Filenames follow naming conventions

### PDF Assembly
- [ ] PDF file size 10-20 MB (indicates all charts included)
- [ ] Cover page shows current date
- [ ] MRI reading on cover matches latest calculation
- [ ] All 3 sections present
- [ ] Page numbers correct
- [ ] No broken images
- [ ] Text is readable and formatted correctly

### Final Review
- [ ] Open PDF and visually inspect each page
- [ ] Check for typos in annotations
- [ ] Verify chart order makes sense
- [ ] Confirm all key indicators included
- [ ] Test PDF opens on different devices

---

## TROUBLESHOOTING

### Issue: FRED API rate limit exceeded
**Solution:**
- Add delays between API calls: `time.sleep(0.5)`
- Cache data locally and only refresh changed series
- Use FRED bulk download for historical data

### Issue: OFR data not loading
**Solution:**
- Manually download FSI CSV from https://www.financialresearch.gov/financial-stress-index/
- Place in `data/` directory
- Update file path in `gather_all_chartbook_data.py`

### Issue: Missing MacroMicro or TradingView charts
**Solution:**
- PDF generator will skip missing sections
- Add charts to respective folders
- Re-run `generate_premium_chartbook.py` only (no need to recalculate data)

### Issue: Charts showing outdated data
**Solution:**
- Run `daily_update.sh` to refresh all data
- Check FRED API key is valid
- Verify internet connection for API calls

### Issue: PDF file size too small (<5 MB)
**Cause:** Missing charts or images not embedding
**Solution:**
- Check that all chart paths exist
- Verify PIL/Pillow installed: `pip install pillow`
- Check for error messages during PDF generation

### Issue: Z-scores look wrong (all near 0 or extreme values)
**Cause:** Insufficient historical data for rolling window
**Solution:**
- Ensure at least 252 days of data for z-score calculation
- Check that `min_periods=30` in z-score function
- Verify data forward-fill is working correctly

---

## KNOWN ISSUES (TO BE FIXED)

Based on current chartbook v1.0, the following improvements are needed:

1. **Date formatting inconsistency** - Some charts show different date formats
2. **Chart sizing** - A few charts may overflow page boundaries
3. **Legend placement** - Some legends overlap with chart elements
4. **Color consistency** - Ensure all charts use Lighthouse color palette
5. **Threshold band labels** - Add text labels to colored bands for clarity
6. **Component breakdown charts** - Stack order may be confusing
7. **Dual-axis charts** - Right axis labels sometimes truncated
8. **PDF page breaks** - Some sections start mid-page instead of new page
9. **Annotation text** - Some annotations too verbose, need shortening
10. **File paths** - Hard-coded paths need to be configurable

**Priority for next version:** Fix items 1, 2, 8, 10 (formatting and structure)

---

## VERSION HISTORY

**v1.0 (November 23, 2025)**
- Initial release
- 41 total charts (19 proprietary, 12 MacroMicro, 10 TradingView)
- Explanatory text sections for accessibility
- Automated data collection and calculation
- Manual PDF assembly

**Planned for v1.1:**
- Config file for paths and API keys
- Improved chart layouts
- Automated MacroMicro screenshot capture
- PDF page break optimization
- Mobile-friendly PDF version

---

## CONTACT & SUPPORT

**Questions or Issues:**
- Email: bob@lighthousemacro.com
- Documentation: `/Users/bob/lighthouse_paywall_deck/PROPRIETARY_INDICATORS_REFERENCE.md`
- Continuous Improvement: `/Users/bob/lighthouse_paywall_deck/CONTINUOUS_IMPROVEMENT_FRAMEWORK.md`

---

**END OF INSTRUCTIONS**

*This document is the single source of truth for chartbook generation. Keep updated as process evolves.*
