#!/usr/bin/env python3
"""
Generates:
- frontend/robots/<slug>.html       — per-robot landing page (long-tail SEO)
- frontend/robots/index.html        — overview / robots-hub
"""
from __future__ import annotations
import json
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"
ROBOT_DIR = FRONTEND / "robots"
SITE_URL = "https://botlease.nl"

sys.path.insert(0, str(ROOT / "scripts"))
from robots_data import ROBOTS, available_robots, waitlist_robots  # noqa: E402

PAGE_CSS = """
*,*::before,*::after { margin:0; padding:0; box-sizing:border-box; }
:root {
  --bg:#08080a; --bg-2:#0e0e12; --bg-3:#16161c; --line:#23232c; --line-2:#2e2e38;
  --ink:#f7f7f9; --ink-2:#a5a5b3; --ink-3:#666672;
  --accent:#ff5e1f; --accent-2:#ffb098; --green:#5be584; --eu:#5be584; --value:#ffc966; --premium:#a6cbff;
}
html { scroll-behavior:smooth; }
body { font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif; background:var(--bg); color:var(--ink); line-height:1.65; -webkit-font-smoothing:antialiased; }
h1,h2,h3,h4 { font-family:'Space Grotesk',sans-serif; letter-spacing:-0.025em; line-height:1.15; font-weight:600; }
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
.brand-mark { width:26px; height:26px; border-radius:8px; background:linear-gradient(135deg, #ff5e1f, #ff8e5c); display:flex; align-items:center; justify-content:center; box-shadow:0 0 20px rgba(255,94,31,0.35); }
.nav-links { display:flex; gap:30px; }
.nav-links a { color:var(--ink-2); font-size:14px; font-weight:500; transition:color .15s; }
.nav-links a:hover, .nav-links a.active { color:var(--ink); }
.btn { display:inline-flex; align-items:center; gap:7px; padding:11px 20px; border-radius:999px; font-weight:600; font-size:14px; background:var(--accent); color:#fff; border:none; cursor:pointer; transition:transform .15s, box-shadow .2s; }
.btn:hover { transform:translateY(-1px); box-shadow:0 12px 30px -10px rgba(255,94,31,0.35); }
.btn.ghost { background:transparent; border:1px solid var(--line-2); color:var(--ink); }

footer { padding:56px 0 36px; border-top:1px solid var(--line); background:var(--bg-2); margin-top:120px; }
footer .row { display:flex; justify-content:space-between; flex-wrap:wrap; gap:20px; color:var(--ink-3); font-size:13px; align-items:center; }
footer a { color:var(--ink-2); }
footer a:hover { color:var(--ink); }

@media (max-width:780px) { .nav-links { display:none; } }

.crumbs { display:flex; gap:8px; font-size:13px; color:var(--ink-3); margin-bottom:24px; }
.crumbs a:hover { color:var(--ink-2); }
.crumbs .sep { color:var(--line-2); }

.tier-badge { display:inline-block; padding:5px 12px; border-radius:999px; font-size:11px; font-weight:600; letter-spacing:0.1em; text-transform:uppercase; font-family:'Space Grotesk'; }
.tier-eu      { background:rgba(91,229,132,0.12); color:var(--eu); border:1px solid rgba(91,229,132,0.25); }
.tier-value   { background:rgba(255,201,102,0.12); color:var(--value); border:1px solid rgba(255,201,102,0.25); }
.tier-premium { background:rgba(166,203,255,0.12); color:var(--premium); border:1px solid rgba(166,203,255,0.25); }
"""

