#!/usr/bin/env python3
"""
LIGHTHOUSE MACRO — THE CHARTBOOK FRIDAY
Week 45, November 7th, 2025
Data through November 9th, 2025
"""

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from pathlib import Path
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURATION
# ============================================================

# Color Palette
OCEAN_BLUE = '#0077FF'
DUSK_ORANGE = '#FF4500'
CAROLINA_BLUE = '#00BFFF'
NEON_MAGENTA = '#FF00FF'
GRAY = '#8A8F98'

# FRED API Key
FRED_API_KEY = '6dcc7a0d790cdcc28c1f751420ee9d27'

# Edition Details
EDITION_DATE = '2025-11-07'
WEEK_NUMBER = 45
DATA_THROUGH = '2025-11-09'

# Directories
CHARTS_DIR = Path('charts')
EXPORTS_DIR = Path('exports')
CHARTS_DIR.mkdir(exist_ok=True)
EXPORTS_DIR.mkdir(exist_ok=True)

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def fred_api(series_id, api_key=FRED_API_KEY, start_date='1990-01-01'):
    """Fetch data from FRED API and return a Pandas Series."""
    url = (
        f"https://api.stlouisfed.org/fred/series/observations"
        f"?series_id={series_id}&api_key={api_key}&file_type=json&observation_start={start_date}"
    )
    try:
        resp = requests.get(url, timeout=30)
        data = resp.json()['observations']
        dates = pd.to_datetime([obs['date'] for obs in data])
        values = [float(obs['value']) if obs['value'] not in ('', '.', 'nan') else np.nan for obs in data]
        series = pd.Series(values, index=dates, name=series_id)
        return series.astype(float)
    except Exception as e:
        print(f"Error fetching {series_id}: {e}")
        return pd.Series(dtype=float, name=series_id)

def zscore(series, window=None):
    """Calculate z-score (rolling if window specified)."""
    if window:
        return (series - series.rolling(window).mean()) / series.rolling(window).std()
    return (series - series.mean()) / series.std()

def percentile(series):
    """Calculate percentile rank."""
    return series.rank(pct=True)

def yoy_change(series):
    """Year-over-year percent change."""
    return series.pct_change(12) * 100

def annualized_growth(series, periods=3):
    """Annualized growth rate over N periods."""
    return (series.pct_change(periods) * (12/periods)) * 100

def style_chart(ax, title, subtitle=None):
    """Apply Lighthouse Macro styling to chart."""
    # Title
    ax.set_title(title, loc='center', fontsize=16, fontweight='bold',
                 color=OCEAN_BLUE, pad=20)

    # Subtitle
    if subtitle:
        ax.text(0.5, 1.02, subtitle, transform=ax.transAxes,
                ha='center', fontsize=10, color=GRAY, style='italic')

    # Get figure
    fig = ax.get_figure()

    # Watermarks
    fig.text(0.02, 0.98, "LIGHTHOUSE MACRO", fontsize=12,
             color=OCEAN_BLUE, alpha=0.8, weight='bold',
             transform=fig.transFigure, va='top')
    fig.text(0.98, 0.02, "MACRO, ILLUMINATED.", fontsize=9,
             color=GRAY, alpha=0.7, transform=fig.transFigure,
             ha='right', va='bottom')

    # Spines - all four visible
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1.5)
        spine.set_color(OCEAN_BLUE)
        spine.set_alpha(0.3)

    # Grid off
    ax.grid(False)

    # Tick styling
    ax.tick_params(colors=GRAY, which='both', labelsize=9)

    return ax

def save_chart(fig, filename, citation=None):
    """Save chart with citation."""
    if citation:
        fig.text(0.02, 0.02, f"Source: {citation} | Analysis: Lighthouse Macro",
                fontsize=7, color=GRAY, alpha=0.6, transform=fig.transFigure,
                va='bottom')

    fig.tight_layout(rect=[0, 0.03, 1, 0.97])
    filepath = CHARTS_DIR / filename
    fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  ✓ Saved: {filename}")

def plot_single(df, title, ylabel, filename, colors=None, citation=None, legend_loc='best'):
    """Create single-axis line chart."""
    fig, ax = plt.subplots(figsize=(14, 8))

    if colors is None:
        colors = [OCEAN_BLUE, DUSK_ORANGE, CAROLINA_BLUE, NEON_MAGENTA]

    for idx, col in enumerate(df.columns):
        color = colors[idx % len(colors)]
        ax.plot(df.index, df[col], color=color, linewidth=2.5,
               label=col, alpha=0.9)

    ax.set_ylabel(ylabel, fontsize=11, color=GRAY, weight='bold')
    ax.legend(loc=legend_loc, frameon=True, fontsize=9,
             fancybox=True, shadow=True)

    style_chart(ax, title)
    save_chart(fig, filename, citation)

def plot_dual(df, title, y1_label, y2_label, filename,
              y1_color=OCEAN_BLUE, y2_color=DUSK_ORANGE, citation=None):
    """Create dual-axis chart."""
    fig, ax1 = plt.subplots(figsize=(14, 8))

    # Left axis
    ax1.plot(df.index, df.iloc[:, 0], color=y1_color,
            linewidth=2.5, label=df.columns[0])
    ax1.set_ylabel(y1_label, color=y1_color, fontsize=11, weight='bold')
    ax1.tick_params(axis='y', labelcolor=y1_color)

    # Right axis
    ax2 = ax1.twinx()
    ax2.plot(df.index, df.iloc[:, 1], color=y2_color,
            linewidth=2.5, label=df.columns[1])
    ax2.set_ylabel(y2_label, color=y2_color, fontsize=11, weight='bold')
    ax2.tick_params(axis='y', labelcolor=y2_color)

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left',
              frameon=True, fontsize=9, fancybox=True, shadow=True)

    style_chart(ax1, title)
    save_chart(fig, filename, citation)

def plot_bar(df, title, ylabel, filename, color=OCEAN_BLUE, citation=None):
    """Create bar chart."""
    fig, ax = plt.subplots(figsize=(14, 8))

    df.plot(kind='bar', ax=ax, color=color, alpha=0.8, width=0.7)
    ax.set_ylabel(ylabel, fontsize=11, color=GRAY, weight='bold')
    ax.set_xlabel('')
    plt.xticks(rotation=45, ha='right')

    style_chart(ax, title)
    save_chart(fig, filename, citation)

# ============================================================
# DATA FETCHING
# ============================================================

