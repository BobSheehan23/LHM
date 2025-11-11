"""Registry for storage backends used by the ingestion pipelines."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, Sequence

from ..clients.fred_client import FREDSeries, Observation
from ..config import Category, SeriesDefinition, StorageConfig
from .filesystem import FilesystemStorageBackend


class StorageBackend(Protocol):
    """Interface for storage backends used by the pipelines."""

    def save(
        self,
        *,
        category: Category,
        series: SeriesDefinition,
        metadata: FREDSeries,
        observations: Sequence[Observation],
        refresh_window: tuple[datetime | None, datetime | None],
    ) -> Path:
        """Persist the provided observations and return the storage path."""


@dataclass
class StorageRegistry:
    """Registry mapping storage identifiers to backend implementations."""

    config: StorageConfig
    _DEFAULT_BACKEND = "filesystem"

    def resolve(self, backend_name: str | None = None) -> StorageBackend:
        """Return the backend implementation for ``backend_name``."""

        backend = (backend_name or self._DEFAULT_BACKEND).lower()
        if backend in {"filesystem", "local", "parquet", "csv", "json"}:
            return FilesystemStorageBackend(self.config)
        raise ValueError(f"Unsupported storage backend '{backend_name}'")
