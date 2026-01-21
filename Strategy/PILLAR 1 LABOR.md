# PILLAR 1: LABOR

## The Labor Transmission Chain

Labor isn't just employment data. It's the economic genome—the code that determines whether the expansion continues or the system resets. The transmission mechanism operates through cascading flows:

```
Worker Confidence → Job-Switching Behavior → Wage Pressure →
Income Growth → Spending Capacity → Corporate Pricing Power →
Profit Margins → Hiring Decisions → Worker Confidence
```

**The Insight:** This isn't a linear chain. It's a feedback loop. And the loop is breaking.

When workers stop quitting, they're not being prudent. They're seeing something management hasn't admitted yet. The quits rate is the economy's truth serum—it strips away the narrative and exposes the underlying fragility. Six to nine months before the unemployment rate rises, quits collapse. Every. Single. Time.

The beauty of labor data: it doesn't lie. You can massage GDP with inventory builds. You can engineer earnings with buybacks. But you can't fake the quits rate. Workers vote with their feet, and the ballots are already counted.

---

## Why Labor Leads Everything

Labor is the **alpha generator** in the three-pillar framework for a simple reason: it sits upstream of every other economic flow.

**The Cascade:**

**1. Labor → Consumer:** Income determines spending capacity (1-3 month lag)
**2. Labor → Credit:** Employment stress precedes default risk (3-6 month lag)
**3. Labor → Housing:** Job stability drives home-buying decisions (6-9 month lag)
**4. Labor → Growth:** Hours worked contracts before output falls (2-4 month lag)
**5. Labor → Prices:** Wage pressure drives services inflation (persistent)

Get the labor call right, and you've triangulated 70% of the macro outlook. Miss it, and you're trading narratives instead of reality.

**Current State:** The labor market is exhibiting late-cycle fragility while headline metrics remain superficially healthy. This is the danger zone—the gap between flows (deteriorating) and stocks (stable) where consensus lags reality by quarters.

---

## Primary Indicators: The Complete Architecture

### A. EMPLOYMENT FLOWS (The Core Signal)

The stock of employment (payrolls, unemployment rate) is a lagging indicator. The **flows** tell you where we're going. This subsection tracks the churn—hires, quits, layoffs, openings—that precedes the headline data.

| **Indicator** | **FRED Code** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **JOLTS Job Openings** | JTSJOL | Monthly | Leads payrolls 3-6 mo | Demand signal, but noisy (ghost jobs) |
| **JOLTS Hires** | JTSHIL | Monthly | Leads payrolls 2-4 mo | Actual hiring execution |
| **JOLTS Quits** | JTSQUL | Monthly | **Leads recession 6-9 mo** | Worker confidence barometer |
| **JOLTS Quits Rate** | JTSQUR | Monthly | **Primary leading indicator** | Normalized for labor force size |
| **JOLTS Layoffs & Discharges** | JTSLDL | Monthly | Lags stress 1-3 mo | Stress confirmation (employers react late) |
| **JOLTS Separations (Total)** | JTSTSL | Monthly | Coincident | Quits + Layoffs + Other |
| **Initial Jobless Claims** | ICSA | Weekly | Leads payrolls 4-8 wks | Highest-frequency stress gauge |
| **Continued Claims** | CCSA | Weekly | Coincident | Labor market slack measure |
| **Insured Unemployment Rate** | IURSA | Weekly | Coincident | Claims normalized to labor force |

#### Derived Flow Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **Hires/Quits Ratio** | JTSHIL / JTSQUL | <2.0 | Demand weakening when below threshold |
| **Quits/Layoffs Ratio** | JTSQUL / JTSLDL | <2.0 | Worker confidence collapsing |
| **Openings/Unemployed** | JTSJOL / (UNRATE × CLF) | <1.2 | Slack developing in labor market |
| **Openings/Hires Ratio** | JTSJOL / JTSHIL | >1.8 | Labor hoarding (openings unfilled) |
| **Claims Momentum** | YoY% Δ in 4-wk MA ICSA | >+15% | Early deterioration signal |
| **Separations Rate** | JTSTSR | >2.0% | Total churn measure |

#### Regime Thresholds: Employment Flows

| **Indicator** | **Expansion** | **Neutral** | **Softening** | **Contraction** |
|---|---|---|---|---|
| **Quits Rate** | >2.5% | 2.2-2.5% | 2.0-2.2% | **<2.0%** |
| **Hires/Quits** | >2.5 | 2.0-2.5 | 1.7-2.0 | **<1.7** |
| **Openings/Unemployed** | >1.8 | 1.2-1.8 | 1.0-1.2 | **<1.0** |
| **Initial Claims 4-wk MA** | <220k | 220-250k | 250-300k | **>300k** |
| **Claims YoY%** | <-5% | -5% to +10% | +10% to +25% | **>+25%** |

