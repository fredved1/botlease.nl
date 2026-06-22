# PROJECT X — Technische Architectuur

> "AI-marketingbureau in een doos" — Azure-native, multi-tenant, AVG/GDPR-compliant.
> Doelgroep: Thomas (bouwer) + Tijmen (IT Connect, Almelo) en zijn klant.
> Toon: concreet, eerlijk, geen overpromise. Alle prijzen/feiten komen uit het onderzoek; onzekerheden zijn expliciet gemarkeerd.

---

## 0. Uitgangspunten en de harde eis

De klant van Tijmen stelt één harde eis: **alles draait binnen ZIJN eigen Azure-omgeving** (vermoedelijk Microsoft Azure, aanname Azure AI Foundry + een klein webservertje). Context is NL/EU, dus AVG/GDPR-conform.

Dat dwingt drie architectuurkeuzes af die de rest van dit document sturen:

1. **Deploy in de tenant van de klant, niet in die van het bureau.** Het canonieke Azure-patroon hiervoor is **Azure Managed Applications**: jij levert een ZIP met `mainTemplate.json` (de Bicep/ARM die alle resources uitrolt) + `createUiDefinition.json` (het intake-formulier). De resources landen in een "managed resource group" in de subscription van de klant; de **data blijft bij de klant**, jij houdt beheertoegang via een identity in jouw tenant. Aangevuld met **Azure Lighthouse** voor één control plane (gedelegeerde RBAC) over meerdere klant-Azures.
   - https://learn.microsoft.com/en-us/azure/azure-resource-manager/managed-applications/
   - https://learn.microsoft.com/en-us/azure/lighthouse/concepts/isv-scenarios

2. **EU-residency is een bewuste, per-resource keuze — geen automatisme.** De #1 valkuil: het **deployment type** van het model bepaalt residency, NIET alleen de regio van de resource. Zie §6.

3. **Keyless auth (Entra ID + Managed Identity).** Geen API-keys in code/repo. Sluit aan op de bestaande BotLease-regel "geen secrets in de repo". Secrets in Azure Key Vault.

> **Open vraag die de hele kostenstructuur bepaalt (markeer dit in de offerte):** wil de klant écht alles in zijn EIGEN subscription (Managed App in zijn tenant), óf is een dedicated resource group in JOUW Azure-tenant ook acceptabel? Het eerste is Tijmens eis; het tweede is goedkoper en wat latere, kleinere klanten waarschijnlijk willen. **Bouw de IaC zo dat dezelfde template beide aankan** (parameter `deploymentTarget`).

---

## 1. Hoogniveau-overzicht — wat herbruiken we uit BotLease?

Thomas heeft de bouwstenen al handmatig/VPS-native gebouwd voor BotLease. PROJECT X **vertaalt** die patronen naar Azure; je herbouwt ze niet from scratch.

| BotLease (VPS / nu) | PROJECT X (Azure-native) | Hergebruik |
|---|---|---|
| Statische site in `frontend/` (Python-generator: `build_*.py`, `*_data.py`, `style_base.py`, `seo_common.py`) | Azure Static Web Apps + dezelfde generator, **config-driven per tenant** | Generator-logica, CSS-variabele-theming, JSON-LD, llms.txt, Umami-tracker zitten er al in |
| Cron/launchd-bots (`news_bot.py`, `indexnow_ping.py`, `rank_bot.py`, `build_seo_dashboard.py`) | Azure Functions (timer-trigger, NCRONTAB) of `.agent.md` serverless agents runtime | Stap-logica, editorial-gate, idempotentie-patronen |
| LLM via Claude-CLI / OpenRouter | Azure OpenAI / Foundry Models (Responses API), EU-deployment, Managed Identity | JSON-schema-prompts, gate-logica blijven 1-op-1 |
| Eigen CRM op VPS (SQLite `crm.db`, `imap_poller.py` + SMTP) | Cosmos DB serverless + Azure Communication Services Email + Azure Functions | Lead-model, kwalificatie-rubriek, threading-idee |
| Rank-tracking via gratis DDG/Bing-scrape | DataForSEO API (betaald, betrouwbaar, echt Google) | Cron/JSON-state/dashboard-architectuur |
| Vercel deploy | Azure Static Web Apps deploy (Bicep + GitHub Action / SWA CLI) | Deploy-werkwijze |

> **Let op (BotLease-eigen valkuilen die meereizen):** Vercel-specifieke onderdelen (`/_vercel/insights`, `vercel.json`, `.vercel/`) werken NIET op Azure en moeten eruit. De ~55 pagina's met `<style id="mobile-first-patch">` die de generators niet emitten zijn een teken dat een echte multi-tenant generator die patch **standaard in de template moet bakken**, anders herhaalt het "niet-rebuilden"-probleem zich bij elke klant.

---

## 2. End-to-end dataflow (ASCII-diagram)

