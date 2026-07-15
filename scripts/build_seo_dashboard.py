#!/usr/bin/env python3
"""
Bouwt het interne SEO-dashboard op /admin/seo (noindex).
Bron: /seo/seo_data.json — bevat target keywords, competitors, historische rank-checks, fixes-log.

Run: python3 scripts/build_seo_dashboard.py
Output: frontend/admin/seo.html
"""
from __future__ import annotations
import json
from datetime import datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "seo" / "seo_data.json"
ANALYTICS = ROOT / "seo" / "analytics_snapshot.json"
OUT = ROOT / "frontend" / "admin" / "seo.html"

with DATA.open() as f:
    data = json.load(f)

analytics = None
if ANALYTICS.exists():
    try:
        analytics = json.loads(ANALYTICS.read_text(encoding="utf-8"))
    except Exception:
        analytics = None


def undash(s: str) -> str:
    """Em-dashes in datagedreven copy -> koppelteken (AI-cadans-tell, playbook 15).

    Placeholders (kale em-dash zonder omliggende tekst) blijven staan; alleen
    lopende copy uit seo_data.json wordt genormaliseerd.
    """
    return s.replace(" — ", " - ").replace("—", "-") if len(s) > 1 else s


def fmt_n(n) -> str:
    if not isinstance(n, (int, float)):
        return "—"
    n = int(n)
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}k"
    return str(n)


