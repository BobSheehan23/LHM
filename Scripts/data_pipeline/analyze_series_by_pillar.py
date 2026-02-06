"""
LIGHTHOUSE MACRO - Series Count by Pillar Analysis
===================================================
Counts all individual economic series tracked by the Lighthouse pipeline,
broken down by the 12-pillar framework.

Sources analyzed:
- lighthouse/config.py (FRED_CURATED, BLS_SERIES, BEA_TABLES, NYFED, OFR)
- collect/labor_series_registry.py (197 labor series)
- collect/fred_extended.py (35 additional FRED series)
- collect/fred.py (core FRED series)
- lighthouse/market_fetchers.py (SPX technicals, AAII, VIX)
- lighthouse/breadth_fetcher.py (13 breadth metrics)
- FRED category auto-discovery (15 categories x ~50)

Usage:
    python analyze_series_by_pillar.py [--db /path/to/Lighthouse_Master.db]

If --db is provided, counts directly from the database.
Otherwise, counts from the pipeline configuration files.
"""

import argparse
import sqlite3
import sys
from pathlib import Path


def count_from_config():
    """Count series from pipeline configuration (no DB needed)."""

    # ================================================================
    # P1: LABOR (238 series)
    # Sources: labor_series_registry.py + FRED curated + BLS
    # ================================================================
    P1_LABOR = {
        # --- labor_series_registry.py (197 unique) ---
        # HEADLINE (5)
        "PAYEMS", "UNRATE", "CIVPART", "EMRATIO", "U6RATE",
        # UNEMPLOYMENT_BY_AGE (8)
        "LNS14000012", "LNS14000036", "LNS14024887", "LNS14000060",
        "LNS14000089", "LNS14000091", "LNS14000093", "LNS14024230",
        # UNEMPLOYMENT_BY_EDUCATION (4)
        "LNS14027659", "LNS14027660", "LNS14027689", "LNS14027662",
        # UNEMPLOYMENT_BY_RACE (4)
        "LNS14000003", "LNS14000006", "LNS14000009", "LNU04032183",
        # UNEMPLOYMENT_BY_GENDER (2)
        "LNS14000001", "LNS14000002",
        # LFPR_BY_AGE (4)
        "LNS11300060", "LNS11324230", "LNS11300012", "LNS11300036",
        # LFPR_BY_GENDER (2)
        "LNS11300001", "LNS11300002",
        # LFPR_BY_RACE (3)
        "LNS11300003", "LNS11300006", "LNS11300009",
        # EPOP_BY_AGE (2)
        "LNS12300060", "LNS12300012",
        # EPOP_BY_GENDER (2)
        "LNS12300001", "LNS12300002",
        # EPOP_BY_RACE (3)
        "LNS12300003", "LNS12300006", "LNS12300009",
        # STATE_UNEMPLOYMENT (51)
        *[f"{st}UR" for st in [
            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC"
        ]],
        # EMPLOYMENT_BY_INDUSTRY (24)
        "USPRIV", "USGOOD", "USMINE", "USCONS", "MANEMP", "DMANEMP", "NDMANEMP",
        "SRVPRD", "USTPU", "USWTRADE", "USTRADE", "CES4300000001",
        "USINFO", "USFIRE", "USPBS", "TEMPHELPS", "USEHS", "CES6562000001",
        "USLAH", "USSERV", "USGOVT", "CES9091000001", "CES9092000001", "CES9093000001",
        # JOLTS_TOTAL (10)
        "JTSJOL", "JTSJOR", "JTSHIL", "JTSHIR", "JTSQUL", "JTSQUR",
        "JTSTSL", "JTSTSR", "JTSLDL", "JTSLDR",
        # JOLTS_BY_INDUSTRY (13)
        "JTS1000QUR", "JTS2300QUR", "JTS3000QUR", "JTS4400QUR",
        "JTS540099QUR", "JTS6200QUR", "JTS7000QUR",
        "JTS2300JOL", "JTS3000JOL", "JTS4400JOL",
        "JTS540099JOL", "JTS6200JOL", "JTS7000JOL",
        # WAGE_SERIES (14)
        "CES0500000003", "CES0500000008", "LES1252881600Q",
        "ECIALLCIV", "ECIWAG",
        "CES1000000003", "CES2000000003", "CES3000000003",
        "CES4200000003", "CES5000000003", "CES5500000003",
        "CES6000000003", "CES6500000003", "CES7000000003",
        # ATLANTA_FED_WAGE_TRACKER (15)
        "WAGE_GROWTH_OVERALL", "WAGE_GROWTH_SWITCHERS", "WAGE_GROWTH_STAYERS",
        "WAGE_GROWTH_BOTTOM_QUARTILE", "WAGE_GROWTH_TOP_QUARTILE",
        "WAGE_GROWTH_16_24", "WAGE_GROWTH_25_54", "WAGE_GROWTH_55_PLUS",
        "WAGE_GROWTH_HS_OR_LESS", "WAGE_GROWTH_SOME_COLLEGE", "WAGE_GROWTH_BACHELORS_PLUS",
        "WAGE_GROWTH_MFG", "WAGE_GROWTH_RETAIL", "WAGE_GROWTH_PROF_SERVICES",
        "WAGE_GROWTH_LEISURE_HOSP",
        # HOURS_SERIES (6)
        "AWHAETP", "AWHMAN", "AWOTMAN", "AWHI", "CES2000000002", "CES4200000002",
        # UNEMPLOYMENT_DECOMPOSITION (11)
        "UEMPLT5", "UEMP5TO14", "UEMP15T26", "UEMP27OV", "UNEMPLOY",
        "UEMPMED", "UEMPMEAN",
        "LNS13023621", "LNS13023705", "LNS13023557", "LNS13023569",
        # CLAIMS_SERIES (4)
        "ICSA", "IC4WSA", "CCSA", "IURSA",
        # LEADING_INDICATORS (3)
        "IHLIDXUS", "OPHNFB", "ULCNFB",
        # LABOR_FORCE_LEVELS (7)
        "CLF16OV", "CE16OV", "LNS12032194", "LNS12600000",
        "LNS12500000", "LNS12026620", "LNS15026639",

        # --- FRED curated labor additions ---
        "FRBATLWGT12MMUMHGO", "FRBATLWGT3MMAUMHWGO",
        "FRBATLWGT12MMUMHWGJST", "FRBATLWGT12MMUMHWGJSW",
        "FRBATLWGT12MMUMHWGWD1WP", "FRBATLWGT12MMUMHWGWD76WP",
        "LNS14000013", "LNS14000024", "LNS14000025",
        "LNS11300002", "LNS11300003",
        "U1RATE", "U2RATE",
        "ADPMNUSNERSA", "PRS85006092", "COMPNFB", "HOANBS", "AHETPI",

        # --- BLS sector jobs (stored as BLS_ prefix in DB) ---
        "BLS_CES0000000001", "BLS_CES1000000001", "BLS_CES2000000001",
        "BLS_CES3000000001", "BLS_CES4000000001", "BLS_CES5000000001",
        "BLS_CES5500000001", "BLS_CES6000000001", "BLS_CES6500000001",
        "BLS_CES7000000001", "BLS_CES8000000001", "BLS_CES9000000001",
        "BLS_LNS14000000", "BLS_LNS13327709", "BLS_LNS11300000",
        "BLS_LNS12300000", "BLS_LNS11300060",
        "BLS_JTS000000000000000JOR", "BLS_JTS000000000000000HIR",
        "BLS_JTS000000000000000QUR", "BLS_JTS000000000000000TSR",
        "BLS_CES0500000003", "BLS_CES0500000008",
    }

    # ================================================================
    # P2: PRICES (96 series)
    # ================================================================
    P2_PRICES = {
        # Headline (4)
        "CPIAUCSL", "CPILFESL", "PCEPI", "PCEPILFE",
        # CPI Aggregates (6)
        "CUSR0000SACL1E", "CUSR0000SAS", "CUSR0000SASLE",
        "CUSR0000SASL2RS", "CUSR0000SAC", "CUSR0000SACL1",
        # CPI Services Detail (3)
        "CUSR0000SEMD", "CUSR0000SEMC", "CUSR0000SAS2RS",
        # CPI Goods Detail (5)
        "CPIAPPSL", "CPIUFDSL", "CPIENGSL", "CPIMEDSL", "CUSR0000SACE",
        # Alternative Measures (4)
        "MEDCPIM158SFRBCLE", "CORESTICKM159SFRBATL",
        "COREFLEXCPIM159SFRBATL", "PCETRIM12M159SFRBDAL",
        # PPI Pipeline - config.py (9)
        "PPIFIS", "PPIDSS", "PPIFGS", "PPIFDF", "PPIIDC", "PPIITM",
        "WPSFD4131", "WPUFD49116", "WPSFD41312",
        # PPI Pipeline - master_db.py (4)
        "PPIACO", "PPICPE", "PPICRM", "PPIFES",
        # GDP Deflator (1)
        "GDPDEF",
        # Trimmed Mean (4)
        "TRMMEANCPIM094SFRBCLE", "TRMMEANCPIM157SFRBCLE",
        "PCETRIM1M158SFRBDAL", "PCETRIM6M680SFRBDAL",
        # CPI Shelter (3)
        "CUSR0000SAH1", "CUSR0000SEHA", "CUSR0000SEHC",
        # CPI Food & Energy (6)
        "CUSR0000SAF11", "CUSR0000SEFV", "CUSR0000SAH2",
        "CUSR0000SETB01", "CUSR0000SEHF01", "CUSR0000SEHF02",
        # CPI Medical (2)
        "CUSR0000SAM1", "CUSR0000SAM2",
        # CPI Transport & Vehicles (5)
        "CUSR0000SAS4", "CUSR0000SETA02", "CUSR0000SETA01",
        "CUSR0000SETC", "CUSR0000SETG01",
        # CPI Other (6)
        "CUSR0000SAE1", "CUSR0000SEHE", "CUSR0000SEEB",
        "CUSR0000SEGA", "CUSR0000SEHF", "CUSR0000SS62031",
        # CPI Granular NSA (10)
        "CUSR0000SAE2", "CUSR0000SEEE01", "CUSR0000SEHB",
        "CUUR0000SACL1E", "CUUR0000SAF11", "CUUR0000SAF112",
        "CUUR0000SAF113", "CUUR0000SAS", "CUUR0000SEFJ", "CUUR0000SEFV",
        # PCE Components (5)
        "DGDSRG3M086SBEA", "DSERRG3M086SBEA", "PCEDG", "PCEND", "PCES",
        # PCE Supercore (3)
        "IA001260M", "IA001176M", "JCXFE",
        # Inflation Expectations (6)
        "MICH", "EXPINF1YR", "EXPINF2YR", "EXPINF5YR", "EXPINF10YR", "EXPINF30YR",
        # Import/Export Prices (2)
        "IR", "IQ",
        # BLS Prices (8)
        "BLS_CUUR0000SA0", "BLS_CUUR0000SA0L1E", "BLS_CUUR0000SA0E",
        "BLS_CUUR0000SAH1", "BLS_CUUR0000SAS", "BLS_CUUR0000SAF1",
        "BLS_WPSFD4", "BLS_WPUFD49104",
    }

    # ================================================================
    # P3: GROWTH (47 series)
    # ================================================================
    P3_GROWTH = {
        "GDP", "GDPC1", "INDPRO", "RSAFS", "UMCSENT",
        "IPMAN", "IPMINE", "IPUTIL", "IPBUSEQ", "IPCONGD", "IPDMAT", "IPNMAT",
        "TCU", "MCUMFN",
        "RSXFS", "RSMVPD", "RSFSDP", "RSGASS", "RSBMGESD",
        "RSGCSN", "RSNSR", "RSHPCS", "RSSGHBMS", "RSFHFS", "RSEAS", "RSCCAS", "RSXFSN",
        "DGORDER", "ADXTNO", "NEWORDER", "AMTMNO", "ACDGNO", "ANDENO", "AMNMNO",
        "DSPIC96", "PCEC96", "PNFI", "PRFI",
        "GACDISA066MSFRBNY", "GACDFSA066MSFRBPHI", "CFNAIMA3", "DFXARC1M027SBEA",
        "BSCICP02USM460S", "BSCICP03USM665S",
        "INVCMRMTSPL", "CMRMTSPL", "HOUST1F",
    }

    # ================================================================
    # P4: HOUSING (17 series)
    # ================================================================
    P4_HOUSING = {
        "HOUST", "PERMIT", "CSUSHPINSA", "MSPUS",
        "HSN1F", "MSPNHSUS", "MSACSR", "HOSINVUSM495N",
        "EXHOSLUSM495S", "PERMIT1", "COMPUTSA", "UNDCONTSA",
        "MORTGAGE30US", "MORTGAGE15US", "RHORUSQ156N", "FIXHAI", "HOUST1F",
    }

    # ================================================================
    # P5: CONSUMER (9 series)
    # ================================================================
    P5_CONSUMER = {
        "TOTALSL", "PSAVERT", "TDSP",
        "DRALACBS", "DRSFRMACBS", "DRCCLACBS",
        "CONSUMER", "UMCSENT", "SUBLPDRCSC",
    }

    # ================================================================
    # P6: BUSINESS (23 series)
    # ================================================================
    P6_BUSINESS = {
        "ISRATIO", "MNFCTRIRSA", "RETAILIRSA", "WHLSLRIRSA", "BUSINV", "RETAILIMSA",
        "TOTCI", "BUSLOANS", "REALLN",
        "DRTSCILM", "DRTSCLCC",
        "ALTSALES", "LAUTOSA", "LTOTALNSA", "HTRUCKSSAAR", "TOTALSA", "AISRSA",
        "RAILFRTCARLOADSD11", "TSIFRGHT", "TSITTL", "FRGSHPUSM649NCIS",
        "TRUCKD11", "RAILFRTINTERMODALD11",
    }

    # ================================================================
    # P7: TRADE (12 series)
    # ================================================================
    P7_TRADE = {
        "BOPGSTB", "BOPGTB", "BOPTEXP", "BOPTIMP",
        "IMPGS", "EXPGS", "NETEXP",
        "DTWEXBGS", "DTWEXAFEGS", "DTWEXEMEGS",
        "IR", "IQ",
    }

    # ================================================================
    # P8: GOVERNMENT (13 series)
    # ================================================================
    P8_GOVERNMENT = {
        "GFDEBTN", "GFDEGDQ188S",
        "MTSDS133FMS", "MTSO133FMS", "MTSR133FMS",
        "FYFSD", "FGEXPND", "FGRECPT",
        "W068RCQ027SBEA", "A091RC1Q027SBEA", "A822RL1Q225SBEA",
        "WTREGEN", "THREEFYTP10",
    }

    # ================================================================
    # P9: FINANCIAL (41 series)
    # ================================================================
    P9_FINANCIAL = {
        # Yield Curve (10)
        "FEDFUNDS", "DGS1", "DGS2", "DGS5", "DGS10", "DGS20", "DGS30",
        "DGS1MO", "DGS3MO", "DGS6MO",
        # Spreads (5)
        "T10Y2Y", "T10Y3M", "T10YFF", "T5YFF",
        # Real Rates & Breakevens (5)
        "DFII5", "DFII10", "T5YIFR", "T10YIE", "T5YIE",
        # Credit Spreads (7)
        "BAMLH0A0HYM2", "BAMLC0A0CM",
        "BAMLC0A1CAAAEY", "BAMLC0A2CAAEY", "BAMLC0A3CAEY",
        "BAMLC0A4CBBBEY", "BAMLH0A0HYM2EY",
        # Financial Conditions (4)
        "NFCI", "ANFCI", "STLFSI4", "KCFSI",
        # Volatility & Commodities (2)
        "VIXCLS", "DCOILWTICO",
        # OFR Financial Stress (9)
        "OFR_FSI", "OFR_FSI_Credit", "OFR_FSI_Equity", "OFR_FSI_SafeAssets",
        "OFR_FSI_Funding", "OFR_FSI_Volatility",
        "OFR_FSI_US", "OFR_FSI_AdvancedEcon", "OFR_FSI_EmergingMkts",
    }

    # ================================================================
    # P10: PLUMBING (34 series)
    # ================================================================
    P10_PLUMBING = {
        # Fed Balance Sheet (5)
        "M2SL", "WALCL", "RRPONTSYD", "TOTRESNS", "H41RESPPALDKNWW",
        # Extended (6)
        "WRESBAL", "MMMFFAQ027S", "WRMFSL", "WIMFSL", "SOFR", "EFFR", "OBFR",
        # NY Fed (10)
        "NYFED_SOFR", "NYFED_EFFR", "NYFED_OBFR", "NYFED_TGCR", "NYFED_BGCR",
        "NYFED_SOFR_Volume", "NYFED_EFFR_Volume", "NYFED_OBFR_Volume",
        "NYFED_TGCR_Volume", "NYFED_BGCR_Volume",
        # OFR Funding (12)
        "OFR_SOFR", "OFR_EFFR", "OFR_OBFR", "OFR_TGCR", "OFR_BGCR",
        "OFR_MMF_Total", "OFR_MMF_Repo", "OFR_MMF_RepoFed", "OFR_MMF_Treasury",
        "OFR_PD_Repo", "OFR_PD_RRP", "OFR_PD_RepoTreasury",
    }

    # ================================================================
    # P11: MARKET STRUCTURE (28 series)
    # ================================================================
    P11_MARKET_STRUCTURE = {
        # SPX Technicals (15)
        "SPX_Close", "SPX_Volume",
        "SPX_20d_MA", "SPX_50d_MA", "SPX_200d_MA",
        "SPX_vs_20d_pct", "SPX_vs_50d_pct", "SPX_vs_200d_pct",
        "SPX_20d_slope", "SPX_50d_slope", "SPX_200d_slope",
        "SPX_RoC_21d", "SPX_RoC_63d", "SPX_Z_RoC_63d", "SPX_RSI_14d",
        # Breadth (13)
        "SPX_PCT_ABOVE_20D", "SPX_PCT_ABOVE_50D", "SPX_PCT_ABOVE_200D",
        "SPX_ADVANCES", "SPX_DECLINES", "SPX_AD_LINE", "SPX_AD_RATIO",
        "SPX_NEW_HIGHS", "SPX_NEW_LOWS", "SPX_NET_NEW_HIGHS",
        "SPX_MCCLELLAN_OSC", "SPX_MCCLELLAN_SUM", "SPX_BREADTH_THRUST",
    }

    # ================================================================
    # P12: SENTIMENT (6 series)
    # ================================================================
    P12_SENTIMENT = {
        "VIX_vs_50d_pct", "VIX_percentile_252d",
        "AAII_Bullish", "AAII_Bearish", "AAII_Neutral", "AAII_Bull_Bear_Spread",
    }

    pillars = {
        "P1:  LABOR": P1_LABOR,
        "P2:  PRICES": P2_PRICES,
        "P3:  GROWTH": P3_GROWTH,
        "P4:  HOUSING": P4_HOUSING,
        "P5:  CONSUMER": P5_CONSUMER,
        "P6:  BUSINESS": P6_BUSINESS,
        "P7:  TRADE": P7_TRADE,
        "P8:  GOVERNMENT": P8_GOVERNMENT,
        "P9:  FINANCIAL": P9_FINANCIAL,
        "P10: PLUMBING": P10_PLUMBING,
        "P11: MARKET STRUCTURE": P11_MARKET_STRUCTURE,
        "P12: SENTIMENT": P12_SENTIMENT,
    }

    return pillars