```
                          ┌──────────────────────────────────────────────────────────────┐
                          │  KLANT-AZURE-TENANT  (West Europe / Sweden Central, EU-only)   │
                          │  uitgerold als Azure Managed Application (Bicep + UI-form)     │
                          └──────────────────────────────────────────────────────────────┘

  PER-KLANT ONBOARDING (= "het script")
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │  GitHub Action / azd up  →  Bicep (Deployment Stamp, idempotent)  →  resources in        │
  │  klant-subscription:  Foundry-project · Functions/Container Apps · Static Web App ·       │
  │  Cosmos DB · AI Search · Storage · Key Vault · ACS Email · (Logic App)                    │
  │  tenant-config.json  (domein · niche-prompt · merk-kleuren · auteur-Person · BANT-rubriek │
  │                        · routing-target · cadans-cron)                                    │
  └────────────────────────────────────────────────────────────────────────────────────────┘

  RUNTIME PIPELINE  (6 stappen, EU-only inference via Data Zone deployment)

  ┌── STAP 1: DOMEIN / NICHE / KEYWORDS ───────────────────────────────────────────────────┐
  │                                                                                          │
  │  [Foundry Research-agent]                                                                 │
  │     │  LLM (GPT-4.1-mini, EU Data Zone) → niche/doelgroep/intentie + domeinnaam-ideeen    │
  │     ├──► DataForSEO Labs API ........... keyword-ideeen, keyword-gap, concurrenten        │
  │     ├──► DataForSEO Google Ads API ..... search volume, CPC, competition                  │
  │     ├──► DataForSEO AI Optimization .... GEO: AI-search-volume + LLM-citatie-tracking     │
  │     ├──► WhoisJSON / WhoisFreaks ....... bulk domein-availability (shortlist)             │
  │     └──► Cloudflare Registrar API ...... uiteindelijke registratie (wholesale)            │
  │            (alleen niet-PII naar externe API's: keywords/branchetermen/domeinen)          │
  └──────────────────────────────────────────────────────────────────────────────────────┬─┘
                                                                                            │ keyword→pagina-map
                                                                                            ▼ (menselijke gate aanbevolen)
  ┌── STAP 2: MARKETINGSITE BOUWEN ────────────────────────────────────────────────────────┐
  │  [Python-generator, config-driven]  →  statische HTML + :root-theming + JSON-LD          │
  │     → Azure Static Web Apps (EU-regio, gratis SSL, custom domein)                         │
  │     → contactformulier-endpoint = Azure Function (HTTP-trigger, in de SWA)                │
  │     → Umami (self-hosted, Container App + Postgres) voor cookieloze analytics             │
  └──────────────────────────────────────────────────────────────────────────────────────┬─┘
                                                                                            │
                                                                                            ▼
  ┌── STAP 3: SEO + GEO ───────────────────────────────────────────────────────────────────┐
  │  [Functions, timer-trigger]                                                               │
  │     ├─ sitemap.xml / sitemap-news.xml builder                                             │
  │     ├─ IndexNow-ping (gratis; Bing→ChatGPT, Yandex, ...)  [Google = aparte lijn: GSC]     │
  │     ├─ schema-validatie (Rich Results Test API) als deploy-gate                           │
  │     ├─ interne links via embeddings (text-embedding-3-small) → Azure AI Search vector     │
  │     ├─ entity-laag: Organization/sameAs JSON-LD + Wikidata-entry (QID)                    │
  │     └─ rank-tracking via DataForSEO SERP/Labs (echt Google.nl)                            │
  └──────────────────────────────────────────────────────────────────────────────────────┬─┘
                                                                                            │
                                                                                            ▼
  ┌── STAP 4: BLOGS / CONTENT (wekelijks) ─────────────────────────────────────────────────┐
  │  [.agent.md serverless agent OF Durable Functions orchestratie]                           │
  │     research (RSS feedparser  of  Grounding with Bing) ──► LLM-draft (JSON-schema)        │
  │       ──► editorial-gate (anti-thin, anti-AI-tell, min. interne+externe links)            │
  │       ──► feitcheck-pass (PASS/FAIL tegen bron, anti-hallucinatie)                        │
  │       ──► hero-image (gpt-image-1) + alt-tekst                                            │
  │       ──► [optioneel] human-in-the-loop approval (Teams / Logic App)                      │
  │       ──► publiceren (SWA) + sitemap-update + IndexNow-ping                               │
  │     loud-failure alert bij "0 gepubliceerd" / feitcheck-FAIL (App Insights)               │
  └──────────────────────────────────────────────────────────────────────────────────────┬─┘
                                                                                            │
                                                                                            ▼
  ┌── STAP 5: INBOUND LEADS AFVANGEN + BEANTWOORDEN + KWALIFICEREN ─────────────────────────┐
  │  Bezoeker op site                                                                         │
  │     ├─ Webformulier ──► Azure Function (Turnstile + honeypot + rate-limit)                │
  │     └─ Chat-widget ───► Azure Function (proxy) ──► [Foundry Sales-agent]                  │
  │                                                       │  BANT-gesprek (GPT-4o-mini, EU)   │
  │                                                       │  AI-disclosure (EU AI Act Art.50) │
  │                                                       ▼                                   │
  │     lead + consent + conversatie ──► Cosmos DB (serverless, partition = tenantId)         │
  │     auto-reply ──► Azure Communication Services Email (geverifieerd afzenderdomein)       │
  │     kwalificatie ──► structured JSON {budget,authority,need,timeline,score,qualified}     │
  └──────────────────────────────────────────────────────────────────────────────────────┬─┘
                                                                                            │ score >= drempel
                                                                                            ▼
  ┌── STAP 6: GEKWALIFICEERDE LEAD DOORZETTEN ─────────────────────────────────────────────┐
  │  [Routing-laag: Logic App Consumption  OF  Azure Function-call]   (per-tenant config)     │
  │     ├─ e-mail (ACS)                                                                       │
  │     ├─ Microsoft Teams Adaptive Card (Accept/Reject)  ── human-in-the-loop               │
  │     ├─ Dynamics 365 (Dataverse)                                                           │
  │     └─ HubSpot / Pipedrive (REST/webhook)                                                 │
  └──────────────────────────────────────────────────────────────────────────────────────┘

  CROSS-CUTTING:  Entra ID + Managed Identity (keyless) · Key Vault (secrets) ·
                  VNet + Private Endpoints (optioneel, sterk EU-argument) ·
                  Application Insights (tracing + loud-failure alerts) ·
                  Azure Policy "allowed locations = EU" afgedwongen in de template
```

---

## 3. Azure-componenten (de fundering)

### 3.1 AI-laag — Microsoft Foundry (voorheen "Azure AI Foundry")

> **Naamswijziging:** "Azure AI Studio" → "Azure AI Foundry" (2025) → in de 2026-docs vaak kortweg **"Microsoft Foundry"**. De Agent Service is **GA sinds mei 2025**. Door 2025/2026 toegevoegd: observability, multi-agent orchestration, Agent-to-Agent (A2A) API, memory (preview), Hosted Agents (preview).

**Twee agent-types — kies bewust hoeveel platform je wilt:**

- **Prompt agents (GA, aanrader voor PROJECT X):** volledig managed; je definieert alleen instructies + model + tools. Geen compute/containers te beheren. Kosten = per-call inference + tool-usage. **Declaratief → per-tenant scriptbaar via Bicep/SDK.** Dit is de simpelste "script-bare" basis.
- **Hosted agents (preview, alleen indien nodig):** jouw eigen code (Agent Framework / LangGraph / OpenAI Agents SDK / eigen code) als container, door Foundry gehost met managed endpoint + autoscale + eigen Entra-identity. Alleen kiezen als je custom orchestratie-code (bv. de blog-generator-loop) écht in Foundry wilt draaien.
  - Hosted-compute prijs (preview): **$0,0994/vCPU-uur + $0,0118/GiB-uur**.

> **Pitfall:** Hosted Agents zijn medio 2026 **preview**. Bouw productie-kritische multi-tenant flows op **Prompt agents (GA) + Responses API**, niet op de preview-laag.

**De Responses API is de kern.** Eén entry-point achter alle agent-types geeft toegang tot Foundry-modellen + platform-tools. Je kunt 'm OOK **rechtstreeks vanuit je eigen webservice aanroepen zonder een agent-resource te maken** — exact wat de news-engine/CRM-vertaling nodig heeft:

```python
# project-endpoint: https://<resource>.services.ai.azure.com/api/projects/<project-name>
from azure.ai.projects import AIProjectClient
from azure.identity import ManagedIdentityCredential   # productie: specifiek, niet DefaultAzureCredential

client = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=ManagedIdentityCredential())
resp = client.get_openai_client().responses.create(model="gpt-4.1-mini", input=...)
```

