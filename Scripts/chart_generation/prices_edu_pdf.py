#!/usr/bin/env python3
"""
Generate Lighthouse Macro branded PDF for Prices Educational Article.
Style matches generate_two_books_pdf.py (the canonical LHM PDF style).
"""

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, HRFlowable
)
from PIL import Image as PILImage

# ============================================
# BRAND COLORS (matches Two Books PDF)
# ============================================
OCEAN_BLUE = colors.HexColor('#0089D1')
DUSK_ORANGE = colors.HexColor('#FF6723')
DARK_GRAY = colors.HexColor('#333333')
LIGHT_GRAY = colors.HexColor('#F5F5F5')
MUTED_GRAY = colors.HexColor('#555555')
WHITE = colors.white

# ============================================
# PATHS
# ============================================
BASE_PATH = '/Users/bob/LHM'
ARTICLE_DIR = f'{BASE_PATH}/Outputs/Educational_Charts/Prices_Post_2'
CHART_DIR = f'{ARTICLE_DIR}/white'
DARK_CHART_DIR = f'{ARTICLE_DIR}/dark'
OUTPUT_PDF = f'{ARTICLE_DIR}/The Last Mile Problem - What Inflation Data Actually Tells Us.pdf'

PAGE_W, PAGE_H = letter
CONTENT_W = PAGE_W - 1.2 * inch  # 0.6" margins each side


def create_header_footer(canvas, doc):
    """Exact match of Two Books PDF header/footer."""
    canvas.saveState()

    # Header bar — full width, Ocean 70% + Dusk 30%
    canvas.setFillColor(OCEAN_BLUE)
    canvas.rect(0, PAGE_H - 0.4 * inch, PAGE_W * 0.7, 0.4 * inch, fill=1, stroke=0)
    canvas.setFillColor(DUSK_ORANGE)
    canvas.rect(PAGE_W * 0.7, PAGE_H - 0.4 * inch, PAGE_W * 0.3, 0.4 * inch, fill=1, stroke=0)

    # Header text — white on colored bar
    canvas.setFillColor(WHITE)
    canvas.setFont('Helvetica-Bold', 10)
    canvas.drawString(0.5 * inch, PAGE_H - 0.28 * inch, "LIGHTHOUSE MACRO")
    canvas.drawRightString(PAGE_W - 0.5 * inch, PAGE_H - 0.28 * inch, "Prices: The Last Mile")

    # Footer text
    canvas.setFillColor(DARK_GRAY)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(0.5 * inch, 0.4 * inch, f"Generated: {datetime.now().strftime('%Y-%m-%d')}")
    canvas.drawCentredString(PAGE_W / 2, 0.4 * inch, "MACRO, ILLUMINATED.")
    canvas.drawRightString(PAGE_W - 0.5 * inch, 0.4 * inch, f"Page {doc.page}")

    # Footer accent bar
    canvas.setFillColor(OCEAN_BLUE)
    canvas.rect(0, 0.25 * inch, PAGE_W * 0.7, 0.05 * inch, fill=1, stroke=0)
    canvas.setFillColor(DUSK_ORANGE)
    canvas.rect(PAGE_W * 0.7, 0.25 * inch, PAGE_W * 0.3, 0.05 * inch, fill=1, stroke=0)

    canvas.restoreState()


# ============================================
# STYLES (matches Two Books PDF)
# ============================================
_base = getSampleStyleSheet()

title_style = ParagraphStyle(
    'LHMTitle',
    parent=_base['Heading1'],
    fontSize=28,
    textColor=OCEAN_BLUE,
    spaceAfter=6,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold',
)

subtitle_style = ParagraphStyle(
    'LHMSubtitle',
    parent=_base['Normal'],
    fontSize=14,
    textColor=DARK_GRAY,
    spaceAfter=20,
    alignment=TA_CENTER,
    fontName='Helvetica',
)

h1_style = ParagraphStyle(
    'LHMH1',
    parent=_base['Heading1'],
    fontSize=18,
    textColor=OCEAN_BLUE,
    spaceBefore=20,
    spaceAfter=12,
    fontName='Helvetica-Bold',
)

h2_style = ParagraphStyle(
    'LHMH2',
    parent=_base['Heading2'],
    fontSize=14,
    textColor=OCEAN_BLUE,
    spaceBefore=16,
    spaceAfter=8,
    fontName='Helvetica-Bold',
)

