#!/usr/bin/env python3
"""BotLease IMAP poller — leest de mailbox(en) rechtstreeks en zet nieuwe zakelijke mail als lead in het CRM.

Vervangt de kwetsbare doorstuur-omweg (hallo@ -> forward -> in.botlease.nl -> SMTP-catcher).
Leest READ-ONLY: raakt de mailbox van Thomas nooit aan (geen vlaggen, niks verplaatst/verwijderd).

- Accounts via CRM_IMAP_ACCOUNTS="adres:wachtwoord,adres2:wachtwoord2" (fallback CRM_SMTP_USER/PASS).
- Eerste run per account = baseline: registreert de huidige hoogste UID, importeert GEEN historie.
- Daarna: alleen nieuwe mail boven die UID, ruis (no-reply/nieuwsbrieven/orders-via-webhook) eruit gefilterd.
- Draait via systemd-timer (botlease-imap.timer). Log: journalctl -u botlease-imap

Inkomende leads krijgen status 'nieuw', drafted=0 -> verschijnen in het CRM; ik schrijf de concepten
wanneer Thomas "update mijn CRM" zegt (de auto-draft-bot staat op zijn verzoek uit).
"""
import email
import imaplib
import os
import re
import sqlite3
from email.header import decode_header, make_header
from email.utils import parseaddr
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
DB = BASE / "crm.db"
HOST = os.environ.get("CRM_IMAP_HOST", "imap.hostnet.nl")
PORT = int(os.environ.get("CRM_IMAP_PORT", "993"))

# Afzenders die GEEN lead worden (automatisch/ruis/al-via-webhook-in-CRM):
SKIP_PATTERNS = [
    "no-reply", "noreply", "donotreply", "do-not-reply", "mailer-daemon", "postmaster",
    "onboarding@resend", "updates.resend", "zeno@", "zeno.rocha", "@updates.",
    "messaging.metamail", "newsletter", "notifications@", "@kvk.nl", "euipo.europa.eu",
    "news@neura-robotics",
]


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def log(m: str) -> None:
    print(f"[imap-poller] {m}", flush=True)


def hdr(v: str) -> str:
    try:
        return str(make_header(decode_header(v or "")))
    except Exception:
        return v or ""


def body_text(msg) -> str:
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition", "")):
                try:
                    return part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", "replace")
                except Exception:
                    pass
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                try:
                    html = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", "replace")
                    return re.sub(r"<[^>]+>", " ", html)
                except Exception:
                    pass
        return ""
    try:
        return msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", "replace")
    except Exception:
        return ""


def accounts():
    raw = os.environ.get("CRM_IMAP_ACCOUNTS", "").strip()
    if raw:
        out = []
        for pair in raw.split(","):
            if ":" in pair:
                u, p = pair.split(":", 1)
                out.append((u.strip(), p.strip()))
        return out
    u = os.environ.get("CRM_SMTP_USER", "")
    p = os.environ.get("CRM_SMTP_PASS", "")
    return [(u, p)] if u and p else []


SENT_FOLDER = os.environ.get("CRM_SENT_FOLDER", "INBOX/Verzonden items")


