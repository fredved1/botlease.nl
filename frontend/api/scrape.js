import dnsp from 'node:dns/promises';
import net from 'node:net';

// ── SSRF-guard ────────────────────────────────────────────────────────────
// Blokkeer private / loopback / link-local / metadata / reserved IP-ranges.
function ipv4ToInt(ip) {
  const p = ip.split('.').map(Number);
  if (p.length !== 4 || p.some((n) => Number.isNaN(n) || n < 0 || n > 255)) return null;
  return ((p[0] << 24) >>> 0) + (p[1] << 16) + (p[2] << 8) + p[3];
}
function isBlockedIPv4(ip) {
  const n = ipv4ToInt(ip);
  if (n === null) return true; // onparseerbaar = blokkeer
  const inRange = (cidrBase, bits) => {
    const base = ipv4ToInt(cidrBase);
    const mask = bits === 0 ? 0 : (~0 << (32 - bits)) >>> 0;
    return (n & mask) === (base & mask);
  };
  return (
    inRange('0.0.0.0', 8) || inRange('10.0.0.0', 8) || inRange('100.64.0.0', 10) ||
    inRange('127.0.0.0', 8) || inRange('169.254.0.0', 16) || inRange('172.16.0.0', 12) ||
    inRange('192.0.0.0', 24) || inRange('192.168.0.0', 16) || inRange('198.18.0.0', 15) ||
    inRange('224.0.0.0', 4) || inRange('240.0.0.0', 4)
  );
}
function isBlockedIP(ip) {
  if (net.isIPv4(ip)) return isBlockedIPv4(ip);
  if (net.isIPv6(ip)) {
    const low = ip.toLowerCase();
    if (low === '::1' || low === '::') return true;
    if (low.startsWith('fe80') || low.startsWith('fc') || low.startsWith('fd')) return true; // link-local + ULA
    const m = low.match(/::ffff:(\d+\.\d+\.\d+\.\d+)$/); // IPv4-mapped
    if (m) return isBlockedIPv4(m[1]);
    return false;
  }
  return true;
}
async function hostnameIsSafe(hostname) {
  // IP-literal? direct checken
  if (net.isIP(hostname)) return !isBlockedIP(hostname);
  let addrs;
  try { addrs = await dnsp.lookup(hostname, { all: true }); }
  catch { return false; }
  if (!addrs.length) return false;
  return addrs.every((a) => !isBlockedIP(a.address)); // élke resolved IP moet veilig zijn
}

function originAllowed(req) {
  const src = req.headers.origin || req.headers.referer || '';
  if (!src) return false; // browser-form stuurt altijd Origin; geen = blokkeer
  return /^https?:\/\/(www\.)?botlease\.nl/.test(src) ||
         /^https:\/\/[a-z0-9-]+\.vercel\.app/.test(src) ||
         /^http:\/\/localhost(:\d+)?/.test(src);
}

export default async function handler(req, res) {
  const origin = req.headers.origin;
  if (origin && originAllowed(req)) res.setHeader('Access-Control-Allow-Origin', origin);
  res.setHeader('Vary', 'Origin');
  res.setHeader('Access-Control-Allow-Methods', 'POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') { res.status(200).end(); return; }
  if (req.method !== 'POST') return res.status(405).end();
  if (!originAllowed(req)) return res.status(403).json({ error: 'Verboden' });

  let { url } = req.body || {};
  if (!url || typeof url !== 'string') return res.status(400).json({ error: 'URL ontbreekt' });
  if (!/^https?:\/\//i.test(url)) url = 'https://' + url;

  let current = url;
  try {
    new URL(current);
  } catch { return res.status(400).json({ error: 'Ongeldige URL' }); }

  try {
    const controller = new AbortController();
    setTimeout(() => controller.abort(), 8000);

    // Handmatige redirect-afhandeling met SSRF-revalidatie per hop (max 4)
    let response = null;
    for (let hop = 0; hop < 5; hop++) {
      const u = new URL(current);
      if (!/^https?:$/.test(u.protocol)) return res.status(400).json({ error: 'Alleen http/https toegestaan' });
      if (!(await hostnameIsSafe(u.hostname))) {
        return res.status(400).json({ error: 'Dit adres is niet toegestaan.' });
      }
      response = await fetch(current, {
        signal: controller.signal,
        redirect: 'manual',
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Language': 'nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7',
        },
      });
      if (response.status >= 300 && response.status < 400 && response.headers.get('location')) {
        current = new URL(response.headers.get('location'), current).href; // resolve relatief
        continue;
      }
      break;
    }

    if (!response) return res.status(502).json({ error: 'Website niet bereikbaar.' });
    if (!response.ok) {
      if (response.status === 403 || response.status === 401) return res.status(502).json({ error: 'Deze website blokkeert externe toegang. Probeer je eigen bedrijfswebsite.' });
      if (response.status === 503 || response.status === 429) return res.status(502).json({ error: 'Website tijdelijk niet bereikbaar. Probeer het later opnieuw.' });
      if (response.status === 404) return res.status(502).json({ error: 'Pagina niet gevonden. Controleer de URL en probeer opnieuw.' });
      return res.status(502).json({ error: `Website niet bereikbaar (${response.status}). Probeer je eigen bedrijfswebsite.` });
    }

    const html = await response.text();
    const domain = new URL(current).hostname.replace('www.', '');
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

    const lowerText = text.toLowerCase();
    const botSignals = [
      'verifieer dat je geen robot', 'prove you are human', 'captcha',
      'access denied', 'just a moment', 'checking your browser',
      'enable javascript and cookies', 'spamvrij', 'echte mensen',
      'echte mens', 'geen robot', 'verify you are human',
      'security check', 'cf-browser-verification', 'ddos protection',
    ];
    if (text.length < 300 || botSignals.some((s) => lowerText.includes(s))) {
      return res.status(502).json({ error: 'Deze website vereist een echte browser of blokkeert automatische toegang. Probeer je eigen bedrijfswebsite.' });
    }

    return res.status(200).json({ domain, content: text });
  } catch (err) {
    if (err.name === 'AbortError') return res.status(504).json({ error: 'Website reageert te langzaam. Probeer je eigen bedrijfswebsite.' });
    return res.status(500).json({ error: 'Kon website niet bereiken. Controleer de URL en probeer opnieuw.' });
  }
}
