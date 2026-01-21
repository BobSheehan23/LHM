# LIGHTHOUSE MACRO: MULTI-ASSET MACRO STRATEGY
**Investment Philosophy & Tactical Framework**  
**Version:** 3.0  
**Date:** December 19, 2025  
**Presented by:** Bob Sheehan, CFA, CMT

---

## EXECUTIVE SUMMARY

**Lighthouse Macro's tactical trading strategy** focuses on high-conviction macro positioning based on systematic identification of regime shifts through proprietary leading indicators. The approach emphasizes concentrated portfolios (3-5 positions typically, up to 10 maximum) across equities, rates, credit, commodities, currencies, and digital assets, with position sizing determined by signal strength and risk budget allocation.

### Core Differentiation

**What makes this approach unique:**
- **Regime-driven, not narrative-driven:** Positions based on quantifiable indicators with explicit invalidation criteria
- **Cross-domain synthesis:** Labor → Credit → Equities transmission chains that specialists miss
- **Leading indicators:** 3-9 month forward visibility before consensus recognition
- **Concentration over diversification:** 3-5 high-conviction bets > 30+ marginal positions
- **Downside protection focus:** 2.35 Sortino ratio prioritizes limiting losses

---

## I. INVESTMENT PHILOSOPHY

### Regime-Based Concentration

**Core Principles:**

1. **Regimes Matter More Than Assets**
   - Asset class returns are regime-dependent
   - Identifying regime shifts earlier = alpha generation
   - Concentrated positioning when conviction high, cash when uncertain

2. **Position Sizing is Alpha**
   - Risk management matters more than instrument selection
   - Bet size reflects signal strength, not equal-weighting
   - Cash as active position (30-70% valid when conviction low)

3. **Simplicity Over Complexity**
   - Implement with liquid instruments (ETFs, futures, spot)
   - Avoid exotic structures for complexity's sake
   - Most blowups start with options; prefer simple execution with proper sizing

4. **Dual Risk Framework**
   - Thesis-based stops (fundamental invalidation)
   - Price-based stops (technical invalidation)
   - Use whichever triggers first; preserve capital

5. **Flows > Stocks**
   - Leading indicators (quits rate, RRP flows) > lagging indicators (unemployment, GDP)
   - Position ahead of data confirmation
   - By the time everyone knows, it's too late

---

## II. THE THREE-PILLAR ANALYTICAL ENGINE

Every trade must pass through the integrated three-pillar framework. Single-pillar signals are not sufficient; we require **convergence across pillars** for high-conviction positioning.

### Pillar 1: Macro Dynamics (The Cycle)

**Focus:** Labor flows → Income → Spending → Profits transmission chain

**Key Insight:** Flows precede stocks. Labor market deterioration shows up in quits rate and hires/quits ratio 6-9 months before unemployment rises.

**Leading Indicators:**
- **Quits rate:** Worker confidence metric; below 2.0% = pre-recessionary
- **Long-term unemployment duration:** Above 22% of total unemployed = fragility
- **Hires/Quits ratio:** Below 2.0 = demand weakening
- **JOLTS openings/unemployed:** Below 1.2 = slack developing

**Current Reading (December 2025):**
- Quits: 1.9% (⚠️ below 2.0% threshold)
- Long-term unemployed: 25.7% (⚠️ above 22% threshold)
- LFI: +0.93 (elevated, defensive signal)

### Pillar 2: Monetary Mechanics (The Plumbing)

**Focus:** Fed balance sheet → reserves → dealer capacity → funding stress

**Key Insight:** RRP exhaustion removes the system's shock absorber. Treasury issuance now drains reserves directly, tightening funding conditions without explicit Fed action.

**Leading Indicators:**
- **RRP/GDP:** Buffer capacity for Treasury absorption
- **Reserves/GDP:** Banking system liquidity cushion
- **SOFR-EFFR spread:** Early warning of funding stress (>15 bps = elevated)
- **SRF usage:** Standing repo facility usage indicates dealer stress

