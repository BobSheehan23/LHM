"""
LIGHTHOUSE MACRO - DATA FETCHERS
================================
Unified fetchers for all data sources with retry logic and rate limiting.
"""

import requests
import pandas as pd
import sqlite3
import time
import logging
from datetime import datetime
from io import StringIO
from typing import Tuple, Optional, List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from .config import (
    API_KEYS, FETCH_CONFIG,
    FRED_CATEGORIES, FRED_CURATED,
    BLS_SERIES, BEA_TABLES,
    NYFED_RATES, OFR_SERIES, OFR_FSI_COLUMNS
)

logger = logging.getLogger(__name__)


# ==========================================
# RETRY DECORATOR
# ==========================================

def retry_with_backoff(
    func,
    max_retries: int = None,
    base_delay: float = None
):
    """
    Retry wrapper with exponential backoff.
    """
    max_retries = max_retries or FETCH_CONFIG["max_retries"]
    base_delay = base_delay or FETCH_CONFIG["retry_delay_base"]

    def wrapper(*args, **kwargs):
        last_exception = None
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                last_exception = e
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
        raise last_exception

    return wrapper


def fetch_with_retry(url: str, params: dict = None, timeout: int = None, method: str = "GET", json_data: dict = None) -> dict:
    """Fetch URL with retry logic."""
    timeout = timeout or FETCH_CONFIG["timeout"]
    max_retries = FETCH_CONFIG["max_retries"]
    base_delay = FETCH_CONFIG["retry_delay_base"]

    last_exception = None
    for attempt in range(max_retries):
        try:
            if method == "POST":
                r = requests.post(url, json=json_data, timeout=timeout)
            else:
                r = requests.get(url, params=params, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            last_exception = e
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                time.sleep(delay)

    logger.error(f"All {max_retries} attempts failed for {url}")
    raise last_exception


# ==========================================
# FRED FETCHER
# ==========================================

class FREDFetcher:
    """Fetch data from FRED API."""

    BASE_URL = "https://api.stlouisfed.org/fred"

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.api_key = API_KEYS["FRED"]
        if not self.api_key:
            raise ValueError("FRED_API_KEY not set")

    def fetch_category(self, category_id: int, category_name: str, limit: int = 50) -> Tuple[int, int]:
        """Fetch top series from a FRED category."""
        c = self.conn.cursor()
        updated = 0
        obs_added = 0

        url = f"{self.BASE_URL}/category/series"
        params = {
            "category_id": category_id,
            "api_key": self.api_key,
            "file_type": "json",
            "limit": limit,
            "order_by": "popularity",
            "sort_order": "desc"
        }

        try:
            data = fetch_with_retry(url, params)

            if "seriess" not in data:
                return 0, 0

            for s in data["seriess"]:
                series_id = s["id"]
                api_updated = s.get("last_updated", "")

                # Check if we need to update
                c.execute("SELECT last_updated FROM series_meta WHERE series_id = ?", (series_id,))
                row = c.fetchone()
                local_updated = row[0] if row else "1900-01-01"

                if row and local_updated >= api_updated:
                    continue  # Skip - already current

                # Fetch observations
                series_updated, series_obs = self._fetch_series(series_id, s, category_name)
                updated += series_updated
                obs_added += series_obs

                time.sleep(FETCH_CONFIG["rate_limit_delay"])

        except Exception as e:
            logger.error(f"Error fetching category {category_name}: {e}")

        return updated, obs_added

    def fetch_curated(self) -> Tuple[int, int]:
        """Fetch curated high-priority FRED series."""
        updated = 0
        obs_added = 0

        for series_id, title in FRED_CURATED.items():
            try:
                series_info = {"id": series_id, "title": title}
                series_updated, series_obs = self._fetch_series(series_id, series_info, "Curated")
                updated += series_updated
                obs_added += series_obs
            except Exception as e:
                logger.error(f"Error fetching {series_id}: {e}")

            time.sleep(FETCH_CONFIG["rate_limit_delay"])

        return updated, obs_added

    def _fetch_series(self, series_id: str, series_info: dict, category: str) -> Tuple[int, int]:
        """Fetch a single FRED series."""
        c = self.conn.cursor()

        url = f"{self.BASE_URL}/series/observations"
        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json"
        }

        data = fetch_with_retry(url, params)

        if "observations" not in data:
            return 0, 0

        obs_list = [
            (series_id, o["date"], float(o["value"]))
            for o in data["observations"]
            if o["value"] != "."
        ]

        if not obs_list:
            return 0, 0

        c.executemany("INSERT OR REPLACE INTO observations VALUES (?,?,?)", obs_list)

        c.execute("""INSERT OR REPLACE INTO series_meta
                    (series_id, title, source, category, frequency, units, last_updated, last_fetched)
                    VALUES (?,?,?,?,?,?,?,?)""",
                 (series_id, series_info.get("title", ""), "FRED", category,
                  series_info.get("frequency", ""), series_info.get("units", ""),
                  datetime.now().isoformat(), datetime.now().isoformat()))

        self.conn.commit()
        return 1, len(obs_list)

    def fetch_all(self) -> Tuple[int, int]:
        """Fetch all FRED data: categories + curated."""
        total_updated = 0
        total_obs = 0

        logger.info("--- FRED: Category Discovery ---")
        for cat_name, cat_id in FRED_CATEGORIES.items():
            logger.info(f"   {cat_name}...")
            updated, obs = self.fetch_category(cat_id, cat_name, FETCH_CONFIG["fred_category_limit"])
            logger.info(f"   {cat_name}: {updated} series, {obs:,} obs")
            total_updated += updated
            total_obs += obs
            self.conn.commit()
            time.sleep(0.3)

        logger.info("--- FRED: Curated Series ---")
        updated, obs = self.fetch_curated()
        logger.info(f"   Curated: {updated} series, {obs:,} obs")
        total_updated += updated
        total_obs += obs
        self.conn.commit()

        return total_updated, total_obs


