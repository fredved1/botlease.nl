# 03 — Pipeline: leveranciers + klanten

> De live-bron is het CRM (`https://crm.botlease.nl`). Dit bestand is het verhaal eromheen: wie, status, op wie wachten we. Bijwerken bij elke statuswijziging.

## 🛒 Klanten / leads

| Wie | Wat | Status | Bal ligt bij | Volgende stap |
|---|---|---|---|---|
| **VR Expert — Dante Spekman** ⭐ | Een van de grootste XR-verhuurders EU; wil humanoid-verhuur verkennen (events/beurzen). Bestelde G1 Edu ×1. | In gesprek | **Ons** (na Dario) | Wacht op Dario's compliance-antwoorden → dan marge doorrekenen + complete mail (leaseprijs + compliance). ⚠️ **Strategie (Dante = klant die concurrent kan worden):** hij is zelf verhuurder, dus de stap klant→concurrent is klein. Zijn compliance-vragen zijn normaal due-diligence, geen bewijs van overnameplan, maar: **antwoord open over het wát/hóé van veiligheid, gesloten over de inkoopketen.** Nooit inkoopbron/-prijs/marge noemen, geen kale unit zonder operator, geen "testunit om mee te spelen", geen exclusiviteit, niets voorschieten. Verkoop de ontzorgde inzet, niet "een G1". Vroege alarmsignalen: vragen verschuiven naar "welke distributeur", "inkoopprijs", "kaal huren zonder begeleiding". Volledige analyse in businessplan §9A. |
| **Atlas Copco — Thomas Christiaensen** | Humanoid-taskforce (BE, industrie). Verkennend. | Hold | Ons | 1-pager klaar (`OUTREACH/send-atlas-onepager.html`); sturen wanneer leverancierslijn rond is |
| **BusinessWise — Tim Swager** (via DPG Media) | Event **16 juli 16:00-17:00**, entree-ontvangst met humanoid. Tel 06-21971403. | Beantwoord 7/7 (prijzen + vragen, #39) | **Ons** | ⚠️ **Beloofd: uiterlijk do 9/7 uitsluitsel beschikbaarheid.** Wij hebben geen units → kan alleen via partner (Dario/Damien/Jordi gepolst 7/7). Locatie nog onbekend. **Thomas: bellen versnelt.** |
| **Van de Beek Advies — Bart** | Event **30 sept** (Agri & Food-kennissessie), 1+ humanoids, korte periode; plus **roadshow-idee** langs groene onderwijsinstellingen | Beantwoord 7/7 (dagtarieven + 3 vragen, #40) | hen | Wacht op locatie/dagdeel, aantal robots, roadshow-omvang. 30/9 haalbaar via order (Unitree 4-5wk, order uiterlijk half aug ná getekende klant) of partner. Roadshow = potentieel structurele omzet. |
| **Kiwa — Erik Steegman** | Event **11 nov 2026, Expo Houten**; R1 of G1, wil uitleg verschillen + beeldmateriaal | Aanvraag 8/7, concept klaar (#46, Lisa) | **Thomas** (versturen) | Concept in werklijst: R1 vs G1 uitleg, dag- en dagdeeltarieven, links naar robotpagina's, 3 vragen (dag/dagdeel, rol, welke beurs). Ruim haalbaar, ook met eigen unit. Kiwa = grote TIC-organisatie, potentieel terugkerende klant. |

## 🏭 Leveranciers (inkoop)

| Leverancier | Contact | Status | Op wie wachten | Notitie |
|---|---|---|---|---|
| **Unitree (China)** | Zoe Wang (sales_www@unitree.com) + Wanda (WhatsApp) | ✅ **Offerte ontvangen** (16/6, aangevuld 2/7) | **Ons** | **G1 EDU U1 $28.900, U2 $36.900 + $1.500 shipping** (CPT, 100% vooruit, 4-5wk). **NIEUW 2/7: R1 $6.200 + stand $250 + shipping $900 = $7.350** (≈€6.800 landed) + TÜV-cert RED art. 3.3(d)/(e) cyber+privacy (bestandsnaam zei "2023:1230" maar het is RED; **Machineverordening-DoC ontbreekt nog** → bij volgende mail opnieuw vragen). Next: order bevestigen → Zoe maakt PI. Pas bestellen ná getekende klant. Detail: `docs/leveranciers/unitree-offerte-2026-06-16.md` |
| **Synergy Tech (Unitree ES)** ⭐ | Dario Samaniego, CEO (dario.samaniego@synergytech.es) + Miriam Muñoz (docs) | ✅ **Alles beantwoord** (25/6) | **Dario** | **Front-runner inkooplijn.** Beantwoordde alle compliance-vragen (CE + deelbaar conformiteitspakket, volledig offline/on-prem met hun eigen lokale AI ARGOS, firmware onder onze controle, AI Act). Turnkey-gat gedicht: kant-en-klare demo-apps (ARGOS) als add-on. **Biedt distributeur-pad met speciale kortingsprijs.** Wil config+volume bevestigd → maakt dan partnervoorstel. Reply 29/6 (#35): distributeurprijs + voorwaarden + ARGOS-prijs op papier gevraagd. **Nudge 7/7 (#42)**: + eventinzet-tarief (G1+ARGOS+operator of korte huur aan ons) + levertijd NL bij order in augustus (event-ready 30/9?). |
| **RobotShop EU** | Nathy (marketplace@robotshop.com, ticket T1121128) | ✅ Offerte + vragen beantwoord (25/6) | **Ons** | **U1 €29.925, U2 €34.200** (5% korting, ex btw, EU, 18mnd garantie, t/m 30 juli). Antwoord 25/6: **8% vanaf 3 units**, **45 dagen geldig**, en **geen reseller op Unitree** (mag niet van fabrikant, enkel volumekorting, case-by-case). Transactionele EU-fallback. Geen actie tenzij we bestellen. PDF in docs/leveranciers/ |
| **PAL Robotics** | Alexandre Saldes (alexandre.sb@pal-robotics.com) | Partner-pad | **Thomas** | **Distributor RFI ontvangen 26/6** (aan thomas@): 4 pagina's (administratief, HR, jaarcijfers 3 jr, bedrijfsprofiel, support-capaciteit, landen). PDF + **concept-antwoorden klaar**: `docs/leveranciers/pal-distributor-rfi-2026-06-26.pdf` + `pal-rfi-concept-antwoorden-2026-07.md`. Lijn: eerlijk over 2026-start, referral/agent-model (~10%, NDSM) als startspoor, geen leveranciersnamen delen. **Thomas vult gaten in + verstuurt ZELF** (harde regel: Claude retourneert nooit formulieren). Echte prijzen: TIAGo ~€110k → niet voor deal 1. ⚠️ Niet op de site terugzetten |
| **NEURA Robotics (DE)** | Kristina Naumoska | ❌ **Afgesloten (2/7)** | — | Kristina sloot netjes af: geen reseller/distributie/lease, uitnodiging om in **2027** terug te komen (dan mogelijk ander commercieel model). Geen actie. |
| **INGEN (FR)** | Damien Blanc (damien.blanc@ingen-geosciences.com) | ✅ **Offerte gevraagd (7/7)** | **hen** | Franse Unitree-reseller. Damien vroeg 29/6+2/7 welke G1-versie/aantallen (wachtte op óns!). **Beantwoord 7/7 (#41)**: U1+U2-offerte NL, 1 unit nu + prijsindicatie bij 3, partnerprijs Go2 Pro (publiek €3.250 ex btw), + eventinzet-vraag (unit+operator voor 16/7 en 30/9). Prio omhoog: derde EU-prijslijn naast Dario/RobotShop. |
| **RoboCorpus (BE)** | Jordi Hurssel (+ collega Hamza) | In gesprek | hen | Reply 17/6 (NL): context + reseller-voorwaarden. **Nudge 7/7 (#43)**: eventinzet op partnerbasis (G1+operator, 16/7 en 30/9, dagtarief voor ons) + reseller-voorwaarden herhaald. Wilden Teams; basics eerst op papier |
| **UBTECH** | Sean Qin | In gesprek | hen | Opent directe lijn (18/6). Reply gestuurd: Walker S2 reseller-prijs (1+3 stuks) gevraagd |
| **Pollen Robotics (FR)** | Santiago Pavon | Beantwoord | Pollen | Reachy 2-verduidelijking gestuurd |
| Overige follow-ups | 1X, Terra, Generation Robots, QUADRUPED, Leobotics, OrcaRobot | Gemaild | hen | Geen reactie; laten rusten |

## ✅ Verstuurd 7 juli (alles vanaf hallo@, geen orders toegezegd, geen klantnamen naar leveranciers)
- **Tim Swager / BusinessWise** (#39): dagtarieven (R1 €750 / G1 €1.450 incl. operator, excl. btw), locatie + invulling gevraagd, uitsluitsel beschikbaarheid uiterlijk 9/7 beloofd, belaanbod gedaan.
- **Bart / Van de Beek** (#40): dagverhuur-uitleg (korte periode kan juist), tarieven + 30% vanaf dag 2, roadshow-interesse uitgesproken, 3 vragen gesteld.
- **Damien / INGEN** (#41): U1+U2-offerte gevraagd (NL levering), 1 unit + indicatie bij 3, partnerprijs Go2 Pro, eventinzet-vraag.
- **Dario / Synergy** (#42): nudge distributeurprijs/ARGOS + eventinzet-tarief + levertijd bij augustus-order.
- **Jordi / RoboCorpus** (#43): eventinzet op partnerbasis (16/7 en 30/9) + dagtarief + reseller-voorwaarden herhaald.

## ✅ Verstuurd 29 juni (alles vanaf hallo@botlease.nl, in de juiste thread, geen beloftes/order)
- **Dario / Synergy** (#35): distributeurprijs + voorwaarden + ARGOS-add-on-prijs op papier gevraagd, GEEN order/volume toegezegd. Bal ligt bij Dario.
- **NEURA / Kristina** (#36): beleefd geparkeerd, ons model is lease/verhuur (geen co-development via NEURA Gym); deur open voor later.
- **RobotShop / Nathy** (#37): begrip bevestigd (geen reseller op Unitree, 8% vanaf 3 units, 45 dgn geldig); geen order toegezegd.
- **INGEN / Damien** (#38): reseller-prijs per mail opgevraagd (G1 EDU + Go2 Pro + voorwaarden) i.p.v. bellen; geen order.

PAL: niets gestuurd, distributeur-formulier geparkeerd (duur + juridisch gevoelig, niet voor deal 1).

## ✅ Verstuurd 24 juni
- **NEURA / Kristina** (#31): ons model verhelderd + partner-track/partnerprijs 4NE-1 gevraagd. → beantwoord 26/6 (geen reseller, willen tech-partner).
- **RobotShop / Nathy** (#32): volumedrempel + geldigheid + reseller-tegenstrijdigheid uitgevraagd. → beantwoord 25/6 (8%@3+, 45 dgn, geen reseller).
- **Dario / Synergy** (#34): nudge op stilgevallen compliance-antwoorden. → beantwoord 25/6 (alles + distributeur-aanbod).

## ⏸️ ON HOLD (niet versturen)
- **VR Expert / Dante** (#33): concept klaar en promise-vrij (event-forward, geen prijs/SLA, acrobatiek-grap eruit), maar **Thomas wil nog GEEN contact**. Eerst blokkerende basis (papieren/financier) + concurrent-klant-strategie scherp. Niet versturen tot Thomas het zegt.
(eerdere ronde 17-18 juni allemaal verstuurd: RobotShop-versie, RoboCorpus, UBTECH-direct, Zoe-offerte-bedankje, UBTECH-Walker-S2, Nathy-offerte-bevestiging)

## 💡 Strategie bij inkoop
Twee prijzen verzamelen (Unitree China via Zoe + EU via Dario/RobotShop), dan de beste route kiezen voor de eerste deal. **Regel: nooit een unit kopen zonder ≥€5k vooruitbetaald of getekend contract.** Lease-financiering loopt via Marinho (zie `04-team.md`), niet eigen spaargeld.

## Wat is "jij krijgt de leads" (correctie)
In de eerste follow-up stond bij de demo-unit-vraag "you get the exposure and the leads" — dat was alléén de ruil voor een **gratis demo-/consignment-unit**, niet het businessmodel. Het echte model = **wij kopen in tegen reseller-prijs, wij bezitten de klant.** Voortaan die leads-framing weglaten.