def render_analytics() -> str:
    # Pivot: Vercel Web Analytics is de bron. Self-hosted Umami stuk op cross-origin/firewall.
    return """
<h2>Analytics - Live verkeer</h2>
<div class="card" style="background:linear-gradient(135deg, #f0fdf4, #ecfdf5); border-color:#bbf7d0">
  <p style="margin-bottom:14px; font-size:15px"><b>Vercel Web Analytics + Speed Insights</b> draait live op alle pagina's. Per-pagina views, top referrers, devices, landen, Core Web Vitals.</p>
  <a href="https://vercel.com/fredved1s-projects/botlease-v2/analytics" target="_blank"
     style="display:inline-block; padding:10px 18px; background:#0070f3; color:#fff; border-radius:8px; font-weight:600; font-size:14px; text-decoration:none">
    Open Vercel Analytics dashboard &rarr;
  </a>
  <p style="margin-top:12px; font-size:12.5px; color:#525252">
    Status afgelopen 7 dagen (laatste check): <b>12 bezoekers, 13 page views, 9 vanuit google.com</b> &mdash; Google indexeert organisch.
  </p>
</div>"""
    if not analytics:
        return """
<h2>Analytics</h2>
<div class="card" style="color:#737373">
  Nog geen Umami snapshot beschikbaar. Run <code>python3 scripts/analytics_bot.py --rebuild</code> op de VPS
  om verkeer + custom events op te halen. Eerste data verschijnt zodra de DNS-record
  <code>analytics.botlease.nl A 185.107.90.42</code> bij Hostnet is gezet en de tracker een paar pageviews heeft gezien.
</div>"""
    periods = analytics.get("periods", {})
    p7 = periods.get("7d", {})
    p30 = periods.get("30d", {})
    p24 = periods.get("24h", {})

    def stat_v(per: dict, key: str) -> str:
        s = per.get("stats", {})
        if not isinstance(s, dict):
            return "—"
        val = s.get(key, 0)
        if isinstance(val, dict):
            val = val.get("value", 0)
        return fmt_n(val)

    def bar_table(items: list, key_name: str = "x", val_label: str = "Visits", max_rows: int = 8) -> str:
        if not isinstance(items, list) or not items:
            return '<p style="color:#a3a3a3; font-size:12.5px">(geen data)</p>'
        max_val = max((it.get("y", 0) for it in items), default=1) or 1
        rows = []
        for it in items[:max_rows]:
            label = str(it.get("x") or "(direct/none)")[:60]
            val = it.get("y", 0)
            pct = int(100 * val / max_val) if max_val else 0
            rows.append(
                f'<tr><td style="font-size:12.5px">{escape(label)}</td>'
                f'<td style="width:40%"><div style="background:#dbeafe; height:6px; width:{pct}%; '
                f'border-radius:3px; display:inline-block"></div></td>'
                f'<td style="text-align:right; font-variant-numeric:tabular-nums; color:#525252">{val}</td></tr>'
            )
        return f'<table style="width:100%"><tbody>{"".join(rows)}</tbody></table>'

    # Funnel calc — find conversion key events in events list
    events_7d = p7.get("events", []) if isinstance(p7.get("events"), list) else []
    ev_map = {it.get("x", ""): it.get("y", 0) for it in events_7d if isinstance(it, dict)}
    view = ev_map.get("cta_aanvraag_view", 0)
    submit = ev_map.get("cta_aanvraag_submit", 0)
    model_clicks = sum(v for k, v in ev_map.items() if k == "model_card_click")
    waitlist = ev_map.get("waitlist_signup", 0)
    cvr = (submit / view * 100) if view else 0

    return f"""
<h2>Analytics - Umami</h2>
<p class="muted" style="margin-top:-8px">Snapshot: {escape(analytics.get('generated_at', '')[:19])}. Live dashboard: <a href="https://analytics.botlease.nl" target="_blank">analytics.botlease.nl</a></p>

<div class="stats">
  <div class="stat"><div class="label">Pageviews 24h</div><div class="v">{stat_v(p24, 'pageviews')}</div><div class="sub">{stat_v(p24, 'visitors')} unieke bezoekers</div></div>
  <div class="stat"><div class="label">Pageviews 7d</div><div class="v">{stat_v(p7, 'pageviews')}</div><div class="sub">{stat_v(p7, 'visitors')} unieke bezoekers</div></div>
  <div class="stat"><div class="label">Pageviews 30d</div><div class="v">{stat_v(p30, 'pageviews')}</div><div class="sub">{stat_v(p30, 'visitors')} unieke bezoekers</div></div>
  <div class="stat"><div class="label">Sessieduur 7d</div><div class="v">{stat_v(p7, 'totaltime')}s</div><div class="sub">cumulatief</div></div>
</div>

<h2 style="font-size:15px; border:none; padding-bottom:0; margin-top:32px">Funnel - afgelopen 7 dagen</h2>
<div class="stats">
  <div class="stat"><div class="label">Aanvraag form views</div><div class="v">{view}</div><div class="sub">cta_aanvraag_view</div></div>
  <div class="stat"><div class="label">Aanvraag submits</div><div class="v" style="color:#16a34a">{submit}</div><div class="sub">conversie {cvr:.1f}%</div></div>
  <div class="stat"><div class="label">Model-card kliks</div><div class="v">{model_clicks}</div><div class="sub">interest signal</div></div>
  <div class="stat"><div class="label">Wachtlijst signups</div><div class="v">{waitlist}</div><div class="sub">Apollo/Figure/etc</div></div>
</div>

<div style="display:grid; grid-template-columns:1fr; gap:16px; margin-top:18px">
  <div class="card"><b>Top pagina's (7d)</b>{bar_table(p7.get('top_pages', []), val_label='Views')}</div>
  <div class="card"><b>Top referrers (7d)</b>{bar_table(p7.get('top_referrers', []), val_label='Hits')}</div>
  <div class="card"><b>Landen (7d)</b>{bar_table(p7.get('countries', []), val_label='Visitors')}</div>
  <div class="card"><b>Events (7d)</b>{bar_table(p7.get('events', []), val_label='Triggers', max_rows=15)}</div>
</div>
"""


ANALYTICS_SECTION = render_analytics()

target_kws = data["target_keywords"]
# Sorteer checks op datum (ascending) zodat trend/laatste-datum-logica correct werkt.
# Pre-sorteer hier zodat alle downstream code consistent is.
checks = sorted(data.get("checks", []), key=lambda c: c.get("date", ""))
competitors = data.get("competitors", [])
fixes_done = data.get("fixes_done", [])
fixes_open = data.get("fixes_open", [])

# Build keyword history table — laatste 4 checks per kw
def history_for(kw_id):
    out = []
    for check in checks[-6:]:
        rank = check.get("ranks", {}).get(kw_id, {})
        if isinstance(rank, dict):
            pos = rank.get("position", 0)
        else:
            pos = rank or 0
        out.append({"date": check["date"], "position": pos})
    return out

