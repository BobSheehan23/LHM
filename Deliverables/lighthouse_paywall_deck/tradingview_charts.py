"""
TradingView Single Name Charts
Charts 51-60: 3-Panel Setup with Robust Relative Z-Score
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from datetime import datetime

# Lighthouse Macro Brand Colors
COLORS = {
    'primary': '#003366',
    'secondary': '#0066CC',
    'accent': '#FF9900',
    'positive': '#00A86B',
    'negative': '#CC0000',
    'neutral': '#808080',
}


def add_branding(ax, chart_number, ticker):
    """Lighthouse Macro standard branding for TradingView charts"""
    from matplotlib.patches import Circle

    # Chart number badge
    circle = Circle((0.02, 0.98), 0.015, transform=ax.transAxes,
                   facecolor=COLORS['primary'], edgecolor='none', zorder=100)
    ax.add_patch(circle)
    ax.text(0.02, 0.98, str(chart_number),
            ha='center', va='center', fontsize=10, fontweight='bold',
            color='white', transform=ax.transAxes, zorder=101)

    # Top left: LIGHTHOUSE MACRO
    ax.text(0.045, 0.98, 'LIGHTHOUSE MACRO',
            ha='left', va='center', fontsize=9, fontweight='bold',
            color=COLORS['primary'], transform=ax.transAxes)

    # Bottom left: Source credit (small grey)
    ax.text(0.02, 0.02, f'Source: TradingView | {ticker}',
            ha='left', va='bottom', fontsize=7, color=COLORS['neutral'],
            transform=ax.transAxes, style='italic')

    # Bottom right: Watermark (ocean blue)
    ax.text(0.98, 0.02, 'MACRO, ILLUMINATED.',
            ha='right', va='bottom', fontsize=8, fontweight='bold',
            color=COLORS['primary'], alpha=0.6, transform=ax.transAxes)


# TradingView chart mappings
# Chart 51-60: Single Name Technical Analysis
TRADINGVIEW_CHARTS = {
    51: ('~/NVDA_2025-11-22_02-17-21.png', 'NVDA', 'AI Infrastructure Leader'),
    52: ('~/ASML_2025-11-22_02-17-37.png', 'ASML', 'Semiconductor Equipment'),
    53: ('~/MSFT_2025-11-22_02-28-11.png', 'MSFT', 'AI Software & Azure'),
    54: ('~/TSM_2025-11-22_02-18-09.png', 'TSM', 'Foundry Capacity'),
    55: ('~/COIN_2025-11-22_02-21-42.png', 'COIN', 'Crypto Exchange'),
    56: ('~/MSTR_2025-11-22_02-24-02.png', 'MSTR', 'Bitcoin Treasury'),
    57: ('~/MARA_2025-11-22_02-25-28.png', 'MARA', 'Bitcoin Miner'),
    58: ('~/JPM_2025-11-22_02-26-31.png', 'JPM', 'Primary Dealer Health'),
    59: ('~/GS_2025-11-22_02-26-13.png', 'GS', 'Market Maker Stress'),
    60: ('~/HYG_2025-11-22_02-29-52.png', 'HYG', 'High-Yield Credit ETF'),
}


def create_tradingview_chart(image_path, chart_num, ticker, description):
    """Create chart from TradingView PNG image"""
    fig, ax = plt.subplots(figsize=(11, 8.5))
    ax.axis('off')

    expanded_path = os.path.expanduser(image_path)
    if os.path.exists(expanded_path):
        img = mpimg.imread(expanded_path)
        ax.imshow(img, aspect='auto')

        # Add title above image
        fig.suptitle(f'{ticker}: {description}',
                    fontsize=16, fontweight='bold',
                    color=COLORS['primary'], y=0.98)

        add_branding(ax, chart_num, ticker)
    else:
        ax.text(0.5, 0.5, f'TradingView chart not found:\n{os.path.basename(image_path)}',
                ha='center', va='center', transform=ax.transAxes,
                fontsize=14, color=COLORS['negative'])
        add_branding(ax, chart_num, ticker)

    plt.tight_layout()
    return fig


def chart_51_nvda():
    """Chart 51: NVDA - AI Infrastructure Leader"""
    path, ticker, desc = TRADINGVIEW_CHARTS[51]
    return create_tradingview_chart(path, 51, ticker, desc)


def chart_52_asml():
    """Chart 52: ASML - Semiconductor Equipment"""
    path, ticker, desc = TRADINGVIEW_CHARTS[52]
    return create_tradingview_chart(path, 52, ticker, desc)


def chart_53_msft():
    """Chart 53: MSFT - AI Software & Azure"""
    path, ticker, desc = TRADINGVIEW_CHARTS[53]
    return create_tradingview_chart(path, 53, ticker, desc)


def chart_54_tsm():
    """Chart 54: TSM - Foundry Capacity"""
    path, ticker, desc = TRADINGVIEW_CHARTS[54]
    return create_tradingview_chart(path, 54, ticker, desc)


def chart_55_coin():
    """Chart 55: COIN - Crypto Exchange"""
    path, ticker, desc = TRADINGVIEW_CHARTS[55]
    return create_tradingview_chart(path, 55, ticker, desc)


def chart_56_mstr():
    """Chart 56: MSTR - Bitcoin Treasury"""
    path, ticker, desc = TRADINGVIEW_CHARTS[56]
    return create_tradingview_chart(path, 56, ticker, desc)


def chart_57_mara():
    """Chart 57: MARA - Bitcoin Miner"""
    path, ticker, desc = TRADINGVIEW_CHARTS[57]
    return create_tradingview_chart(path, 57, ticker, desc)


def chart_58_jpm():
    """Chart 58: JPM - Primary Dealer Health"""
    path, ticker, desc = TRADINGVIEW_CHARTS[58]
    return create_tradingview_chart(path, 58, ticker, desc)


def chart_59_gs():
    """Chart 59: GS - Market Maker Stress"""
    path, ticker, desc = TRADINGVIEW_CHARTS[59]
    return create_tradingview_chart(path, 59, ticker, desc)


def chart_60_hyg():
    """Chart 60: HYG - High-Yield Credit ETF"""
    path, ticker, desc = TRADINGVIEW_CHARTS[60]
    return create_tradingview_chart(path, 60, ticker, desc)
