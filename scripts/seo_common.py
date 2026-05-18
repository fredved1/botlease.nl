"""Shared SEO snippets used by all build scripts.

Plaats deze in <head> en <body> van elke gegenereerde pagina. Door 1 plek te updaten
hoeven we niet door 4 scripts heen als we GA/GSC tokens bijwerken.
"""

# Search engine verification meta tags. User vult in via Search Console.
HEAD_VERIFICATION = """
<meta name="google-site-verification" content="REPLACE-WITH-GSC-TOKEN">
<meta name="msvalidate.01" content="REPLACE-WITH-BING-TOKEN">
""".strip()

# Plausible Analytics — privacy-friendly, EU-hosted, geen cookie banner nodig.
# User maakt account aan op plausible.io en voegt botlease.nl toe — geen code-aanpassing.
PLAUSIBLE_SCRIPT = """
<script defer data-domain="botlease.nl" src="https://plausible.io/js/script.outbound-links.js"></script>
""".strip()

# Combined HEAD snippet
HEAD_SEO = HEAD_VERIFICATION + "\n" + PLAUSIBLE_SCRIPT
