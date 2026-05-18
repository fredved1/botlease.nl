# BotLease SEO handover — actiestappen om #1 in Google te worden

Status mei 2026: 53 pagina's geïndexeerd, complete on-page SEO afgerond.
Voor #1-ranking zijn nu **off-page acties** nodig. Hieronder concrete stappen, priority + ETA.

---

## PRIORITY 0 — env vars in Vercel (10 min) — KRITIEK voor formulieren

Voor het contactformulier + admin dashboard te laten werken: zet drie env vars
in Vercel (Settings → Environment Variables):

### 1. RESEND_API_KEY — voor email naar hallo@botlease.nl

1. Maak gratis account op https://resend.com (gebruik hallo@botlease.nl)
2. Kopieer de API key uit "API Keys"
3. Vercel → botlease-v2 → Settings → Environment Variables:
   - Name: `RESEND_API_KEY`
   - Value: `re_xxx...` (van Resend)
   - Environments: Production, Preview, Development
4. (Optioneel) verifieer botlease.nl als sender domain in Resend → dan kun je
   `RESEND_FROM = BotLease <noreply@botlease.nl>` toevoegen voor mooier afzender-adres.
   Tot je dat doet komt mail van `onboarding@resend.dev` — dat werkt prima.

### 2. ADMIN_PASSWORD — voor /admin dashboard

1. Verzin een lang random wachtwoord (bv. `openssl rand -base64 24` of bitwarden)
2. Vercel → botlease-v2 → Settings → Environment Variables:
   - Name: `ADMIN_PASSWORD`
   - Value: jouw random string
3. Bezoek https://botlease.nl/admin om aanvragen te bekijken (login met dit wachtwoord)

### 3. Supabase env vars (al gezet) — backup van aanvragen

`NEXT_PUBLIC_SUPABASE_URL` en `NEXT_PUBLIC_SUPABASE_ANON_KEY` zijn al ingesteld
en zorgen voor backup naar Supabase database. Geen actie nodig.

### Na env var setup: deploy opnieuw

Vercel deployt automatisch elke commit. Force redeploy:
```bash
vercel --prod --yes
```

---

## PRIORITY 1 — deze week doen

### 1.1 Google Search Console verifiëren (15 min)

1. Ga naar https://search.google.com/search-console
2. Klik "Add property" → kies "Domain" → vul in: `botlease.nl`
3. Verifieer via DNS TXT-record (Vercel: Domains → botlease.nl → Add TXT record)
4. Eenmaal geverifieerd: ga naar "Sitemaps" → submit `https://botlease.nl/sitemap.xml`
5. Tip: vraag indexering aan voor de 5 belangrijkste pagina's via "URL Inspection":
   - `/`
   - `/gids/humanoide-robot-leasen`
   - `/robots/`
   - `/vergelijken`
   - `/kosten`

### 1.2 Bing Webmaster Tools (10 min)

1. Ga naar https://www.bing.com/webmasters
2. Inloggen met Microsoft account
3. Add site `botlease.nl` → verifieer (kan via DNS of HTML-bestand)
4. Submit sitemap `https://botlease.nl/sitemap.xml`
5. Bing = 8% search marktaandeel in NL — niet skipbaar

### 1.3 Google Business Profile aanmaken (30 min)

1. Ga naar https://business.google.com
2. "Add your business" → BotLease, categorie: "Equipment rental service" of "Industrial automation"
3. Adres: High Tech Campus Eindhoven (of jouw exacte adres)
4. Verificatie via postcard (5-7 werkdagen)
5. Vul in: openingstijden, telefoon, foto's (4-6 robot foto's uit /frontend/img/robots/)
6. Voeg KvK-nummer toe — zodra je dat hebt
7. Stuur reviews aan: vraag 2-3 early-adopter klanten (zelfs informeel) om Google review

**Waarom kritiek**: local SEO = Google rankt lokale Eindhoven/NL zoekopdrachten hoger met dit profiel.

### 1.4 Google News Publisher Center (45 min)

1. Ga naar https://publishercenter.google.com
2. Add publication: "BotLease Nieuws"
3. Sitemap URL: `https://botlease.nl/sitemap.xml`
4. RSS URL: `https://botlease.nl/rss.xml`
5. Categorieën: Technology, Business, Industry
6. Verifieer eigenaarschap
7. Submit voor Google News inclusie (review duurt 1-2 weken)

---

## PRIORITY 2 — eerste maand

### 2.1 Backlink outreach — 10 targets

Doel: 5-10 redactionele backlinks van NL/EU tech & business sites in eerste 30 dagen.

**Tier A (high authority, hoge moeite):**

| Site | Approach | Contact |
|---|---|---|
| nrc.nl | Pitch: "Eerste Nederlandse humanoid-leasemaatschappij" | Tech-redactie via tip@nrc.nl |
| fd.nl | Pitch: marktanalyse Goldman Sachs $38B + NL implicaties | FD redactie |
| nu.nl | Press release over commercieel humanoid lease NL | redactie@nu.nl |
| rtlz.nl | Interview Eindhoven, video-mogelijkheid | redactie@rtlz.nl |
| bnr.nl | BNR Tech-show, gast-spot | tech@bnr.nl |

**Tier B (industry blogs, makkelijker):**

| Site | Pitch | Why they'll link |
|---|---|---|
| computable.nl | Humanoid robots in NL MKB | Diep tech-publiek |
| ictmagazine.nl | EU AI-Act compliance gids | Compliance-thema |
| logistiek.nl | 3PL pilot-cases | Hun core audience |
| nieuwsvoorondernemers.nl | MKB-aanpak humanoid lease | MKB-focus |
| robotenz.nl | Catalog-overzicht + interview | NL robotica-community |

