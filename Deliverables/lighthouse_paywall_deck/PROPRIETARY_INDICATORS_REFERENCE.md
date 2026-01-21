# LIGHTHOUSE MACRO - PROPRIETARY INDICATORS REFERENCE
## Complete Guide to Bob Sheehan's Custom Measurements, Indices & Frameworks

**Last Updated:** November 23, 2025
**Compiled From:** All published articles on [lighthousemacro.com](https://www.lighthousemacro.com)

---

## TABLE OF CONTENTS

### SECTION 1: LIQUIDITY INDICATORS
1. Liquidity Cushion Index (LCI)
2. Liquidity Transmission Framework
3. Leverage Capacity Matrix
4. Liquidity Composite Index

### SECTION 2: LABOR MARKET INDICATORS
5. Labor Fragility Index (LFI)
6. Labor Dynamism Index (LDI)
7. Job-Hopper Premium

### SECTION 3: CREDIT & FUNDING STRESS INDICATORS
8. Yield-Funding Stress (YFS)
9. Credit-Labor Gap (CLG)
10. Spread-Volatility Imbalance (SVI)
11. Repo Rate Dispersion Index

### SECTION 4: EQUITY & MARKET POSITIONING
12. Equity Momentum Divergence (EMD)
13. QUAL/SPY Ratio (Quality vs Risk)

### SECTION 5: COMPOSITE/MASTER INDICES
14. Macro Risk Index (MRI)

### SECTION 6: TREASURY MARKET MICROSTRUCTURE
15. Collateral Shortage Index
16. Treasury Auction Tailing Metric
17. Bid-to-Cover Ratio Analysis
18. Dealer Allotment Percentage
19. Dealer Accumulation Momentum
20. Treasury Stress Dashboard (4-Metric System)
21. Bill-Bond Divergence Analysis
22. Treasury Composition Shift Index

### SECTION 7: STABLECOIN & CRYPTO INTEGRATION
23. Stablecoin Treasury Holdings Percentage
24. Stablecoin Supply Correlation with T-Bill Richness
25. 3M Bill-SOFR Spread

### SECTION 8: ADVANCED TRADING FRAMEWORKS
26. Z-Score Positioning Index (Basis Trades)
27. Compression Function Model
28. Recovery Half-Life Metric
29. Market-Neutral Basis Sharpe Ratio

---

# SECTION 1: LIQUIDITY INDICATORS

## 1. Liquidity Cushion Index (LCI)

**Source:** "The Beacon | It's Getting Spooky" (Oct 30, 2025)

### Formula
```
LCI = z_score(ON_RRP / GDP) + z_score(Bank_Reserves / GDP)
LCI = average of the two z-scores
```

### Data Inputs
- **ON RRP:** Federal Reserve's Overnight Reverse Repurchase Facility balance (daily)
- **Bank Reserves:** Reserve balances held at Federal Reserve (weekly)
- **GDP:** Nominal U.S. Gross Domestic Product (quarterly, seasonally adjusted)

### Calculation Steps
1. Calculate RRP-to-GDP ratio: `RRP / GDP`
2. Calculate Reserves-to-GDP ratio: `Reserves / GDP`
3. Compute rolling z-score for each ratio (typically 252-day window):
   - `z_score = (current_value - rolling_mean) / rolling_std`
4. Average the two z-scores

### Interpretation
- **High LCI (>+1σ):** Ample liquidity cushion, system can absorb shocks
- **Normal LCI (±1σ):** Adequate liquidity conditions
- **Low LCI (<-1σ):** Minimal shock-absorption capacity, vulnerable system
- **Critical (<-2σ):** Severe liquidity constraint, crisis-prone

### Key Thresholds
- **Near 0σ:** Minimal cushion (current state as of Oct 2025)
- **Pre-2008 baseline:** Effectively zero (no excess reserves existed then)

### Usage Notes
- Leading indicator for systemic stress events
- Correlates with VIX and credit spread volatility
- Mean reversion tendency after extreme readings

---

## 2. Liquidity Transmission Framework

**Source:** "⚓ Liquidity Transmission Framework" (Nov 8, 2025)

### Framework Structure
This is a **qualitative transmission mechanism** rather than a single formula. It tracks stress propagation through sequential stages:

**Stage 1: RRP Depletion** → **Stage 2: Reserve Drainage** → **Stage 3: SRF Usage Surge** → **Stage 4: Collateral Stress** → **Stage 5: Stablecoin Flow Stalls** → **Stage 6: Perp Basis Collapse** → **Stage 7: Crypto Liquidations**

### Data Inputs Required
1. **RRP Balance:** Daily ON RRP usage
2. **SRF Usage:** Standing Repo Facility borrowing (Fed H.4.1 report)
3. **Stablecoin Treasury Flows:** Changes in USDT/USDC T-bill holdings
4. **Perpetual Futures Basis:** BTC-PERP vs BTC-SPOT spread
5. **Crypto Liquidation Volumes:** Exchange liquidation data (Coinglass, etc.)

### Interpretation
- **Key Insight:** "Stress is now propagating through the system instead of being neutralized by it"
- Liquidity hasn't disappeared—it **stopped absorbing risk** and now **transmits it downstream**
- Unlike 2019 repo crisis (plumbing failure) or 2020 COVID shock (demand surge), current state reflects **structural capacity exhaustion**

### Critical Thresholds
| Indicator | Safe | Caution | Crisis |
|-----------|------|---------|--------|
| RRP Balance | >$500B | $50B-$500B | **<$50B** (current: $10.75B) |
| SRF Usage | <$10B | $10B-$30B | **>$30B** (Oct 31: $50.35B) |
| Liquidation Cascade | <$5B | $5B-$10B | **>$10B** (Oct: $19.16B) |

### Timing
- **15-20 day lag** from liquidity stress to downstream crypto impacts
- Validates transmission framework's predictive power

---

## 3. Leverage Capacity Matrix

**Source:** "⚓ Liquidity Transmission Framework" (Nov 8, 2025)

### Conceptual Framework
Distinguishes between **liquidity quantity** (absolute levels) and **liquidity capacity** (usable leverage given plumbing constraints).

### State Classification
| System State | RRP Level | Capacity | Constraint Type |
|--------------|-----------|----------|-----------------|
| **Ample** | >$1T | High | None |
| **Adequate** | $500B-$1T | Moderate | Minimal |
| **Scarce** | $50B-$500B | Low | Dealer balance sheets |
| **Crisis** | <$50B | Minimal | **Plumbing infrastructure** |

### Current State (Nov 2025)
- **RRP:** $10.75B → **Crisis Mode**
- Leverage constrained by **plumbing infrastructure**, not policy settings
- System operates in "transmission mode" rather than "absorption mode"

### Interpretation
Even if Fed cuts rates or injects liquidity, **structural bottlenecks** (dealer SLR limits, collateral scarcity) prevent effective deployment.

---

## 4. Liquidity Composite Index

**Source:** "⚓ Liquidity Transmission Framework" (Nov 8, 2025)

### Formula (Implied)
```
Liquidity_Composite = weighted_average([
    RRP_balance,
    T_bill_SOFR_spread,
    OFR_FSI,
    Repo_volumes
])
```

### Key Relationship
- **One-for-one correlation** between RRP balance and composite liquidity measure
- Validates RRP as primary liquidity barometer

### Interpretation
- Rising composite = Improving liquidity conditions
- Falling composite = Tightening liquidity, higher stress risk
- Tracks systemic liquidity conditions with high fidelity

---

# SECTION 2: LABOR MARKET INDICATORS

## 5. Labor Fragility Index (LFI)

**Source:** "The Beacon | It's Getting Spooky" (Oct 30, 2025)

### Formula
```
LFI = z_score(Long_Duration_Unemployment_Share)
      + z_score(-Quits_Rate)
      + z_score(-Hires_to_Quits_Ratio)

LFI = average of three components
```

### Data Inputs
- **Long-Duration Unemployment Share:** % of unemployed persons jobless ≥27 weeks (BLS, monthly)
- **Quits Rate:** JOLTS quits as % of employment (BLS JOLTS, monthly)
- **Hires-to-Quits Ratio:** JOLTS hires divided by quits (monthly)

### Calculation Steps
1. Calculate long-duration unemployment share: `Unemployed_27+_Weeks / Total_Unemployed * 100`
2. Obtain quits rate from JOLTS (already published as rate)
3. Calculate hires-to-quits ratio: `Hires / Quits`
4. Z-score each component (252-day or 12-month window)
5. **Invert** quits and hires/quits (higher quits/hires = healthier labor market = lower fragility)
6. Average the three z-scores

### Interpretation
- **LFI > +1σ:** Elevated labor fragility, structural deterioration
- **LFI near 0:** Normal labor market health
- **LFI < -1σ:** Robust labor market, low fragility

### Why It Matters
- **Leading indicator:** Shows labor stress **before** unemployment rate rises
- **Structural vs cyclical:** Captures hidden deterioration beneath headline payrolls
- Quits declining = Workers losing bargaining power
- Long-duration unemployment rising = Harder to re-enter workforce

### Current State (Oct 2025)
- **Rising since early 2024**
- Above 0σ despite stable unemployment rate
- Signals hidden deterioration

---

## 6. Labor Dynamism Index (LDI)

**Source:** "The Beacon | It's Getting Spooky" (Oct 30, 2025)

### Formula
```
LDI = z_score(Quits_Rate)
      + z_score(Hires_to_Quits_Ratio)
      + z_score(Quits_to_Layoffs_Ratio)

LDI = average of three components
```

### Data Inputs
- **Quits Rate:** JOLTS quits as % of employment
- **Hires-to-Quits Ratio:** JOLTS hires / quits
- **Quits-to-Layoffs Ratio:** JOLTS quits / layoffs

### Calculation Steps
1. Obtain quits rate from JOLTS
2. Calculate ratios: `Hires/Quits` and `Quits/Layoffs`
3. Z-score each component
4. Average the three z-scores

### Interpretation
- **High LDI (>+1σ):** Workers have optionality, confident in job-switching
- **Low LDI (<-1σ):** Workers hesitant to quit, late-cycle caution
- **Below 0σ (current):** Reduced worker mobility, risk aversion

### Leading Indicator Properties
- **Leads payroll growth by 2-3 quarters**
- When LDI falls sharply, payroll weakness typically follows

### Relationship to LFI
- **LDI measures:** Worker confidence/optionality (behavioral)
- **LFI measures:** Labor market stress/fragility (structural)
- **Divergence:** Rising LFI + Falling LDI = Late-cycle deterioration

---

## 7. Job-Hopper Premium

**Source:** "The Vanishing Job-Hopper Premium" (Mar 14, 2025)

### Definition
The **wage differential** between workers who switch jobs vs. those who stay with the same employer.

### Formula (Implied)
```
Job_Hopper_Premium = Wage_Growth_Job_Switchers - Wage_Growth_Job_Stayers
```

### Data Source
- **Atlanta Fed Wage Growth Tracker** (breaks down wage growth by job-switchers vs stayers)
- **BLS CPS** (Current Population Survey) microdata

### Key Finding (March 2025)
- Premium narrowed to **just 0.2 percentage points**
- Historical average: **2-4 percentage points**

### Interpretation
- **Positive premium:** Workers rewarded for switching jobs (healthy labor market)
- **Zero/negative premium:** "The grass is no longer greener" (late-cycle warning)
- Signals employer leverage over workers

### Implications
- Workers less willing to quit (feeds into LDI decline)
- Wage growth stagnates even with low unemployment
- Precursor to broader labor market weakening

---

# SECTION 3: CREDIT & FUNDING STRESS INDICATORS

## 8. Yield-Funding Stress (YFS)

**Source:** "The Beacon | It's Getting Spooky" (Oct 30, 2025)

### Formula
```
YFS = weighted_average([
    z_score(10Y_2Y_Spread),
    z_score(10Y_3M_Spread),
    z_score(BGCR_EFFR_Spread)
])
```

### Data Inputs
- **10Y-2Y Spread:** 10-Year Treasury yield minus 2-Year Treasury yield
- **10Y-3M Spread:** 10-Year Treasury yield minus 3-Month T-bill yield
- **BGCR-EFFR Spread:** Broad General Collateral Rate minus Effective Federal Funds Rate

### Calculation Steps
1. Calculate yield curve spreads (already published by FRED)
2. Calculate repo plumbing stress: `BGCR - EFFR`
3. Z-score each component
4. Weight based on volatility or equal-weight average

### Interpretation
- **High YFS (>+1σ):** Inverted curve + money market stress = Fed tightening/stress
- **Low YFS (<-1σ):** Steep curve + smooth plumbing = Easing conditions
- **Current state:** "Improved from 2023 peaks but elevated in absolute terms"

### Why BGCR-EFFR Matters
- **BGCR:** Rate at which dealers can borrow in repo market
- **EFFR:** Overnight lending rate between banks
- **Positive spread:** Repo market under stress (dealers paying up for collateral)
- **Threshold:** Spread >15 bps signals funding stress

---

## 9. Credit-Labor Gap (CLG)

**Source:** "The Beacon | It's Getting Spooky" (Oct 30, 2025)

### Formula
```
CLG = z_score(HY_OAS) - z_score(LFI)
```

Where:
- **HY_OAS:** High-Yield Option-Adjusted Spread (BAML index)
- **LFI:** Labor Fragility Index (see above)

### Calculation Steps
1. Calculate Labor Fragility Index
2. Obtain HY OAS from FRED (series: BAMLH0A0HYM2)
3. Z-score both series over same window (e.g., 252 days)
4. Subtract: `z(HY OAS) - z(LFI)`

### Interpretation
- **CLG > 0 (Positive):** Credit spreads wide relative to labor stress = **Fair pricing**
- **CLG ≈ 0:** Credit spreads match labor fundamentals
- **CLG < 0 (Negative):** **Spreads too tight given labor deterioration** = Pre-widening setup

### Current State (Oct 2025)
- **Negative** → Credit markets underpricing labor market risk
- "Historically a pre-widening configuration"

### Investment Implication
- **Negative CLG:** Reduce credit exposure, spreads likely to widen
- **Positive CLG:** Credit offering value relative to fundamentals

---

## 10. Spread-Volatility Imbalance (SVI)

**Source:** "The Beacon | It's Getting Spooky" (Oct 30, 2025)

### Formula
```
SVI = z_score(HY_Spread_Level) / z_score(HY_Spread_Volatility)
```

Or directional assessment:
```
SVI = "Are spreads tight while volatility is rising?"
```

### Data Inputs
- **HY Spread Level:** Current HY OAS
- **HY Spread Volatility:** 30-day realized volatility of HY OAS

### Interpretation
- **Low SVI (tight spreads + low vol):** Stable, complacent market
- **High SVI (wide spreads + high vol):** Crisis/stress pricing
- **Imbalance (tight spreads + rising vol):** **Late-cycle mismatch** = Poor risk compensation

### Current State
- "Tight spreads with rising vol = poor compensation for risk"
- "Late-cycle mismatch that rarely persists"

### Investment Signal
- **High volatility + tight spreads:** Avoid credit, spreads will widen to compensate

---

## 11. Repo Rate Dispersion Index

**Source:** "The Beacon | It's Getting Spooky" (Oct 30, 2025)

### Formula
```
Repo_Dispersion = BGCR_99th_Percentile - BGCR_1st_Percentile
```

### Data Inputs
- **BGCR Distribution:** Daily percentile data from NY Fed (1st, 25th, 75th, 99th percentiles)
- **Tri-Party Repo Volume:** Daily volume data from NY Fed

### Interpretation
- **Low Dispersion (<25 bps):** Even funding access across market participants
- **Moderate (25-50 bps):** Some funding differentiation
- **High Dispersion (>50 bps):** **Funding fragmentation** = Some participants getting locked out

### Current State
- **Rising dispersion** + **elevated tri-party volume**
- "Classic pre-stress configuration" (similar to Sept 2019 repo crisis)

### Why It Matters
- Dispersion widening = Some dealers/hedge funds struggling to access funding
- Precursor to repo market disruptions
- Combined with high volume = Desperate scramble for cash

---

# SECTION 4: EQUITY & MARKET POSITIONING

## 12. Equity Momentum Divergence (EMD)

**Source:** "The Beacon | It's Getting Spooky" (Oct 30, 2025)

### Formula
```
EMD = z_score((SP500 - SP500_MA) / Realized_Volatility)
```

Where:
- **SP500_MA:** Moving average of S&P 500 (e.g., 200-day MA)
- **Realized_Volatility:** 30-day realized volatility or VIX as proxy

### Calculation Steps
1. Calculate distance from trend: `Price_Deviation = SP500 - MA(SP500, 200)`
2. Calculate realized volatility (or use VIX)
3. Normalize by volatility: `Momentum_Ratio = Price_Deviation / Realized_Vol`
4. Z-score the momentum ratio

### Interpretation
- **EMD > +1σ:** **Stretched momentum**, thin shock-absorption, prone to air pockets
- **EMD near 0:** Normal momentum conditions
- **EMD < -1σ:** Oversold, potential mean reversion

### Current State (Oct 2025)
- **Above +1σ**
- "Stretched momentum with thin shock-absorption—prone to air-pockets when credit moves"

### Investment Implication
- High EMD + Negative CLG = **Asymmetric downside risk**
- Reduce beta exposure, add hedges

---

## 13. QUAL/SPY Ratio (Quality vs Risk)

**Source:** "The Beacon | It's Getting Spooky" (Oct 30, 2025)

### Formula
```
QUAL_SPY_Ratio = QUAL_Price / SPY_Price
```

### Data Inputs
- **QUAL:** iShares MSCI USA Quality Factor ETF (ticker: QUAL)
- **SPY:** S&P 500 ETF (ticker: SPY)

### Interpretation
- **High Ratio:** Quality outperforming = Risk-off, defensive positioning
- **Low Ratio:** Quality underperforming = Risk-on, chasing junk
- **All-time lows:** Maximum complacency, late-cycle behavior

### Current State (Oct 2025)
- **"At or near all-time lows"**
- Despite mounting macro fragility → **Behavioral warning**

### Investment Signal
- Extreme lows + deteriorating fundamentals = **Contrarian sell signal**
- Quality underperformance rarely persists through credit stress events

---

# SECTION 5: COMPOSITE/MASTER INDICES

## 14. Macro Risk Index (MRI)

**Source:** "The Beacon | It's Getting Spooky" (Oct 30, 2025)

### Formula
```
MRI = LFI - LDI + YFS + z_score(HY_OAS) + EMD - LCI
```

### Component Breakdown
| Component | Weight | Contribution |
|-----------|--------|--------------|
| **+LFI** | Equal | Labor fragility (higher = worse) |
| **-LDI** | Equal | Labor dynamism (lower = worse, so subtract) |
| **+YFS** | Equal | Funding stress (higher = worse) |
| **+CSE** | Equal | Credit spread elements (higher = tighter spreads) |
| **+EMD** | Equal | Equity momentum (higher = stretched) |
| **-LCI** | Equal | Liquidity cushion (lower = worse, so subtract) |

### Interpretation
- **Rising MRI while equities climb:** Markets under-pricing macro risk
- **High MRI (>+1σ):** Elevated systemic risk despite market complacency
- **Divergence:** MRI rising + SPX rising = Asymmetric payoff setup

### Current State (Oct 2025)
- **Elevated and rising trend through October**
- Key observation: "Markets are under-pricing macro risk"

### Investment Application
- **High MRI + Low VIX:** Add tail hedges (puts, vol products)
- **High MRI + Tight credit:** Reduce credit, increase quality
- **Divergences define asymmetric payoff profiles**

---

# SECTION 6: TREASURY MARKET MICROSTRUCTURE

## 15. Collateral Shortage Index

**Source:** "Collateral Fragility" (Aug 19, 2025)

### Formula (Implied)
```
Collateral_Shortage = f(SLR_utilization, Repo_spreads, Auction_metrics, Reserve_availability)
```

### Data Inputs
- **Dealer SLR Ratios:** Supplementary Leverage Ratio utilization
- **Treasury Auction Metrics:** Bid-to-cover, tails, foreign participation
- **Reserve Availability:** Bank reserves at Fed
- **Repo Market Spreads:** GC repo rates, SOFR spreads

### Key Thresholds
- **Historical baseline:** ~30
- **Current level:** ~80
- **Crisis echo:** "Echoing the mechanics that led to the 2019 repo crisis"

### Interpretation
- Higher values = Tighter collateral availability + funding market strain
- Rising index precedes:
  - Wider repo spreads
  - Treasury auction tails
  - Dealer balance sheet constraints

---

## 16. Treasury Auction Tailing Metric

**Source:** "Collateral Fragility" (Aug 19, 2025)

### Formula
```
Auction_Tail_Percentage = (Number_of_Tailed_Auctions / Total_Auctions) * 100
```

**Tail Definition:** Auction where clearing yield exceeds expected yield (weak demand)

### Data Inputs
- **Auction results:** U.S. Treasury auction announcements (treasurydirect.gov)
- **Bid-to-cover ratios:** Included in auction results
- **Yield levels:** Clearing yields vs. pre-auction "when-issued" yields

### Key Thresholds
| Period | Tail % | Interpretation |
|--------|--------|----------------|
| Historical | 15% | Normal market function |
| **2025 YTD** | **35%** | Structural demand weakness |

### Interpretation
- Rising tails signal difficulty clearing supply without yield concessions
- "Structural demand weakness" not just tactical positioning
- Precursor to term premium expansion

---

## 17. Bid-to-Cover Ratio Analysis

**Source:** "Seemingly Stable, Systemically Stressed" (Sep 15, 2025)

### Formula
```
Bid_to_Cover = Total_Bids_Received / Amount_of_Securities_Offered
```

### Data Source
- Treasury auction results (published post-auction)

### Key Thresholds
| Maturity | Strong | Neutral | Weak |
|----------|--------|---------|------|
| T-Bills | >3.0x | 2.5-3.0x | <2.5x |
| 10Y Notes | >2.5x | 2.2-2.5x | **<2.2x** |
| 30Y Bonds | >2.3x | 2.0-2.3x | <2.0x |

### Current Observations (2025)
- **T-Bills:** 3.4x (robust, technically driven by stablecoin demand)
- **10Y Notes:** 2.32x (deteriorating)
- **Longer maturities:** "Closer to 2.2x or below" (weak)

### Interpretation
- **Bill-Bond Divergence:** Strong short-end (technical buyers) vs. weak long-end (fundamental weakness)
- Deteriorating long-end B/C = Rising term premium required

---

## 18. Dealer Allotment Percentage

**Source:** "Seemingly Stable, Systemically Stressed" (Sep 15, 2025)

### Formula
```
Dealer_Allotment_% = (Amount_Allocated_to_Primary_Dealers / Total_Auctioned) * 100
```

### Data Source
- Treasury auction results (breaks down allocation by bidder class)

### Critical Threshold
- **Historical norm:** <20%
- **Stress signal:** **>20%** ("Anything above the dashed 20% line is historically rare")

### Interpretation
- Higher dealer percentages = Forced absorption under capacity constraints
- Dealers warehousing bonds they can't distribute
- Precedes:
  - Wider bid-ask spreads
  - Rising repo costs
  - Balance sheet constraints

---

## 19. Dealer Accumulation Momentum

**Source:** "Cracks in the Foundation" (Aug 12, 2025)

### Formula
```
Accumulation_Momentum = Short_Term_Accumulation_Rate / Long_Term_Trend_Rate
```

Where:
- **Short-term rate:** Change in dealer positions over 4 weeks
- **Long-term trend:** Average quarterly change over 2 years

### Data Source
- **NY Fed FR 2004 Report:** Primary Dealer Statistics (weekly)

### Interpretation
- **Ratio > 1.5:** Dealers accumulating faster than historical pace = Stress
- **Current state:** "Consistently exceeds long-term trends"
- **Capacity:** Dealers at "96% of their regulatory ceiling" (SLR constraint)

### Investment Signal
- Elevated accumulation momentum + near-capacity SLR = Supply cannot be absorbed → Yields must rise

---

## 20. Treasury Stress Dashboard (4-Metric System)

**Source:** "Cracks in the Foundation" (Aug 12, 2025)

### Framework
Simultaneous tracking of four independent stress indicators:

| Metric | Current State | Threshold | Status |
|--------|---------------|-----------|---------|
| **1. Auction Tail Frequency** | 45% | Historical <15% | 🔴 Red |
| **2. Foreign Demand** | 63.8% | Historical ~70% | 🔴 Red |
| **3. Dealer Capacity** | 96% | <85% comfortable | 🔴 Red |
| **4. Funding Stress** | 30% | <40% manageable | 🟢 Green |

### Overall Assessment
- **"3 of 4 metrics flashing red"** = Systemic weakness

### Data Sources
1. **Auction Tails:** Treasury auction results
2. **Foreign Demand:** TIC (Treasury International Capital) data
3. **Dealer Capacity:** Primary dealer positions (FR 2004) + SLR ratios
4. **Funding Stress:** Repo spreads, SOFR-OIS, money market indicators

### Interpretation
- All 4 red = Acute stress, yields likely to spike
- 3 of 4 red = Structural weakness, sustained pressure on long-end
- 2 of 4 red = Watchful monitoring
- ≤1 red = Normal functioning

---

## 21. Bill-Bond Divergence Analysis

**Source:** "Cracks in the Foundation" (Aug 12, 2025)

### Framework
Contrasts bid-to-cover ratios and participation across maturity spectrum

### Key Observations (2025)
| Maturity | Bid-to-Cover | Demand Driver | Interpretation |
|----------|--------------|---------------|----------------|
| **T-Bills** | 3.4x | **Technical** (stablecoins) | Front-end strength |
| **10Y Notes** | 2.32x | **Fundamental** (real money) | Back-end erosion |

### Interpretation
- **Strong bills + Weak bonds:** "Technical versus fundamental" demand split
- Stablecoin demand for T-bills creates false sense of Treasury demand health
- Long-end weakness reflects:
  - Deficit concerns
  - Term premium repricing
  - Foreign central bank selling

### Investment Implication
- **Curve steepening trade:** Short bills, long bonds (anticipate long-end weakness)

---

## 22. Treasury Composition Shift Index

**Source:** "Cracks in the Foundation" (Aug 12, 2025)

### Formula
```
Composition_Shift = % change in buyer-mix across:
  - Foreign central banks
  - Domestic banks
  - Primary dealers
```

### Historical vs Current Allocation
| Buyer Class | 2020 | Current | Historical Target |
|-------------|------|---------|-------------------|
| **Foreign CBs** | 45% | **28%** | ~70% (pre-crisis) |
| **Domestic Banks** | 20% | **35%** | ~25% |
| **Primary Dealers** | 15% | **25%** | ~10% |

### Interpretation
- **Declining natural buyers** (foreign CBs) forced replacement by **intermediaries** (dealers)
- Creates **structural fragility:**
  - Dealers are price-sensitive (need term premium)
  - Foreign CBs were price-insensitive (hold to maturity)
- "Buyer-Mix Transformation" = Quality deterioration of Treasury demand base

---

# SECTION 7: STABLECOIN & CRYPTO INTEGRATION

## 23. Stablecoin Treasury Holdings Percentage

**Source:** "Cracks in the Foundation" (Aug 12, 2025)

### Formula
```
Stablecoin_Holdings_% = (Stablecoin_Treasury_Holdings / Total_Treasury_Bills_Outstanding) * 100
```

### Data Inputs
- **Stablecoin reserves:** Public disclosures from Tether, Circle (USDC), etc.
- **Total T-Bills Outstanding:** U.S. Treasury (TreasuryDirect)

### Key Levels (2025)
- **Global T-bill demand:** 3.0%
- **Market composition:** 6% (stablecoin issuers as buyer segment)
- **Tether alone:** $125B of $180B total stablecoin holdings

### Interpretation
- High concentration indicates **vulnerability to redemption shocks**
- If stablecoins experience run → Sudden T-bill supply dumped on market
- Creates **negative convexity:** Stress begets more stress

### Investment Signal
- Monitor stablecoin supply growth (declining = potential T-bill selling)
- Crypto stress events → T-bill market disruption

---

## 24. Stablecoin Supply Correlation with T-Bill Richness

**Source:** "Collateral Fragility" (Aug 19, 2025)

### Formula
```
Correlation(Stablecoin_Supply_Growth, Bill_SOFR_Spread_Tightening)
```

### Relationship
- **Rising stablecoin supply** → **Tighter 3M Bill-SOFR spreads** (bills trade "rich")
- Indicates crypto-driven collateral demand distorting benchmarks

### Interpretation
- Stablecoins buying T-bills → Bills trade expensive relative to SOFR
- Creates **feedback loop:**
  - More crypto inflows → More T-bill demand → Lower yields
  - But: Redemption risk creates **fragility**

---

## 25. 3M Bill-SOFR Spread

**Source:** "Collateral Fragility" (Aug 19, 2025)

### Formula
```
Bill_SOFR_Spread = 3M_T_Bill_Rate - SOFR
```

### Data Inputs
- **3M T-Bill Rate:** Auction yields (TreasuryDirect)
- **SOFR:** Secured Overnight Financing Rate (NY Fed)

### Interpretation
- **Positive spread:** Bills trading rich (high demand)
- **Negative spread:** Bills trading cheap (supply pressure)
- **Volatility:** Reflects collateral demand intensity and Fed facility usage shifts

### Current State
- Described as "volatile" and widening
- Correlates with stablecoin supply changes

---

# SECTION 8: ADVANCED TRADING FRAMEWORKS

## 26. Z-Score Positioning Index (Basis Trades)

**Source:** "The Beam | Treasury Buybacks & The Mechanical Basis Squeeze" (Oct 10, 2025)

### Formula
```
Z_Score = (Current_Basis - Mean_Basis) / StdDev_Basis
```

Applied separately to maturity buckets:
- 7-10 Year
- 10-20 Year
- 20-30 Year

### Data Inputs
- **Current Basis:** Cash Treasury yield minus Treasury futures implied yield
- **Historical Mean/StdDev:** Trailing 1-year statistics

### Key Thresholds
| Maturity | Z-Score | Positioning Signal |
|----------|---------|-------------------|
| 7-10Y | **-1.22σ** | **Oversold → Long candidate** |
| 10-20Y | **+0.97σ** | Approaching compression trigger |
| 20-30Y | +0.90σ | Elevated conditions |

### Stop-Loss
- **±2.5σ reversal:** Exit position if Z-score reverses by 2.5 standard deviations

### Trade Structure
- **Entry:** 10-20Y Z-score breaching +1.0σ within 72-hour window
- **Position:** Long 7-10Y OFR / Short 10-20Y OTR (market-neutral pair)
- **Target:** 3 basis point compression capture

---

## 27. Compression Function Model

**Source:** "The Beam | Treasury Buybacks & The Mechanical Basis Squeeze" (Oct 10, 2025)

### Formula
```
C(t) = -α * exp(-((t-t₀)/β)²) * H(t₀-t)
       + -γ * exp(-t/τ) * H(t-t₀)
```

**Components:**
- **First term:** Pre-operation compression (anticipatory)
- **Second term:** Post-operation mean reversion decay
- **H(·):** Heaviside step function (switches between pre/post)

### Parameter Calibration by Maturity
| Bucket | α | β | γ | τ | R² |
|--------|---|---|---|---|-----|
| 7-10Y | 0.5 | 2.0 | 3.0 | 2.0 | >0.85 |
| 10-20Y | 0.4 | 2.5 | 2.5 | 3.0 | >0.85 |
| 20-30Y | 0.3 | 3.0 | 2.8 | 4.0 | >0.85 |

### Interpretation
- **α, β:** Control pre-operation compression magnitude and timing
- **γ, τ:** Control post-operation decay rate
- **Different τ across buckets:** Explains differential recovery velocities
- **"The signal lives in the operational calendar"**

---

## 28. Recovery Half-Life Metric

**Source:** "The Beam | Treasury Buybacks & The Mechanical Basis Squeeze" (Oct 10, 2025)

### Formula
```
Recovery_Half_Life = ln(2) / τ
```

Where **τ** is the exponential decay constant from the Compression Function Model.

### Observed Half-Lives
| Maturity | τ (days) | Half-Life | Interpretation |
|----------|----------|-----------|----------------|
| 7-10Y | 2.0 | ~1.4 days | **Rapid normalization** |
| 10-20Y | 3.0 | ~2.1 days | Moderate recovery |
| 20-30Y | 4.0 | ~2.8 days | Persistent dislocation |

**Aggregate mean:** 2.67 days

### Interpretation
- Faster recovery in shorter maturities = **Superior liquidity**
- Longer-dated instruments exhibit **dealer balance sheet constraints**
- Trade timing: Exit most positions by T+3 (70% unwind), complete by T+5

---

## 29. Market-Neutral Basis Sharpe Ratio

**Source:** "The Beam | Treasury Buybacks & The Mechanical Basis Squeeze" (Oct 10, 2025)

### Value
**Sharpe Ratio: 1.84**

### Sample Statistics (180-day trailing)
- **Mean compression achieved:** -2.77 basis points
- **Standard deviation:** 0.38 basis points
- **Win rate:** 68%
- **Sample size:** 27 identified operations

### Trade Structure
```
Long:  $10mm 7-10Y OFR (off-the-run)
Short: $10mm 10-20Y OTR (on-the-run)
```

### Interpretation
- Risk-adjusted returns exceed volatility by **1.84x**
- Market-neutral structure isolates calendar effect from directional risk
- **Cross-Maturity Correlation:** 0.73 (confirms compression propagates across buckets)

### Exit Protocol
- **70% unwind at T+3** (three trading days post-operation)
- **Complete exit by T+5**

---

# APPENDIX: QUICK REFERENCE FORMULAS

## Master Formula Sheet

```python
# LIQUIDITY
LCI = (z(RRP/GDP) + z(Reserves/GDP)) / 2

# LABOR
LFI = (z(LongUnemployment%) + z(-Quits) + z(-Hires/Quits)) / 3
LDI = (z(Quits) + z(Hires/Quits) + z(Quits/Layoffs)) / 3

# CREDIT & FUNDING
YFS = (z(10Y-2Y) + z(10Y-3M) + z(BGCR-EFFR)) / 3
CLG = z(HY_OAS) - z(LFI)
SVI = z(HY_OAS_Level) / z(HY_OAS_Volatility)

# EQUITY
EMD = z((SP500 - MA(SP500)) / Realized_Vol)
QUAL_SPY = QUAL_Price / SPY_Price

# COMPOSITE
MRI = LFI - LDI + YFS + z(HY_OAS) + EMD - LCI

# TREASURY MICROSTRUCTURE
Dealer_Allotment_% = Dealer_Amount / Total_Auction * 100
Bill_SOFR_Spread = 3M_Bill_Rate - SOFR

# BASIS TRADES
Z_Score_Basis = (Current_Basis - Mean) / StdDev
Recovery_Half_Life = ln(2) / τ
```

---

# DATA SOURCE SUMMARY

| Indicator | Primary Data Source | Frequency | FRED Series ID (if applicable) |
|-----------|---------------------|-----------|-------------------------------|
| **RRP** | NY Fed / FRED | Daily | RRPONTSYD |
| **Bank Reserves** | FRED | Weekly | WRESBAL |
| **GDP** | FRED | Quarterly | GDP |
| **JOLTS** | BLS / FRED | Monthly | JTSJOL, JTSHIL, JTSQUL, JTSLDL |
| **Unemployment** | BLS / FRED | Monthly | UNRATE, U6RATE |
| **HY OAS** | FRED (BofA) | Daily | BAMLH0A0HYM2 |
| **BBB/AAA OAS** | FRED (BofA) | Daily | BAMLC0A4CBBB, BAMLC0A1CAAA |
| **VIX** | CBOE / FRED | Daily | VIXCLS |
| **S&P 500** | FRED | Daily | SP500 |
| **BGCR** | NY Fed | Daily | NY Fed Markets API |
| **SOFR** | NY Fed / FRED | Daily | SOFR |
| **EFFR** | NY Fed / FRED | Daily | EFFR |
| **Treasury Yields** | U.S. Treasury / FRED | Daily | DGS2, DGS10, DGS30, etc. |
| **Dealer Positions** | NY Fed FR 2004 | Weekly | Manual download |
| **Stablecoin Supply** | Tether/Circle disclosures | Daily | Manual/API |
| **Treasury Auctions** | TreasuryDirect | Per auction | Manual |
| **OFR FSI** | Office of Financial Research | Daily | Manual download |

---

# USAGE NOTES

## Calculation Best Practices

1. **Z-Score Window:** Use 252-day (1-year) rolling window for most indicators
2. **Rebalancing:** Recalculate indices daily with latest data
3. **Missing Data:** Forward-fill daily series when calculating from monthly/quarterly inputs
4. **Outlier Handling:** Winsorize extreme values (>±3σ) before z-scoring to prevent distortion

## Interpretation Guidelines

- **Single indicators:** Useful but context-dependent
- **Composite indices (MRI, LCI, etc.):** More robust, less prone to false signals
- **Thresholds:** Treat as guidelines, not hard rules
- **Regime shifts:** Indicators more reliable at extremes (±1σ, ±2σ) than mid-range

## Trade Implementation

- **Never act on single indicator alone**
- **Confluence:** Wait for 2-3 indicators to confirm
- **Timing:** Many labor/credit indicators lead by 2-6 months
- **Risk management:** Always use stops, size appropriately

---

**End of Proprietary Indicators Reference**

**Compiled by:** Claude (Anthropic) from public Lighthouse Macro publications
**For:** Bob Sheehan, CFA, CMT
**Date:** November 23, 2025

**All formulas, methodologies, and frameworks are proprietary to Lighthouse Macro and Bob Sheehan unless otherwise noted.**
