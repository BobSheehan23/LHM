# Lighthouse Macro - Official Brand Colors

## CORRECTED COLOR PALETTE

```python
COLORS = {
    'ocean_blue': '#0089D1',      # Primary - Ocean Blue
    'orange': '#FF7700',           # Secondary - Orange
    'carolina_blue': '#4B9CD3',    # Tertiary - Carolina Blue
    'magenta': '#FF00FF',          # Quaternary - Magenta
    'neutral': '#808080',          # Grey for axes/text
}
```

## Color Usage Guidelines

- **Ocean Blue (#0089D1)**: Primary series, main chart lines, branding elements
- **Orange (#FF7700)**: Secondary series, dual-axis right side, highlights
- **Carolina Blue (#4B9CD3)**: Tertiary series, supporting data
- **Magenta (#FF00FF)**: Quaternary series, accent highlights
- **Grey (#808080)**: Axes, tick labels, neutral text

## Branding Elements

- **Top Left**: "LIGHTHOUSE MACRO" in ocean blue
- **Bottom Left**: Source attribution in grey (small, italic)
- **Bottom Right**: "MACRO, ILLUMINATED." in ocean blue (outside chart area, using fig.text())

## Chart Number Badge

- Circle filled with ocean blue (#0089D1)
- White text for chart number
- Positioned at top-left corner (0.02, 0.98) in axes coordinates

## Previous Incorrect Colors (DO NOT USE)

- ❌ #003366 (too dark)
- ❌ #005F9E (from old lhm_charts)
- ❌ #1f77b4 (matplotlib default)
- ❌ #FF6B35 (wrong orange)
- ❌ #1DAEFF (wrong carolina blue)
- ❌ #FF4FB3 (wrong magenta)
