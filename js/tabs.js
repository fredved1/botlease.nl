// Tab Navigation System - Based on the provided tab code
class TabSystem {
    constructor() {
        this.activeIndex = 0;
        this.hoveredIndex = null;
        this.tabElements = [];
        this.contentElements = [];
        this.hoverHighlight = null;
        this.activeIndicator = null;
        
        this.init();
    }
    
    init() {
        this.setupElements();
        this.bindEvents();
        this.updateActiveIndicator();
        
        // Initial setup after DOM is ready
        requestAnimationFrame(() => {
            this.updateActiveIndicator();
        });
    }
    
    setupElements() {
        // Get tab elements
        this.tabElements = Array.from(document.querySelectorAll('.tab-item'));
        
        // Get content elements
        this.contentElements = Array.from(document.querySelectorAll('.tab-content'));
        
        // Get hover and active indicators
        this.hoverHighlight = document.getElementById('hoverHighlight');
        this.activeIndicator = document.getElementById('activeIndicator');
        
        if (!this.hoverHighlight || !this.activeIndicator) {
            console.warn('Tab indicators not found');
            return;
        }
    }
    
    bindEvents() {
        this.tabElements.forEach((tab, index) => {
            // Mouse enter event
            tab.addEventListener('mouseenter', () => {
                this.hoveredIndex = index;
                this.updateHoverHighlight();
            });
            
            // Mouse leave event
            tab.addEventListener('mouseleave', () => {
                this.hoveredIndex = null;
                this.updateHoverHighlight();
            });
            
            // Click event
            tab.addEventListener('click', () => {
                this.setActiveTab(index);
            });
        });
        
        // Window resize event
        window.addEventListener('resize', this.debounce(() => {
            this.updateActiveIndicator();
        }, 250));
    }
    
    updateHoverHighlight() {
        if (!this.hoverHighlight) return;
        
        if (this.hoveredIndex !== null) {
            const hoveredElement = this.tabElements[this.hoveredIndex];
            if (hoveredElement) {
                const { offsetLeft, offsetWidth } = hoveredElement;
                this.hoverHighlight.style.left = `${offsetLeft}px`;
                this.hoverHighlight.style.width = `${offsetWidth}px`;
                this.hoverHighlight.style.opacity = '1';
            }
        } else {
            this.hoverHighlight.style.opacity = '0';
        }
    }
    
    updateActiveIndicator() {
        if (!this.activeIndicator) return;
        
        const activeElement = this.tabElements[this.activeIndex];
        if (activeElement) {
            const { offsetLeft, offsetWidth } = activeElement;
            this.activeIndicator.style.left = `${offsetLeft}px`;
            this.activeIndicator.style.width = `${offsetWidth}px`;
        }
    }
    
    setActiveTab(index) {
        if (index === this.activeIndex) return;
        
        // Remove active class from previous tab and content
        if (this.tabElements[this.activeIndex]) {
            this.tabElements[this.activeIndex].classList.remove('active');
        }
        if (this.contentElements[this.activeIndex]) {
            this.contentElements[this.activeIndex].classList.remove('active');
        }
        
        // Set new active index
        this.activeIndex = index;
        
        // Add active class to new tab and content
        if (this.tabElements[this.activeIndex]) {
            this.tabElements[this.activeIndex].classList.add('active');
        }
        if (this.contentElements[this.activeIndex]) {
            this.contentElements[this.activeIndex].classList.add('active');
        }
        
        // Update active indicator
        this.updateActiveIndicator();
        
        // Handle special case for demo tab (initialize chatbot)
        if (index === 0 && typeof window.botleaseChat === 'undefined') {
            // Initialize chatbot when demo tab is activated
            setTimeout(() => {
                if (typeof BotleaseChat !== 'undefined') {
                    window.botleaseChat = new BotleaseChat();
                }
            }, 500);
        }
    }
    
    // Utility function for debouncing
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Enhanced Chat Message Management
class ChatMessageManager {
    constructor() {
        this.messageContainer = null;
        this.welcomeScreen = null;
        this.init();
    }
    
    init() {
        this.messageContainer = document.getElementById('chatMessages');
        this.welcomeScreen = document.querySelector('.welcome-screen');
    }
    
