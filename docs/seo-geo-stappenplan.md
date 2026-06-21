# SEO/GEO-stappenplan BotLease

*Doel: ranken in Google én geciteerd worden door AI (ChatGPT/Gemini/Claude) op "humanoïde robot huren/leasen", "robot huren event/beurs" en per-stad/sector-varianten. — juni 2026*

---

## Diagnose (bijgewerkt 21 juni)

**Update:** de oude-cache-blokkade is voorbij. De rank-bot (Google.nl, 19 juni) toont **#1 op "humanoïde robot leasen Nederland" + Engelse variant** (2/23 keywords). De overige 21 — inclusief **"huren"** (north-star) en alle modellen/sectoren/steden — staan nog op 0. On-site is af én begint te ranken; de winst zit nu in **off-site autoriteit** + **"huren" omhoog krijgen**. NB: meet NL-rankings met de rank-bot, niet met de WebSearch-tool (US-only → vals "ranken nergens").

De **on-site SEO is technisch af** (sitemap, schema, llms.txt, robots.txt, snelheid, transparante prijzen). De resterende knelpunten:

1. **Geen autoriteit.** De site is jong en heeft vrijwel geen links van buitenaf. Google heeft weinig reden om 'm breed hoog te zetten of vaak te crawlen.
2. **NLrobotics = betaald → overgeslagen.** De #1-rankende [NLrobotics "Humanoids in Nederland"](https://www.nlrobotics.nl/humanoids-in-nederland) vraagt geld voor opname/lidmaatschap; pre-eerste-deal niet doen. Gratis alternatieven (LinkedIn, GBP, Crunchbase/Dealroom/Techleap/F6S, Wikidata) leveren dezelfde backlink/autoriteit.
3. **"Huren" rankt nog 0** terwijl het de eerste-omzet-prioriteit is. Homepage-H1 staat nu op "huren of leasen" (21 juni live); herindexering aangevraagd.

**De drie grootste hefbomen:** (1) op NLrobotics komen, (2) off-site autoriteit opbouwen (Google Bedrijfsprofiel + directories + LinkedIn), (3) verse content blijven publiceren.

**Master NAP-profiel** (overal exact zo gebruiken — consistentie is een Google-vertrouwenssignaal):
- Naam: **BotLease**
- Plaats: **Amsterdam** (servicegebied: heel Nederland; geen bezoekadres)
- Telefoon: **+31 6 2369 2944**
- E-mail: **hallo@botlease.nl**
- Web: **https://botlease.nl**

---

## FASE 1 — NU (deze week, hoog effect / laag werk)

| # | Actie | Hoe | Wie |
|---|---|---|---|
| 1 | **Op NLrobotics komen** | Mail/aanmelden bij NLrobotics (nlrobotics.nl) — vraag om opname in "Humanoids in Nederland" + lidmaatschap 1-10 medewerkers. Dit is de #1-rankende pagina op onze zoekwoorden. | Thomas (Claude zet de mail klaar) |
| 2 | **Google Bedrijfsprofiel aanmaken** | business.google.com → bedrijf zonder bezoekadres → servicegebied "Nederland" → categorie "Robotverhuur"/"Verhuurbedrijf". Geeft Maps-zichtbaarheid + sterk autoriteitssignaal. | Thomas (~15 min) |
| 3 | **Bing Webmaster Tools + sitemap indienen** | bing.com/webmasters → site toevoegen (kan via GSC importeren) → sitemap indienen. Bing voedt ook ChatGPT-zoekresultaten. | Thomas |
| 4 | **GSC: homepage + kernpagina's opnieuw indexeren** | Search Console → URL-inspectie → indexering aanvragen voor /, /huren, /robot-huren-evenement, /prijzen, /robots. Sitemap opnieuw indienen (datums zijn vers). | Thomas |
| 5 | **LinkedIn-bedrijfspagina aanmaken** | Bedrijfspagina BotLease (tekst staat klaar in OUTREACH/geo-offsite-plan.md). Levert backlink + de `sameAs` voor het schema. | Thomas (Claude levert tekst) |

---

## FASE 2 — KORTE TERMIJN (2-4 weken)