**Ingebouwde tools die 1-op-1 op de BotLease-patronen matchen:** file search (RAG), code interpreter, web search / **Grounding with Bing**, memory (preview), MCP-servers (remote + custom op Azure Functions via `/runtime/webhooks/mcp`), en custom function calling (om naar de klant-CRM te schrijven).

**Multi-agent-orkestratie** van de 6 stappen: het **Microsoft Agent Framework** (fusie van Semantic Kernel + AutoGen, public preview okt 2025) bovenop Foundry. Ondersteunt connected agents, stateful multi-step workflows, OpenAPI-tools, MCP en A2A. → een set gespecialiseerde agents (Research-agent, Content-agent, SEO-agent, Sales-agent) die samenwerken.

**SDK's:** Python `azure-ai-projects>=2.0.0`, JS `@azure/ai-projects`, .NET `Azure.AI.Projects` + `.Agents` + `Azure.AI.Extensions.OpenAI`, Java `azure-ai-projects`/`azure-ai-agents`. Plus de gewone OpenAI SDK tegen `https://<resource>.openai.azure.com/openai/v1` voor max OpenAI-compat/laagste latency/embeddings.

### 3.2 "Standard agent setup" = alles in de eigen tenant (BYO-stores)

De **standard** setup (i.t.t. "basic" met Microsoft-managed opslag) slaat ALLE agent-data op in JOUW Azure-resources via **capability hosts**. Dit is exact wat de klant wil. Vereist BYO:

| Store | Rol | Eis / prijs |
|---|---|---|
| **Azure Cosmos DB for NoSQL** | thread/conversation storage (agent-state) | **min. 3000 RU/s** (= 3 containers × 1000 RU/s per project); ~$0,25/GB/mnd + RU/s; gratis tier 1000 RU/s + 25 GB |
| **Azure Storage** | geuploade files + chunks/embeddings | centen |
| **Azure AI Search** | vector stores voor RAG/GEO | Free $0 (dev) / Basic ~$75/mnd / S1 ~$250/mnd (realistisch startpunt) |
| **Azure Key Vault** | secrets | paar cent per 10k operaties |

> **Pitfall — Cosmos RU/s-bodem:** standard agent setup faalt (`CapabilityHostProvisioningFailed`) als Cosmos < 3000 RU/s heeft. Per project +3000 RU/s. Bij veel tenants/projecten loopt dit op → reken op een vaste maandbodem of gebruik Cosmos serverless waar mogelijk.
> **Pitfall — capability host is onveranderlijk:** je kunt 'm NIET updaten na creatie. Verkeerde config = project verwijderen en opnieuw. **De Bicep-template moet in één keer goed zijn** vóór je per-tenant uitrolt.

**RBAC-rollen** die de project-managed-identity nodig heeft op de BYO-stores: Cosmos DB Operator + **Cosmos DB Built-in Data Contributor** op database `enterprise_memory`, Storage Account Contributor + Storage Blob Data Owner/Contributor op de agent-blobstores, Search Index Data Contributor + Search Service Contributor. Developers krijgen rol **"Foundry User"** (oude naam: Azure AI User).

### 3.3 Hosting van het kleine API-servertje

**Azure Container Apps (ACA, Consumption) = de beste default.** Serverless containers, scale-to-zero, per-seconde billing. Bonus: de Foundry standard-agent-networking draait zélf al op ACA (delegated subnet `Microsoft.App/environments`), dus VNet-integratie is consistent.

- Gratis grant: eerste **180.000 vCPU-sec + 360.000 GiB-sec + 2 mln requests per subscription per maand** → vaak **$0** voor een kleine API. Daarna ~$0,000024/vCPU-sec.

**Azure Functions (Consumption / Flex Consumption)** voor pure webhooks + cron: lead-intake, mail-parser, wekelijkse blog-publish-trigger, custom MCP-tools.

- Gratis grant: 1M executions + 400.000 GB-s/maand; daarna $0,20/1M + $0,000016/GB-s. Wekelijkse bots = effectief gratis.
- Flex Consumption: $0,40/M executions + $0,000026/GB-s; gratis 250k exec + 100k GB-s.

> **Pitfall:** SWA **managed** Functions ondersteunen **alleen HTTP-triggers** (geen timer/queue). Cron-werk (auto-blog, rank-tracking) moet in een **aparte** Function App of Container App.
> **Pitfall:** default cron in Azure Functions is **UTC**. Zet `WEBSITE_TIME_ZONE = "W. Europe Standard Time"`, anders publiceren de bots een uur/twee verkeerd (NL zomertijd).

### 3.4 Hosting van de marketingsite

**Azure Static Web Apps (SWA).**
- **Free** = $0 (globaal CDN, gratis auto-SSL, 2 custom domeinen, 3 staging-omgevingen, 250 MB, managed Functions) — **geen SLA, door MS bedoeld voor hobby**.
- **Standard** = **$9/app/mnd** (SLA, 5 domeinen, 10 staging, 500 MB, BYO Functions, private endpoints, custom auth). **Voor een betalende klant: Standard** (je wilt een SLA).
- **Het Dedicated-plan is per 31 okt 2025 retired** — kies alleen Free of Standard.
- Alternatief, nóg goedkoper als je geen geïntegreerde API-routes nodig hebt: **Azure Blob static website** (`$web`-container, alleen storage + egress).

**Form-handling op SWA** = HTTP-getriggerde Function in dezelfde SWA → valideert → schrijft naar Cosmos/Table Storage → mail via ACS Email. Geen aparte server, geen CORS-gedoe.

> **Optionele enterprise-edge** (Front Door + CDN, ~$17,52/app/mnd, public preview): **GDPR-let-op — Front Door/CDN zijn NON-regionale services, edge-cache kan de EU Data Boundary verlaten.** Alleen inzetten als de klant cross-border cachen accepteert; anders SWA-regio pinnen op West/North Europe.

### 3.5 Data/opslag-laag

| Doel | Dienst | Prijs-indicatie |
|---|---|---|
| Leads + conversaties + consent (multi-tenant) | **Cosmos DB serverless**, partition op `tenantId` | $0,25/1M RU's + storage, geen minimum |
| Agent thread-state (standard setup) | Cosmos DB for NoSQL (zie §3.2) | min. 3000 RU/s |
| SEO-metadata (keywords, rank-historie, indexatie-log, embeddings-cache) | **Azure Table Storage** | ~enkele euro's/mnd (fors goedkoper dan Cosmos voor simpele key-value) |
| Vector store (interne links + RAG/GEO) | **Azure AI Search** (vector index) of Cosmos vector-search | AI Search Basic ~$75/mnd; voor kleine sites Cosmos serverless of in-memory numpy in de Function vaak goedkoper |
| Files/embeddings/artefacten | Azure Storage (Blob) | centen |

> **Pitfall — multi-tenant data-lekkage:** zonder strikte `tenantId`-partitionering in Cosmos + per-tenant Key Vault/Managed Identity loop je risico dat lead-data van klant A bij klant B komt = **AVG-datalek met meldplicht**. Tenant-isolatie moet **by-design**, niet by-convention.

