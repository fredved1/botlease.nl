// Vercel serverless function — handles contact form submissions
// Sends email to hallo@botlease.nl via Resend (resend.com) + logt elke aanvraag in het CRM (VPS)
//
// REQUIRED ENV VARS (set in Vercel project settings):
//   RESEND_API_KEY      → API key from resend.com (free 3000/mo)
//   RESEND_FROM         → optional, default "BotLease <onboarding@resend.dev>"
//                         set to "BotLease <noreply@botlease.nl>" na domain verification
//
// OPTIONAL (Supabase backup, oude config):
//   CRM_WEBHOOK_URL / CRM_WEBHOOK_SECRET   → CRM op de VPS (zie scripts/crm_server.py)

const RESEND_API_KEY = process.env.RESEND_API_KEY || '';
const RESEND_FROM    = process.env.RESEND_FROM    || 'BotLease <onboarding@resend.dev>';
const NOTIFY_TO      = 'hallo@botlease.nl';

// CRM op de VPS — elke aanvraag wordt daar gelogd (vervangt de dode Supabase-backup)
const CRM_URL    = process.env.CRM_WEBHOOK_URL    || 'https://crm.botlease.nl/api/lead';
const CRM_SECRET = process.env.CRM_WEBHOOK_SECRET || '';

// Sourcing info per robot — INTERNAL ONLY, alleen in admin email zichtbaar.
// Bij een bestelling weet jij meteen bij welke leverancier je het kunt ordenen.
const SOURCE_BY_SLUG = {
  // EU-gebouwd — direct contact met fabrikant
  'neura-4ne1-mini':   'NEURA Robotics direct · info@neura-robotics.com · Metzingen (DE) · 6-10 wk',
  'neura-4ne1-gen3':   'NEURA Robotics direct · info@neura-robotics.com · Metzingen (DE) · via Bosch supply · 8-12 wk',
  'pal-kangaroo':      'PAL Robotics · business@pal-robotics.com · Barcelona (ES) · 8-12 wk',
  'pal-tiago-pro':     'PAL Robotics · business@pal-robotics.com · Barcelona (ES) · 6-10 wk',
  'pollen-reachy-2':   'Pollen Robotics (Hugging Face) · sales@pollen-robotics.com · Bordeaux (FR) · 4-8 wk',
  // Aziatisch — via EU distributeurs of direct
  'unitree-r1':        'PRIMAIR: RobotShop EU (eu.robotshop.com) · BACK-UP: Unitree direct (shop.unitree.com) · 6-8 wk',
  'unitree-g1':        'PRIMAIR: RobotShop EU (eu.robotshop.com) · BACK-UP: Unitree direct (shop.unitree.com) · 6-8 wk',
  'unitree-h1-2':      'PRIMAIR: RobotShop EU (eu.robotshop.com) · BACK-UP: Unitree direct · 8-10 wk',
  'unitree-h2':        'Unitree direct (shop.unitree.com) · 8-10 wk · let op: AI-Act assessment vereist',
  'engineai-se01':     'EngineAI direct · sales@engineai.com.cn · Shenzhen (CN) · 10-14 wk',
  'ubtech-walker-s2':  'UBTECH direct · sales@ubtrobot.com · EU-distributeur: OrcaRobot Nijmegen (richard@orcarobot.com) · Terra Robotics DACH (mail@terra-robotics.de) · 12-16 wk',
  // Wachtlijst — niet leverbaar nu
  'apptronik-apollo':  'WACHTLIJST 2026/2027 · Apptronik (apptronik.com/contact-us) · pre-order via BotLease',
  'figure-02':         'WACHTLIJST 2027 · Figure (figure.ai) · enterprise pilot only',
  'agility-digit':     'WACHTLIJST · Agility Robotics direct (RaaS only) · pre-order via BotLease',
  '1x-neo':            'WACHTLIJST Q1 2027 · 1X Technologies (1x.tech/order) · EU shipping Q1 2027',
};

function escapeHtml(s) {
  return String(s || '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#039;');
}

// Wrap email body in a proper HTML document with a UTF-8 charset declaration.
// Without this, Outlook/Hotmail can mis-decode the multibyte chars (emoji, ·, —,
// ï) and truncate the message ("wordt niet volledig weergegeven").
function wrapEmail(inner, bg) {
  return `<!DOCTYPE html>
<html lang="nl"><head><meta charset="utf-8">` +
    `<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">` +
    `<meta name="viewport" content="width=device-width,initial-scale=1"></head>` +
    `<body style="margin:0;padding:0;background:${bg || '#ffffff'};-webkit-text-size-adjust:100%">${inner}</body></html>`;
}

