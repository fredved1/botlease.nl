# botlease.nl

Statische site voor **BotLease B.V.** — operational lease, verhuur en verkoop van humanoïde robots (NL/EU).

## Structuur
| Map | Wat |
|---|---|
| `frontend/` | de site (webroot op Vercel, project **botlease-v2**) — 85+ pagina's, `frontend/vercel.json` is de actieve config |
| `scripts/` | generators (`build_robots/news/guides/landingpages.py` + `style_base.py`/`seo_common.py`), news-bot, CRM/mail-catcher (draaien op VPS), OG-beeld-generator |
| `docs/` | businessplan v2, concurrentie/haalbaarheid, verkoopdocs (`docs/archief/` = oude versies) |
| `OUTREACH/` | leveranciers-tracker, één-klik-mailpagina's, GEO-offsite-plan |
| `seo/` | keyword-targets + wekelijkse snapshots (analytics/rank-bots) |
| `archive/` | oud chatbot-tijdperk (vóór de humanoid-pivot) — niet meer in gebruik |

## Deployen
Push naar master deployt **niet** automatisch. Vanaf een schone checkout:
```
git worktree add --detach /tmp/bl origin/master && cp -r .vercel /tmp/bl/.vercel
cd /tmp/bl && vercel --prod --yes
```

## ⚠️ Belangrijk vóór je rebuildt
~57 pagina's bevatten een hand-geïnjecteerde `#mobile-first-patch` (hamburgermenu) die de generators **niet** produceren. Nieuws (`frontend/nieuws/`) is wél veilig te rebuilden; al het andere: generator aanpassen én live HTML in-place patchen. Prijzen: bron = `scripts/robots_data.py` (canon v2, €290–€6.650).

## Backend (VPS 185.107.90.42)
- **CRM**: `https://crm.botlease.nl/?key=…` (systemd `botlease-crm`, SQLite) — alle aanvragen/bestellingen/mails als leads
- **Mail-capture**: `botlease-mail` (SMTP :25, `in.botlease.nl`) → CRM
- News-bot: wekelijks (cron-afronding pending)
