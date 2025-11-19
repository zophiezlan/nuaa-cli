/* ============================================
   Keyboard Shortcuts Overlay
   Help users discover and use keyboard shortcuts
   ============================================ */

class KeyboardShortcutsOverlay {
    constructor() {
        this.shortcuts = [
            {
                category: 'Navigation',
                items: [
                    { keys: ['Ctrl', 'K'], description: 'Open search', mac: ['⌘', 'K'] },
                    { keys: ['Ctrl', 'H'], description: 'Go to home', mac: ['⌘', 'H'] },
                    { keys: ['Alt', '←'], description: 'Go back', mac: ['⌥', '←'] },
                    { keys: ['Tab'], description: 'Navigate forward' },
                    { keys: ['Shift', 'Tab'], description: 'Navigate backward' },
                ]
            },
            {
                category: 'Actions',
                items: [
                    { keys: ['Ctrl', 'S'], description: 'Save draft', mac: ['⌘', 'S'] },
                    { keys: ['Ctrl', 'Enter'], description: 'Submit form', mac: ['⌘', '↵'] },
                    { keys: ['Ctrl', 'Q'], description: 'Quick report', mac: ['⌘', 'Q'] },
                    { keys: ['Ctrl', 'P'], description: 'Preview document', mac: ['⌘', 'P'] },
                    { keys: ['Ctrl', 'N'], description: 'New document', mac: ['⌘', 'N'] },
                ]
            },
            {
                category: 'Interface',
                items: [
                    { keys: ['?'], description: 'Show keyboard shortcuts' },
                    { keys: ['Esc'], description: 'Close modal/overlay' },
                    { keys: ['Ctrl', '/'], description: 'Focus search', mac: ['⌘', '/'] },
                    { keys: ['Alt', 'A'], description: 'Accessibility menu', mac: ['⌥', 'A'] },
                ]
            },
            {
                category: 'Editing',
                items: [
                    { keys: ['Ctrl', 'Z'], description: 'Undo', mac: ['⌘', 'Z'] },
                    { keys: ['Ctrl', 'Y'], description: 'Redo', mac: ['⌘', 'Y'] },
                    { keys: ['Ctrl', 'A'], description: 'Select all', mac: ['⌘', 'A'] },
                    { keys: ['Ctrl', 'C'], description: 'Copy', mac: ['⌘', 'C'] },
                    { keys: ['Ctrl', 'V'], description: 'Paste', mac: ['⌘', 'V'] },
                ]
            }
        ];

        this.isVisible = false;
        this.overlay = null;
        this.isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;

        this.init();
    }

    init() {
        // Listen for ? key to show overlay
        document.addEventListener('keydown', (e) => {
            if (e.key === '?' && !this.isInputFocused()) {
                e.preventDefault();
                this.toggle();
            } else if (e.key === 'Escape' && this.isVisible) {
                this.hide();
            }
        });

        this.addStyles();
    }

    isInputFocused() {
        const activeElement = document.activeElement;
        return activeElement && (
            activeElement.tagName === 'INPUT' ||
            activeElement.tagName === 'TEXTAREA' ||
            activeElement.isContentEditable
        );
    }

    addStyles() {
        const style = document.createElement('style');
        style.id = 'keyboard-shortcuts-styles';
        style.textContent = `
            .keyboard-shortcuts-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.75);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10001;
                padding: 20px;
                animation: fadeIn 0.2s ease;
            }

            .keyboard-shortcuts-content {
                background: white;
                border-radius: 12px;
                max-width: 900px;
                width: 100%;
                max-height: 90vh;
                overflow-y: auto;
                box-shadow: 0 10px 50px rgba(0, 0, 0, 0.3);
                animation: slideUp 0.3s ease;
            }

            .keyboard-shortcuts-header {
                padding: 24px 32px;
                border-bottom: 1px solid #e8e8e8;
                display: flex;
                align-items: center;
                justify-content: space-between;
                position: sticky;
                top: 0;
                background: white;
                z-index: 1;
                border-radius: 12px 12px 0 0;
            }

            .keyboard-shortcuts-header h2 {
                margin: 0;
                color: #333;
                display: flex;
                align-items: center;
                gap: 12px;
            }

            .keyboard-shortcuts-close {
                background: none;
                border: none;
                font-size: 28px;
                color: #999;
                cursor: pointer;
                width: 32px;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 4px;
                transition: all 0.2s;
            }

            .keyboard-shortcuts-close:hover {
                background: #f5f5f5;
                color: #333;
            }

            .keyboard-shortcuts-body {
                padding: 32px;
            }

            .keyboard-shortcuts-category {
                margin-bottom: 32px;
            }

            .keyboard-shortcuts-category:last-child {
                margin-bottom: 0;
            }

            .keyboard-shortcuts-category h3 {
                color: #2c5aa0;
                margin-bottom: 16px;
                font-size: 18px;
                font-weight: 600;
            }

            .keyboard-shortcuts-list {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 12px;
            }

            .keyboard-shortcut-item {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 12px 16px;
                background: #f9f9f9;
                border-radius: 8px;
                transition: background 0.2s;
            }

            .keyboard-shortcut-item:hover {
                background: #e8f4f8;
            }

            .keyboard-shortcut-description {
                color: #666;
                font-size: 14px;
            }

            .keyboard-shortcut-keys {
                display: flex;
                gap: 6px;
                flex-shrink: 0;
                margin-left: 12px;
            }

            .keyboard-key {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                min-width: 28px;
                height: 28px;
                padding: 0 8px;
                background: white;
                border: 1px solid #ddd;
                border-bottom-width: 3px;
                border-radius: 4px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
                font-weight: 600;
                color: #333;
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
            }

            .keyboard-shortcuts-footer {
                padding: 20px 32px;
                border-top: 1px solid #e8e8e8;
                background: #f9f9f9;
                text-align: center;
                color: #666;
                font-size: 14px;
                border-radius: 0 0 12px 12px;
            }

            .keyboard-shortcuts-tip {
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 16px;
                margin-top: 24px;
                border-radius: 4px;
            }

            .keyboard-shortcuts-tip strong {
                color: #856404;
            }

            .keyboard-shortcuts-tip p {
                margin: 0;
                color: #856404;
                font-size: 14px;
            }

            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            @keyframes slideUp {
                from {
                    transform: translateY(30px);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
            }

            @media (max-width: 768px) {
                .keyboard-shortcuts-content {
                    max-height: 100vh;
                    border-radius: 0;
                }

                .keyboard-shortcuts-list {
                    grid-template-columns: 1fr;
                }

                .keyboard-shortcuts-header,
                .keyboard-shortcuts-body,
                .keyboard-shortcuts-footer {
                    padding-left: 20px;
                    padding-right: 20px;
                }
            }

            /* Reduced motion support */
            @media (prefers-reduced-motion: reduce) {
                .keyboard-shortcuts-overlay,
                .keyboard-shortcuts-content {
                    animation: none;
                }
            }
        `;
        document.head.appendChild(style);
    }

