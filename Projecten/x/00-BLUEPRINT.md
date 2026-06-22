# PROJECT X — Masterblauwdruk

> AI-marketingbureau in een doos. Eén keer bouwen, dan per nieuw klant-bedrijf "een script runnen" om alles op te zetten.
> Azure-native, multi-tenant, AVG/GDPR-compliant. Eerste klant via Tijmen (IT Connect, Almelo).
>
> **Status:** concept/architectuur. Nog niet gebouwd. Prijzen en Azure Foundry-details zijn actueel medio 2026 maar veranderen snel — verifieer op de live pricing-pagina's vlak voor een offerte.

Dit is het overkoepelende document. De rest van de map werkt het uit:
- **[01-intake.md](01-intake.md)** — de open vragen aan Tijmen/de klant die het hele ontwerp bepalen (deploy-model, EU-residentie hardheid, CRM, budget).
- **[02-architecture.md](02-architecture.md)** — de Azure-architectuur in detail (diensten, auth, netwerk, data-residentie).
- **[03-build-plan.md](03-build-plan.md)** — de bouwfasen van MVP naar volledig, met wat er per fase wordt opgeleverd.
- **[04-data-needed.md](04-data-needed.md)** — wat de klant moet aanleveren per onboarding (merk-assets, domein, auteur, CRM-keys, DNS).

> Let op: deze sub-docs bestaan mogelijk nog niet allemaal; dit document verwijst ernaar als de plek waar die details thuishoren.

---

## 1. Visie en propositie

PROJECT X is een herbruikbaar, grotendeels geautomatiseerd "marketingbureau in een doos". Voor elk nieuw klant-bedrijf doet het systeem zes dingen, en de opzet per klant gebeurt door **één script (Infrastructure-as-Code) te draaien** in plaats van alles handmatig op te tuigen.

**De niche die ons onderscheidt:** alles draait Azure-native en kan volledig **binnen de eigen Azure-omgeving van de klant** draaien. Dat is precies de harde eis van de eerste klant (via Tijmen) en het is exact wat de bestaande white-label-concurrent **GoHighLevel SaaS Mode** *niet* kan: GHL is multi-tenant in húń cloud, niet in de Azure-tenant van de klant. De combinatie "agency-in-a-box + draait in de klant zijn eigen, EU-data-residente Azure" is daarmee onze verkoopbare niche, vooral richting compliance-bewuste NL/EU-enterprises.

**Eerlijk over de grenzen** (zelfde no-overpromise-lijn als BotLease):
- GEO/AI-citatie (geciteerd worden door ChatGPT/Perplexity) is **niet stuurbaar als een ranking**. We maximaliseren de citatiekans (answer capsules, schema, freshness, consensus-signalen) en meten per engine, maar we garanderen geen positie.
- De "alles automatisch" belofte heeft bewuste menselijke gates ingebouwd waar dat moet (content-goedkeuring, lead-doorzet). Volledig autonoom is een risico, geen feature.

**Hergebruik van bestaande ervaring (BotLease):** Thomas heeft de losse bouwstenen al hands-on gebouwd voor BotLease — statische site-generator, eigen CRM + mailsysteem, een wekelijkse LLM-nieuws-engine, technische SEO + GEO (sitemaps, schema, llms.txt, AI-bot-toegang), rank-tracking. PROJECT X is grotendeels het **Azure-native maken en multi-tenant maken** van die patronen, niet het vanaf nul opnieuw uitvinden. Per stap hieronder benoemen we welk BotLease-patroon herbruikbaar is.

---

## 2. Wat het systeem per klant doet — de 6 stappen

