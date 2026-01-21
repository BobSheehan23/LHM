# HORIZON 2026 - SESSION 2 CHART VALIDATION
## December 22, 2025

---

## EXECUTIVE SUMMARY

**Total Files Received:** 44 (39 PNG + 4 WEBP + 1 preview)
**Unique Charts After Deduplication:** 34
**Charts Needing Corrections:** 7
**Exact Duplicates to Remove:** 6
**Similar/Overlapping to Evaluate:** 4

---

## DUPLICATE ANALYSIS

### EXACT DUPLICATES (REMOVE)
| Remove | Keep | Reason |
|--------|------|--------|
| 25.png | 20.png | Federal Debt Trajectory - identical |
| 29.png | 4.png | Bank Reserves vs GDP - identical |
| preview.png | 4.png | Bank Reserves vs GDP - identical |
| 7.webp | 7.png | Same chart, lower quality format |
| 9.webp | 9.png | Same chart, lower quality format |
| 15.webp | 15.png | Same chart, lower quality format |
| 18.webp | 18.png | Same chart, lower quality format |

### SIMILAR CHARTS - EVALUATION NEEDED
| Charts | Topic | Recommendation |
|--------|-------|----------------|
| 11 vs 22 | Foreign Treasury Holdings | **KEEP 11** (more detailed annotations), **REMOVE 22** |
| 12 vs 16 | SOFR-EFFR Spread | **KEEP 16** (longer timeframe + 20D MA), **REMOVE 12** (redundant) |
| 6 vs 18 vs 27 | Treasury Auction Tails | **KEEP ALL 3** (different perspectives: scatter, time series, by tenor) |
| 4 vs 26 | Bank Reserves/GDP | **KEEP 4** (event annotations), **REMOVE 26** (redundant styling) |
| 9 vs 35 | Credit-Labor Gap | **KEEP 35** (longer history), **REMOVE 9** (shorter timeframe, both need corrections) |
| 37 vs 38 | Quits Rate | **KEEP 38** (full history 2000+), **REMOVE 37** (subset 2018+) |

---

## CORRECTIONS REQUIRED

### CRITICAL CORRECTIONS (Thesis-Altering)

#### Chart 9 / Chart 35: Credit-Labor Gap (CLG)
- **OLD VALUES:** CLG: -0.81σ / -0.82σ, HY: 300 bps
- **CORRECT VALUES:** CLG: **+0.16σ**, HY: **295 bps**
- **NARRATIVE CHANGE:** 
  - OLD: "Credit markets dangerously complacent, spreads too tight"
  - NEW: "Credit markets have repriced to match labor reality"
- **ACTION:** Significant annotation replacement needed

### STANDARD CORRECTIONS

#### Chart 7: Credit Spread Percentile Gauges
- **ISSUE:** HY Spread shows "Current: 298 bps"
- **CORRECT:** **295 bps**
- **ACTION:** Update annotation

#### Chart 12: SOFR-EFFR Spread (Repo Stress)
- **ISSUE:** Shows "Current: 8.9bp"
- **CORRECT:** **2 bps** (Dec 18 value)
- **NOTE:** May be stale data from different date
- **ACTION:** Verify date, update annotation

#### Chart 16: SOFR-EFFR Spread (Early Warning)
- **ISSUE:** Shows "Current: 9 bps"
- **CORRECT:** **2 bps**
- **ACTION:** Update annotation

#### Chart 36: Labor Fragility Index (LFI)
- **ISSUE:** No current value annotation visible
- **CORRECT:** Add **-0.63σ** annotation
- **ACTION:** Add magenta callout with current value

#### Chart 39: High Yield Spreads (Historical)
- **ISSUE:** Shows "Current: 298 bps"
- **CORRECT:** **295 bps**
- **ACTION:** Update annotation

---

## FINAL CHART LIST (RECOMMENDED 34 UNIQUE CHARTS)

### PILLAR 1: MACRO DYNAMICS (12 Charts)

| # | File | Title | Status |
|---|------|-------|--------|
| 1 | 1.png | Excess Savings Depletion | ✅ VALID |
| 2 | 5.png | Employment Diffusion Index | ✅ VALID |
| 3 | 8.png | Two-Speed Consumer Credit Bifurcation | ✅ VALID |
| 4 | 23.png | Subprime Auto Delinquencies | ✅ VALID |
| 5 | 24.png | Job Cuts vs Initial Claims | ✅ VALID |
| 6 | 30.png | Market Breadth | ✅ VALID |
| 7 | 33.png | Commercial Real Estate Delinquencies | ✅ VALID |
| 8 | 36.png | Labor Fragility Index | ⚠️ NEEDS ANNOTATION (+LFI: -0.63σ) |
| 9 | 37.png | Quits Rate (Recent) | ⚠️ EVALUATE (may remove for 38) |
| 10 | 38.png | Quits Rate (Full History) | ✅ VALID |

