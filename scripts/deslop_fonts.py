#!/usr/bin/env python3
"""De-slop font pass (playbook 15, juli 2026) — vervang Inter (Google-CDN, AVG-risico
en detector-tell) door een self-hosted duo met karakter:

  - Body/labels:      Hanken Grotesk  (humanist, 300-700, woff2 in frontend/fonts/)
  - Koppen/display:   Bricolage Grotesque (600-800, woff2 in frontend/fonts/)

Patcht NET ALS scripts/unify_fonts.py BEIDE kanten: de gerenderde HTML (in-place,
want ~55 pagina's hebben een mobile-first-patch die generators niet emitten) EN de
generators (zodat toekomstige builds self-hosted blijven). Pure geordende
string-replacement — omkeerbaar via git. Run vanuit repo-root:
  python3 scripts/deslop_fonts.py [--check]
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD_PRECONNECT_1 = '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
OLD_PRECONNECT_2 = '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
OLD_CSS2_LINK = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">'
NEW_FONT_LINKS = (
    '<link rel="preload" as="font" type="font/woff2" crossorigin href="/fonts/hanken-grotesk-latin-400-normal.woff2">\n'
    '<link rel="preload" as="font" type="font/woff2" crossorigin href="/fonts/bricolage-grotesque-latin-700-normal.woff2">\n'
    '<link rel="stylesheet" href="/fonts/fonts.css">'
)

# Ordered: longest/most-specific first.
REPLACEMENTS = [
    (OLD_PRECONNECT_1, ""),
    (OLD_PRECONNECT_2, ""),
    (OLD_CSS2_LINK, NEW_FONT_LINKS),
    # Body stack (body {} rule)
    ("font-family:'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Helvetica Neue', sans-serif",
     "font-family:'Hanken Grotesk', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif"),
    # Rare inverted stack (admin/seo.html)
    ("font-family: -apple-system, 'Inter', sans-serif",
     "font-family:'Hanken Grotesk', -apple-system, sans-serif"),
    # Display/kop-stack: h1-h4, hero's, prijzen, display-cijfers
    ("font-family:'Inter', -apple-system, sans-serif",
     "font-family:'Bricolage Grotesque', -apple-system, sans-serif"),
    ("font-family:'Inter',-apple-system,sans-serif",
     "font-family:'Bricolage Grotesque',-apple-system,sans-serif"),
    # JS-emitted inline style op <h3> (escaped quotes in strings)
    ("font-family:\\'Inter\\',sans-serif", "font-family:\\'Bricolage Grotesque\\',sans-serif"),
    # Label/badge/tabular-varianten -> body-font
    ("font-family:'Inter', sans-serif", "font-family:'Hanken Grotesk', sans-serif"),
    ("font-family:'Inter',sans-serif", "font-family:'Hanken Grotesk',sans-serif"),
    # Bare 'Inter' (labels, eyebrows, badges) -> body-font. ALTIJD als laatste.
    ("font-family:'Inter'", "font-family:'Hanken Grotesk'"),
]

GENERATORS = [
    "scripts/style_base.py",
    "scripts/build_news.py",
    "scripts/build_robots.py",
    "scripts/build_guides.py",
    "scripts/build_landingpages.py",
]


def patch_text(text: str) -> tuple[str, int]:
    n = 0
    for old, new in REPLACEMENTS:
        if old in text:
            n += text.count(old)
            text = text.replace(old, new)
    return text, n


def main(check: bool = False) -> int:
    targets: list[Path] = sorted((ROOT / "frontend").rglob("*.html"))
    targets += [ROOT / g for g in GENERATORS]
    total = 0
    touched = 0
    for p in targets:
        if not p.exists():
            print(f"  !! ontbreekt: {p}")
            continue
        src = p.read_text(encoding="utf-8")
        out, n = patch_text(src)
        if n:
            touched += 1
            total += n
            if not check:
                p.write_text(out, encoding="utf-8")
    mode = "CHECK" if check else "PATCH"
    print(f"[{mode}] {touched} bestanden, {total} replacements")
    # Restwaarschuwing: nog Inter of Google-Fonts over?
    left = []
    for p in targets:
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8")
        if "fonts.googleapis" in s or "'Inter'" in s or "\\'Inter\\'" in s:
            left.append(str(p.relative_to(ROOT)))
    if left and not check:
        print(f"  LET OP, nog Inter/Google-Fonts in {len(left)} bestanden:")
        for f in left[:20]:
            print(f"    {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(check="--check" in sys.argv))
