# PILLAR 4: HOUSING

## The Housing Transmission Chain

Housing isn't shelter—it's the **financial system's collateral backbone**. The transmission mechanism operates through cascading wealth effects and credit amplification:

```
Mortgage Rates → Affordability → Purchase Demand →
Home Prices → Household Wealth → Consumer Spending →
Collateral Values → Credit Availability →
Mortgage Rates (Reinforcing Loop)
```

**The Insight:** Housing is a **leveraged bet on rates and demographics**. When mortgage rates spike 400 bps in 18 months (2022-2023), transaction volumes collapse. But prices don't fall proportionally—locked-in sellers refuse to list, creating the "golden handcuffs" phenomenon. The market freezes, not crashes.

The beauty of housing data: it **leads** the broader economy by 6-12 months. Housing peaked in April 2022. The rest of the economy is still catching up. When housing thaws, recovery begins. Until then, we're in stasis.

---

## Why Housing Matters: The Wealth Effect Multiplier

Housing is **15-20% of GDP** directly (residential investment + imputed rent). But its **true impact** is 2-3x larger through:
- **Wealth effect:** $1 of home equity → $0.05-0.08 of additional consumer spending
- **Employment:** Construction, real estate, mortgage finance = 6% of employment
- **Collateral:** Home equity is 70% of median household net worth
- **Credit transmission:** Mortgage delinquencies → bank stress → credit tightening

**The Cascade:**

**1. Housing → Consumer:** Wealth effect drives spending (3-6 month lag)
**2. Housing → Employment:** Construction jobs lead payrolls (2-4 month lag)
**3. Housing → Banking:** Mortgage health determines credit availability (6-12 month lag)
**4. Housing → Inflation:** Shelter is 34% of CPI, 18% of Core PCE (12-18 month lag)
**5. Housing → Fed Policy:** Rate sensitivity makes housing the Fed's primary transmission channel

Get the housing call right, and you've triangulated the consumer, construction, and collateral outlook. Miss it, and you're trading the economy of 2023 while living in 2026.

**Current State:** Housing remains in **frozen equilibrium**—high rates suppressing demand and supply simultaneously. Starts down -23% from peak, existing sales at 30-year lows, but prices stable (+3.8% YoY) because sellers won't list. This isn't health. This is stasis.

---

## Primary Indicators: The Complete Architecture

### A. HOUSING CONSTRUCTION (The Leading Edge)

New construction is the **most leading** housing indicator. Permits lead starts, starts lead completions, completions lead GDP residential investment.

| **Indicator** | **FRED Code** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **Building Permits** | PERMIT | Monthly | **Leads starts 1-2 mo** | Future construction pipeline |
| **Building Permits: Single-Family** | PERMIT1 | Monthly | Leads multi-family 1-2 mo | Core housing demand signal |
| **Building Permits: Multi-Family** | Derived (PERMIT - PERMIT1) | Monthly | Coincident | Rental market demand |
| **Housing Starts** | HOUST | Monthly | **Leads GDP 6-9 mo** | New construction begins |
| **Housing Starts: Single-Family** | HOUST1F | Monthly | Leads GDP 6-9 mo | Owner-occupied construction |
| **Housing Starts: Multi-Family** | Derived (HOUST - HOUST1F) | Monthly | Coincident | Rental construction |
| **Housing Completions** | COMPUTSA | Monthly | Lagging 4-6 mo | Finished units (inventory addition) |
| **Under Construction** | UNDCONTSA | Monthly | Coincident | Work in progress (employment proxy) |

#### Derived Construction Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **Permits-Starts Gap** | (Permits - Starts) / Starts × 100 | >+10% | Pipeline building; <-10% = draining |
| **SF/MF Ratio (Permits)** | SF Permits / MF Permits | <1.5 | Shift to rentals (affordability stress) |
| **Construction Pipeline** | Under Construction / Monthly Completions | >6 months | Supply glut risk |
| **Starts Momentum** | 3M Avg Starts - 12M Avg Starts | <-100k | Deterioration |

#### Regime Thresholds: Construction

| **Indicator** | **Recession** | **Stagnation** | **Expansion** | **Boom** |
|---|---|---|---|---|
| **Housing Starts** | <1.0M | 1.0-1.3M | 1.3-1.6M | >1.6M |
| **SF Starts** | <0.6M | 0.6-0.8M | 0.8-1.0M | >1.0M |
| **Building Permits YoY%** | <-15% | -15% to +5% | +5% to +15% | >+15% |
| **Starts YoY%** | <-10% | -10% to +5% | +5% to +15% | >+15% |

