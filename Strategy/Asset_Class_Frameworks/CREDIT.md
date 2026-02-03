# Asset Class Framework: Credit

## Primary ETF Universe

### Investment Grade
| Ticker | Name | Duration | Spread | Expense |
|--------|------|----------|--------|---------|
| **LQD** | iShares IG Corporate | ~9 yrs | ~90-150 bps | 0.14% |
| **VCIT** | Vanguard Intermediate-Term Corp | ~6 yrs | ~80-130 bps | 0.04% |
| **VCSH** | Vanguard Short-Term Corp | ~3 yrs | ~50-90 bps | 0.04% |
| **IGIB** | iShares 5-10 Year IG Corp | ~7 yrs | ~90-140 bps | 0.06% |

### High Yield
| Ticker | Name | Duration | Spread | Expense |
|--------|------|----------|--------|---------|
| **HYG** | iShares High Yield Corporate | ~4 yrs | ~300-500 bps | 0.49% |
| **JNK** | SPDR High Yield | ~4 yrs | ~300-500 bps | 0.40% |
| **SHYG** | iShares 0-5 Year HY | ~2 yrs | ~280-450 bps | 0.30% |
| **USHY** | iShares Broad USD HY | ~4 yrs | ~300-500 bps | 0.15% |

### Leveraged Loans (Floating Rate)
| Ticker | Name | Duration | Use Case | Expense |
|--------|------|----------|----------|---------|
| **BKLN** | Invesco Senior Loan | ~0.1 yrs | Floating rate, rate hedge | 0.65% |
| **SRLN** | SPDR Senior Loan | ~0.1 yrs | Floating rate | 0.70% |

### Emerging Market Debt
| Ticker | Name | Duration | Use Case | Expense |
|--------|------|----------|----------|---------|
| **EMB** | iShares JP Morgan USD EM Bond | ~7 yrs | USD-denominated EM | 0.39% |
| **EMLC** | VanEck EM Local Currency | ~5 yrs | Local currency EM | 0.30% |

---

## Pillar-to-Credit Translation

### Financial Pillar (FCI) → Credit Spreads

| FCI Range | Credit Regime | Spread Behavior |
|-----------|---------------|-----------------|
| > +0.5 | Healthy | Spreads tight, carry attractive |
| -0.5 to +0.5 | Neutral | Normal spreads |
| -0.5 to -1.0 | Stress | Spreads widening |
| < -1.0 | Crisis | Spreads blowout, avoid HY |

### Credit-Labor Gap (CLG)

```
CLG = z(HY_OAS) - z(LFI)
```

| CLG Range | Signal | Action |
|-----------|--------|--------|
| > +1.0 | Credit too wide for labor | Buy HY (value) |
| -0.5 to +1.0 | Aligned | Hold current allocation |
| < -0.5 | Credit too tight for labor | **Reduce HY** |
| < -1.0 | Credit ignoring fundamentals | **Avoid HY entirely** |

This is the key cross-pillar signal: when credit spreads are tight while labor fragility is elevated, credit markets are mispricing risk.

### Plumbing Pillar (LCI) → Funding Conditions

| LCI Range | Credit Impact | Trade |
|-----------|---------------|-------|
| > +0.5 | Abundant liquidity, spread compression | Own credit |
| -0.5 to +0.5 | Adequate | Neutral |
| < -0.5 | Scarce liquidity, spread pressure | Reduce credit |
| < -1.0 | Funding stress | Treasuries only |

---

## Spread Framework

### HY OAS Regime Thresholds

| HY OAS | Regime | Signal |
|--------|--------|--------|
| < 300 bps | **Complacent** | Reduce HY, low compensation |
| 300-400 bps | Normal | Market weight |
| 400-500 bps | Elevated | Attractive if fundamentals OK |
| 500-700 bps | Stressed | Value if no recession |
| > 700 bps | Crisis | Deep value or capitulation |

### IG OAS Regime Thresholds

| IG OAS | Regime | Signal |
|--------|--------|--------|
| < 80 bps | Tight | Low compensation |
| 80-120 bps | Normal | Market weight |
| 120-180 bps | Attractive | Add exposure |
| > 180 bps | Stressed | Value |

