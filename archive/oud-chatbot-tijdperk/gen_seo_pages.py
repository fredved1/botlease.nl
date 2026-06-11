#!/usr/bin/env python3
"""Generate SEO landing pages for botlease.nl from the tokenised template.

Each page reuses the shared shell (CSS, nav, mobile-patch, footer, JS) and gets
bespoke meta, JSON-LD schema, hero, body, FAQ and CTA. Run from repo root.
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).parent / "frontend"
TEMPLATE = pathlib.Path("/tmp/seo_template.html").read_text(encoding="utf-8")
BASE = "https://botlease.nl"
IMG = "https://botlease.nl/img/robots/apollo.png"
TODAY = "2026-05-29"


def schema_blocks(slug, headline, desc, crumbs, faqs, extra=None):
    url = f"{BASE}/{slug}"
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": headline,
         "description": desc, "image": IMG,
         "datePublished": f"{TODAY}T08:00:00+02:00", "dateModified": f"{TODAY}T08:00:00+02:00",
         "author": {"@type": "Organization", "name": "BotLease Redactie"},
         "publisher": {"@type": "Organization", "name": "BotLease",
                       "logo": {"@type": "ImageObject", "url": "https://botlease.nl/logo.png"}},
         "mainEntityOfPage": {"@type": "WebPage", "@id": url}, "inLanguage": "nl-NL"},
        {"@context": "https://schema.org", "@type": "BreadcrumbList",
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n,
                              "item": f"{BASE}{p}"} for i, (n, p) in enumerate(crumbs)]},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
        {"@context": "https://schema.org", "@type": "WebPage",
         "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".tldr li", "h1", ".tag"]},
         "url": url},
        {"@context": "https://schema.org", "@type": "Organization", "name": "BotLease",
         "url": BASE, "logo": "https://botlease.nl/logo.png",
         "address": {"@type": "PostalAddress", "addressLocality": "Eindhoven", "addressCountry": "NL"}},
    ]
    if extra:
        blocks.insert(2, extra)
    return "\n".join('<script type="application/ld+json">' + json.dumps(b, ensure_ascii=False) + "</script>"
                     for b in blocks)


def hero(crumbs, eyebrow, h1, tag, tldr_items, toc_items):
    crumb_html = ""
    for i, (n, p) in enumerate(crumbs):
        if i < len(crumbs) - 1:
            crumb_html += f'<a href="{p}">{n}</a><span class="sep">/</span>'
        else:
            crumb_html += f'<span>{n}</span>'
    tldr = "".join(f"<li>{x}</li>" for x in tldr_items)
    toc = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in toc_items)
    return (f'    <nav class="crumbs">{crumb_html}</nav>\n'
            f'    <span class="eyebrow">{eyebrow}</span>\n'
            f'    <h1>{h1}</h1>\n'
            f'    <p class="tag">{tag}</p>\n'
            f'    <div class="tldr"><h3>TL;DR</h3><ul>{tldr}</ul></div>\n'
            f'    <div class="toc"><h3>Inhoud</h3><ol>{toc}</ol></div>')


def faq_html(faqs):
    return "".join(f'<div class="faq-item"><h4>{q}</h4><p>{a}</p></div>' for q, a in faqs)


def build(page):
    s = TEMPLATE
    repl = {
        "⟦TITLE⟧": page["title"], "⟦DESC⟧": page["desc"], "⟦OGDESC⟧": page.get("ogdesc", page["desc"]),
        "⟦KEYWORDS⟧": page["keywords"], "⟦CANON⟧": f"{BASE}/{page['slug']}",
        "⟦SCHEMA⟧": schema_blocks(page["slug"], page["headline"], page["desc"],
                                  page["crumbs"], page["faqs"], page.get("extra_schema")),
        "⟦HERO⟧": hero(page["crumbs"], page["eyebrow"], page["h1"], page["tag"],
                       page["tldr"], page["toc"]),
        "⟦BODY⟧": page["body"], "⟦FAQ⟧": faq_html(page["faqs"]),
        "⟦CTA_H3⟧": page["cta_h3"], "⟦CTA_P⟧": page["cta_p"],
    }
    for k, v in repl.items():
        s = s.replace(k, v)
    left = re.findall(r"⟦[A-Z_0-9]+⟧", s)
    assert not left, f"unfilled tokens: {left}"
    out = ROOT / f"{page['slug']}.html"
    out.write_text(s, encoding="utf-8")
    # validate JSON-LD
    n = 0
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        n += 1
        json.loads(m.group(1))
    return out, n


# ───────────────────────── PAGE DATA ─────────────────────────
PAGES = []

# 1. /huren ----------------------------------------------------------------
PAGES.append({
    "slug": "huren",
    "title": "Humanoïde robot huren in Nederland - per maand | BotLease",
    "desc": "Humanoïde robot huren in plaats van kopen: flexibel per maand, all-in vanaf €290/mnd. Verschil tussen huren, leasen en event-verhuur, en wat het kost.",
    "keywords": "humanoide robot huren, humanoid robot huren, robot huren bedrijf, humanoide robot huren per maand, robot huren nederland, humanoide robot inhuren",
    "headline": "Humanoïde robot huren in Nederland: flexibel per maand",
    "crumbs": [("Home", "/"), ("Humanoïde robot huren", "/huren")],
    "eyebrow": "Huren",
    "h1": "Humanoïde robot huren - flexibel, per maand.",
    "tag": "Geen aanschaf, geen lang contract. Huur een werkende humanoïde robot per maand, inclusief installatie, training, onderhoud en vervanging.",
    "tldr": [
        "Een humanoïde robot huren = een werkende robot per maand afnemen zonder hem te kopen - all-in vanaf €290/mnd, inclusief installatie, training, onderhoud, swap-SLA en verzekering.",
        "Verschil met event-verhuur: wij verhuren robots om wérk te doen (logistiek, productie, service), niet als attractie voor een beurs of feest.",
        "Verschil met leasen: huren is korter en flexibeler; operational lease loopt meestal 36 maanden met een lager maandbedrag. Beide off-balance.",
        "Begin met een pilot van 4 weken (€1.500) om de businesscase te bewijzen voordat je je voor langere termijn vastlegt.",
    ],
    "toc": [("wat-is", "1. Wat betekent een humanoïde robot huren?"),
            ("huren-vs", "2. Huren vs leasen vs event-verhuur"),
            ("kosten", "3. Wat kost een humanoïde robot huren?"),
            ("modellen", "4. Welke robots kun je huren?"),
            ("hoe", "5. Hoe werkt het - van intake tot inzet"),
            ("voor-wie", "6. Voor wie is huren interessant?")],
    "body": (
        '<h2 id="wat-is">1. Wat betekent een humanoïde robot huren?</h2>'
        '<p><b>Een humanoïde robot huren betekent dat je een werkende robot per maand afneemt zonder hem te kopen.</b> Je betaalt een vast maandbedrag en BotLease blijft eigenaar en regelt de installatie, training, het onderhoud en de vervanging. Anders dan bij aanschaf draag je geen investering vooraf en geen restwaarde-risico.</p>'
        '<p>Belangrijk onderscheid: er bestaan twee soorten "robot huren" in Nederland. Het ene is <i>event-verhuur</i> - een robot als blikvanger op een beurs of feest, vaak per dag. Het andere - waar BotLease in zit - is het huren van een robot om <i>echt werk</i> te doen: orderpicking, kitting, voorraadtelling, receptie of inspectie. Deze pagina gaat over dat laatste.</p>'
        '<h2 id="huren-vs">2. Huren vs leasen vs event-verhuur</h2>'
        '<p>De termen lopen door elkaar. Zo zitten ze in elkaar:</p>'
        '<table class="cmp"><thead><tr><th>&nbsp;</th><th>Event-verhuur</th><th>Huren (kort)</th><th>Operational lease</th></tr></thead>'
        '<tbody>'
        '<tr><td><b>Doel</b></td><td>Attractie / show</td><td>Werk doen, flexibel</td><td>Werk doen, structureel</td></tr>'
        '<tr><td><b>Termijn</b></td><td>Dag(en)</td><td>Maand tot maand</td><td>36 mnd, daarna maandelijks</td></tr>'
        '<tr><td><b>Maandprijs</b></td><td>Hoog (per dag)</td><td>Iets hoger</td><td>Laagst</td></tr>'
        '<tr><td><b>Inbegrepen service</b></td><td>Beperkt</td><td>All-in</td><td>All-in</td></tr>'
        '<tr><td><b>Past bij</b></td><td>Marketing</td><td>Piek, project, twijfel</td><td>Vaste taak</td></tr>'
        '</tbody></table>'
        '<p>Twijfel je over huren versus structureel leasen? Lees <a href="/robot-as-a-service">hoe Robot-as-a-Service werkt</a> of zet koop en lease naast elkaar in <a href="/vergelijken/lease-vs-koop">lease vs koop</a>.</p>'
        '<h2 id="kosten">3. Wat kost een humanoïde robot huren?</h2>'
        '<p>Bij BotLease huur je all-in: het maandbedrag dekt installatie, een 2-uurs operatortraining, preventief en correctief onderhoud, alle onderdelen, de swap-SLA (vervangende unit binnen 24 uur), WA-verzekering tot €2,5M en 24/7 Nederlandstalige support. De maandbedragen lopen van <b>€290/mnd</b> (<a href="/robots/unitree-r1">Unitree R1</a>, instap) tot <b>€4.490/mnd</b> (<a href="/robots/neura-4ne1-gen3">NEURA 4NE-1 Gen 3.5</a>, industrieel). Een pilot van 4 weken kost €1.500 en krijg je terug bij doorzetten.</p>'
        '<p><a href="/kosten">Bereken het exacte maandbedrag</a> voor jouw situatie met de calculator.</p>'
        '<h2 id="modellen">4. Welke robots kun je huren?</h2>'
        '<p>Alle 15 modellen uit onze catalogus zijn te huur. Populair voor kortere inzet: <a href="/robots/unitree-g1">Unitree G1</a> (R&amp;D, hospitality, voorraadtelling), <a href="/robots/unitree-h2">Unitree H2</a> (service, receptie) en <a href="/robots/pal-tiago-pro">PAL TIAGo Pro</a> (wheeled, ROS-native). Voor industriële inzet: <a href="/robots/ubtech-walker-s2">UBTECH Walker S2</a> en <a href="/robots/neura-4ne1-gen3">NEURA 4NE-1 Gen 3.5</a>. Bekijk de <a href="/robots">volledige catalogus</a> of <a href="/vergelijken">vergelijk modellen</a>.</p>'
        '<h2 id="hoe">5. Hoe werkt het - van intake tot inzet</h2>'
        '<p><b>Intake (gratis):</b> wij komen binnen 5 werkdagen op locatie, meten de werkruimte en kiezen 1-2 passende modellen. <b>Deployment:</b> robot op locatie, veiligheidsanalyse, taakprogrammering en operatortraining. <b>Productie:</b> de robot draait in je echte workflow; wij monitoren op afstand en sturen bij. Wil je daarna langer door, dan gaat het over in een lease - of de robot gaat retour, zonder gedoe.</p>'
        '<h2 id="voor-wie">6. Voor wie is huren interessant?</h2>'
        '<p>Huren past wanneer je flexibiliteit wilt: een seizoenspiek in je <a href="/sectoren/3pl-fulfillment">fulfillment</a>, een tijdelijk project in de <a href="/sectoren/productie-assemblage">productie</a>, of simpelweg twijfel of een humanoïde robot bij je past. Je test zonder grote investering en zonder je voor jaren vast te leggen. Weet je al dat je structureel wilt inzetten, dan is <a href="/robot-as-a-service">leasen (RaaS)</a> goedkoper per maand. <a href="/#contact">Plan een gratis intake</a> en we adviseren onafhankelijk wat past.</p>'
    ),
    "faqs": [
        ("Wat kost het om een humanoïde robot te huren?",
         "Bij BotLease huur je all-in vanaf €290/maand (Unitree R1) tot €4.490/maand (NEURA 4NE-1 Gen 3.5). Het maandbedrag dekt installatie, training, onderhoud, swap-SLA en verzekering. Een pilot van 4 weken kost €1.500."),
        ("Wat is het verschil tussen een humanoïde robot huren en leasen?",
         "Huren is korter en flexibeler (van maand tot maand), leasen loopt meestal 36 maanden met een lager maandbedrag. Beide zijn off-balance en all-in. Voor structurele inzet is leasen goedkoper; voor een piek, project of twijfel is huren handiger."),
        ("Verhuren jullie robots ook voor evenementen of beurzen?",
         "Ons aanbod is gericht op robots die echt werk doen - logistiek, productie, service en inspectie - niet op event-attracties. Voor een korte demonstratie op locatie kunnen we wel een pilot inplannen."),
        ("Hoe snel staat een gehuurde robot op locatie?",
         "Na een gratis intake (binnen 5 werkdagen) start de inzet gemiddeld 10 werkdagen later. De robot is productief vanaf de tweede week."),
        ("Kan ik een gehuurde robot later overnemen of leasen?",
         "Ja. Een huur- of pilotperiode gaat naadloos over in een operational-leasecontract als je structureel wilt inzetten. De pilotkosten verrekenen we dan met de eerste maand."),
    ],
    "cta_h3": "Humanoïde robot huren en uitproberen?",
    "cta_p": "Plan een gratis intake. Wij komen op locatie en adviseren onafhankelijk welk model past.",
})

# 2. /personeelstekort-humanoide-robot ------------------------------------
PAGES.append({
    "slug": "personeelstekort-humanoide-robot",
    "title": "Humanoïde robot tegen personeelstekort - werkt het? | BotLease",
    "desc": "Lost een humanoïde robot het personeelstekort op? Realistische kijk op welke taken robots overnemen, wat het kost per FTE en hoe je in 2026 begint.",
    "keywords": "humanoide robot personeelstekort, robot tegen personeelstekort, robot als arbeidskracht, robot vervangt mensen, humanoide robot arbeidsmarkt, robot uitzendkracht",
    "headline": "Humanoïde robot tegen personeelstekort: realistische inzet in 2026",
    "crumbs": [("Home", "/"), ("Personeelstekort", "/personeelstekort-humanoide-robot")],
    "eyebrow": "Arbeidsmarkt",
    "h1": "Humanoïde robot tegen het personeelstekort.",
    "tag": "Geen sciencefiction en geen massaontslag. Een nuchtere kijk op welke taken een humanoïde robot vandaag overneemt - en wat dat kost per FTE.",
    "tldr": [
        "Een humanoïde robot vervangt geen mens, maar wel repetitieve, zware of onaantrekkelijke taken waar je toch geen personeel voor vindt.",
        "Reken per taak, niet per persoon: een full-size humanoid neemt in twee ploegen ~1,3 FTE aan repeterend werk over voor €3.000-4.500/mnd all-in.",
        "Sterkste businesscase nu: 3PL/fulfillment en productie, waar de arbeidsmarkt het krapst is en het werk het meest gestandaardiseerd.",
        "Begin met een pilot van 4 weken (€1.500): meet bespaarde uren en uptime vóór je opschaalt. Geen investering vooraf, na jaar 1 maandelijks opzegbaar.",
    ],
    "toc": [("realiteit", "1. Lost een robot het personeelstekort op?"),
            ("taken", "2. Welke taken neemt een humanoïde robot over?"),
            ("kosten-fte", "3. Wat kost een robot per FTE?"),
            ("sectoren", "4. Waar is de businesscase het sterkst?"),
            ("mens-robot", "5. Mens én robot, niet mens óf robot"),
            ("starten", "6. Hoe begin je in 2026?")],
    "body": (
        '<h2 id="realiteit">1. Lost een robot het personeelstekort op?</h2>'
        '<p><b>Een humanoïde robot lost het personeelstekort niet op, maar verlicht het wel gericht.</b> Hij neemt repetitief, fysiek zwaar of onaantrekkelijk werk over - precies de functies waar werkgevers in 2026 het moeilijkst personeel voor vinden. Daardoor zet je je schaarse mensen in op werk dat aandacht, oordeel en contact vraagt.</p>'
        '<p>De Nederlandse arbeidsmarkt blijft krap in logistiek, productie en zorg. Tegelijk worden humanoïde robots betaalbaar en betrouwbaar genoeg voor echt werk. Dat snijvlak - krapte plus rijpe techniek - maakt 2026 het jaar waarin de eerste serieuze MKB-inzet rendabel wordt.</p>'
        '<h2 id="taken">2. Welke taken neemt een humanoïde robot over?</h2>'
        '<p>Geschikt: tote- en pakkethandling, kitting en parts-handling, machinebelading, voorraadtelling, nachtelijke inspectie, en logistieke loopjes (bijvoorbeeld linnen of maaltijden rondbrengen in een instelling). Nog niet geschikt: taken met veel uitzonderingen, fijne motoriek onder tijdsdruk, of direct intensief menselijk contact.</p>'
        '<p>De vuistregel: hoe voorspelbaarder en herhaalbaarder de taak, hoe sterker de businesscase. Bekijk concrete toepassingen per <a href="/sectoren">sector</a>.</p>'
        '<h2 id="kosten-fte">3. Wat kost een robot per FTE?</h2>'
        '<p>Reken per taak, niet per persoon. Een full-size humanoid (bijvoorbeeld <a href="/robots/ubtech-walker-s2">UBTECH Walker S2</a>) draait in twee ploegen en neemt zo ~1,3 FTE aan repeterend werk over. Bij een loonkost van €28/uur is 1,3 FTE × 2.080 uur ≈ €76k aan bespaarde loonkosten per jaar. De lease is ~€3.290/mnd (€39.480/jaar) all-in. Netto resultaat: ~€36k per jaar, plus dat je de functie niet meer hoeft te werven.</p>'
        '<p>Een goedkoper model zoals de <a href="/robots/unitree-g1">Unitree G1</a> (vanaf instapprijs) past voor lichtere taken zoals nachtelijke voorraadtelling. <a href="/kosten">Reken jouw situatie door</a> in de calculator, of vergelijk de inzet met een uitzendkracht per FTE.</p>'
        '<h2 id="sectoren">4. Waar is de businesscase het sterkst?</h2>'
        '<ul>'
        '<li><b><a href="/sectoren/3pl-fulfillment">3PL &amp; fulfillment</a>:</b> krapste arbeidsmarkt, meest gestandaardiseerd werk. ROI 11-14 maanden.</li>'
        '<li><b><a href="/sectoren/productie-assemblage">Productie &amp; assemblage</a>:</b> kitting en machinebelading; versnelt cyclustijd 15-25%.</li>'
        '<li><b><a href="/sectoren/hospitality-retail">Hospitality &amp; retail</a>:</b> nachtwerk en voorraad, plus service-uplift.</li>'
        '<li><b><a href="/sectoren/zorg-instellingen">Zorg &amp; instellingen</a>:</b> logistieke taken weghalen bij zorgpersoneel - primair personeelsbehoud.</li>'
        '</ul>'
        '<h2 id="mens-robot">5. Mens én robot, niet mens óf robot</h2>'
        '<p>De realistische inzet is samenwerking: de robot doet het repeterende deel, je medewerker het deel met oordeel en contact. Dat verhoogt de aantrekkelijkheid van het werk en helpt je mensen behouden - in een krappe markt vaak waardevoller dan de directe besparing. Veiligheid en samenwerking zijn geregeld via de <a href="/gids/ai-act-machineverordening">EU AI-Act en Machineverordening</a>, die wij per deployment afdekken.</p>'
        '<h2 id="starten">6. Hoe begin je in 2026?</h2>'
        '<p>Niet met een grote investering, maar met een <b>pilot van 4 weken</b> (€1.500). We kiezen één taak, zetten een passende robot in en meten bespaarde uren, uptime en foutpercentage. Werkt het, dan schaal je op via <a href="/robot-as-a-service">Robot-as-a-Service</a>; werkt het niet, dan gaat de robot retour. <a href="/#contact">Plan een gratis intake</a> om je krapste functie tegen het licht te houden.</p>'
    ),
    "faqs": [
        ("Lost een humanoïde robot het personeelstekort op?",
         "Niet volledig, maar gericht: een humanoïde robot neemt repetitief, zwaar of onaantrekkelijk werk over waar je toch geen personeel voor vindt. Daardoor zet je schaarse medewerkers in op werk dat oordeel en contact vraagt. Het is mens én robot, niet mens óf robot."),
        ("Vervangt een humanoïde robot banen?",
         "In de praktijk vervangt een robot taken, geen complete functies. Hij draait het repeterende deel; je medewerker doet het deel met uitzonderingen, oordeel en menselijk contact. In de huidige krappe arbeidsmarkt vult een robot vooral vacatures die toch niet ingevuld raken."),
        ("Wat kost een humanoïde robot vergeleken met een medewerker?",
         "Een full-size humanoid neemt in twee ploegen ~1,3 FTE repeterend werk over voor ~€3.290/maand all-in (~€39.480/jaar). Tegenover ~€76k bespaarde loonkosten levert dat netto ~€36k per jaar op, plus dat je de functie niet meer hoeft te werven."),
        ("In welke sector loont een humanoïde robot het snelst?",
         "In 3PL en fulfillment: daar is de arbeidsmarkt het krapst en het werk het meest gestandaardiseerd, met een terugverdientijd van 11-14 maanden. Productie volgt, daarna hospitality en zorg."),
        ("Hoe begin ik zonder groot risico?",
         "Met een pilot van 4 weken voor €1.500. We kiezen één taak, zetten een passende robot in en meten het resultaat. Daarna beslis je pas over leasen - geen investering vooraf, na jaar 1 maandelijks opzegbaar."),
    ],
    "cta_h3": "Je krapste functie tegen het licht houden?",
    "cta_p": "Plan een gratis intake. We kijken samen welke taak een robot kan overnemen en wat dat oplevert.",
})

# 3. /mkb ------------------------------------------------------------------
PAGES.append({
    "slug": "mkb",
    "title": "Humanoïde robot leasen voor het MKB - zonder investering | BotLease",
    "desc": "Humanoïde robot leasen voor het MKB: all-in vanaf €290/mnd, geen investering vooraf, geen technisch team nodig. Zo begint een mkb-bedrijf in 2026.",
    "keywords": "humanoide robot leasen mkb, robot voor mkb, humanoide robot kleine bedrijven, robot leasen zonder investering, mkb robotisering, betaalbare humanoide robot",
    "headline": "Humanoïde robot leasen voor het MKB zonder grote investering",
    "crumbs": [("Home", "/"), ("Voor het MKB", "/mkb")],
    "eyebrow": "MKB",
    "h1": "Humanoïde robot leasen voor het MKB.",
    "tag": "Robotica was lang voorbehouden aan grote bedrijven met diepe zakken en eigen engineers. Met all-in lease is een humanoïde robot nu ook haalbaar voor het MKB.",
    "tldr": [
        "Geen investering vooraf: je leaset all-in vanaf €290/mnd in plaats van €16k-€100k+ te kopen. Je werkkapitaal blijft op de balans.",
        "Geen technisch team nodig: installatie, training, onderhoud, updates en vervanging (swap-SLA binnen 24u) zitten in het maandbedrag.",
        "Geen restwaarde-risico: humanoïde robots zijn jonge techniek - dat risico ligt bij BotLease, niet bij jou.",
        "Flexibel: standaard 36 maanden, na jaar 1 maandelijks opzegbaar. Begin met een pilot van 4 weken (€1.500) om de businesscase te bewijzen.",
    ],
    "toc": [("waarom", "1. Waarom is dit nu haalbaar voor het MKB?"),
            ("drempels", "2. De drie drempels - en hoe lease ze wegneemt"),
            ("kosten", "3. Wat kost het voor een mkb-bedrijf?"),
            ("modellen", "4. Welke modellen passen bij het MKB?"),
            ("sectoren", "5. MKB-toepassingen per sector"),
            ("starten", "6. Hoe begin je als mkb-ondernemer?")],
    "body": (
        '<h2 id="waarom">1. Waarom is dit nu haalbaar voor het MKB?</h2>'
        '<p><b>Een humanoïde robot leasen is voor het MKB haalbaar geworden omdat je hem als all-in dienst per maand afneemt in plaats van koopt.</b> Drie ontwikkelingen komen samen in 2026: de hardware wordt betaalbaar (een <a href="/robots/unitree-g1">Unitree G1</a> kost een fractie van wat industriële robots kostten), de modellen worden betrouwbaar genoeg voor echt werk, en het operational-leasemodel verschuift alle technische en financiële last naar de leasemaatschappij.</p>'
        '<p>Voor een mkb-bedrijf met een krappe arbeidsmarkt, fluctuerende volumes en geen eigen robotica-afdeling is dat precies de combinatie die de drempel wegneemt.</p>'
        '<h2 id="drempels">2. De drie drempels - en hoe lease ze wegneemt</h2>'
        '<p><b>Drempel 1 - de investering.</b> Kopen kost €16k-€100k+ plus installatie en integratie. Met lease betaal je een vast maandbedrag en blijft je werkkapitaal beschikbaar. <b>Drempel 2 - de kennis.</b> Geen eigen engineers nodig: wij verzorgen installatie, programmering, een 2-uurs operatortraining en remote tuning. <b>Drempel 3 - het risico.</b> Humanoïde robots zijn jonge techniek; het restwaarde- en onderhoudsrisico ligt volledig bij BotLease, inclusief een swap-SLA die binnen 24 uur een vervangende unit levert.</p>'
        '<p>Lees in detail hoe dit werkt via <a href="/robot-as-a-service">Robot-as-a-Service</a> of de <a href="/methodologie">methodologie</a>.</p>'
        '<h2 id="kosten">3. Wat kost het voor een mkb-bedrijf?</h2>'
        '<p>All-in maandbedragen lopen van <b>€290/mnd</b> (<a href="/robots/unitree-r1">Unitree R1</a>, instap) tot <b>€4.490/mnd</b> (<a href="/robots/neura-4ne1-gen3">NEURA 4NE-1 Gen 3.5</a>, industrieel). Daarin zitten installatie, training, onderhoud, swap-SLA en verzekering. Een pilot van 4 weken kost €1.500. Vanaf 3 units krijg je 8% korting. <a href="/kosten">Bereken het maandbedrag voor jouw situatie</a> en vergelijk het direct met koop.</p>'
        '<h2 id="modellen">4. Welke modellen passen bij het MKB?</h2>'
        '<p>Voor de meeste mkb-bedrijven liggen de instap- en middenklasse-modellen het meest voor de hand: <a href="/robots/unitree-g1">Unitree G1</a> (veelzijdig, R&amp;D en hospitality), <a href="/robots/unitree-h2">Unitree H2</a> (service en receptie), <a href="/robots/engineai-se01">EngineAI SE01</a> en <a href="/robots/pal-tiago-pro">PAL TIAGo Pro</a> (EU-gebouwd, wheeled). Voor productie-mkb met zwaarder werk: <a href="/robots/ubtech-walker-s2">UBTECH Walker S2</a>. Vergelijk ze in de <a href="/vergelijken">vergelijkingstool</a>.</p>'
        '<h2 id="sectoren">5. MKB-toepassingen per sector</h2>'
        '<p>Een mkb-3PL zet een robot in voor <a href="/sectoren/3pl-fulfillment">tote-handling en orderpicking</a> tijdens piekseizoen. Een maakbedrijf voor <a href="/sectoren/productie-assemblage">kitting en machinebelading</a>. Een hotel of winkel voor <a href="/sectoren/hospitality-retail">nachtelijke voorraadtelling en receptie</a>. Een zorginstelling voor <a href="/sectoren/zorg-instellingen">logistieke loopjes</a> die nu zorgpersoneel kosten.</p>'
        '<h2 id="starten">6. Hoe begin je als mkb-ondernemer?</h2>'
        '<p>Begin klein en bewijs het. Een <b>pilot van 4 weken</b> (€1.500) laat zien of een robot in jouw situatie rendeert, zonder dat je je vastlegt. Wij komen binnen 5 werkdagen op locatie, kiezen een passend model en meten het resultaat. <a href="/#contact">Plan een gratis intake</a> - onafhankelijk advies, geen merk dat we pushen.</p>'
    ),
    "faqs": [
        ("Is een humanoïde robot betaalbaar voor het MKB?",
         "Ja. Door te leasen in plaats van te kopen betaal je een all-in maandbedrag vanaf €290 (Unitree R1) tot €4.490 (NEURA 4NE-1 Gen 3.5), zonder investering vooraf. Een pilot van 4 weken kost €1.500. Daarmee is robotica ook voor kleine en middelgrote bedrijven haalbaar."),
        ("Heb ik technisch personeel nodig om een robot in te zetten?",
         "Nee. BotLease verzorgt installatie, programmering, een 2-uurs operatortraining en onderhoud op afstand. Je hebt geen eigen engineers of robotica-afdeling nodig."),
        ("Wat als de robot stuk gaat - draait mijn proces dan stil?",
         "Nee. Dankzij de swap-SLA staat er binnen 24 uur een vervangende unit op locatie. Halen we dat niet, dan krijg je €100/dag vergoeding. Het onderhouds- en restwaarderisico ligt bij BotLease."),
        ("Kan een klein bedrijf het contract flexibel houden?",
         "Ja. De standaardtermijn is 36 maanden; na het eerste jaar is het maandelijks opzegbaar met één maand opzegtermijn. Zo schaal je mee met fluctuerende volumes."),
        ("Hoe weet ik of het voor mijn mkb-bedrijf loont?",
         "Met een pilot van 4 weken. We kiezen één taak, zetten een passend model in en meten bespaarde uren en uptime. Op basis van dat ROI-rapport beslis je pas of je leaset."),
    ],
    "cta_h3": "Benieuwd of het voor jouw bedrijf loont?",
    "cta_p": "Plan een gratis intake. Wij komen op locatie en geven onafhankelijk advies - zonder merk dat we pushen.",
})


# 4. /prijzen --------------------------------------------------------------
# Canonical prijsdata = kosten-calculator (= robot-detailpagina's). Gesorteerd op lease oplopend.
_MODELS = [
    ("Unitree R1", "unitree-r1", "Instap / demo", 290, 8000),
    ("Unitree G1 Edu", "unitree-g1", "R&D / hospitality", 1295, 23000),
    ("NEURA 4NE-1 Mini", "neura-4ne1-mini", "EU cobot", 1295, 22000),
    ("EngineAI SE01", "engineai-se01", "Service", 1590, 28000),
    ("1X NEO", "1x-neo", "Wachtlijst · home/service", 1999, 20000),
    ("Unitree H2", "unitree-h2", "Service / receptie", 2250, 45000),
    ("Agility Digit v4", "agility-digit", "Wachtlijst · 3PL", 2899, 70000),
    ("PAL TIAGo Pro", "pal-tiago-pro", "EU wheeled", 2950, 65000),
    ("Pollen Reachy 2", "pollen-reachy-2", "EU open-source", 3250, 68000),
    ("Apptronik Apollo", "apptronik-apollo", "Wachtlijst · industrie", 3499, 48000),
    ("Figure 02 / 03", "figure-02", "Wachtlijst · industrie", 3899, 55000),
    ("PAL Kangaroo", "pal-kangaroo", "EU bipedal", 4250, 95000),
    ("UBTECH Walker S2", "ubtech-walker-s2", "Industrieel", 4250, 95000),
    ("NEURA 4NE-1 Gen 3.5", "neura-4ne1-gen3", "EU industrieel flagship", 4490, 98000),
    ("Unitree H1-2", "unitree-h1-2", "Industrieel full-size", 4890, 110000),
]
def _eur(n): return "€" + format(n, ",d").replace(",", ".")
_rows = "".join(
    f'<tr><td><a href="/robots/{slug}">{name}</a></td><td>{tier}</td>'
    f'<td><b>{_eur(lease)}/mnd</b></td><td>{_eur(koop)}</td></tr>'
    for name, slug, tier, lease, koop in _MODELS)
_price_table = (
    '<table class="cmp"><thead><tr><th>Model</th><th>Type</th>'
    '<th>Lease (all-in)</th><th>Aanschafprijs</th></tr></thead>'
    f'<tbody>{_rows}</tbody></table>')

PAGES.append({
    "slug": "prijzen",
    "title": "Wat kost een humanoïde robot? Prijzen 2026 (15 modellen) | BotLease",
    "desc": "Wat kost een humanoïde robot? Aanschafprijs €8.000-€110.000 of lease €290-€4.890/mnd all-in. Prijzen van alle 15 modellen, koop vs lease, in één tabel.",
    "keywords": "humanoide robot prijs, wat kost een humanoide robot, humanoide robot kosten, humanoide robot prijzen, goedkoopste humanoide robot, humanoide robot kopen prijs, humanoid robot prijs nederland",
    "headline": "Wat kost een humanoïde robot? Prijzen van 15 modellen (2026)",
    "crumbs": [("Home", "/"), ("Prijzen", "/prijzen")],
    "eyebrow": "Prijzen 2026",
    "h1": "Wat kost een humanoïde robot?",
    "tag": "Eerlijke prijzen van alle 15 leverbare modellen - aanschaf én all-in lease naast elkaar. Geen \"vanaf\"-marketing.",
    "tldr": [
        "Een humanoïde robot kost €8.000 tot €110.000 om te kopen, of €290 tot €4.890 per maand om all-in te leasen.",
        "Instap (demo/R&D): Unitree R1 €290/mnd, Unitree G1 €1.295/mnd. Industrieel: NEURA 4NE-1 Gen 3.5 €4.490/mnd, Unitree H1-2 €4.890/mnd.",
        "De leaseprijs is all-in: installatie, training, onderhoud, swap-SLA en verzekering inbegrepen. De aanschafprijs is dat níet - tel daar 50-100% bij op voor de echte koopkosten.",
        "Een pilot van 4 weken kost €1.500. Vanaf 3 units 8% korting, vanaf 10 units 15%.",
    ],
    "toc": [("wat-kost", "1. Wat kost een humanoïde robot?"),
            ("tabel", "2. Prijzen van alle 15 modellen"),
            ("koop-vs-lease", "3. Waarom lease vaak goedkoper uitpakt"),
            ("goedkoopste", "4. Goedkoopste en beste prijs-kwaliteit"),
            ("inbegrepen", "5. Wat zit er in de leaseprijs?"),
            ("bereken", "6. Bereken jouw prijs")],
    "body": (
        '<h2 id="wat-kost">1. Wat kost een humanoïde robot?</h2>'
        '<p><b>Een humanoïde robot kost tussen €8.000 en €110.000 om te kopen, of tussen €290 en €4.890 per maand om all-in te leasen.</b> De grote spreiding komt door het type: een instapmodel voor demo en onderzoek (Unitree R1) zit aan de onderkant, een industrieel full-size model met hoge payload (Unitree H1-2, NEURA 4NE-1 Gen 3.5) aan de bovenkant.</p>'
        '<p>Let op: de aanschafprijs is alleen de hardware. De echte koopkosten liggen 50-100% hoger door installatie, integratie, onderhoud en verzekering. Bij lease zit dat allemaal al in het maandbedrag - zie <a href="#koop-vs-lease">paragraaf 3</a>.</p>'
        '<h2 id="tabel">2. Prijzen van alle 15 modellen</h2>'
        '<p>Alle modellen die in 2026 in Nederland leverbaar zijn (of via priority-reservering voor 2026/2027), gesorteerd van goedkoop naar duur. Klik een model voor specs en details.</p>'
        + _price_table +
        '<p>Aanschafprijzen zijn publieke richtprijzen excl. installatie. Leaseprijzen zijn all-in maandbedragen. Zet twee modellen naast elkaar in de <a href="/vergelijken">vergelijkingstool</a> of bekijk de <a href="/robots">volledige catalogus</a>.</p>'
        '<h2 id="koop-vs-lease">3. Waarom lease vaak goedkoper uitpakt dan de aanschafprijs suggereert</h2>'
        '<p>De aanschafprijs is misleidend laag. Neem een Unitree G1 van €23.000. Tel daarbij op: installatie en integratie (€1.800+), een 2-uurs operatortraining, eerste-jaarsonderhoud en onderdelen (~15% van de aanschaf), en verzekering (~3%/jaar). De Total Cost of Ownership in jaar 1 loopt al snel naar €30.000+. En dan draag je nog het restwaarde-risico van jonge techniek.</p>'
        '<p>Bij <a href="/robot-as-a-service">lease (Robot-as-a-Service)</a> betaal je een vast maandbedrag waarin dat allemaal zit, zonder investering vooraf en zonder restwaarderisico. Voor het MKB is dat doorgaans de verstandigste route - lees de afweging in <a href="/vergelijken/lease-vs-koop">lease vs koop</a>.</p>'
        '<h2 id="goedkoopste">4. Goedkoopste en beste prijs-kwaliteit</h2>'
        '<p><b>Goedkoopste:</b> de <a href="/robots/unitree-r1">Unitree R1</a> (€290/mnd) - ideaal voor demo, education en lichte hospitality, maar niet voor productiewerk. <b>Beste prijs-kwaliteit voor werk:</b> de <a href="/robots/unitree-g1">Unitree G1</a> (€1.295/mnd), het de-facto standaardplatform voor R&amp;D en lichte taken. <b>Beste EU-gebouwd:</b> de <a href="/robots/pal-tiago-pro">PAL TIAGo Pro</a> (€2.950/mnd) met 100+ EU-deployments. <b>Industrieel flagship:</b> de <a href="/robots/neura-4ne1-gen3">NEURA 4NE-1 Gen 3.5</a> (€4.490/mnd) met 100 kg payload en Bosch als productiepartner.</p>'
        '<h2 id="inbegrepen">5. Wat zit er in de leaseprijs?</h2>'
        '<p>Het all-in maandbedrag dekt: de hardware, installatie + 2-uurs operatortraining, preventief en correctief onderhoud, alle onderdelen, de swap-SLA (vervangende unit binnen 24 uur, anders €100/dag), WA-verzekering tot €2,5M plus casco, software-updates en remote tuning, en 24/7 Nederlandstalige support. Niet inbegrepen: de pilot (€1.500), elektriciteit op locatie (~€30/mnd) en custom integraties boven 40 uur (€95/uur).</p>'
        '<h2 id="bereken">6. Bereken jouw prijs</h2>'
        '<p>Wil je het exacte maandbedrag voor een specifiek model, contracttermijn en aantal units - inclusief vergelijking met de koopkosten en de verwachte ROI? Gebruik de <a href="/kosten">interactieve kostencalculator</a>. Of <a href="/#contact">plan een gratis intake</a> voor een offerte op maat binnen 48 uur.</p>'
    ),
    "faqs": [
        ("Wat kost een humanoïde robot?",
         "Een humanoïde robot kost tussen €8.000 en €110.000 om te kopen, of tussen €290 en €4.890 per maand om all-in te leasen. Instapmodellen voor demo en R&D zitten aan de onderkant, industriële full-size modellen met hoge payload aan de bovenkant."),
        ("Wat is de goedkoopste humanoïde robot?",
         "De Unitree R1, te leasen vanaf €290/maand (aanschaf ~€8.000). Geschikt voor demo, education en lichte hospitality, maar niet voor productiewerk. Voor echt werk is de Unitree G1 (€1.295/maand) de goedkoopste serieuze keuze."),
        ("Hoeveel kost een humanoïde robot per maand?",
         "All-in lease loopt van €290/maand (Unitree R1) tot €4.890/maand (Unitree H1-2). Dat maandbedrag is inclusief installatie, training, onderhoud, swap-SLA en verzekering. Een pilot van 4 weken kost €1.500."),
        ("Is kopen of leasen goedkoper?",
         "De aanschafprijs lijkt lager, maar de echte koopkosten liggen 50-100% hoger door installatie, integratie, onderhoud en verzekering - plus het restwaarderisico. Voor de meeste bedrijven is all-in lease daarom voordeliger en risicovrijer. Reken beide scenario's door in de calculator."),
        ("Zijn er bijkomende kosten naast de leaseprijs?",
         "Beperkt. Buiten het all-in maandbedrag vallen alleen de pilot (€1.500, terug bij doorzetten), elektriciteit op locatie (~€30/maand) en custom integraties boven 40 uur (€95/uur). Installatie, onderhoud, onderdelen, vervanging en verzekering zitten in het maandbedrag."),
    ],
    "cta_h3": "Exacte prijs voor jouw situatie?",
    "cta_p": "Gebruik de kostencalculator of plan een gratis intake voor een offerte op maat binnen 48 uur.",
})


# 5. /robots/tesla-optimus (magnet) ---------------------------------------
PAGES.append({
    "slug": "robots/tesla-optimus",
    "title": "Tesla Optimus leasen in Nederland? Prijs & alternatieven | BotLease",
    "desc": "Kun je Tesla Optimus leasen of kopen in Nederland? Stand 2026: nog niet voor derden leverbaar. De verwachte prijs en de beste leverbare alternatieven.",
    "keywords": "tesla optimus leasen, tesla optimus kopen, tesla optimus prijs, tesla optimus nederland, tesla bot kopen, optimus robot leasen, tesla humanoide robot",
    "headline": "Tesla Optimus in Nederland: leasen, prijs en alternatieven (2026)",
    "crumbs": [("Home", "/"), ("Robots", "/robots"), ("Tesla Optimus", "/robots/tesla-optimus")],
    "eyebrow": "Robot · status 2026",
    "h1": "Tesla Optimus leasen in Nederland?",
    "tag": "De meest gezochte humanoïde robot - maar nog niet te koop of te leasen voor derden. De stand van zaken, de verwachte prijs, en wat je vandaag wél kunt inzetten.",
    "tldr": [
        "Tesla Optimus (Gen 2/3) is in 2026 níet commercieel verkrijgbaar voor externe bedrijven - Tesla zet de robot eerst intern in de eigen fabrieken in.",
        "Elon Musk noemde een doelprijs van $20.000-30.000 bij massaproductie, maar dat is een toekomstverwachting, geen actuele marktprijs.",
        "Wil je nú een humanoïde robot inzetten, dan zijn er leverbare alternatieven met vergelijkbare capaciteiten: Unitree H1-2, NEURA 4NE-1 Gen 3.5, UBTECH Walker S2.",
        "Via BotLease kun je op de wachtlijst voor westerse industriële humanoids (Figure 02, Apptronik Apollo) - en direct leasen wat al leverbaar is.",
    ],
    "toc": [("kan-het", "1. Kun je Tesla Optimus leasen of kopen in Nederland?"),
            ("prijs", "2. Wat gaat Tesla Optimus kosten?"),
            ("waarom-niet", "3. Waarom is Optimus er nog niet voor bedrijven?"),
            ("alternatieven", "4. De beste leverbare alternatieven"),
            ("wachtlijst", "5. Op de wachtlijst voor westerse humanoids"),
            ("advies", "6. Advies: begin nu, niet straks")],
    "body": (
        '<h2 id="kan-het">1. Kun je Tesla Optimus leasen of kopen in Nederland?</h2>'
        '<p><b>Nee - Tesla Optimus is in 2026 niet commercieel te koop of te leasen voor externe bedrijven, ook niet in Nederland.</b> Tesla zet Optimus eerst in binnen de eigen fabrieken (Fremont, Texas) en heeft nog geen openbaar verkoop- of leasekanaal voor derden geopend. Er is geen Europese distributie en geen officiële zakelijke prijs.</p>'
        '<p>Dat maakt Optimus een uitstekende graadmeter voor de hype rond humanoïde robots, maar geen optie als je vandaag productie- of logistiek werk wilt automatiseren. Daarvoor kijk je naar <a href="#alternatieven">leverbare modellen</a>.</p>'
        '<h2 id="prijs">2. Wat gaat Tesla Optimus kosten?</h2>'
        '<p>Elon Musk heeft meermaals een doelprijs van <b>$20.000-30.000</b> per unit genoemd bij massaproductie. Belangrijk: dat is een ambitie voor de lange termijn, geen prijs die je vandaag kunt betalen. Eerste externe units (als die er komen) zullen naar verwachting fors duurder zijn, en een Europese zakelijke prijs inclusief support en compliance is nog niet bekend.</p>'
        '<p>Ter vergelijking: leverbare westerse industriële humanoids zoals de <a href="/robots/neura-4ne1-gen3">NEURA 4NE-1 Gen 3.5</a> kosten rond €98.000 aanschaf (of €4.490/mnd all-in lease). Zie alle <a href="/prijzen">prijzen op een rij</a>.</p>'
        '<h2 id="waarom-niet">3. Waarom is Optimus er nog niet voor bedrijven?</h2>'
        '<p>Tesla volgt een "eerst zelf gebruiken"-strategie: de robot bewijst zich in de eigen productie voordat hij extern gaat. Daarnaast spelen schaalbaarheid (genoeg units produceren), betrouwbaarheid in de praktijk, en - voor de EU - compliance met de <a href="/gids/ai-act-machineverordening">AI-Act en Machineverordening</a> mee. Tot dat rond is, blijft Optimus voor Nederlandse bedrijven onbereikbaar.</p>'
        '<h2 id="alternatieven">4. De beste leverbare alternatieven voor Tesla Optimus</h2>'
        '<p>Wil je dezelfde soort taken (productie, logistiek, parts-handling) nú aanpakken, dan zijn dit de leverbare humanoids met vergelijkbare ambities:</p>'
        '<ul>'
        '<li><b><a href="/robots/unitree-h1-2">Unitree H1-2</a></b> (€4.890/mnd) - full-size, snel, industrieel inzetbaar en vandaag leverbaar.</li>'
        '<li><b><a href="/robots/neura-4ne1-gen3">NEURA 4NE-1 Gen 3.5</a></b> (€4.490/mnd) - EU-gebouwd flagship, 100 kg payload, Bosch-partner, AI-Act-ready.</li>'
        '<li><b><a href="/robots/ubtech-walker-s2">UBTECH Walker S2</a></b> (€4.250/mnd) - bewezen in auto-industrie (BYD, Foxconn), hot-swap batterij voor 24/7.</li>'
        '<li><b><a href="/robots/unitree-g1">Unitree G1</a></b> (€1.295/mnd) - veel goedkoper instappunt voor lichtere taken en R&amp;D.</li>'
        '</ul>'
        '<p>Vergelijk specs en prijs in de <a href="/vergelijken">vergelijkingstool</a> of bekijk de <a href="/robots">volledige catalogus</a>.</p>'
        '<h2 id="wachtlijst">5. Op de wachtlijst voor westerse humanoids</h2>'
        '<p>Geef je de voorkeur aan een Amerikaanse industriële humanoid in de geest van Optimus, dan kun je via BotLease priority-toegang reserveren voor de <a href="/robots/figure-02">Figure 02</a> (BMW-deployment, derden vanaf Q1 2027) en de <a href="/robots/apptronik-apollo">Apptronik Apollo</a> (Mercedes-pilot, EU vanaf Q4 2026). Zo sta je vooraan zodra commerciële verkoop opent.</p>'
        '<h2 id="advies">6. Advies: begin nu, niet straks</h2>'
        '<p>Wachten op Optimus betekent maanden tot jaren niets doen aan je arbeidskrapte. De verstandige route: start nu een <a href="/#contact">pilot van 4 weken</a> met een leverbaar model, bouw ervaring op, en schaal op of switch wanneer nieuwe modellen beschikbaar komen. Met <a href="/robot-as-a-service">Robot-as-a-Service</a> zit je nergens aan vast: na jaar 1 maandelijks opzegbaar, en wij wisselen het model als er iets beters past.</p>'
    ),
    "faqs": [
        ("Kun je Tesla Optimus kopen of leasen in Nederland?",
         "Nee. Tesla Optimus is in 2026 niet commercieel verkrijgbaar voor externe bedrijven, ook niet in Nederland. Tesla zet de robot eerst intern in de eigen fabrieken in en heeft geen verkoop- of leasekanaal voor derden geopend."),
        ("Wat gaat Tesla Optimus kosten?",
         "Elon Musk noemde een doelprijs van $20.000-30.000 bij massaproductie, maar dat is een toekomstverwachting, geen actuele prijs. Eerste externe units worden naar verwachting duurder, en een EU-zakelijke prijs inclusief support is nog niet bekend."),
        ("Wat is het beste alternatief voor Tesla Optimus dat nu leverbaar is?",
         "Voor industrieel werk: de Unitree H1-2 (€4.890/mnd), NEURA 4NE-1 Gen 3.5 (€4.490/mnd) of UBTECH Walker S2 (€4.250/mnd). Voor lichtere taken en een veel lager budget: de Unitree G1 (€1.295/mnd). Allemaal vandaag te leasen via BotLease."),
        ("Wanneer komt Tesla Optimus naar Europa?",
         "Er is geen officiële datum. Tesla richt zich eerst op interne inzet en Amerikaanse schaalproductie. Externe en Europese beschikbaarheid, inclusief AI-Act-compliance, is nog onzeker. Voor westerse alternatieven kun je via BotLease op de wachtlijst voor Figure 02 en Apptronik Apollo."),
    ],
    "cta_h3": "Niet wachten op Optimus - nu al beginnen?",
    "cta_p": "Plan een gratis intake. Wij adviseren onafhankelijk welk leverbaar model bij je taak past.",
})

# 6. /veelgestelde-vragen (FAQ hub) ---------------------------------------
PAGES.append({
    "slug": "veelgestelde-vragen",
    "title": "Veelgestelde vragen over humanoïde robots leasen | BotLease",
    "desc": "Antwoorden op de meestgestelde vragen over humanoïde robots leasen: kosten, veiligheid, batterij, payload, EU AI-Act, opzeggen, pilot en meer.",
    "keywords": "humanoide robot vragen, humanoide robot leasen faq, hoeveel kost humanoide robot, hoe lang batterij robot, payload humanoide robot, humanoide robot veiligheid",
    "headline": "Veelgestelde vragen over humanoïde robots leasen",
    "crumbs": [("Home", "/"), ("Veelgestelde vragen", "/veelgestelde-vragen")],
    "eyebrow": "FAQ",
    "h1": "Veelgestelde vragen over humanoïde robots.",
    "tag": "De vragen die ondernemers ons het vaakst stellen over het leasen en inzetten van humanoïde robots - kort en eerlijk beantwoord.",
    "tldr": [
        "Lease loopt van €290/mnd (Unitree R1) tot €4.890/mnd (Unitree H1-2), all-in inclusief installatie, onderhoud, swap-SLA en verzekering.",
        "Een pilot van 4 weken (€1.500) bewijst de businesscase; daarna 36 mnd lease, na jaar 1 maandelijks opzegbaar.",
        "Veiligheid en compliance (EU AI-Act, Machineverordening) regelen wij per deployment - jij hebt geen technisch team nodig.",
        "Batterij gaat 2-5 uur mee afhankelijk van het model; hot-swap of laadstation maakt 24/7-inzet mogelijk.",
    ],
    "toc": [("kosten", "Kosten & contract"),
            ("techniek", "Techniek & inzet"),
            ("veiligheid", "Veiligheid & wetgeving"),
            ("starten", "Starten met BotLease")],
    "body": (
        '<h2 id="kosten">Kosten &amp; contract</h2>'
        '<p>De meestgestelde vragen over prijs, contract en opzeggen. Voor een volledige prijslijst zie <a href="/prijzen">prijzen</a> of bereken je situatie in de <a href="/kosten">calculator</a>.</p>'
        '<p><b>Wat kost een humanoïde robot leasen?</b> All-in van €290/mnd (Unitree R1) tot €4.890/mnd (Unitree H1-2). Inbegrepen: installatie, training, onderhoud, swap-SLA, verzekering en support.</p>'
        '<p><b>Wat is de goedkoopste humanoïde robot?</b> De <a href="/robots/unitree-r1">Unitree R1</a> vanaf €290/mnd; voor echt werk de <a href="/robots/unitree-g1">Unitree G1</a> vanaf €1.295/mnd.</p>'
        '<p><b>Kan ik tussentijds opzeggen?</b> Het eerste jaar ligt vast, daarna maandelijks opzegbaar met één maand opzegtermijn, zonder boete.</p>'
        '<p><b>Zijn er bijkomende kosten?</b> Alleen de pilot (€1.500, terug bij doorzetten), elektriciteit (~€30/mnd) en custom integraties boven 40 uur (€95/uur).</p>'
        '<h2 id="techniek">Techniek &amp; inzet</h2>'
        '<p><b>Hoe lang gaat de batterij mee?</b> 2-5 uur afhankelijk van het model en de taak. Met hot-swap-batterij (bijv. <a href="/robots/ubtech-walker-s2">UBTECH Walker S2</a>) of een laadstation is 24/7-inzet mogelijk.</p>'
        '<p><b>Hoeveel kan een humanoïde robot tillen?</b> Van enkele kilo\'s (lichte service-modellen) tot 100 kg payload bij de <a href="/robots/neura-4ne1-gen3">NEURA 4NE-1 Gen 3.5</a>. Kies op basis van je taak.</p>'
        '<p><b>Heb ik technische kennis nodig?</b> Nee. Wij verzorgen installatie, programmering en een 2-uurs operatortraining. Aanpassingen doen wij op afstand.</p>'
        '<p><b>Hoe snel is een robot operationeel?</b> Intake binnen 5 werkdagen, inzet gemiddeld 10 werkdagen later, productief vanaf week 2 van de pilot.</p>'
        '<p><b>Welke robot past bij mijn bedrijf?</b> Dat bepaalt de gratis intake. Bekijk vast de <a href="/sectoren">sectoren</a> of <a href="/vergelijken">vergelijk modellen</a>.</p>'
        '<h2 id="veiligheid">Veiligheid &amp; wetgeving</h2>'
        '<p><b>Hoe veilig is een humanoïde robot op de werkvloer?</b> Elke deployment voldoet aan de Machinerichtlijn/Machineverordening en ISO 10218 / EN ISO 13482. Wij doen risicoanalyse, definiëren werkzones en trainen je team. WA-dekking tot €2,5M.</p>'
        '<p><b>Valt een humanoïde robot onder de EU AI-Act?</b> Meestal wel, als high-risk AI bij veiligheidskritische inzet. Wij dragen de compliance-last als provider en helpen je als deployer - zie de <a href="/gids/ai-act-machineverordening">AI-Act gids</a>.</p>'
        '<p><b>Wat met AVG/GDPR en data?</b> Camera- en sensordata blijven on-prem of in EU-cloud; wij sluiten een verwerkersovereenkomst per klant. EU-gebouwde modellen (NEURA, PAL) zijn extra preferent.</p>'
        '<h2 id="starten">Starten met BotLease</h2>'
        '<p><b>Wat als de robot stuk gaat?</b> Swap-SLA: binnen 24 uur een vervangende unit op locatie, anders €100/dag vergoeding.</p>'
        '<p><b>Is huren of leasen beter?</b> Voor een piek of project: <a href="/huren">huren</a>. Voor structurele inzet: <a href="/robot-as-a-service">leasen (RaaS)</a>, goedkoper per maand.</p>'
        '<p><b>Hoe begin ik?</b> <a href="/#contact">Plan een gratis intake</a>. Wij komen binnen 5 werkdagen langs en geven binnen 48 uur een voorstel.</p>'
    ),
    "faqs": [
        ("Wat kost een humanoïde robot leasen?",
         "All-in lease loopt van €290/maand (Unitree R1) tot €4.890/maand (Unitree H1-2), inclusief installatie, training, onderhoud, swap-SLA en verzekering. Een pilot van 4 weken kost €1.500."),
        ("Hoe lang gaat de batterij van een humanoïde robot mee?",
         "Afhankelijk van model en taak 2 tot 5 uur. Met een hot-swap-batterij of laadstation is 24/7-inzet mogelijk, bijvoorbeeld bij de UBTECH Walker S2."),
        ("Hoeveel kan een humanoïde robot tillen?",
         "Van enkele kilo's bij lichte service-modellen tot 100 kg payload bij de NEURA 4NE-1 Gen 3.5. De keuze hangt af van je taak."),
        ("Hoe veilig is een humanoïde robot op de werkvloer?",
         "Elke deployment voldoet aan de Machinerichtlijn/Machineverordening en ISO 10218 / EN ISO 13482. BotLease voert risicoanalyse uit, definieert werkzones en traint je team. WA-dekking tot €2,5M."),
        ("Valt een humanoïde robot onder de EU AI-Act?",
         "Meestal wel, als high-risk AI bij veiligheidskritische inzet. BotLease draagt de compliance-last als provider en helpt je als deployer voldoen aan je verplichtingen."),
        ("Kan ik een leasecontract tussentijds opzeggen?",
         "Het eerste jaar ligt vast. Daarna is het maandelijks opzegbaar met één maand opzegtermijn, zonder boete."),
        ("Heb ik technisch personeel nodig om een robot te bedienen?",
         "Nee. BotLease verzorgt installatie, programmering en een 2-uurs operatortraining. Aanpassingen aan taken doen wij op afstand of on-site."),
        ("Wat als de robot stuk gaat?",
         "Dankzij de swap-SLA staat er binnen 24 uur een vervangende unit op locatie. Halen we dat niet, dan krijg je €100/dag vergoeding."),
    ],
    "cta_h3": "Nog een vraag die hier niet bij staat?",
    "cta_p": "Plan een gratis intake of mail hallo@botlease.nl - we denken vrijblijvend mee.",
})

# 7. /terugverdientijd-roi -------------------------------------------------
PAGES.append({
    "slug": "terugverdientijd-roi",
    "title": "Terugverdientijd humanoïde robot: ROI per sector | BotLease",
    "desc": "Wat is de terugverdientijd van een humanoïde robot? ROI-rekenvoorbeelden per sector: 3PL 11-14 mnd, productie 13-18 mnd, hospitality en zorg.",
    "keywords": "terugverdientijd humanoide robot, roi humanoide robot, humanoide robot terugverdienen, kosten baten robot, robot rendabel, payback humanoide robot",
    "headline": "Terugverdientijd van een humanoïde robot: ROI per sector",
    "crumbs": [("Home", "/"), ("Terugverdientijd & ROI", "/terugverdientijd-roi")],
    "eyebrow": "ROI",
    "h1": "Terugverdientijd van een humanoïde robot.",
    "tag": "Eerlijke ROI-rekenvoorbeelden per sector, gebaseerd op publieke pilot-data - geen marketing, wel de aannames erbij.",
    "tldr": [
        "Typische terugverdientijd: 3PL/fulfillment 11-14 maanden, productie 13-18 maanden, hospitality 18-24 maanden, zorg 18-30 maanden.",
        "De rekenregel: bespaarde loonkosten + extra capaciteit − all-in leaseprijs. Een full-size humanoid neemt in 2 ploegen ~1,3 FTE repeterend werk over.",
        "Voorbeeld 3PL: ~€76k bespaarde loonkosten/jaar tegenover ~€39k lease = ~€36k netto/jaar, terugverdiend in ~13 maanden.",
        "Omdat lease off-balance en maandelijks is, vergelijk je het maandbedrag direct met de loonkosten van de taak - geen afschrijving over jaren.",
    ],
    "toc": [("hoe-bereken", "1. Hoe bereken je de terugverdientijd?"),
            ("3pl", "2. 3PL & fulfillment: 11-14 maanden"),
            ("productie", "3. Productie & assemblage: 13-18 maanden"),
            ("hospitality", "4. Hospitality & retail: 18-24 maanden"),
            ("zorg", "5. Zorg: 18-30 maanden"),
            ("aannames", "6. Aannames en hoe je zeker weet of het klopt")],
    "body": (
        '<h2 id="hoe-bereken">1. Hoe bereken je de terugverdientijd?</h2>'
        '<p><b>De terugverdientijd van een humanoïde robot is de all-in investering gedeeld door het netto jaarlijkse voordeel</b> (bespaarde loonkosten plus extra capaciteit, min de leaseprijs). Bij operational lease is er geen aanschaf vooraf, dus reken je eenvoudig: vergelijk het maandbedrag met de loonkosten van de taak die de robot overneemt.</p>'
        '<p>De vuistregel: een full-size humanoid draait in twee ploegen en neemt zo ~1,3 FTE aan repeterend werk over. Reken jouw eigen scenario door in de <a href="/kosten">kostencalculator</a>.</p>'
        '<h2 id="3pl">2. 3PL &amp; fulfillment: 11-14 maanden</h2>'
        '<p>De sterkste businesscase, want de arbeidsmarkt is hier het krapst en het werk het meest gestandaardiseerd. <b>Rekenvoorbeeld:</b> een <a href="/robots/ubtech-walker-s2">UBTECH Walker S2</a> (€4.250/mnd = €51.000/jaar) doet tote-handling in twee ploegen en vervangt ~1,3 FTE. Bij €28/uur loonkost: 1,3 × 2.080 uur × €28 ≈ €76.000 bespaarde loonkosten/jaar. Netto voordeel ≈ €25.000/jaar plus de vacature die je niet meer hoeft te vervullen. Terugverdiend in ~11-14 maanden. Meer in <a href="/sectoren/3pl-fulfillment">3PL &amp; fulfillment</a>.</p>'
        '<h2 id="productie">3. Productie &amp; assemblage: 13-18 maanden</h2>'
        '<p>Hier zit het voordeel vaak niet in FTE-vervanging maar in capaciteit en kwaliteit. Een <a href="/robots/neura-4ne1-gen3">NEURA 4NE-1 Gen 3.5</a> in een mixed-assembly cel versnelt de cyclustijd met 15-25%. Voor een lijn met €2M omzet/jaar is dat €300.000-500.000 extra capaciteit - waardoor de lease (€4.490/mnd) zich ruim binnen anderhalf jaar terugverdient. Zie <a href="/sectoren/productie-assemblage">productie &amp; assemblage</a>.</p>'
        '<h2 id="hospitality">4. Hospitality &amp; retail: 18-24 maanden</h2>'
        '<p>Een <a href="/robots/unitree-g1">Unitree G1</a> (€1.295/mnd) doet nachtelijke voorraadtelling: ~2 FTE-uren/week bespaard × €28 × 50 weken ≈ €58.000/jaar aan vrijgespeelde uren, plus de gastenscore-uplift van een lobby-host. Terugverdiend in ~18-24 maanden. Zie <a href="/sectoren/hospitality-retail">hospitality &amp; retail</a>.</p>'
        '<h2 id="zorg">5. Zorg &amp; instellingen: 18-30 maanden</h2>'
        '<p>Lastiger in euro\'s uit te drukken, want het voordeel is primair personeelsbehoud, niet kostenbesparing. Gemiddeld wordt ~0,6 FTE vrijgespeeld voor zorgtaken per robot door logistieke loopjes over te nemen. Voor een instelling met 200 bedden: ~€42.000/jaar bespaarde wervings- en inwerkkosten plus betere zorgkwaliteit. Zie <a href="/sectoren/zorg-instellingen">zorg &amp; instellingen</a>.</p>'
        '<h2 id="aannames">6. Aannames en hoe je zeker weet of het klopt</h2>'
        '<p>Deze cijfers gaan uit van €28/uur loonkost, twee-ploegeninzet en publieke pilot-data uit de EU en VS. Jouw situatie wijkt af - daarom bestaat de <b>pilot van 4 weken</b> (€1.500): we meten de echte uptime, cyclustijd en bespaarde uren in jóuw workflow en leveren een ROI-rapport. Pas daarna beslis je over lease. <a href="/#contact">Plan een gratis intake</a> om je sterkste use-case te bepalen.</p>'
    ),
    "faqs": [
        ("Wat is de terugverdientijd van een humanoïde robot?",
         "Typisch 11-14 maanden in 3PL/fulfillment, 13-18 maanden in productie, 18-24 maanden in hospitality en 18-30 maanden in de zorg. De exacte tijd hangt af van loonkosten, ploegen en hoeveel werk de robot overneemt."),
        ("Hoe bereken je de ROI van een humanoïde robot?",
         "Deel de all-in investering door het netto jaarlijkse voordeel (bespaarde loonkosten plus extra capaciteit, min de leaseprijs). Bij lease vergelijk je simpelweg het maandbedrag met de loonkosten van de taak die de robot overneemt."),
        ("Wanneer is een humanoïde robot rendabel?",
         "Zodra het netto jaarlijkse voordeel de leaseprijs overstijgt - meestal binnen 1 tot 2,5 jaar. Het loont het snelst bij repetitief, voorspelbaar werk in een krappe arbeidsmarkt, zoals 3PL en productie."),
        ("Hoeveel bespaar je met een humanoïde robot in 3PL?",
         "Een full-size humanoid (~€51.000/jaar lease) vervangt in twee ploegen ~1,3 FTE repeterend werk, goed voor ~€76.000 bespaarde loonkosten per jaar - netto ~€25.000 plus de vacature die je niet hoeft te vervullen."),
        ("Hoe weet ik zeker dat de ROI in mijn situatie klopt?",
         "Met een pilot van 4 weken (€1.500): we meten de echte uptime, cyclustijd en bespaarde uren in jouw workflow en leveren een ROI-rapport. Pas daarna beslis je over leasen."),
    ],
    "cta_h3": "Je eigen terugverdientijd berekenen?",
    "cta_p": "Gebruik de kostencalculator of plan een gratis intake voor een ROI-analyse op maat.",
})


# 8. /beste-humanoide-robots-2026 (listicle) ------------------------------
PAGES.append({
    "slug": "beste-humanoide-robots-2026",
    "title": "Beste humanoïde robots voor bedrijven (2026) | BotLease",
    "desc": "De beste humanoïde robots voor bedrijven in 2026, per use-case: beste instap, beste EU-gebouwd, beste industrieel en beste prijs-kwaliteit. Met leaseprijzen.",
    "keywords": "beste humanoide robot, beste humanoide robots 2026, welke humanoide robot, humanoide robot vergelijken, beste humanoide robot bedrijven, top humanoide robots",
    "headline": "De beste humanoïde robots voor bedrijven in 2026",
    "crumbs": [("Home", "/"), ("Beste humanoïde robots 2026", "/beste-humanoide-robots-2026")],
    "eyebrow": "Vergelijking 2026",
    "h1": "De beste humanoïde robots voor bedrijven (2026).",
    "tag": "Geen één \"beste\" robot - wel de beste per doel. Onze onafhankelijke keuzes per use-case, met leaseprijs en waarom.",
    "tldr": [
        "Beste instap: Unitree R1 (€290/mnd) voor demo/R&D; beste prijs-kwaliteit voor werk: Unitree G1 (€1.295/mnd).",
        "Beste EU-gebouwd: PAL TIAGo Pro (€2.950/mnd, 100+ EU-deployments); beste industrieel flagship: NEURA 4NE-1 Gen 3.5 (€4.490/mnd, 100 kg payload).",
        "Beste voor 24/7 productie: UBTECH Walker S2 (€4.250/mnd, hot-swap batterij, bewezen bij BYD/Foxconn).",
        "Wij zijn vendor-neutraal: we adviseren op basis van jouw taak, niet op marge. Begin met een pilot van 4 weken (€1.500).",
    ],
    "toc": [("hoe-kiezen", "1. Er is geen één beste robot"),
            ("instap", "2. Beste instap & prijs-kwaliteit"),
            ("eu", "3. Beste EU-gebouwd"),
            ("industrieel", "4. Beste industrieel & 24/7"),
            ("service", "5. Beste voor service & hospitality"),
            ("kiezen", "6. Zo kies je de juiste")],
    "body": (
        '<h2 id="hoe-kiezen">1. Er is geen één "beste" humanoïde robot</h2>'
        '<p><b>De beste humanoïde robot bestaat niet - de beste robot voor jóuw taak wel.</b> Een instapmodel voor onderzoek is hopeloos in een productielijn, en een industrieel flagship is overkill voor een receptie. Daarom rangschikken we hieronder per use-case in plaats van één winnaar te kiezen. Alle prijzen zijn all-in lease; vergelijk ze ook in de <a href="/prijzen">prijstabel</a> of de <a href="/vergelijken">vergelijkingstool</a>.</p>'
        '<h2 id="instap">2. Beste instap &amp; beste prijs-kwaliteit</h2>'
        '<p><b>Beste instap - <a href="/robots/unitree-r1">Unitree R1</a> (€290/mnd).</b> De goedkoopste serieuze humanoid, ideaal om te leren, te demonstreren en lichte hospitality-taken te doen. Niet voor productiewerk.</p>'
        '<p><b>Beste prijs-kwaliteit voor echt werk - <a href="/robots/unitree-g1">Unitree G1</a> (€1.295/mnd).</b> Het de-facto standaardplatform voor R&amp;D, voorraadtelling en inspectie. Veel capaciteit voor weinig geld; de meeste eerste pilots draaien hierop.</p>'
        '<h2 id="eu">3. Beste EU-gebouwd</h2>'
        '<p><b>Beste EU-allrounder - <a href="/robots/pal-tiago-pro">PAL TIAGo Pro</a> (€2.950/mnd).</b> Spaanse fabrikant met 20+ jaar ervaring en 100+ EU-deployments, ROS-native, EU AI-Act-ready vanaf dag 1. <b>Industrieel EU-flagship - <a href="/robots/neura-4ne1-gen3">NEURA 4NE-1 Gen 3.5</a> (€4.490/mnd):</b> 100 kg payload, Porsche-design, Bosch als productiepartner. EU-gebouwd is strategisch belangrijk voor <a href="/gids/ai-act-machineverordening">AI-Act-compliance</a> en korte levertijden.</p>'
        '<h2 id="industrieel">4. Beste industrieel &amp; 24/7</h2>'
        '<p><b>Beste voor 24/7 productie - <a href="/robots/ubtech-walker-s2">UBTECH Walker S2</a> (€4.250/mnd).</b> Bewezen in massaproductie bij BYD en Foxconn, met hot-swap batterij voor continue inzet. <b>Snelste full-size - <a href="/robots/unitree-h1-2">Unitree H1-2</a> (€4.890/mnd):</b> krachtig en behendig voor zwaarder werk. Voor westerse industriële humanoids kun je op de wachtlijst voor <a href="/robots/figure-02">Figure 02</a> en <a href="/robots/apptronik-apollo">Apptronik Apollo</a>.</p>'
        '<h2 id="service">5. Beste voor service &amp; hospitality</h2>'
        '<p><b><a href="/robots/unitree-h2">Unitree H2</a> (€2.250/mnd)</b> met bionisch gezicht voor receptie en gastinteractie, en de <b><a href="/robots/pollen-reachy-2">Pollen Reachy 2</a> (€3.250/mnd)</b> - open-source, eigendom van Hugging Face, sterk voor manipulatie-onderzoek en demo\'s. Zie toepassingen in <a href="/sectoren/hospitality-retail">hospitality &amp; retail</a>.</p>'
        '<h2 id="kiezen">6. Zo kies je de juiste robot</h2>'
        '<p>Vier vragen: wat is je primaire taak, hoe zwaar is de payload, is EU-compliance kritiek, en wat is je budget? Wij adviseren onafhankelijk - we vertegenwoordigen geen merk exclusief en kiezen wat past. De zekerste test is een <a href="/#contact">pilot van 4 weken</a> (€1.500): we zetten het model in jouw workflow en meten het resultaat. Lees ook de <a href="/gids/humanoide-robot-leasen">complete lease-gids</a>.</p>'
    ),
    "faqs": [
        ("Wat is de beste humanoïde robot voor bedrijven in 2026?",
         "Er is geen enkele beste - het hangt af van je taak. Beste prijs-kwaliteit voor werk is de Unitree G1 (€1.295/mnd), beste EU-gebouwd de PAL TIAGo Pro (€2.950/mnd), beste industrieel de NEURA 4NE-1 Gen 3.5 (€4.490/mnd) en beste voor 24/7 de UBTECH Walker S2 (€4.250/mnd)."),
        ("Wat is de beste goedkope humanoïde robot?",
         "De Unitree R1 (€290/mnd) is de goedkoopste, geschikt voor demo, education en lichte hospitality. Voor echt werk is de Unitree G1 (€1.295/mnd) de beste betaalbare keuze."),
        ("Welke humanoïde robot is het beste voor de industrie?",
         "Voor industrieel werk: de NEURA 4NE-1 Gen 3.5 (100 kg payload, EU-gebouwd) of de UBTECH Walker S2 (bewezen bij BYD/Foxconn, hot-swap batterij voor 24/7). Voor zwaar, snel werk de Unitree H1-2."),
        ("Welke humanoïde robot is het beste voor EU-compliance?",
         "EU-gebouwde modellen: PAL TIAGo Pro en PAL Kangaroo (Spanje), NEURA 4NE-1 (Duitsland) en Pollen Reachy 2 (Frankrijk). Ze zijn AI-Act- en Machineverordening-ready vanaf dag 1 en hebben de kortste levertijd binnen de EU."),
    ],
    "cta_h3": "Welke robot past het beste bij jouw taak?",
    "cta_p": "Plan een gratis intake. Wij adviseren onafhankelijk - geen merk dat we pushen.",
})

# 9. /robot-vs-uitzendkracht ----------------------------------------------
PAGES.append({
    "slug": "robot-vs-uitzendkracht",
    "title": "Humanoïde robot vs uitzendkracht: kosten per FTE | BotLease",
    "desc": "Humanoïde robot of uitzendkracht? Een eerlijke kostenvergelijking per FTE: uurtarief, beschikbaarheid, opschaling en wanneer een robot goedkoper is.",
    "keywords": "robot vs uitzendkracht, humanoide robot vs medewerker, robot als arbeidskracht, robot goedkoper dan mens, kosten robot vs personeel, robot uitzendkracht vergelijking",
    "headline": "Humanoïde robot vs uitzendkracht: de kostenvergelijking per FTE",
    "crumbs": [("Home", "/"), ("Robot vs uitzendkracht", "/robot-vs-uitzendkracht")],
    "eyebrow": "Vergelijking",
    "h1": "Humanoïde robot vs uitzendkracht.",
    "tag": "Wat is goedkoper voor repeterend werk: een uitzendkracht of een humanoïde robot? Een eerlijke rekensom per FTE - inclusief wat de robot níet kan.",
    "tldr": [
        "Een uitzendkracht in logistiek kost ~€28-35/uur all-in; in twee ploegen is dat ~€116.000-145.000/jaar voor 2 FTE-dekking.",
        "Een full-size humanoïde robot leaset voor ~€3.290-4.890/mnd (~€39.000-59.000/jaar) all-in en draait beide ploegen - voor repeterend werk dus fors goedkoper per FTE.",
        "De robot wint bij voorspelbaar, repetitief werk dat 24/7 doorloopt; de mens wint bij uitzonderingen, oordeel en klantcontact.",
        "Realistisch is een mix: de robot doet het repeterende deel, je flexkracht het deel met variatie. Begin met een pilot van 4 weken.",
    ],
    "toc": [("vraag", "1. Robot of uitzendkracht - de juiste vraag"),
            ("kosten", "2. De kostenvergelijking per FTE"),
            ("beschikbaarheid", "3. Beschikbaarheid en opschaling"),
            ("kan-niet", "4. Wat een robot (nog) niet kan"),
            ("mix", "5. De realistische mix"),
            ("starten", "6. Doorrekenen voor jouw situatie")],
    "body": (
        '<h2 id="vraag">1. Robot of uitzendkracht - de juiste vraag</h2>'
        '<p>De vraag is niet "robot óf mens", maar "welk werk laat ik door wie doen". Voor repetitief, voorspelbaar werk - tote-handling, kitting, voorraadtelling - is een humanoïde robot inmiddels een serieus alternatief voor een uitzendkracht. Voor werk met veel uitzonderingen, oordeel of klantcontact blijft de mens onverslaanbaar. Hieronder de eerlijke rekensom.</p>'
        '<h2 id="kosten">2. De kostenvergelijking per FTE</h2>'
        '<p><b>Uitzendkracht:</b> in logistiek reken je ~€28-35/uur all-in (inclusief werkgeverslasten en bureaumarge). Eén FTE = ~2.080 uur/jaar ≈ €58.000-73.000. Voor tweeploegendekking (2 FTE): ~€116.000-145.000/jaar.</p>'
        '<p><b>Humanoïde robot:</b> een full-size model zoals de <a href="/robots/ubtech-walker-s2">UBTECH Walker S2</a> (€4.250/mnd) of <a href="/robots/unitree-h1-2">Unitree H1-2</a> (€4.890/mnd) leaset voor ~€51.000-59.000/jaar all-in en draait beide ploegen zonder toeslag voor nacht of weekend. Voor lichter werk volstaat een <a href="/robots/unitree-g1">Unitree G1</a> (€1.295/mnd ≈ €15.500/jaar).</p>'
        '<table class="cmp"><thead><tr><th>Per jaar (2-ploegen, repeterend werk)</th><th>Uitzendkracht (2 FTE)</th><th>Humanoïde robot</th></tr></thead>'
        '<tbody>'
        '<tr><td><b>Kosten</b></td><td>€116.000-145.000</td><td>€51.000-59.000</td></tr>'
        '<tr><td><b>Nacht-/weekendtoeslag</b></td><td>Ja</td><td>Nee</td></tr>'
        '<tr><td><b>Verloop / inwerken</b></td><td>Doorlopend</td><td>Eenmalig</td></tr>'
        '<tr><td><b>Beschikbaarheid</b></td><td>Afhankelijk van markt</td><td>Direct, geen vacature</td></tr>'
        '<tr><td><b>Flexibiliteit / oordeel</b></td><td>Hoog</td><td>Beperkt</td></tr>'
        '</tbody></table>'
        '<p>Voor puur repeterend tweeploegenwerk is de robot dus grofweg de helft goedkoper per FTE - en je hoeft de vacature niet te vervullen in een krappe markt. Reken jouw scenario door in de <a href="/kosten">calculator</a> of zie de <a href="/terugverdientijd-roi">terugverdientijd per sector</a>.</p>'
        '<h2 id="beschikbaarheid">3. Beschikbaarheid en opschaling</h2>'
        '<p>Het grootste verschil is niet de prijs maar de beschikbaarheid: een uitzendkracht voor nachtdienst of zwaar repetitief werk is in 2026 vaak simpelweg niet te vinden. Een robot heeft geen vacature, geen verloop en geen inwerktijd na de eerste setup. Opschalen doe je per unit, met 8% korting vanaf 3 stuks - zie <a href="/personeelstekort-humanoide-robot">humanoïde robot tegen personeelstekort</a>.</p>'
        '<h2 id="kan-niet">4. Wat een robot (nog) niet kan</h2>'
        '<p>Wees eerlijk: een humanoïde robot is niet goed in taken met veel uitzonderingen, fijne motoriek onder tijdsdruk, improvisatie of intensief menselijk contact. Daar is en blijft je medewerker waardevoller. De robot is een instrument voor het voorspelbare deel van het werk, niet een eén-op-één mensvervanger.</p>'
        '<h2 id="mix">5. De realistische mix</h2>'
        '<p>De sterkste opstelling is samenwerking: de robot doet het repeterende, fysiek zware deel; je flexkracht of vaste medewerker het deel met variatie en oordeel. Zo verlaag je je kosten én maak je het werk aantrekkelijker - wat helpt om de mensen die je wél hebt te behouden. Dat is geen toekomstmuziek; het is hoe de eerste Nederlandse pilots draaien.</p>'
        '<h2 id="starten">6. Doorrekenen voor jouw situatie</h2>'
        '<p>Of een robot in jouw geval goedkoper is dan flexkrachten hangt af van het uurtarief, het aantal ploegen en hoe repetitief het werk is. Een <a href="/#contact">gratis intake</a> plus een pilot van 4 weken (€1.500) geeft je een concrete vergelijking met echte cijfers uit jouw workflow.</p>'
    ),
    "faqs": [
        ("Is een humanoïde robot goedkoper dan een uitzendkracht?",
         "Voor repetitief tweeploegenwerk wel: een full-size humanoid kost ~€51.000-59.000/jaar all-in lease en draait beide ploegen, tegenover ~€116.000-145.000/jaar voor 2 FTE uitzendkrachten. Voor werk met veel variatie of klantcontact is de mens (kosten)effectiever."),
        ("Hoeveel kost een uitzendkracht in de logistiek per jaar?",
         "In de logistiek reken je ~€28-35/uur all-in inclusief werkgeverslasten en bureaumarge. Eén FTE (~2.080 uur) komt daarmee op ~€58.000-73.000 per jaar, plus nacht- en weekendtoeslagen."),
        ("Vervangt een robot een uitzendkracht volledig?",
         "Nee. Een robot neemt het voorspelbare, repetitieve deel over. Werk met uitzonderingen, oordeel, improvisatie of klantcontact blijft mensenwerk. De beste opstelling is een mix: robot plus medewerker."),
        ("Waarom kiezen bedrijven voor een robot in plaats van flexkrachten?",
         "Vooral door beschikbaarheid: voor nachtdienst en zwaar repetitief werk zijn in 2026 vaak geen flexkrachten te vinden. Een robot heeft geen vacature, geen verloop en geen toeslagen, en is per maand op te schalen."),
    ],
    "cta_h3": "Robot vs flexkracht doorrekenen voor jouw werk?",
    "cta_p": "Plan een gratis intake. We vergelijken met echte cijfers uit jouw workflow - geen aannames.",
})


# 10. /machineverordening-2027-humanoide-robots ---------------------------
PAGES.append({
    "slug": "machineverordening-2027-humanoide-robots",
    "title": "Machineverordening 2027 & humanoïde robots: checklist | BotLease",
    "desc": "EU Machineverordening 2023/1230 geldt vanaf 20 januari 2027. Wat verandert er voor humanoïde robots op de werkvloer en welke checklist hebben werkgevers nodig?",
    "keywords": "machineverordening 2027, machineverordening 2023/1230, machineverordening humanoide robot, CE markering robot, machinerichtlijn robot, EU machineverordening werkgevers",
    "headline": "Machineverordening 2027 en humanoïde robots: wat verandert er?",
    "crumbs": [("Home", "/"), ("Machineverordening 2027", "/machineverordening-2027-humanoide-robots")],
    "eyebrow": "Compliance · aftellen naar 2027",
    "h1": "Machineverordening 2027 en humanoïde robots.",
    "tag": "Op 20 januari 2027 vervangt de EU Machineverordening 2023/1230 de oude Machinerichtlijn. Wat dat betekent voor humanoïde robots - en de checklist voor werkgevers.",
    "tldr": [
        "De EU Machineverordening (EU) 2023/1230 wordt vanaf 20 januari 2027 verplicht en vervangt de Machinerichtlijn 2006/42/EG.",
        "Nieuw voor robots: expliciete eisen aan cybersecurity, AI-veiligheid, software-updates over de hele levensduur en bescherming tegen corrupte data.",
        "Conformiteit wordt per deployment beoordeeld, niet alleen per model - context (taak, werkzone, samenwerking met mensen) telt mee.",
        "BotLease draagt deze last als provider en dekt de conformity assessment per locatie af in het leasecontract - geen aparte juridische kosten voor jou.",
    ],
    "toc": [("wat", "1. Wat is de Machineverordening 2023/1230?"),
            ("wanneer", "2. Wanneer geldt ze - de datums"),
            ("nieuw", "3. Wat is nieuw voor humanoïde robots?"),
            ("ai-act", "4. Verschil met de AI-Act"),
            ("checklist", "5. Checklist voor werkgevers"),
            ("botlease", "6. Hoe BotLease dit afdekt")],
    "body": (
        '<h2 id="wat">1. Wat is de Machineverordening 2023/1230?</h2>'
        '<p><b>De Machineverordening (EU) 2023/1230 is de nieuwe Europese wet voor de veiligheid van machines, die vanaf 20 januari 2027 de oude Machinerichtlijn 2006/42/EG vervangt.</b> Omdat het een verordening is (en geen richtlijn), geldt ze direct in alle EU-lidstaten, zonder omzetting in nationale wet. Humanoïde robots vallen er als "machine" volledig onder.</p>'
        '<p>De kern: een machine mag pas op de markt of in gebruik als ze voldoet aan de essentiële gezondheids- en veiligheidseisen, met CE-markering en technische documentatie. Nieuw is dat de verordening expliciet rekening houdt met digitale risico\'s en zelflerende systemen.</p>'
        '<h2 id="wanneer">2. Wanneer geldt ze - de datums</h2>'
        '<p><b>20 januari 2027:</b> de Machineverordening wordt volledig van toepassing; vanaf dan moeten nieuw in gebruik genomen machines eraan voldoen. De Machinerichtlijn 2006/42/EG geldt tot die datum. Voor humanoïde robots die je nú in gebruik neemt, is het dus zaak vooruit te kijken: een robot die je in 2026 inzet, draait in 2027 door onder het nieuwe regime.</p>'
        '<h2 id="nieuw">3. Wat is nieuw voor humanoïde robots?</h2>'
        '<ul>'
        '<li><b>Cybersecurity:</b> bescherming tegen kwaadwillige manipulatie van besturing en data wordt een veiligheidseis.</li>'
        '<li><b>AI &amp; zelflerend gedrag:</b> machines met zelfstandig of lerend gedrag moeten veilig blijven, ook als het gedrag verandert.</li>'
        '<li><b>Software-updates:</b> de fabrikant/provider moet veiligheid borgen over de hele levensduur, inclusief updates - precies relevant bij OTA-updates van humanoids.</li>'
        '<li><b>Corrupte data:</b> de machine moet veilig blijven bij verstoorde sensor- of inputdata.</li>'
        '<li><b>Deployment-context:</b> de risicobeoordeling kijkt naar hoe en waar de robot werkt, niet alleen naar het model.</li>'
        '</ul>'
        '<h2 id="ai-act">4. Verschil met de EU AI-Act</h2>'
        '<p>Twee wetten, één werkvloer. De <b>Machineverordening</b> gaat over fysieke en digitale veiligheid van de machine; de <b>AI-Act</b> over de AI-systemen erin (risicoclassificatie, transparantie, monitoring). Een humanoïde robot moet aan beide voldoen. De volledige uitleg van die samenhang staat in onze <a href="/gids/ai-act-machineverordening">AI-Act &amp; Machineverordening gids</a>.</p>'
        '<h2 id="checklist">5. Checklist voor werkgevers</h2>'
        '<ul>'
        '<li>Inventariseer welke robots/machines je na 20 jan 2027 in gebruik hebt of neemt.</li>'
        '<li>Controleer of de fabrikant CE-markering en technische documentatie onder 2023/1230 levert.</li>'
        '<li>Voer een risicobeoordeling per werkplek/taak uit (werkzones, mens-robot-samenwerking).</li>'
        '<li>Borg cybersecurity en een veilig software-updateproces.</li>'
        '<li>Leg post-market monitoring en incidentregistratie vast.</li>'
        '<li>Train operators en documenteer instructies.</li>'
        '</ul>'
        '<h2 id="botlease">6. Hoe BotLease dit afdekt</h2>'
        '<p>Bij een lease via BotLease ben jij de <i>deployer</i> en wij (samen met de fabrikant) de <i>provider</i>. Wij verzorgen de CE-conformiteit, technische documentatie, cybersecurity en het updateproces, en voeren de conformity assessment per locatie uit - opgenomen in het leasecontract, zonder aparte juridische kosten. EU-gebouwde modellen (<a href="/robots/neura-4ne1-gen3">NEURA</a>, <a href="/robots/pal-tiago-pro">PAL</a>, <a href="/robots/pollen-reachy-2">Pollen</a>) hebben de documentatie het verst klaar. <a href="/#contact">Plan een gratis intake</a> voor een compliance-check van jouw beoogde inzet.</p>'
    ),
    "faqs": [
        ("Wanneer gaat de EU Machineverordening 2023/1230 in?",
         "De Machineverordening (EU) 2023/1230 wordt vanaf 20 januari 2027 volledig van toepassing en vervangt dan de Machinerichtlijn 2006/42/EG. Tot die datum geldt de oude richtlijn."),
        ("Wat verandert de Machineverordening voor humanoïde robots?",
         "Nieuw zijn expliciete eisen aan cybersecurity, AI- en zelflerend gedrag, veilige software-updates over de hele levensduur en bescherming tegen corrupte data. Conformiteit wordt bovendien per deployment beoordeeld, niet alleen per model."),
        ("Heeft een humanoïde robot een CE-markering nodig?",
         "Ja. Onder de Machineverordening moet een humanoïde robot CE-gemarkeerd zijn met bijbehorende technische documentatie voordat hij op de markt of in gebruik wordt genomen. BotLease verzorgt dit als provider."),
        ("Wat is het verschil tussen de Machineverordening en de AI-Act?",
         "De Machineverordening gaat over de fysieke en digitale veiligheid van de machine zelf; de AI-Act over de AI-systemen erin (risicoclassificatie, transparantie, monitoring). Een humanoïde robot moet aan beide voldoen."),
        ("Wie is verantwoordelijk voor de compliance bij een leasecontract?",
         "Bij een lease via BotLease zijn wij samen met de fabrikant de provider en dragen de CE-conformiteit, documentatie en cybersecurity. Jij bent de deployer; wij dekken de conformity assessment per locatie af in het contract."),
    ],
    "cta_h3": "Klaar voor de Machineverordening 2027?",
    "cta_p": "Plan een gratis intake voor een compliance-check van jouw beoogde robotinzet.",
})

# 11. /full-service-lease --------------------------------------------------
PAGES.append({
    "slug": "full-service-lease",
    "title": "Full-service lease humanoïde robot: alles inbegrepen | BotLease",
    "desc": "Full-service lease van humanoïde robots: onderhoud, updates, swap-SLA, verzekering en support in één vast maandbedrag. Het verschil met kale financial lease.",
    "keywords": "full-service lease, operational lease humanoide robot, robot lease onderhoud inbegrepen, all-in robot lease, full service robotlease, robot lease met service",
    "headline": "Full-service lease van humanoïde robots: alles in één maandbedrag",
    "crumbs": [("Home", "/"), ("Full-service lease", "/full-service-lease")],
    "eyebrow": "Full-service lease",
    "h1": "Full-service lease - alles inbegrepen.",
    "tag": "Geen kale financiering met losse onderhoudsfacturen, maar één vast maandbedrag waarin werkelijk alles zit. Zo werkt full-service lease bij BotLease.",
    "tldr": [
        "Full-service lease = één all-in maandbedrag met hardware, installatie, training, onderhoud, onderdelen, swap-SLA, verzekering en support.",
        "Het verschil met financial lease (ABN AMRO, ProfLease e.d.): die financieren alleen de aanschaf - onderhoud, vervanging en risico blijven bij jou.",
        "Je betaalt voor uptime, niet voor een machine: gaat een robot stuk, dan staat er binnen 24 uur een vervangende unit (swap-SLA).",
        "All-in vanaf €290/mnd (Unitree R1) tot €4.890/mnd (Unitree H1-2). Eerste jaar vast, daarna maandelijks opzegbaar.",
    ],
    "toc": [("wat", "1. Wat is full-service lease?"),
            ("vs", "2. Full-service vs financial lease"),
            ("inbegrepen", "3. Wat zit er precies in?"),
            ("waarom", "4. Waarom dit voor robots cruciaal is"),
            ("kosten", "5. Kosten"),
            ("starten", "6. Starten")],
    "body": (
        '<h2 id="wat">1. Wat is full-service lease?</h2>'
        '<p><b>Full-service lease is een leasevorm waarbij niet alleen de hardware, maar ook alle service eromheen in één vast maandbedrag zit.</b> Bij humanoïde robots betekent dat: installatie, training, onderhoud, onderdelen, vervanging, verzekering, software-updates en support - allemaal inbegrepen. Je krijgt een werkende robot als dienst, niet een machine plus een stapel losse contracten. Het is de full-service variant van <a href="/robot-as-a-service">Robot-as-a-Service</a>.</p>'
        '<h2 id="vs">2. Full-service lease vs financial lease</h2>'
        '<p>De meeste leasemaatschappijen bieden <i>financial lease</i>: ze financieren de aanschaf, jij wordt (economisch) eigenaar en draagt zelf onderhoud, vervanging en restwaarderisico. Prima voor een vorkheftruck met een bekende levensduur - maar riskant voor een humanoïde robot, jonge techniek waarvan niemand de onderhoudslast of restwaarde over 3 jaar kent.</p>'
        '<table class="cmp"><thead><tr><th>&nbsp;</th><th>Financial lease</th><th>Full-service lease (BotLease)</th></tr></thead>'
        '<tbody>'
        '<tr><td><b>Wat je financiert</b></td><td>Alleen de aanschaf</td><td>Hardware + alle service</td></tr>'
        '<tr><td><b>Onderhoud &amp; onderdelen</b></td><td>Eigen kosten</td><td>Inbegrepen</td></tr>'
        '<tr><td><b>Vervanging bij defect</b></td><td>Eigen risico</td><td>Swap binnen 24u</td></tr>'
        '<tr><td><b>Restwaarderisico</b></td><td>Jij</td><td>BotLease</td></tr>'
        '<tr><td><b>Op de balans</b></td><td>Ja</td><td>Nee (off-balance)</td></tr>'
        '<tr><td><b>Eén maandbedrag</b></td><td>Nee, losse facturen</td><td>Ja, all-in</td></tr>'
        '</tbody></table>'
        '<h2 id="inbegrepen">3. Wat zit er precies in?</h2>'
        '<p>Het all-in maandbedrag dekt: de hardware (geselecteerd op jouw use-case), installatie en een 2-uurs operatortraining, preventief én correctief onderhoud, alle onderdelen, de swap-SLA (vervangende unit binnen 24 uur, anders €100/dag), WA-verzekering tot €2,5M plus casco, software-updates en remote tuning, en 24/7 Nederlandstalige support. Buiten het maandbedrag vallen alleen de pilot (€1.500), elektriciteit (~€30/mnd) en custom integraties boven 40 uur (€95/uur).</p>'
        '<h2 id="waarom">4. Waarom dit voor robots cruciaal is</h2>'
        '<p>Een humanoïde robot is geen statische machine. Hij krijgt updates, slijt op onvoorspelbare manieren en de techniek veroudert snel. Met full-service lease verschuift dat hele risico - onderhoud, vervanging, veroudering, restwaarde - naar BotLease. Jij houdt een vast, voorspelbaar maandbedrag en gegarandeerde uptime. Dat maakt de businesscase voor het <a href="/mkb">MKB</a> pas echt rond.</p>'
        '<h2 id="kosten">5. Kosten</h2>'
        '<p>All-in van €290/mnd (<a href="/robots/unitree-r1">Unitree R1</a>) tot €4.890/mnd (<a href="/robots/unitree-h1-2">Unitree H1-2</a>). Standaardtermijn 36 maanden, na jaar 1 maandelijks opzegbaar; vanaf 3 units 8% korting. Bekijk alle <a href="/prijzen">prijzen</a> of reken je situatie door in de <a href="/kosten">calculator</a>.</p>'
        '<h2 id="starten">6. Starten</h2>'
        '<p>Begin met een <a href="/#contact">pilot van 4 weken</a> (€1.500). Wij komen binnen 5 werkdagen op locatie, kiezen onafhankelijk een passend model en leveren full-service vanaf dag 1. Geen merk dat we pushen, geen verborgen onderhoudsfacturen.</p>'
    ),
    "faqs": [
        ("Wat is full-service lease van een humanoïde robot?",
         "Een leasevorm waarbij hardware én alle service (installatie, training, onderhoud, onderdelen, vervanging, verzekering, updates en support) in één vast maandbedrag zitten. Je neemt een werkende robot als dienst af, zonder losse onderhoudscontracten."),
        ("Wat is het verschil tussen full-service lease en financial lease?",
         "Financial lease financiert alleen de aanschaf; onderhoud, vervanging en restwaarderisico blijven bij jou en het staat op je balans. Full-service lease (operational lease) is all-in, off-balance, en BotLease draagt onderhoud, vervanging en restwaarderisico."),
        ("Zit onderhoud bij de leaseprijs inbegrepen?",
         "Ja. Bij full-service lease zitten preventief en correctief onderhoud, alle onderdelen en de swap-SLA (vervangende unit binnen 24 uur) in het vaste maandbedrag. Je krijgt geen losse onderhoudsfacturen."),
        ("Wat kost full-service lease van een humanoïde robot?",
         "All-in van €290/maand (Unitree R1) tot €4.890/maand (Unitree H1-2), inclusief alle service. Standaardtermijn 36 maanden, na het eerste jaar maandelijks opzegbaar, vanaf 3 units 8% korting."),
    ],
    "cta_h3": "Alles inbegrepen, één maandbedrag?",
    "cta_p": "Plan een gratis intake. Wij leveren full-service vanaf dag 1 - geen verborgen onderhoudsfacturen.",
})


if __name__ == "__main__":
    for page in PAGES:
        out, n = build(page)
        print(f"✓ {out.relative_to(ROOT.parent)}  ({n} schema blocks, title {len(page['title'])} chars, desc {len(page['desc'])})")
