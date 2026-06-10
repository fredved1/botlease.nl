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
    async def handle_DATA(self, server, session, envelope):
        try:
            if len(envelope.content) > MAX_BYTES:
                return "552 Message too large"
            msg = email.message_from_bytes(envelope.content, policy=email.policy.default)
            frm = str(msg.get("From", envelope.mail_from or ""))[:300]
            m = re.search(r"<([^>]+)>", frm)
            from_email = (m.group(1) if m else frm).strip()[:200]
            from_name = re.sub(r"<[^>]*>", "", frm).strip(' "')[:200] or from_email
            subject = str(msg.get("Subject", ""))[:300]
            body = text_from(msg)
            with sqlite3.connect(DB) as con:
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
