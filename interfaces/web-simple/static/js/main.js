/* ============================================
   Main JavaScript - Common Utilities
   NUAA Web Tools
   ============================================ */

// Global utilities
window.NUAA = window.NUAA || {};

// Service Worker registration for PWA
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/service-worker.js')
            .then(registration => {
                console.log('✅ Service Worker registered:', registration.scope);
            })
            .catch(error => {
                console.log('Service Worker registration failed:', error);
            });
    });
}

// Check for updates
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.addEventListener('controllerchange', () => {
        if (confirm('A new version is available. Reload to update?')) {
            window.location.reload();
        }
    });
}

// Online/Offline detection
window.addEventListener('online', () => {
    console.log('✅ Back online');
    showConnectionToast('Connected to internet', 'success');
});

window.addEventListener('offline', () => {
    console.log('⚠️ Offline');
    showConnectionToast('Working offline', 'warning');
});

function showConnectionToast(message, type) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        background: ${type === 'success' ? '#51cf66' : '#ff6b6b'};
        color: white;
        padding: 15px 30px;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        z-index: 10000;
    `;
    document.body.appendChild(toast);

    setTimeout(() => toast.remove(), 3000);
}

// Install PWA prompt
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;

    // Show custom install button
    showInstallPrompt();
});

function showInstallPrompt() {
    const prompt = document.createElement('div');
    prompt.className = 'install-prompt';
    prompt.innerHTML = `
        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.2); max-width: 400px; margin: 20px auto;">
            <h3 style="margin-bottom: 10px;">Install NUAA Tools</h3>
            <p style="margin-bottom: 20px;">Install this app for quick access and offline use!</p>
            <div style="display: flex; gap: 10px;">
                <button onclick="installPWA()" class="btn primary">Install</button>
                <button onclick="dismissInstallPrompt()" class="btn secondary">Not Now</button>
            </div>
        </div>
    `;
    prompt.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 0;
        right: 0;
        z-index: 10000;
    `;

    // Don't show if user dismissed before
    if (localStorage.getItem('installPromptDismissed') !== 'true') {
        document.body.appendChild(prompt);
    }
}

window.installPWA = async () => {
    if (!deferredPrompt) return;

    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;

    console.log(`User ${outcome} the install prompt`);
    deferredPrompt = null;

    document.querySelector('.install-prompt')?.remove();
};

window.dismissInstallPrompt = () => {
    localStorage.setItem('installPromptDismissed', 'true');
    document.querySelector('.install-prompt')?.remove();
};

// Global error handler
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    // You can send error reports to a logging service here
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});

// Accessibility helpers
NUAA.accessibility = {
    loadPreferences: () => {
        const preferences = JSON.parse(localStorage.getItem('accessibilitySettings') || '{}');

        if (preferences.highContrast) {
            document.body.classList.add('high-contrast');
        }
        if (preferences.darkMode) {
            document.body.classList.add('dark-mode');
        }
        if (preferences.reduceMotion) {
            document.body.classList.add('reduce-motion');
        }
        if (preferences.fontSize) {
            document.body.classList.add(`font-${preferences.fontSize}`);
        }
    },

    skipToContent: () => {
        const main = document.querySelector('main');
        if (main) {
            main.setAttribute('tabindex', '-1');
            main.focus();
            main.removeAttribute('tabindex');
        }
    }
};

// Analytics (privacy-friendly)
NUAA.analytics = {
    trackPageView: (page) => {
        const pageViews = JSON.parse(localStorage.getItem('pageViews') || '[]');
        pageViews.push({
            page,
            timestamp: new Date().toISOString()
        });

        // Keep only last 100 page views
        if (pageViews.length > 100) {
            pageViews.shift();
        }

        localStorage.setItem('pageViews', JSON.stringify(pageViews));
    },

    trackEvent: (category, action, label) => {
        const events = JSON.parse(localStorage.getItem('analyticsEvents') || '[]');
        events.push({
            category,
            action,
            label,
            timestamp: new Date().toISOString()
        });

        // Keep only last 100 events
        if (events.length > 100) {
            events.shift();
        }

        localStorage.setItem('analyticsEvents', JSON.stringify(events));
    },

    getStats: () => {
        const pageViews = JSON.parse(localStorage.getItem('pageViews') || '[]');
        const events = JSON.parse(localStorage.getItem('analyticsEvents') || '[]');

        return {
            pageViews: pageViews.length,
            events: events.length,
            recentPages: pageViews.slice(-10),
            recentEvents: events.slice(-10)
        };
    }
};

// Theme management
NUAA.theme = {
    set: (theme) => {
        document.body.className = '';
        if (theme !== 'default') {
            document.body.classList.add(`theme-${theme}`);
        }
        localStorage.setItem('theme', theme);
    },

    get: () => {
        return localStorage.getItem('theme') || 'default';
    },

    load: () => {
        const theme = NUAA.theme.get();
        NUAA.theme.set(theme);
    }
};

// Network monitoring
NUAA.network = {
    isOnline: () => navigator.onLine,

    checkConnection: async () => {
        if (!navigator.onLine) return false;

        try {
            const response = await fetch('/', { method: 'HEAD', cache: 'no-cache' });
            return response.ok;
        } catch {
            return false;
        }
    },

    onConnectionChange: (callback) => {
        window.addEventListener('online', () => callback(true));
        window.addEventListener('offline', () => callback(false));
    }
};

// Data export utilities
NUAA.export = {
    toJSON: (data, filename) => {
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        NUAA.export.download(blob, filename || 'data.json');
    },

    toCSV: (data, filename) => {
        if (!Array.isArray(data) || data.length === 0) return;

        const headers = Object.keys(data[0]);
        const csv = [
            headers.join(','),
            ...data.map(row => headers.map(header => JSON.stringify(row[header] || '')).join(','))
        ].join('\n');

        const blob = new Blob([csv], { type: 'text/csv' });
        NUAA.export.download(blob, filename || 'data.csv');
    },

    download: (blob, filename) => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Load accessibility preferences
    NUAA.accessibility.loadPreferences();

    // Load theme
    NUAA.theme.load();

    // Track page view
    NUAA.analytics.trackPageView(window.location.pathname);

    // Add skip to content link for accessibility
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.className = 'skip-link';
    skipLink.textContent = 'Skip to main content';
    skipLink.style.cssText = `
        position: absolute;
        top: -40px;
        left: 0;
        background: var(--primary-color, #2c5aa0);
        color: white;
        padding: 8px 16px;
        text-decoration: none;
        z-index: 10000;
    `;
    skipLink.addEventListener('focus', () => {
        skipLink.style.top = '0';
    });
    skipLink.addEventListener('blur', () => {
        skipLink.style.top = '-40px';
    });
    document.body.insertBefore(skipLink, document.body.firstChild);

    console.log('✅ NUAA Tools initialized');
});

// Expose NUAA globally
window.NUAA = NUAA;
