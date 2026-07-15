#!/usr/bin/env python3
"""
Generates:
- frontend/robots/<slug>.html       - per-robot landing page (long-tail SEO)
- frontend/robots/index.html        - overview / robots-hub
"""
from __future__ import annotations
import re
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
from seo_common import HEAD_SEO, trim_desc  # noqa: E402
from style_base import BASE_CSS, NAV_HTML, FOOTER_HTML, FONTS_LINK  # noqa: E402

PAGE_CSS = BASE_CSS + """
/* Tier badges voor robotpagina's */
.tier-badge { display:inline-block; padding:4px 12px; border-radius:999px; font-size:11px; font-weight:600; letter-spacing:0.08em; text-transform:uppercase; font-family:'Hanken Grotesk'; }
.tier-eu      { background:var(--green-soft); color:var(--green); border:1px solid var(--green-line); }
.tier-value   { background:var(--accent-soft); color:var(--accent-deep); border:1px solid var(--accent-line); }
.tier-premium { background:var(--blue-soft); color:var(--blue); border:1px solid #bfdbfe; }
"""

ROBOT_CSS = """
.r-hero { padding:80px 0 40px; }
@media (min-width:768px) { .r-hero { padding:110px 0 40px; } }
.r-hero-grid {
  display:grid; grid-template-columns:1fr; gap:48px; align-items:center;
}
@media (min-width:1024px) {
  .r-hero-grid { grid-template-columns:1.2fr 1fr; gap:64px; }
}
.r-hero h1 {
  font-family:'Bricolage Grotesque', -apple-system, sans-serif; font-weight:700;
  font-size:clamp(36px, 4.6vw, 58px);
  margin:14px 0 18px; letter-spacing:-0.035em; line-height:1.06;
}
.r-hero .tag { color:var(--accent); font-size:18px; margin-bottom:24px; font-weight:500; line-height:1.5; }
.r-hero .lede { color:var(--ink-2); font-size:17px; line-height:1.55; margin-bottom:32px; max-width:560px; }
.r-hero .vendor { color:var(--ink-3); font-size:12.5px; letter-spacing:0.01em; font-weight:600; margin-bottom:8px; }
.r-hero-cta { display:flex; gap:12px; flex-wrap:wrap; margin-bottom:36px; }
.r-hero-art {
  background:var(--bg-card);
  border:1px solid var(--border); border-radius:20px; padding:32px;
  display:flex; align-items:center; justify-content:center;
  aspect-ratio:4/5; position:relative; overflow:hidden;
  box-shadow:var(--shadow-lg);
}
.r-hero-art::before {
  content:""; position:absolute; inset:0;
  background:radial-gradient(60% 50% at 50% 100%, var(--accent-soft) 0%, transparent 60%);
}
.r-hero-art img {
  max-height:90%; max-width:90%; width:auto; height:auto; object-fit:contain;
  position:relative; z-index:2;
}
@media (max-width:1023px) {
  .r-hero-art { aspect-ratio:5/4; max-width:520px; margin:0 auto; }
}

.r-quick {
  background:var(--bg-2);
  border-top:1px solid var(--border); border-bottom:1px solid var(--border);
  padding:32px 0;
}
.r-quick-grid {
  display:grid; grid-template-columns:repeat(2, 1fr); gap:24px;
}
@media (min-width:640px) { .r-quick-grid { grid-template-columns:repeat(3, 1fr); } }
@media (min-width:880px) { .r-quick-grid { grid-template-columns:repeat(6, 1fr); gap:20px; } }
.r-quick-item { display:flex; flex-direction:column; gap:4px; }
.r-quick-item .v {
  font-family:'Hanken Grotesk'; font-size:22px; font-weight:600;
  letter-spacing:-0.02em; color:var(--ink);
}
.r-quick-item .l { font-size:12px; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.1em; font-weight:500; }

section h2 {
  font-family:'Bricolage Grotesque', -apple-system, sans-serif; font-weight:700;
  font-size:clamp(26px, 3vw, 40px);
  margin-bottom:16px; letter-spacing:-0.025em; line-height:1.1;
}
section p.lede { color:var(--ink-2); font-size:17px; max-width:680px; margin-bottom:36px; line-height:1.55; }

.usecases-grid { display:grid; grid-template-columns:1fr; gap:16px; }
@media (min-width:768px) { .usecases-grid { grid-template-columns:repeat(2, 1fr); } }
.usecase-card {
  padding:24px; background:var(--bg-card);
  border:1px solid var(--border); border-radius:12px;
  transition:border-color .2s, transform .2s, box-shadow .2s;
}
.usecase-card:hover { border-color:var(--border-hover); transform:translateY(-2px); box-shadow:var(--shadow-sm); }
.usecase-card .n {
  font-family:'Hanken Grotesk'; color:var(--accent-deep);
  font-weight:600; font-size:12px; margin-bottom:8px; letter-spacing:0.08em;
}
.usecase-card h3, .usecase-card h4 { font-family:'Hanken Grotesk'; font-weight:600; font-size:17px; margin-bottom:6px; color:var(--ink); }
.usecase-card p { color:var(--ink-2); font-size:14.5px; line-height:1.55; }

.spec-table {
  background:var(--bg-card); border:1px solid var(--border);
  border-radius:14px; overflow:hidden;
}
.spec-row {
  display:grid; grid-template-columns:200px 1fr; gap:24px;
  padding:18px 24px; border-bottom:1px solid var(--border);
}
.spec-row:last-child { border-bottom:none; }
.spec-row .k { color:var(--ink-3); font-size:13px; font-weight:500; text-transform:uppercase; letter-spacing:0.05em; }
.spec-row .v { color:var(--ink); font-size:15px; }
@media (max-width:580px) { .spec-row { grid-template-columns:1fr; gap:4px; padding:14px 18px; } }

.price-block {
  background:var(--bg-card); border:1px solid var(--border-hover); border-radius:18px;
  padding:32px; box-shadow:var(--shadow-sm);
}
.price-row { display:flex; align-items:baseline; gap:6px; margin-bottom:10px; }
.price-row b {
  font-family:'Bricolage Grotesque', -apple-system, sans-serif; font-weight:700;
  font-size:48px; letter-spacing:-0.025em; color:var(--ink);
}
.price-row .per { color:var(--ink-3); font-size:15px; }
.price-block .setup { color:var(--ink-2); font-size:14px; margin-bottom:18px; }
.price-block ul { list-style:none; padding:0; margin:18px 0 24px; }
.price-block li {
  color:var(--ink-2); font-size:14.5px; margin-bottom:8px;
  padding-left:22px; position:relative;
}
.price-block li::before { content:"✓"; position:absolute; left:0; color:var(--green); font-weight:700; }

.compare-grid { display:grid; grid-template-columns:1fr; gap:14px; }
@media (min-width:640px) { .compare-grid { grid-template-columns:repeat(3, 1fr); } }
.compare-card {
  padding:22px; background:var(--bg-card);
  border:1px solid var(--border); border-radius:12px;
  transition:border-color .2s, transform .2s, box-shadow .2s;
  display:block; color:inherit;
}
.compare-card:hover { border-color:var(--border-hover); transform:translateY(-2px); box-shadow:var(--shadow-sm); }
.compare-card .vname { font-family:'Hanken Grotesk'; font-weight:600; font-size:17px; margin:6px 0 4px; color:var(--ink); }
.compare-card .vmeta { color:var(--ink-3); font-size:13px; margin-bottom:10px; }
.compare-card .vprice { font-family:'Hanken Grotesk'; color:var(--accent); font-size:15px; font-weight:600; }

.cta-strip {
  padding:48px; background:var(--bg-dark); color:var(--ink-on-dark);
  border-radius:20px; text-align:center; margin-top:48px;
}
.cta-strip h3 {
  font-family:'Bricolage Grotesque', -apple-system, sans-serif; font-weight:700;
  font-size:28px; margin-bottom:10px; color:var(--ink-on-dark);
}
section.body .cta-strip p, .cta-strip p { color:var(--ink-2-on-dark); margin-bottom:24px; font-size:16px; }
.cta-strip .btn { background:var(--accent); color:#fff; border-color:var(--accent); }
.cta-strip .btn:hover { background:#fff; color:var(--ink); border-color:#fff; }

/* Video facade - iframe laadt pas bij klik */
.video-wrap {
  position:relative; border-radius:16px; overflow:hidden;
  aspect-ratio:16/9;
  cursor:pointer; max-width:880px; margin:0 auto;
  box-shadow:var(--shadow-lg);
}
.video-wrap img { width:100%; height:100%; object-fit:cover; max-width:none; max-height:none; }
.video-wrap .play {
  position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
  width:80px; height:80px; border-radius:50%;
  background:var(--accent); display:flex; align-items:center; justify-content:center;
  box-shadow:0 0 0 8px rgba(194,65,12,0.2), 0 20px 40px rgba(0,0,0,0.3);
  transition:transform .2s, background .2s;
}
.video-wrap:hover .play { transform:translate(-50%,-50%) scale(1.06); background:var(--accent-deep); }
.video-wrap .play::before {
  content:""; width:0; height:0;
  border-left:22px solid white; border-top:14px solid transparent; border-bottom:14px solid transparent;
  margin-left:4px;
}
.video-wrap .vlabel {
  position:absolute; bottom:16px; left:16px; right:auto; max-width:calc(100% - 32px);
  color:#f5f5f7; font-family:'Hanken Grotesk'; font-weight:600; font-size:15px;
  background:rgba(0,0,0,0.72); border-radius:10px; padding:8px 14px;
  pointer-events:none;
}
.video-wrap iframe { width:100%; height:100%; border:none; display:block; }
"""

