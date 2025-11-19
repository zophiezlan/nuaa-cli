/* ============================================
   Enhanced Navigation System
   Breadcrumbs, mobile menu, and improved navigation
   ============================================ */

class NavigationSystem {
    constructor() {
        this.breadcrumbs = [];
        this.init();
    }

    init() {
        this.setupBreadcrumbs();
        this.setupMobileMenu();
        this.setupKeyboardNavigation();
        this.addStyles();
    }

    addStyles() {
        const style = document.createElement('style');
        style.id = 'navigation-styles';
        style.textContent = `
            /* Breadcrumb Navigation */
            .breadcrumb-nav {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 12px 0;
                font-size: 14px;
                flex-wrap: wrap;
            }

            .breadcrumb-item {
                display: flex;
                align-items: center;
                gap: 8px;
                color: #666;
            }

            .breadcrumb-item a {
                color: #2c5aa0;
                text-decoration: none;
                transition: color 0.2s;
            }

            .breadcrumb-item a:hover {
                color: #1e3a6e;
                text-decoration: underline;
            }

            .breadcrumb-item.active {
                color: #333;
                font-weight: 500;
            }

            .breadcrumb-separator {
                color: #ccc;
                user-select: none;
            }

            /* Mobile Menu */
            .mobile-menu-toggle {
                display: none;
                background: none;
                border: none;
                font-size: 24px;
                cursor: pointer;
                padding: 8px;
                color: #333;
            }

            .mobile-menu {
                position: fixed;
                top: 0;
                right: -100%;
                width: 280px;
                height: 100vh;
                background: white;
                box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
                z-index: 10000;
                transition: right 0.3s ease;
                overflow-y: auto;
            }

            .mobile-menu.open {
                right: 0;
            }

            .mobile-menu-header {
                padding: 20px;
                border-bottom: 1px solid #e8e8e8;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }

            .mobile-menu-header h3 {
                margin: 0;
                color: #2c5aa0;
            }

            .mobile-menu-close {
                background: none;
                border: none;
                font-size: 28px;
                cursor: pointer;
                color: #999;
                padding: 0;
                width: 32px;
                height: 32px;
            }

            .mobile-menu-nav {
                padding: 20px;
            }

            .mobile-menu-item {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 12px 16px;
                color: #333;
                text-decoration: none;
                border-radius: 8px;
                transition: background 0.2s;
                margin-bottom: 8px;
            }

            .mobile-menu-item:hover {
                background: #e8f4f8;
            }

            .mobile-menu-item-icon {
                font-size: 20px;
                width: 24px;
                text-align: center;
            }

            .mobile-menu-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                z-index: 9999;
                display: none;
            }

            .mobile-menu-overlay.open {
                display: block;
            }

            /* Skip to content link */
            .skip-to-content {
                position: absolute;
                top: -100px;
                left: 20px;
                background: #2c5aa0;
                color: white;
                padding: 12px 24px;
                border-radius: 4px;
                text-decoration: none;
                z-index: 10002;
                transition: top 0.3s;
                font-weight: 500;
            }

            .skip-to-content:focus {
                top: 20px;
            }

            /* Navigation helpers */
            .nav-helper {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: #2c5aa0;
                color: white;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                transition: all 0.3s;
                z-index: 1000;
                border: none;
                font-size: 20px;
            }

            .nav-helper:hover {
                background: #1e3a6e;
                transform: scale(1.1);
            }

            .nav-helper.scroll-to-top {
                opacity: 0;
                pointer-events: none;
            }

            .nav-helper.scroll-to-top.visible {
                opacity: 1;
                pointer-events: all;
            }

            @media (max-width: 768px) {
                .mobile-menu-toggle {
                    display: block;
                }

                .nav-actions > *:not(.mobile-menu-toggle) {
                    display: none;
                }

                .breadcrumb-nav {
                    font-size: 12px;
                }
            }

            /* Keyboard navigation highlights */
            body.keyboard-navigation *:focus {
                outline: 3px solid #2c5aa0;
                outline-offset: 2px;
            }

            /* Reduced motion support */
            @media (prefers-reduced-motion: reduce) {
                .mobile-menu,
                .skip-to-content {
                    transition: none;
                }
            }
        `;
        document.head.appendChild(style);
    }

    setupBreadcrumbs() {
        // Auto-generate breadcrumbs from URL
        const path = window.location.pathname;
        const parts = path.split('/').filter(p => p);

        this.breadcrumbs = [{ label: 'Home', url: '/' }];

        let currentPath = '';
        parts.forEach((part, index) => {
            currentPath += '/' + part;

            // Format the label
            let label = part.replace(/-/g, ' ').replace(/_/g, ' ');
            label = label.charAt(0).toUpperCase() + label.slice(1);

            this.breadcrumbs.push({
                label,
                url: currentPath,
                active: index === parts.length - 1
            });
        });

        this.renderBreadcrumbs();
    }

