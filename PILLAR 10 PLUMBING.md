# PILLAR 10: PLUMBING

## The Liquidity Transmission Chain

Plumbing isn't just Fed policy—it's the **$8 trillion reservoir** that determines whether monetary policy reaches the real economy. The transmission mechanism operates through cascading liquidity flows:

```
Fed Balance Sheet → Reserves → Bank Balance Sheets →
Dealer Intermediation → Repo Markets →
Money Market Rates → Financial Conditions →
Asset Prices → Real Economy
```

**The Insight:** Liquidity transmits **mechanically**: RRP → Reserves → Dealer Balance Sheets → Repo → Risk Assets. When the RRP buffer is exhausted (it is), small shocks cause big damage. The system has lost its shock absorber. We're operating without a cushion for the first time since 2019.

The beauty of plumbing data: it's **observable in real-time**. Unlike GDP or inflation, you can see reserve levels daily. You can watch repo rates tick. You can track RRP drainage. The plumbing doesn't lie—it shows you where stress is building before it surfaces in asset prices.

---

## Why Plumbing Matters: The Hidden Infrastructure

Plumbing is the **invisible infrastructure** that connects Fed policy to financial conditions. When it works, no one notices. When it breaks, everyone notices—violently.

**The Cascade:**

**1. Plumbing → Money Markets:** Reserve levels determine repo rates (immediate)
**2. Plumbing → Banks:** Reserve scarcity constrains bank intermediation (1-4 weeks)
**3. Plumbing → Dealers:** Balance sheet capacity determines Treasury market liquidity (coincident)
**4. Plumbing → Asset Prices:** Funding stress transmits to risk assets (1-7 days)
**5. Plumbing → Financial Stability:** Extreme stress triggers intervention (crisis events)

Get the plumbing call right, and you've anticipated the next repo spike, Treasury dislocation, or liquidity crisis. Miss it, and you're surprised by September 2019, March 2020, or the next event.

**Current State:** The system is **operating without a buffer**. RRP drained from $2.3T (Dec 2022) to **$150B** (Jan 2026). Reserves at **$3.3T**—above the "lowest comfortable level" but falling. QT continuing at $60B/month. Treasury issuance at $2T+/year. Dealer balance sheets stretched. The margin for error is gone.

---

## Primary Indicators: The Complete Architecture

### A. FED BALANCE SHEET (The Reservoir)

The Fed's balance sheet is the **source of all liquidity**. Assets minus liabilities equals reserves plus currency. QT drains the reservoir.

| **Indicator** | **FRED Code** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **Total Fed Assets** | WALCL | Weekly | Coincident | Total balance sheet size |
| **SOMA Holdings (Treasuries)** | TREAST | Weekly | Coincident | QT impact on Treasuries |
| **SOMA Holdings (MBS)** | WSHOMCB | Weekly | Coincident | QT impact on MBS |
| **Reserve Balances** | WRBWFRBL | Weekly | Coincident | Bank reserves at Fed |
| **ON RRP Facility** | RRPONTSYD | Daily | Coincident | MMF cash parked at Fed |
| **TGA Balance** | WTREGEN | Weekly | Coincident | Treasury cash at Fed |
| **Currency in Circulation** | WCURCIR | Weekly | Coincident | Drain on reserves |
| **Foreign Repo Pool (FRP)** | H.4.1 | Weekly | Coincident | Foreign official cash |
| **Standing Repo Facility (SRF)** | NY Fed | Daily | Coincident | Emergency lending |
| **Discount Window** | WLCFLPCL | Weekly | Coincident | Last resort lending |

#### Derived Balance Sheet Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **Reserves/Assets** | Reserves / Total Assets | <13% | Scarcity zone |
| **Fed Liquidity Ratio** | (Reserves + RRP) / Bank Assets | <15% | System liquidity thin |
| **QT Pace (Monthly)** | Change in SOMA | >$60B | Aggressive drain |
| **Reserve Runway** | (Reserves - LCLOR) / Monthly QT | <12 mo | QT end approaching |
| **RRP Cushion** | RRP Balance | <$200B | Buffer exhausted |

#### Regime Thresholds: Balance Sheet

| **Indicator** | **Scarce** | **Ample** | **Abundant** | **Excess** |
|---|---|---|---|---|
| **Reserves ($T)** | <$3.0T | $3.0-3.5T | $3.5-4.5T | >$4.5T |
| **Reserves/GDP** | <11% | 11-13% | 13-17% | >17% |
| **RRP Balance** | <$200B | $200B-$1T | $1T-$2T | >$2T |
| **Fed Liquidity Ratio** | <13% | 13-18% | 18-25% | >25% |

**The Vanishing Buffer:** RRP peaked at **$2.55T** (Dec 2022)—the system's shock absorber. Now at **$150B** (Jan 2026)—**94% drained**. Reserves at **$3.3T**, down from $4.2T peak. Fed liquidity ratio at **14.5%**—approaching the 13% scarcity zone. The cushion that absorbed shocks for three years is gone. From here, every reserve drain hits bank balance sheets directly.

