# Wekelijks nieuwsartikel — prompt voor Claude Code CLI

Plaats deze prompt in een cron job op de VPS. Claude Code voert het hele
traject uit: research → schrijf → append → build → commit → push.

## De prompt (kopieer dit precies)

```
Je bent de redactie van botlease.nl. Schrijf en publiceer 1 nieuw nieuwsartikel
voor deze week. Je werkt in /home/<user>/botlease.nl (clone is al up-to-date).

ONDERWERPEN (kies één, prioriteit van boven naar beneden):
1. Recent humanoid-nieuws van deze week (Apptronik, Figure, NEURA, Unitree,
   UBTECH, 1X, Boston Dynamics — gebruik WebSearch voor laatste nieuws)
2. EU AI-Act of Machineverordening 2023/1230 update / interpretatie
3. Nederlandse pilot-case of klantverhaal (3PL, productie, hospitality, zorg)
4. Marktanalyse (Goldman Sachs, Morgan Stanley, IFR rapporten van deze maand)
5. Sector-specifieke deep-dive (1 vd 4 sectoren — 3PL/productie/hospitality/zorg)

WERKWIJZE:
1. WebSearch + WebFetch voor 1-2 recente bronnen over je gekozen onderwerp
2. Open scripts/articles_data.py — bekijk de structuur van bestaande artikelen
3. Append een nieuw artikel-dict aan ARTICLES lijst met velden:
   - slug (URL-friendly, lowercase, hyphens)
   - title (60-70 chars, primary keyword erin)
   - subtitle (1 zin samenvatting, 140-160 chars voor meta-desc)
   - category (Industrie | Regelgeving | Toepassingen | Markt)
   - date (vandaag, formaat YYYY-MM-DD)
   - reading_time (geschat aantal minuten)
   - author (BotLease Redactie)
   - intro (1 inleidende alinea, 80-150 woorden, hookt lezer)
   - body — list van (tag, content) tuples:
     * ("h2", "Sectiekop")
     * ("p", "<paragraph met <a href='/robots/...'>internal links</a> en <b>bold</b>>")
     * ("ul", ["item1", "item2"])
     * ("quote", "...")
   - sources — list van (naam, url) tuples, MIN 2 betrouwbare bronnen
   - tags — list van keywords (4-6 stuks)
4. Open scripts/build_news.py — voeg ART_BY_SLUG entry toe voor de nieuwe slug.
   Kies passende photo + tint:
   - Robot-specifiek: gebruik /img/robots/<slug>-norm.webp + tint van robot tier
   - Algemeen markt/regulering: photo=None + symbol="art-market" of "art-regulation"
5. Run: python3 scripts/build_news.py
6. Verifieer dat de nieuwe HTML-file in frontend/nieuws/<slug>.html staat
7. Voor SEO: zorg dat artikel min 600 woorden heeft, 3+ internal links naar
   bestaande pagina's (/robots/<slug>, /sectoren/<slug>, /gids/<slug>, of andere
   /nieuws/<slug>), en 2+ externe bronnen.

SEO-CHECKLIST (verifieer voor commit):
- [ ] Title bevat primary keyword (humanoid robot, NEURA, Apollo, etc.)
- [ ] Subtitle is 140-160 chars (meta description sweet spot)
- [ ] Slug is keyword-rich en URL-friendly
- [ ] Min 600 woorden, max 1500
- [ ] 3+ <a href="/..."> interne links
- [ ] 2+ externe <a href="https://..."> bronnen
- [ ] H2-headers met secondaire keywords
- [ ] Verwijst naar Nederlandse context (NL markt, MKB, EU regelgeving)
- [ ] Vermijd: marketing-fluff, ongedocumenteerde claims, supplier-namen
  (bv. "via RobotShop EU" is intern, NIET publiceren)

COMMIT MESSAGE format:
```
news: <korte titel> ({date})

<1-line summary van de inhoud>

Sources: <urls>
```

DEPLOY:
- git push origin master triggert Vercel auto-deploy
- Sitemap.xml en RSS worden automatisch bijgewerkt door build_news.py

Voer alles uit. Geen vragen stellen — je hebt volledige autonomie. Stop pas
als de push succesvol is (geen errors).
```

## Cron entry voor VPS (crontab -e)

```bash
# Elke maandag 09:00 NL tijd: nieuw artikel publiceren
0 9 * * 1 /home/<user>/botlease.nl/scripts/cron_weekly_article.sh >> /var/log/botlease-news.log 2>&1
```

## Setup voor één-malig

```bash
# Op VPS:
cd /home
git clone git@github.com:fredved1/botlease.nl.git
cd botlease.nl

# Claude Code CLI installeren (als nog niet):
curl -fsSL https://claude.ai/install.sh | bash
# Of: npm install -g @anthropic-ai/claude-code

# Auth (eenmalig):
claude login

# Test handmatig:
bash scripts/cron_weekly_article.sh

# Bij succes: voeg cron toe (zie hierboven)
crontab -e
```
