# BotLease Design Tokens

> **Single source of truth:** `scripts/style_base.py` → `BASE_CSS`.
> These tokens are CSS custom properties on `:root`. **Never hardcode a hex/px value
> that a token already covers** — use `var(--token)`. If a value is missing, add a token
> here first, then use it everywhere.

Style: **Apple.com cinematic** — Inter typeface, alternating light/dark sections,
rounded tiles, pill buttons. No mono, no brutalist grid lines, no em-dashes.

## Color

### Backgrounds
| Token | Value | Use |
|---|---|---|
| `--bg` | `#fbfbfd` | page background (near-white) |
| `--bg-2` | `#f5f5f7` | subtle/alt sections, footer |
| `--bg-3` | `#eeeef2` | deeper grey tiles |
| `--bg-card` | `#ffffff` | cards on grey |
| `--bg-dark` | `#000000` | dark sections |
| `--bg-dark-2` | `#1d1d1f` | dark cards |

### Borders / lines
| Token | Value |
|---|---|
| `--border` | `#d2d2d7` |
| `--border-hover` | `#86868b` |
| `--border-strong` | `#6e6e73` |
| `--border-dark` | `#424245` |

### Text (ink)
| Token | Value | Use |
|---|---|---|
| `--ink` | `#1d1d1f` | primary text + headings |
| `--ink-2` | `#424245` | secondary (bumped for contrast on grey) |
| `--ink-3` | `#6e6e73` | tertiary |
| `--ink-4` | `#86868b` | quaternary / separators |
| `--ink-on-dark` | `#f5f5f7` | text on dark sections |
| `--ink-2-on-dark` | `#d2d2d7` | secondary on dark |
| `--ink-3-on-dark` | `#a1a1a6` | tertiary on dark |

### Accent (Apple blue) + semantic
| Token | Value | Use |
|---|---|---|
| `--accent` | `#0066cc` | primary actions, links, eyebrows |
| `--accent-2` | `#2997ff` | accent on dark sections |
| `--accent-deep` | `#0058ad` | button hover |
| `--accent-soft` | `#e8f0fe` | tinted backgrounds |
| `--accent-line` | `#b8d4f1` | tinted borders |
| `--green` | `#30d158` | positive / “leverbaar” |
| `--green-soft` | `#e6f8eb` | green tint bg |
| `--rose` | `#ff453a` | negative / alerts |

## Radius
| Token | Value | Use |
|---|---|---|
| `--r-sm` | `8px` | small chips |
| `--r` | `12px` | default cards |
| `--r-lg` | `18px` | large tiles |
| `--r-xl` | `24px` | hero tiles |
| pill | `980px` | buttons, lang switch (literal, not a token) |

## Shadow
| Token | Value |
|---|---|
| `--shadow-xs` | `0 1px 2px rgba(0,0,0,0.04)` |
| `--shadow-sm` | `0 2px 8px rgba(0,0,0,0.06)` |
| `--shadow-md` | `0 8px 24px rgba(0,0,0,0.08)` |
| `--shadow-lg` | `0 24px 56px -16px rgba(0,0,0,0.14)` |

## Typography
- **Family (everything):** `'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Helvetica Neue', sans-serif`
- Loaded via Google Fonts: Inter weights `400;500;600;700;800;900`.
- **Body:** `font-size:17px; line-height:1.5;` antialiased.
- **Headings h1–h4:** `font-weight:700; letter-spacing:-0.03em; line-height:1.05;` color `--ink`.
- **Eyebrow:** `14px / 600`, color `--accent` (`--accent-2` on dark).
- `::selection` → black bg, white text.

## Layout
- `.container` → `max-width:1280px; padding:0 22px` (`40px` ≥780px).
- `.narrow` → `max-width:820px`.
- `section` → `padding:80px 0` (`120px 0` ≥780px).
- `section.dark` / `section.scene.dark` → bg `--bg-dark`, light text.
- `section.subtle` → bg `--bg-2`.

## Hard copy rules
- **No em-dashes (—) or en-dashes (–).** Use ` - ` (spaced hyphen), a colon, or a new sentence.
- **Straight quotes only** (`'` `"`), never smart quotes (`'` `'` `"` `"`).
- Prices: `€9/maand` style. Copyright year: **2026**.
