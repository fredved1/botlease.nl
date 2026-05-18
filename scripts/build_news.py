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
article.card { padding:0; overflow:hidden; }
article.card .card-body { padding:24px 28px 28px; display:flex; flex-direction:column; flex:1; }
.card-thumb {
  position:relative; height:160px; overflow:hidden;
  background:linear-gradient(135deg, color-mix(in srgb, var(--art-tint) 22%, var(--bg-3)) 0%, var(--bg-3) 100%);
  border-bottom:1px solid var(--line);
}
.card-thumb-pattern {
  position:absolute; inset:0;
  background:radial-gradient(60% 80% at 80% 50%, color-mix(in srgb, var(--art-tint) 28%, transparent) 0%, transparent 70%);
}
.card-thumb-art {
  position:absolute; right:22px; top:50%; transform:translateY(-50%);
  height:140px; width:auto; opacity:0.92;
  filter:drop-shadow(0 8px 18px rgba(0,0,0,0.45));
  transition:transform .35s;
}
.card-thumb-photo {
  position:absolute; right:22px; top:50%; transform:translateY(-50%);
  height:140px; width:auto; max-width:55%; object-fit:contain;
  filter:drop-shadow(0 12px 24px rgba(0,0,0,0.55));
  transition:transform .35s;
}
article.card:hover .card-thumb-art,
article.card:hover .card-thumb-photo { transform:translateY(-50%) scale(1.05); }
article.card.featured .card-thumb { height:220px; }
article.card.featured .card-thumb-art,
article.card.featured .card-thumb-photo { height:200px; right:48px; max-width:50%; }
@media (max-width:780px) {
  .news-grid { grid-template-columns:1fr; }
  article.card.featured { grid-column:span 1; }
  article.card.featured h2 { font-size:24px; }
  article.card.featured .card-thumb { height:160px; }
  article.card.featured .card-thumb-art,
  article.card.featured .card-thumb-photo { height:140px; right:22px; }
}
"""

ARTICLE_CSS = """
.article-hero { padding:130px 0 30px; position:relative; }
.article-hero::before { content:""; position:absolute; inset:0; background:radial-gradient(40% 40% at 80% 0%, rgba(255,94,31,0.12), transparent 70%); z-index:0; }
.article-hero .narrow { position:relative; z-index:2; }
.crumbs { display:flex; gap:8px; font-size:13px; color:var(--ink-3); margin-bottom:24px; }
.crumbs a:hover { color:var(--ink-2); }
.crumbs .sep { color:var(--line-2); }
.hero-banner {
  position:relative; width:100%; height:240px;
  border-radius:18px; overflow:hidden; margin-bottom:36px;
  background:linear-gradient(135deg, color-mix(in srgb, var(--art-tint) 26%, var(--bg-3)) 0%, var(--bg-3) 70%);
  border:1px solid var(--line);
}
.hero-banner-pattern {
  position:absolute; inset:0;
  background:
    radial-gradient(50% 90% at 78% 50%, color-mix(in srgb, var(--art-tint) 35%, transparent) 0%, transparent 65%),
    repeating-linear-gradient(135deg, rgba(255,255,255,0.02) 0 1px, transparent 1px 18px);
}
.hero-banner-label {
  position:absolute; top:20px; left:24px;
  font-family:'Space Grotesk',sans-serif; font-size:11px; font-weight:600;
  text-transform:uppercase; letter-spacing:0.16em;
  color:var(--ink); opacity:0.75;
  padding:5px 12px; background:rgba(8,8,10,0.55); border:1px solid rgba(255,255,255,0.08);
  border-radius:999px; backdrop-filter:blur(8px);
}
.hero-banner-art {
  position:absolute; right:32px; top:50%; transform:translateY(-50%);
  height:220px; width:auto; opacity:0.95;
  filter:drop-shadow(0 18px 36px rgba(0,0,0,0.55));
}
.hero-banner-photo {
  position:absolute; right:24px; top:50%; transform:translateY(-50%);
  height:92%; width:auto; max-width:48%; object-fit:contain;
  filter:drop-shadow(0 18px 36px rgba(0,0,0,0.6));
}
@media (max-width:780px) {
  .hero-banner { height:180px; }
  .hero-banner-art { height:160px; right:18px; }
  .hero-banner-photo { height:86%; right:14px; max-width:55%; }
}
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

