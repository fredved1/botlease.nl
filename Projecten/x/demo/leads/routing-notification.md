# Routing-notificatie naar de klant (gekwalificeerde lead) — LOKALE TESTRUN

> **Wat is dit?** Wat **de klant (Bram van Twentse Warmte)** ontvangt zodra een lead boven de drempel scoort. Dit is **stap 6** van PROJECT X: gekwalificeerde leads doorzetten met een **menselijke goedkeuringsgate** (human-in-the-loop) voordat er iets gebeurt.
>
> **Fictief.** Bedrijf, lead en e-mailadressen bestaan niet.
>
> **Routing-target voor deze tenant** = `email` (Twentse Warmte heeft geen CRM). Hieronder twee vormen: (A) de e-mail die Bram krijgt, en (B) dezelfde notificatie als **Microsoft Teams Adaptive Card** (de vorm die we standaard aanbieden als de klant wel Teams gebruikt). Beide bevatten **Accept / Reject**, en in beide geldt: **geen vervolgactie tot een mens akkoord geeft.**

---

## A. E-mail naar de klant (productie: ACS Email of Logic Apps)

**Van:** Twentse Warmte Leads `<leads@mail.twentsewarmte.nl>`
**Aan:** `bram@twentsewarmte.nl`
**Onderwerp:** [Gekwalificeerde lead, score 95] Marleen Brinkhuis — hybride warmtepomp, Almelo
**Verzonden:** 21 juni 2026, 14:37

---

Hoi Bram,

Er is een nieuwe lead binnengekomen via het warmtescan-formulier en die is **gekwalificeerd (score 95 van 100, drempel 60)**.

**Lead**
- Naam: Marleen Brinkhuis
- Adres: Vincent van Goghplein 14, 7606 GT Almelo (binnen servicegebied)
- E-mail: m.brinkhuis@outlook.com
- Telefoon: 06 24 18 77 30
- Binnengekomen: 21 juni 2026, 14:37 via /contact (organisch)

**Situatie**
- Tussenwoning uit 1998, koopwoning
- cv-ketel ~15 jaar oud en haperend
- Wil van het gas af met een **hybride warmtepomp**
- Termijn: **dit najaar, voor de winter**
- Interesse in **ISDE-subsidie** en akkoord met **gratis warmtescan aan huis**

**Waarom gekwalificeerd**
Eigenaar-bewoner (beslissingsbevoegd), binnen servicegebied, oude ketel aan vervanging toe, korte termijn en hoge koopintentie. Past precies op onze USP (wij regelen de subsidie). Volledige scoring in het bijgevoegde `qualification.json`.

**Voorgestelde vervolgactie (gebeurt NIET vanzelf):**
Warmtescan inplannen voor begin/midden najaar en de ISDE-aanvraag voorbereiden.

> **Jij beslist.** De assistent heeft Marleen alleen een bevestiging gestuurd en heeft **geen prijs, geen offerte en geen afspraak** toegezegd. Er gebeurt pas iets als jij hieronder op Accepteren klikt.

**[ ✅ Accepteren — ik bel/plan de warmtescan ]**  → https://leads.twentsewarmte.nl/lead/lead_2026-06-21_tw_0001/accept?token=…
**[ ❌ Afwijzen — past niet ]**  → https://leads.twentsewarmte.nl/lead/lead_2026-06-21_tw_0001/reject?token=…

Bijlage: `qualification.json` (volledige kwalificatie en BANT-mapping)

---

## B. Dezelfde notificatie als Microsoft Teams Adaptive Card (JSON)

> Dit is wat het Teams-kanaal zou tonen als routing-target `teams` was. De **Action.Http**-knoppen roepen een beveiligde Function aan (token in de URL); pas dan zet de pipeline de lead op `accepted` / `rejected`.

