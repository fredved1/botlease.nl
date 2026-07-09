#!/usr/bin/env python3
"""
Generates sector landing pages (/sectoren/<slug>) and city landing pages (/leasen/<slug>).
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
from landingpages_data import SECTORS, CITIES  # noqa: E402
from robots_data import by_slug  # noqa: E402
from seo_common import HEAD_SEO, trim_desc  # noqa: E402
from style_base import BASE_CSS, NAV_HTML, FOOTER_HTML  # noqa: E402

PAGE_CSS = BASE_CSS + """
.eyebrow {
  display:inline-block; color:var(--accent); font-size:12.5px;
  text-transform:uppercase; letter-spacing:0.12em; font-weight:600;
  margin-bottom:16px;
}

.lp-hero { padding:80px 0 30px; }
@media (min-width:768px) { .lp-hero { padding:110px 0 40px; } }
.lp-hero h1 {
  font-family:'Inter', -apple-system, sans-serif; font-weight:700;
  font-size:clamp(36px, 5vw, 60px);
  margin-bottom:18px; letter-spacing:-0.035em; line-height:1.06;
}
.lp-hero .tag { color:var(--accent); font-size:19px; margin-bottom:24px; max-width:680px; line-height:1.4; }
.lp-hero p.intro { color:var(--ink-2); font-size:17px; max-width:760px; line-height:1.65; }

.metrics-strip {
  background:var(--bg-2);
  border-top:1px solid var(--border); border-bottom:1px solid var(--border);
  padding:40px 0; margin-top:48px;
}
.metrics { display:grid; grid-template-columns:repeat(2,1fr); gap:24px; }
@media (min-width:768px) { .metrics { grid-template-columns:repeat(4,1fr); } }
.metric { display:flex; flex-direction:column; gap:6px; }
.metric .v {
  font-family:'Inter', -apple-system, sans-serif; font-weight:700;
  font-size:32px; letter-spacing:-0.025em; color:var(--accent);
  line-height:1;
}
.metric .l { font-size:12.5px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.1em; font-weight:500; }

section.body { padding:80px 0; }
section.body h2 {
  font-family:'Inter', -apple-system, sans-serif; font-weight:700;
  font-size:clamp(24px, 2.8vw, 36px);
  margin-bottom:14px; letter-spacing:-0.025em; line-height:1.15;
}
section.body p { color:var(--ink); font-size:17px; line-height:1.78; margin-bottom:18px; }
section.body .sub { margin-bottom:48px; }
section.body .sub:last-child { margin-bottom:0; }

.r-strip {
  background:var(--bg-2);
  border-top:1px solid var(--border); border-bottom:1px solid var(--border);
}
.r-grid { display:grid; grid-template-columns:1fr; gap:18px; }
@media (min-width:560px) { .r-grid { grid-template-columns:repeat(2,1fr); } }
@media (min-width:880px) { .r-grid { grid-template-columns:repeat(4,1fr); } }
.r-card {
  background:var(--bg-card); border:1px solid var(--border);
  border-radius:14px; overflow:hidden;
  transition:transform .2s, border-color .2s, box-shadow .2s;
  display:flex; flex-direction:column; color:inherit;
}
.r-card:hover { transform:translateY(-2px); border-color:var(--border-hover); box-shadow:var(--shadow-sm); }
.r-thumb {
  aspect-ratio:4/3;
  background:linear-gradient(180deg, var(--bg-2) 0%, var(--bg-card) 100%);
  position:relative; display:flex; align-items:center; justify-content:center;
  overflow:hidden; border-bottom:1px solid var(--border);
}
.r-thumb img {
  max-height:78%; max-width:72%; width:auto; height:auto;
  object-fit:contain; filter:drop-shadow(0 10px 20px rgba(28,25,23,0.15));
}
.r-body { padding:16px 18px 18px; flex:1; display:flex; flex-direction:column; }
.r-body .v { font-size:11px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.1em; font-weight:600; margin-bottom:4px; }
.r-body h4 { font-family:'Inter'; font-weight:600; font-size:16px; margin-bottom:8px; color:var(--ink); }
.r-body .p { font-family:'Inter'; color:var(--accent); font-size:14px; font-weight:600; margin-top:auto; padding-top:10px; }

