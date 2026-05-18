#!/usr/bin/env python3
"""
Generates:
- /gids/humanoide-robot-leasen.html      (pillar guide)
- /gids/ai-act-machineverordening.html   (AI-Act compliance guide)
- /begrippen.html                        (glossary)
- /over.html                             (about)
- /methodologie.html                     (methodology)
- /kosten.html                           (calculator)
- /vergelijken/index.html                (comparison hub)
- /vergelijken/<a>-vs-<b>.html           (head-to-head pages)
"""
from __future__ import annotations
import json
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"
SITE_URL = "https://botlease.nl"

sys.path.insert(0, str(ROOT / "scripts"))
from guides_data import PILLAR_GUIDE, AI_ACT_GUIDE, GLOSSARY, ABOUT, METHODOLOGY, COSTS_PAGE  # noqa: E402
from robots_data import ROBOTS, by_slug, available_robots, waitlist_robots  # noqa: E402

PAGE_CSS = """
*,*::before,*::after { margin:0; padding:0; box-sizing:border-box; }
:root {
  --bg:#08080a; --bg-2:#0e0e12; --bg-3:#16161c; --line:#23232c; --line-2:#2e2e38;
  --ink:#f7f7f9; --ink-2:#a5a5b3; --ink-3:#666672;
  --accent:#ff5e1f; --accent-2:#ffb098; --green:#5be584;
  --eu:#5be584; --value:#ffc966; --premium:#a6cbff;
}
html { scroll-behavior:smooth; }
body { font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif; background:var(--bg); color:var(--ink); line-height:1.65; -webkit-font-smoothing:antialiased; }
h1,h2,h3,h4 { font-family:'Space Grotesk',sans-serif; letter-spacing:-0.025em; line-height:1.2; font-weight:600; }
a { color:inherit; text-decoration:none; }
img { display:block; max-width:100%; height:auto; }
.container { max-width:1180px; margin:0 auto; padding:0 28px; }
.narrow { max-width:840px; margin:0 auto; padding:0 28px; }

nav.top {
  position:fixed; top:0; left:0; right:0; z-index:60;
  backdrop-filter:blur(20px) saturate(180%); -webkit-backdrop-filter:blur(20px) saturate(180%);
  background:rgba(8,8,10,0.78); border-bottom:1px solid rgba(255,255,255,0.05);
}
nav.top .row { display:flex; align-items:center; justify-content:space-between; padding:16px 0; }
.brand { display:flex; align-items:center; gap:10px; font-family:'Space Grotesk'; font-weight:700; font-size:19px; }
.brand-mark { width:26px; height:26px; border-radius:8px; background:linear-gradient(135deg, #ff5e1f, #ff8e5c); display:flex; align-items:center; justify-content:center; }
.nav-links { display:flex; gap:30px; }
.nav-links a { color:var(--ink-2); font-size:14px; font-weight:500; }
.nav-links a:hover, .nav-links a.active { color:var(--ink); }
.btn { display:inline-flex; align-items:center; gap:7px; padding:11px 20px; border-radius:999px; font-weight:600; font-size:14px; background:var(--accent); color:#fff; transition:transform .15s; }
.btn:hover { transform:translateY(-1px); }
.btn.ghost { background:transparent; border:1px solid var(--line-2); color:var(--ink); }

footer { padding:56px 0 36px; border-top:1px solid var(--line); background:var(--bg-2); margin-top:120px; }
footer .row { display:flex; justify-content:space-between; flex-wrap:wrap; gap:20px; color:var(--ink-3); font-size:13px; align-items:center; }
footer a { color:var(--ink-2); }
@media (max-width:780px) { .nav-links { display:none; } }

.crumbs { display:flex; gap:8px; font-size:13px; color:var(--ink-3); margin-bottom:24px; flex-wrap:wrap; }
.crumbs .sep { color:var(--line-2); }

.eyebrow { display:inline-block; color:var(--accent); font-size:12px; text-transform:uppercase; letter-spacing:0.16em; font-weight:600; margin-bottom:14px; padding:5px 12px; background:rgba(255,94,31,0.08); border:1px solid rgba(255,94,31,0.2); border-radius:999px; }

.g-hero { padding:140px 0 30px; position:relative; }
.g-hero::before { content:""; position:absolute; inset:0; background:radial-gradient(50% 50% at 80% 20%, rgba(255,94,31,0.14), transparent 60%); z-index:0; }
.g-hero .narrow { position:relative; z-index:2; }
.g-hero h1 { font-size:clamp(34px,4.4vw,54px); margin-bottom:18px; letter-spacing:-0.03em; }
.g-hero .tag { color:var(--accent-2); font-size:18px; margin-bottom:24px; max-width:760px; line-height:1.55; }

.tldr { background:linear-gradient(180deg, var(--bg-2) 0%, var(--bg-3) 100%); border:1px solid var(--line); border-radius:18px; padding:32px 36px; margin:40px 0; }
.tldr h3 { font-size:13px; color:var(--accent); text-transform:uppercase; letter-spacing:0.14em; margin-bottom:18px; }
.tldr ul { list-style:none; padding:0; }
.tldr li { padding:10px 0 10px 26px; position:relative; color:var(--ink); font-size:15.5px; line-height:1.65; border-bottom:1px solid var(--line); }
.tldr li:last-child { border-bottom:none; }
.tldr li::before { content:"→"; position:absolute; left:0; top:9px; color:var(--accent); font-weight:700; }

.toc { background:var(--bg-2); border:1px solid var(--line); border-radius:14px; padding:24px 30px; margin:32px 0; }
.toc h3 { font-size:13px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.12em; margin-bottom:14px; font-family:'Space Grotesk'; font-weight:600; }
.toc ol { padding-left:22px; }
.toc li { margin-bottom:7px; }
.toc a { color:var(--ink-2); font-size:14.5px; }
.toc a:hover { color:var(--accent-2); }

section.body { padding:30px 0; }
section.body h2 { font-size:clamp(24px,2.8vw,34px); margin:48px 0 18px; letter-spacing:-0.025em; scroll-margin-top:80px; }
section.body p, section.body ul, section.body ol { font-size:16.5px; color:var(--ink); line-height:1.78; margin-bottom:18px; }
section.body ul, section.body ol { padding-left:24px; }
section.body li { margin-bottom:8px; }
section.body a { color:var(--accent-2); text-decoration:underline; text-decoration-color:rgba(255,176,152,0.3); text-underline-offset:3px; }
section.body a:hover { text-decoration-color:var(--accent-2); }
section.body b, section.body strong { color:var(--ink); font-weight:600; }

.faq-section { padding:80px 0; background:var(--bg-2); border-top:1px solid var(--line); border-bottom:1px solid var(--line); }
.faq-list { max-width:820px; margin:24px auto 0; }
.faq-item { padding:24px 28px; border:1px solid var(--line); border-radius:14px; margin-bottom:14px; background:var(--bg-3); }
.faq-item h4 { font-size:18px; margin-bottom:10px; }
.faq-item p { color:var(--ink-2); font-size:15.5px; line-height:1.7; }
.faq-item a { color:var(--accent-2); text-decoration:underline; }

.cta-strip { padding:48px; background:linear-gradient(135deg, #ff5e1f, #c2400d); border-radius:20px; text-align:center; margin:60px auto; max-width:900px; }
.cta-strip h3 { font-size:28px; margin-bottom:10px; color:#fff; }
.cta-strip p { color:rgba(255,255,255,0.92); margin-bottom:24px; font-size:16px; }
.cta-strip .btn { background:#0a0a0c; }

/* Glossary */
.glossary-grid { display:grid; gap:14px; max-width:920px; margin:0 auto; }
.gloss { padding:20px 26px; background:var(--bg-2); border:1px solid var(--line); border-radius:14px; }
.gloss dt { font-family:'Space Grotesk'; font-weight:600; font-size:18px; color:var(--ink); margin-bottom:6px; }
.gloss dd { color:var(--ink-2); font-size:15px; line-height:1.7; }
.gloss dd a { color:var(--accent-2); text-decoration:underline; }
.alpha-nav { position:sticky; top:78px; background:rgba(8,8,10,0.85); backdrop-filter:blur(12px); padding:14px 0; border-bottom:1px solid var(--line); margin-bottom:32px; z-index:30; }
.alpha-nav .row { display:flex; flex-wrap:wrap; gap:6px; justify-content:center; }
.alpha-nav a { padding:4px 10px; color:var(--ink-2); font-family:'Space Grotesk'; font-weight:600; font-size:13px; border-radius:6px; transition:background .15s, color .15s; }
.alpha-nav a:hover { background:var(--bg-3); color:var(--ink); }
.alpha-letter { font-family:'Space Grotesk'; color:var(--accent); font-size:24px; font-weight:700; margin:32px 0 14px; padding-top:8px; }
.alpha-letter:first-of-type { margin-top:0; }

/* Calculator */
.calc-grid { display:grid; grid-template-columns:1.3fr 1fr; gap:32px; max-width:1080px; margin:0 auto; }
.calc-form { background:var(--bg-2); border:1px solid var(--line); border-radius:18px; padding:32px; }
.calc-out  { background:linear-gradient(180deg, var(--bg-3) 0%, var(--bg-2) 100%); border:1px solid var(--line-2); border-radius:18px; padding:32px; }
.calc-field { margin-bottom:22px; }
.calc-field label { display:block; font-size:13px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.1em; font-weight:600; margin-bottom:8px; font-family:'Space Grotesk'; }
.calc-field select, .calc-field input { width:100%; padding:14px 16px; background:var(--bg-3); border:1px solid var(--line-2); border-radius:10px; color:var(--ink); font-size:15px; font-family:'Inter'; }
.calc-field select:focus, .calc-field input:focus { outline:2px solid var(--accent); border-color:transparent; }
.calc-out .vbig { font-family:'Space Grotesk'; font-size:48px; font-weight:600; letter-spacing:-0.025em; color:var(--accent-2); margin-bottom:6px; }
.calc-out .vsub { color:var(--ink-3); font-size:14px; margin-bottom:24px; }
.calc-out .vrow { display:flex; justify-content:space-between; align-items:center; padding:12px 0; border-bottom:1px solid var(--line); font-size:14.5px; }
.calc-out .vrow:last-child { border-bottom:none; }
.calc-out .vrow .k { color:var(--ink-2); }
.calc-out .vrow .v { font-family:'Space Grotesk'; font-weight:600; color:var(--ink); }
.calc-summary { margin-top:24px; padding:18px; background:rgba(255,94,31,0.08); border:1px solid rgba(255,94,31,0.25); border-radius:12px; color:var(--ink); font-size:14.5px; line-height:1.6; }
@media (max-width:880px) { .calc-grid { grid-template-columns:1fr; } }

/* Comparison */
.cmp-grid { display:grid; gap:18px; max-width:1080px; margin:32px auto; }
.cmp-card { display:grid; grid-template-columns:auto 1fr auto; gap:24px; align-items:center; padding:24px 28px; background:var(--bg-2); border:1px solid var(--line); border-radius:14px; transition:border-color .2s, transform .2s; }
.cmp-card:hover { border-color:var(--line-2); transform:translateY(-2px); }
.cmp-card img { width:72px; height:72px; object-fit:contain; }
.cmp-card .cmp-title { font-family:'Space Grotesk'; font-weight:600; font-size:19px; margin-bottom:4px; }
.cmp-card .cmp-sub { color:var(--ink-3); font-size:13px; }
.cmp-card .cmp-arr { color:var(--accent-2); font-weight:600; }

.h2h-grid { display:grid; grid-template-columns:1fr 1fr; gap:24px; max-width:1080px; margin:40px auto; }
.h2h-card { background:var(--bg-2); border:1px solid var(--line); border-radius:18px; padding:32px; }
.h2h-card .vendor { font-size:11px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.14em; font-weight:600; margin-bottom:6px; }
.h2h-card h3 { font-size:24px; margin-bottom:10px; }
.h2h-card .photo-wrap { aspect-ratio:1; background:linear-gradient(180deg, var(--bg-3) 0%, var(--bg-2) 100%); border:1px solid var(--line); border-radius:12px; display:flex; align-items:center; justify-content:center; margin:18px 0; padding:18px; position:relative; overflow:hidden; }
.h2h-card .photo-wrap::before { content:""; position:absolute; inset:0; background:radial-gradient(45% 35% at 50% 50%, rgba(255,94,31,0.15), transparent 70%); }
.h2h-card .photo-wrap img { max-height:88%; max-width:88%; width:auto; height:auto; object-fit:contain; position:relative; z-index:2; filter:drop-shadow(0 12px 24px rgba(0,0,0,0.5)); }
.h2h-card .price { font-family:'Space Grotesk'; font-size:32px; font-weight:600; color:var(--accent-2); margin-bottom:14px; }
.h2h-card .specs { display:grid; grid-template-columns:repeat(2,1fr); gap:10px; margin-bottom:18px; }
.h2h-card .specs div { padding:8px 12px; background:var(--bg-3); border:1px solid var(--line); border-radius:8px; font-size:12.5px; }
.h2h-card .specs div b { display:block; color:var(--ink); font-family:'Space Grotesk'; font-size:14px; }
.h2h-card .specs div span { color:var(--ink-3); font-size:11px; text-transform:uppercase; letter-spacing:0.06em; }
.h2h-card ul { padding-left:18px; margin-bottom:18px; }
.h2h-card li { color:var(--ink-2); font-size:14px; margin-bottom:6px; line-height:1.55; }
.h2h-vs { text-align:center; color:var(--ink-3); font-family:'Space Grotesk'; font-size:28px; font-weight:700; padding:8px 0; }
@media (max-width:780px) { .h2h-grid { grid-template-columns:1fr; } .h2h-vs { transform:rotate(90deg); padding:14px 0; } }
"""

