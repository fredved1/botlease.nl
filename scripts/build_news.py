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
from datetime import datetime, timezone, timedelta
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"
NEWS_DIR = FRONTEND / "nieuws"
DATA_DIR = FRONTEND / "data"
SITE_URL = "https://botlease.nl"

sys.path.insert(0, str(ROOT / "scripts"))
from articles_data import ARTICLES  # noqa: E402
from seo_common import HEAD_SEO, trim_desc  # noqa: E402
from style_base import BASE_CSS, NAV_HTML, FOOTER_HTML, FONTS_LINK  # noqa: E402


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
PAGE_CSS = BASE_CSS  # editorial light tokens + base styles from style_base.py

LISTING_CSS = """
.news-hero { padding:80px 0 28px; }
@media (min-width:768px) { .news-hero { padding:120px 0 36px; } }
.eyebrow {
  display:inline-block; color:var(--accent); font-size:12.5px;
  text-transform:uppercase; letter-spacing:0.12em; font-weight:600;
  margin-bottom:16px;
}
.news-hero h1 {
  font-family:'Inter', -apple-system, sans-serif; font-weight:700;
  font-size:clamp(40px, 5.5vw, 72px);
  margin-bottom:18px; letter-spacing:-0.035em; line-height:1.02;
}
.news-hero .lede { color:var(--ink-2); font-size:18.5px; max-width:680px; line-height:1.55; margin-bottom:24px; }
.news-hero .badge-row { display:flex; flex-wrap:wrap; gap:12px; align-items:center; margin-bottom:8px; }
.live-badge {
  display:inline-flex; align-items:center; gap:8px;
  background:var(--accent-soft); color:var(--accent-deep);
  border:1px solid var(--accent-line);
  padding:6px 14px; border-radius:999px;
  font-family:'Inter'; font-size:12px; font-weight:600;
  letter-spacing:0.06em; text-transform:uppercase;
}
.live-badge::before {
  content:""; width:8px; height:8px; border-radius:50%;
  background:var(--accent); box-shadow:0 0 0 0 var(--accent);
  animation:livepulse 2s infinite;
}
@keyframes livepulse {
  0%   { box-shadow:0 0 0 0 color-mix(in srgb, var(--accent) 60%, transparent); }
  70%  { box-shadow:0 0 0 9px color-mix(in srgb, var(--accent) 0%, transparent); }
  100% { box-shadow:0 0 0 0 color-mix(in srgb, var(--accent) 0%, transparent); }
}
.update-meta { color:var(--ink-3); font-size:13px; }

/* Category filter chips */
.cat-filter {
  display:flex; flex-wrap:wrap; gap:8px; padding:6px 0 0;
  border-top:1px solid var(--border); margin-top:32px; padding-top:22px;
}
.cat-chip {
  font-family:'Inter'; font-size:13px; font-weight:600;
  padding:7px 16px; border-radius:999px;
  background:transparent; color:var(--ink-2);
  border:1px solid var(--border); cursor:pointer;
  transition:all .15s;
}
.cat-chip:hover { border-color:var(--accent); color:var(--accent); }
.cat-chip.active {
  background:var(--ink); color:var(--bg-card); border-color:var(--ink);
}

/* Lead story - full-bleed hero */
.lead-story {
  position:relative; overflow:hidden;
  border-radius:18px;
  margin-bottom:48px;
  background:#1c1917;
  min-height:380px;
}
@media (min-width:880px) { .lead-story { min-height:520px; } }
.lead-story-photo {
  position:absolute; inset:0; width:100%; height:100%;
  object-fit:cover; object-position:center;
  transition:transform .6s;
}
.lead-story:hover .lead-story-photo { transform:scale(1.03); }
.lead-story-overlay {
  position:absolute; inset:0;
  background:linear-gradient(180deg, rgba(0,0,0,0.18) 0%, rgba(0,0,0,0.35) 45%, rgba(0,0,0,0.88) 100%);
}
.lead-story-content {
  position:absolute; inset:auto 0 0 0;
  padding:32px 36px 36px; color:#fff;
}
@media (min-width:880px) { .lead-story-content { padding:48px 56px 52px; max-width:780px; } }
.lead-story .cat-tag {
  display:inline-block;
  font-family:'Inter'; font-size:11px; font-weight:700;
  letter-spacing:0.12em; text-transform:uppercase;
  padding:5px 12px; border-radius:999px;
  background:var(--accent); color:#fff;
  margin-bottom:18px;
}
.lead-story h2 {
  font-family:'Inter', -apple-system, sans-serif; font-weight:700;
  font-size:clamp(28px, 3.5vw, 44px);
  line-height:1.12; letter-spacing:-0.025em;
  margin-bottom:14px; color:#fff;
}
.lead-story h2 a { color:#fff; }
.lead-story h2 a:hover { color:var(--accent-soft); }
.lead-story p.lede {
  color:rgba(255,255,255,0.85); font-size:16.5px; line-height:1.55;
  max-width:680px; margin-bottom:18px;
}
.lead-story .meta-row {
  display:flex; flex-wrap:wrap; gap:14px; align-items:center;
  color:rgba(255,255,255,0.7); font-size:13px;
}
.lead-story .source-chip {
  display:inline-flex; align-items:center; gap:5px;
  background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.25);
  padding:3px 10px; border-radius:999px;
  color:#fff; font-size:12px; font-weight:500;
}

/* Sub-featured row - 2 columns */
.sub-features {
  display:grid; grid-template-columns:1fr; gap:20px; margin-bottom:48px;
}
@media (min-width:768px) { .sub-features { grid-template-columns:1fr 1fr; gap:24px; } }

/* Main grid - 3 columns */
.news-feed { padding:24px 0 96px; }
.news-grid-title {
  font-family:'Inter'; font-size:13px; text-transform:uppercase;
  letter-spacing:0.12em; font-weight:600; color:var(--ink-3);
  margin-bottom:18px; padding-bottom:12px; border-bottom:1px solid var(--border);
}
.news-grid { display:grid; grid-template-columns:1fr; gap:20px; }
@media (min-width:680px) { .news-grid { grid-template-columns:1fr 1fr; gap:24px; } }
@media (min-width:1024px) { .news-grid { grid-template-columns:repeat(3, 1fr); gap:24px; } }

article.card {
  background:var(--bg-card); border:1px solid var(--border);
  border-radius:14px; padding:0; overflow:hidden;
  transition:transform .25s, border-color .25s, box-shadow .25s;
  display:flex; flex-direction:column;
}
article.card:hover {
  transform:translateY(-3px); border-color:var(--border-hover);
  box-shadow:var(--shadow-md);
}
article.card .card-body { padding:20px 22px 22px; display:flex; flex-direction:column; flex:1; }
article.card .meta { display:flex; gap:10px; align-items:center; margin-bottom:12px; flex-wrap:wrap; }
article.card .cat {
  font-family:'Inter'; color:var(--accent-deep);
  font-size:10.5px; text-transform:uppercase; letter-spacing:0.1em; font-weight:600;
  padding:3px 10px; background:var(--accent-soft);
  border:1px solid var(--accent-line); border-radius:999px;
}
article.card .date { color:var(--ink-3); font-size:12.5px; }
article.card h2 {
  font-family:'Inter'; font-weight:600;
  font-size:18px; line-height:1.28; margin-bottom:10px; letter-spacing:-0.015em;
}
article.card h2 a { color:var(--ink); }
article.card h2 a:hover { color:var(--accent); }
article.card p.lede { color:var(--ink-2); font-size:14px; line-height:1.55; margin-bottom:18px; flex:1; }
article.card .footer-line {
  display:flex; justify-content:space-between; align-items:center;
  padding-top:14px; border-top:1px solid var(--border);
  font-size:12.5px; color:var(--ink-3); gap:10px;
}
article.card .read-more { color:var(--accent); font-weight:600; white-space:nowrap; }
article.card .src {
  font-size:11px; color:var(--ink-3); font-weight:500;
  overflow:hidden; text-overflow:ellipsis; white-space:nowrap;
}

/* Thumbnail */
.card-thumb {
  position:relative; height:200px; overflow:hidden;
  background:var(--bg-2);
  border-bottom:1px solid var(--border);
}
.card-thumb-pattern {
  position:absolute; inset:0;
  background:radial-gradient(60% 80% at 80% 50%, color-mix(in srgb, var(--art-tint, var(--accent)) 14%, transparent) 0%, transparent 70%);
}
.card-thumb-art, .card-thumb-photo:not(.cover) {
  position:absolute; right:22px; top:50%; transform:translateY(-50%);
  height:140px; width:auto; max-width:55%; object-fit:contain;
  filter:drop-shadow(0 8px 20px rgba(28,25,23,0.15));
  transition:transform .35s;
}
.card-thumb-photo.cover {
  /* External hero image - fill entire thumb area */
  position:absolute; inset:0;
  width:100%; height:100%;
  object-fit:cover; object-position:center;
  transition:transform .6s;
}
article.card:hover .card-thumb-photo.cover { transform:scale(1.04); }
article.card:hover .card-thumb-art,
article.card:hover .card-thumb-photo:not(.cover) { transform:translateY(-50%) scale(1.05); }

/* Sub-feature variant */
.thumb-sub.card-thumb { height:260px; }

/* Sub-feature card body slightly larger */
article.card.sub-featured h2 { font-size:21px; line-height:1.22; }
article.card.sub-featured p.lede { font-size:15px; }
"""

