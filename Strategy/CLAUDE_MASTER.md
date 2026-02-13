# LIGHTHOUSE MACRO - MASTER CONTEXT

**LAST_SYNC:** 2026-02-13
**Version:** 4.0

---

## CRITICAL: DATE CHECK PROTOCOL

**EVERY SESSION, BEFORE DOING ANYTHING ELSE:**

1. Note today's date
2. Compare to LAST_SYNC above
3. If LAST_SYNC is NOT today or yesterday:
   - STOP IMMEDIATELY
   - Say: "Context is stale (last sync: [DATE]). Run `lhm-sync` before we proceed."
   - Do NOT answer questions or do work until user confirms sync

**Why this matters:** Prevents Claude from operating on outdated context. Keeps all interfaces aligned.

---

## Complete AI Reference for Bob Sheehan & Lighthouse Macro

**Purpose:** Comprehensive context file for AI assistants working with Bob Sheehan

*"MACRO, ILLUMINATED."*

---

# CHANGELOG

| Date | Update |
|------|--------|
| **2026-02-06** | v4.0: Comprehensive rebuild. Added full chart-styling spec, Two Books framework, Technical Overlay scoring, writing style guide, data infrastructure details, complete project structure, sync workflow. Consolidated from 10+ source files. |
| **2026-02-03** | Removed "Absolute Rules" framing; replaced with flexible "Technical Guardrails". Added Asset Class Coverage section. Added website files. |
| **2026-02-03** | Created Asset Class Frameworks: Equities, Rates, Credit, Commodities, Currencies, Crypto |
| **2026-01-24** | Tania Reif/Senda: BCH analysis delivered Dec 22. Trial phase ongoing (~3 months). |
| **2026-01-24** | Christopher King engaged. Connected Bob with BrimxBrand for brand buildout. |
| **2026-01-24** | BrimxBrand (Mike Stephenson, Kristina) handling website and brand. |
| **2025-10** | Pascal Hugli podcast appearance (repo markets, Fed plumbing, crypto/Treasury). |

---

# SECTION 1: CORE IDENTITY

## Who Bob Is

**Bob Sheehan, CFA, CMT**
Founder & Chief Investment Officer, Lighthouse Macro

### Background

- **Former VP, Data & Analytics at EquiLend**
- **Former Associate PM at Bank of America Private Bank** ($4.5B multi-asset AUM; SGS equity sleeve ~$1.2B at peak, 2.35 Sortino, 103% upside capture, 76% downside capture vs S&P 500)
- **Former Senior Research Analyst at Strom Capital Management**
- **Credentials:** CFA, CMT, BrainStation Data Science Diploma
- **Former Division 1 athlete** (thrived with external structure)

### Personal Context

- **ADHD as a superpower:** Gets bored with repetitive focus, thrives on intellectual diversity across multiple macro domains
- **Code-first approach:** Python-driven frameworks, never approximates or fabricates data
- **Systematic mindset:** Values reproducibility, quantitative rigor, and bridging complex concepts into accessible insights
- **"Lighthouse"** was the name of Bob's house in college where he first studied finance/economics. Evolved into the firm identity over the years.

### Key Relationships & Active Engagements

- **Pascal Hugli** - Swiss investment manager (Maerki Baumann), host of "Less Noise More Signal" podcast/Substack. Bob appeared Oct 2025 discussing repo markets, Fed plumbing, crypto/Treasury dynamics. Pascal wants Bob back on. LHM is a recommended publication on Pascal's Substack. Mike (BrimxBrand) managing how Pascal brands Bob going forward.
- **Tania Reif** - PhD Columbia, former Soros Fund Management, Citadel, Laurion, Alphadyne, IMF. Founder & CIO of Senda Digital Assets (quantamental crypto fund, BVI). Heard Bob on Pascal's podcast. Bob has been doing work for Senda over a ~3-month trial phase.
- **Christopher King** - Theo Advisors and 5+ other ventures. Wants Bob as the data/macro layer and point person for economic questions across his businesses. Connected Bob with BrimxBrand.
- **Mike Stephenson (BrimxBrand)** - CEO of Brim & Brand LLC (Carmel, NY) and introduced via Christopher. Marketing/branding firm handling Lighthouse Macro brand buildout. Kristina on his team is point person for website build. Mike correctly identified Bob as neurodivergent/athlete on first call.

### Contact Information

| Type | Value |
|------|-------|
| Name | Bob Sheehan, CFA, CMT |
| Title | Founder & Chief Investment Officer |
| Website | LighthouseMacro.com |
| Email (Primary) | bob@lighthousemacro.com |
| Email (Advisory) | advisory@lighthousemacro.com |
| Email (Research) | research@lighthousemacro.com |
| Phone | +1 (240) 672-7418 |
| Twitter/X | @LHMacro |

### Document Footer Template

```
Bob Sheehan, CFA, CMT | Founder & Chief Investment Officer
Lighthouse Macro | LighthouseMacro.com | @LHMacro
```

---

## Lighthouse Macro Positioning

**Tagline:** "MACRO, ILLUMINATED."