NAV_HTML = """
<nav class="top">
  <div class="container row">
    <a href="/" class="brand">
      <div class="brand-mark"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round"><path d="M5 9h14v10H5z"/><circle cx="9" cy="14" r="1.2" fill="white"/><circle cx="15" cy="14" r="1.2" fill="white"/><path d="M12 5v4"/></svg></div>
      BotLease
    </a>
    <div class="nav-links">
      <a href="/robots">Robots</a>
      <a href="/vergelijken">Vergelijken</a>
      <a href="/kosten">Kosten</a>
      <a href="/gids/humanoide-robot-leasen">Gids</a>
      <a href="/nieuws">Nieuws</a>
    </div>
    <a href="/#contact" class="btn">Plan demo →</a>
  </div>
</nav>
"""

FOOTER_HTML = """
<footer>
  <div class="container row">
    <div>© 2026 BotLease B.V. — Eindhoven · KvK XXXXXXXX</div>
    <div><a href="/">Home</a> · <a href="/robots">Robots</a> · <a href="/vergelijken">Vergelijken</a> · <a href="/kosten">Kosten</a> · <a href="/nieuws">Nieuws</a> · <a href="/over">Over</a> · <a href="/sitemap.xml">Sitemap</a></div>
  </div>
</footer>
"""