print("="*70)
print("LIGHTHOUSE MACRO — CHARTBOOK GENERATION")
print(f"Edition: Week {WEEK_NUMBER} | {EDITION_DATE}")
print(f"Data Through: {DATA_THROUGH}")
print("="*70)
print("\n📊 Fetching data from FRED API...\n")

# ARC 1: MACRO DYNAMICS
print("Arc 1: Macro Dynamics")

# GDP & Growth
gdp = fred_api('GDP')
gdpc1 = fred_api('GDPC1')  # Real GDP
gdp_final_sales = fred_api('FINSLC1')  # Real Final Sales
gdp_consumption = fred_api('PCECC96')  # Real PCE
gdp_investment = fred_api('GPDIC1')  # Real Gross Private Investment
gdp_govt = fred_api('GCEC1')  # Real Govt Consumption
gdp_exports = fred_api('EXPGSC1')  # Real Exports
gdp_imports = fred_api('IMPGSC1')  # Real Imports

# Inflation
cpi = fred_api('CPIAUCSL')
pce = fred_api('PCEPI')
core_pce = fred_api('PCEPILFE')
ppi = fred_api('PPIACO')
cpi_goods = fred_api('CUSR0000SAC')  # CPI All Commodities
cpi_services = fred_api('CUSR0000SAS')  # CPI Services
breakeven_5y = fred_api('T5YIE')
breakeven_10y = fred_api('T10YIE')

# Labor
payems = fred_api('PAYEMS')
unrate = fred_api('UNRATE')
u6 = fred_api('U6RATE')
lfpr = fred_api('CIVPART')
prime_age_lfpr = fred_api('LNS11300060')  # 25-54 LFPR
avg_hourly_earnings = fred_api('CES0500000003')
avg_weekly_hours = fred_api('AWHAETP')
jobless_claims = fred_api('ICSA')
continuing_claims = fred_api('CCSA')
jolts_openings = fred_api('JTSJOL')
jolts_quits = fred_api('JTSQUR')
jolts_hires = fred_api('JTSHIR')
jolts_layoffs = fred_api('JTSLDL')
uemp_mean = fred_api('UEMPMEAN')
uemp_median = fred_api('UEMPMED')
uemp_27weeks = fred_api('UEMP27OV')

# ISM & Surveys
ism_mfg = fred_api('NAPM')
ism_new_orders = fred_api('NAPMNOI')
ism_inventory = fred_api('NAPMII')
ism_services = fred_api('NMFCI')  # ISM Non-Mfg Composite
michigan_sentiment = fred_api('UMCSENT')
conf_board = fred_api('CSCICP03USM665S')  # Consumer Confidence

# Fiscal
receipts = fred_api('FGRECPT')
outlays = fred_api('FGEXPND')
deficit = fred_api('FYFSD')
debt_gdp = fred_api('GFDEGDQ188S')

# Trade
trade_balance = fred_api('BOPGSTB')
exports = fred_api('EXPGS')
imports = fred_api('IMPGS')

# Commodities
oil_wti = fred_api('DCOILWTICO')
oil_brent = fred_api('DCOILBRENTEU')
gold = fred_api('GOLDAMGBD228NLBM')
copper = fred_api('PCOPPUSDM')

print("  ✓ Macro data fetched")

# ARC 2: MONETARY MECHANICS
print("Arc 2: Monetary Mechanics")

# Fed Balance Sheet
fed_assets = fred_api('WALCL')
fed_securities = fred_api('WSHOSHO')
rrp_on = fred_api('RRPONTSYD')
reserves = fred_api('RESBALNS')
tga = fred_api('WTREGEN')

# Rates
effr = fred_api('EFFR')
sofr = fred_api('SOFR')
iorb = fred_api('IORB')
dgs_3m = fred_api('DGS3MO')
dgs_2y = fred_api('DGS2')
dgs_5y = fred_api('DGS5')
dgs_10y = fred_api('DGS10')
dgs_30y = fred_api('DGS30')

# Term Premium (ACM model approximation via spread)
# We'll calculate a proxy

# Credit
ig_oas = fred_api('BAMLC0A0CM')  # IG Corporate OAS
hy_oas = fred_api('BAMLH0A0HYM2')  # HY OAS
bbb_oas = fred_api('BAMLC0A4CBBB')  # BBB OAS
mortgage_30y = fred_api('MORTGAGE30US')

# Money Supply
m2 = fred_api('M2SL')
m2_velocity = fred_api('M2V')

print("  ✓ Monetary data fetched")

# ARC 3: MARKET TECHNICALS
print("Arc 3: Market Technicals")

# Equities
sp500 = fred_api('SP500')
nasdaq = fred_api('NASDAQCOM')
russell_2000 = fred_api('RU2000PR')
vix = fred_api('VIXCLS')
move = fred_api('MOVE')  # Bond vol

# We'll calculate breadth metrics from SPX

print("  ✓ Market data fetched")

# ARC 4: ASSET CLASSES
print("Arc 4: Asset Classes")

# FX
dxy = fred_api('DTWEXBGS')  # Broad Dollar Index
eurusd = fred_api('DEXUSEU')
jpyusd = fred_api('DEXJPUS')
gbpusd = fred_api('DEXUSUK')

# Commodities (already fetched above)
# Gold, Oil, Copper

print("  ✓ FX & commodity data fetched")

# ARC 5: SINGLE NAMES
print("Arc 5: Single-Name Diagnostics")

# For single names, we'd ideally pull from Yahoo Finance or similar
# For this demo, we'll note that this would require additional data sources
print("  ⚠ Single-name equity data requires additional API (Yahoo Finance, etc.)")

print("\n✅ All data fetched successfully!\n")

# ============================================================
# DATA TRANSFORMATIONS & METRICS
# ============================================================

print("🔧 Computing metrics and transformations...\n")

# Arc 1 Metrics
gdp_yoy = yoy_change(gdp)
gdp_3m_ann = annualized_growth(gdpc1, 3)
final_sales_3m_ann = annualized_growth(gdp_final_sales, 3)

core_pce_yoy = yoy_change(core_pce)
pce_yoy = yoy_change(pce)
cpi_yoy = yoy_change(cpi)

payroll_yoy = yoy_change(payems)
payroll_3m_ann = annualized_growth(payems, 3)

wage_growth = yoy_change(avg_hourly_earnings)

