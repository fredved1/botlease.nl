# BotLease Page Recipes

Each page type is generated HTML. To change a page type, edit its generator and
rebuild — but see **[consistency.md](consistency.md)** first: the live HTML also
carries a hand-injected mobile-first-patch + hamburger that the generators do NOT
emit, so a naive rebuild regresses mobile. Until that is reconciled, font/token
fixes are applied to BOTH the generator and the rendered HTML (see `scripts/unify_fonts.py`).

All page types share the canonical nav, footer, fonts, tokens and pill buttons from
`scripts/style_base.py`. Below are the page-specific components each owns.

## Homepage — `frontend/index.html` (hand-maintained)
Flagship single-page, all CSS inline. Already Inter/Apple. Canonical token aliases added.
- **Components:** `hero-compact` (asymmetric text+photo), `.display`/`.display-xl` (clamp 36-96px, accent→accent-2 text gradient), `.tiles`/`.tile` bento product grid, `.spec-strip`, `.process`/`.step`, `.faq` (`<details>`), `.contact-card` form, `.about-strip`, `.trust-strip` with country chips, `.foot` 4-column footer, 10-language switcher, `.nav-burger` hamburger, scroll-reactive `nav.top.dark`.
- **Type scale (the reference):** display 700-900, card `h3` 600/-0.022em, body 17/1.5.

## Robots — `scripts/build_robots.py` → `/robots/*`
- **Components:** `tier-badge` (eu/value/premium pills), `r-hero-grid` (1.2fr/1fr + 4/5 product-art), `r-quick-grid` (6-up spec strip), `spec-table`, `usecases-grid` (numbered), `price-block` (green-check list), `compare-grid`, `hub-card`/`hub-thumb` (catalogus tiles), `video-wrap` (YouTube facade), `waitlist-form`/`aanvraag-form`, `cta-strip`, sector chips.
- **Gotcha:** `_fmt_nl()` must stay scoped to euro amounts only (see consistency.md).

## Nieuws — `scripts/build_news.py` → `/nieuws/*`
- **Components:** `lead-story` (full-bleed hero + overlay), `card-thumb` system (photo / contained art / SVG fallback with `--art-tint`), category pills (`.cat-tag`/`.cat`/`.cat-chip`), `live-badge`, `tldr` callout, article `hero-banner`, `sources` block, `tags`, `cta-strip`, `related-grid`, SVG art library. Layout: lead → 2-col sub-features → 3-col grid.
- **Editorial palette:** per-article `--art-tint` colors (e.g. `#5be584`, `#ffb098`) are intentional variety, NOT drift.
- **Long-form measure:** article body 17px / line-height 1.78 (intentional reading measure).

## Gids + core — `scripts/build_guides.py` → `/gids/*`, `/kosten`, `/over`, `/methodologie`, `/begrippen`, `/vergelijken/*`
- **Components:** `tldr`, `toc`, `section.body` prose (17/1.78), `faq-section`/`faq-item` (+FAQ JSON-LD), `cta-strip`, `calc-grid`/`calc-form`/`calc-out` (lease calculator, dark output panel), `glossary-grid`/`gloss`/`alpha-nav` (A-Z glossary), `cmp-card`/`cmp-grid`, `h2h-grid`/`h2h-card`/`h2h-vs` (head-to-head compare), `crumbs`.

## Leasen + Sectoren — `scripts/build_landingpages.py` → `/leasen/*`, `/sectoren/*`
- **Components:** `metrics-strip` (4-up KPI band), `local-areas` spec-table (Gebied/Postcode/Use-case), `r-grid`/`r-card`, lease-traject ordered process, city/sector FAQ accordion, `cta-strip`, sector chips, `crumbs`.

## Legacy — `gen_seo_pages.py` (DEAD)
Reads a deleted `/tmp/seo_template.html`; not runnable. The pages it once made
(`/sectoren/*`, `/vergelijken/*`) are now owned by `build_landingpages.py` /
`build_guides.py`. Safe to delete `gen_seo_pages.py`.