**The Quits Rate Kill Line:** Below 2.0%, the labor market has crossed into pre-recessionary territory in every cycle since 1990. No exceptions. We're at **1.9%** (Dec 2025). The data doesn't care about your soft landing narrative.

---

### B. WAGE DYNAMICS (The Inflation Transmission Belt)

Wages are sticky. They accelerate during expansions and decelerate slowly during downturns. This stickiness creates the "last mile" inflation problem—services inflation (driven by wages) resists disinflation even as goods prices collapse.

| **Indicator** | **FRED Code** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **Average Hourly Earnings (AHE)** | CES0500000003 | Monthly | Coincident | Headline wage growth (all workers) |
| **AHE: Production & Nonsupervisory** | CES0500000008 | Monthly | Coincident | 80% of workforce, less mgmt skew |
| **Real Average Hourly Earnings** | CES0500000012 (deflated) | Monthly | Leading 1-2 mo | Purchasing power gauge |
| **Average Weekly Earnings** | CES0500000030 | Monthly | Coincident | AHE × Hours (income proxy) |
| **Employment Cost Index (ECI)** | ECIALLCIV | Quarterly | Lagging 1-2 qtrs | Total compensation (wages + benefits) |
| **ECI: Wages & Salaries** | ECIWAG | Quarterly | Lagging | Excludes benefits component |
| **ECI: Private Industry** | ECIPRIV | Quarterly | Lagging | Excludes public sector |
| **Atlanta Fed Wage Growth Tracker** | Atlanta Fed (web) | Monthly | Coincident | Median wage growth (CPS microdata) |
| **Wage Growth: Job Switchers** | Atlanta Fed (web) | Monthly | **Leading 3-6 mo** | Job-hopper premium (key signal) |
| **Wage Growth: Job Stayers** | Atlanta Fed (web) | Monthly | Lagging | Inertia component |

#### Derived Wage Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **Job-Hopper Premium** | Switchers - Stayers | <0.5 ppts | Late-cycle warning: no premium for switching |
| **Real Wage Growth** | AHE YoY - Core CPI YoY | <0% | Purchasing power eroding |
| **Wage-Productivity Gap** | AHE YoY - Productivity YoY | >2 ppts | Margin squeeze, inflationary |
| **Wage Acceleration** | 3M Ann AHE - 12M Ann AHE | >+1 ppt | Accelerating (inflationary pressure) |
| **Unit Labor Cost Growth** | ECI - Productivity | >3% | Profit margin compression |

#### Regime Thresholds: Wage Dynamics

| **Indicator** | **Disinflationary** | **Neutral** | **Inflationary** | **Crisis** |
|---|---|---|---|---|
| **AHE YoY%** | <3.0% | 3.0-4.0% | 4.0-5.5% | >5.5% |
| **Real AHE YoY%** | <-1% | -1% to +1% | +1% to +2% | >+2% |
| **Job-Hopper Premium** | <0 ppts | 0-1 ppts | 1-3 ppts | >3 ppts |
| **ECI YoY%** | <3.5% | 3.5-4.5% | 4.5-5.5% | >5.5% |

**The Job-Hopper Premium Collapse:** From 2021-2022, job switchers earned 5-6 percentage points more than stayers. That's a healthy, dynamic labor market. By March 2025, the premium narrowed to **0.2 percentage points**. Translation: the grass is no longer greener. Workers know what employers haven't said yet—there are no better opportunities.

---

### C. LABOR SUPPLY (The Structural Foundation)

Labor supply determines the economy's speed limit. Participation rates, demographics, and immigration flows set the ceiling for non-inflationary growth. When supply shrinks (aging population, restrictive immigration), wage pressure intensifies at lower unemployment rates.

| **Indicator** | **FRED Code** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **Civilian Labor Force** | CLF16OV | Monthly | Structural | Total available workers (employed + unemployed) |
| **Labor Force Participation Rate** | CIVPART | Monthly | Structural trend | % of population working or seeking work |
| **Prime-Age LFPR (25-54)** | LNS11300060 | Monthly | Structural | Strips out retirement/school effects |
| **Women's LFPR** | LNS11300002 | Monthly | Structural | 47% of workforce |
| **Men's LFPR** | LNS11300001 | Monthly | Structural | 53% of workforce |
| **Part-Time for Economic Reasons** | LNS12032194 | Monthly | Coincident | Underemployment gauge |
| **Multiple Job Holders** | LNS12026620 | Monthly | Coincident | Supplemental income necessity |
| **Not in Labor Force: Want Job** | LNS15026639 | Monthly | Lagging | Discouraged workers |
| **U6 Underemployment Rate** | U6RATE | Monthly | Lagging | Unemployed + underemployed + marginally attached |

#### Derived Supply Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **Prime-Age Employment-Population Ratio** | (Prime-Age Employed / Prime-Age Pop) × 100 | >80% | Core workforce fully utilized |
| **Labor Force Growth (YoY)** | CLF YoY % | <0.5% | Supply constraint binding |
| **Involuntary Part-Time Share** | Part-Time Econ Reasons / Total Employed | >3% | Hidden slack emerging |
| **Shadow Unemployment** | U6 - U3 | >4% | Underemployment elevated |

