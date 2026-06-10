#!/usr/bin/env python3
"""BotLease CRM — leads/aanvragen-overzicht op de VPS.

- SQLite (crm.db naast dit bestand) + stdlib http.server, geen dependencies.
- Draait op 127.0.0.1:8788 achter nginx (https://crm.botlease.nl/).
- Auth: dashboard/API via ?key= of X-CRM-Key (CRM_ACCESS_KEY);
        website-webhook via X-CRM-Secret (CRM_WEBHOOK_SECRET).
- UI in BotLease-huisstijl (Inter, Apple-clean) met leveranciers-blok bij bestellingen.

Endpoints (pad-prefix /crm wordt gestript voor compatibiliteit):
  GET  /              dashboard-UI
  GET  /api/leads     alle leads (JSON)
  POST /api/lead      nieuwe lead (webhook vanaf botlease.nl-formulier)
  POST /api/add       handmatig toevoegen via UI
  POST /api/update    {id, status?, notes?} bijwerken
"""
import json
import os
import sqlite3
import socketserver
import http.server
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, parse_qs

BASE = Path(__file__).resolve().parent
DB = BASE / "crm.db"
PORT = 8788
ACCESS_KEY = os.environ.get("CRM_ACCESS_KEY", "")
WEBHOOK_SECRET = os.environ.get("CRM_WEBHOOK_SECRET", "")