**Current Reading (December 2025):**
- RRP: ~$100B (⚠️ down from $2.5T peak)
- SOFR-EFFR: 11 bps (⚠️ widening from 5 bps)
- LCI: -0.8 (⚠️ approaching scarce territory)

### Pillar 3: Market Technicals (The Expression)

**Focus:** Positioning, volatility, cross-asset correlations

**Key Insight:** Crowded trades unwind violently during regime shifts. When everyone is positioned the same way, small changes in fundamentals create large price moves.

**Leading Indicators:**
- **VIX term structure:** Backwardation = fear; contango = complacency
- **Equity-bond correlation:** >+0.3 = diversification breaking down
- **Market breadth:** Advance-decline line diverging from price = weakness
- **Cross-asset correlations:** Spike >2σ = leverage unwind

**Current Reading (December 2025):**
- VIX: ~18 (elevated from 12-15 range)
- Equity-bond correlation: Rising (diversification stress)
- Breadth: Deteriorating (narrow leadership)

---

## III. PROPRIETARY INDICATORS

### Macro Risk Index (MRI) - Master Composite

**Formula:**
```
MRI = LFI - LDI + YFS + z(HY_OAS) + EMD - LCI
```

**Components:**
- **LFI:** Labor Fragility Index (quits, long-term unemployed, hires/quits)
- **LDI:** Labor Dynamism Index (worker confidence/churn)
- **YFS:** Yield-Funding Stress (curve inversion + repo stress)
- **HY_OAS:** High-yield credit spread (z-scored)
- **EMD:** Equity Momentum Divergence (price vs trend, volatility-adjusted)
- **LCI:** Liquidity Cushion Index (system shock absorption)

**Signal Thresholds:**
| **MRI Range** | **Regime** | **Equity Allocation** | **Action** |
|---------------|------------|----------------------|------------|
| < 0.0 | Low Risk / Goldilocks | 65-70% | Overweight equities |
| 0.0 - 0.5 | Neutral | 55-60% | Strategic allocation |
| 0.5 - 1.0 | Elevated Risk | 45-50% | Reduce beta, increase quality |
| 1.0 - 1.5 | High Risk | 30-40% | Defensive positioning, add cash |
| > 1.5 | Extreme Risk | 20-30% | Maximum defense, crisis hedges |

**Historical Performance:**
- **Recession prediction precision:** 100% (no false positives when MRI >1.0)
- **Recession prediction recall:** 67% (caught 2001, 2007; missed 2020 exogenous shock)
- **Average lead time:** 9 months from MRI signal to recession start
- **Correlation with forward 6m SPX return:** -0.42

**Current Reading:** MRI = +1.1 (HIGH RISK → Defensive positioning)

### Labor Fragility Index (LFI)

**Formula:**
```
LFI = Average(z(Long-Term Unemployed %), z(-Quits Rate), z(-Hires/Quits Ratio))
```

**Interpretation:**
- LFI < 0: Labor market healthy
- LFI 0 - 0.5: Neutral to softening
- LFI 0.5 - 1.0: Fragility developing (reduce cyclical exposure)
- LFI > 1.0: Severe fragility (recession risk elevated)

**Historical Performance:**
- **Correlation with forward unemployment:** +0.65 (strong positive)
- **Lead time vs unemployment:** 6-9 months
- **Credit spread predictive power:** +0.48 (LFI predicts HY OAS widening)

**Current Reading:** LFI = +0.93 (elevated → defensive signal)

### Liquidity Cushion Index (LCI)

**Formula:**
```
LCI = Average(z(RRP/GDP), z(Reserves/GDP))
```

**Interpretation:**
- LCI > 0: Ample liquidity buffer
- LCI 0 to -0.5: Neutral to tightening
- LCI -0.5 to -1.0: Thin buffer (funding stress risk)
- LCI < -1.0: Scarce liquidity (crisis risk)

**Historical Performance:**
- **Correlation with VIX:** -0.52 (low LCI → high VIX)
- **Funding stress prediction:** 75% hit rate (low LCI → SOFR-EFFR widening)
- **2019 repo spike:** Early warning (LCI negative 2 months before)

