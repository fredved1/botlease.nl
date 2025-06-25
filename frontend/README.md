# BotLease Frontend

Modern, responsive website voor BotLease met geïntegreerde AI chatbot.

## Features

- 🎨 Modern design gebaseerd op v0.dev aesthetics
- 💬 Geïntegreerde AI chatbot (geen modal)
- 📝 Contact formulier met database opslag
- 📱 Volledig responsive
- ⚡ Snelle laadtijden
- 🔒 GDPR compliant

## Local Development

```bash
# Install dependencies
npm install

# Run development server
vercel dev

# Open http://localhost:3000
```

## Deployment

### Automatic (recommended)
1. Push to GitHub
2. Import in Vercel dashboard
3. Auto-deploy on every push

### Manual
```bash
vercel --prod
```

## Configuration

### Backend URL
Update in `index.html`:
```javascript
this.apiUrl = 'https://your-backend-url.com/api';
```

### Database Setup
See `VERCEL_DATABASE_SETUP.md` for Postgres configuration.

## Structure

```
frontend/
├── index.html         # Main website
├── api/              # Serverless functions
│   └── contact.js    # Contact form handler
├── package.json      # Dependencies
└── vercel.json       # Vercel configuration
```

## Environment Variables

Set in Vercel dashboard:
- Database connection (auto-configured)
- Any additional API keys

## Contact Form Data

Submissions are stored in Vercel Postgres and viewable in:
- Vercel Dashboard → Storage → Data
- Or query directly with SQL