ROBOT_CSS = """
.r-hero { padding:140px 0 40px; position:relative; }
.r-hero::before { content:""; position:absolute; inset:0; background:radial-gradient(50% 50% at 75% 30%, rgba(255,94,31,0.14), transparent 60%); z-index:0; }
.r-hero .container { position:relative; z-index:2; }
.r-hero-grid { display:grid; grid-template-columns:1.2fr 1fr; gap:60px; align-items:center; }
.r-hero h1 { font-size:clamp(36px,4.6vw,58px); margin:14px 0 18px; letter-spacing:-0.035em; }
.r-hero .tag { color:var(--accent-2); font-size:18px; margin-bottom:24px; font-weight:500; }
.r-hero .lede { color:var(--ink-2); font-size:17px; margin-bottom:32px; max-width:560px; }
.r-hero .vendor { color:var(--ink-3); font-size:13px; text-transform:uppercase; letter-spacing:0.12em; font-weight:600; margin-bottom:8px; }
.r-hero-cta { display:flex; gap:12px; flex-wrap:wrap; margin-bottom:36px; }
.r-hero-art {
  background:linear-gradient(180deg, var(--bg-3) 0%, var(--bg-2) 100%);
  border:1px solid var(--line); border-radius:24px; padding:24px;
  display:flex; align-items:center; justify-content:center;
  aspect-ratio:4/5; position:relative; overflow:hidden;
  box-shadow:0 40px 80px -20px rgba(0,0,0,0.6);
}
.r-hero-art::before {
  content:""; position:absolute; inset:0;
  background:radial-gradient(50% 40% at 50% 50%, rgba(255,94,31,0.18), transparent 70%);
}
.r-hero-art img { max-height:88%; max-width:88%; width:auto; height:auto; object-fit:contain; position:relative; z-index:2; filter:drop-shadow(0 30px 60px rgba(0,0,0,0.6)); }
@media (max-width:880px) {
  .r-hero-grid { grid-template-columns:1fr; gap:32px; }
  .r-hero-art { aspect-ratio:5/4; max-width:520px; }
}

.r-quick { background:var(--bg-2); border-top:1px solid var(--line); border-bottom:1px solid var(--line); padding:32px 0; }
.r-quick-grid { display:grid; grid-template-columns:repeat(6,1fr); gap:20px; }
.r-quick-item { display:flex; flex-direction:column; gap:4px; }
.r-quick-item .v { font-family:'Space Grotesk'; font-size:22px; font-weight:600; letter-spacing:-0.02em; }
.r-quick-item .l { font-size:11.5px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.1em; font-weight:500; }
@media (max-width:880px) { .r-quick-grid { grid-template-columns:repeat(3,1fr); gap:16px; } }
@media (max-width:520px) { .r-quick-grid { grid-template-columns:repeat(2,1fr); } }

.section-eyebrow { display:inline-block; color:var(--accent); font-size:12px; text-transform:uppercase; letter-spacing:0.16em; font-weight:600; margin-bottom:14px; padding:5px 12px; background:rgba(255,94,31,0.08); border:1px solid rgba(255,94,31,0.2); border-radius:999px; }
section { padding:80px 0; }
section h2 { font-size:clamp(26px,3vw,40px); margin-bottom:16px; letter-spacing:-0.025em; }
section p.lede { color:var(--ink-2); font-size:17px; max-width:680px; margin-bottom:36px; }

.usecases-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:16px; }
.usecase-card { padding:24px; background:var(--bg-2); border:1px solid var(--line); border-radius:14px; }
.usecase-card .n { font-family:'Space Grotesk'; color:var(--accent); font-weight:700; font-size:14px; margin-bottom:8px; letter-spacing:0.08em; }
.usecase-card h4 { font-size:17px; margin-bottom:6px; }
.usecase-card p { color:var(--ink-2); font-size:14.5px; }
@media (max-width:780px) { .usecases-grid { grid-template-columns:1fr; } }

.spec-table { background:var(--bg-2); border:1px solid var(--line); border-radius:14px; overflow:hidden; }
.spec-row { display:grid; grid-template-columns:200px 1fr; gap:24px; padding:18px 24px; border-bottom:1px solid var(--line); }
.spec-row:last-child { border-bottom:none; }
.spec-row .k { color:var(--ink-3); font-size:13.5px; font-weight:500; text-transform:uppercase; letter-spacing:0.05em; }
.spec-row .v { color:var(--ink); font-size:15px; }
@media (max-width:580px) { .spec-row { grid-template-columns:1fr; gap:4px; padding:14px 18px; } }

.price-block { background:linear-gradient(135deg, var(--bg-2) 0%, var(--bg-3) 100%); border:1px solid var(--line-2); border-radius:18px; padding:36px; }
.price-row { display:flex; align-items:baseline; gap:8px; margin-bottom:10px; }
.price-row b { font-family:'Space Grotesk'; font-size:48px; font-weight:600; letter-spacing:-0.025em; }
.price-row .per { color:var(--ink-3); font-size:15px; }
.price-block .setup { color:var(--ink-2); font-size:14px; margin-bottom:18px; }
.price-block ul { list-style:none; padding:0; margin:18px 0 24px; }
.price-block li { color:var(--ink-2); font-size:14.5px; margin-bottom:8px; padding-left:22px; position:relative; }
.price-block li::before { content:"✓"; position:absolute; left:0; color:var(--green); font-weight:700; }

.compare-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }
.compare-card { padding:20px; background:var(--bg-2); border:1px solid var(--line); border-radius:12px; transition:border-color .2s, transform .2s; }
.compare-card:hover { border-color:var(--line-2); transform:translateY(-2px); }
.compare-card .vname { font-family:'Space Grotesk'; font-weight:600; font-size:17px; margin:6px 0 4px; }
.compare-card .vmeta { color:var(--ink-3); font-size:13px; margin-bottom:10px; }
.compare-card .vprice { font-family:'Space Grotesk'; color:var(--accent-2); font-size:15px; font-weight:600; }
@media (max-width:780px) { .compare-grid { grid-template-columns:1fr; } }

.cta-strip { padding:48px; background:linear-gradient(135deg, #ff5e1f, #c2400d); border-radius:20px; text-align:center; margin-top:48px; }
.cta-strip h3 { font-size:28px; margin-bottom:10px; color:#fff; }
.cta-strip p { color:rgba(255,255,255,0.92); margin-bottom:24px; font-size:16px; }
.cta-strip .btn { background:#0a0a0c; }

/* Video facade — iframe laadt pas bij klik (privacy + page speed) */
.video-wrap { position:relative; border-radius:16px; overflow:hidden; aspect-ratio:16/9; background:#000; cursor:pointer; max-width:880px; margin:0 auto; box-shadow:0 30px 60px -20px rgba(0,0,0,0.5); border:1px solid var(--line); }
.video-wrap img { width:100%; height:100%; object-fit:cover; max-width:none; max-height:none; }
.video-wrap .play {
  position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
  width:88px; height:88px; border-radius:50%;
  background:rgba(255,94,31,0.92); display:flex; align-items:center; justify-content:center;
  box-shadow:0 0 0 10px rgba(255,94,31,0.22), 0 20px 40px rgba(0,0,0,0.4);
  transition:transform .2s, background .2s;
}
.video-wrap:hover .play { transform:translate(-50%,-50%) scale(1.08); background:#ff5e1f; }
.video-wrap .play::before {
  content:""; width:0; height:0;
  border-left:24px solid white; border-top:15px solid transparent; border-bottom:15px solid transparent;
  margin-left:4px;
}
.video-wrap .vlabel {
  position:absolute; bottom:20px; left:24px; right:24px;
  color:white; font-family:'Space Grotesk'; font-weight:600; font-size:17px;
  text-shadow:0 2px 8px rgba(0,0,0,0.85);
  pointer-events:none;
}
.video-wrap iframe { width:100%; height:100%; border:none; display:block; }
"""

