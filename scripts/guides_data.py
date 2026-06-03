"""Content voor pillar guides, glossary, about/methodology, kosten-pagina.

Iedere guide is autoritair, lang en geoptimaliseerd voor primary/secondary keywords.
"""

PILLAR_GUIDE = {
    "slug": "humanoide-robot-leasen",
    "title": "Humanoïde robot leasen in Nederland - complete gids 2026 | BotLease",
    "meta_desc": "Complete gids voor humanoïde robot lease in Nederland: 15 modellen vergeleken, prijzen €290-4.490/mnd, EU AI-Act compliance, ROI per sector, het 4-weken pilot-proces. Inclusief vergelijking koop vs lease en checklist voor MKB.",
    "keywords": "humanoide robot leasen, humanoid robot lease Nederland, humanoide robot huren, robot lease MKB, humanoide robot kopen of leasen, humanoide robot prijs Nederland",
    "h1": "Humanoïde robot leasen in Nederland: de complete gids voor 2026.",
    "tagline": "15 modellen vergeleken, eerlijke prijzen, EU AI-Act compliance en het pilot-traject - geschreven voor Nederlandse MKB-ondernemers die weten wat ze willen.",
    "tldr": [
        "Lease-prijzen lopen van €290/mnd (Unitree R1, instap) tot €4.490/mnd (NEURA 4NE-1 Gen 3.5, industrieel). All-in inclusief installatie, training, onderhoud, swap-SLA en verzekering.",
        "Vijf modellen zijn EU-gebouwd (NEURA in Duitsland, PAL in Spanje, Pollen in Frankrijk) - dat is strategisch belangrijk voor de EU AI-Act die vanaf 2 augustus 2026 volledig van kracht is.",
        "Apptronik Apollo, Figure 02, 1X NEO en Boston Dynamics Atlas zijn pas vanaf Q4 2026 / Q1 2027 commercieel verkrijgbaar voor derden in EU. Reserveer-mogelijkheid via BotLease.",
        "Typische pilot kost €1.500 voor 4 weken. ROI loopt van 11-14 maanden (3PL) tot 18-24 maanden (zorg). Geen investering vooraf, opzegbaar per maand na jaar 1.",
    ],
    "sections": [
        {
            "id": "wat-is",
            "h": "1. Wat is humanoïde robot leasing eigenlijk?",
            "body": [
                "Humanoïde robot leasing is een vorm van operational lease waarbij een leasemaatschappij (zoals BotLease) eigenaar blijft van de robot en deze als dienst aan een eindgebruiker beschikbaar stelt - typisch voor 36 maanden, met installatie, training, onderhoud, swap-SLA en verzekering inbegrepen. De gebruiker betaalt een vaste maandprijs en draagt geen restwaarde-risico.",
                "Het belangrijkste verschil met klassieke robotleasing (zoals industriële arm-robots): humanoïdes zijn <b>multi-task</b>, ze passen in bestaande menselijke werkomgevingen zonder dat de vloer of werkstations aangepast hoeven worden. Dat maakt humanoid leasing aantrekkelijk voor MKB-bedrijven die anders nooit voor robotica zouden kiezen - zoals 3PLs met fluctuerende volumes, productiebedrijven met SKU-mix, hotels met piekuren, of zorginstellingen met logistiek-tekort.",
                "<a href=\"/robots\">In onze catalogus</a> staan 15 modellen, ingedeeld in drie categorieën: <a href=\"/robots#eu-gebouwd\">EU-gebouwd</a> (NEURA 4NE-1, PAL Kangaroo, Pollen Reachy 2 - strategisch belangrijk voor EU AI-Act compliance), Aziatisch leverbaar (Unitree, UBTECH, EngineAI - best value), en wachtlijst 2026/2027 (Apptronik Apollo, Figure 02, 1X NEO).",
            ],
        },
        {
            "id": "kopen-vs-leasen",
            "h": "2. Humanoïde robot kopen of leasen - wat is verstandig in 2026?",
            "body": [
                "Een Unitree G1 kost €16.000 aanschaf. Apptronik Apollo wordt rond de €48.000. Een NEURA 4NE-1 Gen 3.5 is €98.000. Maar dat is alleen de hardware. Tel daar bij op: installatie (€5-15k afhankelijk van complexiteit), training operators (€2-4k), software-integratie met je WMS/MES (€5-25k), eerste-jaarsonderhoud + reserveonderdelen (~15% van de aanschafprijs), verzekering (~3% van de aanschafprijs per jaar). Dan praat je over een Total Cost of Ownership van €35k-€170k in jaar 1.",
                "<b>Waarom leasen voor MKB?</b> Drie redenen: (1) Geen investering vooraf - de €100k+ blijft op je balans als werkkapitaal. (2) Geen restwaarde-risico - humanoïde robots zijn nieuwe technologie, niemand weet wat ze in 3 jaar waard zijn. (3) Geen onderhoudslast - wij vervangen binnen 24 uur (<a href=\"/methodologie#swap-sla\">Swap-SLA</a>) en doen preventief onderhoud op afstand.",
                "<b>Wanneer kopen?</b> Alleen als je 24/7 één specifieke taak hebt, weet dat de robot 5+ jaar meegaat, en je een eigen onderhoudsteam hebt. Voor 95% van de Nederlandse MKB-bedrijven is dat niet zo. Voor R&D bij scale-ups en universiteiten kan koop wel logisch zijn (lange afschrijftermijn, eigen kennis).",
                "<a href=\"/kosten\">Bereken hier wat een specifieke robot voor jouw situatie kost</a> - vergelijkt koop vs. lease voor alle 15 modellen.",
            ],
        },
        {
            "id": "modellen",
            "h": "3. Welke 15 modellen zijn nu in Nederland leverbaar?",
            "body": [
                "Marktonderzoek van mei 2026 levert een gefilterd, eerlijk overzicht. Veel modellen die in de media verschijnen (Tesla Optimus, Boston Dynamics Atlas, Figure 02) zijn nog niet open verkocht in EU - alleen pilot-deployments bij specifieke OEMs. Dit zijn de modellen die je vandaag of binnen 12 maanden kunt leasen.",
                "<b>EU-gebouwd - strategische kern (5 modellen):</b>",
                "<ul><li><a href=\"/robots/neura-4ne1-mini\">NEURA 4NE-1 Mini</a> (€890/mnd) - Duitse cobot, artificial skin, Porsche-design.</li><li><a href=\"/robots/neura-4ne1-gen3\">NEURA 4NE-1 Gen 3.5</a> (€4.490/mnd) - industrieel flagship, 100 kg payload, Bosch partner.</li><li><a href=\"/robots/pal-kangaroo\">PAL Kangaroo</a> (€3.490/mnd) - Spaanse bipedal, 20+ jaar heritage, ROS-native.</li><li><a href=\"/robots/pal-tiago-pro\">PAL TIAGo Pro</a> (€1.890/mnd) - wheeled humanoid, 100+ EU-deployments.</li><li><a href=\"/robots/pollen-reachy-2\">Pollen Reachy 2</a> (€2.690/mnd) - open-source, Hugging Face-owned.</li></ul>",
                "<b>Aziatisch leverbaar - best value (6 modellen):</b>",
                "<ul><li><a href=\"/robots/unitree-r1\">Unitree R1</a> (€290/mnd) - instap, demo + education.</li><li><a href=\"/robots/unitree-g1\">Unitree G1</a> (€899/mnd) - bestseller, R&D + hospitality.</li><li><a href=\"/robots/unitree-h1-2\">Unitree H1-2</a> (€3.990/mnd) - full-size industrieel.</li><li><a href=\"/robots/unitree-h2\">Unitree H2</a> (€1.890/mnd) - service met bionisch gezicht.</li><li><a href=\"/robots/engineai-se01\">EngineAI SE01</a> (€1.290/mnd) - natuurlijke gait.</li><li><a href=\"/robots/ubtech-walker-s2\">UBTECH Walker S2</a> (€3.290/mnd) - auto-industrie, mass production.</li></ul>",
                "<b>Wachtlijst 2026/2027 - reserveer voor priority access (4 modellen):</b>",
                "<ul><li><a href=\"/robots/apptronik-apollo\">Apptronik Apollo</a> - Mercedes-Benz pilot, EU Q4 2026.</li><li><a href=\"/robots/figure-02\">Figure 02 / 03</a> - BMW deployment, derde partijen Q1 2027+.</li><li><a href=\"/robots/agility-digit\">Agility Digit v4</a> - Amazon/GXO RaaS, EU-distributie nog niet open.</li><li><a href=\"/robots/1x-neo\">1X NEO</a> - Noorwegen, EU-shipping Q1 2027.</li></ul>",
                "Vergelijk modellen direct in onze <a href=\"/vergelijken\">vergelijkingstool</a> of bekijk de <a href=\"/robots\">volledige catalogus</a> met filters per tier, payload en prijs.",
            ],
        },
        {
            "id": "kosten",
            "h": "4. Hoeveel kost humanoïde robot leasing in 2026?",
            "body": [
                "Eerlijke prijzen - niet de \"vanaf €XXX\" marketing-flauwekul. Hier is hoe BotLease leaseprijzen berekent:",
                "<b>Formule:</b> Lease prijs/mnd = (Aanschafprijs / 36 maanden) + 25% service + 8% verzekering + 30% marge. Voor een €20.000 robot komt dat neer op ongeveer €890/mnd. Voor een €100.000 robot ongeveer €4.000/mnd.",
                "<b>Wat zit er in:</b> Installatie + 2-uurs operatortraining, preventief én correctief onderhoud, alle onderdelen, swap-SLA (vervangende unit binnen 24 uur op locatie), WA-verzekering tot €2,5M + casco, 24/7 helpdesk in het Nederlands, software-updates en remote tuning, integratie met je WMS/MES tijdens onboarding.",
                "<b>Wat zit er niet in:</b> Pilot (€1.500 voor 4 weken), end-of-contract demontage (€500), elektriciteitskosten op locatie (~€30/mnd), custom integraties die langer dan 40 uur duren (€95/uur).",
                "<b>Volume-korting:</b> Vanaf 3 units krijg je 8% korting op de leaseprijs. Vanaf 10 units 15%.",
                "<b>Contracttermijn:</b> 36 maanden standaard. 24 maanden +7%. 12 maanden +15%. Vast eerste jaar, daarna maandelijks opzegbaar met 1 maand opzegtermijn.",
                "<a href=\"/kosten\">Reken hier interactief de exacte prijs voor jouw situatie uit</a> - inclusief vergelijking met koop scenario.",
            ],
        },
        {
            "id": "model-kiezen",
            "h": "5. Hoe kies je het juiste humanoid model?",
            "body": [
                "Vier vragen om het juiste model te kiezen:",
                "<b>Vraag 1: Wat is je primaire taak?</b> Demo + R&D → <a href=\"/robots/unitree-r1\">Unitree R1</a>, <a href=\"/robots/unitree-g1\">Unitree G1</a>, <a href=\"/robots/pollen-reachy-2\">Pollen Reachy 2</a>. Industriële kitting + parts-handling → <a href=\"/robots/neura-4ne1-gen3\">NEURA 4NE-1 Gen 3.5</a>, <a href=\"/robots/ubtech-walker-s2\">UBTECH Walker S2</a>. 3PL tote-handling → <a href=\"/robots/agility-digit\">Digit</a> (wachtlijst) of <a href=\"/robots/unitree-h1-2\">Unitree H1-2</a>. Service in publieke ruimtes → <a href=\"/robots/unitree-h2\">Unitree H2</a>, <a href=\"/robots/1x-neo\">1X NEO</a> (wachtlijst).",
                "<b>Vraag 2: Is EU AI-Act compliance kritiek voor je?</b> Zo ja, kies EU-gebouwd. NEURA, PAL en Pollen zijn vanaf dag 1 EU AI-Act + Machineverordening 2023/1230 ready. Aziatische modellen vereisen een conformity assessment per deployment (verzorgen wij, maar duurt 2-4 weken extra).",
                "<b>Vraag 3: Welk budget heb je?</b> €290-900/mnd → R1, G1, NEURA Mini, H2. €1.500-2.500/mnd → TIAGo, EngineAI, Reachy. €3.000-4.500/mnd → H1-2, Walker S2, PAL Kangaroo, NEURA Gen 3.5, Apollo. Wachtlijst niet inbegrepen.",
                "<b>Vraag 4: Hoe complex is je werkvloer?</b> Eenvoudige aisle-layout + dezelfde taak elke dag → goedkoper Aziatisch model. Mixed-mens-robot productielijnen + veranderende SKUs → premium cobot (NEURA, Apollo).",
                "Twijfel? <a href=\"/#contact\">Plan een gratis intake</a> - wij komen langs en adviseren onafhankelijk welk model past. We verkopen niet één merk: we verkopen wat past.",
            ],
        },
        {
            "id": "ai-act",
            "h": "6. EU AI-Act en Machineverordening 2023/1230 - wat betekent dit voor 2026?",
            "body": [
                "Twee Europese wetten raken elkaar precies waar humanoid leasing ligt. Een korte gids - uitgebreide versie staat in onze <a href=\"/gids/ai-act-machineverordening\">AI-Act gids</a>.",
                "<b>EU AI-Act</b> wordt vanaf 2 augustus 2026 volledig van toepassing. Humanoïde robots vallen vrijwel allemaal onder \"high-risk AI\" zodra ze veiligheidskritisch worden ingezet. Dat betekent: conformity assessment vóór deployment, technische documentatie, post-market monitoring, en transparantie over de AI-functies.",
                "<b>EU Machineverordening 2023/1230</b> vervangt de oude Machinerichtlijn vanaf 20 januari 2027. Nieuwe vereisten voor cybersecurity, AI-veiligheid en software-updates. Dit gaat per deployment beoordeeld worden, niet alleen per robotmodel.",
                "<b>Wat doet BotLease?</b> Wij dragen de compliance-last als <i>provider</i> én helpen jou als <i>deployer</i> voldoen aan je verplichtingen. EU-gebouwde robots (NEURA, PAL, Pollen) hebben de meeste documentatie al klaar; voor Aziatische modellen voeren wij de conformity assessment per locatie uit.",
                "<b>Wat moet jij doen als werkgever?</b> Risicoanalyse vóór deployment, werkzones definiëren, operators trainen, post-market monitoring. Allemaal opgenomen in ons pilot-traject - geen aparte juridische kosten voor jou.",
            ],
        },
        {
            "id": "pilot",
            "h": "7. Het 4-weken pilot-proces stap-voor-stap",
            "body": [
                "<b>Week 0: Intake (gratis).</b> Gesprek op jouw locatie, 60-90 min. Wij meten de werkruimte, bekijken de taak, en kiezen 1-2 modellen die passen. Resultaat: lease-voorstel met heldere prijs en termijn.",
                "<b>Week 1: Deployment.</b> Robot op locatie. Veiligheidsanalyse, werkzone-definitie, eerste taakprogrammering. Operators krijgen 2-uurs training. Integratie met WMS/MES als die er is.",
                "<b>Week 2: Productie.</b> Robot draait in echte workflow. Telemetrie meet uptime, cyclustijd, foutpercentage en interventies. Wij monitoren remote en sturen bij waar nodig.",
                "<b>Week 3: Optimalisatie.</b> Op basis van eerste 2 weken data: taakherprogrammering, gripper-aanpassing, route-optimalisatie. Soms blijkt een andere robot beter te passen - dan switchen we.",
                "<b>Week 4: Evaluatie.</b> ROI-rapport: bespaarde uren, opbrengsten, knelpunten. Beslissing: lease (36 mnd) of robot retour. Geen druk.",
                "<b>Kosten pilot:</b> €1.500 vast, inclusief installatie en demontage. Als je doorgaat met lease, krijg je dit eerste-maand terug.",
            ],
        },
        {
            "id": "roi",
            "h": "8. ROI per sector - wat verdien je terug?",
            "body": [
                "Op basis van publieke pilot-data uit EU/VS en onze eigen modellen - eerlijke cijfers, geen marketing.",
                "<b><a href=\"/sectoren/3pl-fulfillment\">3PL & e-commerce fulfillment</a>:</b> 11-14 maanden ROI. Een UBTECH Walker S2 of (vanaf 2027) Apollo vervangt ~1,3 FTE in 2-ploegen. Bij €28/uur loonkost en 1,3 FTE × 2.080 uur/jaar = €76k bespaarde loonkosten/jaar. Met €3.290/mnd lease (€39.480/jaar) is netto resultaat ~€36k/jaar.",
                "<b><a href=\"/sectoren/productie-assemblage\">Productie & assemblage</a>:</b> 13-18 maanden ROI. Een NEURA 4NE-1 Gen 3.5 in een mixed-assembly cel vervangt geen FTE, maar versnelt cyclustijd met 15-25%. Voor een lijn met €2M omzet/jaar is dat €300-500k extra capaciteit.",
                "<b><a href=\"/sectoren/hospitality-retail\">Hospitality & retail</a>:</b> 18-24 maanden ROI. Een Unitree G1 doet nachtelijke voorraadtelling = 2 FTE/week × €28/uur × 50 weken = €58k/jaar. Plus de gastenscore-uplift van een lobby-host (NEO of H2).",
                "<b><a href=\"/sectoren/zorg-instellingen\">Zorg & instellingen</a>:</b> 18-30 maanden ROI. Lastiger om in geld uit te drukken want primair is het personeelsbehoud, niet kostenbesparing. Gemiddeld 0,6 FTE vrijgespeeld voor zorgtaken per robot. Voor een 200-bedden instelling: ~€42k/jaar bespaarde wervings- en inwerkkosten + betere zorgkwaliteit.",
            ],
        },
        {
            "id": "stappen",
            "h": "9. Volgende stappen - concreet",
            "body": [
                "<b>Verken vrijblijvend:</b> <a href=\"/robots\">Bekijk de catalogus</a>, <a href=\"/vergelijken\">vergelijk modellen</a> of lees onze <a href=\"/nieuws\">analyses van pilot-deployments</a>.",
                "<b>Lees verder:</b> <a href=\"/gids/ai-act-machineverordening\">EU AI-Act gids</a>, <a href=\"/kosten\">lease cost calculator</a>, of <a href=\"/begrippen\">terminologie glossary</a>.",
                "<b>Plan een gratis intake:</b> <a href=\"/#contact\">Plan een demo</a>. Wij komen langs binnen 5 werkdagen, beoordelen je situatie, en geven binnen 48 uur een lease-voorstel.",
            ],
        },
    ],
    "faq": [
        ("Wat is het verschil tussen humanoid robot en cobot?",
         "Een cobot (collaborative robot) is meestal een arm-robot zonder benen, vastgemonteerd op een tafel of machine. Een humanoid heeft twee benen en twee armen - meer mobiel, maar ook complexer. Sommige modellen (NEURA 4NE-1 Mini, PAL TIAGo Pro) zitten tussen beide in: humanoid bovenlichaam op een wheeled basis."),
        ("Welke is de goedkoopste humanoide robot in Nederland?",
         "Unitree R1 - lease vanaf €290/maand (aanschafprijs $4.900). Geschikt voor demo, education en lichte hospitality. Niet voor productiewerk."),
        ("Is humanoide robot leasing AVG/GDPR compliant?",
         "Ja - camera- en sensorstreams blijven on-prem of in EU-cloud (Hetzner Frankfurt). BotLease sluit een verwerkersovereenkomst (DPA) per klant. EU-gebouwde modellen (NEURA, PAL) zijn extra preferent voor GDPR-gevoelige werkomgevingen."),
        ("Hoe lang duurt het tot een robot operationeel is?",
         "Intake binnen 5 werkdagen. Pilot start gemiddeld 10 werkdagen na intake. Productieve inzet vanaf week 2 van de pilot. Lease-contract start na 4-weken pilot."),
        ("Wat als de robot stuk gaat?",
         "Swap-SLA: binnen 24 uur is een vervangende unit op locatie. De defecte gaat naar onze workshop in Eindhoven. Halen we de 24u niet, dan krijg je een dagvergoeding van €100/dag."),
        ("Kan ik tussentijds opzeggen?",
         "Het eerste jaar zit je vast (anders is de pilot-investering niet rendabel voor ons). Daarna maandelijks opzegbaar met 1 maand opzegtermijn. Geen boete."),
        ("Heb ik technische kennis nodig om een robot te bedienen?",
         "Nee. Wij verzorgen installatie, programmering en training. Voor dagelijks gebruik volstaat een 2-uurs training. Aanpassingen aan taken doen wij op afstand of on-site."),
        ("Welke robot past het beste bij mijn bedrijf?",
         "Dat is precies wat de gratis intake bepaalt. In 60 minuten weten we welk model past, wat de pilot kost, en wat de verwachte ROI is. Plan een gesprek via de <a href=\"/#contact\">contactsectie</a>."),
    ],
}


AI_ACT_GUIDE = {
    "slug": "ai-act-machineverordening",
    "title": "EU AI-Act + Machineverordening | gids 2026 | BotLease",
    "meta_desc": "Wat verandert er voor werkgevers met humanoïde robots vanaf 2 augustus 2026 (AI-Act) en 20 januari 2027 (Machineverordening 2023/1230)? Uitgebreide compliance-gids: high-risk classificatie, conformity assessment, deployer-verplichtingen, EU-gebouwd voordeel.",
    "keywords": "EU AI Act robot, Machineverordening 2023/1230, humanoide robot regelgeving Nederland, AI-Act werkgever, robot compliance EU, AI Act high-risk humanoid",
    "h1": "EU AI-Act + Machineverordening voor humanoïde robots.",
    "tagline": "Twee Europese wetten raken elkaar precies waar humanoid-werk plaatsvindt. Wat moet jij als werkgever, deployer of bedrijfseigenaar weten - en wanneer?",
    "tldr": [
        "EU AI-Act treedt volledig in werking op 2 augustus 2026. Humanoïdes vallen vrijwel altijd onder \"high-risk AI\" als ze veiligheidskritisch zijn.",
        "EU Machineverordening 2023/1230 vervangt de oude Machinerichtlijn vanaf 20 januari 2027. Nieuwe cybersecurity- en AI-vereisten.",
        "Dubbele conformiteit vereist: CE-markering (Machineverordening) + AI Act conformity assessment per gebruikssituatie.",
        "EU-gebouwde leveranciers (NEURA, PAL, Pollen) hebben de meeste documentatie al klaar. US/CN-modellen vereisen extra assessment van 2-4 weken.",
        "Werkgever (deployer) verplichtingen: risicoanalyse, post-market monitoring, transparantie naar werknemers. BotLease verzorgt dit binnen het pilot-traject.",
    ],
    "sections": [
        {
            "id": "context",
            "h": "1. Waarom twee wetten en niet één?",
            "body": [
                "Tot 2024 had Europa één robot-regulering: de Machinerichtlijn 2006/42/EG. Die wet ging vooral over fysieke veiligheid - kunnen mensen geraakt of geplet worden. Voor klassieke industriële robots werkte dat prima.",
                "Maar humanoïdes hebben twee gezichten: ze zijn machines (fysieke veiligheid) én ze hebben AI (gedragsveiligheid). Een Apptronik Apollo die een verkeerde inschatting maakt over wat de operator gaat doen, valt niet onder de Machinerichtlijn - daar gaat het over <i>klemvang</i>, niet over <i>beslissingen</i>.",
                "Dus heeft de EU twee complementaire wetten gemaakt: de <b>AI-Act</b> (Verordening 2024/1689) voor de AI-kant, en de nieuwe <b>Machineverordening 2023/1230</b> als upgrade van de Machinerichtlijn, met expliciete vereisten voor digitale systemen en cybersecurity.",
                "Beide gelden voor humanoïde robots. Dubbele conformiteit. Dat klinkt veel, maar in de praktijk overlappen de checks 60-70%.",
            ],
        },
        {
            "id": "ai-act-basics",
            "h": "2. EU AI-Act - wat is het, wanneer geldt het, voor wie?",
            "body": [
                "<b>Wat:</b> Verordening (EU) 2024/1689, officieel gepubliceerd 12 juli 2024. Geleidelijke inwerkingtreding tussen feb 2025 (verboden AI-praktijken) en aug 2027 (volledig). Voor humanoid-werkgevers is de cruciale datum <b>2 augustus 2026</b>: vanaf dan gelden alle bepalingen voor high-risk AI-systemen.",
                "<b>Voor wie:</b> Iedereen die een AI-systeem in de EU op de markt brengt (<i>provider</i>) of gebruikt voor professionele doeleinden (<i>deployer</i>). Voor humanoid-leasing: de fabrikant + BotLease zijn providers. Jouw bedrijf is deployer.",
                "<b>Risicoclassificatie:</b> 4 niveaus. Onaanvaardbaar risico (verboden - bv. sociaal kredietscoresysteem), hoog risico (strenge eisen), beperkt risico (transparantie-eisen), minimaal risico (geen specifieke eisen).",
                "<b>Humanoïde robots in werkomgevingen vallen vrijwel altijd onder high-risk.</b> Reden: ze worden ingezet voor taken die de veiligheid of fundamentele rechten van werknemers kunnen beïnvloeden (artikel 6, AI-Act + Annex III voor werkgelegenheidstoepassingen).",
            ],
        },
        {
            "id": "high-risk-eisen",
            "h": "3. Wat moet een high-risk AI-systeem doen?",
            "body": [
                "Acht vereisten in een notendop (artikelen 8-15 AI-Act):",
                "<ul><li><b>Risk management system</b> - geïdentificeerde en gemonitorde risico's gedurende de levensduur.</li><li><b>Data governance</b> - trainingsdata moet representatief en bias-vrij zijn, met audit-trail.</li><li><b>Technische documentatie</b> - alles wat een conformity assessment-auditeur moet kunnen lezen.</li><li><b>Record-keeping</b> - automatische logging van AI-besluiten gedurende minimaal 6 maanden.</li><li><b>Transparantie</b> - werknemers moeten weten dat ze met AI werken en welke data verzameld wordt.</li><li><b>Human oversight</b> - er moet een mens zijn die kan ingrijpen en de robot kan stoppen.</li><li><b>Accuracy + robustness + cybersecurity</b> - gemeten en gedocumenteerd.</li><li><b>Quality management system</b> - voor de provider (fabrikant + BotLease).</li></ul>",
                "De meeste zijn de verantwoordelijkheid van de provider (fabrikant + BotLease). Voor jou als deployer (eindgebruiker): transparantie naar werknemers, human oversight inrichten, en post-market monitoring uitvoeren (= bijhouden of de robot doet wat hij moet doen).",
            ],
        },
        {
            "id": "machine-verordening",
            "h": "4. EU Machineverordening 2023/1230 - wat verandert er?",
            "body": [
                "De Machineverordening (EU) 2023/1230 vervangt de oude Machinerichtlijn 2006/42/EG vanaf <b>20 januari 2027</b>. Wat is anders:",
                "<ul><li><b>Cybersecurity-vereisten</b> - robots moeten beveiligd zijn tegen hacking. Specifiek voor humanoïdes: software-updates, encrypted communication, secure boot.</li><li><b>AI-gerelateerde veiligheid</b> - als de robot AI gebruikt om beslissingen te nemen, moet het AI-component apart geëvalueerd worden. Dit haakt aan op de AI-Act.</li><li><b>Software updates</b> - niet meer optional. Voor de hele levensduur moet de fabrikant updates leveren. Voor lease-modellen (BotLease) betekent dit dat wij continu moeten patchen.</li><li><b>Significante modificaties</b> - als je een robot na deployment significant aanpast (nieuwe gripper, andere AI-model), moet er een nieuwe conformity assessment.</li><li><b>Digitale documentatie</b> - papier-handleidingen mogen vervangen worden door digitale, met QR-code op de robot.</li></ul>",
                "Voor leveranciers buiten de EU (Unitree, UBTECH, EngineAI) wordt dit een hobbel. Hun robots zijn ontworpen voor de Chinese markt en moeten geretrofit worden voor EU-conformiteit. BotLease verzorgt deze retrofit binnen ons lease-traject - geen extra kosten voor jou.",
            ],
        },
        {
            "id": "deployer-checklist",
            "h": "5. Checklist voor werkgevers (deployers)",
            "body": [
                "Wat jij als werkgever moet doen vóór je een humanoid in dienst neemt:",
                "<ul><li><b>Risicoanalyse op locatie</b> - werkzones, route-conflicten, mens-robot interacties. Wij doen dit in week 1 van de pilot.</li><li><b>Transparantieverklaring aan werknemers</b> - vooral OR / vakbond moet betrokken zijn. Welke data wordt verzameld? Wie heeft toegang?</li><li><b>Operator-training</b> - minstens 1 persoon op locatie moet de robot kunnen stoppen en herstarten. Wij verzorgen 2-uurs training.</li><li><b>Post-market monitoring</b> - logging van incidenten, uptime, foutpercentage. Wij leveren een maandelijks rapport.</li><li><b>Incident-meldingsplicht</b> - bij ernstige incidenten (letsel, dataverlies) moet je melden bij de AI-Office (Brussel) binnen 15 dagen. Wij faciliteren dit als provider.</li><li><b>Verwerkersovereenkomst (DPA)</b> - voor AVG/GDPR-conformiteit van camera- en sensordata.</li></ul>",
                "Klinkt veel? In de praktijk doet BotLease 80% binnen het pilot-traject. Voor jou blijft over: OR informeren, operator aanwijzen, en het post-market rapport doornemen.",
            ],
        },
        {
            "id": "eu-vs-cn-us",
            "h": "6. Waarom EU-gebouwde robots in voordeel zijn",
            "body": [
                "Een veelgemaakt misverstand: \"als de robot CE-gemarkeerd is, ben ik klaar\". Niet meer in 2026/2027. De AI-Act voegt een aparte conformity assessment toe die <i>per AI-systeem</i> beoordeeld wordt - niet alleen per hardware-model.",
                "EU-gebouwde modellen - <a href=\"/robots/neura-4ne1-gen3\">NEURA 4NE-1</a>, <a href=\"/robots/pal-kangaroo\">PAL Kangaroo</a>, <a href=\"/robots/pollen-reachy-2\">Pollen Reachy 2</a> - hebben de meeste compliance-documentatie al klaar omdat de fabrikanten zelf EU-bedrijven zijn. NEURA werkt direct met TÜV Süd, PAL is Spaans + 20+ jaar EU-gecertificeerd. Voor jou als deployer betekent dat: kortere onboarding, minder juridische risico, lagere kans op verrassingen.",
                "Aziatische modellen - <a href=\"/robots/unitree-g1\">Unitree</a>, <a href=\"/robots/ubtech-walker-s2\">UBTECH</a>, <a href=\"/robots/engineai-se01\">EngineAI</a> - vereisen extra werk. BotLease voert per locatie een conformity assessment uit (2-4 weken extra) en houdt EU-specifieke patches bij. Niet onmogelijk, wel meer werk.",
                "Amerikaanse modellen - <a href=\"/robots/apptronik-apollo\">Apptronik Apollo</a>, <a href=\"/robots/figure-02\">Figure</a>, <a href=\"/robots/1x-neo\">1X NEO</a> - zijn pas eind 2026 / Q1 2027 EU-leverbaar omdat de fabrikanten nu zelf hun documentatie EU-klaar maken. Daarom staan ze op onze <a href=\"/robots#waitlist\">wachtlijst</a>.",
            ],
        },
        {
            "id": "tijdpad",
            "h": "7. Tijdpad - wat moet wanneer?",
            "body": [
                "<ul><li><b>2 februari 2025:</b> AI-Act bepalingen voor verboden AI-praktijken treden in werking. Niet relevant voor humanoid-leasing.</li><li><b>2 augustus 2025:</b> AI-Act algemene bepalingen + AI-Office in Brussel operationeel.</li><li><b>2 februari 2026:</b> AI-Act-codes-of-practice voor general-purpose AI gereed. Indirect relevant.</li><li><b>2 augustus 2026:</b> ⚠️ <b>AI-Act volledig van toepassing.</b> High-risk AI-systemen (= alle humanoid-deployments in werkomgevingen) moeten conformity assessment hebben afgerond.</li><li><b>20 januari 2027:</b> ⚠️ <b>Machineverordening 2023/1230 verplicht.</b> Oude Machinerichtlijn vervalt voor nieuwe deployments.</li><li><b>2 augustus 2027:</b> AI-Act volledige inwerkingtreding voor alle bepalingen.</li></ul>",
                "Voor BotLease betekent dit: alles wat we vóór augustus 2026 deployen moet eind augustus 2026 compliant zijn. Alles wat we vanaf 2027 deployen moet ook aan de Machineverordening voldoen. Wij plannen contracten zo dat dit ingebouwd is.",
            ],
        },
        {
            "id": "praktijk",
            "h": "8. Praktijkvoorbeeld - wat betekent dit voor jouw deployment?",
            "body": [
                "Scenario: een 3PL in Rotterdam wil in juli 2026 starten met 2× Unitree H1-2 voor tote-handling.",
                "<b>Stappen:</b>",
                "<ul><li>Week 1: intake + risicoanalyse op locatie. BotLease documenteert werkzones, route-conflicten, mens-robot interacties.</li><li>Week 2: conformity assessment voor de Unitree H1-2 in deze specifieke deployment-situatie. Duurt extra tijd omdat het een Chinees model is.</li><li>Week 3: deployment + 2-uurs operator-training. OR/personeel ingelicht via transparantieverklaring. Verwerkersovereenkomst getekend.</li><li>Week 4: productie + post-market monitoring start. Eerste maandrapport in week 8.</li><li>2 augustus 2026: extra compliance-check - geen acties nodig want we hebben de assessment al gedaan.</li><li>20 januari 2027: Machineverordening-update - BotLease patcht software automatisch.</li></ul>",
                "Totale extra-tijd door regelgeving: 2-4 weken bovenop pilot. Totale extra-kosten voor klant: €0 - alles zit in onze leaseprijs verwerkt.",
            ],
        },
    ],
    "faq": [
        ("Vallen ALLE humanoid-deployments onder high-risk?",
         "Niet allemaal - een R&D-opstelling in een lab is meestal niet high-risk. Maar zodra je de robot inzet in een werkomgeving met andere mensen (productie, magazijn, kantoor), wordt het bijna altijd high-risk. BotLease beoordeelt dit per deployment in week 1 van de pilot."),
        ("Wat als ik nu al een robot in gebruik heb (vóór augustus 2026)?",
         "Bestaande deployments moeten vóór 2 augustus 2027 in compliance gebracht worden. Geen \"grandfathering\" - de AI-Act geldt retroactief voor systemen die in productie blijven."),
        ("Mag ik een Chinese robot blijven gebruiken na 2027?",
         "Ja, mits er voor jouw deployment een conformity assessment is. Het mag NIET zo zijn dat een robot zonder assessment in een werkomgeving draait. BotLease zorgt voor dit assessment voor elke deployment in onze lease-portfolio."),
        ("Wie betaalt de boete als er iets misgaat?",
         "Hangt af van wie de fout heeft gemaakt. Als de robot een design-fout heeft: fabrikant + BotLease (als provider). Als jij als werkgever de robot buiten zijn werkzone gebruikt: jij. Dit staat helder in de lease-overeenkomst."),
        ("Hoe hoog zijn de boetes?",
         "Tot €35 miljoen of 7% van de wereldwijde jaaromzet voor de zwaarste overtredingen (verboden AI-praktijken). Voor high-risk overtredingen: tot €15M / 3%. Voor administratieve overtredingen: €7,5M / 1,5%. Voor MKB is de boete lager (proportioneel)."),
        ("Werkt mijn humanoid samen met andere AI-systemen?",
         "Vaak ja - bv. de WMS van je 3PL heeft eigen AI. Als die systemen samen besluiten nemen, moeten ze als één AI-systeem beoordeeld worden. BotLease neemt dit mee in de assessment."),
    ],
}


GLOSSARY = {
    "slug": "begrippen",
    "title": "Humanoïde robot terminologie - begrippenlijst | BotLease",
    "meta_desc": "Begrippenlijst humanoïde robotica: van AGV en cobot tot SLAM en VLA-model. 40+ termen kort en helder uitgelegd, inclusief Nederlandse context en lease-implicaties.",
    "keywords": "humanoide robot begrippen, robot terminologie, humanoid robot Nederlandse termen, cobot uitleg, SLAM robot, VLA model uitleg",
    "h1": "Humanoïde robot begrippen - 40+ termen uitgelegd.",
    "tagline": "De woordenlijst die je nodig hebt om gesprekken over humanoid-leasing te kunnen volgen. Kort, helder, met Nederlandse context.",
    "terms": [
        ("AGV", "Automated Guided Vehicle. Wheeled robot die volgens een vaste route rijdt, meestal magneetstrips of QR-codes in de vloer volgt. Geen vervanger van humanoid - andere taak. AGVs zijn voor materiaaltransport over vaste paden, humanoids voor flexibel werk."),
        ("AI Act", "EU Verordening 2024/1689. Reguleert AI-systemen op basis van risiconiveau. Humanoid robots in werkomgevingen vallen meestal onder high-risk. Volledig van toepassing vanaf 2 augustus 2026. Zie de <a href=\"/gids/ai-act-machineverordening\">complete AI-Act gids</a>."),
        ("AMR", "Autonomous Mobile Robot. Wheeled robot die zelfstandig navigeert (via SLAM), in tegenstelling tot AGV. Veelgebruikt in magazijnen voor tote-transport. Goedkoper dan humanoid maar minder flexibel."),
        ("Articulated robot", "Robotarm met meerdere gewrichten (\"joints\"). Klassieke industriële robots zoals ABB IRB, KUKA. Geen humanoid maar wel onderdeel van veel humanoid-armen."),
        ("Battery swap", "Hot-swapping van batterij zonder stilstand. Belangrijk voor 24/7 operatie. UBTECH Walker S2 en Apptronik Apollo ondersteunen dit; Unitree-modellen meestal niet."),
        ("Bipedal", "Tweebenig. Echte humanoids zijn bipedal (G1, H1-2, Apollo, Walker S2). Wheeled humanoids (TIAGo Pro, Reachy 2) hebben benen-loos onderlichaam."),
        ("CE-markering", "EU-conformiteitsmarkering voor producten. Verplicht voor robots in EU. Vanaf 2027 vereist conformiteit met de nieuwe Machineverordening 2023/1230."),
        ("Cobot", "Collaborative robot - robot ontworpen om naast mensen te werken zonder veiligheidshek. Vereist kracht-feedback. NEURA 4NE-1 is een humanoid cobot. Universal Robots UR-serie is een arm-cobot."),
        ("Conformity assessment", "Procedure waarbij een onafhankelijke partij toetst of een product voldoet aan EU-regelgeving (AI-Act, Machineverordening). Vereist vóór deployment van high-risk humanoids."),
        ("Cycle time", "Tijd die een robot nodig heeft voor één taakcyclus. Voor humanoids veel minder voorspelbaar dan voor armrobots - afhankelijk van object-herkenning, planning, motoriek."),
        ("Deployer", "Onder AI-Act: organisatie die een AI-systeem gebruikt voor professionele doeleinden. Bij humanoid-lease ben jij (de gebruiker) de deployer, BotLease + fabrikant zijn provider."),
        ("DoF", "Degrees of Freedom - aantal onafhankelijke bewegingsassen. Een mens heeft ~244 DoF. Unitree G1 heeft 23-43 DoF. Apollo heeft 38. Hogere DoF = meer veelzijdigheid maar ook meer complexiteit."),
        ("Embodied AI", "AI die belichaamd is in een fysiek lichaam (robot) en leert door interactie met de echte wereld. Tegenovergesteld van pure software-AI zoals LLMs."),
        ("End-effector", "Het \"hand\" of \"gereedschap\" aan het einde van een robotarm. Humanoid-handen zijn typisch 4-5 vingerig, soms simpele grippers."),
        ("EU AI Office", "Nieuwe EU-instantie in Brussel die de AI-Act handhaaft. Operationeel sinds februari 2025. Ontvangt meldingen van incidenten en uitvaardigt boetes."),
        ("Fleet learning", "Robots delen wat ze leren onderling. NEURA's \"Neuraverse\" en Hugging Face's \"LeRobot\" zijn voorbeelden. Maakt humanoids elke maand slimmer zonder lokale her-training."),
        ("Force control", "Methode waarbij de robot kracht voelt en daarop reageert (vs. positiecontrole, waarbij hij blind een traject volgt). Vereist voor cobot-gedrag. Apptronik Apollo is bekend om zijn force-control."),
        ("Gait", "Loopbeweging van een bipedal robot. \"Natural gait\" is een term die EngineAI populair heeft gemaakt - soepele, menselijke beweging via neural networks i.p.v. klassieke planning."),
        ("GDPR / AVG", "Algemene Verordening Gegevensbescherming. Reguleert dataverwerking inclusief camera- en sensordata van robots. Vereist verwerkersovereenkomst (DPA) per klant."),
        ("Gripper", "Het mechanisme dat een object vasthoudt. Humanoid-grippers zijn typisch parallelle vingers (2-finger) of antropomorfe handen (5-finger)."),
        ("High-risk AI", "AI-Act classificatie voor systemen die fundamentele rechten of veiligheid kunnen beïnvloeden. Vrijwel alle humanoid-deployments in werkomgevingen vallen hieronder. Vereist conformity assessment + ongoing compliance."),
        ("Humanoid Robot", "Robot met een mensachtige vorm: twee armen, hoofd, en typisch twee benen of een mobiele basis. Bedoeld om in menselijke werkomgevingen te functioneren zonder dat de omgeving aangepast hoeft."),
        ("Imitation learning", "AI-techniek waarbij robots taken leren door menselijke demonstraties (vaak via VR-bediening) na te bootsen. Pollen Reachy 2 is hier sterk in."),
        ("Joint torque", "Draaikracht in een robotgewricht, gemeten in Newtonmeter (N·m). Hogere torque = sterkere robot. Unitree H2 heeft 360 N·m per gewricht - fors voor zijn formaat."),
        ("Kitting", "Het verzamelen van componenten voor latere assemblage. Veel humanoid-pilots in productie focussen hierop omdat het taakgericht is maar geen vaste jig vereist."),
        ("LIDAR", "Light Detection And Ranging. Laser-scanner voor afstandsmeting. EngineAI SE01 heeft 360° LIDAR (\"Engine Sense\"). Veel humanoids gebruiken alternatief cameras + depth sensors."),
        ("Machineverordening", "EU Verordening 2023/1230. Vervangt de oude Machinerichtlijn 2006/42/EG vanaf 20 januari 2027. Nieuwe eisen voor cybersecurity en AI-software-veiligheid."),
        ("MES", "Manufacturing Execution System. Software die productieprocessen orkestreert. Humanoids in productie moeten hier mee koppelen - meestal via OPC-UA."),
        ("ONNX", "Open Neural Network Exchange. Standaard formaat voor AI-modellen. Veel humanoid-fabrikanten gebruiken ONNX voor model-deployment op de robot."),
        ("Operational lease", "Lease-vorm waarbij eigendom bij de lessor (BotLease) blijft. Onderscheid van financial lease, waar het economische risico bij de huurder ligt. Voor humanoids vrijwel altijd operational."),
        ("OPC-UA", "Open Platform Communications Unified Architecture. Industriële communicatiestandaard. Humanoids in productie koppelen meestal via OPC-UA aan MES/SCADA."),
        ("Pick and place", "Robottaak: object oppakken en ergens anders neerzetten. Klassiek voor armrobots, lastiger voor humanoids vanwege vrijheid in bewegingstrajecten."),
        ("Provider (AI-Act)", "Onder AI-Act: organisatie die een AI-systeem ontwikkelt of in EU op de markt brengt. Fabrikant + BotLease zijn beide provider voor lease-modellen."),
        ("RaaS", "Robots as a Service. Lease-vorm waarbij je per uur of per taak betaalt i.p.v. vast per maand. Agility verkoopt Digit alleen als RaaS in de VS. BotLease biedt vooral klassieke maandlease."),
        ("ROS / ROS 2", "Robot Operating System. Open-source softwareraamwerk voor robots. PAL Kangaroo + TIAGo zijn ROS-native - voordeel voor universiteiten/labs die ROS-stack al hebben."),
        ("Sim-to-real", "AI-training in simulatie, daarna deployment op echte robot. Veel humanoid-fabrikanten gebruiken NVIDIA Isaac voor sim-to-real training."),
        ("SLAM", "Simultaneous Localization And Mapping. Techniek waarmee robots autonoom in een ruimte navigeren zonder vooraf gemaakte kaart. Vereist voor humanoid-deployment in onbekende ruimtes."),
        ("Swap-SLA", "Service Level Agreement voor vervanging bij defect. BotLease garandeert vervangende unit binnen 24u op locatie. Als we de SLA missen: dagvergoeding van €100/dag."),
        ("Teach-in", "Programmeren van een robot door hem fysiek de beweging voor te doen. Voor humanoids meestal via VR-bediening (Pollen Reachy 2) of via demonstratie via camera (NEURA)."),
        ("Tote", "Plastic bak voor magazijn-gebruik. Standaard formaten 40×60 cm of 60×40 cm. Humanoid-pick-place richt zich meestal op tote-handling."),
        ("VLA-model", "Vision-Language-Action model. AI dat camerabeelden + taalcommando's combineert tot fysieke acties. State-of-the-art voor humanoid intelligentie - RT-2, OpenVLA, NVIDIA GR00T."),
        ("WMS", "Warehouse Management System. Software die magazijnprocessen orkestreert. Voor 3PL-deployments koppelt de humanoid hieraan - typisch via REST API of OPC-UA."),
        ("VR-teleop", "Virtual Reality teleoperation. Mens bestuurt robot via VR-headset, robot leert van die demonstraties. Gebruikt voor imitation learning en remote support."),
    ],
}


