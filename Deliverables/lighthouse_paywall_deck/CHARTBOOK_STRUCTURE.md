# LIGHTHOUSE MACRO - ULTIMATE CHARTBOOK STRUCTURE

## Total: 50 Charts + 6 Section Overviews = 56 Pages

---

## SECTION 1: LIQUIDITY & FUNDING STRESS (Charts 1-10)

### Section Overview Page (Full Page Text)

**Framework: The Liquidity Foundation**

The plumbing matters more than the narrative. While markets obsess over Fed meetings and inflation prints, the real story plays out in overnight repo markets, the RRP facility, and bank reserve levels. This section tracks the system's shock-absorption capacity—the cushion that determines whether volatility spikes get contained or cascade into crisis.

**Key Indicators:**
1. **Liquidity Cushion Index (LCI)** - Are reserves + RRP sufficient to absorb stress?
2. **Yield-Funding Stress (YFS)** - Is the plumbing cracking?
3. **Repo Rate Dispersion** - Are some participants getting locked out?

**The Transmission Mechanism:**
- High LCI + Low YFS = Ample liquidity, markets can absorb shocks
- Low LCI + Rising YFS = Vulnerable system, small shocks → big moves
- Repo dispersion widening = Funding fragmentation, crisis precursor

**What to Watch:**
- RRP drawdown below $500B (critical threshold)
- BGCR-EFFR spread > +15 bps (funding stress)
- Repo dispersion 99th-1st percentile > 50 bps (fragmentation)

**Current Regime:** [Dynamic - populated from latest data]

**Takeaway:** The 2008 crisis taught us: liquidity is binary. You have it until you don't. These charts track the transition.

---

### Chart 1: Liquidity Cushion Index (LCI)
- **Data:** ON RRP/GDP + Bank Reserves/GDP (z-scored)
- **Methodology:** Composite average, threshold bands at ±1σ, ±2σ
- **Source:** NY Fed, FRED

### Chart 2: Yield-Funding Stress (YFS) Composite
- **Data:** 10Y-2Y spread, 10Y-3M spread, BGCR-EFFR spread, SOFR-EFFR spread
- **Methodology:** Z-score composite, weighted by volatility
- **Source:** NY Fed, FRED

### Chart 3: Repo Rate Dispersion Index
- **Data:** BGCR 99th percentile - 1st percentile vs Tri-party repo volume
- **Methodology:** Rolling 30-day dispersion, volume overlay
- **Source:** NY Fed

### Chart 4: Fed Balance Sheet + RRP Overlay
- **Data:** Fed total assets, ON RRP usage, Bank reserves
- **Methodology:** Stacked area chart showing composition
- **Source:** NY Fed, FRED (H.4.1 report)

### Chart 5: SOFR-EFFR-OBFR Dynamics
- **Data:** SOFR, EFFR, OBFR (3 money market rates)
- **Methodology:** Spread overlay (SOFR-EFFR, OBFR-EFFR)
- **Source:** NY Fed Markets API

### Chart 6: Money Market Dashboard (4-Panel)
- **Panel A:** SOFR term structure (overnight, 1M, 3M, 6M)
- **Panel B:** EFFR vs Fed target range
- **Panel C:** RRP usage trend
- **Panel D:** Bank reserves trend
- **Source:** NY Fed

### Chart 7: Treasury Liquidity Metrics
- **Data:** Bid-ask spreads, market depth, primary dealer positions
- **Methodology:** Composite liquidity score
- **Source:** FRED, FINRA TRACE

### Chart 8: Swap Spreads (2Y, 5Y, 10Y, 30Y)
- **Data:** Swap rate - Treasury yield for each maturity
- **Methodology:** Multi-line overlay with zero line
- **Source:** Bloomberg (fallback: FRED proxies)

### Chart 9: Cross-Currency Basis (EUR/USD, JPY/USD)
- **Data:** 3-month FX basis swaps
- **Methodology:** Dual-axis, EUR/USD (primary), JPY/USD (secondary)
- **Source:** Bloomberg, BIS

### Chart 10: Dealer Positioning - Treasury Net Holdings
- **Data:** Primary dealer net positions (Bills, Notes, Bonds)
- **Methodology:** Stacked bar by maturity bucket, zero line
- **Source:** NY Fed (weekly FR 2004 survey)

---

