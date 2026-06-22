# Verwerkersovereenkomst (DPA) — Project X

> ⚠️ **CONCEPT. Laat dit juridisch toetsen vóór ondertekening.**
> Dit is een werkdocument/template, geen kant-en-klaar juridisch eindproduct. BotLease is geen juridisch adviseur. Laat deze tekst door een jurist of een gespecialiseerde AVG-/privacypartij nakijken en op de concrete situatie toesnijden vóór beide partijen tekenen. Verifieer ook of de verwijzingen naar de Microsoft-producten en de Microsoft DPA nog actueel zijn op het moment van ondertekenen (Microsoft- en Azure-voorwaarden wijzigen).

**Fase in het intake-proces:** Fase 3 (Voorstel + SOW + verwerkersovereenkomst). Deze overeenkomst hoort als bijlage bij de Statement of Work (SOW) en wordt samen daarmee voorgelegd. Tekening + aanbetaling (Fase 4) vinden plaats nadat beide partijen akkoord zijn.

**Hoe in te vullen:** vervang alle `[PLACEHOLDERS]` (klantnaam, adres, KvK, contactpersonen, data, regio, bewaartermijn). Schrap of pas aan wat niet van toepassing is. Velden die met `[in te vullen bij scoping]` zijn gemarkeerd komen uit de intake (`01-client-intake.md`) en/of de scoping-call.

---

## 0. Toelichting op de rollen (lees dit eerst, hoort niet in de getekende tekst)

Er zijn binnen Project X twee verschillende AVG-petten. Haal ze niet door elkaar:

1. **De intake-data zelf** (contact- en bedrijfsgegevens van de klant, KvK, gespreksnotities): hiervoor is **BotLease verwerkingsverantwoordelijke**. Dat valt onder de eigen **privacyverklaring** van BotLease, niet onder déze overeenkomst.
2. **De latere lead-data** (persoonsgegevens van bezoekers/leads die via de website, het contactformulier en de AI-chat van de klant binnenkomen): hiervoor is **BotLease (sub)verwerker** namens de klant. **Dat is waar deze verwerkersovereenkomst over gaat.**

De keten is: **Betrokkene (lead) → Klant (verwerkingsverantwoordelijke) → BotLease (verwerker) → sub-verwerkers (Microsoft Azure als EU-platform onder de Microsoft DPA + eventuele form-/intaketool).** Deze overeenkomst staat dus *bovenop* de Microsoft DPA, niet in plaats daarvan.

---

## Verwerkersovereenkomst

Deze verwerkersovereenkomst (de "Overeenkomst") is een bijlage bij en maakt onlosmakelijk deel uit van de tussen partijen gesloten dienstverleningsovereenkomst / Statement of Work d.d. `[DATUM SOW]` (de "Hoofdovereenkomst") betreffende Project X: het opzetten en beheren van een geautomatiseerde marketing- en lead-omgeving in Azure ("de Dienst").

### Artikel 1 — Partijen en rollen

**De Verwerkingsverantwoordelijke ("Verantwoordelijke"):**
- Naam: `[KLANTNAAM]`
- Rechtsvorm: `[RECHTSVORM]`
- Vestigingsadres: `[KLANTADRES, POSTCODE, PLAATS, LAND]`
- KvK-nummer (of buitenlands equivalent): `[KLANT KVK]`
- Vertegenwoordigd door: `[NAAM + FUNCTIE]`
- Contactpersoon privacy: `[NAAM + E-MAIL]`

**De Verwerker:**
- Handelsnaam: BotLease (eenmanszaak van Thomas Vedder)
- Vestigingsadres: `[VESTIGINGSADRES BOTLEASE]`, Amsterdam, Nederland
- KvK-nummer: 95943420
- Vertegenwoordigd door: Thomas Vedder
- Contactpersoon privacy: `[NAAM + E-MAIL BOTLEASE]`