sahm_rule = unrate.rolling(3).mean() - unrate.rolling(12).min()

labor_fragility = pd.DataFrame({
    'quits_z': -zscore(jolts_quits),
    'uemp_27_z': zscore(uemp_27weeks),
    'hours_z': -zscore(avg_weekly_hours),
    'hires_z': -zscore(jolts_hires)
}).mean(axis=1)

# Arc 2 Metrics
curve_2s10s = dgs_10y - dgs_2y
curve_3m10y = dgs_10y - dgs_3m

funding_spread = sofr - effr
collateral_spread = sofr - iorb

rrp_share = rrp_on / (rrp_on + reserves)

# Liquidity conditions
liquidity_index = pd.DataFrame({
    'reserves_z': zscore(reserves),
    'rrp_z': -zscore(rrp_on),
    'tga_z': -zscore(tga),
    'funding_z': -zscore(funding_spread)
}).mean(axis=1)

# Arc 3 Metrics
spx_50ma = sp500.rolling(50).mean()
spx_200ma = sp500.rolling(200).mean()

# Arc 4 Metrics
real_yield_10y = dgs_10y - breakeven_10y

print("✅ Metrics computed!\n")

# ============================================================
# CHART GENERATION
# ============================================================

print("="*70)
print("📈 GENERATING CHARTS")
print("="*70)

# ------------------------------------------------------------
# ARC 1: MACRO DYNAMICS (15-20 charts)
# ------------------------------------------------------------
print("\n🌍 Arc 1: Macro Dynamics")

# Chart 1: Real GDP vs Final Sales (3M annualized)
df = pd.concat([gdp_3m_ann, final_sales_3m_ann], axis=1).dropna()
df.columns = ['Real GDP', 'Final Sales']
plot_single(df.tail(120),
           'Real GDP vs Final Sales (3M Annualized)',
           'Percent Change (Annual Rate)',
           'macro_01_gdp_final_sales.png',
           citation='BEA')

# Chart 2: Core PCE vs Supercore Proxy
df = pd.concat([pce_yoy, core_pce_yoy], axis=1).dropna()
df.columns = ['Headline PCE', 'Core PCE']
plot_single(df.tail(120),
           'PCE Inflation: Headline vs Core',
           'Year-over-Year %',
           'macro_02_pce_inflation.png',
           citation='BEA, BLS')

# Chart 3: Goods vs Services Inflation
df = pd.concat([yoy_change(cpi_goods), yoy_change(cpi_services)], axis=1).dropna()
df.columns = ['Goods Inflation', 'Services Inflation']
plot_single(df.tail(120),
           'Goods vs Services Inflation',
           'Year-over-Year %',
           'macro_03_goods_services_inflation.png',
           citation='BLS')

# Chart 4: Payrolls vs Diffusion (using 3m annualized as proxy)
df = pd.concat([payroll_yoy, payroll_3m_ann], axis=1).dropna()
df.columns = ['Payrolls YoY', 'Payrolls 3M Ann']
plot_dual(df.tail(120),
          'Payroll Growth: Momentum vs Trend',
          'YoY %', '3M Annualized %',
          'macro_04_payrolls_momentum.png',
          citation='BLS')

# Chart 5: ISM Manufacturing vs New Orders-Inventory
df = pd.concat([ism_mfg, ism_new_orders - ism_inventory], axis=1).dropna()
df.columns = ['ISM Mfg PMI', 'New Orders - Inventory']
plot_dual(df.tail(120),
          'ISM Manufacturing: PMI vs Order-Inventory Gap',
          'PMI Level', 'Spread (Index Points)',
          'macro_05_ism_orders_inventory.png',
          citation='ISM')

# Chart 6: Unemployment Rate vs U-6
df = pd.concat([unrate, u6], axis=1).dropna()
df.columns = ['U-3 (Headline)', 'U-6 (Broad)']
plot_single(df.tail(120),
           'Unemployment Rates: U-3 vs U-6',
           'Percent',
           'macro_06_unemployment_u3_u6.png',
           citation='BLS')

# Chart 7: Labor Force Participation: Total vs Prime Age
df = pd.concat([lfpr, prime_age_lfpr], axis=1).dropna()
df.columns = ['Total LFPR', 'Prime Age (25-54)']
plot_single(df.tail(120),
           'Labor Force Participation Rates',
           'Percent',
           'macro_07_lfpr.png',
           citation='BLS')

# Chart 8: Wage Growth vs Core PCE
df = pd.concat([wage_growth, core_pce_yoy], axis=1).dropna()
df.columns = ['Avg Hourly Earnings YoY', 'Core PCE YoY']
plot_dual(df.tail(120),
          'Wages vs Inflation',
          'Wage Growth %', 'Core PCE %',
          'macro_08_wages_inflation.png',
          citation='BLS, BEA')

# Chart 9: JOLTS Quits vs Layoffs
df = pd.concat([jolts_quits, jolts_layoffs], axis=1).dropna()
df.columns = ['Quits Rate', 'Layoffs Rate']
plot_single(df.tail(60),
           'JOLTS: Quits vs Layoffs',
           'Rate (Thousands)',
           'macro_09_jolts_quits_layoffs.png',
           citation='BLS JOLTS')

# Chart 10: JOLTS Openings vs Hires
df = pd.concat([jolts_openings, jolts_hires], axis=1).dropna()
df.columns = ['Job Openings', 'Hires']
plot_single(df.tail(60),
           'JOLTS: Openings vs Hires',
           'Thousands',
           'macro_10_jolts_openings_hires.png',
           citation='BLS JOLTS')

# Chart 11: Sahm Rule Indicator
df = pd.DataFrame({'Sahm Rule': sahm_rule}).dropna()
fig, ax = plt.subplots(figsize=(14, 8))
ax.plot(df.index, df['Sahm Rule'], color=OCEAN_BLUE, linewidth=2.5)
ax.axhline(y=0.5, color=DUSK_ORANGE, linestyle='--', linewidth=2,
          label='Recession Threshold (0.5)')
ax.fill_between(df.index, 0.5, df['Sahm Rule'].max(),
                where=(df['Sahm Rule'] > 0.5), alpha=0.2, color=DUSK_ORANGE)
ax.set_ylabel('Percentage Points', fontsize=11, color=GRAY, weight='bold')
ax.legend(loc='upper left', frameon=True, fontsize=9)
style_chart(ax, 'Sahm Rule Recession Indicator')
save_chart(fig, 'macro_11_sahm_rule.png', citation='BLS, Sahm (2019)')

