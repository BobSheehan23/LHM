"""
LIGHTHOUSE MACRO - DATA PIPELINE
================================
Institutional-grade macro data infrastructure.

One database. All sources. Zero headaches.
"""

from .config import DB_PATH, OUTPUT_DIR
from .pipeline import run_daily_update, get_stats
from .transforms import TRANSFORM_REGISTRY
from .query import get_series, search_series, export_wide

__version__ = "2.0.0"
__all__ = [
    "run_daily_update",
    "get_stats",
    "get_series",
    "search_series",
    "export_wide",
    "TRANSFORM_REGISTRY",
]
