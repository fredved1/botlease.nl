// BotLease Analytics Tracker - serverless event collector.
// Client POSTs to /api/track. Server forwards to Umami on VPS (server-to-server,
// no CORS, no mixed content). Returns 204 immediately.

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).end();

  try {
    // sendBeacon stuurt text/plain → Vercel levert req.body als string. Parse hem.
    let body = req.body || {};
    if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
    const ua = req.headers['user-agent'] || '';
    const ref = req.headers['referer'] || '';
    const ip = (req.headers['x-forwarded-for'] || '').split(',')[0].trim();

    const payload = {
      type: body.type || 'event',
      payload: {
        website: '185bb2a6-3057-420f-9f3b-babb2776450f',
        hostname: 'botlease.nl',
        screen: body.screen || '',
        language: body.language || 'nl',
        title: body.title || '',
        url: body.url || '/',
        referrer: body.referrer || ref,
        name: body.name || undefined,
        data: body.data || undefined,
      },
    };

    // Forward to VPS umami. Use HTTP (no SSL on VPS for botlease.nl).
    const r = await fetch('http://185.107.90.42/_u/api/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': ua,
        'X-Forwarded-For': ip,
      },
      body: JSON.stringify(payload),
    });
    const respText = r.ok ? '' : await r.text();

    res.setHeader('Access-Control-Allow-Origin', '*');
    if (r.ok) return res.status(204).end();
    return res.status(202).json({ upstream: r.status, msg: respText.slice(0, 200) });
  } catch (e) {
    return res.status(204).end();
  }
}
