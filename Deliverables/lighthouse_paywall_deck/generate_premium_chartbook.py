#!/usr/bin/env python3
"""
LIGHTHOUSE MACRO - PREMIUM CHARTBOOK GENERATOR
Combines proprietary indicators, MacroMicro analysis, and TradingView technicals
with explanatory text for accessibility.

Author: Bob Sheehan, CFA, CMT
Date: November 2025
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
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
OUTPUT_PDF = "/Users/bob/Lighthouse_Macro_Premium_Chartbook.pdf"

# ============================================================================
# CUSTOM PAGE TEMPLATE WITH HEADERS/FOOTERS
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

        # Footer
        self.setFont('Helvetica', 8)
        self.setFillColorRGB(0.3, 0.3, 0.3)
        self.drawString(
            inch, 0.5 * inch,
            f"Lighthouse Macro | lighthousemacro.com | © {datetime.now().year}"
        )
        self.drawRightString(
            7.5 * inch, 0.5 * inch,
            f"Page {self._pageNumber} of {page_count}"
        )

        self.restoreState()

# ============================================================================
# STYLE SETUP
# ============================================================================

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#003366'),
    spaceAfter=12,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

section_style = ParagraphStyle(
    'SectionHeader',
    parent=styles['Heading2'],
    fontSize=16,
    textColor=colors.HexColor('#0066CC'),
    spaceAfter=10,
    spaceBefore=20,
    fontName='Helvetica-Bold',
    borderPadding=5,
    borderColor=colors.HexColor('#0066CC'),
    borderWidth=0,
    leftIndent=0
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=10,
    leading=14,
    alignment=TA_JUSTIFY,
    spaceAfter=10
)

indicator_style = ParagraphStyle(
    'IndicatorBox',
    parent=styles['BodyText'],
    fontSize=9,
    leading=12,
    leftIndent=10,
    rightIndent=10,
    spaceAfter=8,
    textColor=colors.HexColor('#333333'),
    backColor=colors.HexColor('#F5F5F5'),
    borderPadding=8
)

# ============================================================================
# LOAD LATEST INDICATOR VALUES
# ============================================================================

def load_latest_indicators():
    """Load the most recent indicator values"""
    df = pd.read_csv(INDICATORS_CSV, index_col=0, parse_dates=[0])
    latest = df.iloc[-1]
    return {
        'date': df.index[-1].strftime('%B %d, %Y'),
        'MRI': latest['MRI'],
        'LCI': latest['LCI'],
        'LFI': latest['LFI'],
        'LDI': latest['LDI'],
        'CLG': latest['CLG'],
        'YFS': latest['YFS'],
        'SVI': latest['SVI'],
        'EMD': latest['EMD']
    }

# ============================================================================
# CONTENT SECTIONS
# ============================================================================

def get_intro_text(indicators):
    """Executive summary with current indicator readings"""
    return f"""
<b>LIGHTHOUSE MACRO</b><br/>
<b>Premium Institutional Chartbook</b><br/>
<br/>
<i>Proprietary Macro Risk Analysis</i><br/>
Data as of {indicators['date']}<br/>
<br/>
<br/>
<b>CURRENT MARKET STATE:</b><br/>
<br/>
Our <b>Macro Risk Index (MRI)</b> currently reads <b>{indicators['MRI']:.2f}σ</b>,
indicating {"<b>ELEVATED SYSTEMIC RISK</b>" if indicators['MRI'] > 1 else "<b>NORMAL RISK ENVIRONMENT</b>" if indicators['MRI'] > -1 else "<b>LOW RISK ENVIRONMENT</b>"}.
This reflects underlying stress in liquidity conditions, labor market fragility, and credit market pricing.<br/>
<br/>
<b>Key Readings:</b><br/>
• Liquidity Cushion Index (LCI): {indicators['LCI']:.2f}σ<br/>
• Labor Fragility Index (LFI): {indicators['LFI']:.2f}σ<br/>
• Labor Dynamism Index (LDI): {indicators['LDI']:.2f}σ<br/>
• Credit-Labor Gap (CLG): {indicators['CLG']:.2f}σ<br/>
• Yield-Funding Stress (YFS): {indicators['YFS']:.2f}σ<br/>
<br/>
This chartbook combines <b>proprietary quantitative indicators</b>, <b>global macro data</b>,
and <b>technical analysis</b> to provide institutional-grade market intelligence.
"""

def get_section_intro(section_name):
    """Introductory text for each major section"""
    intros = {
        'proprietary': """
