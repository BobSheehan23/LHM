#!/usr/bin/env python3
"""
LIGHTHOUSE MACRO - MULTI-DESTINATION SYNC
==========================================
Syncs database backups, strategy docs, and code to all backup destinations.
Called automatically after daily pipeline run, or standalone.

Destinations:
    1. LOCAL  - Dated database backups (7-day rolling)
    2. GITHUB - Auto-commit and push code, strategy, brand, logs
    3. ICLOUD - Database backup copy
    4. GDRIVE - Database backup + Strategy + Brand
    5. DROPBOX - Database backup copy

Usage:
    python sync_all.py              # Full sync to all destinations
    python sync_all.py --git-only   # Only git commit + push
    python sync_all.py --cloud-only # Only cloud sync (no git)
    python sync_all.py --dry-run    # Show what would happen
"""

import os
import sys
import shutil
import subprocess
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# === PATHS ===
LHM_ROOT = Path("/Users/bob/LHM")
DB_SOURCE = LHM_ROOT / "Data" / "databases" / "Lighthouse_Master.db"
BACKUP_DIR = LHM_ROOT / "Data" / "databases" / "backups"
LOGS_DIR = LHM_ROOT / "logs"

# Cloud destinations
ICLOUD_DIR = Path.home() / "Library" / "CloudStorage" / "iCloudDrive-iCloudDrive" / "LHM_Backups"
GDRIVE_DIR = Path.home() / "Library" / "CloudStorage" / "GDrive-bob@lighthousemacro.com" / "My Drive" / "LHM_Backups"
DROPBOX_DIR = Path.home() / "Dropbox" / "LHM_Backups"

# Cloud retention (days)
CLOUD_RETENTION_DAYS = 30
LOCAL_RETENTION_DAYS = 7


