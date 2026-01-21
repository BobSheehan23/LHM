#!/usr/bin/env python3
"""
Lighthouse Macro Risk Dashboard Generator
==========================================
Generates a branded ASCII dashboard summarizing the current risk assessment
from the ensemble model (probability + warning system + RMP).

Usage:
    python generate_dashboard.py
"""

import sys
sys.path.insert(0, "/Users/bob/LHM")

from lighthouse_quant.models.warning_system import WarningSystem, WarningLevel
from lighthouse_quant.models.risk_ensemble import RiskEnsemble


def generate_dashboard():
    """Generate and print the risk dashboard."""
    # Get data
    ws = WarningSystem()
    warning = ws.evaluate()
    ensemble = RiskEnsemble()
    result = ensemble.evaluate()
    rmp = warning.rmp_assessment

    # Dashboard width
    width = 76

    def box_line(content, style="middle"):
        if style == "top":
            return "╔" + "═" * (width - 2) + "╗"
        elif style == "bottom":
            return "╚" + "═" * (width - 2) + "╝"
        elif style == "divider":
            return "╠" + "═" * (width - 2) + "╣"
        elif style == "thin_divider":
            return "╟" + "─" * (width - 2) + "╢"
        else:
            padded = content.ljust(width - 4)
            return "║ " + padded + " ║"

    def center_line(content):
        padded = content.center(width - 4)
        return "║ " + padded + " ║"

    # Regime symbol
    regime_symbol = (
        "🔴" if result.regime.name in ("PRE_CRISIS", "CRISIS")
        else "🟡" if result.regime.name in ("LATE_CYCLE", "HOLLOW_RALLY")
        else "🟢"
    )

    # Build output
    lines = []
    lines.append("")
    lines.append(box_line("", "top"))
    lines.append(center_line("LIGHTHOUSE MACRO"))
    lines.append(center_line("RISK ASSESSMENT DASHBOARD"))
    lines.append(center_line(f"As of {result.date}"))
    lines.append(box_line("", "divider"))

    # REGIME SECTION
    lines.append(center_line(f"{regime_symbol}  REGIME: {result.regime.name.replace('_', ' ')}  {regime_symbol}"))
    lines.append(box_line(""))
    lines.append(box_line(f"Warning Level: {result.warning_level.name}     Model Agreement: {result.model_agreement}"))
    lines.append(box_line(f"Confidence: {result.confidence}              Allocation Multiplier: {result.allocation_multiplier:.2f}x"))
    lines.append(box_line("", "divider"))

    # PROBABILITY SECTION
    lines.append(center_line("PROBABILITY DECOMPOSITION"))
    lines.append(box_line("", "thin_divider"))
    lines.append(box_line(f"  Base Recession Probability (12-month):       {result.base_probability:>6.1%}"))
    lines.append(box_line(f"  + Discontinuity Premium (buffer depletion): +{result.discontinuity_premium:>6.1%}"))
    lines.append(box_line(f"  ─────────────────────────────────────────────────────"))
    lines.append(box_line(f"  ADJUSTED PROBABILITY:                        {result.adjusted_probability:>6.1%}"))
    lines.append(box_line("", "divider"))

    # CRITICAL TRIGGERS
    lines.append(center_line("CRITICAL WARNING TRIGGERS"))
    lines.append(box_line("", "thin_divider"))

    for trigger in result.warning_triggers[:4]:
        parts = trigger.split(":", 1)
        flag_name = parts[0].strip()
        description = parts[1].strip() if len(parts) > 1 else ""
        lines.append(box_line(f"  🚨 {flag_name}"))
        if description:
            lines.append(box_line(f"     {description[:64]}"))

    lines.append(box_line("", "divider"))

    # RMP ASSESSMENT
    lines.append(center_line("FED RESERVE MANAGEMENT (RMP) ASSESSMENT"))
    lines.append(box_line("", "thin_divider"))
    if rmp:
        lines.append(box_line(f"  Current Reserves:  ${rmp.reserves_current:,.0f}B    LCLOR: ${rmp.reserves_lclor:,.0f}B"))
        lines.append(box_line(f"  Buffer Above LCLOR: ${rmp.reserves_buffer:,.0f}B"))
        lines.append(box_line(""))
        lines.append(box_line(f"  Organic Drain Rate: ${rmp.drain_rate_monthly:.0f}B/month"))
        lines.append(box_line(f"  RMP Offset:        -${rmp.rmp_estimated_pace:.0f}B/month"))
        lines.append(box_line(f"  Net Drain Rate:     ${rmp.net_drain_rate:.1f}B/month"))
        lines.append(box_line(""))
        lines.append(box_line(f"  ⏱️  Runway to LCLOR: {rmp.months_to_lclor:.0f} months"))
        lines.append(box_line(f"  📊 Risk Modifier: {rmp.risk_modifier:+.0%} (Fed buying time, not rebuilding)"))
    else:
        lines.append(box_line("  RMP data not available"))
    lines.append(box_line("", "divider"))

    # KEY INSIGHT
    lines.append(center_line("THE HOLLOW RALLY THESIS"))
    lines.append(box_line("", "thin_divider"))
    lines.append(box_line("  Base probability (19.5%) reflects gradual deterioration."))
    lines.append(box_line("  But buffers are exhausted. RRP depleted. Reserves at LCLOR."))
    lines.append(box_line("  Credit spreads ignore labor fragility (CLG < -1.0)."))
    lines.append(box_line(""))
    lines.append(box_line("  Discontinuity risk is underpriced by smooth probability models."))
    lines.append(box_line("  The ensemble adds +50% to capture this hidden fragility."))
    lines.append(box_line("", "divider"))

    # POSITIONING
    lines.append(center_line("POSITIONING GUIDANCE"))
    lines.append(box_line("", "thin_divider"))
    lines.append(box_line("  ✗ Max defensive: 0.15x allocation multiplier"))
    lines.append(box_line("  ✗ No new longs until buffer rebuilds"))
    lines.append(box_line("  ✓ Cash is an active position"))
    lines.append(box_line("  ✓ Daily monitoring of funding stress indicators"))
    lines.append(box_line("", "divider"))

    # INVALIDATION
    lines.append(center_line("INVALIDATION CONDITIONS"))
    lines.append(box_line("", "thin_divider"))
    for cond in result.invalidation_conditions[:4]:
        lines.append(box_line(f"  → {cond[:68]}"))
    lines.append(box_line("", "divider"))

    # FOOTER
    lines.append(center_line("MACRO, ILLUMINATED."))
    lines.append(box_line("", "bottom"))
    lines.append("")

    # Print
    for line in lines:
        print(line)


if __name__ == "__main__":
    generate_dashboard()
