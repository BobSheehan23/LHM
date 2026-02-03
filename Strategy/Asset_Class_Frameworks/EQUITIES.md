# Asset Class Framework: Equities

## Primary ETF Universe

### Broad Market
| Ticker | Name | Expense | Use Case |
|--------|------|---------|----------|
| **SPY** | SPDR S&P 500 | 0.09% | Core US large cap |
| **QQQ** | Invesco Nasdaq 100 | 0.20% | Tech/growth tilt |
| **IWM** | iShares Russell 2000 | 0.19% | Small cap |
| **VTI** | Vanguard Total Stock | 0.03% | Total US market |

### Sector ETFs (Select Sector SPDRs)
| Ticker | Sector | Cyclicality | Pillar Links |
|--------|--------|-------------|--------------|
| **XLK** | Technology | High | Structure, Sentiment |
| **XLF** | Financials | High | Plumbing, Credit |
| **XLY** | Consumer Discretionary | High | Consumer, Labor |
| **XLI** | Industrials | High | Business, Growth |
| **XLE** | Energy | Commodity-linked | Trade, Prices |
| **XLV** | Healthcare | Defensive | Consumer |
| **XLP** | Consumer Staples | Defensive | Consumer |
| **XLU** | Utilities | Defensive/Rate-sensitive | Rates |
| **XLRE** | Real Estate | Rate-sensitive | Housing, Plumbing |
| **XLB** | Materials | Cyclical | Growth, Trade |
| **XLC** | Communication Services | Mixed | Structure |

### International
| Ticker | Name | Use Case |
|--------|------|----------|
| **EFA** | iShares MSCI EAFE | Developed ex-US |
| **EEM** | iShares MSCI Emerging | Emerging markets |
| **FXI** | iShares China Large Cap | China exposure |

---

## Pillar-to-Equity Translation

### MRI Regime → Equity Allocation

| MRI Range | Regime | Equity Allocation | Sector Tilt |
|-----------|--------|-------------------|-------------|
| < -0.5 | Low Risk | 65-70% | Cyclicals (XLY, XLF, XLI) |
| -0.5 to +0.5 | Neutral | 55-60% | Balanced |
| +0.5 to +1.0 | Elevated | 45-55% | Reduce cyclicals |
| +1.0 to +1.5 | High Risk | 35-45% | Defensives (XLV, XLP, XLU) |
| > +1.5 | Crisis | 25-35% | Max defensive, cash |

### Key Pillar Signals

**Labor (LPI, LFI):**
- LPI < -0.5 → Underweight cyclicals, especially XLY (consumer discretionary)
- LFI > +1.0 → Pre-recessionary, rotate to defensives

**Prices (PCI):**
- PCI > +0.5 → Fed constrained, duration-sensitive sectors (XLU, XLRE) underperform
- PCI < 0 → Growth/duration outperforms (XLK, QQQ)

**Plumbing (LCI):**
- LCI < -0.5 → Liquidity scarce, reduce beta exposure
- LCI > +0.5 → Liquidity abundant, risk-on

**Structure (MSI) + Sentiment (SPI):**
- MSI < -1.0 → Structure broken, reduce exposure
- SPI > +1.5 → Extreme fear, contrarian buy signal
- SBD > +1.0 → Distribution (generals without soldiers), reduce

---

## Position Sizing

### Conviction Tiers (from Master Strategy)

| Tier | Score | Max Position | Example |
|------|-------|--------------|---------|
| Tier 1 | 16-19 pts | 20% | Perfect setup  |
| Tier 2 | 12-15 pts | 12% | Strong setup |
| Tier 3 | 8-11 pts | 7% | Moderate conviction |
| Tier 4 | <8 pts | 0% | Avoid |

### Regime Multiplier

Position Size = Base Weight × Regime Multiplier × Liquidity Adjustment

| MRI | Multiplier |
|-----|------------|
| < -0.5 | 1.2x |
| -0.5 to +0.5 | 1.0x |
| +0.5 to +1.0 | 0.6x |
| +1.0 to +1.5 | 0.3x |
| > +1.5 | 0.0x |

---

## Absolute Rules (from Trading Strategy)

1. **Below 200d MA** → Conditional (mature downtrend allows tactical)
2. **Death Cross** → Conditional (>60 days allows tactical)
3. **Red Relative Strength** → **Unconditional - never override**
4. **Z-RoC < -1.0** → Exit trigger
5. **>15% above 50d MA** → **Unconditional - never chase**

---

## Current Assessment Template

| Metric | Reading | Signal |
|--------|---------|--------|
| **SPX vs 200d** | | Above/Below trend |
| **SPX vs 50d** | | Short-term momentum |
| **% > 50d MA** | | Breadth |
| **MRI** | | Regime |
| **MSI** | | Structure |
| **SPI** | | Sentiment |

*Update dynamically with current readings.*

---

*Bob Sheehan, CFA, CMT*
*Founder & CIO, Lighthouse Macro*