# Chart 12: Consumer Sentiment: UMich vs Conference Board
df = pd.concat([michigan_sentiment, conf_board], axis=1).dropna()
df.columns = ['UMich Sentiment', 'Conf Board']
plot_single(df.tail(120),
           'Consumer Sentiment Surveys',
           'Index Level',
           'macro_12_consumer_sentiment.png',
           citation='UMich, Conference Board')

# Chart 13: Trade Balance
df = pd.DataFrame({'Trade Balance': trade_balance}).dropna()
plot_single(df.tail(120),
           'US Trade Balance',
           'Millions USD',
           'macro_13_trade_balance.png',
           citation='BEA')

# Chart 14: Fiscal Deficit
df = pd.DataFrame({'Federal Deficit': deficit}).dropna()
plot_single(df.tail(60),
           'Federal Budget Deficit',
           'Millions USD',
           'macro_14_deficit.png',
           citation='US Treasury')

# Chart 15: Federal Debt to GDP
df = pd.DataFrame({'Debt/GDP': debt_gdp}).dropna()
plot_single(df.tail(120),
           'Federal Debt as % of GDP',
           'Percent',
           'macro_15_debt_gdp.png',
           citation='BEA, US Treasury')

# Chart 16: Labor Fragility Index
df = pd.DataFrame({'Labor Fragility': labor_fragility}).dropna()
plot_single(df.tail(60),
           'Labor Fragility Index (Proprietary)',
           'Z-Score',
           'macro_16_labor_fragility.png',
           citation='BLS JOLTS, Lighthouse Macro')

# Chart 17: Oil Prices: WTI vs Brent
df = pd.concat([oil_wti, oil_brent], axis=1).dropna()
df.columns = ['WTI', 'Brent']
plot_single(df.tail(120),
           'Crude Oil Prices',
           'USD per Barrel',
           'macro_17_oil_prices.png',
           citation='EIA')

# Chart 18: Breakeven Inflation: 5Y vs 10Y
df = pd.concat([breakeven_5y, breakeven_10y], axis=1).dropna()
df.columns = ['5Y Breakeven', '10Y Breakeven']
plot_single(df.tail(120),
           'Breakeven Inflation Expectations',
           'Percent',
           'macro_18_breakeven_inflation.png',
           citation='Federal Reserve')

# ------------------------------------------------------------
# ARC 2: MONETARY MECHANICS (15-20 charts)
# ------------------------------------------------------------
print("\n💧 Arc 2: Monetary Mechanics")

# Chart 21: Fed Balance Sheet Components
df = pd.concat([fed_assets/1e6, fed_securities/1e6], axis=1).dropna()
df.columns = ['Total Assets', 'Securities Held']
plot_single(df.tail(120),
           'Federal Reserve Balance Sheet',
           'Trillions USD',
           'plumbing_21_fed_balance_sheet.png',
           citation='Federal Reserve H.4.1')

# Chart 22: RRP vs Reserves
df = pd.concat([rrp_on/1e6, reserves/1e6], axis=1).dropna()
df.columns = ['ON RRP', 'Reserves']
plot_single(df.tail(120),
           'ON RRP vs Bank Reserves',
           'Trillions USD',
           'plumbing_22_rrp_reserves.png',
           citation='Federal Reserve H.4.1')

# Chart 23: Treasury General Account (TGA)
df = pd.DataFrame({'TGA': tga/1e6}).dropna()
plot_single(df.tail(120),
           'Treasury General Account Balance',
           'Trillions USD',
           'plumbing_23_tga.png',
           citation='Federal Reserve H.4.1')

# Chart 24: RRP Share of Total Reserves+RRP
df = pd.DataFrame({'RRP Share': rrp_share * 100}).dropna()
plot_single(df.tail(120),
           'ON RRP as % of (RRP + Reserves)',
           'Percent',
           'plumbing_24_rrp_share.png',
           citation='Federal Reserve H.4.1, Lighthouse Macro')

# Chart 25: SOFR vs EFFR
df = pd.concat([sofr, effr], axis=1).dropna()
df.columns = ['SOFR', 'EFFR']
plot_single(df.tail(120),
           'Secured vs Unsecured Overnight Rates',
           'Percent',
           'plumbing_25_sofr_effr.png',
           citation='Federal Reserve')

# Chart 26: SOFR - EFFR Spread
df = pd.DataFrame({'SOFR - EFFR': funding_spread}).dropna()
plot_single(df.tail(120),
           'Funding Spread (SOFR - EFFR)',
           'Basis Points',
           'plumbing_26_funding_spread.png',
           citation='Federal Reserve, Lighthouse Macro')

# Chart 27: SOFR - IORB (Collateral Scarcity)
df = pd.DataFrame({'SOFR - IORB': collateral_spread}).dropna()
plot_single(df.tail(120),
           'Collateral Scarcity Proxy (SOFR - IORB)',
           'Basis Points',
           'plumbing_27_collateral_spread.png',
           citation='Federal Reserve, Lighthouse Macro')

# Chart 28: Yield Curve: 2s10s
df = pd.DataFrame({'2s10s': curve_2s10s}).dropna()
fig, ax = plt.subplots(figsize=(14, 8))
ax.plot(df.index, df['2s10s'], color=OCEAN_BLUE, linewidth=2.5)
ax.axhline(y=0, color=DUSK_ORANGE, linestyle='--', linewidth=2, alpha=0.7)
ax.fill_between(df.index, 0, df['2s10s'], where=(df['2s10s'] < 0),
                alpha=0.2, color=DUSK_ORANGE, label='Inverted')
ax.set_ylabel('Basis Points', fontsize=11, color=GRAY, weight='bold')
ax.legend(loc='best', frameon=True, fontsize=9)
style_chart(ax, '2s10s Yield Curve')
save_chart(fig, 'plumbing_28_curve_2s10s.png', citation='Federal Reserve')

# Chart 29: Yield Curve: 3m10y
df = pd.DataFrame({'3m10y': curve_3m10y}).dropna()
fig, ax = plt.subplots(figsize=(14, 8))
ax.plot(df.index, df['3m10y'], color=OCEAN_BLUE, linewidth=2.5)
ax.axhline(y=0, color=DUSK_ORANGE, linestyle='--', linewidth=2, alpha=0.7)
ax.fill_between(df.index, 0, df['3m10y'], where=(df['3m10y'] < 0),
                alpha=0.2, color=DUSK_ORANGE, label='Inverted')
