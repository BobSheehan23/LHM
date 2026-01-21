#!/usr/bin/env python3
"""
Lighthouse Macro — Data Collection Script
Automated data collection from all sources
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.collectors import FREDCollector
from src.core import get_config


def collect_all_fred(start_date: str = None):
    """Collect all FRED series across all pillars"""
    config = get_config()
    collector = FREDCollector()

    print("=" * 60)
    print("LIGHTHOUSE MACRO — DATA COLLECTION")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    for pillar in ["macro_dynamics", "monetary_mechanics", "market_technicals"]:
        print(f"\n📊 Collecting {pillar.replace('_', ' ').title()}...")
        print("-" * 60)

        results = collector.fetch_by_pillar(pillar, start_date=start_date)

        success = sum(1 for v in results.values() if v is not None)
        failed = len(results) - success

        print(f"\n✓ Success: {success}")
        if failed > 0:
            print(f"✗ Failed: {failed}")

    print("\n" + "=" * 60)
    print(f"Collection complete: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Collect macro data")
    parser.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
    parser.add_argument(
        "--pillar",
        choices=["macro_dynamics", "monetary_mechanics", "market_technicals"],
        help="Collect specific pillar only",
    )

    args = parser.parse_args()

    if args.pillar:
        collector = FREDCollector()
        collector.fetch_by_pillar(args.pillar, start_date=args.start_date)
    else:
        collect_all_fred(start_date=args.start_date)
