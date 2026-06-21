# 01 — Overzicht: wat is BotLease

## In het kort
BotLease verhuurt, least en verkoopt **humanoïde robots** aan Nederlandse en EU-organisaties. We zijn geen fabrikant — we kopen in bij gevestigde producenten (Unitree, NEURA, UBTECH, Apptronik, Figure, e.a.) en regelen alles eromheen: levering, installatie, training, onderhoud, swap-SLA, verzekering en het EU-compliance-pad. Onafhankelijk, dus we adviseren welk merk past in plaats van er één te pushen.

## Bedrijf
- **Naam/rechtsvorm:** BotLease — eenmanszaak van Thomas Vedder. **Geen B.V.** (oprichten staat gepland vóór het eerste getekende lease-/verhuurcontract i.v.m. privé-aansprakelijkheid).
- **KvK:** 95943420 · **Vestiging:** Amsterdam · **Contact:** hallo@botlease.nl (zakelijk loket) + thomas@botlease.nl (persoonlijk).
- **Oprichter:** Thomas Vedder (achtergrond: AI/conversational, innovatiemanager bij UWV; doet BotLease ernaast). Geen robotica-achtergrond. Zie `04-team.md`.

## Het aanbod — drie vormen op dezelfde inkooplijn
1. **Event-verhuur** (per dag, incl. operator) — `/robot-huren-evenement`. Unitree R1 €750/dag (€495 dagdeel), G1 €1.450/dag (€950 dagdeel), −30% vanaf dag 2.
2. **Maandhuur** (flexibel, per maand opzegbaar) — `/huren`. R1 €690/mnd, G1 €2.450/mnd, overige op aanvraag.
3. **Operational lease** (36 mnd, all-in, laagste maandlast) — `/gids/humanoide-robot-leasen`. €290–€6.650/mnd.

Positionering nu (juni 2026): **lease is de hoofdboodschap op de site, verhuur subtiel als tweede optie.** Op robotpagina's kiest de klant in het bestelformulier de vorm en de prijs past live aan.

## Catalogus
**13 modellen** (prijscanon staat in `frontend/robots_data.py` en in `05-businessplan.md`). PAL Robotics is verwijderd op juridisch verzoek — nooit terugplaatsen.

## Fase / strategie (kort)
De markt is nog vroeg (Gartner: <20 bedrijven wereldwijd op productieschaal vóór 2028). Daarom: **verhuur/events als eerste omzet → pilots → lease later**. Het advies-pad is broker/commissie + event-verhuur als motor, niet meteen een grote lease-vloot op eigen kapitaal. Volledige strategie + kill-criteria in `05-businessplan.md`.

## Waar alles staat (snelkaart)
- **De site:** `frontend/` (statische HTML, webroot op Vercel).
- **Generators:** `scripts/build_*.py` + `*_data.py` (let op mobile-patch-regel, zie `06-techniek.md`).
- **CRM + mail:** VPS 185.107.90.42, dashboard `https://crm.botlease.nl/?key=…` (zie `06-techniek.md`).
- **Plannen/analyses:** `OUTREACH/businessplan-volledig.html` (volledig plan, enige bron), `OUTREACH/overzicht-ton.html` (status voor Ton), `docs/concurrentie-haalbaarheid-2026-06.md`, `docs/leveranciers/`.
- **Outreach-tooling:** `OUTREACH/` (tracker + één-klik-mailpagina's).