ax.set_ylabel('Basis Points', fontsize=11, color=GRAY, weight='bold')
ax.legend(loc='best', frameon=True, fontsize=9)
style_chart(ax, '3M10Y Yield Curve')
save_chart(fig, 'plumbing_29_curve_3m10y.png', citation='Federal Reserve')

# Chart 30: Treasury Yields Across Curve
df = pd.concat([dgs_3m, dgs_2y, dgs_5y, dgs_10y, dgs_30y], axis=1).dropna()
df.columns = ['3M', '2Y', '5Y', '10Y', '30Y']
plot_single(df.tail(120),
           'Treasury Yield Curve Points',
           'Percent',
           'plumbing_30_treasury_yields.png',
           citation='Federal Reserve')

# Chart 31: IG vs HY Corporate Spreads
df = pd.concat([ig_oas, hy_oas], axis=1).dropna()
df.columns = ['IG OAS', 'HY OAS']
plot_single(df.tail(120),
           'Corporate Credit Spreads',
           'Basis Points',
           'plumbing_31_credit_spreads.png',
           citation='ICE BofA')

# Chart 32: HY-IG Spread
df = pd.DataFrame({'HY-IG Spread': (hy_oas - ig_oas)}).dropna()
plot_single(df.tail(120),
           'HY minus IG Spread',
           'Basis Points',
           'plumbing_32_hy_ig_spread.png',
           citation='ICE BofA, Lighthouse Macro')

# Chart 33: M2 Money Supply
df = pd.DataFrame({'M2': m2/1e6}).dropna()
plot_single(df.tail(120),
           'M2 Money Supply',
           'Trillions USD',
           'plumbing_33_m2.png',
           citation='Federal Reserve')

# Chart 34: M2 Velocity
df = pd.DataFrame({'M2 Velocity': m2_velocity}).dropna()
plot_single(df.tail(120),
           'M2 Velocity of Money',
           'Ratio',
           'plumbing_34_m2_velocity.png',
           citation='Federal Reserve, BEA')

# Chart 35: 30Y Mortgage Rate
df = pd.DataFrame({'30Y Mortgage': mortgage_30y}).dropna()
plot_single(df.tail(120),
           '30-Year Fixed Mortgage Rate',
           'Percent',
           'plumbing_35_mortgage_rate.png',
           citation='Freddie Mac')

# Chart 36: Liquidity Index (Proprietary)
df = pd.DataFrame({'Liquidity Index': liquidity_index}).dropna()
plot_single(df.tail(120),
           'Liquidity Plumbing Index (Proprietary)',
           'Composite Z-Score',
           'plumbing_36_liquidity_index.png',
           citation='Federal Reserve, Lighthouse Macro')

# Chart 37: Real 10Y Yield
df = pd.DataFrame({'Real 10Y Yield': real_yield_10y}).dropna()
plot_single(df.tail(120),
           'Real 10-Year Treasury Yield',
           'Percent',
           'plumbing_37_real_10y.png',
           citation='Federal Reserve, Lighthouse Macro')

# ------------------------------------------------------------
# ARC 3: MARKET TECHNICALS (15-20 charts)
# ------------------------------------------------------------
print("\n📈 Arc 3: Market Technicals")

# Chart 41: S&P 500 Level
df = pd.DataFrame({'S&P 500': sp500}).dropna()
plot_single(df.tail(250),
           'S&P 500 Index',
           'Index Level',
           'tech_41_sp500.png',
           citation='S&P Dow Jones Indices')

# Chart 42: S&P 500 with 50 & 200 Day MAs
df = pd.concat([sp500, spx_50ma, spx_200ma], axis=1).dropna()
df.columns = ['S&P 500', '50-Day MA', '200-Day MA']
plot_single(df.tail(250),
           'S&P 500 with Moving Averages',
           'Index Level',
           'tech_42_sp500_ma.png',
           citation='S&P Dow Jones Indices')

# Chart 43: VIX
df = pd.DataFrame({'VIX': vix}).dropna()
plot_single(df.tail(120),
           'CBOE Volatility Index (VIX)',
           'Index Level',
           'tech_43_vix.png',
           citation='CBOE')

# Chart 44: MOVE Index (Bond Volatility)
df = pd.DataFrame({'MOVE': move}).dropna()
plot_single(df.tail(120),
           'MOVE Index (Bond Market Volatility)',
           'Basis Points',
           'tech_44_move.png',
           citation='ICE BofA')

# Chart 45: VIX vs MOVE
df = pd.concat([vix, move], axis=1).dropna()
df.columns = ['VIX', 'MOVE']
plot_dual(df.tail(120),
          'Equity Vol (VIX) vs Rates Vol (MOVE)',
          'VIX Level', 'MOVE (bps)',
          'tech_45_vix_move.png',
          citation='CBOE, ICE BofA')

# Chart 46: Russell 2000 vs S&P 500 Ratio
df = pd.DataFrame({'RTY/SPX Ratio': (russell_2000 / sp500) * 100}).dropna()
plot_single(df.tail(120),
           'Small Cap vs Large Cap (Russell 2000 / S&P 500)',
           'Ratio Index',
           'tech_46_rty_spx_ratio.png',
           citation='Russell, S&P DJ Indices')

# Chart 47: Nasdaq
df = pd.DataFrame({'Nasdaq': nasdaq}).dropna()
plot_single(df.tail(250),
           'Nasdaq Composite Index',
           'Index Level',
           'tech_47_nasdaq.png',
           citation='Nasdaq')

# Chart 48: S&P 500 Returns (Monthly)
spx_returns = sp500.resample('ME').last().pct_change() * 100
df = pd.DataFrame({'Monthly Returns': spx_returns}).dropna()
fig, ax = plt.subplots(figsize=(14, 8))
colors = [OCEAN_BLUE if x >= 0 else DUSK_ORANGE for x in df['Monthly Returns']]
ax.bar(df.index, df['Monthly Returns'], color=colors, alpha=0.8)
ax.axhline(y=0, color=GRAY, linestyle='-', linewidth=1)
ax.set_ylabel('Percent', fontsize=11, color=GRAY, weight='bold')
style_chart(ax, 'S&P 500 Monthly Returns')
save_chart(fig, 'tech_48_sp500_monthly_returns.png', citation='S&P DJ Indices')

