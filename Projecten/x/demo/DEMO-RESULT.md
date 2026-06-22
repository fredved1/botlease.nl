# PROJECT X — Demo-verslag (lokale end-to-end testrun)

> **Eén regel:** de complete PROJECT X-pipeline (6 stappen) is lokaal doorlopen voor een fictief testbedrijf en levert tastbare, productie-realistische artefacten op: een valide website van 12 pagina's met schema, een feitcheck-bewust blogartikel, en een volledige lead-afhandeling van afvangen tot doorzetten met menselijke gate.

---

## 1. Wat is dit?

Dit is het verslag van een **lokale end-to-end testrun** van PROJECT X, het herbruikbare "AI-marketingbureau in een doos" (volledige blauwdruk in [`../00-BLUEPRINT.md`](../00-BLUEPRINT.md)). Het doel was aantonen dat de hele pipeline werkt en daarbij echte, bruikbare artefacten produceren.

- **Testbedrijf:** **Twentse Warmte** — een **volledig FICTIEF** verwarmingsinstallateur uit Almelo (regio Twente), gespecialiseerd in warmtepompen, hybride warmtepompen, zonneboilers, cv-vervanging en ISDE-subsidie + gratis warmtescan. Bedrijf, KvK (90000001), adres, eigenaar (Bram Oude Wesselink) en lead (Marleen Brinkhuis) zijn verzonnen.
- **Lokaal, niet op Azure.** Er zijn geen echte API-calls gedaan. Domein-beschikbaarheid en keyword-volumes/CPC zijn **gesimuleerd/illustratief** en als zodanig gemarkeerd. Azure Foundry / Responses API / Communication Services / DataForSEO zijn **niet** gebruikt. De LLM in deze run is dit model (Claude), niet de Foundry Responses API. De *output* (site, schema, artikel, lead-afhandeling) is wél productie-realistisch gegenereerd.
- **Stijl:** Nederlands, professioneel, geen overpromise, geen lange streepjes (em-dash) in de teksten/mails.

---

## 2. Wat is er per stap opgeleverd?

### Stap 1 — Domein-/niche-/keyword-onderzoek
- **Bestand:** [`01-research.md`](01-research.md) + machine-leesbaar in [`client-config.json`](client-config.json)
- **Resultaat:** Niche, doelgroep en servicegebied uitgewerkt; een domein-shortlist van 6 namen (5 "vrij", 1 "bezet" om te tonen dat de check ook nee oplevert, alles illustratief); 12 keywords met intent, gesimuleerd volume/KD/CPC en toegewezen doelpagina; een paginastructuur van 5 hoofdpagina's; en het eerste blogonderwerp. De `client-config.json` is exact het bestand dat het opzet-script in de vervolgstappen consumeert (per-tenant config: branding, schema-types, content-cadans, lead-rubriek, routing).

### Stap 2 — Marketingwebsite bouwen
- **Map:** [`site/`](site/) — 12 HTML-pagina's. Belangrijkste: [`site/index.html`](site/index.html), [`site/warmtepomp-installeren.html`](site/warmtepomp-installeren.html), [`site/hybride-warmtepomp.html`](site/hybride-warmtepomp.html), [`site/cv-ketel-vervangen.html`](site/cv-ketel-vervangen.html), [`site/contact.html`](site/contact.html), plus ondersteunend [`site/over-bram.html`](site/over-bram.html), [`site/privacy.html`](site/privacy.html), [`site/voorwaarden.html`](site/voorwaarden.html).
- **Resultaat:** Statische, snelle, mobiel-responsieve site met de klant-branding 1-op-1 uit de config (`--accent:#E2562B`, `--text:#16263a` als `:root` CSS-vars, Inter). Echte NL-content (geen lorem ipsum), nuchtere jij-toon, USP's, servicegebied, illustratieve reviews (als zodanig gelabeld), FAQ en een warmtescan-conversieformulier met honeypot + consent-checkbox.

