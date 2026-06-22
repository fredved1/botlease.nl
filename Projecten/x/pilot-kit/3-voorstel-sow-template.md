# Voorstel + Statement of Work (SOW) — Pilot Project X

> **CONCEPT — laat juridisch toetsen vóór gebruik.** Dit is een sjabloon, geen sluitend contract. De commerciële en juridische bepalingen (aansprakelijkheid, opzegging, IE, verwerkersovereenkomst) moeten door een jurist worden nagekeken vóórdat dit naar een klant gaat of getekend wordt. De verwerkersovereenkomst is een apart document dat hier alleen bij hoort.
>
> **Fase 3** van het intake-proces (Fase 1 kwalificatie-form → Fase 2 scoping-call → **Fase 3 voorstel + SOW + verwerkersovereenkomst** → Fase 4 tekening + aanbetaling → Fase 5 kickoff + diepe intake).
>
> Placeholders staan tussen blokhaken, bv. [KLANTNAAM], [BEDRAG], [DATUM]. Vul ze in vóór verzending. Alle prijzen in dit document zijn **indicatief en moeten vóór de definitieve offerte geverifieerd worden** op de live Azure-/Foundry-pricing-pagina's (zie §8 Aannames).

---

**Tussen:**
BotLease (handelsnaam van Thomas Vedder, eenmanszaak, KvK 95943420, Amsterdam) — hierna "BotLease" of "wij".

**en:**
[KLANTNAAM], [KvK-nummer], [vestigingsadres] — hierna "de Klant" of "u".

**Introducerende partij / technisch contactpunt:** Tijmen ([functie], IT Connect, Almelo) — hierna "IT Connect", betrokken voor de Azure-tenant en techniek aan klantzijde.

| Veld | Waarde |
|---|---|
| Documentversie | v[VERSIE] (concept) |
| Datum voorstel | [DATUM] |
| Geldig tot | [DATUM + 30 dagen] |
| Opgesteld door | Thomas Vedder, BotLease |
| Type traject | Pilot ("Project X" — AI-marketingbureau in een doos) |
| Deploy-model | [A: in de Azure-tenant van de Klant] / [B: in een door BotLease beheerde EU-Azure] |

---

## 1. Samenvatting en doel

[KLANTNAAM] wil zijn online marketing en inbound-leadgeneratie grotendeels automatiseren met een AI-gedreven opzet die volledig binnen een EU-Azure-omgeving draait. BotLease levert daarvoor "Project X": een herbruikbaar, Azure-native systeem dat per bedrijf zes dingen doet (zie §2).

Dit document beschrijft een **pilot**: een eerste, afgebakende oplevering bij één bedrijf, zodat beide partijen de waarde en de werkwijze in de praktijk toetsen vóór een eventuele bredere uitrol. De pilot is bewust beperkt in scope om snel live te gaan en eerlijk te kunnen meten wat het systeem oplevert.

**Doel van de pilot:**
- Een werkende, EU-data-residente marketingsite + content- en lead-pijplijn live krijgen voor [KLANTNAAM].
- Aantonen dat de opzet AVG-bestendig en (waar relevant) AI-Act-bestendig is, met data in de EU.
- Meetbaar maken wat het systeem doet: gepubliceerde content, geïndexeerde pagina's, ontvangen en gekwalificeerde leads, en de gemeten citatiekans bij AI-zoekmachines.
- Een onderbouwde beslissing mogelijk maken over voortzetting/opschaling na de pilotperiode.

**Wat dit nadrukkelijk niet is:** een belofte van een vaste positie in Google of in AI-antwoorden, of een gegarandeerd aantal leads. Zie §9 (no-overpromise-grenzen) — die grenzen zijn onderdeel van dit voorstel.

---

## 2. Scope — de zes stappen (wat WEL en NIET in de pilot zit)

Project X bestaat uit zes stappen. Voor de pilot leggen we per stap expliciet vast wat binnen de afgesproken prijs valt en wat niet.

### Stap 1 — Domein, niche- en keyword-onderzoek

