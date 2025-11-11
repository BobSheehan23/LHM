"""Build series catalogs automatically from FRED tag sources."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path

import yaml

from ..clients import FREDClient
from ..config import Category, SeriesCatalog, SeriesDefinition


@dataclass(slots=True)
class CatalogSourceConfig:
    """Describe how to fetch series for a specific category."""

    tags: tuple[str, ...]
    limit: int = 75


class CatalogSources(dict[Category, CatalogSourceConfig]):
    """Container that parses the YAML configuration into dataclasses."""

    @classmethod
    def load(cls, path: Path) -> "CatalogSources":
        with path.open("r", encoding="utf-8") as handle:
            payload = yaml.safe_load(handle) or {}

        categories: dict[Category, CatalogSourceConfig] = {}
        for raw_category, spec in (payload.get("categories") or {}).items():
            category = Category(raw_category)
            tags = tuple(spec.get("tags") or [])
            limit = int(spec.get("limit", 75))
            categories[category] = CatalogSourceConfig(tags=tags, limit=limit)
        return cls(categories)


def build_catalog_from_sources(client: FREDClient, sources: CatalogSources) -> SeriesCatalog:
    """Construct a :class:`SeriesCatalog` based on tag-driven sources."""

    categories: dict[Category, list[SeriesDefinition]] = {}
    for category, source in sources.items():
        seen: set[str] = set()
        definitions: list[SeriesDefinition] = []
        for series in client.search_series_by_tags(source.tags, limit=source.limit):
            if series.series_id in seen:
                continue
            seen.add(series.series_id)
            definitions.append(
                SeriesDefinition(
                    series_id=series.series_id,
                    title=series.title,
                    frequency=series.frequency,
                    units=series.units,
                    seasonal_adjustment=series.seasonal_adjustment,
                )
            )
        categories[category] = definitions
    return SeriesCatalog(categories=categories)


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a FRED series catalog from tag sources")
    parser.add_argument("--sources", type=Path, required=True, help="YAML file describing tag sources per category")
    parser.add_argument("--output", type=Path, required=True, help="Destination path for the generated catalog")
    parser.add_argument("--api-key", type=str, default=None, help="FRED API key")
    parser.add_argument(
        "--base-url",
        type=str,
        default="https://api.stlouisfed.org",
        help="Base URL for the FRED API",
    )
    parser.add_argument("--limit", type=int, default=None, help="Override the per-category series limit")
    parser.add_argument("--dry-run", action="store_true", help="Print the catalog instead of writing to disk")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    sources = CatalogSources.load(args.sources)
    if args.limit is not None:
        for config in sources.values():
            config.limit = args.limit

    client = FREDClient(args.api_key, args.base_url)
    catalog = build_catalog_from_sources(client, sources)

    if args.dry_run:
        print(json.dumps(catalog.to_yaml_dict(), indent=2))
        return

    args.output.parent.mkdir(parents=True, exist_ok=True)
    catalog.dump(args.output)


if __name__ == "__main__":  # pragma: no cover
    main()
