# PROJECT X — Wat moet je aanleveren? (checklist vóór bouwen + eerste klant)

> Doel van dit bestand: één afvinklijst van **alles wat geregeld moet zijn** voordat de blauwdruk gebouwd kan worden en de eerste klant (via Tijmen, IT Connect Almelo) live kan.
> Per item staat een **[BLOCKER MVP]** of **[later]**-tag. Een blocker = je kunt zonder dit géén werkende MVP voor de eerste klant opleveren.
>
> Lezerspubliek: Thomas (bouwer) + Tijmen (klant-kant). Toon: concreet, geen overpromise. Waar een prijs/feit uit het onderzoek komt staat dat erbij; **onzekerheden zijn expliciet als ⚠️ gemarkeerd** en moeten geverifieerd worden vóór een offerte.

---

## Allereerst: de twee vragen die ALLES bepalen

Deze twee beslissingen zitten vóór de hele checklist. Zolang ze niet beantwoord zijn, weet je niet welke andere items blockers zijn.

1. **Waar draait het? (hosting-model)** — Tijmens harde eis is "alles in zijn eigen omgeving (zeer waarschijnlijk Azure)". Dat betekent het **klant-tenant-model** (Azure Managed Application + optioneel Lighthouse-delegatie). Maar bevestig of het écht zijn eigen subscription moet zijn, of dat "een door jou beheerde Azure-omgeving in de EU" ook mag. Dit bepaalt wie de Azure-rekening betaalt en de hele kostenstructuur.
2. **Hoe hard is de EU-eis? (datalocatie)** — Twee niveaus: (a) data-at-rest-in-EU (makkelijk, "Global Standard"-deployment volstaat) vs. (b) EU-only-**inference** (vereist "Data Zone Standard (EU)"-deployment en beperkt de modelkeuze tot GPT-4o / GPT-4.1; GPT-5.x is medio 2026 nog NIET als Data Zone in EU beschikbaar). Voor een NL-klant is (b) waarschijnlijk de eis.

> Zie **sectie C** voor de volledige beslissingenlijst. De rest van dit document gaat uit van het meest waarschijnlijke scenario: **klant-tenant + EU-only-inference**.

---

## (a) Van Tijmen / de klant aan te leveren

### A1. Azure-tenant + toegang/rollen
- [ ] **[BLOCKER MVP]** Bevestiging dat er een **Azure-subscription + Entra ID-tenant** is om in te deployen (en welke: de eigen tenant van de klant of een door Thomas beheerde EU-omgeving).
- [ ] **[BLOCKER MVP]** Iemand met **Owner óf User Access Administrator**-rechten op de subscription/resource group — nodig om tijdens provisioning de **RBAC-rollen** toe te kennen (anders faalt de Bicep-deploy van de standard agent setup).
  - Concreet toe te kennen rollen aan de Foundry-project managed identity: *Cosmos DB Operator*, *Storage Account Contributor*, *Search Index Data Contributor* + *Search Service Contributor*, *Storage Blob Data Owner/Contributor*, en *Cosmos DB Built-in Data Contributor* op database `enterprise_memory`. Developers krijgen rol *Foundry User* (oude naam: Azure AI User).
- [ ] **[BLOCKER MVP]** Afspraak over **beheertoegang voor Thomas**: via Azure Lighthouse-delegatie of een service principal in Thomas' tenant, met **least-privilege** (alleen de minimale rollen op de juiste resource group — géén "Owner" op de hele subscription; security-bewuste klanten haken daar op af).
- [ ] **[BLOCKER MVP]** **Type contract** bij Microsoft: heeft de klant een **Enterprise Agreement (EA) of Microsoft Customer Agreement (MCA)**, of pure pay-as-you-go? Dit bepaalt of *Zero Data Retention* haalbaar is (zie A6) én of de Managed Application via Marketplace of via private "service catalog" moet.
- [ ] **[later]** Bevestiging of er een interne **Azure-Policy / landing-zone** is die regio's of public access al beperkt (daar moet de template op aansluiten).

### A2. Domein / registrar
- [ ] **[BLOCKER MVP]** **Wie wordt domein-eigenaar/registrant** — de klant zelf, of het bureau? Dit bepaalt of je via Cloudflare (centraal) of via de klant-registrar registreert.
- [ ] **[BLOCKER MVP]** **DNS-beheertoegang** voor het te gebruiken domein — nodig om:
  - de website-CNAME naar Azure Static Web Apps te zetten;
  - **SPF / DKIM / DMARC** in te richten voor Azure Communication Services Email (zonder dit belanden auto-replies in spam; ACS dwingt domeinverificatie af, dus dit moet vóór oplevering).