### PILLAR 2: MONETARY MECHANICS (18 Charts)

| # | File | Title | Status |
|---|------|-------|--------|
| 1 | 2.png | Yield Curve Evolution Heatmap | ✅ VALID |
| 2 | 3.png | Primary Dealer Balance Sheet | ✅ VALID |
| 3 | 4.png | Bank Reserves vs GDP | ✅ VALID |
| 4 | 6.png | Treasury Auction Tails (Scatter) | ✅ VALID |
| 5 | 7.png | Credit Spread Percentile Gauges | ⚠️ NEEDS CORRECTION (HY: 298→295) |
| 6 | 10.png | Standing Repo Facility Usage | ✅ VALID |
| 7 | 11.png | Foreign Treasury Holdings | ✅ VALID |
| 8 | 13.png | Fiscal Dominance Cascade | ✅ VALID |
| 9 | 14.png | Critical Event Calendar | ✅ VALID |
| 10 | 15.png | Repo Rate Dispersion | ✅ VALID |
| 11 | 16.png | SOFR-EFFR Spread (Early Warning) | ⚠️ NEEDS CORRECTION (9→2 bps) |
| 12 | 17.png | 10-Year Yield Scenario Analysis | ✅ VALID |
| 13 | 18.png | Auction Tails (Time Series) | ✅ VALID |
| 14 | 19.png | Treasury Basis Dynamics | ✅ VALID |
| 15 | 20.png | Federal Debt Trajectory | ✅ VALID |
| 16 | 21.png | Federal Interest Expense | ✅ VALID |
| 17 | 27.png | Treasury Auction Tails (By Tenor) | ✅ VALID |
| 18 | 28.png | Treasury Yield Curve Repricing | ✅ VALID |
| 19 | 31.png | Treasury Issuance by Tenor | ✅ VALID |
| 20 | 32.png | Treasury Maturity Wall | ✅ VALID |
| 21 | 35.png | Credit-Labor Gap | ⚠️ MAJOR CORRECTION (CLG sign flip) |
| 22 | 39.png | High Yield Spreads Historical | ⚠️ NEEDS CORRECTION (HY: 298→295) |

### PILLAR 3: MARKET TECHNICALS (3 Charts)

| # | File | Title | Status |
|---|------|-------|--------|
| 1 | 30.png | Market Breadth | ✅ VALID |
| 2 | 34.png | Cross-Asset Positioning Matrix | ✅ VALID |

---

## FILES TO DELETE (10 files)

```
# Exact duplicates
rm 25.png      # Duplicate of 20.png
rm 29.png      # Duplicate of 4.png
rm preview.png # Duplicate of 4.png

# WebP versions (keep PNG)
rm 7.webp
rm 9.webp
rm 15.webp
rm 18.webp

# Similar content (keep better version)
rm 22.png      # Keep 11.png instead
rm 12.png      # Keep 16.png instead
rm 26.png      # Keep 4.png instead
```

---

## CORRECTION SUMMARY TABLE

| Chart | Field | Old Value | New Value | Priority |
|-------|-------|-----------|-----------|----------|
| 35 | CLG | -0.82σ | +0.16σ | CRITICAL |
| 35 | Narrative | "Spreads too tight" | "Spreads match reality" | CRITICAL |
| 9 | CLG | -0.81σ | +0.16σ | CRITICAL |
| 9 | HY OAS | 300 bps | 295 bps | HIGH |
| 7 | HY OAS | 298 bps | 295 bps | HIGH |
| 39 | HY OAS | 298 bps | 295 bps | HIGH |
| 16 | SOFR-EFFR | 9 bps | 2 bps | MEDIUM |
| 36 | LFI | (missing) | -0.63σ | MEDIUM |

---

## DEFINITIVE VALUES REFERENCE

```
LFI:       -0.63σ   (Sep 2025)
LCI:       -0.91σ   (Q1 2025)
CLG:       +0.16σ   (Dec 2025) ← SIGN CHANGED
MRI:       -0.33σ   (Current)

HY OAS:    295 bps  (Dec 18)
SOFR-EFFR: +2 bps   (Dec 18)
10Y-2Y:    +66 bps  (Dec 18)

SPX:       6,834    (Dec 19)
VIX:       16.87    (Dec 18)
RRP:       $3.05B   (Dec 19)

Unemployment: 4.6%  (Nov)
Quits Rate:   1.8%  (Oct)
```

---

## NEXT STEPS

1. **Delete duplicates** (10 files)
2. **Apply corrections** (7 charts)
3. **Final count:** ~34 unique charts
4. **Combined with Session 1:** 19 + 34 = 53 charts
5. **After final dedup/QA:** Target ~50 charts for HORIZON 2026

---

*Report generated: December 22, 2025*
*Session 2 of HORIZON 2026 Chart Validation*
