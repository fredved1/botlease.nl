# 06 — Techniek & infrastructuur

## De website
- **`frontend/`** = de site (statische HTML), webroot op Vercel-project **botlease-v2**. `docs/` wordt NIET publiek geserveerd (interne docs veilig).
- **Generators:** `scripts/build_robots.py`, `build_news.py`, `build_guides.py`, `build_landingpages.py` + `style_base.py`/`seo_common.py`; data in `robots_data.py`, `articles_data.py`, `guides_data.py`, `landingpages_data.py`.
- **⚠️ Mobile-patch-regel (belangrijkste valkuil):** ~55 live pagina's hebben een hand-geïnjecteerd `<style id="mobile-first-patch">` (hamburgermenu) dat de generators NIET emitten. **Die pagina's nooit rebuilden** (sloopt de patch) → in-place editen. `frontend/nieuws/` is wél veilig te rebuilden. Check vóór een edit: `grep -c mobile-first-patch <bestand>`.
- **Prijzen:** bron = `scripts/robots_data.py`. Bij prijswijziging: site-brede sweep + eindscan tot 0 leftovers (zie `docs/` pricing-historie).

## Deployen (push deployt NIET vanzelf)
```
git push origin master
WT=/tmp/bl-deployNN; git worktree add --detach "$WT" origin/master && cp -r .vercel "$WT/.vercel"
cd "$WT" && vercel --prod --yes
cd - && git worktree remove "$WT" --force && git worktree prune
```
Daarna live-verifiëren met `curl -sL https://botlease.nl/...`.

## VPS (185.107.90.42) — CRM + mail
SSH met root-key werkt. Draait: nginx (crm.botlease.nl, api.heymilo.nl), de CRM, het mailsysteem, en losstaande hyperliquid-trading-bots (**NIET aanraken — echt geld**).

### CRM
- **Code:** `scripts/crm_server.py` (repo) → `/root/botlease-crm/crm_server.py`, systemd **botlease-crm**, 127.0.0.1:8788, SQLite `/root/botlease-crm/crm.db`.
- **Dashboard:** `https://crm.botlease.nl/?key=<CRM_ACCESS_KEY>` (key staat in `/root/botlease-crm/env` + mijn privé-geheugen, NIET in de repo).
- **Werklijst (tasks-tabel):** ik zet concept-mails klaar; Thomas checkt + verstuurt. Per mail kiest hij afzender (hallo@ of thomas@). Versturen via de CRM = echte threaded reply met geciteerde historie + kopie in de Verzonden-map.

### Mail (volledig IMAP, geen doorstuur-omweg meer)
- **`scripts/imap_poller.py`** → systemd-timer **botlease-imap** (elke 10 min): leest INBOX + Verzonden-map van **hallo@ én thomas@** rechtstreeks. Inkomend → lead (status nieuw). Uitgaand → log. Filtert ruis (no-reply/nieuwsbrieven/KvK).
- **Versturen** via `/api/send` (CRM): SMTP smtp.hostnet.nl:587, plakt handtekening, zet kopie in Verzonden-map, threadt via opgeslagen Message-ID.
- **Persona's (sinds 7/7):** afzender hallo@ = **"Lisa | BotLease"** met handtekening "Lisa, Sales & Planning"; afzender thomas@ = "Thomas Vedder, Oprichter". Override per mail: `{"as":"thomas"}` of `{"as":"lisa"}` in de /api/send-payload. **Niet mid-thread van identiteit wisselen** (lopende leveranciersthreads waar Thomas de afzender is → thomas@ of as=thomas). Thomas haalt de handtekening uit zijn eigen mailprogramma zodat die niet dubbel/strijdig plakt.
- **Wachtwoorden:** in `/root/botlease-crm/env` (`CRM_SMTP_PASS` = hallo@, thomas@ in `CRM_IMAP_ACCOUNTS`). Nooit in de repo.

### Draft-bot (UIT)
`scripts/draft_bot.py` schrijft automatisch concepten via Claude Code op de VPS — **staat op verzoek uit** (Thomas wil dat ik het via de terminal doe op "update mijn crm"). Heraanzetten: `systemctl enable --now botlease-draft.timer`.

### Dagelijks automatisch (zelf-controlerend systeem)
- **Mail-poller** (botlease-imap.timer): elke 10 min → altijd de laatste berichten in het CRM.
- **Dagelijkse controle** (botlease-controle.timer, 07:30): draait controle.py → logt naar /root/botlease-crm/controle-laatste.log.
- De **ochtendbriefing toont de laatste controle-status** bovenaan (✅ alles klopt / 🔴 let op).

### Ochtendbriefing
`ssh root@185.107.90.42 'python3 /root/botlease-crm/briefing.py'` → toont nieuwe mail, open taken, op wie we wachten. **Eerste actie elke sessie.**

## Werkwijze "update mijn crm" / "check inbox"
1. Poller draaien (`python3 /root/botlease-crm/imap_poller.py`) of briefing.
2. Nieuwe leads lezen, dubbelingen opruimen, statussen bijwerken.
3. Per actiepunt een concept-antwoord (mét volle context, threaded) als taak klaarzetten.
4. `docs/handboek/02-stand-van-zaken.md` + `03-pipeline.md` bijwerken.
5. Kort rapporteren wat er klaarstaat.

## ⚠️ Mail-catcher UIT (18/6) — poller dekt alles
De oude `mail_catcher` (botlease-mail, SMTP :25 via in.botlease.nl-forward) is **uitgezet** — de IMAP-poller leest nu inbound (INBOX) én outbound (Verzonden-map) rechtstreeks, dus de catcher was puur een bron van **dubbele leads zonder msgid**. Niet heraanzetten. (Heraanzetten zou weer no-msgid-duplicaten geven.)

## ⚠️ NOOIT zelf leads INSERTEN voor inkomende mail
De poller importeert élke inkomende mail al (met msgid). Maak je er handmatig óók een aan, dan krijg je een synthetische duplicaat die niet aan de echte mail-thread hangt (gebeurd 18/6: synthetische UBTECH/RobotShop-leads → reply hing aan de verkeerde). **Werkwijze:** zoek de bestaande poller-lead op (op afzender/msgid), UPDATE die (status/notes), en koppel de reply daaraan. Alleen handmatig INSERTEN voor leads die NIET via mail binnenkomen (bv. telefonisch/WhatsApp).

## ⚠️ Mail dedupliceren — alleen op Message-ID
**NOOIT dubbele mails opruimen op afzender+onderwerp.** In een doorlopend gesprek heeft elke reply hetzelfde "Re: …"-onderwerp; groeperen op email+subject verwijdert dan échte vervolgmails (gebeurd 17/6: Seans 2e UBTECH-mail met de Richard-introductie werd zo per ongeluk gewist, daarna hersteld uit de inbox). **Alleen ontdubbelen op exact identiek Message-ID** = letterlijk dezelfde mail. De inbox (IMAP) is altijd de bron-van-waarheid; een per ongeluk gewiste lead is terug te halen uit de inbox met msgid. **Bij twijfel: dubbelcheck tegen de inbox** (Thomas' staande instructie).

## Valkuilen / classifier
- Bulk-mail autonoom versturen wordt door de veiligheidsfilter geblokkeerd (terecht) → losse sends of Thomas klikt. Replies in lopende gesprekken mogen na zijn ok.
- nginx reload/restart + git reset --hard op de VPS worden geblokkeerd → Thomas draait die zelf via `!`.
- Geen secrets greppen/in de repo zetten.