async function sendNotification(data) {
  if (!RESEND_API_KEY) {
    console.warn('[contact] RESEND_API_KEY ontbreekt — email niet verstuurd. Submission:', data);
    return { skipped: true };
  }
  const isOrder    = data.type === 'order';
  const isWaitlist = data.type === 'waitlist';

  const heading = isOrder
    ? `🛒 NIEUWE BESTELLING — ${data.robot_name || data.robot_slug || 'onbekend'} × ${data.aantal || 1}`
    : isWaitlist
      ? `Nieuwe wachtlijst-aanmelding — ${data.robot_name || data.robot_slug || 'onbekend'}`
      : 'Nieuwe lease-aanvraag — BotLease';

  const subjectPrefix = isOrder
    ? `[BESTELLING] ${data.robot_name || data.robot_slug || 'algemeen'} × ${data.aantal || 1}`
    : isWaitlist
      ? `[WACHTLIJST] ${data.robot_name || data.robot_slug || 'algemeen'}`
      : `[BotLease] Lease-aanvraag`;

  const subject = `${subjectPrefix} — ${data.bedrijf || data.naam}`;

  // Source info — alleen voor admin (deze email naar hallo@botlease.nl)
  const source = isOrder ? SOURCE_BY_SLUG[data.robot_slug] || 'Onbekende bron — handmatig zoeken' : '';

  const orderBlock = isOrder ? `
      <div style="background:#fff;border:2px solid #16a34a;border-radius:10px;padding:24px;margin-bottom:14px">
        <p style="margin:0 0 14px;font-size:13px;color:#16a34a;text-transform:uppercase;letter-spacing:0.08em;font-weight:600">📦 Bestelling</p>
        <p style="margin:4px 0;font-size:16px"><b>Robot:</b> ${escapeHtml(data.robot_name || data.robot_slug)}</p>
        <p style="margin:4px 0;font-size:16px"><b>Aantal:</b> ${escapeHtml(String(data.aantal || 1))} unit(s)</p>
        ${data.contract_months ? `<p style="margin:4px 0"><b>Contractduur:</b> ${escapeHtml(data.contract_months)} maanden</p>` : ''}
        ${data.adres ? `<p style="margin:8px 0 4px"><b>Leveringsadres:</b></p><p style="margin:0;white-space:pre-wrap;color:#44403c">${escapeHtml(data.adres)}</p>` : ''}
      </div>
      <div style="background:#fef9c3;border:2px solid #ca8a04;border-radius:10px;padding:18px 24px;margin-bottom:14px">
        <p style="margin:0 0 8px;font-size:13px;color:#a16207;text-transform:uppercase;letter-spacing:0.08em;font-weight:600">🔧 INTERN: bron / leverancier</p>
        <p style="margin:0;font-size:14px;color:#713f12;line-height:1.5"><b>${escapeHtml(source)}</b></p>
        <p style="margin:8px 0 0;font-size:12px;color:#a16207">// Hier kun je deze robot bestellen voor de klant.</p>
      </div>
  ` : '';

  const waitlistBlock = isWaitlist ? `<div style="background:#fff7ed;border:1px solid #fed7aa;border-radius:10px;padding:14px 18px;margin-bottom:14px"><p style="margin:0;font-size:14px;color:#c2410c"><b>Type:</b> Wachtlijst-aanmelding voor ${escapeHtml(data.robot_name || data.robot_slug)}</p></div>` : '';

  const html = wrapEmail(`
    <div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;max-width:640px;margin:0 auto;padding:24px;background:#faf9f6;color:#1c1917">
      <h2 style="font-family:Arial,Helvetica,sans-serif;font-weight:700;color:#1c1917;margin:0 0 18px;font-size:22px">${escapeHtml(heading)}</h2>
      ${orderBlock}
      ${waitlistBlock}
      <div style="background:white;border:1px solid #e7e5e0;border-radius:10px;padding:24px;margin-bottom:14px">
        <p style="margin:0 0 14px;font-size:13px;color:#78716c;text-transform:uppercase;letter-spacing:0.08em">Contactgegevens</p>
        <p style="margin:4px 0"><b>Naam:</b> ${escapeHtml(data.naam)}</p>
        <p style="margin:4px 0"><b>Bedrijf:</b> ${escapeHtml(data.bedrijf)}</p>
        <p style="margin:4px 0"><b>Email:</b> <a href="mailto:${escapeHtml(data.email)}" style="color:#c2410c">${escapeHtml(data.email)}</a></p>
        ${data.telefoon ? `<p style="margin:4px 0"><b>Telefoon:</b> ${escapeHtml(data.telefoon)}</p>` : ''}
      </div>
      ${!isOrder ? `<div style="background:white;border:1px solid #e7e5e0;border-radius:10px;padding:24px;margin-bottom:14px">
        <p style="margin:0 0 14px;font-size:13px;color:#78716c;text-transform:uppercase;letter-spacing:0.08em">${isWaitlist ? 'Wachtlijst-detail' : 'Use-case'}</p>
        ${isWaitlist && data.robot_name ? `<p style="margin:4px 0"><b>Robot:</b> ${escapeHtml(data.robot_name)}</p>` : ''}
        ${data.usecase ? `<p style="margin:4px 0"><b>Sector:</b> ${escapeHtml(data.usecase)}</p>` : ''}
        ${data.bericht ? `<p style="margin:14px 0 4px"><b>Bericht:</b></p><p style="margin:0;white-space:pre-wrap;color:#44403c">${escapeHtml(data.bericht)}</p>` : ''}
      </div>` : (data.bericht ? `<div style="background:white;border:1px solid #e7e5e0;border-radius:10px;padding:24px;margin-bottom:14px"><p style="margin:0 0 8px;font-size:13px;color:#78716c;text-transform:uppercase;letter-spacing:0.08em">Bericht klant</p><p style="margin:0;white-space:pre-wrap;color:#44403c">${escapeHtml(data.bericht)}</p></div>` : '')}
      <p style="font-size:12px;color:#78716c;margin:18px 0 0">
        Ingestuurd via botlease.nl op ${new Date().toLocaleString('nl-NL', { timeZone: 'Europe/Amsterdam' })}.
        Reageer op deze email om direct te antwoorden.
      </p>
    </div>
  `, '#faf9f6');

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
      subject,
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
  const html = wrapEmail(`
    <div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;max-width:600px;margin:0 auto;padding:24px;background:#f7f7f9;color:#08080a">
      <h2 style="font-family:Arial,Helvetica,sans-serif;font-weight:700;color:#08080a;margin:0 0 18px;font-size:22px">Bedankt voor je aanvraag - BotLease</h2>
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
      <p style="font-size:12px;color:#71717a">BotLease B.V. · Amsterdam · hallo@botlease.nl · botlease.nl</p>
    </div>
  `, '#f7f7f9');
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

async function backupToCRM(data) {
  if (!CRM_SECRET) return { skipped: true };
  try {
    let prefix;
    if (data.type === 'order') {
      prefix = `[BESTELLING: ${data.robot_name || data.robot_slug} × ${data.aantal || 1}${data.contract_months ? ' · ' + data.contract_months + 'mnd' : ''}]`;
    } else if (data.type === 'waitlist') {
      prefix = `[WACHTLIJST: ${data.robot_name || data.robot_slug || 'algemeen'}]`;
    } else {
      prefix = `[${data.usecase || 'algemeen'}]`;
    }
    const msgBody = data.type === 'order'
      ? [data.adres ? `Leveringsadres: ${data.adres}` : '', data.bericht || ''].filter(Boolean).join('\n\n')
      : (data.bericht || '');
    const resp = await fetch(CRM_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CRM-Secret': CRM_SECRET,
      },
      body: JSON.stringify({
        name:    data.naam,
        email:   data.email,
        phone:   data.telefoon || '',
        company: data.bedrijf  || '',
        subject: prefix,
        message: msgBody,
        source:  'formulier',
        robot:   data.robot_name || data.robot_slug || '',
        sourcing: data.type === 'order' ? (SOURCE_BY_SLUG[data.robot_slug] || '') : '',
      }),
    });
    if (!resp.ok) {
      console.warn('[contact] CRM backup failed:', await resp.text());
    }
  } catch (e) {
    console.warn('[contact] CRM exception:', e.message);
  }
}