- [ ] **[later]** Welke **registrar gebruikt de klant al** (TransIP / GoDaddy / Namecheap)? Bepaalt of we via Cloudflare Registrar registreren of de bestaande registrar koppelen.
- [ ] **[later]** Landen/talen-scope (NL-only vs NL+BE+DE) → bepaalt de TLD-set (.nl/.be/.com) en de taal-parameters in de keyword-API's.

### A3. Merk / huisstijl / content
- [ ] **[BLOCKER MVP]** **Logo** (bij voorkeur SVG) en **merkkleuren** (hex-codes) → worden geïnjecteerd in de `:root` CSS-variabelen van de generator (theming per merk werkt al via CSS-vars in `style_base.py`).
- [ ] **[BLOCKER MVP]** **Bedrijfsnaam, slogan/positionering, kernboodschap** en bestaande **website-content/teksten** (voor zover aanwezig) als input voor de generator-config (`config.json`/ENV per tenant).
- [ ] **[later]** Beeldbank/keuze: AI-gegenereerde hero-beelden per artikel (Azure OpenAI `gpt-image-1`, ~$0,011–$0,25/beeld) **óf** eigen/gelicenseerde stock van de klant. Let op een mogelijke **AI-beeld-labelplicht** (EU/DE 2026) → desnoods "AI-generated"-credit toevoegen.

### A4. Bedrijfs-/SEO-info (input voor onderzoek + content)
- [ ] **[BLOCKER MVP]** **Niche / branche + belangrijkste diensten/producten** → input voor de domein-/niche-/keyword-onderzoeksstap.
- [ ] **[BLOCKER MVP]** **De zichtbare auteur (E-E-A-T)**: een **echte persoon** bij het klant-bedrijf met naam, functie, foto, korte bio en profiel-URL's (LinkedIn etc.) voor het Person-schema + `/auteur/<slug>`-pagina. Dit is de #1 E-E-A-T-/GEO-hefboom; een generieke "AI"- of Org-auteur verzwakt citaties sterk.
- [ ] **[later]** **Bedrijfs-identiteit voor de entity-laag**: KvK-nummer, eventuele bestaande LinkedIn/Crunchbase/G2-profielen → voor het Organization-schema met `sameAs` en (optioneel) een Wikidata-entry.
- [ ] **[later]** Bestaande **concurrenten** (als de klant ze kent) → versnelt de keyword-gap-analyse.

### A5. Lead-bestemming (waar gaat een gekwalificeerde lead heen?)
- [ ] **[BLOCKER MVP]** **Welk CRM/kanaal** moet de gekwalificeerde lead ontvangen?
  - Microsoft-klant → Dynamics 365 (native) of Dataverse.
  - Niet-Microsoft → HubSpot / Pipedrive via REST-API/webhook.
  - Of simpelweg **e-mail** (ACS) en/of **Microsoft Teams** (Adaptive Card met Accept/Reject).
  - Per tenant is dit een config-keuze (`target = email | teams | dynamics | hubspot`).
- [ ] **[BLOCKER MVP]** **Notificatie-e-mailadres(sen)** waar nieuwe gekwalificeerde leads naartoe gemaild worden.
- [ ] **[BLOCKER MVP]** **Kwalificatie-rubriek**: klassiek BANT (Budget/Authority/Need/Timeline) of branche-specifieke criteria? Dit is de per-tenant config die bepaalt wanneer een lead "qualified" is en doorgezet wordt.
- [ ] **[BLOCKER MVP]** Beslissing: **autonoom doorzetten** boven de score-drempel, of altijd **human-in-the-loop** (Teams Accept/Reject) vóór doorzet? (Sluit aan bij BotLease-regel "geen autonome koude mails"; mens-in-de-lus voorkomt dat goede leads onterecht worden weggegooid.)

