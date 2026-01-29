"""
Labor Market Data Collector - Multi-Source Ingestion
Lighthouse Macro - January 2026

Collects labor market data from:
1. FRED API - Primary source for most BLS series
2. BLS API - Direct access for series not on FRED
3. Atlanta Fed Wage Growth Tracker - Web download
4. Indeed Hiring Lab - GitHub data

This module orchestrates the full labor data collection pipeline.
"""

import os
import time
import json
import requests
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
from io import StringIO

from ..config import CONFIG
from ..utils.logging import get_logger
from ..utils.io import write_parquet
from .labor_series_registry import (
    get_all_series,
    get_fred_series,
    get_series_by_category,
    SeriesDefinition,
    ATLANTA_FED_WAGE_TRACKER,
)

log = get_logger(__name__)


# =============================================================================
# CONFIGURATION
# =============================================================================

LABOR_RAW_DIR = CONFIG.raw_dir / "labor"
LABOR_CURATED_DIR = CONFIG.curated_dir / "labor"

# API rate limits
FRED_REQUESTS_PER_MINUTE = 120
BLS_REQUESTS_PER_DAY = 500
BLS_SERIES_PER_REQUEST = 50

# Default history
DEFAULT_START_DATE = "2000-01-01"


# =============================================================================
# FRED API COLLECTOR
# =============================================================================

