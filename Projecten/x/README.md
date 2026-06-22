# PROJECT X — AI-marketingbureau in een doos

Een herbruikbaar, grotendeels geautomatiseerd systeem dat per klant-bedrijf zes dingen doet:
**domeinonderzoek → marketingsite → SEO/GEO → blogs → leads afvangen/beantwoorden/kwalificeren → gekwalificeerde leads doorzetten.**
Eén keer bouwen, dan per nieuwe klant "een script runnen". Azure-first (draait in de eigen omgeving van de klant), AVG-compliant.
Eerste klant: via Tijmen (IT Connect, Almelo). Bouwt voort op de bouwstenen die Thomas al maakte voor BotLease.

## Leesvolgorde

1. **[00-BLUEPRINT.md](00-BLUEPRINT.md)** — start hier. Visie, de 6 stappen, high-level Azure-architectuur, het "1 script per klant"-model, fasen, kosten, risico's + AVG.
2. **[01-client-intake.md](01-client-intake.md)** — intake-naslagwerk (het "waarom" per vraag) + de open beslissingen die het ontwerp bepalen (deploy-model A/B, hardheid EU-eis, CRM, budget). Voor het invullen: gebruik **[INTAKE-FORMULIER.md](INTAKE-FORMULIER.md)** (compact, invulbaar, blockers gemarkeerd) — dit stuur je naar Tijmen/de klant.
3. **[02-architecture.md](02-architecture.md)** — gedetailleerde Azure-architectuur: diensten, auth (keyless/Managed Identity), netwerk, data-residentie, per-tenant isolatie, dataflow per stap, en het rapportage-/meet-component (§6b).
4. **[03-build-plan.md](03-build-plan.md)** — bouwfasen van MVP naar volledig, met deliverables per fase en het onboarding-script-stappenplan.
5. **[04-data-needed.md](04-data-needed.md)** — afvinkbare checklist: alles wat Tijmen/de klant moet aanleveren + accounts/keys + te nemen beslissingen (met [BLOCKER MVP]-tags).
6. **[05-meten-en-succes.md](05-meten-en-succes.md)** — hoe we SEO/GEO-succes meten: de funnel van leading→lagging, north-star = gekwalificeerde leads, GEO-citatie eerlijk meten.

## Werkende onderdelen (geen concept meer)

- **[onboard.py](onboard.py)** — het echte, deterministische "1 script per klant": leest een `client-config.json` en genereert een complete gethematiseerde site + sitemap.xml + robots.txt + llms.txt. Bewezen op twee verschillende bedrijven (warmtepomp-installateur + advocatenkantoor).
  ```
  python3 onboard.py --config demo/client-config.json --out /tmp/klant-site
  ```
- **[client-config.template.json](client-config.template.json)** — het per-klant config-schema dat het script consumeert.
- **[demo/](demo/)** — een complete end-to-end testrun voor een fictief bedrijf (Twentse Warmte, Almelo): zie **[demo/DEMO-RESULT.md](demo/DEMO-RESULT.md)**. Bevat de gegenereerde site (`demo/site/`), een blogartikel, en de volledige lead-flow (capture → AI-reply → BANT-kwalificatie → routing met human-in-the-loop) in `demo/leads/`.

## Status (22 juni 2026)

- **Blauwdruk + research:** compleet (00-05), web-gegrond.
- **Lokale proof:** de pipeline is end-to-end gesimuleerd (demo/) en het config→site-script (onboard.py) werkt deterministisch op meerdere bedrijven.
- **Nog niet gebouwd:** de Azure-kant (Foundry-agents, Functions, Cosmos, ACS) — dat is Fase 1 uit het build-plan.
- **Volgende stap:** de 2 kernbeslissingen + blocker-items uit `04-data-needed.md` met Tijmen ophalen (vooral: deploy-model en hardheid EU-eis). Daarna Fase 1 (MVP) bouwen.

## Belangrijke kanttekeningen

- **Eerlijk, geen overpromise** (zelfde lijn als BotLease): GEO/AI-citatie is geen gegarandeerde positie; content + lead-doorzet hebben bewuste mens-in-de-lus-gates.
- **Azure/Foundry verandert snel:** prijzen en features per kwartaal verifiëren op de live pricing-pagina's vóór een offerte.
- Doelgroep van deze docs: Thomas (bouwer) + Tijmen (klant-contact).
