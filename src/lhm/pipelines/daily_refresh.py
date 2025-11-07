"""Skeleton implementation of the daily refresh pipeline."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable

from ..clients import FREDClient
from ..config import Category, PipelineConfig, SeriesDefinition, SeriesCatalog


class DailyRefreshPipeline:
    """Coordinate the ingestion of FRED series on a rolling basis."""

    def __init__(self, config: PipelineConfig, client: FREDClient, catalog: SeriesCatalog) -> None:
        self.config = config
        self.client = client
        self.catalog = catalog

    def resolve_refresh_window(self) -> tuple[datetime | None, datetime | None]:
        """Return the date window that should be refreshed.

        The skeleton implementation assumes that the caller will
        re-download the last ``refresh_window_days`` worth of data to
        capture any historical revisions. The concrete implementation will
        be expanded once the stakeholder signs off on the series catalog
        and storage approach.
        """

        end = datetime.utcnow()
        start = end - timedelta(days=self.config.refresh_window_days)
        return start, end

    def iter_catalog(self) -> Iterable[tuple[Category, SeriesDefinition]]:
        """Helper proxy exposing the catalog entries."""

        return self.catalog.iter_series()

    def run(self) -> None:  # pragma: no cover - skeleton placeholder
        """Execute a refresh cycle.

        The method will be populated with the following steps once the
        catalog is approved:

        * resolve the refresh window
        * fetch observations for each series in the catalog
        * persist data to the configured storage backend
        * emit operational metrics/logs
        """

        raise NotImplementedError("DailyRefreshPipeline.run is pending implementation")

    @classmethod
    def load_default_catalog(cls, path: str | Path | None = None) -> SeriesCatalog:
        """Convenience loader for the default catalog path."""

        catalog_path = path or PipelineConfig().catalog_path
        return SeriesCatalog.load(catalog_path)