STATUSES = ["nieuw", "beantwoord", "in gesprek", "offerte", "gewonnen", "verloren", "on hold"]


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created TEXT NOT NULL,
            updated TEXT NOT NULL,
            source TEXT NOT NULL DEFAULT 'formulier',
            name TEXT DEFAULT '', company TEXT DEFAULT '',
            email TEXT DEFAULT '', phone TEXT DEFAULT '',
            subject TEXT DEFAULT '', message TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'nieuw',
            notes TEXT DEFAULT '')""")
        # migraties: robot + sourcing (leveranciers-info bij bestellingen)
        for col in ("robot", "sourcing"):
            try:
                con.execute(f"ALTER TABLE leads ADD COLUMN {col} TEXT DEFAULT ''")
            except sqlite3.OperationalError:
                pass  # bestaat al


def add_lead(d: dict, source: str) -> int:
    with db() as con:
        cur = con.execute(
            "INSERT INTO leads (created, updated, source, name, company, email, phone,"
            " subject, message, status, notes, robot, sourcing) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (now(), now(), source,
             str(d.get("name") or d.get("naam") or "")[:200],
             str(d.get("company") or d.get("bedrijf") or "")[:200],
             str(d.get("email") or "")[:200],
             str(d.get("phone") or d.get("telefoon") or "")[:80],
             str(d.get("subject") or d.get("onderwerp") or d.get("usecase") or "")[:300],
             str(d.get("message") or d.get("bericht") or "")[:8000],
             d.get("status") if d.get("status") in STATUSES else "nieuw",
             str(d.get("notes") or "")[:8000],
             str(d.get("robot") or "")[:200],
             str(d.get("sourcing") or "")[:500]))
        return cur.lastrowid


PAGE = r"""<!DOCTYPE html><html lang="nl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex,nofollow"><title>BotLease CRM</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:#fbfbfd;--bg2:#f5f5f7;--card:#fff;--line:#e5e5e7;--ink:#1d1d1f;--ink2:#424245;--ink3:#6e6e73;
--accent:#0066cc;--accent-soft:#e8f0fe;--green:#1d8a3f;--green-soft:#e6f8eb;--amber:#b45309;--amber-soft:#fef3c7;
--red:#b91c1c;--red-soft:#fee2e2;--purple:#6d28d9;--purple-soft:#ede9fe;--r:14px}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',-apple-system,sans-serif;background:var(--bg);color:var(--ink);font-size:15px;line-height:1.5;-webkit-font-smoothing:antialiased}
.wrap{max-width:980px;margin:0 auto;padding:28px 20px 80px}
header{display:flex;align-items:center;gap:12px;margin-bottom:6px}
.mark{width:34px;height:34px;background:var(--ink);border-radius:9px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:15px}
h1{font-size:22px;font-weight:800;letter-spacing:-0.02em}
.sub{color:var(--ink3);font-size:13px;margin:2px 0 18px}
#saved{color:var(--green);font-size:12.5px;font-weight:600;opacity:0;transition:opacity .3s;margin-left:10px}
.stats{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:18px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 16px;min-width:86px}
.stat b{display:block;font-size:20px;letter-spacing:-0.02em}
.stat span{font-size:11.5px;color:var(--ink3);text-transform:uppercase;letter-spacing:.05em;font-weight:600}
.bar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:16px}
.chip{border:1px solid var(--line);background:var(--card);border-radius:99px;padding:6px 14px;font-size:13px;font-weight:600;color:var(--ink2);cursor:pointer}
.chip.on{background:var(--ink);color:#fff;border-color:var(--ink)}
#zoek{flex:1;min-width:160px;border:1px solid var(--line);border-radius:99px;padding:8px 16px;font:14px 'Inter';background:var(--card)}
.lead{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:18px 20px;margin-bottom:12px;box-shadow:0 1px 2px rgba(0,0,0,.03)}
.lead.s-nieuw{border-left:4px solid var(--accent)}
.top{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:baseline}
.who{font-weight:700;font-size:16px}.who small{font-weight:500;color:var(--ink3);font-size:13.5px}
.tijd{font-size:12px;color:var(--ink3)}
.badges{display:flex;gap:6px;margin:6px 0 2px;flex-wrap:wrap}
.badge{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;padding:3px 10px;border-radius:99px;background:var(--bg2);color:var(--ink2)}
.badge.order{background:var(--amber-soft);color:var(--amber)}
.badge.mail{background:var(--purple-soft);color:var(--purple)}
.badge.st-nieuw{background:var(--accent-soft);color:var(--accent)}
.badge.st-beantwoord,.badge.st-gewonnen{background:var(--green-soft);color:var(--green)}
.badge.st-in-gesprek,.badge.st-offerte{background:var(--amber-soft);color:var(--amber)}
.badge.st-verloren{background:var(--red-soft);color:var(--red)}
.badge.st-on-hold{background:var(--bg2);color:var(--ink3)}
.contact{font-size:13.5px;color:var(--ink2);margin:4px 0}
.contact a{color:var(--accent);text-decoration:none;font-weight:600}
.msg{white-space:pre-wrap;font-size:14px;color:var(--ink2);background:var(--bg2);border-radius:10px;padding:12px 14px;margin:10px 0;max-height:130px;overflow:hidden;cursor:pointer;position:relative}
.msg.open{max-height:none}
.msg.clamp:not(.open)::after{content:"meer tonen ▾";position:absolute;bottom:0;left:0;right:0;padding:22px 14px 8px;background:linear-gradient(transparent,var(--bg2) 60%);color:var(--accent);font-weight:600;font-size:12.5px}
.supplier{background:var(--accent-soft);border:1px solid #b8d4f1;border-radius:10px;padding:11px 14px;margin:10px 0;font-size:13.5px}
.supplier b{color:var(--accent)}
.acts{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:10px}
select,textarea,input{font:13.5px 'Inter';border:1px solid var(--line);border-radius:9px;padding:7px 10px;background:var(--card);color:var(--ink)}
textarea{width:100%;resize:vertical;margin-top:8px}
.btn{display:inline-block;background:var(--accent);color:#fff;border:none;border-radius:99px;padding:8px 16px;font:600 13px 'Inter';cursor:pointer;text-decoration:none}
.btn.ghost{background:var(--bg2);color:var(--ink)}
details{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:14px 18px;margin-bottom:18px}
summary{cursor:pointer;font-weight:700;font-size:14px;color:var(--ink2)}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0 8px}
@media(max-width:600px){.grid{grid-template-columns:1fr}}
.leeg{text-align:center;color:var(--ink3);padding:40px 0}
</style></head><body><div class="wrap">
<header><div class="mark">B</div><h1>BotLease CRM</h1><span id="saved">opgeslagen ✓</span></header>
<div class="sub">Site-aanvragen, bestellingen en mails aan hallo@botlease.nl — automatisch verzameld. De mail-notificaties blijf je gewoon ontvangen.</div>
<div class="stats" id="stats"></div>
<details><summary>＋ Handmatig toevoegen (bv. mail plakken)</summary>
  <div class="grid">
    <input id="a-name" placeholder="Naam">
    <input id="a-company" placeholder="Bedrijf">
    <input id="a-email" placeholder="E-mail">
    <input id="a-subject" placeholder="Onderwerp">
  </div>
  <textarea id="a-message" rows="5" placeholder="Plak hier de mail of het bericht…"></textarea>
  <div class="acts"><button class="btn" onclick="addLead()">Toevoegen</button></div>
</details>
<div class="bar" id="filters"></div>
<div id="list"><div class="leeg">laden…</div></div>
<script>
const KEY=new URLSearchParams(location.search).get('key')||'';
const STATUSES=__STATUSES__;
let LEADS=[],FILTER='alles',ZOEK='';
const flash=()=>{const s=document.getElementById('saved');s.style.opacity=1;setTimeout(()=>s.style.opacity=0,1400);};
async function api(p,body){const r=await fetch(p+(p.includes('?')?'&':'?')+'key='+encodeURIComponent(KEY),
 body?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}:{});
 if(!r.ok){document.getElementById('list').innerHTML='<div class="leeg">Geen toegang ('+r.status+') — open de volledige link mét ?key=…</div>';throw 0;}
 return r.json();}
const esc=s=>{const d=document.createElement('div');d.textContent=s||'';return d.innerHTML;};
const cls=s=>'st-'+s.replace(/ /g,'-');
function ago(iso){if(!iso)return'';const m=(Date.now()-new Date(iso))/60000;
 if(m<60)return Math.max(1,m|0)+' min geleden';if(m<1440)return (m/60|0)+' uur geleden';
 const d=m/1440|0;return d===1?'gisteren':d+' dagen geleden';}
function stats(){const c={};LEADS.forEach(l=>c[l.status]=(c[l.status]||0)+1);
 const open=(c['nieuw']||0)+(c['in gesprek']||0)+(c['offerte']||0);
 document.getElementById('stats').innerHTML=
  `<div class="stat"><b>${LEADS.length}</b><span>totaal</span></div>`+
  `<div class="stat"><b style="color:var(--accent)">${c['nieuw']||0}</b><span>nieuw</span></div>`+
  `<div class="stat"><b style="color:var(--amber)">${open}</b><span>open</span></div>`+
  `<div class="stat"><b style="color:var(--green)">${c['gewonnen']||0}</b><span>gewonnen</span></div>`;}
function filters(){const f=['alles','nieuw','open','gewonnen'];
 document.getElementById('filters').innerHTML=f.map(x=>`<button class="chip ${FILTER===x?'on':''}" onclick="FILTER='${x}';draw()">${x[0].toUpperCase()+x.slice(1)}</button>`).join('')+
 `<input id="zoek" placeholder="Zoeken…" value="${esc(ZOEK)}" oninput="ZOEK=this.value;draw(true)">`;}
function visible(l){
 if(FILTER==='nieuw'&&l.status!=='nieuw')return false;
 if(FILTER==='open'&&!['nieuw','in gesprek','offerte'].includes(l.status))return false;
 if(FILTER==='gewonnen'&&l.status!=='gewonnen')return false;
 if(ZOEK){const h=(l.name+' '+l.company+' '+l.email+' '+l.subject+' '+l.message).toLowerCase();
  if(!h.includes(ZOEK.toLowerCase()))return false;}
 return true;}
let timers={};
function draw(keepFocus){
 stats();if(!keepFocus)filters();
 const el=document.getElementById('list');el.innerHTML='';
 const rows=LEADS.filter(visible);
 if(!rows.length){el.innerHTML='<div class="leeg">Geen leads in deze weergave.</div>';return;}
 rows.forEach(l=>{
  const d=document.createElement('div');d.className='lead s-'+l.status.replace(/ /g,'-');
  const isOrder=(l.subject||'').includes('BESTELLING')||!!l.sourcing;
  const reSub=encodeURIComponent('Re: uw aanvraag bij BotLease');
  d.innerHTML=`
   <div class="top"><div class="who">${esc(l.name)||'(geen naam)'} ${l.company?`<small>· ${esc(l.company)}</small>`:''}</div>
   <div class="tijd">#${l.id} · ${ago(l.created)}</div></div>
   <div class="badges">
     <span class="badge ${l.source==='mail'?'mail':''} ${isOrder?'order':''}">${isOrder?'bestelling':esc(l.source)}</span>
     <span class="badge ${cls(l.status)}">${esc(l.status)}</span>
     ${l.robot?`<span class="badge">${esc(l.robot)}</span>`:''}
   </div>
   ${l.subject?`<div class="contact">${esc(l.subject)}</div>`:''}
   <div class="contact">${l.email?`<a href="mailto:${esc(l.email)}">${esc(l.email)}</a>`:''} ${l.phone?' · '+esc(l.phone):''}</div>
   ${l.message?`<div class="msg" onclick="this.classList.toggle('open')">${esc(l.message)}</div>`:''}
   ${l.sourcing?`<div class="supplier">📦 <b>Bestellen bij:</b> ${esc(l.sourcing)}</div>`:''}
   <div class="acts">
     <select data-id="${l.id}" class="st">${STATUSES.map(s=>`<option ${s===l.status?'selected':''}>${s}</option>`).join('')}</select>
     ${l.email?`<a class="btn" href="mailto:${esc(l.email)}?subject=${reSub}">✉️ Beantwoorden</a>`:''}
   </div>
   <textarea class="nt" data-id="${l.id}" rows="2" placeholder="Notities / opvolging…">${esc(l.notes)}</textarea>`;
  el.appendChild(d);});
 el.querySelectorAll('.msg').forEach(m=>{if(m.scrollHeight>140)m.classList.add('clamp');});
 el.querySelectorAll('select.st').forEach(s=>s.onchange=async e=>{
  await api('api/update',{id:+e.target.dataset.id,status:e.target.value});
  const L=LEADS.find(x=>x.id==e.target.dataset.id);L.status=e.target.value;flash();draw();});
 el.querySelectorAll('textarea.nt').forEach(t=>t.oninput=e=>{clearTimeout(timers[e.target.dataset.id]);
  timers[e.target.dataset.id]=setTimeout(async()=>{await api('api/update',{id:+e.target.dataset.id,notes:e.target.value});flash();},500);});}
async function load(){LEADS=await api('api/leads');draw();}
async function addLead(){const v=id=>document.getElementById(id).value;
 await api('api/add',{name:v('a-name'),company:v('a-company'),email:v('a-email'),subject:v('a-subject'),message:v('a-message'),source:'handmatig'});
 ['a-name','a-company','a-email','a-subject','a-message'].forEach(i=>document.getElementById(i).value='');flash();load();}
load();
</script></div></body></html>"""


class Handler(http.server.BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _path(self):
        p = urlparse(self.path)
        path = p.path
        if path.startswith("/crm"):
            path = path[4:] or "/"
        return path, parse_qs(p.query)

    def _authed(self, q):
        key = (q.get("key", [""])[0] or self.headers.get("X-CRM-Key", ""))
        return ACCESS_KEY and key == ACCESS_KEY

    def _body(self):
        n = int(self.headers.get("Content-Length", 0) or 0)
        if n > 200_000:
            return None
        try:
            return json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return None

    def do_GET(self):
        path, q = self._path()
        if path in ("/", "/index.html"):
            if not self._authed(q):
                return self._send(401, "<h3>401 - open de volledige link met ?key=...</h3>".encode(), "text/html; charset=utf-8")
            return self._send(200, PAGE.replace("__STATUSES__", json.dumps(STATUSES)).encode(), "text/html; charset=utf-8")
        if path == "/api/leads":
            if not self._authed(q):
                return self._send(401, {"error": "unauthorized"})
            with db() as con:
                rows = [dict(r) for r in con.execute(
                    "SELECT * FROM leads ORDER BY CASE status WHEN 'nieuw' THEN 0 ELSE 1 END, id DESC")]
            return self._send(200, rows)
        if path == "/health":
            return self._send(200, {"ok": True})
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        path, q = self._path()
        d = self._body()
        if d is None:
            return self._send(400, {"error": "bad json"})
        if path == "/api/lead":  # webhook vanaf botlease.nl
            if not (WEBHOOK_SECRET and self.headers.get("X-CRM-Secret", "") == WEBHOOK_SECRET):
                return self._send(401, {"error": "unauthorized"})
            lid = add_lead(d, str(d.get("source") or "formulier")[:40])
            return self._send(200, {"ok": True, "id": lid})
        if not self._authed(q):
            return self._send(401, {"error": "unauthorized"})
        if path == "/api/add":
            lid = add_lead(d, str(d.get("source") or "handmatig")[:40])
            return self._send(200, {"ok": True, "id": lid})
        if path == "/api/update":
            sets, vals = [], []
            if d.get("status") in STATUSES:
                sets.append("status=?"); vals.append(d["status"])
            if "notes" in d:
                sets.append("notes=?"); vals.append(str(d["notes"])[:8000])
            if not sets or not isinstance(d.get("id"), int):
                return self._send(400, {"error": "geen velden"})
            sets.append("updated=?"); vals.append(now()); vals.append(d["id"])
            with db() as con:
                con.execute(f"UPDATE leads SET {', '.join(sets)} WHERE id=?", vals)
            return self._send(200, {"ok": True})
        return self._send(404, {"error": "not found"})

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    if not (ACCESS_KEY and WEBHOOK_SECRET):
        raise SystemExit("CRM_ACCESS_KEY en CRM_WEBHOOK_SECRET zijn verplicht (env).")
    init_db()
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"BotLease CRM op 127.0.0.1:{PORT}")
        httpd.serve_forever()
