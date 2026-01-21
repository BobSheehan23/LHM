"""Generate Lighthouse Macro labor market charts from FRED and BLS data."""
from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List

import certifi
import matplotlib.pyplot as plt
import pandas as pd
import requests
from fredapi import Fred

# Ensure TLS trust for API calls (macOS Python sometimes lacks cert bundle)
CERT_PATH = certifi.where()
os.environ.setdefault("REQUESTS_CA_BUNDLE", CERT_PATH)
os.environ.setdefault("SSL_CERT_FILE", CERT_PATH)

BLS_API_KEY = os.getenv("BLS_API_KEY", "e83e702d7e244961951cf9026d1ae437")
FRED_API_KEY = os.getenv("FRED_API_KEY", "6dcc7a0d790cdcc28c1f751420ee9d27")


# Output directories
ROOT = Path(__file__).resolve().parent
CHART_DIR = ROOT / "charts"
DATA_DIR = ROOT / "data"
CHART_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Lighthouse Macro house palette
COLORS = {
    "ocean_blue": "#1f77b4",
    "deep_sunset_orange": "#ff7f0e",
    "neon_carolina_blue": "#2ca02c",
    "neon_magenta": "#d62728",
    "medium_gray": "#7f7f7f",
}

HOUSE_WATERMARK = "MACRO, ILLUMINATED."


def apply_house_style(
    ax: plt.Axes,
    source_text: str,
    *,
    add_footer: bool = True,
    primary_axis: str = "right",
) -> None:
    """Apply Lighthouse Macro chart styling to a Matplotlib axis."""

    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("black")

    ax.tick_params(axis="both", colors="black")

    if primary_axis == "right":
        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()
    else:
        ax.yaxis.set_label_position("left")
        ax.yaxis.tick_left()

    if add_footer:
        fig = ax.get_figure()
        fig.text(
            0.01,
            0.015,
            source_text,
            ha="left",
            va="bottom",
            fontsize=9,
            color=COLORS["medium_gray"],
        )
        fig.text(
            0.99,
            0.015,
            HOUSE_WATERMARK,
            ha="right",
            va="bottom",
            fontsize=9,
            color=COLORS["medium_gray"],
            weight="bold",
        )


def save_chart(fig: plt.Figure, filename: str) -> Path:
    """Save figure to charts directory with consistent formatting."""
    output_path = CHART_DIR / filename
    fig.tight_layout(rect=(0, 0.05, 1, 0.98))
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {output_path.name}")
    return output_path


def get_fred_series(series_ids: Iterable[str]) -> pd.DataFrame:
    """Pull one or more FRED series and return as a DataFrame."""
    fred = Fred(api_key=FRED_API_KEY)
    frames: List[pd.Series] = []
    for sid in series_ids:
        sid = sid.strip()
        try:
            print(f"Fetching FRED series {sid}")
            data = fred.get_series(sid)
        except ValueError:
            data = fred.get_series(sid)
        if data is None or data.empty:
            raise ValueError(f"No data returned for FRED series '{sid}'")
        series = data.to_frame(name=sid)
        frames.append(series)
    df = pd.concat(frames, axis=1).sort_index()
    df.index = pd.PeriodIndex(df.index, freq="M").to_timestamp()
    csv_path = DATA_DIR / f"fred_{'-'.join(series_ids)}.csv"
    df.to_csv(csv_path)
    return df


