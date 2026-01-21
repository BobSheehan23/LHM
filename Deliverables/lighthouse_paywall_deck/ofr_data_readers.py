"""
OFR Data Readers - For manually downloaded CSV files
Use this when OFR API endpoints require authentication

Download sources:
- FSI: https://www.financialresearch.gov/financial-stress-index/
- BSRM: https://www.financialresearch.gov/bank-systemic-risk-monitor/
- STFM: https://www.financialresearch.gov/short-term-funding-monitor/
"""

import pandas as pd
from pathlib import Path
from datetime import datetime


class OFRDataReader:
    """Read manually downloaded OFR data files"""

    def __init__(self, data_dir=None):
        if data_dir is None:
            data_dir = Path(__file__).parent / "data" / "ofr_downloads"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def read_fsi(self, filename='fsi_data.csv'):
        """
        Read Financial Stress Index data

        Download from: https://www.financialresearch.gov/financial-stress-index/
        Save to: data/ofr_downloads/fsi_data.csv

        Returns:
            DataFrame with FSI values and components
        """
        fsi_path = self.data_dir / filename

        if not fsi_path.exists():
            print(f"FSI data not found at {fsi_path}")
            print("Download from: https://www.financialresearch.gov/financial-stress-index/")
            return pd.DataFrame()

        df = pd.read_csv(fsi_path)

        # Parse date column (adjust column name as needed)
        date_col = [col for col in df.columns if 'date' in col.lower()]
        if date_col:
            df[date_col[0]] = pd.to_datetime(df[date_col[0]])
            df = df.set_index(date_col[0]).sort_index()

        return df

    def read_bsrm(self, filename='bsrm_data.csv'):
        """
        Read Bank Systemic Risk Monitor data

        Download from: https://www.financialresearch.gov/bank-systemic-risk-monitor/
        Save to: data/ofr_downloads/bsrm_data.csv

        Returns:
            DataFrame with bank systemic risk metrics
        """
        bsrm_path = self.data_dir / filename

        if not bsrm_path.exists():
            print(f"BSRM data not found at {bsrm_path}")
            print("Download from: https://www.financialresearch.gov/bank-systemic-risk-monitor/")
            return pd.DataFrame()

        df = pd.read_csv(bsrm_path)

        # Parse date column
        date_col = [col for col in df.columns if 'date' in col.lower()]
        if date_col:
            df[date_col[0]] = pd.to_datetime(df[date_col[0]])
            df = df.set_index(date_col[0]).sort_index()

        return df

    def read_stfm_repo(self, filename='stfm_repo_rates.csv'):
        """
        Read STFM repo rates

        Download from: https://www.financialresearch.gov/short-term-funding-monitor/
        Navigate to Repo Rates section and export CSV
        Save to: data/ofr_downloads/stfm_repo_rates.csv

        Returns:
            DataFrame with repo rates
        """
        repo_path = self.data_dir / filename

        if not repo_path.exists():
            print(f"STFM repo data not found at {repo_path}")
            print("Download from: https://www.financialresearch.gov/short-term-funding-monitor/")
            return pd.DataFrame()

        df = pd.read_csv(repo_path)

        # Parse date column
        date_col = [col for col in df.columns if 'date' in col.lower()]
        if date_col:
            df[date_col[0]] = pd.to_datetime(df[date_col[0]])
            df = df.set_index(date_col[0]).sort_index()

        return df

    def read_stfm_cp(self, filename='stfm_commercial_paper.csv'):
        """
        Read STFM commercial paper rates

        Download from: https://www.financialresearch.gov/short-term-funding-monitor/
        Navigate to Commercial Paper section and export CSV
        Save to: data/ofr_downloads/stfm_commercial_paper.csv

        Returns:
            DataFrame with commercial paper rates
        """
        cp_path = self.data_dir / filename

        if not cp_path.exists():
            print(f"STFM CP data not found at {cp_path}")
            print("Download from: https://www.financialresearch.gov/short-term-funding-monitor/")
            return pd.DataFrame()

        df = pd.read_csv(cp_path)

        # Parse date column
        date_col = [col for col in df.columns if 'date' in col.lower()]
        if date_col:
            df[date_col[0]] = pd.to_datetime(df[date_col[0]])
            df = df.set_index(date_col[0]).sort_index()

        return df

    def read_hfm(self, filename='hfm_data.csv'):
        """
        Read Hedge Fund Monitor data

        Download from: https://www.financialresearch.gov/hedge-fund-monitor/
        Save to: data/ofr_downloads/hfm_data.csv

        Returns:
            DataFrame with hedge fund metrics
        """
        hfm_path = self.data_dir / filename

        if not hfm_path.exists():
            print(f"HFM data not found at {hfm_path}")
            print("Download from: https://www.financialresearch.gov/hedge-fund-monitor/")
            return pd.DataFrame()

        df = pd.read_csv(hfm_path)

        # Parse date column
        date_col = [col for col in df.columns if 'date' in col.lower()]
        if date_col:
            df[date_col[0]] = pd.to_datetime(df[date_col[0]])
            df = df.set_index(date_col[0]).sort_index()

        return df

    def get_data_status(self):
        """
        Check which OFR datasets are available locally

        Returns:
            dict with availability status
        """
        status = {
            'fsi': (self.data_dir / 'fsi_data.csv').exists(),
            'bsrm': (self.data_dir / 'bsrm_data.csv').exists(),
            'stfm_repo': (self.data_dir / 'stfm_repo_rates.csv').exists(),
            'stfm_cp': (self.data_dir / 'stfm_commercial_paper.csv').exists(),
            'hfm': (self.data_dir / 'hfm_data.csv').exists(),
        }

        return status

    def print_status(self):
        """Print availability status for all OFR datasets"""
        status = self.get_data_status()

        print("=" * 70)
        print("OFR DATA AVAILABILITY (Manual Downloads)")
        print("=" * 70)

        datasets = {
            'fsi': 'Financial Stress Index',
            'bsrm': 'Bank Systemic Risk Monitor',
            'stfm_repo': 'STFM Repo Rates',
            'stfm_cp': 'STFM Commercial Paper',
            'hfm': 'Hedge Fund Monitor',
        }

        for key, name in datasets.items():
            symbol = "✅" if status[key] else "❌"
            print(f"{symbol} {name:40s} {'AVAILABLE' if status[key] else 'MISSING'}")

        print("\nDownload from:")
        if not status['fsi']:
            print("  FSI:  https://www.financialresearch.gov/financial-stress-index/")
        if not status['bsrm']:
            print("  BSRM: https://www.financialresearch.gov/bank-systemic-risk-monitor/")
        if not status['stfm_repo'] or not status['stfm_cp']:
            print("  STFM: https://www.financialresearch.gov/short-term-funding-monitor/")
        if not status['hfm']:
            print("  HFM:  https://www.financialresearch.gov/hedge-fund-monitor/")

        print("\nSave files to:", self.data_dir)
        print("=" * 70)