LISTING_CSS = """
.hub-hero { padding:140px 0 50px; position:relative; }
.hub-hero::before { content:""; position:absolute; inset:0; background:radial-gradient(50% 50% at 80% 20%, rgba(255,94,31,0.18), transparent 60%); z-index:0; }
.hub-hero .container { position:relative; z-index:2; }
.eyebrow { display:inline-block; color:var(--accent); font-size:12px; text-transform:uppercase; letter-spacing:0.16em; font-weight:600; margin-bottom:14px; padding:5px 12px; background:rgba(255,94,31,0.08); border:1px solid rgba(255,94,31,0.2); border-radius:999px; }
.hub-hero h1 { font-size:clamp(36px,4.8vw,60px); margin-bottom:18px; letter-spacing:-0.035em; }
.hub-hero p { color:var(--ink-2); font-size:18px; max-width:720px; }
.hub-section { padding:50px 0 60px; }
.hub-section .head { margin-bottom:32px; }
.hub-section h2 { font-size:clamp(24px,2.8vw,34px); margin-bottom:8px; }
.hub-section p.lede { color:var(--ink-2); font-size:16px; max-width:720px; }

.hub-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:20px; }
.hub-card { background:var(--bg-2); border:1px solid var(--line); border-radius:16px; overflow:hidden; transition:transform .25s, border-color .25s, box-shadow .25s; display:flex; flex-direction:column; }
.hub-card:hover { transform:translateY(-3px); border-color:var(--line-2); box-shadow:0 30px 60px -30px rgba(0,0,0,0.5); }
.hub-thumb { aspect-ratio:4/3; background:linear-gradient(180deg, var(--bg-3) 0%, var(--bg) 100%); position:relative; overflow:hidden; display:flex; align-items:center; justify-content:center; border-bottom:1px solid var(--line); }
.hub-thumb::before { content:""; position:absolute; inset:0; background:radial-gradient(45% 35% at 50% 50%, rgba(255,94,31,0.16), transparent 70%); }
.hub-thumb img { max-height:80%; max-width:72%; width:auto; height:auto; object-fit:contain; position:relative; z-index:2; filter:drop-shadow(0 18px 30px rgba(0,0,0,0.5)); }
.hub-card-body { padding:22px 24px 24px; display:flex; flex-direction:column; flex:1; }
.hub-card .vendor { color:var(--ink-3); font-size:11px; text-transform:uppercase; letter-spacing:0.12em; font-weight:600; margin-bottom:6px; }
.hub-card h3 { font-size:19px; margin-bottom:6px; }
.hub-card p.tag { color:var(--ink-2); font-size:13.5px; line-height:1.5; margin-bottom:14px; flex:1; }
.hub-card .foot { display:flex; justify-content:space-between; align-items:center; padding-top:14px; border-top:1px solid var(--line); }
.hub-card .price-mini { font-family:'Space Grotesk'; font-weight:600; font-size:16px; }
.hub-card .price-mini .per { color:var(--ink-3); font-size:12px; font-weight:400; }
.hub-card .arr { color:var(--accent-2); font-weight:600; font-size:13.5px; }
@media (max-width:880px) { .hub-grid { grid-template-columns:repeat(2,1fr); } }
@media (max-width:520px) { .hub-grid { grid-template-columns:1fr; } }
"""

