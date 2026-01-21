
# labor_charts.py
# Lighthouse Macro — Labor Market Recalibration Charts
# Outputs: PNG charts + snapshot CSV for Substack/Chartbook
# Requires: fredapi, requests, pandas, numpy, matplotlib, pillow (PIL)
# Style: uses /mnt/data/lhm.mplstyle or /mnt/data/lhm_style.mplstyle if found

import os
import json
import time
from datetime import datetime
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from PIL import Image

# ---------------------------
# Config
# ---------------------------
FRED_API_KEY = os.getenv("FRED_API_KEY", "6dcc7a0d790cdcc28c1f751420ee9d27")
BLS_API_KEY = os.getenv("BLS_API_KEY", "e83e702d7e244961951cf9026d1ae437")

# Output dirs
RUN_DATE = datetime.today().strftime("%Y-%m-%d")
OUT_DIR = os.path.join(os.getcwd(), f"charts_{RUN_DATE}")
os.makedirs(OUT_DIR, exist_ok=True)

SNAPSHOT_CSV = os.path.join(OUT_DIR, "dashboard_snapshot.csv")
CAPTION_CSV = os.path.join(OUT_DIR, "captions.csv")

# Watermark
WATERMARK_PATHS = [
    "/mnt/data/lhm_watermark.png",
    "/mnt/data/lhm_watermark_darkblue.png"
]

# mpl style
MPL_STYLE_CANDIDATES = [
    "/mnt/data/lhm.mplstyle",
    "/mnt/data/lhm_style.mplstyle"
]

for style_path in MPL_STYLE_CANDIDATES:
    if os.path.exists(style_path):
        plt.style.use(style_path)
        break

# ---------------------------
# Helpers
# ---------------------------

def add_watermark(ax, alpha=0.12, scale=0.25, pad=10):
    fig = ax.get_figure()
    for wm in WATERMARK_PATHS:
        if os.path.exists(wm):
            try:
                img = Image.open(wm).convert("RGBA")
                fig.canvas.draw()
                w, h = fig.get_size_inches() * fig.dpi
                target_w = int(w * scale)
                ratio = img.size[1] / img.size[0]
                target_h = int(target_w * ratio)
                img = img.resize((target_w, target_h), resample=Image.LANCZOS)
                fig.figimage(img, xo=int(w - target_w - pad), yo=int(pad), alpha=alpha, zorder=10)
                return
            except Exception:
                pass

def ann_growth(series, months):
    factor = 12 / months
    return (series / series.shift(months)) ** factor - 1

def yoy(series):
    return series.pct_change(12)

def zscore(series, window=36):
    return (series - series.rolling(window).mean()) / series.rolling(window).std()

def save_chart(fig, filename, caption=None, last_vals=None):
    path = os.path.join(OUT_DIR, filename)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    cap = caption or ""
    lv = last_vals or {}
    row = {"file": filename, "caption": cap}
    for k, v in lv.items():
        row[k] = v
    captions.append(row)

def fred_series(series_id, observation_start="2000-01-01"):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "series_id": series_id,
        "observation_start": observation_start
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()["observations"]
    df = pd.DataFrame(data)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date")[["value"]].rename(columns={"value": series_id})
    return df

def bls_series(series_ids, start_year=2000, end_year=None):
    if end_year is None:
        end_year = datetime.today().year
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    headers = {"Content-type": "application/json"}
    payload = {
        "seriesid": series_ids,
        "startyear": str(start_year),
        "endyear": str(end_year),
        "registrationkey": BLS_API_KEY
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers, timeout=60)
    r.raise_for_status()
    j = r.json()
    frames = []
    for s in j.get("Results", {}).get("series", []):
        sid = s["seriesID"]
        obs = s["data"]
        df = pd.DataFrame(obs)
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df = df[df["period"].str.startswith("M")].copy()
        df["month"] = df["period"].str[1:].astype(int)
        df["date"] = pd.to_datetime(df["year"].astype(int)*10000 + df["month"]*100 + 1, format="%Y%m%d")
        df = df.set_index("date")[["value"]].sort_index().rename(columns={"value": sid})
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    out = pd.concat(frames, axis=1).sort_index()
    return out