# ==========================================
# BLS FETCHER
# ==========================================

class BLSFetcher:
    """Fetch data from BLS API."""

    BASE_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.api_key = API_KEYS["BLS"]
        if not self.api_key:
            raise ValueError("BLS_API_KEY not set")

    def fetch_all(self, start_year: int = None) -> Tuple[int, int]:
        """Fetch all BLS series with 20-year chunking."""
        start_year = start_year or FETCH_CONFIG["bls_start_year"]
        c = self.conn.cursor()
        total_obs = 0

        current_year = datetime.now().year
        intervals = [
            (start, min(start + 19, current_year))
            for start in range(start_year, current_year + 1, 20)
        ]

        series_ids = list(BLS_SERIES.keys())

        for start_yr, end_yr in intervals:
            logger.info(f"   BLS {start_yr}-{end_yr}...")

            payload = {
                "seriesid": series_ids,
                "startyear": str(start_yr),
                "endyear": str(end_yr),
                "registrationkey": self.api_key
            }

            try:
                data = fetch_with_retry(self.BASE_URL, method="POST", json_data=payload, timeout=60)

                if data.get("status") == "REQUEST_SUCCEEDED":
                    chunk_obs = 0
                    for s in data["Results"]["series"]:
                        series_id = s["seriesID"]
                        title = BLS_SERIES.get(series_id, series_id)

                        for item in s["data"]:
                            if item["value"] not in ["", "."]:
                                period = item["period"]
                                if period.startswith("M"):
                                    month = period[1:]
                                    date_str = f"{item['year']}-{month}-01"
                                elif period.startswith("Q"):
                                    q_map = {"Q01": "01", "Q02": "04", "Q03": "07", "Q04": "10"}
                                    month = q_map.get(period, "01")
                                    date_str = f"{item['year']}-{month}-01"
                                else:
                                    date_str = f"{item['year']}-01-01"

                                try:
                                    value = float(item["value"])
                                    c.execute("INSERT OR REPLACE INTO observations VALUES (?,?,?)",
                                             (f"BLS_{series_id}", date_str, value))
                                    chunk_obs += 1
                                except ValueError:
                                    pass

                        # Update metadata
                        c.execute("""INSERT OR REPLACE INTO series_meta
                                    (series_id, title, source, category, frequency, units, last_updated, last_fetched)
                                    VALUES (?,?,?,?,?,?,?,?)""",
                                 (f"BLS_{series_id}", title, "BLS", "Labor_Prices", "Monthly", "",
                                  datetime.now().isoformat(), datetime.now().isoformat()))

                    logger.info(f"   BLS {start_yr}-{end_yr}: {chunk_obs:,} obs")
                    total_obs += chunk_obs
                    self.conn.commit()

            except Exception as e:
                logger.error(f"BLS Error: {e}")

            time.sleep(0.5)

        return len(BLS_SERIES), total_obs


