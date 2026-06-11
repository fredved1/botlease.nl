# BotLease — Operations & runbook

Alles wat je moet weten om de site te beheren, troubleshooten, en uit te breiden.
Bewaar dit document zorgvuldig — bevat ook geheimen-referenties (zelf de waarden zijn elders).

---

## TL;DR — Snel overzicht

| Wat | Waar | Hoe |
|---|---|---|
| **Website live** | https://botlease.nl | Vercel project `botlease-v2` |
| **Code** | `/Users/werk/Documents/Python/botlease.nl` | GitHub `fredved1/botlease.nl` |
| **Deploy** | `vercel --prod --yes` vanuit repo root | Of: push naar `master` (auto-deploy) |
| **Contact form** | `botlease.nl/#contact` | Mail komt op **hallo@botlease.nl** |
| **Admin dashboard** | `botlease.nl/admin` | Login met ADMIN_PASSWORD (1Password) |
| **Email service** | Resend.com account: hallo@botlease.nl | Free tier 3.000 mails/mnd |
| **Database backup** | Supabase project `hzexwxpnsqggbxklpues` | Tabel `contacts` |
| **Analytics** | plausible.io | Sign-up + domain toevoegen botlease.nl |

---

## 1. Architectuur — wat draait waar?

```
[Bezoeker]
    │
    │ (browser)
    ▼
[botlease.nl] ◄────── Vercel CDN (edge cache)
    │                 ├── /                       (homepage)
    │                 ├── /robots/<slug>          (15 robot pagina's)
    │                 ├── /sectoren/<slug>        (4 sectoren)
    │                 ├── /leasen/<slug>          (5 steden)
    │                 ├── /gids/<slug>            (pillar + AI-Act gidsen)
    │                 ├── /vergelijken/<a>-vs-<b> (head-to-head)
    │                 ├── /nieuws/<slug>          (10 nieuwsartikelen)
    │                 ├── /kosten · /begrippen · /over · /methodologie
    │                 └── /admin                  (password protected dashboard)
    │
    ▼ (form submit)
[Vercel Serverless Functions]
    ├── /api/contact      → ontvangt formulier, stuurt 2x email + backup naar Supabase
    └── /api/admin-list   → returns submissions voor /admin dashboard (password gated)

[Resend.com] ◄──── /api/contact stuurt:
    ├─ Notification email naar hallo@botlease.nl (met reply-to = aanvrager)
    └─ Auto-confirmation naar aanvrager (met links naar guides)

[Supabase] ◄──── /api/contact slaat backup-rij op in tabel `contacts`
              /api/admin-list haalt deze rijen op voor dashboard
```

---

## 2. Contact form — de complete flow

### Wat gebeurt er als iemand het formulier op botlease.nl invult?

1. **Browser** → form POST naar `/api/contact` met JSON body
2. **Vercel function `/api/contact.js`**:
   - Valideert (naam + email verplicht, email-formaat check)
   - Stuurt 3 dingen parallel:
     - **Notification mail** → `hallo@botlease.nl` via Resend
       - From: `BotLease <onboarding@resend.dev>` (totdat je domain verifieert in Resend)
       - To: `hallo@botlease.nl`
       - Reply-to: `<email van aanvrager>` ← jij kunt op "Reply" klikken en mailt direct met klant
       - Subject: `[BotLease] Lease-aanvraag van <bedrijf> — <sector>`
       - Body: gestylde HTML met alle velden
     - **Auto-confirmation** → `<email aanvrager>` via Resend
       - "Bedankt — wij nemen binnen 4 werkuren contact op" met links
     - **Supabase backup** → tabel `contacts`
       - Velden: name, email, phone, company, message, created_at
3. **Browser** krijgt JSON response → toont success-card

### Wat als Resend niet werkt of er een fout is?

- Function logt naar Vercel Functions logs
- Supabase backup gaat door (zolang Supabase werkt)
- Bezoeker krijgt error met "mail direct naar hallo@botlease.nl"
- Check de logs: `vercel logs https://botlease.nl --since 1h`

---

## 3. Admin dashboard — `/admin`

### Hoe werkt het?

