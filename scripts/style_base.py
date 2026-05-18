"""Shared design system — Apple.com cinematic stijl.

Inter font, alternerend zwart/wit secties, rounded tiles, Apple pill buttons.
Geen mono, geen brutalist grid lines.
"""

FONTS_LINK = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">"""

BASE_CSS = """
*,*::before,*::after { margin:0; padding:0; box-sizing:border-box; }

:root {
  /* Apple-exact colors */
  --bg:          #fbfbfd;
  --bg-2:        #f5f5f7;
  --bg-3:        #eeeef2;
  --bg-card:     #ffffff;
  --bg-dark:     #000000;
  --bg-dark-2:   #1d1d1f;

  /* Borders */
  --border:        #d2d2d7;
  --border-hover:  #86868b;
  --border-strong: #6e6e73;
  --border-dark:   #424245;
  --line:          #d2d2d7;
  --line-2:        #86868b;

  /* Text — Apple greys */
  --ink:    #1d1d1f;
  --ink-2:  #6e6e73;
  --ink-3:  #86868b;
  --ink-4:  #a1a1a6;
  --ink-on-dark:   #f5f5f7;
  --ink-2-on-dark: #86868b;
  --ink-3-on-dark: #6e6e73;

  /* Accent — Apple blue */
  --accent:       #0066cc;
  --accent-2:     #2997ff;
  --accent-deep:  #0058ad;
  --accent-soft:  #e8f0fe;
  --accent-line:  #b8d4f1;

  /* Semantic */
  --green:      #30d158;
  --green-soft: #e6f8eb;
  --green-line: #b4ecbf;
  --blue:       #0066cc;
  --blue-soft:  #e8f0fe;
  --rose:       #ff453a;

  /* Radius — Apple style */
  --r-sm:  8px;
  --r:     12px;
  --r-lg:  18px;
  --r-xl:  24px;
  --r-2xl: 980px;

  /* Shadows */
  --shadow-xs: 0 1px 2px rgba(0,0,0,0.04);
  --shadow-sm: 0 2px 8px rgba(0,0,0,0.06);
  --shadow-md: 0 8px 24px rgba(0,0,0,0.08);
  --shadow-lg: 0 24px 56px -16px rgba(0,0,0,0.14);
}

html { scroll-behavior:smooth; }
body {
  font-family:'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Helvetica Neue', sans-serif;
  background:var(--bg); color:var(--ink);
  font-size:17px; line-height:1.5;
  -webkit-font-smoothing:antialiased;
  -moz-osx-font-smoothing:grayscale;
  text-rendering:optimizeLegibility;
  overflow-x:hidden;
}
h1,h2,h3,h4 {
  font-family:'Inter', -apple-system, sans-serif;
  font-weight:700;
  letter-spacing:-0.03em;
  color:var(--ink); line-height:1.05;
}
a { color:inherit; text-decoration:none; }
img,svg { display:block; max-width:100%; }
button { font-family:inherit; cursor:pointer; }
::selection { background:#000; color:#fff; }

.container { max-width:1280px; margin:0 auto; padding:0 22px; }
.narrow    { max-width:820px;  margin:0 auto; padding:0 22px; }
@media (min-width:780px) { .container, .narrow { padding-inline:40px; } }

/* Nav — Apple compact */
nav.top {
  position:sticky; top:0; z-index:90;
  background:rgba(251,251,253,0.72);
  backdrop-filter:saturate(180%) blur(20px);
  -webkit-backdrop-filter:saturate(180%) blur(20px);
  border-bottom:1px solid rgba(0,0,0,0.06);
  height:48px;
}
nav.top .row { display:flex; align-items:center; justify-content:space-between; height:100%; }
.brand {
  display:flex; align-items:center; gap:8px;
  font-weight:600; font-size:15px; letter-spacing:-0.02em;
  color:var(--ink);
}
.brand-mark {
  width:22px; height:22px; background:var(--ink); border-radius:5px;
  display:flex; align-items:center; justify-content:center;
}
.brand-mark svg path { stroke:var(--bg); }
.brand-mark svg circle[fill] { fill:var(--bg) !important; }
.nav-links { display:flex; gap:0; align-items:center; }
.nav-links a {
  color:var(--ink-2); font-size:12.5px; font-weight:400;
  padding:0 10px; transition:color .15s;
}
.nav-links a:hover, .nav-links a.active { color:var(--ink); }

/* Buttons — Apple pill */
.btn {
  display:inline-flex; align-items:center; gap:4px;
  padding:11px 22px; border-radius:980px;
  font-size:17px; font-weight:400; font-family:inherit;
  background:var(--accent); color:#fff; border:none;
  cursor:pointer; transition:background .15s;
  white-space:nowrap; text-decoration:none;
}
.btn:hover { background:var(--accent-deep); }
.btn.ghost {
  background:transparent; color:var(--accent);
  padding:11px 0;
}
.btn.ghost:hover { background:transparent; color:var(--accent-2); text-decoration:underline; }
.btn.lg { padding:13px 26px; font-size:17px; }
.btn svg { width:11px; height:11px; }

/* Footer */
footer { padding:40px 0 24px; background:var(--bg-2); border-top:1px solid var(--border); color:var(--ink-2); font-size:12px; line-height:1.5; margin-top:0; }
footer .row { display:flex; justify-content:space-between; flex-wrap:wrap; gap:14px; align-items:center; max-width:1280px; margin:0 auto; padding:0 22px; }
footer a { color:var(--ink-2); transition:color .15s; }
footer a:hover { color:var(--ink); }
@media (min-width:780px) { footer .row { padding-inline:40px; } }

@media (max-width:780px) { .nav-links { display:none; } }

/* Sections — Apple style */
section { padding:80px 0; }
@media (min-width:780px) { section { padding:120px 0; } }
section.scene.dark, section.dark {
  background:var(--bg-dark); color:var(--ink-on-dark);
}
section.scene.dark h2, section.dark h2 { color:var(--ink-on-dark); }
section.scene.dark h3, section.dark h3 { color:var(--ink-on-dark); }
section.scene.dark p, section.dark p { color:var(--ink-2-on-dark); }
section.subtle { background:var(--bg-2); }

.eyebrow, .section-eyebrow {
  display:inline-block;
  font-size:14px; font-weight:600;
  color:var(--accent);
  margin-bottom:8px; letter-spacing:-0.005em;
}
section.dark .eyebrow, section.dark .section-eyebrow { color:var(--accent-2); }

/* Reveal */
@media (prefers-reduced-motion: no-preference) {
  .reveal { opacity:0; transform:translateY(20px); transition:opacity .8s ease, transform .8s ease; }
  .reveal.in { opacity:1; transform:translateY(0); }
}

/* Breadcrumbs */
.crumbs { display:flex; gap:8px; font-size:13px; color:var(--ink-2); margin-bottom:24px; flex-wrap:wrap; }
.crumbs a { color:var(--ink-2); transition:color .15s; }
.crumbs a:hover { color:var(--accent); }
.crumbs .sep { color:var(--ink-4); }
"""