.qa { padding:80px 0; }
.qa-item {
  padding:24px; border:1px solid var(--border); border-radius:14px;
  margin-bottom:14px; background:var(--bg-card);
}
.qa-item h4 { font-family:'Inter'; font-weight:600; font-size:18px; margin-bottom:10px; color:var(--ink); letter-spacing:-0.015em; }
.qa-item p { color:var(--ink-2); font-size:15.5px; line-height:1.7; }

.cta-strip {
  padding:48px; background:var(--bg-dark); color:var(--ink-on-dark);
  border-radius:20px; text-align:center; margin:60px 0 100px;
}
.cta-strip h3 {
  font-family:'Inter', -apple-system, sans-serif; font-weight:700;
  font-size:28px; margin-bottom:10px; color:var(--ink-on-dark);
}
.cta-strip p { color:var(--ink-2-on-dark); margin-bottom:24px; font-size:16px; }
.cta-strip .btn { background:var(--accent); color:#fff; border-color:var(--accent); }
.cta-strip .btn:hover { background:#fff; color:var(--ink); border-color:#fff; }
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
    "description": "Nederlands eerste full-service leasemaatschappij voor humanoïde robots. All-in operational lease vanaf €290 per maand: gebruiksklare oplevering, onderhoud, vervangende unit bij storing en compliance-documentatie.",
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


def robot_card(slug: str) -> str:
    r = by_slug(slug)
    if not r:
        return ""
    return f"""<a href="/robots/{r['slug']}" class="r-card">
        <div class="r-thumb"><img src="{r['photo']}" alt="{escape(r['name'])} robot" loading="lazy"></div>
        <div class="r-body">
          <span class="v">{escape(r['vendor'])} · {escape(r['vendor_country'])}</span>
          <h4>{escape(r['name'])}</h4>
          <span class="p">€{r['lease_eur']:,}/mnd</span>
        </div>
      </a>"""


def render_sector(s: dict) -> str:
    metrics_html = "".join(f'<div class="metric"><span class="v">{escape(v)}</span><span class="l">{escape(l)}</span></div>' for v, l in s["metrics"])
    sub_html = "".join(f'<div class="sub"><h2>{escape(sub["h"])}</h2><p>{escape(sub["body"])}</p></div>' for sub in s["subsections"])
    robots_html = "".join(robot_card(slug) for slug in s["recommended_robots"])
    qa_html = "".join(f'<div class="qa-item"><h4>{escape(q)}</h4><p>{escape(a)}</p></div>' for q, a in s["questions"])

    title = f"{s['title_kw']} - vanaf €290/mnd | BotLease"
    desc = f"{s['name']} met humanoïde robots: ROI, robotmodellen, regelgeving. {s['tagline']} BotLease verzorgt all-in lease vanaf €290/maand."

    qa_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["questions"]],
    }, ensure_ascii=False)

    # Service schema per sector - vertelt Google waar deze pagina precies over gaat
    service_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": f"Humanoïde robot lease voor {s['name']}",
        "provider": {"@type": "Organization", "name": "BotLease", "url": SITE_URL},
        "areaServed": {"@type": "Country", "name": "Nederland"},
        "description": s["tagline"],
        "url": f"{SITE_URL}/sectoren/{s['slug']}",
        "offers": {
            "@type": "Offer",
            "priceCurrency": "EUR",
            "priceSpecification": {"@type": "UnitPriceSpecification", "priceCurrency": "EUR", "billingDuration": "P1M", "minPrice": "290", "maxPrice": "4890"},
        },
    }, ensure_ascii=False)

    bc_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Sectoren", "item": f"{SITE_URL}/sectoren/"},
            {"@type": "ListItem", "position": 3, "name": s["name"], "item": f"{SITE_URL}/sectoren/{s['slug']}"},
        ],
    }, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)}</title>
<meta name="description" content="{escape(trim_desc(desc))}">
<meta name="keywords" content="{escape(s['name'])} robot, humanoide robot {escape(s['name'])}, robot leasen {escape(s['name'])}, humanoid {escape(s['name'])} Nederland">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/sectoren/{s['slug']}">