<b>SECTION I: PROPRIETARY INDICATORS</b><br/>
<br/>
These indicators are exclusive to Lighthouse Macro and track systemic risks not captured by standard metrics.
Each indicator is z-scored against rolling 1-year windows to identify statistical extremes.<br/>
<br/>
<b>Macro Risk Index (MRI):</b> Our flagship composite that aggregates labor fragility, labor dynamism,
funding stress, credit spreads, equity momentum, and liquidity cushion. Readings above +1σ indicate
markets are under-pricing systemic risk.<br/>
<br/>
<b>Liquidity Cushion Index (LCI):</b> Measures the banking system's ability to absorb shocks via
Fed reverse repo facility usage and bank reserves relative to GDP. Negative readings indicate
depleted liquidity buffers.<br/>
<br/>
<b>Labor Fragility Index (LFI):</b> Tracks deteriorating labor market conditions through long-duration
unemployment, declining quit rates, and falling hires-to-quits ratios. Rising LFI signals consumer
spending vulnerability.<br/>
<br/>
<b>Labor Dynamism Index (LDI):</b> Measures labor market health via job switching, hiring efficiency,
and employment churn. Falling LDI indicates structural labor market weakness.<br/>
<br/>
<b>Credit-Labor Gap (CLG):</b> Identifies divergences between credit market pricing (HY spreads) and
labor market stress. Positive gaps suggest credit markets are too complacent.<br/>
""",

        'macromicro': """
<b>SECTION II: GLOBAL MACRO INTELLIGENCE</b><br/>
<br/>
This section incorporates data from MacroMicro, tracking leading indicators across equity markets,
AI infrastructure, semiconductor trade flows, and institutional positioning.<br/>
<br/>
<b>Key Focus Areas:</b><br/>
• <b>AI/Tech Infrastructure:</b> Semiconductor equipment billings, Taiwan exports, AI patent activity<br/>
• <b>Leading Indicators:</b> US LEI vs. S&P 500, IT investment contribution to GDP<br/>
• <b>Crypto/Digital Assets:</b> Bitcoin mining costs, institutional adoption signals<br/>
• <b>Global Talent Flows:</b> AI talent migration patterns (forward-looking innovation proxy)<br/>
<br/>
These charts provide context for sectoral leadership, technological adoption cycles, and
cross-asset correlations.
""",

        'tradingview': """