- URL: **https://botlease.nl/admin**
- Login: het ADMIN_PASSWORD (in je password manager — zie sectie 4)
- Wachtwoord wordt opgeslagen in `sessionStorage` van je browser (verlopen bij tab-close)
- Niet geïndexeerd door Google (robots.txt + noindex meta)

### Wat zie je?

- **Stats**: totaal aanvragen, vandaag, deze week, deze maand
- **Tabel**: datum, naam, bedrijf, email (klikbaar → opent mail-client), sector + bericht
- **Zoekfilter**: typ in zoekveld om filtreren
- **CSV export**: knop "Export CSV" downloadt alle aanvragen als CSV bestand
- **Vernieuwen**: knop "Vernieuw" haalt laatste data op

### Onder de motorkap

- `frontend/admin.html` is statische HTML
- Roept `/api/admin-list.js` aan met POST + password
- Function check password tegen `ADMIN_PASSWORD` env var
- Als correct: haalt alle rijen uit Supabase `contacts` tabel (max 200, sorteert op created_at desc)
- Returns JSON naar frontend → tabel rendert

### Password vergeten?

- Reset via Vercel: `vercel env rm ADMIN_PASSWORD production` → daarna opnieuw zetten
- Niet recoverable — alleen vervangen mogelijk

---

## 4. Environment variables — wat staat waar?

Bekijk alles: `vercel env ls` (vanuit repo root)

| Naam | Functie | Waar gemaakt | Vervangen / rotaten? |
|---|---|---|---|
| `RESEND_API_KEY` | Email versturen via Resend | resend.com → API Keys | Maak nieuwe key in Resend → `vercel env rm RESEND_API_KEY production` → `vercel env add RESEND_API_KEY production` (paste new key) → `vercel --prod --yes` |
| `ADMIN_PASSWORD` | /admin login | self-generated | `vercel env rm ADMIN_PASSWORD production` → `printf 'NIEUW_WACHTWOORD' \| vercel env add ADMIN_PASSWORD production` → redeploy |
| `RESEND_FROM` | (optioneel) Custom afzender-naam | self-set | Default: `BotLease <onboarding@resend.dev>`. Nadat je botlease.nl verifieert in Resend: zet op `BotLease <noreply@botlease.nl>` |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL | Supabase dashboard | Verandert niet — alleen bij project-migratie |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase public key | Supabase dashboard | Roteren via Supabase → Settings → API |
| `SUPABASE_SERVICE_KEY` | Supabase admin key | Supabase dashboard | NIET commiten/delen! Server-side only |
| `OPENROUTER_API_KEY` | (legacy) Chatbot AI — niet meer actief gebruikt | openrouter.ai | Kan verwijderd worden |

**Pas op**: env vars zijn per **environment** (Production / Preview / Development). Wij gebruiken alleen Production. Als je een var toevoegt voor Preview moet je ook ze daar zetten.

---

## 5. Resend — email service uitleg

### Wat is het?

Resend is een moderne transactional email API (zoals SendGrid, Mailgun maar developer-friendly). Wij gebruiken het voor alle uitgaande mail vanaf botlease.nl.

### Account

- Gebruikersnaam: `hallo@botlease.nl`
- Dashboard: https://resend.com/dashboard
- Plan: **Free** — 3.000 mails/maand · 100/dag · onbeperkt domeinen

### Hoe upgrade ik naar de Pro plan?

- $20/maand → 50.000 mails/maand
- Resend dashboard → Settings → Billing → kies plan

### Domain verificatie (aanbevolen, eenmalig)

Standaard verstuurt Resend van `onboarding@resend.dev`. Dat werkt prima, maar voor professionaliteit:

1. Resend dashboard → **Domains** → "Add Domain" → `botlease.nl`
2. Resend toont DNS records (3-4 stuks: SPF, DKIM, DMARC)
3. **Vercel** (waar DNS van botlease.nl waarschijnlijk staat) → DNS → voeg de records toe
4. Wacht 5-30 minuten → Resend "Verify" → groen vinkje
5. Vervolgens: voeg env var `RESEND_FROM` toe met waarde `BotLease <noreply@botlease.nl>`:
   ```bash
   printf 'BotLease <noreply@botlease.nl>' | vercel env add RESEND_FROM production
   vercel --prod --yes
   ```

### Logs / debug