<meta property="og:type" content="website">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(s['tagline'])}">
<meta property="og:url" content="{SITE_URL}/sectoren/{s['slug']}">
<meta property="og:image" content="{SITE_URL}/img/robots/apollo.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE_URL}/img/robots/apollo.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{qa_jsonld}</script>
<script type="application/ld+json">{bc_jsonld}</script>
<script type="application/ld+json">{service_jsonld}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
{HEAD_SEO}
</head>
<body>
{NAV_HTML}

<section class="lp-hero">
  <div class="container">
    <nav class="crumbs"><a href="/">Home</a> / <a href="/sectoren/">Sectoren</a> / <span>{escape(s['name'])}</span></nav>
    <span class="eyebrow">Sector - {escape(s['name'])}</span>
    <h1>{escape(s['h1'])}</h1>
    <p class="tag">{escape(s['tagline'])}</p>
    <p class="intro">{escape(s['intro'])}</p>
  </div>
</section>

<div class="metrics-strip">
  <div class="container">
    <div class="metrics">{metrics_html}</div>
  </div>
</div>

<section class="body">
  <div class="container">
    <div style="max-width:760px">{sub_html}</div>
  </div>
</section>

<section class="body r-strip">
  <div class="container">
    <span class="eyebrow">Aanbevolen modellen</span>
    <h2 style="margin:14px 0 32px">Robots voor {escape(s['name'].lower())}.</h2>
    <div class="r-grid">{robots_html}</div>
  </div>
</section>

<section class="qa">
  <div class="container">
    <span class="eyebrow">Veelgestelde vragen</span>
    <h2 style="margin:14px 0 32px">Praktische vragen, eerlijke antwoorden.</h2>
    <div style="max-width:820px">{qa_html}</div>
    <div class="cta-strip">
      <h3>Klaar voor een pilot in {escape(s['name'].lower())}?</h3>
      <p>Gratis intake op locatie · 4-weken pilot voor €1.500 · beslis na de pilot</p>
      <a class="btn" href="/#contact">Plan een demo →</a>
    </div>
  </div>
</section>

