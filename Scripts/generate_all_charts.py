#!/usr/bin/env python3
"""
LIGHTHOUSE MACRO — MASTER CHART GENERATION SCRIPT
THE HORIZON | JANUARY 2026

This script runs all chart generation pipelines in sequence.
Individual scripts are preserved and can still be run independently.

Usage:
    python generate_all_charts.py           # Run all pipelines
    python generate_all_charts.py --core    # Only core 20 charts
    python generate_all_charts.py --premium # Only premium charts
    python generate_all_charts.py --real    # Only real-data charts
"""

import subprocess
import sys
import os
import time
from datetime import datetime

# Script locations (relative to this file)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHART_GEN_DIR = os.path.join(SCRIPT_DIR, 'chart_generation')

SCRIPTS = {
    'core': {
        'name': 'Core Horizon Charts (20 charts)',
        'path': os.path.join(CHART_GEN_DIR, 'generate_horizon_charts.py'),
        'description': 'Main narrative charts: labor, consumer, plumbing, markets'
    },
    'premium': {
        'name': 'Premium Charts (~8 charts)',
        'path': os.path.join(CHART_GEN_DIR, 'generate_premium_charts.py'),
        'description': 'Advanced visualizations: waterfalls, heatmaps, annotated'
    },
    'real': {
        'name': 'Real Data Charts (~35 charts)',
        'path': os.path.join(CHART_GEN_DIR, 'generate_charts_real.py'),
        'description': 'Live API data charts: Fed, Treasury, labor'
    },
    'full': {
        'name': 'Full Chart Set (~35 charts)',
        'path': os.path.join(CHART_GEN_DIR, 'generate_charts.py'),
        'description': 'Complete institutional chart set'
    }
}


def run_script(script_key, verbose=True):
    """Run a single chart generation script."""
    script = SCRIPTS.get(script_key)
    if not script:
        print(f"Unknown script: {script_key}")
        return False

    if not os.path.exists(script['path']):
        print(f"Script not found: {script['path']}")
        return False

    if verbose:
        print(f"\n{'='*60}")
        print(f"Running: {script['name']}")
        print(f"  {script['description']}")
        print(f"{'='*60}\n")

    start = time.time()

    try:
        # Run the script
        result = subprocess.run(
            [sys.executable, script['path']],
            cwd=CHART_GEN_DIR,
            capture_output=not verbose,
            text=True
        )

        elapsed = time.time() - start

        if result.returncode == 0:
            if verbose:
                print(f"\n✓ {script['name']} completed in {elapsed:.1f}s")
            return True
        else:
            print(f"\n✗ {script['name']} failed (exit code {result.returncode})")
            if not verbose and result.stderr:
                print(f"  Error: {result.stderr[:200]}")
            return False

    except Exception as e:
        print(f"\n✗ {script['name']} error: {e}")
        return False


def main():
    """Main entry point."""
    print("="*60)
    print("LIGHTHOUSE MACRO — CHART GENERATION PIPELINE")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    # Parse arguments
    args = sys.argv[1:]

    if '--core' in args:
        scripts_to_run = ['core']
    elif '--premium' in args:
        scripts_to_run = ['premium']
    elif '--real' in args:
        scripts_to_run = ['real']
    elif '--full' in args:
        scripts_to_run = ['full']
    else:
        # Run all scripts
        scripts_to_run = ['core', 'premium', 'real', 'full']

    # Track results
    results = {}
    total_start = time.time()

    for script_key in scripts_to_run:
        results[script_key] = run_script(script_key)

    # Summary
    total_elapsed = time.time() - total_start
    success = sum(1 for v in results.values() if v)

    print("\n" + "="*60)
    print("GENERATION COMPLETE")
    print("="*60)
    print(f"Scripts run: {len(results)}")
    print(f"Successful:  {success}")
    print(f"Failed:      {len(results) - success}")
    print(f"Total time:  {total_elapsed:.1f}s")
    print("="*60)

    for key, succeeded in results.items():
        status = "✓" if succeeded else "✗"
        print(f"  {status} {SCRIPTS[key]['name']}")

    print(f"\nOutput: /Users/bob/Desktop/HORIZON_FINAL./output/charts/")
    print("="*60)

    return 0 if all(results.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