ARTICLE_CSS = """
.article-hero { padding:80px 0 30px; }
@media (min-width:768px) { .article-hero { padding:110px 0 40px; } }
.hero-banner {
  position:relative; width:100%; height:240px;
  border-radius:14px; overflow:hidden; margin-bottom:36px;
  background:var(--accent-soft);
  border:1px solid var(--accent-line);
}
.hero-banner-pattern { display:none; }
.hero-banner-label {
  position:absolute; top:18px; left:20px;
  font-family:'Inter',sans-serif; font-size:11px; font-weight:600;
  text-transform:uppercase; letter-spacing:0.1em;
  color:var(--accent-deep);
  padding:4px 12px; background:var(--bg-card);
  border:1px solid var(--accent-line); border-radius:999px;
}
.hero-banner-art, .hero-banner-photo {
  position:absolute; right:32px; top:50%; transform:translateY(-50%);
  height:88%; width:auto; max-width:48%; object-fit:contain;
  filter:drop-shadow(0 18px 36px rgba(28,25,23,0.18));
}
@media (max-width:780px) {
  .hero-banner { height:180px; }
  .hero-banner-art, .hero-banner-photo { right:18px; height:84%; max-width:55%; }
}
article.full .meta { display:flex; flex-wrap:wrap; gap:12px; align-items:center; margin-bottom:20px; font-size:13.5px; color:var(--ink-3); }
article.full .cat {
  font-family:'Inter'; color:var(--accent-deep);
  font-size:11px; text-transform:uppercase; letter-spacing:0.1em; font-weight:600;
  padding:3px 10px; background:var(--accent-soft);
  border:1px solid var(--accent-line); border-radius:999px;
}
article.full h1 {
  font-family:'Inter', -apple-system, sans-serif; font-weight:700;
  font-size:clamp(34px, 4.5vw, 56px);
  margin-bottom:18px; letter-spacing:-0.035em; line-height:1.06;
}
article.full .subtitle { font-size:19px; color:var(--ink-2); margin-bottom:32px; line-height:1.5; }
article.full .body { padding:32px 0 0; }
article.full .body p, article.full .body ul { font-size:17px; color:var(--ink); margin-bottom:22px; line-height:1.78; }

/* TL;DR callout */
.tldr {
  position:relative;
  background:var(--accent-soft);
  border-left:4px solid var(--accent);
  border-radius:0 12px 12px 0;
  padding:22px 28px 22px 28px;
  margin:0 0 36px;
}
.tldr-label {
  display:inline-block;
  font-family:'Inter', sans-serif;
  font-size:11px; font-weight:700;
  letter-spacing:0.14em; text-transform:uppercase;
  color:var(--accent-deep);
  margin-bottom:8px;
}
.tldr p {
  font-family:'Inter', sans-serif;
  font-size:16.5px !important;
  font-weight:500;
  color:var(--ink) !important;
  margin-bottom:0 !important;
  line-height:1.55 !important;
}
@media (min-width:768px) { .tldr { padding:26px 32px; } .tldr p { font-size:17px !important; } }
article.full .body ul { padding-left:24px; }
article.full .body li { margin-bottom:8px; color:var(--ink); }
article.full .body h2 {
  font-family:'Inter', -apple-system, sans-serif; font-weight:700;
  font-size:30px; margin:56px 0 18px; letter-spacing:-0.025em; line-height:1.15;
}
article.full .body h3 { font-size:21px; margin:36px 0 14px; }
article.full .body a { color:var(--accent); text-decoration:underline; text-decoration-color:var(--accent-line); text-underline-offset:3px; }
article.full .body a:hover { text-decoration-color:var(--accent); }
article.full .body strong, article.full .body b { color:var(--ink); font-weight:600; }
article.full blockquote {
  border-left:3px solid var(--accent);
  padding:8px 0 8px 24px; margin:32px 0;
  font-family:'Inter', -apple-system, sans-serif; font-weight:700;
  font-size:22px; color:var(--ink); line-height:1.4;
}
.sources { margin-top:64px; padding:32px; background:var(--bg-2); border:1px solid var(--border); border-radius:14px; }
.sources h3 { font-size:13px; text-transform:uppercase; letter-spacing:0.1em; color:var(--ink-3); margin-bottom:18px; font-family:'Inter'; font-weight:600; }
.sources ol { padding-left:22px; }
.sources li { color:var(--ink-2); font-size:14.5px; margin-bottom:8px; }
.sources a { color:var(--accent); text-decoration:underline; text-decoration-color:var(--accent-line); }
.tags { margin-top:32px; display:flex; flex-wrap:wrap; gap:8px; }
.tags span { font-size:12px; color:var(--ink-2); background:var(--bg-2); border:1px solid var(--border); padding:4px 10px; border-radius:999px; }
.cta-strip {
  margin-top:64px; padding:48px;
  background:var(--bg-dark); color:var(--ink-on-dark);
  border-radius:20px; text-align:center;
}
.cta-strip h3 {
  font-family:'Inter', -apple-system, sans-serif; font-weight:700;
  font-size:28px; margin-bottom:10px; color:var(--ink-on-dark);
}
.cta-strip p { color:var(--ink-2-on-dark); margin-bottom:24px; font-size:16px; }
.cta-strip .btn { background:var(--accent); color:#fff; border-color:var(--accent); }
.cta-strip .btn:hover { background:#fff; color:var(--ink); border-color:#fff; }
.related { margin-top:80px; padding-top:48px; border-top:1px solid var(--border); }
.related h3 { font-size:13px; text-transform:uppercase; letter-spacing:0.1em; color:var(--ink-3); margin-bottom:22px; font-family:'Inter'; font-weight:600; }
.related-grid { display:grid; grid-template-columns:1fr; gap:18px; }
@media (min-width:640px) { .related-grid { grid-template-columns:1fr 1fr; } }
.related a {
  display:block; padding:24px;
  background:var(--bg-card); border:1px solid var(--border); border-radius:12px;
  transition:border-color .2s, transform .2s, box-shadow .2s;
}
.related a:hover { border-color:var(--border-hover); transform:translateY(-2px); box-shadow:var(--shadow-sm); }
.related .cat { font-size:11px; color:var(--accent-deep); text-transform:uppercase; letter-spacing:0.1em; font-weight:600; }
.related .t { font-family:'Inter'; font-weight:600; margin-top:6px; line-height:1.3; color:var(--ink); }
"""