```json
{
  "type": "AdaptiveCard",
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.5",
  "body": [
    {
      "type": "Container",
      "style": "good",
      "items": [
        { "type": "TextBlock", "text": "Nieuwe gekwalificeerde lead", "weight": "Bolder", "size": "Large" },
        { "type": "TextBlock", "text": "Score 95/100 (drempel 60) — Twentse Warmte", "isSubtle": true, "spacing": "None" }
      ]
    },
    {
      "type": "FactSet",
      "facts": [
        { "title": "Naam", "value": "Marleen Brinkhuis" },
        { "title": "Plaats", "value": "Almelo (7606 GT) — in servicegebied" },
        { "title": "Vraag", "value": "Hybride warmtepomp + warmtescan + ISDE" },
        { "title": "Woning", "value": "Tussenwoning 1998, koop" },
        { "title": "Ketel", "value": "~15 jaar, haperend" },
        { "title": "Termijn", "value": "Najaar 2026, voor de winter" },
        { "title": "E-mail", "value": "m.brinkhuis@outlook.com" },
        { "title": "Telefoon", "value": "06 24 18 77 30" }
      ]
    },
    {
      "type": "TextBlock",
      "text": "De assistent stuurde alleen een bevestiging. Geen prijs, offerte of afspraak toegezegd. Vervolgactie pas na jouw akkoord.",
      "wrap": true,
      "isSubtle": true
    }
  ],
  "actions": [
    {
      "type": "Action.Http",
      "title": "✅ Accepteren",
      "method": "POST",
      "url": "https://leads.twentsewarmte.nl/api/lead/lead_2026-06-21_tw_0001/accept",
      "headers": [ { "name": "Authorization", "value": "Bearer {{actionToken}}" } ],
      "body": "{\"decision\":\"accept\",\"by\":\"bram@twentsewarmte.nl\"}"
    },
    {
      "type": "Action.Http",
      "title": "❌ Afwijzen",
      "method": "POST",
      "url": "https://leads.twentsewarmte.nl/api/lead/lead_2026-06-21_tw_0001/reject",
      "headers": [ { "name": "Authorization", "value": "Bearer {{actionToken}}" } ],
      "body": "{\"decision\":\"reject\",\"by\":\"bram@twentsewarmte.nl\"}"
    }
  ]
}
```

---

## De human-in-the-loop-afspraak (waarom dit zo werkt)

| Wat | Wie | Wanneer |
|---|---|---|
| Lead afvangen + bevestiging sturen | AI-agent | direct, automatisch |
| Kwalificeren + scoren | AI-agent | direct, automatisch |
| **Beslissen of we de klant benaderen** | **Bram (mens)** | **Accept/Reject vereist vóór elke vervolgactie** |
| Warmtescan plannen, offerte, subsidie | Bram (mens) | pas ná Accept |

De AI doet het saaie voorwerk en zorgt dat Bram alleen warme, complete leads ziet. De AI **doet geen toezeggingen en plant niets** namens Bram. Dat is bewust: het beschermt de relatie met de klant en houdt het AI-Act-risicoprofiel laag (de bot informeert, de mens beslist).

---

## Wat in productie waar draait

| Onderdeel | Productie (Azure) |
|---|---|
| Lead afvangen (form + chat) | Azure Container Apps / Functions endpoint → Cosmos DB (partition = tenantId) |
| Eerste reactie + kwalificatie | Foundry sales/qualify-agent (Azure OpenAI gpt-4o-mini, Data Zone EU) |
| Auto-reply naar lead | Azure Communication Services Email (geverifieerd domein) |
| Drempelcheck + routing | Function / Logic App: `score >= qualify_threshold` → notificatie |
| Notificatie-kanaal | per tenant: e-mail (deze klant), Teams Adaptive Card, of CRM (Dynamics/HubSpot/Pipedrive) |
| Accept/Reject afhandelen | beveiligde Function (token) zet lead-status; pas dan vervolgactie |
| Audit/AVG | consent + AI-disclosure + beslissing gelogd in Cosmos, retentie 730 dagen |

*Gesimuleerde routing-notificatie, lokale PROJECT X-testrun, 2026-06-21. Fictief bedrijf en fictieve lead.*
