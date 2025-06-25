// API route voor Vercel - /api/contact
// Deze file moet in de 'api' folder staan voor Vercel deployment

export default async function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  // Handle OPTIONS request
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Only allow POST
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { name, email, phone, company, message } = req.body;

    // Validate required fields
    if (!name || !email || !message) {
      return res.status(400).json({ 
        error: 'Naam, email en bericht zijn verplicht' 
      });
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return res.status(400).json({ 
        error: 'Ongeldig email adres' 
      });
    }

    // Create submission object
    const submission = {
      name,
      email,
      phone: phone || '',
      company: company || '',
      message,
      timestamp: new Date().toISOString(),
      source: 'website_contact_form'
    };

    // Vercel Postgres integratie
    try {
      const { sql } = await import('@vercel/postgres');
      
      const { rows } = await sql`
        INSERT INTO contacts (name, email, phone, company, message)
        VALUES (${name}, ${email}, ${phone}, ${company}, ${message})
        RETURNING id
      `;
      
      console.log('Contact saved to database with ID:', rows[0].id);
    } catch (dbError) {
      console.error('Database error:', dbError);
      // Continue anyway - don't fail the whole request
    }

    // Send success response
    return res.status(200).json({ 
      success: true,
      message: 'Bedankt voor uw aanvraag! We nemen binnen 24 uur contact met u op.'
    });

  } catch (error) {
    console.error('Contact form error:', error);
    return res.status(500).json({ 
      error: 'Er ging iets mis. Probeer het later opnieuw.' 
    });
  }
}