# ---------------------------------------------------------------- SVG art library
# Reused across listing + article pages. Mirrors the silhouettes on the homepage,
# plus two abstract motifs voor regelgeving/markt-artikelen.
SVG_DEFS = """
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
    <symbol id="bot-g1" viewBox="0 0 200 320">
      <g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
        <ellipse cx="100" cy="42" rx="22" ry="24" fill="currentColor" fill-opacity="0.08"/>
        <rect x="84" y="34" width="32" height="10" rx="5" fill="currentColor" fill-opacity="0.4"/>
        <circle cx="92" cy="39" r="2" fill="currentColor"/><circle cx="108" cy="39" r="2" fill="currentColor"/>
        <line x1="94" y1="66" x2="94" y2="78"/><line x1="106" y1="66" x2="106" y2="78"/>
        <path d="M76 82 Q76 78 82 78 L118 78 Q124 78 124 82 L124 160 Q124 166 118 166 L82 166 Q76 166 76 160 Z" fill="currentColor" fill-opacity="0.07"/>
        <rect x="89" y="96" width="22" height="32" rx="3" fill="currentColor" fill-opacity="0.15"/>
        <line x1="93" y1="105" x2="107" y2="105"/><line x1="93" y1="114" x2="107" y2="114"/>
        <circle cx="74" cy="86" r="7" fill="currentColor" fill-opacity="0.15"/>
        <circle cx="126" cy="86" r="7" fill="currentColor" fill-opacity="0.15"/>
        <path d="M70 93 Q66 120 68 148"/><path d="M130 93 Q134 120 132 148"/>
        <rect x="62" y="148" width="12" height="22" rx="3" fill="currentColor" fill-opacity="0.18"/>
        <rect x="126" y="148" width="12" height="22" rx="3" fill="currentColor" fill-opacity="0.18"/>
        <path d="M82 166 L118 166 L120 184 L80 184 Z" fill="currentColor" fill-opacity="0.1"/>
        <path d="M88 186 L86 232"/><path d="M112 186 L114 232"/>
        <circle cx="86" cy="234" r="6" fill="currentColor" fill-opacity="0.15"/>
        <circle cx="114" cy="234" r="6" fill="currentColor" fill-opacity="0.15"/>
        <path d="M86 240 L88 270"/><path d="M114 240 L112 270"/>
        <rect x="76" y="270" width="24" height="8" rx="2" fill="currentColor" fill-opacity="0.2"/>
        <rect x="100" y="270" width="24" height="8" rx="2" fill="currentColor" fill-opacity="0.2"/>
      </g>
    </symbol>
    <symbol id="bot-digit" viewBox="0 0 200 320">
      <g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
        <rect x="76" y="20" width="48" height="28" rx="4" fill="currentColor" fill-opacity="0.1"/>
        <circle cx="100" cy="34" r="6" fill="currentColor" fill-opacity="0.4"/>
        <circle cx="100" cy="34" r="2.5" fill="currentColor"/>
        <line x1="78" y1="44" x2="122" y2="44" stroke-width="2"/>
        <line x1="96" y1="48" x2="96" y2="58"/><line x1="104" y1="48" x2="104" y2="58"/>
        <path d="M62 60 L138 60 L142 170 Q142 182 130 182 L70 182 Q58 182 58 170 Z" fill="currentColor" fill-opacity="0.08"/>
        <rect x="84" y="78" width="32" height="50" rx="2" fill="currentColor" fill-opacity="0.15"/>
        <line x1="90" y1="88" x2="110" y2="88"/>
        <circle cx="93" cy="100" r="2" fill="currentColor"/><circle cx="107" cy="100" r="2" fill="currentColor"/>
        <line x1="90" y1="112" x2="110" y2="112"/>
        <circle cx="56" cy="68" r="9" fill="currentColor" fill-opacity="0.15"/>
        <circle cx="144" cy="68" r="9" fill="currentColor" fill-opacity="0.15"/>
        <path d="M52 76 L46 130"/><path d="M148 76 L154 130"/>
        <circle cx="46" cy="132" r="7" fill="currentColor" fill-opacity="0.18"/>
        <circle cx="154" cy="132" r="7" fill="currentColor" fill-opacity="0.18"/>
        <path d="M46 139 L54 178"/><path d="M154 139 L146 178"/>
        <path d="M40 178 L60 178 L58 188 L42 188 Z" fill="currentColor" fill-opacity="0.2"/>
        <path d="M140 178 L160 178 L158 188 L142 188 Z" fill="currentColor" fill-opacity="0.2"/>
        <path d="M82 184 L70 222" stroke-width="3.5"/>
        <path d="M118 184 L130 222" stroke-width="3.5"/>
        <circle cx="70" cy="224" r="7" fill="currentColor" fill-opacity="0.18"/>
        <circle cx="130" cy="224" r="7" fill="currentColor" fill-opacity="0.18"/>
        <path d="M70 230 L92 270" stroke-width="3.5"/>
        <path d="M130 230 L108 270" stroke-width="3.5"/>
        <path d="M92 270 L88 302"/><path d="M108 270 L112 302"/>
        <rect x="76" y="300" width="26" height="10" rx="2" fill="currentColor" fill-opacity="0.25"/>
        <rect x="98" y="300" width="26" height="10" rx="2" fill="currentColor" fill-opacity="0.25"/>
      </g>
    </symbol>
    <symbol id="bot-apollo" viewBox="0 0 200 320">
      <g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
        <rect x="74" y="8" width="52" height="50" rx="12" fill="currentColor" fill-opacity="0.1"/>
        <rect x="80" y="22" width="40" height="16" rx="3" fill="currentColor" fill-opacity="0.45"/>
        <line x1="86" y1="30" x2="114" y2="30" stroke-width="2"/>
        <line x1="92" y1="58" x2="92" y2="68"/><line x1="108" y1="58" x2="108" y2="68"/>
        <path d="M50 72 Q50 64 60 64 L140 64 Q150 64 150 72 L150 180 Q150 192 138 192 L62 192 Q50 192 50 180 Z" fill="currentColor" fill-opacity="0.1"/>
        <rect x="76" y="84" width="48" height="56" rx="6" fill="currentColor" fill-opacity="0.2"/>
        <rect x="84" y="94" width="32" height="12" rx="2" fill="currentColor" fill-opacity="0.35"/>
        <circle cx="92" cy="124" r="4" fill="currentColor" fill-opacity="0.3"/>
        <circle cx="108" cy="124" r="4" fill="currentColor" fill-opacity="0.3"/>
        <path d="M44 74 Q40 70 46 64 L62 64 L62 92 Q56 96 48 92 Z" fill="currentColor" fill-opacity="0.18"/>
        <path d="M156 74 Q160 70 154 64 L138 64 L138 92 Q144 96 152 92 Z" fill="currentColor" fill-opacity="0.18"/>
        <path d="M46 96 Q38 130 44 162"/><path d="M154 96 Q162 130 156 162"/>
        <circle cx="44" cy="164" r="8" fill="currentColor" fill-opacity="0.18"/>
        <circle cx="156" cy="164" r="8" fill="currentColor" fill-opacity="0.18"/>
        <path d="M44 172 Q42 200 50 220"/><path d="M156 172 Q158 200 150 220"/>
        <rect x="38" y="220" width="22" height="24" rx="4" fill="currentColor" fill-opacity="0.22"/>
        <rect x="140" y="220" width="22" height="24" rx="4" fill="currentColor" fill-opacity="0.22"/>
        <path d="M62 192 L138 192 L142 214 L58 214 Z" fill="currentColor" fill-opacity="0.13"/>
        <path d="M80 216 Q76 254 82 274"/><path d="M120 216 Q124 254 118 274"/>
        <circle cx="82" cy="276" r="9" fill="currentColor" fill-opacity="0.18"/>
        <circle cx="118" cy="276" r="9" fill="currentColor" fill-opacity="0.18"/>
        <path d="M82 284 L84 308"/><path d="M118 284 L116 308"/>
        <rect x="68" y="306" width="32" height="10" rx="3" fill="currentColor" fill-opacity="0.25"/>
        <rect x="100" y="306" width="32" height="10" rx="3" fill="currentColor" fill-opacity="0.25"/>
      </g>
    </symbol>
    <!-- Regelgeving: weegschaal + EU-sterren -->
    <symbol id="art-regulation" viewBox="0 0 200 320">
      <g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
        <!-- pillar -->
        <line x1="100" y1="62" x2="100" y2="246" stroke-width="4"/>
        <rect x="74" y="248" width="52" height="14" rx="3" fill="currentColor" fill-opacity="0.2"/>
        <rect x="62" y="262" width="76" height="10" rx="3" fill="currentColor" fill-opacity="0.15"/>
        <!-- beam -->
        <line x1="38" y1="92" x2="162" y2="92" stroke-width="3.5"/>
        <line x1="100" y1="62" x2="100" y2="92" stroke-width="3.5"/>
        <circle cx="100" cy="62" r="6" fill="currentColor" fill-opacity="0.5"/>
        <!-- left pan -->
        <line x1="50" y1="92" x2="50" y2="120"/>
        <line x1="30" y1="120" x2="70" y2="120"/>
        <path d="M30 120 Q30 142 50 144 Q70 142 70 120" fill="currentColor" fill-opacity="0.18"/>
        <!-- right pan -->
        <line x1="150" y1="92" x2="150" y2="120"/>
        <line x1="130" y1="120" x2="170" y2="120"/>
        <path d="M130 120 Q130 142 150 144 Q170 142 170 120" fill="currentColor" fill-opacity="0.18"/>
        <!-- EU stars arc above -->
        <g fill="currentColor" fill-opacity="0.7" stroke="none">
          <polygon points="60,20 62,26 68,26 63,30 65,36 60,32 55,36 57,30 52,26 58,26"/>
          <polygon points="82,12 84,18 90,18 85,22 87,28 82,24 77,28 79,22 74,18 80,18"/>
          <polygon points="100,8  102,14 108,14 103,18 105,24 100,20 95,24 97,18 92,14 98,14"/>
          <polygon points="118,12 120,18 126,18 121,22 123,28 118,24 113,28 115,22 110,18 116,18"/>
          <polygon points="140,20 142,26 148,26 143,30 145,36 140,32 135,36 137,30 132,26 138,26"/>
        </g>
        <!-- document on left pan -->
        <g stroke-width="2">
          <rect x="38" y="100" width="24" height="14" rx="1" fill="currentColor" fill-opacity="0.25"/>
          <line x1="42" y1="105" x2="58" y2="105"/>
          <line x1="42" y1="109" x2="54" y2="109"/>
        </g>
        <!-- gear on right pan (AI) -->
        <g stroke-width="2">
          <circle cx="150" cy="106" r="9" fill="currentColor" fill-opacity="0.2"/>
          <circle cx="150" cy="106" r="3" fill="currentColor" fill-opacity="0.4"/>
          <line x1="150" y1="94"  x2="150" y2="97"/>
          <line x1="150" y1="115" x2="150" y2="118"/>
          <line x1="138" y1="106" x2="141" y2="106"/>
          <line x1="159" y1="106" x2="162" y2="106"/>
        </g>
      </g>
    </symbol>
    <!-- Markt: oplopende barchart + pijl + euro/dollar -->
    <symbol id="art-market" viewBox="0 0 200 320">
      <g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
        <!-- baseline + y-axis -->
        <line x1="32" y1="40" x2="32" y2="240" stroke-width="2"/>
        <line x1="32" y1="240" x2="180" y2="240" stroke-width="2"/>
        <g stroke-width="1" stroke-opacity="0.4">
          <line x1="28" y1="80" x2="180" y2="80"/>
          <line x1="28" y1="120" x2="180" y2="120"/>
          <line x1="28" y1="160" x2="180" y2="160"/>
          <line x1="28" y1="200" x2="180" y2="200"/>
        </g>
        <!-- bars ascending -->
        <g fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="2">
          <rect x="44"  y="200" width="20" height="40" rx="2"/>
          <rect x="72"  y="172" width="20" height="68" rx="2"/>
          <rect x="100" y="140" width="20" height="100" rx="2"/>
          <rect x="128" y="98"  width="20" height="142" rx="2"/>
          <rect x="156" y="60"  width="20" height="180" rx="2"/>
        </g>
        <!-- trend arrow -->
        <g stroke-width="3.5" fill="none">
          <path d="M40 210 L80 175 L120 145 L165 70"/>
          <polyline points="155,68 165,68 165,80"/>
        </g>
        <!-- euro symbol top-left -->
        <g stroke-width="3" stroke-linecap="round">
          <path d="M80 268 Q70 268 66 274 Q62 282 66 290 Q70 296 80 296"/>
          <line x1="62" y1="278" x2="78" y2="278"/>
          <line x1="62" y1="286" x2="78" y2="286"/>
        </g>
        <!-- dollar -->
        <g stroke-width="3" stroke-linecap="round">
          <path d="M118 268 Q108 268 108 274 Q108 280 116 282 Q124 284 124 290 Q124 296 114 296"/>
          <line x1="116" y1="262" x2="116" y2="302"/>
        </g>
        <!-- 2035 label squareish -->
        <g stroke-width="2" stroke-opacity="0.7">
          <rect x="150" y="262" width="36" height="20" rx="3" fill="currentColor" fill-opacity="0.12"/>
        </g>
      </g>
    </symbol>
  </defs>
</svg>
"""

