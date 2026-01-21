"""
Lighthouse Macro Crypto Fundamentals Engine
============================================
Protocol fundamental analysis with LHM proprietary ratios and verdicts.

Philosophy:
    "Flows > Stocks applies to crypto too. We track protocol revenue flows,
    user acquisition dynamics, and valuation fundamentals systematically."

Key Concepts:
    - Subsidy Score: Token incentives / Revenue (< 0.5 = organic, > 2.0 = ponzi)
    - Float Ratio: Circulating / Total supply (< 0.2 = predatory VC overhang)
    - Capital Efficiency: Volume / TVL (higher = better)
    - Dilution-Adjusted Earnings: Revenue - Token Incentives

Usage:
    from lighthouse_quant.crypto import CryptoFundamentalsEngine

    engine = CryptoFundamentalsEngine()
    report = engine.analyze_protocol('aave')
    watchlist = engine.screen_universe()
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import time

from .token_terminal import TokenTerminalClient


# ==========================================
# CONFIGURATION & THRESHOLDS
# ==========================================

class Verdict(Enum):
    """LHM Investment Verdict"""
    TIER1_ACCUMULATE = "TIER 1 (Accumulate)"
    TIER2_HOLD = "TIER 2 (Hold)"
    NEUTRAL_WATCH = "NEUTRAL (Watch)"
    CAUTION_LOW_FLOAT = "CAUTION (Low Float)"
    AVOID_VAPORWARE = "AVOID (Vaporware)"
    AVOID_PONZI = "AVOID (Unsustainable)"
    AVOID_DEAD = "AVOID (Dead Chain)"
    INSUFFICIENT_DATA = "INSUFFICIENT DATA"


# LHM Thresholds (The Filter)
THRESHOLDS = {
    # Subsidy Assessment
    'subsidy_score_organic': 0.5,      # < 0.5 = organic traction
    'subsidy_score_ponzi': 2.0,        # > 2.0 = unsustainable tokenomics

    # Float Assessment
    'float_ratio_predatory': 0.20,     # < 20% = predatory VC overhang
    'float_ratio_healthy': 0.50,       # > 50% = reasonable float

    # Vaporware Filter
    'min_revenue_for_billion_fdv': 1_000_000,  # Min $1M annual rev if FDV > $1B
    'fdv_threshold': 1_000_000_000,    # $1B FDV threshold

    # Valuation Thresholds (P/E equivalent using P/F with revenue)
    'pe_ratio_cheap': 20,              # < 20 = value territory
    'pe_ratio_fair': 40,               # < 40 = fair value
    'pe_ratio_expensive': 100,         # > 100 = growth premium

    # Activity Thresholds
    'min_dau': 100,                    # Minimum daily active users
    'min_developers': 3,               # Minimum active developers

    # Capital Efficiency
    'capital_turnover_efficient': 0.1, # > 10% daily turnover = efficient
}


# LHM Sector Taxonomy
SECTOR_TAXONOMY = {
    # Layer 1 (Settlement)
    'layer1': {
        'name': 'Layer 1 (Settlement)',
        'description': 'Base layer networks. Security & finality.',
        'key_metric': 'Blockspace Demand (Fees)',
        'examples': ['ethereum', 'solana', 'avalanche', 'near', 'sui']
    },
    # Layer 2 (Scaling)
    'layer2': {
        'name': 'Layer 2 (Scaling)',
        'description': 'Execution bandwidth. High throughput.',
        'key_metric': 'Margins (L2 Fee - L1 Rent)',
        'examples': ['arbitrum', 'optimism', 'base', 'polygon-zkevm', 'starknet']
    },
    # DeFi (Financials)
    'defi_dex': {
        'name': 'DeFi - DEX',
        'description': 'Decentralized exchanges. Trading services.',
        'key_metric': 'Volume / TVL (Capital Efficiency)',
        'examples': ['uniswap', 'curve', 'sushi', 'pancakeswap', 'raydium']
    },
    'defi_lending': {
        'name': 'DeFi - Lending',
        'description': 'Borrowing/lending protocols.',
        'key_metric': 'Revenue / TVL (Utilization)',
        'examples': ['aave', 'compound', 'morpho', 'spark', 'maker']
    },
    'defi_derivatives': {
        'name': 'DeFi - Derivatives',
        'description': 'Perpetuals and options.',
        'key_metric': 'Notional Volume / OI',
        'examples': ['gmx', 'dydx', 'hyperliquid', 'vertex', 'synthetix']
    },
    # Infrastructure
    'infrastructure': {
        'name': 'Infrastructure',
        'description': 'Oracles, indexers, middleware.',
        'key_metric': 'Integrations / Revenue',
        'examples': ['chainlink', 'the-graph', 'pyth']
    },
    # Liquid Staking
    'liquid_staking': {
        'name': 'Liquid Staking',
        'description': 'Staking derivatives.',
        'key_metric': 'Assets Staked / Take Rate',
        'examples': ['lido', 'rocket-pool', 'jito', 'marinade']
    },
    # Stablecoins
    'stablecoins': {
        'name': 'Stablecoin Issuers',
        'description': 'USD-pegged token issuers.',
        'key_metric': 'Outstanding Supply / Revenue',
        'examples': ['circle', 'tether', 'sky']  # MakerDAO = sky now
    },
    # RWA
    'rwa': {
        'name': 'Real World Assets',
        'description': 'Tokenized traditional assets.',
        'key_metric': 'AUM / Yield Spread',
        'examples': ['ondo', 'centrifuge', 'maple']
    },
}


@dataclass
class ProtocolAnalysis:
    """Complete fundamental analysis for a protocol."""
    project_id: str
    name: str
    sector: str
    date: str

    # Market Data
    market_cap: float
    fdv: float
    price: float

    # Financial Metrics
    fees_daily: float
    revenue_daily: float
    token_incentives_daily: float
    earnings_daily: float
    tvl: float
    treasury_net: float

    # Usage Metrics
    dau: int
    mau: int
    transaction_count: int
    active_developers: int

    # Calculated Ratios (LHM Proprietary)
    annualized_fees: float
    annualized_revenue: float
    annualized_incentives: float

    pf_ratio: float
    ps_ratio: float
    pe_ratio: float  # P/E using protocol revenue

    subsidy_score: float
    float_ratio: float
    capital_turnover: float
    dau_mau_ratio: float
    dilution_rate: float

    # LHM Assessment
    verdict: Verdict
    verdict_reasons: List[str]
    red_flags: List[str]

    # Scores (0-100)
    financial_score: int
    usage_score: int
    valuation_score: int
    overall_score: int


class CryptoFundamentalsEngine:
    """
    Lighthouse Macro Crypto Fundamentals Analysis Engine.

    Applies systematic fundamental analysis to crypto protocols using
    Token Terminal data and LHM proprietary ratios.
    """

    def __init__(self, client: TokenTerminalClient = None):
        """
        Initialize the fundamentals engine.

        Args:
            client: TokenTerminalClient instance (creates new if None)
        """
        self.client = client or TokenTerminalClient()
        self.thresholds = THRESHOLDS
        self.sectors = SECTOR_TAXONOMY

    # ==========================================
    # CORE ANALYSIS
    # ==========================================

    def analyze_protocol(self, project_id: str) -> Optional[ProtocolAnalysis]:
        """
        Perform complete fundamental analysis on a protocol.

        Args:
            project_id: Token Terminal project ID

        Returns:
            ProtocolAnalysis object or None if insufficient data
        """
        # Fetch latest metrics
        metrics = self.client.get_latest_metrics(project_id)

        if metrics.empty:
            print(f"No data available for {project_id}")
            return None

        # Extract with safe defaults
        def get_val(key, default=0.0):
            val = metrics.get(key, default)
            return float(val) if pd.notna(val) else default

        # Market Data
        market_cap = get_val('market_cap_circulating')
        fdv = get_val('market_cap_fully_diluted')
        price = get_val('price')

        # Financial (daily values)
        fees_daily = get_val('fees')
        revenue_daily = get_val('revenue')
        token_incentives_daily = get_val('token_incentives')
        earnings_daily = get_val('earnings')
        tvl = get_val('tvl')
        treasury_net = get_val('treasury_net')

        # Usage
        dau = int(get_val('user_dau'))
        mau = int(get_val('user_mau'))
        transaction_count = int(get_val('transaction_count'))
        active_developers = int(get_val('active_developers'))

        # Annualize (multiply daily by 365)
        ann_fees = fees_daily * 365
        ann_revenue = revenue_daily * 365
        ann_incentives = token_incentives_daily * 365

        # Calculate LHM Ratios
        # P/F Ratio (Price to Fees)
        pf_ratio = fdv / ann_fees if ann_fees > 0 else np.inf

        # P/S Ratio (Price to Sales/Revenue)
        ps_ratio = fdv / ann_revenue if ann_revenue > 0 else np.inf

        # P/E Ratio (using protocol revenue as "earnings")
        pe_ratio = fdv / ann_revenue if ann_revenue > 0 else np.inf

        # Subsidy Score: How much are they paying per $1 of revenue?
        subsidy_score = token_incentives_daily / revenue_daily if revenue_daily > 0 else np.inf

        # Float Ratio: How much is actually circulating?
        float_ratio = market_cap / fdv if fdv > 0 else 0

        # Capital Turnover: Volume / TVL (for DEXs primarily)
        trading_volume = get_val('trading_volume')
        capital_turnover = trading_volume / tvl if tvl > 0 else 0

        # DAU/MAU Ratio (stickiness)
        dau_mau_ratio = dau / mau if mau > 0 else 0

        # Dilution Rate: Token incentives as % of revenue
        dilution_rate = (ann_incentives / ann_revenue * 100) if ann_revenue > 0 else np.inf

        # Determine sector
        sector = self._classify_sector(project_id)

        # Get project name
        projects = self.client.get_projects()
        name_match = projects[projects['project_id'] == project_id]
        name = name_match['name'].values[0] if len(name_match) > 0 else project_id

        # Apply verdict logic
        verdict, reasons, red_flags = self._determine_verdict(
            fdv=fdv,
            ann_revenue=ann_revenue,
            subsidy_score=subsidy_score,
            float_ratio=float_ratio,
            pe_ratio=pe_ratio,
            dau=dau,
            active_developers=active_developers,
            sector=sector,
            ann_fees=ann_fees
        )

        # Calculate scores
        financial_score = self._score_financials(ann_revenue, subsidy_score, earnings_daily)
        usage_score = self._score_usage(dau, mau, active_developers)
        valuation_score = self._score_valuation(pe_ratio, pf_ratio, float_ratio)
        overall_score = int((financial_score + usage_score + valuation_score) / 3)

        return ProtocolAnalysis(
            project_id=project_id,
            name=name,
            sector=sector,
            date=str(datetime.now().date()),
            market_cap=market_cap,
            fdv=fdv,
            price=price,
            fees_daily=fees_daily,
            revenue_daily=revenue_daily,
            token_incentives_daily=token_incentives_daily,
            earnings_daily=earnings_daily,
            tvl=tvl,
            treasury_net=treasury_net,
            dau=dau,
            mau=mau,
            transaction_count=transaction_count,
            active_developers=active_developers,
            annualized_fees=ann_fees,
            annualized_revenue=ann_revenue,
            annualized_incentives=ann_incentives,
            pf_ratio=pf_ratio,
            ps_ratio=ps_ratio,
            pe_ratio=pe_ratio,
            subsidy_score=subsidy_score,
            float_ratio=float_ratio,
            capital_turnover=capital_turnover,
            dau_mau_ratio=dau_mau_ratio,
            dilution_rate=dilution_rate,
            verdict=verdict,
            verdict_reasons=reasons,
            red_flags=red_flags,
            financial_score=financial_score,
            usage_score=usage_score,
            valuation_score=valuation_score,
            overall_score=overall_score
        )

    def _classify_sector(self, project_id: str) -> str:
        """Classify project into LHM sector taxonomy."""
        pid_lower = project_id.lower()

        for sector_key, sector_info in self.sectors.items():
            if pid_lower in [ex.lower() for ex in sector_info['examples']]:
                return sector_info['name']

        # Default classification by keywords
        if any(x in pid_lower for x in ['swap', 'dex', 'exchange']):
            return 'DeFi - DEX'
        elif any(x in pid_lower for x in ['lend', 'aave', 'compound', 'borrow']):
            return 'DeFi - Lending'
        elif any(x in pid_lower for x in ['stake', 'lido', 'rocket']):
            return 'Liquid Staking'
        elif any(x in pid_lower for x in ['bridge']):
            return 'Infrastructure'

        return 'Uncategorized'

    def _determine_verdict(
        self,
        fdv: float,
        ann_revenue: float,
        subsidy_score: float,
        float_ratio: float,
        pe_ratio: float,
        dau: int,
        active_developers: int,
        sector: str = None,
        ann_fees: float = 0
    ) -> Tuple[Verdict, List[str], List[str]]:
        """
        Apply LHM verdict logic.

        Returns:
            Tuple of (Verdict, reasons list, red_flags list)
        """
        reasons = []
        red_flags = []

        # L1 chains are infrastructure - judge by fees, not revenue
        # Their "token incentives" are security budget, not marketing spend
        is_l1 = sector and ('Layer 1' in sector or 'L1' in sector.upper())
        is_l2 = sector and ('Layer 2' in sector or 'L2' in sector.upper())

        # Rule 1: The Vaporware Filter
        # For L1/L2, use fees instead of revenue as the threshold
        if is_l1 or is_l2:
            if fdv > self.thresholds['fdv_threshold'] and ann_fees < self.thresholds['min_revenue_for_billion_fdv'] * 10:
                reasons.append(f"FDV ${fdv/1e9:.1f}B but fees only ${ann_fees/1e6:.2f}M")
                return Verdict.AVOID_VAPORWARE, reasons, ["Insufficient fee revenue for valuation"]
        else:
            if fdv > self.thresholds['fdv_threshold'] and ann_revenue < self.thresholds['min_revenue_for_billion_fdv']:
                reasons.append(f"FDV ${fdv/1e9:.1f}B but revenue only ${ann_revenue/1e6:.2f}M")
                return Verdict.AVOID_VAPORWARE, reasons, ["Insufficient revenue for valuation"]

        # Rule 2: The Ponzi Filter
        # L1 chains exempt - their inflation is security budget, not marketing
        if not is_l1 and subsidy_score > self.thresholds['subsidy_score_ponzi']:
            reasons.append(f"Subsidy Score {subsidy_score:.1f}x (paying {subsidy_score:.0f}x revenue in incentives)")
            return Verdict.AVOID_PONZI, reasons, ["Unsustainable token economics"]

        # Rule 3: Dead Protocol Filter
        if active_developers < self.thresholds['min_developers'] and dau < self.thresholds['min_dau']:
            reasons.append(f"Only {active_developers} devs and {dau} daily users")
            return Verdict.AVOID_DEAD, reasons, ["Abandoned protocol"]

        # Rule 4: Predatory Float Warning
        if float_ratio < self.thresholds['float_ratio_predatory']:
            reasons.append(f"Float ratio {float_ratio:.1%} - massive unlock overhang")
            red_flags.append(f"Low float: {float_ratio:.1%}")
            return Verdict.CAUTION_LOW_FLOAT, reasons, red_flags

        # Rule 5: Tier 1 Criteria
        # For L1s, use P/F (price to fees) instead of P/E since they pay out to validators
        if is_l1:
            # L1 specific: strong fee generation, good float, reasonable P/F
            pf_ratio = fdv / ann_fees if ann_fees > 0 else np.inf
            if (pf_ratio < 500 and  # L1s trade at higher multiples
                pf_ratio > 0 and
                float_ratio > self.thresholds['float_ratio_healthy'] and
                dau > 10000):  # Meaningful usage
                reasons.append(f"L1 with P/F {pf_ratio:.0f}x, Float {float_ratio:.0%}, DAU {dau:,}")
                return Verdict.TIER1_ACCUMULATE, reasons, red_flags
            elif (pf_ratio < 1000 and pf_ratio > 0 and float_ratio > 0.30):
                reasons.append(f"L1 with reasonable metrics: P/F {pf_ratio:.0f}x")
                return Verdict.TIER2_HOLD, reasons, red_flags
        elif (pe_ratio < self.thresholds['pe_ratio_fair'] and
            pe_ratio > 0 and
            subsidy_score < self.thresholds['subsidy_score_organic'] and
            float_ratio > self.thresholds['float_ratio_healthy']):
            reasons.append(f"P/E {pe_ratio:.0f}x, Subsidy {subsidy_score:.2f}x, Float {float_ratio:.0%}")
            return Verdict.TIER1_ACCUMULATE, reasons, red_flags

        # Rule 6: Tier 2 Criteria (relaxed)
        if (pe_ratio < self.thresholds['pe_ratio_expensive'] and
            pe_ratio > 0 and
            subsidy_score < 1.0 and
            float_ratio > 0.30):
            reasons.append(f"Decent fundamentals but not Tier 1")
            return Verdict.TIER2_HOLD, reasons, red_flags

        # Collect any remaining red flags
        if subsidy_score > 0.5:
            red_flags.append(f"Elevated subsidy: {subsidy_score:.1f}x")
        if pe_ratio > 100:
            red_flags.append(f"Expensive: P/E {pe_ratio:.0f}x")
        if float_ratio < 0.3:
            red_flags.append(f"Low float: {float_ratio:.0%}")

        reasons.append("Does not meet Tier 1 or Tier 2 criteria")
        return Verdict.NEUTRAL_WATCH, reasons, red_flags

    def _score_financials(self, ann_revenue: float, subsidy_score: float, earnings: float) -> int:
        """Score financial health (0-100)."""
        score = 50  # Base

        # Revenue scale
        if ann_revenue > 100_000_000:
            score += 25
        elif ann_revenue > 10_000_000:
            score += 15
        elif ann_revenue > 1_000_000:
            score += 5
        else:
            score -= 15

        # Subsidy efficiency
        if subsidy_score < 0.2:
            score += 20
        elif subsidy_score < 0.5:
            score += 10
        elif subsidy_score > 2.0:
            score -= 25

        # Profitability
        if earnings > 0:
            score += 15
        elif earnings < -ann_revenue * 0.5:
            score -= 10

        return max(0, min(100, score))

    def _score_usage(self, dau: int, mau: int, developers: int) -> int:
        """Score usage metrics (0-100)."""
        score = 50

        # DAU scale
        if dau > 100_000:
            score += 25
        elif dau > 10_000:
            score += 15
        elif dau > 1_000:
            score += 5
        else:
            score -= 10

        # Stickiness
        stickiness = dau / mau if mau > 0 else 0
        if stickiness > 0.3:
            score += 15
        elif stickiness > 0.15:
            score += 5

        # Development activity
        if developers > 20:
            score += 15
        elif developers > 10:
            score += 10
        elif developers > 5:
            score += 5
        else:
            score -= 10

        return max(0, min(100, score))

    def _score_valuation(self, pe_ratio: float, pf_ratio: float, float_ratio: float) -> int:
        """Score valuation attractiveness (0-100)."""
        score = 50

        # P/E assessment
        if pe_ratio < 20 and pe_ratio > 0:
            score += 25
        elif pe_ratio < 50 and pe_ratio > 0:
            score += 10
        elif pe_ratio > 200:
            score -= 20

        # Float assessment
        if float_ratio > 0.7:
            score += 15
        elif float_ratio > 0.5:
            score += 10
        elif float_ratio < 0.2:
            score -= 20

        return max(0, min(100, score))

    # ==========================================
    # BATCH ANALYSIS & SCREENING
    # ==========================================

    def screen_universe(
        self,
        project_ids: List[str] = None,
        max_projects: int = 50
    ) -> pd.DataFrame:
        """
        Screen multiple protocols and generate comparison report.

        Args:
            project_ids: List of projects to analyze (None = use default watchlist)
            max_projects: Maximum projects to analyze

        Returns:
            DataFrame with all protocols ranked
        """
        if project_ids is None:
            # Default watchlist: major protocols across sectors
            project_ids = [
                # L1
                'ethereum', 'solana', 'avalanche', 'near',
                # L2
                'arbitrum', 'optimism', 'base', 'polygon',
                # DEX
                'uniswap', 'curve', 'pancakeswap', 'raydium',
                # Lending
                'aave', 'compound', 'morpho',
                # Derivatives
                'gmx', 'dydx',
                # Liquid Staking
                'lido', 'rocket-pool', 'jito',
                # Infrastructure
                'chainlink', 'the-graph',
                # Stablecoins
                'sky',  # MakerDAO
            ]

        project_ids = project_ids[:max_projects]
        results = []

        print(f"Analyzing {len(project_ids)} protocols...")
        for i, pid in enumerate(project_ids):
            print(f"  [{i+1}/{len(project_ids)}] {pid}...", end=" ")
            try:
                analysis = self.analyze_protocol(pid)
                if analysis:
                    results.append(self._analysis_to_dict(analysis))
                    print(f"✓ {analysis.verdict.value}")
                else:
                    print("✗ No data")
            except Exception as e:
                print(f"✗ Error: {e}")

        if not results:
            return pd.DataFrame()

        df = pd.DataFrame(results)

        # Sort by overall score descending
        df = df.sort_values('overall_score', ascending=False).reset_index(drop=True)

        return df

    def _analysis_to_dict(self, analysis: ProtocolAnalysis) -> Dict:
        """Convert ProtocolAnalysis to dictionary for DataFrame."""
        return {
            'project_id': analysis.project_id,
            'name': analysis.name,
            'sector': analysis.sector,
            'verdict': analysis.verdict.value,
            'overall_score': analysis.overall_score,
            'financial_score': analysis.financial_score,
            'usage_score': analysis.usage_score,
            'valuation_score': analysis.valuation_score,
            'fdv': analysis.fdv,
            'market_cap': analysis.market_cap,
            'ann_revenue': analysis.annualized_revenue,
            'ann_fees': analysis.annualized_fees,
            'pe_ratio': analysis.pe_ratio,
            'pf_ratio': analysis.pf_ratio,
            'subsidy_score': analysis.subsidy_score,
            'float_ratio': analysis.float_ratio,
            'dau': analysis.dau,
            'active_developers': analysis.active_developers,
            'tvl': analysis.tvl,
            'red_flags': '; '.join(analysis.red_flags) if analysis.red_flags else '',
        }

    def generate_report(
        self,
        project_ids: List[str] = None,
        output_path: str = None
    ) -> str:
        """
        Generate a formatted fundamental analysis report.

        Args:
            project_ids: Projects to analyze
            output_path: CSV output path (optional)

        Returns:
            Formatted report string
        """
        df = self.screen_universe(project_ids)

        if df.empty:
            return "No data available for analysis."

        # Save to CSV if path provided
        if output_path:
            df.to_csv(output_path, index=False)
            print(f"Report saved to {output_path}")

        # Generate text report
        report = []
        report.append("=" * 70)
        report.append("LIGHTHOUSE MACRO CRYPTO FUNDAMENTALS REPORT")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("=" * 70)
        report.append("")

        # Tier 1 picks
        tier1 = df[df['verdict'] == Verdict.TIER1_ACCUMULATE.value]
        if not tier1.empty:
            report.append("TIER 1 - ACCUMULATE")
            report.append("-" * 40)
            for _, row in tier1.iterrows():
                report.append(f"  {row['name']}: P/E {row['pe_ratio']:.0f}x, "
                             f"Subsidy {row['subsidy_score']:.2f}x, "
                             f"Score {row['overall_score']}")
            report.append("")

        # Tier 2 holds
        tier2 = df[df['verdict'] == Verdict.TIER2_HOLD.value]
        if not tier2.empty:
            report.append("TIER 2 - HOLD")
            report.append("-" * 40)
            for _, row in tier2.iterrows():
                report.append(f"  {row['name']}: P/E {row['pe_ratio']:.0f}x, "
                             f"Score {row['overall_score']}")
            report.append("")

        # Avoid list
        avoid = df[df['verdict'].str.contains('AVOID')]
        if not avoid.empty:
            report.append("AVOID")
            report.append("-" * 40)
            for _, row in avoid.iterrows():
                report.append(f"  {row['name']}: {row['verdict']}")
                if row['red_flags']:
                    report.append(f"    Flags: {row['red_flags']}")
            report.append("")

        report.append("=" * 70)
        report.append("MACRO, ILLUMINATED.")

        return "\n".join(report)

    # ==========================================
    # SINGLE PROTOCOL REPORT
    # ==========================================

    def print_analysis(self, analysis: ProtocolAnalysis):
        """Print formatted analysis for a single protocol."""
        if analysis is None:
            print("No analysis available.")
            return

        width = 70
        print()
        print("═" * width)
        print(f"PROTOCOL FUNDAMENTAL ANALYSIS: {analysis.name.upper()}")
        print(f"Sector: {analysis.sector} | Date: {analysis.date}")
        print("═" * width)

        print("\nVALUATION SNAPSHOT")
        print("─" * width)
        print(f"  Market Cap (Circ):  ${analysis.market_cap/1e6:>10,.1f}M │  FDV:           ${analysis.fdv/1e6:>10,.1f}M")
        print(f"  Price:              ${analysis.price:>10.4f}   │  Float Ratio:   {analysis.float_ratio:>10.1%}")
        print(f"  P/F Ratio:          {analysis.pf_ratio:>10.1f}   │  P/S Ratio:     {analysis.ps_ratio:>10.1f}")

        print("\nFINANCIAL METRICS (Annualized)")
        print("─" * width)
        print(f"  Fees:               ${analysis.annualized_fees/1e6:>10,.2f}M")
        print(f"  Revenue:            ${analysis.annualized_revenue/1e6:>10,.2f}M")
        print(f"  Token Incentives:   ${analysis.annualized_incentives/1e6:>10,.2f}M")
        print(f"  Subsidy Score:      {analysis.subsidy_score:>10.2f}x  {'(ORGANIC)' if analysis.subsidy_score < 0.5 else '(SUBSIDIZED)' if analysis.subsidy_score < 2 else '(UNSUSTAINABLE)'}")
        print(f"  TVL:                ${analysis.tvl/1e9:>10,.2f}B")

        print("\nUSAGE METRICS")
        print("─" * width)
        print(f"  DAU:                {analysis.dau:>10,}")
        print(f"  MAU:                {analysis.mau:>10,}")
        print(f"  DAU/MAU Ratio:      {analysis.dau_mau_ratio:>10.1%}")
        print(f"  Active Developers:  {analysis.active_developers:>10}")

        print("\nLHM SCORES")
        print("─" * width)
        print(f"  Financial:          {analysis.financial_score:>10}/100")
        print(f"  Usage:              {analysis.usage_score:>10}/100")
        print(f"  Valuation:          {analysis.valuation_score:>10}/100")
        print(f"  OVERALL:            {analysis.overall_score:>10}/100")

        print("\nVERDICT")
        print("─" * width)
        print(f"  {analysis.verdict.value}")
        for reason in analysis.verdict_reasons:
            print(f"  → {reason}")

        if analysis.red_flags:
            print("\nRED FLAGS")
            print("─" * width)
            for flag in analysis.red_flags:
                print(f"  ⚠ {flag}")

        print()
        print("═" * width)


# ==========================================
# CLI INTERFACE
# ==========================================

if __name__ == "__main__":
    import sys

    print("Lighthouse Macro Crypto Fundamentals Engine")
    print("=" * 50)

    engine = CryptoFundamentalsEngine()

    if len(sys.argv) > 1:
        # Analyze specific protocol
        project_id = sys.argv[1]
        print(f"\nAnalyzing {project_id}...")
        analysis = engine.analyze_protocol(project_id)
        engine.print_analysis(analysis)
    else:
        # Run full screen
        print("\nRunning universe screen...")
        report = engine.generate_report(output_path='/Users/bob/LHM/Outputs/LHM_Crypto_Fundamentals.csv')
        print(report)
