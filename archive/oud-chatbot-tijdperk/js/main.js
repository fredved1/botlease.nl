// BotLease Main JavaScript
class BotleaseWebsite {
    constructor() {
        this.init();
    }
    
    init() {
        this.setupNavigation();
        this.setupScrollEffects();
        this.setupAnimations();
        this.setupInteractions();
        this.setupMobileMenu();
    }
    
    setupNavigation() {
        const nav = document.querySelector('.nav');
        const navToggle = document.querySelector('.nav-toggle');
        const navMenu = document.querySelector('.nav-menu');
        
        // Navbar scroll effect
        let lastScrollY = window.scrollY;
        
        window.addEventListener('scroll', () => {
            const currentScrollY = window.scrollY;
            
            // Background blur effect
            if (currentScrollY > 100) {
                nav.style.background = 'rgba(10, 10, 10, 0.95)';
                nav.style.backdropFilter = 'blur(20px)';
                nav.style.borderBottomColor = 'rgba(255, 255, 255, 0.15)';
            } else {
                nav.style.background = 'rgba(10, 10, 10, 0.8)';
                nav.style.backdropFilter = 'blur(20px)';
                nav.style.borderBottomColor = 'rgba(255, 255, 255, 0.1)';
            }
            
            // Hide/show navbar on scroll
            if (currentScrollY > lastScrollY && currentScrollY > 100) {
                nav.style.transform = 'translateY(-100%)';
            } else {
                nav.style.transform = 'translateY(0)';
            }
            
            lastScrollY = currentScrollY;
        });
        
        // Mobile menu toggle
        if (navToggle && navMenu) {
            navToggle.addEventListener('click', () => {
                navMenu.classList.toggle('active');
                navToggle.classList.toggle('active');
                document.body.classList.toggle('menu-open');
            });
            
            // Close mobile menu when clicking links
            document.querySelectorAll('.nav-link').forEach(link => {
                link.addEventListener('click', () => {
                    navMenu.classList.remove('active');
                    navToggle.classList.remove('active');
                    document.body.classList.remove('menu-open');
                });
            });
        }
    }
    