{FOOTER_HTML}
</body>
</html>
"""


_CITY_LINKS = {"amsterdam": "Amsterdam", "den-haag": "Den Haag", "eindhoven": "Eindhoven",
               "noord-brabant": "Noord-Brabant", "rotterdam": "Rotterdam", "utrecht": "Utrecht"}


def render_city(c: dict) -> str:
    _other_cities = " · ".join(f'<a href="/leasen/{s}" style="color:var(--accent)">{n}</a>'
                               for s, n in _CITY_LINKS.items() if s != c.get("slug"))
    sectors_html = "".join(
        f'<a href="/sectoren/{slug}" style="display:inline-block; margin:0 8px 8px 0; padding:8px 14px; '
        f'background:var(--bg-3); border:1px solid var(--line); border-radius:999px; font-size:13px; color:var(--ink-2)">'
        f'{escape(next(s["name"] for s in SECTORS if s["slug"] == slug))} →</a>'
        for slug in c["sectors_in_focus"]
    )

    # Get 4 recommended robots from the city's sectors
    rec_slugs = []
    for sec_slug in c["sectors_in_focus"]:
        sec = next((s for s in SECTORS if s["slug"] == sec_slug), None)
        if sec:
            for rs in sec["recommended_robots"]:
                if rs not in rec_slugs:
                    rec_slugs.append(rs)
    rec_slugs = rec_slugs[:4]
    robots_html = "".join(robot_card(slug) for slug in rec_slugs)

    title = f"{c['title_kw']} - vanaf €290/mnd | BotLease"
    desc = f"Humanoïde robots leasen in {c['name']}. All-in operational lease vanaf €290/maand. Levering en pilot binnen 5 werkdagen. {c['intro'][:80]}"

    # Lokale industrie/postcodes per stad
    LOCAL_AREAS = {
        "amsterdam": [
            ("Westpoort / Sloterdijk", "1043-1046", "Distrifulfillment, e-commerce warehouses, expeditie"),
            ("Zuidoost / Amstel Business Park", "1101-1108", "Datacenters, tech hoofdkantoren, last-mile fulfillment"),
            ("Schiphol-corridor", "1118-1119", "Air freight, koeriers, time-critical 3PL"),
            ("Centrum / Vondelpark cluster", "1011-1077", "5-sterren hotels, hospitality, luxe retail"),
        ],
        "rotterdam": [
            ("Maasvlakte / Distripark", "3199-3199", "Container handling, mega-warehouses, cross-dock"),
            ("Botlek / petrochemie", "3197-3198", "Industriële inspectie, materiaalhandling"),
            ("Eemhaven / Waalhaven", "3088-3089", "Multi-tenant 3PL, decanting, sortering"),
            ("Drechtsteden (Damen, Boskalis)", "3300-3357", "Maritieme assemblage, kitting"),
        ],
        "eindhoven": [
            ("Brainport campus", "5612-5658", "ASML, NXP, Philips R&D"),
            ("Helmond automotive", "5701-5708", "VDL Nedcar toelevering, assemblage"),
            ("Veldhoven semicon", "5500-5509", "Cleanroom-aanvullingen, parts-handling"),
            ("Best logistiek cluster", "5681-5683", "Bakkerij/foodlogistiek warehouses"),
        ],
        "utrecht": [
            ("UMC Utrecht / De Uithof", "3584-3585", "Universitair medisch centrum, R&D zorg"),
            ("Lage Weide", "3542-3544", "Tote-handling 3PL, e-fulfillment"),
            ("Nieuwegein / Houten zorg", "3433-3994", "Zorginstellingen, verpleeghuizen"),
            ("Papendorp tech-cluster", "3528-3528", "Tech HQ, sociale R&D"),
        ],
        "den-haag": [
            ("Scheveningen hospitality", "2581-2587", "Hotels Kurhaus, Steigenberger, lobby-host"),
            ("Bleizo / Rijswijk", "2280-2289", "3PL, e-fulfillment grotere magazijnen"),
            ("Government cluster Bezuidenhout", "2594-2595", "Defensie, ministeries - EU-only modellen"),
            ("Westland (kassen)", "2675-2685", "Agro robotics, pluk-pilots"),
        ],
    }
    local_areas = LOCAL_AREAS.get(c["slug"], [])
    areas_html = "".join(
        f'<tr><td style="padding:11px 14px; font-weight:600; color:var(--ink); font-size:14px; border-bottom:1px solid var(--border)">{escape(name)}</td>'
        f'<td style="padding:11px 14px; color:var(--ink-2); font-size:13.5px; border-bottom:1px solid var(--border); font-family:\'Inter\', sans-serif; font-variant-numeric:tabular-nums">{escape(pc)}</td>'
        f'<td style="padding:11px 14px; color:var(--ink-2); font-size:13.5px; border-bottom:1px solid var(--border)">{escape(use)}</td></tr>'
        for name, pc, use in local_areas
    )

    # City-specifieke FAQ
    city_faqs = [
        {
            "q": f"Hoe snel kan BotLease een humanoïde robot leveren in {c['name']}?",
            "a": f"In {c['name']} ligt onze gemiddelde levertijd op pilots op 5 werkdagen na ondertekend contract - gebruiksklaar opgeleverd. Voor productieve lease-deployments rekenen we op 6-10 weken vanaf fabrikant tot operationeel.",
        },
        {
            "q": f"Welke sectoren in {c['name']} zetten humanoïde robots in?",
            "a": f"In {c['name']} zien wij de meeste interesse vanuit {', '.join(slug.replace('-', ' & ') for slug in c['sectors_in_focus'])}. Specifieke clusters in deze regio: {', '.join(name for name, _, _ in local_areas[:3])}.",
        },
        {
            "q": f"Werkt BotLease in {c['name']} met lokale onderhouds-partners?",
            "a": f"Ja. Bij een storing regelen we een vervangende unit, doorgaans binnen enkele werkdagen. Voor {c['name']} en omgeving loopt reparatie via de leverancier.",
        },
        {
            "q": f"Voldoen humanoïde robots in {c['name']} aan de EU AI-Act?",
            "a": f"Ja. BotLease regelt voor elke deployment in {c['name']} de importeurs- en CE-conformiteitskant onder de Machineverordening 2023/1230 (documentatie van de fabrikant verzamelen en controleren). Voor government / defensie-toepassingen in {c['name']} (relevant in regio Den Haag) zetten wij uitsluitend EU-gebouwde modellen in (NEURA, Pollen).",
        },
        {
            "q": f"Hoeveel kost een humanoïde robot leasen in {c['name']}?",
            "a": f"Hetzelfde tarief als in heel Nederland: vanaf €290/mnd voor het Unitree R1 instapmodel, oplopend tot €6.650/mnd voor industriële flagships. Alle prijzen zijn publiek op botlease.nl/robots en bevatten gebruiksklare oplevering, onderhoud, een vervangende unit bij storing, WA-verzekering per inzet en Nederlandstalige helpdesk.",
        },
    ]
    city_faq_html = "".join(
        f'<details style="border-top:1px solid var(--border); padding:0"><summary style="cursor:pointer; list-style:none; padding:16px 4px; font-size:16px; font-weight:500; color:var(--ink); display:flex; justify-content:space-between; gap:20px">{escape(f["q"])}<span style="color:var(--ink-3); font-size:20px; font-weight:300">+</span></summary><p style="padding:0 4px 18px; font-size:15px; line-height:1.65; color:var(--ink-2)">{escape(f["a"])}</p></details>'
        for f in city_faqs
    )
    faq_jsonld_city = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
            for f in city_faqs
        ],
    }, ensure_ascii=False)

    bc_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Leasen", "item": f"{SITE_URL}/leasen/"},
            {"@type": "ListItem", "position": 3, "name": c["name"], "item": f"{SITE_URL}/leasen/{c['slug']}"},
        ],
    }, ensure_ascii=False)

    # LocalBusiness schema per stad - geeft kans op Google Local Pack
    local_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": f"BotLease - Humanoïde robot leasen {c['name']}",
        "image": f"{SITE_URL}/img/robots/apollo-norm.webp",
        "url": f"{SITE_URL}/leasen/{c['slug']}",
        "email": "hallo@botlease.nl",
        "priceRange": "€290 - €6.650 per maand",
        "address": {"@type": "PostalAddress", "addressLocality": "Amsterdam", "addressRegion": "Noord-Holland", "addressCountry": "NL"},
        "areaServed": [
            {"@type": "City", "name": c["name"]},
            {"@type": "Country", "name": "Nederland"},
        ],
        "serviceType": "Operational lease van humanoïde robots",
        "description": f"All-in operational lease van humanoïde robots in {c['name']} en omgeving - gebruiksklare oplevering, onderhoud, swap-SLA en EU AI-Act compliance inbegrepen.",
    }, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)}</title>
<meta name="description" content="{escape(trim_desc(desc))}">
<meta name="keywords" content="humanoide robot leasen {escape(c['name'])}, robot huren {escape(c['name'])}, humanoid robot {escape(c['name'])}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/leasen/{c['slug']}">

<meta property="og:type" content="website">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc[:160])}">
<meta property="og:url" content="{SITE_URL}/leasen/{c['slug']}">
<meta property="og:image" content="{SITE_URL}/img/robots/apollo.png">
<meta name="twitter:card" content="summary_large_image">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{bc_jsonld}</script>
<script type="application/ld+json">{local_jsonld}</script>
<script type="application/ld+json">{faq_jsonld_city}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
{HEAD_SEO}
</head>
<body>
{NAV_HTML}

<section class="lp-hero">
  <div class="container">
    <nav class="crumbs"><a href="/">Home</a> / <a href="/leasen/">Leasen per stad</a> / <span>{escape(c['name'])}</span></nav>
    <span class="eyebrow">Regio - {escape(c['name'])}</span>
    <h1>Humanoïde robot leasen in {escape(c['name'])}.</h1>
    <p class="tag">All-in operational lease vanaf €290/maand. Levering binnen 5 werkdagen.</p>
    <p class="intro">{escape(c['intro'])}</p>
    <div style="margin-top:32px">
      <div style="font-size:12px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.12em; margin-bottom:12px; font-weight:600">Sectoren in {escape(c['name'])}</div>
      <div>{sectors_html}</div>
    </div>
  </div>
</section>

<section class="body">
  <div class="container">
    <div style="max-width:760px">
      <h2>Wat past in {escape(c['name'])}?</h2>
      <p>{escape(c['local_hooks'])}</p>
      <p>Vanaf BotLease Amsterdam leveren we humanoids op locatie binnen heel Nederland. Voor {escape(c['name'])} ligt onze gemiddelde respons-tijd op intake-aanvragen op 4 werkuren, en levering van pilot-units gemiddeld 5 werkdagen na ondertekening. Bij een storing regelen we een vervangende unit, doorgaans binnen enkele werkdagen.</p>
    </div>

    {f'''<div style="max-width:840px; margin-top:48px">
      <h2>Industriegebieden bediend in {escape(c['name'])} en omgeving</h2>
      <p style="color:var(--ink-2); font-size:15.5px; line-height:1.65; margin-bottom:18px">De vier sterkste clusters in regio {escape(c['name'])} waar wij momenteel actief zijn. Levering- en swap-SLA's gelden voor alle hier vermelde postcodes; daarbuiten op aanvraag.</p>
      <table style="width:100%; border-collapse:collapse; background:var(--bg-card); border:1px solid var(--border); border-radius:10px; overflow:hidden">
        <thead><tr style="background:var(--bg-2)">
          <th style="text-align:left; padding:11px 14px; font-size:11.5px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.06em; font-weight:600">Gebied</th>
          <th style="text-align:left; padding:11px 14px; font-size:11.5px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.06em; font-weight:600">Postcode</th>
          <th style="text-align:left; padding:11px 14px; font-size:11.5px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.06em; font-weight:600">Typische use-case</th>
        </tr></thead>
        <tbody>{areas_html}</tbody>
      </table>
    </div>''' if areas_html else ''}

    <div style="max-width:760px; margin-top:48px">
      <h2>Hoe een lease-traject in {escape(c['name'])} eruit ziet</h2>
      <ol style="color:var(--ink-2); font-size:15.5px; line-height:1.8; padding-left:22px">
        <li><b>Intake (week 0).</b> 30-min videogesprek of bezoek op locatie in {escape(c['name'])}. Wij beoordelen of de use-case past, welke 2-3 modellen kandidaat zijn, en wat de realistische ROI is.</li>
        <li><b>Pilot (week 1-4).</b> Vier weken proef met één unit op jouw werkvloer voor €1.500. Inclusief setup, training en wekelijkse check-in. Beslis daarna of het door gaat.</li>
        <li><b>Lease-contract (week 5-12).</b> 36-maands operational lease vanaf goedgekeurde levering. Setup-fee eenmalig, daarna maandelijks vast tarief, all-in.</li>
        <li><b>Operatie (maand 4-36).</b> Onderhoud, software-updates, swap-SLA en helpdesk via BotLease. Per maand opzegbaar vanaf maand 13.</li>
      </ol>
    </div>

    <div style="max-width:760px; margin-top:48px">
      <h2>Veelgestelde vragen - {escape(c['name'])}</h2>
      <div style="margin-top:12px">{city_faq_html}<div style="border-top:1px solid var(--border)"></div></div>
    </div>
  </div>
</section>

<section class="body r-strip">
  <div class="container">
    <span class="eyebrow">Aanbevolen modellen voor {escape(c['name'])}</span>
    <h2 style="margin:14px 0 32px">Robotmodellen die hier het meest gevraagd worden.</h2>
    <div class="r-grid">{robots_html}</div>
    <p style="margin-top:32px"><a href="/robots" style="color:var(--accent-2); text-decoration:underline">Bekijk alle 13 modellen in de volledige catalogus →</a></p>
  </div>
</section>

<section class="body">
  <div class="container">
    <div class="cta-strip">
      <h3>Pilot starten in {escape(c['name'])}?</h3>
      <p>Gratis intake op locatie · 4-weken pilot voor €1.500 · beslis na de pilot</p>
      <a class="btn" href="/#contact">Plan een demo →</a>
    </div>
  </div>
</section>

<section style="border-top:1px solid var(--line); padding:36px 0">
  <div class="container">
    <p style="color:var(--ink-2); font-size:14.5px"><b style="color:var(--ink)">Ook actief in:</b> {_other_cities} · <a href="/leasen" style="color:var(--accent)">alle regio's →</a></p>
  </div>
</section>

{FOOTER_HTML}
</body>
</html>
"""


