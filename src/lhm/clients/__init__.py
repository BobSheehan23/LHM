"""External service clients used by the ingestion pipelines."""

from .fred_client import FREDClient, FREDSeries

__all__ = ["FREDClient", "FREDSeries"]
