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
CORS(app, origins=['*'], supports_credentials=True)

# In-memory session storage (for development - gebruik Redis voor productie)
sessions = {}

# System prompt voor Botlease AI Assistant
SYSTEM_PROMPT = """Je bent de Botlease Sales Qualifier. Jouw ENIGE doel: kwalificeren of iemand een potentiële klant is.

JE BENT GEEN:
❌ Universele AI assistent
❌ Technische consultant 
❌ Gratis adviesgever
❌ Procesbouwer

JE BENT WEL:
✅ BotLease verkoop kwalificeerder
✅ Usecase identifier voor BotLease diensten
✅ Lead generator naar het contactformulier

STRIKTE REGELS:
- GEEN uitgebreide analyses of adviezen geven
- GEEN technische implementatie details
- GEEN gratis consulting
- MAX 2 zinnen per antwoord
- ALTIJD doorverwijzen naar contact na 2-3 berichten

ANTWOORD FORMAAT:
1. "BotLease kan [proces] automatiseren en €X per maand besparen"
2. "Welk proces kost jullie nu de meeste tijd?"
3. Na 2 berichten: "Voor maatwerk advies: [contactformulier](https://www.botlease.nl/#contact)"

WEIGER ALLES BEHALVE:
- Vragen over wat BotLease kan
- Processen die geautomatiseerd kunnen worden
- Kosten/tijdbesparing van automatisering

Bij off-topic: "Ik help alleen met BotLease automatisering. Welk bedrijfsproces wil je automatiseren?"


def is_botlease_related(message):
    """Check if message is specifically about BotLease services or business process automation"""
    
    # Allowed BotLease topics
    botlease_keywords = [
        'botlease', 'automatisering', 'proces', 'bedrijf', 'efficiency', 'kosten', 'besparen',
        'workflow', 'tijdsbesparing', 'facturatie', 'klanten', 'voorraad', 'planning',
        'administratie', 'email', 'rapportage', 'data', 'integratie'
    ]
    
    # Block everything else including generic requests
    blocked_patterns = [
        'schrijf', 'maak', 'help me met', 'leg uit', 'vertel over', 'wat is',
        'hoe werkt', 'recept', 'sport', 'weer', 'nieuws', 'code', 'programmeer',
        'vertaal', 'samenvatting', 'homework', 'essay', 'brief', 'email schrijven',
        'plan maken', 'strategie', 'advies geven', 'oplossing bedenken'
    ]
    
    message_lower = message.lower()
    
    # Block obvious non-BotLease requests
    if any(pattern in message_lower for pattern in blocked_patterns):
        return False
    
    # Allow if it contains BotLease-specific keywords
    if any(keyword in message_lower for keyword in botlease_keywords):
        return True
    
    # Block questions that are clearly requests for work/advice
    work_indicators = ['hoe', 'wat', 'waarom', 'wanneer', 'waar', 'welke']
    if any(indicator in message_lower for indicator in work_indicators) and len(message) > 50:
        return False  # Long questions are usually requests for detailed advice
    
    # Default to strict blocking - only allow very specific BotLease queries
    return False


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
        
        # Check if message is BotLease-related
        if not is_botlease_related(user_message):
            off_topic_response = "Ik help alleen met BotLease automatisering. Welk bedrijfsproces wil je automatiseren? Bijvoorbeeld: facturatie, planning, administratie?"
            
            session["messages"].append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            })
            
            session["messages"].append({
                "role": "assistant", 
                "content": off_topic_response,
                "timestamp": datetime.now().isoformat()
            })
            
            return jsonify({
                "response": off_topic_response,
                "session_id": session_id,
                "message_count": len(session["messages"])
            })
        
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
        
        # Analyseer conversatie context voor lead kwalificatie
        user_messages = [msg for msg in session["messages"] if msg["role"] == "user"]
        context_summary = ""
        
        if len(user_messages) > 1:
            # Extraheer belangrijke context uit vorige berichten
            mentioned_processes = []
            mentioned_pain_points = []
            
            all_user_text = " ".join([msg["content"].lower() for msg in user_messages])
            
            # Identificeer genoemde processen
            process_keywords = {
                'facturatie': ['factuur', 'facturatie', 'rekening'],
                'planning': ['planning', 'roosters', 'agenda'],
                'administratie': ['admin', 'administratie', 'papierwerk'],
                'klanten': ['klant', 'customer', 'service'],
                'voorraad': ['voorraad', 'stock', 'inventaris'],
                'email': ['email', 'mail', 'communicatie'],
                'rapportage': ['rapport', 'rapportage', 'dashboard']
            }
            
            for process, keywords in process_keywords.items():
                if any(keyword in all_user_text for keyword in keywords):
                    mentioned_processes.append(process)
            
            if mentioned_processes:
                context_summary += f"Eerder genoemde processen: {', '.join(mentioned_processes)}. "
            
            # Check voor interesse signalen
            interest_signals = ['kosten', 'prijs', 'tijd', 'besparing', 'efficiency', 'automatiseer']
            if any(signal in all_user_text for signal in interest_signals):
                context_summary += "Toont interesse in kosten/tijdsbesparing. "

        # Genereer prompt met verbeterde context
        prompt = f"""{SYSTEM_PROMPT}

CONTEXT VAN DIT GESPREK:
- Bedrijf: {session['company_name']} ({session['industry']})
- Bericht nummer: {len(user_messages)}
- {context_summary}

INSTRUCTIES OP BASIS VAN CONTEXT:
- Als dit bericht 1-2 is: Focus op proces identificatie
- Als dit bericht 3+: VERPLICHT doorverwijzen naar contactformulier
- Verwijs altijd terug naar eerder genoemde processen waar relevant

Laatste berichten:
{chr(10).join(conversation_history[-4:])}  

Gebruiker: {user_message}
Assistant:"""
        
        # Genereer response
        response = model.generate_content(prompt)
        ai_response = response.text
        
        # Forceer contact doorverwijzing na 3+ berichten met context
        if len(user_messages) >= 3:
            contact_prompt = ""
            if mentioned_processes:
                contact_prompt = f"\n\nPerfect! Voor maatwerk automatisering van {', '.join(mentioned_processes)}: [contactformulier](https://www.botlease.nl/#contact)"
            else:
                contact_prompt = "\n\nVoor een persoonlijke procesanalyse: [contactformulier](https://www.botlease.nl/#contact)"
            
            ai_response += contact_prompt
        
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