**Mission:** Institutional-grade macro research serving hedge funds, CIOs, central banks, and allocators

**Core Differentiation:**

| **Attribute** | **Lighthouse Approach** | **Consensus Approach** |
|---|---|---|
| **Signal Source** | 12 Macro Pillars, Proprietary Indicators | Headlines, lagging data |
| **Analytical Framework** | Three-Engine System | Single-dimensional analysis |
| **Position Sizing** | Conviction-weighted (7-20% per position) | Equal-weighted |
| **Concentration** | 3-10 high-conviction positions | 30+ marginal positions |
| **Cash Treatment** | Active position (30-100% valid) | Residual drag |
| **Risk Framework** | Dual stops (thesis + price) | Single trailing stop |
| **Timeframe** | 3-6 month tactical core | Arbitrary calendar |

**Philosophy:** "Flows > Stocks. We track labor market flows, Fed plumbing dynamics, and credit conditions systematically. We monitor structure and sentiment to time entries and exits. Concentrated positions. Conviction-weighted sizing."

---

# SECTION 2: THE DIAGNOSTIC DOZEN (12 Pillars)

## Three-Engine Framework

```
+---------------------------------------------------------------------------------+
|                              12 MACRO PILLARS                                    |
|                          (The Diagnostic Dozen)                                  |
+------------------------+-------------------------+-------------------------------+
|   MACRO DYNAMICS       |   MONETARY MECHANICS    |      MARKET STRUCTURE         |
|   (Pillars 1-7)        |   (Pillars 8-10)        |      (Pillars 11-12)          |
+------------------------+-------------------------+-------------------------------+
| 1. Labor    -> LPI,LFI | 8. Government -> GCI-Gov| 11. Structure -> MSI, SBD     |
| 2. Prices   -> PCI     | 9. Financial  -> FCI,CLG| 12. Sentiment -> SPI, SSD     |
| 3. Growth   -> GCI     | 10. Plumbing  -> LCI    |                               |
| 4. Housing  -> HCI     |                         |                               |
| 5. Consumer -> CCI     |                         |                               |
| 6. Business -> BCI     |                         |                               |
| 7. Trade    -> TCI     |                         |                               |
+------------------------+-------------------------+-------------------------------+
                                       |
                               MRI (Master Composite)
                                       |
                           TRADING STRATEGY EXECUTION
```

## Pillar Summary

| **Pillar** | **Index** | **Key Insight** | **Lead Time** |
|---|---|---|---|
| **1. Labor** | LPI, LFI | Quits rate = truth serum | Leading |
| **2. Prices** | PCI | Last mile sticky, shelter lags | 12-18 months (shelter) |
| **3. Growth** | GCI | Second derivative matters | 2-4 months |
| **4. Housing** | HCI | Frozen equilibrium, rate sensitive | 6-9 months |
| **5. Consumer** | CCI | 68% of GDP, lagging indicator | 1-3 months |
| **6. Business** | BCI | Capex = forward commitment | 4-8 months |
| **7. Trade** | TCI | Dollar/tariff pass-through | 3-6 months |
| **8. Government** | GCI-Gov | Fiscal dominance, term premium | Structural |
| **9. Financial** | FCI, CLG | Credit spreads lead defaults | 6-9 months |
| **10. Plumbing** | LCI | RRP exhaustion = no buffer | 1-4 weeks |
| **11. Structure** | MSI, SBD | Breadth divergence = distribution | 2-4 months |
| **12. Sentiment** | SPI, SSD | Contrarian at extremes only | Days to weeks |

**Full Pillar Details:** `/Users/bob/LHM/Strategy/PILLAR [1-12] *.md`

---

## Macro Risk Index (MRI) v2.0

**The Master Composite:** Synthesizes all 12 pillars into a single regime indicator.

```
MRI = 0.13 * (-LPI)    + 0.08 * PCI       + 0.13 * (-GCI)    + 0.06 * (-HCI)
    + 0.08 * (-CCI)    + 0.08 * (-BCI)    + 0.05 * (-TCI)    + 0.08 * GCI-Gov
    + 0.04 * (-FCI)    + 0.08 * (-LCI)    + 0.12 * (-MSI)    + 0.07 * (-SPI)
```

| **MRI Range** | **Regime** | **Equity Allocation** | **Regime Multiplier** |
|---|---|---|---|
| < -0.5 | Low Risk | 65-70% | 1.2x |
| -0.5 to +0.5 | Neutral | 55-60% | 1.0x |
| +0.5 to +1.0 | Elevated | 45-55% | 0.6x |
| +1.0 to +1.5 | High Risk | 35-45% | 0.3x |
| > +1.5 | Crisis | 25-35% | 0.0x |

---

## Key Composite Formulas

**Labor Fragility Index (LFI):**
```
LFI = 0.35*z(LongTermUnemp%) + 0.35*z(-Quits) + 0.30*z(-Hires/Quits)
```

**Liquidity Cushion Index (LCI):**
```
LCI = 0.25*z(Reserves_vs_LCLOR) + 0.20*z(-EFFR_IORB) + 0.15*z(-SOFR_IORB)
    + 0.15*z(RRP) + 0.10*z(-GCF_TPR) + 0.10*z(-DealerPos) + 0.05*z(-EUR_USD_Basis)
```