# NAV_HTML + FOOTER_HTML komen uit style_base.py - geen lokale override

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
    "neura-robotics-bosch-deal-nederlandse-maakindustrie":
        {"photo": "/img/robots/neura-4ne1.webp", "alt": "NEURA 4NE-1 humanoid robot", "tint": "#5be584", "symbol": None},
    "eu-machineverordening-2027-werkgevers-checklist":
        {"photo": None, "alt": "EU Machineverordening checklist", "tint": "#ffc966", "symbol": "art-regulation", "color": "#ffd166"},
    "ubtech-walker-s2-1000-units-commerciele-volwassenheid":
        {"photo": "/img/robots/walker-s.webp", "alt": "UBTECH Walker S2 mass production", "tint": "#ffb098", "symbol": None},
    "humanoid-fulfillment-pilots-nederland-2026":
        {"photo": "/img/robots/digit.jpg", "alt": "Humanoid robots in Nederlandse fulfillment", "tint": "#ffb098", "symbol": None},
    "eu-gebouwd-humanoid-voordeel-2026":
        {"photo": "/img/robots/kangaroo.png", "alt": "PAL Kangaroo EU-gebouwde humanoid", "tint": "#5be584", "symbol": None},
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


def _local_img(u):
    """Alleen lokale/owned images toestaan; externe (IEEE/yt) URLs weren tegen perf + copyright."""
    u = (u or "").strip()
    return u if u.startswith("/") else ""


