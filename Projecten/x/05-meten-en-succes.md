# PROJECT X — Hoe meten we succes? (SEO/GEO + de hele funnel)

> Het stuk dat de pipeline (00-03) compleet maakt: hoe weten we dat het werkt, hoe bewijzen we waarde aan de klant, en waarop stuurt het systeem zichzelf bij.
> Kernlijn (zelfde no-overpromise als BotLease): **we verkopen geen #1-posities, we verkopen gekwalificeerde leads.** Maar we meten de hele keten ervoor, omdat de business-uitkomst maanden achterloopt en de klant eerder voortgang moet zien.

---

## 1. Het principe: een funnel van leading naar lagging

SEO-"succes" is geen los getal (positie) maar een **keten**, waarbij elke stap een vroege indicator is van de volgende. Je meet ze allemaal, want:
- de **lagging** metric (leads/omzet) is wat telt, maar komt pas na maanden;
- de **leading** metrics (indexatie, eerste posities, impressies) bewijzen al in week 1-6 dat het de goede kant op gaat, vóór de eerste lead binnen is. Zonder die vroege signalen denkt de klant in maand 1 dat het niet werkt.

```
Technische gezondheid  ->  Indexatie  ->  Posities  ->  Impressies  ->  Verkeer  ->  Leads  ->  GEKWALIFICEERDE leads  ->  Deals/omzet
   (dag 1, stuurbaar)                                   (GSC: de waarheid)            (ons systeem vangt + kwalificeert)        (north star)
   <----------------------- leading indicators ----------------------->              <------------- lagging / business -------------->
```

**De grote BotLease-les hierin:** zonder Google Search Console-data stuur je blind. Bij BotLease bleek de site #1 te staan op de 2 lease-woorden maar 0 op "huren" — dat zie je alleen op **keyword-niveau met de juiste databron** (een NL-rank-scrape + GSC), niet met een US-zoektool. Meet dus granulair en met de juiste bron.

---

## 2. De meetketen, per stap

| # | Wat | Concrete metric | Databron | Wanneer zichtbaar | Leading indicator van |
|---|-----|-----------------|----------|-------------------|------------------------|
| 1 | **Technische gezondheid** | Core Web Vitals (LCP/CLS/INP), valide schema, sitemap vers, mobiel, 0 crawl-errors | PageSpeed/Crux API, GSC Coverage, eigen checks | Dag 1 | of de basis crawlbaar is |
| 2 | **Indexatie** | # pagina's geindexeerd, % van sitemap, geen "ontdekt-niet-geindexeerd" | GSC + Bing Webmaster API | Dagen-weken | dat content uberhaupt kan ranken |
| 3 | **Posities / zichtbaarheid** | rank per keyword (top 3 / 10 / 30), # keywords in top 10, share-of-voice vs concurrent, featured snippets | DataForSEO (NL, juiste taal/locatie) | Weken-maanden | toekomstig verkeer |
| 4 | **Bereik (de waarheid van Google)** | impressies, gemiddelde positie, CTR per query/pagina, branded vs non-branded | **GSC Performance API** (+ Bing) | Weken | klikken/verkeer; ook waar CTR achterblijft (title/meta fixen) |
| 5 | **Verkeer** | organische sessies, per landingspagina, engaged sessions, nieuw vs terugkerend | Analytics (privacy-vriendelijk, bv. server-side/Umami-stijl) | Weken-maanden | conversiekansen |
| 6 | **Conversie (business-KPI)** | organische leads (form + chat), **gekwalificeerde leads**, lead-kwaliteit (BANT-score), conversieratio bezoek->lead | **Ons eigen systeem** (lead-DB in Cosmos) | Maanden | omzet |
| 7 | **Deals/omzet** | deals + omzet toegeschreven aan organisch, cost-per-qualified-lead | Klant-CRM (Dynamics/HubSpot) terugkoppeling | Maanden-kwartalen | de echte ROI |

---

## 3. De GEO-dimensie (parallel, apart meten)

GEO (geciteerd worden door ChatGPT/Perplexity/Gemini) is **geen stuurbare ranking** en heeft eigen meetmethodes:
- **Citatie-/mention-tracking:** periodiek (bv. wekelijks) een vaste set relevante prompts per engine draaien en loggen of het klant-bedrijf wordt genoemd/gelinkt. Handmatig of via DataForSEO AI Optimization API (betaalde add-on).
- **AI-referral-verkeer:** in analytics filteren op referrals van `chatgpt.com`, `perplexity.ai`, `gemini.google.com` etc. Groeiend kanaal, maar vaak ondergerapporteerd (niet alle AI-tools zetten een referrer).
- **Aanwezigheid in de bron-laag:** staat het bedrijf in de feitenbronnen waar AI uit put (eigen llms.txt + schema + Wikidata + relevante listicles/directories)?
- **Eerlijk naar de klant:** "we maximaliseren de citatiekans en meten per engine", geen gegarandeerde positie.

