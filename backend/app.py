"""
Botlease AI Chatbot Backend - Sales Qualifier
Strikte lead generator voor BotLease automatisering
Deployment: 2025-07-05
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

# In-memory session storage
sessions = {}

# System prompt voor Botlease Sales Qualifier
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
- Focus op mogelijkheden, niet op fictieve cijfers

GEEN lange uitleg, GEEN technische details, GEEN gratis consulting! """


def is_botlease_related(message):
    """Check if message is about business processes that BotLease can automate"""
    
    # Core business processes that BotLease automates
    business_processes = [
        # Financial processes
        'factureren', 'factuur', 'facturatie', 'rekening', 'boekhouding', 'administratie',
        'inkoop', 'verkoop', 'betaling', 'debiteur', 'crediteur',
        
        # Customer processes  
        'klant', 'customer', 'service', 'support', 'helpdesk', 'ticket',
        'offerte', 'order', 'bestelling',
        
        # Planning & scheduling
        'planning', 'roosters', 'agenda', 'afspraak', 'vergadering',
        'resource', 'capaciteit',
        
        # Inventory & logistics
        'voorraad', 'stock', 'inventaris', 'magazijn', 'logistiek',
        'inkoop', 'levering', 'transport',
        
        # Communication
        'email', 'mail', 'communicatie', 'notificatie', 'melding',
        'bericht', 'contact',
        
        # Reporting & data
        'rapport', 'rapportage', 'dashboard', 'data', 'analyse',
        'kpi', 'metrics', 'cijfer',
        
        # HR processes
        'hr', 'personeel', 'medewerker', 'verlof', 'aanwezigheid',
        'declaratie', 'onkosten',
        
        # General business terms
        'proces', 'workflow', 'taak', 'handmatig', 'repetitief',
        'automatisering', 'efficiency', 'besparing', 'tijd', 'kosten'
    ]
    
    # BotLease company terms
    botlease_terms = [
        'botlease', 'bot lease', 'automatisering', 'ai', 'chatbot', 'robot'
    ]
    
    message_lower = message.lower()
    
    # Always allow BotLease company mentions
    if any(term in message_lower for term in botlease_terms):
        return True
    
    # Allow business process mentions
    if any(process in message_lower for process in business_processes):
        return True
    
    # Block obvious non-business requests
    blocked_patterns = [
        'recept', 'koken', 'sport', 'weer', 'nieuws', 'politiek',
        'medisch', 'gezondheid', 'school', 'huiswerk', 'vakantie',
        'vertaal', 'homework', 'essay', 'verhaal', 'gedicht'
    ]
    
    if any(pattern in message_lower for pattern in blocked_patterns):
        return False
    
    # Allow short business-related questions
    if len(message) <= 30:  # Short messages are usually process names
        return True
    
    # Block very long requests for detailed work
    if len(message) > 100:
        return False
    
    # Default allow for unclear cases (better to engage than block potential leads)
    return True


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model": "gemini-2.5-flash",
        "version": "1.0.1",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    """Simple chat endpoint for frontend compatibility"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"error": "Geen bericht ontvangen"}), 400
        
        # Check if message is BotLease related
        if not is_botlease_related(user_message):
            return jsonify({
                "response": "Ik help specifiek met BotLease AI-automatisering voor klantenservice. Heb je vragen over chatbots, procesautomatisering of wil je weten wat we voor jouw bedrijf kunnen betekenen?"
            })
        
        # Generate response using Gemini
        chat_session = model.start_chat(history=[])
        
        response = chat_session.send_message(f"{SYSTEM_PROMPT}\n\nGebruiker: {user_message}\n\nGeef een kort, direct antwoord (max 3 zinnen):")
        
        bot_response = response.text.strip()
        
        # Ensure response is concise
        sentences = bot_response.split('. ')
        if len(sentences) > 3:
            bot_response = '. '.join(sentences[:3]) + '.'
        
        logger.info(f"Chat - User: {user_message[:50]}... | Bot: {bot_response[:50]}...")
        
        return jsonify({
            "response": bot_response
        })
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({
            "error": "Er ging iets mis. Probeer het opnieuw."
        }), 500


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
        
        # Demo welkomstbericht
        welcome_message = "Hoi! 👋 Test hier hoe een AI chatbot voor jouw bedrijf zou werken!\n\n🔗 Geef me je website URL en ik gedraag me als JOUW chatbot\n📋 Stel vragen die jouw klanten zouden stellen\n⚡ Zie direct hoe AI automatisch klantenservice kan overnemen\n\nTyp bijvoorbeeld: www.jouwbedrijf.nl"
        
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
        
        # Check if message contains a website URL
        import re
        url_pattern = r'(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,})'
        url_match = re.search(url_pattern, user_message.lower())
        
        # Store website in session if detected
        if url_match:
            website = url_match.group(0).strip()
            # Clean up URL formatting
            if not website.startswith('http'):
                website = 'https://' + website
            if not website.startswith('https://www.') and not website.startswith('https://'):
                website = website.replace('https://', 'https://www.')
            
            session["demo_website"] = website
            session["demo_mode"] = True
            
            # Extract company info from URL
            domain_parts = website.replace('https://', '').replace('http://', '').replace('www.', '').split('.')
            company_name = domain_parts[0].capitalize()
            session["demo_company_name"] = company_name
            
            # Guess business type from domain name
            business_keywords = {
                'restaurant': ['restaurant', 'eetcafe', 'bistro', 'pizzeria', 'cafe', 'bar', 'eten', 'food'],
                'retail': ['shop', 'store', 'winkel', 'fashion', 'clothing', 'mode', 'boutique', 'outlet'],
                'legal': ['advocaat', 'juridisch', 'legal', 'notaris', 'recht', 'law', 'jurist'],
                'medical': ['tandarts', 'dokter', 'ziekenhuis', 'kliniek', 'medical', 'gezondheid', 'fysiotherapie', 'huisarts'],
                'automotive': ['garage', 'auto', 'car', 'motor', 'dealer', 'occasions', 'motors'],
                'beauty': ['kapper', 'salon', 'beauty', 'spa', 'wellness', 'nails', 'schoonheid'],
                'construction': ['bouw', 'construction', 'aanneming', 'installatie', 'schilder', 'elektrisch'],
                'consulting': ['advies', 'consulting', 'bureau', 'diensten', 'consultancy'],
                'technology': ['tech', 'software', 'digital', 'it', 'computer', 'webdesign', 'app'],
                'finance': ['financieel', 'finance', 'accounting', 'verzekering', 'bank', 'hypotheek'],
                'hotel': ['hotel', 'pension', 'bnb', 'logies', 'verblijf', 'accommodatie'],
                'education': ['school', 'training', 'cursus', 'les', 'onderwijs', 'academy'],
                'fitness': ['fitness', 'sport', 'gym', 'personal', 'yoga', 'pilates'],
                'real_estate': ['makelaar', 'vastgoed', 'wonen', 'huis', 'property', 'estate']
            }
            
            session["demo_business_type"] = "algemeen"  # default
            domain_lower = company_name.lower()
            for business_type, keywords in business_keywords.items():
                if any(keyword in domain_lower for keyword in keywords):
                    session["demo_business_type"] = business_type
                    break
        
        # Voeg gebruikersbericht toe aan geschiedenis
        session["messages"].append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Bouw conversatie context op
        conversation_history = []
        for msg in session["messages"][-6:]:  # Laatste 6 berichten voor context
            if msg["role"] == "user":
                conversation_history.append(f"Gebruiker: {msg['content']}")
            else:
                conversation_history.append(f"Assistant: {msg['content']}")
        
        # Analyseer conversatie context voor lead kwalificatie
        user_messages = [msg for msg in session["messages"] if msg["role"] == "user"]
        context_summary = ""
        mentioned_processes = []
        
        if len(user_messages) > 1:
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

        # Check if we're in demo mode
        if session.get("demo_mode") and session.get("demo_website"):
            website = session["demo_website"]
            company_name = session.get("demo_company_name", "dit bedrijf")
            business_type = session.get("demo_business_type", "algemeen")
            
            # Business-specific responses
            business_responses = {
                'restaurant': {
                    'welkom': f"Welkom bij {company_name}! Wilt u een tafel reserveren of heeft u vragen over onze menukaart?",
                    'openingstijden': "Wij zijn open di-zo van 17:00-22:00. Maandag zijn wij gesloten.",
                    'reservering': "Voor reserveringen kunt u bellen naar 010-1234567 of online reserveren via onze website.",
                    'menu': "Ons menu vindt u op de website. We serveren moderne Nederlandse keuken met seizoensproducten."
                },
                'retail': {
                    'welkom': f"Welkom bij {company_name}! Waarmee kan ik u vandaag helpen?",
                    'openingstijden': "Wij zijn open ma-za 9:00-18:00, zondag 12:00-17:00.",
                    'voorraad': "Voor actuele voorraad kunt u het beste even bellen of langskomen in de winkel.",
                    'retour': "Retourneren kan binnen 14 dagen met kassabon en in originele staat."
                },
                'medical': {
                    'welkom': f"Welkom bij {company_name}. Voor spoedgevallen belt u 112. Waarmee kan ik u helpen?",
                    'afspraak': "Voor afspraken kunt u bellen tijdens kantooruren of online inplannen via onze patiëntenportaal.",
                    'openingstijden': "Spreekuur: ma-vr 8:00-17:00. Voor spoedgevallen hebben we een avond- en weekenddienst.",
                    'contact': "Voor vragen over medicatie of resultaten kunt u contact opnemen met de assistente."
                },
                'legal': {
                    'welkom': f"Welkom bij {company_name}. Waarmee kunnen we u juridisch adviseren?",
                    'afspraak': "Voor een vrijblijvend intakegesprek kunt u contact opnemen via telefoon of email.",
                    'specialisaties': "Wij zijn gespecialiseerd in ondernemingsrecht, arbeidsrecht en contractrecht.",
                    'kosten': "Voor informatie over tarieven en no cure no pay arrangementen nemen we graag contact met u op."
                },
                'automotive': {
                    'welkom': f"Welkom bij {company_name}! Heeft u een vraag over onderhoud, reparatie of verkoop?",
                    'afspraak': "Voor onderhoud en reparaties kunt u online een afspraak inplannen of bellen naar de werkplaats.",
                    'openingstijden': "Showroom: ma-vr 9:00-18:00, za 9:00-17:00. Werkplaats: ma-vr 8:00-17:00.",
                    'garantie': "Op al onze reparaties geven wij standaard garantie volgens de geldende voorwaarden."
                },
                'hotel': {
                    'welkom': f"Welkom bij {company_name}! Wilt u een kamer reserveren of heeft u vragen over uw verblijf?",
                    'reservering': "Voor reserveringen kunt u online boeken of bellen naar 015-1234567.",
                    'openingstijden': "Receptie is 24/7 bereikbaar. Check-in vanaf 15:00, check-out tot 11:00.",
                    'faciliteiten': "We hebben gratis WiFi, ontbijtservice, parking en een fitnessruimte."
                },
                'education': {
                    'welkom': f"Welkom bij {company_name}! Heeft u vragen over onze cursussen of wilt u zich inschrijven?",
                    'inschrijving': "Voor inschrijvingen kunt u ons contactformulier invullen of bellen tijdens kantooruren.",
                    'openingstijden': "Lessen: ma-vr 9:00-21:00, za 9:00-17:00. Administratie: ma-vr 9:00-17:00.",
                    'cursussen': "Ons actuele cursusaanbod en roosters vindt u op onze website."
                },
                'fitness': {
                    'welkom': f"Welkom bij {company_name}! Wilt u informatie over lidmaatschap of onze groepslessen?",
                    'lidmaatschap': "Voor een proefles en informatie over lidmaatschappen kunt u langskomen of bellen.",
                    'openingstijden': "Ma-vr 6:00-23:00, za-zo 8:00-20:00. Groepslessen volgens rooster.",
                    'faciliteiten': "We hebben moderne fitnessapparatuur, groepslessen en personal training beschikbaar."
                },
                'real_estate': {
                    'welkom': f"Welkom bij {company_name}! Zoekt u een huis om te kopen, verkopen of huren?",
                    'bezichtiging': "Voor bezichtigingen kunt u online een afspraak maken of bellen naar 020-1234567.",
                    'openingstijden': "Kantoor: ma-vr 9:00-18:00, za 10:00-16:00. Bezichtigingen ook 's avonds mogelijk.",
                    'waardering': "Voor een gratis woningwaardering kunt u contact met ons opnemen."
                }
            }
            
            # Get business-specific context
            business_context = business_responses.get(business_type, {
                'welkom': f"Welkom bij {company_name}! Hoe kan ik u vandaag van dienst zijn?",
                'contact': "Voor meer informatie kunt u contact met ons opnemen via telefoon of email.",
                'diensten': "Meer informatie over onze diensten vindt u op onze website."
            })
            
            # Demo mode prompt
            prompt = f"""Je bent nu een DEMO chatbot voor {website} ({company_name}).

