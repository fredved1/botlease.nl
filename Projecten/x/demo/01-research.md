# PROJECT X — Stap 1: Onderzoeksrapport (LOKALE TESTRUN)

> **Wat is dit?** De output van **stap 1 (domein-/niche-/keyword-onderzoek)** van de PROJECT X-pipeline, gedraaid als **lokale end-to-end test** voor een **fictief testbedrijf**. Doel: aantonen dat de pipeline tastbare, productie-realistische artefacten oplevert, voordat we het Azure-native bouwen.
>
> **Begeleidend bestand:** [`client-config.json`](client-config.json) — dezelfde uitkomst, machine-leesbaar, conform `client-config.template.json`.

---

## ⚠️ Disclaimer (lees eerst)

- **Het testbedrijf "Twentse Warmte" is volledig FICTIEF.** Het bestaat niet. Naam, KvK-nummer (90000001), BTW-nummer, adres, eigenaar (Bram Oude Wesselink) en LinkedIn-profiel zijn verzonnen voor demonstratiedoeleinden.
- **Deze run draait LOKAAL, niet op Azure.** Er zijn **geen echte API-calls** gedaan. Concreet:
  - **Domein-beschikbaarheid** (normaal via WhoisJSON/WhoisFreaks): **GESIMULEERD / illustratief.** Niet echt gecheckt.
  - **Keyword-volumes, CPC en concurrentie** (normaal via DataForSEO Labs / Google Ads): **GESIMULEERD / illustratief.** De getallen zijn plausibele schattingen, geen gemeten data.
  - **Merkrecht-check (EUIPO)** en **KvK-validatie**: niet uitgevoerd.
- **De LLM ben ik (Claude), niet de Azure Foundry Responses API.** In productie draait deze stap op `gpt-4.1-mini` (Data Zone EU). De *vorm* en *kwaliteit* van de output is identiek bedoeld; alleen de uitvoeringsomgeving verschilt.
- **Vóór een echte registratie/offerte** moeten alle gesimuleerde cijfers worden vervangen door echte API-uitkomsten en moet de klant zijn echte concurrenten + auteur aanleveren.

---

## 1. Het testbedrijf (fictief)

| Veld | Waarde |
|---|---|
| **Naam** | Twentse Warmte (B.V.) |
| **Plaats** | Almelo (regio Twente, Oost-Nederland) |
| **Niche** | Verwarmingsinstallateur, gespecialiseerd in warmtepompen + verduurzaming |
| **Diensten** | Warmtepomp installeren · Hybride warmtepomp · Zonneboiler/zonnepanelen-koppeling · CV-ketel vervangen · ISDE-subsidie-aanvraag + gratis warmtescan |
| **Doelgroep** | Woningeigenaren (35-65) en VvE-besturen in Twente die van het gas af willen; prijs- en subsidiebewust |
| **Servicegebied** | Almelo, Hengelo, Enschede, Borne, Wierden, Rijssen e.o. |
| **Tagline** | "Warm wonen in Twente, zonder gedoe." |
| **USP** | Vaste lokale monteur die je naam kent, gratis warmtescan aan huis, eerlijke offerte, en wij regelen je ISDE-subsidie. Geen wisselend uitzendvolk, geen verkooppraat. |

**Korte beschrijving (zoals op de site / in schema):**
> Twentse Warmte is een installatiebedrijf uit Almelo dat warmtepompen, zonneboilers en complete cv-vervanging verzorgt voor woningeigenaren en VvE's in Twente. We werken met vaste monteurs, leveren een heldere offerte na een gratis warmtescan aan huis, en regelen de ISDE-subsidieaanvraag voor je.

**Waarom deze niche geschikt is voor de demo:** sterk **lokaal** ("warmtepomp + plaatsnaam"), duidelijke **commerciële intentie**, een natuurlijke **leadconversie** (warmtescan aanvragen), en onderwerpen met geld-impact (subsidie/terugverdientijd) die de **fact-check-gate** zinvol maken. Het laat alle zes pipeline-stappen geloofwaardig tot leven komen.

---

## 2. Merk

| Element | Waarde | Reden |
|---|---|---|
| **Merkkleur (accent)** | `#E2562B` (warm oranje-rood) | Staat voor warmte/energie; valt op in een nuchtere installatiemarkt |
| **Tekst/secundair** | `#16263a` (diep marineblauw) | Vakmanschap en vertrouwen; goed leesbaar contrast |
| **Accent-zacht** | `#fbe7df` | Zachte achtergrond-tint voor kaarten/CTA-blokken |
| **Font** | Inter, system-ui, sans-serif | Neutraal, snel, scherp op mobiel |
| **Toon** | Informeel, jij-vorm, Twents-nuchter; geen verkooppraat, geen lange streepjes | Past bij de doelgroep en bij de humanizer-regel |