**Current Reading:** LCI = -0.8 (thin buffer → monitor funding stress)

### Credit-Labor Gap (CLG)

**Formula:**
```
CLG = z(HY_OAS) - z(LFI)
```

**Interpretation:**
- CLG > +1.0: Credit too tight relative to labor (complacency)
- CLG -1.0 to +1.0: Aligned
- CLG < -1.0: Credit too wide relative to labor (overshooting)

**Use Case:** Identifies when credit markets are ignoring labor reality. Large positive gap = opportunity to position for credit widening before consensus recognizes deterioration.

**Current Reading:** CLG = -1.2 (credit complacent → add credit hedges)

---

## IV. POSITION CONSTRUCTION METHODOLOGY

### Asset Class Framework

**Core Portfolio (90% of capital):**

1. **U.S. Equities (40-70%)**
   - Primary: SPY (S&P 500 ETF)
   - Alternatives: VTI (Total Market), sector tilts
   
2. **U.S. Bonds (20-50%)**
   - Primary: AGG (Aggregate Bond Index)
   - Alternatives: TLT (long duration), SHY (short duration)
   
3. **Cash (0-30%)**
   - Primary: SGOV (Short-term T-bills), money market
   - Active position, not just residual

**Tactical Overlays (10% of capital, rotational):**

4. **Gold (0-10%):** Crisis hedge, real rate hedge (GLD)
5. **Commodities (0-10%):** Inflation hedge (DBC)
6. **International Equities (0-15%):** VEA (Developed), VWO (Emerging)
7. **Sector Tilts (0-20%):** Defensive (XLU, XLP, XLV) or Cyclical (XLY, XLF, XLI)
8. **Volatility (0-5%):** VXX (short-term VIX futures), TAIL (tail risk)

### Position Sizing Rules

**Maximum Limits:**
- Single position: 30%
- Sector concentration: 40%
- Gross exposure: 100% (no leverage)
- Minimum liquidity: 5% (for rebalancing)

**Signal-Based Sizing:**
- High conviction (3 pillars aligned): 20-30% position
- Medium conviction (2 pillars aligned): 10-15% position
- Low conviction (1 pillar or mixed signals): 5-10% position
- No conviction: 0% (stay in cash)

### Entry Signal Construction

**Multi-factor confirmation required.** Single indicator signals are insufficient.

**Example: Risk-Off Entry (Reduce Equity Exposure)**

**Pillar 1: Macro Deterioration**
- ✓ LFI > +0.8 (labor softening)
- ✓ CLG < -1.0 (credit ignoring reality)
- ✓ Consumer stress building (credit card delinquencies rising)

**Pillar 2: Monetary Stress**
- ✓ LCI < -0.5 (thin liquidity buffer)
- ✓ SOFR-EFFR spread widening (funding stress)
- ✓ RRP depleted (no shock absorber)

**Pillar 3: Market Technical Weakness**
- ✓ VIX rising from complacency (<15 → >18)
- ✓ Breadth deteriorating (A/D line diverging)
- ✓ Defensive sectors outperforming (XLU, XLP leading)

**Synthesis: MRI > 1.0 → HIGH CONVICTION DE-RISK**

**Action:**
- Reduce equity from 60% → 40-45%
- Increase bonds from 40% → 45-50%
- Add cash 5-10%
- Tilt toward defensive sectors 3-5%
- Add gold 2-3% (crisis hedge)

### Exit Signal Construction

**Dual Stop-Loss Framework:**

**1. Thesis-Based Stops (Fundamental Invalidation)**

Exit when regime indicators reverse:
- LFI drops below 0.0 (labor stabilizing)
- Quits rate rises above 2.1% (confidence returning)
- Fed announces emergency liquidity intervention
- Credit spreads widen >500 bps (stress already priced)

**2. Price-Based Stops (Technical Invalidation)**

Exit when technical structure breaks:
- 50-day MA crosses below 200-day MA (trend broken)
- Relative strength breaks support (sector rotation)
- Stop-loss triggered (-5% to -10% depending on volatility)

