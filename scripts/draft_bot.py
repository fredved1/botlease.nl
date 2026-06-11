#!/usr/bin/env python3
"""BotLease draft-bot — schrijft automatisch concept-antwoorden voor nieuwe leads.

Draait elke 15 min (systemd timer) op de VPS. Werkwijze:
1. Pak nieuwe inkomende leads (mail/formulier, status 'nieuw', nog geen concept).
2. Genereer per lead een concept-antwoord via OpenRouter (playbook in draft_prompt.md).
3. Zet het als taak in de CRM-werklijst — Thomas checkt en verstuurt zelf.
VERSTUURT NOOIT ZELF. Alleen concepten.

LLM: Claude Code CLI (`claude -p`, abonnement) — geen API-kosten. DB: crm.db (kolom leads.drafted).
Log: journalctl -u botlease-draft
"""
import json
import os
import sqlite3
import subprocess
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
DB = BASE / "crm.db"
PROMPT_FILE = BASE / "draft_prompt.md"
CLAUDE_BIN = os.environ.get("CLAUDE_BIN", "/usr/local/bin/claude")
MODEL = os.environ.get("DRAFT_MODEL", "sonnet")
MAX_PER_RUN = 5


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def log(m: str) -> None:
    print(f"[draft-bot] {m}", flush=True)


def llm(system: str, user: str) -> dict | None:
    prompt = f"{system}\n\n=== INKOMENDE LEAD ===\n{user}"
    try:
        r = subprocess.run(
            [CLAUDE_BIN, "-p", prompt, "--model", MODEL],
            capture_output=True, text=True, timeout=300,
            env={**os.environ, "HOME": "/root"})
        raw = (r.stdout or "").strip()
        if not raw:
            log(f"LLM-fout: lege output ({(r.stderr or '')[:120]})")
            return None
        if raw.startswith("```"):
            raw = raw.strip("`").lstrip("json").strip()
        # pak het eerste {...}-blok voor het geval er tekst omheen staat
        i, j = raw.find("{"), raw.rfind("}")
        if i == -1 or j == -1:
            log(f"LLM-fout: geen JSON in output: {raw[:120]}")
            return None
        d = json.loads(raw[i:j + 1])
        if not isinstance(d, dict) or ("subject" not in d and not d.get("skip")):
            return None
        return d
    except Exception as e:
        log(f"LLM-fout: {str(e)[:160]}")
        return None


def main() -> int:
    system = PROMPT_FILE.read_text(encoding="utf-8")
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    try:
        con.execute("ALTER TABLE leads ADD COLUMN drafted INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    leads = con.execute(
        "SELECT * FROM leads WHERE drafted=0 AND status='nieuw'"
        " AND source IN ('mail','formulier') AND email != '' ORDER BY id ASC LIMIT ?",
        (MAX_PER_RUN,)).fetchall()
    if not leads:
        log("niets te doen.")
        return 0
    for l in leads:
        info = (f"NIEUWE LEAD (#{l['id']}, bron: {l['source']}, {l['created']})\n"
                f"Naam: {l['name']}\nBedrijf: {l['company']}\nE-mail: {l['email']}\n"
                f"Telefoon: {l['phone']}\nOnderwerp: {l['subject']}\n"
                f"Robot: {l['robot']}\nLeverancier-info: {l['sourcing']}\n\n"
                f"BERICHT:\n{l['message'][:4000]}")
        d = llm(system, info)
        if d is None:
            log(f"lead #{l['id']}: geen concept (LLM-fout) — volgende run opnieuw.")
            continue
        if d.get("skip"):
            con.execute("UPDATE leads SET drafted=1 WHERE id=?", (l["id"],))
            con.commit()
            log(f"lead #{l['id']}: overgeslagen ({d.get('reason','spam/niet-relevant')})")
            continue
        title = f"✉️ Antwoord: {l['name'] or l['email']}" + (f" ({l['company']})" if l["company"] else "")
        note = d.get("note", "Automatisch concept — lees vóór verzenden even na.")
        con.execute(
            "INSERT INTO tasks (created, updated, title, note, mail_to, mail_subject, mail_body, status, lead_id)"
            " VALUES (?,?,?,?,?,?,?,?,?)",
            (now(), now(), title[:300], f"[concept door AI] {note}"[:2000],
             l["email"][:200], str(d.get("subject", ""))[:300], str(d.get("body", ""))[:8000], "open", l["id"]))
        con.execute("UPDATE leads SET drafted=1 WHERE id=?", (l["id"],))
        con.commit()
        log(f"lead #{l['id']}: concept klaargezet → taak '{title[:60]}'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