---

### B. RESERVE SCARCITY FRAMEWORK (The Critical Threshold)

Reserve scarcity is the **state variable** that determines whether the system operates smoothly or stress emerges. Multiple indicators triangulate scarcity.

| **Indicator** | **Source** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **EFFR - IORB Spread** | NY Fed | Daily | **Leading 1-4 wks** | Reserve scarcity signal |
| **Reserve Demand Elasticity (RDE)** | NY Fed Research | Quarterly | Leading | Sensitivity of rates to reserves |
| **Lowest Comfortable Level (LCLOR)** | Fed Estimates | Periodic | Benchmark | Floor for reserves |
| **Reserves vs LCLOR Gap** | Derived | Weekly | Leading | Distance to scarcity |
| **Bank Repo Activity** | H.8 | Weekly | Coincident | Banks deploying reserves |
| **SOFR - IORB Spread** | NY Fed | Daily | Coincident | Bank repo arbitrage |

#### Derived Scarcity Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **EFFR - IORB** | EFFR - IORB | >+5 bps | Scarcity emerging |
| **LCLOR Gap** | Reserves - LCLOR Est (~$3.0T) | <$300B | Near scarcity |
| **Scarcity Probability** | Model-based | >50% | Fed attention needed |
| **Reserve Runway (Months)** | Gap / Monthly Drain | <6 mo | QT pause imminent |

#### Regime Thresholds: Reserve Scarcity

| **Indicator** | **Scarce** | **Tight** | **Ample** | **Abundant** |
|---|---|---|---|---|
| **EFFR - IORB** | >+10 bps | +3 to +10 bps | -3 to +3 bps | <-3 bps |
| **Reserves vs LCLOR** | <$0 | $0-$300B | $300B-$800B | >$800B |
| **SOFR - IORB** | >+10 bps | +3 to +10 bps | -5 to +3 bps | <-5 bps |
| **Bank Repo YoY%** | >+20% | +10 to +20% | 0 to +10% | <0% |

**The September 2019 Precedent:** EFFR spiked 300 bps in one day when reserves hit $1.4T (then-LCLOR). The Fed didn't see it coming. Today's LCLOR estimate: **~$3.0T**. Current reserves: **$3.3T**. Gap: **$300B**—roughly 5 months of QT runway at current pace. We're closer to the edge than 2019, but the Fed is watching more carefully.

---

### C. REPO MARKETS (The Transmission Mechanism)

Repo markets are **where the plumbing meets the real economy**. Dealers fund Treasuries via repo. Hedge funds lever positions via repo. MMFs deploy cash via repo. Everything connects here.

| **Indicator** | **Source** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **SOFR** | NY Fed | Daily | Coincident | Secured overnight rate (benchmark) |
| **TGCR** | NY Fed | Daily | Coincident | Tri-party general collateral |
| **BGCR** | NY Fed | Daily | Coincident | Broad general collateral |
| **GCF Repo Rate** | DTCC | Daily | Coincident | Interdealer (FICC cleared) |
| **DVP Repo Rate** | NY Fed | Daily | Coincident | Bilateral delivery-vs-payment |
| **TPR (Tri-Party Repo)** | NY Fed | Daily | Coincident | MMF to dealer |
| **SOFR Percentiles** | NY Fed | Daily | Coincident | Distribution (1st, 25th, 75th, 99th) |
| **Repo Volume** | NY Fed | Daily | Coincident | Transaction volume |

#### Derived Repo Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **SOFR - RRP** | SOFR - ON RRP Rate | <+5 bps | Cash abundance |
| **TGCR - RRP** | TGCR - ON RRP | <0 | Excess cash (MMFs prefer RRP) |
| **GCF - TPR** | GCF - TPR | >+15 bps | Dealer balance sheet stress |
| **SOFR 99th - SOFR Median** | Tail spread | >+20 bps | Funding stress in tails |
| **SOFR - SRF** | Distance to ceiling | <-10 bps | Approaching stress facility |

#### Regime Thresholds: Repo Markets

| **Indicator** | **Stress** | **Tight** | **Normal** | **Easy** |
|---|---|---|---|---|
| **SOFR - IORB** | >+15 bps | +5 to +15 bps | -5 to +5 bps | <-5 bps |
| **GCF - TPR** | >+20 bps | +10 to +20 bps | 0 to +10 bps | <0 bps |
| **SOFR 99th Percentile** | >SRF rate | +15 to SRF | +5 to +15 bps vs median | <+5 bps |
| **TGCR - RRP** | >+15 bps | +5 to +15 bps | -5 to +5 bps | <-5 bps |

**The Collateral vs Cash Regime:** TGCR - RRP tells you whether the system has **excess cash** (negative spread, MMFs prefer RRP) or **excess collateral** (positive spread, collateral is scarce). Currently: **+8 bps**—slight excess collateral as RRP drains and Treasury supply rises. When collateral is excessive (many Treasuries, few buyers), repo rates rise. When cash is excessive (few Treasuries, much cash), repo rates fall to RRP floor.