| # | Actie | Hoe | Wie |
|---|---|---|---|
| 6 | **Bedrijvengidsen, gespreid (2-3/week)** | Gratis vermeldingen met master-NAP. Lijsten: targetvision top-100, connectyourworld (62 gidsen), kliq top-5 gratis. Niet alles tegelijk = natuurlijk linkprofiel. | Thomas (Claude levert de NAP-tekst + lijst) |
| 7 | **Wikidata-item aanmaken** | BotLease als entiteit op Wikidata (founder Thomas Vedder, sector robotverhuur, web). AI-modellen putten hieruit. | Claude bereidt voor, Thomas plaatst |
| 8 | **LinkedIn founder-content (3×/week)** | Thomas post over humanoid-verhuur/lease, events, compliance. Bouwt merk + verwijst naar de site. | Thomas (Claude kan posts klaarzetten) |
| 9 | **sameAs site-breed toevoegen** | Zodra LinkedIn/Wikidata/GBP live zijn: hun URL's in het Organization-schema zetten (alle pagina's). | Claude |
| 10 | **Vakmedia benaderen** | Rocking Robots / Emerce: een nieuwsbericht of gastbijdrage over "eerste onafhankelijke humanoid-verhuur in NL". Levert een gezaghebbende backlink. | Thomas (Claude schrijft het bericht) |
| 11 | **Eventkalenders (WoTS e.d.)** | Als exposant/deelnemer op de WoTS-site en andere eventkalenders = backlink + relevante zichtbaarheid. | Thomas |

---

## FASE 3 — DOORLOPEND

| # | Actie | Hoe | Wie |
|---|---|---|---|
| 12 | **Wekelijks nieuws publiceren** | De nieuws-engine elke week een vers artikel laten publiceren (verse content = Google crawlt vaker = hogere autoriteit). ✅ **Opgelost 19 juni:** schrijft nu via de claude CLI (abonnement), VPS-clone herbouwd, durable runner `scripts/run_news_vps.sh` doet pull→schrijven→commit→push→deploy. Timer: vrijdag 17:00. Monitoren via `/root/botlease-news/logs/newsbot-latest.log` (RESULT-regel). | Automatisch (timer); Claude monitort |
| 13 | **Interne links onderhouden** | Nieuwe pagina's/artikelen naar elkaar laten linken; verhuurpagina's blijven doorlinken. | Claude |
| 14 | **GSC monitoren** | Wekelijks: indexering-status, welke zoekwoorden vertonen, klikken. Bijsturen op wat begint te ranken. | Claude (op afroep) + Thomas |
| 15 | **Long-tail content uitbreiden** | Per stad/sector pagina's die nog ontbreken (bv. "robot huren beurs Utrecht"), zodra de basis rankt. | Claude |

---

## Realistische tijdlijn

- **Week 1-2:** oude cache verdwijnt, nieuwe site-versie in de index (na herindexering + verse sitemap).
- **Week 2-6:** eerste off-site signalen (GBP, directories, NLrobotics, LinkedIn) worden opgepikt → begin van autoriteit.
- **Maand 2-4:** eerste posities op long-tail zoekwoorden ("humanoïde robot huren [stad]", "robot huren beurs").
- **Maand 4-9:** als de markt aantrekt en de autoriteit groeit, posities op de kernzoekwoorden. AI-citaties volgen de autoriteit + Wikidata/llms.txt.

**Eerlijk:** SEO/GEO is weken tot maanden, geen knop. De on-site basis staat (dat was het werk dat móést gebeuren). De winst zit nu **off-site** — vooral op NLrobotics komen en een handvol autoriteitslinks opbouwen. Dat is bewust laag-werk/hoog-effect.

---

## Wat Claude klaarzet (zodat Thomas alleen hoeft te plaatsen)
- De NLrobotics-aanmeldmail (Fase 1.1)
- De master-NAP-tekst + directory-lijst (Fase 2.6)
- Het Wikidata-item (Fase 2.7)
- Het vakmedia-nieuwsbericht (Fase 2.10)
- LinkedIn-bedrijfspagina-tekst + founder-posts (bestaand in OUTREACH/geo-offsite-plan.md)
- sameAs-update site-breed zodra de profielen live zijn (Fase 2.9)
- Wekelijks nieuws + monitoring (Fase 3)