# ---------------------------
# Data Pulls
# ---------------------------

captions = []
snapshots = []

fred_ids = [
    "LNS11300060",   # LFPR
    "LNS12300060",   # Prime-age EPOP
    "JTSJOL",        # Job Openings (level)
    "UNRATE",        # Unemployment Rate
    "JTS100QUR",     # Quits Rate
    "JTS100HIR",     # Hires Rate
    "CPILFESL"       # Core CPI (proxy)
]

dfs = []
for sid in fred_ids:
    try:
        dfs.append(fred_series(sid, "2000-01-01"))
        time.sleep(0.2)
    except Exception as e:
        print(f"FRED fetch failed for {sid}: {e}")

data = pd.concat(dfs, axis=1)

# ---------------------------
# Transforms
# ---------------------------
def add_transforms(df, col, is_rate=False):
    out = pd.DataFrame(index=df.index)
    out[f"{col}_level"] = df[col]
    if not is_rate:
        out[f"{col}_3m_ann"] = ann_growth(df[col], 3)
        out[f"{col}_6m_ann"] = ann_growth(df[col], 6)
    out[f"{col}_yoy"] = yoy(df[col])
    out[f"{col}_z36"] = zscore(df[col], 36)
    return out

rate_like = {"LNS11300060", "LNS12300060", "UNRATE", "JTS100QUR", "JTS100HIR"}

panel = pd.DataFrame(index=data.index)
for c in data.columns:
    panel = panel.join(add_transforms(data, c, is_rate=(c in rate_like)), how="outer")

# ---------------------------
# Plotters
# ---------------------------

def format_pct(ax):
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:.1f}%"))

def chart_lfpr(df):
    col = "LNS11300060"
    subset = df[[f"{col}_level"]].dropna()
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(subset.index, subset[f"{col}_level"], linewidth=3, label="LFPR (level)")
    format_pct(ax)
    ax.set_title("Labor Force Participation Rate (Level)")
    ax.set_xlabel("")
    ax.set_ylabel("Percent")
    ax.spines["top"].set_visible(True); ax.spines["right"].set_visible(True); ax.spines["bottom"].set_visible(True); ax.spines["left"].set_visible(True)
    add_watermark(ax)
    last = subset[f"{col}_level"].dropna().iloc[-1]
    save_chart(fig, f"{RUN_DATE}__LABOR__LFPR__level__{last:.2f}.png",
               caption="Labor supply lens: LFPR level. Slower hiring can reflect supply constraints rather than weak demand.",
               last_vals={"LFPR_last_pct": f"{last:.2f}"})

def chart_prime_age_epop(df):
    col = "LNS12300060"
    subset = df[[f"{col}_level"]].dropna()
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(subset.index, subset[f"{col}_level"], linewidth=3, label="Prime-age EPOP (level)")
    format_pct(ax)
    ax.set_title("Prime-age Employment-Population Ratio (25–54)")
    ax.set_xlabel("")
    ax.set_ylabel("Percent")
    add_watermark(ax)
    last = subset[f"{col}_level"].dropna().iloc[-1]
    save_chart(fig, f"{RUN_DATE}__LABOR__EPOP_25_54__level__{last:.2f}.png",
               caption="Prime-age EPOP anchors the labor cycle; watch inflections for macro regime shifts.",
               last_vals={"EPOP_25_54_last_pct": f"{last:.2f}"})

def chart_openings_vs_unemployed(df):
    opens = df["JTSJOL_level"].dropna()
    u = df["UNRATE_level"].dropna()
    common = opens.index.intersection(u.index)
    opens, u = opens.loc[common], u.loc[common]
    fig, ax1 = plt.subplots(figsize=(10,6))
    ax1.plot(opens.index, opens, linewidth=3, label="Job Openings (level)")
    ax1.set_ylabel("Millions")
    ax2 = ax1.twinx()
    ax2.plot(u.index, u, linewidth=3, linestyle="--", label="Unemployment Rate")
    format_pct(ax2)
    ax1.set_title("Job Openings vs Unemployment Rate")
    ax1.set_xlabel("")
    add_watermark(ax1)
    last_open = opens.iloc[-1]
    last_unrate = u.iloc[-1]
    save_chart(fig, f"{RUN_DATE}__LABOR__Openings_vs_Unrate__{last_open:.2f}_{last_unrate:.2f}.png",
               caption="Openings remain elevated relative to unemployment; the speed of change matters more than levels.",
               last_vals={"Openings_last": f"{last_open:.2f}", "UNRATE_last_pct": f"{last_unrate:.2f}"})