## SECTION 2: LABOR MARKET DYNAMICS (Charts 11-17)

### Section Overview Page (Full Page Text)

**Framework: Labor as Leading Indicator**

The unemployment rate is a lagging indicator. By the time it spikes, the recession is already here. We focus on flow variables—quits, hires, hours worked—that deteriorate 6-12 months before headline payrolls turn negative.

**Key Indicators:**
1. **Labor Fragility Index (LFI)** - How hard is it to find a job once unemployed?
2. **Labor Dynamism Index (LDI)** - Are workers confident enough to quit and upgrade?
3. **Hours vs Employment Divergence** - Are firms cutting hours before headcount?

**The Sequence of Deterioration:**
1. **Quits decline** (workers stop job-hopping) ← We are here
2. **Hours cut** (reduce overtime, shift to part-time)
3. **Temp workers laid off** (easiest to cut)
4. **Hiring freezes** (stop backfilling attrition)
5. **Permanent layoffs** (unemployment rate rises)

**What to Watch:**
- Quits rate < 2.0% (vs 3.0% peak) = Late cycle
- Hours YoY < Employment YoY = Layoffs coming
- LFI rising while unemployment stable = Hidden deterioration

**Current Regime:** [Dynamic]

**Takeaway:** "Payrolls can stay positive while quits slide—that's a late-cycle tell." Don't wait for unemployment to spike.

---

### Chart 11: Labor Fragility Index (LFI)
- **Data:** Long-duration unemployment share, quits rate (inverted), hires/quits (inverted)
- **Methodology:** Z-score composite, threshold bands
- **Source:** FRED (JOLTS, CPS)

### Chart 12: Labor Dynamism Index (LDI)
- **Data:** Quits rate, hires/quits ratio, quits/layoffs ratio
- **Methodology:** Z-score composite, leads payrolls by 2-3 quarters
- **Source:** FRED (JOLTS)

### Chart 13: Payroll Growth vs Quits Rate Divergence
- **Data:** Headline payroll YoY, quits rate (z-score matched)
- **Methodology:** Dual-axis overlay, divergence shading
- **Source:** FRED

### Chart 14: Hours Worked vs Employment
- **Data:** Total hours YoY vs employment YoY
- **Methodology:** Dual-axis, divergence = leading layoff signal
- **Source:** FRED (CES)

### Chart 15: Labor Market Heatmap (8 Metrics)
- **Metrics:** Unemployment, participation, prime-age employment, quits, hires, layoffs, hours, wage growth
- **Methodology:** Z-score heatmap, color-coded (green/yellow/red)
- **Source:** FRED

### Chart 16: JOLTS Indicators (3-Panel)
- **Panel A:** Job openings
- **Panel B:** Hires vs Separations
- **Panel C:** Quits vs Layoffs
- **Source:** FRED (JOLTS)

### Chart 17: Beveridge Curve
- **Data:** Unemployment rate vs job openings rate
- **Methodology:** Scatter with time color gradient, recent trend line
- **Source:** FRED

---

## SECTION 3: CREDIT MARKETS & RISK APPETITE (Charts 18-25)

### Section Overview Page (Full Page Text)

**Framework: Credit Leads, Equities Follow**

Credit markets price risk. Equity markets price narratives. When the two diverge—spreads widening while stocks rally—credit is usually right. This section tracks not just spread levels, but spread adequacy relative to macro fragility.

**Key Indicators:**
1. **Credit-Labor Gap (CLG)** - Are spreads too tight given labor market stress?
2. **HY Spread vs Volatility Imbalance** - Are spreads compensating for volatility?
3. **Excess Bond Premium (EBP)** - Risk aversion above default risk alone

**The Credit Cycle Stages:**
- **Early Cycle:** Spreads wide, defaults peaking, opportunity emerging
- **Mid Cycle:** Spreads normalizing, credit profitable
- **Late Cycle:** Spreads tight, covenant-lite deals, complacency
- **Crisis:** Spreads blow out >1000 bps, credit markets freeze

**What to Watch:**
- HY OAS < 300 bps = Late cycle, reduce credit
- CLG negative (spreads < labor stress) = Pre-widening setup
- EBP rising = Risk aversion building

**Current Regime:** [Dynamic]

**Takeaway:** "Historically a pre-widening configuration" when CLG goes negative. Don't confuse tight spreads with safety.

