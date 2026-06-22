# PROJECT X — Intakeformulier

> Voor Tijmen / de klant. Vul in wat je weet; "weet ik niet" mag ook, dan zoeken we het samen uit.
> ⛔ = **blocker**: zonder dit kunnen we de MVP niet opleveren. De rest mag later.
> Bij veel vragen staat een **aanrader** voor-ingevuld; je hoeft die dan alleen te bevestigen of aan te passen.
> Achtergrond per vraag (het "waarom") staat in `01-client-intake.md`.

**Klant:** ______________________  **Ingevuld door:** ______________  **Datum:** __________

---

## A. De 3 vragen die alles bepalen (eerst deze) ⛔

**A1. Waar draait het?**
- [ ] In de **eigen Azure-tenant** van de klant (data blijft 100% bij hem; wij beheren op afstand) ← *aanrader / waarschijnlijk de eis*
- [ ] In een **door ons beheerde Azure-omgeving** (EU) — goedkoper, minder isolatie
- [ ] Weet ik niet

**A2. Hoe hard is de EU-data-eis?**
- [ ] **EU-only inference** (alle AI-verwerking gegarandeerd in EU; modelkeuze dan GPT-4o/4.1) ← *aanrader voor NL-klant*
- [ ] Alleen **data-opslag in EU** is genoeg (ruimere modelkeuze)
- [ ] Weet ik niet

**A3. Contracttype bij Microsoft?** (bepaalt of we "AI bewaart niets" mogen beloven)
- [ ] Enterprise Agreement (EA) / Microsoft Customer Agreement (MCA)
- [ ] Gewone pay-as-you-go
- [ ] Weet ik niet

---

## B. Het bedrijf ⛔

- **B1. Bedrijfsnaam (officieel + handelsnaam):** _______________________________
- **B2. KvK-nummer:** _____________  **Vestigingsplaats + land:** _______________
- **B3. Wat doet het bedrijf? (2-3 zinnen, eigen woorden):**
  _____________________________________________________________________
  _____________________________________________________________________
- **B4. Bestaande website (indien er een is):** _______________________________
- B5. LinkedIn / andere profielen: _________________________________________

## C. Branche, doelgroep & diensten ⛔

- **C1. Branche/sector:** ___________________________________________________
- **C2. Ideale klant/doelgroep:** ___________________________________________
- **C3. Top diensten/producten om te promoten (max 5):**
  1. ______________________  2. ______________________  3. ______________________
  4. ______________________  5. ______________________