**Rolverdeling.** Ten aanzien van de persoonsgegevens die via de Dienst worden verwerkt (de lead-/bezoekersgegevens van de Verantwoordelijke), treedt de Verantwoordelijke op als verwerkingsverantwoordelijke in de zin van artikel 4 lid 7 AVG, en BotLease als verwerker in de zin van artikel 4 lid 8 AVG. Deze Overeenkomst is opgesteld conform artikel 28 AVG.

Voor zover BotLease op haar beurt sub-verwerkers inschakelt (zie Artikel 9), treedt BotLease ten opzichte van die sub-verwerkers op als (sub)verwerkingsverantwoordelijke in de keten, doch de Verantwoordelijke blijft de eindverantwoordelijke.

### Artikel 2 — Onderwerp, aard, doel en duur van de verwerking

| Element | Invulling |
|---|---|
| **Onderwerp** | De verwerking van persoonsgegevens van bezoekers en (potentiële) leads van de Verantwoordelijke, in het kader van het afvangen, beantwoorden, kwalificeren en doorzetten van inbound sales-leads, en het leveren van de marketingwebsite + content-, SEO- en lead-functionaliteit van de Dienst. |
| **Aard van de verwerking** | Verzamelen, vastleggen, ordenen, opslaan, raadplegen, gebruiken (waaronder geautomatiseerde verwerking door een AI-/taalmodel voor het opstellen van reacties en het scoren van leads), doorzenden naar het door de Verantwoordelijke aangewezen kanaal (e-mail, Microsoft Teams of CRM), en wissen/anonimiseren. |
| **Doel** | Uitsluitend het uitvoeren van de Hoofdovereenkomst: lead-afvang, lead-beantwoording, lead-kwalificatie en lead-routing namens de Verantwoordelijke. Geen ander doel. |
| **Geautomatiseerde besluitvorming** | De AI-chat en lead-kwalificatie geven een score/advies; de uiteindelijke beslissing om een lead op te volgen ligt bij de Verantwoordelijke. `[in te vullen bij scoping: autonoom doorzetten boven drempelscore, of human-in-the-loop. Bij significante geautomatiseerde besluitvorming in de zin van art. 22 AVG aanvullende waarborgen opnemen.]` |
| **Duur** | Deze Overeenkomst geldt voor de looptijd van de Hoofdovereenkomst en eindigt van rechtswege bij beëindiging daarvan, behoudens de bepalingen die naar hun aard voortduren (geheimhouding, teruggave/verwijdering, aansprakelijkheid). |

### Artikel 3 — Categorieën betrokkenen en persoonsgegevens

**Categorieën betrokkenen:**
- Bezoekers van de website van de Verantwoordelijke;
- (Potentiële) klanten / leads die het contactformulier of de AI-chat gebruiken;
- `[eventueel: zakelijke contactpersonen bij bedrijfsleads]`.

**Categorieën persoonsgegevens:**
- Naam en (zakelijke) contactgegevens (e-mailadres, telefoonnummer indien opgegeven);
- Bedrijfsnaam en functie indien opgegeven;
- Inhoud van het contactbericht / chatgesprek (vrije tekst, kan door de betrokkene zelf verstrekte gegevens bevatten);
- Lead-kwalificatie-uitkomst (score, status, notities);
- Technische gegevens die nodig zijn voor anti-spam en logging (bv. tijdstempel, en uitsluitend voor zover noodzakelijk, een geanonimiseerd/gehasht IP-signaal voor rate-limiting);
- Consent-/audit-gegevens (welke privacyverklaring de betrokkene zag, akkoord-tijdstempel).

**Geen bijzondere categorieën.** Partijen beogen geen verwerking van bijzondere categorieën persoonsgegevens (art. 9 AVG) of strafrechtelijke gegevens (art. 10 AVG). De Verantwoordelijke zorgt ervoor dat de invoervelden en de inrichting van de Dienst er niet op aansturen dat betrokkenen dergelijke gegevens verstrekken. Mocht dit toch onverhoopt nodig zijn, dan maken partijen daarover vooraf aanvullende schriftelijke afspraken.

