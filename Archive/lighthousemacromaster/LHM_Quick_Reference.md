# LIGHTHOUSE MACRO: QUICK REFERENCE GUIDE
**Condensed Framework & Indicator Reference**  
**Version:** 3.0  
**Date:** December 19, 2025  
**Bob Sheehan, CFA, CMT**

---

## I. THE CORE FRAMEWORK (ONE-PAGE OVERVIEW)

### Three-Pillar System

```
┌─────────────────────────────────────────────────────────────┐
│  MACRO DYNAMICS          MONETARY MECHANICS    MARKET TECH  │
│  (The Cycle)             (The Plumbing)       (Expression)   │
├─────────────────────────────────────────────────────────────┤
│  Labor → Income →        Fed BS → Reserves →  Positioning →  │
│  Spending → Profits      Dealers → Funding    Vol → Prices   │
│                                                               │
│  Leading: Quits, LTU     Leading: RRP, SOFR   Leading: VIX,  │
│  Lagging: Unemployment   Lagging: Credit      Breadth        │
└─────────────────────────────────────────────────────────────┘
                            ↓
                     MRI SYNTHESIS
                            ↓
                  TACTICAL POSITIONING
```

### Macro Risk Index (MRI) - Master Signal

**Formula:** `MRI = LFI - LDI + YFS + z(HY_OAS) + EMD - LCI`

**Signal Thresholds:**
- **MRI < 0.0:** Risk-on → 65-70% equities
- **MRI 0.0-0.5:** Neutral → 55-60% equities
- **MRI 0.5-1.0:** Caution → 45-50% equities
- **MRI 1.0-1.5:** Defensive → 30-40% equities + cash
- **MRI > 1.5:** Crisis → 20-30% equities + hedges

**Current: MRI = +1.1 (HIGH RISK - Defensive)**

---

## II. INDICATOR CHEAT SHEET

### Labor Fragility Index (LFI)

**What it measures:** Early warning of labor market deterioration

**Components:**
```
LFI = Avg( z(LongTermUnemployed%), z(-QuitsRate), z(-Hires/Quits) )
```

**Key Thresholds:**
- **Quits Rate:**
  - >2.1% = Healthy
  - 2.0-2.1% = Neutral
  - <2.0% = Pre-recessionary ⚠️
  
- **Long-Term Unemployed:**
  - <20% = Healthy
  - 20-22% = Neutral
  - >22% = Fragility ⚠️

- **Hires/Quits Ratio:**
  - >2.0 = Healthy
  - 1.5-2.0 = Neutral
  - <1.5 = Weak demand ⚠️

**LFI Interpretation:**
- <0: Healthy
- 0-0.5: Softening
- 0.5-1.0: Fragility (reduce cyclical) ⚠️
- >1.0: Severe (recession risk high) 🚨

**Current: LFI = +0.93 (Elevated)**

### Liquidity Cushion Index (LCI)

**What it measures:** System's ability to absorb shocks

**Components:**
```
LCI = Avg( z(RRP/GDP), z(Reserves/GDP) )
```

**Key Levels:**
- **RRP:**
  - >$1T = Ample buffer
  - $500B-$1T = Adequate
  - $100-500B = Thin ⚠️
  - <$100B = Exhausted 🚨

- **SOFR-EFFR Spread:**
  - <5 bps = Normal
  - 5-10 bps = Monitoring
  - 10-15 bps = Early stress ⚠️
  - >15 bps = Elevated stress 🚨

**LCI Interpretation:**
- >0: Ample liquidity
- 0 to -0.5: Tightening
- -0.5 to -1.0: Thin (funding risk) ⚠️
- <-1.0: Scarce (crisis risk) 🚨

**Current: LCI = -0.8 (Thin buffer)**

### Credit-Labor Gap (CLG)

**What it measures:** Whether credit markets ignore labor reality

**Formula:**
```
CLG = z(HY_OAS) - z(LFI)
```

**Interpretation:**
- **CLG > +1.0:** Credit too tight vs labor (complacency) → Add credit hedges
- **CLG -1.0 to +1.0:** Aligned
- **CLG < -1.0:** Credit too wide vs labor (overshooting) → Bargains

**Current: CLG = -1.2 (Credit complacent)**

---

## III. DECISION RULES (QUICK REFERENCE)

### Entry Signals: When to Reduce Risk

**Risk-Off Checklist (Need 3+ Yes):**
- [ ] LFI > +0.8 (labor fragility)
- [ ] CLG < -1.0 (credit complacent)
- [ ] LCI < -0.5 (thin liquidity)
- [ ] SOFR-EFFR > 10 bps (funding stress)
- [ ] VIX rising from <15 (complacency breaking)
- [ ] Breadth deteriorating (A/D line diverging)
- [ ] Defensive sectors outperforming