def card_thumb(a: dict, *, variant: str = "default") -> str:
    """Thumbnail at top of a listing card.
    variant: 'hero' (full-bleed huge), 'sub' (medium), 'default' (compact).
    Gebruikt alleen een LOKAAL hero-beeld (geen externe hotlinks); valt anders terug op de owned art-mapping."""
    hero_url = _local_img(a.get("hero_image_url", ""))
    art = art_for(a["slug"])
    alt = escape(a.get("hero_image_alt") or a.get("title", "")[:120])
    fallback_photo = art.get("photo") or "/img/robots/apollo.png"
    fallback_alt = escape(art.get("alt", "Humanoïde robot"))
    if hero_url:
        # Hotlink original, fallback to local photo via onerror
        media = (
            f'<img class="card-thumb-photo cover" src="{escape(hero_url)}" '
            f'alt="{alt}" loading="lazy" '
            f'onerror="this.onerror=null;this.src=\'{fallback_photo}\';this.alt=\'{fallback_alt}\';this.classList.remove(\'cover\')">'
        )
    elif art.get("photo"):
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
        f'<div class="card-thumb thumb-{variant}" style="--art-tint:{art["tint"]}">'
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
<title>{escape(a['title'] + (' | BotLease' if len(a['title']) <= 56 else ''))}</title>
<meta name="description" content="{escape(trim_desc(a['subtitle']))}">
<meta name="keywords" content="{escape(', '.join(a.get('tags', [])))}, humanoide robot, robot lease, Nederland">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="author" content="BotLease">
<link rel="canonical" href="{SITE_URL}/nieuws/{a['slug']}">