    setupMobileMenu() {
        // Create mobile menu styles dynamically
        const style = document.createElement('style');
        style.textContent = `
            @media (max-width: 768px) {
                .nav-menu {
                    position: fixed;
                    top: 0;
                    right: -100%;
                    width: 100%;
                    height: 100vh;
                    background: var(--bg-primary);
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    transition: right 0.3s ease;
                    z-index: 999;
                    gap: var(--space-8);
                }
                
                .nav-menu.active {
                    right: 0;
                }
                
                .nav-toggle {
                    display: flex;
                    z-index: 1001;
                }
                
                .nav-toggle.active span:nth-child(1) {
                    transform: rotate(45deg) translate(5px, 5px);
                }
                
                .nav-toggle.active span:nth-child(2) {
                    opacity: 0;
                }
                
                .nav-toggle.active span:nth-child(3) {
                    transform: rotate(-45deg) translate(7px, -6px);
                }
                
                .nav-link {
                    font-size: var(--font-size-xl);
                    color: var(--text-primary);
                }
                
                body.menu-open {
                    overflow: hidden;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    setupScrollEffects() {
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    const headerOffset = 100;
                    const elementPosition = target.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
        
        // Parallax effects for hero section
        const hero = document.querySelector('.hero');
        if (hero) {
            window.addEventListener('scroll', () => {
                const scrolled = window.pageYOffset;
                const rate = scrolled * -0.5;
                hero.style.transform = `translateY(${rate}px)`;
            });
        }
    }
    
    setupAnimations() {
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -10% 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    
                    // Add staggered animation for grid items
                    if (entry.target.classList.contains('grid')) {
                        const children = entry.target.children;
                        Array.from(children).forEach((child, index) => {
                            setTimeout(() => {
                                child.classList.add('fade-in-up');
                            }, index * 100);
                        });
                    }
                }
            });
        }, observerOptions);
        
        // Observe elements for animation
        document.querySelectorAll('.fade-in-up, .section-header, .card, .feature-item, .process-step, .testimonial').forEach(el => {
            observer.observe(el);
        });
    }
    
    setupInteractions() {
        // Enhanced button interactions
        document.querySelectorAll('.btn').forEach(button => {
            button.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px)';
                
                if (this.classList.contains('btn-primary')) {
                    this.style.boxShadow = '0 8px 25px rgba(102, 126, 234, 0.5)';
                } else if (this.classList.contains('btn-secondary')) {
                    this.style.background = 'rgba(255, 255, 255, 0.1)';
                }
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.transform = '';
                this.style.boxShadow = '';
                
                if (this.classList.contains('btn-secondary')) {
                    this.style.background = '';
                }
            });
            
            // Click effect
            button.addEventListener('click', function(e) {
                const ripple = document.createElement('div');
                ripple.style.position = 'absolute';
                ripple.style.borderRadius = '50%';
                ripple.style.background = 'rgba(255, 255, 255, 0.6)';
                ripple.style.transform = 'scale(0)';
                ripple.style.animation = 'ripple 0.6s linear';
                ripple.style.left = (e.clientX - this.getBoundingClientRect().left) + 'px';
                ripple.style.top = (e.clientY - this.getBoundingClientRect().top) + 'px';
                ripple.style.width = ripple.style.height = '40px';
                ripple.style.marginLeft = ripple.style.marginTop = '-20px';
                
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
        
        // Card hover effects with tilt
        document.querySelectorAll('.card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-8px) scale(1.02)';
                this.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.3)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = '';
                this.style.boxShadow = '';
            });
            
            // 3D tilt effect
            card.addEventListener('mousemove', function(e) {
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = (y - centerY) / 10;
                const rotateY = (centerX - x) / 10;
                
                this.style.transform = `translateY(-8px) scale(1.02) perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            });
        });
        
        // Feature icon animations
        document.querySelectorAll('.feature-icon').forEach(icon => {
            icon.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.1) rotate(5deg)';
                this.style.boxShadow = '0 8px 30px rgba(102, 126, 234, 0.5)';
            });
            
            icon.addEventListener('mouseleave', function() {
                this.style.transform = '';
                this.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.3)';
            });
        });
    }
    
    // Utility methods
    throttle(func, wait) {
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

// Custom cursor effect for interactive elements
class CustomCursor {
    constructor() {
        this.cursor = null;
        this.init();
    }
    
    init() {
        // Create cursor elements
        this.cursor = document.createElement('div');
        this.cursor.className = 'custom-cursor';
        document.body.appendChild(this.cursor);
        
        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            .custom-cursor {
                position: fixed;
                width: 20px;
                height: 20px;
                background: rgba(102, 126, 234, 0.5);
                border-radius: 50%;
                pointer-events: none;
                z-index: 9999;
                transform: translate(-50%, -50%);
                transition: all 0.1s ease;
                opacity: 0;
            }
            
            .custom-cursor.active {
                opacity: 1;
            }
            
            .custom-cursor.hover {
                width: 40px;
                height: 40px;
                background: rgba(102, 126, 234, 0.2);
                border: 2px solid rgba(102, 126, 234, 0.8);
            }
            
            @media (max-width: 768px) {
                .custom-cursor {
                    display: none;
                }
            }
        `;
        document.head.appendChild(style);
        
        this.bindEvents();
    }
    
    bindEvents() {
        document.addEventListener('mousemove', (e) => {
            this.cursor.style.left = e.clientX + 'px';
            this.cursor.style.top = e.clientY + 'px';
            this.cursor.classList.add('active');
        });
        
        document.addEventListener('mouseenter', () => {
            this.cursor.classList.add('active');
        });
        
        document.addEventListener('mouseleave', () => {
            this.cursor.classList.remove('active');
        });
        
        // Hover effects
        document.querySelectorAll('a, button, .card, .btn').forEach(el => {
            el.addEventListener('mouseenter', () => {
                this.cursor.classList.add('hover');
            });
            
            el.addEventListener('mouseleave', () => {
                this.cursor.classList.remove('hover');
            });
        });
    }
}

// Add ripple animation keyframes
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(rippleStyle);

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize main website functionality
    new BotleaseWebsite();
    
    // Initialize custom cursor (desktop only)
    if (window.innerWidth > 768) {
        new CustomCursor();
    }
    
    // Add loading animation
    document.body.classList.add('loaded');
    
    // Performance optimization: lazy load images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // Add dark theme toggle (hidden, for development)
    if (localStorage.getItem('botlease_dev_mode') === 'true') {
        const themeToggle = document.createElement('button');
        themeToggle.textContent = '🌙';
        themeToggle.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            z-index: 1000;
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
        `;
        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('light-theme');
        });
        document.body.appendChild(themeToggle);
    }
});

// Keyboard navigation support
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        // Close any open modals/menus
        const navMenu = document.querySelector('.nav-menu');
        const navToggle = document.querySelector('.nav-toggle');
        
        if (navMenu && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
            document.body.classList.remove('menu-open');
        }
    }
});

// Focus management for accessibility
document.addEventListener('focusin', (e) => {
    if (e.target.matches('.btn, .nav-link, input, textarea, button')) {
        e.target.style.outline = '2px solid rgba(102, 126, 234, 0.8)';
        e.target.style.outlineOffset = '2px';
    }
});

document.addEventListener('focusout', (e) => {
    if (e.target.matches('.btn, .nav-link, input, textarea, button')) {
        e.target.style.outline = '';
        e.target.style.outlineOffset = '';
    }
});

// Error handling for failed resources
window.addEventListener('error', (e) => {
    if (e.target.tagName === 'IMG') {
        e.target.style.display = 'none';
    }
});

// Performance monitoring (development only)
if (localStorage.getItem('botlease_dev_mode') === 'true') {
    window.addEventListener('load', () => {
        setTimeout(() => {
            if ('performance' in window) {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
                console.log('DOM ready time:', perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart, 'ms');
            }
        }, 1000);
    });
}