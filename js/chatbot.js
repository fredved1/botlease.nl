// BotLease Chatbot Integration
class BotleaseChat {
    constructor() {
        this.apiUrl = 'http://localhost:5001/api';
        this.sessionId = null;
        this.isConnected = false;
        this.messages = [];
        this.isTyping = false;
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadChatHistory();
        this.connectToBackend();
    }
    
    bindEvents() {
        // Chat input auto-resize
        const chatInput = document.getElementById('chatInput');
        if (chatInput) {
            chatInput.addEventListener('input', this.autoResize.bind(this));
        }
    }
    
    autoResize(event) {
        const textarea = event.target;
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }
    
    async connectToBackend() {
        try {
            const response = await fetch(`${this.apiUrl}/start-conversation`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({})
            });
            
            if (response.ok) {
                const data = await response.json();
                this.sessionId = data.session_id;
                this.isConnected = true;
                console.log('Connected to BotLease backend:', this.sessionId);
            } else {
                throw new Error('Failed to connect');
            }
        } catch (error) {
            console.error('Backend connection failed:', error);
            this.showError('Verbinding met AI-assistent mislukt. Probeer later opnieuw.');
        }
    }
    
    async sendMessage(text) {
        if (!this.isConnected || !this.sessionId) {
            this.showError('Geen verbinding met AI-assistent. Probeer de pagina te verversen.');
            return;
        }
        
        if (this.isTyping) return;
        
        // Add user message to chat
        this.addMessage('user', text);
        
        // Show typing indicator
        this.showTyping();
        
        try {
            const response = await fetch(`${this.apiUrl}/send-message`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    message: text
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                this.hideTyping();
                this.addMessage('bot', data.response);
            } else {
                throw new Error('Failed to send message');
            }
        } catch (error) {
            console.error('Message send failed:', error);
            this.hideTyping();
            this.showError('Bericht kon niet worden verzonden. Probeer opnieuw.');
        }
    }
    
    addMessage(sender, text) {
        const chatMessages = document.getElementById('chatMessages');
        const welcomeMessage = chatMessages.querySelector('.welcome-message');
        
        // Remove welcome message if it exists
        if (welcomeMessage && this.messages.length === 0) {
            welcomeMessage.remove();
        }
        
        const messageEl = document.createElement('div');
        messageEl.className = `message ${sender}`;
        
        const time = new Date().toLocaleTimeString('nl-NL', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        
        const isBot = sender === 'bot';
        const avatar = isBot ? 'AI' : 'U';
        
        // Process markdown for bot messages
        const content = isBot ? marked.parse(text) : text;
        
        messageEl.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                <div class="message-text">${content}</div>
                <div class="message-time">${time}</div>
            </div>
        `;
        
        chatMessages.appendChild(messageEl);
        
        // Store message
        this.messages.push({ sender, text, time });
        
        // Scroll to bottom
        this.scrollToBottom();
        
        // Save to localStorage
        this.saveChatHistory();
    }
    
    showTyping() {
        if (this.isTyping) return;
        
        this.isTyping = true;
        const chatMessages = document.getElementById('chatMessages');
        
        const typingEl = document.createElement('div');
        typingEl.className = 'message bot';
        typingEl.id = 'typingIndicator';
        
        typingEl.innerHTML = `
            <div class="message-avatar">AI</div>
            <div class="message-content">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
        
        chatMessages.appendChild(typingEl);
        this.scrollToBottom();
    }
    
    hideTyping() {
        this.isTyping = false;
        const typingEl = document.getElementById('typingIndicator');
        if (typingEl) {
            typingEl.remove();
        }
    }
    
    showError(message) {
        const chatMessages = document.getElementById('chatMessages');
        
        const errorEl = document.createElement('div');
        errorEl.className = 'chat-error';
        errorEl.textContent = message;
        
        chatMessages.appendChild(errorEl);
        this.scrollToBottom();
        
        // Auto-remove error after 5 seconds
        setTimeout(() => {
            if (errorEl.parentNode) {
                errorEl.remove();
            }
        }, 5000);
    }
    
    scrollToBottom() {
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    saveChatHistory() {
        try {
            localStorage.setItem('botlease_chat_history', JSON.stringify(this.messages));
            localStorage.setItem('botlease_session_id', this.sessionId);
        } catch (e) {
            console.warn('Could not save chat history:', e);
        }
    }
    
    loadChatHistory() {
        try {
            const history = localStorage.getItem('botlease_chat_history');
            const sessionId = localStorage.getItem('botlease_session_id');
            
            if (history && sessionId) {
                this.messages = JSON.parse(history);
                this.sessionId = sessionId;
                
                // Only load recent messages (last 10)
                const recentMessages = this.messages.slice(-10);
                
                if (recentMessages.length > 0) {
                    const chatMessages = document.getElementById('chatMessages');
                    const welcomeMessage = chatMessages.querySelector('.welcome-message');
                    if (welcomeMessage) {
                        welcomeMessage.remove();
                    }
                    
                    recentMessages.forEach(msg => {
                        this.addMessageToDOM(msg.sender, msg.text, msg.time);
                    });
                }
            }
        } catch (e) {
            console.warn('Could not load chat history:', e);
        }
    }
    
    addMessageToDOM(sender, text, time) {
        const chatMessages = document.getElementById('chatMessages');
        
        const messageEl = document.createElement('div');
        messageEl.className = `message ${sender}`;
        
        const isBot = sender === 'bot';
        const avatar = isBot ? 'AI' : 'U';
        const content = isBot ? marked.parse(text) : text;
        
        messageEl.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                <div class="message-text">${content}</div>
                <div class="message-time">${time}</div>
            </div>
        `;
        
        chatMessages.appendChild(messageEl);
    }
    
    clearHistory() {
        this.messages = [];
        this.sessionId = null;
        localStorage.removeItem('botlease_chat_history');
        localStorage.removeItem('botlease_session_id');
        
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.innerHTML = `
            <div class="welcome-message">
                <h3>Welkom bij BotLease! 👋</h3>
                <p>Ik ben uw AI-assistent. Hoe kan ik u helpen met chatbot-oplossingen?</p>
                <div class="quick-actions">
                    <button class="quick-action" onclick="sendQuickMessage('Wat kan BotLease voor mijn bedrijf betekenen?')">
                        Wat kunnen jullie voor mij doen?
                    </button>
                    <button class="quick-action" onclick="sendQuickMessage('Hoeveel kost een eigen chatbot?')">
                        Prijzen & kosten
                    </button>
                    <button class="quick-action" onclick="sendQuickMessage('Hoe krijg ik een eigen chatbot?')">
                        Implementatieproces
                    </button>
                </div>
            </div>
        `;
        
        this.connectToBackend();
    }
}

// Global chat instance
let botleaseChat;

// Global functions for HTML integration
function toggleChat() {
    const chatContainer = document.getElementById('chatContainer');
    const chatToggle = document.querySelector('.chat-toggle');
    
    chatContainer.classList.toggle('active');
    chatToggle.classList.toggle('active');
    
    // Initialize chat if not already done
    if (!botleaseChat && chatContainer.classList.contains('active')) {
        botleaseChat = new BotleaseChat();
    }
    
    // Focus on input when opening
    if (chatContainer.classList.contains('active')) {
        setTimeout(() => {
            const chatInput = document.getElementById('chatInput');
            if (chatInput) {
                chatInput.focus();
            }
        }, 300);
    }
}

function sendMessage(event) {
    event.preventDefault();
    
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();
    
    if (message && botleaseChat) {
        botleaseChat.sendMessage(message);
        chatInput.value = '';
        chatInput.style.height = 'auto';
    }
}

function sendQuickMessage(message) {
    if (botleaseChat) {
        botleaseChat.sendMessage(message);
    }
}

function handleChatKeydown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage(event);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Pre-warm the chat connection if user seems engaged
    let userEngaged = false;
    
    // Track user engagement
    function trackEngagement() {
        if (!userEngaged) {
            userEngaged = true;
            // Pre-initialize chat after user shows interest
            setTimeout(() => {
                if (!botleaseChat) {
                    botleaseChat = new BotleaseChat();
                }
            }, 2000);
        }
    }
    
    // Add engagement listeners
    document.addEventListener('scroll', trackEngagement, { once: true });
    document.addEventListener('mousemove', trackEngagement, { once: true });
    document.addEventListener('click', trackEngagement, { once: true });
    
    // Auto-initialize after 10 seconds regardless
    setTimeout(() => {
        if (!botleaseChat) {
            botleaseChat = new BotleaseChat();
        }
    }, 10000);
});