<meta property="og:type" content="article">
<meta property="og:title" content="{escape(a['title'])}">
<meta property="og:description" content="{escape(trim_desc(a['subtitle']))}">
<meta property="og:url" content="{SITE_URL}/nieuws/{a['slug']}">
<meta property="og:site_name" content="BotLease">
<meta property="og:locale" content="nl_NL">
<meta property="og:image" content="{article_image(a)}">
<meta property="article:published_time" content="{a['date']}T08:00:00+01:00">
<meta property="article:section" content="{escape(a.get('category', 'Nieuws'))}">
{''.join(f'<meta property="article:tag" content="{escape(t)}">' for t in a.get('tags', []))}

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(a['title'])}">
<meta name="twitter:description" content="{escape(trim_desc(a['subtitle']))}">
<meta name="twitter:image" content="{article_image(a)}">

<link rel="alternate" type="application/rss+xml" title="BotLease Nieuws" href="{SITE_URL}/rss.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{PAGE_CSS}{ARTICLE_CSS}</style>
<script type="application/ld+json">{article_jsonld(a)}</script>
<script type="application/ld+json">{breadcrumb_jsonld(a)}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
{HEAD_SEO}
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
      <p class="subtitle">{escape(trim_desc(a['subtitle']))}</p>
      <div class="body">
        <aside class="tldr">
          <span class="tldr-label">TL;DR</span>
          <p>{escape(a.get('tldr') or a['intro'])}</p>
        </aside>
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

<script>
// Umami: news-article tracking
(function() {{
  function track(name, data) {{
    if (window.umami && typeof window.umami.track === 'function') {{
      window.umami.track(name, data || {{}});
    }}
  }}
  var slug = '{a['slug']}';
  // Outbound source clicks (bronnen sectie)
  document.querySelectorAll('.sources a[href^="http"]').forEach(function(link) {{
    link.addEventListener('click', function() {{
      track('outbound_source', {{ slug: slug, url: link.href.slice(0, 80) }});
    }});
  }});
  // Internal product link clicks from article body
  document.querySelectorAll('article.full .body a[href^="/"]').forEach(function(link) {{
    link.addEventListener('click', function() {{
      track('article_internal_click', {{ slug: slug, target: link.getAttribute('href') }});
    }});
  }});
  // Scroll depth — fire at 50% + 90%
  var fired50 = false, fired90 = false;
  window.addEventListener('scroll', function() {{
    var h = document.documentElement, b = document.body;
    var pct = (h.scrollTop || b.scrollTop) / ((h.scrollHeight || b.scrollHeight) - h.clientHeight) * 100;
    if (pct > 50 && !fired50) {{ fired50 = true; track('article_scroll_50', {{ slug: slug }}); }}
    if (pct > 90 && !fired90) {{ fired90 = true; track('article_scroll_90', {{ slug: slug }}); }}
  }}, {{ passive: true }});
}})();
</script>

