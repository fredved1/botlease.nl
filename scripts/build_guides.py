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
import re
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
from seo_common import HEAD_SEO, trim_desc  # noqa: E402
from style_base import BASE_CSS, NAV_HTML, FOOTER_HTML  # noqa: E402

PAGE_CSS = BASE_CSS + """
.g-hero { padding:80px 0 30px; }
@media (min-width:768px) { .g-hero { padding:110px 0 40px; } }
.g-hero h1 {
  font-family:'Inter', -apple-system, sans-serif; font-weight:700;
  font-size:clamp(34px, 4.6vw, 56px);
  margin-bottom:18px; letter-spacing:-0.035em; line-height:1.06;
}
.g-hero .tag { color:var(--accent); font-size:18px; margin-bottom:24px; max-width:760px; line-height:1.5; }

.tldr {
  background:var(--accent-soft); border:1px solid var(--accent-line);
  border-radius:18px; padding:32px 36px; margin:40px 0;
}
.tldr h3 { font-size:12.5px; color:var(--accent-deep); text-transform:uppercase; letter-spacing:0.12em; margin-bottom:18px; font-weight:600; font-family:'Inter'; }
.tldr ul { list-style:none; padding:0; }
.tldr li {
  padding:12px 0 12px 28px; position:relative;
  color:var(--ink); font-size:16px; line-height:1.65;
  border-bottom:1px solid var(--accent-line);
}
.tldr li:last-child { border-bottom:none; }
.tldr li::before { content:"→"; position:absolute; left:0; top:11px; color:var(--accent); font-weight:700; }

.toc {
  background:var(--bg-2); border:1px solid var(--border);
  border-radius:14px; padding:24px 28px; margin:32px 0;
}
.toc h3 { font-size:12.5px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.12em; margin-bottom:14px; font-family:'Inter'; font-weight:600; }
.toc ol { padding-left:22px; }
.toc li { margin-bottom:7px; }
.toc a { color:var(--ink-2); font-size:14.5px; }
.toc a:hover { color:var(--accent); }

section.body { padding:30px 0; }
section.body h2 {
  font-family:'Inter', -apple-system, sans-serif; font-weight:700;
  font-size:clamp(26px, 3vw, 38px);
  margin:56px 0 18px; letter-spacing:-0.025em; line-height:1.15;
  scroll-margin-top:80px;
}
section.body p, section.body ul, section.body ol { font-size:17px; color:var(--ink); line-height:1.78; margin-bottom:18px; }
section.body ul, section.body ol { padding-left:24px; }
section.body li { margin-bottom:8px; }
section.body a { color:var(--accent); text-decoration:underline; text-decoration-color:var(--accent-line); text-underline-offset:3px; }
section.body a:hover { text-decoration-color:var(--accent); }
section.body b, section.body strong { color:var(--ink); font-weight:600; }

.faq-section {
  padding:80px 0; background:var(--bg-2);
  border-top:1px solid var(--border); border-bottom:1px solid var(--border);
}
.faq-list { max-width:820px; margin:24px auto 0; }
.faq-item {
  padding:24px 28px; border:1px solid var(--border);
  border-radius:14px; margin-bottom:14px; background:var(--bg-card);
}
.faq-item h4 { font-family:'Inter'; font-weight:600; font-size:18px; margin-bottom:10px; color:var(--ink); letter-spacing:-0.015em; }
.faq-item p { color:var(--ink-2); font-size:15.5px; line-height:1.7; }
.faq-item a { color:var(--accent); text-decoration:underline; }

.cta-strip {
  padding:48px; background:var(--bg-dark); color:var(--ink-on-dark);
  border-radius:20px; text-align:center; margin:60px auto; max-width:900px;
}
.cta-strip h3 {
  font-family:'Inter', -apple-system, sans-serif; font-weight:700;
  font-size:28px; margin-bottom:10px; color:var(--ink-on-dark);
}
.cta-strip p { color:var(--ink-2-on-dark); margin-bottom:24px; font-size:16px; }
.cta-strip .btn { background:var(--accent); color:#fff; border-color:var(--accent); }
.cta-strip .btn:hover { background:#fff; color:var(--ink); border-color:#fff; }

/* Glossary */
.glossary-grid { display:grid; gap:14px; max-width:920px; margin:0 auto; }
.gloss { padding:22px 26px; background:var(--bg-card); border:1px solid var(--border); border-radius:14px; }
.gloss dt { font-family:'Inter'; font-weight:600; font-size:18px; color:var(--ink); margin-bottom:6px; letter-spacing:-0.015em; }
.gloss dd { color:var(--ink-2); font-size:15px; line-height:1.7; }
.gloss dd a { color:var(--accent); text-decoration:underline; }
.alpha-nav {
  position:sticky; top:72px; z-index:30;
  background:rgba(250,249,246,0.92); backdrop-filter:blur(14px);
  padding:14px 0; border-bottom:1px solid var(--border); margin-bottom:32px;
}
.alpha-nav .row { display:flex; flex-wrap:wrap; gap:6px; justify-content:center; }
.alpha-nav a {
  padding:4px 10px; color:var(--ink-2);
  font-family:'Inter'; font-weight:600; font-size:13px;
  border-radius:6px; transition:background .15s, color .15s;
}
.alpha-nav a:hover { background:var(--bg-2); color:var(--ink); }
.alpha-letter {
  font-family:'Inter', -apple-system, sans-serif; color:var(--accent);
  font-size:28px; font-weight:500; margin:32px 0 14px; padding-top:8px;
}
.alpha-letter:first-of-type { margin-top:0; }

/* Calculator */
.calc-grid { display:grid; grid-template-columns:1fr; gap:32px; max-width:1080px; margin:0 auto; }
@media (min-width:880px) { .calc-grid { grid-template-columns:1.3fr 1fr; } }
.calc-form { background:var(--bg-card); border:1px solid var(--border); border-radius:18px; padding:32px; box-shadow:var(--shadow-sm); }
.calc-out  {
  background:var(--bg-dark); color:var(--ink-on-dark);
  border-radius:18px; padding:32px;
}
.calc-field { margin-bottom:22px; }
.calc-field label { display:block; font-size:13px; color:var(--ink-2); text-transform:uppercase; letter-spacing:0.08em; font-weight:600; margin-bottom:8px; font-family:'Inter'; }
.calc-field select, .calc-field input {
  width:100%; padding:13px 16px;
  background:var(--bg); border:1px solid var(--border);
  border-radius:8px; color:var(--ink); font-size:15px; font-family:'Inter';
}
.calc-field select:focus, .calc-field input:focus {
  outline:none; border-color:var(--accent);
  box-shadow:0 0 0 3px var(--accent-soft);
}
.calc-out .vbig {
  font-family:'Inter', -apple-system, sans-serif; font-weight:700;
  font-size:48px; letter-spacing:-0.025em;
  color:var(--accent-line); margin-bottom:6px;
}
.calc-out .vsub { color:var(--ink-3-on-dark); font-size:14px; margin-bottom:24px; }
.calc-out .vrow {
  display:flex; justify-content:space-between; align-items:center;
  padding:12px 0; border-bottom:1px solid rgba(250,250,249,0.1);
  font-size:14.5px;
}
.calc-out .vrow:last-child { border-bottom:none; }
.calc-out .vrow .k { color:var(--ink-2-on-dark); }
.calc-out .vrow .v { font-family:'Inter'; font-weight:600; color:var(--ink-on-dark); }
.calc-summary {
  margin-top:24px; padding:18px;
  background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.18);
  border-radius:12px; color:#ffffff; font-size:14.5px; line-height:1.6;
}
.calc-summary b { color:#ffffff; }

/* Comparison */
.cmp-grid { display:grid; gap:14px; max-width:1080px; margin:32px auto; }
.cmp-card {
  display:grid; grid-template-columns:auto 1fr auto;
  gap:20px; align-items:center;
  padding:20px 24px; background:var(--bg-card);
  border:1px solid var(--border); border-radius:12px;
  transition:border-color .2s, transform .2s, box-shadow .2s;
  color:inherit;
}
.cmp-card:hover { border-color:var(--border-hover); transform:translateY(-2px); box-shadow:var(--shadow-sm); }
.cmp-card img { width:64px; height:64px; object-fit:contain; }
.cmp-card .cmp-title { font-family:'Inter'; font-weight:600; font-size:18px; margin-bottom:4px; color:var(--ink); letter-spacing:-0.015em; }
.cmp-card .cmp-sub { color:var(--ink-3); font-size:13px; }
.cmp-card .cmp-arr { color:var(--accent); font-weight:600; font-size:14px; }

.h2h-grid { display:grid; grid-template-columns:1fr; gap:24px; max-width:1080px; margin:40px auto; }
@media (min-width:768px) { .h2h-grid { grid-template-columns:1fr 1fr; } }
.h2h-card { background:var(--bg-card); border:1px solid var(--border); border-radius:18px; padding:32px; }
.h2h-card .vendor { font-size:11px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.12em; font-weight:600; margin-bottom:6px; }
.h2h-card h3 { font-family:'Inter', -apple-system, sans-serif; font-weight:700; font-size:26px; margin-bottom:10px; letter-spacing:-0.025em; }
.h2h-card .photo-wrap {
  aspect-ratio:1;
  background:linear-gradient(180deg, var(--bg-2) 0%, var(--bg-card) 100%);
  border:1px solid var(--border); border-radius:12px;
  display:flex; align-items:center; justify-content:center;
  margin:18px 0; padding:18px; position:relative; overflow:hidden;
}
.h2h-card .photo-wrap::before { content:""; position:absolute; inset:0; background:radial-gradient(45% 35% at 50% 50%, var(--accent-soft), transparent 70%); }
.h2h-card .photo-wrap img { max-height:88%; max-width:88%; width:auto; height:auto; object-fit:contain; position:relative; z-index:2; filter:drop-shadow(0 14px 28px rgba(28,25,23,0.15)); }
.h2h-card .price { font-family:'Inter', -apple-system, sans-serif; font-size:32px; font-weight:500; color:var(--accent); margin-bottom:14px; letter-spacing:-0.025em; }
.h2h-card .specs { display:grid; grid-template-columns:repeat(2,1fr); gap:10px; margin-bottom:18px; }
.h2h-card .specs div { padding:10px 12px; background:var(--bg-2); border:1px solid var(--border); border-radius:8px; font-size:12.5px; }
.h2h-card .specs div b { display:block; color:var(--ink); font-family:'Inter'; font-size:14px; font-weight:600; }
.h2h-card .specs div span { color:var(--ink-3); font-size:11px; text-transform:uppercase; letter-spacing:0.06em; }
.h2h-card ul { padding-left:18px; margin-bottom:18px; }
.h2h-card li { color:var(--ink-2); font-size:14px; margin-bottom:6px; line-height:1.55; }
.h2h-vs { text-align:center; color:var(--ink-3); font-family:'Inter'; font-size:28px; font-weight:600; padding:8px 0; }
"""

