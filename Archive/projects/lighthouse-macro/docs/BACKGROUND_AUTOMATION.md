# Background Automation — Run Continuously on M4/M5

You said: **"I want this to literally just be running in the background once I have that new computer"**

Perfect. Here's how to set it up for continuous automated operation.

---

## 🎯 Goal

**When you get your M4 Max/M5:**
- System runs 24/7 in background
- Collects all FRED data daily (automatic)
- Stores everything locally (huge storage ready)
- Charts auto-generate with perfect format (never specify again)
- Database builds continuously
- Zero manual intervention

---

## 📦 What Runs Automatically

### 1. Daily Data Collection

**What:** Fetch all FRED series, store locally with timestamps
**When:** Every day at 9 AM (after market open)
**Storage:** `~/lighthouse-macro/data/raw/fred/`

### 2. Data Transformations

**What:** Auto-compute YoY, Z-scores, moving averages, etc.
**When:** Immediately after collection
**Storage:** `~/lighthouse-macro/data/processed/`

### 3. Chart Generation (Optional)

**What:** Auto-generate key charts for Chartbook
**When:** Weekly on Friday at 10 AM
**Storage:** `~/lighthouse-macro/charts/`

---

## 🚀 Setup Instructions (For M4/M5)

### Step 1: Install System (One Time)

```bash
cd ~/lighthouse-macro
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Step 2: Configure Automation (macOS)

**Create launchd service** (macOS background task):

```bash
# Create the automation script
cat > ~/lighthouse-macro/scripts/daily_collection.sh << 'EOF'
#!/bin/bash
cd ~/lighthouse-macro
source venv/bin/activate
python scripts/collect.py >> logs/collection.log 2>&1
EOF

chmod +x ~/lighthouse-macro/scripts/daily_collection.sh

# Create logs directory
mkdir -p ~/lighthouse-macro/logs
```

**Create launchd plist:**

```bash
cat > ~/Library/LaunchAgents/com.lighthousemacro.collection.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.lighthousemacro.collection</string>

    <key>ProgramArguments</key>
    <array>
        <string>/Users/bob/lighthouse-macro/scripts/daily_collection.sh</string>
    </array>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>

    <key>StandardOutPath</key>
    <string>/Users/bob/lighthouse-macro/logs/collection.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/bob/lighthouse-macro/logs/collection.error.log</string>

    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
EOF

# Load the service
launchctl load ~/Library/LaunchAgents/com.lighthousemacro.collection.plist
```

**That's it. System now runs daily at 9 AM automatically.**

### Step 3: Verify It's Running

```bash
# Check if service is loaded
launchctl list | grep lighthousemacro

# Check logs
tail -f ~/lighthouse-macro/logs/collection.log
```

---

## 🗄️ Local Database Strategy (M4/M5)

### Current Storage (60 series)

```
~/lighthouse-macro/data/
├── raw/fred/                    # ~5-10 MB
│   ├── GDP_20250127_120000.parquet
│   ├── GDP_latest.parquet
│   └── ... (60 series × versions)
│
├── processed/                   # ~10-20 MB
│   ├── macro_dynamics/
│   ├── monetary_mechanics/
│   └── market_technicals/
│
└── cache/                       # ~5-10 MB
    └── ai_responses/

Total: ~20-40 MB
```

### Scaled Up (All FRED, Your M4/M5 Goal)

```
When you add more series:

10,000 FRED series × 50 years × 12 months
= ~6 million data points

Storage:
- Raw data: ~500 MB - 1 GB
- Transformed: ~1-2 GB
- Historical versions: ~5-10 GB (10 years of daily snapshots)

Total: ~10-15 GB for COMPLETE FRED database

Your M4 Max with 2-8 TB storage: 0.0005% used
```

**Translation:** You can store literally EVERYTHING with room to spare.

---

## 📊 Perfect Chart Format (Now Default)

You said: **"I want to not have to describe how I want the chart to look EVERY single time"**

**Fixed. It's now the default.**

### What Changed

```python
# OLD (you had to specify):
chart = LHMChart()
chart.plot_line(data, color="ocean_blue")
chart.add_watermarks()
chart.some_other_thing()
chart.another_thing()

