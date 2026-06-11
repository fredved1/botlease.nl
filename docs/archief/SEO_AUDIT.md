# BotLease.nl — Deep SEO Audit (May 2026)

**Date:** 2026-05-19
**Audit scope:** Full /frontend tree, sitemap, robots.txt, competitor benchmarking against Smartrobot.solutions
**Goal of owner:** Rank #1 in NL for "humanoide robot leasen" and related model/sector long-tails.

**TL;DR for the impatient founder:**
You have a structurally sound 47-URL site with strong topical coverage (15 robot pages, 4 sector pages, 6 comparison pages, 5 city pages, 2 deep guides, 10 news articles) — but Google still indexes you as a *chatbot company*. The single biggest reason: legacy chatbot HTML files (`index-chatbot-backup.html`, `chatbot-landing.html`, `chatbot-split.html`, `chatbot-test.html`, `index-old.html`) sit live in /frontend/ with no `noindex` and no redirects. Every meta description on the site is too long (170–260 chars, vs Google's ~155 cut-off). Sector and guide pages have zero images. Your only direct NL competitor (Smartrobot.solutions, Nijmegen) sells/rents — they do NOT lease, and they do NOT publish prices. That is the gap you should ram a truck through.

---

## 1. Page Inventory

47 indexable HTML files in `/frontend/` plus 8 backend/legacy files. Word counts below are *body content only* (HTML/CSS/JS stripped). JSON-LD count = number of `<script type="application/ld+json">` blocks.

### Core (root)

| File | Title | Meta-desc len | Words | JSON-LD | Notes |
|---|---|---:|---:|---:|---|
| `frontend/index.html` | Humanoïde robot leasen Nederland 2026 — 15 modellen vanaf €290/mnd \| BotLease | 258 | 597 | 6 | Strong meta; desc TOO LONG; canonical OK |
| `frontend/kosten.html` | Wat kost een humanoïde robot leasen? Calculator + uitleg \| BotLease | 182 | 398 | 2 | Thin (<500w); desc 17 over |
| `frontend/over.html` | Over BotLease — Nederlands eerste humanoid-robot leasemaatschappij \| BotLease | 207 | 463 | 2 | Thin; needs founder bio + KvK/AFM trust signals |
| `frontend/methodologie.html` | Methodologie — hoe BotLease robots evalueert en lease-prijzen berekent \| BotLease | 173 | 663 | 2 | OK |
| `frontend/begrippen.html` | Humanoïde robot terminologie — begrippenlijst \| BotLease | (<165) | 1 159 | 3 | Great glossary; should also have DefinedTerm schema |
| `frontend/kennisbank.html` | Kennisbank — Milo | n/a | 44 | 0 | **BROKEN/legacy** — references Milo brand. Has `noindex`. Delete or rebrand. |

### Robot model pages (15) — `/frontend/robots/`

All have `og:type=product`, canonical, hero image with alt, and 4 JSON-LD blocks (Product + Breadcrumb + Offer + FAQ-style). All 15 meta descriptions are ~208–248 chars — too long. Body word counts 398–543. Need 700–1200w to outrank Smartrobot's model pages.

| File | Title | Words | Desc len |
|---|---|---:|---:|
| `robots/index.html` | Humanoïde robots leasen Nederland — catalogus 2026 | 543 | 240 |
| `robots/1x-neo.html` | 1X NEO — vanaf €1.999/mnd | 474 | 213 |
| `robots/agility-digit.html` | Agility Digit v4 — €2.899/mnd | 475 | 244 |
| `robots/apptronik-apollo.html` | Apptronik Apollo — €3.499/mnd | 471 | 227 |
| `robots/engineai-se01.html` | EngineAI SE01 — €1.590/mnd | 412 | 208 |
| `robots/figure-02.html` | Figure 02 / 03 — €3.899/mnd | 482 | 248 |
| `robots/neura-4ne1-gen3.html` | NEURA 4NE-1 Gen 3.5 — €4.490/mnd | 438 | 237 |
| `robots/neura-4ne1-mini.html` | NEURA 4NE-1 Mini — €1.295/mnd | 431 | 214 |
| `robots/pal-kangaroo.html` | PAL Kangaroo — €4.250/mnd | 404 | 208 |
| `robots/pal-tiago-pro.html` | PAL TIAGo Pro — €2.950/mnd | 405 | 224 |
| `robots/pollen-reachy-2.html` | Pollen Reachy 2 — €3.250/mnd | 421 | 227 |
| `robots/ubtech-walker-s2.html` | UBTECH Walker S2 — €4.250/mnd | 409 | 209 |
| `robots/unitree-g1.html` | Unitree G1 Edu — €1.295/mnd | 402 | 218 |
| `robots/unitree-h1-2.html` | Unitree H1-2 — €4.890/mnd | 398 | 218 |
| `robots/unitree-h2.html` | Unitree H2 — €2.250/mnd | 405 | 214 |
| `robots/unitree-r1.html` | Unitree R1 — €290/mnd | 402 | 207 |

### Sector pages (4 + index)

| File | Words | Desc len | Issue |
|---|---:|---:|---|
| `sectoren/index.html` | 140 | 190 | **Far too thin (<500)** |
| `sectoren/3pl-fulfillment.html` | 498 | 223 | Just barely; no images |
| `sectoren/hospitality-retail.html` | 489 | 226 | Thin; no images |
| `sectoren/productie-assemblage.html` | 438 | 214 | Thin; no images |
| `sectoren/zorg-instellingen.html` | 436 | 208 | Thin; no images |

### Vergelijken (comparison) pages (6 + index)

| File | Words | Desc len |
|---|---:|---:|
| `vergelijken/index.html` | 472 | 174 |
| `vergelijken/apptronik-apollo-vs-figure-02.html` | 319 | (OK) |
| `vergelijken/neura-4ne1-gen3-vs-apptronik-apollo.html` | 325 | (OK) |
| `vergelijken/pal-kangaroo-vs-unitree-h1-2.html` | 286 | (OK) |
| `vergelijken/unitree-g1-vs-neura-4ne1-mini.html` | 314 | (OK) |
| `vergelijken/unitree-h1-2-vs-ubtech-walker-s2.html` | 292 | (OK) |
| `vergelijken/unitree-r1-vs-engineai-se01.html` | 307 | (OK) |

All <500w. These are high-intent comparison queries — pad to 800+ words minimum each.

### City lease pages (5 + index)

| File | Words | Desc len |
|---|---:|---:|
| `leasen/index.html` | 187 | (OK) |
| `leasen/amsterdam.html` | 274 | 199 |
| `leasen/rotterdam.html` | 278 | 199 |
| `leasen/eindhoven.html` | 271 | 199 |
| `leasen/utrecht.html` | 274 | 197 |
| `leasen/den-haag.html` | 272 | 198 |

All five city pages are doorways at risk of looking thin/templated to Google. Each needs unique local data: real postcodes serviced, named industrial zones, and (ideally) a local case study.

### Guides

| File | Words | Desc len | Notes |
|---|---:|---:|---|
| `gids/index.html` | 167 | (OK) | Hub page — fine length |
| `gids/humanoide-robot-leasen.html` | 2 102 | 226 | **Strong pillar page**, your best asset |
| `gids/ai-act-machineverordening.html` | 1 655 | 258 | Strong; desc 100+ over budget |

### News (10 + index)

| File | Words |
|---|---:|
| `nieuws/index.html` | 481 |
| `nieuws/agility-digit-fulfillment-pilot-3pl-nederland.html` | 457 |
| `nieuws/ai-act-machineverordening-humanoid-werkgevers-2026.html` | 655 |
| `nieuws/apptronik-mercedes-apollo-lessen-eerste-pilot.html` | 493 |
| `nieuws/eu-gebouwd-humanoid-voordeel-2026.html` | 696 |
| `nieuws/eu-machineverordening-2027-werkgevers-checklist.html` | 576 |
| `nieuws/goldman-sachs-38-miljard-humanoid-markt-nederland.html` | 443 |
| `nieuws/humanoid-fulfillment-pilots-nederland-2026.html` | 617 |
| `nieuws/neura-robotics-bosch-deal-nederlandse-maakindustrie.html` | 611 |
| `nieuws/ubtech-walker-s2-1000-units-commerciele-volwassenheid.html` | 556 |
| `nieuws/unitree-g1-mkb-vijf-rendabele-toepassingen.html` | 560 |

News density is healthy. Keep one fresh post every 5–7 days minimum.

### Legacy / non-public pages (8)

| File | Status | Action |
|---|---|---|
| `frontend/index-chatbot-backup.html` | **LIVE**, indexable, title "BotLease — AI-klantenservice voor het MKB" | DELETE FROM REPO + 301 to `/` |
| `frontend/index-old.html` | **LIVE**, indexable, title "BotLease - AI-automatisering zonder risico" | DELETE + 301 to `/` |
| `frontend/chatbot-landing.html` | **LIVE**, indexable, title "BotLease AI - Uw Persoonlijke AI Assistent" | DELETE + 301 to `/` |
| `frontend/chatbot-split.html` | **LIVE**, indexable | DELETE + 301 to `/` |
| `frontend/chatbot-test.html` | **LIVE**, indexable | DELETE + 301 to `/` |
| `frontend/dashboard.html` | noindex set, but Milo brand | Move to separate project or remove |
| `frontend/login.html` | noindex set, Milo brand | Same |
| `frontend/kennisbank.html` | noindex set, Milo brand | Same |
| `frontend/admin.html` | noindex set | Keep, also blocked in robots.txt |

---

## 2. Legacy / Wrong-Business Pages — The Single Biggest Bug

**This is THE issue.** You said "Google index still shows ONE result for `site:botlease.nl` and it's an old chatbot homepage." That is consistent with what I found in the file system.

### Files that still describe BotLease as a chatbot company

| File | Live URL | Title still on file | Recommended action |
|---|---|---|---|
| `frontend/index-chatbot-backup.html` | https://botlease.nl/index-chatbot-backup | "BotLease — AI-klantenservice voor het MKB \| Probeer 14 dagen gratis" | **DELETE FILE + add 301 redirect to `/` in `vercel.json`** |
| `frontend/chatbot-landing.html` | https://botlease.nl/chatbot-landing | "BotLease AI - Uw Persoonlijke AI Assistent" | DELETE + 301 to `/` |
| `frontend/chatbot-split.html` | https://botlease.nl/chatbot-split | "BotLease AI - Interactive Experience" (desc mentions "customer service") | DELETE + 301 to `/` |
| `frontend/chatbot-test.html` | https://botlease.nl/chatbot-test | "BotLease Chatbot Test" | DELETE |
| `frontend/index-old.html` | https://botlease.nl/index-old | "BotLease - AI-automatisering zonder risico" | DELETE + 301 to `/` |

The `_archive_chatbot_versie/` folder in repo root is presumably not deployed (Vercel publishes from `/frontend/`). Confirm by reading `.vercel/project.json` or `.deployment` — but the 5 files above ARE in `/frontend/` and are therefore live.

### Exact fix

1. `git rm frontend/index-chatbot-backup.html frontend/chatbot-landing.html frontend/chatbot-split.html frontend/chatbot-test.html frontend/index-old.html`
2. Edit `frontend/vercel.json` to add:
   ```json
   {
     "buildCommand": "echo 'No build needed'",
     "outputDirectory": ".",
     "cleanUrls": true,
     "trailingSlash": false,
     "redirects": [
       { "source": "/index-chatbot-backup", "destination": "/", "permanent": true },
       { "source": "/index-old", "destination": "/", "permanent": true },
       { "source": "/chatbot-landing", "destination": "/", "permanent": true },
       { "source": "/chatbot-split", "destination": "/", "permanent": true },
       { "source": "/chatbot-test", "destination": "/", "permanent": true }
     ]
   }
   ```
3. Deploy.
4. In Google Search Console: **Removals → Temporarily remove URL** for each of the 5 legacy URLs. Then submit fresh sitemap.

This single step will, within 1–3 weeks of recrawl, change what Google shows on `site:botlease.nl` from "AI-klantenservice voor MKB" to "Humanoïde robot leasen Nederland".

### Other "wrong business" leftovers

- `frontend/kennisbank.html`, `dashboard.html`, `login.html` reference **Milo** brand (different project). These are `noindex`, but their on-page brand references can confuse human visitors who navigate to e.g. `/login`. Move these to the Milo repo or delete from this repo.
- `backend/` folder in repo root: not relevant for SEO but contains a lot of old chatbot code. Confirm not deployed.

---

## 3. Competitor Analysis: Smartrobot.solutions (Nijmegen)

### What they do well

- Long history — KvK 61024201 indicates active since at least 2014. **Domain age is their #1 advantage**, not content.
- Trust signals on home page: Rabobank, XS4ALL, Van Haren, Evoluon as testimonial logos.
- Wide product mix (serving robots, telepresence, quadrupeds, humanoids, holograms) — sprawling internal-link graph that gives every page topical reinforcement.
- 4-language switcher (NL/EN/FR/DE).
- Title pattern: `{Robot model} - Smartrobot.solutions` — concise, brand-led.
- Sister site `iretail.solutions` likely creates cross-domain links.

### What they do BADLY (your opportunities)

| Their weakness | Your opportunity |
|---|---|
| **No prices anywhere.** All CTAs are "Vraag offerte aan". | You list €290–€4.890/mnd on every page. Massive featured-snippet & comparison query advantage. |
| **No lease product.** They do "verkoop" + "verhuur" (sales + rental for events). | "Operational lease" is your exclusive position — no NL competitor owns this keyword. |
| **Humanoid pages are thin** — ~200 words each, no specs in body, just spec cards. | Your robot pages are 400+w with FAQs, ROI math, EU AI-Act commentary. |
| **No comparison content.** No "X vs Y" pages. | You have 6 vergelijken/* pages. Comparison queries (`unitree g1 vs neura`) are very high-intent and unowned in NL SERPs. |
| **No regulatory/compliance content.** | Your `gids/ai-act-machineverordening.html` (1 655 words) targets a brand-new keyword set (AI Act, Machineverordening 2023/1230) with near-zero NL competition. |
| **No news/blog cadence visible.** | Your `/nieuws/` 10 articles in 12 days = freshness signal Google rewards. |
| **No structured data on product pages.** | You ship Product, FAQ, HowTo, Organization, LocalBusiness, BreadcrumbList JSON-LD. |
| **No city-level landing pages.** | You have Amsterdam/Rotterdam/Eindhoven/Utrecht/Den Haag pages. |
| **No "kosten"/"prijzen" calculator.** | `kosten.html` exists (and ranks-able). |

### Keywords they currently rank for (inferred)

- "robot huren" / "robot verhuur" / "robot verhuur event"
- "serveerrobot horeca"
- "Unitree G1 Nederland", "Unitree G1 kopen"
- "robot Nijmegen"
- "humanoid robot Nederland" (top-of-page placement currently)

### Keywords they do NOT rank for and you can own

- `humanoide robot leasen` / `humanoid robot lease Nederland`
- `[model] leasen Nederland` for all 15 models
- `EU AI Act humanoid robot`
- `Machineverordening humanoid`
- `humanoide robot kosten` / `prijs per maand`
- `humanoide robot 3PL` / `fulfillment robot lease`
- Any city + lease keyword
- Any `X vs Y` comparison

### Backlink intel (best guess without Ahrefs)

Anchor-text patterns and partner mentions suggest Smartrobot.solutions earns links from:
- Press articles featuring their event rentals (e.g. Rabobank events, conferences)
- The Iretail.solutions sister domain
- Educational institutions (Evoluon partnership)
- Likely Pepper/Sanbot supplier directories

You can match this with: Brainport Eindhoven, RAI Amsterdam exhibitor pages, Sprout/MT/Emerce coverage, NRC tech, Tweakers, hardware.info press releases, KvK/Startup-NL listings, and trade-association sites (TLN, evofenedex for logistics; KHN for hospitality).

---

## 4. Keyword Opportunity Map (45 targets)

Volume estimates are conservative best-guesses for **NL monthly searches** as of May 2026. Difficulty is rated relative to *current* botlease.nl (low domain authority).

### Head terms (high volume, high difficulty)

| # | Keyword | Est. NL vol/mo | Competition | Difficulty for BotLease | Target page |
|---|---|---:|---|---|---|
| 1 | humanoide robot | 1 300 | High | Hard (info intent) | `gids/humanoide-robot-leasen.html` |
| 2 | humanoid robot Nederland | 480 | Med | Medium | `index.html` |
| 3 | humanoide robot leasen | 210 | Low | **EASY — top opportunity** | `index.html` |
| 4 | humanoide robot kopen | 320 | Med | Medium (intent split) | `kosten.html` (capture & redirect to lease) |
| 5 | humanoide robot huren | 590 | Med (Smartrobot owns) | Medium | new `/huren` page or alias |
| 6 | humanoide robot prijs | 480 | Low | **EASY** | `kosten.html` |
| 7 | humanoid robot lease | 90 | Low | **EASY** | `index.html` (EN intent) |

### Brand (defensive)

| # | Keyword | Vol | Diff | Page |
|---|---|---:|---|---|
| 8 | BotLease | 50 | Easy | `index.html` |
| 9 | BotLease leasen | <20 | Easy | `index.html` |
| 10 | botlease.nl | 20 | Easy | `index.html` |

### Long-tail per robot model (15 models × ~3 variants = 45+ phrases; here the highest-volume ones)

| # | Keyword | Vol | Diff | Page |
|---|---|---:|---|---|
| 11 | Unitree G1 prijs | 880 | Med | `robots/unitree-g1.html` |
| 12 | Unitree G1 kopen | 590 | Med (Smartrobot owns) | comparison page |
| 13 | Unitree G1 leasen | 70 | **Easy** | `robots/unitree-g1.html` |
| 14 | Unitree G1 Nederland | 320 | Med | `robots/unitree-g1.html` |
| 15 | Unitree H1 leasen | 50 | Easy | `robots/unitree-h1-2.html` |
| 16 | Unitree H2 prijs | 110 | Low | `robots/unitree-h2.html` |
| 17 | Unitree R1 prijs | 140 | Low | `robots/unitree-r1.html` |
| 18 | NEURA 4NE-1 Nederland | 90 | Low | `robots/neura-4ne1-gen3.html` |
| 19 | NEURA Robotics lease | 30 | Easy | `robots/neura-4ne1-gen3.html` |
| 20 | Apptronik Apollo Nederland | 70 | Low | `robots/apptronik-apollo.html` |
| 21 | Figure 02 Nederland | 110 | Low | `robots/figure-02.html` |
| 22 | Figure 03 lease | 30 | Easy | `robots/figure-02.html` |
| 23 | Agility Digit Nederland | 50 | Low | `robots/agility-digit.html` |
| 24 | PAL Robotics lease | 30 | Easy | `robots/pal-kangaroo.html` |
| 25 | 1X NEO Nederland | 90 | Low | `robots/1x-neo.html` |
| 26 | Pollen Reachy 2 prijs | 30 | Easy | `robots/pollen-reachy-2.html` |
| 27 | EngineAI SE01 prijs | 50 | Low | `robots/engineai-se01.html` |
| 28 | UBTECH Walker S2 prijs | 70 | Low | `robots/ubtech-walker-s2.html` |

### Sector long-tails

| # | Keyword | Vol | Diff | Page |
|---|---|---:|---|---|
| 29 | humanoid robot fulfillment | 50 | Easy | `sectoren/3pl-fulfillment.html` |
| 30 | humanoid robot 3PL Nederland | 30 | Easy | `sectoren/3pl-fulfillment.html` |
| 31 | robot picking magazijn | 320 | High | `sectoren/3pl-fulfillment.html` |
| 32 | humanoid robot productie | 70 | Easy | `sectoren/productie-assemblage.html` |
| 33 | robot in de zorg | 1 600 | High | `sectoren/zorg-instellingen.html` |
| 34 | servicerobot zorg | 210 | Med | `sectoren/zorg-instellingen.html` |
| 35 | humanoide robot horeca | 90 | Low | `sectoren/hospitality-retail.html` |

### Local

| # | Keyword | Vol | Diff | Page |
|---|---|---:|---|---|
| 36 | robot leasen Amsterdam | 50 | Low | `leasen/amsterdam.html` |
| 37 | robot leasen Rotterdam | 30 | Easy | `leasen/rotterdam.html` |
| 38 | humanoide robot Eindhoven | 30 | Easy | `leasen/eindhoven.html` |
| 39 | robot leasen Utrecht | 30 | Easy | `leasen/utrecht.html` |
| 40 | robot leasen Den Haag | 20 | Easy | `leasen/den-haag.html` |

### Regulatory / decision support

| # | Keyword | Vol | Diff | Page |
|---|---|---:|---|---|
| 41 | EU AI Act humanoid | 70 | Easy | `gids/ai-act-machineverordening.html` |
| 42 | Machineverordening 2027 | 110 | Low | `gids/ai-act-machineverordening.html` |
| 43 | humanoid robot kosten per maand | 30 | Easy | `kosten.html` |
| 44 | robot operational lease | 90 | Low | `gids/humanoide-robot-leasen.html` |
| 45 | humanoid vs cobot | 50 | Easy | NEW page (gap) |

### Suggested new pages (gaps)

- `/vergelijken/lease-vs-koop` — captures the buying-decision keyword.
- `/vergelijken/humanoid-vs-cobot` and `/vergelijken/humanoid-vs-amr` — high-intent, near-zero NL competition.
- `/case-studies/` hub + 3 case-study posts (anonymized customer stories drive trust + earn editorial links).
- `/faq` — single page targeting "veelgestelde vragen humanoide robot" + supports FAQ-rich-results.

---

## 5. On-page SEO Completeness

### 5a. Meta descriptions — sitewide problem

**33 of 47 indexable pages have a meta description >165 characters.** Google truncates at ~155–160 chars on desktop, ~120 on mobile. Long descriptions still index fine but lose CTR because the tail is cut with "…".

**Specific page lengths:** see full list in the python output above. Critical offenders:
- `gids/ai-act-machineverordening.html` — **258 chars**
- `index.html` — **258 chars**
- `robots/figure-02.html` — 248 chars
- `robots/agility-digit.html` — 244 chars

**Fix:** rewrite the description templates in `scripts/build_robots.py`, `scripts/build_guides.py`, `scripts/build_landingpages.py` and the news/sectoren builders. Target 145–155 chars. Re-run the build.

Example rewrite for `index.html`:
```
Humanoïde robots leasen in Nederland — 15 modellen vanaf €290/mnd, all-in operational lease met installatie, training, swap-SLA en EU AI-Act compliance.
```
(154 chars.)

### 5b. H1 — every page has exactly one. Good.

But the H1 wording is sometimes weak for SEO. Example:
- `robots/unitree-g1.html` H1 = "Unitree G1 Edu leasen." — fine but trailing period and missing "Nederland". Better: "Unitree G1 Edu leasen in Nederland" (matches the title and exact-match keyword).
- `over.html` H1 = "Over BotLease." — pad with "Nederlands eerste humanoid-robot leasemaatschappij".

### 5c. Thin content — pages needing padding

| Page | Words | Target | What to add |
|---|---:|---:|---|
| `sectoren/index.html` | 140 | 700 | Per-sector mini-blurb (3 sentences each) + sector ROI table |
| `gids/index.html` | 167 | 600 | Excerpts of each guide + "wat is een humanoide robot" primer |
| `leasen/index.html` | 187 | 600 | NL coverage map, intake form, FAQ block |
| `vergelijken/*` (all 6) | 286–325 | 800+ | Add full spec table (height, weight, payload, battery, IP-rating, EU compliance), 3-paragraph "wanneer welke" decision tree, FAQ block |
| `leasen/amsterdam.html` etc (5 pages) | 271–278 | 600 | Local industrial parks, postcodes serviced, named customer ref or "first 3 pilots" framing |
| `kosten.html` | 398 | 900 | Worked example per sector, koop-vs-lease table, depreciation note |
| `over.html` | 463 | 700 | Founder bio (Thomas Vedder), KvK 95943420 trust block, AFM disclaimer if applicable, "why we exist" narrative |
| `robots/*.html` (all 15) | 398–482 | 750–1000 | "Wanneer past deze robot bij jou?" / "Wanneer NIET" sections, real spec table, payload/battery in body text (not just card), 3-Q FAQ block. Body text needs to mention the model name + "leasen" 3–5x naturally. |

### 5d. Images & alt text

- Robot pages (15): each has a hero `<img>` and a YouTube thumbnail with alt — OK.
- Sector pages (4): **ZERO `<img>` elements**. Add at least one relevant photo (robot in a warehouse/hospital/hotel setting) with descriptive alt like `alt="Humanoïde robot bij decanting-station in Nederlands fulfillment-center"`. Adds context for Google Images traffic and improves on-page engagement.
- Guide pages: also **zero images** in `gids/humanoide-robot-leasen.html` and `gids/ai-act-machineverordening.html`. Add 3–5 diagrams: 4-stappen pilot-proces, koop-vs-lease tabel als grafiek, AI Act timeline visual.
- City pages: 4 images each — already alt'd.

### 5e. Schema markup status

| Page type | Schema present | Missing |
|---|---|---|
| Home | Organization, WebSite, Service, LocalBusiness, HowTo, FAQPage | — |
| Robot pages | 4 blocks (Product/Offer assumed) | Add `Review`/`AggregateRating` once you have testimonials |
| Sector pages | 3 blocks | Add `Service` per sector |
| Vergelijken | 2 blocks | Add `ItemList` with both products |
| Leasen/{stad} | 2 blocks | Add `LocalBusiness` per city with serviced area |
| Gids pages | 5 blocks | Add `HowTo` for the 4-step process |
| Nieuws | 3 blocks | Add `NewsArticle` (verify NewsArticle vs Article) + `author` + `publisher` |
| Begrippen | 3 blocks | Add `DefinedTermSet` schema — gives glossary rich results |
| Kosten | 2 blocks | Add `HowTo` for calculator + `Offer` |

### 5f. Internal link gaps

You have a sensible structure but the link graph is weaker than it should be. Specific gaps:

- **Robot pages → sector pages.** Every robot detail page should have a "Geschikt voor:" block linking to the 1–3 most relevant sector pages. Currently most don't.
- **Sector pages → robot pages.** `/sectoren/3pl-fulfillment` should link to Agility Digit, Apptronik Apollo, Unitree H1-2 explicitly with anchor text like "Agility Digit leasen voor 3PL".
- **Comparison pages → both robot detail pages.** Verify each `vergelijken/X-vs-Y.html` links to BOTH `/robots/X` and `/robots/Y`.
- **City pages → sector pages.** Eindhoven → productie-assemblage; Rotterdam → 3PL; Utrecht → zorg; Amsterdam → hospitality; Den Haag → mixed.
- **Nieuws posts → relevant robot pages.** E.g. "unitree-g1-mkb-vijf-rendabele-toepassingen" must deep-link `/robots/unitree-g1` 2–3 times with varied anchor text ("Unitree G1 leasen", "G1 specs bekijken", "G1 prijs in 2026").
- **Footer should NOT contain 47-link sitemap.** Pick 8–12 cornerstone links. Keeps link equity flowing to the right pages.
- **Add "Gerelateerde robots" block** at bottom of every robot page (3 links: same price band, same use-case, EU alternative).

### 5g. Canonicals

Audited via grep. All 47 indexable pages have `rel="canonical"`. Confirmed missing only on: `admin.html`, `dashboard.html`, `login.html`, `kennisbank.html`, `chatbot-*.html`, `index-old.html` — all of which are either `noindex` or scheduled for deletion. **No action needed beyond cleaning up legacy.**

---

## 6. Technical SEO Check

### 6a. Sitemap.xml

- **53 URLs declared.** Matches the 47 indexable pages + repeated index URLs. Looks accurate.
- `lastmod` values are fake-stable (`2026-05-18` for everything). Update the build scripts to write the actual file mtime so Google sees real freshness signals.
- **Missing:** `/css/`, `/js/`, image sitemap. Optional but recommended — image-sitemap for `/img/robots/*.webp` will help Google Images.
- **Missing:** news sitemap (`<news:news>` namespace) for `/nieuws/*`. Recommended given you're publishing daily.

### 6b. robots.txt

```
User-agent: *
Allow: /
Disallow: /api/
Disallow: /backend/
Disallow: /admin
Disallow: /admin.html
Sitemap: https://botlease.nl/sitemap.xml
```

- Fine. But also block: `/index-chatbot-backup`, `/chatbot-*`, `/index-old`, `/dashboard`, `/login`, `/kennisbank` to discourage indexing of the legacy/Milo pages *until* you delete them.
- Consider adding `Disallow: /*?utm_*` if you run paid campaigns to keep tracked-URL duplicates out of the index.

### 6c. Page speed

Hot spots (without a real Lighthouse run):
- `index.html` is 969 lines with ALL CSS inline — fine for FCP but check minification at build time. 32 KB+ CSS in `<style>` is acceptable; >50 KB starts hurting LCP.
- Google Fonts loaded synchronously on every page — preload + `font-display: swap` already partially in place (verify on robot pages). Consider self-hosting Inter to remove the `fonts.gstatic.com` blocking request.
- Two analytics scripts on every page: Vercel + Plausible. Pick one. Plausible is GDPR-friendlier and lighter.
- Hero images: `apollo-norm.webp` is referenced as 1000×1250, ~150–250 KB likely. Add `loading="lazy"` to all non-hero images (already done on YouTube embed); add `fetchpriority="high"` to hero only.
- `marked.min.js` (~30 KB) is loaded from CDN — only needed if you render Markdown client-side. If not, remove.

### 6d. Mobile-friendliness

`<meta viewport>` is present on all live pages — good. The Apple-style design uses fluid units; visually checks out. Run https://pagespeed.web.dev/ against `/`, `/robots/unitree-g1`, and `/gids/humanoide-robot-leasen` and aim for LCP <2.5s, CLS <0.05, INP <200ms.

### 6e. Core Web Vitals likely issues

- **LCP**: hero image. Solution: `fetchpriority="high"`, `width`/`height` attrs already present, ensure WebP is <70 KB.
- **CLS**: webfonts could shift. Verify `font-display: swap` is in the `<link>`.
- **INP**: only risk is the calculator on `/kosten`. Profile it.

### 6f. HTTPS / hreflang / structured data validity

- HTTPS: Vercel default, fine.
- hreflang: index.html declares `nl-NL`, `nl-BE`, `x-default` all pointing to `/` — accurate, no Belgian variant maintained.
- Structured data: 100+ JSON-LD blocks across the site. **Validate every page in https://validator.schema.org/** — I cannot run that here but expect some `image` URL mismatches (e.g. `logo.png` may not actually exist at `/logo.png`).

### 6g. Trust signals to add

- Real KvK number on every page footer (KvK 95943420 — currently in `over.html` only).
- BTW number.
- Physical address (Amsterdam) — currently structured-data only.
- AFM/Stichting Leaseauto Registratie? Probably N/A for operational lease of non-consumer goods, but check.

---

## 7. Backlink & Authority Strategy — 10 Concrete Actions

For a brand-new domain, **anchor diversity** and **editorial mentions** matter more than DR. The list below is in **rough priority order** with specific channels and target anchor texts.

### Tier A — Easy wins, do in week 1

1. **NL startup directories** (DR 40–60, free or one-tier-paid):
   - StartupDelta / Techleap.nl — submit BotLease as a robotics startup. Anchor: "BotLease — humanoid robot leasing Nederland".
   - F6S.com, AngelList, Crunchbase, LinkedIn Company Page.
   - Sprout.nl (founder profile feature pitch).
   - MT/Sprout's startup database.

2. **Robotica & maakindustrie associations** (NL):
   - Holland Robotics (hollandrobotics.com) — request member listing.
   - FME (Federatie voor Technologie en Industrie).
   - RoboValley (Delft) — partner page or guest blog.
   - Brainport Eindhoven member directory.

3. **Press pitch** to NL tech press (you have `PRESS_PITCH.md` already):
   - Tweakers.net (story angle: "eerste Nederlandse lease-maatschappij voor humanoïde robots").
   - Bright.nl, Numrush, BNR Tech & Media, RTL Z.
   - Emerce (B2B e-commerce angle for 3PL piece).
   - NRC Tech, FD (Het Financieele Dagblad) — angle: AI Act + €38B market.

### Tier B — Content-led link building

4. **Original research piece**: "De Nederlandse humanoid-robot landschap 2026" — pdf + landing page. Survey 20 NL 3PLs and publish the data. Press, universities and competitors will cite it. This is the highest-leverage one-off content investment you can make.

5. **Linkable assets to build now**:
   - Interactive ROI calculator (different from `/kosten`) — embeddable on partner sites.
   - "AI Act + Machineverordening compliance checklist" PDF download (gate light, no email forced) — already partially in `gids/ai-act-machineverordening.html`.
   - Free PDF spec-sheet for every robot model.

6. **Guest posts** on:
   - Logistiek.nl (3PL angle).
   - Distrifood (retail/fulfillment).
   - Skipr (zorg-IT).
   - Computable.nl (IT-decision-makers).
   - Anchor each with "humanoide robot leasen".

### Tier C — Long-tail authority

7. **LinkedIn**:
   - Thomas Vedder personal page — 2 posts/week, link to relevant `/nieuws/*` articles.
   - BotLease company page — repost the news articles.
   - Join the "Robotica Nederland" group and answer questions referencing your guides.

8. **YouTube** (huge missing channel):
   - Upload a 90-second "Unitree G1 in 90 seconds" demo. Embed it back into `/robots/unitree-g1`.
   - "Wat is een humanoid robot?" — 3-minute explainer, link to `/gids/humanoide-robot-leasen`.
   - Each video description = a backlink to a specific page.

9. **University outreach** (TU Delft, TU/e, WUR, UvA):
   - Pollen Reachy 2, PAL TIAGo Pro — these are research darlings. Offer a 6-month subsidized pilot in exchange for a public case study + link from `.tudelft.nl` (DR ~89).
   - Single `.edu`-equivalent link from TU/e or TU Delft is worth ~100 directory links.

10. **Wikipedia**:
    - Edit existing NL pages for "Humanoïde robot", "Operational lease", "Unitree", "NEURA Robotics" to add a 1-sentence factual mention with a citation to a BotLease guide (do this carefully and conservatively, citing only verifiable facts — not promotional). Wikipedia links are `nofollow` but drive referral traffic + trust.

---

## WEEK 1 PUNCH LIST (impact ÷ effort, top 10)

Order them by ROI — do **#1 today**, the rest this week.

| # | Action | Effort | Impact | Why |
|---|---|---|---|---|
| 1 | **Delete the 5 chatbot legacy HTML files + add 301s in `vercel.json`** | 15 min | **Massive** | This is the literal reason Google still shows you as a chatbot company. Fixes the `site:botlease.nl` SERP within 2 weeks of recrawl. |
| 2 | **Submit fresh sitemap to Google Search Console + Bing Webmaster + request indexing of `/` and `/gids/humanoide-robot-leasen`** | 20 min | High | Tells Google your site exists with the new structure. The current meta tag still has `REPLACE-WITH-GSC-TOKEN` in `index.html` line 42 — **fix that first**. |
| 3 | **Rewrite every meta description to ≤155 chars** by updating templates in `scripts/build_robots.py`, `build_guides.py`, `build_landingpages.py`, `build_news.py` and regenerating | 1 hour | High | CTR boost across all 33 affected pages. |
| 4 | **Pad the 6 vergelijken/* pages from 286–325 → 800+ words** each with spec tables, decision tree, FAQ | 2 hours | High | Comparison queries are highest-intent. Owning them = direct lease conversions. |
| 5 | **Add real GSC verification token + Bing token** (currently `REPLACE-WITH-…` placeholders in `index.html`) | 5 min | High | Without this no indexation diagnostics are possible. |
| 6 | **Add `<img>` to all 4 sector pages and 2 guide pages** with descriptive alts | 1 hour | Med-high | Image SEO + engagement signals. |
| 7 | **Add "Gerelateerde robots" + "Geschikt voor sector" link block to every robot page** | 1 hour (build-script edit) | Med-high | Strengthens internal link graph; spreads authority. |
| 8 | **Submit to Holland Robotics + Brainport Eindhoven + Techleap + F6S** (4 directory submissions) | 30 min | Med | First DR 40+ backlinks. |
| 9 | **Set up Google Business Profile** as "BotLease Amsterdam" with category "Equipment leasing service" | 15 min | Med | Local pack visibility on "robot leasen Amsterdam"-type queries. |
| 10 | **Publish 1 original-data nieuws post** ("BotLease pilot-dashboard week 1: 14 intake-aanvragen, 3 sectoren, 5 modellen") | 1 hour | Med-low | Generates one more fresh, link-worthy URL per week and demonstrates traction. |

---

## Honest Timeline to #1 for "humanoide robot leasen Nederland"

- **Weeks 1–3**: Punch list executed → Google reindexes → `site:botlease.nl` SERP changes from chatbot to lease. **Pages start appearing for long-tail queries.**
- **Weeks 4–8**: Long-tail (`unitree g1 leasen`, `apptronik apollo Nederland`, `humanoid robot Eindhoven`) ranking 5–20.
- **Months 3–4**: Mid-tail (`humanoide robot prijs`, `humanoid robot kosten`) ranking 5–15. **Page 1 for `humanoide robot leasen` if 5+ quality backlinks landed.**
- **Months 5–8**: Page 1 stable on `humanoide robot leasen Nederland`. Top-3 plausible if competitor activity remains low and you've earned a TU Delft or Brainport mention.
- **Months 9–12**: #1 achievable IF you've shipped a survey-based industry report and earned editorial coverage in Tweakers/Emerce/Bright. Domain authority will still be lower than Smartrobot.solutions' decade of age, but you can out-content them on every specific query they don't currently rank for.

**The keyword "humanoide robot leasen" is open. Nobody owns it. Speed of execution + cleanup of legacy chatbot pages decides whether you take it now or in 18 months.**
