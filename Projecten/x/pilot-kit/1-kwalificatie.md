# Project X — Fase 1: Kwalificatie (kort)

> Het korte instap-deel. Async in te vullen of in 2 minuten samen door te lopen aan het begin van een gesprek.
> Doel: kwalificeren vóór we tijd investeren in een scoping-call, voorstel en SOW. 70% van enterprise-deals stalt door slechte kwalificatie aan de voorkant; deze 7 vragen vangen dat af.
>
> Onderdeel van het gefaseerde intake-proces (zie `../06-intake-aanpak.md`):
> **Fase 1 kwalificatie (dit) → Fase 2 scoping-call → Fase 3 voorstel + SOW + verwerkersovereenkomst → Fase 4 tekening + aanbetaling → Fase 5 kickoff + diepe intake.**

**Belangrijk vooraf (trust-cue, zo ook tonen in het form):** dit deel vraagt NOOIT wachtwoorden, API-keys of Azure-IDs. Die regelen we later veilig out-of-band via Azure Key Vault / Lighthouse. Hier verzamelen we alleen wat nodig is om te bepalen of dit een goede match is.

---

## De vragen (5-8, ±2 min)

| # | Vraag | Waarom we het vragen |
|---|---|---|
| 1 | **Bedrijfsnaam + jouw naam, functie en e-mail.** | Identiteit van de aanvraag en wie ons aanspreekpunt is. Meteen zichtbaar of we met de juiste persoon aan tafel zitten. |
| 2 | **In welke branche/sector zit het bedrijf, en wat is in 1 zin jullie belangrijkste dienst of product?** | Stuurt de eerste inschatting van de niche en het content-/keyword-werk. Signaleert ook of het een YMYL-sector is (finance/zorg), waar menselijke eindcontrole op content verplicht is en de scope groter wordt. |
| 3 | **Moet alles draaien in jullie EIGEN Azure-tenant/subscription, of mag het in een door ons beheerde Azure-omgeving (EU) draaien?** (eigen Azure: ja / nee / weet ik niet) | Dit is de splitsing tussen twee totaal verschillende architecturen en kostenstructuren (klant-tenant via Managed Application vs. onze beheerde EU-omgeving). Het bepaalt ook wie de Azure-rekening draagt. Onze niche is juist "alles in jullie eigen EU-Azure", dus dit is de kernvraag. |
| 4 | **Hoe hard is de EU-eis voor jullie data?** (a) data mag in de EU staan, verder geen harde eis · (b) ook de AI-verwerking moet EU-only blijven · (c) weet ik nog niet | Grove peiling van de #1 valkuil. EU-only-verwerking vraagt een specifieke Azure-opzet (Data Zone EU) en beperkt de modelkeuze: de nieuwste GPT-5.x is medio 2026 nog niet als EU-data-zone beschikbaar, dus bij een harde EU-eis werken we met GPT-4o / GPT-4.1. Hier alleen grof peilen; we werken het hard uit in de scoping-call. |
| 5 | **Wat is de tijdlijn/urgentie?** (live binnen ~1 maand · binnen 1-3 maanden · oriënterend, geen vaste datum) | Bepaalt of dit een echte pilot-kans is of een verkenning. Houdt ons eerlijk over wat haalbaar is: een Azure-tenant provisionen, domein/DNS en mail-verificatie inrichten kost doorlooptijd. |
| 6 | **Budget-indicatie.** Denk aan een eenmalige setup-fee plus een maandelijkse beheer/AI-fee (bij eigen Azure draag je het Azure-verbruik zelf). Past dat ongeveer bij wat jullie in gedachten hadden? (ja / globaal welk niveau / nog geen idee) | Filtert vroeg op betaalbaarheid. We hoeven geen exact bedrag (dat hoort in het voorstel), wel of de orde van grootte past. Voorkomt dat we een volledig voorstel maken voor een budget dat er niet is. Let op: vaste Azure-bodemkosten (zoals AI Search en Cosmos) lopen 24/7 door, ook zonder verkeer; dat verwerken we in de fee. |
| 7 | **Wie neemt de beslissing en wie is intern de trekker (champion)?** Is dat dezelfde persoon, of zit er een budgethouder boven? | We willen weten of onze gesprekspartner kan beslissen of intern moet pitchen. Bepaalt of een aanvullende stakeholder bij de scoping-call moet. Voor de pilot loopt de lijn via Tijmen (IT Connect); goed om expliciet te maken wie aan klantzijde tekent. |

> Optioneel 8e veld (alleen als het natuurlijk past): **bestaande website-URL** — handig om alvast een grove inschatting van niche en huidige positie te maken. Geen blocker voor kwalificatie.

---

## Ga / no-go-check

Markeer per vraag: harde eis · voorkeur · weet ik niet. Daarna onderstaande check.

**GA (gekwalificeerde pilot-kans) wanneer in grote lijnen geldt:**
- **Hosting (vraag 3):** eigen Azure = "ja" of "kan in EU-beheerde omgeving". Dit is onze sweet spot. "Weet ik niet" mag, mits er iemand technisch (zoals Tijmen) bij de scoping-call kan aanschuiven om het te bepalen.
- **EU-eis (vraag 4):** helder of werkbaar. Zelfs een harde EU-only-eis is GA, zolang de klant accepteert dat we dan met GPT-4o / GPT-4.1 werken (geen GPT-5.x in EU-data-zone medio 2026). We beloven nooit een EU-garantie die we niet kunnen verifiëren.
- **Tijdlijn (vraag 5):** concreet (binnen ~3 maanden) of een duidelijke aanleiding. Een echte datum/urgentie tilt het boven "ooit eens".
- **Budget (vraag 6):** orde van grootte past bij setup-fee + maandelijkse fee (plus eigen Azure-verbruik bij model A). Geen exact bedrag nodig, wel "ja, dat niveau kan".
- **Beslisser (vraag 7):** beslisser bekend en bereikbaar, of een champion die intern echt kan trekken en ons bij de juiste persoon brengt.

**NO-GO / eerst uitzoeken bij:**
- Eist alles strikt buiten Azure / op eigen on-prem hardware → valt buiten onze Azure-native propositie.
- Harde EU-only-eis **plus** de eis om per se het allernieuwste model (GPT-5.x) te draaien → medio 2026 niet samen mogelijk; eerst verwachtingen bijstellen.
- "Wil het gisteren live" zonder ruimte voor tenant-provisioning, DNS/mail-verificatie en tekening + aanbetaling → onrealistisch, herkaderen of laten lopen.
- Budget ver onder een eenmalige setup-fee + maandfee → niet kostendekkend, beleefd afhouden.
- Geen aanwijsbare beslisser én geen champion die intern kan trekken → te vroeg; terug in de wachtstand tot er een eigenaar is.
- Puur informatie aan het verzamelen zonder enige aanleiding, budget of mandaat → vriendelijk parkeren, geen scoping-call inplannen.

**Vuistregel:** twijfel je tussen GA en no-go, dan is de scoping-call (fase 2) gratis voor de klant maar kost hém wel tijd. Alleen inplannen als hosting, tijdlijn en beslisser samen genoeg signaal geven dat dit een echte deal kan worden. We schieten nooit werk voor: provisionen en bouwen gebeurt pas ná tekening + aanbetaling.
