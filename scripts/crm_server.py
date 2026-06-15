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
import smtplib
import sqlite3
from email.message import EmailMessage
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
SMTP_HOST = os.environ.get("CRM_SMTP_HOST", "smtp.hostnet.nl")
SMTP_PORT = int(os.environ.get("CRM_SMTP_PORT", "587"))
SMTP_USER = os.environ.get("CRM_SMTP_USER", "hallo@botlease.nl")
SMTP_PASS = os.environ.get("CRM_SMTP_PASS", "")  # leeg = direct-versturen uitgeschakeld


def smtp_accounts():
    """Beschikbare afzenders {adres: wachtwoord}. Uit CRM_IMAP_ACCOUNTS (gedeeld met de IMAP-poller),
    plus de losse CRM_SMTP_USER/PASS als fallback. Volgorde = keuzevolgorde in de UI."""
    out = {}
    raw = os.environ.get("CRM_IMAP_ACCOUNTS", "").strip()
    if raw:
        for pair in raw.split(","):
            if ":" in pair:
                u, p = pair.split(":", 1)
                out[u.strip()] = p.strip()
    if SMTP_USER and SMTP_PASS and SMTP_USER not in out:
        out = {SMTP_USER: SMTP_PASS, **out}
    return out

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
        con.execute("""CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created TEXT NOT NULL, updated TEXT NOT NULL,
            title TEXT NOT NULL, note TEXT DEFAULT '',
            mail_to TEXT DEFAULT '', mail_subject TEXT DEFAULT '', mail_body TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'open')""")
        try:
            con.execute("ALTER TABLE tasks ADD COLUMN lead_id INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass
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
:root{--bg:#fbfbfd;--bg2:#f5f5f7;--card:#fff;--line:#ececf0;--line2:#d2d2d7;--ink:#1d1d1f;--ink2:#424245;--ink3:#86868b;
--accent:#0066cc;--accent-soft:#e8f0fe;--green:#1d8a3f;--green-soft:#e6f8eb;--amber:#b45309;--amber-soft:#fef3c7;
--red:#b91c1c;--red-soft:#fee2e2;--purple:#6d28d9;--purple-soft:#ede9fe}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',-apple-system,sans-serif;background:var(--bg);color:var(--ink);font-size:14.5px;line-height:1.5;-webkit-font-smoothing:antialiased}
.wrap{max-width:880px;margin:0 auto;padding:0 20px 90px}

/* ── header ── */
.hdr{position:sticky;top:0;z-index:50;background:rgba(251,251,253,.85);backdrop-filter:saturate(180%) blur(16px);-webkit-backdrop-filter:saturate(180%) blur(16px);border-bottom:1px solid var(--line)}
.hdr-in{max-width:880px;margin:0 auto;padding:14px 20px;display:flex;align-items:center;gap:11px}
.mark{width:30px;height:30px;background:var(--ink);border-radius:8px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:14px;flex:none}
.hdr h1{font-size:16.5px;font-weight:700;letter-spacing:-.01em}
#saved{margin-left:auto;color:var(--green);font-size:12px;font-weight:600;opacity:0;transition:opacity .3s}

/* ── tabs ── */
.tabs{display:flex;gap:4px;margin:18px 0 20px;background:var(--bg2);border-radius:12px;padding:4px;width:max-content;max-width:100%}
.tab{border:none;background:transparent;border-radius:9px;padding:8px 18px;font:600 13.5px 'Inter';color:var(--ink2);cursor:pointer;display:flex;align-items:center;gap:7px;white-space:nowrap}
.tab.on{background:var(--card);color:var(--ink);box-shadow:0 1px 3px rgba(0,0,0,.08)}
.tab .n{background:var(--accent);color:#fff;font-size:10.5px;font-weight:700;border-radius:99px;padding:1px 7px;min-width:18px;text-align:center}
.tab:not(.on) .n{background:var(--line2);color:var(--ink2)}

/* ── werklijst ── */
.sectie{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--ink3);margin:18px 2px 8px}
.taak{display:flex;align-items:center;gap:14px;background:var(--card);border:1px solid var(--line);border-radius:13px;padding:13px 16px;margin-bottom:8px;transition:border-color .15s}
.taak:hover{border-color:var(--line2)}
.taak .ico{font-size:17px;flex:none;width:26px;text-align:center}
.taak .tx{flex:1;min-width:0}
.taak .tt{font-weight:600;font-size:14px}
.taak .nt{color:var(--ink3);font-size:12.5px;margin-top:1px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.taak .acts{display:flex;gap:8px;flex:none;align-items:center}
.btn{display:inline-flex;align-items:center;gap:5px;border:none;border-radius:99px;padding:8px 15px;font:600 12.5px 'Inter';cursor:pointer;text-decoration:none;background:var(--accent);color:#fff;white-space:nowrap}
.btn:hover{background:#0058ad}
.btn.gh{background:var(--bg2);color:var(--ink2)}
.btn.gh:hover{background:var(--line)}
.btn.kl{background:transparent;border:1.5px solid var(--line2);color:var(--ink3);width:32px;height:32px;border-radius:99px;padding:0;justify-content:center;font-size:14px}
.btn.kl:hover{border-color:var(--green);color:var(--green);background:var(--green-soft)}
.klaarlog{color:var(--ink3);font-size:12px;margin-top:14px;line-height:1.7}
.leeg{text-align:center;color:var(--ink3);padding:48px 0;font-size:14px}
.leeg b{display:block;font-size:30px;margin-bottom:8px}

/* ── leads ── */
.bar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:14px}
.chip{border:1px solid var(--line);background:var(--card);border-radius:99px;padding:6px 14px;font:600 12.5px 'Inter';color:var(--ink2);cursor:pointer}
.chip.on{background:var(--ink);color:#fff;border-color:var(--ink)}
#zoek{flex:1;min-width:150px;border:1px solid var(--line);border-radius:99px;padding:8px 16px;font:13.5px 'Inter';background:var(--card);outline:none}
#zoek:focus{border-color:var(--accent)}
.lead{background:var(--card);border:1px solid var(--line);border-radius:13px;margin-bottom:8px;overflow:hidden;transition:border-color .15s}
.lead:hover{border-color:var(--line2)}
.lhead{display:flex;align-items:center;gap:12px;padding:13px 16px;cursor:pointer;user-select:none}
.av{width:36px;height:36px;border-radius:99px;background:var(--bg2);color:var(--ink2);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;flex:none}
.av.nieuw{background:var(--accent-soft);color:var(--accent)}
.av.gewonnen,.av.beantwoord{background:var(--green-soft);color:var(--green)}
.av.in-gesprek,.av.offerte{background:var(--amber-soft);color:var(--amber)}
.av.verloren{background:var(--red-soft);color:var(--red)}
.lwie{flex:1;min-width:0}
.lnaam{font-weight:600;font-size:14px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lsub{color:var(--ink3);font-size:12.5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lmeta{display:flex;align-items:center;gap:8px;flex:none}
.badge{font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;padding:3px 9px;border-radius:99px;background:var(--bg2);color:var(--ink2);white-space:nowrap}
.badge.b-nieuw{background:var(--accent-soft);color:var(--accent)}
.badge.b-beantwoord,.badge.b-gewonnen{background:var(--green-soft);color:var(--green)}
.badge.b-in-gesprek,.badge.b-offerte{background:var(--amber-soft);color:var(--amber)}
.badge.b-verloren{background:var(--red-soft);color:var(--red)}
.badge.b-on-hold{background:var(--bg2);color:var(--ink3)}
.tijd{font-size:11.5px;color:var(--ink3);white-space:nowrap}
.pijl{color:var(--ink3);font-size:11px;transition:transform .2s}
.lead.open .pijl{transform:rotate(90deg)}
.lbody{display:none;padding:2px 16px 16px;border-top:1px solid var(--line)}
.lead.open .lbody{display:block}
.lrij{font-size:13px;color:var(--ink2);margin:9px 0 7px}
.lrij a{color:var(--accent);text-decoration:none;font-weight:600}
.msg{white-space:pre-wrap;font-size:13.5px;color:var(--ink2);background:var(--bg2);border-radius:10px;padding:11px 13px;margin:8px 0}
.supplier{background:var(--accent-soft);border:1px solid #cfe0f7;border-radius:10px;padding:10px 13px;margin:8px 0;font-size:13px}
.lacts{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:10px}
select,textarea,input{font:13px 'Inter';border:1px solid var(--line2);border-radius:9px;padding:7px 10px;background:var(--card);color:var(--ink);outline:none}
select:focus,textarea:focus,input:focus{border-color:var(--accent)}
textarea{width:100%;resize:vertical;margin-top:8px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0 8px}
@media(max-width:560px){.grid{grid-template-columns:1fr}.taak{flex-wrap:wrap}.taak .acts{margin-left:40px}}
#addpanel{display:none;background:var(--card);border:1px solid var(--line);border-radius:13px;padding:16px;margin-bottom:14px}
#addpanel.show{display:block}

/* ── verstuurd ── */
.out{display:flex;gap:12px;align-items:baseline;padding:11px 4px;border-bottom:1px solid var(--line);font-size:13px}
.out .t{color:var(--ink3);font-size:11.5px;flex:none;width:88px}
.out .a{font-weight:600;flex:none;max-width:240px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.out .s{color:var(--ink2);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
</style></head><body>
<div class="hdr"><div class="hdr-in"><div class="mark">B</div><h1>BotLease CRM</h1><span id="saved">opgeslagen ✓</span></div></div>
<div class="wrap">
<div class="tabs">
  <button class="tab on" id="tab-werk" onclick="toon('werk')">📋 Werklijst <span class="n" id="n-werk">0</span></button>
  <button class="tab" id="tab-leads" onclick="toon('leads')">👥 Leads <span class="n" id="n-leads">0</span></button>
  <button class="tab" id="tab-uit" onclick="toon('uit')">📤 Verstuurd <span class="n" id="n-uit">0</span></button>
</div>

<div id="v-werk"></div>

<div id="v-leads" style="display:none">
  <div class="bar" id="filters"></div>
  <div id="addpanel">
    <div class="grid">
      <input id="a-name" placeholder="Naam"><input id="a-company" placeholder="Bedrijf">
      <input id="a-email" placeholder="E-mail"><input id="a-subject" placeholder="Onderwerp">
    </div>
    <textarea id="a-message" rows="4" placeholder="Plak hier de mail of het bericht…"></textarea>
    <div class="lacts"><button class="btn" onclick="addLead()">Toevoegen</button></div>
  </div>
  <div id="list"></div>
</div>

<div id="v-uit" style="display:none"></div>
</div>
<script>
const KEY=new URLSearchParams(location.search).get('key')||'';
const STATUSES=__STATUSES__;const CANSEND=__CANSEND__;const SENDERS=__SENDERS__;
let LEADS=[],OUT=[],TASKS=[],FILTER='alles',ZOEK='',OPENID=null;
const flash=()=>{const s=document.getElementById('saved');s.style.opacity=1;setTimeout(()=>s.style.opacity=0,1400);};
const esc=s=>{const d=document.createElement('div');d.textContent=s||'';return d.innerHTML;};
async function api(p,body){const r=await fetch(p+(p.includes('?')?'&':'?')+'key='+encodeURIComponent(KEY),
 body?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}:{});
 if(!r.ok){document.querySelector('.wrap').insertAdjacentHTML('afterbegin','<div class="leeg">Geen toegang — open de volledige link mét ?key=…</div>');throw 0;}
 return r.json();}
function ago(iso){if(!iso)return'';const m=(Date.now()-new Date(iso))/60000;
 if(m<60)return Math.max(1,m|0)+'m';if(m<1440)return (m/60|0)+'u';const d=m/1440|0;return d===1?'1d':d+'d';}
function wanneer(iso){if(!iso)return'';const d=new Date(iso),m=['jan','feb','mrt','apr','mei','jun','jul','aug','sep','okt','nov','dec'];
 const z=n=>String(n).padStart(2,'0');return d.getDate()+' '+m[d.getMonth()]+' '+z(d.getHours())+':'+z(d.getMinutes());}
function toon(t){['werk','leads','uit'].forEach(x=>{document.getElementById('v-'+x).style.display=x===t?'':'none';
 document.getElementById('tab-'+x).classList.toggle('on',x===t);});}

/* ── werklijst ── */
function drawTasks(){
 const open=TASKS.filter(t=>t.status==='open'),done=TASKS.filter(t=>t.status==='klaar');
 document.getElementById('n-werk').textContent=open.length;
 const mails=open.filter(t=>t.mail_to).sort((a,b)=>(b.created||'').localeCompare(a.created||'')),acties=open.filter(t=>!t.mail_to);
 const el=document.getElementById('v-werk');el.innerHTML='';
 if(!open.length){el.innerHTML='<div class="leeg"><b>🎉</b>Alles afgewerkt — nieuwe taken verschijnen hier zodra er iets binnenkomt.</div>';}
 const rij=t=>{const ico=(t.title.match(/^\S+/)||['•'])[0];const tt=t.title.replace(/^\S+\s*/,'');
  if(!t.mail_to){return `<div class="taak"><div class="ico">${ico}</div><div class="tx"><div class="tt">${esc(tt)}</div>${t.note?`<div class="nt" title="${esc(t.note)}">${esc(t.note)}</div>`:''}</div><div class="acts"><span class="tijd">${wanneer(t.created)}</span><button class="btn kl" title="Markeer als klaar" onclick="taakKlaar(${t.id})">✓</button></div></div>`;}
  const lead=window.ALLLEADS?ALLLEADS.find(x=>x.id===t.lead_id):null;
  const isOpen=TOPEN===t.id;
  const mailto=`mailto:${encodeURIComponent(t.mail_to)}?bcc=verstuurd%40in.botlease.nl&subject=${encodeURIComponent(t.mail_subject)}&body=${encodeURIComponent(t.mail_body)}`;
  return `<div class="taak mailtaak ${isOpen?'open':''}" style="flex-direction:column;align-items:stretch;gap:0">
    <div style="display:flex;align-items:center;gap:14px;cursor:pointer" onclick="tklap(${t.id})">
      <div class="ico">${ico}</div>
      <div class="tx"><div class="tt">${esc(tt)}</div>${t.note?`<div class="nt" title="${esc(t.note)}">${esc(t.note)}</div>`:''}</div>
      <div class="acts"><span class="tijd">${wanneer(t.created)}</span><span style="font-size:11.5px;color:var(--ink3)">${isOpen?'sluiten':'bekijk mail'}</span><span class="pijl" style="${isOpen?'transform:rotate(90deg)':''}">▶</span></div>
    </div>
    ${isOpen?`<div style="border-top:1px solid var(--line);margin-top:12px;padding-top:12px">
      ${lead&&lead.message?`<div class="sectie" style="margin-top:2px">📥 Origineel bericht van ${esc(lead.name||lead.email)}</div><div class="msg" style="max-height:180px;overflow:auto">${esc(lead.message)}</div>`:''}
      <div class="sectie" style="margin-top:10px">📝 Concept-antwoord · aan ${esc(t.mail_to)} · onderwerp: ${esc(t.mail_subject)}</div>
      <div class="msg" style="max-height:none">${esc(t.mail_body)}</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px">
        <a class="btn" href="${mailto}">✉️ Open in mailprogramma</a>
        ${CANSEND?`<select id="snd${t.id}" style="border:1px solid var(--line2);border-radius:99px;padding:7px 10px;font:12.5px Inter">${SENDERS.map(s=>`<option value="${s}">vanaf ${s}</option>`).join('')}</select><button class="btn gh" onclick="verstuur(${t.id},this)">📨 Verstuur</button>`:''}
        <button class="btn gh" title="Kopieer netjes opgemaakt" onclick='richCopy(${JSON.stringify(t.mail_body)})'>📋 Kopieer</button>
        <button class="btn kl" title="Markeer als klaar" onclick="taakKlaar(${t.id})">✓</button>
      </div></div>`:''}
  </div>`;};
 if(mails.length){el.insertAdjacentHTML('beforeend','<div class="sectie">✉️ Mails versturen ('+mails.length+')</div>'+mails.map(rij).join(''));}
 if(acties.length){el.insertAdjacentHTML('beforeend','<div class="sectie">Acties ('+acties.length+')</div>'+acties.map(rij).join(''));}
 if(done.length){el.insertAdjacentHTML('beforeend',`<div class="klaarlog">✓ Afgerond (${done.length}): ${done.slice(-6).map(t=>esc(t.title.replace(/^\S+\s*/,''))).join(' · ')}</div>`);}
}
let TOPEN=null;
function tklap(id){TOPEN=TOPEN===id?null:id;drawTasks();}
async function verstuur(id,btn){const t=TASKS.find(x=>x.id===id);
 const sel=document.getElementById('snd'+id);const from=sel?sel.value:'';
 if(!confirm('Versturen naar '+t.mail_to+(from?' vanaf '+from:'')+'?'))return;
 btn.disabled=true;btn.textContent='Versturen…';
 try{await api('api/send',{id:id,from:from});flash();t.status='klaar';drawTasks();}
 catch(e){btn.disabled=false;btn.textContent='📨 Verstuur';alert('Versturen mislukt — gebruik de ✉️-knop.');}}
function richCopy(body){
 const html=body.split(/\n\n+/).map(p=>'<p style="margin:0 0 12px;font-family:Calibri,Arial,sans-serif;font-size:11pt">'+p.replace(/\n/g,'<br>')+'</p>').join('');
 const item=new ClipboardItem({'text/html':new Blob([html],{type:'text/html'}),'text/plain':new Blob([body],{type:'text/plain'})});
 navigator.clipboard.write([item]).then(()=>flash());}
async function taakKlaar(id){await api('api/task-update',{id:id,status:'klaar'});flash();TASKS.find(t=>t.id===id).status='klaar';drawTasks();}

/* ── leads ── */
function filters(){const f=[['alles','Alle'],['nieuw','Nieuw'],['open','Open'],['gewonnen','Gewonnen']];
 document.getElementById('filters').innerHTML=f.map(([k,l])=>`<button class="chip ${FILTER===k?'on':''}" onclick="FILTER='${k}';drawLeads()">${l}</button>`).join('')+
 `<input id="zoek" placeholder="Zoeken…" value="${esc(ZOEK)}" oninput="ZOEK=this.value;drawLeads(true)">`+
 `<button class="chip" onclick="document.getElementById('addpanel').classList.toggle('show')">＋ Toevoegen</button>`;}
function visible(l){if(FILTER==='nieuw'&&l.status!=='nieuw')return false;
 if(FILTER==='open'&&!['nieuw','in gesprek','offerte'].includes(l.status))return false;
 if(FILTER==='gewonnen'&&l.status!=='gewonnen')return false;
 if(ZOEK){const h=(l.name+' '+l.company+' '+l.email+' '+l.subject+' '+l.message).toLowerCase();
  if(!h.includes(ZOEK.toLowerCase()))return false;}return true;}
let timers={};
function drawLeads(keepFocus){
 document.getElementById('n-leads').textContent=LEADS.filter(l=>l.status==='nieuw').length||LEADS.length;
 if(!keepFocus)filters();
 const el=document.getElementById('list');el.innerHTML='';
 const rows=LEADS.filter(visible);
 if(!rows.length){el.innerHTML='<div class="leeg"><b>📭</b>Geen leads in deze weergave.</div>';return;}
 rows.forEach(l=>{
  const ini=(l.name||'?').replace(/[^A-Za-z0-9 ]/g,'').split(' ').map(w=>w[0]).join('').slice(0,2).toUpperCase()||'?';
  const st=l.status.replace(/ /g,'-');
  const isOrder=(l.subject||'').includes('BESTELLING')||!!l.sourcing;
  const d=document.createElement('div');d.className='lead'+(OPENID===l.id?' open':'');
  d.innerHTML=`<div class="lhead" onclick="klap(${l.id})">
    <div class="av ${st}">${ini}</div>
    <div class="lwie"><div class="lnaam">${esc(l.name)||'(geen naam)'}${l.company?' · '+esc(l.company):''}</div>
    <div class="lsub">${esc(l.subject||l.email||'')}</div></div>
    <div class="lmeta">${isOrder?'<span class="badge" style="background:var(--amber-soft);color:var(--amber)">bestelling</span>':''}<span class="badge b-${st}">${esc(l.status)}</span><span class="tijd">${ago(l.created)}</span><span class="pijl">▶</span></div></div>
   <div class="lbody">
    <div class="lrij">${l.email?`<a href="mailto:${esc(l.email)}">${esc(l.email)}</a>`:''} ${l.phone?' · '+esc(l.phone):''} ${l.robot?' · '+esc(l.robot):''}</div>
    ${l.message?`<div class="msg">${esc(l.message)}</div>`:''}
    ${l.sourcing?`<div class="supplier">📦 <b>Bestellen bij:</b> ${esc(l.sourcing)}</div>`:''}
    <div class="lacts">
      <select data-id="${l.id}" class="st">${STATUSES.map(s=>`<option ${s===l.status?'selected':''}>${s}</option>`).join('')}</select>
      ${l.email?`<a class="btn gh" href="mailto:${esc(l.email)}?bcc=verstuurd%40in.botlease.nl&subject=${encodeURIComponent('Re: uw aanvraag bij BotLease')}">✉️ Beantwoorden</a>`:''}
    </div>
    <textarea class="nt-edit" data-id="${l.id}" rows="2" placeholder="Notities / opvolging…">${esc(l.notes)}</textarea>
   </div>`;
  el.appendChild(d);});
 el.querySelectorAll('select.st').forEach(s=>s.onchange=async e=>{
  await api('api/update',{id:+e.target.dataset.id,status:e.target.value});
  LEADS.find(x=>x.id==e.target.dataset.id).status=e.target.value;flash();drawLeads();});
 el.querySelectorAll('textarea.nt-edit').forEach(t=>t.oninput=e=>{clearTimeout(timers[e.target.dataset.id]);
  timers[e.target.dataset.id]=setTimeout(async()=>{await api('api/update',{id:+e.target.dataset.id,notes:e.target.value});flash();},500);});}
function klap(id){OPENID=OPENID===id?null:id;drawLeads();}
async function addLead(){const v=id=>document.getElementById(id).value;
 await api('api/add',{name:v('a-name'),company:v('a-company'),email:v('a-email'),subject:v('a-subject'),message:v('a-message'),source:'handmatig'});
 ['a-name','a-company','a-email','a-subject','a-message'].forEach(i=>document.getElementById(i).value='');
 document.getElementById('addpanel').classList.remove('show');flash();load();}

/* ── verstuurd ── */
function drawOut(){document.getElementById('n-uit').textContent=OUT.length;
 const el=document.getElementById('v-uit');
 el.innerHTML=OUT.length?OUT.map(o=>`<div class="out"><span class="t">${(o.created||'').slice(5,16).replace('T',' ')}</span><span class="a">${esc((o.name||'').replace(/^AAN: /,''))}</span><span class="s">${esc(o.subject)}</span></div>`).join('')
  :'<div class="leeg"><b>📤</b>Nog geen gelogde uitgaande mails — zet verstuurd@in.botlease.nl in je BCC.</div>';}

async function load(){
 const all=await api('api/leads');
 OUT=all.filter(l=>l.source==='uitgaand');window.ALLLEADS=all;
 LEADS=all.filter(l=>l.source!=='uitgaand');
 TASKS=await api('api/tasks');
 drawTasks();drawLeads();drawOut();}
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
                return self._send(401, "<h3>401 - open de volledige link met ?key=...</h3>".encode(), "text/html; charset=utf-8")
            return self._send(200, PAGE.replace("__STATUSES__", json.dumps(STATUSES)).replace("__SENDERS__", json.dumps(list(smtp_accounts().keys()))).replace("__CANSEND__", "true" if smtp_accounts() else "false").encode(), "text/html; charset=utf-8")
        if path == "/api/leads":
            if not self._authed(q):
                return self._send(401, {"error": "unauthorized"})
            with db() as con:
                rows = [dict(r) for r in con.execute(
                    "SELECT * FROM leads ORDER BY CASE status WHEN 'nieuw' THEN 0 ELSE 1 END, id DESC")]
            return self._send(200, rows)
        if path == "/api/tasks":
            if not self._authed(q):
                return self._send(401, {"error": "unauthorized"})
            with db() as con:
                rows = [dict(r) for r in con.execute(
                    "SELECT * FROM tasks ORDER BY CASE status WHEN 'open' THEN 0 ELSE 1 END, id ASC")]
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
        _secret_ok = WEBHOOK_SECRET and self.headers.get("X-CRM-Secret", "") == WEBHOOK_SECRET
        if not (self._authed(q) or _secret_ok):
            return self._send(401, {"error": "unauthorized"})
        if path == "/api/task":  # taak toevoegen (Claude zet hier werk klaar)
            with db() as con:
                cur = con.execute(
                    "INSERT INTO tasks (created, updated, title, note, mail_to, mail_subject, mail_body, status, lead_id)"
                    " VALUES (?,?,?,?,?,?,?,?,?)",
                    (now(), now(), str(d.get("title") or "")[:300], str(d.get("note") or "")[:2000],
                     str(d.get("mail_to") or "")[:200], str(d.get("mail_subject") or "")[:300],
                     str(d.get("mail_body") or "")[:8000], "open",
                     d.get("lead_id") if isinstance(d.get("lead_id"), int) else 0))
            return self._send(200, {"ok": True, "id": cur.lastrowid})
        if path == "/api/send":  # direct versturen vanuit de werklijst (user klikt)
            accs = smtp_accounts()
            if not accs:
                return self._send(400, {"error": "SMTP niet geconfigureerd"})
            if not isinstance(d.get("id"), int):
                return self._send(400, {"error": "geen id"})
            sender = d.get("from") if d.get("from") in accs else next(iter(accs))
            with db() as con:
                task = con.execute("SELECT * FROM tasks WHERE id=?", (d["id"],)).fetchone()
            if not task or not task["mail_to"]:
                return self._send(404, {"error": "taak niet gevonden of geen mail"})
            try:
                msg = EmailMessage()
                disp = "Thomas Vedder" if sender.startswith("thomas@") else "Thomas Vedder | BotLease"
                msg["From"] = f"{disp} <{sender}>"
                msg["To"] = task["mail_to"]
                msg["Bcc"] = "verstuurd@in.botlease.nl"
                msg["Subject"] = task["mail_subject"]
                body = task["mail_body"].rstrip()
                if "+31 6 2369 2944" not in body:  # handtekening alleen toevoegen als-ie ontbreekt
                    body += f"\n\nThomas Vedder\nOprichter, BotLease\n+31 6 2369 2944 | {sender}\nwww.botlease.nl"
                msg.set_content(body)
                with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=25) as s:
                    s.starttls()
                    s.login(sender, accs[sender])
                    s.send_message(msg)
            except Exception as e:
                return self._send(502, {"error": f"versturen mislukt: {str(e)[:160]}"})
            with db() as con:
                con.execute("UPDATE tasks SET status='klaar', updated=? WHERE id=?", (now(), d["id"]))
                con.execute(
                    "INSERT INTO leads (created, updated, source, name, company, email, phone,"
                    " subject, message, status, notes) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (now(), now(), "uitgaand", f"AAN: {task['mail_to']}", "", task["mail_to"], "",
                     task["mail_subject"], task["mail_body"][:2000], "beantwoord",
                     "Direct verstuurd vanuit het CRM"))
            return self._send(200, {"ok": True})
        if path == "/api/task-update":
            if d.get("status") in ("open", "klaar") and isinstance(d.get("id"), int):
                with db() as con:
                    con.execute("UPDATE tasks SET status=?, updated=? WHERE id=?", (d["status"], now(), d["id"]))
                return self._send(200, {"ok": True})
            return self._send(400, {"error": "geen velden"})
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