class FREDCollector:
    """Collect data from FRED API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or CONFIG.fred_api_key
        self.base_url = "https://api.stlouisfed.org/fred/series/observations"
        self._request_count = 0
        self._last_request_time = 0.0

    def _rate_limit(self) -> None:
        """Enforce rate limiting."""
        now = time.time()
        if self._request_count >= FRED_REQUESTS_PER_MINUTE:
            elapsed = now - self._last_request_time
            if elapsed < 60:
                sleep_time = 60 - elapsed + 1
                log.info(f"Rate limit reached, sleeping {sleep_time:.1f}s")
                time.sleep(sleep_time)
            self._request_count = 0
        self._last_request_time = now
        self._request_count += 1

    def fetch_series(
        self,
        series_id: str,
        start_date: str = DEFAULT_START_DATE,
        end_date: Optional[str] = None
    ) -> Optional[pd.Series]:
        """Fetch a single FRED series."""
        if not self.api_key:
            log.error("FRED_API_KEY not set")
            return None

        self._rate_limit()

        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
            "observation_start": start_date,
        }
        if end_date:
            params["observation_end"] = end_date

        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json().get("observations", [])

            if not data:
                log.warning(f"No data returned for {series_id}")
                return None

            df = pd.DataFrame(data)
            df["date"] = pd.to_datetime(df["date"])
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            df = df.dropna(subset=["value"])

            if df.empty:
                return None

            return df.set_index("date")["value"]

        except requests.exceptions.RequestException as e:
            log.error(f"Failed to fetch {series_id}: {e}")
            return None
        except (KeyError, ValueError) as e:
            log.error(f"Failed to parse {series_id}: {e}")
            return None

    def fetch_multiple(
        self,
        series_map: dict[str, str],
        start_date: str = DEFAULT_START_DATE,
        progress_callback: Optional[callable] = None
    ) -> pd.DataFrame:
        """
        Fetch multiple FRED series.

        Args:
            series_map: Dict of {fred_id: internal_name}
            start_date: Start date for data
            progress_callback: Optional callback(current, total, series_id)

        Returns:
            DataFrame with all series, columns named by internal_name
        """
        frames = {}
        total = len(series_map)

        for i, (fred_id, internal_name) in enumerate(series_map.items(), 1):
            if progress_callback:
                progress_callback(i, total, fred_id)
            else:
                log.info(f"[{i}/{total}] Fetching {fred_id} ({internal_name})")

            series = self.fetch_series(fred_id, start_date)
            if series is not None:
                frames[internal_name] = series

        if not frames:
            log.error("Failed to fetch any series")
            return pd.DataFrame()

        df = pd.DataFrame(frames)
        df.index = pd.to_datetime(df.index)
        return df.sort_index()


# =============================================================================
# BLS API COLLECTOR
# =============================================================================

class BLSCollector:
    """Collect data directly from BLS API (for series not on FRED)."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("BLS_API_KEY")
        self.base_url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
        self._request_count = 0

    def fetch_series(
        self,
        series_ids: list[str],
        start_year: int = 2000,
        end_year: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Fetch multiple BLS series in a single request.

        Args:
            series_ids: List of BLS series IDs (max 50 per request)
            start_year: Start year
            end_year: End year (defaults to current year)

        Returns:
            DataFrame with series as columns
        """
        if not self.api_key:
            log.warning("BLS_API_KEY not set, using unregistered API (limited)")

        if end_year is None:
            end_year = datetime.now().year

        # BLS API limits to 50 series per request, 20 years per request
        if len(series_ids) > BLS_SERIES_PER_REQUEST:
            log.warning(f"Too many series ({len(series_ids)}), truncating to {BLS_SERIES_PER_REQUEST}")
            series_ids = series_ids[:BLS_SERIES_PER_REQUEST]

        # Split into 20-year chunks if needed
        year_span = end_year - start_year
        if year_span > 20:
            # Fetch in chunks
            all_frames = []
            for chunk_start in range(start_year, end_year, 20):
                chunk_end = min(chunk_start + 19, end_year)
                chunk_df = self._fetch_chunk(series_ids, chunk_start, chunk_end)
                if not chunk_df.empty:
                    all_frames.append(chunk_df)

            if not all_frames:
                return pd.DataFrame()
            return pd.concat(all_frames).sort_index()
        else:
            return self._fetch_chunk(series_ids, start_year, end_year)

    def _fetch_chunk(
        self,
        series_ids: list[str],
        start_year: int,
        end_year: int
    ) -> pd.DataFrame:
        """Fetch a single chunk of BLS data."""
        payload = {
            "seriesid": series_ids,
            "startyear": str(start_year),
            "endyear": str(end_year),
        }
        if self.api_key:
            payload["registrationkey"] = self.api_key

        headers = {"Content-type": "application/json"}

        try:
            response = requests.post(
                self.base_url,
                data=json.dumps(payload),
                headers=headers,
                timeout=60
            )
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "REQUEST_SUCCEEDED":
                log.error(f"BLS API error: {data.get('message', 'Unknown error')}")
                return pd.DataFrame()

            # Parse results
            frames = {}
            for series_result in data.get("Results", {}).get("series", []):
                series_id = series_result.get("seriesID")
                observations = series_result.get("data", [])

                if not observations:
                    continue

                records = []
                for obs in observations:
                    year = int(obs["year"])
                    period = obs["period"]

                    # Handle different period formats
                    if period.startswith("M"):
                        month = int(period[1:])
                        date = datetime(year, month, 1)
                    elif period.startswith("Q"):
                        quarter = int(period[1:])
                        month = (quarter - 1) * 3 + 1
                        date = datetime(year, month, 1)
                    elif period == "A01":
                        date = datetime(year, 1, 1)
                    else:
                        continue

                    value = float(obs["value"])
                    records.append({"date": date, "value": value})

                if records:
                    df = pd.DataFrame(records)
                    df = df.set_index("date").sort_index()
                    frames[series_id] = df["value"]

            if not frames:
                return pd.DataFrame()

            result = pd.DataFrame(frames)
            result.index = pd.to_datetime(result.index)
            return result.sort_index()

        except requests.exceptions.RequestException as e:
            log.error(f"BLS API request failed: {e}")
            return pd.DataFrame()
        except (KeyError, ValueError, json.JSONDecodeError) as e:
            log.error(f"Failed to parse BLS response: {e}")
            return pd.DataFrame()


# =============================================================================
# ATLANTA FED WAGE GROWTH TRACKER COLLECTOR
# =============================================================================

class AtlantaFedCollector:
    """Collect data from Atlanta Fed Wage Growth Tracker."""

    # URL for the wage growth tracker data
    DATA_URL = "https://www.atlantafed.org/-/media/documents/datafiles/chcs/wage-growth-tracker/wage-growth-data.xlsx"

    # Column mappings from Atlanta Fed to our internal names
    COLUMN_MAP = {
        "Overall": "AtlFed_Wage_Growth_Overall",
        "Job Stayer": "AtlFed_Wage_Growth_Stayers",
        "Job Switcher": "AtlFed_Wage_Growth_Switchers",
        "16–24": "AtlFed_Wage_Growth_16_24",
        "25–54": "AtlFed_Wage_Growth_25_54",
        "55+": "AtlFed_Wage_Growth_55_Plus",
        "Male": "AtlFed_Wage_Growth_Male",
        "Female": "AtlFed_Wage_Growth_Female",
        "High school diploma or less": "AtlFed_Wage_Growth_HS_or_Less",
        "Some college": "AtlFed_Wage_Growth_Some_College",
        "Bachelor's degree or higher": "AtlFed_Wage_Growth_Bachelors_Plus",
        "1st Quartile (lowest paid)": "AtlFed_Wage_Growth_Bottom25",
        "2nd Quartile": "AtlFed_Wage_Growth_2nd_Quartile",
        "3rd Quartile": "AtlFed_Wage_Growth_3rd_Quartile",
        "4th Quartile (highest paid)": "AtlFed_Wage_Growth_Top25",
        "Part-time": "AtlFed_Wage_Growth_Part_Time",
        "Full-time": "AtlFed_Wage_Growth_Full_Time",
        "Public sector": "AtlFed_Wage_Growth_Public",
        "Private sector": "AtlFed_Wage_Growth_Private",
    }

    def fetch(self) -> pd.DataFrame:
        """
        Fetch the wage growth tracker data.

        Returns:
            DataFrame with all wage growth series
        """
        log.info("Fetching Atlanta Fed Wage Growth Tracker...")

        try:
            response = requests.get(self.DATA_URL, timeout=60)
            response.raise_for_status()

            # Read Excel file
            df = pd.read_excel(
                response.content,
                sheet_name="Median Wage Growth",
                skiprows=0,
                index_col=0
            )

            # Parse the date index (format varies)
            df.index = pd.to_datetime(df.index, errors="coerce")
            df = df[df.index.notna()]

            # Rename columns to internal names
            rename_map = {}
            for col in df.columns:
                col_clean = str(col).strip()
                if col_clean in self.COLUMN_MAP:
                    rename_map[col] = self.COLUMN_MAP[col_clean]

            df = df.rename(columns=rename_map)

            # Keep only mapped columns
            keep_cols = [c for c in df.columns if c.startswith("AtlFed_")]
            df = df[keep_cols]

            # Convert to numeric
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

            df = df.sort_index()
            log.info(f"Fetched {len(df)} observations, {len(df.columns)} series")

            return df

        except requests.exceptions.RequestException as e:
            log.error(f"Failed to fetch Atlanta Fed data: {e}")
            return pd.DataFrame()
        except Exception as e:
            log.error(f"Failed to parse Atlanta Fed data: {e}")
            return pd.DataFrame()

    def compute_job_hopper_premium(self, df: pd.DataFrame) -> pd.Series:
        """
        Compute the job hopper premium (switchers - stayers).

        This is a CRITICAL cyclical indicator.
        """
        if "AtlFed_Wage_Growth_Switchers" in df.columns and "AtlFed_Wage_Growth_Stayers" in df.columns:
            return df["AtlFed_Wage_Growth_Switchers"] - df["AtlFed_Wage_Growth_Stayers"]
        return pd.Series(dtype=float)


# =============================================================================
# INDEED HIRING LAB COLLECTOR
# =============================================================================

class IndeedCollector:
    """Collect job postings data from Indeed Hiring Lab GitHub."""

    GITHUB_BASE = "https://raw.githubusercontent.com/hiring-lab/job_postings_tracker/main"

    def fetch_us_postings(self) -> pd.DataFrame:
        """Fetch US job postings index."""
        url = f"{self.GITHUB_BASE}/US/aggregate_job_postings_US.csv"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            df = pd.read_csv(StringIO(response.text))

            # Parse date column
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
                df = df.set_index("date")

            # Rename columns
            rename_map = {
                "indeed_job_postings_index": "Indeed_Job_Postings_US",
                "indeed_job_postings_index_sa": "Indeed_Job_Postings_US_SA",
            }
            df = df.rename(columns=rename_map)

            log.info(f"Fetched {len(df)} Indeed job postings observations")
            return df

        except requests.exceptions.RequestException as e:
            log.error(f"Failed to fetch Indeed data: {e}")
            return pd.DataFrame()

    def fetch_sector_postings(self) -> pd.DataFrame:
        """Fetch sector-level job postings."""
        url = f"{self.GITHUB_BASE}/US/job_postings_by_sector_US.csv"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            df = pd.read_csv(StringIO(response.text))

            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])

            log.info(f"Fetched {len(df)} sector-level observations")
            return df

        except requests.exceptions.RequestException as e:
            log.error(f"Failed to fetch Indeed sector data: {e}")
            return pd.DataFrame()


# =============================================================================
# MAIN COLLECTION ORCHESTRATOR
# =============================================================================

class LaborDataCollector:
    """
    Master orchestrator for all labor data collection.

    Usage:
        collector = LaborDataCollector()
        df = collector.collect_all()
    """

    def __init__(self):
        self.fred = FREDCollector()
        self.bls = BLSCollector()
        self.atlanta_fed = AtlantaFedCollector()
        self.indeed = IndeedCollector()

        # Ensure directories exist
        LABOR_RAW_DIR.mkdir(parents=True, exist_ok=True)
        LABOR_CURATED_DIR.mkdir(parents=True, exist_ok=True)

    def collect_fred_labor(
        self,
        start_date: str = DEFAULT_START_DATE,
        save: bool = True
    ) -> pd.DataFrame:
        """
        Collect all FRED-available labor series.

        Returns:
            DataFrame with all FRED labor series
        """
        log.info("=" * 60)
        log.info("COLLECTING FRED LABOR DATA")
        log.info("=" * 60)

        fred_map = get_fred_series()
        log.info(f"Fetching {len(fred_map)} FRED series...")

        df = self.fred.fetch_multiple(fred_map, start_date)

        if save and not df.empty:
            out_path = LABOR_RAW_DIR / "fred_labor.parquet"
            write_parquet(df, out_path)
            log.info(f"Saved to {out_path}")

        log.info(f"FRED collection complete: {df.shape}")
        return df

    def collect_atlanta_fed(self, save: bool = True) -> pd.DataFrame:
        """
        Collect Atlanta Fed Wage Growth Tracker data.

        Returns:
            DataFrame with wage growth tracker series
        """
        log.info("=" * 60)
        log.info("COLLECTING ATLANTA FED WAGE GROWTH TRACKER")
        log.info("=" * 60)

        df = self.atlanta_fed.fetch()

        if not df.empty:
            # Add computed job hopper premium
            df["AtlFed_Job_Hopper_Premium"] = self.atlanta_fed.compute_job_hopper_premium(df)

        if save and not df.empty:
            out_path = LABOR_RAW_DIR / "atlanta_fed_wages.parquet"
            write_parquet(df, out_path)
            log.info(f"Saved to {out_path}")

        log.info(f"Atlanta Fed collection complete: {df.shape}")
        return df

    def collect_indeed(self, save: bool = True) -> pd.DataFrame:
        """
        Collect Indeed job postings data.

        Returns:
            DataFrame with job postings data
        """
        log.info("=" * 60)
        log.info("COLLECTING INDEED HIRING LAB DATA")
        log.info("=" * 60)

        df = self.indeed.fetch_us_postings()

        if save and not df.empty:
            out_path = LABOR_RAW_DIR / "indeed_postings.parquet"
            write_parquet(df, out_path)
            log.info(f"Saved to {out_path}")

        log.info(f"Indeed collection complete: {df.shape}")
        return df

    def collect_all(
        self,
        start_date: str = DEFAULT_START_DATE,
        save: bool = True
    ) -> dict[str, pd.DataFrame]:
        """
        Collect all labor data from all sources.

        Returns:
            Dict of {source_name: DataFrame}
        """
        log.info("=" * 60)
        log.info("FULL LABOR DATA COLLECTION")
        log.info(f"Start date: {start_date}")
        log.info("=" * 60)

        results = {}

        # 1. FRED data
        results["fred"] = self.collect_fred_labor(start_date, save)

        # 2. Atlanta Fed
        results["atlanta_fed"] = self.collect_atlanta_fed(save)

        # 3. Indeed
        results["indeed"] = self.collect_indeed(save)

        # Summary
        log.info("=" * 60)
        log.info("COLLECTION SUMMARY")
        log.info("=" * 60)
        total_series = 0
        for source, df in results.items():
            if not df.empty:
                log.info(f"  {source}: {df.shape[1]} series, {df.shape[0]} observations")
                total_series += df.shape[1]
        log.info(f"  TOTAL: {total_series} series")

        return results

    def build_curated_panel(
        self,
        start_date: str = DEFAULT_START_DATE,
        frequency: str = "M"
    ) -> pd.DataFrame:
        """
        Build a curated panel combining all sources, aligned to specified frequency.

        Args:
            start_date: Start date for panel
            frequency: Target frequency ('D', 'W', 'M', 'Q')

        Returns:
            DataFrame with all series aligned to common frequency
        """
        log.info("Building curated labor panel...")

        # Load raw data
        fred_path = LABOR_RAW_DIR / "fred_labor.parquet"
        atl_path = LABOR_RAW_DIR / "atlanta_fed_wages.parquet"
        indeed_path = LABOR_RAW_DIR / "indeed_postings.parquet"

        frames = []

        if fred_path.exists():
            df_fred = pd.read_parquet(fred_path)
            frames.append(df_fred)
            log.info(f"Loaded FRED: {df_fred.shape}")

        if atl_path.exists():
            df_atl = pd.read_parquet(atl_path)
            frames.append(df_atl)
            log.info(f"Loaded Atlanta Fed: {df_atl.shape}")

        if indeed_path.exists():
            df_indeed = pd.read_parquet(indeed_path)
            frames.append(df_indeed)
            log.info(f"Loaded Indeed: {df_indeed.shape}")

        if not frames:
            log.error("No data loaded")
            return pd.DataFrame()

        # Combine all frames
        panel = pd.concat(frames, axis=1)
        panel = panel[panel.index >= start_date]

        # Resample to target frequency
        if frequency == "D":
            panel = panel.resample("D").ffill()
        elif frequency == "W":
            panel = panel.resample("W-FRI").last()
        elif frequency == "M":
            panel = panel.resample("ME").last()
        elif frequency == "Q":
            panel = panel.resample("QE").last()

        # Save curated panel
        out_path = LABOR_CURATED_DIR / f"labor_panel_{frequency.lower()}.parquet"
        write_parquet(panel, out_path)
        log.info(f"Saved curated panel to {out_path}")
        log.info(f"Panel shape: {panel.shape}")

        return panel


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """Run full labor data collection."""
    import argparse

    parser = argparse.ArgumentParser(description="Collect labor market data")
    parser.add_argument(
        "--source",
        choices=["all", "fred", "atlanta_fed", "indeed"],
        default="all",
        help="Data source to collect"
    )
    parser.add_argument(
        "--start-date",
        default=DEFAULT_START_DATE,
        help="Start date for collection (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--build-panel",
        action="store_true",
        help="Build curated panel after collection"
    )
    args = parser.parse_args()

    collector = LaborDataCollector()

    if args.source == "all":
        collector.collect_all(args.start_date)
    elif args.source == "fred":
        collector.collect_fred_labor(args.start_date)
    elif args.source == "atlanta_fed":
        collector.collect_atlanta_fed()
    elif args.source == "indeed":
        collector.collect_indeed()

    if args.build_panel:
        collector.build_curated_panel(args.start_date)


if __name__ == "__main__":
    main()
