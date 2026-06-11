# Azure Environment Variables voor BotLease Backend

## In Azure Portal → Configuration → Application Settings

Voeg deze **Application Settings** toe:

| Name | Value | Beschrijving |
|------|-------|--------------|
| **GOOGLE_API_KEY** | `AIzaSyAJ_m4yVVNKDai_lyVnUMEvezVPi2KsaN4` | Gemini API key |
| **FLASK_ENV** | `production` | Flask environment |
| **ALLOWED_ORIGINS** | `https://www.botlease.nl,https://botlease.nl,http://localhost:3000` | CORS origins |
| **PORT** | `8000` | Port voor de app |
| **SCM_DO_BUILD_DURING_DEPLOYMENT** | `true` | Build tijdens deployment |
| **PROJECT** | `backend` | Subfolder voor backend code |
| **PYTHON_ENABLE_GUNICORN_MULTIWORKERS** | `true` | Enable multi-workers |
| **WEBSITES_PORT** | `8000` | Azure websites port |

## In General Settings tab:

**Startup Command**:
```
gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app
```

## Optioneel (voor debugging):

| Name | Value |
|------|-------|
| **FLASK_DEBUG** | `0` |
| **LOG_LEVEL** | `INFO` |

## Na het toevoegen:
1. Klik **"Save"** bovenaan
2. Klik **"Continue"** bij restart warning
3. Wacht 1-2 minuten voor restart

## Test URL na deployment:
https://botlease-backend.azurewebsites.net/health