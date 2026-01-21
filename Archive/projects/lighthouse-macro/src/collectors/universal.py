"""
Lighthouse Macro — Universal Data Collector
Load data from ANY source: CSV, Excel, JSON, API, manual input
"""

from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Union
import pandas as pd
import numpy as np

from collectors.base import BaseCollector


class UniversalCollector(BaseCollector):
    """
    Universal data collector that can load from any source.

    Supports:
    - CSV files (local or URL)
    - Excel files
    - JSON files
    - Parquet files
    - Manual DataFrame input
    - Any custom source via plugin
    """

    def __init__(self):
        super().__init__("universal")

    def fetch(self, *args, **kwargs):
        """Not applicable for universal collector - use specific load methods."""
        raise NotImplementedError("Use load_csv(), load_excel(), etc. instead")

    def fetch_bulk(self, *args, **kwargs):
        """Not applicable for universal collector."""
        raise NotImplementedError("Use load_csv(), load_excel(), etc. instead")

    def load_csv(
        self,
        filepath: str,
        series_name: str,
        date_column: str = "date",
        value_column: Optional[str] = None,
        date_format: Optional[str] = None,
        **pandas_kwargs
    ) -> pd.DataFrame:
        """
        Load data from CSV file.

        Args:
            filepath: Path to CSV file (local or URL)
            series_name: Name for the series
            date_column: Name of date column
            value_column: Name of value column (if None, uses first non-date column)
            date_format: Date parsing format
            **pandas_kwargs: Additional arguments for pd.read_csv()

        Returns:
            DataFrame with datetime index and series column
        """
        # Load CSV
        df = pd.read_csv(filepath, **pandas_kwargs)

        # Parse dates
        if date_format:
            df[date_column] = pd.to_datetime(df[date_column], format=date_format)
        else:
            df[date_column] = pd.to_datetime(df[date_column])

        # Set index
        df = df.set_index(date_column)

        # Select value column
        if value_column is None:
            # Use first column that isn't the date
            value_column = [col for col in df.columns if col != date_column][0]

        # Rename and select
        result = df[[value_column]].copy()
        result.columns = [series_name]

        # Save
        self._save_universal(result, series_name, source="CSV")

        return result

    def load_excel(
        self,
        filepath: str,
        series_name: str,
        sheet_name: Union[str, int] = 0,
        date_column: str = "date",
        value_column: Optional[str] = None,
        **pandas_kwargs
    ) -> pd.DataFrame:
        """
        Load data from Excel file.

        Args:
            filepath: Path to Excel file
            series_name: Name for the series
            sheet_name: Sheet name or index
            date_column: Name of date column
            value_column: Name of value column
            **pandas_kwargs: Additional arguments for pd.read_excel()

        Returns:
            DataFrame with datetime index
        """
        df = pd.read_excel(filepath, sheet_name=sheet_name, **pandas_kwargs)

        # Parse dates
        df[date_column] = pd.to_datetime(df[date_column])
        df = df.set_index(date_column)

        # Select value column
        if value_column is None:
            value_column = [col for col in df.columns if col != date_column][0]

        result = df[[value_column]].copy()
        result.columns = [series_name]

        self._save_universal(result, series_name, source="Excel")

        return result

    def load_json(
        self,
        filepath: str,
        series_name: str,
        date_field: str = "date",
        value_field: str = "value",
        **pandas_kwargs
    ) -> pd.DataFrame:
        """Load data from JSON file."""
        df = pd.read_json(filepath, **pandas_kwargs)

        df[date_field] = pd.to_datetime(df[date_field])
        df = df.set_index(date_field)

        result = df[[value_field]].copy()
        result.columns = [series_name]

        self._save_universal(result, series_name, source="JSON")

        return result

    def load_dataframe(
        self,
        df: pd.DataFrame,
        series_name: str,
        date_column: Optional[str] = None,
        value_column: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Load from an existing DataFrame.
        Useful for programmatically constructed data or API responses.

        Args:
            df: Input DataFrame
            series_name: Name for the series
            date_column: Column to use as date index (if not already indexed)
            value_column: Column to use as values

        Returns:
            Properly formatted DataFrame
        """
        df = df.copy()

        # Handle index
        if date_column and date_column in df.columns:
            df[date_column] = pd.to_datetime(df[date_column])
            df = df.set_index(date_column)
        elif not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)

        # Select value column
        if value_column:
            result = df[[value_column]].copy()
            result.columns = [series_name]
        else:
            result = df.copy()
            if len(result.columns) == 1:
                result.columns = [series_name]

        self._save_universal(result, series_name, source="DataFrame")

        return result

    def load_manual(
        self,
        dates: List[str],
        values: List[float],
        series_name: str,
        date_format: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Load manually entered data.

        Args:
            dates: List of date strings
            values: List of values
            series_name: Name for the series
            date_format: Date parsing format

        Returns:
            DataFrame with datetime index
        """
        if date_format:
            dates_parsed = pd.to_datetime(dates, format=date_format)
        else:
            dates_parsed = pd.to_datetime(dates)

        result = pd.DataFrame(
            {series_name: values},
            index=dates_parsed
        )

        self._save_universal(result, series_name, source="Manual")

        return result

    def _save_universal(self, df: pd.DataFrame, series_name: str, source: str):
        """Save universal data with metadata."""
        # Save to data/universal/ directory
        save_dir = self.config.data_dir / "universal"
        save_dir.mkdir(parents=True, exist_ok=True)

        # Timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save data
        filepath = save_dir / f"{series_name}_{timestamp}.parquet"
        df.to_parquet(filepath)

        # Save latest
        latest_path = save_dir / f"{series_name}_latest.parquet"
        df.to_parquet(latest_path)

        # Save metadata
        metadata = {
            "series_name": series_name,
            "source": source,
            "timestamp": timestamp,
            "start_date": str(df.index.min()),
            "end_date": str(df.index.max()),
            "observations": len(df),
            "frequency": pd.infer_freq(df.index),
        }

        import json
        meta_path = save_dir / f"{series_name}_metadata.json"
        with open(meta_path, 'w') as f:
            json.dump(metadata, f, indent=2)

    def align_series(
        self,
        series_dict: Dict[str, pd.Series],
        method: str = "inner",
        fill_method: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Align multiple series to common date range.

        Args:
            series_dict: Dictionary of {name: series}
            method: 'inner' (intersection) or 'outer' (union)
            fill_method: 'ffill', 'bfill', 'interpolate', or None

        Returns:
            Aligned DataFrame with all series
        """
        # Combine
        df = pd.DataFrame(series_dict)

        # Align
        if method == "inner":
            df = df.dropna()
        elif method == "outer":
            if fill_method == "ffill":
                df = df.ffill()
            elif fill_method == "bfill":
                df = df.bfill()
            elif fill_method == "interpolate":
                df = df.interpolate(method='time')

        return df


class DataPipeline:
    """
    End-to-end data pipeline: fetch → clean → transform → align → chart

    Example:
        pipeline = DataPipeline()
        pipeline.add_series("payrolls", source="FRED", series_id="PAYEMS")
        pipeline.add_series("defaults", source="CSV", filepath="moodys_edf.csv")
        pipeline.transform("payrolls", "yoy_pct", periods=12)
        pipeline.align(method="inner")
        chart_data = pipeline.get_chart_data()
    """

    def __init__(self):
        self.series = {}
        self.metadata = {}
        self.aligned_data = None

    def add_series(
        self,
        name: str,
        source: str,
        **kwargs
    ) -> None:
        """
        Add a series to the pipeline.

        Args:
            name: Series name
            source: Data source ('FRED', 'CSV', 'Excel', 'JSON', 'Manual', 'DataFrame')
            **kwargs: Source-specific arguments
        """
        if source == "FRED":
            from collectors import FREDCollector
            collector = FREDCollector()
            series_id = kwargs.get("series_id")
            start_date = kwargs.get("start_date")

            df = collector.load_latest(series_id)
            if df is None or (start_date and df.index.min() > pd.to_datetime(start_date)):
                df = collector.fetch(series_id, start_date=start_date)

            self.series[name] = df[series_id]
            self.metadata[name] = {"source": "FRED", "series_id": series_id}

        elif source == "CSV":
            collector = UniversalCollector()
            df = collector.load_csv(series_name=name, **kwargs)
            self.series[name] = df[name]
            self.metadata[name] = {"source": "CSV", "filepath": kwargs.get("filepath")}

        elif source == "Excel":
            collector = UniversalCollector()
            df = collector.load_excel(series_name=name, **kwargs)
            self.series[name] = df[name]
            self.metadata[name] = {"source": "Excel", "filepath": kwargs.get("filepath")}

        elif source == "DataFrame":
            collector = UniversalCollector()
            df = collector.load_dataframe(series_name=name, **kwargs)
            self.series[name] = df[name]
            self.metadata[name] = {"source": "DataFrame"}

        elif source == "Manual":
            collector = UniversalCollector()
            df = collector.load_manual(series_name=name, **kwargs)
            self.series[name] = df[name]
            self.metadata[name] = {"source": "Manual"}

        else:
            raise ValueError(f"Unknown source: {source}")

    def transform(self, series_name: str, transform_type: str, **kwargs) -> None:
        """
        Apply transformation to a series.

        Args:
            series_name: Name of series to transform
            transform_type: Type of transformation
            **kwargs: Transform-specific arguments
        """
        from transformers import (
            yoy_pct, mom, zscore, zscore_rolling,
            index_to_base, ma_12m, ma_3m
        )

        series = self.series[series_name]

        if transform_type == "yoy_pct":
            self.series[series_name] = yoy_pct(series, **kwargs)
        elif transform_type == "mom":
            self.series[series_name] = mom(series, **kwargs)
        elif transform_type == "zscore":
            self.series[series_name] = zscore(series)
        elif transform_type == "zscore_rolling":
            self.series[series_name] = zscore_rolling(series, **kwargs)
        elif transform_type == "index_to_base":
            self.series[series_name] = index_to_base(series, **kwargs)
        elif transform_type == "ma_12m":
            self.series[series_name] = ma_12m(series)
        elif transform_type == "ma_3m":
            self.series[series_name] = ma_3m(series)
        else:
            raise ValueError(f"Unknown transform: {transform_type}")

    def align(self, method: str = "inner", fill_method: Optional[str] = None) -> None:
        """Align all series to common date range."""
        collector = UniversalCollector()
        self.aligned_data = collector.align_series(
            self.series,
            method=method,
            fill_method=fill_method
        )

    def get_chart_data(self) -> pd.DataFrame:
        """Get aligned data ready for charting."""
        if self.aligned_data is None:
            self.align()
        return self.aligned_data

    def describe(self) -> Dict:
        """Get pipeline summary."""
        summary = {
            "series_count": len(self.series),
            "series": {}
        }

        for name, series in self.series.items():
            summary["series"][name] = {
                "start": str(series.index.min()) if len(series) > 0 else None,
                "end": str(series.index.max()) if len(series) > 0 else None,
                "observations": len(series),
                "metadata": self.metadata.get(name, {})
            }

        if self.aligned_data is not None:
            summary["aligned"] = {
                "start": str(self.aligned_data.index.min()),
                "end": str(self.aligned_data.index.max()),
                "observations": len(self.aligned_data)
            }

        return summary
