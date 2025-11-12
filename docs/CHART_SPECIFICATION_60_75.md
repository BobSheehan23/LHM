# 60-Chart Macro Dashboard Specification (Expandable to 75)

**Date:** 2025-11-12
**Purpose:** Comprehensive chartbook build with explicit FRED tickers, transforms, and data-change hooks
**Integration:** Extends existing `lhm_style_util.py` and `charts_registry.json` patterns

---

## Overview

This specification defines 60 core charts across 5 thematic arcs, expandable to 75 with fast-follow additions. Each chart includes:
- **FRED Tickers** or CSV data source indicators
- **Transform Logic** (resampling, YoY, 3m annualized, etc.)
- **Data-Change Hooks** for annotations, value tags, and regime signals

Where a series isn't on FRED (MOVE, HY/IG OAS alternatives, QRA, GS Prime, sector breadth), the notation `CSV` indicates a drop-in file for `data/` following the existing template.

---

## Arc 1: Macro Dynamics (15 charts)

### 1. Real GDP vs Final Sales (3m ann.)
- **Tickers:** `GDPC1`, `FINSLC1` (quarterly)
- **Transform:** 3-month annualized; index=100 from 2019-12; resample to monthly w/ step or plot quarterly
- **Hook:** Δ3m-ann vs prior quarter; percentile(10y)

### 2. Nominal vs Real GDP (levels & YoY)
- **Tickers:** `GDP`, `GDPC1`
- **Transform:** YoY; spread = nominal – real
- **Hook:** YoY change vs 12m ago; spread Δ

### 3. Core PCE vs "Supercore" proxy
- **Tickers:** `PCEPILFE` (core PCE); supercore = `PCEPILFE` minus PCEDUR/PCEGAS weight-proxy or use services ex-housing CSV
- **Transform:** YoY; 3m ann.
- **Hook:** Supercore 3m-ann inflection sign

