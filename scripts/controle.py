#!/usr/bin/env python3
"""BotLease controle — automatisch vangnet + volledig inzicht.
Draai dit om zeker te weten dat er niks misgaat/mist. Gebruik:
  ssh root@185.107.90.42 'python3 /root/botlease-crm/controle.py'
Checkt: (1) elke zakelijke inbox-mail heeft een CRM-lead (geen verloren mail),
(2) geen dubbele leads, (3) open reply-taken hangen aan de JUISTE mail.
"""
import imaplib, os, sqlite3, subprocess, sys
from email.utils import parseaddr
from email.header import decode_header, make_header

DB="/root/botlease-crm/crm.db"
SKIP=("no-reply","noreply","donotreply","mailer-daemon","postmaster","kvk.nl",
      "resend","metamail","euipo","news@neura-robotics","notifications@","unitree.cc")
# automatische/waardeloze onderwerpen (ticket-acks, routing, surveys)
SKIP_SUBJ=("request received","how would you rate","rate the support","my colleague")
def hdr(v):
    try: return str(make_header(decode_header(v or "")))
    except: return v or ""

# verse mail
try: subprocess.run([sys.executable,"/root/botlease-crm/imap_poller.py"],capture_output=True,timeout=120)
except Exception: pass

con=sqlite3.connect(DB); con.row_factory=sqlite3.Row
problemen=0

# 1) INBOX vs CRM — geen verloren mail
M=imaplib.IMAP4_SSL("imap.hostnet.nl",993); M.login("hallo@botlease.nl",os.environ.get("CRM_SMTP_PASS",""))
M.select("INBOX",readonly=True)
typ,d=M.uid("search",None,"ALL")
inbox=[]
for u in d[0].split():
    typ,md=M.uid("fetch",u,"(BODY.PEEK[HEADER.FIELDS (MESSAGE-ID FROM SUBJECT DATE)])")
    raw=md[0][1].decode("utf-8","replace"); mid=frm=subj=date=""
    for line in raw.split("\n"):
        ll=line.lower()
        if ll.startswith("message-id:"): mid="".join(line.split(":",1)[1].split())
        elif ll.startswith("from:"): frm=hdr(line[5:].strip())
        elif ll.startswith("subject:"): subj=hdr(line[8:].strip())
        elif ll.startswith("date:"): date=line[5:].strip()[:16]
    name,addr=parseaddr(frm)
    if any(s in addr.lower() for s in SKIP): continue
    inbox.append((mid,date,addr,subj))
M.logout()

# CRM: alle msgids + (email,subject)-paren
crm_mids=set(); crm_emails=set()
for r in con.execute("SELECT msgid,notes,email FROM leads"):
    if r["msgid"]: crm_mids.add(r["msgid"])
    if r["notes"]:
        for tok in r["notes"].split():
            if tok.startswith("<") and tok.endswith(">"): crm_mids.add(tok)
    if r["email"]: crm_emails.add(r["email"].lower())

print("\n========== BOTLEASE CONTROLE ==========")
print("\n[1] MAIL-DEKKING (inbox vs CRM):")
echt_verloren=0
for mid,date,addr,subj in inbox:
    if any(s in subj.lower() for s in SKIP_SUBJ): continue   # auto/waardeloos
    if mid and mid in crm_mids: continue                      # exact gekoppeld = ok
    bekend = addr.lower() in crm_emails
    if bekend:
        continue  # contact loopt al in CRM (mail valt onder bestaand gesprek)
    echt_verloren+=1; problemen+=1
    print(f"   🔴 NIEUW CONTACT niet in CRM: {date} | {addr[:30]} | {subj[:38]}")
if not echt_verloren: print("   ✅ geen verloren mail — elke zakelijke afzender staat in het CRM")

# 2) dubbele leads (zelfde msgid)
print("\n[2] DUBBELE LEADS (zelfde Message-ID):")
dups=con.execute("SELECT msgid,COUNT(*) n FROM leads WHERE msgid!='' GROUP BY msgid HAVING n>1").fetchall()
if dups:
    for r in dups: problemen+=1; print(f"   ⚠️ {r['n']}× {r['msgid'][:50]}")
else: print("   ✅ geen dubbele leads")

# 3) open reply-taken: hangen ze aan de juiste mail?
print("\n[3] OPEN REPLY-TAKEN (controleer threading):")
for r in con.execute("SELECT t.title,t.mail_to,t.lead_id,l.subject,l.email,l.created FROM tasks t LEFT JOIN leads l ON l.id=t.lead_id WHERE t.status='open' AND t.mail_to!='' ORDER BY t.id"):
    flags=[]
    if not r["lead_id"] or not r["subject"]:
        flags.append("GEEN MAIL GEKOPPELD")
    # nieuwere mail van zelfde afzender? (= reply hangt aan oude mail)
    if r["email"] and r["created"]:
        newer=con.execute("SELECT COUNT(*) FROM leads WHERE email=? AND source='mail' AND created>?",(r["email"],r["created"])).fetchone()[0]
        if newer: flags.append(f"ER IS {newer} NIEUWERE MAIL van deze afzender")
    # ontvanger wijkt af van wie mailde (Reply-To kan legitiem zijn → 'info')
    if r["email"] and r["mail_to"] and r["email"].lower()!=r["mail_to"].lower():
        flags.append(f"ontvanger {r['mail_to']} != afzender {r['email']}")
    link=f"→ reply op mail van {(r['created'] or '?')[:10]}: {(r['subject'] or '-')[:34]}"
    mark = ("  🔴 "+" | ".join(flags)) if any('NIEUWERE' in f or 'GEKOPPELD' in f for f in flags) else ("  ⚠️ "+" | ".join(flags) if flags else "")
    if any('NIEUWERE' in f or 'GEKOPPELD' in f for f in flags): problemen+=1
    print(f"   {r['title'][:46]:46} {link}{mark}")

print(f"\n========== {problemen} probleem(en) gevonden ==========\n")