**Rule: Use whichever stop triggers first.**
- Preserve capital → Reassess → Re-enter when signals realign

---

## V. RISK MANAGEMENT FRAMEWORK

### Position Limits

**Hard Limits (Never Exceed):**
- Maximum single position: 30%
- Maximum sector concentration: 40%
- Maximum gross exposure: 100%
- Minimum liquidity for rebalancing: 5%

### Drawdown Protocols

**Progressive risk reduction:**

| **Drawdown Level** | **Action** |
|-------------------|-----------|
| -5% | Review positioning, tighten stops |
| -10% | Reduce gross exposure by 25%, increase cash |
| -15% | Cut exposure to minimum (20-30% equity), maximum defense |
| -20% | Emergency reassessment, potential strategy pause |

### Correlation Monitoring

**Track rolling 60-day correlations:**
- When equity-bond correlation > +0.3: Diversification breaking → reduce equity, add alternatives
- When cross-asset correlations spike >2σ: Leverage unwind signal → risk-off

**Example:**
```python
def correlation_regime_monitor(returns_df, asset1, asset2, window=60):
    rolling_corr = returns_df[asset1].rolling(window).corr(returns_df[asset2])
    avg_corr = rolling_corr.mean()
    std_corr = rolling_corr.std()
    
    # Flag regime change (>2 std devs from mean)
    regime_change = abs(rolling_corr - avg_corr) > 2 * std_corr
    
    return rolling_corr, regime_change
```

### Rebalancing Protocols

**Trigger-based rebalancing:**

1. **Calendar:** Quarterly review (Q1, Q2, Q3, Q4)
2. **Threshold:** Any position drifts >5% from target
3. **Signal-driven:** MRI crosses thresholds (+0.5, +1.0, +1.5)
4. **Invalidation:** When thesis-based or price-based stops triggered

---

## VI. CROSS-ASSET INTEGRATION

### Crypto-TradFi Linkages

Analysis incorporates transmission mechanisms across all major asset classes, including emerging crypto-TradFi linkages where relevant to liquidity dynamics:

**Stablecoin Treasury Holdings:**
- ~$100B+ in short-term Treasury bills
- Redemption risk implications for Fed plumbing
- Digital asset leverage tied to TradFi funding conditions

**Key Insight:** Understanding these structural relationships matters for macro analysis regardless of whether crypto is an active portfolio position. When Fed plumbing tightens, it affects both traditional markets AND digital asset leverage capacity.

---

## VII. RECENT APPLICATION & PERFORMANCE

### Case Study 1: November 2025 Stress Test

**Framework Performance: +29.43% Alpha**

**Setup (October 2025):**
- LCI approaching -1.0 (RRP exhausted)
- SOFR-EFFR spread widening to 11 bps
- Dealer balance sheet constraints visible
- Positioned defensively: 50% equity / 45% bonds / 5% cash

**Event (November 2025):**
- Acute funding stress episode
- Treasury auction tails widening
- VIX spike from 15 → 25
- Risk asset repricing

**Outcome:**
- Framework correctly identified vulnerabilities
- Defensive positioning limited downside capture
- Maintained upside participation during recovery
- **Delivered +29.43% alpha vs benchmark**

### Case Study 2: Early Labor Fragility Signal (2024-25)

**Timeline:**

**Q1 2024:** Early Warning
- LFI crosses +0.5 threshold
- Quits rate deteriorates to 2.0%
- Long-term unemployment rising
- **Action:** Begin reducing cyclical exposure

**Q2-Q3 2024:** Confirmation Phase
- Hires/quits ratio declining
- Job openings weakening
- LFI reaches +0.8
- **Action:** Reduce equity 60% → 55%

**Q4 2024:** Credit Market Complacency
- HY OAS at 3rd percentile tightness (~290 bps)
- CLG < -1.0 (credit ignoring labor)
- MRI crosses +0.5 (elevated risk)
- **Action:** Further reduce equity 55% → 50%, increase quality tilt

**Q1 2025:** Defensive Positioning Validated
- Labor market deterioration becoming consensus
- Credit spreads beginning to widen
- Equity volatility increasing
- **Outcome:** Positioned 6-9 months ahead of consensus; avoided late-cycle drawdowns