LISTING_CSS = """
.hub-hero { padding:80px 0 40px; }
@media (min-width:768px) { .hub-hero { padding:110px 0 50px; } }
.eyebrow {
  display:inline-block; color:var(--accent); font-size:14px;
  letter-spacing:-0.005em; font-weight:600;
  margin-bottom:14px;
}
.hub-hero h1 {
  font-family:'Bricolage Grotesque', -apple-system, sans-serif; font-weight:700;
  font-size:60px;
  margin-bottom:18px; letter-spacing:-0.035em; line-height:1.05;
}
@media (max-width:1100px){ .hub-hero h1{font-size:48px;} }
@media (max-width:640px){ .hub-hero h1{font-size:37px;} }
.hub-hero p { color:var(--ink-2); font-size:18px; max-width:720px; line-height:1.55; }
.hub-section { padding:48px 0 64px; }
@media (min-width:768px) { .hub-section { padding:64px 0 80px; } }
.hub-section .head { margin-bottom:32px; }
.hub-section h2 {
  font-family:'Bricolage Grotesque', -apple-system, sans-serif; font-weight:700;
  font-size:36px;
  margin-bottom:10px; letter-spacing:-0.025em; line-height:1.1;
}
@media (max-width:900px){ .hub-section h2{font-size:30px;} }
@media (max-width:640px){ .hub-section h2{font-size:26px;} }
.hub-section p.lede { color:var(--ink-2); font-size:16px; max-width:720px; line-height:1.55; }

.hub-grid { display:grid; grid-template-columns:repeat(2, 1fr); gap:14px; }
@media (min-width:780px) { .hub-grid { grid-template-columns:repeat(3,1fr); gap:16px; } }
@media (min-width:1100px) { .hub-grid { grid-template-columns:repeat(4,1fr); gap:18px; } }
.hub-card {
  background:var(--bg-card); border:1px solid var(--border);
  border-radius:12px; overflow:hidden;
  transition:transform .2s, border-color .2s, box-shadow .2s;
  display:flex; flex-direction:column; color:inherit;
}
.hub-card:hover { transform:translateY(-2px); border-color:var(--border-hover); box-shadow:var(--shadow-sm); }
.hub-thumb {
  aspect-ratio:5/3;
  background:linear-gradient(180deg, var(--bg-2) 0%, var(--bg-card) 100%);
  position:relative; overflow:hidden;
  display:flex; align-items:center; justify-content:center;
}
.hub-thumb::before {
  content:""; position:absolute; inset:0;
  background:radial-gradient(40% 30% at 50% 60%, var(--accent-soft) 0%, transparent 70%);
}
.hub-thumb img {
  max-height:78%; max-width:55%; width:auto; height:auto;
  object-fit:contain; position:relative; z-index:2;
  filter:drop-shadow(0 8px 16px rgba(28,25,23,0.12));
}
.hub-card-body { padding:14px 16px 16px; display:flex; flex-direction:column; flex:1; }
.hub-card .vendor { color:var(--ink-3); font-size:12.5px; letter-spacing:0.01em; font-weight:600; margin-bottom:4px; }
.hub-card h3 { font-family:'Hanken Grotesk'; font-weight:600; font-size:16px; margin-bottom:4px; color:var(--ink); letter-spacing:-0.01em; line-height:1.2; }
.hub-card p.tag { color:var(--ink-2); font-size:12.5px; line-height:1.45; margin-bottom:8px; }
.hub-tags {
  position:absolute; top:10px; left:10px; right:10px; z-index:3;
  display:flex; flex-wrap:wrap; gap:5px;
  pointer-events:none;
}
.hub-tag {
  display:inline-block; padding:3px 9px; border-radius:999px;
  font-size:10.5px; font-weight:600; letter-spacing:0.01em;
  background:rgba(255,255,255,0.92); color:var(--ink);
  border:1px solid rgba(255,255,255,0.6);
  backdrop-filter:blur(6px); -webkit-backdrop-filter:blur(6px);
  box-shadow:0 1px 3px rgba(0,0,0,0.08);
  white-space:nowrap;
}
.hub-card .foot { display:flex; justify-content:space-between; align-items:center; padding-top:10px; border-top:1px solid var(--border); }
.hub-card .price-mini { font-family:'Hanken Grotesk'; font-weight:600; font-size:14px; color:var(--ink); }
.hub-card .price-mini .per { color:var(--ink-3); font-size:11px; font-weight:400; }
.hub-card .arr { color:var(--accent); font-weight:600; font-size:12.5px; }
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
    """NL thousand separator (€1,295 -> €1.295) — scoped to euro amounts ONLY.
    The previous global (\\d),(\\d) regex corrupted every rgba()/grid/JSON comma in
    the document (e.g. rgba(251,251,253,0.72) -> rgba(251.251.253.0.72)); this only
    touches commas that sit inside a € amount, so CSS/JSON/JS are never altered."""
    import re
    return re.sub(r'€\d{1,3}(?:,\d{3})+', lambda m: m.group(0).replace(",", "."), html)


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


def _best_youtube_thumb(vid: str) -> str:
    """Pre-flight check welke YouTube-thumbnail variant 16:9 én aanwezig is.

    YouTube genereert maxresdefault/hq720 niet voor élke video; de generieke
    onerror-fallback is onbetrouwbaar (race conditions, CSP). Daarom bakken we
    de juiste URL bij build-time in de HTML. Resultaat wordt gecached in
    seo/youtube_thumbs.json zodat we niet bij elke build 15× HTTP HEAD doen.
    """
    import json as _json
    import urllib.request as _ur
    cache_path = ROOT / "seo" / "youtube_thumbs.json"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    if cache_path.exists():
        cache = _json.loads(cache_path.read_text())
    else:
        cache = {}
    if vid in cache:
        return cache[vid]
    # Probeer in volgorde van kwaliteit, alleen 16:9 varianten
    for variant in ("maxresdefault", "hq720", "mqdefault"):
        url = f"https://i.ytimg.com/vi/{vid}/{variant}.jpg"
        try:
            req = _ur.Request(url, method="HEAD")
            with _ur.urlopen(req, timeout=4) as resp:
                if resp.status == 200 and int(resp.headers.get("Content-Length", 0)) > 3000:
                    cache[vid] = url
                    cache_path.write_text(_json.dumps(cache, indent=2))
                    return url
        except Exception:
            continue
    # Ultieme fallback - mqdefault is bij YouTube altijd aanwezig
    fallback = f"https://i.ytimg.com/vi/{vid}/mqdefault.jpg"
    cache[vid] = fallback
    cache_path.write_text(_json.dumps(cache, indent=2))
    return fallback


def video_section(r: dict) -> str:
    vid = r.get("video_id")
    if not vid:
        return ""
    title = r.get("video_title") or f"{r['name']} - officiële demonstratie"
    thumb = _best_youtube_thumb(vid)
    return f"""
