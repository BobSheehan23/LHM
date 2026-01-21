#!/usr/bin/env python3
"""
Generate Lighthouse Macro dashboard charts and exports for The Beacon | Oct 2025.

Outputs:
    - charts/*.png  (18 charts)
    - exports/macro_dashboard_data.csv
    - exports/macro_dashboard_charts.pdf
"""

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
OCEAN_BLUE = "0089D1"
DEEP_ORANGE = "#FF6B35"
NEON_CAROLINA_BLUE = "#00C5FF"
NEON_MAGENTA = "#FF00FF"
MED_LIGHT_GRAY = "#999999"
FRED_API_KEY = "6dcc7a0d790cdcc28c1f751420ee9d27"

CHART_SIZE = (12, 6.75)
DATA_START = "1990-01-01"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def fred_api(series_id: str, api_key: str) -> pd.Series:
    """Fetch a FRED series and return a monthly pandas Series."""
    url = (
        "https://api.stlouisfed.org/fred/series/observations"
        f"?series_id={series_id}&api_key={api_key}&file_type=json"
        f"&observation_start={DATA_START}"
    )
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()

    payload = resp.json()
    observations = payload.get("observations", [])
    dates = pd.to_datetime([obs["date"] for obs in observations])
    values = [
        float(obs["value"]) if obs.get("value") not in ("", ".") else np.nan
        for obs in observations
    ]

    return (
        pd.Series(values, index=dates, name=series_id)
        .astype(float)
        .resample("ME")
        .mean()
    )


def zscore(series: pd.Series) -> pd.Series:
    """Standard z-score with NaN handling."""
    std = series.std()
    if std == 0 or np.isnan(std):
        return pd.Series(np.nan, index=series.index)
    return (series - series.mean()) / std


def percentile(series: pd.Series) -> pd.Series:
    """Percentile rank across full history."""
    return series.rank(pct=True)


def style_axes(ax: plt.Axes, title: str) -> None:
    """Apply Lighthouse Macro styling to the axis."""
    ax.set_title(title, loc="left", fontsize=14, fontweight="bold", color=f"#{OCEAN_BLUE}")
    fig = ax.get_figure()
    fig.text(0.01, 0.98, "LIGHTHOUSE MACRO", fontsize=10, color=f"#{OCEAN_BLUE}", alpha=0.7)
    fig.text(0.99, 0.02, "MACRO, ILLUMINATED.", fontsize=8, color=MED_LIGHT_GRAY, alpha=0.7, ha="right")
    ax.spines["top"].set_visible(True)
    ax.spines["right"].set_visible(True)
    for spine in ax.spines.values():
        spine.set_linewidth(1)
        spine.set_color(f"#{OCEAN_BLUE}")
    ax.grid(False)


def save_chart(fig: plt.Figure, filename: str) -> None:
    """Persist chart to the charts directory."""
    charts_dir = Path("charts")
    charts_dir.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(charts_dir / filename, dpi=200)
    plt.close(fig)


def plot_dual(
    data: pd.DataFrame,
    labels: Iterable[str],
    ylabels: Iterable[str],
    title: str,
    fname: str,
) -> None:
    """Dual-axis line chart."""
    fig, ax = plt.subplots(figsize=CHART_SIZE)
    ax.plot(data.index, data.iloc[:, 0], color=f"#{OCEAN_BLUE}", lw=2.5, label=labels[0])
    ax.set_ylabel(list(ylabels)[0], color=f"#{OCEAN_BLUE}")
    ax.tick_params(axis="y", labelcolor=f"#{OCEAN_BLUE}")

    ax2 = ax.twinx()
    ax2.plot(data.index, data.iloc[:, 1], color=DEEP_ORANGE, lw=2.5, label=labels[1])
    ax2.set_ylabel(list(ylabels)[1], color=DEEP_ORANGE)
    ax2.tick_params(axis="y", labelcolor=DEEP_ORANGE)

    lines1, labs1 = ax.get_legend_handles_labels()
    lines2, labs2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labs1 + labs2, loc="upper left", fontsize=8)

    style_axes(ax, title)
    save_chart(fig, fname)