NAV_HTML = """
<nav class="top">
  <div class="container row">
    <a href="/" class="brand">
      <div class="brand-mark"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round"><path d="M5 9h14v10H5z"/><circle cx="9" cy="14" r="1.2" fill="white"/><circle cx="15" cy="14" r="1.2" fill="white"/><path d="M12 5v4"/></svg></div>
      BotLease
    </a>
    <div class="nav-links">
      <a href="/#hoe">Werkwijze</a>
      <a href="/robots" class="active">Robots</a>
      <a href="/#cases">Toepassingen</a>
      <a href="/nieuws">Nieuws</a>
      <a href="/#faq">FAQ</a>
    </div>
    <a href="/#contact" class="btn">Plan demo →</a>
  </div>
</nav>
"""

FOOTER_HTML = """
<footer>
  <div class="container row">
    <div>© 2026 BotLease B.V. (i.o.) — Eindhoven · Rotterdam</div>
    <div><a href="/">Home</a> · <a href="/robots">Robots</a> · <a href="/nieuws">Nieuws</a> · <a href="/#contact">Contact</a> · <a href="/sitemap.xml">Sitemap</a></div>
  </div>
</footer>
"""

ORG_SCHEMA = json.dumps({
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "BotLease",
    "url": SITE_URL,
    "logo": f"{SITE_URL}/logo.png",
    "description": "Nederlands eerste full-service leasemaatschappij voor humanoïde robots.",
    "address": {"@type": "PostalAddress", "addressLocality": "Eindhoven", "addressCountry": "NL"},
}, ensure_ascii=False)


def product_jsonld(r: dict) -> str:
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Product",
        "name": r["name"],
        "image": f"{SITE_URL}{r['photo']}",
        "description": r["short"],
        "brand": {"@type": "Brand", "name": r["vendor"]},
        "manufacturer": {"@type": "Organization", "name": r["vendor"]},
        "category": "Humanoïde robot",
        "offers": {
            "@type": "Offer",
            "url": f"{SITE_URL}/robots/{r['slug']}",
            "priceCurrency": "EUR",
            "price": str(r["lease_eur"]),
            "priceSpecification": {
                "@type": "UnitPriceSpecification",
                "price": str(r["lease_eur"]),
                "priceCurrency": "EUR",
                "billingDuration": "P1M",
                "unitText": "MONTH",
            },
            "availability": "https://schema.org/InStock" if r["category"] == "available" else "https://schema.org/PreOrder",
            "areaServed": [
                {"@type": "Country", "name": "Nederland"},
                {"@type": "Country", "name": "België"},
                {"@type": "Country", "name": "Duitsland"},
            ],
            "seller": {"@type": "Organization", "name": "BotLease"},
        },
        "additionalProperty": [
            {"@type": "PropertyValue", "name": "Hoogte", "value": f"{r['height_cm']} cm"},
            {"@type": "PropertyValue", "name": "Gewicht", "value": f"{r['weight_kg']} kg"},
            {"@type": "PropertyValue", "name": "Payload", "value": f"{r['payload_kg']} kg"},
            {"@type": "PropertyValue", "name": "Batterij", "value": f"{r['battery_hours']} uur"},
            {"@type": "PropertyValue", "name": "DoF", "value": str(r["dof"])},
            {"@type": "PropertyValue", "name": "Snelheid", "value": f"{r['speed_ms']} m/s"},
        ],
    }, ensure_ascii=False)