---

### D. DEALER BALANCE SHEETS (The Bottleneck)

Primary dealers are the **choke point** in the system. They intermediate between the Fed, Treasury, hedge funds, and MMFs. Their balance sheet capacity determines market functioning.

| **Indicator** | **Source** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **Dealer Net UST Position** | NY Fed | Weekly | Coincident | Inventory congestion |
| **Dealer Fails** | NY Fed | Weekly | **Leading 1-2 wks** | Settlement stress |
| **Securities Lending (Fed)** | H.4.1 | Weekly | Coincident | Collateral relief |
| **Primary Dealer Repo Borrowing** | FR2004 | Monthly | Coincident | Funding needs |
| **Auction Primary Dealer Take-Down** | Treasury | Per auction | Coincident | Forced absorption |

#### Derived Dealer Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **Dealer Position % of Issuance** | Net Position / Monthly Issuance | >100% | Congestion |
| **Fails Trend** | Current - 4-wk Avg | >+$5B | Settlement stress |
| **Auction Absorption** | Dealer Take-Down % | >18% | Weak end-demand |
| **GCF - TPR (Sheet Flex)** | Interdealer - Tri-party spread | >+15 bps | Inflexible sheets |

#### Regime Thresholds: Dealer Balance Sheets

| **Indicator** | **Congested** | **Stretched** | **Normal** | **Flexible** |
|---|---|---|---|---|
| **Net UST Position ($B)** | >$80B | $50-80B | $20-50B | <$20B |
| **Dealer Fails ($B weekly)** | >$50B | $25-50B | $10-25B | <$10B |
| **Dealer Take-Down %** | >20% | 15-20% | 10-15% | <10% |
| **GCF - TPR Spread** | >+20 bps | +10 to +20 | 0 to +10 | <0 bps |

**The Great Dealer Sheet Congestion:** Dealer net UST positions at **$65B** (Jan 2026)—elevated as Treasury issuance overwhelms end-demand. Dealers absorbing 17% of auctions (vs 12% historical). GCF - TPR at **+12 bps**—balance sheets inflexible. When dealers are stuffed with inventory, they can't intermediate. Bid-ask spreads widen. Liquidity evaporates. The "basis trade" unwind of March 2020 happened when dealers couldn't absorb.

---

### E. HEDGE FUND LEVERAGE (The Fragility Amplifier)

Hedge funds are the **marginal buyers** of Treasuries via the basis trade (long cash, short futures). They fund positions in repo. When repo tightens, they're forced sellers.

| **Indicator** | **Source** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **HF Total UST Repo Borrowing** | OFR | Quarterly | Lagging | Leverage level |
| **Top-10 HF Repo Borrowing** | OFR | Quarterly | Lagging | Concentration risk |
| **CFTC UST Futures Shorts (Levered)** | CFTC | Weekly | Coincident | Basis trade proxy |
| **CFTC UST Futures Longs (Asset Mgr)** | CFTC | Weekly | Coincident | Duration demand |
| **Treasury Basis Spread** | Derived | Daily | Coincident | Trade profitability |

#### Derived HF Leverage Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **HF Repo Concentration** | Top-10 / Total HF Repo | >50% | Concentration risk |
| **Levered Short Position** | CFTC net short (levered funds) | >$800B notional | Elevated basis trade |
| **Basis Trade Carry** | Cash yield - Futures implied | <+5 bps | Trade unprofitable |
| **HF Repo Growth YoY%** | Current - Year Ago | >+25% | Leverage building |

#### Regime Thresholds: HF Leverage

| **Indicator** | **Fragile** | **Elevated** | **Normal** | **Low** |
|---|---|---|---|---|
| **HF UST Repo ($T)** | >$1.0T | $0.7-1.0T | $0.4-0.7T | <$0.4T |
| **Levered Futures Shorts ($B)** | >$900B | $600-900B | $300-600B | <$300B |
| **Top-10 Concentration** | >55% | 45-55% | 35-45% | <35% |
| **Basis Spread (bps)** | <+3 | +3 to +8 | +8 to +15 | >+15 |

**The Basis Trade Buildup:** Levered fund UST futures shorts at **$850B** notional (Jan 2026)—near record highs. Hedge fund repo borrowing at **$950B**—also near records. Top-10 concentration at **52%**—risk concentrated. The basis trade works until repo funding tightens, at which point levered funds are forced to unwind. That's March 2020. That's what happens when reserves hit scarcity and dealers can't intermediate.

---

### F. MONEY MARKET FUND ALLOCATION (The Cash Distribution)

MMFs are the **cash reservoirs** that choose between RRP, repo, and bills. Their allocation decisions determine whether cash reaches the private sector or stays parked at the Fed.

| **Indicator** | **Source** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **MMF AUM** | ICI | Weekly | Coincident | Total cash available |
| **MMF RRP Usage** | NY Fed | Daily | Coincident | Cash parked at Fed |
| **MMF Repo to Dealers** | OFR | Monthly | Lagging | Private repo allocation |
| **MMF T-Bill Holdings** | OFR | Monthly | Lagging | Bill allocation |
| **Bill Yields vs RRP** | FRED | Daily | Coincident | Allocation incentive |

