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

    // Supabase integratie
    try {
      const { createClient } = await import('@supabase/supabase-js');
      
      const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://ysrxerfgnwnnzmmwppzd.supabase.co';
      const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlzcnhlcmZnbndubnptbXdwcHpkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA4MzI4MDksImV4cCI6MjA2NjQwODgwOX0.5uNOe_ldZjkpyBAbko_CLdrxpLwebDwHCw05XkREg5g';
      
      const supabase = createClient(supabaseUrl, supabaseKey);
      
      const { data, error } = await supabase
        .from('contacts')
        .insert([{
          name,
          email,
          phone: phone || '',
          company: company || '',
          message
        }])
        .select();
        
      if (error) {
        console.error('Supabase error:', error);
      } else {
        console.log('Contact saved to Supabase:', data);
      }
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