#!/usr/bin/env python3
"""
Voeg een nieuwe rank-check toe aan seo/seo_data.json.

Twee modes:

  # Interactief — wordt voor elk keyword gevraagd
  python3 scripts/seo_add_check.py

  # Bulk vanaf CLI — voor één keyword
  python3 scripts/seo_add_check.py --kw humanoide-robot-leasen-nl --pos 12

Vandaag's datum wordt automatisch ingevuld. Als er al een check is voor vandaag,
wordt die uitgebreid in plaats van een nieuwe aangemaakt.
"""
from __future__ import annotations
import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "seo" / "seo_data.json"


def load():
    with DATA.open() as f:
        return json.load(f)


def save(d):
    with DATA.open("w") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)


def today_check(data, method="manual"):
    today = date.today().isoformat()
    for c in data.setdefault("checks", []):
        if c.get("date") == today:
            return c
    new = {"date": today, "method": method, "notes": "", "ranks": {}}
    data["checks"].append(new)
    return new


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--kw", help="keyword-id uit seo_data.json (bijv. unitree-g1-leasen-nl)")
    p.add_argument("--pos", type=int, help="huidige Google-positie (0 = niet in top 30)")
    p.add_argument("--method", default="manual", help="bron van data (manual, gsc, serpapi, websearch)")
    p.add_argument("--note", default="", help="optionele aantekening")
    args = p.parse_args()

    data = load()
    kw_index = {kw["id"]: kw for kw in data["target_keywords"]}

    check = today_check(data, method=args.method)
    if args.note:
        check["notes"] = (check.get("notes", "") + " " + args.note).strip()

    if args.kw and args.pos is not None:
        if args.kw not in kw_index:
            print(f"❌ Onbekend keyword-id: {args.kw}")
            print(f"   Beschikbaar: {', '.join(sorted(kw_index.keys()))}")
            sys.exit(1)
        check["ranks"][args.kw] = {"position": args.pos}
        save(data)
        print(f"✅ {args.kw} = #{args.pos} toegevoegd aan {check['date']}")
        return

    # Interactieve mode
    print(f"\nVoeg rank-data toe voor {check['date']}.")
    print(f"  Per keyword: typ positie (1-30) of 0 voor 'niet in top 30'. Leeg laten = overslaan.\n")
    for kw in data["target_keywords"]:
        existing = check["ranks"].get(kw["id"], {})
        cur = existing.get("position", "") if isinstance(existing, dict) else ""
        prompt = f"  [{kw['priority']}] {kw['kw']:50}"
        if cur != "":
            prompt += f" (vorig: #{cur})"
        val = input(prompt + ": ").strip()
        if not val:
            continue
        try:
            check["ranks"][kw["id"]] = {"position": int(val)}
        except ValueError:
            print(f"     ⚠ Niet geldig, overgeslagen.")

    save(data)
    print(f"\n✅ Opgeslagen in {DATA.relative_to(ROOT)}")
    print(f"   Run: python3 scripts/build_seo_dashboard.py  → om dashboard te verversen")


if __name__ == "__main__":
    main()