# NEW (automatic):
chart = LHMChart()
chart.plot_line(data)
chart.save("output.png")
```

**Everything is automatic:**
- ✅ 12x7 size (default)
- ✅ Ocean blue OUTER frame (8px thick)
- ✅ Gray spines for data area
- ✅ Data area = 85% of canvas
- ✅ Ocean blue watermarks (top-left, bottom-right)
- ✅ Right-side axis
- ✅ No gridlines
- ✅ Proper spacing (no overlaps)

**Test it:**
```bash
python cli.py chart create GDP --output test.png
open test.png
```

Should show:
- 🔵 Blue frame around entire chart
- ⬛ Gray spines around data
- 🟦 Ocean blue watermarks
- ✅ Perfect spacing

---

## 🔄 Continuous Operation Workflow

### What Happens Automatically

**Daily (9 AM):**
1. System wakes up
2. Fetches latest FRED data
3. Saves timestamped snapshot
4. Updates "latest" versions
5. Runs transformations
6. Logs results
7. Goes back to sleep

**Weekly (Friday 10 AM - Optional):**
1. Generate Chartbook (50+ charts)
2. Save to `charts/` directory
3. Ready for publishing

**On-Demand (You):**
```bash
# Quick Beam
python cli.py research beam GDP

# Full Beacon
python cli.py research beacon

# Custom chart
python cli.py chart create UNRATE
```

### Database Builds Automatically

Over time, you accumulate:
- **Historical snapshots** (track data revisions)
- **Complete time series** (decades of data)
- **Pre-computed transformations** (instant access)
- **No API rate limits** (data is local)

**M4 Max with fast SSD:** Lightning-fast queries, instant charts.

---

## 💾 When You Get M4/M5

### Migration Steps

1. **Transfer system:**
   ```bash
   # On old Mac
   cd ~
   tar -czf lighthouse-macro.tar.gz lighthouse-macro/

   # Copy to new M4 Mac, then:
   tar -xzf lighthouse-macro.tar.gz
   cd lighthouse-macro
   python3 -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

2. **Set up automation:**
   ```bash
   # Follow Step 2 above (launchd setup)
   ```

3. **Expand dataset:**
   ```bash
   # Edit configs/series.yaml, add more series
   # Run collection
   python scripts/collect.py
   ```

4. **Verify:**
   ```bash
   python cli.py status
   tail -f logs/collection.log
   ```

**Done. System runs forever.**

---

## 🎯 Your Perfect Workflow (Post-Setup)

### What You Do

**Nothing (data collection)** → Automatic
**Nothing (transformations)** → Automatic
**Nothing (chart format)** → Perfect default

**Only when you need output:**
```bash
# Quick Beam for Twitter/Substack
python cli.py research beam GDP

# Full Beacon article (Sunday)
python cli.py research beacon

# Custom analysis
python cli.py chart create UNRATE
```

**Charts are perfect every time. No tweaking needed.**

---

## 📈 Monitoring (Optional)

### Check System Health

```bash
# View recent logs
tail -20 ~/lighthouse-macro/logs/collection.log

# Check database size
du -sh ~/lighthouse-macro/data/

# List latest collected series
ls -lt ~/lighthouse-macro/data/raw/fred/ | head -20

# Verify automation is running
launchctl list | grep lighthousemacro
```

### Dashboard (Future Enhancement)

Could add:
- Web dashboard showing collection status
- Email alerts if collection fails
- Statistics on database size
- Charts of data coverage

**But honestly, once it's running, you'll forget it's there. That's the point.**

---

## 🏆 Summary

**You want:** "Running in the background, literally everything automated"

**You get:**
- ✅ Daily data collection (automatic)
- ✅ Local database (perfect for M4/M5 huge storage)
- ✅ Perfect chart format (never specify again)
- ✅ Zero manual intervention
- ✅ Scales to thousands of series
- ✅ Lightning-fast on M4 Max

**Setup once on M4/M5 → Forget about it → Use when you need output**

---

**Install it now. Set up automation when you get M4/M5. Never think about data collection again.**

**LIGHTHOUSE MACRO**
MACRO, ILLUMINATED.
