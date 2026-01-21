"""
Lighthouse Macro Chartbook - Paywall Announcement Deck Generator
Generates a professional slide deck showcasing the chartbook's value proposition
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Wedge
import numpy as np
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.gridspec as gridspec

# Lighthouse Macro Brand Colors
COLORS = {
    'primary': '#003366',      # Deep blue
    'secondary': '#0066CC',    # Bright blue
    'accent': '#FF9900',       # Orange
    'positive': '#00A86B',     # Green
    'negative': '#CC0000',     # Red
    'neutral': '#808080',      # Gray
    'background': '#FFFFFF',   # White
    'light_blue': '#E3F2FD',
    'light_orange': '#FFF3E0',
    'light_green': '#E8F5E9',
}

# Global styling
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 11,
    'axes.titlesize': 16,
    'axes.labelsize': 12,
    'figure.figsize': (11, 8.5),
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})


def create_cover_slide():
    """Slide 1: Cover with title and tagline"""
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_subplot(111)
    ax.axis('off')

    # Background gradient effect using rectangles
    for i, alpha in enumerate(np.linspace(0.1, 0.01, 10)):
        rect = Rectangle((0, 0.5 - i*0.05), 1, 0.05,
                         transform=ax.transAxes,
                         facecolor=COLORS['primary'],
                         alpha=alpha,
                         edgecolor='none')
        ax.add_patch(rect)

    # Main title
    ax.text(0.5, 0.65, 'LIGHTHOUSE MACRO',
            ha='center', va='center',
            fontsize=48, fontweight='bold',
            color=COLORS['primary'],
            transform=ax.transAxes)

    # Subtitle
    ax.text(0.5, 0.55, 'FRIDAY CHARTBOOK',
            ha='center', va='center',
            fontsize=36, fontweight='bold',
            color=COLORS['secondary'],
            transform=ax.transAxes)

    # Separator line
    ax.plot([0.2, 0.8], [0.48, 0.48],
            color=COLORS['accent'], linewidth=3,
            transform=ax.transAxes)

    # Tagline
    ax.text(0.5, 0.38, 'Institutional-Grade Macro Intelligence',
            ha='center', va='center',
            fontsize=20, style='italic',
            color=COLORS['neutral'],
            transform=ax.transAxes)

    # Key value props (3 bullet points)
    bullets = [
        '50 Advanced Charts • Three Pillars Framework',
        'Traditional Markets + Crypto Dynamics',
        'Next-Generation Visualization & Analytics'
    ]

    for i, bullet in enumerate(bullets):
        ax.text(0.5, 0.28 - i*0.06, bullet,
                ha='center', va='center',
                fontsize=14,
                color=COLORS['primary'],
                transform=ax.transAxes)

    # Footer
    ax.text(0.5, 0.05, f'Premium Research Product • {datetime.now().year}',
            ha='center', va='center',
            fontsize=11, color=COLORS['neutral'],
            transform=ax.transAxes)

    plt.tight_layout()
    return fig


def create_problem_slide():
    """Slide 2: The Problem - Current state of macro research"""
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_subplot(111)
    ax.axis('off')

    # Title
    ax.text(0.5, 0.92, 'THE MACRO RESEARCH GAP',
            ha='center', va='top',
            fontsize=32, fontweight='bold',
            color=COLORS['primary'],
            transform=ax.transAxes)

    # Subtitle
    ax.text(0.5, 0.85, 'Current Market Intelligence Falls Short',
            ha='center', va='top',
            fontsize=16, style='italic',
            color=COLORS['neutral'],
            transform=ax.transAxes)

    # Four quadrants showing problems
    problems = [
        {
            'title': 'STATIC CHARTS',
            'desc': 'Single-axis snapshots\nmiss transmission\nmechanisms',
            'pos': (0.25, 0.55),
            'color': COLORS['negative']
        },
        {
            'title': 'SILOED ANALYSIS',
            'desc': 'Traditional vs. crypto\nmarkets analyzed\nin isolation',
            'pos': (0.75, 0.55),
            'color': COLORS['negative']
        },
        {
            'title': 'SURFACE LEVEL',
            'desc': 'Headline numbers\nwithout structural\ndynamics',
            'pos': (0.25, 0.25),
            'color': COLORS['negative']
        },
        {
            'title': 'NO FRAMEWORK',
            'desc': 'Disconnected charts\nlacking cohesive\ninvestment narrative',
            'pos': (0.75, 0.25),
            'color': COLORS['negative']
        }
    ]

    for prob in problems:
        # Box
        box = FancyBboxPatch(
            (prob['pos'][0] - 0.18, prob['pos'][1] - 0.12),
            0.36, 0.24,
            boxstyle="round,pad=0.01",
            edgecolor=prob['color'],
            facecolor=COLORS['background'],
            linewidth=3,
            transform=ax.transAxes
        )
        ax.add_patch(box)

        # Title
        ax.text(prob['pos'][0], prob['pos'][1] + 0.08,
                prob['title'],
                ha='center', va='center',
                fontsize=14, fontweight='bold',
                color=prob['color'],
                transform=ax.transAxes)

        # Description
        ax.text(prob['pos'][0], prob['pos'][1] - 0.02,
                prob['desc'],
                ha='center', va='center',
                fontsize=11,
                color=COLORS['neutral'],
                transform=ax.transAxes)

    plt.tight_layout()
    return fig


def create_three_pillars_slide():
    """Slide 3: Three Pillars Framework Visualization"""
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_subplot(111)
    ax.axis('off')

    # Title
    ax.text(0.5, 0.95, 'THE THREE PILLARS FRAMEWORK',
            ha='center', va='top',
            fontsize=32, fontweight='bold',
            color=COLORS['primary'],
            transform=ax.transAxes)

    # Three pillars as columns
    pillars = [
        {
            'name': 'MACRO\nDYNAMICS',
            'icon_y': 0.70,
            'color': COLORS['secondary'],
            'x': 0.2,
            'items': [
                'Economic Cycles',
                'Inflation Drivers',
                'Labor Flows',
                'Growth Indicators'
            ]
        },
        {
            'name': 'MONETARY\nMECHANICS',
            'icon_y': 0.70,
            'color': COLORS['accent'],
            'x': 0.5,
            'items': [
                'Fed Balance Sheet',
                'RRP Facility',
                'Liquidity Transmission',
                'Money Market Plumbing'
            ]
        },
        {
            'name': 'MARKET\nTECHNICALS',
            'icon_y': 0.70,
            'color': COLORS['positive'],
            'x': 0.8,
            'items': [
                'Cross-Asset Flows',
                'Credit Spreads',
                'Crypto Linkages',
                'Sentiment Indicators'
            ]
        }
    ]

    for pillar in pillars:
        # Pillar column (visual pillar shape)
        pillar_top = Wedge((pillar['x'], pillar['icon_y'] + 0.05), 0.08, 0, 180,
                           facecolor=pillar['color'], edgecolor='none',
                           transform=ax.transAxes, alpha=0.9)
        ax.add_patch(pillar_top)

        pillar_body = Rectangle((pillar['x'] - 0.06, 0.15),
                                0.12, pillar['icon_y'] - 0.10,
                                facecolor=pillar['color'],
                                edgecolor='none',
                                transform=ax.transAxes,
                                alpha=0.7)
        ax.add_patch(pillar_body)

        # Pillar name
        ax.text(pillar['x'], 0.82, pillar['name'],
                ha='center', va='center',
                fontsize=14, fontweight='bold',
                color=COLORS['primary'],
                transform=ax.transAxes)

        # Items
        for i, item in enumerate(pillar['items']):
            y_pos = 0.48 - i * 0.08
            # Bullet point
            ax.plot(pillar['x'] - 0.08, y_pos, 'o',
                   color=pillar['color'], markersize=6,
                   transform=ax.transAxes)
            # Text
            ax.text(pillar['x'] - 0.06, y_pos, item,
                   ha='left', va='center',
                   fontsize=10,
                   color=COLORS['primary'],
                   transform=ax.transAxes)

    # Base platform
    base = Rectangle((0.05, 0.08), 0.9, 0.04,
                     facecolor=COLORS['primary'],
                     edgecolor='none',
                     transform=ax.transAxes,
                     alpha=0.9)
    ax.add_patch(base)

    ax.text(0.5, 0.10, 'Institutional-Grade Analytics Foundation',
            ha='center', va='center',
            fontsize=12, fontweight='bold',
            color=COLORS['background'],
            transform=ax.transAxes)

    plt.tight_layout()
    return fig


def create_architecture_slide():
    """Slide 4: 50-Chart Architecture Diagram"""
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_subplot(111)
    ax.axis('off')

    # Title
    ax.text(0.5, 0.95, '50-CHART ARCHITECTURE',
            ha='center', va='top',
            fontsize=32, fontweight='bold',
            color=COLORS['primary'],
            transform=ax.transAxes)

    ax.text(0.5, 0.89, 'Three-Layer Intelligence System',
            ha='center', va='top',
            fontsize=16, style='italic',
            color=COLORS['neutral'],
            transform=ax.transAxes)

    # Three layers as stacked blocks
    layers = [
        {
            'name': 'LAYER 1: MACRO REGIME DASHBOARD',
            'charts': '10 Charts',
            'desc': 'Economic cycle positioning • Leading indicators\nRegime classification • Cross-asset correlations',
            'y_start': 0.70,
            'height': 0.12,
            'color': COLORS['secondary']
        },
        {
            'name': 'LAYER 2: TRANSMISSION MECHANISMS',
            'charts': '25 Charts',
            'desc': 'RRP/Liquidity (5) • Labor Flows (5) • Credit Spreads (5)\nTreasury Plumbing (5) • Crypto-Traditional Linkages (5)',
            'y_start': 0.48,
            'height': 0.18,
            'color': COLORS['accent']
        },
        {
            'name': 'LAYER 3: EARLY WARNING SIGNALS',
            'charts': '15 Charts',
            'desc': 'Proprietary stress indices • Z-score deviations\nScenario probabilities • Factor attribution',
            'y_start': 0.28,
            'height': 0.16,
            'color': COLORS['positive']
        }
    ]

    for layer in layers:
        # Main box
        box = FancyBboxPatch(
            (0.1, layer['y_start']),
            0.8, layer['height'],
            boxstyle="round,pad=0.01",
            edgecolor=layer['color'],
            facecolor=layer['color'],
            linewidth=2,
            alpha=0.2,
            transform=ax.transAxes
        )
        ax.add_patch(box)

        # Border
        border = FancyBboxPatch(
            (0.1, layer['y_start']),
            0.8, layer['height'],
            boxstyle="round,pad=0.01",
            edgecolor=layer['color'],
            facecolor='none',
            linewidth=3,
            transform=ax.transAxes
        )
        ax.add_patch(border)

        # Layer name
        ax.text(0.12, layer['y_start'] + layer['height'] - 0.02,
                layer['name'],
                ha='left', va='top',
                fontsize=13, fontweight='bold',
                color=layer['color'],
                transform=ax.transAxes)

        # Chart count badge
        chart_badge = FancyBboxPatch(
            (0.82, layer['y_start'] + layer['height'] - 0.04),
            0.06, 0.03,
            boxstyle="round,pad=0.003",
            facecolor=layer['color'],
            edgecolor='none',
            transform=ax.transAxes
        )
        ax.add_patch(chart_badge)

        ax.text(0.85, layer['y_start'] + layer['height'] - 0.025,
                layer['charts'],
                ha='center', va='center',
                fontsize=9, fontweight='bold',
                color=COLORS['background'],
                transform=ax.transAxes)

        # Description
        ax.text(0.5, layer['y_start'] + layer['height']/2,
                layer['desc'],
                ha='center', va='center',
                fontsize=10,
                color=COLORS['primary'],
                transform=ax.transAxes)

    # Bottom summary
    ax.text(0.5, 0.15, '= Complete Macro Intelligence Ecosystem =',
            ha='center', va='center',
            fontsize=18, fontweight='bold',
            color=COLORS['primary'],
            transform=ax.transAxes)

    ax.text(0.5, 0.08, 'From regime identification to actionable early warnings',
            ha='center', va='center',
            fontsize=12, style='italic',
            color=COLORS['neutral'],
            transform=ax.transAxes)

    plt.tight_layout()
    return fig


def create_example_rrp_chart():
    """Slide 5: Example Chart - RRP/Liquidity Dual-Axis"""
    fig = plt.figure(figsize=(11, 8.5))

    # Create mock data for demonstration
    np.random.seed(42)
    dates = np.arange(100)

    # RRP: declining trend
    rrp = 2.5 - 0.02 * dates + np.random.normal(0, 0.1, 100)
    rrp = np.maximum(rrp, 0.3)  # Floor at 0.3

    # VIX: inverse relationship with spikes
    vix = 15 + 5 * (1 / (rrp + 0.5)) + np.random.normal(0, 2, 100)

    # Main chart area
    ax1 = plt.subplot(111)

    # Primary axis: RRP
    color1 = COLORS['accent']
    ax1.fill_between(dates, 0, rrp, alpha=0.6, color=color1, label='RRP Usage')
    ax1.plot(dates, rrp, color=color1, linewidth=2.5)
    ax1.set_xlabel('Trading Days', fontsize=12, fontweight='bold')
    ax1.set_ylabel('RRP Balance ($ Trillions)', fontsize=12, fontweight='bold', color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_ylim(0, 3)

    # Secondary axis: VIX
    ax2 = ax1.twinx()
    color2 = COLORS['secondary']
    ax2.plot(dates, vix, color=color2, linewidth=2.5, linestyle='--', label='VIX Index')
    ax2.set_ylabel('VIX Index', fontsize=12, fontweight='bold', color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.axhline(y=20, color=COLORS['negative'], linestyle=':', linewidth=1, alpha=0.5)

    # Stress threshold shading
    stress_periods = rrp < 0.5
    for i in range(len(dates)-1):
        if stress_periods[i]:
            ax1.axvspan(dates[i], dates[i+1], alpha=0.15, color=COLORS['negative'])

    # Title with subtitle
    plt.suptitle('EXAMPLE: RRP Depletion vs Market Volatility',
                fontsize=18, fontweight='bold', color=COLORS['primary'], y=0.98)
    ax1.text(0.5, 1.08, 'Dual-Axis Transmission Mechanism Analysis',
            ha='center', va='top', fontsize=12, style='italic',
            color=COLORS['neutral'], transform=ax1.transAxes)

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2,
              loc='upper right', frameon=True, shadow=True, fontsize=10)

    # Annotation
    crisis_point = 75
    ax1.annotate('Stress Threshold\n(RRP < $500B)',
                xy=(crisis_point, rrp[crisis_point]),
                xytext=(crisis_point - 20, 2.5),
                fontsize=10, color=COLORS['negative'],
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                arrowprops=dict(arrowstyle='->', color=COLORS['negative'], lw=2))

    # Source
    ax1.text(0.02, -0.12, 'Source: Federal Reserve, CBOE | Lighthouse Macro',
            ha='left', va='top', fontsize=9, color=COLORS['neutral'],
            transform=ax1.transAxes)

    plt.tight_layout()
    return fig


def create_labor_spider_chart():
    """Slide 6: Example Chart - Labor Market Spider/Radar"""
    fig = plt.figure(figsize=(11, 8.5))

    categories = ['Hires\nRate', 'Quits\nRate', 'Openings\nRate',
                  'Layoffs\nRate\n(Inverted)', 'Wage\nGrowth']
    N = len(categories)

    # Mock data (normalized 0-100 scale)
    current = [65, 45, 50, 70, 55]
    year_ago = [75, 65, 80, 85, 70]
    pre_pandemic = [70, 60, 65, 80, 60]

    # Compute angles
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    # Close the plots
    current += current[:1]
    year_ago += year_ago[:1]
    pre_pandemic += pre_pandemic[:1]

    # Create polar plot
    ax = plt.subplot(111, polar=True)

    # Plot each period
    ax.plot(angles, current, 'o-', linewidth=3,
            label='Current (Dec 2024)', color=COLORS['secondary'])
    ax.fill(angles, current, alpha=0.25, color=COLORS['secondary'])

    ax.plot(angles, year_ago, 'o--', linewidth=2.5,
            label='1 Year Ago', color=COLORS['accent'])

    ax.plot(angles, pre_pandemic, 'o:', linewidth=2,
            label='Pre-Pandemic Avg', color=COLORS['neutral'])

    # Customize
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=11)
    ax.set_ylim(0, 100)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(['25', '50', '75', '100'], size=9)
    ax.grid(True, linestyle='--', alpha=0.7)

    # Title
    plt.suptitle('EXAMPLE: Labor Market Health - Multi-Dimensional View',
                fontsize=18, fontweight='bold', color=COLORS['primary'], y=0.98)
    ax.text(0.5, 1.15, 'JOLTS Flow Indicators Spider Chart',
            ha='center', va='top', fontsize=12, style='italic',
            color=COLORS['neutral'], transform=ax.transAxes)

    # Legend
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1),
             frameon=True, shadow=True, fontsize=10)

    # Insight box
    insight_text = "INSIGHT: Significant deterioration across\nall dimensions vs. year ago, especially\nquits rate (worker confidence signal)"
    ax.text(0.5, -0.22, insight_text,
            ha='center', va='top', fontsize=10,
            color=COLORS['primary'],
            bbox=dict(boxstyle='round', facecolor=COLORS['light_orange'], alpha=0.8),
            transform=ax.transAxes)

    plt.tight_layout()
    return fig


def create_technical_capabilities_slide():
    """Slide 7: Technical Excellence Dashboard"""
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_subplot(111)
    ax.axis('off')

    # Title
    ax.text(0.5, 0.95, 'TECHNICAL EXCELLENCE',
            ha='center', va='top',
            fontsize=32, fontweight='bold',
            color=COLORS['primary'],
            transform=ax.transAxes)

    ax.text(0.5, 0.88, 'Institutional-Grade Production System',
            ha='center', va='top',
            fontsize=16, style='italic',
            color=COLORS['neutral'],
            transform=ax.transAxes)

    # Performance metrics in grid
    metrics = [
        {
            'value': '<5 min',
            'label': 'Generation Time',
            'sublabel': '50 charts, parallel processing',
            'pos': (0.25, 0.68),
            'color': COLORS['positive']
        },
        {
            'value': '>90%',
            'label': 'Cache Hit Rate',
            'sublabel': 'Fast daily updates',
            'pos': (0.75, 0.68),
            'color': COLORS['positive']
        },
        {
            'value': '100%',
            'label': 'Brand Consistency',
            'sublabel': 'Automated style enforcement',
            'pos': (0.25, 0.42),
            'color': COLORS['secondary']
        },
        {
            'value': '25+',
            'label': 'Dual-Axis Charts',
            'sublabel': 'Causal relationships',
            'pos': (0.75, 0.42),
            'color': COLORS['secondary']
        }
    ]

    for metric in metrics:
        # Circle background
        circle = Circle(metric['pos'], 0.08,
                       facecolor=metric['color'],
                       edgecolor='none',
                       alpha=0.2,
                       transform=ax.transAxes)
        ax.add_patch(circle)

        # Value
        ax.text(metric['pos'][0], metric['pos'][1] + 0.02,
                metric['value'],
                ha='center', va='center',
                fontsize=24, fontweight='bold',
                color=metric['color'],
                transform=ax.transAxes)

        # Label
        ax.text(metric['pos'][0], metric['pos'][1] - 0.10,
                metric['label'],
                ha='center', va='center',
                fontsize=13, fontweight='bold',
                color=COLORS['primary'],
                transform=ax.transAxes)

        # Sublabel
        ax.text(metric['pos'][0], metric['pos'][1] - 0.14,
                metric['sublabel'],
                ha='center', va='center',
                fontsize=10,
                color=COLORS['neutral'],
                transform=ax.transAxes)

    # Technology stack
    ax.text(0.5, 0.22, 'TECHNOLOGY STACK',
            ha='center', va='top',
            fontsize=14, fontweight='bold',
            color=COLORS['primary'],
            transform=ax.transAxes)

    tech_items = [
        'Python 3.11+ • Matplotlib • Plotly',
        'FRED API • 2-Tier Caching • Parallel Execution',
        'PDF Generation • Version Control • Automated Testing'
    ]

    for i, item in enumerate(tech_items):
        ax.text(0.5, 0.16 - i*0.04, item,
                ha='center', va='center',
                fontsize=11,
                color=COLORS['neutral'],
                transform=ax.transAxes)

    plt.tight_layout()
    return fig


def create_institutional_quality_slide():
    """Slide 8: Institutional Quality Comparison"""
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_subplot(111)
    ax.axis('off')

    # Title
    ax.text(0.5, 0.95, 'INSTITUTIONAL QUALITY STANDARDS',
            ha='center', va='top',
            fontsize=32, fontweight='bold',
            color=COLORS['primary'],
            transform=ax.transAxes)

    ax.text(0.5, 0.88, 'Matching Goldman Sachs, JPMorgan, Bridgewater Visual Excellence',
            ha='center', va='top',
            fontsize=14, style='italic',
            color=COLORS['neutral'],
            transform=ax.transAxes)

    # Comparison bars
    categories = [
        'Visual Design',
        'Data Depth',
        'Framework Integration',
        'Update Frequency',
        'Cross-Asset Coverage'
    ]

    lighthouse_scores = [95, 90, 98, 100, 95]  # Lighthouse Macro
    industry_avg_scores = [70, 65, 60, 70, 55]  # Industry average

    y_positions = np.arange(len(categories))
    bar_height = 0.35

    # Create horizontal bars
    bars1 = ax.barh([y - bar_height/2 for y in y_positions], lighthouse_scores,
                    bar_height, label='Lighthouse Macro',
                    color=COLORS['secondary'], alpha=0.8)

    bars2 = ax.barh([y + bar_height/2 for y in y_positions], industry_avg_scores,
                    bar_height, label='Industry Average',
                    color=COLORS['neutral'], alpha=0.5)

    # Customize
    ax.set_yticks(y_positions)
    ax.set_yticklabels(categories, fontsize=12)
    ax.set_xlabel('Quality Score', fontsize=12, fontweight='bold')
    ax.set_xlim(0, 105)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.legend(loc='lower right', fontsize=11, frameon=True, shadow=True)

    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 2, bar.get_y() + bar.get_height()/2,
                   f'{int(width)}',
                   ha='left', va='center', fontsize=10, fontweight='bold')

    # Move to proper position
    ax.set_position([0.25, 0.35, 0.65, 0.45])

    # Bottom differentiators
    ax.text(0.5, 0.18, 'UNIQUE DIFFERENTIATORS',
            ha='center', va='top',
            fontsize=14, fontweight='bold',
            color=COLORS['primary'],
            transform=fig.transFigure)

    differentiators = [
        '✓ Only product systematically tracking crypto-traditional linkages',
        '✓ Proprietary liquidity stress indices',
        '✓ Three Pillars framework for clear investment narrative'
    ]

    for i, diff in enumerate(differentiators):
        ax.text(0.5, 0.13 - i*0.04, diff,
                ha='center', va='center',
                fontsize=11,
                color=COLORS['positive'],
                transform=fig.transFigure)

    return fig


def create_value_proposition_slide():
    """Slide 9: What You Get - Value Summary"""
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_subplot(111)
    ax.axis('off')

    # Title
    ax.text(0.5, 0.95, 'WHAT YOU GET',
            ha='center', va='top',
            fontsize=36, fontweight='bold',
            color=COLORS['primary'],
            transform=ax.transAxes)

    ax.text(0.5, 0.88, 'Weekly Institutional-Grade Intelligence Package',
            ha='center', va='top',
            fontsize=16, style='italic',
            color=COLORS['neutral'],
            transform=ax.transAxes)

    # Main deliverables in boxes
    deliverables = [
        {
            'title': '📊 50 Advanced Charts',
            'items': [
                '• 25+ dual-axis transmission charts',
                '• Proprietary composite indices',
                '• Regime-aware visualizations',
                '• Statistical insights on every chart'
            ],
            'y': 0.72
        },
        {
            'title': '🎯 Three Pillars Framework',
            'items': [
                '• Macro Dynamics: Cycles, inflation, labor',
                '• Monetary Mechanics: Fed, RRP, liquidity',
                '• Market Technicals: Flows, crypto, credit'
            ],
            'y': 0.52
        },
        {
            'title': '⚡ Every Friday Morning',
            'items': [
                '• PDF delivered before market open',
                '• Fresh data through Thursday close',
                '• Publication-quality visualizations',
                '• Clear, actionable insights'
            ],
            'y': 0.32
        }
    ]

    for deliv in deliverables:
        # Box
        box = FancyBboxPatch(
            (0.1, deliv['y'] - 0.15),
            0.8, 0.16,
            boxstyle="round,pad=0.01",
            edgecolor=COLORS['secondary'],
            facecolor=COLORS['light_blue'],
            linewidth=2,
            alpha=0.3,
            transform=ax.transAxes
        )
        ax.add_patch(box)

        # Title
        ax.text(0.12, deliv['y'],
                deliv['title'],
                ha='left', va='top',
                fontsize=15, fontweight='bold',
                color=COLORS['primary'],
                transform=ax.transAxes)

        # Items
        for i, item in enumerate(deliv['items']):
            ax.text(0.13, deliv['y'] - 0.04 - i*0.03,
                    item,
                    ha='left', va='top',
                    fontsize=11,
                    color=COLORS['primary'],
                    transform=ax.transAxes)

    # Bottom guarantee
    ax.text(0.5, 0.10, 'PREMIUM RESEARCH • INSTITUTIONAL QUALITY • ACTIONABLE INSIGHTS',
            ha='center', va='center',
            fontsize=12, fontweight='bold',
            color=COLORS['accent'],
            transform=ax.transAxes)

    plt.tight_layout()
    return fig


def create_cta_slide():
    """Slide 10: Call to Action / Pricing"""
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_subplot(111)
    ax.axis('off')

    # Background accent
    for i, alpha in enumerate(np.linspace(0.05, 0.01, 8)):
        rect = Rectangle((0, 0.3 - i*0.05), 1, 0.05,
                         transform=ax.transAxes,
                         facecolor=COLORS['accent'],
                         alpha=alpha,
                         edgecolor='none')
        ax.add_patch(rect)

    # Main CTA
    ax.text(0.5, 0.75, 'SUBSCRIBE TODAY',
            ha='center', va='center',
            fontsize=42, fontweight='bold',
            color=COLORS['primary'],
            transform=ax.transAxes)

    # Pricing box
    price_box = FancyBboxPatch(
        (0.3, 0.48),
        0.4, 0.18,
        boxstyle="round,pad=0.02",
        edgecolor=COLORS['secondary'],
        facecolor=COLORS['background'],
        linewidth=4,
        transform=ax.transAxes
    )
    ax.add_patch(price_box)

    ax.text(0.5, 0.63, 'PREMIUM TIER',
            ha='center', va='top',
            fontsize=14, fontweight='bold',
            color=COLORS['neutral'],
            transform=ax.transAxes)

    ax.text(0.5, 0.57, '$XX/month',
            ha='center', va='center',
            fontsize=32, fontweight='bold',
            color=COLORS['secondary'],
            transform=ax.transAxes)

    ax.text(0.5, 0.51, 'or $XXX/year (save 20%)',
            ha='center', va='center',
            fontsize=13,
            color=COLORS['neutral'],
            transform=ax.transAxes)

    # Benefits bullets
    benefits = [
        '✓ 50 charts every Friday',
        '✓ Institutional-grade analytics',
        '✓ Cancel anytime'
    ]

    for i, benefit in enumerate(benefits):
        ax.text(0.5, 0.40 - i*0.05, benefit,
                ha='center', va='center',
                fontsize=13,
                color=COLORS['primary'],
                transform=ax.transAxes)

    # CTA button
    button = FancyBboxPatch(
        (0.35, 0.18),
        0.3, 0.06,
        boxstyle="round,pad=0.01",
        edgecolor='none',
        facecolor=COLORS['accent'],
        transform=ax.transAxes
    )
    ax.add_patch(button)

    ax.text(0.5, 0.21, 'JOIN NOW →',
            ha='center', va='center',
            fontsize=16, fontweight='bold',
            color=COLORS['background'],
            transform=ax.transAxes)

    # Footer
    ax.text(0.5, 0.08, 'lighthouse-macro.substack.com',
            ha='center', va='center',
            fontsize=14, style='italic',
            color=COLORS['neutral'],
            transform=ax.transAxes)

    ax.text(0.5, 0.03, 'Questions? Contact: [email]',
            ha='center', va='center',
            fontsize=11,
            color=COLORS['neutral'],
            transform=ax.transAxes)

    plt.tight_layout()
    return fig


def generate_full_deck(output_filename='Lighthouse_Macro_Paywall_Deck.pdf'):
    """Generate complete slide deck"""
    print("Generating Lighthouse Macro Paywall Deck...")
    print("=" * 60)

    slides = [
        ("Cover", create_cover_slide),
        ("Problem", create_problem_slide),
        ("Three Pillars", create_three_pillars_slide),
        ("Architecture", create_architecture_slide),
        ("Example: RRP Chart", create_example_rrp_chart),
        ("Example: Labor Spider", create_labor_spider_chart),
        ("Technical Excellence", create_technical_capabilities_slide),
        ("Institutional Quality", create_institutional_quality_slide),
        ("Value Proposition", create_value_proposition_slide),
        ("Call to Action", create_cta_slide),
    ]

    with PdfPages(output_filename) as pdf:
        for i, (name, func) in enumerate(slides, 1):
            print(f"Generating slide {i}/{len(slides)}: {name}")
            fig = func()
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)

    print("=" * 60)
    print(f"✓ Deck generated successfully: {output_filename}")
    print(f"✓ Total slides: {len(slides)}")

    return output_filename


if __name__ == "__main__":
    output_file = generate_full_deck()
    print(f"\nReady for Substack announcement!")
    print(f"File location: {output_file}")
