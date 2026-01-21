"""
Data Validation Module
Lighthouse Macro - January 2026

Validates all data sources and generates a status report.
Checks:
- FRED API connectivity and series availability
- Data freshness (last update dates)
- Data completeness
- Current readings for key metrics
"""

import pandas as pd
import requests
from datetime import datetime, timedelta
from pathlib import Path

from ..config import CONFIG
from ..utils.logging import get_logger

log = get_logger(__name__)


# FRED Series to Validate
CRITICAL_SERIES = {
    # Liquidity
    "WRESBAL": "Bank Reserves",
    "RRPONTSYD": "RRP Balance",
    "WTREGEN": "TGA Balance",
    "WALCL": "Fed Total Assets",

    # Rates
    "SOFR": "SOFR",
    "EFFR": "EFFR",
    "DGS10": "10Y Treasury",
    "DGS2": "2Y Treasury",

    # Labor
    "JTSQUR": "Quits Rate",
    "JTSHIL": "Hires Level",
    "ICSA": "Initial Claims",
    "UNRATE": "Unemployment Rate",

    # Consumer
    "PSAVERT": "Savings Rate",
    "DRCCLACBS": "CC Delinquency",

    # Credit
    "BAMLH0A0HYM2": "HY OAS",
}

# Expected update frequencies (days)
EXPECTED_FREQUENCIES = {
    "WRESBAL": 7,      # Weekly
    "RRPONTSYD": 1,    # Daily
    "WTREGEN": 7,      # Weekly
    "WALCL": 7,        # Weekly
    "SOFR": 1,         # Daily
    "EFFR": 1,         # Daily
    "DGS10": 1,        # Daily
    "DGS2": 1,         # Daily
    "JTSQUR": 35,      # Monthly (JOLTS has lag)
    "JTSHIL": 35,      # Monthly
    "ICSA": 7,         # Weekly
    "UNRATE": 35,      # Monthly
    "PSAVERT": 35,     # Monthly
    "DRCCLACBS": 95,   # Quarterly
    "BAMLH0A0HYM2": 1, # Daily
}


def check_fred_api() -> dict:
    """Test FRED API connectivity."""
    api_key = CONFIG.fred_api_key
    if not api_key:
        return {'status': 'ERROR', 'message': 'FRED_API_KEY not set'}

    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": "DGS10",
        "api_key": api_key,
        "file_type": "json",
        "limit": 1
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return {'status': 'OK', 'message': 'FRED API accessible'}
    except Exception as e:
        return {'status': 'ERROR', 'message': str(e)}


def validate_series(series_id: str, api_key: str) -> dict:
    """
    Validate a single FRED series.

    Returns dict with:
    - status: OK, WARNING, ERROR
    - last_date: Most recent observation date
    - last_value: Most recent value
    - staleness_days: Days since last update
    - message: Status message
    """
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 5
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json().get('observations', [])

        if not data:
            return {
                'status': 'ERROR',
                'last_date': None,
                'last_value': None,
                'staleness_days': None,
                'message': 'No data returned'
            }

        # Get most recent valid observation
        for obs in data:
            if obs['value'] != '.':  # FRED uses '.' for missing values
                last_date = pd.Timestamp(obs['date'])
                last_value = float(obs['value'])
                break
        else:
            return {
                'status': 'ERROR',
                'last_date': None,
                'last_value': None,
                'staleness_days': None,
                'message': 'No valid observations'
            }

        # Calculate staleness
        staleness_days = (datetime.now() - last_date).days
        expected_freq = EXPECTED_FREQUENCIES.get(series_id, 30)

        # Determine status
        if staleness_days > expected_freq * 2:
            status = 'ERROR'
            message = f'Stale data ({staleness_days} days old)'
        elif staleness_days > expected_freq:
            status = 'WARNING'
            message = f'Possibly stale ({staleness_days} days)'
        else:
            status = 'OK'
            message = 'Current'

        return {
            'status': status,
            'last_date': last_date.strftime('%Y-%m-%d'),
            'last_value': last_value,
            'staleness_days': staleness_days,
            'message': message
        }

    except Exception as e:
        return {
            'status': 'ERROR',
            'last_date': None,
            'last_value': None,
            'staleness_days': None,
            'message': str(e)
        }


def validate_local_data() -> dict:
    """
    Validate locally stored parquet files.

    Returns dict of file paths and their status.
    """
    results = {}

    data_files = [
        CONFIG.raw_dir / "fred" / "fred_raw.parquet",
        CONFIG.raw_dir / "fred" / "fred_extended.parquet",
        CONFIG.raw_dir / "crypto" / "crypto_raw.parquet",
        CONFIG.raw_dir / "market" / "market_raw.parquet",
        CONFIG.raw_dir / "volatility" / "volatility_raw.parquet",
        CONFIG.curated_dir / "macro_master_panel.parquet",
        CONFIG.curated_dir / "crypto_master_panel.parquet",
        CONFIG.curated_dir / "chartbook_master_data.parquet",
        CONFIG.indicators_dir / "indicators_daily.parquet",
    ]

    for file_path in data_files:
        if file_path.exists():
            try:
                df = pd.read_parquet(file_path)
                last_date = df.index.max() if isinstance(df.index, pd.DatetimeIndex) else None
                staleness = (datetime.now() - last_date).days if last_date else None

                results[str(file_path.name)] = {
                    'exists': True,
                    'rows': len(df),
                    'columns': len(df.columns),
                    'last_date': last_date.strftime('%Y-%m-%d') if last_date else 'N/A',
                    'staleness_days': staleness,
                    'status': 'OK' if staleness and staleness < 7 else 'WARNING'
                }
            except Exception as e:
                results[str(file_path.name)] = {
                    'exists': True,
                    'status': 'ERROR',
                    'message': str(e)
                }
        else:
            results[str(file_path.name)] = {
                'exists': False,
                'status': 'MISSING'
            }

    return results