| | |
|---|---|
| **WEL in de pilot** | Niche- en doelgroepbepaling op basis van uw input; seed-keyword-set met indicatief zoekvolume/concurrentie via DataForSEO; concurrent-/keyword-gap op [aantal, bv. 3-5] door u aangeleverde concurrenten; bij een nieuw domein: een shortlist van beschikbare domeinnamen met merkrechten-check (EUIPO) vóór registratie. |
| **NIET in de pilot** | Onbeperkte keyword-rondes of doorlopend keyword-onderzoek na oplevering; betaalde marktonderzoeken; juridisch advies over merkrechten (we signaleren, u/uw jurist beslist). |

### Stap 2 — Marketingwebsite bouwen

| | |
|---|---|
| **WEL in de pilot** | Eén statische, snelle, SEO/GEO-vriendelijke website met uw branding (kleuren, logo via CSS-variabelen), [aantal, bv. 5-8] kernpagina's, schema-markup, llms.txt; gehost op Azure Static Web Apps (Standard) in een EU-regio. |
| **NIET in de pilot** | Maatwerk-(her)ontwerp of een volledig grafisch ontwerptraject; webshop/e-commerce, klantportalen, inlog/accounts; meertalige varianten boven [aantal, default 1] taal; migratie van een bestaand CMS (tenzij apart geoffreerd). |

### Stap 3 — SEO + GEO automatiseren