{FOOTER_HTML}
</body>
</html>
"""


def render_listing(articles: list) -> str:
    articles_sorted = sorted(articles, key=lambda a: a["date"], reverse=True)

    # Collect unique categories for filter chips
    cats_seen = []
    for a in articles_sorted:
        c = a.get("category", "Nieuws")
        if c not in cats_seen:
            cats_seen.append(c)

    cat_chips_html = '<button class="cat-chip active" data-filter="all">Alles</button>' + "".join(
        f'<button class="cat-chip" data-filter="{escape(c)}">{escape(c)}</button>'
        for c in cats_seen
    )

    def source_chip(a: dict, dark: bool = False) -> str:
        src_name = a.get("source_name", "").strip()
        src_url = a.get("source_url", "").strip()
        if not src_name:
            return ""
        cls = "source-chip" if dark else "src"
        if src_url and not dark:
            return f'<span class="{cls}">Bron: {escape(src_name)}</span>'
        return f'<span class="{cls}">{escape(src_name)}</span>'

    # --- Lead story (first article) - full-bleed photo treatment ---
    lead_html = ""
    if articles_sorted:
        a = articles_sorted[0]
        hero_url = _local_img(a.get("hero_image_url", ""))
        art = art_for(a["slug"])
        if hero_url:
            photo_src = hero_url
            photo_alt = escape(a.get("hero_image_alt") or a["title"][:120])
            fallback = art.get("photo") or "/img/robots/apollo.png"
            photo_tag = (
                f'<img class="lead-story-photo" src="{escape(photo_src)}" alt="{photo_alt}" '
                f'onerror="this.onerror=null;this.src=\'{fallback}\'">'
            )
        else:
            photo = art.get("photo") or "/img/robots/apollo.png"
            photo_tag = f'<img class="lead-story-photo" src="{photo}" alt="{escape(art.get("alt", a["title"]))}">'

        meta_bits = [f'<span>{escape(fmt_date_nl(a["date"]))}</span>',
                     f'<span>{a.get("reading_time", 5)} min lezen</span>']
        sc = source_chip(a, dark=True)
        if sc:
            meta_bits.append(sc)

        lead_html = f'''
        <article class="lead-story" data-cat="{escape(a.get("category", "Nieuws"))}">
          {photo_tag}
          <div class="lead-story-overlay"></div>
          <div class="lead-story-content">
            <span class="cat-tag">{escape(a.get("category", "Nieuws"))}</span>
            <h2><a href="/nieuws/{a["slug"]}">{escape(a["title"])}</a></h2>
            <p class="lede">{escape(trim_desc(a["subtitle"], 220))}</p>
            <div class="meta-row">{"".join(meta_bits)}</div>
          </div>
          <a href="/nieuws/{a["slug"]}" style="position:absolute;inset:0;z-index:5" aria-label="Lees: {escape(a["title"])}"></a>
        </article>'''

    # --- Sub-features (next 2 articles) - medium card with photo ---
    sub_html = ""
    for a in articles_sorted[1:3]:
        sub_html += f'''
        <article class="card sub-featured" data-cat="{escape(a.get("category", "Nieuws"))}">
          {card_thumb(a, variant="sub")}
          <div class="card-body">
            <div class="meta">
              <span class="cat">{escape(a.get("category", "Nieuws"))}</span>
              <span class="date">{escape(fmt_date_nl(a["date"]))}</span>
            </div>
            <h2><a href="/nieuws/{a["slug"]}">{escape(a["title"])}</a></h2>
            <p class="lede">{escape(trim_desc(a["subtitle"], 180))}</p>
            <div class="footer-line">
              {source_chip(a) or f'<span>{a.get("reading_time", 5)} min lezen</span>'}
              <a class="read-more" href="/nieuws/{a["slug"]}">Lees →</a>
            </div>
          </div>
        </article>'''

    # --- Main grid (article 4 onwards) - 3 col ---
    cards = []
    for a in articles_sorted[3:]:
        cards.append(f'''
        <article class="card" data-cat="{escape(a.get("category", "Nieuws"))}">
          {card_thumb(a)}
          <div class="card-body">
            <div class="meta">
              <span class="cat">{escape(a.get("category", "Nieuws"))}</span>
              <span class="date">{escape(fmt_date_nl(a["date"]))}</span>
            </div>
            <h2><a href="/nieuws/{a["slug"]}">{escape(a["title"])}</a></h2>
            <p class="lede">{escape(trim_desc(a["subtitle"], 140))}</p>
            <div class="footer-line">
              {source_chip(a) or f'<span>{a.get("reading_time", 5)} min</span>'}
              <a class="read-more" href="/nieuws/{a["slug"]}">Lees →</a>
            </div>
          </div>
        </article>''')

    itemlist_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "BotLease - Nieuws over humanoïde robots",
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
<meta name="description" content="Dagelijks nieuws over humanoïde robots - Unitree, Figure, Apptronik, Agility, 1X. Use-cases, regelgeving en pilot-data uit Nederland.">
<meta name="keywords" content="humanoide robot nieuws, robot Nederland, Unitree nieuws, Figure 02, Apollo Apptronik, Agility Digit, robot lease nieuws, AI Act robot">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/nieuws/">

<meta property="og:type" content="website">
<meta property="og:title" content="BotLease Nieuws - humanoïde robots in Nederland">
<meta property="og:description" content="Dagelijkse analyses over humanoïde robots, Nederlandse use-cases en marktontwikkelingen.">
<meta property="og:url" content="{SITE_URL}/nieuws/">
<meta property="og:locale" content="nl_NL">
<meta property="og:image" content="{SITE_URL}/img/robots/apollo.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="BotLease Nieuws - humanoïde robots in Nederland">
<meta name="twitter:description" content="Dagelijkse analyses over Unitree, Figure, Apptronik, Agility, 1X - voor de Nederlandse markt.">
<meta name="twitter:image" content="{SITE_URL}/img/robots/apollo.png">

<link rel="alternate" type="application/rss+xml" title="BotLease Nieuws" href="{SITE_URL}/rss.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{PAGE_CSS}{LISTING_CSS}</style>
<script type="application/ld+json">{itemlist_jsonld}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE_URL}/"}}, {{"@type": "ListItem", "position": 2, "name": "Nieuws", "item": "{SITE_URL}/nieuws/"}}]}}</script>
<script type="application/ld+json">{ORG_SCHEMA}</script>
{HEAD_SEO}
</head>
<body>
{SVG_DEFS}
{NAV_HTML}

<section class="news-hero">
  <div class="container">
    <div class="badge-row">
      <span class="live-badge">Dagelijks bijgewerkt</span>
      <span class="update-meta">Laatste update: {escape(fmt_date_nl(articles_sorted[0]["date"]) if articles_sorted else "-")}</span>
    </div>
    <div class="eyebrow">Nieuws over humanoïde robots</div>
    <h1>De humanoid-redactie van Europa.</h1>
    <p class="lede">Elke dag nieuwe analyses over de humanoid-revolutie: pilots bij Mercedes, BMW en Foxconn, nieuwe modellen uit Europa en Azië, EU AI-Act updates en wat het betekent voor jouw werkvloer. Bronnen worden per artikel vermeld.</p>
    <div class="cat-filter" role="tablist">{cat_chips_html}</div>
  </div>
</section>

<section class="news-feed">
  <div class="container">
    {lead_html}
    {f'<div class="sub-features">{sub_html}</div>' if sub_html else ''}
    {f'<h2 class="news-grid-title">Meer nieuws</h2><div class="news-grid">{"".join(cards)}</div>' if cards else ''}
  </div>
</section>

<script>
  // Category filter
  (function() {{
    const chips = document.querySelectorAll('.cat-chip');
    const items = document.querySelectorAll('[data-cat]');
    chips.forEach(c => c.addEventListener('click', () => {{
      chips.forEach(x => x.classList.remove('active'));
      c.classList.add('active');
      const f = c.dataset.filter;
      items.forEach(it => {{
        it.style.display = (f === 'all' || it.dataset.cat === f) ? '' : 'none';
      }});
    }}));
  }})();
</script>

{FOOTER_HTML}
</body>
</html>
"""