# ---------------------------------------------------------------- art mapping
# Per artikel: welke foto + kleurtint voor banner/card gradient.
# Voor markt/regulering-artikelen pakken we een symbool-fallback.
DEFAULT_ART = {"photo": "/img/robots/g1.jpg", "alt": "Humanoïde robot", "tint": "#5be584", "symbol": None}
ART_BY_SLUG = {
    "unitree-g1-mkb-vijf-rendabele-toepassingen":
        {"photo": "/img/robots/g1.jpg", "alt": "Unitree G1 humanoid robot", "tint": "#5be584", "symbol": None},
    "apptronik-mercedes-apollo-lessen-eerste-pilot":
        {"photo": "/img/robots/apollo.png", "alt": "Apptronik Apollo robot bij Mercedes", "tint": "#ff5e1f", "symbol": None},
    "ai-act-machineverordening-humanoid-werkgevers-2026":
        {"photo": None, "alt": "AI-Act en Machineverordening", "tint": "#ffc966", "symbol": "art-regulation", "color": "#ffd166"},
    "agility-digit-fulfillment-pilot-3pl-nederland":
        {"photo": "/img/robots/digit.jpg", "alt": "Agility Digit robot in fulfillment", "tint": "#ffb098", "symbol": None},
    "goldman-sachs-38-miljard-humanoid-markt-nederland":
        {"photo": None, "alt": "Humanoid robot markt", "tint": "#6ea8ff", "symbol": "art-market", "color": "#a6cbff"},
}


