# PROJECT X — Intake-aanpak (beslisdocument)

*Voor Thomas (beslisser + bouwer). Stand: juni 2026. Eerlijk, geen hype. Verifieer prijzen/tiers vlak vóór je iets vastlegt — form-tool-prijzen en Azure/model-EU-beschikbaarheid wijzigen per kwartaal.*

Dit document beantwoordt één vraag: **hoe richten we de client-intake voor Project X in zodat hij premium en vertrouwenwekkend is, AVG/EU-residentie waterdicht is, en de output 1-op-1 het opzet-script (`onboard.py`) voedt?**

Brondocumenten die hierbij horen: `01-client-intake.md` (de 11 secties + per-vraag "waarom"), `client-config.template.json` (het JSON-schema dat `onboard.py` consumeert), `04-data-needed.md` (de bekende onzekerheden en valkuilen C1–C11), `00-BLUEPRINT.md` (de "alles-in-eigen-EU-Azure"-filosofie).

---

## 0. Korte samenvatting (TL;DR)

- **De huidige kale form is niet alleen lelijk — hij is functioneel kapot.** Geen `<form action>`, geen webhook, geen opslag: de antwoorden gaan nergens heen. En regel 246 vraagt **Subscription-ID + Tenant-ID als platte tekst** — dat is een beveiligings- én geloofwaardigheidsfout voor een compliance-bureau. Dit móét sowieso weg.
- **Intake is geen formulier maar een proces.** Alle 11 secties in één form proppen = >50% afhaak en het amateurgevoel dat we juist willen vermijden. Splits in: kort kwalificatie-form → scoping-call → SOW + verwerkersovereenkomst → tekening → kickoff + diepe intake.
- **Aanbeveling voor de EERSTE klant (Tijmen/IT Connect): NIET zelf bouwen. Koop de UX in via Tally Pro (EU-by-default, ~€20–29/mnd).** Het is het enige SaaS dat EU-data-residentie *standaard* (Belgisch bedrijf, data in EU) combineert met multi-step, conditionele logica, save-and-resume, file-upload én webhooks — precies de dingen die de kale form mist.
- **Gevoelige velden (Azure subscription-/tenant-ID, API-keys, RBAC) horen NOOIT in een form.** Die lopen out-of-band via Azure Lighthouse / een per-tenant Key Vault met scoped RBAC. Het form vraagt alleen de *toezegging* en *wie het regelt*.
- **AI-versnelling: ja, maar mens-bevestigd, geen autonome chatbot.** Prefill op KvK-nummer (geverifieerde overheidsbron) + website-URL (branding + concept-omschrijving via onze eigen Azure-OpenAI), plus een auto-validatie-pass die de dure config-tegenstrijdigheden afvangt. Elke AI-stap is óf geverifieerd (groen) óf een te-bevestigen concept (grijs).
- **Eigen wizard (output = direct geldige `client-config.json`, gehost in eigen EU-Azure) = het groeipad**, niet de eerste stap. Pas bij ~5+ klanten rechtvaardigt het volume de bouw- en toegankelijkheidsinvestering.

---

## 1. De kwaliteitslat — waarom de kale form niet voldoet

Het probleem is niet smaak. Het zijn drie concrete tekortkomingen, en de derde is een directe geloofwaardigheidsbreuk voor een compliance-first bureau.

**1. Hij doet niets met de data.** De huidige `intake/index.html` heeft geen `<form action>`, geen `fetch/POST`, geen webhook, geen opslag. Iemand vult hem in en de antwoorden verdampen. Dat is geen design-probleem dat je met betere CSS oplost — er zit geen dataflow onder.

**2. Hij behandelt intake als één formulier i.p.v. een proces.** Alle 11 secties (~70 velden) op één pagina is exact het patroon dat afschrikt:
- Forms met >6 vragen halen vaak <50% completion; multi-step met progress-indicator wordt ~53% vaker afgerond; industrie-baseline is dat slechts ~33% van wie begint ook afrondt.
- Een 2-velds form voor een enterprise-AI-traject zou óók fout zijn (te kort = te goedkoop voor een dure dienst). De oplossing is niet inkorten maar **groeperen, uitleggen en conditioneel verbergen**.