def render_sitemap(articles: list) -> str:
    try:
        from robots_data import ROBOTS
    except ImportError:
        ROBOTS = []
    try:
        from landingpages_data import SECTORS, CITIES
    except ImportError:
        SECTORS, CITIES = [], []
    # Vercel cleanUrls + trailingSlash:false → géén trailing slash in sitemap URLs.
    # Eerder hadden /robots/, /sectoren/, /leasen/, /nieuws/, /gids/ trailing slash,
    # wat een 308 redirect uitlokte op elke crawl. Crawl-budget verspild - nu opgelost.
    urls = [
        (SITE_URL + "/", "1.0", "weekly"),
        (SITE_URL + "/gids/humanoide-robot-leasen", "0.98", "monthly"),
        (SITE_URL + "/robots", "0.95", "weekly"),
        (SITE_URL + "/gids/ai-act-machineverordening", "0.92", "monthly"),
        (SITE_URL + "/vergelijken", "0.92", "weekly"),
        (SITE_URL + "/kosten", "0.92", "monthly"),
        (SITE_URL + "/sectoren", "0.9", "weekly"),
        (SITE_URL + "/leasen", "0.9", "weekly"),
        (SITE_URL + "/nieuws", "0.85", "daily"),
        (SITE_URL + "/gids", "0.85", "monthly"),
        (SITE_URL + "/begrippen", "0.75", "monthly"),
        (SITE_URL + "/over", "0.7", "yearly"),
        (SITE_URL + "/methodologie", "0.7", "yearly"),
    ]
    head_to_heads = [
        "unitree-g1-vs-neura-4ne1-mini",
        "unitree-h1-2-vs-ubtech-walker-s2",
        "neura-4ne1-gen3-vs-apptronik-apollo",
        "pal-kangaroo-vs-unitree-h1-2",
        "unitree-r1-vs-engineai-se01",
        "apptronik-apollo-vs-figure-02",
    ]
    for h in head_to_heads:
        urls.append((f"{SITE_URL}/vergelijken/{h}", "0.8", "monthly"))
    # Beslis-pagina's (decision pillars) - hoge intent + zero competition
    urls.append((f"{SITE_URL}/vergelijken/lease-vs-koop", "0.9", "monthly"))
    urls.append((f"{SITE_URL}/vergelijken/humanoid-vs-cobot", "0.9", "monthly"))
    for r in ROBOTS:
        urls.append((f"{SITE_URL}/robots/{r['slug']}", "0.85", "weekly"))
    for s in SECTORS:
        urls.append((f"{SITE_URL}/sectoren/{s['slug']}", "0.8", "weekly"))
    for c in CITIES:
        urls.append((f"{SITE_URL}/leasen/{c['slug']}", "0.75", "weekly"))
    for a in articles:
        urls.append((f"{SITE_URL}/nieuws/{a['slug']}", "0.7", "weekly", a["date"]))
    # Resolveer elke URL naar het bestand om de echte mtime te lezen - Google ziet zo
    # echte freshness, niet een statische build-datum.
    def lastmod_for(url: str) -> str:
        path = url.replace(SITE_URL, "").strip("/")
        candidates = []
        if not path:
            candidates = [FRONTEND / "index.html"]
        else:
            candidates = [
                FRONTEND / f"{path}.html",
                FRONTEND / path / "index.html",
                FRONTEND / path,
            ]
        for c in candidates:
            if c.exists():
                return datetime.fromtimestamp(c.stat().st_mtime, timezone.utc).strftime("%Y-%m-%d")
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        url, prio, freq = u[0], u[1], u[2]
        lastmod = u[3] if len(u) > 3 else lastmod_for(url)
        out.append(f"  <url><loc>{url}</loc><lastmod>{lastmod}</lastmod><changefreq>{freq}</changefreq><priority>{prio}</priority></url>")
    out.append("</urlset>")
    return "\n".join(out)