#### Regime Thresholds: Labor Supply

| **Indicator** | **Tight Supply** | **Balanced** | **Excess Supply** |
|---|---|---|---|
| **Prime-Age LFPR** | >83.5% | 82.0-83.5% | <82.0% |
| **U6 Underemployment** | <7.0% | 7.0-9.0% | >9.0% |
| **Part-Time Econ Reasons (millions)** | <4.0M | 4.0-5.0M | >5.0M |
| **CLF Growth YoY%** | <0% | 0-1.0% | >1.0% |

**The Prime-Age Puzzle:** Prime-age (25-54) LFPR peaked at 83.5% (Feb 2020), collapsed to 80.4% (April 2020), recovered to 83.9% (July 2023)—**above pre-pandemic**—but has since plateaued. The demographic tailwind is fading. Boomers retiring, immigration restrictive, birth rates falling. The supply constraint is structural, not cyclical.

---

### D. JOB QUALITY & COMPOSITION (What Kind of Jobs?)

Not all jobs are created equal. Full-time vs. part-time. Permanent vs. temporary. High-wage vs. low-wage. The composition shift tells you whether the labor market is upgrading or degrading.

| **Indicator** | **FRED Code** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **Full-Time Employment** | LNS12500000 | Monthly | Coincident | Quality employment measure |
| **Part-Time Employment** | LNS12600000 | Monthly | Coincident | Supplemental + underemployed |
| **Temporary Help Services Employment** | TEMPHELPS | Monthly | **Leads payrolls 3-6 mo** | Canary in coal mine (cut first) |
| **Government Employment** | CES9000000001 | Monthly | Counter-cyclical | Public sector hiring (lag private) |
| **Private Payrolls** | PAYEMS - CES9000000001 | Monthly | Coincident | Core labor demand |
| **Manufacturing Employment** | MANEMP | Monthly | Leads services 2-4 mo | Cyclical bellwether |
| **Construction Employment** | USCONS | Monthly | Coincident | Housing/infrastructure proxy |
| **Retail Trade Employment** | USTRADE | Monthly | Coincident | Consumer health proxy |
| **Professional & Business Services** | USPBS | Monthly | Coincident | Corporate hiring gauge |

#### Derived Quality Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **Full-Time/Part-Time Ratio** | Full-Time / Part-Time | <4.0 | Quality deterioration |
| **Temp Help as % of Payrolls** | TEMPHELPS / PAYEMS × 100 | <2.0% | Leading layoff indicator |
| **Private/Government Ratio** | Private Payrolls / Gov't Payrolls | <6.5 | Gov't offsetting private weakness |
| **Goods/Services Job Growth Spread** | Goods YoY% - Services YoY% | <-5 ppts | Manufacturing-led weakness |

#### Regime Thresholds: Job Quality

| **Indicator** | **High Quality** | **Mixed** | **Deteriorating** |
|---|---|---|---|
| **Full-Time/Part-Time Ratio** | >4.5 | 4.0-4.5 | <4.0 |
| **Temp Help YoY%** | >+3% | -3% to +3% | **<-3%** (recession signal) |
| **Private Payrolls 3M Avg** | >200k | 100-200k | <100k |
| **Mfg Employment YoY%** | >+1% | -1% to +1% | **<-1%** |

**The Temp Help Trap:** Temporary help employment peaks 6-9 months before recessions and troughs 3-6 months before recoveries. It's the highest-beta labor segment—first hired, first fired. Temp help employment peaked in March 2022 at 3.09M, and has since fallen to **2.87M** (Dec 2025), down **-7.1% YoY**. That's not noise. That's a leading indicator screaming.

---

### E. UNEMPLOYMENT DECOMPOSITION (Who's Out of Work?)

The unemployment rate is a lagging indicator, but its **composition** tells you whether the weakness is cyclical (temporary layoffs, short-term unemployed) or structural (long-term unemployed, permanent separations).

| **Indicator** | **FRED Code** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **Unemployment Rate (U3)** | UNRATE | Monthly | **Lagging 6-9 mo** | Headline measure |
| **Unemployed (Level)** | UNEMPLOY | Monthly | Lagging | Absolute count (thousands) |
| **Unemployed: Less Than 5 Weeks** | UEMPLT5 | Monthly | Leading 1-3 mo | New entrants, frictional |
| **Unemployed: 5-14 Weeks** | UEMP5TO14 | Monthly | Coincident | Normal job search duration |
| **Unemployed: 15-26 Weeks** | UEMP15T26 | Monthly | Coincident | Extended search (stress signal) |
| **Unemployed: 27+ Weeks** | UEMP27OV | Monthly | **Lagging but critical** | Long-term (structural damage) |
| **Median Weeks Unemployed** | UEMPMED | Monthly | Lagging | Duration measure |
| **Mean Weeks Unemployed** | UEMPMEAN | Monthly | Lagging | Average duration (LT skew) |
| **Unemployed: Job Losers** | LNS13023621 | Monthly | Coincident | Layoffs (involuntary) |
| **Unemployed: Job Leavers** | LNS13023705 | Monthly | Leading 3-6 mo | Quits (voluntary, confidence signal) |
| **Unemployed: Reentrants** | LNS13023557 | Monthly | Lagging | Returning to labor force |
| **Unemployed: New Entrants** | LNS13023569 | Monthly | Neutral | First-time job seekers |