BEDRIJFSTYPE: {business_type}
BEDRIJFSNAAM: {company_name}

DEMO GEDRAG:
1. Gedraag je als de officiële chatbot van {company_name}
2. Gebruik realistische bedrijfsinformatie passend bij het bedrijfstype
3. Wees vriendelijk, professioneel en behulpzaam
4. Geef korte, praktische antwoorden (max 60 woorden)
5. EINDIGE ALTIJD met: "(Dit is een Botlease AI demo)"

STANDAARD ANTWOORDEN VOOR DIT BEDRIJFSTYPE:
{chr(10).join([f"- {key}: {value}" for key, value in business_context.items()])}

VEELGESTELDE VRAGEN BEANTWOORDEN:
- Openingstijden: Geef realistische tijden passend bij het bedrijfstype
- Contact: Gebruik fictieve maar realistische contactgegevens
- Afspraken: Verwijs naar telefoon/online booking systemen
- Producten/diensten: Beschrijf wat logisch is voor dit bedrijfstype
- Prijzen: "Voor actuele prijzen neem contact op" of verwijs naar website

Laatste berichten:
{chr(10).join(conversation_history[-4:])}

Gebruiker: {user_message}

Beantwoord als de chatbot van {company_name}:"""
        else:
            # Regular prompt - first check if they gave a website
            if url_match:
                company_name = session.get("demo_company_name", "dit bedrijf")
                business_type = session.get("demo_business_type", "algemeen")
                
                prompt = f"""De gebruiker heeft website {website} opgegeven voor de chatbot demo!

ANTWOORD EXACT DIT:
"🎯 Perfect! Ik ben nu de chatbot van {company_name}!

✅ Gedetecteerd bedrijfstype: {business_type}
🤖 Vanaf nu beantwoord ik vragen alsof ik jullie officiële chatbot ben

💬 Stel een vraag die jullie klanten zouden stellen - bijvoorbeeld:
• Wat zijn jullie openingstijden?
• Kan ik een afspraak maken?
• Wat zijn jullie tarieven?

Laat maar zien wat je wilt testen! 👋"

Gebruik dit exacte antwoord, verander er niets aan."""
            else:
                # Normal BotLease prompt
                prompt = f"""{SYSTEM_PROMPT}

CONTEXT VAN DIT GESPREK:
- Bedrijf: {session['company_name']} ({session['industry']})
- Bericht nummer: {len(user_messages)}
- {context_summary}

INSTRUCTIES:
- Als gebruiker nog geen website heeft gegeven, vraag er vriendelijk om
- Focus op het demonstreren van chatbot mogelijkheden

Laatste berichten:
{chr(10).join(conversation_history[-4:])}  

Gebruiker: {user_message}
Assistant:"""
        
        # Genereer response
        response = model.generate_content(prompt)
        ai_response = response.text
        
        # Skip contact referral in demo mode
        if not session.get("demo_mode"):
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
            session = sessions[session_id]
            logger.info(f"Ending conversation {session_id} with {len(session['messages'])} messages")
            
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