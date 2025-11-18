/* ============================================
   Dashboard JavaScript
   NUAA Web Tools
   ============================================ */

// Dashboard state
const dashboardState = {
    currentTeam: null,
    documents: [],
    drafts: [],
    stats: {}
};

// Utility functions
const utils = {
    formatDate: (dateString) => {
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays === 0) return 'Today';
        if (diffDays === 1) return 'Yesterday';
        if (diffDays < 7) return `${diffDays} days ago`;

        return date.toLocaleDateString();
    },

    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    showToast: (message, type = 'info') => {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);

        setTimeout(() => toast.classList.add('show'), 10);

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },

    copyToClipboard: async (text) => {
        try {
            await navigator.clipboard.writeText(text);
            utils.showToast('Copied to clipboard!', 'success');
        } catch (err) {
            console.error('Failed to copy:', err);
            utils.showToast('Failed to copy', 'error');
        }
    }
};

// Local storage manager
const storage = {
    getDrafts: (teamId) => {
        return JSON.parse(localStorage.getItem(`drafts_${teamId}`) || '[]');
    },

    saveDraft: (teamId, draft) => {
        const drafts = storage.getDrafts(teamId);
        drafts.push({
            id: Date.now(),
            ...draft,
            timestamp: new Date().toISOString()
        });
        localStorage.setItem(`drafts_${teamId}`, JSON.stringify(drafts));
        return drafts.length;
    },

    deleteDraft: (teamId, draftId) => {
        const drafts = storage.getDrafts(teamId);
        const filtered = drafts.filter(d => d.id !== draftId);
        localStorage.setItem(`drafts_${teamId}`, JSON.stringify(filtered));
    },

    getSettings: () => {
        return JSON.parse(localStorage.getItem('settings') || '{}');
    },

    saveSetting: (key, value) => {
        const settings = storage.getSettings();
        settings[key] = value;
        localStorage.setItem('settings', JSON.stringify(settings));
    },

    getRecentSearches: () => {
        return JSON.parse(localStorage.getItem('recentSearches') || '[]');
    },

    addRecentSearch: (query) => {
        const searches = storage.getRecentSearches();
        searches.unshift(query);
        // Keep only last 10 searches
        if (searches.length > 10) searches.pop();
        localStorage.setItem('recentSearches', JSON.stringify(searches));
    }
};

// API calls
const api = {
    getStats: async (teamId) => {
        try {
            const response = await fetch(`/api/stats/${teamId}`);
            if (!response.ok) throw new Error('Failed to fetch stats');
            return await response.json();
        } catch (error) {
            console.error('Error fetching stats:', error);
            // Return default stats if API fails
            return {
                total: 0,
                recent: 0,
                drafts: storage.getDrafts(teamId).length
            };
        }
    },

    getDocuments: async (teamId, limit = 10) => {
        try {
            const response = await fetch(`/api/documents/${teamId}?limit=${limit}`);
            if (!response.ok) throw new Error('Failed to fetch documents');
            return await response.json();
        } catch (error) {
            console.error('Error fetching documents:', error);
            return { documents: [] };
        }
    },

    getTemplateUsage: async (teamId, templateName) => {
        try {
            const response = await fetch(`/api/template-usage/${teamId}/${templateName}`);
            if (!response.ok) return 0;
            const data = await response.json();
            return data.usage || 0;
        } catch (error) {
            return 0;
        }
    },

    searchDocuments: async (teamId, query) => {
        try {
            const response = await fetch(`/api/search/${teamId}?q=${encodeURIComponent(query)}`);
            if (!response.ok) throw new Error('Failed to search');
            return await response.json();
        } catch (error) {
            console.error('Error searching:', error);
            return { results: [] };
        }
    }
};

