// Admin endpoint — returns lease-aanvragen uit Supabase voor admin dashboard
// Vereist ADMIN_PASSWORD env var in Vercel
//
// Setup:
//   Vercel project → Settings → Environment Variables
//   Voeg ADMIN_PASSWORD toe (lange random string)

const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || '';
const SUPABASE_URL   = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://hzexwxpnsqggbxklpues.supabase.co';
const SUPABASE_KEY   = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type,Authorization');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { password } = req.body || {};

  if (!ADMIN_PASSWORD) {
    return res.status(503).json({ error: 'ADMIN_PASSWORD niet geconfigureerd. Zet env var in Vercel.' });
  }
  if (!password) {
    return res.status(400).json({ error: 'Password vereist' });
  }
  if (password !== ADMIN_PASSWORD) {
    // Constant-time-ish — same response either way to discourage timing attacks
    await new Promise(r => setTimeout(r, 250 + Math.random() * 250));
    return res.status(401).json({ error: 'Onjuist wachtwoord' });
  }

  if (!SUPABASE_KEY) {
    return res.status(503).json({ error: 'Supabase niet geconfigureerd' });
  }

  try {
    const resp = await fetch(
      `${SUPABASE_URL}/rest/v1/contacts?order=created_at.desc&limit=200`,
      {
        headers: {
          'apikey': SUPABASE_KEY,
          'Authorization': `Bearer ${SUPABASE_KEY}`,
        },
      }
    );
    if (!resp.ok) {
      const err = await resp.text();
      console.error('[admin-list] Supabase error:', err);
      return res.status(500).json({ error: 'Database error: ' + err });
    }
    const rows = await resp.json();
    return res.status(200).json({ success: true, count: rows.length, rows });
  } catch (e) {
    console.error('[admin-list] exception:', e);
    return res.status(500).json({ error: 'Server error' });
  }
}
