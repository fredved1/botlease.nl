# PROJECT X — Fase 2: Scoping-/discovery-call agenda

> Voor Thomas (BotLease), met Tijmen (IT Connect, Almelo) erbij. Eerste/pilot-klant.
> Fase 2 in het intake-proces: Fase 1 kort kwalificatie-form -> **Fase 2 scoping/discovery-call (dit document)** -> Fase 3 voorstel + SOW + verwerkersovereenkomst -> Fase 4 tekening + aanbetaling -> Fase 5 kickoff + diepe intake.
>
> **Toon:** white-glove, eerlijk, geen overpromise. Dit gesprek bepaalt de hele architectuur en de offerte. We leggen hier de twee splitsende keuzes vast en de no-overpromise-grenzen, zodat Fase 3 (SOW) geen verrassingen kent.
> **Prijs-disclaimer voor jezelf:** alle Azure/Foundry-bedragen die je noemt zijn indicatief en moeten vóór de offerte (Fase 3) geverifieerd worden op de live pricing-pagina's. Noem geen harde maandbedragen in deze call; noem ranges en "we verifiëren dit in het voorstel".

---

## Doel van de call (in 1 zin)

De twee architectuur-bepalende keuzes vastleggen (deploy-model A/B + hardheid EU-inference), het beslisproces en de economic buyer achter Tijmen helder krijgen, de scope-verwachtingen kalibreren, en de no-overpromise-grenzen alvast benoemen, zodat we daarna een scherp voorstel + SOW + verwerkersovereenkomst kunnen maken.

**Wat deze call expliciet NIET is:** geen diepe technische intake (dat is Fase 5, na tekening). Geen secrets uitvragen (subscription-ID, tenant-ID, API-keys, RBAC lopen altijd out-of-band via Key Vault / Lighthouse, nooit in een gesprek of form als in te vullen waarde). We vragen hier alleen de TOEZEGGING en WIE het later regelt.

---

## Vooraf (Thomas, vóór de call afvinken)

- [ ] Fase-1 kwalificatie-form van deze klant doorgelezen (hosting-voorkeur, grove EU-eis, tijdlijn, contactpersoon).
- [ ] Wie zit er aan tafel? Alleen Tijmen, of ook iemand van de eindklant? (Bepaalt of we de economic-buyer-vragen nu of via Tijmen later beantwoord krijgen.)
- [ ] Notitie-template open (de afvink-velden hieronder zijn meteen je verslag).
- [ ] Tijdsindicatie afgesproken: 45 minuten. Bij twee partijen aan tafel: reken 60 min.

---

## Tijdsindeling (45 min)

| Tijd | Blok | Doel |
|---|---|---|
| 0-5 min | **A. Opening + verwachtingen** | Doel van de call, agenda, white-glove toon |
| 5-12 min | **B. Beslisproces + economic buyer** | Wie tekent, wie betaalt, wat is de echte trigger |
| 12-25 min | **C. De twee architectuur-keuzes** | Deploy-model A/B + hardheid EU-inference (kern van de call) |
| 25-35 min | **D. Scope-verwachtingen** | Wat valt erin, wat erbuiten, tijdlijn, CRM/leads-bestemming |
| 35-42 min | **E. No-overpromise-grenzen** | Eerlijk de grenzen benoemen vóór we ze in de SOW zetten |
| 42-45 min | **F. Afsluiting + vervolgstappen** | Wat gebeurt er na de call, wie levert wat |

---

## A. Opening + verwachtingen (0-5 min)

- [ ] Doel benoemen: "We gaan vandaag de paar keuzes maken die de hele opzet bepalen. Daarna kan ik een scherp voorstel maken. Dit is geen technische diepte-sessie, dat doen we pas na akkoord."
- [ ] Geruststelling/trust-cue: "Ik vraag vandaag geen wachtwoorden, Azure-ID's of toegangsrechten. Die regelen we later veilig via Azure Key Vault, niet in een gesprek of formulier."
- [ ] Agenda kort doorlopen, tijdsindicatie bevestigen.

---

## B. Beslisproces + economic buyer achter Tijmen (5-12 min)

> Tijmen werkt bij IT Connect en brengt een eindklant. We moeten weten wie er echt beslist en betaalt, anders maken we straks een voorstel voor de verkeerde persoon. Dit is de MEDDIC-laag: deze hoort in een gesprek, niet in een form.