export default async function handler(req, res) {
  const _src = req.headers.origin || req.headers.referer || '';
  const _ok = /^https?:\/\/(www\.)?botlease\.nl/.test(_src) || /^https:\/\/[a-z0-9-]+\.vercel\.app/.test(_src) || /^http:\/\/localhost(:\d+)?/.test(_src);
  if (req.headers.origin && _ok) res.setHeader('Access-Control-Allow-Origin', req.headers.origin);
  res.setHeader('Vary', 'Origin');
  res.setHeader('Access-Control-Allow-Methods', 'POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  if (!_ok) return res.status(403).json({ error: 'Verboden' });

  const data = req.body || {};
  // Honeypot: bots vullen het verborgen veld, mensen niet → stille success
  if (data.website || data._gotcha) {
    return res.status(200).json({ success: true, message: 'Bedankt! We nemen binnen 4 werkuren contact op.' });
  }
  const naam       = data.naam     || data.name    || '';
  const email      = data.email    || '';
  const bedrijf    = data.bedrijf  || data.company || '';
  const telefoon   = data.telefoon || data.phone   || '';
  const usecase    = data.usecase  || '';
  const bericht    = data.bericht  || data.message || '';
  const validTypes = ['waitlist', 'order'];
  const type       = validTypes.includes(data.type) ? data.type : 'contact';
  const robot_slug = data.robot_slug || '';
  const robot_name = data.robot_name || '';
  const aantal     = data.aantal || 1;
  const contract_months = data.contract_months || '';
  const adres      = data.adres || '';

  if (!naam || !email) {
    return res.status(400).json({ error: 'Naam en email zijn verplicht' });
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ error: 'Ongeldig email adres' });
  }

  const submission = { naam, email, bedrijf, telefoon, usecase, bericht, type, robot_slug, robot_name, aantal, contract_months, adres };

  // Send notification + confirmation + backup in parallel
  const results = await Promise.allSettled([
    sendNotification(submission),
    sendConfirmation(submission),
    backupToCRM(submission),
  ]);

  // Log results
  results.forEach((r, i) => {
    const label = ['notify', 'confirm', 'crm'][i];
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