# ==========================================
# BEA FETCHER
# ==========================================

class BEAFetcher:
    """Fetch data from BEA API."""

    BASE_URL = "https://apps.bea.gov/api/data/"

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.api_key = API_KEYS["BEA"]
        if not self.api_key:
            raise ValueError("BEA_API_KEY not set")

    def fetch_all(self, start_year: int = None) -> Tuple[int, int]:
        """Fetch all BEA NIPA tables."""
        start_year = start_year or FETCH_CONFIG["bea_start_year"]
        c = self.conn.cursor()
        total_obs = 0

        years = ",".join([str(y) for y in range(start_year, datetime.now().year + 1)])

        for table_info in BEA_TABLES:
            logger.info(f"   BEA {table_info['desc']}...")

            params = {
                "UserID": self.api_key,
                "Method": "GetData",
                "DatasetName": table_info["dataset"],
                "TableName": table_info["table"],
                "Frequency": "Q",
                "Year": years,
                "ResultFormat": "JSON"
            }

            try:
                data = fetch_with_retry(self.BASE_URL, params, timeout=60)

                if "BEAAPI" in data and "Results" in data["BEAAPI"]:
                    rows = data["BEAAPI"]["Results"].get("Data", [])
                    table_obs = 0

                    for row in rows:
                        tp = row.get("TimePeriod", "")
                        if "Q" in tp:
                            q_map = {"Q1": "01", "Q2": "04", "Q3": "07", "Q4": "10"}
                            quarter = tp[-2:]
                            month = q_map.get(quarter, "01")
                            date_str = f"{tp[:4]}-{month}-01"
                        else:
                            date_str = f"{tp}-01-01"

                        line_desc = row.get("LineDescription", "Unknown")
                        series_id = f"BEA_{table_info['desc']}_{line_desc}".replace(" ", "_")[:100]

                        try:
                            value_str = row.get("DataValue", "").replace(",", "")
                            value = float(value_str)
                            c.execute("INSERT OR REPLACE INTO observations VALUES (?,?,?)",
                                     (series_id, date_str, value))
                            table_obs += 1

                            c.execute("""INSERT OR REPLACE INTO series_meta
                                        (series_id, title, source, category, frequency, units, last_updated, last_fetched)
                                        VALUES (?,?,?,?,?,?,?,?)""",
                                     (series_id, line_desc, "BEA", table_info["desc"], "Quarterly", "",
                                      datetime.now().isoformat(), datetime.now().isoformat()))
                        except (ValueError, TypeError):
                            pass

                    logger.info(f"   BEA {table_info['desc']}: {table_obs:,} obs")
                    total_obs += table_obs
                    self.conn.commit()

            except Exception as e:
                logger.error(f"BEA Error: {e}")

            time.sleep(0.5)

        return len(BEA_TABLES), total_obs


# ==========================================
# NY FED FETCHER (No API key needed)
# ==========================================

class NYFedFetcher:
    """Fetch NY Fed reference rates."""

    BASE_URL = "https://markets.newyorkfed.org/api/rates/all/search.json"

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def fetch_all(self, start_date: str = None) -> Tuple[int, int]:
        """Fetch NY Fed reference rates."""
        start_date = start_date or FETCH_CONFIG["nyfed_start_date"]
        c = self.conn.cursor()
        total_obs = 0

        url = f"{self.BASE_URL}?startDate={start_date}"

        try:
            logger.info(f"   NY Fed from {start_date}...")
            r = requests.get(url, timeout=60)

            if r.status_code == 200:
                data = r.json()

                if "refRates" in data:
                    for item in data["refRates"]:
                        rate_type = item.get("type", "")
                        if rate_type in NYFED_RATES:
                            date_str = item.get("effectiveDate", "")
                            rate = item.get("percentRate")

                            if rate is not None and date_str:
                                series_id = f"NYFED_{rate_type}"
                                c.execute("INSERT OR REPLACE INTO observations VALUES (?,?,?)",
                                         (series_id, date_str, float(rate)))
                                total_obs += 1

                                # Volume
                                volume = item.get("volumeInBillions")
                                if volume is not None:
                                    vol_series_id = f"NYFED_{rate_type}_Volume"
                                    c.execute("INSERT OR REPLACE INTO observations VALUES (?,?,?)",
                                             (vol_series_id, date_str, float(volume)))
                                    total_obs += 1

                    # Update metadata
                    for rate_type, title in NYFED_RATES.items():
                        c.execute("""INSERT OR REPLACE INTO series_meta
                                    (series_id, title, source, category, frequency, units, last_updated, last_fetched)
                                    VALUES (?,?,?,?,?,?,?,?)""",
                                 (f"NYFED_{rate_type}", title, "NYFED", "Reference_Rates", "Daily", "Percent",
                                  datetime.now().isoformat(), datetime.now().isoformat()))

                        c.execute("""INSERT OR REPLACE INTO series_meta
                                    (series_id, title, source, category, frequency, units, last_updated, last_fetched)
                                    VALUES (?,?,?,?,?,?,?,?)""",
                                 (f"NYFED_{rate_type}_Volume", f"{title} Volume", "NYFED", "Reference_Rates", "Daily", "Billions USD",
                                  datetime.now().isoformat(), datetime.now().isoformat()))

                    self.conn.commit()
                    logger.info(f"   NY Fed: {total_obs:,} obs")

        except Exception as e:
            logger.error(f"NY Fed Error: {e}")

        return len(NYFED_RATES) * 2, total_obs


