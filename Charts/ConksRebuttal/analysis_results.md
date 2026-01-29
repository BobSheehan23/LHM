# Liquidity Analysis Results
## Lighthouse Macro - Liquidity Research

---

## LCI Database Version (Original Strong Results)

**Source:** `lighthouse_indices` table, `index_id = 'LCI'`
**Methodology:** Contemporaneous returns (past 21-day return when LCI at given level)
**Sample:** 6,529 observations (2000-2026)

### Quintile Analysis (SPX)

| Quintile | Avg 1-Month Return | n |
|----------|-------------------|---|
| Q1 (Scarce) | -0.57% | 1,306 |
| Q2 | +0.51% | 1,306 |
| Q3 | +0.74% | 1,305 |
| Q4 | +0.68% | 1,306 |
| Q5 (Ample) | +1.76% | 1,306 |

**Q5-Q1 Spread: +2.33% (t=13.66, p<0.0001)**

### Decile Analysis (SPX)

| Decile | Avg 1-Month Return | n |
|--------|-------------------|---|
| D1 (Bottom 10%) | -1.71% | 653 |
| D10 (Top 10%) | +1.49% | 653 |

**D10-D1 Spread: +3.21% (t=13.35, p<0.0001)**

### Interpretation

This shows **contemporaneous correlation**: when LCI is ample, returns are good. When LCI is scarce, returns are poor. Liquidity and returns move together.

This is NOT a predictive model (current LCI predicting future returns). It demonstrates that liquidity conditions and market performance are related, refuting claims of "ZERO impact."

---

## LCI Calculated Versions (Forward Return Analysis)

These versions test whether LCI **predicts** future returns (forward 21-day).

### Version Comparison (SPX, Decile Spreads)

| Version | Description | Spread | p-value | Effective? |
|---------|-------------|--------|---------|------------|
| V1 | Mixed (Fed + NFCI) | -0.22% | 0.27 | No |
| V2 | NFCI-focused (50% NFCI) | +0.68% | 0.002 | Yes |
| V3 | Pure Fed Plumbing | +0.00% | 0.98 | No |

**Key Finding:** Pure Fed liquidity levels (reserves, RRP) alone do NOT predict equity returns. Financial conditions (NFCI) provide the predictive signal.

---

### Within-Equity Factor Analysis (V2)

**Sorted by Liquidity Sensitivity:**

| Asset | Bottom 10% | Top 10% | Spread | Significant |
|-------|------------|---------|--------|-------------|
| Financials (XLF) | -0.56% | +0.64% | +1.20% | *** |
| Small Cap (IWM) | +0.09% | +1.06% | +0.97% | ** |
| Value (IWD) | -0.07% | +0.69% | +0.76% | ** |
| S&P 500 (SPY) | +0.26% | +0.86% | +0.59% | * |
| Nasdaq 100 (QQQ) | +0.61% | +1.11% | +0.50% | - |
| Growth (IWF) | +0.55% | +1.06% | +0.50% | - |
| Tech (XLK) | +0.53% | +0.92% | +0.39% | - |
| Utilities (XLU) | +0.42% | +0.44% | +0.02% | - |

**Insights:**
- Financials most sensitive (direct Fed exposure)
- Small Caps highly sensitive (leverage, less liquid)
- Value more sensitive than Growth
- Utilities insensitive (defensive, rate-driven not liquidity-driven)

---

### Crypto Analysis (V2)

| Asset | Bottom 10% | Top 10% | Spread | p-value |
|-------|------------|---------|--------|---------|
| BTC | -2.91% | +4.24% | +7.15% | <0.0001 |

Crypto shows much higher liquidity sensitivity than equities.

---

### Research Agenda

1. **Asset-specific models:** Different liquidity factors may matter for different assets
2. **Transmission mechanisms:** How does Fed liquidity transmit to asset prices?
3. **Level vs Change:** Level alone doesn't predict, but combined with direction shows marginal signal
4. **Factor rotation:** Can liquidity predict when Value vs Growth outperforms?

---

### Version Definitions

**V1 - Original Mixed Model**
- Reserves/GDP: 25%
- RRP/GDP: 25%
- EFFR-IORB: 20%
- SOFR-EFFR: 15%
- TGA: 15%
- NFCI: 15%

**V2 - Financial Conditions Focused**
- NFCI: 50%
- Funding spreads: 25%
- TGA: 15%
- Reserves: 10%

**V3 - Pure Fed Plumbing**
- Reserves/GDP: 30%
- RRP/GDP: 25%
- Funding spreads: 25%
- TGA: 20%