<b>SECTION III: TECHNICAL ANALYSIS - KEY NAMES</b><br/>
<br/>
Technical setups for high-conviction individual names across semiconductors, financials,
crypto exposure, and mega-cap tech. These charts identify support/resistance levels,
trend strength, and potential inflection points.<br/>
<br/>
<b>Coverage:</b><br/>
• <b>Semiconductors:</b> NVDA, ASML, TSM (AI infrastructure plays)<br/>
• <b>Financials:</b> JPM, GS (credit cycle proxies)<br/>
• <b>Crypto Exposure:</b> COIN, MSTR, MARA (digital asset beta)<br/>
• <b>Mega-Cap Tech:</b> MSFT (secular growth + AI leverage)<br/>
• <b>Credit Markets:</b> HYG (high-yield bond ETF - credit risk sentiment)<br/>
<br/>
Charts include trendlines, volume analysis, and key technical levels for tactical positioning.
"""
    }
    return intros.get(section_name, "")

def get_indicator_annotation(chart_name):
    """Brief annotation for each proprietary indicator chart"""
    annotations = {
        'MRI_Macro_Risk_Index.png':
            "<b>Macro Risk Index (MRI):</b> Composite systemic risk gauge. Readings >+1σ indicate elevated risk not priced into markets. Current elevated reading driven by low liquidity cushion and rising labor fragility.",

        'MRI_Macro_Risk_Index_components.png':
            "<b>MRI Component Breakdown:</b> Shows contribution of each sub-indicator to overall MRI. Useful for identifying which risk factors are driving the composite signal.",

        '01_LCI_Liquidity_Cushion_Index.png':
            "<b>Liquidity Cushion Index (LCI):</b> Tracks Fed RRP + bank reserves relative to GDP. Negative readings indicate banking system liquidity stress. Currently at critically low levels.",

        '02_LFI_Labor_Fragility_Index.png':
            "<b>Labor Fragility Index (LFI):</b> Measures labor market deterioration via long-term unemployment, declining quits, and reduced hiring efficiency. Elevated readings precede consumer spending weakness.",

        '03_LDI_Labor_Dynamism_Index.png':
            "<b>Labor Dynamism Index (LDI):</b> Captures job market vitality through quit rates, hiring ratios, and employment churn. Falling dynamism signals structural weakness.",

        '04_CLG_Credit_Labor_Gap.png':
            "<b>Credit-Labor Gap (CLG):</b> Divergence between credit spreads and labor fragility. Positive gaps indicate credit markets under-pricing labor-driven recession risk.",

        '05_YFS_Yield_Funding_Stress.png':
            "<b>Yield-Funding Stress (YFS):</b> Tracks money market stress via SOFR-bill spreads and RRP volatility. Readings >+1σ indicate plumbing issues in short-term funding markets.",

        '06_SVI_Spread_Volatility_Imbalance.png':
            "<b>Spread-Volatility Imbalance (SVI):</b> Compares credit spread levels to VIX. Negative readings indicate equity vol markets pricing more risk than credit markets.",

        '07_EMD_Equity_Momentum_Divergence.png':
            "<b>Equity Momentum Divergence (EMD):</b> Measures discrepancy between S&P 500 momentum and equity risk appetite. Negative readings signal deteriorating breadth.",

        '09_Payrolls_vs_Quits_Divergence.png':
            "<b>Payrolls vs. Quits Divergence:</b> When payroll growth decouples from quit rates, it signals labor hoarding or involuntary employment—both recession precursors.",

        '10_Hours_vs_Employment_Divergence.png':
            "<b>Hours vs. Employment Divergence:</b> Companies cut hours before headcount. Negative divergences are leading indicators of layoffs.",
    }
    return annotations.get(chart_name, "")

# ============================================================================
# CHARTBOOK BUILDER
# ============================================================================

def build_chartbook():
    """Generate the complete premium chartbook PDF"""

    print("=" * 60)
    print("LIGHTHOUSE MACRO - PREMIUM CHARTBOOK GENERATOR")
    print("=" * 60)

    # Load indicator data
    print("\n[1/5] Loading latest indicator values...")
    indicators = load_latest_indicators()
    print(f"   MRI: {indicators['MRI']:.2f}σ")
    print(f"   LCI: {indicators['LCI']:.2f}σ")
    print(f"   LFI: {indicators['LFI']:.2f}σ")

    # Initialize PDF
    print("\n[2/5] Initializing PDF document...")
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )

    story = []

    # ========================================================================
    # COVER PAGE
    # ========================================================================
    print("\n[3/5] Building cover page...")

    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("LIGHTHOUSE MACRO", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(
        "Premium Institutional Chartbook",
        ParagraphStyle('subtitle', parent=styles['Heading2'], alignment=TA_CENTER, textColor=colors.HexColor('#0066CC'))
    ))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(get_intro_text(indicators), body_style))
    story.append(PageBreak())

    # ========================================================================
    # SECTION I: PROPRIETARY INDICATORS
    # ========================================================================
    print("\n[4/5] Adding proprietary indicators section...")

    story.append(Paragraph(get_section_intro('proprietary'), body_style))
    story.append(Spacer(1, 0.3*inch))

    # Priority proprietary charts (most important first)
    priority_charts = [
        'MRI_Macro_Risk_Index.png',
        'MRI_Macro_Risk_Index_components.png',
        '01_LCI_Liquidity_Cushion_Index.png',
        '02_LFI_Labor_Fragility_Index.png',
        '03_LDI_Labor_Dynamism_Index.png',
        '04_CLG_Credit_Labor_Gap.png',
        '05_YFS_Yield_Funding_Stress.png',
        '06_SVI_Spread_Volatility_Imbalance.png',
        '07_EMD_Equity_Momentum_Divergence.png',
        '09_Payrolls_vs_Quits_Divergence.png',
        '10_Hours_vs_Employment_Divergence.png',
        '11_LCI_Components.png',
        '12_LFI_Components.png',
        '13_LDI_Components.png',
        '16_HY_OAS_Timeline.png',
        '17_VIX_Timeline.png',
        '18_Unemployment_Rate.png',
        '19_Job_Openings.png',
        '25_Yield_Curve_10Y2Y.png',
    ]

    for chart_file in priority_charts:
        chart_path = os.path.join(PROP_CHARTS, chart_file)
        if os.path.exists(chart_path):
            # Add annotation
            annotation = get_indicator_annotation(chart_file)
            if annotation:
                story.append(Paragraph(annotation, indicator_style))
                story.append(Spacer(1, 0.1*inch))

            # Add chart
            img = Image(chart_path, width=6.5*inch, height=4.5*inch)
            story.append(img)
            story.append(Spacer(1, 0.2*inch))

            print(f"   ✓ Added {chart_file}")

    story.append(PageBreak())

    # ========================================================================
    # SECTION II: MACROMICRO CHARTS
    # ========================================================================
    print("\n[5/5] Adding MacroMicro section...")

    story.append(Paragraph(get_section_intro('macromicro'), body_style))
    story.append(Spacer(1, 0.3*inch))

    macro_files = sorted([f for f in os.listdir(MACRO_CHARTS) if f.endswith('.png')])
    for chart_file in macro_files:
        chart_path = os.path.join(MACRO_CHARTS, chart_file)
        img = Image(chart_path, width=6.5*inch, height=4.5*inch)
        story.append(img)
        story.append(Spacer(1, 0.3*inch))
        print(f"   ✓ Added {chart_file}")

    story.append(PageBreak())

    # ========================================================================
    # SECTION III: TRADINGVIEW TECHNICALS
    # ========================================================================

    if os.path.exists(TV_CHARTS):
        print("\n[6/6] Adding TradingView section...")

        story.append(Paragraph(get_section_intro('tradingview'), body_style))
        story.append(Spacer(1, 0.3*inch))

        tv_files = sorted([f for f in os.listdir(TV_CHARTS) if f.endswith('.png')])
        for chart_file in tv_files:
            chart_path = os.path.join(TV_CHARTS, chart_file)

            # Extract ticker from filename
            ticker = chart_file.split('_')[0]
            story.append(Paragraph(f"<b>{ticker}</b>",
                ParagraphStyle('ticker', parent=styles['Heading3'], textColor=colors.HexColor('#003366'))
            ))
            story.append(Spacer(1, 0.1*inch))

            img = Image(chart_path, width=6.5*inch, height=4.5*inch)
            story.append(img)
            story.append(Spacer(1, 0.3*inch))
            print(f"   ✓ Added {chart_file}")

    # ========================================================================
    # BUILD PDF
    # ========================================================================
    print("\n" + "=" * 60)
    print("BUILDING PDF...")
    print("=" * 60)

    doc.build(story, canvasmaker=ChartbookTemplate)

    # Get file size
    file_size = os.path.getsize(OUTPUT_PDF) / (1024 * 1024)

    print("\n" + "=" * 60)
    print("CHARTBOOK COMPLETE!")
    print("=" * 60)
    print(f"\nOutput: {OUTPUT_PDF}")
    print(f"Size: {file_size:.1f} MB")
    print(f"Date: {indicators['date']}")
    print(f"\nCurrent MRI: {indicators['MRI']:.2f}σ")
    print("\n✓ Ready for distribution!")
    print("=" * 60)

if __name__ == "__main__":
    build_chartbook()