def chart_quits_hires(df):
    q = df.get("JTS100QUR_level")
    h = df.get("JTS100HIR_level")
    fig, ax = plt.subplots(figsize=(10,6))
    if q is not None:
        ax.plot(q.index, q, linewidth=3, label="Quits Rate")
    if h is not None:
        ax.plot(h.index, h, linewidth=3, linestyle="--", label="Hires Rate")
    format_pct(ax)
    ax.set_title("Quits & Hires (Rates)")
    ax.set_xlabel("")
    ax.set_ylabel("Percent")
    ax.legend(frameon=False)
    add_watermark(ax)
    last_q = q.dropna().iloc[-1] if q is not None else np.nan
    last_h = h.dropna().iloc[-1] if h is not None else np.nan
    save_chart(fig, f"{RUN_DATE}__LABOR__Quits_Hires__{last_q:.2f}_{last_h:.2f}.png",
               caption="Reduced labor-market fluidity shows up as lower quits and slower hires.",
               last_vals={"Quits_last_pct": f"{last_q:.2f}", "Hires_last_pct": f"{last_h:.2f}"})

def chart_eci_vs_core(df):
    core = df.get("CPILFESL_level")
    if core is None or core.dropna().empty:
        return
    core_3m = ann_growth(core, 3)
    core_6m = ann_growth(core, 6)
    fig, ax1 = plt.subplots(figsize=(10,6))
    ax1.plot(core_3m.index, core_3m*100, linewidth=3, label="Core CPI 3m ann (%, SA)")
    ax1.plot(core_6m.index, core_6m*100, linewidth=3, linestyle="--", label="Core CPI 6m ann (%, SA)")
    ax1.set_ylabel("% annualized")
    ax1.set_title("Inflation Pulse: Core CPI (3m/6m annualized)")
    ax1.set_xlabel("")
    ax1.legend(frameon=False)
    add_watermark(ax1)
    last3 = core_3m.dropna().iloc[-1]*100
    last6 = core_6m.dropna().iloc[-1]*100
    save_chart(fig, f"{RUN_DATE}__PRICES__CoreCPI__3m6m_ann__{last3:.2f}_{last6:.2f}.png",
               caption="Inflation composition matters; 3m/6m ann highlight turning points faster than YoY.",
               last_vals={"CoreCPI_3m_ann_pct": f"{last3:.2f}", "CoreCPI_6m_ann_pct": f"{last6:.2f}"})

# ---------------------------
# Run all charts
# ---------------------------
chart_lfpr(panel)
chart_prime_age_epop(panel)
chart_openings_vs_unemployed(panel)
chart_quits_hires(panel)
chart_eci_vs_core(panel)

pd.DataFrame(captions).to_csv(CAPTION_CSV, index=False)

# Snapshot rows: last + transforms where available
snapshot_rows = []
keys = [
    "LNS11300060_level",
    "LNS12300060_level",
    "JTSJOL_level",
    "UNRATE_level",
    "JTS100QUR_level",
    "JTS100HIR_level",
    "CPILFESL_level",
]
for k in keys:
    if k in panel.columns:
        s = panel[k]
        if s.dropna().empty:
            continue
        last = s.dropna().iloc[-1]
        row = {"series": k, "last": last}
        base = k.replace("_level","")
        for suffix in ["_3m_ann","_6m_ann","_z36","_yoy"]:
            col = base + suffix
            if col in panel.columns and not panel[col].dropna().empty:
                row[col] = panel[col].dropna().iloc[-1]
        snapshot_rows.append(row)

if snapshot_rows:
    pd.DataFrame(snapshot_rows).to_csv(SNAPSHOT_CSV, index=False)

print(f"Done. Charts & CSVs in: {OUT_DIR}")