# Status pill voor positie
def pos_pill(pos):
    if pos == 0:
        return '<span class="pill pill-bad">niet in top 30</span>'
    if pos <= 3:
        return f'<span class="pill pill-great">#{pos}</span>'
    if pos <= 10:
        return f'<span class="pill pill-good">#{pos}</span>'
    if pos <= 20:
        return f'<span class="pill pill-okay">#{pos}</span>'
    return f'<span class="pill pill-meh">#{pos}</span>'

# Tabel rijen
rows_html = ""
for kw in target_kws:
    hist = history_for(kw["id"])
    current = hist[-1]["position"] if hist else 0
    prev = hist[-2]["position"] if len(hist) >= 2 else None
    trend = ""
    if prev is not None and current and prev:
        if current < prev:
            trend = f'<span style="color:#16a34a">▲ {prev - current}</span>'
        elif current > prev:
            trend = f'<span style="color:#dc2626">▼ {current - prev}</span>'
        else:
            trend = '<span style="color:#a3a3a3">–</span>'
    elif prev is None and current:
        trend = '<span style="color:#a3a3a3">nieuw</span>'

    priority_color = {"P0": "#dc2626", "P1": "#ea580c", "P2": "#a3a3a3"}.get(kw["priority"], "#a3a3a3")
    rows_html += f"""
    <tr>
      <td><span style="display:inline-block; padding:2px 7px; border-radius:6px; background:{priority_color}; color:#fff; font-size:10px; font-weight:600">{escape(kw['priority'])}</span></td>
      <td><b>{escape(kw['kw'])}</b><br><span style="color:#737373; font-size:11px">→ <a href="{escape(kw['target_page'])}" style="color:#737373">{escape(kw['target_page'])}</a></span></td>
      <td>{pos_pill(current)}</td>
      <td>{trend}</td>
      <td style="color:#737373; font-size:12px">{escape(undash(kw['intent']))}</td>
    </tr>"""

# Competitors tabel
comp_html = "".join(
    f'<tr><td><b>{escape(c["domain"])}</b><br><span style="color:#737373; font-size:11px">{escape(c.get("location", "—"))}</span></td>'
    f'<td><span class="pill pill-{ {"high":"bad", "medium":"okay", "low":"good"}.get(c["threat"], "okay") }">{escape(c["threat"])}</span></td>'
    f'<td style="color:#525252; font-size:12.5px">{escape(undash(c.get("notes", "")))}</td></tr>'
    for c in competitors
)

# Latest check info
last_check = checks[-1] if checks else None
total_kw = len(target_kws)
ranked_kw = sum(1 for kw in target_kws if any(c.get("ranks", {}).get(kw["id"], {}).get("position", 0) > 0 for c in checks[-1:]))
top10 = sum(1 for kw in target_kws if any(0 < c.get("ranks", {}).get(kw["id"], {}).get("position", 999) <= 10 for c in checks[-1:]))

# Fixes lijst
fixes_open_html = "".join(
    f'<li style="margin-bottom:10px"><b>{escape(undash(f.get("title", "")))}</b><br><span style="color:#737373; font-size:13px">{escape(undash(f.get("notes", "")))}</span></li>'
    for f in fixes_open
) or '<li style="color:#a3a3a3">Niets open - wel keywords ranken</li>'

fixes_done_html = "".join(
    f'<li style="margin-bottom:8px; color:#16a34a"><s style="color:#737373">{escape(undash(f.get("title", "")))}</s>'
    f' <span style="color:#16a34a; font-weight:600; font-size:11px">✓ {escape(f.get("date", ""))}</span></li>'
    for f in fixes_done
) or '<li style="color:#a3a3a3">Nog niets afgevinkt</li>'

