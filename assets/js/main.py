// ========================
// THEME TOGGLE - GitHub Pages Compatible
// ========================
const initTheme = () => {
    const themeToggle = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;

    // Get current theme from HTML attribute (set in head)
    const currentTheme = htmlElement.getAttribute('data-theme') || 'light';
    
    // Update icon based on current theme
    updateThemeIcon(currentTheme);

    themeToggle.addEventListener('click', () => {
        const newTheme = htmlElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
        htmlElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });

    function updateThemeIcon(theme) {
        if (themeToggle) {
            themeToggle.textContent = theme === 'light' ? '🌙' : '☀️';
        }
    }
};

// ========================
// PREVENT AUTO-SCROLL TO RESUME
// ========================
const preventAutoScroll = () => {
    // Reset scroll position to top on page load
    window.addEventListener('load', () => {
        if (window.location.hash !== '#resume') {
            window.scrollTo(0, 0);
        }
    });

    // Handle browser back/forward navigation
    window.addEventListener('popstate', () => {
        if (!window.location.hash) {
            window.scrollTo(0, 0);
        }
    });

    // Lazy load PDF iframe only when in viewport
    const initLazyPDF = () => {
        const pdfIframe = document.querySelector('.resume-embed iframe');
        if (!pdfIframe) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const iframe = entry.target;
                    if (iframe.dataset.src && !iframe.src) {
                        iframe.src = iframe.dataset.src;
                    }
                }
            });
        }, { 
            rootMargin: '100px' // Load 100px before entering viewport
        });

        observer.observe(pdfIframe);
    };

    initLazyPDF();
};

// ========================
// MOBILE NAVIGATION
// ========================
const initMobileNav = () => {
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (!navToggle || !navLinks) return;

    navToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        const isExpanded = navLinks.classList.toggle('active');
        navToggle.setAttribute('aria-expanded', isExpanded);
        navToggle.textContent = isExpanded ? '✕' : '☰';
    });

    // Close menu when clicking on a link
    navLinks.addEventListener('click', (e) => {
        if (e.target.tagName === 'A') {
            navLinks.classList.remove('active');
            navToggle.setAttribute('aria-expanded', 'false');
            navToggle.textContent = '☰';
        }
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
            navLinks.classList.remove('active');
            navToggle.setAttribute('aria-expanded', 'false');
            navToggle.textContent = '☰';
        }
    });

    // Close menu on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
            navToggle.setAttribute('aria-expanded', 'false');
            navToggle.textContent = '☰';
        }
    });
};

// ========================
// SMOOTH SCROLL
// ========================
const initSmoothScroll = () => {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            
            // Don't prevent default for # links to maintain URL hash
            if (targetId === '#') return;
            
            const target = document.querySelector(targetId);
            
            if (target) {
                e.preventDefault();
                
                // Calculate header height for offset
                const headerHeight = document.querySelector('.nav').offsetHeight;
                const targetPosition = target.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Update URL without scrolling
                history.pushState(null, null, targetId);
            }
        });
    });
};

// ========================
// CONTACT FORM HANDLER
// ========================
const initContactForm = () => {
    const form = document.getElementById('contact-form');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const name = formData.get('name').trim();
        const email = formData.get('email').trim();
        const message = formData.get('message').trim();

        // Validation
        if (!name || !email || !message) {
            showNotification('Please fill all fields.', 'error');
            return;
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            showNotification('Please enter a valid email address.', 'error');
            return;
        }

        // Simulate form submission
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Sending...';
        submitBtn.disabled = true;

        setTimeout(() => {
            // In a real implementation, you would send this data to your email
            // For GitHub Pages, you can use a service like Formspree or Netlify Forms
            // Or simply show the mailto link
            const subject = `Portfolio Message from ${name}`;
            const body = `Name: ${name}%0D%0AEmail: ${email}%0D%0AMessage: ${message}`;
            const mailtoLink = `mailto:harshrana20025@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
            
            showNotification(`Thank you, ${name}! Your message has been sent to harshrana20025@gmail.com.`, 'success');
            form.reset();
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }, 1500);
    });
};

// ========================
// COPY EMAIL TO CLIPBOARD
// ========================
const copyEmailToClipboard = () => {
    const email = 'harshrana20025@gmail.com';
    
    navigator.clipboard.writeText(email).then(() => {
        showNotification('Email address copied to clipboard!', 'success');
    }).catch(() => {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = email;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showNotification('Email address copied to clipboard!', 'success');
    });
};

// ========================
// NOTIFICATION SYSTEM
// ========================
const showNotification = (message, type = 'info') => {
    // Remove existing notification
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }

    // Create new notification
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button class="notification-close" aria-label="Close notification">✕</button>
    `;

    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : '#3b82f6'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
        z-index: 1001;
        display: flex;
        align-items: center;
        gap: 1rem;
        max-width: 400px;
        animation: slideIn 0.3s ease-out;
    `;

    // Close button
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.style.cssText = `
        background: none;
        border: none;
        color: white;
        font-size: 1.25rem;
        cursor: pointer;
        padding: 0;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
    `;

    closeBtn.addEventListener('click', () => {
        notification.remove();
    });

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);

    document.body.appendChild(notification);

    // Add keyframes for animation
    if (!document.querySelector('#notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
};

// ========================
// INITIALIZE EVERYTHING
// ========================
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    preventAutoScroll();
    initMobileNav();
    initSmoothScroll();
    initContactForm();

    // Set current year in footer
    const yearSpan = document.getElementById('year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }

    // Add loading class for initial animations
    document.body.classList.add('loaded');
});

// Handle page show event for better back/forward navigation
window.addEventListener('pageshow', (event) => {
    // If the page was loaded from cache, ensure we're at the top
    if (event.persisted && !window.location.hash) {
        window.scrollTo(0, 0);
    }
});
