"""
Lighthouse Macro — Chart Generator (clean, styled)
- Dual-axis (right primary), legend (white box), dynamic source footer
- Recession shading clamped to current x-range
- Auto-left x-limit trims to first real datapoint
- Saves to ./charts
Requires: numpy, pandas, matplotlib, pandas_datareader
"""
import os, datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas_datareader import data as pdr

# --- Output ---
FIG_DIR = os.path.join(os.path.dirname(__file__), "charts")
os.makedirs(FIG_DIR, exist_ok=True)

# --- Palette ---
OCEAN_BLUE    = '#005F9E'
SUNSET_ORANGE = '#FF6B35'
CAROLINA_BLUE = '#1DAEFF'
MAGENTA       = '#FF4FB3'
LIGHT_GRAY    = '#B0B0B0'
MID_GRAY      = '#7A7A7A'
BLACK         = '#000000'

# --- Style ---
plt.style.use('default')
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": MID_GRAY,
    "axes.labelcolor": BLACK,
    "xtick.color": MID_GRAY,
    "ytick.color": MID_GRAY,
    "axes.grid": False,
    "legend.frameon": True,
    "legend.facecolor": "white",
    "legend.edgecolor": "none",
    "legend.loc": "upper left",
    "lines.linewidth": 2.0,
    "savefig.facecolor": "white",
    "savefig.bbox": "tight",
    "figure.dpi": 160,
})

# --- Source mapping for footer ---
FRED_SOURCES = {
    'CPIAUCSL':'BLS', 'PCEPILFE':'BEA', 'T5YIE':'UST/FRB', 'T10YIE':'UST/FRB', 'T5YIFR':'FRB',
    'FEDFUNDS':'FRB (H.15)', 'DGS2':'UST (H.15)', 'DGS10':'UST (H.15)', 'DFII10':'UST (TIPS)',
    'DTWEXBGS':'FRB', 'DBAA':"Moody’s Analytics",
    'DCOILWTICO':'EIA', 'PCOPPUSDM':'World Bank',
    'RRPONTSYD':'FRBNY', 'SOFR':'FRBNY',
    'TLRESCONS':'U.S. Census Bureau', 'DGORDER':'U.S. Census Bureau',
    'HOUST':'U.S. Census Bureau', 'MORTGAGE30US':'Freddie Mac PMMS',
    'UNRATE':'BLS', 'JTSJOR':'BLS JOLTS', 'PAYEMS':'BLS',
    'INDPRO':'FRB (G.17)', 'NAPM':'ISM',
    'NFCI':'Chicago Fed'
}

def make_source(*codes, extra=None):
    out=[]
    for c in codes:
        tag = FRED_SOURCES.get(c,'FRED')
        if tag not in out: out.append(tag)
    if extra:
        if isinstance(extra,str) and extra not in out: out.append(extra)
        elif isinstance(extra,(list,tuple)):
            for e in extra:
                if e not in out: out.append(e)
    return ", ".join(out) if out else "FRED"

# --- Axes helpers ---
def lhm_axis_right(ax):
    ax.yaxis.tick_right(); ax.yaxis.set_label_position("right")
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_color(MID_GRAY)
    return ax

def lhm_twin(ax):
    ax2 = ax.twinx()
    ax2.yaxis.tick_left(); ax2.yaxis.set_label_position("left")
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color(MID_GRAY)
    return ax2

def auto_left_xlim(ax):
    starts=[]
    for line in ax.get_lines():
        x=line.get_xdata(orig=False); y=line.get_ydata(orig=False)
        if x is None or y is None: continue
        y=np.asarray(y,dtype=float); m=np.isfinite(y)
        if m.any(): starts.append(np.asarray(x)[m][0])
    if starts: ax.set_xlim(left=max(starts))