<section style="background:var(--bg-2); border-top:1px solid var(--line); border-bottom:1px solid var(--line)">
  <div class="container">
    <div class="section-eyebrow">In actie</div>
    <h2 style="margin-bottom:8px">{escape(r['name'])} - officiële demo.</h2>
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
        "name": r.get("video_title") or f"{r['name']} - officiële demonstratie",
        "description": f"Officiële demonstratie van de {r['name']} humanoïde robot door {r['vendor']}.",
        "thumbnailUrl": [f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg", f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"],
        "uploadDate": "2025-01-01",
        "contentUrl": f"https://www.youtube.com/watch?v={vid}",
        "embedUrl": f"https://www.youtube.com/embed/{vid}",
        "publisher": {"@type": "Organization", "name": r["vendor"]},
    }, ensure_ascii=False)


TAG_TO_SECTOR = {
    "Industrie": ("productie-assemblage", "Productie &amp; assemblage"),
    "Industrieel": ("productie-assemblage", "Productie &amp; assemblage"),
    "Heavy-duty": ("productie-assemblage", "Productie &amp; assemblage"),
    "Cobot": ("productie-assemblage", "Productie &amp; assemblage"),
    "Mass-production": ("productie-assemblage", "Productie &amp; assemblage"),
    "Auto-industrie": ("productie-assemblage", "Productie &amp; assemblage"),
    "Hospitality": ("hospitality-retail", "Hospitality &amp; retail"),
    "Sociale-AI": ("hospitality-retail", "Hospitality &amp; retail"),
    "Service": ("hospitality-retail", "Hospitality &amp; retail"),
    "Demo": ("hospitality-retail", "Hospitality &amp; retail"),
    "Events": ("hospitality-retail", "Hospitality &amp; retail"),
    "3PL": ("3pl-fulfillment", "3PL &amp; fulfillment"),
    "Inspectie": ("3pl-fulfillment", "3PL &amp; fulfillment"),
    "Payload": ("3pl-fulfillment", "3PL &amp; fulfillment"),
    "Education": ("zorg-instellingen", "Zorg &amp; instellingen"),
}


def relevant_sectors(r: dict) -> list[tuple[str, str]]:
    """Mappet de tags van een robot op tot 3 sector-pagina's (uniek, geordend)."""
    seen = []
    for tag in r.get("tags", []):
        if tag in TAG_TO_SECTOR:
            slug_label = TAG_TO_SECTOR[tag]
            if slug_label not in seen:
                seen.append(slug_label)
        if len(seen) >= 3:
            break
    return seen


def faq_for_robot(r: dict) -> list[dict]:
    """Genereer 5 sectie-relevante FAQ Q&A's per robot voor on-page + FAQPage schema."""
    name = r["name"]
    price = f"€{r['lease_eur']:,}/mnd".replace(",", ".")
    setup = f"€{r['setup_eur']:,}".replace(",", ".")
    purchase = f"€{r['purchase_eur']:,}".replace(",", ".")
    is_avail = r["category"] == "available"

    levertijd = "Doorgaans 6-10 weken na bevestigde intake en getekend contract." if is_avail else \
        f"Niet direct leverbaar in 2026. Wij accepteren refundable reserveringen - zodra {r['vendor']} 3rd-party EU-verkoop opent (verwacht 2027) bemiddelt BotLease als eerste."

    sectoren = relevant_sectors(r)
    sector_str = ", ".join(label.replace("&amp;", "&") for _, label in sectoren) if sectoren else "diverse sectoren afhankelijk van de configuratie"

    return [
        {
            "q": f"Wat kost een {name} leasen via BotLease?",
            "a": f"{name} leasen kost {price} all-in operational lease (36 maanden). De eenmalige setup-fee is {setup} en dekt de gebruiksklare oplevering. De all-in maandprijs omvat preventief + correctief onderhoud, swap-SLA (vervangende unit bij storing), WA-verzekering wordt per deployment geregeld en Nederlandstalige helpdesk op werkdagen (spoedlijn bij storingen).",
        },
        {
            "q": f"Wat is de levertijd van een {name} in Nederland?",
            "a": levertijd,
        },
        {
            "q": f"Voor welke sectoren is de {name} geschikt?",
            "a": f"De {name} is geoptimaliseerd voor {sector_str}. Specifieke use-cases die bewezen of getest zijn: {', '.join(r['use_cases'][:3]).lower()}. Tijdens de gratis intake bepalen we of dit model past bij jouw concrete werkvloer.",
        },
        {
            "q": f"Kan ik een {name} ook kopen in plaats van leasen?",
            "a": f"De publieke aanschafprijs van een {name} ligt rond {purchase}. Operational lease via BotLease is meestal aantrekkelijker omdat het kapitaalslag voorkomt, de service-stack (onderhoud, swap, verzekering, compliance) is inbegrepen, en wij het restwaarde-risico dragen. Voor 5+ units kunnen we ook hybride structuren bespreken.",
        },
        {
            "q": f"Voldoet de {name} aan de EU AI-Act en Machineverordening?",
            "a": f"BotLease regelt voor elke deployment de importeurs- en CE-conformiteitskant onder de Machineverordening 2023/1230 (documentatie van de fabrikant verzamelen en controleren). De {name} wordt ingezet met menselijk toezicht (human-in-the-loop); werkzones op de werkvloer wijst de werkgever aan. De technische documentatie blijft up-to-date gedurende de leasetermijn.",
        },
    ]