def plot_single(
    df: pd.DataFrame,
    labels: Iterable[str],
    ylabel: str,
    title: str,
    fname: str,
) -> None:
    """Single-axis multi-line chart."""
    fig, ax = plt.subplots(figsize=CHART_SIZE)
    palette = [f"#{OCEAN_BLUE}", DEEP_ORANGE, NEON_CAROLINA_BLUE, NEON_MAGENTA]

    for idx, col in enumerate(df.columns):
        ax.plot(df.index, df[col], color=palette[idx % len(palette)], lw=2.5, label=list(labels)[idx])

    ax.set_ylabel(ylabel)
    ax.legend(loc="upper left")
    style_axes(ax, title)
    save_chart(fig, fname)


def build_series() -> dict[str, pd.Series]:
    """Download required FRED series."""
    series_map = {
        "PAYEMS": "payems",
        "JTSQUR": "jtsqur",
        "JTSHIR": "jtshir",
        "JTSLDL": "jtsldl",
        "AWHMAN": "awhman",
        "UEMP27OV": "uemp27",
        "UNRATE": "unrate",
        "BAMLH0A0HYM2": "hy_oas",
        "BAMLC0A0CM": "bbb_oas",
        "DGS10": "dgs10",
        "DGS2": "dgs2",
        "SOFR": "sofr",
        "EFFR": "effr",
        "RRPONTSYD": "rrp",
        "RESBALNS": "res",
        "GDP": "gdp",
        "SP500": "sp500_daily",
    }

    return {alias: fred_api(series_id, FRED_API_KEY) for series_id, alias in series_map.items()}