### A6. Akkoord AVG / verwerkersovereenkomst + AI Act
- [ ] **[BLOCKER MVP]** **Verwerkersovereenkomst tussen bureau en klant.** Rolverdeling: de klant is vermoedelijk **verwerkingsverantwoordelijke**, het bureau (sub-)verwerker. Dit komt **bovenop** de Microsoft DPA. Thomas moet een template aanleveren/laten opstellen.
- [ ] **[BLOCKER MVP]** Akkoord op de **datalocatie-keuze** (EU Data Zone) en welk **model + deployment-type** per klant wordt vastgelegd (zie sectie C).
- [ ] **[BLOCKER MVP]** **EU AI Act Art. 50** (transparantieplicht, in werking aug 2026): de sales-chatbot **moet** bij eerste interactie melden dat het AI is. Bouw "Ik ben een AI-assistent"-disclosure + **consent-logging** standaard, niet-uitschakelbaar, in elke tenant-deploy. Boetes tot €35M of 7% omzet.
- [ ] **[BLOCKER MVP]** **Consent-logging**-veld bij elke lead (welk privacy-statement zag de lead, wanneer) → nodig om rechtmatigheid van verwerking aan te kunnen tonen bij de AP.
- [ ] **[later]** **Bewaartermijn** voor leads (marketing-default vaak max ~2 jaar na laatste contact zonder toestemming) → in te bouwen als automatische verwijder-/anonimiseer-job in Cosmos/Functions.
- [ ] **[later, afhankelijk van EA/MCA]** Aanvraag **Modified Abuse Monitoring** (geen human review) en/of **Zero Data Retention** via Microsoft's Limited Access-programma. ⚠️ **ZDR vereist EA/MCA — NIET beschikbaar op pure pay-as-you-go.** Beloof "AI leest niet mee / data wordt niet bewaard" pas ná bevestiging dat de klant-tenant dit traject kan aanvragen.

---

## (b) Accounts / API-keys die nodig zijn

> Vuistregel: **persoonsgegevens (lead-namen/e-mails/gesprekken) blijven STRIKT binnen Azure-EU.** Externe SaaS-API's (DataForSEO, domein-checks) krijgen alléén niet-persoonsgebonden queries (zoekwoorden, branchetermen, domeinnamen). Leg dit vast; sluit waar nodig een DPA met die leverancier.

### B1. Azure / Microsoft (in de klant-tenant)
- [ ] **[BLOCKER MVP]** **Microsoft Foundry** (voorheen Azure AI Foundry) — resource + project met **standard agent setup** (capability hosts → BYO Cosmos DB, Storage, AI Search, Key Vault). Agent-runtime zelf gratis; je betaalt model-tokens + tool-usage.
- [ ] **[BLOCKER MVP]** **Azure OpenAI / Foundry Models** — model-deployment (advies: **GPT-4.1-mini** als werkpaard, ~$0,40 in / $1,60 out per 1M tokens; GPT-4.1 voor zwaardere taken) als **Data Zone Standard (EU)** in een EU-regio.
- [ ] **[BLOCKER MVP]** **Azure Static Web Apps** (Standard ~$9/site/mnd — met SLA; Free heeft géén SLA en is alleen voor demo) voor de marketingsite.
- [ ] **[BLOCKER MVP]** **Azure Container Apps** (Consumption, scale-to-zero) voor het kleine API-servertje. Gratis grant: 180k vCPU-sec + 360k GiB-sec + 2M requests/mnd → kleine API vaak €0.
- [ ] **[BLOCKER MVP]** **Azure Functions** (Consumption/Flex) voor webhooks (lead-intake, mail-parser) + timer-triggers (wekelijkse blog-publish, IndexNow-ping, rank-check). ⚠️ Zet `WEBSITE_TIME_ZONE='W. Europe Standard Time'` — cron is default UTC.
- [ ] **[BLOCKER MVP]** **Azure Cosmos DB for NoSQL** — thread/gesprek-opslag (standard agent setup vereist **min. 3000 RU/s** per project, anders `CapabilityHostProvisioningFailed`) + lead-opslag (partitioneer op `tenantId`).
- [ ] **[BLOCKER MVP]** **Azure Storage** — geüploade files + embeddings/chunks (BYO voor standard agent setup).
- [ ] **[BLOCKER MVP]** **Azure AI Search** — vector store / RAG-kennisbank. ⚠️ **Vaste maandbodem**: Free $0 (alleen dev), Basic ~$75/mnd, S1 ~$250/mnd. Reken dit per tenant door.
- [ ] **[BLOCKER MVP]** **Azure Key Vault** — alle secrets (geen keys in code/repo, sluit aan op CLAUDE.md-regel).
- [ ] **[BLOCKER MVP]** **Entra ID + Managed Identity** — keyless auth (in productie de specifieke `ManagedIdentityCredential`, niet `DefaultAzureCredential`).
- [ ] **[BLOCKER MVP]** **Azure Communication Services — Email** — auto-reply + lead-notificatie. ~$0,00025/e-mail + $0,00012/MB (3.000 mails ≈ $0,75/mnd). Vereist geverifieerd afzenderdomein per tenant (zie A2).
- [ ] **[later]** **Application Insights** — tracing + **alert bij "0 artikelen gepubliceerd" / feitcheck-FAIL** (harde les uit BotLease: de news-bot viel ooit stil zonder dat iemand het merkte). Eerste 5 GB/mnd gratis.
- [ ] **[later]** **Grounding with Bing Search** (Foundry-tool) — live web-research voor blog/lead-research/citatie-checks. ⚠️ **~$35 per 1.000 queries — duur**; alleen inzetten waar live web echt nodig is, niet per pagina. (Het oude standalone Bing Search API is dood sinds aug 2025.)
- [ ] **[later]** **Azure OpenAI image (`gpt-image-1`/`-mini`)** — hero-beelden als er geen feed-image is.
- [ ] **[later]** **Partner Center-account** — alleen nodig als de Managed Application via de Azure Marketplace wordt gepubliceerd. Voor de éérste klant (Tijmen) kan het ook **privé via service catalog** zonder marketplace-review = sneller.

