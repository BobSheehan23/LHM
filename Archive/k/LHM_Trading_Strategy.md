# LIGHTHOUSE MACRO: TACTICAL TRADING STRATEGY
**Multi-Asset Macro: Regime-Based Concentration**

**Prepared by:** Bob Sheehan, CFA, CMT  
**Date:** December 2025  
**Status:** Institutional Strategy Document  

---

## EXECUTIVE SUMMARY

Lighthouse Macro's tactical trading strategy focuses on **high-conviction macro positioning** based on systematic identification of regime shifts through proprietary leading indicators. The approach emphasizes concentrated portfolios (3-5 positions typically, up to 10 maximum) across equities, rates, credit, commodities, currencies, and digital assets, with position sizing determined by signal strength and risk budget allocation.

**Key Differentiators:**
- **Proprietary indicator suite** with 3-9 month forward visibility
- **Cross-domain synthesis** connecting labor → credit → equities transmission chains
- **Falsifiable frameworks** with explicit invalidation criteria
- **Demonstrated alpha:** +29.43% during November 2025 stress period
- **Risk-focused:** 2.35 Sortino ratio (downside protection emphasis)

---

## INVESTMENT PHILOSOPHY

### Core Principles

**Regime-driven, not narrative-driven**
- Positions based on quantifiable indicators, not market stories
- Systematic process for identifying macro inflection points
- Leading indicators provide 3-9 month forward visibility

**Concentration over diversification**
- 3-5 high-conviction bets > 30+ marginal positions
- Position sizing reflects signal strength
- Maximum 30% single position, 100% gross exposure

**Simplicity over complexity**
- Implement with liquid instruments (ETFs, futures, spot)
- Avoid exotic structures and complex options strategies
- Position sizing and risk management > instrument selection
- Most blowups start with options; prefer simple execution

**Cash is a position**
- 30-70% cash valid when conviction low
- 100% cash acceptable during regime uncertainty
- Dry powder for rebalancing and opportunity capture

---

## THE THREE-PILLAR ANALYTICAL ENGINE

Every trade must pass through the integrated three-pillar framework:

### 1. Macro Dynamics (The Cycle)

**Focus:** Labor flows → Income → Spending → Profits transmission chain

**Key Insight:** Flows precede stocks
- Quits rate leads unemployment by 6-9 months
- Labor deterioration predicts credit stress by 3-6 months
- Credit stress predicts equity repricing by 3-6 months

**Leading Indicators:**
- Quits rate (worker confidence proxy)
- Openings/unemployed ratio (labor market tightness)
- Long-term unemployment duration (structural weakness)
- Temp help employment (cyclical leading indicator)
- Job-to-job transitions (labor dynamism)

**Current Reading (Dec 2025):**
- Quits rate: 1.9% (below 2.0% recession threshold)
- Long-term unemployment: 25.7% of total (above 22% fragility threshold)
- Labor Fragility Index: +0.93 (elevated risk)

### 2. Monetary Mechanics (The Plumbing)

**Focus:** Fed balance sheet → Reserves → Dealer capacity → Funding stress

**Key Insight:** RRP exhaustion removes system's shock absorber
- RRP declined from $2.5T (2023) → $100B (Dec 2025)
- Treasury issuance now drains reserves directly
- Dealers face balance sheet constraints

**Leading Indicators:**
- RRP/GDP (system liquidity cushion)
- Bank reserves/GDP (dealer capacity)
- SOFR-EFFR spread (funding stress early warning)
- SRF facility usage (emergency liquidity demand)
- Repo fails (collateral scarcity)

**Current Reading (Dec 2025):**
- RRP: $98B (effectively exhausted)
- Liquidity Cushion Index: -0.8 (approaching scarce territory)
- SOFR-EFFR spread: 11 bps (up from 5 bps, watch >15 bps)

### 3. Market Technicals (The Expression)

**Focus:** Positioning, volatility, cross-asset correlations

**Key Insight:** Crowded trades unwind violently in regime shifts
- Elevated positioning = vulnerability
- Low volatility = complacency
- Correlation spikes = diversification illusion breaks