**Credit-Labor Gap (CLG):**
```
CLG = z(HY_OAS) - z(LFI)
```
- CLG < -1.0: Credit too tight for labor reality

**Market Structure Index (MSI):**
```
MSI = 0.15*z(Price_vs_200d) + 0.10*z(Price_vs_50d) + 0.10*z(50d_Slope)
    + 0.10*z(20d_Slope) + 0.12*z(Z_RoC_63d) + 0.10*z(%>50d_MA)
    + 0.08*z(%>20d_MA) + 0.08*z(%>200d_MA) + 0.07*z(NH_NL_20d)
    + 0.05*z(AD_Slope) + 0.05*z(McClellan_Sum)
```

**Sentiment & Positioning Index (SPI):**
```
SPI = 0.20*z(Put_Call_10d) + 0.15*z(VIX_vs_50d) + 0.15*z(-AAII_Bull_Bear)
    + 0.15*z(-NAAIM) + 0.10*z(-II_Bull_Bear) + 0.10*z(-ETF_Flows_20d)
    + 0.10*z(VIX_Backwardation) + 0.05*z(MMF_Assets_YoY)
```
- High SPI = Fear = Contrarian Bullish

**Structure-Breadth Divergence (SBD):**
```
SBD = z(Price_vs_200d) - z(%_Stocks_>_50d_MA)
```
- SBD > +1.0: Distribution warning (generals without soldiers)

**Sentiment-Structure Divergence (SSD):**
```
SSD = z(SPI) + z(MSI)
```
- SSD > +1.5: Capitulation low forming
- SSD < -1.5: Blow-off top risk

---

## Key Thresholds Quick Reference

### Labor

| Indicator | Threshold | Signal |
|---|---|---|
| Quits Rate | <2.0% | Pre-recessionary |
| LFI | >+0.5 | Fragility elevated |
| Temp Help YoY | <-3% | Recession signal |
| Long-Term Unemployed | >22% | Structural fragility |
| Hires/Quits Ratio | <2.0 | Demand weakening |

### Liquidity

| Indicator | Threshold | Signal |
|---|---|---|
| RRP | <$200B | Buffer exhausted |
| EFFR-IORB | >+8 bps | Acute funding stress |
| LCI | <-0.5 | Scarce regime |
| Reserves vs LCLOR | <$300B | Scarcity threshold |
| SOFR-IORB | >+10 bps | Funding stress |

### Credit

| Indicator | Threshold | Signal |
|---|---|---|
| HY OAS | <300 bps | Complacent |
| CLG | <-1.0 | Credit ignoring fundamentals |

### Market Structure

| Indicator | Threshold | Signal |
|---|---|---|
| Price vs 200d | <0% | Below trend |
| 20d vs 50d | Negative cross | Short-term rollover warning |
| 20d Slope | Negative while 50d rising | Early momentum warning |
| % > 20d MA | <25% | Short-term washed (bounce) |
| % > 20d MA | >80% | Short-term crowded |
| % > 20d MA | 30% to 70% in 10d | Breadth thrust (powerful) |
| % > 50d MA | <35% | Breadth washed (buy) |
| % > 50d MA | >85% | Breadth crowded (caution) |
| Z-RoC | <-1.0 | Momentum broken |
| MSI | <-1.0 | Structure broken |

### Sentiment

| Indicator | Threshold | Signal |
|---|---|---|
| AAII Bull-Bear | >+30% | Euphoria (sell) |
| AAII Bull-Bear | <-20% | Capitulation (buy) |
| NAAIM | >100% | Fully invested (sell) |
| SPI | >+1.5 | Extreme fear (strong buy) |
| SPI | <-1.0 | Euphoria (sell) |

---

## Engine Convergence Matrix

| **Engine 1 (Macro)** | **Engine 2 (Monetary)** | **Engine 3 (Structure/Sentiment)** | **Action** |
|---|---|---|---|
| Bullish | Supportive | Confirming + Fear | **Maximum conviction long** |
| Bullish | Supportive | Confirming + Neutral | Normal position |
| Bullish | Supportive | Diverging | Reduce exposure |
| Bullish | Restrictive | Any | No new longs |
| Bearish | Any | Confirming | Maximum defensive |
| Bearish | Supportive | Diverging + Extreme Fear | Tactical exhaustion only |

---

## 4 Signature Synthesis Chains

1. **Labor to Credit to Equity:** Labor flows (Quits) deteriorate first (Leading), credit spreads widen (Coincident), equity multiples compress (Lagging). Watch "Silent Deceleration" to predict credit blowout.

2. **Collateral Fragility (Crypto-Treasury Loop):** Crypto is the marginal buyer of U.S. Treasuries via stablecoins. Crypto volatility forces Treasury liquidation.

3. **Plumbing to Asset Prices:** RRP drain, reserve scarcity, dealer constraints (SLR), repo spreads widen, Treasury auction tails, risk asset repricing.

