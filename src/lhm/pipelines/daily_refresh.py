"""Implementation of the daily refresh pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
import logging
from pathlib import Path
from typing import Iterable, Sequence

from ..clients import FREDAPIError, FREDClient
from ..clients.fred_client import Observation
from ..config import Category, PipelineConfig, SeriesDefinition, SeriesCatalog
from ..storage import StorageRegistry

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class SeriesIngestionResult:
    """Capture high level information about a completed series refresh."""

    category: Category
    series: SeriesDefinition
    observations: int
    storage_path: Path
    refresh_window: tuple[datetime | None, datetime | None]


class DailyRefreshPipeline:
    """Coordinate the ingestion of FRED series on a rolling basis."""

    def __init__(
        self,
        config: PipelineConfig,
        client: FREDClient,
        catalog: SeriesCatalog,
        *,
        storage_registry: StorageRegistry | None = None,
    ) -> None:
        self.config = config
        self.client = client
        self.catalog = catalog
        self._storage_registry = storage_registry or StorageRegistry(config.storage)
        self._storage = self._storage_registry.resolve(config.storage_backend)

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

    def run(
        self,
        *,
        full_refresh: bool = False,
        explicit_start: date | None = None,
        explicit_end: date | None = None,
    ) -> list[SeriesIngestionResult]:
        """Execute a refresh cycle and return a summary of completed ingestions."""

        refresh_window = self._resolve_window(full_refresh, explicit_start, explicit_end)
        results: list[SeriesIngestionResult] = []

        for category, definition in self.iter_catalog():
            logger.info("Refreshing series %s (%s)", definition.series_id, category.value)
            try:
                series_metadata = self.client.list_series([definition.series_id])[0]
            except FREDAPIError as exc:  # pragma: no cover - depends on network interactions
                logger.exception("Failed to load metadata for %s: %s", definition.series_id, exc)
                continue

            try:
                observations = self._fetch_series_observations(definition.series_id, refresh_window)
            except FREDAPIError as exc:  # pragma: no cover - depends on network interactions
                logger.exception("Failed to download observations for %s: %s", definition.series_id, exc)
                continue
            storage_path = self._storage.save(
                category=category,
                series=definition,
                metadata=series_metadata,
                observations=observations,
                refresh_window=refresh_window,
            )

            result = SeriesIngestionResult(
                category=category,
                series=definition,
                observations=len(observations),
                storage_path=storage_path,
                refresh_window=refresh_window,
            )
            logger.debug(
                "Stored %s observations for %s at %s", len(observations), definition.series_id, storage_path
            )
            results.append(result)

        return results

    @classmethod
    def load_default_catalog(cls, path: str | Path | None = None) -> SeriesCatalog:
        """Convenience loader for the default catalog path."""

        catalog_path = path or PipelineConfig().catalog_path
        return SeriesCatalog.load(catalog_path)

    # ------------------------------------------------------------------
    def _fetch_series_observations(
        self, series_id: str, refresh_window: tuple[datetime | None, datetime | None]
    ) -> Sequence[Observation]:
        start, end = refresh_window
        return self.client.fetch_observations(
            series_id,
            start_date=start.date() if start else None,
            end_date=end.date() if end else None,
        )

    def _resolve_window(
        self,
        full_refresh: bool,
        explicit_start: date | None,
        explicit_end: date | None,
    ) -> tuple[datetime | None, datetime | None]:
        if full_refresh:
            return None, None

        if explicit_start or explicit_end:
            start = datetime.combine(explicit_start, datetime.min.time()) if explicit_start else None
            end = datetime.combine(explicit_end, datetime.min.time()) if explicit_end else None
            return start, end

        return self.resolve_refresh_window()