# Convenience functions
def get_fsi_data():
    """Quick access to FSI data"""
    reader = OFRDataReader()
    return reader.read_fsi()


def get_bsrm_data():
    """Quick access to BSRM data"""
    reader = OFRDataReader()
    return reader.read_bsrm()


def get_repo_rates():
    """Quick access to STFM repo rates"""
    reader = OFRDataReader()
    return reader.read_stfm_repo()


def get_cp_rates():
    """Quick access to STFM commercial paper rates"""
    reader = OFRDataReader()
    return reader.read_stfm_cp()


def get_hfm_data():
    """Quick access to HFM data"""
    reader = OFRDataReader()
    return reader.read_hfm()


if __name__ == "__main__":
    reader = OFRDataReader()
    reader.print_status()

    # Try to load any available data
    print("\nAttempting to load available data...\n")

    fsi = reader.read_fsi()
    if not fsi.empty:
        print(f"✓ FSI data loaded: {len(fsi)} observations")
        print(f"  Latest FSI: {fsi.iloc[-1].values[0] if len(fsi) > 0 else 'N/A'}")

    bsrm = reader.read_bsrm()
    if not bsrm.empty:
        print(f"✓ BSRM data loaded: {len(bsrm)} observations")

    repo = reader.read_stfm_repo()
    if not repo.empty:
        print(f"✓ STFM Repo data loaded: {len(repo)} observations")

    cp = reader.read_stfm_cp()
    if not cp.empty:
        print(f"✓ STFM CP data loaded: {len(cp)} observations")

    hfm = reader.read_hfm()
    if not hfm.empty:
        print(f"✓ HFM data loaded: {len(hfm)} observations")