ORG_SCHEMA = json.dumps({
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "BotLease",
    "url": SITE_URL,
    "logo": f"{SITE_URL}/logo.png",
    "address": {"@type": "PostalAddress", "addressLocality": "Eindhoven", "addressCountry": "NL"},
}, ensure_ascii=False)


def render_guide(g: dict, og_image: str = "/img/robots/apollo.png", how_to: bool = False) -> str:
    """Renders the pillar / AI-Act guide pages."""
    toc = "".join(f'<li><a href="#{s["id"]}">{escape(s["h"])}</a></li>' for s in g["sections"])
    sections_html = []
    for s in g["sections"]:
        body_html = "".join(
            (
                f'<{("ul" if p.startswith("<ul>") else "ol" if p.startswith("<ol>") else "p")}>{p}</{("ul" if p.startswith("<ul>") else "ol" if p.startswith("<ol>") else "p")}>'
                if not (p.startswith("<ul>") or p.startswith("<ol>"))
                else p
            )
            if not p.startswith("<")
            else (f'<p>{p}</p>' if not (p.startswith("<ul>") or p.startswith("<ol>") or p.startswith("<p>")) else p)
            for p in s["body"]
        )
        # Cleaner: simpler logic — wrap raw text in <p>, leave HTML strings as-is
        body_html = ""
        for p in s["body"]:
            if p.startswith("<ul>") or p.startswith("<ol>"):
                body_html += p
            else:
                body_html += f"<p>{p}</p>"
        sections_html.append(f'<h2 id="{s["id"]}">{escape(s["h"])}</h2>{body_html}')
    sections_str = "".join(sections_html)

    tldr_html = ""
    if g.get("tldr"):
        tldr_items = "".join(f"<li>{p}</li>" for p in g["tldr"])
        tldr_html = f'<div class="tldr"><h3>TL;DR</h3><ul>{tldr_items}</ul></div>'

    faq_html = ""
    faq_jsonld = ""
    if g.get("faq"):
        faq_items = "".join(f'<div class="faq-item"><h4>{escape(q)}</h4><p>{a}</p></div>' for q, a in g["faq"])
        faq_html = f'''
<section class="faq-section">
  <div class="narrow">
    <span class="eyebrow">Veelgestelde vragen</span>
    <h2 style="margin-top:14px">Vraag &amp; antwoord.</h2>
    <div class="faq-list">{faq_items}</div>
  </div>
</section>'''
        faq_jsonld = json.dumps({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a.replace("<", "").replace(">", "")}}
                for q, a in g["faq"]
            ],
        }, ensure_ascii=False)

    breadcrumb = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Gids", "item": f"{SITE_URL}/gids/"},
            {"@type": "ListItem", "position": 3, "name": g.get("h1", "")[:60],
             "item": f"{SITE_URL}/gids/{g['slug']}"},
        ],
    }, ensure_ascii=False)

    article_jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "Article",
        "headline": g.get("h1"), "description": g.get("meta_desc"),
        "image": f"{SITE_URL}{og_image}",
        "datePublished": "2026-05-18T08:00:00+02:00",
        "dateModified": "2026-05-18T08:00:00+02:00",
        "author": {"@type": "Organization", "name": "BotLease Redactie"},
        "publisher": {"@type": "Organization", "name": "BotLease",
                      "logo": {"@type": "ImageObject", "url": f"{SITE_URL}/logo.png"}},
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{SITE_URL}/gids/{g['slug']}"},
        "inLanguage": "nl-NL",
    }, ensure_ascii=False)

    speakable_jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "WebPage",
        "speakable": {"@type": "SpeakableSpecification",
                      "cssSelector": [".tldr li", "h1", ".tag"]},
        "url": f"{SITE_URL}/gids/{g['slug']}",
    }, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(g['title'])}</title>
<meta name="description" content="{escape(g['meta_desc'])}">
<meta name="keywords" content="{escape(g['keywords'])}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta name="author" content="BotLease">
<link rel="canonical" href="{SITE_URL}/gids/{g['slug']}">

<meta property="og:type" content="article">
<meta property="og:title" content="{escape(g['title'])}">
<meta property="og:description" content="{escape(g['meta_desc'])}">
<meta property="og:url" content="{SITE_URL}/gids/{g['slug']}">
<meta property="og:image" content="{SITE_URL}{og_image}">
<meta property="og:locale" content="nl_NL">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(g['title'])}">
<meta name="twitter:description" content="{escape(g['meta_desc'])}">
<meta name="twitter:image" content="{SITE_URL}{og_image}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{article_jsonld}</script>
<script type="application/ld+json">{breadcrumb}</script>
{f'<script type="application/ld+json">{faq_jsonld}</script>' if faq_jsonld else ''}
<script type="application/ld+json">{speakable_jsonld}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
</head>
<body>
{NAV_HTML}

