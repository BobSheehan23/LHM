"""
Quick script to integrate MacroMicro charts into the chartbook
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
import os

# Lighthouse Macro Brand Colors
COLORS = {
    'primary': '#003366',
    'secondary': '#0066CC',
    'accent': '#FF9900',
}

def add_chart_number(ax, chart_number):
    """Add chart number badge"""
    from matplotlib.patches import Circle
    circle = Circle((0.02, 0.98), 0.015, transform=ax.transAxes,
                   facecolor=COLORS['secondary'], edgecolor='none', zorder=100)
    ax.add_patch(circle)
    ax.text(0.02, 0.98, str(chart_number),
            ha='center', va='center',
            fontsize=10, fontweight='bold', color='white',
            transform=ax.transAxes, zorder=101)


def create_image_chart(image_path, chart_num, title):
    """Create chart from PNG image"""
    fig, ax = plt.subplots(figsize=(11, 8.5))
    ax.axis('off')

    if os.path.exists(image_path):
        img = mpimg.imread(image_path)
        ax.imshow(img)
        add_chart_number(ax, chart_num)
    else:
        ax.text(0.5, 0.5, f'Image not found:\n{os.path.basename(image_path)}',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=14, color='red')

    plt.tight_layout()
    return fig


# MacroMicro chart mappings
MACROMICRO_CHARTS = {
    18: ('~/mm-chart-960x540.png', 'US Redbook Same-Store Retail Sales'),
    19: ('~/mm-chart-960x540 (1).png', 'World AI Infrastructure Companies Inventory'),
    20: ('~/mm-chart-960x540 (2).png', 'US Magnificent 7 CapEx vs Compute Efficiency'),
    21: ('~/mm-chart-960x540 (3).png', 'World AI Software Companies RPO'),
    22: ('~/mm-chart-2025-11-21_Global Semi Equip Billings vs. Taiwan Exports -960x540.png',
         'Global Semi Equipment Billings vs Taiwan Exports'),
    23: ('~/mm-chart-2025-11-21_US - Contribution of IT Investment to Change in Real GDP-960x540.png',
         'US IT Investment Contribution to GDP'),
    24: ('~/mm-chart-2025-11-21_US - Share of Companies Currently or Planning to Use AI-960x540.png',
         'US AI Adoption by Companies'),
    25: ('~/mm-chart-2025-11-21_World - Number of AI-Related Patents Granted (% of World Total)-960x540.png',
         'World AI Patents by Country'),
    26: ('~/mm-chart-2025-11-21_Bitcoin - Average Mining Costs-960x540.png',
         'Bitcoin Mining Costs'),
    27: ('~/mm-chart-2025-11-21_World - Net AI Talent Migration per 10,000 LinkedIn Members-975x635.png',
         'World AI Talent Migration'),
}


def main():
    """Generate chartbook section with MacroMicro charts"""
    output_file = 'MacroMicro_Charts_Section.pdf'

    print(f"\nGenerating MacroMicro charts section...")
    print(f"Output: {output_file}\n")

    with PdfPages(output_file) as pdf:
        for chart_num, (path, title) in sorted(MACROMICRO_CHARTS.items()):
            expanded_path = os.path.expanduser(path)
            print(f"Chart {chart_num}: {title}")
            fig = create_image_chart(expanded_path, chart_num, title)
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)

    print(f"\n✓ Generated {output_file}")
    print(f"Total charts: {len(MACROMICRO_CHARTS)}")


if __name__ == "__main__":
    main()
