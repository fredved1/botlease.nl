# PROJECT X — Client Intake

> Intake-vragenlijst voor elke nieuwe klant van het "AI-marketingbureau in een doos".
> Doel: alle antwoorden vullen straks de `client-config.template.json` die het opzet-script consumeert.
> Eén keer netjes invullen = één keer een script draaien = klant live.

**Toon van dit document:** eerlijk en concreet. Waar iets nog niet 100% zeker is in 2026 (Azure Foundry verandert snel), staat dat er expliciet bij. We beloven geen dingen die we niet hard kunnen maken (geen gegarandeerde AI-citaties, geen "data wordt nooit bewaard" zonder dat de juiste Azure-knop bevestigd is).

**Hoe te gebruiken:** loop de secties met de klant (en Tijmen) door. Per vraag staat *waarom* we het nodig hebben, zodat de klant snapt dat we niet zomaar gegevens verzamelen. Markeer per antwoord of het een harde eis, een voorkeur, of "weet ik niet" is.

---

## 0. Allereerst: het deploy-model (bepaalt bijna alles erna)

Dit is de belangrijkste vraag van de hele intake. Het bepaalt de kostenstructuur, wie de Azure-rekening betaalt, en welke compliance-garanties we kunnen geven.

| # | Vraag | Waarom we het vragen |
|---|---|---|
| 0.1 | **Moet alles draaien in de EIGEN Azure-tenant/subscription van de klant, of mag het in een door ons beheerde Azure-omgeving (EU) draaien?** | Dit is de splitsing tussen twee totaal verschillende architecturen. Tijmens klant eist waarschijnlijk "alles in zijn eigen Azure". Dan rollen we uit via een **Azure Managed Application** in zíjn subscription (data blijft bij hem, wij beheren via een identity in onze tenant). Mag het in onze omgeving, dan kunnen we resources delen tussen klanten = veel goedkoper. |
| 0.2 | **Wie betaalt het Azure-verbruik?** De klant rechtstreeks (eigen abonnement) of factureren wij door? | Bepaalt ons prijsmodel: setup-fee + maandelijkse beheer/AI-fee (klant draagt Azure zelf) vs. all-in maandbedrag (wij dragen Azure en rekenen door). |
| 0.3 | **Heeft de klant een Enterprise Agreement (EA) of Microsoft Customer Agreement (MCA), of een gewone pay-as-you-go subscription?** | Cruciaal voor compliance: **Zero Data Retention (ZDR)** bij Azure OpenAI is alléén beschikbaar op EA/MCA, NIET op pure pay-as-you-go. Bepaalt ook of we via Marketplace of via private service catalog uitrollen. |
| 0.4 | **Mogen wij beheertoegang krijgen via Azure Lighthouse / een service principal?** Zo ja: welke minimale rollen op welke resource group? | We willen één control plane over alle klant-Azures. We vragen least-privilege (alleen wat nodig is), niet "Owner" op de hele subscription. Security-bewuste klanten haken anders af. |
| 0.5 | Bestaat er al een interne Azure-landing-zone / Azure Policy die regio's of public access beperkt? | Dan sluiten we daarop aan in plaats van eigen policies te forceren. |

---

## 1. Bedrijfsinformatie (basis-identiteit)

| # | Vraag | Waarom |
|---|---|---|
| 1.1 | Officiële bedrijfsnaam + handelsnaam(en) | Voor merk, schema-markup en de juridische velden in mails. |
| 1.2 | KvK-nummer (of buitenlands equivalent) | Voor het `sameAs`-blok in het Organization-schema (entity-laag = hoogste GEO-ROI). |
| 1.3 | Vestigingsadres + land | LocalBusiness-schema en regio-bepaling. |
| 1.4 | Korte bedrijfsomschrijving in 2-3 zinnen (in eigen woorden) | Seed voor de niche-/positioneringsbepaling door het LLM. |
| 1.5 | Bestaande website-URL (indien aanwezig) | Om bestaande content/keywords/concurrenten af te leiden en niet vanaf nul te beginnen. |
| 1.6 | Bestaande socials + profielen (LinkedIn, eventueel Crunchbase, G2, Wikidata-QID) | Voor `sameAs` in het schema + de entity-fundering (knowledge-graph). |