---

### Chart 18: High-Yield OAS + BBB-AAA Differential
- **Data:** HY OAS (primary), BBB-AAA spread (secondary)
- **Methodology:** Dual-axis, threshold lines at 300/500/800 bps
- **Source:** FRED (BAML indices)

### Chart 19: Credit Cycle - C&I Loan Growth
- **Data:** Commercial & Industrial loans YoY
- **Methodology:** Single-axis, zero line, recession shading
- **Source:** FRED

### Chart 20: Excess Bond Premium (EBP) vs Fed Funds
- **Data:** Gilchrist-Zakrajšek EBP, Fed Funds rate
- **Methodology:** Dual-axis overlay
- **Source:** FRED

### Chart 21: Corporate Leverage - Debt/GDP
- **Data:** Nonfinancial corporate debt to GDP
- **Methodology:** Single-axis, historical average line
- **Source:** FRED

### Chart 22: Credit Impulse
- **Data:** Change in credit growth (YoY)
- **Methodology:** Single-axis, zero line, shade positive/negative
- **Source:** FRED (total bank credit, GDP)

### Chart 23: Credit-Labor Gap (CLG)
- **Data:** Z(HY OAS) - Z(LFI)
- **Methodology:** Single-axis, zero line critical
- **Source:** FRED, proprietary LFI calculation

### Chart 24: HY Spread vs Volatility Imbalance
- **Data:** HY OAS (z-score), realized HY spread volatility (z-score)
- **Methodology:** Scatter plot or dual-axis
- **Source:** FRED

### Chart 25: Cross-Asset Credit Stress
- **Data:** HY OAS, VIX, Investment Grade OAS
- **Methodology:** 3-line overlay, normalized to z-scores
- **Source:** FRED, CBOE

---

## SECTION 4: EQUITY POSITIONING & MOMENTUM (Charts 26-32)

### Section Overview Page (Full Page Text)

**Framework: Momentum Matters, Until It Doesn't**

Equity markets can stay irrational longer than you can stay solvent. But stretched momentum + macro deterioration = fragile setup. This section tracks not just price levels, but positioning, quality preferences, and shock-absorption capacity.

**Key Indicators:**
1. **Equity Momentum Divergence (EMD)** - How stretched is momentum relative to volatility?
2. **Quality vs Risk (QUAL/SPY)** - Flight to quality or junk rally?
3. **Macro Risk Index (MRI)** - Are equities pricing in macro risk?

**The Late-Cycle Pattern:**
- Equities grind higher (FOMO, passive flows)
- Volatility compressed (low VIX)
- Quality underperforms (junk rally)
- Macro deteriorates (labor, credit weakening)
- **Result:** Thin shock absorption, prone to air pockets

**What to Watch:**
- EMD > +1σ = Stretched momentum, reduce beta
- QUAL/SPY at cycle lows = Maximum risk appetite
- MRI rising + SPX rising = Markets under-pricing risk

**Current Regime:** [Dynamic]

**Takeaway:** "Currently at cycle lows despite macro deterioration; signals late-stage bull market behavior." When everyone's bullish, be careful.

---

### Chart 26: Equity Momentum Divergence (EMD)
- **Data:** SPX distance from 200-day MA / realized volatility
- **Methodology:** Z-score, threshold bands ±1σ
- **Source:** FRED, proprietary calculation

### Chart 27: Quality vs Risk Ratio (QUAL/SPY)
- **Data:** iShares MSCI USA Quality ETF / SPY
- **Methodology:** Price ratio, historical context
- **Source:** Yahoo Finance / TradingView

### Chart 28: Macro Risk Index (MRI)
- **Data:** LFI + (−LDI) + YFS + HY OAS + EMD + (−LCI)
- **Methodology:** Z-score composite, threshold bands
- **Source:** Proprietary composite

### Chart 29: SPX vs Cross-Asset Correlation
- **Data:** SPX, 60-day rolling correlation to TLT (bonds)
- **Methodology:** Dual-axis, correlation on secondary axis
- **Source:** FRED

### Chart 30: VIX Term Structure
- **Data:** VIX, VIX3M, VIX6M (if available, else use VIX only)
- **Methodology:** Multi-line overlay
- **Source:** CBOE, FRED