**Pitch template** (`PRESS_PITCH.md` hieronder).

### 2.2 Industry forum + community posts

- LinkedIn (BotLease company page) — 2 posts per week minimaal
- Reddit: r/Netherlands, r/robotics, r/BNL (Dutch business)
- Tweakers.net forum: "Wie heeft ervaring met humanoid-leasing?"
- Bizz.nl, Sprout, Emerce — entrepreneurial communities

### 2.3 Press release publiceren

- Persbericht over launch, distribueer via:
  - Persberichten.com (gratis)
  - Newsdesk.nl (gratis)
  - Persgroep (betaald, €295)
  - PR Newswire NL (betaald, €450 — alleen voor major news)

---

## PRIORITY 3 — eerste kwartaal

### 3.1 Content velocity

Schrijf 2 nieuwsartikelen per week. Topics:
- Robotmodel-launches (volg fabrikant nieuwsbrieven)
- EU-regelgeving updates (TÜV, EU AI Office aankondigingen)
- Pilot-rapporten (Mercedes, BMW, Amazon, GXO)
- Marktanalyses (Goldman, Morgan Stanley, IFR)
- Nederlandse use-cases (interview NL klanten als die er zijn)

### 3.2 Contentlinks van externe sites verbeteren

Wikipedia-bewerking: voeg BotLease toe aan de Nederlandse pagina "Humanoide robot" (als die bestaat) of maak er een. Geen referentie naar BotLease als primaire bron — wel naar de gids als secundaire bron.

### 3.3 YouTube channel

- Maak BotLease YouTube channel
- Upload korte demo's van pilot-deployments
- Link in beschrijving naar /robots/<slug>
- Embed via VideoObject schema (al ingebouwd in de site)

---

## TECHNISCHE CHECKLIST

Wat al gedaan is in de site:

- [x] Sitemap.xml met 53 URLs
- [x] Robots.txt met sitemap directive
- [x] OG:image + twitter:image op alle pagina's
- [x] Schema.org: Organization, LocalBusiness, Product, BreadcrumbList, FAQPage, Article, NewsArticle, VideoObject, DefinedTermSet, SpeakableSpecification
- [x] Canonical URLs op alle pagina's
- [x] hreflang nl-NL via og:locale
- [x] Mobile-responsive
- [x] Lazy loading op alle non-critical images
- [x] preconnect naar Google Fonts
- [x] Click-to-play video facade (geen tracking tot interactie)
- [x] Geldige HTML (geen broken links in interne structure)
- [x] Internal linking: 5+ links per pagina naar gerelateerde content
- [x] Topic clusters: robots ↔ sectoren ↔ leasen ↔ gidsen

Wat handmatig nog kan:

- [ ] Add Google Analytics 4 (of beter: Plausible / Fathom voor privacy)
- [ ] Add Hotjar of Microsoft Clarity voor user behavior insights
- [ ] Lighthouse audit run (verwacht: 90+ Performance, 100 SEO)
- [ ] Custom 404 page met search-suggesties
- [ ] Add hreflang voor EN-versie als je internationaal wilt (later)
- [ ] Setup transactional email (lease-aanvragen → confirmation mail)
- [ ] Setup conversion tracking voor "Plan demo" form

---

## VERWACHTE TIJDLIJN TOT #1

**Realistische progressie voor "humanoide robot leasen Nederland":**

| Week | Status | Verwacht |
|---|---|---|
| 1-2 | Indexering door Googlebot | 30-50 pagina's geïndexeerd |
| 2-4 | Long-tail keywords ranken | Top 20 voor 10+ termen |
| 4-8 | Primary keyword traffic | Top 10 voor "humanoide robot leasen" zonder backlinks |
| 8-16 | Met 5-10 backlinks | Top 5 voor primary keywords |
| 16-26 | Met 10-20 backlinks + content velocity | Top 3 voor "humanoide robot leasen Nederland" |
| 26+ | Domain authority opgebouwd | #1 haalbaar mits geen sterke concurrent verschijnt |

**Concurrentie-analyse:**
- Vrijwel geen serieuze NL-spelers in humanoid-leasing.
- Tovertafel.nl, RobotShop.eu en ABB-leasing zijn niet vergelijkbaar (andere niche).
- Grootste risico: een buitenlandse speler (DHL Robotics, Bosch Rexroth) opent NL-vestiging.

**Het echte werk = backlinks krijgen.** On-page SEO is af. Content is af. Schema is af. Wat ontbreekt is autoriteit, en dat krijg je alleen via externe sites.

---

## VOLGENDE TASKS DIE BOTLEASE-SITE NOG KAN HEBBEN

Als je nog 4-8u extra wil investeren:

- Interactive ROI calculator op /sectoren/<slug> pagina's (sector-specifieke berekeningen)
- "Resources" sectie met PDFs (download-gated voor leadgeneration)
- Klant-portaal met inlog voor leasers (account.botlease.nl) — toont robot status
- Live chat (Crisp, Intercom) — verlaagt drop-off op /robots pagina's
- Een/Engelse versie van de site (botlease.nl/en/) — toegang tot Belgische/Duitse markt
- Affiliate-programma met integratoren en SI's (CGI, Capgemini, etc.)
- Webinar-pagina: maandelijks webinar over "humanoid lease voor jouw sector"

Maar dit zijn extras. De kern is gedaan.
