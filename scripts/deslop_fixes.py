#!/usr/bin/env python3
"""De-slop pass 2 (playbook 15, juli 2026) — mechanische bron-fixes na de font-swap.

Families (gevonden met impeccable detect, element-geannoteerd):
  1. clipped-overflow: skip-link off-screen -> fixed+transform; .lang-menu calc(100%+6px) -> 30px
  2. side-tab: .tldr border-left:4px -> volle tint zonder zijstreep
  3. cramped-padding: .video-wrap border+bg weg (thumbnail vult de kaart); .hub-thumb border-bottom weg
  4. low-contrast: .cta-strip p verliest van section.body p (specificiteit) -> geprefixte selector;
     .vlabel wit-op-onbekende-bg -> eigen donkere chip; #ffd166-notice -> donker amber;
     admin-tokens (#71717a op #0a0a0e, wit op #f97316)
  5. tiny-text: 11.5px form-notes en 11px .src -> 12px
  6. tight-leading: nieuws kaart/lead-koppen (anchors erven te krappe lh) -> 1.35
  7. all-caps-body: uppercase eyebrows/vendor-labels (>30 tekens) -> mixed case, homepage-stijl
  8. skipped-heading: TL;DR h3->h2, FAQ/usecase/robotkaart h4->h3, stads-/sectorkaarten h4->h2,
     vergelijk-kaarten h3->h2 (selectors bewegen mee, specificiteit geprefixd)
  9. numbered-section-markers: usecase-nummers 01..04 -> 1..4
 10. SVG-watermerk <text> (Inter-attribuut + contrast-ruis) verwijderd

Patcht HTML in-place (mobile-first-patch-pagina's mogen niet gerebuild) EN generators.
Run vanuit repo-root: python3 scripts/deslop_fixes.py
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"

GENERATORS = [ROOT / g for g in (
    "scripts/style_base.py", "scripts/build_news.py", "scripts/build_robots.py",
    "scripts/build_guides.py", "scripts/build_landingpages.py",
)]

# ── 1. Globale string-replacements (alle HTML + generators) ──────────────────
GLOBAL_REPLACEMENTS: list[tuple[str, str]] = [
    # skip-link: fixed + transform i.p.v. absolute off-screen (body clipt hem niet meer)
    (".skip-to-main{position:absolute;left:-9999px;top:0;z-index:200;background:var(--accent,#0066cc);color:#fff;padding:10px 16px;font-weight:600;text-decoration:none;}\n.skip-to-main:focus{left:0;}",
     ".skip-to-main{position:fixed;top:0;left:0;transform:translateY(-150%);z-index:200;background:var(--accent,#0066cc);color:#fff;padding:10px 16px;font-weight:600;text-decoration:none;}\n.skip-to-main:focus{transform:none;}"),
    # taalmenu: 100%-calc triggert clip-detectie; nav-hoogte is vast dus 30px is deterministisch
    ("position:absolute; top:calc(100% + 6px); right:0;",
     "position:absolute; top:30px; right:0;"),
    # TL;DR-callout: zijstreep weg, tint + volle radius blijft
    ("  position:relative;\n  background:var(--accent-soft);\n  border-left:4px solid var(--accent);\n  border-radius:0 12px 12px 0;\n  padding:22px 28px 22px 28px;\n  margin:0 0 36px;",
     "  position:relative;\n  background:var(--accent-soft);\n  border-radius:12px;\n  padding:22px 28px;\n  margin:0 0 36px;"),
    # video-facade: kaartrand+bg weg (thumbnail vult het vlak, detector: cramped-padding)
    ("  position:relative; border-radius:16px; overflow:hidden;\n  aspect-ratio:16/9; background:var(--bg-darker);\n  cursor:pointer; max-width:880px; margin:0 auto;\n  box-shadow:var(--shadow-lg); border:1px solid var(--border);",
     "  position:relative; border-radius:16px; overflow:hidden;\n  aspect-ratio:16/9;\n  cursor:pointer; max-width:880px; margin:0 auto;\n  box-shadow:var(--shadow-lg);"),
    # video-label: eigen donkere chip i.p.v. wit-op-thumbnail (leesbaar op elke thumbnail)
    ("  position:absolute; bottom:20px; left:24px; right:24px;\n  color:white; font-family:'Hanken Grotesk'; font-weight:600; font-size:17px;\n  text-shadow:0 2px 12px rgba(0,0,0,0.9);\n  pointer-events:none;",
     "  position:absolute; bottom:16px; left:16px; right:auto; max-width:calc(100% - 32px);\n  color:#f5f5f7; font-family:'Hanken Grotesk'; font-weight:600; font-size:15px;\n  background:rgba(0,0,0,0.72); border-radius:10px; padding:8px 14px;\n  pointer-events:none;"),
    # robots-hub thumbnail: border-bottom weg (kaart heeft al een eigen rand)
    ("  background:linear-gradient(180deg, var(--bg-2) 0%, var(--bg-card) 100%);\n  position:relative; overflow:hidden;\n  display:flex; align-items:center; justify-content:center;\n  border-bottom:1px solid var(--border);",
     "  background:linear-gradient(180deg, var(--bg-2) 0%, var(--bg-card) 100%);\n  position:relative; overflow:hidden;\n  display:flex; align-items:center; justify-content:center;"),
    # cta-strip: verloor van section.body p (specificiteit) -> donkergrijs-op-zwart, echte bug
    (".cta-strip p { color:var(--ink-2-on-dark); margin-bottom:24px; font-size:16px; }",
     "section.body .cta-strip p, .cta-strip p { color:var(--ink-2-on-dark); margin-bottom:24px; font-size:16px; }"),
    # form-notes 11.5px -> 12px (tiny-text)
    ("font-size:11.5px", "font-size:12px"),
    # nieuws-kaart bron-regel 11px -> 12px
    ("article.card .src { font-size:11px;", "article.card .src { font-size:12px;"),
    # nieuws koppen: anchors erven krappe line-height (tight-leading)
    ("article.card h2 { font-family:'Bricolage Grotesque', -apple-system, sans-serif; font-weight:600; font-size:18px; line-height:1.28;",
     "article.card h2 { font-family:'Bricolage Grotesque', -apple-system, sans-serif; font-weight:600; font-size:18px; line-height:1.35;"),
    ("article.card h2 { font-family:'Hanken Grotesk'; font-weight:600; font-size:18px; line-height:1.28;",
     "article.card h2 { font-family:'Hanken Grotesk'; font-weight:600; font-size:18px; line-height:1.35;"),
    ("article.card.sub-featured h2 { font-size:21px; line-height:1.22; }",
     "article.card.sub-featured h2 { font-size:21px; line-height:1.35; }"),
    ("line-height:1.12; letter-spacing:-0.025em; margin-bottom:14px; color:#fff;",
     "line-height:1.32; letter-spacing:-0.025em; margin-bottom:14px; color:#fff;"),
    # uppercase eyebrow (landingpages/sectoren/robots-templates) -> homepage-stijl, geen caps
    ("  display:inline-block; color:var(--accent); font-size:12.5px;\n  text-transform:uppercase; letter-spacing:0.12em; font-weight:600;\n  margin-bottom:16px;",
     "  display:inline-block; color:var(--accent); font-size:14px;\n  letter-spacing:-0.005em; font-weight:600;\n  margin-bottom:14px;"),
    # vendor-/speclabels met landnaam (>30 tekens uppercase) -> mixed case, iets groter
    (".r-body .v { font-size:11px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.1em; font-weight:600; margin-bottom:4px; }",
     ".r-body .v { font-size:12.5px; color:var(--ink-3); letter-spacing:0.01em; font-weight:600; margin-bottom:4px; }"),
    (".hub-card .vendor { color:var(--ink-3); font-size:10.5px; text-transform:uppercase; letter-spacing:0.1em; font-weight:600; margin-bottom:4px; }",
     ".hub-card .vendor { color:var(--ink-3); font-size:12.5px; letter-spacing:0.01em; font-weight:600; margin-bottom:4px; }"),
    (".r-hero .vendor { color:var(--ink-3); font-size:12.5px; text-transform:uppercase; letter-spacing:0.12em; font-weight:600; margin-bottom:8px; }",
     ".r-hero .vendor { color:var(--ink-3); font-size:12.5px; letter-spacing:0.01em; font-weight:600; margin-bottom:8px; }"),
    # pre-order notice: licht amber op wit is onleesbaar -> donker amber
    ("border:1px solid rgba(255,201,102,0.3); border-radius:10px; padding:14px 18px; color:#ffd166;",
     "border:1px solid rgba(255,201,102,0.45); border-radius:10px; padding:14px 18px; color:#7a4f00;"),
    # TL;DR-kop wordt h2 (markup hieronder); selector dekt beide
    (".tldr h3 { font-size:12.5px;", ".tldr h2, .tldr h3 { font-size:12.5px;"),
    # QA-vragen h4 -> h3
    (".qa-item h4 {", ".qa-item h3, .qa-item h4 {"),
    # usecase-kaarten h4 -> h3
    (".usecase-card h4 {", ".usecase-card h3, .usecase-card h4 {"),
    # robotkaarten h4 -> h3 (leasen/sectoren; leasen/index en sectoren/index -> h2)
    (".r-body h4 {", "section.body .r-body h2, .r-body h2, .r-body h3, .r-body h4 {"),
    # vergelijk-kaarten h3 -> h2 op vergelijken-pagina's
    (".h2h-card h3 {", "section.body .h2h-card h2, .h2h-card h2, .h2h-card h3 {"),
]

# ── 2. Markup-transformaties per bestandsfamilie ─────────────────────────────
TLDR_FILES_MARK = "<h3>TL;DR</h3>"

# alle h4 -> h3 (QA-vragen, usecase-kaarten, robotkaarten); outline is per bestand geverifieerd
H4_TO_H3_FILES = [
    "veelgestelde-vragen.html", "robot-as-a-service.html", "huren.html", "mkb.html",
    "full-service-lease.html", "kosten.html", "prijzen.html", "personeelstekort-humanoide-robot.html",
    "robot-vs-uitzendkracht.html", "terugverdientijd-roi.html", "beste-humanoide-robots-2026.html",
    "machineverordening-2027-humanoide-robots.html", "methodologie.html", "over.html",
    "gids/humanoide-robot-leasen.html", "gids/ai-act-machineverordening.html", "robots/tesla-optimus.html",
    "sectoren/3pl-fulfillment.html", "sectoren/productie-assemblage.html",
    "sectoren/hospitality-retail.html", "sectoren/zorg-instellingen.html",
    "leasen/amsterdam.html", "leasen/den-haag.html", "leasen/eindhoven.html",
    "leasen/noord-brabant.html", "leasen/rotterdam.html", "leasen/utrecht.html",
    "robots/1x-neo.html", "robots/agility-digit.html", "robots/apptronik-apollo.html",
    "robots/engineai-se01.html", "robots/figure-02.html", "robots/neura-4ne1-gen3.html",
    "robots/neura-4ne1-mini.html", "robots/pollen-reachy-2.html", "robots/ubtech-walker-s2.html",
    "robots/unitree-g1.html", "robots/unitree-h1-2.html", "robots/unitree-h2.html",
    "robots/unitree-r1.html", "vergelijken/humanoid-vs-cobot.html", "vergelijken/lease-vs-koop.html",
]

# h4 -> h2 (kaarttitels direct na h1)
H4_TO_H2_FILES = ["leasen/index.html", "sectoren/index.html"]

# h2h-kaart h3 -> h2 (modelnamen direct na h1)
H2H_TO_H2_FILES = [
    "vergelijken/apptronik-apollo-vs-figure-02.html",
    "vergelijken/neura-4ne1-gen3-vs-apptronik-apollo.html",
    "vergelijken/unitree-g1-vs-neura-4ne1-mini.html",
    "vergelijken/unitree-h1-2-vs-ubtech-walker-s2.html",
    "vergelijken/unitree-r1-vs-engineai-se01.html",
]


def patch_global(text: str) -> tuple[str, int]:
    n = 0
    for old, new in GLOBAL_REPLACEMENTS:
        if old in text:
            n += text.count(old)
            text = text.replace(old, new)
    return text, n


def main() -> int:
    total = 0
    html_files = sorted(FRONTEND.rglob("*.html"))
    for p in html_files + GENERATORS:
        src = p.read_text(encoding="utf-8")
        out, n = patch_global(src)
        rel = str(p.relative_to(ROOT))

        if p.suffix == ".html":
            frel = str(p.relative_to(FRONTEND))
            # TL;DR h3 -> h2
            if TLDR_FILES_MARK in out:
                out = out.replace(TLDR_FILES_MARK, "<h2>TL;DR</h2>")
                n += 1
            # begrippen: h3 direct na h1 -> h2
            if frel == "begrippen.html":
                out = out.replace("<h3>Een term mist?</h3>", "<h2>Een term mist?</h2>")
                out = out.replace(".cta-strip h3 {", ".cta-strip h2, .cta-strip h3 {")
                n += 1
            if frel in H4_TO_H3_FILES:
                c = out.count("<h4") + out.count("</h4>")
                out = re.sub(r"<h4(\s|>)", lambda m: "<h3" + m.group(1), out)
                out = out.replace("</h4>", "</h3>")
                n += c
            if frel in H4_TO_H2_FILES:
                c = out.count("<h4") + out.count("</h4>")
                out = re.sub(r"<h4(\s|>)", lambda m: "<h2" + m.group(1), out)
                out = out.replace("</h4>", "</h2>")
                n += c
            if frel in H2H_TO_H2_FILES:
                # de modelnaam-h3 volgt altijd direct op de .vendor-div in de h2h-kaart
                out, c3 = re.subn(r'(<div class="vendor">[^<]*</div>\s*)<h3>([^<]*)</h3>', r"\1<h2>\2</h2>", out)
                n += c3
        # nieuws SVG-watermerk (Inter-attribuut, contrast-ruis, decoratief op 6% opacity)
        c = len(re.findall(r'<text [^>]*fill-opacity="0\.06"[^>]*>[^<]*</text>', out))
        if c:
            out = re.sub(r'<text [^>]*fill-opacity="0\.06"[^>]*>[^<]*</text>', "", out)
            n += c
        # generator-parity voor watermerk (python-code in build_news.py)
        if p.name == "build_news.py":
            wm = ("    o.append(f'<text x=\"{w-44}\" y=\"{h-34}\" text-anchor=\"end\" font-family=\"Inter,sans-serif\" '\n"
                  "             f'font-size=\"118\" font-weight=\"800\" fill=\"{acc2}\" fill-opacity=\"0.06\">{escape(cat[:2].upper())}</text>')\n")
            if wm in out:
                out = out.replace(wm, "")
                n += 1

        if out != src:
            p.write_text(out, encoding="utf-8")
            total += n
            print(f"  {rel}: {n}")
    print(f"TOTAAL: {total} wijzigingen")
    return 0


if __name__ == "__main__":
    sys.exit(main())