**3. Hij vraagt secrets als platte tekst.** Regel 246: `K1. Subscription-ID + Tenant-ID` als gewone tekst-input, plus Owner-rechten en Lighthouse-toegang. Voor een bureau dat AVG/compliance verkoopt is dit het tegenovergestelde van de propositie. Azure-IDs en toegangsgegevens horen niet in een willekeurig formulier.

**Wat "premium/vertrouwenwekkend" hier concreet betekent:**

| Dimensie | Goedkoop voelt | Premium voelt |
|---|---|---|
| Structuur | Eén lange muur van velden | Multi-step wizard met progress + sectienamen (Bedrijf → Merk → Domein → SEO → Leads → Compliance) |
| Per vraag | Kaal label, geen context | De "Waarom we het vragen"-tekst uit `01-client-intake.md` als inline helper ("we vragen je KvK voor het sameAs-blok in je schema-markup") |
| Logica | Alle vragen altijd zichtbaar | Conditioneel: bij `use_existing` vervalt het hele naam/domein-blok, bij `geo_enabled=false` de auteur-sectie |
| Visueel | Dichtgepakt, browser-default, placeholder-als-label | Inter, ruime witruimte, AA-contrast 4.5:1, zichtbare gekoppelde `<label>`s, regellengte 45–85 tekens |
| Toegankelijkheid | `outline:none`, placeholder-only | WCAG 2.2 AA — **sinds 28-6-2025 wettelijk** via de European Accessibility Act. Een ontoegankelijke intake bij een compliance-bureau is een directe geloofwaardigheidsbreuk. |
| Trust-cues | Geen | Bovenaan: "je data staat in de EU; dit formulier vraagt NOOIT wachtwoorden of API-keys — secrets gaan later veilig in Azure Key Vault" |
| Tooling zelf | Form op US-server | Aantoonbaar EU-gehost form + getekende DPA |

Het sterkste premium-signaal voor *onze* niche is niet flair — het is dat we onze eigen AVG-/datalocatie-belofte zichtbaar waarmaken in het formulier zelf.

---

## 2. Aanbevolen aanpak (de kernkeuze)

**Behandel de intake als een gefaseerd proces, en koop voor de eerste klant de UX in via een EU-by-default form-tool (Tally Pro) in plaats van zelf te bouwen.**

Onderbouwing, met de **AVG/EU-residentie-eis als leidend criterium**:

1. **EU-residentie is de splitser, niet design.** Onze hele pitch is "alles in EU-Azure". Een intake op US-servers maakt zin 1 van die pitch vals. Dat schift het veld meteen:
   - **EU-by-default:** Tally (België), Formaloo, Formbricks (DE, self-host).
   - **EU-auto-voor-EU-account:** Jotform (Frankfurt).
   - **US-default, EU achter dure/handmatige tier:** Typeform (mooiste design maar EU pas vanaf ~$199/mnd Growth), Fillout (EU pas vanaf Team-plan), Paperform. → **voor onze niche afgeraden, hoe mooi ook.**
   - **Microsoft Forms valt functioneel af:** externe respondenten kunnen géén bestanden uploaden (logo-upload onmogelijk) en er zijn géén webhooks. Twee harde blockers.

2. **Voor <5 klanten in jaar 1 is zelf bouwen over-engineering (zie C11).** De kale form faalde juist omdat premium + toegankelijk (WCAG 2.2 AA) + save-resume + validatie zelf bouwen veel werk is. Onderschat dat niet opnieuw. Koop nu de ervaring; bouw eigen bij schaal.

3. **Tally levert alle vijf de eisen die de intake nodig heeft:** conditionele logica (gratis), file-upload (logo + auteursfoto), save-and-resume (partial submissions, op Pro), custom domein (`intake.botlease.nl`) + custom CSS om het in BotLease-stijl premium te maken, en webhooks naar onze Azure-Function. Plus het sterkste papieren EU-verhaal van het hele veld.

4. **Gevoelige velden gaan NIET door de form-tool.** Dit is een harde grens, geen detail: subscription-/tenant-ID, API-keys, CRM-credentials en RBAC-delegatie lopen out-of-band (Lighthouse / per-tenant Key Vault, scoped "Key Vault Secrets User"-rol, niet Owner). Het form vraagt alleen wie ze later aanlevert. Maak dit zichtbaar als trust-cue.