#### Derived MMF Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **RRP as % of MMF AUM** | RRP / MMF AUM | <5% | RRP exhausted |
| **Bill Spread vs RRP** | 1M Bill - RRP Rate | >+10 bps | Bills attractive |
| **Private Repo Share** | Dealer Repo / (RRP + Repo + Bills) | >40% | Private funding strong |
| **MMF AUM Growth YoY%** | Current - Year Ago | >+15% | Cash inflows |

#### Regime Thresholds: MMF Allocation

| **Indicator** | **RRP Full** | **Balanced** | **Private** | **RRP Empty** |
|---|---|---|---|---|
| **RRP as % of AUM** | >30% | 15-30% | 5-15% | <5% |
| **Bill Spread vs RRP** | <0 bps | 0-10 bps | 10-20 bps | >+20 bps |
| **Private Repo Share** | <25% | 25-35% | 35-50% | >50% |

**The RRP Drain Completed:** RRP at **$150B** vs MMF AUM of **$6.8T** = **2.2%** allocation to RRP (vs 35% at peak). The drain is essentially complete. MMFs have reallocated to bills (~55%) and private repo (~42%). This is **healthy for liquidity transmission**—cash is reaching the private sector. But it means the buffer is gone. Future reserve drains hit bank balance sheets directly.

---

### G. FHLB & BANK FUNDING (The Domestic Plumbing)

Federal Home Loan Banks (FHLBs) and commercial banks form the **domestic funding chain**. FHLBs are the "lender of next-to-last resort"—they step in when interbank funding tightens.

| **Indicator** | **Source** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **EFFR** | NY Fed | Daily | Coincident | Unsecured overnight (fed funds) |
| **OBFR** | NY Fed | Daily | Coincident | Bank overnight funding |
| **Fed Funds Volumes** | NY Fed | Daily | Coincident | Interbank activity |
| **FHLB Advances** | FHLB OF | Quarterly | Lagging | Advances to member banks |
| **FHLB Liquidity** | FHLB OF | Quarterly | Lagging | Available lending capacity |
| **Fed Funds Lenders (FHLB share)** | NY Fed | Daily | Coincident | FHLB role |
| **Fed Funds Borrowers (FBO share)** | NY Fed | Daily | Coincident | Foreign bank stress |

#### Derived Bank Funding Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **SOFR - EFFR** | Secured - Unsecured | >+10 bps | FHLB stress |
| **EFFR - IORB** | Fed funds scarcity | >+5 bps | Reserve scarcity |
| **FHLB Advance Growth** | YoY % | >+20% | Bank stress (SVB pattern) |
| **FBO Fed Funds Share** | FBO borrowing / Total | >50% | Foreign bank stress |

#### Regime Thresholds: Bank Funding

| **Indicator** | **Stress** | **Tight** | **Normal** | **Easy** |
|---|---|---|---|---|
| **SOFR - EFFR** | >+15 bps | +5 to +15 bps | -5 to +5 bps | <-5 bps |
| **EFFR Percentile Range** | >25 bps | 15-25 bps | 5-15 bps | <5 bps |
| **FHLB Advance Growth YoY%** | >+30% | +15 to +30% | 0 to +15% | <0% |
| **FBO Share of Borrowing** | >55% | 45-55% | 35-45% | <35% |

**The FHLB Early Warning:** FHLB advances spiked **+45% YoY** in March 2023 (SVB crisis)—banks rushed to FHLBs for liquidity. Currently at **+8% YoY**—normalized. FHLBs are the canary: when advances spike, banks are stressed. SOFR - EFFR at **+4 bps**—normal. The domestic plumbing is functioning, but watch for FHLB advance spikes as the early warning signal.

---

### H. GLOBAL DOLLAR FUNDING (The Offshore Jaws)

The dollar is the **world's funding currency**. Offshore stress shows up in FX swap basis, Fed swap lines, and FIMA facility usage. The "global jaws" define the offshore funding corridor.

| **Indicator** | **Source** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **EUR-USD Cross-Currency Basis** | Bloomberg | Daily | **Leading 1-2 wks** | Offshore dollar stress |
| **JPY-USD Cross-Currency Basis** | Bloomberg | Daily | Leading | Japan funding stress |
| **Fed Central Bank Swap Lines** | H.4.1 | Weekly | Coincident | Emergency dollar provision |
| **FIMA Repo Facility Usage** | H.4.1 | Weekly | Coincident | Foreign official borrowing |
| **Foreign Repo Pool (FRP)** | H.4.1 | Weekly | Coincident | Foreign official deposits |
| **FX Swap Implied Rate** | Derived | Daily | Coincident | Synthetic dollar cost |

