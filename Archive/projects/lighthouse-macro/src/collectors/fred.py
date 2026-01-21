"""
Lighthouse Macro — FRED Data Collector
Federal Reserve Economic Data API client
"""

from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd
import requests

from collectors.base import BaseCollector
from core import get_config


class FREDCollector(BaseCollector):
    """Collector for Federal Reserve Economic Data (FRED)"""

    BASE_URL = "https://api.stlouisfed.org/fred"

    def __init__(self):
        super().__init__(source_name="fred")
        self.api_key = self.config.fred_api_key

        if not self.api_key:
            raise ValueError(
                "FRED API key not found. Set FRED_API_KEY in configs/secrets.env"
            )

    def fetch(
        self,
        series_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Fetch a single FRED series.

        Args:
            series_id: FRED series ID (e.g., 'GDP', 'UNRATE')
            start_date: Start date in YYYY-MM-DD format (optional)
            end_date: End date in YYYY-MM-DD format (optional)

        Returns:
            DataFrame with date index and value column
        """
        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
        }

        if start_date:
            params["observation_start"] = start_date
        if end_date:
            params["observation_end"] = end_date

        url = f"{self.BASE_URL}/series/observations"
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        if "observations" not in data:
            raise ValueError(f"No data returned for series {series_id}")

        # Convert to DataFrame
        df = pd.DataFrame(data["observations"])

        # Filter out missing values represented as '.'
        df = df[df["value"] != "."]

        # Convert to proper types
        df["date"] = pd.to_datetime(df["date"])
        df["value"] = pd.to_numeric(df["value"])

        # Set date as index
        df = df.set_index("date")[["value"]]
        df.columns = [series_id]

        # Save raw data
        self.save_raw(df, series_id)

        return df

    def fetch_bulk(
        self, series_ids: List[str], start_date: Optional[str] = None, **kwargs
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch multiple FRED series.

        Args:
            series_ids: List of FRED series IDs
            start_date: Start date in YYYY-MM-DD format (optional)

        Returns:
            Dictionary mapping series_id to DataFrame
        """
        results = {}

        for series_id in series_ids:
            try:
                df = self.fetch(series_id, start_date=start_date)
                results[series_id] = df
                print(f"✓ Fetched {series_id}: {len(df)} observations")
            except Exception as e:
                print(f"✗ Failed to fetch {series_id}: {str(e)}")
                results[series_id] = None

        return results

    def fetch_by_pillar(
        self, pillar: str, start_date: Optional[str] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch all series for a specific Three Pillars category.

        Args:
            pillar: One of 'macro_dynamics', 'monetary_mechanics', 'market_technicals'
            start_date: Start date in YYYY-MM-DD format (optional)

        Returns:
            Dictionary mapping series_id to DataFrame
        """
        pillar_data = self.config.get_series_by_pillar(pillar)

        if not pillar_data:
            raise ValueError(f"Unknown pillar: {pillar}")

        # Flatten all series from all categories
        all_series = []
        for category, series_list in pillar_data.items():
            if isinstance(series_list, list):
                all_series.extend(series_list)

        print(f"Fetching {len(all_series)} series for pillar: {pillar}")

        return self.fetch_bulk(all_series, start_date=start_date)

    def get_metadata(self, series_id: str) -> Dict:
        """
        Get metadata for a FRED series.

        Args:
            series_id: FRED series ID

        Returns:
            Dictionary with series metadata
        """
        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
        }

        url = f"{self.BASE_URL}/series"
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        if "seriess" in data and len(data["seriess"]) > 0:
            series_info = data["seriess"][0]
            return {
                "series_id": series_id,
                "title": series_info.get("title"),
                "units": series_info.get("units"),
                "frequency": series_info.get("frequency"),
                "seasonal_adjustment": series_info.get("seasonal_adjustment"),
                "last_updated": series_info.get("last_updated"),
                "observation_start": series_info.get("observation_start"),
                "observation_end": series_info.get("observation_end"),
                "source": "FRED",
            }

        return super().get_metadata(series_id)

    def search(self, search_text: str, limit: int = 10) -> List[Dict]:
        """
        Search FRED for series matching text.

        Args:
            search_text: Search query
            limit: Maximum number of results

        Returns:
            List of series metadata dictionaries
        """
        params = {
            "search_text": search_text,
            "api_key": self.api_key,
            "file_type": "json",
            "limit": limit,
        }

        url = f"{self.BASE_URL}/series/search"
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        if "seriess" in data:
            return [
                {
                    "id": s.get("id"),
                    "title": s.get("title"),
                    "frequency": s.get("frequency"),
                    "units": s.get("units"),
                }
                for s in data["seriess"]
            ]

        return []
