#!/usr/bin/env python3
"""
BotLease news generator.

Builds:
- frontend/nieuws/index.html          (listing page)
- frontend/nieuws/<slug>.html         (one HTML file per article)
- frontend/sitemap.xml                (incl. main page + every article)
- frontend/robots.txt
- frontend/rss.xml                    (RSS feed for syndicators / Google News)
- frontend/data/articles.json         (machine-readable index)

Designed to be idempotent: rerunning is safe.
"""
from __future__ import annotations
import json
import re
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"
NEWS_DIR = FRONTEND / "nieuws"
DATA_DIR = FRONTEND / "data"
SITE_URL = "https://botlease.nl"

sys.path.insert(0, str(ROOT / "scripts"))
from articles_data import ARTICLES  # noqa: E402


# ---------------------------------------------------------------- helpers
def fmt_date_nl(iso: str) -> str:
    mnd = ["januari","februari","maart","april","mei","juni",
           "juli","augustus","september","oktober","november","december"]
    d = datetime.strptime(iso, "%Y-%m-%d")
    return f"{d.day} {mnd[d.month-1]} {d.year}"


def render_body(body) -> str:
    out = []
    for tag, content in body:
        if tag == "p":
            out.append(f"<p>{content}</p>")
        elif tag == "h2":
            out.append(f"<h2>{escape(content)}</h2>")
        elif tag == "h3":
            out.append(f"<h3>{escape(content)}</h3>")
        elif tag == "ul":
            items = "".join(f"<li>{escape(it)}</li>" for it in content)
            out.append(f"<ul>{items}</ul>")
        elif tag == "quote":
            out.append(f"<blockquote><p>{content}</p></blockquote>")
    return "\n".join(out)


def render_sources(sources) -> str:
    if not sources:
        return ""
    items = "\n".join(
        f'<li><a href="{escape(url)}" target="_blank" rel="noopener nofollow">{escape(name)}</a></li>'
        for name, url in sources
    )
    return f'<section class="sources"><h3>Bronnen</h3><ol>{items}</ol></section>'


# --------------- shared CSS so every page voelt consistent
PAGE_CSS = """
*,*::before,*::after { margin:0; padding:0; box-sizing:border-box; }
:root {
  --bg:#08080a; --bg-2:#0e0e12; --bg-3:#16161c; --line:#23232c; --line-2:#2e2e38;
  --ink:#f7f7f9; --ink-2:#a5a5b3; --ink-3:#666672;
  --accent:#ff5e1f; --accent-2:#ffb098; --green:#5be584;
}
html { scroll-behavior:smooth; }
body { font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif; background:var(--bg); color:var(--ink); line-height:1.65; -webkit-font-smoothing:antialiased; }
h1,h2,h3,h4 { font-family:'Space Grotesk',sans-serif; letter-spacing:-0.025em; line-height:1.15; font-weight:600; }
a { color:inherit; text-decoration:none; }
.container { max-width:1180px; margin:0 auto; padding:0 28px; }
.narrow { max-width:760px; margin:0 auto; padding:0 28px; }

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

footer { padding:56px 0 36px; border-top:1px solid var(--line); background:var(--bg-2); margin-top:120px; }
footer .row { display:flex; justify-content:space-between; flex-wrap:wrap; gap:20px; color:var(--ink-3); font-size:13px; align-items:center; }
footer a { color:var(--ink-2); }
footer a:hover { color:var(--ink); }

@media (max-width:780px) { .nav-links { display:none; } }
"""

