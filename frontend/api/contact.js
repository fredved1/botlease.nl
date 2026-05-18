// Vercel serverless function — handles contact form submissions
// Sends email to hallo@botlease.nl via Resend (resend.com) + backup to Supabase
//
// REQUIRED ENV VARS (set in Vercel project settings):
//   RESEND_API_KEY      → API key from resend.com (free 3000/mo)
//   RESEND_FROM         → optional, default "BotLease <onboarding@resend.dev>"
//                         set to "BotLease <noreply@botlease.nl>" na domain verification
//
// OPTIONAL (Supabase backup, oude config):
//   NEXT_PUBLIC_SUPABASE_URL / NEXT_PUBLIC_SUPABASE_ANON_KEY

const RESEND_API_KEY = process.env.RESEND_API_KEY || '';
const RESEND_FROM    = process.env.RESEND_FROM    || 'BotLease <onboarding@resend.dev>';
const NOTIFY_TO      = 'hallo@botlease.nl';

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://hzexwxpnsqggbxklpues.supabase.co';
const SUPABASE_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';

function escapeHtml(s) {
  return String(s || '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#039;');
}

async function sendNotification(data) {
  if (!RESEND_API_KEY) {
    console.warn('[contact] RESEND_API_KEY ontbreekt — email niet verstuurd. Submission:', data);
    return { skipped: true };
  }
  const html = `
    <div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:600px;margin:0 auto;padding:24px;background:#f7f7f9;color:#08080a">
      <h2 style="font-family:'Space Grotesk',sans-serif;color:#08080a;margin:0 0 18px;font-size:22px">Nieuwe lease-aanvraag — BotLease</h2>
      <div style="background:white;border:1px solid #e4e4e7;border-radius:10px;padding:24px;margin-bottom:14px">
        <p style="margin:0 0 14px;font-size:13px;color:#71717a;text-transform:uppercase;letter-spacing:0.08em">Contactgegevens</p>
        <p style="margin:4px 0"><b>Naam:</b> ${escapeHtml(data.naam)}</p>
        <p style="margin:4px 0"><b>Bedrijf:</b> ${escapeHtml(data.bedrijf)}</p>
        <p style="margin:4px 0"><b>Email:</b> <a href="mailto:${escapeHtml(data.email)}">${escapeHtml(data.email)}</a></p>
        ${data.telefoon ? `<p style="margin:4px 0"><b>Telefoon:</b> ${escapeHtml(data.telefoon)}</p>` : ''}
      </div>
      <div style="background:white;border:1px solid #e4e4e7;border-radius:10px;padding:24px;margin-bottom:14px">
        <p style="margin:0 0 14px;font-size:13px;color:#71717a;text-transform:uppercase;letter-spacing:0.08em">Use-case</p>
        <p style="margin:4px 0"><b>Sector:</b> ${escapeHtml(data.usecase || 'Niet opgegeven')}</p>
        ${data.bericht ? `<p style="margin:14px 0 4px"><b>Bericht:</b></p><p style="margin:0;white-space:pre-wrap;color:#3f3f46">${escapeHtml(data.bericht)}</p>` : ''}
      </div>
      <p style="font-size:12px;color:#71717a;margin:18px 0 0">
        Ingestuurd via botlease.nl op ${new Date().toLocaleString('nl-NL', { timeZone: 'Europe/Amsterdam' })}.
        Reageer op deze email om direct te antwoorden.
      </p>
    </div>
  `;

  const resp = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: RESEND_FROM,
      to: [NOTIFY_TO],
      reply_to: data.email,
      subject: `[BotLease] Lease-aanvraag van ${data.bedrijf || data.naam} — ${data.usecase || 'algemeen'}`,
      html,
    }),
  });

  if (!resp.ok) {
    const err = await resp.text();
    console.error('[contact] Resend error:', resp.status, err);
    throw new Error(`Resend ${resp.status}`);
  }
  return await resp.json();
}

async function sendConfirmation(data) {
  if (!RESEND_API_KEY || !data.email) return { skipped: true };
  const html = `
    <div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:600px;margin:0 auto;padding:24px;background:#f7f7f9;color:#08080a">
      <h2 style="font-family:'Space Grotesk',sans-serif;color:#08080a;margin:0 0 18px;font-size:22px">Bedankt voor je aanvraag — BotLease</h2>
      <p style="font-size:15px;line-height:1.6">Hallo ${escapeHtml(data.naam)},</p>
      <p style="font-size:15px;line-height:1.6">Bedankt voor je interesse in humanoïde robot leasing via BotLease. We hebben je aanvraag goed ontvangen en nemen binnen <b>4 werkuren</b> contact op via ${escapeHtml(data.email)}.</p>
      <p style="font-size:15px;line-height:1.6">In de tussentijd kun je vrijblijvend rondkijken:</p>
      <ul style="font-size:15px;line-height:1.7">
        <li><a href="https://botlease.nl/robots" style="color:#f97316">Volledige robotcatalogus</a> — 15 modellen vergeleken</li>
        <li><a href="https://botlease.nl/gids/humanoide-robot-leasen" style="color:#f97316">Complete lease-gids</a></li>
        <li><a href="https://botlease.nl/kosten" style="color:#f97316">Bereken je lease-prijs</a></li>
      </ul>
      <p style="font-size:15px;line-height:1.6;margin-top:24px">Vragen tussendoor? Antwoord op deze email of bel direct.</p>
      <p style="font-size:15px;line-height:1.6">— Team BotLease</p>
      <hr style="border:none;border-top:1px solid #e4e4e7;margin:24px 0">
      <p style="font-size:12px;color:#71717a">BotLease B.V. · Eindhoven · hallo@botlease.nl · botlease.nl</p>
    </div>
  `;
  const resp = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: RESEND_FROM,
      to: [data.email],
      subject: 'Bedankt voor je aanvraag — BotLease',
      html,
    }),
  });
  if (!resp.ok) {
    console.warn('[contact] Confirmation failed:', resp.status);
  }
  return resp.ok ? await resp.json() : { error: true };
}

async function backupToSupabase(data) {
  if (!SUPABASE_KEY) return { skipped: true };
  try {
    const resp = await fetch(`${SUPABASE_URL}/rest/v1/contacts`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'apikey': SUPABASE_KEY,
        'Authorization': `Bearer ${SUPABASE_KEY}`,
        'Prefer': 'return=minimal',
      },
      body: JSON.stringify({
        name:    data.naam,
        email:   data.email,
        phone:   data.telefoon || '',
        company: data.bedrijf  || '',
        message: `[${data.usecase || 'algemeen'}] ${data.bericht || ''}`.trim(),
      }),
    });
    if (!resp.ok) {
      console.warn('[contact] Supabase backup failed:', await resp.text());
    }
  } catch (e) {
    console.warn('[contact] Supabase exception:', e.message);
  }
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const data = req.body || {};
  // Support both old field names (name/email/message) and new (naam/email/bericht)
  const naam     = data.naam     || data.name    || '';
  const email    = data.email    || '';
  const bedrijf  = data.bedrijf  || data.company || '';
  const telefoon = data.telefoon || data.phone   || '';
  const usecase  = data.usecase  || '';
  const bericht  = data.bericht  || data.message || '';

  if (!naam || !email) {
    return res.status(400).json({ error: 'Naam en email zijn verplicht' });
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ error: 'Ongeldig email adres' });
  }

  const submission = { naam, email, bedrijf, telefoon, usecase, bericht };

  // Send notification + confirmation + backup in parallel
  const results = await Promise.allSettled([
    sendNotification(submission),
    sendConfirmation(submission),
    backupToSupabase(submission),
  ]);

  // Log results
  results.forEach((r, i) => {
    const label = ['notify', 'confirm', 'supabase'][i];
    if (r.status === 'rejected') console.error(`[contact] ${label} failed:`, r.reason);
  });

  const notifyOk = results[0].status === 'fulfilled' && !results[0].value?.skipped;

  if (!notifyOk && !RESEND_API_KEY) {
    // Resend not configured yet — fail soft, log the submission so it's not lost
    console.log('[contact] SUBMISSION (Resend not configured):', JSON.stringify(submission));
    return res.status(200).json({
      success: true,
      message: 'Bedankt! We nemen binnen 4 werkuren contact op.',
      _note: 'Resend not configured — check Vercel logs',
    });
  }

  return res.status(200).json({
    success: true,
    message: `Bedankt ${naam}! We nemen binnen 4 werkuren contact op via ${email}.`,
  });
}
