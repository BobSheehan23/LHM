# LHM Momentum Z (21d ROC) - Pine Script v6

Copy the code block below and paste into TradingView Pine Editor:

```
//@version=6
indicator("LHM — Momentum Z (21d ROC)", "LHM Z-ROC", overlay=false, timeframe="D", timeframe_gaps=true)

// ---- INPUTS ----
lenROC = input.int(21, title="ROC length")
lookback = input.int(252, title="Z lookback", minval=10)
smoothZ = input.int(5, title="Smooth Z (EMA)", minval=0, maxval=100)
robustZ = input.bool(true, title="Use robust Z (median/MAD)?")
capZ = input.float(3.0, title="Cap Z at ±", minval=0.0, maxval=10.0, step=0.5)

// Relative mode
useRelative = input.bool(false, title="Use RELATIVE (close / benchmark)?")
benchSym = input.symbol("CRYPTOCAP:TOTAL", title="Benchmark for relative")

// Colors
Dusk = color.new(#FF6723, 0)
Sky = color.new(#2389db, 0)
Gray = color.new(#444444, 0)

// ---- SOURCE ----
f_src(sym) => request.security(sym, timeframe.period, close)
rel = close / f_src(benchSym)
src = useRelative ? rel : close

// ---- ROC ----
roc = ta.roc(src, lenROC)

// ---- Z-SCORE CALCULATION ----
// Classic Z: mean/std
mean_ = ta.sma(roc, lookback)
stdev = ta.stdev(roc, lookback)
z_std = stdev == 0.0 ? 0.0 : (roc - mean_) / stdev

// Robust Z: median & MAD
median_ = ta.percentile_linear_interpolation(roc, lookback, 50)
mad = ta.percentile_linear_interpolation(math.abs(roc - median_), lookback, 50)
z_robust = mad == 0.0 ? 0.0 : (roc - median_) / (mad * 1.4826)

// Select method
z_raw = robustZ ? z_robust : z_std

// ---- WINSORIZE ----
z_capped = math.max(-capZ, math.min(capZ, z_raw))

// ---- SMOOTH ----
zFinal = smoothZ > 0 ? ta.ema(z_capped, smoothZ) : z_capped

// ---- PLOT ----
plot(zFinal, title="Z of ROC", color=Dusk, linewidth=3)
hline(0, title="Zero", color=Gray, linestyle=hline.style_dotted, linewidth=1)
hline(2.0, title="+2σ", color=Sky, linestyle=hline.style_solid, linewidth=2)
hline(-2.0, title="-2σ", color=Sky, linestyle=hline.style_solid, linewidth=2)

// ---- BACKGROUND ZONES ----
bgcolor(zFinal > 2.0 ? color.new(Dusk, 85) : na)
bgcolor(zFinal < -2.0 ? color.new(Sky, 85) : na)
```