### Artikel 4 — Instructies van de Verantwoordelijke

1. BotLease verwerkt de persoonsgegevens uitsluitend op basis van schriftelijke instructies van de Verantwoordelijke, zoals vastgelegd in de Hoofdovereenkomst, de per-tenant configuratie en deze Overeenkomst, behalve wanneer een wettelijke verplichting BotLease tot verwerking noopt. In dat laatste geval stelt BotLease de Verantwoordelijke voorafgaand op de hoogte, tenzij die wetgeving dit verbiedt.
2. BotLease verwerkt de persoonsgegevens niet voor eigen doeleinden en gebruikt ze niet om eigen modellen te trainen of te verbeteren.
3. Indien BotLease van mening is dat een instructie van de Verantwoordelijke in strijd is met de AVG of andere privacywetgeving, meldt BotLease dit onverwijld aan de Verantwoordelijke.
4. **AI-transparantie.** De AI-chat van de Dienst maakt bij de eerste interactie kenbaar dat de betrokkene met een AI-assistent communiceert (conform de EU AI Act art. 50, in werking medio 2026). Deze melding is een vast, niet-uitschakelbaar onderdeel van de Dienst.

### Artikel 5 — Geheimhouding

1. BotLease verplicht zich tot geheimhouding van alle persoonsgegevens waarvan zij in het kader van deze Overeenkomst kennisneemt, behalve voor zover openbaarmaking wettelijk verplicht is.
2. BotLease draagt er zorg voor dat eenieder die onder haar gezag toegang heeft tot de persoonsgegevens (waaronder eventuele medewerkers en ingeschakelde derden) tot geheimhouding is verplicht, hetzij uit hoofde van een wettelijke verplichting, hetzij via een geheimhoudingsbeding.
3. De geheimhoudingsplicht blijft na afloop van deze Overeenkomst van kracht.

### Artikel 6 — Beveiligingsmaatregelen

BotLease treft passende technische en organisatorische maatregelen om de persoonsgegevens te beveiligen tegen verlies of onrechtmatige verwerking, rekening houdend met de stand van de techniek, de uitvoeringskosten en de aard, omvang, context en doeleinden van de verwerking (art. 32 AVG). De maatregelen omvatten ten minste:

- **EU-data-residentie.** Alle persoonsgegevens van de Dienst worden opgeslagen en verwerkt binnen de Europese Economische Ruimte, in Microsoft Azure (regio `[in te vullen: West Europe / North Europe / Sweden Central]`). `[in te vullen bij scoping: bij een harde EU-only-inference-eis wordt een Data Zone Standard (EU) model-deployment gebruikt; de modelkeuze is dan beperkt tot de op dat moment in de EU Data Zone beschikbare modellen (medio 2026 bv. GPT-4o / GPT-4.1).]`
- **Versleuteling.** Persoonsgegevens worden versleuteld opgeslagen (encryption at rest) en versleuteld verzonden (TLS/HTTPS in transit).
- **Secrets-beheer.** Geheimen (sleutels, credentials) worden bewaard in Azure Key Vault. Toegang verloopt waar mogelijk keyless via een managed identity; secrets worden nooit in broncode of repositories opgenomen.
- **Toegangsbeheer (RBAC).** Toegang verloopt volgens het principe van minimale rechten (least privilege) via Microsoft Entra ID en Azure RBAC, met scoped rollen op alleen de benodigde resources. Geen brede "Owner"-rechten waar dat niet nodig is.
- **Logische scheiding.** Gegevens van de Verantwoordelijke worden logisch (en in het klant-tenant-model fysiek) gescheiden gehouden van die van andere opdrachtgevers.
- **Anti-misbruik.** Publieke lead-endpoints zijn beschermd met anti-spam-maatregelen (o.a. een cookieloze CAPTCHA-vervanger, honeypot en rate-limiting) om misbruik en kostenexplosie te voorkomen.
- **Logging en monitoring.** Relevante gebeurtenissen worden gelogd voor beveiliging en het kunnen aantonen van naleving, met inachtneming van dataminimalisatie.