def render_sectors_hub() -> str:
    cards = "".join(
        f'<a href="/sectoren/{s["slug"]}" class="r-card" style="aspect-ratio:auto">'
        f'<div class="r-body" style="padding:24px">'
        f'<span class="v">Sector</span>'
        f'<h4 style="font-size:19px; margin-bottom:10px">{escape(s["name"])}</h4>'
        f'<p style="color:var(--ink-2); font-size:13.5px; line-height:1.5">{escape(s["tagline"])}</p>'
        f'<span class="p" style="margin-top:14px">Bekijk →</span>'
        f'</div></a>'
        for s in SECTORS
    )
    return f"""<!DOCTYPE html>
<html lang="nl"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Humanoïde robots per sector | BotLease</title>
<meta name="description" content="Humanoïde robots per sector in Nederland - 3PL, productie, hospitality, zorg. ROI-data, aanbevolen modellen en regelgeving per sector.">
<link rel="canonical" href="{SITE_URL}/sectoren/">
<meta property="og:type" content="website">
<meta property="og:title" content="Humanoïde robots per sector | BotLease">
<meta property="og:url" content="{SITE_URL}/sectoren/">
<meta property="og:image" content="{SITE_URL}/img/robots/apollo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{ORG_SCHEMA}</script>
{HEAD_SEO}
</head><body>
{NAV_HTML}
<section class="lp-hero"><div class="container">
  <span class="eyebrow">Sectoren</span>
  <h1>Humanoïde robots per sector.</h1>
  <p class="tag">Per sector: realistische ROI, aanbevolen modellen, regelgeving en case-studies.</p>
</div></section>
<section class="body"><div class="container">
  <div class="r-grid" style="grid-template-columns:repeat(2,1fr)">{cards}</div>
</div></section>
{FOOTER_HTML}
</body></html>
"""


