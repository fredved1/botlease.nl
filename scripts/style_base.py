"""Shared design system — shadcn/ui zinc dark mode, gecombineerd met Fraunces editorial typography.

Inspiratie: v0 Nano Banana template, Vercel.com, Anthropic.com (dark mode versies).
Pure monochrome (zwart/wit/grijs) — geen accent kleur. Hierarchy via typografie en spacing.
"""

FONTS_LINK = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&display=swap" rel="stylesheet">"""

BASE_CSS = """
*,*::before,*::after { margin:0; padding:0; box-sizing:border-box; }

:root {
  /* Surfaces — shadcn zinc dark */
  --bg:           #0a0a0a;
  --bg-2:         #141414;
  --bg-3:         #1f1f1f;
  --bg-card:      #0f0f0f;
  --bg-elevated:  #1a1a1a;
  /* Aliases voor build scripts die deze referenties hadden */
  --bg-dark:      #1a1a1a;
  --bg-darker:    #050505;

  /* Borders — subtle */
  --border:        #262626;
  --border-hover:  #3a3a3a;
  --border-strong: #525252;
  --line:          #262626;
  --line-2:        #3a3a3a;

  /* Ink (text) */
  --ink:    #fafafa;
  --ink-2:  #a3a3a3;
  --ink-3:  #737373;
  --ink-4:  #525252;
  --ink-on-dark:    #fafafa;
  --ink-2-on-dark:  #a3a3a3;
  --ink-3-on-dark:  #737373;

  /* Accent — minimal, near-white voor primaire actions */
  --accent:       #fafafa;
  --accent-2:     #e5e5e5;
  --accent-deep:  #d4d4d4;
  --accent-soft:  rgba(250,250,250,0.06);
  --accent-line:  rgba(250,250,250,0.18);

  /* Semantic — subtiel, alleen voor specifieke contexts */
  --green:      #22c55e;
  --green-soft: rgba(34,197,94,0.10);
  --green-line: rgba(34,197,94,0.25);
  --blue:       #60a5fa;
  --blue-soft:  rgba(96,165,250,0.10);
  --rose:       #fb7185;

  /* Radius — shadcn default 0.5rem */
  --r-sm: 6px;
  --r:    8px;
  --r-lg: 10px;
  --r-xl: 14px;

  /* Shadows — minimaal, voor depth */
  --shadow-xs: 0 1px 2px rgba(0,0,0,0.3);
  --shadow-sm: 0 2px 8px rgba(0,0,0,0.35);
  --shadow-md: 0 8px 24px rgba(0,0,0,0.45);
  --shadow-lg: 0 24px 56px -16px rgba(0,0,0,0.6);
}

html { scroll-behavior:smooth; }
body {
  font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  background:var(--bg); color:var(--ink);
  line-height:1.6; -webkit-font-smoothing:antialiased;
  -moz-osx-font-smoothing:grayscale;
  text-rendering:optimizeLegibility;
  overflow-x:hidden;
}
h1,h2,h3,h4 {
  font-family:'Space Grotesk', system-ui, sans-serif;
  letter-spacing:-0.025em; font-weight:600;
  color:var(--ink); line-height:1.1;
}
.serif { font-family:'Fraunces', Georgia, serif; font-weight:500; letter-spacing:-0.015em; }
a { color:inherit; text-decoration:none; }
img,svg { display:block; max-width:100%; }
button { font-family:inherit; cursor:pointer; }
::selection { background:var(--ink); color:var(--bg); }

.container { max-width:1200px; margin:0 auto; padding:0 24px; }
.narrow    { max-width:760px;  margin:0 auto; padding:0 24px; }
@media (min-width:768px) { .container, .narrow { padding-inline:32px; } }

/* Nav */
nav.top {
  position:sticky; top:0; z-index:80;
  background:rgba(10,10,10,0.72);
  backdrop-filter:saturate(180%) blur(20px);
  -webkit-backdrop-filter:saturate(180%) blur(20px);
  border-bottom:1px solid var(--border);
}
nav.top .row { display:flex; align-items:center; justify-content:space-between; padding:14px 0; }
.brand { display:flex; align-items:center; gap:10px; font-family:'Space Grotesk'; font-weight:600; font-size:18px; letter-spacing:-0.01em; color:var(--ink); }
.brand-mark {
  width:28px; height:28px; border-radius:7px;
  background:var(--ink);
  display:flex; align-items:center; justify-content:center;
}
.brand-mark svg path { stroke:var(--bg); }
.brand-mark svg circle[fill] { fill:var(--bg) !important; }
.nav-links { display:flex; gap:4px; align-items:center; }
.nav-links a {
  color:var(--ink-2); font-size:14px; font-weight:500;
  padding:8px 14px; border-radius:6px;
  transition:color .15s, background .15s;
}
.nav-links a:hover, .nav-links a.active { color:var(--ink); background:var(--bg-3); }

/* Buttons — shadcn style */
.btn {
  display:inline-flex; align-items:center; gap:6px;
  padding:10px 18px; border-radius:8px;
  font-weight:500; font-size:14px; font-family:'Inter',sans-serif;
  background:var(--ink); color:var(--bg);
  border:1px solid var(--ink); cursor:pointer;
  transition:background .15s, opacity .15s;
  white-space:nowrap; text-decoration:none;
}
.btn:hover { background:var(--accent-2); border-color:var(--accent-2); }
.btn.ghost { background:transparent; color:var(--ink); border:1px solid var(--border-strong); }
.btn.ghost:hover { background:var(--bg-3); border-color:var(--border-hover); }
.btn.accent { background:var(--ink); border-color:var(--ink); color:var(--bg); }
.btn.accent:hover { background:var(--accent-2); }
.btn.lg { padding:13px 24px; font-size:15px; border-radius:9px; }
.btn svg { width:14px; height:14px; }

/* Footer */
footer { padding:64px 0 32px; border-top:1px solid var(--border); background:var(--bg); margin-top:96px; }
footer .row { display:flex; justify-content:space-between; flex-wrap:wrap; gap:14px; color:var(--ink-3); font-size:13px; align-items:center; }
footer a { color:var(--ink-2); transition:color .15s; }
footer a:hover { color:var(--ink); }

@media (max-width:780px) { .nav-links { display:none; } }

/* Section common */
section { padding:96px 0; }
@media (min-width:768px) { section { padding:120px 0; } }
section.subtle { background:var(--bg-2); border-top:1px solid var(--border); border-bottom:1px solid var(--border); }
section.dark { background:var(--bg); }

.section-eyebrow {
  display:inline-block;
  font-size:12.5px; font-weight:600; letter-spacing:0.12em;
  text-transform:uppercase;
  color:var(--ink-3);
  margin-bottom:16px;
}

/* Reveal */
@media (prefers-reduced-motion: no-preference) {
  .reveal { opacity:0; transform:translateY(16px); transition:opacity .6s ease, transform .6s ease; }
  .reveal.in { opacity:1; transform:translateY(0); }
}

/* Breadcrumbs */
.crumbs { display:flex; gap:8px; font-size:13px; color:var(--ink-3); margin-bottom:24px; flex-wrap:wrap; }
.crumbs a { color:var(--ink-3); transition:color .15s; }
.crumbs a:hover { color:var(--ink); }
.crumbs .sep { color:var(--ink-4); }
"""