<section class="g-hero">
  <div class="narrow">
    <nav class="crumbs">
      <a href="/">Home</a><span class="sep">/</span>
      <a href="/gids/">Gids</a><span class="sep">/</span>
      <span>{escape(g.get('h1','')[:55])}…</span>
    </nav>
    <span class="eyebrow">Gids</span>
    <h1>{escape(g['h1'])}</h1>
    <p class="tag">{escape(g['tagline'])}</p>
    {tldr_html}
    <div class="toc">
      <h3>Inhoud</h3>
      <ol>{toc}</ol>
    </div>
  </div>
</section>

<section class="body">
  <div class="narrow">{sections_str}</div>
</section>

{faq_html}

<section>
  <div class="container">
    <div class="cta-strip">
      <h3>Klaar voor de volgende stap?</h3>
      <p>Plan een gratis intake. Wij komen op locatie en geven onafhankelijk advies.</p>
      <a class="btn" href="/#contact">Plan een demo →</a>
    </div>
  </div>
</section>

{FOOTER_HTML}
</body>
</html>
"""


def render_glossary(g: dict) -> str:
    # Group by first letter
    grouped: dict[str, list] = {}
    for term, body in g["terms"]:
        letter = term[0].upper()
        if letter == "I": letter = "I"  # placeholder for sorting trick — not needed
        grouped.setdefault(letter, []).append((term, body))
    letters_sorted = sorted(grouped.keys())

    alpha_nav = "".join(f'<a href="#letter-{l}">{l}</a>' for l in letters_sorted)
    body_html = ""
    for l in letters_sorted:
        items_html = "".join(
            f'<dl class="gloss" id="term-{escape(t.lower().replace(" ", "-"))}"><dt>{escape(t)}</dt><dd>{b}</dd></dl>'
            for t, b in sorted(grouped[l], key=lambda x: x[0].lower())
        )
        body_html += f'<div class="alpha-letter" id="letter-{l}">{l}</div><div class="glossary-grid">{items_html}</div>'

    breadcrumb = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Begrippen", "item": f"{SITE_URL}/begrippen"},
        ],
    }, ensure_ascii=False)

    defined_terms_jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "DefinedTermSet",
        "name": "BotLease humanoid robot begrippenlijst",
        "description": g["meta_desc"],
        "hasDefinedTerm": [
            {"@type": "DefinedTerm", "name": t,
             "description": b.replace("<", "").replace(">", "")[:300],
             "inDefinedTermSet": f"{SITE_URL}/begrippen"}
            for t, b in g["terms"]
        ],
    }, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(g['title'])}</title>
<meta name="description" content="{escape(g['meta_desc'])}">
<meta name="keywords" content="{escape(g['keywords'])}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/begrippen">
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(g['title'])}">
<meta property="og:description" content="{escape(g['meta_desc'])}">
<meta property="og:url" content="{SITE_URL}/begrippen">
<meta property="og:image" content="{SITE_URL}/img/robots/apollo.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{breadcrumb}</script>
<script type="application/ld+json">{defined_terms_jsonld}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
</head>
<body>
{NAV_HTML}

<section class="g-hero">
  <div class="container">
    <nav class="crumbs">
      <a href="/">Home</a><span class="sep">/</span>
      <span>Begrippen</span>
    </nav>
    <span class="eyebrow">Begrippenlijst</span>
    <h1>{escape(g['h1'])}</h1>
    <p class="tag">{escape(g['tagline'])}</p>
  </div>
</section>

<div class="alpha-nav">
  <div class="container row">{alpha_nav}</div>
</div>

<section class="body">
  <div class="container">{body_html}</div>
</section>

<section>
  <div class="container">
    <div class="cta-strip">
      <h3>Een term mist?</h3>
      <p>Mail ons — wij voegen hem toe en linken hem aan de juiste robotmodellen.</p>
      <a class="btn" href="mailto:hallo@botlease.nl">Stuur een mail →</a>
    </div>
  </div>
</section>

{FOOTER_HTML}
</body>
</html>
"""


def render_simple(g: dict, kind: str = "over") -> str:
    """About / Methodology — no FAQ, simpler layout."""
    sections_html = []
    for s in g["sections"]:
        body_html = ""
        for p in s["body"]:
            if p.startswith("<ul>") or p.startswith("<ol>"):
                body_html += p
            else:
                body_html += f"<p>{p}</p>"
        sections_html.append(f'<h2 id="{s["id"]}">{escape(s["h"])}</h2>{body_html}')

    breadcrumb = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Over" if kind == "over" else "Methodologie",
             "item": f"{SITE_URL}/{g['slug']}"},
        ],
    }, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(g['title'])}</title>
<meta name="description" content="{escape(g['meta_desc'])}">
<meta name="keywords" content="{escape(g['keywords'])}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/{g['slug']}">
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(g['title'])}">
<meta property="og:description" content="{escape(g['meta_desc'])}">
<meta property="og:url" content="{SITE_URL}/{g['slug']}">
<meta property="og:image" content="{SITE_URL}/img/robots/apollo.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{breadcrumb}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
</head>
<body>
{NAV_HTML}

<section class="g-hero">
  <div class="narrow">
    <nav class="crumbs">
      <a href="/">Home</a><span class="sep">/</span>
      <span>{'Over' if kind == 'over' else 'Methodologie'}</span>
    </nav>
    <span class="eyebrow">{'Over' if kind == 'over' else 'Methodologie'}</span>
    <h1>{escape(g['h1'])}</h1>
    <p class="tag">{escape(g['tagline'])}</p>
  </div>
</section>

<section class="body">
  <div class="narrow">{''.join(sections_html)}</div>
</section>

<section>
  <div class="container">
    <div class="cta-strip">
      <h3>Plan een gesprek.</h3>
      <p>Gratis intake op locatie binnen 5 werkdagen.</p>
      <a class="btn" href="/#contact">Contact →</a>
    </div>
  </div>
</section>

