"""
Botlease AI Chatbot Backend - Sales Qualifier
OpenRouter backend voor BotLease automatisering
"""

import os
import logging
import uuid
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in environment variables")

OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'meta-llama/llama-3.3-70b-instruct:free')
OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions'

app = Flask(__name__)
CORS(app, origins=['*'], supports_credentials=True)

sessions = {}

SYSTEM_PROMPT = """Je bent een vriendelijke BotLease specialist die bedrijven helpt ontdekken welke processen geautomatiseerd kunnen worden.

JOUW STIJL:
✅ Vriendelijk en toegankelijk
✅ Enthousiast over automatisering
✅ Gericht op praktische oplossingen
✅ Kort en bondig (max 2 zinnen)

JOUW DOEL:
- Identificeren welke processen BotLease kan automatiseren
- Interesse wekken met concrete besparingen (€/tijd)
- Doorverwijzen naar het contactformulier voor maatwerk

ANTWOORD STRUCTUUR:
1. Bevestig het proces: "Facturatie automatiseren is een geweldige keuze!"
2. Vraag naar details: "Hoeveel facturen maken jullie per maand?"
3. Alleen bij genoeg info: bereken besparing (tijd × €25/uur)
4. Vervolgvraag: "Welke andere repetitieve taken kosten jullie tijd?"
5. Na 3+ berichten: Doorverwijzen naar contactformulier

KOSTENBEREKNING ALLEEN ALS:
- Je weet hoeveel tijd het proces nu kost (uren/week)
- Je weet frequentie (hoeveel keer per dag/week/maand)
- Bereken dan: huidige tijd × €25 per uur = maandelijkse besparing

ZONDER DETAILS:
- GEEN specifieke bedragen noemen
- Wel algemeen: "Dat kan flink wat tijd en geld besparen"

GEEN lange uitleg, GEEN technische details, GEEN gratis consulting! """


def call_openrouter(messages, max_tokens=200):
    """Call OpenRouter API with given messages"""
    response = requests.post(
        OPENROUTER_URL,
        headers={
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://botlease.nl',
            'X-Title': 'BotLease'
        },
        json={
            'model': OPENROUTER_MODEL,
            'messages': messages,
            'max_tokens': max_tokens
        },
        timeout=30
    )
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "model": OPENROUTER_MODEL,
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.json
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({"error": "Geen bericht ontvangen"}), 400

        messages = [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': user_message}
        ]

        bot_response = call_openrouter(messages)

        logger.info(f"Chat - User: {user_message[:50]}... | Bot: {bot_response[:50]}...")

        return jsonify({"response": bot_response})

    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({"error": "Er ging iets mis. Probeer het opnieuw."}), 500


@app.route('/api/start-conversation', methods=['POST'])
def start_conversation():
    try:
        data = request.json
        session_id = str(uuid.uuid4())

        sessions[session_id] = {
            "id": session_id,
            "company_name": data.get('company_name', 'Onbekend'),
            "industry": data.get('industry', 'Algemeen'),
            "messages": [{'role': 'system', 'content': SYSTEM_PROMPT}],
            "created_at": datetime.now().isoformat()
        }

        welcome_message = "Hoi! 👋 Ik ben de BotLease AI-assistent. Vertel me welke processen in jouw bedrijf veel tijd kosten, en ik laat zien hoeveel je kunt besparen met automatisering!"

        sessions[session_id]["messages"].append({
            "role": "assistant",
            "content": welcome_message
        })

        return jsonify({
            "session_id": session_id,
            "message": welcome_message
        })

    except Exception as e:
        logger.error(f"Error starting conversation: {str(e)}")
        return jsonify({"error": "Er ging iets mis bij het starten van de conversatie"}), 500


@app.route('/api/send-message', methods=['POST'])
def send_message():
    try:
        data = request.json
        session_id = data.get('session_id')
        user_message = data.get('message')

        if not session_id or not user_message:
            return jsonify({"error": "Session ID en bericht zijn verplicht"}), 400

        if session_id not in sessions:
            return jsonify({"error": "Ongeldige sessie"}), 404

        session = sessions[session_id]
        session["messages"].append({"role": "user", "content": user_message})

        ai_response = call_openrouter(session["messages"][-10:])  # laatste 10 berichten

        session["messages"].append({"role": "assistant", "content": ai_response})

        logger.info(f"Processed message for session: {session_id}")

        return jsonify({
            "response": ai_response,
            "session_id": session_id,
            "message_count": len(session["messages"])
        })

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return jsonify({"error": "Er ging iets mis bij het verwerken van uw bericht"}), 500


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
    app.run(host='0.0.0.0', port=port, debug=debug)