body_style = ParagraphStyle(
    'LHMBody',
    parent=_base['Normal'],
    fontSize=10,
    textColor=DARK_GRAY,
    spaceAfter=8,
    alignment=TA_JUSTIFY,
    fontName='Helvetica',
    leading=14,
)

italic_style = ParagraphStyle(
    'LHMItalic',
    parent=body_style,
    fontName='Helvetica-Oblique',
    textColor=OCEAN_BLUE,
)

bullet_style = ParagraphStyle(
    'LHMBullet',
    parent=body_style,
    leftIndent=20,
    bulletIndent=10,
    spaceAfter=4,
)

caption_style = ParagraphStyle(
    'LHMCaption',
    parent=_base['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=9,
    leading=12,
    textColor=MUTED_GRAY,
    alignment=TA_CENTER,
    spaceAfter=12,
)

footer_style = ParagraphStyle(
    'LHMFooter',
    parent=_base['Normal'],
    fontName='Helvetica',
    fontSize=8,
    leading=11,
    textColor=MUTED_GRAY,
    alignment=TA_CENTER,
)

section_label_style = ParagraphStyle(
    'LHMSectionLabel',
    parent=_base['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=13,
    textColor=OCEAN_BLUE,
    spaceAfter=4,
)


def lhm_table(data, col_widths):
    """Create a table with the standard LHM style (Ocean header, Ocean grid)."""
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), OCEAN_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, OCEAN_BLUE),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t


def get_chart_path(filename):
    """Get chart path, preferring white theme."""
    white_path = os.path.join(CHART_DIR, filename)
    dark_path = os.path.join(DARK_CHART_DIR, filename)
    if os.path.exists(white_path):
        return white_path
    elif os.path.exists(dark_path):
        return dark_path
    return None


def add_chart(story, filename, caption_text):
    """Add a chart image with caption."""
    path = get_chart_path(filename)
    if path is None:
        story.append(Paragraph(f'[Chart missing: {filename}]', italic_style))
        return

    img = PILImage.open(path)
    aspect = img.height / img.width
    img_w = CONTENT_W
    img_h = img_w * aspect

    max_h = 4.2 * inch
    if img_h > max_h:
        img_h = max_h
        img_w = img_h / aspect

    chart_img = Image(path, width=img_w, height=img_h)
    chart_img.hAlign = 'CENTER'

    story.append(Spacer(1, 6))
    story.append(chart_img)
    story.append(Spacer(1, 4))
    story.append(Paragraph(caption_text, caption_style))