**The Permits-Starts Lead:** Building permits consistently lead starts by 1-2 months. Permits peaked at 1.88M (Jan 2022) and are now at **1.42M** (Dec 2025)—down **-24% from peak**. Starts followed, peaking at 1.80M (April 2022), now at **1.38M** (Dec 2025)—down **-23%**. Housing construction has been in recession for **32 months**.

---

### B. HOME SALES (The Transaction Signal)

Sales volumes tell you about **market liquidity and turnover**. In frozen markets, both buyers and sellers retreat—transactions collapse even as prices hold.

| **Indicator** | **FRED Code** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **New Home Sales** | HSN1F | Monthly | **Leads starts 1-3 mo** | Builder sales (forward-looking) |
| **Existing Home Sales** | EXHOSLUSM495S | Monthly | Coincident | Resale market (backward-looking) |
| **Pending Home Sales Index** | NAR (web) | Monthly | **Leads existing 1-2 mo** | Contracts signed, not closed |
| **MBA Purchase Index** | MBA (web) | Weekly | **Leads sales 4-8 wks** | Mortgage applications for purchase |
| **Months' Supply: New Homes** | MSACSR | Monthly | Coincident | Inventory/sales ratio (new) |
| **Months' Supply: Existing Homes** | Derived | Monthly | Coincident | Inventory/sales ratio (resale) |

#### Derived Sales Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **New/Existing Ratio** | New Sales / Existing Sales | >0.20 | Builders capturing market share |
| **Sales Momentum** | 3M Sales - 12M Avg Sales | <-10% | Deterioration |
| **Transaction Volume ($$)** | Sales × Median Price | YoY < 0% | Market shrinking |
| **MBA Purchase YoY%** | Current - Year Ago | <-10% | Demand weakening |

#### Regime Thresholds: Sales

| **Indicator** | **Frozen** | **Weak** | **Normal** | **Hot** |
|---|---|---|---|---|
| **Existing Home Sales (SAAR)** | <3.5M | 3.5-4.5M | 4.5-5.5M | >5.5M |
| **New Home Sales (SAAR)** | <550k | 550-650k | 650-750k | >750k |
| **Pending Home Sales Index** | <65 | 65-85 | 85-110 | >110 |
| **Months' Supply (Existing)** | >6.0 | 4.0-6.0 | 2.5-4.0 | <2.5 |

**The 30-Year Low:** Existing home sales hit **3.84M** SAAR (Dec 2025)—the **lowest since 1995**. New home sales are at **664k**, holding up better because builders can offer rate buydowns. The new/existing ratio has spiked to **0.17**, highest in decades. Sellers won't list; buyers can only buy new.

---

### C. HOME PRICES (The Wealth Effect Anchor)

Home prices are the **lagging confirmation** of what sales already told you. But they matter enormously for household wealth—$47 trillion in home equity at peak.

| **Indicator** | **Source** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **Case-Shiller National HPI** | S&P/CoreLogic | Monthly | **Lags sales 3-6 mo** | Gold standard, repeat-sales methodology |
| **Case-Shiller 20-City Composite** | S&P/CoreLogic | Monthly | Lags 3-6 mo | Major metro composite |
| **FHFA House Price Index** | FHFA | Monthly | Lags 3-6 mo | Conforming loans only, broader coverage |
| **Zillow Home Value Index** | Zillow | Monthly | **Leads Case-Shiller 1-2 mo** | Real-time estimate (all homes) |
| **Redfin Median Sale Price** | Redfin | Weekly | **Leads Case-Shiller 2-3 mo** | Transaction-based, real-time |
| **Median Existing Home Price** | NAR | Monthly | Coincident | Reported with sales data |
| **Median New Home Price** | Census | Monthly | Coincident | Reported with new sales |

#### Derived Price Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **HPI YoY%** | Current - Year Ago | <0% | Declining (wealth destruction) |
| **Real HPI YoY%** | Nominal HPI YoY - CPI YoY | <-3% | Real depreciation (affordability improving) |
| **Price-Income Ratio** | Median Price / Median Income | >5.5x | Severely unaffordable |
| **Price Momentum** | 3M Ann - 12M Ann | <-5 ppts | Deceleration |

#### Regime Thresholds: Prices

| **Indicator** | **Deflation** | **Stable** | **Appreciation** | **Bubble** |
|---|---|---|---|---|
| **Case-Shiller YoY%** | <0% | 0-3% | 3-8% | >8% |
| **FHFA HPI YoY%** | <0% | 0-4% | 4-10% | >10% |
| **Real HPI YoY%** | <-2% | -2% to +2% | +2% to +5% | >+5% |
| **Price-Income Ratio** | <3.5x | 3.5-4.5x | 4.5-5.5x | >5.5x |

