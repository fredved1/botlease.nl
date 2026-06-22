# Automatische eerste e-mailreactie (auto-reply) — LOKALE TESTRUN

> **Wat is dit?** De **automatische eerste e-mail** die de lead (Marleen) direct na haar warmtescan-aanvraag ontvangt. Onderdeel van **stap 5** van PROJECT X.
>
> **Fictief.** Testbedrijf en ontvanger bestaan niet.
>
> **In productie** wordt deze mail verstuurd via **Azure Communication Services (ACS) Email** vanaf het per-tenant geverifieerde domein `mail.twentsewarmte.nl` (SPF/DKIM/DMARC ingesteld, anders spam). De tekst wordt door de Foundry-agent gepersonaliseerd op de naam + situatie van de lead. **Vriendelijk, menselijk, geen overpromise** (humanizer-regel, geen lange streepjes).

---

**Van:** Twentse Warmte `<warmtescan@mail.twentsewarmte.nl>`
**Aan:** Marleen Brinkhuis `<m.brinkhuis@outlook.com>`
**Antwoorden naar:** `bram@twentsewarmte.nl`
**Onderwerp:** Je warmtescan-aanvraag is binnen, Marleen
**Verzonden:** 21 juni 2026, 14:37 (automatisch)

---

Hoi Marleen,

Bedankt voor je aanvraag bij Twentse Warmte. Je gratis warmtescan staat genoteerd, en ik vat even kort samen wat ik van je begreep zodat we niets missen:

- Een tussenwoning uit 1998 (koop) in Almelo
- Een cv-ketel van ongeveer 15 jaar oud die begint te haperen
- Interesse in een hybride warmtepomp, het liefst nog dit najaar geregeld
- Je wilt weten wat de ISDE-subsidie oplevert, en die regelen wij voor je mee

**Wat er nu gebeurt:** Bram, onze eigenaar en hoofdmonteur, neemt binnen twee werkdagen persoonlijk contact met je op om de gratis warmtescan in te plannen. Tijdens die scan kijkt hij bij je thuis naar je woning, je radiatoren en je warmtevraag. Pas daarna krijg je een eerlijke offerte met een reële prijs. Dat doen we bewust zo, want een prijs zonder de woning te zien zou een slag in de lucht zijn.

Een paar dingen die je alvast kunt lezen terwijl je op Bram wacht:

- Wat een hybride warmtepomp ongeveer kost en wanneer het loont: https://twentsewarmte.nl/hybride-warmtepomp
- Hoe de ISDE-subsidie in 2026 werkt en wat je terugkrijgt: https://twentsewarmte.nl/blog/isde-subsidie-warmtepomp-2026

Heb je tussendoor een vraag of verandert er iets? Beantwoord deze mail gerust, dan leest Bram met je mee.

Hartelijke groet,
Het team van Twentse Warmte
Warm wonen in Twente, zonder gedoe.

---

*Deze eerste reactie is automatisch opgesteld door onze digitale assistent. De warmtescan en je offerte worden persoonlijk door Bram (een mens) geregeld. Wil je dat we je gegevens verwijderen? Mail dit dan en we doen dat. Privacybeleid: https://twentsewarmte.nl/privacy*

---

## Productienoot

| Aspect | Productie (Azure) |
|---|---|
| Verzendkanaal | Azure Communication Services Email, sender `mail.twentsewarmte.nl` |
| Domeinverificatie | SPF + DKIM + DMARC verplicht in tenant-deploy, anders spam |
| Personalisatie | Foundry-agent vult naam + samenvatting; vaste, getoetste template eromheen |
| AI-transparantie | Voettekst meldt dat de eerste reactie door de assistent is opgesteld (AI Act) |
| Geen overpromise | Geen genoemd bedrag, geen "binnen 24u", geen harde belofte over levertijd |
| Anti-misbruik | Auto-reply alleen ná Turnstile + honeypot + rate-limit (kosten/mail-bomb-bescherming) |
| Kosten | ~ $0,00025 per e-mail (ACS) |

*Gesimuleerde auto-reply, lokale PROJECT X-testrun, 2026-06-21.*
