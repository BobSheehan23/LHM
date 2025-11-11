"""Command line helpers to run the ingestion pipelines."""

from __future__ import annotations

import argparse
import json
import logging
import os
from pathlib import Path
from typing import Any

from .clients import FREDClient
from .config import PipelineConfig, SeriesCatalog
from .pipelines import DailyRefreshPipeline


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the FRED ingestion pipeline")
    parser.add_argument(
        "--catalog",
        type=Path,
        default=None,
        help="Path to the curated series catalog (defaults to configs/fred_series_catalog.yaml)",
    )
    parser.add_argument(
        "--storage-root",
        type=Path,
        default=None,
        help="Destination root directory for downloaded series",
    )
    parser.add_argument(
        "--storage-format",
        choices=["parquet", "csv", "json"],
        default=None,
        help="File format used to persist observations",
    )
    parser.add_argument(
        "--refresh-window-days",
        type=int,
        default=None,
        help="Number of trailing days to refresh when not running a full backfill",
    )
    parser.add_argument(
        "--full-refresh",
        action="store_true",
        help="Download the full history for each series instead of a rolling window",
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default=None,
        help="Explicit start date (YYYY-MM-DD) for the observation window",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default=None,
        help="Explicit end date (YYYY-MM-DD) for the observation window",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="FRED API key. Defaults to the FRED_API_KEY environment variable.",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        help="Logging level (e.g. INFO, DEBUG)",
    )
    return parser


def _parse_date(raw: str | None) -> Any:
    if not raw:
        return None
    from datetime import date

    try:
        return date.fromisoformat(raw)
    except ValueError as exc:  # pragma: no cover - user input validation
        raise SystemExit(f"Invalid date: {raw}") from exc


def main(argv: list[str] | None = None) -> None:
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO))

    config = PipelineConfig()
    if args.storage_root is not None:
        config.storage.root_path = Path(args.storage_root)
    if args.storage_format is not None:
        config.storage.format = args.storage_format
    if args.refresh_window_days is not None:
        config.refresh_window_days = args.refresh_window_days
    if args.catalog is not None:
        config.catalog_path = Path(args.catalog)

    config.fred.api_key = args.api_key or os.environ.get("FRED_API_KEY") or config.fred.api_key

    catalog_path = config.catalog_path
    if not catalog_path.exists():
        raise SystemExit(f"Catalog file not found: {catalog_path}")

    catalog = SeriesCatalog.load(catalog_path)
    client = FREDClient(
        config.fred.api_key,
        config.fred.base_url,
        rate_limit_per_minute=config.fred.rate_limit_per_minute,
    )
    pipeline = DailyRefreshPipeline(config, client, catalog)

    results = pipeline.run(
        full_refresh=args.full_refresh,
        explicit_start=_parse_date(args.start_date),
        explicit_end=_parse_date(args.end_date),
    )

    summary = [
        {
            "category": result.category.value,
            "series_id": result.series.series_id,
            "observations": result.observations,
            "storage_path": str(result.storage_path),
        }
        for result in results
    ]
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":  # pragma: no cover
    main()
