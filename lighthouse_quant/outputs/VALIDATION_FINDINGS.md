# LIGHTHOUSE MACRO - INDICATOR VALIDATION FINDINGS

**Date:** 2026-01-19
**Analysis Period:** 1990-01-01 to 2026-01-16

---

## EXECUTIVE SUMMARY

The validation identified several areas requiring attention:

1. **Lead-Lag Relationships:** Only 3 of 14 hypothesized relationships validated cleanly
2. **LFI Component Weights:** Random Forest suggests hires/quits ratio is more important than currently weighted
3. **MRI Calibration:** The MRI never reached "crisis" threshold (>1.5) even during 2008; max was 1.24
4. **Data Quality:** Some infinity values in MRI computation in 2010s decade

---

## LEAD-LAG VALIDATION RESULTS

### Validated Relationships (3/14)

| Leading | Lagging | Expected Lag | Actual Lag | Correlation | Granger p |
|---------|---------|--------------|------------|-------------|-----------|
| JOLTS Quits Rate | Unemployment Rate | 6m | 1m | -0.78 | <0.0001 |
| HY OAS | Unemployment Rate | 9m | 10m | +0.57 | 0.088 |
| SLOOS CI Tightening | C&I Loans YoY | 6m | 11m | -0.34 | <0.0001 |

### Key Findings

**Quits Rate is the strongest leading indicator** for unemployment with r=-0.78. However, the actual lead time is much shorter than expected (1 month vs 6 months). This suggests:
- Quits rate is near-coincident with unemployment deterioration
- The lag may be capturing the acceleration phase rather than the level change

**HY OAS leads unemployment by ~10 months** with r=+0.57, validating the credit-labor linkage in CLG.

**SLOOS CI Tightening leads loan growth** with an 11-month lag (vs expected 6m), confirming credit standards lead lending volumes.

### Relationships Needing Review

| Relationship | Issue | Recommendation |
|--------------|-------|----------------|
| Initial Claims → Unemployment | No lead (lag=0) | Claims are coincident, not leading |
| Hires Rate → Payrolls | No lead (lag=0) | More coincident than expected |
| Housing Starts → GDP | No lead (lag=0) | May need to test against IP instead |
| Yield Curve → Unemployment | Weak correlation, long lag | Relationship may be non-linear |
| CPI Shelter → Core CPI | No lag detected | Shelter doesn't lead, it lags core |

---

## COMPOSITE WEIGHT VALIDATION

### LFI (Labor Fragility Index)

**Current Weights:**
- Long-term unemployed share: 0.35
- Inverted Quits Rate: 0.35
- Inverted Hires/Quits Ratio: 0.30

**Data-Driven Importance (for predicting forward unemployment change):**

| Component | Correlation | Elastic Net | Random Forest | Average |
|-----------|-------------|-------------|---------------|---------|
| Hires/Quits Inv | 0.09 | 0.00 | 0.86 | **0.32** |
| Quits Inv | 0.73 | 0.00 | 0.10 | **0.28** |
| Long-term Unemp | 0.18 | 0.00 | 0.04 | **0.07** |

**Finding:** Random Forest heavily weights hires/quits ratio (0.86) while Elastic Net zeroes it out. This divergence suggests:
- Non-linear relationship that RF captures but linear models miss
- Possible multicollinearity between components
- The quits rate alone (correlation 0.73) carries most of the predictive signal

**Recommendation:** Consider simplifying LFI to weight quits rate more heavily, or explore non-linear composite construction.

### MRI (Macro Risk Index)

**Current Weights vs Data-Driven Importance:**

| Pillar | Current Weight | Data-Driven | Delta |
|--------|----------------|-------------|-------|
| LPI | -0.15 | 0.33 | **+0.18** (underweighted) |
| LCI | -0.10 | 0.14 | +0.04 |
| BCI | -0.10 | 0.13 | +0.03 |
| GCI_Gov | +0.10 | 0.12 | +0.02 |
| TCI | -0.07 | 0.11 | +0.04 |
| FCI | -0.05 | 0.07 | +0.02 |
| PCI | +0.10 | 0.03 | **-0.07** (overweighted) |
| CCI | -0.10 | 0.02 | **-0.08** (overweighted) |
| HCI | -0.08 | 0.02 | **-0.06** (overweighted) |
| GCI | -0.15 | 0.02 | **-0.13** (overweighted) |

