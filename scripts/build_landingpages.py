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
from seo_common import HEAD_SEO  # noqa: E402
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
  font-family:'Fraunces', Georgia, serif; font-weight:500;
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
  font-family:'Fraunces', Georgia, serif; font-weight:500;
  font-size:32px; letter-spacing:-0.025em; color:var(--accent);
  line-height:1;
}
.metric .l { font-size:12.5px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.1em; font-weight:500; }

section.body { padding:80px 0; }
section.body h2 {
  font-family:'Fraunces', Georgia, serif; font-weight:500;
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
.r-body h4 { font-family:'Space Grotesk'; font-weight:600; font-size:16px; margin-bottom:8px; color:var(--ink); }
.r-body .p { font-family:'Space Grotesk'; color:var(--accent); font-size:14px; font-weight:600; margin-top:auto; padding-top:10px; }

.qa { padding:80px 0; }
.qa-item {
  padding:24px; border:1px solid var(--border); border-radius:14px;
  margin-bottom:14px; background:var(--bg-card);
}
.qa-item h4 { font-family:'Space Grotesk'; font-weight:600; font-size:18px; margin-bottom:10px; color:var(--ink); letter-spacing:-0.015em; }
.qa-item p { color:var(--ink-2); font-size:15.5px; line-height:1.7; }

.cta-strip {
  padding:48px; background:var(--bg-dark); color:var(--ink-on-dark);
  border-radius:20px; text-align:center; margin:60px 0 100px;
}
.cta-strip h3 {
  font-family:'Fraunces', Georgia, serif; font-weight:500;
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
    "name": "BotLease",
    "url": SITE_URL,
    "logo": f"{SITE_URL}/logo.png",
    "address": {"@type": "PostalAddress", "addressLocality": "Eindhoven", "addressCountry": "NL"},
}, ensure_ascii=False)


def _fmt_nl(html: str) -> str:
    """Convert digit-comma-digit (Python thousand separator) to digit-dot-digit (NL format).
    Does NOT touch CSS/JSON/JS commas."""
    import re
    return re.sub(r'(\d),(\d)', r'\1.\2', html)


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

    title = f"{s['title_kw']} — vanaf €890/mnd | BotLease"
    desc = f"{s['name']} met humanoïde robots: ROI, robotmodellen, regelgeving. {s['tagline']} BotLease verzorgt all-in lease vanaf €890/maand."

    qa_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["questions"]],
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
<meta name="description" content="{escape(desc)}">
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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{qa_jsonld}</script>
<script type="application/ld+json">{bc_jsonld}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
{HEAD_SEO}
</head>
<body>
{NAV_HTML}

<section class="lp-hero">
  <div class="container">
    <nav class="crumbs"><a href="/">Home</a> / <a href="/sectoren/">Sectoren</a> / <span>{escape(s['name'])}</span></nav>
    <span class="eyebrow">Sector — {escape(s['name'])}</span>
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


def render_city(c: dict) -> str:
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

    title = f"{c['title_kw']} — vanaf €290/mnd | BotLease"
    desc = f"Humanoïde robots leasen in {c['name']}. All-in operational lease vanaf €290/maand. Levering en pilot binnen 5 werkdagen. {c['intro'][:80]}"

    bc_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Leasen", "item": f"{SITE_URL}/leasen/"},
            {"@type": "ListItem", "position": 3, "name": c["name"], "item": f"{SITE_URL}/leasen/{c['slug']}"},
        ],
    }, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{bc_jsonld}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
{HEAD_SEO}
</head>
<body>
{NAV_HTML}

<section class="lp-hero">
  <div class="container">
    <nav class="crumbs"><a href="/">Home</a> / <a href="/leasen/">Leasen per stad</a> / <span>{escape(c['name'])}</span></nav>
    <span class="eyebrow">Regio — {escape(c['name'])}</span>
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
      <p>Vanaf BotLease HQ in Eindhoven leveren we humanoids op locatie binnen heel Nederland. Voor {escape(c['name'])} ligt onze gemiddelde respons-tijd op intake-aanvragen op 4 werkuren, en levering van pilot-units gemiddeld 5 werkdagen na ondertekening.</p>
    </div>
  </div>
</section>

<section class="body r-strip">
  <div class="container">
    <span class="eyebrow">Aanbevolen modellen voor {escape(c['name'])}</span>
    <h2 style="margin:14px 0 32px">Robotmodellen die hier het meest gevraagd worden.</h2>
    <div class="r-grid">{robots_html}</div>
    <p style="margin-top:32px"><a href="/robots" style="color:var(--accent-2); text-decoration:underline">Bekijk alle 15 modellen in de volledige catalogus →</a></p>
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
<title>Humanoïde robots per sector — 3PL, productie, hospitality, zorg | BotLease</title>
<meta name="description" content="Humanoïde robots per sector in Nederland: 3PL & fulfillment, productie & assemblage, hospitality & retail, zorg & instellingen. ROI-data, aanbevolen modellen en sectorspecifieke regelgeving.">
<link rel="canonical" href="{SITE_URL}/sectoren/">
<meta property="og:type" content="website">
<meta property="og:title" content="Humanoïde robots per sector | BotLease">
<meta property="og:url" content="{SITE_URL}/sectoren/">
<meta property="og:image" content="{SITE_URL}/img/robots/apollo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&display=swap" rel="stylesheet">
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
<title>Humanoïde robot leasen — Amsterdam, Rotterdam, Eindhoven, Utrecht, Den Haag | BotLease</title>
<meta name="description" content="Humanoïde robot leasen in de 5 grootste Nederlandse steden. Lokale levering, sectorspecifiek advies, intake binnen 4 werkuren.">
<link rel="canonical" href="{SITE_URL}/leasen/">
<meta property="og:type" content="website">
<meta property="og:title" content="Humanoïde robot leasen per stad | BotLease">
<meta property="og:url" content="{SITE_URL}/leasen/">
<meta property="og:image" content="{SITE_URL}/img/robots/apollo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{ORG_SCHEMA}</script>
{HEAD_SEO}
</head><body>
{NAV_HTML}
<section class="lp-hero"><div class="container">
  <span class="eyebrow">Leasen per stad</span>
  <h1>Humanoïde robot leasen per stad.</h1>
  <p class="tag">Lokale levering, sectorspecifiek advies, intake binnen 4 werkuren.</p>
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
        (sec_dir / f"{s['slug']}.html").write_text(render_sector(s), encoding="utf-8")
    (sec_dir / "index.html").write_text(render_sectors_hub(), encoding="utf-8")

    for c in CITIES:
        (city_dir / f"{c['slug']}.html").write_text(render_city(c), encoding="utf-8")
    (city_dir / "index.html").write_text(render_cities_hub(), encoding="utf-8")

    print(f"✅ Built {len(SECTORS)} sectors + {len(CITIES)} cities + 2 hubs")


if __name__ == "__main__":
    build()