#### Derived Global Funding Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **EUR-USD Basis** | Xccy basis (3M) | <-30 bps | Offshore stress |
| **Swap Line Usage** | Total outstanding | >$10B | Stress facility activated |
| **FIMA Usage** | Outstanding | >$5B | Foreign official stress |
| **Implied Funding Premium** | FX swap rate - SOFR | >+25 bps | Dollar scarcity offshore |

#### Regime Thresholds: Global Funding

| **Indicator** | **Crisis** | **Stress** | **Tight** | **Normal** |
|---|---|---|---|---|
| **EUR-USD Basis (3M)** | <-75 bps | -75 to -40 bps | -40 to -15 bps | >-15 bps |
| **Swap Line Usage ($B)** | >$100B | $20-100B | $5-20B | <$5B |
| **FIMA Usage ($B)** | >$20B | $5-20B | $1-5B | <$1B |

**The Global Jaws Framework:** The Fed has constructed a "corridor" for global dollar funding:
- **Floor:** Foreign Repo Pool rate (FRPR) / ON RRP
- **Ceiling:** FIMA repo facility / FX swap lines

EUR-USD basis at **-18 bps** (Jan 2026)—slightly stressed but not crisis. Swap line usage at **$2B**—minimal. The global jaws are functioning. But when onshore stress (SOFR, EFFR) spikes, it transmits offshore within days. March 2020: EUR-USD basis hit **-150 bps**. The global dollar system is interconnected. Onshore stress = offshore stress.

---

## Plumbing Pillar Composite Index (Liquidity Cushion Index - LCI)

### Formula

The Liquidity Cushion Index synthesizes reserves, repo, dealers, and funding stress into a single liquidity health indicator:

```
LCI = 0.25 × z(Reserves_vs_LCLOR)
    + 0.20 × z(-EFFR_IORB_Spread)                 # Inverted (positive spread = stress)
    + 0.15 × z(-SOFR_IORB_Spread)                 # Inverted
    + 0.15 × z(RRP_Balance)                       # Buffer level
    + 0.10 × z(-GCF_TPR_Spread)                   # Inverted (dealer stress)
    + 0.10 × z(-Dealer_Net_Position)              # Inverted (congestion)
    + 0.05 × z(-EUR_USD_Basis)                    # Inverted (offshore stress)
```

**Component Weighting Rationale:**
- **Reserves vs LCLOR (25%):** Primary scarcity measure
- **EFFR - IORB (20%):** Fed funds scarcity signal (inverted)
- **SOFR - IORB (15%):** Repo market stress (inverted)
- **RRP Balance (15%):** Buffer/cushion level
- **GCF - TPR (10%):** Dealer balance sheet flex (inverted)
- **Dealer Position (10%):** Intermediation congestion (inverted)
- **EUR-USD Basis (5%):** Offshore stress (inverted)

### Interpretation

| **LCI Range** | **Regime** | **Risk Asset Stance** | **Signal** |
|---|---|---|---|
| > +1.0 | Abundant Liquidity | Overweight risk | Flush system, tailwind |
| +0.5 to +1.0 | Ample | Neutral | Normal functioning |
| -0.5 to +0.5 | Tight | Slight underweight | **Vigilance required** |
| -1.0 to -0.5 | Scarce | Underweight risk | **Stress emerging** |
| < -1.0 | Crisis | Maximum defense | Systemic stress, intervention likely |

### Historical Calibration

| **Period** | **LCI** | **Regime** | **Outcome** |
|---|---|---|---|
| **Aug 2019** | +0.2 | Tight | Pre-repo spike |
| **Sep 2019** | -1.2 | Crisis | Repo spike, Fed intervention |
| **Feb 2020** | +0.4 | Ample | Pre-COVID normal |
| **Mar 2020** | -1.8 | Crisis | COVID crash, massive intervention |
| **Dec 2021** | +1.5 | Abundant | Peak liquidity (RRP $1.9T) |
| **Mar 2023** | -0.6 | Scarce | SVB crisis, BTFP launched |
| **Dec 2025** | **-0.8** | **Scarce** | **Buffer exhausted, stress building** |

**Current Assessment (Dec 2025):** LCI at **-0.8** places plumbing in "Scarce" regime—not crisis, but cushion exhausted:
- **Reserves at $3.3T** (~$300B above LCLOR estimate)
- **RRP at $150B** (buffer 94% drained)
- **EFFR - IORB at +3 bps** (edging toward scarcity)
- **SOFR - IORB at +5 bps** (repo market tightening)
- **GCF - TPR at +12 bps** (dealer sheets inflexible)
- **Dealer positions at $65B** (elevated)
- **EUR-USD basis at -18 bps** (slight offshore stress)

The system is **operating without margin for error**. Any shock—month-end, quarter-end, Treasury settlement, geopolitical event—hits directly without the RRP buffer to absorb it.

---

## Lead/Lag Relationships: The Plumbing Cascade

