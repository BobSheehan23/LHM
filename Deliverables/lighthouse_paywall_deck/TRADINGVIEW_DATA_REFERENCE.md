# TradingView Data Reference - Lighthouse Macro

## Data Available via TradingView (vs FRED gaps)

### Market Volatility Indicators
- **MOVE Index** (`CBOE:MOVE`) - Bond market volatility (NOT in FRED)
  - Use for: Chart 38 Repo Market Depth alternative
  - Proxy for Treasury market stress
- **VIX** (`CBOE:VIX`) - Equity volatility
- **VVIX** (`CBOE:VVIX`) - Vol of vol
- **SKEW** (`CBOE:SKEW`) - Tail risk indicator

### Credit & Rates
- **CDX IG/HY Indices** - Credit default swaps
  - More real-time than FRED HY spreads
- **SOFR Futures** (`CME:SR1!`, `SR3!`) - Forward rate expectations
- **FRA-OIS Spreads** - Better than FRED for real-time stress
- **Cross-Currency Basis** (EUR/USD, JPY/USD basis swaps)
  - NOT available in FRED at all

### Crypto Market Data (Charts 28-32 improvements)
- **Bitcoin** (`COINBASE:BTCUSD`, `BITSTAMP:BTCUSD`)
- **Ethereum** (`COINBASE:ETHUSD`)
- **Stablecoins:**
  - USDT: `BINANCE:USDTUSD`
  - USDC: `COINBASE:USDCUSD`
  - DAI: `COINBASE:DAIUSD`
- **On-chain metrics:**
  - Bitcoin hash rate
  - Exchange inflows/outflows
  - Stablecoin supply (better than any free API)

### Commodity & FX
- **DXY** (`TVC:DXY`) - Dollar index
- **Gold** (`OANDA:XAUUSD`, `TVC:GOLD`)
- **Oil** (`NYMEX:CL1!`, `TVC:USOIL`)
- **Copper** (`COMEX:HG1!`) - Global growth proxy

### Futures Positioning (CFTC COT data)
- **Speculator Positioning:**
  - S&P 500 futures
  - Treasury futures (2Y, 10Y, 30Y)
  - VIX futures
- Better formatted than pulling from CFTC directly

### International Rates & Bonds
- **JGB Yields** (`TVC:JP10Y`, `JP02Y`)
- **Bund Yields** (`TVC:DE10Y`)
- **Gilt Yields** (`TVC:GB10Y`)
- **China Rates** (`TVC:CN10Y`)
- Use for: Cross-country yield comparison charts

### Equity Factor Indices
- **Equal-Weight S&P** (`SP:SPW`) vs cap-weighted
- **Value vs Growth** (`IVE` vs `IVW`)
- **Small Cap vs Large Cap** (Russell spread analysis)

### ETF Flows & Positioning
- **HYG, LQD** - Corporate credit ETFs (already using)
- **TLT, IEF, SHY** - Treasury ETF flows
- **GLD, SLV** - Commodity positioning
- **XLF, XLE, XLK** - Sector rotation

### Alternative Data via TradingView
- **Shipping Rates** (Baltic Dry Index)
- **Lumber Futures** - Housing/inflation proxy
- **Nat Gas** - Energy market stress

---

## Immediate Upgrades for Chartbook

### Chart 38: Add MOVE Index from TradingView
**Current:** Using HY yield as bond vol proxy
**Better:** Pull actual `CBOE:MOVE` via TradingView export or API

### Charts 28-32: Crypto Layer (Currently Placeholders)
Replace with:
1. **Chart 28:** Bitcoin + Stablecoin supply overlay
2. **Chart 29:** USDT/USDC flows and composition
3. **Chart 30:** Stablecoin market cap vs MMF assets
4. **Chart 31:** Crypto volatility (BTC realized vol vs VIX)
5. **Chart 32:** BTC correlation to Nasdaq/Gold

### Chart 34: Swap Spreads
**Current:** Using problematic FRED tickers
**Better:** TradingView swap spread data or calculate from futures

### Chart 37: Cross-Currency Basis
**Current:** Using FX volatility as proxy
**Better:** Actual EUR/USD, JPY/USD basis swap data from TradingView

---

## TradingView API Integration (Future)

### Option 1: Screenshot Automation (Current)
- Manual export from TradingView charts
- 3-panel setup with custom indicators
- **Pros:** Full customization, robust relative z-score
- **Cons:** Manual process, not automated

### Option 2: TradingView Data API
- Requires paid plan ($60-300/mo depending on tier)
- Access via `tradingview-ta` Python library
- **Pros:** Automated daily updates, real-time data
- **Cons:** Cost, API rate limits

### Option 3: Hybrid Approach (Recommended)
- Use TradingView **webhooks** to export specific indicators
- Store in local DB (SQLite or Postgres)
- Auto-generate charts using stored data
- **Pros:** Best of both worlds
- **Cons:** Setup complexity

---

## Data Sources Summary

| Category | FRED | NY Fed | OFR | TradingView | Best Source |
|----------|------|---------|-----|-------------|-------------|
| Core Macro | ✓ | - | - | - | **FRED** |
| Money Markets | Partial | ✓ | ✓ | ✓ | **NY Fed** |
| Credit Spreads | ✓ | - | - | ✓ | **FRED** (daily), **TV** (intraday) |
| Volatility | VIX only | - | - | ✓ | **TradingView** |
| Crypto | BTC only | - | - | ✓ | **TradingView** |
| FX/Commodities | Limited | - | - | ✓ | **TradingView** |
| Cross-Currency Basis | ✗ | ✗ | ✗ | ✓ | **TradingView** |
| Single Names | ✗ | ✗ | ✗ | ✓ | **TradingView** |

---

## Next Steps

1. **Short-term:** Export MOVE index from TradingView for Chart 38
2. **Medium-term:** Build out crypto layer (Charts 28-32) with TradingView data
3. **Long-term:** Set up TradingView API integration for daily auto-updates

---

## TradingView Chart Specifications (Current 3-Panel Setup)

**Panel 1: Price Action**
- Candlesticks
- 50 SMA (blue)
- 200 SMA (red)

**Panel 2: Relative Strength**
- (Stock / Benchmark) ratio
- Trend zones: Green (up), Black (neutral), Red (down)

**Panel 3: Robust Relative Z-Score**
- 63d ROC (stock) - 63d ROC (benchmark)
- Z-score using Median/MAD (252d lookback)
- Horizontal lines: +2, 0, -2

**Benchmarks Used:**
- NVDA, ASML, TSM → SMH
- MSFT → QQQ
- JPM, GS → XLF
- COIN, MSTR, MARA → BTC or R3K
- HYG → LQD

This setup provides:
- **Trend confirmation** (50/200 MA)
- **Relative performance** (vs sector/market)
- **Statistical extremes** (entry/exit timing)