LISTING_CSS = """
.news-hero { padding:140px 0 60px; position:relative; overflow:hidden; }
.news-hero::before { content:""; position:absolute; inset:0; background:radial-gradient(50% 50% at 80% 20%, rgba(255,94,31,0.18), transparent 60%); z-index:0; }
.news-hero .container { position:relative; z-index:2; }
.eyebrow { display:inline-block; color:var(--accent); font-size:12px; text-transform:uppercase; letter-spacing:0.16em; font-weight:600; margin-bottom:14px; padding:5px 12px; background:rgba(255,94,31,0.08); border:1px solid rgba(255,94,31,0.2); border-radius:999px; }
.news-hero h1 { font-size:clamp(36px,4.8vw,60px); margin-bottom:18px; letter-spacing:-0.035em; }
.news-hero p { color:var(--ink-2); font-size:18px; max-width:680px; }
.news-feed { padding:30px 0 80px; }
.news-grid { display:grid; grid-template-columns:1fr 1fr; gap:24px; }
article.card { background:var(--bg-2); border:1px solid var(--line); border-radius:18px; padding:30px 28px; transition:transform .25s, border-color .25s, box-shadow .25s; display:flex; flex-direction:column; min-height:300px; }
article.card:hover { transform:translateY(-3px); border-color:var(--line-2); box-shadow:0 30px 60px -30px rgba(0,0,0,0.5); }
article.card .meta { display:flex; gap:10px; align-items:center; margin-bottom:14px; }
article.card .cat { font-family:'Space Grotesk'; color:var(--accent); font-size:11px; text-transform:uppercase; letter-spacing:0.12em; font-weight:600; padding:4px 10px; background:rgba(255,94,31,0.08); border:1px solid rgba(255,94,31,0.2); border-radius:999px; }
article.card .date { color:var(--ink-3); font-size:13px; }
article.card h2 { font-size:23px; line-height:1.25; margin-bottom:10px; letter-spacing:-0.02em; }
article.card h2 a:hover { color:var(--accent-2); }
article.card p.lede { color:var(--ink-2); font-size:14.5px; line-height:1.6; margin-bottom:20px; flex:1; }
article.card .footer-line { display:flex; justify-content:space-between; align-items:center; padding-top:18px; border-top:1px solid var(--line); font-size:13px; color:var(--ink-3); }
article.card .read-more { color:var(--accent-2); font-weight:600; }
article.card.featured { grid-column:span 2; background:linear-gradient(135deg, rgba(255,94,31,0.08), rgba(255,94,31,0.02)); border-color:rgba(255,94,31,0.25); }
article.card.featured h2 { font-size:30px; max-width:680px; }
article.card.featured p.lede { font-size:16px; max-width:680px; }
@media (max-width:780px) {
  .news-grid { grid-template-columns:1fr; }
  article.card.featured { grid-column:span 1; }
  article.card.featured h2 { font-size:24px; }
}
"""

