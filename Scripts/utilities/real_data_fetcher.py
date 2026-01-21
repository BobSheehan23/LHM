"""
LIGHTHOUSE MACRO - Real Data Fetcher
All data from actual APIs - NO SYNTHETIC DATA

Sources:
- NY Fed Markets API: https://markets.newyorkfed.org
- Treasury Fiscal Data: https://fiscaldata.treasury.gov
- FRED API: https://fred.stlouisfed.org
- BLS API: https://api.bls.gov
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from functools import lru_cache
import json
import time


# =============================================================================
# API KEYS
# =============================================================================
FRED_API_KEY = '11893c506c07b3b8647bf16cf60586e8'
BLS_API_KEY = '2e66aeb26c664d4fbc862de06d1f8899'
BEA_API_KEY = '4401D40D-4047-414F-B4FE-D441E96F8DE8'


# =============================================================================
# NY FED API - https://markets.newyorkfed.org
# =============================================================================

class NYFedAPI:
    """NY Fed Markets Data API"""

    BASE_URL = "https://markets.newyorkfed.org"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'LighthouseMacro/1.0'
        })

    def _get(self, endpoint):
        """Make GET request to NY Fed API"""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"    NY Fed API error: {e}")
            return None

    def get_sofr(self, last_n=500):
        """
        GET /api/rates/secured/sofr/last/{number}.json
        Returns SOFR rate with percentiles (1st, 25th, 75th, 99th)
        Note: NY Fed API max is ~500 per request
        """
        last_n = min(last_n, 500)  # API limit
        data = self._get(f"/api/rates/secured/sofr/last/{last_n}.json")
        if data and 'refRates' in data:
            df = pd.DataFrame(data['refRates'])
            df['effectiveDate'] = pd.to_datetime(df['effectiveDate'])
            for col in ['percentRate', 'volumeInBillions', 'percentile1', 'percentile25',
                       'percentile75', 'percentile99', 'targetRateFrom', 'targetRateTo']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.set_index('effectiveDate').sort_index()
            print(f"    Fetched NY Fed SOFR: {len(df)} obs")
            return df
        return pd.DataFrame()

    def get_effr(self, last_n=500):
        """
        GET /api/rates/unsecured/effr/last/{number}.json
        """
        last_n = min(last_n, 500)  # API limit
        data = self._get(f"/api/rates/unsecured/effr/last/{last_n}.json")
        if data and 'refRates' in data:
            df = pd.DataFrame(data['refRates'])
            df['effectiveDate'] = pd.to_datetime(df['effectiveDate'])
            for col in ['percentRate', 'volumeInBillions', 'percentile1', 'percentile25',
                       'percentile75', 'percentile99']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.set_index('effectiveDate').sort_index()
            print(f"    Fetched NY Fed EFFR: {len(df)} obs")
            return df
        return pd.DataFrame()

    def get_obfr(self, last_n=500):
        """
        GET /api/rates/unsecured/obfr/last/{number}.json
        """
        data = self._get(f"/api/rates/unsecured/obfr/last/{last_n}.json")
        if data and 'refRates' in data:
            df = pd.DataFrame(data['refRates'])
            df['effectiveDate'] = pd.to_datetime(df['effectiveDate'])
            for col in ['percentRate', 'volumeInBillions']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.set_index('effectiveDate').sort_index()
            print(f"    Fetched NY Fed OBFR: {len(df)} obs")
            return df
        return pd.DataFrame()

    def get_tgcr(self, last_n=500):
        """
        GET /api/rates/secured/tgcr/last/{number}.json
        Tri-Party General Collateral Rate
        """
        data = self._get(f"/api/rates/secured/tgcr/last/{last_n}.json")
        if data and 'refRates' in data:
            df = pd.DataFrame(data['refRates'])
            df['effectiveDate'] = pd.to_datetime(df['effectiveDate'])
            for col in ['percentRate', 'volumeInBillions']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.set_index('effectiveDate').sort_index()
            print(f"    Fetched NY Fed TGCR: {len(df)} obs")
            return df
        return pd.DataFrame()

    def get_bgcr(self, last_n=500):
        """
        GET /api/rates/secured/bgcr/last/{number}.json
        Broad General Collateral Rate
        """
        data = self._get(f"/api/rates/secured/bgcr/last/{last_n}.json")
        if data and 'refRates' in data:
            df = pd.DataFrame(data['refRates'])
            df['effectiveDate'] = pd.to_datetime(df['effectiveDate'])
            for col in ['percentRate', 'volumeInBillions']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.set_index('effectiveDate').sort_index()
            print(f"    Fetched NY Fed BGCR: {len(df)} obs")
            return df
        return pd.DataFrame()

    def get_rrp_operations(self, last_n=500):
        """
        GET /api/rp/reverserepo/all/results/last/{number}.json
        Reverse Repo (RRP/ON RRP) operations
        """
        data = self._get(f"/api/rp/reverserepo/all/results/last/{last_n}.json")
        if data and 'repo' in data and 'operations' in data['repo']:
            df = pd.DataFrame(data['repo']['operations'])
            df['operationDate'] = pd.to_datetime(df['operationDate'])
            for col in ['totalAmtSubmitted', 'totalAmtAccepted', 'participatingCpty']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            # Convert to billions
            if 'totalAmtAccepted' in df.columns:
                df['totalAmtAccepted'] = df['totalAmtAccepted'] / 1e9
            df = df.set_index('operationDate').sort_index()
            print(f"    Fetched NY Fed RRP: {len(df)} ops")
            return df
        return pd.DataFrame()

    def get_repo_operations(self, last_n=500):
        """
        GET /api/rp/repo/all/results/last/{number}.json
        Repo operations (includes SRF)
        """
        last_n = min(last_n, 500)  # API limit
        data = self._get(f"/api/rp/repo/all/results/last/{last_n}.json")
        if data and 'repo' in data and 'operations' in data['repo']:
            df = pd.DataFrame(data['repo']['operations'])
            df['operationDate'] = pd.to_datetime(df['operationDate'])
            for col in ['totalAmtSubmitted', 'totalAmtAccepted']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            if 'totalAmtAccepted' in df.columns:
                df['totalAmtAccepted'] = df['totalAmtAccepted'] / 1e9
            df = df.set_index('operationDate').sort_index()
            print(f"    Fetched NY Fed Repo: {len(df)} ops")
            return df
        return pd.DataFrame()

    def get_soma_summary(self):
        """
        GET /api/soma/summary.json
        SOMA holdings summary by security type
        """
        data = self._get("/api/soma/summary.json")
        if data and 'soma' in data and 'summary' in data['soma']:
            df = pd.DataFrame(data['soma']['summary'])
            df['asOfDate'] = pd.to_datetime(df['asOfDate'])
            for col in ['total', 'bills', 'notesbonds', 'tips', 'frn', 'mbs', 'cmbs', 'agencies']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.set_index('asOfDate').sort_index()
            print(f"    Fetched NY Fed SOMA: {len(df)} obs")
            return df
        return pd.DataFrame()

    def get_primary_dealer_timeseries(self):
        """
        GET /api/pd/get/all/timeseries.csv
        All primary dealer survey data
        """
        url = f"{self.BASE_URL}/api/pd/get/all/timeseries.csv"
        try:
            df = pd.read_csv(url)
            print(f"    Fetched NY Fed Primary Dealer: {len(df)} rows")
            return df
        except Exception as e:
            print(f"    NY Fed PD error: {e}")
            return pd.DataFrame()

    def list_primary_dealer_series(self):
        """
        GET /api/pd/list/timeseries.json
        List all available PD series
        """
        data = self._get("/api/pd/list/timeseries.json")
        if data and 'pd' in data and 'timeseries' in data['pd']:
            return pd.DataFrame(data['pd']['timeseries'])
        return pd.DataFrame()


# =============================================================================
# TREASURY FISCAL DATA API - https://fiscaldata.treasury.gov
# =============================================================================

class TreasuryAPI:
    """Treasury Fiscal Data API"""

    BASE_URL = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service"

    def __init__(self):
        self.session = requests.Session()

    def _get(self, endpoint, params=None):
        """Make GET request to Treasury API"""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"    Treasury API error: {e}")
            return None

    def get_auction_results(self, start_date='2024-01-01'):
        """
        Auction results including high yield, low yield for tail calculation
        """
        params = {
            'filter': f'auction_date:gte:{start_date}',
            'sort': '-auction_date',
            'page[size]': 500
        }
        data = self._get("/v1/accounting/od/auctions_query", params)
        if data and 'data' in data:
            df = pd.DataFrame(data['data'])
            if 'auction_date' in df.columns:
                df['auction_date'] = pd.to_datetime(df['auction_date'])
            for col in ['high_investment_rate', 'low_investment_rate', 'offering_amt']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            print(f"    Fetched Treasury Auctions: {len(df)} results")
            return df
        return pd.DataFrame()

    def get_debt_to_penny(self):
        """
        Total public debt outstanding (daily)
        """
        params = {
            'sort': '-record_date',
            'page[size]': 500
        }
        data = self._get("/v2/accounting/od/debt_to_penny", params)
        if data and 'data' in data:
            df = pd.DataFrame(data['data'])
            df['record_date'] = pd.to_datetime(df['record_date'])
            for col in ['tot_pub_debt_out_amt']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.set_index('record_date').sort_index()
            print(f"    Fetched Treasury Debt: {len(df)} obs")
            return df
        return pd.DataFrame()

    def get_mspd_holdings(self):
        """
        Monthly Statement of Public Debt - holdings by type
        """
        params = {
            'sort': '-record_date',
            'page[size]': 200
        }
        data = self._get("/v1/debt/mspd/mspd_table_1", params)
        if data and 'data' in data:
            df = pd.DataFrame(data['data'])
            print(f"    Fetched Treasury MSPD: {len(df)} rows")
            return df
        return pd.DataFrame()

    def get_tic_holdings(self, start_date='2020-01-01'):
        """
        Treasury International Capital - Foreign holdings by country
        Try multiple endpoints since API varies
        """
        # Try mfh_country endpoint first
        endpoints = [
            "/v2/accounting/od/mfh_country",
            "/v1/accounting/od/mfh_country_quarterly",
            "/v2/accounting/od/securities_mfh_country",
        ]

        for endpoint in endpoints:
            params = {
                'sort': '-record_date',
                'page[size]': 200
            }
            data = self._get(endpoint, params)
            if data and 'data' in data and len(data['data']) > 0:
                df = pd.DataFrame(data['data'])
                if 'record_date' in df.columns:
                    df['record_date'] = pd.to_datetime(df['record_date'])
                print(f"    Fetched Treasury TIC: {len(df)} rows")
                return df

        print("    Treasury TIC: No valid endpoint found")
        return pd.DataFrame()


# =============================================================================
# FRED API
# =============================================================================

class FREDAPI:
    """Federal Reserve Economic Data API"""

    BASE_URL = "https://api.stlouisfed.org/fred"

    def __init__(self, api_key=FRED_API_KEY):
        self.api_key = api_key
        self.session = requests.Session()

    def get_series(self, series_id, start_date='2000-01-01'):
        """Fetch a FRED series"""
        url = f"{self.BASE_URL}/series/observations"
        params = {
            'series_id': series_id,
            'api_key': self.api_key,
            'file_type': 'json',
            'observation_start': start_date
        }
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if 'observations' not in data:
                return pd.Series(dtype=float)

            dates = []
            values = []
            for obs in data['observations']:
                dates.append(obs['date'])
                val = obs['value']
                values.append(float(val) if val != '.' else np.nan)

            series = pd.Series(values, index=pd.to_datetime(dates), name=series_id)
            series = series.dropna().sort_index()
            print(f"    Fetched FRED {series_id}: {len(series)} obs")
            return series
        except Exception as e:
            print(f"    FRED error {series_id}: {e}")
            return pd.Series(dtype=float)

    # Pre-defined series fetchers
    def get_sofr(self, start='2018-01-01'):
        return self.get_series('SOFR', start)

    def get_effr(self, start='2000-01-01'):
        return self.get_series('EFFR', start)

    def get_yields(self, start='2000-01-01'):
        """Get full Treasury yield curve"""
        series_map = {
            '3M': 'DGS3MO', '6M': 'DGS6MO', '1Y': 'DGS1',
            '2Y': 'DGS2', '3Y': 'DGS3', '5Y': 'DGS5',
            '7Y': 'DGS7', '10Y': 'DGS10', '20Y': 'DGS20', '30Y': 'DGS30'
        }
        yields = {}
        for tenor, series_id in series_map.items():
            yields[tenor] = self.get_series(series_id, start)
        return yields

    def get_credit_spreads(self, start='2000-01-01'):
        """Get credit spread indices"""
        return {
            'HY': self.get_series('BAMLH0A0HYM2', start),      # HY OAS
            'BBB': self.get_series('BAMLC0A4CBBB', start),     # BBB OAS
            'AAA': self.get_series('BAMLC0A1CAAA', start),     # AAA OAS
            'IG': self.get_series('BAMLC0A0CM', start),        # IG OAS
        }

    def get_reserves(self, start='2008-01-01'):
        return self.get_series('WRESBAL', start)

    def get_rrp(self, start='2013-01-01'):
        return self.get_series('RRPONTSYD', start)

    def get_savings_rate(self, start='2000-01-01'):
        return self.get_series('PSAVERT', start)

    def get_consumer_credit(self, start='2000-01-01'):
        return self.get_series('TOTALSL', start)

    def get_initial_claims(self, start='2000-01-01'):
        return self.get_series('ICSA', start)

    def get_vix(self, start='2000-01-01'):
        return self.get_series('VIXCLS', start)

    def get_gdp(self, start='1990-01-01'):
        return {
            'nominal': self.get_series('GDP', start),
            'real': self.get_series('GDPC1', start),
            'deflator': self.get_series('GDPDEF', start)
        }

    def get_debt(self, start='2000-01-01'):
        return {
            'total': self.get_series('GFDEBTN', start),
            'debt_gdp': self.get_series('GFDEGDQ188S', start)
        }

    def get_unemployment(self, start='2000-01-01'):
        return {
            'rate': self.get_series('UNRATE', start),
            'long_term': self.get_series('LNS13025703', start),  # 27+ weeks
        }

    def get_cre_delinquency(self, start='2000-01-01'):
        return self.get_series('DRCLACBS', start)

    def get_auto_delinquency(self, start='2000-01-01'):
        return self.get_series('DRALACBS', start)


# =============================================================================
# BLS API
# =============================================================================

class BLSAPI:
    """Bureau of Labor Statistics API"""

    BASE_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

    def __init__(self, api_key=BLS_API_KEY):
        self.api_key = api_key
        self.session = requests.Session()

    def get_series(self, series_ids, start_year=2019, end_year=2026):
        """Fetch one or more BLS series"""
        if isinstance(series_ids, str):
            series_ids = [series_ids]

        payload = {
            "seriesid": series_ids,
            "startyear": str(start_year),
            "endyear": str(end_year),
            "registrationkey": self.api_key
        }

        try:
            response = self.session.post(self.BASE_URL, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get('status') != 'REQUEST_SUCCEEDED':
                print(f"    BLS API error: {data.get('message', 'Unknown')}")
                return {}

            results = {}
            for series in data['Results']['series']:
                series_id = series['seriesID']
                dates = []
                values = []
                for item in series['data']:
                    period = item['period']
                    if period.startswith('M'):
                        month = period[1:]
                        date = f"{item['year']}-{month}-01"
                        dates.append(date)
                        values.append(float(item['value']))

                s = pd.Series(values, index=pd.to_datetime(dates), name=series_id)
                s = s.sort_index()
                results[series_id] = s
                print(f"    Fetched BLS {series_id}: {len(s)} obs")

            return results
        except Exception as e:
            print(f"    BLS error: {e}")
            return {}

    def get_jolts_quits(self, start_year=2019):
        """JOLTS Quits Rate - Total Nonfarm"""
        return self.get_series('JTS000000000000000QUR', start_year)

    def get_jolts_hires(self, start_year=2019):
        """JOLTS Hires Rate - Total Nonfarm"""
        return self.get_series('JTS000000000000000HIR', start_year)

    def get_jolts_openings(self, start_year=2019):
        """JOLTS Job Openings Rate - Total Nonfarm"""
        return self.get_series('JTS000000000000000JOR', start_year)


# =============================================================================
# BEA API - Bureau of Economic Analysis
# =============================================================================

class BEAAPI:
    """Bureau of Economic Analysis NIPA & Fixed Assets Data API"""

    BASE_URL = "https://apps.bea.gov/api/data/"

    # Default: Long-term data from 2000
    DEFAULT_YEARS = ','.join([str(y) for y in range(2000, 2027)])

    def __init__(self, api_key=BEA_API_KEY):
        self.api_key = api_key
        self.session = requests.Session()

    def get_table(self, table_id, year=None, frequency="Q", dataset="NIPA"):
        """
        Fetch a specific NIPA or FixedAssets table.

        Key NIPA Tables:
        - T10105: GDP breakdown (Goods, Services, Structures) - Table 1.1.5
        - T20305: PCE by Major Type (Durable/Non-Durable/Services) - Table 2.3.5
        - T20100: Personal Income & Disposition (Wages, Transfers, DPI, Saving Rate) - Table 2.1
        - T11200: National Income by Type (Corporate Profits before/after tax) - Table 1.12
        - T11000: Gross Domestic Income by Type - Table 1.10
        - T20304: PCE Price Index (includes Core ex-Food/Energy) - Table 2.3.4
        - T10101: Percent Change in Real GDP - Table 1.1.1

        Key FixedAssets Tables:
        - FAAt101: Fixed Assets by Type
        - FAAt701: Government Fixed Assets

        dataset: 'NIPA' or 'FixedAssets'
        frequency: 'Q' for Quarterly, 'A' for Annual, 'M' for Monthly
        year: defaults to 2000-2026 for long-term analysis
        """
        if year is None:
            year = self.DEFAULT_YEARS

        # FixedAssets requires Annual frequency
        if dataset == "FixedAssets":
            frequency = "A"

        params = {
            "UserID": self.api_key,
            "Method": "GetData",
            "DatasetName": dataset,
            "TableName": table_id,
            "Frequency": frequency,
            "Year": year,
            "ResultFormat": "JSON"
        }

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=60)
            response.raise_for_status()
            data = response.json()

            if "BEAAPI" in data and "Results" in data["BEAAPI"]:
                records = data["BEAAPI"]["Results"]["Data"]
                df = pd.DataFrame(records)
                df['Source_TableID'] = table_id
                df['Source_Dataset'] = dataset
                print(f"    Fetched BEA {table_id}: {len(df)} rows")
                return df
            else:
                print(f"    BEA API error structure for {table_id}")
                return pd.DataFrame()
        except Exception as e:
            print(f"    BEA API error {table_id}: {e}")
            return pd.DataFrame()

    # =========================================================================
    # CORE GDP PRODUCTS
    # =========================================================================

    def get_gdp(self, years=None):
        """Gross Domestic Product - comprehensive measure of U.S. economy (Table 1.1.5)"""
        return self.get_table("T10105", year=years)

    def get_gdp_components(self, years=None):
        """Alias for get_gdp - GDP breakdown by Goods, Services, Structures"""
        return self.get_gdp(years)

    def get_real_gdp_growth(self, years=None):
        """Percent Change in Real GDP (Table 1.1.1)"""
        return self.get_table("T10101", year=years)

    def get_gdi(self, years=None):
        """Gross Domestic Income - GDP measured via incomes (Table 1.10)"""
        return self.get_table("T11000", year=years)

    # =========================================================================
    # CONSUMER PRODUCTS
    # =========================================================================

    def get_consumer_spending(self, years=None):
        """Consumer Spending / PCE by Major Type - Durable/Non-Durable/Services (Table 2.3.5)"""
        return self.get_table("T20305", year=years)

    def get_pce_components(self, years=None):
        """Alias for get_consumer_spending"""
        return self.get_consumer_spending(years)

    def get_personal_income(self, years=None):
        """
        Personal Income - Wages, Social Security, interest, rents (Table 2.1)
        Also includes: Disposable Personal Income (Line 26), Personal Saving Rate (Lines 33-35)
        """
        return self.get_table("T20100", year=years)

    def get_disposable_personal_income(self, years=None):
        """Disposable Personal Income - income after taxes (Table 2.1, Line 26)"""
        return self.get_table("T20100", year=years)

    def get_personal_saving_rate(self, years=None):
        """Personal Saving Rate - % of DPI saved (Table 2.1, Lines 33-35)"""
        return self.get_table("T20100", year=years)

    # =========================================================================
    # CORPORATE / BUSINESS PRODUCTS
    # =========================================================================

    def get_corporate_profits(self, years=None):
        """Corporate Profits - financial health of corporate America (Table 1.12)"""
        return self.get_table("T11200", year=years)

    def get_fixed_assets(self, years=None):
        """Fixed Assets by Type - Buildings, trucks, software, equipment (FAAt101)"""
        return self.get_table("FAAt101", year=years, dataset="FixedAssets")

    def get_industry_fixed_assets(self, years=None):
        """Industry Fixed Assets (FAAt105)"""
        return self.get_table("FAAt105", year=years, dataset="FixedAssets")

    # =========================================================================
    # GOVERNMENT PRODUCTS
    # =========================================================================

    def get_government_receipts_expenditures(self, years=None):
        """Government Receipts and Expenditures - taxes, spending (Table 3.1)"""
        return self.get_table("T30100", year=years)

    def get_government_fixed_assets(self, years=None):
        """Government Fixed Assets (FAAt701)"""
        return self.get_table("FAAt701", year=years, dataset="FixedAssets")

    # =========================================================================
    # PRICE INDEX PRODUCTS
    # =========================================================================

    def get_pce_price_index(self, years=None):
        """PCE Price Index - inflation in prices paid by U.S. residents (Table 2.3.4)"""
        return self.get_table("T20304", year=years)

    def get_core_pce_price_index(self, years=None):
        """Core PCE Price Index - ex Food & Energy, underlying inflation (Table 2.3.4)"""
        return self.get_table("T20304", year=years)

    def get_gdp_price_index(self, years=None):
        """GDP Price Index - price changes for U.S. produced goods/services (Table 1.1.4)"""
        return self.get_table("T10104", year=years)

    def get_gdp_price_deflator(self, years=None):
        """GDP Price Deflator - similar to GDP price index (Table 1.1.9)"""
        return self.get_table("T10109", year=years)

    def get_gross_domestic_purchases_price_index(self, years=None):
        """Gross Domestic Purchases Price Index - featured overall price measure (Table 1.6.4)"""
        return self.get_table("T10604", year=years)

    def get_multiple_tables(self, table_ids, years=None, dataset="NIPA"):
        """
        Fetch multiple tables and combine them.

        Example:
            tables = ["T10105", "T20305", "T11000"]
            df = bea.get_multiple_tables(tables)
        """
        all_dfs = []
        for table_id in table_ids:
            df = self.get_table(table_id, year=years, dataset=dataset)
            if len(df) > 0:
                all_dfs.append(df)
            time.sleep(0.5)  # Be nice to the API

        if all_dfs:
            combined = pd.concat(all_dfs, ignore_index=True)
            return combined
        return pd.DataFrame()

    def get_full_macro_deep_dive(self, years=None):
        """
        Pull ALL key NIPA + FixedAssets tables for maximum granularity.
        Default: Long-term data from 2000-present.

        Includes ALL BEA National Economic Accounts products:
        - GDP (Table 1.1.5)
        - Real GDP Growth (Table 1.1.1)
        - GDI (Table 1.10)
        - Consumer Spending/PCE (Table 2.3.5)
        - Personal Income, DPI, Saving Rate (Table 2.1)
        - Corporate Profits (Table 1.12)
        - Government Receipts & Expenditures (Table 3.1)
        - PCE Price Index (Table 2.3.4)
        - GDP Price Index (Table 1.1.4)
        - Gross Domestic Purchases Price Index (Table 1.6.4)
        - Fixed Assets by Type (FAAt101)
        - Government Fixed Assets (FAAt701)

        Columns: Source_TableID, Source_Dataset, LineNumber, LineDescription, SeriesCode, TimePeriod, DataValue
        """
        print("    Pulling full BEA macro deep dive (ALL products, long-term)...")

        all_dfs = []

        # NIPA Tables
        nipa_tables = [
            "T10105",  # GDP breakdown (Goods, Services, Structures)
            "T10101",  # Real GDP % Change
            "T11000",  # GDI
            "T20305",  # Consumer Spending / PCE by type
            "T20100",  # Personal Income, DPI, Saving Rate
            "T11200",  # Corporate Profits
            "T30100",  # Government Receipts & Expenditures
            "T20304",  # PCE Price Index (includes Core)
            "T10104",  # GDP Price Index
            "T10604",  # Gross Domestic Purchases Price Index
        ]

        for table_id in nipa_tables:
            df = self.get_table(table_id, year=years, dataset="NIPA")
            if len(df) > 0:
                all_dfs.append(df)
            time.sleep(0.5)

        # Fixed Assets Tables (Annual only)
        fixed_assets_tables = [
            "FAAt101",  # Fixed Assets by Type
            "FAAt701",  # Government Fixed Assets
        ]

        for table_id in fixed_assets_tables:
            df = self.get_table(table_id, year=years, dataset="FixedAssets")
            if len(df) > 0:
                all_dfs.append(df)
            time.sleep(0.5)

        if all_dfs:
            combined = pd.concat(all_dfs, ignore_index=True)
            return combined
        return pd.DataFrame()

    def get_granular_view(self, df):
        """
        Format BEA data for granular analysis.

        Returns cleaned DataFrame with key columns.
        """
        if len(df) == 0:
            return df

        output_cols = ['Source_TableID', 'LineNumber', 'LineDescription',
                       'SeriesCode', 'TimePeriod', 'DataValue']
        available_cols = [c for c in output_cols if c in df.columns]
        return df[available_cols].copy()


# =============================================================================
# FED DFA (Distributional Financial Accounts)
# =============================================================================

class FedDFAAPI:
    """Federal Reserve Distributional Financial Accounts"""

    # DFA data download URL
    DFA_URL = "https://www.federalreserve.gov/releases/z1/dataviz/dfa/distribute/chart/data.json"

    def __init__(self):
        self.session = requests.Session()

    def get_wealth_distribution(self):
        """
        Get wealth distribution by percentile group
        Returns shares of total wealth
        """
        try:
            response = self.session.get(self.DFA_URL, timeout=30)
            response.raise_for_status()
            data = response.json()
            print(f"    Fetched Fed DFA wealth data")
            return data
        except Exception as e:
            print(f"    Fed DFA error: {e}")
            return None


# =============================================================================
# CONSOLIDATED DATA ORCHESTRATOR
# =============================================================================

class RealDataFetcher:
    """
    Orchestrates all real data fetching - NO SYNTHETIC DATA
    """

    def __init__(self):
        self.nyfed = NYFedAPI()
        self.treasury = TreasuryAPI()
        self.fred = FREDAPI()
        self.bls = BLSAPI()
        self.bea = BEAAPI()
        self.dfa = FedDFAAPI()

        # Cache for expensive fetches
        self._cache = {}

    def get_sofr_effr_spread(self):
        """SOFR-EFFR spread from NY Fed (with percentiles)"""
        sofr = self.nyfed.get_sofr(last_n=1000)
        effr = self.nyfed.get_effr(last_n=1000)

        if sofr.empty or effr.empty:
            # Fallback to FRED
            sofr_fred = self.fred.get_sofr()
            effr_fred = self.fred.get_effr()
            if len(sofr_fred) > 0 and len(effr_fred) > 0:
                common = sofr_fred.index.intersection(effr_fred.index)
                spread = (sofr_fred.loc[common] - effr_fred.loc[common]) * 100
                return pd.DataFrame({'spread': spread})

        common = sofr.index.intersection(effr.index)
        spread = (sofr.loc[common, 'percentRate'] - effr.loc[common, 'percentRate']) * 100

        result = pd.DataFrame({
            'spread': spread,
            'sofr': sofr.loc[common, 'percentRate'],
            'effr': effr.loc[common, 'percentRate'],
        })

        # Add percentiles if available
        for col in ['percentile1', 'percentile25', 'percentile75', 'percentile99']:
            if col in sofr.columns:
                result[f'sofr_{col}'] = sofr.loc[common, col]

        return result

    def get_repo_dispersion(self):
        """
        Repo rate dispersion from NY Fed
        Returns SOFR, TGCR, BGCR with percentiles
        """
        sofr = self.nyfed.get_sofr(last_n=500)
        tgcr = self.nyfed.get_tgcr(last_n=500)
        bgcr = self.nyfed.get_bgcr(last_n=500)

        result = pd.DataFrame()

        if not sofr.empty:
            result['sofr'] = sofr['percentRate']
            for col in ['percentile1', 'percentile25', 'percentile75', 'percentile99']:
                if col in sofr.columns:
                    result[f'sofr_{col}'] = sofr[col]

        if not tgcr.empty:
            result['tgcr'] = tgcr['percentRate']

        if not bgcr.empty:
            result['bgcr'] = bgcr['percentRate']

        return result

    def get_rrp_usage(self):
        """RRP operations from NY Fed"""
        return self.nyfed.get_rrp_operations()

    def get_srf_usage(self):
        """
        SRF usage from NY Fed repo operations
        Filter for Standing Repo Facility operations
        """
        repo = self.nyfed.get_repo_operations(last_n=500)  # API limit
        # SRF operations typically have specific identifiers
        # The repo endpoint includes all repo ops, filter as needed
        return repo

    def get_yield_curve(self):
        """Full yield curve from FRED"""
        return self.fred.get_yields()

    def get_credit_spreads(self):
        """Credit spreads from FRED"""
        return self.fred.get_credit_spreads()

    def get_auction_data(self):
        """Treasury auction results"""
        return self.treasury.get_auction_results()

    def get_foreign_holdings(self):
        """
        Foreign Treasury holdings - try Treasury API then fallback to FRED
        FRED has foreign official holdings
        """
        # Try Treasury TIC first
        tic = self.treasury.get_tic_holdings()
        if len(tic) > 0:
            return tic

        # Fallback to FRED series for foreign holdings
        print("    Using FRED fallback for foreign holdings...")
        china = self.fred.get_series('FDHBFCNA', '2015-01-01')  # China
        japan = self.fred.get_series('FDHBFJNA', '2015-01-01')  # Japan
        total = self.fred.get_series('FDHBFIN', '2015-01-01')   # Total foreign

        if len(total) > 0:
            return {
                'total_foreign': total,
                'china': china if len(china) > 0 else None,
                'japan': japan if len(japan) > 0 else None,
            }

        return {}

    def get_labor_data(self):
        """Labor market data from BLS and FRED"""
        # BLS JOLTS
        quits = self.bls.get_jolts_quits()
        hires = self.bls.get_jolts_hires()

        # FRED unemployment
        unemp = self.fred.get_unemployment()

        return {
            'quits': quits.get('JTS000000000000000QUR', pd.Series()),
            'hires': hires.get('JTS000000000000000HIR', pd.Series()),
            'unemployment': unemp.get('rate', pd.Series()),
            'long_term_unemp': unemp.get('long_term', pd.Series()),
        }

    def get_reserves_and_rrp(self):
        """Bank reserves and RRP from FRED"""
        return {
            'reserves': self.fred.get_reserves(),
            'rrp': self.fred.get_rrp(),
        }

    def get_wealth_distribution(self):
        """Wealth distribution from Fed DFA"""
        return self.dfa.get_wealth_distribution()

    def get_consumer_data(self):
        """Consumer credit and savings data"""
        return {
            'savings_rate': self.fred.get_savings_rate(),
            'consumer_credit': self.fred.get_consumer_credit(),
        }

    def get_delinquency_data(self):
        """Delinquency rates"""
        return {
            'cre': self.fred.get_cre_delinquency(),
            'auto': self.fred.get_auto_delinquency(),
        }

    def get_gdp_data(self):
        """GDP components"""
        return self.fred.get_gdp()

    def get_debt_data(self):
        """Federal debt data"""
        return self.fred.get_debt()

    def get_vix(self):
        """VIX from FRED"""
        return self.fred.get_vix()

    def get_claims(self):
        """Initial jobless claims"""
        return self.fred.get_initial_claims()


# =============================================================================
# TEST
# =============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("TESTING REAL DATA FETCHER")
    print("=" * 60)

    fetcher = RealDataFetcher()

    print("\n--- NY Fed Reference Rates ---")
    spread = fetcher.get_sofr_effr_spread()
    print(f"SOFR-EFFR spread: {len(spread)} obs")
    if len(spread) > 0:
        print(f"  Latest spread: {spread['spread'].iloc[-1]:.2f} bps")

    print("\n--- NY Fed RRP ---")
    rrp = fetcher.get_rrp_usage()
    print(f"RRP ops: {len(rrp)} ops")
    if len(rrp) > 0:
        print(f"  Latest RRP: ${rrp['totalAmtAccepted'].iloc[-1]:.1f}B")

    print("\n--- FRED Yields ---")
    yields = fetcher.get_yield_curve()
    for tenor, data in yields.items():
        if len(data) > 0:
            print(f"  {tenor}: {data.iloc[-1]:.2f}%")

    print("\n--- FRED Credit Spreads ---")
    spreads = fetcher.get_credit_spreads()
    for name, data in spreads.items():
        if len(data) > 0:
            print(f"  {name}: {data.iloc[-1]*100:.0f} bps")

    print("\n--- BLS JOLTS ---")
    labor = fetcher.get_labor_data()
    if len(labor['quits']) > 0:
        print(f"  Quits rate: {labor['quits'].iloc[-1]:.1f}%")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
