#!/usr/bin/env python3
"""BotLease outreach tracker — klein lokaal server-app.
Bewerk in de browser (http://localhost:8787), elke wijziging gaat direct naar schijf
(tracker_data.json = data, tracker.md = leesbaar overzicht). Browser sluiten mag.
Stoppen: Ctrl+C of sluit het proces. Opnieuw starten: python3 OUTREACH/tracker_server.py
"""
import json
import socketserver
import http.server
import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "tracker_data.json"
MD = BASE / "tracker.md"
PORT = 8791


def today():
    try:
        return datetime.date.today().strftime("%-d-%-m-%Y")
    except Exception:
        return "5-6-2026"


def seed():
    t = today()
    fab = [
        ("PAL Robotics", "business@pal-robotics.com"),
        ("Pollen Robotics", "sales@pollen-robotics.com"),
        ("EngineAI", "sales@engineai.com.cn"),
        ("UBTECH", "sales@ubtrobot.com"),
        ("Unitree", "sales_global@unitree.com"),
        ("NEURA Robotics", "info@neura-robotics.com"),
        ("1X Technologies", "press@1x.tech"),
    ]
    dis = [
        ("Terra Robotics", "mail@terra-robotics.de"),
        ("Generation Robots", "contact@generationrobots.com"),
        ("QUADRUPED / MyBotShop", "info@quadruped.de"),
        ("Synergy Tech (Unitree ES)", "info@synergytech.es"),
        ("RoboCorpus", "jordi.hurssel@robocorpus.be"),
        ("INGEN Innovations", "services@ingen-geosciences.com"),
        ("Leobotics", "contact@leobotics.fr"),
        ("RobotShop Europe", "marketplace@robotshop.com"),
        ("OrcaRobot (UBTECH EU/NL)", "richard@orcarobot.com"),
    ]
    frm = [
        ("Apptronik", "apptronik.com/contact-us"),
        ("Agility Robotics", "agilityrobotics.com/sales"),
        ("Figure AI", "figure.ai/company"),
        ("INNOV8 Group", "innov8.fr/contact-us"),
    ]
    suppliers = []
    for pfx, grp, rows in [("fab", "Fabrikanten", fab),
                           ("dis", "EU-distributeurs", dis),
                           ("frm", "Alleen via formulier", frm)]:
        for i, (n, c) in enumerate(rows):
            suppliers.append({"id": f"{pfx}{i}", "name": n, "contact": c,
                              "group": grp, "status": "Gemaild", "date": t, "note": ""})
    return {
        "leads": [{"id": "lead0",
                   "name": "Atlas Copco Airpower (humanoid taskforce)",
                   "status": "Holdmail te sturen", "date": t,
                   "note": "Wacht op leverancier + specialist voor het echte gesprek"}],
        "suppliers": suppliers,
    }


def write_md(data):
    L = ["# BotLease — outreach tracker", "", f"_Laatst bijgewerkt: {today()}_", "",
         "## Inkomende leads", "", "| Bedrijf | Status | Datum | Notitie |", "|---|---|---|---|"]
    for r in data.get("leads", []):
        L.append(f"| {r['name']} | {r['status']} | {r.get('date','')} | {r.get('note','')} |")
    L += ["", "## Leveranciers & distributeurs", ""]
    grp = None
    for r in data.get("suppliers", []):
        if r["group"] != grp:
            grp = r["group"]
            L += ["", f"### {grp}", "| Bedrijf | Contact | Status | Gemaild op | Notitie |",
                  "|---|---|---|---|---|"]
        L.append(f"| {r['name']} | {r['contact']} | {r['status']} | {r.get('date','')} | {r.get('note','')} |")
    MD.write_text("\n".join(L) + "\n", encoding="utf-8")


def load():
    if DATA.exists():
        return json.loads(DATA.read_text(encoding="utf-8"))
    d = seed()
    store(d)
    return d


def store(data):
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    write_md(data)