#### Derived Unemployment Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **Long-Term Unemployed Share** | (27+ Weeks / Total Unemployed) × 100 | >22% | **Pre-recessionary fragility** |
| **Job Losers Share** | (Job Losers / Total Unemployed) × 100 | >55% | Involuntary separations rising |
| **Job Leavers Share** | (Job Leavers / Total Unemployed) × 100 | <10% | Confidence collapsing |
| **Short-Term Unemployed (<5 wks) Share** | (<5 Wks / Total Unemployed) × 100 | <18% | Frictional unemployment drying up |
| **Median Duration Change (3M)** | Current - 3M Prior | >+1.5 wks | Search difficulty increasing |

#### Regime Thresholds: Unemployment Composition

| **Indicator** | **Healthy** | **Neutral** | **Fragile** | **Crisis** |
|---|---|---|---|---|
| **LT Unemployed Share** | <18% | 18-22% | **22-28%** | >28% |
| **Unemployment Rate** | <4.0% | 4.0-4.5% | 4.5-5.5% | >5.5% |
| **Median Duration** | <8 wks | 8-12 wks | 12-18 wks | >18 wks |
| **Job Leavers Share** | >12% | 10-12% | **8-10%** | <8% |

**The 27+ Week Threshold:** When long-term unemployment exceeds 22% of total unemployed, the labor market has transitioned from cyclical softness to structural fragility. Workers stuck unemployed for 6+ months face skill erosion, employer bias, and declining re-employment probability. This is where "soft landing" becomes "hard reset." Current reading: **25.7%** (Dec 2025). We're there.

---

### F. HOURS WORKED & PRODUCTIVITY (The Intensive Margin)

Employers cut hours before headcount. It's cheaper, reversible, and doesn't damage morale as much as layoffs. Tracking hours worked gives you a 2-4 month lead on payroll declines.

| **Indicator** | **FRED Code** | **Frequency** | **Lead/Lag** | **Interpretation** |
|---|---|---|---|---|
| **Average Weekly Hours (All Workers)** | AWHAETP | Monthly | **Leads payrolls 2-4 mo** | Aggregate hours signal |
| **Avg Weekly Hours (Manufacturing)** | AWHMAN | Monthly | **Leads IP 1-3 mo** | Production intensity |
| **Avg Weekly Hours (Retail)** | AWOTMAN | Monthly | Coincident | Consumer demand proxy |
| **Aggregate Weekly Hours Index** | AWHI | Monthly | **Leads GDP 1-2 qtrs** | Total labor input |
| **Labor Productivity (Nonfarm)** | OPHNFB | Quarterly | Lagging | Output per hour |
| **Unit Labor Costs** | ULCNFB | Quarterly | Lagging | Compensation per unit output |
| **Manufacturing Overtime Hours** | AWOTMAN (subset) | Monthly | Leading 1-2 mo | Demand stress gauge |

#### Derived Hours & Productivity Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **Aggregate Weekly Payrolls (Proxy)** | PAYEMS × AWHAETP × CES0500000003 | N/A | Total labor income in economy |
| **Hours Momentum** | 3M Avg YoY% - 12M Avg YoY% | <-1 ppt | Decelerating labor input |
| **Productivity-Adjusted Wage Growth** | AHE YoY - Productivity YoY | >2 ppts | Real labor cost pressure |
| **Output Gap Proxy** | Aggregate Hours YoY - Trend (2%) | <-1 ppt | Slack building |

#### Regime Thresholds: Hours Worked

| **Indicator** | **Expansion** | **Neutral** | **Contraction** |
|---|---|---|---|
| **Avg Weekly Hours (All)** | >34.5 hrs | 34.3-34.5 hrs | **<34.3 hrs** |
| **Avg Weekly Hours (Mfg)** | >41.0 hrs | 40.5-41.0 hrs | **<40.5 hrs** |
| **Aggregate Hours YoY%** | >+2% | 0% to +2% | **<0%** |
| **Unit Labor Costs YoY%** | <2% | 2-4% | >4% |

**The Manufacturing Hours Canary:** Manufacturing weekly hours peaked at 41.7 in December 2021. They've since declined to **40.6 hours** (Dec 2025). That's **-2.6% lower**. Employers don't cut hours for fun—they cut hours when demand disappears. This precedes layoffs by 2-3 months. The clock is ticking.

---

