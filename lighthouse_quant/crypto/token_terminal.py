"""
Token Terminal API Client
=========================
Standardized interface to Token Terminal's on-chain metrics API.

Usage:
    from lighthouse_quant.crypto import TokenTerminalClient

    client = TokenTerminalClient()
    eth_metrics = client.get_metrics('ethereum', days=30)
    all_projects = client.get_projects()
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import time
import os

# API Configuration
API_KEY = os.environ.get('TOKEN_TERMINAL_API_KEY', '348c4261-f49b-4517-949c-e18ef6a6c300')
BASE_URL = 'https://api.tokenterminal.com/v2'


class TokenTerminalClient:
    """
    Token Terminal API Client with rate limiting and caching.
    """

    # Metric categories for batch fetching
    METRIC_GROUPS = {
        'market': [
            'market_cap_fully_diluted', 'market_cap_circulating',
            'token_trading_volume', 'tokenholders', 'price',
            'token_supply_maximum', 'token_supply_circulating'
        ],
        'financial': [
            'fees', 'revenue', 'take_rate', 'gross_profit', 'earnings',
            'token_incentives', 'expenses', 'treasury', 'treasury_net',
            'tvl', 'active_loans', 'trading_volume'
        ],
        'usage': [
            'user_dau', 'user_wau', 'user_mau',
            'active_addresses_daily', 'active_addresses_monthly',
            'transaction_count', 'afpu', 'arpu'
        ],
        'valuation': [
            'pf_circulating', 'pf_fully_diluted',
            'ps_circulating', 'ps_fully_diluted'
        ],
        'development': [
            'active_developers', 'code_commits',
            'contracts_deployed', 'contract_deployers'
        ],
        'ecosystem': [
            'ecosystem_fees', 'ecosystem_tvl', 'ecosystem_active_loans',
            'ecosystem_stablecoin_supply', 'gdp'
        ]
    }

    def __init__(self, api_key: str = None, rate_limit_delay: float = 0.25):
        """
        Initialize the Token Terminal client.

        Args:
            api_key: Token Terminal API key. Defaults to env var or hardcoded key.
            rate_limit_delay: Seconds to wait between API calls (default 0.25s = 4 req/sec)
        """
        self.api_key = api_key or API_KEY
        self.base_url = BASE_URL
        self.rate_limit_delay = rate_limit_delay
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        self._cache = {}
        self._last_request_time = 0

    def _rate_limit(self):
        """Enforce rate limiting between requests."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self._last_request_time = time.time()

    def _request(self, endpoint: str, params: dict = None) -> Optional[dict]:
        """
        Make a rate-limited request to the API.

        Args:
            endpoint: API endpoint (without base URL)
            params: Query parameters

        Returns:
            JSON response data or None on error
        """
        self._rate_limit()
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                # Rate limited, wait and retry once
                print(f"Rate limited, waiting 5s...")
                time.sleep(5)
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
                if response.status_code == 200:
                    return response.json()
            else:
                print(f"API Error {response.status_code}: {response.text[:200]}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    # ==========================================
    # PROJECT ENDPOINTS
    # ==========================================

    def get_projects(self, include_archived: bool = False) -> pd.DataFrame:
        """
        Get list of all available projects.

        Args:
            include_archived: Include archived/inactive projects

        Returns:
            DataFrame with project metadata
        """
        data = self._request('/projects')
        if not data or 'data' not in data:
            return pd.DataFrame()

        df = pd.DataFrame(data['data'])

        if not include_archived:
            df = df[df['is_archived'] == False]

        return df

    def search_projects(self, query: str) -> pd.DataFrame:
        """
        Search for projects by name or symbol.

        Args:
            query: Search string

        Returns:
            DataFrame of matching projects
        """
        projects = self.get_projects()
        if projects.empty:
            return projects

        query_lower = query.lower()
        mask = (
            projects['name'].str.lower().str.contains(query_lower, na=False) |
            projects['symbol'].str.lower().str.contains(query_lower, na=False) |
            projects['project_id'].str.lower().str.contains(query_lower, na=False)
        )
        return projects[mask]

    # ==========================================
    # METRICS ENDPOINTS
    # ==========================================

    def get_metrics(
        self,
        project_id: str,
        days: int = 30,
        metric_ids: List[str] = None
    ) -> pd.DataFrame:
        """
        Get time series metrics for a project.

        Args:
            project_id: Token Terminal project ID (e.g., 'ethereum', 'aave')
            days: Number of days of history to fetch
            metric_ids: Specific metrics to fetch (None = all available)

        Returns:
            DataFrame with date index and metric columns
        """
        params = {'limit': days}
        if metric_ids:
            params['metric_ids'] = ','.join(metric_ids)

        data = self._request(f'/projects/{project_id}/metrics', params)

        if not data or 'data' not in data:
            return pd.DataFrame()

        df = pd.DataFrame(data['data'])

        if 'timestamp' in df.columns:
            df['date'] = pd.to_datetime(df['timestamp']).dt.date
            df = df.set_index('date').sort_index()

        return df

    def get_latest_metrics(self, project_id: str) -> pd.Series:
        """
        Get the most recent metrics snapshot for a project.

        Args:
            project_id: Token Terminal project ID

        Returns:
            Series with latest metric values
        """
        df = self.get_metrics(project_id, days=1)
        if df.empty:
            return pd.Series(dtype=float)
        return df.iloc[-1]

    def get_metric_history(
        self,
        project_id: str,
        metric_id: str,
        days: int = 365
    ) -> pd.Series:
        """
        Get historical time series for a single metric.

        Args:
            project_id: Token Terminal project ID
            metric_id: Specific metric to fetch
            days: Days of history

        Returns:
            Series with date index
        """
        df = self.get_metrics(project_id, days=days, metric_ids=[metric_id])
        if df.empty or metric_id not in df.columns:
            return pd.Series(dtype=float)
        return df[metric_id]

    # ==========================================
    # BATCH OPERATIONS
    # ==========================================

    def get_metrics_batch(
        self,
        project_ids: List[str],
        days: int = 1,
        metrics: List[str] = None
    ) -> pd.DataFrame:
        """
        Fetch metrics for multiple projects.

        Args:
            project_ids: List of project IDs
            days: Days of history per project
            metrics: Specific metrics to fetch

        Returns:
            DataFrame with multi-index (project_id, date)
        """
        all_data = []

        for pid in project_ids:
            print(f"  Fetching {pid}...")
            df = self.get_metrics(pid, days=days, metric_ids=metrics)
            if not df.empty:
                df['project_id'] = pid
                all_data.append(df.reset_index())

        if not all_data:
            return pd.DataFrame()

        combined = pd.concat(all_data, ignore_index=True)
        return combined

    def get_sector_comparison(
        self,
        project_ids: List[str],
        metrics: List[str] = None
    ) -> pd.DataFrame:
        """
        Get latest metrics for multiple projects for comparison.

        Args:
            project_ids: List of project IDs to compare
            metrics: Metrics to include (default = valuation + financial)

        Returns:
            DataFrame with projects as rows, metrics as columns
        """
        if metrics is None:
            metrics = self.METRIC_GROUPS['valuation'] + self.METRIC_GROUPS['financial'][:6]

        results = []
        for pid in project_ids:
            latest = self.get_latest_metrics(pid)
            if not latest.empty:
                latest['project_id'] = pid
                results.append(latest)

        if not results:
            return pd.DataFrame()

        df = pd.DataFrame(results)
        df = df.set_index('project_id')

        # Keep only requested metrics that exist
        available_metrics = [m for m in metrics if m in df.columns]
        return df[available_metrics]

    # ==========================================
    # CONVENIENCE METHODS
    # ==========================================

    def get_top_by_metric(
        self,
        metric: str,
        n: int = 20,
        ascending: bool = False
    ) -> pd.DataFrame:
        """
        Get top N projects ranked by a specific metric.

        Note: This requires fetching all projects, which is slow.
        Consider caching the results.

        Args:
            metric: Metric to rank by (e.g., 'fees', 'tvl')
            n: Number of top projects
            ascending: Sort ascending (lowest first)

        Returns:
            DataFrame of top projects with the metric
        """
        projects = self.get_projects()
        if projects.empty:
            return pd.DataFrame()

        # Get latest metrics for each project (expensive operation)
        results = []
        for pid in projects['project_id'].head(100):  # Limit to prevent timeout
            latest = self.get_latest_metrics(pid)
            if not latest.empty and metric in latest.index:
                results.append({
                    'project_id': pid,
                    'name': projects[projects['project_id'] == pid]['name'].values[0],
                    metric: latest[metric]
                })

        if not results:
            return pd.DataFrame()

        df = pd.DataFrame(results)
        df = df.sort_values(metric, ascending=ascending).head(n)
        return df.reset_index(drop=True)


# ==========================================
# STANDALONE FUNCTIONS
# ==========================================

def fetch_project_snapshot(project_id: str) -> Dict:
    """
    Quick fetch of key metrics for a single project.

    Args:
        project_id: Token Terminal project ID

    Returns:
        Dictionary of key metrics
    """
    client = TokenTerminalClient()
    latest = client.get_latest_metrics(project_id)

    if latest.empty:
        return {}

    return {
        'project_id': project_id,
        'date': str(latest.name) if hasattr(latest, 'name') else None,
        # Market
        'market_cap': latest.get('market_cap_circulating'),
        'fdv': latest.get('market_cap_fully_diluted'),
        'price': latest.get('price'),
        # Financial
        'fees': latest.get('fees'),
        'revenue': latest.get('revenue'),
        'earnings': latest.get('earnings'),
        'token_incentives': latest.get('token_incentives'),
        'tvl': latest.get('tvl'),
        # Usage
        'dau': latest.get('user_dau'),
        'mau': latest.get('user_mau'),
        # Valuation
        'pf_ratio': latest.get('pf_fully_diluted'),
        'ps_ratio': latest.get('ps_fully_diluted'),
    }


# CLI Testing
if __name__ == "__main__":
    print("Token Terminal Client Test")
    print("=" * 50)

    client = TokenTerminalClient()

    # Test: Get projects
    print("\n1. Fetching projects...")
    projects = client.get_projects()
    print(f"   Total projects: {len(projects)}")

    # Test: Search
    print("\n2. Searching for 'ethereum'...")
    eth_search = client.search_projects('ethereum')
    print(f"   Found: {eth_search['name'].tolist()[:5]}")

    # Test: Get metrics
    print("\n3. Fetching Ethereum metrics (30 days)...")
    eth_metrics = client.get_metrics('ethereum', days=30)
    print(f"   Columns: {eth_metrics.columns.tolist()[:10]}...")
    print(f"   Date range: {eth_metrics.index.min()} to {eth_metrics.index.max()}")

    # Test: Latest snapshot
    print("\n4. Latest Ethereum snapshot...")
    latest = client.get_latest_metrics('ethereum')
    print(f"   Fees: ${latest.get('fees', 0):,.0f}")
    print(f"   Revenue: ${latest.get('revenue', 0):,.0f}")
    print(f"   DAU: {latest.get('user_dau', 0):,.0f}")
    print(f"   P/F Ratio: {latest.get('pf_fully_diluted', 0):,.1f}")

    print("\n" + "=" * 50)
    print("Test complete.")