### B2. SEO-/keyword-data
- [ ] **[BLOCKER MVP]** **DataForSEO**-account — pay-as-you-go, **minimum deposit $50** (credits verlopen niet, geen abonnement). Dekt:
  - Google Ads (Keywords Data) API: search volume, CPC, competition (~$50–75 per 1M keywords).
  - Labs API: keyword-ideeën, competitor-domeinen, keyword-gap (~$110 per 1M keywords).
  - SERP/rank-tracking (standard $0,0006/req, live $0,002/req).
  - Een compleet onderzoek per bedrijf is typisch **<$1**.
  - ⚠️ Sluit een **DPA met DataForSEO** en check serverlocatie/sub-processors. Stuur er nooit PII naartoe.
- [ ] **[later]** **DataForSEO AI Optimization API** (GEO-laag: AI-search-volume + citatie-/mention-tracking in ChatGPT/Perplexity/Gemini/Claude). Sterk verkoopargument, maar extra kosten → eventueel als betaalde add-on.

### B3. Search Console / Bing / indexatie
- [ ] **[BLOCKER MVP]** **IndexNow-key** per tenant-domein (gratis, .txt-bestand op site-root) — instant indexatie-ping naar Bing/ChatGPT/Yandex. BotLease heeft dit al werkend (`indexnow_ping.py`). ⚠️ **Google ondersteunt IndexNow NIET** → Google apart via sitemaps + Search Console.
- [ ] **[later]** **Google Search Console**-property (gratis) — per-URL performance/indexatie-data; voedt de monitoring-fase.
- [ ] **[later]** **Bing Webmaster Tools**-property (gratis) — Bing-indexatie + Keyword Research als goedkope tweede volumebron.