def count_from_db(db_path: str):
    """Count series directly from the Lighthouse Master database."""
    conn = sqlite3.connect(db_path)

    print(f"\nReading from: {db_path}")
    print(f"DB size: {Path(db_path).stat().st_size / 1e6:.1f} MB\n")

    # Total counts
    total_series = conn.execute("SELECT COUNT(*) FROM series_meta").fetchone()[0]
    total_obs = conn.execute("SELECT COUNT(*) FROM observations").fetchone()[0]
    date_range = conn.execute("SELECT MIN(date), MAX(date) FROM observations").fetchone()

    print(f"Total Series: {total_series:,}")
    print(f"Total Observations: {total_obs:,}")
    print(f"Date Range: {date_range[0]} to {date_range[1]}")

    print("\nBy Source:")
    import pandas as pd
    by_source = pd.read_sql(
        "SELECT source, COUNT(*) as series FROM series_meta GROUP BY source ORDER BY series DESC",
        conn,
    )
    print(by_source.to_string(index=False))

    print("\nBy Category:")
    by_cat = pd.read_sql(
        "SELECT category, COUNT(*) as series FROM series_meta GROUP BY category ORDER BY series DESC LIMIT 20",
        conn,
    )
    print(by_cat.to_string(index=False))

    conn.close()
    return None  # DB mode doesn't return pillar breakdown (needs category->pillar mapping)


def main():
    parser = argparse.ArgumentParser(description="Lighthouse Macro Series Count by Pillar")
    parser.add_argument("--db", type=str, help="Path to Lighthouse_Master.db (optional)")
    args = parser.parse_args()

    print("=" * 70)
    print("LIGHTHOUSE MACRO - ECONOMIC SERIES BY PILLAR")
    print("=" * 70)

    if args.db and Path(args.db).exists():
        count_from_db(args.db)
    else:
        pillars = count_from_config()

        print()
        curated_total = 0
        for name, series_set in pillars.items():
            count = len(series_set)
            curated_total += count
            bar = "█" * (count // 3)
            print(f"  {name:30s}  {count:>5}  {bar}")

        print(f"\n  {'TOTAL (explicit/curated)':30s}  {curated_total:>5}")
        print(f"\n  + BEA NIPA tables (9 tables)                    ~225 line items")
        print(f"  + FRED category auto-discovery (15 categories)  ~500-750 series")
        print(f"\n  ESTIMATED DB GRAND TOTAL                       ~{curated_total + 225 + 500}-{curated_total + 225 + 750}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
