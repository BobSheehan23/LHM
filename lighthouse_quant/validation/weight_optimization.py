"""
Composite Weight Optimization
=============================
Validates and optimizes weights for composite indices like LFI, LCI, MRI.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import warnings


@dataclass
class WeightOptimizationResult:
    """Results from weight optimization."""
    composite_name: str
    method: str
    original_weights: Dict[str, float]
    optimized_weights: Dict[str, float]
    original_r2: float
    optimized_r2: float
    improvement_pct: float
    feature_importance: Dict[str, float]
    n_observations: int
    cv_scores: Optional[List[float]] = None


def compute_zscore(series: pd.Series, window: int = 24) -> pd.Series:
    """Compute rolling z-score."""
    rolling_mean = series.rolling(window, min_periods=window//2).mean()
    rolling_std = series.rolling(window, min_periods=window//2).std()
    return (series - rolling_mean) / rolling_std


def optimize_weights_elastic_net(
    components: pd.DataFrame,
    target: pd.Series,
    l1_ratios: List[float] = [0.1, 0.5, 0.7, 0.9, 0.95, 1.0],
    cv_folds: int = 5,
    normalize_output: bool = True
) -> Tuple[Dict[str, float], float, List[float]]:
    """
    Optimize component weights using Elastic Net regression.

    Elastic Net combines L1 (Lasso) and L2 (Ridge) regularization:
    - L1 drives some weights to zero (feature selection)
    - L2 handles correlated features better

    Args:
        components: DataFrame with component series as columns
        target: Target variable to predict
        l1_ratios: List of L1/L2 mixing ratios to try
        cv_folds: Number of cross-validation folds
        normalize_output: Whether to normalize weights to sum to 1

    Returns:
        Tuple of (weights dict, best R2 score, CV scores)
    """
    try:
        from sklearn.linear_model import ElasticNetCV
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import TimeSeriesSplit
    except ImportError:
        warnings.warn("scikit-learn not installed")
        return {}, 0.0, []

    # Align data
    df = pd.concat([components, target.rename("target")], axis=1).dropna()
    if len(df) < 50:
        warnings.warn(f"Insufficient data: {len(df)} observations")
        return {}, 0.0, []

    X = df[components.columns].values
    y = df["target"].values

    # Remove infinite values
    mask = np.isfinite(X).all(axis=1) & np.isfinite(y)
    X = X[mask]
    y = y[mask]

    if len(X) < 50:
        warnings.warn(f"Insufficient finite data: {len(X)} observations")
        return {}, 0.0, []

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Time series cross-validation
    tscv = TimeSeriesSplit(n_splits=cv_folds)

    # Fit Elastic Net with CV
    model = ElasticNetCV(
        l1_ratio=l1_ratios,
        cv=tscv,
        max_iter=10000,
        random_state=42
    )
    model.fit(X_scaled, y)

    # Extract weights (need to unscale)
    raw_weights = model.coef_ / scaler.scale_

    # Create weights dict
    weights = dict(zip(components.columns, raw_weights))

    # Normalize if requested
    if normalize_output:
        total = sum(abs(v) for v in weights.values())
        if total > 0:
            weights = {k: v/total for k, v in weights.items()}

    # Compute R2
    y_pred = model.predict(X_scaled)
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - (ss_res / ss_tot)

    # Get CV scores
    cv_scores = list(model.mse_path_.mean(axis=1))

    return weights, r2, cv_scores


def optimize_weights_pca(
    components: pd.DataFrame,
    n_components: Optional[int] = None,
    variance_threshold: float = 0.95
) -> Tuple[Dict[str, float], float, np.ndarray]:
    """
    Analyze components using PCA to identify redundancy and importance.

    Args:
        components: DataFrame with component series
        n_components: Number of PCs to keep (None = use variance threshold)
        variance_threshold: Cumulative variance to retain

    Returns:
        Tuple of (importance weights, variance explained, loadings matrix)
    """
    try:
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler
    except ImportError:
        warnings.warn("scikit-learn not installed")
        return {}, 0.0, np.array([])

    # Clean data
    df = components.dropna()
    if len(df) < 50:
        warnings.warn(f"Insufficient data: {len(df)} observations")
        return {}, 0.0, np.array([])

    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df.values)

    # Fit PCA
    pca = PCA()
    pca.fit(X_scaled)

    # Determine number of components
    cumvar = np.cumsum(pca.explained_variance_ratio_)
    if n_components is None:
        n_components = np.argmax(cumvar >= variance_threshold) + 1

    # Compute importance as weighted average of absolute loadings
    # Weight by variance explained
    loadings = np.abs(pca.components_[:n_components])
    variances = pca.explained_variance_ratio_[:n_components]

    # Weighted importance per feature
    importance = np.zeros(len(components.columns))
    for i in range(n_components):
        importance += loadings[i] * variances[i]

    # Normalize to sum to 1
    importance = importance / importance.sum()

    weights = dict(zip(components.columns, importance))
    total_var = cumvar[n_components - 1]

    return weights, total_var, pca.components_


def analyze_component_importance(
    components: pd.DataFrame,
    target: pd.Series,
    methods: List[str] = ["elastic_net", "random_forest", "correlation"]
) -> pd.DataFrame:
    """
    Analyze component importance using multiple methods.

    Args:
        components: DataFrame with component series
        target: Target variable
        methods: List of methods to use

    Returns:
        DataFrame with importance scores per method
    """
    results = {col: {} for col in components.columns}

    # Align data and remove infinities
    df = pd.concat([components, target.rename("target")], axis=1).dropna()

    # Replace infinities
    df = df.replace([np.inf, -np.inf], np.nan).dropna()

    if len(df) < 50:
        warnings.warn(f"Insufficient data: {len(df)} observations")
        return pd.DataFrame()

    X = df[components.columns]
    y = df["target"]

    # Correlation-based importance
    if "correlation" in methods:
        for col in components.columns:
            corr = X[col].corr(y)
            results[col]["correlation"] = abs(corr)

    # Elastic Net
    if "elastic_net" in methods:
        weights, _, _ = optimize_weights_elastic_net(X, y)
        for col, w in weights.items():
            results[col]["elastic_net"] = abs(w)

    # Random Forest
    if "random_forest" in methods:
        try:
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.preprocessing import StandardScaler
            from sklearn.model_selection import TimeSeriesSplit

            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X.values)

            # Use time series split for validation
            tscv = TimeSeriesSplit(n_splits=3)

            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=5,
                random_state=42,
                n_jobs=-1
            )
            model.fit(X_scaled, y.values)

            for i, col in enumerate(components.columns):
                results[col]["random_forest"] = model.feature_importances_[i]

        except ImportError:
            warnings.warn("scikit-learn not installed for random forest")

    # Convert to DataFrame
    importance_df = pd.DataFrame(results).T
    importance_df.index.name = "component"

    # Normalize each method
    for col in importance_df.columns:
        total = importance_df[col].sum()
        if total > 0:
            importance_df[col] = importance_df[col] / total

    # Add average importance
    importance_df["average"] = importance_df.mean(axis=1)
    importance_df = importance_df.sort_values("average", ascending=False)

    return importance_df


def validate_composite_weights(
    composite_name: str,
    components: pd.DataFrame,
    target: pd.Series,
    original_weights: Dict[str, float]
) -> WeightOptimizationResult:
    """
    Validate existing composite weights against data-driven optimization.

    Args:
        composite_name: Name of composite index (e.g., "LFI")
        components: DataFrame with component z-scores
        target: Target variable to predict
        original_weights: Current weights in the composite

    Returns:
        WeightOptimizationResult with comparison
    """
    # Align data
    df = pd.concat([components, target.rename("target")], axis=1).dropna()
    n_obs = len(df)

    if n_obs < 50:
        return WeightOptimizationResult(
            composite_name=composite_name,
            method="elastic_net",
            original_weights=original_weights,
            optimized_weights={},
            original_r2=np.nan,
            optimized_r2=np.nan,
            improvement_pct=np.nan,
            feature_importance={},
            n_observations=n_obs
        )

    X = df[components.columns]
    y = df["target"]

    # Compute original composite value
    original_composite = pd.Series(0.0, index=X.index)
    for col, weight in original_weights.items():
        if col in X.columns:
            original_composite += weight * X[col].fillna(0)

    # Original R2
    ss_res_orig = np.sum((y - original_composite) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    original_r2 = 1 - (ss_res_orig / ss_tot)

    # Optimize weights
    optimized_weights, optimized_r2, cv_scores = optimize_weights_elastic_net(X, y)

    # Compute improvement
    if original_r2 > 0:
        improvement = (optimized_r2 - original_r2) / abs(original_r2) * 100
    else:
        improvement = np.nan

    # Feature importance
    importance_df = analyze_component_importance(X, y)
    feature_importance = importance_df["average"].to_dict() if len(importance_df) > 0 else {}

    return WeightOptimizationResult(
        composite_name=composite_name,
        method="elastic_net",
        original_weights=original_weights,
        optimized_weights=optimized_weights,
        original_r2=original_r2,
        optimized_r2=optimized_r2,
        improvement_pct=improvement,
        feature_importance=feature_importance,
        n_observations=n_obs,
        cv_scores=cv_scores
    )


# Original weights from compute_indices.py for reference
ORIGINAL_WEIGHTS = {
    "LFI": {
        "z_longterm_unemp": 0.35,  # Unemployed_27wks_Plus_z
        "z_quits_inv": 0.35,       # -JOLTS_Quits_Rate_z
        "z_hires_quits_inv": 0.30  # -Hires/Quits ratio z-score
    },
    "LPI": {
        "z_quits": 0.25,
        "z_hires_quits": 0.20,
        "z_longterm_inv": 0.20,
        "z_claims_inv": 0.20,
        "z_lfpr": 0.15
    },
    "LCI": {
        "z_reserves": 0.30,
        "z_rrp": 0.25,
        "z_effr_sofr": 0.25,
        "z_nfci": 0.20
    },
    "MRI": {
        "LPI": -0.15,
        "PCI": 0.10,
        "GCI": -0.15,
        "HCI": -0.08,
        "CCI": -0.10,
        "BCI": -0.10,
        "TCI": -0.07,
        "GCI_Gov": 0.10,
        "FCI": -0.05,
        "LCI": -0.10
    }
}