ARTICLE_CSS = """
.article-hero { padding:130px 0 30px; position:relative; }
.article-hero::before { content:""; position:absolute; inset:0; background:radial-gradient(40% 40% at 80% 0%, rgba(255,94,31,0.12), transparent 70%); z-index:0; }
.article-hero .narrow { position:relative; z-index:2; }
.crumbs { display:flex; gap:8px; font-size:13px; color:var(--ink-3); margin-bottom:24px; }
.crumbs a:hover { color:var(--ink-2); }
.crumbs .sep { color:var(--line-2); }
article.full .meta { display:flex; flex-wrap:wrap; gap:12px; align-items:center; margin-bottom:20px; font-size:13.5px; color:var(--ink-3); }
article.full .cat { font-family:'Space Grotesk'; color:var(--accent); font-size:11px; text-transform:uppercase; letter-spacing:0.12em; font-weight:600; padding:4px 10px; background:rgba(255,94,31,0.08); border:1px solid rgba(255,94,31,0.2); border-radius:999px; }
article.full h1 { font-size:clamp(34px,4.5vw,52px); margin-bottom:18px; letter-spacing:-0.035em; line-height:1.1; }
article.full .subtitle { font-size:19px; color:var(--ink-2); margin-bottom:32px; line-height:1.5; }
article.full .body { padding:32px 0 0; }
article.full .body p, article.full .body ul { font-size:16.5px; color:var(--ink); margin-bottom:22px; line-height:1.75; }
article.full .body ul { padding-left:24px; }
article.full .body li { margin-bottom:8px; }
article.full .body h2 { font-size:26px; margin:48px 0 18px; letter-spacing:-0.025em; }
article.full .body h3 { font-size:20px; margin:32px 0 14px; }
article.full .body a { color:var(--accent-2); text-decoration:underline; text-decoration-color:rgba(255,176,152,0.3); text-underline-offset:3px; }
article.full .body a:hover { text-decoration-color:var(--accent-2); }
article.full blockquote { border-left:3px solid var(--accent); padding:8px 0 8px 24px; margin:24px 0; font-size:19px; color:var(--ink); font-style:italic; }
.sources { margin-top:56px; padding:32px; background:var(--bg-2); border:1px solid var(--line); border-radius:14px; }
.sources h3 { font-size:14px; text-transform:uppercase; letter-spacing:0.1em; color:var(--ink-3); margin-bottom:18px; font-family:'Space Grotesk'; }
.sources ol { padding-left:22px; }
.sources li { color:var(--ink-2); font-size:14.5px; margin-bottom:8px; }
.sources a { color:var(--accent-2); text-decoration:underline; text-decoration-color:rgba(255,176,152,0.4); }
.tags { margin-top:28px; display:flex; flex-wrap:wrap; gap:8px; }
.tags span { font-size:12px; color:var(--ink-2); background:var(--bg-3); border:1px solid var(--line); padding:4px 10px; border-radius:999px; }
.cta-strip { margin-top:60px; padding:32px; background:linear-gradient(135deg, #ff5e1f, #c2400d); border-radius:18px; text-align:center; }
.cta-strip h3 { font-size:24px; margin-bottom:8px; }
.cta-strip p { opacity:0.92; margin-bottom:20px; }
.cta-strip .btn { background:#0a0a0c; }
.related { margin-top:80px; padding-top:48px; border-top:1px solid var(--line); }
.related h3 { font-size:14px; text-transform:uppercase; letter-spacing:0.1em; color:var(--ink-3); margin-bottom:22px; }
.related-grid { display:grid; grid-template-columns:1fr 1fr; gap:18px; }
.related a { display:block; padding:20px 22px; background:var(--bg-2); border:1px solid var(--line); border-radius:12px; transition:border-color .2s, transform .2s; }
.related a:hover { border-color:var(--line-2); transform:translateY(-2px); }
.related .cat { font-size:11px; color:var(--accent); text-transform:uppercase; letter-spacing:0.1em; font-weight:600; }
.related .t { font-family:'Space Grotesk'; font-weight:600; margin-top:6px; line-height:1.3; }
@media (max-width:780px) { .related-grid { grid-template-columns:1fr; } }
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
      <a href="/#robots">Robots</a>
      <a href="/#cases">Toepassingen</a>
      <a href="/nieuws" class="active">Nieuws</a>
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
    <div><a href="/">Home</a> · <a href="/nieuws">Nieuws</a> · <a href="/#contact">Contact</a> · <a href="/sitemap.xml">Sitemap</a> · <a href="/rss.xml">RSS</a></div>
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
    "sameAs": []
}, ensure_ascii=False)


# ---------------------------------------------------------------- builders

def article_jsonld(a: dict) -> str:
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": a["title"],
        "description": a["subtitle"],
        "datePublished": a["date"] + "T08:00:00+01:00",
        "dateModified": a["date"] + "T08:00:00+01:00",
        "author": {"@type": "Organization", "name": a.get("author", "BotLease Redactie")},
        "publisher": {"@type": "Organization", "name": "BotLease",
                      "logo": {"@type": "ImageObject", "url": f"{SITE_URL}/logo.png"}},
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{SITE_URL}/nieuws/{a['slug']}"},
        "keywords": ", ".join(a.get("tags", [])),
        "articleSection": a.get("category", "Nieuws"),
        "inLanguage": "nl-NL",
    }, ensure_ascii=False)


def render_article(a: dict, related: list) -> str:
    related_html = "".join(
        f'<a href="/nieuws/{r["slug"]}"><div class="cat">{escape(r["category"])}</div><div class="t">{escape(r["title"])}</div></a>'
        for r in related[:2]
    )
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(a['title'])} | BotLease Nieuws</title>
<meta name="description" content="{escape(a['subtitle'])}">
<meta name="keywords" content="{escape(', '.join(a.get('tags', [])))}, humanoide robot, robot lease, Nederland">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="author" content="BotLease">
<link rel="canonical" href="{SITE_URL}/nieuws/{a['slug']}">

<meta property="og:type" content="article">
<meta property="og:title" content="{escape(a['title'])}">
<meta property="og:description" content="{escape(a['subtitle'])}">
<meta property="og:url" content="{SITE_URL}/nieuws/{a['slug']}">
<meta property="og:site_name" content="BotLease">
<meta property="og:locale" content="nl_NL">
<meta property="article:published_time" content="{a['date']}T08:00:00+01:00">
<meta property="article:section" content="{escape(a.get('category', 'Nieuws'))}">
{''.join(f'<meta property="article:tag" content="{escape(t)}">' for t in a.get('tags', []))}

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(a['title'])}">
<meta name="twitter:description" content="{escape(a['subtitle'])}">

<link rel="alternate" type="application/rss+xml" title="BotLease Nieuws" href="{SITE_URL}/rss.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>{PAGE_CSS}{ARTICLE_CSS}</style>
<script type="application/ld+json">{article_jsonld(a)}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
</head>
<body>
{NAV_HTML}

<section class="article-hero">
  <div class="narrow">
    <nav class="crumbs">
      <a href="/">Home</a>
      <span class="sep">/</span>
      <a href="/nieuws">Nieuws</a>
      <span class="sep">/</span>
      <span>{escape(a.get('category',''))}</span>
    </nav>
    <article class="full">
      <div class="meta">
        <span class="cat">{escape(a.get('category', 'Nieuws'))}</span>
        <span>{escape(fmt_date_nl(a['date']))}</span>
        <span>·</span>
        <span>{a.get('reading_time', 5)} min lezen</span>
      </div>
      <h1>{escape(a['title'])}</h1>
      <p class="subtitle">{escape(a['subtitle'])}</p>
      <div class="body">
        <p><strong>{escape(a['intro'])}</strong></p>
        {render_body(a['body'])}
      </div>
      {render_sources(a.get('sources', []))}
      <div class="tags">{''.join(f'<span>{escape(t)}</span>' for t in a.get('tags', []))}</div>
      <div class="cta-strip">
        <h3>Klaar om dit zelf te ervaren?</h3>
        <p>Een pilot van 4 weken kost €1.500. Lease vanaf €899/mnd. Beslis na 4 weken.</p>
        <a class="btn" href="/#contact">Plan een demo →</a>
      </div>
      {f'<div class="related"><h3>Lees verder</h3><div class="related-grid">{related_html}</div></div>' if related_html else ''}
    </article>
  </div>
</section>

{FOOTER_HTML}
</body>
</html>
"""


