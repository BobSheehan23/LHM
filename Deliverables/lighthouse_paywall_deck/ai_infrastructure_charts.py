"""
Lighthouse Macro - Section 6: AI Infrastructure (Charts 36-42)
Next-generation chartbook with MacroMicro images + TradingView single names
"""

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from PIL import Image
from lighthouse_style import (
    COLORS,
    create_single_axis_chart,
    enforce_no_gridlines
)


# MacroMicro images directory
MACROMICRO_DIR = Path(__file__).parent / "macromicro_charts"

# TradingView images directory
TRADINGVIEW_IMG_DIR = Path(__file__).parent / "tradingview_screenshots"
TRADINGVIEW_IMG_DIR.mkdir(parents=True, exist_ok=True)


def load_macromicro_image(chart_name):
    """
    Load MacroMicro chart image

    Args:
        chart_name: Name of the chart image file

    Returns:
        PIL Image object or None
    """
    # Try different extensions
    for ext in ['.png', '.jpg', '.jpeg']:
        filepath = MACROMICRO_DIR / f"{chart_name}{ext}"
        if filepath.exists():
            return Image.open(filepath)

    return None


def create_image_chart(chart_number, image_path, title, source='MacroMicro'):
    """
    Create chart from image file with Lighthouse branding

    Args:
        chart_number: Chart number
        image_path: Path to image file
        title: Chart title
        source: Data source

    Returns:
        matplotlib Figure
    """
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_axes([0.05, 0.12, 0.9, 0.76])  # Leave room for branding
    ax.axis('off')

    if image_path.exists():
        img = Image.open(image_path)
        ax.imshow(img)
    else:
        ax.text(0.5, 0.5, f'Image not found:\n{image_path.name}\n\nPlease add to:\n{image_path.parent}',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=12, color=COLORS['neutral'])

    # Add title at top
    fig.text(0.5, 0.94, title,
            ha='center', va='top', fontsize=14, fontweight='bold',
            color=COLORS['ocean_blue'])

    # Chart number badge
    from matplotlib.patches import Circle
    circle = Circle((0.02, 0.98), 0.015, transform=fig.transFigure,
                   facecolor=COLORS['ocean_blue'], edgecolor='none', zorder=100)
    fig.patches.append(circle)
    fig.text(0.02, 0.98, str(chart_number),
            ha='center', va='center', fontsize=10, fontweight='bold',
            color='white', transform=fig.transFigure, zorder=101)

    # LIGHTHOUSE MACRO
    fig.text(0.045, 0.98, 'LIGHTHOUSE MACRO',
            ha='left', va='center', fontsize=9, fontweight='bold',
            color=COLORS['ocean_blue'], transform=fig.transFigure)

    # Source
    fig.text(0.02, 0.02, f'Source: {source}',
            ha='left', va='bottom', fontsize=7, color=COLORS['neutral'], style='italic')

    # Watermark
    fig.text(0.98, 0.02, 'MACRO, ILLUMINATED.',
            ha='right', va='bottom', fontsize=8, fontweight='bold',
            color=COLORS['ocean_blue'], alpha=0.6)

    return fig


# === MacroMicro Charts (36-39) ===

def chart_36_mag7_capex():
    """Chart 36: Mag 7 CapEx Trends (MacroMicro)"""
    image_path = MACROMICRO_DIR / "mag7_capex.png"
    return create_image_chart(
        chart_number=36,
        image_path=image_path,
        title='Magnificent 7 CapEx Trends: AI Infrastructure Spend',
        source='MacroMicro'
    )


def chart_37_ai_software_rpo():
    """Chart 37: AI Software RPO Growth (MacroMicro)"""
    image_path = MACROMICRO_DIR / "ai_software_rpo.png"
    return create_image_chart(
        chart_number=37,
        image_path=image_path,
        title='AI Software RPO Growth: Remaining Performance Obligations',
        source='MacroMicro'
    )


def chart_38_semi_equipment_exports():
    """Chart 38: Global Semi Equipment vs Taiwan Exports (MacroMicro)"""
    image_path = MACROMICRO_DIR / "semi_equipment_exports.png"
    return create_image_chart(
        chart_number=38,
        image_path=image_path,
        title='Global Semiconductor Equipment vs Taiwan Exports',
        source='MacroMicro'
    )


def chart_39_it_investment_gdp():
    """Chart 39: US IT Investment Contribution to GDP (MacroMicro)"""
    image_path = MACROMICRO_DIR / "it_investment_gdp.png"
    return create_image_chart(
        chart_number=39,
        image_path=image_path,
        title='US IT Investment Contribution to Real GDP Growth',
        source='MacroMicro'
    )


# === TradingView Single Name Charts (40-42) ===
# 3-Panel Setup: Price + 50/200 SMA, Relative Strength, Robust Relative Z-Score

def chart_40_nvda():
    """Chart 40: NVDA - AI Infrastructure Leader (TradingView 3-Panel)"""
    image_path = TRADINGVIEW_IMG_DIR / "nvda_3panel.png"
    return create_image_chart(
        chart_number=40,
        image_path=image_path,
        title='NVDA: AI Infrastructure Leader (vs SMH Benchmark)',
        source='TradingView - 3-Panel Analysis'
    )


def chart_41_msft():
    """Chart 41: MSFT - Cloud/AI Software Leader (TradingView 3-Panel)"""
    image_path = TRADINGVIEW_IMG_DIR / "msft_3panel.png"
    return create_image_chart(
        chart_number=41,
        image_path=image_path,
        title='MSFT: Cloud/AI Software Leader (vs QQQ Benchmark)',
        source='TradingView - 3-Panel Analysis'
    )


def chart_42_tsm():
    """Chart 42: TSM - Foundry Capacity Bottleneck (TradingView 3-Panel)"""
    image_path = TRADINGVIEW_IMG_DIR / "tsm_3panel.png"
    return create_image_chart(
        chart_number=42,
        image_path=image_path,
        title='TSM: Foundry Capacity Bottleneck (vs SMH Benchmark)',
        source='TradingView - 3-Panel Analysis'
    )


# Section 6 complete: 7 AI infrastructure charts (4 MacroMicro + 3 TradingView)
# Charts display images with proper Lighthouse branding overlay
