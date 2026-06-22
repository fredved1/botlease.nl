#!/usr/bin/env python3
"""
PROJECT X - onboarding-script (lokale referentie-implementatie).

"1 script per klant": leest een client-config.json en genereert deterministisch
een complete, gethematiseerde marketingsite + SEO/GEO-bestanden (sitemap, robots,
llms.txt). Dit is het CONFIG-DRIVEN, deterministische deel van de pipeline.

Wat dit script WEL doet (deterministisch, geen LLM nodig):
  - site-structuur (home + dienstpagina per service + contact + blog-index + auteur)
  - theming uit branding.colors (1-op-1 de :root CSS-vars)
  - volledige technische SEO per pagina (title/meta/canonical/OG/JSON-LD)
  - GEO-bestanden: sitemap.xml, robots.txt (AI-bots welkom), llms.txt (feitenkaart)
  - lead-formulier + AI-chat-widget met verplichte AI-disclosure (EU AI Act art. 50)

Wat in PRODUCTIE de Foundry content-agent invult (gemarkeerd met LLM-CONTENT-HOOK):
  - de wervende paginateksten en de blogartikelen (hier: nette templated copy
    uit de config-velden als placeholder, zodat de site zelfstandig oogt).

Gebruik:
  python3 onboard.py --config demo/client-config.json --out /tmp/klant-site
  python3 onboard.py --config <config> --out <dir> [--base-url https://...]

Het script is idempotent: opnieuw draaien overschrijft de output schoon.
"""
import argparse
import datetime
import html
import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------- config helpers
def load_config(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def clean(d):
    """Verwijder _comment/_*-velden zodat alleen echte config overblijft."""
    if isinstance(d, dict):
        return {k: clean(v) for k, v in d.items() if not k.startswith("_") and not k.startswith("$")}
    if isinstance(d, list):
        return [clean(x) for x in d]
    return d


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = (s.replace("ä", "a").replace("ë", "e").replace("ï", "i").replace("ö", "o")
          .replace("ü", "u").replace("é", "e").replace("è", "e").replace("ç", "c"))
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def esc(s) -> str:
    return html.escape(str(s or ""), quote=True)


def jsonld(obj) -> str:
    return ('<script type="application/ld+json">'
            + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>")


# ---------------------------------------------------------------- site model
class Site:
    def __init__(self, cfg: dict, base_url: str | None):
        c = clean(cfg)
        comp = c.get("company", {})
        self.name = (comp.get("trade_names") or [c.get("client_display_name", "Bedrijf")])[0]
        self.legal = comp.get("legal_name", self.name)
        self.description = comp.get("description", "")
        self.addr = comp.get("address", {})
        self.city = self.addr.get("city", "")
        niche = c.get("niche", {})
        self.industry = niche.get("industry", "")
        self.audience = niche.get("target_audience", "")
        self.services = niche.get("key_services", []) or []
        self.languages = niche.get("languages", ["nl"])
        b = c.get("branding", {})
        self.colors = b.get("colors", {})
        self.font = b.get("font_family", "Inter, system-ui, sans-serif")
        seo = c.get("seo_geo", {})
        self.keywords = seo.get("seed_keywords", []) or []
        self.author = seo.get("author", {})
        self.geo_enabled = seo.get("geo_enabled", True)
        cp = c.get("content_pipeline", {})
        self.topics = cp.get("topics", []) or []
        leads = c.get("leads", {})
        self.ai_disclosure = leads.get("ai_disclosure_text",
                                       "Je chat met een AI-assistent.")
        dom = c.get("domain", {})
        primary = dom.get("primary_domain", "example.nl")
        self.base = (base_url or f"https://{primary}").rstrip("/")
        self.is_fictional = "FICTIEF" in self.description.upper() or c.get("status") == "demo"
        self.generated = datetime.date.today().isoformat()
        # afgeleide
        self.author_slug = slugify(self.author.get("name", "auteur"))
        self.service_pages = [{"name": s, "slug": slugify(s)} for s in self.services]

    # ---- gedeelde HTML-shell met theming + SEO + JSON-LD ----
    def shell(self, *, title, desc, path, body, extra_ld=None, og_type="website"):
        col = self.colors
        accent = col.get("accent", "#0066cc")
        accent_soft = col.get("accent_soft", "#eaf2ff")
        bg = col.get("bg", "#ffffff")
        bg_card = col.get("bg_card", "#f5f6f8")
        text = col.get("text", "#1d1d1f")
        canonical = f"{self.base}{path}"
        org_ld = {
            "@context": "https://schema.org", "@type": "Organization",
            "@id": f"{self.base}/#organization", "name": self.name, "url": self.base + "/",
            "description": self.description,
            "address": {"@type": "PostalAddress", "addressLocality": self.city,
                        "addressCountry": self.addr.get("country", "NL")},
            "areaServed": self.city,
        }
        lds = [jsonld(org_ld)] + [jsonld(x) for x in (extra_ld or [])]
        nav = ('<nav class="nav"><a href="/" class="brand">' + esc(self.name) + "</a><div class=\"links\">"
               + "".join(f'<a href="/{p["slug"]}.html">{esc(p["name"])}</a>' for p in self.service_pages[:4])
               + '<a href="/blog/index.html">Blog</a><a href="/contact.html" class="cta">Contact</a></div></nav>')
        fict = ('<div class="fict">Let op: dit is een FICTIEF demo-bedrijf, gegenereerd door het '
                'PROJECT X onboarding-script. Geen echte onderneming.</div>' if self.is_fictional else "")
        footer = (f'<footer><div>{esc(self.name)}{" (" + esc(self.city) + ")" if self.city else ""} · '
                  f'<a href="/contact.html">Contact</a> · <a href="/privacy.html">Privacy</a> · '
                  f'<a href="/over-{esc(self.author_slug)}.html">Over ons</a></div>'
                  f'<div class="gen">Gegenereerd met PROJECT X · {self.generated}</div></footer>')
        return f"""<!DOCTYPE html>
<html lang="{esc(self.languages[0])}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canonical)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
{chr(10).join(lds)}
<style>
:root{{--accent:{accent};--accent-soft:{accent_soft};--bg:{bg};--bg-card:{bg_card};--text:{text};--font:{self.font}}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:var(--font);background:var(--bg);color:var(--text);line-height:1.6;font-size:16px}}
.wrap{{max-width:880px;margin:0 auto;padding:0 20px}}
.nav{{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;max-width:880px;margin:0 auto;padding:16px 20px;border-bottom:1px solid var(--bg-card)}}
.brand{{font-weight:800;font-size:19px;color:var(--text);text-decoration:none}}
.links a{{color:var(--text);text-decoration:none;margin-left:16px;font-size:14px;font-weight:500}}
.links a.cta{{background:var(--accent);color:#fff;padding:8px 16px;border-radius:99px}}
.fict{{background:#fff8e6;border-bottom:1px solid #f0d98a;color:#7a5b00;font-size:13px;text-align:center;padding:8px 16px}}
.hero{{padding:64px 0 40px}}
.hero h1{{font-size:clamp(30px,5vw,46px);letter-spacing:-.02em;line-height:1.1;margin-bottom:16px}}
.hero p.lead{{font-size:19px;color:var(--text);opacity:.8;max-width:620px}}
.btn{{display:inline-block;background:var(--accent);color:#fff;text-decoration:none;padding:13px 26px;border-radius:99px;font-weight:600;margin-top:24px}}
h2{{font-size:28px;margin:40px 0 14px;letter-spacing:-.01em}}
h3{{font-size:19px;margin:22px 0 8px}}
section{{padding:8px 0}}
.tldr{{background:var(--accent-soft);border-radius:14px;padding:20px 24px;margin:28px 0}}
.tldr b{{display:block;margin-bottom:6px}}
.grid{{display:grid;gap:16px;grid-template-columns:1fr;margin-top:16px}}
@media(min-width:680px){{.grid{{grid-template-columns:1fr 1fr}}}}
.card{{background:var(--bg-card);border-radius:14px;padding:20px 22px}}
.card a{{color:var(--accent);text-decoration:none;font-weight:600}}
.faq dt{{font-weight:600;margin-top:16px}}
.faq dd{{opacity:.85}}
form{{background:var(--bg-card);border-radius:14px;padding:22px;margin-top:20px}}
label{{display:block;font-size:14px;font-weight:600;margin:12px 0 4px}}
input,textarea{{width:100%;padding:11px 13px;border:1px solid #d8dadf;border-radius:9px;font-family:inherit;font-size:15px}}
.consent{{display:flex;gap:8px;align-items:flex-start;margin-top:14px;font-size:13px;font-weight:400}}
.consent input{{width:auto;margin-top:3px}}
.hp{{position:absolute;left:-9999px}}
button{{background:var(--accent);color:#fff;border:0;border-radius:99px;padding:13px 28px;font-weight:600;font-size:15px;margin-top:16px;cursor:pointer}}
.chat{{position:fixed;right:20px;bottom:20px;background:#fff;border:1px solid var(--bg-card);box-shadow:0 8px 30px rgba(0,0,0,.12);border-radius:14px;max-width:300px;padding:16px;font-size:13px}}
.chat .disc{{background:var(--accent-soft);border-radius:8px;padding:8px 10px;font-size:12px;margin-bottom:8px}}
footer{{border-top:1px solid var(--bg-card);margin-top:60px;padding:24px 20px;font-size:13px;opacity:.7;max-width:880px;margin-left:auto;margin-right:auto}}
footer a{{color:inherit}}.gen{{margin-top:6px;font-size:12px;opacity:.7}}
</style>
</head>
<body>
{fict}
{nav}
<main class="wrap">
{body}
</main>
{footer}
<div class="chat" aria-label="AI-assistent">
  <div class="disc">{esc(self.ai_disclosure)}</div>
  <div>Stel je vraag over {esc(self.services[0] if self.services else "onze diensten")}...</div>
</div>
</body>
</html>"""

    # ---- pagina's ----
    def home(self):
        kw = self.keywords[0] if self.keywords else self.industry
        title = f"{self.name} | {self.industry}"[:62]
        desc = (self.description[:150]).rsplit(" ", 1)[0] + "."
        faqs = [
            (f"Wat doet {self.name}?", self.description),
            (f"In welke regio werkt {self.name}?",
             f"Wij werken voor klanten in en rond {self.city}." if self.city else "Wij werken regionaal."),
            ("Wat kost het?", "Je krijgt een heldere offerte op maat na een gratis intake. "
                              "Bedragen zijn altijd indicatief tot de offerte."),
        ]
        faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
                  "mainEntity": [{"@type": "Question", "name": q,
                                  "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
        cards = "".join(
            f'<div class="card"><h3>{esc(p["name"])}</h3>'
            f'<p>Meer over {esc(p["name"]).lower()} bij {esc(self.name)}.</p>'
            f'<a href="/{p["slug"]}.html">Lees meer &rarr;</a></div>'
            for p in self.service_pages)
        faq_html = "".join(f"<dt>{esc(q)}</dt><dd>{esc(a)}</dd>" for q, a in faqs)
        body = f"""
<section class="hero">
  <h1>{esc(self.name)}{(" in " + esc(self.city)) if self.city else ""}</h1>
  <p class="lead">{esc(self.description)}</p>
  <a href="/contact.html" class="btn">Plan een gratis intake</a>
</section>
<div class="tldr"><b>In het kort</b>
{esc(self.name)} is actief in {esc(self.industry.lower())}{(" in de regio " + esc(self.city)) if self.city else ""}.
Diensten: {esc(", ".join(self.services))}. Vraag een vrijblijvende intake aan.</div>
<!-- LLM-CONTENT-HOOK: in productie vult de Foundry content-agent hier wervende, unieke hero- en sectieteksten in op basis van keyword "{esc(kw)}". -->
<section><h2>Onze diensten</h2><div class="grid">{cards}</div></section>
<section class="faq"><h2>Veelgestelde vragen</h2><dl>{faq_html}</dl></section>
"""
        return self.shell(title=title, desc=desc, path="/", body=body, extra_ld=[faq_ld])

    def service(self, p):
        title = f"{p['name']} | {self.name}"[:62]
        desc = f"{p['name']} bij {self.name}{(' in ' + self.city) if self.city else ''}. Vraag een vrijblijvende offerte aan."[:150]
        crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": self.base + "/"},
            {"@type": "ListItem", "position": 2, "name": p["name"], "item": f"{self.base}/{p['slug']}.html"}]}
        svc = {"@context": "https://schema.org", "@type": "Service", "serviceType": p["name"],
               "provider": {"@id": f"{self.base}/#organization"},
               "areaServed": self.city, "description": desc}
        faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f"Hoe werkt {p['name'].lower()} bij {self.name}?",
             "acceptedAnswer": {"@type": "Answer", "text": "We starten met een gratis intake, geven daarna een "
                                "heldere offerte en plannen de uitvoering met een vaste contactpersoon."}}]}
        body = f"""
<nav style="font-size:13px;opacity:.6;padding-top:18px"><a href="/" style="color:inherit">Home</a> / {esc(p['name'])}</nav>
<section class="hero" style="padding-top:24px">
  <h1>{esc(p['name'])}</h1>
  <p class="lead">{esc(p['name'])} door {esc(self.name)}{(", voor klanten in en rond " + esc(self.city)) if self.city else ""}.</p>
  <a href="/contact.html" class="btn">Vraag een offerte aan</a>
</section>
<div class="tldr"><b>In het kort</b> {esc(p['name'])} bij {esc(self.name)}: gratis intake, heldere offerte, vaste contactpersoon.</div>
<!-- LLM-CONTENT-HOOK: Foundry content-agent vult hier de volledige dienst-uitleg, proces, prijsindicatie en cases in (config-driven, per service). -->
<section><h2>Waarom {esc(self.name)}?</h2>
<p>{esc(self.audience or ("Wij helpen klanten in en rond " + self.city + " verder."))}</p></section>
<section class="faq"><h2>Veelgestelde vraag</h2>
<dl><dt>Hoe werkt {esc(p['name'].lower())}?</dt>
<dd>We starten met een gratis intake, geven daarna een heldere offerte en plannen de uitvoering met een vaste contactpersoon.</dd></dl></section>
"""
        return self.shell(title=title, desc=desc, path=f"/{p['slug']}.html", body=body,
                          extra_ld=[crumb, svc, faq_ld])

    def contact(self):
        title = f"Contact | {self.name}"[:62]
        desc = f"Neem contact op met {self.name}{(' in ' + self.city) if self.city else ''} voor een vrijblijvende intake."[:150]
        cp = {"@context": "https://schema.org", "@type": "ContactPoint", "contactType": "sales",
              "areaServed": self.city, "availableLanguage": self.languages}
        body = f"""
<section class="hero" style="padding-top:40px">
  <h1>Contact</h1>
  <p class="lead">Plan een vrijblijvende intake met {esc(self.name)}. We reageren op werkdagen.</p>
</section>
<form onsubmit="return false">
  <p style="font-size:13px;opacity:.7">Demo-formulier. In productie gaat dit naar een Azure Function en de lead-agent.</p>
  <label>Naam</label><input type="text" name="naam" required>
  <label>E-mail</label><input type="email" name="email" required>
  <label>Je vraag</label><textarea name="bericht" rows="4"></textarea>
  <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
  <div class="consent"><input type="checkbox" required>
    <span>Ik ga akkoord met de <a href="/privacy.html">privacyverklaring</a>. Mijn gegevens worden alleen
    gebruikt om mijn aanvraag te behandelen (AVG).</span></div>
  <button>Verstuur aanvraag</button>
</form>
"""
        return self.shell(title=title, desc=desc, path="/contact.html", body=body, extra_ld=[cp])

    def author_page(self):
        a = self.author
        name = a.get("name", "Auteur")
        title = f"Over {name} | {self.name}"[:62]
        desc = f"{name}, {a.get('job_title', '')} bij {self.name}."[:150]
        person = {"@context": "https://schema.org", "@type": "Person", "name": name,
                  "jobTitle": a.get("job_title", ""), "worksFor": {"@id": f"{self.base}/#organization"},
                  "description": a.get("bio", "")}
        body = f"""
<section class="hero" style="padding-top:40px">
  <h1>{esc(name)}</h1>
  <p class="lead">{esc(a.get('job_title', ''))}</p>
</section>
<section><p>{esc(a.get('bio', ''))}</p></section>
"""
        return self.shell(title=title, desc=desc, path=f"/over-{self.author_slug}.html", body=body,
                          extra_ld=[person], og_type="profile")

    def blog_index(self):
        title = f"Blog | {self.name}"[:62]
        desc = f"Kennis en tips van {self.name} over {esc(self.industry.lower())}."[:150]
        items = self.topics[:5] or ["Eerste artikel"]
        blog_ld = {"@context": "https://schema.org", "@type": "Blog", "name": f"{self.name} blog",
                   "url": f"{self.base}/blog/index.html"}
        cards = "".join(
            f'<div class="card"><h3>{esc(t)}</h3>'
            f'<p>Onderwerp gepland in de content-pijplijn.</p>'
            f'<span style="font-size:13px;opacity:.6">Wordt automatisch gepubliceerd</span></div>'
            for t in items)
        body = f"""
<section class="hero" style="padding-top:40px"><h1>Blog</h1>
<p class="lead">Kennis en tips van {esc(self.name)}.</p></section>
<!-- LLM-CONTENT-HOOK: de content-agent (Foundry, op cadans uit content_pipeline.cadence_cron) schrijft elk artikel, passeert de editorial+feitcheck-gate, en publiceert het hier. -->
<div class="grid">{cards}</div>
"""
        return self.shell(title=title, desc=desc, path="/blog/index.html", body=body, extra_ld=[blog_ld])

    def privacy(self):
        title = f"Privacy | {self.name}"[:62]
        body = f"""
<section class="hero" style="padding-top:40px"><h1>Privacyverklaring</h1></section>
<section><p>{esc(self.name)} verwerkt persoonsgegevens uitsluitend om aanvragen te behandelen,
conform de AVG. Gegevens worden niet langer bewaard dan nodig en niet aan derden verkocht.
Dit is een door PROJECT X gegenereerde basisversie; in productie wordt deze juridisch getoetst.</p></section>
"""
        return self.shell(title=title, desc=f"Privacyverklaring van {self.name}.", path="/privacy.html", body=body)

    # ---- SEO/GEO-bestanden ----
    def urls(self):
        u = ["/", "/contact.html", "/blog/index.html", "/privacy.html",
             f"/over-{self.author_slug}.html"]
        u += [f"/{p['slug']}.html" for p in self.service_pages]
        return u

    def sitemap(self):
        out = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for path in self.urls():
            prio = "1.0" if path == "/" else "0.8"
            out.append(f"  <url><loc>{self.base}{path}</loc><lastmod>{self.generated}</lastmod>"
                       f"<changefreq>weekly</changefreq><priority>{prio}</priority></url>")
        out.append("</urlset>")
        return "\n".join(out) + "\n"

    def robots(self):
        ai_bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "ClaudeBot",
                   "Claude-Web", "Google-Extended", "Applebot-Extended", "CCBot"]
        lines = ["# robots.txt - AI-crawlers expliciet welkom (GEO)"]
        for b in ai_bots:
            lines += [f"User-agent: {b}", "Allow: /", ""]
        lines += ["User-agent: *", "Allow: /", "", f"Sitemap: {self.base}/sitemap.xml", ""]
        return "\n".join(lines)

    def llms(self):
        svc = "\n".join(f"- {s}" for s in self.services)
        kw = ", ".join(self.keywords)
        fict = ("\n> LET OP: FICTIEF demo-bedrijf, gegenereerd door PROJECT X. Geen echte onderneming.\n"
                if self.is_fictional else "")
        return f"""# {self.name} - llms.txt (citeerbare feitenkaart)
_Laatst bijgewerkt: {self.generated}_
{fict}
## Wat
{self.description}

## Bedrijf
- Naam: {self.name}
- Branche: {self.industry}
- Werkgebied: {self.city or "regionaal (NL)"}
- Doelgroep: {self.audience}

## Diensten
{svc}

## Relevante zoekwoorden
{kw}

## Auteur / expertise (E-E-A-T)
- {self.author.get("name", "")} - {self.author.get("job_title", "")}

## Toon en grenzen
Prijzen zijn altijd indicatief tot een persoonlijke offerte. Geen bindende beloftes zonder intake.
"""