{FOOTER_HTML}
</body>
</html>
"""


def render_costs(g: dict) -> str:
    """Interactive lease cost calculator."""
    # Robot options for dropdown
    options = "".join(
        f'<option value="{r["slug"]}" data-purchase="{r["purchase_eur"]}" data-lease="{r["lease_eur"]}" '
        f'data-setup="{r["setup_eur"]}" data-name="{escape(r["name"])}">'
        f'{escape(r["name"])} — €{r["lease_eur"]:,}/mnd</option>'.replace(",", ".")
        for r in ROBOTS
    )

    breadcrumb = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Kosten", "item": f"{SITE_URL}/kosten"},
        ],
    }, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(g['title'])}</title>
<meta name="description" content="{escape(g['meta_desc'])}">
<meta name="keywords" content="{escape(g['keywords'])}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/kosten">
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(g['title'])}">
<meta property="og:description" content="{escape(g['meta_desc'])}">
<meta property="og:url" content="{SITE_URL}/kosten">
<meta property="og:image" content="{SITE_URL}/img/robots/apollo.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{breadcrumb}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
</head>
<body>
{NAV_HTML}

<section class="g-hero">
  <div class="container">
    <nav class="crumbs"><a href="/">Home</a><span class="sep">/</span><span>Kosten</span></nav>
    <span class="eyebrow">Lease-prijs calculator</span>
    <h1>{escape(g['h1'])}</h1>
    <p class="tag">{escape(g['tagline'])}</p>
  </div>
</section>

<section class="body">
  <div class="container">
    <div class="calc-grid">
      <div class="calc-form">
        <div class="calc-field">
          <label for="model">Robot model</label>
          <select id="model">
            {options}
          </select>
        </div>
        <div class="calc-field">
          <label for="duration">Contractduur</label>
          <select id="duration">
            <option value="36" data-mod="1.0">36 maanden (standaard)</option>
            <option value="24" data-mod="1.07">24 maanden (+7%)</option>
            <option value="12" data-mod="1.15">12 maanden (+15%)</option>
          </select>
        </div>
        <div class="calc-field">
          <label for="units">Aantal units</label>
          <input id="units" type="number" min="1" max="50" value="1">
        </div>
        <div class="calc-field">
          <label for="hours">Inzet per week (uren)</label>
          <input id="hours" type="number" min="1" max="168" value="40">
        </div>
        <div class="calc-field">
          <label for="loon">Vermeden loonkost per uur (€)</label>
          <input id="loon" type="number" min="0" max="200" value="28">
        </div>
        <p style="font-size:13px; color:var(--ink-3); margin-top:18px">Volume-korting: 3+ units −8%, 10+ units −15%. BTW excl.</p>
      </div>
      <div class="calc-out">
        <div class="vbig" id="out-monthly">€890</div>
        <div class="vsub">per maand, all-in lease (excl. BTW)</div>

        <div class="vrow"><span class="k">Eenmalige setup</span><span class="v" id="out-setup">€2.500</span></div>
        <div class="vrow"><span class="k">Totaal contractwaarde</span><span class="v" id="out-total">€34.040</span></div>
        <div class="vrow"><span class="k">Aanschafprijs (publiek)</span><span class="v" id="out-purchase">€19.999</span></div>
        <div class="vrow"><span class="k">Vermeden loonkosten/jr</span><span class="v" id="out-savings">€58.240</span></div>
        <div class="vrow"><span class="k">Geschatte ROI-periode</span><span class="v" id="out-roi">6,9 mnd</span></div>

        <div class="calc-summary" id="out-summary">
          Selecteer een model om de berekening te starten.
        </div>
      </div>
    </div>

    <div style="max-width:840px; margin:60px auto 0">
      <h2 style="margin-bottom:16px">Wat zit er in de leaseprijs?</h2>
      <ul style="font-size:16.5px; line-height:1.75; color:var(--ink); padding-left:22px">
        <li><b>Robot zelf</b> — afschrijving over 36 maanden gedragen door BotLease.</li>
        <li><b>Installatie</b> + 2-uurs operatortraining (apart in setup-fee).</li>
        <li><b>Preventief + correctief onderhoud</b> — wij komen langs als er iets is.</li>
        <li><b>Onderdelen</b> — alle reserveonderdelen inbegrepen.</li>
        <li><b>Swap-SLA</b> — vervangende unit binnen 24u op locatie (anders €100/dag vergoeding).</li>
        <li><b>Verzekering</b> — WA tot €2,5M + casco.</li>
        <li><b>24/7 helpdesk</b> — Nederlands sprekende engineers.</li>
        <li><b>Software-updates</b> + remote tuning + AI-Act compliance maintenance.</li>
      </ul>
      <h2 style="margin-top:48px; margin-bottom:16px">Wat zit er NIET in?</h2>
      <ul style="font-size:16.5px; line-height:1.75; color:var(--ink); padding-left:22px">
        <li><b>Pilot:</b> €1.500 voor 4 weken (terug bij doorgaan met lease).</li>
        <li><b>Elektriciteit op locatie:</b> ~€30/maand per robot.</li>
        <li><b>Custom integraties &gt;40 uur:</b> €95/uur.</li>
        <li><b>Schade door verkeerd gebruik</b> (buiten werkzone, opzettelijk).</li>
      </ul>

      <h2 style="margin-top:48px; margin-bottom:16px">Hoe deze berekening werkt</h2>
      <p>De leaseprijs is gebaseerd op aanschafprijs / 36 maanden + 25% service-reserve + 8% verzekering + 30% marge. Voor specifieke modellen ronden we naar beneden af. ROI-periode is een schatting op basis van: (totaal contract / jaarlijkse besparing) × 12. Echte ROI hangt af van je situatie — laat ons een individuele case-study maken in de gratis intake.</p>
      <p>Zie ook: <a href="/methodologie#prijsformule">complete prijsmethodologie</a> · <a href="/gids/humanoide-robot-leasen#kosten">de kosten-sectie van de pillar guide</a></p>
    </div>
  </div>
</section>

{FOOTER_HTML}

<script>
(function(){{
  var model    = document.getElementById('model');
  var duration = document.getElementById('duration');
  var units    = document.getElementById('units');
  var hours    = document.getElementById('hours');
  var loon     = document.getElementById('loon');

  function eu(n){{ return '€' + Math.round(n).toLocaleString('nl-NL'); }}

  function calc(){{
    var sel       = model.options[model.selectedIndex];
    var purchase  = parseFloat(sel.dataset.purchase) || 0;
    var baseLease = parseFloat(sel.dataset.lease)    || 0;
    var setupFee  = parseFloat(sel.dataset.setup)    || 0;
    var name      = sel.dataset.name || '';

    var durSel = duration.options[duration.selectedIndex];
    var durMod = parseFloat(durSel.dataset.mod) || 1;
    var months = parseInt(durSel.value) || 36;

    var u = Math.max(1, parseInt(units.value) || 1);
    var volMod = u >= 10 ? 0.85 : u >= 3 ? 0.92 : 1.0;

    var lease   = baseLease * durMod * volMod;
    var setupT  = setupFee * u;
    var total   = lease * months * u + setupT;

    var h       = parseFloat(hours.value) || 0;
    var l       = parseFloat(loon.value)  || 0;
    var saveYr  = h * 52 * l * u;
    var roiMo   = saveYr > 0 ? (total / saveYr) * 12 : 0;

    document.getElementById('out-monthly').textContent  = eu(lease * u);
    document.getElementById('out-setup').textContent    = eu(setupT);
    document.getElementById('out-total').textContent    = eu(total);
    document.getElementById('out-purchase').textContent = eu(purchase * u);
    document.getElementById('out-savings').textContent  = eu(saveYr);
    document.getElementById('out-roi').textContent      = roiMo > 0 ? roiMo.toFixed(1) + ' mnd' : '—';

    var lockIn = months === 36 ? 'standaard contract' : months + '-maands contract (+' + Math.round((durMod-1)*100) + '%)';
    var volTxt = u >= 10 ? ' inclusief 15% volume-korting' : u >= 3 ? ' inclusief 8% volume-korting' : '';
    var summary = '<b>' + name + '</b> × ' + u + ' unit' + (u>1?'s':'') + ' op een ' + lockIn + volTxt + '. ';
    summary += 'Bij ' + h + ' uur inzet per week × €' + l + '/uur loonkost: ROI rond <b>' + (roiMo>0?roiMo.toFixed(1):'n.v.t.') + ' maanden</b>.';
    document.getElementById('out-summary').innerHTML = summary;
  }}

  [model, duration, units, hours, loon].forEach(function(el){{
    el.addEventListener('input', calc);
    el.addEventListener('change', calc);
  }});
  calc();
}})();
</script>
</body>
</html>
"""