4. **Fiscal Dominance (2026 Theme):** The "Honest Signal" is the term premium. Must reprice to ~150bps to clear structural deficits in post-QT world.

---

## Pillar-to-Trade Mapping

| **Pillar Signal** | **Trading Expression** | **Asset Class** |
|---|---|---|
| LFI > +0.8 | Reduce cyclical equity exposure | Equities |
| LCI < -0.5 | Reduce gross exposure, add cash | All |
| CLG < -1.0 | Add credit protection (HY short) | Credit |
| PCI > +1.0 | Short duration, inflation hedges | Rates |
| GCI-Gov > +1.0 | Steepener trades, term premium | Rates |
| BCI < -0.5 | Underweight small caps vs large | Equities |
| HCI < -0.5 | Avoid homebuilders, housing-sensitive | Equities |
| MSI < -0.5 | Reduce gross exposure | All |
| SPI > +1.5 | Contrarian fade (crowding risk) | All |

---

## Technical Guardrails

These are signals we monitor, not rules we obey blindly. In normal ranges, they're inputs to weigh alongside fundamentals. At extremes, they demand attention. The discipline is knowing the difference.

| **Signal** | **What It Measures** | **Context** |
|---|---|---|
| Price vs 200d MA | Primary trend position | Below = higher bar for longs, but mature downtrends (>60d) offer tactical opportunity |
| 50d vs 200d MA | Trend structure | Death cross = weakening, but duration matters (fresh vs stale) |
| Relative Strength | Performance vs benchmark | Persistent underperformance is a flag, but context (rotation vs risk-off) matters |
| Z-RoC (63d) | Momentum | Extremes (<-1.5 or >+1.5) are significant; normal ranges are one input among many |
| Distance from 50d | Extension | >15% stretched = poor entry risk/reward; wait for consolidation |

**Philosophy:** When a signal is screaming, listen. When it's whispering, weigh it.

---

# SECTION 3: THE TWO BOOKS FRAMEWORK

## Portfolio Structure

True global macro is directional, not directionally constrained. The books are entry frameworks, not holding period constraints.

### Core Book (50-100% of capital)

- Macro + Fundamental + Technical driven
- LONG OR SHORT based on thesis
- MRI regime multiplier applies to sizing
- Thesis-driven entry with 3-6 month catalyst horizon
- Full position sizing (up to 20% per position)
- Can go to 100% cash when no setups qualify

### Technical Overlay Book (0-50% of capital)

- Pure technical (trend + momentum + relative strength)
- LONG OR SHORT based on price structure
- Activated when Core Book is defensive (MRI > +1.0)
- No macro thesis required, following price
- Sizing at 50% of Core (max 10% longs, 5% shorts per position)
- Tighter stops (10% longs, 8% shorts)

### Position Sizing

```
Position Size = Base Weight * Conviction Multiplier * Regime Multiplier
```

| Conviction Tier | Score | Base Weight |
|---|---|---|
| Tier 1 | 16-19 pts | 20% |
| Tier 2 | 12-15 pts | 12% |
| Tier 3 | 8-11 pts | 7% |
| Tier 4 | <8 pts | 0% (avoid) |

| MRI Regime | Multiplier |
|---|---|
| Supportive (< +0.5) | 1.0x |
| Neutral (+0.5 to +1.0) | 0.6x |
| Restrictive (> +1.0) | 0.3x |

### Dual Stop System (Core Book)

Every position has TWO stops. Use whichever triggers first.

**Thesis Stop (Fundamental):**
- Revenue declines 3 consecutive quarters
- Key indicator crosses invalidation threshold
- Macro regime shift against thesis

**Price Stop (Technical):**
- Price closes below 200d MA (longs) / above 200d MA (shorts)
- Z-RoC drops below -1.0 (longs) / rises above +1.0 (shorts)
- 15% drawdown from entry (hard stop)

### Technical Overlay Scoring (12-Point System)

Three components, 4 points each. Minimum score to enter: 8/12.

| Component | Points | What It Measures |
|---|---|---|
| **Trend Structure** | 0-4 | Price vs 50d vs 200d alignment + slope |
| **Momentum (Z-RoC)** | 0-4 | Direction, magnitude, and trajectory |
| **Relative Strength** | 0-4 | vs BTC/SPX (multiple timeframes + slope) |

### Short-Specific Requirements (All must be true)

- Price < 50d < 200d (both MAs falling)
- Z-RoC declining with bearish divergence (trajectory > level)
- Relative strength RED on both 63d and 252d
- Clear breakdown pattern (not just weakness)
- NOT extended (price not >10% below 50d MA)
- Score >= 8/12

### Position Graduation

Technical Book positions can graduate to Core Book treatment when fundamental drivers emerge. Core Book positions can shift to Technical Book limits when macro uncertainty rises but technical structure holds.

### Capital Allocation Priority

1. Core Book positions with both thesis AND technical confirmation
2. Core Book positions with thesis (technical neutral)
3. Technical Overlay positions with strong scores
4. Cash

---

# SECTION 4: ASSET CLASS COVERAGE

The 12 Pillars are the diagnostic framework. Asset classes are implementation.

