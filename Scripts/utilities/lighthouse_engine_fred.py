import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fredapi import Fred
import os

class LighthouseDataEngine:
    """
    Core ETL and Indicator Engine for Lighthouse Macro.
    Implements the 6-factor Macro Risk Index (MRI) and sub-indices.
    Now powered by FRED real data.
    """

    # FRED Series IDs
    FRED_SERIES = {
        'quits_rate': 'JTSQUR',           # Quits Rate (%)
        'lt_unemp_pct': 'LNS13025703',    # % of Unemployed > 27 weeks (share of labor force)
        'hires_rate': 'JTSHIR',           # Hires Rate (%)
        'on_rrp': 'RRPONTSYD',            # ON RRP ($B)
        'reserves': 'WRESBAL',            # Reserve Balances ($B)
        'gdp': 'GDP',                     # Nominal GDP ($B, quarterly)
        'sofr': 'SOFR',                   # SOFR rate
        'effr': 'EFFR',                   # Effective Fed Funds Rate
        'dgs10': 'DGS10',                 # 10Y Treasury
        'dgs3mo': 'DGS3MO',               # 3M Treasury
        'hy_oas': 'BAMLH0A0HYM2',         # ICE BofA HY OAS
        'sp500': 'SP500',                 # S&P 500
    }

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('FRED_API_KEY')
        if not self.api_key:
            raise ValueError("FRED_API_KEY required")
        self.fred = Fred(api_key=self.api_key)
        self.raw_data = pd.DataFrame()
        self.indicators = pd.DataFrame()

    def fetch_fred_data(self, start_date='2018-01-01'):
        """
        Fetches all required series from FRED.
        """
        print("Fetching data from FRED...")
        data = {}

        for name, series_id in self.FRED_SERIES.items():
            try:
                data[name] = self.fred.get_series(series_id, observation_start=start_date)
                print(f"  ✓ {name} ({series_id})")
            except Exception as e:
                print(f"  ✗ {name} ({series_id}): {e}")
                data[name] = pd.Series(dtype=float)

        # Combine into DataFrame
        df = pd.DataFrame(data)

        # Resample everything to daily, forward-fill
        df = df.resample('D').last().ffill()

        # Compute derived series
        # Hires/Quits ratio
        df['hires_quits_ratio'] = df['hires_rate'] / df['quits_rate']

        # RRP and Reserves as % of GDP (quarterly GDP interpolated)
        df['gdp_interp'] = df['gdp'].interpolate(method='linear')
        df['on_rrp_gdp'] = (df['on_rrp'] / df['gdp_interp']) * 100
        df['reserves_gdp'] = (df['reserves'] / 1000 / df['gdp_interp']) * 100  # reserves in $M

        # SOFR-EFFR spread (bps)
        df['sofr_effr'] = (df['sofr'] - df['effr']) * 100

        # HY OAS comes in % from FRED, convert to bps
        df['hy_oas'] = df['hy_oas'] * 100

        # Yield curve 10Y-3M
        df['curve_10y3m'] = df['dgs10'] - df['dgs3mo']

        # S&P 500 technicals
        df['sp500_200dma'] = df['sp500'].rolling(200).mean()
        df['sp500_vol'] = df['sp500'].pct_change().rolling(60).std() * np.sqrt(252) * 100

        self.raw_data = df.dropna(subset=['quits_rate', 'hy_oas', 'sp500'])
        print(f"\nData range: {self.raw_data.index.min().strftime('%Y-%m-%d')} to {self.raw_data.index.max().strftime('%Y-%m-%d')}")
        print(f"Rows: {len(self.raw_data)}")

        return self.raw_data

    def z_score(self, series, window=252):
        """Computes rolling z-score for standardization (1-year lookback)."""
        return (series - series.rolling(window).mean()) / series.rolling(window).std()

    def compute_indicators(self):
        """
        Computes the proprietary indices.
        """
        df = self.raw_data.copy()

        # --- 1. Labor Fragility Index (LFI) ---
        df['z_lt_unemp'] = self.z_score(df['lt_unemp_pct'])
        df['z_neg_quits'] = self.z_score(-df['quits_rate'])
        df['z_neg_hq'] = self.z_score(-df['hires_quits_ratio'])

        df['LFI'] = (df['z_lt_unemp'] + df['z_neg_quits'] + df['z_neg_hq']) / 3

        # --- 2. Liquidity Cushion Index (LCI) ---
        df['z_rrp'] = self.z_score(df['on_rrp_gdp'])
        df['z_reserves'] = self.z_score(df['reserves_gdp'])

        df['LCI'] = (df['z_rrp'] + df['z_reserves']) / 2

        # --- 3. Yield-Funding Stress (YFS) ---
        df['z_neg_curve'] = self.z_score(-df['curve_10y3m'])
        df['z_funding'] = self.z_score(df['sofr_effr'])

        df['YFS'] = (df['z_neg_curve'] + df['z_funding']) / 2

        # --- 4. Equity Momentum Divergence (EMD) ---
        df['dist_from_trend'] = (df['sp500'] - df['sp500_200dma']) / df['sp500_200dma'] * 100
        df['EMD'] = self.z_score(df['dist_from_trend'])

        # --- 5. Labor Dynamism Index (LDI) ---
        df['LDI'] = self.z_score(df['quits_rate'])

        # --- 6. Credit-Labor Gap (CLG) ---
        df['z_hy_oas'] = self.z_score(df['hy_oas'])
        df['CLG'] = df['z_hy_oas'] - df['LFI']

        # --- 7. Macro Risk Index (MRI) ---
        df['MRI'] = (
            df['LFI'] +
            (-df['LDI']) +
            df['YFS'] +
            df['z_hy_oas'] +
            df['EMD'] +
            (-df['LCI'])
        ) / 6

        self.indicators = df
        return df

    def get_regime(self, mri_value):
        if pd.isna(mri_value): return "Insufficient Data"
        if mri_value < -1.0: return "LOW RISK"
        if mri_value < 0.0: return "MODERATE RISK"
        if mri_value < 1.0: return "ELEVATED RISK"
        return "HIGH RISK"

    def print_dashboard(self):
        """Print current system status."""
        latest = self.indicators.iloc[-1]

        print("\n" + "="*50)
        print("LIGHTHOUSE MACRO | SYSTEM STATUS (LIVE FRED DATA)")
        print(f"Date: {latest.name.strftime('%Y-%m-%d')}")
        print("="*50)

        mri = latest['MRI']
        print(f"\n>>> MACRO RISK INDEX (MRI): {mri:.2f}")
        print(f">>> REGIME: {self.get_regime(mri)}")

        print("\n--- COMPONENT BREAKDOWN (Z-Scores) ---")
        print(f"Labor Fragility (LFI):     {latest['LFI']:+.2f}  (High = Stress)")
        print(f"Labor Dynamism (LDI):      {latest['LDI']:+.2f}  (Low = Weak)")
        print(f"Liquidity Cushion (LCI):   {latest['LCI']:+.2f}  (Low = Stress)")
        print(f"Yield/Funding (YFS):       {latest['YFS']:+.2f}")
        print(f"Equity Momentum (EMD):     {latest['EMD']:+.2f}")
        print(f"Credit Stress (HY OAS z):  {latest['z_hy_oas']:+.2f}")

        print(f"\n--- CREDIT-LABOR GAP (CLG) ---")
        clg = latest['CLG']
        print(f"CLG: {clg:+.2f}", end="")
        if clg < -0.5:
            print("  ⚠️  Spreads too tight for labor reality")
        elif clg > 0.5:
            print("  Spreads pricing in labor weakness")
        else:
            print("  Aligned")

        print("\n--- RAW INPUTS (Latest) ---")
        print(f"Quits Rate:        {latest['quits_rate']:.1f}%")
        print(f"Hires/Quits:       {latest['hires_quits_ratio']:.2f}")
        print(f"LT Unemp Share:    {latest['lt_unemp_pct']:.1f}%")
        print(f"ON RRP/GDP:        {latest['on_rrp_gdp']:.2f}%")
        print(f"Reserves/GDP:      {latest['reserves_gdp']:.2f}%")
        print(f"HY OAS:            {latest['hy_oas']:.0f} bps")
        print(f"10Y-3M Curve:      {latest['curve_10y3m']:.2f}%")
        print(f"SOFR-EFFR:         {latest['sofr_effr']:.1f} bps")
        print(f"S&P 500:           {latest['sp500']:,.0f}")
        print(f"S&P vs 200DMA:     {latest['dist_from_trend']:+.1f}%")
        print("="*50)


# --- Execution ---
if __name__ == "__main__":
    engine = LighthouseDataEngine()
    engine.fetch_fred_data(start_date='2018-01-01')
    engine.compute_indicators()
    engine.print_dashboard()
