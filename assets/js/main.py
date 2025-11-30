// ========================
// THEME TOGGLE
// ========================
const initTheme = () => {
    const themeToggle = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;

    // Get saved theme or default to light
    const currentTheme = localStorage.getItem('theme') || 'light';
    htmlElement.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme);

    themeToggle.addEventListener('click', () => {
        const newTheme = htmlElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
        htmlElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });

    function updateThemeIcon(theme) {
        themeToggle.textContent = theme === 'light' ? '🌙' : '☀️';
    }
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
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const target = document.querySelector(targetId);
            
            if (target) {
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
            showNotification(`Thank you, ${name}! Your message has been sent. I'll get back to you soon.`, 'success');
            form.reset();
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }, 1500);
    });
};

// ========================
// RESUME UPLOAD
// ========================
const initResumeUpload = () => {
    const fileInput = document.getElementById('upload');
    if (!fileInput) return;

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;

        // Validate file type
        if (file.type !== 'application/pdf') {
            showNotification('Please upload a PDF file only.', 'error');
            fileInput.value = '';
            return;
        }

        // Validate file size (5MB)
        if (file.size > 5 * 1024 * 1024) {
            showNotification('File size must be less than 5MB.', 'error');
            fileInput.value = '';
            return;
        }

        // Preview the uploaded PDF
        const iframe = document.querySelector('.resume-embed iframe');
        if (iframe) {
            iframe.src = URL.createObjectURL(file);
            showNotification(`Resume "${file.name}" uploaded successfully!`, 'success');
        }
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
// INTERSECTION OBSERVER FOR ACTIVE NAV LINKS
// ========================
const initScrollSpy = () => {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-links a[href^="#"]');

    const observerOptions = {
        rootMargin: '-20% 0px -60% 0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${id}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }, observerOptions);

    sections.forEach(section => observer.observe(section));
};

// ========================
// LAZY LOADING FOR IMAGES
// ========================
const initLazyLoading = () => {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for older browsers
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }
};

// ========================
// INITIALIZE EVERYTHING
// ========================
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initMobileNav();
    initSmoothScroll();
    initContactForm();
    initResumeUpload();
    initScrollSpy();
    initLazyLoading();

    // Set current year in footer
    const yearSpan = document.getElementById('year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }

    // Add loading class for initial animations
    document.body.classList.add('loaded');
});

// ========================
// PERFORMANCE OPTIMIZATIONS
// ========================
// Debounce function for scroll events
const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

// Handle window resize
window.addEventListener('resize', debounce(() => {
    // Close mobile menu on resize to desktop
    if (window.innerWidth > 768) {
        const navLinks = document.querySelector('.nav-links');
        const navToggle = document.querySelector('.nav-toggle');
        if (navLinks && navToggle) {
            navLinks.classList.remove('active');
            navToggle.setAttribute('aria-expanded', 'false');
            navToggle.textContent = '☰';
        }
    }
}, 250));
