#!/bin/bash
# Deploy script voor Azure

echo "🚀 Starting Azure deployment..."

# Get the publish profile first
echo "📋 Please go to Azure Portal > Your Web App > Overview"
echo "Click 'Get publish profile' and save the file"
echo "What's the exact name of your web app? (e.g., botlease-backend)"
read -p "Web app name: " WEBAPP_NAME

# Create deployment package
echo "📦 Creating deployment package..."
cd /Users/fredved/Documents/Python\ projecten/botlease_clone/botlease-final/backend
zip -r deploy.zip . -x "*.pyc" -x "__pycache__/*" -x ".env" -x "venv/*" -x "*.log" -x ".DS_Store" -x "app_old.py" -x "*.sh" -x "*.md"

# Deploy using Azure CLI
echo "🔧 Deploying to Azure..."
az webapp deployment source config-zip \
  --resource-group botlease-rg \
  --name $WEBAPP_NAME \
  --src deploy.zip

echo "✅ Deployment complete!"
echo "🧪 Testing health endpoint..."
sleep 30
curl https://$WEBAPP_NAME.azurewebsites.net/health

# Cleanup
rm deploy.zip