# --- Last value label ---
def _luma(hex_color):
    hc=hex_color.lstrip('#'); r,g,b=[int(hc[i:i+2],16)/255 for i in (0,2,4)]
    def lin(c): return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
    R,G,B=lin(r),lin(g),lin(b); return 0.2126*R+0.7152*G+0.0722*B

def lastvalue_label(ax, y, color, mode='fill', fmt='{:,.2f}'):
    if y is None or (isinstance(y,float) and (np.isnan(y) or np.isinf(y))): return
    text = '#FFF' if _luma(color)<0.35 else '#111'
    fc, ec = (color,'none') if mode=='fill' else ('#FFF', color)
    txt = text if mode=='fill' else color
    ax.annotate(fmt.format(float(y)), xy=(1,y), xycoords=('axes fraction','data'),
                xytext=(0,0), textcoords='offset points', ha='right', va='center',
                bbox=dict(boxstyle='round,pad=0.25', fc=fc, ec=ec, lw=1, alpha=0.98),
                color=txt, fontsize=9)

# --- Recession shading (clamped) ---
_recessions=None
def get_recessions(start='1950-01-01', end=None):
    global _recessions
    if _recessions is not None: return _recessions
    rec = pdr.DataReader('USREC','fred', start=start, end=end).astype(int)
    shift = rec['USREC'].shift(1, fill_value=0)
    starts = rec.index[(rec['USREC']==1)&(shift==0)]
    ends   = rec.index[(rec['USREC']==0)&(shift==1)]
    if len(ends)<len(starts): ends = ends.append(pd.Index([rec.index[-1]]))
    _recessions = list(zip(starts, ends))
    return _recessions

def shade_recessions(ax, color=LIGHT_GRAY, alpha=0.18):
    x0,x1=ax.get_xlim()
    left=pd.to_datetime(mdates.num2date(x0)); right=pd.to_datetime(mdates.num2date(x1))
    for s,e in get_recessions():
        if e<left or s>right: continue
        s=max(s,left); e=min(e,right)
        ax.axvspan(s,e,color=color,alpha=alpha,zorder=0)

# --- Footer & legend ---
def footer(fig, left_text, right_text="MACRO, ILLUMINATED."):
    fig.subplots_adjust(bottom=0.18)
    fig.text(0.01,0.02,left_text, ha='left', va='bottom', fontsize=8, color=MID_GRAY)
    fig.text(0.99,0.02,right_text, ha='right', va='bottom', fontsize=9, color=MID_GRAY)

def apply_legend(ax):
    handles, labels=[],[]
    for _ax in ax.figure.axes:
        h,l = _ax.get_legend_handles_labels()
        for hi,li in zip(h,l):
            if li and li not in labels:
                handles.append(hi); labels.append(li)
    if labels:
        leg=ax.legend(handles,labels,loc='upper left',frameon=True)
        f=leg.get_frame(); f.set_facecolor('white'); f.set_alpha(1.0); f.set_edgecolor('none')

# --- Save helper (one call per chart) ---
def savefig(ax, fname, sources=None, source_text=None):
    # ensure left twin exists for consistent layout
    if len(ax.figure.axes)==1: _=lhm_twin(ax)
    # trim left limit on all axes
    for _ax in ax.figure.axes:
        try: auto_left_xlim(_ax)
        except: pass
    # now shade, legend, footer
    shade_recessions(ax)
    apply_legend(ax)
    if source_text is None:
        src = make_source(*sources) if sources else "FRED"
        source_text = f"Source: Lighthouse Macro, {src}."
    footer(ax.figure, source_text)
    path=os.path.join(FIG_DIR,fname)
    ax.figure.savefig(path)
    print("Saved:", path)

# --- Data utils ---
def fred_fetch(codes, start='1995-01-01', end=None):
    if isinstance(codes,str): codes=[codes]
    end=end or dt.date.today().isoformat()
    out=pd.DataFrame()
    for c in codes:
        s=pdr.DataReader(c,'fred',start=start,end=end)
        out[c]=s[c]
    return out

