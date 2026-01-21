"""
Lighthouse Macro - Complete Data Source Integration
FRED + OFR + NY Fed + MacroMicro PNGs
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from fredapi import Fred
import warnings
warnings.filterwarnings('ignore')

# API Keys
FRED_API_KEY = '11893c506c07b3b8647bf16cf60586e8'
fred = Fred(api_key=FRED_API_KEY)


class NYFedCollector:
    """NY Fed Data API Collector"""

    BASE_URL = "https://markets.newyorkfed.org/api"

    @staticmethod
    def get_sofr(start_date=None):
        """Fetch SOFR rates"""
        url = f"{NYFedCollector.BASE_URL}/rates/secured/sofr/search.json"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data['refRates'])
                df['effectiveDate'] = pd.to_datetime(df['effectiveDate'])
                df = df.set_index('effectiveDate')
                return df['percentRate'].astype(float)
        except:
            pass
        return pd.Series(dtype=float)

    @staticmethod
    def get_rrp():
        """Fetch RRP operations"""
        url = f"{NYFedCollector.BASE_URL}/rp/reverserepo/search.json"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data['repo']['operations'])
                df['operationDate'] = pd.to_datetime(df['operationDate'])
                df = df.set_index('operationDate')
                return df['totalAmtAccepted'].astype(float)
        except:
            pass
        return pd.Series(dtype=float)

    @staticmethod
    def get_primary_dealer_positions():
        """Fetch primary dealer positions"""
        url = f"{NYFedCollector.BASE_URL}/pd/get/latest.json"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return pd.DataFrame(response.json())
        except:
            pass
        return pd.DataFrame()


class OFRCollector:
    """Office of Financial Research API Collector"""

    BASE_URL = "https://www.financialresearch.gov/data"

    @staticmethod
    def get_financial_stress_index():
        """
        OFR Financial Stress Index
        Note: OFR data often requires direct download, not API
        """
        # OFR typically provides CSV downloads
        # This is a placeholder - actual implementation depends on OFR's current data format
        try:
            url = "https://www.financialresearch.gov/financial-stress-index/files/data.csv"
            df = pd.read_csv(url)
            df['date'] = pd.to_datetime(df.iloc[:, 0])
            df = df.set_index('date')
            return df.iloc[:, 1].astype(float)
        except:
            pass
        return pd.Series(dtype=float)

    @staticmethod
    def get_repo_market_data():
        """
        OFR Repo Market Data
        Placeholder - OFR provides specialized repo data
        """
        # Most OFR data requires manual download and processing
        # This would pull from local cache if available
        return pd.Series(dtype=float)


class DataOrchestrator:
    """Orchestrate all data sources"""

    def __init__(self):
        self.fred = fred
        self.nyfed = NYFedCollector()
        self.ofr = OFRCollector()
        self.cache = {}

    def safe_fetch_fred(self, series_id, start_date='2019-01-01', name=None):
        """Safely fetch FRED series"""
        try:
            data = self.fred.get_series(series_id, observation_start=start_date)
            if name:
                data.name = name
            return data
        except Exception as e:
            print(f"Warning: Could not fetch {series_id}: {e}")
            return pd.Series(dtype=float, name=name or series_id)

    def get_money_market_rates(self):
        """Get comprehensive money market rates"""
        data = {}

        # FRED sources
        data['SOFR_FRED'] = self.safe_fetch_fred('SOFR', name='SOFR')
        data['EFFR'] = self.safe_fetch_fred('EFFR', name='EFFR')
        data['IORB'] = self.safe_fetch_fred('IORB', name='IORB')
        data['OBFR'] = self.safe_fetch_fred('OBFR', name='OBFR')

        # NY Fed direct
        sofr_nyfed = self.nyfed.get_sofr()
        if len(sofr_nyfed) > 0:
            data['SOFR'] = sofr_nyfed

        return data

    def get_liquidity_metrics(self):
        """Get comprehensive liquidity data"""
        data = {}

        # Fed balance sheet
        data['Fed_Assets'] = self.safe_fetch_fred('WALCL', name='Fed Total Assets')
        data['RRP_FRED'] = self.safe_fetch_fred('RRPONTSYD', name='RRP')
        data['Reserves'] = self.safe_fetch_fred('WRESBAL', name='Reserves')
        data['TGA'] = self.safe_fetch_fred('WTREGEN', name='TGA')

        # NY Fed RRP
        rrp_nyfed = self.nyfed.get_rrp()
        if len(rrp_nyfed) > 0:
            data['RRP'] = rrp_nyfed

        # Market stress
        data['VIX'] = self.safe_fetch_fred('VIXCLS', name='VIX')
        data['MOVE'] = self.safe_fetch_fred('MOVE', name='MOVE Index')

        return data

    def get_credit_data(self):
        """Get credit market data"""
        data = {}

        # Spreads
        data['HY_Spread'] = self.safe_fetch_fred('BAMLH0A0HYM2', name='HY Spread')
        data['BBB_Spread'] = self.safe_fetch_fred('BAMLC0A4CBBB', name='BBB Spread')
        data['AAA_Spread'] = self.safe_fetch_fred('BAMLC0A1CAAA', name='AAA Spread')

        # Lending
        data['Total_Credit'] = self.safe_fetch_fred('TOTCI', name='Total Credit')
        data['Consumer_Credit'] = self.safe_fetch_fred('CONSUMER', name='Consumer Credit')
        data['Commercial_Loans'] = self.safe_fetch_fred('BUSLOANS', name='C&I Loans')

        return data

    def get_labor_data(self):
        """Get comprehensive labor market data"""
        data = {}

        # JOLTS
        data['Openings'] = self.safe_fetch_fred('JTSJOL', name='Job Openings')
        data['Hires'] = self.safe_fetch_fred('JTSHIL', name='Hires')
        data['Quits'] = self.safe_fetch_fred('JTSQUL', name='Quits')
        data['Layoffs'] = self.safe_fetch_fred('JTSLDL', name='Layoffs')

        # Unemployment
        data['Unemployment'] = self.safe_fetch_fred('UNRATE', name='Unemployment')
        data['U6'] = self.safe_fetch_fred('U6RATE', name='U6')
        data['Participation'] = self.safe_fetch_fred('CIVPART', name='Participation')

        # Wages
        data['Avg_Hourly'] = self.safe_fetch_fred('CES0500000003', name='Avg Hourly Earnings')
        data['ECI'] = self.safe_fetch_fred('ECIALLCIV', name='ECI')

        return data


def fetch_all_data():
    """Fetch all data sources and cache"""
    print("Fetching data from all sources...")

    orchestrator = DataOrchestrator()

    all_data = {
        'money_markets': orchestrator.get_money_market_rates(),
        'liquidity': orchestrator.get_liquidity_metrics(),
        'credit': orchestrator.get_credit_data(),
        'labor': orchestrator.get_labor_data(),
    }

    # Count successful fetches
    total_series = sum(len(category) for category in all_data.values())
    successful = sum(len(series) > 0 for category in all_data.values() for series in category.values())

    print(f"\nFetched {successful}/{total_series} data series successfully")

    return all_data


if __name__ == "__main__":
    data = fetch_all_data()
    print("\nAvailable data categories:")
    for category, series_dict in data.items():
        print(f"\n{category}:")
        for name, series in series_dict.items():
            status = f"✓ {len(series)} points" if len(series) > 0 else "✗ No data"
            print(f"  {name}: {status}")