NAV_HTML = """
<nav class="top">
  <div class="container row">
    <a class="brand" href="/">
      <div class="brand-mark"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke-width="2.5" stroke-linecap="round"><path d="M5 9h14v10H5z"/><circle cx="9" cy="14" r="1.2" fill="currentColor"/><circle cx="15" cy="14" r="1.2" fill="currentColor"/><path d="M12 5v4"/></svg></div>
      BotLease
    </a>
    <div class="nav-links">
      <a href="/robots">Robots</a>
      <a href="/sectoren">Sectoren</a>
      <a href="/vergelijken">Vergelijken</a>
      <a href="/kosten">Kosten</a>
      <a href="/nieuws">Nieuws</a>
    </div>
    <a href="/#contact" class="btn" style="padding:5px 14px; font-size:13px;">Plan demo</a>
  </div>
</nav>
"""

FOOTER_HTML = """
<footer>
  <div class="row">
    <div>© 2026 BotLease — KvK 95943420 · Vrouwengelukhof 58, 1061BS Amsterdam</div>
    <div><a href="/">Home</a> · <a href="/robots">Robots</a> · <a href="/sectoren">Sectoren</a> · <a href="/nieuws">Nieuws</a> · <a href="/over">Over</a> · hallo@botlease.nl</div>
  </div>
</footer>
"""