```
LEADING                           COINCIDENT                  LAGGING
────────────────────────────────────────────────────────────────────────────────────
│                                 │                          │
│  QT Pace (3-6 mo impact)        │  Reserve Levels           │  Bank Balance Sheets
│  Treasury Issuance (1-3 mo)     │  EFFR - IORB              │  Dealer P&L
│  TGA Rebuilds (1-4 wks)         │  SOFR Levels              │  HF Leverage (quarterly)
│  EFFR Drift (1-4 wks)           │  RRP Balance              │  MMF Allocation (monthly)
│  Dealer Fails (1-2 wks)         │  GCF - TPR                │  FHLB Advances
│  SOFR 99th Pctl (days)          │  Swap Line Usage          │  Credit Conditions
│  EUR-USD Basis (1-2 wks)        │  SRF Take-Up              │  Financial Conditions
│                                 │                          │
────────────────────────────────────────────────────────────────────────────────────
```

**The Critical Chain:**

**1. QT + Treasury issuance** → Reserves drain over months
**2. TGA rebuilds** (post-debt ceiling, tax dates) → Reserves drain in weeks
**3. EFFR - IORB drifts up** → Scarcity signal emerges
**4. SOFR spikes** (especially 99th percentile) → Repo stress
**5. Dealer fails rise** → Settlement stress
**6. GCF - TPR widens** → Dealer balance sheets freeze
**7. EUR-USD basis blows out** → Offshore stress
**8. Swap lines / SRF activated** → Crisis intervention

We're currently at Steps 1-3: QT continuing, RRP drained, EFFR drifting, SOFR elevated. The question is whether we stop here or progress to Steps 4-8.

---

## Integration with Three-Engine Framework

### Pillar 10 → Pillar 9 (Financial)

Plumbing stress transmits to **financial conditions** and **credit markets**:

```
Repo Stress → Dealer Funding Costs ↑ →
Treasury Market Illiquidity → Credit Spreads Widen →
Financial Conditions Tighten → Risk Assets Reprice
```

**Current Linkage:** LCI at -0.8 is already feeding into tighter financial conditions. Treasury bid-ask spreads widening. HY spreads at 290 bps but vulnerable to repo stress. March 2020 pattern: repo stress → Treasury illiquidity → credit freeze → equity crash.

**Cross-Pillar Signal:** When **LCI < -0.5** (scarce liquidity) AND **HY spreads widen > 50 bps in a week**, systemic stress is emerging. Fed intervention likely within days.

---

### Pillar 10 → Pillar 8 (Government)

Treasury issuance is the **primary driver** of reserve drainage:

```
Treasury Issuance ↑ → Private Sector Absorbs →
Reserves/RRP Drain → Plumbing Stress →
Auctions Struggle → Yields Rise → Issuance Costs Rise
```

**Current Linkage:** $2T+ annual issuance must be absorbed. RRP buffer gone. Every new Treasury sale drains reserves from banks. The "crowding out" is happening in real-time through the plumbing.

**Cross-Pillar Signal:** When **GCI-Gov > +1.0** (heavy issuance) AND **LCI < -0.5** (thin liquidity), Treasury auctions will struggle. Tails widen. Yields spike. This is fiscal dominance expressed through plumbing mechanics.

---

### Pillar 10 → Pillar 3 (Growth)

Plumbing stress tightens **financial conditions**, which slows **growth**:

```
Plumbing Stress → Financial Conditions Tighten →
Credit Availability ↓ → Business Investment ↓ →
Hiring ↓ → Consumer Spending ↓ → GDP ↓
```

**Current Linkage:** LCI at -0.8 is feeding into the Goldman Financial Conditions Index (tightening). Credit spreads stable but vulnerable. The plumbing is a **necessary condition** for the soft landing—if it breaks, the landing gets hard.

**Cross-Pillar Signal:** When **LCI < -1.0** (crisis liquidity) AND **GCI < -0.5** (growth contracting), recession is confirmed via financial channel.

---

### Pillar 10 → Pillar 2 (Prices)

The Fed uses plumbing to transmit **monetary policy** to the real economy:

```
Fed Funds Target → EFFR/SOFR → Bank Funding Costs →
Loan Rates → Credit Conditions → Aggregate Demand →
Inflation
```

**Current Linkage:** The Fed has hiked to 4.25-4.50%. Transmission is working: SOFR at 4.35%, mortgage rates at 6.95%, corporate yields elevated. But **plumbing stress can overwhelm policy**—in a crisis, rates spike regardless of Fed target. The plumbing determines whether policy transmits smoothly or violently.

**Cross-Pillar Signal:** When **LCI < -1.0** (crisis) AND **PCI > +0.5** (elevated inflation), the Fed faces impossible choice: ease to fix plumbing (risk inflation) or stay tight to fight inflation (risk financial crisis). March 2020 choice: ease massively.

---

## Stress Transmission Framework

### The Five Stages of Plumbing Stress

| **Stage** | **Indicators** | **Fed Response** | **Current Status** |
|---|---|---|---|
| **1. Tightening** | EFFR drifts up, RRP drains | Monitoring | ✅ We're here |
| **2. Stress Emerging** | SOFR spikes, GCF-TPR widens | Verbal guidance | ⏳ Approaching |
| **3. Acute Stress** | Fails spike, basis blows out | SRF activation | ⏳ Not yet |
| **4. Crisis** | Swap lines activated, credit freezes | Emergency facilities | ⏳ Not yet |
| **5. Intervention** | QE restart, rate cuts, new facilities | All tools deployed | ⏳ Not yet |

