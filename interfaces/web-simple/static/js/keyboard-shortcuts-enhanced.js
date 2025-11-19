/* ============================================
   Enhanced Keyboard Shortcuts System
   ============================================ */

const KeyboardShortcuts = {
    shortcuts: {
        // Navigation
        'ctrl+h': { action: 'goHome', description: 'Go to home page', category: 'Navigation' },
        'ctrl+b': { action: 'goBack', description: 'Go back', category: 'Navigation' },
        'ctrl+k': { action: 'focusSearch', description: 'Focus search', category: 'Navigation' },
        'alt+1': { action: 'goToTeam', description: 'Go to team dashboard', category: 'Navigation' },

        // Document Actions
        'ctrl+s': { action: 'saveDocument', description: 'Save draft', category: 'Document' },
        'ctrl+shift+s': { action: 'saveAndClose', description: 'Save and close', category: 'Document' },
        'ctrl+p': { action: 'previewDocument', description: 'Preview document', category: 'Document' },
        'ctrl+e': { action: 'exportDocument', description: 'Export document', category: 'Document' },
        'ctrl+shift+e': { action: 'emailDocument', description: 'Email document', category: 'Document' },

        // Editing
        'ctrl+z': { action: 'undo', description: 'Undo', category: 'Editing' },
        'ctrl+shift+z': { action: 'redo', description: 'Redo', category: 'Editing' },
        'ctrl+f': { action: 'findInDocument', description: 'Find in document', category: 'Editing' },
        'ctrl+shift+v': { action: 'showVersionHistory', description: 'Version history', category: 'Editing' },

        // View
        'ctrl+shift+d': { action: 'toggleDarkMode', description: 'Toggle dark mode', category: 'View' },
        'ctrl+shift+t': { action: 'toggleThemeSelector', description: 'Theme selector', category: 'View' },
        'ctrl+shift+k': { action: 'showKeyboardShortcuts', description: 'Show shortcuts', category: 'View' },
        'ctrl+shift+n': { action: 'toggleNotifications', description: 'Notifications', category: 'View' },

        // Quick Actions
        'ctrl+n': { action: 'newDocument', description: 'New document', category: 'Quick Actions' },
        'ctrl+q': { action: 'quickReport', description: 'Quick report', category: 'Quick Actions' },
        'ctrl+shift+a': { action: 'showAnalytics', description: 'Analytics', category: 'Quick Actions' },
        'ctrl+shift+x': { action: 'adminPanel', description: 'Admin panel', category: 'Quick Actions' },

        // System
        'escape': { action: 'closeModals', description: 'Close modals/dialogs', category: 'System' },
        'shift+?': { action: 'showHelp', description: 'Show help', category: 'System' }
    },

    commandPalette: null,
    isListening: true,

    init() {
        this.registerShortcuts();
        this.createHelpPanel();
        this.createCommandPalette();

        // Listen for ? key to show shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === '?' && e.shiftKey) {
                e.preventDefault();
                this.showHelp Panel();
            }
        });
    },

    registerShortcuts() {
        document.addEventListener('keydown', (e) => {
            if (!this.isListening) return;

            // Don't trigger in input fields unless it's a special key
            if ((e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') &&
                !e.ctrlKey && !e.metaKey && !e.altKey) {
                return;
            }

            const key = this.getKeyCombo(e);
            const shortcut = this.shortcuts[key];

            if (shortcut) {
                e.preventDefault();
                this.executeAction(shortcut.action, e);
            }
        });
    },

    getKeyCombo(event) {
        const parts = [];
        if (event.ctrlKey || event.metaKey) parts.push('ctrl');
        if (event.altKey) parts.push('alt');
        if (event.shiftKey) parts.push('shift');

        let key = event.key.toLowerCase();
        if (key === ' ') key = 'space';

        parts.push(key);
        return parts.join('+');
    },

    executeAction(action, event) {
        const actions = {
            // Navigation
            goHome: () => window.location.href = '/',
            goBack: () => window.history.back(),
            focusSearch: () => {
                const searchInput = document.querySelector('#searchInput, [placeholder*="Search"]');
                if (searchInput) {
                    searchInput.focus();
                    if (window.toggleSearch) window.toggleSearch();
                }
            },
            goToTeam: () => {
                const teamLinks = document.querySelectorAll('a[href^="/team/"]');
                if (teamLinks.length > 0) teamLinks[0].click();
            },

            // Document Actions
            saveDocument: () => {
                if (window.saveDraft) window.saveDraft();
                else if (document.querySelector('[onclick*="saveDraft"]')) {
                    document.querySelector('[onclick*="saveDraft"]').click();
                }
            },
            saveAndClose: () => {
                if (window.saveDraft) window.saveDraft();
                setTimeout(() => window.history.back(), 500);
            },
            previewDocument: () => {
                if (window.previewDocument) window.previewDocument();
                else if (document.querySelector('[onclick*="preview"]')) {
                    document.querySelector('[onclick*="preview"]').click();
                }
            },
            exportDocument: () => {
                if (window.exportDocument) window.exportDocument();
            },
            emailDocument: () => {
                if (window.sendEmail) window.sendEmail();
            },

            // Editing
            undo: () => {
                // Browser default - don't prevent
            },
            redo: () => {
                // Browser default - don't prevent
            },
            findInDocument: () => {
                // Browser default - don't prevent
            },
            showVersionHistory: () => {
                if (window.VersionHistory) {
                    const docId = window.location.pathname.split('/').pop() || 'current';
                    window.VersionHistory.showVersionHistory(docId, '');
                }
            },

            // View
            toggleDarkMode: () => {
                if (window.ThemeSwitcher) window.ThemeSwitcher.quickToggle();
            },
            toggleThemeSelector: () => {
                if (window.ThemeSwitcher) window.ThemeSwitcher.toggleThemeSelector();
            },
            showKeyboardShortcuts: () => this.showHelpPanel(),
            toggleNotifications: () => {
                if (window.toggleNotifications) window.toggleNotifications();
            },

            // Quick Actions
            newDocument: () => {
                const newBtn = document.querySelector('a[href*="/template/"]');
                if (newBtn) newBtn.click();
            },
            quickReport: () => {
                if (window.showQuickReport) window.showQuickReport();
            },
            showAnalytics: () => {
                window.location.href = '/analytics';
            },
            adminPanel: () => {
                window.location.href = '/admin';
            },

            // System
            closeModals: () => {
                document.querySelectorAll('.modal').forEach(m => m.remove());
                document.querySelectorAll('[style*="display: flex"]').forEach(el => {
                    if (el.classList.contains('modal') || el.classList.contains('overlay')) {
                        el.style.display = 'none';
                    }
                });
            },
            showHelp: () => this.showHelpPanel()
        };

        if (actions[action]) {
            actions[action]();
            this.showToast(`⌨️ ${action}`);
        }
    },

    createHelpPanel() {
        // Create help panel HTML
        const panel = document.createElement('div');
        panel.id = 'keyboardShortcutsPanel';
        panel.className = 'modal';
        panel.style.display = 'none';
        panel.innerHTML = `
            <div class="modal-content large">
                <div class="modal-header">
                    <h2>⌨️ Keyboard Shortcuts</h2>
                    <button class="modal-close" onclick="this.closest('.modal').style.display='none'">&times;</button>
                </div>
                <div class="modal-body">
                    <p style="color: var(--gray-600); margin-bottom: var(--spacing-xl);">
                        Press <kbd>?</kbd> or <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>K</kbd> to show this panel anytime
                    </p>

                    ${Object.entries(this.groupByCategory()).map(([category, shortcuts]) => `
                        <div class="shortcuts-category">
                            <h3>${category}</h3>
                            <div class="shortcuts-list">
                                ${shortcuts.map(s => `
                                    <div class="shortcut-item">
                                        <div class="shortcut-keys">
                                            ${this.formatKeyCombo(s.key)}
                                        </div>
                                        <div class="shortcut-description">${s.description}</div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    `).join('')}

                    <div class="shortcuts-tip" style="margin-top: var(--spacing-2xl); padding: var(--spacing-lg); background: var(--primary-light); border-radius: var(--border-radius);">
                        <strong>💡 Pro Tip:</strong> Press <kbd>Ctrl</kbd>+<kbd>K</kbd> to open the command palette for quick access to any action!
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(panel);

        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            .shortcuts-category {
                margin-bottom: var(--spacing-2xl);
            }

            .shortcuts-category h3 {
                color: var(--primary-color);
                margin-bottom: var(--spacing-lg);
                padding-bottom: var(--spacing-sm);
                border-bottom: 2px solid var(--primary-color);
            }

            .shortcuts-list {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
                gap: var(--spacing-md);
            }

            .shortcut-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: var(--spacing-md);
                background: var(--gray-50);
                border-radius: var(--border-radius-sm);
            }

            .shortcut-keys {
                display: flex;
                gap: 4px;
            }

            .shortcut-keys kbd {
                padding: 4px 8px;
                background: white;
                border: 1px solid var(--gray-400);
                border-radius: 4px;
                font-size: 0.85rem;
                font-weight: 600;
                box-shadow: 0 2px 0 var(--gray-400);
            }

            .shortcut-description {
                color: var(--gray-700);
            }
        `;
        document.head.appendChild(style);
    },

    showHelpPanel() {
        const panel = document.getElementById('keyboardShortcutsPanel');
        if (panel) {
            panel.style.display = 'flex';
        }
    },

    createCommandPalette() {
        // Command palette for quick actions
        const palette = document.createElement('div');
        palette.id = 'commandPalette';
        palette.className = 'modal';
        palette.style.display = 'none';
        palette.innerHTML = `
            <div class="modal-content" style="margin-top: 100px; max-width: 600px;">
                <div style="position: relative;">
                    <input type="text" id="commandPaletteInput"
                           placeholder="Type a command..."
                           style="width: 100%; padding: 20px; font-size: 1.2rem; border: none; border-radius: var(--border-radius);">
                    <div id="commandPaletteResults" style="max-height: 400px; overflow-y: auto;"></div>
                </div>
            </div>
        `;

        document.body.appendChild(palette);

        // Add command palette listener
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                this.showCommandPalette();
            }
        });

        // Search functionality
        document.addEventListener('input', (e) => {
            if (e.target.id === 'commandPaletteInput') {
                this.searchCommands(e.target.value);
            }
        });

        // Close on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && palette.style.display === 'flex') {
                palette.style.display = 'none';
            }
        });
    },

    showCommandPalette() {
        const palette = document.getElementById('commandPalette');
        palette.style.display = 'flex';

        const input = document.getElementById('commandPaletteInput');
        input.value = '';
        input.focus();

        this.searchCommands('');
    },

    searchCommands(query) {
        const results = document.getElementById('commandPaletteResults');
        const lowerQuery = query.toLowerCase();

        const allCommands = Object.entries(this.shortcuts).map(([key, shortcut]) => ({
            key,
            ...shortcut
        }));

        const filtered = query ?
            allCommands.filter(cmd =>
                cmd.description.toLowerCase().includes(lowerQuery) ||
                cmd.action.toLowerCase().includes(lowerQuery)
            ) : allCommands.slice(0, 10);

        results.innerHTML = filtered.map(cmd => `
            <div class="command-item" onclick="KeyboardShortcuts.executeAction('${cmd.action}'); document.getElementById('commandPalette').style.display='none';">
                <div>
                    <strong>${cmd.description}</strong>
                    <div style="font-size: 0.85rem; color: var(--gray-600);">${cmd.category}</div>
                </div>
                <div class="shortcut-keys">
                    ${this.formatKeyCombo(cmd.key)}
                </div>
            </div>
        `).join('');

        // Add command-item styles
        if (!document.getElementById('command-palette-styles')) {
            const style = document.createElement('style');
            style.id = 'command-palette-styles';
            style.textContent = `
                .command-item {
                    padding: var(--spacing-md);
                    cursor: pointer;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    transition: background var(--transition-fast);
                }

                .command-item:hover {
                    background: var(--primary-light);
                }
            `;
            document.head.appendChild(style);
        }
    },

    formatKeyCombo(combo) {
        return combo.split('+').map(key => {
            const keyMap = {
                'ctrl': '⌘',
                'shift': '⇧',
                'alt': '⌥',
                'escape': 'Esc'
            };
            return `<kbd>${keyMap[key] || key.toUpperCase()}</kbd>`;
        }).join(' ');
    },

    groupByCategory() {
        const grouped = {};
        Object.entries(this.shortcuts).forEach(([key, shortcut]) => {
            if (!grouped[shortcut.category]) {
                grouped[shortcut.category] = [];
            }
            grouped[shortcut.category].push({ key, ...shortcut });
        });
        return grouped;
    },

    showToast(message) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--gray-900);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: var(--shadow-lg);
            z-index: 10000;
            animation: fadeInOut 2s ease;
        `;

        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 2000);

        if (!document.getElementById('toast-animation')) {
            const style = document.createElement('style');
            style.id = 'toast-animation';
            style.textContent = `
                @keyframes fadeInOut {
                    0%, 100% { opacity: 0; transform: translateY(20px); }
                    10%, 90% { opacity: 1; transform: translateY(0); }
                }
            `;
            document.head.appendChild(style);
        }
    },

    disable() {
        this.isListening = false;
    },

    enable() {
        this.isListening = true;
    }
};

// Auto-initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => KeyboardShortcuts.init());
} else {
    KeyboardShortcuts.init();
}

// Export
window.KeyboardShortcuts = KeyboardShortcuts;
