# Google Search Console + Bing Webmaster Tools — stap voor stap

## A. Google Search Console (15 min)

1. Ga naar **https://search.google.com/search-console**
2. Inloggen met je Google-account (zorg dat dat dezelfde is die je voor BotLease wil gebruiken)
3. Klik "**Property toevoegen**" → kies **"URL-prefix"** (NIET "Domain", want dat vergt DNS-toegang)
4. Vul in: `https://botlease.nl/` en klik **Doorgaan**
5. Google geeft je een **HTML-tag** met een verificatiecode. Het ziet eruit zoals:
   ```html
   <meta name="google-site-verification" content="aBcDeFGH12345...">
   ```
6. **Kopieer alleen de `content`-waarde** (het stuk tussen aanhalingstekens na `content=`)
7. Set de waarde als environment variable in Vercel:
   ```bash
   vercel env add BOTLEASE_GSC_TOKEN production
   # Plak de token-waarde wanneer gevraagd
   ```
   Of lokaal voor één-malig builden:
   ```bash
   export BOTLEASE_GSC_TOKEN="aBcDeFGH12345..."
   ```
8. Run in je repo-terminal:
   ```bash
   python3 scripts/build_robots.py
   python3 scripts/build_guides.py
   python3 scripts/build_landingpages.py
   python3 scripts/build_news.py
   vercel --prod --yes
   ```
9. Wacht ~30 seconden, ga terug naar Search Console, klik **Verifiëren**.
10. Klik in het linkermenu **Sitemaps** → vul in: `sitemap.xml` → **Verzenden**.
11. Klik daarna in linkermenu **URL-inspectie**. Plak deze URL's één voor één en vraag **Indexering aanvragen** voor elk:
    - `https://botlease.nl/`
    - `https://botlease.nl/robots/`
    - `https://botlease.nl/gids/humanoide-robot-leasen`
    - `https://botlease.nl/kosten`
    - `https://botlease.nl/vergelijken`

**Wat je vandaag nog ziet:** een dashboard met "Geen gegevens beschikbaar". Dat is normaal — Google moet eerst crawlen en data verzamelen. **Eerste impressies verschijnen binnen 3-10 dagen.**

---

## B. Bing Webmaster Tools (10 min)

1. Ga naar **https://www.bing.com/webmasters/**
2. Inloggen met Microsoft- of Google-account
3. **Add a site** → vul in: `https://botlease.nl`
4. Kies **Import from Google Search Console** als beschikbaar (snelste route, vereist dat je GSC al hebt gedaan). Anders kies "HTML Meta Tag" verificatie en volg dezelfde route als GSC:
   - Kopieer de meta-tag content waarde
   - Set als Vercel env var: `vercel env add BOTLEASE_BING_TOKEN production`
   - Rebuild + deploy (zie GSC stap 8)
5. Verifieer in Bing dashboard
6. **Sitemaps** → **Submit a Sitemap** → `https://botlease.nl/sitemap.xml`

Bing dekt ~5-10% van NL searches. Gratis, kost niets, dus altijd doen.

---

## C. IndexNow (extra, 5 min — pushes new URLs naar Bing/Yandex direct)

1. Genereer een API-key (UUID) bijvoorbeeld via `uuidgen` in terminal
2. Maak in `/frontend/` een file `<key>.txt` met als enige inhoud die UUID-string
3. Voeg in Bing Webmaster Tools je IndexNow key toe via Settings → IndexNow

Dit is optioneel maar elke nieuwe nieuws-post triggert dan automatische herindexering binnen 1-2 minuten i.p.v. dagen.

---

## D. Verificatie deze maand

Open elke week even GSC → Performance. Verwacht dit traject:

| Week | Wat zien |
|---|---|
| Week 1 (vandaag tot +7d) | 0 impressies, "Geen data" |
| Week 2 | Eerste 50-200 impressies, mogelijk geen klikken |
| Week 3-4 | 200-1.000 impressies, eerste klikken op long-tail |
| Week 6-8 | 1.000+ impressies, branded queries beginnen te lopen |

Update dan in `seo/seo_data.json` de ranks via `python3 scripts/seo_add_check.py` zodat het dashboard de progressie pakt.