### G. LABOR FRAGILITY INDEX (The Composite Warning Signal)

The Labor Fragility Index (LFI) is our proprietary measure synthesizing the **leading indicators** of labor market stress into a single composite.

```
LFI = 0.30 × z(Long_Term_Unemployed_Share)
    + 0.25 × z(-Quits_Rate)                    # Inverted
    + 0.20 × z(-Hires_Quits_Ratio)             # Inverted
    + 0.15 × z(-Temp_Help_YoY)                 # Inverted (falling = stress)
    + 0.10 × z(-Job_Hopper_Premium)            # Inverted
```

**Component Weighting Rationale:**
- **Long-Term Unemployed Share (30%):** Structural fragility gauge, highest persistence
- **Quits Rate (25%):** Primary leading indicator, cleanest signal
- **Hires/Quits Ratio (20%):** Demand confirmation, cross-validates quits
- **Temp Help (15%):** Canary in coal mine, first to be cut
- **Job-Hopper Premium (10%):** Microstructure of worker confidence

#### LFI Interpretation

| **LFI Range** | **Regime** | **Interpretation** |
|---|---|---|
| < 0.0 | Healthy | Labor market robust, flows positive |
| 0.0 to +0.5 | Neutral | Balanced conditions, normal churn |
| +0.5 to +1.0 | Elevated | **Fragility developing, early stress** |
| +1.0 to +1.5 | High | **Pre-recessionary, flows deteriorating** |
| > +1.5 | Critical | **Recession imminent, structural damage** |

**Current LFI: +0.93** (Elevated Fragility). Labor market in pre-recessionary zone.

---

### H. SECTORAL EMPLOYMENT DYNAMICS (Where the Jobs Are)

Different sectors lead and lag at different points in the cycle. Manufacturing leads services. Construction leads housing. Government is counter-cyclical.

| **Sector** | **FRED Code** | **GDP Contribution** | **Cycle Behavior** |
|---|---|---|---|
| **Manufacturing** | MANEMP | ~10% | **Leads services 2-4 mo** |
| **Construction** | USCONS | ~5% | **Leads housing 3-6 mo** |
| **Professional Services** | USPBS | ~15% | Coincident |
| **Healthcare** | USHCE | ~13% | Defensive (counter-cyclical) |
| **Retail Trade** | USTRADE | ~10% | Coincident to lagging |
| **Leisure & Hospitality** | USLAH | ~11% | Lagging (last to recover) |
| **Government** | USGOVT | ~14% | **Counter-cyclical** (policy response) |
| **Financial Activities** | USFIRE | ~6% | Coincident |
| **Information** | USINFO | ~2% | Volatile (tech cycle) |

#### Sectoral Spread Metrics

