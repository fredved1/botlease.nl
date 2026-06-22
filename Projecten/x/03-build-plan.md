# PROJECT X — Bouwplan (gefaseerd)

> **Doel van dit document.** Een concreet, gefaseerd plan zodat Thomas PROJECT X kan bouwen (het "AI-marketingbureau in een doos") en straks per nieuwe klant **alleen een script hoeft te runnen**. Doelgroep: Thomas (bouwer) + Tijmen (klant-kant, IT Connect Almelo).
>
> **Toon.** Eerlijk, geen hype, geen overpromise. Waar de bevindingen onzeker zijn, staat dat er expliciet bij. Prijzen en feiten komen uit het onderzoek; **alle Azure-prijzen en Foundry-features op offerte-/bouwmoment opnieuw verifiëren** — Microsoft Foundry verandert snel (productnaam, SDK's, en sommige facturering, zoals agent-memory, start pas in 2026).

---

## 0. Leeswijzer: vier fasen + het onboarding-script

| Fase | Wat | Resultaat | Wat mag nog HANDMATIG |
|---|---|---|---|
| **Fase 0** | Fundament: Azure-setup, keuzes, compliance-kaders | Eén werkende "lege" tenant-stack + besluitenlijst | Bijna alles is opzetwerk |
| **Fase 1** | MVP: 1 klant end-to-end, deels met de hand | Eerste klant (via Tijmen) live met site + leads + content | Onderzoek goedkeuren, content-review, deploy met de hand |
| **Fase 2** | Automatisering van elke losse stap | Elke van de 6 stappen draait als losse, geteste agent/Function | Het aan-elkaar-knopen tot één run |
| **Fase 3** | Multi-tenant: "1 script per klant" | Eén `azd up` + config-file = nieuwe klant | (Bijna) niets meer |

**Kernregel door alle fasen heen (uit de bevindingen):** automatiseer pas wat je minstens één keer met de hand hebt zien werken. Eerst de keten bewijzen op één klant (Fase 1), dan elke stap los betrouwbaar maken (Fase 2), dan pas de onboarding scripten (Fase 3). Onder ~5 klanten in jaar 1 is volledige automatisering deels over-engineering — een half-handmatig script kan dan al volstaan.

---

## De 6 functionele stappen (waar PROJECT X om draait)

1. **Domein-/niche-/keyword-onderzoek** (LLM + DataForSEO + domein-availability)
2. **Marketingwebsite bouwen** (generator → Azure Static Web Apps)
3. **SEO + GEO automatiseren** (sitemaps, schema, llms.txt, IndexNow, interne links via embeddings, rank-tracking)
4. **Blog/content automatisch publiceren** (research → draft → feitcheck-gate → publiceren)
5. **Inbound sales-leads afvangen + automatisch beantwoorden + kwalificeren** (formulier + chatbot → Foundry-agent → BANT-JSON)
6. **Gekwalificeerde leads doorzetten naar de klant** (e-mail / Teams / CRM)

Deze stappen zijn 1-op-1 te mappen op Thomas' bestaande BotLease-bouwstenen (news-engine, CRM, IMAP-poller, SEO-scripts, rank-tracker). Het hergebruik is conceptueel (de pijplijn-logica en de gates), niet letterlijk de code — de runtime verschuift van "Mac + VPS + cron + OpenRouter/Claude-CLI" naar "Azure Functions + Foundry + Azure OpenAI in de EU".

---

## FASE 0 — Fundament & Azure-setup

**Doel:** een lege, werkende, compliant Azure-stack in één EU-regio, plus de harde keuzes vastgelegd. Nog géén klant-functionaliteit; wel: "een agent kan binnen de EU een token verbranden via Managed Identity, en niets staat buiten de EU."

### 0.1 Besluiten die ALLES bepalen (eerst beslissen, met Tijmen)
Deze open vragen uit het onderzoek blokkeren de architectuur. Leg ze schriftelijk vast vóór je bouwt:

- **Deploy-model:** draait alles in de **eigen Azure-subscription van de klant** (Tijmens harde eis → Azure Managed Application + Lighthouse), of accepteert een klant later een resource group in **jullie** Azure (goedkoper, deelbaar)? Bouw de IaC zó dat dezelfde template **beide** aankan via een parameter `deploymentTarget`.
- **Hoe hard is de EU-eis?** Onderscheid (de #1 valkuil):
  - *Data-at-rest in EU* → makkelijk, `Global Standard` deployment volstaat.
  - *EU-only verwerking (inference)* → vereist **`Data Zone Standard (EU)`** deployment. Dit beperkt de modelkeuze: GPT-4o / GPT-4.1 zijn als Data-Zone-EU beschikbaar (Sweden Central), maar **GPT-5.x is medio 2026 NIET als Data Zone Standard in EU** (alleen US-datazones, of EU als Global Standard). Pin per klant model + deployment-type expliciet vast.
- **Heeft de klant een EA/MCA?** Bepaalt of **Zero Data Retention** haalbaar is (ZDR werkt NIET op pure pay-as-you-go). Tijmens klant draait waarschijnlijk op EA/MCA → haalbaar; BotLease zelf (eenmanszaak, PAYG) → niet.
- **Mag de pijplijn naar buiten bellen?** DataForSEO, IndexNow, Wikidata, domein-API's zijn per definitie externe SaaS. Spreek af dat alleen **niet-persoonsgebonden** data (keywords, branchetermen, domeinnamen) naar buiten gaat en **PII (lead-namen/e-mails) strikt in Azure-EU** blijft. Leg dit vast in DPA's/verwerkersovereenkomst.
- **Regio:** West Europe (Amsterdam) of Sweden Central. Let op de nuance: **EU Data Boundary** dekt NL (West Europe), maar de **model-hosting "Data Zone"-regio's** voor de zwaarste modellen zijn vaak Sweden Central / Germany West Central. Plan compute/storage in West Europe; kies model-deployment bewust. Bij private networking (VNet) moeten **alle** workspace-resources in dezelfde regio staan — regio-keuze vóóraf vastleggen.

### 0.2 Concrete taken
1. Azure-subscription + Entra-tenant gereed; iemand met **Owner / User Access Administrator** om RBAC toe te kennen tijdens provisioning.
2. **Resource group in een EU-regio** + Azure Policy "allowed locations" (verbied resource-creatie buiten EU).
3. **Microsoft Foundry resource + project** met **standard agent setup** (niet "basic"): koppel BYO-resources zodat agent-state in de tenant blijft:
   - **Azure Cosmos DB for NoSQL** (thread/conversatie-opslag; let op: standard setup faalt onder **3000 RU/s** per project — `CapabilityHostProvisioningFailed`).
   - **Azure Storage** (geüploade files + chunks/embeddings).
   - **Azure AI Search** (vector stores / RAG).
   - **Azure Key Vault** (secrets).
   - *Tip:* gebruik Microsofts **Bicep-template** `43-standard-agent-setup-with-customization` (of `15-private-network-...` bij VNet) uit `github.com/microsoft-foundry/foundry-samples`. Eén deploy maakt Foundry + project + Cosmos + Storage + Search + Key Vault + connections + capability hosts + RBAC. Reken ~30-45 min.
   - ⚠️ **Capability host is onveranderlijk** — niet te updaten na creatie. Krijg de template in één keer goed vóór je per-tenant uitrolt; fout = project verwijderen en opnieuw.
4. **Keyless auth opzetten:** Managed Identity i.p.v. API-keys. Project-MI rollen geven: Cosmos DB Operator + Cosmos DB Built-in Data Contributor (op `enterprise_memory`), Storage Blob Data Owner/Contributor, Search Index Data Contributor + Search Service Contributor. Developers: rol **Foundry User** (oude naam: Azure AI User). In productie de specifieke `ManagedIdentityCredential` gebruiken, **niet** `DefaultAzureCredential` (latency / credential-probing / onbedoelde fallback).
5. **Eén model-deployment** als `Data Zone Standard (EU)` (start met **GPT-4.1-mini** als werkpaard; GPT-4.1 voor zwaardere reasoning). Plus een **embeddings-deployment** (`text-embedding-3-small`) voor interne links.
6. **Hosting-laag opzetten:** **Azure Container Apps (Consumption, scale-to-zero)** voor het kleine API-servertje/orchestratie; **Azure Functions (Consumption/Flex)** voor webhooks + cron-triggers; **Azure Static Web Apps (Standard, $9/site)** voor de site.
7. **Compliance-knoppen aanvragen** (als de klant EU-only/strikt wil): **Modified Abuse Monitoring** (geen human review) en evt. **Zero Data Retention** via het Limited Access-programma. Anders logt Azure OpenAI standaard prompts/completions ~30 dagen.
8. **AI Act / AVG-bouwstenen klaarzetten:** een herbruikbaar "Je praat met een AI-assistent"-disclosure-blok (AI Act Art. 50, vanaf aug 2026 verplicht) + consent-logging-veld. En een **verwerkersovereenkomst-template** tussen bureau en klant (bureau is sub-verwerker; Microsoft is verwerker via de DPA).

### 0.3 "Klaar" als…
- Een test-call `AIProjectClient(endpoint, ManagedIdentityCredential()).get_openai_client().responses.create(...)` werkt vanuit een Container App, **zonder enige API-key in code**, tegen een **EU Data Zone**-model.
- Cosmos/Storage/Search/Key Vault staan in de EU-regio en de project-MI heeft de juiste RBAC.
- De vier kernbesluiten uit 0.1 staan schriftelijk vast (deploy-model, hardheid EU-eis, EA/MCA-status, externe-API-grens).
- Azure Policy blokkeert non-EU-regio's.

---

## FASE 1 — MVP: 1 klant end-to-end (deels handmatig)

**Doel:** de eerste klant (via Tijmen) volledig live krijgen — site + GEO/SEO-basis + werkende lead-afvang + minstens één gepubliceerd blog — waarbij Thomas de "denk"-stappen nog **met de hand goedkeurt**. Dit bewijst de keten vóór je hem automatiseert.

> **Filosofie van Fase 1:** alles wat *oordeel* vereist (welke keywords, welke niche, is de content goed, mag deze lead door) doet Thomas handmatig of met een approval-knop. De machine doet het *uitvoerende* werk (data ophalen, HTML genereren, mail versturen).

### Stap 1 — Domein-/niche-/keyword-onderzoek (MVP)
- **Handmatig + LLM-assist:** LLM (Azure OpenAI GPT-4.1-mini in EU) genereert uit "bedrijf + branche" een niche-beschrijving, doelgroep, seed-keywords en domeinnaam-shortlist.
- **Echte cijfers deterministisch:** DataForSEO **Labs API** (keyword-ideeën, competitor-domeinen, keyword-gap, search-intent) + **Google Ads (Keywords Data) API** (volume, CPC, competition). Eén compleet onderzoek per bedrijf kost typisch **< $1**. Deposit $50, geen abonnement.
- **Domein-check:** shortlist door een **bulk-availability-API** (WhoisJSON ~1.000 gratis/mnd of WhoisFreaks 500 credits) halen; registreren later via **Cloudflare Registrar** (wholesale, geen markup) — *Cloudflare-beta kan nog géén bulk-check, dus scheiden.*
- **Mens beslist:** Thomas (en/of de klant) kiest de definitieve niche + keywords + domein. **Geen autonome mass-publish** — gezien Google's pSEO-risico is een menselijke gate hier verstandig.
- ⚠️ Elke door de LLM verzonnen domeinnaam tegen de availability-API **én** een merkcheck (EUIPO) houden vóór registratie.

### Stap 2 — Marketingwebsite bouwen (MVP)
- **Hergebruik Thomas' generator** (`scripts/build_*.py` + `*_data.py` + `style_base.py` + `seo_common.py`), nu tenant-config-driven gemaakt: per klant een `config.json` met merknaam, kleuren (de `:root` CSS-vars zitten er al in), logo/SVG, content en SEO-tokens.
- **Bak de mobile-first-patch standaard in de template** — anders herhaalt het BotLease-"niet rebuilden"-probleem zich per klant.
- **Verplichte GEO-laag in de template** (geen handwerk meer): Organization/LocalBusiness-schema met `sameAs`, FAQPage-schema, TL;DR/answer-capsule (40-60 woorden onder elke H2), llms.txt feitenkaart, named author + Person-schema.
- **Hosting:** Azure Static Web Apps (Standard). Regio pinnen op West/North Europe. Deploy via `az staticwebapp secrets list --query properties.apiKey` + de SWA CLI of de GitHub Action — of netter via OIDC federated credentials (geen secrets opslaan).
- **Vercel-resten eruit:** `/_vercel/insights`, `vercel.json`, `.vercel/` werken niet op Azure en moeten vervangen worden.
- **Analytics:** Umami self-hosted (Container App + PostgreSQL Flexible Server) i.p.v. Vercel Insights — cookieloos, GDPR-conform. Eén gedeelde Umami kan voor meerdere tenants.

### Stap 3 — SEO + GEO (MVP)
- **Sitemaps + schema + llms.txt** genereren (Thomas heeft dit al; in template bakken).
- **IndexNow-ping** (hergebruik `indexnow_ping.py`) — key per tenant-domein, urlList uit de sitemap. Gratis. ⚠️ **Google ondersteunt IndexNow niet** → Google apart via Search Console + sitemaps.
- **Schema-validatie als deploy-blokkerende stap** (Google Rich Results Test API + Schema.org validator) — dit gat zit nu nog in BotLease.
- **Entity-laag (hoogste ROI):** per klant één **Wikidata-entry** (QID) aanmaken + `sameAs`-block injecteren naar Wikidata/LinkedIn/KvK. In Fase 1 mag dit handmatig.
- **Rank-tracking:** in MVP mag de bestaande DDG/Bing-scrape (`rank_bot.py`) nog, maar plan de upgrade naar **DataForSEO SERP/Labs** voor echte Google.nl-data (verdedigbaarder voor een betalende klant).

### Stap 4 — Blog/content (MVP)
- **Hergebruik de news-engine-logica** (`news_bot.py`): research → LLM-draft naar **strikte JSON** → **editorial_gate** → publiceren → sitemap → IndexNow.
- **Runtime-vervanging:** de Claude-CLI/OpenRouter-route vervalt; LLM-call gaat via **Foundry Responses API** met EU Data Zone + Managed Identity. De JSON-schema-prompt en gate-logica blijven 1-op-1.
- **Research-bron:** in MVP RSS-feeds (zoals BotLease) of **Grounding with Bing Search** (Foundry-tool, ~$35/1.000 transacties — **spaarzaam**, alleen voor echte research, niet per pagina).
- **Cadans:** wekelijks 2-3 artikelen. **NOOIT honderden tegelijk** (Google's scaled-content-abuse straft 50-80% verkeersverlies).
- **Named author = echte persoon** bij de klant (Person-schema + /auteur/-pagina). #1 E-E-A-T/GEO-hefboom.
- **Mens-in-de-lus:** in Fase 1 keurt Thomas (of de klant) elk artikel goed vóór publicatie.

### Stap 5 — Sales-leads afvangen + beantwoorden + kwalificeren (MVP)
- **Dubbel vangnet:** (1) HTML-formulier → Azure Function, (2) AI-chat-widget. Hergebruik Thomas' patroon (`contact.js` + `chat.js`), maar Azure-native.
- ⚠️ **OpenRouter/Gemini/Qwen (huidige chat.js) mag NIET** — data verlaat de tenant/EU. Alles via **Azure OpenAI / Foundry-agent in de EU**.
- **Anti-spam (verplicht vóór live):** Cloudflare Turnstile (cookieloos, 1M/mnd gratis) + server-side honeypot + per-IP rate-limit. Zonder dit kan een bot je auto-reply-mail misbruiken (mail-bomb → ACS-rekening + domeinreputatie kapot).
- **Auto-reply:** Foundry-agent stelt op, een Function verstuurt via **Azure Communication Services Email** ($0,00025/mail). Per tenant een geverifieerd afzenderdomein (SPF/DKIM/DMARC — opnemen in deploy, anders spam bij oplevering).
- **Kwalificatie:** Foundry Prompt-agent voert BANT-gesprek, dwingt **structured-output JSON** af: `{budget, authority, need, timeline, score, qualified, samenvatting}`.
- **Opslag:** Cosmos DB serverless, **gepartitioneerd op `tenantId`** (harde data-scheiding). Consent-veld meebewaren.

### Stap 6 — Gekwalificeerde lead doorzetten (MVP)
- **Mens-in-de-lus by design:** boven de score-drempel → **Teams Adaptive Card met Accept/Reject** (via Logic Apps Consumption) of e-mail naar de klant. Bewaar de kwalificatie-redenering, zodat de klant kan corrigeren (sluit aan bij BotLease' "geen autonome koude mails"-regel).
- **Routing-target = config per tenant:** `email | teams | dynamics | hubspot`. Microsoft-klant → Dynamics 365; anders HubSpot/Pipedrive via REST vanuit een Function. Voor de generieke laag: **Logic Apps Consumption** of een **Function** (goedkoopst, draagbaarst), **niet** Power Automate per-user (schaalt slecht in agency-model).

### "Klaar" voor Fase 1 als…
- De eerste klant heeft een **live site** op eigen domein (EU-gehost), met GEO/SEO-basis (schema gevalideerd, sitemap + IndexNow, llms.txt, Wikidata-entry).
- Minstens **één blog gepubliceerd** via de pijplijn (met menselijke goedkeuring).
- Een **lead die via formulier én via chat** binnenkomt, krijgt een automatische, EU-conforme reactie, wordt gekwalificeerd tot JSON, en komt als **Accept/Reject** bij de klant terecht.
- Disclosure ("ik ben AI") + consent-logging staan live.
- Alles draait in de EU; geen PII verlaat Azure-EU.

---

## FASE 2 — Automatisering van elke stap

**Doel:** elke van de 6 stappen draait als een losse, geteste, herstartbare bouwsteen — met loud-failure-alerts — zodat er straks weinig handwerk meer in de keten zit. Hier verschuift het werk van "Thomas doet het" naar "een agent/Function doet het, Thomas controleert steekproefsgewijs."

### 2.1 Per stap automatiseren
- **Stap 1 (onderzoek):** wrap DataForSEO + availability-API's als **OpenAPI-tools / MCP-tools** voor een **research-agent**. De agent levert een keyword→pagina-map als JSON. **Menselijke gate blijft** (mass-publish-risico), maar wordt een approval-knop i.p.v. handwerk.
- **Stap 2 (site):** generator draait in een **CI-stap** (Container App of GitHub Action) op basis van `config.json`. Bicep provisioned de SWA.
- **Stap 3 (SEO/GEO):**
  - **Interne links via embeddings** (de grootste upgrade t.o.v. handgemaakte BotLease-links): elke pagina → vector (`text-embedding-3-small`) → cosine-similariteit in Azure AI Search of Cosmos vector-search → self-healing link-graph, nul orphans. Bij kleine sites mag dit goedkoop in-memory (numpy in een Function).
  - **Rank-tracking** overzetten op DataForSEO SERP (echte Google-data).
  - **Schema-validatie** als harde CI-gate.
  - **IndexNow + GSC + Bing** als losse, geplande Functions.
- **Stap 4 (content):** zet de news/blog-pijplijn als **timer-getriggerde agent**. Twee Azure-native vormen:
  - **Azure Functions Serverless Agents Runtime** (`.agent.md` met YAML-cron-trigger + markdown-instructies; companion `mcp.json` / `agents.config.yaml` voor tools). Microsofts eigen showcase is letterlijk een daily-news-agent — exact Thomas' use-case. *Preview (Build 2026) — verifieer GA-status op bouwmoment.*
  - **Durable Functions** voor de meerstaps-orchestratie (research → draft → **feitcheck-pass** → beeld → publish), retries met backoff, en een **wacht-event voor human-in-the-loop approval** (YMYL/eerste runs).
  - **Feitcheck als aparte LLM-pass** (PASS/FAIL JSON: elke claim die niet letterlijk uit de bron volgt → flag). Anti-hallucinatie.
  - **Gate strenger maken:** AI-tell-woorden blokkeren (delve/leverage/moreover/"in het huidige landschap"), ≥2-3 interne + 3-5 externe bronnen eisen, paragraaf-lengte-variatie, humanizer-pass (geen lange streepjes/AI-toon).
  - **Beeld:** `gpt-image-1`/`-mini` voor hero + alt-tekst (DALL-E 2/3 uit de API per 12 mei 2026); evt. "AI-generated"-credit (EU/DE labelplicht 2026).
- **Stap 5 (sales):** Foundry-agent vast, met file-search (RAG over klant-FAQ/catalogus uit AI Search) + function-calling om naar Cosmos te schrijven. Memory (preview) optioneel.
- **Stap 6 (routing):** Logic App / Function-routing per tenant-config; CRM-write geautomatiseerd.

### 2.2 Robuustheid die je MOET overnemen van Thomas' BotLease-ervaring
- **Idempotentie + atomic writes** (temp + replace; nooit corrupt databestand committen; AST/JSON-validatie vóór wegschrijven).
- **Seen-state direct na elke succesvolle publicatie persisteren** (crash mag state niet desyncen); per-item isolatie (één slecht item skipt, crasht de run niet).
- **LOUD failure-detectie** — dé harde les: BotLease' news-bot viel stil en exit'te "0 artikelen" zonder alarm. In Azure: **Application Insights / Foundry-tracing + alert** (Logic App/mail) bij "0 gepubliceerd" of feitcheck-FAIL. App Insights eerste 5 GB/mnd gratis.
- **Cron-tijdzone:** Azure Functions cron is **default UTC** → zet `WEBSITE_TIME_ZONE='W. Europe Standard Time'`, anders publiceert nieuws een uur/twee verkeerd (NL zomertijd).

### 2.3 Datalaag opschonen
- Multi-tenant metadata (keywords, pagina-status, rank-historie, indexatie-log, embeddings-cache): **Azure Table Storage** (fors goedkoper dan Cosmos voor simpele key-value: ~enkele euro's/mnd vs ~$26+/mnd Cosmos serverless). Cosmos houden voor agent-threads + leads.

### "Klaar" voor Fase 2 als…
- Elke 6 stappen draait **zelfstandig** als agent/Function, getest, met retries en een **0-output/FAIL-alert**.
- Content-pijplijn publiceert wekelijks zelf, met feitcheck-gate + humanizer + named author, en valt **luid** als er iets stilstaat.
- Interne links zijn self-healing (embeddings); rank-tracking draait op echte Google-data; schema-validatie blokkeert kapotte deploys.
- Thomas controleert nog **steekproefsgewijs**, maar voert geen routinewerk meer met de hand uit.

---

## FASE 3 — Multi-tenant: "1 script per klant"

**Doel:** een nieuwe klant opzetten = **één commando + één config-file**. Alle losse bouwstenen uit Fase 2 worden geparametriseerd en met Infrastructure-as-Code achter één onboarding-script gezet.

### 3.1 Architectuur-patroon
- **Voor Tijmens eis ("alles in de eigen Azure van de klant"):** publiceer de stack als **Azure Managed Application** — een ZIP met `mainTemplate.json` (Bicep met alle resources) + `createUiDefinition.json` (het intake-formulier). De resources landen in een **managed resource group in de subscription van de KLANT**; jij houdt beheer via een identity in jouw tenant. Koppel **Azure Lighthouse**-delegatie zodat je één control-plane houdt over alle klant-Azures (least-privilege RBAC per resource group, **nooit** Owner op de hele subscription).
  - *Sneller voor de eerste klant:* rol de managed-app-definitie **privé** uit via de service catalog (geen Marketplace-review nodig). Marketplace-publicatie (Partner Center + ARM-TTK + Microsoft-review) komt later.
- **Voor latere "lite"-klanten die in jullie Azure mogen:** dedicated resource group + **gedeelde** AI Search/Cosmos met security-filters (scheelt de vaste $75-$250/mnd per klant). Dezelfde Bicep, andere `deploymentTarget`.
- **"Het script" zelf:** **subscription vending** (Azure Verified Modules, `bicep-lz-vending`) + **Deployment Stamps**-pattern: één idempotente Bicep/Terraform-template, per klant één parameterfile, getriggerd door GitHub Actions / Azure DevOps. Elke klant = één "stamp". **Idempotent** = veilig opnieuw te draaien (deterministische naming op `tenantId`, `what-if`/deployment stacks).
- **Multi-agent-orchestratie:** het **Microsoft Agent Framework** (Semantic Kernel + AutoGen, preview okt 2025) bovenop Foundry, met connected agents (research/site/SEO/content/sales/qualify), OpenAPI-tools, MCP en A2A.

### 3.2 Wat parametriseren per tenant (de config-file)
Eén `tenant-config.json/yaml` per klant draagt alles:
- domein + niche-systeemprompt + keyword→pagina-map
- merk-assets (logo SVG, kleuren = `:root` vars), toon
- `seo_data.json` / keyword-set, taal/land-scope (NL / NL+BE+DE)
- named author (Person: naam, functie, foto, sameAs/socials)
- kwalificatie-rubriek (BANT of branche-specifiek) + score-drempel
- routing-target (`email | teams | dynamics | hubspot`) + CRM-keys (in **Key Vault**, niet in de config)
- cadans-cron + model + deployment-type (`Data Zone (EU)` of `Global`)
- compliance-vlaggen (Modified Abuse Monitoring / ZDR aan?)

### "Klaar" voor Fase 3 als…
- `azd up` (of de GitHub Actions-workflow) + één parameterfile rolt een **complete, werkende tenant** uit: site, agents, ACS-domein, Cosmos-container, Key Vault, routing, SEO/GEO-bots — in de gekozen tenant, in de EU.
- Het script is **idempotent** (tweede run breekt niets).
- Een tweede klant erbij = config invullen + script draaien, **zonder code-wijziging**.
- Disclosure + consent + verwerkersovereenkomst zijn standaard, niet-uitschakelbaar onderdeel van elke deploy.

---

## HET ONBOARDING-SCRIPT — stap voor stap bij een nieuwe klant

Dit is het hart van "agency-in-a-box". Bij een nieuwe klant doet het script (na het invullen van `tenant-config`):

1. **Intake lezen** — parameterfile valideren (domein, regio = EU, deploy-target, model + deployment-type, compliance-vlaggen). Stoppen als regio ≠ EU of een verplicht veld mist.
2. **Resources provisionen** (Bicep/Managed App, idempotent, deterministische naming op `tenantId`):
   - resource group (EU) + Azure Policy "allowed locations"
   - Foundry-project + standard agent setup (Cosmos ≥3000 RU/s, Storage, AI Search, Key Vault, capability hosts, RBAC)
   - model-deployment (`Data Zone EU`) + embeddings-deployment
   - Static Web App + Container App + Functions
   - ACS-resource + **afzenderdomein verifiëren** (SPF/DKIM/DMARC) — anders faalt mail bij oplevering
   - Lighthouse-delegatie (least-privilege) voor jullie beheer
3. **Secrets in Key Vault** — CRM-keys, DataForSEO-login, Cloudflare-token, Turnstile-secret. **Nooit in de repo/config.**
4. **Compliance-knoppen** — indien gevraagd: Modified Abuse Monitoring / ZDR-aanvraag triggeren; disclosure + consent-logging activeren.
5. **Onderzoek draaien** (semi-automatisch) — research-agent: niche + keywords (DataForSEO) + domein-shortlist + availability-check. **→ menselijke goedkeuring** van de keyword→pagina-map en het domein (+ EUIPO-merkcheck). Evt. domein registreren via Cloudflare.
6. **Site genereren + deployen** — generator op `config.json` (merk, kleuren, content, GEO-template ingebakken: schema, FAQ, TL;DR, llms.txt, named author). Push naar SWA. Schema-validatie als gate.
7. **Entity-laag** — Wikidata-entry (QID) + `sameAs`-block injecteren.
8. **SEO/GEO-bots activeren** — sitemaps + IndexNow-key + GSC/Bing-property + interne-link-embeddings + rank-tracking-cron.
9. **Content-pijplijn aanzetten** — timer-agent met tenant-toon, named author, feeds/keywords, interne-link-lijst uit de actuele sitemap, feitcheck-gate + humanizer. Cadans-cron zetten (NL-tijdzone).
10. **Lead-laag live** — formulier + chat-widget (in huisstijl), Turnstile + honeypot + rate-limit, auto-reply via ACS, BANT-agent met JSON-output, Cosmos `tenantId`-partitie.
11. **Routing koppelen** — per config naar e-mail/Teams/CRM, met Accept/Reject human-in-the-loop.
12. **Monitoring + alerts** — App Insights/Foundry-tracing, "0-output/FAIL"-alert, Cost Management-budget + alert per tenant.
13. **Oplevering** — smoke-test: testlead door de hele keten, één testblog, schema valideert, mail komt aan (niet in spam). Rapport naar Thomas + klant.

**Realistisch over handmatig vs. automatisch:** stap 5 (welke keywords/niche/domein) en de content-/lead-goedkeuring blijven bewust **menselijke gates** — niet omdat het niet kan, maar omdat Google's pSEO-straf en de AI-Act/AVG-risico's een mens-in-de-lus rechtvaardigen. De rest (2-4, 6-13) is volledig scriptbaar.

---

## Vaste maandlasten per tenant (om in de prijs te verwerken)

Los van LLM-tokenverbruik (dat is verwaarloosbaar: een lead-gesprek of blog kost centen) zijn er **vaste bodemkosten** die 24/7 doorlopen:

| Onderdeel | Indicatie (verifiëren!) | Opmerking |
|---|---|---|
| Azure AI Search | Basic ~$75/mnd, S1 ~$250/mnd | **Grootste vaste post.** Free = alleen dev. Bij kleine klanten margemoordend → overweeg gedeelde index (lite-variant). |
| Cosmos DB | ~$0,25/GB/mnd + RU/s (≥3000 RU/s vereist) | Gratis tier 1000 RU/s + 25 GB; serverless waar mogelijk. |
| Static Web App | ~$9/site/mnd (Standard, met SLA) | Free heeft géén SLA — niet voor betalende klant. |
| Container Apps | vaak **$0** (free grant: 180k vCPU-sec, 2M req/mnd) | Scale-to-zero. |
| Azure Functions | ruime gratis grant | Wekelijkse bots ≈ gratis. |
| ACS Email | ~$0,75 / 3.000 mails | Pay-per-use. |
| Umami (analytics) | ~€15-30/mnd (PostgreSQL Flexible) | Kan gedeeld over tenants. |
| Grounding with Bing | ~$35 / 1.000 transacties | **Spaarzaam** — alleen echte research/citatie-monitoring. |
| DataForSEO | $50 deposit, pay-as-you-go (~<$1/onderzoek) | Extern (geen PII heen sturen). |

**Prijsmodel-richting (markt-benchmark uit de bevindingen):** AI-marketingbureaus rekenen $3.000-$25.000/mnd; GoHighLevel-agencies ~$497/mnd basis. Voor de Azure-in-eigen-tenant-enterprise-propositie (klant draagt zelf de Azure-rekening): een **setup-fee** (de script-run + intake) + een **maandelijkse beheer/AI-fee** aan de bovenkant van de markt. *Definitieve prijsstelling is een aparte beslissing, niet in dit bouwplan.*

---

## Grootste valkuilen (samengevat, één plek)

1. **Residency-val:** `Global Standard` geeft GEEN EU-only-verwerking, ook al staat de resource in de EU. Voor harde EU-eis: `Data Zone Standard (EU)`. #1 fout.
2. **Model-lag in EU:** GPT-5.x is medio 2026 niet EU-data-zone. Communiceer vooraf: EU-only = GPT-4o/4.1.
3. **Claude-via-Foundry valt medio 2026 niet onder de EU Data Boundary** — bij harde EU-eis: Azure-OpenAI-modellen, geen Claude-via-Foundry (verifieer op bouwmoment of EU-native Claude inmiddels live is).
4. **Cosmos < 3000 RU/s → standard agent setup faalt.** Capability host is daarna **onveranderlijk**.
5. **Silent failure:** zonder "0-output"-alert valt de pijplijn maandenlang stil (BotLease-les). Loud failure verplicht.
6. **Vaste bodemkost per tenant** (AI Search + Cosmos) eet marge bij kleine klanten.
7. **Auto-reply zonder Turnstile/rate-limit** = mail-bomb-risico + kapotte domeinreputatie.
8. **Multi-tenant data-lek** zonder strikte `tenantId`-partitie + per-tenant Key Vault = AVG-datalek met meldplicht.
9. **AI Act Art. 50:** "ik ben AI"-disclosure vergeten = boete-risico vanaf aug 2026.
10. **Scaled content abuse:** nooit honderden pagina's tegelijk; lage cadans + harde gate.
11. **Cron default UTC** in Azure Functions — `WEBSITE_TIME_ZONE` zetten.
12. **Preview-features:** Hosted agents, agent-memory, Serverless Agents Runtime zijn preview medio 2026 — bouw productie-kritisch op **Prompt agents (GA) + Responses API**; verifieer GA-status vóór je erop leunt.

---

*Onzekerheden zijn in dit document expliciet gemarkeerd met ⚠️ of "verifiëren". Alle Azure-prijzen en Foundry-features op offerte-/bouwmoment opnieuw checken — het product verandert per kwartaal.*
