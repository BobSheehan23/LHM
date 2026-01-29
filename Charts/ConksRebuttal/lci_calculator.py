#!/usr/bin/env python3
"""
Lighthouse Macro - LCI (Liquidity Cushion Index) Calculator
Calculates LCI from source data (FRED, NY Fed)

Core thesis: Liquidity conditions drive asset returns
- Ample liquidity (high LCI) = risk-on, positive returns
- Scarce liquidity (low LCI) = risk-off, negative returns

=============================================================================
VERSION HISTORY - DO NOT DELETE PREVIOUS VERSIONS
=============================================================================

V1 - Original Fed Liquidity Model
    Weights: Reserves (25%), RRP (25%), EFFR-IORB (20%), SOFR-EFFR (15%), TGA (15%), NFCI (15%)
    Issue: Fed liquidity (reserves, RRP) increases DURING crises as Fed responds,
           which can pollute the leading signal.

V2 - Financial Conditions Focused
    Weights: NFCI (50%), Funding spreads (25%), TGA (15%), Reserves (10%)
    Result: Better crisis detection, correct direction (scarce = negative returns)
    Issue: Heavy NFCI reliance - are we just measuring financial conditions, not liquidity?

V3 - Pure Fed Plumbing (Equity-focused)
    Weights: Reserves/GDP (30%), RRP/GDP (25%), Funding spreads (25%), TGA (20%)
    Rationale: For equities, Fed balance sheet mechanics may matter more than
               broad financial conditions. Tests the "liquidity level" hypothesis.

V4 - Crypto/Risk Asset Model (future)
    TBD - Crypto may be more sensitive to financial conditions and risk appetite

=============================================================================
RESEARCH AGENDA
=============================================================================
- Within-equity analysis: Growth vs Value, Large vs Small, Cyclical vs Defensive,
  Speculative vs Quality, High Beta vs Low Vol
- Asset-specific models: What liquidity factors matter most for each asset class?
- Transmission mechanisms: How does liquidity transmit to different assets?

Higher LCI = More liquidity cushion = Bullish
Lower LCI = Less liquidity cushion = Bearish
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


def get_fred_series(series_id, start_date='2000-01-01'):
    """Fetch series from FRED using fredapi with rate limiting"""
    from fredapi import Fred
    import time

    # Use the working API key from lighthouse infrastructure
    api_key = '11893c506c07b3b8647bf16cf60586e8'

    try:
        fred = Fred(api_key=api_key)
        time.sleep(0.3)  # Rate limit
        data = fred.get_series(series_id, observation_start=start_date)
        print(f"  Fetched {series_id}: {len(data)} obs")
        return data
    except Exception as e:
        print(f"  Warning: Could not fetch {series_id}: {e}")
        return None


def get_nyfed_rrp():
    """Fetch RRP data from NY Fed API"""
    import requests
    try:
        url = "https://markets.newyorkfed.org/api/rp/reverserepo/propositions/search.json"
        params = {
            'startDate': '2013-01-01',
            'endDate': datetime.now().strftime('%Y-%m-%d')
        }
        response = requests.get(url, params=params, timeout=30)
        data = response.json()

        if 'repo' in data and 'operations' in data['repo']:
            ops = data['repo']['operations']
            df = pd.DataFrame(ops)
            df['date'] = pd.to_datetime(df['operationDate'])
            df = df.set_index('date').sort_index()
            df['totalAmtAccepted'] = pd.to_numeric(df['totalAmtAccepted'], errors='coerce')
            return df['totalAmtAccepted'] / 1000  # Convert to billions
    except Exception as e:
        print(f"  Warning: Could not fetch RRP from NY Fed: {e}")
    return None


def get_nyfed_rates():
    """Fetch EFFR and SOFR from NY Fed API"""
    import requests
    rates = {}

    # EFFR - unsecured
    try:
        url = "https://markets.newyorkfed.org/api/rates/unsecured/effr/search.json"
        params = {'startDate': '2000-01-01', 'endDate': datetime.now().strftime('%Y-%m-%d')}
        response = requests.get(url, params=params, timeout=30)
        data = response.json()

        if 'refRates' in data:
            df = pd.DataFrame(data['refRates'])
            df['date'] = pd.to_datetime(df['effectiveDate'])
            df = df.set_index('date').sort_index()
            df['percentRate'] = pd.to_numeric(df['percentRate'], errors='coerce')
            rates['effr'] = df['percentRate']
            print(f"  Fetched EFFR: {len(rates['effr'])} obs")
    except Exception as e:
        print(f"  Warning: Could not fetch EFFR: {e}")

    # SOFR - secured
    try:
        url = "https://markets.newyorkfed.org/api/rates/secured/sofr/search.json"
        params = {'startDate': '2018-01-01', 'endDate': datetime.now().strftime('%Y-%m-%d')}
        response = requests.get(url, params=params, timeout=30)
        data = response.json()

        if 'refRates' in data:
            df = pd.DataFrame(data['refRates'])
            df['date'] = pd.to_datetime(df['effectiveDate'])
            df = df.set_index('date').sort_index()
            df['percentRate'] = pd.to_numeric(df['percentRate'], errors='coerce')
            rates['sofr'] = df['percentRate']
            print(f"  Fetched SOFR: {len(rates['sofr'])} obs")
    except Exception as e:
        print(f"  Warning: Could not fetch SOFR: {e}")

    return rates


def get_financial_stress_index():
    """
    Fetch financial stress/conditions index from FRED
    Uses Chicago Fed NFCI (National Financial Conditions Index) - weekly, back to 1971
    Higher values = tighter conditions = more stress
    """
    from fredapi import Fred
    import time

    api_key = '11893c506c07b3b8647bf16cf60586e8'
    fred = Fred(api_key=api_key)

    try:
        time.sleep(0.3)
        # NFCI is preferred - goes back further and is current
        data = fred.get_series('NFCI', observation_start='2000-01-01')
        print(f"  Fetched NFCI: {len(data)} obs")
        return data
    except Exception as e:
        print(f"  Warning: Could not fetch NFCI: {e}")

    # Fallback to ANFCI (adjusted NFCI)
    try:
        time.sleep(0.3)
        data = fred.get_series('ANFCI', observation_start='2000-01-01')
        print(f"  Fetched ANFCI: {len(data)} obs")
        return data
    except Exception as e:
        print(f"  Warning: Could not fetch ANFCI: {e}")

    return None


def calculate_zscore(series, window=252*2):
    """
    Calculate rolling z-score
    Using 2-year lookback for regime-awareness
    """
    mean = series.rolling(window=window, min_periods=60).mean()
    std = series.rolling(window=window, min_periods=60).std()
    return (series - mean) / std


def calculate_lci(version='v2'):
    """
    Calculate Liquidity Cushion Index from source data

    Args:
        version: 'v1' = original formula (Fed liquidity + financial conditions)
                 'v2' = simplified formula (focused on financial conditions)

    Returns DataFrame with LCI and components

    V2 Philosophy:
    - Financial conditions indices (NFCI) are the key leading indicator
    - Reserve levels matter but lag the cycle (Fed responds TO crises)
    - Funding spreads matter for short-term stress
    - TGA matters for liquidity supply/demand

    The key insight: High reserves during a crisis don't help if financial
    conditions are still tight. NFCI captures the actual conditions that
    drive returns.
    """
    print("Fetching data from FRED and NY Fed...")

    # === FETCH DATA ===

    # GDP (quarterly, will forward fill)
    gdp = get_fred_series('GDP', '2000-01-01')

    # Bank Reserves (weekly)
    reserves = get_fred_series('WRESBAL', '2000-01-01')  # Reserve balances with Fed
    if reserves is None:
        reserves = get_fred_series('TOTRESNS', '2000-01-01')  # Fallback to monthly

    # TGA (Treasury General Account)
    tga = get_fred_series('WTREGEN', '2000-01-01')  # Weekly TGA balance

    # IORB (Interest on Reserve Balances) - was IOER before July 2021
    iorb = get_fred_series('IORB', '2019-01-01')
    ioer = get_fred_series('IOER', '2008-01-01')

    # Fed Funds Target Rate (for pre-IORB era stress measure)
    ff_target_upper = get_fred_series('DFEDTARU', '2000-01-01')  # Upper bound (post-2008)
    ff_target = get_fred_series('DFEDTAR', '2000-01-01')  # Single target (pre-2008)

    # RRP from NY Fed
    rrp = get_nyfed_rrp()

    # Rates from NY Fed
    nyfed_rates = get_nyfed_rates()
    effr = nyfed_rates.get('effr')
    sofr = nyfed_rates.get('sofr')

    # Financial Conditions Index (Chicago Fed NFCI)
    nfci = get_financial_stress_index()

    print("Processing data...")

    # === BUILD DAILY DATAFRAME ===

    # Create daily date range
    # Start from 2003 to capture pre-GFC, GFC, and post-GFC periods
    start = '2003-01-01'
    end = datetime.now().strftime('%Y-%m-%d')
    dates = pd.date_range(start=start, end=end, freq='D')
    df = pd.DataFrame(index=dates)

    # Merge GDP (quarterly -> daily via forward fill)
    if gdp is not None:
        df = df.join(gdp.rename('gdp'))
        df['gdp'] = df['gdp'].ffill()

    # Merge Reserves
    if reserves is not None:
        df = df.join(reserves.rename('reserves'))
        df['reserves'] = df['reserves'].ffill()

    # Merge TGA
    if tga is not None:
        df = df.join(tga.rename('tga'))
        df['tga'] = df['tga'].ffill()

    # Merge RRP
    if rrp is not None:
        rrp.index = rrp.index.tz_localize(None) if rrp.index.tz else rrp.index
        df = df.join(rrp.rename('rrp'))
        df['rrp'] = df['rrp'].ffill().fillna(0)  # Pre-RRP era = 0

    # Merge IORB/IOER (combine into one series)
    if iorb is not None or ioer is not None:
        iorb_combined = pd.concat([ioer, iorb]).sort_index()
        iorb_combined = iorb_combined[~iorb_combined.index.duplicated(keep='last')]
        df = df.join(iorb_combined.rename('iorb'))
        df['iorb'] = df['iorb'].ffill()

    # Merge EFFR
    if effr is not None:
        effr.index = effr.index.tz_localize(None) if effr.index.tz else effr.index
        df = df.join(effr.rename('effr'))
        df['effr'] = df['effr'].ffill()

    # Merge SOFR
    if sofr is not None:
        sofr.index = sofr.index.tz_localize(None) if sofr.index.tz else sofr.index
        df = df.join(sofr.rename('sofr'))
        df['sofr'] = df['sofr'].ffill()

    # Merge Fed Funds Target (combine pre-2008 single target with post-2008 upper bound)
    if ff_target is not None or ff_target_upper is not None:
        ff_combined = pd.concat([ff_target, ff_target_upper]).sort_index()
        ff_combined = ff_combined[~ff_combined.index.duplicated(keep='last')]
        df = df.join(ff_combined.rename('ff_target'))
        df['ff_target'] = df['ff_target'].ffill()

    # Merge NFCI (Chicago Fed National Financial Conditions Index)
    if nfci is not None:
        nfci.index = nfci.index.tz_localize(None) if hasattr(nfci.index, 'tz') and nfci.index.tz else nfci.index
        df = df.join(nfci.rename('nfci'))
        df['nfci'] = df['nfci'].ffill()

    # === CALCULATE RATIOS AND SPREADS ===

    # Reserves/GDP ratio (%)
    if 'reserves' in df.columns and 'gdp' in df.columns:
        df['reserves_gdp'] = (df['reserves'] / df['gdp']) * 100

    # RRP/GDP ratio (%)
    if 'rrp' in df.columns and 'gdp' in df.columns:
        df['rrp_gdp'] = (df['rrp'] / df['gdp']) * 100

    # TGA/GDP ratio (%)
    if 'tga' in df.columns and 'gdp' in df.columns:
        df['tga_gdp'] = (df['tga'] / df['gdp']) * 100

    # EFFR-IORB spread (bps) - positive = funding pressure
    if 'effr' in df.columns and 'iorb' in df.columns:
        df['effr_iorb'] = (df['effr'] - df['iorb']) * 100

    # SOFR-EFFR spread (bps) - positive = repo stress
    if 'sofr' in df.columns and 'effr' in df.columns:
        df['sofr_effr'] = (df['sofr'] - df['effr']) * 100

    # EFFR vs Target spread (bps) - for pre-IORB era, positive = Fed losing control
    if 'effr' in df.columns and 'ff_target' in df.columns:
        df['effr_target'] = (df['effr'] - df['ff_target']) * 100

    # === CALCULATE Z-SCORES FOR ALL AVAILABLE COMPONENTS ===

    # Reserves/GDP z-score (higher = more cushion = positive)
    if 'reserves_gdp' in df.columns:
        df['z_reserves'] = calculate_zscore(df['reserves_gdp'])

    # RRP/GDP z-score (higher = more excess liquidity = positive)
    if 'rrp_gdp' in df.columns:
        df['z_rrp'] = calculate_zscore(df['rrp_gdp'])

    # EFFR-IORB z-score (INVERTED: higher spread = tighter = negative)
    if 'effr_iorb' in df.columns:
        df['z_effr_iorb'] = -calculate_zscore(df['effr_iorb'])

    # SOFR-EFFR z-score (INVERTED: higher spread = more stress = negative)
    if 'sofr_effr' in df.columns:
        df['z_sofr_effr'] = -calculate_zscore(df['sofr_effr'])

    # TGA z-score (INVERTED: higher TGA = drains liquidity = negative)
    if 'tga_gdp' in df.columns:
        df['z_tga'] = -calculate_zscore(df['tga_gdp'])

    # EFFR vs Target z-score (INVERTED: higher = Fed losing control = negative)
    if 'effr_target' in df.columns:
        df['z_effr_target'] = -calculate_zscore(df['effr_target'])

    # NFCI z-score (INVERTED: higher NFCI = tighter conditions = negative for liquidity)
    if 'nfci' in df.columns:
        df['z_nfci'] = -calculate_zscore(df['nfci'])

    # === CALCULATE LCI WITH ADAPTIVE WEIGHTING ===
    # Different weights based on data availability per row

    def calculate_lci_row_v1(row):
        """V1: Original formula with Fed liquidity + financial conditions"""
        components = []
        weights = []

        # Always use reserves if available
        if pd.notna(row.get('z_reserves')):
            components.append(row['z_reserves'])
            weights.append(0.25)

        # RRP (0 pre-2013, so z-score may be weird early on)
        if pd.notna(row.get('z_rrp')):
            components.append(row['z_rrp'])
            weights.append(0.25)

        # TGA always available
        if pd.notna(row.get('z_tga')):
            components.append(row['z_tga'])
            weights.append(0.15)

        # SOFR-EFFR only post-2018
        if pd.notna(row.get('z_sofr_effr')):
            components.append(row['z_sofr_effr'])
            weights.append(0.15)

        # EFFR-IORB only post-2008
        if pd.notna(row.get('z_effr_iorb')):
            components.append(row['z_effr_iorb'])
            weights.append(0.20)
        # Fallback to EFFR vs Target for pre-2008
        elif pd.notna(row.get('z_effr_target')):
            components.append(row['z_effr_target'])
            weights.append(0.20)

        # NFCI - broader financial conditions measure (available from 2000)
        if pd.notna(row.get('z_nfci')):
            components.append(row['z_nfci'])
            weights.append(0.15)

        if not components:
            return np.nan

        # Normalize weights and calculate weighted average
        total_weight = sum(weights)
        lci = sum(c * w / total_weight for c, w in zip(components, weights))
        return lci

    def calculate_lci_row_v2(row):
        """
        V2: Financial conditions-focused formula

        Key insight: NFCI is the dominant factor for forward returns because
        it captures actual credit conditions in the economy. Fed reserves
        often INCREASE during stress (as the Fed responds), which pollutes
        the signal if weighted too heavily.

        Weights:
        - NFCI: 50% (primary driver of forward returns)
        - Funding spreads: 25% (EFFR-IORB or EFFR-Target)
        - TGA: 15% (Treasury operations affect near-term liquidity)
        - Reserves: 10% (Fed response, less predictive but still relevant)
        """
        components = []
        weights = []

        # NFCI is PRIMARY - this is the key signal
        if pd.notna(row.get('z_nfci')):
            components.append(row['z_nfci'])
            weights.append(0.50)

        # Funding spreads - important for stress detection
        if pd.notna(row.get('z_effr_iorb')):
            components.append(row['z_effr_iorb'])
            weights.append(0.25)
        elif pd.notna(row.get('z_effr_target')):
            components.append(row['z_effr_target'])
            weights.append(0.25)

        # TGA - Treasury operations
        if pd.notna(row.get('z_tga')):
            components.append(row['z_tga'])
            weights.append(0.15)

        # Reserves - smaller weight because it's reactive not predictive
        if pd.notna(row.get('z_reserves')):
            components.append(row['z_reserves'])
            weights.append(0.10)

        if not components:
            return np.nan

        total_weight = sum(weights)
        lci = sum(c * w / total_weight for c, w in zip(components, weights))
        return lci

    def calculate_lci_row_v3(row):
        """
        V3: Pure Fed Plumbing Model (Equity-focused)

        Tests Conks' claim about "level" of liquidity having no effect.
        Focuses on actual Fed balance sheet mechanics without NFCI.

        Rationale: For equities specifically, the level of reserves and RRP
        may matter as they represent actual cash in the system available
        for risk-taking. This is the pure "liquidity level" test.

        Weights:
        - Reserves/GDP: 30% (banking system liquidity buffer)
        - RRP/GDP: 25% (excess liquidity parked at Fed)
        - Funding spreads: 25% (EFFR-IORB stress signal)
        - TGA: 20% (Treasury operations, inverted)
        """
        components = []
        weights = []

        # Reserves/GDP - core liquidity measure
        if pd.notna(row.get('z_reserves')):
            components.append(row['z_reserves'])
            weights.append(0.30)

        # RRP/GDP - excess liquidity
        if pd.notna(row.get('z_rrp')):
            components.append(row['z_rrp'])
            weights.append(0.25)

        # Funding spreads
        if pd.notna(row.get('z_effr_iorb')):
            components.append(row['z_effr_iorb'])
            weights.append(0.25)
        elif pd.notna(row.get('z_effr_target')):
            components.append(row['z_effr_target'])
            weights.append(0.25)

        # TGA - Treasury operations
        if pd.notna(row.get('z_tga')):
            components.append(row['z_tga'])
            weights.append(0.20)

        if not components:
            return np.nan

        total_weight = sum(weights)
        lci = sum(c * w / total_weight for c, w in zip(components, weights))
        return lci

    def calculate_lci_row_original(row):
        """
        ORIGINAL LCI Formula from calculate_proprietary_indicators.py

        LCI = (z(RRP/GDP) + z(Reserves/GDP)) / 2

        This is the formula that produced the strong results.
        Simple average of two pure Fed liquidity measures.
        """
        components = []

        if pd.notna(row.get('z_rrp')):
            components.append(row['z_rrp'])

        if pd.notna(row.get('z_reserves')):
            components.append(row['z_reserves'])

        if not components:
            return np.nan

        return sum(components) / len(components)

    # Use version-specific calculation
    if version == 'original':
        df['LCI'] = df.apply(calculate_lci_row_original, axis=1)
    elif version == 'v3':
        df['LCI'] = df.apply(calculate_lci_row_v3, axis=1)
    elif version == 'v2':
        df['LCI'] = df.apply(calculate_lci_row_v2, axis=1)
    else:
        df['LCI'] = df.apply(calculate_lci_row_v1, axis=1)

    # Drop rows where LCI couldn't be calculated
    df = df.dropna(subset=['LCI'])

    # === ADDITIONAL METRICS FOR RICHER ANALYSIS ===

    # LCI Momentum (21-day rate of change)
    df['LCI_momentum'] = df['LCI'].diff(21)

    # LCI Direction (5-day smoothed direction)
    df['LCI_direction'] = df['LCI'].rolling(5).mean().diff()

    # LCI Regime (historical percentile - where are we vs history?)
    df['LCI_percentile'] = df['LCI'].rolling(window=252*3, min_periods=252).apply(
        lambda x: (x.iloc[-1] > x).mean() * 100, raw=False
    )

    # LCI Acceleration (change in momentum)
    df['LCI_acceleration'] = df['LCI_momentum'].diff(5)

    # Regime classification
    df['LCI_regime'] = pd.cut(
        df['LCI'],
        bins=[-np.inf, -1.0, -0.5, 0.5, 1.0, np.inf],
        labels=['Crisis', 'Scarce', 'Neutral', 'Ample', 'Flush']
    )

    # Determine which components are available
    available_components = []
    if 'z_reserves' in df.columns and df['z_reserves'].notna().any():
        available_components.append('reserves')
    if 'z_rrp' in df.columns and df['z_rrp'].notna().any():
        available_components.append('rrp')
    if 'z_tga' in df.columns and df['z_tga'].notna().any():
        available_components.append('tga')
    if 'z_effr_iorb' in df.columns and df['z_effr_iorb'].notna().any():
        available_components.append('effr_iorb')
    if 'z_sofr_effr' in df.columns and df['z_sofr_effr'].notna().any():
        available_components.append('sofr_effr')
    if 'z_effr_target' in df.columns and df['z_effr_target'].notna().any():
        available_components.append('effr_target')
    if 'z_nfci' in df.columns and df['z_nfci'].notna().any():
        available_components.append('nfci')

    print(f"LCI calculated: {len(df)} observations from {df.index.min().date()} to {df.index.max().date()}")
    print(f"Components available: {available_components}")
    print(f"LCI range: {df['LCI'].min():.2f} to {df['LCI'].max():.2f}")
    print(f"Current LCI: {df['LCI'].iloc[-1]:.2f} ({df['LCI_regime'].iloc[-1]})")
    print(f"Current momentum (21d): {df['LCI_momentum'].iloc[-1]:.2f}")
    print(f"Current percentile: {df['LCI_percentile'].iloc[-1]:.0f}%")

    return df


if __name__ == '__main__':
    df = calculate_lci()

    # Quick sanity check
    print("\n=== LCI Summary Stats ===")
    print(df['LCI'].describe())

    print("\n=== Recent Values ===")
    print(df[['LCI']].tail(10))
