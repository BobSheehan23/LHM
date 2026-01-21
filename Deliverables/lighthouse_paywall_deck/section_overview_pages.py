"""
Lighthouse Macro - Section Overview Pages
Full-page text explanations for each section
"""

import matplotlib.pyplot as plt
from lighthouse_style import COLORS


def create_section_overview(section_number, title, content_blocks):
    """
    Create a full-page text overview for a section

    Args:
        section_number: Section number (1-6)
        title: Section title
        content_blocks: List of (heading, text) tuples
    """
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    # Section number (large)
    ax.text(0.5, 0.88, f'SECTION {section_number}',
            ha='center', va='center', fontsize=36, fontweight='bold',
            color=COLORS['ocean_blue'], transform=ax.transAxes)

    # Section title
    ax.text(0.5, 0.82, title.upper(),
            ha='center', va='center', fontsize=20, fontweight='bold',
            color=COLORS['ocean_blue'], transform=ax.transAxes)

    # Separator line
    ax.plot([0.15, 0.85], [0.78, 0.78],
            color=COLORS['ocean_blue'], linewidth=2,
            transform=ax.transAxes)

    # Content blocks
    y_position = 0.72
    line_spacing = 0.03

    for heading, text in content_blocks:
        # Heading
        if heading:
            ax.text(0.1, y_position, heading,
                    ha='left', va='top', fontsize=12, fontweight='bold',
                    color=COLORS['ocean_blue'], transform=ax.transAxes)
            y_position -= 0.04

        # Body text (wrap manually with \n in the text)
        ax.text(0.1, y_position, text,
                ha='left', va='top', fontsize=10,
                color=COLORS['black'], transform=ax.transAxes,
                wrap=True)

        # Calculate spacing based on number of lines
        num_lines = text.count('\n') + 1
        y_position -= (num_lines * line_spacing + 0.03)

    # Watermark
    fig.text(0.5, 0.05, 'MACRO, ILLUMINATED.',
            ha='center', va='bottom', fontsize=10, fontweight='bold',
            color=COLORS['ocean_blue'], alpha=0.6)

    return fig


def section_1_overview():
    """Section 1: Liquidity & Funding Stress"""
    content_blocks = [
        ("Framework: The Liquidity Foundation",
         "The plumbing matters more than the narrative. While markets obsess over Fed meetings\n" +
         "and inflation prints, the real story plays out in overnight repo markets, the RRP facility,\n" +
         "and bank reserve levels. This section tracks the system's shock-absorption capacity—\n" +
         "the cushion that determines whether volatility spikes get contained or cascade into crisis."),

        ("Key Indicators:",
         "1. Liquidity Cushion Index (LCI) - Are reserves + RRP sufficient to absorb stress?\n" +
         "2. Yield-Funding Stress (YFS) - Is the plumbing cracking?\n" +
         "3. Repo Rate Dispersion - Are some participants getting locked out?"),

        ("The Transmission Mechanism:",
         "• High LCI + Low YFS = Ample liquidity, markets can absorb shocks\n" +
         "• Low LCI + Rising YFS = Vulnerable system, small shocks → big moves\n" +
         "• Repo dispersion widening = Funding fragmentation, crisis precursor"),

        ("What to Watch:",
         "• RRP drawdown below $500B (critical threshold)\n" +
         "• BGCR-EFFR spread > +15 bps (funding stress)\n" +
         "• Repo dispersion 99th-1st percentile > 50 bps (fragmentation)"),

        ("Takeaway:",
         "The 2008 crisis taught us: liquidity is binary. You have it until you don't.\n" +
         "These charts track the transition from ample to scarce—the most important\n" +
         "regime shift in markets.")
    ]

    return create_section_overview(1, "Liquidity & Funding Stress", content_blocks)