def art_for(slug: str) -> dict:
    return ART_BY_SLUG.get(slug, DEFAULT_ART)


def article_hero_banner(a: dict) -> str:
    """Banner above the article title: gradient + foto of abstract motief."""
    art = art_for(a["slug"])
    if art.get("photo"):
        media = (
            f'<img class="hero-banner-photo" src="{art["photo"]}" '
            f'alt="{escape(art["alt"])}" loading="lazy">'
        )
    else:
        media = (
            f'<svg class="hero-banner-art" viewBox="0 0 200 320" '
            f'style="color:{art.get("color", "#ffd166")}" aria-hidden="true">'
            f'<use href="#{art["symbol"]}"/></svg>'
        )
    return (
        f'<div class="hero-banner" style="--art-tint:{art["tint"]}">'
        f'  <div class="hero-banner-pattern"></div>'
        f'  <span class="hero-banner-label">{escape(a.get("category", "Nieuws"))}</span>'
        f'  {media}'
        f'</div>'
    )


def card_thumb(a: dict) -> str:
    """Compact thumbnail at the top of a listing card."""
    art = art_for(a["slug"])
    if art.get("photo"):
        media = (
            f'<img class="card-thumb-photo" src="{art["photo"]}" '
            f'alt="{escape(art["alt"])}" loading="lazy">'
        )
    else:
        media = (
            f'<svg class="card-thumb-art" viewBox="0 0 200 320" '
            f'style="color:{art.get("color", "#ffd166")}" aria-hidden="true">'
            f'<use href="#{art["symbol"]}"/></svg>'
        )
    return (
        f'<div class="card-thumb" style="--art-tint:{art["tint"]}">'
        f'  <div class="card-thumb-pattern"></div>'
        f'  {media}'
        f'</div>'
    )

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