| **Asset Class** | **Instruments** | **Key Pillar Links** |
|---|---|---|
| **Equities** | ETFs (SPY, QQQ, sectors), single stocks | MSI, SPI, GCI, LPI |
| **Rates** | Duration ETFs (TLT, IEF, SHY), TIPS | PCI, LCI, GCI-Gov |
| **Credit** | IG, HY, loans (LQD, HYG, BKLN) | FCI, CLG, LCI |
| **Commodities** | Gold, energy, metals (GLD, XLE, CPER) | PCI, GCI, TCI |
| **Currencies** | Dollar, majors, EM (UUP, FXE, CEW) | TCI, GCI, MRI |
| **Crypto** | BTC, ETH, alts | LCI (Net Liquidity), MRI |

**Detailed Frameworks:** `/Users/bob/LHM/Strategy/Asset_Class_Frameworks/` (EQUITIES.md, RATES.md, CREDIT.md, COMMODITIES.md, CURRENCIES.md, CRYPTO.md)

---

# SECTION 5: COMMUNICATION GUIDELINES

## Voice & Tone: The 80/20 Rule

- **80% Institutional Rigor:** CFA/CMT credibility, quantitative precision, clear analysis
- **20% Personality:** Dry observations, skepticism of consensus, occasional wit when natural
- **0% Forced Flair:** No manufactured catchphrases, no trying to coin new expressions

**The Key Principle:** Personality should emerge from the analysis, not be layered on top. A sharp observation lands harder than a forced quip. Let the data do the heavy lifting.

**The "We" Frame:** Speak as Lighthouse Macro. "We're seeing stress" not "The data shows stress."

**The Vibe:** Deadpan & dry. Skeptical of consensus. Data-driven. Subtle humor. "I'm not mad, just disappointed in the data." The adult in the room watching the market throw furniture.

### What Good Looks Like

- "The labor data softened. Again." (Dry, lets the repetition speak)
- "Spreads are pricing one story. Labor is telling another." (Clean contrast)
- "The buffer is gone. The runway is short." (Direct, no embellishment)
- "The Fed's in a box. They just haven't admitted it yet." (Observation, not hot take)

### What to Avoid

- Forced metaphors reaching for catchphrases
- Trying to make every observation "quotable"
- Excessive nautical references beyond natural brand vocabulary
- Any phrase auditioning for a newsletter subtitle
- Emdashes (use commas, periods, colons, parentheses, ellipses instead)
- Semicolons (use commas)
- Any patterns commonly associated with AI-generated content
- Over-excited adjectives ("Skyrocketing," "Plummeting")
- Robotic transitions ("In conclusion," "It is important to note")

### Banned Phrases

- "Cautiously optimistic"
- "Geopolitical uncertainty"
- "Complex constellation of factors"
- "In our view" (just state it)
- "Going forward" (filler)
- "At the end of the day" (cliche)
- "It is important to note"
- "In conclusion"
- Any AI-sounding robotic transitions

### Standard Sign-Off (Use Sparingly, Beacon/Horizon Only)

> That's our view from the Watch. Until next time, we'll be sure to keep the light on....

**Subscribe CTA:** "Join The Watch."

### Bob's Writing Cadence (from Tweets/Substack)

- Skeptical of consensus
- Allergic to vague platitudes
- Lets data talk, then adds a dry observation
- Short sentences control rhythm
- Uses casual precision with occasional slang
- Emoji usage: sparring, purposeful (flame for hot takes, eyes for "look at this")
- Threading for complex macro arguments
- Athletic/ADHD personality: thrives on intellectual diversity

---

# SECTION 6: BRAND SYSTEM

## Nautical 8-Color Palette

| Name | Hex | Usage |
|---|---|---|
| **Ocean** | `#0089D1` | Primary brand color, headers, borders, data (white theme) |
| **Dusk** | `#FF6723` | Secondary series, accent bar segment |
| **Sky** | `#4FC3F7` | Primary data (dark theme) |
| **Venus** | `#FF2389` | 2% target lines, critical alerts |
| **Sea** | `#00BB99` | Tertiary series, on-target regime bands |
| **Doldrums** | `#D3D6D9` | Zero lines, reference |
| **Starboard** | `#00FF00` | Extreme bullish |
| **Port** | `#FF0000` | Crisis regime bands |

### Document Brand Colors

| Color | Hex | Usage |
|---|---|---|
| Ocean Blue | `#0089D1` | Primary brand, headers, borders, accents |
| Dusk Orange | `#FF4500` | Secondary accent, highlights, CTAs |
| Carolina Blue | `#00BFFF` | Tertiary accent, gradients |
| White | `#FFFFFF` | Backgrounds, text on dark |
| Dark Gray | `#333333` | Body text |
| Light Gray | `#F5F5F5` | Background alternates |

### Accent Bar

- Ocean Blue `#0089D1` for approximately 2/3 width (left side)
- Dusk Orange `#FF4500` for approximately 1/3 width (right side)
- Height: 4-6px for documents, scalable for presentations

## Typography