def render_comparison_hub() -> str:
    """The /vergelijken hub — sortable table of all robots."""
    cards = "".join(
        f"""<a href="/robots/{r['slug']}" class="cmp-card">
          <img src="{r['photo']}" alt="{escape(r['name'])} robot foto">
          <div>
            <div class="cmp-title">{escape(r['name'])}</div>
            <div class="cmp-sub">{escape(r['vendor'])} · {escape(r['vendor_country'])} · {r['height_cm']} cm · {r['payload_kg']} kg payload</div>
          </div>
          <div style="text-align:right">
            <div class="cmp-arr">€{r['lease_eur']:,}/mnd</div>
            <div style="font-size:11px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.1em; margin-top:2px">{escape(r['category'])}</div>
          </div>
        </a>""".replace(",", ".") for r in ROBOTS
    )

    breadcrumb = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Vergelijken", "item": f"{SITE_URL}/vergelijken"},
        ],
    }, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Humanoïde robots vergelijken — 15 modellen naast elkaar | BotLease</title>
<meta name="description" content="Vergelijk alle 15 humanoïde robots leverbaar in Nederland: NEURA 4NE-1, Unitree G1, PAL Kangaroo, Apptronik Apollo, Figure 02. Specificaties, prijzen, use-cases naast elkaar.">
<meta name="keywords" content="humanoide robots vergelijken, robot vergelijking, beste humanoid robot Nederland, vergelijk humanoid lease">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/vergelijken">
<meta property="og:type" content="website">
<meta property="og:title" content="Humanoïde robots vergelijken | BotLease">
<meta property="og:description" content="15 modellen naast elkaar — specs, prijs, use-case.">
<meta property="og:url" content="{SITE_URL}/vergelijken">
<meta property="og:image" content="{SITE_URL}/img/robots/apollo.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{breadcrumb}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
</head>
<body>
{NAV_HTML}

<section class="g-hero">
  <div class="container">
    <nav class="crumbs"><a href="/">Home</a><span class="sep">/</span><span>Vergelijken</span></nav>
    <span class="eyebrow">Vergelijken</span>
    <h1>Vergelijk 15 humanoïde robots in Nederland.</h1>
    <p class="tag">Specs, prijs, use-case, leverbaarheid — naast elkaar. Klik een robot voor de detailpagina, of bekijk onze populaire head-to-head vergelijkingen onderaan.</p>
  </div>
</section>

<section class="body">
  <div class="container">
    <h2 style="font-size:22px; margin-bottom:18px">Alle modellen, gesorteerd op leverbaarheid + prijs</h2>
    <div class="cmp-grid">{cards}</div>
  </div>
</section>

<section style="background:var(--bg-2); border-top:1px solid var(--line); border-bottom:1px solid var(--line); padding:60px 0">
  <div class="container">
    <span class="eyebrow">Populaire head-to-heads</span>
    <h2 style="margin:14px 0 28px">Direct vergelijken — top 6 vergelijkingen.</h2>
    <div class="cmp-grid">
      <a href="/vergelijken/unitree-g1-vs-neura-4ne1-mini" class="cmp-card"><div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px; font-family:'Space Grotesk'; font-weight:700; font-size:13px; color:var(--ink-2)">G1 vs M</div><div><div class="cmp-title">Unitree G1 vs NEURA 4NE-1 Mini</div><div class="cmp-sub">Bestseller vs EU-instap · €899 vs €890 per maand</div></div><div class="cmp-arr">Vergelijk →</div></a>
      <a href="/vergelijken/unitree-h1-2-vs-ubtech-walker-s2" class="cmp-card"><div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px; font-family:'Space Grotesk'; font-weight:700; font-size:13px; color:var(--ink-2)">H1 vs W2</div><div><div class="cmp-title">Unitree H1-2 vs UBTECH Walker S2</div><div class="cmp-sub">Industrieel value vs auto-industrie · €3.990 vs €3.290</div></div><div class="cmp-arr">Vergelijk →</div></a>
      <a href="/vergelijken/neura-4ne1-gen3-vs-apptronik-apollo" class="cmp-card"><div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px; font-family:'Space Grotesk'; font-weight:700; font-size:13px; color:var(--ink-2)">EU vs US</div><div><div class="cmp-title">NEURA 4NE-1 Gen 3.5 vs Apptronik Apollo</div><div class="cmp-sub">EU-flagship vs US-wachtlijst · €4.490 vs €3.499</div></div><div class="cmp-arr">Vergelijk →</div></a>
      <a href="/vergelijken/pal-kangaroo-vs-unitree-h1-2" class="cmp-card"><div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px; font-family:'Space Grotesk'; font-weight:700; font-size:13px; color:var(--ink-2)">ES vs CN</div><div><div class="cmp-title">PAL Kangaroo vs Unitree H1-2</div><div class="cmp-sub">EU-veteraan vs CN-value · €3.490 vs €3.990</div></div><div class="cmp-arr">Vergelijk →</div></a>
      <a href="/vergelijken/unitree-r1-vs-engineai-se01" class="cmp-card"><div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px; font-family:'Space Grotesk'; font-weight:700; font-size:13px; color:var(--ink-2)">R1 vs SE</div><div><div class="cmp-title">Unitree R1 vs EngineAI SE01</div><div class="cmp-sub">Instap demo vs natural gait · €290 vs €1.290</div></div><div class="cmp-arr">Vergelijk →</div></a>
      <a href="/vergelijken/apptronik-apollo-vs-figure-02" class="cmp-card"><div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px; font-family:'Space Grotesk'; font-weight:700; font-size:13px; color:var(--ink-2)">Apollo vs F2</div><div><div class="cmp-title">Apptronik Apollo vs Figure 02</div><div class="cmp-sub">Mercedes-pilot vs BMW-pilot · €3.499 vs €3.899</div></div><div class="cmp-arr">Vergelijk →</div></a>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="cta-strip">
      <h3>Niet zeker welk model past?</h3>
      <p>Plan een gratis intake. Wij adviseren onafhankelijk welk model bij jouw use-case past.</p>
      <a class="btn" href="/#contact">Plan een demo →</a>
    </div>
  </div>
