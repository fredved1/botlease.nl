# BotLease Design System

The canonical design system for **botlease.nl**. Style: Apple.com cinematic — Inter,
alternating light/dark scenes, rounded tiles, pill buttons, one accent blue.

**Code source of truth:** `scripts/style_base.py` (`BASE_CSS`, `NAV_HTML`, `FOOTER_HTML`, `LANG_JS`).
Every page is generated HTML — to change style, change the generator, never the output.

## Read in this order
1. **[tokens.md](tokens.md)** — colors, type, radius, spacing (CSS variables). The vocabulary.
2. **[components.md](components.md)** — nav, footer, buttons, sections, breadcrumbs. The shared parts.
3. **[page-recipes.md](page-recipes.md)** — which generator owns which page type + its bespoke components.
4. **[consistency.md](consistency.md)** — known drift, fix status, and the rules that keep it from coming back.

## The one rule
> If two pages look different in a way that isn’t intentional content, it’s a bug.
> One font (Inter), one accent (`--accent` #0066cc), one nav, one footer, one button shape.

## Generators → output
| Generator | Builds | Uses style_base? |
|---|---|---|
| `scripts/style_base.py` | (shared base: nav/footer/fonts/tokens) | — source — |
| `scripts/build_robots.py` | `/robots/*` | yes |
| `scripts/build_news.py` | `/nieuws/*` | yes |
| `scripts/build_guides.py` | `/gids/*`, `/kosten`, `/methodologie`, `/begrippen`, `/over` | yes |
| `scripts/build_landingpages.py` | `/leasen/*`, `/sectoren/*` | yes |
| `frontend/index.html` | `/` homepage | hand-maintained (inline CSS) |
| `gen_seo_pages.py` | `/sectoren/*`, `/vergelijken/*` (legacy) | **no — broken** (`/tmp` template deleted) |

See [consistency.md](consistency.md) for the live drift status across these.