### 3.6 E-mail

**Azure Communication Services (ACS) Email** vervangt de fragiele BotLease IMAP-poller + Hostnet-SMTP.
- **$0,00025/e-mail + $0,00012/MB** → 3.000 mails/maand ~$0,75.
- EU-data in NL/IE/CH (binnen EU Data Boundary), GDPR/SOC2-gecertificeerd.
- Per tenant een **geverifieerd afzenderdomein (SPF/DKIM/DMARC)** — ACS dwingt domeinverificatie af.

> **Pitfall — deliverability:** zonder correct SPF/DKIM/DMARC per tenant-domein belanden auto-replies in spam. Neem domeinverificatie op in het per-klant deploy-script, anders "werkt het niet" bij oplevering.

### 3.7 Identity, networking, observability (cross-cutting)

- **Entra ID + Managed Identity (keyless).** In productie de **specifieke `ManagedIdentityCredential`** (niet `DefaultAzureCredential` — vermijdt latency, credential-probing en onbedoelde fallback-paden). Agent-identity + **On-Behalf-Of (OBO)** passthrough naar downstream-systemen zonder secrets in code/prompts.
- **Private networking (optioneel, sterk EU-argument):** Foundry, AI Search, Cosmos, Storage en ACA in één VNet met private endpoints; dedicated subnet delegated aan `Microsoft.App/environments`. Sluit publiek internet uit.
  - Private endpoints ~$0,01/uur elk + data-processing; VNet zelf gratis.
  - **Pitfall — regio-lock:** met private networking moeten ALLE Foundry-workspace-resources in dezelfde regio als de VNet staan. Plan regio vooraf.
- **Application Insights** voor end-to-end tracing + **loud-failure alerts** (eerste 5 GB/mnd gratis). Dit is een **harde les uit BotLease**: de news-bot viel 20 mei stil en exit 0 zelfs bij "0 artikelen". Alert op "0 gepubliceerd" / feitcheck-FAIL is verplicht.
- **Azure Policy** "allowed locations = EU" afgedwongen in de Managed-App-template.

---

## 4. Dataflow per pipeline-stap (detail + API's met prijs)

### STAP 1 — Domein / niche / keyword-onderzoek

**Flow:** Research-agent (LLM doet het "denken": niche, doelgroep, intentie, creatieve domeinnaam- en seed-keyword-shortlists) → deterministische cijfers + availability uit externe API's.