**Design-richting:** onze eigen merk-look (Inter, CSS-vars, ruime witruimte, AA-contrast) via custom domein + custom CSS op Tally. Splits de twee zware secties (9 Azure-techniek, 10 Compliance) zo dat je ze met Tijmen erbij doorloopt en de niet-technische eindklant ze niet als muur voor zich krijgt.

---

## 3. Concrete opties met trade-offs

| Tool | Design (out-of-box) | Branding | Conditionele logica | Save/resume | EU-GDPR-hosting | Webhook/integratie | Prijs (juni 2026) |
|---|---|---|---|---|---|---|---|
| **➤ Tally** *(aanbevolen)* | Strak/modern (Notion-achtig); premium met custom CSS | Custom domein + CSS op Pro | Ja, **gratis** | Ja (partial submissions, **Pro**) | **EU-by-default** (BE-bedrijf, data in EU), DPA | Webhooks op **alle** plannen | Gratis / Pro ~€20–29 / Business ~€65–89 |
| **Jotform** | "Form-builder-achtig", iets gedateerd | Veel styling-werk nodig | Sterkste van het veld | Ja (continue later) | EU-Frankfurt **auto voor EU-account** | 100+ integraties + webhooks, DPA | Gratis / Bronze ~$34 / Gold ~$99 |
| **Formaloo** | Minder onderscheidend | OK | Ja | Ja | **EU-by-default**, DPA op enterprise | Ja | $0–$499 (DPA pas enterprise) |
| **Fillout** | Modern, sterk | Goed | Sterke visuele logica | Ja | **US-default**; EU pas vanaf Team-plan + handmatig aanzetten | Webhooks, 30+ integraties | $19 / $49 / $59 / $89 |
| **Typeform** | **Mooiste van het veld** | Sterk | Sterk | Ja | **US-default**; EU pas Growth ~$199+/Enterprise | Ruim | ~$29 / ~$99 / Growth ~$199+ |
| **MS Forms** | Basaal | Geen | Zwak (geen losse vraag, geen AND) | Beperkt | EU Data Boundary, MAAR... | **Geen webhooks**; **geen externe upload** | In M365 |
| **Formbricks** (self-host) | Minder polished | Volledig brandbaar | Ja | Ja | **Zeer sterk** (DE/Frankfurt, AGPLv3, self-host op onze Azure → geen derde verwerker) | Ja | Self-host gratis (alleen Azure-hosting) / cloud ~$49 |
| **Eigen wizard** | **Hoogste** (1-op-1 design-system) | Volledig | Exact op onze 11 secties | Zelf bouwen | **Sterkst** (eigen EU-Azure, geen derde verwerker) | Schrijft **direct** `client-config.json`, geen mapping | Geen licentie; bouwtijd + Azure ~€0–10/mnd |

**Aanbevolen nu:** **Tally Pro.** Beste balans EU-default × features × prijs × time-to-live.
**Alternatief als Tally net niet premium genoeg voelt:** Jotform-EU (feature-rijker) of Formaloo (ook EU-default).
**Groeipad bij ≥5 klanten:** eigen wizard in eigen EU-Azure (sectie 7, optie B).
**Tussenstap als je zero-derde-verwerker wilt zonder volledige zelfbouw:** Formbricks self-hosted op onze Azure.

---

## 4. Het intake-proces (eerste contact → config → bouw)

Vijf fasen. De kern: **feiten in een form, strategie/architectuur in een gesprek, secrets out-of-band.** Per fase wekken we vertrouwen op een andere manier.

**Fase 1 — Kort kwalificatie-form (5–7 velden, ±2 min, async)**
Bedrijf, branche, hosting-voorkeur (eigen Azure ja/nee), grove hardheid EU-eis, tijdlijn, contactpersoon/champion. Multi-step met progress + tijdsindicatie. *Vertrouwen:* het oogt meteen verzorgd en kost de klant niks. Dit kwalificeert vóór we tijd investeren (70% van enterprise-deals stalt door slechte kwalificatie).

