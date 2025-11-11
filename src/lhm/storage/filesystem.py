"""Local filesystem storage backend for FRED series observations."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
import json
from pathlib import Path
from typing import Sequence

from ..clients.fred_client import FREDSeries, Observation
from ..config import Category, SeriesDefinition, StorageConfig
from .registry import StorageBackend


class FilesystemStorageBackend(StorageBackend):
    """Persist series observations and metadata on the local filesystem."""

    def __init__(self, config: StorageConfig) -> None:
        self._config = config
        self._root = Path(config.root_path)
        self._format = (config.format or "parquet").lower()

    # ------------------------------------------------------------------
    def save(
        self,
        *,
        category: Category,
        series: SeriesDefinition,
        metadata: FREDSeries,
        observations: Sequence[Observation],
        refresh_window: tuple[datetime | None, datetime | None],
    ) -> Path:
        """Persist observations to disk and return the materialised path."""

        destination = self._normalise_destination(category, series)
        destination.mkdir(parents=True, exist_ok=True)

        observations_path = self._write_observations(destination, observations)
        self._write_metadata(destination, series, metadata, refresh_window)

        return observations_path

    # ------------------------------------------------------------------
    def _normalise_destination(self, category: Category, series: SeriesDefinition) -> Path:
        return self._root / category.value / series.series_id.lower()

    def _write_observations(self, destination: Path, observations: Sequence[Observation]) -> Path:
        if self._format == "csv":
            return self._write_csv(destination, observations)
        if self._format == "json":
            return self._write_json(destination, observations)
        if self._format == "parquet":
            return self._write_parquet(destination, observations)
        raise ValueError(f"Unsupported storage format '{self._format}'")

    def _write_csv(self, destination: Path, observations: Sequence[Observation]) -> Path:
        import csv

        path = destination / f"observations.csv"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["realtime_start", "realtime_end", "date", "value", "raw_value"])
            for entry in observations:
                writer.writerow(
                    [
                        entry.realtime_start.isoformat(),
                        entry.realtime_end.isoformat(),
                        entry.observation_date.isoformat(),
                        "" if entry.value is None else f"{entry.value:.16g}",
                        entry.raw_value,
                    ]
                )
        return path

    def _write_json(self, destination: Path, observations: Sequence[Observation]) -> Path:
        path = destination / "observations.json"
        serialised = [
            {
                "realtime_start": entry.realtime_start.isoformat(),
                "realtime_end": entry.realtime_end.isoformat(),
                "date": entry.observation_date.isoformat(),
                "value": entry.value,
                "raw_value": entry.raw_value,
            }
            for entry in observations
        ]
        with path.open("w", encoding="utf-8") as handle:
            json.dump(serialised, handle, indent=2)
        return path

    def _write_parquet(self, destination: Path, observations: Sequence[Observation]) -> Path:
        try:
            import pandas as pd
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise RuntimeError(
                "Parquet storage requires the optional 'pandas' dependency. "
                "Install pandas (and pyarrow/fastparquet) or switch to CSV/JSON."
            ) from exc

        frame = pd.DataFrame(
            {
                "realtime_start": [entry.realtime_start for entry in observations],
                "realtime_end": [entry.realtime_end for entry in observations],
                "date": [entry.observation_date for entry in observations],
                "value": [entry.value for entry in observations],
                "raw_value": [entry.raw_value for entry in observations],
            }
        )
        path = destination / "observations.parquet"
        frame.to_parquet(path, index=False)
        return path

    def _write_metadata(
        self,
        destination: Path,
        series: SeriesDefinition,
        metadata: FREDSeries,
        refresh_window: tuple[datetime | None, datetime | None],
    ) -> None:
        payload = {
            "series": asdict(series),
            "fred_metadata": asdict(metadata),
            "ingested_at_utc": datetime.utcnow().isoformat(timespec="seconds"),
            "refresh_window": {
                "start": refresh_window[0].isoformat() if refresh_window[0] else None,
                "end": refresh_window[1].isoformat() if refresh_window[1] else None,
            },
            "storage_format": self._format,
        }

        with (destination / "metadata.json").open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)