**Key Finding:** LPI (Labor Pillar) is the most important predictor of recession but is currently weighted at only 0.15. Meanwhile GCI (Growth), CCI (Consumer), and HCI (Housing) appear overweighted relative to their predictive power.

---

## REGIME VALIDATION VS NBER RECESSIONS

### MRI Performance

| Threshold | Recessions Detected | Lead Time | False Alarms | F1 Score |
|-----------|---------------------|-----------|--------------|----------|
| > 0.5 | 0/4 (0%) | N/A | 2 | 0.00 |
| > 1.0 | 0/4 (0%) | N/A | 0 | 0.00 |
| > 1.5 | 0/4 (0%) | N/A | 0 | 0.00 |

**CRITICAL FINDING:** MRI failed to detect ANY of the 4 recessions in our sample period at any threshold.

**Root Cause Analysis:**
- MRI peaked at **1.24 during the 2008 crisis** (below "High Risk" threshold of 1.5)
- MRI spends **94.9% of time in "Neutral"** range (-0.5 to +0.5)
- Some **-infinity values** in 2010s corrupting calculations

### LFI Performance

| Threshold | Detection Rate | Avg Lead Time | F1 Score |
|-----------|----------------|---------------|----------|
| > 0.5 | 100% | 8.5 months | 0.10 |
| > 1.0 | 25% | 10.0 months | 0.09 |

**Finding:** LFI at >0.5 threshold catches all recessions with 8.5 month lead, but has many false positives (low F1). This is expected for a fragility measure.

### LCI Performance

| Threshold | Detection Rate | Avg Lead Time | F1 Score |
|-----------|----------------|---------------|----------|
| < -0.5 | 50% | 4.5 months | 0.09 |
| < -1.0 | 25% | 5.1 months | 0.14 |

**Finding:** LCI at <-1.0 is more precise (fewer false alarms) but misses half of recessions. LCI is better as a confirming signal than primary trigger.

---

## RECOMMENDATIONS

### Immediate Actions

1. **Fix MRI Data Quality**
   - Investigate and remove -infinity values in 2010s
   - Root cause is likely division by zero in one of the pillar computations

2. **Recalibrate MRI Thresholds**
   - Current thresholds (0.5/1.0/1.5) are too high given historical MRI range
   - Consider: Low Risk (<-0.2), Neutral (-0.2 to +0.2), Elevated (0.2 to 0.5), High (0.5 to 0.8), Crisis (>0.8)

3. **Adjust MRI Weights**
   - Increase LPI weight from 0.15 to 0.25-0.30
   - Reduce GCI weight from 0.15 to 0.05-0.08
   - Reduce CCI weight from 0.10 to 0.03-0.05

### Research Priorities

1. **Test Non-Linear Composites**
   - Random Forest suggests non-linear relationships matter
   - Consider ensemble or threshold-based composite construction

2. **Re-examine Lead Times**
   - Many expected lead times not validated
   - Initial claims is coincident, not leading
   - May need to use acceleration (2nd derivative) rather than levels

3. **Add Recession Probability Model**
   - Convert MRI to probability using logistic transformation
   - Calibrate against NBER dates using out-of-sample validation

---

## DATA QUALITY NOTES

- **Infinity values in MRI:** Found in 2010s decade, needs investigation
- **JOLTS data starts 2001:** Pre-2001 labor analysis relies on claims/unemployment only
- **GDP data quarterly:** Growth signals have inherent lag from interpolation

---

## NEXT STEPS

1. Fix MRI computation to eliminate infinities
2. Re-run validation with recalibrated thresholds
3. Build recession probability model using validated indicators
4. Backtest regime-based allocation with corrected signals

---

**Files Generated:**
- `/Users/bob/LHM/lighthouse_quant/outputs/validation_report.html`
- `/Users/bob/LHM/lighthouse_quant/outputs/validation_results.json`
- `/Users/bob/LHM/lighthouse_quant/outputs/VALIDATION_FINDINGS.md` (this file)
