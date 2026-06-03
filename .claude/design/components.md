# BotLease Components

> Canonical markup + CSS live in `scripts/style_base.py` as `NAV_HTML`, `FOOTER_HTML`,
> `LANG_JS`, and the component rules inside `BASE_CSS`. Every generated page must
> emit these **verbatim** — do not fork the nav/footer per page type.

## Navigation — `nav.top`
- Sticky, `height:48px`, `background:rgba(251,251,253,0.72)` + `backdrop-filter:blur(20px)`, bottom hairline.
- Left: `.brand` = `.brand-mark` (rounded-square SVG monogram) + text **“BotLease”**.
- Center: `.nav-links` → Robots · Sectoren · Vergelijken · Kosten · Nieuws (12.5px, `--ink-2`, hover `--ink`).
- Right: language switcher (`.lang-switch`, 10 languages via Google Translate cookie) + **“Plan demo”** pill (`/#contact`).
- `.nav-links` is hidden `@media (max-width:780px)` → mobile uses the hamburger patch (`#mobile-first-patch`).
- **Source:** `NAV_HTML`. Active link: add `class="active"`.

## Footer — `footer`
- `background:var(--bg-2)`, top border, 12px text.
- Row 1: `© 2026 BotLease - KvK 95943420 · Amsterdam`
- Row 2: Home · Robots · Sectoren · Nieuws · Over · hallo@botlease.nl
- **Source:** `FOOTER_HTML` (also re-includes the language-switcher JS).

## Buttons — `.btn`
| Variant | Style |
|---|---|
| `.btn` | pill `border-radius:980px`, `background:var(--accent)`, white text, `padding:11px 22px`, 17px/400. Hover → `--accent-deep`. |
| `.btn.lg` | `padding:13px 26px`. |
| `.btn.ghost` | transparent, `--accent` text, underline on hover. |
| nav “Plan demo” | `.btn` with `padding:5px 14px; font-size:13px`. |

**Never** introduce square buttons, gradient buttons, or a second accent color.

## Sections & rhythm
- `<section>` vertical padding 80px → 120px (≥780px).
- Alternate light (`--bg`), subtle (`--bg-2`), and dark (`section.dark`, black bg) scenes.
- `.eyebrow` / `.section-eyebrow` → small-caps accent label above a heading.
- `.reveal` → fade-up on scroll (respects `prefers-reduced-motion`).

## Breadcrumbs — `.crumbs`
- 13px, `--ink-2`, `.sep` separators in `--ink-4`, hover `--accent`. Used on robots/gids/sectoren sub-pages.

## Page-specific components
Each page type owns bespoke components (spec-tables, calculators, head-to-head cards,
news lead-story, etc.). These are catalogued per generator in **[page-recipes.md](page-recipes.md)**.
They must still use the shared tokens, Inter, and the pill button — only their layout is bespoke.

## Authoring rules
1. Import nav/footer/fonts from `style_base.py`; never hand-roll them.
2. Use `var(--token)` for every color/radius — see `tokens.md`.
3. One typeface (Inter), one accent (`--accent`), one button shape (pill).
4. No em-dashes, no smart quotes (enforced in copy + LLM prompt for the news bot).
5. New page type → add a generator that imports `style_base`, never a `/tmp` template.
