"""
Labor Market Series Registry - Comprehensive Data Collection
Lighthouse Macro - January 2026

This module defines ALL labor market series for ingestion from:
- FRED (Federal Reserve Economic Data)
- BLS API (Bureau of Labor Statistics)
- Atlanta Fed Wage Growth Tracker
- Indeed Hiring Lab
- State-level LAUS data

The registry is organized by analytical category to support
the Pillar 1 Labor framework's segmentation analysis.

Categories:
1. HEADLINE AGGREGATES - Core national indicators
2. DEMOGRAPHIC SEGMENTATION - Age, education, race, gender
3. GEOGRAPHIC SEGMENTATION - State-level, regional
4. INDUSTRY SEGMENTATION - Sector-specific flows and stocks
5. FLOW INDICATORS - JOLTS hires, quits, openings by segment
6. WAGE DYNAMICS - Earnings by segment, wage growth tracker
7. LABOR SUPPLY - Participation, employment-population ratios
8. JOB QUALITY - Full-time/part-time, temp help, hours
9. UNEMPLOYMENT DECOMPOSITION - Duration, reason, composition
10. LEADING INDICATORS - High-frequency, real-time proxies
"""

from typing import TypedDict

# =============================================================================
# TYPE DEFINITIONS
# =============================================================================

class SeriesDefinition(TypedDict):
    """Definition for a data series."""
    fred_id: str | None          # FRED series ID (if available)
    bls_id: str | None           # BLS API series ID (if different from FRED)
    name: str                    # Internal name for database
    description: str             # Human-readable description
    frequency: str               # D, W, M, Q (daily, weekly, monthly, quarterly)
    source: str                  # FRED, BLS, ATLANTA_FED, INDEED, etc.
    category: str                # Analytical category
    subcategory: str | None      # More specific grouping
    seasonal_adj: bool           # Whether seasonally adjusted
    units: str                   # Percent, Thousands, Index, etc.
    lead_lag: str | None         # Leading, Coincident, Lagging
    notes: str | None            # Additional context


# =============================================================================
# 1. HEADLINE AGGREGATES
# =============================================================================

HEADLINE_SERIES: dict[str, SeriesDefinition] = {
    # Core Employment
    "PAYEMS": {
        "fred_id": "PAYEMS",
        "bls_id": "CES0000000001",
        "name": "Nonfarm_Payrolls",
        "description": "Total Nonfarm Payrolls, Thousands",
        "frequency": "M",
        "source": "FRED",
        "category": "HEADLINE",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": "Primary headline employment measure"
    },
    "UNRATE": {
        "fred_id": "UNRATE",
        "bls_id": "LNS14000000",
        "name": "Unemployment_Rate",
        "description": "Civilian Unemployment Rate",
        "frequency": "M",
        "source": "FRED",
        "category": "HEADLINE",
        "subcategory": "Unemployment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Lagging",
        "notes": "U-3 headline unemployment rate, lags cycle by 6-9 months"
    },
    "CIVPART": {
        "fred_id": "CIVPART",
        "bls_id": "LNS11300000",
        "name": "LFPR_Total",
        "description": "Labor Force Participation Rate",
        "frequency": "M",
        "source": "FRED",
        "category": "HEADLINE",
        "subcategory": "Labor Supply",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Structural",
        "notes": "Structural labor supply measure"
    },
    "EMRATIO": {
        "fred_id": "EMRATIO",
        "bls_id": "LNS12300000",
        "name": "Emp_Pop_Ratio",
        "description": "Employment-Population Ratio",
        "frequency": "M",
        "source": "FRED",
        "category": "HEADLINE",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": "Share of population employed"
    },
    "U6RATE": {
        "fred_id": "U6RATE",
        "bls_id": "LNS13327709",
        "name": "U6_Underemployment",
        "description": "U-6 Total Unemployed + Marginally Attached + Part-Time for Economic Reasons",
        "frequency": "M",
        "source": "FRED",
        "category": "HEADLINE",
        "subcategory": "Unemployment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Lagging",
        "notes": "Broader measure of labor underutilization"
    },
}


# =============================================================================
# 2. DEMOGRAPHIC SEGMENTATION - UNEMPLOYMENT RATES
# =============================================================================

UNEMPLOYMENT_BY_AGE: dict[str, SeriesDefinition] = {
    "LNS14000012": {
        "fred_id": "LNS14000012",
        "bls_id": "LNS14000012",
        "name": "Unemp_Rate_16_19",
        "description": "Unemployment Rate - 16 to 19 years",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Age_Unemployment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Leading",
        "notes": "Youth unemployment, typically 2-3x headline, often leads cycle"
    },
    "LNS14000036": {
        "fred_id": "LNS14000036",
        "bls_id": "LNS14000036",
        "name": "Unemp_Rate_20_24",
        "description": "Unemployment Rate - 20 to 24 years",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Age_Unemployment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Leading",
        "notes": "Young adult unemployment, sensitive to entry-level hiring"
    },
    "LNS14024887": {
        "fred_id": "LNS14024887",
        "bls_id": "LNS14024887",
        "name": "Unemp_Rate_16_24",
        "description": "Unemployment Rate - 16 to 24 years (Youth)",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Age_Unemployment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Leading",
        "notes": "Combined youth unemployment"
    },
    "LNS14000060": {
        "fred_id": "LNS14000060",
        "bls_id": "LNS14000060",
        "name": "Unemp_Rate_25_54",
        "description": "Unemployment Rate - 25 to 54 years (Prime Age)",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Age_Unemployment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": "Core workforce unemployment, less volatile than youth"
    },
    "LNS14000089": {
        "fred_id": "LNS14000089",
        "bls_id": "LNS14000089",
        "name": "Unemp_Rate_25_34",
        "description": "Unemployment Rate - 25 to 34 years",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Age_Unemployment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": None
    },
    "LNS14000091": {
        "fred_id": "LNS14000091",
        "bls_id": "LNS14000091",
        "name": "Unemp_Rate_35_44",
        "description": "Unemployment Rate - 35 to 44 years",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Age_Unemployment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": None
    },
    "LNS14000093": {
        "fred_id": "LNS14000093",
        "bls_id": "LNS14000093",
        "name": "Unemp_Rate_45_54",
        "description": "Unemployment Rate - 45 to 54 years",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Age_Unemployment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": None
    },
    "LNS14024230": {
        "fred_id": "LNS14024230",
        "bls_id": "LNS14024230",
        "name": "Unemp_Rate_55_Plus",
        "description": "Unemployment Rate - 55 years and over",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Age_Unemployment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Lagging",
        "notes": "Older worker unemployment, often stickier once unemployed"
    },
}

UNEMPLOYMENT_BY_EDUCATION: dict[str, SeriesDefinition] = {
    "LNS14027659": {
        "fred_id": "LNS14027659",
        "bls_id": "LNS14027659",
        "name": "Unemp_Rate_LessThanHS",
        "description": "Unemployment Rate - Less Than High School Diploma, 25 yrs+",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Education_Unemployment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Leading",
        "notes": "Most vulnerable education cohort, often first to see stress"
    },
    "LNS14027660": {
        "fred_id": "LNS14027660",
        "bls_id": "LNS14027660",
        "name": "Unemp_Rate_HS_Only",
        "description": "Unemployment Rate - High School Graduates, No College, 25 yrs+",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Education_Unemployment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": None
    },
    "LNS14027689": {
        "fred_id": "LNS14027689",
        "bls_id": "LNS14027689",
        "name": "Unemp_Rate_SomeCollege",
        "description": "Unemployment Rate - Some College or Associate Degree, 25 yrs+",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Education_Unemployment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": None
    },
    "LNS14027662": {
        "fred_id": "LNS14027662",
        "bls_id": "LNS14027662",
        "name": "Unemp_Rate_Bachelors_Plus",
        "description": "Unemployment Rate - Bachelor's Degree and Higher, 25 yrs+",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Education_Unemployment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Lagging",
        "notes": "Most insulated cohort, often last to show stress"
    },
}

