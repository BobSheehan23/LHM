import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class LighthouseDataEngine:
    """
    Core ETL and Indicator Engine for Lighthouse Macro.
    Implements the 6-factor Macro Risk Index (MRI) and sub-indices.
    """

    def __init__(self):
        self.raw_data = pd.DataFrame()
        self.indicators = pd.DataFrame()

    def generate_synthetic_data(self, days=365):
        """
        Generates synthetic data mirroring the 'Late 2025' scenario
        described in the architecture to demonstrate indicator logic.
        """
        dates = pd.date_range(end=datetime.today(), periods=days)

        # 1. Labor Data (Deteriorating)
        # Quits rate trending down to 1.9%
        quits = np.linspace(2.4, 1.9, days) + np.random.normal(0, 0.05, days)
        # Long-term unemp trending up to 25.7%
        lt_unemp = np.linspace(18, 25.7, days) + np.random.normal(0, 0.5, days)
        # Hires/Quits ratio trending up (loosening)
        hires_quits = np.linspace(1.4, 1.85, days) + np.random.normal(0, 0.05, days)

        # 2. Monetary/Plumbing (Stress Building)
        # ON RRP draining to exhaustion (~$100B)
        on_rrp_gdp = np.linspace(8.0, 0.4, days)  # % of GDP
        # Reserves draining
        reserves_gdp = np.linspace(14.0, 12.5, days)
        # SOFR-EFFR spread widening slightly
        sofr_effr = np.linspace(2, 10, days) + np.random.normal(0, 1, days)
        # Curve inversion (10Y-3M)
        curve = np.linspace(-1.5, -0.5, days) # Basis points/100

        # 3. Market/Credit (Complacent to Late Cycle)
        # HY OAS (Tight)
        hy_oas = np.linspace(400, 310, days) + np.random.normal(0, 10, days)
        # S&P 500 Price (Trending up but momentum waning)
        sp500 = np.linspace(4500, 5800, days) + np.random.normal(0, 50, days)

        self.raw_data = pd.DataFrame({
            'date': dates,
            'quits_rate': quits,
            'lt_unemp_pct': lt_unemp,
            'hires_quits_ratio': hires_quits,
            'on_rrp_gdp': on_rrp_gdp,
            'reserves_gdp': reserves_gdp,
            'sofr_effr': sofr_effr,
            'curve_10y3m': curve,
            'hy_oas': hy_oas,
            'sp500': sp500
        }).set_index('date')

        # Calculate 200DMA for Market Techs
        self.raw_data['sp500_200dma'] = self.raw_data['sp500'].rolling(200).mean()
        self.raw_data['sp500_vol'] = self.raw_data['sp500'].rolling(60).std()

    def z_score(self, series, window=365):
        """Computes rolling z-score for standardization."""
        return (series - series.rolling(window).mean()) / series.rolling(window).std()

    def compute_indicators(self):
        """
        Computes the proprietary indices based on Part IV of the architecture.
        """
        df = self.raw_data.copy()

        # --- 1. Labor Fragility Index (LFI) ---
        # Avg z-scores of: LT Unemp (bad), -Quits (low is bad), -Hires/Quits (low ratio is bad? Text says low hires/quits = tight, high = loose.
        # Text Logic: "low hires/quits ratio... when quits fall faster than hires -> loosening".
        # Let's follow the formula explicitly: z(LT Unemp), z(-Quits), z(-Hires/Quits)

        df['z_lt_unemp'] = self.z_score(df['lt_unemp_pct'])
        df['z_neg_quits'] = self.z_score(-df['quits_rate'])
        df['z_neg_hq'] = self.z_score(-df['hires_quits_ratio']) # Text implies fragility increases as market loosens/deteriorates

        df['LFI'] = (df['z_lt_unemp'] + df['z_neg_quits'] + df['z_neg_hq']) / 3

        # --- 2. Liquidity Cushion Index (LCI) ---
        # Avg z-scores of: RRP/GDP, Reserves/GDP
        df['z_rrp'] = self.z_score(df['on_rrp_gdp'])
        df['z_reserves'] = self.z_score(df['reserves_gdp'])

        df['LCI'] = (df['z_rrp'] + df['z_reserves']) / 2

        # --- 3. Yield-Funding Stress (YFS) ---
        # Avg z-scores: -Curve (inversion is stress), SOFR-EFFR (widening is stress)
        df['z_neg_curve'] = self.z_score(-df['curve_10y3m'])
        df['z_funding'] = self.z_score(df['sofr_effr'])

        df['YFS'] = (df['z_neg_curve'] + df['z_funding']) / 2

        # --- 4. Equity Momentum Divergence (EMD) ---
        # Price vs Trend, vol adjusted
        df['dist_from_trend'] = (df['sp500'] - df['sp500_200dma']) / df['sp500_vol']
        df['EMD'] = self.z_score(df['dist_from_trend'])

        # --- 5. Labor Dynamism Index (LDI) ---
        # Proxy: Z(Quits)
        df['LDI'] = self.z_score(df['quits_rate'])

        # --- 6. Macro Risk Index (MRI) ---
        # MRI = (LFI + (-LDI) + YFS + z(HY_OAS) + EMD + (-LCI)) / 6
        df['z_hy_oas'] = self.z_score(df['hy_oas'])

        df['MRI'] = (
            df['LFI'] +
            (-df['LDI']) +
            df['YFS'] +
            df['z_hy_oas'] +
            df['EMD'] +
            (-df['LCI'])
        ) / 6

        self.indicators = df
        return df.iloc[-1]

    def get_regime(self, mri_value):
        if mri_value < -1.0: return "Low Risk"
        if mri_value < 0.0: return "Moderate Risk"
        if mri_value < 1.0: return "Elevated Risk"
        return "High Risk"

# --- Execution ---
if __name__ == "__main__":
    engine = LighthouseDataEngine()
    engine.generate_synthetic_data()
    current_metrics = engine.compute_indicators()

    print("\n" + "="*40)
    print("LIGHTHOUSE MACRO | SYSTEM STATUS")
    print(f"Date: {current_metrics.name.strftime('%Y-%m-%d')}")
    print("="*40)

    print(f"\nMACRO RISK INDEX (MRI): {current_metrics['MRI']:.2f}")
    print(f"REGIME: {engine.get_regime(current_metrics['MRI'])}")

    print("\n--- COMPONENT BREAKDOWN (Z-Scores) ---")
    print(f"Labor Fragility (LFI):    {current_metrics['LFI']:.2f} (High = Stress)")
    print(f"Liquidity Cushion (LCI):  {current_metrics['LCI']:.2f} (Low = Stress)")
    print(f"Yield/Funding (YFS):      {current_metrics['YFS']:.2f}")
    print(f"Credit Stress (HY OAS):   {current_metrics['z_hy_oas']:.2f}")

    print("\n--- RAW INPUTS ---")
    print(f"Quits Rate:      {engine.raw_data['quits_rate'].iloc[-1]:.2f}%")
    print(f"ON RRP/GDP:      {engine.raw_data['on_rrp_gdp'].iloc[-1]:.2f}%")
    print(f"HY OAS:          {engine.raw_data['hy_oas'].iloc[-1]:.0f} bps")
    print("="*40)
