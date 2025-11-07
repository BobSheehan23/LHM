"""Series catalog definitions for structured FRED ingestion."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Iterable, List, Mapping

import yaml


class Category(str, Enum):
    """High-level macroeconomic groupings requested by the stakeholder."""

    GDP = "gdp"
    LABOR = "labor"
    PRICES = "prices"
    HEALTH = "health"
    MONEY = "money"
    TRADE = "trade"
    GOVERNMENT = "government"
    BUSINESS = "business"
    CONSUMER = "consumer"
    HOUSING = "housing"
    TAXES = "taxes"


@dataclass(frozen=True)
class SeriesDefinition:
    """Describe a single FRED series and its metadata."""

    series_id: str
    title: str
    frequency: str | None = None
    units: str | None = None
    seasonal_adjustment: str | None = None
    notes: str | None = None


@dataclass
class SeriesCatalog:
    """Container grouping the series definitions by category."""

    categories: Mapping[Category, List[SeriesDefinition]] = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, handle: Iterable[str]) -> "SeriesCatalog":
        """Create a catalog from a YAML document."""

        payload = yaml.safe_load(handle)
        categories: dict[Category, List[SeriesDefinition]] = {}
        for raw_category, raw_series in payload.get("categories", {}).items():
            category = Category(raw_category)
            definitions = [SeriesDefinition(**entry) for entry in raw_series or []]
            categories[category] = definitions
        return cls(categories=categories)

    @classmethod
    def load(cls, path: str | Path) -> "SeriesCatalog":
        """Load a YAML catalog from disk."""

        with Path(path).expanduser().open("r", encoding="utf-8") as handle:
            return cls.from_yaml(handle)

    def to_yaml_dict(self) -> dict:
        """Represent the catalog as a serialisable dictionary."""

        return {
            "categories": {
                category.value: [
                    {
                        "series_id": definition.series_id,
                        "title": definition.title,
                        "frequency": definition.frequency,
                        "units": definition.units,
                        "seasonal_adjustment": definition.seasonal_adjustment,
                        "notes": definition.notes,
                    }
                    for definition in definitions
                ]
                for category, definitions in sorted(self.categories.items(), key=lambda item: item[0].value)
            }
        }

    def dump(self, path: str | Path) -> None:
        """Persist the catalog to disk."""

        with Path(path).expanduser().open("w", encoding="utf-8") as handle:
            yaml.safe_dump(self.to_yaml_dict(), handle, sort_keys=False, allow_unicode=True)

    def iter_series(self) -> Iterable[tuple[Category, SeriesDefinition]]:
        """Iterate over ``(category, series_definition)`` tuples."""

        for category, definitions in self.categories.items():
            for definition in definitions:
                yield category, definition