| Element | Font | Weight | Size Guidelines |
|---|---|---|---|
| Document Title | Montserrat | Bold | 28-36pt |
| Section Headers | Montserrat | Bold | 18-24pt |
| Subheaders | Montserrat | SemiBold | 14-16pt |
| Body Text | Inter | Regular | 11-12pt |
| Captions | Inter | Regular | 9-10pt |
| Data/Tables | Inter or Source Code Pro | Regular | 10-11pt |

Google Fonts:
- Montserrat: https://fonts.google.com/specimen/Montserrat
- Inter: https://fonts.google.com/specimen/Inter
- Source Code Pro: https://fonts.google.com/specimen/Source+Code+Pro

## Logo & Watermarks

| Element | Details |
|---|---|
| Logo | `assets/logo.jpg`, White lighthouse on ocean blue background |
| Banner | `assets/banner.jpg`, Horizontal lockup with lighthouse icon, text, tagline, accent bar |
| Logo Placement | Top-left, minimum 40px margin from edges |
| Clear Space | Minimum 1/4 of logo width on all sides |

### Watermarks

| Position | Content |
|---|---|
| Top-left | LIGHTHOUSE MACRO |
| Bottom-right | MACRO, ILLUMINATED. |

- Font: Montserrat Bold
- Color: Ocean Blue `#0089D1` at 15-20% opacity
- Size: Subtle but legible (typically 8-10pt)

---

# SECTION 7: CHART STYLING SPECIFICATION

**Full spec:** `/Users/bob/LHM/Brand/chart-styling.md` (Version 3.0, TT Deck Standard)

## Core Rules

- **No gridlines.** All four spines visible at 0.5pt
- Right axis is primary
- No tick marks
- Spine colors: Dark theme `#1e3350`, White theme `#cccccc`
- Every chart must have: `border: 2px solid #0089D1`
- DPI 200, bbox_inches='tight', pad_inches=0.10
- 4.0pt Ocean Blue outer border at figure edge

## Dual-Axis Charts

- RHS = Primary (Ocean Blue / Sky)
- LHS = Secondary (Dusk Orange)
- Both axes get last-value pills (colored rounded boxes with bold white text)

## Single-Axis Charts

- Ticks on RHS, RHS pill only
- Full width available for data

## X-Axis Padding

- 30-day left padding for breathing room
- 180-day right padding for last-value pills

## Data Handling

- Always `dropna()`
- Forward-fill quarterly data to daily
- Smooth volatile series with 3-month MA
- Don't smooth already-smoothed measures (like 3-month moving averages of rates)

## Reference Lines

| Type | Color | Style |
|---|---|---|
| Zero line | Doldrums `#D3D6D9` | Dashed |
| 2% Target | Venus `#FF2389` | Solid |
| 3% Danger | Sea `#00BB99` | Solid |

## Regime Bands (for composite z-score indicators)

Colored `axhspan` bands: Crisis (Port), High Risk (Port alpha), Elevated (Dusk), On-target (Sea), Deflationary (Ocean)

## Recession Shading

- Dark theme: white, alpha 0.06
- White theme: gray, alpha 0.12

## Annotation Box

Dynamic commentary in dead space with Ocean Blue border. Used for contextual notes on charts.

## Chart Layout Rules

- **1 column:** Full content width
- **2 columns:** 48% each, 4% gutter
- **4 panels:** 48% x 48% grid
- **Caption:** Centered below, Inter 9-10pt, "Figure N: Description"
- **Spacing:** 8px chart-to-caption, 16px caption-to-next-element

## Helper Functions (chart-styling.md API)

```python
new_fig()           # Create branded figure
style_ax()          # Style axis with theme
style_dual_ax()     # Style dual-axis chart
style_single_ax()   # Style single-axis chart
set_xlim_to_data()  # Fit x-axis to data range with padding
brand_fig()         # Add watermarks, date, accent bar, source
add_last_value_label()  # Add pill labels on axes
add_annotation_box()    # Add commentary box
add_recessions()        # Add NBER recession shading
legend_style()          # Themed legend
```

## Dual Theme Generation

Generate both dark and white versions of every chart.

## Reference Implementations

- `prices_edu_charts.py`
- `tt_research_charts.py`
- `generate_two_books_pdf.py`

---

# SECTION 8: CONTENT CADENCE & DOCUMENT TYPES

## Publication Schedule

| **Type** | **Frequency** | **Length** |
|---|---|---|
| **Beacon** | Weekly (Sundays) | 3-4k words |
| **Beam** | 1-3x weekly | Single chart + 150-300 words |
| **Chartbook** | Bi-weekly | 50-75 charts |
| **Horizon** | Monthly (First Monday) | Forward outlook |

## Document Type Structures

### Beacon (Long-Form Analysis)

Deep-dive synthesizing macro dynamics, monetary mechanics, and market technicals. Portrait, single-column.

Structure: Executive Summary, Macro Context, Monetary Dynamics, Market Technicals, Conclusion

### Beam (Single-Chart Insight)

Quick-hit insight centered on one compelling chart. 150-300 words max. Portrait or square.

Structure: Logo, Title, Chart (full-width bordered), Commentary