**Auteur (E-E-A-T, fictief):**
- **Naam:** Bram Oude Wesselink
- **Functie:** Eigenaar en hoofdmonteur, Twentse Warmte
- **Bio:** Ruim 15 jaar installateur in de regio Almelo, installeerde honderden warmtepompen en cv-systemen, schrijft over wat een woningeigenaar echt moet weten voordat hij van het gas af gaat.
- *In productie: een echte medewerker met echte foto + echt LinkedIn-profiel. E-E-A-T eist een natuurlijk persoon, geen "AI" of "Organization".*

---

## 3. Domein-shortlist (beschikbaarheid GESIMULEERD)

> ⚠️ De kolom **Status** is **illustratief**. In productie draait hier een echte bulk-availability-check (WhoisJSON/WhoisFreaks) + een EUIPO-merkrechtcheck per naam. Niets hieronder is daadwerkelijk geverifieerd.

| # | Domein | Status (gesimuleerd) | Beoordeling |
|---|---|---|---|
| 1 | **twentsewarmte.nl** | "vrij" (illustratief) | **Aanrader.** Kort, exacte merknaam, regio + dienst in één, .nl voor lokale SEO. |
| 2 | twentse-warmte.nl | "vrij" (illustratief) | Variant met streepje; als redirect-vangnet naar #1 registreren. |
| 3 | warmtepomptwente.nl | "vrij" (illustratief) | Sterk op exact-match keyword, maar minder merkbaar dan de bedrijfsnaam. |
| 4 | almelowarmte.nl | "vrij" (illustratief) | Hyperlokaal (Almelo) maar dekt het bredere Twente-servicegebied minder. |
| 5 | twentsewarmte.com | "vrij" (illustratief) | Defensief registreren; .nl blijft primair voor een NL-only installateur. |
| 6 | warmtepomp-almelo.nl | "bezet" (illustratief) | Geblokkeerd in dit scenario; toont dat de check ook "nee" oplevert. |

**Aanbeveling:** registreer **twentsewarmte.nl** als primair domein, met **twentse-warmte.nl** en **twentsewarmte.com** als defensieve redirects. Registrar: Cloudflare (wholesale, geen markup). Registrant op naam van de klant.

---

## 4. Keyword-onderzoek (volumes/CPC GESIMULEERD)

> ⚠️ **Alle cijfers in de kolommen Volume, Moeilijkheid en CPC zijn illustratief/gesimuleerd** — plausibele schattingen voor een Twente-installateur, geen DataForSEO-meting. "Volume" = geschat maandelijks NL-zoekvolume; "KD" = keyword difficulty (0-100); "CPC" = indicatieve Google-Ads-klikprijs in euro. **Intent** stuurt het paginatype.

| # | Keyword | Intent | Volume (gesim.) | KD (gesim.) | CPC (gesim.) | Doelpagina |
|---|---|---|---|---|---|---|
| 1 | warmtepomp almelo | Lokaal/commercieel | 90 | 22 | €3,80 | `/` (home) |
| 2 | warmtepomp installateur twente | Lokaal/commercieel | 140 | 28 | €4,20 | `/warmtepomp-installeren` |
| 3 | hybride warmtepomp | Commercieel/informatie | 4.400 | 41 | €2,90 | `/hybride-warmtepomp` |
| 4 | hybride warmtepomp kosten | Commercieel/onderzoek | 1.300 | 38 | €3,10 | `/hybride-warmtepomp` |
| 5 | isde subsidie warmtepomp 2026 | Informatie (transactioneel) | 2.600 | 33 | €1,40 | `/blog/isde-subsidie-warmtepomp-2026` |
| 6 | cv ketel vervangen almelo | Lokaal/commercieel | 70 | 20 | €4,60 | `/cv-ketel-vervangen` |
| 7 | warmtepomp kosten | Onderzoek | 8.100 | 47 | €2,70 | `/warmtepomp-installeren` |
| 8 | warmtepomp oude woning | Informatie | 880 | 35 | €2,10 | blog (toekomstig) |
| 9 | warmtescan woning | Commercieel | 320 | 24 | €3,00 | `/contact` (warmtescan-formulier) |
| 10 | zonneboiler installateur twente | Lokaal/commercieel | 50 | 18 | €3,40 | `/warmtepomp-installeren` (sectie) |
| 11 | van het gas af | Informatie | 3.600 | 44 | €1,10 | blog (toekomstig) |
| 12 | beste warmtepomp 2026 | Onderzoek/vergelijk | 1.900 | 49 | €2,50 | blog (toekomstig) |