- Resend dashboard → **Emails** → ziet elke verstuurde mail, status (delivered/bounced/spam)
- Vercel logs → `vercel logs --since 1h` → ziet onze function-side logs

### Limit-monitoring

- Free tier reset elke 1e van de maand
- Dashboard toont je verbruik
- Stel notificatie in: Resend → Settings → Notifications → "80% van limit"

---

## 6. Supabase — database

### Account

- Project: `hzexwxpnsqggbxklpues`
- URL: https://hzexwxpnsqggbxklpues.supabase.co
- Dashboard: https://supabase.com/dashboard
- Plan: Free (500 MB storage, 50.000 monthly active users)

### Tabel `contacts`

| Kolom | Type | Beschrijving |
|---|---|---|
| `id` | uuid | Auto-generated primary key |
| `name` | text | Naam aanvrager |
| `email` | text | Email aanvrager |
| `phone` | text | Telefoon (optioneel) |
| `company` | text | Bedrijfsnaam |
| `message` | text | `[<sector>] <bericht>` — sector als prefix |
| `created_at` | timestamp | Auto, wanneer rij is aangemaakt |

### Direct in Supabase kijken

1. Supabase dashboard → **Table editor** → `contacts`
2. Filter, sorteer, edit, delete handmatig
3. Of via SQL editor: `SELECT * FROM contacts ORDER BY created_at DESC LIMIT 50`

### Backup / export

- Dashboard → **Database** → "Backups" — Supabase doet zelf daily backups op Free tier (7 dagen retention)
- Manual export via SQL: `SELECT * FROM contacts` → "Export to CSV"

---

## 7. Deploy & build flow

### Hoe deploy ik?

Vanuit repo root:

```bash
cd /Users/werk/Documents/Python/botlease.nl
vercel --prod --yes
```

Of: gewoon committen en pushen naar `master` op GitHub → Vercel deployt automatisch.

```bash
git add -A
git commit -m "wat heb ik veranderd"
git push origin master
# Vercel detecteert push, deployt binnen ~30 sec
```

### Wat staat waar?

```
/Users/werk/Documents/Python/botlease.nl/
├── frontend/                    # ← Dit wordt gedeployed
│   ├── index.html               # Homepage (static)
│   ├── admin.html               # Admin dashboard (static)
│   ├── robots.txt               # Auto-generated
│   ├── sitemap.xml              # Auto-generated
│   ├── rss.xml                  # Auto-generated
│   ├── api/                     # Vercel serverless functions
│   │   ├── contact.js           # Form submission → email
│   │   ├── admin-list.js        # Admin dashboard data
│   │   └── ... (legacy: chat, debug, scrape, waitlist)
│   ├── img/robots/              # Robot foto's (jpg/png/webp)
│   ├── nieuws/                  # 10 nieuwsartikelen
│   ├── robots/                  # 15 robot detailpagina's + hub
│   ├── sectoren/                # 4 sector-pagina's + hub
│   ├── leasen/                  # 5 stad-pagina's + hub
│   ├── gids/                    # 2 pillar guides + hub
│   ├── vergelijken/             # 6 head-to-head + hub
│   ├── kosten.html              # Lease calculator
│   ├── begrippen.html           # Glossary
│   ├── over.html · methodologie.html
│   └── vercel.json              # Vercel config
├── scripts/                     # Build scripts (Python 3)
│   ├── articles_data.py         # ← Edit hier voor nieuwe artikelen
│   ├── robots_data.py           # ← Edit hier voor nieuwe robots
│   ├── landingpages_data.py     # ← Edit hier voor sectoren/steden
│   ├── guides_data.py           # ← Edit hier voor pillar/AI-Act/glossary
│   ├── seo_common.py            # Shared analytics + verification snippets
│   ├── build_news.py            # Rebuilds /nieuws + sitemap + RSS
│   ├── build_robots.py          # Rebuilds /robots
│   ├── build_landingpages.py    # Rebuilds /sectoren + /leasen
│   └── build_guides.py          # Rebuilds /gids + /vergelijken + others
└── index.html                   # ← Kopie van frontend/index.html (Vercel root)
```

### Hoe rebuild ik na het bewerken van data?

Bewerk data files (`articles_data.py`, `robots_data.py`, etc.), draai dan:

```bash
cd /Users/werk/Documents/Python/botlease.nl
python3 scripts/build_robots.py        # Robot pagina's
python3 scripts/build_landingpages.py  # Sectoren + steden
python3 scripts/build_guides.py        # Gidsen + vergelijken
python3 scripts/build_news.py          # Nieuws + sitemap (DRAAI ALTIJD ALS LAATSTE — bouwt sitemap)
cp frontend/index.html index.html      # Sync root index met frontend
```

Of in één commando:

```bash
python3 scripts/build_robots.py && \
python3 scripts/build_landingpages.py && \
python3 scripts/build_guides.py && \
python3 scripts/build_news.py && \
cp frontend/index.html index.html
```

### Hoe deploy ik handmatig na rebuild?

```bash
git add -A
git commit -m "rebuild: <wat veranderd>"
git push origin master
# Of force deploy:
vercel --prod --yes
```

---

## 8. Veelvoorkomende taken

### Nieuw nieuwsartikel toevoegen

1. Open `scripts/articles_data.py`
2. Append een nieuw dict (kopieer een bestaande als template)
3. Velden: slug, title, subtitle, category, date (YYYY-MM-DD), reading_time, intro, body (lijst van (tag, content) tuples), sources, tags
4. Voor de foto: ofwel verwijs naar bestaande robot-foto, ofwel voeg nieuwe `ART_BY_SLUG` mapping toe in `scripts/build_news.py`
5. Rebuild + deploy

### Nieuwe robot toevoegen

1. Open `scripts/robots_data.py`
2. Append nieuw dict in `ROBOTS` lijst
3. Velden: slug, name, vendor, vendor_country, category (`available`/`waitlist`), tier (`eu`/`value`/`premium`), badge, photo, photo_dims, tagline, short, height_cm, weight_kg, payload_kg, battery_hours, dof, speed_ms, lease_eur, setup_eur, purchase_eur, use_cases, specs_detail, tags, vendor_url, video_id (optional), video_title (optional)
4. Download de foto naar `frontend/img/robots/<slug>.jpg|webp|png`
5. Rebuild + deploy

### Nieuwe sectorpagina toevoegen

1. Open `scripts/landingpages_data.py`
2. Append in `SECTORS` lijst
3. Velden: slug, name, title_kw, h1, tagline, intro, metrics, subsections, recommended_robots (list of robot slugs), questions
4. Rebuild + deploy

### Stad toevoegen

1. Open `scripts/landingpages_data.py`
2. Append in `CITIES` lijst
3. Velden: slug, name, title_kw, intro, sectors_in_focus, local_hooks
4. Rebuild + deploy

### Robot uit catalogus halen

In `scripts/robots_data.py`: zet `"category": "waitlist"` of verwijder helemaal (de pagina blijft tot je rebuild + deploy).

### Pagina uit sitemap halen (de-index)

Voeg `Disallow: /pad` toe in `build_news.py` → `render_robots()` functie. Rebuild + deploy.

---

## 9. Troubleshooting

### "Het contactformulier werkt niet"

1. Check Vercel logs: `vercel logs --since 30min`
2. Zoek naar `[contact]` regels
3. Mogelijke oorzaken:
   - `RESEND_API_KEY` ontbreekt of verlopen → check `vercel env ls`
   - Resend account suspended (te veel bouncing/spam) → check resend.com dashboard
   - Supabase neer → check status.supabase.com
4. Test direct in browser console:
   ```js
   fetch('/api/contact', {
     method:'POST',
     headers:{'Content-Type':'application/json'},
     body: JSON.stringify({ naam:'Test', email:'test@example.com', bedrijf:'Test BV' })
   }).then(r => r.json()).then(console.log)
   ```

### "/admin geeft 'Onjuist wachtwoord' bij correct wachtwoord"

- Check `vercel env ls` → staat `ADMIN_PASSWORD` er nog?
- Heeft de laatste deploy de env var gepickt? Trigger redeploy: `vercel --prod --yes`
- Check Vercel function logs voor `[admin-list]` regels

### "Pagina geeft 404"

- Wel in frontend/ directory? `ls frontend/<pad>`
- Sitemap up-to-date? `cat frontend/sitemap.xml | grep <pad>`
- Vercel build successful? Check Vercel dashboard → Deployments

### "Build script faalt"

