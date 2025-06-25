"""
Botlease AI Chatbot Backend
Professionele chatbot API voor business automatisering
"""

import os
import logging
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize model
model = genai.GenerativeModel('gemini-2.5-flash')

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=os.getenv('ALLOWED_ORIGINS', '*').split(','))

# In-memory session storage (for development - gebruik Redis voor productie)
sessions = {}

# System prompt voor Botlease AI Assistant
SYSTEM_PROMPT = """Je bent de Botlease AI Assistant, een expert in business process automatisering voor het Nederlandse MKB.

Je belangrijkste taken zijn:
1. Bedrijfsprocessen analyseren en automatiseringsmogelijkheden identificeren
2. ROI en tijdsbesparing inschatten voor voorgestelde automatiseringen
3. Praktische implementatiestappen voorstellen
4. Vragen beantwoorden over AI en automatisering

Communiceer altijd:
- In het Nederlands
- Professioneel maar toegankelijk
- Met concrete voorbeelden en cijfers waar mogelijk
- Focus op praktische oplossingen

Bij het voorstellen van automatisering, overweeg altijd:
- Tijdsbesparing per week/maand
- Geschatte kosten vs baten
- Implementatie complexiteit (laag/medium/hoog)
- Quick wins vs lange termijn projecten"""


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model": "gemini-2.5-flash",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/start-conversation', methods=['POST'])
def start_conversation():
    """Start een nieuwe conversatie sessie"""
    try:
        data = request.json
        session_id = str(uuid.uuid4())
        
        # Initialiseer sessie
        sessions[session_id] = {
            "id": session_id,
            "company_name": data.get('company_name', 'Onbekend'),
            "industry": data.get('industry', 'Algemeen'),
            "messages": [],
            "created_at": datetime.now().isoformat(),
            "context": []
        }
        
        # Personaliseer welkomstbericht
        industry = data.get('industry', 'uw branche')
        welcome_message = f"""Hallo! Ik ben de Botlease AI Assistant. 

Ik help bedrijven in {industry} met het identificeren en implementeren van slimme automatiseringsoplossingen. 

Wat is momenteel uw grootste uitdaging of welk proces kost u de meeste tijd?"""
        
        # Sla welkomstbericht op
        sessions[session_id]["messages"].append({
            "role": "assistant",
            "content": welcome_message,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"Started new conversation: {session_id}")
        
        return jsonify({
            "session_id": session_id,
            "message": welcome_message,
            "company_name": data.get('company_name'),
            "industry": data.get('industry')
        })
        
    except Exception as e:
        logger.error(f"Error starting conversation: {str(e)}")
        return jsonify({"error": "Er ging iets mis bij het starten van de conversatie"}), 500


@app.route('/api/send-message', methods=['POST'])
def send_message():
    """Verstuur een bericht naar de AI"""
    try:
        data = request.json
        session_id = data.get('session_id')
        user_message = data.get('message')
        
        if not session_id or not user_message:
            return jsonify({"error": "Session ID en bericht zijn verplicht"}), 400
        
        # Check of sessie bestaat
        if session_id not in sessions:
            return jsonify({"error": "Ongeldige sessie"}), 404
        
        session = sessions[session_id]
        
        # Voeg gebruikersbericht toe aan geschiedenis
        session["messages"].append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Bouw conversatie context op
        conversation_history = []
        for msg in session["messages"][-10:]:  # Laatste 10 berichten voor context
            if msg["role"] == "user":
                conversation_history.append(f"Gebruiker: {msg['content']}")
            else:
                conversation_history.append(f"Assistant: {msg['content']}")
        
        # Genereer prompt met context
        prompt = f"""{SYSTEM_PROMPT}

Bedrijfsinformatie:
- Naam: {session['company_name']}
- Branche: {session['industry']}

Conversatie geschiedenis:
{chr(10).join(conversation_history)}

Gebruiker: {user_message}
Assistant:"""
        
        # Genereer response
        response = model.generate_content(prompt)
        ai_response = response.text
        
        # Sla AI response op
        session["messages"].append({
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"Processed message for session: {session_id}")
        
        return jsonify({
            "response": ai_response,
            "session_id": session_id,
            "message_count": len(session["messages"])
        })
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return jsonify({"error": "Er ging iets mis bij het verwerken van uw bericht"}), 500


@app.route('/api/get-conversation', methods=['GET'])
def get_conversation():
    """Haal conversatie geschiedenis op"""
    try:
        session_id = request.args.get('session_id')
        
        if not session_id:
            return jsonify({"error": "Session ID is verplicht"}), 400
        
        if session_id not in sessions:
            return jsonify({"error": "Ongeldige sessie"}), 404
        
        session = sessions[session_id]
        
        return jsonify({
            "session_id": session_id,
            "company_name": session["company_name"],
            "industry": session["industry"],
            "messages": session["messages"],
            "created_at": session["created_at"]
        })
        
    except Exception as e:
        logger.error(f"Error retrieving conversation: {str(e)}")
        return jsonify({"error": "Er ging iets mis bij het ophalen van de conversatie"}), 500


@app.route('/api/end-conversation', methods=['POST'])
def end_conversation():
    """Beëindig een conversatie sessie"""
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({"error": "Session ID is verplicht"}), 400
        
        if session_id in sessions:
            # Log conversation summary
            session = sessions[session_id]
            logger.info(f"Ending conversation {session_id} with {len(session['messages'])} messages")
            
            # Verwijder sessie
            del sessions[session_id]
            
            return jsonify({
                "message": "Conversatie beëindigd",
                "session_id": session_id
            })
        else:
            return jsonify({"error": "Sessie niet gevonden"}), 404
            
    except Exception as e:
        logger.error(f"Error ending conversation: {str(e)}")
        return jsonify({"error": "Er ging iets mis bij het beëindigen van de conversatie"}), 500


@app.route('/api/analyze-process', methods=['POST'])
def analyze_process():
    """Analyseer een specifiek bedrijfsproces voor automatisering"""
    try:
        data = request.json
        process_description = data.get('process')
        company_type = data.get('company_type', 'MKB')
        
        if not process_description:
            return jsonify({"error": "Procesbeschrijving is verplicht"}), 400
        
        # Specifieke prompt voor procesanalyse
        analysis_prompt = f"""Analyseer het volgende bedrijfsproces voor automatiseringsmogelijkheden:

Proces: {process_description}
Bedrijfstype: {company_type}

Geef een gestructureerde analyse met:
1. **Automatiseringsmogelijkheden**: Welke delen kunnen geautomatiseerd worden?
2. **Geschatte tijdsbesparing**: Hoeveel tijd kan er bespaard worden?
3. **Benodigde tools/technologie**: Welke tools zijn nodig?
4. **Implementatie complexiteit**: Laag/Medium/Hoog
5. **ROI inschatting**: Wanneer verdient de investering zich terug?
6. **Eerste stappen**: Concrete acties om te beginnen

Gebruik markdown formatting voor een duidelijke structuur."""
        
        # Genereer analyse
        response = model.generate_content(analysis_prompt)
        
        return jsonify({
            "analysis": response.text,
            "process": process_description,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error analyzing process: {str(e)}")
        return jsonify({"error": "Er ging iets mis bij de procesanalyse"}), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint niet gevonden"}), 404


@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {str(e)}")
    return jsonify({"error": "Interne server fout"}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    logger.info(f"Starting Botlease Chatbot Backend on port {port}")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )