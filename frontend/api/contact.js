const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://hzexwxpnsqggbxklpues.supabase.co';
const SUPABASE_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh6ZXh3eHBuc3FnZ2J4a2xwdWVzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE5Nzg2OTIsImV4cCI6MjA4NzU1NDY5Mn0.Lv8WaPCJuCb_PJIDlSFIjcZ3kEzg9sxGJkJsS3SWihg';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,POST');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { name, email, phone, company, message } = req.body;

  if (!name || !email || !message) {
    return res.status(400).json({ error: 'Naam, email en bericht zijn verplicht' });
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return res.status(400).json({ error: 'Ongeldig email adres' });
  }

  const response = await fetch(`${SUPABASE_URL}/rest/v1/contacts`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'apikey': SUPABASE_KEY,
      'Authorization': `Bearer ${SUPABASE_KEY}`,
      'Prefer': 'return=minimal'
    },
    body: JSON.stringify({ name, email, phone: phone || '', company: company || '', message })
  });

  if (!response.ok) {
    const err = await response.text();
    console.error('Supabase error:', err);
    return res.status(500).json({ error: 'Opslaan mislukt: ' + err });
  }

  return res.status(200).json({
    success: true,
    message: 'Bedankt! We nemen binnen 24 uur contact met u op.'
  });
}