def yoy(s, periods=12):  # silent on NA padding
    return s.pct_change(periods, fill_method=None)*100.0

def last_valid(s):
    s=pd.Series(s).dropna()
    return None if s.empty else float(s.iloc[-1])

# 1) CPI vs Fed Funds
def chart_01():
    df = fred_fetch(['CPIAUCSL','FEDFUNDS'], start='1995-01-01')
    cpi = yoy(df['CPIAUCSL']); ffr = df['FEDFUNDS']
    fig, ax = plt.subplots(figsize=(10,4)); lhm_axis_right(ax)
    ax.plot(cpi.index, cpi, color=SUNSET_ORANGE, label='CPI YoY %')
    lastvalue_label(ax, last_valid(cpi), SUNSET_ORANGE, 'fill', '{:.1f}')
    ax2 = lhm_twin(ax)
    ax2.plot(ffr.index, ffr, color=OCEAN_BLUE, label='Fed Funds %')
    lastvalue_label(ax2, last_valid(ffr), OCEAN_BLUE, 'outline', '{:.2f}')
    ax.set_title('Inflation vs Fed Funds')
    savefig(ax, '01_cpi_vs_fedfunds.png', sources=['CPIAUCSL','FEDFUNDS'])

# 2) Breakevens vs CPI
def chart_02():
    df = fred_fetch(['T5YIE','T10YIE','CPIAUCSL'], start='2003-01-01')
    cpi = yoy(df['CPIAUCSL'])
    fig, ax = plt.subplots(figsize=(10,4)); lhm_axis_right(ax)
    ax.plot(df.index, df['T10YIE'], color=OCEAN_BLUE, label='10Y Breakeven %')
    ax.plot(df.index, df['T5YIE'],  color=CAROLINA_BLUE, label='5Y Breakeven %')
    lastvalue_label(ax, last_valid(df['T10YIE']), OCEAN_BLUE, 'fill', '{:.2f}')
    lastvalue_label(ax, last_valid(df['T5YIE']),  CAROLINA_BLUE, 'outline', '{:.2f}')
    ax2 = lhm_twin(ax)
    ax2.plot(cpi.index, cpi, color=SUNSET_ORANGE, label='CPI YoY %')
    lastvalue_label(ax2, last_valid(cpi), SUNSET_ORANGE, 'fill', '{:.1f}')
    ax.set_title('Breakevens vs CPI')
    savefig(ax, '02_breakevens_vs_cpi.png', sources=['T10YIE','T5YIE','CPIAUCSL'])

# 3) 5y5y expectations
def chart_03():
    df = fred_fetch('T5YIFR', start='2003-01-01')
    fig, ax = plt.subplots(figsize=(10,4)); lhm_axis_right(ax)
    ax.plot(df.index, df['T5YIFR'], color=CAROLINA_BLUE, label='5y5y Inflation Expectation')
    lastvalue_label(ax, last_valid(df['T5YIFR']), CAROLINA_BLUE, 'fill', '{:.2f}%')
    ax.set_title('5y5y Forward Inflation Expectation')
    savefig(ax, '03_5y5y.png', sources=['T5YIFR'])

# 4) Yield curve: 10Y, 2Y, 2s10s
def chart_04():
    df = fred_fetch(['DGS10','DGS2'], start='2010-01-01')
    spread = df['DGS10'] - df['DGS2']
    fig, ax = plt.subplots(figsize=(10,4)); lhm_axis_right(ax)
    ax.plot(df.index, df['DGS10'], color=OCEAN_BLUE, label='10Y %')
    ax.plot(df.index, df['DGS2'],  color=MAGENTA,    label='2Y %')
    lastvalue_label(ax, last_valid(df['DGS10']), OCEAN_BLUE, 'fill', '{:.2f}')
    lastvalue_label(ax, last_valid(df['DGS2']),  MAGENTA,    'outline', '{:.2f}')
    ax2 = lhm_twin(ax)
    ax2.plot(spread.index, spread, color=SUNSET_ORANGE, label='2s10s (LHS)')
    lastvalue_label(ax2, last_valid(spread), SUNSET_ORANGE, 'fill', '{:.2f}')
    ax.set_title('Treasury Yields & Curve')
    savefig(ax, '04_yield_curve.png', sources=['DGS10','DGS2'])