UNEMPLOYMENT_BY_RACE: dict[str, SeriesDefinition] = {
    "LNS14000003": {
        "fred_id": "LNS14000003",
        "bls_id": "LNS14000003",
        "name": "Unemp_Rate_White",
        "description": "Unemployment Rate - White",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Race_Unemployment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": None
    },
    "LNS14000006": {
        "fred_id": "LNS14000006",
        "bls_id": "LNS14000006",
        "name": "Unemp_Rate_Black",
        "description": "Unemployment Rate - Black or African American",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Race_Unemployment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Leading",
        "notes": "Historically ~2x White unemployment, often leads cycle turns"
    },
    "LNS14000009": {
        "fred_id": "LNS14000009",
        "bls_id": "LNS14000009",
        "name": "Unemp_Rate_Hispanic",
        "description": "Unemployment Rate - Hispanic or Latino",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Race_Unemployment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Leading",
        "notes": "Concentrated in cyclically sensitive industries"
    },
    "LNU04032183": {
        "fred_id": "LNU04032183",
        "bls_id": "LNU04032183",
        "name": "Unemp_Rate_Asian",
        "description": "Unemployment Rate - Asian",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Race_Unemployment",
        "seasonal_adj": False,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": "Not seasonally adjusted"
    },
}

UNEMPLOYMENT_BY_GENDER: dict[str, SeriesDefinition] = {
    "LNS14000001": {
        "fred_id": "LNS14000001",
        "bls_id": "LNS14000001",
        "name": "Unemp_Rate_Men",
        "description": "Unemployment Rate - Men, 16 years and over",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Gender_Unemployment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": "More cyclically volatile (goods-producing industries)"
    },
    "LNS14000002": {
        "fred_id": "LNS14000002",
        "bls_id": "LNS14000002",
        "name": "Unemp_Rate_Women",
        "description": "Unemployment Rate - Women, 16 years and over",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Gender_Unemployment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": "More stable (services-concentrated)"
    },
}


# =============================================================================
# 3. DEMOGRAPHIC SEGMENTATION - LABOR FORCE PARTICIPATION
# =============================================================================

LFPR_BY_AGE: dict[str, SeriesDefinition] = {
    "LNS11300060": {
        "fred_id": "LNS11300060",
        "bls_id": "LNS11300060",
        "name": "LFPR_25_54",
        "description": "Labor Force Participation Rate - 25 to 54 years (Prime Age)",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Age_LFPR",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Structural",
        "notes": "Core labor supply measure, strips out retirement/education effects"
    },
    "LNS11324230": {
        "fred_id": "LNS11324230",
        "bls_id": "LNS11324230",
        "name": "LFPR_55_Plus",
        "description": "Labor Force Participation Rate - 55 years and over",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Age_LFPR",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Structural",
        "notes": "Retirement dynamics, COVID acceleration of early retirement"
    },
    "LNS11300012": {
        "fred_id": "LNS11300012",
        "bls_id": "LNS11300012",
        "name": "LFPR_16_19",
        "description": "Labor Force Participation Rate - 16 to 19 years",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Age_LFPR",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Structural",
        "notes": "Youth participation, affected by education enrollment trends"
    },
    "LNS11300036": {
        "fred_id": "LNS11300036",
        "bls_id": "LNS11300036",
        "name": "LFPR_20_24",
        "description": "Labor Force Participation Rate - 20 to 24 years",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Age_LFPR",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Structural",
        "notes": None
    },
}

LFPR_BY_GENDER: dict[str, SeriesDefinition] = {
    "LNS11300001": {
        "fred_id": "LNS11300001",
        "bls_id": "LNS11300001",
        "name": "LFPR_Men",
        "description": "Labor Force Participation Rate - Men",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Gender_LFPR",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Structural",
        "notes": "Long-term secular decline since 1950s"
    },
    "LNS11300002": {
        "fred_id": "LNS11300002",
        "bls_id": "LNS11300002",
        "name": "LFPR_Women",
        "description": "Labor Force Participation Rate - Women",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Gender_LFPR",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Structural",
        "notes": "Long-term secular increase, now plateaued"
    },
}

LFPR_BY_RACE: dict[str, SeriesDefinition] = {
    "LNS11300003": {
        "fred_id": "LNS11300003",
        "bls_id": "LNS11300003",
        "name": "LFPR_White",
        "description": "Labor Force Participation Rate - White",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Race_LFPR",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Structural",
        "notes": None
    },
    "LNS11300006": {
        "fred_id": "LNS11300006",
        "bls_id": "LNS11300006",
        "name": "LFPR_Black",
        "description": "Labor Force Participation Rate - Black or African American",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Race_LFPR",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Structural",
        "notes": None
    },
    "LNS11300009": {
        "fred_id": "LNS11300009",
        "bls_id": "LNS11300009",
        "name": "LFPR_Hispanic",
        "description": "Labor Force Participation Rate - Hispanic or Latino",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Race_LFPR",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Structural",
        "notes": None
    },
}


# =============================================================================
# 4. DEMOGRAPHIC SEGMENTATION - EMPLOYMENT-POPULATION RATIO
# =============================================================================

EPOP_BY_AGE: dict[str, SeriesDefinition] = {
    "LNS12300060": {
        "fred_id": "LNS12300060",
        "bls_id": "LNS12300060",
        "name": "EPOP_25_54",
        "description": "Employment-Population Ratio - 25 to 54 years (Prime Age)",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Age_EPOP",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": "Core employment utilization measure"
    },
    "LNS12300012": {
        "fred_id": "LNS12300012",
        "bls_id": "LNS12300012",
        "name": "EPOP_16_19",
        "description": "Employment-Population Ratio - 16 to 19 years",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Age_EPOP",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Leading",
        "notes": "Youth employment, sensitive to entry-level conditions"
    },
}

EPOP_BY_GENDER: dict[str, SeriesDefinition] = {
    "LNS12300001": {
        "fred_id": "LNS12300001",
        "bls_id": "LNS12300001",
        "name": "EPOP_Men",
        "description": "Employment-Population Ratio - Men",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Gender_EPOP",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": None
    },
    "LNS12300002": {
        "fred_id": "LNS12300002",
        "bls_id": "LNS12300002",
        "name": "EPOP_Women",
        "description": "Employment-Population Ratio - Women",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Gender_EPOP",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": None
    },
}

EPOP_BY_RACE: dict[str, SeriesDefinition] = {
    "LNS12300003": {
        "fred_id": "LNS12300003",
        "bls_id": "LNS12300003",
        "name": "EPOP_White",
        "description": "Employment-Population Ratio - White",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Race_EPOP",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": None
    },
    "LNS12300006": {
        "fred_id": "LNS12300006",
        "bls_id": "LNS12300006",
        "name": "EPOP_Black",
        "description": "Employment-Population Ratio - Black or African American",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Race_EPOP",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": None
    },
    "LNS12300009": {
        "fred_id": "LNS12300009",
        "bls_id": "LNS12300009",
        "name": "EPOP_Hispanic",
        "description": "Employment-Population Ratio - Hispanic or Latino",
        "frequency": "M",
        "source": "FRED",
        "category": "DEMOGRAPHIC",
        "subcategory": "Race_EPOP",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": None
    },
}


# =============================================================================
# 5. GEOGRAPHIC SEGMENTATION - STATE UNEMPLOYMENT
# =============================================================================

# All 50 states + DC unemployment rates
STATE_CODES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL",
    "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME",
    "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH",
    "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI",
    "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