def log(msg):
    """Print with timestamp."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def git_sync(dry_run=False):
    """Auto-commit changed files and push to GitHub."""
    log("GIT SYNC: Starting...")

    os.chdir(LHM_ROOT)

    # Check if there are any changes
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True, cwd=str(LHM_ROOT)
    )

    if not result.stdout.strip():
        log("GIT SYNC: No changes to commit.")
        return True

    # Stage specific directories (not everything)
    stage_paths = [
        "Strategy/",
        "Brand/",
        "Scripts/",
        "lighthouse_quant/",
        "logs/",
        ".gitignore",
    ]

    if dry_run:
        log(f"GIT SYNC [DRY RUN]: Would stage: {', '.join(stage_paths)}")
        log("GIT SYNC [DRY RUN]: Would commit and push to origin/main")
        return True

    for path in stage_paths:
        full = LHM_ROOT / path
        if full.exists():
            subprocess.run(
                ["git", "add", path],
                cwd=str(LHM_ROOT), capture_output=True
            )

    # Check if anything is staged
    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=str(LHM_ROOT)
    )

    if result.returncode == 0:
        log("GIT SYNC: Nothing staged to commit.")
        return True

    # Commit
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    commit_msg = f"Daily pipeline sync {date_str}"

    result = subprocess.run(
        ["git", "commit", "-m", commit_msg],
        capture_output=True, text=True, cwd=str(LHM_ROOT)
    )

    if result.returncode != 0:
        log(f"GIT SYNC: Commit failed: {result.stderr}")
        return False

    log(f"GIT SYNC: Committed: {commit_msg}")

    # Push
    result = subprocess.run(
        ["git", "push", "origin", "main"],
        capture_output=True, text=True, cwd=str(LHM_ROOT),
        timeout=120
    )

    if result.returncode != 0:
        log(f"GIT SYNC: Push failed: {result.stderr}")
        return False

    log("GIT SYNC: Pushed to origin/main.")
    return True


def cloud_sync(dry_run=False):
    """Copy database backup and key folders to cloud destinations."""
    log("CLOUD SYNC: Starting...")

    date_str = datetime.now().strftime("%Y%m%d")
    backup_name = f"Lighthouse_Master_{date_str}.db"

    if not DB_SOURCE.exists():
        log(f"CLOUD SYNC: Database not found at {DB_SOURCE}")
        return False

    destinations = {
        "iCloud": ICLOUD_DIR,
        "GDrive": GDRIVE_DIR,
        "Dropbox": DROPBOX_DIR,
    }

    success = True

    for name, dest_dir in destinations.items():
        try:
            # Check if cloud storage mount exists
            if not dest_dir.parent.exists():
                log(f"CLOUD SYNC [{name}]: Mount point not found, skipping.")
                continue

            if dry_run:
                log(f"CLOUD SYNC [{name}] [DRY RUN]: Would copy {backup_name} to {dest_dir}")
                continue

            dest_dir.mkdir(parents=True, exist_ok=True)

            # Copy dated database backup
            dest_file = dest_dir / backup_name
            if not dest_file.exists():
                shutil.copy2(DB_SOURCE, dest_file)
                log(f"CLOUD SYNC [{name}]: Copied {backup_name}")
            else:
                log(f"CLOUD SYNC [{name}]: {backup_name} already exists, skipping.")

            # For GDrive, also sync Strategy and Brand folders
            if name == "GDrive":
                gdrive_lhm = dest_dir.parent / "LHM"
                gdrive_lhm.mkdir(parents=True, exist_ok=True)

                for folder in ["Strategy", "Brand"]:
                    src = LHM_ROOT / folder
                    dst = gdrive_lhm / folder
                    if src.exists():
                        # Use rsync for efficient folder sync
                        result = subprocess.run(
                            ["rsync", "-a", "--delete",
                             str(src) + "/", str(dst) + "/"],
                            capture_output=True, text=True
                        )
                        if result.returncode == 0:
                            log(f"CLOUD SYNC [{name}]: Synced {folder}/")
                        else:
                            log(f"CLOUD SYNC [{name}]: rsync {folder} failed: {result.stderr}")

            # Clean up old backups
            cleanup_cloud_backups(dest_dir, name)

        except Exception as e:
            log(f"CLOUD SYNC [{name}]: Error: {e}")
            success = False

    return success


def cleanup_cloud_backups(dest_dir, name):
    """Remove cloud backups older than retention period."""
    try:
        cutoff = datetime.now().timestamp() - (CLOUD_RETENTION_DAYS * 24 * 60 * 60)
        removed = 0
        for f in dest_dir.glob("Lighthouse_Master_*.db"):
            if f.stat().st_mtime < cutoff:
                f.unlink()
                removed += 1
        if removed:
            log(f"CLOUD SYNC [{name}]: Removed {removed} old backup(s) (>{CLOUD_RETENTION_DAYS} days)")
    except Exception as e:
        log(f"CLOUD SYNC [{name}]: Cleanup error: {e}")


def sync_to_all_destinations(dry_run=False):
    """Run full sync to all destinations."""
    log("=" * 60)
    log("LIGHTHOUSE MACRO - MULTI-DESTINATION SYNC")
    log("=" * 60)

    results = {}

    # 1. Git sync
    try:
        results["GitHub"] = git_sync(dry_run=dry_run)
    except Exception as e:
        log(f"GIT SYNC: Exception: {e}")
        results["GitHub"] = False

    # 2. Cloud sync
    try:
        results["Cloud"] = cloud_sync(dry_run=dry_run)
    except Exception as e:
        log(f"CLOUD SYNC: Exception: {e}")
        results["Cloud"] = False

    # Summary
    log("-" * 40)
    log("SYNC SUMMARY:")
    for dest, ok in results.items():
        status = "OK" if ok else "FAILED"
        log(f"  {dest}: {status}")
    log("=" * 60)

    return all(results.values())


def main():
    parser = argparse.ArgumentParser(description="Lighthouse Macro Multi-Destination Sync")
    parser.add_argument("--git-only", action="store_true", help="Only git commit + push")
    parser.add_argument("--cloud-only", action="store_true", help="Only cloud sync")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")

    args = parser.parse_args()

    if args.git_only:
        git_sync(dry_run=args.dry_run)
    elif args.cloud_only:
        cloud_sync(dry_run=args.dry_run)
    else:
        sync_to_all_destinations(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
