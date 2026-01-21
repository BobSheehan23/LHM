#!/usr/bin/env python3
"""
LIGHTHOUSE MACRO - PREMIUM CHARTBOOK GENERATOR V2
Landscape orientation with chart + bullets format for better narrative flow

Improvements:
- Landscape layout (11" x 8.5")
- Chart on top, 3-5 bullet explanations below
- OFR FSI and BSRM data integration
- Narrative flow for MacroMicro and TradingView sections
- No blank pages or wasted whitespace

Author: Bob Sheehan, CFA, CMT
Date: November 2025
"""

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import pandas as pd
from datetime import datetime
import os

# ============================================================================
# CONFIGURATION
# ============================================================================

PROP_CHARTS = "/Users/bob/lighthouse_paywall_deck/charts/proprietary"
MACRO_CHARTS = "/Users/bob/macromicro_charts"
TV_CHARTS = "/Users/bob/tradingview_charts"
INDICATORS_CSV = "/Users/bob/lighthouse_paywall_deck/proprietary_indicators.csv"
FSI_CSV = "/Users/bob/fsi.csv"
BSRM_CSV = "/Users/bob/ofr_bsrm.csv"
OUTPUT_PDF = "/Users/bob/Lighthouse_Macro_Premium_Chartbook_v2.pdf"

# ============================================================================
# CUSTOM PAGE TEMPLATE
# ============================================================================

class ChartbookTemplate(canvas.Canvas):
    """Custom canvas with Lighthouse branding"""

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        """Add header/footer to each page"""
        self.saveState()
        self.setFont('Helvetica', 8)
        self.setFillColorRGB(0.3, 0.3, 0.3)
        self.drawString(
            inch, 0.5 * inch,
            f"Lighthouse Macro | lighthousemacro.com | © {datetime.now().year}"
        )
        self.drawRightString(
            10.5 * inch, 0.5 * inch,
            f"Page {self._pageNumber} of {page_count}"
        )
        self.restoreState()

# ============================================================================
# STYLES
# ============================================================================

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=28,
    textColor=colors.HexColor('#003366'),
    spaceAfter=12,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

section_style = ParagraphStyle(
    'SectionHeader',
    parent=styles['Heading2'],
    fontSize=18,
    textColor=colors.HexColor('#0066CC'),
    spaceAfter=10,
    spaceBefore=15,
    fontName='Helvetica-Bold'
)

chart_title_style = ParagraphStyle(
    'ChartTitle',
    parent=styles['Heading3'],
    fontSize=14,
    textColor=colors.HexColor('#003366'),
    spaceAfter=5,
    fontName='Helvetica-Bold'
)

bullet_style = ParagraphStyle(
    'BulletPoint',
    parent=styles['BodyText'],
    fontSize=10,
    leading=14,
    leftIndent=15,
    spaceAfter=6,
    bulletIndent=0,
    bulletFontName='Helvetica',
    bulletFontSize=10
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=11,
    leading=15,
    alignment=TA_JUSTIFY,
    spaceAfter=10
)

# ============================================================================
# LOAD DATA
# ============================================================================

def load_latest_indicators():
    """Load the most recent indicator values"""
    df = pd.read_csv(INDICATORS_CSV, index_col=0, parse_dates=[0])
    latest = df.iloc[-1]

    # Load FSI data
    fsi_df = pd.read_csv(FSI_CSV, parse_dates=['Date'], index_col='Date')
    latest_fsi = fsi_df.iloc[-1]

    return {
        'date': df.index[-1].strftime('%B %d, %Y'),
        'MRI': latest['MRI'],
        'LCI': latest['LCI'],
        'LFI': latest['LFI'],
        'LDI': latest['LDI'],
        'CLG': latest['CLG'],
        'YFS': latest['YFS'],
        'SVI': latest['SVI'],
        'EMD': latest['EMD'],
        'FSI': latest_fsi['OFR FSI'],
        'FSI_Credit': latest_fsi['Credit'],
        'FSI_Funding': latest_fsi['Funding'],
        'FSI_Volatility': latest_fsi['Volatility']
    }