### B4. Domein-API's
- [ ] **[BLOCKER MVP voor de research-stap]** **Bulk domein-availability-API met free tier** voor het checken van de door de LLM gegenereerde shortlist:
  - WhoisJSON (~1.000 gratis requests/mnd, geen creditcard), of WhoisFreaks (500 gratis credits, 1.528+ TLD's).
- [ ] **[later]** **Cloudflare Registrar API** (beta) voor de uiteindelijke **registratie** tegen wholesale (geen markup, gratis WHOIS-privacy). ⚠️ Kan (nog) **geen bulk-availability** en geen transfers/renewals → daarom gescheiden van de check-stap hierboven.
- [ ] **[later/vermijden als instap]** GoDaddy API (vereist ≥50 domeinen sinds ~mei 2024) en Namecheap API (vereist ≥20 domeinen / ≥$50 saldo) — niet geschikt als instap-availability-bron.

### B5. E-mail / Teams / CRM (afhankelijk van A5)
- [ ] **[BLOCKER MVP]** **ACS Email** afzenderdomein + DNS-records (zie A2/B1).
- [ ] **[afhankelijk van keuze]** **CRM-API-key/credentials**: Dynamics 365 (vereist licenties — Sales Pro $65/user/mnd, Enterprise $95/user/mnd), of HubSpot (API gratis op alle tiers, incl. gratis CRM-tier), of Pipedrive.
- [ ] **[afhankelijk van keuze]** **Microsoft Teams** + routing via **Logic Apps Consumption** (eerste 4.000 acties/mnd gratis — aanbevolen voor multi-tenant) **of** Power Automate ($15/user/mnd — alleen als de klant zelf in Power Platform werkt).

### B6. Anti-spam (lead-formulier/chat)
- [ ] **[BLOCKER MVP]** **Cloudflare Turnstile**-keys (gratis tot 1M verificaties/mnd, cookieloos/AVG-vriendelijk) + server-side **honeypot** + per-IP **rate-limiting** in de Function. Zonder dit kan een bot de auto-reply-mail misbruiken (mail-bomb → kostenexplosie + domeinreputatie-schade). ⚠️ reCAPTCHA niet aanbevolen (CNIL-kritiek + gratis tier verlaagd naar 10.000/mnd).

### B7. Code / herbruikbare BotLease-bouwstenen (van Thomas)
- [ ] **[BLOCKER MVP]** De bestaande **Python config-generator** (`build_*.py`, `*_data.py`, `style_base.py`, `seo_common.py`) — uitbouwen naar tenant-config-driven (data + theming + SEO-tokens per klant uit JSON/ENV i.p.v. hardcoded BotLease).
- [ ] **[later]** De **nieuws-engine-logica** (`news_bot.py`: RSS-fetch → dedupe → recency-filter → SEO-scoring → LLM-rewrite naar strikte JSON → `editorial_gate()` → publish → IndexNow). De **gate-logica en JSON-schema-prompt zijn 1-op-1 herbruikbaar**; alleen de LLM-call (nu Claude-CLI/OpenRouter) moet naar de Foundry Responses API met Managed Identity. ⚠️ De Claude-CLI-/OAuth-route mag NIET in een klant-Azure-omgeving.

---

## (c) Beslissingen die Thomas/Tijmen samen moeten nemen

| # | Beslissing | Opties | Impact | Blocker? |
|---|---|---|---|---|
| C1 | **Hosting-model** | (A) klant-eigen subscription via Managed Application + Lighthouse · (B) dedicated resource group in Thomas' Azure · (C) gedeeld multi-tenant in Thomas' Azure | Bepaalt wie de Azure-rekening betaalt, isolatie-niveau, en of shared resources mogen | **[BLOCKER MVP]** |
| C2 | **Datalocatie / residency** | (a) data-at-rest-in-EU (Global Standard volstaat) · (b) EU-only-inference (Data Zone Standard EU; beperkt model tot GPT-4o/4.1) | Bepaalt modelkeuze, kosten (Data Zone ~5–10% duurder) en compliance | **[BLOCKER MVP]** |
| C3 | **EU-regio** | West Europe (Amsterdam, NL) · North Europe (Ierland) · Sweden Central (breedst voor GPT-4o/4.1 Data Zone) · Germany West Central | ⚠️ Let op: NL/West Europe valt wél onder EU Data Boundary, maar **EU Data Zone model-hosting** is momenteel Sweden Central / Germany West Central — niet elk model is in West Europe gehost. Bij VNet: alle resources moeten in dezelfde regio. | **[BLOCKER MVP]** |
| C4 | **Modelniveau** | GPT-4.1-mini (goedkoop, EU-data-zone-OK, waarschijnlijk genoeg voor blog/SEO/lead-replies) · GPT-4.1 (zwaardere reasoning) · GPT-5 (alleen als kwaliteit het echt eist → residency-compromis) | Kosten + kwaliteit + of EU-only haalbaar blijft | **[BLOCKER MVP]** |
| C5 | **Resource-isolatie** | per klant fysiek eigen Cosmos/Search (hardste isolatie, hoogste vaste kost) · gedeeld met project-isolatie (veel goedkoper, botst met "alles in eigen tenant") | Bepaalt de vaste maandbodem per tenant (AI Search $75–250 + Cosmos RU/s draaien 24/7) | **[BLOCKER MVP]** |
| C6 | **Prijsmodel naar de klant** | setup-fee (de "script-run") + maandelijkse beheer/AI-fee (klant draagt eigen Azure-verbruik) · all-in SaaS-prijs | ⚠️ Markt-benchmark: GoHighLevel ~$497/mnd agency-basis; AI-bureaus $5K–$25K/mnd mid-market; losse builds $2.500–$15.000 eenmalig + $500–$5.000/mnd retainer. Voor de Azure-in-eigen-tenant-enterprise-niche zit je aan de bovenkant. | **[BLOCKER MVP]** (voor offerte) |
| C7 | **Private networking** | VNet + private endpoints (sterk compliance-argument, maar regio-lock + complexer) · publiek met Turnstile/RBAC | Verhoogt complexiteit; sterkste verkoopargument voor "alles in eigen omgeving" | **[later]** |
| C8 | **Sales-agent autonomie** | autonoom antwoorden/doorzetten · human-in-the-loop (Teams Accept/Reject) | Bepaalt agent-architectuur + AI-Act-risicoprofiel | **[BLOCKER MVP]** |
| C9 | **Content-type** | nieuws (feed-gedreven, zoals BotLease) · evergreen blogs (keyword/onderwerp via Bing grounding) · beide | Bepaalt RSS-feeds vs. Grounding-with-Bing als research-bron | **[later]** |
| C10 | **Abuse-monitoring** | standaard (30-dagen logging) · Modified Abuse Monitoring + ZDR aanvragen (vereist EA/MCA) | Of je "AI leest niet mee" mag beloven in het contract | **[later, afhankelijk van A1-contracttype]** |
| C11 | **Aantal klanten jaar 1** | <5 (volledige multi-tenant-automatisering is dan mogelijk over-engineering; half-handmatig script volstaat) · meer (investeer in IaC/marketplace) | Bepaalt hoeveel je nú in automatisering investeert | **[later]** |
| C12 | **Externe API's binnen/buiten Azure** | alleen LLM + orkestratie + PII in Azure, niet-persoonlijke keyword/domein-calls naar EU-SaaS toegestaan · álles strikt binnen Azure | Bepaalt of DPA's met DataForSEO c.s. nodig zijn of een EU-only alternatief gezocht moet worden | **[BLOCKER MVP]** (compliance-uitgangspunt) |

---

## Samenvatting: de minimale "ga/no-go"-lijst voor de eerste klant

Zonder **al deze** kun je geen werkende MVP opleveren:

1. **Azure-subscription + Entra-tenant** met iemand die RBAC kan toekennen (A1).
2. **Beslissing hosting-model (C1) + datalocatie/regio/model (C2–C4) + resource-isolatie (C5)** vastgelegd per klant.
3. **Domein + DNS-toegang** voor site-CNAME en SPF/DKIM/DMARC (A2).
4. **Logo + kleuren + bedrijfs-/nicheinfo + echte auteur** voor de generator (A3, A4).
5. **Lead-bestemming + kwalificatie-rubriek + autonomie-keuze** (A5, C8).
6. **Verwerkersovereenkomst + AI-disclosure + consent-logging** (A6).
7. **Foundry + Azure OpenAI (Data Zone EU) + SWA + Functions + Cosmos + Storage + AI Search + Key Vault + ACS Email** geprovisioned (B1).
8. **DataForSEO-account ($50 deposit) + DPA** (B2, C12).
9. **IndexNow-key** (B3) en **domein-availability-API** (B4).
10. **Turnstile + honeypot + rate-limiting** vóór elk publiek lead-endpoint (B6).
11. **Prijsmodel** afgesproken (C6) voor de offerte.

---

### Belangrijkste valkuilen om vooraf met de klant te bespreken
- **Residency-val:** "Global Standard" geeft géén EU-inference-garantie, ook al staat de resource in een EU-regio. Kies bewust "Data Zone Standard (EU)" als EU-only hard is.
- **Model-lag in EU:** de nieuwste modellen (GPT-5.x) zijn medio 2026 nog niet als Data Zone in EU beschikbaar → bij een harde EU-eis pin je op GPT-4o/4.1. Communiceer dit vooraf.
- **Claude-via-Foundry** valt medio 2026 nog niet onder de EU Data Boundary → bij harde EU-eis Azure-OpenAI-modellen gebruiken, geen Claude-via-Foundry (verifieer op deploy-moment).
- **Vaste bodemkost per tenant:** AI Search Basic/S1 + Cosmos RU/s draaien 24/7, ook zonder verkeer → kan bij kleine klanten de marge opeten.
- **Foundry verandert snel:** prijzen/SDK's/namen wijzigen per kwartaal (memory-billing start 1-6-2026, hosted compute 22-4-2026). ⚠️ **Verifieer alle Azure-/Foundry-prijzen op de live pricing-pagina vlak vóór elke offerte** — de cijfers in dit document zijn de onderzoeksstand en kunnen verlopen zijn.
- **Geen overpromise op GEO:** citatie in ChatGPT/Perplexity is niet stuurbaar als een ranking; verkoop het als "we maximaliseren citatiekans + meten per engine", niet als gegarandeerde positie.
