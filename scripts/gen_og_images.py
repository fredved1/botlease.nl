#!/usr/bin/env python3
"""Genereert 1200×630 OG/Discover-varianten van de nieuws-hero-foto's.

Google Discover vereist beelden ≥1200px breed; de robot-foto's zijn 1000×1250
portret. Dit script maakt per foto een liggende merk-variant:
cover-geschaalde blur-achtergrond + scherpe contain-foto + BotLease-merkbalk.

Output: frontend/img/og/<stem>-og.jpg  (build_news.og_image_for verwijst hiernaar)
Draaien na het toevoegen van nieuwe foto's aan de pool: python3 scripts/gen_og_images.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "frontend" / "img"
OUT = IMG / "og"
W, H = 1200, 630

FONT_PATHS = ["/System/Library/Fonts/Helvetica.ttc",
              "/System/Library/Fonts/Supplemental/Arial.ttf"]


def font(size: int, bold: bool = False):
    for fp in FONT_PATHS:
        try:
            return ImageFont.truetype(fp, size, index=1 if bold else 0)
        except Exception:
            continue
    return ImageFont.load_default()


def make_og(src: Path, dst: Path) -> None:
    im = Image.open(src).convert("RGBA")
    # transparante foto's eerst op de site-achtergrond leggen
    base = Image.new("RGBA", im.size, (245, 245, 247, 255))
    base.alpha_composite(im)
    im = base.convert("RGB")

    # achtergrond: cover-schaal + blur + lichte sluier (site-tint)
    scale = max(W / im.width, H / im.height)
    bg = im.resize((round(im.width * scale), round(im.height * scale)))
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2,
                  (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    bg = bg.filter(ImageFilter.GaussianBlur(26))
    veil = Image.new("RGB", (W, H), (245, 245, 247))
    bg = Image.blend(bg, veil, 0.55)

    # voorgrond: contain-schaal als afgeronde kaart met zachte schaduw, rechts uitgelijnd
    fh = H - 80
    fscale = fh / im.height
    fg = im.resize((round(im.width * fscale), fh))
    canvas = bg.copy()
    x, y = W - fg.width - 90, (H - fh) // 2
    r = 28
    # schaduw
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x + 6, y + 10, x + fg.width + 6, y + fh + 10),
                                         radius=r, fill=(0, 0, 0, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), sh).convert("RGB")
    # foto met afgeronde hoeken + dunne rand
    mask = Image.new("L", fg.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, fg.width, fh), radius=r, fill=255)
    canvas.paste(fg, (x, y), mask)
    ImageDraw.Draw(canvas).rounded_rectangle((x, y, x + fg.width, y + fh),
                                             radius=r, outline=(210, 210, 215), width=2)

    # merkbalk linksonder
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((48, H - 118, 458, H - 48), radius=16, fill=(29, 29, 31))
    d.text((72, H - 104), "BotLease", font=font(34, bold=True), fill=(245, 245, 247))
    d.text((232, H - 96), "·  NIEUWS", font=font(22), fill=(41, 151, 255))
    d.text((48, 52), "HUMANOÏDE ROBOTS IN NEDERLAND", font=font(20), fill=(66, 66, 69))

    canvas.save(dst, "JPEG", quality=86, optimize=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    robots_dir = IMG / "robots"
    done = 0
    for src in sorted(robots_dir.glob("*.webp")) + [robots_dir / "apollo.png"]:
        if not src.exists():
            continue
        dst = OUT / f"{src.stem.replace('-norm', '')}-og.jpg"
        make_og(src, dst)
        done += 1
    print(f"✅ {done} OG-beelden (1200×630) → {OUT}")


if __name__ == "__main__":
    main()