def render_listing(articles: list) -> str:
    articles_sorted = sorted(articles, key=lambda a: a["date"], reverse=True)
    cards = []
    for i, a in enumerate(articles_sorted):
        featured = " featured" if i == 0 else ""
        cards.append(f'''
        <article class="card{featured}">
          <div class="meta">
            <span class="cat">{escape(a.get('category', 'Nieuws'))}</span>
            <span class="date">{escape(fmt_date_nl(a['date']))}</span>
          </div>
          <h2><a href="/nieuws/{a['slug']}">{escape(a['title'])}</a></h2>
          <p class="lede">{escape(a['subtitle'])}</p>
          <div class="footer-line">
            <span>{a.get('reading_time', 5)} min lezen</span>
            <a class="read-more" href="/nieuws/{a['slug']}">Lees artikel →</a>
          </div>
        </article>''')

    itemlist_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "BotLease — Nieuws over humanoïde robots",
        "itemListElement": [
            {"@type": "ListItem", "position": idx + 1,
             "url": f"{SITE_URL}/nieuws/{a['slug']}",
             "name": a["title"]}
            for idx, a in enumerate(articles_sorted)
        ]
    }, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nieuws & analyse over humanoïde robots in Nederland | BotLease</title>
<meta name="description" content="Dagelijks nieuws en analyses over humanoïde robots: Unitree, Figure, Apptronik, Agility, 1X. Use-cases, regelgeving, marktanalyses en pilot-data uit Nederland.">
<meta name="keywords" content="humanoide robot nieuws, robot Nederland, Unitree nieuws, Figure 02, Apollo Apptronik, Agility Digit, robot lease nieuws, AI Act robot">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/nieuws/">

<meta property="og:type" content="website">
<meta property="og:title" content="BotLease Nieuws — humanoïde robots in Nederland">
<meta property="og:description" content="Dagelijkse analyses over humanoïde robots, Nederlandse use-cases en marktontwikkelingen.">
<meta property="og:url" content="{SITE_URL}/nieuws/">
<meta property="og:locale" content="nl_NL">

<link rel="alternate" type="application/rss+xml" title="BotLease Nieuws" href="{SITE_URL}/rss.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>{PAGE_CSS}{LISTING_CSS}</style>
<script type="application/ld+json">{itemlist_jsonld}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
</head>
<body>
{NAV_HTML}