**The Frozen Paradox:** Case-Shiller National HPI at **+3.8% YoY** (Oct 2025). Prices stable despite 30-year low sales. Why? **Supply collapse matched demand collapse.** Existing inventory at 1.13M units (down from 2.5M in 2019). "Golden handcuffs"—sellers with 3% mortgages won't list. No listings = no price pressure. Stasis, not crash.

---

### D. AFFORDABILITY & RATES (The Binding Constraint)

Affordability determines **marginal demand**. When mortgage rates double, monthly payments spike 40%. The buyer pool shrinks. Transactions freeze.

| **Indicator** | **FRED Code** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **30Y Fixed Mortgage Rate** | MORTGAGE30US | Weekly | Coincident | Primary rate benchmark |
| **15Y Fixed Mortgage Rate** | MORTGAGE15US | Weekly | Coincident | Refinance benchmark |
| **10Y Treasury Yield** | DGS10 | Daily | **Leads mortgages 0-1 wk** | Rate floor |
| **Mortgage Spread (30Y - 10Y)** | Derived | Daily | Coincident | MBS credit/prepay risk |
| **Housing Affordability Index** | NAR | Monthly | Lagging 1 mo | 100 = median income qualifies for median home |
| **NAHB Affordability Index** | NAHB | Quarterly | Lagging 1 qtr | Builder-calculated metric |
| **Payment-to-Income Ratio** | Derived | Monthly | Coincident | Monthly mortgage payment / monthly income |

#### Derived Affordability Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **Mortgage Rate YoY Change** | Current Rate - Year Ago | >+100 bps | Demand destruction |
| **Mortgage-Treasury Spread** | 30Y Mortgage - 10Y Treasury | >250 bps | Credit stress elevated |
| **Affordability Gap** | Current Affordability - Historical Avg (100) | <-20 | Severely unaffordable |
| **Payment Shock** | Monthly Payment (Current Rate) - Payment (3% Rate) | >$800/month | Demand frozen |

#### Regime Thresholds: Affordability

| **Indicator** | **Frozen** | **Stretched** | **Normal** | **Easy** |
|---|---|---|---|---|
| **30Y Mortgage Rate** | >7.5% | 6.5-7.5% | 5.0-6.5% | <5.0% |
| **Affordability Index** | <85 | 85-100 | 100-120 | >120 |
| **Payment-to-Income** | >35% | 28-35% | 22-28% | <22% |
| **Mortgage Spread** | >300 bps | 200-300 bps | 150-200 bps | <150 bps |

**The Rate Lock:** 30Y mortgage at **6.95%** (Jan 2026). Median existing home price $387k. Monthly payment: **$2,574** (P&I only). Median household income: $80k. Payment-to-income: **38.6%**—highest on record. Affordability Index at **82**—worst since 1985. The math doesn't work for first-time buyers.

---

### E. INVENTORY & SUPPLY (The Scarcity Signal)

Inventory determines whether price rises or falls. Low inventory = seller's market = prices up. High inventory = buyer's market = prices down.

| **Indicator** | **Source** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **Existing Home Inventory** | NAR | Monthly | Coincident | Active listings (resale) |
| **New Home Inventory** | Census | Monthly | Coincident | Builder inventory (new) |
| **Months' Supply (Existing)** | NAR | Monthly | **Leads prices 3-6 mo** | Inventory/sales ratio |
| **Months' Supply (New)** | Census | Monthly | Leads prices 3-6 mo | Builder inventory/sales |
| **Active Listings (Realtor.com)** | Realtor.com | Weekly | **Leads NAR 2-4 wks** | Real-time inventory |
| **New Listings** | Redfin | Weekly | Leading 2-4 wks | Fresh supply hitting market |
| **Housing Starts Backlog** | Derived | Monthly | Lagging | Under construction - completions |

#### Derived Supply Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **Inventory Gap vs 2019** | Current - 2019 Level | <-40% | Structural undersupply |
| **Months Supply Change** | Current - 6M Ago | >+1.0 mo | Supply building (bearish prices) |
| **New Listings YoY%** | Current - Year Ago | <-10% | Sellers on strike |
| **Construction/Population Growth** | Starts / Population Growth | <1.0x | Undersupply accumulating |

#### Regime Thresholds: Inventory

