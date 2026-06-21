# 02 — Stand van zaken (levend logboek)

> ⭐ Dit is het belangrijkste bestand om bij te houden. Nieuwste update bovenaan. Datum + wat + door wie.

## 2026-06-21
- **⭐ SEO/GEO-sprint uitgevoerd + live** (audit-workflow: 7 dimensies + adversariële tegencheck). Kerncorrectie: de **rank-bot** (`seo/seo_data.json`, Google.nl-scrape 19 juni) toont **#1 op "humanoïde robot leasen Nederland" + Engelse variant** (2/23 keywords; "huren" + de rest nog 0). De WebSearch-tool is US-only en gaf vals "ranken nergens" → voor NL-rankings de rank-bot gebruiken, niet WebSearch.
- **Verhuur-first on-page** ("huren" rankt nog 0, is north-star): homepage H1 = "Humanoïde robot huren of leasen" (was leasen-only) + hero leidt met huren; /huren-title ingekort. Homepage is de doelpagina voor de huren-zoekwoorden.
- **PAL-compliance (was nog LIVE!):** PAL uit `sitemap-images.xml` (stale 22-mei-versie met merknaam + oude prijzen) → vers gegenereerd via `render_image_sitemap()`. PAL + pal-robotics.com-link uit nieuws (`articles_data.py`) + uit `landingpages_data.py` (latent, kwam bij rebuild terug). "15 modellen"→13 (template + 4 artikelen). Dode `pal-kangaroo`-keyword uit `seo_data.json`. **0 PAL publiek** nu.
- **Favicon toegevoegd** (bestond niet → geen icoon in Google/tabs): `favicon.ico`+png's uit `logo.png` + link-tags op homepage. Google-icoon volgt bij volgende crawl.
- **Hygiëne:** 5 meta-descriptions <155 (steden weer uniek), em-dash uit indexable titles, telefoon in Organization/ContactPoint-schema + `llms.txt`, ItemList op "beste robots 2026"-listicle, tel:-belknop in footer, verse sitemap-lastmods. 4× gedeployed, alles geverifieerd live.
- **Off-site (Thomas):** GSC sitemap + herindexering ✅, Bing-import ✅. **NLrobotics = betaald → overgeslagen.** Volgende gratis stappen: LinkedIn-bedrijfspagina (tekst klaar in `OUTREACH/07-linkedin-company.md`, **Thomas doet morgen**) → Google Bedrijfsprofiel (`12-google-business.md`) → directories. Beide drafts gecorrigeerd (geen PAL/15 modellen/24u). **Zodra LinkedIn + GBP live: `sameAs` site-breed toevoegen** (laatste entity-schakel). Nog open on-site: hreflang nl-BE (staat op slechts 2/80 pagina's → aparte uitrol), event-per-stad/beurs-pagina's.

## 2026-06-20
- **⭐ Compliance-deepdive → businessplan v1.2 (§9A "Compliance als kerncompetentie").** Diep onderzoek (workflow: 5 dimensies + juridische toets + strategie) op de 5 vragen die Dante/VR Expert stelde en die naar Dario doorgespeeld zijn: CE/Machineverordening 2023/1230, EU AI Act (G1 = niet hoog-risico voor deze inzet; wel art. 4/5/50), data-naar-China + AVG/Schrems II + cyber (RED/CRA), aansprakelijkheid (PLD 2024/2853, importeurspunt) + verzekering, turnkey/veiligheid. Kern: **wie buiten de EU inkoopt wordt "importeur" met fabrikant-plichten → dat is juist onze rol en moat.** Eerlijke nuances meegenomen: B.V. is géén aansprakelijkheidsschild voor het product, verzekerbaarheid is een open risico, mei-2026-richtsnoeren/Digital Omnibus nog niet definitief, EU-DoC voor G1 per levering opvragen i.p.v. aannemen. + compliance-tijdlijn (nu vs later) en aanpalende regimes (NIS2/GPSR/batterij/recall/boetes).
- **Dante-strategie vastgelegd** (03-pipeline + §9A): hij is zelf verhuurder, dus klant-die-concurrent-kan-worden. Open over veiligheid, **gesloten over de inkoopketen**; nooit bron/prijs/marge, geen kale unit/testunit, geen exclusiviteit, niets voorschieten. Verkoop ontzorging, niet "een G1".

## 2026-06-19
- **⭐ Nieuws-engine gerepareerd + weer live.** Oorzaak waarom er sinds ~11 juni niets verscheen: (1) het schrijven liep via OpenRouter en dat tegoed was op (402) → de bot las wel feeds maar schreef niets, stil; (2) de VPS-nieuwsclone hing 100 commits achter + had een dirty tree → `git pull/push` faalde elke run, dus zelfs gegenereerde artikelen bereikten GitHub/site nooit (8 artikelen van 12 juni stonden er onverstuurd). Fixes: schrijven loopt nu primair via de **`claude` CLI (jouw Claude Code-abonnement)**, self-refreshing, geen API-kosten (OAuth-API + OpenRouter als vangnet). Clone herbouwd als schone checkout. **Durable runner** `scripts/run_news_vps.sh` (in git → overleeft her-clone) doet pull → schrijven → commit → push → **deploy** met luide foutdetectie. `VERCEL_TOKEN` op de VPS gezet zodat de VPS zelf deployt (push deployt niet vanzelf; CLI ook geüpgraded 47→54). **2 verse artikelen live**: halve-marathon-robot (50:26, Honor) + MotionDisco (zelf-ontdekte humanoid-skills). Wekelijkse timer (vr 17:00) staat aan.
- **NEURA (Kristina) + RobotShop (Nathy) reageerden** → 2 concept-replies klaargezet in de werklijst (open, niet verstuurd). RobotShop: **geen reseller mogelijk** (contractueel), 5% standaard, heroverweegt bij volume. NEURA: kwalificeert rond NEURA Gym (intern budget) — past matig op ons model; reply verheldert onze positie + vraagt partnerprijs 4NE-1.
- **Dario (Synergy) nog geen reactie** → VR Expert-marge + complete Dante-mail wachten nog op zijn compliance-antwoorden.
- Controle: 0 problemen (mail-dekking, geen dubbele leads, threading ok). 10 van 12 nieuwe mails waren privé recreatie-replies (campings/koophuisje) — bewust buiten het CRM gehouden.
- **Businessplan bijgewerkt naar v1.1** (audit-workflow: 4 dimensies → adversariële verificatie → 7 geverifieerde edits): nieuws-engine als content-/SEO-motor toegevoegd (§1+§8), NEURA-nuance (Gym/co-development, past matig op ons model) + RobotShop reseller-stand aangescherpt (§7), Machineverordening-datum consistent gemaakt (§3: 2023/1230 vanaf jan 2027), Automation Xperience naar verleden (§8), en een interne inconsistentie rechtgetrokken (R1 inkoop €6k→~€5k in §10.1, gelijk aan §4/site).
- **Prijs-bronfix:** `scripts/robots_data.py` had G1 `purchase_eur` nog op €23.000 terwijl canon + live site €16.000 zijn → bron op €16.000 gezet (latente rebuild-bug). Geen rebuild nodig (live stond al goed).

## 2026-06-18
- **⭐ RobotShop-offerte binnen (PDF Bid 1482037, t/m 30 juli):** G1 EDU U1 €29.925, U2 €34.200 (5% korting, ex btw). EU, geen import, 18mnd garantie, ETA 8-12 wk. → tweede inkoopprijs. **Voor U2 goedkoper dan China.** PDF in `docs/leveranciers/`. Reply gestuurd (offerte bevestigd + volume-korting gevraagd).
- **UBTECH (Sean) opent directe lijn** ("you can source directly from UBTech") → reply gestuurd: Walker S2 reseller-prijs gevraagd.
- **3 inkoopprijzen-overzicht (G1 EDU):** Unitree China ~€28k/€35.3k (import-gedoe) · RobotShop EU €29.925/€34.200 (simpel) · Synergy (Dario) = nog open. Vergelijking in businessplan §5b.
- **Systeemfout opgelost:** oude mail-catcher (botlease-mail) UIT — die importeerde elke mail nóg eens zonder msgid (= bron dubbele leads). Poller dekt nu alles. + les: nooit handmatig leads inserten voor inkomende mail (poller doet dat al). 2 lessen in 06-techniek.md.
- **Streepje-garantie:** CRM-versturen strijkt nu automatisch elk em/en-streepje uit onze tekst (Thomas: "never"). 3 niveaus: CLAUDE.md + playbook + verzendfilter.
- **Businessplan §1 rechtgetrokken:** eenmanszaak (geen B.V.), 13 modellen, tractie geactualiseerd.

## 2026-06-17 (later)
- **Volledige contact-check gedraaid (geverifieerd schoon, 0 problemen):** 4 replies klaar (Zoe [4], RobotShop [1], RoboCorpus [2] NL, UBTECH [3]), allemaal aan de juiste laatste mail / juiste adres / juiste taal. 5 contacten wachten correct op de ander. Geen verloren mail, geen dubbele leads.
- **Vangnet `controle.py` gebouwd** (verloren mail / dubbele leads / reply aan juiste+laatste mail) — vaste verificatiestap vóór "klaar". Fixte onderweg: Zoe-reply hing aan oude mail i.p.v. de offerte; RobotShop-adres → Reply-To (marketplace@); Atlas Copco-email; Richard-lead datum.

## 2026-06-17
- **⭐ UNITREE-OFFERTE BINNEN (Zoe, 16/6):** G1 EDU U1 $28.900/unit, U2 $36.900/unit + $1.500 shipping (CPT, 100% vooruit, 4-5 wk). Verwerkt in businessplan §5b + `docs/leveranciers/unitree-offerte-2026-06-16.md`. **Vondst:** echte prijs (~€28-35k landed) is hóger dan de €23k op de site → leaseprijs/positionering heroverwegen zodra EU-prijzen (RobotShop/Synergy) ernaast liggen.
- **Businessplan §5b toegevoegd:** leveranciers + echte inkoopprijzen + alle contacten + klantenpijplijn.
- **Bedrijfshandboek aangemaakt** (`CLAUDE.md` + `docs/handboek/`) zodat elke (nieuwe) sessie meteen de stand kent.
- **3 mails klaargezet** in de CRM-werklijst: [1] RobotShop (versie opgeven → offerte — nu extra belangrijk: 2e prijs naast Zoe), [2] RoboCorpus, [3] UBTECH. Zie `03-pipeline.md`.

## 2026-06-16
- **VR Expert (Dante) stuurde uitgebreide vragenmail** (lease­prijs + wat inbegrepen + compliance/CE/data-naar-China/firmware/kant-en-klaar). Technische+compliance-vragen **doorgespeeld naar Dario (Synergy)** — mail verstuurd vanuit thomas@. Wachten op Dario's antwoord vóór we Dante's voorstel doorrekenen.
- **UBTECH (Sean) verwees naar SmartRobot Solutions** (= grootste NL-concurrent) voor lease. Besluit: niet via concurrent inkopen, directe lijn proberen.
- **Site-eindcheck (74-agent swarm, adversarieel geverifieerd):** 40 echte fouten gefixt — 139 kapotte rgba()-CSS-waarden (eigen eerdere fout), overpromises (24u swap, 24/7 support, levering-5-werkdagen, verzonnen "Eindhoven HQ"), afgebroken meta's, ontbrekende og-tags, prijzentabel gesorteerd. Site is nu professioneel/consistent.

## 2026-06-15
- **Mailsysteem volledig op IMAP**: CRM leest nu rechtstreeks inkomende + uitgaande mail van hallo@ én thomas@ (geen kwetsbare doorstuur-omweg meer). Versturen vanuit CRM kan vanaf beide adressen (afzender-keuze) + komt in de Verzonden-map + threadt als echte reply met geciteerde historie.
- **Verhuur-first → teruggedraaid naar rustig**: homepage was te druk met verhuur; teruggezet naar lease-focus met verhuur subtiel + keuze-per-robot in het bestelformulier (vorm kiezen, prijs past live aan, keuze komt mee in CRM).
- **11 mails verstuurd** (Zoe-offerte, UBTECH-reply, 9 leverancier-follow-ups). Synergy (Dario, CEO/Unitree-distributeur ES) reageerde: open voor distributeur-prijzen.

## 2026-06-12
- **PAL-meeting (Alexandre) bij NDSM** — ging goed, van incident naar partner-pad. PAL stuurt een formulier (robotics-assessment); op basis daarvan beoordeelt PAL partnership. Echte inkoopprijzen: TIAGo ~€110k, StockBot ~€30k. Wacht op zijn formulier.

## 2026-06-11
- **Unitree (Zoe) stuurde selection table + CE-certificaat (RED, niet Machineverordening).** Condities: staffelkorting pas >$50k, 100% vooruit, 4-5 wk incl. verzending, $1.500 shipping/unit. Offerte U1+U2 aangevraagd.
- **PAL volledig van de site verwijderd** (juridisch verzoek Alexandre) → catalogus 13 modellen.
- **Prijs-restructure**: 8 modellen kostendekkend geherprijsd (canon v2, €290–€6.650).

## Eerder (samengevat)
- CRM + mailsysteem gebouwd op VPS; site SEO/GEO af; nieuws-engine; concurrentie/haalbaarheidsanalyse gemaakt; verhuurpagina's live. Details in de overige handboek-bestanden en `docs/`.

---
**Bijhouden:** voeg na elke betekenisvolle actie (mail verstuurd, deal-update, site-wijziging, besluit) een regel bovenaan toe. Houd het kort.