- [ ] **Wie is de eindklant precies?** (bedrijfsnaam, branche, grootte) `____________________`
- [ ] **Rol van Tijmen/IT Connect:** doorverwijzer, IT-partner van de klant, mede-uitvoerder, of zelf de klant? `____________________`
  - Bepaalt: tekenen we met de eindklant of met IT Connect? Wie wordt de contractpartij in de SOW?
- [ ] **Economic buyer:** wie heeft het budget en zet uiteindelijk de handtekening? `____________________`
- [ ] **Beslisproces:** wie moeten allemaal ja zeggen (IT, directie, security/compliance-officer, DPO)? `____________________`
- [ ] **De echte trigger / pijn:** waarom nu? Wat lost dit op dat een gewoon marketingbureau of GoHighLevel niet kan? (Verwachting: de "alles in eigen EU-Azure"-eis.) `____________________`
- [ ] **Budget-indicatie + verwachtingsbeeld:** heeft de klant een orde van grootte in gedachten? (Niet hard pinnen, wel kalibreren of we in dezelfde wereld zitten.) `____________________`
- [ ] **Tijdlijn / urgentie:** wanneer wil de klant live? Is er een harde deadline (event, campagne, fiscaal jaar)? `____________________`
- [ ] **Wie betaalt het Azure-verbruik?** Klant rechtstreeks (eigen abonnement) of factureren wij door? `____________________`
  - Bepaalt ons prijsmodel: setup-fee + maandelijkse beheer/AI-fee (klant draagt Azure) vs. all-in maandbedrag.

---

## C. De twee architectuur-bepalende keuzes (12-25 min) — KERN VAN DE CALL

> Dit zijn de twee vragen die letterlijk alles erna bepalen: kosten, isolatie, modelkeuze, compliance-garanties. Zonder deze antwoorden is een voorstel gokwerk. Leg per antwoord vast: harde eis, voorkeur, of "weet ik nog niet".

### C1. Deploy-model: A (klant-tenant) of B (bureau-tenant)?

- [ ] **De vraag:** "Moet alles draaien in jullie EIGEN Azure-tenant/subscription, of mag het in een door ons beheerde Azure-omgeving in de EU draaien?"
- [ ] Leg de twee modellen kort uit:
  - **Model A — in de Azure van de klant** (verwachte eis): wij rollen uit via een Azure Managed Application in jullie subscription. Data blijft 100% bij jullie; wij beheren via een afgeschermde identity (Azure Lighthouse, least-privilege, nooit "Owner" op de hele subscription). Hoogste isolatie. Jullie dragen de vaste Azure-bodemlast zelf.
  - **Model B — in onze Azure**: gedeelde/afgescheiden omgeving in onze EU-Azure. Goedkoper (resources deelbaar), maar lagere isolatie en niet "alles in eigen tenant".
- [ ] **Antwoord vastleggen:** A / B / nog onbeslist `____________________`
- [ ] **Status:** harde eis / voorkeur / weet nog niet `____________________`
- [ ] Bij model A, de TOEZEGGINGEN uitvragen (niet de waarden zelf):
  - [ ] Is er een Azure-subscription + Entra ID-tenant om in te deployen? (ja/nee, wie bevestigt) `____________________`
  - [ ] Is er iemand met Owner of User Access Administrator die tijdens provisioning de RBAC-rollen kan toekennen? Wie? `____________________`
  - [ ] Akkoord met beheertoegang voor Thomas via Azure Lighthouse, least-privilege? Wie regelt de delegatie? `____________________`
  - [ ] **Niet uitvragen in deze call:** subscription-ID, tenant-ID, daadwerkelijke RBAC-toekenning. Die lopen out-of-band in Fase 5.
- [ ] **EA/MCA-vraag (bepaalt of "AI leest niet mee" mag worden beloofd):** "Hebben jullie een Enterprise Agreement of Microsoft Customer Agreement bij Microsoft, of een gewone pay-as-you-go subscription?" `____________________`
  - Eerlijk benoemen: Zero Data Retention / Modified Abuse Monitoring is alléén beschikbaar op EA/MCA. Op pure pay-as-you-go kunnen we niet beloven dat prompts niet ~30 dagen worden gelogd. Dit pas beloven ná bevestiging.

### C2. Hardheid van de EU-eis: data-at-rest in EU vs. EU-only-inference?