---

## 2. Branche, niche & doelgroep

| # | Vraag | Waarom |
|---|---|---|
| 2.1 | In welke branche/sector zit het bedrijf? | Stuurt keyword-onderzoek, content-toon en bepaalt of het een **YMYL-sector** is (finance/zorg) — dan is menselijke eindcontrole op content verplicht. |
| 2.2 | Wie is de ideale klant/doelgroep (B2B/B2C, functietitels, bedrijfsgrootte)? | Voedt de positionering, de toon van de content en het kwalificatie-rubriek van de sales-agent. |
| 2.3 | Wie zijn de 3-5 belangrijkste concurrenten (URL's)? | DataForSEO Labs doet hierop een keyword-gap-analyse: welke keywords ranken concurrenten waar de klant nog niet rankt. |
| 2.4 | Welke producten/diensten wil je actief promoten (top 5)? | Worden de pijler-pagina's en de seed-keywords. |
| 2.5 | Welke regio('s)/markt(en) bedien je? (bv. NL-only, NL+BE, NL+BE+DE) | Bepaalt taal- en locatie-parameters in de keyword-API's én de domein-TLD-set (.nl/.be/.de/.com). |
| 2.6 | In welke talen moet de content en de site? | Bepaalt of we per taal een aparte content-pijplijn + sitemap nodig hebben. |

---

## 3. Merk, huisstijl & assets

> Dit is de directe input voor de site-generator. De generator is CSS-variabele-gebaseerd, dus kleuren + logo + naam injecteren levert direct een eigen merk-look (geen herontwerp nodig).

| # | Vraag | Waarom |
|---|---|---|
| 3.1 | Logo als **SVG** (en eventueel PNG-fallback) | Brandmark in nav + footer + Organization-schema. SVG schaalt scherp op elk scherm. |
| 3.2 | Merkkleuren als hex-codes: primair/accent, achtergrond, kaart-achtergrond, tekst | Worden direct de `:root` CSS-variabelen in de site-template. |
| 3.3 | Voorkeursfont (of "kies iets passends") | Default is een nette web-safe stack; merkfont kan op verzoek. |
| 3.4 | Tone of voice: formeel/informeel, jij/u, voorbeeldzinnen die "klinken als ons" | Stuurt de content-agent + de humanizer-pass (geen AI-toon, geen lange streepjes). |
| 3.5 | Bestaande beeldbank / stockfoto's, of mogen we AI-hero-beelden genereren per artikel? | Bepaalt of we `gpt-image-1` inzetten (~$0,005-$0,25/beeld). **Let op:** EU/DE AI-label-plicht (2026) kan een "AI-generated"-credit vereisen bij gegenereerd beeld. |
| 3.6 | Verplichte juridische teksten (algemene voorwaarden, privacyverklaring, KvK/BTW in footer) | Moeten in de footer/op de site; ook nodig voor consent-logging en de AVG-paragraaf. |

---

## 4. Domeinnaam & DNS

| # | Vraag | Waarom |
|---|---|---|
| 4.1 | Heb je al een domein, of moeten we er één zoeken/registreren? | Bepaalt of we de availability-check + registratie-stap draaien of het bestaande domein koppelen. |
| 4.2 | Zo ja: welk domein + bij welke registrar staat het (TransIP, GoDaddy, Namecheap, Cloudflare …)? | Bepaalt waar we DNS-records (SPF/DKIM/DMARC voor mail, custom domain voor de site) moeten zetten. |
| 4.3 | Zo nee: gewenste TLD's en eventuele naam-ideeën | Het LLM genereert een shortlist; we checken beschikbaarheid (WhoisJSON/WhoisFreaks) en registreren via Cloudflare Registrar (wholesale, geen markup). Elke naam checken we óók tegen merkrechten (EUIPO) vóór registratie. |
| 4.4 | **Wie wordt eigenaar/registrant van het domein — de klant of het bureau?** | Bepaalt of we centraal (bureau bezit) of op naam van de klant registreren. Belangrijk juridisch + bij offboarding. |
| 4.5 | Wie beheert de DNS en kan records toevoegen? | Nodig vóór oplevering: zonder correcte SPF/DKIM/DMARC belanden de auto-reply-mails in spam. |

---

## 5. SEO & GEO (AI-citatie)

| # | Vraag | Waarom |
|---|---|---|
| 5.1 | Belangrijkste zoektermen waarop je gevonden wilt worden (5-15) | Seed-keywords; we breiden uit via DataForSEO en valideren op echte zoekvolumes. |
| 5.2 | Is GEO/AI-citatie (zichtbaarheid in ChatGPT/Perplexity/Gemini) gewenst als onderdeel of als add-on? | GEO is een los verkoopbare laag (DataForSEO AI Optimization). **Eerlijk:** we maximaliseren citatie-KANS (answer-capsules, schema, freshness, llms.txt) maar kunnen geen positie garanderen. |
| 5.3 | Wie wordt de **zichtbare auteur** van de content (echte persoon bij de klant)? Naam, functie, korte bio, foto, profiel-URL's | E-E-A-T is bijna verplicht: 96% van AI-Overview-citaties komt van bronnen met named author + Person-schema. Een echte persoon weegt veel zwaarder dan "Organization" of "AI". |
| 5.4 | Mogen we een Wikidata-entry voor het bedrijf aanmaken? | Hoogste ROI per uur voor knowledge-graph-zichtbaarheid; Wikidata heeft geen notability-drempel. |
| 5.5 | Heb je al Google Search Console / Bing Webmaster Tools ingericht? | Nodig voor indexatie-monitoring (Google) en IndexNow (Bing → ook ChatGPT). |

---

## 6. Content / blog-pijplijn

| # | Vraag | Waarom |
|---|---|---|
| 6.1 | **Nieuws** (feed-gedreven, reageren op de actualiteit) of **evergreen blogs** (keyword/onderwerp-gedreven) — of beide? | Bepaalt of we RSS-feeds dan wel "Grounding with Bing Search" als research-bron nemen. |
| 6.2 | Welke onderwerpen/feeds zijn relevant? | Vult de research-input van de content-agent. |
| 6.3 | Gewenste publicatiecadans (bv. wekelijks 2-3 artikelen) | We adviseren een lage, constante cadans — massa AI-content wordt door Google afgestraft (scaled content abuse). Volume is de val, niet AI op zich. |
| 6.4 | **Wil je een mens-in-de-lus goedkeuring vóór publicatie?** (zeker bij start of YMYL-sector) | Bij gevoelige sectoren vanaf 2026 verplicht. We bouwen dan een approval-stap (Teams-kaart of mail) in. |
| 6.5 | Publicatie-doel: nieuwe Azure-site, of een bestaand CMS van de klant (WordPress/Webflow) via API? | Bepaalt of we naar Azure Static Web Apps publiceren of naar een extern CMS pushen. |

---

## 7. Inbound leads: afvangen, beantwoorden, kwalificeren, doorzetten

| # | Vraag | Waarom |
|---|---|---|
| 7.1 | Welke kanalen: contactformulier, AI-chatwidget, of beide? | We adviseren altijd beide: het formulier vangt wie niet wil chatten, de chat wie snel antwoord wil. |
| 7.2 | **Mag de AI-chatbot autonoom antwoorden, of altijd met mens-in-de-lus?** | Bepaalt de agent-architectuur én het AI-Act-risicoprofiel. (BotLease-regel: geen autonome koude mails.) |
| 7.3 | Welk kwalificatie-rubriek? Klassiek BANT (Budget/Authority/Need/Timeline) of branche-specifieke criteria? | Dit is de per-tenant config die het kwalificatie-script draagbaar maakt; de agent levert een JSON-score 0-100 + qualified ja/nee. |
| 7.4 | Vanaf welke score moet een lead worden doorgezet? | De drempel waarboven we routeren naar de klant. |
| 7.5 | **Lead-routing-bestemming:** e-mail, Microsoft Teams (Accept/Reject-kaart), of direct in een CRM? | Bepaalt of we Logic Apps + Teams-connector nodig hebben of alleen een mail/CRM-write. Per tenant configureerbaar. |
| 7.6 | Afzenderdomein voor de automatische e-mails (via Azure Communication Services) | Per tenant een geverifieerd domein met SPF/DKIM/DMARC, anders deliverability-problemen. |
| 7.7 | Gewenste bewaartermijn voor leads (default marketing: max ~2 jaar na laatste contact zonder toestemming) | We bouwen een automatische verwijder-/anonimiseer-job in (AVG). |

---

## 8. Bestaande systemen & CRM

| # | Vraag | Waarom |
|---|---|---|
| 8.1 | Welk CRM gebruikt de klant — Dynamics 365, HubSpot, Pipedrive, anders, of niets? | Bepaalt de routing-bestemming. Microsoft-klant → Dynamics (native). Niet-Microsoft → HubSpot/Pipedrive via REST-API/webhook vanuit een Function. |
| 8.2 | Welke API-keys/toegang heeft de klant voor dat CRM, en wie levert die aan? | Komen in Azure Key Vault (nooit in code/repo). |
| 8.3 | Gebruikt de klant Microsoft Teams (voor lead-notificaties)? | Bepaalt of Adaptive Cards in Teams een optie is. |
| 8.4 | Heeft de klant al een Google Ads-account (voor keyword-data) en/of analytics? | We gebruiken DataForSEO als wrapper rond Google Ads-data (minder gedoe). Analytics draaien we cookieloos via self-hosted Umami (geen consent-banner nodig). |
| 8.5 | Welke andere downstream-systemen moet een gekwalificeerde lead raken? | Bepaalt welke function-tools/MCP-servers/OBO-auth we moeten bouwen. |

---

## 9. Azure-tenant, toegang & techniek

| # | Vraag | Waarom |
|---|---|---|
| 9.1 | Subscription-ID + tenant-ID waar we uitrollen | Doel van de Bicep/Managed-App-deploy. |
| 9.2 | **Verplichte EU-regio:** West Europe (Amsterdam, NL) of North Europe (Ierland)? | Klant kan om NL-residency vragen → dan West Europe pinnen. Let op: bij VNet/private networking moeten álle resources in dezelfde regio. |
| 9.3 | Wie heeft Owner / User Access Administrator om de RBAC-rollen toe te kennen tijdens provisioning? | Nodig om Managed Identity de juiste rollen op Cosmos/Storage/Search te geven. |
| 9.4 | Is **private networking (VNet + private endpoints)** een eis of nice-to-have? | Sterk compliance-argument, maar verhoogt complexiteit en geeft regio-lock. |
| 9.5 | Mogen externe SaaS-API's (DataForSEO, domein-checks, IndexNow, Wikidata) aangeroepen worden, of moet ALLES strikt binnen Azure blijven? | Sommige diensten zijn per definitie extern. We sturen daar alléén niet-persoonsgebonden data heen (keywords, domeinen) — geen lead-PII. Leg dit vast met een DPA. |

---

## 10. Compliance & AVG/AI Act

| # | Vraag | Waarom |
|---|---|---|
| 10.1 | Hoe hard is de EU-only-eis? **Data-at-rest in EU** (makkelijk) vs. **EU-only-INFERENCE** (vereist Data Zone Standard EU, beperkt de modelkeuze)? | Dit is de #1 valkuil. "Global Standard" geeft GEEN EU-inference-garantie ook al staat de resource in de EU. EU-only-inference → pin op GPT-4o/GPT-4.1 (Data Zone EU); de nieuwste GPT-5.x is medio 2026 nog niet als EU-data-zone beschikbaar. |
| 10.2 | Wil de klant **Modified Abuse Monitoring** (geen human review van prompts) en/of **Zero Data Retention**? | Standaard logt Azure OpenAI prompts/completions ~30 dagen. ZDR vereist EA/MCA (zie 0.3). Beloof "AI leest niet mee / data wordt niet bewaard" pas ná bevestiging dat het traject aangevraagd kan worden. |
| 10.3 | Wie is verwerkingsverantwoordelijke en wie verwerker? | Het bureau is vermoedelijk (sub)verwerker namens de klant → er is een verwerkersovereenkomst nodig tussen bureau en klant, bóvenop de Microsoft DPA. |
| 10.4 | Akkoord met de verplichte **AI-disclosure** in de chatbot ("Je praat met een AI-assistent") + consent-logging? | EU AI Act Art. 50 (transparantieplicht) treedt aug 2026 in werking, boetes tot 35M euro / 7% omzet. Dit is een niet-uitschakelbaar, ingebouwd onderdeel van elke tenant-deploy. |
| 10.5 | Welk privacy-statement/consent-tekst ziet de lead, en moet dat per kanaal gelogd worden? | Voor het aantonen van rechtmatigheid bij de AP slaan we per lead op welke consent is gegeven en wanneer. |

---

## 11. Commercieel (intern, niet per se met klant te delen)

| # | Vraag | Waarom |
|---|---|---|
| 11.1 | Budget-plafond per maand (model-tokens + tools + vaste Azure-lasten)? | Bepaalt modelkeuze (GPT-4.1-mini bulk vs. groter model), of we Azure AI Search ($75-$250/mnd) inzetten of goedkopere vector-opslag, en hoeveel Grounding-with-Bing (~$35/1000 queries) verantwoord is. |
| 11.2 | Setup-fee (de "script-run" + intake) + maandelijkse beheer/AI-fee, of all-in SaaS-prijs? | Markt-benchmark: white-label agency-in-a-box ~$497/mnd; AI-marketingbureaus mid-market $5K-$25K/mnd. Onze Azure-in-eigen-tenant-enterprise-propositie zit aan de bovenkant. |
| 11.3 | Verwachte aantal klanten in jaar 1? | Onder ~5 klanten is volledige multi-tenant-automatisering mogelijk over-engineering; dan volstaat een half-handmatig script. |

---

## Bekende onzekerheden (medio 2026 — verifiëren op deploy-moment)

- **Azure Foundry verandert snel.** "Azure AI Foundry" heet inmiddels vaak "Microsoft Foundry"; SDK's, tool-prijzen en memory-billing wijzigen. Verifieer de live pricing-pagina vlak vóór elke offerte.
- **EU-model-lag.** GPT-5.x is medio 2026 nog NIET als Data Zone Standard in EU-regio's beschikbaar (wel als Global Standard). Harde EU-inference-eis = beperkt tot GPT-4o/GPT-4.1.
- **Claude-via-Foundry** valt medio 2026 nog NIET onder de EU Data Boundary. Voor een harde EU-eis: Azure-OpenAI/Azure-direct modellen, geen Claude-via-Foundry (tenzij EU-native deployment inmiddels live is — checken).
- **Hosted Agents + memory + serverless-agents-runtime** zijn (deels) preview en de billing start in 2026. Bouw productie-kritische flows liever op GA-componenten (Prompt agents + Responses API).
- **Vaste bodemkost per tenant.** AI Search Basic/S1 + Cosmos RU/s draaien 24/7, ook zonder verkeer. Bij veel kleine klanten eet dit de marge — overweeg gedeelde resources waar de klant dat compliance-technisch toestaat (botst met "alles in eigen tenant").