def breadcrumb_jsonld(r: dict) -> str:
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Robots", "item": f"{SITE_URL}/robots/"},
            {"@type": "ListItem", "position": 3, "name": r["name"], "item": f"{SITE_URL}/robots/{r['slug']}"},
        ]
    }, ensure_ascii=False)


def video_section(r: dict) -> str:
    vid = r.get("video_id")
    if not vid:
        return ""
    title = r.get("video_title") or f"{r['name']} — officiële demonstratie"
    thumb = f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg"
    return f"""
<section style="background:var(--bg-2); border-top:1px solid var(--line); border-bottom:1px solid var(--line)">
  <div class="container">
    <div class="section-eyebrow">In actie</div>
    <h2 style="margin-bottom:8px">{escape(r['name'])} — officiële demo.</h2>
    <p class="lede" style="margin-bottom:32px">{escape(title)}. Bron: {escape(r['vendor'])}.</p>
    <div class="video-wrap" data-video-id="{vid}" role="button" aria-label="Speel video af: {escape(title)}">
      <img src="{thumb}" alt="{escape(title)}" loading="lazy"
           onerror="this.src='https://i.ytimg.com/vi/{vid}/hqdefault.jpg'">
      <div class="play" aria-hidden="true"></div>
      <div class="vlabel">▶ {escape(title)}</div>
    </div>
  </div>
</section>"""


def video_jsonld(r: dict) -> str:
    vid = r.get("video_id")
    if not vid:
        return ""
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": r.get("video_title") or f"{r['name']} — officiële demonstratie",
        "description": f"Officiële demonstratie van de {r['name']} humanoïde robot door {r['vendor']}.",
        "thumbnailUrl": [f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg"],
        "uploadDate": "2025-01-01",
        "contentUrl": f"https://www.youtube.com/watch?v={vid}",
        "embedUrl": f"https://www.youtube.com/embed/{vid}",
        "publisher": {"@type": "Organization", "name": r["vendor"]},
    }, ensure_ascii=False)


def render_robot(r: dict, related: list) -> str:
    tier_class = {"eu": "tier-eu", "value": "tier-value", "premium": "tier-premium"}.get(r["tier"], "tier-eu")
    photo_url = f"{SITE_URL}{r['photo']}"
    use_cases_html = "".join(
        f'<div class="usecase-card"><div class="n">USE-CASE {i+1:02d}</div><h4>{escape(uc.split(":")[0] if ":" in uc else uc[:60])}</h4><p>{escape(uc)}</p></div>'
        for i, uc in enumerate(r["use_cases"])
    )
    specs_html = "".join(
        f'<div class="spec-row"><div class="k">{escape(k)}</div><div class="v">{escape(v)}</div></div>'
        for k, v in r["specs_detail"]
    )
    related_html = "".join(
        f'<a href="/robots/{rel["slug"]}" class="compare-card">'
        f'<div class="vendor" style="font-size:11px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.12em">{escape(rel["vendor"])}</div>'
        f'<div class="vname">{escape(rel["name"])}</div>'
        f'<div class="vmeta">{rel["height_cm"]} cm · {rel["payload_kg"]} kg payload</div>'
        f'<div class="vprice">€{rel["lease_eur"]:,}/mnd</div>'
        f'</a>'.replace(",", ".")
        for rel in related[:3]
    )
    waitlist_notice = (
        '<p style="background:rgba(255,201,102,0.1); border:1px solid rgba(255,201,102,0.3); '
        'border-radius:10px; padding:14px 18px; color:#ffd166; font-size:14px; margin:18px 0">'
        '⏳ Deze robot is nog niet commercieel leverbaar voor EU-derden. Reserveer een plek op de wachtlijst — '
        'BotLease krijgt prioriteit zodra ze beschikbaar komen.</p>'
    ) if r["category"] == "waitlist" else ""

    title_kw = f"{r['name']} leasen in Nederland — vanaf €{r['lease_eur']:,}/mnd | BotLease".replace(",", ".")
    meta_desc = (
        f"{r['name']} ({r['vendor']}, {r['vendor_country']}) leasen via BotLease vanaf €{r['lease_eur']:,}/maand. "
        f"All-in operational lease: installatie, training, onderhoud, swap-SLA, verzekering. "
        f"{r['tagline']}"
    ).replace(",", ".")

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title_kw)}</title>
<meta name="description" content="{escape(meta_desc)}">
<meta name="keywords" content="{escape(r['name'])} leasen, {escape(r['name'])} huren Nederland, {escape(r['vendor'])} robot, humanoide robot lease, {', '.join(r['tags'])}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="author" content="BotLease">
<link rel="canonical" href="{SITE_URL}/robots/{r['slug']}">