html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex,nofollow,noarchive,nosnippet">
<title>SEO Dashboard - BotLease (intern)</title>
<link rel="stylesheet" href="/fonts/fonts.css">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family:'Hanken Grotesk', -apple-system, sans-serif;
  background: #fafaf9; color: #1c1917;
  font-size: 14px; line-height: 1.5;
  padding: 32px 24px;
}}
.container {{ max-width: 1100px; margin: 0 auto; }}
h1 {{
  font-size: 28px; font-weight: 700; letter-spacing: -0.02em;
  margin-bottom: 4px;
}}
h2 {{ font-family:'Bricolage Grotesque', -apple-system, sans-serif;
  font-size: 18px; font-weight: 600; letter-spacing: -0.01em;
  margin: 36px 0 14px;
  padding-bottom: 8px; border-bottom: 1px solid #e7e5e4;
}}
.muted {{ color: #737373; font-size: 13px; margin-bottom: 24px; }}
.stats {{
  display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;
  margin: 24px 0;
}}
@media (min-width: 720px) {{ .stats {{ grid-template-columns: repeat(4, 1fr); }} }}
.stat {{
  background: #fff; border: 1px solid #e7e5e4; border-radius: 10px;
  padding: 16px 18px;
}}
.stat .label {{ color: #737373; font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600; }}
.stat .v {{ font-size: 28px; font-weight: 700; letter-spacing: -0.02em; margin-top: 4px; }}
.stat .sub {{ color: #6e6e73; font-size: 12px; margin-top: 2px; }}
table {{
  width: 100%; border-collapse: collapse;
  background: #fff; border: 1px solid #e7e5e4; border-radius: 10px;
  overflow: hidden;
}}
th, td {{
  text-align: left; padding: 10px 14px;
  border-bottom: 1px solid #f5f5f4;
  font-size: 13px; vertical-align: top;
}}
th {{ background: #fafaf9; font-weight: 600; font-size: 11px; color: #525252; text-transform: uppercase; letter-spacing: 0.04em; }}
tr:last-child td {{ border-bottom: none; }}
.pill {{
  display: inline-block; padding: 3px 10px; border-radius: 999px;
  font-size: 11.5px; font-weight: 600;
}}
.pill-great {{ background: #d1fae5; color: #065f46; }}
.pill-good  {{ background: #dbeafe; color: #1e40af; }}
.pill-okay  {{ background: #fef3c7; color: #92400e; }}
.pill-meh   {{ background: #f3f4f6; color: #525252; }}
.pill-bad   {{ background: #fee2e2; color: #991b1b; }}
ul {{ list-style: none; padding: 0; }}
ul li {{ padding-left: 24px; position: relative; }}
ul li::before {{ content: "□"; position: absolute; left: 0; color: #a3a3a3; font-size: 16px; line-height: 1; top: 1px; }}
.card {{
  background: #fff; border: 1px solid #e7e5e4; border-radius: 10px;
  padding: 20px 22px;
}}
.banner {{
  background: #fef3c7; border: 1px solid #fde68a; border-radius: 10px;
  padding: 14px 18px; font-size: 13px; color: #78350f; margin-bottom: 28px;
}}
.banner strong {{ color: #92400e; }}
a {{ color: #0066cc; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
code {{ background: #f5f5f4; padding: 2px 6px; border-radius: 4px; font-size: 12px; }}
.footnote {{ color: #6e6e73; font-size: 12px; margin-top: 32px; padding-top: 20px; border-top: 1px solid #e7e5e4; }}
</style>
<!-- impeccable-disable numbered-section-markers -- datums en verificatietokens in intern SEO-rapport zijn data, geen sectiescaffold -->
</head>
<body>
<div class="container">

<h1>SEO Dashboard</h1>
<p class="muted">Intern overzicht - botlease.nl rankings, fixes en concurrentie. Gegenereerd: {datetime.now().strftime('%d-%m-%Y %H:%M')}.</p>

<div class="banner" style="background:#fff7ed; border:1px solid #f59e0b; color:#7c2d12">
  <strong>Actie vereist: Google re-crawl.</strong> De site is technisch maximaal (73/73 URLs 200, 288 JSON-LD blokken valide, mobile-first, &minus;52% paginagewicht via lazy-loaded Google Translate, IndexNow voor alle 73 URLs, verse sitemap-lastmod, llms.txt met alle pagina's). <b>MAAR:</b> <code>site:botlease.nl</code> toont in Google nog steeds de oude Milo-chatbot-homepage ("AI-assistent in 15 minuten | &euro;49/maand") &mdash; Google heeft de nieuwe humanoid-lease-site nog niet opnieuw gecrawld, waardoor de hele site onzichtbaar is voor de doeltermen.
  <p style="margin-top:10px; font-size:13px"><b>Deblokkeer dit (alleen jij kunt dit):</b> Google Search Console &rarr; property verifi&euml;ren &rarr; homepage URL-inspectie &rarr; "Indexering aanvragen" + sitemap indienen op <a href="https://search.google.com/search-console" target="_blank">search.google.com/search-console</a>. IndexNow bereikt Bing/Yandex w&eacute;l, maar Google niet. Pas na de re-crawl renderen de 13 nieuwe pagina's + fundering in Google.</p>
</div>

<div class="stats">
  <div class="stat">
    <div class="label">Keywords gevolgd</div>
    <div class="v">{total_kw}</div>
    <div class="sub">P0-P2 prioriteit</div>
  </div>
  <div class="stat">
    <div class="label">Rankings (top 30)</div>
    <div class="v" style="color:{'#16a34a' if ranked_kw > 0 else '#dc2626'}">{ranked_kw} / {total_kw}</div>
    <div class="sub">{f'{int(ranked_kw/total_kw*100)}%' if total_kw else '0%'}</div>
  </div>
  <div class="stat">
    <div class="label">Top 10</div>
    <div class="v" style="color:{'#16a34a' if top10 > 0 else '#737373'}">{top10}</div>
    <div class="sub">eerste pagina Google</div>
  </div>
  <div class="stat">
    <div class="label">Laatste check</div>
    <div class="v" style="font-size:18px">{escape(last_check['date']) if last_check else '—'}</div>
    <div class="sub">{escape(undash(last_check.get('method', '—'))[:30]) if last_check else ''}</div>
  </div>
</div>

{ANALYTICS_SECTION}

<h2>Keyword rankings</h2>
<table>
  <thead>
    <tr>
      <th>Prio</th>
      <th>Keyword → doelpagina</th>
      <th>Positie</th>
      <th>Trend</th>
      <th>Intent</th>
    </tr>
  </thead>
  <tbody>{rows_html}
  </tbody>
</table>

<h2>Concurrentie</h2>
<table>
  <thead>
    <tr>
      <th>Domein</th>
      <th>Dreiging</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>{comp_html}
  </tbody>
</table>

<h2>Fixes - nog te doen</h2>
<div class="card">
  <ul>{fixes_open_html}</ul>
</div>

<h2>Fixes - afgevinkt</h2>
<div class="card">
  <ul style="list-style:none">{fixes_done_html}</ul>
</div>

<h2>Hoe dit dashboard bijgewerkt wordt</h2>
<div class="card" style="font-size:13.5px; line-height:1.6">
  <p style="margin-bottom:10px"><b>1. Nieuwe rank-check toevoegen</b> - open <code>seo/seo_data.json</code> en voeg een nieuw entry toe aan de <code>checks</code> array met datum + posities per keyword. Voor handmatige checks: ga naar Google in een incognito venster, zoek het keyword, tel waar botlease.nl staat (0 = niet in top 30).</p>
  <p style="margin-bottom:10px"><b>2. Fix afvinken</b> - verplaats een entry van <code>fixes_open</code> naar <code>fixes_done</code> met datum.</p>
  <p style="margin-bottom:10px"><b>3. Rebuild dashboard</b> - <code>python3 scripts/build_seo_dashboard.py</code>.</p>
  <p><b>4. Echte automatisering</b> - voor wekelijkse automatische rank-tracking, koppel een SerpAPI of DataForSEO account (~$10-50/mnd). Of zet up Google Search Console (gratis) en exporteer wekelijks de "Performance" data - dat is de echte waarheid.</p>
</div>

<p class="footnote">
  Intern dashboard - niet indexeerbaar (noindex). Niet linken vanaf publieke pagina's. Toegang via <code>/admin/seo</code>.<br>
  Brondata: <code>seo/seo_data.json</code> · Builder: <code>scripts/build_seo_dashboard.py</code>
</p>

</div>
</body>
</html>
"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html, encoding="utf-8")
print(f"✅ Dashboard gebouwd: {OUT.relative_to(ROOT)}")
print(f"   {total_kw} keywords, {len(checks)} checks, {len(fixes_open)} open fixes, {len(fixes_done)} afgevinkt")