- **C4. Regio/markt:** ☐ NL  ☐ NL+BE  ☐ NL+BE+DE  ☐ anders: __________
- **C5. Talen voor site + content:** ☐ NL  ☐ NL+EN  ☐ anders: __________
- C6. 3-5 belangrijkste concurrenten (URL's): ________________________________

## D. Merk & huisstijl ⛔ (dit voedt direct de site-generator)

- **D1. Logo aanleveren** (SVG bij voorkeur, anders PNG): ☐ meegestuurd  ☐ volgt
- **D2. Merkkleuren (hex):** accent `#_______`  tekst `#_______`  achtergrond `#_______`
  *(weet je de hex niet? Stuur het logo, dan leiden wij ze af.)*
- **D3. Toon:** ☐ formeel (u)  ☐ informeel (jij)   Voorbeeldzin die "klinkt als jullie": __________________
- D4. Beeld: ☐ wij genereren AI-hero-beelden  ☐ klant levert eigen/stockfoto's
- D5. Bestaande juridische teksten (privacy/AV)? ☐ ja, aanleveren  ☐ nee, wij maken een basis

## E. Domein & DNS ⛔

- **E1.** ☐ Bestaand domein: ____________________  ☐ Wij zoeken/registreren een nieuw domein
- **E2. Bij nieuw:** gewenste TLD's (☐ .nl ☐ .com ☐ .be) + naam-ideeën: __________________
- **E3. Wie wordt eigenaar van het domein?** ☐ klant  ☐ bureau
- **E4. Wie kan DNS-records aanpassen** (nodig voor mail + site)? Naam/rol: ______________

## F. De zichtbare auteur ⛔ (grootste SEO/GEO-hefboom)

Eén echte persoon bij de klant onder wiens naam de content verschijnt (geen "AI" of "de redactie").
- **F1. Naam:** _______________________  **Functie:** _______________________
- **F2. Korte bio (2-3 zinnen) + foto:** ☐ aangeleverd  ☐ volgt
- F3. LinkedIn-profiel van die persoon: ____________________________________

## G. SEO & GEO

- **G1. Belangrijkste zoektermen waarop gevonden worden (5-15):**
  _____________________________________________________________________
- G2. AI-citatie (ChatGPT/Perplexity) gewenst? ☐ ja, als onderdeel  ☐ later/add-on  *(eerlijk: we maximaliseren de kans, geen garantie)*
- G3. Al een Google Search Console / Bing Webmaster? ☐ ja  ☐ nee  ☐ weet ik niet
- G4. Mogen we een Wikidata-vermelding aanmaken? ☐ ja  ☐ nee

## H. Content / blog

- **H1. Type:** ☐ evergreen blogs (aanrader voor de meeste bedrijven)  ☐ nieuws/actualiteit  ☐ beide
- H2. Relevante onderwerpen/feeds: __________________________________________
- H3. Cadans: ☐ 1/week (aanrader bij start)  ☐ 2-3/week  ☐ anders: ______
- **H4. Goedkeuring vóór publicatie?** ☐ ja, mens kijkt mee (aanrader bij start)  ☐ nee, automatisch
- H5. Publiceren naar: ☐ nieuwe site (door ons)  ☐ bestaand CMS (welke?): __________

## I. Leads ⛔ (afvangen → beantwoorden → kwalificeren → doorzetten)

- **I1. Kanalen:** ☐ contactformulier  ☐ AI-chat  ☐ beide (aanrader)
- **I2. Chatbot:** ☐ mag autonoom antwoorden  ☐ mens-in-de-lus (aanrader) — geen bindende offerte zonder mens
- **I3. Kwalificatie-criteria:** ☐ BANT (Budget/Authority/Need/Timeline)  ☐ branche-specifiek, namelijk: __________
- **I4. Waar gaat een gekwalificeerde lead heen?** ☐ e-mail naar: __________  ☐ Microsoft Teams  ☐ CRM (welke?): __________
- I5. Afzender-e-mailadres voor automatische mails (op het klant-domein): __________________

## J. Bestaande systemen

- J1. CRM? ☐ Dynamics 365  ☐ HubSpot  ☐ Pipedrive  ☐ anders: ______  ☐ geen
- J2. Gebruikt de klant Microsoft Teams? ☐ ja  ☐ nee
- J3. Andere systemen die een lead moet bereiken: ___________________________

## K. Azure-toegang ⛔ (alleen bij model A — eigen tenant)

- **K1. Subscription-ID + Tenant-ID:** _______________________________________
- **K2. Verplichte regio:** ☐ West Europe (NL/Amsterdam)  ☐ North Europe (Ierland)  ☐ geen voorkeur
- **K3. Wie heeft Owner / User Access Administrator** (om rechten toe te kennen)? __________________
- **K4. Mogen wij beheertoegang** via Azure Lighthouse (least-privilege)? ☐ ja  ☐ nee  ☐ bespreken
- K5. Private networking (VNet) een eis? ☐ ja  ☐ nee/nice-to-have

## L. Compliance ⛔

- **L1. Verwerkersovereenkomst** tussen bureau en klant: ☐ akkoord, wij leveren template  ☐ klant heeft eigen template
- **L2. AI-disclosure in de chat** ("je praat met een AI-assistent") + consent-logging: ☐ akkoord *(wettelijk verplicht, niet uitschakelbaar)*
- L3. "AI bewaart niets" (ZDR) gewenst? ☐ ja (vereist EA/MCA, zie A3)  ☐ niet nodig
- L4. Bewaartermijn leads: ☐ standaard (max ~2 jaar)  ☐ anders: __________

## M. Commercieel (intern — niet per se met klant delen)

- M1. Budget-plafond per maand: __________
- M2. Prijsmodel: ☐ setup-fee + maandelijkse fee (klant betaalt Azure zelf)  ☐ all-in SaaS-prijs
- M3. Verwacht aantal klanten jaar 1: __________

---

### De minimale "go"-lijst (hieruit kunnen we Fase 1 starten)
A1-A3 · B1-B4 · C1-C5 · D1-D3 · E1/E3/E4 · F1 · I1-I4 · K1-K3 · L1-L2.
De `[later]`-items mogen na de start. Zodra de ⛔-velden ingevuld zijn, kunnen wij de eerste klant-MVP bouwen.

> Onzekerheden die we eerlijk vooraf melden: Azure/Foundry-prijzen veranderen per kwartaal (we verifiëren vóór de offerte); de nieuwste GPT-5-modellen zijn bij een harde EU-eis nog niet beschikbaar (dan GPT-4o/4.1); AI-citatie is een kans, geen gegarandeerde positie.
