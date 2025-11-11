# FRED Data Platform

The Lighthouse Macro ingestion stack now provides a complete workflow for
curating, downloading, and persisting large collections of FRED series on
an automated cadence.

## Objectives

1. Provide a clearly structured configuration layer where each category
   maps to a curated list of FRED series (50-100 per category).
2. Separate the concerns of configuration, data acquisition, storage,
   and orchestration so that each layer can evolve independently.
3. Maintain an automated daily refresh cadence that rehydrates recent
   observations while respecting FRED's rate limits and terms of use.

## High-Level Architecture

| Layer        | Responsibility                                                      |
| ------------ | ------------------------------------------------------------------- |
| Config       | Defines series metadata, API credentials, and storage preferences. |
| Client       | Handles authenticated calls to FRED and response validation.        |
| Pipelines    | Orchestrates recurring refresh jobs and error handling.             |
| Storage      | Persists data in the agreed upon analytics format.                  |

## Key Modules

- `lhm.catalog.generate`: Generates the 50-100 indicators per category by
  querying FRED tag endpoints based on the recipes stored in
  `configs/fred_catalog_sources.yaml`.
- `lhm.config.series_catalog.SeriesCatalog`: Loads and validates the
  materialised catalog consumed by downstream components.
- `lhm.clients.fred_client.FREDClient`: Provides metadata lookups, tag
  searches, and observation downloads with built-in rate limiting.
- `lhm.pipelines.daily_refresh.DailyRefreshPipeline`: Coordinates the
  refresh cycle, including window resolution, data collection, and
  persistence.
- `lhm.storage.filesystem.FilesystemStorageBackend`: Writes Parquet, CSV,
  or JSON datasets alongside metadata manifests for each series.
- `lhm.cli`: Convenience CLI for executing the pipeline from the command
  line or a scheduler.

## Operational Workflow

1. **Generate the catalog**: `python -m lhm.catalog.generate --sources configs/fred_catalog_sources.yaml --output configs/fred_series_catalog.yaml --api-key $FRED_API_KEY`
   produces the per-category inventory. Adjust the tag recipes or limits
   as desired.
2. **Run the ingestion pipeline**: `python -m lhm.cli --catalog configs/fred_series_catalog.yaml --storage-root data/raw/fred --storage-format parquet --full-refresh --api-key $FRED_API_KEY`
   performs either a full backfill or rolling refresh depending on the
   flags supplied.
3. **Schedule recurring updates**: integrate the CLI command into your
   preferred scheduler (cron, Airflow, Dagster, etc.) to rehydrate the
   desired window daily.

## Next Steps

- Expand automated testing (unit and integration) once API credentials
  are available in CI.
- Add additional storage backends (e.g., DuckDB, cloud object stores) as
  production requirements evolve.
- Layer in monitoring/alerting once deployment targets are defined.