| # | Stap | Wat het doet | BotLease-patroon dat hergebruikt wordt | Azure-native invulling |
|---|------|--------------|----------------------------------------|------------------------|
| 1 | **Domein-/niche-/keyword-onderzoek** | Uit "bedrijf + branche" → niche, doelgroep, intentie, seed-keywords, domeinnaam-shortlist + beschikbaarheid + keyword-volume/CPC/concurrentie | (nieuw, maar `rank_bot.py`/`seo_common.py`-state-patroon herbruikbaar) | LLM = Azure OpenAI (EU Data Zone); data = DataForSEO Labs/Google Ads + domein-availability-API (extern, geen PII) |
| 2 | **Marketingwebsite bouwen** | Genereert een statische, snelle, SEO/GEO-vriendelijke site met klant-branding (kleuren/logo), schema, llms.txt | De Python config-generator (`build_*.py` + `*_data.py` + `style_base.py` CSS-vars + `seo_common.py`) is al een config-driven blauwdruk, alleen nog single-tenant | Azure Static Web Apps (Standard, $9/site/mnd, met SLA) of Blob static website |
| 3 | **SEO + GEO automatiseren** | Technische SEO (sitemaps, schema, interne links), IndexNow-ping, rank-tracking, entity-laag (Organization/sameAs + Wikidata), GEO-tactieken (TL;DR, answer capsules, FAQPage) | `indexnow_ping.py`, schema-emit in generators, llms.txt-feitenkaart, TL;DR's — direct herbruikbaar als verplichte template-laag | Azure Functions (timer-trigger) als "bots"; embeddings (Azure OpenAI) + Azure AI Search/Cosmos voor self-healing interne links; DataForSEO voor rank-data |
| 4 | **Blog/content automatisch publiceren** | Wekelijks 2-3 artikelen: research → LLM-draft → E-E-A-T/feitcheck-gate → publiceren → intern linken → schema/auteur/beeld | `news_bot.py` is dé blauwdruk: RSS→dedupe→recency→SEO-scoring→LLM-rewrite naar strikte JSON→`editorial_gate()`→append→rebuild→IndexNow. 1-op-1 te vertalen | Azure Functions "serverless agents runtime" (.agent.md, cron-trigger) + Foundry Agent Service; beeld via gpt-image-1; Durable Functions voor orchestratie + optionele human-in-the-loop |
| 5 | **Inbound sales-leads afvangen + beantwoorden + kwalificeren** | Twee vangnetten (formulier + AI-chat-widget); AI stelt eerste reactie op, voert BANT-gesprek, scoort tegen rubriek (JSON-output) | `contact.js` (formulier→CRM) + `chat.js` (chatbot) = exact het dubbel-kanaal-patroon; `imap_poller.py`/CRM-werklijst voor opvolging | Foundry Agent Service (lead-agent) + Azure OpenAI GPT-4o-mini; auto-reply via Azure Communication Services Email; opslag in Cosmos DB |
| 6 | **Gekwalificeerde leads doorzetten naar de klant** | Boven een drempelscore: routeren naar e-mail / Teams (Accept/Reject-kaart) / CRM (Dynamics, HubSpot) | CRM-webhook-patroon | Logic Apps (Consumption) of een Function-call naar de CRM-API; routing-target is per tenant config |

---

## 3. High-level architectuur (Azure-first)

```
                      ┌─────────────────────────────────────────────────┐
                      │   Klant-Azure-tenant (West Europe / Sweden Central)│
                      │   alles EU-data-resident, AVG-compliant            │
                      │                                                    │
  Bezoeker ──► Azure Static Web Apps (de site)                            │
                      │        │                                          │
                      │        ▼ formulier + chat-widget                  │
                      │   Azure Container Apps  ◄── "het kleine            │
                      │   / Azure Functions          webservertje"        │
                      │        │  (API, webhooks, anti-spam: Turnstile     │
                      │        │   + honeypot + rate-limit)                │
                      │        ▼                                          │
                      │   Microsoft Foundry Agent Service                 │
                      │   ├─ research-agent   ├─ content-agent            │
                      │   ├─ SEO-agent        ├─ sales/qualify-agent      │
                      │   │   (Responses API, één endpoint, EU Data Zone) │
                      │   ▼                                              │
                      │   Azure OpenAI modellen (GPT-4.1-mini / 4o-mini, │
                      │   Data Zone Standard EU) + embeddings            │
                      │                                                    │
                      │   Data/state (BYO, blijft in tenant):            │
                      │   ├─ Cosmos DB (threads/leads, partition=tenantId)│
                      │   ├─ Azure AI Search (RAG/GEO-kennisbank, vectors)│
                      │   ├─ Azure Storage (files/embeddings/beeld)       │
                      │   └─ Azure Key Vault (secrets, keyless via MI)    │
                      │                                                    │
                      │   Auth: Microsoft Entra ID + Managed Identity     │
                      │   Mail: Azure Communication Services Email        │
                      │   Routing: Logic Apps → e-mail/Teams/CRM          │
                      └─────────────────────────────────────────────────┘
            ▲
            │ beheer (cross-tenant control plane)
   Bureau-tenant (Thomas) ── Azure Lighthouse-delegatie (least-privilege)
   + Managed Application-definitie (mainTemplate.json + createUiDefinition.json)
   + IaC: Bicep (Foundry standard-agent-setup template) via GitHub Actions
```