def faqpage_jsonld(r: dict) -> str:
    faqs = faq_for_robot(r)
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
            for f in faqs
        ],
    }, ensure_ascii=False)



# Head-to-head vergelijkingen per robot (interne links robotpagina → /vergelijken/*)
_H2H_LINKS = {
  "unitree-g1": [("NEURA 4NE-1 Mini", "/vergelijken/unitree-g1-vs-neura-4ne1-mini")],
  "neura-4ne1-mini": [("Unitree G1", "/vergelijken/unitree-g1-vs-neura-4ne1-mini")],
  "unitree-h1-2": [("UBTECH Walker S2", "/vergelijken/unitree-h1-2-vs-ubtech-walker-s2"), ],
  "ubtech-walker-s2": [("Unitree H1-2", "/vergelijken/unitree-h1-2-vs-ubtech-walker-s2")],
  "neura-4ne1-gen3": [("Apptronik Apollo", "/vergelijken/neura-4ne1-gen3-vs-apptronik-apollo")],
  "apptronik-apollo": [("NEURA 4NE-1 Gen 3.5", "/vergelijken/neura-4ne1-gen3-vs-apptronik-apollo"), ("Figure 02", "/vergelijken/apptronik-apollo-vs-figure-02")],
  "unitree-r1": [("EngineAI SE01", "/vergelijken/unitree-r1-vs-engineai-se01")],
  "engineai-se01": [("Unitree R1", "/vergelijken/unitree-r1-vs-engineai-se01")],
  "figure-02": [("Apptronik Apollo", "/vergelijken/apptronik-apollo-vs-figure-02")],
}

