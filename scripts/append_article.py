#!/usr/bin/env python3
"""
Append a new article dict to scripts/articles_data.py.

Reads the article from stdin as JSON. Format expected:
{
  "slug": "...", "title": "...", "subtitle": "...",
  "category": "...", "date": "YYYY-MM-DD", "reading_time": 7,
  "intro": "...",
  "body": [["h2","..."],["p","..."],...],
  "sources": [["Name","URL"],...],
  "tags": ["..."]
}
Idempotent: dedupes by slug. If slug exists, exits 0 without changes.
"""
import json
import sys
import re
import ast
from pathlib import Path
from datetime import date

DATA = Path(__file__).resolve().parent / "articles_data.py"

def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print("ERROR: no JSON on stdin", file=sys.stderr); sys.exit(2)

    # Strip optional ```json fences
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
    if m: raw = m.group(1)

    art = json.loads(raw)

    # Body/sources arrived as list-of-lists; convert to tuples for python file
    art["body"] = [tuple(item) for item in art["body"]]
    art["sources"] = [tuple(item) for item in art.get("sources", [])]
    art.setdefault("author", "BotLease Redactie")
    art.setdefault("reading_time", 6)
    art.setdefault("date", date.today().isoformat())

    text = DATA.read_text(encoding="utf-8")

    # Dedup by slug
    if f'"slug": "{art["slug"]}"' in text or f"'slug': '{art['slug']}'" in text:
        print(f"[skip] slug '{art['slug']}' already exists")
        return

    # Python source for new dict (use repr for safety)
    def py_repr(x, indent=8):
        ind = " " * indent
        if isinstance(x, dict):
            inner = ",\n".join(f"{ind}    {repr(k)}: {py_repr(v, indent+4)}" for k, v in x.items())
            return "{\n" + inner + "\n" + ind + "}"
        if isinstance(x, list):
            return "[\n" + ",\n".join(f"{ind}    {py_repr(v, indent+4)}" for v in x) + "\n" + ind + "]"
        if isinstance(x, tuple):
            return "(" + ", ".join(py_repr(v, indent) for v in x) + ")"
        return repr(x)

    new_entry = "    " + py_repr(art, indent=4) + ",\n"

    # Insert before the closing "]" of ARTICLES list
    new_text = re.sub(r"(\n\])\s*\Z", new_entry + r"\1", text, flags=re.DOTALL)
    if new_text == text:
        print("ERROR: could not find ARTICLES list terminator", file=sys.stderr)
        sys.exit(3)

    DATA.write_text(new_text, encoding="utf-8")
    print(f"[ok] appended article: {art['slug']}")

if __name__ == "__main__":
    main()