### 4. Headline vs Core CPI
- **Tickers:** `CPIAUCSL`, `CPILFESL`
- **Transform:** YoY; 6m ann.; goods/services split (see #5)
- **Hook:** Core 6m-ann − headline 6m-ann

### 5. Goods vs Services CPI
- **Tickers:** `CUSR0000SAG` (goods), `CUSR0000SAS` (services)
- **Transform:** YoY; spread
- **Hook:** Spread Δ1m; z-score(24m)

### 6. PCE Deflator vs CPI (basis)
- **Tickers:** `PCEPI`, `CPIAUCSL`
- **Transform:** YoY; CPI−PCE gap
- **Hook:** Gap vs 10y range

### 7. Labor: Unemployment & Sahm Rule
- **Tickers:** `UNRATE` + rolling min(12m) for Sahm; show threshold 0.50pp
- **Transform:** Sahm = U3(3mma) − 12m low
- **Hook:** Sahm Δ1m; proximity to 0.50 threshold

### 8. Payrolls & Diffusion (proxy)
- **Tickers:** `PAYEMS`; diffusion proxy = breadth across sectors CSV or use `CES3000000008` etc.
- **Transform:** YoY; 3m ann.
- **Hook:** Payrolls 3m-ann vs 6m-ann

### 9. JOLTS: Openings, Quits Rate
- **Tickers:** `JTSJOL`, `JTSQUR`
- **Transform:** Openings per unemployed = `JTSJOL / UNEMPLOY`; Quits rate level
- **Hook:** Quits Δ1m; openings/unemp ratio Δ1m

### 10. Hours & Earnings
- **Tickers:** `CES0500000003` (avg weekly hours, total private), `CES0500000008` (earnings)
- **Transform:** Hours YoY; earnings 3m ann.
- **Hook:** Real earnings = earnings − `CPIAUCSL` 3m-ann

### 11. Industrial Production & Capacity Utilization
- **Tickers:** `INDPRO`, `TCU`
- **Transform:** YoY; z-score(10y)
- **Hook:** IP Δ1m; TCU distance from 80

### 12. Retail Sales (Control group proxy)
- **Tickers:** `RSAFS` (headline); `RRSFS` (real retail)
- **Transform:** Real = deflate by `CPIAUCSL`; 3m ann.
- **Hook:** Control-like proxy Δ3m-ann

### 13. Housing: Starts & Permits
- **Tickers:** `HOUST`, `PERMIT`
- **Transform:** 3m MA; YoY
- **Hook:** Permits vs Starts gap Δ

### 14. Home Prices
- **Tickers:** `CSUSHPINSA` or `USSTHPI`
- **Transform:** YoY; 3m ann.
- **Hook:** Momentum flip flag (3m ann crosses 0)

### 15. Sentiment (UMich) vs Unemployment
- **Tickers:** `UMCSENT`, `UNRATE` (inv.)
- **Transform:** Standardize; correlation(24m)
- **Hook:** Correlation trend Δ6m

---

## Arc 2: Monetary Mechanics (15 charts)

### 16. Fed Balance Sheet: RRP & Reserves
- **Tickers:** `RRPONTSYD`, `WRESBAL`
- **Transform:** Δw/w; z-score(52w)
- **Hook:** RRP bleed pace (Δw/w), Reserves Δw/w

### 17. TGA (Treasury General Account)
- **Tickers:** `WTREGEN`
- **Transform:** Δw/w; 4w sum of net issuance CSV to overlay
- **Hook:** TGA draw/build pace

### 18. EFFR vs SOFR vs IORB
- **Tickers:** `EFFR`, `SOFR`, `IORB`
- **Transform:** Spreads: SOFR−EFFR, EFFR−IORB
- **Hook:** Spread Δ1d/1w; flag stress if SOFR>EFFR

### 19. Bills vs RRP (4W bill yield − SOFR)
- **Tickers:** `DGS1MO`, `SOFR`
- **Transform:** Basis (bps)
- **Hook:** Basis sign flip; Δ1w

### 20. ACM 10y Term Premium
- **Data:** CSV (NY Fed ACM)
- **Transform:** Level; 3m change
- **Hook:** TP Δ3m; percentile(5y)

### 21. Yield Curve 3m-10y
- **Tickers:** `TB3MS`, `DGS10`
- **Transform:** Spread; inversion duration (days <0)
- **Hook:** Δ10d and inversion streak length

### 22. Yield Curve 2s-10s
- **Tickers:** `DGS2`, `DGS10`
- **Transform:** Spread; 30-day MA
- **Hook:** Steepening momentum flag

### 23. Coupon vs Bill Share (issuance)
- **Data:** CSV (QRA)
- **Transform:** Share of bills; 3m MA
- **Hook:** Bill share Δq/q

### 24. Bank Credit & Reserves
- **Tickers:** `TOTBKCR` (or `CLF`, alt) + `WRESBAL`
- **Transform:** YoY; correlation(52w)
- **Hook:** Divergence signal (|z|>1)

### 25. M2 & Velocity
- **Tickers:** `M2SL`, `M2V`
- **Transform:** YoY; z-score
- **Hook:** Velocity Δq/q

### 26. Corporate Credit Spreads
- **Tickers:** `BAMLH0A0HYM2` (HY OAS), `BAMLC0A0CM` (IG OAS)
- **Transform:** Level; 4w change
- **Hook:** HY vs IG gap Δ

### 27. Mortgage Rate & Housing Affordability
- **Tickers:** `MORTGAGE30US`, wages proxy `CES0500000008`, `CPIAUCSL`
- **Transform:** Affordability index proxy
- **Hook:** Affordability Δ1m

### 28. FX Basis Proxy: Cross-currency (JPY/USD)
- **Data:** CSV (3m basis) + `DCOILWTICO` optional overlay
- **Transform:** Level; 3m change
- **Hook:** Basis squeeze flag

### 29. Liquidity Plumbing Index (LPI)
- **Components:** (−ΔRRP w/w), (−ΔTGA w/w), SOFR−EFFR, `WRESBAL` YoY
- **Transform:** Standardize each; mean z
- **Hook:** LPI Δw/w & regime (Easing/Tightening)

### 30. Collateral Fragility Score (CFS)
- **Components:** SOFR−EFFR, `DGS1MO`−SOFR, (−`RRPONTSYD`)
- **Transform:** Z-score composite
- **Hook:** CFS Δw/w & state (Stable/Fragile)

---

## Arc 3: Market Technicals (15 charts)

### 31. S&P 500 Level w/ MAs
- **Tickers:** `SP500` (FRED daily)
- **Transform:** 50/200-dma; golden/death cross flags
- **Hook:** Price vs MA bands; Δ5d

### 32. Equal-Weight vs Cap-Weight SPX
- **Data:** CSV (RSP/SPY ratio) or `SP500EW` if available
- **Transform:** Ratio; z-score(3y)
- **Hook:** Breadth thrust flag

### 33. SPX Breadth (adv/decl proxies)
- **Data:** CSV (percent >50dma / >200dma)
- **Transform:** Level; 10-day thrusts
- **Hook:** %>200dma Δ5d

### 34. Nasdaq-100 & Momentum
- **Data:** CSV (NDX) or `NASDAQCOM`
- **Transform:** 12-1 momentum; RSI(14)
- **Hook:** Momentum regime tag

### 35. Drawdowns: SPX vs HY OAS
- **Tickers:** `SP500`, `BAMLH0A0HYM2`
- **Transform:** SPX drawdown; overlay HY OAS
- **Hook:** Divergence flag (higher OAS without new lows)

### 36. MOVE vs VIX
- **Tickers:** `VIXCLS` and CSV (MOVE)
- **Transform:** Z-score each; spread (MOVE−VIX)
- **Hook:** Spread Δ1w

### 37. Rates-Equities Correlation
- **Tickers:** `SP500` vs `DGS10` daily returns
- **Transform:** Rolling 90d corr
- **Hook:** Sign flip flag

### 38. Small vs Large (IWM/SPY)
- **Data:** CSV ratio
- **Transform:** Ratio; 26-wk ROC
- **Hook:** Trend break flag

### 39. Value vs Growth
- **Data:** CSV (VLUE/QQQ or Russell factors)
- **Transform:** Ratio; z-score(5y)
- **Hook:** Rotation pulse Δ1m

### 40. Energy vs Tech (XLE/XLK)
- **Data:** CSV ratio
- **Transform:** Ratio; 3m MA crossover
- **Hook:** Crossover event

### 41. Copper/Gold vs 10y
- **Tickers:** `PCOPPUSDM`, `GOLDAMGBD228NLBM`, `DGS10`
- **Transform:** Ratio; correlation(1y)
- **Hook:** Corr Δ3m

### 42. Credit vs Equity (IG OAS vs SPX)
- **Tickers:** `BAMLC0A0CM`, `SP500`
- **Transform:** OAS inverted z; overlay SPX
- **Hook:** Disagreement flag

### 43. Term Structure of VIX (1m–3m)
- **Data:** CSV (VX1/VX3)
- **Transform:** Contango/backwardation
- **Hook:** Term premium Δ5d

### 44. CTA Trend Proxy (simple rules)
- **Data:** CSV (model output)
- **Transform:** 20/100/200-dma signals across majors
- **Hook:** Net signal flips

### 45. Breadth Heatmap (sectors)
- **Data:** CSV (%>50dma by sector)
- **Transform:** Heatmap table + bar
- **Hook:** Sector thrust count

---

## Arc 4: Asset Class Dashboard (10 charts)

### 46. Dollar Index (Trade-weighted)
- **Tickers:** `DTWEXBGS` (broad) or `DTWEXAFEGS` (advanced)
- **Transform:** 3m ROC; z-score(3y)
- **Hook:** ROC Δ1m

### 47. EURUSD / DXY proxy
- **Tickers:** `DEXUSEU` (USD per EUR; invert for EURUSD)
- **Transform:** 3m ROC
- **Hook:** Breakout flag vs 200-dma

### 48. USDJPY
- **Tickers:** `DEXJPUS` (JPY per USD)
- **Transform:** 3m ROC; RSI
- **Hook:** RSI regime tag

### 49. GBPUSD
- **Tickers:** `DEXUSUK`
- **Transform:** 3m ROC
- **Hook:** Δ5d vs carry proxy CSV

### 50. Gold vs 10y Real (breakeven proxy)
- **Tickers:** `GOLDAMGBD228NLBM`, `T10YIE`, `DGS10` → real ≈ DGS10 − T10YIE
- **Transform:** Gold z(3y); overlay real yield (inv.)
- **Hook:** Divergence Δ1m

### 51. WTI Crude
- **Tickers:** `DCOILWTICO`
- **Transform:** 13w ROC; term flag CSV (CL1-CL6)
- **Hook:** ROC Δ4w

### 52. Copper
- **Tickers:** `PCOPPUSDM`
- **Transform:** 26w ROC; z-score
- **Hook:** China-sensitive pulse tag (note only)

### 53. HY OAS (level)
- **Tickers:** `BAMLH0A0HYM2`
- **Transform:** Level; 4w Δ
- **Hook:** Tightening/widening state

### 54. IG OAS (level)
- **Tickers:** `BAMLC0A0CM`
- **Transform:** Level; 4w Δ
- **Hook:** Pace vs HY (pair with #53)

### 55. UST Term Premium Map
- **Data:** CSV ACM term premia (2y, 5y, 10y, 30y)
- **Transform:** Bar + 3m Δ
- **Hook:** Kink location shift

---

## Arc 5: Proprietary & Dashboards (5 charts)

### 56. Liquidity Plumbing Index (LPI)
- **Reference:** As in #29
- **Transform:** Mean z; regime shading
- **Hook:** Δw/w; state (Easing/Tightening)

### 57. Collateral Fragility Score (CFS)
- **Reference:** As in #30
- **Transform:** Mean z; stress bands
- **Hook:** Δw/w; state (Stable/Fragile)

### 58. Real Policy Rate
- **Formula:** `EFFR` − `PCEPILFE` YoY
- **Transform:** Level; 3m Δ
- **Hook:** Above/below zero tag

### 59. Growth Pulse Composite
- **Components:** 3m-ann: `GDPC1`, `INDPRO`, real `PCEC96` (Real PCE)
- **Transform:** Standardize; mean
- **Hook:** Composite Δ1m and band

### 60. Regime Dashboard (4-panel)
- **Components:** LPI, CFS, 2s10s, HY OAS
- **Transform:** Each with 12m z; traffic-light map
- **Hook:** "Regime flip" when 3/4 signals cross

---

## Fast-Follow Extension: Charts 61-75

### 61. CPI "super-supercore"
- **Data:** Services ex-housing, ex-energy CSV
- **Transform:** YoY; 3m ann.
- **Hook:** Momentum inflection

### 62. Trimmed-mean PCE
- **Data:** CSV (Dallas Fed)
- **Transform:** YoY vs headline PCE
- **Hook:** Gap Δ1m

### 63. Atlanta Fed Sticky vs Flexible CPI
- **Data:** CSV
- **Transform:** YoY spread
- **Hook:** Spread regime change

### 64. Jobless Claims
- **Tickers:** `ICSA` vs Continuing `CCSA`
- **Transform:** 4w MA; ratio
- **Hook:** Ratio Δ4w

### 65. NFIB Hiring Plans
- **Tickers:** `NFIBHIRE` (if connected) or CSV
- **Transform:** Level; 6m Δ
- **Hook:** Above/below 50 threshold

### 66. ISM Manufacturing
- **Tickers:** `NAPM` & New Orders `NAPMNOR` (mind the series gaps)
- **Transform:** Level; expansion/contraction zone
- **Hook:** 50 threshold cross

### 67. ISM Services
- **Tickers:** `NAPMNONM` CSV if needed
- **Transform:** Level vs manufacturing
- **Hook:** Divergence flag

### 68. Fiscal deficit
- **Data:** Monthly Treasury Statement CSV + `GFDEBTN` debt stock
- **Transform:** 12m sum; % GDP
- **Hook:** Deficit pace Δq/q

### 69. Tax receipts
- **Data:** 12m sum CSV
- **Transform:** YoY
- **Hook:** Growth deceleration flag

### 70. TIPS 10y & 5y real yields
- **Tickers:** `DFII10`, `DFII5`
- **Transform:** Level; 5y-10y spread
- **Hook:** Curve steepness Δ

### 71. 10y breakeven vs Core PCE gap
- **Tickers:** `T10YIE` vs `PCEPILFE` YoY
- **Transform:** Breakeven − inflation; gap
- **Hook:** Gap Δ3m

### 72. Eurodollar/SOFR futures curve
- **Data:** CSV
- **Transform:** Forward rate curve; curvature
- **Hook:** Kink shift

### 73. SPX equal-weight drawdown vs cap-weight drawdown
- **Data:** CSV
- **Transform:** Both drawdowns from ATH
- **Hook:** Divergence magnitude

### 74. EM FX basket
- **Data:** CSV (equal basket of BRL/MXN/CLP)
- **Transform:** Index; 3m ROC
- **Hook:** EM stress flag

### 75. Copper/China PMI overlay
- **Data:** CSV (PMI) + `PCOPPUSDM`
- **Transform:** PMI with copper overlay
- **Hook:** Divergence Δ1m

---

## Implementation Notes

### File Integration
- **Styling:** Reuse and extend `lhm_style_util.py` with watermarks, value tags, PDF export
- **Registry:** Extend `charts_registry.json` pattern from ~55 to 60-75 chart IDs
- **CSV Hooks:** Drop external CSVs into `data/` for non-FRED series; document column names in registry notes

### Automation Pipeline
- **Structure:** Clone Week-45 run structure for export pathing
- **Output:** Generate teaser ready for Substack Founding-Member edition
- **Narrative:** Slot chart IDs into existing Chartbook markdown scaffold (Lead Summary + per-arc tables)

### Transform Utilities Required
- **Resampling:** Quarterly → monthly (step/interpolation options)
- **Rolling calculations:** 3m ann, 6m ann, YoY, MAs (50/200-day, 3m, etc.)
- **Z-scores:** Flexible windows (10y, 5y, 3y, 52w, 24m)
- **Composites:** Mean standardized components (LPI, CFS, Growth Pulse)
- **Technical indicators:** RSI, ROC, momentum, drawdowns, correlations
- **Spreads & ratios:** Basis calculations, curve spreads, sector/factor ratios

### Hook Computation Framework
Each hook represents a computable signal that can drive:
- **Annotations:** Dynamic text overlays with latest values/changes
- **Value tags:** Badge-style indicators (regime, state, threshold status)
- **Traffic lights:** Color-coded signals (green/yellow/red)
- **Flags:** Event markers (crossovers, flips, thresholds, divergences)

Hooks should be computed during chart generation and passed to annotation utilities.

---

## Expandability Beyond 75

Additional candidate charts for future expansion:
- Regional Fed nowcasts (NY Fed, Atlanta GDPNow)
- Consumer credit growth & delinquencies
- Commercial real estate price indices
- Equity valuation metrics (CAPE, earnings yield vs bonds)
- Options flow proxies (put/call ratios, gamma exposure)
- Commodity term structures (gold, oil, natural gas)
- International yield curves (Bunds, Gilts, JGBs)
- Fed Funds futures-implied path
- Cross-asset volatility (realized vs implied)

---

**Document Version:** 1.0
**Last Updated:** 2025-11-12
**Status:** Ready for implementation
**Next Steps:** Extend `charts_registry.json`, wire transforms, validate CSV templates

---

*"That's our view from the Watch. As always, we'll be sure to leave the light on."*
