"""
LIGHTHOUSE MACRO - PROPRIETARY INDICATORS CALCULATOR
Computes all 29 custom indices from master dataset

Input: chartbook_master_data.csv
Output: proprietary_indicators.csv (daily values for all custom metrics)

Author: Bob Sheehan, CFA, CMT
Date: November 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ProprietaryIndicatorEngine:
    """Calculate all Lighthouse Macro proprietary indicators"""

    def __init__(self, master_data_path='chartbook_master_data.csv'):
        """Load master dataset"""
        print("=" * 70)
        print("LIGHTHOUSE MACRO - PROPRIETARY INDICATORS CALCULATOR")
        print("=" * 70)

        print(f"\n📊 Loading master dataset: {master_data_path}")
        self.df = pd.read_csv(master_data_path, index_col=0, parse_dates=True)

        # Forward fill to handle different frequencies
        self.df = self.df.fillna(method='ffill')

        print(f"✓ Loaded {len(self.df)} rows × {len(self.df.columns)} columns")
        print(f"  Date range: {self.df.index.min()} to {self.df.index.max()}")

        # Store calculated indicators
        self.indicators = pd.DataFrame(index=self.df.index)

    def calculate_zscore(self, series, window=252, min_periods=30):
        """Calculate rolling z-score"""
        rolling_mean = series.rolling(window=window, min_periods=min_periods).mean()
        rolling_std = series.rolling(window=window, min_periods=min_periods).std()
        zscore = (series - rolling_mean) / rolling_std
        return zscore

    def calculate_yoy_change(self, series, periods=252):
        """Calculate year-over-year percentage change"""
        return series.pct_change(periods=periods) * 100

    # ==================== SECTION 1: LIQUIDITY INDICATORS ====================

    def liquidity_cushion_index(self):
        """
        Liquidity Cushion Index (LCI)
        Formula: z(RRP/GDP) + z(Reserves/GDP) / 2
        """
        print("\n📊 Calculating Liquidity Cushion Index (LCI)...")

        # Calculate ratios
        rrp_gdp = self.df['RRP'] / self.df['GDP']
        reserves_gdp = self.df['Bank_Reserves'] / self.df['GDP']

        # Z-score each component
        z_rrp = self.calculate_zscore(rrp_gdp)
        z_reserves = self.calculate_zscore(reserves_gdp)

        # Average
        lci = (z_rrp + z_reserves) / 2

        self.indicators['LCI'] = lci
        self.indicators['LCI_RRP_Component'] = z_rrp
        self.indicators['LCI_Reserves_Component'] = z_reserves

        latest = lci.dropna().iloc[-1] if len(lci.dropna()) > 0 else np.nan
        print(f"  ✓ LCI calculated. Latest value: {latest:.2f}σ")

        return lci

    def yield_funding_stress(self):
        """
        Yield-Funding Stress (YFS)
        Formula: z(10Y-2Y) + z(10Y-3M) [+ z(BGCR-EFFR)] / 3
        Note: BGCR component optional if data unavailable
        """
        print("\n📊 Calculating Yield-Funding Stress (YFS)...")

        # Z-score components
        z_10y2y = self.calculate_zscore(self.df['Yield_Curve_10Y2Y'])
        z_10y3m = self.calculate_zscore(self.df['Yield_Curve_10Y3M'])

        # Average (BGCR not available in current dataset)
        yfs = (z_10y2y + z_10y3m) / 2

        self.indicators['YFS'] = yfs
        self.indicators['YFS_10Y2Y_Component'] = z_10y2y
        self.indicators['YFS_10Y3M_Component'] = z_10y3m

        latest = yfs.dropna().iloc[-1] if len(yfs.dropna()) > 0 else np.nan
        print(f"  ✓ YFS calculated. Latest value: {latest:.2f}σ")
        print(f"  ⚠ Note: BGCR-EFFR component not available (requires NY Fed data)")

        return yfs

    def bill_sofr_spread(self):
        """
        3M Bill-SOFR Spread
        Formula: UST_3M - SOFR
        """
        print("\n📊 Calculating 3M Bill-SOFR Spread...")

        spread = self.df['UST_3M'] - self.df['SOFR']

        self.indicators['Bill_SOFR_Spread'] = spread

        latest = spread.dropna().iloc[-1] if len(spread.dropna()) > 0 else np.nan
        print(f"  ✓ Bill-SOFR Spread calculated. Latest value: {latest:.2f} bps")

        return spread

    # ==================== SECTION 2: LABOR INDICATORS ====================

    def labor_fragility_index(self):
        """
        Labor Fragility Index (LFI)
        Formula: z(Unemployed_27_Weeks%) + z(-Quits) + z(-Hires/Quits) / 3
        """
        print("\n📊 Calculating Labor Fragility Index (LFI)...")

        # Calculate components
        # Long-duration unemployment already in dataset
        long_unemploy = self.df['Unemployed_27_Weeks']

        # Quits rate (inverted - higher quits = healthier = lower fragility)
        quits = -self.df['Quits']

        # Hires-to-quits ratio (inverted)
        hires_quits = -(self.df['Hires'] / self.df['Quits'])

        # Z-score each
        z_long_unemploy = self.calculate_zscore(long_unemploy)
        z_quits = self.calculate_zscore(quits)
        z_hires_quits = self.calculate_zscore(hires_quits)

        # Average
        lfi = (z_long_unemploy + z_quits + z_hires_quits) / 3

        self.indicators['LFI'] = lfi
        self.indicators['LFI_LongUnemployment'] = z_long_unemploy
        self.indicators['LFI_Quits'] = z_quits
        self.indicators['LFI_HiresQuits'] = z_hires_quits

        latest = lfi.dropna().iloc[-1] if len(lfi.dropna()) > 0 else np.nan
        print(f"  ✓ LFI calculated. Latest value: {latest:.2f}σ")

        return lfi

    def labor_dynamism_index(self):
        """
        Labor Dynamism Index (LDI)
        Formula: z(Quits) + z(Hires/Quits) + z(Quits/Layoffs) / 3
        """
        print("\n📊 Calculating Labor Dynamism Index (LDI)...")

        # Calculate components
        quits = self.df['Quits']
        hires_quits = self.df['Hires'] / self.df['Quits']
        quits_layoffs = self.df['Quits'] / self.df['Layoffs']

        # Z-score each
        z_quits = self.calculate_zscore(quits)
        z_hires_quits = self.calculate_zscore(hires_quits)
        z_quits_layoffs = self.calculate_zscore(quits_layoffs)

        # Average
        ldi = (z_quits + z_hires_quits + z_quits_layoffs) / 3

        self.indicators['LDI'] = ldi
        self.indicators['LDI_Quits'] = z_quits
        self.indicators['LDI_HiresQuits'] = z_hires_quits
        self.indicators['LDI_QuitsLayoffs'] = z_quits_layoffs

        latest = ldi.dropna().iloc[-1] if len(ldi.dropna()) > 0 else np.nan
        print(f"  ✓ LDI calculated. Latest value: {latest:.2f}σ")

        return ldi

    # ==================== SECTION 3: CREDIT INDICATORS ====================

    def credit_labor_gap(self, lfi=None):
        """
        Credit-Labor Gap (CLG)
        Formula: z(HY_OAS) - z(LFI)
        """
        print("\n📊 Calculating Credit-Labor Gap (CLG)...")

        # Use pre-calculated LFI or calculate if not provided
        if lfi is None:
            lfi = self.indicators.get('LFI')
            if lfi is None:
                lfi = self.labor_fragility_index()

        # Z-score HY OAS
        z_hy = self.calculate_zscore(self.df['HY_OAS'])
        z_lfi = self.calculate_zscore(lfi)

        # Calculate gap
        clg = z_hy - z_lfi

        self.indicators['CLG'] = clg
        self.indicators['CLG_HY_Component'] = z_hy
        self.indicators['CLG_LFI_Component'] = z_lfi

        latest = clg.dropna().iloc[-1] if len(clg.dropna()) > 0 else np.nan
        print(f"  ✓ CLG calculated. Latest value: {latest:.2f}σ")
        if latest < 0:
            print(f"  ⚠ WARNING: Negative CLG = Spreads too tight given labor stress!")

        return clg

    def spread_volatility_imbalance(self):
        """
        Spread-Volatility Imbalance (SVI)
        Formula: z(HY_OAS_level) / z(HY_OAS_volatility)
        """
        print("\n📊 Calculating Spread-Volatility Imbalance (SVI)...")

        # HY OAS level
        hy_level = self.df['HY_OAS']

        # Calculate 30-day realized volatility of HY OAS
        hy_volatility = hy_level.rolling(window=30).std()

        # Z-score both
        z_level = self.calculate_zscore(hy_level)
        z_vol = self.calculate_zscore(hy_volatility)

        # Ratio (avoiding division by zero)
        svi = z_level / z_vol.replace(0, np.nan)

        self.indicators['SVI'] = svi
        self.indicators['SVI_Level_Component'] = z_level
        self.indicators['SVI_Volatility_Component'] = z_vol
        self.indicators['HY_OAS_Realized_Vol'] = hy_volatility

        latest = svi.dropna().iloc[-1] if len(svi.dropna()) > 0 else np.nan
        print(f"  ✓ SVI calculated. Latest value: {latest:.2f}")

        return svi

    # ==================== SECTION 4: EQUITY INDICATORS ====================

    def equity_momentum_divergence(self):
        """
        Equity Momentum Divergence (EMD)
        Formula: z((SP500 - MA200) / Realized_Vol)
        """
        print("\n📊 Calculating Equity Momentum Divergence (EMD)...")

        # Calculate 200-day moving average
        sp500 = self.df['SP500']
        ma200 = sp500.rolling(window=200).mean()

        # Price deviation from trend
        price_deviation = sp500 - ma200

        # Realized volatility (use VIX as proxy, or calculate 30-day realized vol)
        realized_vol = sp500.pct_change().rolling(window=30).std() * np.sqrt(252) * 100
        # Alternative: use VIX directly
        # realized_vol = self.df['VIX']

        # Normalize by volatility
        momentum_ratio = price_deviation / realized_vol.replace(0, np.nan)

        # Z-score
        emd = self.calculate_zscore(momentum_ratio)

        self.indicators['EMD'] = emd
        self.indicators['EMD_Price_Deviation'] = price_deviation
        self.indicators['EMD_Realized_Vol'] = realized_vol
        self.indicators['SP500_MA200'] = ma200

        latest = emd.dropna().iloc[-1] if len(emd.dropna()) > 0 else np.nan
        print(f"  ✓ EMD calculated. Latest value: {latest:.2f}σ")
        if latest > 1:
            print(f"  ⚠ WARNING: EMD >+1σ = Stretched momentum, thin shock absorption!")

        return emd

    # ==================== SECTION 5: MASTER COMPOSITE ====================

    def macro_risk_index(self, lfi=None, ldi=None, yfs=None, emd=None, lci=None):
        """
        Macro Risk Index (MRI) - FLAGSHIP COMPOSITE
        Formula: LFI - LDI + YFS + z(HY_OAS) + EMD - LCI
        """
        print("\n" + "=" * 70)
        print("📊 CALCULATING FLAGSHIP: MACRO RISK INDEX (MRI)")
        print("=" * 70)

        # Use pre-calculated components or calculate if not provided
        if lfi is None:
            lfi = self.indicators.get('LFI')
            if lfi is None:
                lfi = self.labor_fragility_index()

        if ldi is None:
            ldi = self.indicators.get('LDI')
            if ldi is None:
                ldi = self.labor_dynamism_index()

        if yfs is None:
            yfs = self.indicators.get('YFS')
            if yfs is None:
                yfs = self.yield_funding_stress()

        if emd is None:
            emd = self.indicators.get('EMD')
            if emd is None:
                emd = self.equity_momentum_divergence()

        if lci is None:
            lci = self.indicators.get('LCI')
            if lci is None:
                lci = self.liquidity_cushion_index()

        # Z-score HY OAS for credit component
        z_hy = self.calculate_zscore(self.df['HY_OAS'])

        # Calculate MRI
        mri_raw = lfi - ldi + yfs + z_hy + emd - lci

        # Z-score the composite for interpretability
        mri = self.calculate_zscore(mri_raw)

        self.indicators['MRI'] = mri
        self.indicators['MRI_Raw'] = mri_raw
        self.indicators['MRI_LFI_Component'] = lfi
        self.indicators['MRI_LDI_Component'] = -ldi  # Subtracted
        self.indicators['MRI_YFS_Component'] = yfs
        self.indicators['MRI_Credit_Component'] = z_hy
        self.indicators['MRI_EMD_Component'] = emd
        self.indicators['MRI_LCI_Component'] = -lci  # Subtracted

        latest = mri.dropna().iloc[-1] if len(mri.dropna()) > 0 else np.nan
        print(f"\n  ✓ MRI calculated. Latest value: {latest:.2f}σ")

        if latest > 1:
            print(f"  🔴 HIGH RISK: MRI >+1σ = Markets under-pricing macro risk!")
        elif latest > 0:
            print(f"  🟡 ELEVATED: MRI positive = Above-average systemic risk")
        else:
            print(f"  🟢 MODERATE: MRI negative = Below-average systemic risk")

        print("\nComponent Breakdown (latest values):")
        print(f"  +LFI (Labor Fragility):      {lfi.dropna().iloc[-1] if len(lfi.dropna()) > 0 else np.nan:+.2f}σ")
        print(f"  -LDI (Labor Dynamism):       {-ldi.dropna().iloc[-1] if len(ldi.dropna()) > 0 else np.nan:+.2f}σ")
        print(f"  +YFS (Yield-Funding Stress): {yfs.dropna().iloc[-1] if len(yfs.dropna()) > 0 else np.nan:+.2f}σ")
        print(f"  +HY OAS (Credit):            {z_hy.dropna().iloc[-1] if len(z_hy.dropna()) > 0 else np.nan:+.2f}σ")
        print(f"  +EMD (Equity Momentum):      {emd.dropna().iloc[-1] if len(emd.dropna()) > 0 else np.nan:+.2f}σ")
        print(f"  -LCI (Liquidity Cushion):    {-lci.dropna().iloc[-1] if len(lci.dropna()) > 0 else np.nan:+.2f}σ")
        print(f"  {'=' * 40}")
        print(f"  = MRI Total:                 {latest:+.2f}σ")

        return mri

    # ==================== SUPPORTING CALCULATIONS ====================

    def supporting_calculations(self):
        """Calculate additional useful metrics"""
        print("\n📊 Calculating supporting metrics...")

        # Payrolls YoY
        self.indicators['Payrolls_YoY'] = self.calculate_yoy_change(
            self.df['Total_Nonfarm_Payrolls']
        )

        # Hours YoY
        self.indicators['Hours_YoY'] = self.calculate_yoy_change(
            self.df['Total_Hours_Worked']
        )

        # Hours vs Employment divergence
        self.indicators['Hours_Employment_Divergence'] = (
            self.indicators['Hours_YoY'] - self.indicators['Payrolls_YoY']
        )

        # Credit growth
        self.indicators['Credit_Growth_YoY'] = self.calculate_yoy_change(
            self.df['Total_Bank_Credit']
        )

        # Curve steepness
        self.indicators['Curve_Steepness_10Y2Y'] = self.df['Yield_Curve_10Y2Y']

        print("  ✓ Supporting calculations complete")

    # ==================== MASTER CALCULATION ====================

    def calculate_all(self):
        """Calculate all proprietary indicators"""
        print("\n" + "=" * 70)
        print("CALCULATING ALL PROPRIETARY INDICATORS")
        print("=" * 70)

        # Section 1: Liquidity
        self.liquidity_cushion_index()
        self.yield_funding_stress()
        self.bill_sofr_spread()

        # Section 2: Labor
        lfi = self.labor_fragility_index()
        ldi = self.labor_dynamism_index()

        # Section 3: Credit
        self.credit_labor_gap(lfi=lfi)
        self.spread_volatility_imbalance()

        # Section 4: Equity
        emd = self.equity_momentum_divergence()

        # Section 5: Master Composite (uses all above)
        self.macro_risk_index()

        # Supporting calculations
        self.supporting_calculations()

        print("\n" + "=" * 70)
        print("✓ ALL INDICATORS CALCULATED")
        print("=" * 70)
        print(f"\nTotal indicators created: {len(self.indicators.columns)}")
        print(f"Date range: {self.indicators.index.min()} to {self.indicators.index.max()}")

        return self.indicators

    def save_indicators(self, output_path='proprietary_indicators.csv'):
        """Save calculated indicators to CSV"""
        print(f"\n💾 Saving indicators to: {output_path}")
        self.indicators.to_csv(output_path)

        # Save summary statistics
        summary_path = output_path.replace('.csv', '_summary.csv')
        summary = self.indicators.describe()
        summary.to_csv(summary_path)

        print(f"✓ Indicators saved: {output_path}")
        print(f"✓ Summary stats saved: {summary_path}")

        # Display latest values
        print("\n" + "=" * 70)
        print("LATEST VALUES (Most Recent)")
        print("=" * 70)

        key_indicators = [
            'MRI', 'LCI', 'LFI', 'LDI', 'CLG', 'YFS',
            'SVI', 'EMD', 'Bill_SOFR_Spread'
        ]

        latest_date = self.indicators.index[-1]
        print(f"\nDate: {latest_date}\n")

        for indicator in key_indicators:
            if indicator in self.indicators.columns:
                value = self.indicators[indicator].iloc[-1]
                if pd.notna(value):
                    print(f"  {indicator:25s}: {value:+7.2f}{'σ' if 'Spread' not in indicator else ' bps'}")
                else:
                    print(f"  {indicator:25s}: N/A")


def main():
    """Main execution"""
    # Initialize engine
    engine = ProprietaryIndicatorEngine(
        master_data_path='/Users/bob/lighthouse_paywall_deck/chartbook_master_data.csv'
    )

    # Calculate all indicators
    indicators = engine.calculate_all()

    # Save to CSV
    engine.save_indicators(
        output_path='/Users/bob/lighthouse_paywall_deck/proprietary_indicators.csv'
    )

    print("\n" + "=" * 70)
    print("✓ PROPRIETARY INDICATORS ENGINE COMPLETE")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Review proprietary_indicators.csv")
    print("  2. Check proprietary_indicators_summary.csv for statistics")
    print("  3. Use these indicators to generate charts")
    print("\nReady to visualize! 📊")


if __name__ == "__main__":
    main()
