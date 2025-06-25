# Fix Basic Authentication Issue

## Probleem: 
"Get publish profile" zegt dat Basic Auth disabled is, ondanks dat het op "On" staat.

## Oplossing 1: Force Enable via Azure CLI
```bash
az webapp auth update --name botlease --resource-group botlease-rg --enabled true
```

## Oplossing 2: Via Portal - Alternative Method
1. Ga naar **Deployment Center** in je Web App
2. Klik **"Disconnect"** als er een source connected is
3. Ga terug naar **Configuration** → **General settings**
4. Zet **SCM Basic Auth Publishing** op **"Off"**
5. **Save** en wacht 30 seconden
6. Zet het weer op **"On"**
7. **Save** opnieuw

## Oplossing 3: Alternative Deployment Method
Als Basic Auth niet werkt, gebruik Azure CLI direct:

```bash
# Via Azure CLI (als je ingelogd bent)
az webapp deployment source config-zip \
  --resource-group botlease-rg \
  --name botlease \
  --src /Users/fredved/Documents/Python\ projecten/botlease_clone/botlease-final/backend/backend.zip
```

## Oplossing 4: Check Resource Group
Controleer of de Resource Group naam klopt:
- Ga naar **Overview** → kijk bij **Resource group**
- Als het niet "botlease-rg" is, update de commands