STATE_UNEMPLOYMENT: dict[str, SeriesDefinition] = {}
for state in STATE_CODES:
    STATE_UNEMPLOYMENT[f"{state}UR"] = {
        "fred_id": f"{state}UR",
        "bls_id": None,
        "name": f"Unemp_Rate_{state}",
        "description": f"Unemployment Rate - {state}",
        "frequency": "M",
        "source": "FRED",
        "category": "GEOGRAPHIC",
        "subcategory": "State_Unemployment",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": None
    }

# Regional aggregates
REGIONAL_SERIES: dict[str, SeriesDefinition] = {
    # Census Region unemployment (constructed from state data)
    # Note: These may need to be calculated from state-level data
}


# =============================================================================
# 6. INDUSTRY SEGMENTATION - EMPLOYMENT
# =============================================================================

EMPLOYMENT_BY_INDUSTRY: dict[str, SeriesDefinition] = {
    # Private sector total
    "USPRIV": {
        "fred_id": "USPRIV",
        "bls_id": "CES0500000001",
        "name": "Emp_Private",
        "description": "All Employees: Total Private",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": None
    },
    # Goods-producing
    "USGOOD": {
        "fred_id": "USGOOD",
        "bls_id": "CES0600000001",
        "name": "Emp_Goods_Producing",
        "description": "All Employees: Goods-Producing Industries",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Leading",
        "notes": "Cyclically sensitive, leads services"
    },
    # Mining and logging
    "USMINE": {
        "fred_id": "USMINE",
        "bls_id": "CES1000000001",
        "name": "Emp_Mining_Logging",
        "description": "All Employees: Mining and Logging",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": "Commodity price sensitive"
    },
    # Construction
    "USCONS": {
        "fred_id": "USCONS",
        "bls_id": "CES2000000001",
        "name": "Emp_Construction",
        "description": "All Employees: Construction",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Leading",
        "notes": "Interest rate sensitive, leads housing"
    },
    # Manufacturing - Total
    "MANEMP": {
        "fred_id": "MANEMP",
        "bls_id": "CES3000000001",
        "name": "Emp_Manufacturing",
        "description": "All Employees: Manufacturing",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Leading",
        "notes": "Leading indicator, first to contract"
    },
    # Manufacturing - Durable
    "DMANEMP": {
        "fred_id": "DMANEMP",
        "bls_id": "CES3100000001",
        "name": "Emp_Mfg_Durable",
        "description": "All Employees: Durable Goods Manufacturing",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Leading",
        "notes": "More cyclically sensitive than non-durable"
    },
    # Manufacturing - Non-Durable
    "NDMANEMP": {
        "fred_id": "NDMANEMP",
        "bls_id": "CES3200000001",
        "name": "Emp_Mfg_NonDurable",
        "description": "All Employees: Non-Durable Goods Manufacturing",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": None
    },
    # Services-providing
    "SRVPRD": {
        "fred_id": "SRVPRD",
        "bls_id": "CES0800000001",
        "name": "Emp_Services_Providing",
        "description": "All Employees: Service-Providing Industries",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Lagging",
        "notes": "Lags goods-producing"
    },
    # Trade, Transportation, Utilities
    "USTPU": {
        "fred_id": "USTPU",
        "bls_id": "CES4000000001",
        "name": "Emp_Trade_Transport_Utilities",
        "description": "All Employees: Trade, Transportation, and Utilities",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": None
    },
    # Wholesale Trade
    "USWTRADE": {
        "fred_id": "USWTRADE",
        "bls_id": "CES4100000001",
        "name": "Emp_Wholesale_Trade",
        "description": "All Employees: Wholesale Trade",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": None
    },
    # Retail Trade
    "USTRADE": {
        "fred_id": "USTRADE",
        "bls_id": "CES4200000001",
        "name": "Emp_Retail_Trade",
        "description": "All Employees: Retail Trade",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": "Consumer spending proxy"
    },
    # Transportation and Warehousing
    "CES4300000001": {
        "fred_id": "CES4300000001",
        "bls_id": "CES4300000001",
        "name": "Emp_Transportation_Warehousing",
        "description": "All Employees: Transportation and Warehousing",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": None
    },
    # Information
    "USINFO": {
        "fred_id": "USINFO",
        "bls_id": "CES5000000001",
        "name": "Emp_Information",
        "description": "All Employees: Information",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": "Tech sector proxy"
    },
    # Financial Activities
    "USFIRE": {
        "fred_id": "USFIRE",
        "bls_id": "CES5500000001",
        "name": "Emp_Financial_Activities",
        "description": "All Employees: Financial Activities",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": None
    },
    # Professional and Business Services
    "USPBS": {
        "fred_id": "USPBS",
        "bls_id": "CES6000000001",
        "name": "Emp_Prof_Business_Services",
        "description": "All Employees: Professional and Business Services",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": "Includes temp help services"
    },
    # Temporary Help Services (critical leading indicator)
    "TEMPHELPS": {
        "fred_id": "TEMPHELPS",
        "bls_id": "CES6056132001",
        "name": "Emp_Temp_Help",
        "description": "All Employees: Temporary Help Services",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Leading",
        "notes": "PRIMARY LEADING INDICATOR - first hired, first fired"
    },
    # Education and Health Services
    "USEHS": {
        "fred_id": "USEHS",
        "bls_id": "CES6500000001",
        "name": "Emp_Education_Health",
        "description": "All Employees: Education and Health Services",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Lagging",
        "notes": "Defensive, counter-cyclical"
    },
    # Health Care
    "CES6562000001": {
        "fred_id": "CES6562000001",
        "bls_id": "CES6562000001",
        "name": "Emp_Healthcare",
        "description": "All Employees: Health Care",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Lagging",
        "notes": "Defensive sector"
    },
    # Leisure and Hospitality
    "USLAH": {
        "fred_id": "USLAH",
        "bls_id": "CES7000000001",
        "name": "Emp_Leisure_Hospitality",
        "description": "All Employees: Leisure and Hospitality",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Lagging",
        "notes": "Last to recover"
    },
    # Other Services
    "USSERV": {
        "fred_id": "USSERV",
        "bls_id": "CES8000000001",
        "name": "Emp_Other_Services",
        "description": "All Employees: Other Services",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": None
    },
    # Government
    "USGOVT": {
        "fred_id": "USGOVT",
        "bls_id": "CES9000000001",
        "name": "Emp_Government",
        "description": "All Employees: Government",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Counter-cyclical",
        "notes": "Counter-cyclical, policy response"
    },
    # Federal Government
    "CES9091000001": {
        "fred_id": "CES9091000001",
        "bls_id": "CES9091000001",
        "name": "Emp_Federal_Govt",
        "description": "All Employees: Federal Government",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Counter-cyclical",
        "notes": None
    },
    # State Government
    "CES9092000001": {
        "fred_id": "CES9092000001",
        "bls_id": "CES9092000001",
        "name": "Emp_State_Govt",
        "description": "All Employees: State Government",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Counter-cyclical",
        "notes": None
    },
    # Local Government
    "CES9093000001": {
        "fred_id": "CES9093000001",
        "bls_id": "CES9093000001",
        "name": "Emp_Local_Govt",
        "description": "All Employees: Local Government",
        "frequency": "M",
        "source": "FRED",
        "category": "INDUSTRY",
        "subcategory": "Employment",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Counter-cyclical",
        "notes": None
    },
}


# =============================================================================
# 7. JOLTS FLOW INDICATORS
# =============================================================================