### Chart 31: Sector Rotation Heatmap
- **Data:** 11 S&P sectors, relative performance (z-score)
- **Methodology:** Heatmap, cyclicals vs defensives
- **Source:** FRED or sector ETFs

### Chart 32: Equity Risk Premium
- **Data:** S&P 500 earnings yield - 10Y Treasury yield
- **Methodology:** Single-axis, historical context
- **Source:** FRED, S&P

---

## SECTION 5: CRYPTO & DIGITAL ASSETS (Charts 33-39)

### Section Overview Page (Full Page Text)

**Framework: Crypto as Macro Barometer**

Bitcoin is no longer an isolated asset. When BTC trades 80%+ correlated with Nasdaq, it's a risk-on/risk-off instrument. Stablecoins represent on-chain liquidity—"dry powder" that precedes rallies. This section tracks crypto-traditional integration and digital dollar competition.

**Key Indicators:**
1. **Stablecoin Supply** - On-chain liquidity, leads BTC price
2. **BTC Correlation to Nasdaq/Gold** - Risk-on or safe haven?
3. **Stablecoin vs MMF** - Digital dollar gaining share?

**The Crypto Liquidity Framework:**
- Rising stablecoin supply = Capital entering, bullish 3-6M
- Falling stablecoin supply = Off-ramping, bearish
- BTC corr to Nasdaq > 0.6 = Risk-on asset
- BTC corr to Gold > 0.5 = Safe haven narrative

**What to Watch:**
- Stablecoin supply growth accelerating = BTC rally ahead
- BTC realized vol converging to equity vol = Maturation
- Stablecoin/MMF ratio rising = Structural shift

**Current Regime:** [Dynamic]

**Takeaway:** Stablecoins backed by Treasuries compete with MMFs for same collateral. Crypto is eating TradFi from the inside.

---

### Chart 33: Bitcoin + Stablecoin Supply Overlay
- **Data:** BTC price (primary), total stablecoin market cap (secondary)
- **Methodology:** Dual-axis
- **Source:** TradingView (COINBASE:BTCUSD), CoinGecko API

### Chart 34: Stablecoin Composition (USDT, USDC, DAI)
- **Data:** Individual stablecoin market caps
- **Methodology:** Stacked area chart
- **Source:** CoinGecko, Glassnode

### Chart 35: Stablecoin vs Money Market Funds
- **Data:** Total stablecoin supply ($B), MMF assets ($T)
- **Methodology:** Dual-axis, growth rates overlay
- **Source:** CoinGecko, FRED (MMMFFAQ027S)

### Chart 36: BTC Realized Volatility vs VIX
- **Data:** BTC 30-day realized vol, VIX
- **Methodology:** Dual-axis overlay
- **Source:** TradingView, FRED

### Chart 37: BTC Correlation to Nasdaq/Gold (90-Day Rolling)
- **Data:** BTC vs NDX correlation, BTC vs Gold correlation
- **Methodology:** Dual-line overlay, zero line
- **Source:** TradingView, proprietary calculation

### Chart 38: On-Chain Activity - Active Addresses
- **Data:** BTC active addresses (7-day MA)
- **Methodology:** Single-axis, trend overlay
- **Source:** Glassnode API or TradingView export

### Chart 39: Crypto Market Cap vs Global M2
- **Data:** Total crypto market cap, global M2 money supply
- **Methodology:** Dual-axis, crypto as % of M2
- **Source:** CoinGecko, BIS/FRED

---

## SECTION 6: AI INFRASTRUCTURE & CAPEX CYCLE (Charts 40-50)

### Section Overview Page (Full Page Text)

**Framework: AI CapEx as Leading GDP Indicator**

The Magnificent 7 are spending $200B+ annually on AI infrastructure. This CapEx cycle drives semiconductor demand, foundry capacity, and IT investment—all of which feed into GDP with a lag. This section tracks the build-out and identifies inflection points.

**Key Indicators:**
1. **Mag 7 CapEx Trends** - Are they still spending or cutting?
2. **Semiconductor Equipment Exports** - Leading indicator of chip production
3. **IT Investment Contribution to GDP** - How much is AI driving growth?

**The CapEx Cycle:**
- **Early Stage:** Hyperscalers announce massive budgets
- **Build-Out:** Equipment orders surge, NVDA/TSM rally
- **Peak CapEx:** Spending plateaus, utilization still low
- **Digestion:** CapEx cuts, equipment names correct
- **Payoff:** Utilization rises, revenue justifies spending

