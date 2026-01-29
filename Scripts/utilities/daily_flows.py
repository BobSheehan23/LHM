#!/usr/bin/env python3
"""
LIGHTHOUSE MACRO | DAILY FLOWS PIPELINE
Orchestration script for 06:00 ET daily run.

Pulls from:
- Lighthouse_Master.db (1000+ FRED series)
- real_data_fetcher.py (NY Fed, Treasury, BLS, BEA live APIs)
- DefiLlama (stablecoin data for SLI)

Author: Bob Sheehan, CFA, CMT
"""

import os
import sys
import json
import sqlite3
import logging
import requests
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import numpy as np

# Add HORIZON_FINAL to path for imports
HORIZON_DIR = Path.home() / 'Desktop' / 'HORIZON_FINAL.'
sys.path.insert(0, str(HORIZON_DIR))

from real_data_fetcher import RealDataFetcher
from horizon_q1_2026 import LighthouseMacroEngine, apply_lighthouse_style

# =============================================================================
# CONFIGURATION
# =============================================================================

# Databases
MASTER_DB = HORIZON_DIR / 'Lighthouse_Master.db'
QUANT_DB = HORIZON_DIR / 'Macro_Quant_Database.db'

# Output directories
OUTPUT_DIR = Path.home() / 'lighthouse_output'
LOG_DIR = OUTPUT_DIR / 'logs'
CHARTS_DIR = OUTPUT_DIR / 'charts'
DATA_DIR = OUTPUT_DIR / 'data'