- [ ] **De vraag:** "Is de eis dat de data in de EU staat (data-at-rest), of moet ook de AI-verwerking zelf (de inference) gegarandeerd binnen de EU blijven?"
- [ ] Eerlijk de valkuil uitleggen: een standaard "Global Standard"-deployment geeft GEEN garantie dat de inference in de EU blijft, ook al staat de resource in een EU-regio. De data-at-rest blijft wel in de EU. Voor harde EU-only-inference moeten we "Data Zone Standard (EU)" kiezen.
- [ ] **De consequentie eerlijk benoemen (modelkeuze):** bij een harde EU-only-inference-eis zijn we medio 2026 beperkt tot **GPT-4o / GPT-4.1** (Data Zone EU). De allernieuwste modellen (GPT-5.x) zijn medio 2026 nog NIET als EU-data-zone beschikbaar. Dat is geen tekortkoming van ons, maar van wat Microsoft op dit moment EU-resident aanbiedt. Voor onze workload (blog/SEO/lead-replies) is GPT-4.1-mini ruim voldoende.
- [ ] **Antwoord vastleggen:** data-at-rest-in-EU / EU-only-inference / nog onbeslist `____________________`
- [ ] **Status:** harde eis / voorkeur / weet nog niet `____________________`
- [ ] **Voorkeursregio aanstippen (niet hard nu):** West Europe (Amsterdam, NL) is logisch voor NL-residency; let op dat brede EU-data-zone-modelhosting nu vooral Sweden Central / Germany West Central is. Vastleggen in Fase 5. Voorkeur klant? `____________________`

---

## D. Scope-verwachtingen (25-35 min)

> Doel: kalibreren wat de klant verwacht vs. wat we in de pilot opleveren, zodat de SOW geen scope-creep krijgt. Onder ~5 klanten mag de pilot half-handmatig zijn; volledige automatisering is dan over-engineering. Benoem dat eerlijk.

- [ ] De 6 stappen kort schetsen en per stap polsen of die in scope is voor de pilot:
  - [ ] 1. Domein-/niche-/keyword-onderzoek
  - [ ] 2. Marketingwebsite bouwen (statisch, snel, SEO/GEO-vriendelijk, eigen merk)
  - [ ] 3. SEO + GEO automatiseren (sitemaps, schema, IndexNow, rank-tracking)
  - [ ] 4. Blog/content automatisch publiceren (lage cadans, editorial-gate, mens-in-de-lus bij start)
  - [ ] 5. Inbound leads afvangen + beantwoorden + kwalificeren (formulier + AI-chat-widget)
  - [ ] 6. Gekwalificeerde leads doorzetten naar de klant
- [ ] **MVP-scope kalibreren:** "Voor de eerste opzet houden we het bewust pragmatisch; een deel mag half-handmatig. Volledige multi-tenant-automatisering bouwen we pas als het volume het rechtvaardigt." Akkoord? `____________________`
- [ ] **CRM / lead-bestemming:** waar moet een gekwalificeerde lead heen? Dynamics 365 / HubSpot / Pipedrive / Teams (Accept-Reject) / e-mail / nog onbekend `____________________`
- [ ] **Lead-autonomie:** mag de AI-chatbot autonoom antwoorden, of altijd mens-in-de-lus? (Sluit aan op de no-overpromise-lijn.) `____________________`
- [ ] **Kwalificatie-rubriek:** klassiek BANT of branche-specifiek? (Detail volgt in Fase 5, nu alleen richting.) `____________________`
- [ ] **Content-type richting:** nieuws (feed-gedreven) / evergreen blogs / beide? `____________________`
- [ ] **Domein:** bestaand domein koppelen of nieuw zoeken/registreren? Wie wordt registrant (klant of bureau)? `____________________`
- [ ] **Named author (E-E-A-T):** is er een echte persoon bij de klant die zichtbare auteur van de content wordt? (Nodig voor GEO; nu alleen polsen of dat kan.) `____________________`
- [ ] **Wat valt expliciet BUITEN scope** voor de pilot, vastleggen om later discussie te voorkomen: `____________________`

---

## E. No-overpromise-grenzen alvast benoemen (35-42 min)

> Dit op tafel leggen vóór de SOW is het sterkste vertrouwenssignaal voor een compliance-bureau. We verkopen liever eerlijk dan dat we later moeten terugkomen op een belofte. Benoem deze grenzen actief; ze komen straks letterlijk in de SOW.

