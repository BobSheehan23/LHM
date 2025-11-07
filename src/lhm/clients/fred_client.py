"""Minimal FRED client stub for future implementation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable, Protocol


@dataclass(frozen=True)
class FREDSeries:
    """Series metadata returned by FRED."""

    series_id: str
    title: str
    frequency: str | None = None
    observation_start: date | None = None
    observation_end: date | None = None


class HTTPBackend(Protocol):
    """Protocol for HTTP clients used by :class:`FREDClient`."""

    def get(self, url: str, params: dict[str, str]) -> dict:  # pragma: no cover - skeleton placeholder
        ...


class FREDClient:
    """Lightweight wrapper around the FRED API.

    The skeleton client exposes the interface that downstream pipeline
    code will rely on. The actual HTTP implementation will be added in a
    follow-up once the data catalog has been validated.
    """

    def __init__(self, api_key: str | None, base_url: str, http_backend: HTTPBackend | None = None) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._http = http_backend

    def list_series(self, series_ids: Iterable[str]) -> list[FREDSeries]:  # pragma: no cover - skeleton placeholder
        """Return metadata for the requested series.

        Implementation to be provided in the next iteration. The method is
        included so that pipeline code can be prototyped against a stable
        contract.
        """

        raise NotImplementedError("FREDClient.list_series is pending implementation")

    def fetch_observations(
        self,
        series_id: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> None:  # pragma: no cover - skeleton placeholder
        """Download observations for a given series.

        The data retrieval strategy will be implemented after the
        stakeholder confirms the catalog of series.
        """

        raise NotImplementedError("FREDClient.fetch_observations is pending implementation")
