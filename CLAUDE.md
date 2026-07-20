# CLAUDE.md — lees dit eerst

Dit bestand wordt automatisch geladen aan het begin van elke sessie. Het is de **wegwijzer** naar het bedrijfshandboek. Lees bij twijfel altijd eerst `docs/handboek/`.

## 🎯 Ons doel (north star) — elke mail en actie dient dit
**Nu:** van gesprekken naar de EERSTE betaalde deal (concreet: VR Expert binnenhalen), terwijl we een goedkope, betrouwbare inkooplijn vastleggen tegen **reseller-/distributeurprijs waarbij WIJ de klant bezitten.**

Houd elke mail aan deze richting:
- **Wij kopen in, wij bezitten de klant.** Geen leads weggeven aan leveranciers (de "you get the leads"-framing was alleen ooit een ruil voor een gratis demo-unit).
- **Nooit voorschieten** — order bij een leverancier pas ná een getekende/aanbetaalde klant.
- **Verhuur/events = eerste omzet, lease = later.** De markt is nog vroeg.
- **Onafhankelijk blijven** — nooit merk-exclusiviteit tekenen; dat is juist onze waarde.
- **Eerlijk, menselijk, geen overpromise.** NL tegen NL/BE-contacten, geen lange streepjes.

## Wat is dit project
**BotLease** (botlease.nl) — eenmanszaak van **Thomas Vedder** (KvK 95943420, Amsterdam). Verhuurt, least en verkoopt humanoïde robots aan Nederlandse/EU-organisaties. Geen B.V. (B.V. komt vóór het eerste getekende contract). Statische site in `frontend/`, eigen CRM + mailsysteem op een VPS.

## ⭐ Begin elke sessie zo
1. **Draai de ochtendbriefing** (toont nieuwe mail, open taken, op wie we wachten):
   `ssh root@185.107.90.42 'python3 /root/botlease-crm/briefing.py'`
1b. **Draai de controle** (vangnet: verloren mail? dubbele leads? reply aan de juiste/laatste mail?) — vóór je mail-werk "klaar" noemt:
   `ssh root@185.107.90.42 'python3 /root/botlease-crm/controle.py'` — moet "0 problemen" tonen.
2. **Lees `docs/handboek/02-stand-van-zaken.md`** — de laatste updates + wie wat deed.
3. Bij een mail/deal-actie: check `docs/handboek/03-pipeline.md` voor de context.

## 📘 DE BLAUWDRUK — nieuw bedrijf starten
Leeft in het blauwdruk-project: **`~/Documents/Python/ai-organisatie-blauwdruk/`** (spiegel: `~/Documents/Python/botlease/blauwdruk/`). Klant-AI-organisatie → `BLAUWDRUK.md` (REF: perduro/backupco). **Eigen webshop/dropship → `playbooks/13-webshop-dropship.md`** (REF: Deskt, deskt.eu — Stripe→CJ-fulfilment, echte foto's, Merchant-feed, Keychain-mail, SEO-3-banen, valkuilen-register). Nieuwe les geleerd? Zelfde dag toevoegen.

## Het handboek (docs/handboek/)
| Bestand | Wat |
|---|---|
| `01-overzicht.md` | Wat BotLease is, fase, het model (huren/lease/event) |
| `02-stand-van-zaken.md` | ⭐ Levend logboek: laatste updates, wie deed wat — **houd dit bij** |
| `03-pipeline.md` | Leveranciers + klanten, status, op wie wachten we — **houd dit bij** |
| `04-team.md` | Thomas, Marinho (financiering), Ton (sales) |
| `05-businessplan.md` | Strategie-samenvatting + links naar volledige plannen |
| `06-techniek.md` | Site, CRM, mail, VPS, deployen, valkuilen |

## Harde regels (NOOIT overtreden)
- **Geen koude mails autonoom versturen** naar externe partijen zonder dat Thomas het per geval autoriseert. Replies in lopende gesprekken mogen wél na zijn "stuur jij maar".
- **NOOIT akkoord/toezeggingen per mail geven namens Thomas.** Geen "akkoord", geen orderbevestiging, geen contractuele instemming, geen "we gaan ermee door", geen ingevulde formulieren terugsturen. Informatieve replies (prijzen, vragen, status) mogen; alles wat instemming of verplichting inhoudt verstuurt Thomas ALTIJD zelf handmatig (7/7/2026).
- **Humanizer over elke mail** — menselijk, geen AI-toon, geen overpromise. **NOOIT lange streepjes (— em-dash of – en-dash) in mails of teksten** — dat verraadt AI. Gebruik gewoon komma's, punten of haakjes. (Geldt voor mails; in code/markdown-tabellen maakt het niet uit.)
- **Taal spiegelen** — Nederlands antwoorden op Nederlandse/Belgische contacten (Dante/VR Expert, Jordi/RoboCorpus), Engels op internationale (Zoe, Dario, Sean, Alexandre). Kijk naar de taal van hún mail.
- **Geen overpromises op de site**: swap = "vervangende unit bij storing, doorgaans binnen enkele werkdagen" (NOOIT "binnen 24u"/"€100/dag"); verzekering = "per deployment geregeld" (NOOIT een bedrag); helpdesk = "op werkdagen" (NOOIT "24/7 support", wel "24/7 inzetbaar" als robot-eigenschap); eventdagprijzen = "excl. btw en reiskosten (vooraf in de offerte)" (NOOIT "transport inbegrepen" beloven; besluit Thomas 7/7).
- **Mail-persona's**: hallo@ = **Lisa (Sales & Planning)**, thomas@ = Thomas Vedder. CRM zet automatisch de juiste From + handtekening. NOOIT mid-thread van identiteit wisselen: lopende gesprekken waar Thomas de bekende afzender is → versturen vanaf thomas@ of met `{"as":"thomas"}` in /api/send.
- **PAL Robotics is verwijderd** (juridisch verzoek) — nooit terugplaatsen. Catalogus = 13 modellen.
- **Mobile-patch-regel**: ~55 pagina's hebben `<style id="mobile-first-patch">` die de generators NIET emitten → die pagina's **in-place editen, nooit rebuilden**. Nieuws (`frontend/nieuws/`) is wél veilig te rebuilden.
- **Geen secrets in de repo** — wachtwoorden/keys staan in `/root/botlease-crm/env` op de VPS en in mijn privé-geheugen, niet in git.

## Deployen (push alleen deployt NIET)
```
git push origin master
git worktree add --detach /tmp/bl origin/master && cp -r .vercel /tmp/bl/.vercel
cd /tmp/bl && vercel --prod --yes && cd - && git worktree remove /tmp/bl --force
```

## Mijn vaste taken (Claude)
- Inkomende mail → concept-antwoorden klaarzetten in het CRM (werklijst).
- Na elke deal-/site-update: `docs/handboek/02-stand-van-zaken.md` + `03-pipeline.md` bijwerken.
- Op verzoek "update mijn crm" / "check inbox": volledige sweep (zie 06-techniek.md).