<section class="news-hero">
  <div class="container">
    <div class="eyebrow">Nieuws & analyse</div>
    <h1>Humanoïde robots in Nederland.</h1>
    <p>Dagelijkse analyses over de humanoid-revolutie: nieuwe modellen, pilot-data, regelgeving en wat het betekent voor het Nederlandse MKB. Geschreven door de BotLease redactie, gekoppeld aan publieke bronnen.</p>
  </div>
</section>

<section class="news-feed">
  <div class="container">
    <div class="news-grid">{''.join(cards)}</div>
  </div>
</section>

{FOOTER_HTML}
</body>
</html>
"""


def render_sitemap(articles: list) -> str:
    urls = [
        (SITE_URL + "/", "1.0", "weekly"),
        (SITE_URL + "/nieuws/", "0.9", "daily"),
    ]
    for a in articles:
        urls.append((f"{SITE_URL}/nieuws/{a['slug']}", "0.7", "weekly", a["date"]))
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        url, prio, freq = u[0], u[1], u[2]
        lastmod = u[3] if len(u) > 3 else datetime.now(timezone.utc).strftime("%Y-%m-%d")
        out.append(f"  <url><loc>{url}</loc><lastmod>{lastmod}</lastmod><changefreq>{freq}</changefreq><priority>{prio}</priority></url>")
    out.append("</urlset>")
    return "\n".join(out)


def render_robots() -> str:
    return f"""User-agent: *
Allow: /
Disallow: /api/
Disallow: /backend/

Sitemap: {SITE_URL}/sitemap.xml
"""


def render_rss(articles: list) -> str:
    items_sorted = sorted(articles, key=lambda a: a["date"], reverse=True)[:20]
    items = []
    for a in items_sorted:
        pub = datetime.strptime(a["date"], "%Y-%m-%d").strftime("%a, %d %b %Y 08:00:00 +0100")
        items.append(f"""    <item>
      <title>{escape(a['title'])}</title>
      <link>{SITE_URL}/nieuws/{a['slug']}</link>
      <guid isPermaLink="true">{SITE_URL}/nieuws/{a['slug']}</guid>
      <pubDate>{pub}</pubDate>
      <category>{escape(a.get('category','Nieuws'))}</category>
      <description><![CDATA[{a['subtitle']}]]></description>
    </item>""")

    last_build = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>BotLease Nieuws — humanoïde robots in Nederland</title>
    <link>{SITE_URL}/nieuws/</link>
    <atom:link href="{SITE_URL}/rss.xml" rel="self" type="application/rss+xml"/>
    <description>Dagelijkse analyses over humanoïde robots, lease, pilots, regelgeving en marktontwikkeling in Nederland.</description>
    <language>nl-NL</language>
    <lastBuildDate>{last_build}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
"""


# ---------------------------------------------------------------- main
def build():
    NEWS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    articles_sorted = sorted(ARTICLES, key=lambda a: a["date"], reverse=True)

    # Per artikel — "related" = next 2 nieuwere/oudere
    for i, a in enumerate(articles_sorted):
        related = [x for x in articles_sorted if x["slug"] != a["slug"]][:2]
        (NEWS_DIR / f"{a['slug']}.html").write_text(render_article(a, related), encoding="utf-8")

    (NEWS_DIR / "index.html").write_text(render_listing(articles_sorted), encoding="utf-8")
    (FRONTEND / "sitemap.xml").write_text(render_sitemap(articles_sorted), encoding="utf-8")
    (FRONTEND / "robots.txt").write_text(render_robots(), encoding="utf-8")
    (FRONTEND / "rss.xml").write_text(render_rss(articles_sorted), encoding="utf-8")

    data_summary = [
        {"slug": a["slug"], "title": a["title"], "subtitle": a["subtitle"],
         "date": a["date"], "category": a.get("category"), "tags": a.get("tags", [])}
        for a in articles_sorted
    ]
    (DATA_DIR / "articles.json").write_text(
        json.dumps(data_summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"✅ Built {len(articles_sorted)} articles")
    print(f"   /nieuws/  →  {NEWS_DIR}")
    print(f"   sitemap.xml, robots.txt, rss.xml in {FRONTEND}")


if __name__ == "__main__":
    build()