</section>

{FOOTER_HTML}
</body>
</html>
"""


def render_h2h(slug_a: str, slug_b: str) -> str:
    a = by_slug(slug_a)
    b = by_slug(slug_b)
    if not a or not b:
        return ""

    def card(r, side):
        photo_url = r["photo"]
        return f"""<div class="h2h-card">
          <div class="vendor">{escape(r['vendor'])} · {escape(r['vendor_country'])}</div>
          <h3>{escape(r['name'])}</h3>
          <div class="photo-wrap"><img src="{photo_url}" alt="{escape(r['name'])} robot foto" loading="lazy"></div>
          <div class="price">€{r['lease_eur']:,}/mnd</div>
          <div class="specs">
            <div><b>{r['height_cm']} cm</b><span>Hoogte</span></div>
            <div><b>{r['payload_kg']} kg</b><span>Payload</span></div>
            <div><b>{r['battery_hours']} u</b><span>Batterij</span></div>
            <div><b>{r['speed_ms']} m/s</b><span>Snelheid</span></div>
            <div><b>{r['dof']}</b><span>DoF</span></div>
            <div><b>€{r['purchase_eur']:,}</b><span>Aanschafprijs</span></div>
          </div>
          <p style="color:var(--ink-2); font-size:14.5px; line-height:1.65; margin-bottom:14px">{escape(r['short'])}</p>
          <a class="btn ghost" href="/robots/{r['slug']}">Bekijk detail →</a>
        </div>""".replace(",", ".")

    h1 = f"{a['name']} vs {b['name']} — vergelijking 2026"
    title = f"{h1} | BotLease"
    meta_desc = f"Side-by-side vergelijking {a['name']} vs {b['name']}: specs, prijs, use-case, leverbaarheid. €{a['lease_eur']:,}/mnd vs €{b['lease_eur']:,}/mnd. Welke past bij jouw situatie?".replace(",", ".")
    slug = f"{slug_a}-vs-{slug_b}"
    breadcrumb = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Vergelijken", "item": f"{SITE_URL}/vergelijken"},
            {"@type": "ListItem", "position": 3, "name": f"{a['name']} vs {b['name']}", "item": f"{SITE_URL}/vergelijken/{slug}"},
        ],
    }, ensure_ascii=False)

    # Comparison verdict
    if a["tier"] == "eu" and b["tier"] != "eu":
        verdict = f"<b>{a['name']}</b> wint op EU-compliance en supply chain (gebouwd in {a['vendor_country']}). <b>{b['name']}</b> wint op prijs of capaciteit voor specifieke use-cases. Voor compliance-gevoelige sectoren (zorg, government, financieel): kies de {a['name']}."
    elif b["tier"] == "eu" and a["tier"] != "eu":
        verdict = f"<b>{b['name']}</b> wint op EU-compliance en supply chain (gebouwd in {b['vendor_country']}). <b>{a['name']}</b> wint op prijs of capaciteit voor specifieke use-cases. Voor compliance-gevoelige sectoren (zorg, government, financieel): kies de {b['name']}."
    elif a["category"] == "waitlist" and b["category"] == "available":
        verdict = f"<b>{b['name']}</b> wint op leverbaarheid (direct bestelbaar). <b>{a['name']}</b> staat op de wachtlijst voor 2027 — alleen reserveren mogelijk. Voor productieve inzet 2026: kies de {b['name']}."
    elif b["category"] == "waitlist" and a["category"] == "available":
        verdict = f"<b>{a['name']}</b> wint op leverbaarheid (direct bestelbaar). <b>{b['name']}</b> staat op de wachtlijst voor 2027. Voor productieve inzet 2026: kies de {a['name']}."
    elif a["lease_eur"] < b["lease_eur"] * 0.7:
        verdict = f"<b>{a['name']}</b> is significant goedkoper (€{a['lease_eur']:,}/mnd vs €{b['lease_eur']:,}/mnd). <b>{b['name']}</b> heeft hogere payload en is geschikter voor heavy-duty taken. Voor lichte use-cases (demo, R&D, lichte service): {a['name']}. Voor industrieel: {b['name']}.".replace(",", ".")
    elif b["lease_eur"] < a["lease_eur"] * 0.7:
        verdict = f"<b>{b['name']}</b> is significant goedkoper (€{b['lease_eur']:,}/mnd vs €{a['lease_eur']:,}/mnd). <b>{a['name']}</b> heeft hogere payload en is geschikter voor heavy-duty taken. Voor lichte use-cases: {b['name']}. Voor industrieel: {a['name']}.".replace(",", ".")
    else:
        verdict = f"Beide modellen zitten in dezelfde prijsklasse. Het verschil zit in de details: <b>{a['name']}</b> is sterk voor {', '.join(a['tags'][:2]).lower()}, <b>{b['name']}</b> voor {', '.join(b['tags'][:2]).lower()}. Plan een intake voor specifiek advies."

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)}</title>
<meta name="description" content="{escape(meta_desc)}">
<meta name="keywords" content="{escape(a['name'])} vs {escape(b['name'])}, vergelijk humanoid robot, {escape(a['name'])} of {escape(b['name'])}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/vergelijken/{slug}">
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(h1)}">
<meta property="og:description" content="{escape(meta_desc)}">
<meta property="og:url" content="{SITE_URL}/vergelijken/{slug}">
<meta property="og:image" content="{SITE_URL}{a['photo']}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{breadcrumb}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
</head>
<body>
{NAV_HTML}

<section class="g-hero">
  <div class="container">
    <nav class="crumbs"><a href="/">Home</a><span class="sep">/</span><a href="/vergelijken">Vergelijken</a><span class="sep">/</span><span>{escape(a['name'])} vs {escape(b['name'])}</span></nav>
    <span class="eyebrow">Head-to-head</span>
    <h1>{escape(h1)}.</h1>
    <p class="tag">€{a['lease_eur']:,}/mnd vs €{b['lease_eur']:,}/mnd · {a['vendor_country']} vs {b['vendor_country']} — een eerlijke side-by-side voor MKB-ondernemers.</p>
  </div>
</section>

<section class="body">
  <div class="container">
    <div class="h2h-grid">
      {card(a, 'left')}
      {card(b, 'right')}
    </div>

    <div style="max-width:840px; margin:40px auto">
      <h2>Onze verdict</h2>
      <p style="font-size:17px; line-height:1.75; color:var(--ink)">{verdict}</p>

      <h2 style="margin-top:36px">Wanneer kies je {escape(a['name'])}?</h2>
      <ul>
        {''.join(f'<li>{escape(uc)}</li>' for uc in a['use_cases'][:3])}
      </ul>

      <h2 style="margin-top:36px">Wanneer kies je {escape(b['name'])}?</h2>
      <ul>
        {''.join(f'<li>{escape(uc)}</li>' for uc in b['use_cases'][:3])}
      </ul>

      <h2 style="margin-top:36px">Bekijk de detailpagina's</h2>
      <p><a href="/robots/{a['slug']}">Volledige specs en use-cases voor de {escape(a['name'])}</a> · <a href="/robots/{b['slug']}">Volledige specs en use-cases voor de {escape(b['name'])}</a></p>
    </div>

    <div class="cta-strip">
      <h3>Niet zeker welke past?</h3>
      <p>Plan een gratis intake — wij adviseren onafhankelijk welke past bij jouw use-case.</p>
      <a class="btn" href="/#contact">Plan een demo →</a>
    </div>
  </div>
</section>

{FOOTER_HTML}
</body>
</html>
""".replace(",", ".")


