"""
OFR (Office of Financial Research) API - Complete Reference & Local Caching
https://data.financialresearch.gov/

Includes:
- Short-term Funding Monitor (STFM) API
- Hedge Fund Monitor (HFM) API

No tokens or registration required - open public interface
"""

import requests
import pandas as pd
import json
from pathlib import Path
from datetime import datetime, timedelta
import time
import io

# Local cache directory
CACHE_DIR = Path(__file__).parent / "data" / "ofr_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

STFM_BASE_URL = "https://data.financialresearch.gov/v1"
HFM_BASE_URL = "https://data.financialresearch.gov/hf/v1"


class OFRAPI:
    """
    OFR API with intelligent caching
    Supports both STFM (Short-term Funding Monitor) and HFM (Hedge Fund Monitor)
    """

    def __init__(self, cache_hours=24, api_type='stfm'):
        """
        Args:
            cache_hours: Hours before cache expires (default 24)
            api_type: 'stfm' for Short-term Funding or 'hfm' for Hedge Fund (default 'stfm')
        """
        self.cache_hours = cache_hours
        self.api_type = api_type.lower()
        self.base_url = HFM_BASE_URL if self.api_type == 'hfm' else STFM_BASE_URL

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Lighthouse-Macro-Research/1.0',
            'Accept': 'application/json'
        })

    def _get_cache_path(self, endpoint):
        """Generate cache file path from endpoint"""
        safe_name = f"{self.api_type}_{endpoint.replace('/', '_').replace('?', '_').replace('=', '_').replace('.', '_')}"
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
                wait_time = 2 ** attempt
                print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {e}")
                time.sleep(wait_time)

    def get(self, endpoint, use_cache=True, force_refresh=False):
        """
        Fetch data from OFR API with caching

        Args:
            endpoint: API endpoint (e.g., 'metadata/mnemonics')
            use_cache: Whether to use cached data
            force_refresh: Force refresh even if cache is valid

        Returns:
            dict or list from JSON response
        """
        cache_path = self._get_cache_path(endpoint)

        # Try cache first
        if use_cache and not force_refresh and self._is_cache_valid(cache_path):
            print(f"Using cached OFR data: {endpoint}")
            with open(cache_path, 'r') as f:
                return json.load(f)

        # Fetch from API
        url = f"{self.base_url}/{endpoint}"
        print(f"Fetching from OFR: {endpoint}")
        data = self._fetch_with_retry(url)

        # Save to cache
        with open(cache_path, 'w') as f:
            json.dump(data, f, indent=2)

        return data

    def get_csv(self, endpoint, use_cache=True, force_refresh=False):
        """
        Fetch CSV data from OFR API with caching (used for HFM categories)

        Args:
            endpoint: API endpoint that returns CSV
            use_cache: Whether to use cached data
            force_refresh: Force refresh even if cache is valid

        Returns:
            pandas DataFrame
        """
        cache_path = self._get_cache_path(endpoint).with_suffix('.csv')

        # Try cache first
        if use_cache and not force_refresh and self._is_cache_valid(cache_path):
            print(f"Using cached OFR CSV data: {endpoint}")
            return pd.read_csv(cache_path)

        # Fetch from API
        url = f"{self.base_url}/{endpoint}"
        print(f"Fetching CSV from OFR: {endpoint}")

        for attempt in range(3):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()

                # Parse CSV
                df = pd.read_csv(io.StringIO(response.text))

                # Save to cache
                df.to_csv(cache_path, index=False)

                return df
            except requests.exceptions.RequestException as e:
                if attempt == 2:
                    raise
                wait_time = 2 ** attempt
                print(f"Retry {attempt + 1}/3 after {wait_time}s: {e}")
                time.sleep(wait_time)

        return pd.DataFrame()

    # === METADATA ENDPOINTS ===

    def list_all_mnemonics(self):
        """
        Get all available series mnemonics (unique identifiers)
        Endpoint: /metadata/mnemonics/

        Returns:
            List of all series identifiers
        """
        endpoint = "metadata/mnemonics/"
        data = self.get(endpoint)
        return data

    def get_series_metadata(self, mnemonic):
        """
        Get metadata for a specific series

        Args:
            mnemonic: Series identifier (e.g., 'REPO-TRI_AR_OO-P')

        Returns:
            dict with series metadata
        """
        endpoint = f"metadata/query/{mnemonic}"
        data = self.get(endpoint)
        return data

    def search_series(self, query_term):
        """
        Search for series matching a query term

        Args:
            query_term: Search term (e.g., 'repo', 'treasury', 'rate')

        Returns:
            List of matching series with metadata
        """
        endpoint = f"metadata/search/{query_term}"
        data = self.get(endpoint)
        return data

    # === DATA ENDPOINTS ===

    def get_timeseries(self, mnemonic, start_date=None, end_date=None):
        """
        Get time series data for a single series

        Args:
            mnemonic: Series identifier
            start_date: Start date (YYYY-MM-DD), optional
            end_date: End date (YYYY-MM-DD), optional

        Returns:
            DataFrame with time series data
        """
        endpoint = f"series/timeseries/{mnemonic}"

        # Add date filters if provided
        params = []
        if start_date:
            params.append(f"start_date={start_date}")
        if end_date:
            params.append(f"end_date={end_date}")
        if params:
            endpoint += "?" + "&".join(params)

        data = self.get(endpoint)

        # Convert to DataFrame
        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                df = df.set_index('date').sort_index()
            return df
        return pd.DataFrame()

    def get_full_series(self, mnemonic):
        """
        Get both metadata and data for a single series

        Args:
            mnemonic: Series identifier

        Returns:
            dict with 'metadata' and 'data' keys
        """
        endpoint = f"series/full/{mnemonic}"
        data = self.get(endpoint)

        result = {
            'metadata': data.get('metadata', {}),
            'data': pd.DataFrame()
        }

        # Convert data to DataFrame
        if 'data' in data and isinstance(data['data'], list):
            df = pd.DataFrame(data['data'])
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                df = df.set_index('date').sort_index()
            result['data'] = df

        return result

    def get_multiple_series(self, mnemonics):
        """
        Get metadata and data for multiple series

        Args:
            mnemonics: List of series identifiers

        Returns:
            dict with series mnemonics as keys
        """
        # OFR API format: comma-separated list
        mnemonic_str = ','.join(mnemonics)
        endpoint = f"series/multifull/{mnemonic_str}"
        data = self.get(endpoint)

        results = {}
        for mnemonic in mnemonics:
            if mnemonic in data:
                series_data = data[mnemonic]
                results[mnemonic] = {
                    'metadata': series_data.get('metadata', {}),
                    'data': pd.DataFrame()
                }

                if 'data' in series_data and isinstance(series_data['data'], list):
                    df = pd.DataFrame(series_data['data'])
                    if 'date' in df.columns:
                        df['date'] = pd.to_datetime(df['date'])
                        df = df.set_index('date').sort_index()
                    results[mnemonic]['data'] = df

        return results

    def get_dataset(self, dataset_name):
        """
        Get all series in a specified dataset

        Args:
            dataset_name: Name of dataset (e.g., 'repo', 'cp', 'abcp')

        Returns:
            dict with all series in dataset
        """
        endpoint = f"series/dataset/{dataset_name}"
        data = self.get(endpoint)
        return data

    def calculate_spread(self, mnemonic1, mnemonic2):
        """
        Calculate spread between two series

        Args:
            mnemonic1: First series identifier
            mnemonic2: Second series identifier

        Returns:
            DataFrame with spread values
        """
        endpoint = f"calc/spread/{mnemonic1}/{mnemonic2}"
        data = self.get(endpoint)

        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                df = df.set_index('date').sort_index()
            return df
        return pd.DataFrame()

    # === CONVENIENCE METHODS FOR KEY SERIES ===

    def get_repo_rates(self):
        """
        Get key repo market rates

        Common repo series:
        - REPO-TRI_AR_OO-P: Tri-party repo overnight rate
        - REPO-DVP_AR_OO-P: DVP repo overnight rate
        """
        # Known key repo series mnemonics
        key_series = [
            'REPO-TRI_AR_OO-P',  # Tri-party repo overnight
            'REPO-DVP_AR_OO-P',  # DVP repo overnight
        ]

        results = {}
        for mnemonic in key_series:
            try:
                results[mnemonic] = self.get_full_series(mnemonic)
            except Exception as e:
                print(f"Failed to fetch {mnemonic}: {e}")

        return results

    def get_commercial_paper_rates(self):
        """
        Get commercial paper rates

        Common CP series:
        - CP-AA_AR_OO-P: AA-rated overnight CP
        - CP-A2P2_AR_OO-P: A2/P2-rated overnight CP
        """
        # Known key CP series mnemonics
        key_series = [
            'CP-AA_AR_OO-P',     # AA-rated overnight
            'CP-A2P2_AR_OO-P',   # A2/P2-rated overnight
        ]

        results = {}
        for mnemonic in key_series:
            try:
                results[mnemonic] = self.get_full_series(mnemonic)
            except Exception as e:
                print(f"Failed to fetch {mnemonic}: {e}")

        return results

    def get_financial_stress_indicators(self):
        """
        Get financial stress indicators from OFR

        Returns:
            dict with stress indicator data
        """
        # Known stress indicator mnemonics (would need to be populated from API docs)
        stress_series = []  # Placeholder - would need actual mnemonic list

        indicators = {}
        for mnemonic in stress_series:
            try:
                indicators[mnemonic] = self.get_timeseries(mnemonic)
            except Exception as e:
                print(f"Failed to fetch {mnemonic}: {e}")

        return indicators

    # === HEDGE FUND MONITOR (HFM) ENDPOINTS ===

    def get_hfm_category(self, category_name):
        """
        Get Hedge Fund Monitor category data (CSV format)

        Args:
            category_name: Category name (e.g., 'aum', 'leverage', 'liquidity')

        Returns:
            DataFrame with category data

        Available categories (as of latest API docs):
        - aum: Assets Under Management
        - leverage: Leverage metrics
        - liquidity: Liquidity metrics
        - performance: Performance metrics
        - concentration: Concentration metrics
        """
        if self.api_type != 'hfm':
            print("Warning: Switching to HFM API for category data")

        endpoint = f"categories/{category_name}"
        df = self.get_csv(endpoint)

        # Parse date column if present
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date').sort_index()

        return df

    def get_hfm_all_categories(self):
        """
        Get all available HFM categories

        Returns:
            dict with category name as key and DataFrame as value
        """
        categories = ['aum', 'leverage', 'liquidity', 'performance', 'concentration']
        results = {}

        for cat in categories:
            try:
                results[cat] = self.get_hfm_category(cat)
                print(f"✓ Fetched HFM category: {cat}")
            except Exception as e:
                print(f"✗ Failed to fetch HFM category {cat}: {e}")

        return results

    # === UTILITY METHODS ===

    def clear_cache(self):
        """Clear all cached data"""
        for cache_file in CACHE_DIR.glob("*.json"):
            cache_file.unlink()
        print(f"Cleared {len(list(CACHE_DIR.glob('*.json')))} OFR cache files")

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

