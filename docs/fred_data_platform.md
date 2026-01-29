# FRED Data Platform Skeleton

This document summarises the scaffolding that will power the automated
retrieval of FRED indicators once the catalog of series has been
approved.

## Objectives

1. Provide a clearly structured configuration layer where each category
   maps to a curated list of FRED series (50-100 per category).
2. Separate the concerns of configuration, data acquisition, storage,
   and orchestration so that each layer can evolve independently.
3. Prepare for a daily refresh cadence that rehydrates recent
   observations while respecting FRED's rate limits and terms of use.

## High-Level Architecture

| Layer        | Responsibility                                                      |
| ------------ | ------------------------------------------------------------------- |
| Config       | Defines series metadata, API credentials, and storage preferences. |
| Client       | Handles authenticated calls to FRED and response validation.        |
| Pipelines    | Orchestrates recurring refresh jobs and error handling.             |
| Storage      | Persists data in the agreed upon analytics format.                  |

## Key Modules

- `lhm.config.series_catalog.SeriesCatalog`: Loads and validates the
  category -> series mapping from YAML.
- `lhm.clients.fred_client.FREDClient`: Placeholder interface for the
  HTTP client that will communicate with FRED.
- `lhm.pipelines.daily_refresh.DailyRefreshPipeline`: Coordinates the
  daily ingestion cycle.
- `lhm.storage.registry.StorageRegistry`: Future entry point for
  storage backends (e.g., local parquet, cloud data warehouse).

## Next Steps

- Finalise the list of 50-100 FRED series per category.
- Implement the concrete FRED client, including authentication and
  throttling.
- Introduce persistence utilities aligned with the stakeholder's data
  lake/warehouse standards.
- Add CI workflows and automated tests once the functional components
  are in place.