def article_image(a: dict) -> str:
    art = art_for(a["slug"])
    if art.get("photo"):
        return f"{SITE_URL}{art['photo']}"
    return f"{SITE_URL}/img/robots/apollo.png"


def article_jsonld(a: dict) -> str:
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": a["title"],
        "description": a["subtitle"],
        "image": [article_image(a)],
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


def breadcrumb_jsonld(a: dict) -> str:
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Nieuws", "item": f"{SITE_URL}/nieuws/"},
            {"@type": "ListItem", "position": 3, "name": a["title"], "item": f"{SITE_URL}/nieuws/{a['slug']}"},
        ]
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
<meta property="og:image" content="{article_image(a)}">
<meta property="article:published_time" content="{a['date']}T08:00:00+01:00">
<meta property="article:section" content="{escape(a.get('category', 'Nieuws'))}">
{''.join(f'<meta property="article:tag" content="{escape(t)}">' for t in a.get('tags', []))}

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(a['title'])}">
<meta name="twitter:description" content="{escape(a['subtitle'])}">
<meta name="twitter:image" content="{article_image(a)}">

<link rel="alternate" type="application/rss+xml" title="BotLease Nieuws" href="{SITE_URL}/rss.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>{PAGE_CSS}{ARTICLE_CSS}</style>
<script type="application/ld+json">{article_jsonld(a)}</script>
<script type="application/ld+json">{breadcrumb_jsonld(a)}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
</head>
<body>
{SVG_DEFS}
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
    {article_hero_banner(a)}
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
          {card_thumb(a)}
          <div class="card-body">
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
<meta property="og:image" content="{SITE_URL}/img/robots/apollo.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="BotLease Nieuws — humanoïde robots in Nederland">
<meta name="twitter:description" content="Dagelijkse analyses over Unitree, Figure, Apptronik, Agility, 1X — voor de Nederlandse markt.">
<meta name="twitter:image" content="{SITE_URL}/img/robots/apollo.png">

<link rel="alternate" type="application/rss+xml" title="BotLease Nieuws" href="{SITE_URL}/rss.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>{PAGE_CSS}{LISTING_CSS}</style>
<script type="application/ld+json">{itemlist_jsonld}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE_URL}/"}}, {{"@type": "ListItem", "position": 2, "name": "Nieuws", "item": "{SITE_URL}/nieuws/"}}]}}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
</head>
<body>
{SVG_DEFS}
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