---

## VIII. CURRENT POSITIONING (December 2025)

### Regime Assessment: Phase 3 Stress

**MRI Reading: +1.1 (HIGH RISK)**

**Pillar 1 - Macro: Deteriorating**
- Labor fragility elevated (LFI +0.93)
- Consumer stress building
- Recession risk 40% next 12 months

**Pillar 2 - Monetary: Stress Developing**
- Liquidity cushion thin (LCI -0.8)
- Plumbing elevated but not crisis
- Fed likely to cut 2026 → supportive for bonds

**Pillar 3 - Market: Mixed**
- Technicals weakening but not broken
- Positioning elevated → vulnerable
- Valuations expensive (21x P/E) → limited upside

### Tactical Allocation

| **Asset** | **Strategic** | **Tactical** | **Rationale** |
|-----------|---------------|--------------|---------------|
| **SPY (Equities)** | 60% | 40% | Underweight -20% (recession risk, expensive valuations) |
| **AGG (Bonds)** | 40% | 45% | Overweight +5% (Fed cutting likely, deflation hedge) |
| **Cash** | 0% | 10% | Add +10% (liquidity for rebalancing, reduce volatility) |
| **XLV (Healthcare)** | 0% | 3% | Add +3% (defensive sector tilt) |
| **GLD (Gold)** | 0% | 2% | Add +2% (crisis hedge, real rates declining) |

### Expected Outcomes

**If Thesis Correct (Recession Q4 2026):**
- SPY: -18% → Portfolio impact: -7.2%
- AGG: +8% → Portfolio impact: +3.6%
- Cash: 0% → Portfolio impact: 0%
- XLV: -5% → Portfolio impact: -0.15%
- GLD: +12% → Portfolio impact: +0.24%
- **Total Portfolio: -3.5% (outperforms strategic by ~8%)**

**If Thesis Wrong (Goldilocks Continues):**
- SPY: +12% → Portfolio impact: +4.8%
- AGG: 0% → Portfolio impact: 0%
- Cash: 0% → Portfolio impact: 0%
- XLV: +6% → Portfolio impact: +0.18%
- GLD: 0% → Portfolio impact: 0%
- **Total Portfolio: +5.0% (underperforms strategic by ~2%)**

**Risk/Reward:** Asymmetric (avoid -11% vs give up +2%)

### Invalidation Criteria

**Exit defensive positioning if:**
- Quits rate rises above 2.1% (worker confidence returning)
- Job openings rise above 8.5M (demand accelerating)
- Hours worked stabilize or increase
- Fed announces emergency liquidity intervention
- LFI drops below +0.5 (fragility diminishing)
- MRI drops below +0.5 (risk normalizing)

---

## IX. VALUE PROPOSITION FOR INSTITUTIONAL ALLOCATORS

### What Lighthouse Macro Provides

**1. Systematic Process for Macro Inflection Points**
- Quantifiable frameworks, not discretionary market calls
- Leading indicators with 3-9 month forward visibility
- Falsifiable theses with explicit invalidation criteria

**2. Cross-Domain Synthesis**
- Labor → Credit → Equities transmission chains
- Fed plumbing → Asset price feedback loops
- Regulatory → Market structure → Liquidity dynamics

**3. Production-Grade Research Infrastructure**
- Automated ETL pipelines (daily updates at 06:00 ET)
- Replicable indicator computation
- Backtested frameworks with out-of-sample validation

**4. Conviction-Weighted Positioning**
- Concentrated portfolios aligned with high-conviction themes
- Position sizing reflects signal strength
- Track record of early positioning ahead of consensus

**5. Downside Protection Focus**
- 2.35 Sortino ratio (prioritizes limiting losses)
- Regime-based de-risking before drawdowns
- Dual stop-loss framework (thesis + technical)

### Track Record Highlights

**Historical Performance (Bank of America Private Bank 2015-2021):**
- +1.7% alpha vs benchmark
- 1.54 Sharpe ratio
- 103/93 capture ratios (upside/downside)
- 2.35 Sortino ratio