**Hoofdstrategie:**
- **Lokale exact-match keywords** (#1, #2, #6, #10) hebben laag volume maar hoge koopintentie en lage moeilijkheid → snelste pad naar leads. Deze landen op home + dienstpagina's met `LocalBusiness`-schema.
- **Hoog-volume informatie-keywords** (#5, #7, #11, #12) zijn moeilijker en informatief → ideaal als **blog-content** die de site autoriteit geeft en intern doorlinkt naar de dienstpagina's.
- **GEO-kans:** kopers vragen AI-assistenten "welke warmtepomp-installateur in Twente / wat kost een hybride warmtepomp". We maximaliseren de citatiekans met FAQPage-schema, een TL;DR/answer-capsule per pagina, `llms.txt` en named author. **Geen garantie op een positie** — dit is een kans, geen ranking-knop.

---

## 5. Paginastructuur van de site

| Pad | Titel | Doel | Primair keyword | Schema |
|---|---|---|---|---|
| `/` | Warmtepomp en cv-installateur in Twente — Twentse Warmte | Home: USP, servicegebied, gratis warmtescan-CTA, social proof | warmtepomp almelo | Organization + LocalBusiness |
| `/warmtepomp-installeren` | Warmtepomp laten installeren in Twente | Dienstpagina: proces, kosten-indicatie, terugverdientijd, FAQ | warmtepomp installateur twente | Service + FAQPage |
| `/hybride-warmtepomp` | Hybride warmtepomp: kosten en wanneer het loont | Dienstpagina: hybride vs. volledig, kosten, ISDE, FAQ | hybride warmtepomp kosten | Service + FAQPage |
| `/cv-ketel-vervangen` | CV-ketel vervangen in Almelo en omgeving | Dienstpagina: vervanging + verduurzamingsadvies, FAQ | cv ketel vervangen almelo | Service + FAQPage |
| `/contact` | Gratis warmtescan aanvragen | Conversiepagina: warmtescan-formulier (lead-capture) + AI-chat-widget + contactgegevens | warmtescan woning | LocalBusiness + ContactPoint |

Vaste ondersteunende pagina's (verplicht in elke tenant-deploy): `/over-bram` (auteur/Person-schema), `/privacy`, `/voorwaarden`, plus `sitemap.xml`, `robots.txt`, `llms.txt` en de IndexNow-key.txt op de root.

---

## 6. Blogonderwerp (eerste artikel)

| Veld | Waarde |
|---|---|
| **Titel** | ISDE-subsidie voor je warmtepomp in 2026: zo vraag je hem aan (en wat je terugkrijgt) |
| **Target-keyword** | isde subsidie warmtepomp 2026 |
| **Slug** | `/blog/isde-subsidie-warmtepomp-2026` |

**Waarom dit onderwerp:** hoog geschat volume met lage moeilijkheid (kolom 4 hierboven), zware koopintentie (mensen die subsidie uitzoeken staan op het punt te investeren), en een natuurlijke interne link naar `/hybride-warmtepomp` en `/contact` (warmtescan). De geld-claims (subsidiebedragen) maken de **fact-check-gate** zinvol: elk bedrag moet uit een geverifieerde bron komen, anders FAIL. Auteur: Bram Oude Wesselink (Person-schema, E-E-A-T).

---

## 7. Hoe dit aansluit op de rest van de pipeline

Deze stap-1-output (de ingevulde `client-config.json`) is exact wat het opzet-script consumeert. De vervolgstappen gebruiken deze velden:

| Pipeline-stap | Gebruikt uit deze config |
|---|---|
| 2 — Website bouwen | `branding.colors` → `:root` CSS-vars; `company`/`niche` → schema + paginastructuur uit §5 |
| 3 — SEO + GEO | `seo_geo.schema_types`, `emit_llms_txt`, `indexnow_key`, named author |
| 4 — Content | `content_pipeline.topics` (start = blog uit §6), `editorial_gate`, `cadence_cron` |
| 5 — Leads | `leads.channels` (warmtescan-formulier + chat), `qualification` (custom rubriek), `ai_disclosure_text` |
| 6 — Doorzetten | `leads.routing.target` = e-mail naar bram@twentsewarmte.nl boven `qualify_threshold` 60 |

**Volgende stap in de testrun:** de site genereren (stap 2) op basis van deze config, daarna een voorbeeldartikel (stap 4) en een voorbeeld-leadafhandeling (stap 5-6) — alles lokaal en als "illustratief/gesimuleerd" gemarkeerd waar normaal een externe API of Azure-dienst zou draaien.

---

*Gegenereerd in de lokale PROJECT X-testrun op 2026-06-21. Testbedrijf fictief; externe data gesimuleerd. Verifieer alle cijfers met echte API-calls vóór registratie of offerte.*