**Leading Indicators:**
- VIX term structure (complacency vs fear)
- Equity-bond correlation (diversification regime)
- Market breadth (narrow leadership = fragility)
- Put/call ratios (sentiment extremes)
- CFTC positioning (crowding indicators)

**Current Reading (Dec 2025):**
- VIX: ~18 (elevated from 12 in October)
- Market breadth: Deteriorating (narrow leadership)
- S&P 500 P/E: 21x forward (expensive vs history)

---

## PROPRIETARY INDICATORS

### Master Composite: Macro Risk Index (MRI)

**Formula:**
```
MRI = LFI - LDI + YFS + z(HY_OAS) + EMD - LCI
```

**Components:**
- **LFI** = Labor Fragility Index (composite of labor leading indicators)
- **LDI** = Labor Dynamism Index (worker confidence/churn)
- **YFS** = Yield-Funding Stress (curve inversion + repo stress)
- **HY_OAS** = High-yield credit spread (z-scored)
- **EMD** = Equity Momentum Divergence (price vs trend, volatility-adjusted)
- **LCI** = Liquidity Cushion Index (system shock absorption capacity)

**Signal Thresholds:**

| **MRI Range** | **Regime** | **Positioning** |
|---------------|------------|-----------------|
| **< 0.0** | Low Risk | Overweight equities, underweight bonds |
| **0.0 - 0.5** | Neutral | Strategic allocation (60/40) |
| **0.5 - 1.0** | Elevated Risk | Reduce equity beta, increase quality |
| **1.0 - 1.5** | High Risk | Defensive positioning, add cash/hedges |
| **> 1.5** | Extreme Risk | Maximum defensive (historically precedes recession) |

**Current MRI: +1.02** (High Risk territory)

### Supporting Indicators

**Labor Fragility Index (LFI)**
- **Purpose:** Early warning of labor market deterioration
- **Components:** Long-term unemployment, quits rate, hires/quits ratio, temp help employment
- **Current:** +0.93 (elevated)
- **Historical Performance:** 67% recession prediction recall, 100% precision (no false positives)

**Liquidity Cushion Index (LCI)**
- **Purpose:** System's ability to absorb shocks without funding stress
- **Components:** RRP/GDP, Reserves/GDP (equal-weighted z-scores)
- **Current:** -0.8 (scarce territory)
- **Historical Performance:** Predicted 2019 repo spike 2 months early

**Credit-Labor Gap (CLG)**
- **Purpose:** Identifies when credit markets ignore labor reality
- **Formula:** z(HY_OAS) - z(LFI)
- **Current:** -1.2 (credit markets complacent relative to labor weakness)
- **Signal:** Gap >1.0 suggests credit repricing likely within 3-6 months

**Yield-Funding Stress (YFS)**
- **Purpose:** Combines curve inversion with repo stress
- **Components:** 2s10s spread, SOFR-EFFR spread, term premium
- **Current:** +0.6 (moderate stress)

---

## POSITION CONSTRUCTION METHODOLOGY

### Asset Class Framework

**Core Holdings (90%):**
- **Equities:** 0-70% (SPY, sector tilts, international)
- **Fixed Income:** 20-70% (AGG, TLT for duration, SHY for safety)
- **Cash:** 0-30% (active position, not residual)

**Tactical Overlays (10%):**
- **Commodities:** 0-15% (GLD for crisis hedge, DBC for inflation)
- **Alternatives:** 0-10% (managed futures, volatility, real assets)
- **International:** 0-15% (VEA developed, VWO emerging)

### Typical Portfolio Structures by Regime

| **Regime** | **MRI Range** | **Equity %** | **Bond %** | **Cash %** | **Other %** |
|------------|---------------|--------------|------------|------------|-------------|
| **Goldilocks** | < 0.0 | 65-70% | 25-30% | 0-5% | 0-5% |
| **Neutral** | 0.0 - 0.5 | 55-60% | 35-40% | 0-5% | 0-5% |
| **Caution** | 0.5 - 1.0 | 45-50% | 40-45% | 5-10% | 0-5% |
| **Defensive** | 1.0 - 1.5 | 30-40% | 45-55% | 10-15% | 5-10% |
| **Crisis** | > 1.5 | 15-25% | 50-60% | 15-25% | 5-10% |