    addMessage(sender, text, time) {
        if (!this.messageContainer) return;
        
        // Hide welcome screen when first message is sent
        if (this.welcomeScreen && this.welcomeScreen.style.display !== 'none') {
            this.welcomeScreen.style.display = 'none';
        }
        
        const messageEl = document.createElement('div');
        messageEl.className = `message ${sender}`;
        
        const isBot = sender === 'bot';
        const avatar = isBot ? 'AI' : 'U';
        
        // Process markdown for bot messages if marked is available
        const content = isBot && typeof marked !== 'undefined' ? marked.parse(text) : text;
        
        messageEl.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                <div class="message-text">${content}</div>
                <div class="message-time">${time}</div>
            </div>
        `;
        
        this.messageContainer.appendChild(messageEl);
        this.scrollToBottom();
        
        // Add vibration effect for new messages (if supported)
        if ('vibrate' in navigator && sender === 'bot') {
            navigator.vibrate([50]);
        }
    }
    
    addTypingIndicator() {
        if (!this.messageContainer) return;
        
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
        
        this.messageContainer.appendChild(typingEl);
        this.scrollToBottom();
    }
    
    removeTypingIndicator() {
        const typingEl = document.getElementById('typingIndicator');
        if (typingEl) {
            typingEl.remove();
        }
    }
    
    clearMessages() {
        if (!this.messageContainer) return;
        
        this.messageContainer.innerHTML = `
            <div class="welcome-screen">
                <div class="welcome-animation">
                    <div class="pulse-ring"></div>
                    <div class="pulse-ring"></div>
                    <div class="pulse-ring"></div>
                    <div class="ai-logo">AI</div>
                </div>
                <h4>Welkom bij BotLease! 👋</h4>
                <p>Ik ben uw AI-consultant en help u ontdekken hoe AI-automatisering uw bedrijf kan versterken.</p>
                
                <div class="quick-actions-grid">
                    <button class="quick-action-card" onclick="sendQuickMessage('Wat kan BotLease voor mijn bedrijf betekenen?')">
                        <div class="action-icon">💡</div>
                        <div class="action-text">Wat kunnen jullie voor mijn bedrijf doen?</div>
                    </button>
                    
                    <button class="quick-action-card" onclick="sendQuickMessage('Hoe werkt jullie no cure no pay principe?')">
                        <div class="action-icon">✅</div>
                        <div class="action-text">Hoe werkt no cure, no pay?</div>
                    </button>
                    
                    <button class="quick-action-card" onclick="sendQuickMessage('Hoeveel kost een pilot en wat krijg ik daarvoor?')">
                        <div class="action-icon">💰</div>
                        <div class="action-text">Kosten en wat krijg ik?</div>
                    </button>
                    
                    <button class="quick-action-card" onclick="sendQuickMessage('Welke processen kunnen jullie automatiseren?')">
                        <div class="action-icon">⚙️</div>
                        <div class="action-text">Welke processen automatiseren?</div>
                    </button>
                </div>
            </div>
        `;
        
        this.welcomeScreen = document.querySelector('.welcome-screen');
    }
    
    scrollToBottom() {
        if (this.messageContainer) {
            this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
        }
    }
    
    showError(message) {
        if (!this.messageContainer) return;
        
        const errorEl = document.createElement('div');
        errorEl.className = 'chat-error';
        errorEl.textContent = message;
        
        this.messageContainer.appendChild(errorEl);
        this.scrollToBottom();
        
        // Auto-remove error after 5 seconds
        setTimeout(() => {
            if (errorEl.parentNode) {
                errorEl.remove();
            }
        }, 5000);
    }
}

// Enhanced Input Handling
class ChatInputHandler {
    constructor() {
        this.input = null;
        this.sendButton = null;
        this.init();
    }
    
    init() {
        this.input = document.getElementById('chatInput');
        this.sendButton = document.getElementById('sendBtn');
        
        if (this.input) {
            this.bindEvents();
        }
    }
    
    bindEvents() {
        // Auto-resize functionality
        this.input.addEventListener('input', (e) => {
            this.autoResize(e.target);
        });
        
        // Enhanced send button state
        this.input.addEventListener('input', () => {
            this.updateSendButtonState();
        });
        
        // Focus effects
        this.input.addEventListener('focus', () => {
            this.input.parentElement.classList.add('focused');
        });
        
        this.input.addEventListener('blur', () => {
            this.input.parentElement.classList.remove('focused');
        });
        
        // Keyboard shortcuts
        this.input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }
    
    autoResize(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 100) + 'px';
    }
    
    updateSendButtonState() {
        const hasText = this.input.value.trim().length > 0;
        if (this.sendButton) {
            this.sendButton.style.opacity = hasText ? '1' : '0.6';
            this.sendButton.style.transform = hasText ? 'scale(1)' : 'scale(0.9)';
        }
    }
    
    sendMessage() {
        const message = this.input.value.trim();
        if (message && window.botleaseChat) {
            window.botleaseChat.sendMessage(message);
            this.clearInput();
        }
    }
    
    clearInput() {
        this.input.value = '';
        this.input.style.height = 'auto';
        this.updateSendButtonState();
    }
    
    focus() {
        if (this.input) {
            this.input.focus();
        }
    }
}

// Animation Controller
class AnimationController {
    constructor() {
        this.init();
    }
    
    init() {
        this.setupIntersectionObserver();
        this.setupParallaxEffects();
    }
    
    setupIntersectionObserver() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -10% 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'fadeIn 0.6s ease-out forwards';
                }
            });
        }, observerOptions);
        
        // Observe cards and other elements
        document.querySelectorAll('.feature-card, .pricing-card, .case-card, .process-step').forEach(el => {
            observer.observe(el);
        });
    }
    
    setupParallaxEffects() {
        // Add subtle parallax to hero elements
        window.addEventListener('scroll', this.throttle(() => {
            const scrolled = window.pageYOffset;
            const heroSection = document.querySelector('.hero-section');
            
            if (heroSection) {
                const rate = scrolled * -0.2;
                heroSection.style.transform = `translateY(${rate}px)`;
            }
        }, 16));
    }
    
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }
}

// Enhanced Performance Monitor
class PerformanceMonitor {
    constructor() {
        this.metrics = {};
        this.init();
    }
    
    init() {
        if ('performance' in window) {
            this.trackPageLoad();
            this.trackUserInteractions();
        }
    }
    
    trackPageLoad() {
        window.addEventListener('load', () => {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                this.metrics.loadTime = perfData.loadEventEnd - perfData.loadEventStart;
                this.metrics.domReady = perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart;
                
                if (localStorage.getItem('botlease_dev_mode') === 'true') {
                    console.log('Performance Metrics:', this.metrics);
                }
            }, 1000);
        });
    }
    
    trackUserInteractions() {
        let interactionCount = 0;
        
        ['click', 'scroll', 'keydown'].forEach(eventType => {
            document.addEventListener(eventType, () => {
                interactionCount++;
            }, { once: true });
        });
        
        this.metrics.userEngaged = () => interactionCount > 0;
    }
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Initialize tab system
    window.tabSystem = new TabSystem();
    
    // Initialize chat message manager
    window.messageManager = new ChatMessageManager();
    
    // Initialize input handler
    window.inputHandler = new ChatInputHandler();
    
    // Initialize animations
    window.animationController = new AnimationController();
    
    // Initialize performance monitoring
    window.performanceMonitor = new PerformanceMonitor();
    
    // Add global error handling
    window.addEventListener('error', (e) => {
        if (e.target.tagName === 'IMG') {
            e.target.style.display = 'none';
        }
    });
    
    // Add accessibility enhancements
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            // Close any open modals or reset focus
            const activeElement = document.activeElement;
            if (activeElement && activeElement.blur) {
                activeElement.blur();
            }
        }
    });
});

// Global functions for backward compatibility
function sendQuickMessage(message) {
    if (window.botleaseChat) {
        window.botleaseChat.sendMessage(message);
    }
}

function clearChat() {
    if (window.messageManager) {
        window.messageManager.clearMessages();
    }
    if (window.botleaseChat) {
        window.botleaseChat.clearHistory();
    }
}