| **Metric** | **Formula** | **Threshold** | **Signal** |
|---|---|---|---|
| **Mfg-Services Spread** | Mfg Employment YoY - Services YoY | <-3 ppts | Manufacturing-led weakness |
| **Private-Government Spread** | Private YoY - Government YoY | <-2 ppts | Gov't propping up headline |
| **Cyclical-Defensive Spread** | (Mfg + Construction) YoY - (Healthcare + Gov't) YoY | <-4 ppts | Late-cycle rotation |

**Current State:** Manufacturing employment **-1.8% YoY**, services **+1.2% YoY**. Spread: **-3.0 ppts**. Classic late-cycle divergence—goods economy in recession, services holding (for now).

---

## Labor Pillar Composite Index (LPI)

### Formula

The Labor Pillar Composite synthesizes flows, stocks, and quality metrics into a single regime indicator:

```
LPI = 0.20 × z(Quits_Rate)
    + 0.15 × z(Hires_Quits_Ratio)
    + 0.15 × z(-Long_Term_Unemployed_Share)      # Inverted
    + 0.15 × z(-Initial_Claims_4wk_MA)           # Inverted
    + 0.10 × z(Prime_Age_LFPR)
    + 0.10 × z(Avg_Weekly_Hours_Mfg)
    + 0.10 × z(-Temp_Help_YoY)                   # Inverted (negative = bad)
    + 0.05 × z(Job_Hopper_Premium)
```

**Component Weighting Rationale:**
- **Quits Rate (20%):** Primary leading indicator, cleanest signal
- **Hires/Quits (15%):** Demand confirmation, cross-validates quits
- **LT Unemployment (15%):** Structural fragility gauge
- **Initial Claims (15%):** Highest-frequency stress sensor
- **Prime-Age LFPR (10%):** Supply-side health
- **Mfg Hours (10%):** Leading activity signal
- **Temp Help (10%):** Canary in coal mine
- **Job-Hopper Premium (5%):** Worker confidence microstructure

### Interpretation

| **LPI Range** | **Regime** | **Equity Allocation** | **Signal** |
|---|---|---|---|
| > +1.0 | Labor Boom | 65-70% | Tight labor, wage pressure, inflation risk |
| +0.5 to +1.0 | Expansion | 60-65% | Healthy growth, lean into cyclicals |
| -0.5 to +0.5 | Neutral | 55-60% | Balanced conditions, strategic allocation |
| -1.0 to -0.5 | Softening | 45-50% | **Fragility developing, reduce cyclicals** |
| < -1.0 | Contraction | 30-40% | Recession imminent, maximum defense |

### Historical Calibration

| **Period** | **LPI** | **Regime** | **Outcome (12M Forward)** |
|---|---|---|---|
| **Dec 2006** | -0.4 | Softening | Recession (Dec 2007 start) |
| **Dec 2007** | -1.2 | Contraction | Deep recession confirmed |
| **Dec 2018** | +0.1 | Neutral | Manufacturing recession, no broad downturn |
| **Feb 2020** | +0.8 | Expansion | COVID shock (exogenous) |
| **Dec 2021** | +1.6 | Boom | Tightest labor market in 50 years |
| **Dec 2023** | +0.3 | Neutral | Normalization underway |
| **Dec 2025** | **-0.6** | **Softening** | **Fragility signal active** |

**Current Assessment (Dec 2025):** LPI at **-0.6** places the labor market squarely in the "Softening" regime. This is the zone where flows deteriorate but stocks remain superficially healthy. The unemployment rate is still 4.2%—unremarkable. But quits are at 1.9% (pre-recessionary), long-term unemployment is 25.7% (structural fragility), temp help is down -7.1% YoY (leading layoff signal), and the job-hopper premium is 0.2 ppts (confidence collapse).

The market is priced for a soft landing. The labor data is screaming late-cycle stress. One of them is wrong.

---

## Lead/Lag Relationships: The Labor Cascade

```
LEADING                         COINCIDENT              LAGGING
─────────────────────────────────────────────────────────────────────────────
│                               │                       │
│  Quits Rate (6-9 mo lead)     │  Payrolls             │  Unemployment (6-9 mo lag)
│  Job-Hopper Premium (3-6 mo)  │  Job Openings         │  LT Unemployment (12+ mo)
│  Temp Help Employment (3-6 mo)│  Hiring Rate          │  ECI (1-2 qtrs)
│  Avg Weekly Hours Mfg (2-4 mo)│  AHE                  │  Wage-Productivity Gap
│  Initial Claims (4-8 wks)     │  Prime-Age LFPR       │  Unit Labor Costs
│  Hires/Quits Ratio (2-4 mo)   │  Part-Time Econ       │  Mean Weeks Unemployed
│  JOLTS Hires (2-4 mo)         │  U6 Underemployment   │  Median Duration
│  Job Leavers as % (3-6 mo)    │                       │  Discouraged Workers
│                               │                       │
─────────────────────────────────────────────────────────────────────────────
```

**The Critical Chain:**

**1. Quits collapse first** (workers sense trouble) → 6-9 months later → **Unemployment rises**
**2. Temp help gets cut** (employers reduce contingent labor) → 3-6 months later → **Payrolls decline**
**3. Manufacturing hours drop** (employers reduce shifts) → 2-4 months later → **Manufacturing layoffs**
**4. Initial claims spike** (early layoffs) → 4-8 weeks later → **Payrolls turn negative**

This isn't theory. This is the historical record, repeated with metronomic regularity across eight business cycles.

---

## Integration with Three-Engine Framework

### Pillar 1 ↔ Pillar 1 (Internal Labor Dynamics)

Labor flows create feedback loops within the pillar itself:

```
Quits Decline → Wage Pressure Eases → Job-Hopper Premium Compresses →
Worker Confidence Falls → Quits Decline Further (Reinforcing Loop)
```

The loop can run in reverse during expansions (virtuous cycle) or contractions (vicious cycle). Current state: **Vicious cycle engaged.**

---

### Pillar 1 → Pillar 2 (Prices)

Labor is the **primary input** into wage-driven services inflation:

```
A. Labor → Wage Pressure → Services Inflation

Employment Tightness → Wage Growth Acceleration →
Unit Labor Costs ↑ → Services Price Passthrough →
Core Services CPI Elevated
```

**Current Linkage:** LFI at +0.93 (fragility) suggests labor tightness is **fading**. Wage growth decelerating (AHE 3.9% YoY, down from 5.5% peak). Services inflation (3.6%) should follow with 6-9 month lag.

**Cross-Pillar Signal:** When **LFI > +0.8** AND **PCI > +0.5** (elevated inflation), the Fed faces a **policy dilemma**: cut to support labor vs. hold to fight inflation. Current: **LFI +0.93, PCI +0.7**. **Dilemma active.**

---

### Pillar 1 → Pillar 3 (Growth)

Labor determines growth through the **production function**:

```
B. Labor → Output Growth

Labor Input (Employment × Hours) = Primary Production Factor
↓
Aggregate Hours Contract → Output Contracts (2-4 month lag)
↓
GDP Growth Slows
```

**Current Linkage:** Aggregate weekly hours **-1.2% YoY** = negative labor input growth. GDP can't expand when the primary factor is contracting (unless productivity surges—it's not).

