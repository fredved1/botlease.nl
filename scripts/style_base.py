"""Shared editorial light design system voor alle pagina's.

Importeer in elke build script en gebruik {BASE_CSS}, {NAV_HTML}, {FOOTER_HTML}.
Page-specific CSS bouwt voort op deze tokens.
"""

FONTS_LINK = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&display=swap" rel="stylesheet">"""

BASE_CSS = """
*,*::before,*::after { margin:0; padding:0; box-sizing:border-box; }

:root {
  /* Surfaces — warm cream */
  --bg:         #faf9f6;
  --bg-2:       #f3f1ec;
  --bg-3:       #ebe8e1;
  --bg-card:    #ffffff;
  --bg-dark:    #1c1917;
  --bg-darker:  #0c0a09;

  /* Borders */
  --border:        #e7e5e0;
  --border-hover:  #d4d1c8;
  --border-strong: #a8a29e;
  --line:          #e7e5e0;
  --line-2:        #d4d1c8;

  /* Ink */
  --ink:    #1c1917;
  --ink-2:  #44403c;
  --ink-3:  #78716c;
  --ink-4:  #a8a29e;
  --ink-on-dark:    #fafaf9;
  --ink-2-on-dark:  #d6d3d1;
  --ink-3-on-dark:  #a8a29e;

  /* Accent — refined terracotta */
  --accent:       #c2410c;
  --accent-2:     #ea580c;
  --accent-deep:  #9a3412;
  --accent-soft:  #fff7ed;
  --accent-line:  #fed7aa;

  /* Semantic */
  --green:      #15803d;
  --green-soft: #f0fdf4;
  --green-line: #bbf7d0;
  --blue:       #1d4ed8;
  --blue-soft:  #eff6ff;
  --rose:       #be123c;

  /* Radius */
  --r-sm: 6px;
  --r:    10px;
  --r-lg: 14px;
  --r-xl: 20px;

  /* Shadows */
  --shadow-xs: 0 1px 2px rgba(28,25,23,0.04);
  --shadow-sm: 0 2px 8px rgba(28,25,23,0.06);
  --shadow-md: 0 8px 24px rgba(28,25,23,0.08);
  --shadow-lg: 0 24px 56px -16px rgba(28,25,23,0.12);
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
::selection { background:var(--accent); color:#fff; }

.container { max-width:1200px; margin:0 auto; padding:0 24px; }
.narrow    { max-width:760px;  margin:0 auto; padding:0 24px; }
@media (min-width:768px) { .container, .narrow { padding-inline:32px; } }

/* Nav */
nav.top {
  position:sticky; top:0; z-index:80;
  background:rgba(250,249,246,0.85);
  backdrop-filter:saturate(180%) blur(20px);
  -webkit-backdrop-filter:saturate(180%) blur(20px);
  border-bottom:1px solid var(--border);
}
nav.top .row { display:flex; align-items:center; justify-content:space-between; padding:16px 0; }
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
  color:var(--ink-2); font-size:14.5px; font-weight:500;
  padding:8px 14px; border-radius:8px;
  transition:color .15s, background .15s;
}
.nav-links a:hover, .nav-links a.active { color:var(--ink); background:var(--bg-2); }

/* Buttons */
.btn {
  display:inline-flex; align-items:center; gap:6px;
  padding:10px 18px; border-radius:8px;
  font-weight:500; font-size:14.5px; font-family:'Inter',sans-serif;
  background:var(--ink); color:var(--ink-on-dark);
  border:1px solid var(--ink); cursor:pointer;
  transition:transform .15s, background .15s, box-shadow .2s;
  white-space:nowrap; text-decoration:none;
}
.btn:hover { background:var(--bg-darker); transform:translateY(-1px); box-shadow:var(--shadow-sm); }
.btn.ghost { background:transparent; color:var(--ink); border:1px solid var(--border-strong); }
.btn.ghost:hover { background:var(--bg-2); border-color:var(--ink); }
.btn.accent { background:var(--accent); border-color:var(--accent); color:#fff; }
.btn.accent:hover { background:var(--accent-deep); border-color:var(--accent-deep); }
.btn.lg { padding:13px 24px; font-size:15px; border-radius:10px; }
.btn svg { width:14px; height:14px; }

/* Footer */
footer { padding:72px 0 32px; border-top:1px solid var(--border); background:var(--bg-2); margin-top:120px; }
footer .row { display:flex; justify-content:space-between; flex-wrap:wrap; gap:14px; color:var(--ink-3); font-size:13px; align-items:center; }
footer a { color:var(--ink-2); transition:color .15s; }
footer a:hover { color:var(--accent); }

@media (max-width:780px) { .nav-links { display:none; } }

/* Section common */
section { padding:96px 0; }
@media (min-width:768px) { section { padding:120px 0; } }
section.subtle { background:var(--bg-2); }
section.dark { background:var(--bg-dark); color:var(--ink-on-dark); }
section.dark h2 { color:var(--ink-on-dark); }
section.dark p { color:var(--ink-2-on-dark); }

.section-eyebrow {
  display:inline-block;
  font-size:12.5px; font-weight:600; letter-spacing:0.12em;
  text-transform:uppercase;
  color:var(--accent);
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
.crumbs a:hover { color:var(--accent); }
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