### Credit Spread Historical Context

| Period | HY OAS | Context |
|--------|--------|---------|
| **2007 Peak** | 250 bps | Pre-GFC complacency |
| **2008 Crisis** | 2,000+ bps | Financial crisis |
| **2019 Pre-COVID** | 350 bps | Late cycle |
| **2020 COVID** | 1,100 bps | Pandemic panic |
| **2021-22** | 300-350 bps | Recovery |
| **Dec 2025** | ~320 bps | Current (complacent) |

---

## Credit Quality Considerations

### Rating Migration Risk

| Economic Condition | Migration Risk | Action |
|--------------------|----------------|--------|
| Expansion (GCI > 0) | Low, upgrades > downgrades | Own BBB, BB |
| Late cycle (LFI > 0.5) | Rising, watch BBBs | Reduce BBB, up in quality |
| Recession | High, fallen angels | Avoid BBB, own A+ |

### BBB "Cliff" Risk

BBB-rated bonds are ~50% of IG index. If downgraded to HY ("fallen angels"):
- Forced selling by IG-only mandates
- HY index must absorb supply
- Spread contagion

Watch BBB spreads vs. A spreads for early warning.

---

## Duration vs. Spread Decomposition

Credit returns = Rate return + Spread return

### When to Own Credit Duration (LQD, EMB)

| Rate Direction | Spread Direction | Credit Return |
|----------------|------------------|---------------|
| Rates falling | Spreads tightening | **Excellent** |
| Rates falling | Spreads widening | Mixed (rate wins) |
| Rates rising | Spreads tightening | Mixed (spread wins) |
| Rates rising | Spreads widening | **Terrible** |

### Short Duration Credit (VCSH, SHYG)

When:
- PCI > +0.5 (Fed constrained, rates risk)
- Spreads attractive but rate risk elevated
- Prefer spread exposure without duration

### Floating Rate (BKLN, SRLN)

When:
- Rates rising (Fed hiking)
- Want credit exposure without rate risk
- Accept lower credit quality (mostly BB/B)

---

## Position Sizing

### Credit Allocation by MRI Regime

| MRI Range | Total Credit | IG | HY | EM |
|-----------|--------------|----|----|-----|
| < -0.5 | 15-20% | 10-12% | 5-8% | 2-3% |
| -0.5 to +0.5 | 12-18% | 8-12% | 4-6% | 1-2% |
| +0.5 to +1.0 | 8-15% | 8-12% | 0-3% | 0-1% |
| +1.0 to +1.5 | 5-10% | 5-10% | 0% | 0% |
| > +1.5 | 0-5% | 0-5% | 0% | 0% |

### HY Sizing Rules

- **Never > 10%** of portfolio in HY
- **Exit entirely** when CLG < -1.0
- **Reduce by half** when LCI < -0.5
- **Full allocation** only when CLG > 0 AND LCI > 0

---

## Default Cycle Framework

### Leading Indicators of Defaults

| Indicator | Lead Time | Signal |
|-----------|-----------|--------|
| **HY Spreads** | 6-9 months | Spreads > 500 bps |
| **Loan Officer Survey** | 6-12 months | Tightening standards |
| **LFI** | 3-6 months | Labor fragility precedes credit stress |
| **Distressed Ratio** | 3-6 months | % of HY trading > 1000 bps OAS |

### Default Rate Expectations

| HY OAS | Implied Default Rate |
|--------|---------------------|
| 300 bps | ~2% (historical avg) |
| 500 bps | ~4% |
| 700 bps | ~6% |
| 1000 bps | ~10%+ |

---

## Current Assessment Template

| Metric | Reading | Signal |
|--------|---------|--------|
| **HY OAS** | | Spread level |
| **IG OAS** | | IG spreads |
| **CLG** | | Credit-Labor Gap |
| **LCI** | | Liquidity regime |
| **FCI** | | Financial conditions |
| **HY Distressed %** | | Stress indicator |

*Update dynamically with current readings.*

---

*Bob Sheehan, CFA, CMT*
*Founder & CIO, Lighthouse Macro*
