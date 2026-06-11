# Azure Deployment Guide voor BotLease Backend

## Stap 1: Azure CLI Installeren (als je die nog niet hebt)
```bash
# macOS
brew update && brew install azure-cli

# Of download van: https://aka.ms/installazureclimacos
```

## Stap 2: Login bij Azure
```bash
az login
```

## Stap 3: Resource Group maken
```bash
# Maak een resource group in West Europe
az group create --name botlease-rg --location westeurope
```

## Stap 4: App Service Plan maken
```bash
# B1 = Basic tier, geschikt voor productie
az appservice plan create \
  --name botlease-plan \
  --resource-group botlease-rg \
  --sku B1 \
  --is-linux
```

## Stap 5: Web App maken
```bash
az webapp create \
  --resource-group botlease-rg \
  --plan botlease-plan \
  --name botlease-backend \
  --runtime "PYTHON:3.11" \
  --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"
```

## Stap 6: Environment Variables instellen
```bash
# Google API Key
az webapp config appsettings set \
  --resource-group botlease-rg \
  --name botlease-backend \
  --settings GOOGLE_API_KEY="AIzaSyAJ_m4yVVNKDai_lyVnUMEvezVPi2KsaN4"

# Flask environment
az webapp config appsettings set \
  --resource-group botlease-rg \
  --name botlease-backend \
  --settings FLASK_ENV="production"

# Allowed origins
az webapp config appsettings set \
  --resource-group botlease-rg \
  --name botlease-backend \
  --settings ALLOWED_ORIGINS="https://www.botlease.nl,https://botlease.nl"
```

## Stap 7: Deploy vanaf GitHub
```bash
# Configure deployment from GitHub
az webapp deployment source config \
  --name botlease-backend \
  --resource-group botlease-rg \
  --repo-url https://github.com/fredved1/botlease.nl \
  --branch master \
  --manual-integration
```

## Stap 8: Deploy de code
```bash
# Navigate to backend folder
cd backend

# Deploy using zip
az webapp deployment source config-zip \
  --resource-group botlease-rg \
  --name botlease-backend \
  --src <(zip -r - . -x "*.pyc" -x "__pycache__/*" -x ".env" -x "venv/*")
```

## Stap 9: Test de deployment
```bash
# Get the URL
echo "https://botlease-backend.azurewebsites.net/health"

# Test health endpoint
curl https://botlease-backend.azurewebsites.net/health
```

## Stap 10: Update Frontend
Update in `frontend/index.html`:
```javascript
this.apiUrl = 'https://botlease-backend.azurewebsites.net/api';
```

## Belangrijke URLs:
- Backend Health: https://botlease-backend.azurewebsites.net/health
- Azure Portal: https://portal.azure.com
- Logs bekijken: `az webapp log tail --name botlease-backend --resource-group botlease-rg`

## Troubleshooting:
- Check logs: `az webapp log show --name botlease-backend --resource-group botlease-rg`
- Restart app: `az webapp restart --name botlease-backend --resource-group botlease-rg`
- SSH into container: `az webapp ssh --name botlease-backend --resource-group botlease-rg`