# NAV_HTML + FOOTER_HTML komen uit style_base.py

ORG_SCHEMA = json.dumps({
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": f"{SITE_URL}/#organization",
    "name": "BotLease",
    "legalName": "BotLease",
    "url": SITE_URL,
    "logo": f"{SITE_URL}/logo.png",
    "description": "Nederlands eerste full-service leasemaatschappij voor humanoïde robots. All-in operational lease vanaf €290 per maand: installatie, training, onderhoud, swap-SLA en EU AI-Act compliance.",
    "address": {"@type": "PostalAddress", "addressLocality": "Amsterdam", "addressCountry": "NL"},
    "email": "hallo@botlease.nl",
    "areaServed": ["NL", "BE", "DE", "LU"],
    "knowsAbout": ["humanoïde robots", "operational lease", "Robot-as-a-Service", "EU AI-Act", "Machineverordening 2023/1230", "Unitree", "NEURA Robotics", "Apptronik", "Figure AI", "Agility Robotics", "1X Technologies", "UBTECH", "EngineAI", "Pollen Robotics"],
    "identifier": {"@type": "PropertyValue", "propertyID": "KvK", "value": "95943420"},
    "founder": {"@type": "Person", "name": "Thomas Vedder", "jobTitle": "Oprichter"},
    "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "email": "hallo@botlease.nl", "areaServed": ["NL", "BE", "DE", "LU"], "availableLanguage": ["nl", "en"]},
}, ensure_ascii=False)


def _fmt_nl(html: str) -> str:
    """NL thousand separator (€1,295 -> €1.295) - scoped to euro amounts ONLY.
    A global (\\d),(\\d) regex would corrupt every rgba()/grid/JSON comma; this only
    touches commas inside a € amount, so CSS/JSON/JS are never altered."""
    import re
    return re.sub(r'€\d{1,3}(?:,\d{3})+', lambda m: m.group(0).replace(",", "."), html)


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
        # Cleaner: simpler logic - wrap raw text in <p>, leave HTML strings as-is
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
        "author": {"@type": "Person", "name": "Thomas Vedder", "url": f"{SITE_URL}/auteur/thomas-vedder"},
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
<meta name="description" content="{escape(trim_desc(g['meta_desc']))}">
<meta name="keywords" content="{escape(g['keywords'])}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta name="author" content="BotLease">
<link rel="canonical" href="{SITE_URL}/gids/{g['slug']}">

<meta property="og:type" content="article">
<meta property="og:title" content="{escape(g['title'])}">
<meta property="og:description" content="{escape(trim_desc(g['meta_desc']))}">
<meta property="og:url" content="{SITE_URL}/gids/{g['slug']}">
<meta property="og:image" content="{SITE_URL}{og_image}">
<meta property="og:locale" content="nl_NL">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(g['title'])}">
<meta name="twitter:description" content="{escape(trim_desc(g['meta_desc']))}">
<meta name="twitter:image" content="{SITE_URL}{og_image}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{article_jsonld}</script>
<script type="application/ld+json">{breadcrumb}</script>
{f'<script type="application/ld+json">{faq_jsonld}</script>' if faq_jsonld else ''}
<script type="application/ld+json">{speakable_jsonld}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
{HEAD_SEO}
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
        if letter == "I": letter = "I"  # placeholder for sorting trick - not needed
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
<meta name="description" content="{escape(trim_desc(g['meta_desc']))}">
<meta name="keywords" content="{escape(g['keywords'])}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/begrippen">
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(g['title'])}">
<meta property="og:description" content="{escape(trim_desc(g['meta_desc']))}">
<meta property="og:url" content="{SITE_URL}/begrippen">
<meta property="og:image" content="{SITE_URL}/img/robots/apollo.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{breadcrumb}</script>
<script type="application/ld+json">{defined_terms_jsonld}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
{HEAD_SEO}
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
      <p>Mail ons - wij voegen hem toe en linken hem aan de juiste robotmodellen.</p>
      <a class="btn" href="mailto:hallo@botlease.nl">Stuur een mail →</a>
    </div>
  </div>
</section>