JOLTS_TOTAL: dict[str, SeriesDefinition] = {
    # Job Openings
    "JTSJOL": {
        "fred_id": "JTSJOL",
        "bls_id": "JTS000000000000000JOL",
        "name": "JOLTS_Openings_Level",
        "description": "Job Openings: Total Nonfarm",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Openings",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Leading",
        "notes": "Demand signal, but noisy (ghost postings)"
    },
    "JTSJOR": {
        "fred_id": "JTSJOR",
        "bls_id": "JTS000000000000000JOR",
        "name": "JOLTS_Openings_Rate",
        "description": "Job Openings Rate: Total Nonfarm",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Openings",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Leading",
        "notes": None
    },
    # Hires
    "JTSHIL": {
        "fred_id": "JTSHIL",
        "bls_id": "JTS000000000000000HIL",
        "name": "JOLTS_Hires_Level",
        "description": "Hires: Total Nonfarm",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Hires",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Leading",
        "notes": "Actual hiring execution"
    },
    "JTSHIR": {
        "fred_id": "JTSHIR",
        "bls_id": "JTS000000000000000HIR",
        "name": "JOLTS_Hires_Rate",
        "description": "Hires Rate: Total Nonfarm",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Hires",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Leading",
        "notes": None
    },
    # Quits (PRIMARY SIGNAL)
    "JTSQUL": {
        "fred_id": "JTSQUL",
        "bls_id": "JTS000000000000000QUL",
        "name": "JOLTS_Quits_Level",
        "description": "Quits: Total Nonfarm",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Quits",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Leading",
        "notes": "PRIMARY LEADING INDICATOR - worker confidence"
    },
    "JTSQUR": {
        "fred_id": "JTSQUR",
        "bls_id": "JTS000000000000000QUR",
        "name": "JOLTS_Quits_Rate",
        "description": "Quits Rate: Total Nonfarm",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Quits",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Leading",
        "notes": "PRIMARY INDICATOR - <2.0% = pre-recessionary"
    },
    # Total Separations
    "JTSTSL": {
        "fred_id": "JTSTSL",
        "bls_id": "JTS000000000000000TSL",
        "name": "JOLTS_Separations_Level",
        "description": "Total Separations: Total Nonfarm",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Separations",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": "Quits + Layoffs + Other"
    },
    "JTSTSR": {
        "fred_id": "JTSTSR",
        "bls_id": "JTS000000000000000TSR",
        "name": "JOLTS_Separations_Rate",
        "description": "Total Separations Rate: Total Nonfarm",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Separations",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": None
    },
    # Layoffs and Discharges
    "JTSLDL": {
        "fred_id": "JTSLDL",
        "bls_id": "JTS000000000000000LDL",
        "name": "JOLTS_Layoffs_Level",
        "description": "Layoffs and Discharges: Total Nonfarm",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Layoffs",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Lagging",
        "notes": "Stress confirmation (employers react late)"
    },
    "JTSLDR": {
        "fred_id": "JTSLDR",
        "bls_id": "JTS000000000000000LDR",
        "name": "JOLTS_Layoffs_Rate",
        "description": "Layoffs and Discharges Rate: Total Nonfarm",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Layoffs",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Lagging",
        "notes": None
    },
}

# JOLTS by Industry (Quits Rate - key cyclical indicator)
JOLTS_BY_INDUSTRY: dict[str, SeriesDefinition] = {
    "JTS1000QUR": {
        "fred_id": "JTS1000QUR",
        "bls_id": None,
        "name": "JOLTS_Quits_Rate_Private",
        "description": "Quits Rate: Total Private",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Industry",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Leading",
        "notes": None
    },
    "JTS2300QUR": {
        "fred_id": "JTS2300QUR",
        "bls_id": None,
        "name": "JOLTS_Quits_Rate_Construction",
        "description": "Quits Rate: Construction",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Industry",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Leading",
        "notes": None
    },
    "JTS3000QUR": {
        "fred_id": "JTS3000QUR",
        "bls_id": None,
        "name": "JOLTS_Quits_Rate_Manufacturing",
        "description": "Quits Rate: Manufacturing",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Industry",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Leading",
        "notes": None
    },
    "JTS4400QUR": {
        "fred_id": "JTS4400QUR",
        "bls_id": None,
        "name": "JOLTS_Quits_Rate_Retail",
        "description": "Quits Rate: Retail Trade",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Industry",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Leading",
        "notes": None
    },
    "JTS540099QUR": {
        "fred_id": "JTS540099QUR",
        "bls_id": None,
        "name": "JOLTS_Quits_Rate_ProfServices",
        "description": "Quits Rate: Professional and Business Services",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Industry",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Leading",
        "notes": None
    },
    "JTS6200QUR": {
        "fred_id": "JTS6200QUR",
        "bls_id": None,
        "name": "JOLTS_Quits_Rate_Healthcare",
        "description": "Quits Rate: Health Care and Social Assistance",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Industry",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": None
    },
    "JTS7000QUR": {
        "fred_id": "JTS7000QUR",
        "bls_id": None,
        "name": "JOLTS_Quits_Rate_LeisureHosp",
        "description": "Quits Rate: Leisure and Hospitality",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Industry",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Leading",
        "notes": "High turnover sector"
    },
    # Job Openings by Industry
    "JTS2300JOL": {
        "fred_id": "JTS2300JOL",
        "bls_id": None,
        "name": "JOLTS_Openings_Construction",
        "description": "Job Openings: Construction",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Industry",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Leading",
        "notes": None
    },
    "JTS3000JOL": {
        "fred_id": "JTS3000JOL",
        "bls_id": None,
        "name": "JOLTS_Openings_Manufacturing",
        "description": "Job Openings: Manufacturing",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Industry",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Leading",
        "notes": None
    },
    "JTS4400JOL": {
        "fred_id": "JTS4400JOL",
        "bls_id": None,
        "name": "JOLTS_Openings_Retail",
        "description": "Job Openings: Retail Trade",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Industry",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Leading",
        "notes": None
    },
    "JTS540099JOL": {
        "fred_id": "JTS540099JOL",
        "bls_id": None,
        "name": "JOLTS_Openings_ProfServices",
        "description": "Job Openings: Professional and Business Services",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Industry",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Leading",
        "notes": None
    },
    "JTS6200JOL": {
        "fred_id": "JTS6200JOL",
        "bls_id": None,
        "name": "JOLTS_Openings_Healthcare",
        "description": "Job Openings: Health Care and Social Assistance",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Industry",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": None
    },
    "JTS7000JOL": {
        "fred_id": "JTS7000JOL",
        "bls_id": None,
        "name": "JOLTS_Openings_LeisureHosp",
        "description": "Job Openings: Leisure and Hospitality",
        "frequency": "M",
        "source": "FRED",
        "category": "FLOWS",
        "subcategory": "JOLTS_Industry",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Lagging",
        "notes": None
    },
}


# =============================================================================
# 8. WAGE DYNAMICS
# =============================================================================

