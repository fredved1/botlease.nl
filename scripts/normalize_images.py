#!/usr/bin/env python3
"""
Normaliseer alle robot foto's naar identieke 1000x1250 (4:5 portrait) PNG met
transparante achtergrond. Hierdoor renderen alle foto's even groot in cards
ongeacht de oorspronkelijke aspect ratio.

Werkt op: jpg, png, webp.
Output: <slug>.png in dezelfde dir.
Overschrijft originelen ALLEEN als --replace flag.
"""
from __future__ import annotations
import sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "frontend" / "img" / "robots"

# Target canvas — 4:5 portrait
TARGET_W = 1000
TARGET_H = 1250

# How much of the canvas the photo should fill (rest is padding)
SCALE = 0.92


def normalize(src_path: Path, out_path: Path):
    """Resize image to fit TARGET_W × TARGET_H × SCALE, centered, transparent bg."""
    img = Image.open(src_path)

    # Apply EXIF orientation if any
    img = ImageOps.exif_transpose(img)

    # Convert to RGBA for transparency
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # If the photo has a non-transparent background (most), try to detect dominant edge
    # color and make it transparent. Skip for now — keep original background since
    # most photos have white/grey backgrounds that look fine in cards.

    # Compute scale to fit within (TARGET_W × SCALE, TARGET_H × SCALE)
    max_w = int(TARGET_W * SCALE)
    max_h = int(TARGET_H * SCALE)

    scale_w = max_w / img.width
    scale_h = max_h / img.height
    scale = min(scale_w, scale_h)

    new_w = int(img.width * scale)
    new_h = int(img.height * scale)

    img_resized = img.resize((new_w, new_h), Image.LANCZOS)

    # Center on transparent canvas
    canvas = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
    paste_x = (TARGET_W - new_w) // 2
    paste_y = (TARGET_H - new_h) // 2
    canvas.paste(img_resized, (paste_x, paste_y), img_resized)

    # Save as WebP with transparency — ~70% smaller than PNG, alle moderne browsers
    canvas.save(out_path, "WEBP", quality=88, method=6)
    return canvas.size


def main():
    if not SRC_DIR.exists():
        print(f"❌ {SRC_DIR} does not exist")
        return

    images = []
    for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp"):
        images.extend(SRC_DIR.glob(ext))

    print(f"Found {len(images)} images to normalize")

    for src in sorted(images):
        # Skip if already normalized (filename ends in -norm)
        if src.stem.endswith("-norm"):
            continue
        out = src.with_name(f"{src.stem}-norm.webp")
        try:
            size = normalize(src, out)
            print(f"✓ {src.name} → {out.name}  {size[0]}×{size[1]}  ({out.stat().st_size // 1024}KB)")
        except Exception as e:
            print(f"✗ {src.name} FAILED: {e}")


if __name__ == "__main__":
    main()
