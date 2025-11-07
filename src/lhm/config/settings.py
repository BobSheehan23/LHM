"""Settings dataclasses used to configure the data platform."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class FREDConfig:
    """Connection parameters for the FRED API."""

    api_key: str | None = None
    base_url: str = "https://api.stlouisfed.org"
    rate_limit_per_minute: int = 60


@dataclass(slots=True)
class StorageConfig:
    """Describe how fetched series should be stored locally."""

    root_path: Path = Path("data/raw/fred")
    format: str = "parquet"


@dataclass(slots=True)
class PipelineConfig:
    """Top-level configuration for the recurring ingestion pipeline."""

    fred: FREDConfig = FREDConfig()
    storage: StorageConfig = StorageConfig()
    catalog_path: Path = Path("configs/fred_series_catalog.yaml")
    refresh_window_days: int = 7