def render_gids_hub() -> str:
    """The /gids/ index — links to pillar + AI-Act guides."""
    breadcrumb = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Gids", "item": f"{SITE_URL}/gids/"},
        ],
    }, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="nl"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Humanoïde robot leasing — gidsen en bronnen | BotLease</title>
<meta name="description" content="Complete gidsen voor humanoïde robot leasing in Nederland: pillar guide, EU AI-Act compliance, lease calculator, methodologie.">
<link rel="canonical" href="{SITE_URL}/gids/">
<meta property="og:type" content="website">
<meta property="og:title" content="BotLease gidsen — humanoïde robot leasing">
<meta property="og:image" content="{SITE_URL}/img/robots/apollo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{breadcrumb}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
</head><body>
{NAV_HTML}
<section class="g-hero"><div class="container">
  <nav class="crumbs"><a href="/">Home</a><span class="sep">/</span><span>Gids</span></nav>
  <span class="eyebrow">Gidsen</span>
  <h1>Alles wat je moet weten over humanoïde robot leasing.</h1>
  <p class="tag">Long-form gidsen, calculator, vergelijkingen en glossary — voor wie verder wil dan een marketingbrochure.</p>
</div></section>
<section class="body"><div class="container">
  <div class="cmp-grid">
    <a href="/gids/humanoide-robot-leasen" class="cmp-card">
      <div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ffb098" stroke-width="2"><path d="M4 4h16v4H4z"/><path d="M4 10h10v10H4z"/><path d="M16 12h4v8h-4z"/></svg></div>
      <div><div class="cmp-title">Pillar guide: humanoïde robot leasen</div><div class="cmp-sub">3.000 woorden — modellen, kosten, ROI, EU compliance, pilot-proces</div></div>
      <div class="cmp-arr">Lees →</div></a>
    <a href="/gids/ai-act-machineverordening" class="cmp-card">
      <div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ffb098" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 6v6l4 2"/></svg></div>
      <div><div class="cmp-title">EU AI-Act + Machineverordening gids</div><div class="cmp-sub">2.500 woorden — compliance vanaf 2 augustus 2026 + 20 januari 2027</div></div>
      <div class="cmp-arr">Lees →</div></a>
    <a href="/kosten" class="cmp-card">
      <div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ffb098" stroke-width="2"><path d="M6 4h12v16H6z"/><path d="M9 8h6"/><path d="M9 12h6"/><path d="M9 16h3"/></svg></div>
      <div><div class="cmp-title">Lease cost calculator</div><div class="cmp-sub">Interactieve berekening — leaseprijs, ROI, vergelijking koop vs lease</div></div>
      <div class="cmp-arr">Bereken →</div></a>
    <a href="/begrippen" class="cmp-card">
      <div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ffb098" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h10"/></svg></div>
      <div><div class="cmp-title">Begrippenlijst</div><div class="cmp-sub">40+ termen uitgelegd — AGV, cobot, SLAM, VLA, EU AI-Act</div></div>
      <div class="cmp-arr">Bekijk →</div></a>
    <a href="/methodologie" class="cmp-card">
      <div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ffb098" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 1v6m0 10v6m11-11h-6M7 12H1"/></svg></div>
      <div><div class="cmp-title">Methodologie</div><div class="cmp-sub">Hoe wij robots evalueren, prijzen berekenen, risico's dragen</div></div>
      <div class="cmp-arr">Lees →</div></a>
    <a href="/over" class="cmp-card">
      <div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ffb098" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 20a8 8 0 0116 0"/></svg></div>
      <div><div class="cmp-title">Over BotLease</div><div class="cmp-sub">Missie, team, waarom we bestaan</div></div>
      <div class="cmp-arr">Lees →</div></a>
  </div>
</div></section>
{FOOTER_HTML}
</body></html>
"""


def build():
    gids = FRONTEND / "gids"
    vergelijken = FRONTEND / "vergelijken"
    gids.mkdir(parents=True, exist_ok=True)
    vergelijken.mkdir(parents=True, exist_ok=True)

    (gids / "humanoide-robot-leasen.html").write_text(render_guide(PILLAR_GUIDE), encoding="utf-8")
    (gids / "ai-act-machineverordening.html").write_text(render_guide(AI_ACT_GUIDE), encoding="utf-8")
    (gids / "index.html").write_text(render_gids_hub(), encoding="utf-8")
    (FRONTEND / "begrippen.html").write_text(render_glossary(GLOSSARY), encoding="utf-8")
    (FRONTEND / "over.html").write_text(render_simple(ABOUT, "over"), encoding="utf-8")
    (FRONTEND / "methodologie.html").write_text(render_simple(METHODOLOGY, "methodologie"), encoding="utf-8")
    (FRONTEND / "kosten.html").write_text(render_costs(COSTS_PAGE), encoding="utf-8")
    (vergelijken / "index.html").write_text(render_comparison_hub(), encoding="utf-8")

    # 6 head-to-head pages
    head_to_heads = [
        ("unitree-g1", "neura-4ne1-mini"),
        ("unitree-h1-2", "ubtech-walker-s2"),
        ("neura-4ne1-gen3", "apptronik-apollo"),
        ("pal-kangaroo", "unitree-h1-2"),
        ("unitree-r1", "engineai-se01"),
        ("apptronik-apollo", "figure-02"),
    ]
    for a, b in head_to_heads:
        html = render_h2h(a, b)
        if html:
            (vergelijken / f"{a}-vs-{b}.html").write_text(html, encoding="utf-8")

    print(f"✅ Built guides: pillar, AI-Act, glossary, about, methodology, costs, /gids/ hub, /vergelijken/ hub + {len(head_to_heads)} head-to-head pages")


if __name__ == "__main__":
    build()