def section_2_overview():
    """Section 2: Labor Market Dynamics"""
    content_blocks = [
        ("Framework: Labor as Leading Indicator",
         "The unemployment rate is a lagging indicator. By the time it spikes, the recession is\n" +
         "already here. We focus on flow variables—quits, hires, hours worked—that deteriorate\n" +
         "6-12 months before headline payrolls turn negative."),

        ("Key Indicators:",
         "1. Labor Fragility Index (LFI) - How hard is it to find a job once unemployed?\n" +
         "2. Labor Dynamism Index (LDI) - Are workers confident enough to quit and upgrade?\n" +
         "3. Hours vs Employment Divergence - Are firms cutting hours before headcount?"),

        ("The Sequence of Deterioration:",
         "1. Quits decline (workers stop job-hopping)\n" +
         "2. Hours cut (reduce overtime, shift to part-time)\n" +
         "3. Temp workers laid off (easiest to cut)\n" +
         "4. Hiring freezes (stop backfilling attrition)\n" +
         "5. Permanent layoffs (unemployment rate rises)"),

        ("What to Watch:",
         "• Quits rate < 2.0% (vs 3.0% peak) = Late cycle\n" +
         "• Hours YoY < Employment YoY = Layoffs coming\n" +
         "• LFI rising while unemployment stable = Hidden deterioration"),

        ("Takeaway:",
         "\"Payrolls can stay positive while quits slide—that's a late-cycle tell.\"\n" +
         "Don't wait for unemployment to spike. By then, the damage is done.")
    ]

    return create_section_overview(2, "Labor Market Dynamics", content_blocks)


def section_3_overview():
    """Section 3: Credit Markets & Risk Appetite"""
    content_blocks = [
        ("Framework: Credit Leads, Equities Follow",
         "Credit markets price risk. Equity markets price narratives. When the two diverge—\n" +
         "spreads widening while stocks rally—credit is usually right. This section tracks not just\n" +
         "spread levels, but spread adequacy relative to macro fragility."),

        ("Key Indicators:",
         "1. Credit-Labor Gap (CLG) - Are spreads too tight given labor market stress?\n" +
         "2. HY Spread vs Volatility Imbalance - Are spreads compensating for volatility?\n" +
         "3. Excess Bond Premium (EBP) - Risk aversion above default risk alone"),

        ("The Credit Cycle Stages:",
         "• Early Cycle: Spreads wide, defaults peaking, opportunity emerging\n" +
         "• Mid Cycle: Spreads normalizing, credit profitable\n" +
         "• Late Cycle: Spreads tight, covenant-lite deals, complacency\n" +
         "• Crisis: Spreads blow out >1000 bps, credit markets freeze"),

        ("What to Watch:",
         "• HY OAS < 300 bps = Late cycle, reduce credit\n" +
         "• CLG negative (spreads < labor stress) = Pre-widening setup\n" +
         "• EBP rising = Risk aversion building"),

        ("Takeaway:",
         "\"Historically a pre-widening configuration\" when CLG goes negative.\n" +
         "Don't confuse tight spreads with safety. Spread adequacy matters more than levels.")
    ]

    return create_section_overview(3, "Credit Markets & Risk Appetite", content_blocks)


def section_4_overview():
    """Section 4: Equity Positioning & Momentum"""
    content_blocks = [
        ("Framework: Momentum Matters, Until It Doesn't",
         "Equity markets can stay irrational longer than you can stay solvent. But stretched\n" +
         "momentum + macro deterioration = fragile setup. This section tracks not just price\n" +
         "levels, but positioning, quality preferences, and shock-absorption capacity."),

        ("Key Indicators:",
         "1. Equity Momentum Divergence (EMD) - How stretched is momentum vs volatility?\n" +
         "2. Quality vs Risk (QUAL/SPY) - Flight to quality or junk rally?\n" +
         "3. Macro Risk Index (MRI) - Are equities pricing in macro risk?"),

        ("The Late-Cycle Pattern:",
         "• Equities grind higher (FOMO, passive flows)\n" +
         "• Volatility compressed (low VIX)\n" +
         "• Quality underperforms (junk rally)\n" +
         "• Macro deteriorates (labor, credit weakening)\n" +
         "• Result: Thin shock absorption, prone to air pockets"),

        ("What to Watch:",
         "• EMD > +1σ = Stretched momentum, reduce beta\n" +
         "• QUAL/SPY at cycle lows = Maximum risk appetite\n" +
         "• MRI rising + SPX rising = Markets under-pricing risk"),

        ("Takeaway:",
         "\"Currently at cycle lows despite macro deterioration; signals late-stage bull\n" +
         "market behavior.\" When everyone's bullish, be careful.")
    ]

    return create_section_overview(4, "Equity Positioning & Momentum", content_blocks)