### Chartbook (Visual Compilation)

50-75 institutional-quality charts. Landscape for multi-chart pages.

Structure: Cover, TOC, Section Dividers, Charts (2-4 per page), Closing

### Horizon (Forward Outlook)

Strategic forward-looking piece. Key themes, risk matrix, watchlist, tactical implications.

Structure: State of Play, Key Themes, Risk Matrix, Watchlist, Tactical Implications

### Educational Series (Pillar Posts)

One post per pillar. 3,000-3,500 words, 8-10 charts.

Structure: Hook, Core Insight, What to Watch, Indicators (7-9 subsections with charts), Consensus Trap, Where We Are Now, How to Track, Invalidation Criteria, Bottom Line

### Framework Documents

Methodology explanations. Components, formulas, interpretation guides.

### Presentations (PPTX)

Title slide with banner. Section dividers with Ocean Blue background. Content slides with logo top-left. Chart slides bordered and captioned.

### One-Pagers

Single-page summaries. Clean, scannable, high information density.

**Full templates:** `/Users/bob/LHM/Brand/templates.md`

---

# SECTION 9: DATA INFRASTRUCTURE

## lighthouse_mega Package

**Location:** `/Users/bob/lighthouse_mega/`

Python-first pipelines: ARIMA, VAR, NLP. The production data package.

```
lighthouse_mega/
  __init__.py
  pipeline.py         # Core data pipeline
  run_pipeline.py     # Pipeline execution
  validate_series.py  # Data validation
  utils/              # Shared utilities
  charts/             # Chart generation
  data/               # Data storage
  requirements.txt
```

## Data Pipeline

```
RAW DATA -> STAGING -> CURATED -> FEATURES -> INDICATORS -> OUTPUTS
```

## Schedule

- 06:00 ET: Data refresh (`daily_flows.py`)
- 07:00 ET: Indicator computation
- 07:15 ET: Alert generation

## Data Sources

Primary: FRED, TreasuryDirect, OFR, TIC, NY Fed, BLS, Census, ISM, SIFMA
Market: Bloomberg (via API), Yahoo Finance, CoinGecko, Glassnode
On-chain: Glassnode, DefiLlama, Token Terminal, CoinGlass

## LHM Repository Structure

```
/Users/bob/LHM/
  Strategy/           # Pillar docs, CLAUDE_MASTER.md, Trading Strategy, Two Books, Asset Class Frameworks
  Brand/              # brand-guide.md, chart-styling.md, templates.md, voice-and-tone
  Scripts/            # Python scripts, chart generation, data pipeline, sync_claude_context.sh
  Data/               # Raw, processed, curated data, databases (lhm_data.db, market_data.db)
  Charts/             # Generated chart images
  Analysis/           # Research analysis files
  Working/            # Work-in-progress documents
  Website/            # LighthouseMacro.com source
  Images/             # Brand images, logos
  Outputs/            # Generated reports, PDFs
  Archive/            # Historical files
  External/           # External research
  lighthouse_quant/   # Quantitative models
  logs/               # Sync and pipeline logs
  .claude/            # Claude Code settings
  .github/            # Copilot instructions
```

## Critical Data Rules

- **Never fabricate or approximate data.** If inputs are missing, stop and request the exact source.
- **Code-first = reproducibility first.** Every output must be traceable to code.
- **Credentials and API keys:** Never commit. Use environment variables and `.env` locally.
- **PYTHONPATH:** Set to `/Users/bob/LHM` for imports.

---

# SECTION 10: CODING STANDARDS

## Python Conventions

- Python 3.8+ (target)
- Type hints and docstrings required on all public functions
- PEP8 compliant
- Use `pandas`, `numpy`, `matplotlib` as core stack; `statsmodels`/`pyarrow` optional
- Notebooks must use relative paths and set random seeds for reproducibility
- Export charts to `charts/` directory
- Tests: `pytest`, mock external API calls, include sample data

## Git Workflow

- Subtree integration pattern (not submodules) per `docs/integration-implementation-guide.md`
- Add: `git subtree add --prefix=<path> <repo> main --squash`
- Pull updates: `git subtree pull --prefix=<path> <repo> main --squash`
- Never commit raw data or secrets to `data/` or `configs/`
- Keep function signatures stable; prefer adding helpers over changing public APIs

## Charting in Code

- No gridlines. All four spines visible. Right axis primary.
- Color palette: Ocean, Dusk, Sky, Venus, Sea, Doldrums, Starboard, Port
- Line thickness ~3; longest history available
- Axes matched at zero; independently scaled for clarity
- Labels clear, no overlaps
- Watermark "MACRO, ILLUMINATED." bottom-right (never overlap data)
- Always generate both dark and white theme versions

## Allowed Bash Permissions (Claude Code)

```json
{
  "allow": [
    "Bash(source:*)", "Bash(python:*)", "Bash(python3:*)",
    "Bash(pip install:*)", "Bash(pip3 install:*)",
    "Bash(.venv/bin/pip install:*)", "Bash(.venv/bin/python3:*)",
    "Bash(wc:*)", "Bash(PYTHONPATH=/Users/bob/LHM python:*)",
    "Bash(PYTHONPATH=/Users/bob/LHM python3:*)",
    "Bash(sqlite3:*)", "Bash(pip3 list:*)",
    "Bash(chmod:*)", "Bash(open:*)", "Bash(curl:*)"
  ]
}
```

