#!/usr/bin/env python3
"""One-off + reusable font unifier — collapse the legacy editorial typefaces
(Fraunces serif, Space Grotesk, JetBrains Mono) onto the canonical Inter system
defined in scripts/style_base.py.

Patches BOTH the rendered HTML (the live site — preserves the mobile-first-patch,
hand-fixes and content that a full rebuild would destroy) AND the 4 generators
(so future builds stay Inter). Pure ordered string replacement — no parsing, fully
reversible via git. Run from repo root: python3 scripts/unify_fonts.py [--check]
"""
from __future__ import annotations
import sys
from pathlib import Path

raise SystemExit(
    "VEROUDERD (2026-07, playbook 15): unify_fonts.py zou Inter + Google-Fonts-CDN "
    "terugzetten. De site is inmiddels self-hosted Hanken Grotesk + Bricolage "
    "Grotesque (zie scripts/deslop_fonts.py). Niet meer draaien."
)

ROOT = Path(__file__).resolve().parent.parent
CANON_LINK = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap"

# Ordered replacements. Longest/most-specific FIRST so a later bare rule never
# half-matches a string an earlier rule already handled.
REPLACEMENTS = [
    # --- Fraunces display headings: swap to Inter AND bump weight 500 -> 700 to
    #     match the canonical h1-h4 (Inter 700). Compound first, bare second.
    ("font-family:'Fraunces', Georgia, serif; font-weight:500",
     "font-family:'Inter', -apple-system, sans-serif; font-weight:700"),
    ("font-family:'Fraunces', Georgia, serif",
     "font-family:'Inter', -apple-system, sans-serif"),

    # --- Space Grotesk (labels/badges/prices) -> Inter. With-fallback variants
    #     before the bare one. Include the escaped-quote variant from generators.
    ("font-family:'Space Grotesk', sans-serif", "font-family:'Inter', sans-serif"),
    ("font-family:'Space Grotesk',sans-serif",  "font-family:'Inter',sans-serif"),
    ("font-family:\\'Space Grotesk\\',sans-serif", "font-family:\\'Inter\\',sans-serif"),
    ("font-family:'Space Grotesk'", "font-family:'Inter'"),

    # --- JetBrains Mono (postcode cells) -> Inter with tabular numerals.
    ("font-family:'JetBrains Mono', ui-monospace, monospace",
     "font-family:'Inter', sans-serif; font-variant-numeric:tabular-nums"),
    ("font-family:'JetBrains Mono', monospace",
     "font-family:'Inter', sans-serif; font-variant-numeric:tabular-nums"),

    # --- Google Fonts links: every legacy combination -> canonical Inter-only.
    #     Covers the two main hrefs (clean + _fmt_nl-corrupted dot variant),
    #     the JetBrains variant, and the missing-900 variants.
    ("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&display=swap", CANON_LINK),
    ("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144.400;9..144.500;9..144.600&display=swap", CANON_LINK),
    ("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap", CANON_LINK),
    ("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap", CANON_LINK),
]


def patch_text(text: str) -> tuple[str, int]:
    n = 0
    for old, new in REPLACEMENTS:
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            n += c
    return text, n


def targets() -> list[Path]:
    files: list[Path] = []
    fe = ROOT / "frontend"
    files += [p for p in fe.rglob("*.html") if "/admin/" not in str(p)]
    for g in ("build_robots", "build_news", "build_guides", "build_landingpages", "style_base"):
        p = ROOT / "scripts" / f"{g}.py"
        if p.exists():
            files.append(p)
    return files


def main() -> int:
    check = "--check" in sys.argv[1:]
    total_files = total_repl = 0
    for path in targets():
        text = path.read_text(encoding="utf-8")
        new, n = patch_text(text)
        if n:
            total_files += 1
            total_repl += n
            rel = path.relative_to(ROOT)
            print(f"  {'would patch' if check else 'patched'} {rel}  ({n} repl)")
            if not check:
                tmp = path.with_suffix(path.suffix + ".tmp")
                tmp.write_text(new, encoding="utf-8")
                tmp.replace(path)
    verb = "would change" if check else "changed"
    print(f"\n{verb} {total_files} files, {total_repl} replacements.")
    # Residual check — anything still on a legacy face?
    leftover = 0
    for path in targets():
        t = path.read_text(encoding="utf-8")
        for face in ("Fraunces", "Space Grotesk", "JetBrains Mono"):
            leftover += t.count(face)
    print(f"residual legacy-font mentions remaining: {leftover}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