def poll(con, user, pw, folder, mode):
    """mode 'in' = INBOX -> leads (status nieuw); mode 'out' = Verzonden -> log (source uitgaand).
    READ-ONLY: raakt de mailbox nooit aan. Baseline op de eerste run per (account, map)."""
    M = imaplib.IMAP4_SSL(HOST, PORT)
    M.login(user, pw)
    typ, _ = M.select(f'"{folder}"', readonly=True)
    if typ != "OK":
        M.logout()
        return 0
    typ, st = M.status(f'"{folder}"', "(UIDVALIDITY)")
    uv = re.search(rb"UIDVALIDITY (\d+)", st[0]).group(1).decode()
    typ, d = M.uid("search", None, "ALL")
    uids = sorted(int(x) for x in d[0].split())
    tag = f"{user}|{folder}"
    k_uv, k_last = f"uidvalidity_{tag}", f"last_uid_{tag}"
    row_uv = con.execute("SELECT v FROM imap_state WHERE k=?", (k_uv,)).fetchone()
    if not uids:
        # lege map: baseline op 0, zodat de EERSTE toekomstige mail wél wordt opgepakt
        if row_uv is None:
            con.execute("INSERT OR REPLACE INTO imap_state VALUES (?,?)", (k_uv, uv))
            con.execute("INSERT OR REPLACE INTO imap_state VALUES (?,?)", (k_last, "0"))
            con.commit()
        M.logout()
        return 0
    max_uid = max(uids)
    if row_uv is None or row_uv[0] != uv:
        con.execute("INSERT OR REPLACE INTO imap_state VALUES (?,?)", (k_uv, uv))
        # Verzonden-map die voor het eerst verschijnt: laat de laatste paar sends alsnog
        # binnenkomen (zodat de allereerste mail uit thomas@ ook gelogd wordt), maar cap
        # op 5 zodat een volle historie nooit in één keer geïmporteerd wordt.
        if mode == "out":
            baseline = uids[-6] if len(uids) > 5 else 0
        else:
            baseline = max_uid
        con.execute("INSERT OR REPLACE INTO imap_state VALUES (?,?)", (k_last, str(baseline)))
        con.commit()
        log(f"{tag}: baseline op UID {baseline} (was nieuw)")
        M.logout()
        return 0
    last_uid = int(con.execute("SELECT v FROM imap_state WHERE k=?", (k_last,)).fetchone()[0])
    count = 0
    for u in [x for x in uids if x > last_uid]:
        typ, md = M.uid("fetch", str(u), "(RFC822)")
        if not md or not md[0]:
            continue
        msg = email.message_from_bytes(md[0][1])
        subj = hdr(msg.get("Subject", ""))
        mid = "".join((msg.get("Message-ID", "") or "").split())[:300]
        if mid and con.execute("SELECT 1 FROM leads WHERE notes LIKE ?", (f"%{mid}%",)).fetchone():
            continue
        if mode == "out":
            to = hdr(msg.get("To", ""))
            _, to_addr = parseaddr(to)
            # dubbele log voorkomen (CRM-Verstuurknop / BCC-catcher schreven 'm al)
            if con.execute("SELECT 1 FROM leads WHERE source='uitgaand' AND email=? AND subject=? AND created > datetime('now','-2 day')",
                           (to_addr, subj)).fetchone():
                continue
            con.execute(
                "INSERT INTO leads (created,updated,source,name,company,email,phone,subject,message,status,notes,drafted)"
                " VALUES (?,?,?,?,?,?,?,?,?,?,?,1)",
                (now(), now(), "uitgaand", f"AAN: {to or to_addr}", "", to_addr, "",
                 subj, body_text(msg)[:2000], "beantwoord", f"via IMAP Verzonden {mid}"))
            count += 1
        else:
            frm = hdr(msg.get("From", ""))
            name, addr = parseaddr(frm)
            if any(p in addr.lower() or p in frm.lower() for p in SKIP_PATTERNS):
                continue
            try:
                con.execute(
                    "INSERT INTO leads (created,updated,source,name,company,email,phone,subject,message,status,notes,drafted,msgid)"
                    " VALUES (?,?,?,?,?,?,?,?,?,?,?,0,?)",
                    (now(), now(), "mail", name or addr, "", addr, "", subj, body_text(msg)[:8000],
                     "nieuw", f"via IMAP {user} {mid}", mid))
            except sqlite3.OperationalError:
                con.execute(
                    "INSERT INTO leads (created,updated,source,name,company,email,phone,subject,message,status,notes,drafted)"
                    " VALUES (?,?,?,?,?,?,?,?,?,?,?,0)",
                    (now(), now(), "mail", name or addr, "", addr, "", subj, body_text(msg)[:8000],
                     "nieuw", f"via IMAP {user} {mid}"))
            count += 1
    con.execute("INSERT OR REPLACE INTO imap_state VALUES (?,?)", (k_last, str(max_uid)))
    con.commit()
    M.logout()
    if count:
        log(f"{tag}: {count} {'uitgaand gelogd' if mode == 'out' else 'nieuwe lead(s)'}, last_uid={max_uid}")
    return count


def main() -> int:
    accs = accounts()
    if not accs:
        log("geen accounts geconfigureerd — stop.")
        return 0
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS imap_state (k TEXT PRIMARY KEY, v TEXT)")
    total = 0
    for user, pw in accs:
        for folder, mode in (("INBOX", "in"), (SENT_FOLDER, "out")):
            try:
                total += poll(con, user, pw, folder, mode)
            except Exception as e:
                log(f"{user}|{folder}: fout {repr(e)[:160]}")
    log(f"klaar — {total} nieuw verwerkt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
