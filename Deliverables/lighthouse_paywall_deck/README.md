# Lighthouse Macro Chartbook - Paywall Announcement Deck

## Overview
Professional 10-slide PDF deck designed to announce the premium paywall for the Lighthouse Macro Friday Chartbook on Substack.

## Deck Contents

### Slide 1: Cover
- Lighthouse Macro branding
- Friday Chartbook title
- Key value propositions: 50 charts, Three Pillars framework, cross-asset coverage

### Slide 2: The Problem
- Identifies gaps in current macro research
- Four pain points: static charts, siloed analysis, surface-level insights, no framework

### Slide 3: Three Pillars Framework
- Visual representation of the analytical framework
- Pillar 1: Macro Dynamics (cycles, inflation, labor)
- Pillar 2: Monetary Mechanics (Fed, RRP, liquidity)
- Pillar 3: Market Technicals (flows, credit, crypto)

### Slide 4: 50-Chart Architecture
- Three-layer system visualization
- Layer 1: Regime Dashboard (10 charts)
- Layer 2: Transmission Mechanisms (25 charts)
- Layer 3: Early Warning Signals (15 charts)

### Slide 5: Example Chart - RRP/Liquidity
- Demonstrates dual-axis chart capability
- Shows RRP depletion vs. VIX (market volatility)
- Highlights transmission mechanism analysis

### Slide 6: Example Chart - Labor Market Spider
- Multi-dimensional visualization
- JOLTS flow indicators across 5 dimensions
- Comparison across time periods

### Slide 7: Technical Excellence
- Performance metrics dashboard
- 4 key capabilities: <5min generation, >90% cache hit rate, 100% brand consistency, 25+ dual-axis charts
- Technology stack overview

### Slide 8: Institutional Quality
- Comparison bar chart vs. industry standards
- 5 quality dimensions: visual design, data depth, framework integration, update frequency, cross-asset coverage
- Unique differentiators

### Slide 9: What You Get
- Value proposition summary
- 3 main deliverables: 50 advanced charts, Three Pillars framework, weekly Friday delivery
- Clear benefits for each

### Slide 10: Call to Action
- Subscribe prompt with pricing structure
- Premium tier pricing (to be customized)
- Benefits bullets and CTA button
- Contact information

## Customization Guide

### Updating Pricing
Edit line ~906-910 in `generate_deck.py`:
```python
ax.text(0.5, 0.57, '$XX/month',  # Change price here
        ha='center', va='center',
        fontsize=32, fontweight='bold',
        color=COLORS['secondary'],
        transform=ax.transAxes)
```

### Changing Colors
All colors defined at the top (lines 17-27):
```python
COLORS = {
    'primary': '#003366',      # Deep blue
    'secondary': '#0066CC',    # Bright blue
    'accent': '#FF9900',       # Orange
    # ... etc
}
```

### Adding Your Email/Contact
Edit line ~955 in `generate_deck.py`:
```python
ax.text(0.5, 0.03, 'Questions? Contact: [email]',  # Add your email
```

### Adding Your Substack URL
Edit line ~948:
```python
ax.text(0.5, 0.08, 'lighthouse-macro.substack.com',  # Your Substack URL
```

## Regenerating the Deck

After making any customizations:

```bash
cd /Users/bob/lighthouse_paywall_deck
source venv/bin/activate
python generate_deck.py
```

The new PDF will be generated as `Lighthouse_Macro_Paywall_Deck.pdf`

## File Structure

```
lighthouse_paywall_deck/
├── generate_deck.py              # Main script
├── Lighthouse_Macro_Paywall_Deck.pdf  # Generated deck
├── venv/                         # Python virtual environment
└── README.md                     # This file
```

## Usage for Substack

1. Upload the PDF to your Substack post as an attachment
2. Reference it in your announcement post
3. Consider extracting 1-2 key slides as inline images to preview the content
4. Link to the PDF for full details

## Suggested Substack Post Structure

```markdown
# Introducing: The Lighthouse Macro Friday Chartbook (Premium)

Today I'm excited to announce a new premium offering...

[Brief intro paragraph about the chartbook]

**What You'll Get:**
- 50 institutional-grade charts every Friday morning
- Comprehensive Three Pillars framework
- Advanced dual-axis visualizations
- Crypto-traditional market linkages

[Preview image: Slide 3 or 5]

For full details on the framework, chart examples, and technical capabilities,
see the attached deck.

📎 [Lighthouse_Macro_Paywall_Deck.pdf]

**Subscribe Today**
[Substack subscribe button]

Questions? Reply to this email or contact...
```

## Technical Notes

- Generated with matplotlib 3.10.7 + numpy 2.3.5
- Output: 10-slide PDF, ~90KB file size
- Resolution: 300 DPI (print quality)
- Page size: 11" × 8.5" landscape
- Font warnings about emojis are normal and don't affect quality

## Next Steps

1. Customize pricing and contact info
2. Regenerate deck
3. Review PDF quality
4. Upload to Substack
5. Craft announcement post
6. Launch!