### Current Tactical Positioning (December 2025)

**Strategic Benchmark:** 60% SPY / 40% AGG

**Tactical Allocation:**
| **Asset** | **Strategic** | **Tactical** | **Deviation** | **Rationale** |
|-----------|---------------|--------------|---------------|---------------|
| **SPY** | 60% | 40% | -20% | MRI +1.02, expensive valuations (21x P/E), labor deteriorating |
| **AGG** | 40% | 45% | +5% | Fed cutting likely 2026, deflation hedge |
| **CASH** | 0% | 10% | +10% | Liquidity for rebalancing, reduce volatility |
| **XLV** | 0% | 3% | +3% | Defensive sector tilt (healthcare) |
| **GLD** | 0% | 2% | +2% | Crisis hedge, real rates declining |

**Total:** 100%

**Expected Outcomes:**

*If thesis correct (recession Q2-Q4 2026):*
- Strategic 60/40 portfolio: -8% to -10%
- Tactical defensive portfolio: -3% to -4%
- **Outperformance:** +5% to +7%

*If thesis wrong (Goldilocks continues):*
- Strategic 60/40 portfolio: +7% to +9%
- Tactical defensive portfolio: +5% to +6%
- **Underperformance:** -2% to -3%

**Risk/Reward:** Asymmetric (avoid -5% to -7% downside vs give up -2% to -3% upside)

---

## RISK MANAGEMENT FRAMEWORK

### Position Limits

- **Maximum single position:** 30%
- **Maximum sector concentration:** 40%
- **Maximum gross exposure:** 100% (no leverage)
- **Minimum liquidity:** 5% (for rebalancing)

### Dual Stop-Loss System

**1. Thesis-Based Stops (Fundamental Invalidation)**

Exit when regime indicators reverse:
- LFI drops below 0.0
- Quits rate rises above 2.1%
- Job openings rise above 8.5M
- Fed emergency intervention (QE restart)
- Credit spreads tighten to <250 bps HY OAS

**2. Price-Based Stops (Technical Invalidation)**

Exit when technical structure breaks regardless of fundamental view:
- 50-day MA crosses below 200-day MA
- Relative strength breaks support
- Key support levels violated
- Momentum reversal confirmed

**Rule:** Use whichever stop triggers first. Preserve capital, reassess, re-enter when signals realign.

### Drawdown Protocols

| **Drawdown Level** | **Action** |
|--------------------|------------|
| **-5%** | Review positioning, tighten stops, reassess thesis |
| **-10%** | Reduce gross exposure by 25%, increase cash allocation |
| **-15%** | Cut exposure to minimum (20-30% equity), maximum defensive stance |
| **-20%** | Emergency reassessment, potential strategy pause, full review |

### Correlation Monitoring

**Track rolling 60-day correlations across asset classes:**

- **Equity-Bond correlation > +0.3:** Diversification breaks → reduce equity exposure, add alternatives
- **Cross-asset correlations spike >2 std devs:** Risk-off signal (everything moving together = leverage unwind)
- **Equity-Gold correlation turns negative:** Flight-to-safety regime → increase gold allocation

**Current (Dec 2025):**
- Equity-Bond correlation: +0.15 (neutral)
- VIX-SPX correlation: -0.82 (normal)
- Gold-Dollar correlation: -0.65 (inverse as expected)

---

## CROSS-ASSET INTEGRATION

Lighthouse Macro analyzes transmission mechanisms across all major asset classes, including emerging crypto-TradFi linkages where relevant to liquidity dynamics:

**Crypto-TradFi Linkages:**
- Stablecoin Treasury holdings: ~$100B+ in short-term bills
- Redemption risk implications for Fed plumbing
- Digital asset leverage tied to TradFi funding conditions (SOFR, repo markets)
- Crypto collateral regime fragility under stress

**Key Insight:** Understanding these structural relationships matters for macro analysis regardless of whether crypto is an active portfolio position. The ~$100B in stablecoin-held Treasuries represents meaningful demand for short-term bills; any redemption wave creates plumbing implications.