---

# SECTION 11: PROPRIETARY INDICATORS (The Codex)

| Indicator | Full Name | Definition |
|---|---|---|
| **LPI** | Labor Pressure Index | Composite labor health across flows and stocks |
| **LFI** | Labor Fragility Index | Avg(z(LongTermUnemp), z(-Quits), z(-Hires/Quits)). Structural weakness before headline unemployment. |
| **PCI** | Price Conditions Index | Inflation pressure composite |
| **GCI** | Growth Conditions Index | Real economy momentum (second derivative focus) |
| **HCI** | Housing Conditions Index | Housing market health and rate sensitivity |
| **CCI** | Consumer Conditions Index | Consumer spending and credit health |
| **BCI** | Business Conditions Index | Business investment and capex commitment |
| **TCI** | Trade Conditions Index | Dollar dynamics and trade flow impact |
| **GCI-Gov** | Government Conditions Index | Fiscal dominance and term premium dynamics |
| **FCI** | Financial Conditions Index | Credit spreads and financial stress |
| **CLG** | Credit-Labor Gap | z(HY_OAS) - z(LFI). Negative = spreads too tight for labor reality. |
| **LCI** | Liquidity Cushion Index | System shock absorption via RRP, Reserves, Funding spreads |
| **MSI** | Market Structure Index | Breadth, trend, momentum composite |
| **SPI** | Sentiment & Positioning Index | Contrarian indicator. High = Fear = Bullish |
| **SBD** | Structure-Breadth Divergence | z(Price_vs_200d) - z(%_Stocks_>_50d_MA). Distribution warning. |
| **SSD** | Sentiment-Structure Divergence | z(SPI) + z(MSI). Capitulation/Blow-off detector. |
| **MRI** | Macro Risk Index | Master composite. Synthesizes all 12 pillars. |
| **SLI** | Stablecoin Liquidity Impulse | Rate of change in stablecoin market cap. Proxy for on-chain liquidity. |

---

# SECTION 12: SYNC WORKFLOW

## Context Sync Script

**Location:** `/Users/bob/LHM/Scripts/sync_claude_context.sh`

**What it does:**
1. Updates LAST_SYNC date in CLAUDE_MASTER.md
2. Copies to Claude Code: `/Users/bob/.claude/CLAUDE.md`
3. Creates desktop export: `~/Desktop/LHM_CLAUDE_CONTEXT.md`
4. Creates Gemini export: `~/Desktop/LHM_GEMINI_CONTEXT.md`

**Automatic targets:**
- Claude Code (file copy)

**Manual targets (copy from Desktop):**
- Claude.ai/iOS (paste into custom instructions)
- Claude Desktop (paste to custom instructions)
- Gemini (paste context)

**Run command:** `bash /Users/bob/LHM/Scripts/sync_claude_context.sh`
**Alias:** `lhm-sync`

---

# REFERENCE FILES

| **Content** | **Location** |
|---|---|
| This Master Context | `/Users/bob/LHM/Strategy/CLAUDE_MASTER.md` |
| Full Pillar Details | `/Users/bob/LHM/Strategy/PILLAR [1-12] *.md` |
| Trading Strategy Master | `/Users/bob/LHM/Strategy/LIGHTHOUSE MACRO TRADING STRATEGY - MASTER.md` |
| Two Books Framework | `/Users/bob/LHM/Strategy/TWO_BOOKS_FRAMEWORK.md` |
| Asset Class Frameworks | `/Users/bob/LHM/Strategy/Asset_Class_Frameworks/*.md` |
| Indicators Reference | `/Users/bob/LHM/Strategy/LIGHTHOUSE MACRO - PROPRIETARY INDICATORS REFERENCE.md` |
| Brand Guide | `/Users/bob/LHM/Brand/brand-guide.md` |
| Chart Styling (Full Spec) | `/Users/bob/LHM/Brand/chart-styling.md` |
| Templates | `/Users/bob/LHM/Brand/templates.md` |
| Voice & Tone | `/Users/bob/LHM/Brand/voice-and-tone-for-gemini.md` |
| Writing Style (from tweets) | `/Users/bob/LHM/Working/Bob's Writing Style for Lighthouse Macro.md` |
| Domain Expertise | `/Users/bob/LHM/Working/LHM_Domain_Expertise_Clean.md` |
| Website Source | `/Users/bob/LHM/Website/` |
| Sync Script | `/Users/bob/LHM/Scripts/sync_claude_context.sh` |
| Copilot Instructions | `/Users/bob/LHM/.github/copilot-instructions.md` |
| lighthouse_mega package | `/Users/bob/lighthouse_mega/` |

---

**END OF MASTER CONTEXT**

**Version:** 4.0
**Author:** Bob Sheehan, CFA, CMT
**Last Updated:** 2026-02-06