**Fase 2 — Scoping-/discovery-call (live)**
De twee architectuur-bepalende vragen uit `01-client-intake.md` Sectie 0: deploy-model (C1: `client_tenant` vs `agency_tenant`) en hardheid EU-inference (C2). Plus de MEDDIC-laag: wie is de economic buyer en wat is het beslisproces achter Tijmen. *Vertrouwen:* één zichtbare eigenaar van het traject (white-glove); strategie hoort in een gesprek, niet in een form (open velden leveren slechte antwoorden).

**Fase 3 — Voorstel + SOW + verwerkersovereenkomst**
Scope, deliverables, acceptatiecriteria, rollen aan beide kanten (de klant levert RBAC/DNS/auteur aan), change control. **De no-overpromise-grenzen expliciet vastleggen** (GEO = citatiekans geen positie; swap/support-taal conform CLAUDE.md). *Vertrouwen:* leg de DPA op tafel vóór de klant erom vraagt — voor een compliance-bureau is dat het sterkste signaal.

**Fase 4 — Tekening + aanbetaling**
BotLease-regel: nooit voorschieten/provisionen vóór getekend + aanbetaald. De Azure-bodemkosten (AI Search/Cosmos draaien 24/7) lopen direct, dus deploy pas ná tekening.

**Fase 5 — Kickoff-call + diepe technische intake (de volle config)**
Pas hier de multi-step EU-form die `client-config.template.json` vult, met:
- per veld de "waarom" uit `01-client-intake.md` als inline helper;
- file-upload voor logo/huisstijl;
- conditionele logica + autosave;
- secties 9 (Azure) + 10 (compliance) doorlopen mét Tijmen, gesplitst van het klant-deel;
- secrets NIET in het form — alleen de toezegging + wie ze in Key Vault zet.
*Vertrouwen:* een verzorgd welcome packet (PDF/Notion) met proces, tijdlijn, contactpersonen en het "jij bezit je eigen Azure"-verhaal; de kickoff is het belangrijkste single event in onboarding (vaste agenda: scope, rollen, cadans, eerste deliverable + eigenaren).

> Scheduling: Cal.com (open-source, EU-self-host) boven Calendly (US). Welcome packet niet in Notion met lead-PII (Notion is US-gehost).

---

## 5. Dataflow & AVG

**Drie gevoeligheidsklassen, drie kanalen:**

| Klasse | Voorbeelden | Kanaal |
|---|---|---|
| Niet-gevoelig | kleuren, niche, keywords, talen | EU-form-tool (Tally) → webhook |
| PII (contact/auteur) | naam, e-mail, foto, LinkedIn, KvK | EU-form-tool + DPA; **personen vragen we aan de klant, niet scrapen** |
| Streng geheim | Azure subscription-/tenant-ID, CRM-API-keys, RBAC-delegatie | **NOOIT in form** — out-of-band naar per-tenant Key Vault, scoped RBAC |

**De pijplijn (niet-gevoelig + PII):**
```
Tally (EU) → webhook (HTTPS POST) → Azure Container App / Function (West Europe, NL-residency)
  → Pydantic-validatie tegen het JSON-schema → Cosmos DB (partition op tenantId, zoals de leads)
  → genereer/patch <tenant>.config.json (alleen kv:-REFERENTIES voor secrets, geen waarden)
```

**JSON Schema = single source of truth.** De config heeft al een `$schema`-veld (draft 2020-12). Definieer de config als Pydantic-model, genereer daaruit zowel de form-validatie als de server-side check. De validatielaag:
- vult de "aanrader"-defaults in;
- dwingt enums af (bv. `deployment_type ∈ {data_zone_standard_eu, global_standard}`);
- **faalt luid** bij een ontbrekende blocker — zodat `onboard.py` (regel 38 `json.load`, regel 435 `--config required`) de config gegarandeerd kan consumeren. Zonder deze laag krijg je een mooie form die toch een onbruikbare config oplevert.

**Mapping-discipline:** leg per form-veld de exacte JSON-pad-mapping vast (bv. veld → `deployment.target`) en valideer de gegenereerde JSON tegen het `$schema` vóór de script-run. Anders ontstaat stille schema-drift.

