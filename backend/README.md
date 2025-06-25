# BotLease Chatbot Backend

Flask-based chatbot backend powered by Google's Gemini AI model.

## Setup

### 1. Install Dependencies
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the backend directory:
```
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash-exp
PORT=5001
```

### 3. Run Locally
```bash
python app.py
```

The backend will be available at `http://localhost:5001`

## API Endpoints

### Health Check
```
GET /health
```

### Start Conversation
```
POST /api/start-conversation
Content-Type: application/json

Response:
{
  "session_id": "uuid-string",
  "message": "Conversation started"
}
```

### Send Message
```
POST /api/send-message
Content-Type: application/json

{
  "session_id": "uuid-string",
  "message": "User message"
}

Response:
{
  "response": "AI response",
  "session_id": "uuid-string"
}
```

## Deployment Options

### Azure App Service
1. Create an Azure App Service (Python 3.11)
2. Set environment variables in Azure portal
3. Deploy using GitHub Actions or Azure CLI

### Railway
1. Connect GitHub repo
2. Add environment variables
3. Deploy automatically

### Local Docker
```bash
docker build -t botlease-backend .
docker run -p 5001:5001 --env-file .env botlease-backend
```

## Architecture

- **app.py**: Main Flask application
- **llm_providers.py**: LLM integration (Gemini)
- **conversation_storage.py**: In-memory session management

## Frontend Integration

Update the frontend API URL in `index.html`:
```javascript
this.apiUrl = 'https://your-backend-url.com/api';
```