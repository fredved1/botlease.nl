# BotLease - AI-automatisering zonder risico

Full-stack applicatie voor BotLease, een AI-automatiseringsbedrijf opgericht door Thomas Vedder.

## 🚀 Project Structuur

```
botlease/
├── index.html          # Frontend website
├── api/               # Vercel API routes
│   └── contact.js     # Contact form handler
├── backend/           # Flask chatbot backend
│   ├── app.py         # Main Flask app
│   ├── requirements.txt
│   └── README.md
└── package.json       # Frontend dependencies
```

## 🛠️ Tech Stack

### Frontend
- Pure HTML/CSS/JavaScript
- Vercel hosting
- Vercel Postgres voor contact forms

### Backend
- Flask + Python
- Google Gemini AI
- Azure/Railway hosting

## 📦 Installatie

### Frontend
```bash
# Install dependencies
npm install

# Run locally
vercel dev

# Deploy to Vercel
vercel --prod
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file (see backend/.env.example)
python app.py
```

## 🔧 Environment Variables

### Frontend (Vercel)
- Automatisch geconfigureerd voor Vercel Postgres

### Backend
- `GEMINI_API_KEY`: Google AI API key
- `GEMINI_MODEL`: Model naam (default: gemini-2.0-flash-exp)

## 🚀 Deployment

### Frontend
1. Push naar GitHub
2. Verbind met Vercel
3. Automatische deployments bij elke push

### Backend opties
1. **Azure App Service** (aanrader voor enterprise)
2. **Railway** (makkelijk en snel)
3. **Docker** (voor custom hosting)

## 📝 Features

- ✅ Moderne, professionele website
- ✅ Geïntegreerde AI chatbot
- ✅ Contact formulier met database opslag
- ✅ Responsive design
- ✅ No cure, no pay messaging
- ✅ Thomas Vedder's persoonlijke verhaal

## 👤 Contact

**Thomas Vedder**  
Founder BotLease  
AI-specialist met overheid ervaring

## 📄 License

© 2024 BotLease. All rights reserved.