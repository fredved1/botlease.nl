# Chat-transcript — AI-assistent Twentse Warmte (LOKALE TESTRUN)

> **Wat is dit?** Een gesimuleerd, realistisch chatgesprek tussen de **AI-chat-widget** op `/contact` en een bezoeker, als demonstratie van **stap 5** (afvangen + beantwoorden + kwalificeren) van de PROJECT X-pipeline.
>
> **Fictief.** Testbedrijf **Twentse Warmte** en de bezoeker (Marleen Brinkhuis) bestaan niet. Dit toont dezelfde lead als [`inbound-lead.json`](inbound-lead.json), maar dan via het chat-kanaal in plaats van het formulier.
>
> **In productie** draait de assistent op de **Foundry sales/qualify-agent** (Azure OpenAI `gpt-4o-mini`, Data Zone EU). De agent volgt `leads.qualification.custom_criteria` uit de client-config, slaat het gesprek op in Cosmos DB en levert aan het eind een JSON-kwalificatie ([`qualification.json`](qualification.json)). De **AI-disclosure is niet-uitschakelbaar** (EU AI Act Art. 50).

---

**Tijdstip:** 21 juni 2026, 14:33 (Europe/Amsterdam)
**Kanaal:** chat-widget op `twentsewarmte.nl/contact`
**Autonomie:** `human_in_loop` — de assistent informeert en plant een warmtescan-voorkeur, maar geeft **geen bindende prijs of offerte**. Dat doet Bram.

---

**Assistent (eerste bericht, automatisch):**
Hoi! Je chat met de digitale assistent van Twentse Warmte. **Ik ben een AI-assistent**, geen monteur. Ik kan je helpen met vragen over warmtepompen, kosten en subsidie, en alvast een gratis warmtescan voor je klaarzetten. Voor een persoonlijke offerte zet ik je door naar Bram (een mens). Waar kan ik je mee helpen?

**Bezoeker:**
Onze cv-ketel is bijna 15 jaar oud en hapert. We willen eigenlijk van het gas af. Kan dat met een warmtepomp in een huis uit 1998?

**Assistent:**
Goede kans van wel. Een tussen- of hoekwoning uit eind jaren 90 is vaak al redelijk geïsoleerd, dus daar past een hybride warmtepomp of soms een volledige warmtepomp prima bij. Met een ketel van 15 jaar zit je sowieso tegen vervanging aan, dus dit is een logisch moment om te verduurzamen. Mag ik wat vragen om je goed te kunnen helpen? Is het een **koopwoning** of huur je?

**Bezoeker:**
Koopwoning, een tussenwoning hier in Almelo.

**Assistent:**
Mooi, en Almelo valt binnen ons servicegebied in Twente, dus we kunnen langskomen. Want je noemde "van het gas af": denk je aan een **hybride warmtepomp** (de cv-ketel blijft als achtervang, lagere investering) of liever helemaal **all-electric**? Voor de meeste woningen uit die bouwperiode is hybride de nuchtere eerste stap.

**Bezoeker:**
Hybride lijkt me prima om mee te beginnen. Wat kost dat ongeveer? En klopt het dat er subsidie is?

**Assistent:**
Klopt, er is **ISDE-subsidie** voor warmtepompen in 2026. Het bedrag hangt af van het type en vermogen, en wij regelen de aanvraag voor je mee. Over de prijs ben ik eerlijk: een **exacte prijs geef ik bewust niet via de chat**, want die hangt af van je woning, je radiatoren en je warmtevraag. Een serieuze prijs hoor je pas ná de **gratis warmtescan aan huis** — dan meet onze monteur het echt op en krijg je een heldere offerte zonder verkooppraat. Achtergrond over kosten en de subsidie lees je hier: [hybride warmtepomp: kosten](/hybride-warmtepomp) en [ISDE-subsidie 2026](/blog/isde-subsidie-warmtepomp-2026). Zal ik die gratis warmtescan voor je klaarzetten?

**Bezoeker:**
Ja graag. Het liefst nog dit najaar, vóór de winter.

**Assistent:**
Helder, najaar 2026 dus, ruim op tijd voor het stookseizoen. Dan zet ik je aanvraag klaar voor Bram. Een paar laatste dingen zodat hij meteen iets aan je voorstel heeft:
1. Op welk **adres en postcode** zou de warmtescan zijn?
2. Op welke **naam** zal ik de aanvraag zetten?
3. Wat is het handigste **e-mailadres of telefoonnummer** om je te bereiken?

**Bezoeker:**
Marleen Brinkhuis, Vincent van Goghplein 14, 7606 GT Almelo. Mail: m.brinkhuis@outlook.com, of 06 24 18 77 30.

**Assistent:**
Dank je, Marleen. Ik heb genoeg om je aanvraag goed door te zetten. Korte samenvatting:
- **Koopwoning**, tussenwoning uit 1998 in Almelo (binnen ons servicegebied)
- **cv-ketel ~15 jaar**, haperend → vervanging actueel
- Interesse: **hybride warmtepomp** + **gratis warmtescan** + **ISDE-subsidie**
- Gewenste termijn: **dit najaar, vóór de winter**

Voor ik afsluit: ga je ermee akkoord dat we je gegevens gebruiken om deze warmtescan-aanvraag te behandelen? (Zie ons [privacybeleid](/privacy).)

**Bezoeker:**
Ja, prima.

**Assistent:**
Top, genoteerd (akkoord op 21-06-2026, 14:37). Je krijgt zo een **automatische bevestiging per e-mail** van mij. Daarna neemt **Bram (een mens)** persoonlijk contact met je op om de warmtescan in te plannen en je vragen over kosten en subsidie te beantwoorden. Fijne dag, Marleen!

---

## Wat de agent in productie achter de schermen deed

| Stap | Productie (Azure) |
|---|---|
| AI-disclosure tonen + loggen | Verplicht eerste bericht; consent + disclosure-tijdstip naar Cosmos (AI Act Art. 50) |
| Kwalificatie-vragen stellen | Foundry qualify-agent volgt `leads.qualification.custom_criteria` uit de client-config |
| Gesprek opslaan | Cosmos DB, partition = `tenantId`, retentie 730 dagen (auto-anonimiseer-job) |
| Geen bindende prijs | `chat_autonomy: human_in_loop` — prijs/offerte expliciet uit scope van de bot |
| JSON-kwalificatie produceren | Agent emit gestructureerde output → [`qualification.json`](qualification.json) |
| Auto-reply versturen | Azure Communication Services Email → [`ai-autoreply.md`](ai-autoreply.md) |
| Doorzetten (boven drempel 60) | Function/Logic App → e-mail naar Bram → [`routing-notification.md`](routing-notification.md) |

*Gesimuleerd gesprek, lokale PROJECT X-testrun, 2026-06-21. Fictief bedrijf en fictieve persoon.*