def get_money_market_data():
    """
    Fetch comprehensive money market data from OFR

    Returns:
        dict with repo, CP, and other money market data
    """
    api = OFRAPI()

    data = {
        'repo_rates': api.get_repo_rates(),
        'cp_rates': api.get_commercial_paper_rates(),
    }

    return data


def get_all_available_series():
    """
    Get list of all available OFR series

    Returns:
        List of all series mnemonics with descriptions
    """
    api = OFRAPI()
    mnemonics = api.list_all_mnemonics()

    # Get metadata for each
    series_info = []
    if isinstance(mnemonics, list):
        for mnemonic in mnemonics[:50]:  # Limit to first 50 for performance
            try:
                metadata = api.get_series_metadata(mnemonic)
                series_info.append({
                    'mnemonic': mnemonic,
                    'metadata': metadata
                })
            except:
                pass

    return series_info


# === EXAMPLE USAGE ===

if __name__ == "__main__":
    print("=" * 70)
    print("OFR API - DATA PULL (STFM + HFM)")
    print("=" * 70)

    # === PART 1: SHORT-TERM FUNDING MONITOR (STFM) ===
    print("\n" + "=" * 70)
    print("PART 1: SHORT-TERM FUNDING MONITOR (STFM)")
    print("=" * 70)

    stfm_api = OFRAPI(cache_hours=24, api_type='stfm')

    # 1. List available series
    print("\n1. Fetching available series...")
    mnemonics = stfm_api.list_all_mnemonics()
    print(f"   Total series available: {len(mnemonics) if isinstance(mnemonics, list) else 'Unknown'}")

    # 2. Get metadata for first few mnemonics
    print("\n2. Getting metadata for sample series...")
    if isinstance(mnemonics, list) and len(mnemonics) > 0:
        for mnemonic in mnemonics[:3]:
            try:
                metadata = stfm_api.get_series_metadata(mnemonic)
                print(f"   {mnemonic}: {metadata.get('name', 'N/A')[:60]}")
            except Exception as e:
                print(f"   {mnemonic}: Failed to fetch metadata - {e}")

    # 3. Get specific series data (try a common repo series)
    print("\n3. Fetching specific time series...")
    if isinstance(mnemonics, list) and len(mnemonics) > 0:
        # Try first available mnemonic
        first_series = mnemonics[0]
        try:
            ts_data = stfm_api.get_timeseries(first_series)
            if not ts_data.empty:
                print(f"   {first_series}: {len(ts_data)} observations")
                print(f"   Latest value: {ts_data.iloc[-1].values[0] if len(ts_data.columns) > 0 else 'N/A'}")
            else:
                print(f"   {first_series}: No data available")
        except Exception as e:
            print(f"   {first_series}: Failed to fetch data - {e}")

    # 4. Get repo rates convenience method
    print("\n4. Fetching repo rates (convenience method)...")
    repo_rates = stfm_api.get_repo_rates()
    print(f"   Retrieved {len(repo_rates)} repo rate series")

    # === PART 2: HEDGE FUND MONITOR (HFM) ===
    print("\n" + "=" * 70)
    print("PART 2: HEDGE FUND MONITOR (HFM)")
    print("=" * 70)

    hfm_api = OFRAPI(cache_hours=24, api_type='hfm')

    # 1. Get AUM data
    print("\n1. Fetching Hedge Fund AUM data...")
    try:
        aum_data = hfm_api.get_hfm_category('aum')
        if not aum_data.empty:
            print(f"   AUM data: {len(aum_data)} observations")
            print(f"   Columns: {list(aum_data.columns)}")
        else:
            print("   AUM data: No data available")
    except Exception as e:
        print(f"   Failed to fetch AUM data: {e}")

    # 2. Get leverage data
    print("\n2. Fetching Hedge Fund leverage data...")
    try:
        leverage_data = hfm_api.get_hfm_category('leverage')
        if not leverage_data.empty:
            print(f"   Leverage data: {len(leverage_data)} observations")
            print(f"   Columns: {list(leverage_data.columns)}")
        else:
            print("   Leverage data: No data available")
    except Exception as e:
        print(f"   Failed to fetch leverage data: {e}")

    # 3. Get all categories
    print("\n3. Fetching all HFM categories...")
    all_hfm = hfm_api.get_hfm_all_categories()
    for cat_name, df in all_hfm.items():
        if not df.empty:
            print(f"   {cat_name}: {len(df)} rows, {len(df.columns)} columns")

    # === CACHE STATS ===
    print("\n" + "=" * 70)
    stats = stfm_api.get_cache_stats()
    print(f"OFR Cache Statistics:")
    print(f"  Files: {stats['total_files']}")
    print(f"  Size: {stats['total_size_mb']:.2f} MB")
    if stats['oldest']:
        print(f"  Oldest: {stats['oldest'].strftime('%Y-%m-%d %H:%M')}")
        print(f"  Newest: {stats['newest'].strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