# 5) Dollar vs Real 10Y
def chart_05():
    df = fred_fetch(['DTWEXBGS','DFII10'], start='2003-01-01')
    fig, ax = plt.subplots(figsize=(10,4)); lhm_axis_right(ax)
    ax.plot(df.index, df['DTWEXBGS'], color=OCEAN_BLUE, label='USD Broad')
    lastvalue_label(ax, last_valid(df['DTWEXBGS']), OCEAN_BLUE, 'fill', '{:.1f}')
    ax2 = lhm_twin(ax)
    ax2.plot(df.index, df['DFII10'], color=SUNSET_ORANGE, label='10Y TIPS %')
    lastvalue_label(ax2, last_valid(df['DFII10']), SUNSET_ORANGE, 'outline', '{:.2f}')
    ax.set_title('Dollar vs Real Yields')
    savefig(ax, '05_dxy_vs_real10y.png', sources=['DTWEXBGS','DFII10'])

# 6) Oil & Copper (index=100) vs CPI YoY
def chart_06():
    df = fred_fetch(['DCOILWTICO','PCOPPUSDM','CPIAUCSL'], start='2000-01-01')
    cpi = yoy(df['CPIAUCSL'])
    oil = 100 * df['DCOILWTICO'] / df['DCOILWTICO'].dropna().iloc[0]
    cu  = 100 * df['PCOPPUSDM']  / df['PCOPPUSDM'].dropna().iloc[0]
    fig, ax = plt.subplots(figsize=(10,4)); lhm_axis_right(ax)
    ax.plot(oil.index, oil, color=OCEAN_BLUE, label='WTI (idx=100)')
    ax.plot(cu.index,  cu,  color=CAROLINA_BLUE, label='Copper (idx=100)')
    lastvalue_label(ax, last_valid(oil), OCEAN_BLUE, 'fill', '{:.0f}')
    lastvalue_label(ax, last_valid(cu),  CAROLINA_BLUE, 'outline', '{:.0f}')
    ax2 = lhm_twin(ax)
    ax2.plot(cpi.index, cpi, color=SUNSET_ORANGE, label='CPI YoY %')
    lastvalue_label(ax2, last_valid(cpi), SUNSET_ORANGE, 'fill', '{:.1f}')
    ax.set_title('Oil & Copper vs CPI')
    savefig(ax, '06_oil_copper_vs_cpi.png', sources=['DCOILWTICO','PCOPPUSDM','CPIAUCSL'])

# 7) RRP & SOFR vs CPI
def chart_07():
    df = fred_fetch(['RRPONTSYD','SOFR','CPIAUCSL'], start='2018-01-01')
    cpi = yoy(df['CPIAUCSL'])
    fig, ax = plt.subplots(figsize=(10,4)); lhm_axis_right(ax)
    ax.plot(df.index, df['RRPONTSYD']/1e6, color=CAROLINA_BLUE, label='ON RRP ($T)')
    lastvalue_label(ax, last_valid(df['RRPONTSYD']/1e6), CAROLINA_BLUE, 'fill', '{:.2f}')
    ax.plot(df.index, df['SOFR'], color=MAGENTA, lw=1.6, label='SOFR %')
    lastvalue_label(ax, last_valid(df['SOFR']), MAGENTA, 'outline', '{:.2f}')
    ax2 = lhm_twin(ax)
    ax2.plot(cpi.index, cpi, color=SUNSET_ORANGE, label='CPI YoY %')
    lastvalue_label(ax2, last_valid(cpi), SUNSET_ORANGE, 'fill', '{:.1f}')
    ax.set_title('RRP & SOFR vs CPI')
    savefig(ax, '07_rrp_sofr_vs_cpi.png', sources=['RRPONTSYD','SOFR','CPIAUCSL'])