def section_5_overview():
    """Section 5: Crypto & Digital Assets"""
    content_blocks = [
        ("Framework: Crypto as Macro Barometer",
         "Bitcoin is no longer an isolated asset. When BTC trades 80%+ correlated with Nasdaq,\n" +
         "it's a risk-on/risk-off instrument. Stablecoins represent on-chain liquidity—'dry powder'\n" +
         "that precedes rallies. This section tracks crypto-traditional integration."),

        ("Key Indicators:",
         "1. Stablecoin Supply - On-chain liquidity, leads BTC price\n" +
         "2. BTC Correlation to Nasdaq/Gold - Risk-on or safe haven?\n" +
         "3. Stablecoin vs MMF - Digital dollar gaining share?"),

        ("The Crypto Liquidity Framework:",
         "• Rising stablecoin supply = Capital entering, bullish 3-6M\n" +
         "• Falling stablecoin supply = Off-ramping, bearish\n" +
         "• BTC corr to Nasdaq > 0.6 = Risk-on asset\n" +
         "• BTC corr to Gold > 0.5 = Safe haven narrative"),

        ("What to Watch:",
         "• Stablecoin supply growth accelerating = BTC rally ahead\n" +
         "• BTC realized vol converging to equity vol = Maturation\n" +
         "• Stablecoin/MMF ratio rising = Structural shift"),

        ("Takeaway:",
         "Stablecoins backed by Treasuries compete with MMFs for same collateral.\n" +
         "Crypto is eating TradFi from the inside.")
    ]

    return create_section_overview(5, "Crypto & Digital Assets", content_blocks)


def section_6_overview():
    """Section 6: AI Infrastructure & CapEx Cycle"""
    content_blocks = [
        ("Framework: AI CapEx as Leading GDP Indicator",
         "The Magnificent 7 are spending $200B+ annually on AI infrastructure. This CapEx cycle\n" +
         "drives semiconductor demand, foundry capacity, and IT investment—all of which feed\n" +
         "into GDP with a lag. This section tracks the build-out and identifies inflection points."),

        ("Key Indicators:",
         "1. Mag 7 CapEx Trends - Are they still spending or cutting?\n" +
         "2. Semiconductor Equipment Exports - Leading indicator of chip production\n" +
         "3. IT Investment Contribution to GDP - How much is AI driving growth?"),

        ("The CapEx Cycle:",
         "1. Early Stage: Hyperscalers announce massive budgets\n" +
         "2. Build-Out: Equipment orders surge, NVDA/TSM rally\n" +
         "3. Peak CapEx: Spending plateaus, utilization still low\n" +
         "4. Digestion: CapEx cuts, equipment names correct\n" +
         "5. Payoff: Utilization rises, revenue justifies spending"),

        ("What to Watch:",
         "• Mag 7 CapEx growth decelerating = Peak AI spending\n" +
         "• Taiwan semi exports declining = Chip demand rolling over\n" +
         "• IT investment/GDP flattening = CapEx not flowing to GDP yet"),

        ("Takeaway:",
         "Follow the CapEx, not the hype. When spending slows, NVDA is a sell\n" +
         "regardless of revenue beats.")
    ]

    return create_section_overview(6, "AI Infrastructure & CapEx Cycle", content_blocks)
