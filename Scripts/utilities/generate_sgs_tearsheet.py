#!/usr/bin/env python3
"""Generate SGS Tear Sheet with S&P 500 comparison."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus.flowables import HRFlowable

# Colors
BOFA_BLUE = HexColor('#012169')
BOFA_RED = HexColor('#C41230')
DARK = HexColor('#1a1a1a')
GRAY = HexColor('#666666')
LIGHT_GRAY = HexColor('#f5f5f5')
TABLE_HEADER = HexColor('#012169')

def create_tearsheet():
    doc = SimpleDocTemplate(
        "/Users/bob/SGS_Tearsheet_Jan2020.pdf",
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.4*inch,
        bottomMargin=0.4*inch
    )

    styles = {
        'header': ParagraphStyle(
            'header',
            fontName='Helvetica-Bold',
            fontSize=8,
            textColor=BOFA_BLUE,
        ),
        'title': ParagraphStyle(
            'title',
            fontName='Helvetica-Bold',
            fontSize=18,
            textColor=DARK,
            spaceAfter=4
        ),
        'subtitle': ParagraphStyle(
            'subtitle',
            fontName='Helvetica',
            fontSize=8,
            textColor=GRAY,
            spaceAfter=8
        ),
        'section': ParagraphStyle(
            'section',
            fontName='Helvetica-Bold',
            fontSize=9,
            textColor=DARK,
            spaceBefore=10,
            spaceAfter=4
        ),
        'body': ParagraphStyle(
            'body',
            fontName='Helvetica',
            fontSize=8,
            textColor=DARK,
            alignment=TA_JUSTIFY,
            leading=10
        ),
        'small': ParagraphStyle(
            'small',
            fontName='Helvetica',
            fontSize=7,
            textColor=GRAY,
            leading=9
        ),
        'disclaimer': ParagraphStyle(
            'disclaimer',
            fontName='Helvetica',
            fontSize=6,
            textColor=GRAY,
            leading=7,
            spaceBefore=8
        ),
        'table_header': ParagraphStyle(
            'table_header',
            fontName='Helvetica-Bold',
            fontSize=7,
            textColor=white,
        ),
        'table_cell': ParagraphStyle(
            'table_cell',
            fontName='Helvetica',
            fontSize=7,
            textColor=DARK,
        ),
    }

    story = []

    # Header row
    header_table = Table(
        [[Paragraph("<b>BANK OF AMERICA</b>", styles['header']),
          Paragraph("<b>PRIVATE BANK</b>", ParagraphStyle('right', fontName='Helvetica-Bold', fontSize=8, textColor=BOFA_BLUE, alignment=TA_RIGHT))]],
        colWidths=[4*inch, 3.5*inch]
    )
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(header_table)

    story.append(HRFlowable(width="100%", thickness=2, color=BOFA_RED, spaceAfter=8))

    story.append(Paragraph("MODEL PORTFOLIO – SUMMARY AS OF JANUARY 31, 2020", styles['subtitle']))
    story.append(Paragraph("STRATEGIC GROWTH STRATEGY (SGS)", styles['title']))

    # Strategy description and investment team side by side
    desc_text = """SGS seeks to outperform the S&P 500 over a full market cycle with less volatility than the index. The strategy combines top-down macro analysis with technical signals and bottom-up fundamental research to create a portfolio that is both opportunistic and defensive. Technical analysis identifies optimal entry/exit points, macro analysis informs sector and factor tilts, and rigorous fundamental due diligence ensures quality at the security level. A strict sell discipline protects capital in drawdowns."""

    # Investment Team table
    team_data = [
        [Paragraph("<b>Investment Team</b>", styles['section']), '', ''],
        [Paragraph("<b>Name</b>", styles['table_cell']), Paragraph("<b>Year Joined</b>", styles['table_cell']), Paragraph("<b>Credentials</b>", styles['table_cell'])],
        [Paragraph("Jeffrey Whalen<br/><i>Portfolio Manager</i>", styles['table_cell']), Paragraph("2010", styles['table_cell']), Paragraph("CMT", styles['table_cell'])],
        [Paragraph("Bob Sheehan<br/><i>Associate Portfolio Manager</i>", styles['table_cell']), Paragraph("2015", styles['table_cell']), Paragraph("CFA, CMT", styles['table_cell'])],
        [Paragraph("Adam Betancourt<br/><i>Associate Portfolio Manager</i>", styles['table_cell']), Paragraph("2015", styles['table_cell']), Paragraph("CFA", styles['table_cell'])],
        [Paragraph("Kevin Dawson<br/><i>Analyst</i>", styles['table_cell']), Paragraph("2017", styles['table_cell']), Paragraph("--", styles['table_cell'])],
    ]

    team_table = Table(team_data, colWidths=[1.3*inch, 0.5*inch, 0.8*inch])
    team_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('SPAN', (0, 0), (2, 0)),
        ('LINEBELOW', (0, 1), (-1, 1), 0.5, GRAY),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_GRAY),
    ]))

    # Left column: description + team
    left_content = [[Paragraph(desc_text, styles['body'])], [Spacer(1, 8)], [team_table]]
    left_table = Table(left_content, colWidths=[2.8*inch])

    # Top 10 Holdings
    holdings_data = [
        [Paragraph("<b>Top Ten Holdings</b>", styles['section']), ''],
        [Paragraph("<b>Security</b>", styles['table_cell']), Paragraph("<b>% of Portfolio</b>", styles['table_cell'])],
        [Paragraph("Microsoft Corporation", styles['table_cell']), Paragraph("8.16", styles['table_cell'])],
        [Paragraph("Apple Inc.", styles['table_cell']), Paragraph("7.66", styles['table_cell'])],
        [Paragraph("Amazon.com, Inc.", styles['table_cell']), Paragraph("6.04", styles['table_cell'])],
        [Paragraph("Mastercard Incorporated Class A", styles['table_cell']), Paragraph("4.43", styles['table_cell'])],
        [Paragraph("Alphabet Inc. Class C", styles['table_cell']), Paragraph("4.16", styles['table_cell'])],
        [Paragraph("salesforce.com, inc.", styles['table_cell']), Paragraph("3.95", styles['table_cell'])],
        [Paragraph("Danaher Corporation", styles['table_cell']), Paragraph("3.92", styles['table_cell'])],
        [Paragraph("Home Depot, Inc.", styles['table_cell']), Paragraph("3.65", styles['table_cell'])],
        [Paragraph("Facebook, Inc. Class A", styles['table_cell']), Paragraph("3.33", styles['table_cell'])],
        [Paragraph("Zoetis, Inc. Class A", styles['table_cell']), Paragraph("3.25", styles['table_cell'])],
    ]

    holdings_table = Table(holdings_data, colWidths=[1.8*inch, 0.8*inch])
    holdings_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('SPAN', (0, 0), (1, 0)),
        ('LINEBELOW', (0, 1), (-1, 1), 0.5, GRAY),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_GRAY),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
    ]))

    # Portfolio Characteristics - SGS vs S&P 500
    char_data = [
        [Paragraph("<b>Portfolio Characteristics</b>", styles['section']), '', ''],
        [Paragraph("<b>Metric</b>", styles['table_cell']), Paragraph("<b>Portfolio</b>", styles['table_cell']), Paragraph("<b>S&P 500</b>", styles['table_cell'])],
        [Paragraph("Weighted Avg Mkt Cap ($MN)", styles['table_cell']), Paragraph("$437,979", styles['table_cell']), Paragraph("$312,851", styles['table_cell'])],
        [Paragraph("Weighted Median Mkt Cap ($MN)", styles['table_cell']), Paragraph("$161,527", styles['table_cell']), Paragraph("$128,670", styles['table_cell'])],
        [Paragraph("# of Securities", styles['table_cell']), Paragraph("39", styles['table_cell']), Paragraph("505", styles['table_cell'])],
        [Paragraph("Dividend Yield", styles['table_cell']), Paragraph("0.92", styles['table_cell']), Paragraph("1.81", styles['table_cell'])],
        [Paragraph("Price/Earnings", styles['table_cell']), Paragraph("29.5", styles['table_cell']), Paragraph("22.5", styles['table_cell'])],
        [Paragraph("Price/Book", styles['table_cell']), Paragraph("6.8", styles['table_cell']), Paragraph("3.5", styles['table_cell'])],
        [Paragraph("Hist 3Yr Sales Growth", styles['table_cell']), Paragraph("16.7", styles['table_cell']), Paragraph("9.7", styles['table_cell'])],
        [Paragraph("Hist 3Yr EPS Growth", styles['table_cell']), Paragraph("23.3", styles['table_cell']), Paragraph("17.5", styles['table_cell'])],
    ]

    char_table = Table(char_data, colWidths=[1.5*inch, 0.7*inch, 0.7*inch])
    char_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('SPAN', (0, 0), (2, 0)),
        ('LINEBELOW', (0, 1), (-1, 1), 0.5, GRAY),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_GRAY),
        ('ALIGN', (1, 1), (2, -1), 'RIGHT'),
    ]))

    # Sector Analysis
    sector_data = [
        [Paragraph("<b>Sector Analysis</b>", styles['section']), '', ''],
        [Paragraph("<b>Sector</b>", styles['table_cell']), Paragraph("<b>Portfolio</b>", styles['table_cell']), Paragraph("<b>S&P 500</b>", styles['table_cell'])],
        [Paragraph("Communication Services", styles['table_cell']), Paragraph("10.49%", styles['table_cell']), Paragraph("10.47%", styles['table_cell'])],
        [Paragraph("Consumer Discretionary", styles['table_cell']), Paragraph("17.39%", styles['table_cell']), Paragraph("9.82%", styles['table_cell'])],
        [Paragraph("Consumer Staples", styles['table_cell']), Paragraph("7.04%", styles['table_cell']), Paragraph("7.23%", styles['table_cell'])],
        [Paragraph("Energy", styles['table_cell']), Paragraph("0.66%", styles['table_cell']), Paragraph("3.87%", styles['table_cell'])],
        [Paragraph("Financials", styles['table_cell']), Paragraph("3.03%", styles['table_cell']), Paragraph("12.60%", styles['table_cell'])],
        [Paragraph("Health Care", styles['table_cell']), Paragraph("13.60%", styles['table_cell']), Paragraph("13.79%", styles['table_cell'])],
        [Paragraph("Industrials", styles['table_cell']), Paragraph("7.65%", styles['table_cell']), Paragraph("9.02%", styles['table_cell'])],
        [Paragraph("Information Technology", styles['table_cell']), Paragraph("38.67%", styles['table_cell']), Paragraph("24.19%", styles['table_cell'])],
        [Paragraph("Materials", styles['table_cell']), Paragraph("1.48%", styles['table_cell']), Paragraph("2.49%", styles['table_cell'])],
        [Paragraph("Real Estate", styles['table_cell']), Paragraph("--", styles['table_cell']), Paragraph("2.97%", styles['table_cell'])],
        [Paragraph("Utilities", styles['table_cell']), Paragraph("--", styles['table_cell']), Paragraph("3.55%", styles['table_cell'])],
    ]

    sector_table = Table(sector_data, colWidths=[1.3*inch, 0.7*inch, 0.7*inch])
    sector_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('SPAN', (0, 0), (2, 0)),
        ('LINEBELOW', (0, 1), (-1, 1), 0.5, GRAY),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_GRAY),
        ('ALIGN', (1, 1), (2, -1), 'RIGHT'),
    ]))

    # Asset Allocation
    alloc_data = [
        [Paragraph("<b>Asset Allocation</b>", styles['section']), '', ''],
        [Paragraph("<b>Region</b>", styles['table_cell']), Paragraph("<b># Securities</b>", styles['table_cell']), Paragraph("<b>Weight</b>", styles['table_cell'])],
        [Paragraph("U.S. Large Cap", styles['table_cell']), Paragraph("29", styles['table_cell']), Paragraph("77.71%", styles['table_cell'])],
        [Paragraph("U.S. Mid Cap", styles['table_cell']), Paragraph("6", styles['table_cell']), Paragraph("11.43%", styles['table_cell'])],
        [Paragraph("International Developed", styles['table_cell']), Paragraph("3", styles['table_cell']), Paragraph("5.42%", styles['table_cell'])],
        [Paragraph("Emerging Markets", styles['table_cell']), Paragraph("1", styles['table_cell']), Paragraph("1.45%", styles['table_cell'])],
    ]

    alloc_table = Table(alloc_data, colWidths=[1.3*inch, 0.7*inch, 0.7*inch])
    alloc_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('SPAN', (0, 0), (2, 0)),
        ('LINEBELOW', (0, 1), (-1, 1), 0.5, GRAY),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_GRAY),
        ('ALIGN', (1, 1), (2, -1), 'RIGHT'),
    ]))

    # Build the main layout
    # Row 1: Description/Team | Holdings | Characteristics
    main_row1 = Table(
        [[left_table, holdings_table, char_table]],
        colWidths=[2.9*inch, 2.7*inch, 2*inch]
    )
    main_row1.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(main_row1)

    story.append(Spacer(1, 8))

    # Row 2: Sector | Allocation
    main_row2 = Table(
        [[sector_table, alloc_table]],
        colWidths=[2.9*inch, 2.9*inch]
    )
    main_row2.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(main_row2)

    # Disclaimer
    disclaimer = """Source: Model portfolio was constructed by the Chief Investment Office for Bank of America. Index data is provided by FactSet as of January 2020. Portfolio characteristics and holdings are subject to change periodically and may not be representative of the model's current characteristics and holdings. The Strategy may underperform its benchmark. There can be no assurance that the strategy will outperform its benchmark. Gross performance results are presented before the deduction of investment advisory fees, custodial fees, and trading commissions. Investing involves risks. There is always the potential of losing money when you invest in securities."""
    story.append(Paragraph(disclaimer, styles['disclaimer']))

    story.append(Paragraph("This information is intended for use in a one-on-one presentation only. Distribution to any other audience is prohibited.",
                          ParagraphStyle('footer', fontName='Helvetica-Bold', fontSize=6, textColor=GRAY, spaceBefore=4)))

    # PAGE 2 - Performance
    story.append(PageBreak())

    # Header
    header_table2 = Table(
        [[Paragraph("<b>BANK OF AMERICA</b>", styles['header']),
          Paragraph("<b>PRIVATE BANK</b>", ParagraphStyle('right', fontName='Helvetica-Bold', fontSize=8, textColor=BOFA_BLUE, alignment=TA_RIGHT))]],
        colWidths=[4*inch, 3.5*inch]
    )
    header_table2.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(header_table2)
    story.append(HRFlowable(width="100%", thickness=2, color=BOFA_RED, spaceAfter=8))

    story.append(Paragraph("MODEL PORTFOLIO – PERFORMANCE & STATISTICS AS OF JANUARY 31, 2020", styles['subtitle']))
    story.append(Paragraph("STRATEGIC GROWTH STRATEGY (SGS)", styles['title']))

    # Performance table
    perf_data = [
        [Paragraph("<b>Performance</b>", styles['section']), '', '', '', '', '', '', '', '', ''],
        ['', Paragraph("<b>Inception</b>", styles['table_cell']), Paragraph("<b>Jan-20</b>", styles['table_cell']),
         Paragraph("<b>4Q 2019</b>", styles['table_cell']), Paragraph("<b>YTD</b>", styles['table_cell']),
         Paragraph("<b>1 Year</b>", styles['table_cell']), Paragraph("<b>3 Year</b>", styles['table_cell']),
         Paragraph("<b>5 Year</b>", styles['table_cell']), Paragraph("<b>FY'19</b>", styles['table_cell']),
         Paragraph("<b>ITD</b>", styles['table_cell'])],
        [Paragraph("<b>SGS</b>", styles['table_cell']), Paragraph("01/01/09", styles['table_cell']),
         Paragraph("3.20%", styles['table_cell']), Paragraph("9.65%", styles['table_cell']),
         Paragraph("3.20%", styles['table_cell']), Paragraph("31.40%", styles['table_cell']),
         Paragraph("21.73%", styles['table_cell']), Paragraph("15.21%", styles['table_cell']),
         Paragraph("38.58%", styles['table_cell']), Paragraph("16.93%", styles['table_cell'])],
        [Paragraph("<b>S&P 500</b>", styles['table_cell']), Paragraph("", styles['table_cell']),
         Paragraph("-0.04%", styles['table_cell']), Paragraph("9.07%", styles['table_cell']),
         Paragraph("-0.04%", styles['table_cell']), Paragraph("21.68%", styles['table_cell']),
         Paragraph("14.54%", styles['table_cell']), Paragraph("12.37%", styles['table_cell']),
         Paragraph("31.49%", styles['table_cell']), Paragraph("14.55%", styles['table_cell'])],
    ]

    perf_table = Table(perf_data, colWidths=[0.6*inch, 0.65*inch, 0.6*inch, 0.6*inch, 0.5*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.5*inch])
    perf_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('SPAN', (0, 0), (9, 0)),
        ('LINEBELOW', (0, 1), (-1, 1), 0.5, GRAY),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_GRAY),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 2), (-1, 2), HexColor('#e8f4e8')),
    ]))
    story.append(perf_table)

    story.append(Spacer(1, 12))

    # Risk Statistics - vs S&P 500
    risk_data1 = [
        [Paragraph("<b>Risk Statistics (02/2017 - 01/2020)</b>", styles['section']), '', '', '', '', '', ''],
        ['', Paragraph("<b>Ann. Return</b>", styles['table_cell']), Paragraph("<b>Ann. Std Dev</b>", styles['table_cell']),
         Paragraph("<b>Beta</b>", styles['table_cell']), Paragraph("<b>Ann. Alpha</b>", styles['table_cell']),
         Paragraph("<b>Sharpe</b>", styles['table_cell']), Paragraph("<b>R-Square</b>", styles['table_cell'])],
        [Paragraph("<b>SGS</b>", styles['table_cell']), Paragraph("21.73", styles['table_cell']),
         Paragraph("13.01", styles['table_cell']), Paragraph("1.06", styles['table_cell']),
         Paragraph("5.32", styles['table_cell']), Paragraph("1.54", styles['table_cell']),
         Paragraph("93.18", styles['table_cell'])],
        [Paragraph("<b>S&P 500</b>", styles['table_cell']), Paragraph("14.54", styles['table_cell']),
         Paragraph("11.95", styles['table_cell']), Paragraph("1.00", styles['table_cell']),
         Paragraph("0.00", styles['table_cell']), Paragraph("1.08", styles['table_cell']),
         Paragraph("100.00", styles['table_cell'])],
    ]

    risk_table1 = Table(risk_data1, colWidths=[0.8*inch, 0.9*inch, 0.9*inch, 0.7*inch, 0.9*inch, 0.7*inch, 0.8*inch])
    risk_table1.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('SPAN', (0, 0), (6, 0)),
        ('LINEBELOW', (0, 1), (-1, 1), 0.5, GRAY),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_GRAY),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 2), (-1, 2), HexColor('#e8f4e8')),
    ]))
    story.append(risk_table1)

    story.append(Spacer(1, 12))

    # Capture Ratios
    risk_data2 = [
        [Paragraph("<b>Capture & Risk-Adjusted Returns (02/2017 - 01/2020)</b>", styles['section']), '', '', '', '', ''],
        ['', Paragraph("<b>Upside Capture %</b>", styles['table_cell']), Paragraph("<b>Downside Capture %</b>", styles['table_cell']),
         Paragraph("<b>Information Ratio</b>", styles['table_cell']), Paragraph("<b>Sortino Ratio</b>", styles['table_cell']),
         Paragraph("<b>Tracking Error</b>", styles['table_cell'])],
        [Paragraph("<b>SGS</b>", styles['table_cell']), Paragraph("102.97", styles['table_cell']),
         Paragraph("75.84", styles['table_cell']), Paragraph("1.57", styles['table_cell']),
         Paragraph("2.35", styles['table_cell']), Paragraph("4.56", styles['table_cell'])],
        [Paragraph("<b>S&P 500</b>", styles['table_cell']), Paragraph("100.00", styles['table_cell']),
         Paragraph("100.00", styles['table_cell']), Paragraph("--", styles['table_cell']),
         Paragraph("1.57", styles['table_cell']), Paragraph("0.00", styles['table_cell'])],
    ]

    risk_table2 = Table(risk_data2, colWidths=[0.8*inch, 1.1*inch, 1.2*inch, 1.1*inch, 1*inch, 1*inch])
    risk_table2.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('SPAN', (0, 0), (5, 0)),
        ('LINEBELOW', (0, 1), (-1, 1), 0.5, GRAY),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_GRAY),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 2), (-1, 2), HexColor('#e8f4e8')),
    ]))
    story.append(risk_table2)

    story.append(Spacer(1, 16))

    # Key Highlights box
    highlights = """<b>KEY PERFORMANCE HIGHLIGHTS vs S&P 500 (3-Year Period)</b><br/><br/>
    • <b>Annualized Outperformance:</b> +719 basis points (21.73% vs 14.54%)<br/>
    • <b>Sortino Ratio:</b> 2.35 vs 1.57 (50% higher risk-adjusted returns)<br/>
    • <b>Upside Capture:</b> 103% (captured more than 100% of market gains)<br/>
    • <b>Downside Capture:</b> 76% (protected capital in drawdowns)<br/>
    • <b>Sharpe Ratio:</b> 1.54 vs 1.08 (43% higher)<br/>
    • <b>Alpha:</b> +5.32% annualized vs benchmark"""

    highlight_table = Table([[Paragraph(highlights, styles['body'])]], colWidths=[6*inch])
    highlight_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, BOFA_BLUE),
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#f0f4f8')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(highlight_table)

    # Disclaimer
    disclaimer2 = """Source: Model portfolio data was constructed by the Chief Investment Office (CIO) for Bank of America. Index data is provided by FactSet as of January 2020. The investment returns presented for the Strategic Growth Strategy - Model Portfolio are simulated; presented gross of Bank of America's Investment Management & Trust fees, transaction costs, and tax withholdings; and do not represent actual trading of client accounts. Past performance is no guarantee of future results. Investing involves risks. There is always the potential of losing money when you invest in securities."""
    story.append(Paragraph(disclaimer2, styles['disclaimer']))

    story.append(Paragraph("This information is intended for use in a one-on-one presentation only. Distribution to any other audience is prohibited.",
                          ParagraphStyle('footer', fontName='Helvetica-Bold', fontSize=6, textColor=GRAY, spaceBefore=4)))

    doc.build(story)
    print("SGS Tearsheet saved to: /Users/bob/SGS_Tearsheet_Jan2020.pdf")

if __name__ == "__main__":
    create_tearsheet()
