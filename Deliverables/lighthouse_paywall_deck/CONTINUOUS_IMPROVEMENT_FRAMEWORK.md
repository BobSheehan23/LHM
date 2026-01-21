## LIGHTHOUSE MACRO - CONTINUOUS IMPROVEMENT FRAMEWORK
### Optimizing Proprietary Indicators for Maximum Edge

**Date:** November 23, 2025
**Purpose:** Systematically improve indicator quality, weights, and predictive power

---

## PHILOSOPHY

> "Not only should we constantly look to create new metrics for an edge, we should be making sure the metrics we currently have are optimally created/weighted/applied."
> — Bob Sheehan

**Core Principles:**
1. **Data-Driven Optimization:** Test everything, assume nothing
2. **Continuous Calibration:** Markets evolve, so must our indicators
3. **Edge Preservation:** Maintain proprietary advantage through iteration
4. **Institutional Rigor:** Document, validate, and improve systematically

---

## OPTIMIZATION FRAMEWORK

### Phase 1: Indicator Quality Assessment (Monthly)

**For Each Indicator, Measure:**

1. **Signal-to-Noise Ratio**
   - Calculate autocorrelation (does signal persist?)
   - Measure false signal rate
   - Compare to random walk

2. **Predictive Power**
   - Lead time to market events (how many days/weeks ahead?)
   - Correlation to forward returns
   - Regime shift detection accuracy

3. **Stability**
   - Consistency across market regimes
   - Robustness to outliers
   - Rolling window performance

---

### Phase 2: Component Weight Optimization (Quarterly)

**Current Indicators Needing Optimization:**

#### 1. Macro Risk Index (MRI)
**Current Formula:**
```
MRI = LFI - LDI + YFS + z(HY OAS) + EMD - LCI
```

**Equal-weighted (each component = 1)**

**Optimization Questions:**
- Should components have **different weights**?
- Should weights be **dynamic** based on regime?
- Which component has **highest predictive power** for SPX drawdowns?

**Testing Framework:**
```python
# Optimization script pseudocode
def optimize_mri_weights():
    # Test all weight combinations
    for w1 in np.linspace(0.5, 2.0, 10):  # LFI weight
        for w2 in np.linspace(0.5, 2.0, 10):  # LDI weight
            # ... etc
            mri_candidate = w1*LFI - w2*LDI + w3*YFS + w4*HY + w5*EMD - w6*LCI

            # Evaluate predictive power
            correlation_to_forward_SPX = correlate(mri_candidate, SPX.pct_change(21).shift(-21))
            sharpe_ratio = mean(returns) / std(returns)
            max_drawdown = calculate_max_dd(backtest_strategy(mri_candidate))

            # Track best performer
            if sharpe_ratio > best_sharpe:
                best_weights = [w1, w2, w3, w4, w5, w6]

    return best_weights
```

**Backtest Validation:**
- Use 2018-2022 for optimization
- Test on 2023-2025 out-of-sample
- Require >15% improvement over equal-weight

---

#### 2. Labor Fragility Index (LFI)
**Current Formula:**
```
LFI = z(LongUnemployment%) + z(-Quits) + z(-Hires/Quits) / 3
```