**If 3+ triggered → Reduce equity by 10-20%**

### Exit Signals: When to Add Risk

**Risk-On Checklist (Need 3+ Yes):**
- [ ] LFI drops below +0.5 (labor stabilizing)
- [ ] Quits rate > 2.1% (confidence returning)
- [ ] LCI rises above -0.5 (liquidity improving)
- [ ] SOFR-EFFR < 8 bps (funding normalizing)
- [ ] VIX declining (fear subsiding)
- [ ] Breadth improving (participation widening)
- [ ] Cyclical sectors leading

**If 3+ triggered → Increase equity by 10-20%**

### Stop-Loss Rules

**Thesis-Based Stops (Fundamental):**
- LFI drops below 0.0 → Exit defensive
- Quits rate > 2.1% → Exit defensive
- Fed emergency intervention → Reassess
- Credit spreads > 500 bps → Stress priced

**Price-Based Stops (Technical):**
- 50-day MA crosses below 200-day → Exit
- Position down -10% → Reassess
- Relative strength breaks → Rotate

**Rule: Exit on FIRST stop triggered**

---

## IV. TACTICAL ALLOCATION MATRIX

| **Regime** | **MRI** | **Equity** | **Bonds** | **Cash** | **Other** | **Example Tilt** |
|-----------|---------|-----------|----------|----------|----------|------------------|
| **Goldilocks** | <0.0 | 65-70% | 25-30% | 0-5% | 0-5% | Overweight cyclicals |
| **Neutral** | 0.0-0.5 | 55-60% | 35-40% | 0-5% | 0-5% | Strategic allocation |
| **Caution** | 0.5-1.0 | 45-50% | 40-45% | 5-10% | 0-5% | Add quality, reduce beta |
| **Defensive** | 1.0-1.5 | 30-40% | 45-55% | 10-15% | 5-10% | Defensive sectors, gold |
| **Crisis** | >1.5 | 20-30% | 50-60% | 15-25% | 5-10% | Max defense, tail hedges |

**Current (Dec 2025): MRI = +1.1 → DEFENSIVE**
- Equity: 40% (SPY)
- Bonds: 45% (AGG)
- Cash: 10% (SGOV)
- Defensive: 3% (XLV)
- Gold: 2% (GLD)

---

## V. KEY DATA SOURCES & UPDATE SCHEDULE

### Daily Updates (06:00 ET)

**Market Data:**
- S&P 500, Treasury yields (10Y, 2Y)
- HY OAS, BBB OAS spreads
- VIX, volatility metrics
- SOFR, EFFR rates

**Fed Plumbing:**
- ON RRP balance
- Bank reserves
- Fed balance sheet
- SRF usage (if any)

### Monthly Updates (First Friday, 08:30 ET)

**Labor Data:**
- Nonfarm payrolls (headline unemployment)
- JOLTS: Quits, hires, openings, layoffs
- Duration metrics (weeks unemployed)
- Temp help employment

**Derived Indicators:**
- LFI recalculated
- MRI updated
- CLG refreshed

### Quarterly Reviews

**Indicator validation:**
- Backtest performance
- Correlation stability
- False signal analysis
- Methodology refinement

---

## VI. CURRENT MARKET VIEW (ONE-PAGE)

### December 2025 Snapshot

**Labor Market:**
- Quits: 1.9% 🚨 (below 2.0% threshold)
- LTU: 25.7% 🚨 (above 22% threshold)
- **Signal:** Fragility developing

**Fed Plumbing:**
- RRP: ~$100B 🚨 (exhausted)
- SOFR-EFFR: 11 bps ⚠️ (widening)
- **Signal:** Thin liquidity buffer

**Credit Markets:**
- HY OAS: ~300 bps (3rd percentile tight)
- CLG: -1.2 🚨 (complacent)
- **Signal:** Ignoring labor reality

**Equity Markets:**
- S&P 500: 21x P/E (expensive)
- Breadth: Deteriorating
- **Signal:** Limited upside, vulnerable

### Synthesis: Phase 3 Stress

**MRI = +1.1 (HIGH RISK)**

**Base Case (60% probability):**
- Recession Q4 2026
- Credit spreads widen 300 → 500 bps
- S&P 500 declines -15% to -20%
- Fed cuts 150-200 bps

**Bull Case (25% probability):**
- Soft landing achieved
- Labor stabilizes, quits rise
- Goldilocks continues

**Bear Case (15% probability):**
- Recession pulls forward to Q2 2026
- Credit stress accelerates
- S&P 500 declines >25%

**Positioning:** Defensive (40% equity / 45% bonds / 15% cash+other)