for d in [OUTPUT_DIR, LOG_DIR, CHARTS_DIR, DATA_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f'daily_{datetime.now():%Y%m%d}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging.getLogger('lighthouse')


# =============================================================================
# DATABASE QUERIES
# =============================================================================

def query_series(db_path, series_id):
    """Pull a single series from the database."""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(f"""
        SELECT date, value FROM observations
        WHERE series_id = ?
        ORDER BY date
    """, conn, params=[series_id])
    conn.close()

    if len(df) > 0:
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        return df['value']
    return pd.Series(dtype=float)


def query_latest(db_path, series_id):
    """Get the most recent value for a series."""
    conn = sqlite3.connect(db_path)
    result = conn.execute("""
        SELECT value FROM observations
        WHERE series_id = ?
        ORDER BY date DESC LIMIT 1
    """, [series_id]).fetchone()
    conn.close()
    return result[0] if result else None


def get_db_stats(db_path):
    """Get database health stats."""
    conn = sqlite3.connect(db_path)
    series_count = conn.execute("SELECT COUNT(*) FROM series_meta").fetchone()[0]
    obs_count = conn.execute("SELECT COUNT(*) FROM observations").fetchone()[0]
    latest = conn.execute("SELECT MAX(date) FROM observations").fetchone()[0]
    conn.close()
    return {'series': series_count, 'observations': obs_count, 'latest_date': latest}


def init_indices_table(db_path):
    """Create lighthouse_indices table if it doesn't exist."""
    conn = sqlite3.connect(db_path)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS lighthouse_indices (
            date TEXT NOT NULL,
            index_id TEXT NOT NULL,
            value REAL,
            status TEXT,
            PRIMARY KEY (date, index_id)
        )
    ''')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_indices_date ON lighthouse_indices(date)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_indices_id ON lighthouse_indices(index_id)')
    conn.commit()
    conn.close()


def write_indices_to_db(db_path, metrics):
    """Write computed indices to Lighthouse_Master.db."""
    init_indices_table(db_path)

    date_str = metrics['date'].strftime('%Y-%m-%d')

    records = [
        (date_str, 'LFI', metrics['lfi'][0], metrics['lfi'][1]),
        (date_str, 'LCI', metrics['lci'][0], metrics['lci'][1]),
        (date_str, 'CLG', metrics['clg'][0], metrics['clg'][1]),
        (date_str, 'SLI', metrics['sli'][0], metrics['sli'][1]),
        (date_str, 'MRI', metrics['mri'][0], metrics['mri'][1]),
    ]

    # Also store component data
    if len(metrics['sli']) > 2:
        sli_data = metrics['sli'][2]
        records.extend([
            (date_str, 'SLI_MCAP', sli_data['mcap_current'], None),
            (date_str, 'SLI_ROC_30D', sli_data['roc_30d'], None),
            (date_str, 'SLI_ROC_90D_ANN', sli_data['roc_90d_ann'], None),
        ])

    conn = sqlite3.connect(db_path)
    conn.executemany('''
        INSERT OR REPLACE INTO lighthouse_indices (date, index_id, value, status)
        VALUES (?, ?, ?, ?)
    ''', records)
    conn.commit()

    count = conn.execute('SELECT COUNT(*) FROM lighthouse_indices WHERE date = ?', [date_str]).fetchone()[0]
    conn.close()

    log.info(f'Wrote {count} indices to lighthouse_indices for {date_str}')
    return count


# =============================================================================
# STABLECOIN DATA (DefiLlama)
# =============================================================================

def fetch_stablecoin_data():
    """
    Fetch stablecoin market cap from DefiLlama.
    Returns current, 30d ago, and 90d ago for SLI calculation.
    """
    try:
        # Use the historical charts endpoint which has full time series
        # This endpoint returns total stablecoin mcap across all chains
        hist_url = "https://stablecoins.llama.fi/stablecoincharts/all?stablecoin=1"
        response = requests.get(hist_url, timeout=30)
        response.raise_for_status()
        data = response.json()

        if not data or len(data) == 0:
            log.warning('DefiLlama returned empty data')
            return None

        # Parse time series
        records = []
        for item in data:
            ts = item.get('date')
            circ = item.get('totalCirculating', {})
            mcap = circ.get('peggedUSD', 0) if isinstance(circ, dict) else 0
            if ts and mcap:
                records.append({'date': ts, 'mcap': mcap / 1e9})

        if not records:
            log.warning('Could not parse DefiLlama data')
            return None

        df = pd.DataFrame(records)
        df['date'] = pd.to_datetime(df['date'], unit='s')
        df = df.set_index('date').sort_index()

        # Current (most recent)
        current = df['mcap'].iloc[-1]
        now = df.index[-1]

        # 30d and 90d ago
        date_30d = now - timedelta(days=30)
        date_90d = now - timedelta(days=90)

        # Find closest values
        mcap_30d = df.loc[df.index <= date_30d, 'mcap'].iloc[-1] if (df.index <= date_30d).any() else current * 0.97
        mcap_90d = df.loc[df.index <= date_90d, 'mcap'].iloc[-1] if (df.index <= date_90d).any() else current * 0.90

        log.info(f'Stablecoin mcap: ${current:.1f}B (30d ago: ${mcap_30d:.1f}B, 90d ago: ${mcap_90d:.1f}B)')

        return {
            'stablecoin_mcap': current,
            'stablecoin_mcap_30d_ago': mcap_30d,
            'stablecoin_mcap_90d_ago': mcap_90d,
        }

    except Exception as e:
        log.error(f'DefiLlama fetch failed: {e}')
        return None


# =============================================================================
# DATA AGGREGATION
# =============================================================================

def fetch_all_data():
    """
    Aggregate data from all sources:
    - Lighthouse_Master.db for FRED series
    - real_data_fetcher for live NY Fed / BLS data
    - DefiLlama for stablecoin data
    """
    data = {}
    fetcher = RealDataFetcher()

    log.info('Fetching from Lighthouse_Master.db...')

    # Bank Reserves (FRED: WRESBAL)
    reserves = query_latest(MASTER_DB, 'WRESBAL')
    if reserves:
        data['bank_reserves'] = reserves / 1000  # Convert to billions
        log.info(f'  Reserves: ${data["bank_reserves"]:.0f}B')

    # GDP (FRED: GDP)
    gdp = query_latest(MASTER_DB, 'GDP')
    if gdp:
        data['gdp_nominal'] = gdp
        log.info(f'  GDP: ${gdp:.0f}B')

    # HY OAS (FRED: BAMLH0A0HYM2)
    hy_oas = query_latest(MASTER_DB, 'BAMLH0A0HYM2')
    if hy_oas:
        data['hy_oas'] = hy_oas * 100  # Convert to bps
        log.info(f'  HY OAS: {data["hy_oas"]:.0f} bps')

    # VIX (FRED: VIXCLS)
    vix = query_latest(MASTER_DB, 'VIXCLS')
    if vix:
        data['vix'] = vix
        log.info(f'  VIX: {vix:.2f}')

    # Unemployment (FRED: UNRATE)
    unrate = query_latest(MASTER_DB, 'UNRATE')
    if unrate:
        data['unemployment_rate'] = unrate
        log.info(f'  Unemployment: {unrate:.1f}%')

    # Long-term unemployment share (calculate from FRED series)
    long_term = query_latest(MASTER_DB, 'LNS13025703')  # 27+ weeks unemployed (thousands)
    total_unemp = query_latest(MASTER_DB, 'UNEMPLOY')    # Total unemployed (thousands)
    if long_term and total_unemp and total_unemp > 0:
        data['long_term_unemp_share'] = long_term / total_unemp
        log.info(f'  Long-term unemp share: {data["long_term_unemp_share"]*100:.1f}%')

    # Live NY Fed data
    log.info('Fetching from NY Fed API...')
    try:
        sofr_effr = fetcher.get_sofr_effr_spread()
        if len(sofr_effr) > 0:
            data['sofr'] = sofr_effr['sofr'].iloc[-1]
            data['effr'] = sofr_effr['effr'].iloc[-1]
            log.info(f'  SOFR: {data["sofr"]:.2f}%, EFFR: {data["effr"]:.2f}%')

        rrp = fetcher.get_rrp_usage()
        if len(rrp) > 0:
            data['on_rrp'] = rrp['totalAmtAccepted'].iloc[-1]
            log.info(f'  ON RRP: ${data["on_rrp"]:.1f}B')
    except Exception as e:
        log.warning(f'NY Fed fetch error: {e}')

    # Live BLS data (JOLTS)
    log.info('Fetching from BLS API...')
    try:
        labor = fetcher.get_labor_data()
        if len(labor.get('quits', [])) > 0:
            data['quits_rate'] = labor['quits'].iloc[-1]
            log.info(f'  Quits rate: {data["quits_rate"]:.1f}%')
        if len(labor.get('hires', [])) > 0:
            data['hires_rate'] = labor['hires'].iloc[-1]
            log.info(f'  Hires rate: {data["hires_rate"]:.1f}%')
    except Exception as e:
        log.warning(f'BLS fetch error: {e}')

    # Yields from FRED
    log.info('Fetching yields...')
    try:
        yields = fetcher.get_yield_curve()
        if '10Y' in yields and len(yields['10Y']) > 0:
            data['10y_yield'] = yields['10Y'].iloc[-1]
            log.info(f'  10Y: {data["10y_yield"]:.2f}%')
        if '30Y' in yields and len(yields['30Y']) > 0:
            data['30y_yield'] = yields['30Y'].iloc[-1]
            log.info(f'  30Y: {data["30y_yield"]:.2f}%')
    except Exception as e:
        log.warning(f'Yield fetch error: {e}')

    # Stablecoin data for SLI
    log.info('Fetching stablecoin data...')
    stable_data = fetch_stablecoin_data()
    if stable_data:
        data.update(stable_data)

    return data


# =============================================================================
# PIPELINE STAGES
# =============================================================================

def stage_fetch(engine):
    """Stage 1: Fetch fresh data and update engine."""
    log.info('=' * 50)
    log.info('STAGE 1: DATA FETCH')
    log.info('=' * 50)

    # Check database health first
    stats = get_db_stats(MASTER_DB)
    log.info(f'Lighthouse_Master.db: {stats["series"]} series, {stats["observations"]:,} obs')
    log.info(f'Latest data: {stats["latest_date"]}')

    try:
        fresh_data = fetch_all_data()
        engine.data.update(fresh_data)
        engine.current_date = datetime.now()
        log.info(f'Engine updated with {len(fresh_data)} fields')
        return True
    except Exception as e:
        log.error(f'Data fetch failed: {e}')
        return False


def stage_compute(engine):
    """Stage 2: Compute all indices."""
    log.info('=' * 50)
    log.info('STAGE 2: INDEX COMPUTATION')
    log.info('=' * 50)

    try:
        metrics = engine.generate_dashboard(include_sli=True)
        return metrics
    except Exception as e:
        log.error(f'Compute failed: {e}')
        return None


def stage_charts(engine, save=True):
    """Stage 3: Generate charts."""
    log.info('=' * 50)
    log.info('STAGE 3: CHART GENERATION')
    log.info('=' * 50)

    apply_lighthouse_style()
    date_str = datetime.now().strftime('%Y%m%d')

    charts = {}
    try:
        charts['reserves'] = engine.plot_reserves_danger_zone()
        charts['savings'] = engine.plot_k_shaped_savings()
        charts['calendar'] = engine.plot_stress_calendar()

        if save:
            for name, fig in charts.items():
                path = CHARTS_DIR / f'{name}_{date_str}.png'
                fig.savefig(path, dpi=150, bbox_inches='tight',
                           facecolor='white', edgecolor='none')
                log.info(f'Saved: {path}')

        log.info(f'Generated {len(charts)} charts')
        return charts
    except Exception as e:
        log.error(f'Chart generation failed: {e}')
        return None


def stage_export(metrics):
    """Stage 4: Export metrics to JSON."""
    log.info('=' * 50)
    log.info('STAGE 4: EXPORT')
    log.info('=' * 50)

    date_str = datetime.now().strftime('%Y%m%d')
    output_path = DATA_DIR / f'metrics_{date_str}.json'

    try:
        export = {
            'timestamp': datetime.now().isoformat(),
            'lfi': metrics['lfi'][0],
            'lfi_status': metrics['lfi'][1],
            'lci': metrics['lci'][0],
            'lci_status': metrics['lci'][1],
            'clg': metrics['clg'][0],
            'clg_status': metrics['clg'][1],
            'sli': metrics['sli'][0],
            'sli_status': metrics['sli'][1],
            'sli_mcap': metrics['sli'][2]['mcap_current'],
            'sli_roc_30d': metrics['sli'][2]['roc_30d'],
            'mri': metrics['mri'][0],
            'mri_status': metrics['mri'][1],
        }

        with open(output_path, 'w') as f:
            json.dump(export, f, indent=2)
        log.info(f'Exported: {output_path}')

        # Latest.json for easy access
        latest_path = DATA_DIR / 'latest.json'
        with open(latest_path, 'w') as f:
            json.dump(export, f, indent=2)

        return export
    except Exception as e:
        log.error(f'Export failed: {e}')
        return None


def stage_persist(metrics):
    """Stage 5: Write indices to Lighthouse_Master.db."""
    log.info('=' * 50)
    log.info('STAGE 5: PERSIST TO DATABASE')
    log.info('=' * 50)

    try:
        count = write_indices_to_db(MASTER_DB, metrics)
        return count
    except Exception as e:
        log.error(f'Database persist failed: {e}')
        return 0


def stage_alerts(metrics):
    """Stage 6: Check alert conditions."""
    log.info('=' * 50)
    log.info('STAGE 6: ALERTS')
    log.info('=' * 50)

    alerts = []

    if metrics['mri'][0] > 1.0:
        alerts.append(f"MRI DEFENSIVE: {metrics['mri'][0]:+.2f}")

    if metrics['lci'][0] < -1.0:
        alerts.append(f"LCI STRESS RISK: {metrics['lci'][0]:+.2f}")

    if metrics['clg'][0] < -1.0:
        alerts.append(f"CLG MISPRICED: {metrics['clg'][0]:+.2f}")

    if metrics['sli'][0] < -1.0:
        alerts.append(f"SLI DRAINING: {metrics['sli'][0]:+.2f}")

    if alerts:
        log.warning('ALERTS TRIGGERED:')
        for alert in alerts:
            log.warning(f'  >> {alert}')
    else:
        log.info('No alerts triggered.')

    return alerts


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def run_daily_pipeline(save_charts=True, show_charts=False):
    """Execute full daily pipeline."""
    log.info('=' * 60)
    log.info('LIGHTHOUSE MACRO | DAILY FLOWS PIPELINE')
    log.info(f'Started: {datetime.now():%Y-%m-%d %H:%M:%S}')
    log.info('=' * 60)

    engine = LighthouseMacroEngine()

    # Stage 1: Fetch
    if not stage_fetch(engine):
        log.error('Pipeline aborted: data fetch failed')
        return None

    # Stage 2: Compute
    metrics = stage_compute(engine)
    if metrics is None:
        log.error('Pipeline aborted: compute failed')
        return None

    # Stage 3: Charts
    charts = stage_charts(engine, save=save_charts)

    # Stage 4: Export
    export = stage_export(metrics)

    # Stage 5: Persist to database
    stage_persist(metrics)

    # Stage 6: Alerts
    alerts = stage_alerts(metrics)

    log.info('=' * 60)
    log.info('PIPELINE COMPLETE')
    log.info('=' * 60)

    if show_charts and charts:
        import matplotlib.pyplot as plt
        plt.show()

    return {
        'metrics': metrics,
        'charts': charts,
        'export': export,
        'alerts': alerts,
    }


def update_fred_database():
    """Run the FRED database update (smart update logic)."""
    log.info('Running FRED database update...')
    sys.path.insert(0, str(HORIZON_DIR))
    from fred_quant_database import run_daily_update
    return run_daily_update(series_per_category=100)


# =============================================================================
# CLI
# =============================================================================

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Lighthouse Macro Daily Pipeline')
    parser.add_argument('--no-save', action='store_true', help='Skip saving charts')
    parser.add_argument('--show', action='store_true', help='Display charts')
    parser.add_argument('--update-db', action='store_true', help='Update FRED database first')
    args = parser.parse_args()

    if args.update_db:
        update_fred_database()

    result = run_daily_pipeline(
        save_charts=not args.no_save,
        show_charts=args.show
    )

    if result and result['alerts']:
        sys.exit(1)
    sys.exit(0)