**What to Watch:**
- Mag 7 CapEx growth decelerating = Peak AI spending
- Taiwan semi exports declining = Chip demand rolling over
- IT investment/GDP flattening = CapEx not flowing to GDP yet

**Current Regime:** [Dynamic]

**Takeaway:** Follow the CapEx, not the hype. When spending slows, NVDA is a sell regardless of revenue beats.

---

### Chart 40: Magnificent 7 CapEx Trends
- **Data:** MacroMicro chart image (Apple, MSFT, Google, Amazon, Meta, NVDA, Tesla CapEx)
- **Methodology:** Image overlay with Lighthouse branding
- **Source:** MacroMicro screenshot

### Chart 41: AI Software RPO Growth
- **Data:** MacroMicro chart image (Remaining Performance Obligations for AI software cos)
- **Methodology:** Image overlay
- **Source:** MacroMicro

### Chart 42: Global Semi Equipment vs Taiwan Exports
- **Data:** MacroMicro chart image
- **Methodology:** Image overlay
- **Source:** MacroMicro

### Chart 43: US IT Investment Contribution to Real GDP Growth
- **Data:** MacroMicro chart image
- **Methodology:** Image overlay
- **Source:** MacroMicro

### Chart 44: Semiconductor Capacity Utilization
- **Data:** Global fab utilization rate (%)
- **Methodology:** Single-axis line chart
- **Source:** SEMI, FRED proxy

### Chart 45: AI Token Context Window Growth
- **Data:** GPT-3 → GPT-4 → Claude 3 → GPT-4o context windows
- **Methodology:** Log-scale bar chart showing exponential growth
- **Source:** Public model specs

### Chart 46: Data Center Power Demand Forecast
- **Data:** US data center electricity consumption (actual + forecast)
- **Methodology:** Historical + projection, area chart
- **Source:** EIA, industry reports

### Chart 47: NVDA Technical Analysis (3-Panel TradingView)
- **Panel A:** Price + 50/200 SMA
- **Panel B:** Relative strength vs SMH
- **Panel C:** Robust relative z-score
- **Source:** TradingView screenshot

### Chart 48: MSFT Technical Analysis (3-Panel TradingView)
- **Panel A:** Price + 50/200 SMA
- **Panel B:** Relative strength vs QQQ
- **Panel C:** Robust relative z-score
- **Source:** TradingView screenshot

### Chart 49: TSM Technical Analysis (3-Panel TradingView)
- **Panel A:** Price + 50/200 SMA
- **Panel B:** Relative strength vs SMH
- **Panel C:** Robust relative z-score
- **Source:** TradingView screenshot

### Chart 50: Global AI Infrastructure Investment Map
- **Data:** CapEx by region (US, China, EU, Other)
- **Methodology:** Stacked area or geographic visualization
- **Source:** Industry reports, MacroMicro

---

## CHARTBOOK METADATA

**Cover Page:**
- Title: LIGHTHOUSE MACRO - INSTITUTIONAL CHARTBOOK
- Subtitle: 50 Charts Across Liquidity, Labor, Credit, Equity, Crypto, AI
- Date: [Dynamic]
- Branding: "Macro, Illuminated."

**Table of Contents:**
- Section 1: Liquidity & Funding Stress (Charts 1-10)
- Section 2: Labor Market Dynamics (Charts 11-17)
- Section 3: Credit Markets & Risk Appetite (Charts 18-25)
- Section 4: Equity Positioning & Momentum (Charts 26-32)
- Section 5: Crypto & Digital Assets (Charts 33-39)
- Section 6: AI Infrastructure & CapEx Cycle (Charts 40-50)

**Total Pages:** 56
- Cover: 1
- Table of Contents: 1
- Section Overviews: 6 (full-page text)
- Charts: 50
- Back Page: 1 (contact/subscription info)

**Update Frequency:** Weekly (Fridays)

**Data Sources:**
- Federal Reserve Economic Data (FRED)
- NY Fed Markets API
- Office of Financial Research (OFR)
- TradingView (crypto, equities)
- MacroMicro (AI infrastructure)
- Proprietary calculations (LCI, YFS, LFI, LDI, CLG, EMD, MRI)