**Kernbeslissingen:**

1. **Foundry Agent Service als AI-laag.** "Azure AI Studio" heet sinds 2025 **Azure AI Foundry** en in de 2026-docs vaak kortweg **Microsoft Foundry**. De Agent Service is GA sinds mei 2025. De runtime zelf kost **geen platform-fee**: je betaalt alleen model-tokens + tool-usage (+ vanaf 2026 hosted-compute en memory, indien gebruikt).
2. **Responses API als entry-point.** Eén endpoint per project (`https://<resource>.services.ai.azure.com/api/projects/<project>`) geeft toegang tot modellen + ingebouwde tools (file search/RAG, code interpreter, web search/Grounding with Bing, function calling, MCP). Je kunt 'm óók rechtstreeks vanuit je webservice aanroepen zónder een agent-resource te maken — exact het patroon dat de BotLease nieuws-engine/CRM nodig heeft.
3. **"Standard agent setup" = alles in eigen tenant.** I.t.t. de "basic" setup (Microsoft-managed opslag) houdt de **standard** setup alle agent-state, gesprekken en kennisbestanden in de Azure-resources van de klant, via "capability hosts" op BYO Cosmos DB + Storage + AI Search + Key Vault. Dit is precies wat Tijmens klant wil.
4. **Hosting van het webservertje = Azure Container Apps (Consumption).** Scale-to-zero, per-seconde billing, ruime gratis grant (180k vCPU-sec / 360k GiB-sec / 2M requests per maand per subscription → vaak €0). Azure Functions voor pure webhooks + cron (lead-intake, mail-parser, wekelijkse blog-publish).
5. **Keyless auth.** Geen API-keys in code/repo (sluit aan op de BotLease-regel "geen secrets in de repo"). De webservice authenticeert met `ManagedIdentityCredential` (in productie liever de specifieke variant dan `DefaultAzureCredential`, i.v.m. latency en onbedoelde fallback-paden); RBAC least-privilege op Cosmos/Storage/Search; secrets in Key Vault.

---

## 4. De herbruikbare multi-tenant aanpak — "1 script per klant"

Er zijn **twee deploy-modellen** en je moet de IaC zo bouwen dat dezelfde template **beide** aankan (parameter bv. `deploymentTarget`):

| Model | Voor wie | Hoe | Kostenprofiel |
|-------|----------|-----|---------------|
| **A — In de Azure van de KLANT** | Tijmens klant (harde eis), enterprise/compliance | **Azure Managed Application**: jij levert een ZIP met `mainTemplate.json` (Bicep die alles uitrolt) + `createUiDefinition.json` (intake-formulier). Resources landen in een "managed resource group" in de subscription van de klant; jij houdt beheer via een identity in jouw tenant, gekoppeld aan **Azure Lighthouse**-delegatie. | Niets te delen → elke klant betaalt apart de vaste bodemlast (AI Search, Cosmos RU/s). Hoogste isolatie. |
| **B — In JULLIE Azure** | Latere, kleinere klanten die hun eigen Azure níet willen beheren | Shared subscription, isolatie via aparte resource group + tenantId-partitionering + security-filters. Eventueel gedeelde AI Search/Cosmos. | Goedkoper (gedeelde resources mogelijk), lagere isolatie. |

**Het "script" zelf** = Infrastructure-as-Code + orchestrator:
- **Bicep** via de officiële Microsoft **"standard-agent-setup" templates** (`github.com/microsoft-foundry/foundry-samples`, map `43-standard-agent-setup-with-customization` en `15-private-network-standard-agent-setup`). Eén deploy maakt Foundry-resource + project + Cosmos + Storage + AI Search + Key Vault + connections + capability hosts + RBAC. Reken **~30-45 min provisioning** per tenant.
- Patroon: **subscription vending** (Azure Verified Modules, `bicep-lz-vending`) + **Deployment Stamps** (1 idempotente template per klant = 1 "stamp"), getriggerd door GitHub Actions met een **per-klant parameterfile**.
- **Idempotent** = je kunt het script veilig opnieuw draaien (deterministische naming op basis van tenant-id; what-if/deployment stacks).