def fetch_bls_series(series_ids: Iterable[str], start_year: int = 2000) -> pd.DataFrame:
    """Retrieve one or more series from the BLS public API."""
    series_ids = list(series_ids)
    payload = {
        "seriesid": series_ids,
        "startyear": str(start_year),
        "endyear": str(datetime.now().year),
        "registrationkey": BLS_API_KEY,
        "catalog": True,
    }
    response = requests.post(
        "https://api.bls.gov/publicAPI/v2/timeseries/data/",
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    if data.get("status") != "REQUEST_SUCCEEDED":
        raise RuntimeError(f"BLS API error: {data.get('message')}")

    records: List[Dict] = []
    meta: Dict[str, Dict] = {}
    for item in data["Results"]["series"]:
        sid = item["seriesID"]
        meta[sid] = item.get("catalog", {})
        for obs in item["data"]:
            period = obs["period"]
            if not period.startswith("M"):
                continue
            month = int(period[1:])
            row = {
                "date": pd.Timestamp(year=int(obs["year"]), month=month, day=1),
                "series_id": sid,
                "value": float(obs["value"]),
            }
            records.append(row)

    df = pd.DataFrame(records)
    if df.empty:
        raise ValueError(f"No BLS data returned for {series_ids}")
    df = df.pivot(index="date", columns="series_id", values="value").sort_index()
    csv_path = DATA_DIR / f"bls_{'-'.join(series_ids)}.csv"
    df.to_csv(csv_path)
    return df


def list_bls_surveys(save_path: Path | None = DATA_DIR / "bls_surveys.csv") -> pd.DataFrame:
    """Retrieve the catalog of available BLS surveys and optionally persist to CSV."""
    params = {"registrationkey": BLS_API_KEY} if BLS_API_KEY else None
    response = requests.get(
        "https://api.bls.gov/publicAPI/v2/surveys",
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("status") != "REQUEST_SUCCEEDED":
        raise RuntimeError(f"BLS API error: {payload.get('message')}")

    surveys = payload.get("Results", {}).get("survey", [])
    if not surveys:
        raise ValueError("No BLS surveys returned by the API")

    df = pd.DataFrame(surveys)
    df.sort_values("survey_abbreviation", inplace=True, ignore_index=True)

    if save_path:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(save_path, index=False)

    return df


def chart_1_openings_to_unemployed() -> Path:
    df = get_fred_series(["JTSJOL", "UNEMPLOY"])
    df = df.dropna()
    df["ratio"] = df["JTSJOL"] / df["UNEMPLOY"]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        df.index,
        df["ratio"],
        color=COLORS["ocean_blue"],
        linewidth=3.0,
    )
    ax.axhline(
        1.0,
        color=COLORS["medium_gray"],
        linestyle="--",
        linewidth=1.5,
        alpha=0.7,
    )
    ax.set_title(
        "Job Openings-to-Unemployed Ratio Falls Below 1",
        fontsize=16,
        weight="bold",
        pad=12,
    )
    ax.set_ylabel("Ratio")
    ax.set_xlabel("")
    apply_house_style(ax, "Source: Lighthouse Macro, FRED")
    return save_chart(fig, "chart1_openings_to_unemployed.png")


def chart_2_quits_hires() -> Path:
    df = get_fred_series(["JTSQUR", "JTSHIR"])
    df = df.dropna()

    fig, ax_right = plt.subplots(figsize=(10, 6))
    line_quits, = ax_right.plot(
        df.index,
        df["JTSQUR"],
        label="Quits Rate",
        color=COLORS["ocean_blue"],
        linewidth=3.0,
    )
    ax_right.set_ylabel("Quits Rate (% of employment)")
    ax_right.set_xlabel("")
    apply_house_style(ax_right, "Source: Lighthouse Macro, FRED")

    ax_left = ax_right.twinx()
    line_hires, = ax_left.plot(
        df.index,
        df["JTSHIR"],
        label="Hires Rate",
        color=COLORS["deep_sunset_orange"],
        linewidth=3.0,
    )
    ax_left.set_ylabel("Hires Rate (% of employment)")
    apply_house_style(
        ax_left,
        "Source: Lighthouse Macro, FRED",
        add_footer=False,
        primary_axis="left",
    )

    fig.suptitle(
        "Quits and Hires Revert Toward Pre-Pandemic Norms",
        fontsize=16,
        weight="bold",
        y=0.96,
    )
    handles = [line_quits, line_hires]
    labels = [h.get_label() for h in handles]
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False, fontsize=11)
    return save_chart(fig, "chart2_quits_hires.png")


def chart_3_u6_vs_u3() -> Path:
    df = get_fred_series(["UNRATE", "U6RATE"])
    df = df.dropna()

    fig, ax_right = plt.subplots(figsize=(10, 6))
    line_u3, = ax_right.plot(
        df.index,
        df["UNRATE"],
        label="U-3",
        color=COLORS["medium_gray"],
        linewidth=3.0,
    )
    ax_right.set_ylabel("U-3 Unemployment Rate (%)")
    ax_right.set_xlabel("")
    apply_house_style(ax_right, "Source: Lighthouse Macro, FRED")

    ax_left = ax_right.twinx()
    line_u6, = ax_left.plot(
        df.index,
        df["U6RATE"],
        label="U-6",
        color=COLORS["deep_sunset_orange"],
        linewidth=3.0,
    )
    ax_left.set_ylabel("U-6 Underemployment Rate (%)")
    apply_house_style(
        ax_left,
        "Source: Lighthouse Macro, FRED",
        add_footer=False,
        primary_axis="left",
    )

    fig.suptitle(
        "Underemployment Gap Widens: U-6 vs. U-3",
        fontsize=16,
        weight="bold",
        y=0.96,
    )
    handles = [line_u3, line_u6]
    labels = [h.get_label() for h in handles]
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False, fontsize=11)
    return save_chart(fig, "chart3_u6_vs_u3.png")