- [ ] **GEO / AI-citatie:** "Geciteerd worden door ChatGPT, Perplexity of Gemini is geen knop die we kunnen omzetten. We maximaliseren de citatiekans (answer-capsules, schema, freshness, llms.txt) en meten per engine, maar we garanderen geen positie of ranking." Klant begrijpt dit? `____________________`
- [ ] **SEO algemeen:** geen gegarandeerde Google-posities; we leveren de technische en content-fundering en meten de voortgang.
- [ ] **"AI leest niet mee / data wordt niet bewaard":** dit beloven we pas ná bevestiging dat de klant-tenant Zero Data Retention / Modified Abuse Monitoring kan aanvragen (vereist EA/MCA). Standaard logt Azure prompts/completions ~30 dagen.
- [ ] **Automatisering met bewuste gates:** content krijgt een editorial/feitcheck-gate, leads kunnen mens-in-de-lus. Volledig autonoom is een risico, geen feature. Geen massa-content (Google straft scaled content af); lage, constante cadans.
- [ ] **EU AI Act Art. 50 (vanaf aug 2026):** de sales-chatbot moet bij eerste interactie melden dat het AI is. Dit is een niet-uitschakelbaar, ingebouwd onderdeel. Geen optie om "weg te halen voor een menselijker gevoel".
- [ ] **Prijzen indicatief:** "De Azure- en model-prijzen die ik noem zijn indicatief; ze veranderen per kwartaal. In het voorstel verifieer ik ze op de actuele pricing-pagina's." Geen harde maandbedragen toezeggen in deze call.
- [ ] **AVG-rollen kort schetsen** (komt in de verwerkersovereenkomst): wij zijn verwerkingsverantwoordelijke voor de intake-data zelf, en (sub)verwerker voor de latere lead-data van jullie site. Er komt een verwerkersovereenkomst bovenop de Microsoft DPA.

---

## F. Afsluiting + vervolgstappen (42-45 min)

- [ ] Samenvatten wat is besloten: deploy-model, hardheid EU-eis, scope-richting, wie de buyer is. Hardop teruggeven ter bevestiging.
- [ ] Benoemen wat de klant aanlevert vóór het voorstel (geen secrets, alleen toezeggingen + namen).
- [ ] Volgende stap en timing afspreken.

---

## Concrete vervolgstappen NA de call

**Thomas (BotLease):**
- [ ] Verslag van deze call vastleggen (de afvink-velden hierboven) en de twee kernkeuzes (C1 deploy-model, C2 EU-hardheid) in de `client-config` als beslissingen noteren.
- [ ] Azure-/Foundry-/model-prijzen + de EU-data-zone-modellijst verifiëren op de live pricing-pagina's (verplicht vóór de offerte).
- [ ] **Voorstel + SOW** opstellen (Fase 3): scope, deliverables, acceptatiecriteria, rollen aan beide kanten (klant levert RBAC/DNS/auteur aan), change control, en de no-overpromise-grenzen expliciet vastgelegd. Bovenaan vermelden: "concept, laat juridisch toetsen vóór gebruik".
- [ ] **Verwerkersovereenkomst** (concept) klaarzetten, bovenop de Microsoft DPA, met de juiste AVG-rollen. Bovenaan: "concept, laat juridisch toetsen vóór gebruik". Op tafel leggen vóór de klant erom vraagt.
- [ ] Prijsmodel bepalen: setup-fee + maandelijkse beheer/AI-fee vs. all-in, op basis van wie het Azure-verbruik draagt (uit blok B).
- [ ] Niets provisionen vóór tekening + aanbetaling (Azure-bodemkosten lopen direct; BotLease-regel: nooit voorschieten).

**Klant / Tijmen (aan te leveren vóór of bij het voorstel, alleen toezeggingen, geen secrets):**
- [ ] Bevestiging contractpartij (eindklant of IT Connect) + wie tekent (economic buyer).
- [ ] Bevestiging deploy-model (A/B) en hardheid EU-eis als definitieve keuze.
- [ ] Bevestiging EA/MCA-status (bepaalt of ZDR/Modified Abuse Monitoring kan).
- [ ] Aanwijzen wie later (Fase 5) de RBAC/Lighthouse-delegatie regelt en wie DNS beheert. Namen, geen toegang.
- [ ] Bevestiging dat er een echte named author beschikbaar is (E-E-A-T).
- [ ] Akkoord op de no-overpromise-grenzen zoals besproken (komt terug in de SOW).

**Daarna:** Fase 3 voorstel + SOW + verwerkersovereenkomst delen -> Fase 4 tekening + aanbetaling -> Fase 5 kickoff + diepe technische intake (de volle config; secrets out-of-band via Key Vault / Lighthouse).
