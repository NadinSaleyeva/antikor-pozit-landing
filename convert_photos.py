#!/usr/bin/env python3
"""Convert PNG photos to WebP format for web optimization"""

from PIL import Image
import os
from pathlib import Path

# Source and destination directories
source_dir = Path("PHOTO")
dest_dir = Path("assets/gallery")

# Create destination directory if it doesn't exist
dest_dir.mkdir(parents=True, exist_ok=True)

# Get all PNG files
png_files = sorted(source_dir.glob("*.png"))

print(f"Found {len(png_files)} PNG files to convert")
print(f"Destination: {dest_dir}")
print("-" * 50)

total_original_size = 0
total_webp_size = 0

for png_file in png_files:
    # Get original file size
    original_size = png_file.stat().st_size
    total_original_size += original_size

    # Create output filename
    webp_filename = png_file.stem + ".webp"
    output_path = dest_dir / webp_filename

    # Open and convert image
    img = Image.open(png_file)

    # Convert to RGB if necessary (WebP doesn't support all modes)
    if img.mode in ("RGBA", "LA", "P"):
        # Create white background
        background = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        if img.mode in ("RGBA", "LA"):
            background.paste(img, mask=img.split()[-1])
            img = background
    elif img.mode != "RGB":
        img = img.convert("RGB")

    # Save as WebP with quality 85
    img.save(output_path, "WebP", quality=85, method=6)

    # Get WebP file size
    webp_size = output_path.stat().st_size
    total_webp_size += webp_size

    # Calculate savings
    savings = ((original_size - webp_size) / original_size) * 100

    print(f"[OK] {png_file.name}")
    print(f"  {original_size / 1024 / 1024:.2f}MB -> {webp_size / 1024 / 1024:.2f}MB ({savings:.1f}% smaller)")

print("-" * 50)
print(f"\nTotal original size: {total_original_size / 1024 / 1024:.2f}MB")
print(f"Total WebP size: {total_webp_size / 1024 / 1024:.2f}MB")
print(f"Total savings: {((total_original_size - total_webp_size) / total_original_size) * 100:.1f}%")
print(f"\nAll files converted to: {dest_dir}/")