def render_robot(r: dict, related: list) -> str:
    tier_class = {"eu": "tier-eu", "value": "tier-value", "premium": "tier-premium"}.get(r["tier"], "tier-eu")
    photo_url = f"{SITE_URL}{r['photo']}"
    use_cases_html = "".join(
        f'<div class="usecase-card"><div class="n">{i+1:d}</div><h3>{escape(uc)}</h3></div>'
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
        '<p style="background:rgba(255,201,102,0.1); border:1px solid rgba(255,201,102,0.45); '
        'border-radius:10px; padding:14px 18px; color:#7a4f00; font-size:14px; margin:18px 0; max-width:520px">'
        '⏳ Deze robot is nog niet commercieel leverbaar voor EU-derden. '
        '<a href="#wachtlijst" style="color:#7a4f00; font-weight:600; text-decoration:underline">Reserveer plek op wachtlijst</a> - '
        'BotLease krijgt prioriteit zodra ze beschikbaar komen.</p>'
    ) if r["category"] == "waitlist" else ""

    # GEO BLUF: "In het kort"-box (gelabelde feiten, citeerbaar door LLM's)
    _tldr_best = "; ".join((uc.rstrip('.')[:1].lower() + uc.rstrip('.')[1:]) for uc in r["use_cases"][:3])
    _tldr_tag = r["tagline"].rstrip()
    if not _tldr_tag.endswith('.'):
        _tldr_tag += '.'
    _h2h = _H2H_LINKS.get(r["slug"], [])
    _tldr_h2h = ("        <li><b style=\"color:var(--ink)\">Direct vergelijken:</b> "
                 + " · ".join(f'<a href="{href}" style="color:var(--accent)">vs {nm} →</a>' for nm, href in _h2h)
                 + "</li>\n") if _h2h else ""
    _tldr_avail = (
        f"Op wachtlijst - BotLease regelt priority-access bij {escape(r['vendor'])} zodra de EU-verkoop opent (verwacht Q4 2026 / Q1 2027)."
        if r["category"] == "waitlist"
        else "Leverbaar in Nederland - intake binnen 5 werkdagen, levering doorgaans 6-10 weken."
    )
    tldr_html = f"""<section style="background:var(--bg-2); border-top:1px solid var(--line); border-bottom:1px solid var(--line); padding:26px 0">
  <div class="container">
    <div style="max-width:620px">
      <div class="section-eyebrow" style="margin-bottom:12px">In het kort</div>
      <ul style="list-style:none; padding:0; margin:0; display:grid; gap:10px; color:var(--ink-2); font-size:15px; line-height:1.5">
        <li><b style="color:var(--ink)">Wat:</b> {escape(r['name'])} - humanoïde robot van {escape(r['vendor'])} ({escape(r['vendor_country'])}). {escape(_tldr_tag)}</li>
        <li><b style="color:var(--ink)">Leaseprijs:</b> all-in vanaf €{r['lease_eur']:,}/mnd, inclusief gebruiksklare oplevering, onderhoud en een vervangende unit bij storing.</li>
        <li><b style="color:var(--ink)">Beste voor:</b> {escape(_tldr_best)}.</li>
        <li><b style="color:var(--ink)">Leverbaarheid:</b> {_tldr_avail}</li>
{_tldr_h2h}      </ul>
      <p style="margin:14px 0 0; color:var(--ink-3); font-size:12.5px">Laatst bijgewerkt: 5 juni 2026 · leaseprijs indicatief, all-in per maand.</p>
    </div>
  </div>
</section>

"""

    # Dedicated waitlist form sectie alleen voor waitlist-modellen
    waitlist_form = ""
    if r["category"] == "waitlist":
        waitlist_form = f"""
<section id="wachtlijst" style="background:var(--bg-2); border-top:1px solid var(--line); border-bottom:1px solid var(--line)">
  <div class="container">
    <div style="display:grid; grid-template-columns:1fr; gap:48px; max-width:1080px; margin:0 auto" class="waitlist-grid">
      <div>
        <div class="section-eyebrow">Wachtlijst</div>
        <h2 style="margin:14px 0 16px">Reserveer een plek voor de {escape(r['name'])}.</h2>
        <p class="lede" style="margin-bottom:24px">Deze robot is in 2026 nog niet open verkocht voor EU-derden. BotLease heeft directe lijnen met {escape(r['vendor'])} en kan prioriteit-toegang regelen zodra commerciële verkoop opent - verwacht {('Q4 2026 / Q1 2027' if r['slug'] != '1x-neo' else 'Q1 2027')}.</p>
        <p style="color:var(--ink-2); font-size:14.5px; line-height:1.6">Wat krijg je door je aan te melden:</p>
        <ul style="color:var(--ink-2); font-size:14.5px; line-height:1.7; padding-left:22px; margin:14px 0 0">
          <li>Priority access zodra eerste EU-units beschikbaar zijn</li>
          <li>Eerst-recht op pilot-slot in jouw sector</li>
          <li>Maandelijkse update over levertijd + prijs</li>
          <li>Geen verplichting tot bestellen</li>
        </ul>
      </div>
      <form onsubmit="handleWaitlistSubmit(event)" data-robot-slug="{r['slug']}" data-robot-name="{escape(r['name'])}"
            style="background:var(--bg-2); border:1px solid var(--line); border-radius:14px; padding:32px">
        <input type="text" name="website" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
        <div style="margin-bottom:18px">
          <label for="wl-naam" style="display:block; font-size:13px; color:var(--ink-2); margin-bottom:6px; font-weight:500">Naam</label>
          <input id="wl-naam" name="naam" required placeholder="Voor- en achternaam"
                 style="width:100%; padding:12px 14px; background:var(--bg-3); border:1px solid var(--line); border-radius:8px; color:var(--ink); font-family:inherit; font-size:14.5px">
        </div>
        <div style="margin-bottom:18px">
          <label for="wl-bedrijf" style="display:block; font-size:13px; color:var(--ink-2); margin-bottom:6px; font-weight:500">Bedrijf</label>
          <input id="wl-bedrijf" name="bedrijf" required placeholder="Naam van je organisatie"
                 style="width:100%; padding:12px 14px; background:var(--bg-3); border:1px solid var(--line); border-radius:8px; color:var(--ink); font-family:inherit; font-size:14.5px">
        </div>
        <div style="margin-bottom:18px">
          <label for="wl-email" style="display:block; font-size:13px; color:var(--ink-2); margin-bottom:6px; font-weight:500">Werk-email</label>
          <input id="wl-email" name="email" type="email" required placeholder="naam@bedrijf.nl"
                 style="width:100%; padding:12px 14px; background:var(--bg-3); border:1px solid var(--line); border-radius:8px; color:var(--ink); font-family:inherit; font-size:14.5px">
        </div>
        <div style="margin-bottom:18px">
          <label for="wl-aantal" style="display:block; font-size:13px; color:var(--ink-2); margin-bottom:6px; font-weight:500">Verwacht aantal units</label>
          <select id="wl-aantal" name="usecase"
                 style="width:100%; padding:12px 14px; background:var(--bg-3); border:1px solid var(--line); border-radius:8px; color:var(--ink); font-family:inherit; font-size:14.5px">
            <option>1 unit (pilot)</option>
            <option>2-5 units</option>
            <option>6-10 units</option>
            <option>10+ units (enterprise)</option>
            <option>Nog onbekend</option>
          </select>
        </div>
        <div style="margin-bottom:18px">
          <label for="wl-bericht" style="display:block; font-size:13px; color:var(--ink-2); margin-bottom:6px; font-weight:500">Geplande use-case (optioneel)</label>
          <textarea id="wl-bericht" name="bericht" placeholder="Waar wil je deze robot inzetten?"
                    style="width:100%; padding:12px 14px; background:var(--bg-3); border:1px solid var(--line); border-radius:8px; color:var(--ink); font-family:inherit; font-size:14.5px; min-height:90px; resize:vertical"></textarea>
        </div>
        <button type="submit" class="btn"
                style="width:100%; justify-content:center">Reserveer plek op wachtlijst</button>
        <p class="form-note" style="color:var(--ink-3); font-size:12.5px; margin-top:12px; text-align:center">Geen verplichting · Reactie binnen 1-2 werkdagen</p>
      </form>
    </div>
  </div>
</section>
<style>
  @media (min-width: 880px) {{ .waitlist-grid {{ grid-template-columns: 1fr 1fr !important; gap: 64px !important; align-items: start; }} }}
/* leesbaarheid: prozaregels begrensd (de-slop, live-engine mat >85 tekens/regel) */
section.body p, section.body li { max-width:600px; }
section.body .cta-strip p, .cta-strip p { max-width:560px; margin-left:auto; margin-right:auto; }
details p { max-width:600px; }
.hub-hero p { max-width:600px; }
</style>"""

    # Voor waitlist-robots: eigen prijssectie met "Reserveer plek" CTA (geen aanvraag-form)
    waitlist_price_section = ""
    if r["category"] == "waitlist":
        waitlist_price_section = f"""
<section id="price">
  <div class="container">
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:40px; align-items:start">
      <div>
        <div class="section-eyebrow">Lease-prijs (indicatief)</div>
        <h2>All-in vanaf €{r['lease_eur']:,}/mnd.</h2>
        <p class="lede">36 maanden operational lease zodra leverbaar voor 3rd-party EU-derden. Definitieve prijs en condities afhankelijk van fabrikants-release.</p>
        <p style="color:var(--ink-3); font-size:14px">Aanschafprijs publiek: <b style="color:var(--ink)">€{r['purchase_eur']:,}</b>.</p>
      </div>
      <div class="price-block">
        <div class="price-row"><b>€{r['lease_eur']:,}</b><span class="per">/mnd · 36 mnd</span></div>
        <div class="setup">+ €{r['setup_eur']:,} eenmalige setup (gebruiksklare oplevering)</div>
        <ul>
          <li>Gebruiksklare oplevering met korte uitleg</li>
          <li>Preventief + correctief onderhoud</li>
          <li>Vervangende unit bij storing, doorgaans binnen enkele werkdagen</li>
          <li>WA-verzekering wordt per deployment geregeld + casco</li>
          <li>helpdesk op werkdagen Nederlands</li>
          <li>Software-updates en remote tuning</li>
        </ul>
        <a class="btn" href="#wachtlijst" style="display:block; text-align:center">Reserveer plek →</a>
      </div>
    </div>
  </div>
</section>"""

    # Unified AANVRAAG form - alleen voor available robots (waitlist heeft eigen form)
    order_form = ""
    if r["category"] == "available":
        order_form = f"""
<section id="aanvraag" style="background:var(--bg-2); border-top:1px solid var(--border); border-bottom:1px solid var(--border)">
  <div class="container">
    <div style="display:grid; grid-template-columns:1fr; gap:48px; max-width:1080px; margin:0 auto" class="aanvraag-grid">
      <div>
        <div class="section-eyebrow">Lease-prijs &amp; aanvraag</div>
        <h2 style="margin:14px 0 14px">Vraag deze {escape(r['name'])} aan.</h2>
        <p class="lede" style="margin-bottom:24px">All-in operational lease, 36 maanden. Geen investering vooraf, per maand opzegbaar na jaar 1.</p>

        <div style="background:var(--bg-card); border:1px solid var(--border-hover); border-radius:14px; padding:24px; margin-bottom:24px">
          <div style="display:flex; align-items:baseline; gap:6px; margin-bottom:8px">
            <b style="font-family:'Bricolage Grotesque', -apple-system, sans-serif; font-weight:700; font-size:40px; letter-spacing:-0.025em; color:var(--ink)">€{r['lease_eur']:,}</b>
            <span style="color:var(--ink-3); font-size:14px">/mnd · 36 mnd</span>
          </div>
          <div style="color:var(--ink-2); font-size:13.5px; margin-bottom:14px">+ €{r['setup_eur']:,} eenmalige setup (gebruiksklare oplevering)</div>
          <ul style="list-style:none; padding:0; margin:0; color:var(--ink-2); font-size:13.5px; line-height:1.7">
            <li style="padding-left:20px; position:relative"><span style="position:absolute; left:0; color:var(--green); font-weight:700">✓</span> Preventief + correctief onderhoud</li>
            <li style="padding-left:20px; position:relative"><span style="position:absolute; left:0; color:var(--green); font-weight:700">✓</span> Vervangende unit bij storing, doorgaans binnen enkele werkdagen</li>
            <li style="padding-left:20px; position:relative"><span style="position:absolute; left:0; color:var(--green); font-weight:700">✓</span> WA-verzekering wordt per deployment geregeld + casco</li>
            <li style="padding-left:20px; position:relative"><span style="position:absolute; left:0; color:var(--green); font-weight:700">✓</span> helpdesk op werkdagen Nederlands</li>
            <li style="padding-left:20px; position:relative"><span style="position:absolute; left:0; color:var(--green); font-weight:700">✓</span> Software-updates en remote tuning</li>
          </ul>
        </div>

        <p style="color:var(--ink-3); font-size:13px; line-height:1.55">Aanschafprijs publiek: <b style="color:var(--ink)">€{r['purchase_eur']:,}</b> - wij dragen het restwaarde-risico. Vrijblijvend, reactie binnen 1-2 werkdagen.</p>
      </div>
      <form onsubmit="handleAanvraagSubmit(event)" data-robot-slug="{r['slug']}" data-robot-name="{escape(r['name'])}"
            style="background:var(--bg-2); border:1px solid var(--line); border-radius:14px; padding:32px">
        <input type="text" name="website" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
        <div style="margin-bottom:18px">
          <label for="aanv-naam" style="display:block; font-size:13px; color:var(--ink-2); margin-bottom:6px; font-weight:500">Naam</label>
          <input id="aanv-naam" name="naam" required placeholder="Voor- en achternaam"
                 style="width:100%; padding:12px 14px; background:var(--bg-3); border:1px solid var(--line); border-radius:8px; color:var(--ink); font-family:inherit; font-size:14.5px">
        </div>
        <div style="margin-bottom:18px">
          <label for="aanv-bedrijf" style="display:block; font-size:13px; color:var(--ink-2); margin-bottom:6px; font-weight:500">Bedrijf</label>
          <input id="aanv-bedrijf" name="bedrijf" required placeholder="Naam van je organisatie"
                 style="width:100%; padding:12px 14px; background:var(--bg-3); border:1px solid var(--line); border-radius:8px; color:var(--ink); font-family:inherit; font-size:14.5px">
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:18px">
          <div>
            <label for="aanv-email" style="display:block; font-size:13px; color:var(--ink-2); margin-bottom:6px; font-weight:500">Werk-email</label>
            <input id="aanv-email" name="email" type="email" required placeholder="naam@bedrijf.nl"
                   style="width:100%; padding:12px 14px; background:var(--bg-3); border:1px solid var(--line); border-radius:8px; color:var(--ink); font-family:inherit; font-size:14.5px">
          </div>
          <div>
            <label for="aanv-telefoon" style="display:block; font-size:13px; color:var(--ink-2); margin-bottom:6px; font-weight:500">Telefoon <span style="color:var(--ink-3); font-weight:400">(optioneel)</span></label>
            <input id="aanv-telefoon" name="telefoon" placeholder="+31 ..."
                   style="width:100%; padding:12px 14px; background:var(--bg-3); border:1px solid var(--line); border-radius:8px; color:var(--ink); font-family:inherit; font-size:14.5px">
          </div>
        </div>
        <div style="margin-bottom:18px">
          <label for="aanv-stadium" style="display:block; font-size:13px; color:var(--ink-2); margin-bottom:6px; font-weight:500">Waar sta je in het proces?</label>
          <select id="aanv-stadium" name="usecase"
                 style="width:100%; padding:12px 14px; background:var(--bg-3); border:1px solid var(--line); border-radius:8px; color:var(--ink); font-family:inherit; font-size:14.5px">
            <option>Eerst meer info / oriënterend gesprek</option>
            <option>Pilot van 4 weken (€1.500) - indien beschikbaar</option>
            <option>Concrete lease-aanvraag (1 unit)</option>
            <option>Bulk-traject (3+ units)</option>
            <option>Anders - leg ik uit in bericht</option>
          </select>
          <p style="font-size:12px; color:var(--ink-3); margin-top:6px; font-style:italic; line-height:1.5">We bevestigen in het gesprek welk model voor jou geschikt is en welke vorm van kennismaking - online toelichting, video-demo of fysieke pilot - op dat moment realistisch is.</p>
        </div>
        <div style="margin-bottom:18px">
          <label for="aanv-bericht" style="display:block; font-size:13px; color:var(--ink-2); margin-bottom:6px; font-weight:500">Wat wil je oplossen? <span style="color:var(--ink-3); font-weight:400">(optioneel)</span></label>
          <textarea id="aanv-bericht" name="bericht" placeholder="Use-case, sector, deadline, vragen…"
                    style="width:100%; padding:12px 14px; background:var(--bg-3); border:1px solid var(--line); border-radius:8px; color:var(--ink); font-family:inherit; font-size:14.5px; min-height:96px; resize:vertical"></textarea>
        </div>
        <button type="submit" class="btn" style="width:100%; justify-content:center">Vraag aan</button>
        <p class="form-note" style="color:var(--ink-3); font-size:12.5px; margin-top:12px; text-align:center">Reactie binnen 1-2 werkdagen · Geen verplichting</p>
      </form>
    </div>
  </div>
</section>
<style>
  @media (min-width: 880px) {{ .aanvraag-grid {{ grid-template-columns: 1fr 1fr !important; gap: 64px !important; align-items: start; }} }}
</style>"""

    title_kw = f"{r['name']} leasen in Nederland - vanaf €{r['lease_eur']:,}/mnd | BotLease".replace(",", ".")
    # Cap meta-desc onder Google's ~155-char cut-off voor maximale CTR
    meta_desc = (
        f"{r['name']} leasen in Nederland vanaf €{r['lease_eur']:,}/mnd. "
        f"All-in operational lease: gebruiksklare oplevering, onderhoud, vervangende unit bij storing en verzekering."
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
<meta property="og:title" content="{escape(r['name'])} leasen - €{r['lease_eur']:,}/mnd | BotLease">
<meta property="og:description" content="{escape(r['tagline'])}">
<meta property="og:url" content="{SITE_URL}/robots/{r['slug']}">
<meta property="og:image" content="{photo_url}">
<meta property="og:site_name" content="BotLease">
<meta property="og:locale" content="nl_NL">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(r['name'])} leasen - €{r['lease_eur']:,}/mnd">
<meta name="twitter:description" content="{escape(r['tagline'])}">
<meta name="twitter:image" content="{photo_url}">

