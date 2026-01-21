"""
NY Fed Markets API - Complete Reference & Local Caching
https://markets.newyorkfed.org/beta

This module provides robust fetching with local caching to avoid repeated API failures.
"""

import requests
import pandas as pd
import json
from pathlib import Path
from datetime import datetime, timedelta
import time

# Local cache directory
CACHE_DIR = Path(__file__).parent / "data" / "nyfed_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://markets.newyorkfed.org/api"


class NYFedAPI:
    """NY Fed Markets API with intelligent caching"""

    def __init__(self, cache_hours=24):
        """
        Args:
            cache_hours: Hours before cache expires (default 24)
        """
        self.cache_hours = cache_hours
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Lighthouse-Macro-Research/1.0',
            'Accept': 'application/json'
        })

    def _get_cache_path(self, endpoint):
        """Generate cache file path from endpoint"""
        safe_name = endpoint.replace('/', '_').replace('.', '_')
        return CACHE_DIR / f"{safe_name}.json"

    def _is_cache_valid(self, cache_path):
        """Check if cache exists and is not expired"""
        if not cache_path.exists():
            return False

        mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
        age = datetime.now() - mtime
        return age < timedelta(hours=self.cache_hours)

    def _fetch_with_retry(self, url, max_retries=3):
        """Fetch URL with exponential backoff retry"""
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {e}")
                time.sleep(wait_time)

    def get(self, endpoint, use_cache=True, force_refresh=False):
        """
        Fetch data from NY Fed API with caching

        Args:
            endpoint: API endpoint (e.g., 'rates/secured/sofr/search.json')
            use_cache: Whether to use cached data
            force_refresh: Force refresh even if cache is valid

        Returns:
            dict or list from JSON response
        """
        cache_path = self._get_cache_path(endpoint)

        # Try cache first
        if use_cache and not force_refresh and self._is_cache_valid(cache_path):
            print(f"Using cached data: {endpoint}")
            with open(cache_path, 'r') as f:
                return json.load(f)

        # Fetch from API
        url = f"{BASE_URL}/{endpoint}"
        print(f"Fetching from NY Fed: {endpoint}")
        data = self._fetch_with_retry(url)

        # Save to cache
        with open(cache_path, 'w') as f:
            json.dump(data, f, indent=2)

        return data

    # === REFERENCE RATES ===

    def get_sofr(self, last_n=None, start_date=None, end_date=None):
        """
        Get SOFR (Secured Overnight Financing Rate)

        Args:
            last_n: Last n observations (if None, uses search with dates)
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            DataFrame with SOFR rates
        """
        if last_n:
            endpoint = f"rates/secured/sofr/last/{last_n}.json"
        else:
            endpoint = "rates/secured/sofr/search.json"
            if start_date:
                endpoint += f"?startDate={start_date}"
            if end_date:
                sep = '&' if '?' in endpoint else '?'
                endpoint += f"{sep}endDate={end_date}"

        data = self.get(endpoint)

        if 'refRates' in data:
            df = pd.DataFrame(data['refRates'])
            df['effectiveDate'] = pd.to_datetime(df['effectiveDate'])
            df = df.set_index('effectiveDate').sort_index()

            # Convert rates to float
            for col in ['percentRate', 'percentPercentile1', 'percentPercentile25',
                       'percentPercentile75', 'percentPercentile99']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            return df
        return pd.DataFrame()

    def get_effr(self, last_n=None):
        """Get EFFR (Effective Federal Funds Rate)"""
        endpoint = f"rates/unsecured/effr/last/{last_n or 1000}.json"
        data = self.get(endpoint)

        if 'refRates' in data:
            df = pd.DataFrame(data['refRates'])
            df['effectiveDate'] = pd.to_datetime(df['effectiveDate'])
            df = df.set_index('effectiveDate').sort_index()

            for col in ['percentRate', 'percentPercentile1', 'percentPercentile25',
                       'percentPercentile75', 'percentPercentile99', 'volumeInBillions']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            return df
        return pd.DataFrame()

    def get_obfr(self, last_n=None):
        """Get OBFR (Overnight Bank Funding Rate)"""
        endpoint = f"rates/unsecured/obfr/last/{last_n or 1000}.json"
        data = self.get(endpoint)

        if 'refRates' in data:
            df = pd.DataFrame(data['refRates'])
            df['effectiveDate'] = pd.to_datetime(df['effectiveDate'])
            df = df.set_index('effectiveDate').sort_index()

            for col in ['percentRate', 'volumeInBillions']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            return df
        return pd.DataFrame()

    # === REPO OPERATIONS ===

    def get_rrp_operations(self, start_date=None, end_date=None):
        """
        Get Reverse Repo (RRP) operations
        Endpoint: /api/rp/reverserepo/propositions/search.json

        Args:
            start_date: Start date (YYYY-MM-DD), optional
            end_date: End date (YYYY-MM-DD), optional

        Returns:
            DataFrame with RRP operations
        """
        # Correct endpoint: propositions/search
        endpoint = "rp/reverserepo/propositions/search.json"

        # Add date filters if provided
        if start_date or end_date:
            params = []
            if start_date:
                params.append(f"startDate={start_date}")
            if end_date:
                params.append(f"endDate={end_date}")
            if params:
                endpoint += "?" + "&".join(params)

        data = self.get(endpoint)

        if 'repo' in data and 'operations' in data['repo']:
            df = pd.DataFrame(data['repo']['operations'])
            if 'operationDate' in df.columns:
                df['operationDate'] = pd.to_datetime(df['operationDate'])
                df = df.set_index('operationDate').sort_index()

            # Convert amounts to numeric (millions to billions)
            for col in ['totalAmtAccepted', 'totalAmtSubmitted']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce') / 1000000  # Convert millions to billions

            return df
        return pd.DataFrame()

    def get_repo_operations(self, last_n=250):
        """
        Get Repo operations (Fed lending to dealers)
        Endpoint: /api/rp/repo/results/last/{number}.json
        """
        endpoint = f"rp/repo/results/last/{last_n}.json"
        data = self.get(endpoint)

        if 'repo' in data and 'operations' in data['repo']:
            df = pd.DataFrame(data['repo']['operations'])
            if 'operationDate' in df.columns:
                df['operationDate'] = pd.to_datetime(df['operationDate'])
                df = df.set_index('operationDate').sort_index()

            for col in ['totalAmtAccepted', 'totalAmtSubmitted']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce') / 1000

            return df
        return pd.DataFrame()

    # === PRIMARY DEALER STATISTICS ===

    def get_primary_dealer_latest(self, series_break='PDALL'):
        """
        Get latest Primary Dealer statistics

        Args:
            series_break: Series break code (e.g., 'PDALL', 'PD')

        Returns:
            DataFrame with dealer positioning data
        """
        endpoint = f"pd/latest/{series_break}.json"
        data = self.get(endpoint)

        # This endpoint returns complex nested structure
        # Parse based on actual response structure
        return data

    def get_primary_dealer_timeseries(self, timeseries_id):
        """
        Get specific timeseries from Primary Dealer statistics

        Args:
            timeseries_id: Timeseries/Key ID (get list with list_primary_dealer_series())

        Returns:
            DataFrame
        """
        endpoint = f"pd/get/{timeseries_id}.json"
        data = self.get(endpoint)
        return data

    def list_primary_dealer_series(self):
        """List all available Primary Dealer timeseries"""
        endpoint = "pd/list/timeseries.json"
        data = self.get(endpoint)

        if 'pd' in data and 'timeseries' in data['pd']:
            return pd.DataFrame(data['pd']['timeseries'])
        return pd.DataFrame()

    # === SOMA HOLDINGS ===

    def get_soma_summary(self):
        """Get SOMA (System Open Market Account) holdings summary"""
        endpoint = "soma/summary.json"
        data = self.get(endpoint)

        if 'soma' in data and 'summary' in data['soma']:
            df = pd.DataFrame(data['soma']['summary'])
            return df
        return pd.DataFrame()

    def get_soma_treasury_holdings(self, as_of_date=None):
        """
        Get SOMA Treasury holdings

        Args:
            as_of_date: Date (YYYY-MM-DD), defaults to latest

        Returns:
            DataFrame
        """
        if as_of_date:
            endpoint = f"soma/tsy/get/asof/{as_of_date}.json"
        else:
            # Get latest as of date first
            latest_data = self.get("soma/asofdates/latest.json")
            if 'soma' in latest_data and 'asOfDates' in latest_data['soma']:
                as_of_date = latest_data['soma']['asOfDates'][0]['asOfDate']
                endpoint = f"soma/tsy/get/asof/{as_of_date}.json"
            else:
                return pd.DataFrame()

        data = self.get(endpoint)

        if 'soma' in data and 'holdings' in data['soma']:
            df = pd.DataFrame(data['soma']['holdings'])
            return df
        return pd.DataFrame()

    # === UTILITY METHODS ===

    def clear_cache(self):
        """Clear all cached data"""
        for cache_file in CACHE_DIR.glob("*.json"):
            cache_file.unlink()
        print(f"Cleared {len(list(CACHE_DIR.glob('*.json')))} cache files")

    def get_cache_stats(self):
        """Get statistics about cached data"""
        cache_files = list(CACHE_DIR.glob("*.json"))
        stats = {
            'total_files': len(cache_files),
            'total_size_mb': sum(f.stat().st_size for f in cache_files) / 1024 / 1024,
            'oldest': None,
            'newest': None
        }

        if cache_files:
            mtimes = [datetime.fromtimestamp(f.stat().st_mtime) for f in cache_files]
            stats['oldest'] = min(mtimes)
            stats['newest'] = max(mtimes)

        return stats