**AVG-rollen (twee verschillende petten — niet door elkaar halen):**
- **Intake-data zelf** (contact-/bedrijfsgegevens, KvK): BotLease is **verwerkingsverantwoordelijke**. Grondslag = uitvoering overeenkomst / precontractueel (art. 6(1)(b)) of gerechtvaardigd belang (art. 6(1)(f)). → eigen **privacyverklaring** + bewaartermijn.
- **Latere lead-data** (van de klant zijn site): BotLease is **(sub)verwerker** namens de klant. → **verwerkersovereenkomst** bovenop de Microsoft DPA.
- Elke externe form-tool wordt een **sub-verwerker** → teken de Tally-DPA vóór de eerste klant invult. Keten: klant → BotLease → Tally(EU) + Microsoft(EU).

**Bewaren & loggen:**
- Bewaartermijn intake (data-minimalisatie, art. 5(1)(c)): niet-doorgegane intakes na 12–24 mnd anonimiseren/verwijderen; dezelfde verwijder-job die voor leads (`retention_days: 730`) komt kan dit meenemen.
- **Nooit secret-waarden in de intake-store** — alleen `kv:`-referenties (de template doet dit al goed).
- **Consent-/audit-log:** wie ging wanneer akkoord met welke privacyverklaring-versie + DPA-versie + tijdstempel van RBAC-toekenning. De config heeft al `consent_logging: true` voor leads; trek dit door naar de intake.
- Anti-spam op het publieke endpoint: Cloudflare Turnstile (cookieloos, AVG-vriendelijk) + honeypot, **geen reCAPTCHA** (CNIL-kritiek). Webhook binnen ~5s een 200 teruggeven; zware mapping asynchroon.

---

## 6. AI-versnelling (het eigen onderscheid — maar mens-bevestigd)

**Bouw een hybride "AI-versnelde, mens-bevestigde" intake, GEEN autonome chatbot.** ~80% van het premium-effect voor ~20% van de bouwkost, en elke stap is óf geverifieerd óf expliciet een te-bevestigen concept.

**Wat we WEL doen:**

