/* ============================================
   Theme Switcher - Dark Mode & Custom Themes
   ============================================ */

const ThemeSwitcher = {
    currentTheme: 'light',
    availableThemes: ['light', 'dark', 'high-contrast', 'sepia', 'ocean'],

    init() {
        // Load saved theme
        const savedTheme = localStorage.getItem('theme') || 'light';
        this.setTheme(savedTheme);

        // Add theme toggle button
        this.createToggleButton();

        // Add theme selector panel
        this.createThemeSelector();

        // Listen for system theme changes
        this.watchSystemTheme();
    },

    createToggleButton() {
        const button = document.createElement('button');
        button.className = 'theme-toggle';
        button.id = 'themeToggle';
        button.setAttribute('aria-label', 'Toggle theme');
        button.innerHTML = '🌙';
        button.onclick = () => this.toggleThemeSelector();

        document.body.appendChild(button);
    },

    createThemeSelector() {
        const selector = document.createElement('div');
        selector.className = 'theme-selector';
        selector.id = 'themeSelector';
        selector.innerHTML = `
            <h4 style="margin-bottom: 1rem;">Choose Theme</h4>
            <div class="theme-option" data-theme="light">
                <div class="theme-preview light"></div>
                <div>
                    <strong>Light</strong>
                    <div style="font-size: 0.85rem; color: var(--gray-600);">Default bright theme</div>
                </div>
            </div>
            <div class="theme-option" data-theme="dark">
                <div class="theme-preview dark"></div>
                <div>
                    <strong>Dark</strong>
                    <div style="font-size: 0.85rem; color: var(--gray-600);">Easy on the eyes</div>
                </div>
            </div>
            <div class="theme-option" data-theme="high-contrast">
                <div class="theme-preview high-contrast"></div>
                <div>
                    <strong>High Contrast</strong>
                    <div style="font-size: 0.85rem; color: var(--gray-600);">Maximum readability</div>
                </div>
            </div>
            <div class="theme-option" data-theme="sepia">
                <div class="theme-preview sepia"></div>
                <div>
                    <strong>Sepia</strong>
                    <div style="font-size: 0.85rem; color: var(--gray-600);">Warm reading mode</div>
                </div>
            </div>
            <div class="theme-option" data-theme="ocean">
                <div class="theme-preview ocean"></div>
                <div>
                    <strong>Ocean Blue</strong>
                    <div style="font-size: 0.85rem; color: var(--gray-600);">Cool and calm</div>
                </div>
            </div>
        `;

        document.body.appendChild(selector);

        // Add click handlers
        selector.querySelectorAll('.theme-option').forEach(option => {
            option.onclick = () => {
                const theme = option.dataset.theme;
                this.setTheme(theme);
                this.toggleThemeSelector();
            };
        });

        // Close when clicking outside
        document.addEventListener('click', (e) => {
            if (!selector.contains(e.target) && !document.getElementById('themeToggle').contains(e.target)) {
                selector.classList.remove('show');
            }
        });
    },

    toggleThemeSelector() {
        const selector = document.getElementById('themeSelector');
        selector.classList.toggle('show');

        // Update active theme indication
        selector.querySelectorAll('.theme-option').forEach(option => {
            if (option.dataset.theme === this.currentTheme) {
                option.classList.add('active');
            } else {
                option.classList.remove('active');
            }
        });
    },

    setTheme(theme) {
        // Remove all theme classes
        document.body.classList.remove('dark-mode', 'theme-high-contrast', 'theme-sepia', 'theme-ocean');

        // Apply new theme
        if (theme === 'dark') {
            document.body.classList.add('dark-mode');
        } else if (theme !== 'light') {
            document.body.classList.add(`theme-${theme}`);
        }

        // Update toggle button icon
        const icons = {
            'light': '🌙',
            'dark': '☀️',
            'high-contrast': '⚫',
            'sepia': '📖',
            'ocean': '🌊'
        };

        const toggleBtn = document.getElementById('themeToggle');
        if (toggleBtn) {
            toggleBtn.innerHTML = icons[theme];
        }

        // Save preference
        this.currentTheme = theme;
        localStorage.setItem('theme', theme);

        // Update meta theme-color for mobile browsers
        let metaThemeColor = document.querySelector('meta[name="theme-color"]');
        if (!metaThemeColor) {
            metaThemeColor = document.createElement('meta');
            metaThemeColor.name = 'theme-color';
            document.head.appendChild(metaThemeColor);
        }

        const themeColors = {
            'light': '#2c5aa0',
            'dark': '#1a1a1a',
            'high-contrast': '#000000',
            'sepia': '#f4ecd8',
            'ocean': '#006994'
        };

        metaThemeColor.content = themeColors[theme];

        // Dispatch event for other components
        document.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));

        // Show toast notification
        this.showToast(`Theme changed to ${theme === 'dark' ? 'dark mode' : theme}`);
    },

    quickToggle() {
        // Quick toggle between light and dark
        const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    },

    watchSystemTheme() {
        // Check if user prefers dark mode at system level
        if (window.matchMedia) {
            const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');

            // Only apply if no saved preference
            if (!localStorage.getItem('theme')) {
                this.setTheme(darkModeQuery.matches ? 'dark' : 'light');
            }

            // Watch for changes
            darkModeQuery.addListener((e) => {
                if (!localStorage.getItem('theme')) {
                    this.setTheme(e.matches ? 'dark' : 'light');
                }
            });
        }
    },

    showToast(message) {
        const toast = document.createElement('div');
        toast.className = 'toast show';
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 100px;
            right: 20px;
            background: var(--primary-color);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 10000;
            animation: slideInRight 0.3s ease;
        `;

        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 2000);
    }
};

// Keyboard shortcut for quick theme toggle
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Shift + D for dark mode toggle
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'D') {
        e.preventDefault();
        ThemeSwitcher.quickToggle();
    }
});

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => ThemeSwitcher.init());
} else {
    ThemeSwitcher.init();
}

// Export for use in other modules
window.ThemeSwitcher = ThemeSwitcher;
