#!/usr/bin/env python3
"""BotLease mail-catcher — ontvangt mail voor in.botlease.nl en zet die in het CRM.

Werking: Hostnet stuurt hallo@botlease.nl door naar inbox@in.botlease.nl (naast
Hotmail). De MX van in.botlease.nl wijst naar deze VPS; dit script draait een
minimale SMTP-server op poort 25 en schrijft elke mail als lead (source='mail')
in /root/botlease-crm/crm.db — zelfde database als het CRM-dashboard.

Systemd: botlease-mail.service. Geen relay (alleen ontvangen, nooit doorsturen).
"""
import email
import email.policy
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from aiosmtpd.controller import Controller

DB = Path("/root/botlease-crm/crm.db")
MAX_BYTES = 5_000_000


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def text_from(msg) -> str:
    """Beste leesbare tekst uit een (multipart) mail."""
    try:
        part = msg.get_body(preferencelist=("plain", "html"))
        if part is None:
            return ""
        body = part.get_content()
        if part.get_content_type() == "text/html":
            body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", body, flags=re.S | re.I)
            body = re.sub(r"<[^>]+>", " ", body)
            body = re.sub(r"\s+", " ", body)
        return body.strip()[:8000]
    except Exception:
        return "(kon mail-inhoud niet parsen)"


class CRMHandler:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        # alleen post voor ons eigen capture-domein — weert relay-probes en scanner-spam
        if not address.lower().endswith("@in.botlease.nl"):
            return "550 not relaying to that domain"
        envelope.rcpt_tos.append(address)
        return "250 OK"

    async def handle_DATA(self, server, session, envelope):
        try:
            if len(envelope.content) > MAX_BYTES:
                return "552 Message too large"
            # BCC-logboek: stuurt Thomas een mail met BCC naar verstuurd@in.botlease.nl,
            # dan loggen we die als uitgaande mail (geen nieuwe lead).
            is_outgoing = any(r.lower().startswith("verstuurd@") for r in envelope.rcpt_tos)
            msg = email.message_from_bytes(envelope.content, policy=email.policy.default)
            frm = str(msg.get("From", envelope.mail_from or ""))[:300]
            m = re.search(r"<([^>]+)>", frm)
            from_email = (m.group(1) if m else frm).strip()[:200]
            from_name = re.sub(r"<[^>]*>", "", frm).strip(' "')[:200] or from_email
            subject = str(msg.get("Subject", ""))[:300]
            body = text_from(msg)
            to_hdr = str(msg.get("To", ""))[:200]
            with sqlite3.connect(DB) as con:
                if is_outgoing:
                    con.execute(
                        "INSERT INTO leads (created, updated, source, name, company, email, phone,"
                        " subject, message, status, notes) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                        (now(), now(), "uitgaand", f"AAN: {to_hdr}", "", to_hdr, "",
                         subject, body[:2000], "beantwoord", "Automatisch gelogd via BCC verstuurd@in.botlease.nl"))
                    # taak afvinken als deze mail bij een open taak hoort:
                    # 1) exacte adres-match; 2) anders domein-match, maar alleen als
                    #    er precies één open taak op dat domein wacht (tickets/aliassen).
                    con.execute("UPDATE tasks SET status='klaar', updated=? WHERE status='open'"
                                " AND mail_to != '' AND instr(lower(?), lower(mail_to)) > 0",
                                (now(), to_hdr))
                    doms = set(re.findall(r"@([a-z0-9.-]+\.[a-z]{2,})", to_hdr.lower()))
                    for dom in doms:
                        open_dom = con.execute(
                            "SELECT id FROM tasks WHERE status='open' AND lower(mail_to) LIKE ?",
                            (f"%@{dom}",)).fetchall()
                        if len(open_dom) == 1:
                            con.execute("UPDATE tasks SET status='klaar', updated=? WHERE id=?",
                                        (now(), open_dom[0][0]))
                else:
                    con.execute(
                        "INSERT INTO leads (created, updated, source, name, company, email, phone,"
                        " subject, message, status, notes) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                        (now(), now(), "mail", from_name, "", from_email, "",
                         subject, body, "nieuw", ""))
            print(f"[mail] lead opgeslagen van {from_email}: {subject[:60]}")
            return "250 Message accepted for delivery"
        except Exception as e:
            print(f"[mail] FOUT: {e}")
            return "451 Temporary failure"


if __name__ == "__main__":
    controller = Controller(CRMHandler(), hostname="0.0.0.0", port=25)
    controller.start()
    print("BotLease mail-catcher op :25 (in.botlease.nl)")
    import time
    while True:
        time.sleep(3600)
