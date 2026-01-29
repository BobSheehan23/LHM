#!/usr/bin/env python3
"""
Create Lighthouse Macro email header banner (1100x220 PNG)
Simply resize the existing banner to exact dimensions needed
"""

from PIL import Image

# Load the existing banner with the correct shield/beacon lighthouse
banner = Image.open("/Users/bob/LHM/Brand/Banner.JPG")

# Resize to exact email dimensions
resized = banner.resize((1100, 220), Image.LANCZOS)

# Convert to RGB if needed and save as PNG
if resized.mode != 'RGB':
    resized = resized.convert('RGB')

output_path = "/Users/bob/LHM/email_header_banner_1100x220.png"
resized.save(output_path, "PNG")
print(f"Banner saved to: {output_path}")
print(f"Dimensions: {resized.size[0]}x{resized.size[1]}")