| | |
|---|---|
| **WEL in de pilot** | Technische SEO (sitemaps, schema, interne links), IndexNow-ping naar Bing/ChatGPT, entity-laag (Organization/sameAs), GEO-tactieken (TL;DR's, answer-capsules, FAQPage); rank-tracking en citatie-monitoring per engine op een afgesproken set zoektermen. |
| **NIET in de pilot** | Een gegarandeerde positie in Google of in AI-antwoorden (zie §9); linkbuilding/PR/betaalde plaatsingen; Google Ads/SEA-campagnebeheer; Google Search Console-property aanmaken namens u (we sluiten aan op uw property). |

### Stap 4 — Blog/content automatisch publiceren

| | |
|---|---|
| **WEL in de pilot** | Een geautomatiseerde content-pijplijn (research → AI-draft → redactionele/feitcheck-gate → publiceren → intern linken → schema/auteur); cadans [bv. 2 artikelen/week] gedurende de pilotperiode; een verplichte mens-in-de-lus-goedkeuringsstap [aan/uit, advies: aan bij start en bij YMYL-sectoren]. |
| **NIET in de pilot** | Onbeperkte volumes of "massa-content" (we publiceren bewust een lage, constante cadans, zie §9); social-media-beheer of -posts; nieuwsbrieven/e-mailcampagnes; redactie/eindredactie door een menselijke tekstschrijver bovenop de AI-draft (de goedkeuring/eindcontrole ligt bij uw aangewezen auteur). |

### Stap 5 — Inbound leads afvangen, beantwoorden en kwalificeren

| | |
|---|---|
| **WEL in de pilot** | Contactformulier + AI-chatwidget op de site; AI stelt een eerste reactie op en voert een kwalificatiegesprek volgens een afgesproken rubriek (BANT of branche-specifiek), met een score en qualified ja/nee; verplichte, niet-uitschakelbare AI-disclosure ("u praat met een AI-assistent") + consent-logging; anti-spam (Turnstile + honeypot + rate-limiting); auto-reply via Azure Communication Services Email vanaf een geverifieerd afzenderdomein. |
| **NIET in de pilot** | Telefonische of WhatsApp-/social-DM-afhandeling; menselijke 24/7-bemanning van de chat; CRM-schoonmaak of import van bestaande leads; gegarandeerde aantallen leads of conversies (zie §9). |

### Stap 6 — Gekwalificeerde leads doorzetten naar de Klant

| | |
|---|---|
| **WEL in de pilot** | Routering van leads boven de afgesproken drempelscore naar één bestemming: [e-mail] / [Microsoft Teams met Accept/Reject-kaart] / [CRM: Dynamics 365 / HubSpot / Pipedrive]; keuze tussen autonoom doorzetten of mens-in-de-lus vóór doorzet. |
| **NIET in de pilot** | Diepe tweerichtings-CRM-synchronisatie of maatwerk-CRM-integraties buiten de afgesproken bestemming; meerdere gelijktijdige routing-bestemmingen (boven [1] is meerwerk); aankoop/levering van CRM-licenties (die regelt en betaalt u zelf). |

> **Gevoelige toegang loopt buiten dit document om.** Azure subscription-/tenant-ID, API-keys, CRM-credentials en RBAC-delegatie worden NIET in dit voorstel of in een formulier als waarde uitgevraagd. Ze lopen out-of-band via Azure Key Vault / Azure Lighthouse met least-privilege-rollen. In §4 leggen we alleen vast wie ze aanlevert en wanneer.

---

## 3. Deliverables en acceptatiecriteria

| # | Deliverable | Acceptatiecriterium (afgevinkt = geaccepteerd) |
|---|---|---|
| D1 | Onderzoeksrapport (niche, keywords, concurrenten, [evt. domein-shortlist]) | Aangeleverd als document; besproken en akkoord bevonden door [KLANTNAAM]. |
| D2 | Live marketingwebsite op [domein] | Bereikbaar via het afgesproken domein over HTTPS; uw branding zichtbaar; alle afgesproken kernpagina's aanwezig; sitemap en llms.txt bereikbaar. |
| D3 | Technische SEO/GEO-laag actief | Sitemap ingediend; schema valideert zonder fouten; IndexNow-ping verzonden; rank-/citatie-monitoring ingericht op de afgesproken zoektermen (meting ingericht, geen positiegarantie). |
| D4 | Content-pijplijn operationeel | Minimaal [aantal, bv. 4] artikelen via de pijplijn gepubliceerd binnen de pilotperiode, elk door de redactionele/feitcheck-gate en (indien aan) door uw auteur goedgekeurd. |
| D5 | Lead-afvang + AI-kwalificatie live | Een testlead doorloopt formulier én chat, krijgt een auto-reply, wordt gescoord, en de AI-disclosure + consent-logging zijn aantoonbaar aanwezig. |
| D6 | Lead-doorzet werkend | Een gekwalificeerde testlead arriveert aantoonbaar op de afgesproken bestemming ([e-mail/Teams/CRM]). |
| D7 | Opleverdocument | Korte beschrijving van wat live staat, waar het draait (regio/deployment-type), welke accounts/keys bij wie liggen, en hoe te monitoren (incl. alert bij "0 gepubliceerd"). |

**Acceptatieproces:** na oplevering van een deliverable heeft u [aantal, bv. 5] werkdagen om te accepteren of gemotiveerd af te keuren tegen het bijbehorende criterium. Reageert u niet binnen die termijn, dan geldt de deliverable als geaccepteerd. Afkeuring kan alleen op het afgesproken acceptatiecriterium, niet op nieuwe wensen (die lopen via change control, §7).

---

## 4. Rolverdeling — wat BotLease doet vs. wat de Klant aanlevert

**BotLease levert/doet:**
- Het ontwerp en de bouw van de zes stappen binnen de afgesproken scope.
- De Infrastructure-as-Code en de provisioning van de Azure-resources (in deploy-model A: in uw tenant; in model B: in onze EU-Azure).
- De per-tenant configuratie (branding, niche-prompt, kwalificatie-rubriek, routing, cadans).
- Inrichting van monitoring en de verplichte AI-disclosure + consent-logging.
- Een concept-verwerkersovereenkomst (apart document, laat juridisch toetsen).

**De Klant (en, waar aangegeven, IT Connect) levert aan / regelt:**

| Onderwerp | Wie | Wanneer | Toelichting |
|---|---|---|---|
| **RBAC / Azure-toegang** | Klant/IT Connect | Vóór provisioning (Fase 5) | Iemand met Owner of User Access Administrator kent de benodigde least-privilege-rollen toe; beheertoegang voor BotLease via Azure Lighthouse of service principal. **De toegang zelf loopt out-of-band, niet via dit document — we leggen hier alleen de toezegging + de verantwoordelijke vast.** |
| **DNS** | Klant/IT Connect | Vóór oplevering | DNS-beheertoegang om de site-CNAME naar Azure te zetten en SPF/DKIM/DMARC voor het afzenderdomein in te richten (anders belanden auto-replies in spam). |
| **Auteur (E-E-A-T)** | Klant | Vóór content live | Een echte persoon bij u (naam, functie, korte bio, foto, profiel-URL's) als zichtbare auteur. Geen gescrapete persoonsgegevens; u levert dit zelf aan. |
| **Merk / huisstijl** | Klant | Vóór site-bouw | Logo (bij voorkeur SVG) + merkkleuren (hex), tone-of-voice, verplichte juridische teksten (privacyverklaring, AV, KvK/BTW). |
| **Bedrijfs-/niche-info** | Klant | Fase 5 | Branche, kerndiensten, doelgroep, [evt.] concurrenten. |
| **Lead-bestemming + rubriek** | Klant | Vóór go-live | Routing-doel (e-mail/Teams/CRM), notificatie-adres(sen), kwalificatie-rubriek, score-drempel, autonoom of mens-in-de-lus. |
| **CRM-licenties + credentials** | Klant | Indien CRM-routing | Eventuele CRM-licenties koopt en betaalt u zelf; credentials gaan out-of-band in Key Vault. |
| **Akkoorden compliance** | Klant | Vóór tekening | Verwerkersovereenkomst, datalocatie-keuze (model + deployment-type), AI-disclosure, consent-logging, bewaartermijn leads. |
| **Microsoft-contracttype** | Klant/IT Connect | Scoping | Bevestiging EA/MCA of pay-as-you-go (bepaalt of Zero Data Retention / Modified Abuse Monitoring haalbaar is; zie §9). |

> Vertraging in aanlevering door de Klant verschuift de tijdlijn en kan, indien Azure-resources al draaien, doorlopende verbruikskosten meebrengen (die u in model A zelf draagt).

---

## 5. Tijdlijn en fasen

Indicatieve doorlooptijd pilot: [bv. 4-6 weken] vanaf tekening + aanbetaling, mits de Klant tijdig aanlevert (§4).

| Fase | Inhoud | Indicatieve duur | Wie |
|---|---|---|---|
| Fase 1 (afgerond) | Kwalificatie-form | — | Klant |
| Fase 2 (afgerond) | Scoping-/discovery-call | — | Beiden |
| **Fase 3 (nu)** | **Dit voorstel + SOW + concept-verwerkersovereenkomst** | [bv. 1 week beoordeling] | Beiden |
| Fase 4 | Tekening + aanbetaling | [—] | Beiden |
| Fase 5 | Kickoff + diepe intake; provisioning Azure-resources (reken ~30-45 min per tenant provisioning, exclusief voorbereiding) | [bv. week 1] | Beiden |
| Bouw 1 | Site + technische SEO/GEO live (D2, D3) | [bv. week 1-2] | BotLease |
| Bouw 2 | Content-pijplijn + lead-afvang/kwalificatie/doorzet live (D4-D6) | [bv. week 2-4] | BotLease |
| Oplevering | Acceptatie + opleverdocument (D7) | [bv. week 4-6] | Beiden |
| Pilot-evaluatie | Meetrapport + go/no-go opschaling | [na pilotperiode] | Beiden |

> **BotLease-regel: nooit voorschieten.** Provisioning (Fase 5) start pas ná tekening én aanbetaling. De vaste Azure-bodemkosten (o.a. AI Search en Cosmos) lopen 24/7 zodra geprovisioned is.

---

## 6. Prijsmodel

> **Alle bedragen hieronder zijn indicatief en moeten vóór de definitieve offerte geverifieerd worden** op de actuele Azure-/Foundry-pricing-pagina's. Azure- en model-EU-beschikbaarheid en -prijzen wijzigen per kwartaal. Bedragen zijn [excl./incl.] btw — bevestig vóór tekening.

**Model:** eenmalige setup-fee (de intake + de "script-run"/provisioning + de pilot-bouw) + een maandelijkse beheer-/AI-fee. **De Klant draagt het eigen Azure-verbruik** (model A: rechtstreeks op het eigen abonnement; model B: [doorbelast / inbegrepen, kies één]).

| Post | Indicatief bedrag | Toelichting |
|---|---|---|
| **Setup-fee (eenmalig)** | € [BEDRAG] | Intake, onderzoek, provisioning, bouw van de zes stappen binnen pilot-scope, oplevering. |
| **Maandelijkse beheer-/AI-fee** | € [BEDRAG] / maand | Beheer, monitoring, content-cadans, lead-pijplijn, kleine bijstellingen binnen scope. Looptijd pilot: [aantal] maanden. |
| **Aanbetaling bij tekening** | [bv. 50%] van de setup-fee = € [BEDRAG] | Voorwaarde voor start provisioning (Fase 5). |

**Azure-verbruik (draagt de Klant, indicatief — verifiëren vóór offerte):**

| Post | Indicatie | Opmerking |
|---|---|---|
| Azure AI Search | ~$75/mnd (Basic) tot ~$250/mnd (S1) | Grootste vaste bodemlast; draait 24/7. |
| Cosmos DB | RU/s-afhankelijk (standard agent setup vereist min. ~3000 RU/s) | Vaste bodem; 24/7. |
| Azure Static Web Apps | ~$9/site/mnd (Standard, met SLA) | Free-tier heeft geen SLA, niet voor productie. |
| Container Apps / Functions | vaak ~$0 binnen de gratis grant | Schaalt naar nul. |
| LLM-tokens (GPT-4.1-mini/4o-mini werkpaard) | centen tot enkele euro's/mnd bij deze workload | Data Zone EU ligt ~5-10% hoger dan Global Standard. |
| Grounding with Bing (indien gebruikt) | ~$35 per 1.000 queries | Duur; alleen waar live web echt nodig is. |
| ACS Email | ~$0,00025/mail + dataverbruik | Verwaarloosbaar bij pilot-volume. |

> Realistische vaste Azure-bodem per tenant: grofweg ~$85-$260/mnd, los van LLM-verbruik. **Dit is een schatting, geen toezegging; u betaalt het werkelijke verbruik aan Microsoft (model A).**

**Niet inbegrepen / aparte kosten van de Klant:** domeinregistratie, eventuele CRM-licenties, betaalde stockbeelden, en externe SaaS-accounts (bv. DataForSEO-deposit) voor zover die op naam van de Klant lopen. Welke partij welk account aanhoudt, leggen we vast in Fase 5.

---

## 7. Change control (meerwerk)

- Werk buiten de scope van §2 (bv. extra talen, een tweede routing-bestemming, CMS-migratie, maatwerk-design, hogere content-cadans) is meerwerk.
- Meerwerk wordt vóór uitvoering schriftelijk vastgelegd in een korte change-aanvraag met omschrijving, impact op tijdlijn en prijs, en uw akkoord.
- Geen werk buiten scope wordt uitgevoerd zonder uw schriftelijke akkoord op de change-aanvraag.
- Afkeuring van een deliverable kan alleen tegen het overeengekomen acceptatiecriterium (§3); nieuwe wensen lopen via change control.

---

## 8. Aannames

Dit voorstel gaat uit van het volgende. Klopt een aanname niet, dan kan dat de scope, tijdlijn of prijs raken (via §7).

1. Deploy-model is [A / B] en is in Fase 2 bevestigd.
2. Hardheid EU-eis is [data-at-rest in EU / EU-only-inference]. Bij EU-only-inference beperkt de modelkeuze zich medio 2026 tot GPT-4o / GPT-4.1 (Data Zone EU); de nieuwste GPT-5.x is dan nog niet als EU-data-zone beschikbaar.
3. EU-regio is [West Europe / North Europe / Sweden Central / Germany West Central]; bij private networking moeten alle resources in dezelfde regio staan.
4. De Klant heeft een geschikte Azure-subscription + Entra-tenant en iemand die RBAC kan toekennen.
5. Microsoft-contracttype is [EA/MCA / pay-as-you-go]. Zero Data Retention en Modified Abuse Monitoring zijn alleen aanvraagbaar op EA/MCA, niet op pure pay-as-you-go.
6. De Klant levert merk, auteur, niche-info, DNS- en lead-bestemming tijdig aan (§4).
7. **Alle in §6 genoemde Azure-/Foundry-prijzen en de EU-model-beschikbaarheid zijn indicatief en worden vóór de definitieve offerte opnieuw geverifieerd op de live pricing-pagina's.**
8. Externe SaaS-API's (DataForSEO, domein-checks) krijgen uitsluitend niet-persoonsgebonden queries; lead-PII blijft strikt binnen Azure-EU. Waar nodig sluiten we DPA's met die leveranciers.
9. Eén taal en één routing-bestemming, tenzij anders vermeld in §2.

---

## 9. No-overpromise-grenzen (onderdeel van dit voorstel)

Wij beloven niets wat we niet hard kunnen maken. De volgende grenzen zijn expliciet onderdeel van de overeenkomst:

**GEO / AI-citatie en SEO:**
- Wij maximaliseren de **kans** dat uw content geciteerd of gevonden wordt en wij **meten dit per engine** (Google, Bing/ChatGPT, Perplexity, Gemini). Wij garanderen **geen** positie, ranking, of vermelding in AI-antwoorden of in Google. Posities worden bepaald door de zoekmachines/AI-engines zelf en liggen buiten onze invloed.

**Leads:**
- Wij garanderen **geen** aantal leads, geen aantal gekwalificeerde leads en geen conversies. Het systeem vangt, beantwoordt, kwalificeert en routeert inbound leads; hoeveel er binnenkomen hangt af van uw markt, aanbod en verkeer.

**Content:**
- Wij publiceren bewust een **lage, constante cadans** met een verplichte redactionele/feitcheck-gate. Wij publiceren géén grote volumes AI-content tegelijk; dat wordt door zoekmachines afgestraft (scaled content abuse) en is een risico, geen feature.

**Privacy / "AI leest niet mee":**
- De belofte dat prompts/antwoorden niet bewaard worden of niet voor menselijke review in aanmerking komen (Zero Data Retention / Modified Abuse Monitoring) doen wij **alleen** als is bevestigd dat uw Azure-tenant dat traject kan aanvragen (vereist EA/MCA). Tot die bevestiging gaan wij uit van de standaard Microsoft-instellingen.

**Beschikbaarheid / support / vervanging:**
- Support is op werkdagen, niet 24/7.
- Bij een verstoring lossen wij dit op of zetten waar van toepassing een vervangende voorziening in, doorgaans binnen enkele werkdagen. Wij noemen geen vaste hersteltijd ("binnen 24 uur") en geen vast bedrag.
- Service-levels (responstijden, eventuele uptime-afspraken) worden, indien gewenst, apart vastgelegd; dit pilot-voorstel bevat geen SLA tenzij expliciet bijgevoegd.

**Compliance:**
- Wij bouwen AVG- en (waar relevant) AI-Act-bestendig en leveren een concept-verwerkersovereenkomst. Wij geven geen juridische garantie of vrijwaring; eindverantwoordelijkheid voor de juridische teksten en de inzet ligt bij de Klant, na toetsing door uw eigen jurist.

---

## 10. AVG-rollen (samengevat — zie verwerkersovereenkomst voor het volledige beeld)

- Voor de **intake-/contactgegevens van de Klant zelf** is BotLease **verwerkingsverantwoordelijke** (eigen privacyverklaring + bewaartermijn).
- Voor de **lead-data die via de site van de Klant binnenkomt** is BotLease **(sub)verwerker** namens de Klant. Hiervoor geldt een **verwerkersovereenkomst tussen BotLease en de Klant, bovenop de Microsoft DPA**.
- Elke externe form-/SaaS-tool die wij inzetten, is een **sub-verwerker**; daarmee sluiten wij de benodigde DPA's. Verwerkingsketen: Klant → BotLease → Microsoft (EU) + eventuele sub-verwerkers (EU).

---

## 11. Akkoord

Ondertekening hieronder geldt als akkoord op dit voorstel + SOW en op de bijbehorende (concept-)verwerkersovereenkomst. Tekening leidt tot de aanbetaling uit §6; provisioning start pas daarna (§5).

> **Herinnering: dit is een concept. Laat het juridisch toetsen vóór ondertekening.**

| | BotLease | [KLANTNAAM] |
|---|---|---|
| Naam | Thomas Vedder | [NAAM] |
| Functie | Eigenaar | [FUNCTIE] |
| Datum | [DATUM] | [DATUM] |
| Handtekening | __________________ | __________________ |

---

*Bestand: `/Users/werk/Documents/Python/botlease.nl/Projecten/x/pilot-kit/3-voorstel-sow-template.md`. Concept-template, stand juni 2026. Verifieer alle Azure-/Foundry-prijzen en de EU-model-beschikbaarheid vlak vóór elke offerte; laat de juridische bepalingen en de verwerkersovereenkomst toetsen vóór gebruik.*