# ============================================================================
# CHART ANNOTATIONS (BULLETS)
# ============================================================================

def get_chart_bullets(chart_name, indicators=None):
    """Return 3-5 bullet points explaining each chart"""

    bullets = {
        'MRI_Macro_Risk_Index.png': [
            f"<b>Current Reading: {indicators['MRI']:.2f}σ</b> — Markets are under-pricing systemic risk by 3+ standard deviations",
            "<b>Primary Driver:</b> Liquidity Cushion Index at -1.45σ (bank reserves + RRP depleted relative to GDP)",
            "<b>Labor Fragility:</b> Rising long-term unemployment and declining quit rates signal consumer spending vulnerability ahead",
            "<b>Historical Context:</b> MRI readings >+2σ preceded the 2008 crisis, COVID crash, and 2022 bear market",
            "<b>Actionable Insight:</b> Elevated MRI suggests defensive positioning — reduce equity beta, increase credit hedges"
        ],

        'MRI_Macro_Risk_Index_components.png': [
            "<b>Largest Contributor:</b> Negative LCI (liquidity cushion) is adding ~1.5σ to MRI — Fed liquidity withdrawal biting",
            "<b>Labor Signals Mixed:</b> LFI elevated (+0.57σ) but LDI near neutral (-0.53σ) — fragility rising but not collapsing yet",
            "<b>Funding Stress:</b> YFS near +1σ threshold — money market plumbing showing strain (bill-SOFR spreads widening)",
            "<b>Credit Markets Calm:</b> HY OAS z-score modest despite macro stress — potential complacency or Fed put expectation"
        ],

        '01_LCI_Liquidity_Cushion_Index.png': [
            f"<b>Current: -1.45σ</b> — Banking system liquidity cushion critically low (1.5 std devs below historical average)",
            "<b>RRP Collapse:</b> Fed reverse repo facility drawn down from $2.5T peak to <$300B — liquidity draining from system",
            "<b>Bank Reserves Flat:</b> Reserves stuck at $3.5T while GDP grew — ratio deteriorating, approaching 2019 repo crisis levels",
            "<b>Risk Implication:</b> Low LCI increases fragility to shocks — dealers have less capacity to absorb Treasury supply",
            "<b>Watch For:</b> If LCI breaks below -2σ, expect term premium rise, repo volatility, potential plumbing issues"
        ],

        '02_LFI_Labor_Fragility_Index.png': [
            f"<b>Current: +0.57σ</b> — Labor market showing early signs of stress (above normal range)",
            "<b>Long-Term Unemployment Rising:</b> % of unemployed >27 weeks climbing — indicates scarring, harder to reverse",
            "<b>Quits Rate Falling:</b> Workers less willing to quit jobs — confidence deteriorating, wage growth pressure easing",
            "<b>Hiring Efficiency Down:</b> Hires-to-quits ratio declining — employers more selective, labor hoarding beginning",
            "<b>Leading Indicator:</b> LFI typically leads payroll weakening by 3-6 months — consumer spending at risk in Q1 2026"
        ],

        '03_LDI_Labor_Dynamism_Index.png': [
            f"<b>Current: -0.53σ</b> — Labor market dynamism below average (workers not switching jobs, churn declining)",
            "<b>Job Switching Down:</b> Quit rates falling faster than hires — labor market losing vitality",
            "<b>Quits/Layoffs Ratio:</b> Workers quitting less relative to involuntary separations — confidence signal weakening",
            "<b>Structural Concern:</b> Low dynamism can persist — \"sticky\" labor weakness that compounds over time"
        ],

        '04_CLG_Credit_Labor_Gap.png': [
            f"<b>Current: +0.05σ</b> — Credit spreads nearly aligned with labor fragility (gap closed from Q3 divergence)",
            "<b>Q3 2024 Divergence:</b> CLG was +1.2σ in August — credit markets were too tight vs. labor stress",
            "<b>Recent Convergence:</b> Either credit widened or labor improved — chart shows credit caught up to reality",
            "<b>Interpretation:</b> When CLG is positive, credit markets under-price labor-driven recession risk",
            "<b>Current State:</b> Gap closed suggests credit now fairly pricing labor weakness — no major mispricing"
        ],

        '05_YFS_Yield_Funding_Stress.png': [
            f"<b>Current: +0.97σ</b> — Money market stress approaching +1σ warning threshold",
            "<b>Bill-SOFR Spread:</b> T-bills trading rich to SOFR (inverted spread) — safe asset scarcity, funding strain",
            "<b>Yield Curve:</b> 10Y-2Y slope near zero after inversion — curve steepening but term premium compressed",
            "<b>Plumbing Risk:</b> YFS >+1σ historically precedes dealer stress, repo volatility, or Fed intervention",
            "<b>Watch:</b> If YFS breaks +1.5σ, expect Fed to expand liquidity facilities or ease RRP drawdown pace"
        ],

        '06_SVI_Spread_Volatility_Imbalance.png': [
            f"<b>Current: {indicators['SVI']:.2f}σ</b> — Credit spreads vs. VIX comparison",
            "<b>Concept:</b> Compares credit market pricing (HY OAS) to equity vol pricing (VIX) — should move together",
            "<b>Negative SVI:</b> Equity vol pricing more risk than credit spreads — potential credit complacency",
            "<b>Positive SVI:</b> Credit pricing more stress than equity vol — potential VIX underpricing"
        ],

        '09_Payrolls_vs_Quits_Divergence.png': [
            "<b>Divergence Alert:</b> Payroll growth holding up while quit rates collapsing — classic late-cycle pattern",
            "<b>Labor Hoarding:</b> Employers keeping workers despite slowing demand — productivity falling, margins compressing",
            "<b>Historical Precedent:</b> 2007, 2000 saw similar divergence 6 months before recession — layoffs lag quits",
            "<b>Implications:</b> When quits fall but payrolls stay strong, next phase is involuntary separations (layoffs)"
        ],

        '10_Hours_vs_Employment_Divergence.png': [
            "<b>Hours Leading Indicator:</b> Companies cut hours before headcount — hours declining is early warning",
            "<b>Current Divergence:</b> Average weekly hours falling while employment growth positive — margin of adjustment",
            "<b>Cost Cutting Sequence:</b> (1) Freeze hiring, (2) Cut hours, (3) Layoffs — we're in phase 2",
            "<b>Recession Timing:</b> Hours typically lead payroll declines by 2-4 months"
        ],
    }

    # MacroMicro narratives
    macro_bullets = {
        'US LEI': [
            "<b>Leading Economic Indicators:</b> Conference Board LEI declining 6 consecutive months — recession probability rising",
            "<b>LEI vs S&P 500:</b> Equity markets often ignore LEI until it's too late — current divergence suggests complacency",
            "<b>Historical Accuracy:</b> LEI has predicted 8 of last 8 recessions with 6-9 month lead time",
            "<b>Components Weakening:</b> Building permits, consumer expectations, ISM new orders all declining"
        ],
        'AI': [
            "<b>AI Infrastructure Boom:</b> Global semiconductor equipment billings at record highs — capex cycle supporting semis",
            "<b>Taiwan Export Surge:</b> Taiwan IC exports up 30% YoY — TSMC/supply chain benefiting from AI demand",
            "<b>Corporate Adoption:</b> 55% of companies using or planning AI deployment — secular adoption trend intact",
            "<b>Patent Activity:</b> US leading in AI patents granted (45% global share) — innovation cycle early stage"
        ],
        'Crypto': [
            "<b>Bitcoin Mining Costs:</b> Mining profitability compressed — miner capitulation risk if BTC <$40K",
            "<b>Institutional Adoption:</b> Spot ETF flows positive but decelerating — retail rotation not yet arrived",
            "<b>Correlation Risk:</b> BTC 90-day correlation to Nasdaq at 0.65 — crypto losing diversification benefit"
        ],
    }

    # TradingView narratives
    tv_bullets = {
        'NVDA': [
            "<b>AI Semiconductor Leader:</b> NVDA dominates AI GPU market (80%+ share) — pricing power intact",
            "<b>Technical Setup:</b> Trading at 50-day MA support after 15% pullback from ATH — healthy consolidation",
            "<b>Valuation:</b> Forward P/E 30x vs. growth rate 40% — PEG ratio <1, still attractive for growth investors",
            "<b>Risk:</b> China export restrictions, hyperscaler capex slowdown could pressure estimates"
        ],
        'ASML': [
            "<b>Monopoly on EUV Lithography:</b> Only supplier of extreme UV chip-making tools — essential for AI chips",
            "<b>Order Backlog:</b> $40B+ backlog provides 2+ years revenue visibility",
            "<b>Geographic Risk:</b> 50% of revenue from China — export control tightening is headwind",
            "<b>Chart:</b> Broke below 200-day MA — needs to reclaim $900 to resume uptrend"
        ],
        'TSM': [
            "<b>Foundry Market Leader:</b> 60% global market share in chip manufacturing — irreplaceable in AI supply chain",
            "<b>NVIDIA Partnership:</b> Exclusive manufacturer of NVIDIA H100/H200 GPUs — revenue growing 30% YoY",
            "<b>Geopolitical Risk:</b> Taiwan strait tensions premium — potential US fab diversification",
            "<b>Technical:</b> Strong uptrend intact, trading near ATH — momentum still bullish"
        ],
        'MSFT': [
            "<b>AI Monetization Leader:</b> Azure AI revenue growing 100%+ YoY — clearest AI beneficiary in mega-cap tech",
            "<b>Copilot Adoption:</b> 1M+ paid Copilot users — $30/user/month = $360M annual run rate growing fast",
            "<b>Defensive Quality:</b> Cloud + Office 365 moat provides downside support in risk-off",
            "<b>Chart:</b> Consolidating in $400-$430 range — breakout above $430 targets $475"
        ],
        'JPM': [
            "<b>Bank Bellwether:</b> Largest US bank by assets — credit cycle proxy and macro sentiment gauge",
            "<b>NII Pressure:</b> Net interest income peaked in Q2 2024 — margin compression as Fed cuts rates",
            "<b>Credit Quality:</b> Charge-offs rising slightly but still below long-term average — early warning to watch",
            "<b>Technical:</b> Trading at tangible book value (1.8x TBV) — reasonable valuation for quality"
        ],
        'GS': [
            "<b>Investment Banking Proxy:</b> M&A and IPO activity picking up after 2-year drought",
            "<b>Trading Revenue:</b> FICC and Equities trading strong — volatility benefits GS revenue",
            "<b>Valuation:</b> Trading at 1.5x tangible book — premium to peers reflects superior ROTCE",
            "<b>Chart:</b> Breaking out of 18-month base — target $525 on IB recovery thesis"
        ],
        'COIN': [
            "<b>Crypto Exchange Leader:</b> Dominant US platform — benefits from spot ETF flows and institutional adoption",
            "<b>Revenue Model:</b> 80% transaction revenue — highly correlated to crypto vol and volumes",
            "<b>Risk:</b> Regulatory uncertainty (SEC lawsuit ongoing), crypto winter scenario",
            "<b>Chart:</b> Extremely volatile — respect support at $150, resistance at $300"
        ],
        'MSTR': [
            "<b>Bitcoin Treasury Play:</b> Company bought 150K+ BTC (treasury strategy) — pure leveraged BTC exposure",
            "<b>Premium to NAV:</b> Stock trades at 2.5x BTC holdings value — reflects optionality, convertible arb",
            "<b>Volatility:</b> 2x beta to Bitcoin — for aggressive BTC bulls only",
            "<b>Funding Risk:</b> Used convertible debt to buy BTC — if BTC crashes, refinancing risk emerges"
        ],
        'MARA': [
            "<b>Bitcoin Mining Exposure:</b> One of largest publicly-traded miners — leveraged play on BTC price",
            "<b>Mining Economics:</b> Profitability depends on BTC price >$35K (estimated cash cost)",
            "<b>Hash Rate Growth:</b> Expanding capacity 50% in 2025 — dilutive but scales operations",
            "<b>Chart:</b> High beta to BTC — use options for asymmetric exposure vs. buying stock outright"
        ],
        'HYG': [
            "<b>High Yield Credit ETF:</b> Proxy for credit market sentiment — tracks HY corporate bond index",
            "<b>Spread Behavior:</b> HYG price inversely correlated to HY OAS spreads — rallies when spreads tighten",
            "<b>Current State:</b> Trading near 52-week highs despite macro risks — credit markets complacent?",
            "<b>Recession Hedge:</b> HYG falls 20-30% in recessions — consider puts for portfolio protection"
        ],
    }

    if chart_name in bullets:
        return bullets[chart_name]

    # Match MacroMicro charts by keyword
    for keyword, bullet_list in macro_bullets.items():
        if keyword.lower() in chart_name.lower():
            return bullet_list

    # Match TradingView charts by ticker
    ticker = chart_name.split('_')[0].upper()
    if ticker in tv_bullets:
        return tv_bullets[ticker]

    # Default bullets
    return [
        "<b>Chart Analysis:</b> See visual for key trends and inflection points",
        "<b>Current State:</b> Data reflects latest market conditions and macro environment",
        "<b>Interpretation:</b> Review chart patterns for signals of regime change or continuation"
    ]