<meta property="og:type" content="product">
<meta property="og:title" content="{escape(r['name'])} leasen — €{r['lease_eur']:,}/mnd | BotLease">
<meta property="og:description" content="{escape(r['tagline'])}">
<meta property="og:url" content="{SITE_URL}/robots/{r['slug']}">
<meta property="og:image" content="{photo_url}">
<meta property="og:site_name" content="BotLease">
<meta property="og:locale" content="nl_NL">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(r['name'])} leasen — €{r['lease_eur']:,}/mnd">
<meta name="twitter:description" content="{escape(r['tagline'])}">
<meta name="twitter:image" content="{photo_url}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>{PAGE_CSS}{ROBOT_CSS}</style>
<script type="application/ld+json">{product_jsonld(r)}</script>
<script type="application/ld+json">{breadcrumb_jsonld(r)}</script>
{f'<script type="application/ld+json">{video_jsonld(r)}</script>' if r.get('video_id') else ''}
<script type="application/ld+json">{ORG_SCHEMA}</script>
</head>
<body>
{NAV_HTML}

<section class="r-hero">
  <div class="container">
    <nav class="crumbs">
      <a href="/">Home</a><span class="sep">/</span>
      <a href="/robots">Robots</a><span class="sep">/</span>
      <span>{escape(r['name'])}</span>
    </nav>
    <div class="r-hero-grid">
      <div>
        <span class="tier-badge {tier_class}">{escape(r['badge'])}</span>
        <div class="vendor" style="margin-top:18px">{escape(r['vendor'])} · {escape(r['vendor_country'])}</div>
        <h1>{escape(r['name'])} leasen.</h1>
        <p class="tag">{escape(r['tagline'])}</p>
        <p class="lede">{escape(r['short'])}</p>
        {waitlist_notice}
        <div class="r-hero-cta">
          <a class="btn" href="/#contact">Plan een demo →</a>
          <a class="btn ghost" href="#price">Bekijk prijs</a>
        </div>
      </div>
      <div class="r-hero-art">
        <img src="{r['photo']}" alt="{escape(r['name'])} humanoïde robot — {escape(r['vendor'])}" width="{r['photo_dims'][0]}" height="{r['photo_dims'][1]}">
      </div>
    </div>
  </div>
</section>

<section class="r-quick">
  <div class="container">
    <div class="r-quick-grid">
      <div class="r-quick-item"><span class="v">{r['height_cm']} cm</span><span class="l">Hoogte</span></div>
      <div class="r-quick-item"><span class="v">{r['weight_kg']} kg</span><span class="l">Gewicht</span></div>
      <div class="r-quick-item"><span class="v">{r['payload_kg']} kg</span><span class="l">Payload</span></div>
      <div class="r-quick-item"><span class="v">{r['battery_hours']} u</span><span class="l">Batterij</span></div>
      <div class="r-quick-item"><span class="v">{r['dof']}</span><span class="l">DoF</span></div>
      <div class="r-quick-item"><span class="v">{r['speed_ms']} m/s</span><span class="l">Snelheid</span></div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-eyebrow">Toepassingen</div>
    <h2>Waar verdient een {escape(r['name'])} zich terug?</h2>
    <p class="lede">Specifieke use-cases waar dit model getest of bewezen is — niet generiek "robots zijn handig".</p>
    <div class="usecases-grid">{use_cases_html}</div>
  </div>
</section>

<section style="background:var(--bg-2); border-top:1px solid var(--line); border-bottom:1px solid var(--line)">
  <div class="container">
    <div class="section-eyebrow">Specificaties</div>
    <h2>Wat zit er onder de motorkap.</h2>
    <div class="spec-table">{specs_html}</div>
  </div>
</section>

{video_section(r)}