def generate_outputs() -> None:
    """Main generation routine for charts and exports."""
    data = build_series()

    payroll_yoy = data["payems"].pct_change(12) * 100
    quits_z = zscore(data["jtsqur"])

    frag_index = pd.concat(
        [
            -zscore(data["jtsqur"]),
            zscore(data["uemp27"]),
            -zscore(data["awhman"]),
            -zscore(data["jtshir"]),
        ],
        axis=1,
    ).mean(axis=1)

    dyn_index = pd.concat(
        [
            zscore(data["jtsqur"]),
            zscore(data["jtshir"]),
            -zscore(data["uemp27"]),
        ],
        axis=1,
    ).mean(axis=1)

    lagged_frag = frag_index.shift(6)
    credit_labor_gap_raw = (data["hy_oas"] - lagged_frag).dropna()
    credit_labor_gap = zscore(credit_labor_gap_raw)

    funding_gap = (data["sofr"] - data["effr"]).dropna()
    liquidity_share = (data["rrp"] / (data["rrp"] + data["res"])).dropna()
    funding_stress = zscore(funding_gap) + zscore(liquidity_share)

    transition_tracker = (
        0.4 * frag_index + 0.35 * credit_labor_gap + 0.25 * zscore(funding_stress)
    ).dropna()

    ma50 = data["sp500_daily"].rolling(50).mean()
    ma200 = data["sp500_daily"].rolling(200).mean()

    spread_diff = data["bbb_oas"] - data["hy_oas"]
    hy_vol = data["hy_oas"].pct_change().rolling(126).std()

    gdp_monthly = data["gdp"].resample("ME").ffill()
    rrp_gdp = (data["rrp"] / gdp_monthly) * 100
    res_gdp = (data["res"] / gdp_monthly) * 100

    yc = data["dgs10"] - data["dgs2"]
    funding = data["sofr"] - data["effr"]

    # Export CSV
    export_data = {
        "payroll_yoy": payroll_yoy,
        "quits_z": quits_z,
        "frag_index": frag_index,
        "dyn_index": dyn_index,
        "credit_labor_gap": credit_labor_gap_raw,
        "funding_stress": funding_stress,
        "transition_tracker": transition_tracker,
        "spx": data["sp500_daily"],
        "ma50": ma50,
        "ma200": ma200,
        "hy_oas": data["hy_oas"],
        "unrate": data["unrate"],
        "spread_diff": spread_diff,
        "hy_vol": hy_vol,
        "rrp_gdp": rrp_gdp,
        "res_gdp": res_gdp,
        "yc": yc,
        "funding": funding,
    }

    combined_df = pd.concat(export_data, axis=1)
    exports_dir = Path("exports")
    exports_dir.mkdir(exist_ok=True)
    combined_df.to_csv(exports_dir / "macro_dashboard_data.csv")

    # Chart data prep
    series1 = pd.concat([payroll_yoy, quits_z], axis=1).dropna()
    hours_norm = data["awhman"] / data["awhman"].loc["2019-01-31"] * 100
    payroll_norm = data["payems"] / data["payems"].loc["2019-01-31"] * 100
    hires_to_quits = (data["jtshir"] / data["jtsqur"]).dropna()
    quits_to_layoffs = (data["jtsqur"] / data["jtsldl"]).dropna()

    series7 = pd.concat([data["hy_oas"], lagged_frag], axis=1).dropna()
    series7.columns = ["HY_OAS", "Lagged_Frag"]

    heat_df = pd.concat(
        [
            percentile(frag_index),
            percentile(data["hy_oas"]),
            percentile(funding_gap),
            percentile(yc),
            percentile(data["jtsqur"]),
            percentile(liquidity_share),
        ],
        axis=1,
    ).dropna()
    heat_df.columns = [
        "LaborFrag",
        "HY_OAS",
        "Funding",
        "YieldCurve",
        "Quits",
        "RRPShare",
    ]

    series9 = pd.concat([data["hy_oas"], data["unrate"]], axis=1).dropna()
    series13 = pd.concat([yc, funding], axis=1).dropna()

    series17 = pd.concat([data["sp500_daily"], data["dgs10"]], axis=1).dropna()
    series18 = pd.concat([data["sp500_daily"], data["hy_oas"]], axis=1).dropna()

    # Chart generation
    plot_dual(
        series1,
        labels=["Payrolls YoY", "Quits (z)"],
        ylabels=["Percent", "z-score"],
        title="Headline vs Flow: Payrolls vs Quits",
        fname="chart01_payrolls_vs_quits.png",
    )

    plot_single(
        pd.DataFrame({"Hours": hours_norm, "Headcount": payroll_norm}).dropna(),
        labels=["Hours (AWHMAN)", "Headcount (PAYEMS)"],
        ylabel="Index (2019=100)",
        title="Under the Hood: Hours vs Headcount",
        fname="chart02_hours_vs_headcount.png",
    )

    plot_single(
        pd.DataFrame({"Hires/Quits": hires_to_quits}).dropna(),
        labels=["Hires/Quits"],
        ylabel="Ratio",
        title="Hires vs Quits Ratio",
        fname="chart03_hires_quits_ratio.png",
    )

    plot_single(
        pd.DataFrame({"Quits/Layoffs": quits_to_layoffs}).dropna(),
        labels=["Quits/Layoffs"],
        ylabel="Ratio",
        title="Quits vs Layoffs Ratio",
        fname="chart04_quits_layoffs_ratio.png",
    )

    plot_single(
        pd.DataFrame({"Labor Fragility": frag_index}).dropna(),
        labels=["Labor Fragility"],
        ylabel="z-score",
        title="Labor Fragility Index",
        fname="chart05_labor_fragility.png",
    )

    plot_single(
        pd.DataFrame({"Labor Dynamism": dyn_index}).dropna(),
        labels=["Labor Dynamism"],
        ylabel="z-score",
        title="Labor Dynamism Index (High = Dynamic)",
        fname="chart06_labor_dynamism.png",
    )

    plot_dual(
        series7,
        labels=["HY OAS", "Lagged Labor Fragility"],
        ylabels=["Percent", "z-score"],
        title="When Credit Notices Labor",
        fname="chart07_credit_vs_lagged_fragility.png",
    )

    fig, ax = plt.subplots(figsize=CHART_SIZE)
    sns.heatmap(heat_df.T, cmap="coolwarm", linewidths=0.5, ax=ax, cbar_kws={"label": "Percentile"})
    ax.set_title("Transition Heatmap (Percentile Rank)", loc="left", fontsize=14, fontweight="bold")
    ax.set_ylabel("")
    ax.set_xlabel("")
    fig.text(0.01, 0.98, "LIGHTHOUSE MACRO", fontsize=10, color=f"#{OCEAN_BLUE}", alpha=0.7)
    fig.text(0.99, 0.02, "MACRO, ILLUMINATED.", fontsize=8, color=MED_LIGHT_GRAY, alpha=0.7, ha="right")
    save_chart(fig, "chart08_transition_heatmap.png")

    plot_dual(
        series9,
        labels=["HY OAS", "Unemployment Rate"],
        ylabels=["Percent", "Percent"],
        title="HY Spread vs Unemployment",
        fname="chart09_hy_vs_unemployment.png",
    )

    plot_single(
        pd.DataFrame({"Spread Differential": spread_diff}).dropna(),
        labels=["Spread Differential (BBB - HY)"],
        ylabel="Percent",
        title="The BBB Cliff",
        fname="chart10_spread_differential.png",
    )

    plot_single(
        pd.DataFrame({"HY Volatility": hy_vol}).dropna(),
        labels=["HY Spread Volatility (6m)"],
        ylabel="Volatility",
        title="Credit Spread Volatility (6m)",
        fname="chart11_hy_volatility.png",
    )

    plot_single(
        pd.DataFrame({"RRP % GDP": rrp_gdp, "Reserves % GDP": res_gdp}).dropna(),
        labels=["RRP % GDP", "Reserves % GDP"],
        ylabel="Percent",
        title="RRP and Reserves vs GDP",
        fname="chart12_rrp_reserves_gdp.png",
    )

    plot_dual(
        series13,
        labels=["Yield Curve (10Y-2Y)", "SOFR - EFFR"],
        ylabels=["bp", "bp"],
        title="Yield Curve vs Funding Spread",
        fname="chart13_yield_curve_vs_funding.png",
    )

    plot_single(
        pd.DataFrame({"Funding Stress": funding_stress}).dropna(),
        labels=["Funding Stress"],
        ylabel="z-score",
        title="Funding Stress Index",
        fname="chart14_funding_stress.png",
    )

    plot_single(
        pd.DataFrame({"Transition Tracker": transition_tracker}).dropna(),
        labels=["Transition Tracker"],
        ylabel="Composite Index",
        title="Transition Tracker Composite",
        fname="chart15_transition_tracker.png",
    )

    plot_single(
        pd.DataFrame({"SPX": data["sp500_daily"], "MA50": ma50, "MA200": ma200}).dropna(),
        labels=["S&P 500", "50-day MA", "200-day MA"],
        ylabel="Index Level",
        title="S&P 500: 50 & 200-Day MAs",
        fname="chart16_spx_moving_averages.png",
    )

    plot_dual(
        series17,
        labels=["S&P 500", "10Y Yield"],
        ylabels=["Index", "Percent"],
        title="S&P 500 vs 10Y Yield",
        fname="chart17_spx_vs_10y.png",
    )

    plot_dual(
        series18,
        labels=["S&P 500", "HY OAS"],
        ylabels=["Index", "Percent"],
        title="S&P 500 vs HY OAS",
        fname="chart18_spx_vs_hy_oas.png",
    )

    # PDF export
    charts_dir = Path("charts")
    pdf_path = exports_dir / "macro_dashboard_charts.pdf"
    with PdfPages(pdf_path) as pdf:
        for chart_file in sorted(charts_dir.glob("*.png")):
            fig = plt.figure()
            img = plt.imread(chart_file)
            plt.imshow(img)
            plt.axis("off")
            pdf.savefig(fig)
            plt.close(fig)


def main() -> None:
    try:
        generate_outputs()
        print("Charts saved to ./charts and exports saved to ./exports")
    except requests.HTTPError as err:
        body = err.response.text if err.response is not None else ""
        print(f"FRED API error: {err}\n{body}")
    except Exception as exc:
        print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()