{FOOTER_HTML}
</body>
</html>
"""


def render_simple(g: dict, kind: str = "over") -> str:
    """About / Methodology - no FAQ, simpler layout."""
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

    person_jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "Person",
        "@id": f"{SITE_URL}/#founder",
        "name": "Thomas Vedder",
        "jobTitle": "Oprichter",
        "url": f"{SITE_URL}/auteur/thomas-vedder",
        "worksFor": {"@id": f"{SITE_URL}/#organization"},
        "knowsAbout": ["humanoïde robots", "operational lease", "Robot-as-a-Service",
                       "EU AI-Act", "conversational AI", "Nederlandse maakindustrie"],
        "description": ("Oprichter van BotLease en redacteur van het BotLease-nieuws over "
                        "humanoïde robots in Nederland en Europa. Achtergrond in "
                        "conversational AI en taalmodellen."),
    }, ensure_ascii=False) if kind == "over" else ""

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(g['title'])}</title>
<meta name="description" content="{escape(trim_desc(g['meta_desc']))}">
<meta name="keywords" content="{escape(g['keywords'])}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/{g['slug']}">
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(g['title'])}">
<meta property="og:description" content="{escape(trim_desc(g['meta_desc']))}">
<meta property="og:url" content="{SITE_URL}/{g['slug']}">
<meta property="og:image" content="{SITE_URL}/img/robots/apollo.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{breadcrumb}</script>
{f'<script type="application/ld+json">{person_jsonld}</script>' if person_jsonld else ''}
<script type="application/ld+json">{ORG_SCHEMA}</script>
{HEAD_SEO}
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
        f'{escape(r["name"])} - €{r["lease_eur"]:,}/mnd</option>'.replace(",", ".")
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
<meta name="description" content="{escape(trim_desc(g['meta_desc']))}">
<meta name="keywords" content="{escape(g['keywords'])}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/kosten">
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(g['title'])}">
<meta property="og:description" content="{escape(trim_desc(g['meta_desc']))}">
<meta property="og:url" content="{SITE_URL}/kosten">
<meta property="og:image" content="{SITE_URL}/img/robots/apollo.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{breadcrumb}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
{HEAD_SEO}
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
        <div class="vbig" id="out-monthly">€1.295</div>
        <div class="vsub">per maand, all-in lease (excl. BTW)</div>

        <div class="vrow"><span class="k">Eenmalige setup</span><span class="v" id="out-setup">€2.500</span></div>
        <div class="vrow"><span class="k">Totaal contractwaarde</span><span class="v" id="out-total">€49.120</span></div>
        <div class="vrow"><span class="k">Aanschafprijs (publiek)</span><span class="v" id="out-purchase">€22.000</span></div>
        <div class="vrow"><span class="k">Vermeden loonkosten/jr</span><span class="v" id="out-savings">€58.240</span></div>
        <div class="vrow"><span class="k">Geschatte ROI-periode</span><span class="v" id="out-roi">10,1 mnd</span></div>

        <div class="calc-summary" id="out-summary">
          Selecteer een model om de berekening te starten.
        </div>
      </div>
    </div>

    <div style="max-width:840px; margin:60px auto 0">
      <h2 style="margin-bottom:16px">Wat zit er in de leaseprijs?</h2>
      <ul style="font-size:16.5px; line-height:1.75; color:var(--ink); padding-left:22px">
        <li><b>Robot zelf</b> - afschrijving over 36 maanden gedragen door BotLease.</li>
        <li><b>Installatie</b> + 2-uurs operatortraining (apart in setup-fee).</li>
        <li><b>Preventief + correctief onderhoud</b> - wij komen langs als er iets is.</li>
        <li><b>Onderdelen</b> - alle reserveonderdelen inbegrepen.</li>
        <li><b>Swap-SLA</b> - vervangende unit binnen 24u op locatie (anders €100/dag vergoeding).</li>
        <li><b>Verzekering</b> - WA tot €2,5M + casco.</li>
        <li><b>helpdesk op werkdagen</b> - Nederlands sprekende engineers.</li>
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
      <p>De leaseprijs is gebaseerd op aanschafprijs / 36 maanden + 25% service-reserve + 8% verzekering + 30% marge. Voor specifieke modellen ronden we naar beneden af. ROI-periode is een schatting op basis van: (totaal contract / jaarlijkse besparing) × 12. Echte ROI hangt af van je situatie - laat ons een individuele case-study maken in de gratis intake.</p>
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
    document.getElementById('out-roi').textContent      = roiMo > 0 ? roiMo.toFixed(1) + ' mnd' : '-';

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
    """The /vergelijken hub - sortable table of all robots."""
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
        </a>""" for r in ROBOTS
    )

    # Editoriale "beste per use-case 2026" picks (data-grounded)
    _rob = {r["slug"]: r for r in ROBOTS}
    PICKS = [
        ("🥇", "Beste instapmodel", "unitree-r1", "Laagste drempel om te starten — volwaardige bipedal voor demo's, onderzoek en lichte taken."),
        ("⚖️", "Beste prijs-kwaliteit allround", "unitree-g1", "Het werkpaard: bewezen, breed inzetbaar voor service en R&D, scherpe maandprijs."),
        ("🇪🇺", "Beste EU-gebouwd", "neura-4ne1-mini", "In Duitsland gebouwd — kortste levertijd, lokale support en compliance ingebouwd."),
        ("📦", "Beste voor logistiek &amp; fulfilment (3PL)", "agility-digit", "Purpose-built voor warehouse: tassen tillen, bins verplaatsen. Draait al bij echte 3PL-pilots."),
        ("🏭", "Beste voor zware productie", "unitree-h1-2", "Hoogste payload en snelheid in de catalogus — gemaakt voor industrieel tilwerk."),
        ("🔬", "Beste voor onderzoek &amp; manipulatie", "pollen-reachy-2", "Open-source en EU-gebouwd (Frankrijk) — ideaal voor labs en fijne grijptaken."),
    ]
    pick_cards = "".join(
        f"""<a href="/robots/{slug}" class="cmp-card">
        <div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px; font-size:30px">{emoji}</div>
        <div>
          <div style="font-size:11px; text-transform:uppercase; letter-spacing:0.1em; color:var(--ink-3); font-weight:700; margin-bottom:3px">{award}</div>
          <div class="cmp-title">{escape(_rob[slug]['name'])}{' · wachtlijst' if _rob[slug]['tier'] == 'premium' else ''}</div>
          <div class="cmp-sub">{why}</div>
        </div>
        <div style="text-align:right"><div class="cmp-arr">€{_rob[slug]['lease_eur']:,}/mnd</div></div>
      </a>""" for emoji, award, slug, why in PICKS
    )

    _ranked = sorted(ROBOTS, key=lambda r: (r["tier"] == "premium", r["lease_eur"]))
    itemlist_jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "ItemList",
        "name": "Humanoïde robots vergelijken in Nederland (2026)",
        "description": "Vergelijking van 15 humanoïde robots beschikbaar voor operational lease in Nederland, gerangschikt op leverbaarheid en maandprijs.",
        "itemListOrder": "https://schema.org/ItemListOrderAscending",
        "numberOfItems": len(_ranked),
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": f"{SITE_URL}/robots/{r['slug']}", "name": r["name"]}
            for i, r in enumerate(_ranked)
        ],
    }, ensure_ascii=False)

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
<title>Humanoïde robots vergelijken: 13 modellen naast elkaar (2026) | BotLease</title>
<meta name="description" content="Vergelijk 15 humanoïde robots op prijs, specs en leverbaarheid in Nederland. Alle leaseprijzen all-in per maand, van €290 tot €6.650. Inclusief onze keuze per use-case.">
<meta name="keywords" content="humanoide robots vergelijken, robot vergelijking, humanoid robot specs prijzen, vergelijk humanoid lease">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/vergelijken">
<meta property="og:type" content="website">
<meta property="og:title" content="Humanoïde robots vergelijken | BotLease">
<meta property="og:description" content="13 modellen naast elkaar - specs, prijs, use-case.">
<meta property="og:url" content="{SITE_URL}/vergelijken">
<meta property="og:image" content="{SITE_URL}/img/robots/apollo.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{breadcrumb}</script>
<script type="application/ld+json">{itemlist_jsonld}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
{HEAD_SEO}
</head>
<body>
{NAV_HTML}

<section class="g-hero">
  <div class="container">
    <nav class="crumbs"><a href="/">Home</a><span class="sep">/</span><span>Vergelijken</span></nav>
    <span class="eyebrow">Vergelijken · 2026</span>
    <h1>Vergelijk 15 humanoïde robots — specs, prijs en leverbaarheid.</h1>
    <p class="tag">Welke humanoïde robot past bij jouw use-case? Hieronder onze keuze per situatie, gevolgd door alle 13 modellen naast elkaar — specs, prijs en leverbaarheid in Nederland. Alle prijzen all-in per maand.</p>
  </div>
</section>

