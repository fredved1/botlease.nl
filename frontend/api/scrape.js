export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') { res.status(200).end(); return; }
  if (req.method !== 'POST') return res.status(405).end();

  let { url } = req.body || {};
  if (!url) return res.status(400).json({ error: 'URL ontbreekt' });

  // Zorg voor https://
  if (!/^https?:\/\//i.test(url)) url = 'https://' + url;

  try {
    const controller = new AbortController();
    // 8s — ruim onder Vercel's 10s platform timeout zodat we altijd JSON terugsturen
    setTimeout(() => controller.abort(), 8000);

    const response = await fetch(url, {
      signal: controller.signal,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
      },
    });

    if (!response.ok) {
      if (response.status === 403 || response.status === 401) {
        return res.status(502).json({ error: 'Deze website blokkeert externe toegang. Probeer je eigen bedrijfswebsite.' });
      }
      if (response.status === 503 || response.status === 429) {
        return res.status(502).json({ error: 'Website tijdelijk niet bereikbaar. Probeer het later opnieuw.' });
      }
      if (response.status === 404) {
        return res.status(502).json({ error: 'Pagina niet gevonden. Controleer de URL en probeer opnieuw.' });
      }
      return res.status(502).json({ error: `Website niet bereikbaar (${response.status}). Probeer je eigen bedrijfswebsite.` });
    }

    const html = await response.text();
    const domain = new URL(url).hostname.replace('www.', '');

    // Strip scripts, styles, nav, footer etc. en haal tekst op
    const text = html
      .replace(/<script[\s\S]*?<\/script>/gi, '')
      .replace(/<style[\s\S]*?<\/style>/gi, '')
      .replace(/<nav[\s\S]*?<\/nav>/gi, '')
      .replace(/<footer[\s\S]*?<\/footer>/gi, '')
      .replace(/<header[\s\S]*?<\/header>/gi, '')
      .replace(/<!--[\s\S]*?-->/g, '')
      .replace(/<[^>]+>/g, ' ')
      .replace(/&nbsp;/g, ' ')
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/\s{2,}/g, ' ')
      .trim()
      .slice(0, 2500);

    // Detecteer bot-verificatie pagina's (CAPTCHA, robot-check, etc.)
    const lowerText = text.toLowerCase();
    const botSignals = [
      'verifieer dat je geen robot', 'prove you are human', 'captcha',
      'access denied', 'just a moment', 'checking your browser',
      'enable javascript and cookies', 'spamvrij', 'echte mensen',
      'echte mens', 'geen robot', 'verify you are human',
      'security check', 'cf-browser-verification', 'ddos protection',
    ];
    if (text.length < 300 || botSignals.some(s => lowerText.includes(s))) {
      return res.status(502).json({ error: 'Deze website vereist een echte browser of blokkeert automatische toegang. Probeer je eigen bedrijfswebsite.' });
    }

    return res.status(200).json({ domain, content: text });
  } catch (err) {
    if (err.name === 'AbortError') return res.status(504).json({ error: 'Website reageert te langzaam. Probeer je eigen bedrijfswebsite.' });
    return res.status(500).json({ error: 'Kon website niet bereiken. Controleer de URL en probeer opnieuw.' });
  }
}