| **Indicator** | **Undersupplied** | **Balanced** | **Oversupplied** |
|---|---|---|---|
| **Months' Supply (Existing)** | <3.0 | 3.0-5.0 | >5.0 |
| **Months' Supply (New)** | <5.0 | 5.0-7.0 | >7.0 |
| **Existing Inventory Level** | <1.5M | 1.5-2.5M | >2.5M |
| **Active Listings YoY%** | <-10% | -10% to +10% | >+10% |

**The Structural Shortage:** Existing inventory at **1.13M** units—down **55% from 2019's 2.5M**. New home inventory at **490k**—elevated because builders are the only game in town. Months' supply at **3.5 months** for existing (seller's market), **8.9 months** for new (builder excess). The bifurcation: new homes overstocked, existing homes frozen.

---

### F. BUILDER SENTIMENT & ACTIVITY (The Forward Bet)

Builders are the **smart money** in housing. They commit capital 12-18 months ahead of sales. Their sentiment and actions are highly predictive.

| **Indicator** | **Source** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **NAHB Home Builder Confidence** | NAHB | Monthly | **Leads starts 1-3 mo** | Traffic, sales expectations |
| **NAHB: Current Sales** | NAHB | Monthly | Coincident | Present conditions |
| **NAHB: Future Sales** | NAHB | Monthly | **Leads starts 2-4 mo** | 6-month outlook |
| **NAHB: Traffic of Prospective Buyers** | NAHB | Monthly | **Leads sales 1-2 mo** | Foot traffic proxy |
| **Builder Price Cuts (Redfin)** | Redfin | Monthly | Coincident | Desperation gauge |
| **Rate Buydowns Offered** | Builder surveys | Monthly | Coincident | Incentive intensity |

#### Derived Builder Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **NAHB Momentum** | Current - 6M Avg | <-10 | Rapid deterioration |
| **Future-Current Gap** | Future Sales - Current Sales | <-5 | Pessimism about pipeline |
| **Price Cuts Share** | % of Listings with Price Reductions | >30% | Buyer's market |

#### Regime Thresholds: Builder Sentiment

| **Indicator** | **Pessimistic** | **Neutral** | **Optimistic** | **Euphoric** |
|---|---|---|---|---|
| **NAHB Index** | <40 | 40-50 | 50-65 | >65 |
| **Future Sales Component** | <45 | 45-55 | 55-70 | >70 |
| **Traffic Component** | <30 | 30-45 | 45-55 | >55 |

**The Builder Pivot:** NAHB at **47** (Dec 2025)—below the neutral 50 line but recovering from 31 low (Dec 2022). Builders adapting: smaller homes, rate buydowns (effectively 5.5% vs market 6.95%), incentives. They're selling new homes by subsidizing affordability. This works until it doesn't.

---

### G. MORTGAGE MARKET HEALTH (The Credit Channel)

Mortgage credit health determines whether housing stress transmits to the banking system. Delinquencies and defaults matter for systemic risk.

| **Indicator** | **FRED Code** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **Mortgage Delinquency Rate (30+ Days)** | DRSFRMACBS | Quarterly | Lagging 1-2 qtrs | Stress gauge |
| **Mortgage Delinquency Rate (90+ Days)** | DRSFRM | Quarterly | Lagging 2-3 qtrs | Serious delinquency |
| **Foreclosure Rate** | MBA | Quarterly | Lagging 3-6 qtrs | End-stage stress |
| **Mortgage Originations** | MBA | Quarterly | Coincident | Lending activity |
| **Refinance Activity** | MBA | Weekly | Coincident | Rate sensitivity gauge |
| **Home Equity as % of Value** | FRED (Z.1) | Quarterly | Lagging | Equity cushion |
| **Negative Equity Share** | CoreLogic | Quarterly | Lagging | Underwater borrowers |

#### Derived Credit Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **Delinquency Trend** | Current 30+ Day - Year Ago | >+0.5 ppt | Stress building |
| **Equity Cushion** | Median Equity / Median Value | <20% | Negative equity risk |
| **Originations YoY%** | Current - Year Ago | <-20% | Credit contraction |
| **Refi Share of Apps** | Refi Apps / Total Apps | <20% | Rate-locked homeowners |

#### Regime Thresholds: Credit Health

| **Indicator** | **Crisis** | **Stressed** | **Normal** | **Healthy** |
|---|---|---|---|---|
| **30+ Day Delinquency** | >5.0% | 3.5-5.0% | 2.5-3.5% | <2.5% |
| **90+ Day Delinquency** | >2.0% | 1.0-2.0% | 0.5-1.0% | <0.5% |
| **Negative Equity Share** | >10% | 5-10% | 2-5% | <2% |
| **Foreclosure Rate** | >3.0% | 1.5-3.0% | 0.5-1.5% | <0.5% |

**The Equity Buffer:** Mortgage delinquency (30+) at **2.1%** (Q3 2025)—historically low. Negative equity share at **1.8%**—lowest ever. Why? Homeowners locked in 3% rates with massive equity cushions (median equity $315k). No forced selling = no price crash. This is the **opposite** of 2008. The stress is in transaction volumes and construction, not credit quality.

---

### H. RENTAL MARKET (The Affordability Release Valve)

When buying becomes unaffordable, people rent. Rental market dynamics affect housing demand, shelter inflation, and multifamily construction.

| **Indicator** | **Source** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **Zillow Rent Index** | Zillow | Monthly | **Leads CPI Shelter 12 mo** | Real-time market rents |
| **Apartment List Rent Index** | Apartment List | Monthly | Leads CPI 10-12 mo | National median rent |
| **CoreLogic Single-Family Rent** | CoreLogic | Monthly | Leads CPI 12 mo | SFR rental market |
| **Vacancy Rate (Rental)** | Census | Quarterly | Lagging 1-2 qtrs | Supply/demand balance |
| **Multifamily Starts** | Census | Monthly | **Leads supply 18-24 mo** | Future rental supply |
| **Multifamily Completions** | Census | Monthly | Coincident | Current supply additions |

#### Derived Rental Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **Market Rent → CPI Lag** | Zillow YoY (12M Prior) vs CPI Shelter | Gap = mechanical disinflation | Predictive for shelter CPI |
| **Rent-to-Own Ratio** | Median Rent × 12 / Median Price | >6% | Renting preferable |
| **MF Completions vs Absorption** | Completions - Net Absorption | >0 | Oversupply building |

#### Regime Thresholds: Rental

| **Indicator** | **Deflationary** | **Stable** | **Inflationary** |
|---|---|---|---|
| **Zillow Rent YoY%** | <0% | 0-4% | >4% |
| **Rental Vacancy Rate** | >8% | 6-8% | <6% |
| **MF Starts YoY%** | <-20% | -20% to +20% | >+20% |

**The Rental Reset:** Zillow rent growth at **+2.8% YoY** (Dec 2025)—normalizing from +16% peak (Feb 2022). Rental vacancy at **6.8%**—rising as multifamily completions hit record highs (500k+ units in 2025). This is **pipeline disinflation** for shelter CPI. Rents already slowed; CPI shelter will follow by mid-2026.

---

## Housing Pillar Composite Index (HCI)

### Formula

The Housing Pillar Composite synthesizes construction, sales, prices, affordability, and credit into a single housing cycle indicator:

```
HCI = 0.20 × z(Housing_Starts_YoY)
    + 0.15 × z(Existing_Home_Sales_YoY)
    + 0.15 × z(NAHB_Index)
    + 0.15 × z(-Months_Supply)                    # Inverted (high supply = weak)
    + 0.10 × z(HPI_YoY)
    + 0.10 × z(-30Y_Mortgage_Rate)                # Inverted (high rates = weak)
    + 0.10 × z(MBA_Purchase_Index_YoY)
    + 0.05 × z(-Mortgage_Delinquency_30Day)       # Inverted (high DQ = weak)
```

**Component Weighting Rationale:**
- **Housing Starts (20%):** Most leading indicator, GDP impact
- **Existing Sales (15%):** Transaction volume, market liquidity
- **NAHB Index (15%):** Builder forward bet, sentiment
- **Months' Supply (15%):** Price direction signal (inverted)
- **HPI YoY (10%):** Wealth effect anchor
- **Mortgage Rate (10%):** Affordability binding constraint (inverted)
- **MBA Purchase (10%):** Real-time demand gauge
- **Delinquency (5%):** Credit health (inverted)

### Interpretation

| **HCI Range** | **Regime** | **Construction Allocation** | **Signal** |
|---|---|---|---|
| > +1.0 | Housing Boom | Overweight homebuilders, lumber | Full expansion |
| +0.5 to +1.0 | Expansion | Neutral homebuilders | Healthy growth |
| -0.5 to +0.5 | Neutral/Stagnation | Underweight construction | Range-bound |
| -1.0 to -0.5 | Contraction | **Avoid homebuilders** | Housing recession |
| < -1.0 | Crisis | Maximum underweight | Systemic risk |

### Historical Calibration

| **Period** | **HCI** | **Regime** | **Outcome (12M Forward)** |
|---|---|---|---|
| **Dec 2005** | +1.4 | Boom | Housing peak (bubble bursting) |
| **Dec 2007** | -1.5 | Crisis | Systemic collapse, GFC |
| **Dec 2011** | -0.8 | Contraction | Bottom formation, recovery beginning |
| **Dec 2019** | +0.6 | Expansion | Pre-COVID strength |
| **Dec 2021** | +1.2 | Boom | Rate shock coming |
| **Dec 2022** | -0.9 | Contraction | Maximum rate pain |
| **Dec 2025** | **-0.6** | **Contraction** | **Frozen equilibrium** |

**Current Assessment (Dec 2025):** HCI at **-0.6** places housing in "Contraction" regime—better than -0.9 trough (Dec 2022) but still negative. The market is **frozen, not crashing**:
- **Starts at -8.2% YoY** (construction recession)
- **Existing sales at -3.5% YoY** (30-year transaction low)
- **NAHB at 47** (recovering but below neutral)
- **Mortgage rates at 6.95%** (affordability frozen)
- **HPI at +3.8% YoY** (stable due to supply collapse)
- **Delinquency at 2.1%** (healthy—no forced selling)

This is **1990s Japan**, not 2008 America. No credit crisis. Just frozen transactions as sellers refuse to list and buyers can't afford.

---

## Lead/Lag Relationships: The Housing Cascade

```
LEADING                           COINCIDENT                  LAGGING
────────────────────────────────────────────────────────────────────────────────────
│                                 │                          │
│  MBA Purchase Index (4-8 wks)   │  Housing Starts          │  Case-Shiller HPI (3-6 mo)
│  Building Permits (1-2 mo)      │  Existing Home Sales     │  CPI Shelter (12-18 mo)
│  NAHB Index (1-3 mo)            │  New Home Sales          │  Mortgage Delinquency (1-2 qtrs)
│  Mortgage Rate Changes (1-2 mo) │  Active Inventory        │  Foreclosures (3-6 qtrs)
│  Pending Home Sales (1-2 mo)    │  Months' Supply          │  FHFA HPI (3-6 mo)
│  Zillow Rent Index (12 mo→CPI)  │  Median Prices           │  Residential Investment GDP
│  10Y Treasury (0-1 wk→Mortgage) │  Completions             │  Home Equity Loans
│  Redfin Listings Data (2-4 wks) │                          │  Property Tax Receipts
│                                 │                          │
────────────────────────────────────────────────────────────────────────────────────
```

**The Critical Chain:**

**1. Mortgage rates rise** (Fed hikes, Treasury selloff) → 4-8 weeks later → **MBA purchase apps collapse**
**2. Purchase apps collapse** → 1-2 months later → **Sales volumes drop**
**3. Sales drop + Supply frozen** → 3-6 months later → **Prices adjust (or don't, if supply collapses)**
**4. Construction slows** → 6-9 months later → **GDP residential investment contracts**
**5. Market rents cool** → 12-18 months later → **CPI shelter falls** (mechanical)

This isn't theory. This is the transmission mechanism that's been running for 36 months since the rate shock began.

---

## Integration with Three-Engine Framework

### Pillar 4 → Pillar 1 (Labor)

Housing drives **construction employment** (7.5M jobs) and related sectors (real estate, finance, furniture):

```
Housing Starts ↓ → Construction Employment ↓ →
Related Retail ↓ → Consumer Spending ↓ →
Broader Payrolls ↓
```

**Current Linkage:** Housing starts at -8.2% YoY. Construction employment peaked at 8.0M (2023), now at **7.85M** (-1.9% from peak). Related sectors (real estate, mortgage) shedding jobs. This feeds into LFI.

**Cross-Pillar Signal:** When **HCI < -0.5** (housing contraction) AND **LFI > +0.8** (labor fragility), recession risk exceeds 60% within 12 months. Current: **HCI -0.6, LFI +0.93**. **Warning threshold engaged.**

---

### Pillar 4 → Pillar 2 (Prices)

Housing determines **34% of CPI** (shelter) with a 12-18 month lag:

```
Market Rents (Zillow) ↓ → 12-18 month lag →
CPI Shelter ↓ → Core CPI ↓ → Core PCE ↓
```

**Current Linkage:** Zillow rent growth at +2.8% (Dec 2025), down from +16% peak (Feb 2022). This implies CPI Shelter will fall to ~3.0% by Q2 2026 (currently 5.1%). **Mechanical disinflation** baked in.

**Cross-Pillar Signal:** Housing is the **primary driver** of the remaining inflation overshoot. Shelter at 5.1% contributes **~1.7 ppts** to core CPI. When this normalizes to 3.0%, core CPI falls to ~2.8%. The Fed knows this—they're waiting.

---

### Pillar 4 → Pillar 3 (Growth)

Housing is **15-20% of GDP** directly, but **2-3x larger** through multiplier effects:

```
Residential Investment ↓ → GDP Growth ↓
Wealth Effect ↓ → Consumer Spending ↓ → GDP ↓
Construction Employment ↓ → Income ↓ → Spending ↓
```

**Current Linkage:** Residential fixed investment at **-4.2% QoQ Ann** (Q3 2025)—has been contracting for 8 consecutive quarters. This is **subtracting ~0.2 ppts** from GDP each quarter. Housing is a direct drag on growth.

**Cross-Pillar Signal:** When **HCI < -0.5** (housing contraction) AND **GCI < -0.3** (growth weak), the housing drag accelerates broader slowdown. Current: **HCI -0.6, GCI -0.4**. **Synchronized weakness.**

---

### Pillar 4 → Pillar 9 (Financial/Rates)

Housing is **hyper-sensitive** to interest rates—the Fed's primary transmission mechanism:

```
Fed Funds ↑ → 10Y Treasury ↑ → Mortgage Rates ↑ →
Affordability ↓ → Housing Demand ↓ → Construction ↓
```

**Current Linkage:** Fed Funds at 4.25-4.50%, 10Y Treasury at 4.60%, 30Y mortgage at 6.95%. The **mortgage spread** (30Y - 10Y) at **235 bps**—still elevated vs. historical 150-180 bps due to MBS volatility/prepay uncertainty.

**The Rate Sensitivity:** Every 100 bps in mortgage rates = ~10% change in affordability = ~5-10% change in sales volumes. If Fed cuts 100 bps (to 3.25-3.50%), mortgages might fall to 6.0-6.5%, thawing some demand. But not returning to 2021 levels.

---

## Data Source Summary

| **Category** | **Primary Source** | **Frequency** | **Release Lag** | **FRED Availability** |
|---|---|---|---|---|
| **Starts/Permits** | Census Bureau | Monthly | ~17 days | Same day (HOUST, PERMIT) |
| **New Home Sales** | Census Bureau | Monthly | ~26 days | Same day (HSN1F) |
| **Existing Home Sales** | NAR | Monthly | ~22 days | Delayed (EXHOSLUSM495S) |
| **Case-Shiller HPI** | S&P/CoreLogic | Monthly | ~60 days | Same day (CSUSHPINSA) |
| **FHFA HPI** | FHFA | Monthly | ~55 days | Same day (USSTHPI) |
| **Mortgage Rates** | Freddie Mac | Weekly | ~3 days | Same day (MORTGAGE30US) |
| **NAHB Index** | NAHB | Monthly | ~15 days | Web scrape (not in FRED) |
| **Zillow Rent/HVI** | Zillow | Monthly | ~5 days | Web scrape (not in FRED) |
| **MBA Purchase Index** | MBA | Weekly | ~3 days | Web scrape (not in FRED) |
| **Delinquency** | MBA | Quarterly | ~45 days | Fed Z.1 (DRSFRMACBS) |

**Critical Timing:** Housing starts released mid-month (~17th), provides **real-time construction pulse**. Case-Shiller delayed 60 days—use Zillow/Redfin for real-time price signals. MBA weekly for highest-frequency demand gauge.

---

## Current State Assessment (January 2026)

| **Indicator** | **Current** | **Threshold** | **Assessment** |
|---|---|---|---|
| **Housing Starts** | 1.38M | <1.3M = stagnation | 🟡 Low-end normal |
| **Starts YoY%** | -8.2% | <-10% = recession | 🟡 **Weak** |
| **Existing Home Sales** | 3.84M | <4.0M = frozen | 🔴 **30-year low** |
| **New Home Sales** | 664k | <600k = recession | 🟢 Holding (builder buydowns) |
| **Case-Shiller YoY%** | +3.8% | <0% = deflation | 🟢 **Stable** (supply collapse) |
| **30Y Mortgage Rate** | 6.95% | >7.0% = frozen | 🟡 Elevated |
| **Affordability Index** | 82 | <90 = crisis | 🔴 **Worst since 1985** |
| **NAHB Index** | 47 | <45 = pessimistic | 🟡 Recovering |
| **Months' Supply (Existing)** | 3.5 mo | >5.0 = oversupply | 🟢 Tight (no supply) |
| **Mortgage Delinquency** | 2.1% | >3.5% = stressed | 🟢 **Healthy** |
| **HCI Estimate** | **-0.6** | <-0.5 = contraction | 🟡 **Housing Contraction** |

### Narrative Synthesis

Housing is in **frozen equilibrium**—the market that refuses to crash or recover.

**The Freeze:**
- **Transaction volumes at 30-year lows** (existing sales 3.84M)
- **Affordability at 40-year lows** (index at 82)
- **Mortgage rates near cycle highs** (6.95%)
- **Construction in recession** (starts -8.2% YoY, 32 months from peak)

**The Paradox:**
- **Prices stable** (+3.8% YoY) because supply collapsed alongside demand
- **No forced selling** (delinquency 2.1%, equity $315k median)
- **Inventory at record lows** (1.13M existing, -55% vs 2019)
- **"Golden handcuffs"**—sellers with 3% mortgages won't list

**Translation:** This isn't 2008. Credit quality is pristine. There's no wave of defaults or foreclosures coming. The problem is **market dysfunction**—transactions frozen, mobility impaired, construction activity depressed. Housing is a drag on GDP and employment, but not a systemic financial risk.

**Cross-Pillar Confirmation:**
- **Labor Pillar:** Construction jobs -1.9% from peak, related sectors (real estate, mortgage) shedding
- **Prices Pillar:** Shelter CPI at 5.1% but market rents at 2.8%—mechanical disinflation coming
- **Growth Pillar:** Residential investment subtracting ~0.2 ppts from GDP quarterly

**MRI (Macro Risk Index):** Housing contributes **-0.6 (HCI)** to macro risk—a drag, not a crisis. The frozen market creates **stasis risk** (impaired mobility, depressed construction), not **tail risk** (credit crisis, forced selling, systemic contagion).

---

## Invalidation Criteria

### Bull Case (Housing Thaw) Invalidation Thresholds

If the following occur **simultaneously for 3+ months**, the bearish housing thesis is invalidated:

✅ **30Y Mortgage Rate** drops below **6.0%** (affordability improving)
✅ **Existing Home Sales** exceed **4.5M SAAR** (+15% from current)
✅ **Housing Starts** exceed **1.5M** (+9% from current)
✅ **NAHB Index** exceeds **55** (builder optimism)
✅ **MBA Purchase Index YoY%** turns **positive** (+10%+)
✅ **HCI** exceeds **+0.3** (neutral regime)

**Action if Invalidated:** Rotate to **homebuilders** (XHB, ITB), **building materials** (lumber, copper), **home improvement** (HD, LOW). Housing thaw = consumer confidence revival.

---

### Bear Case (Housing Crisis) Confirmation Thresholds

If the following occur, housing is **deteriorating beyond frozen into crisis**:

🔴 **Mortgage Delinquency 30+** exceeds **4.0%** (credit stress emerging)
🔴 **Existing Home Sales** drop below **3.0M** (market paralysis)
🔴 **Case-Shiller YoY%** turns **negative** for 3+ months (price deflation)
🔴 **Housing Starts** drop below **1.0M** (construction collapse)
🔴 **Negative Equity Share** exceeds **5%** (forced selling catalyst)
🔴 **HCI** drops below **-1.0** (crisis regime)

**Action if Confirmed:** Maximum defensive. Avoid **all housing exposure** (homebuilders, REITs, mortgage lenders). Overweight **cash** (SGOV), **long duration** (TLT). Housing crisis = recession confirmation.

---

## Conclusion: Housing as the Frozen Collateral

Housing isn't shelter. It's **$47 trillion in collateral** that determines wealth, spending, and credit transmission.

The current configuration is **unprecedented**—not 2008-style crisis, not 1990s-style recovery. It's **frozen equilibrium**:
- Rates too high to buy
- Equity too valuable to sell
- Supply too scarce to crash
- Demand too weak to rally

**Current State:**
- **HCI -0.6** (Contraction Regime, but not crisis)
- **Starts at 1.38M** (construction recession, 32 months from peak)
- **Existing sales at 3.84M** (30-year low)
- **Prices at +3.8% YoY** (stable due to supply collapse)
- **Affordability at 82** (worst since 1985)
- **Delinquency at 2.1%** (pristine credit)

**The Thaw Catalyst:** Mortgage rates below 6.0% would unlock ~15% of locked-in sellers (those with rates above 5.5%). That requires Fed cuts + MBS spread normalization. Timeline: Q3 2026 earliest if inflation cooperates.

**Until then:** Stasis. Frozen transactions. Impaired mobility. Construction drag on GDP. But not a crash.

**That's our view from the Watch. Until next time, we'll be sure to keep the light on....**

*Bob Sheehan, CFA, CMT*
*Founder & CIO, Lighthouse Macro*
*January 15, 2026*