# 8) Manufacturing construction
def chart_08():
    df = fred_fetch('TLRESCONS', start='2002-01-01')
    idx = 100 * df['TLRESCONS'] / df['TLRESCONS'].dropna().iloc[0]
    fig, ax = plt.subplots(figsize=(10,4)); lhm_axis_right(ax)
    ax.plot(idx.index, idx, color=OCEAN_BLUE, label='US Manufacturing Construction (idx=100)')
    lastvalue_label(ax, last_valid(idx), OCEAN_BLUE, 'fill', '{:.0f}')
    ax.set_title('Reindustrialization: Manufacturing Construction Spend')
    savefig(ax, '08_manufacturing_construction.png', sources=['TLRESCONS'])

# 9) Durable Goods Orders
def chart_09():
    df = fred_fetch('DGORDER', start='2000-01-01')
    idx = 100 * df['DGORDER'] / df['DGORDER'].dropna().iloc[0]
    fig, ax = plt.subplots(figsize=(10,4)); lhm_axis_right(ax)
    ax.plot(idx.index, idx, color=CAROLINA_BLUE, label='Durable Goods Orders (idx=100)')
    lastvalue_label(ax, last_valid(idx), CAROLINA_BLUE, 'fill', '{:.0f}')
    ax.set_title('Durable Goods Orders (Index)')
    savefig(ax, '09_durable_goods_orders.png', sources=['DGORDER'])

# 10) Unemployment vs Job Openings Rate
def chart_10():
    df = fred_fetch(['UNRATE','JTSJOR'], start='2001-01-01')
    fig, ax = plt.subplots(figsize=(10,4)); lhm_axis_right(ax)
    ax.plot(df.index, df['UNRATE'], color=OCEAN_BLUE, label='Unemployment Rate %')
    lastvalue_label(ax, last_valid(df['UNRATE']), OCEAN_BLUE, 'fill', '{:.1f}')
    ax2 = lhm_twin(ax)
    ax2.plot(df.index, df['JTSJOR'], color=SUNSET_ORANGE, label='Job Openings Rate %')
    lastvalue_label(ax2, last_valid(df['JTSJOR']), SUNSET_ORANGE, 'outline', '{:.1f}')
    ax.set_title('Labor Market: UNRATE vs JOLTS Job Openings Rate')
    savefig(ax, '10_unrate_vs_jolts.png', sources=['UNRATE','JTSJOR'])

# 11) Housing Starts vs 30Y Mortgage Rate
def chart_11():
    df = fred_fetch(['HOUST','MORTGAGE30US'], start='1995-01-01')
    hs = df['HOUST']/1000.0
    fig, ax = plt.subplots(figsize=(10,4)); lhm_axis_right(ax)
    ax.plot(hs.index, hs, color=CAROLINA_BLUE, label='Housing Starts (M, Thous)')
    lastvalue_label(ax, last_valid(hs), CAROLINA_BLUE, 'fill', '{:.2f}')
    ax2 = lhm_twin(ax)
    ax2.plot(df.index, df['MORTGAGE30US'], color=SUNSET_ORANGE, label='30Y Mortgage Rate %')
    lastvalue_label(ax2, last_valid(df['MORTGAGE30US']), SUNSET_ORANGE, 'outline', '{:.2f}')
    ax.set_title('Housing Starts vs 30Y Mortgage Rate')
    savefig(ax, '11_housing_vs_mortgage.png', sources=['HOUST','MORTGAGE30US'])