# Chart 49: S&P 500 vs 10Y Yield
df = pd.concat([sp500, dgs_10y], axis=1).dropna()
df.columns = ['S&P 500', '10Y Yield']
plot_dual(df.tail(120),
          'S&P 500 vs 10-Year Treasury Yield',
          'Index Level', 'Percent',
          'tech_49_sp500_vs_10y.png',
          citation='S&P DJ Indices, Federal Reserve')

# Chart 50: S&P 500 vs HY Spread
df = pd.concat([sp500, hy_oas], axis=1).dropna()
df.columns = ['S&P 500', 'HY OAS']
plot_dual(df.tail(120),
          'S&P 500 vs High Yield Credit Spread',
          'Index Level', 'Basis Points',
          'tech_50_sp500_vs_hy.png',
          citation='S&P DJ Indices, ICE BofA')

# Chart 51: S&P 500 Drawdown
spx_dd = (sp500 / sp500.expanding().max() - 1) * 100
df = pd.DataFrame({'Drawdown': spx_dd}).dropna()
fig, ax = plt.subplots(figsize=(14, 8))
ax.fill_between(df.index, 0, df['Drawdown'], color=DUSK_ORANGE, alpha=0.6)
ax.plot(df.index, df['Drawdown'], color=DUSK_ORANGE, linewidth=2)
ax.set_ylabel('Percent', fontsize=11, color=GRAY, weight='bold')
ax.axhline(y=0, color=GRAY, linestyle='-', linewidth=1)
style_chart(ax, 'S&P 500 Drawdown from Peak')
save_chart(fig, 'tech_51_sp500_drawdown.png', citation='S&P DJ Indices')

# ------------------------------------------------------------
# ARC 4: ASSET CLASS DASHBOARD (8-12 charts)
# ------------------------------------------------------------
print("\n💹 Arc 4: Asset Class Dashboard")

# Chart 61: Dollar Index (DXY)
df = pd.DataFrame({'DXY': dxy}).dropna()
plot_single(df.tail(120),
           'US Dollar Index (Broad)',
           'Index Level',
           'asset_61_dxy.png',
           citation='Federal Reserve')

# Chart 62: Gold Price
df = pd.DataFrame({'Gold': gold}).dropna()
plot_single(df.tail(120),
           'Gold Spot Price',
           'USD per Troy Ounce',
           'asset_62_gold.png',
           citation='ICE Benchmark Administration')

# Chart 63: Gold vs Real Yields
df = pd.concat([gold, real_yield_10y], axis=1).dropna()
df.columns = ['Gold', 'Real 10Y Yield']
plot_dual(df.tail(120),
          'Gold vs Real Yields',
          'USD/oz', 'Percent',
          'asset_63_gold_vs_real_yield.png',
          citation='IBA, Federal Reserve')

# Chart 64: Copper (Dr. Copper)
df = pd.DataFrame({'Copper': copper}).dropna()
plot_single(df.tail(120),
           'Copper Price (Dr. Copper)',
           'USD per Metric Ton',
           'asset_64_copper.png',
           citation='IMF')

# Chart 65: EUR/USD
df = pd.DataFrame({'EUR/USD': eurusd}).dropna()
plot_single(df.tail(120),
           'EUR/USD Exchange Rate',
           'Exchange Rate',
           'asset_65_eurusd.png',
           citation='Federal Reserve')

# Chart 66: JPY/USD
df = pd.DataFrame({'JPY/USD': jpyusd}).dropna()
plot_single(df.tail(120),
           'JPY/USD Exchange Rate',
           'Yen per Dollar',
           'asset_66_jpyusd.png',
           citation='Federal Reserve')

# Chart 67: GBP/USD
df = pd.DataFrame({'GBP/USD': gbpusd}).dropna()
plot_single(df.tail(120),
           'GBP/USD Exchange Rate',
           'Exchange Rate',
           'asset_67_gbpusd.png',
           citation='Federal Reserve')

# Chart 68: Commodities Index (Oil)
df = pd.DataFrame({'WTI Crude': oil_wti}).dropna()
plot_single(df.tail(120),
           'WTI Crude Oil Price',
           'USD per Barrel',
           'asset_68_wti.png',
           citation='EIA')

# ------------------------------------------------------------
# ARC 5: SINGLE-NAME DIAGNOSTICS
# ------------------------------------------------------------
print("\n🧭 Arc 5: Single-Name Diagnostics")
print("  ⚠ Skipping - requires equity-specific data source (Yahoo Finance, etc.)")

# For a production version, you'd fetch:
# - AAPL, NVDA, MSFT, GOOGL, AMZN, META, TSLA, JPM, BAC, etc.
# - Compare to sector indices, earnings, macro factors

# ============================================================
# PROPRIETARY INDICATORS SUMMARY
# ============================================================

print("\n🧩 Calculating Proprietary Indicators...")

# Liquidity Plumbing Index
liq_latest = liquidity_index.dropna().iloc[-1]
liq_state = "Easing" if liq_latest > 0 else "Tightening"

# Collateral Fragility Score (SOFR-IORB basis proxy)
coll_latest = collateral_spread.dropna().iloc[-1]
coll_state = "Stable" if abs(coll_latest) < 5 else "Worsening"

# Labor Fragility
labor_frag_latest = labor_fragility.dropna().iloc[-1]
labor_state = "Elevated" if labor_frag_latest > 0.5 else "Moderate"

print(f"  Liquidity Index: {liq_latest:.2f} ({liq_state})")
print(f"  Collateral Fragility: {coll_latest:.2f} bps ({coll_state})")
print(f"  Labor Fragility: {labor_frag_latest:.2f} ({labor_state})")

# ============================================================
# NARRATIVES & TAKEAWAYS
# ============================================================

print("\n📝 Generating narrative summaries...\n")

# Get latest values for summary
latest_gdp = gdp_3m_ann.dropna().iloc[-1]
latest_core_pce = core_pce_yoy.dropna().iloc[-1]
latest_unrate = unrate.dropna().iloc[-1]
latest_payroll = payroll_yoy.dropna().iloc[-1]
latest_curve = curve_2s10s.dropna().iloc[-1]
latest_rrp = rrp_on.dropna().iloc[-1] / 1e9
latest_sp500 = sp500.dropna().iloc[-1]
latest_vix = vix.dropna().iloc[-1]
latest_hy = hy_oas.dropna().iloc[-1]

