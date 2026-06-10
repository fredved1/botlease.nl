#!/usr/bin/env python3
"""BotLease CRM — leads/aanvragen-overzicht op de VPS.

- SQLite (crm.db naast dit bestand) + stdlib http.server, geen dependencies.
- Draait op 127.0.0.1:8788 achter nginx (https://api.heymilo.nl/crm/).
- Auth: dashboard/API-reads via ?key= of X-CRM-Key (ACCESS_KEY);
        website-webhook via X-CRM-Secret (WEBHOOK_SECRET).
- Secrets in env-file (systemd EnvironmentFile), zie botlease-crm.service.

Endpoints (pad-prefix /crm wordt gestript):
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


def add_lead(d: dict, source: str) -> int:
    with db() as con:
        cur = con.execute(
            "INSERT INTO leads (created, updated, source, name, company, email, phone, subject, message, status, notes)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (now(), now(), source,
             str(d.get("name") or d.get("naam") or "")[:200],
             str(d.get("company") or d.get("bedrijf") or "")[:200],
             str(d.get("email") or "")[:200],
             str(d.get("phone") or d.get("telefoon") or "")[:80],
             str(d.get("subject") or d.get("onderwerp") or d.get("usecase") or "")[:300],
             str(d.get("message") or d.get("bericht") or "")[:8000],
             d.get("status") if d.get("status") in STATUSES else "nieuw",
             str(d.get("notes") or "")[:8000]))
        return cur.lastrowid


PAGE = r"""<!DOCTYPE html><html lang="nl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex,nofollow"><title>BotLease CRM</title>
<style>
body{font-family:-apple-system,Inter,Arial,sans-serif;max-width:1060px;margin:22px auto;padding:0 16px;color:#1d1d1f;background:#fbfbfd;line-height:1.45}
h1{font-size:22px;margin-bottom:2px}
#stats{font-size:13.5px;font-weight:600;color:#0a3d7a;background:#eef3fb;border-radius:9px;padding:9px 13px;margin:12px 0}
.lead{background:#fff;border:1px solid #e5e5e7;border-radius:12px;margin:10px 0;padding:13px 16px}
.lead.nieuw{border-left:4px solid #0066cc}
.top{display:flex;justify-content:space-between;gap:10px;align-items:baseline;flex-wrap:wrap}
.who{font-weight:700;font-size:15px}.who small{font-weight:400;color:#6e6e73}
.meta{font-size:12px;color:#86868b}
.msg{white-space:pre-wrap;font-size:13.5px;color:#424245;background:#f5f5f7;border-radius:8px;padding:10px 12px;margin:8px 0}
select,input,textarea,button{font:13px -apple-system,Inter,Arial,sans-serif;padding:6px 8px;border:1px solid #d2d2d7;border-radius:7px;background:#fff;color:#1d1d1f}
textarea{width:100%;box-sizing:border-box;resize:vertical}
button{cursor:pointer;font-weight:600}
button.primary{background:#0066cc;color:#fff;border:0;padding:9px 16px;border-radius:9px}
.row{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:6px}
#saved{color:#1d8a3f;font-size:12.5px;opacity:0;transition:opacity .3s;margin-left:8px}
details{margin:16px 0}summary{cursor:pointer;font-weight:600;font-size:14px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0}
.badge{font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;font-weight:700;padding:2px 8px;border-radius:99px;background:#eef3fb;color:#0a3d7a}
a{color:#0066cc}
</style></head><body>
<h1>BotLease CRM <span id="saved">opgeslagen ✓</span></h1>
<div style="font-size:12.5px;color:#86868b">Aanvragen via botlease.nl komen hier automatisch binnen. Mails uit Hotmail: plak ze via "handmatig toevoegen".</div>
<div id="stats">laden…</div>

<details><summary>＋ Handmatig toevoegen (bv. mail uit je inbox plakken)</summary>
  <div class="grid">
    <input id="a-name" placeholder="Naam">
    <input id="a-company" placeholder="Bedrijf">
    <input id="a-email" placeholder="E-mail">
    <input id="a-subject" placeholder="Onderwerp">
  </div>
  <textarea id="a-message" rows="6" placeholder="Plak hier de mail of het bericht…"></textarea>
  <div class="row"><button class="primary" onclick="addLead()">Toevoegen</button></div>
</details>

<div id="list">laden…</div>
<script>
const KEY=new URLSearchParams(location.search).get('key')||'';
const STATUSES=__STATUSES__;
function flash(){const s=document.getElementById('saved');s.style.opacity=1;setTimeout(()=>s.style.opacity=0,1400);}
async function api(path,body){
  const r=await fetch(path+(path.includes('?')?'&':'?')+'key='+encodeURIComponent(KEY),
    body?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}:{});
  if(!r.ok){document.getElementById('stats').textContent='Fout: '+r.status+' — klopt je ?key= in de URL?';throw new Error(r.status);}
  return r.json();
}
function esc(s){const d=document.createElement('div');d.textContent=s||'';return d.innerHTML;}
let timers={};
function render(leads){
  const counts={};leads.forEach(l=>counts[l.status]=(counts[l.status]||0)+1);
  document.getElementById('stats').textContent=leads.length+' leads totaal · '+STATUSES.filter(s=>counts[s]).map(s=>counts[s]+' '+s).join(' · ');
  const el=document.getElementById('list');el.innerHTML='';
  leads.forEach(l=>{
    const d=document.createElement('div');d.className='lead'+(l.status==='nieuw'?' nieuw':'');
    d.innerHTML=`<div class="top">
      <div class="who">${esc(l.name)||'(geen naam)'} <small>${esc(l.company)}</small></div>
      <div class="meta">#${l.id} · ${esc(l.source)} · ${esc((l.created||'').slice(0,16).replace('T',' '))}</div></div>
    <div class="meta">${l.email?`<a href="mailto:${esc(l.email)}">${esc(l.email)}</a>`:''} ${esc(l.phone)} ${l.subject?'· '+esc(l.subject):''}</div>
    ${l.message?`<div class="msg">${esc(l.message)}</div>`:''}
    <div class="row">
      <select data-id="${l.id}" class="st">${STATUSES.map(s=>`<option ${s===l.status?'selected':''}>${s}</option>`).join('')}</select>
      <span class="badge">${esc(l.status)}</span>
    </div>
    <textarea class="nt" data-id="${l.id}" rows="2" placeholder="Notities / opvolging…">${esc(l.notes)}</textarea>`;
    el.appendChild(d);
  });
  el.querySelectorAll('select.st').forEach(s=>s.onchange=async e=>{await api('api/update',{id:+e.target.dataset.id,status:e.target.value});flash();load();});
  el.querySelectorAll('textarea.nt').forEach(t=>t.oninput=e=>{clearTimeout(timers[e.target.dataset.id]);
    timers[e.target.dataset.id]=setTimeout(async()=>{await api('api/update',{id:+e.target.dataset.id,notes:e.target.value});flash();},500);});
}
async function load(){render(await api('api/leads'));}
async function addLead(){
  const v=id=>document.getElementById(id).value;
  await api('api/add',{name:v('a-name'),company:v('a-company'),email:v('a-email'),subject:v('a-subject'),message:v('a-message'),source:'handmatig'});
  ['a-name','a-company','a-email','a-subject','a-message'].forEach(i=>document.getElementById(i).value='');
  flash();load();
}
load();
</script></body></html>"""


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
                return self._send(401, "<h3>401 - voeg ?key=... toe aan de URL</h3>".encode(), "text/html; charset=utf-8")
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