def build_pdf():
    """Build the full branded PDF matching Two Books style."""

    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        rightMargin=0.6 * inch,
        leftMargin=0.6 * inch,
        topMargin=0.8 * inch,
        bottomMargin=0.7 * inch,
    )

    story = []

    # ==========================================
    # TITLE PAGE
    # ==========================================
    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph("THE LAST MILE", title_style))
    story.append(Paragraph("PROBLEM", title_style))
    story.append(Spacer(1, 0.3 * inch))

    # Accent bar
    accent = Table([['']], colWidths=[4 * inch])
    accent.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), OCEAN_BLUE),
        ('LINEBELOW', (0, 0), (0, 0), 4, DUSK_ORANGE),
    ]))
    story.append(accent)

    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("What Inflation Data Actually Tells Us", subtitle_style))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(
        '<i>"The headline is improving. The details are stuck.<br/>'
        'This is the last mile problem."</i>',
        italic_style
    ))
    story.append(Spacer(1, 0.8 * inch))
    story.append(Paragraph("Lighthouse Macro", subtitle_style))
    story.append(Paragraph("Pillar 2 of 12 | Educational Series", subtitle_style))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(
        "Bob Sheehan, CFA, CMT<br/>Founder &amp; Chief Investment Officer",
        body_style
    ))

    story.append(PageBreak())

    # ==========================================
    # HOOK / INTRO
    # ==========================================
    story.append(Paragraph(
        "Inflation is at 2.7%. Mission accomplished, right?",
        ParagraphStyle('Hook', parent=body_style, fontSize=12, fontName='Helvetica-Oblique',
                       spaceAfter=10, leading=17)
    ))
    story.append(Paragraph(
        "Not so fast. That headline number, the Consumer Price Index, isn't even what the Fed targets. "
        "The Fed watches Core PCE, which sits at 2.8%. That's 40% above the 2% goal. And underneath the surface:",
        body_style
    ))

    for b in [
        "Core services inflation is running at 3.0%, double core goods",
        "Sticky CPI is at 3.0%, 1.5x the target, and barely budging",
        "Shelter, 34% of the CPI basket, is still mechanically unwinding from its 2023 peak",
        "The Dallas Fed Trimmed Mean, which strips outlier noise, confirms the stickiness is broad-based at 2.5%",
    ]:
        story.append(Paragraph(f'• {b}', bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'The headline is improving. The details are stuck. This is the "last mile" problem, '
        "and it's why the Fed remains boxed in.",
        body_style
    ))

    story.append(PageBreak())

    # ==========================================
    # SECTION 1: The Great Divergence
    # ==========================================
    story.append(Paragraph('THE GREAT DIVERGENCE', h1_style))
    story.append(Paragraph(
        'The single most important chart in inflation right now is the split between goods and services.',
        body_style
    ))

    add_chart(story, 'chart_01_goods_vs_services.png',
              'Figure 1: Core goods CPI vs. core services CPI. The divergence is the defining feature of the current inflation regime.')

    story.append(Paragraph(
        "Core goods are effectively deflating. Core services remain elevated. This isn't a unified "
        '"inflation" story. It\'s two completely different economies running at two completely different speeds.',
        body_style
    ))
    story.append(Paragraph(
        "Goods inflation was always the transitory part. Supply chains healed. Inventories rebuilt. "
        "China exported deflation. The strong dollar made imports cheaper. That story is over.",
        body_style
    ))
    story.append(Paragraph(
        "Services inflation is the structural part. It's driven by wages, rents, and insurance, "
        "components that don't respond to supply chain fixes or monetary policy in the same way. "
        "This is where the last mile problem lives.",
        body_style
    ))

    story.append(PageBreak())

    # ==========================================
    # SECTION 2: The Gap That Matters
    # ==========================================
    story.append(Paragraph('THE GAP THAT MATTERS', h1_style))
    story.append(Paragraph(
        "Here's the distinction that separates informed analysis from headlines: "
        "the Fed doesn't target CPI. It targets Core PCE.",
        body_style
    ))

    add_chart(story, 'chart_02_headline_vs_core.png',
              "Figure 2: Headline CPI vs. Core PCE. The Fed watches Core PCE, and it's still meaningfully above target.")

    story.append(Paragraph(
        "CPI and PCE measure different things. CPI uses fixed weights (what people bought last year). "
        "PCE uses chain-weighted spending (what people are buying now). PCE also captures a broader "
        "set of expenditures, including employer-provided healthcare.",
        body_style
    ))
    story.append(Paragraph(
        "The practical result: PCE tends to run slightly below CPI because it accounts for substitution "
        "effects. When beef gets expensive, people buy chicken. CPI misses that. PCE captures it. "
        "This is why the Fed chose PCE as its target.",
        body_style
    ))
    story.append(Paragraph(
        'At 2.8%, Core PCE is 40% above the 2% goal. That\'s not "close to target." '
        "That's still meaningfully elevated.",
        body_style
    ))

    story.append(PageBreak())

    # ==========================================
    # SECTION 3: The Shelter Lag Trap
    # ==========================================
    story.append(Paragraph('THE SHELTER LAG TRAP', h1_style))
    story.append(Paragraph(
        "Shelter is 34% of the CPI basket. It's the single largest component. "
        "And it operates on a mechanical lag that distorts the headline number.",
        body_style
    ))

    add_chart(story, 'chart_03_shelter_lag.png',
              "Figure 3: Shelter CPI, Rent of Primary Residence, and Owners' Equivalent Rent. All three are declining but remain above target.")

    story.append(Paragraph(
        "Here's how the lag works: the BLS measures shelter through surveys of existing leases. "
        "When market rents spike (as they did in 2021-2022), it takes 12-18 months for those increases "
        "to flow through the lease renewal cycle into CPI. The same works in reverse. Market rents peaked "
        "in early 2022 and have been decelerating since. But CPI shelter didn't peak until March 2023.",
        body_style
    ))
    story.append(Paragraph(
        "The good news: the shelter decline is baked in. Market rents have decelerated substantially, "
        "and that will continue to flow through CPI over the next several quarters.",
        body_style
    ))
    story.append(Paragraph(
        "The bad news: even after shelter normalizes, services ex-shelter remains sticky. "
        "Shelter was masking the problem, not causing it.",
        body_style
    ))

    story.append(PageBreak())

    # ==========================================
    # SECTION 4: The Persistence Problem
    # ==========================================
    story.append(Paragraph('THE PERSISTENCE PROBLEM', h1_style))
    story.append(Paragraph(
        "The Atlanta Fed decomposes CPI into two categories that reveal the structural nature of current inflation.",
        body_style
    ))

    add_chart(story, 'chart_04_sticky_vs_flexible.png',
              'Figure 4: Sticky CPI vs. Flexible CPI (shifted 12 months). Flexible inflation leads Sticky by roughly 12 months.')

    story.append(Paragraph(
        '<b>Flexible CPI</b> includes items with prices that change frequently: gasoline, food, airfares. '
        "These respond quickly to supply and demand. Flexible CPI has normalized. Mission accomplished on the transitory components.",
        body_style
    ))
    story.append(Paragraph(
        '<b>Sticky CPI</b> includes items where prices change infrequently: rent, insurance, medical care, education. '
        "These embed expectations and wage costs. They're slow to rise and slow to fall. "
        "Sticky CPI at 3.0% is 1.5x the 2% target.",
        body_style
    ))
    story.append(Paragraph(
        "The chart shows flexible inflation shifted forward 12 months to reveal the lead relationship. "
        "The correlation is clear: what happens in flexible prices today flows into sticky prices roughly a year later.",
        body_style
    ))
    story.append(Paragraph(
        "This is why we track persistence. Headline disinflation is mostly a flexible-price story. "
        "The structural floor, set by sticky prices, hasn't broken. Until sticky CPI moves decisively "
        "toward 2%, the last mile remains incomplete.",
        body_style
    ))

    story.append(PageBreak())

    # ==========================================
    # SECTION 5: The Pipeline
    # ==========================================
    story.append(Paragraph('THE PIPELINE: PPI LEADS CPI', h1_style))
    story.append(Paragraph(
        "Producer prices are the pipeline signal. What manufacturers and service providers pay "
        "eventually passes through to consumers.",
        body_style
    ))

    add_chart(story, 'chart_05_ppi_leads_cpi.png',
              'Figure 5: PPI Final Demand vs. CPI. When PPI is below CPI, disinflationary pressure is building. When above, inflationary pressure is in the pipeline.')

    story.append(Paragraph(
        "The relationship is straightforward: PPI leads CPI by 3-6 months. When PPI runs below CPI, "
        "producers are absorbing cost declines that haven't yet passed through to consumers. That's disinflationary.",
        body_style
    ))
    story.append(Paragraph(
        "When PPI runs above CPI, as it does now, producers are facing cost increases that will eventually "
        "pass through. That's inflationary pressure building in the pipeline.",
        body_style
    ))

    story.append(PageBreak())

    # ==========================================
    # SECTION 6: Expectations
    # ==========================================
    story.append(Paragraph('INFLATION EXPECTATIONS: ARE THEY ANCHORED?', h1_style))
    story.append(Paragraph(
        "Inflation expectations are arguably more important than inflation itself. If businesses and "
        "consumers expect inflation to remain elevated, they price accordingly. Wages get negotiated higher. "
        "Prices get set higher. Expectations become self-fulfilling.",
        body_style
    ))

    add_chart(story, 'chart_06_expectations.png',
              'Figure 6: The 5-Year, 5-Year Forward Inflation Rate vs. University of Michigan 1-Year Consumer Expectations.')

    story.append(Paragraph("Two measures tell different stories:", body_style))
    story.append(Paragraph(
        "<b>5Y5Y Forward</b> (bond market expectations) sits at 2.2%. This is the market's view of where "
        "inflation will be 5-10 years from now. It's drifting slightly above the 2% anchor but hasn't broken "
        "the 3% danger zone. Professional investors aren't panicking.",
        body_style
    ))
    story.append(Paragraph(
        '<b>UMich 1Y Expectations</b> (consumer expectations) are at 4.4%. Consumers still <i>feel</i> inflation. '
        "Grocery bills, insurance premiums, rent: these are the prices people interact with daily. "
        "They don't care that goods are deflating if their rent is up 5%.",
        body_style
    ))
    story.append(Paragraph(
        "The risk: if 5Y5Y breaks above 3%, the Fed loses the expectations anchor. That would force "
        "aggressive tightening regardless of growth conditions. For now, it's drifting, not de-anchored. "
        "But it bears watching.",
        body_style
    ))

    story.append(PageBreak())

    # ==========================================
    # SECTION 7: Trimmed Mean
    # ==========================================
    story.append(Paragraph('THE SIGNAL BENEATH THE NOISE', h1_style))
    story.append(Paragraph(
        "The Dallas Fed Trimmed Mean PCE strips the most extreme price changes each month, "
        "both high and low, to reveal the underlying trend.",
        body_style
    ))

    add_chart(story, 'chart_07_trimmed_mean.png',
              'Figure 7: Dallas Fed Trimmed Mean PCE vs. Core PCE. The trimmed mean strips outlier noise and confirms the underlying trend.')

    story.append(Paragraph(
        "During 2021-2023, the trimmed mean was more accurate than core PCE at capturing the true inflation trend. "
        "It avoided the distortions from volatile components like used cars and airfares.",
        body_style
    ))
    story.append(Paragraph(
        "At 2.5%, the trimmed mean is telling us the same story as sticky CPI: the underlying inflation trend "
        "is above target, and it's not just one or two outlier categories driving it. The stickiness is broad-based.",
        body_style
    ))

    story.append(PageBreak())

    # ==========================================
    # SECTION 8: Wages vs Prices
    # ==========================================
    story.append(Paragraph('THE SPIRAL CHECK', h1_style))
    story.append(Paragraph(
        "The wage-price spiral is the inflation scenario that keeps central bankers awake. Workers demand "
        "higher wages because prices are rising. Businesses raise prices to cover higher labor costs. Repeat.",
        body_style
    ))

    add_chart(story, 'chart_08_wages_vs_prices.png',
              'Figure 8: ECI Total Compensation vs. Core PCE. Wages above inflation means positive real wages but sticky services.')

    story.append(Paragraph(
        "ECI Total Compensation is running at 3.6%, above Core PCE at 2.8%. That's positive real wages, "
        "which is good for workers and consumers. But it's also the reason services inflation won't come down "
        "easily. Labor costs are the largest input for most service businesses.",
        body_style
    ))
    story.append(Paragraph(
        "The good news: there's no spiral. Wages aren't accelerating. They're decelerating from their 2022 peak. "
        "The bad news: wages above inflation is an equilibrium that sustains services inflation above target. "
        "It's stable, but it's stable at the wrong level.",
        body_style
    ))

    story.append(PageBreak())

    # ==========================================
    # SECTION 9: Dollar Channel
    # ==========================================
    story.append(Paragraph('THE DOLLAR CHANNEL', h1_style))
    story.append(Paragraph(
        "The trade-weighted dollar is the mechanism behind goods deflation.",
        body_style
    ))

    add_chart(story, 'chart_09_dollar_goods.png',
              'Figure 9: Trade-weighted dollar (inverted) vs. Core Goods CPI, shifted 18 months to show the lead relationship.')

    story.append(Paragraph(
        "A strong dollar makes imports cheaper. Since the US imports a massive share of its goods consumption, "
        "dollar strength flows directly into goods prices with a 9-18 month lag. The current goods deflation "
        "isn't a mystery. It's the mechanical result of prior dollar strength.",
        body_style
    ))
    story.append(Paragraph(
        "The implication: if the dollar weakens (which it would in a rate-cutting cycle), goods deflation reverses. "
        "That removes one of the few forces currently pulling headline inflation lower. The Fed's own easing "
        "could reignite goods inflation.",
        body_style
    ))

    story.append(PageBreak())

    # ==========================================
    # SECTION 10: PCI Composite
    # ==========================================
    story.append(Paragraph('PUTTING IT ALL TOGETHER: THE PRICES COMPOSITE', h1_style))
    story.append(Paragraph(
        "We synthesize the key inflation signals into a composite we call the Prices Composite Index (PCI):",
        body_style
    ))

    add_chart(story, 'chart_10_pci_composite.png',
              'Figure 10: The Prices Composite Index (PCI). Regime bands show the inflation environment.')

    story.append(Paragraph('The PCI combines:', body_style))
    for c in [
        "Core PCE momentum (3-month annualized)",
        "Services inflation trend",
        "Shelter trajectory",
        "Sticky price persistence",
        "Expectations anchoring (5Y5Y forward)",
        "Goods deflation offset (inverted)",
    ]:
        story.append(Paragraph(f'• {c}', bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Each component is z-scored over a rolling 60-month window and weighted by its historical importance "
        "to the inflation outlook.",
        body_style
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph('Regime Bands', h2_style))

    regime_data = [
        ['PCI Range', 'Regime', 'Interpretation'],
        ['> +1.5', 'Crisis', 'Inflation emergency'],
        ['+1.0 to +1.5', 'High', 'Aggressive tightening needed'],
        ['+0.5 to +1.0', 'Elevated', "Fed can't ease aggressively"],
        ['-0.5 to +0.5', 'On Target', 'Policy flexibility'],
        ['< -0.5', 'Deflationary', 'Easing urgently needed'],
    ]
    story.append(lhm_table(regime_data, [1.5 * inch, 1.5 * inch, 3.2 * inch]))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "The specific weights are our proprietary work, but the signal is clear: when multiple inflation "
        "indicators remain elevated simultaneously, the composite stays in restrictive territory, and the Fed stays boxed in.",
        body_style
    ))

    story.append(PageBreak())

    # ==========================================
    # WHAT IT'S SAYING NOW
    # ==========================================
    story.append(Paragraph("WHAT IT'S SAYING NOW", h1_style))

    story.append(Paragraph('<b>The headline is improving:</b>', body_style))
    for b in [
        "CPI at 2.7%, down from 9.1% peak",
        "Core goods deflating",
        "Shelter mechanically declining",
    ]:
        story.append(Paragraph(f'• {b}', bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph('<b>The details are stuck:</b>', body_style))
    for b in [
        "Core PCE at 2.8%, still 40% above target",
        "Services at 3.0%, barely budging",
        "Sticky CPI at 3.0%, 1.5x target",
        "Trimmed Mean at 2.5%, confirming breadth",
        "Wages above inflation, sustaining services stickiness",
    ]:
        story.append(Paragraph(f'• {b}', bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "This is the bifurcated reality. Goods are solved. Services are stuck. The last mile isn't a distance "
        "problem. It's a composition problem. And composition problems don't respond to time alone.",
        body_style
    ))

    story.append(PageBreak())

    # ==========================================
    # WHAT TO WATCH
    # ==========================================
    story.append(Paragraph('WHAT TO WATCH', h1_style))
    story.append(Paragraph(
        "If you want to track the inflation picture yourself, here's a practical watchlist:",
        body_style
    ))

    # Core Trend
    story.append(Paragraph('Core Trend', h2_style))
    story.append(lhm_table(
        [
            ['Indicator', 'Source', 'Frequency', 'Watch For'],
            ['Core PCE YoY', 'FRED: PCEPILFE', 'Monthly', 'Sustained move below 2.5%'],
            ['Trimmed Mean PCE', 'FRED: PCETRIM12M...', 'Monthly', 'Convergence toward 2%'],
            ['Sticky CPI', 'Atlanta Fed', 'Monthly', 'Break below 3%'],
        ],
        [1.5 * inch, 1.8 * inch, 0.9 * inch, 2.0 * inch]
    ))
    story.append(Spacer(1, 10))

    # Components
    story.append(Paragraph('Components', h2_style))
    story.append(lhm_table(
        [
            ['Indicator', 'Source', 'Frequency', 'Watch For'],
            ['Shelter CPI', 'FRED: CUSR0000SAH1', 'Monthly', 'Continued mechanical decline'],
            ['Services ex-Shelter', 'BLS', 'Monthly', 'This is the true last mile'],
            ['Core Goods CPI', 'FRED: CUSR...SACL1E', 'Monthly', 'Reversal from deflation'],
        ],
        [1.5 * inch, 1.8 * inch, 0.9 * inch, 2.0 * inch]
    ))
    story.append(Spacer(1, 10))

    # Expectations
    story.append(Paragraph('Expectations', h2_style))
    story.append(lhm_table(
        [
            ['Indicator', 'Source', 'Frequency', 'Watch For'],
            ['5Y5Y Forward', 'FRED: T5YIFR', 'Daily', 'Break above 2.5% / 3%'],
            ['UMich 1Y', 'Univ. of Michigan', 'Monthly', 'Convergence toward 3%'],
        ],
        [1.5 * inch, 1.8 * inch, 0.9 * inch, 2.0 * inch]
    ))
    story.append(Spacer(1, 10))

    # Pipeline
    story.append(Paragraph('Pipeline', h2_style))
    story.append(lhm_table(
        [
            ['Indicator', 'Source', 'Frequency', 'Watch For'],
            ['PPI Final Demand', 'FRED: PPIFIS', 'Monthly', 'PPI above CPI = inflationary'],
            ['ECI Total Comp', 'FRED: ECIALLCIV', 'Quarterly', 'Deceleration below 3.5%'],
        ],
        [1.5 * inch, 1.8 * inch, 0.9 * inch, 2.0 * inch]
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "The signal isn't any single indicator. It's the composition. When services moderate, sticky prices "
        "break lower, and expectations re-anchor, that's when the last mile is complete.",
        body_style
    ))

    story.append(PageBreak())

    # ==========================================
    # BOTTOM LINE
    # ==========================================
    story.append(Paragraph('THE BOTTOM LINE', h1_style))
    story.append(Paragraph(
        "The last mile of disinflation is a services problem, not an inflation problem in the traditional sense. "
        "Goods are deflating. The shelter lag is unwinding mechanically. But services ex-shelter remain stuck, "
        "held up by wage growth that's positive in real terms but inconsistent with 2% inflation.",
        body_style
    ))
    story.append(Paragraph(
        "The Fed is boxed in. Cut too aggressively and you risk reigniting inflation through a weaker dollar "
        "and easier financial conditions. Stay too tight and you risk breaking the labor market (see Pillar 1) "
        "while waiting for services to moderate.",
        body_style
    ))
    story.append(Paragraph(
        "The framework says: watch the composition, not the headline. The headline will reach 2% eventually. "
        "The question is whether it gets there through genuine services moderation or through a recession that "
        "crushes demand. The flows that lead, not the stocks that lag, will tell us which path we're on.",
        body_style
    ))

    # Closing
    story.append(Spacer(1, 0.5 * inch))
    story.append(HRFlowable(width="80%", thickness=2, color=OCEAN_BLUE, spaceBefore=10, spaceAfter=20))

    closing_style = ParagraphStyle(
        'Closing',
        parent=body_style,
        alignment=TA_CENTER,
        fontSize=12,
        textColor=OCEAN_BLUE,
        fontName='Helvetica-Oblique',
    )

    story.append(Paragraph(
        "<i>Next in the series: Pillar 3 (Growth) and the Second Derivative.<br/>"
        "Why the rate of change matters more than the level, and what leading<br/>"
        "indicators are saying about the growth trajectory.</i>",
        closing_style
    ))

    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(
        '<b>Join The Watch</b> for the full 12-Pillar Educational Series.',
        ParagraphStyle('CTA', parent=body_style, alignment=TA_CENTER, fontSize=11)
    ))

    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("MACRO, ILLUMINATED.", title_style))

    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(
        "Bob Sheehan, CFA, CMT<br/>"
        "Founder &amp; Chief Investment Officer<br/>"
        "Lighthouse Macro<br/>"
        "bob@lighthousemacro.com | @LHMacro",
        body_style
    ))

    # Data sources / disclosure
    story.append(Spacer(1, 0.5 * inch))
    story.append(HRFlowable(width="100%", thickness=0.5, color=OCEAN_BLUE, spaceAfter=8))

    disc_style = ParagraphStyle('Disc', parent=body_style, fontSize=8, leading=11, textColor=MUTED_GRAY)
    story.append(Paragraph(
        '<b>Data Sources:</b> Bureau of Labor Statistics (CPI, PPI) · Bureau of Economic Analysis (PCE) · '
        'Atlanta Fed (Sticky/Flexible CPI) · Dallas Fed (Trimmed Mean PCE) · '
        'University of Michigan (Consumer Expectations) · FRED',
        disc_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '<b>Disclosure:</b> This is educational content. Not investment advice. Past patterns don\'t guarantee '
        'future results. The inflation framework is empirically grounded and uses publicly available data. '
        'Composite weightings are proprietary.',
        disc_style
    ))

    # Build
    doc.build(story, onFirstPage=create_header_footer, onLaterPages=create_header_footer)
    print(f'\nPDF generated: {OUTPUT_PDF}')
    return OUTPUT_PDF


if __name__ == '__main__':
    build_pdf()