<link rel="preload" as="font" type="font/woff2" crossorigin href="/fonts/hanken-grotesk-latin-400-normal.woff2">
<link rel="preload" as="font" type="font/woff2" crossorigin href="/fonts/bricolage-grotesque-latin-700-normal.woff2">
<link rel="stylesheet" href="/fonts/fonts.css">
<style>{PAGE_CSS}{ROBOT_CSS}</style>
<script type="application/ld+json">{product_jsonld(r)}</script>
<script type="application/ld+json">{breadcrumb_jsonld(r)}</script>
<script type="application/ld+json">{faqpage_jsonld(r)}</script>
{f'<script type="application/ld+json">{video_jsonld(r)}</script>' if r.get('video_id') else ''}
<script type="application/ld+json">{ORG_SCHEMA}</script>
{HEAD_SEO}
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
        <h1>{escape(r['name'])} leasen in Nederland.</h1>
        <p class="tag">{escape(r['tagline'])}</p>
        <p class="lede">{escape(r['short'])}</p>
        {waitlist_notice}
        <div class="r-hero-cta">
          {('<a class="btn" href="#aanvraag">Vraag aan →</a>') if r['category'] == 'available' else ('<a class="btn" href="#wachtlijst">Reserveer plek →</a>')}
        </div>
      </div>
      <div class="r-hero-art">
        <img src="{r['photo']}" alt="{escape(r['name'])} humanoïde robot - {escape(r['vendor'])}" width="{r['photo_dims'][0]}" height="{r['photo_dims'][1]}">
      </div>
    </div>
  </div>
