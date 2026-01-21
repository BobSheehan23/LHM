# %%
"""
Macroeconomic Stress Composite Analysis
---------------------------------------

This script mirrors the exploratory and modeling pipeline for analyzing
macroeconomic stress data. It is structured with ``# %%`` cell markers so it
can be opened in editors that support notebook-style execution.
"""

# %%
# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
import ipywidgets as widgets
from IPython.display import display
from datetime import datetime
from pathlib import Path
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy.stats import zscore

pd.set_option("display.max_columns", None)
sns.set(style="whitegrid")

# %%
# Load datasets
path = Path(".")  # Adjust path if needed

df_composite = pd.read_csv(path / "lighthouse_macro_stress_composite.csv", parse_dates=["date"])
df_alerts = pd.read_csv(path / "macro_stress_alerts.csv", parse_dates=["date"])
df_beacons = pd.read_csv(path / "lighthouse_beacon_master.csv")

with open(path / "macro_86b36.txt") as f:
    macro_codes = [code.strip() for code in f.read().split(",") if code.strip()]

# %%
# Data cleaning and merging
df_composite.columns = df_composite.columns.str.lower()
df_alerts.columns = df_alerts.columns.str.lower()
df_beacons.columns = df_beacons.columns.str.lower()

df_merged = pd.merge(df_composite, df_alerts, on="date", how="outer")

if "series_id" in df_composite.columns and "series_id" in df_beacons.columns:
    df_composite = df_composite.merge(df_beacons, on="series_id", how="left")

# %%
# Exploratory Data Analysis
plt.figure(figsize=(12, 6))
plt.plot(df_composite["date"], df_composite["composite_score"])
plt.title("Composite Score Over Time")
plt.xlabel("Date")
plt.ylabel("Score")
plt.tight_layout()
plt.show()

# %%
alerts_ts = df_alerts.set_index("date").resample("M").sum(numeric_only=True)
alerts_ts.plot(kind="bar", stacked=True, figsize=(14, 6))
plt.title("Monthly Aggregated Alerts")
plt.tight_layout()
plt.show()

# %%
plt.figure(figsize=(14, 10))
sns.heatmap(df_composite.select_dtypes(include=np.number).corr(), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation Matrix")
plt.tight_layout()
plt.show()

# %%
# PCA and clustering
macro_features = (
    df_composite.select_dtypes(include=np.number)
    .drop(columns=["composite_score"], errors="ignore")
    .dropna(axis=1)
)
X_scaled = StandardScaler().fit_transform(macro_features)

pca = PCA(n_components=2)
pca_result = pca.fit_transform(X_scaled)

df_pca = pd.DataFrame(pca_result, columns=["PC1", "PC2"])
df_pca["date"] = df_composite["date"]

fig = px.scatter(df_pca, x="PC1", y="PC2", color=df_composite["composite_score"], title="PCA on Macro Features")
fig.show()

# %%
kmeans = KMeans(n_clusters=3, random_state=42)
df_composite["cluster"] = kmeans.fit_predict(X_scaled)
df_pca["cluster"] = df_composite["cluster"]

fig = px.scatter(df_pca, x="PC1", y="PC2", color="cluster", title="KMeans Clustering")
fig.show()

# %%
# Summary statistics
macro_numeric = df_composite.select_dtypes(include=np.number)
summary_stats = macro_numeric.describe().T
summary_stats["missing_pct"] = df_composite.isnull().mean() * 100
summary_stats["volatility"] = macro_numeric.std()
summary_stats["skew"] = macro_numeric.skew()
summary_stats["kurtosis"] = macro_numeric.kurtosis()
top_stats = summary_stats.sort_values(by="volatility", ascending=False).head(10)
top_stats

# %%
# Interactive explorer
dropdown = widgets.Dropdown(
    options=macro_numeric.columns,
    description="Macro Series:",
    layout={"width": "400px"},
)


def plot_series(series_name):
    fig = px.line(df_composite, x="date", y=series_name, title=f"{series_name} Over Time")
    fig.show()


widgets.interact(plot_series, series_name=dropdown)
