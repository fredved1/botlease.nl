# BotLease Style Consistency — status & rules

Status of the design-system audit (2026-06-03) and the rules that keep style from
drifting again.

## What was wrong (and is now fixed)

The site had **two competing type systems**:
- **Homepage** = Apple/**Inter** (the recent flagship rebuild).
- **Every sub-page** (robots, nieuws, gids, leasen, sectoren, vergelijken) = legacy
  **editorial**: headings in **Fraunces** serif (Georgia fallback), labels in
  **Space Grotesk**, postcodes in **JetBrains Mono**. This was baked into all 4
  generators AND the rendered HTML — so the whole site rendered serif headings
  while the homepage was sans. That serif/sans split was the visible "verschil in stijl".

### Fixed
| Issue | Fix | Where |
|---|---|---|
| Fraunces / Space Grotesk / JetBrains everywhere | → **Inter** (display headings → weight 700). 1045+ replacements. | `scripts/unify_fonts.py` ran over all HTML + 4 generators |
| 3 font families loaded per page | → canonical **Inter-only** `<link>` (weights 400-900) | all 81 HTML + generators |
| `_fmt_nl()` global `(\d),(\d)` regex corrupted every `rgba()`/grid/JSON comma (broke nav blur, box-shadows, grid columns on robot pages) | → scoped to **euro amounts only** (`€\d{1,3}(,\d{3})+`) | `scripts/build_robots.py`; 59 corrupted values reversed in live robots HTML |
| Off-palette orange `#ffb098` icons on gids index | → `--accent` `#0066cc` | `scripts/build_guides.py` + `frontend/gids/index.html` |
| Homepage used a parallel token vocabulary (`--fg-light` etc.) | → canonical token aliases added (same values) | `frontend/index.html` `:root` |

Verification: 0 legacy-font HTML files, all 81 pages on the canonical Inter link,
0 corrupted CSS, all 4 generators run clean and produce Inter-only output.

## Known open item — generators vs the mobile-first-patch
The 57 rendered pages carry a hand-injected `#mobile-first-patch` style block +
`.nav-burger` hamburger + `.skip-to-main` that **no generator emits** (it was a
one-time injection; no script reproduces it). The generators also produce some
different content than the live HTML (e.g. a robot's Organization-schema city).

**Consequence:** do NOT blindly run a generator over `frontend/` — it strips the
mobile menu and reverts hand-fixes. To make rebuild safe, fold the mobile-first-patch
+ hamburger into `style_base.py` (`NAV_HTML` + `BASE_CSS`) so the canonical source
produces them, then reconcile the content diffs. Until then, patch HTML in place
(as `unify_fonts.py` does) alongside the generator.

## Rules that prevent re-drift
1. **One typeface: Inter.** No Fraunces, Space Grotesk, JetBrains Mono, Georgia, or
   any serif/mono for body. New CSS uses the Inter stack from `tokens.md`.
2. **One accent: `--accent` `#0066cc`.** No second accent; no warm/orange icons
   (news `--art-tint` is the one documented exception).
3. **Use `var(--token)`** for color/radius — never re-hardcode a value a token covers.
4. **Font `<link>` is always** `Inter:wght@400;500;600;700;800;900&display=swap`.
5. **Never run a doc-wide comma→dot (or similar) regex.** Scope number formatting to
   the exact pattern (euro amounts) so it can't corrupt CSS/JSON.
6. **No em-dashes / smart quotes** in copy (enforced for the news bot in its LLM prompt).
7. New page type → a generator that imports `style_base.py`. Never a `/tmp` template
   (that is how `gen_seo_pages.py` died).
8. After any style change, re-verify: `grep -rl "Fraunces\|Space Grotesk\|JetBrains" frontend`
   should be empty, and only the canonical font `<link>` should appear.

## Tools
- `scripts/unify_fonts.py` — idempotent font unifier (HTML + generators). `--check` for dry-run.