WAGE_SERIES: dict[str, SeriesDefinition] = {
    # Average Hourly Earnings
    "CES0500000003": {
        "fred_id": "CES0500000003",
        "bls_id": "CES0500000003",
        "name": "AHE_Total_Private",
        "description": "Average Hourly Earnings of All Employees: Total Private",
        "frequency": "M",
        "source": "FRED",
        "category": "WAGES",
        "subcategory": "Earnings",
        "seasonal_adj": True,
        "units": "Dollars",
        "lead_lag": "Coincident",
        "notes": "Headline wage growth"
    },
    "CES0500000008": {
        "fred_id": "CES0500000008",
        "bls_id": "CES0500000008",
        "name": "AHE_Production_Nonsupervisory",
        "description": "Average Hourly Earnings of Production and Nonsupervisory Employees",
        "frequency": "M",
        "source": "FRED",
        "category": "WAGES",
        "subcategory": "Earnings",
        "seasonal_adj": True,
        "units": "Dollars",
        "lead_lag": "Coincident",
        "notes": "80% of workforce, less management skew"
    },
    # Real Earnings (inflation-adjusted)
    "LES1252881600Q": {
        "fred_id": "LES1252881600Q",
        "bls_id": None,
        "name": "Real_Median_Weekly_Earnings",
        "description": "Employed Full-Time: Median Usual Weekly Real Earnings",
        "frequency": "Q",
        "source": "FRED",
        "category": "WAGES",
        "subcategory": "Real_Earnings",
        "seasonal_adj": True,
        "units": "2023 Dollars",
        "lead_lag": "Coincident",
        "notes": "Inflation-adjusted purchasing power"
    },
    # Employment Cost Index
    "ECIALLCIV": {
        "fred_id": "ECIALLCIV",
        "bls_id": None,
        "name": "ECI_Total_Compensation",
        "description": "Employment Cost Index: Total Compensation, All Civilian",
        "frequency": "Q",
        "source": "FRED",
        "category": "WAGES",
        "subcategory": "ECI",
        "seasonal_adj": True,
        "units": "Index Dec 2005=100",
        "lead_lag": "Lagging",
        "notes": "Includes benefits, composition-adjusted"
    },
    "ECIWAG": {
        "fred_id": "ECIWAG",
        "bls_id": None,
        "name": "ECI_Wages_Salaries",
        "description": "Employment Cost Index: Wages and Salaries, All Civilian",
        "frequency": "Q",
        "source": "FRED",
        "category": "WAGES",
        "subcategory": "ECI",
        "seasonal_adj": True,
        "units": "Index Dec 2005=100",
        "lead_lag": "Lagging",
        "notes": "Excludes benefits"
    },
    # AHE by Industry
    "CES1000000003": {
        "fred_id": "CES1000000003",
        "bls_id": "CES1000000003",
        "name": "AHE_Mining_Logging",
        "description": "Average Hourly Earnings: Mining and Logging",
        "frequency": "M",
        "source": "FRED",
        "category": "WAGES",
        "subcategory": "Industry_Earnings",
        "seasonal_adj": True,
        "units": "Dollars",
        "lead_lag": "Coincident",
        "notes": None
    },
    "CES2000000003": {
        "fred_id": "CES2000000003",
        "bls_id": "CES2000000003",
        "name": "AHE_Construction",
        "description": "Average Hourly Earnings: Construction",
        "frequency": "M",
        "source": "FRED",
        "category": "WAGES",
        "subcategory": "Industry_Earnings",
        "seasonal_adj": True,
        "units": "Dollars",
        "lead_lag": "Coincident",
        "notes": None
    },
    "CES3000000003": {
        "fred_id": "CES3000000003",
        "bls_id": "CES3000000003",
        "name": "AHE_Manufacturing",
        "description": "Average Hourly Earnings: Manufacturing",
        "frequency": "M",
        "source": "FRED",
        "category": "WAGES",
        "subcategory": "Industry_Earnings",
        "seasonal_adj": True,
        "units": "Dollars",
        "lead_lag": "Coincident",
        "notes": None
    },
    "CES4200000003": {
        "fred_id": "CES4200000003",
        "bls_id": "CES4200000003",
        "name": "AHE_Retail_Trade",
        "description": "Average Hourly Earnings: Retail Trade",
        "frequency": "M",
        "source": "FRED",
        "category": "WAGES",
        "subcategory": "Industry_Earnings",
        "seasonal_adj": True,
        "units": "Dollars",
        "lead_lag": "Coincident",
        "notes": None
    },
    "CES5000000003": {
        "fred_id": "CES5000000003",
        "bls_id": "CES5000000003",
        "name": "AHE_Information",
        "description": "Average Hourly Earnings: Information",
        "frequency": "M",
        "source": "FRED",
        "category": "WAGES",
        "subcategory": "Industry_Earnings",
        "seasonal_adj": True,
        "units": "Dollars",
        "lead_lag": "Coincident",
        "notes": "Tech sector wages"
    },
    "CES5500000003": {
        "fred_id": "CES5500000003",
        "bls_id": "CES5500000003",
        "name": "AHE_Financial_Activities",
        "description": "Average Hourly Earnings: Financial Activities",
        "frequency": "M",
        "source": "FRED",
        "category": "WAGES",
        "subcategory": "Industry_Earnings",
        "seasonal_adj": True,
        "units": "Dollars",
        "lead_lag": "Coincident",
        "notes": None
    },
    "CES6000000003": {
        "fred_id": "CES6000000003",
        "bls_id": "CES6000000003",
        "name": "AHE_Prof_Business_Services",
        "description": "Average Hourly Earnings: Professional and Business Services",
        "frequency": "M",
        "source": "FRED",
        "category": "WAGES",
        "subcategory": "Industry_Earnings",
        "seasonal_adj": True,
        "units": "Dollars",
        "lead_lag": "Coincident",
        "notes": None
    },
    "CES6500000003": {
        "fred_id": "CES6500000003",
        "bls_id": "CES6500000003",
        "name": "AHE_Education_Health",
        "description": "Average Hourly Earnings: Education and Health Services",
        "frequency": "M",
        "source": "FRED",
        "category": "WAGES",
        "subcategory": "Industry_Earnings",
        "seasonal_adj": True,
        "units": "Dollars",
        "lead_lag": "Coincident",
        "notes": None
    },
    "CES7000000003": {
        "fred_id": "CES7000000003",
        "bls_id": "CES7000000003",
        "name": "AHE_Leisure_Hospitality",
        "description": "Average Hourly Earnings: Leisure and Hospitality",
        "frequency": "M",
        "source": "FRED",
        "category": "WAGES",
        "subcategory": "Industry_Earnings",
        "seasonal_adj": True,
        "units": "Dollars",
        "lead_lag": "Coincident",
        "notes": "Lowest-wage major sector"
    },
}

