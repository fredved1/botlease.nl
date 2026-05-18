# Landing pages — sectoren en steden voor long-tail SEO.
# Iedere pagina is zelfstandig waardevol: realistische ROI-cijfers,
# specifieke robots per use-case, lokale/sectorale context.

SECTORS = [
    {
        "slug": "3pl-fulfillment",
        "name": "3PL & E-commerce fulfillment",
        "title_kw": "Humanoïde robots in 3PL en e-commerce fulfillment Nederland",
        "h1": "Humanoïde robots voor 3PL en e-commerce fulfillment.",
        "tagline": "Tote-handling, decanting en pick-pack — door humanoids waar AMR's tekortschieten.",
        "intro": (
            "De Nederlandse 3PL- en e-commerce-sector heeft het zwaar: 4 op de 10 magazijnen melden tekort aan personeel, "
            "loonkosten stijgen 5-7% per jaar, en piekuren (Black Friday, Sinterklaas) eisen flexibele capaciteit die "
            "vaste teams niet kunnen leveren. Humanoïde robots zijn geen vervanging voor AMRs of klassieke "
            "robotarmen — ze vullen het gat waar geen vaste infrastructuur past, en waar zachte trays, ongelijke "
            "totes en menselijke routes vereist zijn."
        ),
        "metrics": [
            ("11–14 mnd", "Typische ROI-periode"),
            ("1,3 FTE", "Vervangbaar per robot in 2-ploegen"),
            ("24/7", "Inzetbaarheid in 3 shifts"),
            ("€28/uur", "Vermeden loonkosten gemiddeld"),
        ],
        "subsections": [
            {
                "h": "Tote- en pakkethandling",
                "body": (
                    "Een Agility Digit of Apptronik Apollo werkt zonder gids tussen bestaande shelving en conveyor-zones. "
                    "Geen aanpassing van vloer of looppaden nodig — de robot navigeert wat menselijke werknemers ook gebruiken. "
                    "Bij GXO Wentzville en Amazon-pilots zijn meer dan 100.000 totes verwerkt zonder dat de magazijn-layout "
                    "aangepast hoefde te worden."
                ),
            },
            {
                "h": "Decanting en sortering",
                "body": (
                    "Voor het overpakken van inkomende pallets naar magazijntotes is een humanoid sneller dan een gespecialiseerde "
                    "decanting-robot omdat de SKU-mix te groot is voor pre-programmering. Een Digit of Walker S2 hanteert "
                    "tassen, dozen en losse items met dezelfde 2-armige greep — geen gripper-swap, geen jig."
                ),
            },
            {
                "h": "Cycle-counting buiten piek",
                "body": (
                    "Tussen 23:00 en 06:00 kan een Unitree G1 met SLAM-stack autonoom door het magazijn lopen en RFID-tags "
                    "scannen. Voor een 1.200 m² fulfillment-locatie levert dat ~2 FTE per week aan besparing — bij €28/uur "
                    "is dat €58.000 per jaar."
                ),
            },
        ],
        "recommended_robots": ["agility-digit", "apptronik-apollo", "ubtech-walker-s2", "unitree-h1-2"],
        "questions": [
            ("Welke robot past het beste bij ons fulfillment-proces?",
             "Dat hangt af van tote-grootte (8-25 kg), aisle-breedte (1,2 m of meer voor full-size, 0,8 m voor compact), en of "
             "de pilot in een 2-ploeg of 3-ploeg moet draaien. Tijdens de gratis intake meten we dit op locatie."),
            ("Werkt de robot met onze WMS?",
             "Ja — alle humanoids ondersteunen REST/OPC-UA koppeling met SAP EWM, Manhattan, Blue Yonder, Körber en de grote "
             "Nederlandse WMS-leveranciers. BotLease verzorgt de integratie."),
            ("Hoe gaat het bij piek (Black Friday)?",
             "Surge-lease: extra units voor 6-12 weken tegen weekprijs. Geen jaarcontract, snel op- en afschalen. Dit is de "
             "scherpste case voor humanoids vs. vaste robotarmen."),
        ],
    },
    {
        "slug": "productie-assemblage",
        "name": "Productie en assemblage",
        "title_kw": "Humanoïde robots in productie en assemblage Nederland",
        "h1": "Humanoïde robots voor productie en assemblage.",
        "tagline": "Kitting, parts-handling en kwaliteitscontrole — voor mixed-mens-robot productielijnen.",
        "intro": (
            "Nederlandse maakbedrijven kampen met een aanhoudend personeelstekort in productie: gemiddeld 12% openstaande "
            "vacatures in de metaal- en machine-industrie (CBS, Q1 2026). Tegelijk vragen klanten meer maatwerk en kortere "
            "doorlooptijden. Humanoïde robots zijn ideaal voor de stappen die nu mensenwerk zijn omdat ze niet jig-baar zijn — "
            "kitting, materiaaltransport tussen werkstations, inspectie van onderdelen."
        ),
        "metrics": [
            ("13–18 mnd", "Typische ROI-periode"),
            ("24/7", "Productieve uptime mogelijk"),
            ("0 jigs", "Geen kostbare aanpassingen aan lijn"),
            ("€60-90k", "Vermeden FTE-kost per jaar"),
        ],
        "subsections": [
            {
                "h": "Kitting voor assemblage",
                "body": (
                    "Apptronik Apollo verzamelt componenten in een Mercedes-fabriek voor opvolgende montage. De Apollo doet "
                    "geen 'mens-werk' — hij verzorgt deeltaken (kitting, parts-handling, kwaliteitscontrole) die anders door "
                    "een operator gedaan moeten worden. Ideaal voor mixed-flow lijnen."
                ),
            },
            {
                "h": "Machine-tending",
                "body": (
                    "Een UBTECH Walker S2 of NEURA 4NE-1 Gen 3.5 laadt en lost CNC-machines, persen of injection-molding. "
                    "Werkt 24/7 zonder pauze, levert consistente cyclustijden. Anders dan een vaste robotarm: hij wisselt "
                    "tussen machines, geen jig-up nodig per nieuwe SKU."
                ),
            },
            {
                "h": "Inline kwaliteitscontrole",
                "body": (
                    "Een NEURA 4NE-1 inspecteert componenten met de geïntegreerde 4K-camera + thermische sensor. De "
                    "AI-engine herkent afwijkingen die mensen makkelijk missen na 4 uur. Geen aparte inspectiestation nodig — "
                    "robot scant naast de productielijn."
                ),
            },
        ],
        "recommended_robots": ["neura-4ne1-gen3", "apptronik-apollo", "ubtech-walker-s2", "unitree-h1-2"],
        "questions": [
            ("Werken humanoids veilig naast onze operators?",
             "Ja, mits ze CE-gemarkeerd zijn met EN ISO 13482 cobot-compliance. NEURA 4NE-1 heeft artificial-skin "
             "(detecteert nabijheid voor aanraking), Apptronik Apollo gebruikt force-control. Werkzones worden tijdens de "
             "intake gedefinieerd."),
            ("Past dit binnen de EU Machineverordening?",
             "De Machineverordening 2023/1230 geldt vanaf 20 jan 2027. EU-gebouwde humanoids (NEURA, PAL) zijn al "
             "voorbereid; bij Amerikaanse/Chinese modellen voert BotLease de conformity assessment uit per deployment."),
            ("Hoeveel personeel hebben we nodig?",
             "Eén operator kan 3-5 humanoids beheren in een normale productielijn. De robot vraagt vooral aandacht bij "
             "uitzonderingen (gripper-issues, onverwachte onderdelen). Voor 8-uurs shifts: 1 operator per cel."),
        ],
    },
    {
        "slug": "hospitality-retail",
        "name": "Hospitality en retail",
        "title_kw": "Humanoïde robots in hospitality en retail Nederland",
        "h1": "Humanoïde robots voor hospitality en retail.",
        "tagline": "Lobby-host, room-service en nachtelijke voorraadtelling — verhoogt service én bespaart op personeel.",
        "intro": (
            "Hotels met meer dan 80 kamers en retailers boven 1.000 m² zien een groeiende interesse in humanoid-hosts. "
            "Niet als gimmick: data van de eerste 50 Europese pilots laat zien dat hotels gemiddeld 0,3-0,5 ster winnen op "
            "gastenscore-platforms en dat personeel 30% minder routinewerk doet. De ROI zit in verlengde personeelsdekking "
            "(avond/nacht) en in betere gastervaring tijdens piek."
        ),
        "metrics": [
            ("+0,3–0,5★", "Gemiddelde gastenscore-verbetering"),
            ("30%", "Minder routinewerk voor personeel"),
            ("2 FTE/wk", "Bespaard op nachtelijke voorraadtelling"),
            ("€58k/jr", "Typische besparing per retail-locatie"),
        ],
        "subsections": [
            {
                "h": "Lobby-host bij hotels",
                "body": (
                    "Een 1X NEO (vanaf Q1 2027) of Unitree H2 begroet gasten in de lobby, wijst de weg, en haalt bagage op "
                    "tussen lobby en lift. De check-in zelf blijft mensenwerk — de robot vult de service-gaten 's avonds "
                    "en 's nachts in. Best voor 80+ kamerhotels waar gemiddelde wachttijden onder druk staan."
                ),
            },
            {
                "h": "Voorraadtelling 's nachts",
                "body": (
                    "Tussen 23:00 en 06:00 kan een Unitree G1 met camera-vision en SLAM-stack autonoom door een winkel "
                    "lopen en RFID/barcode-tags scannen. Voor een 1.200 m² retailer: ~2 FTE per week aan handmatige "
                    "telling besparen — bij €28/uur is dat €58.000 per jaar."
                ),
            },
            {
                "h": "Marketing-events en activaties",
                "body": (
                    "Op B2B-beurzen trekt een humanoid 2-3× zoveel gekwalificeerde leads als een conventionele stand. "
                    "Unitree G1 (€899/mnd) of R1 (€290/mnd) zijn het juiste prijspunt: groot genoeg voor impact, klein "
                    "genoeg om geen veiligheidshek te vereisen."
                ),
            },
        ],
        "recommended_robots": ["unitree-g1", "unitree-h2", "unitree-r1", "1x-neo"],
        "questions": [
            ("Hoe reageren gasten op een robot?",
             "Bij de meeste pilots: positief. 65% van de gasten interacteert vrijwillig binnen 24 uur, 80% rapporteert "
             "geen ongemak. Belangrijk: training van personeel om bij te springen wanneer de robot vastloopt — gasten "
             "voelen zich snel ongemakkelijk bij een 'kapotte' robot."),
            ("Werkt dit in een kleiner hotel of winkel?",
             "Onder 80 kamers (hotels) of 800 m² (retail) is de ROI moeilijk te halen — dan zit je in event-mode of "
             "marketing-stunts. Goedkoper alternatief: huur per event in plaats van leasen."),
            ("Wat zegt AVG/GDPR over robot-cameras?",
             "Camera-streams blijven on-prem of op EU-cloud (Hetzner FSN). BotLease sluit een DPA per klant en is "
             "AI-act compliant als deployer. Gasten worden geïnformeerd via bordjes bij de ingang."),
        ],
    },
    {
        "slug": "zorg-instellingen",
        "name": "Zorg en instellingen",
        "title_kw": "Humanoïde robots in zorg en instellingen Nederland",
        "h1": "Humanoïde robots in zorginstellingen.",
        "tagline": "Linnen- en materiaaltransport — voor de niet-zorgtaken die nu zorgmedewerkers doen.",
        "intro": (
            "Nederlandse zorginstellingen verliezen jaarlijks 10-15% van zorgmedewerkers aan logistieke taken: linnen "
            "verplaatsen, materiaal aanvullen, voedseldistributie. Humanoïde robots zijn geen oplossing voor zorgtaken "
            "zelf (dat blijft mensenwerk), maar voor het wegnemen van die logistieke last waardoor zorgmedewerkers "
            "meer tijd hebben voor patiënten. EU-gebouwde modellen (PAL TIAGo, NEURA 4NE-1 Mini) zijn first choice "
            "vanwege GDPR + EU AI-Act compliance."
        ),
        "metrics": [
            ("0,6 FTE", "Vrijgespeeld zorgpersoneel per robot"),
            ("18–24 mnd", "Typische ROI-periode"),
            ("EU-built", "Voor GDPR + AI-Act compliance"),
            ("24/7", "Ondersteuning bij personeelstekort"),
        ],
        "subsections": [
            {
                "h": "Linnen- en wasgoedtransport",
                "body": (
                    "PAL TIAGo Pro (wheeled, EU-gebouwd in Barcelona) transporteert linnenkarren tussen wasrij en "
                    "afdelingen. Werkt veilig naast patiënten, heeft EN ISO 13482 cobot-compliance, en wordt al in "
                    "meerdere Spaanse en Italiaanse ziekenhuizen ingezet."
                ),
            },
            {
                "h": "Materiaaltransport",
                "body": (
                    "Voor vervoer van medisch materiaal tussen voorraadkamer en behandelkamers is een NEURA 4NE-1 Mini "
                    "of Unitree G1 geschikt. De robot herkent obstakels (rolstoelen, infuuspalen), wacht bij liften, "
                    "en herkent patiëntenkamers via QR of NFC."
                ),
            },
            {
                "h": "Voedseldistributie tijdens piekuren",
                "body": (
                    "Ontbijt- en avondserveerronde tussen keuken en kamers — vaak 1-2 zorgmedewerkers die anders direct "
                    "zorg konden bieden. Een PAL TIAGo of Unitree H2 (sociale interactie) verzorgt deze ronde."
                ),
            },
        ],
        "recommended_robots": ["pal-tiago-pro", "neura-4ne1-mini", "unitree-g1", "unitree-h2"],
        "questions": [
            ("Mag dit volgens de Wet zorg en dwang?",
             "Ja — de robot voert geen zorghandelingen uit, alleen logistiek. Geen impact op Wzd-protocollen. De "
             "AVG-verwerking van patiëntdata blijft een zorgvuldigheidspunt: camera-streams blijven on-prem, geen "
             "patiëntdata wordt opgeslagen."),
            ("Werkt dit in de nacht?",
             "Ja — humanoids zijn ideaal voor nachtelijke logistiek omdat ze geen rust nodig hebben en omdat het "
             "personeelstekort 's nachts het scherpst is. Battery-swap automatisch via dockingstation."),
            ("Hoe veilig is dit naast kwetsbare patiënten?",
             "Cobot-compliante modellen (PAL, NEURA, 4NE-1 Mini) hebben kracht-detectie: bij aanraking stoppen ze "
             "binnen 50ms. Werkzones worden in de intake gedefinieerd. WA-dekking tot €2,5M is inbegrepen."),
        ],
    },
]