def chart_4_lfpr_epop() -> Path:
    df = get_fred_series(["CIVPART", "LNS12300060"])
    df = df.dropna()

    fig, ax_right = plt.subplots(figsize=(10, 6))
    line_lfpr, = ax_right.plot(
        df.index,
        df["CIVPART"],
        label="Labor Force Participation Rate",
        color=COLORS["ocean_blue"],
        linewidth=3.0,
    )
    ax_right.set_ylabel("Labor Force Participation Rate (%)")
    ax_right.set_xlabel("")
    apply_house_style(ax_right, "Source: Lighthouse Macro, FRED")

    ax_left = ax_right.twinx()
    line_epop, = ax_left.plot(
        df.index,
        df["LNS12300060"],
        label="Prime-Age EPOP",
        color=COLORS["deep_sunset_orange"],
        linewidth=3.0,
    )
    ax_left.set_ylabel("Prime-Age Employment-Population Ratio (%)")
    apply_house_style(
        ax_left,
        "Source: Lighthouse Macro, FRED",
        add_footer=False,
        primary_axis="left",
    )

    fig.suptitle(
        "Prime-Age EPOP Recovers, But Labor Force Participation Stalls",
        fontsize=16,
        weight="bold",
        y=0.96,
    )
    handles = [line_lfpr, line_epop]
    labels = [h.get_label() for h in handles]
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False, fontsize=11)
    return save_chart(fig, "chart4_lfpr_epop.png")


def chart_5_unemployment_by_education() -> Path:
    series = {
        "< HS": "LNS14027659",
        "HS, no college": "LNS14027660",
        "Some college/AA": "LNS14027689",
        "Bachelor+": "LNS14027662",
    }
    df = get_fred_series(series.values())
    df.rename(columns={v: k for k, v in series.items()}, inplace=True)
    latest = df.tail(120)  # last 10 years for readability

    color_map = {
        "< HS": COLORS["neon_magenta"],
        "HS, no college": COLORS["deep_sunset_orange"],
        "Some college/AA": COLORS["neon_carolina_blue"],
        "Bachelor+": COLORS["ocean_blue"],
    }

    fig, ax = plt.subplots(figsize=(10, 6))
    for column in latest.columns:
        ax.plot(
            latest.index,
            latest[column],
            label=column,
            linewidth=3.0,
            color=color_map[column],
        )
    ax.set_title(
        "White-Collar Weakness: Higher Unemployment Among Degree Holders",
        fontsize=16,
        weight="bold",
        pad=12,
    )
    ax.set_ylabel("Unemployment Rate (%)")
    ax.set_xlabel("")
    ax.legend(loc="upper left", frameon=False)
    apply_house_style(ax, "Source: Lighthouse Macro, FRED")
    return save_chart(fig, "chart5_unemployment_by_education.png")


def chart_6_long_term_share() -> Path:
    df = get_fred_series(["LNS13025703", "UNEMPLOY"])
    df.dropna(inplace=True)
    df["Long-term share"] = 100 * df["LNS13025703"] / df["UNEMPLOY"]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        df.index,
        df["Long-term share"],
        color=COLORS["neon_carolina_blue"],
        linewidth=3.0,
    )
    ax.set_title(
        "Long-Term Unemployment Share Hits 25.7%",
        fontsize=16,
        weight="bold",
        pad=12,
    )
    ax.set_ylabel("Percent of total unemployed")
    ax.set_xlabel("")
    apply_house_style(ax, "Source: Lighthouse Macro, FRED")
    return save_chart(fig, "chart6_long_term_share.png")


def chart_7_real_wages() -> Path:
    df = get_fred_series(["CES0500000003", "CPIAUCSL"])
    df.dropna(inplace=True)
    df["Real Average Hourly Earnings"] = df["CES0500000003"] / df["CPIAUCSL"]
    base = df.loc[df.index >= pd.Timestamp("2018-01-01")].copy()
    base["Real Earnings Index"] = base["Real Average Hourly Earnings"] / base["Real Average Hourly Earnings"].iloc[0] * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        base.index,
        base["Real Earnings Index"],
        color=COLORS["ocean_blue"],
        linewidth=3.0,
    )
    ax.set_title(
        "Real Wages Recover Slightly, But Remain Fragile",
        fontsize=16,
        weight="bold",
        pad=12,
    )
    ax.set_ylabel("Index (2018=100)")
    ax.set_xlabel("")
    apply_house_style(ax, "Source: Lighthouse Macro, FRED")
    return save_chart(fig, "chart7_real_wages.png")