| Tool | Doel | Prijs-indicatie | Azure? |
|---|---|---|---|
| Azure OpenAI GPT-4o-mini / GPT-4.1-mini (Data Zone EU) | niche/intentie/positionering + domeinnaam-ideeen | enkele centen tokens per onderzoek | ja |
| **DataForSEO Labs API** | keyword-ideeen, keyword-gap, concurrent-domeinen, ranked keywords | $0,01/task + $0,0001/item (~$110 per 1M kw); Search Intent $0,001/task + $0,0001/kw | nee |
| **DataForSEO Google Ads (Keywords Data) API** | search volume, historisch (sinds 2019), CPC, competition | ~$0,05/task Standard (1-3u) of $0,075/task Live; ~$50-75 per 1M kw; 1 task = tot 1.000 kw | nee |
| **DataForSEO AI Optimization API** | GEO: AI-search-volume/intent + LLM-citatie-tracking (ChatGPT/Perplexity/Gemini/Claude) | pay-per-call binnen hetzelfde deposit | nee |
| **WhoisJSON / WhoisFreaks** | bulk domein-availability (shortlist over veel TLD's) | WhoisJSON ~1.000 gratis/mnd; WhoisFreaks 500 gratis credits | nee |
| **Cloudflare Registrar API (beta)** | uiteindelijke registratie tegen wholesale (geen markup), WHOIS-privacy gratis | geen markup; .nl/.com ~$8-12/jaar | nee |
| Bing Webmaster Tools + DataForSEO Bing Ads | tweede, exactere volume-bron (Microsoft-native) | Bing Webmaster gratis; Bing Ads pay-per-call | nee |

**DataForSEO** is de duidelijke prijs-/kwaliteitswinnaar: pay-as-you-go, **$50 minimum-deposit (credits verlopen niet), geen abonnement**. Een compleet onderzoek per bedrijf typisch **< $1**.

> **Pitfalls stap 1:**
> - **GoDaddy Domains-API** vereist sinds ~mei 2024 ≥50 geregistreerde domeinen of betaald reseller-plan — **niet** als instap.
> - **Cloudflare Registrar-beta** kan (nog) **geen bulk-availability** en geen transfers/renewals → bulk-check via WhoisJSON/WhoisFreaks, registratie via Cloudflare.
> - **Google Keyword Planner heeft geen losse betaalbare API** (loopt via Google Ads API: OAuth2 + developer token + strenge rate-limits). DataForSEO als wrapper bespaart veel onderhoud.
> - **Ahrefs/Semrush API's vermijden als instap** (~$500-1.000+/mnd vast + units, onvoorspelbaar bij wisselend per-tenant volume).
> - LLM-domeinnamen kunnen **merkrechten** schenden of net niet beschikbaar zijn → elke naam tegen availability-API **én** een merkcheck (bv. EUIPO) houden vóór registratie.
> - **AVG:** alleen niet-PII (keywords/branchetermen/domeinen) naar externe API's; **DPA met DataForSEO sluiten** en documenteren dat geen PII de keyword-/domein-API's bereikt.

> **Gate:** de keyword→pagina-map met **menselijke goedkeuring** vóór mass-publish (Google's pSEO-risico, zie stap 3).

### STAP 2 — Marketingsite bouwen

**Flow:** tenant-config (merk, kleuren als `:root`-vars, logo-SVG, content, SEO-tokens) → Python-generator → statische HTML → SWA-deploy.

- Theming is al **CSS-variabele-gebaseerd** in `style_base.py` (`:root` met `--accent`, `--bg`, etc.) → per klant alleen die waarden + logo + naam injecteren = direct eigen merk-look, zonder herontwerp.
- **Verplichte template-lagen** (waren handwerk bij BotLease, worden nu standaard): TL;DR/answer-in-first-200-words, 130-160-woord standalone blokken, FAQPage-schema, named author + Person-schema, llms.txt feitenkaart, mobile-first-patch.
- **Form-handling** = HTTP-Function in de SWA → Cosmos/Table Storage + ACS Email.
- **Analytics:** Umami self-hosted (Container App + PostgreSQL Flexible Server, ~€15-30/mnd, eventueel 1 gedeelde instance voor alle tenants) → cookieloos, GDPR-conform, geen consent-banner. Het bestaande `/api/track`-trackerpatroon stuurt hier al naartoe.

| Tool | Prijs-indicatie |
|---|---|
| Azure Static Web Apps (Standard) | $9/site/mnd (Free $0, geen SLA) |
| Bicep `Microsoft.Web/staticSites` (API 2025-03-01) + `Azure/static-web-apps-deploy` Action of SWA CLI | gratis |
| Astro 5 (optioneel upgrade-pad) | open source |

> **Alternatief/upgrade:** Astro 5 (Content Layer API, server islands, near-0 JS, auto sitemap/RSS) als Thomas later weg wil van de Python-HTML-generator. Voor maximaal hergebruik nu: **eigen Python-generator multi-tenant maken** = sneller. **Beslis dit vroeg** om dubbel werk te voorkomen.

### STAP 3 — SEO + GEO

**Flow:** timer-Functions die elk een "bot" draaien.

| Bot | API/tool | Prijs-indicatie |
|---|---|---|
| Sitemap + sitemap-news builder | eigen code | $0 |
| Indexatie-versnelling | **IndexNow** (bulk POST tot 10.000 URLs/call, key = .txt op root) | **gratis, geen account** |
| Google-lijn (apart!) | Google Search Console API + URL-inspection (+ Bulk Export naar BigQuery) | gratis |
| Schema-validatie (deploy-gate) | Google Rich Results Test API (~25.000 req/dag) + Schema.org validator | gratis |
| Interne links (self-healing graph) | Azure OpenAI `text-embedding-3-small` → cosine-similariteit → Azure AI Search vector | embeddings zeer goedkoop; AI Search Basic ~$75/mnd |
| Entity-laag | Organization/sameAs JSON-LD + **Wikidata-entry (QID)** | gratis/open |
| Rank-tracking | **DataForSEO SERP/Labs** (echt Google.nl) | SERP standard $0,0006/req, live $0,002; Labs vanaf $0,0001/item |

**GEO en SEO zijn twee aparte crawl-doelgroepen.** Slechts ~11% van de domeinen die ChatGPT citeert wordt óók door Perplexity geciteerd → **per-engine tracking verplicht**. ChatGPT's live web-search draait op de **Bing-index** → Bing-indexering (via IndexNow) is een harde voorwaarde voor ChatGPT-zichtbaarheid.

**De grootste upgrade t.o.v. BotLease:** interne links via **embeddings i.p.v. keyword-matching** = self-healing link-graph, nul orphan pages.

> **Pitfalls stap 3:**
> - **Dunne pSEO wordt afgestraft** (Google Helpful-Content / scaled-content-abuse, maart-2026 core-update: 50-80% verkeersverlies). **Nooit duizenden pagina's tegelijk** → progressive rollout: ~100 pagina's → 4-6 wk monitoren → schalen → maandelijks underperformers prunen.
> - **Google ondersteunt IndexNow NIET** (stand 2026) → Google = aparte lijn (sitemaps + GSC + kwaliteit/freshness).
> - **Schema zonder validatie = stille fouten.** Validatie moet een deploy-blokkerende CI-stap zijn.
> - **Freshness telt:** ~29% van AI-Overview-citaties uit 2025-content; pagina's 18+ mnd niet bijgewerkt worden significant minder geciteerd → maak `last-updated` een echte per-pagina datum.
> - **Vrij SERP-scrapen** (huidig BotLease DDG-patroon) is fragiel + juridisch grijs op multi-tenant productieschaal → DataForSEO.

### STAP 4 — Blogs / content (wekelijks)

**Flow (= BotLease news-engine, vertaald):** research → LLM-draft (strikte JSON) → editorial-gate → feitcheck-pass → hero-image → [optioneel] human approval → publiceren + sitemap + IndexNow.

De **Azure-native vorm** is letterlijk wat Microsoft op Build 2026 lanceerde: de **Azure Functions "serverless agents runtime" (public preview, juni 2026)**. Je definieert een agent in een `.agent.md`-bestand met YAML-frontmatter die de **trigger** declareert (cron, bv. `0 0 15 * * *`) + markdown-instructies; companion-files `mcp.json` en `agents.config.yaml` declareren tools. **Microsofts eigen voorbeeld is een "daily news agent"** — exact de BotLease-use-case, maar declaratief. Dit vervangt de launchd-plist + bash-wrapper.

| Tool | Doel | Prijs-indicatie |
|---|---|---|
| Azure Functions Serverless Agents Runtime (`.agent.md`, timer) | orchestrator/scheduler | Flex Consumption: $0,40/M exec + $0,000026/GB-s; gratis 250k exec + 100k GB-s; geen "agents-tax" (scale-to-zero) |
| Foundry Agent Service (Prompt agent + Responses API) | schrijf- + feitcheck-stappen | prompt-agents draaien gratis; betaal tokens + tools |
| Foundry Models — Data Zone EU deployment | de LLM zelf | per-token; Data Zone (EUR) iets boven Global Standard |
| Grounding with Bing Search | research per keyword/onderwerp (evergreen blogs) | **~$35/1.000 queries** — duur, spaarzaam inzetten (niet per pagina) |
| Azure OpenAI `gpt-image-1` / `gpt-image-1.5` | hero-image + alt-tekst | ~$0,011-$0,25/beeld; mini vanaf ~$0,005 (DALL-E 2/3 uit API per 12 mei 2026) |
| Durable Functions | orchestratie + retries + human-in-the-loop | laag bij wekelijkse cadans |

**Cadans:** houd de BotLease-default aan — **wekelijks 2-3 artikelen**, plus periodiek `dateModified`-refresh van pijler-pagina's. Volume is de val, niet AI op zich (86,5% van top-rankende pagina's gebruikt AI-hulp).

**De editorial-gate is je belangrijkste bouwsteen** en moet per tenant strenger: verbied AI-tell-woorden (delve, leverage, moreover, "in conclusion", "in het huidige landschap" — sluit aan op de humanizer-regel + geen lange streepjes), eis ≥2-3 interne + 3-5 externe authoritieve links, paragraaf-lengte-variatie, en een **aparte feitcheck-pass** (draft tegen bron, PASS/FAIL JSON) tegen hallucinatie.

**Named author = #1 E-E-A-T/GEO-hefboom:** per tenant een **echte persoon** van het klant-bedrijf als author (Person-schema + bio-pagina `/auteur/<slug>` + `rel="author"` + sameAs). NOOIT "AI" of generieke Organization.

> **Pitfalls stap 4:**
> - **Silent failure** (BotLease-les): alert op "0 published" / feitcheck-FAIL verplicht.
> - **Dode interne links:** genereer de link-lijst in de prompt **dynamisch uit de actuele sitemap**, niet hardcoded.
> - **Beeld-labelplicht:** EU/DE AI-labelregels (2026) kunnen een "AI-generated" credit bij hero-beelden vereisen → inbouwen.
> - **Idempotentie:** atomic writes + AST/syntax-validatie vóór wegschrijven; seen-state direct persisteren; per-item isolatie (één slecht item crasht de run niet).

### STAP 5 — Inbound leads afvangen + beantwoorden + kwalificeren

**Twee vangnetten** (kopie van BotLease `contact.js` + `chat.js`, Azure-native):
1. **Webformulier** (HTML POST → Azure Function) — betrouwbare basis voor wie niet wil chatten.
2. **AI-chat-widget** → Function-proxy → Foundry Sales-agent — voor wie snel antwoord wil.

**Kwalificatie = LLM-scoring tegen een vast rubriek (BANT/MEDDIC-light) met structured output.** Aan het eind dwingt de agent een JSON af: `{budget, authority, need, timeline, score 0-100, qualified true/false, samenvatting}`. Pas **boven een drempel** routeren naar de klant.

| Tool | Doel | Prijs-indicatie |
|---|---|---|
| Foundry Agent Service + GPT-4o-mini (EU Data Zone) | gesprek + kwalificatie | runtime gratis; ~$0,15/1M in + $0,60/1M out → praktisch een paar €/mnd per tenant |
| Azure Functions (Flex Consumption) | formulier-endpoint, chat-proxy, mail-trigger, CRM-write, anti-spam | 1M exec/mnd gratis |
| Azure Communication Services Email | auto-reply + notificatie | $0,00025/mail |
| Cosmos DB serverless (partition `tenantId`) | leads/scores/consent/conversaties | $0,25/1M RU's |
| **Cloudflare Turnstile** + honeypot + rate-limit | bot-/spam-bescherming (cookieloos, AVG-vriendelijk) | gratis tot 1M verificaties/mnd |
| Bot Framework Web Chat (Direct Line) of eigen widget | chat-UI | open-source gratis; eigen widget = $0 |

> **Pitfalls stap 5:**
> - **OpenRouter/externe modellen (huidige `chat.js` via Gemini/Qwen/Gemma) zijn NIET acceptabel** voor een klant-met-eigen-omgeving — data verlaat de tenant en de EU. Alles via Azure OpenAI/Foundry in EU.
> - **Auto-reply-mail = misbruikrisico.** Zonder Turnstile + rate-limit + honeypot kan een bot mail-bombs triggeren via jouw domein → ACS-rekening + domeinreputatie exploderen. Verifieer ook dat het opgegeven e-mailadres van de lead is.
> - **LLM-kwalificatie kan hallucineren** → houd een mens-in-de-lus voor de doorzet-beslissing (Teams Accept/Reject) en bewaar de redenering.
> - **Consent-logging is geen nagedachte:** leg vast welk privacy-statement/consent de lead zag en wanneer (veld bij de lead in Cosmos) — anders kun je rechtmatigheid niet aantonen bij de AP.

### STAP 6 — Gekwalificeerde lead doorzetten

**Routing-target per tenant configureerbaar** (`target = email | teams | dynamics | hubspot`):

| Bestemming | Hoe | Prijs-indicatie |
|---|---|---|
| E-mail | ACS Email | $0,00025/mail |
| Microsoft Teams Adaptive Card (Accept/Reject) | Logic Apps / Power Automate + Teams-connector | Logic Apps: eerste 4.000 acties/mnd gratis |
| Dynamics 365 | Dataverse-connector / native | Sales Pro $65/user/mnd, Enterprise $95 |
| HubSpot / Pipedrive | REST-API/webhook vanuit Function | HubSpot API gratis op alle tiers |

**Vuistregel routing-laag:** **Logic Apps Consumption** (per-actie, geen per-user-licentie) of gewoon een **Azure Function-call** ($0 extra, meest draagbaar) voor de generieke laag. **Power Automate** ($15/user/mnd) alleen als de klant zélf in Power Platform werkt — schaalt slecht in een agency-in-a-box.

---

## 5. Per-klant-isolatie & "het script runnen"

### 5.1 Drie multi-tenancy-modellen

| Model | Waar staat de data | Wanneer |
|---|---|---|
| **(A) Bureau host alles** — shared subscription, RBAC + `tenantId`-isolatie | in JOUW Azure | goedkoop, schaalbaar; latere kleine klanten die hun Azure niet willen beheren |
| **(B) In de Azure van de klant** — Azure Managed Application + Lighthouse | in de tenant van de KLANT | **Tijmens harde eis**; enterprise-klanten |
| **(C) Hybride** — dezelfde IaC met parameter `deploymentTarget` | beide | aanrader: bouw het product zo dat het beide kan |

### 5.2 "Het script" = Infrastructure-as-Code + orchestrator

Het concrete Azure-patroon: **subscription vending** (Azure Verified Modules, `bicep-lz-vending`) + de **Deployment Stamps**-pattern: één **idempotente** Bicep/Terraform-template, een **per-klant parameterfile**, getriggerd door GitHub Actions / Azure DevOps. **Elke klant = 1 "stamp".** Idempotent = je kunt het script veilig opnieuw draaien.

Microsoft levert kant-en-klare **standard-agent-setup Bicep-templates** (`github.com/microsoft-foundry/foundry-samples`, mappen `43-standard-agent-setup-with-customization` en `15-private-network-standard-agent-setup`). Eén Bicep-deploy maakt: Foundry-resource + project + Cosmos + Storage + AI Search + Key Vault + connections + capability hosts + RBAC. **Reken ~30-45 min provisioning.**

**Per-klant onboarding-script (B-model):**
1. `azd up` / GitHub Action pakt `tenant-config.json` van de klant.
2. Bicep rolt de stamp idempotent uit in de klant-subscription (Managed App).
3. tenant-config injecteren: domein, niche-systeemprompt, merk-kleuren, auteur-Person, BANT-rubriek, routing-target, CRM-keys (→ Key Vault), cadans-cron.
4. ACS-afzenderdomein verifiëren (SPF/DKIM/DMARC).
5. Lighthouse-delegatie (least-privilege RBAC) goedkeuren bij installatie.

> **De referentie-concurrent:** GoHighLevel SaaS Mode bewijst de propositie — bij aankoop draait een "Snapshot" automatisch (sub-account, credentials, template, billing). Dat is exact jullie "script". Verschil: GHL is multi-tenant in HÚN cloud, **niet in de Azure van de klant**. De Azure-native-in-eigen-tenant-variant is juist de niche die GHL **niet** kan.

### 5.3 Isolatie-niveau binnen het klant-model

- **"Project per klant"** binnen één Foundry-account: data-isolatie via aparte Cosmos-/Storage-containers per project — goedkoper.
- **"Resource group / Foundry-resource per klant"**: hardste isolatie, hoogste vaste kost.
- Voor Tijmens eis ("alles in KLANT-eigen tenant") wordt het sowieso **per-klant-subscription** → de Bicep-template draait in de subscription van de klant.

> **Pitfall — vaste bodemkost per tenant:** AI Search Basic/S1 ($75-$250/mnd) + Cosmos RU/s draaien 24/7, ook zonder verkeer. Bij veel kleine klanten eet dat de marge. Overweeg gedeelde Search/Cosmos (project-isolatie + security-filters) waar de klant dat compliance-technisch toestaat — **maar dat botst met "alles in EIGEN tenant"**, dus alleen voor het A/lite-model.
> **Pitfall — Marketplace-doorlooptijd:** een Managed Application via Azure Marketplace vereist Partner Center + ARM-TTK-validatie + MS-review. Voor de **eerste klant (Tijmen) kun je de definitie privé (service catalog) uitrollen** zonder marketplace = sneller.
> **Pitfall — Lighthouse-scope:** vraag alleen minimale RBAC per resource group (least privilege), nooit "Owner" op de hele subscription — anders haken security-bewuste klanten af.

---

## 6. AVG/GDPR & data-residency — de belangrijkste valkuilen

### 6.1 Residency hangt af van het DEPLOYMENT TYPE, niet alleen de regio

Dit is **de #1 fout**:

| Deployment type | Wat gebeurt er | Voor PROJECT X |
|---|---|---|
| **Global Standard** | inference kan in **elke wereldwijde regio** (geen residency-garantie); wel data-at-rest in jouw regio | alleen bij "data-at-rest-in-EU volstaat" |
| **Data Zone Standard (EU)** | prompts/responses **alleen binnen EU-lidstaten** verwerkt | **de echte EU-residency-optie** bij harde EU-only-inference-eis |
| **Standard (regional)** | strikt binnen één regio | strengste |

> **Pitfall — model-lag in EU:** GPT-4o is beschikbaar als Data Zone in **Sweden Central**. Maar **GPT-5.2/5.5 zijn medio 2026 NIET als Data Zone Standard in EU** (alleen US-datazones), wel als Global Standard in Sweden/Poland Central. **Voor een harde EU-eis: pin op een model dat Data-Zone-EU ondersteunt (GPT-4o / GPT-4.1)** of accepteer Global Standard met data-at-rest-in-EU. **Leg dit per klant expliciet vast.**

> **Pitfall — Anthropic/Claude-via-Foundry valt medio 2026 nog NIET onder de EU Data Boundary.** Voor de harde EU-eis: **geen Claude-via-Foundry**, blijf bij Azure OpenAI / Azure-direct modellen. (Verifieer op deploy-moment of de EU-native Claude-deployment inmiddels live is.)

> **Belangrijk onderscheid (medio 2026):** de EU Data Boundary omvat wél Nederland (West Europe), MAAR de Foundry/Azure-OpenAI **Data Zone model-hosting-regio's in de EU zijn momenteel Sweden Central + Germany West Central**; West Europe host niet noodzakelijk elk model. Plan compute/storage in West/North Europe, en kies voor de model-deployment **"Data Zone Standard (EU)"**.

### 6.2 DPA, abuse-monitoring en Zero Data Retention

- Azure OpenAI / Azure-direct modellen vallen onder de Microsoft **Products & Services DPA**: klant-prompts/completions worden **NIET gebruikt om modellen te trainen** en NIET door het systeem opgeslagen (los van wat jij zelf in Cosmos/Storage opslaat). Microsoft = data-processor; klant = controller. **EU Data Boundary (mei 2026) dekt o.a. NL, FR, DE, IT, NO, PL, ES, SE, CH.**
- Standaard logt Azure OpenAI prompts/responses **~30 dagen** voor abuse-monitoring (mogelijke human review). Voor een privacy-gevoelige klant: vraag **"Modified Abuse Monitoring"** (geen human review) en/of **Zero Data Retention** aan via het Limited Access-programma.
  > **Pitfall:** **ZDR vereist een Enterprise Agreement of Microsoft Customer Agreement — NIET op pure pay-as-you-go.** Tijmens klant draait waarschijnlijk al op EA/MCA (haalbaar); BotLease zelf (eenmanszaak, PAYG) niet. **Beloof "data wordt niet bewaard" nooit voordat je dit hebt bevestigd.**

### 6.3 EU AI Act (verkoopargument + verplichting)

- **EU AI Act Art. 50-transparantieplicht treedt aug 2026 in werking** → de sales-/lead-chatbot **MOET bij eerste interactie melden dat het AI is** ("Je praat met een AI-assistent"). Boetes tot €35M of 7% omzet. Maak deze disclosure + consent-logging een **verplicht, niet-uitschakelbaar** onderdeel van elke tenant-deploy.

### 6.4 Externe SaaS (DataForSEO, Whois, Cloudflare)

Niet-Azure SaaS botst niet met "alles in eigen Azure" **zolang er geen PII van de eindklant naartoe gaat** (alleen keywords/branchetermen/domeinen). **Leg dit expliciet vast, sluit DPA's**, en check serverlocatie/sub-processors van DataForSEO.

---

## 6b. Rapportage- & meet-component (de waardebewijslaag)

> Onderbouwing en KPI-set: zie **[05-meten-en-succes.md](05-meten-en-succes.md)**. Dit is hoe het in de architectuur landt.

Zonder dit weet de klant niet of het werkt, en stuurt het systeem zichzelf niet bij. Eén component, drie functies:

- **`report`-Function (Azure Functions, timer, wekelijks + maandelijks):** trekt per tenant data uit GSC Performance API + Bing Webmaster + DataForSEO (rank/SERP) + de site-analytics + de eigen lead-DB (Cosmos), en schrijft een **snapshot** weg (per-tenant equivalent van BotLease' `seo_data.json`) zodat je historie/trends hebt. Bron-keuze bewust: NL-rankings via DataForSEO/GSC, niet via een US-zoektool (BotLease-les).
- **Per-klant maandrapport / dashboard:** de tastbare waarde-levering. Toont de **north-star** (gekwalificeerde leads/maand uit organisch + cost-per-qualified-lead) + de funnel (indexatie → posities → impressies → verkeer → leads → qualified) + top-bewegers + GEO-citatie-stand. Genereerbaar als statische HTML (zelfde generator-stijl) of in een klein dashboard.
- **Alerts (Logic App / App Insights):** harde BotLease-les (stille uitval) → waarschuw bij `0 gepubliceerd`, `feitcheck-FAIL`, `indexatie gedaald`, `ranking-drop > X`, `spam-spike op lead-formulier`. Een systeem dat stilvalt zonder melding is erger dan geen systeem.
- **Self-optimization-haakje:** de rank-/CTR-data voedt terug in de pipeline (lage CTR → title/meta herschrijven; pagina blijft hangen op pos 11-20 → content verdiepen/intern linken). Eerst mens-in-de-lus (kijkt naar het rapport), automatiseren pas als het patroon bewezen is.

Dataflow: `report-Function → {GSC, Bing, DataForSEO, analytics, Cosmos lead-DB} → snapshot (Storage/Cosmos) → maandrapport (HTML) + alerts (Logic App)`.

---

## 7. Indicatieve maandkosten per tenant (B-model, in klant-subscription)

> **Let op:** dit zijn ruwe indicaties uit de bevindingen. **Foundry-prijzen veranderen snel** (memory-billing start 1-6-2026, hosted-compute 22-4-2026) — **verifieer de live pricing-pagina vóór elke offerte** en reken een buffer.

| Component | Vast/variabel | Indicatie |
|---|---|---|
| Azure Static Web Apps (Standard) | vast | ~$9/mnd |
| Azure AI Search (Basic) | **vast (bodem)** | ~$75/mnd (S1 ~$250 bij meer RAG) |
| Cosmos DB (≥3000 RU/s voor agent-state) | **vast (bodem)** | RU/s-afhankelijk (gratis tier dekt 1000 RU/s) |
| Container Apps / Functions (API + bots) | variabel | vaak ~$0 binnen free grant |
| Azure OpenAI tokens (GPT-4.1-mini bulk + GPT-4o-mini chat) | variabel | enkele €/mnd bij normaal volume |
| ACS Email | variabel | ~$0,75 per 3.000 mails |
| Grounding with Bing (alleen waar nodig) | variabel | ~$35/1.000 queries — spaarzaam |
| Umami analytics (eventueel gedeeld) | vast | ~€15-30/mnd PostgreSQL |
| DataForSEO (extern, gedeeld deposit) | variabel | onderzoek < $1/bedrijf; rank-tracking enkele €/wk |

**De vaste bodemkost** (AI Search + Cosmos RU/s + SWA) is dominant — dat is het verschil tussen LLM-verbruik (laag) en 24/7-resources (vast). Prijsmodel-aanrader uit de markt: **setup-fee (de "script-run") + maandelijkse beheer/AI-fee**, want de klant draagt zelf de Azure-verbruikskosten. Markt-benchmark: HighLevel ~$497/mnd agency; AI-bureaus mid-market $5K-$25K/mnd.

---

## 8. Belangrijkste open vragen (vóór de eerste build met Tijmen)

1. **Deploy-model:** alles in de EIGEN subscription van de klant (Managed App + Lighthouse), of een dedicated resource group in JOUW tenant? Bepaalt de hele kostenstructuur en wie de Azure-rekening betaalt.
2. **EU-eis hoe hard:** data-at-rest-in-EU (Global Standard volstaat, nieuwste modellen beschikbaar) vs. EU-only-INFERENCE (Data Zone Standard EU, beperkt tot GPT-4o/4.1)?
3. **EA/MCA aanwezig?** Bepaalt of Zero Data Retention / Modified Abuse Monitoring haalbaar is.
4. **Gedeelde vs. per-tenant AI Search/Cosmos?** Goedkoper vs. hardste isolatie — botst met "alles in eigen tenant".
5. **CRM-bestemming:** Dynamics 365, HubSpot, Pipedrive of niets? Bepaalt routing + of de native Dynamics Qualification Agent inzetbaar is.
6. **Private networking** eis of nice-to-have? Sterk compliance-argument, maar regio-lock + complexiteit.
7. **Named author per klant:** echte persoon bij de klant (sterkste E-E-A-T-signaal) of merk-persona?
8. **Sales-agent autonoom** of altijd human-in-the-loop (BotLease-regel "geen autonome koude mails")? Bepaalt agent-architectuur + AI-Act-risicoprofiel.
9. **Verwerkersrollen:** het bureau is vermoedelijk (sub)verwerker namens de klant → **verwerkersovereenkomst bureau↔klant** bovenop de Microsoft DPA. Template aanleveren/laten opstellen.
10. **Generator-keuze:** eigen Python-generator behouden (snelste hergebruik) of overstappen op Astro (toekomstvaster)? Nu beslissen voorkomt dubbel werk.
11. **Port-pad bestaande bouwstenen:** Thomas' Python (news-engine, IMAP-poller, CRM-webhook) porteren naar Functions/Container Apps, of als referentie-architectuur herbouwen? Bepaalt de tijdsinvestering van de eerste tenant-build.

---

## 9. Bronnen (selectie, geverifieerd in het onderzoek 2025/2026)

- Microsoft Foundry Agent Service — overview: https://learn.microsoft.com/en-us/azure/foundry/agents/overview
- Standard agent setup (BYO Cosmos/Storage/Search): https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/standard-agent-setup
- Deployment types (Data Zone vs Global): https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types
- Foundry SDK's & endpoints: https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/sdk-overview
- Foundry standard-agent-setup Bicep-templates: https://github.com/microsoft-foundry/foundry-samples
- Azure Managed Applications: https://learn.microsoft.com/en-us/azure/azure-resource-manager/managed-applications/
- Azure Lighthouse (ISV): https://learn.microsoft.com/en-us/azure/lighthouse/concepts/isv-scenarios
- Deployment Stamps pattern: https://learn.microsoft.com/en-us/azure/architecture/patterns/deployment-stamp
- Subscription vending (AVM): https://azure.github.io/Azure-Landing-Zones/sub-vending/
- Microsoft Agent Framework: https://azure.microsoft.com/en-us/blog/introducing-microsoft-agent-framework/
- Azure Functions serverless agents runtime (Build 2026, `.agent.md`): https://techcommunity.microsoft.com/blog/appsonazureblog/azure-functions-at-build-2026-update/4524075
- Azure Container Apps pricing: https://azure.microsoft.com/en-us/pricing/details/container-apps/
- Azure Static Web Apps plans (Free/Standard, Dedicated retired): https://learn.microsoft.com/en-us/azure/static-web-apps/plans
- Azure Functions pricing: https://azure.microsoft.com/en-us/pricing/details/functions/
- Azure AI Search tiers: https://learn.microsoft.com/en-us/azure/search/search-sku-tier
- Cosmos DB serverless pricing: https://azure.microsoft.com/en-us/pricing/details/cosmos-db/serverless/
- ACS Email pricing + EU Data Boundary: https://learn.microsoft.com/en-us/azure/communication-services/concepts/email-pricing
- Foundry Models / data-privacy (DPA): https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy
- EU Data Boundary: https://learn.microsoft.com/en-us/privacy/eudb/eu-data-boundary-learn
- EU AI Act transparantie (Art. 50): https://artificialintelligenceact.eu/transparency-rules-article-50/
- DataForSEO pricing: https://dataforseo.com/pricing
- DataForSEO AI Optimization API: https://docs.dataforseo.com/v3/ai_optimization-overview/
- Cloudflare Registrar API (beta): https://blog.cloudflare.com/registrar-api-beta/
- IndexNow: https://www.indexnow.org/documentation
- Grounding with Bing (pricing): https://www.microsoft.com/en-us/bing/apis/grounding-pricing
- Cloudflare Turnstile: https://www.cloudflare.com/products/turnstile/
- Wikidata: https://www.wikidata.org/
- GoHighLevel (benchmark): https://www.gohighlevel.com/white-label-crm
