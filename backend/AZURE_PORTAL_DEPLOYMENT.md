# Azure Portal Deployment Guide voor BotLease Backend

## Stap 1: Login bij Azure Portal
1. Ga naar https://portal.azure.com
2. Login met je Azure account

## Stap 2: Maak een Web App
1. Klik op **"Create a resource"** (+ icoon)
2. Zoek naar **"Web App"**
3. Klik **"Create"**

### Basics tab:
- **Subscription**: Kies je subscription
- **Resource Group**: Klik "Create new" → naam: `botlease-rg`
- **Name**: `botlease-backend` (dit wordt: botlease-backend.azurewebsites.net)
- **Publish**: Code
- **Runtime stack**: Python 3.11
- **Operating System**: Linux
- **Region**: West Europe
- **Pricing plan**: 
  - Klik "Create new"
  - Name: `botlease-plan`
  - Sku and size: Klik "Change size" → **B1** (Basic)

### Deployment tab:
- **Continuous deployment**: Disable (we doen het later)

### Networking tab:
- Laat alles default

### Monitoring tab:
- **Enable Application Insights**: No (voor nu)

### Review + create:
- Klik **"Review + create"**
- Klik **"Create"**

⏱️ Wacht 2-3 minuten tot deployment klaar is

## Stap 3: Configure Environment Variables
1. Ga naar je Web App (botlease-backend)
2. In het linker menu: **Configuration** → **Application settings**
3. Klik **"+ New application setting"** voor elk van deze:

| Name | Value |
|------|-------|
| GOOGLE_API_KEY | AIzaSyAJ_m4yVVNKDai_lyVnUMEvezVPi2KsaN4 |
| FLASK_ENV | production |
| ALLOWED_ORIGINS | https://www.botlease.nl,https://botlease.nl |
| PORT | 8000 |
| SCM_DO_BUILD_DURING_DEPLOYMENT | true |

4. Klik **"Save"** bovenaan
5. Klik **"Continue"** bij de restart warning

## Stap 4: Configure Startup Command
1. Nog in Configuration
2. Ga naar **"General settings"** tab
3. **Startup Command**: `gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app`
4. Klik **"Save"**

## Stap 5: Setup Deployment
1. In het linker menu: **Deployment Center**
2. **Source**: GitHub
3. Klik **"Authorize"** en geef toegang
4. **Organization**: fredved1
5. **Repository**: botlease.nl
6. **Branch**: master
7. **Build provider**: App Service build service
8. Klik **"Save"**

## Stap 6: Configure Build
1. In Deployment Center, klik op **"Disconnect"**
2. Nu handmatig deploy:
   - In linker menu: **Advanced Tools** → **Go**
   - Dit opent Kudu console
   - Ga naar **Debug console** → **Bash**
   
3. Run deze commands in Kudu:
```bash
cd /home/site/wwwroot
rm -rf *
git clone https://github.com/fredved1/botlease.nl.git .
cp -r backend/* .
pip install -r requirements.txt
```

## Stap 7: Deployment via ZIP (Alternatief - Makkelijker!)

1. Maak eerst een ZIP file:
```bash
cd /Users/fredved/Documents/Python projecten/botlease_clone/botlease-final/backend
zip -r backend.zip . -x "*.pyc" -x "__pycache__/*" -x ".env" -x "venv/*" -x "*.log"
```

2. In Azure Portal:
   - Ga naar je Web App
   - Linker menu: **Advanced Tools** → **Go**
   - In Kudu: **Tools** → **Zip Push Deploy**
   - Sleep je `backend.zip` naar het scherm

## Stap 8: Test de Deployment
1. Ga naar: https://botlease-backend.azurewebsites.net/health
2. Je zou moeten zien:
```json
{
  "status": "healthy",
  "model": "gemini-2.5-flash",
  "version": "1.0.0",
  "timestamp": "2025-..."
}
```

## Stap 9: Update Frontend
1. In `frontend/index.html`, zoek alle:
   ```javascript
   this.apiUrl = 'http://localhost:5001/api';
   ```
2. Vervang met:
   ```javascript
   this.apiUrl = 'https://botlease-backend.azurewebsites.net/api';
   ```
3. Commit en push naar GitHub

## Stap 10: Monitor & Logs
1. In Azure Portal → je Web App
2. **Log stream**: Live logs bekijken
3. **Diagnose and solve problems**: Voor troubleshooting

## Troubleshooting:
- **500 Error?** → Check Log Stream voor Python errors
- **Timeout?** → Startup command moet correct zijn
- **Module not found?** → Check of requirements.txt goed is
- **CORS issues?** → Check ALLOWED_ORIGINS setting

## Belangrijke URLs:
- Health check: https://botlease-backend.azurewebsites.net/health
- API Start conversation: https://botlease-backend.azurewebsites.net/api/start-conversation
- Kudu console: https://botlease-backend.scm.azurewebsites.net

## Kosten:
- B1 Basic: ~€50/maand
- Voor development: gebruik **F1 Free** tier (beperkt tot 60 min/dag)