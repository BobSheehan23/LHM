"""
Lighthouse Macro — Base Collector Class
"""

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from core import get_config


class BaseCollector(ABC):
    """Base class for all data collectors"""

    def __init__(self, source_name: str):
        self.source_name = source_name
        self.config = get_config()
        self.raw_data_dir = self.config.data_dir / "raw" / source_name
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def fetch(self, series_id: str, **kwargs) -> pd.DataFrame:
        """
        Fetch data for a specific series.

        Args:
            series_id: Identifier for the data series
            **kwargs: Additional parameters specific to the data source

        Returns:
            DataFrame with the fetched data
        """
        pass

    @abstractmethod
    def fetch_bulk(self, series_ids: List[str], **kwargs) -> Dict[str, pd.DataFrame]:
        """
        Fetch multiple series at once (more efficient when supported).

        Args:
            series_ids: List of series identifiers
            **kwargs: Additional parameters

        Returns:
            Dictionary mapping series_id to DataFrame
        """
        pass

    def save_raw(
        self, data: pd.DataFrame, series_id: str, timestamp: Optional[datetime] = None
    ) -> Path:
        """
        Save raw data to disk with timestamp.

        Args:
            data: DataFrame to save
            series_id: Series identifier
            timestamp: Optional timestamp (defaults to now)

        Returns:
            Path to saved file
        """
        if timestamp is None:
            timestamp = datetime.now()

        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        filename = f"{series_id}_{timestamp_str}.parquet"
        filepath = self.raw_data_dir / filename

        # Save as parquet for efficient storage
        data.to_parquet(filepath, index=True)

        # Also save latest version without timestamp
        latest_path = self.raw_data_dir / f"{series_id}_latest.parquet"
        data.to_parquet(latest_path, index=True)

        return filepath

    def load_latest(self, series_id: str) -> Optional[pd.DataFrame]:
        """
        Load the most recent version of a series.

        Args:
            series_id: Series identifier

        Returns:
            DataFrame if exists, None otherwise
        """
        latest_path = self.raw_data_dir / f"{series_id}_latest.parquet"
        if latest_path.exists():
            return pd.read_parquet(latest_path)
        return None

    def get_metadata(self, series_id: str) -> Dict[str, Any]:
        """
        Get metadata about a series (to be implemented by subclasses).

        Args:
            series_id: Series identifier

        Returns:
            Dictionary with metadata
        """
        return {
            "series_id": series_id,
            "source": self.source_name,
            "last_updated": None,
        }