def render_image_sitemap() -> str:
    """Image sitemap voor Google Images traffic - alle robot photos + hero."""
    try:
        from robots_data import ROBOTS
    except ImportError:
        ROBOTS = []
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    # Homepage hero
    out.append(f"""  <url>
    <loc>{SITE_URL}/</loc>
    <image:image><image:loc>{SITE_URL}/img/hero/hero-robot.webp</image:loc>
      <image:title>Humanoïde robot leasen Nederland - BotLease catalogus 2026</image:title>
      <image:caption>BotLease - Nederlands eerste lease-maatschappij voor humanoïde robots, vanaf €290/mnd</image:caption>
    </image:image>
  </url>""")
    # Robot detail pages, each with hero image
    for r in ROBOTS:
        out.append(f"""  <url>
    <loc>{SITE_URL}/robots/{r['slug']}</loc>
    <image:image><image:loc>{SITE_URL}{r['photo']}</image:loc>
      <image:title>{r['name']} humanoïde robot - {r['vendor']}</image:title>
      <image:caption>{r['name']} leasen in Nederland vanaf €{r['lease_eur']:,}/mnd via BotLease</image:caption>
    </image:image>
  </url>""")
    out.append("</urlset>")
    return "\n".join(out).replace(",", ".")


def render_news_sitemap(articles: list) -> str:
    """News sitemap met <news:news> namespace - voor Google News indexering."""
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">']
    # Alleen recente (<30 dagen) articles, dat is wat Google News indexeert
    cutoff = (datetime.now(timezone.utc) - timedelta(days=30)).date().isoformat()
    for a in articles:
        if a["date"] < cutoff:
            continue
        out.append(f"""  <url>
    <loc>{SITE_URL}/nieuws/{a['slug']}</loc>
    <news:news>
      <news:publication>
        <news:name>BotLease</news:name>
        <news:language>nl</news:language>
      </news:publication>
      <news:publication_date>{a['date']}</news:publication_date>
      <news:title>{a['title']}</news:title>
    </news:news>
  </url>""")
    out.append("</urlset>")
    return "\n".join(out)


def render_robots() -> str:
    return f"""User-agent: *
Allow: /
Disallow: /api/
Disallow: /backend/
Disallow: /admin
Disallow: /admin/
Disallow: /dashboard
Disallow: /login
Disallow: /kennisbank
Disallow: /index-chatbot-backup
Disallow: /index-old
Disallow: /chatbot-landing
Disallow: /chatbot-split
Disallow: /chatbot-test
Disallow: /*?utm_*

Sitemap: {SITE_URL}/sitemap.xml
Sitemap: {SITE_URL}/sitemap-images.xml
Sitemap: {SITE_URL}/sitemap-news.xml
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
    <title>BotLease Nieuws - humanoïde robots in Nederland</title>
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

    # Per artikel - "related" = next 2 nieuwere/oudere
    for i, a in enumerate(articles_sorted):
        related = [x for x in articles_sorted if x["slug"] != a["slug"]][:2]
        (NEWS_DIR / f"{a['slug']}.html").write_text(render_article(a, related), encoding="utf-8")

    (NEWS_DIR / "index.html").write_text(render_listing(articles_sorted), encoding="utf-8")
    # sitemap.xml / sitemap-images.xml / robots.txt worden NIET meer door de news-bot
    # overschreven: deze bevatten alle 73 pagina's (incl. de SEO-landingspagina's) en
    # worden los onderhouden. render_sitemap() hier kent alleen nieuws + een verouderde
    # statische lijst → zou de 13 nieuwe pagina's uit de sitemap gooien. (1 juni 2026)
    # (FRONTEND / "sitemap.xml").write_text(render_sitemap(articles_sorted), encoding="utf-8")
    # (FRONTEND / "sitemap-images.xml").write_text(render_image_sitemap(), encoding="utf-8")
    # (FRONTEND / "robots.txt").write_text(render_robots(), encoding="utf-8")
    (FRONTEND / "sitemap-news.xml").write_text(render_news_sitemap(articles_sorted), encoding="utf-8")
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