# 12) Core PCE vs CPI YoY
def chart_12():
    df = fred_fetch(['PCEPILFE','CPIAUCSL'], start='1995-01-01')
    core_pce = yoy(df['PCEPILFE']); cpi = yoy(df['CPIAUCSL'])
    fig, ax = plt.subplots(figsize=(10,4)); lhm_axis_right(ax)
    ax.plot(core_pce.index, core_pce, color=OCEAN_BLUE, label='Core PCE YoY %')
    lastvalue_label(ax, last_valid(core_pce), OCEAN_BLUE, 'fill', '{:.1f}')
    ax2 = lhm_twin(ax)
    ax2.plot(cpi.index, cpi, color=SUNSET_ORANGE, label='CPI YoY %')
    lastvalue_label(ax2, last_valid(cpi), SUNSET_ORANGE, 'outline', '{:.1f}')
    ax.set_title('Core PCE vs CPI YoY')
    savefig(ax, '12_corepce_vs_cpi.png', sources=['PCEPILFE','CPIAUCSL'])

# 13) Financial Conditions (NFCI)
def chart_13():
    df = fred_fetch('NFCI', start='1990-01-01')
    fig, ax = plt.subplots(figsize=(10,4)); lhm_axis_right(ax)
    ax.axhline(0, color=LIGHT_GRAY, ls='--', lw=1.0)
    ax.plot(df.index, df['NFCI'], color=OCEAN_BLUE, label='Chicago Fed NFCI')
    lastvalue_label(ax, last_valid(df['NFCI']), OCEAN_BLUE, 'fill', '{:.2f}')
    ax.set_title('Financial Conditions (NFCI, 0 = Neutral)')
    savefig(ax, '13_nfci.png', sources=['NFCI'])

# 14) Credit Spread: BAA - 10Y
def chart_14():
    df = fred_fetch(['DBAA','DGS10'], start='1995-01-01')
    spread = df['DBAA'] - df['DGS10']
    fig, ax = plt.subplots(figsize=(10,4)); lhm_axis_right(ax)
    ax.plot(spread.index, spread, color=SUNSET_ORANGE, label='BAA - 10Y Spread (bps)')
    lastvalue_label(ax, last_valid(spread), SUNSET_ORANGE, 'fill', '{:.2f}')
    ax.set_title('Corporate Credit Spread (BAA - 10Y)')
    savefig(ax, '14_baa_minus_10y.png', sources=['DBAA','DGS10'])

# 15) Payrolls YoY vs Industrial Production YoY
def chart_15():
    df = fred_fetch(['PAYEMS','INDPRO'], start='1995-01-01')
    py = df['PAYEMS'].pct_change(12) * 100.0
    ip = df['INDPRO'].pct_change(12) * 100.0
    fig, ax = plt.subplots(figsize=(10,4)); lhm_axis_right(ax)
    ax.plot(py.index, py, color=OCEAN_BLUE, label='Nonfarm Payrolls YoY %')
    lastvalue_label(ax, last_valid(py), OCEAN_BLUE, 'fill', '{:.2f}')
    ax2 = lhm_twin(ax)
    ax2.plot(ip.index, ip, color=SUNSET_ORANGE, label='Industrial Production YoY %')
    lastvalue_label(ax2, last_valid(ip), SUNSET_ORANGE, 'outline', '{:.2f}')
    ax.set_title('Payrolls YoY vs Industrial Production YoY')
    savefig(ax, '15_payrolls_vs_indpro.png', sources=['PAYEMS','INDPRO'])

def main():
    charts = [chart_01, chart_02, chart_03, chart_04, chart_05,
              chart_06, chart_07, chart_08, chart_09, chart_10,
              chart_11, chart_12, chart_13, chart_14, chart_15]
    for fn in charts:
        try:
            fn(); plt.close('all')
        except Exception as e:
            print("Error in", fn.__name__, "->", e)

if __name__ == "__main__":
    main()