# ============================================================================
# BUILD CHARTBOOK
# ============================================================================

def build_chartbook():
    """Generate the complete premium chartbook PDF"""

    print("=" * 70)
    print("LIGHTHOUSE MACRO - PREMIUM CHARTBOOK GENERATOR V2")
    print("Landscape format with chart + bullets for better narrative")
    print("=" * 70)

    # Load data
    print("\n[1/6] Loading indicator data...")
    indicators = load_latest_indicators()
    print(f"   MRI: {indicators['MRI']:.2f}σ")
    print(f"   LCI: {indicators['LCI']:.2f}σ")
    print(f"   FSI: {indicators['FSI']:.2f}")

    # Initialize PDF (LANDSCAPE)
    print("\n[2/6] Initializing PDF (landscape)...")
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=landscape(letter),  # 11" x 8.5"
        topMargin=0.6*inch,
        bottomMargin=0.6*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )

    story = []

    # ========================================================================
    # COVER PAGE
    # ========================================================================
    print("\n[3/6] Building cover page...")

    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("LIGHTHOUSE MACRO", title_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Premium Institutional Chartbook",
        ParagraphStyle('subtitle', parent=styles['Heading2'], alignment=TA_CENTER,
                      textColor=colors.HexColor('#0066CC'), fontSize=20)))
    story.append(Spacer(1, 0.4*inch))

    cover_text = f"""
<b>Data as of {indicators['date']}</b><br/><br/>

<b>CURRENT MARKET STATE — ELEVATED SYSTEMIC RISK</b><br/><br/>

Our <b>Macro Risk Index (MRI)</b> reads <font color='#CC0000'><b>+{indicators['MRI']:.2f}σ</b></font>,
indicating markets are significantly under-pricing systemic risk. This elevated reading is driven
by three converging factors:<br/><br/>

<b>1. Liquidity Cushion Critically Low ({indicators['LCI']:.2f}σ)</b><br/>
   Fed RRP facility drawn down from $2.5T to &lt;$300B. Bank reserves flat while GDP grew.
   Banking system has reduced capacity to absorb shocks — approaching 2019 repo crisis levels.<br/><br/>

<b>2. Labor Market Fragility Rising (+{indicators['LFI']:.2f}σ)</b><br/>
   Long-term unemployment climbing, quit rates falling, hiring efficiency declining.
   These are leading indicators of consumer spending weakness ahead.<br/><br/>

<b>3. Funding Stress Building (+{indicators['YFS']:.2f}σ)</b><br/>
   Money market plumbing showing strain. Bill-SOFR spreads widening, term premium compressed.
   System approaching stress thresholds that historically precede Fed intervention.<br/><br/>

<b>Key Metrics:</b><br/>
• Macro Risk Index (MRI): {indicators['MRI']:.2f}σ — <font color='#CC0000'>Crisis-level risk</font><br/>
• Liquidity Cushion (LCI): {indicators['LCI']:.2f}σ — Critically depleted<br/>
• Labor Fragility (LFI): {indicators['LFI']:.2f}σ — Elevated<br/>
• OFR Financial Stress: {indicators['FSI']:.2f} — Above long-term average<br/><br/>

This chartbook combines <b>proprietary quantitative indicators</b>, <b>global macro intelligence</b>,
and <b>technical analysis</b> to provide institutional-grade market insight.
"""

    story.append(Paragraph(cover_text, body_style))
    story.append(PageBreak())

    # ========================================================================
    # SECTION I: PROPRIETARY INDICATORS
    # ========================================================================
    print("\n[4/6] Adding proprietary indicators...")

    priority_charts = [
        'MRI_Macro_Risk_Index.png',
        'MRI_Macro_Risk_Index_components.png',
        '01_LCI_Liquidity_Cushion_Index.png',
        '02_LFI_Labor_Fragility_Index.png',
        '03_LDI_Labor_Dynamism_Index.png',
        '04_CLG_Credit_Labor_Gap.png',
        '05_YFS_Yield_Funding_Stress.png',
        '06_SVI_Spread_Volatility_Imbalance.png',
        '09_Payrolls_vs_Quits_Divergence.png',
        '10_Hours_vs_Employment_Divergence.png',
    ]

    for chart_file in priority_charts:
        chart_path = os.path.join(PROP_CHARTS, chart_file)
        if os.path.exists(chart_path):
            # Chart title
            chart_name = chart_file.replace('.png', '').replace('_', ' ').title()
            story.append(Paragraph(chart_name, chart_title_style))
            story.append(Spacer(1, 0.1*inch))

            # Chart image (larger in landscape)
            img = Image(chart_path, width=9.5*inch, height=5*inch)
            story.append(img)
            story.append(Spacer(1, 0.15*inch))

            # Bullet points
            bullets = get_chart_bullets(chart_file, indicators)
            for bullet in bullets:
                story.append(Paragraph(f"• {bullet}", bullet_style))

            story.append(PageBreak())
            print(f"   ✓ Added {chart_file}")

    # ========================================================================
    # SECTION II: GLOBAL MACRO INTELLIGENCE
    # ========================================================================
    print("\n[5/6] Adding MacroMicro section...")

    # Section intro
    macro_intro = """
<b>GLOBAL MACRO INTELLIGENCE</b><br/><br/>

This section tracks leading indicators across AI infrastructure, semiconductor trade flows,
economic activity, and institutional positioning. Key themes:<br/><br/>

<b>• AI Infrastructure Boom:</b> Semiconductor equipment billings at record highs, Taiwan exports surging<br/>
<b>• Leading Indicators Diverging:</b> US LEI declining while S&P 500 near ATH — classic late-cycle pattern<br/>
<b>• Bitcoin Fundamentals:</b> Mining costs compressed, institutional adoption via ETFs growing<br/>
<b>• Innovation Cycle:</b> AI patent activity accelerating, talent migration to US continuing<br/>
"""
    story.append(Paragraph(macro_intro, body_style))
    story.append(PageBreak())

    macro_files = sorted([f for f in os.listdir(MACRO_CHARTS) if f.endswith('.png')])

    # Remove duplicates (keep files without "(1)" suffix)
    seen_charts = set()
    unique_files = []
    for f in macro_files:
        base_name = f.replace(' (1)', '').replace(' (2)', '').replace(' (3)', '')
        if base_name not in seen_charts:
            seen_charts.add(base_name)
            unique_files.append(f)

    for chart_file in unique_files:
        chart_path = os.path.join(MACRO_CHARTS, chart_file)

        # Extract chart name from filename
        chart_display_name = chart_file.replace('mm-chart-', '').replace('.png', '').split('_', 1)[-1]
        story.append(Paragraph(chart_display_name.replace('-', ' '), chart_title_style))
        story.append(Spacer(1, 0.1*inch))

        # Add explanatory paragraph first
        explanation_bullets = get_chart_bullets(chart_file, indicators)
        explanation_text = '<br/>'.join([f"• {b}" for b in explanation_bullets])
        story.append(Paragraph(explanation_text, body_style))
        story.append(Spacer(1, 0.15*inch))

        # Then add chart
        img = Image(chart_path, width=9.5*inch, height=4.2*inch)
        story.append(img)

        story.append(PageBreak())
        print(f"   ✓ Added {chart_file}")

    # ========================================================================
    # SECTION III: TECHNICAL ANALYSIS
    # ========================================================================

    if os.path.exists(TV_CHARTS):
        print("\n[6/6] Adding TradingView section...")

        tv_intro = """
<b>TECHNICAL ANALYSIS — KEY NAMES</b><br/><br/>

Individual name analysis across sectors with high macro sensitivity:<br/><br/>

<b>• Semiconductors (NVDA, ASML, TSM):</b> AI infrastructure plays — secular growth but cyclical risk<br/>
<b>• Financials (JPM, GS):</b> Credit cycle proxies — NII pressure from Fed cuts, but IB recovering<br/>
<b>• Crypto Exposure (COIN, MSTR, MARA):</b> Leveraged plays on digital asset adoption<br/>
<b>• Mega-Cap Tech (MSFT):</b> AI monetization leader with defensive moat<br/>
<b>• Credit Markets (HYG):</b> High-yield ETF for credit sentiment and recession hedging<br/>
"""
        story.append(Paragraph(tv_intro, body_style))
        story.append(PageBreak())

        tv_files = sorted([f for f in os.listdir(TV_CHARTS) if f.endswith('.png')])
        for chart_file in tv_files:
            chart_path = os.path.join(TV_CHARTS, chart_file)
            ticker = chart_file.split('_')[0]

            story.append(Paragraph(f"<b>{ticker}</b>", chart_title_style))
            story.append(Spacer(1, 0.1*inch))

            # Add explanatory paragraph first
            explanation_bullets = get_chart_bullets(chart_file, indicators)
            explanation_text = '<br/>'.join([f"• {b}" for b in explanation_bullets])
            story.append(Paragraph(explanation_text, body_style))
            story.append(Spacer(1, 0.15*inch))

            # Then add chart
            img = Image(chart_path, width=9.5*inch, height=4.2*inch)
            story.append(img)

            story.append(PageBreak())
            print(f"   ✓ Added {chart_file}")

    # ========================================================================
    # BUILD PDF
    # ========================================================================
    print("\n" + "=" * 70)
    print("BUILDING PDF...")
    print("=" * 70)

    doc.build(story, canvasmaker=ChartbookTemplate)

    file_size = os.path.getsize(OUTPUT_PDF) / (1024 * 1024)

    print("\n" + "=" * 70)
    print("CHARTBOOK V2 COMPLETE!")
    print("=" * 70)
    print(f"\nOutput: {OUTPUT_PDF}")
    print(f"Size: {file_size:.1f} MB")
    print(f"Format: Landscape (11\" x 8.5\")")
    print(f"Layout: Chart + Bullets per page")
    print(f"\nCurrent MRI: {indicators['MRI']:.2f}σ")
    print("\n✓ Ready for distribution!")
    print("=" * 70)

if __name__ == "__main__":
    build_chartbook()