### Warning Signals Checklist

| **Signal** | **Threshold** | **Current** | **Status** |
|---|---|---|---|
| EFFR - IORB | >+8 bps sustained | +3 bps | 🟡 Watch |
| SOFR 99th percentile | >SRF rate | SRF - 15 bps | 🟢 OK |
| Dealer fails | >$50B weekly | $28B | 🟢 OK |
| GCF - TPR | >+20 bps | +12 bps | 🟡 Watch |
| EUR-USD basis | <-40 bps | -18 bps | 🟢 OK |
| Swap line usage | >$20B | $2B | 🟢 OK |
| SRF take-up | >$5B daily | $0 | 🟢 OK |

**Current Assessment:** Stage 1 (Tightening) confirmed. Stage 2 signals approaching but not triggered. The system is tight but not stressed. However, **margin for error is zero**. Any exogenous shock—debt ceiling, geopolitical event, large fund blow-up—could push us from Stage 1 to Stage 3 rapidly.

---

## Data Source Summary

| **Category** | **Primary Source** | **Frequency** | **Release Lag** | **FRED Availability** |
|---|---|---|---|---|
| **Fed Balance Sheet** | H.4.1 | Weekly (Thu) | Same day | Same day (WALCL, etc.) |
| **Reserve Balances** | H.4.1 | Weekly | Same day | Same day (WRBWFRBL) |
| **ON RRP** | NY Fed | Daily | Same day | Same day (RRPONTSYD) |
| **EFFR** | NY Fed | Daily | Next morning | Same day (EFFR) |
| **SOFR** | NY Fed | Daily | Next morning | Same day (SOFR) |
| **Repo Rates (GCF, DVP, TPR)** | NY Fed | Daily | Next morning | Limited FRED |
| **Dealer Positions** | NY Fed | Weekly | ~1 week lag | FR2004 |
| **HF Leverage** | OFR | Quarterly | ~45 days | OFR website |
| **FHLB Data** | FHLB Office of Finance | Quarterly | ~30 days | Limited |
| **FX Basis** | Bloomberg | Real-time | Real-time | Proprietary |
| **Swap Lines** | H.4.1 | Weekly | Same day | Same day |

**Critical Timing:** EFFR and SOFR released **next morning** provide overnight stress reads. H.4.1 (Thursday 4:30 PM ET) provides weekly balance sheet update. Watch **month-end, quarter-end, and tax dates** (April 15, June 15, Sep 15, Dec 15) for predictable stress points.

---

## Current State Assessment (January 2026)

| **Indicator** | **Current** | **Threshold** | **Assessment** |
|---|---|---|---|
| **Reserves** | $3.3T | <$3.0T = scarcity | 🟡 **$300B cushion** |
| **RRP Balance** | $150B | <$200B = buffer gone | 🔴 **Drained** |
| **EFFR - IORB** | +3 bps | >+8 bps = stress | 🟡 **Drifting up** |
| **SOFR - IORB** | +5 bps | >+10 bps = stress | 🟡 **Elevated** |
| **GCF - TPR** | +12 bps | >+20 bps = dealer stress | 🟡 **Inflexible sheets** |
| **Dealer Net UST** | $65B | >$80B = congested | 🟡 **Elevated** |
| **HF Repo Borrowing** | $950B | >$1T = fragile | 🟡 **Near threshold** |
| **EUR-USD Basis** | -18 bps | <-40 bps = offshore stress | 🟢 OK |
| **Swap Line Usage** | $2B | >$20B = stress | 🟢 OK |
| **SRF Take-Up** | $0 | >$5B = ceiling hit | 🟢 OK |
| **LCI Estimate** | **-0.8** | <-0.5 = scarce | 🔴 **Scarce Regime** |

### Narrative Synthesis

The plumbing is **operating without a safety margin**. Not crisis—but no buffer.

**The Drain:**
- RRP at **$150B** (down from $2.55T peak)—**94% drained**
- Reserves at **$3.3T** (~$300B above LCLOR)—5 months of QT runway
- QT continuing at **$60B/month**
- Treasury issuance at **$2T+/year**

**The Stress Signals:**
- EFFR - IORB at **+3 bps** (drifting toward scarcity)
- SOFR - IORB at **+5 bps** (repo market tightening)
- GCF - TPR at **+12 bps** (dealer sheets inflexible)
- Dealer positions at **$65B** (congestion building)
- HF leverage at **$950B** (fragility elevated)

**The Buffer Gone:**
- When RRP was $2T, shocks were absorbed: MMFs shifted allocation, reserves stayed stable
- Now: every Treasury issuance, every TGA rebuild, every reserve drain hits bank balance sheets directly
- The **margin for error is zero**

