"""
Master Dashboard Runner
Lighthouse Macro - January 2026

Generates all dashboards with appropriate scheduling:
- Liquidity Stress Dashboard: Daily
- Labor Health Monitor: Weekly (Thursdays)
- Consumer Solvency Tracker: Monthly
- Treasury Demand Gauge: Auction-day
"""

import sys
from datetime import datetime
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lighthouse_data.dashboards.liquidity_dashboard import generate_liquidity_dashboard, print_liquidity_summary
from lighthouse_data.dashboards.labor_dashboard import generate_labor_dashboard, print_labor_summary
from lighthouse_data.dashboards.consumer_dashboard import generate_consumer_dashboard, print_consumer_summary
from lighthouse_data.dashboards.treasury_dashboard import generate_treasury_dashboard, print_treasury_summary
from lighthouse_data.utils.logging import get_logger

log = get_logger(__name__)


def run_daily_dashboards():
    """Run dashboards that update daily."""
    log.info("=" * 60)
    log.info("RUNNING DAILY DASHBOARDS")
    log.info("=" * 60)

    results = {}

    # Liquidity Dashboard (Daily)
    log.info("\n--- Liquidity Stress Dashboard ---")
    try:
        print_liquidity_summary()
        fig = generate_liquidity_dashboard(save=True)
        results['Liquidity'] = 'Success' if fig else 'No Data'
        if fig:
            import matplotlib.pyplot as plt
            plt.close(fig)
    except Exception as e:
        log.error(f"Liquidity dashboard failed: {e}")
        results['Liquidity'] = f'Error: {e}'

    # Treasury Dashboard (can run daily, most relevant on auction days)
    log.info("\n--- Treasury Demand Gauge ---")
    try:
        print_treasury_summary()
        fig = generate_treasury_dashboard(save=True)
        results['Treasury'] = 'Success' if fig else 'No Data'
        if fig:
            import matplotlib.pyplot as plt
            plt.close(fig)
    except Exception as e:
        log.error(f"Treasury dashboard failed: {e}")
        results['Treasury'] = f'Error: {e}'

    return results


def run_weekly_dashboards():
    """Run dashboards that update weekly."""
    log.info("=" * 60)
    log.info("RUNNING WEEKLY DASHBOARDS")
    log.info("=" * 60)

    results = {}

    # Labor Dashboard (Weekly - Thursdays after claims)
    log.info("\n--- Labor Health Monitor ---")
    try:
        print_labor_summary()
        fig = generate_labor_dashboard(save=True)
        results['Labor'] = 'Success' if fig else 'No Data'
        if fig:
            import matplotlib.pyplot as plt
            plt.close(fig)
    except Exception as e:
        log.error(f"Labor dashboard failed: {e}")
        results['Labor'] = f'Error: {e}'

    return results


def run_monthly_dashboards():
    """Run dashboards that update monthly."""
    log.info("=" * 60)
    log.info("RUNNING MONTHLY DASHBOARDS")
    log.info("=" * 60)

    results = {}

    # Consumer Dashboard (Monthly)
    log.info("\n--- Consumer Solvency Tracker ---")
    try:
        print_consumer_summary()
        fig = generate_consumer_dashboard(save=True)
        results['Consumer'] = 'Success' if fig else 'No Data'
        if fig:
            import matplotlib.pyplot as plt
            plt.close(fig)
    except Exception as e:
        log.error(f"Consumer dashboard failed: {e}")
        results['Consumer'] = f'Error: {e}'

    return results


def run_all_dashboards():
    """Run all dashboards regardless of schedule."""
    log.info("=" * 60)
    log.info("RUNNING ALL DASHBOARDS")
    log.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info("=" * 60)

    all_results = {}

    # Daily
    daily = run_daily_dashboards()
    all_results.update(daily)

    # Weekly
    weekly = run_weekly_dashboards()
    all_results.update(weekly)

    # Monthly
    monthly = run_monthly_dashboards()
    all_results.update(monthly)

    # Summary
    log.info("\n" + "=" * 60)
    log.info("DASHBOARD GENERATION COMPLETE")
    log.info("=" * 60)
    for name, status in all_results.items():
        log.info(f"  {name:15} : {status}")

    return all_results


def smart_run():
    """
    Smart runner that determines which dashboards to run based on day of week and date.

    - Daily: Liquidity, Treasury (every business day)
    - Weekly: Labor (Thursdays)
    - Monthly: Consumer (1st business day of month)
    """
    today = datetime.now()
    day_of_week = today.weekday()  # 0=Monday, 6=Sunday
    day_of_month = today.day

    results = {}

    # Skip weekends
    if day_of_week >= 5:
        log.info("Weekend - skipping dashboard generation")
        return results

    # Always run daily dashboards on business days
    log.info("Running daily dashboards...")
    daily = run_daily_dashboards()
    results.update(daily)

    # Run weekly on Thursdays (after claims release)
    if day_of_week == 3:  # Thursday
        log.info("Thursday - running weekly dashboards...")
        weekly = run_weekly_dashboards()
        results.update(weekly)

    # Run monthly on 1st-3rd of month (catch first business day)
    if day_of_month <= 3:
        log.info("Beginning of month - running monthly dashboards...")
        monthly = run_monthly_dashboards()
        results.update(monthly)

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Lighthouse Macro Dashboard Runner')
    parser.add_argument('--all', action='store_true', help='Run all dashboards')
    parser.add_argument('--daily', action='store_true', help='Run daily dashboards only')
    parser.add_argument('--weekly', action='store_true', help='Run weekly dashboards only')
    parser.add_argument('--monthly', action='store_true', help='Run monthly dashboards only')
    parser.add_argument('--smart', action='store_true', help='Smart run based on schedule')

    args = parser.parse_args()

    if args.all:
        run_all_dashboards()
    elif args.daily:
        run_daily_dashboards()
    elif args.weekly:
        run_weekly_dashboards()
    elif args.monthly:
        run_monthly_dashboards()
    elif args.smart:
        smart_run()
    else:
        # Default to all
        run_all_dashboards()