</section>

{tldr_html}<section class="r-quick">
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
    <p class="lede">Specifieke use-cases waar dit model getest of bewezen is - niet generiek "robots zijn handig".</p>
    <div class="usecases-grid">{use_cases_html}</div>
    {('<div style="margin-top:32px; padding-top:24px; border-top:1px solid var(--border); display:flex; flex-wrap:wrap; gap:10px; align-items:center"><span style="color:var(--ink-3); font-size:13.5px; font-weight:500; margin-right:6px">Geschikt voor sector:</span>' + "".join(f'<a href="/sectoren/{slug}" style="display:inline-block; padding:6px 14px; border-radius:999px; background:var(--bg-2); border:1px solid var(--border); color:var(--ink); font-size:13px; font-weight:500; text-decoration:none">{label} →</a>' for slug, label in relevant_sectors(r)) + '</div>') if relevant_sectors(r) else ''}

    <div style="margin-top:28px; padding:18px 22px; background:var(--bg-2); border:1px solid var(--border); border-radius:12px; font-size:14px; color:var(--ink-2); line-height:1.55">
      Nieuw met humanoid-lease? Lees onze <a href="/gids/humanoide-robot-leasen" style="color:var(--accent); font-weight:600; text-decoration:underline">complete gids over humanoïde robots leasen</a> -
      hoe het werkt, kosten, ROI-berekening en EU AI-Act compliance.
      Of bekijk <a href="/vergelijken/lease-vs-koop" style="color:var(--accent); font-weight:600; text-decoration:underline">lease vs. koop</a> en
      <a href="/kosten" style="color:var(--accent); font-weight:600; text-decoration:underline">de volledige prijslijst</a>.
    </div>
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

{order_form}

{waitlist_form}

{waitlist_price_section}

<section>
  <div class="container">
    <div class="section-eyebrow">Veelgestelde vragen</div>
    <h2>{escape(r['name'])} - vraag &amp; antwoord.</h2>
    <div style="max-width:820px; margin-top:24px">
      {"".join(f'<details style="border-top:1px solid var(--border); padding:0"><summary style="cursor:pointer; list-style:none; padding:20px 6px; font-size:17px; font-weight:500; letter-spacing:-0.01em; color:var(--ink); display:flex; justify-content:space-between; align-items:center; gap:20px">{escape(f["q"])}<span style="color:var(--ink-3); font-size:22px; font-weight:300">+</span></summary><p style="padding:0 6px 22px; font-size:15.5px; line-height:1.6; color:var(--ink-2); max-width:600px">{escape(f["a"])}</p></details>' for f in faq_for_robot(r))}
      <div style="border-top:1px solid var(--border)"></div>
    </div>
  </div>
</section>

<section style="background:var(--bg-2); border-top:1px solid var(--line)">
  <div class="container">
    <div class="section-eyebrow">Alternatieven</div>
    <h2>Vergelijk met andere modellen.</h2>
    <div class="compare-grid">{related_html}</div>
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

// Wachtlijst form handler → POST /api/contact met type=waitlist
function handleWaitlistSubmit(e) {{
  e.preventDefault();
  var form = e.target;
  var btn  = form.querySelector('button[type="submit"]');
  var note = form.querySelector('.form-note');
  var origBtn = btn.innerHTML;
  btn.disabled = true; btn.innerHTML = 'Versturen…';
  var data = Object.fromEntries(new FormData(form));
  data.type = 'waitlist';
  data.robot_slug = form.dataset.robotSlug || '';
  data.robot_name = form.dataset.robotName || '';

  fetch('/api/contact', {{
    method:'POST',
    headers:{{'Content-Type':'application/json'}},
    body: JSON.stringify(data),
  }})
    .then(function(r){{ return r.json().then(function(j){{ return {{ ok:r.ok, body:j }}; }}); }})
    .then(function(res){{
      if (res.ok && res.body.success) {{
        form.innerHTML = '<div style="text-align:center;padding:32px 0"><div style="display:inline-flex;align-items:center;justify-content:center;width:56px;height:56px;border-radius:50%;background:rgba(34,197,94,0.12);border:1px solid rgba(34,197,94,0.3);margin-bottom:20px"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"/></svg></div><h3 style="font-family:\\'Bricolage Grotesque\\',sans-serif;font-weight:600;font-size:20px;margin-bottom:10px;color:var(--ink)">Je staat op de wachtlijst</h3><p style="color:var(--ink-2);font-size:14.5px;line-height:1.55">Een bevestiging is verstuurd. Je hoort van ons zodra de eerste EU-units leverbaar zijn.</p></div>';
        if (window.umami) window.umami.track('waitlist_signup', {{ robot: data.robot_slug }});
      }} else {{
        if (note) {{ note.textContent = (res.body && res.body.error) || 'Er ging iets mis - probeer opnieuw'; note.style.color = '#dc2626'; }}
        btn.disabled = false; btn.innerHTML = origBtn;
      }}
    }})
    .catch(function(){{
      if (note) {{ note.textContent = 'Netwerkfout - mail naar hallo@botlease.nl'; note.style.color = '#dc2626'; }}
      btn.disabled = false; btn.innerHTML = origBtn;
    }});
}}