<section style="border-top:1px solid var(--line); padding:60px 0">
  <div class="container">
    <span class="eyebrow">Onze keuze · 2026</span>
    <h2 style="margin:14px 0 10px">Onze keuze per use-case</h2>
    <p class="tag" style="max-width:700px; margin-bottom:28px">Geen enkele humanoïde robot is "de beste" voor álles. Dit is per situatie het sterkste model uit onze catalogus van 15 — beoordeeld op leverbaarheid in Nederland, prijs-kwaliteit en bewezen inzet. Alle prijzen zijn all-in per maand. Lees ook de volledige ranking: <a href="/beste-humanoide-robots-2026" style="color:var(--accent)">de beste humanoïde robots voor bedrijven (2026) →</a></p>
    <div class="cmp-grid">{pick_cards}</div>
    <p style="margin-top:20px; color:var(--ink-3); font-size:12.5px">Laatst bijgewerkt: 5 juni 2026 · 13 modellen, prijzen all-in per maand.</p>
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
    <h2 style="margin:14px 0 28px">Direct vergelijken - top 5 vergelijkingen.</h2>
    <div class="cmp-grid">
      <a href="/vergelijken/unitree-g1-vs-neura-4ne1-mini" class="cmp-card"><div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px; font-family:'Inter'; font-weight:700; font-size:13px; color:var(--ink-2)">G1 vs M</div><div><div class="cmp-title">Unitree G1 vs NEURA 4NE-1 Mini</div><div class="cmp-sub">Bestseller vs EU-instap · beide €1.295 per maand</div></div><div class="cmp-arr">Vergelijk →</div></a>
      <a href="/vergelijken/unitree-h1-2-vs-ubtech-walker-s2" class="cmp-card"><div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px; font-family:'Inter'; font-weight:700; font-size:13px; color:var(--ink-2)">H1 vs W2</div><div><div class="cmp-title">Unitree H1-2 vs UBTECH Walker S2</div><div class="cmp-sub">Industrieel value vs auto-industrie · €6.650 vs €5.750</div></div><div class="cmp-arr">Vergelijk →</div></a>
      <a href="/vergelijken/neura-4ne1-gen3-vs-apptronik-apollo" class="cmp-card"><div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px; font-family:'Inter'; font-weight:700; font-size:13px; color:var(--ink-2)">EU vs US</div><div><div class="cmp-title">NEURA 4NE-1 Gen 3.5 vs Apptronik Apollo</div><div class="cmp-sub">EU-flagship vs US-wachtlijst · €5.950 vs €3.499</div></div><div class="cmp-arr">Vergelijk →</div></a>
      <a href="/vergelijken/unitree-r1-vs-engineai-se01" class="cmp-card"><div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px; font-family:'Inter'; font-weight:700; font-size:13px; color:var(--ink-2)">R1 vs SE</div><div><div class="cmp-title">Unitree R1 vs EngineAI SE01</div><div class="cmp-sub">Instap demo vs natural gait · €290 vs €1.590</div></div><div class="cmp-arr">Vergelijk →</div></a>
      <a href="/vergelijken/apptronik-apollo-vs-figure-02" class="cmp-card"><div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px; font-family:'Inter'; font-weight:700; font-size:13px; color:var(--ink-2)">Apollo vs F2</div><div><div class="cmp-title">Apptronik Apollo vs Figure 02</div><div class="cmp-sub">Mercedes-pilot vs BMW-pilot · €3.499 vs €3.899</div></div><div class="cmp-arr">Vergelijk →</div></a>
      <a href="/vergelijken/humanoid-vs-cobot" class="cmp-card"><div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px; font-family:'Inter'; font-weight:700; font-size:13px; color:var(--ink-2)">H vs C</div><div><div class="cmp-title">Humanoïde robot vs cobot</div><div class="cmp-sub">Welke automatisering past bij jouw proces? · beslisgids</div></div><div class="cmp-arr">Vergelijk →</div></a>
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
        </div>"""

    h1 = f"{a['name']} vs {b['name']} - vergelijking 2026"
    title = f"{h1} | BotLease"
    def _eu(n):
        return "€" + f"{n:,}".replace(",", ".")
    meta_desc = (f"Side-by-side vergelijking {a['name']} vs {b['name']}: specs, prijs, use-case en leverbaarheid. "
                 f"{_eu(a['lease_eur'])}/mnd vs {_eu(b['lease_eur'])}/mnd, all-in lease.")
    slug = f"{slug_a}-vs-{slug_b}"
    breadcrumb = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Vergelijken", "item": f"{SITE_URL}/vergelijken"},
            {"@type": "ListItem", "position": 3, "name": f"{a['name']} vs {b['name']}", "item": f"{SITE_URL}/vergelijken/{slug}"},
        ],
    }, ensure_ascii=False)

    # ItemList schema voor vergelijkingen - beide producten in één lijst
    itemlist_h2h = json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": [
            {
                "@type": "ListItem", "position": 1,
                "item": {
                    "@type": "Product",
                    "name": a["name"],
                    "image": f"{SITE_URL}{a['photo']}",
                    "url": f"{SITE_URL}/robots/{a['slug']}",
                    "offers": {"@type": "Offer", "priceCurrency": "EUR", "price": str(a["lease_eur"]), "url": f"{SITE_URL}/robots/{a['slug']}"},
                },
            },
            {
                "@type": "ListItem", "position": 2,
                "item": {
                    "@type": "Product",
                    "name": b["name"],
                    "image": f"{SITE_URL}{b['photo']}",
                    "url": f"{SITE_URL}/robots/{b['slug']}",
                    "offers": {"@type": "Offer", "priceCurrency": "EUR", "price": str(b["lease_eur"]), "url": f"{SITE_URL}/robots/{b['slug']}"},
                },
            },
        ],
    }, ensure_ascii=False)

    # Comparison verdict
    if a["tier"] == "eu" and b["tier"] != "eu":
        verdict = f"<b>{a['name']}</b> wint op EU-compliance en supply chain (gebouwd in {a['vendor_country']}). <b>{b['name']}</b> wint op prijs of capaciteit voor specifieke use-cases. Voor compliance-gevoelige sectoren (zorg, government, financieel): kies de {a['name']}."
    elif b["tier"] == "eu" and a["tier"] != "eu":
        verdict = f"<b>{b['name']}</b> wint op EU-compliance en supply chain (gebouwd in {b['vendor_country']}). <b>{a['name']}</b> wint op prijs of capaciteit voor specifieke use-cases. Voor compliance-gevoelige sectoren (zorg, government, financieel): kies de {b['name']}."
    elif a["category"] == "waitlist" and b["category"] == "available":
        verdict = f"<b>{b['name']}</b> wint op leverbaarheid (direct bestelbaar). <b>{a['name']}</b> staat op de wachtlijst voor 2027 - alleen reserveren mogelijk. Voor productieve inzet 2026: kies de {b['name']}."
    elif b["category"] == "waitlist" and a["category"] == "available":
        verdict = f"<b>{a['name']}</b> wint op leverbaarheid (direct bestelbaar). <b>{b['name']}</b> staat op de wachtlijst voor 2027. Voor productieve inzet 2026: kies de {a['name']}."
    elif a["lease_eur"] < b["lease_eur"] * 0.7:
        verdict = f"<b>{a['name']}</b> is significant goedkoper (€{a['lease_eur']:,}/mnd vs €{b['lease_eur']:,}/mnd). <b>{b['name']}</b> heeft hogere payload en is geschikter voor heavy-duty taken. Voor lichte use-cases (demo, R&D, lichte service): {a['name']}. Voor industrieel: {b['name']}.".replace(",", ".")
    elif b["lease_eur"] < a["lease_eur"] * 0.7:
        verdict = f"<b>{b['name']}</b> is significant goedkoper (€{b['lease_eur']:,}/mnd vs €{a['lease_eur']:,}/mnd). <b>{a['name']}</b> heeft hogere payload en is geschikter voor heavy-duty taken. Voor lichte use-cases: {b['name']}. Voor industrieel: {a['name']}.".replace(",", ".")
    else:
        verdict = f"Beide modellen zitten in dezelfde prijsklasse. Het verschil zit in de details: <b>{a['name']}</b> is sterk voor {', '.join(a['tags'][:2]).lower()}, <b>{b['name']}</b> voor {', '.join(b['tags'][:2]).lower()}. Plan een intake voor specifiek advies."

    # Extra E-A-T padding: full spec table + decision-tree + auto-FAQ
    def euro(x):
        return f"€{x:,}".replace(",", ".")

    full_spec_rows = [
        ("Hoogte", f"{a['height_cm']} cm", f"{b['height_cm']} cm"),
        ("Gewicht", f"{a['weight_kg']} kg", f"{b['weight_kg']} kg"),
        ("Payload", f"{a['payload_kg']} kg", f"{b['payload_kg']} kg"),
        ("Batterij", f"{a['battery_hours']} u", f"{b['battery_hours']} u"),
        ("Snelheid", f"{a['speed_ms']} m/s", f"{b['speed_ms']} m/s"),
        ("Vrijheidsgraden (DoF)", str(a["dof"]), str(b["dof"])),
        ("Land van productie", a["vendor_country"], b["vendor_country"]),
        ("Lease p/mnd", euro(a["lease_eur"]) + "/mnd", euro(b["lease_eur"]) + "/mnd"),
        ("Setup-fee", euro(a["setup_eur"]), euro(b["setup_eur"])),
        ("Publieke aanschafprijs", euro(a["purchase_eur"]), euro(b["purchase_eur"])),
        ("Beschikbaarheid", "Direct leverbaar" if a["category"] == "available" else "Wachtlijst", "Direct leverbaar" if b["category"] == "available" else "Wachtlijst"),
    ]
    spec_table_html = "".join(
        f'<tr><td style="padding:11px 14px; color:var(--ink-3); font-size:13px; border-bottom:1px solid var(--border)">{escape(k)}</td>'
        f'<td style="padding:11px 14px; color:var(--ink); font-size:14.5px; font-weight:500; border-bottom:1px solid var(--border)">{escape(va)}</td>'
        f'<td style="padding:11px 14px; color:var(--ink); font-size:14.5px; font-weight:500; border-bottom:1px solid var(--border)">{escape(vb)}</td></tr>'
        for k, va, vb in full_spec_rows
    )

    # "Wanneer NIET" reasoning per robot
    def not_for(r):
        if r["payload_kg"] < 6:
            return f"Heavy-duty industriële kitting of pallet-handling - {r['name']} heeft slechts {r['payload_kg']} kg payload."
        if r["battery_hours"] < 3:
            return f"24/7 productie zonder hot-swap - batterijduur is {r['battery_hours']} uur, niet geschikt voor continue dubbele shifts zonder onderbreking."
        if r["category"] == "waitlist":
            return f"Productieve inzet in 2026 - {r['name']} is nog niet open verkrijgbaar voor EU-derden, alleen reserveringen mogelijk."
        if r["lease_eur"] > 4000:
            return f"Light-duty events, demo's of receptie - bij {euro(r['lease_eur'])}/mnd is dit een industrieel platform dat zich pas terugbetaalt bij ≥30 uur productief werk per week."
        return f"Hoogwaardige zorgrobotica of safety-critical pilots - {r['name']} is een general-purpose model, geen gespecialiseerde zorg-of operatie-eenheid."

    # Auto-FAQ voor vergelijking
    faq_h2h = [
        {
            "q": f"Wat is het belangrijkste verschil tussen {a['name']} en {b['name']}?",
            "a": f"De {a['name']} ({euro(a['lease_eur'])}/mnd, {a['payload_kg']} kg payload, {a['vendor_country']}) is geoptimaliseerd voor {', '.join(a['tags'][:2]).lower()}. De {b['name']} ({euro(b['lease_eur'])}/mnd, {b['payload_kg']} kg payload, {b['vendor_country']}) richt zich op {', '.join(b['tags'][:2]).lower()}. Het scherpste verschil zit in payload, prijspunt en EU-supply chain.",
        },
        {
            "q": f"Welke is goedkoper, {a['name']} of {b['name']}?",
            "a": f"De {a['name']} kost {euro(a['lease_eur'])}/mnd, de {b['name']} {euro(b['lease_eur'])}/mnd - verschil van {euro(abs(a['lease_eur']-b['lease_eur']))}/mnd. Over een 36-mnd lease scheelt dat {euro(abs(a['lease_eur']-b['lease_eur'])*36)}. Beide all-in inclusief installatie, training, onderhoud, swap-SLA en verzekering.",
        },
        {
            "q": f"Voldoen {a['name']} én {b['name']} aan de EU AI-Act?",
            "a": f"BotLease voert per deployment een EU AI-Act risicoanalyse uit en regelt de CE-conformiteit onder Machineverordening 2023/1230, voor zowel {a['name']} (productie {a['vendor_country']}) als {b['name']} (productie {b['vendor_country']}). EU-gebouwde modellen hebben een kortere paper-trail; niet-EU modellen vergen extra technische documentatie bij de douane.",
        },
        {
            "q": f"Hoe lang duurt het voordat een {a['name']} of {b['name']} operationeel is?",
            "a": f"Direct leverbare modellen: 6-10 weken vanaf intake tot operationeel inclusief 2-uurs operator-training. {a['name']}: {'leverbaar binnen 6-10 weken' if a['category']=='available' else 'wachtlijst 2027'}. {b['name']}: {'leverbaar binnen 6-10 weken' if b['category']=='available' else 'wachtlijst 2027'}.",
        },
        {
            "q": f"Kan ik {a['name']} en {b['name']} ook combineren in één deployment?",
            "a": f"Ja. BotLease ondersteunt heterogene vloten - bijvoorbeeld een {a['name']} voor licht werk en een {b['name']} voor zwaardere taken. We harmoniseren de fleet-management-stack, helpdesk en swap-SLA over beide modellen, en bieden bij ≥3 units een gecombineerde lease-deal met staffelkorting.",
        },
    ]
    faq_h2h_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
            for f in faq_h2h
        ],
    }, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)}</title>
<meta name="description" content="{escape(trim_desc(meta_desc))}">
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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{breadcrumb}</script>
<script type="application/ld+json">{itemlist_h2h}</script>
<script type="application/ld+json">{faq_h2h_jsonld}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
{HEAD_SEO}
</head>
<body>
{NAV_HTML}

<section class="g-hero">
  <div class="container">
    <nav class="crumbs"><a href="/">Home</a><span class="sep">/</span><a href="/vergelijken">Vergelijken</a><span class="sep">/</span><span>{escape(a['name'])} vs {escape(b['name'])}</span></nav>
    <span class="eyebrow">Head-to-head</span>
    <h1>{escape(h1)}.</h1>
    <p class="tag">€{a['lease_eur']:,}/mnd vs €{b['lease_eur']:,}/mnd · {a['vendor_country']} vs {b['vendor_country']} - een eerlijke side-by-side voor MKB-ondernemers.</p>
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

      <h2 style="margin-top:36px">Volledige spec-vergelijking</h2>
      <p style="color:var(--ink-2); font-size:15.5px; line-height:1.65; margin-bottom:18px">Alle harde cijfers naast elkaar. Voor uitgebreide motivering per spec en third-party benchmarks: zie de detail-pagina's onderaan.</p>
      <table style="width:100%; border-collapse:collapse; background:var(--bg-card); border:1px solid var(--border); border-radius:10px; overflow:hidden; margin-top:6px">
        <thead><tr style="background:var(--bg-2)">
          <th style="text-align:left; padding:12px 14px; font-size:11.5px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.06em; font-weight:600">Specificatie</th>
          <th style="text-align:left; padding:12px 14px; font-size:13px; color:var(--ink); font-weight:600">{escape(a['name'])}</th>
          <th style="text-align:left; padding:12px 14px; font-size:13px; color:var(--ink); font-weight:600">{escape(b['name'])}</th>
        </tr></thead>
        <tbody>{spec_table_html}</tbody>
      </table>

      <h2 style="margin-top:40px">Wanneer kies je {escape(a['name'])}?</h2>
      <p style="color:var(--ink-2); font-size:15.5px; line-height:1.7; margin-bottom:14px">De {escape(a['name'])} is gebouwd voor {', '.join(a['tags'][:3]).lower()}. Op specs gemeten is dit het juiste model wanneer je payload tot {a['payload_kg']} kg verwacht, batterijduur van {a['battery_hours']} uur per shift voldoende is, en je in de prijsklasse van {euro(a['lease_eur'])}/mnd zit. Veel voorkomende toepassingen waar deze configuratie zich terugbetaalt:</p>
      <ul style="color:var(--ink-2); font-size:15px; line-height:1.7">
        {''.join(f'<li style="margin-bottom:6px">{escape(uc)}</li>' for uc in a['use_cases'])}
      </ul>

      <h2 style="margin-top:36px">Wanneer kies je {escape(b['name'])}?</h2>
      <p style="color:var(--ink-2); font-size:15.5px; line-height:1.7; margin-bottom:14px">De {escape(b['name'])} bedient {', '.join(b['tags'][:3]).lower()}. Met {b['payload_kg']} kg payload, {b['battery_hours']} uur batterijduur en een instapprijs van {euro(b['lease_eur'])}/mnd is dit het model dat past wanneer je use-case meer richting deze profielen leunt:</p>
      <ul style="color:var(--ink-2); font-size:15px; line-height:1.7">
        {''.join(f'<li style="margin-bottom:6px">{escape(uc)}</li>' for uc in b['use_cases'])}
      </ul>

      <h2 style="margin-top:36px">Wanneer kies je géén van beide?</h2>
      <p style="color:var(--ink-2); font-size:15.5px; line-height:1.7; margin-bottom:10px"><b>{escape(a['name'])} past niet voor:</b> {escape(not_for(a))}</p>
      <p style="color:var(--ink-2); font-size:15.5px; line-height:1.7">; <b>{escape(b['name'])} past niet voor:</b> {escape(not_for(b))} In die gevallen is de catalogus van 13 modellen op <a href="/robots">/robots</a> de betere ingang - vooral de modellen in een aangrenzende prijsklasse of met een afwijkende footprint.</p>

      <h2 style="margin-top:36px">Veelgestelde vragen</h2>
      <div style="margin-top:14px">
        {''.join(f'<details style="border-top:1px solid var(--border); padding:0"><summary style="cursor:pointer; list-style:none; padding:16px 4px; font-size:16px; font-weight:500; color:var(--ink); display:flex; justify-content:space-between; gap:20px">{escape(f["q"])}<span style="color:var(--ink-3); font-size:20px; font-weight:300">+</span></summary><p style="padding:0 4px 18px; font-size:15px; line-height:1.65; color:var(--ink-2)">{escape(f["a"])}</p></details>' for f in faq_h2h)}
        <div style="border-top:1px solid var(--border)"></div>
      </div>

      <h2 style="margin-top:36px">Bekijk de detailpagina's</h2>
      <p><a href="/robots/{a['slug']}">Volledige specs en use-cases voor de {escape(a['name'])}</a> · <a href="/robots/{b['slug']}">Volledige specs en use-cases voor de {escape(b['name'])}</a></p>
    </div>

    <div class="cta-strip">
      <h3>Niet zeker welke past?</h3>
      <p>Plan een gratis intake - wij adviseren onafhankelijk welke past bij jouw use-case.</p>
      <a class="btn" href="/#contact">Plan een demo →</a>
    </div>
  </div>
</section>

{FOOTER_HTML}
</body>
</html>
"""