---

## VII. RISK MANAGEMENT CHECKLIST

### Portfolio Limits

- [ ] No single position >30%
- [ ] No sector concentration >40%
- [ ] Gross exposure ≤100% (no leverage)
- [ ] Minimum 5% liquidity for rebalancing

### Monitoring Checklist (Daily)

- [ ] MRI calculation updated
- [ ] LFI within expected range
- [ ] LCI not breaching -1.0
- [ ] SOFR-EFFR spread not >15 bps
- [ ] VIX not spiking >30
- [ ] No position stop-loss triggered

### Rebalancing Triggers

- [ ] Quarterly calendar (Q1, Q2, Q3, Q4)
- [ ] Any position drifts >5% from target
- [ ] MRI crosses threshold (±0.5)
- [ ] Thesis or price stop triggered

### Drawdown Response

- [ ] -5%: Review positioning, tighten stops
- [ ] -10%: Reduce exposure 25%, increase cash
- [ ] -15%: Cut to minimum (20-30% equity)
- [ ] -20%: Emergency reassessment, strategy pause

---

## VIII. COMMUNICATION STANDARDS

### Publication Formats

**Weekly Beacon (200-400 words):**
- Single theme
- Data point → mechanism → signpost
- Example: "RRP closed at $98B yesterday. The buffer's gone."

**Daily Beam (800-1,200 words):**
- Setup → Signal → Transmission → Playbook → Bottom Line
- 2-3 charts
- Specific positioning + invalidation

**Monthly Horizon (3,000-5,000 words):**
- Comprehensive regime analysis
- All three pillars
- 8-12 charts
- Full positioning guide

### The 60/40/0 Rule

- 60% Institutional Rigor (quantified, falsifiable)
- 40% Real Bob (clear, dry humor)
- 0% Corporate Fluff (no hedging)

### Banned Phrases

❌ "Cautiously optimistic"
❌ "Complex constellation of factors"
❌ "In our view" (obviously your view)
❌ "Going forward" / "It appears that"

### Signature Sign-Off

**Every publication ends with:**
> "That's our view from the Watch. We'll keep the light on."
> 
> ***MACRO, ILLUMINATED.***

---

## IX. PROPRIETARY COLOR PALETTE

**Official 8-Color System:**

1. **Ocean Blue (#0089D1):** Primary series, bullish signals
2. **Dusk Orange (#FF6723):** Warnings, secondary emphasis
3. **Electric Cyan (#00FFFF):** Volatility, high-energy
4. **Hot Magenta (#FF2389):** Critical alerts, extreme readings
5. **Teal Green (#00BB99):** Secondary series, stable metrics
6. **Neutral Gray (#D3D6D9):** Backgrounds, reference lines
7. **Lime Green (#00FF00):** Extreme bullish/overbought
8. **Pure Red (#FF0000):** Crisis zones, recession signals

**Chart Standards:**
- No gridlines
- Clean spines
- Right-axis primary
- Annotate inflections, not noise

---

## X. CONTACT & RESOURCES

### For Institutional Inquiries

**Retainer Relationships:** $5k-$25k/month
**Custom Research:** $10k-$50k/project
**Advisory Roles:** Negotiable (equity + cash)

### For Subscription Access

**Launch:** Q1 2026
**Founding Member:** $500/year
**Professional:** $2,500/year

### Resources

**Website:** lighthousemacro.com
**Email:** [Contact]
**Phone:** [Contact]

---

## XI. APPENDIX: QUICK FORMULAS

### Key Indicators

```python
# Labor Fragility Index
LFI = np.mean([
    zscore(long_term_unemployed_pct),
    zscore(-quits_rate),
    zscore(-hires_to_quits_ratio)
])

# Liquidity Cushion Index
LCI = np.mean([
    zscore(rrp / gdp),
    zscore(reserves / gdp)
])

# Macro Risk Index
MRI = LFI - LDI + YFS + zscore(hy_oas) + EMD - LCI

# Credit-Labor Gap
CLG = zscore(hy_oas) - zscore(LFI)
```

### Z-Score Calculation

```python
def zscore(series, window=252):
    """
    Rolling z-score (1-year window default)
    """
    mean = series.rolling(window).mean()
    std = series.rolling(window).std()
    return (series - mean) / std
```

---

**That's our view from the Watch. We'll keep the light on.**

***MACRO, ILLUMINATED.***

---

*This quick reference guide provides condensed access to Lighthouse Macro's core frameworks and decision rules. For comprehensive analysis and domain expertise, refer to the complete Lighthouse Macro Master Document.*

**— Bob Sheehan, CFA, CMT**  
**Founder & CIO, Lighthouse Macro**  
**December 2025**