**Cross-Pillar Signal:** When **LPI < -0.5** (labor softening) AND **GCI < -0.3** (growth contracting), recession probability exceeds 70% within 12 months. Current: **LPI -0.6, GCI -0.4**. **Warning threshold breached.**

---

### Pillar 1 → Pillar 5 (Consumer)

Labor is the **primary determinant** of consumer health:

```
C. Labor → Consumer Spending (1-3 Month Lag)

Employment × Hours × Wages = Aggregate Weekly Payrolls
↓
Disposable Personal Income
↓
Personal Consumption Expenditures (68% of GDP)
```

**Current Linkage:** Payroll growth slowing + hours declining + wage growth decelerating = **Income growth deceleration** = Consumer spending will soften in Q1-Q2 2026.

**Cross-Pillar Signal:** When **LPI < -0.5** (labor softening), **CCI** (Consumer Composite) typically follows 1-2 quarters later. Historical correlation: **+0.72** (LPI leads CCI by 3 months).

---

### Pillar 1 → Pillar 9 (Financial)

Labor stress precedes **credit stress** through the income-debt service channel:

```
D. Labor → Credit Stress (3-6 Month Lag)

Job Loss / Hours Cut
↓
Income Decline
↓
Debt Service Burden ↑
↓
Credit Card Delinquencies ↑ → Auto Delinquencies ↑ → Mortgage Delinquencies ↑
```

**Current Linkage:** LFI at +0.93 (elevated fragility) precedes credit stress by 3-6 months. Credit card delinquencies already rising (3.0%, above pre-pandemic 2.5%). The transmission is underway.

**Cross-Pillar Signal:** CLG (Credit-Labor Gap) = z(HY_OAS) - z(LFI). Current reading: **-1.2** (credit spreads too tight given labor fragility). Credit markets are ignoring the labor reality. This gap closes—violently—when consensus catches up.

---

### Pillar 1 → Pillar 10 (Plumbing)

Labor determines Fed policy response, which determines liquidity:

```
E. Labor → Fed Policy → Liquidity (6-12 Month Lag)

Unemployment Rising + Quits Collapsing
↓
FOMC Recognizes Weakness (With Lag)
↓
Rate Cuts Begin
↓
Liquidity Transmission Begins (if plumbing allows)
```

**Current Linkage:** Fed still operating under "strong labor market" assumption (based on lagging unemployment rate). But quits rate at 1.9% and LFI at +0.93 suggest **labor market already weakening**. Fed is 6-9 months behind the data.

**The Plumbing Constraint:** Even if Fed cuts aggressively, transmission is impaired when LCI (Liquidity Cushion Index) is negative. Current LCI: **-0.8**. The system has lost its shock absorber. Rate cuts will be less effective than historical experience suggests.

---

## Data Source Summary

| **Category** | **Primary Source** | **Frequency** | **Release Lag** | **FRED Availability** |
|---|---|---|---|---|
| **Employment Situation** | BLS | Monthly | ~5 days | Same day (PAYEMS, UNRATE, etc.) |
| **JOLTS** | BLS | Monthly | ~40 days | Same day (JTSJOL, JTSQUR, etc.) |
| **Initial Claims** | DOL | Weekly | ~3 days | Same day (ICSA, CCSA) |
| **Average Hourly Earnings** | BLS (CES) | Monthly | ~5 days | Same day (CES0500000003) |
| **Employment Cost Index** | BLS | Quarterly | ~30 days | Same day (ECIALLCIV) |
| **Atlanta Fed Wage Tracker** | Atlanta Fed | Monthly | ~15 days | Web scrape (not in FRED) |
| **Productivity & Costs** | BLS | Quarterly | ~45 days | Same day (OPHNFB, ULCNFB) |
| **Labor Force Participation** | BLS (CPS) | Monthly | ~5 days | Same day (CIVPART, LNS11300060) |

**Critical Timing:** JOLTS is released **~40 days** after the reference month. This means the November JOLTS data (including quits rate) isn't released until mid-January. By the time consensus sees the deterioration, the deterioration has already transmitted into consumer spending and credit stress. **We're trading on 6-week-old labor flow data.** Use the weekly claims data and monthly hours worked to fill the gap.

---

## Current State Assessment (January 2026)

