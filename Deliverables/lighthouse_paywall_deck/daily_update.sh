#!/bin/bash
################################################################################
# LIGHTHOUSE MACRO - DAILY AUTOMATION SCRIPT
# Automatically updates all data, indicators, and charts daily
#
# Author: Bob Sheehan, CFA, CMT
# Date: November 2025
#
# Usage: Run this script daily (via cron or manually)
#   ./daily_update.sh
#
# Or schedule with cron (runs every weekday at 6 AM):
#   0 6 * * 1-5 cd /Users/bob/lighthouse_paywall_deck && ./daily_update.sh
################################################################################

# Set working directory
cd /Users/bob/lighthouse_paywall_deck

# Activate virtual environment
source venv/bin/activate

# Create log file with timestamp
LOGFILE="logs/daily_update_$(date +%Y%m%d_%H%M%S).log"
mkdir -p logs

echo "=========================================" | tee -a $LOGFILE
echo "LIGHTHOUSE MACRO - DAILY UPDATE" | tee -a $LOGFILE
echo "Started: $(date)" | tee -a $LOGFILE
echo "=========================================" | tee -a $LOGFILE

# Step 1: Update master dataset
echo "" | tee -a $LOGFILE
echo "[1/3] Updating master dataset..." | tee -a $LOGFILE
python gather_all_chartbook_data.py >> $LOGFILE 2>&1

if [ $? -eq 0 ]; then
    echo "✓ Master data updated successfully" | tee -a $LOGFILE
else
    echo "✗ ERROR: Master data update failed" | tee -a $LOGFILE
    exit 1
fi

# Step 2: Calculate proprietary indicators
echo "" | tee -a $LOGFILE
echo "[2/3] Calculating proprietary indicators..." | tee -a $LOGFILE
python calculate_proprietary_indicators.py >> $LOGFILE 2>&1

if [ $? -eq 0 ]; then
    echo "✓ Proprietary indicators calculated" | tee -a $LOGFILE
else
    echo "✗ ERROR: Indicator calculation failed" | tee -a $LOGFILE
    exit 1
fi

# Step 3: Generate all charts
echo "" | tee -a $LOGFILE
echo "[3/3] Generating all proprietary charts..." | tee -a $LOGFILE
python generate_all_proprietary_charts.py >> $LOGFILE 2>&1

if [ $? -eq 0 ]; then
    echo "✓ All charts generated" | tee -a $LOGFILE
else
    echo "✗ ERROR: Chart generation failed" | tee -a $LOGFILE
    exit 1
fi

# Summary
echo "" | tee -a $LOGFILE
echo "=========================================" | tee -a $LOGFILE
echo "DAILY UPDATE COMPLETE" | tee -a $LOGFILE
echo "Finished: $(date)" | tee -a $LOGFILE
echo "=========================================" | tee -a $LOGFILE

# Count generated files
CHART_COUNT=$(ls -1 charts/proprietary/*.png 2>/dev/null | wc -l)
echo "Charts available: $CHART_COUNT" | tee -a $LOGFILE

# Display latest MRI value
echo "" | tee -a $LOGFILE
echo "Latest Macro Risk Index (MRI):" | tee -a $LOGFILE
tail -1 proprietary_indicators.csv | awk -F',' '{print "  Date: " $1 "\n  MRI: " $2 "σ"}' | tee -a $LOGFILE

echo "" | tee -a $LOGFILE
echo "✓ All proprietary metrics updated and ready for chartbook!" | tee -a $LOGFILE
echo "Log saved to: $LOGFILE" | tee -a $LOGFILE

# Optional: Send notification (uncomment if you want email alerts)
# echo "Daily update complete. MRI: $(tail -1 proprietary_indicators.csv | awk -F',' '{print $2}')" | \
#   mail -s "Lighthouse Macro Daily Update" bob@lighthousemacro.com

exit 0