---

## 4. Project X's unieke voordeel: we bezitten de hele funnel

De meeste SEO-tools stoppen bij verkeer. **Project X vangt en kwalificeert de lead zelf**, dus we kunnen de keten doortrekken tot waar het de klant echt om gaat:
- **Cost-per-qualified-lead uit organisch** (de heilige graal voor een MKB-klant).
- **SEO-/GEO-toegeschreven pipeline** (welke landingspagina/zoekwoord leverde welke gekwalificeerde lead).
- Eén verhaal van **impressie tot gekwalificeerde lead in één systeem**, geen losse tools aan elkaar knopen.

Dat is meteen het sterkste verkoop- en retentie-argument: we rapporteren niet "we staan #3 op keyword X", maar "organisch leverde deze maand N gekwalificeerde leads tegen kosten Y".

---

## 5. Baseline + doelen (per klant, eerlijk gefaseerd)

- **Baseline bij onboarding vastleggen** (vaak bijna nul bij een nieuwe site): huidige posities, indexatie, verkeer, leads. Zonder nulmeting is voortgang niet aantoonbaar.
- **Eén north-star per klant** (meestal: gekwalificeerde leads/maand uit organisch) + een handvol leading-KPI's eronder. Niet 30 metrics; de klant wil 1 getal dat ertoe doet.
- **Realistische tijdlijn** (zelfde eerlijkheid als BotLease):
  - **Maand 1-2:** techniek 100%, geindexeerd, baseline gezet, eerste long-tail-posities verschijnen.
  - **Maand 2-4:** keywords komen top 10-30 binnen, impressies stijgen, eerste organische leads.
  - **Maand 4-9:** kernkeywords ranken, gestage stroom gekwalificeerde leads, eerste GEO-citaties.
- **Definieer "succes" vooraf samen met de klant** als een doel op de north-star (bv. "X gekwalificeerde leads/maand binnen 6 maanden"), niet als een keyword-positie.

---

## 6. Het meet-/rapportage-component (hoort in de architectuur)

Dit is een ontbrekend onderdeel dat aan 02-architecture.md toegevoegd moet worden:
- **Een wekelijkse/maandelijkse "report"-Function** (Azure Functions timer) die per tenant trekt: GSC + Bing Performance API, DataForSEO rank-data, analytics, en de eigen lead-DB (Cosmos). Schrijft een snapshot weg (zoals BotLease `seo_data.json`, maar per tenant) zodat je historie en trends hebt.
- **Een per-klant dashboard / automatisch maandrapport** (de tastbare waarde-leverancier richting de klant): north-star + de funnel + top-bewegers + de gekwalificeerde leads van die maand.
- **Alerts (harde BotLease-les: stille uitval):** waarschuw bij "indexatie gedaald", "0 gepubliceerd", "ranking-drop > X", "feitcheck-FAIL". Een systeem dat stilvalt zonder melding is erger dan geen systeem.
- **Self-optimization-haakje:** de rank-/CTR-data voedt terug in de pipeline (lage CTR -> title/meta herschrijven; pagina blijft hangen op pos 11-20 -> content verdiepen/intern linken). Begin handmatig (mens kijkt naar het rapport), automatiseer pas als het patroon bewezen is.

---

## 7. Eerlijke caveats (vooraf met de klant bespreken)

- **Attributie is nooit perfect:** multi-touch (iemand vindt je via Google, komt later direct terug), branded vs non-branded splitsen, en GEO-referrals worden vaak niet getagd. Rapporteer in **ranges en trends**, niet in schijnprecisie.
- **Seizoen + concurrentie + Google-updates** bewegen mee; vergelijk year-over-year waar mogelijk en duid context.
- **SEO/GEO is weken tot maanden**, geen knop. Daarom de leading indicators vooraan, zodat voortgang vroeg zichtbaar is.
- **Geen vanity-rapportage:** "1.000 impressies" zonder leads is geen succes. De keten moet doorlopen tot de north-star.

---

## 8. De concrete KPI-set (het dashboard, kort)

**North star:** gekwalificeerde leads/maand uit organisch + cost-per-qualified-lead.

**Leading (wekelijks):** % sitemap geindexeerd · # keywords top 10 · impressies (GSC) · gemiddelde CTR · organische sessies · AI-citaties (set prompts) · technische gezondheid (CWV/schema/0 errors).

**Lagging (maandelijks):** organische leads · gekwalificeerde leads · conversieratio bezoek->lead · (via klant-CRM) deals + omzet uit organisch.

**Guardrails / alerts:** indexatie-daling · ranking-drop · 0 gepubliceerd · feitcheck-FAIL · spam-spike op het lead-formulier.