# ==========================================
# OFR FETCHER (No API key needed)
# ==========================================

class OFRFetcher:
    """Fetch OFR Short-term Funding Monitor and FSI."""

    SERIES_URL = "https://data.financialresearch.gov/v1/series/timeseries/"
    FSI_URL = "https://www.financialresearch.gov/financial-stress-index/data/fsi.csv"

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def fetch_all(self) -> Tuple[int, int]:
        """Fetch all OFR data."""
        c = self.conn.cursor()
        total_obs = 0
        series_count = 0

        # Fetch each series
        for mnemonic, title in OFR_SERIES.items():
            logger.info(f"   OFR {title}...")
            url = f"{self.SERIES_URL}?mnemonic={mnemonic}"

            try:
                r = requests.get(url, timeout=30)
                if r.status_code == 200:
                    data = r.json()
                    obs_count = 0

                    for item in data:
                        if isinstance(item, list) and len(item) >= 2:
                            date_str = item[0]
                            value = item[1]
                            if value is not None:
                                c.execute("INSERT OR REPLACE INTO observations VALUES (?,?,?)",
                                         (f"OFR_{mnemonic}", date_str, float(value)))
                                obs_count += 1

                    if obs_count > 0:
                        c.execute("""INSERT OR REPLACE INTO series_meta
                                    (series_id, title, source, category, frequency, units, last_updated, last_fetched)
                                    VALUES (?,?,?,?,?,?,?,?)""",
                                 (f"OFR_{mnemonic}", title, "OFR", "Short_Term_Funding", "Daily", "",
                                  datetime.now().isoformat(), datetime.now().isoformat()))
                        series_count += 1
                        total_obs += obs_count
                        logger.info(f"   OFR {title}: {obs_count:,} obs")

            except Exception as e:
                logger.error(f"OFR Error {mnemonic}: {e}")

            time.sleep(0.2)

        self.conn.commit()

        # Fetch FSI
        logger.info("   OFR FSI...")
        try:
            r = requests.get(self.FSI_URL, timeout=30)
            if r.status_code == 200:
                df = pd.read_csv(StringIO(r.text))
                fsi_obs = 0

                for col, series_id in OFR_FSI_COLUMNS.items():
                    if col in df.columns:
                        for _, row in df.iterrows():
                            if pd.notna(row[col]):
                                c.execute("INSERT OR REPLACE INTO observations VALUES (?,?,?)",
                                         (series_id, row["Date"], float(row[col])))
                                fsi_obs += 1

                        c.execute("""INSERT OR REPLACE INTO series_meta
                                    (series_id, title, source, category, frequency, units, last_updated, last_fetched)
                                    VALUES (?,?,?,?,?,?,?,?)""",
                                 (series_id, f"Financial Stress Index - {col}", "OFR", "Financial_Stress", "Daily", "Index",
                                  datetime.now().isoformat(), datetime.now().isoformat()))
                        series_count += 1

                total_obs += fsi_obs
                self.conn.commit()
                logger.info(f"   OFR FSI: {fsi_obs:,} obs")

        except Exception as e:
            logger.error(f"OFR FSI Error: {e}")

        return series_count, total_obs