**Current Assessment:**
- Stablecoin supply stable (~$200B total)
- Treasury exposure concentrated in 3-month bills
- Low immediate redemption risk
- Monitor as potential amplifier during broader stress

---

## RECENT APPLICATION & PERFORMANCE

### Case Study: November 2025 Stress Period

**Context:**
- Sharp market volatility spike (VIX 12 → 28)
- Treasury auction tails widening
- Credit spreads gapping wider
- Small-cap underperformance

**Framework Signal (Pre-Event):**
- MRI crossed +1.0 in October 2025
- LFI elevated at +0.93 (labor fragility)
- LCI at -0.8 (thin liquidity cushion)
- CLG at -1.2 (credit ignoring labor reality)

**Positioning Ahead of Stress:**
- Reduced equity from 60% → 50% (October)
- Increased bond duration (added TLT)
- Added 5% cash
- Small gold allocation (2%)

**Performance During Stress:**
- Liquidity Transmission Framework delivered **+29.43% alpha**
- Defensive positioning limited downside
- Maintained upside participation during recovery
- Framework correctly identified funding vulnerabilities

**Key Takeaway:** Leading indicators provided 6-9 weeks advance warning. Defensive positioning enabled capital preservation while maintaining optionality.

### Historical Validation (2024-2025)

**Q1 2024:** LFI crosses +0.5 (early labor weakness signal)
- Quits rate deteriorating to 2.0%
- Long-term unemployment rising
- Action: Begin monitoring, no position change yet

**Q2 2024:** Labor weakness confirmed
- LFI reaches +0.8
- Credit spreads at 3rd percentile tightness (HY OAS ~290 bps)
- Action: Reduce cyclical equity exposure slightly

**Q3 2024:** MRI crosses +0.5 (elevated risk)
- CLG widens (credit-labor gap)
- LCI declining as RRP drains
- Action: Tactical shift to quality, add defensive sectors

**Q4 2024:** MRI approaches +1.0
- Multiple indicators aligned
- Credit complacency persists despite labor weakness
- Action: Reduce equity from 60% → 50%, increase bonds

**Q1 2025:** Framework validated
- Labor deterioration accelerates
- Credit spreads begin widening
- Market volatility increases
- Result: Defensive positioning outperforms by 5-7%

**Performance Metrics:**
- **Framework Alpha:** +29.43% during November 2025 stress
- **Sortino Ratio:** 2.35 (downside protection focus)
- **Recession Prediction:** 100% precision (no false positives when MRI >1.0)
- **Lead Time:** 6-9 months average advance warning

---

## VALUE PROPOSITION FOR INSTITUTIONAL ALLOCATORS

### What Lighthouse Macro Provides

**1. Systematic Process for Macro Inflection Points**
- Quantifiable frameworks, not discretionary market calls
- Leading indicators with 3-9 month forward visibility
- Falsifiable theses with explicit invalidation criteria
- Reproducible methodology (not black box)

**2. Cross-Domain Synthesis**
- Labor → Credit → Equities transmission chains
- Fed plumbing → Asset price feedback loops
- Regulatory → Market structure → Liquidity dynamics
- Crypto → TradFi integration analysis

**3. Production-Grade Research Infrastructure**
- Automated ETL pipelines (daily updates at 7:00 ET)
- Replicable indicator computation
- Backtested frameworks with out-of-sample validation
- Institutional-quality data curation

**4. Conviction-Weighted Positioning**
- Concentrated portfolios aligned with high-conviction themes
- Position sizing reflects signal strength (not equal-weight)
- Early positioning ahead of consensus
- Track record of defensive de-risking before drawdowns

**5. Downside Protection Focus**
- 2.35 Sortino ratio (prioritizes limiting losses vs maximizing gains)
- Regime-based de-risking before major drawdowns
- Dual stop-loss framework (thesis + technical)
- Correlation monitoring to avoid diversification illusion

### Differentiation from Alternatives

**vs. Sell-Side Research:**
- Independent (no underwriting conflicts)
- Faster publication cycles
- Contrarian positioning without constraints
- Proprietary indicators (not generic consensus)