### Stap 3 — SEO + GEO automatiseren
- **Bestanden:** [`site/sitemap.xml`](site/sitemap.xml), [`site/robots.txt`](site/robots.txt), [`site/llms.txt`](site/llms.txt), plus de JSON-LD in elke pagina.
- **Resultaat:** Technische SEO + GEO-laag staat. Schema per paginatype: Organization + LocalBusiness + WebSite + FAQPage (home), Service + FAQPage (dienstpagina's), Person (over-bram), Blog (blogindex), Article + BreadcrumbList + FAQPage (artikel). `robots.txt` heet AI-crawlers expliciet welkom (GPTBot, ClaudeBot, PerplexityBot, Google-Extended e.a.); `llms.txt` is een citeerbare feitenkaart met indicatieve prijzen en de eerlijke disclaimer dat dit een fictief testbedrijf is. TL;DR / answer-capsules staan op home en artikel.

### Stap 4 — Blog/content automatisch publiceren
- **Bestand:** [`site/blog/isde-subsidie-warmtepomp-2026.html`](site/blog/isde-subsidie-warmtepomp-2026.html) (met blogindex [`site/blog/index.html`](site/blog/index.html)).
- **Resultaat:** Een volwaardig, ~6-minuten-artikel over de ISDE-subsidie 2026, met named author (Bram, Person-schema + byline + author-box), interne links naar de dienstpagina's en `/contact`, een bronnenblok en een zichtbare **redactionele/feitcheck-notitie**. Alle subsidiebedragen zijn nadrukkelijk indicatief gehouden ("controleer op rvo.nl") — precies waar de productie-feitcheck-gate op slaat, omdat geld-claims anders een hallucinatie-risico zijn.

### Stap 5 — Inbound leads afvangen, beantwoorden, kwalificeren
- **Bestanden:** [`leads/inbound-lead.json`](leads/inbound-lead.json), [`leads/chat-transcript.md`](leads/chat-transcript.md), [`leads/ai-autoreply.md`](leads/ai-autoreply.md), [`leads/qualification.json`](leads/qualification.json).
- **Resultaat:** Beide vangnetten gedemonstreerd. Een realistische inbound lead (Marleen, oude cv-ketel, wil hybride + ISDE) komt binnen via zowel het formulier (`inbound-lead.json`, met AVG-consent-logging en anti-spam-velden) als via een chatgesprek (`chat-transcript.md`, met niet-uitschakelbare AI-disclosure conform EU AI Act Art. 50). De agent stuurt een warme, persoonlijke auto-reply zonder overpromise of genoemd bedrag, en levert een gestructureerde kwalificatie: custom branche-rubriek (score 95/100) plus een BANT-mapping op verzoek.

### Stap 6 — Gekwalificeerde leads doorzetten
- **Bestand:** [`leads/routing-notification.md`](leads/routing-notification.md).
- **Resultaat:** Boven de drempel (60) wordt de lead doorgezet naar Bram, in twee vormen: een e-mailnotificatie (routing-target van deze tenant) én dezelfde inhoud als Microsoft Teams Adaptive Card (de standaard-variant als de klant Teams gebruikt). Beide met **Accept/Reject** en een harde human-in-the-loop-regel: de AI doet geen toezegging, plant niets en zet pas door na menselijke goedkeuring.

---

## 3. Echt vs. gesimuleerd in deze run

| Onderdeel | Status in deze run |
|---|---|
| Website (12 pagina's, branding, content) | **ECHT gegenereerd** — valide HTML, echte NL-content |
| JSON-LD schema (alle paginatypes) | **ECHT gegenereerd** — parseert, types kloppen per pagina |
| Blogartikel (ISDE 2026, named author, bronnen) | **ECHT gegenereerd** — feitcheck-bewust geschreven |
| Lead-afhandeling (intake, auto-reply, kwalificatie-JSON, routing) | **ECHT gegenereerd** — volledige flow met human gate |
| sitemap.xml / robots.txt / llms.txt | **ECHT gegenereerd** |
| Domein-beschikbaarheid (WhoisJSON/WhoisFreaks) | **Gesimuleerd / illustratief** — geen echte call |
| Keyword-volume / KD / CPC (DataForSEO Labs / Google Ads) | **Gesimuleerd / illustratief** — plausibele schattingen |
| KvK / BTW / EUIPO-merkrecht-check | **Niet uitgevoerd** (fictief bedrijf) |
| Azure (Foundry Agent Service, Responses API) | **Niet gebruikt** — ran lokaal |
| Azure Communication Services Email (auto-reply verzending) | **Niet gebruikt** — mail als artefact opgesteld, niet verzonden |
| Cosmos DB / AI Search / Static Web Apps / Functions | **Niet gebruikt** — bestanden op schijf i.p.v. cloud |
| LLM | **Dit model (Claude)** i.p.v. de Foundry Responses API (`gpt-4.1-mini` Data Zone EU in productie) |

---

## 4. Hoe dit 1-op-1 naar de Azure-build mapt

Elke stap in deze lokale run heeft een directe Azure-tegenhanger; de architectuur en het bouwplan staan al klaar:

| Demo-stap (lokaal) | Azure-productie | Doc-referentie |
|---|---|---|
| `client-config.json` invullen | Per-tenant config-injectie + IaC-parameterfile | [`../02-architecture.md`](../02-architecture.md) §5; [`../03-build-plan.md`](../03-build-plan.md) "Onboarding-script" |
| Onderzoek (domein/keyword) | Responses API + DataForSEO + Whois (alleen niet-PII) | `02-architecture.md` §4 (stap 1) |
| Site op schijf | Azure Static Web Apps (Standard) uit dezelfde generator + config | `02-architecture.md` §3; `03-build-plan.md` Fase 1 |
| SEO/GEO-bestanden | Azure Functions (cron) voor sitemap/IndexNow/rank-tracking | `02-architecture.md` §4 (stap 3); `03-build-plan.md` Fase 2 |
| Blogartikel als bestand | Content-agent (cron di 09:00) + `editorial_gate()` + feitcheck-pass | `02-architecture.md` §4 (stap 4); `03-build-plan.md` Fase 2 |
| Lead-JSON + auto-reply-md | Function-intake → Cosmos DB → qualify-agent → ACS Email | `02-architecture.md` §4 (stap 5) |
| Routing-md (Accept/Reject) | Logic App / Function → e-mail/Teams/CRM, met token-gate | `02-architecture.md` §4 (stap 6); `03-build-plan.md` Fase 1 |
| "Eén keer per klant draaien" | Bicep standard-agent-setup + Deployment Stamps, idempotent | `02-architecture.md` §5; `03-build-plan.md` Fase 3 |

De `provisioning_steps`-sectie onderaan [`client-config.json`](client-config.json) beschrijft precies de 8 idempotente acties die het script in Azure zou uitvoeren (resource group + Foundry standard-agent + model-deployments als `data_zone_standard_eu` + Static Web App + Functions + ACS-domeinverificatie + GSC/IndexNow + cost-budget/alert).

---

## 5. Zo bekijk je het (open in je browser)

Open lokaal via `file://`:

- **Website (home):** `file:///Users/werk/Documents/Python/botlease.nl/Projecten/x/demo/site/index.html`
- **Blogartikel (ISDE 2026):** `file:///Users/werk/Documents/Python/botlease.nl/Projecten/x/demo/site/blog/isde-subsidie-warmtepomp-2026.html`
- **Contact / warmtescan-formulier + chat-widget:** `file:///Users/werk/Documents/Python/botlease.nl/Projecten/x/demo/site/contact.html`

> Let op: omdat de site absolute paden gebruikt (`/contact.html`, `/blog/`), werkt klikken tussen pagina's het mooist als je de map serveert in plaats van losse bestanden te openen. Vanuit `demo/site/` bijvoorbeeld: `python3 -m http.server 8080` en dan `http://localhost:8080/` bezoeken. Het formulier en de chat zijn demo-placeholders (geen echte verzending); dat staat ook in de UI vermeld.

De lead-artefacten ([`leads/`](leads/)) en het onderzoek ([`01-research.md`](01-research.md)) lees je als Markdown.

---

## 6. Validatie van de HTML

Alle 12 pagina's zijn geautomatiseerd gecontroleerd (tag-balans-parser + JSON-LD-parse). Uitkomst voor `site/index.html`:

- **Valide en gebalanceerd.** Exact één `<!DOCTYPE html>`, één `<html>`/`<head>`/`<body>`, precies **één `<h1>`** (correcte heading-hiërarchie). Tags sluiten netjes: `<div>` 74 open / 74 dicht, `<section>` 8/8, `<form>` 1/1, `<script>` 2/2, `<style>` 1/1 — geen residual stack, geen losse/verdwaalde tags.
- **JSON-LD parseert** zonder fouten (de `@graph` met Organization + LocalBusiness + WebSite + FAQPage).
- **Geen em-dash/en-dash** in de prose van de mails, het chat-transcript of het artikel (humanizer-regel gehaald). De enige "–" in het artikel zit in een CSS-pseudo-element (`content:"\2013"` als open/dicht-markering bij FAQ-items), niet in zichtbare tekst.
- De overige 11 pagina's gaven hetzelfde resultaat: gebalanceerd, valide JSON-LD, juiste schema-types per paginatype.

---

## 7. Eerlijke observaties

**Wat meeviel / sterk is:**
- De config-driven aanpak werkt: alle branding, schema-types, content-cadans en lead-rubriek komen uit één `client-config.json`, precies zoals de blauwdruk belooft ("één bestand per klant"). De site is daarmee echt herbruikbaar gemaakt, niet ad-hoc geschreven.
- De content is bruikbaar en nuchter, niet AI-wollig. Het artikel houdt geld-claims netjes indicatief en wijst naar rvo.nl — dat is exact wat de feitcheck-gate moet afdwingen.
- De compliance-haakjes zitten er concreet in: niet-uitschakelbare AI-disclosure, consent-logging met versie + timestamp, anti-spam (honeypot + Turnstile-verwijzing), en een echte human-in-the-loop-gate bij het doorzetten.

**Wat in productie extra nodig is (eerlijk):**
- **Echte data i.p.v. simulatie:** domein-availability (Whois), keyword-volumes (DataForSEO) en de echte concurrent-URL's van de klant moeten de gesimuleerde cijfers vervangen vóór registratie of offerte.
- **Echte assets en E-E-A-T-persoon:** logo, hero-/blogbeeld (met AI-label waar gegenereerd) en een échte auteur met echte foto + echt LinkedIn-profiel. E-E-A-T eist een natuurlijk persoon; de fictieve Bram is een placeholder.
- **De feitcheck-gate moet echt draaien:** in deze run is de redactionele notitie handmatig geschreven. In Azure is dit een tweede LLM-pass (draft tegen bron, PASS/FAIL) met een harde stop bij geld-claims, plus een **loud-failure-alert** op "0 gepubliceerd" / fact-check FAIL (de BotLease-news-bot viel ooit stil met exit 0 — die les is verwerkt).
- **De Azure-infra zelf:** Foundry standard-agent-setup (capability host is onveranderlijk, Cosmos min. 3000 RU/s), Static Web Apps Standard, ACS-domeinverificatie (SPF/DKIM/DMARC, anders spam), `WEBSITE_TIME_ZONE` op de cron, en `data_zone_standard_eu` voor EU-only-inference. Dit is de ~30-45 min provisioning + de vaste maandbodem (~$85-260/tenant) die in de prijs moet.
- **Kleine schoonmaak in de demo-map:** `blog.html` en `site/blog/artikel-1.html` zijn redirect-/duplicaat-bestanden (`artikel-1.html` is identiek aan het ISDE-artikel). Functioneel onschadelijk, maar de generator zou in productie geen dubbele canonical/inhoud moeten emitten — punt voor de bouwfase.

---

*Lokale PROJECT X-testrun, 2026-06-21. Testbedrijf en lead fictief; externe data gesimuleerd/illustratief; geen Azure gebruikt. Verifieer alle cijfers met echte API-calls vóór registratie of offerte.*