**De per-tenant config** (de eigenlijke "agency-in-a-box"-laag, los van de infra) is één JSON/YAML per klant met: domein, merk (kleuren/`:root` CSS-vars, logo), niche-systeemprompt, kwalificatie-rubriek (BANT of branche-specifiek), interne-link-lijst, content-cadans (cron), routing-target, auteur-Person. Onboarding = `azd up` (of GitHub Action) + die config-file injecteren.

**Benchmark (GoHighLevel "Snapshot"):** bij aankoop draait daar automatisch sub-account-aanmaak + credentials mailen + template inladen + billing starten. Dat "snapshot = 1 klik klant opzetten" is exact ons doel — wij doen het Azure-native én in de tenant van de klant.

---

## 5. Bouwfasen (MVP → volledig) — in het kort

Zie **[03-build-plan.md](03-build-plan.md)** voor de uitwerking. Hoofdlijn:

- **Fase 0 — Intake & beslissingen.** Open vragen uit [01-intake.md](01-intake.md) beantwoorden mét Tijmen/klant: deploy-model (A of B), hardheid EU-eis (data-at-rest vs. EU-only-inference), CRM-bestemming, budget per tenant, private networking ja/nee, EA/MCA aanwezig (bepaalt of Zero Data Retention haalbaar is). Zonder deze antwoorden is de rest gokwerk.
- **Fase 1 — MVP voor de eerste klant (Tijmen), half-handmatig mag.** Eén Foundry standard-agent-setup (Bicep) in de klant-subscription; statische site (port van de Python-generator met klant-config); formulier + chat-widget → Function → Cosmos; auto-reply via ACS Email; lead-kwalificatie-agent met JSON-output; doorzet naar e-mail/Teams. Onder ~5 klanten is volledige automatisering over-engineering — een half-handmatig "script" volstaat eerst.
- **Fase 2 — Content + SEO/GEO automatiseren.** Port van `news_bot.py` naar de Azure Functions agents-runtime (.agent.md, cron) met de `editorial_gate()` + feitcheck-pass; IndexNow-ping; entity-laag (Organization/sameAs + Wikidata); rank-tracking via DataForSEO; embeddings-gedreven interne links.
- **Fase 3 — Productiseren als "agency-in-a-box".** IaC volledig idempotent + Deployment Stamps; per-tenant config-driven; Managed Application-definitie (eerst privé/service-catalog voor klant 1, later eventueel Marketplace) + Lighthouse-delegatie; cost-budgets/alerts per tenant; loud-failure-monitoring (App Insights/Logic App-alert bij "0 gepubliceerd").

---

## 6. Kostenmodel / indicatie

> Alle bedragen zijn indicatief (USD tenzij anders), medio 2026, Global Standard pay-as-you-go. **Data Zone EU ligt ~5-10% hoger** dan Global Standard. Verifieer op de live pricing-pagina's vóór een offerte; Foundry-prijzen veranderen snel en sommige facturering (hosted compute, memory) start pas in 2026.

**Vaste bodemkost per tenant (draait 24/7, ook zonder verkeer) — dit is de belangrijkste post:**

| Post | Indicatie | Opmerking |
|------|-----------|-----------|
| Azure AI Search | Free $0 (dev) / **Basic ~$75/mnd** / S1 ~$250/mnd | Realistisch startpunt voor RAG = Basic of S1. De grootste vaste last. |
| Cosmos DB | ~$0,25/GB/mnd + RU/s; **standard agent setup vereist min. 3000 RU/s** | Gratis tier 1000 RU/s + 25 GB; overweeg serverless waar mogelijk |
| Azure Static Web Apps | **$9/site/mnd (Standard, met SLA)** | Free heeft géén SLA → niet voor betalende klant |
| Container Apps / Functions | vaak **$0** binnen de gratis grant | 180k vCPU-sec / 2M requests gratis p/mnd |
| Key Vault, Storage, Entra/MI | centen | Managed identity is gratis |
| Private endpoints (optioneel) | ~$0,01/uur elk + data-processing | Alleen bij private networking-eis |

→ **Realistische vaste bodem per tenant: grofweg ~$85-$260/mnd** (vooral AI Search + SWA + Cosmos RU/s), los van LLM-verbruik.

**Variabel (verbruik) — verwaarloosbaar bij deze workload:**