    createOverlay() {
        const overlay = document.createElement('div');
        overlay.className = 'keyboard-shortcuts-overlay';
        overlay.setAttribute('role', 'dialog');
        overlay.setAttribute('aria-modal', 'true');
        overlay.setAttribute('aria-labelledby', 'shortcuts-title');

        const categoriesHTML = this.shortcuts.map(category => `
            <div class="keyboard-shortcuts-category">
                <h3>${category.icon || ''} ${category.category}</h3>
                <div class="keyboard-shortcuts-list">
                    ${category.items.map(item => {
                        const keys = this.isMac && item.mac ? item.mac : item.keys;
                        return `
                            <div class="keyboard-shortcut-item">
                                <span class="keyboard-shortcut-description">${item.description}</span>
                                <div class="keyboard-shortcut-keys">
                                    ${keys.map(key => `
                                        <kbd class="keyboard-key">${key}</kbd>
                                    `).join(' ')}
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        `).join('');

        overlay.innerHTML = `
            <div class="keyboard-shortcuts-content">
                <div class="keyboard-shortcuts-header">
                    <h2 id="shortcuts-title">
                        <span>⌨️</span>
                        Keyboard Shortcuts
                    </h2>
                    <button class="keyboard-shortcuts-close"
                            aria-label="Close shortcuts overlay"
                            onclick="window.keyboardShortcuts.hide()">
                        ×
                    </button>
                </div>
                <div class="keyboard-shortcuts-body">
                    ${categoriesHTML}
                    <div class="keyboard-shortcuts-tip">
                        <strong>💡 Tip:</strong>
                        <p>Press <kbd class="keyboard-key">?</kbd> anytime to show this guide. Most shortcuts work throughout the application.</p>
                    </div>
                </div>
                <div class="keyboard-shortcuts-footer">
                    Press <kbd class="keyboard-key">Esc</kbd> to close
                </div>
            </div>
        `;

        // Click outside to close
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                this.hide();
            }
        });

        return overlay;
    }

    show() {
        if (this.isVisible) return;

        this.overlay = this.createOverlay();
        document.body.appendChild(this.overlay);
        this.isVisible = true;

        // Focus the close button for keyboard users
        setTimeout(() => {
            const closeBtn = this.overlay.querySelector('.keyboard-shortcuts-close');
            closeBtn.focus();
        }, 100);

        // Prevent body scrolling
        document.body.style.overflow = 'hidden';

        // Track with analytics if available
        if (window.NUAA && window.NUAA.analytics) {
            window.NUAA.analytics.trackEvent('UI', 'show_keyboard_shortcuts', 'overlay');
        }
    }

    hide() {
        if (!this.isVisible || !this.overlay) return;

        this.overlay.remove();
        this.overlay = null;
        this.isVisible = false;

        // Restore body scrolling
        document.body.style.overflow = '';
    }

    toggle() {
        if (this.isVisible) {
            this.hide();
        } else {
            this.show();
        }
    }

    // Add a shortcut dynamically
    addShortcut(category, shortcut) {
        const cat = this.shortcuts.find(c => c.category === category);
        if (cat) {
            cat.items.push(shortcut);
        } else {
            this.shortcuts.push({
                category,
                items: [shortcut]
            });
        }
    }
}

// Create global instance
window.keyboardShortcuts = new KeyboardShortcutsOverlay();

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = KeyboardShortcutsOverlay;
}