PAGE = r'''<!DOCTYPE html><html lang="nl"><head><meta charset="utf-8"><title>BotLease — tracker</title>
<style>
body{font-family:-apple-system,Inter,Arial,sans-serif;max-width:1000px;margin:24px auto;padding:0 18px;color:#1d1d1f;line-height:1.4}
h1{font-size:23px;margin-bottom:4px}h2{font-size:13px;text-transform:uppercase;letter-spacing:.05em;color:#6e6e73;margin:24px 0 6px}
.note{background:#f5f5f7;border-radius:10px;padding:13px 15px;font-size:13px;color:#424245}
#sum{font-size:14px;font-weight:600;margin:14px 0 4px;padding:10px 14px;background:#eef3fb;border-radius:9px;color:#0a3d7a}
#saved{font-size:13px;color:#1d8a3f;opacity:0;transition:opacity .3s;margin-left:10px}
table{border-collapse:collapse;width:100%;margin:4px 0}
td,th{text-align:left;padding:6px 9px;border-bottom:1px solid #ececf0;font-size:13.5px}
th{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:#86868b}
tr.grp td{background:#fafafa;font-weight:700;font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:#6e6e73}
code{font-size:12.5px;color:#5a5a5f}
select,input{font:13px -apple-system,Inter,Arial,sans-serif;padding:5px 7px;border:1px solid #d2d2d7;border-radius:7px;background:#fff;color:#1d1d1f}
</style></head><body>
<h1>BotLease — outreach tracker<span id="saved">opgeslagen op schijf &#10003;</span></h1>
<div class="note">Bewerk hier; <b>elke wijziging wordt meteen op schijf opgeslagen</b> (tracker_data.json + tracker.md). De browser sluiten mag, het blijft staan. Laat dit programma draaien zolang je werkt.</div>
<div id="sum"></div>
<h2>Inkomende leads</h2>
<table id="leads"><thead><tr><th>Bedrijf</th><th>Status</th><th>Datum</th><th>Notitie</th></tr></thead><tbody></tbody></table>
<h2>Leveranciers &amp; distributeurs</h2>
<table id="suppliers"><thead><tr><th>Bedrijf</th><th>Contact</th><th>Status</th><th>Gemaild op</th><th>Notitie</th></tr></thead><tbody></tbody></table>
<script>
var SUP=['Gemaild','Antwoord ontvangen','In gesprek','Geen reactie','Afgehaakt'];
var LEAD=['Holdmail te sturen','Holdmail verstuurd','Gesprek gepland','On hold','Afgehaakt'];
var DATA={leads:[],suppliers:[]};
function sel(opts,val,on){var s=document.createElement('select');opts.forEach(function(o){var op=document.createElement('option');op.textContent=o;if(o===val)op.selected=true;s.appendChild(op);});s.onchange=on;return s;}
function inp(val,on,ph){var i=document.createElement('input');i.value=val||'';if(ph)i.placeholder=ph;i.oninput=on;return i;}
function td(child){var t=document.createElement('td');if(typeof child==='string')t.innerHTML=child;else t.appendChild(child);return t;}
function render(){
  var lb=document.querySelector('#leads tbody');lb.innerHTML='';
  DATA.leads.forEach(function(r){var tr=document.createElement('tr');
    tr.appendChild(td('<b>'+r.name+'</b>'));
    tr.appendChild(td(sel(LEAD,r.status,function(e){r.status=e.target.value;save();})));
    tr.appendChild(td(inp(r.date,function(e){r.date=e.target.value;save();})));
    var ni=inp(r.note,function(e){r.note=e.target.value;save();},'notitie...');ni.style.width='100%';
    tr.appendChild(td(ni));lb.appendChild(tr);});
  var sb=document.querySelector('#suppliers tbody');sb.innerHTML='';var grp='';
  DATA.suppliers.forEach(function(r){
    if(r.group!==grp){grp=r.group;var g=document.createElement('tr');g.className='grp';var gc=td(grp);gc.colSpan=5;g.appendChild(gc);sb.appendChild(g);}
    var tr=document.createElement('tr');
    tr.appendChild(td('<b>'+r.name+'</b>'));
    tr.appendChild(td('<code>'+r.contact+'</code>'));
    tr.appendChild(td(sel(SUP,r.status,function(e){r.status=e.target.value;save();})));
    tr.appendChild(td(inp(r.date,function(e){r.date=e.target.value;save();})));
    var ni=inp(r.note,function(e){r.note=e.target.value;save();},'notitie...');ni.style.width='100%';
    tr.appendChild(td(ni));sb.appendChild(tr);});
  summary();
}
function summary(){var a=0,g=0,n=0;DATA.suppliers.forEach(function(r){if(r.status==='Antwoord ontvangen')a++;else if(r.status==='In gesprek')g++;else if(r.status==='Geen reactie')n++;});
  document.getElementById('sum').textContent=DATA.suppliers.length+' leveranciers benaderd  ·  '+a+' antwoord  ·  '+g+' in gesprek  ·  '+n+' geen reactie';}
var tmr=null;
function save(){summary();clearTimeout(tmr);tmr=setTimeout(function(){
  fetch('/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(DATA)})
   .then(function(r){return r.json();}).then(function(){var s=document.getElementById('saved');s.style.opacity=1;setTimeout(function(){s.style.opacity=0;},1200);});
},300);}
fetch('/data').then(function(r){return r.json();}).then(function(d){DATA=d;render();});
</script>
</body></html>'''


class Handler(http.server.BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/index"):
            self._send(200, PAGE.encode("utf-8"), "text/html; charset=utf-8")
        elif self.path == "/data":
            self._send(200, json.dumps(load(), ensure_ascii=False).encode("utf-8"))
        else:
            self._send(404, b"not found", "text/plain")

    def do_POST(self):
        if self.path == "/save":
            n = int(self.headers.get("Content-Length", 0))
            try:
                data = json.loads(self.rfile.read(n))
                store(data)
                self._send(200, b'{"ok":true}')
            except Exception as e:
                self._send(400, json.dumps({"ok": False, "err": str(e)}).encode("utf-8"))
        else:
            self._send(404, b"not found", "text/plain")

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    load()  # seed on first run
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"BotLease tracker draait op http://localhost:{PORT}  (Ctrl+C om te stoppen)")
        httpd.serve_forever()
