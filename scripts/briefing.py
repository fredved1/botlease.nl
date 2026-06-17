#!/usr/bin/env python3
"""BotLease ochtendbriefing — de eerste actie van elke Claude-sessie.
Draait op de VPS: poldert beide mailboxen en toont nieuwe mail, open taken, op wie we wachten.
Gebruik: ssh root@185.107.90.42 'python3 /root/botlease-crm/briefing.py'
"""
import sqlite3, subprocess, sys
from datetime import datetime

DB = "/root/botlease-crm/crm.db"

# 1) verse mail ophalen
try:
    subprocess.run([sys.executable, "/root/botlease-crm/imap_poller.py"],
                   capture_output=True, timeout=120)
except Exception:
    pass

con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
print("\n========== BOTLEASE OCHTENDBRIEFING ==========")
print(datetime.now().strftime("%A %d %B %Y, %H:%M"))
print("🎯 DOEL: eerste betaalde deal (VR Expert) + goedkope inkooplijn tegen reseller-prijs (wij bezitten de klant). Nooit voorschieten.")

# laatste dagelijkse controle-uitkomst tonen
try:
    import os
    log="/root/botlease-crm/controle-laatste.log"
    if os.path.exists(log):
        lines=[l for l in open(log).read().splitlines() if "probleem" in l]
        mtime=datetime.fromtimestamp(os.path.getmtime(log)).strftime("%d %b %H:%M")
        if lines:
            status=lines[-1].strip("= ").strip()
            ok = status.startswith("0")
            print(f"\n[controle {mtime}] {'✅ alles klopt' if ok else '🔴 LET OP — ' + status}")
except Exception:
    pass

# 2) nieuwe inkomende mail (status nieuw)
nieuw = con.execute("SELECT created,name,email,subject FROM leads WHERE status='nieuw' AND source='mail' ORDER BY id DESC").fetchall()
print(f"\n--- NIEUWE MAIL ({len(nieuw)}) ---")
for r in nieuw:
    print(f"  {r['created'][:16]} | {(r['name'] or r['email'])[:30]:30} | {(r['subject'] or '')[:44]}")
if not nieuw: print("  (geen nieuwe inkomende mail)")

# 3) open mail-taken (klaar om te versturen)
taken = con.execute("SELECT title FROM tasks WHERE status='open' AND mail_to!='' ORDER BY id").fetchall()
print(f"\n--- KLAAR OM TE VERSTUREN ({len(taken)}) ---")
for r in taken: print(f"  - {r['title'][:70]}")
if not taken: print("  (geen mails klaarstaand)")

# 4) actieve gesprekken — op wie wachten we
print("\n--- ACTIEVE GESPREKKEN (in gesprek / offerte) ---")
for r in con.execute("SELECT name,company,subject FROM leads WHERE status IN ('in gesprek','offerte') AND source IN ('mail','formulier') ORDER BY company"):
    wie = (r['company'] or r['name'] or '')[:26]
    print(f"  {wie:26} | {(r['subject'] or '')[:46]}")

# 5) overige acties (niet-mail taken)
acties = con.execute("SELECT title FROM tasks WHERE status='open' AND mail_to='' ORDER BY id").fetchall()
if acties:
    print(f"\n--- OVERIGE ACTIES ({len(acties)}) ---")
    for r in acties: print(f"  - {r['title'][:70]}")

print("\nVolgende: lees docs/handboek/02-stand-van-zaken.md voor de laatste updates.")
print("==============================================\n")