def chart_8_unemployment_duration() -> Path:
    df = fetch_bls_series(["LNU03008275"], start_year=2000)
    df.rename(columns={"LNU03008275": "Average Weeks"}, inplace=True)
    df.dropna(inplace=True)
    df["Trend"] = df["Average Weeks"].rolling(6, min_periods=1).mean()

    fig, ax_right = plt.subplots(figsize=(10, 6))
    line_monthly, = ax_right.plot(
        df.index,
        df["Average Weeks"],
        label="Monthly",
        color=COLORS["neon_carolina_blue"],
        linewidth=3.0,
        alpha=0.65,
    )
    ax_right.set_ylabel("Monthly Average Weeks Unemployed")
    ax_right.set_xlabel("")
    apply_house_style(ax_right, "Source: Lighthouse Macro, BLS")

    ax_left = ax_right.twinx()
    line_trend, = ax_left.plot(
        df.index,
        df["Trend"],
        label="6-Month Avg",
        color=COLORS["ocean_blue"],
        linewidth=3.0,
    )
    ax_left.set_ylabel("6-Month Average Weeks Unemployed")
    apply_house_style(
        ax_left,
        "Source: Lighthouse Macro, BLS",
        add_footer=False,
        primary_axis="left",
    )

    fig.suptitle(
        "Rising Unemployment Duration Elevates Inflation Risk",
        fontsize=16,
        weight="bold",
        y=0.96,
    )
    handles = [line_monthly, line_trend]
    labels = [h.get_label() for h in handles]
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False, fontsize=11)
    return save_chart(fig, "chart8_unemployment_duration.png")


def chart_9_matching_efficiency() -> Path:
    df = get_fred_series(["JTSHIL", "JTSJOL"])
    df.dropna(inplace=True)
    df["Hires/Openings"] = df["JTSHIL"] / df["JTSJOL"]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        df.index,
        df["Hires/Openings"],
        color=COLORS["neon_magenta"],
        linewidth=3.0,
    )
    ax.set_title(
        "Most Job Vacancies Still Target the Employed",
        fontsize=16,
        weight="bold",
        pad=12,
    )
    ax.set_ylabel("Hires per Opening")
    ax.set_xlabel("")
    apply_house_style(ax, "Source: Lighthouse Macro, FRED")
    return save_chart(fig, "chart9_matching_efficiency.png")


def chart_10_duration_disparities() -> Path:
    series_map = {
        "16-19": "LNU03008279",
        "20-24": "LNU03008287",
        "25-34": "LNU03008289",
        "35-44": "LNU03008293",
        "45-54": "LNU03008297",
        "55-64": "LNU03008301",
        "65+": "LNU03008305",
    }
    df = fetch_bls_series(series_map.values(), start_year=2010)
    df = df.sort_index()
    latest_month = df.index.max()
    latest_values = df.loc[latest_month].rename(index={v: k for k, v in series_map.items()})

    fig, ax = plt.subplots(figsize=(10, 6))
    latest_values.sort_values().plot(
        kind="barh",
        color=COLORS["deep_sunset_orange"],
        ax=ax,
        edgecolor="black",
    )
    ax.set_title(
        "Scarring Is Uneven: Duration by Age Cohort",
        fontsize=16,
        weight="bold",
        pad=12,
    )
    ax.set_xlabel("Average Weeks Unemployed (NSA)")
    ax.set_ylabel("")
    ax.set_xlim(0, max(30, latest_values.max() + 2))
    apply_house_style(
        ax,
        "Source: Lighthouse Macro, BLS",
        primary_axis="left",
    )
    return save_chart(fig, "chart10_duration_disparities.png")


CHART_BUILDERS = [
    chart_1_openings_to_unemployed,
    chart_2_quits_hires,
    chart_3_u6_vs_u3,
    chart_4_lfpr_epop,
    chart_5_unemployment_by_education,
    chart_6_long_term_share,
    chart_7_real_wages,
    chart_8_unemployment_duration,
    chart_9_matching_efficiency,
    chart_10_duration_disparities,
]


def main() -> None:
    results: List[Path] = []
    for builder in CHART_BUILDERS:
        try:
            path = builder()
            results.append(path)
        except Exception as exc:
            print(f"Error generating {builder.__name__}: {exc}", file=sys.stderr)
            raise
    print("All charts generated:")
    for path in results:
        print(f" - {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