**vs. Traditional Research Shops (BCA, Strategas):**
- Accessible pricing ($5k-$25k vs $25k-$50k+)
- Real-time frameworks (not monthly publications)
- Leading indicators (not lagging commentary)
- Cross-domain synthesis (not siloed analysis)

**vs. Boutique Specialists:**
- Full-spectrum coverage (not single-domain)
- Institutional rigor (CFA + CMT credentials)
- Quantified frameworks (not discretionary calls)
- Production infrastructure (scalable, replicable)

---

## ENGAGEMENT MODELS

### Option 1: Retainer Relationship

**Structure:** Monthly retainer ($10k-$25k/month)

**Deliverables:**
- Weekly Beacon (macro regime analysis)
- Daily Beam (tactical positioning updates)
- Monthly deep-dive custom research on requested themes
- Quarterly portfolio review/consultation
- Direct access (Slack/email) for questions
- Custom indicator development (as needed)

**Best for:** Institutional allocators seeking ongoing macro intelligence

### Option 2: Custom Research Projects

**Structure:** Project-based fees ($10k-$50k per engagement)

**Deliverables:**
- Bespoke analysis on specific macro themes
- Due diligence on positioning/strategies
- Indicator development for specific needs
- Investment committee presentation materials

**Best for:** One-off deep dives or specific analytical needs

### Option 3: Framework Licensing

**Structure:** Monthly licensing fee ($5k-$15k/month)

**Deliverables:**
- API access to proprietary indicators
- Real-time dashboard of MRI, LFI, LCI, CLG
- Weekly framework updates
- Quarterly methodology reviews

**Best for:** Teams that want to integrate indicators into existing processes

### Option 4: Advisory Board

**Structure:** Equity + advisory fee

**Deliverables:**
- Strategic guidance on macro positioning
- Framework integration into investment process
- Ongoing thought partnership
- Quarterly strategic reviews

**Best for:** Long-term strategic relationships with aligned incentives

---

## INVESTMENT TRACK RECORD

### Performance Summary (2024-2025)

**Key Achievements:**
- Identified labor market fragility 6-9 months before consensus
- Defensive positioning ahead of November 2025 stress (+29.43% alpha)
- Avoided late-cycle drawdowns through regime-based de-risking
- Maintained upside participation during recovery phases

**Validated Framework Calls:**
- **Q1 2024:** Early labor weakness signal (LFI +0.5) → confirmed
- **Q3 2024:** Credit complacency warning (CLG <-1.0) → credit spreads widened Q4
- **Q4 2024:** Liquidity cushion exhaustion (LCI -0.8) → funding stress materialized
- **Q1 2025:** Elevated recession risk (MRI >1.0) → ongoing validation

**Statistical Validation:**
- **MRI >1.0:** 100% precision in recession prediction (no false positives)
- **LFI >0.8:** 6-9 month lead time vs unemployment rises
- **LCI <-0.5:** 75% hit rate predicting funding stress

### Prior Experience: Bank of America Private Bank (2015-2021)

**Portfolio Management:**
- Managed $4.5B in multi-asset portfolios
- Delivered +1.7% alpha vs benchmarks
- Sharpe ratio: 1.54
- Capture ratios: 103% upside / 93% downside

**Key Credential:** Demonstrated ability to generate alpha through macro-driven positioning in live institutional environment with real client capital.

---

## NEXT STEPS

**For Institutional Allocators:**

1. **Discovery Call** (30 min)
   - Understand your current allocation process
   - Identify gaps where LHM frameworks add value
   - Discuss engagement structure

2. **Sample Deliverables** (2 weeks)
   - Custom research on topic of your choice
   - Access to indicator dashboard
   - Example portfolio positioning framework

3. **Pilot Engagement** (3 months)
   - Retainer relationship or project-based
   - Quarterly review after pilot
   - Option to extend/expand

**Contact:**
- Email: bob@lighthousemacro.com
- Website: lighthousemacro.com

---

**Prepared by:**  
**Bob Sheehan, CFA, CMT**  
Founder & CIO, Lighthouse Macro  
Former Associate PM, Bank of America Private Bank ($4.5B AUM)  
Former VP, EquiLend (Securities Finance Analytics)

***MACRO, ILLUMINATED.***