| Post | Indicatie |
|------|-----------|
| GPT-4.1-mini (werkpaard content/SEO/leads) | $0,40 in / $1,60 out per 1M tokens; cached input 50-90% korting |
| GPT-4o-mini (lead-chat) | $0,15 / $0,60 per 1M; ~10M tokens ≈ ~$3 |
| GPT-4.1 / GPT-4o (zwaardere reasoning) | $2,00/$8,00 resp. $2,50/$10 per 1M |
| Grounding with Bing (web-research) | **~$35 per 1.000 queries** — duur; alleen voor news-research/citatie-monitoring, niet per pagina |
| Azure Communication Services Email | $0,00025/e-mail + $0,00012/MB; 3.000 mails ≈ ~$0,75/mnd |
| gpt-image-1 hero-beeld | ~$0,011-$0,25/beeld; mini vanaf ~$0,005 |
| DataForSEO (extern) | $50 min. deposit, geen abo; compleet keyword-onderzoek per bedrijf typisch <$1; SERP standard $0,0006/req |

**Eigen prijszetting (markt-benchmark):** generieke marketing-automation $50-$3.000/mnd; AI-marketingbureaus $3.000-$25.000/mnd (mid-market gem. $5K-$25K); losse builds $2.500-$15.000 eenmalig + $500-$5.000/mnd retainer. Onze Azure-in-eigen-tenant-enterprise-propositie zit aan de bovenkant: **setup-fee (de "script-run" + intake) + maandelijkse beheer/AI-fee**, waarbij de klant in model A zelf de Azure-verbruikskosten draagt. Open vraag: draagt de klant Azure rechtstreeks of factureren wij door? (zie [01-intake.md](01-intake.md)).

---

## 7. Risico's + AVG/GDPR

**De #1 valkuil — data-residency:**
- **"Global Standard" deployment geeft GÉÉN EU-residency-garantie** voor de inference (kan wereldwijd routen), óók als de resource in een EU-regio staat. Data-at-rest blijft wel in jouw regio. Voor de harde EU-eis **moet** je **"Data Zone Standard" (EU)** of een regionale "Standard"-deployment kiezen. Leg per klant expliciet vast: welk model + welk deployment-type.
- **Model-lag in EU Data Zone:** de nieuwste modellen (GPT-5.2/5.5) zijn medio 2026 **niet** als Data Zone Standard in EU beschikbaar (alleen US-datazones), wel als Global Standard in Sweden Central/Poland Central. Bij een harde EU-only-inference-eis ben je dus beperkt tot **GPT-4o / GPT-4.1**. Communiceer dit vooraf.
- **Sweden Central** is medio 2026 het breedst voor GPT-4o/4.1 Data Zone EU. (Let op nuance: West Europe/NL valt onder de EU Data Boundary, maar niet elk model wordt fysiek in West Europe gehost — model-hosting-zones in de EU zijn vooral Sweden Central en Germany West Central. Plan compute/storage in West/North Europe, kies model-deployment expliciet als Data Zone EU.)

**AVG/GDPR overig:**
- Azure OpenAI / Azure-direct modellen vallen onder de Microsoft **DPA**: klant-prompts/completions trainen **geen** modellen en worden niet door het systeem opgeslagen (los van wat jij zelf in Cosmos/Storage opslaat). Microsoft = data-processor, klant = controller. De **EU Data Boundary** (mei 2026) dekt o.a. NL, FR, DE, IT, NO, PL, ES, SE, CH.
- **Anthropic/Claude-via-Foundry valt medio 2026 nog NIET onder de EU Data Boundary** → niet gebruiken bij een harde EU-residency-eis; blijf bij Azure-direct (OpenAI) modellen. (Verifieer op deploy-moment of de EU-native Claude-deployment inmiddels live is.)
- **Abuse-monitoring** logt standaard prompts/completions ~30 dagen met mogelijke human review. Voor strikte privacy vraag je **"Modified Abuse Monitoring"** (geen human review) en/of **Zero Data Retention** aan via het Limited Access-programma. **ZDR vereist een EA/MCA — niet beschikbaar op pure pay-as-you-go.** Belofte "AI leest niet mee / data wordt niet bewaard" pas doen ná bevestiging dat de klant-tenant dit kan aanvragen.
- **EU AI Act Art. 50** (transparantieplicht, in werking aug 2026): de sales-/lead-chatbot **moet** bij eerste interactie melden dat het AI is. Boetes tot €35M of 7% omzet. Maak een **"Ik ben een AI-assistent"-disclosure + consent-logging** een verplicht, niet-uitschakelbaar onderdeel van elke tenant-deploy.
- **Verwerkersovereenkomst:** het bureau is vermoedelijk (sub)verwerker namens de klant → er moet een verwerkersovereenkomst tussen bureau en klant komen, bovenop de Microsoft DPA. Template aanleveren/laten opstellen.
- **Externe API's (DataForSEO, domein-checks):** GDPR-acceptabel zolang er **geen persoonsgegevens** van de eindklant naartoe gaan (alleen zoekwoorden/branchetermen/domeinnamen). Leg dit vast, sluit DPA's, en houd PII (lead-namen/e-mails) strikt binnen Azure-EU.