# Atlanta Fed Wage Growth Tracker (special handling - web scrape or direct download)
ATLANTA_FED_WAGE_TRACKER: dict[str, SeriesDefinition] = {
    "WAGE_GROWTH_OVERALL": {
        "fred_id": None,
        "bls_id": None,
        "name": "AtlFed_Wage_Growth_Overall",
        "description": "Atlanta Fed Wage Growth Tracker: Overall Median",
        "frequency": "M",
        "source": "ATLANTA_FED",
        "category": "WAGES",
        "subcategory": "Wage_Growth_Tracker",
        "seasonal_adj": True,
        "units": "Percent YoY",
        "lead_lag": "Coincident",
        "notes": "Median wage growth from matched CPS sample"
    },
    "WAGE_GROWTH_SWITCHERS": {
        "fred_id": None,
        "bls_id": None,
        "name": "AtlFed_Wage_Growth_Switchers",
        "description": "Atlanta Fed Wage Growth Tracker: Job Switchers",
        "frequency": "M",
        "source": "ATLANTA_FED",
        "category": "WAGES",
        "subcategory": "Wage_Growth_Tracker",
        "seasonal_adj": True,
        "units": "Percent YoY",
        "lead_lag": "Leading",
        "notes": "CRITICAL - job hopper premium indicator"
    },
    "WAGE_GROWTH_STAYERS": {
        "fred_id": None,
        "bls_id": None,
        "name": "AtlFed_Wage_Growth_Stayers",
        "description": "Atlanta Fed Wage Growth Tracker: Job Stayers",
        "frequency": "M",
        "source": "ATLANTA_FED",
        "category": "WAGES",
        "subcategory": "Wage_Growth_Tracker",
        "seasonal_adj": True,
        "units": "Percent YoY",
        "lead_lag": "Lagging",
        "notes": "Inertia component of wage growth"
    },
    "WAGE_GROWTH_BOTTOM_QUARTILE": {
        "fred_id": None,
        "bls_id": None,
        "name": "AtlFed_Wage_Growth_Bottom25",
        "description": "Atlanta Fed Wage Growth Tracker: Bottom Wage Quartile",
        "frequency": "M",
        "source": "ATLANTA_FED",
        "category": "WAGES",
        "subcategory": "Wage_Growth_Tracker",
        "seasonal_adj": True,
        "units": "Percent YoY",
        "lead_lag": "Coincident",
        "notes": "Low-wage worker wage growth"
    },
    "WAGE_GROWTH_TOP_QUARTILE": {
        "fred_id": None,
        "bls_id": None,
        "name": "AtlFed_Wage_Growth_Top25",
        "description": "Atlanta Fed Wage Growth Tracker: Top Wage Quartile",
        "frequency": "M",
        "source": "ATLANTA_FED",
        "category": "WAGES",
        "subcategory": "Wage_Growth_Tracker",
        "seasonal_adj": True,
        "units": "Percent YoY",
        "lead_lag": "Coincident",
        "notes": "High-wage worker wage growth"
    },
    # Age cuts
    "WAGE_GROWTH_16_24": {
        "fred_id": None,
        "bls_id": None,
        "name": "AtlFed_Wage_Growth_16_24",
        "description": "Atlanta Fed Wage Growth Tracker: Age 16-24",
        "frequency": "M",
        "source": "ATLANTA_FED",
        "category": "WAGES",
        "subcategory": "Wage_Growth_Tracker",
        "seasonal_adj": True,
        "units": "Percent YoY",
        "lead_lag": "Coincident",
        "notes": None
    },
    "WAGE_GROWTH_25_54": {
        "fred_id": None,
        "bls_id": None,
        "name": "AtlFed_Wage_Growth_25_54",
        "description": "Atlanta Fed Wage Growth Tracker: Age 25-54",
        "frequency": "M",
        "source": "ATLANTA_FED",
        "category": "WAGES",
        "subcategory": "Wage_Growth_Tracker",
        "seasonal_adj": True,
        "units": "Percent YoY",
        "lead_lag": "Coincident",
        "notes": None
    },
    "WAGE_GROWTH_55_PLUS": {
        "fred_id": None,
        "bls_id": None,
        "name": "AtlFed_Wage_Growth_55_Plus",
        "description": "Atlanta Fed Wage Growth Tracker: Age 55+",
        "frequency": "M",
        "source": "ATLANTA_FED",
        "category": "WAGES",
        "subcategory": "Wage_Growth_Tracker",
        "seasonal_adj": True,
        "units": "Percent YoY",
        "lead_lag": "Coincident",
        "notes": None
    },
    # Education cuts
    "WAGE_GROWTH_HS_OR_LESS": {
        "fred_id": None,
        "bls_id": None,
        "name": "AtlFed_Wage_Growth_HS_or_Less",
        "description": "Atlanta Fed Wage Growth Tracker: High School or Less",
        "frequency": "M",
        "source": "ATLANTA_FED",
        "category": "WAGES",
        "subcategory": "Wage_Growth_Tracker",
        "seasonal_adj": True,
        "units": "Percent YoY",
        "lead_lag": "Coincident",
        "notes": None
    },
    "WAGE_GROWTH_SOME_COLLEGE": {
        "fred_id": None,
        "bls_id": None,
        "name": "AtlFed_Wage_Growth_Some_College",
        "description": "Atlanta Fed Wage Growth Tracker: Some College",
        "frequency": "M",
        "source": "ATLANTA_FED",
        "category": "WAGES",
        "subcategory": "Wage_Growth_Tracker",
        "seasonal_adj": True,
        "units": "Percent YoY",
        "lead_lag": "Coincident",
        "notes": None
    },
    "WAGE_GROWTH_BACHELORS_PLUS": {
        "fred_id": None,
        "bls_id": None,
        "name": "AtlFed_Wage_Growth_Bachelors_Plus",
        "description": "Atlanta Fed Wage Growth Tracker: Bachelor's Degree or Higher",
        "frequency": "M",
        "source": "ATLANTA_FED",
        "category": "WAGES",
        "subcategory": "Wage_Growth_Tracker",
        "seasonal_adj": True,
        "units": "Percent YoY",
        "lead_lag": "Coincident",
        "notes": None
    },
    # Industry cuts
    "WAGE_GROWTH_MFG": {
        "fred_id": None,
        "bls_id": None,
        "name": "AtlFed_Wage_Growth_Manufacturing",
        "description": "Atlanta Fed Wage Growth Tracker: Manufacturing",
        "frequency": "M",
        "source": "ATLANTA_FED",
        "category": "WAGES",
        "subcategory": "Wage_Growth_Tracker",
        "seasonal_adj": True,
        "units": "Percent YoY",
        "lead_lag": "Coincident",
        "notes": None
    },
    "WAGE_GROWTH_RETAIL": {
        "fred_id": None,
        "bls_id": None,
        "name": "AtlFed_Wage_Growth_Retail",
        "description": "Atlanta Fed Wage Growth Tracker: Retail Trade",
        "frequency": "M",
        "source": "ATLANTA_FED",
        "category": "WAGES",
        "subcategory": "Wage_Growth_Tracker",
        "seasonal_adj": True,
        "units": "Percent YoY",
        "lead_lag": "Coincident",
        "notes": None
    },
    "WAGE_GROWTH_PROF_SERVICES": {
        "fred_id": None,
        "bls_id": None,
        "name": "AtlFed_Wage_Growth_ProfServices",
        "description": "Atlanta Fed Wage Growth Tracker: Professional and Business Services",
        "frequency": "M",
        "source": "ATLANTA_FED",
        "category": "WAGES",
        "subcategory": "Wage_Growth_Tracker",
        "seasonal_adj": True,
        "units": "Percent YoY",
        "lead_lag": "Coincident",
        "notes": None
    },
    "WAGE_GROWTH_LEISURE_HOSP": {
        "fred_id": None,
        "bls_id": None,
        "name": "AtlFed_Wage_Growth_LeisureHosp",
        "description": "Atlanta Fed Wage Growth Tracker: Leisure and Hospitality",
        "frequency": "M",
        "source": "ATLANTA_FED",
        "category": "WAGES",
        "subcategory": "Wage_Growth_Tracker",
        "seasonal_adj": True,
        "units": "Percent YoY",
        "lead_lag": "Coincident",
        "notes": None
    },
}


# =============================================================================
# 9. HOURS WORKED
# =============================================================================

HOURS_SERIES: dict[str, SeriesDefinition] = {
    # Average Weekly Hours
    "AWHAETP": {
        "fred_id": "AWHAETP",
        "bls_id": "CES0500000002",
        "name": "Avg_Weekly_Hours_Total_Private",
        "description": "Average Weekly Hours of All Employees: Total Private",
        "frequency": "M",
        "source": "FRED",
        "category": "HOURS",
        "subcategory": "Weekly_Hours",
        "seasonal_adj": True,
        "units": "Hours",
        "lead_lag": "Leading",
        "notes": "Leading indicator - employers cut hours before headcount"
    },
    "AWHMAN": {
        "fred_id": "AWHMAN",
        "bls_id": "CES3000000002",
        "name": "Avg_Weekly_Hours_Manufacturing",
        "description": "Average Weekly Hours of Production Workers: Manufacturing",
        "frequency": "M",
        "source": "FRED",
        "category": "HOURS",
        "subcategory": "Weekly_Hours",
        "seasonal_adj": True,
        "units": "Hours",
        "lead_lag": "Leading",
        "notes": "LEADING INDICATOR - leads IP by 1-3 months"
    },
    "AWOTMAN": {
        "fred_id": "AWOTMAN",
        "bls_id": "CES3000000007",
        "name": "Avg_Weekly_Overtime_Hours_Manufacturing",
        "description": "Average Weekly Overtime Hours of Production Workers: Manufacturing",
        "frequency": "M",
        "source": "FRED",
        "category": "HOURS",
        "subcategory": "Weekly_Hours",
        "seasonal_adj": True,
        "units": "Hours",
        "lead_lag": "Leading",
        "notes": "Overtime cut first when demand weakens"
    },
    # Aggregate Weekly Hours Index
    "AWHI": {
        "fred_id": "AWHI",
        "bls_id": None,
        "name": "Aggregate_Weekly_Hours_Index",
        "description": "Indexes of Aggregate Weekly Hours: Total Private",
        "frequency": "M",
        "source": "FRED",
        "category": "HOURS",
        "subcategory": "Aggregate_Hours",
        "seasonal_adj": True,
        "units": "Index 2017=100",
        "lead_lag": "Leading",
        "notes": "Total labor input measure"
    },
    # Average Weekly Hours by Industry
    "CES2000000002": {
        "fred_id": "CES2000000002",
        "bls_id": "CES2000000002",
        "name": "Avg_Weekly_Hours_Construction",
        "description": "Average Weekly Hours: Construction",
        "frequency": "M",
        "source": "FRED",
        "category": "HOURS",
        "subcategory": "Industry_Hours",
        "seasonal_adj": True,
        "units": "Hours",
        "lead_lag": "Leading",
        "notes": None
    },
    "CES4200000002": {
        "fred_id": "CES4200000002",
        "bls_id": "CES4200000002",
        "name": "Avg_Weekly_Hours_Retail",
        "description": "Average Weekly Hours: Retail Trade",
        "frequency": "M",
        "source": "FRED",
        "category": "HOURS",
        "subcategory": "Industry_Hours",
        "seasonal_adj": True,
        "units": "Hours",
        "lead_lag": "Coincident",
        "notes": None
    },
}


