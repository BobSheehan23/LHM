# LIGHTHOUSE MACRO: INDICATORS REFERENCE CARD
**Quick Reference for All Proprietary Indicators**

**Last Updated:** December 19, 2025

---

## MASTER COMPOSITE

### Macro Risk Index (MRI)

**Formula:**
```
MRI = LFI - LDI + YFS + z(HY_OAS) + EMD - LCI
```

**Components:**
- **LFI:** Labor Fragility Index
- **LDI:** Labor Dynamism Index
- **YFS:** Yield-Funding Stress
- **HY_OAS:** High-Yield Credit Spread (z-scored)
- **EMD:** Equity Momentum Divergence
- **LCI:** Liquidity Cushion Index

**Current Value:** +1.02

**Thresholds & Actions:**

| **MRI Range** | **Regime** | **Equity %** | **Bond %** | **Cash %** | **Action** |
|---------------|------------|--------------|------------|------------|------------|
| **< 0.0** | Low Risk | 65-70% | 25-30% | 0-5% | Overweight equities |
| **0.0 - 0.5** | Neutral | 55-60% | 35-40% | 0-5% | Strategic allocation |
| **0.5 - 1.0** | Elevated | 45-50% | 40-45% | 5-10% | Reduce beta, add quality |
| **1.0 - 1.5** | High Risk | 30-40% | 45-55% | 10-15% | Defensive stance |
| **> 1.5** | Extreme | 15-25% | 50-60% | 15-25% | Maximum defense |

**Historical Performance:**
- 100% precision in recession prediction (MRI >1.0)
- 67% recall (caught 2 of 3 recessions; missed 2020 exogenous shock)
- Average lead time: 9 months

---

## LABOR INDICATORS

### Labor Fragility Index (LFI)

**Purpose:** Early warning system for labor market deterioration

**Formula:**
```
LFI = Average( z(LongTermUnemployed%), z(-QuitsRate), z(-Hires/Quits) )
```

**Components (Equal-Weighted Z-Scores):**
1. Long-term unemployment percentage (27+ weeks / total unemployed)
2. Quits rate (inverted - lower = worse)
3. Hires-to-quits ratio (inverted - lower = deteriorating)

**Current Value:** +0.93 (elevated)

**Interpretation:**
- **LFI < 0.0:** Strong labor market
- **LFI 0.0 - 0.5:** Neutral
- **LFI 0.5 - 0.8:** Early weakness
- **LFI 0.8 - 1.2:** Elevated fragility (CURRENT)
- **LFI > 1.2:** Extreme fragility (recession imminent)

**Key Thresholds:**
- Quits rate <2.0% (current: 1.9% 🔴)
- LTU >22% of unemployed (current: 25.7% 🔴)
- Hires/Quits <1.1 (current: monitoring)

**Historical Performance:**
- Leads unemployment by 6-9 months
- Correlation with forward 6m unemployment: +0.65
- 100% precision, 67% recall on recessions

**Invalidation:**
- Quits rate rises above 2.1%
- LTU falls below 20%
- Hires surge above openings

---

### Labor Dynamism Index (LDI)

**Purpose:** Measures worker confidence and labor market churn

**Formula:**
```
LDI = Average( z(QuitsRate), z(JobToJobRate), z(VoluntaryDepartures/TotalSeparations) )
```

**Components:**
1. Quits rate (voluntary separations as % of employment)
2. Job-to-job transition rate (workers moving directly to new positions)
3. Voluntary departures / total separations ratio

**Current Value:** +0.15 (declining from +0.45 in Q2 2024)

**Thresholds:**
- **LDI > +0.5:** High dynamism (workers confident, job-hopping)
- **LDI +0.0 - +0.5:** Neutral (normal churn levels)
- **LDI -0.5 - 0.0:** Low dynamism (workers cautious)
- **LDI < -0.5:** Very low dynamism (workers scared to leave, pre-recessionary) 🚨

**Interpretation:**
- **High LDI:** Workers confident, leaving for better opportunities
- **Low LDI:** Workers cautious, hanging onto current jobs
- **Declining LDI:** Worker confidence deteriorating

**Role in MRI:** LDI appears with NEGATIVE sign (MRI = LFI - LDI + ...)
- Declining LDI = rising MRI = increased risk
- When LDI falls, workers lose confidence → labor market softening

**Historical Performance:**
- Lead time vs unemployment: 4-6 months
- Correlation with forward wage growth: +0.58
- Pre-2008 signal: LDI declined from +0.8 to -0.3 (18 months before peak unemployment)
- Pre-2020 signal: N/A (exogenous shock)

**Current Status:** LDI declining as quits rate falls to 1.9% and job-to-job transitions slow. This contributes to elevated MRI reading.

---

## LIQUIDITY INDICATORS

### Liquidity Cushion Index (LCI)