# ---------------------------------------------------------------- runner
def build(config_path: Path, out_dir: Path, base_url: str | None):
    cfg = load_config(config_path)
    site = Site(cfg, base_url)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "blog").mkdir(exist_ok=True)

    written = []

    def w(rel, content):
        p = out_dir / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        written.append(rel)

    w("index.html", site.home())
    for p in site.service_pages:
        w(f"{p['slug']}.html", site.service(p))
    w("contact.html", site.contact())
    w(f"over-{site.author_slug}.html", site.author_page())
    w("blog/index.html", site.blog_index())
    w("privacy.html", site.privacy())
    w("sitemap.xml", site.sitemap())
    w("robots.txt", site.robots())
    w("llms.txt", site.llms())

    print(f"\n  PROJECT X onboarding - {site.name}")
    print(f"  {'-' * 48}")
    print(f"  niche      : {site.industry}")
    print(f"  werkgebied : {site.city}")
    print(f"  diensten   : {len(site.services)}  -> {len(site.service_pages)} dienstpagina's")
    print(f"  kleuren    : accent {site.colors.get('accent')}  text {site.colors.get('text')}")
    print(f"  base-url   : {site.base}")
    print(f"  bestanden  : {len(written)} geschreven naar {out_dir}")
    for f in written:
        print(f"               - {f}")
    print(f"\n  Open: file://{(out_dir / 'index.html').resolve()}\n")
    return written


def main():
    ap = argparse.ArgumentParser(description="PROJECT X onboarding: client-config.json -> marketingsite + SEO/GEO.")
    ap.add_argument("--config", required=True, type=Path, help="pad naar client-config.json")
    ap.add_argument("--out", required=True, type=Path, help="output-map voor de site")
    ap.add_argument("--base-url", default=None, help="override base-URL (default: https://<primary_domain>)")
    args = ap.parse_args()
    if not args.config.exists():
        sys.exit(f"config niet gevonden: {args.config}")
    build(args.config, args.out, args.base_url)


if __name__ == "__main__":
    main()