# =============================================================================
# 10. UNEMPLOYMENT DECOMPOSITION
# =============================================================================

UNEMPLOYMENT_DECOMPOSITION: dict[str, SeriesDefinition] = {
    # By Duration
    "UEMPLT5": {
        "fred_id": "UEMPLT5",
        "bls_id": "LNS13008396",
        "name": "Unemp_Less_Than_5_Weeks",
        "description": "Unemployed Less Than 5 Weeks",
        "frequency": "M",
        "source": "FRED",
        "category": "UNEMPLOYMENT",
        "subcategory": "Duration",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Leading",
        "notes": "New entrants to unemployment, frictional"
    },
    "UEMP5TO14": {
        "fred_id": "UEMP5TO14",
        "bls_id": "LNS13008516",
        "name": "Unemp_5_to_14_Weeks",
        "description": "Unemployed 5 to 14 Weeks",
        "frequency": "M",
        "source": "FRED",
        "category": "UNEMPLOYMENT",
        "subcategory": "Duration",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": None
    },
    "UEMP15T26": {
        "fred_id": "UEMP15T26",
        "bls_id": "LNS13008636",
        "name": "Unemp_15_to_26_Weeks",
        "description": "Unemployed 15 to 26 Weeks",
        "frequency": "M",
        "source": "FRED",
        "category": "UNEMPLOYMENT",
        "subcategory": "Duration",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": "Extended search duration"
    },
    "UEMP27OV": {
        "fred_id": "UEMP27OV",
        "bls_id": "LNS13008756",
        "name": "Unemp_27_Weeks_Plus",
        "description": "Unemployed 27 Weeks and Over",
        "frequency": "M",
        "source": "FRED",
        "category": "UNEMPLOYMENT",
        "subcategory": "Duration",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Lagging",
        "notes": "STRUCTURAL FRAGILITY - skill erosion, employer bias"
    },
    "UNEMPLOY": {
        "fred_id": "UNEMPLOY",
        "bls_id": "LNS13000000",
        "name": "Unemp_Total_Level",
        "description": "Total Unemployed",
        "frequency": "M",
        "source": "FRED",
        "category": "UNEMPLOYMENT",
        "subcategory": "Level",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Lagging",
        "notes": None
    },
    # Median Duration
    "UEMPMED": {
        "fred_id": "UEMPMED",
        "bls_id": "LNS13008275",
        "name": "Unemp_Median_Duration",
        "description": "Median Duration of Unemployment",
        "frequency": "M",
        "source": "FRED",
        "category": "UNEMPLOYMENT",
        "subcategory": "Duration",
        "seasonal_adj": True,
        "units": "Weeks",
        "lead_lag": "Lagging",
        "notes": "Central tendency of duration"
    },
    "UEMPMEAN": {
        "fred_id": "UEMPMEAN",
        "bls_id": "LNS13008276",
        "name": "Unemp_Mean_Duration",
        "description": "Average (Mean) Duration of Unemployment",
        "frequency": "M",
        "source": "FRED",
        "category": "UNEMPLOYMENT",
        "subcategory": "Duration",
        "seasonal_adj": True,
        "units": "Weeks",
        "lead_lag": "Lagging",
        "notes": "Skewed by long-term unemployed"
    },
    # By Reason
    "LNS13023621": {
        "fred_id": "LNS13023621",
        "bls_id": "LNS13023621",
        "name": "Unemp_Job_Losers",
        "description": "Unemployed: Job Losers and Persons Who Completed Temporary Jobs",
        "frequency": "M",
        "source": "FRED",
        "category": "UNEMPLOYMENT",
        "subcategory": "Reason",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": "Involuntary separations"
    },
    "LNS13023705": {
        "fred_id": "LNS13023705",
        "bls_id": "LNS13023705",
        "name": "Unemp_Job_Leavers",
        "description": "Unemployed: Job Leavers",
        "frequency": "M",
        "source": "FRED",
        "category": "UNEMPLOYMENT",
        "subcategory": "Reason",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Leading",
        "notes": "Voluntary quits into unemployment - confidence signal"
    },
    "LNS13023557": {
        "fred_id": "LNS13023557",
        "bls_id": "LNS13023557",
        "name": "Unemp_Reentrants",
        "description": "Unemployed: Reentrants to Labor Force",
        "frequency": "M",
        "source": "FRED",
        "category": "UNEMPLOYMENT",
        "subcategory": "Reason",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Lagging",
        "notes": None
    },
    "LNS13023569": {
        "fred_id": "LNS13023569",
        "bls_id": "LNS13023569",
        "name": "Unemp_New_Entrants",
        "description": "Unemployed: New Entrants to Labor Force",
        "frequency": "M",
        "source": "FRED",
        "category": "UNEMPLOYMENT",
        "subcategory": "Reason",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Neutral",
        "notes": "First-time job seekers"
    },
}


# =============================================================================
# 11. JOBLESS CLAIMS (WEEKLY)
# =============================================================================

CLAIMS_SERIES: dict[str, SeriesDefinition] = {
    "ICSA": {
        "fred_id": "ICSA",
        "bls_id": None,
        "name": "Initial_Claims",
        "description": "Initial Claims for Unemployment Insurance",
        "frequency": "W",
        "source": "FRED",
        "category": "CLAIMS",
        "subcategory": "Initial",
        "seasonal_adj": True,
        "units": "Persons",
        "lead_lag": "Leading",
        "notes": "Highest-frequency stress gauge"
    },
    "IC4WSA": {
        "fred_id": "IC4WSA",
        "bls_id": None,
        "name": "Initial_Claims_4WMA",
        "description": "4-Week Moving Average of Initial Claims",
        "frequency": "W",
        "source": "FRED",
        "category": "CLAIMS",
        "subcategory": "Initial",
        "seasonal_adj": True,
        "units": "Persons",
        "lead_lag": "Leading",
        "notes": "Smoothed initial claims"
    },
    "CCSA": {
        "fred_id": "CCSA",
        "bls_id": None,
        "name": "Continued_Claims",
        "description": "Continued Claims (Insured Unemployment)",
        "frequency": "W",
        "source": "FRED",
        "category": "CLAIMS",
        "subcategory": "Continued",
        "seasonal_adj": True,
        "units": "Persons",
        "lead_lag": "Coincident",
        "notes": "Labor market slack"
    },
    "IURSA": {
        "fred_id": "IURSA",
        "bls_id": None,
        "name": "Insured_Unemployment_Rate",
        "description": "Insured Unemployment Rate",
        "frequency": "W",
        "source": "FRED",
        "category": "CLAIMS",
        "subcategory": "Rate",
        "seasonal_adj": True,
        "units": "Percent",
        "lead_lag": "Coincident",
        "notes": "Claims normalized to covered employment"
    },
}