**Technische valkuilen om in te bouwen:**
- **Capability host is onveranderlijk** — niet te updaten na creatie; verkeerde config = project verwijderen en opnieuw. Bicep-template in één keer goed hebben vóór multi-tenant uitrol.
- **Cosmos RU/s-bodem:** standard agent setup faalt (`CapabilityHostProvisioningFailed`) onder 3000 RU/s; per project +3000. Loopt op bij veel tenants.
- **Vaste bodemkost per tenant** (AI Search + Cosmos) kan de marge opeten bij veel kleine klanten → "lite"-variant in model B met gedeelde index + security-filters.
- **Regio-lock bij VNet:** alle Foundry-workspace-resources moeten in dezelfde regio als de VNet. Regio vooraf plannen.
- **Hosted agents zijn preview** (medio 2026) → bouw productie-kritische multi-tenant flows op **Prompt agents (GA) + Responses API**, niet op de preview-laag.
- **Silent failure:** de BotLease news-bot viel ooit stil (exit 0 bij "0 artikelen"). In Azure een **alert op "0 gepubliceerd" / feitcheck-FAIL** (App Insights/Logic App) verplicht inbouwen.
- **Scaled content abuse:** nooit honderden pSEO-pagina's tegelijk live (Google-penalty). Progressive rollout (~100 → 4-6 wk monitoren → schalen); lage cadans (2-3 artikelen/week) + harde editorial-gate.
- **Cron in Azure Functions is default UTC** → zet `WEBSITE_TIME_ZONE` (W. Europe Standard Time), anders publiceert content op het verkeerde moment.
- **Auto-reply-mail = misbruikrisico** → Turnstile + honeypot + rate-limit verplicht, anders mail-bomb/kostenexplosie + domeinreputatieschade.
- **SPF/DKIM/DMARC per tenant-domein** → ACS dwingt domeinverificatie af; opnemen in het per-klant deploy-script, anders belanden auto-replies in spam bij oplevering.

---

## 8. Belangrijkste open beslissingen (volledig in [01-intake.md](01-intake.md))

1. Deploy-model **A** (klant-tenant, managed app) of **B** (bureau-tenant)? Bepaalt de hele kosten- en isolatie-structuur en wie de Azure-rekening betaalt.
2. Hoe hard is de EU-eis: **data-at-rest-in-EU** (makkelijk, Global Standard volstaat) vs. **EU-only-inference** (vereist Data Zone EU, beperkt modelkeuze tot GPT-4o/4.1)?
3. Heeft de klant een **EA/MCA** (bepaalt of ZDR/Modified Abuse Monitoring haalbaar is)?
4. Welk **CRM** (Dynamics 365 / HubSpot / Pipedrive / niets) → routing-bestemming + notificatiekanaal (Teams vs. e-mail).
5. **Private networking** (VNet + private endpoints): eis of nice-to-have? Sterk compliance-argument, maar verhoogt complexiteit + regio-lock.
6. Mag **AI Search/Cosmos gedeeld** worden over tenants (goedkoper) of fysiek per klant (hardste isolatie)? Botst met "alles in eigen tenant".
7. Wie is de **named author** per klant-site (E-E-A-T eist een echte persoon)?
8. Port Thomas zijn bestaande Python-bouwstenen, of herbouwt hij ze als referentie-architectuur? Bepaalt de tijdsinvestering van de eerste tenant-build.

---

*Bronnen: Microsoft Learn (Foundry agents/overview, standard-agent-setup, deployment-types, agent-identity, data-privacy, managed-applications, lighthouse, deployment-stamp), techcommunity GA-blog + Build 2026 update, Azure pricing-pagina's (OpenAI, Container Apps, Functions, AI Search, Cosmos, Foundry Agent Service, Communication Services), DataForSEO, Cloudflare, kriv.ai (GDPR/residency), EU AI Act Art. 50, GoHighLevel. Volledige URL's per onderwerp in de onderzoeksbevindingen waarop dit document is gebaseerd.*