**The Transmission Chain at Risk:**
- Reserves drain → EFFR spikes → SOFR spikes → Dealer funding costs rise → Treasury liquidity evaporates → Credit freezes → Risk assets crash
- This is September 2019, March 2020, the next event waiting to happen
- Difference: Fed is watching now, SRF is operational, they'll act faster

**Cross-Pillar Confirmation:**
- **Government Pillar:** $2T issuance overwhelming absorption capacity
- **Financial Pillar:** Credit spreads tight but vulnerable to plumbing shock
- **Growth Pillar:** Financial conditions tightening through plumbing channel

**MRI (Macro Risk Index):** Plumbing contributes **-0.8 (LCI)** to composite—the **second-largest risk factor** after fiscal. The system has lost its shock absorber.

---

## Invalidation Criteria

### Bull Case (Liquidity Easing) Invalidation Thresholds

If the following occur **for 3+ months**, the bearish plumbing thesis is invalidated:

✅ **Fed pauses QT** or restarts QE
✅ **Reserves stabilize above $3.5T**
✅ **EFFR - IORB falls below 0 bps** (sustained)
✅ **RRP rebuilds above $500B** (new cash inflows)
✅ **Dealer positions normalize below $40B**
✅ **LCI rises above +0.5** (ample regime)

**Action if Invalidated:** Plumbing is **no longer a constraint**. Risk assets have tailwind. Add cyclical exposure.

---

### Bear Case (Liquidity Crisis) Confirmation Thresholds

If the following occur, plumbing is **deteriorating into crisis**:

🔴 **EFFR - IORB exceeds +15 bps** (sustained)
🔴 **SOFR spikes above SRF rate** (ceiling breached)
🔴 **Dealer fails exceed $75B weekly**
🔴 **EUR-USD basis breaks -60 bps**
🔴 **SRF take-up exceeds $20B** (emergency usage)
🔴 **Swap lines activated >$50B**
🔴 **LCI drops below -1.5** (crisis regime)

**Action if Confirmed:** Maximum defensive. Expect Fed intervention within days. Front-run the intervention: long duration (Fed will cut/buy), long gold (safe haven), short credit (spreads will blow before Fed fixes). After intervention, aggressive risk-on.

---

## The QT Endgame Framework

### When Does QT End?

QT ends when reserves approach the **Lowest Comfortable Level of Reserves (LCLOR)**. The Fed's job is to stop before stress emerges—September 2019 showed what happens when they overshoot.

**Current Math:**
- Reserves: **$3.3T**
- LCLOR Estimate: **~$3.0T** (Fed's working assumption)
- Gap: **$300B**
- QT Pace: **$60B/month**
- Runway: **~5 months** (May/June 2026)

**The Scenarios:**

| **Scenario** | **Trigger** | **Probability** | **Outcome** |
|---|---|---|---|
| **Orderly Taper** | Reserves hit $3.1T, no stress | 40% | QT slows, then ends Q2 2026 |
| **Stress-Induced Pause** | EFFR spikes, repo stress | 35% | QT pauses abruptly, SRF deployed |
| **Crisis Stop** | Systemic event, credit freeze | 15% | QT ends, QE restarts |
| **Extended QT** | Reserves fall smoothly, no stress | 10% | QT continues past $3.0T |

**Our Base Case:** QT slows in Q2 2026, ends by Q3 2026. Some stress likely before the end—Fed will cut it close.

---

## Conclusion: The System Without a Cushion

Plumbing isn't visible until it breaks. Then it's the only thing that matters.

**Current State:**
- **LCI -0.8** (Scarce Regime)
- **Reserves $3.3T** (~$300B above LCLOR, 5 months runway)
- **RRP $150B** (buffer 94% drained)
- **EFFR - IORB +3 bps** (scarcity emerging)
- **Dealer sheets inflexible** (GCF - TPR +12 bps)
- **HF leverage elevated** ($950B basis trade)

**The Transmission Chain:**
```
Fed Balance Sheet → Reserves → Bank Balance Sheets →
Dealer Intermediation → Repo Markets → Treasury Liquidity →
Financial Conditions → Asset Prices
```

Every link in this chain is **tighter than it was 12 months ago**. The RRP buffer that absorbed shocks for three years is gone. From here, shocks transmit directly.

**The Fed's Toolkit:**
- **SRF:** Ceiling on repo (operational, unused)
- **Discount Window:** Last resort (stigma limits usage)
- **QT Pause:** Can stop drainage (likely Q2-Q3 2026)
- **QE Restart:** Nuclear option (only in crisis)
- **Swap Lines:** Offshore dollar provision (operational, minimal usage)

**The Honest Assessment:**
The Fed is watching more carefully than 2019. The SRF exists. They'll likely act before crisis. But "likely" isn't "certainly." And "before crisis" still means "after stress."

The soft landing requires the plumbing to hold. LCI at -0.8 says it's holding—barely. The margin for error is zero.

**That's our view from the Watch. Until next time, we'll be sure to keep the light on....**

*Bob Sheehan, CFA, CMT*
*Founder & CIO, Lighthouse Macro*
*January 15, 2026*