**Purpose:** Measures system's ability to absorb shocks without funding stress

**Formula:**
```
LCI = Average(z(RRP/GDP), z(Reserves/GDP))
```

**Current Value:** -0.8 (approaching scarce territory)

**Interpretation:**
- **LCI > 0.5:** Ample liquidity cushion
- **LCI 0.0 - 0.5:** Adequate
- **LCI -0.5 - 0.0:** Moderate
- **LCI -0.5 - -1.0:** Scarce (CURRENT)
- **LCI < -1.0:** Critically scarce

**Key Inputs:**
- **RRP:** $98B (down from $2.5T peak) 🔴
- **Bank Reserves:** ~$3.5T
- **GDP:** ~$29T

**Why It Matters:**
- RRP exhaustion = Treasury issuance drains reserves directly
- Low reserves = dealer balance sheet constraints
- Constrained dealers = funding stress → asset repricing

**Historical Performance:**
- Predicted 2019 repo spike 2 months early
- Correlation with VIX: -0.52 (low LCI → high VIX)
- 75% hit rate predicting SOFR-EFFR widening

**Watch Indicators:**
- SOFR-EFFR spread (current: 11 bps, watch >15 bps)
- SRF facility usage
- Repo fails (collateral scarcity)

---

## CREDIT INDICATORS

### Credit-Labor Gap (CLG)

**Purpose:** Identifies when credit markets ignore labor market reality

**Formula:**
```
CLG = z(HY_OAS) - z(LFI)
```

**Current Value:** -1.2 (credit complacent)

**Interpretation:**
- **CLG > +1.0:** Credit too loose vs labor (false positive risk)
- **CLG -0.5 - +0.5:** Aligned
- **CLG < -1.0:** Credit too tight vs labor = repricing likely (CURRENT)

**Why It Matters:**
- Labor leads credit by 3-6 months
- When labor deteriorates but credit stays tight → gap widens
- Gap >1.0 (absolute value) → credit repricing within 3-6 months

**Current Readings:**
- **LFI:** +0.93 (elevated labor fragility)
- **HY OAS:** ~300 bps (3rd percentile tightness since 2000)
- **Gap:** -1.2 (credit ignoring reality)

**Historical Performance:**
- Correlation with forward credit spread changes: +0.48
- Successfully identified credit complacency Q3 2024

**Invalidation:**
- Credit spreads widen to match labor signal (gap closes)
- Labor improves (LFI declines to match credit)

---

### HY OAS (High-Yield Option-Adjusted Spread)

**Purpose:** Credit risk premium over Treasuries

**Current Value:** ~300 bps

**Historical Context:**
- Average (2000-2025): ~500 bps
- Current percentile: 3rd (very tight)
- 2020 peak: 1,100 bps
- 2007 pre-crisis: 250 bps

**Interpretation:**
- <300 bps: Extremely tight (complacency) (CURRENT)
- 300-450 bps: Tight
- 450-600 bps: Neutral
- 600-800 bps: Wide (stress)
- >800 bps: Extreme stress

**Why It Matters:**
- Credit spreads price default risk
- Tight spreads = market pricing low recession probability
- When labor deteriorates but credit stays tight = mispricing

---

## FUNDING STRESS INDICATORS

### Yield-Funding Stress (YFS)

**Purpose:** Combines yield curve inversion with repo funding stress

**Components:**
1. 2s10s spread (yield curve slope)
2. SOFR-EFFR spread (repo stress)
3. Term premium

**Current Value:** +0.6 (moderate stress)

**Interpretation:**
- **YFS < 0.0:** Low stress
- **YFS 0.0 - 0.5:** Moderate
- **YFS 0.5 - 1.0:** Elevated (CURRENT)
- **YFS > 1.0:** High stress

**Key Inputs:**
- **2s10s curve:** -15 bps (inverted)
- **SOFR-EFFR:** 11 bps (up from 5 bps)
- **Term premium:** Rising

**Watch Thresholds:**
- SOFR-EFFR >15 bps sustained = funding stress escalating
- 2s10s >0 bps = curve steepening (Fed cutting)

---

### SOFR-EFFR Spread

**Current Value:** 11 bps (up from 5 bps last month)

**Interpretation:**
- <5 bps: Normal
- 5-10 bps: Slight elevation
- 10-15 bps: Moderate stress (CURRENT)
- >15 bps: Elevated stress (WATCH)
- >25 bps: Acute stress (crisis)

**Why It Matters:**
- SOFR = Secured Overnight Financing Rate (collateralized)
- EFFR = Effective Federal Funds Rate (uncollateralized)
- Spread widening = collateral becoming more valuable (scarcity signal)

---

## EQUITY INDICATORS

### Equity Momentum Divergence (EMD)

**Purpose:** Price vs trend deviation, volatility-adjusted