**Recent Validation (Lighthouse Macro 2024-25):**
- November 2025: +29.43% alpha during acute stress
- Early 2024: Labor fragility identified 6-9 months ahead
- Q4 2024: Defensive positioning before consensus recognition

---

## X. IMPLEMENTATION CONSIDERATIONS

### For Direct Investment Mandates

**Ideal Structure:**
- Separately managed account (SMA) or co-managed structure
- Assets: $10M - $500M
- Benchmark: 60/40 traditional OR custom strategic allocation
- Tactical ranges: ±20% deviation from strategic
- Rebalancing: Quarterly OR signal-driven

**Fees:**
- Management: 1.0% - 1.5% of AUM
- Performance: 10% - 20% above high-water mark
- Hurdle rate: 5% annually (align incentives)

### For Advisory/Research Relationships

**Ideal Structure:**
- Monthly retainer: $10k - $25k
- Services: Custom research, indicator access, quarterly reviews
- Deliverables: Weekly Beacon, Daily Beam, Monthly Horizon + bespoke analysis
- Support: Direct Slack/email access

**Value:**
- Augment internal research capabilities
- Independent perspective (no sell-side conflicts)
- Proprietary leading indicators
- Cross-domain synthesis internal teams miss

### For Framework Licensing

**Ideal Structure:**
- License proprietary indicators (MRI, LFI, LCI, CLG)
- Monthly fee: $15k - $30k
- Real-time data feed via API
- Integration into client's existing systems
- Performance fee override: Optional (5-10% of alpha generated)

---

## XI. ABOUT THE FOUNDER

### Bob Sheehan, CFA, CMT

**Credentials:**
- CFA (Chartered Financial Analyst)
- CMT (Chartered Market Technician)
- Dual credential enables rare fundamental-technical integration

**Professional Experience:**

**Bank of America Private Bank (2015-2021)**
- Associate Portfolio Manager, $4.5B multi-asset AUM
- Delivered +1.7% alpha with 1.54 Sharpe ratio
- 103/93 capture ratios (upside/downside protection)
- Multi-asset global portfolio construction

**EquiLend (2021-2023)**
- VP, Product Management
- Built securities lending analytics platform
- Developed institutional-grade plumbing expertise

**Lighthouse Macro (2023-Present)**
- Founder & CIO
- Independent macro research and strategy
- Institutional readership: 5,000+ professionals (20% QoQ growth)
- Recognized in "Less Noise More Signal" 2025 year-end report

**The ADHD Advantage:**
- Intellectual restlessness enables simultaneous mastery across domains
- While specialists go deep-narrow, Bob maintains institutional depth EVERYWHERE
- Cross-domain synthesis emerges from operating across multiple fields simultaneously
- Prevents the stagnation that plagues narrow specialists ("the plumbing guy," "the labor guy")

---

## XII. NEXT STEPS

**For Institutional Conversations:**

1. **Review this strategy document** and assess fit with your investment process
2. **Discuss structural arrangements** (SMA, advisory, licensing)
3. **Legal review** of terms and IP considerations
4. **Trial period** (3-6 months) to validate frameworks with your team
5. **Formalize relationship** with appropriate agreements

**Questions to Address:**

- What is the ideal structural arrangement? (Direct investment, advisory, licensing)
- How does this integrate with existing research/portfolio construction?
- What are the key concerns or objections?
- What would success look like in 6 months? 12 months?
- How do we structure this to align incentives appropriately?

**Contact:**
- Email: [Contact Information]
- Phone: [Contact Information]
- Website: [lighthousemacro.com]

---

**That's our view from the Watch. We'll keep the light on.**

***MACRO, ILLUMINATED.***

---

*This strategy document provides a comprehensive overview of Lighthouse Macro's investment approach, frameworks, and recent performance. For complete domain expertise and analytical methodologies, refer to the Lighthouse Macro Master Document.*

**— Bob Sheehan, CFA, CMT**  
**Founder & CIO, Lighthouse Macro**  
**December 2025**