def render_cities_hub() -> str:
    cards = "".join(
        f'<a href="/leasen/{c["slug"]}" class="r-card" style="aspect-ratio:auto">'
        f'<div class="r-body" style="padding:24px">'
        f'<span class="v">Regio</span>'
        f'<h4 style="font-size:19px; margin-bottom:10px">{escape(c["name"])}</h4>'
        f'<p style="color:var(--ink-2); font-size:13.5px; line-height:1.5">{escape(c["intro"][:140])}…</p>'
        f'<span class="p" style="margin-top:14px">Bekijk →</span>'
        f'</div></a>'
        for c in CITIES
    )
    return f"""<!DOCTYPE html>
<html lang="nl"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Humanoïde robot leasen per regio | BotLease</title>
<meta name="description" content="Humanoïde robot leasen in de 5 grootste Nederlandse steden. Lokale levering, sectorspecifiek advies, intake binnen 1-2 werkdagen.">
<link rel="canonical" href="{SITE_URL}/leasen/">
<meta property="og:type" content="website">
<meta property="og:title" content="Humanoïde robot leasen per stad | BotLease">
<meta property="og:url" content="{SITE_URL}/leasen/">
<meta property="og:image" content="{SITE_URL}/img/robots/apollo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{ORG_SCHEMA}</script>
{HEAD_SEO}
</head><body>
{NAV_HTML}
<section class="lp-hero"><div class="container">
  <span class="eyebrow">Leasen per stad</span>
  <h1>Humanoïde robot leasen per stad.</h1>
  <p class="tag">Lokale levering, sectorspecifiek advies, intake binnen 1-2 werkdagen.</p>
</div></section>
<section class="body"><div class="container">
  <div class="r-grid" style="grid-template-columns:repeat(2,1fr)">{cards}</div>
</div></section>
{FOOTER_HTML}
</body></html>
"""


def build():
    sec_dir = FRONTEND / "sectoren"
    city_dir = FRONTEND / "leasen"
    sec_dir.mkdir(parents=True, exist_ok=True)
    city_dir.mkdir(parents=True, exist_ok=True)

    for s in SECTORS:
        (sec_dir / f"{s['slug']}.html").write_text(_fmt_nl(render_sector(s)), encoding="utf-8")
    (sec_dir / "index.html").write_text(_fmt_nl(render_sectors_hub()), encoding="utf-8")

    for c in CITIES:
        (city_dir / f"{c['slug']}.html").write_text(_fmt_nl(render_city(c)), encoding="utf-8")
    (city_dir / "index.html").write_text(_fmt_nl(render_cities_hub()), encoding="utf-8")

    print(f"✅ Built {len(SECTORS)} sectors + {len(CITIES)} cities + 2 hubs")


if __name__ == "__main__":
    build()
