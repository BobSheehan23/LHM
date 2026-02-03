# Asset Class Framework: Rates (Fixed Income)

## Primary ETF Universe

### Duration Spectrum
| Ticker | Name | Duration | Expense | Use Case |
|--------|------|----------|---------|----------|
| **SHY** | iShares 1-3 Year Treasury | ~2 yrs | 0.15% | Short duration, cash alternative |
| **IEI** | iShares 3-7 Year Treasury | ~4 yrs | 0.15% | Intermediate |
| **IEF** | iShares 7-10 Year Treasury | ~7 yrs | 0.15% | Core duration |
| **TLT** | iShares 20+ Year Treasury | ~17 yrs | 0.15% | Long duration, rate bets |
| **GOVT** | iShares US Treasury Bond | ~6 yrs | 0.05% | Broad Treasury |

### Money Market / Ultra-Short
| Ticker | Name | Duration | Use Case |
|--------|------|----------|----------|
| **SGOV** | iShares 0-3 Month Treasury | ~0.1 yrs | Cash proxy, T-bill exposure |
| **BIL** | SPDR 1-3 Month T-Bill | ~0.1 yrs | Cash management |
| **SHV** | iShares Short Treasury | ~0.3 yrs | Near-cash |

### Inflation-Protected
| Ticker | Name | Use Case |
|--------|------|----------|
| **TIP** | iShares TIPS | Inflation hedge |
| **STIP** | iShares 0-5 Year TIPS | Short TIPS |

### Credit (see also CREDIT.md)
| Ticker | Name | Use Case |
|--------|------|----------|
| **LQD** | iShares IG Corporate | Investment grade |
| **HYG** | iShares High Yield | High yield (risk-on) |
| **AGG** | iShares Core US Aggregate | Broad bond market |

---

## Pillar-to-Rates Translation

### Prices Pillar (PCI) → Duration Positioning

| PCI Range | Regime | Duration Stance | Preferred ETFs |
|-----------|--------|-----------------|----------------|
| > +1.0 | High Inflation | **Underweight duration** | SGOV, SHY, TIP |
| +0.5 to +1.0 | Elevated | Neutral to short | SHY, IEI |
| -0.5 to +0.5 | On Target | Neutral | IEF, AGG |
| < -0.5 | Deflationary | **Overweight duration** | TLT, IEF |

### Plumbing Pillar (LCI) → Funding/Spread Dynamics

| LCI Range | Regime | Signal | Action |
|-----------|--------|--------|--------|
| > +0.5 | Abundant | Spreads compress | Can own credit (LQD, HYG) |
| -0.5 to +0.5 | Adequate | Neutral | Core Treasuries |
| < -0.5 | Scarce | Spreads widen risk | Treasuries only, avoid credit |
| < -1.0 | Stress | Flight to quality | TLT, SGOV (barbell) |

### Labor + Growth → Recession/Easing Signal

| Condition | Implication | Rates Action |
|-----------|-------------|--------------|
| LPI < -0.5 AND GCI < -0.3 | Recession risk >70% | Add duration (TLT) |
| LFI > +1.0 | Pre-recessionary | Anticipate Fed cuts, add duration |
| LPI > +0.5 AND GCI > +0.5 | Expansion | Reduce duration, steepener |

---

## Yield Curve Framework

### Key Spreads to Monitor

| Spread | FRED Codes | Current | Signal |
|--------|------------|---------|--------|
| **2s10s** | DGS10 - DGS2 | | Curve slope |
| **3m10y** | DGS10 - DGS3MO | | Near-term recession signal |
| **5s30s** | DGS30 - DGS5 | | Term premium |

### Curve Regime Interpretation

| 2s10s | Regime | Historical Implication |
|-------|--------|------------------------|
| > +100 bps | Steep | Early cycle, expansion |
| +50 to +100 | Normal | Mid-cycle |
| 0 to +50 | Flat | Late cycle |
| < 0 | Inverted | **Recession warning (12-18 mo lead)** |

### Steepener vs Flattener Trades

**Bull Steepener** (rates fall, curve steepens):
- Condition: Fed cutting into recession
- Trade: Long TLT, short SHY (or just long TLT)
- Pillar signal: LPI < -0.5, PCI falling

**Bear Steepener** (rates rise, curve steepens):
- Condition: Term premium repricing, fiscal concerns
- Trade: Short TLT or underweight duration
- Pillar signal: GCI-Gov elevated, supply concerns

**Bull Flattener** (rates fall, curve flattens):
- Condition: Flight to quality, deflation scare
- Trade: Long TLT
- Pillar signal: Crisis regime, LCI < -1.0

**Bear Flattener** (rates rise, curve flattens):
- Condition: Fed hiking
- Trade: Underweight duration, especially long end
- Pillar signal: PCI > +1.0, Fed tightening

---

## Real Rates Framework

### TIPS vs Nominal Treasury

Real Rate = Nominal Yield - Breakeven Inflation

| 10Y Real Rate | Regime | Implication |
|---------------|--------|-------------|
| > +2.5% | Very Restrictive | Growth headwind, equity pressure |
| +1.5 to +2.5% | Restrictive | Tightening financial conditions |
| +0.5 to +1.5% | Neutral | Normal range |
| < +0.5% | Accommodative | Supportive of risk assets |
| < 0% | Negative | Financial repression |

### When to Own TIPS

- PCI > +0.5 AND 5Y5Y forward > 2.5% → TIPS over nominals
- Breakeven < 2.0% AND PCI elevated → TIPS undervalued
- Dollar weakening (DXY < 100) → Import inflation risk, favor TIPS

---

## Position Sizing

### Duration as Risk

1 year of duration ≈ 1% price move per 100bp yield change

| ETF | Duration | Price Impact (100bp yield rise) |
|-----|----------|--------------------------------|
| SGOV | ~0.1 | -0.1% |
| SHY | ~2 | -2% |
| IEF | ~7 | -7% |
| TLT | ~17 | -17% |

### Allocation Framework

| MRI Regime | Fixed Income Allocation | Duration Target |
|------------|------------------------|-----------------|
| Low Risk | 25-30% | 5-7 years |
| Neutral | 30-35% | 4-6 years |
| Elevated | 35-45% | 3-5 years |
| High Risk | 45-55% | 2-4 years |
| Crisis | 50-65% | Barbell (0 + 15+) |

---

## Current Assessment Template

| Metric | Reading | Signal |
|--------|---------|--------|
| **10Y Yield** | | Level |
| **2s10s Spread** | | Curve |
| **10Y Real Rate** | | Restrictiveness |
| **5Y5Y Forward** | | Expectations |
| **PCI** | | Inflation regime |
| **LCI** | | Liquidity regime |

*Update dynamically with current readings.*

---

*Bob Sheehan, CFA, CMT*
*Founder & CIO, Lighthouse Macro*