**Questions:**
- Should **long-duration unemployment** be weighted higher? (It's sticky, hard to reverse)
- Should **quits** be weighted higher? (Leading indicator)
- Is **hires/quits** redundant with quits alone?

**Test Matrix:**
| Weight Scheme | LongUnemp | Quits | H/Q | Correlation to Future Payrolls | Lead Time |
|---------------|-----------|-------|-----|-------------------------------|-----------|
| **Equal** | 0.33 | 0.33 | 0.33 | ? | ? |
| **Long-Heavy** | 0.50 | 0.30 | 0.20 | ? | ? |
| **Quits-Heavy** | 0.25 | 0.50 | 0.25 | ? | ? |
| **Two-Factor** | 0.50 | 0.50 | 0.00 | ? | ? |

**Validation Metric:** Correlation to 3-month forward NFP growth

---

#### 3. Liquidity Cushion Index (LCI)
**Current Formula:**
```
LCI = z(RRP/GDP) + z(Reserves/GDP) / 2
```

**Questions:**
- Should RRP be weighted **higher** than reserves? (More volatile, more predictive?)
- Should we include **TGA** as third component?
- Should we add **IORB-SOFR spread** (plumbing stress)?

**Enhanced LCI Candidates:**
```
LCI_v2 = 0.6*z(RRP/GDP) + 0.4*z(Reserves/GDP)
LCI_v3 = 0.4*z(RRP/GDP) + 0.3*z(Reserves/GDP) + 0.3*z(-TGA/GDP)
LCI_v4 = 0.5*z(RRP/GDP) + 0.3*z(Reserves/GDP) + 0.2*z(-IORB_SOFR_Spread)
```

**Test Against:** VIX spikes, credit spread widening events

---

### Phase 3: Window Length Optimization (Quarterly)

**Current Default:** 252-day (1-year) rolling window for z-scores

**Questions:**
- Is 252 days optimal for all indicators?
- Should labor indicators use **longer windows** (slower-moving)?
- Should credit indicators use **shorter windows** (faster-reacting)?

**Test Matrix:**
| Indicator | Current | Test 126d | Test 378d | Test 504d | Optimal? |
|-----------|---------|-----------|-----------|-----------|----------|
| LCI | 252 | ? | ? | ? | ? |
| LFI | 252 | ? | ? | ? | ? |
| YFS | 252 | ? | ? | ? | ? |
| CLG | 252 | ? | ? | ? | ? |

**Validation:** Sharpe ratio of signal-based trading strategy

---

### Phase 4: Threshold Calibration (Quarterly)

**Current Thresholds:**
- +1σ = Caution
- +2σ = High Risk
- -1σ = Low Risk

**Questions:**
- Are these thresholds **optimal** for each indicator?
- Should MRI use **asymmetric thresholds** (+0.75σ vs -1.5σ)?
- Should CLG threshold be **0σ** or something else?

**Optimization Framework:**
```python
# Find optimal thresholds
def optimize_thresholds(indicator_name, target_metric):
    best_threshold = None
    best_performance = 0

    for threshold in np.arange(-2, 2, 0.1):
        # Generate signals
        signals = indicator > threshold  # Long when above threshold

        # Backtest
        returns = signals.shift(1) * SPX.pct_change()
        sharpe = returns.mean() / returns.std() * np.sqrt(252)

        if sharpe > best_performance:
            best_performance = sharpe
            best_threshold = threshold

    return best_threshold, best_performance
```

---

## NEW INDICATOR DEVELOPMENT

### Candidate Indicators to Build

#### 1. **Bank Lending Standards Composite**
**Components:**
- Senior Loan Officer Opinion Survey (SLOOS) data
- C&I loan tightening %
- Consumer loan tightening %
- CRE loan tightening %

**Hypothesis:** Leads credit spread widening by 2-3 quarters

**Status:** Not yet built - needs SLOOS data integration

---

#### 2. **Labor Market Flow Efficiency Index**
**Formula (proposed):**
```
Flow_Efficiency = z(Hires / Openings)  # Conversion rate
                  + z(-Duration_Unemployment)  # Speed of matching
                  - z(Mismatch_Index)  # Skill alignment
```

**Hypothesis:** Declining efficiency → Structural labor issues → Rising LFI

**Status:** Not yet built - need mismatch proxy

---

#### 3. **Treasury Absorption Capacity Index**
**Components:**
- Primary dealer SLR headroom
- Foreign official holdings trend
- Stablecoin T-bill demand
- MMF asset growth

**Hypothesis:** When <30 capacity units → Term premium rises

**Status:** Partially built (Collateral Shortage Index) - needs formalization

---

#### 4. **Crypto-TradFi Linkage Stress Index**
**Components:**
- Stablecoin depegging events (count)
- Stablecoin supply growth volatility
- BTC correlation to Nasdaq (90-day rolling)
- Crypto liquidation volumes

**Hypothesis:** Rising linkage stress → BTC drawdowns precede equity vol

**Status:** Not yet built - need crypto data integration

---

#### 5. **AI CapEx Momentum Index**
**Components:**
- Mag 7 CapEx guidance YoY growth
- NVDA revenue growth
- Taiwan semi exports YoY
- Cloud infrastructure spending

**Hypothesis:** CapEx deceleration → NVDA/SMH underperformance in 6 months

**Status:** Not yet built - need quarterly CapEx data

---

## MONTHLY REVIEW CHECKLIST

**First Friday of Each Month:**

### 1. Performance Review
- [ ] Calculate Sharpe ratio of each indicator over past 30/90/180 days
- [ ] Identify false signals (MRI >+1σ but no SPX decline)
- [ ] Document regime shifts missed or caught
- [ ] Update indicator scoreboard

### 2. Calibration Check
- [ ] Review z-score distributions (should be ~N(0,1))
- [ ] Check for structural breaks in components
- [ ] Validate data quality (missing values, outliers)
- [ ] Confirm formulas still match documentation

### 3. Optimization Queue
- [ ] Add underperforming indicators to optimization backlog
- [ ] Prioritize by:
   - Client usage (how often referenced in chartbook?)
   - Predictive power decline
   - Ease of improvement

---

## QUARTERLY DEEP DIVE

**Every Quarter (Mid-Jan, Mid-Apr, Mid-Jul, Mid-Oct):**

### 1. Component Weight Optimization
- Run weight optimization for top 3 composite indicators
- Backtest proposed changes on 3-year rolling window
- Document results in `optimization_log_YYYYQ#.md`

### 2. New Indicator Development
- Build 1 new indicator from candidate list
- Validate on historical data
- Add to chartbook if passes quality bar

### 3. Decommissioning Review
- Identify indicators with consistently low predictive power
- Consider sunsetting or merging with others
- Maintain chartbook focus on **best 25 proprietary metrics**

---

## OPTIMIZATION LOG TEMPLATE

```markdown
# Indicator Optimization Log: [Indicator Name]
**Date:** YYYY-MM-DD
**Analyst:** Bob Sheehan

## Current State
- Formula: [current formula]
- Weights: [current weights]
- Window: [current window]
- Sharpe Ratio (trailing 1Y): [value]

## Proposed Changes
1. [Description of change]
2. [Rationale]

## Backt Results
| Metric | Current | Proposed | Improvement |
|--------|---------|----------|-------------|
| Sharpe Ratio | X.XX | X.XX | +X% |
| Max Drawdown | -X% | -X% | +X% |
| Win Rate | X% | X% | +X% |
| Correlation to SPX | X.XX | X.XX | +X% |

## Decision
- [ ] Implement changes
- [ ] Reject (insufficient improvement)
- [ ] Revisit in Q#

## Implementation Date
YYYY-MM-DD
```

---

## AUTOMATION

### Daily
- ✅ **Data refresh** (gather_all_chartbook_data.py)
- ✅ **Indicator calculation** (calculate_proprietary_indicators.py)
- ✅ **Chart generation** (generate_all_proprietary_charts.py)

**Run via:** `./daily_update.sh`

### Weekly (Every Friday)
- Generate full 50-chart chartbook PDF
- Review latest MRI, LCI, LFI, CLG values
- Flag any indicators >+2σ or <-2σ for commentary

### Monthly (First Friday)
- Run performance review checklist
- Update indicator scoreboard
- Document false signals

### Quarterly
- Weight optimization for top 3 indicators
- Build 1 new indicator
- Deep dive analysis

---

## INDICATOR SCOREBOARD (Updated Monthly)

| Indicator | Sharpe (30d) | Sharpe (90d) | Sharpe (180d) | Lead Time | Last Optimized | Next Review |
|-----------|--------------|--------------|---------------|-----------|----------------|-------------|
| MRI | ? | ? | ? | ? days | Never | 2026-Q1 |
| LCI | ? | ? | ? | ? days | Never | 2026-Q1 |
| LFI | ? | ? | ? | ? days | Never | 2026-Q1 |
| LDI | ? | ? | ? | ? days | Never | 2026-Q1 |
| CLG | ? | ? | ? | ? days | Never | 2026-Q1 |
| YFS | ? | ? | ? | ? days | Never | 2026-Q1 |
| SVI | ? | ? | ? | ? days | Never | 2026-Q1 |
| EMD | ? | ? | ? | ? days | Never | 2026-Q1 |

---

## SUCCESS METRICS

### Indicator Quality
- **Target Sharpe Ratio:** >1.0 for composite indicators
- **Lead Time:** 15-30 days for labor, 5-15 days for credit/equity
- **False Signal Rate:** <20% (indicator signals but no follow-through)

### Edge Preservation
- **Backtest Improvement:** Each optimization should yield >10% Sharpe improvement
- **Out-of-Sample Validation:** Must work on unseen data (2023-2025)
- **Client Value:** Indicators drive actionable insights in chartbook commentary

---

## NEXT STEPS (Immediate)

1. ✅ **Complete daily automation** - Done!
2. **Build optimization script** (`optimize_indicator_weights.py`)
3. **Create monthly scoreboard** (track indicator performance)
4. **Schedule Q1 2026 optimization** (January deep dive)

---

**This framework ensures your proprietary metrics stay sharp, predictive, and ahead of the market.**

**Continuous improvement = sustained edge.**
