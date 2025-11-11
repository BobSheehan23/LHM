"""HTTP client responsible for interacting with the public FRED API."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
import json
import time
from typing import Iterable, Iterator, Mapping, Sequence
from urllib import parse, request


class FREDAPIError(RuntimeError):
    """Raised when the FRED API returns an error payload."""


@dataclass(frozen=True)
class FREDSeries:
    """Series metadata returned by FRED."""

    series_id: str
    title: str
    frequency: str | None = None
    observation_start: date | None = None
    observation_end: date | None = None
    units: str | None = None
    seasonal_adjustment: str | None = None


@dataclass(frozen=True)
class Observation:
    """Single FRED observation entry."""

    realtime_start: date
    realtime_end: date
    observation_date: date
    value: float | None
    raw_value: str

    @classmethod
    def from_api(cls, payload: Mapping[str, str]) -> "Observation":
        """Parse a raw JSON observation payload into a dataclass instance."""

        realtime_start = _parse_date(payload.get("realtime_start"))
        realtime_end = _parse_date(payload.get("realtime_end"))
        observation_date = _parse_date(payload.get("date"))
        raw_value = payload.get("value", "")
        value = _normalise_value(raw_value)
        return cls(
            realtime_start=realtime_start,
            realtime_end=realtime_end,
            observation_date=observation_date,
            value=value,
            raw_value=raw_value,
        )


def _parse_date(raw: str | None) -> date:
    """Convert the FRED date string to :class:`datetime.date`."""

    if not raw:
        raise FREDAPIError("FRED returned a payload missing date information")
    try:
        return datetime.fromisoformat(raw).date()
    except ValueError as exc:  # pragma: no cover - defensive coding
        raise FREDAPIError(f"Could not parse FRED date: {raw}") from exc


def _parse_optional_date(raw: object | None) -> date | None:
    if raw in (None, ""):
        return None
    try:
        return datetime.fromisoformat(str(raw)).date()
    except ValueError:  # pragma: no cover - defensive coding
        return None


def _normalise_value(raw_value: str) -> float | None:
    """Convert the observation value string into a float when possible."""

    if raw_value in {"", "."}:
        return None
    try:
        return float(raw_value)
    except ValueError:
        return None


class _RateLimiter:
    """Simple leaky bucket rate limiter based on wall-clock time."""

    def __init__(self, rate_limit_per_minute: int | None) -> None:
        self._interval = 60.0 / rate_limit_per_minute if rate_limit_per_minute else 0.0
        self._last_invocation: float | None = None

    def wait(self) -> None:
        """Sleep until we are allowed to perform the next request."""

        if not self._interval:
            return
        now = time.monotonic()
        if self._last_invocation is None:
            self._last_invocation = now
            return
        elapsed = now - self._last_invocation
        if elapsed < self._interval:
            time.sleep(self._interval - elapsed)
        self._last_invocation = time.monotonic()


class FREDClient:
    """Lightweight wrapper around the FRED API suitable for batch ingestion."""

    def __init__(
        self,
        api_key: str | None,
        base_url: str,
        *,
        rate_limit_per_minute: int | None = 60,
        user_agent: str = "lhm-fred-ingestor/1.0",
        timeout: float = 30.0,
    ) -> None:
        self.api_key = api_key or ""
        self.base_url = base_url.rstrip("/")
        self._rate_limiter = _RateLimiter(rate_limit_per_minute)
        self._user_agent = user_agent
        self._timeout = timeout

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def list_series(self, series_ids: Iterable[str]) -> list[FREDSeries]:
        """Return metadata for the requested series."""

        return [self._fetch_single_series(series_id) for series_id in series_ids]

    def search_series_by_tags(self, tags: Sequence[str], *, limit: int = 100) -> list[FREDSeries]:
        """Return popular series that match the provided FRED tags."""

        tag_names = ";".join(tag.strip() for tag in tags if tag.strip())
        if not tag_names:
            raise ValueError("At least one FRED tag must be supplied")

        payload = self._request(
            "tags/series",
            {
                "tag_names": tag_names,
                "sort_order": "desc",
                "sort_by": "popularity",
                "limit": str(limit),
            },
        )
        series_payload = payload.get("seriess") or []
        return [self._coerce_series(entry) for entry in series_payload]

    def fetch_observations(
        self,
        series_id: str,
        *,
        start_date: date | None = None,
        end_date: date | None = None,
        limit: int | None = None,
    ) -> list[Observation]:
        """Download observations for a given series within an optional window."""

        params: dict[str, str] = {
            "series_id": series_id,
            "sort_order": "asc",
            "observation_start": start_date.isoformat() if start_date else "",
            "observation_end": end_date.isoformat() if end_date else "",
        }
        if limit:
            params["limit"] = str(limit)

        payload = self._request("series/observations", params)
        observations_payload = payload.get("observations", [])
        return [Observation.from_api(entry) for entry in observations_payload]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _fetch_single_series(self, series_id: str) -> FREDSeries:
        payload = self._request("series", {"series_id": series_id})
        series_payload = payload.get("seriess") or []
        if not series_payload:
            raise FREDAPIError(f"Series '{series_id}' not found")
        entry = series_payload[0]
        return self._coerce_series(entry)

    def _request(self, endpoint: str, params: Mapping[str, str]) -> Mapping[str, object]:
        self._rate_limiter.wait()
        all_params = {
            "file_type": "json",
            "api_key": self.api_key,
        }
        all_params.update({key: value for key, value in params.items() if value is not None})
        query = parse.urlencode(all_params)
        url = f"{self.base_url}/fred/{endpoint.lstrip('/')}?{query}"

        http_request = request.Request(url, method="GET", headers={"User-Agent": self._user_agent})
        try:
            with request.urlopen(http_request, timeout=self._timeout) as response:  # noqa: S310 - trusted domain
                raw_payload = response.read()
        except OSError as exc:  # pragma: no cover - network failure is environment specific
            raise FREDAPIError(f"Failed to call FRED endpoint '{endpoint}': {exc}") from exc

        try:
            payload = json.loads(raw_payload.decode("utf-8"))
        except json.JSONDecodeError as exc:  # pragma: no cover - defensive coding
            raise FREDAPIError("FRED returned malformed JSON") from exc

        if isinstance(payload, Mapping) and payload.get("error_code"):
            message = payload.get("error_message", "Unknown error")
            raise FREDAPIError(f"FRED API error {payload.get('error_code')}: {message}")
        return payload

    # Utility to ease unit testing by exposing lazy iterables -----------------
    def iter_series(self, series_ids: Iterable[str]) -> Iterator[FREDSeries]:
        """Yield series metadata lazily."""

        for series_id in series_ids:
            yield self._fetch_single_series(series_id)

    def _coerce_series(self, payload: Mapping[str, object]) -> FREDSeries:
        series_id = str(payload.get("id") or payload.get("series_id") or "").strip()
        if not series_id:
            raise FREDAPIError("FRED response missing series identifier")
        return FREDSeries(
            series_id=series_id,
            title=str(payload.get("title", "")),
            frequency=str(payload.get("frequency")) if payload.get("frequency") else None,
            observation_start=_parse_optional_date(payload.get("observation_start")),
            observation_end=_parse_optional_date(payload.get("observation_end")),
            units=str(payload.get("units")) if payload.get("units") else None,
            seasonal_adjustment=str(payload.get("seasonal_adjustment"))
            if payload.get("seasonal_adjustment")
            else None,
        )

