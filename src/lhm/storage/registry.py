"""Placeholder registry for storage backends."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from ..config import StorageConfig


class StorageBackend(Protocol):
    """Interface for storage backends used by the pipelines."""

    def save(self, series_id: str, path: Path, payload: object) -> None:  # pragma: no cover - skeleton placeholder
        ...


@dataclass
class StorageRegistry:
    """Registry mapping storage identifiers to backend implementations."""

    config: StorageConfig

    def resolve(self, backend_name: str) -> StorageBackend:  # pragma: no cover - skeleton placeholder
        """Return the backend implementation for ``backend_name``.

        The implementation is intentionally deferred until we decide on the
        canonical storage layout (e.g., Parquet files, DuckDB, Postgres).
        """

        raise NotImplementedError("StorageRegistry.resolve is pending implementation")