`[in te vullen bij scoping: indien private networking (VNet + private endpoints) is overeengekomen, hier opnemen als aanvullende maatregel.]`

De achterliggende platformbeveiliging van Microsoft Azure is geregeld in de Microsoft Products and Services Data Protection Addendum (de "Microsoft DPA"), waarnaar in Artikel 9 wordt verwezen.

### Artikel 7 — Meldplicht datalekken

1. BotLease informeert de Verantwoordelijke zonder onredelijke vertraging, en in elk geval binnen `[bv. 48 uur]` nadat zij bekend is geworden met een inbreuk in verband met persoonsgegevens (datalek), zodat de Verantwoordelijke kan voldoen aan haar eigen meldplicht jegens de Autoriteit Persoonsgegevens (binnen 72 uur, art. 33 AVG) en, waar van toepassing, jegens de betrokkenen (art. 34 AVG).
2. De melding bevat ten minste, voor zover bekend: de aard van de inbreuk, de (geschatte) categorieën en aantallen betrokkenen en gegevens, de waarschijnlijke gevolgen en de getroffen of voorgestelde maatregelen.
3. BotLease verleent de Verantwoordelijke redelijke medewerking bij het onderzoek, de beperking en de afhandeling van de inbreuk, en doet zelf geen mededelingen aan de toezichthouder of betrokkenen namens de Verantwoordelijke zonder diens voorafgaande afstemming, tenzij wettelijk verplicht.

### Artikel 8 — Rechten van betrokkenen

1. BotLease verleent de Verantwoordelijke, rekening houdend met de aard van de verwerking, redelijke medewerking en passende technische en organisatorische maatregelen om verzoeken van betrokkenen tot uitoefening van hun rechten (inzage, rectificatie, wissing, beperking, overdraagbaarheid, bezwaar; art. 12-23 AVG) te kunnen afhandelen.
2. Richt een betrokkene een dergelijk verzoek rechtstreeks tot BotLease, dan stuurt BotLease dit zonder onnodige vertraging door naar de Verantwoordelijke en handelt zij het niet zelfstandig af, tenzij de Verantwoordelijke daartoe instructie geeft.
3. BotLease verleent eveneens redelijke medewerking aan de verplichtingen van de Verantwoordelijke uit hoofde van art. 32 tot en met 36 AVG (beveiliging, datalekmelding, gegevensbeschermingseffectbeoordeling/DPIA en voorafgaande raadpleging), voor zover dat redelijkerwijs van BotLease kan worden verlangd en gelet op de aan BotLease ter beschikking staande informatie.

### Artikel 9 — Sub-verwerkers