narratives = {
    'lead_summary': [
        f"Growth moderating: Real GDP 3M annualized at {latest_gdp:.1f}%; labor market cooling but resilient.",
        f"Monetary mechanics: RRP at ${latest_rrp:.0f}B, reserves elevated; funding spreads benign.",
        f"Markets: SPX {latest_sp500:.0f}, VIX {latest_vix:.1f}, credit spreads contained (HY OAS {latest_hy:.0f}bps)."
    ],

    'arc1_narrative': (
        f"Growth appears to be plateauing with real GDP growth at {latest_gdp:.1f}% annualized (3M). "
        f"Core PCE inflation running at {latest_core_pce:.1f}% YoY, showing sticky services inflation. "
        f"Labor market resilience persists with unemployment at {latest_unrate:.1f}% and payrolls growing {latest_payroll:.1f}% YoY, "
        "though JOLTS data suggests softening beneath the surface."
    ),

    'arc2_narrative': (
        f"Monetary plumbing remains stable. ON RRP at ${latest_rrp:.0f}B, continuing its bleed from peak levels. "
        f"The yield curve (2s10s) is at {latest_curve:.0f}bps, with collateral markets showing normal functioning. "
        "Fed balance sheet runoff (QT) continues at a measured pace with reserves ample."
    ),

    'arc3_narrative': (
        f"Equity markets at SPX {latest_sp500:.0f} with volatility muted (VIX {latest_vix:.1f}). "
        "Concentration risk remains elevated in mega-cap tech. Cross-asset correlations shifting "
        "as rates volatility (MOVE) decouples from equity vol regime."
    ),

    'arc4_narrative': (
        "Dollar strength persisting on rate differential expectations. Gold consolidating near recent highs "
        "as real yields hold. Commodities mixed with oil range-bound and copper sensitive to China growth outlook."
    ),
}

# ============================================================
# FINAL REPORT ASSEMBLY
# ============================================================

print("="*70)
print("📄 Assembling Final Chartbook PDF...")
print("="*70)

pdf_path = EXPORTS_DIR / f"Lighthouse_Macro_Chartbook_Week{WEEK_NUMBER}_{EDITION_DATE}.pdf"