# =============================================================================
# 12. LEADING/REAL-TIME INDICATORS
# =============================================================================

LEADING_INDICATORS: dict[str, SeriesDefinition] = {
    # Indeed Job Postings (Real-time)
    "IHLIDXUS": {
        "fred_id": "IHLIDXUS",
        "bls_id": None,
        "name": "Indeed_Job_Postings_US",
        "description": "Indeed Job Postings Index: United States",
        "frequency": "D",
        "source": "FRED",
        "category": "LEADING",
        "subcategory": "Job_Postings",
        "seasonal_adj": True,
        "units": "Index Feb 1 2020=100",
        "lead_lag": "Leading",
        "notes": "Real-time job postings, daily frequency"
    },
    # Productivity
    "OPHNFB": {
        "fred_id": "OPHNFB",
        "bls_id": None,
        "name": "Nonfarm_Labor_Productivity",
        "description": "Nonfarm Business Sector: Labor Productivity (Output Per Hour)",
        "frequency": "Q",
        "source": "FRED",
        "category": "PRODUCTIVITY",
        "subcategory": None,
        "seasonal_adj": True,
        "units": "Index 2017=100",
        "lead_lag": "Lagging",
        "notes": None
    },
    "ULCNFB": {
        "fred_id": "ULCNFB",
        "bls_id": None,
        "name": "Unit_Labor_Costs",
        "description": "Nonfarm Business Sector: Unit Labor Cost",
        "frequency": "Q",
        "source": "FRED",
        "category": "PRODUCTIVITY",
        "subcategory": None,
        "seasonal_adj": True,
        "units": "Index 2017=100",
        "lead_lag": "Lagging",
        "notes": "Compensation per unit output - margin pressure"
    },
}


# =============================================================================
# 13. LABOR FORCE LEVELS (for computing shares)
# =============================================================================

LABOR_FORCE_LEVELS: dict[str, SeriesDefinition] = {
    "CLF16OV": {
        "fred_id": "CLF16OV",
        "bls_id": "LNS11000000",
        "name": "Civilian_Labor_Force",
        "description": "Civilian Labor Force Level",
        "frequency": "M",
        "source": "FRED",
        "category": "LABOR_FORCE",
        "subcategory": "Level",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Structural",
        "notes": None
    },
    "CE16OV": {
        "fred_id": "CE16OV",
        "bls_id": "LNS12000000",
        "name": "Civilian_Employment",
        "description": "Civilian Employment Level",
        "frequency": "M",
        "source": "FRED",
        "category": "LABOR_FORCE",
        "subcategory": "Level",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": None
    },
    # Part-time
    "LNS12032194": {
        "fred_id": "LNS12032194",
        "bls_id": "LNS12032194",
        "name": "Part_Time_Econ_Reasons",
        "description": "Part-Time Workers for Economic Reasons",
        "frequency": "M",
        "source": "FRED",
        "category": "LABOR_FORCE",
        "subcategory": "Part_Time",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": "Underemployment - want full-time but can't find it"
    },
    "LNS12600000": {
        "fred_id": "LNS12600000",
        "bls_id": "LNS12600000",
        "name": "Part_Time_Total",
        "description": "Part-Time Employed Total",
        "frequency": "M",
        "source": "FRED",
        "category": "LABOR_FORCE",
        "subcategory": "Part_Time",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": None
    },
    "LNS12500000": {
        "fred_id": "LNS12500000",
        "bls_id": "LNS12500000",
        "name": "Full_Time_Total",
        "description": "Full-Time Employed Total",
        "frequency": "M",
        "source": "FRED",
        "category": "LABOR_FORCE",
        "subcategory": "Full_Time",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": None
    },
    # Multiple job holders
    "LNS12026620": {
        "fred_id": "LNS12026620",
        "bls_id": "LNS12026620",
        "name": "Multiple_Job_Holders",
        "description": "Multiple Jobholders Total",
        "frequency": "M",
        "source": "FRED",
        "category": "LABOR_FORCE",
        "subcategory": "Multiple_Jobs",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Coincident",
        "notes": "Financial stress indicator"
    },
    # Not in labor force
    "LNS15026639": {
        "fred_id": "LNS15026639",
        "bls_id": "LNS15026639",
        "name": "NILF_Want_Job",
        "description": "Not in Labor Force, Want a Job Now",
        "frequency": "M",
        "source": "FRED",
        "category": "LABOR_FORCE",
        "subcategory": "NILF",
        "seasonal_adj": True,
        "units": "Thousands",
        "lead_lag": "Lagging",
        "notes": "Discouraged and marginally attached"
    },
}


# =============================================================================
# MASTER REGISTRY - ALL SERIES COMBINED
# =============================================================================

def get_all_series() -> dict[str, SeriesDefinition]:
    """Return all series definitions combined into a single dictionary."""
    all_series = {}
    all_series.update(HEADLINE_SERIES)
    all_series.update(UNEMPLOYMENT_BY_AGE)
    all_series.update(UNEMPLOYMENT_BY_EDUCATION)
    all_series.update(UNEMPLOYMENT_BY_RACE)
    all_series.update(UNEMPLOYMENT_BY_GENDER)
    all_series.update(LFPR_BY_AGE)
    all_series.update(LFPR_BY_GENDER)
    all_series.update(LFPR_BY_RACE)
    all_series.update(EPOP_BY_AGE)
    all_series.update(EPOP_BY_GENDER)
    all_series.update(EPOP_BY_RACE)
    all_series.update(STATE_UNEMPLOYMENT)
    all_series.update(EMPLOYMENT_BY_INDUSTRY)
    all_series.update(JOLTS_TOTAL)
    all_series.update(JOLTS_BY_INDUSTRY)
    all_series.update(WAGE_SERIES)
    all_series.update(ATLANTA_FED_WAGE_TRACKER)
    all_series.update(HOURS_SERIES)
    all_series.update(UNEMPLOYMENT_DECOMPOSITION)
    all_series.update(CLAIMS_SERIES)
    all_series.update(LEADING_INDICATORS)
    all_series.update(LABOR_FORCE_LEVELS)
    return all_series


def get_fred_series() -> dict[str, str]:
    """Return mapping of FRED ID to internal name for all FRED-available series."""
    all_series = get_all_series()
    return {
        series["fred_id"]: series["name"]
        for series in all_series.values()
        if series.get("fred_id")
    }


def get_series_by_category(category: str) -> dict[str, SeriesDefinition]:
    """Return all series in a given category."""
    all_series = get_all_series()
    return {
        key: series
        for key, series in all_series.items()
        if series.get("category") == category
    }


def get_leading_indicators() -> dict[str, SeriesDefinition]:
    """Return all series marked as leading indicators."""
    all_series = get_all_series()
    return {
        key: series
        for key, series in all_series.items()
        if series.get("lead_lag") == "Leading"
    }


def count_series() -> dict[str, int]:
    """Return count of series by category."""
    all_series = get_all_series()
    counts: dict[str, int] = {}
    for series in all_series.values():
        cat = series.get("category", "UNKNOWN")
        counts[cat] = counts.get(cat, 0) + 1
    return counts


if __name__ == "__main__":
    # Print summary statistics
    all_series = get_all_series()
    print(f"\nTotal series defined: {len(all_series)}")
    print("\nSeries by category:")
    for cat, count in sorted(count_series().items()):
        print(f"  {cat}: {count}")

    fred_series = get_fred_series()
    print(f"\nFRED-available series: {len(fred_series)}")

    leading = get_leading_indicators()
    print(f"Leading indicators: {len(leading)}")