- Python 3 vereist (`python3 --version` → 3.10+)
- Vanuit repo root draaien
- Check syntax errors in data files met `python3 -c "import scripts.robots_data"`

### "Plausible Analytics toont geen data"

- User moet eerst sign-uppen op plausible.io
- Domain toevoegen: `botlease.nl`
- Plan: $9/mnd voor 10k pageviews
- Geen actie in code nodig — script staat al op alle pagina's

### "GSC / Bing tonen 'unverified'"

- User moet het TOKEN-placeholder vervangen in:
  - `frontend/index.html` (homepage)
  - `scripts/seo_common.py` (alle gegenereerde pagina's)
- Daarna rebuild + deploy
- Daarna kan user verifiëren via Google Search Console

---

## 10. Veiligheid — wat te NIET committen

In de hele repo staan **geen secrets**. Wat NIET commit moet worden:

- ❌ Echte API keys (Resend, Supabase service key, OpenRouter)
- ❌ `ADMIN_PASSWORD` waarde
- ❌ Resend account-wachtwoorden
- ❌ Vercel auth tokens

Wat staat WEL in repo:

- ✅ Placeholder strings (`REPLACE-WITH-GSC-TOKEN`, `XXXXXXXX` voor KvK)
- ✅ Supabase public URL (publiek, hoort in NEXT_PUBLIC_*)
- ✅ Supabase anon key (publiek, expliciet bedoeld voor frontend gebruik — heeft alleen RLS-beperkte access)

### Als je per ongeluk een secret commit:

1. **Maak de key gelijk ongeldig** (Resend dashboard → API Keys → Revoke)
2. Genereer een nieuwe key, vervang in Vercel env
3. (Optioneel) git history cleanen — niet nodig als key al revoked, want dan is hij waardeloos
4. Trigger redeploy

---

## 11. Belangrijke URLs (bookmark in 1Password of browser)

| Dienst | URL |
|---|---|
| Live site | https://botlease.nl |
| Admin dashboard | https://botlease.nl/admin |
| Vercel project | https://vercel.com/fredved1s-projects/botlease-v2 |
| GitHub repo | https://github.com/fredved1/botlease.nl |
| Resend dashboard | https://resend.com/emails |
| Supabase project | https://supabase.com/dashboard/project/hzexwxpnsqggbxklpues |
| Plausible | https://plausible.io/botlease.nl (nadat je domein toevoegt) |
| Google Search Console | https://search.google.com/search-console |
| Bing Webmaster Tools | https://www.bing.com/webmasters |

---

## 12. Wachtwoorden / secrets reminder

⚠️ **Wat je bewaart in je password manager (1Password / Bitwarden / etc.):**

- `ADMIN_PASSWORD` voor /admin login (je hebt deze van mij gekregen toen ik hem zette)
- Resend.com login (hallo@botlease.nl + wachtwoord dat je daar koos)
- Resend API key zelf (begint met `re_...`) — kun je niet meer ophalen uit Resend dashboard, alleen revoken
- Supabase login (waarschijnlijk linked aan je Github)
- Vercel login (linked aan je Github)

⚠️ **Wat je gewoon vergeet:**

- Mailwachtwoord van `hallo@botlease.nl` (in mailclient/Apple Mail)
- Domain registrar login (bij wie staat botlease.nl?)

Schrijf op waar deze staan voordat je het vergeet.

---

## 13. Wat komt er nog (optioneel)

Lijst van features die nog gebouwd kunnen worden — geen volgorde, niet kritiek:

- Live chat widget (Crisp, Intercom, of eigen Slack-bridge)
- Lighthouse audit + page speed optimalisatie
- Lazy-loaded YouTube embeds met facade
- /en/ Engelse versie van de site (Belgisch + Duits MKB bereik)
- Custom 404 pagina met search-suggesties
- Webinar registratie module
- Klant-portaal (account.botlease.nl) waar leasers hun robot-status zien
- Affiliate-systeem voor SI-partners
- Robot-specifieke landing pages voor SEA (Google Ads)
- A/B testing op headers/CTAs via Vercel Edge Config
- Slack-integratie: elke aanvraag → notification in #botlease-leads channel

---

**Laatste update**: 18 mei 2026 — door initial setup met Claude Opus 4.7