# === CONVENIENCE FUNCTIONS ===

def get_money_market_dashboard_data():
    """
    Fetch all data needed for money market dashboard
    Returns dict with SOFR, EFFR, OBFR, RRP
    """
    api = NYFedAPI()

    data = {
        'sofr': api.get_sofr(last_n=1000),
        'effr': api.get_effr(last_n=1000),
        'obfr': api.get_obfr(last_n=1000),
        'rrp': api.get_rrp_operations(last_n=1000),
    }

    return data


def get_dealer_positioning_data():
    """Fetch Primary Dealer positioning data"""
    api = NYFedAPI()

    # Get list of available series first
    series_list = api.list_primary_dealer_series()
    print("Available Primary Dealer series:")
    print(series_list[['keyid', 'label']].head(20) if not series_list.empty else "No series found")

    # Get latest data
    latest = api.get_primary_dealer_latest()

    return {
        'series_list': series_list,
        'latest': latest
    }


def get_soma_data():
    """Fetch SOMA holdings data"""
    api = NYFedAPI()

    data = {
        'summary': api.get_soma_summary(),
        'treasury_holdings': api.get_soma_treasury_holdings(),
    }

    return data


# === EXAMPLE USAGE ===

if __name__ == "__main__":
    # Initialize API
    api = NYFedAPI(cache_hours=24)

    print("=" * 70)
    print("NY FED MARKETS API - DATA PULL")
    print("=" * 70)

    # 1. Money Market Rates
    print("\n1. Fetching Money Market Rates...")
    sofr = api.get_sofr(last_n=500)
    print(f"   SOFR: {len(sofr)} observations, latest = {sofr['percentRate'].iloc[-1]:.2f}%" if not sofr.empty else "   SOFR: No data")

    effr = api.get_effr(last_n=500)
    print(f"   EFFR: {len(effr)} observations, latest = {effr['percentRate'].iloc[-1]:.2f}%" if not effr.empty else "   EFFR: No data")

    obfr = api.get_obfr(last_n=500)
    print(f"   OBFR: {len(obfr)} observations, latest = {obfr['percentRate'].iloc[-1]:.2f}%" if not obfr.empty else "   OBFR: No data")

    # 2. RRP Operations
    print("\n2. Fetching RRP Operations...")
    rrp = api.get_rrp_operations()
    print(f"   RRP: {len(rrp)} operations, latest = ${rrp['totalAmtAccepted'].iloc[-1]:.1f}B" if not rrp.empty else "   RRP: No data")

    # 3. Primary Dealer Stats
    print("\n3. Fetching Primary Dealer Statistics...")
    series_list = api.list_primary_dealer_series()
    print(f"   Found {len(series_list)} available timeseries" if not series_list.empty else "   No series data")

    # 4. SOMA Holdings
    print("\n4. Fetching SOMA Holdings...")
    soma_summary = api.get_soma_summary()
    print(f"   SOMA summary: {len(soma_summary)} rows" if not soma_summary.empty else "   SOMA: No data")

    # Cache stats
    print("\n" + "=" * 70)
    stats = api.get_cache_stats()
    print(f"Cache Statistics:")
    print(f"  Files: {stats['total_files']}")
    print(f"  Size: {stats['total_size_mb']:.2f} MB")
    if stats['oldest']:
        print(f"  Oldest: {stats['oldest'].strftime('%Y-%m-%d %H:%M')}")
        print(f"  Newest: {stats['newest'].strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