<section id="price">
  <div class="container">
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:40px; align-items:start">
      <div>
        <div class="section-eyebrow">Lease-prijs</div>
        <h2>All-in vanaf €{r['lease_eur']:,}/mnd.</h2>
        <p class="lede">36 maanden operational lease. Geen investering vooraf. Per maand opzegbaar na jaar 1.</p>
        <p style="color:var(--ink-3); font-size:14px">Aanschafprijs publiek: <b style="color:var(--ink)">€{r['purchase_eur']:,}</b> — wij dragen het restwaarde-risico.</p>
      </div>
      <div class="price-block">
        <div class="price-row"><b>€{r['lease_eur']:,}</b><span class="per">/mnd · 36 mnd</span></div>
        <div class="setup">+ €{r['setup_eur']:,} eenmalige setup (installatie, training, integratie)</div>
        <ul>
          <li>Installatie + 2-uurs training operators</li>
          <li>Preventief + correctief onderhoud</li>
          <li>Swap-SLA: vervangende unit binnen 24u</li>
          <li>WA-verzekering tot €2,5M + casco</li>
          <li>24/7 helpdesk Nederlands</li>
          <li>Software-updates en remote tuning</li>
        </ul>
        <a class="btn" href="/#contact" style="display:block; text-align:center">Vraag offerte →</a>
      </div>
    </div>
  </div>
</section>

<section style="background:var(--bg-2); border-top:1px solid var(--line)">
  <div class="container">
    <div class="section-eyebrow">Alternatieven</div>
    <h2>Vergelijk met andere modellen.</h2>
    <p class="lede">Twijfel over het juiste model? Vergelijk specs, prijs en use-cases. Of plan een gratis intake — wij adviseren onafhankelijk.</p>
    <div class="compare-grid">{related_html}</div>
  </div>
</section>

<section>
  <div class="container">
    <div class="cta-strip">
      <h3>Klaar voor een demo van de {escape(r['name'])}?</h3>
      <p>Gratis intake op locatie · binnen 5 werkdagen · geen verplichtingen</p>
      <a class="btn" href="/#contact">Plan een demo →</a>
    </div>
  </div>
</section>

{FOOTER_HTML}

