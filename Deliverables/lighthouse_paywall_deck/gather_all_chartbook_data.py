"""
LIGHTHOUSE MACRO - COMPLETE CHARTBOOK DATA COLLECTOR
Gathers ALL data needed for 50-chart chartbook into one consolidated CSV

Data Sources:
- FRED: 100+ economic series
- NY Fed: Money market rates, RRP, dealer positions
- OFR: Financial Stress Index, Bank Systemic Risk Monitor
- Crypto: Placeholder for manual TradingView/CoinGecko data

Output: chartbook_master_data.csv (wide format, date index)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fredapi import Fred
import requests
import warnings
import os
warnings.filterwarnings('ignore')

# API Keys
FRED_API_KEY = '11893c506c07b3b8647bf16cf60586e8'
fred = Fred(api_key=FRED_API_KEY)

# Data paths
DATA_DIR = '/Users/bob/lighthouse_paywall_deck/data'
OFR_DIR = f'{DATA_DIR}/ofr_downloads'


class ComprehensiveDataCollector:
    """Collect all data for 50-chart chartbook"""

    def __init__(self, start_date='2019-01-01'):
        self.start_date = start_date
        self.fred = fred
        self.data = pd.DataFrame()
        self.metadata = []

    def safe_fetch_fred(self, series_id, name=None, transform=None):
        """Safely fetch FRED series with error handling"""
        try:
            data = self.fred.get_series(series_id, observation_start=self.start_date)
            series_name = name or series_id

            # Apply transformation if specified
            if transform == 'yoy':
                data = data.pct_change(periods=252) * 100  # Annual YoY
            elif transform == 'diff':
                data = data.diff()

            self.metadata.append({
                'series_id': series_id,
                'name': series_name,
                'source': 'FRED',
                'points': len(data),
                'start': data.index.min() if len(data) > 0 else None,
                'end': data.index.max() if len(data) > 0 else None
            })

            return pd.Series(data, name=series_name)
        except Exception as e:
            print(f"⚠ Warning: Could not fetch {series_id}: {str(e)[:50]}")
            return pd.Series(dtype=float, name=name or series_id)

    def fetch_nyfed_data(self):
        """Fetch NY Fed market data"""
        print("\n📊 Fetching NY Fed data...")

        # Try to fetch RRP from NY Fed API
        try:
            url = "https://markets.newyorkfed.org/api/rp/reverserepo/search.json"
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data['repo']['operations'])
                df['operationDate'] = pd.to_datetime(df['operationDate'])
                df = df.set_index('operationDate')
                rrp_nyfed = df['totalAmtAccepted'].astype(float) / 1000  # Convert to billions
                print(f"  ✓ RRP (NY Fed): {len(rrp_nyfed)} observations")
                return {'RRP_NYFED': rrp_nyfed}
        except Exception as e:
            print(f"  ⚠ NY Fed API failed: {str(e)[:50]}")

        return {}

    def load_ofr_data(self):
        """Load OFR data from local files"""
        print("\n📊 Loading OFR data...")
        ofr_data = {}

        # Financial Stress Index
        fsi_path = f'{OFR_DIR}/fsi_data.csv'
        if os.path.exists(fsi_path):
            df = pd.read_csv(fsi_path, parse_dates=['Date'], index_col='Date')
            # Use the main FSI column
            ofr_data['OFR_FSI'] = df['OFR FSI']
            # Also include sub-components
            for col in df.columns:
                if col != 'OFR FSI':
                    ofr_data[f'FSI_{col.replace(" ", "_")}'] = df[col]
            print(f"  ✓ OFR FSI: {len(df)} observations, {len(df.columns)} components")

        # Bank Systemic Risk Monitor
        bsrm_path = f'{OFR_DIR}/bsrm_data.csv'
        if os.path.exists(bsrm_path):
            df = pd.read_csv(bsrm_path)
            # Check actual column names
            if 'Date' in df.columns or 'date' in df.columns:
                date_col = 'Date' if 'Date' in df.columns else 'date'
                df[date_col] = pd.to_datetime(df[date_col])
                df = df.set_index(date_col)
                # Get the first data column (assuming it's BSRM)
                data_col = [col for col in df.columns if col not in ['Date', 'date']][0]
                ofr_data['OFR_BSRM'] = df[data_col]
                print(f"  ✓ OFR BSRM: {len(df)} observations")

        return ofr_data

    def fetch_section1_liquidity_data(self):
        """Section 1: Liquidity & Funding Stress (Charts 1-10)"""
        print("\n📊 Section 1: Liquidity & Funding Stress")
        data = {}

        # Money market rates
        data['SOFR'] = self.safe_fetch_fred('SOFR', 'SOFR')
        data['EFFR'] = self.safe_fetch_fred('EFFR', 'EFFR')
        data['OBFR'] = self.safe_fetch_fred('OBFR', 'OBFR')
        data['IORB'] = self.safe_fetch_fred('IORB', 'IORB')
        data['IOER'] = self.safe_fetch_fred('IOER', 'IOER')

        # Fed balance sheet
        data['Fed_Total_Assets'] = self.safe_fetch_fred('WALCL', 'Fed Total Assets')
        data['RRP'] = self.safe_fetch_fred('RRPONTSYD', 'RRP')
        data['Bank_Reserves'] = self.safe_fetch_fred('WRESBAL', 'Bank Reserves')
        data['TGA'] = self.safe_fetch_fred('WTREGEN', 'TGA Balance')

        # Treasury rates
        data['UST_3M'] = self.safe_fetch_fred('DGS3MO', '3M Treasury')
        data['UST_2Y'] = self.safe_fetch_fred('DGS2', '2Y Treasury')
        data['UST_10Y'] = self.safe_fetch_fred('DGS10', '10Y Treasury')
        data['UST_30Y'] = self.safe_fetch_fred('DGS30', '30Y Treasury')

        # Yield curve
        data['Yield_Curve_10Y2Y'] = self.safe_fetch_fred('T10Y2Y', '10Y-2Y Spread')
        data['Yield_Curve_10Y3M'] = self.safe_fetch_fred('T10Y3M', '10Y-3M Spread')

        # Market stress
        data['VIX'] = self.safe_fetch_fred('VIXCLS', 'VIX')

        # GDP for ratios
        data['GDP'] = self.safe_fetch_fred('GDP', 'GDP')

        return data

    def fetch_section2_labor_data(self):
        """Section 2: Labor Market Dynamics (Charts 11-17)"""
        print("\n📊 Section 2: Labor Market Dynamics")
        data = {}

        # JOLTS data
        data['Job_Openings'] = self.safe_fetch_fred('JTSJOL', 'Job Openings')
        data['Hires'] = self.safe_fetch_fred('JTSHIL', 'Hires')
        data['Quits'] = self.safe_fetch_fred('JTSQUL', 'Quits')
        data['Layoffs'] = self.safe_fetch_fred('JTSLDL', 'Layoffs')
        data['Total_Separations'] = self.safe_fetch_fred('JTSTSL', 'Total Separations')

        # Unemployment metrics
        data['Unemployment_Rate'] = self.safe_fetch_fred('UNRATE', 'Unemployment Rate')
        data['U6_Rate'] = self.safe_fetch_fred('U6RATE', 'U6 Rate')
        data['Labor_Force_Participation'] = self.safe_fetch_fred('CIVPART', 'Participation Rate')
        data['Prime_Age_Employment'] = self.safe_fetch_fred('LNS12300060', 'Prime Age Employment')

        # Long-term unemployment
        data['Unemployed_27_Weeks'] = self.safe_fetch_fred('UEMP27OV', 'Unemployed 27+ Weeks')
        data['Median_Unemployment_Duration'] = self.safe_fetch_fred('UEMPMED', 'Median Duration')

        # Employment and hours
        data['Total_Nonfarm_Payrolls'] = self.safe_fetch_fred('PAYEMS', 'Nonfarm Payrolls')
        data['Total_Hours_Worked'] = self.safe_fetch_fred('AWHI', 'Aggregate Hours Index')
        data['Avg_Weekly_Hours'] = self.safe_fetch_fred('AWHAETP', 'Avg Weekly Hours')

        # Wages
        data['Avg_Hourly_Earnings'] = self.safe_fetch_fred('CES0500000003', 'Avg Hourly Earnings')
        data['ECI_Total_Comp'] = self.safe_fetch_fred('ECIALLCIV', 'ECI Total Compensation')
        data['Median_Weekly_Earnings'] = self.safe_fetch_fred('LES1252881600Q', 'Median Weekly Earnings')

        # NFIB Small Business
        data['NFIB_Hiring_Plans'] = self.safe_fetch_fred('HNOISP', 'NFIB Hiring Plans')

        return data

    def fetch_section3_credit_data(self):
        """Section 3: Credit Markets & Risk Appetite (Charts 18-25)"""
        print("\n📊 Section 3: Credit Markets & Risk Appetite")
        data = {}

        # Credit spreads
        data['HY_OAS'] = self.safe_fetch_fred('BAMLH0A0HYM2', 'HY OAS')
        data['BBB_OAS'] = self.safe_fetch_fred('BAMLC0A4CBBB', 'BBB OAS')
        data['AAA_OAS'] = self.safe_fetch_fred('BAMLC0A1CAAA', 'AAA OAS')
        data['IG_OAS'] = self.safe_fetch_fred('BAMLC0A0CM', 'IG OAS')

        # Credit growth
        data['Total_Bank_Credit'] = self.safe_fetch_fred('TOTCI', 'Total Bank Credit')
        data['CI_Loans'] = self.safe_fetch_fred('BUSLOANS', 'C&I Loans')
        data['Consumer_Credit'] = self.safe_fetch_fred('TOTALSL', 'Consumer Credit')

        # Corporate debt
        data['Corp_Debt_to_GDP'] = self.safe_fetch_fred('NCBDBIQ027S', 'Corp Debt/GDP')
        data['Household_Debt_to_GDP'] = self.safe_fetch_fred('HDTGPDUSQ163N', 'Household Debt/GDP')

        # Excess Bond Premium
        data['Excess_Bond_Premium'] = self.safe_fetch_fred('BAMLH0A0HYM2EY', 'Excess Bond Premium')

        # Fed Funds Rate
        data['Fed_Funds_Rate'] = self.safe_fetch_fred('FEDFUNDS', 'Fed Funds Rate')
        data['Fed_Funds_Target'] = self.safe_fetch_fred('DFEDTARU', 'Fed Funds Target')

        return data

    def fetch_section4_equity_data(self):
        """Section 4: Equity Positioning & Momentum (Charts 26-32)"""
        print("\n📊 Section 4: Equity Positioning & Momentum")
        data = {}

        # Equity indices
        data['SP500'] = self.safe_fetch_fred('SP500', 'S&P 500')
        data['NASDAQ'] = self.safe_fetch_fred('NASDAQCOM', 'Nasdaq Composite')
        data['DJIA'] = self.safe_fetch_fred('DJIA', 'Dow Jones')

        # Equity volatility
        data['VIX'] = self.safe_fetch_fred('VIXCLS', 'VIX')

        # Corporate earnings
        data['SP500_PE_Ratio'] = self.safe_fetch_fred('MULTPL/SP500_PE_RATIO_MONTH', 'S&P 500 P/E')

        # Treasury for equity risk premium
        data['UST_10Y_ERP'] = self.safe_fetch_fred('DGS10', '10Y for ERP')

        return data

    def fetch_section5_crypto_data(self):
        """Section 5: Crypto & Digital Assets (Charts 33-39)"""
        print("\n📊 Section 5: Crypto & Digital Assets")
        data = {}

        # Note: Crypto data typically requires TradingView/CoinGecko
        # These are placeholders for manual data entry

        # Money market funds (for stablecoin comparison)
        data['MMF_Total_Assets'] = self.safe_fetch_fred('MMMFFAQ027S', 'MMF Assets')

        return data

    def fetch_section6_ai_infrastructure_data(self):
        """Section 6: AI Infrastructure & CapEx Cycle (Charts 40-50)"""
        print("\n📊 Section 6: AI Infrastructure & CapEx")
        data = {}

        # Technology sector indicators
        data['Industrial_Production_Tech'] = self.safe_fetch_fred('IPB54100N', 'IP: Technology')
        data['Capacity_Utilization_Tech'] = self.safe_fetch_fred('TCU', 'Capacity Util: Tech')

        # Semiconductor indicators
        data['Philly_Fed_Semi'] = self.safe_fetch_fred('BSCICP03USM665S', 'Semi Equipment Production')

        # Business investment
        data['Nonresidential_Investment'] = self.safe_fetch_fred('PNFI', 'Nonresidential Investment')
        data['Info_Processing_Equipment'] = self.safe_fetch_fred('Y001RE1Q156SBEA', 'Info Processing Equipment')

        # Exports (for Taiwan semi comparison)
        data['Taiwan_Exports'] = self.safe_fetch_fred('XTEXVA01TWM667S', 'Taiwan Exports')

        return data

    def fetch_all_data(self):
        """Fetch all data from all sections"""
        print("=" * 70)
        print("LIGHTHOUSE MACRO - COMPREHENSIVE CHARTBOOK DATA COLLECTION")
        print("=" * 70)

        all_data = {}

        # Fetch from all sections
        all_data.update(self.fetch_section1_liquidity_data())
        all_data.update(self.fetch_section2_labor_data())
        all_data.update(self.fetch_section3_credit_data())
        all_data.update(self.fetch_section4_equity_data())
        all_data.update(self.fetch_section5_crypto_data())
        all_data.update(self.fetch_section6_ai_infrastructure_data())

        # Add NY Fed data
        all_data.update(self.fetch_nyfed_data())

        # Add OFR data
        all_data.update(self.load_ofr_data())

        # Combine into DataFrame
        print("\n" + "=" * 70)
        print("📊 CONSOLIDATING DATA")
        print("=" * 70)

        # Convert to DataFrame
        df = pd.DataFrame(all_data)

        # Sort by date
        df = df.sort_index()

        # Fill forward to handle different frequencies
        df = df.fillna(method='ffill')

        print(f"\n✓ Master dataset created:")
        print(f"  • Date range: {df.index.min()} to {df.index.max()}")
        print(f"  • Total columns: {len(df.columns)}")
        print(f"  • Total rows: {len(df)}")
        print(f"  • Coverage: {df.notna().sum().sum():,} data points")

        self.data = df
        return df

    def save_to_csv(self, filename='chartbook_master_data.csv'):
        """Save consolidated data to CSV"""
        output_path = f'/Users/bob/lighthouse_paywall_deck/{filename}'
        self.data.to_csv(output_path)
        print(f"\n✓ Data saved to: {output_path}")
        print(f"  File size: {os.path.getsize(output_path) / 1024:.1f} KB")

        # Save metadata
        metadata_path = output_path.replace('.csv', '_metadata.csv')
        pd.DataFrame(self.metadata).to_csv(metadata_path, index=False)
        print(f"✓ Metadata saved to: {metadata_path}")

        return output_path

    def generate_summary_report(self):
        """Generate summary report of data collection"""
        print("\n" + "=" * 70)
        print("📊 DATA COLLECTION SUMMARY")
        print("=" * 70)

        # Summary by section
        sections = {
            'Liquidity & Funding': ['SOFR', 'EFFR', 'RRP', 'Fed_Total_Assets', 'VIX'],
            'Labor Market': ['Unemployment_Rate', 'Job_Openings', 'Quits', 'Hires'],
            'Credit Markets': ['HY_OAS', 'BBB_OAS', 'CI_Loans', 'Fed_Funds_Rate'],
            'Equity Markets': ['SP500', 'NASDAQ', 'VIX'],
            'Crypto/Digital': ['MMF_Total_Assets'],
            'AI Infrastructure': ['Industrial_Production_Tech', 'Taiwan_Exports']
        }

        for section, indicators in sections.items():
            available = [ind for ind in indicators if ind in self.data.columns]
            print(f"\n{section}:")
            print(f"  Available: {len(available)}/{len(indicators)}")
            for ind in available[:3]:  # Show first 3
                latest = self.data[ind].dropna()
                if len(latest) > 0:
                    print(f"    • {ind}: {len(latest)} obs, latest = {latest.iloc[-1]:.2f}")

        # Coverage statistics
        print(f"\n{'=' * 70}")
        print("COVERAGE STATISTICS")
        print(f"{'=' * 70}")
        coverage = (self.data.notna().sum() / len(self.data) * 100).describe()
        print(f"\nData completeness by column:")
        print(f"  Mean coverage: {coverage['mean']:.1f}%")
        print(f"  Min coverage: {coverage['min']:.1f}%")
        print(f"  Max coverage: {coverage['max']:.1f}%")

        # Most complete series
        print(f"\nMost complete series (top 10):")
        top_coverage = (self.data.notna().sum() / len(self.data) * 100).nlargest(10)
        for col, pct in top_coverage.items():
            print(f"  • {col}: {pct:.1f}%")

        # Series needing manual collection
        print(f"\n{'=' * 70}")
        print("⚠ MANUAL DATA NEEDED")
        print(f"{'=' * 70}")
        print("\nThe following data requires manual collection:")
        print("  • Stablecoin supply (USDT, USDC, DAI) - CoinGecko")
        print("  • Bitcoin price - TradingView")
        print("  • QUAL/SPY ETF prices - TradingView/Yahoo")
        print("  • Sector ETF prices (11 sectors) - TradingView")
        print("  • Cross-currency basis swaps - Bloomberg")
        print("  • Swap spreads (2Y, 5Y, 10Y, 30Y) - Bloomberg")
        print("  • MacroMicro charts (4 screenshots)")
        print("  • TradingView 3-panel charts (NVDA, MSFT, TSM)")


def main():
    """Main execution"""
    collector = ComprehensiveDataCollector(start_date='2018-01-01')

    # Fetch all data
    df = collector.fetch_all_data()

    # Save to CSV
    collector.save_to_csv()

    # Generate summary report
    collector.generate_summary_report()

    print("\n" + "=" * 70)
    print("✓ DATA COLLECTION COMPLETE")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Review chartbook_master_data.csv")
    print("  2. Collect manual data (crypto, ETFs, screenshots)")
    print("  3. Use this data for all 50 charts in the chartbook")


if __name__ == "__main__":
    main()
