# Asset Class Framework: Currencies

## Primary ETF Universe

### Dollar Index
| Ticker | Name | Expense | Use Case |
|--------|------|---------|----------|
| **UUP** | Invesco DB US Dollar Bullish | 0.75% | Long USD |
| **UDN** | Invesco DB US Dollar Bearish | 0.75% | Short USD |

### Major Currencies
| Ticker | Name | Expense | Currency |
|--------|------|---------|----------|
| **FXE** | Invesco CurrencyShares Euro | 0.40% | EUR/USD |
| **FXY** | Invesco CurrencyShares Yen | 0.40% | USD/JPY inverse |
| **FXB** | Invesco CurrencyShares Pound | 0.40% | GBP/USD |
| **FXC** | Invesco CurrencyShares CAD | 0.40% | CAD/USD |
| **FXA** | Invesco CurrencyShares AUD | 0.40% | AUD/USD |
| **FXF** | Invesco CurrencyShares CHF | 0.40% | CHF/USD |

### EM Currencies
| Ticker | Name | Expense | Use Case |
|--------|------|---------|----------|
| **CEW** | WisdomTree EM Currency | 0.55% | Broad EM FX |

---

## Pillar-to-Currency Translation

### Dollar Framework (DXY)

The dollar is driven by:
1. **Relative Growth**: US vs. RoW growth differential
2. **Relative Rates**: US vs. RoW rate differential
3. **Risk Appetite**: Dollar strengthens in risk-off
4. **Capital Flows**: Safe haven demand

### Growth Differential → Dollar

| US GCI vs RoW | Dollar Direction |
|---------------|------------------|
| US outperforming | Dollar bullish |
| US underperforming | Dollar bearish |
| Global recession | Dollar bullish (safe haven) |
| Global expansion | Dollar bearish (risk-on) |

### Rate Differential → Dollar

| US Rates vs RoW | Dollar Direction |
|-----------------|------------------|
| US rates higher, widening | Dollar bullish |
| US rates higher, narrowing | Dollar bearish |
| US rates lower | Dollar bearish |

### Risk Regime → Dollar

| MRI Range | Dollar Behavior |
|-----------|-----------------|
| < +0.5 | Risk-on, dollar pressure |
| +0.5 to +1.0 | Mixed |
| +1.0 to +1.5 | Flight to quality, dollar bid |
| > +1.5 | Crisis, strong dollar |

---

## Dollar Impact on Other Assets

### Dollar → Commodities (Inverse)

| DXY Move | Commodity Impact | Trade |
|----------|------------------|-------|
| DXY +10% | Commodities -5 to -10% | Underweight DBC, GLD |
| DXY -10% | Commodities +5 to +10% | Overweight DBC, GLD |

### Dollar → EM (Inverse)

| DXY Move | EM Impact | Trade |
|----------|-----------|-------|
| DXY rising | EM stress, capital outflows | Underweight EEM |
| DXY falling | EM relief, inflows | Overweight EEM |

### Dollar → US Multinationals

| DXY Move | S&P 500 EPS Impact |
|----------|-------------------|
| DXY +10% | -2 to -3% EPS headwind |
| DXY -10% | +2 to +3% EPS tailwind |

---

## Yen as Risk Indicator

The Japanese yen (JPY) often serves as a risk barometer due to carry trade dynamics.

### Yen Behavior

| Environment | Yen Direction | Mechanism |
|-------------|---------------|-----------|
| Risk-on | Yen weakens | Carry trades funded in JPY |
| Risk-off | Yen strengthens | Carry trade unwinds |
| BOJ tightening | Yen strengthens | Rate differential narrows |

### USD/JPY Levels

| USD/JPY | Signal |
|---------|--------|
| > 150 | Extreme yen weakness, intervention risk |
| 140-150 | Weak yen |
| 130-140 | Neutral |
| < 130 | Yen strength, risk-off |

---

## Euro Framework

### EUR/USD Drivers

1. **ECB vs Fed Policy**: Rate differential
2. **European Growth**: Relative economic performance
3. **Energy Prices**: Europe energy-import dependent
4. **Political Risk**: EU fragmentation concerns

### EUR/USD Levels

| EUR/USD | Signal |
|---------|--------|
| > 1.15 | Strong euro, dollar weakness |
| 1.05-1.15 | Normal range |
| < 1.05 | Weak euro, dollar strength |
| Parity | Crisis level |

---

## Currency Positioning by Regime

### MRI-Based Currency Allocation

| MRI Range | Dollar Stance | Trade |
|-----------|---------------|-------|
| < +0.5 | Underweight | UDN, FXE, CEW |
| +0.5 to +1.0 | Neutral | No active position |
| +1.0 to +1.5 | Overweight | UUP |
| > +1.5 | Strong overweight | UUP, FXY short |

### Inflation Regime → Currency

| PCI Range | Currency Impact |
|-----------|-----------------|
| > +1.0 | Fed hawkish → Dollar bullish |
| -0.5 to +1.0 | Mixed |
| < -0.5 | Fed dovish → Dollar bearish |

---

## Carry Trade Framework

### High-Yield vs Low-Yield Currencies

**Funding Currencies** (low rates): JPY, CHF, EUR
**Carry Currencies** (high rates): AUD, NZD, EM

### Carry Trade Regime

| Environment | Carry Strategy |
|-------------|----------------|
| Low VIX, stable growth | Long carry (CEW, FXA) |
| Rising VIX, slowing growth | Unwind carry, long JPY |
| Crisis | Max long JPY, CHF |

---

## Position Sizing

Currency positions are typically small due to:
- Low absolute returns vs. equities
- High volatility relative to returns
- Correlation to other risk positions

### Suggested Allocation

| Position Type | Max Allocation |
|---------------|----------------|
| Dollar hedge (UUP/UDN) | 5-10% |
| Single currency (FXE, FXY) | 3-5% |
| EM currency (CEW) | 2-5% |

---

## Current Assessment Template

| Metric | Reading | Signal |
|--------|---------|--------|
| **DXY** | | Dollar level |
| **EUR/USD** | | Euro |
| **USD/JPY** | | Risk gauge |
| **US 10Y - Bund 10Y** | | Rate differential |
| **VIX** | | Risk appetite |
| **MRI** | | Macro regime |

*Update dynamically with current readings.*

---

*Bob Sheehan, CFA, CMT*
*Founder & CIO, Lighthouse Macro*