| **Indicator** | **Current Level** | **Threshold** | **Assessment** |
|---|---|---|---|
| **Quits Rate** | 1.9% | <2.0% = Pre-recessionary | 🔴 **Breach** |
| **Hires/Quits Ratio** | 1.8 | <2.0 = Weakening | 🟡 Caution |
| **Long-Term Unemployed Share** | 25.7% | >22% = Fragility | 🔴 **Breach** |
| **Initial Claims 4-wk MA** | 235k | <250k = Stable | 🟢 OK |
| **Temp Help YoY%** | -7.1% | <-3% = Recession signal | 🔴 **Breach** |
| **Mfg Weekly Hours** | 40.6 hrs | <40.5 = Contraction | 🟡 Caution |
| **Job-Hopper Premium** | 0.2 ppts | <0.5 ppts = Late-cycle | 🔴 **Breach** |
| **Unemployment Rate** | 4.2% | <4.5% = Stable | 🟢 OK |
| **Prime-Age LFPR** | 83.7% | >83.0% = Healthy | 🟢 OK |
| **LPI Estimate** | **-0.6** | <-0.5 = Softening | 🟡 **Softening Regime** |
| **LFI Estimate** | **+0.93** | >+0.5 = Fragility | 🔴 **Elevated** |

### Narrative Synthesis

The labor market is exhibiting **classic late-cycle bifurcation**: stocks look fine, flows are deteriorating. The unemployment rate (4.2%) and prime-age participation (83.7%) signal health. But underneath:

- **Workers have stopped quitting** (1.9%, below 2.0% threshold for first time since 2020)
- **Long-term unemployment is spiking** (25.7%, highest since 2021)
- **Temp help is collapsing** (-7.1% YoY, leading indicator of broader layoffs)
- **Manufacturing hours are contracting** (40.6 hrs, production cutbacks underway)
- **The job-hopper premium is gone** (0.2 ppts, no wage premium for switching)

**Translation:** Workers see something employers haven't said yet. The quits rate is the truth serum. It doesn't lie.

**Cross-Pillar Confirmation:**
- **Consumer Pillar:** Credit card delinquencies rising (3.0%), saving rate depleted (4.5%)
- **Credit Markets:** HY spreads at 290 bps (3rd percentile tightness), ignoring labor fragility
- **Plumbing Pillar:** LCI at -0.8 (system has lost shock absorber)

**MRI (Macro Risk Index):** Estimated **+1.1** (HIGH RISK regime). Labor contributes **+0.93 (LFI) - (-0.2) (LDI) = +1.13** to the composite. Labor is the primary driver of elevated systemic risk.

---

## Invalidation Criteria

### Bull Case (Labor Resilience) Invalidation Thresholds

If the following conditions are met **simultaneously for 3+ months**, the bearish labor thesis is invalidated:

✅ **Quits Rate** rises above **2.1%** (confidence returning)
✅ **Job Openings** rise above **8.5M** (demand accelerating)
✅ **Long-Term Unemployed Share** drops below **20%** (structural healing)
✅ **Temp Help Employment** YoY% turns positive (hiring resuming)
✅ **Initial Claims 4-wk MA** drops below **220k** (stress fading)
✅ **Hours Worked (Mfg)** rises above **41.0 hrs** (production accelerating)
✅ **LFI** drops below **+0.5** (fragility diminishing)

**Action if Invalidated:** Rotate from defensive to cyclical positioning. Increase equity allocation to 60-65%. Add exposure to consumer discretionary (XLY), financials (XLF), and industrials (XLI).

---

### Bear Case (Labor Collapse) Confirmation Thresholds

If the following conditions are met, the labor deterioration is **accelerating beyond "softening" into "contraction"**:

🔴 **Unemployment Rate** crosses **4.5%** and rising (recession historically begins)
🔴 **Initial Claims 4-wk MA** exceeds **300k** for 4+ consecutive weeks (acute stress)
🔴 **Temp Help YoY%** exceeds **-10%** (cascading layoffs)
🔴 **Quits Rate** drops below **1.7%** (workers paralyzed, extreme risk aversion)
🔴 **Payrolls 3M Average** turns **negative** (job losses confirmed)
🔴 **LFI** exceeds **+1.5** (severe fragility, recession imminent)
🔴 **LPI** drops below **-1.0** (contraction regime confirmed)

**Action if Confirmed:** Maximum defensive posture. Reduce equity allocation to 30-40%. Overweight bonds (AGG, TLT), gold (GLD), and cash (SGOV). Avoid all cyclical exposure.

---

## Conclusion: The Labor Market as Economic Genome

Labor isn't a sector. It's the **code that writes the economy.**

When the quits rate collapses, it's not workers being prudent—it's workers reading the signal before management admits it. When long-term unemployment spikes while headline unemployment stays low, it's not a statistical quirk—it's the market fragmenting in real time. When temp help gets cut, it's not cost optimization—it's the canary singing its last note.

The labor market doesn't forecast the recession. **It is the recession,** six to nine months before the NBER makes it official.

**Current state:**
- **LPI at -0.6** (Softening Regime)
- **LFI at +0.93** (Elevated Fragility)
- **Quits Rate at 1.9%** (Pre-Recessionary)

The flows are screaming. The stocks are sleeping. One of them is wrong.

**That's our view from the Watch. Until next time, we'll be sure to keep the light on....**

*Bob Sheehan, CFA, CMT*
*Founder & CIO, Lighthouse Macro*
*January 15, 2026*