// Event handlers
const handlers = {
    showQuickReport: () => {
        const modal = document.getElementById('quickReportModal');
        if (modal) {
            modal.style.display = 'flex';
            document.getElementById('quickReportText')?.focus();
        }
    },

    closeQuickReport: () => {
        const modal = document.getElementById('quickReportModal');
        if (modal) modal.style.display = 'none';
    },

    submitQuickReport: async () => {
        const textarea = document.getElementById('quickReportText');
        const teamId = dashboardState.currentTeam;

        if (!textarea || !teamId) return;

        const text = textarea.value.trim();
        if (!text) {
            utils.showToast('Please enter some content', 'warning');
            return;
        }

        try {
            const response = await fetch('/quick-submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    team_id: teamId,
                    data: text,
                    timestamp: new Date().toISOString()
                })
            });

            const result = await response.json();

            if (result.success) {
                utils.showToast('Quick report submitted!', 'success');
                handlers.closeQuickReport();
                textarea.value = '';
                // Refresh stats and documents
                loadDashboard(teamId);
            }
        } catch (error) {
            console.error('Error submitting quick report:', error);
            utils.showToast('Failed to submit report', 'error');
        }
    },

    saveDraft: () => {
        const textarea = document.getElementById('quickReportText');
        const teamId = dashboardState.currentTeam;

        if (!textarea || !teamId) return;

        const text = textarea.value.trim();
        if (!text) return;

        const draftCount = storage.saveDraft(teamId, {
            type: 'quick-report',
            content: text
        });

        utils.showToast('Draft saved!', 'success');
        handlers.closeQuickReport();
        textarea.value = '';

        // Update draft count
        const draftCountEl = document.getElementById('draftCount');
        if (draftCountEl) draftCountEl.textContent = draftCount;
    },

    showDrafts: () => {
        const teamId = dashboardState.currentTeam;
        const drafts = storage.getDrafts(teamId);

        if (drafts.length === 0) {
            utils.showToast('No saved drafts', 'info');
            return;
        }

        // Create drafts modal
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.style.display = 'flex';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2>Saved Drafts (${drafts.length})</h2>
                    <button class="modal-close" onclick="this.closest('.modal').remove()">&times;</button>
                </div>
                <div class="modal-body">
                    ${drafts.map(draft => `
                        <div class="draft-item" style="padding: 15px; border-bottom: 1px solid var(--gray-200);">
                            <div style="display: flex; justify-content: space-between; align-items: start;">
                                <div style="flex: 1;">
                                    <strong>${draft.type || 'Draft'}</strong>
                                    <p style="margin: 5px 0; color: var(--gray-600);">${draft.content.substring(0, 100)}...</p>
                                    <small style="color: var(--gray-500);">${utils.formatDate(draft.timestamp)}</small>
                                </div>
                                <div style="display: flex; gap: 10px;">
                                    <button class="btn secondary" onclick="handlers.loadDraft(${draft.id})">Load</button>
                                    <button class="btn danger" onclick="handlers.deleteDraft(${draft.id})">Delete</button>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    },

    loadDraft: (draftId) => {
        const teamId = dashboardState.currentTeam;
        const drafts = storage.getDrafts(teamId);
        const draft = drafts.find(d => d.id === draftId);

        if (draft) {
            const textarea = document.getElementById('quickReportText');
            if (textarea) {
                textarea.value = draft.content;
                handlers.showQuickReport();
                document.querySelector('.modal')?.remove();
            }
        }
    },

    deleteDraft: (draftId) => {
        if (confirm('Delete this draft?')) {
            const teamId = dashboardState.currentTeam;
            storage.deleteDraft(teamId, draftId);
            utils.showToast('Draft deleted', 'success');
            document.querySelector('.modal')?.remove();
            handlers.showDrafts();
        }
    },

    toggleSearch: () => {
        const overlay = document.getElementById('searchOverlay');
        if (!overlay) return;

        const isVisible = overlay.style.display !== 'none';
        overlay.style.display = isVisible ? 'none' : 'block';

        if (!isVisible) {
            document.getElementById('searchInput')?.focus();
        }
    },

    performSearch: utils.debounce(async (event) => {
        const query = event.target.value.trim();
        const resultsContainer = document.getElementById('searchResults');

        if (!query || !resultsContainer) return;

        if (query.length < 2) {
            resultsContainer.innerHTML = '';
            return;
        }

        storage.addRecentSearch(query);

        const teamId = dashboardState.currentTeam;
        const { results } = await api.searchDocuments(teamId, query);

        if (results.length === 0) {
            resultsContainer.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--gray-500);">No results found</div>';
            return;
        }

        resultsContainer.innerHTML = results.map(result => `
            <div class="search-result-item" style="padding: 15px; border-bottom: 1px solid var(--gray-200); cursor: pointer;"
                 onclick="window.location.href='/document/${result.id}'">
                <strong>${result.title || result.name}</strong>
                <p style="margin: 5px 0; color: var(--gray-600); font-size: 0.9em;">${result.snippet || ''}</p>
                <small style="color: var(--gray-500);">${utils.formatDate(result.date)}</small>
            </div>
        `).join('');
    }, 300),

    toggleNotifications: () => {
        const panel = document.getElementById('notificationPanel');
        if (!panel) return;

        const isVisible = panel.style.display !== 'none';
        panel.style.display = isVisible ? 'none' : 'block';

        if (!isVisible) {
            // Mark as read
            const badge = document.getElementById('notificationBadge');
            if (badge) badge.style.display = 'none';
        }
    },

    switchView: (view) => {
        document.querySelectorAll('.toggle-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        const button = document.querySelector(`[data-view="${view}"]`);
        if (button) button.classList.add('active');

        const container = document.getElementById('templatesContainer');
        if (container) {
            if (view === 'list') {
                container.classList.add('list-view');
            } else {
                container.classList.remove('list-view');
            }
        }

        storage.saveSetting('templatesView', view);
    },

    favoriteTemplate: (templateName) => {
        event.stopPropagation();
        const favorites = JSON.parse(localStorage.getItem('favoriteTemplates') || '[]');

        if (favorites.includes(templateName)) {
            const index = favorites.indexOf(templateName);
            favorites.splice(index, 1);
            utils.showToast('Removed from favorites', 'info');
        } else {
            favorites.push(templateName);
            utils.showToast('Added to favorites', 'success');
        }

        localStorage.setItem('favoriteTemplates', JSON.stringify(favorites));
    },

    shareTemplate: (templateName) => {
        event.stopPropagation();
        const url = `${window.location.origin}/template/${dashboardState.currentTeam}/${templateName}`;
        utils.copyToClipboard(url);
    }
};

// Make handlers globally available
Object.assign(window, {
    showQuickReport: handlers.showQuickReport,
    closeQuickReport: handlers.closeQuickReport,
    submitQuickReport: handlers.submitQuickReport,
    saveDraft: handlers.saveDraft,
    showDrafts: handlers.showDrafts,
    toggleSearch: handlers.toggleSearch,
    toggleNotifications: handlers.toggleNotifications,
    performSearch: handlers.performSearch,
    switchView: handlers.switchView,
    favoriteTemplate: handlers.favoriteTemplate,
    shareTemplate: handlers.shareTemplate,
    handlers: handlers
});

// Dashboard initialization
async function loadDashboard(teamId) {
    dashboardState.currentTeam = teamId;

    // Load stats
    const stats = await api.getStats(teamId);
    dashboardState.stats = stats;

    // Update UI
    const totalDocsEl = document.getElementById('totalDocs');
    const recentDocsEl = document.getElementById('recentDocs');
    const draftCountEl = document.getElementById('draftCount');

    if (totalDocsEl) totalDocsEl.textContent = stats.total || 0;
    if (recentDocsEl) recentDocsEl.textContent = stats.recent || 0;
    if (draftCountEl) draftCountEl.textContent = stats.drafts || 0;

    // Load recent documents
    const { documents } = await api.getDocuments(teamId, 5);
    dashboardState.documents = documents;

    const recentContainer = document.getElementById('recentDocuments');
    if (recentContainer && documents.length > 0) {
        recentContainer.innerHTML = documents.map(doc => `
            <div class="document-item">
                <span class="doc-icon">📄</span>
                <div class="doc-info">
                    <h4>${doc.name || 'Untitled'}</h4>
                    <span class="doc-date">${utils.formatDate(doc.date)}</span>
                </div>
                <div class="doc-actions">
                    <button onclick="viewDocument('${doc.id}')" class="btn secondary">View</button>
                    <button onclick="exportDocument('${doc.id}')" class="btn secondary">Export</button>
                </div>
            </div>
        `).join('');
    }

    // Restore view preference
    const savedView = storage.getSettings().templatesView || 'grid';
    handlers.switchView(savedView);
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K for search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        handlers.toggleSearch();
    }

    // Ctrl/Cmd + Q for quick report
    if ((e.ctrlKey || e.metaKey) && e.key === 'q') {
        e.preventDefault();
        handlers.showQuickReport();
    }

    // Escape to close modals
    if (e.key === 'Escape') {
        handlers.closeQuickReport();
        const searchOverlay = document.getElementById('searchOverlay');
        if (searchOverlay) searchOverlay.style.display = 'none';
        const notificationPanel = document.getElementById('notificationPanel');
        if (notificationPanel) notificationPanel.style.display = 'none';
    }
});

// Export for other scripts
window.dashboardUtils = utils;
window.dashboardState = dashboardState;
window.storage = storage;
window.api = api;

console.log('✅ Dashboard JS loaded');
