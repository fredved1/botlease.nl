"""Shared SEO snippets used by all build scripts.

Plaats deze in <head> en <body> van elke gegenereerde pagina. Door 1 plek te updaten
hoeven we niet door 4 scripts heen als we GA/GSC tokens bijwerken.
"""

import os

# Search engine verification meta tags. Tokens via ENV variabelen — als ze niet
# gezet zijn worden de meta-tags weggelaten (placeholders zijn schadelijker dan
# afwezigheid; Google zou ze in de source zien en als rare strings indexeren).
#
# Setup:
#   export BOTLEASE_GSC_TOKEN="abc123..."   # uit Google Search Console
#   export BOTLEASE_BING_TOKEN="def456..."  # uit Bing Webmaster Tools
#   (of voeg toe aan Vercel env vars voor production builds)
_gsc = os.environ.get("BOTLEASE_GSC_TOKEN", "").strip()
_bing = os.environ.get("BOTLEASE_BING_TOKEN", "").strip()

_verification_tags = []
if _gsc and _gsc != "REPLACE-WITH-GSC-TOKEN":
    _verification_tags.append(f'<meta name="google-site-verification" content="{_gsc}">')
if _bing and _bing != "REPLACE-WITH-BING-TOKEN":
    _verification_tags.append(f'<meta name="msvalidate.01" content="{_bing}">')

HEAD_VERIFICATION = "\n".join(_verification_tags)

# Multi-layer analytics setup:
# 1. Vercel Web Analytics + Speed Insights (page views + core web vitals, in Vercel UI)
# 2. Custom tracker -> /api/track -> Umami self-hosted (per-page, per-event, custom dashboard)
TRACKERS = """
<script defer src="/_vercel/insights/script.js"></script>
<script defer src="/_vercel/speed-insights/script.js"></script>
<script>
(function(){
  function t(name, data){
    try{
      navigator.sendBeacon('/api/track', JSON.stringify({
        type:'event',
        name:name||undefined,
        data:data||undefined,
        url:location.pathname+location.search,
        title:document.title,
        referrer:document.referrer||'',
        screen:screen.width+'x'+screen.height,
        language:navigator.language
      }));
    }catch(e){}
  }
  // Page view
  t();
  // Expose for custom events
  window.bl_track = t;
  // Outbound clicks
  document.addEventListener('click', function(e){
    var a = e.target.closest('a[href^="http"]');
    if (a && a.hostname && a.hostname !== location.hostname) {
      t('outbound', {url: a.href.slice(0,200)});
    }
  });
  // Scroll depth
  var fired = {};
  window.addEventListener('scroll', function(){
    var h = document.documentElement, b = document.body;
    var pct = Math.round(((h.scrollTop||b.scrollTop)/((h.scrollHeight||b.scrollHeight)-h.clientHeight))*100);
    [50, 90].forEach(function(m){
      if (pct >= m && !fired[m]) { fired[m] = 1; t('scroll', {depth: m}); }
    });
  }, {passive: true});
})();
</script>
""".strip()

# Combined HEAD snippet
HEAD_SEO = HEAD_VERIFICATION + "\n" + TRACKERS


def trim_desc(s: str, max_len: int = 150) -> str:
    """Trim een meta-description naar Google's ~155-char cut-off, op woordgrens.

    Google snijdt descriptions af bij ~155-160 chars op desktop. Te lang = CTR-verlies.
    Te kort = gemiste keyword-density. Sweet spot: 140-155.
    """
    s = " ".join(s.split())  # normaliseer whitespace
    if len(s) <= max_len:
        return s
    cut = s[:max_len]
    # liefst afkappen op een zinsgrens (voorkomt "…en wat zijn realistische.")
    for sep in (". ", "! ", "? "):
        idx = cut.rfind(sep)
        if idx >= 80:
            return cut[:idx + 1]
    last_space = cut.rfind(" ")
    if last_space > 0:
        cut = cut[:last_space]
    return cut.rstrip(",;: .") + "…"