1. De Verantwoordelijke verleent BotLease een algemene schriftelijke toestemming voor het inschakelen van sub-verwerkers, mits BotLease aan elke sub-verwerker bij overeenkomst ten minste dezelfde gegevensbeschermingsverplichtingen oplegt als in deze Overeenkomst zijn opgenomen (art. 28 lid 4 AVG).
2. **Bij aanvang ingeschakelde sub-verwerkers:**

   | Sub-verwerker | Rol / dienst | Locatie / residentie | Juridische grondslag |
   |---|---|---|---|
   | **Microsoft (Azure / Azure OpenAI / Foundry)** | Cloud-platform: hosting, opslag, e-mailverzending (ACS) en AI-/taalmodel-inferentie | EU / EER (regio `[in te vullen]`) onder de EU Data Boundary | Microsoft Products and Services Data Protection Addendum (Microsoft DPA). Microsoft treedt op als (sub)verwerker; prompts/completions worden niet gebruikt om Microsoft-modellen te trainen. |
   | `[FORM-/INTAKETOOL, bv. Tally]` *(indien van toepassing)* | Intake-/formulierdienst (alleen relevant voor intake-data; zie kanttekening) | `[EU / EER]` | `[DPA van de tool]` |
   | `[EVENTUELE OVERIGE, bv. Cloudflare Turnstile voor anti-spam]` | `[anti-spam]` | `[in te vullen]` | `[in te vullen]` |

   > Kanttekening: een form-/intaketool verwerkt doorgaans de **intake-data** (waarvoor BotLease verantwoordelijke is), niet de lead-data van deze Overeenkomst. Hij is hier opgenomen voor volledigheid van de keten; schrap deze rij als hij geen lead-persoonsgegevens raakt.

   > Externe SEO-/keyword-/domein-API's (bv. DataForSEO, domein-availability-checks) ontvangen **uitsluitend niet-persoonsgebonden data** (zoekwoorden, branchetermen, domeinnamen) en zijn daarom geen sub-verwerker van persoonsgegevens onder deze Overeenkomst. Persoonsgegevens van leads blijven strikt binnen Azure-EU.

3. BotLease informeert de Verantwoordelijke voorafgaand over voorgenomen wijzigingen in de sub-verwerkers (toevoeging of vervanging) en geeft de Verantwoordelijke de gelegenheid om binnen `[bv. 14 dagen]` gemotiveerd bezwaar te maken. Bij gegrond bezwaar zoeken partijen in redelijk overleg naar een oplossing; lukt dat niet, dan kan elk der partijen de betreffende dienst of de Hoofdovereenkomst beëindigen conform de daarin opgenomen voorwaarden.
4. BotLease blijft jegens de Verantwoordelijke volledig aansprakelijk voor de nakoming van de verplichtingen door de door haar ingeschakelde sub-verwerkers.

### Artikel 10 — Doorgifte buiten de EER

1. De persoonsgegevens van de Dienst worden binnen de EER opgeslagen en verwerkt. BotLease geeft geen persoonsgegevens door aan een land buiten de EER of aan een internationale organisatie, tenzij de Verantwoordelijke daarvoor voorafgaand schriftelijk toestemming geeft én aan de voorwaarden van hoofdstuk V AVG is voldaan (bv. een adequaatheidsbesluit of passende waarborgen zoals de EU-standaardcontractbepalingen).
2. Voor zover Microsoft als sub-verwerker onverhoopt verwerking buiten de EER zou laten plaatsvinden, gelden de waarborgen uit de Microsoft DPA, waaronder de EU-standaardcontractbepalingen. Bij een harde EU-residentie-eis wordt de Dienst zo geconfigureerd dat opslag én verwerking binnen de EU blijven (zie Artikel 6).

### Artikel 11 — Audit en controle

1. BotLease stelt de Verantwoordelijke op diens redelijke verzoek de informatie ter beschikking die nodig is om de naleving van de in art. 28 AVG en deze Overeenkomst neergelegde verplichtingen aan te tonen.
2. BotLease maakt audits, waaronder inspecties, door de Verantwoordelijke of een door hem gemachtigde controleur mogelijk en draagt eraan bij, met inachtneming van het volgende:
   - audits vinden plaats na redelijke voorafgaande aankondiging (`[bv. minimaal 14 dagen]`), maximaal `[bv. eenmaal per jaar]`, behoudens een concreet vermoeden van een inbreuk of een eis van de toezichthouder;
   - audits verstoren de bedrijfsvoering zo min mogelijk en respecteren de geheimhouding jegens andere opdrachtgevers;
   - de kosten van een door de Verantwoordelijke geïnitieerde audit komen voor diens rekening, tenzij de audit een wezenlijke tekortkoming van BotLease aantoont.