def render_gids_hub() -> str:
    """The /gids/ index - links to pillar + AI-Act guides."""
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
<title>Humanoïde robot leasing - gidsen en bronnen | BotLease</title>
<meta name="description" content="Complete gidsen voor humanoïde robot leasing in Nederland: pillar guide, EU AI-Act compliance, lease calculator, methodologie.">
<link rel="canonical" href="{SITE_URL}/gids/">
<meta property="og:type" content="website">
<meta property="og:title" content="BotLease gidsen - humanoïde robot leasing">
<meta property="og:image" content="{SITE_URL}/img/robots/apollo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{breadcrumb}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
{HEAD_SEO}
</head><body>
{NAV_HTML}
<section class="g-hero"><div class="container">
  <nav class="crumbs"><a href="/">Home</a><span class="sep">/</span><span>Gids</span></nav>
  <span class="eyebrow">Gidsen</span>
  <h1>Alles wat je moet weten over humanoïde robot leasing.</h1>
  <p class="tag">Long-form gidsen, calculator, vergelijkingen en glossary - voor wie verder wil dan een marketingbrochure.</p>
</div></section>
<section class="body"><div class="container">
  <div class="cmp-grid">
    <a href="/gids/humanoide-robot-leasen" class="cmp-card">
      <div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#0066cc" stroke-width="2"><path d="M4 4h16v4H4z"/><path d="M4 10h10v10H4z"/><path d="M16 12h4v8h-4z"/></svg></div>
      <div><div class="cmp-title">Pillar guide: humanoïde robot leasen</div><div class="cmp-sub">3.000 woorden - modellen, kosten, ROI, EU compliance, pilot-proces</div></div>
      <div class="cmp-arr">Lees →</div></a>
    <a href="/gids/ai-act-machineverordening" class="cmp-card">
      <div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#0066cc" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 6v6l4 2"/></svg></div>
      <div><div class="cmp-title">EU AI-Act + Machineverordening gids</div><div class="cmp-sub">2.500 woorden - compliance vanaf 2 augustus 2026 + 20 januari 2027</div></div>
      <div class="cmp-arr">Lees →</div></a>
    <a href="/kosten" class="cmp-card">
      <div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#0066cc" stroke-width="2"><path d="M6 4h12v16H6z"/><path d="M9 8h6"/><path d="M9 12h6"/><path d="M9 16h3"/></svg></div>
      <div><div class="cmp-title">Lease cost calculator</div><div class="cmp-sub">Interactieve berekening - leaseprijs, ROI, vergelijking koop vs lease</div></div>
      <div class="cmp-arr">Bereken →</div></a>
    <a href="/begrippen" class="cmp-card">
      <div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#0066cc" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h10"/></svg></div>
      <div><div class="cmp-title">Begrippenlijst</div><div class="cmp-sub">40+ termen uitgelegd - AGV, cobot, SLAM, VLA, EU AI-Act</div></div>
      <div class="cmp-arr">Bekijk →</div></a>
    <a href="/methodologie" class="cmp-card">
      <div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#0066cc" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 1v6m0 10v6m11-11h-6M7 12H1"/></svg></div>
      <div><div class="cmp-title">Methodologie</div><div class="cmp-sub">Hoe wij robots evalueren, prijzen berekenen, risico's dragen</div></div>
      <div class="cmp-arr">Lees →</div></a>
    <a href="/over" class="cmp-card">
      <div style="width:72px; height:72px; display:flex; align-items:center; justify-content:center; background:var(--bg-3); border-radius:8px"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#0066cc" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 20a8 8 0 0116 0"/></svg></div>
      <div><div class="cmp-title">Over BotLease</div><div class="cmp-sub">Missie, team, waarom we bestaan</div></div>
      <div class="cmp-arr">Lees →</div></a>
  </div>