<script>
document.querySelectorAll('.video-wrap').forEach(function(el){{
  el.addEventListener('click', function(){{
    var id = el.dataset.videoId;
    if(!id) return;
    el.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0" '
      + 'title="' + (el.getAttribute('aria-label') || 'Video') + '" '
      + 'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" '
      + 'allowfullscreen></iframe>';
  }});
}});
</script>
</body>
</html>
""".replace(",", ".")


def render_hub() -> str:
    def card(r):
        price_text = f'€{r["lease_eur"]:,}/mnd'.replace(",", ".")
        return f"""<a href="/robots/{r['slug']}" class="hub-card">
            <div class="hub-thumb">
              <img src="{r['photo']}" alt="{escape(r['name'])} humanoïde robot" loading="lazy">
            </div>
            <div class="hub-card-body">
              <div class="vendor">{escape(r['vendor'])} · {escape(r['vendor_country'])}</div>
              <h3>{escape(r['name'])}</h3>
              <p class="tag">{escape(r['tagline'])}</p>
              <div class="foot">
                <span class="price-mini">{price_text}<span class="per"> / mnd</span></span>
                <span class="arr">Bekijk →</span>
              </div>
            </div>
        </a>"""

    eu_cards    = "".join(card(r) for r in available_robots() if r["tier"] == "eu")
    value_cards = "".join(card(r) for r in available_robots() if r["tier"] == "value")
    waitlist    = "".join(card(r) for r in waitlist_robots())

    itemlist = json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "BotLease robot catalogus — humanoïde robots voor lease in Nederland",
        "itemListElement": [
            {"@type": "ListItem", "position": i+1, "url": f"{SITE_URL}/robots/{r['slug']}", "name": r["name"]}
            for i, r in enumerate(ROBOTS)
        ],
    }, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Humanoïde robots leasen Nederland — catalogus 2026 | BotLease</title>
<meta name="description" content="Vergelijk alle leverbare humanoïde robots in Nederland: NEURA 4NE-1, Unitree G1/H1-2/H2/R1, PAL Kangaroo, Pollen Reachy 2, UBTECH Walker S2, EngineAI SE01. Vanaf €290/mnd all-in lease. EU-gebouwde modellen prioriteit voor AI-Act compliance.">
<meta name="keywords" content="humanoide robot leasen Nederland, NEURA 4NE-1, Unitree leasen, PAL Robotics Kangaroo, Apptronik Apollo, Figure 02, humanoid catalogus 2026, robot huren MKB Nederland">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/robots/">

<meta property="og:type" content="website">
<meta property="og:title" content="Humanoïde robots leasen Nederland — 15 modellen vergelijken | BotLease">
<meta property="og:description" content="Complete catalogus humanoïde robots voor lease in Nederland: EU-gebouwd (NEURA, PAL, Pollen), Aziatisch (Unitree, UBTECH, EngineAI), wachtlijst (Apptronik, Figure, 1X NEO).">
<meta property="og:url" content="{SITE_URL}/robots/">
<meta property="og:image" content="{SITE_URL}/img/robots/neura-4ne1.webp">
<meta property="og:locale" content="nl_NL">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE_URL}/img/robots/neura-4ne1.webp">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>{PAGE_CSS}{LISTING_CSS}</style>
<script type="application/ld+json">{itemlist}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE_URL}/"}}, {{"@type": "ListItem", "position": 2, "name": "Robots", "item": "{SITE_URL}/robots/"}}]}}</script>
</head>
<body>
{NAV_HTML}

<section class="hub-hero">
  <div class="container">
    <div class="eyebrow">Catalogus 2026</div>
    <h1>Humanoïde robots leasen in Nederland.</h1>
    <p>15 modellen vergeleken, gerangschikt naar leverbaarheid. EU-gebouwde robots (NEURA, PAL, Pollen) eerst — voor de kortste supply chain en EU AI-Act compliance vanaf dag 1. Daarna Aziatische value-modellen, en de wachtlijst voor 2027.</p>
  </div>
</section>

<section class="hub-section">
  <div class="container">
    <div class="head">
      <span class="tier-badge tier-eu">EU-gebouwd · direct leverbaar</span>
      <h2 style="margin-top:14px">Europese humanoids — korte supply chain, EU AI-Act compliant.</h2>
      <p class="lede">Geproduceerd in Duitsland (NEURA), Spanje (PAL) en Frankrijk (Pollen). EU AI-Act + Machineverordening 2023/1230 ready vanaf dag 1. Geen importheffingen, EU-talige support, GDPR by design.</p>
    </div>
    <div class="hub-grid">{eu_cards}</div>
  </div>
</section>

<section class="hub-section" style="background:var(--bg-2); border-top:1px solid var(--line); border-bottom:1px solid var(--line)">
  <div class="container">
    <div class="head">
      <span class="tier-badge tier-value">Aziatisch · direct leverbaar</span>
      <h2 style="margin-top:14px">Value-modellen uit China — agressief geprijsd, snel leverbaar.</h2>
      <p class="lede">Unitree, UBTECH en EngineAI verkopen via shop/EU-distributeurs. 6-10 weken levertijd. Lagere instapprijs maar let op AI-Act compliance assessment (BotLease regelt dit per deployment).</p>
    </div>
    <div class="hub-grid">{value_cards}</div>
  </div>
</section>

<section class="hub-section">
  <div class="container">
    <div class="head">
      <span class="tier-badge tier-premium">Wachtlijst 2026/2027</span>
      <h2 style="margin-top:14px">Premium Amerikaans/Aziatisch — wachtlijst.</h2>
      <p class="lede">Bewezen modellen die nog niet open verkocht worden in EU. Apptronik Apollo, Figure 02/03, Boston Dynamics Atlas — allemaal in pilot bij grote OEMs (Mercedes, BMW, Hyundai). BotLease faciliteert priority access zodra EU-verkoop open gaat.</p>
    </div>
    <div class="hub-grid">{waitlist}</div>
  </div>
</section>

{FOOTER_HTML}
</body>
</html>
"""


def build():
    ROBOT_DIR.mkdir(parents=True, exist_ok=True)
    for r in ROBOTS:
        related = [x for x in ROBOTS if x["slug"] != r["slug"] and x["tier"] == r["tier"]]
        if len(related) < 3:
            related += [x for x in ROBOTS if x["slug"] != r["slug"] and x not in related]
        (ROBOT_DIR / f"{r['slug']}.html").write_text(render_robot(r, related[:3]), encoding="utf-8")
    (ROBOT_DIR / "index.html").write_text(render_hub(), encoding="utf-8")
    print(f"✅ Built {len(ROBOTS)} robot pages + hub at /robots/")


if __name__ == "__main__":
    build()