3. Voor de onderliggende platformlaag kan BotLease verwijzen naar de certificeringen en auditrapporten van Microsoft Azure (bv. ISO 27001, SOC 2), zoals beschikbaar gesteld onder de Microsoft DPA.

### Artikel 12 — Teruggave en verwijdering bij einde

1. Bij beëindiging van de Hoofdovereenkomst, of eerder op verzoek van de Verantwoordelijke, zal BotLease naar keuze van de Verantwoordelijke alle persoonsgegevens van de Dienst:
   - in een gangbaar, gestructureerd machineleesbaar formaat aan de Verantwoordelijke teruggeven/exporteren, en/of
   - veilig en onomkeerbaar verwijderen, inclusief bestaande kopieën,
   tenzij opslag van (een deel van de) persoonsgegevens wettelijk verplicht is.
2. BotLease voert de teruggave en/of verwijdering uit binnen `[bv. 30 dagen]` na het einde van de Hoofdovereenkomst en bevestigt de verwijdering desgevraagd schriftelijk.
3. In het klant-tenant-model (de Dienst draait in de eigen Azure-omgeving van de Verantwoordelijke) blijven de gegevens fysiek in de tenant van de Verantwoordelijke; "teruggave" is in dat geval het overdragen van het beheer en het intrekken van de beheertoegang van BotLease.

### Artikel 13 — Bewaartermijn

1. BotLease bewaart de lead-persoonsgegevens niet langer dan noodzakelijk voor het doel van de verwerking, en in elk geval niet langer dan de door de Verantwoordelijke vastgestelde bewaartermijn van `[BEWAARTERMIJN, default marketing: max. 2 jaar / 730 dagen na laatste contact zonder toestemming]`.
2. Na het verstrijken van de bewaartermijn worden de gegevens automatisch verwijderd of geanonimiseerd via een ingebouwde, periodieke verwijder-/anonimiseer-job (art. 5 lid 1 onder e AVG, opslagbeperking).
3. Consent-/audit-gegevens worden bewaard zolang dat nodig is om de rechtmatigheid van de verwerking te kunnen aantonen, en niet langer.

### Artikel 14 — Aansprakelijkheid

Op de aansprakelijkheid van partijen onder deze Overeenkomst is de aansprakelijkheidsregeling uit de Hoofdovereenkomst van toepassing, voor zover dwingend recht (waaronder de AVG) zich daar niet tegen verzet. `[in te vullen / afstemmen met de aansprakelijkheidsbepaling in de SOW en juridisch laten toetsen.]`

### Artikel 15 — Slotbepalingen

1. Bij strijdigheid tussen deze Overeenkomst en de Hoofdovereenkomst prevaleert, uitsluitend voor onderwerpen die de verwerking van persoonsgegevens betreffen, deze Overeenkomst.
2. Wijzigingen van deze Overeenkomst zijn alleen geldig indien schriftelijk overeengekomen en door beide partijen ondertekend.
3. Op deze Overeenkomst is Nederlands recht van toepassing. Geschillen worden voorgelegd aan de bevoegde rechter te `[ARRONDISSEMENT, bv. Amsterdam]`, tenzij partijen schriftelijk anders overeenkomen.

---

### Ondertekening

| | Verantwoordelijke | Verwerker |
|---|---|---|
| Naam organisatie | `[KLANTNAAM]` | BotLease (Thomas Vedder) |
| Naam ondertekenaar | `[NAAM]` | Thomas Vedder |
| Functie | `[FUNCTIE]` | Eigenaar |
| Datum | `[DATUM]` | `[DATUM]` |
| Handtekening | | |

---

> **Nogmaals: dit is een concept.** Laat het juridisch toetsen vóór ondertekening en stem het af op de definitieve SOW, de gekozen sub-verwerkers en de actuele Microsoft-voorwaarden. Verifieer prijzen, model-EU-beschikbaarheid en de status van de EU Data Boundary opnieuw vlak vóór gebruik; die wijzigen per kwartaal.
