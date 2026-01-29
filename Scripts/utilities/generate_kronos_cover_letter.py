#!/usr/bin/env python3
"""Generate cover letter for Kronos Research Discretionary Trader role."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY

DARK = HexColor('#1a1a1a')
GRAY = HexColor('#444444')

def create_cover_letter():
    doc = SimpleDocTemplate(
        "/Users/bob/Bob_Sheehan_Kronos_Cover_Letter.pdf",
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    styles = {
        'header': ParagraphStyle(
            'header',
            fontName='Helvetica-Bold',
            fontSize=12,
            textColor=DARK,
            spaceAfter=2
        ),
        'contact': ParagraphStyle(
            'contact',
            fontName='Helvetica',
            fontSize=10,
            textColor=GRAY,
            spaceAfter=4
        ),
        'date': ParagraphStyle(
            'date',
            fontName='Helvetica',
            fontSize=10,
            textColor=DARK,
            spaceBefore=20,
            spaceAfter=20
        ),
        'body': ParagraphStyle(
            'body',
            fontName='Helvetica',
            fontSize=10,
            textColor=DARK,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=14
        ),
        'closing': ParagraphStyle(
            'closing',
            fontName='Helvetica',
            fontSize=10,
            textColor=DARK,
            spaceBefore=12,
            spaceAfter=4
        )
    }

    story = []

    # Header
    story.append(Paragraph("Bob Sheehan, CFA, CMT", styles['header']))
    story.append(Paragraph("bob@lighthousemacro.com | 240-672-7418", styles['contact']))
    story.append(Paragraph("linkedin.com/in/bob-sheehan-cfa-cmt | LighthouseMacro.com", styles['contact']))

    story.append(Paragraph("January 20, 2026", styles['date']))

    story.append(Paragraph("Kronos Research<br/>Hiring Team", styles['body']))

    story.append(Spacer(1, 12))

    # Body
    story.append(Paragraph(
        "I am writing to express my interest in the Experienced Discretionary Trader position at Kronos Research. "
        "With over a decade of experience spanning institutional portfolio management, macro research, and active crypto "
        "trading, I am drawn to the opportunity to contribute to a newly formed discretionary effort within a successful "
        "prop trading firm.",
        styles['body']
    ))

    story.append(Paragraph(
        "My background aligns directly with what you are seeking. At Bank of America Private Bank, I managed multi-asset "
        "portfolios ($4.5B AUM) and co-managed the Strategic Growth Strategy ($1B AUM), a proprietary large cap equity "
        "strategy that outperformed the S&P 500 by 719 bps annualized (21.7% vs 14.5%) with a 2.35 Sortino ratio, 103% "
        "upside capture, and 76% downside capture through a systematic macro and technical approach. This experience "
        "taught me how to synthesize cross-asset signals, size positions with conviction, and manage risk across market regimes.",
        styles['body']
    ))

    story.append(Paragraph(
        "Since founding Lighthouse Macro, I have built institutional-grade research infrastructure that translates economic "
        "data into actionable trading signals. My framework synthesizes across three engines: Macro Dynamics (growth, inflation, "
        "labor, credit), Monetary Mechanics (Fed plumbing, reserves, repo stress, dealer constraints), and Market Technicals "
        "(structure and security-specific signals). I recently launched a public crypto portfolio on Botsfolio as a Pro "
        "Portfolio Creator, building a transparent, trackable record applying this framework to digital assets. The approach "
        "combines on-chain fundamentals, microstructure analysis (funding rates, liquidation asymmetry, exchange flows), and "
        "price signals to drive coin selection and timing.",
        styles['body']
    ))

    story.append(Paragraph(
        "What excites me about Kronos is the chance to apply discretionary judgment within a quantitative framework, "
        "collaborating with a research team to optimize strategies. My CFA and CMT credentials, combined with a Data Science "
        "diploma and hands-on Python development, position me to bridge fundamental analysis with systematic execution. "
        "I thrive in fast-paced environments and am motivated by the intellectual challenge of navigating volatile markets. "
        "Cash is an active allocation in my framework. I deploy when the setup meets my criteria, not before.",
        styles['body']
    ))

    story.append(Paragraph(
        "I would welcome the opportunity to discuss how my experience in discretionary trading, macro research, and crypto "
        "markets can contribute to Kronos Research's discretionary trading department.",
        styles['body']
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Sincerely,", styles['closing']))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Bob Sheehan, CFA, CMT", styles['header']))

    doc.build(story)
    print("Cover letter saved to: /Users/bob/Bob_Sheehan_Kronos_Cover_Letter.pdf")

if __name__ == "__main__":
    create_cover_letter()