    renderBreadcrumbs() {
        // Find existing breadcrumb container or create one
        let container = document.querySelector('.breadcrumb-nav');

        if (!container) {
            // Create breadcrumb nav
            container = document.createElement('nav');
            container.className = 'breadcrumb-nav';
            container.setAttribute('aria-label', 'Breadcrumb');

            // Insert after top navigation
            const topNav = document.querySelector('.top-nav');
            if (topNav) {
                topNav.after(container);
            }
        }

        // Render breadcrumbs
        container.innerHTML = this.breadcrumbs.map((crumb, index) => {
            const isLast = index === this.breadcrumbs.length - 1;

            return `
                <div class="breadcrumb-item ${isLast ? 'active' : ''}">
                    ${!isLast ? `<a href="${crumb.url}">${crumb.label}</a>` : crumb.label}
                    ${!isLast ? '<span class="breadcrumb-separator" aria-hidden="true">›</span>' : ''}
                </div>
            `;
        }).join('');
    }

    setupMobileMenu() {
        // Create mobile menu HTML
        const menuHTML = `
            <div class="mobile-menu-overlay"></div>
            <div class="mobile-menu">
                <div class="mobile-menu-header">
                    <h3>Menu</h3>
                    <button class="mobile-menu-close" aria-label="Close menu">×</button>
                </div>
                <nav class="mobile-menu-nav">
                    <a href="/" class="mobile-menu-item">
                        <span class="mobile-menu-item-icon">🏠</span>
                        <span>Home</span>
                    </a>
                    <a href="/accessibility" class="mobile-menu-item">
                        <span class="mobile-menu-item-icon">♿</span>
                        <span>Accessibility</span>
                    </a>
                    <a href="#" onclick="window.keyboardShortcuts.show(); return false;" class="mobile-menu-item">
                        <span class="mobile-menu-item-icon">⌨️</span>
                        <span>Keyboard Shortcuts</span>
                    </a>
                    <a href="/help/general" class="mobile-menu-item">
                        <span class="mobile-menu-item-icon">❓</span>
                        <span>Help & Support</span>
                    </a>
                </nav>
            </div>
        `;

        // Add to body
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = menuHTML;
        document.body.appendChild(tempDiv);

        // Setup mobile menu toggle
        const navActions = document.querySelector('.nav-actions');
        if (navActions) {
            const toggleBtn = document.createElement('button');
            toggleBtn.className = 'mobile-menu-toggle';
            toggleBtn.setAttribute('aria-label', 'Open menu');
            toggleBtn.innerHTML = '☰';
            toggleBtn.onclick = () => this.toggleMobileMenu();
            navActions.appendChild(toggleBtn);
        }

        // Setup close handlers
        document.querySelector('.mobile-menu-close').onclick = () => this.closeMobileMenu();
        document.querySelector('.mobile-menu-overlay').onclick = () => this.closeMobileMenu();
    }

    toggleMobileMenu() {
        const menu = document.querySelector('.mobile-menu');
        const overlay = document.querySelector('.mobile-menu-overlay');

        menu.classList.toggle('open');
        overlay.classList.toggle('open');

        // Prevent body scroll when menu is open
        if (menu.classList.contains('open')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    }

    closeMobileMenu() {
        const menu = document.querySelector('.mobile-menu');
        const overlay = document.querySelector('.mobile-menu-overlay');

        menu.classList.remove('open');
        overlay.classList.remove('open');
        document.body.style.overflow = '';
    }

    setupKeyboardNavigation() {
        // Detect if user is navigating with keyboard
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });

        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigation');
        });

        // Add skip to content link
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.className = 'skip-to-content';
        skipLink.textContent = 'Skip to main content';
        document.body.insertBefore(skipLink, document.body.firstChild);

        // Ensure main content has ID
        let main = document.querySelector('main');
        if (main && !main.id) {
            main.id = 'main-content';
            main.setAttribute('tabindex', '-1');
        }

        // Setup scroll to top button
        this.setupScrollToTop();
    }

    setupScrollToTop() {
        const button = document.createElement('button');
        button.className = 'nav-helper scroll-to-top';
        button.innerHTML = '↑';
        button.setAttribute('aria-label', 'Scroll to top');
        button.onclick = () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        };
        document.body.appendChild(button);

        // Show/hide based on scroll position
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                button.classList.add('visible');
            } else {
                button.classList.remove('visible');
            }
        });
    }
}

// Initialize navigation
document.addEventListener('DOMContentLoaded', () => {
    window.navigation = new NavigationSystem();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NavigationSystem;
}