</div></section>
{FOOTER_HTML}
</body></html>
"""


def render_decision_page(slug: str, title: str, h1: str, meta_desc: str, intro: str, sections: list[tuple[str, str]], faqs: list[dict]) -> str:
    """Generic decision-pillar pagina (lease-vs-koop, humanoid-vs-cobot, etc.)"""
    breadcrumb = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Vergelijken", "item": f"{SITE_URL}/vergelijken"},
            {"@type": "ListItem", "position": 3, "name": h1, "item": f"{SITE_URL}/vergelijken/{slug}"},
        ],
    }, ensure_ascii=False)
    faq_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faqs],
    }, ensure_ascii=False)
    sections_html = "".join(
        f'<h2 style="margin-top:36px">{escape(h)}</h2>\n<div style="color:var(--ink-2); font-size:15.5px; line-height:1.7">{body}</div>'
        for h, body in sections
    )
    faq_html = "".join(
        f'<details style="border-top:1px solid var(--border); padding:0"><summary style="cursor:pointer; list-style:none; padding:16px 4px; font-size:16px; font-weight:500; color:var(--ink); display:flex; justify-content:space-between; gap:20px">{escape(f["q"])}<span style="color:var(--ink-3); font-size:20px; font-weight:300">+</span></summary><p style="padding:0 4px 18px; font-size:15px; line-height:1.65; color:var(--ink-2)">{escape(f["a"])}</p></details>'
        for f in faqs
    )
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)}</title>
<meta name="description" content="{escape(trim_desc(meta_desc))}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/vergelijken/{slug}">
<meta property="og:type" content="article">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(meta_desc)}">
<meta property="og:url" content="{SITE_URL}/vergelijken/{slug}">
<meta property="og:image" content="{SITE_URL}/img/hero/hero-robot.webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{breadcrumb}</script>
<script type="application/ld+json">{faq_jsonld}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
{HEAD_SEO}
</head>
<body>
{NAV_HTML}
<section class="g-hero">
  <div class="container">
    <nav class="crumbs"><a href="/">Home</a><span class="sep">/</span><a href="/vergelijken">Vergelijken</a><span class="sep">/</span><span>{escape(h1)}</span></nav>
    <span class="eyebrow">Beslisgids</span>
    <h1>{escape(h1)}.</h1>
    <p class="tag">{escape(intro)}</p>
  </div>
</section>
<section class="body"><div class="container"><div style="max-width:780px">
{sections_html}

<h2 style="margin-top:40px">Veelgestelde vragen</h2>
<div style="margin-top:14px">{faq_html}<div style="border-top:1px solid var(--border)"></div></div>

<div class="cta-strip" style="margin-top:40px">
  <h3>Niet zeker over jouw situatie?</h3>
  <p>Plan een gratis 30-min intake - wij adviseren onafhankelijk op basis van jouw use-case.</p>
  <a class="btn" href="/#contact">Plan een demo →</a>
</div>
</div></div></section>
{FOOTER_HTML}
</body></html>"""


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
    (vergelijken / "index.html").write_text(_fmt_nl(render_comparison_hub()), encoding="utf-8")

    # 6 head-to-head pages
    head_to_heads = [
        ("unitree-g1", "neura-4ne1-mini"),
        ("unitree-h1-2", "ubtech-walker-s2"),
        ("neura-4ne1-gen3", "apptronik-apollo"),
        ("unitree-r1", "engineai-se01"),
        ("apptronik-apollo", "figure-02"),
    ]
    for a, b in head_to_heads:
        html = render_h2h(a, b)
        if html:
            (vergelijken / f"{a}-vs-{b}.html").write_text(_fmt_nl(html), encoding="utf-8")

    # Audit-suggested decision pages: lease-vs-koop, humanoid-vs-cobot (near-zero NL competition)
    lease_vs_koop = render_decision_page(
        slug="lease-vs-koop",
        title="Humanoïde robot leasen of kopen? Vergelijking 2026 | BotLease",
        h1="Humanoïde robot leasen of kopen",
        meta_desc="Humanoïde robot leasen of kopen? Vergelijking van capex, cashflow, restwaarde-risico en compliance. Voor Nederlandse MKB - wat past wanneer.",
        intro="De €25k tot €100k+ vraag: is een humanoïde robot een aanschafbeslissing of een operationele uitgave? Hier zit het écht.",
        sections=[
            ("De cijfers - €25.000 robot, 36 maanden",
             "<p>Een Unitree G1 kost €16.000 koop, €1.295/mnd lease (€46.620 over 36 maanden). Op het eerste oog dus 2× zo duur leasen. Maar dat is een misleidende vergelijking - die €1.295 omvat dingen die je bij koop nog moet betalen.</p>"
             "<table style='width:100%; border-collapse:collapse; margin:18px 0; background:var(--bg-card); border:1px solid var(--border); border-radius:10px; overflow:hidden'>"
             "<thead><tr style='background:var(--bg-2)'><th style='padding:11px 14px; text-align:left; font-size:11.5px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.06em'>Component</th><th style='padding:11px 14px; text-align:right; font-size:11.5px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.06em'>Kopen (zelf)</th><th style='padding:11px 14px; text-align:right; font-size:11.5px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.06em'>Leasen via BotLease</th></tr></thead>"
             "<tbody>"
             "<tr><td style='padding:10px 14px; border-bottom:1px solid var(--border); font-size:14px'>Aanschaf / lease (36mnd)</td><td style='padding:10px 14px; border-bottom:1px solid var(--border); text-align:right; font-size:14px'>€16.000</td><td style='padding:10px 14px; border-bottom:1px solid var(--border); text-align:right; font-size:14px'>€46.620</td></tr>"
             "<tr><td style='padding:10px 14px; border-bottom:1px solid var(--border); font-size:14px'>Installatie + training</td><td style='padding:10px 14px; border-bottom:1px solid var(--border); text-align:right; font-size:14px'>€2.500</td><td style='padding:10px 14px; border-bottom:1px solid var(--border); text-align:right; font-size:14px'>incl.</td></tr>"
             "<tr><td style='padding:10px 14px; border-bottom:1px solid var(--border); font-size:14px'>Onderhoud + onderdelen (3 jaar)</td><td style='padding:10px 14px; border-bottom:1px solid var(--border); text-align:right; font-size:14px'>€6.900 (10%/j)</td><td style='padding:10px 14px; border-bottom:1px solid var(--border); text-align:right; font-size:14px'>incl.</td></tr>"
             "<tr><td style='padding:10px 14px; border-bottom:1px solid var(--border); font-size:14px'>WA-verzekering (3 jaar)</td><td style='padding:10px 14px; border-bottom:1px solid var(--border); text-align:right; font-size:14px'>€2.300 (1%/j)</td><td style='padding:10px 14px; border-bottom:1px solid var(--border); text-align:right; font-size:14px'>incl.</td></tr>"
             "<tr><td style='padding:10px 14px; border-bottom:1px solid var(--border); font-size:14px'>EU AI-Act compliance traject</td><td style='padding:10px 14px; border-bottom:1px solid var(--border); text-align:right; font-size:14px'>€3.000-€8.000</td><td style='padding:10px 14px; border-bottom:1px solid var(--border); text-align:right; font-size:14px'>incl.</td></tr>"
             "<tr><td style='padding:10px 14px; border-bottom:1px solid var(--border); font-size:14px'>Swap-SLA reserve unit</td><td style='padding:10px 14px; border-bottom:1px solid var(--border); text-align:right; font-size:14px'>kun je niet zelf</td><td style='padding:10px 14px; border-bottom:1px solid var(--border); text-align:right; font-size:14px'>24u swap inbegrepen</td></tr>"
             "<tr><td style='padding:10px 14px; font-size:14px'><b>Restwaarde-risico</b></td><td style='padding:10px 14px; text-align:right; font-size:14px'>jouw probleem</td><td style='padding:10px 14px; text-align:right; font-size:14px'><b>BotLease draagt</b></td></tr>"
             "</tbody></table>"
             "<p>Totaal over 3 jaar: zelf kopen kost <b>€37.700-€42.700</b>, lease via BotLease kost <b>€46.620</b>. Verschil: ~€4.000-€9.000 over 3 jaar. Voor dat geld krijg je het volledige risico-traject afgevangen.</p>"),
            ("Wanneer kopen wél de juiste keuze is",
             "<ul style='line-height:1.75'>"
             "<li><b>Je hebt een 5+ jaar roadmap.</b> Voor R&D-labs of universiteiten die de robot meerdere jaren op één model willen blijven. Lease loopt 36 mnd; daarna gaat een nieuwe generatie weer in lease.</li>"
             "<li><b>Capex-budget is geen issue.</b> Voor bedrijven met cash op de balans en geen drempel om kapitaal vast te leggen.</li>"
             "<li><b>Je hebt eigen onderhouds-stack.</b> Met interne robotica-ingenieurs die elders al werken aan AGV's of cobots - dan is de eigen service-laag goedkoper dan via lease.</li>"
             "<li><b>De use-case is statisch.</b> Je weet zeker dat dit model 36+ maanden blijft passen, zonder pivot naar zwaardere/lichtere taken.</li>"
             "</ul>"),
            ("Wanneer leasen wint",
             "<ul style='line-height:1.75'>"
             "<li><b>MKB met cashflow-discipline.</b> €1.295/mnd is voorspelbaar - €23k aanschaf in één keer is een raid op de werkkapitaal-buffer.</li>"
             "<li><b>Onzekere ROI.</b> Pilot 4 weken voor €1.500, dan beslissen. Bij koop is het allemaal of niets.</li>"
             "<li><b>EU AI-Act compliance is een onbekend traject voor jouw bedrijf.</b> BotLease regelt het, jij hoeft geen ISO-13482 expert in te huren.</li>"
             "<li><b>Tech moves fast.</b> Een €23k robot van 2026 is in 2029 mogelijk €8k waard. Lease drukt dat restwaarde-risico naar BotLease.</li>"
             "<li><b>Geen continue operatie.</b> Als de robot 30 uur per week werkt i.p.v. 24/7, betaal je via lease alleen voor wat je gebruikt. Bij koop staat een €23k asset half stil.</li>"
             "</ul>"),
            ("Hybride: koop + service-contract",
             "<p>Een derde route die we soms zien: klant koopt de robot zelf en sluit een aparte service-overeenkomst af voor onderhoud, swap-SLA en compliance. Voor sommige klanten financieel optimaal. <b>BotLease biedt dit op aanvraag</b> - schikt vooral voor klanten met 5+ units die hun eigen ops-team willen behouden.</p>"),
            ("Welke modellen leasen, welke kopen",
             "<ul style='line-height:1.75'>"
             "<li><b>Sterk lease-case:</b> Unitree G1, NEURA 4NE-1 Mini, EngineAI SE01 - relatief snel verouderend, restwaarde valt hard.</li>"
             "<li><b>Sterk koop-case:</b> Pollen Reachy 2 - EU-gebouwd, stabiel platform met lange supporthistorie. </li>"
             "<li><b>Alleen lease (te onzeker voor koop):</b> Apptronik Apollo, Figure 02 - wachtlijst, prijs nog niet stabiel.</li>"
             "</ul>"
             "<p>Voor specifiek advies per situatie: <a href='/kosten'>gebruik onze kosten-calculator</a> of plan een intake.</p>"),
        ],
        faqs=[
            {"q": "Is leasen altijd duurder dan kopen?", "a": "Op de directe aanschafprijs ja, maar over 3 jaar volledig kostenbeeld inclusief installatie, onderhoud, verzekering, swap-SLA en EU AI-Act compliance is het verschil typisch 10-25% - niet 100%."},
            {"q": "Kan ik de robot na 36 maanden lease overnemen?", "a": "Ja. Aan het einde van de leasetermijn kun je de unit overnemen tegen restwaarde (typisch 20-30% van aanschafprijs). Wij geven 60 dagen voor einde lease een vast overnamebod."},
            {"q": "Wat als de robot binnen het leasecontract obsoleet wordt?", "a": "BotLease draagt dat risico. Per maand 13 kun je elke maand opzeggen, of upgraden naar een nieuwer model. Bij koop zit je aan een afschrijvend asset vast."},
            {"q": "Kan ik leasen fiscaal aftrekken?", "a": "Operational lease zit volledig in de OPEX en is direct aftrekbaar. Koop wordt geactiveerd en jaarlijks afgeschreven (5-7 jaar). Operationeel resultaat ziet er bij lease cleaner uit - KIA en investeringsaftrek kunnen bij koop voordeel geven, vraag je accountant."},
            {"q": "Heeft BotLease een lease-of-koop calculator?", "a": "Ja, op /kosten kun je per model je kostenscenario over 36 maanden simuleren. Reken zelf na - wij geven geen marketing-getallen."},
        ],
    )
    (vergelijken / "lease-vs-koop.html").write_text(_fmt_nl(lease_vs_koop), encoding="utf-8")

    humanoid_vs_cobot = render_decision_page(
        slug="humanoid-vs-cobot",
        title="Humanoïde robot vs cobot: wanneer welke kiezen? | BotLease",
        h1="Humanoïde robot vs cobot",
        meta_desc="Humanoïde robot vs cobot: wanneer kies je welke? Verschillen in capex, flexibiliteit, payload en use-cases - voor het Nederlandse MKB uitgelegd.",
        intro="Universal Robots vs Unitree G1. €25k cobot vs €25k humanoid. Het is geen vervanging - het zijn twee oplossingen voor verschillende problemen.",
        sections=[
            ("Het verschil in één zin",
             "<p>Een <b>cobot</b> (collaborative robot, denk Universal Robots UR5 of OMRON TM) is een vaste robotarm op een tafel of vloer-mount. Een <b>humanoïde robot</b> (denk Unitree G1, NEURA 4NE-1) is een mobiele tweebenige robot met armen die in een menselijke omgeving werkt zoals een mens dat zou doen.</p>"
             "<p>Cobot = wás gewoon \"robot-arm\", aangepast om naast mensen te werken. Humanoid = volledig nieuwe vorm, ontworpen om in jouw bestaande mensen-werkruimte te functioneren.</p>"),
            ("Wanneer kies je een cobot",
             "<ul style='line-height:1.75'>"
             "<li><b>Vaste taak, vaste plek.</b> Pick-and-place bij dezelfde lopende band, soldeerwerk aan dezelfde productlijn, schroeven aan hetzelfde frame. Een cobot blinkt uit in herhaaldelijk identiek werk.</li>"
             "<li><b>Hoge precisie, zware payload.</b> Een UR20 tilt 20 kg met 0,05mm precisie. Een Unitree G1 tilt 3 kg, met menselijke (niet sub-millimeter) precisie.</li>"
             "<li><b>24/7 operatie.</b> Cobots hebben geen batterij - stroom-aansluiting, draaien continu. Humanoids draaien typisch 2-4 uur per laadbeurt.</li>"
             "<li><b>Lager prijspunt.</b> UR3e cobot vanaf €27.000 koop, €450/mnd lease via UR Financial Services × DLL. Humanoids beginnen bij €290/mnd (R1) en zijn typisch €1.295-€6.650/mnd.</li>"
             "<li><b>Bewezen ROI-modellen.</b> Cobots staan al 10 jaar in productie. Voor één-taak workflows zijn de ROI-berekeningen bekend en betrouwbaar.</li>"
             "</ul>"),
            ("Wanneer kies je een humanoïde robot",
             "<ul style='line-height:1.75'>"
             "<li><b>Variabele taken, variabele plekken.</b> Een humanoid loopt naar de volgende werkstation, ruimt op tussen taken, doet een ronde door het magazijn. Cobots zijn vastgemonteerd.</li>"
             "<li><b>Bestaande werkomgeving zonder aanpassingen.</b> Cobots hebben kooi/zone-vereisten en moeten gemount worden. Een humanoid loopt door je magazijn alsof er een uitzendkracht bij is.</li>"
             "<li><b>Front-of-house / klant-interactie.</b> Humanoids kunnen klanten begroeten, rondleiden, ondersteunen. Geen klant accepteert een robotarm aan de receptie.</li>"
             "<li><b>Tote-handling, decanting, mobile manipulation.</b> Vandaag GXO's domein met Agility Digit. Een cobot kan niet 100m verderop een tote oppakken.</li>"
             "<li><b>Snelle herinzet.</b> Vandaag receptie, morgen pakhuis-inspectie, overmorgen demo op de beurs. Een cobot blijft staan.</li>"
             "</ul>"),
            ("Cobot + humanoid samen - het beste van twee werelden",
             "<p>De toekomst is geen of/of. Toonaangevende NL-deployments combineren beide: cobot voor de gespecialiseerde precisietaak, humanoid voor het flexibele logistieke werk eromheen. Voorbeeld: cobot op de assemblage-tafel, humanoid die parts aanvoert naar de cobot en eindproducten wegbrengt.</p>"
             "<p>BotLease werkt samen met cobot-leveranciers waar dat past - geen exclusieve binding aan humanoids. Bij een intake bespreken we eerlijk welke combinatie werkt.</p>"),
            ("Concrete vergelijking - €900/mnd budget",
             "<table style='width:100%; border-collapse:collapse; margin:18px 0; background:var(--bg-card); border:1px solid var(--border); border-radius:10px; overflow:hidden'>"
             "<thead><tr style='background:var(--bg-2)'><th style='padding:11px 14px; text-align:left; font-size:11.5px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.06em'>Aspect</th><th style='padding:11px 14px; text-align:left; font-size:11.5px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.06em'>UR5e cobot (~€700/mnd)</th><th style='padding:11px 14px; text-align:left; font-size:11.5px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.06em'>Unitree G1 humanoid (€1.295/mnd)</th></tr></thead>"
             "<tbody>"
             "<tr><td style='padding:10px 14px; border-bottom:1px solid var(--border); font-size:14px'>Mobiliteit</td><td style='padding:10px 14px; border-bottom:1px solid var(--border); font-size:14px'>Statisch</td><td style='padding:10px 14px; border-bottom:1px solid var(--border); font-size:14px'>Loopt 2 m/s</td></tr>"
             "<tr><td style='padding:10px 14px; border-bottom:1px solid var(--border); font-size:14px'>Payload</td><td style='padding:10px 14px; border-bottom:1px solid var(--border); font-size:14px'>5 kg, sub-mm precisie</td><td style='padding:10px 14px; border-bottom:1px solid var(--border); font-size:14px'>3 kg, menselijke precisie</td></tr>"
             "<tr><td style='padding:10px 14px; border-bottom:1px solid var(--border); font-size:14px'>Werktijd per dag</td><td style='padding:10px 14px; border-bottom:1px solid var(--border); font-size:14px'>24/7 via netstroom</td><td style='padding:10px 14px; border-bottom:1px solid var(--border); font-size:14px'>~4 uur, dan opladen</td></tr>"
             "<tr><td style='padding:10px 14px; border-bottom:1px solid var(--border); font-size:14px'>Installatie</td><td style='padding:10px 14px; border-bottom:1px solid var(--border); font-size:14px'>Vaste mount, kooi/zone</td><td style='padding:10px 14px; border-bottom:1px solid var(--border); font-size:14px'>Plug-and-play, geen aanpassing werkvloer</td></tr>"
             "<tr><td style='padding:10px 14px; font-size:14px'>Sterkste use-case</td><td style='padding:10px 14px; font-size:14px'>Repetitieve precisie op één plek</td><td style='padding:10px 14px; font-size:14px'>Variabel werk, mobile manipulation</td></tr>"
             "</tbody></table>"),
        ],
        faqs=[
            {"q": "Kan een humanoïde robot een cobot vervangen?", "a": "Voor de meeste industriële precisietaken (laser-snijden, soldeer, schroef met sub-mm tolerantie): nee. Voor flexibele mobile manipulation (tote-handling, klantontvangst, ronde door magazijn): ja, vaak beter."},
            {"q": "Welke is goedkoper, cobot of humanoid?", "a": "Vergelijkbaar prijspunt: UR3e/UR5e zit op €600-€900/mnd, instap humanoids zoals Unitree G1 op €1.295/mnd. Hoog-payload industriele humanoids (NEURA Gen 3.5 €5.950/mnd) zitten ver boven elke cobot. Cobots blijven veelal goedkoper bij gelijkwaardige output."},
            {"q": "Welke is veiliger?", "a": "Cobots zijn ouder en hebben langere safety-certification track-record (ISO 10218, ISO/TS 15066). Humanoids vallen onder EN ISO 13482 (mobile servant robots) en moeten extra werkzone-management hebben. Beide werken veilig naast mensen mits goed gedefinieerd."},
            {"q": "Welke is toekomstvaster?", "a": "Humanoids leren sneller via Vision-Language-Action AI (Helix, Neuraverse, GR00T). Een cobot van 2026 kan in 2030 nog steeds hetzelfde. Een humanoid van 2026 zou in 2030 véél meer kunnen via software-updates. Maar de hardware is ook minder gerijpt - meer onderdelenrisico."},
            {"q": "Adviseert BotLease ook cobots?", "a": "Onze hoofd-catalogus is humanoid, maar in onze intake adviseren we eerlijk wanneer een cobot beter past. We hebben een partner-netwerk waar we naar verwijzen - geen verkoop-druk op humanoid wanneer dat geen zin heeft."},
        ],
    )
    (vergelijken / "humanoid-vs-cobot.html").write_text(_fmt_nl(humanoid_vs_cobot), encoding="utf-8")

    print(f"✅ Built guides: pillar, AI-Act, glossary, about, methodology, costs, /gids/ hub, /vergelijken/ hub + {len(head_to_heads)} head-to-head pages + 2 decision pages")


if __name__ == "__main__":
    build()