**Formula:**
```
EMD = (Price - MA50) / (ATR * MA50)
```
Where:
- MA50 = 50-day moving average
- ATR = Average True Range (volatility adjustment)

**Current Value:** Declining (exact value TBD)

**Interpretation:**
- **EMD > +1.0:** Strong uptrend (overbought risk)
- **EMD 0.0 - +1.0:** Uptrend
- **EMD -1.0 - 0.0:** Downtrend
- **EMD < -1.0:** Strong downtrend (oversold)

**Why It Matters:**
- Captures price momentum relative to trend
- Volatility adjustment prevents false signals during calm periods
- Works in MRI to identify when equities deviating from fundamentals

---

### S&P 500 Technical Levels

**Current Price:** ~6,100 (as of Dec 2025)

**Key Moving Averages:**
- **50-day MA:** ~6,050
- **200-day MA:** ~5,800

**Technical Invalidation:**
- 50d MA crosses below 200d MA = "death cross" (major bearish)
- Break below 200d MA = long-term trend break
- Loss of 5,800 support = accelerated downside

**Current Status:**
- Price above 50d and 200d MA (technically intact)
- Breadth deteriorating (narrow leadership)
- Valuation: 21x forward P/E (expensive)

---

## CROSS-ASSET CORRELATIONS

### Equity-Bond Correlation

**Current Value:** +0.15 (neutral)

**Interpretation:**
- **<-0.3:** Negative (bonds hedge equities) - normal regime
- **-0.3 - +0.3:** Neutral (CURRENT)
- **>+0.3:** Positive (diversification breaks) - risk-off regime

**Why It Matters:**
- Traditional 60/40 relies on negative correlation
- When correlation turns positive → diversification illusion breaks
- Action: >+0.3 sustained = reduce equity, add alternatives

**Historical Regimes:**
- 2000-2020: -0.4 average (bonds hedged equities)
- 2022: +0.6 (inflation regime, both fell)
- 2023-2024: -0.2 (normalized)

---

## COMPOSITE INDICATORS SUMMARY

**Current State (December 2025):**

| **Indicator** | **Value** | **Threshold** | **Status** | **Regime** |
|---------------|-----------|---------------|------------|------------|
| **MRI** | +1.02 | >1.0 | 🔴 High Risk | Defensive |
| **LFI** | +0.93 | >0.8 | 🔴 Elevated | Labor fragility |
| **LDI** | +0.15 | <-0.5 = stress | 🟠 Declining | Worker caution |
| **LCI** | -0.8 | <-0.5 | 🔴 Scarce | Thin cushion |
| **CLG** | -1.2 | \|Gap\| >1.0 | 🔴 | Credit complacent |
| **YFS** | +0.6 | >1.0 | 🟢 Moderate | Watch |
| **HY OAS** | ~300 | <350 | 🟠 Tight | Complacent |
| **SOFR-EFFR** | 11 bps | >15 | 🟢 | Watch closely |
| **EMD** | Declining | <0.0 | 🟠 | Weakening |

**Synthesis:** Four of nine indicators in red territory. MRI at +1.02 signals high risk regime. Defensive positioning appropriate.

---

## INVALIDATION CRITERIA (QUICK REFERENCE)

**Thesis invalidated if:**
1. MRI drops below +0.5 sustained (2+ months)
2. LFI drops below 0.0 (labor strengthening)
3. Quits rate rises above 2.1% (worker confidence returning)
4. Job openings surge above 8.5M (demand accelerating)
5. Fed announces emergency QE (plumbing backstop)
6. Credit spreads tighten to <250 bps HY OAS (extreme complacency)

**Technical invalidation if:**
1. S&P 500 50d MA crosses above 200d MA ("golden cross")
2. Breadth indicators strengthen (>60% stocks above 200d MA)
3. VIX drops below 12 sustained (complacency)

**If invalidated:**
- Exit defensive positions
- Reassess regime
- Potentially rotate to neutral/risk-on

---

## DATA SOURCES & UPDATE FREQUENCY

**Labor Data:**
- Source: BLS (JOLTS, Employment Situation)
- Frequency: Monthly
- Update: First Friday + 1 month lag

**Credit Data:**
- Source: FRED, Bloomberg
- Frequency: Daily
- Update: Real-time

**Liquidity Data:**
- Source: Federal Reserve (H.4.1 report)
- Frequency: Weekly (Thursday release)
- Update: Next day

**Market Data:**
- Source: Yahoo Finance, Bloomberg
- Frequency: Daily
- Update: Real-time

**LHM Dashboard:**
- Update: Daily at 7:00 ET (after data ingestion)
- Publication: Beacon (weekly), Beam (daily)

---

**Compiled by:** Bob Sheehan, CFA, CMT  
**For:** Indicator quick reference and thresholds  
***MACRO, ILLUMINATED.***