def run_full_validation() -> dict:
    """
    Run full validation of all data sources.

    Returns comprehensive validation report.
    """
    log.info("=" * 60)
    log.info("LIGHTHOUSE MACRO DATA VALIDATION")
    log.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info("=" * 60)

    report = {
        'timestamp': datetime.now().isoformat(),
        'api_status': {},
        'series_status': {},
        'local_data': {},
        'summary': {}
    }

    # 1. Check API connectivity
    log.info("\n--- API CONNECTIVITY ---")
    api_check = check_fred_api()
    report['api_status']['FRED'] = api_check
    log.info(f"FRED API: {api_check['status']} - {api_check['message']}")

    if api_check['status'] != 'OK':
        log.error("Cannot proceed without FRED API access")
        return report

    # 2. Validate critical series
    log.info("\n--- FRED SERIES VALIDATION ---")
    api_key = CONFIG.fred_api_key

    ok_count = 0
    warn_count = 0
    error_count = 0

    for series_id, name in CRITICAL_SERIES.items():
        result = validate_series(series_id, api_key)
        report['series_status'][series_id] = {
            'name': name,
            **result
        }

        status_icon = "  " if result['status'] == 'OK' else "!!" if result['status'] == 'ERROR' else "! "
        value_str = f"{result['last_value']:.2f}" if result['last_value'] else 'N/A'
        log.info(f"{status_icon} {series_id:15} ({name:20}): {value_str:>12} | {result['last_date'] or 'N/A':>10} | {result['message']}")

        if result['status'] == 'OK':
            ok_count += 1
        elif result['status'] == 'WARNING':
            warn_count += 1
        else:
            error_count += 1

    # 3. Validate local data
    log.info("\n--- LOCAL DATA VALIDATION ---")
    local_results = validate_local_data()
    report['local_data'] = local_results

    for filename, data in local_results.items():
        if data.get('exists'):
            if data['status'] == 'OK':
                log.info(f"   {filename:40}: {data['rows']:>6} rows | {data['columns']:>3} cols | Last: {data['last_date']}")
            else:
                log.warning(f"!  {filename:40}: {data.get('message', data['status'])}")
        else:
            log.warning(f"!! {filename:40}: MISSING")

    # 4. Summary
    report['summary'] = {
        'total_series': len(CRITICAL_SERIES),
        'ok_count': ok_count,
        'warning_count': warn_count,
        'error_count': error_count,
        'overall_status': 'OK' if error_count == 0 and warn_count == 0 else
                          'WARNING' if error_count == 0 else 'ERROR'
    }

    log.info("\n" + "=" * 60)
    log.info("VALIDATION SUMMARY")
    log.info("=" * 60)
    log.info(f"Total Series Checked: {len(CRITICAL_SERIES)}")
    log.info(f"  OK:      {ok_count}")
    log.info(f"  Warning: {warn_count}")
    log.info(f"  Error:   {error_count}")
    log.info(f"\nOverall Status: {report['summary']['overall_status']}")
    log.info("=" * 60)

    return report


def get_current_readings() -> dict:
    """
    Get current readings for all key metrics (from Horizon Report checklist).
    """
    api_key = CONFIG.fred_api_key
    if not api_key:
        return {}

    readings = {}

    checklist_series = {
        # From validation checklist in the document
        "PAYEMS": "Nonfarm Payrolls (K)",
        "JTSQUR": "Quits Rate (%)",
        "PSAVERT": "Savings Rate (%)",
        "WRESBAL": "Bank Reserves ($B)",
        "RRPONTSYD": "RRP Balance ($B)",
        "SOFR": "SOFR (%)",
        "EFFR": "EFFR (%)",
        "DGS10": "10Y Yield (%)",
        "BAMLH0A0HYM2": "HY OAS (bps)",
        "ICSA": "Initial Claims (K)",
    }

    log.info("\n" + "=" * 60)
    log.info("CURRENT READINGS - KEY METRICS")
    log.info("=" * 60)

    for series_id, name in checklist_series.items():
        result = validate_series(series_id, api_key)
        if result['last_value']:
            # Format based on series
            if series_id in ['WRESBAL', 'RRPONTSYD']:
                value = result['last_value'] / 1e6  # Convert millions to billions
                formatted = f"${value:.1f}B"
            elif series_id == 'PAYEMS':
                value = result['last_value']
                formatted = f"{value:.0f}K"
            elif series_id == 'ICSA':
                value = result['last_value'] / 1000
                formatted = f"{value:.0f}K"
            elif series_id == 'BAMLH0A0HYM2':
                value = result['last_value'] * 100  # OAS is in decimal
                formatted = f"{value:.0f} bps"
            else:
                formatted = f"{result['last_value']:.2f}"

            readings[series_id] = {
                'name': name,
                'value': result['last_value'],
                'formatted': formatted,
                'date': result['last_date']
            }
            log.info(f"{name:30}: {formatted:>15} (as of {result['last_date']})")
        else:
            log.warning(f"{name:30}: DATA UNAVAILABLE")

    log.info("=" * 60)

    return readings


def print_validation_report():
    """Print a formatted validation report."""
    run_full_validation()
    print("\n")
    get_current_readings()


if __name__ == "__main__":
    print_validation_report()