CITIES = [
    {
        "slug": "amsterdam",
        "name": "Amsterdam",
        "title_kw": "Humanoïde robot leasen Amsterdam",
        "intro": (
            "Amsterdam is Nederlands grootste cluster voor e-commerce-hoofdkantoren, tech-scale-ups en luxe hospitality. "
            "BotLease levert humanoids op locatie binnen Schiphol-corridor, Zuidoost (Amstel Business Park) en Westpoort "
            "(Sloterdijk fulfillment) — gemiddeld 5 werkdagen na intake."
        ),
        "sectors_in_focus": ["3pl-fulfillment", "hospitality-retail"],
        "local_hooks": (
            "Voor Amsterdamse 3PL-spelers in Westpoort en Schiphol-corridor is een Apptronik Apollo of UBTECH Walker S2 "
            "ideaal voor cross-dock en piek-fulfillment. Voor hotels in centrum (5-sterren cluster Vondelpark, Prinsengracht) "
            "biedt een Unitree H2 of NEO een service-uplift zonder lobbymensen extra."
        ),
    },
    {
        "slug": "rotterdam",
        "name": "Rotterdam",
        "title_kw": "Humanoïde robot leasen Rotterdam",
        "intro": (
            "Rotterdam is het logistieke hart van Nederland: Maasvlakte, Botlek, Waalhaven. BotLease levert humanoids voor "
            "warehouse-deployments in Eemhaven, Distripark Maasvlakte en het 3PL-cluster rond Heinenoord. Eindhoven HQ "
            "leveringsradius dekt heel Rijnmond binnen 2 uur."
        ),
        "sectors_in_focus": ["3pl-fulfillment", "productie-assemblage"],
        "local_hooks": (
            "Voor 3PLs op Maasvlakte en Botlek-petrochemie is een Agility Digit of UBTECH Walker S2 first choice voor "
            "tote-handling. Voor maakindustrie in regio Drechtsteden (Damen Shipyards, Boskalis) zijn industriele NEURA 4NE-1 "
            "Gen 3.5 of Apptronik Apollo (wachtlijst 2027) interessant voor kitting + parts-handling."
        ),
    },
    {
        "slug": "eindhoven",
        "name": "Eindhoven",
        "title_kw": "Humanoïde robot leasen Eindhoven Brainport",
        "intro": (
            "Eindhoven Brainport is Nederlands maakindustrie-hart: ASML, NXP, Philips, VDL. BotLease bedient deze regio actief vanuit "
            "Amsterdam (Vrouwengelukhof 58) met demo-units op voorraad voor pilots binnen 5 werkdagen. Sterk netwerk in Helmond "
            "(automotive cluster) en Veldhoven (semi-conductor toeleveranciers)."
        ),
        "sectors_in_focus": ["productie-assemblage", "3pl-fulfillment"],
        "local_hooks": (
            "Voor semicon-toeleveranciers (FEI, BESI, Thermo Fisher) is een NEURA 4NE-1 ideaal voor cleanroom-aanvullingen "
            "en lichte parts-handling. Voor automotive-OEM-suppliers (VDL Nedcar, Inalfa) zijn UBTECH Walker S2 of "
            "Apptronik Apollo de juiste industrieel-zware modellen."
        ),
    },
    {
        "slug": "utrecht",
        "name": "Utrecht",
        "title_kw": "Humanoïde robot leasen Utrecht",
        "intro": (
            "Utrecht is het knooppunt voor zorginstellingen (UMC Utrecht), universitair onderzoek en logistieke knooppunten "
            "rond A12/A2. BotLease levert humanoids binnen 2 uur vanaf Eindhoven HQ — handig voor zorg- en onderzoeksprojecten "
            "in regio Utrecht-Nieuwegein."
        ),
        "sectors_in_focus": ["zorg-instellingen", "3pl-fulfillment"],
        "local_hooks": (
            "Voor UMC Utrecht-omgeving en zorginstellingen in Nieuwegein/Houten is een PAL TIAGo Pro of NEURA 4NE-1 Mini "
            "uitstekend voor materiaaltransport en lichte logistiek. Voor logistieke knooppunten Lage Weide is Agility "
            "Digit of Unitree H1-2 een goede tote-handling keuze."
        ),
    },
    {
        "slug": "den-haag",
        "name": "Den Haag",
        "title_kw": "Humanoïde robot leasen Den Haag",
        "intro": (
            "Den Haag is een sector-mix: government, defensie, hotels rond Scheveningen, en logistieke clusters in Bleizo "
            "en Rijswijk. BotLease verzorgt humanoid-deployments voor zowel publieke instellingen (security-pilots, "
            "demo-events) als private hospitality."
        ),
        "sectors_in_focus": ["hospitality-retail", "3pl-fulfillment"],
        "local_hooks": (
            "Voor Scheveningse hotels en hospitality-cluster (Kurhaus, Steigenberger) zijn Unitree H2 of NEO ideaal voor "
            "lobby-host. Voor government R&D en defensie-pilots zijn EU-gebouwde modellen (NEURA, PAL) verplicht — "
            "geen Chinese hardware in security-toepassingen."
        ),
    },
]