1. **KvK-prefill (geverifieerd, groen).** Eerste scherm vraagt alleen KvK-nummer + website-URL. KvK Basisprofiel-API (~€6,40/mnd + €0,02/call, gratis testomgeving) vult naam/rechtsvorm/adres/SBI-branche. Overheidsbron = geen hallucinatie. Goedkoopste, betrouwbaarste signaal, perfect on-brand.
2. **Brand-prefill (te bevestigen).** Website-URL → Brand-API (Logo.dev gratis voor logo's; Context.dev free-tier voor logo+kleuren+fonts) vult `branding.logo` + `branding.colors`. Bespaart de klant het saaiste deel (hex-codes/SVG). **Altijd visueel bevestigen** — kleuren zitten er soms net naast en worden 1-op-1 de `:root` CSS-vars.
3. **LLM-website-analyse (concept, grijs).** Onze eigen Azure-OpenAI (Data Zone EU, gpt-4.1-mini) analyseert de publieke site en stelt concept-omschrijving, top-diensten, vermoedelijke concurrenten en seed-keywords voor. Sterkste "wij zijn een AI-bureau"-signaal: de klant ziet AI letterlijk aan het werk op zijn eigen bedrijf. Centen per intake, geen extra vendor.
4. **Auto-validatie-pass (hoogste interne ROI).** Een LLM/regel-check op interne tegenstrijdigheden vóór provisioning — precies de dure valkuilen uit `04-data-needed.md`: `zero_data_retention=true` bij `agreement_type=PAYG`, `eu_only_inference` met gpt-5.x (medio 2026 niet als EU-data-zone), `private_networking` met resources in verschillende regio's. Vangt de #1 dure fouten af; puur compliance-versterkend.
5. **Auto-samenvatting + scope-concept (afsluit-wow).** Na invullen: (a) mensentaal-samenvatting van wat we bouwen, (b) scope/offerte-concept (modelkeuze + AI Search-tier + fee-richting o.b.v. budget-cap) **ter controle door Thomas, geen autoverzending**, (c) de `client-config.json` zelf. Proposal-draften van ~6u naar <1u.

**Harde scheiding tegen hallucinatie (reasoning-modellen halluceren tot ~48%):** geverifieerde bron = bevestigd/groen; LLM-gok = grijs concept met verplicht "controleer dit"-vinkje. Nooit een LLM-geraden KvK-nummer, adres of juridische tekst als feit.

**Wat we bewust NIET doen (gimmicks/risico):**
- Geen volledig autonome AI-chat die óók de compliance/technische secties (0, 9, 10) voert — die vereisen expertise-dialoog met Thomas/Tijmen; een bot maakt ze oppervlakkig en riskeert de dure architectuurkeuzes verkeerd vast te leggen.
- Geen chatbot die eerst om e-mail/demo vraagt vóór hij waarde levert (klassiek B2B-anti-patroon).
- Geen PERSOONsgegevens scrapen (auteur/contact) — die vragen we aan de klant: netter, AVG-veiliger, on-brand. Research alleen het BEDRIJF.
- Geen echte Foundry conversational agent bij <5 klanten (over-engineering, C11).

---

## 7. Aanbevolen volgende stap (kies één)

**Optie A — Tally Pro deze week live (AANBEVOLEN voor klant 1)**
EU-by-default form-tool, custom domein `intake.botlease.nl` + custom CSS in BotLease-stijl. Webhook → kleine Azure Container App (West Europe) → Pydantic-validatie → `client-config.json`. Teken de Tally-DPA. Secrets out-of-band via Key Vault.
- *Kosten:* ~€20–29/mnd + Azure ~€0 binnen free grant. *Bouwtijd:* 1–2 dagen (vooral webhook + mapping + validatie).
- *Voor:* snelste time-to-live, EU-papieren op orde, geen zelfbouw-onderhoud.
- *Tegen:* externe sub-verwerker (DPA verplicht); output mappen naar config; styling-tijd voor echt premium.

**Optie B — Zelf bouwen in de Azure-stack (groeipad bij ≥5 klanten)**
Eigen wizard (Next.js/React of Azure Static Web App + Function) op `intake.botlease.nl`, 1-op-1 BotLease design-system, schrijft **direct** geldige `client-config.json`, JSON Schema als single source of truth, alles in eigen EU-Azure.
- *Kosten:* geen licentie; SWA ~€9/mnd + Functions ~€0. *Bouwtijd:* 1–2 weken voor een nette, toegankelijke wizard.
- *Voor:* hoogste premium-uitstraling, end-to-end EU-residentie (geen derde verwerker), geen mapping-stap, "zelfs onze intake draait in eigen EU-Azure" = verkoopargument.
- *Tegen:* meeste bouw + onderhoud (a11y/security op ons); over-engineering bij <5 klanten.

**Optie C — Tussenstap: Formbricks self-hosted op onze Azure**
Zero-derde-verwerker zonder volledige zelfbouw (AGPLv3, DE/Frankfurt, Docker op onze Azure).
- *Kosten:* software gratis, alleen Azure-hosting + ops-tijd.
- *Voor:* sterk compliance-verhaal, geen extra DPA. *Tegen:* infra-onderhoud + branding-pass op ons; minder polished out-of-box.

### Mijn voorkeur
**Begin met Optie A (Tally Pro) voor de Tijmen/IT Connect-pilot, en zet Optie B op de roadmap zodra klant 2–3 in zicht is.** Reden: de eerste klant heeft snelheid en een waterdicht EU-verhaal nodig, niet de marge-investering van een eigen wizard. Tally levert beide vandaag. De directe `client-config.json`-write en het sterkste compliance-verhaal (eigen wizard) verdienen zich pas terug bij volume — precies de C11-logica.

**Ongeacht de keuze, doe deze week eerst dit (los van de tool):**
1. Verwijder het Subscription-/Tenant-ID-tekstveld (regel 246) uit de huidige form. Het is een beveiligingsfout zolang het bestaat.
2. Verplaats secrets naar het out-of-band Key Vault-pad (toezegging + wie regelt het).
3. Splits de 11 secties in een kort kwalificatie-deel (fase 1) en een diepe intake (fase 5).
4. Hergebruik de "Waarom we het vragen"-kolom uit `01-client-intake.md` als inline microcopy — die hebben we al, gratis vertrouwens-hefboom.

---

*Bestand: `/Users/werk/Documents/Python/botlease.nl/Projecten/x/06-intake-aanpak.md`. Verifieer KvK-, Brand-API-, form-tool- en Azure-prijzen + de EU-data-zone-modellijst opnieuw vlak vóór elke offerte; cijfers hier zijn stand juni 2026.*