ABOUT = {
    "slug": "over",
    "title": "Over BotLease | humanoid-robot leasemaatschappij",
    "meta_desc": "BotLease is opgericht in 2026 in Amsterdam (KvK 95943420). Wij maken humanoïde robots toegankelijk voor het Nederlandse MKB via all-in operational lease - geen vendor lock-in, onafhankelijk advies, EU-first.",
    "keywords": "BotLease over ons, BotLease team, humanoid robot bedrijf Nederland, BotLease Eindhoven, robot leasemaatschappij Nederland",
    "h1": "Over BotLease.",
    "tagline": "Wij maken humanoïde robots toegankelijk voor het Nederlandse MKB. Geen vendor lock-in. Onafhankelijk advies. EU-first.",
    "sections": [
        {
            "id": "missie",
            "h": "Onze missie",
            "body": [
                "De wereld gaat veranderen. Humanoïde robots verschuiven van labdemo's naar echte productievloeren - Mercedes, BMW, Foxconn, Bosch en BYD zetten ze inmiddels in op industriële schaal. De volgende stap is dat ze breed beschikbaar komen voor de rest van de economie: logistiek, zorg, hospitality, productie, retail.",
                "Lease heeft zich daarvoor al decennia bewezen in andere sectoren - van bedrijfswagens en CNC-machines tot medische apparatuur en IT-infrastructuur. Het patroon is steeds hetzelfde: een nieuwe, dure activaklasse wordt pas écht bruikbaar voor een brede markt zodra iemand de financiering, het onderhoud en het restwaarde-risico van de eindgebruiker overneemt. Datzelfde model brengen wij naar humanoïde robotica.",
                "Onze missie: humanoïde robotica toegankelijk maken voor organisaties binnen Europa - ongeacht omvang of sector. Een werkgever hoeft niet te kiezen tussen \"miljoenen-deal met de fabrikant\" of \"niets\". Lease, swap-SLA en ingebouwde compliance (CE + EU AI-Act) zijn het pad daartussen. Eén maandfactuur, een werkende robot, geen vendor lock-in.",
            ],
        },
        {
            "id": "waarom-wij",
            "h": "Waarom BotLease en niet rechtstreeks bij de fabrikant?",
            "body": [
                "Drie redenen:",
                "<ul><li><b>Geen vendor lock-in.</b> Unitree heeft alleen Unitree. Apptronik heeft alleen Apollo. Wij hebben 15 modellen van 7 fabrikanten - we adviseren wat past, niet wat we verkopen.</li><li><b>Lokale support.</b> Onze workshop staat in Eindhoven. Een defecte robot is er binnen 24 uur uit en een vervangende staat klaar. Geen container uit Shenzhen die 6 weken duurt.</li><li><b>EU AI-Act + Machineverordening compliance.</b> Wij dragen de juridische last als provider. Fabrikanten in China of Texas snappen EU-regelgeving niet altijd. Wij wel - zie onze <a href=\"/gids/ai-act-machineverordening\">AI-Act gids</a>.</li></ul>",
            ],
        },
        {
            "id": "methodologie",
            "h": "Hoe wij robots beoordelen",
            "body": [
                "Wij testen elke robot voor we hem in de catalogus opnemen. Vier criteria:",
                "<ul><li><b>Bewezen field-use.</b> Niet \"demo op IFA\". Wel \"100+ uur productie bij echte klant\". Daarom staat Sanctuary Phoenix niet in onze catalog: alleen prototypes.</li><li><b>EU-leverbaar.</b> Niet \"komt eraan in 2027\" - we verkopen geen vaporware. Apollo en Figure staan op onze <a href=\"/robots#waitlist\">wachtlijst</a>, niet in de hoofdcatalog.</li><li><b>Compliance-pad helder.</b> Voor non-EU modellen (Unitree, UBTECH) moet er een werkend pad zijn naar CE + AI-Act conformiteit. Voor EU-modellen is dit baked-in.</li><li><b>Reële prijs.</b> Wat de fabrikant zegt minus de reality-check. Pollen Reachy 2 \"officieel\" $70k, wij betalen meer omdat we per-unit kopen i.p.v. fleet.</li></ul>",
                "Lees onze <a href=\"/methodologie\">volledige methodologie</a> voor de details - inclusief hoe we lease-prijzen berekenen en welke risico's we niet meelopen.",
            ],
        },
        {
            "id": "ontstaan",
            "h": "Hoe BotLease is ontstaan",
            "body": [
                "BotLease begon niet als robotica-bedrijf. Oprichter Thomas Vedder werkte tussen 2022 en 2025 aan conversational AI projecten - chatbots, taalmodel-deployments, klantenservice-automatisering voor het Nederlandse MKB. Het patroon dat hij steeds terugzag: AI-technologie werd commercieel volwassen jaren voordat het MKB er toegang toe kreeg. Eerst kregen alleen enterprise-klanten met grote IT-budgetten de nieuwe tools. Pas later - vaak 2-3 jaar later - werd het toegankelijk voor bedrijven met 10-200 medewerkers.",
                "In 2025 herhaalde dat patroon zich voor humanoïde robotica. Apptronik tekende contracten met Mercedes-Benz Sindelfingen. Figure AI deployde robots bij BMW Spartanburg. UBTECH startte mass production met BYD en Foxconn. NEURA Robotics ging in productie met Bosch. Dezelfde dynamiek: enterprise eerst, MKB jaren later (of nooit, zonder tussenpersoon).",
                "BotLease is opgericht om die gap te dichten. Niet door zelf humanoids te bouwen - maar door als onafhankelijke lease-bemiddelaar de relaties, financiering, compliance en service-stack te leveren waar fabrikanten geen tijd voor hebben voor het Nederlandse MKB.",
                "De financiële en operationele kant van die service-stack komt niet uit de lucht vallen: het kernteam heeft jarenlange ervaring bij enkele van de grootste leasemaatschappijen van Europa, gespecialiseerd in lease van bedrijfsmiddelen. Restwaarde-modellen, swap-SLA's, end-of-term scenario's, compliance-administratie - patronen die in volwassen lease-markten al decennia werken, vertaald naar een nieuwe activaklasse.",
            ],
        },
        {
            "id": "team",
            "h": "Het team",
            "body": [
                "<b>Thomas Vedder - Oprichter.</b> Achtergrond in conversational AI, taalmodellen en MKB-software. Werkte tussen 2022-2025 aan klant-AI projecten voor Nederlandse bedrijven (zie ook <a href=\"https://heymilo.nl\">Milo</a>, BotLease's consumenten-AI zusterproduct). Verantwoordelijk voor strategie, klant-intake, partner-relaties en operationele service.",
                "<b>Multidisciplinair adviseurs-netwerk.</b> BotLease is klein van omvang, breed in expertise. Adviseurs uit:",
                "<ul><li><b>AI / Machine Learning.</b> Praktische ervaring met conversational AI, LLM-deployments en multimodale modellen. Helpt bij het selecteren van robots waarvan de softwarestack betrouwbaar is - niet alleen demo-magic.</li>"
                "<li><b>Gedragswetenschap / human factors.</b> Hoe medewerkers en robots samenwerken op de werkvloer; wat acceptatie vraagt; hoe je een pilot ontwerpt zodat hij representatief is voor productie.</li>"
                "<li><b>Robotica &amp; industrial automation.</b> ROS-engineering, fleet-ops, MES-integratie. Bij elke deployment zorgen voor passende integratie in bestaande IT.</li>"
                "<li><b>Industriële veiligheid &amp; CE-trajecten.</b> Machineverordening 2023/1230, ISO 10218 / EN ISO 13482 - geregeld via gecertificeerde safety-engineers waar nodig.</li>"
                "<li><b>Operational leasing.</b> Jarenlange ervaring bij enkele van Europa's grootste leasemaatschappijen, specifiek in lease van bedrijfsmiddelen. Brengt contractvormen, restwaarde-modellen en swap-SLA's mee die in volwassen lease-markten al decennia bewezen zijn - nu toegepast op humanoïde robotica.</li></ul>",
                "Klein team, breed netwerk. Geen exclusieve fabrikantsrelatie - we vergelijken onafhankelijk.",
                "Voor pers- of analist-aanvragen: <a href=\"mailto:hallo@botlease.nl\">hallo@botlease.nl</a>. KvK 95943420, gevestigd in Amsterdam.",
            ],
        },
        {
            "id": "kvk-trust",
            "h": "Bedrijfsgegevens",
            "body": [
                "<ul style='line-height:1.85'>"
                "<li><b>Statutaire naam:</b> BotLease (eenmanszaak)</li>"
                "<li><b>KvK-nummer:</b> 95943420 (Kamer van Koophandel Amsterdam)</li>"
                "<li><b>Vestiging:</b> Amsterdam, Noord-Holland, Nederland</li>"
                "<li><b>Email:</b> <a href=\"mailto:hallo@botlease.nl\">hallo@botlease.nl</a></li>"
                "<li><b>Website:</b> botlease.nl</li>"
                "<li><b>Service-gebied:</b> Nederland (België en Duitsland-grens op aanvraag)</li>"
                "<li><b>Compliance:</b> EU AI-Act Reg. 2024/1689 + Machineverordening 2023/1230 per deployment beoordeeld</li>"
                "<li><b>Verzekering:</b> WA tot €2,5M + casco per geleased asset</li>"
                "<li><b>Algemene voorwaarden:</b> beschikbaar op aanvraag voor due-diligence trajecten</li>"
                "</ul>",
            ],
        },
    ],
}