// Aanvraag-formulier handler → POST /api/contact met type=order
function handleAanvraagSubmit(e) {{
  e.preventDefault();
  var form = e.target;
  var btn  = form.querySelector('button[type="submit"]');
  var note = form.querySelector('.form-note');
  var origBtn = btn.innerHTML;
  btn.disabled = true; btn.innerHTML = 'Versturen…';
  var data = Object.fromEntries(new FormData(form));
  data.type = 'order';
  data.robot_slug = form.dataset.robotSlug || '';
  data.robot_name = form.dataset.robotName || '';

  fetch('/api/contact', {{
    method:'POST',
    headers:{{'Content-Type':'application/json'}},
    body: JSON.stringify(data),
  }})
    .then(function(r){{ return r.json().then(function(j){{ return {{ ok:r.ok, body:j }}; }}); }})
    .then(function(res){{
      if (res.ok && res.body.success) {{
        form.innerHTML = '<div style="text-align:center;padding:32px 0"><div style="display:inline-flex;align-items:center;justify-content:center;width:56px;height:56px;border-radius:50%;background:rgba(34,197,94,0.12);border:1px solid rgba(34,197,94,0.3);margin-bottom:20px"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"/></svg></div><h3 style="font-family:\\'Bricolage Grotesque\\',sans-serif;font-weight:600;font-size:20px;margin-bottom:10px;color:var(--ink)">Aanvraag ontvangen</h3><p style="color:var(--ink-2);font-size:14.5px;line-height:1.55">We nemen binnen 1-2 werkdagen contact op via je email om de aanvraag te bespreken.</p></div>';
        if (window.umami) window.umami.track('cta_aanvraag_submit', {{ source: 'robot', robot: data.robot_slug }});
      }} else {{
        if (note) {{ note.textContent = '// ' + ((res.body && res.body.error) || 'Probeer opnieuw'); note.style.color = '#f87171'; }}
        btn.disabled = false; btn.innerHTML = origBtn;
      }}
    }})
    .catch(function(){{
      if (note) {{ note.textContent = '// Netwerkfout - mail naar hallo@botlease.nl'; note.style.color = '#f87171'; }}
      btn.disabled = false; btn.innerHTML = origBtn;
    }});
}}

// Umami: aanvraag-form view + outbound source tracking
(function() {{
  function track(name, data) {{
    if (window.umami && typeof window.umami.track === 'function') {{
      window.umami.track(name, data || {{}});
    }}
  }}
  var form = document.querySelector('form[onsubmit*="Aanvraag"]') || document.querySelector('form[onsubmit*="Waitlist"]');
  if (form && 'IntersectionObserver' in window) {{
    var fired = false, robot = form.dataset.robotSlug || '';
    var io = new IntersectionObserver(function(es) {{
      es.forEach(function(e) {{
        if (e.isIntersecting && !fired) {{
          fired = true;
          track('cta_aanvraag_view', {{ source: 'robot', robot: robot }});
          io.disconnect();
        }}
      }});
    }}, {{ threshold: 0.3 }});
    io.observe(form);
  }}
}})();
</script>
</body>
</html>
"""


def render_hub() -> str:
    # Filter status/tier tags die al via tier-badge worden getoond
    SKIP_TAGS = {"EU-gebouwd", "Wachtlijst", "Bestseller", "Premium", "Instap", "Made in NL"}

    def card(r):
        price_text = f'€{r["lease_eur"]:,}/mnd'.replace(",", ".")
        use_tags = [t for t in r.get("tags", []) if t not in SKIP_TAGS][:3]
        tags_html = "".join(f'<span class="hub-tag">{escape(t)}</span>' for t in use_tags)
        return f"""<a href="/robots/{r['slug']}" class="hub-card">
            <div class="hub-thumb">
              <div class="hub-tags">{tags_html}</div>
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
        "name": "BotLease robot catalogus - humanoïde robots voor lease in Nederland",
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
<title>Humanoïde robots leasen | catalogus 2026 | BotLease</title>
<meta name="description" content="Catalogus humanoïde robots in Nederland - 13 modellen leasen vanaf €290/mnd. NEURA, Unitree, UBTECH, Apptronik vergeleken. All-in operational lease.">
<meta name="keywords" content="humanoide robot leasen Nederland, NEURA 4NE-1, Unitree leasen, Apptronik Apollo, Figure 02, humanoid catalogus 2026, robot huren MKB Nederland">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/robots/">

<meta property="og:type" content="website">
<meta property="og:title" content="Humanoïde robots leasen Nederland - 13 modellen vergelijken | BotLease">
<meta property="og:description" content="Complete catalogus humanoïde robots voor lease in Nederland: EU-gebouwd (NEURA, Pollen), Aziatisch (Unitree, UBTECH, EngineAI), wachtlijst (Apptronik, Figure, 1X NEO).">
<meta property="og:url" content="{SITE_URL}/robots/">
<meta property="og:image" content="{SITE_URL}/img/robots/neura-4ne1.webp">
<meta property="og:locale" content="nl_NL">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE_URL}/img/robots/neura-4ne1.webp">

<link rel="preload" as="font" type="font/woff2" crossorigin href="/fonts/hanken-grotesk-latin-400-normal.woff2">
<link rel="preload" as="font" type="font/woff2" crossorigin href="/fonts/bricolage-grotesque-latin-700-normal.woff2">
<link rel="stylesheet" href="/fonts/fonts.css">
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
    <p>13 modellen vergeleken, gerangschikt naar leverbaarheid. EU-gebouwde robots (NEURA, Pollen) eerst - voor de kortste supply chain en EU AI-Act compliance vanaf dag 1. Daarna Aziatische value-modellen, en de wachtlijst voor 2027.</p>
  </div>
</section>

<section class="hub-section">
  <div class="container">
    <div class="head">
      <span class="tier-badge tier-eu">EU-gebouwd · direct leverbaar</span>
      <h2 style="margin-top:14px">Europese humanoids - korte supply chain, EU AI-Act compliant.</h2>
      <p class="lede">Geproduceerd in Duitsland (NEURA) en Frankrijk (Pollen). EU AI-Act + Machineverordening 2023/1230 ready vanaf dag 1. Geen importheffingen, EU-talige support, GDPR by design.</p>
    </div>
    <div class="hub-grid">{eu_cards}</div>
  </div>
</section>

<section class="hub-section" style="background:var(--bg-2); border-top:1px solid var(--line); border-bottom:1px solid var(--line)">
  <div class="container">
    <div class="head">
      <span class="tier-badge tier-value">Aziatisch · direct leverbaar</span>
      <h2 style="margin-top:14px">Value-modellen uit China - agressief geprijsd, snel leverbaar.</h2>
      <p class="lede">Unitree, UBTECH en EngineAI verkopen via shop/EU-distributeurs. 6-10 weken levertijd. Lagere instapprijs maar let op AI-Act compliance assessment (BotLease regelt dit per deployment).</p>
    </div>
    <div class="hub-grid">{value_cards}</div>
  </div>
</section>

<section class="hub-section">
  <div class="container">
    <div class="head">
      <span class="tier-badge tier-premium">Wachtlijst 2026/2027</span>
      <h2 style="margin-top:14px">Premium Amerikaans/Aziatisch - wachtlijst.</h2>
      <p class="lede">Bewezen modellen die nog niet open verkocht worden in EU. Apptronik Apollo, Figure 02/03, Boston Dynamics Atlas - allemaal in pilot bij grote OEMs (Mercedes, BMW, Hyundai). BotLease faciliteert priority access zodra EU-verkoop open gaat.</p>
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
        (ROBOT_DIR / f"{r['slug']}.html").write_text(_fmt_nl(render_robot(r, related[:3])), encoding="utf-8")
    (ROBOT_DIR / "index.html").write_text(_fmt_nl(render_hub()), encoding="utf-8")
    print(f"✅ Built {len(ROBOTS)} robot pages + hub at /robots/")


if __name__ == "__main__":
    build()