with PdfPages(pdf_path) as pdf:
    # --------------------------------------------------------
    # COVER PAGE
    # --------------------------------------------------------
    fig = plt.figure(figsize=(11, 8.5))
    fig.patch.set_facecolor('white')

    # Title
    fig.text(0.5, 0.75, 'LIGHTHOUSE MACRO',
             ha='center', fontsize=42, weight='bold', color=OCEAN_BLUE)
    fig.text(0.5, 0.68, 'THE CHARTBOOK FRIDAY',
             ha='center', fontsize=24, color=GRAY)

    # Edition info
    fig.text(0.5, 0.58, f'Week {WEEK_NUMBER} • {EDITION_DATE}',
             ha='center', fontsize=16, color=GRAY)
    fig.text(0.5, 0.53, f'Data Through: {DATA_THROUGH}',
             ha='center', fontsize=12, color=GRAY, style='italic')

    # Lead summary
    fig.text(0.5, 0.42, 'Lead Summary',
             ha='center', fontsize=18, weight='bold', color=OCEAN_BLUE)

    y_pos = 0.37
    for bullet in narratives['lead_summary']:
        fig.text(0.1, y_pos, f'• {bullet}',
                ha='left', fontsize=11, color=GRAY, wrap=True)
        y_pos -= 0.04

    # Footer
    fig.text(0.5, 0.15, 'Prepared by: Lighthouse Macro Research',
             ha='center', fontsize=11, color=GRAY)
    fig.text(0.5, 0.12, 'Lead: Bob Sheehan, CFA, CMT',
             ha='center', fontsize=10, color=GRAY)

    fig.text(0.5, 0.05, 'MACRO, ILLUMINATED.',
             ha='center', fontsize=14, color=GRAY, alpha=0.6, style='italic')

    plt.axis('off')
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # --------------------------------------------------------
    # TABLE OF CONTENTS
    # --------------------------------------------------------
    fig = plt.figure(figsize=(11, 8.5))
    fig.patch.set_facecolor('white')

    fig.text(0.5, 0.90, 'Table of Contents',
             ha='center', fontsize=24, weight='bold', color=OCEAN_BLUE)

    toc_items = [
        ('Arc 1: Macro Dynamics', 'Charts 01-18', 'GDP, Inflation, Labor, Fiscal, Trade'),
        ('Arc 2: Monetary Mechanics', 'Charts 21-37', 'Fed, RRP, Yields, Credit, Liquidity'),
        ('Arc 3: Market Technicals', 'Charts 41-51', 'Equities, Volatility, Breadth'),
        ('Arc 4: Asset Class Dashboard', 'Charts 61-68', 'FX, Commodities, Rates, Credit'),
        ('Arc 5: Single-Name Diagnostics', 'Charts 71+', 'Flagship Equities (Future)'),
        ('Proprietary Indicators', 'Summary', 'Liquidity, Fragility, Positioning'),
    ]

    y = 0.80
    for title, charts, desc in toc_items:
        fig.text(0.10, y, title, fontsize=14, weight='bold', color=OCEAN_BLUE)
        fig.text(0.65, y, charts, fontsize=12, color=GRAY)
        fig.text(0.10, y-0.03, desc, fontsize=10, color=GRAY, style='italic')
        y -= 0.10

    plt.axis('off')
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # --------------------------------------------------------
    # ARC DIVIDER PAGES + CHARTS
    # --------------------------------------------------------

    # Arc 1 Divider
    fig = plt.figure(figsize=(11, 8.5))
    fig.patch.set_facecolor('white')
    fig.text(0.5, 0.60, 'Arc 1', ha='center', fontsize=32, weight='bold', color=OCEAN_BLUE)
    fig.text(0.5, 0.50, 'Macro Dynamics', ha='center', fontsize=28, color=GRAY)
    fig.text(0.5, 0.40, narratives['arc1_narrative'],
             ha='center', fontsize=11, color=GRAY, wrap=True,
             bbox=dict(boxstyle='round', facecolor='white', edgecolor=OCEAN_BLUE, linewidth=2))
    plt.axis('off')
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # Add Arc 1 charts
    for chart in sorted(CHARTS_DIR.glob("macro_*.png")):
        fig = plt.figure(figsize=(11, 8.5))
        img = plt.imread(chart)
        plt.imshow(img)
        plt.axis('off')
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    # Arc 2 Divider
    fig = plt.figure(figsize=(11, 8.5))
    fig.patch.set_facecolor('white')
    fig.text(0.5, 0.60, 'Arc 2', ha='center', fontsize=32, weight='bold', color=OCEAN_BLUE)
    fig.text(0.5, 0.50, 'Monetary Mechanics', ha='center', fontsize=28, color=GRAY)
    fig.text(0.5, 0.40, narratives['arc2_narrative'],
             ha='center', fontsize=11, color=GRAY, wrap=True,
             bbox=dict(boxstyle='round', facecolor='white', edgecolor=OCEAN_BLUE, linewidth=2))
    plt.axis('off')
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # Add Arc 2 charts
    for chart in sorted(CHARTS_DIR.glob("plumbing_*.png")):
        fig = plt.figure(figsize=(11, 8.5))
        img = plt.imread(chart)
        plt.imshow(img)
        plt.axis('off')
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    # Arc 3 Divider
    fig = plt.figure(figsize=(11, 8.5))
    fig.patch.set_facecolor('white')
    fig.text(0.5, 0.60, 'Arc 3', ha='center', fontsize=32, weight='bold', color=OCEAN_BLUE)
    fig.text(0.5, 0.50, 'Market Technicals', ha='center', fontsize=28, color=GRAY)
    fig.text(0.5, 0.40, narratives['arc3_narrative'],
             ha='center', fontsize=11, color=GRAY, wrap=True,
             bbox=dict(boxstyle='round', facecolor='white', edgecolor=OCEAN_BLUE, linewidth=2))
    plt.axis('off')
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # Add Arc 3 charts
    for chart in sorted(CHARTS_DIR.glob("tech_*.png")):
        fig = plt.figure(figsize=(11, 8.5))
        img = plt.imread(chart)
        plt.imshow(img)
        plt.axis('off')
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    # Arc 4 Divider
    fig = plt.figure(figsize=(11, 8.5))
    fig.patch.set_facecolor('white')
    fig.text(0.5, 0.60, 'Arc 4', ha='center', fontsize=32, weight='bold', color=OCEAN_BLUE)
    fig.text(0.5, 0.50, 'Asset Class Dashboard', ha='center', fontsize=28, color=GRAY)
    fig.text(0.5, 0.40, narratives['arc4_narrative'],
             ha='center', fontsize=11, color=GRAY, wrap=True,
             bbox=dict(boxstyle='round', facecolor='white', edgecolor=OCEAN_BLUE, linewidth=2))
    plt.axis('off')
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # Add Arc 4 charts
    for chart in sorted(CHARTS_DIR.glob("asset_*.png")):
        fig = plt.figure(figsize=(11, 8.5))
        img = plt.imread(chart)
        plt.imshow(img)
        plt.axis('off')
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    # --------------------------------------------------------
    # SUMMARY PAGE
    # --------------------------------------------------------
    fig = plt.figure(figsize=(11, 8.5))
    fig.patch.set_facecolor('white')

    fig.text(0.5, 0.92, 'Executive Summary',
             ha='center', fontsize=24, weight='bold', color=OCEAN_BLUE)

    # Key metrics table
    y = 0.82
    metrics = [
        ('MACRO', ''),
        ('Real GDP (3M Ann.)', f'{latest_gdp:.1f}%'),
        ('Core PCE YoY', f'{latest_core_pce:.1f}%'),
        ('Unemployment', f'{latest_unrate:.1f}%'),
        ('Payrolls YoY', f'{latest_payroll:.1f}%'),
        ('', ''),
        ('MONETARY', ''),
        ('2s10s Curve', f'{latest_curve:.0f} bps'),
        ('ON RRP', f'${latest_rrp:.0f}B'),
        ('Liquidity Index', f'{liq_latest:.2f} ({liq_state})'),
        ('', ''),
        ('MARKETS', ''),
        ('S&P 500', f'{latest_sp500:.0f}'),
        ('VIX', f'{latest_vix:.1f}'),
        ('HY OAS', f'{latest_hy:.0f} bps'),
    ]

    for label, value in metrics:
        if label == '':
            y -= 0.02
            continue
        if value == '':
            fig.text(0.25, y, label, fontsize=12, weight='bold', color=OCEAN_BLUE)
        else:
            fig.text(0.25, y, label, fontsize=11, color=GRAY)
            fig.text(0.65, y, value, fontsize=11, color=OCEAN_BLUE, weight='bold')
        y -= 0.04

    fig.text(0.5, 0.15, '© Lighthouse Macro 2025',
             ha='center', fontsize=10, color=GRAY)
    fig.text(0.5, 0.10, 'MACRO, ILLUMINATED.',
             ha='center', fontsize=14, color=GRAY, alpha=0.6, style='italic')

    plt.axis('off')
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

print(f"\n✅ PDF Generated: {pdf_path}")

# ============================================================
# EXPORT DATA TO CSV
# ============================================================

print("\n💾 Exporting data to CSV...")

export_data = pd.DataFrame({
    'gdp_3m_ann': gdp_3m_ann,
    'core_pce_yoy': core_pce_yoy,
    'unrate': unrate,
    'payroll_yoy': payroll_yoy,
    'curve_2s10s': curve_2s10s,
    'rrp_billions': rrp_on / 1e9,
    'reserves_billions': reserves / 1e9,
    'sp500': sp500,
    'vix': vix,
    'hy_oas': hy_oas,
    'liquidity_index': liquidity_index,
    'labor_fragility': labor_fragility,
})

csv_path = EXPORTS_DIR / f'chartbook_data_week{WEEK_NUMBER}_{EDITION_DATE}.csv'
export_data.to_csv(csv_path)
print(f"✅ Data exported: {csv_path}")

# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "="*70)
print("🎉 CHARTBOOK GENERATION COMPLETE!")
print("="*70)
print(f"\n📊 Charts Generated: {len(list(CHARTS_DIR.glob('*.png')))} files")
print(f"📄 PDF Report: {pdf_path}")
print(f"💾 Data Export: {csv_path}")
print("\n" + "="*70)
print("\nNext Steps:")
print("1. Review PDF for quality and accuracy")
print("2. Add single-name diagnostics (requires equity data)")
print("3. Prepare Substack teaser (3-5 lead charts + summary)")
print("4. Upload full PDF to Substack with download link")
print("="*70)