NAV_HTML = """
<nav class="top">
  <div class="container row">
    <a class="brand" href="/">
      <div class="brand-mark"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke-width="2.5" stroke-linecap="round"><path d="M5 9h14v10H5z"/><circle cx="9" cy="14" r="1.2" fill="currentColor"/><circle cx="15" cy="14" r="1.2" fill="currentColor"/><path d="M12 5v4"/></svg></div>
      BotLease
    </a>
    <div class="nav-links">
      <a href="/robots">Robots</a>
      <a href="/vergelijken">Vergelijken</a>
      <a href="/kosten">Kosten</a>
      <a href="/gids/humanoide-robot-leasen">Gids</a>
      <a href="/nieuws">Nieuws</a>
    </div>
    <a href="/#contact" class="btn">Plan demo</a>
  </div>
</nav>
"""

FOOTER_HTML = """
<footer>
  <div class="container row">
    <div>© 2026 BotLease B.V. — Eindhoven · KvK XXXXXXXX</div>
    <div><a href="/">Home</a> · <a href="/robots">Robots</a> · <a href="/vergelijken">Vergelijken</a> · <a href="/kosten">Kosten</a> · <a href="/nieuws">Nieuws</a> · <a href="/over">Over</a> · <a href="/sitemap.xml">Sitemap</a></div>
  </div>
</footer>
"""
