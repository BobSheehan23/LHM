"""
HORIZON 2026 - CHART ANNOTATION REPLACER V2
Uses pixel-color detection to find and replace magenta annotations
More reliable than OCR for small colored text
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pathlib import Path
import json

# ============================================================================
# CONFIGURATION
# ============================================================================

# Magenta color range (Hot Magenta: RGB 255, 35, 137)
MAGENTA_THRESHOLD = {
    'r_min': 200, 'r_max': 255,
    'g_min': 0,   'g_max': 100,
    'b_min': 100, 'b_max': 200
}

# Font settings
try:
    FONT = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', size=16)
except:
    try:
        FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size=16)
    except:
        FONT = ImageFont.load_default()

MAGENTA_COLOR = (255, 35, 137)  # Hot Magenta

# Manual corrections (chart_name → new_value mapping)
MANUAL_CORRECTIONS = {
    'chart_03': '295',  # Credit Spread Waterfall: HY 298 → 295
    'chart_04': '+0.16σ',  # Credit-Labor Gap: -0.28σ → +0.16σ
    'chart_13': '-0.63σ',  # Labor Fragility Index: needs annotation
    'chart_19': '-0.63σ',  # LFI alt: 0.13σ → -0.63σ
}

# ============================================================================
# ANNOTATION DETECTION
# ============================================================================

def find_magenta_annotations(img):
    """
    Find all magenta text regions in the image.
    Returns list of bounding boxes.
    """
    width, height = img.size
    pixels = img.load()
    
    magenta_pixels = []
    
    # Scan image for magenta pixels
    for x in range(width):
        for y in range(height):
            try:
                r, g, b = pixels[x, y][:3]
                
                # Check if pixel matches magenta criteria
                if (MAGENTA_THRESHOLD['r_min'] <= r <= MAGENTA_THRESHOLD['r_max'] and
                    MAGENTA_THRESHOLD['g_min'] <= g <= MAGENTA_THRESHOLD['g_max'] and
                    MAGENTA_THRESHOLD['b_min'] <= b <= MAGENTA_THRESHOLD['b_max']):
                    magenta_pixels.append((x, y))
            except:
                continue
    
    if not magenta_pixels:
        return []
    
    # Cluster nearby pixels into bounding boxes
    # Sort by x-coordinate to group nearby text
    magenta_pixels.sort()
    
    bboxes = []
    current_cluster = [magenta_pixels[0]]
    
    for pixel in magenta_pixels[1:]:
        # If pixel is within 50px of last pixel in cluster, add to cluster
        if abs(pixel[0] - current_cluster[-1][0]) < 50 and abs(pixel[1] - current_cluster[-1][1]) < 50:
            current_cluster.append(pixel)
        else:
            # Start new cluster
            if len(current_cluster) > 10:  # Filter noise
                # Create bbox for this cluster
                xs = [p[0] for p in current_cluster]
                ys = [p[1] for p in current_cluster]
                bbox = (min(xs), min(ys), max(xs), max(ys))
                bboxes.append(bbox)
            
            current_cluster = [pixel]
    
    # Don't forget last cluster
    if len(current_cluster) > 10:
        xs = [p[0] for p in current_cluster]
        ys = [p[1] for p in current_cluster]
        bbox = (min(xs), min(ys), max(xs), max(ys))
        bboxes.append(bbox)
    
    return bboxes


def replace_annotation(img, bbox, new_text):
    """
    Replace annotation at bbox with new text.
    """
    draw = ImageDraw.Draw(img)
    
    x1, y1, x2, y2 = bbox
    
    # Expand bbox for clean erasure
    padding = 8
    erase_bbox = (x1 - padding, y1 - padding, x2 + padding, y2 + padding)
    
    # Erase old text (white background)
    draw.rectangle(erase_bbox, fill='white')
    
    # Draw new text in magenta
    # Center text in bbox
    bbox_text = draw.textbbox((0, 0), new_text, font=FONT)
    text_width = bbox_text[2] - bbox_text[0]
    text_height = bbox_text[3] - bbox_text[1]
    
    text_x = x1 + (x2 - x1 - text_width) // 2
    text_y = y1 + (y2 - y1 - text_height) // 2
    
    draw.text((text_x, text_y), new_text, fill=MAGENTA_COLOR, font=FONT)
    
    return img


# ============================================================================
# MAIN PROCESSING
# ============================================================================

def process_chart(input_path, output_dir):
    """
    Process a single chart.
    """
    chart_name = Path(input_path).stem
    print(f"\n{'='*80}")
    print(f"Processing: {chart_name}")
    print('='*80)
    
    # Check if manual correction exists
    if chart_name not in MANUAL_CORRECTIONS:
        print("  ✓ No corrections needed for this chart")
        return None
    
    new_value = MANUAL_CORRECTIONS[chart_name]
    
    # Load image
    img = Image.open(input_path).convert('RGB')
    
    # Find magenta annotations
    print("Detecting magenta annotations...")
    bboxes = find_magenta_annotations(img)
    print(f"  Found {len(bboxes)} magenta regions")
    
    if not bboxes:
        print("  ⚠️  No magenta annotations found to replace")
        # Still apply correction by adding annotation
        # Add text to bottom-right corner
        width, height = img.size
        draw = ImageDraw.Draw(img)
        text = f"Current: {new_value}"
        
        bbox_text = draw.textbbox((0, 0), text, font=FONT)
        text_width = bbox_text[2] - bbox_text[0]
        
        text_x = width - text_width - 50
        text_y = height - 50
        
        draw.text((text_x, text_y), text, fill=MAGENTA_COLOR, font=FONT)
        
        output_path = Path(output_dir) / f"{chart_name}_corrected.png"
        img.save(output_path, quality=95)
        print(f"  ✓ Added annotation: {new_value}")
        print(f"  ✓ Saved: {output_path.name}")
        return output_path
    
    # Replace each annotation (typically just one)
    for i, bbox in enumerate(bboxes):
        print(f"  Replacing annotation {i+1}: {bbox} → '{new_value}'")
        img = replace_annotation(img, bbox, new_value)
    
    # Save
    output_path = Path(output_dir) / f"{chart_name}_corrected.png"
    img.save(output_path, quality=95)
    print(f"  ✓ Saved: {output_path.name}")
    
    return output_path


def process_batch(input_dir, output_dir):
    """
    Process all charts in a directory.
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)
    
    # Get all PNG/JPG files
    image_files = sorted(list(input_path.glob('*.png')) + list(input_path.glob('*.jpg')))
    
    print(f"\n{'='*80}")
    print(f"HORIZON 2026 - BATCH ANNOTATION CORRECTION")
    print(f"Processing {len(image_files)} charts")
    print('='*80)
    
    results = {
        'processed': 0,
        'corrected': 0,
        'unchanged': 0,
        'corrections': []
    }
    
    for img_file in image_files:
        output = process_chart(img_file, output_path)
        results['processed'] += 1
        
        if output:
            results['corrected'] += 1
            results['corrections'].append({
                'input': str(img_file),
                'output': str(output),
                'chart_name': img_file.stem
            })
        else:
            results['unchanged'] += 1
    
    # Save summary
    summary_file = output_path / 'correction_summary.json'
    with open(summary_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*80}")
    print("BATCH COMPLETE")
    print('='*80)
    print(f"  Total processed: {results['processed']}")
    print(f"  Charts corrected: {results['corrected']}")
    print(f"  Charts unchanged: {results['unchanged']}")
    print(f"  Summary: {summary_file}")
    print('='*80)
    
    return results


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python chart_replacer_v2.py <input_dir> <output_dir>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    process_batch(input_dir, output_dir)