METHODOLOGY = {
    "slug": "methodologie",
    "title": "Methodologie - robot-evaluatie + lease-prijzen | BotLease",
    "meta_desc": "Hoe wij robots evalueren, lease-prijzen berekenen en risico's beheren. Inclusief Swap-SLA voorwaarden, prijsformule, en evaluatiecriteria voor opname in onze catalogus.",
    "keywords": "BotLease methodologie, hoe humanoid lease berekend, Swap-SLA voorwaarden, BotLease risico management, robot evaluatie criteria",
    "h1": "Methodologie - hoe wij werken.",
    "tagline": "Transparantie over hoe wij robots evalueren, prijzen bepalen, en risico's dragen. Geen black box.",
    "sections": [
        {
            "id": "evaluatie",
            "h": "Hoe wij een robot evalueren voor opname",
            "body": [
                "Voordat een model in onze catalogus komt, doorloopt het een 6-staps evaluatie:",
                "<ol><li><b>Marktleverbaarheid.</b> Is er een EU-distributeur of directe shop met &lt;12 weken levertijd? Zo nee: niet opgenomen of als \"wachtlijst\" gemarkeerd.</li><li><b>Documentatie-check.</b> Heeft de fabrikant CE-certificaten, technische documentatie, en een conformity-assessment pad voor AI-Act? Zo nee: alleen op wachtlijst.</li><li><b>Hands-on pilot.</b> Wij leasen of kopen 1-2 units en draaien minimaal 30 dagen in een echte werkomgeving (typisch ons eigen Eindhoven HQ of bij een early-adopter klant).</li><li><b>Service-pad.</b> Kunnen wij onderdelen krijgen, reparaties uitvoeren, en software-updates ontvangen voor minimaal 5 jaar? Zo niet: niet opgenomen.</li><li><b>Prijsmodel.</b> Wat is de werkelijke total cost over 36 mnd? Inclusief onderdelen, retrofit, AI-Act assessment. Hieruit volgt de leaseprijs.</li><li><b>Risico-inschatting.</b> Wat is de kans op productlijn-stopzetting, support-uitval, of verandering in distributie-strategie? Hoog risico = hogere marge of niet opgenomen.</li></ol>",
            ],
        },
        {
            "id": "prijsformule",
            "h": "Lease-prijs formule",
            "body": [
                "Geheim klein recept (waarom geheim? niet - zie hier):",
                "<b>Maandprijs = (Aanschafprijs / 36) + (Aanschafprijs × 0,25 / 12) + (Aanschafprijs × 0,08 / 12) + Marge.</b>",
                "<ul><li>Aanschafprijs / 36: lineaire afschrijving over 36 maanden.</li><li>×0,25/12: 25% jaarlijkse service+onderdelen-reserve = 2,08%/mnd.</li><li>×0,08/12: 8% jaarlijkse verzekering = 0,67%/mnd.</li><li>Marge: typisch 30% bovenop bovenstaande basis-kost.</li></ul>",
                "Voor een €20.000 robot komt dat neer op: €556 (afschrijving) + €417 (service) + €133 (verzekering) = €1.106 basis. Plus 30% marge = €1.438. Wij ronden naar beneden af op €890/mnd om aantrekkelijk te zijn - verlies op marge i.p.v. op klant.",
                "<b>Volume-korting:</b> 3+ units = -8%. 10+ units = -15%. Per-unit marge daalt maar absoluut volume compenseert.",
                "<b>Korter contract:</b> 24 maanden = +7%. 12 maanden = +15%. Reden: snellere afschrijving over kortere termijn.",
            ],
        },
        {
            "id": "swap-sla",
            "h": "Swap-SLA - wat beloven we precies",
            "body": [
                "Onze Swap-SLA: bij defect of storing langer dan 4 uur, vervangende unit binnen 24 uur op locatie. Logistiek vanaf Eindhoven workshop.",
                "<b>Service-niveau:</b>",
                "<ul><li><b>P1 (productie-stop):</b> respons binnen 30 min, technicus on-site of swap binnen 24u.</li><li><b>P2 (degraded):</b> respons binnen 2 uur, fix of swap binnen 48u.</li><li><b>P3 (operationeel met workaround):</b> respons binnen 8 uur, fix binnen 5 werkdagen.</li></ul>",
                "<b>Dekkingsgebied:</b> heel Nederland binnen 24u, België/Duitsland-grens binnen 36u.",
                "<b>Wat als we de SLA missen?</b> Dagvergoeding van €100/dag tot we de SLA halen. Dit is geen credit op je leaseprijs maar een fysieke uitbetaling.",
                "<b>Exclusies:</b> schade door verkeerd gebruik (buiten werkzone, oneigenlijke taken), opzettelijke schade, force majeure (oorlog, pandemie, ramp), schade door derden (bv. heftruck rijdt robot omver). Allemaal in de lease-overeenkomst gedefinieerd.",
            ],
        },
        {
            "id": "risicos",
            "h": "Welke risico's dragen wij wel - en welke niet",
            "body": [
                "<b>Wel:</b> restwaarde-risico (jij krijgt geen factuur als de robot in 3 jaar 90% in waarde daalt), defect-risico (wij vervangen), software-update risico (wij houden bij), compliance-risico (wij verzorgen AI-Act assessment).",
                "<b>Niet:</b> ROI-risico (wij garanderen geen ROI; jij beoordeelt of de robot voor jou rendabel is - pilot is bedoeld om dit te testen), opzettelijke schade (verzekering pakt geen vandalisme), force majeure, lock-in-risico (na 12 mnd kan je elke maand stoppen, wij kunnen niet 36 mnd vasthouden).",
                "<b>Speciaal voor wachtlijst-modellen:</b> als een Apollo of Figure niet in 2027 leverbaar komt, krijg je je reservation-fee (typisch €1.500) terug + 20% bonus. Wij dragen dat risico, jij niet.",
            ],
        },
        {
            "id": "transparantie",
            "h": "Transparantie waar mogelijk",
            "body": [
                "Wij publiceren onze prijsformule (zie boven), onze evaluatie-criteria (zie boven), en onze service-niveaus (zie boven). Dat is niet standaard in lease-industrie - Pon en Athlon doen dit niet.",
                "Wat we niet publiceren: inkoopprijzen per fabrikant (NDA's), individuele klantcontracten (vertrouwelijkheid), en specifieke marges per model (commercieel gevoelig). Voor due diligence op enterprise-deals: <a href=\"mailto:hallo@botlease.nl\">vraag een onder NDA</a>.",
            ],
        },
    ],
}


COSTS_PAGE = {
    "slug": "kosten",
    "title": "Wat kost een humanoïde robot leasen? Calculator + uitleg | BotLease",
    "meta_desc": "Bereken de exacte leaseprijs van 15 humanoïde robotmodellen. Vergelijk koop vs lease over 36 maanden inclusief installatie, onderhoud, verzekering. Eerlijke prijzen vanaf €290/maand.",
    "keywords": "humanoide robot kosten, humanoide robot prijs Nederland, robot lease calculator, hoeveel kost humanoid robot, robot leasen kosten",
    "h1": "Wat kost een humanoïde robot leasen?",
    "tagline": "Eerlijke prijzen - bereken hieronder de exacte kosten voor jouw situatie. Inclusief vergelijking koop vs lease.",
}
